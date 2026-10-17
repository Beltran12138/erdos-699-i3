"""Phase 2: exhaustive search of near-misses parametrised by Lemma 1.

Near-miss = (n, j) with 6 <= j < n/2 and no prime p >= 5 dividing both C(n,3) and C(n,j).
Lemma 1: with N0 = {2,3}-part of n, A0 = n / N0, j = c*A0 (1 <= c < N0/2), and
   either  n - 1 = A1  divides L1 = lcm(c, N0-c)                     (case N1 = 1)
   or      n - 2 = N2*A2 with N2 in {1,2}, A2 | L2 = lcm(c, N0-c, N0-2c).
So for each {2,3}-number N0 <= X and each c, every near-miss with this (N0, c) has
   n - 1 = d (d | L1)   or   n - 2 = d or 2d (d | L2),  d coprime to 6.
Enumerating these covers ALL near-misses whose {2,3}-part is <= X (hence all n <= X, and much larger n).

For each candidate we report:
  R1  = low-digit congruences hold (j mod p^e <= k for p^e || n-k, p >= 5)   [positive control: (162,70)]
  NM  = full Lucas for all p >= 5 (near-miss)
  CE  = additionally 3 does not divide gcd (real counterexample to #699 at i=3)
Usage: python search2.py X
"""
import sys, time, math

def smooth23(X):
    out = []
    a = 1
    while a <= X:
        b = a
        while b <= X:
            out.append(b); b *= 3
        a *= 2
    return sorted(out)

def factor(x):
    f = {}
    d = 2
    while d * d <= x:
        while x % d == 0:
            f[d] = f.get(d, 0) + 1; x //= d
        d += 1 if d == 2 else 2
    if x > 1: f[x] = f.get(x, 0) + 1
    return f

def part23(x):
    s = 1
    while x % 2 == 0: x //= 2; s *= 2
    while x % 3 == 0: x //= 3; s *= 3
    return s

def divisors_from(f):
    ds = [1]
    for p, e in f.items():
        ds = [d * p ** k for d in ds for k in range(e + 1)]
    return ds

def lucas_ok(n, j, p):
    while j:
        if j % p > n % p: return False
        j //= p; n //= p
    return True

def check(n, j):
    """returns (R1, NM, CE) flags"""
    r1 = nm = True
    v3 = 0
    for k in (0, 1, 2):
        for p, e in factor(n - k).items():
            if p == 3: v3 += e
            if p < 5: continue
            if j % (p ** e) > k: r1 = False
            if not lucas_ok(n, j, p): nm = False
    ce = nm and not (v3 >= 2 and not lucas_ok(n, j, 3))
    return r1, nm, ce

def main(X):
    t0 = time.time()
    seen = set(); stats = {'cand': 0, 'R1': [], 'NM': [], 'CE': []}
    fcache = {}
    def fac(x):
        if x not in fcache: fcache[x] = factor(x)
        return fcache[x]
    for N0 in smooth23(X):
        if N0 < 3: continue
        for c in range(1, (N0 + 1) // 2):
            if 2 * c >= N0: break
            f1, f2, f3 = fac(c), fac(N0 - c), fac(N0 - 2 * c)
            L = {}
            for f in (f1, f2, f3):
                for p, e in f.items():
                    if p >= 5: L[p] = max(L.get(p, 0), e)
            L1 = {}
            for f in (f1, f2):
                for p, e in f.items():
                    if p >= 5: L1[p] = max(L1.get(p, 0), e)
            ns = set()
            for d in divisors_from(L1): ns.add(d + 1)
            for d in divisors_from(L): ns.add(d + 2); ns.add(2 * d + 2)
            for n in ns:
                if n % N0 or part23(n) != N0: continue
                j = c * (n // N0)
                if j < 6 or 2 * j >= n: continue
                if (n, j) in seen: continue
                seen.add((n, j)); stats['cand'] += 1
                # cheap pre-filter (Lemma 1): rough parts of n-1, n-2 must be built from primes of L
                ok = True
                for k in (1, 2):
                    x = (n - k) // part23(n - k)
                    for p in L:
                        while x % p == 0: x //= p
                    if x != 1: ok = False; break
                if not ok: continue
                stats.setdefault('pre', 0); stats['pre'] += 1
                r1, nm, ce = check(n, j)
                if r1: stats['R1'].append((n, j, N0, c))
                if nm: stats['NM'].append((n, j, N0, c))
                if ce: stats['CE'].append((n, j, N0, c)); print("COUNTEREXAMPLE?", n, j, N0, c, flush=True)
        if N0 > 1000:
            print(f"  N0={N0} done, cand {stats['cand']}, R1 {len(stats['R1'])}, NM {len(stats['NM'])} {time.time()-t0:.0f}s", flush=True)
    print(f"X={X}: candidates {stats['cand']}; R1 {stats['R1'][:30]}; NM {stats['NM'][:30]}; CE {stats['CE']} ({time.time()-t0:.0f}s)")

if __name__ == "__main__":
    main(int(float(sys.argv[1])))
