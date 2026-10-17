"""Compare the float sieve in search3.py with an exact-integer version (squared inequalities, no sqrt).
Exact forms:  Lemma 1'(f): 108*((n-1)(n-2))^2 <= (N1*N2)^2 * N0^6 ; Lemma 1' N1=1: 4(n-1) <= N0^2
              Thm 2: M1=1: 4(n-1) <= M0^2 ;  else 3*((n-1)(n-2))^2 <= M0^6
Reports candidates kept by exact but dropped by float (these would be a soundness gap)."""
import sys
from search3 import N23, Np, sieve_ok
def exact_ok(n):
    if n % 4: return False
    N0, N1, N2 = N23(n), N23(n - 1), N23(n - 2)
    P = (n - 1) * (n - 2)
    if not (108 * P * P <= (N1 * N2) ** 2 * N0 ** 6 and (N1 != 1 or 4 * (n - 1) <= N0 ** 2)): return False
    M0, M1 = Np(n), Np(n - 1)
    return (4 * (n - 1) <= M0 * M0) if M1 == 1 else (3 * P * P <= M0 ** 6)
Y = int(float(sys.argv[1])); a = 2; ke = kf = 0; gap = []; extra = []
while 2 ** a <= Y:
    P2 = 2 ** a
    for m in range(1, min(Y // P2, 3 * P2) + 1, 2):
        n = P2 * m
        if n < 12: continue
        e, f = exact_ok(n), sieve_ok(n)
        ke += e; kf += f
        if e and not f: gap.append(n)
        if f and not e: extra.append(n)
    a += 1
print(f"Y={Y:.0e}: exact {ke}, float {kf}, kept-by-exact-dropped-by-float {len(gap)} {gap[:10]}, float-only {len(extra)}")
