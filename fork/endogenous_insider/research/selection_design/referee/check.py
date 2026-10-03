"""Referee re-implementation of the key numbers in ../note.md.

Independent of ../selection_solve.py: closed forms are re-derived and evaluated in mpmath; the
investor's deviation payoffs are computed by an exact recursive Laplace convolution (O(N) per
schedule) instead of a dense kernel matrix. Writes CSV only, into this folder.
"""
from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path

import mpmath as mp
import numpy as np
from scipy.signal import lfilter

HERE = Path(__file__).resolve().parent
mp.mp.dps = 30


@dataclass(frozen=True)
class Par:
    h: float = 10.0
    ell: float = 1.0
    p: float = 0.5
    b: float = 2.0
    k: float = 0.02
    c: float = 6.0


BENCH = Par()


def mM(par: Par) -> tuple[mp.mpf, mp.mpf]:
    M = 1 / (1 + mp.e ** (-2 / mp.mpf(par.b)))
    return 1 - M, M


def pay(par: Par, r) -> dict:
    r = mp.mpf(r)
    h, l, p = mp.mpf(par.h), mp.mpf(par.ell), mp.mpf(par.p)
    t0 = p * (1 - p / r)
    tH = r / 2 + p ** 2 / (2 * r)
    tL = l - (l ** 2 - p ** 2) / (2 * r)
    gH = h - tH
    gL = (l ** 2 - p ** 2) / (2 * r)
    return dict(r=r, t0=t0, tH=tH, tL=tL, gH=gH, gL=gL, DT=tH - tL, wL=tL - t0)


def B(P: dict, mu) -> mp.mpf:
    return P["gL"] + mu * (P["gH"] - P["gL"])


def tau(par: Par, P: dict, s) -> mp.mpf:
    return (par.c - s - P["gL"]) / (P["gH"] - P["gL"])


def FZ(par: Par, z) -> mp.mpf:
    b = mp.mpf(par.b)
    return mp.e ** (z / b) / 2 if z <= 0 else 1 - mp.e ** (-z / b) / 2


def SZ(par: Par, z) -> mp.mpf:
    return 1 - FZ(par, z)


def mu_full(par: Par, x) -> mp.mpf:
    b = mp.mpf(par.b)
    return 1 / (1 + mp.e ** (-(abs(x + 1) - abs(x - 1)) / b))


def logit(t) -> mp.mpf:
    return mp.log(t / (1 - t))


def pool_post(par: Par, x) -> mp.mpf:
    a, c = FZ(par, x - 1), FZ(par, x + 1)
    return a / (a + c)


def J_quad(par: Par, P: dict, x0) -> mp.mpf:
    """Statistic (A.7) with entry on [x0, inf), by adaptive quadrature."""
    b = mp.mpf(par.b)
    f = lambda z: mp.e ** (-abs(z) / b) / (2 * b)
    g = lambda y: f(y - 1) * f(y + 1) / (f(y - 1) + f(y + 1))
    pts = sorted({x0, mp.mpf(-1), mp.mpf(1)})
    pts = [q for q in pts if q >= x0] + [mp.inf]
    return P["DT"] * mp.quad(g, pts)


def J_closed(par: Par, P: dict, x0) -> mp.mpf:
    m, _ = mM(par)
    b = mp.mpf(par.b)
    gd = lambda u: 2 * mp.atan(mp.tanh(u / 2))
    return P["DT"] * (m / 2 + mp.e ** (-1 / b) / 4 * (gd(1 / b) - gd(x0 / b)))


def minimal_pool(par: Par, r, s) -> dict:
    """Full orders, entry on {mu_X >= tau_s}, seller-funded subsidy s (kappa = 1)."""
    P = pay(par, r)
    m, M = mM(par)
    ts = tau(par, P, s)
    if ts <= m:
        eH = eL = mp.mpf(1)
        xs = -mp.inf
    else:
        xs = mp.mpf(1) if ts >= M else (par.b / mp.mpf(2)) * logit(ts)
        eH, eL = SZ(par, xs - 1), SZ(par, xs + 1)
    E = (eH + eL) / 2
    RT = P["t0"] + (eH * (P["tH"] - P["t0"]) + eL * P["wL"]) / 2
    W = (eH * P["gH"] + eL * P["gL"]) / 2 + E * (mp.mpf(par.p) ** 2 / P["r"] - par.c)
    mubar = pool_post(par, xs) if ts > m else mp.nan
    return dict(r=r, s=s, tau_s=ts, x_star=xs, e_H=eH, e_L=eL, E=E, R_T=RT, outlay=s * E,
                N=RT - s * E, W=W, mubar=mubar)


def frak_r(par: Par, d) -> mp.mpf:
    d = mp.mpf(d)
    return par.ell + d + mp.sqrt(d * d + 2 * par.ell * d)


def r_ceiling(par: Par) -> mp.mpf:
    _, M = mM(par)
    a = M * par.h - par.c
    return (a + mp.sqrt(a * a + M * ((1 - M) * par.ell ** 2 - par.p ** 2))) / M


# ------------------------------------------------------------------------------------------
# Grid layer: exact recursive Laplace convolution of a residual on a uniform flow grid
# ------------------------------------------------------------------------------------------

L_GRID, H_GRID = 30.0, 0.001
XG = np.round(np.arange(-L_GRID, L_GRID + H_GRID / 2, H_GRID), 6)
I_ORD = np.where(np.abs(XG) <= 1.0 + 1e-9)[0]   # grid points usable as orders


def conv_laplace(b: float, A: np.ndarray) -> np.ndarray:
    """F(s) = int f(x - s) A(x) dx at every grid point s, f Laplace(b); trapezoid in each cell."""
    a = math.exp(-H_GRID / b)
    u = np.empty_like(A)
    u[0] = 0.0
    u[1:] = 0.5 * H_GRID * (a * A[:-1] + A[1:])
    left = lfilter([1.0], [1.0, -a], u)
    Ar = A[::-1]
    v = np.empty_like(Ar)
    v[0] = 0.0
    v[1:] = 0.5 * H_GRID * (a * Ar[:-1] + Ar[1:])
    right = lfilter([1.0], [1.0, -a], v)[::-1]
    return (left + right) / (2.0 * b)


def lap(b: float, z: np.ndarray) -> np.ndarray:
    return np.exp(-np.abs(z) / b) / (2.0 * b)


@dataclass(frozen=True)
class GridOutcome:
    qH: float
    qL: float
    brH: float
    brL: float
    UH: float
    UL: float
    eH: float
    eL: float
    mubar: float
    pool_ok: bool


def grid_profile(par: Par, r: float, s: float, qH: float, qL: float, cutoff: float = -np.inf,
                 pool_cost_cut: float = 0.0) -> GridOutcome:
    P = pay(par, r)
    DT = float(P["DT"])
    ts = float(tau(par, P, s))
    aH, aL = lap(par.b, XG - qH), lap(par.b, XG - qL)
    mu = aH / (aH + aL)
    entry = (mu >= ts - 1e-12) & (XG >= cutoff)
    e = entry.astype(float)
    AH, AL = e * DT * (1 - mu), e * DT * mu
    FH, FL = conv_laplace(par.b, AH), conv_laplace(par.b, AL)
    q = XG[I_ORD]
    payH = q * FH[I_ORD] - par.k * np.abs(q)
    payL = -q * FL[I_ORD] - par.k * np.abs(q)
    iH, iL = int(payH.argmax()), int(payL.argmax())
    brH, UH = (float(q[iH]), float(payH[iH])) if payH[iH] > 0 else (0.0, 0.0)
    brL, UL = (float(q[iL]), float(payL[iL])) if payL[iL] > 0 else (0.0, 0.0)
    pool = ~entry
    if pool.any():
        wH, wL = np.trapezoid(aH * pool, XG), np.trapezoid(aL * pool, XG)
        mubar = wH / (wH + wL)
        pool_ok = float(B(P, mubar)) < par.c - s - pool_cost_cut
    else:
        mubar, pool_ok = float("nan"), True
    return GridOutcome(qH=qH, qL=qL, brH=brH, brL=brL, UH=UH, UL=UL, eH=float(np.trapezoid(e * aH, XG)),
                       eL=float(np.trapezoid(e * aL, XG)), mubar=float(mubar), pool_ok=bool(pool_ok))


def write_csv(path: Path, rows: list[dict]) -> None:
    keys = list(rows[0].keys())
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        for row in rows:
            w.writerow({k: (mp.nstr(v, 10) if isinstance(v, mp.mpf) else
                            (f"{v:.10g}" if isinstance(v, float) else v)) for k, v in row.items()})
