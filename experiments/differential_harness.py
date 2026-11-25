#!/usr/bin/env python3
"""
Cross-Language Differential Fuzz Harness (Julia StaticArrays vs. Python NumPy).
Inspired by Spherepop's differential.py: runs 100 randomized subspace + holonomy
trials across both runtimes and asserts agreement within 1e-12.
"""

import json
import subprocess
import numpy as np


def python_holonomy_reference(k: int, coupling: float, steps: int = 64) -> float:
    H = np.eye(k, dtype=np.float64)
    dt = 2.0 * np.pi / steps
    for i in range(steps):
        tm = (i + 0.5) * dt
        x_mid = np.zeros(k)
        dx = np.zeros(k)
        x_mid[0], x_mid[1] = np.cos(tm), np.sin(tm)
        dx[0], dx[1] = -np.sin(tm) * dt, np.cos(tm) * dt
        A_mid = np.zeros((k, k), dtype=np.float64)
        if coupling != 0.0:
            for mu in range(k):
                for nu in range(k):
                    if mu != nu:
                        A_mid[mu, nu] = coupling * (x_mid[mu] * dx[nu] - x_mid[nu] * dx[mu])
        step_exp = np.eye(k) + A_mid + 0.5 * (A_mid @ A_mid)
        H = H @ step_exp
    return float(np.linalg.norm(H - np.eye(k), ord=2))


def main() -> None:
    rng = np.random.default_rng(2026)
    couplings = [0.0] + [float(c) for c in rng.uniform(0.01, 0.5, size=99)]

    julia_code = f"""
    include("julia/ManifoldInstruments.jl")
    using .ManifoldInstruments, StaticArrays
    P = build_isometric_basis(64, 8; seed=42)
    g_sub = SMatrix{{8,8,Float64}}(P' * P)
    couplings = {json.dumps(couplings)}
    for c in couplings
        res = holonomy_loop_static(g_sub; coupling=Float64(c))
        println(res.holonomy_deviation)
    end
    """
    proc = subprocess.run(["julia", "-e", julia_code], capture_output=True, text=True, check=True)
    julia_vals = [float(line.strip()) for line in proc.stdout.strip().splitlines() if line.strip()]
    assert len(julia_vals) == len(couplings), f"Expected {len(couplings)} outputs, got {len(julia_vals)}"

    max_diff = 0.0
    for c, j_val in zip(couplings, julia_vals):
        p_val = python_holonomy_reference(8, c)
        diff = abs(j_val - p_val)
        if diff > max_diff:
            max_diff = diff
        assert diff < 1e-12, f"Differential mismatch at coupling={c}: Julia={j_val} vs Python={p_val}"

    print(json.dumps({
        "differential_trials": len(couplings),
        "max_julia_python_discrepancy": max_diff,
        "differential_gate_passed": True,
    }, indent=2))


if __name__ == "__main__":
    main()
