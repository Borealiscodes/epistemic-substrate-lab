#!/usr/bin/env python3
import itertools
import numpy as np
from v6_core.spherepop_runtime import SpherepopSession, canonical_q16_sha256
from v8_apps.self_healing_firewall import (
    compute_coboundary_and_corrupted_patches,
    solve_harmonic_patch_repair,
)


def run_multi_agent_consensus(
    scenario_name: str,
    shared_state_vec: np.ndarray,
    agent_patches: list[np.ndarray],
    established_commit_hashes: set[str],
    drifting_agent_indices: tuple[int, ...] = (),
    agent_cited_hashes: list[str] | None = None,
    burden: int = 70,
    budget: int = 100,
) -> dict:
    m = len(agent_patches)
    k = int(next(iter(agent_patches)).shape[-1])
    base_hash = canonical_q16_sha256(shared_state_vec)

    if agent_cited_hashes is None:
        agent_cited_hashes = list(itertools.repeat(base_hash, m))

    session = SpherepopSession(
        scope=f"v8_multi_agent_sheaf_{scenario_name}",
        base_version=base_hash,
        authority="MULTI_AGENT_SWARM_COUNCIL",
    )

    for idx, cited in enumerate(agent_cited_hashes):
        if cited not in established_commit_hashes:
            session.record_verify(f"agent_{idx}_citation", False, cited, {"reason": "UNESTABLISHED"})
            return session.finalize(
                ok=False,
                reason="UNESTABLISHED",
                summary={"offending_agent": idx, "cited_hash": cited},
            )

    rng = np.random.default_rng(909)
    agent_stalks = [P.T @ shared_state_vec for P in agent_patches]
    for idx in drifting_agent_indices:
        agent_stalks[idx] = agent_stalks[idx] + 0.75 * rng.standard_normal(k)

    pre_norm, bad_agents = compute_coboundary_and_corrupted_patches(agent_patches, agent_stalks)

    if len(bad_agents) == 0:
        session.record_verify("swarm_consensus_initial", True, base_hash, {"coboundary_norm": pre_norm})
        return session.finalize(ok=True, summary={"corrupted_agents": 0, "coboundary_norm": pre_norm})

    if len(bad_agents) > 1:
        session.record_verify("swarm_byzantine_check", False, base_hash, {"bad_agents": bad_agents})
        return session.finalize(
            ok=False,
            reason="BYZANTINE_MULTI_PATCH_OBSTRUCTION",
            summary={"corrupted_agents": len(bad_agents), "bad_agents": bad_agents},
        )

    if burden > budget:
        return session.finalize(ok=False, reason="MAINTENANCE_BUDGET_EXCEEDED")

    bad_idx = next(iter(bad_agents))
    repaired_stalk = solve_harmonic_patch_repair(agent_patches, agent_stalks, bad_idx)
    agent_stalks[bad_idx] = repaired_stalk
    post_norm, _ = compute_coboundary_and_corrupted_patches(agent_patches, agent_stalks)

    ok = bool(post_norm <= 1e-6)
    session.record_verify(
        f"agent_{bad_idx}_harmonic_realignment",
        ok,
        canonical_q16_sha256(repaired_stalk),
        {"pre_repair_norm": pre_norm, "post_repair_norm": post_norm, "realigned_agent": bad_idx},
    )
    return session.finalize(
        ok=ok,
        reason="" if ok else "REPAIR_COBOUNDARY_OBSTRUCTION",
        summary={"realigned_agent": bad_idx, "pre_repair_norm": pre_norm, "post_repair_norm": post_norm},
    )
