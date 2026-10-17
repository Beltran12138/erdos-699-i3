"""Clean reformulation test: g(t) = t(t-1)(t-2). For n in the remaining family F (sieve survivors),
V := B(n)*B(n-1)*B(n-2) (the 'big' part of n(n-1)(n-2): primes >= 5 and 3^b when b >= 2).
The low-digit system implies V | g(j). This is weaker (it allows e.g. a prime power of n-1 to divide j-2).
Question: does V | g(j) have a root j with 3 <= j < n/2 for some n in F?
Roots of g mod p^e (p >= 5): t ≡ 0, 1, 2. Mod 3^b (b >= 2): computed by brute force.
Usage: python gtest.py Y [cap]
"""
import sys, math
from sympy import factorint
from search3 import candidates

def roots_mod(q, p):
    if p >= 5: return [0, 1, 2]
    return [t for t in range(q) if (t * (t - 1) * (t - 2)) % q == 0]

def main(Y, cap):
    tot = 0; hits = []; skipped = 0
    for n in sorted(candidates(Y, False)):
        tot += 1
        pp = []
        for k in (0, 1, 2):
            for p, e in factorint(n - k).items():
                if p >= 5 or (p == 3 and e >= 2): pp.append((p, p ** e))
        jmax = (n - 1) // 2
        count = math.prod(len(roots_mod(q, p)) for p, q in pp)
        if count > cap: skipped += 1; continue
        sols, M = [0], 1
        for p, q in sorted(pp, key=lambda x: -x[1]):
            rs = roots_mod(q, p); invM = pow(M, -1, q); new = []
            for r0 in sols:
                for r in rs: new.append(r0 + M * (((r - r0) * invM) % q))
            M *= q
            sols = [x for x in new if x <= jmax] if M > jmax else new
        js = [x + M * s for x in sols for s in range(max(0, (jmax - x) // M) + 1)]
        js = [j for j in js if 3 <= j <= jmax]
        if js: hits.append((n, js[:5]))
    print(f"Y={Y:.0e}: {tot} survivors, skipped(cap) {skipped}, n with a root j in [3, n/2): {len(hits)} {hits[:15]}")

if __name__ == "__main__":
    main(int(float(sys.argv[1])), int(float(sys.argv[2])) if len(sys.argv) > 2 else 2 * 10 ** 6)
