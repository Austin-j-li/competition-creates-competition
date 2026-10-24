"""Shared objects for the E2 scripts. Print-only helpers; no checks that stop a run.

Two number fields:
  EXACT  - fractions.Fraction (calibration A and all rational inputs);
  MP     - mpmath mpf with 40 significant digits (calibration B, Laplace cross-checks).
Decimal inputs are parsed as decimals (Fraction('1.2') = 6/5), never through a binary float.
"""
from fractions import Fraction as Fr
from mpmath import mp, mpf, exp, log, e as E_NUM

mp.dps = 40


class Field:
    def __init__(self, name):
        self.name = name

    def __call__(self, x):
        """Convert an int, a decimal string, a Fraction or an mpf into the field."""
        if self.name == "exact":
            if isinstance(x, Fr):
                return x
            if isinstance(x, (int, str)):
                return Fr(x)
            raise TypeError("exact field needs int, str or Fraction")
        if isinstance(x, Fr):
            return mpf(x.numerator) / mpf(x.denominator)
        if isinstance(x, str):
            q = Fr(x)
            return mpf(q.numerator) / mpf(q.denominator)
        return mpf(x)


EXACT = Field("exact")
MP = Field("mp")


def show(x, digits=12):
    """Display string: the exact fraction (if short) and a decimal."""
    if isinstance(x, Fr):
        dec = mp.nstr(mpf(x.numerator) / x.denominator, digits)
        s = f"{x.numerator}/{x.denominator}" if x.denominator != 1 else f"{x.numerator}"
        return f"{s} (= {dec})" if len(s) < 40 else f"{dec} (exact rational, {len(s)} chars)"
    return mp.nstr(x, digits)


# ---------------------------------------------------------------- auction objects
def auction(F, r, h=10, ell=1, p="0.5"):
    """Point-mass classes, R ~ U[0, r], p < ell < r < h. Paper eq. (4)."""
    r, h, ell, p = F(r), F(h), F(ell), F(p)
    t0 = p * (1 - p / r)
    tH = r / 2 + p * p / (2 * r)
    tL = ell - (ell * ell - p * p) / (2 * r)
    gH, gL = h - tH, ell - tL
    return dict(r=r, t0=t0, tH=tH, tL=tL, gH=gH, gL=gL, D=tH - tL, wH=tH - t0, wL=tL - t0)


def auction_by_integration(r, theta, p=Fr(1, 2)):
    """Expected target proceeds t(theta) and challenger gain g(theta) by direct exact integration
    over R ~ U[0, r] of the realized outcomes. The target receives max{p, min(R, theta)}; the
    challenger keeps (theta - max{p, R})_+. Exact for rational inputs (piecewise linear integrands)."""
    r, theta, p = Fr(r), Fr(theta), Fr(p)

    def integrate(fn, lo, hi, kinks):
        pts = sorted({lo, hi, *[x for x in kinks if lo < x < hi]})
        tot = Fr(0)
        for x0, x1 in zip(pts, pts[1:]):
            m = (x0 + x1) / 2  # piecewise linear: midpoint rule is exact on each piece
            tot += fn(m) * (x1 - x0)
        return tot

    t = integrate(lambda R: max(p, min(R, theta)), Fr(0), r, [p, theta]) / r
    g = integrate(lambda R: max(theta - max(p, R), Fr(0)), Fr(0), r, [p, theta]) / r
    t0 = integrate(lambda R: p if R >= p else Fr(0), Fr(0), r, [p]) / r
    return t0, t, g


def B(A, mu):
    return A["gL"] + mu * (A["gH"] - A["gL"])


def tau(A, cH):
    return (cH - A["gL"]) / (A["gH"] - A["gL"])


# ---------------------------------------------------------------- the slot
def slot_from_lam_beta(F, lam, beta):
    lam, beta = F(lam), F(beta)
    b = (1 - lam) * beta
    c = (1 - lam) * (1 - 2 * beta)
    return dict(lam=lam, beta=beta, b=b, c=c, u=lam / b)


def bounds(u, pi):
    """Posterior bounds after one unit order: likelihood ratio 1 + u."""
    m = pi / (pi + (1 - pi) * (1 + u))
    M = pi * (1 + u) / (pi * (1 + u) + 1 - pi)
    return m, M


# ---------------------------------------------------------------- Laplace benchmark (b = 2)
def laplace_full_order_entry(tau_val, rho, bscale=2):
    """Paper eq. (12) at prior 1/2 with full orders (1, -1). Returns (E, e_H, e_L, x_star).
    The threshold is interior or at the plateau (tie rule enters at tau = M)."""
    rho, bscale = mpf(rho), mpf(bscale)
    tau_val = mpf(tau_val)
    M = 1 / (1 + exp(-2 / bscale))
    if tau_val > M:
        return rho, rho, rho, None
    xs = bscale / 2 * log(tau_val / (1 - tau_val))
    if xs < -1:
        xs = mpf(-1)
    aH = 1 - exp((xs - 1) / bscale) / 2
    aL = exp(-(xs + 1) / bscale) / 2
    eH, eL = rho + (1 - rho) * aH, rho + (1 - rho) * aL
    return (eH + eL) / 2, eH, eL, xs


def calibration_A(F=EXACT):
    return slot_from_lam_beta(F, Fr(6, 17), Fr(1, 3))


def calibration_B():
    """u = e - 1 (so M(pi) equals the Laplace bound at b = 2 for every prior), and the
    full-order entry at the benchmark strong strength equals the exact Laplace entry:
    b + lam/2 = (alpha_H + alpha_L)/2 with lam = u b."""
    A3 = auction(MP, 3)
    E_lap, eH, eL, xs = laplace_full_order_entry(tau(A3, MP(6)), MP("0.25"))
    half_sum = (E_lap - mpf("0.25")) / mpf("0.75")  # (alpha_H + alpha_L)/2
    u = E_NUM - 1
    b = 2 * half_sum / (2 + u)
    lam = u * b
    beta = b / (1 - lam)
    S = dict(lam=lam, beta=beta, b=b, c=1 - lam - 2 * b, u=u)
    return S, E_lap


def calibration_B_coordinator():
    """The coordinator's version: match the six-digit display 0.522757."""
    half_sum = (mpf("0.522757") - mpf("0.25")) / mpf("0.75")
    u = E_NUM - 1
    b = 2 * half_sum / (2 + u)
    lam = u * b
    return dict(lam=lam, beta=b / (1 - lam), b=b, c=1 - lam - 2 * b, u=u)


if __name__ == "__main__":
    print("Calibration A:", {k: show(v) for k, v in calibration_A().items()})
    SB, E_lap = calibration_B()
    print("Laplace benchmark full-order entry at r = 3 (40 digits):", mp.nstr(E_lap, 40))
    print("Calibration B (exact Laplace match):")
    for k_, v in SB.items():
        print(f"   {k_} = {mp.nstr(v, 30)}")
    SC = calibration_B_coordinator()
    print("Calibration B, coordinator's six-digit match: differences from the exact match")
    for k_ in ("lam", "beta", "b"):
        print(f"   {k_}: {mp.nstr(SC[k_], 12)}  (difference {mp.nstr(SC[k_] - SB[k_], 3)})")
    m, M = bounds(SB["u"], mpf(1) / 2)
    print("B: M(1/2) =", mp.nstr(M, 20), " e/(1+e) =", mp.nstr(E_NUM / (1 + E_NUM), 20))
    print("B: c - b =", mp.nstr(SB["c"] - SB["b"], 12), "(positive, so beta < 1/3 and the zero flow is less informative)")
    # Auction objects: closed forms against direct integration
    for r in (Fr(11, 10), Fr(6, 5), Fr(23, 10), Fr(3), Fr(18, 5)):
        A = auction(EXACT, r)
        t0, tH, gH = auction_by_integration(r, 10)
        _, tL, gL = auction_by_integration(r, 1)
        diffs = [t0 - A["t0"], tH - A["tH"], tL - A["tL"], gH - A["gH"], gL - A["gL"]]
        print(f"r = {r}: closed form minus integration = {[str(x) for x in diffs]};  Delta_T = {show(A['D'])}")
