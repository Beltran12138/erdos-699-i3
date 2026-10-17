# Independent check: direct gcd of binomials, no Lucas, no pruning.
import sys
from math import comb, gcd
N = int(sys.argv[1]); half = '--half' in sys.argv; mode = sys.argv[2]
def strip(g, ps):
    for p in ps:
        while g % p == 0: g //= p
    return g
out = []
for n in range(12, N + 1):
    c3 = comb(n, 3); jmax = n // 2 if half else (n - 1) // 2
    for j in range(6, jmax + 1):
        g = gcd(c3, comb(n, j))
        if strip(g, (2,) if mode == 'full' else (2, 3)) == 1:
            out.append((n, j))
print(mode, half, N, out)
