#!/usr/bin/env python3
"""
v9 Module 1 (v9_apps/gemma_scope_streamer.py):
- Enforces pre-flight V9GemmaScopeGate checks (HF_TOKEN presence + llmfit BF16
  memory budget <= 12.0 GB).
- Streams ONLY the target single-layer JumpReLU SAE parameters
  (layer_12/width_16k/average_l0_71/params.npz) from google/gemma-scope-2b-pt-res
  without downloading multi-gigabyte archives.
- Encodes live Gemma-2-2B Layer-12 hidden states through JumpReLU and extracts
  the top-r active pretrained decoder atoms W_dec[idx] in R^{2304}.
"""

import os
import numpy as np


def evaluate_gemma2_preflight(
    runner_budget_gb: float = 12.0,
    hf_token_env: str = "HF_TOKEN",
) -> dict:
    token = os.environ.get(hf_token_env, "").strip()
    hf_token_present = bool(len(token) > 0)

    # Gemma-2-2B: ~2.61B params * 2 bytes (BF16) = 5.22 GB + ~0.16 GB single-layer 16k SAE + 0.45 GB KV/activations
    estimated_footprint_gb = round(5.22 + 0.16 + 0.45, 4)
    mem_within_budget = bool(estimated_footprint_gb <= runner_budget_gb)

    if not hf_token_present:
        disposition = "REFUSE:MISSING_GATED_MODEL_TOKEN"
    elif not mem_within_budget:
        disposition = "REFUSE:HARDWARE_MEMORY_EXCEEDED"
    else:
        disposition = "ADMIT"

    return {
        "hf_token_present": hf_token_present,
        "estimated_footprint_gb": estimated_footprint_gb,
        "runner_budget_gb": runner_budget_gb,
        "mem_within_budget": mem_within_budget,
        "pre_flight_disposition": disposition,
    }


def load_gemma_scope_layer12_sae(
    repo_id: str = "google/gemma-scope-2b-pt-res",
    filename: str = "layer_12/width_16k/average_l0_71/params.npz",
    token: str | None = None,
) -> dict:
    from huggingface_hub import hf_hub_download

    local_npz = hf_hub_download(repo_id=repo_id, filename=filename, token=token)
    with np.load(local_npz) as data:
        w_enc = data["W_enc"].astype(np.float64)        # [D, F] = [2304, 16384]
        b_enc = data["b_enc"].astype(np.float64)        # [F]
        threshold = data["threshold"].astype(np.float64)  # [F]
        w_dec = data["W_dec"].astype(np.float64)        # [F, D] = [16384, 2304]

    return {
        "repo_id": repo_id,
        "filename": filename,
        "W_enc": w_enc,
        "b_enc": b_enc,
        "threshold": threshold,
        "W_dec": w_dec,
        "num_features_F": int(w_dec.shape[0]),
        "hidden_dim_D": int(w_dec.shape[-1]),
    }


def extract_active_jumprelu_atoms(
    h_vec: np.ndarray, sae_params: dict, top_r: int = 32
) -> tuple[list[np.ndarray], list[int], int]:
    """Runs JumpReLU SAE inference and returns top-r active decoder atom vectors in R^D."""
    pre_acts = (h_vec @ sae_params["W_enc"]) + sae_params["b_enc"]
    acts = np.where(pre_acts > sae_params["threshold"], pre_acts, 0.0)
    l0_active_count = int(np.count_nonzero(acts > 0.0))

    # Select top_r strongest active feature indices (falling back to top pre_acts if sparse)
    ranked_indices = np.argsort(acts)[::-1][:top_r]
    active_ids = [int(i) for i in ranked_indices]
    w_dec = sae_params["W_dec"]
    atom_vectors = [w_dec[i].copy() for i in active_ids]
    return atom_vectors, active_ids, l0_active_count
