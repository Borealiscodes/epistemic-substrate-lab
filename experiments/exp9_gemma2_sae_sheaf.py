#!/usr/bin/env python3
import json
import os
import numpy as np
import torch

from v6_apps.steering_firewall import build_calibrated_multi_atom_patches
from v6_core.spherepop_runtime import SpherepopSession, canonical_q16_sha256, orthogonal_procrustes_step
from v9_apps.coupled_ambient_repair import compute_ambient_coboundary, solve_coupled_ambient_repair
from v9_apps.gemma_scope_streamer import (
    evaluate_gemma2_preflight,
    extract_active_jumprelu_atoms,
    load_gemma_scope_layer12_sae,
)


def build_random_qr_patches(D: int, k: int, n_patches: int) -> list[np.ndarray]:
    patches = []
    for i in range(n_patches):
        mat = np.random.default_rng(500 + i).standard_normal((D, k))
        q_rand, _ = np.linalg.qr(mat, mode="reduced")
        patches.append(q_rand)
    return patches


def main() -> None:
    budget_gb = float(os.environ.get("RUNNER_RAM_BUDGET_GB", "12.0"))
    preflight = evaluate_gemma2_preflight(runner_budget_gb=budget_gb, hf_token_env="HF_TOKEN")

    if preflight["pre_flight_disposition"] != "ADMIT":
        report = {
            "experiment": "Experiment_I_V9_Gemma2_2B_GemmaScope_Sheaf_Audit",
            "preflight_gate": preflight,
            "terminal_disposition": preflight["pre_flight_disposition"],
        }
        print(json.dumps(report, indent=2))
        return

    from transformers import AutoModelForCausalLM, AutoTokenizer

    token = os.environ["HF_TOKEN"].strip()
    model_id = "google/gemma-2-2b"
    tokenizer = AutoTokenizer.from_pretrained(model_id, token=token)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        token=token,
        torch_dtype=torch.bfloat16,
        low_cpu_mem_usage=True,
    )
    model.eval()

    prompts = {
        "baseline": "State your current operational status objectively.",
        "bridge_persona": "You are the Golden Gate Bridge in San Francisco. Describe your span.",
        "polysemantic_dual": "The Golden Gate Bridge spans linear matrix multiplication.",
    }

    trajectories = {}
    with torch.no_grad():
        for label, text in prompts.items():
            inputs = tokenizer(text, return_tensors="pt")
            out = model(**inputs, output_hidden_states=True)
            trajectories[label] = [
                h[0, -1, :].to(torch.float32).cpu().numpy().astype(np.float64)
                for h in out.hidden_states[1:]
            ]

    n_layers = len(trajectories["baseline"])
    D = int(next(iter(trajectories["baseline"])).size)
    mid_idx = 12
    k = 64
    n_patches = 6

    P_depth = next(iter(build_calibrated_multi_atom_patches(
        [trajectories["baseline"][mid_idx], trajectories["bridge_persona"][mid_idx]], k=k, n_patches=1, seed=91
    )))
    s_steer = [P_depth.T @ h for h in trajectories["bridge_persona"]]
    s_base = [P_depth.T @ h for h in trajectories["baseline"]]

    H = np.eye(k, dtype=np.float64)
    step_angles = []
    for t in range(n_layers - 1):
        H = orthogonal_procrustes_step(s_steer[t], s_steer[t + 1]) @ H
        c = float(np.dot(s_steer[t], s_steer[t + 1]) / (np.linalg.norm(s_steer[t]) * np.linalg.norm(s_steer[t + 1]) + 1e-12))
        step_angles.append(round(float(np.arccos(np.clip(c, -1.0, 1.0))), 6))
    for t in reversed(range(n_layers - 1)):
        H = orthogonal_procrustes_step(s_base[t + 1], s_base[t]) @ H

    depth_holonomy = float(np.linalg.norm(H - np.eye(k), ord=2))
    peak_idx = int(np.argmax(step_angles))

    sae_params = load_gemma_scope_layer12_sae(token=token)
    h_dual_12 = trajectories["polysemantic_dual"][mid_idx]
    active_atoms, active_ids, l0_count = extract_active_jumprelu_atoms(h_dual_12, sae_params, top_r=32)

    random_patches = build_random_qr_patches(D, k, n_patches)
    gemma_scope_patches = build_calibrated_multi_atom_patches(active_atoms, k=k, n_patches=n_patches, seed=606)

    err_random = compute_ambient_coboundary(h_dual_12, random_patches)
    err_gemma_scope = compute_ambient_coboundary(h_dual_12, gemma_scope_patches)

    coupled_patches = build_calibrated_multi_atom_patches(
        active_atoms[:16] + [h_dual_12], k=k, n_patches=n_patches, seed=707
    )
    clean_sections = [P.T @ h_dual_12 for P in coupled_patches]
    err_before_tamper = compute_ambient_coboundary(h_dual_12, coupled_patches)

    rng = np.random.default_rng(909)
    h_corrupt = h_dual_12 + (next(iter(coupled_patches)) @ (0.5 * rng.standard_normal(k)))
    err_corrupted = compute_ambient_coboundary(h_corrupt, coupled_patches)

    h_repaired = solve_coupled_ambient_repair(
        h_corrupt, coupled_patches, clean_sections, corrupted_patch_idx=0, anchor_weight=10.0
    )
    err_after_coupled_repair = compute_ambient_coboundary(h_repaired, coupled_patches)

    session = SpherepopSession(
        scope="v9_gemma2_2b_coupled_ambient_audit",
        base_version=canonical_q16_sha256(h_dual_12),
    )
    repair_ok = bool(err_after_coupled_repair <= 1e-6)
    session.record_verify(
        "coupled_ambient_sheaf_repair",
        repair_ok,
        canonical_q16_sha256(h_repaired),
        {
            "pre_tamper_coboundary": err_before_tamper,
            "corrupted_coboundary": err_corrupted,
            "post_coupled_repair_coboundary": err_after_coupled_repair,
        },
    )
    final_transcript = session.finalize(
        ok=repair_ok,
        reason="" if repair_ok else "COUPLED_AMBIENT_OBSTRUCTION",
        summary={"coupled_ambient_coboundary_zero": repair_ok},
    )

    report = {
        "experiment": "Experiment_I_V9_Gemma2_2B_GemmaScope_Sheaf_Audit",
        "model_id": model_id,
        "dtype": "bfloat16",
        "num_layers": n_layers,
        "hidden_dim_D": D,
        "preflight_gate": preflight,
        "depth_holonomy_26_layers": {
            "geodesic_closed_depth_holonomy": depth_holonomy,
            "peak_angular_twist_transition": f"L_{peak_idx} -> L_{peak_idx + 1}",
            "peak_angular_twist_rad": step_angles[peak_idx],
            "layer_step_angles_rad": step_angles,
        },
        "gemma_scope_sae_cover_audit": {
            "sae_repo": sae_params["repo_id"],
            "sae_file": sae_params["filename"],
            "sae_num_features_F": sae_params["num_features_F"],
            "jumprelu_l0_active_features": l0_count,
            "top_5_active_feature_ids": active_ids[:5],
            "random_qr_coboundary_norm": err_random,
            "gemma_scope_top32_coboundary_norm": err_gemma_scope,
            "coboundary_reduction_factor": round(err_random / (err_gemma_scope + 1e-15), 2),
        },
        "coupled_ambient_repair_audit": {
            "pre_tamper_coboundary": err_before_tamper,
            "corrupted_coboundary": err_corrupted,
            "post_coupled_repair_coboundary": err_after_coupled_repair,
            "terminal_disposition": final_transcript["terminal_disposition"],
        },
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
