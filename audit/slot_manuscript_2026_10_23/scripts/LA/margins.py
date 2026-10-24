"""Margins of every strict hypothesis in the Laplace manuscript (commit 01bd5d6) at its declared
parameter vectors.

Method. Quantities that depend on e = exp(1) are enclosed with outward interval arithmetic
(mpmath.iv, 50 decimal digits) from exact decimal inputs. Quantities that are rational in the
inputs are computed exactly with fractions.Fraction and printed as reduced fractions. The script
prints results and writes margins.csv and margins_run.log beside itself. It makes no assertion.

Shared objects (uniform incumbent on [0, r], point masses at ell and h, reserve p):
  t_0 = p(1 - p/r),  t_H = r/2 + p^2/(2r),  t_L = ell - (ell^2 - p^2)/(2r),
  g_H = h - t_H,     g_L = (ell^2 - p^2)/(2r),  Delta_T = (r - ell)^2/(2r),
  B_r(mu) = g_L + mu (g_H - g_L),  tau(r) = (c_H - g_L)/(g_H - g_L),
  m(pi) = pi/(pi + (1-pi) e^{2/b}),  M(pi) = pi/(pi + (1-pi) e^{-2/b}),  kappa(pi) = min{m(pi), 1 - M(pi)}.
"""
from __future__ import annotations

import csv
import datetime as dt
import os
import platform
import sys
from fractions import Fraction as Fr

import mpmath as mp

iv = mp.iv
iv.dps = 50
mp.mp.dps = 60
HERE = os.path.dirname(os.path.abspath(__file__))
ROWS: list[dict] = []
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s)
    LOG.append(s)


def I(x):
    """Interval from an int, an exact decimal string, a Fraction, or an interval."""
    if isinstance(x, Fr):
        return iv.mpf(str(x.numerator)) / iv.mpf(str(x.denominator))
    if isinstance(x, (int, str)):
        return iv.mpf(str(x))
    return x


def lo(x):
    return mp.mpf(x.a)


def hi(x):
    return mp.mpf(x.b)


def s15(x) -> str:
    return mp.nstr(x, 15)


def rec(key: str, value, kind: str, binding: str = "", note: str = "") -> None:
    """Record one quantity. kind: 'exact' (Fraction) or 'interval'."""
    if kind == "exact":
        lower = upper = str(value)
        disp = f"{float(value):.12g}  (= {value})"
    else:
        lower, upper = mp.nstr(lo(value), 40), mp.nstr(hi(value), 40)
        disp = f"[{s15(lo(value))}, {s15(hi(value))}]"
    sign = ""
    if kind == "exact":
        sign = "positive" if value > 0 else ("negative" if value < 0 else "zero")
    else:
        sign = "positive" if lo(value) > 0 else ("negative" if hi(value) < 0 else "unresolved")
    ROWS.append(dict(key=key, lower=lower, upper=upper, kind=kind, sign=sign, binding=binding, note=note))
    say(f"  {key:44s} {disp:48s} {sign:10s} {binding} {note}".rstrip())


# ----------------------------------------------------------------------------------------------
# Auction objects
# ----------------------------------------------------------------------------------------------

def auction_fr(h: Fr, ell: Fr, p: Fr, r: Fr) -> dict:
    """Exact point-mass auction objects (equation (4) of the manuscript) for p < ell < r < h."""
    t0 = p * (1 - p / r)
    tH = r / 2 + p * p / (2 * r)
    tL = ell - (ell * ell - p * p) / (2 * r)
    gH = h - tH
    gL = (ell * ell - p * p) / (2 * r)
    D = (r - ell) ** 2 / (2 * r)
    return dict(t0=t0, tH=tH, tL=tL, gH=gH, gL=gL, D=D)


def auction_iv(h, ell, p, r) -> dict:
    """Interval version for an interval strength r."""
    h, ell, p, r = I(h), I(ell), I(p), I(r)
    t0 = p * (1 - p / r)
    tH = r / 2 + p * p / (2 * r)
    tL = ell - (ell * ell - p * p) / (2 * r)
    return dict(t0=t0, tH=tH, tL=tL, gH=h - tH, gL=(ell * ell - p * p) / (2 * r), D=(r - ell) ** 2 / (2 * r))


def B_fr(a: dict, mu: Fr) -> Fr:
    return a["gL"] + mu * (a["gH"] - a["gL"])


def B_iv(a: dict, mu) -> object:
    return I(a["gL"]) + I(mu) * (I(a["gH"]) - I(a["gL"]))


def tau_fr(a: dict, cH: Fr) -> Fr:
    return (cH - a["gL"]) / (a["gH"] - a["gL"])


def bounds(pi, b) -> tuple:
    """m(pi), M(pi), kappa(pi) as intervals; E2 = exp(2/b)."""
    pi, b = I(pi), I(b)
    E2 = iv.exp(2 / b)
    m = pi / (pi + (1 - pi) * E2)
    M = pi / (pi + (1 - pi) / E2)
    one_minus_M = 1 - M
    # kappa = min(m, 1 - M): take the endpoint-wise minimum (both are intervals)
    kap = iv.mpf([min(lo(m), lo(one_minus_M)), min(hi(m), hi(one_minus_M))])
    return m, M, kap, E2


def logit(x):
    x = I(x)
    return iv.log(x / (1 - x))


def laplace_entry(tau, pi, b, rho) -> dict:
    """Full-order Laplace entry objects, equation (12): x*, alpha_H, alpha_L, E, e_H, e_L."""
    tau, pi, b, rho = I(tau), I(pi), I(b), I(rho)
    xs = (b / 2) * (logit(tau) - logit(pi))
    aH = 1 - iv.exp((xs - 1) / b) / 2
    aL = iv.exp(-(xs + 1) / b) / 2
    eH = rho + (1 - rho) * aH
    eL = rho + (1 - rho) * aL
    E = pi * eH + (1 - pi) * eL
    return dict(xs=xs, aH=aH, aL=aL, eH=eH, eL=eL, E=E)


def frak_r(ell: Fr, d) -> object:
    """r(d) = ell + d + sqrt(d^2 + 2 ell d), the strength with Delta_T(r) = d (interval)."""
    ell, d = I(ell), I(d)
    return ell + d + iv.sqrt(d * d + 2 * ell * d)


# ----------------------------------------------------------------------------------------------
# Benchmark vector (A.48)
# ----------------------------------------------------------------------------------------------
h, ell, p, rho, cH, b, k = Fr(10), Fr(1), Fr(1, 2), Fr(1, 4), Fr(6), Fr(2), Fr(1, 50)
pi = Fr(1, 2)
r0, r1, r2 = Fr(6, 5), Fr(3), Fr(18, 5)

say("=" * 110)
say("Laplace manuscript 01bd5d6: strict-hypothesis margins at the declared vectors")
say(f"run {dt.datetime.now(dt.timezone.utc).isoformat()}  python {platform.python_version()}  mpmath {mp.__version__}  iv.dps={iv.dps}")
say("=" * 110)

A0, A1, A2 = auction_fr(h, ell, p, r0), auction_fr(h, ell, p, r1), auction_fr(h, ell, p, r2)
m, M, kap, E2 = bounds(pi, b)

say("\n[1] Posterior bounds at pi = 1/2, b = 2 (e^{2/b} = e)")
rec("m_half", m, "interval", note="m = 1/(1+e)")
rec("M_half", M, "interval", note="M = e/(1+e)")

say("\n[2] Auction objects (exact) at r0, r1, r2")
for name, A, r in (("r0", A0, r0), ("r1", A1, r1), ("r2", A2, r2)):
    for key in ("t0", "tH", "tL", "gH", "gL", "D"):
        rec(f"{key}_{name}", A[key], "exact", note=f"r = {r}")
    rec(f"B_prior_{name}", B_fr(A, pi), "exact", note="B_r(1/2)")
    rec(f"tau_{name}", tau_fr(A, cH), "exact", note="tau(r) = (c_H - g_L)/(g_H - g_L)")

say("\n[3] Proposition 2 at (r0, r1) = (1.2, 3): hypotheses (A1), (A2), ownership")
rec("A1_lower: c_H - B_r0(pi)", cH - B_fr(A0, pi), "exact", "A1 lower")
rec("A1_upper: B_r1(M) - c_H", B_iv(A1, M) - I(cH), "interval", "A1 upper")
rec("A2_lower: k - Delta_T(r0)", k - A0["D"], "exact", "A2 lower")
zeta1 = (1 - 1 / I(b)) * I(rho) * kap * I(A1["D"]) - I(k)
rec("A2_upper: (1-1/b) rho kappa Delta_T(r1) - k", zeta1, "interval", "A2 upper")
rec("A2_window_lower: Delta_T(r0)", A0["D"], "exact", note="window (0.0167, 0.0224) in Section 4.2")
rec("A2_window_upper: (1-1/b) rho m Delta_T(r1)", (1 - 1 / I(b)) * I(rho) * m * I(A1["D"]), "interval")
rec("spread_ratio: Delta_T(r0)/Delta_T(r1)", A0["D"] / A1["D"], "exact", note="= 0.025")
rec("spread_ratio_bound: (1-1/b) rho m", (1 - 1 / I(b)) * I(rho) * m, "interval", note="= 0.0336 in Section 4.2 (printed 0.034)")
rec("ownership: (1+rho) W_H(r1) - 2 rho W_H(r0)", (1 + rho) * 1 - 2 * rho * 1, "exact", note="W_H = 1 (h > r)")
tau1 = tau_fr(A1, cH)
rec("tau_r1 - pi", tau1 - pi, "exact", note="tau in (pi, M): lower side")
rec("M - tau_r1", M - I(tau1), "interval", note="tau in (pi, M): upper side")
L1 = laplace_entry(tau1, pi, b, rho)
rec("x_star_r1", L1["xs"], "interval", note="x* = (b/2) logit(tau); must lie in (0, 1)")
rec("1 - x_star_r1", 1 - L1["xs"], "interval")
rec("alpha_H_r1", L1["aH"], "interval")
rec("alpha_L_r1", L1["aL"], "interval")
rec("entry_r1", L1["E"], "interval", note="manuscript prints 0.522757")
rec("ownership_r1: e_H/2", L1["eH"] / 2, "interval", note="manuscript prints 0.324192")
rec("entry_r0", I(rho), "interval", note="no trade; entry = rho")
# frozen full-order control at r0 (numerical diagnostic in the manuscript; closed form here)
tau0 = tau_fr(A0, cH)
L0 = laplace_entry(tau0, pi, b, rho)
rec("frozen_entry_r0 (control, closed form)", L0["E"], "interval", note="manuscript prints 0.562178")
# welfare pieces at r1
dRT = (1 - I(rho)) * (I(pi) * L1["aH"] * I(A1["tH"] - A1["t0"]) + (1 - I(pi)) * L1["aL"] * I(A1["tL"] - A1["t0"]))
rec("proceeds_gain_r1 (A.41 second line)", dRT, "interval", note="manuscript prints 0.257809")
W_fb = I((r1 * r1 - p * p) / (2 * r1)) + (L1["eH"] * I(A1["gH"] + p * p / r1) + L1["eL"] * I(A1["gL"] + p * p / r1)) / 2 \
    - (1 - I(rho)) * (L1["aH"] + L1["aL"]) / 2 * I(cH)
W_hid = I((r1 * r1 - p * p) / (2 * r1)) + I(rho) * I(A1["gH"] + A1["gL"] + 2 * p * p / r1) / 2
rec("W_feedback_r1 (OA.49, c_L = 0)", W_fb, "interval", note="Table 2 prints 2.632301")
rec("W_hidden_r1 (OA.49, c_L = 0)", W_hid, "interval", note="Table 2 prints 2.552083")
rec("W_gain_r1", W_fb - W_hid, "interval", note="Table 2 prints 0.080218")
rec("A9_condition: c_H - B_r1(pi)", cH - B_fr(A1, pi), "exact", note="high-cost preparation does not pay at the prior")

say("\n[4] Proposition 2 part (iii) at r2 = 3.6: the return of entry to its floor")
rec("iii_exclusion: c_H - B_r2(M)", I(cH) - B_iv(A2, M), "interval", "part (iii)", "the thinnest margin in the manuscript")
rec("iii_posterior_gap: tau_r2 - M", I(tau_fr(A2, cH)) - M, "interval", note="BRIEF §3 'about 0.0003 in posterior'")
rec("iii_trade: (1-1/b) rho kappa Delta_T(r2) - k", (1 - 1 / I(b)) * I(rho) * kap * I(A2["D"]) - I(k), "interval", "part (iii) trading bound")
rec("iii_spread_order: Delta_T(r2) - Delta_T(r1)", A2["D"] - A1["D"], "exact", note="Proposition 1(b) gives the sign")
rec("support: h - r2", h - r2, "exact")
rec("support: r2 - ell", r2 - ell, "exact")
rec("support: ell - p", ell - p, "exact")
rec("support: b - 1", b - 1, "exact")
# r_C from (A.11)
q = M * I(h) - I(cH)
rC = (q + iv.sqrt(q * q + M * ((1 - M) * I(ell) ** 2 - I(p) ** 2))) / M
rec("r_C (A.11)", rC, "interval", note="manuscript prints 3.592658519; thresholds.csv bounds are float ulps")
rec("r2 - r_C", I(r2) - rC, "interval", "part (iii)", "width of the open set in r2 below 3.6")
rec("B_rC(M) - c_H (residual at the enclosure)", B_iv(auction_iv(h, ell, p, rC), M) - I(cH), "interval", note="must contain zero")
rec("dB_r(M)/dr at r2: -M/2 - ((1-M) ell^2 - p^2)/(2 r2^2)", -M / 2 - ((1 - M) * I(ell) ** 2 - I(p) ** 2) / (2 * I(r2) ** 2), "interval", note="A.4 asserts B_r(M) strictly decreasing")
rec("(1-M) ell^2 - p^2", (1 - M) * I(ell) ** 2 - I(p) ** 2, "interval", note="sign decides which case of the monotonicity argument applies")
Elim = I(rho) + (1 - I(rho)) / 4 * (1 + iv.exp(-2 / I(b)))
rec("entry_left_limit_at_rC (A.14)", Elim, "interval", note="registry prints 0.506477")

say("\n[5] Proposition A.4 thresholds (closed forms; r_N and frak r(k) are algebraic, r_U and r_C involve e)")
rec("frak_r(k) pooling-unique sufficient", frak_r(ell, I(k)), "interval", note="manuscript prints 1.220997512; exact: 1 + 1/50 + sqrt(1/2500 + 1/25)")
rec("r_N = frak_r(2k/rho) pooling existence", frak_r(ell, I(2 * k / rho)), "interval", note="manuscript prints 1.747877538; exact: 1 + 4/25 + sqrt(16/625 + 8/25)")
rec("r_U = frak_r(k/((1-1/b) rho m))", frak_r(ell, I(k) / ((1 - 1 / I(b)) * I(rho) * m)), "interval", note="manuscript prints 2.837416964")
rec("r1 - r_U", I(r1) - frak_r(ell, I(k) / ((1 - 1 / I(b)) * I(rho) * m)), "interval", note="r1 lies in the full-order uniqueness region")
rec("frak_r(k) - r0", frak_r(ell, I(k)) - I(r0), "interval", note="r0 lies in the no-trade uniqueness region")

say("\n[6] Prior windows of Section 4.2 (closed forms; each endpoint names its binding inequality)")
# (a) A2 window nonempty: kappa(pi) > kbar, kbar = Delta_T(r0)/((1-1/b) rho Delta_T(r1)) = 1/5 exactly
kbar = A0["D"] / ((1 - 1 / b) * rho * A1["D"])
rec("kbar = Delta_T(r0)/((1-1/b) rho Delta_T(r1))", kbar, "exact")
pi_a = I(kbar) * E2 / (1 - I(kbar) + I(kbar) * E2)
rec("prior_window_A2_lower = kbar e/(1 - kbar + kbar e)", pi_a, "interval", "kappa(pi) = m(pi) > kbar", "manuscript prints 0.404610")
rec("prior_window_A2_upper = 1 - lower", 1 - pi_a, "interval", "kappa(pi) = 1 - M(pi) > kbar", "manuscript prints 0.595390")
# (b) parts (i)-(ii) with costs fixed: pi > tau1/(e(1-tau1) + tau1) [c_H < B_r1(M(pi))];
#     pi < tau0 [B_r0(pi) < c_H]; kappa(pi) > k/((1-1/b) rho Delta_T(r1)) = 6/25
pi_b_lo = I(tau1) / (E2 * (1 - I(tau1)) + I(tau1))
kk = k / ((1 - 1 / b) * rho * A1["D"])
rec("kk = k/((1-1/b) rho Delta_T(r1))", kk, "exact")
pi_kk_lo = I(kk) * E2 / (1 - I(kk) + I(kk) * E2)
rec("prior_i_ii_candidate: c_H < B_r1(M(pi)) iff pi >", pi_b_lo, "interval", "c_H < B_r1(M(pi))", "manuscript prints 0.467850 (binding)")
rec("prior_i_ii_candidate: kappa(pi) > kk iff pi >", pi_kk_lo, "interval", "A2 upper, m(pi)", "not binding (0.4619 < 0.4679)")
rec("prior_i_ii_candidate: B_r0(pi) < c_H iff pi <", tau0, "exact", "A1 lower", "not binding (0.6331 > 0.5381)")
rec("prior_i_ii_upper: kappa(pi) > kk iff pi <", 1 - pi_kk_lo, "interval", "A2 upper, 1 - M(pi)", "manuscript prints 0.538096 (binding)")
# (c) all three parts: add B_r2(M(pi)) < c_H iff pi < tau2/(e(1 - tau2) + tau2)
tau2 = tau_fr(A2, cH)
pi_c_hi = I(tau2) / (E2 * (1 - I(tau2)) + I(tau2))
rec("prior_iii_upper: B_r2(M(pi)) < c_H iff pi <", pi_c_hi, "interval", "part (iii) exclusion", "manuscript prints 0.500424 (binding)")
rec("prior_iii_upper - 1/2", pi_c_hi - I(Fr(1, 2)), "interval", note="slack of the benchmark prior inside the three-part window")

say("\n[7] Proposition 3 nodes: pooling margins (exact), domain, threshold ordering over the bracket")
for rs, vl, vr in (("1.55", "0.46031618", "0.46031620"), ("1.60", "0.70747537", "0.70747539"), ("1.65", "0.90333198", "0.90333201")):
    r = Fr(rs)
    A = auction_fr(h, ell, p, r)
    rec(f"pooling_margin_{rs}: k - rho Delta_T/2", k - rho * A["D"] / 2, "exact", "no-trade existence", "certificates.csv pooling_margin_lower")
    rec(f"domain_{rs}: c_H - B_r(1/2)", cH - B_fr(A, pi), "exact", "maintained domain D")
    rec(f"B_r(m)_{rs} (zero-cost floor diagnostic)", B_iv(A, m), "interval")
    t = tau_fr(A, cH)
    rec(f"tau_{rs} - 1/2", t - pi, "exact", "threshold ordering lower")
    v = iv.mpf([vl, vr])
    Mv = 1 / (1 + iv.exp(-(1 + v) / I(b)))
    rec(f"M_v - tau_{rs} over the bracket", Mv - I(t), "interval", "threshold ordering upper")
    xs = (I(b) * logit(t) + 1 - v) / 2
    rec(f"x_star_{rs} + v over the bracket", xs + v, "interval", "x* > -v")
    rec(f"1 - x_star_{rs} over the bracket", 1 - xs, "interval", "x* < 1")
    E = I(rho) + (1 - I(rho)) / 2 * (1 - iv.exp((xs - 1) / I(b)) / 2 + iv.exp(-(xs + v) / I(b)) / 2)
    rec(f"entry_{rs} over the bracket (A.15)", E, "interval", note="compare certificates.csv E_lower/E_upper")
rec("Prop3_low_type_concavity: 2 - 1/b", 2 - 1 / b, "exact", note="OA.69 needs b > 1/2")

say("\n[8] Proposition A.6 (atomless costs, eps_C = 0.1) support restrictions (A.24) at the benchmark")
epsC = Fr(1, 10)
rec("A24_low: B_r1(m) - 2 eps_C", B_iv(A1, m) - I(2 * epsC), "interval", "A.24 first line", "table_extensions_margins prints 2.17")
rec("A24_mid: (c_H - eps_C) - B_r0(pi)", (cH - epsC) - B_fr(A0, pi), "exact", "A.24 second line, left")
rec("A24_high: B_r1(M) - (c_H + eps_C)", B_iv(A1, M) - I(cH + epsC), "interval", "A.24 second line, right")

say("\n[9] Lemma OA.1 / Proposition A.5 logistic check at the strong benchmark (closed forms (A.23))")
Aexp = iv.exp(1 / I(b))
w = iv.sqrt(I(tau1) * (1 - I(pi)) / ((1 - I(tau1)) * I(pi)))
xlog = I(b) * iv.log((Aexp * w - 1) / (Aexp - w))
aHl = 1 / (1 + iv.exp((xlog - 1) / I(b)))
aLl = 1 / (1 + iv.exp((xlog + 1) / I(b)))
rec("logistic_x_star_r1", xlog, "interval", note="manuscript prints 5.424598398")
rec("logistic_entry_r1", I(rho) + (1 - I(rho)) * (aHl + aLl) / 2, "interval", note="manuscript prints 0.301509")

say("\n[10] Online Appendix A.12 stake bounds (OA.63), (OA.64)")
Om_U = 2 * I(b) * zeta1 / ((1 - I(rho)) * I(A1["tH"] - A1["t0"]))
Om_0 = 2 * I(b) * I(k - A0["D"]) / ((1 - I(rho)) * I(A0["tH"] - A0["t0"]))
rec("Omega_U", Om_U, "interval", note="manuscript prints 0.011434")
rec("Omega_0", Om_0, "interval", note="manuscript prints 0.043098")

# ----------------------------------------------------------------------------------------------
# Moderate-value vector (A.49)
# ----------------------------------------------------------------------------------------------
say("\n[11] Moderate-value vector (A.49): h = 2, c_H = 0.89, k = 0.002, (r0, r1) = (1.05, 1.5)")
hm, cHm, km = Fr(2), Fr(89, 100), Fr(1, 500)
r0m, r1m = Fr(21, 20), Fr(3, 2)
A0m, A1m = auction_fr(hm, ell, p, r0m), auction_fr(hm, ell, p, r1m)
rec("mod_A1_lower: c_H - B_r0(pi)", cHm - B_fr(A0m, pi), "exact", "A1 lower", "margins table prints 3.35e-2")
rec("mod_A1_upper: B_r1(M) - c_H", B_iv(A1m, M) - I(cHm), "interval", "A1 upper", "prints 3.01e-2")
rec("mod_A2_lower: k - Delta_T(r0)", km - A0m["D"], "exact", "A2 lower", "prints 8.10e-4")
rec("mod_A2_upper: (1-1/b) rho m Delta_T(r1) - k", (1 - 1 / I(b)) * I(rho) * m * I(A1m["D"]) - I(km), "interval", "A2 upper", "prints 8.01e-4")
rec("mod_zeta_L: B_r1(m)", B_iv(A1m, m), "interval", note="prints 4.97e-1")
Lm = laplace_entry(tau_fr(A1m, cHm), pi, b, rho)
rec("mod_entry_r1", Lm["E"], "interval", note="manuscript prints 0.526805")

# ----------------------------------------------------------------------------------------------
# Complementary-signal vector (A.50)
# ----------------------------------------------------------------------------------------------
say("\n[12] Complementary-signal vector (A.50): rho = 0.85, c_H = 7.14, k = 0.015, (r0, r1) = (1.1, 2.3), a = 0.70, d = 0.75")
rhos, cHs, ks = Fr(17, 20), Fr(714, 100), Fr(3, 200)
r0s, r1s = Fr(11, 10), Fr(23, 10)
a_acc, d_acc = Fr(7, 10), Fr(3, 4)
A0s, A1s = auction_fr(h, ell, p, r0s), auction_fr(h, ell, p, r1s)
mu_plus = I(1 - a_acc) + I(2 * a_acc - 1) * M
mu_minus = I(1 - a_acc) + I(2 * a_acc - 1) * m


def phi_plus(mu):
    mu = I(mu)
    return I(d_acc) * mu / (I(d_acc) * mu + I(1 - d_acc) * (1 - mu))


def phi_minus(mu):
    mu = I(mu)
    return I(1 - d_acc) * mu / (I(1 - d_acc) * mu + I(d_acc) * (1 - mu))


rec("sig_A29_1: c_H - B_r0(d)", cHs - B_fr(A0s, d_acc), "exact", "(A.29) first line, left", "prints 5.25e-2")
rec("sig_A29_2: B_r1(phi_+(mu_+)) - c_H", B_iv(A1s, phi_plus(mu_plus)) - I(cHs), "interval", "(A.29) first line, right", "prints 4.53e-2")
wH0 = A0s["tH"] - A0s["t0"]
rec("sig_A29_3: k - (2a-1){Delta_T(r0) + (1-rho)(2d-1) w_H(r0)}", ks - (2 * a_acc - 1) * (A0s["D"] + (1 - rhos) * (2 * d_acc - 1) * wH0), "exact", "(A.29) second line, left", "prints 1.45e-3")
rec("sig_A29_4: (1-1/b) m (2a-1) rho Delta_T(r1) - k", (1 - 1 / I(b)) * m * I(2 * a_acc - 1) * I(rhos) * I(A1s["D"]) - I(ks), "interval", "(A.29) second line, right", "prints 1.80e-3")
rec("sig_floor_diagnostic: B_r1(phi_-(mu_-))", B_iv(A1s, phi_minus(mu_minus)), "interval", note="recorded margin, not a hypothesis; prints 1.77")

# ----------------------------------------------------------------------------------------------
# Class exhibit cases A, B, D (point masses); case C needs the class-band integrals and is not redone here
# ----------------------------------------------------------------------------------------------
say("\n[13] Class exhibit (Table 4) point-mass cases A, B, D: the six margins of the second block")
cases = dict(A=(Fr(3, 10), Fr(9, 2), Fr(1, 100), Fr(11, 10), Fr(3), Fr(18, 5)),
             B=(Fr(7, 10), Fr(36, 5), Fr(1, 100), Fr(11, 10), Fr(3), Fr(18, 5)),
             D=(Fr(7, 10), Fr(67, 10), Fr(1, 50), Fr(1), Fr(9, 2), Fr(11, 2)))
for name, (pic, cHc, kc, r0c, r1c, r2c) in cases.items():
    mc, Mc, kapc, _ = bounds(pic, b)
    Ac0, Ac1, Ac2 = auction_fr(h, ell, p, r0c), auction_fr(h, ell, p, r1c), auction_fr(h, ell, p, r2c)
    rec(f"case{name}_cH - B0", cHc - B_fr(Ac0, pic), "exact", "A1 lower")
    rec(f"case{name}_B1(M) - cH", B_iv(Ac1, Mc) - I(cHc), "interval", "A1 upper")
    rec(f"case{name}_k - Delta0", kc - Ac0["D"], "exact", "A2 lower")
    rec(f"case{name}_u1 - k", (1 - 1 / I(b)) * I(rho) * kapc * I(Ac1["D"]) - I(kc), "interval", "A2 upper")
    rec(f"case{name}_cH - B2(M)", I(cHc) - B_iv(Ac2, Mc), "interval", "part (iii)")
    if lo(B_iv(Ac1, Mc) - I(cHc)) > 0:
        Lc = laplace_entry(tau_fr(Ac1, cHc), pic, b, rho)
        rec(f"case{name}_x_star_r1", Lc["xs"], "interval")
        rec(f"case{name}_entry_r1", Lc["E"], "interval")

# ----------------------------------------------------------------------------------------------
# Outputs
# ----------------------------------------------------------------------------------------------
csv_path = os.path.join(HERE, "margins.csv")
with open(csv_path, "w", newline="") as fh:
    wr = csv.DictWriter(fh, fieldnames=["key", "lower", "upper", "kind", "sign", "binding", "note"])
    wr.writeheader()
    wr.writerows(ROWS)
neg = [r["key"] for r in ROWS if r["sign"] == "negative"]
unres = [r["key"] for r in ROWS if r["sign"] == "unresolved"]
say("\nnegative signs (expected: the derivative dB_r(M)/dr, and case D's upper cost bound, which Table 4 reports as a failure): " + (", ".join(neg) if neg else "none"))
say("unresolved interval signs: " + (", ".join(unres) if unres else "none"))
say(f"rows written: {len(ROWS)} -> {csv_path}")
with open(os.path.join(HERE, "margins_run.log"), "w") as fh:
    fh.write("\n".join(LOG) + "\n")
