"""Exhaustive check of Erdős #699 at i = 3 for all n <= Y, using Lemma 1' and Theorem 2 as a sieve on n.

Sieve (necessary conditions for a counterexample with 6 <= j < n/2), computed from v2, v3 only:
  Lemma 1'  : with N = {2,3}-part, (n-1)(n-2) <= N(n-1)N(n-2)N(n)^3/(6*sqrt3), and N(n-1)=1 => n-1 <= N(n)^2/4
  Theorem 2 : 4 | n; with N' = 2-part * (3 if 3 || x),
              N'(n-1)=1 => n-1 <= N'(n)^2/4,  else sqrt3*(n-1)(n-2) <= N'(n)^3
For every surviving n, ALL j in [4, n/2] are tested exactly (no use of the lemmas):
  constrained primes = p >= 5 dividing n(n-1)(n-2), and 3 if 9 | n(n-1)(n-2) [then 3 | C(n,3)];
  j is enumerated along the largest constrained prime power q (j mod q <= k), then full Lucas for every constrained prime.
Output: counterexamples (G a power of 2) and near-misses ignoring 3.
Usage: python search3.py Y [--nosieve]   (--nosieve: test every n, for control runs)
"""
import sys, time, math
from sympy import factorint

S3 = math.sqrt(3); K = 6 * S3

def v(x, p):
    k = 0
    while x % p == 0: x //= p; k += 1
    return k

def N23(x): return 2 ** v(x, 2) * 3 ** v(x, 3)
def Np(x):  return 2 ** v(x, 2) * (3 if v(x, 3) == 1 else 1)

def sieve_ok(n):
    if n % 4: return False
    N0, N1, N2 = N23(n), N23(n - 1), N23(n - 2)
    if not ((n - 1) * (n - 2) * K <= N1 * N2 * N0 ** 3 and (N1 != 1 or 4 * (n - 1) <= N0 ** 2)):
        return False
    M0, M1 = Np(n), Np(n - 1)
    return (4 * (n - 1) <= M0 * M0) if M1 == 1 else (S3 * (n - 1) * (n - 2) <= M0 ** 3)

def lucas_ok(n, j, p):
    while j:
        if j % p > n % p: return False
        j //= p; n //= p
    return True

def test_n(n):
    """returns (counterexamples, near_misses_ignoring_3) as lists of j in [4, n/2]"""
    conds = []
    for k in (0, 1, 2):
        for p, e in factorint(n - k).items():
            if p >= 5: conds.append((p, p ** e, k))
            elif p == 3 and e >= 2: conds.append((3, 3 ** e, k))
    jmax = n // 2
    ce, nm = [], []
    big = [c for c in conds if c[0] >= 5]
    # all j satisfying the low-digit congruences j mod q in {0..k} for every big prime power, via CRT
    if big:
        sols, M = [0], 1
        for _, q, k in sorted(big, key=lambda c: -c[1]):
            inv = pow(M, -1, q)
            new = []
            for r0 in sols:
                for t in range(k + 1):
                    x = r0 + M * (((t - r0) * inv) % q)       # x ≡ r0 (mod M), x ≡ t (mod q)
                    new.append(x)
            M *= q
            sols = [x for x in new if x <= jmax] if M > jmax else new
        js = sorted(x + M * s for x in sols for s in range(max(0, (jmax - x) // M) + 1))
    else:
        js = range(4, jmax + 1)
    for j in js:
        if j < 4 or j > jmax: continue
        if all(lucas_ok(n, j, p) for p, _, _ in big):
            nm.append(j)
            if all(lucas_ok(n, j, p) for p, _, _ in conds if p == 3):
                ce.append(j)
    return ce, nm

def candidates(Y, nosieve):
    if nosieve:
        yield from range(12, Y + 1); return
    a = 2
    while 2 ** a <= Y:
        P = 2 ** a
        mmax = min(Y // P, 3 * P)             # Theorem 2 forces m = n/2^a well below 3*2^a; exact test below
        for m in range(1, mmax + 1, 2):
            n = P * m
            if n >= 12 and sieve_ok(n): yield n
        a += 1

def main(Y, nosieve):
    t0 = time.time(); cnt = 0; CE = []; NM = []
    for n in sorted(candidates(Y, nosieve)):
        cnt += 1
        ce, nm = test_n(n)
        for j in ce:
            CE.append((n, j)); print("COUNTEREXAMPLE?", n, j, flush=True)
        for j in nm:
            NM.append((n, j))
        if cnt % 20000 == 0:
            print(f"  {cnt} n tested, last n={n:,}, CE {len(CE)}, NM {NM[-3:]} {time.time()-t0:.0f}s", flush=True)
    print(f"Y={Y:,} nosieve={nosieve}: tested {cnt} n; counterexamples {CE}; near-misses(no prime>=5 shared, j in [4,n/2]) {NM[:40]} ({len(NM)}) ({time.time()-t0:.0f}s)")

if __name__ == "__main__":
    main(int(float(sys.argv[1])), '--nosieve' in sys.argv)
