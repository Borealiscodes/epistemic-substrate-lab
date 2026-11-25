import Mathlib

namespace EpistemicAudit

def pullbackDist {α E : Type*} [SeminormedAddCommGroup E] (f : α → E) (x y : α) : ℝ :=
  ‖f x - f y‖

theorem pullbackDist_nonneg {α E : Type*} [SeminormedAddCommGroup E]
    (f : α → E) (x y : α) : 0 ≤ pullbackDist f x y :=
  norm_nonneg _

theorem pullbackDist_symm {α E : Type*} [SeminormedAddCommGroup E]
    (f : α → E) (x y : α) : pullbackDist f x y = pullbackDist f y x :=
  norm_sub_rev _ _

theorem pullbackDist_triangle {α E : Type*} [SeminormedAddCommGroup E]
    (f : α → E) (x y z : α) :
    pullbackDist f x z ≤ pullbackDist f x y + pullbackDist f y z := by
  unfold pullbackDist
  have h : f x - f z = (f x - f y) + (f y - f z) :=
    (sub_add_sub_cancel (f x) (f y) (f z)).symm
  rw [h]
  exact norm_add_le (f x - f y) (f y - f z)

structure GaussianRat where
  re : ℚ
  im : ℚ
  deriving DecidableEq

def GaussianRat.add (a b : GaussianRat) : GaussianRat :=
  ⟨a.re + b.re, a.im + b.im⟩

def GaussianRat.mul (a b : GaussianRat) : GaussianRat :=
  ⟨a.re * b.re - a.im * b.im, a.re * b.im + a.im * b.re⟩

def GaussianRat.zero : GaussianRat := ⟨0, 0⟩

abbrev Persona5 := Fin 5 → GaussianRat
abbrev Enneract9 := Fin 9 → GaussianRat
abbrev PureOperator1x1 := Matrix (Fin 1) (Fin 1) GaussianRat

def sumChannels {n : ℕ} (v : Fin n → GaussianRat) : GaussianRat :=
  (List.ofFn v).foldl GaussianRat.add GaussianRat.zero

def bindEnneract (P : Persona5) (E : Enneract9) : PureOperator1x1 :=
  fun _ _ => GaussianRat.mul (sumChannels P) (sumChannels E)

theorem santa_collapse_is_1x1_pure (P : Persona5) (E : Enneract9) :
    ∃ z : GaussianRat, bindEnneract P E = fun _ _ => z :=
  ⟨GaussianRat.mul (sumChannels P) (sumChannels E), rfl⟩

theorem causa_interchange_kernel_invariant
    {R M N : Type*} [Ring R] [AddCommGroup M] [Module R M]
    [AddCommGroup N] [Module R N]
    (τ : M →ₗ[R] N) (x δ : M) (hδ : δ ∈ LinearMap.ker τ) :
    τ (x + δ) = τ x := by
  rw [map_add, LinearMap.mem_ker.mp hδ, add_zero]

structure SVDAuditReport where
  sigmaMin : ℝ
  destroyedDims : ℕ

def AdmissibleSubspace (r : SVDAuditReport) : Prop :=
  0 < r.sigmaMin ∧ r.destroyedDims = 0

theorem admissible_implies_nonzero_floor {r : SVDAuditReport} (h : AdmissibleSubspace r) :
    r.sigmaMin ≠ 0 :=
  ne_of_gt h.1

structure AuthorshipProfile where
  contribution : Prop
  endorsement : Prop
  standing : Prop
  answerability : Prop
  operativeRefusal : Prop

def IsAccountableAuthor (p : AuthorshipProfile) : Prop :=
  p.contribution ∧ p.endorsement ∧ p.standing ∧ p.answerability ∧ p.operativeRefusal

theorem non_entailment_of_accountable_authorship :
    ∃ p : AuthorshipProfile, p.contribution ∧ ¬ IsAccountableAuthor p := by
  refine ⟨⟨True, False, False, False, False⟩, trivial, ?_⟩
  intro h
  exact h.2.1

end EpistemicAudit

namespace SpherepopSheafBridge

/-- Scoped execution disposition modeled after Spherepop@fe79af5. -/
inductive Disposition where
  | collapsed : Disposition
  | refused (reason : String) : Disposition
  deriving DecidableEq, Repr

/-- Local verification state for a rank-k patch or scoped sphere. -/
structure ScopedPatch where
  localVerified : Bool
  boundAuthority : Bool

/-- Global collapse is admissible iff both local scopes are verified,
    bound to authority, and their overlap coboundary vanishes (delta^0 s = 0). -/
def evaluateComposition (p1 p2 : ScopedPatch) (overlapCoboundaryZero : Bool) : Disposition :=
  if p1.localVerified && p2.localVerified && p1.boundAuthority && p2.boundAuthority && overlapCoboundaryZero then
    Disposition.collapsed
  else
    Disposition.refused "COBOUNDARY_OR_AUTHORITY_OBSTRUCTION"

/-- Nested Sphere Theorem: Locally valid patches with non-vanishing coboundary
    are mathematically barred from global collapse and must emit Refuse. -/
theorem nested_obstruction_forces_refusal
    (p1 p2 : ScopedPatch)
    (h1 : p1.localVerified = true) (h2 : p2.localVerified = true)
    (hb1 : p1.boundAuthority = true) (hb2 : p2.boundAuthority = true)
    (h_obs : overlapCoboundaryZero = false) :
    evaluateComposition p1 p2 overlapCoboundaryZero =
      Disposition.refused "COBOUNDARY_OR_AUTHORITY_OBSTRUCTION" := by
  simp [evaluateComposition, h1, h2, hb1, hb2, h_obs]

/-- Linear coboundary exactness (delta^1 o delta^0 = 0) over modules:
    any exact 1-cochain delta^0(s) lies in ker(delta^1). -/
theorem coboundary_exactness_zero
    {R C0 C1 C2 : Type*} [Ring R]
    [AddCommGroup C0] [Module R C0]
    [AddCommGroup C1] [Module R C1]
    [AddCommGroup C2] [Module R C2]
    (d0 : C0 →ₗ[R] C1) (d1 : C1 →ₗ[R] C2)
    (hexact : d1.comp d0 = 0) (s : C0) :
    d1 (d0 s) = 0 := by
  have h := LinearMap.congr_fun hexact s
  simpa [LinearMap.comp_apply] using h

end SpherepopSheafBridge

namespace V4HardwareAndCohomologyGate

open SpherepopSheafBridge

/-- Hardware memory admissibility gate modeled after Audit IV (llmfit sizing check). -/
def evaluateHardwareAndComposition
    (memWithinBudget : Bool)
    (p1 p2 : ScopedPatch)
    (overlapCoboundaryZero : Bool) : Disposition :=
  if !memWithinBudget then
    Disposition.refused "HARDWARE_MEMORY_EXCEEDED"
  else
    evaluateComposition p1 p2 overlapCoboundaryZero

/-- Theorem: Exceeding the cgroup/CI RAM budget forces an auditable Spherepop
    REFUSE event prior to tensor allocation, preventing silent OOM kills. -/
theorem memory_overflow_forces_refusal
    (p1 p2 : ScopedPatch) (overlapCoboundaryZero : Bool) :
    evaluateHardwareAndComposition false p1 p2 overlapCoboundaryZero =
      Disposition.refused "HARDWARE_MEMORY_EXCEEDED" := by
  simp [evaluateHardwareAndComposition]

end V4HardwareAndCohomologyGate

namespace V5DepthChainGate

open SpherepopSheafBridge

/-- Evaluates global collapse across an entire multi-layer trajectory (L_0 -> L_{N-1}):
    every layer must pass coboundary gluing for global COLLAPSE to be admissible. -/
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

/-- Theorem: A multi-layer chain collapses if and only if every layer is obstruction-free. -/
theorem layer_chain_collapses_iff_all_true (layers : List Bool) :
    evaluateLayerChain layers = Disposition.collapsed ↔ ∀ b ∈ layers, b = true := by
  unfold evaluateLayerChain
  split
  · rename_i h
    rw [List.all_eq_true] at h
    exact ⟨fun _ b hb => h b hb, fun _ => rfl⟩
  · rename_i h
    constructor
    · intro h_eq; cases h_eq
    · intro hall
      exfalso
      apply h
      rw [List.all_eq_true]
      intro b hb
      exact hall b hb

end V5DepthChainGate

namespace V6ApplicationContracts

open SpherepopSheafBridge

/-- Unified operational state across all four v6 application tracks:
    Track 1 (Firewall), Track 2 (Quantization), Track 3 (CI Warrant), Track 4 (Calibration). -/
structure V6DeploymentState where
  firewallLayersClean : Bool
  quantGeometryValid : Bool
  humanWarrantBound : Bool
  unembeddingCalibrated : Bool

def evaluateV6Pipeline (s : V6DeploymentState) : Disposition :=
  if s.firewallLayersClean && s.quantGeometryValid && s.humanWarrantBound && s.unembeddingCalibrated then
    Disposition.collapsed
  else if !s.firewallLayersClean then
    Disposition.refused "TRACK1_RUNTIME_STEERING_OBSTRUCTION"
  else if !s.quantGeometryValid then
    Disposition.refused "TRACK2_QUANTIZATION_GEOMETRY_DISTORTION"
  else if !s.humanWarrantBound then
    Disposition.refused "TRACK3_UNENDORSED_ASYMMETRIC_INSCRIPTION"
  else
    Disposition.refused "TRACK4_UNEMBEDDING_CALIBRATION_ANOMALY"

theorem v6_pipeline_collapses_iff_all_four_tracks_pass (s : V6DeploymentState) :
    evaluateV6Pipeline s = Disposition.collapsed ↔
      (s.firewallLayersClean = true ∧
       s.quantGeometryValid = true ∧
       s.humanWarrantBound = true ∧
       s.unembeddingCalibrated = true) := by
  unfold evaluateV6Pipeline
  by_cases h1 : s.firewallLayersClean = true <;>
  by_cases h2 : s.quantGeometryValid = true <;>
  by_cases h3 : s.humanWarrantBound = true <;>
  by_cases h4 : s.unembeddingCalibrated = true <;>
  simp [h1, h2, h3, h4]

end V6ApplicationContracts

namespace V7EstablishedRepairGate

open SpherepopSheafBridge

/-- History state tracking established Q16.16 checkpoint hashes and maintenance burden
    modeled after spherepop-kernel@6be6108 (repair_target_fixture.json). -/
structure RepairHistory where
  establishedHashes : List String
  currentHead : String
  length : Nat
  burden : Nat
  budget : Nat
  deriving DecidableEq, Repr

/-- Evaluates a Spherepop REPAIR request against established history H,
    principal authorization, maintenance budget, and post-repair sheaf gluing. -/
def evaluateRepair
    (h : RepairHistory)
    (targetHash : String)
    (authorized : Bool)
    (postRepairCoboundaryZero : Bool) : Disposition × RepairHistory :=
  if !(targetHash ∈ h.establishedHashes) then
    (Disposition.refused "UNESTABLISHED", h)
  else if !authorized then
    (Disposition.refused "UNAUTHORIZED_PRINCIPAL", h)
  else if h.burden > h.budget then
    (Disposition.refused "MAINTENANCE_BUDGET_EXCEEDED", h)
  else if !postRepairCoboundaryZero then
    (Disposition.refused "REPAIR_COBOUNDARY_OBSTRUCTION", h)
  else
    let h' : RepairHistory := {
      establishedHashes := targetHash :: h.establishedHashes
      currentHead := targetHash
      length := h.length + 1
      burden := h.burden
      budget := h.budget
    }
    (Disposition.collapsed, h')

/-- Theorem (Matches repair_target_fixture.json Step 1):
    If targetHash is not in H.establishedHashes, evaluateRepair MUST emit
    REFUSE("UNESTABLISHED") and leave H completely unchanged. -/
theorem unestablished_target_forces_refusal_and_preserves_history
    (h : RepairHistory) (targetHash : String)
    (authorized postRepairCoboundaryZero : Bool)
    (h_missing : targetHash ∉ h.establishedHashes) :
    evaluateRepair h targetHash authorized postRepairCoboundaryZero =
      (Disposition.refused "UNESTABLISHED", h) := by
  simp [evaluateRepair, h_missing]

/-- Theorem (Matches repair_target_fixture.json Step 3):
    An established target, authorized principal, bounded burden, and clean
    harmonic coboundary yield COLLAPSE and advance history length by 1. -/
theorem valid_established_repair_collapses
    (h : RepairHistory) (targetHash : String)
    (h_est : targetHash ∈ h.establishedHashes)
    (h_auth : authorized = true)
    (h_bud : ¬ (h.burden > h.budget))
    (h_cob : postRepairCoboundaryZero = true) :
    (evaluateRepair h targetHash authorized postRepairCoboundaryZero).1 = Disposition.collapsed ∧
    (evaluateRepair h targetHash authorized postRepairCoboundaryZero).2.length = h.length + 1 := by
  simp [evaluateRepair, h_est, h_auth, h_bud, h_cob]

end V7EstablishedRepairGate
