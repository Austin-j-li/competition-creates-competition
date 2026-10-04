"""Mixed-profile checks.

A mixed equilibrium needs a type to be indifferent between two orders that are both global maxima of its
payoff against the schedule the mixture itself creates. Two checks:

1. audit(): sample many consistent schedules (pure and two-atom mixtures, half-line and island pools) and
   count the local maxima of each type's payoff on [0,1] (H) or [-1,0] (L). If every sampled schedule has
   one local maximum, the best response is a single order and no mixture can be an equilibrium on that
   class of schedules. If some schedules have two, the gap between the two peaks shows how close a tie is.
2. mixed_search(): for a given pool, solve for two-atom mixtures of one type (the other type pure on a
   lattice) by choosing the weight that equalises the two payoffs, then test global optimality.

Both are numerical diagnostics. They are not exhaustive: supports larger than two, and both types mixing at
once, are only covered by the audit through random two-atom draws.
"""
from __future__ import annotations

import math

import numpy as np
from scipy.optimize import brentq

from engine import (Econ, Profile, QGRID_H, QGRID_L, best_response, build_schedule, outcome, payoff)


def local_maxima(u: np.ndarray, tol: float = 1e-12) -> list[int]:
    """Indices of strict local maxima of a sampled payoff curve, ignoring plateaus below tol."""
    idx = []
    n = len(u)
    for i in range(n):
        left = u[i] - u[i - 1] if i > 0 else math.inf
        right = u[i] - u[i + 1] if i < n - 1 else math.inf
        if left > tol and right >= -tol and u[i] > tol:
            idx.append(i)
        elif left >= -tol and right > tol and u[i] > tol and i < n - 1:
            idx.append(i)
    # remove plateau duplicates
    out = []
    for i in idx:
        if not out or i - out[-1] > 1:
            out.append(i)
    return out


def random_profile(ec: Econ, rng: np.random.Generator) -> Profile:
    """A random pure or two-atom profile with a random half-line and optional island pool."""
    def atoms(sign: float) -> tuple[tuple[float, float], ...]:
        if rng.random() < 0.5:
            return ((float(sign * rng.choice([0.0, 0.25, 0.5, 0.75, 1.0, rng.random()])), 1.0),)
        a, b = sorted(rng.random(2))
        lam = float(rng.choice([0.2, 0.5, 0.8]))
        return ((float(sign * a), 1.0 - lam), (float(sign * b), lam))
    H, L = atoms(+1.0), atoms(-1.0)
    pool: list[tuple[float, float]] = []
    if rng.random() < 0.8:
        pool.append((-math.inf, float(rng.uniform(-1.0, 2.5))))
    if rng.random() < 0.3:
        y1 = float(rng.uniform(0.0, 4.0))
        pool.append((y1, y1 + float(rng.choice([0.3, 0.7, 1.5, math.inf]))))
    return Profile(H=H, L=L, pool=tuple(pool))


def audit(ec: Econ, n: int = 3000, seed: int = 0) -> dict:
    """Count local maxima of U_H and U_L over random consistent schedules."""
    rng = np.random.default_rng(seed)
    done = 0
    tried = 0
    multiH = multiL = 0
    gapH = gapL = math.inf
    interiorH = 0       # schedules where the global best response of H is below 1
    maxH_any = maxL_any = 0
    while done < n and tried < 20 * n:
        tried += 1
        prof = random_profile(ec, rng)
        sch = build_schedule(ec, prof)
        if not sch.consistent:
            continue
        done += 1
        uH = payoff(sch, 0, QGRID_H)
        uL = payoff(sch, 1, QGRID_L)
        mH = local_maxima(uH)
        mL = local_maxima(uL)
        maxH_any = max(maxH_any, len(mH))
        maxL_any = max(maxL_any, len(mL))
        if len(mH) >= 2:
            multiH += 1
            top = sorted((uH[i] for i in mH), reverse=True)
            gapH = min(gapH, float(top[0] - top[1]))
        if len(mL) >= 2:
            multiL += 1
            top = sorted((uL[i] for i in mL), reverse=True)
            gapL = min(gapL, float(top[0] - top[1]))
        if uH.max() > 1e-12 and QGRID_H[int(uH.argmax())] < 1.0 - 1e-9:
            interiorH += 1
    return {"sampled": done, "multi_peak_H": multiH, "multi_peak_L": multiL, "min_peak_gap_H": gapH,
            "min_peak_gap_L": gapL, "H_interior_best": interiorH, "max_peaks_H": maxH_any, "max_peaks_L": maxL_any}


def mixed_search(ec: Econ, pool: tuple[tuple[float, float], ...], who: str, lattice: int = 11) -> list[dict]:
    """Two-atom mixtures for one type (who = 'L' or 'H'); the other type is pure on a lattice.

    For every pair of support points the weight is chosen by root finding so the two payoffs are equal.
    A candidate is kept when both types' regrets are below 1e-7 (lattice supports, so ties are approximate).
    """
    qs_pure_H = np.linspace(0.0, 1.0, lattice)
    qs_pure_L = np.linspace(-1.0, 0.0, lattice)
    out: list[dict] = []
    mix_pts = qs_pure_L if who == "L" else qs_pure_H
    other_pts = qs_pure_H if who == "L" else qs_pure_L
    sgn = 1 if who == "H" else -1
    for i, a in enumerate(mix_pts):
        for b in mix_pts[i + 1:]:
            for o in other_pts:
                def prof_for(lam: float) -> Profile:
                    mix = ((float(a), 1.0 - lam), (float(b), lam))
                    if who == "L":
                        return Profile(H=((float(o), 1.0),), L=mix, pool=pool)
                    return Profile(H=mix, L=((float(o), 1.0),), pool=pool)
                theta = 1 if who == "L" else 0

                def gap(lam: float) -> float:
                    sch = build_schedule(ec, prof_for(lam))
                    return float(payoff(sch, theta, a)[0] - payoff(sch, theta, b)[0])
                lams = np.linspace(0.02, 0.98, 13)
                vals = [gap(float(l)) for l in lams]
                for j in range(len(lams) - 1):
                    if vals[j] * vals[j + 1] < 0.0:
                        lam = brentq(gap, float(lams[j]), float(lams[j + 1]), xtol=1e-12)
                        sch = build_schedule(ec, prof_for(lam))
                        if not sch.consistent:
                            continue
                        _, uH = best_response(sch, 0)
                        _, uL = best_response(sch, 1)
                        if who == "L":
                            regL = max(0.0, uL - float(payoff(sch, 1, a)[0]))
                            regH = max(0.0, uH - float(payoff(sch, 0, o)[0]))
                        else:
                            regH = max(0.0, uH - float(payoff(sch, 0, a)[0]))
                            regL = max(0.0, uL - float(payoff(sch, 1, o)[0]))
                        if regH <= 1e-7 and regL <= 1e-7:
                            oc = outcome(sch)
                            out.append({"who": who, "a": float(a), "b": float(b), "other": float(o), "lam": lam,
                                        "E": oc.E, "O_H": oc.O_H, "regH": regH, "regL": regL})
    return out


def bridge_mixture(ec: Econ, cutoff: float | None, a: tuple[float, float], b: tuple[float, float]) -> dict | None:
    """Mixed profile that connects two pure equilibria at the same pool by mixing the L order.

    a = (qH, qL_a) and b = (qH, qL_b) are pure equilibria with the same H order. With weight lam on qL_b, the L
    type is indifferent between qL_a and qL_b at lam*, the root of U_L(qL_a) - U_L(qL_b). Complementarity makes
    the difference change sign between the two pure equilibria, so a root exists when both are equilibria.
    The mixed profile is accepted only when the pool is consistent and both types' global best responses are
    attained at the support (regret below 1e-9).
    """
    pool = () if cutoff is None or cutoff == -math.inf else ((-math.inf, float(cutoff)),)
    qH = a[0]

    def prof(lam: float) -> Profile:
        return Profile(H=((qH, 1.0),), L=((a[1], 1.0 - lam), (b[1], lam)), pool=pool)

    def gap(lam: float) -> float:
        sch = build_schedule(ec, prof(lam))
        return float(payoff(sch, 1, a[1])[0] - payoff(sch, 1, b[1])[0])

    lams = np.linspace(0.0, 1.0, 41)
    vals = [gap(float(x)) for x in lams]
    roots = []
    for i in range(len(lams) - 1):
        if vals[i] * vals[i + 1] < 0.0:
            roots.append(brentq(gap, float(lams[i]), float(lams[i + 1]), xtol=1e-13))
    out = None
    for lam in roots:
        sch = build_schedule(ec, prof(lam))
        if not sch.consistent:
            continue
        _, uH = best_response(sch, 0)
        _, uL = best_response(sch, 1)
        regH = max(0.0, uH - float(payoff(sch, 0, qH)[0]))
        regL = max(0.0, uL - float(payoff(sch, 1, a[1])[0]), uL - float(payoff(sch, 1, b[1])[0]))
        if regH <= 1e-9 and regL <= 1e-9:
            oc = outcome(sch)
            cand = {"lam": lam, "qH": qH, "qL_a": a[1], "qL_b": b[1], "E": oc.E, "O_H": oc.O_H, "eH": oc.eH,
                    "pool_prob": oc.pool_prob, "pool_belief": oc.pool_belief, "regH": regH, "regL": regL}
            if out is None or cand["E"] < out["E"]:
                out = cand
    return out
