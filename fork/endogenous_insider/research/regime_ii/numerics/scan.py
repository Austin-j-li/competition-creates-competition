"""Cutoff-family scan with continuation and branch-end refinement; one parameter point at a time.

A parameter point is (r1, rho, c_L) with c_H fixed. The scan returns every distinct pure-order equilibrium
found, labelled by family. It uses engine.py for payoffs and search.py for best-response iteration.
Records are numerical diagnostics until verify.py confirms them.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np
from scipy.optimize import brentq

from engine import Econ, build_schedule, entry_at_belief, make_econ, no_trade_exists, outcome, pure
from search import Candidate, iterate_pure, make_candidate, pool_end_of

STARTS_FAST: tuple[tuple[float, float], ...] = (
    (1.0, -1.0), (1.0, -0.5), (0.5, -0.5), (0.0, 0.0), (1.0, 0.0), (0.25, -0.25), (0.5, 0.0), (0.0, -0.5),
    (-0.5, 0.5), (0.5, 0.5),
)


def regime_of(ec: Econ) -> str:
    """I: cheap type prepares at belief m. II: not at m, but at 1/2. III: only above 1/2. IV: never."""
    if ec.tauL <= ec.m + 1e-13:
        return "I"
    if ec.tauL <= 0.5 + 1e-13:
        return "II"
    if ec.tauL <= ec.M + 1e-13:
        return "III"
    return "IV"


def xbar_full(ec: Econ) -> float:
    """Largest half-line cutoff whose pool belief under full orders stays below tau_L (+inf if tau_L >= 1/2)."""
    b = ec.b
    if ec.tauL <= ec.m + 1e-13:
        return -math.inf
    if ec.tauL >= 0.5 - 1e-13:
        return math.inf

    def F(z: float) -> float:
        return 0.5 * math.exp(z / b) if z <= 0 else 1.0 - 0.5 * math.exp(-z / b)

    g = lambda x: F(x - 1.0) / (F(x - 1.0) + F(x + 1.0)) - ec.tauL  # noqa: E731
    return brentq(g, -1.0, 400.0, xtol=1e-13)


def cutoff_grid(ec: Econ, step: float = 0.1, cap: float = 7.0) -> list[float | None]:
    """None (minimal pool) then cutoffs from -1 to just above the largest consistent cutoff, capped."""
    xb = xbar_full(ec)
    if xb == -math.inf:          # regime I: no voluntary pool is consistent
        return [None]
    top = cap if math.isinf(xb) else min(cap, xb + 2.0 * step)
    grid: list[float | None] = [None]
    if top > -1.0:
        grid += [float(round(x, 6)) for x in np.arange(-1.0, top + 1e-9, step)]
    return grid


def family_label(qH: float, qL: float, voluntary: bool) -> str:
    if abs(qH) < 1e-9 and abs(qL) < 1e-9:
        return "notrade"
    full = abs(qH - 1.0) < 1e-6 and abs(qL + 1.0) < 1e-6
    kind = "full" if full else "partial"
    return f"{kind}-{'pool' if voluntary else 'minimal'}"


@dataclass
class ScanResult:
    ec: Econ
    members: list[Candidate] = field(default_factory=list)
    unresolved: int = 0
    n_cutoffs: int = 0
    labels: list[str] = field(default_factory=list)


def scan_point(ec: Econ, step: float = 0.1, starts: tuple[tuple[float, float], ...] = STARTS_FAST,
               refine: bool = True, cap: float = 7.0) -> ScanResult:
    """Scan the cutoff family by continuation; refine the end of each branch by bisection."""
    res = ScanResult(ec=ec)
    seen: dict[tuple[float, float, float], Candidate] = {}
    prev: list[tuple[float, float]] = []
    grid = cutoff_grid(ec, step, cap)
    res.n_cutoffs = len(grid)
    last_ok: dict[int, tuple[float, tuple[float, float]]] = {}
    for cut in grid:
        extra = tuple(prev)
        now: list[tuple[float, float]] = []
        order = list(starts) + [s for s in extra if all(abs(s[0] - t[0]) > 1e-6 or abs(s[1] - t[1]) > 1e-6 for t in starts)]
        got: list[tuple[float, float]] = []
        for st in order:
            fp = iterate_pure(ec, st, cut)
            if fp is None:
                res.unresolved += 1
                continue
            qH, qL, it = fp
            if any(abs(qH - a) < 1e-5 and abs(qL - c) < 1e-5 for a, c in got):
                continue
            cand = make_candidate(ec, qH, qL, cut, "pure", it, st)
            if cand.consistent and cand.regret_H <= 1e-9 and cand.regret_L <= 1e-9:
                got.append((qH, qL))
                key = (round(qH, 5), round(qL, 5), round(cand.pool_end, 5))
                if key not in seen:
                    seen[key] = cand
        prev = got
    members = list(seen.values())
    if refine:
        members += _refine_ends(ec, members, step)
    res.members = _dedupe(members)
    return res


def _dedupe(cands: list[Candidate]) -> list[Candidate]:
    out: dict[tuple[float, float, float], Candidate] = {}
    for c in cands:
        out.setdefault((round(c.qH, 5), round(c.qL, 5), round(c.pool_end, 5)), c)
    return sorted(out.values(), key=lambda c: (c.pool_end, c.qL))


def _same_branch(a: Candidate, b: Candidate) -> bool:
    return abs(a.qH - b.qH) < 0.25 and abs(a.qL - b.qL) < 0.25


def _try(ec: Econ, start: Candidate, cutoff: float) -> Candidate | None:
    fp = iterate_pure(ec, (start.qH, start.qL), cutoff)
    if fp is None:
        return None
    cand = make_candidate(ec, fp[0], fp[1], cutoff, "pure", fp[2], (start.qH, start.qL))
    ok = cand.consistent and cand.regret_H <= 1e-9 and cand.regret_L <= 1e-9 and _same_branch(cand, start)
    return cand if ok else None


def _refine_ends(ec: Econ, members: list[Candidate], step: float) -> list[Candidate]:
    """For every member with a gap next to it, bisect on the cutoff to find the end of its branch.

    A branch is followed by starting best-response iteration at the previous member's orders. The new
    member must have orders within 0.25 of the previous one, which keeps the bisection on one branch.
    Both directions are refined: the upper end carries the lowest entry, the lower end shows where the
    branch starts.
    """
    extra: list[Candidate] = []
    for c in members:
        if c.cutoff == -math.inf or c.cutoff <= -1.0 + 1e-9:
            continue
        for direction in (+1.0, -1.0):
            lo, cur = c.cutoff, c
            hi = lo + direction * step
            if direction < 0 and hi < -1.0:
                continue
            if _try(ec, cur, hi) is not None:
                continue
            for _ in range(14):
                mid = 0.5 * (lo + hi)
                cand = _try(ec, cur, mid)
                if cand is not None:
                    lo, cur = mid, cand
                else:
                    hi = mid
            if cur is not c:
                extra.append(cur)
    return extra


def row_of(ec: Econ, c: Candidate, ec_weak: Econ) -> dict:
    """One CSV row for a candidate. Reversal is judged against the weak-incumbent no-trade benchmark."""
    forced = pool_end_of(build_schedule(ec, pure(c.qH, c.qL, None)))
    voluntary = (c.pool_end - forced) > 1e-7 if math.isfinite(c.pool_end) and math.isfinite(forced) else (
        math.isfinite(c.pool_end) and not math.isfinite(forced))
    e_weak = entry_at_belief(ec_weak, 0.5)
    o_weak = 0.5 * e_weak
    o = c.out
    return {
        "r": ec.r, "rho": ec.rho, "cL": ec.cL, "cH": ec.cH, "tauL": ec.tauL, "tauH": ec.tauH,
        "regime": regime_of(ec), "family": family_label(c.qH, c.qL, bool(voluntary)),
        "cutoff": c.cutoff, "pool_end": c.pool_end, "qH": c.qH, "qL": c.qL,
        "eH": o.eH, "eL": o.eL, "E": o.E, "O_H": o.O_H, "pool_prob": o.pool_prob, "pool_belief": o.pool_belief,
        "var_mu": o.var_mu, "informative": o.var_mu > 1e-10,
        "E_weak": e_weak, "OH_weak": o_weak,
        "E_gt_weak": o.E > e_weak + 1e-12, "OH_gt_weak": o.O_H > o_weak + 1e-12,
        "reversal": (o.E > e_weak + 1e-12) and (o.O_H > o_weak + 1e-12),
        "regret_H": c.regret_H, "regret_L": c.regret_L,
        "entry_gap_E": o.E - e_weak, "entry_gap_OH": o.O_H - o_weak,
    }
