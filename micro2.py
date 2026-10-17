"""PLAN2 goal A, microscope 1: which half of the low-digit system kills the remaining family F?
For each sieve survivor n (F, from search3.candidates), count j in [4, n/2] satisfying the low-digit
congruences from
   H01 : n and n-1 only        (drop the n-2 conditions)
   H02 : n and n-2 only        (drop the n-1 conditions)
   H012: all three             (should be empty, as found before)
"Constrained" prime powers: p^e || n-k with p >= 5, or 3^b with b >= 2.
Usage: python micro2.py Y
"""
import sys
from sympy import factorint
from search3 import candidates

def conds_of(n):
    out = {0: [], 1: [], 2: []}
    for k in (0, 1, 2):
        for p, e in factorint(n - k).items():
            if p >= 5 or (p == 3 and e >= 2):
                out[k].append((p ** e, k))
    return out

def crt_js(conds, jmax):
    sols, M = [0], 1
    for q, k in sorted(conds, key=lambda c: -c[0]):
        inv = pow(M, -1, q); new = []
        for r0 in sols:
            for t in range(k + 1):
                new.append(r0 + M * (((t - r0) * inv) % q))
        M *= q
        sols = [x for x in new if x <= jmax] if M > jmax else new
    return [j for j in (x + M * s for x in sols for s in range(max(0, (jmax - x) // M) + 1)) if 4 <= j <= jmax]

def main(Y):
    stats = {'H01': [], 'H02': [], 'H012': []}; tot = 0
    for n in sorted(candidates(Y, False)):
        tot += 1
        c = conds_of(n); jmax = n // 2
        for name, ks in (('H01', (0, 1)), ('H02', (0, 2)), ('H012', (0, 1, 2))):
            js = crt_js([x for k in ks for x in c[k]], jmax)
            if js: stats[name].append((n, len(js), js[:3]))
    print(f"Y={Y:.0e}: {tot} survivors")
    for k, v in stats.items():
        print(f"  {k}: {len(v)} n with solutions; first {v[:8]}")

if __name__ == "__main__":
    main(int(float(sys.argv[1])))
