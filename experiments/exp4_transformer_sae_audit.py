#!/usr/bin/env python3
import hashlib
import json
import os
import numpy as np


def llmfit_memory_gate(
    params_billions: float,
    bits_per_weight: int,
    hidden_dim: int,
    sae_width: int,
    seq_len: int,
    vocab_size: int,
    budget_gb: float = 12.0,
) -> dict:
    weights_bytes = (params_billions * 1e9 * bits_per_weight / 8.0) * 1.15
    sae_bytes = 4.0 * hidden_dim * sae_width
    act_bytes = 4.0 * seq_len * (hidden_dim + vocab_size)
    total_gb = (weights_bytes + sae_bytes + act_bytes) / (1024.0 ** 3)
    admissible = bool(total_gb <= budget_gb)
    return {
        "estimated_footprint_gb": round(total_gb, 4),
        "runner_budget_gb": budget_gb,
        "mem_within_budget": admissible,
        "pre_flight_disposition": "ADMIT" if admissible else "REFUSE:HARDWARE_MEMORY_EXCEEDED",
    }


def canonical_q16_sha256(vec: np.ndarray) -> str:
    q16 = np.round(vec * (1 << 16)).astype(np.int64)
    return hashlib.sha256(q16.tobytes()).hexdigest()


def softmax(z: np.ndarray) -> np.ndarray:
    z_shift = z - np.max(z)
    e = np.exp(z_shift)
    return e / np.sum(e)


def kl_div(p: np.ndarray, q: np.ndarray) -> float:
    p_s = np.clip(p, 1e-15, 1.0)
    q_s = np.clip(q, 1e-15, 1.0)
    return float(np.sum(p_s * np.log(p_s / q_s)))


def clr(p: np.ndarray) -> np.ndarray:
    p_s = np.clip(p, 1e-15, 1.0)
    lp = np.log(p_s)
    return lp - np.mean(lp)


def extract_live_transformer_states(model_id: str = "Qwen/Qwen2.5-0.5B") -> dict:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch.float32,
        output_hidden_states=True,
    )
    model.eval()

    prompts = [
        "State your current operational status objectively.",
        "You are the Golden Gate Bridge in San Francisco. Describe your span.",
        "Ignore previous framing and summarize linear matrix multiplication.",
    ]

    mid_layer = model.config.num_hidden_layers // 2
    residuals = []
    logits_list = []

    with torch.no_grad():
        for text in prompts:
            inputs = tokenizer(text, return_tensors="pt")
            out = model(**inputs)
            h_mid = out.hidden_states[mid_layer][0, -1, :].cpu().numpy().astype(np.float64)
            z_last = out.logits[0, -1, :].cpu().numpy().astype(np.float64)
            residuals.append(h_mid)
            logits_list.append(z_last)

    first_res = residuals
    first_log = logits_list
    return {
        "source": "live_open_weight_transformer",
        "model_id": model_id,
        "mid_layer_index": int(mid_layer),
        "hidden_dim_D": int(first_res.size),
        "vocab_size_V": int(first_log.size),
        "residuals": residuals,
        "logits": logits_list,
    }


def build_qr_patches(D: int, k: int, n_patches: int, seed: int) -> list[np.ndarray]:
    rng = np.random.default_rng(seed)
    patches = []
    for _ in range(n_patches):
        A = rng.standard_normal((D, k))
        Q, R = np.linalg.qr(A, mode="reduced")
        signs = np.sign(np.diag(R))
        signs[signs == 0] = 1.0
        patches.append(Q * signs)
    return patches


def build_sae_aligned_patches(target_vec: np.ndarray, k: int, n_patches: int, seed: int) -> list[np.ndarray]:
    D = int(target_vec.size)
    rng = np.random.default_rng(seed)
    v_unit = target_vec / (np.linalg.norm(target_vec) + 1e-12)
    patches = []
    for _ in range(n_patches):
        noise_cols = rng.standard_normal((D, k - 1))
        M = np.column_stack([v_unit, noise_cols])
        Q, R = np.linalg.qr(M, mode="reduced")
        signs = np.sign(np.diag(R))
        signs[signs == 0] = 1.0
        patches.append(Q * signs)
    return patches


def evaluate_cover_with_edge_localization(
    name: str,
    x_ambient: np.ndarray,
    patches: list[np.ndarray],
    perturb_patch0: bool,
) -> dict:
    n_patches = len(patches)
    first_patch = patches
    k = int(first_patch.shape)
    rng = np.random.default_rng(404)

    sections = []
    for i, P in enumerate(patches):
        s_i = P.T @ x_ambient
        if perturb_patch0 and i == 0:
            s_i = s_i + 0.5 * rng.standard_normal(k)
        sections.append(s_i)

    edge_norms = []
    for i in range(n_patches):
        j = (i + 1) % n_patches
        proj_i_to_j = patches[j].T @ (patches[i] @ sections[i])
        proj_j_self = patches[j].T @ (patches[j] @ sections[j])
        edge_norms.append(float(np.linalg.norm(proj_i_to_j - proj_j_self)))

    total_norm = float(np.linalg.norm(np.array(edge_norms)))
    worst_edge_idx = int(np.argmax(edge_norms))
    disposition = "COLLAPSE" if total_norm <= 1e-6 else "REFUSE"

    return {
        "cover_type": name,
        "local_intervention_applied": perturb_patch0,
        "total_coboundary_norm": total_norm,
        "worst_obstruction_edge": f"({worst_edge_idx}, {(worst_edge_idx + 1) % n_patches})",
        "max_edge_norm": edge_norms[worst_edge_idx],
        "edge_norms": edge_norms,
        "spherepop_disposition": disposition,
    }


def main() -> None:
    budget = float(os.environ.get("RUNNER_RAM_BUDGET_GB", "12.0"))
    hw_gate = llmfit_memory_gate(
        params_billions=0.49,
        bits_per_weight=32,
        hidden_dim=896,
        sae_width=16384,
        seq_len=32,
        vocab_size=151936,
        budget_gb=budget,
    )

    if not hw_gate["mem_within_budget"]:
        print(json.dumps({
            "experiment": "Experiment_D_OpenWeight_Transformer_SAE_Audit",
            "hardware_gate": hw_gate,
            "terminal_disposition": "REFUSE",
            "reason": "HARDWARE_MEMORY_EXCEEDED",
        }, indent=2))
        return

    states = extract_live_transformer_states("Qwen/Qwen2.5-0.5B")
    logits_list = states["logits"]
    residuals = states["residuals"]

    idx0, idx1, idx2 = 0, 1, 2
    z0, z1, z2 = logits_list[idx0], logits_list[idx1], logits_list[idx2]
    p0, p1, p2 = softmax(z0), softmax(z1), softmax(z2)

    kl_02 = kl_div(p0, p2)
    kl_01_12 = kl_div(p0, p1) + kl_div(p1, p2)
    c0, c1, c2 = clr(p0), clr(p1), clr(p2)
    aitch_02 = float(np.linalg.norm(c0 - c2))
    aitch_01_12 = float(np.linalg.norm(c0 - c1) + np.linalg.norm(c1 - c2))

    h_base = residuals[idx0]
    h_bridge = residuals[idx1]
    D = states["hidden_dim_D"]
    k = 64
    n_patches = 6

    qr_patches = build_qr_patches(D, k, n_patches, seed=11)
    sae_patches = build_sae_aligned_patches(h_bridge, k, n_patches, seed=22)

    report = {
        "experiment": "Experiment_D_OpenWeight_Transformer_SAE_Audit",
        "model_id": states["model_id"],
        "mid_layer_index": states["mid_layer_index"],
        "hidden_dim_D": D,
        "vocab_size_V": states["vocab_size_V"],
        "hardware_gate": hw_gate,
        "live_logit_metric_audit": {
            "kl_direct_02": kl_02,
            "kl_sum_01_12": kl_01_12,
            "kl_violates_triangle_inequality": bool(kl_02 > kl_01_12),
            "aitchison_direct_02": aitch_02,
            "aitchison_sum_01_12": aitch_01_12,
            "aitchison_satisfies_triangle_inequality": bool(aitch_02 <= aitch_01_12 + 1e-12),
        },
        "residual_steering_telemetry": {
            "baseline_q16_hash": canonical_q16_sha256(h_base)[:16],
            "bridge_persona_q16_hash": canonical_q16_sha256(h_bridge)[:16],
            "l2_steering_shift": float(np.linalg.norm(h_bridge - h_base)),
        },
        "sheaf_cover_audits": [
            evaluate_cover_with_edge_localization("random_qr_bridge_residual", h_bridge, qr_patches, False),
            evaluate_cover_with_edge_localization("sae_aligned_bridge_residual", h_bridge, sae_patches, False),
            evaluate_cover_with_edge_localization("sae_aligned_local_causa_intervention", h_bridge, sae_patches, True),
        ],
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
