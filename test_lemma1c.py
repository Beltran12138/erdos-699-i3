"""Claim (c) of Lemma 1 on relaxation R0'': congruences from n and n-2 only (p >= 5).
Claim: A2 | lcm(c, N0-c, N0-2c).  Negative control (deliberately wrong): A2 | lcm(c, N0-c)."""
import sys, math
from micro import spf_table, factor

N = int(float(sys.argv[1])); spf = spf_table(N)

def parts(x):
    f = factor(x, spf); s = 1
    for p, e in f.items():
        if p < 5: s *= p ** e
    return s, x // s, [p ** e for p, e in f.items() if p >= 5]

def lcm(*a):
    r = 1
    for x in a: r = r * x // math.gcd(r, x)
    return r

cnt = bad = neg = 0
for n in range(12, N + 1):
    N0, A0, _ = parts(n); N2, A2, q2 = parts(n - 2)
    for j in range(A0, (n - 1) // 2 + 1, A0):
        if j < 6 or not all(j % q <= 2 for q in q2): continue
        cnt += 1; c = j // A0
        if lcm(c, N0 - c, N0 - 2 * c) % A2: bad += 1; print("FAIL", n, j)
        if lcm(c, N0 - c) % A2: neg += 1
print(f"R0'' N={N}: solutions {cnt}, claim (c) failures {bad}, negative-control failures {neg}")
