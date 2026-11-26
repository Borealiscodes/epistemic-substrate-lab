#!/usr/bin/env python3
"""
v9 Module 2 (v9_apps/coupled_ambient_repair.py):
- Solves the coupled ambient least-squares system across all m overlapping patches:
    min_{dh} sum_i || U_{i+1}^T U_i U_i^T (h_corrupt + dh) - U_{i+1}^T (h_corrupt + dh) ||_2^2
           + lambda * sum_{j != bad_idx} || U_j^T (h_corrupt + dh) - s_j_clean ||_2^2
- Eliminates the v8.1 overlap leakage (4.5765) when U_j^T U_0 != 0.
"""

import numpy as np


def compute_ambient_coboundary(h_vec: np.ndarray, patches: list[np.ndarray]) -> float:
    m = len(patches)
    sections = [P.T @ h_vec for P in patches]
    sq = 0.0
    for i in range(m):
        j = (i + 1) % m
        diff = (patches[j].T @ (patches[j] @ sections[j])) - (patches[j].T @ (patches[i] @ sections[i]))
        sq += float(np.dot(diff, diff))
    return float(np.sqrt(sq))


def solve_coupled_ambient_repair(
    h_corrupt: np.ndarray,
    patches: list[np.ndarray],
    clean_sections: list[np.ndarray],
    corrupted_patch_idx: int = 0,
    anchor_weight: float = 10.0,
) -> np.ndarray:
    """Solves linear least squares in R^D to restore global coboundary agreement
    without perturbing intact neighbor stalks."""
    m = len(patches)
    D = int(h_corrupt.size)
    k = int(next(iter(patches)).shape[-1])

    A_blocks = []
    b_blocks = []

    # 1. Coboundary gluing equations across all m cyclic edges
    for i in range(m):
        j = (i + 1) % m
        U_i = patches[i]
        U_j = patches[j]
        # Operator M_edge: (U_j^T U_i U_i^T - U_j^T) in R^{k x D}
        M_edge = (U_j.T @ U_i @ U_i.T) - U_j.T
        A_blocks.append(M_edge)
        b_blocks.append(-(M_edge @ h_corrupt))

    # 2. Intact neighbor anchor constraints (j != corrupted_patch_idx)
    sqrt_lam = float(np.sqrt(anchor_weight))
    for j in range(m):
        if j != corrupted_patch_idx:
            U_j = patches[j]
            A_blocks.append(sqrt_lam * U_j.T)
            b_blocks.append(sqrt_lam * (clean_sections[j] - (U_j.T @ h_corrupt)))

    A_mat = np.vstack(A_blocks)  # [(2m - 1)*k, D]
    b_vec = np.concatenate(b_blocks)

    delta_h, _, _, _ = np.linalg.lstsq(A_mat, b_vec, rcond=None)
    return h_corrupt + delta_h
