"""Relaxation R1 of the i=3 near-miss condition: keep only the low-digit congruences
   j mod p^e in {0..k}  for every p^e || (n-k), p >= 5, k in {0,1,2}   (ignore higher digits and the prime 3).
If R1 has no solution with 6 <= j < n/2, the i=3 case (j < n/2) reduces to a pure congruence statement."""
import sys, time
from micro import spf_table, factor
N = int(float(sys.argv[1])); t0 = time.time()
spf = spf_table(N); hits = []
for n in range(12, N + 1):
    conds = []
    for k in (0, 1, 2):
        for p, e in factor(n - k, spf).items():
            if p >= 5: conds.append((p ** e, k))
    jmax = (n - 1) // 2
    if not conds:
        hits.append((n, 'nocond')); continue
    q, k0 = max(conds)
    for s in range(jmax // q + 1):
        for r in range(k0 + 1):
            j = r + q * s
            if 6 <= j <= jmax and all(j % qq <= kk for qq, kk in conds):
                hits.append((n, j))
print(f"R1 N={N:,}: {len(hits)} solutions ({time.time()-t0:.0f}s); first 40: {hits[:40]}")
