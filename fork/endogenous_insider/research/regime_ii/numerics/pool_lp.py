"""All pure-order equilibria under arbitrary pools, by linear programming.

Fix pure orders (q_H, q_L). By Lemma CD.2 an equilibrium is a pool N (any measurable set of flows that
contains Z_0 = {mu_X < tau_L}) with pool belief below tau_L, such that each type's order is a global best
response to the schedule that N creates. Cut the flow line into cells. Let pi_i in [0,1] be the pooled share
of cell i. Every one of these conditions is LINEAR in pi:

  belief:   sum_i pi_i [h_i (1 - tau_L) - tau_L l_i] <= -eps
  type H:   U_H(q) <= U_H(q_H)  for every q on a lattice
  type L:   U_L(s) <= U_L(q_L)  for every s on a lattice
  entry:    E = sum_i (1 - pi_i) e_i (h_i + l_i)/2,  e_H-entry = sum_i (1 - pi_i) e_i h_i

so for each order pair the set of supporting pools is a polytope, and the lowest E or lowest O_H over all
pools is a linear program. Feasible means an equilibrium with these orders exists (up to the lattice).
The result is a numerical diagnostic; pool_to_intervals + engine.regret give the exact best-response check,
and verify.py the independent quadrature check.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.optimize import linprog

from engine import Econ, _crossings, pure_pool, Profile, mu_flow

GX, GW = leggauss(4)


def _F(z: np.ndarray, b: float) -> np.ndarray:
    z = np.asarray(z, dtype=float)
    return np.where(z <= 0, 0.5 * np.exp(np.minimum(z, 0.0) / b), 1.0 - 0.5 * np.exp(-np.maximum(z, 0.0) / b))


@dataclass(frozen=True)
class Cells:
    lo: np.ndarray
    hi: np.ndarray
    h: np.ndarray        # Pr(cell | H)
    l: np.ndarray        # Pr(cell | L)
    e: np.ndarray        # entry level on the cell (0 on the forced pool)
    GH: np.ndarray       # (nq, ncells): gross payoff of H order q from cell i, per unit of non-pooled cell
    GL: np.ndarray       # (ns, ncells): gross payoff of L short s
    qgrid_H: np.ndarray
    sgrid_L: np.ndarray


def build_cells(ec: Econ, qH: float, qL: float, width: float = 0.01, Lx: float = 8.0, step_q: float = 0.01) -> Cells:
    b = ec.b
    prof = Profile(H=((qH, 1.0),), L=((qL, 1.0),))
    thr = [x for tau in (ec.tauL, ec.tauH) for x in _crossings(ec, prof, tau)]
    grid = np.round(np.arange(-Lx, Lx + 1e-9, width), 10).tolist()
    edges = sorted(set(grid) | set(thr) | {qH, qL})
    lo = np.array([-math.inf] + edges)
    hi = np.array(edges + [math.inf])
    n = len(lo)
    fin = np.isfinite(lo) & np.isfinite(hi)
    mid = np.where(fin, 0.5 * (lo + hi), 0.0)
    half = np.where(fin, 0.5 * (hi - lo), 0.0)
    # representative points for mu and entry
    rep = mid.copy()
    rep[0] = -Lx - 5.0
    rep[-1] = Lx + 5.0
    mu_rep = mu_flow(ec, prof, rep)
    e = ec.rho * (mu_rep >= ec.tauL - 1e-13) + (1.0 - ec.rho) * (mu_rep >= ec.tauH - 1e-13)
    h = np.array([(_F(c - qH, b) if math.isfinite(c) else 1.0) - (_F(a - qH, b) if math.isfinite(a) else 0.0)
                  for a, c in zip(lo, hi)], dtype=float)
    l = np.array([(_F(c - qL, b) if math.isfinite(c) else 1.0) - (_F(a - qL, b) if math.isfinite(a) else 0.0)
                  for a, c in zip(lo, hi)], dtype=float)
    # GL nodes on finite cells
    xs = mid[:, None] + half[:, None] * GX[None, :]
    ws = half[:, None] * GW[None, :]
    mu_n = mu_flow(ec, prof, xs)
    qs = np.round(np.arange(0.0, 1.0 + 1e-9, step_q), 10)
    GH = np.zeros((len(qs), n))
    GL = np.zeros((len(qs), n))
    for iq, q in enumerate(qs):
        kH = np.exp(-np.abs(xs - q) / b) / (2 * b)          # H buys q
        GH[iq, :] = q * ec.DeltaT * e * (kH * (1.0 - mu_n) * ws).sum(axis=1)
        kL = np.exp(-np.abs(xs + q) / b) / (2 * b)          # L sells q: flow centred at -q
        GL[iq, :] = q * ec.DeltaT * e * (kL * mu_n * ws).sum(axis=1)
        # tails in closed form (mu is constant there)
        for idx, side in ((0, -1), (n - 1, +1)):
            a = hi[0] if side < 0 else lo[-1]
            muT = mu_rep[idx]
            if side < 0:
                massH, massL = _F(a - q, b), _F(a + q, b)
            else:
                massH, massL = 1.0 - _F(a - q, b), 1.0 - _F(a + q, b)
            GH[iq, idx] = q * ec.DeltaT * e[idx] * (1.0 - muT) * float(massH)
            GL[iq, idx] = q * ec.DeltaT * e[idx] * muT * float(massL)
    return Cells(lo=lo, hi=hi, h=h, l=l, e=e, GH=GH, GL=GL, qgrid_H=qs, sgrid_L=qs)


def solve(ec: Econ, qH: float, qL: float, objective: str = "E", cells: Cells | None = None, eps: float = 1e-7,
          width: float = 0.01, slack: float = 0.0) -> dict | None:
    """LP over pooled shares. Returns the optimum or None when no pool supports these orders."""
    c = cells or build_cells(ec, qH, qL, width=width)
    n = len(c.h)
    forced = c.e == 0.0
    k = ec.k
    iH = int(round(qH / 0.01))
    iL = int(round(-qL / 0.01))
    # belief constraint
    rows = [c.h * (1 - ec.tauL) - ec.tauL * c.l]
    rhs = [-eps]
    # type H: sum_i (1 - pi_i) (GH[q,i] - GH[qH,i]) <= k (q - qH)   ->   -sum pi d <= k (q - qH) - sum d
    for iq, q in enumerate(c.qgrid_H):
        if iq == iH:
            continue
        d = c.GH[iq] - c.GH[iH]
        rows.append(-d)
        rhs.append(float(k * (q - qH) - d.sum()) + slack)
    # type L: the same for shorts of size s against the own short -qL
    for iq, s_ in enumerate(c.sgrid_L):
        if iq == iL:
            continue
        d = c.GL[iq] - c.GL[iL]
        rows.append(-d)
        rhs.append(float(k * (s_ - (-qL)) - d.sum()) + slack)
    # participation: own payoffs must be nonnegative (order 0 earns 0): included as q = 0 rows (iq = 0)
    mass_E = c.e * (c.h + c.l) / 2.0
    mass_H = c.e * c.h
    obj = -(mass_E if objective == "E" else mass_H)
    bounds = [(1.0, 1.0) if forced[i] else (0.0, 1.0) for i in range(n)]
    res = linprog(obj, A_ub=np.array(rows), b_ub=np.array(rhs), bounds=bounds, method="highs")
    if res.status != 0:
        return None
    pi = res.x
    E = float((mass_E * (1 - pi)).sum())
    eH = float((mass_H * (1 - pi)).sum())
    eL = float((c.e * c.l * (1 - pi)).sum())
    return {"pi": pi, "cells": c, "E": E, "eH": eH, "eL": eL, "O_H": 0.5 * eH,
            "belief": float((pi * c.h).sum() / ((pi * c.h).sum() + (pi * c.l).sum()))}


def pool_to_intervals(sol: dict, b: float = 2.0) -> tuple[tuple[float, float], ...]:
    """Pooled cells as intervals.

    A fractional finite cell is pooled on its left part (same share). The two infinite tail cells are
    plateaus with exponential tails, so a share p of the right tail [a, inf) is the sub-interval
    [a, a - b log(1 - p)], and a share p of the left tail (-inf, d] is [d + b log(1 - p), d].
    """
    c, pi = sol["cells"], sol["pi"]
    out: list[list[float]] = []
    for a, d, p in zip(c.lo, c.hi, pi):
        if p <= 1e-9:
            continue
        full = p >= 1 - 1e-9
        if full:
            lo_, hi_ = a, d
        elif math.isinf(d):
            lo_, hi_ = a, a - b * math.log(1.0 - p)
        elif math.isinf(a):
            lo_, hi_ = d + b * math.log(1.0 - p), d
        else:
            lo_, hi_ = a, a + p * (d - a)
        if out and abs(out[-1][1] - lo_) < 1e-12:
            out[-1][1] = hi_
        else:
            out.append([lo_, hi_])
    return tuple((float(x), float(y)) for x, y in out)
