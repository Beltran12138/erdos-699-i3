"""Re-run the UNDETERMINED cases of pure2.py with
  (1) a higher candidate cap, and
  (2) factorisations of the odd part of n-2 taken from factordb.com (public, read-only). Each one is verified
      locally: the product must equal the number, and every factor must pass sympy.isprime (BPSW); a factor that
      factordb reports as composite is kept as an unfactored cofactor, which is still used soundly.
Input: pure2 log lines "UNDETERMINED a tag ...". Usage: python resolve.py pure2_300.log [cap]
"""
import sys, json, math, subprocess, time
from sympy import isprime, factorint, cyclotomic_poly, divisors
import pure2

def factordb(N):
    out = subprocess.run(["curl", "-s", "-m", "60", f"http://factordb.com/api?query={N}"],
                         capture_output=True, text=True).stdout
    d = json.loads(out)
    fac = {}; cof = 1; prod = 1
    for p, e in d["factors"]:
        p = int(p); e = int(e); prod *= p ** e
        if isprime(p): fac[p] = fac.get(p, 0) + e
        else: cof *= p ** e
    assert prod == N, "factordb product mismatch"
    return fac, cof, d.get("status")

def analyse_fac(n, fac, cof, cap):
    N, B0 = pure2.small_big(n); N1, B1 = pure2.small_big(n - 1)
    big2 = [(p, p ** e) for p, e in fac.items() if p >= 5 or (p == 3 and e >= 2)]
    Pmax = N * N // (4 * B1)
    sols, M = [0], 1
    for p, q in big2:
        t = (N1 * pow(B0 * B0, -1, q)) % q
        invM = pow(M, -1, q); new = []
        for r0 in sols:
            for r in {0, t}:
                new.append(r0 + M * (((r - r0) * invM) % q))
        M *= q
        sols = [x for x in new if x <= Pmax] if M > Pmax else new
    count = sum(max(0, (Pmax - x) // M) + 1 for x in sols)
    if count > cap: return 'UNDETERMINED', f'{count} candidates, cofactor {cof.bit_length()} bits'
    hits = []
    for x in sols:
        for s in range(max(0, (Pmax - x) // M) + 1):
            P = x + M * s
            if P < 1: continue
            if cof > 1 and (P * (P * B0 * B0 - N1)) % cof: continue
            D2 = N * N - 4 * P * B1
            if D2 <= 0: continue
            D = math.isqrt(D2)
            if D * D == D2 and (N - D) % 2 == 0:
                c = (N - D) // 2; j = c * B0
                if 4 <= j and 2 * j < n: hits.append((P, j))
    return ('EXCLUDED', f'{len(big2)} prime powers, cofactor {cof.bit_length()} bits') if not hits else ('SOLUTION?', str(hits[:5]))

def main(log, cap):
    cases = []
    for line in open(log):
        if line.startswith("UNDETERMINED"):
            _, a, tag = line.split()[:3]; cases.append((int(a), tag))
    for a, tag in cases:
        n = 2 ** a if tag == '2^a' else 3 * 2 ** a
        odd = (n - 2) // 2
        if tag == '2^a':
            fac = {}; cof = 1
            for d in divisors(a - 1):
                if d == 1: continue
                f, r = pure2.factor_timed(int(cyclotomic_poly(d, 2)), 120)
                for p, e in f.items(): fac[p] = fac.get(p, 0) + e
                cof *= r
            src = 'local'
            if cof > 1:
                fac2, cof2, st = factordb(odd); fac, cof, src = fac2, cof2, f'factordb:{st}'
        else:
            fac, cof, st = factordb(odd); src = f'factordb:{st}'
        assert math.prod(p ** e for p, e in fac.items()) * cof == odd
        vr, info = analyse_fac(n, fac, cof, cap)
        print(a, tag, src, vr, info, flush=True)
        time.sleep(1)

if __name__ == "__main__":
    main(sys.argv[1], int(float(sys.argv[2])) if len(sys.argv) > 2 else 10 ** 8)
