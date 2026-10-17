# Erdős #699 at i = 3: a counterexample needs 4 | n and a power of 2 of size ≳ √n

*Draft, 2026-10-17. The proofs below were checked by an independent referee (a separate agent working from the statements only), and the prime-power core is formalised in Lean 4 / Mathlib. There has been no human specialist review.*

## 1. Background

Erdős Problem #699 (Erdős–Szekeres) asks whether, for every 1 ≤ i < j ≤ n/2, some prime p ≥ i divides gcd(C(n,i), C(n,j)). The following were known when this note was written (2026-10-17):

- **i ≥ 4.** Van Doorn–Rocca (proof claim, 2026-07-25) show that there are only finitely many exceptions. They write: "for i = 3 we cannot even exclude the possibility that G is a power of two infinitely often". A companion manuscript ("The cubic boundary") says that a completion at i = 3 must keep track of which of n, n−1, n−2 supplies each prime power.
- **i = 3, specific j.** j ≤ 3i/2 and j = n/2 are settled (Price / GPT-5.6, accepted by the site); j = 5 follows from Del Pin's comment.

For i = 3 the question becomes: for 3 < j < n/2, can G = gcd(C(n,3), C(n,j)) be a power of 2?

## 2. Notation

- **N(x) and A(x).** For x ≥ 1, x = N(x)·A(x), where N(x) is the {2,3}-part of x and every prime factor of A(x) is ≥ 5.
- **N′(x) and B(x).** For x ≥ 1, x = N′(x)·B(x), where N′(x) = 2^{v₂(x)}·3^{[v₃(x)=1]}. So B(x) consists of the primes ≥ 5 together with 3^{v₃(x)} when v₃(x) ≥ 2.
- **Why B is the right object.** Exactly one of n, n−1, n−2 is divisible by 3; call it y. Then v₃(C(n,3)) = v₃(y) − 1. So 3 | C(n,3) exactly when 9 | y, which is exactly when 3 lands in B(y). Hence the odd primes dividing C(n,3) are precisely the primes dividing B(n)B(n−1)B(n−2).

## 3. Results

**Lemma 1.** Let 1 ≤ j < n/2 and suppose no prime ≥ 5 divides both C(n,3) and C(n,j). Write N₀ = N(n), A_k = A(n−k) and N_k = N(n−k). Then:

- (a) A₀ | j. Writing j = c·A₀, we have 1 ≤ c < N₀/2, and hence N₀ ≥ 3.
- (b) A₁ | lcm(c, N₀−c).
- (c) A₂ | lcm(c, N₀−c, N₀−2c).
- (d) N₀³ ≥ 3√3·(n−2).

**Lemma 1′.** Under the same hypotheses:

- (e) A₁A₂ | c(N₀−c)(N₀−2c).
- (f) (n−1)(n−2) < N₁N₂N₀³/(6√3).
- If N₁ = 1, then also n−1 ≤ N₀²/4.

**Theorem 2.** Let 4 ≤ j < n/2 and suppose G = gcd(C(n,3), C(n,j)) is a power of 2. Write N′ = N′(n), N_k′ = N′(n−k) and B_k = B(n−k). Then:

- (a′)–(e′) hold: these are (a), (b), (c), (e) with B, N′ in place of A, N.
- (g) 4 | n and N₁′N₂′ ≤ 6.
  - If N₁′ = 1, then n−1 ≤ N′²/4.
  - If N₁′ ≠ 1, then 3 ∥ n−1, N′ = 2^{v₂(n)}, and √3·(n−1)(n−2) < N′³.

  In every case, 2^{v₂(n)} ≥ (2/3)·√(n−1).

**Corollary.** Every counterexample to #699 at i = 3 has 4 | n and 2^{v₂(n)} ≥ (2/3)·√(n−1). When 3 ∥ n−1 the condition is even 2^{v₂(n)} ≳ 1.2·n^{2/3}.

For comparison, the number of n ≤ X that survive each filter:

| filter | n ≤ 10⁵ | n ≤ 10⁶ | n ≤ 10⁷ |
|---|---|---|---|
| Lemma 1 (d) | 4,749 | 24,694 | 127,560 |
| Lemma 1′ | 337 | 856 | 2,100 |
| Theorem 2 (g) | 288 | 920 | 2,892 |
| Lemma 1′ + Theorem 2 | 126 | 312 | 737 |

The Theorem 2 count grows like √X.

## 4. Proofs

**Local step (Lucas).** Let p be a prime, k ∈ {0,1,2} with k < p, and p^e ∥ n−k. If p ∤ C(n,j), then

  j mod p^e ∈ {0, …, k}.   (★)

The reason is that the lowest e base-p digits of n are k, 0, …, 0, and Lucas's theorem says each digit of j is at most the corresponding digit of n. This is formalised as `low_digits`.

**Labelled step.** Let n = N₀A₀ and j = cA₀.

- **k = 0.** p^e | j. This is `local_k0`, and it gives (a).
- **k = 1.**
  - If j ≡ 0 (mod p^e): from p^e | N₀A₀ − 1 we get gcd(p^e, A₀) = 1, so p^e | c.
  - If j ≡ 1 (mod p^e): then p^e divides N₀ − c = c(N₀A₀ − 1) − N₀(cA₀ − 1).

  This is `local_k1`.
- **k = 2, p odd.** The three residues j ≡ 0, 1, 2 (mod p^e) give p^e | c, p^e | N₀ − 2c and p^e | N₀ − c respectively. Here we use 2(N₀ − c) = c(N₀A₀ − 2) − N₀(cA₀ − 2) and the fact that p^e is odd. This is `local_k2`.

The same steps apply with B and N′ in place of A and N. For p = 3 with v₃ ≥ 2 we still have k ≤ 2 < 3, and N′ is invertible mod 3 whenever 3 | n−1 or 3 | n−2.

**Assembly.**

- **Pairwise gcds.** gcd(c, N₀−c), gcd(c, N₀−2c) and gcd(N₀−c, N₀−2c) all divide gcd(c, N₀). So they are {2,3}-numbers (powers of 2 in the primed setting whenever 3 | B₁B₂).
- **(e).** By the labelled step, each prime power of A₁A₂ lands whole in exactly one of c, N₀−c, N₀−2c. The prime powers are pairwise coprime, so their product divides c(N₀−c)(N₀−2c). (b) and (c) follow in the same way.
- **Size bound.** On 0 < x < 1/2, the function x(1−x)(1−2x) has maximum 1/(6√3), attained at the irrational point x = (3−√3)/6. Hence c(N₀−c)(N₀−2c) < N₀³/(6√3) for every integer c. Since (n−1)(n−2) = N₁N₂A₁A₂, this gives (f). If N₁ = 1, then n−1 = A₁ ≤ c(N₀−c) ≤ N₀²/4.
- **(d), from the case analysis on the {2,3}-parts.** In every case N₁ = 1 or N₂ ≤ 2:
  - n odd: N₀ is a power of 3 and 3 | n, so N₂ = 1;
  - v₂(n) = 1: N₀ = 2·3^b with b ≥ 1, so N₁ = 1;
  - v₂(n) ≥ 2: N₁ = 1 if 3 | n−2, and N₂ = 2 otherwise.

  In each case n−2 ≤ 2c(N₀−c)(N₀−2c) < N₀³/(3√3).
- **(g).**
  - *n odd.* Then N′ = 3, c = 1, and (c′) forces B(n−2) | 2, so n = 3. This is excluded because j ≥ 4 requires n ≥ 9. Both (b′) and (c′) are needed here: n = 2^k + 1 satisfies the (b′) condition.
  - *n ≡ 2 (mod 4).* Then N′ = 6 and c ∈ {1, 2}, and (b′) forces n−1 | 5 or n−1 = 1, so n ≤ 6.
  - *4 | n.* Then N₁′ ∈ {1, 3} and N₂′ ∈ {2, 6}, and 3 occurs in at most one of them. The bound follows as in (f).

## 5. Verification

- **Referee.** A separate agent was given only the statements. It had no access to these files or to the web. It proved Lemma 1, Lemma 1′ and Theorem 2 independently: all parts were judged PROVED, with high confidence. It then tested them with its own code:
  - full enumeration of 2,233,530 pairs (n ≤ 3000) and of 1,553,762 pairs (n ≤ 2500), each computed by direct gcd and by Kummer, with 0 disagreements;
  - non-vacuous tests under weakened hypotheses, including 13,252,951 cases for a generalised (e), with 0 failures;
  - negative controls (wrong variants of (b), (c), (e) and (g)), all of which were caught.
- **Lean 4 / Mathlib.** `lean/Erdos699I3.lean` formalises `low_digits`, `local_k0`, `local_k1` and `local_k2`. The axioms used are propext, Classical.choice and Quot.sound only; there is no `sorry` and no `native_decide`. The assembly (multiplying coprime prime powers, the {2,3}-part case analysis and the calculus bound) is **not** formalised.
- **Computation.**
  - `micro.py` (exact Lucas test; it does not use the lemmas): for n ≤ 10⁷ no pair with 6 ≤ j < n/2 has gcd free of primes ≥ 5. It agrees pair by pair with brute force for n ≤ 1500. With j = n/2 allowed it reproduces (28,14), (244,122) and (2188,1094).
  - `search2.py`: covers every such pair with N(n) ≤ 10⁶ and finds none. The only pair satisfying the low-digit congruences alone is (162, 70).
  - `search3.py` (uses the sieve of Lemma 1′ + Theorem 2, then tests every j in [4, n/2] exactly, via CRT over all low-digit congruences and then full Lucas): for **all n ≤ 10¹⁶** there is no counterexample and no pair sharing no prime ≥ 5. 1,300,756 sieve survivors were tested. The float comparisons in the sieve were re-run in exact integer form (squared inequalities), and the survivor sets are identical (`sieve_exact_check.py`).
  - **Consequence.** Given Lemma 1′ and Theorem 2, and Price's j = n/2 case, Erdős #699 holds at i = 3 for every n ≤ 10¹⁶.

## 6. What remains open

The open part of i = 3 is the family n = 2^a·m with odd m ≲ 2.25·2^a, i.e. at most O(√X) values n ≤ X, subject to the further divisibility conditions (b′), (c′) and (e′). Numerically these conditions leave no n ≤ 10⁶; the referee observed this, and it is not proved. Heuristically only finitely many n should survive. A proof would need to control simultaneous divisibility of n−1 and n−2 by c, N′−c and N′−2c when N′ is a large power of 2. This resembles S-unit problems, where the known tools are ineffective.

## 7. AI usage

The lemmas, the code and this note were produced by Claude (Anthropic), working with the user. The referee was a separate Claude agent instance.
