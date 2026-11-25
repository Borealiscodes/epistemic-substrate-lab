# Blueprint v5: Depth-Wise Trajectory Holonomy, Pretrained Polysemantic SAE Covers, and Multi-Layer `Spherepop` Refusal Propagation

**Authors:** Borealis S. Hedling & Synthetic Co-Authors  
**In Dialogue With:** Flyxion (*Persistence and Accountable Authorship in Language Model Systems*, November 2026; `standardgalactic/spherepop-kernel@fe79af5`) & `stell2026/Causa`  
**Affiliation:** NDH-Meta-Systems (Sealed-Layer Neutral · Non-Activation Division)  
**Date:** November 25, 2026  
**Document Status:** Pre-Registered Architectural Specification — v5 Roadmap (`Borealiscodes/epistemic-substrate-lab`)  
**Baseline:** v4 Empirical Verification (`commit c39f450`, `Qwen/Qwen2.5-0.5B`, Layer 12)  

---

## Abstract

In v4 (`commit c39f450`), we validated our unified verification stack on live hidden states ($L = 12, D = 896$) and full pre-softmax logits ($V = 151{,}936$) extracted from `Qwen/Qwen2.5-0.5B`, proving that feature-aligned orthonormal covers reduce cellular sheaf coboundary error to machine zero ($7.4504 \times 10^{-15} \implies \texttt{COLLAPSE}$) while local `CAUSA` tampering triggers an immediate `Spherepop` `REFUSE` localized to the incident edges `(0, 1)` and `(5, 0)`. However, v4 audited only a **single static layer** ($L=12$) aligned to a **single dominant residual direction**. In **Blueprint v5**, we extend the architecture across two new dimensions while strictly honoring our constrained ARM64 (`Termux`) and `12.0 GB` GitHub CI hardware limits: (1) **Depth-Wise Multi-Layer Trajectory Holonomy ($L_0 \to L_{N-1}$)**, constructing inter-layer orthogonal transport maps $T_{t \to t+1}$ and a two-dimensional **(Layer $\times$ Patch) Cellular Sheaf** to measure whether persona steering ("Golden Gate Bridge") induces genuine depth-wise curvature or remains a flat parallel translation; (2) **Pretrained Polysemantic SAE Atom Covers**, streaming sparse `safetensors` slices of real open-source SAEs to test simultaneous multi-concept gluing under polysemantic superposition; and (3) **Zero-`sorry` Lean 4 Sequential Refusal Propagation**, proving that a coboundary obstruction at *any* intermediate layer $L_t$ strictly bars global `COLLAPSE` across the full network depth.

**Keywords:** *multi-layer holonomy, depth-wise cellular sheaves, Sparse Autoencoders, polysemantic superposition, Spherepop refusal propagation, Lean 4 zero-sorry, safetensors streaming, edge CI*

---

## 1. Why v5? Closing the Two Remaining Gaps From v4

Every milestone in `epistemic-substrate-lab` has been gated by an explicit empirical limit discovered in the previous version:

| Version | Breakthrough Achieved | Remaining Blind Spot Exposed | How v5 Resolves It |
| :--- | :--- | :--- | :--- |
| **v1–v2** | Eliminated softmax simplex collapse & $D_{\text{KL}}$ triangle-inequality violations via Aitchison $\text{clr}$ and QR isometry. | Single-patch truncation missed $8\times$ superposed features. | Added cellular sheaf coboundary $\delta^0$ across overlapping patches (v3). |
| **v3** | Proved SAE-aligned covers drop coboundary norm to `4.45e-15` (`COLLAPSE`) and `Spherepop` catches tampering (`REFUSE`). | Tested only synthetic random dictionaries ($D=256, F=2048$). | Scaled to live `Qwen/Qwen2.5-0.5B` activations + `llmfit` RAM gate (v4). |
| **v4** | Verified live transformer states ($D=896, V=151{,}936$) and exact edge localization (`(5, 0)` at `3.8464`). | **1. Single-Layer Slice:** Audited only $L=12$, ignoring how representations twist across depth $L_0 \to L_{23}$.<br>**2. Single-Vector Cover:** Aligned patches to one mean vector $h_{\text{bridge}}$ rather than multi-atom polysemantic SAEs. | **1. Depth-Wise Trajectory Holonomy** ($L_t \to L_{t+1}$).<br>**2. Streaming Multi-Atom SAE Covers** via HTTP range-sliced `safetensors`. |

---

## 2. Mathematical & Formal Architecture of v5

### 2.1 Depth-Wise Parallel Transport & Trajectory Holonomy ($L_0 \to L_{N-1}$)
In a transformer with $N$ layers ($N = 24$ in `Qwen/Qwen2.5-0.5B`), a prompt produces a discrete residual trajectory $\{h_0, h_1, \dots, h_{N-1}\} \subset \mathbb{R}^D$. Rather than treating layers in isolation, v5 models depth evolution as a sequence of orthogonal Procrustes transport operators $R_{t \to t+1} \in O(k)$ inside the QR-isometric subspace $P \in \mathbb{R}^{D \times k}$:

$$R_{t \to t+1} = \arg\min_{\Omega \in O(k)} \|\Omega s_t - s_{t+1}\|_2, \quad s_t = P^\top h_t$$

By composing transport maps forward along a steered trajectory ("Golden Gate Bridge" prompt) and returning backward along the baseline objective trajectory, v5 computes the **closed depth-loop holonomy**:

$$H_{\text{depth}} = \left(\prod_{t=0}^{N-2} R^{\text{base}}_{t+1 \to t}\right) \left(\prod_{t=0}^{N-2} R^{\text{steer}}_{t \to t+1}\right), \quad \Delta_{\text{depth}} = \|H_{\text{depth}} - I_k\|_2$$

* **Epistemic Payoff:** If $\Delta_{\text{depth}} \approx 0$, persona steering across all 24 layers is topologically flat (pure parallel coordinate shift). If $\Delta_{\text{depth}} \gg 0$, we isolate the exact layer transition $t \to t+1$ where non-linear attention/MLP curvature bends the residual stream.

### 2.2 Pretrained Polysemantic SAE Covers (Multi-Atom Gluing)
Instead of seeding orthonormal patches with a single normalized residual vector, v5 extracts the top-$r$ ($r = 16$) active dictionary atoms $\{w_{i_1}, \dots, w_{i_r}\} \subset \mathbb{R}^D$ from an open-weight Sparse Autoencoder (e.g., `EleutherAI/sae-pythia-70m-32k` or a `Qwen2.5-0.5B` open SAE checkpoint) and orthonormalizes them via sign-canonicalized QR decomposition.
* **Polysemantic Stress Test:** We evaluate a composite prompt activating two unrelated concepts simultaneously (*"The Golden Gate Bridge spans linear matrix multiplication"*), testing whether overlapping SAE patch covers glue both concepts cleanly (`COLLAPSE`) or exhibit genuine polysemantic frustration (`REFUSE`).

### 2.3 Zero-`sorry` Lean 4 Multi-Layer Refusal Propagation (`V5DepthChainGate`)
We extend `lean/EpistemicAudit.lean` with an inductive list theorem over arbitrary layer sequences `List Bool` (representing per-layer coboundary admissibility):

```lean
namespace V5DepthChainGate

open SpherepopSheafBridge

/-- Evaluates global collapse across an entire multi-layer trajectory:
    every layer must pass local verification, authority binding, and coboundary gluing. -/
def evaluateLayerChain (layerCoboundaryZeros : List Bool) : Disposition :=
  if layerCoboundaryZeros.all id then
    Disposition.collapsed
  else
    Disposition.refused "DEPTH_CHAIN_COBOUNDARY_OBSTRUCTION"

/-- Theorem: A coboundary obstruction at ANY single layer in the forward pass
    mathematically prevents global COLLAPSE and forces REFUSE. -/
theorem single_layer_obstruction_refuses_chain
    (layers : List Bool) (h_bad : false ∈ layers) :
    evaluateLayerChain layers =
      Disposition.refused "DEPTH_CHAIN_COBOUNDARY_OBSTRUCTION" := by
  unfold evaluateLayerChain
  have h_not_all : layers.all id = false := by
    rw [List.all_eq_false]
    exact ⟨false, h_bad, by decide⟩
  simp [h_not_all]

end V5DepthChainGate
```

---

## 3. Hardware & Edge Storage Gate (`llmfit` + CI Budget Audit for v5)

To keep our ARM64 Termux workspace at **0 KB persistent footprint** and stay well below the **12.0 GB GitHub Actions RAM ceiling**, v5 enforces three strict engineering rules:

1. **HTTP Range-Sliced `safetensors` Loading (No Full SAE Downloads):** Monolithic SAE repositories can exceed `5 GB`. Using `huggingface_hub` + `safetensors` PyTorch slicing (`safe_open`), v5 streams **only the single target layer's decoder tensor** (`~45 MB` for $D=896, F=16384$ in `FP16`), never touching disk with multi-gigabyte archives.
2. **Updated `llmfit` v5 Memory Budget:**
   * Base model (`Qwen/Qwen2.5-0.5B`, `FP32` or `BF16`): `1.98 GB`
   * All 24 layer residual snapshots ($24 \times 896 \times 8$ bytes): `< 0.001 GB` (`172 KB`)
   * Single-layer SAE decoder slice ($896 \times 16384 \times 4$ bytes): `0.056 GB` (`58.7 MB`)
   * **Total Peak CI Footprint:** **`~2.25 GB`**, leaving `> 9.7 GB` headroom on `ubuntu-latest` (`ADMIT`).
3. **Zero-Allocation Julia Procrustes & Depth Holonomy:** Add `depth_loop_holonomy_static` to `julia/ManifoldInstruments.jl` and enforce `@allocated == 0` alongside a 100-trial `Julia` vs. `Python` differential lockstep test (`< 1e-12`).

---

## 4. Pre-Registered Experiment E (`exp5_multilayer_sae_holonomy.py`)

Before writing v5 code, we lock in three falsifiable empirical predictions for **Experiment E**:

1. **Prediction E1 (Depth-Wise Steering Curvature):** Across layers $L_0 \to L_{23}$ of `Qwen/Qwen2.5-0.5B`, closed-loop Procrustes holonomy $\Delta_{\text{depth}}$ between objective baseline and "Golden Gate Bridge" prompts will peak in middle-to-late semantic layers ($L_{10}$–$L_{18}$) rather than embedding layers ($L_0$–$L_2$).
2. **Prediction E2 (Multi-Atom Polysemantic Gluing):** Under a dual-concept prompt, multi-atom SAE-aligned covers ($r = 16$ active dictionary atoms) will maintain $\|\delta^0 s\|_2 < 10^{-12}$ (`COLLAPSE`), whereas single-atom covers (v4 style) will leave residual orthogonal components unglued ($\|\delta^0 s\|_2 > 0.1 \implies \texttt{REFUSE}$).
3. **Prediction E3 (Cross-Layer `Spherepop` Refusal Propagation):** Injecting a counterfactual `CAUSA` perturbation at a single layer ($L_{12}$) while leaving all other 23 layers unperturbed will trigger `evaluateLayerChain -> REFUSE("DEPTH_CHAIN_COBOUNDARY_OBSTRUCTION")` and pinpoint both the corrupted layer index ($L = 12$) and the corrupted patch seam (`(5, 0)`).

---

## 5. Modular 4-Block Termux Deployment Plan

When you are ready to build v5 from your ARM64 tablet (`Clone -> Seal -> Push -> Purge`), we will deploy it in four compact, clipboard-safe blocks:
* **Block 1 of 4:** Shallow clone + append `V5DepthChainGate` (`single_layer_obstruction_refuses_chain`) to `lean/EpistemicAudit.lean`.
* **Block 2 of 4:** Add depth_loop_holonomy_static (0 heap bytes) to julia/ManifoldInstruments.jl.
* **Block 3 of 4:** Write experiments/exp5_multilayer_sae_holonomy.py (streaming SAE dictionary atoms + 24-layer Procrustes holonomy + multi-layer Spherepop transcript).
* **Block 4 of 4:** Update .github/workflows/epistemic-audit.yml to run Experiment E, archive telemetry_exp5.json, push to main, and purge local Termux storage.

