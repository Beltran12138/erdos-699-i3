# Draft proof claim for erdosproblems.com/forum/thread/699 (to be submitted by the account owner)

## Claimed by
<your name> (using Claude Opus 5.5)

## Type
Partial (the case i = 3)

## Summary
Partial result for the case i = 3, which Van Doorn–Rocca's claim leaves open. Every counterexample with 4 ≤ j < n/2 must have 4 | n and 2^{v₂(n)} > (√3(n−1)(n−2))^{1/3}/3 ≈ 0.40·n^{2/3}. So only O(X^{1/3}) values n ≤ X remain, all of the form 2^a·m with m odd and m < 4·2^{a/2}. Together with the known cases j = 4, j = 5 and j = n/2, this settles i = 3 for every n outside this sparse family. A sieved exhaustive check finds no counterexample with n ≤ 10¹⁶.

The idea is the one the Van Doorn–Rocca manuscript identifies as missing ("keep track of which of n, n−1, n−2 supplies each prime power"). Write n = N′B, where B collects the primes ≥ 5 and the power of 3 when 9 divides it. By Lucas's theorem j = cB. A prime power of n−1 must divide c or N′−c, because it divides both cB − 1 and N′B − 1 and hence their combination c − N′. A prime power of n−2 must likewise divide c, N′−2c or N′−c. So (n−1)(n−2)/6 ≤ c(N′−c)(N′−2c) < N′³/(6√3).

## Notes
Verification:
- An independent referee (a separate AI agent, given only the statements, with no access to our files or the web) re-proved every part and tested it with its own code. It used full enumeration up to n ≈ 3000 by two independent methods, non-vacuous tests under weakened hypotheses, and negative controls.
- The prime-power core (the Lucas low-digit lemma and the three "labelled" local lemmas) is formalised in Lean 4 / Mathlib using the standard axioms only. The assembly steps (multiplying coprime prime powers, the case analysis on the {2,3}-parts and the calculus bound) are not formalised.
- The computations behind the n ≤ 10¹⁶ check have controls: agreement with a brute-force gcd computation for small n, reproduction of the known pairs (28,14), (244,122) and (2188,1094), and the float sieve checked against an exact-integer version.

The family n = 2^a·m above remains open. We expect it to need S-unit-type input.

AI usage: the mathematics, code and write-up were produced by Claude (Anthropic, Opus 5.5) working with me. I take responsibility for the claim. Specialist review is very welcome; please report problems as GitHub issues.

## External link to proof
https://github.com/Beltran12138/erdos-699-i3/blob/main/NOTE.md

## External link to formalisation
https://github.com/Beltran12138/erdos-699-i3/blob/main/lean/Erdos699I3.lean
