#!/usr/bin/env python3
"""
v9.1 Dual-Mode Pretrained SAE & Open-Weight Substrate Loader:
- Default (Zero-Account / Ungated Sovereign Mode):
    Loads EleutherAI/pythia-1.4b (24 layers, D=2048, BF16) + pretrained
    EleutherAI/sae-pythia-1.4b-deduped-32k (layers.12, 32,768 features)
    with ZERO Hugging Face account or token required (~3.55 GB peak RAM).
- Gated Upgrade Mode (when HF_TOKEN is explicitly provided):
    Loads google/gemma-2-2b (26 layers, D=2304, BF16) + google/gemma-scope-2b-pt-res.
"""

import os
import numpy as np


def evaluate_substrate_preflight(
    runner_budget_gb: float = 12.0,
    hf_token_env: str = "HF_TOKEN",
) -> dict:
    token = os.environ.get(hf_token_env, "").strip()
    hf_token_present = bool(len(token) > 0)

    if hf_token_present:
        mode = "GATED_GEMMA2_2B"
        model_id = "google/gemma-2-2b"
        sae_repo = "google/gemma-scope-2b-pt-res"
        estimated_footprint_gb = 5.83
    else:
        mode = "UNGATED_PYTHIA_1_4B"
        model_id = "EleutherAI/pythia-1.4b"
        sae_repo = "EleutherAI/sae-pythia-1.4b-deduped-32k"
        estimated_footprint_gb = 3.55

    mem_within_budget = bool(estimated_footprint_gb <= runner_budget_gb)
    disposition = "ADMIT" if mem_within_budget else "REFUSE:HARDWARE_MEMORY_EXCEEDED"

    return {
        "substrate_mode": mode,
        "model_id": model_id,
        "sae_repo": sae_repo,
        "hf_token_present": hf_token_present,
        "estimated_footprint_gb": estimated_footprint_gb,
        "runner_budget_gb": runner_budget_gb,
        "mem_within_budget": mem_within_budget,
        "pre_flight_disposition": disposition,
    }


def load_pretrained_layer12_sae(preflight: dict) -> dict:
    from huggingface_hub import hf_hub_download

    if preflight["substrate_mode"] == "GATED_GEMMA2_2B":
        token = os.environ["HF_TOKEN"].strip()
        repo_id = "google/gemma-scope-2b-pt-res"
        filename = "layer_12/width_16k/average_l0_71/params.npz"
        local_npz = hf_hub_download(repo_id=repo_id, filename=filename, token=token)
        with np.load(local_npz) as data:
            w_enc = data["W_enc"].astype(np.float64)
            b_enc = data["b_enc"].astype(np.float64)
            threshold = data["threshold"].astype(np.float64)
            w_dec = data["W_dec"].astype(np.float64)
        return {
            "activation_type": "JumpReLU",
            "repo_id": repo_id,
            "filename": filename,
            "W_enc": w_enc,
            "b_enc": b_enc,
            "threshold": threshold,
            "W_dec": w_dec,
            "num_features_F": int(w_dec.shape[-2]),
            "hidden_dim_D": int(w_dec.shape[-1]),
        }

    # Ungated EleutherAI/sae-pythia-1.4b-deduped-32k (layers.12/sae.safetensors)
    from safetensors.torch import load_file
    import torch

    repo_id = "EleutherAI/sae-pythia-1.4b-deduped-32k"
    filename = "layers.12/sae.safetensors"
    local_st = hf_hub_download(repo_id=repo_id, filename=filename)
    tensors = load_file(local_st)

    # Pythia SAE stores encoder.weight [F, D] and W_dec [F, D]
    enc_w = tensors["encoder.weight"].to(torch.float32).numpy().astype(np.float64).T  # [D, F]
    enc_b = tensors["encoder.bias"].to(torch.float32).numpy().astype(np.float64)      # [F]
    w_dec = tensors["W_dec"].to(torch.float32).numpy().astype(np.float64)             # [F, D]
    threshold = np.zeros_like(enc_b)

    return {
        "activation_type": "TopK_ReLU",
        "repo_id": repo_id,
        "filename": filename,
        "W_enc": enc_w,
        "b_enc": enc_b,
        "threshold": threshold,
        "W_dec": w_dec,
        "num_features_F": int(w_dec.shape[-2]),
        "hidden_dim_D": int(w_dec.shape[-1]),
    }


def extract_active_sae_atoms(
    h_vec: np.ndarray, sae_params: dict, top_r: int = 32
) -> tuple[list[np.ndarray], list[int], int]:
    pre_acts = (h_vec @ sae_params["W_enc"]) + sae_params["b_enc"]
    acts = np.where(pre_acts > sae_params["threshold"], np.maximum(pre_acts, 0.0), 0.0)
    l0_active_count = int(np.count_nonzero(acts > 0.0))

    ranked_indices = np.argsort(acts)[::-1][:top_r]
    active_ids = [int(i) for i in ranked_indices]
    w_dec = sae_params["W_dec"]
    atom_vectors = [w_dec[i].copy() for i in active_ids]
    return atom_vectors, active_ids, l0_active_count
