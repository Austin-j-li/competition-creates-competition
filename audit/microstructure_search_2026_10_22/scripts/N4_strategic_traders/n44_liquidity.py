"""N4.4(b): price-sensitive liquidity trade in the slot (participation responds to the adverse-selection cost).

The non-informed filler receives a purchase motive with probability beta_hat and a sale motive with
probability beta_hat; the motive has a private benefit v ~ U[0, vbar] per unit. It buys iff
v >= kappa_+ = e(1) Delta (mu(1) - 1/2) + k, sells iff v >= kappa_- = e(-1) Delta (1/2 - mu(-1)) + k.
Participation b_+ = (1 - lam) beta_hat (1 - kappa_+/vbar) is a fixed point; it is a quadratic in b_+ on each
entry piece. Calibration: beta_hat = 2/5, vbar = 51/50 reproduces b = 11/51 at r = 3 on the recruiting piece.
Print-only. Run from the repository root:
  .venv/bin/python audit/microstructure_search_2026_10_22/scripts/N4_strategic_traders/n44_liquidity.py
"""
from fractions import Fraction as F
from math import isqrt
from common import RHO, CH, K, PI, R0, R1, R2, LAM, dec, head, objects, Bf

BH, VBAR = F(2, 5), F(51, 50)


def sqrt_bracket(x, digits=20):
    sc = 10 ** digits
    lo = F(isqrt(x.numerator * sc * sc // x.denominator), sc)
    return lo, lo + F(1, sc)


def fixed_points(o, lam, e1, bh=BH, vbar=VBAR):
    """Roots b of 2 b^2 + [lam - 2 Bh (1 - k/vbar)] b - Bh (1 - k/vbar) lam + Bh e1 Delta lam / (2 vbar) = 0, b in (0, Bh]."""
    Bh = (1 - lam) * bh
    a2 = F(2)
    a1 = lam - 2 * Bh * (1 - K / vbar)
    a0 = -Bh * (1 - K / vbar) * lam + Bh * e1 * o["D"] * lam / (2 * vbar)
    disc = a1 * a1 - 4 * a2 * a0
    roots = []
    if disc >= 0:
        lo, hi = sqrt_bracket(disc)
        for sgn in (1, -1):
            blo, bhi = (-a1 + sgn * lo) / (2 * a2), (-a1 + sgn * hi) / (2 * a2)
            blo, bhi = min(blo, bhi), max(blo, bhi)
            if bhi > 0 and blo <= Bh:
                roots.append((blo, bhi))
    return roots


def branch_report(o, lam, label, e1):
    roots = fixed_points(o, lam, e1)
    out = []
    for (blo, bhi) in roots:
        b = (blo + bhi) / 2
        mu1 = (lam + b) / (lam + 2 * b)
        recruits = Bf(o, mu1) >= CH
        consistent = recruits if e1 == 1 else (not recruits)
        kap = e1 * o["D"] * (mu1 - PI) + K
        part = 1 - kap / VBAR
        print(f"    {label}: b in [{dec(blo,10)}, {dec(bhi,10)}], mu(1) ~ {dec(mu1,6)} vs tau {dec(o['tau'],6)}: "
              f"recruits={recruits}, consistent={consistent}; kappa_+ ~ {dec(kap,5)}, participation 1-G ~ {dec(part,5)}, "
              f"uninformed buy prob ~ {dec(BH*part,5)}")
        out.append((b, consistent))
    return out


def main():
    lam = LAM
    head("N4.4(b) Price-sensitive liquidity: fixed points of uninformed purchase participation")
    print(f"  beta_hat = {BH}, vbar = {VBAR}; Bh = (1-lam) beta_hat = {(1-lam)*BH}; informed lam = {lam}")
    for r in (R0, R1, R2):
        o = objects(r)
        print(f"\n  r = {r}: Delta = {dec(o['D'],5)}, tau = {dec(o['tau'],6)}")
        if o["D"] < K:
            b = (1 - lam) * BH * (1 - K / VBAR)
            print(f"    no informed trade: kappa = k, b = {b} (~{dec(b,6)}), posterior 1/2 at every flow; entry rho")
            continue
        branch_report(o, lam, "recruiting piece e(1)=1  ", F(1))
        branch_report(o, lam, "non-recruiting piece e(1)=rho", RHO)
        # sale side: e(-1) = rho always; b_- fixed point with mu(-1) = b_-/(lam + 2 b_-)
        Bh = (1 - lam) * BH
        a2, a1 = F(2), lam - 2 * Bh * (1 - K / VBAR)
        a0 = -Bh * (1 - K / VBAR) * lam + Bh * RHO * o["D"] * lam / (2 * VBAR)
        disc = a1 * a1 - 4 * a2 * a0
        lo, hi = sqrt_bracket(disc)
        bm = (-a1 + lo) / (2 * a2)
        print(f"    sale side (entry rho): b_- ~ {dec(bm,6)}, mu(-1) ~ {dec(bm/(lam+2*bm),6)}; "
              f"informed L sale return rho Delta mu(-1) - k ~ {dec(RHO*o['D']*bm/(lam+2*bm)-K,6)}")
        # informed H return in each branch
        for (lab, e1) in (("recruiting", F(1)), ("non-recruiting", RHO)):
            for (blo, bhi) in fixed_points(o, lam, e1):
                b = (blo + bhi) / 2
                mu1 = (lam + b) / (lam + 2 * b)
                print(f"    informed H purchase return on the {lab} piece: e(1) Delta (1 - mu(1)) - k ~ {dec(e1*o['D']*(1-mu1)-K,6)}")

    head("Multiplicity interval in r: where both pieces are self-consistent")
    def status(r):
        o = objects(r)
        rec = any(c for (_, c) in [(b, Bf(o, (lam+b)/(lam+2*b)) >= CH) for (blo, bhi) in fixed_points(o, lam, F(1)) for b in [(blo+bhi)/2]])
        non = any(c for (_, c) in [(b, Bf(o, (lam+b)/(lam+2*b)) < CH) for (blo, bhi) in fixed_points(o, lam, RHO) for b in [(blo+bhi)/2]])
        return rec, non
    grid = [F(3) + F(i, 100) for i in range(0, 121)]
    prev = None
    for r in grid:
        st = status(r)
        if st != prev:
            print(f"    r = {dec(r,2)}: recruiting piece consistent = {st[0]}, non-recruiting piece consistent = {st[1]}")
            prev = st
    # brackets of the two boundaries
    def f_rec(r):
        o = objects(r)
        roots = fixed_points(o, lam, F(1))
        b = sum(roots[0]) / 2 if roots else None
        return Bf(o, (lam+b)/(lam+2*b)) - CH if b is not None else None
    def f_non(r):
        o = objects(r)
        roots = fixed_points(o, lam, RHO)
        b = sum(roots[0]) / 2 if roots else None
        return Bf(o, (lam+b)/(lam+2*b)) - CH if b is not None else None
    for name, f in (("recruiting piece stops being consistent (B = c_H)", f_rec), ("non-recruiting piece becomes consistent (B = c_H)", f_non)):
        lo, hi = F(3), F(21, 5)
        flo = f(lo)
        for _ in range(40):
            mid = (lo + hi) / 2
            fm = f(mid)
            if (fm > 0) == (flo > 0):
                lo, flo = mid, fm
            else:
                hi = mid
        print(f"    {name}: r in [{dec(lo,9)}, {dec(hi,9)}]")
    o = objects(R1)
    print(f"\n  Fixed-noise comparison: V3 ceiling r_C = (50 + sqrt(2529))/29 ~ 3.458247 (X_check).")


if __name__ == "__main__":
    main()
