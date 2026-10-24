#!/usr/bin/env python
"""XP2: recompute every R6/R9 quantity and compare it with registry/P2_auction.csv.

Usage (from the repository root):
    .venv/bin/python audit/slot_manuscript_2026_10_23/scripts/XP2/xp2_check.py

The script prints a run record, writes xp2_values.csv (every recomputed key,
midpoint and enclosure) and xp2_diff.csv (one comparison row per registry key).
It contains no assertions; it reports what it finds.
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import platform
import random
import re
import sys
import time
from fractions import Fraction as Fr

import mpmath
from mpmath import iv, mp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import xp2_engine as X  # noqa: E402
from xp2_engine import (B0, BB, BETA, E, ETA, LAM, U, I, Linv, Mpost, auction,  # noqa: E402
                        ends, evaluate, gross, imax, imin, mid, mpost, node,
                        pure_equilibria, sign)

TEAM = os.path.abspath(os.path.join(HERE, "..", ".."))
T_START = time.time()

V: dict[str, object] = {}       # key -> Fraction or interval
NOTE: dict[str, str] = {}


def put(key, val, note=""):
    V[key] = val
    if note:
        NOTE[key] = note


def fmt(x, n=12):
    if isinstance(x, Fr):
        return str(x) if x.denominator < 10**6 else mp.nstr(mp.mpf(x.numerator) / x.denominator, n)
    if isinstance(x, int):
        return str(x)
    return mp.nstr(mid(x), n)


def say(*a):
    print(*a)


def put_node(prefix, res):
    for f, v in res.items():
        if f.startswith("_"):
            continue
        put(prefix + f, v)


P10, P1, P2v = (Fr(10), Fr(10)), (Fr(1), Fr(1)), (Fr(2), Fr(2))
HALF, QUARTER = Fr(1, 2), Fr(1, 4)
BASE = dict(H=P10, L=P1, pi=HALF, p=HALF, rho=QUARTER, c=Fr(6), k=Fr(1, 50),
            rs=(Fr(6, 5), Fr(3), Fr(18, 5)))
EXAMPLES = {
    "base": BASE,
    "moderate": dict(BASE, H=P2v, c=Fr(89, 100), k=Fr(1, 500), rs=(Fr(21, 20), Fr(3, 2))),
    "bands": dict(BASE, H=(Fr(199, 20), Fr(201, 20)), L=(Fr(19, 20), Fr(21, 20))),
    "ex_a": dict(BASE, pi=Fr(3, 10), c=Fr(9, 2), k=Fr(1, 100), rs=(Fr(11, 10), Fr(3), Fr(18, 5))),
    "ex_b": dict(BASE, pi=Fr(7, 10), c=Fr(36, 5), k=Fr(1, 100), rs=(Fr(11, 10), Fr(3), Fr(18, 5))),
    "ex_c": dict(BASE, H=(Fr(1), Fr(19)), L=(Fr(3, 5), Fr(7, 5)), pi=Fr(7, 10), c=Fr(67, 10),
                 k=Fr(1, 50), rs=(Fr(1), Fr(9, 2), Fr(11, 2))),
    "ex_d": dict(BASE, pi=Fr(7, 10), c=Fr(67, 10), k=Fr(1, 50), rs=(Fr(1), Fr(9, 2), Fr(11, 2))),
}

say("XP2 independent recomputation of the P2 package (R6, R9)")
say("mpmath", mpmath.__version__, "python", platform.python_version(), "iv.dps", iv.dps)
say()

# ============================================================================
# 1. Slot primitives and benchmark singles
# ============================================================================
say("== 1. Slot primitives of calibration B ==")
put("u_B", U)
put("beta_B", BETA)
put("lambda_B", LAM)
put("b_B", BB)
put("M_half_B", Mpost(HALF))
put("m_half_B", mpost(HALF))
say("u =", fmt(U), " beta =", BETA, " lambda =", fmt(LAM), " b =", fmt(BB), " b0 =", fmt(B0))
say("check lambda/b - u =", fmt(LAM / BB - U, 6), "  2b+b0+lambda-1 =", fmt(2 * BB + B0 + LAM - 1, 6))
say("M(1/2) =", fmt(Mpost(HALF)), " m(1/2) =", fmt(mpost(HALF)), " e/(1+e) =", fmt(E / (1 + E)))
put("margin_p2_beta_lower_B", BETA)
put("margin_p2_beta_upper_B", Fr(1, 3) - BETA)
put("margin_p2_lambda_lower_B", LAM)
put("margin_p2_lambda_upper_B", 1 - LAM)
put("margin_p2_bplus_B", BB + LAM - I(HALF))

ob_b = [auction(P10, P1, HALF, r) for r in BASE["rs"]]
for i, ob in enumerate(ob_b):
    tau = (Fr(6) - ob["gl"]) / (ob["gh"] - ob["gl"])
    put(f"tau_r{i}", tau)
    say(f"r{i}={BASE['rs'][i]}: t0={ob['t0']} tH={ob['th']} tL={ob['tl']} gH={ob['gh']} gL={ob['gl']}"
        f" Delta={ob['delta']} tau={tau}")
# closed-form check of the shared objects (TEAM_RULES section 3)
for r in BASE["rs"]:
    p, h, l = HALF, Fr(10), Fr(1)
    cf = dict(t0=p * (1 - p / r), th=r / 2 + p * p / (2 * r), tl=l - (l * l - p * p) / (2 * r),
              gh=h - r / 2 - p * p / (2 * r), gl=(l * l - p * p) / (2 * r), delta=(r - l) ** 2 / (2 * r))
    ob = auction(P10, P1, p, r)
    say(f"  closed forms at r={r}: all equal ->", all(cf[k] == ob[k] for k in cf))
put("prior_lo_B", Linv(V["tau_r1"]))
put("prior_hi_B", Linv(V["tau_r2"]))
say("prior window (L(tau1), L(tau2)) =", fmt(V["prior_lo_B"]), fmt(V["prior_hi_B"]))
say()

# ============================================================================
# 2. Value-class examples
# ============================================================================
say("== 2. Value-class examples (forced orders from the all-profile bounds) ==")
NODES = {}
for name, ex in EXAMPLES.items():
    for lab, val in (("pi", ex["pi"]), ("p", ex["p"]), ("rho", ex["rho"]), ("cost", ex["c"]),
                     ("k", ex["k"]), ("high_lo", ex["H"][0]), ("high_hi", ex["H"][1]),
                     ("low_lo", ex["L"][0]), ("low_hi", ex["L"][1])):
        put(f"p2_input_{name}_{lab}", val)
    for i, r in enumerate(ex["rs"]):
        put(f"p2_input_{name}_r{i}", r)
    obs = []
    for i, r in enumerate(ex["rs"]):
        res, ob = node(ex["H"], ex["L"], ex["pi"], ex["p"], ex["rho"], ex["c"], ex["k"], r)
        obs.append(ob)
        NODES[(name, i)] = res
        put_node(f"p2_{name}_r{i}_", res)
        eqs = pure_equilibria(ob, ex["pi"], ex["rho"], ex["c"], ex["k"])
        say(f"{name:9s} r{i}={str(r):6s} {res['_why']:38s} profile={res.get('_profile')} "
            f"pattern={res.get('_pattern')} E={fmt(res['entry'], 9)} O_H={fmt(res['ownership'], 9)} "
            f"W_H={fmt(res['wh'], 9)} choice_h={fmt(res['choice_h'], 6)} choice_l={fmt(res['choice_l'], 6)}"
            f" flags={res['_flags']} pure-eq={[(e[0]) for e in eqs]}")
    pi, rho, c, k = I(ex["pi"]), I(ex["rho"]), I(ex["c"]), I(ex["k"])
    M, m = Mpost(ex["pi"]), mpost(ex["pi"])
    mar = dict(weak_cost=c - gross(obs[0], pi), weak_trade=k - I(obs[0]["delta"]),
               strong_top=gross(obs[1], M) - c, strong_prior=c - gross(obs[1], pi),
               high_floor=rho * (1 - M) * I(obs[1]["delta"]) - k,
               low_floor=rho * m * I(obs[1]["delta"]) - k,
               ownership=(rho + (1 - rho) * (BB + LAM)) * I(obs[1]["wh"]) - rho * I(obs[0]["wh"]))
    if len(obs) == 3:
        mar.update(collapse=c - gross(obs[2], M),
                   collapse_high=rho * (1 - M) * I(obs[2]["delta"]) - k,
                   collapse_low=rho * m * I(obs[2]["delta"]) - k)
    for lab, val in mar.items():
        put(f"margin_p2_{name}_{lab}_B", val)
    say("   margins:", {lab: (fmt(v, 7), sign(v)) for lab, v in mar.items()})
    if name == "ex_c":
        say("   ex_c W_H at the three strengths:", [o["wh"] for o in obs],
            " ownership r0, r1, r2:", [fmt(NODES[(name, i)]["ownership"], 9) for i in range(3)])
        # class order for C: G_L(v) >= G_H(v) everywhere
        grid = [Fr(j, 20) for j in range(0, 401)]

        def GL(v):
            return min(max((v - Fr(3, 5)) / Fr(4, 5), Fr(0)), Fr(1))

        def GH(v):
            return min(max((v - 1) / Fr(18), Fr(0)), Fr(1))
        say("   ex_c min over a 1/20 grid of G_L - G_H on [0,20]:", min(GL(v) - GH(v) for v in grid))
say()

# primitive and support margins of the benchmark
for lab, val in (("p", HALF), ("low_above_p", Fr(1) - HALF), ("r0_above_low", Fr(6, 5) - 1),
                 ("r1_above_r0", Fr(3) - Fr(6, 5)), ("r2_above_r1", Fr(18, 5) - 3),
                 ("high_above_r2", Fr(10) - Fr(18, 5)), ("pi", HALF), ("one_minus_pi", HALF),
                 ("rho", QUARTER), ("one_minus_rho", Fr(3, 4)), ("k", Fr(1, 50)), ("cost", Fr(6)),
                 ("class_gap", Fr(9))):
    put(f"margin_p2_primitive_{lab}_B", val)

# fixed benchmark costs at other priors
say("== 2b. Benchmark costs and strengths at priors 3/10 and 7/10 ==")
for tag, prior in (("three_tenths", Fr(3, 10)), ("seven_tenths", Fr(7, 10))):
    ex = dict(BASE, pi=prior)
    vec = []
    for i, r in enumerate(ex["rs"]):
        res, ob = node(ex["H"], ex["L"], prior, ex["p"], ex["rho"], ex["c"], ex["k"], r)
        put_node(f"p2_fixed_prior_{tag}_r{i}_", res)
        vec.append(res)
        say(f"pi={prior} r{i}: {res['_why']} profile={res['_profile']} pattern={res['_pattern']}"
            f" entry={fmt(res['entry'], 9)} flags={res['_flags']}")
    say(f"   entry vector at pi={prior}:", [fmt(x["entry"], 9) for x in vec])
    kap = imin(mpost(prior), 1 - Mpost(prior))
    up = I(QUARTER) * kap * I(Fr(2, 3))
    put(f"p2_other_prior_{tag}_trade_upper", up)
    put(f"p2_other_prior_{tag}_trade_window", up - I(Fr(1, 60)))
    put(f"p2_other_prior_{tag}_weak_cost", I(Fr(6)) - gross(ob_b[0], prior))
    put(f"p2_other_prior_{tag}_top_cost", gross(ob_b[1], Mpost(prior)) - 6)
say()

# ============================================================================
# 3. Admissible region at the benchmark
# ============================================================================
say("== 3. Admissible region at the benchmark ==")
tau1, tau2 = V["tau_r1"], V["tau_r2"]
# M(1/2) = (1+u)/(2+u) > tau1  <=>  u > (2 tau1 - 1)/(1 - tau1)
u_lo = (2 * tau1 - 1) / (1 - tau1)
u_hi = (2 * tau2 - 1) / (1 - tau2)
put("u_lo", u_lo)
put("u_hi", u_hi)
put("margin_p2_u_lo_B", U - I(u_lo))
put("margin_p2_u_hi_B", I(u_hi) - U)
say("u band from tau1 < M(1/2) < tau2:", u_lo, u_hi, " u inside:", sign(U - I(u_lo)), sign(I(u_hi) - U))
# trade bound at pi=1/2: rho * m(1/2) * Delta1 > k <=> (1/6)/(2+u) > 1/50 <=> u < 19/3
say("trade bound u < 19/3 =", float(Fr(19, 3)), " weaker than u_hi:", Fr(19, 3) > u_hi)
put("p2_prior_trade_lo", E / (9 + E))
put("p2_prior_trade_hi", 9 / (9 + E))
put("p2_prior_fixed_k_lo", 3 * E / (22 + 3 * E))
put("p2_prior_fixed_k_hi", 22 / (22 + 3 * E))
cost_hi = (Fr(6) - ob_b[0]["gl"]) / (ob_b[0]["gh"] - ob_b[0]["gl"])
put("p2_prior_cost_hi", cost_hi)
say("weak-cost prior cap tau0 =", cost_hi, "=", float(cost_hi))
put("margin_p2_posterior_collapse_B", I(tau2) - Mpost(HALF))
for name, z in (("lo", V["prior_lo_B"]), ("hi", V["prior_hi_B"])):
    kap = imin(mpost(z), 1 - Mpost(z))
    put(f"margin_p2_prior_{name}_trade_B", I(QUARTER) * kap * I(Fr(2, 3)) - I(Fr(1, 50)))
    put(f"margin_p2_prior_{name}_weak_B", 6 - gross(ob_b[0], z))
put("margin_p2_prior_lower_order_B", V["prior_lo_B"] - V["p2_prior_fixed_k_lo"])
put("margin_p2_prior_upper_order_B", V["p2_prior_fixed_k_hi"] - I(cost_hi))
put("margin_p2_prior_window_order_B", I(cost_hi) - V["prior_lo_B"])
# the two trade windows in closed form from the kappa(pi) thresholds
for thr, lab in ((Fr(1, 10), "kappa>1/10 (some k)"), (Fr(3, 25), "kappa>3/25 (k=1/50)")):
    # m(pi) = thr  <=>  pi = thr e /(1 - thr + thr e) ; 1-M(pi) = thr <=> pi = (1-thr)/(1-thr+thr e)
    ti = I(thr)
    lo_ = ti * E / (1 - ti + ti * E)
    hi_ = (1 - ti) / (1 - ti + ti * E)
    say(f"  {lab}: prior interval ({fmt(lo_, 10)}, {fmt(hi_, 10)})")
# check every hypothesis on the final window at its endpoints and an interior grid
say("  three-strength window check on 11 interior priors:")
lo_w, hi_w = mid(V["prior_lo_B"]), mid(V["prior_hi_B"])
for j in range(1, 12):
    z = Fr(int((lo_w + (hi_w - lo_w) * j / 12) * 10**12), 10**12)
    kap = imin(mpost(z), 1 - Mpost(z))
    sg = [sign(6 - gross(ob_b[0], z)), sign(Fr(1, 50) - ob_b[0]["delta"]),
          sign(gross(ob_b[1], Mpost(z)) - 6), sign(I(QUARTER) * kap * I(Fr(2, 3)) - I(Fr(1, 50))),
          sign(6 - gross(ob_b[2], Mpost(z)))]
    say(f"    pi={float(z):.9f} signs C0,T0,C1,T1,C2 = {sg}")
say()

# ============================================================================
# 4. Access to prices, transfer and trade scale
# ============================================================================
say("== 4. Access to prices at r1, transfer and break-even trade scale ==")
seen, ob1 = node(P10, P1, HALF, HALF, QUARTER, Fr(6), Fr(1, 50), Fr(3))
hid, _ = node(P10, P1, HALF, HALF, QUARTER, Fr(6), Fr(1, 50), Fr(3), regime="hidden")
put_node("p2_base_hidden_", hid)
dR = seen["proceeds"] - hid["proceeds"]
dW = seen["surplus"] - hid["surplus"]
put("p2_access_proceeds_gain", dR)
put("p2_access_surplus_gain", dW)
pi, rho = I(HALF), I(QUARTER)
M, m = Mpost(HALF), mpost(HALF)
dR_f = (1 - rho) * (pi * (BB + LAM) * I(ob1["th"] - ob1["t0"]) + (1 - pi) * BB * I(ob1["tl"] - ob1["t0"]))
dW_f = (1 - rho) * (BB + pi * LAM) * (gross(ob1, M) - 6 + I(HALF * Fr(1, 6)))
say("proceeds: access", fmt(seen["proceeds"]), "hidden", fmt(hid["proceeds"]), "gain", fmt(dR),
    " formula", fmt(dR_f), " diff", fmt(dR - dR_f, 3))
say("surplus : access", fmt(seen["surplus"]), "hidden", fmt(hid["surplus"]), "gain", fmt(dW),
    " formula", fmt(dW_f), " diff", fmt(dW - dW_f, 3))
say("hidden profile", hid["_profile"], "pattern", hid["_pattern"], "choices",
    fmt(hid["choice_h"], 8), fmt(hid["choice_l"], 8))
# informed gross profit, two ways
D1 = I(ob1["delta"])
G = LAM * D1 * (pi * (1 - M) + (1 - pi) * rho * m)
# liquidity side: (1-lambda) sum_q eta_q q (E[V | q, liquidity] - P_q)
tbar = pi * I(ob1["th"]) + (1 - pi) * I(ob1["tl"])
liq = iv.mpf(0)
for q in (-1, 1):
    ent = seen["entry_" + ("minus" if q < 0 else "plus")]
    ev = I(ob1["t0"]) + ent * (tbar - I(ob1["t0"]))
    liq += (1 - LAM) * I(ETA[q]) * q * (ev - seen["price_" + ("minus" if q < 0 else "plus")])
say("informed gross profit G =", fmt(G), "; liquidity gross P&L =", fmt(liq), "; sum =", fmt(G + liq, 3))
put("p2_access_gross_transfer", G)
put("p2_access_gross_conditional", G / LAM)
put("p2_access_break_even", dR / G)
put("p2_access_trade_resource_cost", LAM * I(Fr(1, 50)))
say("G/lambda =", fmt(G / LAM), " z* = dR/G =", fmt(dR / G), " dR/(G/lambda) =", fmt(dR / (G / LAM)))
# no-informed economy: posterior pi everywhere, B1(pi) < c_H => entry rho => proceeds = hidden level
noinf = I(ob1["t0"]) + rho * (pi * I(ob1["th"] - ob1["t0"]) + (1 - pi) * I(ob1["tl"] - ob1["t0"]))
say("no-informed proceeds", fmt(noinf), " equals hidden:", fmt(noinf - hid["proceeds"], 3))
# trade scale z: shareholders' total gain dR - z G, sign check at z* +/- 1e-6
for zz in (Fr(68483, 10000), Fr(68484, 10000)):
    say(f"  total gain at z={float(zz)}: {fmt(dR - I(zz) * G, 8)}")
say()

say("== 4b. Access outside the recruitment region: c_H = 12/5 ==")
oseen, _ = node(P10, P1, HALF, HALF, QUARTER, Fr(12, 5), Fr(1, 50), Fr(3))
ohid, _ = node(P10, P1, HALF, HALF, QUARTER, Fr(12, 5), Fr(1, 50), Fr(3), regime="hidden")
put_node("p2_outside_seen_", oseen)
put_node("p2_outside_hidden_", ohid)
put("p2_outside_proceeds_gain", oseen["proceeds"] - ohid["proceeds"])
put("p2_outside_surplus_gain", oseen["surplus"] - ohid["surplus"])
fR = -(1 - rho) * (pi * BB * I(ob1["th"] - ob1["t0"]) + (1 - pi) * (BB + LAM) * I(ob1["tl"] - ob1["t0"]))
fW = -(1 - rho) * (BB + (1 - pi) * LAM) * (gross(ob1, m) - I(Fr(12, 5)) + I(Fr(1, 12)))
say("seen pattern", oseen["_pattern"], "hidden pattern", ohid["_pattern"],
    "profiles", oseen["_profile"], ohid["_profile"])
say("cost signs B1(m)-c, B1(pi)-c:", fmt(gross(ob1, m) - I(Fr(12, 5)), 8), fmt(gross(ob1, pi) - I(Fr(12, 5)), 8))
say("proceeds change", fmt(V["p2_outside_proceeds_gain"]), " formula", fmt(fR), "; surplus change",
    fmt(V["p2_outside_surplus_gain"]), " formula", fmt(fW))
say()

# ============================================================================
# 5. Constructive sequence (source recipe retained)
# ============================================================================
say("== 5. Constructive sequence ==")
for ratio in (Fr(21, 20), Fr(11, 10), Fr(5, 4), Fr(3, 2), Fr(2)):
    nm = f"{ratio.numerator}_{ratio.denominator}"
    first = None
    for n in range(1, 21):
        d = (ratio - 1) / 2**n
        r0, r1 = 1 + d * d / (ratio - 1), 1 + d
        a0, a1 = auction((ratio, ratio), P1, HALF, r0), auction((ratio, ratio), P1, HALF, r1)
        M, m = Mpost(HALF), mpost(HALF)
        cost = (gross(a0, HALF) + gross(a1, M)) / 2
        k = (I(a0["delta"]) + I(Fr(1, 2)) * I(QUARTER) * m * I(a1["delta"])) / 2
        mar = (cost - gross(a0, HALF), gross(a1, M) - cost, k - I(a0["delta"]),
               I(QUARTER) * m * I(a1["delta"]) - k)
        # slot-native recipe (no factor 1/2): first feasible n for comparison
        k2 = (I(a0["delta"]) + I(QUARTER) * m * I(a1["delta"])) / 2
        native = all(sign(x) == "pos" for x in (mar[0], mar[1], k2 - I(a0["delta"]),
                                                I(QUARTER) * m * I(a1["delta"]) - k2))
        ok = all(sign(x) == "pos" for x in mar)
        if first is None:
            for j, x in enumerate(mar):
                put(f"p2_seq_{nm}_n{n}_margin{j}", x)
            say(f"  h={ratio} n={n} margins={[fmt(x, 6) for x in mar]} feasible={ok} native-recipe={native}")
        if ok and first is None:
            first = n
            put(f"p2_seq_{nm}_ratio", ratio)
            put(f"p2_seq_{nm}_n", Fr(n))
            put(f"p2_seq_{nm}_r0", r0)
            put(f"p2_seq_{nm}_r1", r1)
            put(f"p2_seq_{nm}_k", k)
            put(f"p2_seq_{nm}_cost", cost)
            for lab, r in (("weak", r0), ("strong", r1)):
                res, _ = node((ratio, ratio), P1, HALF, HALF, QUARTER, cost, k, r)
                put_node(f"p2_seq_{nm}_{lab}_", res)
                say(f"     {lab}: {res['_why']} pattern={res['_pattern']} entry={fmt(res['entry'], 9)}"
                    f" B(m)={fmt(res['low_profit_minus'], 6)} flags={res['_flags']}")
            say(f"     first feasible n={n}: r0={r0} r1={r1} k={fmt(k, 12)} c_H={fmt(cost, 12)}")
say()

# ============================================================================
# 6. Reserves
# ============================================================================
say("== 6. Reserves ==")
BANDS = ((Fr(199, 20), Fr(201, 20)), (Fr(19, 20), Fr(21, 20)))
RES = {}
for law, (H, L), highp in (("points", (P10, P1), Fr(101, 100)), ("bands", BANDS, Fr(11, 10))):
    for tag, p in (("base", HALF), ("exclude", highp), ("deter", Fr(31, 20))):
        for i, r in enumerate((Fr(6, 5), Fr(3))):
            res, ob = node(H, L, HALF, p, QUARTER, Fr(6), Fr(1, 50), r)
            RES[(law, tag, i)] = res
            put_node(f"p2_reserve_{law}_{tag}_r{i}_", res)
            prof = res["_profile"]
            if prof == (0, 0):
                glob = I(Fr(1, 50)) - I(ob["delta"])
            else:
                glob = I(QUARTER) * imin(mpost(HALF), 1 - Mpost(HALF)) * I(ob["delta"]) - I(Fr(1, 50))
            put(f"p2_reserve_{law}_{tag}_r{i}_global", glob)
            say(f"  {law:6s} p={str(p):7s} r={str(r):4s} {res['_why']:34s} pattern={res['_pattern']}"
                f" E={fmt(res['entry'], 9)} S={fmt(res['sale'], 9)} C2={fmt(res['two'], 9)}"
                f" R={fmt(res['proceeds'], 9)} Delta={ob['delta']} B(1/2)-6={fmt(gross(ob, HALF) - 6, 7)}"
                f" B(M)-6={fmt(gross(ob, Mpost(HALF)) - 6, 7)} flags={res['_flags']}")
    for i in range(2):
        put(f"margin_p2_reserve_{law}_exclude_gain{i}_B",
            RES[(law, "exclude", i)]["proceeds"] - RES[(law, "base", i)]["proceeds"])
        put(f"margin_p2_reserve_{law}_rev{i}_B",
            RES[(law, "deter", i)]["proceeds"] - RES[(law, "base", i)]["proceeds"])
say("  flat entry at exclusion reserves (E(r0)-E(r1)):",
    {law: fmt(RES[(law, 'exclude', 0)]['entry'] - RES[(law, 'exclude', 1)]['entry'], 3) for law in ("points", "bands")})
say("  formula rho+(1-rho)(b+lambda/2) =", fmt(I(QUARTER) + I(Fr(3, 4)) * (BB + LAM / 2)))
# p_H, weak top, and margins
M, m = Mpost(HALF), mpost(HALF)
ph = iv.sqrt(6 * (10 - 6 / M) - 9)
put("p2_reserve_ph", ph)
put("p2_reserve_weak_top", 10 - 6 / M)
put("margin_p2_ph_weak_B", ph - I(Fr(6, 5)))
put("margin_p2_deter_lower_B", I(Fr(31, 20)) - ph)
put("margin_p2_deter_upper_B", 10 - 6 / M - I(Fr(31, 20)))
put("margin_p2_reserve_admissible_top_B", M * I(Fr(413, 50)) - 6)
put("margin_p2_reserve_uniform_weak_B", I(QUARTER) * m * I(Fr(17, 20)) - I(Fr(1, 50)))
put("margin_p2_reserve_uniform_strong_B", I(QUARTER) * m * 1 - I(Fr(1, 50)))
d_ph = I(Fr(3, 2)) - ph + ph * ph / 2       # r/2 - p + 3p^2/(2r) at r = 3
put("margin_p2_ph_trade_B", I(QUARTER) * m * d_ph - I(Fr(1, 50)))
put("margin_p2_ph_prior_B", 6 - 3 / M)
say("  p_H =", fmt(ph), " 10-6/M =", fmt(10 - 6 / M), " p_H - 6/5 =", fmt(ph - I(Fr(6, 5)), 8))
# exact tuple at p_H (C1 admits the high cost at +1); objects in intervals
t0 = ph - ph * ph / 3
tH = I(Fr(3, 2)) + ph * ph / 6
gH = 10 - tH
say("  B(M) - 6 at p_H (identity gives 0):", fmt(M * gH - 6, 5))
aH, aL = X.masses(1, -1)
ent = {-1: rho, 0: rho, 1: I(1)}
for q in (-1, 0, 1):
    mq = pi * aH[q] / (pi * aH[q] + (1 - pi) * aL[q])
    put(f"p2_ph_price{q + 1}", t0 + ent[q] * d_ph * mq)
for cls, tj, qj in (("h", tH, 1), ("l", t0, -1)):
    pays = {}
    for q in (-1, 0, 1):
        pays[q] = iv.mpf(0) if q == 0 else q * (t0 + ent[q] * (tj - t0) - V[f"p2_ph_price{q + 1}"]) - I(Fr(1, 50))
        put(f"p2_ph_{cls}_pay{q + 1}", pays[q])
    others = [pays[q] for q in (-1, 0, 1) if q != qj]
    put(f"p2_ph_{cls}_choice", pays[qj] - imax(*others))
# endpoints
for nm, (H, L), p in (("endpoint", (P10, P1), Fr(10)), ("band_endpoint", BANDS, Fr(201, 20))):
    res, ob = node(H, L, HALF, p, QUARTER, Fr(6), Fr(1, 50), Fr(3))
    put_node(f"p2_{nm}_r1_", res)
    say(f"  {nm}: p={p} {res['_why']} pattern={res['_pattern']} E={fmt(res['entry'])} S={fmt(res['sale'])}"
        f" C2={fmt(res['two'])} R={fmt(res['proceeds'])} flags={res['_flags']}")
# necessity scan: point values, p in (1, 6/5]: flat entry (both strengths recruit at +1 only)
say("  scan p in (1, 6/5] step 1/200 (points): entry pattern at r0 and r1")
pats = set()
for j in range(1, 41):
    p = 1 + Fr(j, 200)
    for r in (Fr(6, 5), Fr(3)):
        res, ob = node(P10, P1, HALF, p, QUARTER, Fr(6), Fr(1, 50), r)
        pats.add((float(r), res.get("_profile"), res.get("_pattern")))
say("   patterns found:", sorted(pats, key=str))
say("  scan p in (21/20, 6/5] step 1/400 (narrow bands): band objects minus point objects, entry pattern")
pats, maxgap = set(), Fr(0)
for j in range(1, 61):
    p = Fr(21, 20) + Fr(j, 400)
    for r in (Fr(6, 5), Fr(3)):
        res, ob = node(BANDS[0], BANDS[1], HALF, p, QUARTER, Fr(6), Fr(1, 50), r)
        obp = auction(P10, P1, p, r)
        maxgap = max([maxgap] + [abs(ob[f] - obp[f]) for f in ("t0", "th", "tl", "gh", "gl", "delta")])
        pats.add((float(r), res.get("_profile"), res.get("_pattern")))
say("   largest |band - point| over t0, tH, tL, gH, gL, Delta:", maxgap, "; patterns:", sorted(pats, key=str))
say()

# ============================================================================
# 6b. Random-instance diagnostic of the general two-class proposition at B
# ============================================================================
say("== 6b. Random uniform classes, priors and strengths at calibration B (diagnostic) ==")
rng = random.Random(20261023)
tried = accepted = agree = own_agree = 0
bad_cases = []
while accepted < 300 and tried < 20000:
    tried += 1
    lL = Fr(rng.randint(11, 60), 20)
    hL = lL + Fr(rng.randint(0, 40), 20)
    lH = lL + Fr(rng.randint(0, 60), 20)
    hH = max(hL, lH) + Fr(rng.randint(0, 200), 20)
    if hH == lH and hL == lL and lH == lL:
        continue
    Hl, Ll = (lH, hH), (lL, hL)
    pi_ = Fr(rng.randint(5, 95), 100)
    rs = sorted(Fr(rng.randint(11, 400), 20) for _ in range(3))
    if len(set(rs)) < 3:
        continue
    obs = [auction(Hl, Ll, HALF, r) for r in rs]
    Mz, mz = Mpost(pi_), mpost(pi_)
    kap = imin(mz, 1 - Mz)
    c_lo, c_hi = gross(obs[0], pi_), gross(obs[1], Mz)
    k_lo, k_hi = I(obs[0]["delta"]), I(QUARTER) * kap * I(obs[1]["delta"])
    if sign(c_hi - c_lo) != "pos" or sign(k_hi - k_lo) != "pos":
        continue
    c_ = Fr(int(mid((c_lo + c_hi) / 2) * 10**15), 10**15)
    k_ = Fr(int(mid((k_lo + k_hi) / 2) * 10**15), 10**15)
    if sign(I(c_) - gross(obs[2], Mz)) != "pos":
        continue
    accepted += 1
    out = []
    for i, r in enumerate(rs):
        res, ob = node(Hl, Ll, pi_, HALF, QUARTER, c_, k_, r)
        eqs = pure_equilibria(ob, pi_, QUARTER, c_, k_)
        out.append((res.get("_profile"), res.get("_pattern"), [e[0] for e in eqs], res))
    pred = [((0, 0), (0, 0, 0)), ((1, -1), (0, 0, 1)), ((1, -1), (0, 0, 0))]
    ok = all(out[i][0] == pred[i][0] and out[i][1] == pred[i][1] and out[i][2] == [pred[i][0]] for i in range(3))
    agree += ok
    own_gain = out[1][3]["ownership"] - out[0][3]["ownership"]
    cond = (I(QUARTER) + I(Fr(3, 4)) * (BB + LAM)) * I(obs[1]["wh"]) - I(QUARTER) * I(obs[0]["wh"])
    own_agree += sign(own_gain) == sign(cond)
    if not ok:
        bad_cases.append((Hl, Ll, pi_, rs, c_, k_, [(o[0], o[1], o[2]) for o in out]))
say(f"   draws {tried}, instances meeting the strict hypotheses {accepted}, predicted outcome and unique pure"
    f" equilibrium at all three strengths {agree}, ownership sign equals condition sign {own_agree}")
for bc in bad_cases[:5]:
    say("   DISAGREE", bc)
say()

# ============================================================================
# 7. Payment rule
# ============================================================================
say("== 7. Payment rule (zero reserve) ==")


def pay_objects(eta: Fr, r: Fr, h=Fr(10), l=Fr(1)):
    """Integrate T_eta(R, theta) = (1-eta) min + eta max directly over R ~ U[0, r]."""
    def emin(th):
        return r / 2 if th >= r else th - th * th / (2 * r)

    def emax(th):
        return th if th >= r else th + (r - th) ** 2 / (2 * r)

    def T(th):
        return (1 - eta) * emin(th) + eta * emax(th)

    def gpos(th):  # E[(th - R)_+]
        return th - r / 2 if th >= r else th * th / (2 * r)
    return T(h) - T(l), (1 - eta) * gpos(h), (1 - eta) * gpos(l)


mism = 0
for j in range(0, 101):
    eta = Fr(j, 100)
    tag = f"{eta.numerator}_{eta.denominator}"
    for i, r in enumerate((Fr(6, 5), Fr(3))):
        sp, gh, gl = pay_objects(eta, r)
        closed = eta * 9 + (1 - 2 * eta) * ((r - 1) ** 2 / (2 * r))
        mism += closed != sp
        put(f"p2_payment_{tag}_r{i}_spread", sp)
        put(f"p2_payment_{tag}_r{i}_gh", gh)
        put(f"p2_payment_{tag}_r{i}_gl", gl)
say("direct integration vs closed form (13): mismatches =", mism)
s0 = pay_objects(Fr(0), Fr(6, 5))[0]
s1 = pay_objects(Fr(0), Fr(3))[0]
put("p2_payment_coefficient_spread_a0", s0)
put("p2_payment_coefficient_spread_b0", pay_objects(Fr(1), Fr(6, 5))[0] - s0)
put("p2_payment_coefficient_spread_a1", s1)
put("p2_payment_coefficient_spread_b1", pay_objects(Fr(1), Fr(3))[0] - s1)
put("p2_payment_coefficient_high0", pay_objects(Fr(0), Fr(6, 5))[1])
put("p2_payment_coefficient_high1", pay_objects(Fr(0), Fr(3))[1])
put("p2_payment_coefficient_low0", pay_objects(Fr(0), Fr(6, 5))[2])
put("p2_payment_coefficient_low1", pay_objects(Fr(0), Fr(3))[2])
put("p2_payment_coefficient_excess_change", s1 - s0)
say("Delta_eta(3) - Delta_eta(6/5) at eta = 0, 1/4, 1/2, 3/4:",
    [pay_objects(Fr(x, 4), Fr(3))[0] - pay_objects(Fr(x, 4), Fr(6, 5))[0] for x in range(4)])
say("coefficients:", s0, V["p2_payment_coefficient_spread_b0"], s1, V["p2_payment_coefficient_spread_b1"])
say()

# ============================================================================
# 8. Three-class collision and four-class groups
# ============================================================================
say("== 8. More than two classes ==")
PRI = (QUARTER, HALF, QUARTER)
OB8 = auction(P10, P1, Fr(1), Fr(8))
say("R~U[0,8], p=1: t0 =", OB8["t0"], " t(1), g(1) =", OB8["tl"], OB8["gl"], " t(10), g(10) =", OB8["th"], OB8["gh"])
W0 = (1 + 2 * B0 + LAM) / 2


def collision(w, stem):
    t = (I(OB8["tl"]), (1 - w) * I(OB8["tl"]) + w * I(OB8["th"]), I(OB8["th"]))
    g = (I(OB8["gl"]), w * I(OB8["gh"]), I(OB8["gh"]))
    sig = (-1, 0, 1)
    a = [{q: (1 - LAM) * I(ETA[q]) + (LAM if q == sig[j] else 0) for q in (-1, 0, 1)} for j in range(3)]
    means, prices, posts = {}, {}, {}
    rho_ = I(QUARTER)
    for qi, q in enumerate((-1, 0, 1)):
        d = sum((I(PRI[j]) * a[j][q] for j in range(3)), iv.mpf(0))
        post = [I(PRI[j]) * a[j][q] / d for j in range(3)]
        posts[q] = post
        for j in range(3):
            put(f"{stem}_q{qi}_mu{j}", post[j])
        means[q] = sum((post[j] * t[j] for j in range(3)), iv.mpf(0))
        prices[q] = I(OB8["t0"]) + rho_ * (means[q] - I(OB8["t0"]))
        put(f"{stem}_q{qi}_mean", means[q])
        put(f"{stem}_q{qi}_price", prices[q])
        prof = sum((post[j] * g[j] for j in range(3)), iv.mpf(0))
        say(f"   {stem} order {q}: posterior {[fmt(x, 8) for x in post]} mean {fmt(means[q], 10)}"
            f" price {fmt(prices[q], 10)} gross profit {fmt(prof, 8)} (c_H=10)")
    put(f"{stem}_mean_zero_minus_plus", means[0] - means[1])
    for j in range(3):
        pays = {}
        for qi, q in enumerate((-1, 0, 1)):
            pays[q] = iv.mpf(0) if q == 0 else q * rho_ * (t[j] - means[q]) - I(Fr(1, 8))
            put(f"{stem}_class{j}_pay{qi}", pays[q])
        others = [pays[q] for q in (-1, 0, 1) if q != sig[j]]
        put(f"{stem}_choice{j}", pays[sig[j]] - imax(*others))
    say(f"   {stem}: mean0-mean+ = {fmt(means[0] - means[1], 6)}; choices "
        f"{[fmt(V[f'{stem}_choice{j}'], 8) for j in range(3)]}; signs {[sign(V[f'{stem}_choice{j}']) for j in range(3)]}")
    return means, prices, posts


put("p2_many_weight", W0)
collision(W0, "p2_many")
put("p2_many_mean_zero_minus_plus", Fr(0))  # exact identity (checked below in rationals)
collision(W0 - I(Fr(1, 1000)), "p2_many_down")
collision(W0 + I(Fr(1, 1000)), "p2_many_up")
put("margin_p2_many_w_lower_B", W0)
put("margin_p2_many_w_upper_B", 1 - W0)
put("margin_p2_many_beta_B", BETA - Fr(1, 4))
put("p2_many_high_cost", Fr(10) - OB8["gh"])
# a valid common lower bound on class-3 posterior at every order: min over orders
c3 = [I(QUARTER) * BB / (BB + LAM / 4), I(QUARTER) * B0 / (B0 + LAM / 2), I(QUARTER) * (BB + LAM) / (BB + LAM / 4)]
say("   class-3 posterior at orders -1, 0, +1:", [fmt(x, 8) for x in c3],
    "; P2 bound (1/4) b/(b0+lambda/2) =", fmt(I(QUARTER) * BB / (B0 + LAM / 2), 8))
put("p2_many_low_cost", I(QUARTER) * BB / (B0 + LAM / 2) * I(OB8["gh"]))
# exact identity check in rationals at random rational slot parameters
rng = random.Random(7)
bad = 0
for _ in range(200):
    lam_ = Fr(rng.randint(1, 999), 1000)
    bet_ = Fr(rng.randint(1, 333), 1000)
    b_, b0_ = (1 - lam_) * bet_, (1 - lam_) * (1 - 2 * bet_)
    w_ = (1 + 2 * b0_ + lam_) / 2
    z0 = (b0_ * (w_ / 2 + Fr(1, 4)) + lam_ * w_ / 2) / (b0_ + lam_ / 2)
    z1 = (b_ * (w_ / 2 + Fr(1, 4)) + lam_ / 4) / (b_ + lam_ / 4)
    bad += z0 != z1
say("   exact identity z0 = z1 at 200 random rational (lambda, beta): failures =", bad)

say(" four-class groups:")
VALS = (Fr(1), Fr(1001, 1000), Fr(9999, 1000), Fr(10))
PR4 = (QUARTER,) * 4
o0 = [X.kernel(v, HALF, Fr(6, 5), True) for v in VALS]
o1 = [X.kernel(v, HALF, Fr(3), True) for v in VALS]
t0w = [o[0] for o in o0]
t1 = [o[0] for o in o1]
put("p2_groups_weak_range", Fr(1, 50) - (max(t0w) - min(t0w)))
put("p2_groups_weak_cost", Fr(6) - sum(PR4[j] * o0[j][1] for j in range(4)))
best_hi, best_lo = None, None
for mask in range(16):
    w = [I(E) if (mask >> j) & 1 else I(1) for j in range(4)]
    den = sum((I(PR4[j]) * w[j] for j in range(4)), iv.mpf(0))
    mean = sum((I(PR4[j]) * w[j] * I(t1[j]) for j in range(4)), iv.mpf(0)) / den
    best_hi = mean if best_hi is None else imax(best_hi, mean)
    best_lo = mean if best_lo is None else imin(best_lo, mean)
gam_h = I(min(t1[2], t1[3])) - best_hi
gam_l = best_lo - I(max(t1[0], t1[1]))
gam = imin(gam_h, gam_l)
say("   strong t:", [str(x) for x in t1], " max/min feasible mean:", fmt(best_hi, 10), fmt(best_lo, 10))
say("   gamma_H =", fmt(gam_h, 10), " gamma_L =", fmt(gam_l, 10))
put("p2_groups_gamma", gam)
put("p2_groups_trade", I(QUARTER) * gam - I(Fr(1, 50)))
gl_bar = (o1[0][1] + o1[1][1]) / 2
gh_bar = (o1[2][1] + o1[3][1]) / 2
put("p2_groups_profit_gap", gh_bar - gl_bar)
put("p2_groups_top", I(gl_bar) + Mpost(HALF) * I(gh_bar - gl_bar) - 6)
# verify the strong group tuple directly: forced orders, group posterior, entry, prices, deviations
aH, aL = X.masses(1, -1)
zq = {q: pi * aH[q] / (pi * aH[q] + (1 - pi) * aL[q]) for q in (-1, 0, 1)}
tl_bar, th_bar = (t1[0] + t1[1]) / 2, (t1[2] + t1[3]) / 2
entq = {q: rho + (1 - rho) * (1 if sign(I(gl_bar) + zq[q] * I(gh_bar - gl_bar) - 6) == "pos" else 0) for q in zq}
mean_q = {q: I(tl_bar) + zq[q] * I(th_bar - tl_bar) for q in zq}
P_q = {q: I(Fr(5, 12)) + entq[q] * (mean_q[q] - I(Fr(5, 12))) for q in zq}
worst = None
for j in range(4):
    want = 1 if j >= 2 else -1
    pays = {q: (iv.mpf(0) if q == 0 else q * entq[q] * (I(t1[j]) - mean_q[q]) - I(Fr(1, 50))) for q in zq}
    margin = pays[want] - imax(*[pays[q] for q in zq if q != want])
    worst = margin if worst is None else imin(worst, margin)
say("   group tuple: entry by order", {q: fmt(entq[q], 6) for q in zq}, " prices",
    {q: fmt(P_q[q], 8) for q in zq}, " smallest class choice margin", fmt(worst, 8))
say("   E1 = rho + (1-rho)(b + lambda/2) =", fmt(rho + (1 - rho) * (BB + LAM / 2), 10))
say()

# ============================================================================
# 9. Comparison with the registry
# ============================================================================
say("== 9. Registry comparison ==")
REG = os.path.join(TEAM, "registry", "P2_auction.csv")
rows = list(csv.DictReader(open(REG)))
keys = [r["key"] for r in rows]
dups = sorted({k for k in keys if keys.count(k) > 1})
say("rows", len(rows), " duplicate keys", dups)


def parse(s):
    s = s.strip()
    if "/" in s:
        return Fr(s)
    return mp.mpf(s)


def display_ok(disp, mine):
    """Is the registry display a correct rounding of my enclosure?"""
    d = disp.strip()
    a, b = ends(mine)
    if "/" in d or re.fullmatch(r"-?\d+", d):
        target = Fr(d)
        if isinstance(mine, Fr):
            return mine == target, "exact"
        t = mp.mpf(target.numerator) / target.denominator
        return (a <= t <= b) or abs((a + b) / 2 - t) < mp.mpf(10) ** -40, "exact-vs-interval"
    mm = re.fullmatch(r"(-?\d+)(?:\.(\d+))?(?:e([-+]?\d+))?", d)
    if not mm:
        return False, "unparsed"
    places = len(mm.group(2) or "")
    expo = int(mm.group(3) or 0)
    ulp = mp.mpf(10) ** (expo - places)
    t = mp.mpf(d)
    lo_ok = abs(a - t) <= ulp / 2 + mp.mpf(10) ** -50
    hi_ok = abs(b - t) <= ulp / 2 + mp.mpf(10) ** -50
    return lo_ok and hi_ok, f"ulp={mp.nstr(ulp, 3)}"


out_rows, missing, vbad, dbad, signbad = [], [], [], [], []
for r in rows:
    k = r["key"]
    if k not in V:
        missing.append(k)
        out_rows.append(dict(key=k, registry_value=r["value"], registry_display=r["display"],
                             xp2_value="", abs_diff="", value_match="not recomputed",
                             display_match="", note=""))
        continue
    mine = V[k]
    reg = parse(r["value"])
    a, b = ends(mine)
    regf = mp.mpf(reg.numerator) / reg.denominator if isinstance(reg, Fr) else reg
    if isinstance(mine, Fr) and isinstance(reg, Fr):
        diff = abs(mine - reg)
        vmatch = diff == 0
        diff = mp.mpf(diff.numerator) / diff.denominator
    else:
        diff = max(abs(a - regf), abs(b - regf))
        vmatch = diff <= mp.mpf(10) ** -40 * max(1, abs(regf))
    dmatch, how = display_ok(r["display"], mine)
    if not vmatch:
        vbad.append((k, r["value"], fmt(mine, 20), mp.nstr(diff, 5)))
    if not dmatch:
        dbad.append((k, r["display"], fmt(mine, 15), how))
    if sign(mine) not in ("zero",) and (regf > 0) != (a > 0) and regf != 0:
        signbad.append((k, r["value"], fmt(mine, 10)))
    out_rows.append(dict(key=k, registry_value=r["value"], registry_display=r["display"],
                         xp2_value=fmt(mine, 30), abs_diff=mp.nstr(diff, 5),
                         value_match="yes" if vmatch else "NO", display_match="yes" if dmatch else "NO",
                         note=how))
say("recomputed:", len(rows) - len(missing), " not recomputed:", len(missing))
say("value mismatches beyond 1e-40 relative:", len(vbad))
for x in vbad:
    say("   VALUE", x)
say("display mismatches (registry display is not a correct rounding of the enclosure):", len(dbad))
for x in dbad:
    say("   DISPLAY", x)
say("sign disagreements:", len(signbad))
for x in signbad:
    say("   SIGN", x)
if missing:
    say("not recomputed keys:", missing)
extra = sorted(set(V) - set(keys))
say("keys recomputed here but absent from the registry:", extra)
# tiny margins whose 6-decimal display hides the value
tiny = [(r["key"], r["display"], r["value"][:14]) for r in rows
        if re.fullmatch(r"-?0\.0+", r["display"].strip()) and parse(r["value"]) != 0]
say("rows whose display shows 0.000000 or -0.000000 for a nonzero value:", tiny)
neg_zero = [r["key"] for r in rows if r["display"].strip().startswith("-0.000000")]
say("rows displayed with a minus sign and only zeros:", neg_zero)

say()
say("== 10. Key collisions with the other registry files ==")
p2 = {r["key"]: r for r in rows}
for f in ("P1_core", "P3_research", "P4_information", "P5_observables", "registry"):
    path = os.path.join(TEAM, "registry", f + ".csv")
    if not os.path.exists(path):
        say(f, "absent")
        continue
    other = list(csv.DictReader(open(path)))
    shared = [o for o in other if o["key"] in p2]
    diffs = []
    for o in shared:
        x, y = parse(p2[o["key"]]["value"]), parse(o["value"])
        xf = mp.mpf(x.numerator) / x.denominator if isinstance(x, Fr) else x
        yf = mp.mpf(y.numerator) / y.denominator if isinstance(y, Fr) else y
        dd = abs(xf - yf)
        if dd > mp.mpf(10) ** -12 * max(1, abs(xf)) or p2[o["key"]]["display"] != o["display"]:
            diffs.append((o["key"], p2[o["key"]]["value"][:24], p2[o["key"]]["display"], o["value"][:24], o["display"]))
    say(f"{f}: {len(other)} rows, {len(shared)} shared with P2, {len(diffs)} differ in value (>1e-12 rel) or display")
    for d in diffs:
        say("   COLLISION", d)
# same quantity under different keys in P1 (starter keys)
p1 = {r["key"]: r for r in csv.DictReader(open(os.path.join(TEAM, "registry", "P1_core.csv")))}
pairs = (("entry_r0", "p2_base_r0_entry"), ("entry_r1_B", "p2_base_r1_entry"), ("entry_r2", "p2_base_r2_entry"),
         ("own_r0", "p2_base_r0_ownership"), ("own_r1_B", "p2_base_r1_ownership"),
         ("own_r2_B", "p2_base_r2_ownership"))
for a_, b_ in pairs:
    if a_ in p1:
        x, y = parse(p1[a_]["value"]), V[b_]
        xf = mp.mpf(x.numerator) / x.denominator if isinstance(x, Fr) else x
        say(f"  P1 {a_}={p1[a_]['display']}  vs  P2 {b_}={p2[b_]['display']}  |diff|={mp.nstr(abs(xf - mid(y)), 3)}")
    else:
        say(f"  P1 has no key {a_}")

# ============================================================================
# 11. Outputs
# ============================================================================
with open(os.path.join(HERE, "xp2_diff.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(out_rows[0].keys()))
    w.writeheader()
    w.writerows(out_rows)
with open(os.path.join(HERE, "xp2_values.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["key", "midpoint", "lower", "upper", "exact"])
    for k in sorted(V):
        a, b = ends(V[k])
        w.writerow([k, mp.nstr((a + b) / 2, 30), mp.nstr(a, 40), mp.nstr(b, 40),
                    str(V[k]) if isinstance(V[k], Fr) else ""])
man = dict(script="xp2_check.py", engine="xp2_engine.py", python=platform.python_version(),
           mpmath=mpmath.__version__, iv_dps=iv.dps,
           registry_sha256=hashlib.sha256(open(REG, "rb").read()).hexdigest(),
           outputs={f: hashlib.sha256(open(os.path.join(HERE, f), "rb").read()).hexdigest()
                    for f in ("xp2_diff.csv", "xp2_values.csv")},
           seconds=round(time.time() - T_START, 2))
with open(os.path.join(HERE, "manifest.json"), "w") as fh:
    json.dump(man, fh, indent=1)
say()
say("elapsed seconds:", round(time.time() - T_START, 2))
