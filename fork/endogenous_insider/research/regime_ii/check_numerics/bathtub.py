"""Referee fractional knapsack for the full-order equilibrium set.

Under full orders every pool N contains Z0 = (-inf, z0) and is consistent iff
int_N (mu_X - tauL) dP < 0. Entry is E(N) = E0 - int_{N minus Z0} phi dP.
Discretise [z0, inf) into cells, sort by value per unit cost, fill the budget.
New code: cell integrals by 5-point Gauss-Legendre in numpy; no closed form of the bathtub set is used.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy import optimize

from model import Prm, auction, z0 as z0_of, f, F

GX, GW = np.polynomial.legendre.leggauss(7)


@dataclass(frozen=True)
class Knap:
    E0: float
    eH0: float
    infE: float
    infeH: float
    poolE: tuple[tuple[float, float], ...]
    poolH: tuple[tuple[float, float], ...]
    budget: float


def fv(x: np.ndarray, b: float) -> np.ndarray:
    return np.exp(-np.abs(x) / b) / (2 * b)


def cells(zlo: float, extra: tuple[float, ...] = (), h1: float = 1e-3, xmid: float = 12.0,
          xmax: float = 70.0) -> np.ndarray:
    n1 = int(math.ceil((xmid - zlo) / h1))
    a = np.linspace(zlo, xmid, n1 + 1)
    c = np.geomspace(1.0, xmax - xmid + 1.0, 400) + xmid - 1.0
    e = np.concatenate([a, c[1:], np.array(extra)])
    e = np.unique(e)
    return e[e >= zlo]


def knap(P: Prm, h1: float = 1e-3, scale: float = 1.0) -> Knap:
    a = auction(P)
    b = P.b
    z0 = z0_of(P)
    # forced pool Z0 = (-inf, z0): budget = -int (mu - tauL) dP over Z0
    # int_{-inf}^{z0} f(x-1)/2 dx = F(z0-1)/2 ; dP integral = (F(z0-1)+F(z0+1))/2
    Pz = 0.5 * (F(z0 - 1, b) + F(z0 + 1, b))
    Hz = 0.5 * F(z0 - 1, b)
    budget = scale * (a.tauL * Pz - Hz)  # = -Gamma(Z0) > 0, scaled to stay strictly inside
    edges = cells(z0, (0.5 * b * math.log(a.tauH / (1 - a.tauH)), 1.0), h1)
    lo, hi = edges[:-1], edges[1:]
    xs = 0.5 * (hi + lo)[:, None] + 0.5 * (hi - lo)[:, None] * GX[None, :]
    ws = 0.5 * (hi - lo)[:, None] * GW[None, :]
    fm, fp = fv(xs - 1, b), fv(xs + 1, b)
    dP = ((fm + fp) / 2 * ws).sum(1)
    dHm = (fm / 2 * ws).sum(1)  # mu dP = f(x-1)/2
    cost = dHm - a.tauL * dP
    # entry weight per unit flow: rho below x*, 1 above (mu >= tauH); mu is monotone so use midpoint
    mu_mid = fv(xs.mean(1) - 1, b) / (fv(xs.mean(1) - 1, b) + fv(xs.mean(1) + 1, b))
    phi = np.where(mu_mid >= a.tauH, 1.0, P.rho)
    valE = phi * dP
    valH = phi * (fm * ws).sum(1)  # e_H = int phi f(x-1) dx
    # total entry with minimal pool
    E0 = float(valE.sum())
    eH0 = float(valH.sum())
    out = []
    for val, tot in ((valE, E0), (valH, eH0)):
        # tiny cost cells: add the epsilon to avoid division by zero
        ratio = val / np.maximum(cost, 1e-300)
        key = np.round(np.log(np.maximum(ratio, 1e-300)), 9)
        order = np.lexsort((-lo, -key))
        spent, gained = 0.0, 0.0
        sel = np.zeros(len(cost), dtype=float)
        for i in order:
            if cost[i] <= 0:
                sel[i] = 1.0
                gained += val[i]
                continue
            if spent + cost[i] <= budget:
                spent += cost[i]
                gained += val[i]
                sel[i] = 1.0
            else:
                lam = (budget - spent) / cost[i]
                gained += lam * val[i]
                sel[i] = lam
                spent = budget
                break
        # pool intervals (fractional cell: lower part)
        pool = []
        for i in np.nonzero(sel)[0]:
            l0, h0 = lo[i], lo[i] + sel[i] * (hi[i] - lo[i])
            if pool and abs(pool[-1][1] - l0) < 1e-12:
                pool[-1] = (pool[-1][0], h0)
            else:
                pool.append((float(l0), float(h0)))
        out.append((tot - gained, tuple(pool)))
    return Knap(E0, eH0, out[0][0], out[1][0], out[0][1], out[1][1], budget)


def threshold(P: Prm, which: str, lo: float, hi: float, h1: float = 1e-3) -> float:
    """Largest cL with inf E (or inf e_H) >= rho, by bisection on cL."""
    def g(cL: float) -> float:
        kn = knap(Prm(**{**P.__dict__, "cL": cL}), h1)
        return (kn.infE if which == "E" else kn.infeH) - P.rho
    return optimize.brentq(g, lo, hi, xtol=1e-7)
