"""PLAN2: the P-reformulation of the low-digit system, and a fast exact test per n.

Setting (mode 'real' = Theorem 2: big part B includes 3^b when b >= 2; mode 'no3' = Lemma 1: big part A, primes >= 5 only).
Write n = N*B0, n-1 = N1*B1, n-2 = N2*B2 (N* = small {2,3}-parts per mode). If j = c*B0 satisfies the low-digit
system (necessary for a counterexample / near-miss), then
   P := c(N-c)/B1 is a positive integer,  Delta := N - 2c > 0,  Delta^2 = N^2 - 4*P*B1,
and for every prime power q || B2:  P ≡ 0  or  P ≡ N1 * B0^{-2}  (mod q).
Also 1 <= P <= N^2/(4*B1).
So: factor B2 only, enumerate P by CRT over the 2^w residue choices, keep P in range, test that N^2 - 4*P*B1 is a
perfect square, then recover c = (N - Delta)/2 and run the exact low-digit check for j = c*B0.
Usage: python ptest.py control      (positive control: (162,70) in mode no3; compare with brute force for n <= 3000)
       python ptest.py pure A       (n = 2^a and 3*2^a, a <= A, mode real)
"""
import sys, math, time
from sympy import factorint

def split(x, mode):
    """return (small part, big part, list of (p, p^e) in big part)"""
    f = factorint(x); small = 1; big = []
    for p, e in f.items():
        if p >= 5 or (mode == 'real' and p == 3 and e >= 2): big.append((p, p ** e))
        else: small *= p ** e
    return small, x // small, big

def lowdigit_ok(n, j, mode):
    for k in (0, 1, 2):
        _, _, big = split(n - k, mode)
        for p, q in big:
            if j % q > k: return False
    return True

def ptest(n, mode, big2=None):
    """return list of j (4 <= j < n/2) passing the full low-digit system, found via the P-reformulation."""
    N, B0, _ = split(n, mode)
    N1, B1, _ = split(n - 1, mode)
    if big2 is None:
        N2, B2, big2 = split(n - 2, mode)
    if N < 3: return []
    Pmax = N * N // (4 * B1)
    if Pmax < 1: return []
    # CRT over residues {0, N1*B0^-2} mod each q
    sols, M = [0], 1
    for p, q in big2:
        t = (N1 * pow(B0 * B0, -1, q)) % q
        invM = pow(M, -1, q); new = []
        for r0 in sols:
            for r in {0, t}:
                new.append(r0 + M * (((r - r0) * invM) % q))
        M *= q
        sols = [x for x in new if x <= Pmax] if M > Pmax else new
    Ps = sorted({x + M * s for x in sols for s in range(max(0, (Pmax - x) // M) + 1)})
    out = []
    for P in Ps:
        if P < 1: continue
        D2 = N * N - 4 * P * B1
        if D2 <= 0: continue
        D = math.isqrt(D2)
        if D * D != D2 or (N - D) % 2: continue
        c = (N - D) // 2
        j = c * B0
        if 4 <= j and 2 * j < n and lowdigit_ok(n, j, mode):
            out.append(j)
    return out

def control():
    print("(162,70) via ptest no3:", ptest(162, 'no3'))
    # brute-force comparison of the low-digit system, n <= 3000, both modes
    for mode in ('no3', 'real'):
        mism = []
        for n in range(12, 3001):
            brute = [j for j in range(4, (n + 1) // 2) if 2 * j < n and lowdigit_ok(n, j, mode)]
            fast = ptest(n, mode)
            if sorted(brute) != sorted(fast): mism.append((n, brute, fast))
        print(f"mode {mode}: n<=3000 mismatches {len(mism)} {mism[:5]}")

def pure(A):
    t0 = time.time(); found = []
    for a in range(2, A + 1):
        for m in (1, 3):
            n = m * 2 ** a
            if n < 12: continue
            js = ptest(n, 'real')
            if js: found.append((a, m, js)); print("SOLUTION?", a, m, js, flush=True)
        if a % 10 == 0: print(f"  a<={a} done {time.time()-t0:.0f}s, found {found}", flush=True)
    print(f"pure n=2^a,3*2^a, a<={A}: solutions {found} ({time.time()-t0:.0f}s)")

if __name__ == "__main__":
    if sys.argv[1] == 'control': control()
    else: pure(int(sys.argv[2]))
