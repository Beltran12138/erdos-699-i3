# Erdős #699 at i = 3: almost all n are settled

*Draft, 2026-10-17. Not yet independently refereed.*

## Statement

For a positive integer x write x = N(x)·A(x), where N(x) is the largest divisor of x of the form 2^a 3^b and every prime factor of A(x) is at least 5.

**Lemma 1.** Let 6 ≤ j < n/2 and suppose no prime p ≥ 5 divides both C(n,3) and C(n,j). Put N₀ = N(n), A₀ = A(n), A₁ = A(n−1), A₂ = A(n−2). Then

- (a) A₀ | j; writing j = c·A₀, we have 1 ≤ c < N₀/2;
- (b) A₁ | lcm(c, N₀−c);
- (c) A₂ | lcm(c, N₀−c, N₀−2c);
- (d) N₀³ ≥ 3√3·(n−2).

**Corollary.** If N(n)³ < 3√3·(n−2), then for every 3 < j ≤ n/2 some prime p ≥ 3 divides gcd(C(n,3), C(n,j)). That is, Erdős Problem #699 holds for i = 3 at this n. For j < n/2 the shared prime can even be taken to be ≥ 5.

The n not covered satisfy N(n) ≥ 1.73·(n−2)^{1/3}. Up to X there are ≍ X^{2/3} log X of them, so the corollary covers a set of n of density 1. Numerically the uncovered share is 8.7% of n ≤ 10⁴, 4.7% of n ≤ 10⁵, 2.5% of n ≤ 10⁶ and 1.3% of n ≤ 10⁷.

## Proof

**Local condition.** Let p ≥ 5 be a prime with p^e ∥ n−k, where k ∈ {0,1,2}. Then p | C(n,3), so by hypothesis p ∤ C(n,j). By Lucas's theorem every base-p digit of j is at most the corresponding digit of n. Because n ≡ k (mod p^e) and k < p, the lowest e digits of n are k, 0, …, 0. Hence

  j ≡ t (mod p^e) for some t ∈ {0, …, k}.   (★)

**(a)** For k = 0, (★) forces p^e | j. This holds for every prime power exactly dividing A₀, so A₀ | j. Write j = c·A₀ with c ≥ 1. Since j < n/2 = N₀A₀/2, we get c < N₀/2.

**(b)** Split A₁ = d·e, where d collects the prime powers with t = 0 and e those with t = 1. Then d | j = cA₀ and gcd(d, A₀) = 1, so d | c. Also e | j − 1 = cA₀ − 1 and e | n − 1 = N₀A₀ − 1, hence

  e | N₀(cA₀ − 1) − c(N₀A₀ − 1) = c − N₀.

Since 0 < N₀ − c, we get e | N₀ − c. As gcd(d, e) = 1, A₁ = de divides lcm(c, N₀−c).

**(c)** Split A₂ = d·f·g according to t = 0, 1, 2. As in (b), d | c. Next, f | cA₀ − 1 and f | N₀A₀ − 2 give f | N₀(cA₀−1) − c(N₀A₀−2) = 2c − N₀, and N₀ − 2c ≥ 1. Finally, g | cA₀ − 2 and g | N₀A₀ − 2 give g | 2(c − N₀); g is odd, so g | N₀ − c. The three parts are pairwise coprime, so A₂ | lcm(c, N₀−c, N₀−2c).

**(d)** Exactly one of n, n−1, n−2 is divisible by 3. Moreover N₀ ≥ 3, since N₀ ≤ 2 would force c < 1. The three cases are:

- *n odd.* Then N₀ is a power of 3, and N₀ > 1 forces 3 | n. Hence n−2 is coprime to 6 and N(n−2) = 1.
- *v₂(n) = 1.* Then N₀ = 2·3^b with b ≥ 1, so 3 | n. Since n−1 is odd and not divisible by 3, N(n−1) = 1.
- *v₂(n) ≥ 2.* Then v₂(n−2) = 1. If 3 | n−2, then N(n−1) = 1. Otherwise N(n−2) = 2.

So either n − 1 = A₁ ≤ c(N₀−c) ≤ N₀²/4, or n − 2 ≤ 2A₂ ≤ 2c(N₀−c)(N₀−2c). On 0 < x < 1/2 the function x(1−x)(1−2x) has maximum 1/(6√3), attained at x = (3−√3)/6. Hence n − 2 ≤ N₀³/(3√3) in both cases.

**Corollary.** Take 3 < j ≤ n/2.
- j = 4: covered by the case j ≤ 3i/2 (Price, accepted on the site).
- j = 5: follows from the same size argument (Del Pin, forum comment, 2026-07-24).
- j = n/2: covered by Price's n = 2j case.
- 6 ≤ j < n/2: if no prime ≥ 5 were shared, (d) would contradict N(n)³ < 3√3(n−2). ∎

## Computations

All code is in this repository.

- **Direct scan, independent of Lemma 1** (`micro.py`, exact Lucas test, no use of the lemma): for 6 ≤ j < n/2 and all n ≤ 10⁷, no pair shares no prime ≥ 5. Controls: it agrees pair by pair with a direct-gcd brute force for n ≤ 1500. With j = n/2 allowed it reproduces the known pairs (28,14), (244,122) and (2188,1094). A deliberately weakened test produces a spurious hit.
- **Parametrised search via Lemma 1** (`search2.py`): enumerating {2,3}-numbers N₀ ≤ X and 1 ≤ c < N₀/2, then the divisors allowed by (b) and (c), covers every pair (n, j) with 6 ≤ j < n/2 sharing no prime ≥ 5 and having N(n) ≤ X. For X = 10⁵ there is none. Keeping only the low-digit congruences (★), the only pair is (162, 70). [X = 10⁶: running.]
- **Tests of (a)–(c)** on relaxations with many solutions (336 and 1523 pairs): 0 failures. Deliberately wrong variants fail 243 and 783 times.

## Relation to existing work

Van Doorn–Rocca (proof claim, 2026-07-25) prove that for 4 ≤ i there are only finitely many exceptions. They state that for i = 3 they "cannot even exclude the possibility that G is a power of two infinitely often". The accompanying manuscript's section "The cubic boundary" says that a completion at i = 3 must keep track of which of n, n−1, n−2 supplies each prime power. Lemma 1 is an argument of exactly that labelled kind. It reduces the open part of i = 3 to the sparse set of n with N(n) ≥ 1.73 n^{1/3}, but it does not settle that set.
