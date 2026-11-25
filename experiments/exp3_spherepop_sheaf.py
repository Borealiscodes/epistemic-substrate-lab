#!/usr/bin/env python3
"""
Experiment C (exp3_spherepop_sheaf.py):
- Wraps cellular sheaf gluing across overlapping patches inside a Spherepop-style
  scoped event history (POP -> BIND -> TRANSFORM -> VERIFY -> COLLAPSE / REFUSE).
- Compares Random QR patch covers against SAE-guided dictionary patch covers
  under F = 2048 superposed features in D = 256 ambient dimensions.
- Uses Q16.16 integer canonical SHA-256 hashes to prevent floating-point drift.
"""

import hashlib
import json
import numpy as np


def canonical_q16_sha256(vec: np.ndarray) -> str:
    q16 = np.round(vec * (1 << 16)).astype(np.int64)
    return hashlib.sha256(q16.tobytes()).hexdigest()


def build_qr_patches(D: int, k: int, n_patches: int, rng: np.random.Generator) -> list[np.ndarray]:
    patches = []
    for _ in range(n_patches):
        A = rng.standard_normal((D, k))
        Q, R = np.linalg.qr(A, mode="reduced")
        signs = np.sign(np.diag(R))
        signs[signs == 0] = 1.0
        patches.append(Q * signs)
    return patches


def build_sae_guided_patches(W_dict: np.ndarray, active_idx: np.ndarray, k: int, n_patches: int, rng: np.random.Generator) -> list[np.ndarray]:
    """Orthonormal bases seeded by active Sparse Autoencoder (SAE) dictionary atoms."""
    D, F = W_dict.shape
    patches = []
    for i in range(n_patches):
        # Include active atoms + random dictionary neighbors to form a k-column bank
        extra = rng.choice(F, size=max(0, k - len(active_idx)), replace=False)
        cols = np.unique(np.concatenate([active_idx, extra]))[:k]
        if len(cols) < k:
            pad = rng.standard_normal((D, k - len(cols)))
            M = np.hstack([W_dict[:, cols], pad])
        else:
            M = W_dict[:, cols]
        Q, R = np.linalg.qr(M, mode="reduced")
        signs = np.sign(np.diag(R))
        signs[signs == 0] = 1.0
        patches.append(Q * signs)
    return patches


def evaluate_spherepop_cover(name: str, x_ambient: np.ndarray, patches: list[np.ndarray], perturb: bool, rng: np.random.Generator) -> dict:
    n_patches, k = len(patches), patches[0].shape[1]
    base_hash = canonical_q16_sha256(x_ambient)

    events = [
        {"op": "POP", "scope": f"parent_{name}", "base_version": base_hash[:16]},
        {"op": "BIND", "scope": f"parent_{name}", "authority": "NDH_SEALED_LAYER"},
    ]

    local_sections = []
    for i, P in enumerate(patches):
        s_i = P.T @ x_ambient
        if perturb and i == 0:
            s_i = s_i + 0.5 * rng.standard_normal(k)
        local_sections.append(s_i)
        events.append({
            "op": "VERIFY",
            "scope": f"sub_patch_{i}",
            "local_valid": True,
            "section_hash": canonical_q16_sha256(s_i)[:16],
        })

    # Compute Sheaf Laplacian energy s^T L_F s = ||delta^0 s||_2^2
    sq_err = 0.0
    for i in range(n_patches):
        j = (i + 1) % n_patches
        proj_i_to_j = patches[j].T @ (patches[i] @ local_sections[i])
        proj_j_self = patches[j].T @ (patches[j] @ local_sections[j])
        diff = proj_i_to_j - proj_j_self
        sq_err += float(np.dot(diff, diff))
    coboundary_norm = float(np.sqrt(sq_err))

    if coboundary_norm <= 1e-6:
        disposition = "COLLAPSE"
        events.append({"op": "COLLAPSE", "scope": f"parent_{name}", "coboundary_norm": coboundary_norm})
    else:
        disposition = "REFUSE"
        events.append({
            "op": "REFUSE",
            "scope": f"parent_{name}",
            "reason": "COBOUNDARY_OBSTRUCTION",
            "coboundary_norm": coboundary_norm,
        })

    return {
        "cover_type": name,
        "local_intervention_applied": perturb,
        "coboundary_norm": coboundary_norm,
        "terminal_disposition": disposition,
        "event_count": len(events),
        "events": events,
    }


def main() -> None:
    D, F, n_patches, k = 256, 2048, 6, 64
    rng = np.random.default_rng(77)

    W = rng.standard_normal((D, F))
    W /= np.linalg.norm(W, axis=0, keepdims=True)
    f_true = np.zeros(F)
    active_idx = rng.choice(F, size=12, replace=False)
    f_true[active_idx] = rng.standard_normal(12)
    x_ambient = W @ f_true

    qr_patches = build_qr_patches(D, k, n_patches, np.random.default_rng(10))
    sae_patches = build_sae_guided_patches(W, active_idx, k, n_patches, np.random.default_rng(20))

    report = {
        "experiment": "Experiment_C_Spherepop_SAE_vs_QR_Sheaf_Audit",
        "ambient_dim_D": D,
        "superposed_features_F": F,
        "runs": [
            evaluate_spherepop_cover("random_qr_unperturbed", x_ambient, qr_patches, False, np.random.default_rng(1)),
            evaluate_spherepop_cover("sae_guided_unperturbed", x_ambient, sae_patches, False, np.random.default_rng(2)),
            evaluate_spherepop_cover("sae_guided_local_intervention", x_ambient, sae_patches, True, np.random.default_rng(3)),
        ],
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
