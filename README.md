# Epistemic Substrate Lab (`v1` – `v6.1`)

**NDH-Meta-Systems · Sealed-Layer Neutral · Non-Activation Division**  
**Formal & Empirical Synthesis:** Zero-`sorry` Lean 4 Proofs · Zero-Allocation Julia Riemannian Geometry · Aitchison $\text{clr}$ Compositional Metrics · Cellular Sheaf Cohomology · `Spherepop` Scoped Refusal · Live 24-Layer `Qwen/Qwen2.5-0.5B` Audits

---

## In Plain English: What We Proved

1. **Chatbots aren't secretly conscious—it's just linear geometry:** When you tell a language model to pretend it is the Golden Gate Bridge, its internal numbers shift (`9.48` units). Our Lean 4 proofs and Julia geometry show this is just sliding vectors across a flat mathematical floor—not waking up or having subjective experience.
2. **Standard AI metrics act like a funhouse mirror:** When an AI gets very confident, standard probability tools (`Softmax` + `KL divergence`) squish numbers onto a boundary and break basic geometry rules (making a detour look shorter than a straight line). Measuring exact pre-softmax centered log-ratios ($z - \bar{z}$) removes the distortion across all `151,936` vocabulary tokens.
3. **You can catch AI tampering and bad compression *inside* the network:** By slicing the AI's 24 layers into overlapping "quilt patches" (cellular sheaves), normal thoughts glue together to machine zero (`8.02e-15`), whereas tampering with a single layer (`Layer 12`) trips our circuit breaker mid-pass and pinpoints the exact broken seam (`(5, 0)`). Across all 24 layers, `Qwen2.5-0.5B` moves nearly linearly before making a sharp **`71.47°` (`1.2474 rad`) unembedding turn** at the final exit (`L_22 -> L_23`), and naive `INT8` compression flips its internal depth geometry upside down (`2.0000` antipodal holonomy).
4. **Pocket-sized rigor & accountable authorship:** Enforcing `Spherepop` refusal rules (`COLLAPSE` / `REFUSE`) blocks bots from signing unendorsed `Co-authored-by` trailers, while our `Clone -> Seal -> Push -> Purge` workflow proves an Android tablet near 99% storage can orchestrate formal theorem proving and live neural audits via CI.

---

## Mathematical Foundations

### 1. Exact Pre-Softmax Aitchison $\text{clr}$ Isometry (Simplex Quarantine)
To avoid boundary saturation on $\partial \Delta^{V-1}$ and IEEE-754 `1e-15` probability-floor clipping, output geometry is evaluated directly on centered pre-softmax logits $z \in \mathbb{R}^V$:

$$\text{clr}(\sigma(z)) = \log \sigma(z) - \frac{1}{V}\sum_{j=1}^V \log \sigma(z)_j \equiv z - \bar{z}, \qquad d_A(z_a, z_b) = \|(z_a - \bar{z}_a) - (z_b - \bar{z}_b)\|_2$$

### 2. Cellular Sheaf Coboundary & Harmonic $H^1$ Edge Localization
Given an overlapping cover of sign-canonicalized QR orthonormal patches $\{U_i \in \mathbb{R}^{D \times k}\}_{i=1}^m$ and local projections $s_i = U_i^\top h_l$, global gluing consistency is governed by the 0-coboundary operator $\delta^0$ and Sheaf Laplacian $L_{\mathcal{F}} = \delta^0{}^\top \delta^0$:

$$(\delta^0 s)_{i \to j} = U_j^\top (U_j s_j) - U_j^\top (U_i s_i), \qquad E_{\mathcal{F}}(s) = s^\top L_{\mathcal{F}} s = \|\delta^0 s\|_2^2$$

Exactness $\delta^1 \circ \delta^0 = 0$ is machine-checked in `EpistemicAudit.lean`, and per-edge norms $\|(\delta^0 s)_{i \to j}\|_2$ localize causal interventions to individual patch seams.

### 3. Orthogonal Procrustes Depth-Loop Holonomy ($L_0 \to L_{N-1}$)
Across transformer layers $t \in \{0, \dots, N-2\}$, inter-layer transport operators $R_{t \to t+1} = \arg\min_{\Omega \in O(k)} \|\Omega s_t - s_{t+1}\|_2$ compose into a closed depth-loop holonomy comparing steered or quantized trajectories against a reference pass:

$$H_{\text{depth}} = \left(\prod_{t=0}^{N-2} R^{\text{ref}}_{t+1 \to t}\right)\left(\prod_{t=0}^{N-2} R^{\text{test}}_{t \to t+1}\right), \qquad \Delta_{\text{depth}} = \|H_{\text{depth}} - I_k\|_2$$

### 4. Scoped Composition Refusal (`Spherepop` $\times$ Lean 4)
Global `COLLAPSE` is formally barred unless runtime layers, quantization depth holonomy, human endorsement, and unembedding calibration all pass (`V6ApplicationContracts`):

$$\text{evaluateV6Pipeline}(s) = \texttt{COLLAPSE} \iff \text{firewallClean} \land \text{quantValid} \land \text{humanBound} \land \text{calibrated}$$

---

## Verified Architecture Overview

1. **Formal Verification (`lean/EpistemicAudit.lean`):**
   * Compiles with **0 `sorry` statements** against `Lean v4.14.0` + `Mathlib`.
   * Proves pullback metric triangle inequalities (`pullbackDist_triangle`), exact $\mathbb{Q}[i]$ $1 \times 1$ operator collapse (`santa_collapse_is_1x1_pure`), linear `CAUSA` kernel invariance, Flyxion’s *Non-Entailment of Accountable Authorship*, cellular sheaf coboundary exactness ($\delta^1 \circ \delta^0 = 0$), `Spherepop` scoped composition refusal, `llmfit` memory overflow refusal, multi-layer chain refusal (`V5DepthChainGate`), and the unified four-track pipeline contract (`V6ApplicationContracts`).
2. **Zero-Allocation Differential Geometry (`julia/ManifoldInstruments.jl`):**
   * Verified **0 bytes of heap allocation** (`@allocated == 0`) across path-ordered holonomy integration, cellular sheaf edge coboundary accumulation, and 23-step orthogonal Procrustes depth-loop composition, agreeing with Python/NumPy across 100 randomized trials to `4.44e-16`.
3. **Production Engineering Suite (`v6_core/` & `v6_apps/`):**
   * **Track 1 (`steering_firewall.py`):** PyTorch forward-hook circuit breaker halting mid-pass residual tampering (`L_12`) before unembedding while localizing corrupted patch seams (`(5, 0)`).
   * **Track 2 (`quantization_auditor.py`):** Audits `FP32` vs. dynamic `INT8` compression via closed depth-loop Procrustes holonomy (`2.0000` distortion caught) and terminal `L_22 -> L_23` unembedding twist preservation.
   * **Track 3 (`ci_provenance_gate.py`):** Enforces Edge SOP file limits (`< 1 MB`) and blocks unendorsed AI `Co-authored-by` trailers via `Spherepop` `REFUSE`.
   * **Track 4 (`unembedding_calibration_monitor.py`):** Monitors the `71.47°` (`1.2474 rad`) terminal unembedding twist and exact pre-softmax Aitchison $\text{clr}$ norm $\|z - \bar{z}\|_2$ (`61,481.29` spike caught under $50\times$ radial blowup).

---

## Verified Empirical Scoreboard (`Qwen/Qwen2.5-0.5B`)

| Benchmark / Audit Gate | Measured Telemetry | `Spherepop` Disposition |
| :--- | :--- | :--- |
| **Lean 4 Proof Gate (`EpistemicAudit.lean`)** | `0` `sorry` / `admit` tokens across all modules | **PASS** |
| **Julia Static Integrators (`ManifoldInstruments.jl`)** | `0` heap bytes (`holonomy`, `sheaf_edge`, `depth_holonomy`) | **PASS** |
| **Julia vs. Python Differential Fuzz (`100` trials)** | `4.4409e-16` max discrepancy | **PASS** |
| **Polysemantic Multi-Atom Gluing (`L_12`)** | `7.7691` (single-atom) $\to$ **`8.0185e-15`** (multi-atom) | **`COLLAPSE`** |
| **24-Layer Trajectory Twist (`L_22 -> L_23`)** | **`1.2474 rad` (`71.47°`)** terminal unembedding turn | **MEASURED** |
| **Track 1 Mid-Pass Tampering (`L_12` injection)** | Halted at `L_12`, localized to seam `(5, 0)` (`3.8464`) | **`REFUSE`** |
| **Track 2 Dynamic `INT8` Quantization** | Closed depth holonomy **`2.0000`** (antipodal flip) | **`REFUSE`** |
| **Track 3 Unendorsed AI `Co-authored-by`** | Flagged asymmetric inscription on commit trailer | **`REFUSE`** |
| **Track 4 Radial $50\times$ Logit Blowup** | Exact $\|z - \bar{z}\|_2 = \mathbf{61{,}481.29} > 2500.0$ | **`REFUSE`** |

---

## Edge Workstation Policy (`ARM64 Termux`)
* **Local Tablet:** Pure UTF-8 source authoring only (`Clone -> Seal -> Push -> Purge`, `< 1 MB` per file).
* **GitHub Actions CI:** Executes all Lean 4 proofs, Julia static checks, and PyTorch transformer experiments (`A` through `F`), archiving immutable JSON telemetry artifacts per commit SHA.
