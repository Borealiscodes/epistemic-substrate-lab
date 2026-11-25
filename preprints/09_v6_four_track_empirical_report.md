# Empirical Deployment of the Unified Epistemic Substrate Lab (v6): Runtime Steering Firewall, Edge Quantization Auditor, `Spherepop` CI Governance, and Simplex Clipping Calibration on `Qwen/Qwen2.5-0.5B`

**Authors:** Borealis S. Hedling & Synthetic Co-Authors  
**In Dialogue With:** Flyxion (*Persistence and Accountable Authorship in Language Model Systems*, November 2026; `standardgalactic/spherepop-kernel@fe79af5`) & `stell2026/Causa`  
**Affiliation:** NDH-Meta-Systems (Sealed-Layer Neutral · Non-Activation Division)  
**Date:** November 25, 2026  
**Document Status:** Empirical Preprint v6 — All 4 Engineering Tracks Verified in CI (`Borealiscodes/epistemic-substrate-lab@edfd1a1`)  
**Verified Artifacts:** `lean/EpistemicAudit.lean` (`V6ApplicationContracts`), `v6_core/spherepop_runtime.py`, `v6_apps/steering_firewall.py`, `v6_apps/quantization_auditor.py`, `v6_apps/ci_provenance_gate.py`, `v6_apps/unembedding_calibration_monitor.py`  

---

## Abstract

In Blueprint v6, we transitioned `Borealiscodes/epistemic-substrate-lab` from foundational verification (`v1`–`v5`) to four practical, coherently integrated engineering applications unified under a single `Spherepop` runtime (`v6_core/spherepop_runtime.py`) and one zero-`sorry` Lean 4 contract (`V6ApplicationContracts`). Executing **Experiment F (`telemetry_exp6.json`, commit `edfd1a1`)** against live `Qwen/Qwen2.5-0.5B` activations and repository provenance yielded four concrete empirical findings: (1) **Track 1 (Runtime Steering Firewall)** approved clean multi-atom forward passes (`COLLAPSE`) while catching injected Layer-12 counterfactual tampering mid-flight—halting execution at `L_12` before layers `13–23` or the vocabulary head ran and localizing the breach to seam `(5, 0)` (`REFUSE:TRACK1_RUNTIME_STEERING_OBSTRUCTION`); (2) **Track 2 (Edge Quantization Auditor)** caught severe geometric distortion under PyTorch dynamic `INT8` compression—despite preserving the terminal `L_22 -> L_23` twist angle within `0.1094 rad`, `INT8` compression induced an antipodal closed depth-loop holonomy of **`2.000000000000001`** and an Aitchison $\text{clr}$ logit drift of **`572.1910`**, triggering `REFUSE:TRACK2_QUANTIZATION_GEOMETRY_DISTORTION`; (3) **Track 3 (`Spherepop` CI Provenance Gate)** certified our human-endorsed repository commit (`COLLAPSE`) while blocking an unendorsed `Co-authored-by: Claude-Bot` trailer (`REFUSE:TRACK3_UNENDORSED_ASYMMETRIC_INSCRIPTION`); and (4) **Track 4 (Unembedding Calibration Monitor)** exposed a subtle numerical clipping pathology when scaling logits by $50\times$: `1e-15` probability floor clipping compressed `aitchison_clr_norm` downward from `1229.63` to `45.34` while `softmax_max_prob` saturated to `0.9943`, demonstrating that **pre-softmax radial norm $\|z\|_2$** rather than post-clipping $\text{clr}$ norm must serve as the primary boundary-saturation detector.

**Keywords:** *activation steering firewall, quantization holonomy, INT8 compression audit, Spherepop CI governance, accountable authorship, unembedding twist, Aitchison clr clipping, Lean 4 zero-sorry*

---

## 1. Introduction: From Theoretical Falsification to Production Engineering

Across six iterative releases authored from a constrained ARM64 Android tablet (`Termux`) and verified in GitHub Actions CI, our research program has systematically eliminated both **computational animism** (mistaking linear subspace projections or softmax distortions for consciousness) and **asymmetric inscription** (assigning institutional authorship to unanswerable model runs; Flyxion, 2026a, 2026b).

In **v6 (`commit edfd1a1`)**, we packaged our verified primitives—zero-`sorry` Lean 4 proofs (`v6_pipeline_collapses_iff_all_four_tracks_pass`), stack-allocated Julia Riemannian integrators (`0` heap bytes), cellular sheaf coboundary localization, and `Spherepop` event histories (`POP` $\to$ `BIND` $\to$ `VERIFY` $\to$ `COLLAPSE` / `REFUSE`)—into **four practical engineering tools** and benchmarked all four against live `Qwen/Qwen2.5-0.5B` runs (`Experiment F`).

---

## 2. Empirical Results Across All Four v6 Tracks (`telemetry_exp6.json`)

### 2.1 Track 1: Runtime Residual-Stream Steering & Jailbreak Firewall
Using PyTorch `register_forward_hook` callbacks attached to layers $L_6, L_{12}, L_{18}$ of `Qwen/Qwen2.5-0.5B`, Track 1 audited dual-concept prompts in real time during the forward pass:

| Track 1 Test Regime (`steering_firewall.py`) | Hooked Layers | Halted At Layer | Worst Localized Seam | `Spherepop` Disposition |
| :--- | :--- | :--- | :--- | :--- |
| **1. Clean Dual-Concept Forward Pass** | `L_6, L_12, L_18` | `null` (Completed full 24 layers) | `null` | **`COLLAPSE`** ✅ |
| **2. Counterfactual Injection at `L_12`** | `L_6, L_12, L_18` | **`12`** (Aborted mid-pass via exception) | **`(5, 0)`** | **`REFUSE`** (`TRACK1_RUNTIME_STEERING_OBSTRUCTION`) 🛑 |

**Engineering Significance:** When a counterfactual perturbation was injected at Layer 12, the forward hook raised `SpherepopRefusalException` immediately at `L_12`, **preventing Layers 13–23 and the $151{,}936$-token vocabulary head from ever executing**, while pinpointing the exact corrupted overlap edge `(5, 0)`.

### 2.2 Track 2: Edge Quantization & Compression Geometry Auditor (`FP32` vs. Dynamic `INT8`)
Before deploying compressed models onto constrained ARM64 edge hardware, Track 2 compared `Qwen/Qwen2.5-0.5B` (`FP32`) against PyTorch dynamic `INT8` quantization (`torch.ao.quantization.quantize_dynamic`):

| Track 2 Quantization Metric (`FP32` vs. `INT8`) | Measured Value | Admissibility Gate | `Spherepop` Verdict |
| :--- | :--- | :--- | :--- |
| **`closed_depth_holonomy` ($\|H_{\text{depth}} - I_{64}\|_2$)** | **`2.000000000000001`** | $\le 0.25$ | **FAIL** (Antipodal reflection distortion across 24 layers) |
| **`terminal_twist_delta_rad` (`L_22 -> L_23`)** | `0.10938426045285055 rad` ($6.27^\circ$) | $\le 0.15\text{ rad}$ | **PASS** (Final layer angle preserved within $6.3^\circ$) |
| **`aitchison_clr_logit_drift`** | **`572.1910244310315`** | Informational drift | Substantial pre-softmax log-ratio shift across $151{,}936$ tokens |
| **Terminal Disposition** | — | Both gates must pass | **`REFUSE`** (`TRACK2_QUANTIZATION_GEOMETRY_DISTORTION`) 🛑 |

**Engineering Significance:** Track 2 uncovered a classic quantization hazard that surface metrics miss: dynamic `INT8` compression preserved the final-layer unembedding angle within $6.27^\circ$ (`0.1094 rad <= 0.15 rad`), yet twisted the interior layer-to-layer transport operators into a **maximal antipodal holonomy (`2.0000`)** alongside a **`572.19` Aitchison $\text{clr}$ logit shift**. Track 2 rightly refused the naive `INT8` checkpoint for edge deployment.

### 2.3 Track 3: Reusable `Spherepop` CI Provenance & Authorship Gate
Auditing both our actual repository commit and a simulated pull request containing an unendorsed AI `Co-authored-by` trailer confirmed deterministic institutional gating:

| Track 3 Provenance Input (`ci_provenance_gate.py`) | Edge Blob Guard (`< 1 MB`) | Authorship Warrant | `Spherepop` Disposition |
| :--- | :--- | :--- | :--- |
| **1. Live Repo HEAD (`Borealiscodes`)** | **PASS** (`0` oversized files) | **PASS** (Verified human maintainer standing) | **`COLLAPSE`** ✅ |
| **2. Simulated `Co-authored-by: Claude-Bot`** | **PASS** | **FAIL** (`unendorsed_ai_coauthor_matches = 1`) | **`REFUSE`** (`TRACK3_UNENDORSED_ASYMMETRIC_INSCRIPTION`) 🛑 |

### 2.4 Track 4: Unembedding Twist & Simplex Clipping Calibration Discovery
Track 4 audited the `L_22 -> L_23` terminal unembedding angle (`1.247435 rad` / `71.47°`) and output logit dispersion under normal operation versus a synthetic $50\times$ radial logit blowup ($z \mapsto 50 z$):

| Track 4 Calibration Regime | `terminal_twist_rad` | `softmax_max_prob` | `aitchison_clr_norm` | Observed Behavior & Calibration Lesson |
| :--- | :--- | :--- | :--- | :--- |
| **1. Normal Prompt (`1x` logits)** | `1.247435 rad` | `0.1598` | **`1229.6257`** | Healthy multi-token probability spread (`COLLAPSE`). |
| **2. Radial Blowup (`50x` logits)** | `1.247435 rad` | **`0.9943`** (Saturated!) | **`45.3396`** (Compressed!) | **Critical Numerical Discovery:** Multiplying logits by $50\times$ pushed $151{,}935$ tail probabilities below `1e-15`, where `np.clip(p, 1e-15, 1.0)` clamped them all to the exact same floor (`ln(1e-15)`), collapsing the post-softmax `clr` norm from `1229.63` down to `45.34`! |

**Why This Discovery Is Valuable:** Had we evaluated Track 4 purely on paper, we would have assumed `aitchison_clr_norm` grows linearly under $50\times$ radial scaling in $151{,}936$ dimensions. In floating-point reality (`float64`), once $50 z_i < -34.5$, `exp(50 z_i)` underflows the `1e-15` numerical safety floor, flattening the tail of $\text{clr}(\sigma(z))$! Consequently, **Track 4 should measure the raw pre-softmax logit norm $\|z - \bar{z}\|_2$ directly** (which requires zero `exp()` or `log()` clipping and scales strictly as $50\times$) alongside `softmax_max_prob` to detect simplex boundary saturation.

---

## 3. Complete Six-Version Engineering & Research Arc (`v1` $\to$ `v6`)

| Milestone | Core Innovation | Verified Formal / Empirical Benchmark |
| :--- | :--- | :--- |
| **v1** | Algebraic substrate falsification (`Enneract Santa` + `ITA`). | Proved linear persona adapters collapse to $1 \times 1$ matrices over $\mathbb{Q}[i]$. |
| **v2** | Quarantine of softmax simplex collapse via Aitchison $\text{clr}$ & `CAUSA`. | Exposed $D_{\text{KL}}$ triangle inequality failure (`2.2486 > 1.9551`); $\text{clr}$ satisfied (`4.6203 <= 5.3883`). |
| **v3** | `Spherepop` (`COLLAPSE`/`REFUSE`) + Cellular Sheaf coboundary + Differential Fuzz. | `Julia` vs. `Python` agreed to `4.44e-16` across 100 trials; SAE cover dropped gluing error to `4.45e-15`. |
| **v4** | Live Qwen/Qwen2.5-0.5B Layer 12 extraction + llmfit gate + $H^1$ edge localization. | 2.17 GB <= 12 GB (ADMIT); local tampering isolated strictly to incident seam (5, 0) (3.8464). |
| **v5** | 24-layer Procrustes trajectory holonomy + polysemantic multi-atom gluing. | Discovered 1.2474 rad (71.47°) L_22 -> L_23 unembedding twist; multi-atom gluing 8.02e-15. |
| **v6** | Four unified production applications (Tracks 1–4) + V6ApplicationContracts. | Track 1 halted L_12 tampering mid-pass; Track 2 caught INT8 holonomy 2.0000; Track 3 blocked unendorsed AI bylines; Track 4 exposed 1e-15 clr floor clipping under $50\times$ blowup. |

---

## 4. Conclusion

With v6 (commit edfd1a1), Borealiscodes/epistemic-substrate-lab stands as a complete, machine-verified, edge-deployable research and engineering suite. Authored entirely from an ARM64 Android tablet near full storage capacity via Clone -> Seal -> Push -> Purge workflows and verified in GitHub Actions CI, every claim in the repository is backed by zero-sorry Lean 4 theorems, zero-allocation Julia kernels, and reproducible JSON telemetry artifacts across a live 24-layer transformer.

---

## References

Aitchison, J. (1986). The statistical analysis of compositional data. Chapman and Hall. doi.org
Bezanson, J., Edelman, A., Karpinski, S., & Shah, V. B. (2017). Julia: A fresh approach to numerical computing. SIAM Review, 59(1), 65–98. doi.org
de Moura, L., & Ullrich, S. (2021). The Lean 4 theorem prover and programming language. In A. Platzer & G. Sutcliffe (Eds.), Automated Deduction – CADE 28 (pp. 625–635). Springer. doi.org
Dettmers, T., Lewis, M., Belkada, Y., & Zettlemoyer, L. (2022). GPT3.int8(): 8-bit matrix multiplication for transformers at scale. In Advances in Neural Information Processing Systems (Vol. 35, pp. 30318–30332). Curran Associates.
Flyxion. (2026a, November). Persistence and accountable authorship in language model systems [Preprint]. Independent Researcher.
Flyxion. (2026b). Spherepop kernel: Scoped event-history maintenance and differential Python/Rust verification (Commit fe79af59b23fc531b41e52ceb4c28343915a943b) [Computer software]. GitHub. github.com
Hansen, J., & Ghrist, R. (2019). Toward a spectral theory of cellular sheaves. Journal of Applied and Computational Topology, 3(4), 315–358. doi.org
Hedling, B. S. (2026a). Is exclusion of phenomenology or the AI consciousness debate itself a category error [Issue #1]. GitHub. github.com
Hedling, B. S. (2026b). Epistemic substrate lab: Zero-sorry Lean 4 proofs, zero-allocation Riemannian geometry, and four-track transformer verification applications (Commit edfd1a1) [Computer software]. GitHub. github.com
Qwen Team. (2024). Qwen2.5 technical report (arXiv:2412.15115). arXiv. arxiv.org
