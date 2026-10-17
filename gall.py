"""Clean conjecture, all n (no sieve): g(t) = t(t-1)(t-2), V(n) = big part of n(n-1)(n-2)
(primes >= 5, and 3^b when b >= 2). List every (n, j) with 3 <= j < n/2 and V(n) | g(j), for n <= Y.
Roots of g mod p^e (p >= 5): 0, 1, 2; mod 3^b: brute force. CRT with early size pruning.
n whose CRT tree exceeds `cap` are deferred and re-run at the end with no cap (largest prime powers first,
so the modulus passes n/2 quickly and the candidate list stays small).
Usage: python gall.py Y [cap]
"""
import sys, time, math
from micro import spf_table, factor

R3 = {}
def roots_mod(q, p):
    if p >= 5: return (0, 1, 2)
    if q not in R3: R3[q] = tuple(t for t in range(q) if (t * (t - 1) * (t - 2)) % q == 0)
    return R3[q]

def solve(n, spf, cap):
    pp = []
    for k in (0, 1, 2):
        for p, e in factor(n - k, spf).items():
            if p >= 5 or (p == 3 and e >= 2): pp.append((p, p ** e))
    jmax = (n - 1) // 2
    if not pp: return 'V=1'
    if cap and math.prod(len(roots_mod(q, p)) for p, q in pp) > cap: return None
    sols, M = [0], 1
    for p, q in sorted(pp, key=lambda x: -x[1]):
        rs = roots_mod(q, p); invM = pow(M, -1, q); new = []
        for r0 in sols:
            for r in rs: new.append(r0 + M * (((r - r0) * invM) % q))
        M *= q
        sols = [x for x in new if x <= jmax] if M > jmax else new
    js = [x + M * s for x in sols for s in range(max(0, (jmax - x) // M) + 1)]
    return sorted(j for j in js if 3 <= j <= jmax)

def main(Y, cap):
    t0 = time.time(); spf = spf_table(Y)
    hits = []; skipped = []
    for n in range(8, Y + 1):
        r = solve(n, spf, cap)
        if r is None: skipped.append(n); continue
        if r:
            hits.append((n, r if isinstance(r, str) else r[:6])); print("HIT", n, r if isinstance(r, str) else r[:6], flush=True)
        if n % 1_000_000 == 0:
            print(f"  n<={n:,} hits {len(hits)} deferred {len(skipped)} {time.time()-t0:.0f}s", flush=True)
    print(f"main pass done: hits {hits}; deferred {len(skipped)} ({time.time()-t0:.0f}s)", flush=True)
    for n in skipped:
        r = solve(n, spf, 0)
        if r:
            hits.append((n, r[:6])); print("HIT (deferred)", n, r[:6], flush=True)
    print(f"Y={Y:,}: hits {len(hits)}: {hits[:60]} ; deferred {len(skipped)} all re-run with no cap ({time.time()-t0:.0f}s)")

if __name__ == "__main__":
    main(int(float(sys.argv[1])), int(float(sys.argv[2])) if len(sys.argv) > 2 else 10 ** 6)
