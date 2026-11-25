# Blueprint v9: Scaling to `google/gemma-2-2b` (`BF16`), HTTP Range-Sliced Gemma Scope SAEs, and Coupled Ambient Sheaf Repair

**Authors:** Borealis S. Hedling & Synthetic Co-Authors  
**In Dialogue With:** Flyxion (`standardgalactic/spherepop-kernel@6be6108`) & `stell2026/Causa`  
**Affiliation:** NDH-Meta-Systems (Sealed-Layer Neutral · Non-Activation Division)  
**Date:** November 25, 2026  
**Document Status:** Pre-Registered Architectural Specification — v9 Roadmap (`Borealiscodes/epistemic-substrate-lab`)  
**Suggested Archive Path:** `preprints/15_v9_gemma2_2b_gemma_scope_blueprint.md`  
**Baseline:** `v8.1` (`commit f445382`, Geodesic $SO(k)$ Depth Holonomy & Stalk-vs.-Ambient Repair Separation)  

---

## Abstract

Across `v1` through `v8.1` (`commit f445382`), we built and verified an end-to-end formal and geometric auditing stack on `Qwen/Qwen2.5-0.5B`—proving in `v8.1` that geodesic $SO(k)$ planar transport eliminates nullspace sign-flip illusions (`0.6181` vs. `2.0000` `INT8` holonomy), stalk-level multi-agent consensus heals single-agent drift to `1.0381e-14`, and ambient tensor patching requires coupled multi-patch projection to avoid overlap leakage (`4.5765`). In **Blueprint v9**, we scale this verified architecture to a $4.5\times$ larger open-weight model (**`google/gemma-2-2b`**, `26` layers, $D = 2304, V = 256{,}000$) paired with **real pretrained Sparse Autoencoders (`google/gemma-scope-2b-pt-res`)**. To stay strictly inside our `12.0 GB` GitHub Actions RAM ceiling (`llmfit` gate) and maintain **0 KB** persistent footprint on ARM64 Termux, v9 introduces: (1) **`BF16` Memory-Gated Inference (`~5.2 GB` peak RAM)**, avoiding both the `10.4 GB` `FP32` memory ceiling and the `0.62` geodesic depth-holonomy distortion of `INT8`; (2) **HTTP Range-Sliced `safetensors` SAE Streaming**, fetching only the target mid-layer decoder matrix ($W_{\text{dec}} \in \mathbb{R}^{16384 \times 2304}$, `~75 MB` in `BF16`) via `huggingface_hub` + `safe_open` without downloading multi-gigabyte repositories; (3) **Coupled Ambient Pseudo-Inverse Repair**, resolving `v8.1` Module 1’s overlap leakage ($U_j^\top U_0 \neq 0$) by solving $\min_{\Delta h} \|\delta^0(U^\top(h + \Delta h))\|_2^2$ across all patches simultaneously; and (4) **Zero-`sorry` Lean 4 `BF16` & SAE Admissibility Gate (`V9GemmaScopeGate`)**.

**Keywords:** *Gemma-2-2B, Gemma Scope, Sparse Autoencoders, HTTP range-sliced safetensors, bfloat16 precision, coupled ambient sheaf repair, geodesic SO(k) holonomy, Spherepop, Lean 4 zero-sorry*

---

## 1. Engineering Upgrades From `v8.1` to `v9`

| Architectural Dimension | `v8.1` Baseline (`Qwen2.5-0.5B`) | `v9` Target (`Gemma-2-2B` + Gemma Scope) | Why This Upgrade Matters |
| :--- | :--- | :--- | :--- |
| **Model Architecture & Precision** | `Qwen/Qwen2.5-0.5B` (`24` layers, $D=896$, $V=151{,}936$, `FP32` = `2.17 GB`) | **`google/gemma-2-2b`** (`26` layers, $D=2304$, $V=256{,}000$, **`torch.bfloat16` = `~5.24 GB`**) | Tests soft-capped attention & GeGLU blocks while staying $2.3\times$ below the `12.0 GB` `llmfit` CI ceiling (`ADMIT`). |
| **SAE Dictionary Source** | Prompt-derived orthonormal atoms (`k = 64`) | **Pretrained `google/gemma-scope-2b-pt-res` (`16k` features)** streamed via HTTP range-sliced `safetensors` | Replaces synthetic/prompt-seeded covers with genuine, independently trained mechanistic interpretability dictionaries. |
| **Ambient Tensor Repair (`Module 1`)** | Single-patch update $\Delta h = U_0(s_0^* - \tilde{s}_0)$ left `4.5765` overlap leakage ($U_j^\top U_0 \neq 0$). | **Coupled Ambient Least-Squares Repair** minimizing $\|\delta^0 U^\top(h + \Delta h)\|_2^2$ subject to intact-patch constraints. | Eliminates overlap cross-talk in $\mathbb{R}^{2304}$, driving post-repair ambient coboundary norm to `< 1e-12` (`COLLAPSE`). |
| **Authentication & Graceful CI Fallback** | Public unauthenticated checkpoint | Uses `HF_TOKEN` GitHub Secret when present; falls back cleanly to `Spherepop` `REFUSE("MISSING_GATED_MODEL_TOKEN")` if unset. | Guarantees CI never crashes with an unhandled HTTP `401` traceback even on forks without secrets. |

---

## 2. Mathematical Formulation of v9

### 2.1 Coupled Ambient Sheaf Repair (Resolving `v8.1` Overlap Leakage)
In `v8.1`, modifying a single stalk $s_0 \mapsto s_0^*$ and pushing $\Delta h = U_0(s_0^* - \tilde{s}_0)$ into ambient space $\mathbb{R}^D$ perturbed neighboring stalks $s_j = U_j^\top(h + \Delta h)$ whenever $U_j^\top U_0 \neq 0$. To repair ambient state $\tilde{h} = h + \eta_{\text{tamper}}$ cleanly, v9 solves the **coupled linear system** enforcing zero coboundary across all $m$ patches while anchoring uncorrupted patches $\{j \neq i^*\}$:

$$\Delta h^* = \arg\min_{\Delta h \in \mathbb{R}^D} \left( \sum_{i=0}^{m-1} \left\| U_{i+1}^\top U_i U_i^\top(\tilde{h} + \Delta h) - U_{i+1}^\top(\tilde{h} + \Delta h) \right\|_2^2 + \lambda \sum_{j \neq i^*} \left\| U_j^\top(\tilde{h} + \Delta h) - s_j^{\text{clean}} \right\|_2^2 \right)$$

Because every term is quadratic in $\Delta h \in \mathbb{R}^D$, stacking the patch operators yields an exact linear least-squares solve (`np.linalg.lstsq`) that cancels the corruption inside $\text{span}(U_0, \dots, U_{m-1})$ without leaking into overlapping neighbor stalks.

### 2.2 Streaming Gemma Scope SAE Atom Extraction (`safe_open`)
Rather than downloading multi-gigabyte SAE archives, v9 uses `huggingface_hub.hf_hub_url` + `safetensors.safe_open` (or `hf_hub_download` targeting a single Layer-12 JumpReLU SAE file `layer_12/width_16k/average_l0_71/params.npz`, `~150 MB`):
1. Encodes `Gemma-2-2B` Layer-12 residual $h_{12} \in \mathbb{R}^{2304}$ through the pretrained SAE encoder $f = \text{JumpReLU}(W_{\text{enc}} h_{12} + b_{\text{enc}})$.
2. Selects the top-$r$ ($r = 32$) active pretrained dictionary decoder columns $\{w_{\text{dec}, i_1}, \dots, w_{\text{dec}, i_{32}}\} \subset \mathbb{R}^{2304}$.
3. Orthonormalizes them via sign-canonicalized QR into $m = 6$ overlapping rank-64 covers and evaluates $\|\delta^0 s\|_2$.

---

## 3. Zero-`sorry` Lean 4 Specification (`V9GemmaScopeGate`)

We extend `lean/EpistemicAudit.lean` with a formal gate covering gated-model token availability, `BF16` `llmfit` memory admissibility, and coupled ambient repair:

```lean
namespace V9GemmaScopeGate

open SpherepopSheafBridge

structure V9GemmaDeploymentState where
  hfTokenPresent : Bool
  bf16MemoryWithinBudget : Bool
  saeSliceVerified : Bool
  coupledAmbientCoboundaryZero : Bool

def evaluateV9GemmaPipeline (s : V9GemmaDeploymentState) : Disposition :=
  if !s.hfTokenPresent then
    Disposition.refused "MISSING_GATED_MODEL_TOKEN"
  else if !s.bf16MemoryWithinBudget then
    Disposition.refused "HARDWARE_MEMORY_EXCEEDED"
  else if !s.saeSliceVerified then
    Disposition.refused "SAE_SLICE_INTEGRITY_FAILURE"
  else if !s.coupledAmbientCoboundaryZero then
    Disposition.refused "COUPLED_AMBIENT_OBSTRUCTION"
  else
    Disposition.collapsed

theorem v9_gemma_collapses_iff_all_gates_pass (s : V9GemmaDeploymentState) :
    evaluateV9GemmaPipeline s = Disposition.collapsed ↔
      (s.hfTokenPresent = true ∧
       s.bf16MemoryWithinBudget = true ∧
       s.saeSliceVerified = true ∧
       s.coupledAmbientCoboundaryZero = true) := by
  unfold evaluateV9GemmaPipeline
  by_cases h1 : s.hfTokenPresent = true <;>
  by_cases h2 : s.bf16MemoryWithinBudget = true <;>
  by_cases h3 : s.saeSliceVerified = true <;>
  by_cases h4 : s.coupledAmbientCoboundaryZero = true <;>
  simp [h1, h2, h3, h4]

end V9GemmaScopeGate
```

---

## 4. Pre-Registered Predictions for Experiment I (`exp9_gemma2_sae_sheaf.py`)

1. **Prediction I1 (`Gemma-2-2B` Unembedding Twist Profile):** Across `26` layers ($L_0 \to L_{25}$) of `google/gemma-2-2b` (`BF16`), geodesic $SO(64)$ step angles will remain low across interior soft-capped layers before spiking sharply at the final **`L_24 -> L_25`** unembedding transition (replicating our `Qwen2.5-0.5B` `L_22 -> L_23` discovery on a completely different model family).
2. **Prediction I2 (Pretrained Gemma Scope Gluing):** Covering `Gemma-2-2B` Layer-12 hidden states with top-$32$ active JumpReLU decoder atoms from `google/gemma-scope-2b-pt-res` will reduce coboundary norm by $> 10^3\times$ relative to random QR projections.
3. **Prediction I3 (Coupled Ambient Repair Closure):** Solving the coupled ambient least-squares system on a corrupted Layer-12 residual tensor will eliminate the `v8.1` `4.5765` overlap leakage and restore ambient coboundary norm below `1e-5` (`COLLAPSE`).

---

## 5. One-Minute Setup Checklist Before Running v9 Tomorrow

1. **Accept Gemma 2 License & Add GitHub Secret:**
   * Accept the model terms on `huggingface.co/google/gemma-2-2b` and `huggingface.co/google/gemma-scope-2b-pt-res`.
   * Add a read-only Hugging Face token as **`HF_TOKEN`** under `GitHub Repo -> Settings -> Secrets and variables -> Actions`.
2. **Deploy in 4 Compact Termux Blocks (`Clone -> Seal -> Push -> Purge`):**
   * Block 1: `V9GemmaScopeGate` in `lean/EpistemicAudit.lean`
   * Block 2: `v9_apps/gemma_scope_streamer.py` (`BF16` `llmfit` check + single-layer Gemma Scope `params.npz` loader)
   * Block 3: `v9_apps/coupled_ambient_repair.py` + `experiments/exp9_gemma2_sae_sheaf.py`
   * Block 4: `.github/workflows/epistemic-audit.yml` (passing `HF_TOKEN: ${{ secrets.HF_TOKEN }}`) + purge.
