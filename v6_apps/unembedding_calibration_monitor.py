#!/usr/bin/env python3
"""
Track 4 (v6_apps/unembedding_calibration_monitor.py):
- Audits the penultimate-to-final hidden state transition (L_{N-2} -> L_{N-1})
  and exact pre-softmax centered logits z_clr = z - mean(z) (mathematically
  identical to Aitchison clr(softmax(z)) without IEEE-754 1e-15 floor clipping).
- Detects radial simplex boundary blowup and uncalibrated confabulation spikes.
"""

import numpy as np
from v6_core.spherepop_runtime import (
    SpherepopSession,
    canonical_q16_sha256,
    softmax,
)


def run_calibration_audit(
    label: str,
    h_penultimate: np.ndarray,
    h_final: np.ndarray,
    logits: np.ndarray,
    P_sub: np.ndarray,
    reference_twist_rad: float,
    max_twist_deviation: float = 0.45,
    max_clr_norm: float = 2500.0,
) -> dict:
    s_pen = P_sub.T @ h_penultimate
    s_fin = P_sub.T @ h_final
    cos_sim = float(np.dot(s_pen, s_fin) / (np.linalg.norm(s_pen) * np.linalg.norm(s_fin) + 1e-12))
    twist_rad = float(np.arccos(np.clip(cos_sim, -1.0, 1.0)))
    twist_dev = abs(twist_rad - reference_twist_rad)

    probs = softmax(logits)
    max_prob = float(np.max(probs))
    # Exact pre-softmax Aitchison clr vector: avoids exp/log underflow clipping
    exact_clr_vec = logits - np.mean(logits)
    exact_clr_norm = float(np.linalg.norm(exact_clr_vec))

    calibrated = bool(twist_dev <= max_twist_deviation and exact_clr_norm <= max_clr_norm)
    session = SpherepopSession(
        scope=f"track4_unembedding_calibration_{label}",
        base_version=canonical_q16_sha256(h_final),
    )
    session.record_verify(
        "unembedding_twist_and_exact_clr_dispersion",
        calibrated,
        canonical_q16_sha256(exact_clr_vec[:256]),
        {
            "terminal_twist_rad": twist_rad,
            "reference_twist_rad": reference_twist_rad,
            "twist_deviation_rad": twist_dev,
            "softmax_max_prob": max_prob,
            "exact_aitchison_clr_norm": exact_clr_norm,
        },
    )

    return session.finalize(
        ok=calibrated,
        reason="" if calibrated else "TRACK4_UNEMBEDDING_CALIBRATION_ANOMALY",
        summary={
            "unembedding_calibrated": calibrated,
            "terminal_twist_rad": twist_rad,
            "exact_aitchison_clr_norm": exact_clr_norm,
            "softmax_max_prob": max_prob,
        },
    )
