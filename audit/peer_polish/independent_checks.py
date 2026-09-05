#!/usr/bin/env python3
"""Independent reproduction of the core numbers (spec S1-B, S1-C; tests T02-T15).

This script is deliberately self-contained: it parses the input declarations from the
online appendix text (section C.0), implements every formula from the paper on its own
(mpmath closed forms, scipy/mpmath quadrature), and only reads the repository's CSV files
to compare against them. It never imports numerics.search or numerics.validation.

Acceptance uses explicit exceptions (CheckFailure) recorded per check; a failed check does
not stop the run, but the exit code is nonzero if any required check fails.

Outputs:
  audit/peer_polish/independent_checks.json
  audit/peer_polish/logs/s1_independent_checks.md
"""
from __future__ import annotations

import csv
import json
import math
import os
import re
import sys
import time
import warnings
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, asdict
from decimal import Decimal, getcontext
from pathlib import Path

import mpmath as mp
import numpy as np
from scipy import integrate, optimize

warnings.simplefilter("error", integrate.IntegrationWarning)  # never suppress: a warning is a failure
getcontext().prec = 60
mp.mp.dps = 40

ROOT = Path(__file__).resolve().parents[2]
OUT_JSON = ROOT / "audit/peer_polish/independent_checks.json"
OUT_MD = ROOT / "audit/peer_polish/logs/s1_independent_checks.md"

# ---------------------------------------------------------------------------------------
# numerical controls (C.0), tightened for the ordinary-quadrature refinement (S1-C)
# ---------------------------------------------------------------------------------------
TOL_FORMULA = 1e-9      # independent formula / oracle agreement
TOL_PROB = 1e-8         # probability and posterior identities
TOL_PRICE = 1e-8        # conditional price identity
TOL_ENTRY = 1e-8        # buyer preparation deviation gain
TOL_DEV = 1e-7          # ordinary numerical investor deviation gain
QUAD_ABS = 1e-12        # C.0 target 1e-11 tightened by ten
QUAD_REL = 1e-12
ORDER_INTERVALS = 800   # C.0 initial 400 doubled
DISPLAY_TOL = 5e-11     # landmark agreement (10 printed decimals)

LANDMARKS = {
    "strong_preparation": ("0.5227572973", "base/Laplace/atoms r=3 feedback full E"),
    "strong_high_value_ownership": ("0.3241924258", "base/Laplace/atoms r=3 feedback full O_H"),
    "strong_target_proceeds": ("0.8723920451", "base/Laplace/atoms r=3 feedback full R_T"),
    "frozen_prep_weak": ("0.5621780582", "base/Laplace/atoms r=1.2 frozen full E"),
    "strong_hidden_proceeds": ("0.6145833333", "base/Laplace/atoms r=3 price_hidden R_T"),
    "net_surplus_gain": ("0.0802175348", "base/Laplace/atoms r=3 W_feedback - W_hidden"),
    "logistic_strong_prep": ("0.3015088516", "base/logistic/atoms r=3 feedback full E"),
    "atomless_laplace_strong_prep": ("0.5227147164", "base/Laplace/uniform_mixture r=3 feedback full E"),
    "atomless_logistic_strong_prep": ("0.3013741277", "base/logistic/uniform_mixture r=3 feedback full E"),
    "moderate_strong_prep": ("0.5268046622", "moderate r=1.5 feedback full E"),
    "complementary_strong_prep": ("0.8794375516", "signal a=0.70 d=0.75 r=2.3 full E"),
}


class CheckFailure(Exception):
    pass


# ---------------------------------------------------------------------------------------
# results ledger
# ---------------------------------------------------------------------------------------
class Ledger:
    def __init__(self) -> None:
        self.rows: list[dict] = []
        self.t0 = time.time()

    def add(self, test: str, name: str, independent, repo=None, tol=None, *, passed: bool | None = None,
            status: str | None = None, budget: dict | None = None, note: str = "", required: bool = True):
        ind = _num(independent)
        rp = _num(repo)
        diff = abs(ind - rp) if (ind is not None and rp is not None and math.isfinite(ind) and math.isfinite(rp)) else None
        if passed is None:
            if diff is not None and tol is not None:
                passed = diff <= tol
            elif ind is not None and rp is not None and tol is not None:
                passed = (ind == rp)  # inf == inf etc.
            else:
                passed = True
        if status is None:
            status = "pass" if passed else "FAIL"
        row = {"test": test, "quantity": name, "independent": _ser(independent), "repo": _ser(repo),
               "abs_diff": diff, "tolerance": tol, "status": status, "error_budget": budget or {}, "note": note,
               "required": required}
        self.rows.append(row)
        return passed

    def require(self, test: str, name: str, cond: bool, note: str = "", **kw):
        try:
            if not cond:
                raise CheckFailure(f"{test} {name}: {note}")
            self.add(test, name, True, passed=True, note=note, **kw)
        except CheckFailure as ex:
            self.add(test, name, False, passed=False, note=str(ex), **kw)
        return cond


def _num(x):
    if x is None:
        return None
    if isinstance(x, bool):
        return float(x)
    if isinstance(x, (int, float)):
        return float(x)
    if isinstance(x, (mp.mpf, Decimal)):
        return float(x)
    if isinstance(x, str):
        try:
            return float(x)
        except ValueError:
            return None
    return None


def _ser(x):
    if isinstance(x, (mp.mpf,)):
        return mp.nstr(x, 25)
    if isinstance(x, Decimal):
        return str(x)
    if isinstance(x, (np.floating,)):
        return float(x)
    if isinstance(x, (np.bool_,)):
        return bool(x)
    return x


# ---------------------------------------------------------------------------------------
# C.0 declarations parsed from the appendix text
# ---------------------------------------------------------------------------------------
def parse_declarations(text: str) -> dict[str, dict[str, str]]:
    blocks = re.findall(r"\*\*Input declaration: ([^*]+?)\.\*\*\s*```text\n(.*?)```", text, re.S)
    out = {}
    for name, body in blocks:
        d = {}
        for stmt in re.split(r"[;\n]", body):
            stmt = stmt.strip()
            if stmt.endswith("."):
                stmt = stmt[:-1]
            if "=" in stmt:
                k, v = stmt.split("=", 1)
                d[k.strip()] = v.strip()
        out[name] = d
    return out


APPX = (ROOT / "paper/online_appendix.md").read_text()
DECL = parse_declarations(APPX)
for req in ("benchmark", "moderate acquisition values", "complementary signals", "numerical controls"):
    if req not in DECL:
        raise CheckFailure(f"C.0 declaration block missing: {req}")
NC = DECL["numerical controls"]
if float(NC["quadrature_absolute_target"]) != 1e-11 or int(NC["initial_order_intervals"]) != 400 \
        or int(NC["refined_order_intervals"]) != 800 or float(NC["deviation_gain_acceptance"]) != 1e-7:
    raise CheckFailure("numerical controls in C.0 differ from the values hard-wired above; refusing to proceed")


@dataclass(frozen=True)
class Econ:
    """Exact-decimal primitives; every field is the declared string."""
    h: str
    ell: str
    p: str
    rho: str
    c_L: str
    c_H: str
    b: str
    k: str
    noise: str = "Laplace"       # Laplace | logistic
    cost: str = "atoms"          # atoms | uniform_mixture
    eps_C: str = "0"
    tag: str = "base"

    def M(self, name: str) -> mp.mpf:
        return mp.mpf(getattr(self, name))

    def F(self, name: str) -> float:
        return float(Decimal(getattr(self, name)))


def econ_from(decl: dict, tag: str, **kw) -> Econ:
    return Econ(decl["h"], decl["ell"], decl["p"], decl["rho"], decl["c_L"], decl["c_H"], decl["b"], decl["k"], tag=tag, **kw)


BENCH = DECL["benchmark"]
MODER = DECL["moderate acquisition values"]
SIGN = DECL["complementary signals"]
E_BASE = econ_from(BENCH, "base")
E_MOD = econ_from(MODER, "moderate")
E_SIG = econ_from(SIGN, "signal")
ECONOMIES = [
    E_BASE,
    Econ(**{**asdict(E_BASE), "cost": "uniform_mixture", "eps_C": BENCH["cost_halfwidth"]}),
    Econ(**{**asdict(E_BASE), "noise": "logistic"}),
    Econ(**{**asdict(E_BASE), "noise": "logistic", "cost": "uniform_mixture", "eps_C": BENCH["cost_halfwidth"]}),
]


# ---------------------------------------------------------------------------------------
# auction layer (OA.5, OA.50, OA.51, OA.52) -- mpmath closed forms and direct integration
# ---------------------------------------------------------------------------------------
def kernel(r, v, p):
    """(t_v, g_v) for uniform R on [0,r] and fixed challenger value v (OA.51), all mpf."""
    t_0 = p * (1 - p / r) if p <= r else mp.mpf(0)
    if v < p:
        return t_0, mp.mpf(0)
    if v < r:
        return v - (v * v - p * p) / (2 * r), (v * v - p * p) / (2 * r)
    if p <= r <= v:
        t_v = r / 2 + p * p / (2 * r)
        return t_v, v - t_v
    return p, v - p  # r < p <= v


@dataclass(frozen=True)
class Pay:
    r: mp.mpf
    p: mp.mpf
    t_0: mp.mpf
    t_H: mp.mpf
    t_L: mp.mpf
    g_H: mp.mpf
    g_L: mp.mpf

    @property
    def Delta(self):
        return self.t_H - self.t_L

    @property
    def w_H(self):
        return self.t_H - self.t_0

    @property
    def w_L(self):
        return self.t_L - self.t_0

    def B(self, mu):
        return self.g_L + mu * (self.g_H - self.g_L)

    def tau(self, c):
        if self.g_H == self.g_L:
            return mp.inf if c > self.g_L else -mp.inf
        return (c - self.g_L) / (self.g_H - self.g_L)

    def floats(self) -> dict:
        return {k: float(v) for k, v in dict(r=self.r, p=self.p, t_0=self.t_0, t_H=self.t_H, t_L=self.t_L, g_H=self.g_H,
                                            g_L=self.g_L, Delta=self.Delta, w_H=self.w_H, w_L=self.w_L).items()}


def pay_binary(e: Econ, r: str | mp.mpf, p: str | mp.mpf | None = None) -> Pay:
    r = mp.mpf(r)
    p = e.M("p") if p is None else mp.mpf(p)
    t_0 = p * (1 - p / r) if p <= r else mp.mpf(0)
    tH, gH = kernel(r, e.M("h"), p)
    tL, gL = kernel(r, e.M("ell"), p)
    return Pay(r, p, t_0, tH, tL, gH, gL)


def pay_benchmark_formula(e: Econ, r) -> Pay:
    """Main-text closed forms for p < ell < r < h."""
    r = mp.mpf(r)
    p, ell, h = e.M("p"), e.M("ell"), e.M("h")
    return Pay(r, p, p * (1 - p / r), r / 2 + p * p / (2 * r), ell - (ell * ell - p * p) / (2 * r),
               h - r / 2 - p * p / (2 * r), (ell * ell - p * p) / (2 * r))


def T_real(R, v, p):
    if v < p:
        return p if R >= p else mp.mpf(0)
    return max(p, min(R, v))


def G_real(R, v, p):
    return max(v - max(p, R), mp.mpf(0))


def integrate_uniform(fun, r, splits, dps: int = 30):
    """(1/r) int_0^r fun(R) dR with mpmath Gauss-Legendre on the split segments."""
    pts = sorted({mp.mpf(0), r, *[s for s in splits if 0 < s < r]})
    with mp.workdps(dps):
        tot = mp.mpf(0)
        for a, c in zip(pts[:-1], pts[1:]):
            tot += mp.quad(fun, [a, c])
    return tot / r


def pay_integrated(e: Econ, r, p=None) -> Pay:
    r = mp.mpf(r)
    p = e.M("p") if p is None else mp.mpf(p)
    h, ell = e.M("h"), e.M("ell")
    splits = [p, ell, h]
    t_0 = integrate_uniform(lambda R: (p if R >= p else mp.mpf(0)), r, splits)
    tH = integrate_uniform(lambda R: T_real(R, h, p), r, splits)
    tL = integrate_uniform(lambda R: T_real(R, ell, p), r, splits)
    gH = integrate_uniform(lambda R: G_real(R, h, p), r, splits)
    gL = integrate_uniform(lambda R: G_real(R, ell, p), r, splits)
    return Pay(r, p, t_0, tH, tL, gH, gL)


def pay_class(e: Econ, r, p, eps_V, integrate_direct: bool) -> Pay:
    """Atomless-value class economy: average the kernel (or the direct integral) over each band."""
    r, p, eps_V = mp.mpf(r), mp.mpf(p), mp.mpf(eps_V)
    h, ell = e.M("h"), e.M("ell")
    t_0 = p * (1 - p / r) if p <= r else mp.mpf(0)

    def band(center, which):
        lo, hi = center - eps_V, center + eps_V
        pts = sorted({lo, hi, *[x for x in (p, r) if lo < x < hi]})
        tot = mp.mpf(0)
        for a, c in zip(pts[:-1], pts[1:]):
            if integrate_direct:
                f = (lambda v: integrate_uniform(lambda R: T_real(R, v, p), r, [p, v], 20)) if which == "t" else \
                    (lambda v: integrate_uniform(lambda R: G_real(R, v, p), r, [p, v], 20))
            else:
                f = (lambda v: kernel(r, v, p)[0]) if which == "t" else (lambda v: kernel(r, v, p)[1])
            with mp.workdps(30):
                tot += mp.quad(f, [a, c])
        return tot / (hi - lo)

    return Pay(r, p, t_0, band(h, "t"), band(ell, "t"), band(h, "g"), band(ell, "g"))


def pay_class_OA52(e: Econ, r, p, eps_V) -> Pay:
    r, p, eps_V = mp.mpf(r), mp.mpf(p), mp.mpf(eps_V)
    h, ell = e.M("h"), e.M("ell")
    t_0 = p * (1 - p / r)
    gL = (ell * ell + eps_V ** 2 / 3 - p * p) / (2 * r)
    tL = ell - gL
    tH = r / 2 + p * p / (2 * r)
    return Pay(r, p, t_0, tH, tL, h - tH, gL)


# ---------------------------------------------------------------------------------------
# noise laws and posterior (float layer for quadrature-heavy work)
# ---------------------------------------------------------------------------------------
def pdf(noise: str, z, b):
    z = np.asarray(z, dtype=float)
    if noise == "Laplace":
        return np.exp(-np.abs(z) / b) / (2 * b)
    u = np.exp(-np.abs(z) / b)
    return u / (b * (1 + u) ** 2)


def logpdf(noise: str, z, b):
    z = np.abs(np.asarray(z, dtype=float))
    if noise == "Laplace":
        return -z / b - math.log(2 * b)
    return -z / b - math.log(b) - 2 * np.log1p(np.exp(-z / b))


def expit(t):
    t = np.asarray(t, dtype=float)
    return 1 / (1 + np.exp(-t))


TAIL_CUT_MULT = 60.0  # finite cut at max|breakpoint or center| + 60 b; the omitted mass is bounded explicitly


def tail_mass_bound(noise: str, b: float) -> float:
    """Noise mass beyond distance 60 b from the density center (both tails)."""
    T = TAIL_CUT_MULT * b
    if noise == "Laplace":
        return math.exp(-T / b)
    return 2 / (1 + math.exp(T / b))


def survival(noise: str, z, b):
    z = np.asarray(z, dtype=float)
    if noise == "Laplace":
        return np.where(z < 0, 1 - 0.5 * np.exp(z / b), 0.5 * np.exp(-z / b))
    return 1 / (1 + np.exp(z / b))


def posterior_bounds_mp(b):
    m = 1 / (1 + mp.exp(2 / b))
    return m, 1 - m


# ---------------------------------------------------------------------------------------
# candidate schedule (benchmark information structure), float layer
# ---------------------------------------------------------------------------------------
class Sched:
    """Pure order profile (q_H, q_L), regime feedback | price_hidden, optional external dividend."""

    def __init__(self, e: Econ, pay: Pay, q_H: float, q_L: float, regime: str = "feedback", dividend: float = 0.0):
        self.e = e
        self.pay = pay
        self.pf = pay.floats()
        self.q_H, self.q_L = float(q_H), float(q_L)
        self.regime = regime
        self.dividend = float(dividend)
        self.noise = e.noise
        self.b = e.F("b")
        self.rho, self.cL, self.cH, self.k = e.F("rho"), e.F("c_L"), e.F("c_H"), e.F("k")
        self.epsC = e.F("eps_C")
        self.breakpoints = self._breakpoints()

    # densities and posterior --------------------------------------------------------
    def aH(self, x):
        return pdf(self.noise, np.asarray(x, float) - self.q_H, self.b)

    def aL(self, x):
        return pdf(self.noise, np.asarray(x, float) - self.q_L, self.b)

    def mu(self, x):
        x = np.asarray(x, float)
        return expit(logpdf(self.noise, x - self.q_H, self.b) - logpdf(self.noise, x - self.q_L, self.b))

    def g(self, x):
        return 0.5 * (self.aH(x) + self.aL(x))

    # entry rule -----------------------------------------------------------------------
    def H_C(self, c):
        c = np.asarray(c, float)
        if self.e.cost == "atoms":
            return self.rho * (c >= self.cL) + (1 - self.rho) * (c >= self.cH)
        eps = self.epsC

        def U(c0):
            return np.clip((c - (c0 - eps)) / (2 * eps), 0, 1)
        return self.rho * U(self.cL) + (1 - self.rho) * U(self.cH)

    def paid_cost_at_B(self, B):
        """E[C 1{C <= B}] under the cost law."""
        B = np.asarray(B, float)
        if self.e.cost == "atoms":
            return self.rho * self.cL * (B >= self.cL) + (1 - self.rho) * self.cH * (B >= self.cH)
        eps = self.epsC

        def comp(c0):
            lo, hi = c0 - eps, c0 + eps
            top = np.clip(B, lo, hi)
            return (top ** 2 - lo ** 2) / (2 * (2 * eps))
        return self.rho * comp(self.cL) + (1 - self.rho) * comp(self.cH)

    def B(self, mu):
        return self.pf["g_L"] + np.asarray(mu, float) * (self.pf["g_H"] - self.pf["g_L"])

    def public_mu(self, x):
        if self.regime == "price_hidden":
            return np.full_like(np.asarray(x, float), 0.5)
        return self.mu(x)

    def entry(self, x):
        return self.H_C(self.B(self.public_mu(x)))

    # price and residuals: computed by direct conditional expectation, not by the residual formula
    def EV_given(self, x, state):
        e = self.entry(x)
        w = self.pf["w_H"] if state == "H" else self.pf["w_L"]
        return self.pf["t_0"] + e * w + self.dividend

    def price(self, x):
        mu = self.mu(x)
        return mu * self.EV_given(x, "H") + (1 - mu) * self.EV_given(x, "L")

    def A(self, x, state):
        if state == "H":
            return self.EV_given(x, "H") - self.price(x)
        return self.price(x) - self.EV_given(x, "L")

    def A_formula(self, x, state):
        mu = self.mu(x)
        e = self.entry(x)
        return e * self.pf["Delta"] * ((1 - mu) if state == "H" else mu)

    # breakpoints: supports and every posterior crossing of a cost boundary --------------
    def cost_boundaries(self):
        if self.e.cost == "atoms":
            return [self.cL, self.cH]
        eps = self.epsC
        return [self.cL - eps, self.cL + eps, self.cH - eps, self.cH + eps]

    def crossing(self, c):
        """x_c with B(mu(x)) >= c iff x >= x_c (monotone posterior); +-inf when never/always."""
        if self.regime == "price_hidden":
            return -np.inf if float(self.B(0.5)) >= c else np.inf
        gH, gL = self.pf["g_H"], self.pf["g_L"]
        if gH == gL:
            return -np.inf if gL >= c else np.inf
        tau = (c - gL) / (gH - gL)
        if self.q_H == self.q_L:
            return -np.inf if 0.5 >= tau else np.inf
        lo, hi = min(self.q_H, self.q_L), max(self.q_H, self.q_L)
        if self.noise == "Laplace":
            mu_lo, mu_hi = float(self.mu(lo - 1)), float(self.mu(hi + 1))
            if tau <= mu_lo:
                return -np.inf
            if tau > mu_hi:
                return np.inf
            if tau == mu_hi:
                return hi  # tie rule: the whole upper plateau enters
            return float(optimize.brentq(lambda x: float(self.mu(x)) - tau, lo, hi, xtol=1e-15, rtol=8.9e-16))
        m = 1 / (1 + math.exp((hi - lo) / self.b))
        if tau <= m:
            return -np.inf
        if tau >= 1 - m:
            return np.inf
        span = 80 * self.b
        return float(optimize.brentq(lambda x: float(self.mu(x)) - tau, lo - span, hi + span, xtol=1e-15, rtol=8.9e-16))

    def _breakpoints(self):
        pts = {self.q_H, self.q_L}
        if self.regime == "feedback":
            for c in self.cost_boundaries():
                xc = self.crossing(c)
                if np.isfinite(xc):
                    pts.add(xc)
        return tuple(sorted(pts))

    def x_star(self):
        return self.crossing(self.cH)


# ---------------------------------------------------------------------------------------
# quadrature over the full line with segment splitting (no truncation; tails to infinity)
# ---------------------------------------------------------------------------------------
def quad_line(fun, breakpoints, extra=(), n_limit: int = 200, noise: str = "Laplace", b: float = 2.0):
    """int over the real line of fun(x) dx split at all breakpoints. The line is cut at
    +-(max|breakpoint, extra| + 60 b); the omitted mass is bounded separately (see tail_mass_bound).
    Returns (value, abs error estimate)."""
    pts = sorted(set(list(breakpoints) + [float(x) for x in extra if np.isfinite(x)]))
    T = TAIL_CUT_MULT * b
    pts = [pts[0] - T] + pts + [pts[-1] + T]
    tot, err = 0.0, 0.0
    f = lambda x: float(fun(np.array([x]))[0])
    for a, c in zip(pts[:-1], pts[1:]):
        v, e_ = integrate.quad(f, a, c, epsabs=QUAD_ABS, epsrel=QUAD_REL, limit=n_limit)
        tot += v
        err += e_
    return tot, err


def U_order(s: Sched, state: str, q: float):
    """Expected trading profit of order q (any sign) in `state` against the fixed schedule.

    E[q (V_T - P) - k|q| | state] = q * eps_state * int f(x - q) A_state(x) dx - k|q|, eps_H = +1, eps_L = -1.
    Returns (value, quadrature error, tail bound entry)."""
    if q == 0.0:
        return 0.0, 0.0, 0.0
    eps = 1.0 if state == "H" else -1.0
    val, err = quad_line(lambda x: pdf(s.noise, x - q, s.b) * s.A(x, state), s.breakpoints, extra=[q], noise=s.noise, b=s.b)
    A_bar = s.pf["Delta"]
    return q * eps * val - s.k * abs(q), abs(q) * err, abs(q) * A_bar * tail_mass_bound(s.noise, s.b)


def deviation_scan(spec: dict) -> dict:
    """Worker: global order scan on [-1,1] for both states; returns gains and error budgets."""
    s = sched_from_spec(spec)
    n = spec.get("intervals", ORDER_INTERVALS)
    grid = list(np.linspace(-1, 1, n + 1))
    xs = s.x_star()
    extra = [xs, -xs, s.q_H, s.q_L, -s.q_H, -s.q_L] if np.isfinite(xs) else [s.q_H, s.q_L, -s.q_H, -s.q_L]
    qs = sorted(set(grid + [float(x) for x in extra if -1 <= x <= 1]))
    out = {}
    for state, q_own in (("H", s.q_H), ("L", s.q_L)):
        base, base_err, base_tail = U_order(s, state, q_own)
        best_gain, best_q, qerr, tail = -np.inf, None, 0.0, 0.0
        for q in qs:
            u, e_, t_ = U_order(s, state, q)
            g = u - base
            if g > best_gain:
                best_gain, best_q = g, q
            qerr = max(qerr, e_ + base_err)
            tail = max(tail, t_ + base_tail)
        h = 2.0 / n
        A_bar = s.pf["Delta"]
        lip1 = A_bar * (1 + 1 / s.b) + s.k               # |dU/dq| bound
        lip2 = 2 * A_bar / s.b + A_bar / s.b ** 2         # OA.63 second-derivative bound (a.e.)
        out[state] = {"max_gain": best_gain, "argmax_q": best_q, "candidate_payoff": base,
                      "budget": {"quadrature": qerr, "tail_truncation": tail,
                                 "between_grid_first_order": lip1 * h / 2, "between_grid_second_order": lip2 * h * h / 8,
                                 "grid_points": len(qs), "order_intervals": n}}
    return {"spec": spec, "scan": out}


def sched_from_spec(spec: dict) -> Sched:
    e = Econ(**spec["econ"])
    pay = pay_binary(e, spec["r"], spec.get("p"))
    return Sched(e, pay, spec["q_H"], spec["q_L"], spec.get("regime", "feedback"), spec.get("dividend", 0.0))


# ---------------------------------------------------------------------------------------
# equilibrium objects for a schedule: entry (flow and cost based), revenue, welfare, identities
# ---------------------------------------------------------------------------------------
def objects(s: Sched) -> dict:
    bp = s.breakpoints
    # flow-based entry
    ql = lambda fun: quad_line(fun, bp, noise=s.noise, b=s.b)
    eH, eH_err = ql(lambda x: s.aH(x) * s.entry(x))
    eL, eL_err = ql(lambda x: s.aL(x) * s.entry(x))
    # cost-based entry: integrate the tail probability over the cost law
    def tail_prob(c, state):
        xc = s.crossing(c)
        if xc == -np.inf:
            return 1.0
        if xc == np.inf:
            return 0.0
        q = s.q_H if state == "H" else s.q_L
        return float(survival(s.noise, xc - q, s.b))

    def cost_based(state):
        if s.e.cost == "atoms":
            return s.rho * tail_prob(s.cL, state) + (1 - s.rho) * tail_prob(s.cH, state)
        eps = s.epsC
        tot = 0.0
        for w, c0 in ((s.rho, s.cL), (1 - s.rho, s.cH)):
            # split at the attainable-profit plateau boundaries so the integrand is smooth
            lo, hi = c0 - eps, c0 + eps
            edges = sorted({lo, hi, *[float(v) for v in (s.B(s.mu(min(s.q_H, s.q_L) - 60 * s.b)), s.B(s.mu(max(s.q_H, s.q_L) + 60 * s.b))) if lo < v < hi]})
            v = 0.0
            for a, c in zip(edges[:-1], edges[1:]):
                v += integrate.quad(lambda cc: tail_prob(cc, state), a, c, epsabs=QUAD_ABS, epsrel=QUAD_REL, limit=200)[0]
            tot += w * v / (2 * eps)
        return tot
    eH2, eL2 = cost_based("H"), cost_based("L")
    E = 0.5 * (eH + eL)
    O_H = 0.5 * eH
    R_T = s.pf["t_0"] + 0.5 * (eH * s.pf["w_H"] + eL * s.pf["w_L"])
    paid, paid_err = ql(lambda x: s.g(x) * s.paid_cost_at_B(s.B(s.public_mu(x))))
    r, p = s.pf["r"], s.pf["p"]
    W = (r * r - p * p) / (2 * r) + 0.5 * (eH * (s.pf["g_H"] + p * p / r) + eL * (s.pf["g_L"] + p * p / r)) - paid
    # identities
    intH, _ = ql(lambda x: s.aH(x))
    intL, _ = ql(lambda x: s.aL(x))
    Emu, _ = ql(lambda x: s.g(x) * s.mu(x))
    EP, EP_err = ql(lambda x: s.g(x) * s.price(x))
    EV = R_T + s.dividend
    # pointwise price identity and residual formula agreement on a fine grid
    lo = min(bp) - 40 * s.b
    hi = max(bp) + 40 * s.b
    xs = np.unique(np.concatenate([np.linspace(lo, hi, 20001), np.array(bp)]))
    mu = s.mu(xs)
    e = s.entry(xs)
    P = s.price(xs)
    EVx = s.pf["t_0"] + e * (mu * s.pf["w_H"] + (1 - mu) * s.pf["w_L"]) + s.dividend
    eps_P = float(np.max(np.abs(P - EVx)))
    res_err = max(float(np.max(np.abs(s.A(xs, st) - s.A_formula(xs, st)))) for st in "HL")
    # entry optimality: any cost type reversing its decision at any tested public posterior
    Bpub = s.B(s.public_mu(xs))
    eps_e = 0.0
    for c in ([s.cL, s.cH] if s.e.cost == "atoms" else [s.cL - s.epsC, s.cL, s.cL + s.epsC, s.cH - s.epsC, s.cH, s.cH + s.epsC]):
        enters = Bpub >= c
        eps_e = max(eps_e, float(np.max(np.maximum(np.where(enters, c - Bpub, Bpub - c), 0.0))))
    return {"e_H": eH, "e_L": eL, "e_H_cost_based": eH2, "e_L_cost_based": eL2, "E": E, "O_H": O_H, "R_T": R_T, "W": W,
            "paid_cost": paid, "mean_price": EP, "EV": EV, "int_aH": intH, "int_aL": intL, "E_mu": Emu,
            "eps_P": eps_P, "residual_formula_error": res_err, "eps_e": eps_e, "x_star": s.x_star(),
            "tau": float(s.pay.tau(s.e.M("c_H"))), "quad_err": max(eH_err, eL_err, paid_err, EP_err),
            "tail_mass_bound": tail_mass_bound(s.noise, s.b)}


def welfare_gain_OA47(s_fb: Sched) -> float:
    """OA.47 / OA.48 evaluated on the feedback marginal flow density."""
    p, r = s_fb.pf["p"], s_fb.pf["r"]
    rho = s_fb.rho

    def integrand(x):
        Bx = s_fb.B(s_fb.mu(x))
        if s_fb.e.cost == "atoms":
            return s_fb.g(x) * (Bx - s_fb.cH + p * p / r) * (Bx >= s_fb.cH)
        eps = s_fb.epsC
        lo, hi = s_fb.cH - eps, s_fb.cH + eps
        top = np.clip(Bx, lo, hi)
        inner = ((Bx + p * p / r) * (top - lo) - (top ** 2 - lo ** 2) / 2) / (2 * eps)
        return s_fb.g(x) * inner
    v, _ = quad_line(integrand, s_fb.breakpoints, noise=s_fb.noise, b=s_fb.b)
    return (1 - rho) * v


# closed forms for full Laplace/logistic orders with atomic costs (eq. 14 / OA.16-17, eq. 20 / OA.23-25)
def full_order_closed(e: Econ, pay: Pay) -> dict:
    b, rho = e.M("b"), e.M("rho")
    m, M = posterior_bounds_mp(b)
    tau = pay.tau(e.M("c_H"))
    if e.noise == "Laplace":
        if tau <= m:
            xs, aH, aL = -mp.inf, mp.mpf(1), mp.mpf(1)
        elif tau > M:
            xs, aH, aL = mp.inf, mp.mpf(0), mp.mpf(0)
        elif tau == M:
            xs, aH, aL = mp.mpf(1), mp.mpf(1) / 2, mp.exp(-2 / b) / 2
        else:
            xs = b / 2 * mp.log(tau / (1 - tau))
            aH = 1 - mp.exp((xs - 1) / b) / 2 if xs < 1 else mp.exp(-(xs - 1) / b) / 2
            aL = mp.exp(-(xs + 1) / b) / 2 if xs > -1 else 1 - mp.exp((xs + 1) / b) / 2
    else:
        if tau <= m:
            xs, aH, aL = -mp.inf, mp.mpf(1), mp.mpf(1)
        elif tau >= M:
            xs, aH, aL = mp.inf, mp.mpf(0), mp.mpf(0)
        else:
            A = mp.exp(1 / b)
            w = mp.sqrt(tau / (1 - tau))
            xs = b * mp.log((A * w - 1) / (A - w))
            aH = 1 / (1 + mp.exp((xs - 1) / b))
            aL = 1 / (1 + mp.exp((xs + 1) / b))
    eH = rho + (1 - rho) * aH
    eL = rho + (1 - rho) * aL
    return {"tau": tau, "m": m, "M": M, "x_star": xs, "alpha_H": aH, "alpha_L": aL, "e_H": eH, "e_L": eL,
            "E": (eH + eL) / 2, "O_H": eH / 2, "R_T": pay.t_0 + (eH * pay.w_H + eL * pay.w_L) / 2}


def theorem_margins(e: Econ, pay0: Pay, pay1: Pay) -> dict:
    b, rho, k = e.M("b"), e.M("rho"), e.M("k")
    m, M = posterior_bounds_mp(b)
    cL, cH = e.M("c_L"), e.M("c_H")
    epsC = e.M("eps_C")
    # atomless costs: replace endpoints as in Proposition A.6 (OA.26)
    return {"zeta_L": pay1.B(m) - (cL + epsC), "zeta_H0": (cH - epsC) - pay0.B(mp.mpf(1) / 2), "zeta_H1": pay1.B(M) - (cH + epsC),
            "zeta_0": k - pay0.Delta, "zeta_1": (1 - 1 / b) * rho * m * pay1.Delta - k}


# ---------------------------------------------------------------------------------------
# CSV access, joined on full parameter columns and labels
# ---------------------------------------------------------------------------------------
def read_csv(path: str) -> list[dict]:
    with open(ROOT / path, newline="") as f:
        return list(csv.DictReader(f))


def pick(rows: list[dict], **key) -> dict:
    hits = [r for r in rows if all(str(r.get(k)) == str(v) for k, v in key.items())]
    if len(hits) != 1:
        raise CheckFailure(f"join on {key} returned {len(hits)} rows")
    return hits[0]


def ff(x) -> float:
    return float(x)


# ---------------------------------------------------------------------------------------
# tests
# ---------------------------------------------------------------------------------------
def t02_t03_auction(L: Ledger):
    prim = read_csv("tables/auction_primitives.csv")
    for e, strengths in ((E_BASE, ("r_weak", "r_strong", "r_collapse")), (E_MOD, ("r_weak", "r_strong")), (E_SIG, ("r_weak", "r_strong"))):
        decl = {"base": BENCH, "moderate": MODER, "signal": SIGN}[e.tag]
        for sname in strengths:
            rs = decl[sname]
            pay = pay_binary(e, rs)
            pay_f = pay_benchmark_formula(e, rs)
            pay_i = pay_integrated(e, rs)
            row = pick(prim, parameter_set=e.tag, r=rs)
            for a in ("t_0", "t_H", "t_L", "g_H", "g_L"):
                v = getattr(pay, a)
                L.add("T02", f"auction/{e.tag}/r={rs}/{a} integrated vs OA.51", getattr(pay_i, a), v, TOL_FORMULA,
                      budget={"mpmath_dps": 30})
                L.add("T02", f"auction/{e.tag}/r={rs}/{a} main-text formula vs OA.51", getattr(pay_f, a), v, TOL_FORMULA)
                L.add("T02", f"auction/{e.tag}/r={rs}/{a} repo CSV", v, ff(row[a]), TOL_FORMULA)
            L.add("T02", f"auction/{e.tag}/r={rs}/Delta_T = (r-ell)^2/(2r)", pay.Delta, (mp.mpf(rs) - e.M("ell")) ** 2 / (2 * mp.mpf(rs)), TOL_FORMULA)
            L.add("T02", f"auction/{e.tag}/r={rs}/Delta_T repo", pay.Delta, ff(row["Delta_T"]), TOL_FORMULA)
            m, M = posterior_bounds_mp(e.M("b"))
            for nm, mu in (("B_m", m), ("B_prior", mp.mpf(1) / 2), ("B_M", M)):
                L.add("T02", f"auction/{e.tag}/r={rs}/{nm} repo", pay.B(mu), ff(row[nm]), TOL_FORMULA)
    # T03: full-domain regimes with equality cases, generic (r, v, p) triples
    e = E_BASE
    cases = [("v<p", "3", "1", "2"), ("v=p (bid meets reserve)", "3", "1", "1"), ("p<v<r", "3", "2", "0.5"),
             ("v=r", "3", "3", "0.5"), ("p<r<v", "3", "10", "0.5"), ("p=r<v", "3", "10", "3"), ("r<p<v", "3", "10", "5"),
             ("r<p=v", "3", "5", "5"), ("p=0", "3", "1", "0"), ("v<p, p>r", "3", "1", "4"), ("p just below v", "3", "1", "0.9999"),
             ("p just above v", "3", "1", "1.0001")]
    for label, rs, vs, ps in cases:
        r, v, p = mp.mpf(rs), mp.mpf(vs), mp.mpf(ps)
        t_k, g_k = kernel(r, v, p)
        t_i = integrate_uniform(lambda R: T_real(R, v, p), r, [p, v])
        g_i = integrate_uniform(lambda R: G_real(R, v, p), r, [p, v])
        L.add("T03", f"regime {label} (r={rs}, v={vs}, p={ps}): t_v integral vs kernel", t_i, t_k, TOL_FORMULA)
        L.add("T03", f"regime {label} (r={rs}, v={vs}, p={ps}): g_v integral vs kernel", g_i, g_k, TOL_FORMULA)
        # no-sale state: when v < p the seller receives zero on R < p
        if v < p:
            no_sale = integrate_uniform(lambda R: (mp.mpf(1) if (R < p) else mp.mpf(0)), r, [p])
            L.add("T03", f"regime {label}: no-sale probability = min(p,r)/r", no_sale, min(p, r) / r, TOL_FORMULA)
    # equality: v = p sells with certainty (bid equal to the reserve is admissible), v = p - 0 does not
    r, p = mp.mpf(3), mp.mpf(1)
    sale_eq = integrate_uniform(lambda R: (mp.mpf(1) if T_real(R, p, p) > 0 else mp.mpf(0)), r, [p])
    sale_below = integrate_uniform(lambda R: (mp.mpf(1) if T_real(R, p - mp.mpf("1e-9"), p) > 0 else mp.mpf(0)), r, [p])
    L.require("T03", "v = p: sale certain (tie convention), v just below p: sale iff R >= p",
              abs(sale_eq - 1) < TOL_FORMULA and abs(sale_below - (1 - p / r)) < TOL_FORMULA,
              note=f"Pr(sale|v=p)={mp.nstr(sale_eq,12)}, Pr(sale|v=p-1e-9)={mp.nstr(sale_below,12)}")
    # class economy oracle at the declared reserves
    epsV = BENCH["value_band_halfwidth"]
    rc = read_csv("tables/reserve_comparisons.csv")
    for rs in (BENCH["r_weak"], BENCH["r_strong"]):
        for ps in (BENCH["p"], BENCH["atomless_alternative_reserve"]):
            pk = pay_class(e, rs, ps, epsV, integrate_direct=False)
            pi = pay_class(e, rs, ps, epsV, integrate_direct=True)
            row = pick(rc, value_law="uniform_classes", r=rs, p=ps)
            for a in ("t_0", "t_H", "t_L", "g_H", "g_L"):
                L.add("T03", f"class/r={rs}/p={ps}/{a} direct OA.50 integral vs kernel average", getattr(pi, a), getattr(pk, a), TOL_FORMULA)
                L.add("T03", f"class/r={rs}/p={ps}/{a} repo CSV", getattr(pk, a), ff(row[a]), TOL_FORMULA)
            if mp.mpf(ps) < e.M("ell") - mp.mpf(epsV) and e.M("ell") + mp.mpf(epsV) < mp.mpf(rs) < e.M("h") - mp.mpf(epsV):
                p52 = pay_class_OA52(e, rs, ps, epsV)
                for a in ("t_0", "t_H", "t_L", "g_H", "g_L"):
                    L.add("T03", f"class/r={rs}/p={ps}/{a} OA.52 formula", p52.__getattribute__(a), getattr(pk, a), TOL_FORMULA)
        for ps in (BENCH["p"], BENCH["binary_alternative_reserve"]):
            pb = pay_binary(e, rs, ps)
            pbi = pay_integrated(e, rs, ps)
            row = pick(rc, value_law="binary", r=rs, p=ps)
            for a in ("t_0", "t_H", "t_L", "g_H", "g_L"):
                L.add("T03", f"binary/r={rs}/p={ps}/{a} direct OA.50 integral vs kernel", getattr(pbi, a), getattr(pb, a), TOL_FORMULA)
                L.add("T03", f"binary/r={rs}/p={ps}/{a} repo CSV", getattr(pb, a), ff(row[a]), TOL_FORMULA)


def benchmark_candidates() -> list[dict]:
    """All candidate schedules retained in tables/equilibrium_controls.csv, as specs."""
    specs = []
    ctrl = read_csv("tables/equilibrium_controls.csv")
    for e in ECONOMIES:
        for sname in ("r_weak", "r_strong", "r_collapse"):
            rs = BENCH[sname]
            for row in ctrl:
                if not (row["parameter_set"] == e.tag and row["noise"] == e.noise and row["cost_law"] == e.cost and row["r"] == rs):
                    continue
                regime = "price_hidden" if row["experiment"] in ("price_hidden", "matched_dividend") else "feedback"
                specs.append({"econ": asdict(e), "r": rs, "q_H": ff(row["q_H"]), "q_L": ff(row["q_L"]), "regime": regime,
                              "dividend": ff(row["matched_dividend"]) if row["experiment"] == "matched_dividend" else 0.0,
                              "experiment": row["experiment"], "sname": sname, "row": row})
    return specs


def econ_label(e: dict) -> str:
    return f"{e['tag']}/{e['noise']}/{e['cost']}"


def t04_t05_t06_t08_t09_t10(L: Ledger, scans: dict):
    ctrl = read_csv("tables/equilibrium_controls.csv")
    ext = read_csv("tables/extensions.csv")
    fb = read_csv("numerics/feedback_comparisons.csv")
    objs = {}
    for spec in benchmark_candidates():
        s = sched_from_spec(spec)
        o = objects(s)
        row = spec["row"]
        key = (econ_label(spec["econ"]), spec["r"], spec["experiment"], spec["q_H"], spec["q_L"])
        objs[key] = (s, o, row)
        lab = f"{key[0]}/r={key[1]}/{key[2]}/({key[3]:g},{key[4]:g})"
        # T04 identities
        L.add("T04", f"{lab}: int a_H = 1", o["int_aH"], 1.0, TOL_PROB)
        L.add("T04", f"{lab}: int a_L = 1", o["int_aL"], 1.0, TOL_PROB)
        L.add("T04", f"{lab}: E[mu_X] = 1/2", o["E_mu"], 0.5, TOL_PROB)
        L.add("T04", f"{lab}: E[P] = E[V_T] (+dividend)", o["mean_price"], o["EV"], TOL_PROB, budget={"quadrature": o["quad_err"]})
        L.add("T04", f"{lab}: flow-based vs cost-based e_H", o["e_H"], o["e_H_cost_based"], TOL_FORMULA)
        L.add("T04", f"{lab}: flow-based vs cost-based e_L", o["e_L"], o["e_L_cost_based"], TOL_FORMULA)
        # T05 pointwise price identity, residual formula, entry optimality
        L.add("T05", f"{lab}: sup|P - E[V_T|x]|", o["eps_P"], 0.0, TOL_PRICE)
        L.add("T05", f"{lab}: residual direct vs eq.10 formula", o["residual_formula_error"], 0.0, TOL_PRICE)
        L.add("T05", f"{lab}: entry reversal gain", o["eps_e"], 0.0, TOL_ENTRY)
        # repo values (join on full parameter columns + labels)
        for a in ("e_H", "e_L", "E", "O_H", "R_T", "W"):
            L.add("T04", f"{lab}: {a} vs repo", o[a], ff(row[a]), TOL_FORMULA)
        L.add("T04", f"{lab}: expected paid preparation cost vs repo", o["paid_cost"], ff(row["expected_preparation_cost"]), TOL_FORMULA)
        L.add("T04", f"{lab}: tau vs repo", o["tau"], ff(row["tau"]), TOL_FORMULA)
        if spec["regime"] == "feedback" and spec["econ"]["cost"] == "atoms" and spec["q_H"] != spec["q_L"]:
            L.add("T04", f"{lab}: x_star vs repo", o["x_star"], ff(row["x_star"]), 1e-9)
        # closed forms for full orders with atomic costs
        if spec["regime"] == "feedback" and spec["econ"]["cost"] == "atoms" and spec["q_H"] == 1.0 and spec["q_L"] == -1.0:
            cf = full_order_closed(Econ(**spec["econ"]), s.pay)
            for a in ("e_H", "e_L", "E", "O_H", "R_T"):
                L.add("T04", f"{lab}: {a} quadrature vs closed form", o[a], cf[a], TOL_FORMULA)
            L.add("T04", f"{lab}: x_star root vs closed form", o["x_star"], cf["x_star"], 1e-9)
        # T07 scans
        sc = scans.get(key)
        if sc is not None:
            gain = max(sc["H"]["max_gain"], sc["L"]["max_gain"])
            accepted = row["accepted"].lower() == "true"
            is_eq = row["experiment"] in ("feedback", "price_hidden", "matched_dividend")
            bud = {st: sc[st]["budget"] for st in "HL"}
            if is_eq and accepted:
                L.add("T07", f"{lab}: max unilateral gain (accepted equilibrium row)", gain, 0.0, TOL_DEV,
                      passed=gain <= TOL_DEV, budget=bud, note=f"argmax H q={sc['H']['argmax_q']}, L q={sc['L']['argmax_q']}")
            else:
                m_ = re.search(r"epsilon_q=([0-9.e+-]+)|deviation gain ([0-9.e+-]+)", row["status"])
                repo_gain = ff(m_.group(1) or m_.group(2)) if m_ else None
                L.add("T07", f"{lab}: max unilateral gain (retained non-equilibrium/control row)", gain, repo_gain, 5e-4 if repo_gain is not None else None,
                      budget=bud, note=f"repo status: {row['status']}", required=False)
                if is_eq and not accepted:
                    L.require("T07", f"{lab}: rejected row has a profitable deviation", gain > TOL_DEV, note=f"gain={gain:.3e}")
    # T06 theorem margins (A1)-(A3) and part (iii)
    for e in ECONOMIES:
        pay0, pay1, pay2 = (pay_binary(e, BENCH[s]) for s in ("r_weak", "r_strong", "r_collapse"))
        z = theorem_margins(e, pay0, pay1)
        row = pick(ext, parameter_set=e.tag, noise=e.noise, cost_law=e.cost, r_weak=BENCH["r_weak"], r_strong=BENCH["r_strong"])
        lab = f"{e.tag}/{e.noise}/{e.cost}"
        for nm, v in z.items():
            L.add("T06", f"{lab}: {nm} vs repo", v, ff(row[nm]), TOL_FORMULA)
            L.require("T06", f"{lab}: {nm} > 0", v > 0, note=mp.nstr(v, 12))
        for a in ("E_weak", "E_strong", "O_H_weak", "O_H_strong"):
            # cross-check extension table against the accepted feedback rows
            exp_key = (lab, BENCH["r_weak" if "weak" in a else "r_strong"], "feedback")
            cands = [(k, v) for k, v in objs.items() if k[:3] == exp_key and v[2]["accepted"].lower() == "true"]
            L.require("T06", f"{lab}: exactly one accepted feedback candidate at {a.split('_')[-1]}", len(cands) == 1, note=str(len(cands)))
            if len(cands) == 1:
                L.add("T06", f"{lab}: {a} table vs accepted candidate", cands[0][1][1][a.split("_")[0] if a.startswith("E") else "O_H"], ff(row[a]), TOL_FORMULA)
        # part (iii) conditions at the collapse strength
        m, M = posterior_bounds_mp(e.M("b"))
        epsC = e.M("eps_C")
        c3 = {"low_cost_floor_r2": pay2.B(m) - (e.M("c_L") + epsC),
              "full_order_bound_r2": (1 - 1 / e.M("b")) * e.M("rho") * m * pay2.Delta - e.M("k"),
              "expensive_entry_infeasible_r2 (c_H - eps_C - B_r2(M))": (e.M("c_H") - epsC) - pay2.B(M)}
        for nm, v in c3.items():
            if e.cost == "atoms" or not nm.startswith("expensive_entry_infeasible"):
                L.require("T06", f"{lab}: part (iii) {nm} > 0", v > 0, note=mp.nstr(v, 12))
        if e.cost != "atoms":
            L.add("T06", f"{lab}: atomless collapse node has partial expensive entry (c_H - eps_C < B_r2(M) < c_H + eps_C)",
                  float(pay2.B(M)), None, status="info", note=f"B_r2(M)={mp.nstr(pay2.B(M),10)}; repo E={pick(ctrl, parameter_set=e.tag, noise=e.noise, cost_law=e.cost, r=BENCH['r_collapse'], experiment='feedback', q_H='1.0')['E']}",
                  required=False)
    # T08 control semantics
    for e in ECONOMIES:
        lab = f"{e.tag}/{e.noise}/{e.cost}"
        fz = pick(ctrl, parameter_set=e.tag, noise=e.noise, cost_law=e.cost, r=BENCH["r_weak"], experiment="frozen")
        L.require("T08", f"{lab}: frozen weak profile labelled numerical diagnostic, not equilibrium",
                  fz["status"].startswith("numerical diagnostic") and "not an equilibrium assertion" in fz["status"], note=fz["status"])
        k_w = (lab, BENCH["r_weak"], "frozen", 1.0, -1.0)
        if k_w in scans:
            g = max(scans[k_w]["H"]["max_gain"], scans[k_w]["L"]["max_gain"])
            L.require("T08", f"{lab}: frozen weak profile has a profitable investor deviation (gain > tol)", g > TOL_DEV, note=f"gain={g:.4e}")
        # hidden game reoptimized: weak -> pooling accepted, full rejected; strong -> full accepted, pooling rejected
        for rs, want in ((BENCH["r_weak"], "0.0"), (BENCH["r_strong"], "1.0")):
            acc = [r for r in ctrl if r["parameter_set"] == e.tag and r["noise"] == e.noise and r["cost_law"] == e.cost and r["r"] == rs
                   and r["experiment"] == "price_hidden" and r["accepted"].lower() == "true"]
            L.require("T08", f"{lab}: price-hidden r={rs} accepted candidate is q_H={want}", len(acc) == 1 and acc[0]["q_H"] == want,
                      note=str([(a["q_H"], a["q_L"]) for a in acc]))
        # independent: hidden pooling at weak is a best response (constant residual rho Delta/2 < k) and full at strong (bound)
        pay0, pay1 = pay_binary(e, BENCH["r_weak"]), pay_binary(e, BENCH["r_strong"])
        e0 = float(Sched(e, pay0, 0, 0, "price_hidden").H_C(float(pay0.B(mp.mpf(1) / 2))))
        L.require("T08", f"{lab}: hidden weak pooling coefficient e0*Delta/2 - k < 0", e0 * float(pay0.Delta) / 2 - e.F("k") < 0)
        m, _ = posterior_bounds_mp(e.M("b"))
        L.require("T08", f"{lab}: hidden strong full-order bound (1-1/b) e0 m Delta - k > 0",
                  (1 - 1 / e.M("b")) * mp.mpf(e0) * m * pay1.Delta - e.M("k") > 0)
    # T09 dividend invariance and T10 welfare identity
    for e in ECONOMIES:
        lab = f"{e.tag}/{e.noise}/{e.cost}"
        for sname in ("r_weak", "r_strong", "r_collapse"):
            rs = BENCH[sname]
            fbk = [(k, v) for k, v in objs.items() if k[:3] == (lab, rs, "feedback") and v[2]["accepted"].lower() == "true"]
            hdk = [(k, v) for k, v in objs.items() if k[:3] == (lab, rs, "price_hidden") and v[2]["accepted"].lower() == "true"]
            mdk = [(k, v) for k, v in objs.items() if k[:3] == (lab, rs, "matched_dividend")]
            if not (len(fbk) == 1 and len(hdk) == 1 and len(mdk) == 1):
                L.require("T09", f"{lab}/r={rs}: one accepted feedback, one hidden and one matched row", False, note=f"{len(fbk)},{len(hdk)},{len(mdk)}")
                continue
            (kf, (sf, of, rf)), (kh, (sh, oh, rh)), (km, (sm, om, rm)) = fbk[0], hdk[0], mdk[0]
            D0 = of["R_T"] - oh["R_T"]
            L.add("T09", f"{lab}/r={rs}: D0 = R_T^fb - R_T^hidden vs repo matched_dividend", D0, ff(rm["matched_dividend"]), TOL_FORMULA)
            L.require("T09", f"{lab}/r={rs}: matched row uses the hidden profile", (km[3], km[4]) == (kh[3], kh[4]), note=f"{km[3:]}, {kh[3:]}")
            # rebuild the matched schedule with the independent D0
            s_m = Sched(e, sh.pay, kh[3], kh[4], "price_hidden", D0)
            xs = np.linspace(-8, 8, 4001)
            inv = max(float(np.max(np.abs(s_m.A(xs, st) - sh.A(xs, st)))) for st in "HL")
            shift = float(np.max(np.abs(s_m.price(xs) - sh.price(xs) - D0)))
            o_m = objects(s_m)
            L.add("T09", f"{lab}/r={rs}: residual invariance sup|A^matched - A^hidden|", inv, 0.0, TOL_FORMULA)
            L.add("T09", f"{lab}/r={rs}: price shift equals D0 pointwise", shift, 0.0, TOL_FORMULA)
            L.add("T09", f"{lab}/r={rs}: E[P^matched] = E[P^feedback] = R_T^feedback", o_m["mean_price"], of["R_T"], TOL_PROB)
            for a in ("e_H", "e_L", "E", "R_T", "W", "paid_cost"):
                L.add("T09", f"{lab}/r={rs}: matched {a} = hidden {a}", o_m[a], oh[a], TOL_FORMULA)
            L.add("T09", f"{lab}/r={rs}: matched row E vs repo", o_m["E"], ff(rm["E"]), TOL_FORMULA)
            # T10 welfare
            dW_direct = welfare_gain_OA47(sf) if (kf[3], kf[4]) == (1.0, -1.0) and (kh[3], kh[4]) == (1.0, -1.0) else None
            W_gain = of["W"] - oh["W"]
            frow = pick(fb, parameter_set=e.tag, noise=e.noise, cost_law=e.cost, r=rs)
            L.add("T10", f"{lab}/r={rs}: W_gain (OA.49 difference) vs repo", W_gain, ff(frow["W_gain"]), TOL_FORMULA)
            if dW_direct is not None:
                L.add("T10", f"{lab}/r={rs}: OA.47/48 integral vs OA.49 difference", dW_direct, W_gain, TOL_FORMULA)
            dR_cond = 0.5 * ((of["e_H"] - oh["e_H"]) * sf.pf["w_H"] + (of["e_L"] - oh["e_L"]) * sf.pf["w_L"])
            dR_price = of["mean_price"] - oh["mean_price"]
            L.add("T10", f"{lab}/r={rs}: revenue gain from conditional entry vs mean-price difference", dR_cond, dR_price, TOL_PROB)
            L.add("T10", f"{lab}/r={rs}: revenue gain vs repo R_T_gain", dR_cond, ff(frow["R_T_gain"]), TOL_FORMULA)
            # paid-cost selection: the naive 'mean cost times entry' differs from the selected paid cost when the high type enters
            if e.cost == "atoms":
                naive = (e.F("rho") * e.F("c_L") + (1 - e.F("rho")) * e.F("c_H")) * of["E"]
                L.add("T10", f"{lab}/r={rs}: selected paid cost vs naive mean cost x entry (informational)", of["paid_cost"], naive, None,
                      note=f"selected paid cost = rho c_L + (1-rho) c_H Pr(high type enters) = {of['paid_cost']:.10f}; naive product {naive:.10f}",
                      required=False, passed=True, status="info")
    return objs


def t11_logistic(L: Ledger):
    e = ECONOMIES[2]  # logistic, atoms
    pay = pay_binary(e, BENCH["r_strong"])
    cf = full_order_closed(e, pay)
    b = e.M("b")
    # inverse check: log-odds formula OA.24 at x_star equals logit(tau)
    lo = 2 * mp.log(mp.cosh((cf["x_star"] + 1) / (2 * b))) - 2 * mp.log(mp.cosh((cf["x_star"] - 1) / (2 * b)))
    L.add("T11", "logistic x*: OA.24 log-odds at x* = logit(tau)", lo, mp.log(cf["tau"] / (1 - cf["tau"])), 1e-25)
    # root-based inverse from the densities themselves
    def mu_log(x):
        fH = mp.exp(-(x - 1) / b) / (b * (1 + mp.exp(-(x - 1) / b)) ** 2)
        fL = mp.exp(-(x + 1) / b) / (b * (1 + mp.exp(-(x + 1) / b)) ** 2)
        return fH / (fH + fL)
    root = mp.findroot(lambda x: mu_log(x) - cf["tau"], mp.mpf(5))
    L.add("T11", "logistic x*: density-ratio root vs closed form", root, cf["x_star"], 1e-20)
    ctrl = read_csv("tables/equilibrium_controls.csv")
    row = pick(ctrl, parameter_set="base", noise="logistic", cost_law="atoms", r=BENCH["r_strong"], experiment="feedback", q_H="1.0")
    L.add("T11", "logistic x* vs repo", cf["x_star"], ff(row["x_star"]), 1e-9)
    L.add("T11", "logistic strong preparation vs repo", cf["E"], ff(row["E"]), TOL_FORMULA)
    L.add("T11", "logistic strong preparation vs landmark", cf["E"], Decimal(LANDMARKS["logistic_strong_prep"][0]), DISPLAY_TOL)
    sd = b * mp.pi / mp.sqrt(3)
    std = cf["x_star"] / sd
    L.add("T11", "standardized cutoff x*/(b pi/sqrt3)", std, Decimal("1.495369"), 5e-7)
    tails = read_csv("figures_data/posterior_tails.csv")
    trow = pick(tails, noise="logistic", tau_label="benchmark")
    L.add("T11", "standardized cutoff vs repo posterior_tails threshold_noise_sd", std, ff(trow["threshold_noise_sd"]), TOL_FORMULA)
    L.add("T11", "noise variance b^2 pi^2/3 vs repo", sd * sd, ff(trow["noise_variance"]), TOL_FORMULA)
    L.require("T11", "standardized cutoff uses noise variance, not flow variance", abs(ff(trow["flow_variance"]) - (float(sd * sd) + 1.0)) < 1e-9
              and abs(ff(trow["threshold_noise_sd"]) - float(cf["x_star"]) / math.sqrt(float(sd * sd))) < 1e-9)
    # direct integration of the tails
    xs = float(cf["x_star"])
    for sh, val, nm in ((1.0, cf["alpha_H"], "alpha_H"), (-1.0, cf["alpha_L"], "alpha_L")):
        v1 = integrate.quad(lambda z: float(pdf("logistic", z - sh, float(b))), xs, np.inf, epsabs=QUAD_ABS, epsrel=QUAD_REL, limit=200)[0]
        L.add("T11", f"logistic {nm} direct tail integral vs closed form", v1, val, TOL_FORMULA)
    # threshold and endpoint behaviour
    m, M = posterior_bounds_mp(b)
    A = mp.exp(1 / b)
    for eps_ in ("1e-4", "1e-6", "1e-8"):
        tau = M - mp.mpf(eps_)
        w = mp.sqrt(tau / (1 - tau))
        x = b * mp.log((A * w - 1) / (A - w))
        L.require("T11", f"logistic tau = M - {eps_}: finite cutoff with positive tail mass", mp.isfinite(x) and x > 1,
                  note=f"x*={mp.nstr(x, 8)}, alpha_H={mp.nstr(1/(1+mp.exp((x-1)/b)), 6)}")
    L.require("T11", "logistic tau = M: unattained endpoint -> zero tail mass (no finite replacement)",
              ff(pick(tails, noise="logistic", tau_label="M_plus_1e-6")["alpha_H"]) == 0.0 and
              pick(tails, noise="logistic", normalized_distance="0.0")["x_star"] == "unattainable" if any(r["normalized_distance"] == "0.0" for r in tails) else True)
    L.require("T11", "Laplace tau = M: plateau tie rule alpha_H = 1/2, alpha_L = e^{-2/b}/2",
              abs(ff(pick(tails, noise="Laplace", normalized_distance="0.0")["alpha_H"]) - 0.5) < 1e-15 and
              abs(ff(pick(tails, noise="Laplace", normalized_distance="0.0")["alpha_L"]) - float(mp.exp(-2 / b) / 2)) < 1e-15)
    # scan a few tails rows independently (both laws)
    for noise in ("Laplace", "logistic"):
        for lab_ in ("benchmark", "M_minus_1e-4", "M_minus_1e-6"):
            rr = pick(tails, noise=noise, tau_label=lab_)
            tau = mp.mpf(rr["tau"])
            ee = Econ(**{**asdict(E_BASE), "noise": noise})
            cH = pay.g_L + tau * (pay.g_H - pay.g_L)
            ee2 = Econ(**{**asdict(ee), "c_H": mp.nstr(cH, 30)})
            cf2 = full_order_closed(ee2, pay)
            L.add("T11", f"{noise} tails row {lab_}: E", cf2["E"], ff(rr["E"]), 1e-8)


def t12_atomless(L: Ledger, objs: dict):
    for e in (ECONOMIES[1], ECONOMIES[3]):
        lab = f"{e.tag}/{e.noise}/{e.cost}"
        for rs in (BENCH["r_weak"], BENCH["r_strong"], BENCH["r_collapse"]):
            pay = pay_binary(e, rs)
            s = Sched(e, pay, 1.0, -1.0)
            eps = e.F("eps_C")
            # CDF checks at exact points
            for c, want in ((e.F("c_L") - eps, 0.0), (e.F("c_L"), e.F("rho") / 2), (e.F("c_L") + eps, e.F("rho")),
                            (e.F("c_H") - eps, e.F("rho")), (e.F("c_H"), e.F("rho") + (1 - e.F("rho")) / 2), (e.F("c_H") + eps, 1.0)):
                L.add("T12", f"{lab}: H_C({c:g})", float(s.H_C(c)), want, 1e-12)
            key = (lab, rs, "feedback", 1.0, -1.0)
            if key in objs:
                o = objs[key][1]
                L.add("T12", f"{lab}/r={rs}: flow-based vs cost-based e_H (mixture)", o["e_H"], o["e_H_cost_based"], TOL_FORMULA)
                L.add("T12", f"{lab}/r={rs}: flow-based vs cost-based e_L (mixture)", o["e_L"], o["e_L_cost_based"], TOL_FORMULA)
                # paid cost by a second route: integrate c * Pr(B(mu_X) >= c) dH_C(c) over the marginal law
                def tail_marg(c):
                    xc = s.crossing(c)
                    if xc == -np.inf:
                        return 1.0
                    if xc == np.inf:
                        return 0.0
                    return 0.5 * (float(survival(s.noise, xc - 1, s.b)) + float(survival(s.noise, xc + 1, s.b)))
                paid2 = 0.0
                for w, c0 in ((s.rho, s.cL), (1 - s.rho, s.cH)):
                    lo, hi = c0 - eps, c0 + eps
                    edges = sorted({lo, hi, *[float(v) for v in (s.B(s.mu(-200)), s.B(s.mu(200))) if lo < v < hi]})
                    for a, c in zip(edges[:-1], edges[1:]):
                        paid2 += w * integrate.quad(lambda cc: cc * tail_marg(cc), a, c, epsabs=QUAD_ABS, epsrel=QUAD_REL, limit=200)[0] / (2 * eps)
                L.add("T12", f"{lab}/r={rs}: paid cost flow route vs cost route", o["paid_cost"], paid2, TOL_FORMULA)
                naive = (e.F("rho") * e.F("c_L") + (1 - e.F("rho")) * e.F("c_H")) * o["E"]
                L.add("T12", f"{lab}/r={rs}: paid cost vs mean cost x entry (informational)", o["paid_cost"], naive, None,
                      required=False, passed=True, status="info", note=f"difference {o['paid_cost']-naive:+.6e}")
                atomic = e.F("rho") * e.F("c_L") + (1 - e.F("rho")) * e.F("c_H") * (o["E"] - e.F("rho")) / (1 - e.F("rho"))
                L.add("T12", f"{lab}/r={rs}: paid cost vs atomic formula (informational)", o["paid_cost"], atomic, None, required=False, passed=True,
                      status="info", note=f"difference {o['paid_cost']-atomic:+.6e}")


def t13_moderate(L: Ledger, scans: dict):
    e = E_MOD
    mv = read_csv("numerics/moderate_values.csv")
    row = pick(mv, h=MODER["h"], ell=MODER["ell"], p=MODER["p"], rho=MODER["rho"], c_L=MODER["c_L"], c_H=MODER["c_H"], b=MODER["b"], k=MODER["k"],
               r_weak=MODER["r_weak"], r_strong=MODER["r_strong"])
    pay0, pay1 = pay_binary(e, MODER["r_weak"]), pay_binary(e, MODER["r_strong"])
    z = theorem_margins(e, pay0, pay1)
    for nm, v in z.items():
        L.add("T13", f"moderate {nm} vs repo", v, ff(row[nm]), TOL_FORMULA)
        L.require("T13", f"moderate {nm} > 0 (strict)", v > 0, note=mp.nstr(v, 12))
    L.require("T13", "moderate support p < ell < r_weak < r_strong < h", e.M("p") < e.M("ell") < mp.mpf(MODER["r_weak"]) < mp.mpf(MODER["r_strong"]) < e.M("h"))
    L.require("T13", "moderate c_L < c_H", e.M("c_L") < e.M("c_H"))
    cf = full_order_closed(e, pay1)
    L.add("T13", "moderate E_strong closed form vs repo", cf["E"], ff(row["E_strong"]), TOL_FORMULA)
    L.add("T13", "moderate E_strong vs landmark", cf["E"], Decimal(LANDMARKS["moderate_strong_prep"][0]), DISPLAY_TOL)
    L.add("T13", "moderate O_H_strong closed form vs repo", cf["O_H"], ff(row["O_H_strong"]), TOL_FORMULA)
    L.add("T13", "moderate E_weak = rho", e.M("rho"), ff(row["E_weak"]), TOL_FORMULA)
    L.add("T13", "moderate O_H_weak = rho/2", e.M("rho") / 2, ff(row["O_H_weak"]), TOL_FORMULA)
    s1 = Sched(e, pay1, 1.0, -1.0)
    o1 = objects(s1)
    L.add("T13", "moderate strong E quadrature vs closed form", o1["E"], cf["E"], TOL_FORMULA)
    L.add("T13", "moderate strong E[P] = R_T", o1["mean_price"], o1["R_T"], TOL_PROB)
    for key in (("moderate", MODER["r_strong"], "full"), ("moderate", MODER["r_weak"], "pooling")):
        sc = scans.get(key)
        if sc:
            gain = max(sc["H"]["max_gain"], sc["L"]["max_gain"])
            L.add("T13", f"moderate {key[2]} at r={key[1]}: max unilateral gain", gain, 0.0, TOL_DEV, passed=gain <= TOL_DEV,
                  budget={st: sc[st]["budget"] for st in "HL"})


# ---------------------------------------------------------------------------------------
# complementary signals (A.7)
# ---------------------------------------------------------------------------------------
class SigSched:
    def __init__(self, e: Econ, pay: Pay, a: str, d: str, q_plus: float, q_minus: float):
        self.e, self.pay, self.pf = e, pay, pay.floats()
        self.a, self.d = float(Decimal(a)), float(Decimal(d))
        self.qp, self.qm = float(q_plus), float(q_minus)
        self.b, self.rho, self.cL, self.cH, self.k = e.F("b"), e.F("rho"), e.F("c_L"), e.F("c_H"), e.F("k")
        self.noise = e.noise
        self.breakpoints = self._bps()

    def fp(self, x):
        return pdf(self.noise, np.asarray(x, float) - self.qp, self.b)

    def fm(self, x):
        return pdf(self.noise, np.asarray(x, float) - self.qm, self.b)

    def lam(self, x):
        x = np.asarray(x, float)
        return expit(logpdf(self.noise, x - self.qp, self.b) - logpdf(self.noise, x - self.qm, self.b))

    def mu(self, x):
        return (1 - self.a) + (2 * self.a - 1) * self.lam(x)

    def phi(self, mu, y):
        mu = np.asarray(mu, float)
        return self.d * mu / (self.d * mu + (1 - self.d) * (1 - mu)) if y == "+" else (1 - self.d) * mu / ((1 - self.d) * mu + self.d * (1 - mu))

    def B(self, mu):
        return self.pf["g_L"] + np.asarray(mu, float) * (self.pf["g_H"] - self.pf["g_L"])

    def e_y(self, x, y):
        """Entry probability of the buyer with private signal y at flow x (both cost types)."""
        Bj = self.B(self.phi(self.mu(x), y))
        return self.rho * (Bj >= self.cL) + (1 - self.rho) * (Bj >= self.cH)

    def e_state(self, x, theta):
        pyp = self.d if theta == "H" else 1 - self.d
        return pyp * self.e_y(x, "+") + (1 - pyp) * self.e_y(x, "-")

    def price_OA35(self, x):
        mu = self.mu(x)
        return self.pf["t_0"] + mu * self.e_state(x, "H") * self.pf["w_H"] + (1 - mu) * self.e_state(x, "L") * self.pf["w_L"]

    def joint_terms(self, x):
        """List of (prob weight * density, theta, y) over the finite states (Theta, T, Y) at flow x."""
        out = []
        for theta, pth in (("H", 0.5), ("L", 0.5)):
            pt = self.a if theta == "H" else 1 - self.a
            py = self.d if theta == "H" else 1 - self.d
            for t, ptv, dens in (("+", pt, self.fp(x)), ("-", 1 - pt, self.fm(x))):
                for y, pyv in (("+", py), ("-", 1 - py)):
                    out.append((pth * ptv * pyv * dens, theta, t, y))
        return out

    def price_direct(self, x):
        """E[V_T | X = x] summing over the joint law of (Theta, T, Y)."""
        num, den = 0.0, 0.0
        for wgt, theta, t, y in self.joint_terms(x):
            w = self.pf["w_H"] if theta == "H" else self.pf["w_L"]
            num = num + wgt * (self.pf["t_0"] + self.e_y(x, y) * w)
            den = den + wgt
        return num / den

    def post_direct(self, x, y):
        """Pr(H | X = x, Y = y) from the joint likelihood."""
        num, den = 0.0, 0.0
        for wgt, theta, t, yy in self.joint_terms(x):
            if yy != y:
                continue
            den = den + wgt
            if theta == "H":
                num = num + wgt
        return num / den

    def A(self, x, sig):
        """Residual for the trader with signal sig in {'+','-'}: E[V_T | T, x] - P (sign so that correctly signed orders gain)."""
        pH = self.a if sig == "+" else 1 - self.a
        EV = self.pf["t_0"] + pH * self.e_state(x, "H") * self.pf["w_H"] + (1 - pH) * self.e_state(x, "L") * self.pf["w_L"]
        P = self.price_OA35(x)
        return (EV - P) if sig == "+" else (P - EV)

    def A_formula(self, x, sig):
        lam = self.lam(x)
        D = self.e_state(x, "H") * self.pf["w_H"] - self.e_state(x, "L") * self.pf["w_L"]
        return (2 * self.a - 1) * ((1 - lam) if sig == "+" else lam) * D

    def lam_required(self, y):
        tau = float(self.pay.tau(self.e.M("c_H")))
        if tau <= 0:
            return -np.inf
        if tau >= 1:
            return np.inf
        d = self.d
        mu_req = tau * (1 - d) / (d * (1 - tau) + tau * (1 - d)) if y == "+" else tau * d / ((1 - d) * (1 - tau) + tau * d)
        return (mu_req - (1 - self.a)) / (2 * self.a - 1)

    def x_star(self, y):
        """Flow cutoff for private signal y under full Laplace orders (OA.39), with always/never/tie handling."""
        lr = self.lam_required(y)
        m = 1 / (1 + math.exp((self.qp - self.qm) / self.b)) if self.qp != self.qm else 0.5
        M = 1 - m
        if self.qp == self.qm:
            return -np.inf if lr <= 0.5 else np.inf
        if lr <= m:
            return -np.inf
        if lr > M:
            return np.inf
        if lr == M:
            return self.qp
        return float(optimize.brentq(lambda x: float(self.lam(x)) - lr, self.qm, self.qp, xtol=1e-15, rtol=8.9e-16))

    def _bps(self):
        pts = {self.qp, self.qm}
        for y in "+-":
            xs = self.x_star(y)
            if np.isfinite(xs):
                pts.add(xs)
        # low-cost boundaries too (should be 'always' under the theorem margins, but handled generically)
        return tuple(sorted(pts))


def sig_closed(ss: SigSched) -> dict:
    """OA.39-OA.41 closed forms with Laplace survival."""
    a, d, rho = ss.a, ss.d, ss.rho
    Q = {}
    xs = {}
    for y in "+-":
        x = ss.x_star(y)
        xs[y] = x
        if x == -np.inf:
            qp = qm = 1.0
        elif x == np.inf:
            qp = qm = 0.0
        else:
            qp = float(survival(ss.noise, x - ss.qp, ss.b))
            qm = float(survival(ss.noise, x - ss.qm, ss.b))
        Q[("H", y)] = a * qp + (1 - a) * qm
        Q[("L", y)] = (1 - a) * qp + a * qm
    eH = rho + (1 - rho) * (d * Q[("H", "+")] + (1 - d) * Q[("H", "-")])
    eL = rho + (1 - rho) * ((1 - d) * Q[("L", "+")] + d * Q[("L", "-")])
    return {"e_H": eH, "e_L": eL, "E": 0.5 * (eH + eL), "O_H": 0.5 * eH,
            "R_T": ss.pf["t_0"] + 0.5 * (eH * ss.pf["w_H"] + eL * ss.pf["w_L"]), "x_star_Yplus": xs["+"], "x_star_Yminus": xs["-"]}


def sig_objects(ss: SigSched) -> dict:
    """Direct integration over the joint law of (Theta, T, Y, Z) and identity checks."""
    bp = ss.breakpoints
    ql = lambda fun: quad_line(fun, bp, noise=ss.noise, b=ss.b)
    eH, _ = ql(lambda x: (ss.a * ss.fp(x) + (1 - ss.a) * ss.fm(x)) * ss.e_state(x, "H"))
    eL, _ = ql(lambda x: ((1 - ss.a) * ss.fp(x) + ss.a * ss.fm(x)) * ss.e_state(x, "L"))
    g = lambda x: 0.5 * (ss.fp(x) + ss.fm(x))
    intp, _ = ql(lambda x: ss.fp(x))
    Emu, _ = ql(lambda x: g(x) * ss.mu(x))
    EP, _ = ql(lambda x: g(x) * ss.price_direct(x))
    R_T = ss.pf["t_0"] + 0.5 * (eH * ss.pf["w_H"] + eL * ss.pf["w_L"])
    lo, hi = min(bp) - 40 * ss.b, max(bp) + 40 * ss.b
    xs = np.unique(np.concatenate([np.linspace(lo, hi, 8001), np.array(bp)]))
    price_err = float(np.max(np.abs(ss.price_direct(xs) - ss.price_OA35(xs))))
    post_err = max(float(np.max(np.abs(ss.post_direct(xs, y) - ss.phi(ss.mu(xs), y)))) for y in "+-")
    res_err = max(float(np.max(np.abs(ss.A(xs, sg) - ss.A_formula(xs, sg)))) for sg in "+-")
    # joint-law structure: Theta independent of X given T; Y independent of X given Theta
    condH_given_Tplus = []
    for x in xs[::400]:
        terms = ss.joint_terms(x)
        num = sum(w for w, th, t, y in terms if t == "+" and th == "H")
        den = sum(w for w, th, t, y in terms if t == "+")
        condH_given_Tplus.append(num / den)
    theta_indep = float(np.max(np.abs(np.array(condH_given_Tplus) - ss.a)))
    y_given_theta = []
    for x in xs[::400]:
        terms = ss.joint_terms(x)
        num = sum(w for w, th, t, y in terms if th == "H" and y == "+")
        den = sum(w for w, th, t, y in terms if th == "H")
        y_given_theta.append(num / den)
    y_indep = float(np.max(np.abs(np.array(y_given_theta) - ss.d)))
    eHx, eLx = ss.e_state(xs, "H"), ss.e_state(xs, "L")
    D = eHx * ss.pf["w_H"] - eLx * ss.pf["w_L"]
    order_ok = bool(np.all(eHx >= eLx - 1e-15) and np.all(eLx >= ss.rho - 1e-15))
    D_ok = bool(np.all(D >= ss.rho * ss.pf["Delta"] - 1e-12))
    # price inversion: recover mu from P on the positive-D image (P strictly increasing in mu, OA.36)
    inv_err = 0.0
    sub = xs[::200]
    def Pmu(mu):  # OA.35 as a function of the public posterior alone
        eH = ss.d * ss.e_y_mu(mu, "+") + (1 - ss.d) * ss.e_y_mu(mu, "-")
        eL = (1 - ss.d) * ss.e_y_mu(mu, "+") + ss.d * ss.e_y_mu(mu, "-")
        return ss.pf["t_0"] + mu * eH * ss.pf["w_H"] + (1 - mu) * eL * ss.pf["w_L"]
    for x in sub:
        P_obs = float(ss.price_OA35(x))
        lo_, hi_ = 0.0, 1.0
        for _ in range(200):
            mid = 0.5 * (lo_ + hi_)
            if Pmu(mid) <= P_obs:
                lo_ = mid
            else:
                hi_ = mid
        mu_rec = 0.5 * (lo_ + hi_)
        inv_err = max(inv_err, abs(mu_rec - float(ss.mu(x))))
        # update with Y and compare with the direct joint likelihood
        for y in "+-":
            inv_err = max(inv_err, abs(float(ss.phi(mu_rec, y)) - float(ss.post_direct(x, y))))
    return {"e_H": eH, "e_L": eL, "E": 0.5 * (eH + eL), "O_H": 0.5 * eH, "R_T": R_T, "int_fp": intp, "E_mu": Emu, "mean_price": EP,
            "price_err": price_err, "posterior_err": post_err, "residual_err": res_err, "theta_indep_err": theta_indep,
            "y_indep_err": y_indep, "entry_order_ok": order_ok, "D_bound_ok": D_ok, "inversion_err": inv_err}


def _e_y_mu(self, mu, y):
    Bj = self.B(self.phi(mu, y))
    return self.rho * (Bj >= self.cL) + (1 - self.rho) * (Bj >= self.cH)


SigSched.e_y_mu = _e_y_mu


def U_sig(ss: SigSched, sig: str, q: float):
    if q == 0.0:
        return 0.0, 0.0
    eps = 1.0 if sig == "+" else -1.0
    val, err = quad_line(lambda x: pdf(ss.noise, x - q, ss.b) * ss.A(x, sig), ss.breakpoints, extra=[q], noise=ss.noise, b=ss.b)
    return q * eps * val - ss.k * abs(q), abs(q) * err


def sig_scan(spec: dict) -> dict:
    ss = SigSched(E_SIG, pay_binary(E_SIG, spec["r"]), spec["a"], spec["d"], spec["q_plus"], spec["q_minus"])
    n = ORDER_INTERVALS
    grid = list(np.linspace(-1, 1, n + 1))
    extra = [v for y in "+-" for v in (ss.x_star(y), -ss.x_star(y)) if np.isfinite(v)] + [ss.qp, ss.qm, -ss.qp, -ss.qm]
    qs = sorted(set(grid + [float(x) for x in extra if -1 <= x <= 1]))
    out = {}
    A_bar = (2 * ss.a - 1) * (ss.pf["Delta"] + (1 - ss.rho) * (2 * ss.d - 1) * ss.pf["w_H"])
    for sig, q_own in (("+", ss.qp), ("-", ss.qm)):
        base, base_err = U_sig(ss, sig, q_own)
        best, bq, qerr = -np.inf, None, 0.0
        for q in qs:
            u, e_ = U_sig(ss, sig, q)
            if u - base > best:
                best, bq = u - base, q
            qerr = max(qerr, e_ + base_err)
        h = 2.0 / n
        out[sig] = {"max_gain": best, "argmax_q": bq, "candidate_payoff": base,
                    "budget": {"quadrature": qerr, "tail_truncation": A_bar * tail_mass_bound(ss.noise, ss.b), "between_grid_first_order": (A_bar * (1 + 1 / ss.b) + ss.k) * h / 2,
                               "between_grid_second_order": (2 * A_bar / ss.b + A_bar / ss.b ** 2) * h * h / 8, "order_intervals": n}}
    return {"spec": spec, "scan": out}


def t14_t15_signals(L: Ledger, sig_scans: dict):
    rows = read_csv("numerics/two_signals.csv")
    A_grid = ["0.68", "0.69", "0.70", "0.71", "0.72"]
    D_grid = ["0.73", "0.74", "0.75", "0.76", "0.77"]
    # T15 completeness
    pairs = sorted({(r["a"], r["d"]) for r in rows})
    L.require("T15", "all 25 accuracy pairs present in numerics/two_signals.csv", set(pairs) == {(a, d) for a in A_grid for d in D_grid},
              note=f"{len(pairs)} pairs")
    L.require("T15", "declared example (0.70, 0.75) present", ("0.70", "0.75") in pairs)
    neg = [r for r in rows if any(ff(r[c]) < 0 for c in ("low_cost_margin", "private_only_exclusion_margin", "joint_entry_margin", "weak_order_margin", "strong_order_margin"))]
    L.require("T15", "rows with a negative theorem margin are retained (not dropped)", len(neg) > 0, note=f"{len(neg)} rows with a negative margin retained")
    for a in A_grid:
        for d in D_grid:
            for rs in (SIGN["r_weak"], SIGN["r_strong"]):
                hits = [r for r in rows if r["a"] == a and r["d"] == d and r["r"] == rs]
                L.require("T15", f"grid (a={a}, d={d}, r={rs}): both order profiles retained", {(h["q_plus"], h["q_minus"]) for h in hits} == {("0.0", "0.0"), ("1.0", "-1.0")},
                          note=str([(h["q_plus"], h["q_minus"], h["status"][:40]) for h in hits]))
    # analytical margins (OA.29) per pair
    pay0, pay1 = pay_binary(E_SIG, SIGN["r_weak"]), pay_binary(E_SIG, SIGN["r_strong"])
    b, rho, k = E_SIG.M("b"), E_SIG.M("rho"), E_SIG.M("k")
    m, M = posterior_bounds_mp(b)
    for a in A_grid:
        for d in D_grid:
            am, dm = mp.mpf(a), mp.mpf(d)
            mu_m = (1 - am) + (2 * am - 1) * m
            mu_p = (1 - am) + (2 * am - 1) * M
            phim = (1 - dm) * mu_m / ((1 - dm) * mu_m + dm * (1 - mu_m))
            phip = dm * mu_p / (dm * mu_p + (1 - dm) * (1 - mu_p))
            marg = {"low_cost_margin": pay1.B(phim) - E_SIG.M("c_L"), "private_only_exclusion_margin": E_SIG.M("c_H") - pay0.B(dm),
                    "joint_entry_margin": pay1.B(phip) - E_SIG.M("c_H"),
                    "weak_order_margin": k - (2 * am - 1) * (pay0.Delta + (1 - rho) * (2 * dm - 1) * pay0.w_H),
                    "strong_order_margin": (1 - 1 / b) * m * (2 * am - 1) * rho * pay1.Delta - k}
            for rs in (SIGN["r_weak"], SIGN["r_strong"]):
                for qp, qm in (("0.0", "0.0"), ("1.0", "-1.0")):
                    row = pick(rows, a=a, d=d, r=rs, q_plus=qp, q_minus=qm)
                    lab = f"signal a={a} d={d} r={rs} ({qp},{qm})"
                    L.add("T14", f"{lab}: mu_lower", mu_m, ff(row["mu_lower"]), TOL_FORMULA)
                    L.add("T14", f"{lab}: mu_upper", mu_p, ff(row["mu_upper"]), TOL_FORMULA)
                    L.add("T14", f"{lab}: phi_-(mu_lower)", phim, ff(row["phi_minus_mu_lower"]), TOL_FORMULA)
                    L.add("T14", f"{lab}: phi_+(mu_upper)", phip, ff(row["phi_plus_mu_upper"]), TOL_FORMULA)
                    for nm, v in marg.items():
                        L.add("T14", f"{lab}: {nm}", v, ff(row[nm]), TOL_FORMULA)
                    ss = SigSched(E_SIG, pay_binary(E_SIG, rs), a, d, ff(qp), ff(qm))
                    cf = sig_closed(ss)
                    o = sig_objects(ss)
                    for nm in ("e_H", "e_L", "E", "O_H", "R_T"):
                        L.add("T14", f"{lab}: {nm} joint-law integration vs OA.41 closed form", o[nm], cf[nm], TOL_FORMULA)
                        L.add("T14", f"{lab}: {nm} vs repo", cf[nm], ff(row[nm]), TOL_FORMULA)
                    for y, col in (("+", "x_star_Yplus"), ("-", "x_star_Yminus")):
                        rv = row[col]
                        if rv == "n/a":
                            L.require("T14", f"{lab}: {col} n/a only for uninformative orders", qp == qm)
                        else:
                            L.add("T14", f"{lab}: {col}", cf[col], (float("inf") if rv == "inf" else -float("inf") if rv == "-inf" else ff(rv)), 1e-9)
                    L.add("T14", f"{lab}: int f_+ = 1", o["int_fp"], 1.0, TOL_PROB)
                    L.add("T14", f"{lab}: E[mu_X] = 1/2", o["E_mu"], 0.5, TOL_PROB)
                    L.add("T14", f"{lab}: E[P] = R_T", o["mean_price"], o["R_T"], TOL_PROB)
                    L.add("T14", f"{lab}: price direct conditional expectation vs OA.35", o["price_err"], 0.0, TOL_PRICE)
                    L.add("T14", f"{lab}: joint posterior phi_y(mu_P) vs direct likelihood", o["posterior_err"], 0.0, TOL_PRICE)
                    L.add("T14", f"{lab}: residuals direct vs OA.37", o["residual_err"], 0.0, TOL_PRICE)
                    L.add("T14", f"{lab}: Theta independent of X given T (Pr(H|T=+,x) = a)", o["theta_indep_err"], 0.0, 1e-12)
                    L.add("T14", f"{lab}: Y independent of X given Theta (Pr(Y=+|H,x) = d)", o["y_indep_err"], 0.0, 1e-12)
                    L.require("T14", f"{lab}: e_H >= e_L >= rho pointwise", o["entry_order_ok"])
                    L.require("T14", f"{lab}: D = e_H w_H - e_L w_L >= rho Delta_T pointwise", o["D_bound_ok"])
                    L.add("T14", f"{lab}: price inversion then Y-update vs direct joint posterior", o["inversion_err"], 0.0, 1e-7)
                    L.add("T14", f"{lab}: posterior_error repo column", ff(row["posterior_error"]), 0.0, TOL_PRICE, required=False)
                    sc = sig_scans.get((a, d, rs, qp, qm))
                    if sc:
                        gain = max(sc["+"]["max_gain"], sc["-"]["max_gain"])
                        accepted = row["accepted"].lower() == "true"
                        bud = {sg: sc[sg]["budget"] for sg in "+-"}
                        if accepted:
                            L.add("T14", f"{lab}: max unilateral gain (accepted row)", gain, 0.0, TOL_DEV, passed=gain <= TOL_DEV, budget=bud,
                                  note=f"argmax + q={sc['+']['argmax_q']}, - q={sc['-']['argmax_q']}")
                        else:
                            m_ = re.search(r"epsilon_q=([0-9.e+-]+)", row["status"])
                            L.add("T14", f"{lab}: max unilateral gain (rejected row)", gain, ff(m_.group(1)) if m_ else None, 5e-4 if m_ else None,
                                  budget=bud, note=row["status"][:80], required=False)
                            L.require("T14", f"{lab}: rejected row has a profitable deviation", gain > TOL_DEV, note=f"gain={gain:.3e}")
    # declared example landmark
    ss = SigSched(E_SIG, pay1, SIGN["a"], SIGN["d"], 1.0, -1.0)
    cf = sig_closed(ss)
    L.add("T14", "complementary strong preparation vs landmark", cf["E"], Decimal(LANDMARKS["complementary_strong_prep"][0]), DISPLAY_TOL)


# ---------------------------------------------------------------------------------------
# reserve comparisons (C.6 declared rows) with E, A, S, C2
# ---------------------------------------------------------------------------------------
def reserve_rows(L: Ledger, scans: dict):
    rc = read_csv("tables/reserve_comparisons.csv")
    e = E_BASE
    epsV = mp.mpf(BENCH["value_band_halfwidth"])
    m, M = posterior_bounds_mp(e.M("b"))
    for law in ("binary", "uniform_classes"):
        reserves = (BENCH["p"], BENCH["binary_alternative_reserve"]) if law == "binary" else (BENCH["p"], BENCH["atomless_alternative_reserve"])
        for rs in (BENCH["r_weak"], BENCH["r_strong"]):
            for ps in reserves:
                row = pick(rc, value_law=law, r=rs, p=ps)
                pay = pay_binary(e, rs, ps) if law == "binary" else pay_class(e, rs, ps, epsV, integrate_direct=False)
                lab = f"reserve {law} r={rs} p={ps}"
                # entry floor and trading bounds with the actual floor e(m)
                e_m = float(Sched(e, pay, 1, -1).H_C(float(pay.B(m))))
                floor = pay.B(m) - e.M("c_L")
                no_trade = e.M("k") - pay.Delta
                full = (1 - 1 / e.M("b")) * mp.mpf(e_m) * m * pay.Delta - e.M("k")
                L.add("T03", f"{lab}: low_cost_floor_margin vs repo", floor, ff(row["low_cost_floor_margin"]), TOL_FORMULA)
                qH, qL = ff(row["q_H"]), ff(row["q_L"])
                if (qH, qL) == (0.0, 0.0):
                    L.require("T03", f"{lab}: pooling row supported by k - Delta_T > 0", no_trade > 0, note=mp.nstr(no_trade, 10))
                    L.add("T03", f"{lab}: trading_margin vs repo (k - Delta_T)", no_trade, ff(row["trading_margin"]), TOL_FORMULA)
                else:
                    L.require("T03", f"{lab}: full-order row supported by (1-1/b) e(m) m Delta_T - k > 0 and floor > 0", full > 0 and floor > 0, note=mp.nstr(full, 10))
                    L.add("T03", f"{lab}: trading_margin vs repo", full, ff(row["trading_margin"]), TOL_FORMULA)
                s = Sched(e, pay, qH, qL)
                o = objects(s)
                for a in ("e_H", "e_L", "E", "R_T"):
                    L.add("T03", f"{lab}: {a} vs repo", o[a], ff(row[a]), TOL_FORMULA)
                L.add("T03", f"{lab}: E[P] = R_T", o["mean_price"], o["R_T"], TOL_PROB)
                L.add("T03", f"{lab}: sup|P - E[V_T|x]|", o["eps_P"], 0.0, TOL_PRICE)
                # E, A, S, C2 (spec 9.5) and high-value ownership from the allocation event
                p_, r_ = mp.mpf(ps), mp.mpf(rs)
                if law == "binary":
                    prH, prL = (mp.mpf(1) if e.M("h") >= p_ else mp.mpf(0)), (mp.mpf(1) if e.M("ell") >= p_ else mp.mpf(0))
                    # Pr(high class value beats reserve and incumbent): h > r in the benchmark support
                    winH = mp.mpf(1) if e.M("h") > max(p_, r_) else None
                else:
                    def band_prob(c):
                        lo, hi = c - epsV, c + epsV
                        return min(max((hi - p_) / (hi - lo), 0), 1)
                    prH, prL = band_prob(e.M("h")), band_prob(e.M("ell"))
                    winH = mp.mpf(1) if e.M("h") - epsV > max(p_, r_) else None
                E_ = mp.mpf(o["E"])
                A_ = (mp.mpf(o["e_H"]) * prH + mp.mpf(o["e_L"]) * prL) / 2
                PR = max(1 - p_ / r_, 0) if p_ <= r_ else mp.mpf(0)
                C2 = PR * A_
                S = PR + A_ - C2
                L.require("T03", f"{lab}: 0 <= C2 <= A <= E <= 1 and 0 <= S <= 1", 0 <= C2 <= A_ <= E_ <= 1 and 0 <= S <= 1,
                          note=f"E={mp.nstr(E_,10)}, A={mp.nstr(A_,10)}, S={mp.nstr(S,10)}, C2={mp.nstr(C2,10)}, Pr(R>=p)={mp.nstr(PR,10)}")
                L.add("T03", f"{lab}: S = Pr(R>=p) + A - C2 (identity)", S, PR + A_ - C2, 1e-30)
                for nm, v in (("E", E_), ("A", A_), ("S", S), ("C2", C2), ("Pr(R>=p)", PR), ("O_H", (mp.mpf(o["e_H"]) * winH / 2) if winH is not None else None)):
                    L.add("T03", f"{lab}: {nm}", v, None, status="info", note="spec 9.5 event probabilities (not in repo tables)", required=False)
                sc = scans.get(("reserve", law, rs, ps))
                if sc:
                    gain = max(sc["H"]["max_gain"], sc["L"]["max_gain"])
                    L.add("T07", f"{lab}: max unilateral gain", gain, 0.0, TOL_DEV, passed=gain <= TOL_DEV, budget={st: sc[st]["budget"] for st in "HL"})


# ---------------------------------------------------------------------------------------
# thresholds (A.5) and registry landmarks
# ---------------------------------------------------------------------------------------
def thresholds(L: Ledger):
    e = E_BASE
    th = read_csv("numerics/thresholds.csv")
    reg = read_csv("numerics/quantity_registry.csv")
    ell, k, rho, b, cH, h, p = (e.M(n) for n in ("ell", "k", "rho", "b", "c_H", "h", "p"))
    m, M = posterior_bounds_mp(b)
    frak = lambda d: ell + d + mp.sqrt(d * d + 2 * ell * d)
    Delta = lambda r: (r - ell) ** 2 / (2 * r)
    vals = {"pooling_unique_sufficient": frak(k), "pooling_existence": frak(2 * k / rho),
            "full_orders_unique_sufficient": frak(k / ((1 - 1 / b) * rho * m))}
    L.add("thresholds", "frak_r(k): Delta_T(frak_r(k)) = k residual", Delta(vals["pooling_unique_sufficient"]) - k, 0.0, 1e-30)
    L.add("thresholds", "r_N: rho Delta_T/2 = k residual", rho * Delta(vals["pooling_existence"]) / 2 - k, 0.0, 1e-30)
    L.add("thresholds", "r_U: (1-1/b) rho m Delta_T = k residual", (1 - 1 / b) * rho * m * Delta(vals["full_orders_unique_sufficient"]) - k, 0.0, 1e-30)
    disc = (M * h - cH) ** 2 + M * ((1 - M) * ell * ell - p * p)
    L.require("thresholds", "r_C discriminant nonnegative", disc >= 0, note=mp.nstr(disc, 10))
    rC = ((M * h - cH) + mp.sqrt(disc)) / M
    vals["high_cost_ceiling"] = rC
    payC = pay_binary(e, rC)
    L.add("thresholds", "r_C: B_r(M) - c_H residual", payC.B(M) - cH, 0.0, 1e-30)
    L.add("thresholds", "r_C: OA.20 quadratic residual", M * rC ** 2 - 2 * (M * h - cH) * rC - ((1 - M) * ell * ell - p * p), 0.0, 1e-28)
    # the other algebraic root is outside the strictly decreasing domain
    rC2 = ((M * h - cH) - mp.sqrt(disc)) / M
    L.require("thresholds", "r_C other root outside (ell, h) domain", not (ell < rC2 < h), note=mp.nstr(rC2, 10))
    for nm, v in vals.items():
        row = pick(th, boundary=nm)
        L.add("thresholds", f"{nm} vs repo thresholds.csv", v, ff(row["value"]), 1e-12)
        pay = pay_binary(e, v)
        L.require("thresholds", f"{nm} in support and maintained domain (c_L < B(m), B(1/2) < c_H)",
                  ell < v < h and e.M("c_L") < pay.B(m) and pay.B(mp.mpf(1) / 2) < cH)
    L.add("thresholds", "m vs repo", m, ff(pick(th, boundary="m")["value"]), 1e-15)
    L.add("thresholds", "M vs repo", M, ff(pick(th, boundary="M")["value"]), 1e-15)
    left = rho + (1 - rho) * (1 + mp.exp(-2 / b)) / 4
    L.add("thresholds", "Laplace entry left limit (OA.21) vs repo", left, ff(pick(th, boundary="laplace_entry_left_limit")["value"]), 1e-15)
    L.require("thresholds", "ordering frak_r(k) < r_N < r_U < r_C", vals["pooling_unique_sufficient"] < vals["pooling_existence"] < vals["full_orders_unique_sufficient"] < vals["high_cost_ceiling"])
    L.require("thresholds", "benchmark strengths straddle: r_weak < frak_r(k), r_U < r_strong < r_C < r_collapse",
              mp.mpf(BENCH["r_weak"]) < vals["pooling_unique_sufficient"] and vals["full_orders_unique_sufficient"] < mp.mpf(BENCH["r_strong"]) < vals["high_cost_ceiling"] < mp.mpf(BENCH["r_collapse"]))
    regv = {r["name"]: r for r in reg}
    for key, v in (("base_r_pool_unique_sufficient", vals["pooling_unique_sufficient"]), ("base_r_no_trade_exact", vals["pooling_existence"]),
                   ("base_r_full_unique_sufficient", vals["full_orders_unique_sufficient"]), ("base_r_high_cost_ceiling", rC),
                   ("base_m", m), ("base_M", M), ("base_laplace_entry_ceiling_left_limit", left)):
        L.add("thresholds", f"registry {key}", v, ff(regv[key]["value"]), 1e-12)
    # logistic threshold registry values
    el = ECONOMIES[2]
    cf = full_order_closed(el, pay_binary(el, BENCH["r_strong"]))
    L.add("thresholds", "registry logistic_flow_threshold", cf["x_star"], ff(regv["logistic_flow_threshold"]["value"]), 1e-9)
    L.add("thresholds", "registry logistic_threshold_noise_sd", cf["x_star"] / (el.M("b") * mp.pi / mp.sqrt(3)), ff(regv["logistic_threshold_noise_sd"]["value"]), 1e-9)
    # landmarks from the registry and repo tables
    ctrl = read_csv("tables/equilibrium_controls.csv")
    fb = read_csv("numerics/feedback_comparisons.csv")
    cf_s = full_order_closed(E_BASE, pay_binary(E_BASE, BENCH["r_strong"]))
    land = {"strong_preparation": cf_s["E"], "strong_high_value_ownership": cf_s["O_H"], "strong_target_proceeds": cf_s["R_T"],
            "frozen_prep_weak": full_order_closed(E_BASE, pay_binary(E_BASE, BENCH["r_weak"]))["E"],
            "strong_hidden_proceeds": pay_binary(E_BASE, BENCH["r_strong"]).t_0 + rho * (pay_binary(E_BASE, BENCH["r_strong"]).w_H + pay_binary(E_BASE, BENCH["r_strong"]).w_L) / 2,
            "logistic_strong_prep": full_order_closed(ECONOMIES[2], pay_binary(E_BASE, BENCH["r_strong"]))["E"],
            "moderate_strong_prep": full_order_closed(E_MOD, pay_binary(E_MOD, MODER["r_strong"]))["E"]}
    for key, v in land.items():
        L.add("landmark", f"{key} ({LANDMARKS[key][1]})", v, Decimal(LANDMARKS[key][0]), DISPLAY_TOL)
    for key, rowkey in (("atomless_laplace_strong_prep", ("Laplace", "uniform_mixture")), ("atomless_logistic_strong_prep", ("logistic", "uniform_mixture"))):
        row = pick(ctrl, parameter_set="base", noise=rowkey[0], cost_law=rowkey[1], r=BENCH["r_strong"], experiment="feedback", q_H="1.0")
        L.add("landmark", f"{key} repo table vs landmark (independent value checked in T04)", ff(row["E"]), Decimal(LANDMARKS[key][0]), DISPLAY_TOL)
    frow = pick(fb, parameter_set="base", noise="Laplace", cost_law="atoms", r=BENCH["r_strong"])
    L.add("landmark", "net_surplus_gain repo vs landmark (independent value checked in T10)", ff(frow["W_gain"]), Decimal(LANDMARKS["net_surplus_gain"][0]), DISPLAY_TOL)
    return land


# ---------------------------------------------------------------------------------------
# driver
# ---------------------------------------------------------------------------------------
def run_scans(specs: list[dict], fn, workers: int) -> list[dict]:
    with ProcessPoolExecutor(max_workers=workers) as ex:
        return list(ex.map(fn, specs, chunksize=1))


def main() -> int:
    L = Ledger()
    t0 = time.time()
    print("T02/T03 auction layer ...", flush=True)
    t02_t03_auction(L)
    print("thresholds ...", flush=True)
    land = thresholds(L)
    # scans (parallel)
    workers = max(1, min(8, (os.cpu_count() or 2) - 1))
    bench_specs = []
    for sp in benchmark_candidates():
        d = {k: v for k, v in sp.items() if k != "row"}
        bench_specs.append(d)
    # moderate and reserve candidates
    extra_specs = [{"econ": asdict(E_MOD), "r": MODER["r_strong"], "q_H": 1.0, "q_L": -1.0, "experiment": "moderate_full"},
                   {"econ": asdict(E_MOD), "r": MODER["r_weak"], "q_H": 0.0, "q_L": 0.0, "experiment": "moderate_pooling"}]
    rc = read_csv("tables/reserve_comparisons.csv")
    for row in rc:
        if row["value_law"] == "binary":
            extra_specs.append({"econ": asdict(E_BASE), "r": row["r"], "p": row["p"], "q_H": ff(row["q_H"]), "q_L": ff(row["q_L"]),
                                "experiment": f"reserve_binary"})
    print(f"T07 order scans: {len(bench_specs) + len(extra_specs)} benchmark-type schedules on {workers} workers ...", flush=True)
    res = run_scans(bench_specs + extra_specs, deviation_scan, workers)
    scans = {}
    for r in res:
        sp = r["spec"]
        if sp["experiment"] in ("moderate_full", "moderate_pooling"):
            scans[("moderate", sp["r"], "full" if sp["q_H"] == 1.0 else "pooling")] = r["scan"]
        elif sp["experiment"] == "reserve_binary":
            scans[("reserve", "binary", sp["r"], sp["p"])] = r["scan"]
        else:
            scans[(econ_label(sp["econ"]), sp["r"], sp["experiment"], sp["q_H"], sp["q_L"])] = r["scan"]
    # class-economy reserve rows need the class payoffs: run them serially with the class Pay
    class_specs = []
    for row in rc:
        if row["value_law"] == "uniform_classes":
            class_specs.append(row)
    print(f"T07 class-economy reserve scans: {len(class_specs)} ...", flush=True)
    for row in class_specs:
        pay = pay_class(E_BASE, row["r"], row["p"], BENCH["value_band_halfwidth"], integrate_direct=False)
        s = Sched(E_BASE, pay, ff(row["q_H"]), ff(row["q_L"]))
        # reuse deviation_scan logic through a spec-less path
        scans[("reserve", "uniform_classes", row["r"], row["p"])] = _scan_sched(s)
    print(f"scans done at {time.time()-t0:.0f}s; T04-T10 objects ...", flush=True)
    objs = t04_t05_t06_t08_t09_t10(L, scans)
    print(f"T11 ... ({time.time()-t0:.0f}s)", flush=True)
    t11_logistic(L)
    t12_atomless(L, objs)
    t13_moderate(L, scans)
    print(f"reserve rows ... ({time.time()-t0:.0f}s)", flush=True)
    reserve_rows(L, scans)
    # signal scans
    sig_specs = []
    rows = read_csv("numerics/two_signals.csv")
    for row in rows:
        sig_specs.append({"a": row["a"], "d": row["d"], "r": row["r"], "q_plus": ff(row["q_plus"]), "q_minus": ff(row["q_minus"])})
    print(f"T14 signal scans: {len(sig_specs)} schedules ... ({time.time()-t0:.0f}s)", flush=True)
    sres = run_scans(sig_specs, sig_scan, workers)
    sig_scans = {(r["spec"]["a"], r["spec"]["d"], r["spec"]["r"], f"{r['spec']['q_plus']:.1f}", f"{r['spec']['q_minus']:.1f}"): r["scan"] for r in sres}
    print(f"T14/T15 signal objects ... ({time.time()-t0:.0f}s)", flush=True)
    t14_t15_signals(L, sig_scans)
    elapsed = time.time() - t0
    # summary
    summary = {}
    for r in L.rows:
        s = summary.setdefault(r["test"], {"pass": 0, "FAIL": 0, "info": 0, "open": 0, "required_fail": 0})
        s[r["status"] if r["status"] in s else "open"] += 1
        if r["status"] == "FAIL" and r["required"]:
            s["required_fail"] += 1
    out = {"generated": time.strftime("%Y-%m-%d %H:%M:%S"), "elapsed_seconds": elapsed,
           "environment": {"python": sys.version.split()[0], "numpy": np.__version__, "scipy": __import__("scipy").__version__, "mpmath": mp.__version__},
           "controls": {"quad_abs": QUAD_ABS, "quad_rel": QUAD_REL, "order_intervals": ORDER_INTERVALS, "tol_formula": TOL_FORMULA, "tol_prob": TOL_PROB,
                        "tol_price": TOL_PRICE, "tol_entry": TOL_ENTRY, "tol_dev": TOL_DEV, "mpmath_dps": mp.mp.dps},
           "declarations_parsed_from_C0": DECL, "summary": summary, "checks": L.rows}
    OUT_JSON.write_text(json.dumps(out, indent=1, default=str))
    write_summary(out)
    nfail = sum(s["required_fail"] for s in summary.values())
    print(json.dumps(summary, indent=1))
    print(f"total checks {len(L.rows)}; required failures {nfail}; elapsed {elapsed:.0f}s")
    return 1 if nfail else 0


def _scan_sched(s: Sched) -> dict:
    n = ORDER_INTERVALS
    grid = list(np.linspace(-1, 1, n + 1))
    xs = s.x_star()
    extra = [xs, -xs, s.q_H, s.q_L, -s.q_H, -s.q_L] if np.isfinite(xs) else [s.q_H, s.q_L, -s.q_H, -s.q_L]
    qs = sorted(set(grid + [float(x) for x in extra if -1 <= x <= 1]))
    out = {}
    for state, q_own in (("H", s.q_H), ("L", s.q_L)):
        base, base_err, _ = U_order(s, state, q_own)
        best, bq, qerr = -np.inf, None, 0.0
        for q in qs:
            u, e_, _ = U_order(s, state, q)
            if u - base > best:
                best, bq = u - base, q
            qerr = max(qerr, e_ + base_err)
        h = 2.0 / n
        A_bar = s.pf["Delta"]
        out[state] = {"max_gain": best, "argmax_q": bq, "candidate_payoff": base,
                      "budget": {"quadrature": qerr, "tail_truncation": A_bar * tail_mass_bound(s.noise, s.b), "between_grid_first_order": (A_bar * (1 + 1 / s.b) + s.k) * h / 2,
                                 "between_grid_second_order": (2 * A_bar / s.b + A_bar / s.b ** 2) * h * h / 8, "order_intervals": n}}
    return out


def write_summary(out: dict) -> None:
    lines = ["# S1-B/S1-C independent checks", "",
             f"Generated {out['generated']}; elapsed {out['elapsed_seconds']:.0f} s; "
             f"Python {out['environment']['python']}, numpy {out['environment']['numpy']}, scipy {out['environment']['scipy']}, mpmath {out['environment']['mpmath']}.",
             "", "Controls: quadrature targets 1e-12 abs/rel (C.0 1e-11 tightened by ten), order intervals 800 (C.0 400 doubled), "
             "line cut at 60 b beyond the outermost breakpoint with the omitted mass bounded (Laplace e^{-60}, logistic 2/(1+e^{60})), mpmath 40 digits for closed forms, 30 digits for auction integrals.",
             "", "## Counts per test", "", "| test | pass | fail | info | required failures |", "|---|---:|---:|---:|---:|"]
    for t, s in out["summary"].items():
        lines.append(f"| {t} | {s['pass']} | {s['FAIL']} | {s['info']} | {s['required_fail']} |")
    lines += ["", "## Landmarks", "", "| landmark | independent | spec value | abs diff | status |", "|---|---:|---:|---:|---|"]
    for r in out["checks"]:
        if r["test"] == "landmark" or "landmark" in r["quantity"]:
            lines.append(f"| {r['quantity']} | {r['independent']} | {r['repo']} | {r['abs_diff']:.2e} | {r['status']} |")
    fails = [r for r in out["checks"] if r["status"] == "FAIL"]
    lines += ["", f"## Failures ({len(fails)})", ""]
    if not fails:
        lines.append("None.")
    for r in fails:
        lines.append(f"- [{r['test']}] {r['quantity']}: independent={r['independent']} repo={r['repo']} diff={r['abs_diff']} tol={r['tolerance']} "
                     f"required={r['required']} note={r['note']}")
    # error budgets for T07
    lines += ["", "## Deviation-scan error budgets (T07, T13, T14: maximum over rows)", ""]
    keys = ["quadrature", "tail_truncation", "between_grid_first_order", "between_grid_second_order"]
    agg = {k: 0.0 for k in keys}
    nb = 0
    for r in out["checks"]:
        for st, b in (r.get("error_budget") or {}).items():
            if isinstance(b, dict) and "quadrature" in b:
                nb += 1
                for k in keys:
                    agg[k] = max(agg[k], b.get(k, 0.0))
    lines.append(f"{nb} state-scans; max quadrature error {agg['quadrature']:.2e}; max tail-truncation bound {agg['tail_truncation']:.2e} (cut at 60 b); "
                 f"between-grid coverage bound: first-order Lipschitz {agg['between_grid_first_order']:.2e}, second-order (OA.63) {agg['between_grid_second_order']:.2e}.")
    lines.append("The between-grid bound is a coverage budget for the finite grid; global optimality of the accepted rows rests on the analytical "
                 "margins (A1)-(A3) and the derivative bound, which are verified separately (T06).")
    OUT_MD.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    sys.exit(main())
