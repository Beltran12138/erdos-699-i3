"""PLAN3 data: on the H01 relaxation (conditions from n and n-1 only, which do have solutions in F), record
B0, N', c and the cofactor P1 = c(N'-c)/B1 (it must be an integer there).  If Thue-Mahler-style finiteness
were reachable by bounding the cofactor, P1 and B0 would stay in a finite set; we check whether they grow with N'."""
import math
from micro2 import conds_of, crt_js
from search3 import candidates
from pure2 import small_big
rows = []
for n in sorted(candidates(10**10, False)):
    c = conds_of(n); js = crt_js(c[0] + c[1], n // 2)
    N, B0 = small_big(n); N1, B1 = small_big(n - 1)
    for j in js:
        cc = j // B0
        P1 = cc * (N - cc) // B1
        assert cc * (N - cc) % B1 == 0
        rows.append((n, N, B0, cc, P1, round(cc / N, 4)))
rows.sort(key=lambda r: r[1])
print("H01 solutions:", len(rows))
for r in rows[:6] + rows[len(rows)//2 - 3: len(rows)//2 + 3] + rows[-6:]:
    print("  n=%d N'=%d B0=%d c=%d P1=%d x=c/N'=%s" % r)
import collections
byN = collections.defaultdict(list)
for r in rows: byN[len(str(r[1]))].append(r)
for d in sorted(byN):
    rs = byN[d]
    print(f"  N' with {d} digits: {len(rs)} sols, P1 range {min(r[4] for r in rs)}..{max(r[4] for r in rs)}, B0 range {min(r[2] for r in rs)}..{max(r[2] for r in rs)}")
