"""Independent re-computation of the key numbers of note.md. Writes referee/recheck.csv only.

This module does not import core.py, grid.py, or solve.py. It rebuilds the auction payoffs by integrating
the sale rule over the uniform incumbent, integrates the existence statistic (A.7) and the state entry
probabilities in the flow variable x (not in the arcsine variable of Lemma CD.6), and evaluates investor
payoffs against fixed schedules with adaptive quadrature in x. Every number here is a numerical diagnostic.
"""
from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path

import mpmath as mp

mp.mp.dps = 18
HERE = Path(__file__).resolve().parent


@dataclass(frozen=True)
class Prim:
    h: mp.mpf = mp.mpf(10)
    ell: mp.mpf = mp.mpf(1)
    p: mp.mpf = mp.mpf("0.5")
    b: mp.mpf = mp.mpf(2)
    k: mp.mpf = mp.mpf("0.02")


@dataclass(frozen=True)
class Pay:
    r: mp.mpf
    t0: mp.mpf
    tH: mp.mpf
    tL: mp.mpf
    gH: mp.mpf
    gL: mp.mpf
    DT: mp.mpf
    wL: mp.mpf


@dataclass(frozen=True)
class Law:
    atoms: tuple = ()
    uniforms: tuple = ()


PRIM = Prim()


def pay_by_integration(pr: Prim, r: float) -> Pay:
    """Sale rule integrated over R ~ U[0, r]; independent of the closed forms (4)."""
    r = mp.mpf(r)
    pts = [0, pr.p, pr.ell, r]
    avg = lambda fn: mp.quad(fn, pts) / r  # noqa: E731
    t0 = avg(lambda u: pr.p if u >= pr.p else 0)
    tH = avg(lambda u: max(pr.p, u))
    tL = avg(lambda u: max(pr.p, min(u, pr.ell)))
    gH = avg(lambda u: max(pr.h - max(pr.p, u), 0))
    gL = avg(lambda u: max(pr.ell - max(pr.p, u), 0))
    return Pay(r, t0, tH, tL, gH, gL, tH - tL, tL - t0)


def m_of(pr: Prim) -> mp.mpf:
    return 1 / (1 + mp.e ** (2 / pr.b))


def B(pay: Pay, mu):
    return pay.gL + mu * (pay.gH - pay.gL)


def G(law: Law, y) -> mp.mpf:
    out = mp.mpf(0)
    for loc, mass in law.atoms:
        out += mass if y >= loc else 0
    for lo, hi, mass in law.uniforms:
        out += mass * min(max((y - lo) / (hi - lo), 0), 1)
    return out


def f(pr: Prim, z):
    return mp.e ** (-abs(z) / pr.b) / (2 * pr.b)


def F(pr: Prim, z):
    return mp.e ** (z / pr.b) / 2 if z <= 0 else 1 - mp.e ** (-z / pr.b) / 2


def mu_pure(pr: Prim, x, qH, qL):
    a, c = f(pr, x - qH), f(pr, x - qL)
    return a / (a + c)


def x_breaks(pr: Prim, pay: Pay, law: Law, qH, qL, extra=()) -> list:
    """Flow points where entry can jump or kink under pure orders (qH, qL) with qH > qL."""
    pts = [qL, qH, *extra]
    locs = [loc for loc, _ in law.atoms] + [v for lo, hi, _ in law.uniforms for v in (lo, hi)]
    d = qH - qL
    for c in locs:
        mu = (c - pay.gL) / (pay.gH - pay.gL)
        if 0 < mu < 1:
            # on (qL, qH): logit mu = (2x - qH - qL)/b
            x = (pr.b * mp.log(mu / (1 - mu)) + qH + qL) / 2
            if qL < x < qH:
                pts.append(x)
    return sorted(set(pts))


def entry(pr: Prim, pay: Pay, law: Law, x, qH=1, qL=-1, cutoff=-mp.inf):
    if x < cutoff:
        return mp.mpf(0)
    return G(law, B(pay, mu_pure(pr, x, qH, qL)))


def integrate(fn, pts) -> mp.mpf:
    return mp.quad(fn, [-mp.inf, *pts, mp.inf])


def full_order_stats(pr: Prim, pay: Pay, law: Law, cutoff=-mp.inf) -> dict:
    extra = () if cutoff == -mp.inf else (cutoff,)
    pts = x_breaks(pr, pay, law, 1, -1, extra)
    e = lambda x: entry(pr, pay, law, x, 1, -1, cutoff)  # noqa: E731
    kappa = lambda x: f(pr, x - 1) * f(pr, x + 1) / (f(pr, x - 1) + f(pr, x + 1))  # noqa: E731
    J = pay.DT * integrate(lambda x: e(x) * kappa(x), pts)
    eH = integrate(lambda x: e(x) * f(pr, x - 1), pts)
    eL = integrate(lambda x: e(x) * f(pr, x + 1), pts)
    pool = integrate(lambda x: (1 if e(x) == 0 else 0) * (f(pr, x - 1) + f(pr, x + 1)) / 2, pts)
    var_mu = integrate(lambda x: mu_pure(pr, x, 1, -1) ** 2 * (f(pr, x - 1) + f(pr, x + 1)) / 2, pts) - mp.mpf(1) / 4
    return {"J": J, "eH": eH, "eL": eL, "E": (eH + eL) / 2, "O_H": eH / 2, "pool": pool, "var_mu": var_mu}


def investor_payoff(pr: Prim, pay: Pay, law: Law, qH, qL, theta: str, s, cutoff=-mp.inf) -> mp.mpf:
    """U_theta(s) for a correctly signed order of size s >= 0 against the fixed schedule at (qH, qL)."""
    extra = [cutoff] if cutoff != -mp.inf else []
    pts = x_breaks(pr, pay, law, qH, qL, extra)
    shift = s if theta == "H" else -s
    pts = sorted(set(pts + [shift]))

    def integrand(x):
        e = entry(pr, pay, law, x, qH, qL, cutoff)
        mu = mu_pure(pr, x, qH, qL)
        A = e * pay.DT * ((1 - mu) if theta == "H" else mu)
        return f(pr, x - shift) * A

    return s * integrate(integrand, pts) - pr.k * s


def best_response_scan(pr: Prim, pay: Pay, law: Law, qH, qL, theta: str, cutoff=-mp.inf) -> tuple:
    """Scan s on [0, 1] with step 0.01, refine by golden-section search around the best cell."""
    grid = [mp.mpf(i) / 100 for i in range(101)]
    vals = [investor_payoff(pr, pay, law, qH, qL, theta, s, cutoff) for s in grid]
    i = max(range(101), key=lambda j: vals[j])
    lo, hi = grid[max(i - 1, 0)], grid[min(i + 1, 100)]
    g = lambda s: -investor_payoff(pr, pay, law, qH, qL, theta, s, cutoff)  # noqa: E731
    phi = (mp.sqrt(5) - 1) / 2
    a, c = lo, hi
    for _ in range(40):
        x1, x2 = c - phi * (c - a), a + phi * (c - a)
        if g(x1) < g(x2):
            c = x2
        else:
            a = x1
    s_star = (a + c) / 2
    cands = [(vals[i], grid[i]), (-g(s_star), s_star), (vals[100], grid[100]), (vals[0], grid[0])]
    best = max(cands, key=lambda t: t[0])
    return best[1], best[0]


def pool_prob_pure(pr: Prim, pay: Pay, law: Law, qH, qL) -> mp.mpf:
    pts = x_breaks(pr, pay, law, qH, qL)
    return integrate(lambda x: (1 if entry(pr, pay, law, x, qH, qL) == 0 else 0)
                     * (f(pr, x - qH) + f(pr, x - qL)) / 2, pts)


def ceiling(pr: Prim, c) -> mp.mpf:
    M = 1 - m_of(pr)
    return mp.findroot(lambda r: B(pay_closed(pr, r), M) - c, (pr.ell + mp.mpf("1e-9"), pr.h - mp.mpf("1e-9")),
                       solver="bisect")


def pay_closed(pr: Prim, r) -> Pay:
    """Closed forms (4), used only for root finding after the integration check below."""
    r = mp.mpf(r)
    t0 = pr.p * (1 - pr.p / r)
    tH = r / 2 + pr.p ** 2 / (2 * r)
    tL = pr.ell - (pr.ell ** 2 - pr.p ** 2) / (2 * r)
    gH = pr.h - tH
    gL = (pr.ell ** 2 - pr.p ** 2) / (2 * r)
    return Pay(r, t0, tH, tL, gH, gL, tH - tL, tL - t0)


def bisect(fn, a, b_, tol=mp.mpf("1e-9")) -> mp.mpf:
    fa = fn(a)
    for _ in range(200):
        mid = (a + b_) / 2
        fm = fn(mid)
        if (fm > 0) == (fa > 0):
            a, fa = mid, fm
        else:
            b_ = mid
        if b_ - a < tol:
            break
    return (a + b_) / 2


def main() -> None:
    pr = PRIM
    m = m_of(pr)
    M = 1 - m
    rows: list[dict] = []

    def add(claim: str, note_value: str, value, tol: float, where: str) -> None:
        v = float(value)
        try:
            nv = float(note_value)
            ok = "info" if math.isnan(nv) else abs(v - nv) <= tol
        except ValueError:
            ok = "info"
        rows.append({"claim": claim, "where": where, "note_value": note_value, "recomputed": f"{v:.10g}",
                     "tolerance": tol, "agrees": ok})
        print(f"{claim:60s} note={note_value:>12s} recomputed={v:.8g} ok={ok}", flush=True)

    # payoffs: integration versus closed forms
    p3 = pay_by_integration(pr, 3)
    pc = pay_closed(pr, 3)
    add("max |payoff(integrated) - payoff(4)| at r=3", "0",
        max(abs(getattr(p3, a) - getattr(pc, a)) for a in ("t0", "tH", "tL", "gH", "gL")), 1e-15, "Section 3")
    add("B_3(m)", "2.366", B(p3, m), 5e-4, "T1")
    add("B_3(1/2)", "4.292", B(p3, mp.mpf(1) / 2), 5e-4, "T1")
    add("B_3(M)", "6.217", B(p3, M), 5e-4, "T1")
    add("required floor mass k/[(1-1/b) m Delta_T] at r=3", "0.2231", pr.k / ((1 - 1 / pr.b) * m * p3.DT), 5e-5,
        "CD.5")
    tau = (6 - p3.gL) / (p3.gH - p3.gL)
    xstar = pr.b / 2 * mp.log(tau / (1 - tau))
    add("x* at r=3 (fork)", "0.8712", xstar, 5e-5, "T3")
    J_closed = p3.DT * (m / 2 + mp.e ** (-1 / pr.b) / 2 * (mp.asin(mp.sqrt(M)) - mp.asin(mp.sqrt(tau))))
    add("J(3) fork, arcsine closed form", "0.0955029", J_closed, 5e-8, "CD.6")

    laws = {
        "fork_point_6": (Law(atoms=((mp.mpf(6), 1),)), {"pool": "0.636", "J": "0.0955", "E": "0.3637", "O_H": "0.2656"}),
        "U[5.9,6.1]": (Law(uniforms=((mp.mpf("5.9"), mp.mpf("6.1"), 1),)),
                       {"pool": "0.627", "J": "0.0955", "E": "0.3636", "O_H": "0.2655"}),
        "U[5.5,6.5]": (Law(uniforms=((mp.mpf("5.5"), mp.mpf("6.5"), 1),)),
                       {"pool": "0.592", "J": "0.0711", "E": "0.2699", "O_H": "0.1966"}),
        "U[3,9]": (Law(uniforms=((mp.mpf(3), mp.mpf(9), 1),)),
                   {"pool": "0.401", "J": "0.0699", "E": "0.2546", "O_H": "0.1776"}),
        "U[0,12]": (Law(uniforms=((mp.mpf(0), mp.mpf(12), 1),)),
                    {"pool": "0", "J": "0.0989", "E": "0.3576", "O_H": "0.2085"}),
        "benchmark": (Law(atoms=((mp.mpf(1), mp.mpf("0.25")), (mp.mpf(6), mp.mpf("0.75")))),
                      {"pool": "0", "J": "0.1407", "E": "0.5228", "O_H": "0.3242"}),
    }
    stats = {}
    for name, (law, note) in laws.items():
        st = full_order_stats(pr, p3, law)
        stats[name] = st
        for key, tol in (("pool", 5e-4), ("J", 5e-5), ("E", 5e-5), ("O_H", 5e-5)):
            add(f"T1 {name} {key}", note[key], st[key], tol, "T1")
    add("J(3) fork, x-integration", "0.0955029", stats["fork_point_6"]["J"], 5e-8, "CD.6")
    # O_H uplift for U[0,12]
    beta = (p3.gH - p3.gL) / 12
    add("U[0,12] beta*Var(mu_P) at r=3", "0.0297", beta * stats["U[0,12]"]["var_mu"], 5e-5, "CD.11 text")
    add("U[0,12] O_H - g_half/2 at r=3", "0.0297",
        stats["U[0,12]"]["O_H"] - B(p3, mp.mpf(1) / 2) / 24, 5e-5, "CD.11 text")

    # uniform-noise expansion, Proposition CD.13(c)
    w1 = (2 * tau - 1) / (2 * (tau * (1 - tau)) ** mp.mpf(1.5))
    for eps in ("0.01", "0.05", "0.1"):
        e_ = mp.mpf(eps)
        st = full_order_stats(pr, p3, Law(uniforms=((6 - e_, 6 + e_, 1),)))
        delta = e_ / (p3.gH - p3.gL)
        pred = -p3.DT * mp.e ** (-1 / pr.b) / 24 * w1 * delta ** 2
        add(f"CD.13(c) J_eps - J, eps={eps} (exact)", f"{float(pred):.6g}", st["J"] - stats["fork_point_6"]["J"],
            abs(float(pred)) * 0.01, "CD.13(c)")
    st = full_order_stats(pr, p3, Law(uniforms=((mp.mpf("5.9"), mp.mpf("6.1"), 1),)))
    add("T3 eps=0.1 entry change", "-6e-5", st["E"] - stats["fork_point_6"]["E"], 1e-5, "T3 text")
    for eps, note_J, note_x in (("0.25", "0.089611", "2.478"), ("0.5", "0.071124", "1.949"),
                                 ("1.0", "0.064245", "1.621"), ("1.5", "0.064007", "1.498")):
        e_ = mp.mpf(eps)
        law = Law(uniforms=((6 - e_, 6 + e_, 1),))
        st = full_order_stats(pr, p3, law)
        add(f"T3 J eps={eps}", note_J, st["J"], 5e-6, "T3")
        tau_m = (6 - e_ - p3.gL) / (p3.gH - p3.gL)
        z0 = pr.b / 2 * mp.log(tau_m / (1 - tau_m))
        g = lambda xc: (1 - 1 / pr.b) * full_order_stats(pr, p3, law, xc)["J"] - pr.k  # noqa: E731
        add(f"T3 full-order cutoff end eps={eps}", note_x, bisect(g, z0 + mp.mpf("1e-6"), mp.mpf(4), mp.mpf("1e-6")),
            2e-3, "T3")

    # full-order cutoff end for the fork, closed form and by bisection
    xe = 1 + pr.b * mp.log((1 - 1 / pr.b) * m * p3.DT / (2 * pr.k))
    add("fork full-order cutoff end, closed form", "2.614", xe, 5e-4, "after CD.8")
    law6 = laws["fork_point_6"][0]
    g6 = lambda xc: (1 - 1 / pr.b) * full_order_stats(pr, p3, law6, xc)["J"] - pr.k  # noqa: E731
    add("fork full-order cutoff end, bisection on integrated J", "2.614", bisect(g6, xstar + mp.mpf("1e-6"),
                                                                                    mp.mpf(4), mp.mpf("1e-7")),
        5e-4, "after CD.8")
    # minimal-pool belief and B at it
    mubar = F(pr, xstar - 1) / (F(pr, xstar - 1) + F(pr, xstar + 1))
    add("B_3(mubar(x*))", "3.195", B(p3, mubar), 5e-4, "CD.15 text")
    # T5 cutoffs
    for cl, note in (("3.0", "0.593"), ("3.5", "1.320"), ("4.0", "2.911"), ("4.2", "5.037"), ("2.5", "-0.350")):
        mu_l = (mp.mpf(cl) - p3.gL) / (p3.gH - p3.gL)
        xb = bisect(lambda xc: F(pr, xc - 1) / (F(pr, xc - 1) + F(pr, xc + 1)) - mu_l, mp.mpf(-1), mp.mpf(30))
        add(f"T5 largest consistent cutoff c'={cl}", note, xb, 5e-4, "T5")
    # pool probability lower bound
    add("Pr(X<=-1) under full orders", "0.25*(1+e^-1)", (1 + mp.e ** (-2 / pr.b)) / 4, 0, "CD.3(iv)")
    # b threshold
    add("b <= 2/logit(tau) at r=3", "2.296", 2 / mp.log(tau / (1 - tau)), 5e-4, "6.2 item 3")
    # floor table T4
    for rho, nJ, nE in (("0.25", "0.14073", "0.5228"), ("0.1", "0.11359", "0.4273"), ("0.01", "0.09731", "0.3700")):
        rr = mp.mpf(rho)
        st = full_order_stats(pr, p3, Law(atoms=((mp.mpf(1), rr), (mp.mpf(6), 1 - rr))))
        add(f"T4 J rho={rho}", nJ, st["J"], 5e-6, "T4")
        add(f"T4 E rho={rho}", nE, st["E"], 5e-5, "T4")
        add(f"T4 E gap = rho Pr(X<x*) rho={rho}", f"{float(rr * stats['fork_point_6']['pool']):.6g}",
            st["E"] - stats["fork_point_6"]["E"], 1e-6, "T4")

    # boundaries along r (T9 of note.md): roots of (1-1/b) J(r) - k on the minimal pool
    def margin(law, r):
        pay = pay_closed(pr, r)
        return (1 - 1 / pr.b) * full_order_stats(pr, pay, law)["J"] - pr.k

    add("fork full orders start r", "2.0155", bisect(lambda r: margin(law6, r), mp.mpf("1.95"), mp.mpf("2.1")),
        1e-4, "T9")
    l01 = laws["U[5.9,6.1]"][0]
    l05 = laws["U[5.5,6.5]"][0]
    add("eps=0.1 full orders start r", "2.0155", bisect(lambda r: margin(l01, r), mp.mpf("1.95"), mp.mpf("2.1")),
        1e-4, "T9")
    add("eps=0.5 full orders start r", "2.0161", bisect(lambda r: margin(l05, r), mp.mpf("1.95"), mp.mpf("2.1")),
        1e-4, "T9")
    add("eps=0.1 full orders end r", "3.7026", bisect(lambda r: margin(l01, r), mp.mpf("3.6"), mp.mpf("3.86")),
        1e-4, "T9")
    add("eps=0.5 full orders end r", "4.3507", bisect(lambda r: margin(l05, r), mp.mpf("4.2"), mp.mpf("4.9")),
        1e-4, "T9")
    for c, note in (("6", "3.5927"), ("6.1", "nan"), ("5.9", "3.866"), ("5.5", "4.959")):
        add(f"r_C({c})", note, ceiling(pr, mp.mpf(c)), 5e-4, "T3/T9")
    # entry at the end of the eps=0.1 branch and the CD.13(d) lower bound
    r_end = mp.mpf("3.70")
    pe = pay_closed(pr, r_end)
    st = full_order_stats(pr, pe, l01)
    add("eps=0.1 E at r=3.70 (grid 0.105)", "0.105", st["E"], 1e-3, "CD.13 text")
    add("eps=0.1 e_L at r=3.70", "nan", st["eL"], 0, "CD.13(d)")
    add("k e^{-2/b}/Delta_T at r=3.70", "nan", pr.k * mp.e ** (-2 / pr.b) / pe.DT, 0, "CD.13(d)")
    # fork entry at r_C from (A.14) with rho = 0
    add("(1+e^{-2/b})/4", "0.342", (1 + mp.e ** (-2 / pr.b)) / 4, 5e-4, "CD.13 text")

    # investor best responses at selected grid fixed points (T8 and the fork)
    checks = (
        ("U[3,9]", Law(uniforms=((mp.mpf(3), mp.mpf(9), 1),)), "1.90", mp.mpf(1), mp.mpf("-0.443"), "0.443", "0"),
        ("U[3,9]", Law(uniforms=((mp.mpf(3), mp.mpf(9), 1),)), "1.95", mp.mpf(1), mp.mpf("-0.530"), "0.530", "0.368"),
        ("U[3,9]", Law(uniforms=((mp.mpf(3), mp.mpf(9), 1),)), "2.10", mp.mpf(1), mp.mpf("-0.815"), "0.815", "0.380"),
        ("fork_point_6", law6, "2.00", mp.mpf(1), mp.mpf("-0.98"), "0.98", "nan"),
    )
    for name, law, r, qH, qL, note_v, note_pool in checks:
        pay = pay_closed(pr, r)
        sH, uH = best_response_scan(pr, pay, law, qH, qL, "H")
        sL, uL = best_response_scan(pr, pay, law, qH, qL, "L")
        add(f"{name} r={r} at (1,{float(qL)}): high-type best size", "1", sH, 2e-3, "T8")
        add(f"{name} r={r} at (1,{float(qL)}): low-type best short", note_v, sL, 3e-3, "T8")
        add(f"{name} r={r} pool probability", note_pool, pool_prob_pure(pr, pay, law, qH, qL), 2e-3, "T8")
    # Lemma CD.8 exactness at the two sides of the fork start
    for r in ("2.00", "2.05"):
        pay = pay_closed(pr, r)
        sL, _ = best_response_scan(pr, pay, law6, 1, -1, "L")
        add(f"fork r={r}: low-type best short against full-order minimal-pool schedule", "nan", sL, 0, "CD.8")

    with (HERE / "recheck.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()
