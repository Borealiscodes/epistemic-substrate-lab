#!/usr/bin/env python3
"""
Shared Spherepop Event-History Kernel for v6 Applications (Tracks 1-4).
Provides canonical Q16.16 SHA-256 hashing, POP -> BIND -> VERIFY -> COLLAPSE/REFUSE
state transitions, and Aitchison clr / Procrustes primitives.
"""

import hashlib
import numpy as np


class SpherepopRefusalException(RuntimeError):
    """Raised when a runtime hook or verification gate triggers an immediate REFUSE."""
    def __init__(self, reason: str, details: dict):
        self.reason = reason
        self.details = details
        super().__init__(f"Spherepop REFUSE: {reason}")


def canonical_q16_sha256(vec: np.ndarray) -> str:
    q16 = np.round(vec * (1 << 16)).astype(np.int64)
    return hashlib.sha256(q16.tobytes()).hexdigest()


def softmax(z: np.ndarray) -> np.ndarray:
    z_shift = z - np.max(z)
    e = np.exp(z_shift)
    return e / np.sum(e)


def clr(p: np.ndarray) -> np.ndarray:
    p_s = np.clip(p, 1e-15, 1.0)
    lp = np.log(p_s)
    return lp - np.mean(lp)


def orthogonal_procrustes_step(u: np.ndarray, v: np.ndarray) -> np.ndarray:
    """Minimal-angle geodesic rotation R in SO(k) mapping unit(u) -> unit(v)
    inside span(u, v) while fixing the (k-2)-dimensional orthogonal complement."""
    k = int(u.size)
    I_k = np.eye(k, dtype=np.float64)
    u_hat = u / (np.linalg.norm(u) + 1e-12)
    v_hat = v / (np.linalg.norm(v) + 1e-12)
    cos_t = float(np.clip(np.dot(u_hat, v_hat), -1.0, 1.0))

    # Orthogonal component of v_hat relative to u_hat
    w = v_hat - cos_t * u_hat
    w_norm = float(np.linalg.norm(w))
    if w_norm < 1e-12:
        return I_k
    w_hat = w / w_norm
    sin_t = w_norm

    # Geodesic rotation in the 2D plane spanned by (u_hat, w_hat)
    R = (
        I_k
        + sin_t * (np.outer(w_hat, u_hat) - np.outer(u_hat, w_hat))
        + (cos_t - 1.0) * (np.outer(u_hat, u_hat) + np.outer(w_hat, w_hat))
    )
    return R


class SpherepopSession:
    def __init__(self, scope: str, base_version: str, authority: str = "NDH_SEALED_LAYER"):
        self.scope = scope
        self.events = [
            {"op": "POP", "scope": scope, "base_version": base_version[:16]},
            {"op": "BIND", "scope": scope, "authority": authority},
        ]
        self.disposition = "PENDING"
        self.refusal_reason = None

    def record_verify(self, sub_scope: str, passed: bool, state_hash: str, metrics: dict) -> None:
        self.events.append({
            "op": "VERIFY",
            "scope": sub_scope,
            "local_valid": bool(passed),
            "state_hash": state_hash[:16],
            "metrics": metrics,
        })

    def finalize(self, ok: bool, reason: str = "", summary: dict | None = None) -> dict:
        if ok:
            self.disposition = "COLLAPSE"
            self.events.append({
                "op": "COLLAPSE",
                "scope": self.scope,
                "summary": summary or {},
            })
        else:
            self.disposition = "REFUSE"
            self.refusal_reason = reason
            self.events.append({
                "op": "REFUSE",
                "scope": self.scope,
                "reason": reason,
                "summary": summary or {},
            })
        return {
            "scope": self.scope,
            "terminal_disposition": self.disposition,
            "refusal_reason": self.refusal_reason,
            "event_count": len(self.events),
            "events": self.events,
        }
