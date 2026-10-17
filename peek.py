# Necessary condition for an i=3 counterexample to #699 (Bloom's observation):
# if V = odd part of C(n,3) is coprime to C(n,j), then V | C(j,3).
# Count (n,j), 5<j<n/2, satisfying V | C(j,3); then check which are actual counterexamples (gcd a power of 2).
import sys
from math import comb, gcd
N = int(sys.argv[1])
def odd(x):
    while x % 2 == 0: x //= 2
    return x
nec = full = 0; ex = []
for n in range(12, N + 1):
    V = odd(comb(n, 3))
    for j in range(6, (n + 1) // 2):          # j < n/2 (n = 2j already settled)
        if comb(j, 3) % V == 0:
            nec += 1
            g = gcd(comb(n, 3), comb(n, j))
            if odd(g) == 1:
                full += 1
            if len(ex) < 12: ex.append((n, j, odd(g)))
print(f"n<={N}: necessary-condition pairs {nec}, actual counterexamples {full}; first: {ex}")
