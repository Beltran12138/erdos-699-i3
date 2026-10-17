# Erdős Problem #699 at i = 3

Partial progress on [Erdős Problem #699](https://www.erdosproblems.com/699): for i = 3, every counterexample must have 4 | n and a power-of-2 factor of size ≳ n^{2/3}, so at most O(X^{1/3}) values n ≤ X remain. There is no counterexample with n ≤ 10¹⁶.

- **[NOTE.md](NOTE.md)**: statements, proofs, verification status, and what remains open.
- **[lean/Erdos699I3.lean](lean/Erdos699I3.lean)**: Lean 4 / Mathlib formalisation of the prime-power core (the Lucas low-digit lemma and the three labelled local lemmas). It uses the standard axioms only and has no `sorry`. The assembly steps are not formalised.
- **Code**:
  - `micro.py`: direct exact scan, independent of the lemmas;
  - `search2.py`: exhaustive search parametrised by Lemma 1;
  - `search3.py`: lemma-sieved check of all n ≤ Y;
  - `sieve_exact_check.py`: checks the float sieve against an exact-integer version;
  - `brute.py`, `test_lemma1*.py`: controls.
- **Logs**: `*.log`, the outputs of the runs cited in NOTE.md.
- **Process records**: `PLAN.md` (pre-registration, frozen before the work began) and `LOG.md` (run log), both in Chinese.

Produced by Claude (Anthropic) working with the repository owner; an independent Claude agent served as referee. There has been no human specialist review yet. Please report errors via GitHub issues.

License: MIT for code; the text of NOTE.md is CC BY 4.0.
