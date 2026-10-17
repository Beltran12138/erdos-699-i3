"""Microscope for Erdős #699 at i = 3.

Exact criterion (Lucas): an odd prime p divides C(n,j) iff some base-p digit of j exceeds that of n.
The odd primes dividing C(n,3) = n(n-1)(n-2)/6 are: every p >= 5 dividing n(n-1)(n-2), and p = 3 iff
v3(n(n-1)(n-2)) >= 2. So G = gcd(C(n,3), C(n,j)) is a power of 2 iff every such p fails to divide C(n,j).

Pruning: if p^e || (n-k), p >= 5, then n ≡ k (mod p^e), so Lucas forces j mod p^e ∈ {0..k}.
We enumerate j only along the largest such prime power q, then test all conditions exactly.

Modes: 'full'  = real counterexamples (prime 3 also counts);
       'no3'   = near-misses where no prime >= 5 is shared (G = 2^a 3^b);
j range: 6 <= j < n/2 by default (j = 4, 5 and n = 2j are already settled); --half adds j = n/2.
Usage: python micro.py N [no3|full] [--half]
"""
import sys, time
import numpy as np

def spf_table(N):
    spf = np.zeros(N + 1, dtype=np.int32)
    spf[1] = 1
    for p in range(2, int(N ** 0.5) + 1):
        if spf[p] == 0:
            spf[p] = p
            blk = spf[p * p::p]
            blk[blk == 0] = p
    z = np.nonzero(spf == 0)[0]
    spf[z] = z
    return spf

def factor(x, spf):
    f = {}
    while x > 1:
        p = int(spf[x]); e = 0
        while x % p == 0:
            x //= p; e += 1
        f[p] = e
    return f

def digits_ok(n, j, p):
    """True iff p does NOT divide C(n,j), i.e. every base-p digit of j <= that of n."""
    while j:
        if j % p > n % p:
            return False
        j //= p; n //= p
    return True

def main(N, mode, half):
    t0 = time.time()
    spf = spf_table(N)
    print(f"spf table to {N:,} in {time.time() - t0:.1f}s", flush=True)
    hits = []
    cand_total = 0
    for n in range(12, N + 1):
        conds = []          # (p, q=p^e, k)
        primes = set()
        v3 = 0
        for k in (0, 1, 2):
            for p, e in factor(n - k, spf).items():
                if p >= 5:
                    conds.append((p, p ** e, k)); primes.add(p)
                elif p == 3:
                    v3 += e
        if mode == 'full' and v3 >= 2:
            primes.add(3)
        jmax = n // 2 if half else (n - 1) // 2
        if conds:
            p0, q, k0 = max(conds, key=lambda c: c[1])
            js = (r + q * s for s in range(jmax // q + 1) for r in range(k0 + 1))
        else:
            js = range(6, jmax + 1)
        for j in js:
            if j < 6 or j > jmax:
                continue
            cand_total += 1
            if all(digits_ok(n, j, p) for p in primes):
                hits.append((n, j))
                if len(hits) <= 40:
                    print(f"HIT n={n} j={j}  n={factor(n, spf)} n-1={factor(n - 1, spf)} n-2={factor(n - 2, spf)}", flush=True)
        if n % 1_000_000 == 0:
            print(f"  n<={n:,} hits {len(hits)} candidates {cand_total:,} {time.time() - t0:.0f}s", flush=True)
    print(f"mode={mode} half={half} N={N:,}: {len(hits)} hits, {cand_total:,} candidates, {time.time() - t0:.0f}s")
    return hits

if __name__ == "__main__":
    N = int(float(sys.argv[1]))
    mode = sys.argv[2] if len(sys.argv) > 2 else 'no3'
    main(N, mode, '--half' in sys.argv)
