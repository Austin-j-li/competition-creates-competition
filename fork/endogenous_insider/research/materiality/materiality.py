"""Materiality index for the endogenous-insider fork.

Solver layer. Writes CSV only. The renderer `render_tables.py` never solves.

Notation follows `paper/main.md` and `fork/endogenous_insider/mechanism.md`. Under full
orders (q_H, q_L) = (1, -1) and an entry set A = [x', inf), every quantity below has a closed
form in the Laplace survival function and the Gudermannian function gd(u) = arctan(sinh u).
Those closed forms are evaluated in 40-digit arithmetic. Each row carries its status.

Columns (transliterations of C.0): h, ell, p, b, k, c, r, Delta_T, tau, x_star, e_H, e_L, E.
New columns: mat_H = e_H * Delta_T, mat_L = e_L * Delta_T, mat = E * Delta_T (ex ante
materiality index), J (gross value of full-order trading, (A.7)), resid_H = J / mat_H
(market residual uncertainty on the entry set, state H), and the own-order entry
probabilities prob_H_s (= Pr(X in A | H, order s)) for s in {0, 1/2, 1}.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

import mpmath as mp

mp.mp.dps = 40

HERE = Path(__file__).resolve().parent


@dataclass(frozen=True)
class Params:
    """Primitive declaration. Strings keep exact decimals; parsed once into mpf."""

    h: str = "10"
    ell: str = "1"
    p: str = "0.5"
    b: str = "2"
    k: str = "0.02"
    c: str = "6"  # fork: one deterministic preparation cost (c_H of the benchmark)
    rho_bench: str = "0.25"  # benchmark floor, used only for the comparison column
    c_L_bench: str = "1"  # benchmark low cost, used only for the comparison column


@dataclass(frozen=True)
class Payoffs:
    t0: mp.mpf
    tH: mp.mpf
    tL: mp.mpf
    gH: mp.mpf
    gL: mp.mpf
    Delta_T: mp.mpf
    B_half: mp.mpf
    B_M: mp.mpf
    B_m: mp.mpf
    tau: mp.mpf


def mpf(s: str) -> mp.mpf:
    return mp.mpf(s)


def posterior_bounds(params: Params) -> tuple[mp.mpf, mp.mpf]:
    b = mpf(params.b)
    M = 1 / (1 + mp.e ** (-2 / b))
    return 1 - M, M


def payoffs(params: Params, r: mp.mpf) -> Payoffs:
    """Equation (4) of the paper with the fork's single cost c in place of c_H."""
    h, ell, p, c = (mpf(params.h), mpf(params.ell), mpf(params.p), mpf(params.c))
    t0 = p * (1 - p / r)
    tH = r / 2 + p**2 / (2 * r)
    tL = ell - (ell**2 - p**2) / (2 * r)
    gH = h - tH
    gL = (ell**2 - p**2) / (2 * r)
    m, M = posterior_bounds(params)
    B = lambda mu: gL + mu * (gH - gL)  # noqa: E731
    return Payoffs(t0, tH, tL, gH, gL, tH - tL, B(mp.mpf(1) / 2), B(M), B(m), (c - gL) / (gH - gL))


def laplace_survival(z: mp.mpf, b: mp.mpf) -> mp.mpf:
    """S_Z(z) = Pr(Z > z) for Laplace noise with scale b."""
    if z >= 0:
        return mp.e ** (-z / b) / 2
    return 1 - mp.e ** (z / b) / 2


def gd(u: mp.mpf) -> mp.mpf:
    """Gudermannian function, the antiderivative of sech."""
    return mp.atan(mp.sinh(u))


def J_closed_form(Delta_T: mp.mpf, x_prime: mp.mpf, b: mp.mpf) -> mp.mpf:
    """J(x') = Delta_T * int_{x'}^inf f(x-1) f(x+1) / (f(x-1) + f(x+1)) dx, full orders, A = [x', inf).

    Lemma M.3 of note.md. For x' in [-1, 1]:
        J = Delta_T * e^{-1/b} / 4 * [ gd(1/b) - gd(x'/b) + sech(1/b) ].
    For x' >= 1:
        J = Delta_T * e^{-x'/b} / (4 cosh(1/b)).
    """
    if x_prime >= 1:
        return Delta_T * mp.e ** (-x_prime / b) / (4 * mp.cosh(1 / b))
    if x_prime < -1:
        raise ValueError("closed form stated for x' >= -1 only")
    return Delta_T * mp.e ** (-1 / b) / 4 * (gd(1 / b) - gd(x_prime / b) + 1 / mp.cosh(1 / b))


def J_quadrature(Delta_T: mp.mpf, x_prime: mp.mpf, b: mp.mpf) -> mp.mpf:
    """Independent check of the closed form by adaptive quadrature."""
    f = lambda z: mp.e ** (-abs(z) / b) / (2 * b)  # noqa: E731
    g = lambda x: f(x - 1) * f(x + 1) / (f(x - 1) + f(x + 1))  # noqa: E731
    pts = sorted({x_prime, mp.mpf(-1), mp.mpf(1), mp.mpf(0)} | {mp.inf})
    pts = [q for q in pts if q >= x_prime]
    if pts[0] != x_prime:
        pts = [x_prime] + pts
    return Delta_T * mp.quad(g, pts)


@dataclass(frozen=True)
class MaterialityRow:
    r: str
    x_prime: str
    branch: str
    Delta_T: str
    tau: str
    x_star: str
    e_H: str
    e_L: str
    E: str
    mat_H: str
    mat_L: str
    mat: str
    J: str
    J_quad_abs_err: str
    resid_H: str
    suff_margin: str  # (1 - 1/b) J - k ; positive means Proposition F.2(c) test holds
    prob_H_s0: str
    prob_H_s05: str
    prob_H_s1: str
    prob_L_s0: str
    prob_L_s05: str
    prob_L_s1: str
    mat_bench: str  # benchmark index with floor rho: [rho + (1-rho) E] Delta_T
    floor_bench: str  # rho * Delta_T, the benchmark's pointwise materiality floor
    disclosure_spread: str  # price spread if theta were public: entry iff g_theta >= c
    region: str
    status: str


def fmt(x: mp.mpf, digits: int = 12) -> str:
    return mp.nstr(x, digits)


def full_order_row(params: Params, r: mp.mpf, x_prime: mp.mpf | None, branch: str) -> MaterialityRow:
    """One row for full orders (1, -1) and entry set A = [x', inf).

    With x_prime None the minimal pool x' = x* is used. Requires tau <= M; otherwise the
    entry set is empty and the row is the dead profile.
    """
    b, k, c, rho, cL = (mpf(params.b), mpf(params.k), mpf(params.c), mpf(params.rho_bench), mpf(params.c_L_bench))
    pay = payoffs(params, r)
    m, M = posterior_bounds(params)
    region = "live_candidate"
    if pay.Delta_T < k:
        region = "trading_impossible"
    if pay.B_M < c:
        region = "above_ceiling"
    if pay.tau > M or pay.tau <= mp.mpf(1) / 2:
        # No flow supports entry (tau > M), or the dead profile fails (tau <= 1/2).
        x_star = mp.inf if pay.tau > M else mp.mpf(0)
        zero = mp.mpf(0)
        return MaterialityRow(
            r=fmt(r), x_prime="inf", branch="dead", Delta_T=fmt(pay.Delta_T), tau=fmt(pay.tau),
            x_star=fmt(x_star) if x_star != mp.inf else "inf", e_H="0", e_L="0", E="0", mat_H="0", mat_L="0",
            mat="0", J="0", J_quad_abs_err="0", resid_H="nan", suff_margin=fmt(-k), prob_H_s0="0",
            prob_H_s05="0", prob_H_s1="0", prob_L_s0="0", prob_L_s05="0", prob_L_s1="0",
            mat_bench=fmt(rho * pay.Delta_T), floor_bench=fmt(rho * pay.Delta_T),
            disclosure_spread=fmt(disclosure_spread(pay, c)), region=region, status="analytical (Prop F.1)",
        )
    x_star = b / 2 * mp.log(pay.tau / (1 - pay.tau))
    xp = x_star if x_prime is None else x_prime
    if xp < x_star:
        raise ValueError("entry set must lie inside {mu_X >= tau}")
    eH = laplace_survival(xp - 1, b)
    eL = laplace_survival(xp + 1, b)
    E = (eH + eL) / 2
    J = J_closed_form(pay.Delta_T, xp, b)
    Jq = J_quadrature(pay.Delta_T, xp, b)
    suff = (1 - 1 / b) * J - k
    probs_H = [laplace_survival(xp - s, b) for s in (mp.mpf(0), mp.mpf("0.5"), mp.mpf(1))]
    probs_L = [laplace_survival(xp + s, b) for s in (mp.mpf(0), mp.mpf("0.5"), mp.mpf(1))]
    bench_floor_ok = cL < pay.B_m
    mat_bench = (rho + (1 - rho) * E) * pay.Delta_T if bench_floor_ok else mp.nan
    status = "closed form; sufficient test holds" if suff > 0 else "closed form; sufficient test fails (existence open)"
    if region == "trading_impossible":
        status = "closed form of a hypothetical profile; no live equilibrium exists here (Prop F.1 iv)"
    return MaterialityRow(
        r=fmt(r), x_prime=fmt(xp), branch=branch, Delta_T=fmt(pay.Delta_T), tau=fmt(pay.tau), x_star=fmt(x_star),
        e_H=fmt(eH), e_L=fmt(eL), E=fmt(E), mat_H=fmt(eH * pay.Delta_T), mat_L=fmt(eL * pay.Delta_T),
        mat=fmt(E * pay.Delta_T), J=fmt(J), J_quad_abs_err=fmt(abs(J - Jq), 3), resid_H=fmt(J / (eH * pay.Delta_T)),
        suff_margin=fmt(suff), prob_H_s0=fmt(probs_H[0]), prob_H_s05=fmt(probs_H[1]), prob_H_s1=fmt(probs_H[2]),
        prob_L_s0=fmt(probs_L[0]), prob_L_s05=fmt(probs_L[1]), prob_L_s1=fmt(probs_L[2]),
        mat_bench=fmt(mat_bench), floor_bench=fmt(rho * pay.Delta_T),
        disclosure_spread=fmt(disclosure_spread(pay, c)), region=region, status=status,
    )


def disclosure_spread(pay: Payoffs, c: mp.mpf) -> mp.mpf:
    """Price spread between states if theta were public before preparation.

    With theta public the challenger prepares iff g_theta >= c, so V_T = t_theta if g_theta >= c
    and t_0 otherwise. This is the magnitude a disclosure-based test would use. It differs
    from Delta_T because disclosure changes the entry decision itself.
    """
    vH = pay.tH if pay.gH >= c else pay.t0
    vL = pay.tL if pay.gL >= c else pay.t0
    return vH - vL


def r_grid() -> list[mp.mpf]:
    pts = {mp.mpf(x) / 100 for x in range(125, 360, 5)}
    pts |= {mp.mpf(s) for s in ("1.2", "1.66", "2.05", "3", "3.5", "3.59", "3.5926", "3.5927", "3.6")}
    return sorted(pts)


def family_grid(x_star: mp.mpf) -> list[mp.mpf]:
    pts = [x_star]
    x = mp.mpf("0.9")
    while x <= mp.mpf("3.5"):
        pts.append(x)
        x += mp.mpf("0.1")
    return sorted(set(pts))


@dataclass(frozen=True)
class ThresholdRow:
    boundary: str
    value: str
    definition: str
    status: str


def thresholds(params: Params) -> list[ThresholdRow]:
    """Closed-form boundaries used in the note. All evaluated by root finding on closed forms."""
    b, k, c, ell = mpf(params.b), mpf(params.k), mpf(params.c), mpf(params.ell)
    h, p = mpf(params.h), mpf(params.p)
    m, M = posterior_bounds(params)
    frak_r = lambda d: ell + d + mp.sqrt(d * d + 2 * ell * d)  # noqa: E731
    r_C = ((M * h - c) + mp.sqrt((M * h - c) ** 2 + M * ((1 - M) * ell**2 - p**2))) / M
    # Sufficient-existence boundary for the full-order minimal-pool profile: (1 - 1/b) J(r) = k.
    g = lambda r: (1 - 1 / b) * J_closed_form(payoffs(params, r).Delta_T, b / 2 * mp.log(payoffs(params, r).tau / (1 - payoffs(params, r).tau)), b) - k  # noqa: E731
    r_J = mp.findroot(g, (mp.mpf("1.9"), mp.mpf("2.2")), solver="bisect")
    # Materiality index at the ceiling (left limit) and the index value where the live branch starts.
    pay_C = payoffs(params, r_C)
    mat_C = (1 + mp.e ** (-2 / b)) / 4 * pay_C.Delta_T  # E -> (alpha_H + alpha_L)/2 with x* -> 1
    # Family bound at r = 3: sufficient test holds for x' < xbar.
    pay3 = payoffs(params, mp.mpf(3))
    xbar = b * mp.log((1 - 1 / b) * pay3.Delta_T / (4 * k * mp.cosh(1 / b)))
    return [
        ThresholdRow("frak_r_k", fmt(frak_r(k)), "r(k): Delta_T(r) = k; below it D is unique (Prop F.1 iv)", "analytical, closed form"),
        ThresholdRow("r_C", fmt(r_C), "B_r(M) = c; above it D is unique (Prop F.1 iii)", "analytical, closed form (A.11)"),
        ThresholdRow("r_J", fmt(r_J), "(1 - 1/b) J(r) = k on the minimal-pool full-order profile; above it Prop F.2(c) certifies a live equilibrium", "closed form J, bisection root"),
        ThresholdRow("mat_at_ceiling", fmt(mat_C), "left limit of the materiality index E * Delta_T at r_C on the minimal-pool branch", "analytical, closed form (A.14) with rho = 0"),
        ThresholdRow("mat_above_ceiling", "0", "materiality index above r_C (D unique)", "analytical (Prop F.1 iii)"),
        ThresholdRow("xbar_family_r3", fmt(xbar), "at r = 3, full orders with A = [x', inf) pass the sufficient test iff x' < xbar (Lemma M.3)", "analytical, closed form"),
        ThresholdRow("m", fmt(m), "lower posterior bound", "analytical"),
        ThresholdRow("M", fmt(M), "upper posterior bound", "analytical"),
    ]


@dataclass(frozen=True)
class DeviationRow:
    r: str
    x_prime: str
    s: str
    prob_H: str  # Pr(X in A | H, order +s)
    gross_H: str  # F_H(s), gross profit per unit for the high type at order s
    bound_H: str  # Delta_T * prob_H, Proposition M.2 bound
    prob_L: str  # Pr(X in A | L, order -s)
    gross_L: str  # F_L(s)
    bound_L: str
    U_H: str  # s F_H(s) - k s
    U_L: str
    status: str


def deviation_rows(params: Params, r: mp.mpf, x_prime: mp.mpf | None) -> list[DeviationRow]:
    """Gross trading value against the fixed full-order schedule, as a function of own order size s."""
    b, k = mpf(params.b), mpf(params.k)
    pay = payoffs(params, r)
    x_star = b / 2 * mp.log(pay.tau / (1 - pay.tau))
    xp = x_star if x_prime is None else x_prime
    f = lambda z: mp.e ** (-abs(z) / b) / (2 * b)  # noqa: E731
    mu = lambda x: f(x - 1) / (f(x - 1) + f(x + 1))  # noqa: E731
    rows = []
    for s_str in ("0", "0.1", "0.25", "0.5", "0.75", "1"):
        s = mp.mpf(s_str)
        pts = sorted({xp, mp.mpf(1), mp.mpf(-1), s, -s} | {mp.inf})
        pts = [q for q in pts if q >= xp]
        if pts[0] != xp:
            pts = [xp] + pts
        FH = pay.Delta_T * mp.quad(lambda x: f(x - s) * (1 - mu(x)), pts)
        FL = pay.Delta_T * mp.quad(lambda x: f(x + s) * mu(x), pts)
        pH, pL = laplace_survival(xp - s, b), laplace_survival(xp + s, b)
        rows.append(DeviationRow(fmt(r), fmt(xp), s_str, fmt(pH), fmt(FH), fmt(pay.Delta_T * pH), fmt(pL), fmt(FL),
                                 fmt(pay.Delta_T * pL), fmt(s * FH - k * s), fmt(s * FL - k * s), "quadrature; numerical diagnostic"))
    return rows


def write_csv(path: Path, rows: Iterable) -> None:
    rows = list(rows)
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(asdict(rows[0]).keys()))
        w.writeheader()
        for row in rows:
            w.writerow(asdict(row))


def main() -> None:
    params = Params()
    branch = [full_order_row(params, r, None, "live_minimal_pool") for r in r_grid()]
    write_csv(HERE / "materiality_branch.csv", branch)

    r1 = mp.mpf(3)
    pay = payoffs(params, r1)
    x_star = mpf(params.b) / 2 * mp.log(pay.tau / (1 - pay.tau))
    family = [full_order_row(params, r1, xp, "cutoff_family") for xp in family_grid(x_star)]
    write_csv(HERE / "materiality_family.csv", family)

    dev = deviation_rows(params, r1, None) + deviation_rows(params, mp.mpf("2.05"), None)
    write_csv(HERE / "materiality_deviation.csv", dev)

    write_csv(HERE / "materiality_thresholds.csv", thresholds(params))

    max_err = max(mp.mpf(row.J_quad_abs_err) for row in branch + family)
    print(f"rows: branch={len(branch)} family={len(family)} deviation={len(dev)}; max |J_closed - J_quad| = {mp.nstr(max_err, 3)}")


if __name__ == "__main__":
    main()
