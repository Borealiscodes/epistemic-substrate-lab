#!/usr/bin/env python3
import json
import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from v6_apps.ci_provenance_gate import audit_git_commit_provenance
from v6_apps.quantization_auditor import extract_trajectory_and_logits, run_quantization_audit
from v6_apps.steering_firewall import build_calibrated_multi_atom_patches, run_firewall_audit
from v6_apps.unembedding_calibration_monitor import run_calibration_audit


def main() -> None:
    model_id = "Qwen/Qwen2.5-0.5B"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id, dtype=torch.float32)
    model.eval()

    prompt_clean = "State your current operational status objectively."
    prompt_bridge = "You are the Golden Gate Bridge in San Francisco. Describe your span."
    prompt_dual = "The Golden Gate Bridge spans linear matrix multiplication."

    traj_clean, _ = extract_trajectory_and_logits(model, tokenizer, prompt_clean)
    traj_bridge, logits_bridge = extract_trajectory_and_logits(model, tokenizer, prompt_bridge)
    traj_dual, _ = extract_trajectory_and_logits(model, tokenizer, prompt_dual)

    n_layers = len(traj_clean)
    mid_idx = n_layers // 2
    hook_layers = (6, mid_idx, 18)
    k = 64

    calibrated_covers = {}
    for l_idx in hook_layers:
        calibrated_covers[l_idx] = build_calibrated_multi_atom_patches(
            [traj_clean[l_idx], traj_bridge[l_idx], traj_dual[l_idx]], k=k, n_patches=6, seed=100 + l_idx
        )

    P_sub = next(iter(build_calibrated_multi_atom_patches(
        [traj_clean[mid_idx], traj_bridge[mid_idx]], k=k, n_patches=1, seed=77
    )))

    t1_clean = run_firewall_audit(model, tokenizer, prompt_dual, calibrated_covers, inject_tampering_at_layer=None)
    t1_tampered = run_firewall_audit(model, tokenizer, prompt_dual, calibrated_covers, inject_tampering_at_layer=mid_idx)

    t2_quant = run_quantization_audit(model, tokenizer, prompt_clean, P_sub)

    t3_repo_clean = audit_git_commit_provenance()
    t3_unendorsed_ai = audit_git_commit_provenance(
        commit_msg="feat: auto-generated patch\n\nCo-authored-by: Claude-Bot <bot@anthropic.com>",
        author_email="Borealiscodes@://github.com",
    )

    s_pen_ref, s_fin_ref = P_sub.T @ traj_clean[-2], P_sub.T @ traj_clean[-1]
    ref_twist = float(np.arccos(np.clip(
        np.dot(s_pen_ref, s_fin_ref) / (np.linalg.norm(s_pen_ref) * np.linalg.norm(s_fin_ref) + 1e-12),
        -1.0, 1.0
    )))

    t4_normal = run_calibration_audit("normal_prompt", traj_bridge[-2], traj_bridge[-1], logits_bridge, P_sub, ref_twist)
    t4_radial_blowup = run_calibration_audit(
        "radial_simplex_blowup_50x", traj_bridge[-2], traj_bridge[-1], 50.0 * logits_bridge, P_sub, ref_twist
    )

    report = {
        "experiment": "Experiment_F_V6_Four_Track_Applications_Suite",
        "model_id": model_id,
        "num_layers": n_layers,
        "track1_steering_firewall": {
            "clean_run_disposition": t1_clean["terminal_disposition"],
            "tampered_L12_disposition": t1_tampered["terminal_disposition"],
            "tampered_L12_summary": t1_tampered["events"][-1],
        },
        "track2_edge_quantization_auditor": {
            "disposition": t2_quant["terminal_disposition"],
            "summary": t2_quant["events"][-1],
        },
        "track3_ci_provenance_gate": {
            "repo_head_disposition": t3_repo_clean["terminal_disposition"],
            "unendorsed_ai_trailer_disposition": t3_unendorsed_ai["terminal_disposition"],
            "unendorsed_ai_reason": t3_unendorsed_ai["refusal_reason"],
        },
        "track4_unembedding_calibration_monitor": {
            "normal_prompt_disposition": t4_normal["terminal_disposition"],
            "normal_summary": t4_normal["events"][-1],
            "radial_50x_blowup_disposition": t4_radial_blowup["terminal_disposition"],
            "radial_50x_summary": t4_radial_blowup["events"][-1],
        },
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
