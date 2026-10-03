"""Selection design in the endogenous-insider fork.

The model is the fork of `fork/endogenous_insider/mechanism.md`: one known preparation cost c, no
low-cost floor. This module studies devices that act on the dead equilibrium D:

* a uniform preparation subsidy s, paid to the challenger whenever it prepares;
* a backstop subsidy s_bar, paid only if the challenger prepares while the price is the no-entry
  price t_0;
* a subsidy lottery: with probability rho the challenger's cost is cut to B_r(m), which recreates the
  paper's preparation floor (A1).

The seller funds every transfer (kappa = 1), so the target's terminal value on entry is t_theta - s and
the seller's net proceeds equal the mean price. Transfers that do not depend on theta cancel from the
investor's residual, so the investor's problem is the fork's problem with tau replaced by tau_s.

This module solves and writes CSV only. Closed-form rows are labelled "analytical" only where the note
proves the formula and the existence test; best-response fixed points on the grid are labelled
"numerical diagnostic". The grid and the order search are copied from `fork/endogenous_insider/solve.py`.
"""
from __future__ import annotations

import csv
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
INF = float("inf")
NAN = float("nan")
TIE = 1e-12  # tie rule: a belief within TIE of the threshold counts as indifference, so the challenger prepares


# ----------------------------------------------------------------------------------------------
# Parameter record and closed forms
# ----------------------------------------------------------------------------------------------

@dataclass(frozen=True)
class Params:
    """Benchmark primitives of the fork: Online Appendix C.0 with rho -> 0 and c_H -> c."""
    h: float = 10.0
    ell: float = 1.0
    p: float = 0.5
    b: float = 2.0
    k: float = 0.02
    c: float = 6.0

    @property
    def M(self) -> float:
        return 1.0 / (1.0 + math.exp(-2.0 / self.b))

    @property
    def m(self) -> float:
        return 1.0 - self.M


BENCH = Params()


@dataclass(frozen=True)
class Payoffs:
    """Acquisition payoffs (4) at strength r and reserve p."""
    r: float
    t0: float
    tH: float
    tL: float
    gH: float
    gL: float

    @property
    def Delta_T(self) -> float:
        return self.tH - self.tL

    @property
    def wL(self) -> float:
        return self.tL - self.t0


def payoffs(par: Params, r: float) -> Payoffs:
    p, ell = par.p, par.ell
    return Payoffs(r=r, t0=p * (1.0 - p / r), tH=r / 2.0 + p * p / (2.0 * r),
                   tL=ell - (ell * ell - p * p) / (2.0 * r),
                   gH=par.h - r / 2.0 - p * p / (2.0 * r), gL=(ell * ell - p * p) / (2.0 * r))


def gross_profit(par: Params, pay: Payoffs, mu: float) -> float:
    """B_r(mu)."""
    return pay.gL + mu * (pay.gH - pay.gL)


def tau_of(par: Params, pay: Payoffs, s: float) -> float:
    """tau_s = (c - s - g_L) / (g_H - g_L)."""
    return (par.c - s - pay.gL) / (pay.gH - pay.gL)


@dataclass(frozen=True)
class Thresholds:
    """Subsidy thresholds at strength r. s_M < s_D < s_m."""
    s_M: float   # tau_s = M: smallest subsidy at which a live equilibrium can exist
    s_D: float   # tau_s = 1/2: smallest subsidy that removes D
    s_m: float   # tau_s = m: smallest subsidy that makes entry certain
    gain_bound: float  # w_L + M Delta_T: largest possible seller gain per entry, gross of subsidy
    d_margin: float    # s_D - gain_bound; positive means every D-removing uniform subsidy loses money
    d_closed: float    # the closed form of d_margin in the note, as a cross-check


def thresholds(par: Params, r: float) -> Thresholds:
    pay = payoffs(par, r)
    s_M = par.c - gross_profit(par, pay, par.M)
    s_D = par.c - gross_profit(par, pay, 0.5)
    s_m = par.c - gross_profit(par, pay, par.m)
    gain = pay.wL + par.M * pay.Delta_T
    d_closed = (par.c - par.h / 2.0 + par.p - par.m * par.ell - (par.M - par.m) * r / 4.0
                - ((par.M - par.m) * par.ell ** 2 / 4.0 + par.p ** 2) / r)
    return Thresholds(s_M=s_M, s_D=s_D, s_m=s_m, gain_bound=gain, d_margin=s_D - gain, d_closed=d_closed)


def case_label(par: Params, tau_s: float) -> str:
    if tau_s > par.M:
        return "tau_s>M"
    if tau_s > 0.5:
        return "1/2<tau_s<=M"
    if tau_s > par.m:
        return "m<tau_s<=1/2"
    return "tau_s<=m"


# Laplace noise
def F_Z(par: Params, z: float) -> float:
    return 0.5 * math.exp(z / par.b) if z <= 0.0 else 1.0 - 0.5 * math.exp(-z / par.b)


def S_Z(par: Params, z: float) -> float:
    return 1.0 - F_Z(par, z)


def x_star_full(par: Params, tau_s: float) -> float:
    """Flow at which the full-order posterior (A.8) reaches tau_s; -inf if tau_s <= m, +inf if tau_s > M."""
    if tau_s <= par.m + TIE:
        return -INF
    if tau_s > par.M + TIE:
        return INF
    if tau_s >= par.M - TIE:
        return 1.0
    return 0.5 * par.b * math.log(tau_s / (1.0 - tau_s))


def pool_average(par: Params, x_cut: float) -> float:
    """Pr(H | X < x_cut) under full orders, equation (F.2)."""
    a, bb = F_Z(par, x_cut - 1.0), F_Z(par, x_cut + 1.0)
    return a / (a + bb)


def x_bar(par: Params, tau_s: float) -> float:
    """Largest pool end consistent with the challenger: pool_average(x_bar) = tau_s (inf if tau_s >= 1/2)."""
    if tau_s >= 0.5:
        return INF
    if tau_s <= par.m:
        return -1.0
    return brentq(lambda x: pool_average(par, x) - tau_s, -1.0, 200.0, xtol=1e-13)


def gd(u: float) -> float:
    """Gudermannian function, the antiderivative of sech."""
    return 2.0 * math.atan(math.tanh(u / 2.0))


def J_closed(par: Params, pay: Payoffs, x_cut: float) -> float:
    """J = F_H(1) = F_L(1) under full orders with entry on [x_cut, inf), x_cut in [-1, 1] (closed form)."""
    if x_cut > 1.0:
        raise ValueError("closed form covers x_cut <= 1 only")
    xc = max(x_cut, -1.0)
    val = par.m / 2.0 + 0.25 * math.exp(-1.0 / par.b) * (gd(1.0 / par.b) - gd(xc / par.b))
    if x_cut <= -1.0:
        val += par.m / 2.0
    return pay.Delta_T * val


@dataclass(frozen=True)
class Outcome:
    """One candidate continuation with its accounting. Status uses the paper's vocabulary."""
    r: float
    s: float
    device: str
    branch: str
    q_H: float
    q_L: float
    e_H: float
    e_L: float
    E: float
    O_H: float
    R_T: float        # expected gross target proceeds
    outlay: float     # expected transfer paid by the seller
    net: float        # R_T - outlay; equals the mean price when the seller funds the transfer
    W: float          # acquisition surplus net of preparation cost, excluding transfers and trading costs
    mubar: float      # pooled posterior at t_0 (nan if no pool)
    pool_prob: float
    x_star: float     # lower end of the entry region on flows (inf if none)
    U_H: float
    U_L: float
    test: str         # sufficient existence or uniqueness test used, with its margin
    status: str


def accounting(par: Params, pay: Payoffs, e_H: float, e_L: float, outlay: float) -> dict:
    E = 0.5 * (e_H + e_L)
    R_T = pay.t0 + 0.5 * (e_H * (pay.tH - pay.t0) + e_L * (pay.tL - pay.t0))
    W = 0.5 * (e_H * pay.gH + e_L * pay.gL) + E * (par.p ** 2 / pay.r - par.c)
    return {"E": E, "O_H": 0.5 * e_H, "R_T": R_T, "outlay": outlay, "net": R_T - outlay, "W": W}


def dead_outcome(par: Params, r: float, s: float, device: str, exists: bool, why: str) -> Outcome:
    pay = payoffs(par, r)
    acc = accounting(par, pay, 0.0, 0.0, 0.0)
    return Outcome(r=r, s=s, device=device, branch="dead D", q_H=0.0, q_L=0.0, e_H=0.0, e_L=0.0, **acc,
                   mubar=0.5, pool_prob=1.0, x_star=INF, U_H=0.0, U_L=0.0, test=why,
                   status="analytical" if exists else "analytical (not an equilibrium)")


def certain_entry_no_trade(par: Params, r: float, s: float, exists: bool) -> Outcome:
    """Profile C: zero orders, entry at the single price. Equilibrium iff tau_s <= 1/2 and Delta_T <= 2k."""
    pay = payoffs(par, r)
    acc = accounting(par, pay, 1.0, 1.0, s)
    return Outcome(r=r, s=s, device="uniform", branch="no trade, certain entry C", q_H=0.0, q_L=0.0,
                   e_H=1.0, e_L=1.0, **acc, mubar=NAN, pool_prob=0.0, x_star=-INF, U_H=0.0, U_L=0.0,
                   test=f"Delta_T-2k={pay.Delta_T - 2 * par.k:.6g}",
                   status="analytical" if exists else "analytical (not an equilibrium)")


def full_order_min_pool(par: Params, r: float, s: float) -> Outcome | None:
    """Full orders, entry on [x*_s, inf). Closed form; existence by k < (1-1/b) J(x*_s)."""
    pay = payoffs(par, r)
    tau_s = tau_of(par, pay, s)
    if tau_s > par.M + TIE:
        return None
    if tau_s <= par.m + TIE:  # certain entry; the paper's floor economy with rho = 1
        acc = accounting(par, pay, 1.0, 1.0, s * 1.0)
        margin = (1.0 - 1.0 / par.b) * par.m * pay.Delta_T - par.k
        return Outcome(r=r, s=s, device="uniform", branch="full orders, certain entry", q_H=1.0, q_L=-1.0,
                       e_H=1.0, e_L=1.0, **acc, mubar=NAN, pool_prob=0.0, x_star=-INF, U_H=NAN, U_L=NAN,
                       test=f"(1-1/b)m*Delta_T-k={margin:.6g} (uniqueness)",
                       status="analytical" if margin > 0 else "test fails (open)")
    xs = x_star_full(par, tau_s)
    e_H, e_L = S_Z(par, xs - 1.0), S_Z(par, xs + 1.0)
    acc = accounting(par, pay, e_H, e_L, s * 0.5 * (e_H + e_L))
    J = J_closed(par, pay, xs)
    margin = (1.0 - 1.0 / par.b) * J - par.k
    pool_prob = 0.5 * (F_Z(par, xs - 1.0) + F_Z(par, xs + 1.0))
    return Outcome(r=r, s=s, device="uniform", branch="full orders, minimal pool", q_H=1.0, q_L=-1.0,
                   e_H=e_H, e_L=e_L, **acc, mubar=pool_average(par, xs), pool_prob=pool_prob, x_star=xs,
                   U_H=NAN, U_L=NAN, test=f"(1-1/b)J-k={margin:.6g} (existence)",
                   status="analytical" if margin > 0 else "test fails (open)")


# ----------------------------------------------------------------------------------------------
# Grid search: best-response iteration against fixed schedules (copied from the fork's solver)
# ----------------------------------------------------------------------------------------------

@dataclass(frozen=True)
class Grid:
    X: np.ndarray
    DX: float
    S: np.ndarray
    KERNEL: np.ndarray


def make_grid(par: Params) -> Grid:
    X = np.linspace(-30.0, 30.0, 60001)
    S = np.round(np.linspace(-1.0, 1.0, 201), 3)
    return Grid(X=X, DX=float(X[1] - X[0]), S=S, KERNEL=density(par, X[None, :] - S[:, None]))


def density(par: Params, z: np.ndarray) -> np.ndarray:
    return np.exp(-np.abs(z) / par.b) / (2.0 * par.b)


@dataclass(frozen=True)
class Schedule:
    mu: np.ndarray
    e: np.ndarray
    gain_H: np.ndarray   # E[V_T | H, x] - P(x)
    gain_L: np.ndarray   # E[V_T | L, x] - P(x)
    e_H: float
    e_L: float
    mubar: float
    pool_prob: float
    pool_ok: bool
    x_star: float


def schedule(par: Params, grid: Grid, r: float, s: float, q_H: float, q_L: float,
             cutoff: float = -INF, pool_subsidy: float = 0.0, rho: float = 0.0) -> Schedule:
    """Candidate continuation at fixed orders.

    Uniformly subsidized challenger prepares on {mu_X >= tau_s} and above `cutoff`. With probability rho
    (lottery) the challenger prepares at every price; then no flow pools (Proposition A.2). At the pool
    price t_0 the challenger also receives `pool_subsidy` (the backstop), which enters the pool test.
    """
    pay = payoffs(par, r)
    tau_s = tau_of(par, pay, s)
    aH, aL = density(par, grid.X - q_H), density(par, grid.X - q_L)
    mu = aH / (aH + aL)
    entry = (mu >= tau_s - TIE) & (grid.X >= cutoff)
    e = rho + (1.0 - rho) * entry.astype(float)
    pool = ~entry
    if rho == 0.0 and pool.any():
        wH, wL = float(aH[pool].sum()), float(aL[pool].sum())
        mubar = wH / (wH + wL)
        pool_ok = gross_profit(par, pay, mubar) < par.c - s - pool_subsidy
        pool_prob = 0.5 * (wH + wL) * grid.DX
    else:
        mubar, pool_ok, pool_prob = NAN, True, 0.0
    x_star = float(grid.X[entry][0]) if entry.any() else INF
    return Schedule(mu=mu, e=e, gain_H=e * pay.Delta_T * (1.0 - mu), gain_L=-e * pay.Delta_T * mu,
                    e_H=float((e * aH).sum() * grid.DX), e_L=float((e * aL).sum() * grid.DX),
                    mubar=mubar, pool_prob=pool_prob, pool_ok=bool(pool_ok), x_star=x_star)


def best_response(par: Params, grid: Grid, gain: np.ndarray) -> tuple[float, float]:
    coarse = grid.S * (grid.KERNEL @ gain) * grid.DX - par.k * np.abs(grid.S)
    i = int(coarse.argmax())
    lo, hi = max(-1.0, grid.S[i] - 0.01), min(1.0, grid.S[i] + 0.01)
    fine = np.linspace(lo, hi, 41)
    vals = np.array([q * (density(par, grid.X - q) * gain).sum() * grid.DX - par.k * abs(q) for q in fine])
    j = int(vals.argmax())
    if vals[j] <= 0.0:  # the zero order is always available and earns exactly zero
        return 0.0, 0.0
    return float(fine[j]), float(vals[j])


@dataclass(frozen=True)
class FixedPoint:
    q_H: float
    q_L: float
    U_H: float
    U_L: float
    sch: Schedule


def iterate(par: Params, grid: Grid, r: float, s: float, q_H: float, q_L: float, cutoff: float = -INF,
            pool_subsidy: float = 0.0, rho: float = 0.0, max_iter: int = 80,
            tol: float = 5e-4) -> tuple[FixedPoint | None, str]:
    for _ in range(max_iter):
        sch = schedule(par, grid, r, s, q_H, q_L, cutoff, pool_subsidy, rho)
        bH, uH = best_response(par, grid, sch.gain_H)
        bL, uL = best_response(par, grid, sch.gain_L)
        if abs(bH - q_H) < tol and abs(bL - q_L) < tol:
            if not sch.pool_ok:
                return None, "fixed point fails the pool test"
            return FixedPoint(q_H=q_H, q_L=q_L, U_H=uH, U_L=uL, sch=sch), "fixed point"
        q_H, q_L = bH, bL
    return None, "no convergence"


STARTS = [(1.0, -1.0), (1.0, -0.5), (1.0, 0.0), (0.5, -0.5), (0.25, -0.25), (0.0, 0.0)]


def fixed_point_outcome(par: Params, r: float, s: float, device: str, fp: FixedPoint,
                        outlay: float, branch: str) -> Outcome:
    pay = payoffs(par, r)
    acc = accounting(par, pay, fp.sch.e_H, fp.sch.e_L, outlay)
    return Outcome(r=r, s=s, device=device, branch=branch, q_H=fp.q_H, q_L=fp.q_L, e_H=fp.sch.e_H,
                   e_L=fp.sch.e_L, **acc, mubar=fp.sch.mubar, pool_prob=fp.sch.pool_prob,
                   x_star=fp.sch.x_star, U_H=fp.U_H, U_L=fp.U_L, test="grid best response",
                   status="numerical diagnostic")


def search_uniform(par: Params, grid: Grid, r: float, s: float) -> list[Outcome]:
    """Distinct pure fixed points with the uniform subsidy, from the declared starts."""
    found: list[Outcome] = []
    for q0 in STARTS:
        fp, _ = iterate(par, grid, r, s, *q0)
        if fp is None:
            continue
        if any(abs(fp.q_H - o.q_H) < 0.015 and abs(fp.q_L - o.q_L) < 0.015 for o in found):
            continue
        E = 0.5 * (fp.sch.e_H + fp.sch.e_L)
        branch = "grid fixed point, no entry" if E <= 0 else (
            "grid fixed point, certain entry" if fp.sch.pool_prob == 0.0 else "grid fixed point, pool")
        found.append(fixed_point_outcome(par, r, s, "uniform", fp, s * E, branch))
    return found


# ----------------------------------------------------------------------------------------------
# Experiments
# ----------------------------------------------------------------------------------------------

def frak_r(par: Params, d: float) -> float:
    """(A.10): root above ell of Delta_T(r) = d."""
    return par.ell + d + math.sqrt(d * d + 2.0 * par.ell * d)


def r_ceiling(par: Params) -> float:
    """(A.11) with c_H -> c."""
    M = par.M
    a = M * par.h - par.c
    return (a + math.sqrt(a * a + M * ((1 - M) * par.ell ** 2 - par.p ** 2))) / M


def across_strengths(par: Params, grid: Grid) -> list[dict]:
    rC = r_ceiling(par)
    rs = sorted(set(np.round(np.arange(1.05, 9.951, 0.05), 3).tolist()) | {1.2, 3.0, round(rC, 4)})
    rows = []
    for r in rs:
        pay = payoffs(par, r)
        th = thresholds(par, r)
        tau0 = tau_of(par, pay, 0.0)
        live0 = full_order_min_pool(par, r, 0.0) if tau0 > 0.5 else None
        at_sD = full_order_min_pool(par, r, th.s_D)
        at_sm = full_order_min_pool(par, r, th.s_m)
        C_exists = pay.Delta_T <= 2 * par.k
        net_C = (pay.tH + pay.tL) / 2.0 - th.s_D
        # grid search at s_D from all declared starts (numerical diagnostic)
        found = search_uniform(par, grid, r, th.s_D)
        solver = max(found, key=lambda o: (o.q_H - o.q_L)) if found else None
        why = (f"{len(found)} pure fixed point(s): " + "; ".join(f"({o.q_H:+.3f},{o.q_L:+.3f})" for o in found)
               if found else "no pure fixed point from six starts (open)")
        backstop_top = (par.c - gross_profit(par, pay, live0.mubar)) if live0 is not None else NAN
        rows.append({
            "r": r, "t_0": pay.t0, "t_H": pay.tH, "t_L": pay.tL, "g_H": pay.gH, "g_L": pay.gL,
            "Delta_T": pay.Delta_T, "w_L": pay.wL, "B_prior": gross_profit(par, pay, 0.5),
            "B_prior_zero_reserve": 0.5 * (par.h - r / 2.0 + par.ell ** 2 / (2.0 * r)),
            "tau": tau0, "s_M": th.s_M, "s_D": th.s_D, "s_m": th.s_m,
            "gain_bound": th.gain_bound, "d_margin": th.d_margin, "d_closed": th.d_closed,
            "live_s0_exists": live0 is not None and live0.status == "analytical",
            "R_T_live_s0": live0.R_T if live0 is not None else NAN,
            "W_live_s0": live0.W if live0 is not None else NAN,
            "E_live_s0": live0.E if live0 is not None else NAN,
            "test_live_s0": live0.test if live0 is not None else "tau>M or tau<=1/2",
            "net_D": pay.t0,
            "net_sD_minpool": at_sD.net if at_sD is not None else NAN,
            "E_sD_minpool": at_sD.E if at_sD is not None else NAN,
            "W_sD_minpool": at_sD.W if at_sD is not None else NAN,
            "test_sD_minpool": at_sD.test if at_sD is not None else "",
            "status_sD_minpool": at_sD.status if at_sD is not None else "",
            "C_exists_at_sD": C_exists, "net_C_at_sD": net_C,
            "solver_sD_qH": solver.q_H if solver else NAN, "solver_sD_qL": solver.q_L if solver else NAN,
            "solver_sD_E": solver.E if solver else NAN, "solver_sD_net": solver.net if solver else NAN,
            "solver_sD_note": why,
            "net_sm_certain": at_sm.net if at_sm is not None else NAN,
            "W_sm_certain": at_sm.W if at_sm is not None else NAN,
            "test_sm_certain": at_sm.test if at_sm is not None else "",
            "backstop_window_low": th.s_D if live0 is not None else NAN,
            "backstop_window_high": backstop_top,
            "lottery_rho_N": 2 * par.k / pay.Delta_T,
            "lottery_rho_U": par.k / ((1 - 1 / par.b) * par.m * pay.Delta_T),
        })
        print(f"r={r:.3f} s_D={th.s_D:.4f} d={th.d_margin:.4f} net_sD={rows[-1]['net_sD_minpool']:.4f} "
              f"t0={pay.t0:.4f} live={rows[-1]['R_T_live_s0']:.4f} solver={why}", flush=True)
    return rows


def sweep_subsidy(par: Params, grid: Grid, r: float) -> list[Outcome]:
    pay = payoffs(par, r)
    th = thresholds(par, r)
    special = [th.s_M, th.s_D, th.s_m, th.s_D - 1e-6, th.s_m - 1e-6, 0.0]
    ss = sorted(set(np.round(np.arange(-0.25, 4.001, 0.05), 4).tolist()) | set(special))
    out: list[Outcome] = []
    for s in ss:
        tau_s = tau_of(par, pay, s)
        dead = tau_s > 0.5 + TIE
        out.append(dead_outcome(par, r, s, "uniform", dead, "B_r(1/2) < c - s" if dead else "B_r(1/2) >= c - s"))
        out.append(certain_entry_no_trade(par, r, s, tau_s <= 0.5 + TIE and pay.Delta_T <= 2 * par.k))
        mp = full_order_min_pool(par, r, s)
        if mp is not None:
            out.append(mp)
        if tau_s <= par.M + TIE:
            out.extend(search_uniform(par, grid, r, s))
        print(f"s={s:+.4f} tau_s={tau_s:.4f} {case_label(par, tau_s)} D={dead} "
              f"minpool_net={(mp.net if mp else NAN):.4f}", flush=True)
    return out


def sweep_cost(par: Params, r: float) -> list[dict]:
    """Closed-form comparison at r across c in (B_r(1/2), B_r(M)]: minimal D-removing subsidy vs D vs live."""
    pay0 = payoffs(par, r)
    lo, hi = gross_profit(par, pay0, 0.5), gross_profit(par, pay0, par.M)
    cs = sorted(set(np.round(np.arange(lo + 0.01, hi, 0.02), 4).tolist()) | {par.c, hi})
    rows = []
    for c in cs:
        q = Params(h=par.h, ell=par.ell, p=par.p, b=par.b, k=par.k, c=c)
        th = thresholds(q, r)
        live = full_order_min_pool(q, r, 0.0)
        sub = full_order_min_pool(q, r, th.s_D)
        rows.append({"r": r, "c": c, "s_D": th.s_D, "tau": tau_of(q, pay0, 0.0),
                     "R_T_live_s0": live.R_T, "test_live_s0": live.test, "net_D": pay0.t0,
                     "net_sD_minpool": sub.net, "test_sD_minpool": sub.test,
                     "gain_vs_D": sub.net - pay0.t0, "gain_vs_live": sub.net - live.R_T,
                     "backstop_window_high": c - gross_profit(q, pay0, live.mubar)})
    return rows


def breakeven_costs(par: Params, r: float) -> dict:
    pay = payoffs(par, r)
    lo, hi = gross_profit(par, pay, 0.5), gross_profit(par, pay, par.M)
    e_H0 = 1.0 - 0.5 * math.exp(-1.0 / par.b)
    c_vs_D = lo + pay.wL + e_H0 * pay.Delta_T

    def gap_live(c: float) -> float:
        q = Params(h=par.h, ell=par.ell, p=par.p, b=par.b, k=par.k, c=c)
        return full_order_min_pool(q, r, c - lo).net - full_order_min_pool(q, r, 0.0).R_T

    c_vs_live = brentq(gap_live, lo + 1e-9, hi) if gap_live(lo + 1e-9) * gap_live(hi) < 0 else NAN
    return {"r": r, "B_prior": lo, "B_M": hi, "c_breakeven_vs_D": c_vs_D, "c_breakeven_vs_live": c_vs_live,
            "c_any_profit_bound": lo + pay.wL + par.M * pay.Delta_T}


def backstop_family(par: Params, grid: Grid, r: float) -> list[Outcome]:
    """Cutoff family of the unsubsidized fork at r; the backstop keeps member x' iff mubar < tau_{s_bar}."""
    pay = payoffs(par, r)
    xs = x_star_full(par, tau_of(par, pay, 0.0))
    out = []
    for cut in np.round(np.arange(xs, 4.001, 0.05), 4):
        fp, why = iterate(par, grid, r, 0.0, 1.0, -1.0, cutoff=float(cut))
        if fp is None:
            continue
        o = fixed_point_outcome(par, r, 0.0, "backstop", fp, 0.0, f"cutoff family x'={cut:.3f}")
        if o.E > 0.0:
            out.append(o)
    return out


def backstop_window(par: Params, r: float, family: list[Outcome]) -> list[dict]:
    pay = payoffs(par, r)
    th = thresholds(par, r)
    live0 = full_order_min_pool(par, r, 0.0)
    top = par.c - gross_profit(par, pay, live0.mubar)
    grid_s = sorted(set(np.round(np.arange(th.s_D, top + 0.25, 0.05), 4).tolist())
                    | {th.s_D, top - 1e-4, top})
    rows = []
    for sb in grid_s:
        tau_sb = tau_of(par, pay, sb)
        keep = [o for o in family if o.mubar < tau_sb]
        rows.append({"r": r, "s_bar": sb, "tau_sbar": tau_sb, "dead_removed": tau_sb <= 0.5 + TIE,
                     "min_pool_survives": live0.mubar < tau_sb, "members_searched": len(family),
                     "members_surviving": len(keep),
                     "largest_surviving_cutoff": max((o.x_star for o in keep), default=NAN),
                     "R_T_worst_surviving": min((o.R_T for o in keep), default=NAN),
                     "R_T_best_surviving": max((o.R_T for o in keep), default=NAN),
                     "E_worst_surviving": min((o.E for o in keep), default=NAN),
                     "outlay": 0.0, "x_bar": x_bar(par, tau_sb) if tau_sb > par.m else NAN,
                     "status": "analytical (window); numerical diagnostic (family members)"})
    return rows


def lottery(par: Params, grid: Grid, r: float) -> list[Outcome]:
    """Subsidy lottery: with probability rho the challenger's cost falls to B_r(m); this is (A1)."""
    pay = payoffs(par, r)
    th = thresholds(par, r)
    out = []
    for rho in [0.0, 0.02, 0.04, 0.05, 0.06, 0.07, 0.08, 0.1, 0.15, 0.2, 0.25, 0.3, 0.5]:
        rho_N = 2 * par.k / pay.Delta_T
        nt_exists = rho * pay.Delta_T / 2.0 <= par.k
        acc = accounting(par, pay, rho, rho, rho * th.s_m)
        out.append(Outcome(r=r, s=th.s_m, device=f"lottery rho={rho}", branch="no trade, entry rho",
                           q_H=0.0, q_L=0.0, e_H=rho, e_L=rho, **acc, mubar=NAN, pool_prob=0.0,
                           x_star=INF, U_H=0.0, U_L=0.0, test=f"rho-2k/Delta_T={rho - rho_N:.6g}",
                           status="analytical" if nt_exists else "analytical (not an equilibrium)"))
        if rho == 0.0:
            continue
        found: list[FixedPoint] = []
        for q0 in STARTS:
            fp, _ = iterate(par, grid, r, 0.0, *q0, rho=rho)
            if fp is None or any(abs(fp.q_H - g.q_H) < 0.015 and abs(fp.q_L - g.q_L) < 0.015 for g in found):
                continue
            found.append(fp)
            out.append(fixed_point_outcome(par, r, th.s_m, f"lottery rho={rho}", fp, rho * th.s_m,
                                           "grid fixed point"))
        print(f"lottery rho={rho}: no-trade exists={nt_exists}; found "
              + "; ".join(f"({g.q_H:+.2f},{g.q_L:+.2f})" for g in found), flush=True)
    return out


def reserve_payoffs(par: Params, r: float, p: float) -> Payoffs:
    """(A.42) for the uniform incumbent on the reserve domain p in [0, h], benchmark values ell < r < h."""
    if p <= par.ell:
        return payoffs(Params(h=par.h, ell=par.ell, p=p, b=par.b, k=par.k, c=par.c), r)
    if p <= r:
        t0 = p * (1.0 - p / r)
        tH = r / 2.0 + p * p / (2.0 * r)
        return Payoffs(r=r, t0=t0, tH=tH, tL=t0, gH=par.h - tH, gL=0.0)
    return Payoffs(r=r, t0=0.0, tH=p, tL=0.0, gH=par.h - p, gL=0.0)


def reserve_table(par: Params, r: float) -> list[dict]:
    """Does any reserve remove D? D exists iff B_{p,r}(1/2) < c. Closed forms only."""
    rows = []
    for p in [0.0, 0.25, 0.5, 0.75, 1.0, 1.01, 1.2, 1.5, 2.0, 3.0, 5.0, 7.0, 9.0]:
        pay = reserve_payoffs(par, r, p)
        tau = (par.c - pay.gL) / (pay.gH - pay.gL)
        rows.append({"r": r, "p": p, "t_0": pay.t0, "t_H": pay.tH, "t_L": pay.tL, "g_H": pay.gH, "g_L": pay.gL,
                     "Delta_T": pay.Delta_T, "B_prior": gross_profit(par, pay, 0.5), "tau": tau,
                     "dead_exists": gross_profit(par, pay, 0.5) < par.c, "live_possible": tau <= par.M,
                     "x_star_full": x_star_full(par, tau) if tau <= par.M else INF, "status": "analytical"})
    return rows


def key_numbers(par: Params, r1: float = 3.0, r0: float = 1.2) -> list[dict]:
    """Closed-form scalars quoted in note.md, with their definitions."""
    pay, th = payoffs(par, r1), thresholds(par, r1)
    tau0 = tau_of(par, pay, 0.0)
    xs = x_star_full(par, tau0)
    live = full_order_min_pool(par, r1, 0.0)
    fee = full_order_min_pool(par, r1, th.s_M)
    at_sD = full_order_min_pool(par, r1, th.s_D)

    def first_r(x_of_r) -> float:
        return brentq(lambda r: (1 - 1 / par.b) * J_closed(par, payoffs(par, r), x_of_r(r)) - par.k,
                      1.3, 3.0, xtol=1e-12)

    rows = [
        ("m", par.m, "lower posterior bound", "analytical"),
        ("M", par.M, "upper posterior bound", "analytical"),
        ("frak_r_k", frak_r(par, par.k), "r(k): Delta_T = k", "analytical"),
        ("frak_r_2k", frak_r(par, 2 * par.k), "r(2k): Delta_T = 2k; C is an equilibrium below it when s >= s_D", "analytical"),
        ("r_pool_forced", frak_r(par, par.k / ((1 - 1 / par.b) * par.m)),
         "Delta_T = k/((1-1/b)m): above it every equilibrium with s in [s_D, s_m) has a pool", "analytical"),
        ("r_hand_bound", frak_r(par, 2 * par.k / ((1 - 1 / par.b) * par.m)),
         "Delta_T = 2k/((1-1/b)m): above it J >= Delta_T m/2 proves existence for every tau_s in (m, M]", "analytical"),
        ("r_test_s0", first_r(lambda r: x_star_full(par, tau_of(par, payoffs(par, r), 0.0))),
         "smallest r with k < (1-1/b)J(x*) at s = 0 (closed-form J, numerical root)", "analytical formula, numerical root"),
        ("r_test_sD", first_r(lambda r: 0.0),
         "smallest r with k < (1-1/b)J(0), the test at s = s_D (closed-form J, numerical root)", "analytical formula, numerical root"),
        ("r_C", r_ceiling(par), "B_r(M) = c", "analytical"),
        ("t_0", pay.t0, f"r={r1}", "analytical"), ("t_H", pay.tH, f"r={r1}", "analytical"),
        ("t_L", pay.tL, f"r={r1}", "analytical"), ("Delta_T", pay.Delta_T, f"r={r1}", "analytical"),
        ("w_L", pay.wL, f"r={r1}", "analytical"), ("B_prior", gross_profit(par, pay, 0.5), f"r={r1}", "analytical"),
        ("B_M", gross_profit(par, pay, par.M), f"r={r1}", "analytical"),
        ("B_m", gross_profit(par, pay, par.m), f"r={r1}", "analytical"),
        ("tau", tau0, f"r={r1}, s=0", "analytical"), ("x_star", xs, f"r={r1}, s=0", "analytical"),
        ("J", J_closed(par, pay, xs), f"closed form at r={r1}, s=0", "analytical"),
        ("J_hand_bound", pay.Delta_T * par.m / 2.0, "Delta_T m/2 <= J", "analytical"),
        ("s_M", th.s_M, f"r={r1}", "analytical"), ("s_D", th.s_D, f"r={r1}", "analytical"),
        ("s_m", th.s_m, f"r={r1}", "analytical"), ("gain_bound", th.gain_bound, "w_L + M Delta_T", "analytical"),
        ("d_margin", th.d_margin, "s_D - w_L - M Delta_T", "analytical"),
        ("mubar_min_pool", live.mubar, f"pool posterior, minimal pool, r={r1}, s=0", "analytical"),
        ("backstop_top", par.c - gross_profit(par, pay, live.mubar), "c - B_r(mubar*), s_0 = 0", "analytical"),
        ("backstop_top_fee", par.c - gross_profit(par, pay, fee.mubar), "c - B_r(mubar*), s_0 = s_M", "analytical"),
        ("R_T_live", live.R_T, f"minimal pool, r={r1}, s=0", "analytical"),
        ("W_live", live.W, f"minimal pool, r={r1}, s=0", "analytical"),
        ("net_fee_live", fee.net, f"minimal pool, r={r1}, s=s_M (fee)", "analytical"),
        ("net_sD", at_sD.net, f"minimal pool, r={r1}, s=s_D", "analytical"),
        ("W_sD", at_sD.W, f"minimal pool, r={r1}, s=s_D", "analytical"),
        ("pigou_subsidy", par.p ** 2 / r1, "p^2/r: surplus-maximizing uniform subsidy on the minimal pool", "analytical"),
        ("net_C_sD", (par.h + par.ell) / 2.0 - par.c, "(h + ell)/2 - c: seller net under C at s_D", "analytical"),
        ("rho_N", 2 * par.k / pay.Delta_T, f"lottery: no trade fails above it, r={r1}", "analytical"),
        ("rho_U", par.k / ((1 - 1 / par.b) * par.m * pay.Delta_T), f"lottery: unique full orders above it, r={r1}",
         "analytical"),
        ("R_T_full_disclosure", pay.t0 + 0.5 * (pay.tH - pay.t0), f"theta public, r={r1}", "analytical"),
        ("s_D_r0", thresholds(par, r0).s_D, f"r={r0}", "analytical"),
    ]
    return [{"name": n, "value": v, "definition": d, "status": s} for n, v, d, s in rows]


def write_csv(path: Path, rows: list[dict]) -> None:
    keys = list(rows[0].keys())
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        for row in rows:
            w.writerow({k: (f"{v:.9g}" if isinstance(v, float) else v) for k, v in row.items()})


def main() -> None:
    par = BENCH
    grid = make_grid(par)
    r1 = 3.0
    write_csv(HERE / "key_numbers.csv", key_numbers(par, r1))
    write_csv(HERE / "subsidy_sweep_r3.csv", [asdict(o) for o in sweep_subsidy(par, grid, r1)])
    write_csv(HERE / "cost_sweep_r3.csv", sweep_cost(par, r1))
    write_csv(HERE / "breakeven_r3.csv", [breakeven_costs(par, r1)])
    fam = backstop_family(par, grid, r1)
    write_csv(HERE / "backstop_family_r3.csv", [asdict(o) for o in fam])
    write_csv(HERE / "backstop_window_r3.csv", backstop_window(par, r1, fam))
    write_csv(HERE / "lottery_r3.csv", [asdict(o) for o in lottery(par, grid, r1)])
    write_csv(HERE / "reserve_r3.csv", reserve_table(par, r1))
    write_csv(HERE / "across_strengths.csv", across_strengths(par, grid))
    print("done")


if __name__ == "__main__":
    main()
