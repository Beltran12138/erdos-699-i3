"""PLAN2 goal B: n = 2^a and n = 3*2^a, via the P-reformulation (mode 'real', B0 = 1).

Only the factorisation of n-2 is needed. For n = 2^a, n-2 = 2(2^(a-1)-1) is split into cyclotomic values Phi_d(2).
For n = 3*2^a, n-2 = 2(3*2^(a-1)-1) is factored directly. Each piece gets a time limit. A composite cofactor C that
stays unfactored is still used soundly: every prime power of C divides P or P*B0^2 - N1, so C | P*(P*B0^2 - N1).
Verdict per n: EXCLUDED (no P survives), SOLUTION? (a j passes the exact low-digit check), or UNDETERMINED
(too many P candidates because the factored part is too small, or the final check could not factor).
Usage: python pure2.py A [timeout_per_piece_s]
"""
import sys, math, time, multiprocessing as mp
from sympy import factorint, cyclotomic_poly, divisors, isprime

def _fac(x, q):
    q.put(factorint(x))

def factor_timed(x, tmax):
    """full factorisation dict, or (partial dict, cofactor) if time runs out."""
    if x == 1: return {}, 1
    if isprime(x): return {x: 1}, 1
    q = mp.Queue(); pr = mp.Process(target=_fac, args=(x, q)); pr.start(); pr.join(tmax)
    if pr.is_alive():
        pr.terminate(); pr.join()
        f = factorint(x, limit=10 ** 6)          # trial division part only
        rest = x
        known = {}
        for p, e in f.items():
            if isprime(p):
                known[p] = e; rest //= p ** e
        return known, rest
    return q.get(), 1

def v(x, p):
    k = 0
    while x % p == 0: x //= p; k += 1
    return k

def small_big(x):
    """real mode: small part = 2^v2 * 3^[v3=1]"""
    s = 2 ** v(x, 2) * (3 if v(x, 3) == 1 else 1)
    return s, x // s

def analyse(n, pieces, tmax, cap=10 ** 6):
    """pieces: list of integers whose product is the odd part of n-2 (with multiplicity merged later)."""
    N, B0 = small_big(n); N1, B1 = small_big(n - 1)
    fac = {}; cof = 1
    for x in pieces:
        f, r = factor_timed(x, tmax)
        for p, e in f.items(): fac[p] = fac.get(p, 0) + e
        cof *= r
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
    if count > cap:
        return 'UNDETERMINED', f'{count} P candidates (factored part too small; cofactor {cof.bit_length()} bits)'
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
    if not hits:
        return 'EXCLUDED', f'{len(big2)} prime powers, cofactor {cof.bit_length()} bits'
    return 'SOLUTION?', str(hits[:5])        # to be checked exactly by hand

def main(A, tmax):
    t0 = time.time(); res = {'EXCLUDED': 0, 'UNDETERMINED': [], 'SOLUTION?': []}
    for a in range(4, A + 1):
        # n = 2^a : odd part of n-2 is 2^(a-1)-1 = prod_{d | a-1, d > 1} Phi_d(2)
        n = 2 ** a
        pieces = [int(cyclotomic_poly(d, 2)) for d in divisors(a - 1) if d > 1]
        vr, info = analyse(n, pieces, tmax)
        # n = 3*2^a : odd part of n-2 is 3*2^(a-1)-1
        vr3, info3 = analyse(3 * n, [3 * 2 ** (a - 1) - 1], tmax)
        for tag, verdict, inf in (('2^a', vr, info), ('3*2^a', vr3, info3)):
            if verdict == 'EXCLUDED': res['EXCLUDED'] += 1
            else:
                res[verdict].append((a, tag, inf)); print(verdict, a, tag, inf, flush=True)
        if a % 10 == 0:
            print(f"  a<={a}: excluded {res['EXCLUDED']}, undetermined {len(res['UNDETERMINED'])}, solution? {len(res['SOLUTION?'])}  {time.time()-t0:.0f}s", flush=True)
    print(f"A={A}: excluded {res['EXCLUDED']}; undetermined {res['UNDETERMINED']}; solution? {res['SOLUTION?']} ({time.time()-t0:.0f}s)")

if __name__ == "__main__":
    main(int(sys.argv[1]), float(sys.argv[2]) if len(sys.argv) > 2 else 30)
