"""Test the intermediate claims of Lemma 1 on a weaker relaxation that has many solutions.
R0: keep only the congruences from n and n-1 (p >= 5):  p^e || n  => p^e | j ;  p^e || n-1 => j mod p^e in {0,1}.
Claims to test on every R0 solution (6 <= j < n/2):
  (a) A0 | j, so j = c*A0 with 1 <= c < N0/2
  (b) A1 | lcm(c, N0 - c)
and on every R1 solution (all three numbers) additionally
  (c) A2 | lcm(c, N0-c, N0-2c)   and   (d) N0^3 >= 3*sqrt(3)*(n-2)
Negative control: claim (b') A1 | c  (deliberately wrong) must fail somewhere."""
import sys, math
from micro import spf_table, factor
N = int(float(sys.argv[1])); spf = spf_table(N)
def parts(x):
    f = factor(x, spf); s = 1
    for p, e in f.items():
        if p < 5: s *= p ** e
    return s, x // s, [(p ** e) for p, e in f.items() if p >= 5]
def lcm(*a):
    r = 1
    for x in a: r = r * x // math.gcd(r, x)
    return r
cnt0 = cnt1 = bad = badneg = 0
for n in range(12, N + 1):
    N0, A0, q0 = parts(n); N1, A1, q1 = parts(n - 1); N2, A2, q2 = parts(n - 2)
    jmax = (n - 1) // 2
    step = A0 if A0 > 1 else 1
    for j in range(step, jmax + 1, step):          # R0 forces A0 | j; brute over multiples
        if j < 6 or not all(j % q <= 1 for q in q1): continue
        cnt0 += 1
        c = j // A0
        if not (j % A0 == 0 and 1 <= c and 2 * c < N0): bad += 1; print("FAIL a", n, j)
        if lcm(c, N0 - c) % A1: bad += 1; print("FAIL b", n, j)
        if c % A1: badneg += 1
        if all(j % q <= 2 for q in q2):
            cnt1 += 1
            if lcm(c, N0 - c, N0 - 2 * c) % A2: bad += 1; print("FAIL c", n, j)
            if N0 ** 3 < 3 * math.sqrt(3) * (n - 2): bad += 1; print("FAIL d", n, j)
print(f"N={N}: R0 solutions {cnt0}, R1 solutions {cnt1}, claim failures {bad}, negative-control failures {badneg}")
