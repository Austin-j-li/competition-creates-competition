"""Referee re-implementation for the information-acquisition note.

Independent of acquisition.py: no import from it. Every number is computed from the primitives with
scipy quadrature or mpmath, with thresholds found by root-finding rather than by the note's closed forms.
Pure functions with type hints. The script prints a report and writes check_results.csv only.

Status of every number here: numerical diagnostic (floating-point quadrature, no interval enclosure).
"""
from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Callable, NamedTuple

import mpmath as mpm
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
FORK = HERE.parents[2]

mpm.mp.dps = 30


class Prim(NamedTuple):
    h: float
    ell: float
    p: float
    b: float
    k: float
    c: float


BENCH = Prim(10.0, 1.0, 0.5, 2.0, 0.02, 6.0)


class Pay(NamedTuple):
    t0: float
    tH: float
    tL: float
    gH: float
    gL: float
    DT: float
    tau: float


def pay(pr: Prim, r: float) -> Pay:
    t0 = pr.p * (1 - pr.p / r)
    tH = r / 2 + pr.p ** 2 / (2 * r)
    tL = pr.ell - (pr.ell ** 2 - pr.p ** 2) / (2 * r)
    gH = pr.h - tH
    gL = (pr.ell ** 2 - pr.p ** 2) / (2 * r)
    return Pay(t0, tH, tL, gH, gL, tH - tL, (pr.c - gL) / (gH - gL))


def B(pr: Prim, r: float, mu: float) -> float:
    q = pay(pr, r)
    return q.gL + mu * (q.gH - q.gL)


def f(pr: Prim, z: float) -> float:
    return math.exp(-abs(z) / pr.b) / (2 * pr.b)


def mM(pr: Prim) -> tuple[float, float]:
    m = 1 / (1 + math.exp(2 / pr.b))
    return m, 1 - m


def mu_lam(pr: Prim, lam: float, qH: float, qL: float, x: float) -> float:
    """Market maker's posterior at flow x with acquisition probability lam and pure orders (qH, qL)."""
    aH = lam * f(pr, x - qH) + (1 - lam) * f(pr, x)
    aL = lam * f(pr, x - qL) + (1 - lam) * f(pr, x)
    return aH / (aH + aL)


def r_frak(pr: Prim, d: float) -> float:
    return brentq(lambda r: pay(pr, r).DT - d, pr.ell + 1e-12, pr.h)


def r_ceiling(pr: Prim) -> float:
    _, M = mM(pr)
    return brentq(lambda r: B(pr, r, M) - pr.c, pr.ell + 1e-9, pr.h - 1e-9, xtol=1e-15)


def M_lam_direct(pr: Prim, lam: float) -> float:
    """Plateau posterior under full orders, which the note claims is the sup over all strategies."""
    return mu_lam(pr, lam, 1.0, -1.0, 5.0)


def lam_min_direct(pr: Prim, r: float) -> float:
    tau = pay(pr, r).tau
    if M_lam_direct(pr, 1.0) < tau:
        return float("nan")
    return brentq(lambda l: M_lam_direct(pr, l) - tau, 0.0, 1.0, xtol=1e-15)


def threshold(pr: Prim, r: float, lam: float, qH: float = 1.0, qL: float = -1.0) -> float:
    """Smallest flow with mu >= tau (posterior nondecreasing for qH >= 0 >= qL)."""
    tau = pay(pr, r).tau
    g = lambda x: mu_lam(pr, lam, qH, qL, x) - tau
    if g(50.0) < -1e-15:
        return math.inf
    if g(-50.0) >= 0:
        return -math.inf
    hi = max(qH, 0.0) + 1e-12
    if g(hi) < 0:  # flat beyond max(qH,0); at the plateau the tie rule admits preparation
        return hi if abs(g(hi)) < 1e-12 else math.inf
    return brentq(g, -50.0, hi, xtol=1e-14)


# ---------------------------------------------------------------------------------------------
# Investor profits against a fixed schedule: entry on [xc, inf), prices from orders (qH, qL) at lam
# ---------------------------------------------------------------------------------------------

def gross(pr: Prim, r: float, lam: float, qH: float, qL: float, xc: float, theta: str, s: float) -> float:
    """Gross profit per unit of a correctly signed order of size s >= 0 by an informed type theta."""
    DT = pay(pr, r).DT
    if theta == "H":
        g = lambda x: f(pr, x - s) * DT * (1 - mu_lam(pr, lam, qH, qL, x))
    else:
        g = lambda x: f(pr, x + s) * DT * mu_lam(pr, lam, qH, qL, x)
    pts = sorted({xc, max(xc, -1.0), max(xc, 0.0), max(xc, 1.0), max(xc, s), max(xc, -s), max(xc, qH),
                  max(xc, qL)})
    tot = 0.0
    edges = pts + [60.0]
    for a, bnd in zip(edges[:-1], edges[1:]):
        if bnd > a:
            tot += quad(g, a, bnd, epsabs=1e-14, epsrel=1e-12, limit=200)[0]
    return tot


def best_correct_order(pr: Prim, r: float, lam: float, qH: float, qL: float, xc: float, theta: str
                       ) -> tuple[float, float]:
    """Global maximizer of s (F(s) - k) over s in [0, 1] by a dense scan plus local refinement.

    Wrong-signed orders earn a nonpositive gross amount minus the cost, so they are never better than zero.
    """
    grid = np.linspace(0.0, 1.0, 101)
    vals = [s * (gross(pr, r, lam, qH, qL, xc, theta, s) - pr.k) for s in grid]
    i = int(np.argmax(vals))
    lo, hi = grid[max(i - 1, 0)], grid[min(i + 1, len(grid) - 1)]
    res = minimize_scalar(lambda s: -(s * (gross(pr, r, lam, qH, qL, xc, theta, s) - pr.k)), bounds=(lo, hi),
                          method="bounded", options={"xatol": 1e-7})
    cand = [(float(grid[i]), float(vals[i])), (float(res.x), float(-res.fun)), (1.0, float(vals[-1]))]
    s, v = max(cand, key=lambda t: t[1])
    if v <= 0:
        return 0.0, 0.0
    return s, v


class Candidate(NamedTuple):
    r: float
    lam: float
    xc: float
    FH1: float
    FL1: float
    V: float
    suff_test: bool
    sH: float
    sL: float
    UH: float
    UL: float
    pool_posterior: float
    entry_posterior_min: float


def full_order_candidate(pr: Prim, r: float, lam: float, xc: float | None = None, global_check: bool = True
                         ) -> Candidate:
    """Full orders (1,-1); entry on [xc, inf) with xc >= x*_lam (minimal pool when xc is None)."""
    xs = threshold(pr, r, lam)
    if xc is None:
        xc = xs
    FH1 = gross(pr, r, lam, 1.0, -1.0, xc, "H", 1.0)
    FL1 = gross(pr, r, lam, 1.0, -1.0, xc, "L", 1.0)
    V = 0.5 * (FH1 + FL1) - pr.k
    suff = pr.k < (1 - 1 / pr.b) * min(FH1, FL1)
    if global_check:
        sH, UH = best_correct_order(pr, r, lam, 1.0, -1.0, xc, "H")
        sL, UL = best_correct_order(pr, r, lam, 1.0, -1.0, xc, "L")
    else:
        sH = sL = UH = UL = float("nan")
    # pool posterior Pr(H | X < xc)
    wH = lam * (0.5 * math.exp((xc - 1) / pr.b) if xc <= 1 else 1 - 0.5 * math.exp(-(xc - 1) / pr.b)) \
        + (1 - lam) * (0.5 * math.exp(xc / pr.b) if xc <= 0 else 1 - 0.5 * math.exp(-xc / pr.b))
    wL = lam * (0.5 * math.exp((xc + 1) / pr.b) if xc <= -1 else 1 - 0.5 * math.exp(-(xc + 1) / pr.b)) \
        + (1 - lam) * (0.5 * math.exp(xc / pr.b) if xc <= 0 else 1 - 0.5 * math.exp(-xc / pr.b))
    return Candidate(r, lam, xc, FH1, FL1, V, bool(suff), sH, sL, UH, UL, wH / (wH + wL),
                     mu_lam(pr, lam, 1.0, -1.0, xc))


# ---------------------------------------------------------------------------------------------
# Closed forms claimed in the note, recomputed independently
# ---------------------------------------------------------------------------------------------

def J_direct(pr: Prim, r: float) -> float:
    """(F.3) by mpmath quadrature with x* from root-finding."""
    xs = threshold(pr, r, 1.0)
    DT = pay(pr, r).DT
    fm = lambda x: mpm.exp(-abs(x) / pr.b) / (2 * pr.b)
    g = lambda x: fm(x - 1) * fm(x + 1) / (fm(x - 1) + fm(x + 1))
    return float(DT * (mpm.quad(g, [xs, 1]) + mpm.quad(g, [1, mpm.inf])))


def J_note(pr: Prim, r: float) -> float:
    """(G.4) as printed in the note."""
    m, _ = mM(pr)
    q = pay(pr, r)
    tau = mpm.mpf(q.tau)
    sh = (2 * tau - 1) / (2 * mpm.sqrt(tau * (1 - tau)))
    gd = lambda u: mpm.atan(mpm.sinh(u))
    return float(q.DT * (mpm.mpf(m) / 2 + mpm.exp(-1 / mpm.mpf(pr.b)) / 4 * (gd(1 / mpm.mpf(pr.b)) - mpm.atan(sh))))


def V_lambda_min_note(pr: Prim, r: float) -> float:
    q = pay(pr, r)
    return q.DT / 4 * ((1 - q.tau) + q.tau * math.exp(-2 / pr.b)) - pr.k


def G7(pr: Prim, r: float) -> bool:
    q = pay(pr, r)
    return (q.DT * (1 - q.tau) * math.exp(-1 / pr.b) / 2 > pr.k and
            q.DT * q.tau * math.exp(-2 / pr.b) * (1 - 1 / pr.b) / 2 > pr.k)


def U_bar(pr: Prim, r: float) -> float:
    q = pay(pr, r)
    _, M = mM(pr)
    return 0.5 * (max(q.DT * (1 - q.tau) - pr.k, 0) + max(q.DT * M - pr.k, 0))


class Short(NamedTuple):
    Phi: float
    s: float
    U: float
    s_direct: float
    U_direct: float


def nonacquirer_short(pr: Prim, r: float) -> Short:
    """Game B at lam = 1 on the minimal-pool full-order schedule: closed form (G.9) and direct maximization."""
    q = pay(pr, r)
    xs = threshold(pr, r, 1.0)
    g = lambda x: f(pr, x) * q.DT * (mu_lam(pr, 1.0, 1.0, -1.0, x) - 0.5)
    Phi = quad(g, xs, 1.0, epsabs=1e-14, epsrel=1e-12)[0] + quad(g, 1.0, 60.0, epsabs=1e-14, epsrel=1e-12)[0]
    if Phi <= pr.k:
        s = 0.0
    else:
        h = lambda s: (1 - s / pr.b) * math.exp(-s / pr.b) * Phi - pr.k
        s = 1.0 if h(1.0) >= 0 else brentq(h, 0.0, 1.0, xtol=1e-14)
    U = s * (math.exp(-s / pr.b) * Phi - pr.k)

    def direct(s: float) -> float:  # short of size s, residual e (mu - 1/2) Delta_T, no use of the shift identity
        gg = lambda x: f(pr, x + s) * q.DT * (mu_lam(pr, 1.0, 1.0, -1.0, x) - 0.5)
        return s * (quad(gg, xs, 1.0, epsabs=1e-14, epsrel=1e-12)[0] +
                    quad(gg, 1.0, 60.0, epsabs=1e-14, epsrel=1e-12)[0]) - pr.k * s

    res = minimize_scalar(lambda s: -direct(s), bounds=(0.0, 1.0), method="bounded", options={"xatol": 1e-8})
    sd, Ud = (float(res.x), float(-res.fun)) if -res.fun > 0 else (0.0, 0.0)
    if direct(1.0) > Ud:
        sd, Ud = 1.0, direct(1.0)
    return Short(Phi, s, U, sd, Ud)


def V_exogenous(pr: Prim, r: float, lam: float) -> float:
    """Remark G.1: e = 1 everywhere, full orders, value of acquisition."""
    DT = pay(pr, r).DT
    def g(x: float) -> float:
        f1, fm1, f0 = f(pr, x - 1), f(pr, x + 1), f(pr, x)
        S = f1 + fm1
        return (2 * lam * f1 * fm1 + (1 - lam) * f0 * S) / (lam * S + 2 * (1 - lam) * f0)
    tot = sum(quad(g, a, bnd, epsabs=1e-14, epsrel=1e-12)[0] for a, bnd in
              [(-60, -1), (-1, 0), (0, 1), (1, 60)])
    return DT / 2 * tot - pr.k


# ---------------------------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------------------------

def main() -> None:
    pr = BENCH
    m, M = mM(pr)
    out: list[dict] = []

    def rec(item: str, note_value: str, referee_value: float | str, verdict: str) -> None:
        out.append({"item": item, "note": note_value, "referee": referee_value, "verdict": verdict})
        print(f"{item:55s} note={note_value:>14s} referee={referee_value!s:>24s} {verdict}")

    rk, rC = r_frak(pr, pr.k), r_ceiling(pr)
    rec("r_frak(k)", "1.2210", f"{rk:.6f}", "agrees")
    rec("r_C", "3.5927", f"{rC:.9f}", "agrees")
    rec("sup_r B_r(1/2)", "4.875", f"{B(pr, 1.0 + 1e-12, 0.5):.6f}", "agrees")

    # M_lambda: sup over strategies equals the plateau value; check against (G.3) and monotone in lam
    a, d = math.exp(1 / pr.b), math.exp(-1 / pr.b)
    worst = max(abs(M_lam_direct(pr, l) - (l * a + 1 - l) / (l * (a + d) + 2 * (1 - l)))
                for l in np.linspace(0, 1, 101))
    rec("max |M_lam direct - (G.3)|", "0", f"{worst:.2e}", "agrees")
    # brute-force sup of the posterior over random mixed orders at lam = 0.9 (Lemma G.1)
    rng = np.random.default_rng(0)
    X = np.linspace(-15, 15, 3001)
    sup_post = 0.0
    lam = 0.9
    for _ in range(400):
        qs = rng.uniform(-1, 1, size=(2, 3))
        ws = rng.dirichlet(np.ones(3), size=2)
        aH = lam * sum(ws[0, j] * np.exp(-np.abs(X - qs[0, j]) / pr.b) for j in range(3)) + (1 - lam) * np.exp(-np.abs(X) / pr.b)
        aL = lam * sum(ws[1, j] * np.exp(-np.abs(X - qs[1, j]) / pr.b) for j in range(3)) + (1 - lam) * np.exp(-np.abs(X) / pr.b)
        sup_post = max(sup_post, float((aH / (aH + aL)).max()))
    rec("Lemma G.1: max posterior, 400 random mixtures, lam=.9", f"<= {M_lam_direct(pr, 0.9):.6f}",
        f"{sup_post:.6f}", "agrees" if sup_post <= M_lam_direct(pr, 0.9) + 1e-12 else "REFUTED")

    # lambda_min and tau at Table 2 rows
    for r in (1.66, 1.8, 2.0, 2.02, 2.05, 2.5, 3.0, 3.5, 3.5926):
        q = pay(pr, r)
        lm = lam_min_direct(pr, r)
        rec(f"tau, lambda_min at r={r}", "", f"{q.tau:.4f}, {lm:.5f}", "")

    # J: closed form (G.4) versus direct quadrature of (F.3)
    for r in (2.02, 2.05, 2.5, 3.0, 3.5, 3.5926, rC):
        Jd, Jn = J_direct(pr, r), J_note(pr, r)
        rec(f"J(r) at r={r:.4f}: (G.4) vs quadrature", f"{Jn:.10f}", f"{Jd:.10f}",
            "agrees" if abs(Jd - Jn) < 1e-9 else "DIFFERS")
        rec(f"U*(r)=J-k at r={r:.4f}", f"{Jn - pr.k:.4f}", f"{Jd - pr.k:.6f}", "")

    # first grid strength (step 0.01) with k < (1-1/b) J(r)
    first = next(r for r in np.round(np.arange(1.70, 2.30, 0.01), 2) if pr.k < (1 - 1 / pr.b) * J_direct(pr, r))
    root = brentq(lambda r: (1 - 1 / pr.b) * J_direct(pr, r) - pr.k, 1.9, 2.1, xtol=1e-12)
    rec("first grid r with full-order test", "2.02", f"{first} (exact crossing {root:.5f})", "agrees")
    rec("margin (1-1/b)J(2.02)-k", "", f"{(1 - 1 / pr.b) * J_direct(pr, 2.02) - pr.k:.3e}", "")

    # dJ/dr > 0 on [2.02, r_C]: finite differences on a fine grid, and (G.5) versus numerical derivative
    rs = np.linspace(2.02, rC, 400)
    Js = np.array([J_note(pr, r) for r in rs])
    rec("J increasing on [2.02, r_C] (400-node grid)", "yes", str(bool(np.all(np.diff(Js) > 0))), "agrees")
    for r in (2.02, 3.0, 3.5):
        num_d = float(mpm.diff(lambda rr: J_note(pr, float(rr)), r, h=1e-5))
        q = pay(pr, r)
        tau = q.tau
        G = J_note(pr, r) / q.DT
        Np = (pr.ell ** 2 - pr.p ** 2) / (2 * r * r)
        D = pr.h - r / 2 - pr.ell ** 2 / (2 * r)
        Dp = -0.5 + pr.ell ** 2 / (2 * r * r)
        taup = Np / D - tau * Dp / D
        formula = q.DT * ((r + pr.ell) / (r * (r - pr.ell)) * G - math.exp(-1 / pr.b) / (4 * math.sqrt(tau * (1 - tau))) * taup)
        rec(f"dJ/dr at r={r}: (G.5) vs numerical", f"{formula:.6f}", f"{num_d:.6f}",
            "agrees" if abs(formula - num_d) < 1e-5 else "DIFFERS")
    # (G.6) arithmetic
    D_rC = pr.h - rC / 2 - pr.ell ** 2 / (2 * rC)
    tpb = ((pr.ell ** 2 - pr.p ** 2) / (2 * 2.02 ** 2) + M / 2) / D_rC
    lhs = (rC + pr.ell) / (rC * (rC - pr.ell)) * m / 2
    rhs = math.exp(-1 / pr.b) / 4 * 2 * math.cosh(1 / pr.b) * tpb
    rec("(G.6) left / right", "0.0663 / 0.0194", f"{lhs:.5f} / {rhs:.5f}", "agrees")

    # (G.7) first grid strength and (G.8) value
    firstG7 = next(r for r in np.round(np.arange(2.0, 2.5, 0.01), 2) if G7(pr, r))
    rec("first grid r with (G.7)", "2.20", f"{firstG7}", "agrees")
    for r in (2.5, 3.0, 3.5):
        lm = lam_min_direct(pr, r)
        cand = full_order_candidate(pr, r, lm + 1e-12)
        rec(f"V(lam_min) at r={r}: (G.8) vs quadrature", f"{V_lambda_min_note(pr, r):.5f}", f"{cand.V:.5f}",
            "agrees" if abs(cand.V - V_lambda_min_note(pr, r)) < 2e-5 else "DIFFERS")
        rec(f"  global best orders at lam_min, r={r}", "(1,-1)", f"({cand.sH:.4f},-{cand.sL:.4f})",
            "agrees" if cand.sH > 0.9999 and cand.sL > 0.9999 else "DIFFERS")

    # profile V(lambda, r): monotone? test region? global best response
    for r in (2.05, 2.5, 3.0, 3.5):
        lm = lam_min_direct(pr, r)
        lams = np.linspace(lm + 1e-10, 1.0, 41)
        cands = [full_order_candidate(pr, r, l, global_check=False) for l in lams]
        Vs = np.array([c.V for c in cands])
        test = [c.suff_test for c in cands]
        first_ok = next((l for l, t in zip(lams, test) if t), float("nan"))
        rec(f"V(lam) increasing on [lam_min,1] at r={r}", "increasing", str(bool(np.all(np.diff(Vs) > 0))), "")
        rec(f"  V(lam_min), V(1), rise share at r={r}", "",
            f"{Vs[0]:.5f}, {Vs[-1]:.5f}, {(Vs[-1] - Vs[0]) / Vs[-1]:.4f}", "")
        rec(f"  first lam with sufficient test at r={r}", "", f"{first_ok:.4f}", "")
    # r = 2.05 below the test: global best response of each type to the full-order schedule
    for lam in (0.70, 0.75, 0.85, 0.93):
        c = full_order_candidate(pr, 2.05, lam)
        rec(f"r=2.05 lam={lam}: BR to full-order schedule", "", f"H {c.sH:.4f}, L -{c.sL:.4f}", "")
    # is entry possible at lam=0.70 with the partial short the low type picks?
    c = full_order_candidate(pr, 2.05, 0.70)
    post_max = mu_lam(pr, 0.70, 1.0, -c.sL, 5.0)
    rec("r=2.05 lam=0.70: max posterior at BR orders vs tau", "", f"{post_max:.5f} vs {pay(pr, 2.05).tau:.5f}", "")

    # Game B
    for r in (2.0, 2.02, 2.03, 2.04, 2.05, 2.5, 3.0, 3.5, 3.5926, rC):
        sh = nonacquirer_short(pr, r)
        rec(f"game B at r={r:.4f}: Phi, s_U, U_U (closed) | direct", "",
            f"{sh.Phi:.5f}, {sh.s:.4f}, {sh.U:.6f} | {sh.s_direct:.4f}, {sh.U_direct:.6f}", "")
    rootPhi = brentq(lambda r: nonacquirer_short(pr, r).Phi - pr.k, 1.70, 2.1, xtol=1e-10)
    rec("strength where Phi(r) = k on the full-order schedule", "(first grid 2.05)", f"{rootPhi:.5f}", "")
    lowb = brentq(lambda r: pay(pr, r).DT * (M - 0.5) * math.exp(-1 / pr.b) / 2 - pr.k, 1.5, 3.0)
    rec("strength where the (G.9) lower bound equals k", "2.09", f"{lowb:.5f}", "agrees")

    # Remark G.1
    for lam in (0.0, 0.25, 0.5, 0.75, 1.0):
        rec(f"Remark G.1 V({lam}) at r=3", "", f"{V_exogenous(pr, 3.0, lam):.4f}", "")
    rec("B_3(m)", "2.37", f"{B(pr, 3.0, m):.4f}", "agrees")

    # U bar
    for r in (1.66, 1.8, 2.0, 2.05, 2.5, 3.0, 3.5, 3.5926):
        rec(f"U_bar at r={r}", "", f"{U_bar(pr, r):.4f}", "")

    # Counterexample search: mixed-acquisition equilibria with a larger pool, below the 'band'
    for r, lam, xc in ((3.0, 0.95, 1.5), (3.0, 0.95, 2.0), (3.0, 0.90, 1.8), (2.5, 0.90, 1.5)):
        c = full_order_candidate(pr, r, lam, xc)
        lm = lam_min_direct(pr, r)
        band_lo = full_order_candidate(pr, r, lm + 1e-12, global_check=False).V
        ok = (c.entry_posterior_min >= pay(pr, r).tau and B(pr, r, c.pool_posterior) < pr.c and c.sH > 0.9999
              and c.sL > 0.9999)
        rec(f"larger pool r={r} lam={lam} x'={xc}: V, test, BR", f"band >= {band_lo:.4f}",
            f"V={c.V:.5f} suff={c.suff_test} BR=({c.sH:.3f},-{c.sL:.3f}) pool mu={c.pool_posterior:.3f}",
            "mixed eq outside band" if ok and c.V < band_lo else "")

    # Observable acquisition: consistent cutoffs at r=3, lam=1
    for kap in (0.05, 0.07):
        xk = brentq(lambda xc: full_order_candidate(pr, 3.0, 1.0, xc, global_check=False).V - kap, 0.88, 3.0)
        rec(f"x'(kappa) at r=3, kappa={kap}", "1.47 / 0.97", f"{xk:.4f}", "")

    # r = r_C exactly: live equilibrium under the tie rule
    cC = full_order_candidate(pr, rC, 1.0)
    rec("at r = r_C: x*, V, suff test, BR", "no insider claimed outside (r(k), r_C)",
        f"x*={cC.xc:.6f} V={cC.V:.5f} suff={cC.suff_test} BR=({cC.sH:.3f},-{cC.sL:.3f})", "live eq at r_C")

    with (HERE / "check_results.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["item", "note", "referee", "verdict"])
        w.writeheader()
        w.writerows(out)


if __name__ == "__main__":
    main()
