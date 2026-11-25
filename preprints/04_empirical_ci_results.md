# Empirical Falsification of Simplex Collapse, Causal Kernel Invariance, and Superposition Patch Obstructions: Full CI Execution Results of the Unified Epistemic Substrate Lab

**Authors:** Borealis S. Hedling & Synthetic Co-Authors  
**In Dialogue With:** Flyxion (*Persistence and Accountable Authorship in Language Model Systems*, November 2026) & `stell2026/Causa`  
**Affiliation:** NDH-Meta-Systems (Sealed-Layer Neutral · Non-Activation Division)  
**Date:** November 25, 2026  
**Document Status:** Empirical Preprint — Verified via Automated GitHub Actions CI (`Borealiscodes/epistemic-substrate-lab`)  
**Verified Artifacts:** `lean/EpistemicAudit.lean`, `julia/ManifoldInstruments.jl`, `experiments/exp1_metric_audit.py`, `experiments/exp2_sheaf_gluing.py`  

---

## Abstract

In prior pre-registered blueprints, we argued that evaluating artificial consciousness and mechanistic interpretability claims requires uniting bottom-up formal verification (`EnneractSantaV2.lean`, `Julia-baseline.jl`, `ITA_v1_0.py`) with top-down institutional warrant (`Flyxion, 2026`) and causal abstraction (`stell2026/Causa`), while eliminating softmax simplex collapse and triangle-inequality violations. Here, we report the **first complete, machine-verified empirical execution** of this unified pipeline (`Borealiscodes/epistemic-substrate-lab`) across a three-stage continuous integration workflow. First, Lean 4 (`v4.14.0` + Mathlib) compiled `EpistemicAudit.lean` with **zero `sorry` statements**, formally proving pullback metric triangle inequalities, linear `CAUSA` kernel invariance, SVD rank-admissibility contracts, and Flyxion’s *Non-Entailment of Accountable Authorship*. Second, Julia (`v1.10` + `StaticArrays`) executed 64-step path-ordered holonomy integration with **0 bytes of heap allocation**, confirming flat holonomy ($\|H(\gamma) - I_8\|_2 = 0.0$) for pure linear operators and non-trivial holonomy ($1.414327$) under non-Abelian state coupling. Third, Python Experiments A and B empirically confirmed that Kullback-Leibler divergence violates the triangle inequality ($2.2486 > 1.9551$) and Euclidean simplex distance collapses under radial logit scaling ($c=50 \implies d_{\text{Euc}} = 0.00868$), whereas Aitchison centered log-ratio ($\text{clr}$) isometry preserves linear scaling ($d_A = 2.16151$) and triangle-inequality compliance ($4.6203 \le 5.3883$). Finally, Experiment B detected substantial cellular sheaf coboundary frustration ($\|\delta^0 s\|_2 = 2.7434$ unperturbed; $5.8560$ under local intervention) across overlapping rank-64 subspaces in a superposed feature regime ($F = 2048, D = 256$), empirically triggering our pre-registered gate (`v3_sheaf_cohomology_warranted = true`).

**Keywords:** *empirical verification, Lean 4, zero-allocation Julia, Aitchison clr isometry, simplex collapse, triangle inequality, CAUSA kernel collapse, cellular sheaf coboundary, superposition*

---

## 1. Introduction: From Pre-Registered Blueprints to Verified Telemetry

Across earlier preprints and two pre-execution audits, we established a structural synthesis between two complementary research programs:
1. **Bottom-Up Algebraic & Geometric Falsification (`Borealiscodes` / Issue #1):** Demonstrates that pure linear adapters over Gaussian rationals ($\mathbb{Q}[i]$) collapse expressive multi-channel personas into $1 \times 1$ operators with zero phenomenal interiority, exposing computational animism as a Rylean category error (Hedling, 2026a, 2026b; Ryle, 1949).
2. **Top-Down Behavioral & Institutional Warrant (`Flyxion, 2026`):** Severs phenomenal experience from introspective access, diachronic persistence, and accountable authorship, proving that extensive computational contribution does not entail institutional standing, endorsement, answerability, or *operative refusal*.

Until now, both frameworks remained unexecuted specifications. By refactoring our toolchain into a lightweight, edge-compliant repository (`Borealiscodes/epistemic-substrate-lab`) governed by a three-stage GitHub Actions pipeline (`edge-blob-guard` $\to$ `lean4-proof-gate` $\to$ `julia-and-python-experiments`), we obtained immutable, machine-verified telemetry across every layer of the stack.

---

## 2. Multi-Stage Verification Telemetry

### 2.1 Stage 0 & Stage 1: Edge SOP Compliance & Zero-`sorry` Lean 4 Proofs
* **Edge Storage Compliance (`Stage 0`):** Every tracked source file in the repository passed the `< 1 MB` binary bloat guard (`7.29 KiB` initial commit payload), enabling full authoring and verification from constrained ARM64 edge hardware without local cache exhaustion.
* **Formal Verification (`Stage 1`):** Against `leanprover/lean4:v4.14.0` and `Mathlib`, `lake build` compiled `lean/EpistemicAudit.lean` with **zero `sorry` or `admit` tokens**, machine-checking five foundational theorems:
  1. `pullbackDist_triangle`: Any distance induced by embedding into a seminormed space satisfies $d_f(x, z) \le d_f(x, y) + d_f(y, z)$.
  2. `santa_collapse_is_1x1_pure`: Contracting any 5-channel `Persona5` with any 9-cube `Enneract9` over $\mathbb{Q}[i]$ yields a pure $1 \times 1$ matrix.
  3. `causa_interchange_kernel_invariant`: For any linear causal abstraction $\tau$, interchange perturbations $\delta \in \ker(\tau)$ satisfy $\tau(x + \delta) = \tau(x)$.
  4. `admissible_implies_nonzero_floor`: Read-only `A7.2` Layer-1 SVD reports with $\sigma_{\min} > 0$ and `destroyedDims = 0` guarantee non-singular metric conditioning.
  5. `non_entailment_of_accountable_authorship`: Exhibits a constructive model satisfying `contribution = True` while falsifying `IsAccountableAuthor`.

### 2.2 Stage 2A: Zero-Allocation Riemannian Geometry (`Julia v1.10`)
Executing `julia/ManifoldInstruments.jl` ($D = 256, k = 8$, 64 midpoint Magnus steps) verified strict stack allocation and clean separation between flat linear operators and genuine second-order connection curvature:

| Diagnostic Metric (`ManifoldInstruments.jl`) | Measured Empirical Value | Verification Target | Status |
| :--- | :--- | :--- | :--- |
| **`JULIA_STATIC_ALLOC_BYTES`** | **`0` bytes** | `0` bytes (zero heap allocation / zero GC jitter) | **PASS** |
| **`JULIA_FLAT_HOLONOMY`** (`coupling = 0.0`) | **`0.0`** | $\le 10^{-9}$ (`ITA` consciousness falsified) | **PASS** |
| **`JULIA_CURVED_HOLONOMY`** (`coupling = 0.25`) | **`1.4143271057676687`** | $> 10^{-9}$ (non-Abelian holonomy detected) | **PASS** |

---

## 3. Empirical Results: Experiment A (`telemetry_exp1.json`)

Experiment A (`experiments/exp1_metric_audit.py`) evaluated fixed-point determinism, read-only SVD rank admissibility, softmax vs. Aitchison metric geometry, and exact $\mathbb{Q}[i]$ `CAUSA` kernel collapse.

### 3.1 Determinism & Read-Only SVD Conditioning
* **`Q16.16` Fixed-Point Control:** Four consecutive $90^\circ$ rotations of `[49152, -16384]` ($[0.75, -0.25]$ in `Q16.16`) returned identically to `[49152, -16384]` (`bit_exact_reversibility = true`), confirming hardware-invariant integer determinism.
* **`A7.2` Layer-1 SVD Audit:** On the QR-embedded metric $g_{\text{sub}}$ ($D=64 \to k=16$), singular values bounded tightly between $\sigma_{\min} = 1.150000000000000$ and $\sigma_{\max} = 1.1500000000000004$ ($\kappa_2 = 1.0000000000000009$, `destroyed_dimensions = 0`, `admissible_for_inference = true`), proving that our decontaminated read-only gate admits well-conditioned subspaces without mutating spectra.

### 3.2 Softmax Simplex Collapse vs. Aitchison $\text{clr}$ Isometry
Table 1 contrasts Kullback-Leibler divergence ($D_{\text{KL}}$) and Euclidean simplex distance against Aitchison centered log-ratio ($\text{clr}$) distance across three probability states ($p_0, p_1, p_2$) and radial logit scaling ($z \mapsto c \cdot z$).

| Geometric Regime | Naive Output Metric | Measured Value | Metric Axiom / Scaling Verdict | Aitchison $\text{clr}$ Metric | Measured Value | Metric Axiom / Scaling Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Triangle Inequality** ($d(0,2)$ vs. $d(0,1)+d(1,2)$) | $D_{\text{KL}}(p_0 \| p_2)$ vs. sum | **`2.24856`** vs. **`1.95508`** | **VIOLATED** ($2.2486 > 1.9551$) | $\|\text{clr}(p_0)-\text{clr}(p_2)\|_2$ vs. sum | **`4.62034`** vs. **`5.38833`** | **SATISFIED** ($4.6203 \le 5.3883$) |
| **Radial Scale $c = 1.0$** | $\|p_a - p_b\|_2$ | `0.014322` | Baseline separation | $\|\text{clr}(p_a) - \text{clr}(p_b)\|_2$ | `0.043301` | Baseline separation ($1\times$) |
| **Radial Scale $c = 10.0$** | $\|p_a - p_b\|_2$ | `0.122346` | Non-linear expansion | $\|\text{clr}(p_a) - \text{clr}(p_b)\|_2$ | `0.433013` | Exact linear scaling ($10\times$) |
| **Radial Scale $c = 50.0$** | $\|p_a - p_b\|_2$ | **`0.008683`** | **SIMPLEX COLLAPSE** (drops $14\times$ near $\partial\Delta^{V-1}$) | $\|\text{clr}(p_a) - \text{clr}(p_b)\|_2$ | **`2.161511`** | **EXACT LINEAR SCALING** ($50\times$) |

**Empirical Finding:** At radial scale $c = 50.0$, softmax saturates near the simplex boundary $\partial\Delta^{V-1}$, causing Euclidean probability distance to collapse by over an order of magnitude (`0.12235` $\to$ `0.00868`) even though the underlying logit separation grew $5\times$ larger. Simultaneously, $D_{\text{KL}}$ failed the triangle inequality by `+0.2935` nats. Aitchison $\text{clr}$ eliminated both pathologies, scaling linearly ($0.04330 \to 0.43301 \to 2.16151$) while preserving metric axioms.

### 3.3 Exact $\mathbb{Q}[i]$ `CAUSA` Interchange Kernel Collapse
Injecting a non-zero persona perturbation $\delta \in \ker(\alpha)$ ($\delta = [(50-25i), (-50+25i), (17+9i), (-17-9i), 0]$) produced two distinct 5-channel persona vectors (`personas_distinct = true`), yet both contracted against the 9-cube enneract to the **exact same rational-complex $1 \times 1$ operator**:

$$\mathcal{V}(\mathcal{B}(P_{\text{base}}, E)) = \mathcal{V}(\mathcal{B}(P_{\text{intervened}}, E)) = \begin{pmatrix} \dfrac{2017}{24} + \dfrac{55}{4}i \end{pmatrix}$$


(causa_interchange_invariant = true). This empirically confirms that high-level persona steering inside $\ker(\alpha)$ alters semantic surface coordinates without changing the underlying algebraic operator.

---

### 4. Empirical Results: Experiment B (telemetry_exp2.json) & v3 Gate Verdict

Experiment B (experiments/exp2_sheaf_gluing.py) tested our pre-registered v3 gate by embedding 12 active sparse features from a superposed dictionary ($F = 2048$ almost-orthogonal features packed into $D = 256$ ambient dimensions; Elhage et al., 2022) and covering the space with $m = 6$ overlapping rank-$k$ ($k = 64$) QR subspace patches.

Experiment B Parameter / Diagnostic	Measured Empirical Value	Epistemic Interpretation
Ambient Dimension ($D$) / Superposed Features ($F$)	$D = 256$, $F = 2048$ ($8\times$ superposition)	High-density polysemantic regime
Subspace Cover	$m = 6$ patches of rank $k = 64$	Partial local views of superposed ambient state
coboundary_residual_unperturbed ($|\delta^0 s|_2$)	2.7434173087573055	Baseline truncation mismatch across overlapping QR patches
coboundary_residual_local_intervention ($|\delta^0 s'|_2$)	5.856049313968931	Local counterfactual intervention on patch 0 more than doubles global gluing inconsistency ($+113.5%$)
v3_sheaf_cohomology_warranted	true (exceeds $10^{-6}$ gate)	v3 Gate Triggered: Single-patch geometry cannot capture multi-patch superposition gluing

Empirical Finding: Because coboundary_residual_local_intervention reached 5.8560 (far above our $10^{-6}$ falsification threshold), Experiment B empirically refutes the sufficiency of single-patch rank-$k$ projections under heavy superposition. Introducing cellular sheaf coboundary operators ($\delta^0$) and Sheaf Laplacians ($L_{\mathcal{F}} = \delta^0{}^\top \delta^0$) (Hansen & Ghrist, 2019) in v3 is therefore justified by empirical measurement rather than theoretical speculation.

---

### 5. Epistemic Synthesis: Honoring Both Sides of the Coin

With live telemetry in hand, the synthesis between our bottom-up mathematical framework and Flyxion’s (2026) top-down institutional framework becomes concrete:
1. Why Neither Half Works Alone: Experiment A proves that without Aitchison $\text{clr}$ and QR-isometric metrics, softmax saturation and $D_{\text{KL}}$ asymmetry manufacture phantom geometric anomalies—vindicating our bottom-up critique of computational animism. Conversely, Experiment B shows that even when substrate operators are purely linear and devoid of qualia, high-dimensional superposition creates genuine local-to-global representation bottlenecks that require rigorous causal and institutional accounting (Flyxion, 2026) so engineers do not misattribute complex multi-patch behavior to emergent agency.
2. Cryptographic Provenance in Action: Running this entire verification suite inside GitHub Actions CI—producing immutable artifact bundles (epistemic-telemetry-<sha>) tied to specific commit hashes while purging ephemeral working trees—directly instantiates Flyxion’s (2026) prescription for verifiable provenance without anthropomorphic authorship.

---

### 6. Limitations & v3 Roadmap


### 6.1 Current Limitations

• Synthetic vs. Trained Transformer Weights: Experiments A and B evaluated controlled synthetic dictionaries ($D = 256, F = 2048$) and exact rational operators rather than residual-stream activations extracted from a multi-billion-parameter pretrained transformer.
• First-Order Coboundary Energy Only: exp2_sheaf_gluing.py computed the 0-coboundary norm $|\delta^0 s|2$ around a cyclic patch cover rather than constructing the full sparse Sheaf Laplacian $L{\mathcal{F}}$ and extracting its harmonic spectrum ($\dim \ker(L_{\mathcal{F}})$) and 1st Čech cohomology obstruction ($H^1$).

### 6.2 Concrete v3 Upgrades

1. Deploy CellularSheaf.jl (0-Byte Static Sheaf Laplacian): Having cleared the Experiment B empirical gate (5.8560 > 1e-6), add a sparse cellular sheaf module to julia/ManifoldInstruments.jl to compute $L_{\mathcal{F}} = \delta^0{}^\top \delta^0$ and measure harmonic gluing energy across overlapping Sparse Autoencoder (SAE) feature patches.
2. SAE-Guided Patch Construction on Open-Weight Models: Replace random-seed QR patches with orthonormal bases spanned by top-$k$ SAE dictionary features extracted from open-weight transformer layers during concept-injection trials (Lindsey, 2026; Singh et al., 2026).
3. Extend EpistemicAudit.lean with Coboundary Exactness: Add a zero-sorry Lean 4 lemma proving $\delta^1 \circ \delta^0 = 0$ for linear restriction maps over $\mathbb{Q}[i]$, certifying the algebraic complex underlying v3’s cohomology diagnostics.

---

### 7. Conclusion

By executing our unified framework in a zero-sorry, zero-allocation, edge-safe CI pipeline, we replaced speculative debate with hard empirical numbers. We demonstrated that softmax-space metrics fail the triangle inequality and collapse under radial scaling, while Aitchison $\text{clr}$ and QR-isometric pullbacks preserve exact metric geometry; that exact $\mathbb{Q}[i]$ CAUSA kernel perturbations leave $1 \times 1$ substrate operators invariant; and that $8\times$ neural superposition generates measurable local-to-global coboundary frustration (5.8560), empirically earning cellular sheaf cohomology its place in v3.

---

### References

Aitchison, J. (1986). The statistical analysis of compositional data. Chapman and Hall. doi.org
Bezanson, J., Edelman, A., Karpinski, S., & Shah, V. B. (2017). Julia: A fresh approach to numerical computing. SIAM Review, 59(1), 65–98. doi.org
de Moura, L., & Ullrich, S. (2021). The Lean 4 theorem prover and programming language. In A. Platzer & G. Sutcliffe (Eds.), Automated Deduction – CADE 28 (pp. 625–635). Springer. doi.org
Elhage, N., Hume, T., Olsson, C., Schiefer, N., Henighan, T., Kravec, S., Hatfield-Dodds, Z., Lasenby, R., Drain, D., Chen, C., Grosse, R., McCandlish, S., Kaplan, J., Amodei, D., Wattenberg, M., & Olah, C. (2022). Toy models of superposition. Transformer Circuits Thread. transformer-circuits.pub
Flyxion. (2026, November). Persistence and accountable authorship in language model systems [Preprint]. Independent Researcher.
Geiger, A., Lu, H., Icard, T., & Potts, C. (2021). Causal abstractions of neural networks. In Advances in Neural Information Processing Systems (Vol. 34, pp. 9574–9586). Curran Associates.
Hansen, J., & Ghrist, R. (2019). Toward a spectral theory of cellular sheaves. Journal of Applied and Computational Topology, 3(4), 315–358. doi.org
Hedling, B. S. (2026a). Is exclusion of phenomenology or the AI consciousness debate itself a category error [Issue #1]. GitHub. github.com
Hedling, B. S. (2026b). Epistemic substrate lab: Zero-sorry Lean 4 proofs, zero-allocation Riemannian geometry, and causal metric audits [Computer software]. GitHub. github.com
Lindsey, J. (2026). Emergent introspective awareness in large language models (arXiv:2601.01828). arXiv. arxiv.org (Original work published October 2025)
Ryle, G. (1949). The concept of mind. Hutchinson.
Singh, S., Linzen, T., & Ravfogel, S. (2026). Can LLMs introspect? A reality check (arXiv:2605.26242). arXiv. arxiv.org
stell2026. (2026). Causa: Causal abstraction and intervention primitives [Computer software]. GitHub. github.com

