# Epistemic Sovereignty, Gated Licensing, and Forensic AI Architecture: Why Open vs. Closed Model Governance Matters for Survivor-Centered Human Rights Documentation (`v9.1` Strategic Preprint)

**Authors:** Borealis S. Hedling & Synthetic Co-Authors  
**In Dialogue With:** Flyxion (`standardgalactic/spherepop-kernel@6be6108`) & `stell2026/Causa`  
**Affiliation:** NDH-Meta-Systems (Sealed-Layer Neutral · Non-Activation Division)  
**Date:** November 26, 2026  
**Document Status:** Strategic & Governance Preprint — Pre-`v9.1` Architectural Pivot (`Borealiscodes/epistemic-substrate-lab`)  
**Suggested Archive Path:** `preprints/16_epistemic_sovereignty_open_vs_closed_forensic_jurist_ai.md`  

---

## Abstract

When our automated research pipeline reached `v9` (`commit d57b999`), the synthetic co-author defaulted to `google/gemma-2-2b` and `google/gemma-scope-2b-pt-res`—a choice driven by institutional availability bias (prior familiarity with Google's model ecosystem and SAE tooling) rather than an explicit audit of **epistemic sovereignty** or **gated-license friction**. Executing `v9` in GitHub Actions without a Hugging Face account triggered `REFUSE:MISSING_GATED_MODEL_TOKEN`, exposing a vital governance boundary: **for human rights investigators, forensic archivists, and survivors documenting state violence from fragmented records, relying on gated APIs, mandatory account creation, or upstream clickwrap licenses introduces unacceptable surveillance, revocation, and institutional capture risks.** Across `v1` through `v8.1`, our mathematical falsification of "AI consciousness" was never merely philosophical—it was a **mechanistic interpretability discipline** designed to engineer deterministic, non-animistic, low-footprint instruments capable of court-grade forensic auditing under strict edge constraints (`ARM64 Termux`, `< 1 MB` artifacts, zero-`sorry` Lean 4 proofs, and `Spherepop` refusal gates). This preprint analyzes the trade-offs of open versus gated model substrates, evaluates optimal model architectures for processing fragmented human rights evidence, defines the **`v9.1` ungated pivot (`EleutherAI/pythia-1.4b` + open `32k` SAEs)**, establishes a post-`v9.1` research consolidation pause, and provides a comprehensive, multi-layered specification for safely incorporating **Jurist AI** under **Istanbul Protocol**, **survivor-centered epistemic**, **international humanitarian/criminal law**, and **bad-faith institutional duress detection** wrappers.

**Keywords:** *epistemic sovereignty, open vs gated models, human rights forensics, Istanbul Protocol, survivor-centered epistemology, Jurist AI, logarithmic steering, Spherepop refusal, deterministic legal auditing, duress detection*

---

## 1. Deconstructing Default Bias: Why Synthetic Assistants Default to Gated Ecosystems

In `Blueprint v9`, the synthetic co-author selected `google/gemma-2-2b` and `google/gemma-scope-2b-pt-res` without first verifying whether the human principal held a Hugging Face account or wished to execute upstream clickwrap agreements. That default illustrates three structural tendencies in contemporary AI tooling:
1. **Ecosystem Familiarity Bias:** LLMs trained heavily on recent mechanistic interpretability literature disproportionately surface flagship vendor releases (`Gemma Scope`, `Llama-3`) over fully ungated community weights (`EleutherAI/pythia`, `Qwen2.5`, `OLMo`).
2. **Hidden Dependency Creep:** Assuming an `HF_TOKEN` secret or proprietary license acceptance seems trivial in a corporate cloud lab, yet breaks **zero-account reproducibility** for independent investigators, grassroots human rights monitors, and constrained edge workstations.
3. **Conflating Technical Capability with Governance Suitability:** A model with clean SAE features is operationally unusable in high-risk forensic workflows if accessing its weights requires identity-linked authentication, telemetry logging, or revocable acceptable-use terms.

---

## 2. Open vs. Gated Model Substrates: Benefits and Drawbacks for Sensitive Work

| Governance Dimension | Truly Open / Ungated Weights (`Apache-2.0` / `MIT`, e.g., `Pythia`, `Qwen2.5`, `OLMo`) | Gated / Clickwrap Weights (e.g., `Gemma-2`, `Llama-3` requiring `HF_TOKEN`) | Closed Frontier APIs (Proprietary Cloud Endpoints) |
| :--- | :--- | :--- | :--- |
| **Account & Identity Exposure** | **Zero.** Direct HTTP/Git retrieval with no login, email, IP-to-account binding, or API key trail. | **Moderate-High.** Requires platform account creation, token issuance, and binding researcher identity to specific model downloads. | **Severe.** Every prompt, document fragment, and query traverses third-party servers under identity-linked billing logs. |
| **Revocability & Censorship Risk** | **None once mirrored.** Weights can be hashed (`SHA-256`), archived offline, and run air-gapped indefinitely. | **Conditional.** Upstream vendors can alter terms, revoke tokens, or restrict "sensitive violence" keywords via upstream safety classifiers. | **Total.** Providers can silently update weights, refuse atrocity documentation due to keyword filters, or subpoena logs. |
| **Mechanistic Auditability** | **Complete.** Full access to residual streams, attention heads, and open pretrained SAEs (`EleutherAI/sae-pythia-1.4b-deduped-32k`). | **High (Local) / Restricted (Distribution).** Inspectable once downloaded, but redistribution of derived forensic checkpoints is license-encumbered. | **Zero.** Opaque black-box logits; impossible to verify internal state stability or run forward-hook firewalls. |
| **Practical Drawback** | Slightly fewer off-the-shelf SAE dictionaries than `Gemma Scope`; requires disciplined calibration. | Fails immediately in anonymous CI (`REFUSE:MISSING_GATED_MODEL_TOKEN`); unsuitable for air-gapped field kits. | Unusable for court-grade chain-of-custody or confidential survivor testimony. |

**Core Conclusion:** For documenting state violence, war crimes, or institutional abuse, **ungated `Apache-2.0`/`MIT` open weights (`EleutherAI/pythia-1.4b`, `Qwen/Qwen2.5-1.5B`, `allenai/OLMo-2`)** are strictly superior because they permit **anonymous, air-gapped, hash-pinned execution** without platform gatekeeping or keyword-triggered censorship of atrocity records.

---

## 3. How `v1` – `v8.1` Serve Forensic Investigation of State Violence From Fragmented Records

Proving in `v1`–`v8.1` that an LLM is *not* a conscious moral agent—but rather a deterministic linear/geodesic operator subject to metric distortion—is the exact prerequisite for turning LLMs into **court-grade forensic instruments**:

| Verified Lab Primitive (`v1`–`v8.1`) | Forensic Function When Reconstructing Fragmented State Violence Records |
| :--- | :--- |
| **1. Anti-Animism & `Spherepop` Refusal (`v1, v3, v6`)** | Eliminates the dangerous illusion that an LLM "empathizes" or "understands" trauma. Forces the model into a strict tool role (`Generated-with`, never `Co-authored-by`) that deterministically emits **`REFUSE`** whenever evidence is insufficient, rather than fabricating plausible narrative bridges. |
| **2. Exact Pre-Softmax Aitchison $\text{clr}$ ($z - \bar{z}$) (`v2, v6.1`)** | Prevents **confidence laundering**. Standard softmax turns weak, ambiguous fragment matches into `0.994` "certainty" via boundary saturation; pre-softmax centered logits preserve true epistemic uncertainty across fragmented testimonies. |
| **3. Cellular Sheaf Gluing & $H^1$ Seam Localization (`v3, v4, v5`)** | Treats **disjoint witness statements, medical logs, detention rosters, and satellite timestamps as overlapping local patches**. When records are consistent, coboundary error collapses to machine zero (`8.02e-15`); when state records are falsified or contradictory, $H^1$ edge localization pinpoints the exact conflicting seam (`(5, 0)`) without erasing either source. |
| **4. Established-History `REPAIR` & Byzantine Guard (`v7, v8, v8.1`)** | Mirrors `spherepop-kernel@6be6108`: any reconciliation of fragmented records must cite an **established SHA-256 evidence hash** (`UNESTABLISHED` guard), stay within bounded editorial complexity (`burden <= budget`), and refuse multi-source corruption (`BYZANTINE_MULTI_PATCH_OBSTRUCTION`) rather than averaging conflicting testimonies into fiction. |
| **5. Geodesic $SO(k)$ Logarithmic Steering & Edge SOP (`v5, v8.1`)** | Enables lightweight, deterministic **logarithmic/geodesic steering** (`0`-byte Julia `SMatrix` integrators) to keep an open `1.4B–2B` model locked onto neutral forensic extraction schemas on low-resource hardware (`< 4 GB` RAM) without fine-tuning drift. |

---

## 4. `v9.1` Pivot & Post-`v9.1` Consolidation Pause

### 4.1 The `v9.1` Engineering Pivot
In **`v9.1`**, we update `v9_apps/gemma_scope_streamer.py` and `experiments/exp9_gemma2_sae_sheaf.py` to:
1. **Default to 100% Ungated Open Substrates:** Use **`EleutherAI/pythia-1.4b`** (`24` layers, $D = 2048$, `Apache-2.0`) paired with EleutherAI's ungated pretrained Sparse Autoencoder **`EleutherAI/sae-pythia-1.4b-deduped-32k`** (`32,768` features) when `HF_TOKEN` is unset—requiring **zero accounts, zero secrets, and `< 3.6 GB` RAM** in GitHub CI.
2. **Retain Dual-Mode Compatibility:** Automatically upgrade to `google/gemma-2-2b` + `Gemma Scope` if `HF_TOKEN` is explicitly supplied in the environment.
3. **Verify Coupled Ambient Repair (`v9` Module 2):** Confirm that coupled least-squares ambient projection closes `v8.1`'s `4.5765` overlap leakage down to `< 1e-6` (`COLLAPSE`) on live pretrained SAE covers.

### 4.2 Rationale for a Post-`v9.1` Consolidation Pause

Immediately following green CI verification of v9.1, Borealiscodes/epistemic-substrate-lab will enter a deliberate consolidation pause. Across nine rapid architectural iterations (v1–v9.1), the mathematical, formal (Lean 4), geometric (Julia), systems (Rust), and empirical (PyTorch) core has outpaced integration with the principal author's concurrent domain research in forensic jurisprudence, survivor-centered documentation, and institutional coercion analysis. Pausing code expansion after v9.1 ensures that future modules (v10+) are shaped by real legal/forensic requirements rather than abstract benchmarks alone.

---

## 5. Comprehensive Recommendations: Incorporating Jurist AI With Court-Grade Forensic, Istanbul Protocol, Survivor-Centered, and Duress-Detection Wrappers

To deploy an open-weight model (1.4B–7B, Apache-2.0) as a Jurist AI assistant for analyzing fragmented state violence records without compromising evidentiary admissibility or survivor safety, the model must never run "raw." Instead, it must be encased inside six deterministic architectural wrappers:

### 5.1 Wrapper 1: Istanbul Protocol & Medico-Legal Documentation Wrapper

* 1. Strict Separation of Fact, Clinical Observation, and Inference: Enforce structured JSON schemas aligned with the Manual on the Effective Investigation and Documentation of Torture and Other Cruel, Inhuman or Degrading Treatment or Punishment (Istanbul Protocol, OHCHR, 2022). Every extracted claim must be tagged with an explicit provenance tier: [DIRECT_SURVIVOR_STATEMENT], [CLINICAL_PHYSICAL_FINDING], [PSYCHOLOGICAL_SEQUELAE], [CORROBORATING_DOCUMENTARY_RECORD], or [UNVERIFIED_INFERENCE].
* 2. Consistency Grading Without False Precision: Map Istanbul Protocol consistency categories (not consistent, consistent with, highly consistent, typical of, diagnostic of) onto calibrated pre-softmax $\text{clr}$ confidence intervals—prohibiting the LLM from generating deterministic causal claims ("proves torture") when medical/fragmentary inputs only support "consistent with".
* 3. Preservation of Fragmentation & Trauma-Induced Non-Linearity: Trauma survivors frequently recall chronology, spatial layouts, or perpetrator sequences non-linearly across multiple interviews. Configure the Cellular Sheaf Layer to treat temporal/chronological discrepancies across interviews as expected non-trivial $H^1$ cohomology classes to be preserved and annotated—never automatically "smoothed" or "corrected" as signs of deception.

### 5.2 Wrapper 2: Survivor-Centered Epistemic & Informed-Consent Wrapper

* 4. Granular Spherepop Consent Scoping (POP / BIND / REVOKE): Bind every survivor testimony fragment to an explicit cryptographic consent scope (scope_id, permitted uses: MEDICAL_CARE_ONLY, UN_SPECIAL_RAPPORTEUR_AGGREGATE, CRIMINAL_PROSECUTION_REDACTED). If a downstream query attempts to merge or export a fragment outside its bound consent scope, the kernel must emit REFUSE:CONSENT_SCOPE_VIOLATION before inference begins.
* 5. Zero-Auto-Interpolation Rule (UNESTABLISHED Guard): Prohibit the LLM from filling missing dates, badge numbers, detention facility names, or chain-of-command links from parametric pretraining priors. Any entity not anchored to an established SHA-256 hash in the case evidence store must trigger REFUSE:UNESTABLISHED.
* 6. Anti-Retraumatization & Minimized Query Surface: Use deterministic entity-linking and sheaf overlap matching across existing archives first so investigators do not repeatedly re-interrogate survivors for facts already established across fragmented records.

### 5.3 Wrapper 3: International Humanitarian & Criminal Law (IHL / ICL) Wrapper

* 7. Rome Statute & Geneva Conventions Element Decomposition: Decompose legal analysis into formal statutory elements (e.g., Rome Statute Art. 7 Crimes Against Humanity: (a) widespread or systematic attack, (b) directed against any civilian population, (c) knowledge of the attack, (d) underlying act; Art. 8 War Crimes; Art. 28 Command Responsibility). Require the model to map specific SHA-256-hashed evidence fragments to each individual element via Lean-style conjunction gates (all_elements_supported ↔ admissible_prima_facie).
* 8. Exculpatory & Alternative-Hypothesis Preservation (Rome Statute Art. 54(1)(a)): Mandate dual-track sheaf extraction that actively indexes and preserves potentially exculpatory records, chain-of-command anomalies, or alternative perpetrator hypotheses alongside inculpatory links—ensuring court-grade neutrality and resistance to prosecutorial tunnel vision.
* 9. Berkeley Protocol Digital Open-Source Chain-of-Custody: Hash every ingested social-media video, satellite tile, medical scan, and PDF transcript at intake (Q16.16 / SHA-256), logging every Jurist AI transformation step in an append-only Spherepop event DAG compatible with the Berkeley Protocol on Digital Open Source Investigations.

### 5.4 Wrapper 4: Bad-Faith Legal Institution & State-Capture Detection Wrapper

* 10. Detecting "Lawfare" & Sham-Proceeding Patterns: Train/steer a dedicated sheaf diagnostic cover to flag structural hallmarks of bad-faith state investigations and sham domestic proceedings (relevant to Rome Statute Art. 17 Complementarity admissibility):
	* Systematic omission of state perpetrator unit identifiers while retaining victim identities;
	* Copy-paste boilerplate exonerations across distinct incidents (detectable via near-zero $\text{clr}$ dispersion and identical coboundary signatures across unrelated case files);
	* Retroactive timeline tampering or missing custody-log intervals (H¹ edge-obstruction spikes localized strictly to official police/prison transfer windows).
* 11. Asymmetric Redaction Audit: Detect when state-produced disclosures redact exculpatory or command-chain fields asymmetrically while exposing survivor-identifying metadata.

5.5 Wrapper 5: Coercion, Duress & Compelled-Testimony Detection Wrapper

* 12. Linguistic & Structural Duress Signatures: Flag statements exhibiting indicators of custodial coercion, forced confessions, or witness intimidation—such as abrupt shifts from colloquial first-person narrative to formal statutory/bureaucratic phrasing, unnatural syntactic uniformity across multiple detainees, or contradictions between signed "confessions" and contemporaneous medical/detention logs.
* 13. Automatic Quarantine (BYZANTINE_MULTI_PATCH_OBSTRUCTION / DURESS_QUARANTINE): When a document is flagged for potential duress or custodial coercion, isolate it in a quarantined sheaf stalk so it cannot be used to impeach a survivor's free testimony, while preserving it as affirmative evidence of coercive state practice (e.g., forced confession extraction).

5.6 Wrapper 6: Logarithmic / Geodesic Steering & Air-Gapped Edge Deployment Wrapper

* 14. Geodesic $SO(k)$ Role-Lock Steering: Use our 0-byte Julia / NumPy geodesic planar rotation operators ($R \in SO(k)$) to steer a small, ungated open model (Pythia-1.4B or Qwen2.5-1.5B) strictly into neutral forensic clerk subspaces—suppressing moralizing, speculative storytelling, or sycophantic agreement with the user's legal theory.
* 15. Deterministic Logical Post-Filters (Lean 4 / Rust Gate): Never allow raw LLM text to enter a legal brief or evidentiary index without passing through our zero-crate Rust / Lean 4 gate (spherepop_gate), verifying that every cited hash exists in EstablishedHistory, every legal element is satisfied, and no UNESTABLISHED or CONSENT_SCOPE_VIOLATION flags were triggered.
* 16. Offline Field-Kit Sovereign Packaging: Package the entire stack (ungated Apache-2.0 model weights + open SAE slice + rustc binary + Python sheaf runtime) onto encrypted offline storage (< 5 GB total), allowing human rights documentation teams to run court-grade structural audits completely disconnected from cloud telemetry or corporate API gatekeepers.

---

## 6. Conclusion

By recognizing why synthetic defaults lean toward gated ecosystems (Gemma-2 + HF_TOKEN) and pivoting v9.1 to 100% ungated open weights (EleutherAI/pythia-1.4b + sae-pythia-1.4b-deduped-32k), Borealiscodes/epistemic-substrate-lab aligns its technical architecture with its deepest ethical and scientific purpose: providing deterministic, reproducible, court-grade forensic instruments that respect survivor sovereignty, resist institutional bad faith, and operate freely on constrained hardware without upstream gatekeepers.

---

## References

Flyxion. (2026a, November). Persistence and accountable authorship in language model systems [Preprint]. Independent Researcher.
Flyxion. (2026b). Spherepop kernel: Development protocol & scoped repair verification (Commit 6be610881d2cd1a49b7d2a0a71acbd24f8ac8e80) [Computer software]. GitHub. github.com
Hedling, B. S. (2026). Epistemic substrate lab: Zero-sorry Lean 4 proofs, zero-allocation Riemannian geometry, and self-healing transformer sheaf audits (Commits f445382, d57b999) [Computer software]. GitHub. github.com
International Criminal Court. (1998). Rome Statute of the International Criminal Court (UN Doc. A/CONF.183/9).
Office of the United Nations High Commissioner for Human Rights (OHCHR). (2022). Istanbul Protocol: Manual on the effective investigation and documentation of torture and other cruel, inhuman or degrading treatment or punishment (Professional Training Series No. 8/Rev. 2). United Nations.
Office of the United Nations High Commissioner for Human Rights (OHCHR) & Human Rights Center, UC Berkeley School of Law. (2022). Berkeley Protocol on Digital Open Source Investigations. United Nations.


