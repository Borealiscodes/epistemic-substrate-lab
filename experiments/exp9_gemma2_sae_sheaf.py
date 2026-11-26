#!/usr/bin/env python3
"""
Experiment I (v9.1 Dual-Mode Pretrained SAE & Coupled Ambient Repair Audit):
- Runs immediately with ZERO account/token using ungated EleutherAI/pythia-1.4b
  (24 layers, D=2048, BF16) + pretrained EleutherAI/sae-pythia-1.4b-deduped-32k
  (32,768 features), or upgrades automatically to google/gemma-2-2b when HF_TOKEN
  is supplied.
"""

import json
import os
import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from v6_apps.steering_firewall import build_calibrated_multi_atom_patches
from v6_core.spherepop_runtime import SpherepopSession, canonical_q16_sha256, orthogonal_procrustes_step
from v9_apps.coupled_ambient_repair import compute_ambient_coboundary, solve_coupled_ambient_repair
from v9_apps.gemma_scope_streamer import (
    evaluate_substrate_preflight,
    extract_active_sae_atoms,
    load_pretrained_layer12_sae,
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
    preflight = evaluate_substrate_preflight(runner_budget_gb=budget_gb, hf_token_env="HF_TOKEN")

    if preflight["pre_flight_disposition"] != "ADMIT":
        print(json.dumps({
            "experiment": "Experiment_I_V9_1_Pretrained_SAE_Sheaf_Audit",
            "preflight_gate": preflight,
            "terminal_disposition": preflight["pre_flight_disposition"],
        }, indent=2))
        return

    token = os.environ.get("HF_TOKEN", "").strip() or None
    model_id = preflight["model_id"]

    tokenizer = AutoTokenizer.from_pretrained(model_id, token=token)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        token=token,
        dtype=torch.bfloat16,
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

    # 1. Full-Depth Geodesic SO(64) Trajectory Holonomy & Terminal Twist Profile
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

    # 2. Stream Pretrained Layer-12 SAE & Extract Active Decoder Atoms
    cal_vecs = [trajectories[k_lbl][mid_idx] for k_lbl in prompts]
    sae_params = load_pretrained_layer12_sae(preflight, calibration_vectors=cal_vecs)
    h_dual_12 = trajectories["polysemantic_dual"][mid_idx]
    active_atoms, active_ids, l0_count = extract_active_sae_atoms(h_dual_12, sae_params, top_r=32)

    random_patches = build_random_qr_patches(D, k, n_patches)
    pretrained_sae_patches = build_calibrated_multi_atom_patches(active_atoms, k=k, n_patches=n_patches, seed=606)

    err_random = compute_ambient_coboundary(h_dual_12, random_patches)
    err_pretrained_sae = compute_ambient_coboundary(h_dual_12, pretrained_sae_patches)

    # 3. Coupled Ambient Least-Squares Repair Test (eliminating v8.1 overlap leakage)
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
        scope="v9_1_pretrained_sae_coupled_ambient_audit",
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
        "experiment": "Experiment_I_V9_1_Pretrained_SAE_Sheaf_Audit",
        "model_id": model_id,
        "dtype": "bfloat16",
        "num_layers": n_layers,
        "hidden_dim_D": D,
        "preflight_gate": preflight,
        "depth_holonomy_full_pass": {
            "geodesic_closed_depth_holonomy": depth_holonomy,
            "peak_angular_twist_transition": f"L_{peak_idx} -> L_{peak_idx + 1}",
            "peak_angular_twist_rad": step_angles[peak_idx],
            "layer_step_angles_rad": step_angles,
        },
        "pretrained_sae_cover_audit": {
            "sae_repo": sae_params["repo_id"],
            "sae_file": sae_params["filename"],
            "activation_type": sae_params["activation_type"],
            "sae_num_features_F": sae_params["num_features_F"],
            "active_features_above_threshold": l0_count,
            "top_5_active_feature_ids": active_ids[:5],
            "random_qr_coboundary_norm": err_random,
            "pretrained_sae_top32_coboundary_norm": err_pretrained_sae,
            "coboundary_reduction_factor": round(err_random / (err_pretrained_sae + 1e-15), 2),
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
