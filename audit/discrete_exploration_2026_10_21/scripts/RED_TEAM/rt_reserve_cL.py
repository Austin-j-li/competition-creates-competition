"""Red team: C8 / X_C8, the seller's reserve after the price, for c_L in {0, 0.1, 1} (print only).

Maximizes expected proceeds S(p; mu, r) over p in [0, h] by a finite candidate list
(regime boundaries, participation caps, stationary points) and by a fine grid.
Prints the optimal reserve, proceeds, entry, and the investor's purchase return
under full buying at r in {1.2, 3, 3.6} and mu in {m1, M1}, c_H = 5.
Run from the repository root with .venv/bin/python. No assertions.
"""
from mpmath import mp, mpf, exp, sqrt

mp.dps = 30
h, l, rho, cH, b, k = mpf(10), mpf(1), mpf(1) / 4, mpf(5), mpf(2), mpf(1) / 50
a = exp(-1 / b)
M1, m1 = 1 / (1 + a), a / (1 + a)


def objs(p, r):
    """(t0, tH, tL, gH, gL) at reserve p in [0, h] (paper Appendix A.7 regimes)."""
    if p <= l:
        t0 = p * (1 - p / r)
        tH = r / 2 + p ** 2 / (2 * r)
        tL = l - (l ** 2 - p ** 2) / (2 * r)
        return t0, tH, tL, h - tH, (l ** 2 - p ** 2) / (2 * r)
    if p <= r:
        t0 = p * (1 - p / r)
        tH = r / 2 + p ** 2 / (2 * r)
        return t0, tH, t0, h - tH, mpf(0)
    return mpf(0), p, mpf(0), h - p, mpf(0)


def entry(p, r, mu, cL):
    t0, tH, tL, gH, gL = objs(p, r)
    Bv = gL + mu * (gH - gL)
    return rho * (1 if Bv >= cL else 0) + (1 - rho) * (1 if Bv >= cH else 0), Bv


def proceeds(p, r, mu, cL):
    t0, tH, tL, gH, gL = objs(p, r)
    e, _ = entry(p, r, mu, cL)
    return t0 + e * (tL - t0 + mu * (tH - tL))


def cap(r, mu, c):
    """Largest p with B(p, mu) >= c, or None."""
    t0, tH, tL, gH, gL = objs(mpf(0), r)
    B0 = gL + mu * (gH - gL)
    if c > B0:
        return None
    Bl = mu * (h - objs(l, r)[1])
    Br = mu * (h - r)
    if c >= Bl:
        return sqrt(2 * r * (B0 - c))
    if c >= Br:
        return sqrt(2 * r * (h - c / mu) - r ** 2)
    return h - c / mu


def candidates(r, mu, cL):
    cands = [mpf(0), l, r, h]
    for c in (cL, cH):
        q = cap(r, mu, c)
        if q is not None:
            cands += [q, q - mpf(10) ** -12]
    for e in (rho, mpf(1)):
        if 2 - 3 * e != 0:
            cands.append(r * (1 - e) / (2 - 3 * e))          # regime I stationary point
        z = e * mu
        if 2 - 3 * z != 0:
            cands.append(r * (1 - z) / (2 - 3 * z))          # regime II stationary point
    cands.append(r / 2)                                        # no-entry regime II optimum
    cands += [l - mpf(10) ** -12, r - mpf(10) ** -12]
    return [c for c in cands if 0 <= c <= h]


def solve(r, mu, cL):
    best = max(((proceeds(c, r, mu, cL), c) for c in candidates(r, mu, cL)), key=lambda t: t[0])
    grid = max(((proceeds(mpf(i) / 200, r, mu, cL), mpf(i) / 200) for i in range(0, 2001)), key=lambda t: t[0])
    return best, grid


for cL in (mpf(0), mpf('0.1'), mpf(1)):
    print(f"\n==================== c_L = {cL} ====================")
    for rr in ('1.2', '3', '3.6'):
        r = mpf(rr)
        res = {}
        for name, mu in (('m1', m1), ('M1', M1)):
            (Sbest, pbest), (Sgrid, pgrid) = solve(r, mu, cL)
            e, Bv = entry(pbest, r, mu, cL)
            res[name] = (pbest, Sbest, e)
            print(f"r={rr} mu={name}: candidate optimum p*={mp.nstr(pbest, 10)} S={mp.nstr(Sbest, 10)} entry={mp.nstr(e, 6)} B(p*)={mp.nstr(Bv, 8)} | grid p={mp.nstr(pgrid, 6)} S={mp.nstr(Sgrid, 10)}")
        # full-buying outcome: good news prob 1/2, posteriors M1 (prob 1/2) and m1 (prob 1/2)
        E = (res['m1'][2] + res['M1'][2]) / 2
        RT = (res['m1'][1] + res['M1'][1]) / 2
        # investor's gross purchase return under the induced schedule
        def resid(mu, name):
            pstar, S, e = res[name]
            t0, tH, tL, gH, gL = objs(pstar, r)
            return e * (tH - tL) * (1 - mu)
        K1 = M1 * resid(M1, 'M1') + m1 * resid(m1, 'm1')
        print(f"   full buying: expected entry {mp.nstr(E, 6)}, expected proceeds {mp.nstr(RT, 10)}, investor gross return K(1) = {mp.nstr(K1, 8)} vs k = {k}")
