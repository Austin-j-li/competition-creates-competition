"""Exact cutoffs of the three-point model, with rational bracketing checks.

Run from the repository root:
  .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/A_three_point/tp_cutoffs.py

Irrational cutoffs are printed at 40 significant digits (decimal module).
Each one is then bracketed by two rationals 1e-12 apart, and the defining
inequality is evaluated exactly (Fractions) on both sides.
"""
import sys
from decimal import Decimal, getcontext
from fractions import Fraction as F

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import tp_closed_form as cf  # noqa: E402

getcontext().prec = 50
BENCH = {"h": F(10), "ell": F(1), "p": F(1, 2), "rho": F(1, 4), "cL": F(0),
         "cH": F(6), "k": F(1, 50), "r": F(3), "lam": F(1), "pi": F(1, 2)}


def D(x):
    return Decimal(x.numerator) / Decimal(x.denominator)


def frak_r(d, ell):
    """Root above ell of DeltaT(r) = d:  ell + d + sqrt(d^2 + 2 ell d)."""
    d, ell = D(d), D(ell)
    return ell + d + (d * d + 2 * ell * d).sqrt()


def r_C(mu, par):
    """Larger root of B_r(mu) = c_H (the crossing used in the memo)."""
    h, ell, p, cH = (D(par["h"]), D(par["ell"]), D(par["p"]), D(par["cH"]))
    mu = D(mu)
    if mu == 0:
        return (ell * ell - p * p) / (2 * cH)
    a = mu * h - cH
    disc = a * a + mu * ((1 - mu) * ell * ell - p * p)
    if disc < 0:
        return None
    return (a + disc.sqrt()) / mu


def bracket(name, root, fn):
    """Evaluate fn exactly just below and just above a decimal root."""
    eps = F(1, 10 ** 12)
    rr = F(str(root))
    lo, hi = rr - eps, rr + eps
    print(f"  {name}: root = {root:.40}")
    print(f"     at r = root - 1e-12: {float(fn(lo)):+.6e}")
    print(f"     at r = root + 1e-12: {float(fn(hi)):+.6e}")


def with_r(par, r):
    q = dict(par)
    q["r"] = r
    return q


def main():
    par = dict(BENCH)
    k, rho, pi = par["k"], par["rho"], par["pi"]
    print("Benchmark: h=10, ell=1, p=1/2, rho=1/4, c_L=0, c_H=6, k=1/50,"
          " pi=1/2, lam=1")
    print("\n1. Trading cutoff under the Intuitive-Criterion completion:"
          " K_rho(r) = k, r_T = frak_r(3k/(2 rho (1-pi)))")
    d = 3 * k / (2 * rho * (1 - pi))
    print(f"  argument 3k/(2 rho (1-pi)) = {d}")
    bracket("r_T", frak_r(d, par["ell"]),
            lambda r: cf.K_values(with_r(par, r))[0] - k)
    print("\n2. No-trade boundary under passive beliefs:"
          " (3/2) K_rho(r) = k, r = frak_r(k/(rho (1-pi)))")
    d2 = k / (rho * (1 - pi))
    print(f"  argument k/(rho (1-pi)) = {d2}")
    bracket("r_passive", frak_r(d2, par["ell"]),
            lambda r: F(3, 2) * cF(with_r(par, r)) - k)
    print("\n3. No-trade boundary under the adverse belief v = 0:"
          " (1/3)[2 rho (1-pi) + rho] DeltaT = k")
    d3 = 3 * k / (rho * (3 - 2 * pi))
    print(f"  argument 3k/(rho (3-2 pi)) = {d3}")
    bracket("r_adverse", frak_r(d3, par["ell"]),
            lambda r: (2 * rho * (1 - pi) + rho) / 3
            * cf.objects(with_r(par, r))["DeltaT"] - k)
    print("\n4. No-trade boundary robust to every off-path belief:"
          " (1/3)[2 rho (1-pi) + max(rho, 1-tau(r))] DeltaT(r) = k")

    def robust(r):
        q = with_r(par, r)
        t = cf.tau(q)
        mx = max(rho, 1 - t) if 0 < t <= 1 else (rho if t > 1 else F(1))
        return (2 * rho * (1 - pi) + mx) / 3 * cf.objects(q)["DeltaT"] - k
    lo, hi = F(1) + F(1, 10 ** 9), F(3)
    for _ in range(200):
        mid = (lo + hi) / 2
        if robust(mid) > 0:
            hi = mid
        else:
            lo = mid
    print(f"  root by exact bisection: in [{float(lo):.15f}, {float(hi):.15f}]")
    print(f"     robust(lo) = {float(robust(lo)):+.3e}, robust(hi) ="
          f" {float(robust(hi)):+.3e}")
    print(f"     tau at the root = {float(cf.tau(with_r(par, lo))):.6f}")
    print("\n5. Expensive-entry ceiling at the revealing flow: g_H(r) = c_H")
    rc1 = r_C(F(1), par)
    bracket("r_C(1)", rc1, lambda r: cf.objects(with_r(par, r))["gH"] - par["cH"])
    print("  closed form 4 + (3/2) sqrt(7) =",
          f"{Decimal(4) + Decimal(3) / 2 * Decimal(7).sqrt():.40}")
    print("\n6. Prior crossing B_r(pi) = c_H at the benchmark:")
    rp = r_C(pi, par)
    print(f"  r_C(1/2) = {rp:.20} (below ell = 1, so B_r(1/2) < c_H on (ell, h))")
    print(f"  B_1(1/2) = {float(cf.B(with_r(par, F(1)), F(1, 2))):.6f}")
    print("\n7. Return of entry before r = h requires c_H > h/2 - p^2/(2h):")
    print(f"  h/2 - p^2/(2h) = {par['h'] / 2 - par['p'] ** 2 / (2 * par['h'])}"
          f" = {float(par['h'] / 2 - par['p'] ** 2 / (2 * par['h'])):.6f}")
    print("\n8. Trading cutoff for other priors (rule E, region IV):")
    for pi2 in (F(1, 3), F(2, 3)):
        q = dict(par)
        q["pi"] = pi2
        d4 = 3 * k / (2 * rho * (1 - pi2))
        bracket(f"r_T(pi={pi2})", frak_r(d4, par["ell"]),
                lambda r, q=q: cf.K_values(with_r(q, r))[0] - k)
    print("\n9. Region-II example c_H = 4 (pi=1/2, lam=1):")
    q = dict(par)
    q["cH"] = F(4)
    d5 = 3 * k / (2 * (1 - pi))
    bracket("K_1(r) = k: frak_r(3k/(2(1-pi)))", frak_r(d5, par["ell"]),
            lambda r: cf.K_values(with_r(q, r))[1] - k)
    rp4 = r_C(pi, q)
    bracket("r_C(1/2) for c_H=4: B_r(1/2) = 4", rp4,
            lambda r: cf.B(with_r(q, r), F(1, 2)) - q["cH"])
    print("  closed form 2 + (3/2) sqrt(2) =",
          f"{Decimal(2) + Decimal(3) / 2 * Decimal(2).sqrt():.40}")
    rc4 = r_C(F(1), q)
    print(f"  r_C(1) for c_H=4: {rc4:.20} (above h = 10)")
    print("\n10. Presence lam = 1/2: m_lam = 1/3; crossing B_r(1/3) = c_H"
          " for c_H = 2")
    q2 = dict(par)
    q2["cH"], q2["lam"] = F(2), F(1, 2)
    rm = r_C(F(1, 3), q2)
    bracket("r_C(1/3) for c_H=2", rm,
            lambda r: cf.B(with_r(q2, r), F(1, 3)) - q2["cH"])


def cF(q):
    return cf.K_values(q)[0]


if __name__ == "__main__":
    main()
