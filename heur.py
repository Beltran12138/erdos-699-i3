"""PLAN2 goal A: quantitative heuristic for the remaining family F (tightened Theorem 2 (g)).
Each prime power of B1 tags c with 0 or N'; each prime power of B2 tags c with 0, N'/2 or N'. CRT gives c mod B1*B2,
and c must lie in (0, N'/2). Treating each tag pattern as a uniformly random residue, the expected number of
solutions at n is
   T(n) = 2^w(B1) * 3^w(B2) * (N'/2) / (B1*B2).
We sum T over n in F up to Y (factoring n-1 and n-2) and report the partial sums by decade, which lets us
extrapolate the tail beyond the verified range.
Usage: python heur.py Y
"""
import sys, math
from sympy import factorint

def v(x, p):
    k = 0
    while x % p == 0: x //= p; k += 1
    return k

def Np(x): return 2 ** v(x, 2) * (3 if v(x, 3) == 1 else 1)

def in_F(n):
    if n % 4: return False
    P = (n - 1) * (n - 2)
    return 3 * P * P < Np(n) ** 6

def big_omega(x):
    s = Np(x); B = x // s
    return B, len(factorint(B)) if B > 1 else 0

def main(Y):
    dec = {}; tot = 0.0; cnt = 0
    a = 2
    while 2 ** a <= Y:
        P2 = 2 ** a
        for m in range(1, min(Y // P2, 4 * int(2 ** (a / 2)) + 3) + 1, 2):
            n = P2 * m
            if n < 12 or not in_F(n): continue
            cnt += 1
            B1, w1 = big_omega(n - 1); B2, w2 = big_omega(n - 2)
            T = (2 ** w1) * (3 ** w2) * (Np(n) / 2) / (B1 * B2)
            d = len(str(n)) - 1
            dec[d] = dec.get(d, 0.0) + T; tot += T
        a += 1
    print(f"Y={Y:.0e}: |F|={cnt}, expected solutions (heuristic) total {tot:.3e}")
    for d in sorted(dec): print(f"  n in [1e{d}, 1e{d+1}): {dec[d]:.3e}")

if __name__ == "__main__":
    main(int(float(sys.argv[1])))
