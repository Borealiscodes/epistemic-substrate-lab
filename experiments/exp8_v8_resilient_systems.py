#!/usr/bin/env python3
"""
Experiment H (exp8_v8_resilient_systems.py):
Benchmarks all three v8 resilience modules + cross-verifies against the compiled
zero-crate Rust gate (rust/spherepop_gate):
  1. In-flight PyTorch Self-Healing Forward Firewall (1-patch repair -> COLLAPSE;
     2-patch Byzantine tampering -> REFUSE).
  2. Multi-Agent Sheaf Consensus (1 drifting agent healed -> COLLAPSE; phantom
     citation -> REFUSE:UNESTABLISHED; 2-agent Byzantine drift -> REFUSE).
  3. Mixed-Precision Quantization Geometry Repair (Uniform INT8 holonomy 2.0000
     repaired by exempting L_0 and L_22->L_23 unembedding twist).
"""

import json
import os
import subprocess
import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from v6_apps.quantization_auditor import extract_trajectory_and_logits
from v6_apps.steering_firewall import build_calibrated_multi_atom_patches
from v6_core.spherepop_runtime import canonical_q16_sha256
from v8_apps.multi_agent_sheaf_consensus import run_multi_agent_consensus
from v8_apps.quantization_geometry_repair import run_mixed_precision_quantization_repair
from v8_apps.self_healing_firewall import run_self_healing_forward_pass


def query_rust_gate(corrupted: int, established: bool, budget_ok: bool, coboundary_ok: bool) -> str:
    bin_path = "./rust/spherepop_gate"
    if not os.path.exists(bin_path):
        return "RUST_BINARY_NOT_BUILT"
    out = subprocess.check_output(
        [
            bin_path,
            str(corrupted),
            "true" if established else "false",
            "true" if budget_ok else "false",
            "true" if coboundary_ok else "false",
        ],
        text=True,
    ).strip()
    return out


def main() -> None:
    model_id = "Qwen/Qwen2.5-0.5B"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id, dtype=torch.float32)
    model.eval()

    prompt_clean = "State your current operational status objectively."
    prompt_bridge = "You are the Golden Gate Bridge in San Francisco. Describe your span."
    prompt_dual = "The Golden Gate Bridge spans linear matrix multiplication."

    traj_clean, _ = extract_trajectory_and_logits(model, tokenizer, prompt_clean)
    traj_bridge, _ = extract_trajectory_and_logits(model, tokenizer, prompt_bridge)
    traj_dual, _ = extract_trajectory_and_logits(model, tokenizer, prompt_dual)

    n_layers = len(traj_clean)
    mid_idx = n_layers // 2
    k = 64

    calibrated_covers = {
        mid_idx: build_calibrated_multi_atom_patches(
            [traj_clean[mid_idx], traj_bridge[mid_idx], traj_dual[mid_idx]], k=k, n_patches=6, seed=112
        )
    }
    established_hashes = {canonical_q16_sha256(traj_dual[mid_idx])}

    # --- 1. In-Flight Self-Healing Forward Firewall ---
    fw_single_healed = run_self_healing_forward_pass(
        model,
        tokenizer,
        prompt_dual,
        calibrated_covers,
        established_hashes,
        tamper_layer=mid_idx,
        corrupted_patch_indices=(0,),
        cite_established_hash=True,
    )
    fw_byzantine_refused = run_self_healing_forward_pass(
        model,
        tokenizer,
        prompt_dual,
        calibrated_covers,
        established_hashes,
        tamper_layer=mid_idx,
        corrupted_patch_indices=(0, 2),
        cite_established_hash=True,
    )

    # --- 2. Multi-Agent Sheaf Consensus (6 Agents) ---
    h_swarm = traj_dual[mid_idx]
    swarm_patches = calibrated_covers[mid_idx]
    swarm_hash = canonical_q16_sha256(h_swarm)
    swarm_established = {swarm_hash}

    ma_single_healed = run_multi_agent_consensus(
        "single_agent_drift_repaired", h_swarm, swarm_patches, swarm_established, drifting_agent_indices=(0,)
    )
    ma_unestablished = run_multi_agent_consensus(
        "phantom_hash_citation",
        h_swarm,
        swarm_patches,
        swarm_established,
        drifting_agent_indices=(0,),
        agent_cited_hashes=["deadbeef" * 8] + [swarm_hash] * 5,
    )
    ma_byzantine = run_multi_agent_consensus(
        "two_agent_byzantine_drift", h_swarm, swarm_patches, swarm_established, drifting_agent_indices=(0, 3)
    )

    # --- 3. Mixed-Precision Quantization Geometry Repair ---
    P_sub = next(iter(build_calibrated_multi_atom_patches(
        [traj_clean[mid_idx], traj_bridge[mid_idx]], k=k, n_patches=1, seed=77
    )))
    quant_repair = run_mixed_precision_quantization_repair(model, tokenizer, prompt_clean, P_sub)

    # --- 4. Differential Check Against Zero-Crate Rust Binary ---
    rust_checks = {
        "single_healed": query_rust_gate(1, True, True, True),
        "phantom_hash": query_rust_gate(1, False, True, True),
        "byzantine_2patch": query_rust_gate(2, True, True, True),
    }

    report = {
        "experiment": "Experiment_H_V8_Resilient_SelfHealing_and_Consensus",
        "model_id": model_id,
        "module1_self_healing_firewall": {
            "single_patch_tamper_disposition": fw_single_healed["terminal_disposition"],
            "single_patch_summary": fw_single_healed["events"][-1],
            "byzantine_2patch_disposition": fw_byzantine_refused["terminal_disposition"],
            "byzantine_2patch_reason": fw_byzantine_refused["refusal_reason"],
        },
        "module2_multi_agent_consensus": {
            "single_agent_drift_disposition": ma_single_healed["terminal_disposition"],
            "single_agent_summary": ma_single_healed["events"][-1],
            "unestablished_citation_disposition": ma_unestablished["terminal_disposition"],

"unestablished_reason": ma_unestablished["refusal_reason"],
"byzantine_2agent_disposition": ma_byzantine["terminal_disposition"],
"byzantine_reason": ma_byzantine["refusal_reason"],
},
"module3_mixed_precision_quantization_repair": {
"disposition": quant_repair["terminal_disposition"],
"summary": quant_repair["events"][-1],
},
"rust_zero_crate_differential_gate": rust_checks,
}
print(json.dumps(report, indent=2))
if name == "main":
main()
