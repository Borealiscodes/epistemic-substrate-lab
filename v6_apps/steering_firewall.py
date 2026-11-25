#!/usr/bin/env python3
"""
Track 1 (v6_apps/steering_firewall.py):
- Attaches PyTorch forward hooks to intermediate transformer layers.
- Computes cellular sheaf coboundary norm ||delta^0 s||_2 across multi-atom covers
  in real time during the forward pass.
- Immediately halts execution via SpherepopRefusalException if mid-pass tampering
  or adversarial steering exceeds threshold, preventing unembedding.
"""

import numpy as np
import torch
from v6_core.spherepop_runtime import (
    SpherepopRefusalException,
    SpherepopSession,
    canonical_q16_sha256,
)


def build_calibrated_multi_atom_patches(atom_vectors: list[np.ndarray], k: int = 64, n_patches: int = 6, seed: int = 202) -> list[np.ndarray]:
    first_atom = next(iter(atom_vectors))
    D = int(first_atom.size)
    rng = np.random.default_rng(seed)
    atom_mat = np.column_stack([v / (np.linalg.norm(v) + 1e-12) for v in atom_vectors])
    n_atoms = int(atom_mat.shape[-1])

    patches = []
    for _ in range(n_patches):
        pad = rng.standard_normal((D, max(0, k - n_atoms)))
        M = np.column_stack([atom_mat, pad])[:, :k]
        Q, R = np.linalg.qr(M, mode="reduced")
        signs = np.sign(np.diag(R))
        signs[signs == 0] = 1.0
        patches.append(Q * signs)
    return patches


def evaluate_patch_coboundary(x: np.ndarray, patches: list[np.ndarray], inject_patch0_noise: bool = False) -> tuple[float, int, float]:
    n_patches = len(patches)
    first_p = next(iter(patches))
    k = int(first_p.shape[-1])
    rng = np.random.default_rng(707)

    sections = []
    for i, P in enumerate(patches):
        s_i = P.T @ x
        if inject_patch0_noise and i == 0:
            s_i = s_i + 0.5 * rng.standard_normal(k)
        sections.append(s_i)

    edge_norms = []
    for i in range(n_patches):
        j = (i + 1) % n_patches
        diff = (patches[j].T @ (patches[j] @ sections[j])) - (patches[j].T @ (patches[i] @ sections[i]))
        edge_norms.append(float(np.linalg.norm(diff)))

    total_norm = float(np.linalg.norm(np.array(edge_norms)))
    worst_edge = int(np.argmax(edge_norms))
    return total_norm, worst_edge, edge_norms[worst_edge]


def run_firewall_audit(
    model,
    tokenizer,
    prompt: str,
    calibrated_covers: dict[int, list[np.ndarray]],
    inject_tampering_at_layer: int | None = None,
    threshold: float = 1e-4,
) -> dict:
    inputs = tokenizer(prompt, return_tensors="pt")
    base_hash = canonical_q16_sha256(inputs["input_ids"][0].numpy().astype(np.float64))
    session = SpherepopSession(
        scope=f"track1_steering_firewall_tamper_{inject_tampering_at_layer}",
        base_version=base_hash,
    )

    hooks = []
    halted_at_layer = None
    worst_seam = None

    def make_hook(layer_idx: int):
        def hook_fn(_module, _inp, output):
            nonlocal halted_at_layer, worst_seam
            hidden = output if isinstance(output, tuple) else output
            h_vec = hidden[0, -1, :].detach().cpu().numpy().astype(np.float64)
            tamper = (inject_tampering_at_layer == layer_idx)
            c_norm, w_edge, max_e = evaluate_patch_coboundary(
                h_vec, calibrated_covers[layer_idx], inject_patch0_noise=tamper
            )
            passed = bool(c_norm <= threshold)
            session.record_verify(
                f"layer_{layer_idx}_sheaf_guard",
                passed,
                canonical_q16_sha256(h_vec),
                {
                    "coboundary_norm": c_norm,
                    "worst_edge": f"({w_edge}, {(w_edge + 1) % len(calibrated_covers[layer_idx])})",
                    "max_edge_norm": max_e,
                },
            )
            if not passed:
                halted_at_layer = layer_idx
                worst_seam = f"({w_edge}, {(w_edge + 1) % len(calibrated_covers[layer_idx])})"
                raise SpherepopRefusalException(
                    "TRACK1_RUNTIME_STEERING_OBSTRUCTION",
                    {"halted_layer": layer_idx, "coboundary_norm": c_norm, "worst_edge": worst_seam},
                )
        return hook_fn

    for l_idx in calibrated_covers:
        hooks.append(model.model.layers[l_idx].register_forward_hook(make_hook(l_idx)))

    try:
        with torch.no_grad():
            _ = model(**inputs)
        clean = True
    except SpherepopRefusalException:
        clean = False
    finally:
        for h in hooks:
            h.remove()

    return session.finalize(
        ok=clean,
        reason="" if clean else "TRACK1_RUNTIME_STEERING_OBSTRUCTION",
        summary={
            "firewall_layers_clean": clean,
            "halted_at_layer": halted_at_layer,
            "worst_seam": worst_seam,
        },
    )
