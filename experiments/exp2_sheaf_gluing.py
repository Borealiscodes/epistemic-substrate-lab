#!/usr/bin/env python3
"""
Experiment B (exp2_sheaf_gluing.py):
- Tests local-to-global patch consistency across overlapping rank-k QR subspaces
  in a superposed feature regime (F = 2048 almost-orthogonal features in D = 256).
- Adapts RI-Haunted-Township's k-hop coboundary propagation to compute the cellular
  sheaf coboundary residual ||delta^0 s||_2 and evaluate the v3 sheaf gate.
"""

import json
import numpy as np


def run_superposition_sheaf_test(D: int = 256, F: int = 2048, n_patches: int = 6, k: int = 64, seed: int = 77) -> dict:
    rng = np.random.default_rng(seed)

    # 1. Construct superposed dictionary W in R^{D x F} with unit-norm columns
    W = rng.standard_normal((D, F))
    W /= np.linalg.norm(W, axis=0, keepdims=True)

    # Sparse active feature vector (12 active features out of 2048)
    f_true = np.zeros(F)
    active_idx = rng.choice(F, size=12, replace=False)
    f_true[active_idx] = rng.standard_normal(12)
    x_ambient = W @ f_true

    # 2. Construct m overlapping rank-k QR subspace patches
    patches = []
    for _ in range(n_patches):
        A = rng.standard_normal((D, k))
        Q, R = np.linalg.qr(A, mode="reduced")
        signs = np.sign(np.diag(R))
        signs[signs == 0] = 1.0
        patches.append(Q * signs)

    # 3. Local patch observations s_i = P_i^T x_ambient
    local_sections = [P.T @ x_ambient for P in patches]
    local_sections_perturbed = [s.copy() for s in local_sections]
    # Inject a local counterfactual perturbation restricted to patch 0's coordinates
    local_sections_perturbed[0] = local_sections_perturbed[0] + 0.5 * rng.standard_normal(k)

    def coboundary_energy(sections: list[np.ndarray]) -> float:
        sq_err = 0.0
        for i in range(n_patches):
            j = (i + 1) % n_patches
            proj_i_to_j = patches[j].T @ (patches[i] @ sections[i])
            proj_j_self = patches[j].T @ (patches[j] @ sections[j])
            diff = proj_i_to_j - proj_j_self
            sq_err += float(np.dot(diff, diff))
        return float(np.sqrt(sq_err))

    coboundary_unperturbed = coboundary_energy(local_sections)
    coboundary_intervened = coboundary_energy(local_sections_perturbed)

    return {
        "experiment": "Experiment_B_Superposition_Sheaf_Gluing",
        "ambient_dim_D": D,
        "superposed_features_F": F,
        "num_patches": n_patches,
        "patch_rank_k": k,
        "coboundary_residual_unperturbed": coboundary_unperturbed,
        "coboundary_residual_local_intervention": coboundary_intervened,
        "v3_sheaf_cohomology_warranted": bool(coboundary_intervened > 1e-6),
    }


def main() -> None:
    print(json.dumps(run_superposition_sheaf_test(), indent=2))


if __name__ == "__main__":
    main()
