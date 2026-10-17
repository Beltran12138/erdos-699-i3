import Mathlib

/-!
# Erdős #699 at i = 3 — the local (prime-power) lemmas behind Lemma 1 / Theorem 2

`low_digits` is the Lucas-theorem step: if `p ^ e ∣ n - k` with `k < p` and `p ∤ C(n, j)`,
then the lowest `e` base-`p` digits of `j` force `j % p ^ e ≤ k`.

`local_k0`, `local_k1`, `local_k2` are the "labelled" steps: with `n = N0 * A0` and `j = c * A0`,
a prime power exactly attached to `n`, `n - 1`, `n - 2` must divide `c`, `N0 - c`, or `N0 - 2c`.

Not formalised here (see NOTE.md): multiplying the pairwise coprime prime powers together,
the case analysis on the {2,3}-parts, and the calculus bound `max c(N0-c)(N0-2c) = N0^3/(6√3)`.
-/

open Nat

namespace Erdos699I3

/-- Lucas, low digits: `p ^ e ∣ n - k`, `k < p`, `k ≤ n`, `p ∤ C(n,j)`  ⟹  `j % p ^ e ≤ k`. -/
theorem low_digits {p : ℕ} [hp : Fact p.Prime] (e : ℕ) :
    ∀ {n j k : ℕ}, k < p → k ≤ n → p ^ e ∣ n - k → ¬ p ∣ n.choose j → j % p ^ e ≤ k := by
  induction e with
  | zero => intro n j k _ _ _ _; rw [pow_zero, Nat.mod_one]; exact Nat.zero_le _
  | succ e ih =>
    intro n j k hkp hkn hdvd hnc
    have hp0 : 0 < p := hp.out.pos
    -- n % p = k and n / p = (n - k) / p
    obtain ⟨m, hm⟩ := hdvd
    have hn : n = k + p * (p ^ e * m) := by rw [pow_succ] at hm; rw [← mul_assoc, mul_comm p]; omega
    have hnmod : n % p = k := by rw [hn, Nat.add_mul_mod_self_left, Nat.mod_eq_of_lt hkp]
    have hndiv : n / p = p ^ e * m := by
      rw [hn, Nat.add_mul_div_left _ _ hp0, Nat.div_eq_of_lt hkp, zero_add]
    -- Lucas: C(n,j) ≡ C(n%p, j%p) * C(n/p, j/p)  [MOD p]
    have hl : n.choose j ≡ (n % p).choose (j % p) * (n / p).choose (j / p) [MOD p] :=
      Choose.choose_modEq_choose_mod_mul_choose_div_nat
    have hprod : ¬ p ∣ (n % p).choose (j % p) * (n / p).choose (j / p) := by
      intro h; apply hnc
      exact (Nat.modEq_zero_iff_dvd.mp (hl.trans (Nat.modEq_zero_iff_dvd.mpr h)))
    -- lowest digit
    have hlow : j % p ≤ k := by
      by_contra hlt
      apply hprod
      rw [hnmod, Nat.choose_eq_zero_of_lt (by omega), zero_mul]
      exact dvd_zero p
    -- the next e digits vanish (induction with k = 0)
    have hhigh : (j / p) % p ^ e ≤ 0 := by
      refine ih (n := n / p) hp0 (Nat.zero_le _) ?_ ?_
      · rw [Nat.sub_zero, hndiv]; exact dvd_mul_right _ _
      · intro h; apply hprod; exact Dvd.dvd.mul_left h _
    obtain ⟨t, ht⟩ := Nat.dvd_of_mod_eq_zero (Nat.le_zero.mp hhigh)
    have hj : j = j % p + p ^ (e + 1) * t := by
      have := Nat.mod_add_div j p
      rw [ht] at this
      calc j = j % p + p * (p ^ e * t) := this.symm
        _ = j % p + p ^ (e + 1) * t := by ring
    have hlt : j % p < p ^ (e + 1) :=
      lt_of_lt_of_le (Nat.mod_lt _ hp0) (Nat.le_self_pow (Nat.succ_ne_zero e) p)
    rw [hj, Nat.add_mul_mod_self_left, Nat.mod_eq_of_lt hlt]
    exact hlow

/-- k = 0: a prime power dividing `n` divides `j`. -/
theorem local_k0 {p e n j : ℕ} [hp : Fact p.Prime]
    (hdvd : p ^ e ∣ n) (hnc : ¬ p ∣ n.choose j) : p ^ e ∣ j := by
  have := low_digits (p := p) e (k := 0) hp.out.pos (Nat.zero_le n) (by simpa using hdvd) hnc
  exact Nat.dvd_of_mod_eq_zero (Nat.le_zero.mp this)

/-- k = 1: with `n = N0*A0`, `j = c*A0`, a prime power dividing `n - 1` divides `c` or `N0 - c`. -/
theorem local_k1 {p e N0 A0 c : ℕ} [hp : Fact p.Prime]
    (hpos : 1 ≤ N0 * A0) (hdvd : p ^ e ∣ N0 * A0 - 1)
    (hnc : ¬ p ∣ (N0 * A0).choose (c * A0)) :
    (p ^ e : ℤ) ∣ c ∨ (p ^ e : ℤ) ∣ (N0 : ℤ) - c := by
  have hr := low_digits (p := p) e (k := 1) hp.out.one_lt hpos hdvd hnc
  obtain ⟨t, ht⟩ := hdvd
  have htZ : ((N0 : ℤ) * A0 - 1) = (p ^ e : ℤ) * t := by
    have : ((N0 * A0 - 1 : ℕ) : ℤ) = (N0 : ℤ) * A0 - 1 := by push_cast [Nat.cast_sub hpos]; ring
    rw [← this, ht]; push_cast; ring
  rcases Nat.le_one_iff_eq_zero_or_eq_one.mp hr with h0 | h1
  · -- j ≡ 0 : p^e ∣ c*A0 and p^e is coprime to A0
    left
    obtain ⟨q, hq⟩ := Nat.dvd_of_mod_eq_zero h0
    have hcop : IsCoprime (p ^ e : ℤ) (A0 : ℤ) := ⟨-t, N0, by linarith [htZ]⟩
    have : (p ^ e : ℤ) ∣ (A0 : ℤ) * c := ⟨q, by rw [mul_comm]; exact_mod_cast hq⟩
    exact hcop.dvd_of_dvd_mul_left this
  · -- j ≡ 1 : p^e ∣ c*A0 - 1, and N0 - c = c*(N0*A0 - 1) - N0*(c*A0 - 1)
    right
    have h1' := Nat.div_add_mod (c * A0) (p ^ e)
    rw [h1] at h1'
    set q := c * A0 / p ^ e
    have hjZ : ((c : ℤ) * A0 - 1) = (p ^ e : ℤ) * q := by
      have : ((c * A0 : ℕ) : ℤ) = (p ^ e : ℤ) * q + 1 := by exact_mod_cast h1'.symm
      push_cast at this; linarith
    exact ⟨c * t - N0 * q, by linear_combination (c : ℤ) * htZ - (N0 : ℤ) * hjZ⟩

/-- k = 2 (p odd): a prime power dividing `n - 2` divides `c`, `N0 - 2c`, or `N0 - c`. -/
theorem local_k2 {p e N0 A0 c : ℕ} [hp : Fact p.Prime] (hp2 : p ≠ 2)
    (hpos : 2 ≤ N0 * A0) (hdvd : p ^ e ∣ N0 * A0 - 2)
    (hnc : ¬ p ∣ (N0 * A0).choose (c * A0)) :
    (p ^ e : ℤ) ∣ c ∨ (p ^ e : ℤ) ∣ (N0 : ℤ) - 2 * c ∨ (p ^ e : ℤ) ∣ (N0 : ℤ) - c := by
  have hp3 : 2 < p := lt_of_le_of_ne hp.out.two_le (Ne.symm hp2)
  have hr := low_digits (p := p) e (k := 2) hp3 hpos hdvd hnc
  obtain ⟨t, ht⟩ := hdvd
  have htZ : ((N0 : ℤ) * A0 - 2) = (p ^ e : ℤ) * t := by
    have : ((N0 * A0 - 2 : ℕ) : ℤ) = (N0 : ℤ) * A0 - 2 := by push_cast [Nat.cast_sub hpos]; ring
    rw [← this, ht]; push_cast; ring
  -- p^e is odd, hence coprime to 2
  have hodd : Odd (p ^ e) := (hp.out.odd_of_ne_two hp2).pow
  obtain ⟨s, hs⟩ := hodd
  have hsZ : (p : ℤ) ^ e = 2 * s + 1 := by exact_mod_cast hs
  have hcop2 : IsCoprime (p ^ e : ℤ) 2 := ⟨1, -s, by linarith [hsZ]⟩
  have h' := Nat.div_add_mod (c * A0) (p ^ e)
  set q := c * A0 / p ^ e
  have hjq : ((c : ℤ) * A0) = (p ^ e : ℤ) * q + ((c * A0 % p ^ e : ℕ) : ℤ) := by
    exact_mod_cast h'.symm
  interval_cases hrv : (c * A0 % p ^ e)
  · -- j ≡ 0 : p^e ∣ c*A0, so p^e ∣ c*(N0*A0) = c*(p^e t + 2), so p^e ∣ 2c
    left
    have h2c : (p ^ e : ℤ) ∣ 2 * c :=
      ⟨N0 * q - c * t, by push_cast at hjq; linear_combination (-(c : ℤ)) * htZ + (N0 : ℤ) * hjq⟩
    exact hcop2.dvd_of_dvd_mul_left h2c
  · -- j ≡ 1 : N0 - 2c = c*(N0*A0 - 2) - N0*(c*A0 - 1)
    right; left
    exact ⟨c * t - N0 * q, by push_cast at hjq; linear_combination (c : ℤ) * htZ - (N0 : ℤ) * hjq⟩
  · -- j ≡ 2 : 2(N0 - c) = c*(N0*A0 - 2) - N0*(c*A0 - 2)
    right; right
    have h2 : (p ^ e : ℤ) ∣ 2 * ((N0 : ℤ) - c) :=
      ⟨c * t - N0 * q, by push_cast at hjq; linear_combination (c : ℤ) * htZ - (N0 : ℤ) * hjq⟩
    exact hcop2.dvd_of_dvd_mul_left h2

end Erdos699I3

#print axioms Erdos699I3.low_digits
#print axioms Erdos699I3.local_k0
#print axioms Erdos699I3.local_k1
#print axioms Erdos699I3.local_k2
