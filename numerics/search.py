"""Equilibrium search layer (C.1, C.2). Returns candidates and unresolved nodes; never accepts."""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy import optimize

from .auction import AuctionPayoffs
from .deviations import U, dU, F
from .information import OrderProfile, Schedule, entry_at_posterior, make_schedule
from .noise import posterior_bounds
from .params import Primitives


@dataclass(frozen=True)
class Margins:
    """Analytical margins at a node (OA.68, Proposition 3)."""
    low_cost_floor: float          # B_r(m) - c_L  (>0: every low-cost realization enters)
    high_prior_exclusion: float    # c_H - B_r(1/2)
    high_ceiling: float            # B_r(M) - c_H  (>0: expensive entry feasible at the ceiling)
    pooling_exists: float          # k - e0 Delta_T / 2   (>=0: pooling is an equilibrium)
    pooling_unique_bound: float    # k - Delta_T          (>0: no trade is unique)
    full_unique_bound: float       # (1-1/b) rho m Delta_T - k  (>0: full orders unique)
    e0: float                      # actual prior entry probability H_C(B_r(1/2))
    in_domain: bool                # low_cost_floor > 0 and high_prior_exclusion > 0


def margins(prim: Primitives, pay: AuctionPayoffs) -> Margins:
    m, M = posterior_bounds(prim.fb)
    rho, k, b = prim.frho, prim.fk, prim.fb
    e0 = float(entry_at_posterior(prim, pay, np.array([0.5]))[0])
    lc = pay.B(m) - prim.fc_L
    hp = prim.fc_H - pay.B(0.5)
    return Margins(
        low_cost_floor=lc,
        high_prior_exclusion=hp,
        high_ceiling=pay.B(M) - prim.fc_H,
        pooling_exists=k - e0 * pay.Delta_T / 2,
        pooling_unique_bound=k - pay.Delta_T,
        full_unique_bound=(1 - 1 / b) * rho * m * pay.Delta_T - k,
        e0=e0,
        in_domain=(lc > 0) and (hp > 0),
    )


@dataclass
class Candidate:
    branch: str                     # pooling | full_orders | asymmetric | pure | mixed
    profile: OrderProfile
    sched: Schedule
    diagnostics: dict = field(default_factory=dict)
    unresolved_reason: str = ""


# --- full-order candidate: sharper existence test and derivative bounds -----------------
def J_test(sched: Schedule) -> dict:
    """OA.22: J = F_H(1) = F_L(1); k < (1 - 1/b) J is sufficient for full-order existence."""
    prim = sched.prim
    JH = F(sched, "H", 1.0).value
    JL = F(sched, "L", 1.0).value
    return {"J_H": JH, "J_L": JL, "J_gap": abs(JH - JL), "J_margin": (1 - 1 / prim.fb) * min(JH, JL) - prim.fk}


def derivative_cover(sched: Schedule, state: str, n_mesh: int) -> dict:
    """Floating-point analogue of OA.64: min_j U'(s_j) - L_U/(2n) on the mesh s_j = j/n."""
    Delta = sched.pay.Delta_T
    b = sched.prim.fb
    L_U = 2 * Delta / b + Delta / (b * b)
    vals = np.array([dU(sched, state, j / n_mesh).value for j in range(n_mesh + 1)])
    return {"min_dU": float(vals.min()), "argmin_s": float(vals.argmin() / n_mesh),
            "gamma": float(vals.min() - L_U / (2 * n_mesh)), "L_U": L_U, "dU_at_1": float(vals[-1])}


def full_order_candidate(prim: Primitives, pay: AuctionPayoffs, regime: str = "feedback", dividend: float = 0.0) -> Candidate:
    sched = make_schedule(prim, pay, OrderProfile.pure(1.0, -1.0), regime, dividend)
    diag = J_test(sched)
    diag["dU_L_at_1"] = dU(sched, "L", 1.0).value
    diag["dU_H_at_1"] = dU(sched, "H", 1.0).value
    return Candidate("full_orders", sched.profile, sched, diag)


def pooling_candidate(prim: Primitives, pay: AuctionPayoffs, regime: str = "feedback", dividend: float = 0.0) -> Candidate:
    sched = make_schedule(prim, pay, OrderProfile.pure(0.0, 0.0), regime, dividend)
    mg = margins(prim, pay)
    return Candidate("pooling", sched.profile, sched, {"pooling_coefficient": mg.e0 * pay.Delta_T / 2 - prim.fk})


# --- asymmetric continuation (1, -v) -------------------------------------------------------
def Psi(prim: Primitives, pay: AuctionPayoffs, v: float) -> float:
    """Psi(r, v) = U_L'(v; 1, -v): unilateral derivative at s = v against the schedule for (1, -v)."""
    sched = make_schedule(prim, pay, OrderProfile.pure(1.0, -v))
    return dU(sched, "L", v).value


def asymmetric_roots(prim: Primitives, pay: AuctionPayoffs, mesh: float = 0.01,
                     extra_brackets: list[tuple[float, float]] | None = None, v_lo: float = 0.005,
                     v_hi: float = 0.995) -> dict:
    """Bracket sign changes of Psi on the magnitude mesh, polish with Brent, and look for tangencies."""
    vs = np.arange(v_lo, v_hi + 1e-12, mesh)
    vs = np.array(sorted(set(np.round(vs, 10).tolist()) | {v_lo, v_hi}))
    psi = np.array([Psi(prim, pay, v) for v in vs])
    roots, brackets = [], []
    for i in range(len(vs) - 1):
        if psi[i] == 0.0:
            roots.append(float(vs[i]))
        elif psi[i] * psi[i + 1] < 0:
            brackets.append((float(vs[i]), float(vs[i + 1])))
    for br in extra_brackets or []:
        brackets.append(br)
    for a, b_ in brackets:
        fa, fb = Psi(prim, pay, a), Psi(prim, pay, b_)
        if fa * fb < 0:
            roots.append(float(optimize.brentq(lambda v: Psi(prim, pay, v), a, b_, xtol=1e-13, rtol=1e-13)))
    # local minima of |Psi| that do not change sign: potential tangencies (retained, not claimed)
    tangencies = []
    absv = np.abs(psi)
    for i in range(1, len(vs) - 1):
        if absv[i] < absv[i - 1] and absv[i] < absv[i + 1] and psi[i - 1] * psi[i + 1] > 0:
            res = optimize.minimize_scalar(lambda v: abs(Psi(prim, pay, v)), bounds=(vs[i - 1], vs[i + 1]), method="bounded",
                                           options={"xatol": 1e-10})
            tangencies.append((float(res.x), float(res.fun)))
    roots = sorted(set(round(r, 12) for r in roots))
    return {"v_mesh": vs, "psi_mesh": psi, "roots": roots, "tangencies": tangencies,
            "psi_at_v_hi": float(psi[-1]), "psi_at_v_lo": float(psi[0])}


def asymmetric_candidate(prim: Primitives, pay: AuctionPayoffs, v: float) -> Candidate:
    sched = make_schedule(prim, pay, OrderProfile.pure(1.0, -v))
    diag = {"v": v, "Psi": dU(sched, "L", v).value, "dU_H_at_1": dU(sched, "H", 1.0).value}
    diag.update(J_test(sched))
    return Candidate("asymmetric", sched.profile, sched, diag)


# --- best-response map for pure profiles ---------------------------------------------------
def best_response(sched: Schedule, state: str, grid_n: int = 41) -> tuple[float, float]:
    """Global maximizer of U_theta(s) over correctly signed magnitudes s in [0, 1]. Returns (s*, U*)."""
    eps = 1.0 if state == "H" else -1.0
    grid = np.linspace(0.0, 1.0, grid_n)
    vals = np.array([U(sched, state, eps * s).value for s in grid])
    i = int(vals.argmax())
    lo, hi = grid[max(i - 1, 0)], grid[min(i + 1, grid_n - 1)]
    if hi > lo:
        res = optimize.minimize_scalar(lambda s: -U(sched, state, eps * s).value, bounds=(lo, hi), method="bounded",
                                       options={"xatol": 1e-11})
        if -res.fun >= vals[i]:
            return float(res.x), float(-res.fun)
    return float(grid[i]), float(vals[i])


def pure_fixed_points(prim: Primitives, pay: AuctionPayoffs, inits: list[tuple[float, float]] | None = None,
                      max_iter: int = 60, tol: float = 1e-7, damping: float = 0.5) -> dict:
    """Search fixed points (u, v) of the best-response map over [0,1]^2 from several initializations.

    Returns converged distinct fixed points and the list of initializations that did not converge.
    """
    if inits is None:
        inits = [(u, v) for u in (0.0, 0.25, 0.5, 0.75, 1.0) for v in (0.0, 0.25, 0.5, 0.75, 1.0)]
    found, failed = [], []
    for u0, v0 in inits:
        u, v = u0, v0
        ok = False
        for _ in range(max_iter):
            sched = make_schedule(prim, pay, OrderProfile.pure(u, -v))
            bu, _ = best_response(sched, "H")
            bv, _ = best_response(sched, "L")
            du, dv = bu - u, bv - v
            if abs(du) < tol and abs(dv) < tol:
                ok = True
                break
            u = min(1.0, max(0.0, u + damping * du))
            v = min(1.0, max(0.0, v + damping * dv))
        if not ok and abs(du) < 1e-3 and abs(dv) < 1e-3:
            # linear convergence is slow near the fixed point: polish by solving BR(u,v) - (u,v) = 0
            free = [i for i, (x, d) in enumerate(((u, du), (v, dv))) if 1e-9 < x < 1 - 1e-9 or abs(d) > tol]
            if free:
                def gfun(z):
                    uu, vv = u, v
                    if 0 in free:
                        uu = z[free.index(0)]
                    if 1 in free:
                        vv = z[free.index(1)]
                    uu, vv = min(1.0, max(0.0, uu)), min(1.0, max(0.0, vv))
                    sch = make_schedule(prim, pay, OrderProfile.pure(uu, -vv))
                    out = []
                    if 0 in free:
                        out.append(best_response(sch, "H")[0] - uu)
                    if 1 in free:
                        out.append(best_response(sch, "L")[0] - vv)
                    return out
                z0 = [(u, v)[i] for i in free]
                sol, info, ier, _ = optimize.fsolve(gfun, z0, full_output=True, xtol=1e-12)
                if ier == 1:
                    uu, vv = u, v
                    if 0 in free:
                        uu = min(1.0, max(0.0, sol[free.index(0)]))
                    if 1 in free:
                        vv = min(1.0, max(0.0, sol[free.index(1)]))
                    sch = make_schedule(prim, pay, OrderProfile.pure(uu, -vv))
                    if abs(best_response(sch, "H")[0] - uu) < tol and abs(best_response(sch, "L")[0] - vv) < tol:
                        u, v, ok = uu, vv, True
        if ok:
            if not any(abs(u - fu) < 1e-6 and abs(v - fv) < 1e-6 for fu, fv, _ in found):
                found.append((u, v, (u0, v0)))
        else:
            failed.append((u0, v0, u, v))
    return {"fixed_points": found, "unconverged": failed}


# --- finite-support mixed search -------------------------------------------------------------
def mixed_support_search(prim: Primitives, pay: AuctionPayoffs, mesh: float = 0.05, iters: int = 300,
                         beta: float = 40.0, prune: float = 1e-7, tol: float = 1e-7, init_v: float = 0.5,
                         init_weights: np.ndarray | None = None) -> dict:
    """Search a mixed profile: H mixes over the correctly signed mesh, L plays its unique best response.

    L's problem is strictly concave against any schedule with a nondecreasing residual (OA.60), so
    only the favorable type can mix. Weights follow damped multiplicative updates toward the
    support-payoff indifference condition. The result is a candidate with its diagnostics, or an
    unresolved record; wrong-signed orders are checked as deviations of the final candidate.
    """
    qs = np.round(np.arange(0.0, 1.0 + 1e-12, mesh), 10)
    w = np.full(len(qs), 1.0 / len(qs)) if init_weights is None else init_weights.copy()
    v = init_v
    history = []
    converged = False
    for it in range(iters):
        prof = OrderProfile(tuple(qs.tolist()), tuple(w.tolist()), (-v,), (1.0,))
        sched = make_schedule(prim, pay, prof)
        pay_H = np.array([U(sched, "H", q).value for q in qs])
        bv, _ = best_response(sched, "L")
        supp = w > prune
        gap = pay_H.max() - pay_H[supp].min()
        history.append((it, float(gap), float(abs(bv - v))))
        if gap < tol and abs(bv - v) < tol:
            converged = True
            break
        w = w * np.exp(beta * (pay_H - pay_H.max()))
        w[w < prune * 1e-3] = 0.0
        w = w / w.sum()
        v = 0.5 * v + 0.5 * bv
    supp = w > prune
    prof = OrderProfile(tuple(qs[supp].tolist()), tuple((w[supp] / w[supp].sum()).tolist()), (-v,), (1.0,))
    sched = make_schedule(prim, pay, prof)
    pay_H = np.array([U(sched, "H", q).value for q in qs])
    on = np.isin(qs, qs[supp])
    return {"profile": prof, "sched": sched, "converged": converged, "iterations": len(history),
            "support_gap": float(pay_H[on].max() - pay_H[on].min()) if on.any() else float("nan"),
            "off_support_gain": float((pay_H[~on].max() - pay_H[on].max()) if (~on).any() else -np.inf),
            "mesh_q": qs, "payoffs": pay_H, "weights": w, "v": v, "history": history}
