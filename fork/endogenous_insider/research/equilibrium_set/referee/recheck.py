"""Independent re-implementation of the key numbers of note.md (referee scratch).

Pure functions. Integrals by scipy.integrate.quad with explicit breakpoints; no closed form from
note.md is used except where the line says so, so each closed form is checked against quadrature.
Prints results; writes recheck.csv. Status of every number: numerical diagnostic.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
H_, ELL, P_, B, K, C = 10.0, 1.0, 0.5, 2.0, 0.02, 6.0
m = 1.0 / (1.0 + math.exp(2.0 / B))
M = 1.0 - m
INF = math.inf


def acq(r: float) -> tuple[float, float]:
    """(Delta_T, tau) from (4) and (F.1)."""
    tH = r / 2 + P_ ** 2 / (2 * r)
    tL = ELL - (ELL ** 2 - P_ ** 2) / (2 * r)
    gH = H_ - tH
    gL = (ELL ** 2 - P_ ** 2) / (2 * r)
    return tH - tL, (C - gL) / (gH - gL)


def f(x: float) -> float:
    return math.exp(-abs(x) / B) / (2 * B)


def mu_pure(x: float, q: float, z: float) -> float:
    """Posterior (7) under pure orders (q, -z)."""
    return 1.0 / (1.0 + math.exp(-(abs(x + z) - abs(x - q)) / B))


def integ(fun, lo: float, hi: float, pts: list[float]) -> float:
    if hi <= lo:
        return 0.0
    cuts = sorted(set([lo] + [p for p in pts if lo < p < hi] + ([hi] if hi < INF else [])))
    tot = 0.0
    for a, b in zip(cuts[:-1], cuts[1:]):
        tot += quad(fun, a, b, limit=200, epsabs=1e-14, epsrel=1e-13)[0]
    if hi == INF:
        # tail beyond the last breakpoint: integrands decay like e^{-x/b}; e^{-60} is below 1e-26
        tot += quad(fun, cuts[-1], cuts[-1] + 120.0, limit=400, epsabs=1e-16, epsrel=1e-13)[0]
    return tot


def F_theta(r: float, q: float, z: float, A: list[tuple[float, float]], theta: str, s: float) -> float:
    """Gross per unit for a deviation of magnitude s against the schedule of orders (q, -z) and entry set A."""
    dT, _ = acq(r)
    if theta == "H":
        fun = lambda x: f(x - s) * (1 - mu_pure(x, q, z))
    else:
        fun = lambda x: f(x + s) * mu_pure(x, q, z)
    pts = [q, -z, s, -s, 0.0, 1.0, -1.0]
    return dT * sum(integ(fun, lo, hi, pts) for lo, hi in A)


def U(r, q, z, A, theta, s):
    return s * (F_theta(r, q, z, A, theta, s) - K)


def best_resp(r, q, z, A, theta, n=401):
    ss = np.linspace(0, 1, n)
    vals = np.array([U(r, q, z, A, theta, s) for s in ss])
    i = int(vals.argmax())
    lo, hi = ss[max(i - 1, 0)], ss[min(i + 1, n - 1)]
    if 0 < i < n - 1:
        res = minimize_scalar(lambda s: -U(r, q, z, A, theta, s), bounds=(lo, hi), method="bounded",
                              options={"xatol": 1e-10})
        if -res.fun > vals[i]:
            return float(res.x), float(-res.fun), ss, vals
    return float(ss[i]), float(vals[i]), ss, vals


def xstar(r, q, z):
    """Smallest x with mu >= tau under orders (q, -z), by bisection on the flow line."""
    _, tau = acq(r)
    tau = tau - 1e-13   # rounding guard at the plateau edge z = n(r), where mu = tau exactly
    if mu_pure(q + 5, q, z) < tau:
        return INF
    a, b_ = -z - 5, q + 5
    for _ in range(200):
        mid = 0.5 * (a + b_)
        if mu_pure(mid, q, z) >= tau:
            b_ = mid
        else:
            a = mid
    return b_


def J_quad(r):
    dT, tau = acq(r)
    xs = B / 2 * math.log(tau / (1 - tau))
    g = lambda x: f(x + 1) / (1.0 + math.exp(-(abs(x + 1) - abs(x - 1)) / B))
    return dT * integ(g, xs, INF, [1.0])


def C_quad(r, z, A=None):
    """Delta_T int_A f(x) mu_X dx under (1, -z); A defaults to the minimal pool U(z)."""
    if A is None:
        A = [(xstar(r, 1.0, z), INF)]
    return F_theta(r, 1.0, z, A, "L", 0.0)


def psi_quad(r, z):
    return C_quad(r, z) * math.exp(-z / B) * (1 - z / B) - K


def n_of(r):
    _, tau = acq(r)
    return B * math.log(tau / (1 - tau)) - 1


def G_closed(r):
    dT, tau = acq(r)
    return dT * (1 - tau) / 2 * (1 + 1 / B - math.log(tau / (1 - tau))) - K


def entry(r, q, z, A):
    """(e_H, e_L) = Pr(X in A | theta) under orders (q, -z)."""
    def Fz(x):
        if x == INF:
            return 1.0
        return 0.5 * math.exp(x / B) if x <= 0 else 1 - 0.5 * math.exp(-x / B)
    eH = sum(Fz(hi - q) - Fz(lo - q) for lo, hi in A)
    eL = sum(Fz(hi + z) - Fz(lo + z) for lo, hi in A)
    return eH, eL


def main() -> None:
    out = []
    def rec(name, val, note=""):
        out.append({"name": name, "value": repr(val), "note": note})
        print(f"{name:55s} {val!r} {note}")

    # 1. J(3) by quadrature of (F.3)
    rec("J(3) quadrature", J_quad(3.0), "note: [0.0955028924240038, 0.0955028924240039]")
    rec("(1-1/b)J(3)-k", 0.5 * J_quad(3.0) - K)
    # 2. r_J by root of quadrature J
    rJ = brentq(lambda r: 0.5 * J_quad(r) - K, 1.5, 2.5, xtol=1e-13)
    rec("r_J (quadrature root)", rJ, "note: 2.01551644106010")
    # r_C from B_r(M) = c by root finding (not by (A.11))
    def BM(r):
        tH = r / 2 + P_ ** 2 / (2 * r); gH = H_ - tH; gL = (ELL ** 2 - P_ ** 2) / (2 * r)
        return gL + M * (gH - gL) - C
    rC = brentq(BM, 2.0, 5.0, xtol=1e-14)
    rec("r_C (root of B_r(M)=c)", rC, "note: 3.5926585")
    rec("frak_r(k) root of Delta_T=k", brentq(lambda r: acq(r)[0] - K, 1.0001, 2.0, xtol=1e-14), "note: 1.2209975")
    # 3. G = Psi(n, r) by quadrature, and r_e
    for r in (1.62, 1.66, 2.0, 3.0):
        rec(f"G closed - Psi_quad(n) at r={r}", G_closed(r) - psi_quad(r, n_of(r)))
    re_ = brentq(lambda r: psi_quad(r, n_of(r)), 1.6, 1.7, xtol=1e-12)
    rec("r_e (quadrature root of Psi(n(r), r))", re_, "note: 1.6585908245511")
    rec("n(r_e)", n_of(re_), "note: 0.2469019")
    _, tau_e = acq(re_)
    rec("1/(4 tau(r_e))", 1 / (4 * tau_e), "note: 0.3840228")
    ne = n_of(re_)
    rec("U_H at r_e: k n/(b-n)", K * ne / (B - ne), "note: 0.0028167")
    # brute force the edge equilibrium at r_e: orders (1, -n), A = [1, inf)
    A = [(1.0, INF)]
    sH, vH, _, _ = best_resp(re_, 1.0, ne, A, "H")
    sL, vL, _, _ = best_resp(re_, 1.0, ne, A, "L", n=801)
    rec("edge eq: high BR, value", (sH, vH))
    rec("edge eq: low BR (should be n), value", (sL, vL))
    eH, eL = entry(re_, 1.0, ne, A)
    rec("edge eq: E, O_H", (0.5 * (eH + eL), 0.5 * eH))
    # 4. below the edge: max over z in [n, 1] of Psi by quadrature
    for r in (1.25, 1.4, 1.55, 1.62, 1.65, re_ - 1e-4):
        n = n_of(r)
        zs = np.linspace(n, 1.0, 81)
        vals = [psi_quad(r, float(zz)) for zz in zs]
        i = int(np.argmax(vals))
        rec(f"below edge r={r:.6f}: max Psi, argmax z, n", (max(vals), float(zs[i]), n))
    # 5. dPsi/dz sign on a grid (finite differences of the quadrature Psi)
    worst = -INF
    for r in np.linspace(1.3, rC - 1e-6, 25):
        n = n_of(r)
        zs = np.linspace(n, 1.0, 41)
        v = np.array([psi_quad(float(r), float(zz)) for zz in zs])
        worst = max(worst, float(np.diff(v).max()))
    rec("max finite difference of Psi in z on grid (should be < 0)", worst)
    # 6. slopes at r_e
    h = 1e-5
    def zU(r):
        n = n_of(r)
        if psi_quad(r, 1.0) >= 0:
            return 1.0
        if psi_quad(r, n) <= 0:
            return n
        return brentq(lambda zz: psi_quad(r, zz), n, 1.0, xtol=1e-13)
    rec("slope of n at r_e", (n_of(re_ + h) - n_of(re_)) / h, "note: about 0.34")
    rec("slope of z_U at r_e (right difference)", (zU(re_ + h) - zU(re_)) / h, "note: about 3.6")
    rec("slope of z_U at r_e (difference over [r_e+h, r_e+2h])", (zU(re_ + 2 * h) - zU(re_ + h)) / h)
    # 7. plateau equilibrium ES.5 at r = 2.5 and 3: brute-force both best responses
    for r in (2.0, 3.0):
        n = n_of(r)
        Gv = G_closed(r)
        pi = K / (Gv + K)
        y = 1 + B * math.log(1 / pi)
        A = [(y, INF)]
        sH, vH, _, _ = best_resp(r, 1.0, n, A, "H")
        sL, vL, _, _ = best_resp(r, 1.0, n, A, "L", n=801)
        eH, eL = entry(r, 1.0, n, A)
        _, tau = acq(r)
        mubar = (1 - eH) / ((1 - eH) + (1 - eL))
        rec(f"plateau eq r={r}: H BR, L BR, -n", (sH, sL, -n))
        rec(f"plateau eq r={r}: E, pi/(4tau), O_H, pi/4, mubar<tau", (0.5 * (eH + eL), pi / (4 * tau), 0.5 * eH, pi / 4, mubar < tau))
    # 8. holes at r = 3, full orders: least entry [x*, y] with (1-1/b) J_A = k
    r = 3.0
    dT, tau = acq(r)
    xs = B / 2 * math.log(tau / (1 - tau))
    g = lambda x: f(x + 1) / (1.0 + math.exp(-(abs(x + 1) - abs(x - 1)) / B))
    G0 = K / (0.5 * dT)
    y = brentq(lambda t: integ(g, xs, t, [1.0]) - G0, xs + 1e-6, 30.0, xtol=1e-12)
    eH, eL = entry(r, 1.0, 1.0, [(xs, y)])
    rec("r=3 least-entry y, entry", (y, 0.5 * (eH + eL)), "note: 1.9589, 0.15195")
    xc = brentq(lambda t: integ(g, t, INF, [1.0]) - G0, xs, 30.0, xtol=1e-12)
    eH, eL = entry(r, 1.0, 1.0, [(xc, INF)])
    rec("r=3 cutoff-family end x', entry", (xc, 0.5 * (eH + eL)), "note: 2.614, 0.15258")
    sH, _, _, _ = best_resp(r, 1.0, 1.0, [(xs, y)], "H")
    sL, _, _, _ = best_resp(r, 1.0, 1.0, [(xs, y)], "L")
    rec("r=3 least-entry set: H BR, L BR", (sH, sL))
    # 9. entry band rows
    for r in (1.7, 2.0, 2.5, 3.0, 3.5):
        n = n_of(r)
        _, tau = acq(r)
        pi = K / (G_closed(r) + K)
        zu = zU(r)
        xsu = xstar(r, 1.0, zu)
        eH, eL = entry(r, 1.0, zu, [(xsu, INF)])
        rec(f"band r={r}: [n, z_U], least E, minimal-pool E", (n, zu, pi / (4 * tau), 0.5 * (eH + eL)))
    # 10. the live-branch rows of section 5
    for r in (1.70, 1.80, 1.90, 2.00, 2.50, 3.00, 3.59):
        zu = zU(r)
        xsu = xstar(r, 1.0, zu)
        A = [(xsu, INF)]
        eH, eL = entry(r, 1.0, zu, A)
        rec(f"branch r={r}: q_L, x*, E, O_H, U_H, U_L",
            (-zu, xsu, 0.5 * (eH + eL), 0.5 * eH, U(r, 1.0, zu, A, "H", 1.0), U(r, 1.0, zu, A, "L", zu)))
    with (HERE / "recheck.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["name", "value", "note"])
        w.writeheader()
        w.writerows(out)


if __name__ == "__main__":
    main()
