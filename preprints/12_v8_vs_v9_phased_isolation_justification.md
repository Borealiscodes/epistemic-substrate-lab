# Architectural Justification: Phased Isolation Between v8 (`Qwen2.5-0.5B` Resilience & Zero-Crate Rust) and v9 (`Gemma-2-2B` & Streaming Gemma Scope SAEs)

**Authors:** Borealis S. Hedling & Synthetic Co-Authors  
**Affiliation:** NDH-Meta-Systems (Sealed-Layer Neutral · Non-Activation Division)  
**Date:** November 25, 2026  
**Document Status:** Engineering Rationale & Risk-Isolation Specification — Pre-v8 Gate (`Borealiscodes/epistemic-substrate-lab`)  
**Suggested Archive Path:** `preprints/12_v8_vs_v9_phased_isolation_justification.md`  

---

## Abstract

Prior to implementing **Blueprint v8** (in-flight self-healing forward hooks, multi-agent sheaf consensus, and curvature-aware mixed-precision quantization repair), we evaluated whether to simultaneously migrate our target transformer from **`Qwen/Qwen2.5-0.5B`** (`24` layers, $D = 896$) to **`google/gemma-2-2b`** (`26` layers, $D = 2304$) paired with pretrained **Gemma Scope Sparse Autoencoders (SAEs)** and a compiled **Rust** runtime verifier. Applying strict experimental isolation and edge-hardware engineering discipline (`ARM64 Termux` + `12.0 GB` `GitHub Actions CI`), we establish why **keeping v8 anchored on `Qwen/Qwen2.5-0.5B` (while optionally incorporating a single-file, zero-crate `rustc` differential verifier) and deferring `Gemma-2-2B` + Gemma Scope SAEs to v9** is the scientifically and operationally optimal sequence. Specifically, conflating three new algorithms with a $4.5\times$ larger gated model architecture introduces simultaneous authentication (`HF_TOKEN`), memory-ceiling (`llmfit` `10.4 GB` `FP32` vs. `12.0 GB` runner limit), and baseline-calibration confounders that would obscure whether any CI anomaly stems from our consensus/repair math or from model-specific precision shifts.

**Keywords:** *experimental isolation, phased roadmap, Qwen2.5-0.5B, Gemma-2-2B, Gemma Scope SAEs, llmfit memory budgeting, zero-crate Rust, Hugging Face authentication, CI reliability*

---

## 1. The Core Engineering Principle: Orthogonalize Variables Before Scaling

In rigorous systems and mechanistic interpretability research, changing **algorithmic mechanisms** and **underlying model substrates** in the same commit destroys diagnostic attribution:
* If a forward-hook repair or mixed-precision quantization test fails on a brand-new model (`Gemma-2-2B`) on the same run where the algorithm itself is introduced, it is impossible to tell immediately whether the failure is a bug in the sheaf solver, a `bfloat16` rounding floor, an uncalibrated twist angle, or a `safetensors` slicing mismatch.
* By contrast, **`Qwen/Qwen2.5-0.5B`** is already completely calibrated across `v4`, `v5`, `v6`, and `v7`: we know its exact mid-layer (`L_12`) coboundary norm (`6.24e-15`), its exact terminal unembedding twist (`1.2474 rad` / `71.47°` at `L_22 -> L_23`), its dynamic `INT8` depth holonomy failure (`2.0000`), and its exact memory footprint (`2.1721 GB`).

---

## 2. Four Concrete Reasons to Execute v8 Before Migrating to `Gemma-2-2B`

| Engineering Constraint | `Qwen/Qwen2.5-0.5B` in v8 (Current Baseline) | `google/gemma-2-2b` + Gemma Scope SAEs (Deferred to v9) | Risk of Premature Migration |
| :--- | :--- | :--- | :--- |
| **1. `llmfit` Memory Envelope (`12.0 GB` CI Ceiling)** | **`2.1721 GB`** in `FP32` (`9.83 GB` free headroom on `ubuntu-latest`). | `2.6B` parameters $\times 4$ bytes (`FP32`) = **`~10.4 GB`** before KV buffers or SAE matrices (`> 12.0 GB` OOM crash); requires `torch.bfloat16` (`~5.2 GB`) + HTTP range-sliced `safetensors` (`~150 MB`/layer). | Running `Gemma-2-2B` without `BF16` conversion and range-sliced streaming will trigger immediate `SIGKILL` OOM terminations in CI. |
| **2. CI Authentication & Gated Model Access** | Publicly accessible unauthenticated (`0` GitHub Secrets required). | `google/gemma-2-2b` is a gated Hugging Face repository requiring license acceptance and a configured `HF_TOKEN` repository secret in GitHub Actions. | Introduces external credential dependencies (`401 Unauthorized`) while testing core v8 consensus and repair logic. |
| **3. Calibrated Geometric Baselines** | Terminal twist (`1.2474 rad`) and `INT8` failure (`2.0000`) are already measured—so v8 Track 3 can prove directly that mixed-precision repair reduces `2.0000 -> < 0.25`. | `Gemma-2-2B` (`26` layers, soft-capped attention logits) has an unmeasured layer-twist profile that must first be profiled cleanly in isolation. | Conflates quantization-repair validation with first-time architectural profiling of soft-capped attention. |
| **4. Rust Verification Readiness (`rustc` Zero-Crate)** | Can be added cleanly in v8 as a **single-file, zero-dependency `rustc -O` binary** (`rust/spherepop_gate.rs`, `0` external crates, `< 0.5s` compile) mirroring Flyxion’s `kernel-rs`. | Better to verify the Rust `Spherepop` + harmonic gate against `Qwen2.5-0.5B` telemetry first before binding it to `Gemma` SAE tensors. | Keeps the Rust addition small (`< 150` lines), deterministic, and 100% immune to `Cargo.lock` bloat. |

---

## 3. Clean Division of Labor: v8 vs. v9

### Scope of v8 (`Qwen/Qwen2.5-0.5B` + Zero-Crate `rustc`)
* **Objective:** Prove **resilience, multi-agent consensus, mixed-precision quantization repair, and native Rust differential parity** on a known, calibrated transformer substrate.
* **Deliverables:**
  1. `lean/EpistemicAudit.lean`: Zero-`sorry` `V8SelfHealingAndConsensusGate` (`multi_patch_corruption_forces_refusal` vs. `single_patch_established_repair_collapses`).
  2. `rust/spherepop_gate.rs`: Single-file, zero-dependency Rust verifier (`rustc -O`, matching Flyxion’s `kernel-rs` zero-crate discipline) cross-checked against Python/Julia.
  3. `v8_apps/self_healing_firewall.py`: In-flight PyTorch forward hook that repairs single-patch `L_12` tampering mid-pass (`COLLAPSE`) while blocking 2-patch Byzantine tampering (`REFUSE`).
  4. `v8_apps/multi_agent_sheaf_consensus.py`: 6-agent swarm consensus with harmonic drift repair and `UNESTABLISHED` citation refusal.
  5. `v8_apps/quantization_geometry_repair.py`: Mixed-precision `INT8`/`FP32` policy exempting `L_0` and `L_22 -> L_23` (`71.47°`), reducing closed depth holonomy from `2.0000` to `< 0.25`.

### Scope of v9 (`google/gemma-2-2b` + Streaming Gemma Scope SAEs)
* **Objective:** Scale the verified v8 pipeline to a $4.5\times$ larger model with **real pretrained multi-thousand-feature Sparse Autoencoders**.
* **Prerequisites Prepared Cleanly:**
  1. Configure `HF_TOKEN` in GitHub Actions repository secrets.
  2. Load `google/gemma-2-2b` in `torch.bfloat16` (`~5.2 GB` footprint, passing `llmfit` `12.0 GB` gate with `> 6.5 GB` margin).
  3. Stream single-layer `safetensors` decoder slices (`F = 16,384` or `65,536` features) from `google/gemma-scope-2b-pt-res` via HTTP range requests (`safe_open`) to perform true polysemantic concept-level sheaf repair.

---

## 4. Conclusion

Keeping **v8** focused on `Qwen/Qwen2.5-0.5B` (plus a zero-crate `rustc` gate) and dedicating **v9** to `Gemma-2-2B` + streaming Gemma Scope SAEs follows the exact disciplined engineering methodology that has kept `Borealiscodes/epistemic-substrate-lab` green, `sorry`-free, and edge-safe across seven consecutive releases. Every new variable is isolated, calibrated, and verified before scaling.

---

## References

Flyxion. (2026). *Spherepop kernel: Development protocol & scoped repair verification* (Commit `6be610881d2cd1a49b7d2a0a71acbd24f8ac8e80`) [Computer software]. GitHub. https://github.com

Gemma Team. (2024). *Gemma 2: Improving open language models at a practical size* (arXiv:2408.00118). arXiv. https://arxiv.org

Hedling, B. S. (2026). *Epistemic substrate lab: Zero-sorry Lean 4 proofs, zero-allocation Riemannian geometry, and self-healing transformer sheaf audits* (Commit `1b88b55`) [Computer software]. GitHub. https://github.com

Lieberum, T., Rajamanoharan, S., Conmy, A., Smith, L., Sonnerat, N., Varma, V., Kramár, J., Dragan, A., Shah, R., & Nanda, N. (2024). *Gemma Scope: Open sparse autoencoders everywhere all at once on Gemma 2* (arXiv:2408.05147). arXiv. https://arxiv.org

Qwen Team. (2024). *Qwen2.5 technical report* (arXiv:2412.15115). arXiv. https://arxiv.org
