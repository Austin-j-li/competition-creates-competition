"""Interval certificates at r = 3 for the cost-distribution track. Writes certificates.csv only.

For each declared cost law this module encloses, with mpmath interval arithmetic:
  (1) the regime: the signs of G at B_r(m), B_r(1/2), B_r(M), from enclosures of the three profit levels;
  (2) the no-trade test Delta_T G(B_r(1/2)) <= 2k, in exact rational arithmetic (B_r(1/2) is rational);
  (3) a rigorous lower bound J_low for the full-order existence statistic with the minimal pool, from the
      arcsine representation of Lemma C.6 and a lower Riemann sum: G(B_r(mu)) is nondecreasing in mu, so its
      value at the left end of each cell bounds it below; 1/sqrt(mu(1-mu)) is bounded below on each cell by
      its interval extension; shrinking [m, M] inward to rational endpoints only lowers a nonnegative integral.
The existence test k < (1 - 1/b) J_low then certifies the full-order minimal-pool equilibrium of
Proposition C.7, whose challenger and market-maker conditions are analytical. Status: computer-assisted.
"""
from __future__ import annotations

import csv
from fractions import Fraction
from pathlib import Path

from mpmath import iv, mpf

HERE = Path(__file__).resolve().parent
iv.dps = 40

H, ELL, P, B, K = Fraction(10), Fraction(1), Fraction(1, 2), Fraction(2), Fraction(1, 50)
R = Fraction(3)
N_CELLS = 20000

# (label, atoms as (location, mass), uniforms as (lo, hi, mass)), all exact rationals
LAWS: tuple[tuple[str, tuple, tuple], ...] = (
    ("fork_point_6", ((Fraction(6), Fraction(1)),), ()),
    ("noise_eps_0.1", (), ((Fraction(59, 10), Fraction(61, 10), Fraction(1)),)),
    ("noise_eps_0.5", (), ((Fraction(11, 2), Fraction(13, 2), Fraction(1)),)),
    ("noise_eps_1", (), ((Fraction(5), Fraction(7), Fraction(1)),)),
    ("noise_eps_1.5", (), ((Fraction(9, 2), Fraction(15, 2), Fraction(1)),)),
    ("uniform_3_9", (), ((Fraction(3), Fraction(9), Fraction(1)),)),
    ("uniform_0_12", (), ((Fraction(0), Fraction(12), Fraction(1)),)),
    ("benchmark_two_point", ((Fraction(1), Fraction(1, 4)), (Fraction(6), Fraction(3, 4))), ()),
    ("floor_rho_0.01", ((Fraction(1), Fraction(1, 100)), (Fraction(6), Fraction(99, 100))), ()),
    ("two_point_3.5_eta_0.05", ((Fraction(7, 2), Fraction(1, 20)), (Fraction(6), Fraction(19, 20))), ()),
)


def payoffs_exact(r: Fraction) -> dict[str, Fraction]:
    t0 = P * (1 - P / r)
    tH = r / 2 + P ** 2 / (2 * r)
    tL = ELL - (ELL ** 2 - P ** 2) / (2 * r)
    gH, gL = H - tH, (ELL ** 2 - P ** 2) / (2 * r)
    return {"t0": t0, "tH": tH, "tL": tL, "gH": gH, "gL": gL, "DeltaT": tH - tL}


def G_exact(atoms: tuple, uniforms: tuple, y: Fraction) -> Fraction:
    out = Fraction(0)
    for loc, mass in atoms:
        out += mass if y >= loc else 0
    for lo, hi, mass in uniforms:
        out += mass * min(max((y - lo) / (hi - lo), Fraction(0)), Fraction(1))
    return out


def G_lower(atoms: tuple, uniforms: tuple, y: iv.mpf) -> iv.mpf:
    """Lower enclosure of G over the interval y: G is nondecreasing, so evaluate at the lower end."""
    y_lo = iv.mpf(y.a)
    out = iv.mpf(0)
    for loc, mass in atoms:
        if y_lo.a >= mpf(loc.numerator) / mpf(loc.denominator):
            out += iv.mpf(mass.numerator) / mass.denominator
    for lo, hi, mass in uniforms:
        z = (y_lo - iv.mpf(lo.numerator) / lo.denominator) / (iv.mpf((hi - lo).numerator) / (hi - lo).denominator)
        z_lo = max(mpf(0), min(mpf(1), z.a))
        out += iv.mpf(z_lo) * (iv.mpf(mass.numerator) / mass.denominator)
    return iv.mpf(out.a)


def G_sign(atoms: tuple, uniforms: tuple, y: iv.mpf) -> str:
    """'zero' if G = 0 on the whole interval y, 'positive' if G > 0 on it, else 'undecided'."""
    c0 = min([loc for loc, m in atoms if m > 0] + [lo for lo, _, m in uniforms if m > 0])
    atom = any(loc == c0 and m > 0 for loc, m in atoms)
    c0f = iv.mpf(c0.numerator) / c0.denominator
    if y.b < c0f.a:
        return "zero"
    if y.a > c0f.b or (atom and y.a >= c0f.b):
        return "positive"
    return "undecided"


def certify_law(label: str, atoms: tuple, uniforms: tuple) -> dict:
    pay = payoffs_exact(R)
    gH, gL, DT = (iv.mpf(pay[k].numerator) / pay[k].denominator for k in ("gH", "gL", "DeltaT"))
    b = iv.mpf(B.numerator) / B.denominator
    m = 1 / (1 + iv.exp(2 / b))
    M = 1 - m
    B_m, B_M = gL + m * (gH - gL), gL + M * (gH - gL)
    B_half_exact = pay["gL"] + (pay["gH"] - pay["gL"]) / 2
    G_half = G_exact(atoms, uniforms, B_half_exact)
    no_trade = pay["DeltaT"] * G_half <= 2 * K

    sign_m, sign_M = G_sign(atoms, uniforms, B_m), G_sign(atoms, uniforms, B_M)
    sign_half = "zero" if G_half == 0 else "positive"
    if sign_m == "positive":
        reg = "I floor"
    elif sign_m == "zero" and sign_half == "positive":
        reg = "II prior entry"
    elif sign_half == "zero" and sign_M == "positive":
        reg = "III price-gated entry"
    elif sign_M == "zero":
        reg = "IV no entry"
    else:
        reg = "undecided"

    # rational inner endpoints: m_hi >= m and M_lo <= M
    m_hi = Fraction(str(mpf(m.b))).limit_denominator(10 ** 12) + Fraction(1, 10 ** 10)
    M_lo = Fraction(str(mpf(M.a))).limit_denominator(10 ** 12) - Fraction(1, 10 ** 10)
    assert (iv.mpf(m_hi.numerator) / m_hi.denominator).a > m.b, "inner lower endpoint must exceed m"
    assert (iv.mpf(M_lo.numerator) / M_lo.denominator).b < M.a, "inner upper endpoint must be below M"
    integral = iv.mpf(0)
    width = (M_lo - m_hi) / N_CELLS
    for i in range(N_CELLS):
        a, c = m_hi + i * width, m_hi + (i + 1) * width
        cell = iv.mpf([mpf(a.numerator) / a.denominator, mpf(c.numerator) / c.denominator])
        a_iv = iv.mpf(a.numerator) / a.denominator
        g_low = G_lower(atoms, uniforms, gL + a_iv * (gH - gL))
        if g_low.a <= 0:
            continue
        w_low = iv.mpf((1 / iv.sqrt(cell * (1 - cell))).a)
        integral += g_low * w_low * (iv.mpf(width.numerator) / width.denominator)
    integral = iv.mpf(integral.a)
    lower_plateau = G_lower(atoms, uniforms, B_m) * m / 2
    upper_plateau = G_lower(atoms, uniforms, B_M) * m / 2
    J_low = DT * (lower_plateau + iv.exp(-1 / b) / 4 * integral + upper_plateau)
    margin = (1 - 1 / b) * J_low - iv.mpf(K.numerator) / K.denominator
    unique_full = (1 - 1 / b) * m * DT * G_lower(atoms, uniforms, B_m) - iv.mpf(K.numerator) / K.denominator
    return {"law": label, "r": "3", "B_m_low": float(B_m.a), "B_m_high": float(B_m.b),
            "B_half_exact": f"{B_half_exact} = {float(B_half_exact):.10g}",
            "B_M_low": float(B_M.a), "B_M_high": float(B_M.b),
            "G_at_B_m": sign_m, "G_at_B_half_exact": f"{G_half}", "G_at_B_M": sign_M, "regime": reg,
            "no_trade_exists_exact": no_trade, "dead_exists_exact": G_half == 0,
            "J_lower_bound": float(J_low.a), "existence_margin_lower": float(margin.a),
            "full_order_minimal_pool_certified": bool(margin.a > 0),
            "unique_full_margin_lower": float(unique_full.a),
            "unique_full_certified": bool(unique_full.a > 0),
            "cells": N_CELLS, "status": "computer-assisted" if margin.a > 0 else "not certified"}


def main() -> None:
    rows = [certify_law(*law) for law in LAWS]
    keys = list(rows[0].keys())
    with (HERE / "certificates.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        for row in rows:
            w.writerow({k: (f"{v:.10g}" if isinstance(v, float) else v) for k, v in row.items()})
            print(row["law"], row["regime"], row["J_lower_bound"], row["existence_margin_lower"], row["status"],
                  flush=True)


if __name__ == "__main__":
    main()
