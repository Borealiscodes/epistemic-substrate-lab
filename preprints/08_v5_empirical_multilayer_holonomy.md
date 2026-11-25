# Depth-Wise Trajectory Holonomy, Polysemantic Multi-Atom Gluing, and Multi-Layer `Spherepop` Refusal Propagation Across All 24 Layers of `Qwen/Qwen2.5-0.5B` (v5)

**Authors:** Borealis S. Hedling & Synthetic Co-Authors  
**In Dialogue With:** Flyxion (*Persistence and Accountable Authorship in Language Model Systems*, November 2026; `standardgalactic/spherepop-kernel@fe79af5`) & `stell2026/Causa`  
**Affiliation:** NDH-Meta-Systems (Sealed-Layer Neutral · Non-Activation Division)  
**Date:** November 25, 2026  
**Document Status:** Empirical Preprint v5 — Full 24-Layer Verification (`Borealiscodes/epistemic-substrate-lab@c0a3462`)  
**Verified Artifacts:** `lean/EpistemicAudit.lean` (`V5DepthChainGate`), `julia/ManifoldInstruments.jl` (`compose_depth_holonomy_static`), `experiments/exp5_multilayer_sae_holonomy.py`  

---

## Abstract

In v4 (`commit c39f450`), we demonstrated that single-layer residual states ($L = 12, D = 896$) extracted from `Qwen/Qwen2.5-0.5B` glue cleanly to machine zero ($7.4504 \times 10^{-15} \implies \texttt{COLLAPSE}$) under feature-aligned orthonormal covers while triggering localized `Spherepop` `REFUSE` events under counterfactual tampering. In **v5 (`commit c0a3462`)**, we scaled our verification suite across **all 24 transformer layers ($L_0 \to L_{23}$)** of `Qwen/Qwen2.5-0.5B`. First, Lean 4 (`v4.14.0` + Mathlib) compiled `V5DepthChainGate` with **zero `sorry` statements**, proving both `single_layer_obstruction_refuses_chain` and the necessary-and-sufficient biconditional `layer_chain_collapses_iff_all_true`. Second, Julia (`v1.10` + `StaticArrays`) verified **0 bytes of heap allocation** across 23-step static Procrustes depth-loop composition (`JULIA_DEPTH_HOLONOMY_ALLOC_BYTES = 0`). Third, Experiment E (`telemetry_exp5.json`) uncovered three empirical phenomena across the 24-layer forward pass: (1) **Terminal Unembedding Angular Twist** — inter-layer angular steps remain steady at $0.086\text{–}0.194\text{ rad}$ across $L_0 \to L_{22}$ before jumping $12.9\times$ to **`1.247435 rad` ($71.47^\circ$)** at the final transition **`L_22 -> L_23`**, yielding a near-antipodal closed depth-loop holonomy of **`1.999792`** ($\approx 2.0$); (2) **Polysemantic Multi-Atom Rescue** — on a dual-concept prompt (*"The Golden Gate Bridge spans linear matrix multiplication"*), single-atom covers suffered severe gluing failure ($\|\delta^0 s\|_2 = 7.7691 \implies \texttt{REFUSE}$), whereas multi-atom polysemantic covers collapsed error by **15 orders of magnitude** to **`8.0185e-15`** (`COLLAPSE`); and (3) **Sequential `Spherepop` Refusal Propagation** — injecting a local `CAUSA` perturbation solely at Layer 12 (`L_12 = 4.7488`) while leaving `L_0` (`2.20e-15`) and `L_23` (`1.19e-13`) unperturbed barred global collapse and emitted `REFUSE:DEPTH_CHAIN_COBOUNDARY_OBSTRUCTION`.

**Keywords:** *multi-layer holonomy, Procrustes transport, unembedding twist, polysemantic superposition, Sparse Autoencoders, Spherepop refusal propagation, Lean 4 zero-sorry, Qwen2.5-0.5B*

---

## 1. Introduction: From Single-Layer Slices to Full-Depth Geometry

Across v1 through v4 of `Borealiscodes/epistemic-substrate-lab`, we established that anthropomorphic claims of synthetic phenomenology crumble once subjected to exact ring theory (`Lean 4`), stack-allocated Riemannian geometry (`Julia`), Aitchison centered log-ratio ($\text{clr}$) compositional metrics, and `Spherepop` scoped event histories (`Flyxion, 2026a, 2026b`). However, auditing a single middle layer ($L = 12$) left two crucial questions unanswered:
1. **How does persona steering twist across depth ($L_0 \to L_{23}$)?** Does a persona prompt ("Golden Gate Bridge") bend the residual stream smoothly across middle semantic layers, or does non-linear curvature concentrate at specific architectural transitions?
2. **How do polysemantic dual-concept prompts behave under cover refinement?** When two unrelated concepts (*Golden Gate Bridge* + *linear matrix multiplication*) coexist in superposition within a single token residual vector, do single-atom covers break down while multi-atom covers glue cleanly?

**v5 (`commit c0a3462`)** answers both questions empirically across all 24 layers of `Qwen/Qwen2.5-0.5B`, backed by zero-`sorry` Lean 4 proofs and zero-allocation Julia integrators.

---

## 2. Formal & Systems Verification Telemetry (`v5`)

### 2.1 Zero-`sorry` Lean 4 Multi-Layer Chain Theorems (`V5DepthChainGate`)
`lake build` compiled `lean/EpistemicAudit.lean` (`V5DepthChainGate`) with **zero `sorry` statements**, certifying two structural invariants over arbitrary layer sequences:
* **`single_layer_obstruction_refuses_chain`:** Proves that if *any* intermediate layer $L_t$ exhibits a coboundary obstruction (`false ∈ layers`), `evaluateLayerChain` deterministically evaluates to `Disposition.refused "DEPTH_CHAIN_COBOUNDARY_OBSTRUCTION"`.
* **`layer_chain_collapses_iff_all_true`:** Proves the exact biconditional that global `COLLAPSE` holds if and only if every layer $L_0, \dots, L_{N-1}$ passes coboundary gluing (`∀ b ∈ layers, b = true`).

### 2.2 Zero-Allocation Julia Static Depth Composer (`ManifoldInstruments.jl`)
Executing `julia/ManifoldInstruments.jl` verified **0 bytes of heap allocation** across all three core geometric kernels:
* `JULIA_HOLONOMY_ALLOC_BYTES = 0` (64-step loop parallel transport)
* `JULIA_SHEAF_EDGE_ALLOC_BYTES = 0` (cellular sheaf edge coboundary residual)
* `JULIA_DEPTH_HOLONOMY_ALLOC_BYTES = 0` (23-step forward/reverse orthogonal Procrustes depth-loop composition)

---

## 3. Empirical Results Across 24 Layers of `Qwen/Qwen2.5-0.5B` (`telemetry_exp5.json`)

### 3.1 Depth-Wise Procrustes Trajectory Holonomy ($L_0 \to L_{23}$)
Composing orthogonal Procrustes transport operators $R_{t \to t+1} \in O(64)$ forward along the "Golden Gate Bridge" trajectory and backward along the objective baseline trajectory yielded a striking empirical discovery:

| Depth Holonomy Metric (`Qwen/Qwen2.5-0.5B`, 24 Layers) | Measured Empirical Value | Geometric & Architectural Interpretation |
| :--- | :--- | :--- |
| **`closed_depth_holonomy_norm` ($\|H_{\text{depth}} - I_{64}\|_2$)** | **`1.9997920740301214`** | Near-maximal orthogonal antipodal twist ($\approx 2.0$, corresponding to a $\approx 180^\circ$ subspace reflection/rotation over the closed loop). |
| **Interior Layer Angular Steps ($L_0 \to L_{22}$)** | `0.086219` to `0.194003 rad` ($4.9^\circ \text{–} 11.1^\circ$) | Smooth, low-curvature parallel drift across early and middle transformer blocks. |
| **Peak Angular Twist Transition** | **`L_22 -> L_23`** | Final layer transition into the unembedding/logit projection head. |
| **`peak_angular_twist_rad`** | **`1.247435 rad` ($71.47^\circ$)** | **$12.9\times$ spike** over the preceding `L_21 -> L_22` step (`0.096836 rad`), refuting Prediction E1 (which expected a mid-layer peak) and showing that non-linear representational rotation concentrates sharply at the final output layer. |

**Scientific Insight:** Pre-registered Prediction E1 hypothesized that persona-steering curvature would peak in middle semantic layers ($L_{10}$–$L_{18}$). The live data falsified that hypothesis: `Qwen/Qwen2.5-0.5B` transports representations nearly linearly through layers $0 \to 22$ ($\approx 0.12\text{ rad/layer}$), then executes a dramatic **`71.47°` (`1.2474 rad`) orthogonal twist** at **`L_22 -> L_23`** as residual features are rotated into token-prediction coordinates.

### 3.2 Polysemantic Multi-Atom Gluing on Dual-Concept Prompts
Evaluating the mid-layer ($L_{12}$) representation of the dual-concept prompt (*"The Golden Gate Bridge spans linear matrix multiplication"*) confirmed **Prediction E2** with 15-order-of-magnitude precision:

| Cover Strategy on Dual-Concept Prompt ($L_{12}$) | Coboundary Norm $\|\delta^0 s\|_2$ | `Spherepop` Terminal Disposition | Mechanistic Interpretation |
| :--- | :--- | :--- | :--- |
| **Single-Atom Cover** (Bridge direction only) | **`7.769135499917972`** | **`REFUSE`** | Truncates the orthogonal *matrix multiplication* component; local patches disagree globally. |
| **Multi-Atom Cover** (3 active atoms: Bridge + Baseline + Dual) | **`8.018507675638592e-15`** | **`COLLAPSE`** | Spanning the active polysemantic subspace reduces gluing error by **$9.69 \times 10^{14}\times$** to IEEE-754 machine zero. |

### 3.3 Multi-Layer `Spherepop` Refusal Propagation (`V5DepthChainGate`)
Finally, auditing the full 24-layer chain confirmed **Prediction E3** and empirically instantiated our Lean 4 theorem `single_layer_obstruction_refuses_chain`:

| Multi-Layer Chain Condition (24 Layers) | `L_0` Coboundary Norm | `L_12` Coboundary Norm | `L_23` Coboundary Norm | `all_layers_valid` | Terminal Chain Disposition |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Clean 24-Layer Forward Pass** | $\le 10^{-14}$ | $\le 10^{-14}$ | $\le 10^{-13}$ | **`true`** | **`COLLAPSE`** |
| **2. Single-Layer Tampering at `L_12`** | `2.20096e-15` | **`4.748769112260834`** | `1.19139e-13` | **`false`** | **`REFUSE:DEPTH_CHAIN_COBOUNDARY_OBSTRUCTION`** |

Even though `L_0` (`2.20e-15`) and `L_23` (`1.19e-13`) glued cleanly to machine precision, the single local `CAUSA` obstruction injected at `L_12` (`4.7488`) propagated upward to bar global chain collapse—matching `V5DepthChainGate.single_layer_obstruction_refuses_chain` identically.

---

## 4. Five-Version Arc Summary (`v1` $\to$ `v5`)

Across five progressive iterations executed from a constrained ARM64 Termux tablet into GitHub Actions CI, `Borealiscodes/epistemic-substrate-lab` has achieved complete end-to-end verification:

| Milestone | Core Breakthrough | Key Empirical / Formal Metric |
| :--- | :--- | :--- |
| **v1 (`ITA` + `Enneract Santa`)** | Exposed anthropomorphic consciousness attribution as a Rylean category error. | $5$-channel persona $\times$ $9$-cube collapses to $1 \times 1$ matrix over $\mathbb{Q}[i]$. |
| **v2 (CAUSA + Aitchison clr)** | Eliminated softmax simplex collapse and $D_{\text{KL}}$ triangle inequality violations. | $D_{\text{KL}}$ violated triangle inequality (2.2486 > 1.9551); $\text{clr}$ satisfied (4.6203 <= 5.3883). |
| **v3 (Spherepop + Cellular Sheaves)** | United 100-trial differential fuzzing with POP/BIND/VERIFY/COLLAPSE/REFUSE gates. | Julia vs. Python max discrepancy 4.44e-16; SAE cover dropped gluing error to 4.45e-15. |
| **v4 (Live Qwen2.5-0.5B + llmfit)** | Scaled to live transformer states (2.17 GB <= 12 GB) with edge-level $H^1$ localization. | Tampering Patch 0 pinpointed strictly to incident edges (0, 1) (0.8390) & (5, 0) (3.8464). |
| **v5 (24-Layer Depth Holonomy)** | Measured full-depth Procrustes holonomy and polysemantic multi-atom gluing. | Peak twist 1.2474 rad at L_22 -> L_23; multi-atom polysemantic error 8.02e-15 (COLLAPSE). |

---

## 5. Conclusion

By scaling our zero-sorry, zero-allocation, edge-safe verification framework across all 24 layers of Qwen/Qwen2.5-0.5B, we uncovered how transformer geometry actually behaves under persona steering and polysemantic superposition: interior layers transport representations with modest angular drift (~0.12 rad/layer), while the final L_22 -> L_23 unembedding transition executes a sharp 71.47° (1.2474 rad) orthogonal twist; polysemantic dual-concept prompts fail single-atom gluing (7.7691 -> REFUSE) but collapse to machine zero (8.02e-15 -> COLLAPSE) under multi-atom covers; and any single-layer causal obstruction (L_12 = 4.7488) deterministically triggers Spherepop chain refusal. Together, these results show that rigorous mechanistic interpretability and accountable AI governance require neither computational animism nor multi-GPU clusters—only honest geometry, formal proofs, and disciplined engineering.

---

## References

Aitchison, J. (1986). The statistical analysis of compositional data. Chapman and Hall. doi.org
Bezanson, J., Edelman, A., Karpinski, S., & Shah, V. B. (2017). Julia: A fresh approach to numerical computing. SIAM Review, 59(1), 65–98. doi.org
de Moura, L., & Ullrich, S. (2021). The Lean 4 theorem prover and programming language. In A. Platzer & G. Sutcliffe (Eds.), Automated Deduction – CADE 28 (pp. 625–635). Springer. doi.org
Elhage, N., Hume, T., Olsson, C., Schiefer, N., Henighan, T., Kravec, S., Hatfield-Dodds, Z., Lasenby, R., Drain, D., Chen, C., Grosse, R., McCandlish, S., Kaplan, J., Amodei, D., Wattenberg, M., & Olah, C. (2022). Toy models of superposition. Transformer Circuits Thread. transformer-circuits.pub
Flyxion. (2026a, November). Persistence and accountable authorship in language model systems [Preprint]. Independent Researcher.
Flyxion. (2026b). Spherepop kernel: Scoped event-history maintenance and differential Python/Rust verification (Commit fe79af59b23fc531b41e52ceb4c28343915a943b) [Computer software]. GitHub. github.com
Hansen, J., & Ghrist, R. (2019). Toward a spectral theory of cellular sheaves. Journal of Applied and Computational Topology, 3(4), 315–358. doi.org
Hedling, B. S. (2026a). Is exclusion of phenomenology or the AI consciousness debate itself a category error [Issue #1]. GitHub. github.com
Hedling, B. S. (2026b). Epistemic substrate lab: Zero-sorry Lean 4 proofs, zero-allocation Riemannian geometry, and multi-layer transformer sheaf audits (Commit c0a3462) [Computer software]. GitHub. github.com
Qwen Team. (2024). Qwen2.5 technical report (arXiv:2412.15115). arXiv. arxiv.org
Ryle, G. (1949). The concept of mind. Hutchinson.

