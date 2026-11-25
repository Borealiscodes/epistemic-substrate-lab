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
  calc
    ‖f x - f z‖ = ‖(f x - f y) + (f y - f z)‖ := by ring_nf
    _ ≤ ‖f x - f y‖ + ‖f y - f z‖ := norm_add_le _ _

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
  Finset.univ.fold GaussianRat.add GaussianRat.zero v

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
