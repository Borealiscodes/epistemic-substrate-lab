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
