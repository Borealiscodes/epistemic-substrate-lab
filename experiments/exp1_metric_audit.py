#!/usr/bin/env python3
"""
Experiment A (exp1_metric_audit.py):
- Compares softmax KL divergence (triangle inequality violations) & Euclidean simplex
  saturation against Aitchison centered log-ratio (clr) isometry and pre-softmax
  QR-isometric SPD pullback metrics.
- Includes decontaminated Q16.16 fixed-point determinism control (RI-Haunted-Township),
  read-only A7.2 Layer-1 SVD rank detector, and exact Q[i] CAUSA kernel collapse.
"""

from dataclasses import dataclass
from fractions import Fraction
import json
import numpy as np


# --- 1. Q16.16 Fixed-Point Determinism Control ---
Q16_SHIFT = 16
Q16_ONE = 1 << Q16_SHIFT

def to_q16(x: float) -> int:
    return int(round(x * Q16_ONE))

def run_q16_determinism_check() -> dict:
    x, y = to_q16(0.75), to_q16(-0.25)
    x0, y0 = x, y
    for _ in range(4):
        x, y = -y, x
    return {
        "q16_initial": [x0, y0],
        "q16_after_4_rotations": [x, y],
        "bit_exact_reversibility": (x == x0 and y == y0),
    }


# --- 2. Read-Only A7.2 Layer-1 SVD Rank-Deficiency Detector ---
def svd_layer1_audit(M: np.ndarray, tol: float = 1e-11) -> dict:
    s = np.linalg.svd(M, compute_uv=False)
    destroyed = int(np.sum(s <= tol))
    sigma_min = float(np.min(s))
    sigma_max = float(np.max(s))
    cond = float(sigma_max / sigma_min) if sigma_min > 0 else float("inf")
    return {
        "sigma_min": sigma_min,
        "sigma_max": sigma_max,
        "condition_number": cond,
        "destroyed_dimensions": destroyed,
        "admissible_for_inference": bool(sigma_min > 0.0 and destroyed == 0),
    }


# --- 3. Softmax Simplex Collapse & Triangle Inequality vs. Aitchison clr ---
def softmax(z: np.ndarray) -> np.ndarray:
    z_shift = z - np.max(z)
    e = np.exp(z_shift)
    return e / np.sum(e)

def kl_div(p: np.ndarray, q: np.ndarray) -> float:
    p_safe = np.clip(p, 1e-15, 1.0)
    q_safe = np.clip(q, 1e-15, 1.0)
    return float(np.sum(p_safe * np.log(p_safe / q_safe)))

def clr(p: np.ndarray) -> np.ndarray:
    p_safe = np.clip(p, 1e-15, 1.0)
    log_p = np.log(p_safe)
    return log_p - np.mean(log_p)

def run_simplex_vs_aitchison_audit() -> dict:
    z0 = np.array([2.0, 1.0, 0.1, -1.0])
    z1 = np.array([1.0, 2.0, 0.5, -0.5])
    z2 = np.array([-1.0, 0.2, 2.5, 1.5])
    p0, p1, p2 = softmax(z0), softmax(z1), softmax(z2)

    kl_02 = kl_div(p0, p2)
    kl_01_12 = kl_div(p0, p1) + kl_div(p1, p2)

    c0, c1, c2 = clr(p0), clr(p1), clr(p2)
    aitch_02 = float(np.linalg.norm(c0 - c2))
    aitch_01_12 = float(np.linalg.norm(c0 - c1) + np.linalg.norm(c1 - c2))

    scales = [1.0, 10.0, 50.0]
    boundary_shifts = []
    for c in scales:
        pa = softmax(c * np.array([1.0, 0.9, 0.0, -1.0]))
        pb = softmax(c * np.array([1.0, 0.85, 0.0, -1.0]))
        boundary_shifts.append({
            "radial_scale_c": c,
            "euclidean_simplex_dist": float(np.linalg.norm(pa - pb)),
            "aitchison_clr_dist": float(np.linalg.norm(clr(pa) - clr(pb))),
        })

    return {
        "kl_direct_02": kl_02,
        "kl_sum_01_12": kl_01_12,
        "kl_violates_triangle_inequality": bool(kl_02 > kl_01_12),
        "aitchison_direct_02": aitch_02,
        "aitchison_sum_01_12": aitch_01_12,
        "aitchison_satisfies_triangle_inequality": bool(aitch_02 <= aitch_01_12 + 1e-12),
        "radial_simplex_collapse_test": boundary_shifts,
    }


# --- 4. Exact Q[i] CAUSA Kernel Interchange Collapse ---
@dataclass(frozen=True)
class GaussianRat:
    re: Fraction
    im: Fraction

    def __add__(self, o: "GaussianRat") -> "GaussianRat":
        return GaussianRat(self.re + o.re, self.im + o.im)

    def __mul__(self, o: "GaussianRat") -> "GaussianRat":
        return GaussianRat(self.re * o.re - self.im * o.im, self.re * o.im + self.im * o.re)

def run_causa_qi_kernel_check() -> dict:
    zero = GaussianRat(Fraction(0), Fraction(0))
    enneract = [GaussianRat(Fraction(i + 1, 4), Fraction((-1) ** i, 3)) for i in range(9)]
    p_base = [GaussianRat(Fraction(k, 2), Fraction(1, 5)) for k in range(1, 6)]
    delta = [
        GaussianRat(Fraction(50), Fraction(-25)),
        GaussianRat(Fraction(-50), Fraction(25)),
        GaussianRat(Fraction(17), Fraction(9)),
        GaussianRat(Fraction(-17), Fraction(-9)),
        zero,
    ]
    p_intervened = [a + b for a, b in zip(p_base, delta)]
    out_base = sum(p_base, zero) * sum(enneract, zero)
    out_int = sum(p_intervened, zero) * sum(enneract, zero)
    return {
        "personas_distinct": p_base != p_intervened,
        "causa_interchange_invariant": out_base == out_int,
        "collapsed_1x1_re": str(out_base.re),
        "collapsed_1x1_im": str(out_base.im),
    }


def main() -> None:
    rng = np.random.default_rng(42)
    Q, _ = np.linalg.qr(rng.standard_normal((64, 16)))
    g_sub = Q.T @ (np.eye(64) + 0.15 * np.eye(64)) @ Q

    report = {
        "experiment": "Experiment_A_Metric_and_Kernel_Audit",
        "q16_determinism": run_q16_determinism_check(),
        "a72_layer1_svd_audit": svd_layer1_audit(g_sub),
        "simplex_vs_aitchison": run_simplex_vs_aitchison_audit(),
        "causa_qi_kernel_collapse": run_causa_qi_kernel_check(),
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
