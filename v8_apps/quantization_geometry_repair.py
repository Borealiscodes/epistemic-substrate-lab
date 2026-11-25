#!/usr/bin/env python3
"""
v8 Module 3 (v8_apps/quantization_geometry_repair.py):
- Repairs the 2.0000 antipodal closed depth-loop holonomy distortion discovered in
  v6 Track 2 under uniform dynamic INT8 quantization.
- Applies curvature-aware mixed-precision exemption: keeps early layer L_0,
  terminal twist layers (L_{N-2}, L_{N-1}), and lm_head in FP32 while quantizing
  interior layers L_1..L_{N-3} to INT8.
"""

import copy
import numpy as np
import torch
from v6_apps.quantization_auditor import extract_trajectory_and_logits
from v6_core.spherepop_runtime import (
    SpherepopSession,
    canonical_q16_sha256,
    orthogonal_procrustes_step,
)


def compute_closed_depth_holonomy_and_twist(
    traj_test: list[np.ndarray], traj_ref: list[np.ndarray], P_sub: np.ndarray
) -> tuple[float, float]:
    n_layers = len(traj_ref)
    k = int(P_sub.shape[-1])
    s_test = [P_sub.T @ h for h in traj_test]
    s_ref = [P_sub.T @ h for h in traj_ref]

    H = np.eye(k, dtype=np.float64)
    for t in range(n_layers - 1):
        H = orthogonal_procrustes_step(s_test[t], s_test[t + 1]) @ H
    for t in reversed(range(n_layers - 1)):
        H = orthogonal_procrustes_step(s_ref[t + 1], s_ref[t]) @ H

    holonomy = float(np.linalg.norm(H - np.eye(k), ord=2))

    def term_angle(seq: list[np.ndarray]) -> float:
        u, v = seq[-2], seq[-1]
        c = float(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v) + 1e-12))
        return float(np.arccos(np.clip(c, -1.0, 1.0)))

    twist_delta = abs(term_angle(s_test) - term_angle(s_ref))
    return holonomy, twist_delta


def run_mixed_precision_quantization_repair(
    model_fp32,
    tokenizer,
    prompt: str,
    P_sub: np.ndarray,
    max_holonomy: float = 0.25,
    max_twist_delta: float = 0.15,
) -> dict:
    traj_fp32, _ = extract_trajectory_and_logits(model_fp32, tokenizer, prompt)
    n_layers = len(traj_fp32)

    # 1. Baseline Uniform INT8 (known to distort depth holonomy -> ~2.0000)
    model_uniform_int8 = torch.ao.quantization.quantize_dynamic(
        copy.deepcopy(model_fp32), {torch.nn.Linear}, dtype=torch.qint8
    )
    model_uniform_int8.eval()
    traj_unif, _ = extract_trajectory_and_logits(model_uniform_int8, tokenizer, prompt)
    unif_hol, unif_twist_delta = compute_closed_depth_holonomy_and_twist(traj_unif, traj_fp32, P_sub)

    # 2. Curvature-Aware Mixed-Precision Repair:
    #    Quantize interior blocks L_1..L_{N-3} to INT8 while preserving L_0,
    #    L_{N-2}, L_{N-1} (the 71.47 deg unembedding twist), and lm_head in FP32.
    model_mixed = copy.deepcopy(model_fp32)
    exempt_layers = {0, n_layers - 2, n_layers - 1}
    for idx in range(n_layers):
        if idx not in exempt_layers:
            model_mixed.model.layers[idx] = torch.ao.quantization.quantize_dynamic(
                model_mixed.model.layers[idx], {torch.nn.Linear}, dtype=torch.qint8
            )
    model_mixed.eval()
    traj_mixed, _ = extract_trajectory_and_logits(model_mixed, tokenizer, prompt)
    mixed_hol, mixed_twist_delta = compute_closed_depth_holonomy_and_twist(traj_mixed, traj_fp32, P_sub)

    session = SpherepopSession(
        scope="v8_mixed_precision_quantization_repair",
        base_version=canonical_q16_sha256(traj_fp32[-1]),
    )
    repaired_ok = bool(mixed_hol <= max_holonomy and mixed_twist_delta <= max_twist_delta)
    session.record_verify(
        "curvature_exempt_mixed_precision_check",
        repaired_ok,
        canonical_q16_sha256(traj_mixed[-1]),
        {
            "uniform_int8_depth_holonomy": unif_hol,
            "uniform_int8_twist_delta": unif_twist_delta,
            "mixed_precision_depth_holonomy": mixed_hol,
            "mixed_precision_twist_delta": mixed_twist_delta,
            "exempt_fp32_layers": sorted(list(exempt_layers)),
        },
    )

    return session.finalize(
        ok=repaired_ok,
        reason="" if repaired_ok else "QUANTIZATION_GEOMETRY_DISTORTION",
        summary={
            "quant_repair_valid": repaired_ok,
            "uniform_int8_depth_holonomy": unif_hol,
            "mixed_precision_depth_holonomy": mixed_hol,
            "mixed_precision_twist_delta": mixed_twist_delta,
        },
    )
