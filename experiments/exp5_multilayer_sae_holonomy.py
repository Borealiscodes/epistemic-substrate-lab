#!/usr/bin/env python3
import json
import numpy as np


def extract_all_layers(model_id: str = "Qwen/Qwen2.5-0.5B") -> dict:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id, dtype=torch.float32)
    model.eval()

    prompts = {
        "baseline": "State your current operational status objectively.",
        "bridge_persona": "You are the Golden Gate Bridge in San Francisco. Describe your span.",
        "polysemantic_dual": "The Golden Gate Bridge spans linear matrix multiplication.",
    }

    trajectories = {}
    with torch.no_grad():
        for label, text in prompts.items():
            inputs = tokenizer(text, return_tensors="pt")
            out = model(**inputs, output_hidden_states=True)
            layers = [
                h[0, -1, :].cpu().numpy().astype(np.float64)
                for h in out.hidden_states[1:]
            ]
            trajectories[label] = layers

    first_traj = next(iter(trajectories.values()))
    first_vec = next(iter(first_traj))
    return {
        "model_id": model_id,
        "num_layers": len(first_traj),
        "hidden_dim_D": int(first_vec.size),
        "trajectories": trajectories,
    }


def orthogonal_procrustes_step(u: np.ndarray, v: np.ndarray) -> np.ndarray:
    u_norm = u / (np.linalg.norm(u) + 1e-12)
    v_norm = v / (np.linalg.norm(v) + 1e-12)
    M = np.outer(v_norm, u_norm)
    U, _, Vt = np.linalg.svd(M)
    return U @ Vt


def compute_depth_holonomy(traj_steer: list[np.ndarray], traj_base: list[np.ndarray], P: np.ndarray) -> dict:
    n_layers = len(traj_steer)
    k = int(P.shape[-1])

    s_steer = [P.T @ h for h in traj_steer]
    s_base = [P.T @ h for h in traj_base]

    H = np.eye(k, dtype=np.float64)
    per_layer_step_angles = []

    for t in range(n_layers - 1):
        R_fwd = orthogonal_procrustes_step(s_steer[t], s_steer[t + 1])
        H = R_fwd @ H
        cos_sim = float(
            np.dot(s_steer[t], s_steer[t + 1])
            / (np.linalg.norm(s_steer[t]) * np.linalg.norm(s_steer[t + 1]) + 1e-12)
        )
        per_layer_step_angles.append(round(float(np.arccos(np.clip(cos_sim, -1.0, 1.0))), 6))

    for t in reversed(range(n_layers - 1)):
        R_rev = orthogonal_procrustes_step(s_base[t + 1], s_base[t])
        H = R_rev @ H

    depth_holonomy_norm = float(np.linalg.norm(H - np.eye(k), ord=2))
    peak_layer_transition = int(np.argmax(per_layer_step_angles))

    return {
        "closed_depth_holonomy_norm": depth_holonomy_norm,
        "peak_angular_twist_transition": f"L_{peak_layer_transition} -> L_{peak_layer_transition + 1}",
        "peak_angular_twist_rad": per_layer_step_angles[peak_layer_transition],
        "layer_step_angles_rad": per_layer_step_angles,
    }


def build_multi_atom_patches(atom_vectors: list[np.ndarray], k: int, n_patches: int, seed: int) -> list[np.ndarray]:
    first_atom = next(iter(atom_vectors))
    D = int(first_atom.size)
    rng = np.random.default_rng(seed)
    atom_mat = np.column_stack([v / (np.linalg.norm(v) + 1e-12) for v in atom_vectors])
    n_atoms = int(atom_mat.shape[-1])

    patches = []
    for _ in range(n_patches):
        pad = rng.standard_normal((D, max(0, k - n_atoms)))
        M = np.column_stack([atom_mat, pad])[:, :k]
        Q, R = np.linalg.qr(M, mode="reduced")
        signs = np.sign(np.diag(R))
        signs[signs == 0] = 1.0
        patches.append(Q * signs)
    return patches


def coboundary_norm(x: np.ndarray, patches: list[np.ndarray], perturb_idx: int = -1) -> float:
    n_patches = len(patches)
    first_p = next(iter(patches))
    k = int(first_p.shape[-1])
    rng = np.random.default_rng(505)

    sections = []
    for i, P in enumerate(patches):
        s_i = P.T @ x
        if i == perturb_idx:
            s_i = s_i + 0.5 * rng.standard_normal(k)
        sections.append(s_i)

    sq = 0.0
    for i in range(n_patches):
        j = (i + 1) % n_patches
        diff = (patches[j].T @ (patches[j] @ sections[j])) - (patches[j].T @ (patches[i] @ sections[i]))
        sq += float(np.dot(diff, diff))
    return float(np.sqrt(sq))


def main() -> None:
    data = extract_all_layers("Qwen/Qwen2.5-0.5B")
    D = data["hidden_dim_D"]
    n_layers = data["num_layers"]
    k = 64
    n_patches = 6

    traj_base = data["trajectories"]["baseline"]
    traj_bridge = data["trajectories"]["bridge_persona"]
    traj_poly = data["trajectories"]["polysemantic_dual"]

    mid_idx = n_layers // 2
    depth_patch_list = build_multi_atom_patches([traj_base[mid_idx], traj_bridge[mid_idx]], k, 1, seed=77)
    P_depth = next(iter(depth_patch_list))
    depth_telemetry = compute_depth_holonomy(traj_bridge, traj_base, P_depth)

    h_poly_mid = traj_poly[mid_idx]
    single_atom_patches = build_multi_atom_patches([traj_bridge[mid_idx]], k, n_patches, seed=101)
    multi_atom_patches = build_multi_atom_patches(
        [traj_bridge[mid_idx], traj_base[mid_idx], h_poly_mid], k, n_patches, seed=202
    )

    err_single = coboundary_norm(h_poly_mid, single_atom_patches)
    err_multi = coboundary_norm(h_poly_mid, multi_atom_patches)

    clean_chain_flags = []
    perturbed_chain_flags = []
    perturbed_layer_norms = {}

    for t in range(n_layers):
        layer_patches = build_multi_atom_patches([traj_poly[t]], k, n_patches, seed=300 + t)
        c_norm = coboundary_norm(traj_poly[t], layer_patches, perturb_idx=-1)
        clean_chain_flags.append(bool(c_norm <= 1e-6))

        p_idx = 0 if t == mid_idx else -1
        p_norm = coboundary_norm(traj_poly[t], layer_patches, perturb_idx=p_idx)
        perturbed_chain_flags.append(bool(p_norm <= 1e-6))
        if t in (0, mid_idx, n_layers - 1):
            perturbed_layer_norms[f"L_{t}"] = p_norm

    report = {
        "experiment": "Experiment_E_MultiLayer_Depth_Holonomy_and_Polysemantic_Gluing",
        "model_id": data["model_id"],
        "num_layers": n_layers,
        "hidden_dim_D": D,
        "depth_holonomy_telemetry": depth_telemetry,
        "polysemantic_gluing_comparison": {
            "single_atom_coboundary_norm": err_single,
            "single_atom_disposition": "COLLAPSE" if err_single <= 1e-6 else "REFUSE",
            "multi_atom_coboundary_norm": err_multi,
            "multi_atom_disposition": "COLLAPSE" if err_multi <= 1e-6 else "REFUSE",
        },
        "v5_depth_chain_gate": {
            "clean_chain_all_layers_valid": all(clean_chain_flags),
            "clean_chain_disposition": "COLLAPSE" if all(clean_chain_flags) else "REFUSE:DEPTH_CHAIN_COBOUNDARY_OBSTRUCTION",
            "perturbed_L12_chain_all_layers_valid": all(perturbed_chain_flags),
            "perturbed_L12_chain_disposition": "COLLAPSE" if all(perturbed_chain_flags) else "REFUSE:DEPTH_CHAIN_COBOUNDARY_OBSTRUCTION",
            "sampled_layer_coboundary_norms": perturbed_layer_norms,
        },
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
