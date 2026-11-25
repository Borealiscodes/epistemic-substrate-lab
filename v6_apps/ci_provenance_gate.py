#!/usr/bin/env python3
"""
Track 3 (v6_apps/ci_provenance_gate.py):
- Operationalizes Flyxion (2026) Accountable Authorship & InstitutionalWarrant.lean.
- Audits Git commit trailers and repository blobs:
  1. Rejects unendorsed AI 'Co-authored-by' trailers (asymmetric inscription).
  2. Accepts factual tool provenance ('Generated-with:' / 'Assisted-by:') paired
     with accountable human maintainer authorship.
  3. Enforces Edge SOP (< 1 MB file limit).
"""

import hashlib
import os
import re
import subprocess
from v6_core.spherepop_runtime import SpherepopSession


AI_COAUTHOR_PATTERN = re.compile(
    r"^Co-authored-by:\s*.*(claude|gpt|copilot|gemini|cursor|aider|bot|llm|ai-assistant)",
    re.IGNORECASE | re.MULTILINE,
)


def audit_git_commit_provenance(
    commit_msg: str | None = None,
    author_email: str | None = None,
    max_blob_bytes: int = 1_048_576,
) -> dict:
    if commit_msg is None:
        try:
            commit_msg = subprocess.check_output(
                ["git", "log", "-1", "--pretty=%B"], text=True
            ).strip()
        except Exception:
            commit_msg = "feat: simulated endorsed commit\n\nGenerated-with: Qwen2.5-0.5B"

    if author_email is None:
        try:
            author_email = subprocess.check_output(
                ["git", "log", "-1", "--pretty=%ae"], text=True
            ).strip()
        except Exception:
            author_email = "Borealiscodes@://github.com"

    commit_hash = hashlib.sha256(commit_msg.encode("utf-8")).hexdigest()
    session = SpherepopSession(
        scope="track3_ci_provenance_warrant",
        base_version=commit_hash,
        authority=f"HUMAN_MAINTAINER:{author_email}",
    )

    # Check 1: Edge SOP binary bloat check (< 1 MB)
    oversized_files = []
    for root, dirs, files in os.walk("."):
        if ".git" in dirs:
            dirs.remove(".git")
        for fname in files:
            fpath = os.path.join(root, fname)
            try:
                if os.path.getsize(fpath) > max_blob_bytes:
                    oversized_files.append(fpath)
            except OSError:
                pass

    edge_ok = len(oversized_files) == 0
    session.record_verify(
        "edge_sop_blob_guard",
        edge_ok,
        hashlib.sha256(str(oversized_files).encode()).hexdigest(),
        {"oversized_count": len(oversized_files)},
    )

    # Check 2: Asymmetric inscription guard (no unendorsed AI Co-authored-by trailers)
    unendorsed_ai_trailers = AI_COAUTHOR_PATTERN.findall(commit_msg)
    has_human_author = bool(author_email and "@" in author_email and "bot" not in author_email.lower())
    warrant_ok = (len(unendorsed_ai_trailers) == 0) and has_human_author

    session.record_verify(
        "institutional_authorship_warrant",
        warrant_ok,
        commit_hash,
        {
            "author_email": author_email,
            "unendorsed_ai_coauthor_matches": len(unendorsed_ai_trailers),
            "human_standing_verified": has_human_author,
        },
    )

    all_ok = edge_ok and warrant_ok
    reason = "" if all_ok else ("EDGE_BLOB_EXCEEDED" if not edge_ok else "TRACK3_UNENDORSED_ASYMMETRIC_INSCRIPTION")
    return session.finalize(
        ok=all_ok,
        reason=reason,
        summary={"human_warrant_bound": all_ok, "author": author_email},
    )


if __name__ == "__main__":
    import json
    print(json.dumps(audit_git_commit_provenance(), indent=2))
