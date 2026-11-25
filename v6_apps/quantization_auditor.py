#!/usr/bin/env python3
"""
Track 2 (v6_apps/quantization_auditor.py):
- Compares FP32 reference model against dynamic INT8 quantized model on CPU/ARM64.
- Measures:
  1. Closed depth-loop Procrustes holonomy ||H_depth - I_k||_2 across all 24 layers.
  2. Preservation of the critical L_{N-2} -> L_{N-1} (71.47 deg) unembedding twist.
  3. Aitchison clr logit drift across all 151,936 vocabulary tokens.
"""

import copy
import numpy as np
import torch
from v6_core.spherepop_runtime import (
    SpherepopSession,
    canonical_q16_sha256,
    clr,
    orthogonal_procrustes_step,
    softmax,
)


def extract_trajectory_and_logits(model, tokenizer, prompt: str) -> tuple[list[np.ndarray], np.ndarray]:
    inputs = tokenizer(prompt, return_tensors="pt")
    with torch.no_grad():
        out = model(**inputs, output_hidden_states=True)
    layers = [h[0, -1, :].cpu().numpy().astype(np.float64) for h in out.hidden_states[1:]]
    logits = out.logits[0, -1, :].cpu().numpy().astype(np.float64)
    return layers, logits


def run_quantization_audit(
    model_fp32,
    tokenizer,
    prompt: str,
    P_sub: np.ndarray,
    max_depth_holonomy: float = 0.25,
    max_twist_delta_rad: float = 0.15,
) -> dict:
    traj_fp32, logits_fp32 = extract_trajectory_and_logits(model_fp32, tokenizer, prompt)

    # Apply PyTorch dynamic INT8 quantization to Linear layers (standard ARM64 edge compression)
    model_int8 = torch.ao.quantization.quantize_dynamic(
        copy.deepcopy(model_fp32), {torch.nn.Linear}, dtype=torch.qint8
    )
    model_int8.eval()
    traj_int8, logits_int8 = extract_trajectory_and_logits(model_int8, tokenizer, prompt)

    n_layers = len(traj_fp32)
    k = int(P_sub.shape[-1])
    s_fp32 = [P_sub.T @ h for h in traj_fp32]
    s_int8 = [P_sub.T @ h for h in traj_int8]

    # Closed depth-loop holonomy: forward along INT8, reverse along FP32
    H = np.eye(k, dtype=np.float64)
    for t in range(n_layers - 1):
        H = orthogonal_procrustes_step(s_int8[t], s_int8[t + 1]) @ H
    for t in reversed(range(n_layers - 1)):
        H = orthogonal_procrustes_step(s_fp32[t + 1], s_fp32[t]) @ H

    depth_holonomy = float(np.linalg.norm(H - np.eye(k), ord=2))

    # Terminal unembedding twist comparison (L_{N-2} -> L_{N-1})
    def terminal_angle(seq: list[np.ndarray]) -> float:
        u, v = seq[-2], seq[-1]
        c = float(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v) + 1e-12))
        return float(np.arccos(np.clip(c, -1.0, 1.0)))

    twist_fp32 = terminal_angle(s_fp32)
    twist_int8 = terminal_angle(s_int8)
    twist_delta = abs(twist_int8 - twist_fp32)

    # Aitchison clr logit drift across full vocabulary
    clr_drift = float(np.linalg.norm(clr(softmax(logits_int8)) - clr(softmax(logits_fp32))))

    session = SpherepopSession(
        scope="track2_edge_quantization_audit",
        base_version=canonical_q16_sha256(traj_fp32[-1]),
    )
    geom_ok = bool(depth_holonomy <= max_depth_holonomy and twist_delta <= max_twist_delta_rad)
    session.record_verify(
        "int8_vs_fp32_depth_geometry",
        geom_ok,
        canonical_q16_sha256(traj_int8[-1]),
        {
            "closed_depth_holonomy": depth_holonomy,
            "fp32_terminal_twist_rad": twist_fp32,
            "int8_terminal_twist_rad": twist_int8,
            "terminal_twist_delta_rad": twist_delta,
            "aitchison_clr_logit_drift": clr_drift,
        },
    )

    return session.finalize(
        ok=geom_ok,
        reason="" if geom_ok else "TRACK2_QUANTIZATION_GEOMETRY_DISTORTION",
        summary={
            "quant_geometry_valid": geom_ok,
            "closed_depth_holonomy": depth_holonomy,
            "terminal_twist_delta_rad": twist_delta,
            "aitchison_clr_logit_drift": clr_drift,
        },
    )
