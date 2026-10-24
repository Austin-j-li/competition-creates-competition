"""Equilibria of the discrete-Laplace stake model (mpmath; print only).

Reduction: with buy-only orders every flow x >= 1 has posterior M and every flow x <= 0 has posterior m,
for every pair (bH, bL). So investor payoffs depend on two entry rates (eG, eB) and on (M, m).
Closed-form gains are used for the scans. Every reported equilibrium is re-checked from primitives by
direct summation over flows (dl_gain_direct).

Run from the repository root:
    .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/C5_stake/dl_enumerate.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mpmath import mp, mpf, exp, nstr  # noqa: E402
from dl_lib import BENCH, R0, R1, R2, R_END, auction, tau_of, posteriors, noise_pmf  # noqa: E402
from dl_thresholds import thresholds, consts  # noqa: E402

mp.dps = 40
PAR = BENCH
RHO, KC = PAR["rho"], PAR["k"]
EPS = mpf(10) ** (-28)   # boundary values are tested up to this rounding allowance


def le0(x):
    return x <= EPS


def ge0(x):
    return x >= -EPS


def entry_rates(a, bH, bL, phiG=None, phiB=None):
    """Entry at good-news and bad-news flows. phi = high-cost preparation probability.
    Rule: prepare iff B(mu) >= cH (prepare at indifference), unless phi is supplied."""
    M, m = posteriors(bH, bL)
    tau = tau_of(a, PAR)
    pg = (1 if M >= tau else 0) if phiG is None else phiG
    pb = (1 if m >= tau else 0) if phiB is None else phiB
    return M, m, RHO + (1 - RHO) * pg, RHO + (1 - RHO) * pb


def gains_cf(a, omega, bH, bL, phiG=None, phiB=None):
    aa, delta, g0, g1 = consts(PAR)
    M, m, eG, eB = entry_rates(a, bH, bL, phiG, phiB)
    D, wL, wH = a["D"], a["wL"], a["wH"]
    DH = omega * wH * delta * (eG - eB) + D * (g1 * eG * (1 - M) + (1 - g1) * eB * (1 - m)) - KC
    DL = omega * wL * delta * (eG - eB) - D * (g1 * eG * M + (1 - g1) * eB * m) - KC
    return DH, DL, M, m, eG, eB


def dl_gain_direct(a, omega, bH, bL, eG, eB, span=150):
    """Direct summation over flows -span..span. Returns (gain_H, gain_L) of buying versus not."""
    D, wL, wH, t0 = a["D"], a["wL"], a["wH"], a["t0"]
    M, m = posteriors(bH, bL)
    out = []
    for w, sgn in ((wH, 1), (wL, -1)):
        u = {}
        for q in (0, 1):
            tot = mpf(0)
            for z in range(-span, span + 1):
                x = q + z
                e = eG if x >= 1 else eB
                mu = M if x >= 1 else m
                price = t0 + e * (wL + D * mu)
                vt = t0 + e * w
                tot += noise_pmf(z, PAR) * (omega * vt + q * (vt - price))
            u[q] = tot - KC * q
        out.append(u[1] - u[0])
    return out[0], out[1]


def bisect(f, lo, hi, n=120):
    flo = f(lo)
    for _ in range(n):
        mid = (lo + hi) / 2
        fm = f(mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


def equilibria(r, omega):
    """List equilibria as dicts with fields: kind, bH, bL, phiG, strict_inv (pure orders, buyer gain > 0),
    chall_ok (challenger prepares at indifference), E, OH."""
    a = auction(r, PAR)
    t = thresholds(r, PAR)
    tau = t["tau"]
    aa, delta, g0, g1 = consts(PAR)
    eqs = []

    def add(kind, bH, bL, phiG, phi_is_rule):
        DH, DL, M, m, eG, eB = gains_cf(a, omega, bH, bL, phiG)
        gH = g0 + delta * bH
        gL = g0 + delta * bL
        eH = gH * eG + (1 - gH) * eB
        eL = gL * eG + (1 - gL) * eB
        pure = bH in (0, 1) and bL in (0, 1)
        strict = pure and ((bH == 1 and DH > 0) or (bH == 0 and DH <= 0)) and ((bL == 1 and DL > 0) or (bL == 0 and DL <= 0))
        eqs.append(dict(kind=kind, bH=bH, bL=bL, phiG=phiG, DH=DH, DL=DL, eG=eG, eB=eB, M=M, m=m,
                        strict=strict, rule_ok=phi_is_rule, E=(eH + eL) / 2, OH=eH / 2, eH=eH, eL=eL))

    # --- no trade
    DH0, DL0, *_ = gains_cf(a, omega, mpf(0), mpf(0))
    if le0(DH0) and le0(DL0):
        add("NT", mpf(0), mpf(0), None, True)
    # --- line bL = 0 (H mixing)
    if t["recruit_ok"] and tau > mpf(1) / 2:
        bstar = t["beta_star"]
    else:
        bstar = None
    DH1, DL1, *_ = gains_cf(a, omega, mpf(1), mpf(0))
    if ge0(DH1) and le0(DL1):
        add("S", mpf(1), mpf(0), None, True)
    # interior roots of D_H along bL = 0 away from the jump at bstar
    N = 4000
    prev_b, prev_D = mpf(0), gains_cf(a, omega, mpf(0), mpf(0))[0]
    for i in range(1, N):
        b = mpf(i) / N
        DHb = gains_cf(a, omega, b, mpf(0))[0]
        jump = bstar is not None and prev_b < bstar <= b
        if (prev_D > 0) != (DHb > 0) and not jump:
            root = bisect(lambda x: gains_cf(a, omega, x, mpf(0))[0], prev_b, b)
            DHr, DLr, *_ = gains_cf(a, omega, root, mpf(0))
            if le0(DLr):
                add("H-mix", root, mpf(0), None, True)
        prev_b, prev_D = b, DHb
    # threshold mixing at (bstar, 0)
    if bstar is not None and 0 < bstar < 1:
        # D_H(phi) is affine in phi
        d0 = gains_cf(a, omega, bstar, mpf(0), phiG=mpf(0))
        d1 = gains_cf(a, omega, bstar, mpf(0), phiG=mpf(1))
        s = d1[0] - d0[0]
        if s != 0:
            ph = -d0[0] / s
            if 0 <= ph <= 1:
                DHc, DLc = gains_cf(a, omega, bstar, mpf(0), phiG=ph)[:2]
                if le0(DLc):
                    add("H-thresh-mix", bstar, mpf(0), ph, ph == 1)
    # --- line bH = 1 (L mixing)
    if t["recruit_ok"] and tau > mpf(1) / 2:
        bmax = t["beta_max"]
        # interior root of D_L on (0, bmax)
        fL = lambda x: gains_cf(a, omega, mpf(1), x)[1]
        if fL(mpf(0)) < 0 < fL(bmax - mpf(10) ** (-25)):
            root = bisect(fL, mpf(0), bmax - mpf(10) ** (-25))
            add("M", mpf(1), root, None, True)
        d0 = gains_cf(a, omega, mpf(1), bmax, phiG=mpf(0))
        d1 = gains_cf(a, omega, mpf(1), bmax, phiG=mpf(1))
        s = d1[1] - d0[1]
        if s != 0:
            ph = -d0[1] / s
            if 0 <= ph <= 1 and ge0(d0[0] + ph * (d1[0] - d0[0])):
                add("M'", mpf(1), bmax, ph, ph == 1)
    return eqs


def verify_direct(r, omega, eq):
    a = auction(r, PAR)
    bH, bL = eq["bH"], eq["bL"]
    M, m = posteriors(bH, bL)
    tau = tau_of(a, PAR)
    eG = eq["eG"]
    eB = eq["eB"]
    gH, gL = dl_gain_direct(a, omega, bH, bL, eG, eB)
    return gH, gL


def lemma_scan(r, omega, n=60):
    """Check on an n x n grid: (A) bL <= bH implies D_H > D_L; (B) bL > bH implies D_L < 0."""
    a = auction(r, PAR)
    bad_A = bad_B = 0
    worst_A = None
    worst_B = None
    for i in range(n + 1):
        for j in range(n + 1):
            bH, bL = mpf(i) / n, mpf(j) / n
            DH, DL, *_ = gains_cf(a, omega, bH, bL)
            if bL <= bH:
                d = DH - DL
                if worst_A is None or d < worst_A:
                    worst_A = d
                if not d > 0:
                    bad_A += 1
            else:
                if worst_B is None or DL > worst_B:
                    worst_B = DL
                if not DL < 0:
                    bad_B += 1
    return bad_A, worst_A, bad_B, worst_B


def report(r, label, omegas):
    t = thresholds(r, PAR)
    print(f"\n=== {label}: r={nstr(r, 6)}  tau={nstr(t['tau'], 10)}  rho D/2 <= k: {t['NT_cost_ok']} ===")
    for key in ("omega_H", "omega_star", "Omega2", "Omega1"):
        if key in t:
            print(f"   {key} = {nstr(t[key], 12)}")
    for om in omegas:
        eqs = equilibria(r, om)
        print(f"\n omega = {nstr(om, 10)}")
        bA, wA, bB, wB = lemma_scan(r, om, 40)
        print(f"   lemma scan 40x40: violations (A) {bA} min(D_H-D_L)={nstr(wA, 5)}; (B) {bB} max(D_L | bL>bH)={nstr(wB, 5)}")
        if not eqs:
            print("   no equilibrium found (conventional rules)")
        for eq in eqs:
            dH, dL = verify_direct(r, om, eq)
            phi = "-" if eq["phiG"] is None else nstr(eq["phiG"], 8)
            print(f"   {eq['kind']:13s} bH={nstr(eq['bH'], 10):>12s} bL={nstr(eq['bL'], 10):>12s} phi_G={phi:>10s}  "
                  f"strict={eq['strict'] and eq['rule_ok']!s:5s} inv-mix-ok(chall rule)={eq['rule_ok']!s:5s} "
                  f"E={nstr(eq['E'], 8)} O_H={nstr(eq['OH'], 8)} "
                  f"| direct gains H={nstr(dH, 6)} L={nstr(dL, 6)}")


if __name__ == "__main__":
    t0_ = thresholds(R0, PAR)
    t1_ = thresholds(R1, PAR)
    om_r0 = [mpf(0), mpf("0.1"), t0_["omega_star"] - mpf("0.001"), t0_["omega_star"] + mpf("0.001"),
             t0_["omega_H"] - mpf("0.001"), t0_["omega_H"] + mpf("0.001"), mpf("0.3"),
             t0_["Omega2"] + mpf("0.001"), t0_["Omega1"], t0_["Omega1"] + mpf("0.001"), mpf(1), mpf(5)]
    report(R0, "WEAK r0", om_r0)
    om_r1 = [mpf(0), mpf(1), mpf(3), t1_["Omega2"], mpf("3.5"), t1_["Omega1"], t1_["Omega1"] + mpf("0.001"), mpf(5), mpf(20), mpf(100)]
    report(R1, "STRONG r1", om_r1)
    report(R_END, "r = 4 (no recruitment: B(M1) < cH)", [mpf(0), mpf(5), mpf(50)])
