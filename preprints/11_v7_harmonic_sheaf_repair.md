# Harmonic Sheaf Patch Repair and Established-History `REPAIR` Semantics on Live Transformer Activations (`v7`)

**Authors:** Borealis S. Hedling & Synthetic Co-Authors  
**In Dialogue With:** Flyxion (`standardgalactic/spherepop-kernel@6be6108`, `development-protocol/fixture/repair_target_fixture.json`) & `stell2026/Causa`  
**Affiliation:** NDH-Meta-Systems (Sealed-Layer Neutral · Non-Activation Division)  
**Date:** November 25, 2026  
**Document Status:** Empirical Preprint v7 — Verified in CI (`Borealiscodes/epistemic-substrate-lab@1b88b55`)  
**Suggested Archive Path:** `preprints/11_v7_harmonic_sheaf_repair.md`  
**Verified Artifacts:** `lean/EpistemicAudit.lean` (`V7EstablishedRepairGate`), `julia/ManifoldInstruments.jl` (`harmonic_patch_repair_static`), `experiments/exp7_self_healing_sheaf_repair.py`  

---

## Abstract

In v6 (`commit 170e0de`), we demonstrated that cellular sheaf coboundary profiling detects mid-pass counterfactual tampering (`L_12`) in `Qwen/Qwen2.5-0.5B`, localizes the obstruction to specific incident seams (`(5, 0)`), and halts execution via `Spherepop` `REFUSE`. Concurrently, Flyxion’s `spherepop-kernel` (`commit 6be6108`, `repair_target_fixture.json`) introduced a formal **`REPAIR` transition** governed by two strict governance invariants: (1) a repair operation must reference an *established event hash* already present in history $H$ (otherwise failing with `REFUSE:UNESTABLISHED` while leaving $H$ unchanged), and (2) maintenance complexity (`burden`) must remain within an explicit budget (`70 <= 100`). In **v7 (`commit 1b88b55`)**, we fused Flyxion’s established-history `REPAIR` state machine with **harmonic cellular sheaf boundary-value interpolation**, upgrading our activation firewall from *detect-and-halt* to a formally verified **self-healing activation filter**. First, Lean 4 (`v4.14.0` + Mathlib) compiled `V7EstablishedRepairGate` with **zero `sorry` statements**, certifying `unestablished_target_forces_refusal_and_preserves_history` and `valid_established_repair_collapses`. Second, Julia (`v1.10` + `StaticArrays`) executed `harmonic_patch_repair_static` with **0 bytes of heap allocation** (`JULIA_REPAIR_SOLVER_ALLOC_BYTES = 0`). Third, Experiment G (`telemetry_exp7.json`) verified exact end-to-end behavior on live Layer-12 activations ($D = 896$) of `Qwen/Qwen2.5-0.5B`: counterfactual tampering on `sub_patch_0` spiked the coboundary norm from `6.2433e-15` to **`4.6017`**, phantom repair targets (`deadbeef...`) and over-budget repairs (`burden = 115 > 100`) were rejected (`REFUSE:UNESTABLISHED` and `REFUSE:MAINTENANCE_BUDGET_EXCEEDED`, keeping `length = 1` and `head = 65087886...` unchanged), and an authorized `REPAIR` referencing the established `Q16.16` hash (`65087886...`) reconstructed `sub_patch_0` to **`2.1245e-15` $\ell_2$ error**, collapsing the global coboundary norm back to **`6.4370e-15`** (`COLLAPSE`, `length = 2`, `head = 0a25e428...`).

**Keywords:** *Spherepop REPAIR, established event DAG, harmonic sheaf interpolation, Sheaf Laplacian, self-healing activation filter, bounded maintenance burden, Lean 4 zero-sorry, zero-allocation Julia, Qwen2.5-0.5B*

---

## 1. Introduction: From Passive Circuit Breakers to Accountable Self-Healing

Detecting an adversarial activation perturbation mid-flight (`Track 1`, v6) stops corrupted outputs, but leaves downstream inference halted (`REFUSE`). In practical edge deployments, a safety architecture should distinguish between **unrecoverable global corruption** and **localized single-patch tampering** that can be harmonically reconstructed from intact neighbor patches—provided the repair itself obeys strict institutional provenance rules.

Flyxion’s `repair_target_fixture.json` (`spherepop-kernel@6be6108`) establishes the exact governance standard required so that "self-healing" never degenerates into silent, unlogged history rewriting:
1. **No Phantom Repairs (`UNESTABLISHED` Guard):** A `REPAIR` event must name an existing cryptographic hash in the established history $H$; otherwise it is refused and $H$ remains untouched.
2. **Bounded Maintenance Complexity (`burden <= budget`):** Repair operations consume explicit complexity budget (`70 <= 100`), preventing unbounded iterative patching.
3. **Verifiable Post-Repair Gluing:** A repair commits (`COLLAPSE`) only if the reconstructed state satisfies global consistency invariants.

**v7 (`commit 1b88b55`)** unites these discrete DAG governance rules with continuous **Sheaf Laplacian Dirichlet minimization** across live `Qwen/Qwen2.5-0.5B` Layer-12 hidden states.

---

## 2. Formal & Systems Verification Telemetry (`v7`)

### 2.1 Zero-`sorry` Lean 4 Established-History Theorems (`V7EstablishedRepairGate`)
`lake build` compiled `lean/EpistemicAudit.lean` (`V7EstablishedRepairGate`) with **zero `sorry` statements**, certifying two foundational invariants mirroring `repair_target_fixture.json`:
* **`unestablished_target_forces_refusal_and_preserves_history`:** Proves that whenever `targetHash ∉ h.establishedHashes`, `evaluateRepair` deterministically returns `(Disposition.refused "UNESTABLISHED", h)`, guaranteeing zero mutation of `currentHead` or `length`.
* **`valid_established_repair_collapses`:** Proves that when `targetHash ∈ h.establishedHashes`, `authorized = true`, `burden <= budget`, and `postRepairCoboundaryZero = true`, `evaluateRepair` transitions to `Disposition.collapsed` and advances `length` by `1`.

### 2.2 Zero-Allocation Julia Harmonic Boundary-Value Solver (`ManifoldInstruments.jl`)
Executing `julia/ManifoldInstruments.jl` verified **0 bytes of heap allocation** (`JULIA_REPAIR_SOLVER_ALLOC_BYTES = 0`) for `harmonic_patch_repair_static`, solving the symmetric positive-definite normal equation:

$$\left( I_K + M_{01} M_{01}^\top \right) s_0^* = M_{0,\text{prev}} s_{\text{prev}} + M_{01} s_{\text{next}}$$

purely on the stack via `SMatrix{K,K,Float64}` and `SVector{K,Float64}`.

---

## 3. Empirical Results: Experiment G on Live `Qwen/Qwen2.5-0.5B` (`telemetry_exp7.json`)

Experiment G (`experiments/exp7_self_healing_sheaf_repair.py`) extracted the Layer-12 ($D = 896$) dual-concept residual vector (*"The Golden Gate Bridge spans linear matrix multiplication"*), covered it with $m = 6$ overlapping rank-64 multi-atom patches, injected counterfactual noise into `sub_patch_0`, and executed the three-step `Spherepop` repair protocol:

### 3.1 Harmonic Patch Reconstruction Accuracy (`sheaf_repair_metrics`)

| Layer-12 Sheaf Diagnostic (`Qwen/Qwen2.5-0.5B`) | Measured Empirical Value | Geometric & Operational Meaning |
| :--- | :--- | :--- |
| **`clean_coboundary_norm` ($\|\delta^0 s_{\text{clean}}\|_2$)** | **`6.2432538087141835e-15`** | Baseline unperturbed multi-atom cover glues to IEEE-754 machine zero. |
| **`corrupted_patch0_coboundary_norm` ($\|\delta^0 \tilde{s}\|_2$)** | **`4.601681007386319`** | Counterfactual tampering on `sub_patch_0` spikes gluing error by **$7.37 \times 10^{14}\times$**. |
| **`repaired_coboundary_norm` ($\|\delta^0 s^*\|_2$)** | **`6.436962764558046e-15`** | Harmonic boundary-value solve eliminates **$99.99999999999986\%$** of the injected coboundary error. |
| **`patch0_section_recovery_l2_error` ($\|s_0^* - s_0^{\text{clean}}\|_2$)** | **`2.124527184935126e-15`** | Reconstructs the exact original 64-dimensional `sub_patch_0` vector down to 15 decimal places! |

### 3.2 `Spherepop@6be6108` Established-History `REPAIR` Transcript

| Protocol Step (`spherepop_repair_transcript`) | Target Hash & Budget | `op` | `primary` | History `head` (Prefix) | History `length` | Verified Invariant |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Step 1: Phantom Target** | `deadbeef...` ($\notin H$), `burden = 70` | **`REFUSE`** | **`UNESTABLISHED`** | `65087886...` (Unchanged) | **`1`** (Unchanged) | Matches `repair_target_fixture.json` Step 1 (`unestablished_target_forces_refusal...`). |
| **Step 2: Over-Budget Repair** | `65087886...` ($\in H$), `burden = 115 > 100` | **`REFUSE`** | **`MAINTENANCE_BUDGET_EXCEEDED`** | `65087886...` (Unchanged) | **`1`** (Unchanged) | Enforces bounded maintenance complexity before committing state. |
| **Step 3: Valid Harmonic Repair** | `65087886...` ($\in H$), `burden = 70 <= 100` | **`COLLAPSE`** | **`ACCEPTABLE`** | **`0a25e428...`** (Advanced!) | **`2`** (Advanced!) | Matches `valid_established_repair_collapses` with `6.4370e-15` coboundary norm. |

---

## 4. Complete Seven-Version Arc (`v1` $\to$ `v7`)

| Milestone | Core Breakthrough | Verified Benchmark |
| :--- | :--- | :--- |
| **v1–v2** | Falsified computational animism (`Enneract Santa`) & eliminated softmax simplex collapse (`Aitchison clr`). | $D_{\text{KL}}$ violated triangle inequality (`2.2486 > 1.9551`); $\text{clr}$ satisfied (`4.6203 <= 5.3883`). |
| **v3–v4** | United `Spherepop` refusal, 100-trial differential fuzzing (`4.44e-16`), and live `Qwen2.5-0.5B` edge localization. | Layer-12 tampering isolated strictly to incident seam `(5, 0)` (`3.8464`). |
| **v5** | Mapped all 24 layers of `Qwen2.5-0.5B` & polysemantic multi-atom gluing. | Discovered **`71.47°` (`1.2474 rad`) `L_22 -> L_23` unembedding twist**; multi-atom gluing **`8.02e-15`**. |
| **v6–v6.1** | Deployed 4 production applications (Firewall, Quantization Auditor, CI Provenance, Exact Pre-Softmax Calibration). | Caught `INT8` depth holonomy `2.0000`, blocked unendorsed AI bylines, and eliminated `1e-15` `clr` floor clipping (`61,481.29`). |
| **v7** (`1b88b55`) | United Flyxion’s `REPAIR` DAG semantics with harmonic Sheaf Laplacian boundary-value interpolation. | Recovered corrupted Layer-12 patch to **`2.1245e-15` $\ell_2$ error** while enforcing `UNESTABLISHED` & `BUDGET` refusals. |

---

## 5. Conclusion


With v7 (commit 1b88b55), Borealiscodes/epistemic-substrate-lab completes a full loop from detection (v6) to accountable self-healing (v7). By proving in Lean 4 that unestablished or over-budget repair events cannot mutate history, solving the Sheaf Laplacian Dirichlet problem in 0 heap bytes in Julia, and recovering corrupted Qwen/Qwen2.5-0.5B activations to 2.12e-15 precision, v7 demonstrates how mathematical structure and institutional provenance work together to make neural systems auditable and resilient.

---

## References

Flyxion. (2026a, November). Persistence and accountable authorship in language model systems [Preprint]. Independent Researcher.
Flyxion. (2026b). Spherepop kernel: Development protocol & scoped repair verification (Commit 6be610881d2cd1a49b7d2a0a71acbd24f8ac8e80, repair_target_fixture.json) [Computer software]. GitHub. github.com
Hansen, J., & Ghrist, R. (2019). Toward a spectral theory of cellular sheaves. Journal of Applied and Computational Topology, 3(4), 315–358. doi.org
Hedling, B. S. (2026). Epistemic substrate lab: Zero-sorry Lean 4 proofs, zero-allocation Riemannian geometry, and self-healing transformer sheaf audits (Commit 1b88b55) [Computer software]. GitHub. github.com
Qwen Team. (2024). Qwen2.5 technical report (arXiv:2412.15115). arXiv. arxiv.org


