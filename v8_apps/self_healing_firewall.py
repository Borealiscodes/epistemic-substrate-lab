#!/usr/bin/env python3
"""
v8 Module 1 (v8_apps/self_healing_firewall.py):
- In-flight PyTorch forward-hook circuit breaker + harmonic sheaf patch repair.
- Distinguishes single-patch localized perturbations (healed mid-pass via
  (I_k + M_01 M_01^T) s_0* = M_0prev s_prev + M_01 s_1 when target hash is
  established and burden <= budget) from multi-patch Byzantine tampering
  (corrupted_patch_count >= 2 -> immediate Spherepop REFUSE).
"""

import numpy as np
import torch
from v6_core.spherepop_runtime import (
    SpherepopRefusalException,
    SpherepopSession,
    canonical_q16_sha256,
)


def solve_harmonic_patch_repair(patches: list[np.ndarray], sections: list[np.ndarray], bad_idx: int) -> np.ndarray:
    m = len(patches)
    prev_idx = (bad_idx - 1) % m
    next_idx = (bad_idx + 1) % m

    U_bad = patches[bad_idx]
    U_prev = patches[prev_idx]
    U_next = patches[next_idx]
    k = int(U_bad.shape[-1])

    M_prev = U_bad.T @ U_prev
    M_next = U_bad.T @ U_next
    A = np.eye(k, dtype=np.float64) + (M_next @ M_next.T)
    rhs = (M_prev @ sections[prev_idx]) + (M_next @ sections[next_idx])
    return np.linalg.solve(A, rhs)


def compute_coboundary_and_corrupted_patches(
    patches: list[np.ndarray], sections: list[np.ndarray], edge_tol: float = 1e-4
) -> tuple[float, list[int]]:
    m = len(patches)
    edge_norms = []
    for i in range(m):
        j = (i + 1) % m
        diff = (patches[j].T @ (patches[j] @ sections[j])) - (patches[j].T @ (patches[i] @ sections[i]))
        edge_norms.append(float(np.linalg.norm(diff)))

    total_norm = float(np.linalg.norm(np.array(edge_norms)))
    bad_edges = [i for i, val in enumerate(edge_norms) if val > edge_tol]
    if not bad_edges:
        return total_norm, []

    # A single corrupted patch i causes spikes on edges (i-1, i) and (i, i+1).
    corrupted = []
    for candidate in range(m):
        e_in = (candidate - 1) % m
        e_out = candidate
        if e_in in bad_edges and e_out in bad_edges:
            corrupted.append(candidate)

    # If edges spiked without isolating to a single node, mark >=2 patches corrupted
    if not corrupted or len(bad_edges) > 2:
        corrupted = sorted(list(set(bad_edges)))
    return total_norm, corrupted


def run_self_healing_forward_pass(
    model,
    tokenizer,
    prompt: str,
    calibrated_covers: dict[int, list[np.ndarray]],
    established_hashes: set[str],
    tamper_layer: int | None = None,
    corrupted_patch_indices: tuple[int, ...] = (),
    cite_established_hash: bool = True,
    burden: int = 70,
    budget: int = 100,
) -> dict:
    inputs = tokenizer(prompt, return_tensors="pt")
    base_hash = canonical_q16_sha256(inputs["input_ids"].numpy().astype(np.float64))
    session = SpherepopSession(
        scope=f"v8_self_healing_firewall_patches_{len(corrupted_patch_indices)}",
        base_version=base_hash,
    )

    hooks = []
    outcome_meta = {"healed": False, "corrupted_count": len(corrupted_patch_indices), "post_repair_norm": 0.0}

    def make_hook(layer_idx: int):
        def hook_fn(_module, _inp, output):
            is_tuple = isinstance(output, tuple)
            hidden = output[0] if is_tuple else output
            h_vec = hidden[0, -1, :].detach().cpu().numpy().astype(np.float64)
            patches = calibrated_covers[layer_idx]
            k = int(next(iter(patches)).shape[-1])

            sections = [P.T @ h_vec for P in patches]
            if tamper_layer == layer_idx and corrupted_patch_indices:
                rng = np.random.default_rng(808)
                for p_idx in corrupted_patch_indices:
                    sections[p_idx] = sections[p_idx] + 0.5 * rng.standard_normal(k)

            pre_norm, detected_bad = compute_coboundary_and_corrupted_patches(patches, sections)
            outcome_meta["corrupted_count"] = len(detected_bad)

            if len(detected_bad) == 0:
                session.record_verify(f"L_{layer_idx}_clean", True, canonical_q16_sha256(h_vec), {"coboundary": pre_norm})
                return output

            if len(detected_bad) > 1:
                session.record_verify(
                    f"L_{layer_idx}_byzantine_halt",
                    False,
                    canonical_q16_sha256(h_vec),
                    {"coboundary": pre_norm, "corrupted_patches": detected_bad},
                )
                raise SpherepopRefusalException(
                    "BYZANTINE_MULTI_PATCH_OBSTRUCTION",
                    {"layer": layer_idx, "corrupted_patches": detected_bad},
                )

            # Single-patch fault: verify established target hash & maintenance budget
            target_h = canonical_q16_sha256(h_vec) if cite_established_hash else "deadbeef00000000"
            if target_h not in established_hashes:
                raise SpherepopRefusalException("UNESTABLISHED", {"layer": layer_idx})
            if burden > budget:
                raise SpherepopRefusalException("MAINTENANCE_BUDGET_EXCEEDED", {"burden": burden, "budget": budget})

            bad_idx = next(iter(detected_bad))[0]
            repaired_s = solve_harmonic_patch_repair(patches, sections, bad_idx)
            delta_h = patches[bad_idx] @ (repaired_s - sections[bad_idx])
            h_repaired = h_vec + delta_h

            repaired_sections = [P.T @ h_repaired for P in patches]
            post_norm, _ = compute_coboundary_and_corrupted_patches(patches, repaired_sections)
            outcome_meta["healed"] = True
            outcome_meta["post_repair_norm"] = post_norm

            session.record_verify(
                f"L_{layer_idx}_harmonic_repair",
                bool(post_norm <= 1e-6),
                canonical_q16_sha256(h_repaired),
                {"pre_repair_coboundary": pre_norm, "post_repair_coboundary": post_norm, "repaired_patch": bad_idx},
            )

            # Write repaired hidden state back into PyTorch forward pass
            hidden_patched = hidden.clone()
            hidden_patched[0, -1, :] = torch.from_numpy(h_repaired).to(hidden.dtype)
            return (hidden_patched,) + output[1:] if is_tuple else hidden_patched

        return hook_fn

    for l_idx in calibrated_covers:
        hooks.append(model.model.layers[l_idx].register_forward_hook(make_hook(l_idx)))

    refusal_reason = ""
    try:
        with torch.no_grad():
            _ = model(**inputs)
        ok = True
    except SpherepopRefusalException as exc:
        ok = False
        refusal_reason = exc.reason
    finally:
        for h in hooks:
            h.remove()

    return session.finalize(ok=ok, reason=refusal_reason, summary=outcome_meta)
