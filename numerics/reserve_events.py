"""Exact reserve events, regime classification, and admissible-bid outcome measures (spec S2 section 9; OA A.10, C.6).

Events are declared by their defining relation and evaluated algebraically at 50 decimal digits; the
tie convention (entry at indifference; a bid equal to the reserve is admissible) is applied to the
declared identity, never to a rounded floating-point comparison. Nodes that are not declared events
have their inequalities evaluated in high precision with an explicit unresolved outcome when the
sign cannot be established.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from decimal import Decimal
from fractions import Fraction

import mpmath as mp
import numpy as np
from scipy import integrate

from .auction import AuctionPayoffs
from .continuations import NA, payoff_regime, payoffs_exact
from .params import Primitives

DPS = 50
SIGN_RESOLUTION = mp.mpf("1e-40")   # an inequality closer to zero than this at 50 digits is reported unresolved
OFFSETS = ("0.0001", "0.000001", "0.00000001")


@dataclass(frozen=True)
class EventNode:
    law: str                       # binary | uniform_classes
    r: str                         # exact strength declaration
    p_exact: str                   # exact decimal, or the event tag for an irrational event
    p_decimal: str                 # 30-digit decimal (reference only; never used for a tie decision)
    event_id: str                  # e.g. floor_equality_p_L, ceiling_equality_p_H, reserve_equals_ell, grid, offset:...
    event_defining_relation: str
    applicable: bool               # event lies in the regime that defines it
    note: str = ""
    tie_at_floor: bool = False
    tie_at_ceiling: bool = False
    is_exact_event: bool = False

    @property
    def p_float(self) -> float:
        return float(mp.mpf(self.p_decimal))

    @property
    def p_mp(self):
        with mp.workdps(DPS):
            return mp.mpf(self.p_decimal) if not self.is_exact_event else event_value_mp(self)


def _dec30(x) -> str:
    with mp.workdps(DPS):
        return mp.nstr(mp.mpf(x), 32, strip_zeros=False)


def posterior_bounds_mp(b):
    m = 1 / (1 + mp.exp(2 / b))
    return m, 1 - m


def event_value_mp(node: EventNode):
    """Recompute an exact event value from its defining relation (not from the stored decimal)."""
    with mp.workdps(DPS):
        h, ell, cL, cH, b = (mp.mpf(s) for s in node.p_exact.split("|")[1].split(","))
        r = mp.mpf(node.r)
        m, M = posterior_bounds_mp(b)
        tag = node.p_exact.split("|")[0]
        if tag == "p_L=h-c_L/m":
            return h - cL / m
        if tag == "p_H=sqrt(2r(h-c_H/M)-r^2)":
            return mp.sqrt(2 * r * (h - cH / M) - r * r)
        raise ValueError(f"unknown event tag {tag}")


def exact_events(prim: Primitives, law: str, r: str, eps_V: str) -> list[EventNode]:
    """The two exact events p_L (low-cost floor equality) and p_H (expensive-entry ceiling equality)."""
    with mp.workdps(DPS):
        h, ell, cL, cH, b = (mp.mpf(prim.h), mp.mpf(prim.ell), mp.mpf(prim.c_L), mp.mpf(prim.c_H), mp.mpf(prim.b))
        rr, eV = mp.mpf(r), mp.mpf(eps_V) if law == "uniform_classes" else mp.mpf(0)
        m, M = posterior_bounds_mp(b)
        params = f"{prim.h},{prim.ell},{prim.c_L},{prim.c_H},{prim.b}"
        pL = h - cL / m
        pH = mp.sqrt(2 * rr * (h - cH / M) - rr * rr) if 2 * rr * (h - cH / M) - rr * rr > 0 else mp.mpf("nan")
        # p_L is defined where the low class is entirely excluded, the incumbent is excluded (p >= r), and the high
        # class lies entirely above the reserve: then g_H = h - p (class mean) and B(m) = m (h - p).
        pL_ok = (pL > ell + eV) and (pL >= rr) and (pL < h - eV)
        # p_H is defined for ell < p < r with the low class excluded and the high class above the incumbent support.
        pH_ok = (not mp.isnan(pH)) and (ell + eV < pH < rr) and (h - eV > rr)
        out = [EventNode(law, r, f"p_L=h-c_L/m|{params}", _dec30(pL), "floor_equality_p_L",
                         "B_r(m) = c_L with g_H = h - p, g_L = 0 (low-cost floor equality; entry admitted by the tie rule)",
                         bool(pL_ok), "" if pL_ok else "event outside its defining regime at this strength",
                         tie_at_floor=True, is_exact_event=True)]
        if not mp.isnan(pH):
            out.append(EventNode(law, r, f"p_H=sqrt(2r(h-c_H/M)-r^2)|{params}", _dec30(pH), "ceiling_equality_p_H",
                                 "M (h - r/2 - p^2/(2r)) = c_H (expensive-entry ceiling equality; tau = M, x* = 1)",
                                 bool(pH_ok), "" if pH_ok else "event outside its defining regime (requires ell < p_H < r)",
                                 tie_at_ceiling=True, is_exact_event=True))
        return out


def event_grid(prim: Primitives, law: str, r: str, eps_V: str, declared: list[str], offsets: tuple[str, ...] = OFFSETS) -> list[EventNode]:
    """Support/participation events with one-sided offsets on both sides (where feasible in [0, top])."""
    top = Decimal(prim.h) + (Decimal(eps_V) if law == "uniform_classes" else Decimal(0))
    base: list[EventNode] = []

    def dec_node(val: Decimal, eid: str, rel: str) -> EventNode:
        s = format(val.normalize(), "f") if val != val.to_integral() else str(val.quantize(Decimal(1)))
        return EventNode(law, r, s, _dec30(s), eid, rel, True)

    ell, h, rd, eV = Decimal(prim.ell), Decimal(prim.h), Decimal(r), Decimal(eps_V)
    base.append(dec_node(Decimal(0), "reserve_zero", "p = 0"))
    base.append(dec_node(ell, "reserve_equals_ell", "p = ell (low value bids at the reserve; tie rule admits the bid)"))
    base.append(dec_node(rd, "reserve_equals_r", "p = r (incumbent support top)"))
    base.append(dec_node(h, "reserve_equals_h", "p = h (high value bids at the reserve with zero rent)"))
    if law == "uniform_classes":
        base.append(dec_node(ell - eV, "reserve_equals_ell_minus_epsV", "p = ell - eps_V (bottom of the low band)"))
        base.append(dec_node(ell + eV, "reserve_equals_ell_plus_epsV", "p = ell + eps_V (top of the low band)"))
        base.append(dec_node(h - eV, "reserve_equals_h_minus_epsV", "p = h - eps_V (bottom of the high band)"))
        base.append(dec_node(h + eV, "reserve_equals_h_plus_epsV", "p = h + eps_V (top of the high band)"))
    for d in declared:
        base.append(dec_node(Decimal(d), f"declared_reserve_{d}", "declared reserve alternative (C.0)"))
    base.extend(exact_events(prim, law, r, eps_V))
    nodes: list[EventNode] = []
    seen: set[str] = set()
    for n in base:
        if n.p_decimal in seen:
            continue
        seen.add(n.p_decimal)
        nodes.append(n)
        with mp.workdps(DPS):
            pv = n.p_mp
            for off in offsets:
                for sgn in (-1, 1):
                    x = pv + sgn * mp.mpf(off)
                    if x < 0 or x > mp.mpf(str(top)):
                        continue
                    if n.is_exact_event:
                        pe = f"{n.p_exact}{'+' if sgn > 0 else '-'}{off}"
                    else:
                        xd = Decimal(n.p_exact) + sgn * Decimal(off)
                        pe = format(xd.normalize(), "f")
                    off_node = EventNode(law, r, pe, _dec30(x), f"offset:{n.event_id}{'+' if sgn > 0 else '-'}{off}",
                                         f"{n.event_id} {'+' if sgn > 0 else '-'} {off} (regime classification on one side)", True)
                    if off_node.p_decimal not in seen:
                        seen.add(off_node.p_decimal)
                        nodes.append(off_node)
    nodes.sort(key=lambda n: mp.mpf(n.p_decimal))
    return nodes


# ---------------------------------------------------------------------------------------------
# high-precision regime and margin classification at a node
# ---------------------------------------------------------------------------------------------
def _sign_relation(value, is_equality_event: bool) -> str:
    if is_equality_event:
        return "equality_event"
    if value > SIGN_RESOLUTION:
        return "strict_positive"
    if value < -SIGN_RESOLUTION:
        return "strict_negative"
    return "unresolved"


def classify_node(prim: Primitives, node: EventNode, eps_V: str) -> dict:
    """Regime, exact payoffs (binary values; class values where the event formulas apply), floor and ceiling relations."""
    with mp.workdps(DPS):
        h, ell, cL, cH, b, rho, k = (mp.mpf(prim.h), mp.mpf(prim.ell), mp.mpf(prim.c_L), mp.mpf(prim.c_H), mp.mpf(prim.b),
                                     mp.mpf(prim.rho), mp.mpf(prim.k))
        r = mp.mpf(node.r)
        p = node.p_mp
        m, M = posterior_bounds_mp(b)
        eV = mp.mpf(eps_V) if node.law == "uniform_classes" else mp.mpf(0)
        band = band_status(h, ell, eV, r, p)
        ex = payoffs_exact(prim, r, p)
        if node.law == "uniform_classes":
            ex = class_payoffs_mp(h, ell, eV, r, p)
        B_m = ex["g_L"] + m * (ex["g_H"] - ex["g_L"])
        B_M = ex["g_L"] + M * (ex["g_H"] - ex["g_L"])
        B_half = ex["g_L"] + (ex["g_H"] - ex["g_L"]) / 2
        floor = _sign_relation(B_m - cL, node.event_id == "floor_equality_p_L" and node.applicable)
        ceiling = _sign_relation(B_M - cH, node.event_id == "ceiling_equality_p_H" and node.applicable)
        prior_excl = _sign_relation(cH - B_half, False)
        Delta = ex["Delta_T"]
        e_m = rho if floor in ("strict_positive", "equality_event") else mp.mpf(0)
        full_bound = (1 - 1 / b) * e_m * m * Delta - k
        return {"regime": ex["regime"], "band_status": band, "t_0": ex["t_0"], "t_H": ex["t_H"], "t_L": ex["t_L"], "g_H": ex["g_H"],
                "g_L": ex["g_L"], "Delta_T": Delta, "B_m": B_m, "B_M": B_M, "B_half": B_half, "m": m, "M": M,
                "low_cost_floor_relation": floor, "low_cost_floor_margin": B_m - cL, "ceiling_relation": ceiling,
                "ceiling_margin": B_M - cH, "prior_exclusion_relation": prior_excl, "no_trade_unique_margin": k - Delta,
                "full_unique_margin": full_bound, "full_unique_relation": _sign_relation(full_bound, False),
                "pooling_exists_margin": k - (rho if B_half >= cL else mp.mpf(0)) * Delta / 2}


def band_status(h, ell, eV, r, p) -> str:
    if eV == 0:
        return "binary values (no bands)"
    low_excluded = p > ell + eV
    low_included = p <= ell - eV
    high_above = (h - eV > p) and (h - eV >= r)
    if low_excluded and high_above:
        return "low band entirely excluded; high band entirely above reserve and incumbent support (event formulas apply)"
    if low_included and high_above:
        return "low band entirely included; high band entirely above reserve and incumbent support"
    if ell - eV < p <= ell + eV:
        return "reserve inside the low band (integrate the value distribution; event formulas do not apply)"
    if h - eV < p <= h + eV:
        return "reserve inside the high band (integrate the value distribution; event formulas do not apply)"
    if p > h + eV:
        return "reserve above the high band (no sale)"
    return "high band not entirely above the incumbent support (integrate)"


def class_payoffs_mp(h, ell, eV, r, p) -> dict:
    """Class-averaged OA.51 kernel by exact piecewise integration in mp arithmetic (any reserve, including inside a band)."""
    t_0 = p * (1 - p / r) if p <= r else mp.mpf(0)

    def avg(center):
        lo, hi = center - eV, center + eV
        pts = sorted({lo, hi, *[x for x in (p, r) if lo < x < hi]})
        tot_t, tot_g = mp.mpf(0), mp.mpf(0)
        for a, b_ in zip(pts[:-1], pts[1:]):
            mid = (a + b_) / 2
            if mid < p:
                tot_t += t_0 * (b_ - a)
            elif mid < r:
                I1 = (b_ ** 2 - a ** 2) / 2
                I2 = (b_ ** 3 - a ** 3) / 3
                tot_t += I1 - (I2 - p * p * (b_ - a)) / (2 * r)
                tot_g += (I2 - p * p * (b_ - a)) / (2 * r)
            elif p <= r:
                t_v = r / 2 + p * p / (2 * r)
                tot_t += t_v * (b_ - a)
                tot_g += (b_ ** 2 - a ** 2) / 2 - t_v * (b_ - a)
            else:
                tot_t += p * (b_ - a)
                tot_g += (b_ ** 2 - a ** 2) / 2 - p * (b_ - a)
        return tot_t / (hi - lo), tot_g / (hi - lo)

    t_H, g_H = avg(h)
    t_L, g_L = avg(ell)
    return {"t_0": t_0, "t_H": t_H, "t_L": t_L, "g_H": g_H, "g_L": g_L, "Delta_T": t_H - t_L,
            "regime": payoff_regime(ell, h, r, p) + " [class bands: " + band_status(h, ell, eV, r, p) + "]"}


def full_order_objects_mp(prim: Primitives, cls: dict, tie_at_ceiling: bool, tie_at_floor: bool) -> dict:
    """Laplace full-order closed forms (eq. 14) in mp arithmetic with the tie rule applied symbolically."""
    with mp.workdps(DPS):
        b, rho, cH = mp.mpf(prim.b), mp.mpf(prim.rho), mp.mpf(prim.c_H)
        m, M = cls["m"], cls["M"]
        gH, gL = cls["g_H"], cls["g_L"]
        if gH == gL:
            tau = mp.inf if cH > gL else -mp.inf
        else:
            tau = (cH - gL) / (gH - gL)
        if tie_at_ceiling:
            x_star, aH, aL = mp.mpf(1), mp.mpf(1) / 2, mp.exp(-2 / b) / 2
        elif tau <= m:
            x_star, aH, aL = -mp.inf, mp.mpf(1), mp.mpf(1)
        elif tau > M:
            x_star, aH, aL = mp.inf, mp.mpf(0), mp.mpf(0)
        else:
            x_star = b / 2 * mp.log(tau / (1 - tau))
            aH = 1 - mp.exp((x_star - 1) / b) / 2 if x_star < 1 else mp.exp(-(x_star - 1) / b) / 2
            aL = mp.exp(-(x_star + 1) / b) / 2 if x_star > -1 else 1 - mp.exp((x_star + 1) / b) / 2
        low_enters = cls["low_cost_floor_relation"] in ("strict_positive", "equality_event") or tie_at_floor
        base = rho if low_enters else mp.mpf(0)
        e_H = base + (1 - rho) * aH
        e_L = base + (1 - rho) * aL
        E = (e_H + e_L) / 2
        R_T = cls["t_0"] + (e_H * (cls["t_H"] - cls["t_0"]) + e_L * (cls["t_L"] - cls["t_0"])) / 2
        return {"tau": tau, "x_star": x_star, "alpha_H": aH, "alpha_L": aL, "e_H": e_H, "e_L": e_L, "E": E, "R_T": R_T,
                "low_cost_enters_everywhere": low_enters}


# ---------------------------------------------------------------------------------------------
# outcome measures from the actual allocation event (spec 9.5)
# ---------------------------------------------------------------------------------------------
def _band_tail(center: float, eps_V: float, p: float) -> float:
    """Pr(V >= p | class) for V uniform on [center - eps_V, center + eps_V] (atom at center when eps_V = 0)."""
    if eps_V == 0:
        return float(center >= p)
    lo, hi = center - eps_V, center + eps_V
    return float(np.clip((hi - p) / (hi - lo), 0.0, 1.0))


def _band_win(center: float, eps_V: float, p: float, r: float) -> float:
    """E[1{V >= p} Pr(R < V)] for the class band: the challenger wins when admissible and the incumbent is below it."""
    if eps_V == 0:
        return float(center >= p) * min(center / r, 1.0)
    lo, hi = center - eps_V, center + eps_V
    a = max(lo, p)
    if a >= hi:
        return 0.0
    val, _ = integrate.quad(lambda v: min(v / r, 1.0), a, hi, points=[r] if a < r < hi else None, epsabs=1e-13, epsrel=1e-13, limit=200)
    return val / (hi - lo)


def outcome_measures(prim: Primitives, law: str, eps_V: str, r: float, p: float, e_H: float, e_L: float, pi: float = 0.5) -> dict:
    """E, A, S, C2, O_H with S also computed by direct integration of the union event (identity check)."""
    h, ell = prim.fh, prim.fell
    eV = float(Decimal(eps_V)) if law == "uniform_classes" else 0.0
    admit_H, admit_L = _band_tail(h, eV, p), _band_tail(ell, eV, p)
    E = pi * e_H + (1 - pi) * e_L
    A = pi * e_H * admit_H + (1 - pi) * e_L * admit_L
    pr_R = max(0.0, 1.0 - p / r) if p <= r else 0.0
    C2 = pr_R * A
    S = pr_R + A - C2
    O_H = pi * e_H * _band_win(h, eV, p, r)
    # direct union-event integration over R ~ U[0, r] and each class law: Pr(R >= p or [I = 1, V >= p])
    def union(center: float, e: float) -> float:
        if eV == 0:
            inner = lambda R: float(R >= p or (center >= p)) * e + float(R >= p) * (1 - e)
        else:
            lo, hi = center - eV, center + eV
            tail = lambda R: (float(R >= p) if R >= p else 0.0)
            inner = lambda R: e * (1.0 if R >= p else _band_tail(center, eV, p)) + (1 - e) * float(R >= p)
        pts = sorted({0.0, r, *[x for x in (p,) if 0 < x < r]})
        tot = 0.0
        for a, b_ in zip(pts[:-1], pts[1:]):
            v, _ = integrate.quad(inner, a, b_, epsabs=1e-13, epsrel=1e-13, limit=200)
            tot += v
        return tot / r
    S_direct = pi * union(h, e_H) + (1 - pi) * union(ell, e_L)
    bounds_ok = (0 <= C2 <= A + 1e-15) and (A <= E + 1e-15) and (E <= 1 + 1e-15) and (0 <= S <= 1 + 1e-15)
    return {"E": E, "A": A, "S": S, "C2": C2, "O_H": O_H, "Pr_R_ge_p": pr_R, "S_direct": S_direct,
            "S_identity_error": abs(S_direct - S), "bounds_ok": bounds_ok}
