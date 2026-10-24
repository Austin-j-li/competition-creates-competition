"""Interval-arithmetic sign certificates for the discrete-Laplace stake model (mpmath.iv; print only).

Every strict inequality used in the benchmark classification is evaluated with outward-rounded intervals,
a = exp(-1/2) enclosed by an interval of width about 1e-45. The script prints CERTIFIED when the whole
interval has the stated sign and NOT CERTIFIED otherwise. Closed forms follow the memo (Section 3.6).

Run from the repository root:
    .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/C5_stake/dl_certify.py
"""
from fractions import Fraction as F

from mpmath import iv, mp

iv.dps = 50
mp.dps = 30

h, ell, p, rho, cH, k = F(10), F(1), F(1, 2), F(1, 4), F(5), F(1, 50)


def I(x):
    x = F(x)
    return iv.mpf(x.numerator) / iv.mpf(x.denominator)


A = iv.exp(-I(F(1, 2)))                       # a = exp(-1/b), b = 2
G0 = A / (1 + A)
G1 = 1 / (1 + A)
DEL = (1 - A) / (1 + A)
RHO, K = I(rho), I(k)


def auction(r):
    r = F(r)
    t0 = p * (1 - p / r)
    tH = r / 2 + p * p / (2 * r)
    tL = ell - (ell * ell - p * p) / (2 * r)
    gH = h - tH
    gL = (ell * ell - p * p) / (2 * r)
    tau = (cH - gL) / (gH - gL)
    return dict(D=I(tH - tL), wL=I(tL - t0), wH=I(tH - t0), tau=I(tau), Dq=tH - tL, tauq=tau)


def post(bH, bL):
    gH, gL = G0 + DEL * bH, G0 + DEL * bL
    return gH / (gH + gL), (1 - gH) / (2 - gH - gL)


def gains(Au, omega, bH, bL, phiG):
    """Closed-form gains with entry rho + (1-rho) phiG at good news and rho at bad news (bL <= bH)."""
    M, m = post(bH, bL)
    eG = RHO + (1 - RHO) * phiG
    eB = RHO
    D, wL, wH = Au["D"], Au["wL"], Au["wH"]
    DH = omega * wH * DEL * (eG - eB) + D * (G1 * eG * (1 - M) + (1 - G1) * eB * (1 - m)) - K
    DL = omega * wL * DEL * (eG - eB) - D * (G1 * eG * M + (1 - G1) * eB * m) - K
    return DH, DL


def verdict(name, x, want):
    """want = '>0' or '<0'."""
    lo, hi = x.a, x.b
    ok = (lo > 0) if want == ">0" else (hi < 0)
    print(f"  {'CERTIFIED    ' if ok else 'NOT CERTIFIED'} {name:62s} in [{float(lo):+.6e}, {float(hi):+.6e}]  want {want}")
    return ok


def thresholds(Au):
    tau = Au["tau"]
    D, wL, wH = Au["D"], Au["wL"], Au["wH"]
    out = {}
    out["omega_H"] = (K - D * G0 * G1 * (1 + RHO)) / (wH * DEL * (1 - RHO))
    out["Omega1"] = (D * (G1 ** 2 + RHO * G0 ** 2) + K) / (wL * DEL * (1 - RHO))
    bmax = (G1 / tau - 1) / DEL
    mat = G0 / (1 - DEL * bmax)
    out["beta_max"] = bmax
    out["Omega2"] = (D * (G1 * tau + RHO * G0 * mat) + K) / (wL * DEL * (1 - RHO))
    ustar = G0 * (2 * tau - 1) / (1 - tau)
    bstar = ustar / DEL
    const = D * G0 * G1 * (1 / (2 * G0 + ustar) + RHO / (2 * G1 - ustar)) - K
    out["beta_star"] = bstar
    out["omega_star"] = -const / (wH * DEL * (1 - RHO))
    return out


def show_encl(label, x):
    print(f"  {label:34s} [{float(x.a):.12f}, {float(x.b):.12f}]  width {float(x.b - x.a):.1e}")


if __name__ == "__main__":
    for rname, r in (("r0 = 6/5", F(6, 5)), ("r1 = 3", F(3))):
        Au = auction(r)
        t = thresholds(Au)
        print(f"\n== {rname}: enclosures ==")
        print(f"  tau = {Au['tauq']} = {float(Au['tauq']):.9f};  rho*Delta_T/2 = {rho * Au['Dq'] / 2} vs k = {k}")
        for key in ("omega_H", "omega_star", "Omega2", "Omega1", "beta_max", "beta_star"):
            show_encl(key, t[key])

    # ---------------- weak economy r0: five equilibria at omega = 9/25 ----------------
    print("\n== r0 = 6/5, omega = 9/25 (between Omega2(r0) = 0.3596 and Omega1(r0) = 0.3720) ==")
    Au = auction(F(6, 5))
    t = thresholds(Au)
    om = I(F(9, 25))
    zero, one = iv.mpf(0), iv.mpf(1)
    # NT
    DH, DL = gains(Au, om, zero, zero, zero)
    verdict("NT: H gain at (0,0) (exact: rho*D/2 - k)", DH, "<0")
    verdict("NT: L gain at (0,0)", DL, "<0")
    # S
    DH, DL = gains(Au, om, one, zero, one)
    verdict("S: H gain at (1,0) with entry after good news", DH, ">0")
    verdict("S: L gain at (1,0)", DL, "<0")
    # M: sign change of D_L on (0, beta_max) at bH = 1 and H gain positive
    DH0, DL0 = gains(Au, om, one, zero, one)
    DH1, DL1 = gains(Au, om, one, t["beta_max"], one)
    verdict("M: L gain at (1,0)", DL0, "<0")
    verdict("M: L gain at (1,beta_max), phi=1", DL1, ">0")
    verdict("M: H gain at (1,beta_max), phi=1", DH1, ">0")
    # M': challenger mixing at beta_max: L gain changes sign between phi = 0 and phi = 1
    DHm0, DLm0 = gains(Au, om, one, t["beta_max"], zero)
    verdict("M': L gain at (1,beta_max), phi=0", DLm0, "<0")
    verdict("M': H minus L gain at (1,beta_max), phi=0 (affine in phi; so > 0 at the root)", DHm0 - DLm0, ">0")
    verdict("M': H minus L gain at (1,beta_max), phi=1", DH1 - DL1, ">0")
    # H-threshold mixing at (beta_star, 0)
    DHs0, DLs0 = gains(Au, om, t["beta_star"], zero, zero)
    DHs1, DLs1 = gains(Au, om, t["beta_star"], zero, one)
    verdict("Hthr: H gain at (beta_star,0), phi=0", DHs0, "<0")
    verdict("Hthr: H gain at (beta_star,0), phi=1", DHs1, ">0")
    verdict("Hthr: L gain at (beta_star,0), phi=0", DLs0, "<0")
    verdict("Hthr: L gain at (beta_star,0), phi=1", DLs1, "<0")
    # Hth for every omega >= omega_star: phi(omega) = (k - K_I) / ((1-rho){omega wH delta + c}), c = D g0 g1 / (2 g0 + u*).
    # L's gain at (beta_star, 0) is  omega wL delta (1-rho) phi - D {g1 (rho + (1-rho) phi) tau + g0 rho m*} - k.
    # The first term rises in omega and tends to (wL/wH)(k - K_I); the phi-term of the trading part is <= 0.
    D_, wL_, wH_, tau_ = Au["D"], Au["wL"], Au["wH"], Au["tau"]
    ustar_ = G0 * (2 * tau_ - 1) / (1 - tau_)
    KI_ = D_ * G0 * G1 * RHO * (1 / (2 * G0 + ustar_) + 1 / (2 * G1 - ustar_))
    mstar_ = post(t["beta_star"], zero)[1]
    verdict("Hth: k - K_I > 0 (phi is positive)", K - KI_, ">0")
    Ubound = (wL_ / wH_) * (K - KI_) - D_ * RHO * (G1 * tau_ + G0 * mstar_) - K
    verdict("Hth: upper bound on L's gain for every omega >= omega_star", Ubound, "<0")

    # ---------------- weak economy: unique no trade for omega = 9/50 < omega_star ----------------
    print("\n== r0 = 6/5, omega = 9/50 (below omega_star = 0.18780): no trade should be unique ==")
    om = I(F(9, 50))
    DH, _ = gains(Au, om, zero, zero, zero)
    verdict("regime I max over beta (at beta=0): H gain", DH, "<0")
    DHs, _ = gains(Au, om, t["beta_star"], zero, one)
    verdict("regime II max over beta (at beta_star): H gain", DHs, "<0")
    _, DLb = gains(Au, om, one, t["beta_max"], one)
    verdict("L line max over beta (at beta_max): L gain", DLb, "<0")
    _, DLo = gains(Au, om, t["beta_max"] + iv.mpf("1e-20"), zero, zero)
    # a point beyond the recruiting limit: entry is rho at good news too
    _, DLr = gains(Au, om, one, t["beta_max"] + iv.mpf("1e-6"), zero)
    verdict("L line beyond beta_max (entry rho): L gain", DLr, "<0")

    # ---------------- strong economy r1: omega = 7/2 between Omega2 and Omega1 ----------------
    print("\n== r1 = 3, omega = 7/2 (between Omega2(r1) = 3.4225 and Omega1(r1) = 3.5878) ==")
    Au = auction(F(3))
    t = thresholds(Au)
    om = I(F(7, 2))
    DH, DL = gains(Au, om, one, zero, one)
    verdict("S: H gain at (1,0)", DH, ">0")
    verdict("S: L gain at (1,0)", DL, "<0")
    DH1, DL1 = gains(Au, om, one, t["beta_max"], one)
    verdict("M: L gain at (1,beta_max), phi=1", DL1, ">0")
    DHm0, DLm0 = gains(Au, om, one, t["beta_max"], zero)
    verdict("M': L gain at (1,beta_max), phi=0", DLm0, "<0")
    print("\n== r1 = 3, omega = 18/5 (above Omega1 = 3.5878): S fails; only M' remains ==")
    om = I(F(18, 5))
    DH, DL = gains(Au, om, one, zero, one)
    verdict("S: L gain at (1,0) (L mimics)", DL, ">0")
    DH1, DL1 = gains(Au, om, one, t["beta_max"], one)
    verdict("(1,beta_max) with phi=1: L gain (wants more) so no strict-rule equilibrium", DL1, ">0")
    DHm0, DLm0 = gains(Au, om, one, t["beta_max"], zero)
    verdict("M': L gain at (1,beta_max), phi=0", DLm0, "<0")
    print("\n== r1 = 3, omega = 3 (< Omega2): unique S ==")
    om = I(F(3))
    DH, DL = gains(Au, om, one, zero, one)
    verdict("S: L gain", DL, "<0")
    _, DLb = gains(Au, om, one, t["beta_max"], one)
    verdict("L line max over beta (at beta_max): L gain", DLb, "<0")
    DHs, _ = gains(Au, om, zero, zero, zero)
    verdict("H line, regime I at beta=0: H gain (decreasing in beta, minimum at beta_star)", DHs, ">0")
    DHs1, _ = gains(Au, om, t["beta_star"], zero, zero)
    verdict("H line, regime I at beta_star-: H gain", DHs1, ">0")
    DHs2, _ = gains(Au, om, one, zero, one)
    verdict("H line, regime II at beta=1: H gain (regime II minimum)", DHs2, ">0")
