"""Finite-support mixed-profile search with documented starts, budget, stopping rule, and attempt records (OA C.2; spec 10.3).

Domain. The favorable type H mixes over the correctly signed order mesh {0, m, 2m, ..., 1}; the low type L plays a
pure order -v with v in [0, 1]. The restriction to a pure low-type order is the OA.60 concavity argument, whose
premise (a bounded nondecreasing low-type residual against the candidate schedule) is checked on every final
iterate and recorded as ``residual_monotone``; it is never assumed silently.

Method per start. (A) Damped multiplicative-weights (replicator) iteration on the support weights with the
low-type best response damped toward v, for at most ``max_iter`` iterations; stops when the support-payoff gap
and the low-type fixed-point residual are both below ``tol`` (converged), when the gap stops decreasing over
``stall_window`` iterations (stalled), or when the budget is exhausted. (B) At the final positive-weight
support, the support-payoff indifference and probability-simplex system is solved directly (least squares in
the free weights and v); support points whose solved weight falls below the pruning threshold are removed with
their residuals retained; profitable off-support mesh actions are added and the system re-solved (at most
``max_support_rounds`` rounds). A solved support of size one is a pure profile and is reported as such.

Outcomes. ``converged-candidate`` (a mixed profile with at least two support points whose indifference and
simplex conditions hold within tolerance; validated by the caller over the full order interval), ``converged-pure``
(the search collapsed to a pure profile, reported for deduplication against the pure candidates), and
``unresolved`` (neither phase produced a candidate within the budget; the record says why). No outcome is a
statement about nonexistence.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy import optimize

from .auction import AuctionPayoffs
from .deviations import U
from .information import OrderProfile, Schedule, make_schedule
from .params import Controls, Primitives

DOMAIN_TEXT = "H mixes over the correctly signed mesh {0, m, ..., 1} at spacing m; L plays a pure order -v with v in [0, 1] (OA.60 restriction, residual monotonicity checked)"


@dataclass(frozen=True)
class MixedStart:
    start_id: str
    description: str
    weights: tuple[float, ...]
    v0: float


@dataclass(frozen=True)
class MixedAttempt:
    r: str
    mesh: float
    start_id: str
    start_description: str
    v_init: float
    domain: str
    budget: int
    iterations: int
    stop_reason: str                    # converged | stalled | budget_exhausted
    final_gap: float                    # support-payoff gap on the mesh at the last replicator iterate
    final_v_residual: float             # |BR_L(v) - v| at the last replicator iterate
    support_solve: str                  # solved | pruned_to_pure | failed | rounds_exhausted | not_attempted
    support_solve_residual: float
    support_rounds: int
    pruned_points: tuple[tuple[float, float, float], ...]   # (q, weight at removal, payoff gap at removal) with residual retained
    support_q: tuple[float, ...]
    support_w: tuple[float, ...]
    support_payoffs: tuple[float, ...]
    gap_to_best_tested: tuple[float, ...]            # per support point: best mesh payoff minus U(q_j)
    best_tested_q: float
    v: float
    simplex_residual: float             # |sum w - 1|
    min_weight: float
    residual_monotone: bool
    outcome: str                        # converged-candidate | converged-pure | unresolved
    witness: str
    profile: OrderProfile | None = field(default=None, compare=False)
    sched: Schedule | None = field(default=None, compare=False)

    def support_text(self) -> str:
        return ";".join(f"{q:.6g}:{w:.6g}" for q, w in zip(self.support_q, self.support_w))


def default_starts(qs: np.ndarray, scale: float = 0.05) -> list[MixedStart]:
    """Three documented initialisations: uniform weights at v = 0.5; mass near q = 1 at v = 0.9; mass near q = 0 at v = 0.1."""
    n = len(qs)
    uni = np.full(n, 1.0 / n)
    hi = np.exp(-(1.0 - qs) / scale)
    lo = np.exp(-qs / scale)
    return [MixedStart("S1_uniform_v0.5", "uniform weights on the mesh; v = 0.5", tuple(uni.tolist()), 0.5),
            MixedStart("S2_mass_near_1_v0.9", f"weights proportional to exp(-(1-q)/{scale}); v = 0.9", tuple((hi / hi.sum()).tolist()), 0.9),
            MixedStart("S3_mass_near_0_v0.1", f"weights proportional to exp(-q/{scale}); v = 0.1", tuple((lo / lo.sum()).tolist()), 0.1)]


def _profile(qs: np.ndarray, w: np.ndarray, v: float, prune: float) -> OrderProfile:
    keep = w > prune
    ww = w[keep] / w[keep].sum()
    return OrderProfile(tuple(qs[keep].tolist()), tuple(ww.tolist()), (-float(v),), (1.0,))


def best_response_L(sched: Schedule, grid_n: int = 21) -> tuple[float, float]:
    """Global maximiser of U_L(-s) over s in [0, 1]: coarse grid then bounded refinement around the best cell."""
    grid = np.linspace(0.0, 1.0, grid_n)
    vals = np.array([U(sched, "L", -s).value for s in grid])
    i = int(vals.argmax())
    lo, hi = grid[max(i - 1, 0)], grid[min(i + 1, grid_n - 1)]
    res = optimize.minimize_scalar(lambda s: -U(sched, "L", -s).value, bounds=(lo, hi), method="bounded", options={"xatol": 1e-11})
    if -res.fun >= vals[i]:
        return float(res.x), float(-res.fun)
    return float(grid[i]), float(vals[i])


def residual_monotone(sched: Schedule) -> bool:
    """OA.60 premise for the low type: A_L nondecreasing in the flow (checked on a grid across the hull)."""
    lo, hi = sched.hull()
    xs = np.linspace(lo - 3 * sched.prim.fb, hi + 3 * sched.prim.fb, 2001)
    return bool(np.all(np.diff(sched.A(xs, "L")) >= -1e-12))


def replicator(prim: Primitives, pay: AuctionPayoffs, qs: np.ndarray, w0: np.ndarray, v0: float, max_iter: int, tol: float,
               beta: float = 40.0, prune: float = 1e-7, stall_window: int = 25, stall_rel: float = 0.02) -> dict:
    w = np.asarray(w0, dtype=float).copy()
    v = float(v0)
    history: list[tuple[int, float, float]] = []
    stop = "budget_exhausted"
    pay_H = np.zeros(len(qs))
    for it in range(max_iter):
        sched = make_schedule(prim, pay, _profile(qs, w, v, 0.0))
        pay_H = np.array([U(sched, "H", q).value for q in qs])
        bv, _ = best_response_L(sched)
        supp = w > prune
        gap = float(pay_H.max() - pay_H[supp].min())
        vres = float(abs(bv - v))
        history.append((it, gap, vres))
        if gap < tol and vres < tol:
            stop = "converged"
            break
        if len(history) > stall_window and history[-1][1] > (1 - stall_rel) * history[-1 - stall_window][1] and vres < tol:
            stop = "stalled"
            break
        w = w * np.exp(beta * (pay_H - pay_H.max()))
        w[w < prune * 1e-3] = 0.0
        w = w / w.sum()
        v = 0.5 * v + 0.5 * bv
    return {"w": w, "v": v, "history": history, "stop": stop, "iterations": len(history), "pay_H": pay_H}


def solve_support(prim: Primitives, pay: AuctionPayoffs, support: np.ndarray, w0: np.ndarray, v0: float, tol: float) -> dict:
    """Solve U_H(q_j) = U_H(q_1) for all j, sum w = 1, BR_L(v) = v in the free weights (w_2..w_n) and v; bounded to [0, 1]."""
    n = len(support)
    if n == 1:
        # pure high-type order: the low type's fixed point v = BR_L(v) by damped iteration, polished by a bracketed root
        u = float(support[0])
        g = lambda s: best_response_L(make_schedule(prim, pay, OrderProfile((u,), (1.0,), (-s,), (1.0,))))[0] - s
        v, nfev = float(v0), 0
        for _ in range(30):
            d = g(v)
            nfev += 1
            if abs(d) < tol:
                break
            v = min(1.0, max(0.0, v + 0.5 * d))
        d = g(v)
        if abs(d) >= tol:
            a, b_ = max(0.0, v - 0.05), min(1.0, v + 0.05)
            if g(a) * g(b_) < 0:
                v = float(optimize.brentq(g, a, b_, xtol=1e-11))
                d = g(v)
        return {"w": np.array([1.0]), "v": v, "residual": abs(d), "ok": abs(d) < tol, "nfev": nfev}

    def residuals(z: np.ndarray) -> np.ndarray:
        wf = np.clip(z[:-1], 0.0, 1.0)
        w1 = 1.0 - wf.sum()
        vv = float(np.clip(z[-1], 0.0, 1.0))
        w = np.concatenate([[max(w1, 0.0)], wf])
        if w.sum() <= 0:
            return np.full(n, 1.0)
        sched = make_schedule(prim, pay, OrderProfile(tuple(support.tolist()), tuple((w / w.sum()).tolist()), (-vv,), (1.0,)))
        uH = np.array([U(sched, "H", q).value for q in support])
        bv, _ = best_response_L(sched)
        return np.concatenate([uH[1:] - uH[0], [bv - vv, min(w1, 0.0)]])

    z0 = np.concatenate([np.asarray(w0[1:], dtype=float), [v0]])
    res = optimize.least_squares(residuals, z0, bounds=(np.zeros(n), np.ones(n)), xtol=1e-12, ftol=1e-12, gtol=1e-12, max_nfev=200)
    wf = np.clip(res.x[:-1], 0.0, 1.0)
    w = np.concatenate([[1.0 - wf.sum()], wf])
    return {"w": w, "v": float(np.clip(res.x[-1], 0.0, 1.0)), "residual": float(np.max(np.abs(res.fun))), "ok": bool(res.success and np.max(np.abs(res.fun)) < tol),
            "nfev": int(res.nfev)}


def mixed_search_node(prim: Primitives, pay: AuctionPayoffs, controls: Controls, r_label: str, meshes: tuple[float, ...] = (0.05, 0.025),
                      max_iter: int = 120, tol: float = 1e-7, prune: float = 1e-7, max_support_rounds: int = 8,
                      starts: list[MixedStart] | None = None) -> list[MixedAttempt]:
    """Run every documented start on every mesh and return one attempt record per (mesh, start)."""
    out: list[MixedAttempt] = []
    for mesh in meshes:
        qs = np.round(np.arange(0.0, 1.0 + 1e-12, mesh), 10)
        for st in (starts if starts is not None else default_starts(qs)):
            rep = replicator(prim, pay, qs, np.array(st.weights), st.v0, max_iter, tol, prune=prune)
            hist = rep["history"]
            gap_last, vres_last = hist[-1][1], hist[-1][2]
            w, v = rep["w"], rep["v"]
            support = qs[w > prune]
            w_s = w[w > prune] / w[w > prune].sum()
            # (B) support reduction and the indifference/simplex system. Dominated support points (payoff below the
            # support maximum by more than tol at the current iterate) are removed with their residuals retained;
            # profitable off-support mesh actions are added; the system is then solved on the remaining support.
            pruned: list[tuple[float, float, float]] = []
            solve_status, solve_res, rounds = "not_attempted", float("nan"), 0
            sol = None
            while rounds < max_support_rounds:
                rounds += 1
                sched = make_schedule(prim, pay, OrderProfile(tuple(support.tolist()), tuple(w_s.tolist()), (-float(v),), (1.0,)))
                pay_mesh = np.array([U(sched, "H", q).value for q in qs])
                on = np.isin(qs, support)
                sup_pay = pay_mesh[on]
                dominated = sup_pay < sup_pay.max() - tol
                if dominated.any() and (~dominated).sum() >= 1:
                    pruned.extend((float(q), float(wt), float(sup_pay.max() - pv)) for q, wt, pv in zip(support[dominated], w_s[dominated], sup_pay[dominated]))
                    support, w_s = support[~dominated], w_s[~dominated] / w_s[~dominated].sum()
                    solve_status = "pruning"
                    continue
                off_gain = float(pay_mesh[~on].max() - sup_pay.max()) if (~on).any() else -np.inf
                if off_gain > tol and sol is None:
                    q_add = float(qs[~on][int(pay_mesh[~on].argmax())])
                    old_w = dict(zip(support.tolist(), w_s.tolist()))
                    support = np.array(sorted(support.tolist() + [q_add]))
                    w_s = np.array([old_w.get(float(q), 0.5) for q in support])
                    w_s = w_s / w_s.sum()
                    solve_status = "adding_off_support"
                    continue
                sol = solve_support(prim, pay, support, w_s, v, tol)
                solve_res = sol["residual"]
                if not sol["ok"]:
                    solve_status = "failed"
                    break
                w_s, v = sol["w"] / sol["w"].sum(), sol["v"]
                small = w_s <= prune
                if small.any() and (~small).sum() >= 1:
                    pruned.extend((float(q), float(wt), 0.0) for q, wt in zip(support[small], w_s[small]))
                    support, w_s = support[~small], w_s[~small] / w_s[~small].sum()
                    solve_status = "pruning"
                    sol = None
                    continue
                solve_status = "solved" if len(support) > 1 else "pruned_to_pure"
                break
            else:
                solve_status = "rounds_exhausted"
            # final record at the solved (or last) support
            prof = OrderProfile(tuple(float(q) for q in support), tuple(float(x) for x in w_s), (-float(v),), (1.0,))
            sched = make_schedule(prim, pay, prof)
            pay_mesh = np.array([U(sched, "H", q).value for q in qs])
            sup_pay = np.array([U(sched, "H", q).value for q in support])
            best_q = float(qs[int(pay_mesh.argmax())])
            gaps = tuple(float(pay_mesh.max() - p) for p in sup_pay)
            bv, _ = best_response_L(sched)
            simplex = float(abs(sum(prof.w_H) - 1.0))
            mono = residual_monotone(sched)
            solved_ok = solve_status in ("solved", "pruned_to_pure") and sol is not None and sol["ok"] and max(gaps) < tol and abs(bv - v) < tol
            if solved_ok and len(support) >= 2:
                outcome, witness = "converged-candidate", ""
            elif solved_ok:
                outcome, witness = "converged-pure", f"support collapsed to the pure profile ({support[0]:.6g},{-v:.6g})"
            else:
                outcome = "unresolved"
                witness = (f"replicator {rep['stop']} after {rep['iterations']} of {max_iter} iterations (gap {gap_last:.3e}, v residual {vres_last:.3e}); "
                           f"support solve {solve_status} (residual {solve_res:.3e}); best tested mesh gain {max(gaps):.3e} at q = {best_q:.4g}")
            out.append(MixedAttempt(r_label, mesh, st.start_id, st.description, st.v0, DOMAIN_TEXT.replace("spacing m", f"spacing {mesh}"), max_iter,
                                    rep["iterations"], rep["stop"], float(gap_last), float(vres_last), solve_status, float(solve_res), rounds,
                                    tuple(pruned), tuple(float(q) for q in support), tuple(float(x) for x in w_s), tuple(float(x) for x in sup_pay),
                                    gaps, best_q, float(v), simplex, float(min(w_s)), mono, outcome, witness, prof, sched))
    return out


ATTEMPT_COLUMNS = ["r", "mesh", "start_id", "start_description", "v_init", "domain", "budget", "iterations", "stop_reason", "final_gap",
                   "final_v_residual", "support_solve", "support_solve_residual", "support_rounds", "pruned_points", "support",
                   "support_payoffs", "gap_to_best_tested", "best_tested_q", "v", "simplex_residual", "min_weight", "residual_monotone",
                   "outcome", "witness", "validation"]


def attempt_row(a: MixedAttempt, validation_text: str = "") -> dict:
    return {"r": a.r, "mesh": a.mesh, "start_id": a.start_id, "start_description": a.start_description, "v_init": a.v_init, "domain": a.domain,
            "budget": a.budget, "iterations": a.iterations, "stop_reason": a.stop_reason, "final_gap": a.final_gap,
            "final_v_residual": a.final_v_residual, "support_solve": a.support_solve, "support_solve_residual": a.support_solve_residual,
            "support_rounds": a.support_rounds, "pruned_points": ";".join(f"{q:.6g}:w={w:.3e}:gap={g:.3e}" for q, w, g in a.pruned_points),
            "support": a.support_text(), "support_payoffs": ";".join(f"{p:.10g}" for p in a.support_payoffs),
            "gap_to_best_tested": ";".join(f"{g:.3e}" for g in a.gap_to_best_tested), "best_tested_q": a.best_tested_q, "v": a.v,
            "simplex_residual": a.simplex_residual, "min_weight": a.min_weight, "residual_monotone": a.residual_monotone,
            "outcome": a.outcome, "witness": a.witness, "validation": validation_text}
