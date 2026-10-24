"""Numbers for proof package P1 (R2, R3, R4) at calibration B; writes registry/P1_core.csv.

Exact inputs are Fractions. Every quantity that involves Euler's number e is an outward
interval (mpmath.iv, 50 digits). Roots of rational functions use exact rational bisection
(bracket width at most 1e-40). Printed enclosures come from the exact endpoints: the lower
end rounds down and the upper end rounds up. A 6-place display counts as certified only if
both exact ends round to it.
Run from the repository root:
  .venv/bin/python audit/slot_manuscript_2026_10_23/scripts/P1_core/p1_numbers.py
"""
from fractions import Fraction as Fr

from mpmath import iv

from p1_common import (HERE, REGISTRY, Log, Registry, auction, tau, Delta, J, B,
                       h, ell, p, rho, cH, k, pi_half, r0, r1, r2, beta_B,
                       ivq, ivbr, ivends, ivstr, qbrstr, ivsign, round_dec, sig_str,
                       bisect_root, frak_r, value_str, e_series_bracket)

SRC = "scripts/P1_core/p1_numbers.py"
LOGNAME = "scripts/P1_core/p1_numbers.log"
log = Log(HERE / "p1_numbers.log")
reg = Registry(SRC, LOGNAME)
CA, AN, IN = "computer-assisted", "analytical", "input"


def d6(x):
    """Six-place display of an exact rational (for log lines)."""
    return round_dec(x, 6)


def d9(x):
    return round_dec(x, 9)


log("P1_core numbers at calibration B. Intervals are outward enclosures at 50 digits;")
log("printed enclosures round the lower end down and the upper end up (24 places).")
log("Benchmark primitives (h, ell, p, rho, c_H, k, pi) =", h, ell, p, rho, cH, k, pi_half,
    "; strengths r0, r1, r2 =", r0, r1, r2)

# ------------------------------------------------------------------ A. slot primitives
E = iv.e
eS_lo, eS_hi = e_series_bracket(110)
e_lo, e_hi = ivends(E)
log("\nA. Slot primitives")
log("   e: mpmath.iv enclosure", ivstr(E))
log("   e: series bracket S_110 < e < S_110 + 112/(111 * 111!) =", qbrstr(eS_lo, eS_hi, 60))
log("   the mpmath.iv enclosure contains the series bracket:", e_lo <= eS_lo and eS_hi <= e_hi)
u = E - 1
beta = ivq(beta_B)
lam = u * beta / (1 + u * beta)
b = beta / (1 + u * beta)
b0 = (1 - lam) * (1 - 2 * beta)
M = (1 + u) / (2 + u)
m = 1 / (2 + u)
log("   u = e - 1 =", ivstr(u))
log("   beta =", beta_B, "(exact decimal)")
log("   lambda = u beta/(1 + u beta) =", ivstr(lam))
log("   b = (1 - lambda) beta = beta/(1 + u beta) =", ivstr(b), "; check lambda/b - u =", ivstr(lam / b - u))
log("   b0 = (1 - lambda)(1 - 2 beta) =", ivstr(b0), "; b0 - b =", ivstr(b0 - b), "sign", ivsign(b0 - b))
log("   M(1/2) = (1+u)/(2+u) = e/(1+e) =", ivstr(M), "; m(1/2) = 1/(1+e) =", ivstr(m))
reg.add_iv("u_B", u, IN, "1 + u = e (declared)")
reg.add("beta_B", "294655/1000000", "0.294655", IN, "exact decimal (declared)")
reg.add_iv("lambda_B", lam, CA, "lambda = u beta/(1 + u beta)")
reg.add_iv("b_B", b, CA, "b = (1 - lambda) beta")
reg.add_iv("b0_B", b0, CA, "liquidity abstention probability (1 - lambda)(1 - 2 beta)")
reg.add_iv("M_half_B", M, CA, "M(1/2) = e/(1 + e)")
reg.add_iv("m_half_B", m, CA, "m(1/2) = 1/(1 + e)")

# ------------------------------------------------------------------ B. auction objects
log("\nB. Auction objects (exact) at the three strengths")
for name, r in (("r0", r0), ("r1", r1), ("r2", r2)):
    a = auction(r)
    log(f"   r = {r}: t0 {a['t0']}, tH {a['tH']}, tL {a['tL']}, gH {a['gH']}, gL {a['gL']}, Delta {a['D']},"
        f" tau {tau(r)} = {d9(tau(r))}, B(1/2) {B(r, pi_half)}")
    reg.add_dec_exact(f"tau_{name}", tau(r), AN, "tau(r) = (c_H - g_L)/(g_H - g_L)")
    reg.add_frac(f"tau_{name}_frac", tau(r), AN)
    reg.add_dec_exact(f"Delta_{name}", a["D"], AN, "Delta_T(r) = (r - ell)^2/(2r)")

# ------------------------------------------------------------------ C. Proposition 2
log("\nC. Proposition 2 at calibration B, prior 1/2")
D0, D1, D2 = Delta(r0), Delta(r1), Delta(r2)
kappa = m  # at prior 1/2, min{m, 1 - M} = m = 1 - M
E1 = ivq(rho) + ivq(1 - rho) * (b + lam / 2)
eH = ivq(rho) + ivq(1 - rho) * (b + lam)
eL = ivq(rho) + ivq(1 - rho) * b
own1 = eH / 2
log("   entry at r1: rho + (1 - rho)(b + lambda/2) =", ivstr(E1))
log("   class-conditional entry e_H =", ivstr(eH), "; e_L =", ivstr(eL))
log("   high-class ownership at r1 = e_H/2 (W_H = 1) =", ivstr(own1))
reg.add_dec_exact("entry_r0", rho, AN, "no informed trade; entry rho")
reg.add_iv("entry_r1_B", E1, CA, "rho + (1 - rho)(b + lambda/2)")
reg.add_dec_exact("entry_r2", rho, AN, "full orders; no order recruits")
reg.add_iv("eH_r1_B", eH, CA, "entry given class H at r1")
reg.add_iv("eL_r1_B", eL, CA, "entry given class L at r1")
reg.add_dec_exact("own_r0", rho / 2, AN, "pi rho W_H with W_H = 1")
reg.add_iv("own_r1_B", own1, CA, "pi [rho + (1 - rho)(b + lambda)] W_H with W_H = 1")
reg.add_dec_exact("own_r2_B", rho / 2, AN, "pi rho W_H with W_H = 1; entry returns to rho")
# Prices on every order
for name, r in (("r0", r0), ("r1", r1), ("r2", r2)):
    a = auction(r)
    t0, tL, D = ivq(a["t0"]), ivq(a["tL"]), ivq(a["D"])
    if name == "r0":
        P = t0 + ivq(rho) * (tL - t0 + D / 2)
        log(f"   prices at r0 (every order, posterior 1/2, entry rho): {ivstr(P)}")
        reg.add_iv("price_r0", P, CA, "t0 + rho (t_L - t0 + Delta/2), every order")
        continue
    ent_plus = ivq(1) if name == "r1" else ivq(rho)
    Pm = t0 + ivq(rho) * (tL - t0 + D * m)
    P0 = t0 + ivq(rho) * (tL - t0 + D / 2)
    Pp = t0 + ent_plus * (tL - t0 + D * M)
    log(f"   prices at {name}: P(-1) = {ivstr(Pm)}, P(0) = {ivstr(P0)}, P(+1) = {ivstr(Pp)}")
    reg.add_iv(f"price_{name}_m1_B", Pm, CA, f"price after a sale at {name}")
    reg.add_iv(f"price_{name}_0_B", P0, CA, f"price after no order at {name}")
    reg.add_iv(f"price_{name}_p1_B", Pp, CA, f"price after a purchase at {name}")

log("\n   Hypotheses of Proposition 2 and their margins at B (prior 1/2)")
mg = {}
mg["weakcost"] = ivq(cH - B(r0, pi_half))
mg["recruit"] = ivq(B(r1, 0)) + M * ivq(B(r1, 1) - B(r1, 0)) - ivq(cH)
mg["kweak"] = ivq(k - D0)
mg["kstrong"] = ivq(rho) * kappa * ivq(D1) - ivq(k)
mg["return"] = ivq(cH) - (ivq(B(r2, 0)) + M * ivq(B(r2, 1) - B(r2, 0)))
mg["return_post"] = ivq(tau(r2)) - M
mg["recruit_post"] = M - ivq(tau(r1))
# implied (redundant) inequalities
mg["implied_prior_r1"] = ivq(cH - B(r1, pi_half))
mg["implied_kstrong_r2"] = ivq(rho) * kappa * ivq(D2) - ivq(k)
mg["implied_prior_r2"] = ivq(cH - B(r2, pi_half))
labels = {
    "weakcost": "c_H - B_0(pi)", "recruit": "B_1(M) - c_H", "kweak": "k - Delta_0",
    "kstrong": "rho kappa Delta_1 - k", "return": "c_H - B_2(M)",
    "return_post": "tau(r2) - M (posterior units)", "recruit_post": "M - tau(r1) (posterior units)",
    "implied_prior_r1": "c_H - B_1(pi) (implied)", "implied_kstrong_r2": "rho kappa Delta_2 - k (implied)",
    "implied_prior_r2": "c_H - B_2(pi) (implied)"}
for key, val in mg.items():
    log(f"   {labels[key]:40s} {ivstr(val)}  sign {ivsign(val)}")
reg.add_dec_exact("margin_weakcost_B", cH - B(r0, pi_half), AN, "c_H - B_0(pi) = 287/240; free of the slot")
reg.add_iv("margin_recruit_B", mg["recruit"], CA, "B_1(M) - c_H")
reg.add_dec_exact("margin_kweak_B", k - D0, AN, "k - Delta_0 = 1/300; free of the slot")
reg.add_iv("margin_kstrong_B", mg["kstrong"], CA, "rho min{m, 1 - M} Delta_1 - k")
reg.add_iv("margin_return_B", mg["return"], CA, "c_H - B_2(M)")
reg.add_iv("margin_return_post_B", mg["return_post"], CA, "tau(r2) - M: the return margin in posterior units")
reg.add_iv("margin_recruit_post_B", mg["recruit_post"], CA, "M - tau(r1) in posterior units")
reg.add_dec_exact("margin_implied_prior_r1", cH - B(r1, pi_half), AN, "c_H - B_1(pi) = 41/24 (implied)")
reg.add_iv("margin_kstrong2_B", mg["implied_kstrong_r2"], CA, "rho kappa Delta_2 - k (implied)")
reg.add_dec_exact("margin_implied_prior_r2", cH - B(r2, pi_half), AN, "c_H - B_2(pi) (implied)")
reg.add_dec_exact("margin_tau_r0_half", tau(r0) - pi_half, AN, "tau(r0) - 1/2 = 41/308: the prior never recruits on the path")
log("   tau(r0) - 1/2 =", tau(r0) - pi_half, "=", d9(tau(r0) - pi_half))
log("   strong trading bound at r2 holds for M < 1 - k/(rho Delta(r2)) =", 1 - k / (rho * Delta(r2)),
    "=", d9(1 - k / (rho * Delta(r2))))

# ------------------------------------------------------------------ D. admissible region
log("\nD. Admissible region at the benchmark (prior 1/2)")
u_lo, u_hi = Fr(82, 59), Fr(2686, 1559)
M_lo, M_hi = tau(r1), tau(r2)
log("   M band (tau(3), tau(18/5)) =", M_lo, M_hi, "; u band:", u_lo, u_hi,
    "; check (1+u)/(2+u) at the ends:", (1 + u_lo) / (2 + u_lo), (1 + u_hi) / (2 + u_hi))
u_k = Fr(19, 3)
log("   k < rho (1 - M) Delta(3) <=> M < 22/25 <=> u < 19/3 =", d9(u_k), "(slack against u_hi)")
reg.add_dec_exact("u_lo", u_lo, AN, "u > 82/59 <=> M > tau(3)")
reg.add_frac("u_lo_frac", u_lo, AN)
reg.add_dec_exact("u_hi", u_hi, AN, "u < 2686/1559 <=> M < tau(18/5)")
reg.add_frac("u_hi_frac", u_hi, AN)
reg.add_dec_exact("M_lo", M_lo, AN, "tau(3)")
reg.add_frac("M_lo_frac", M_lo, AN)
reg.add_dec_exact("M_hi", M_hi, AN, "tau(18/5)")
reg.add_frac("M_hi_frac", M_hi, AN)
reg.add_dec_exact("u_kstrong", u_k, AN, "the strong trading-cost condition at prior 1/2 is u < 19/3")
mu_lo, mu_hi = u - ivq(u_lo), ivq(u_hi) - u
log("   u - u_lo =", ivstr(mu_lo), "; u_hi - u =", ivstr(mu_hi))
reg.add_iv("margin_u_lo_B", mu_lo, CA, "u - 82/59")
reg.add_iv("margin_u_hi_B", mu_hi, CA, "2686/1559 - u")
lam_lo = 82 * beta_B / (59 + 82 * beta_B)
lam_hi = 2686 * beta_B / (1559 + 2686 * beta_B)
log("   lambda range at beta_B:", lam_lo, "=", d9(lam_lo), ";", lam_hi, "=", d9(lam_hi))
log("   lambda_B - lambda_lo =", ivstr(lam - ivq(lam_lo)), "; lambda_hi - lambda_B =", ivstr(ivq(lam_hi) - lam))
reg.add_dec_exact("lambda_lo_B", lam_lo, AN, "82 beta/(59 + 82 beta) at beta_B")
reg.add_dec_exact("lambda_hi_B", lam_hi, AN, "2686 beta/(1559 + 2686 beta) at beta_B")
reg.add_iv("margin_lambda_lo_B", lam - ivq(lam_lo), CA, "lambda_B - lambda_lo_B (exact cutoff 82 beta/(59 + 82 beta))")
reg.add_iv("margin_lambda_hi_B", ivq(lam_hi) - lam, CA, "lambda_hi_B - lambda_B (exact cutoff 2686 beta/(1559 + 2686 beta))")
third = Fr(1, 3)
reg.add_dec_exact("lambda_lo_third", 82 * third / (59 + 82 * third), AN, "82/259 at beta = 1/3")
reg.add_dec_exact("lambda_hi_third", 2686 * third / (1559 + 2686 * third), AN, "2686/7363 at beta = 1/3")
reg.add_dec_exact("margin_beta_B", third - beta_B, AN,
                  "1/3 - beta_B: slack in the structural weak restriction beta <= 1/3 (not a strict hypothesis)")
log("   1/3 - beta_B =", third - beta_B, "=", d9(third - beta_B), "(slack in a structural weak restriction)")

# ------------------------------------------------------------------ E. prior range at B
log("\nE. Prior range at B (other benchmark inputs fixed)")
eiv = E
p_lo = ivq(141) / (ivq(141) + 59 * eiv)
p_hi = ivq(4245) / (ivq(4245) + 1559 * eiv)
p_klo = 3 * eiv / (22 + 3 * eiv)
p_khi = ivq(22) / (22 + 3 * eiv)
log("   M(pi) > tau(3)    <=> pi > 141/(141 + 59 e)     =", ivstr(p_lo))
log("   M(pi) < tau(18/5) <=> pi < 4245/(4245 + 1559 e) =", ivstr(p_hi))
log("   B_{6/5}(pi) < c_H <=> pi < tau(6/5) = 195/308   =", d9(tau(r0)))
log("   kappa(pi) > 3/25  <=> pi in (3e/(22 + 3e), 22/(22 + 3e)) =", ivstr(p_klo), ivstr(p_khi))
log("   Delta(6/5) < k holds for every prior.")
log("   All three parts: (", ivstr(p_lo), ",", ivstr(p_hi), ")")
log("   Parts (i) and (ii): (", ivstr(p_lo), ", 195/308 )")
reg.add_iv("prior_lo_B", p_lo, CA, "141/(141 + 59 e)")
reg.add_iv("prior_hi_B", p_hi, CA, "4245/(4245 + 1559 e)")
reg.add_dec_exact("prior_ii_hi", tau(r0), AN, "parts (i)-(ii): pi < tau(6/5) = 195/308")
reg.add_iv("prior_kappa_lo_B", p_klo, CA, "3e/(22 + 3e)")
reg.add_iv("prior_kappa_hi_B", p_khi, CA, "22/(22 + 3e)")
reg.add_iv("margin_prior_lo_B", ivq(pi_half) - p_lo, CA, "1/2 - prior_lo_B (exact cutoff 141/(141 + 59 e))")
reg.add_iv("margin_prior_hi_B", p_hi - ivq(pi_half), CA, "prior_hi_B - 1/2 (exact cutoff 4245/(4245 + 1559 e))")

# ------------------------------------------------------------------ F. Proposition 3 thresholds
log("\nF. Proposition 3 thresholds (exact bisection; bracket width <= 1e-40)")
rA = bisect_root(lambda r: J(r) - k, r0, r2)
rJ = bisect_root(lambda r: rho * J(r) - k, r0, r2)
rS_ = bisect_root(lambda r: rho * Delta(r) * tau(r) - k, r0, r2)
for nm, br, fn in (("r_A", rA, "J - k"), ("r_J", rJ, "rho J - k"), ("r_star", rS_, "rho Delta tau - k")):
    log(f"   {nm} in {qbrstr(br[0], br[1], 45)}; {fn} at the ends has signs "
        f"{'-' if br[2] < 0 else '+'} and {'-' if br[3] < 0 else '+'}")
reg.add_bracket("rA", rA[0], rA[1], CA, "J(r) = Delta(r)(1 - tau(r)) = k; slot-free")
reg.add_bracket("rJ", rJ[0], rJ[1], CA, "rho J(r) = k; slot-free; end of the non-recruiting mixed branch")
reg.add_bracket("rstar", rS_[0], rS_[1], CA, "rho Delta(r) tau(r) = k; slot-free")
# tau and Delta are increasing on the path, so the images of the brackets are brackets.
tA = (tau(rA[0]), tau(rA[1]))
tJ = (tau(rJ[0]), tau(rJ[1]))
tS = (tau(rS_[0]), tau(rS_[1]))
reg.add_bracket("tau_rA", tA[0], tA[1], CA, "tau(r_A)")
reg.add_bracket("piA_hi", tA[0], tA[1], CA, "upper end of the prior window = tau(r_A); slot-free")
reg.add_bracket("tau_rJ", tJ[0], tJ[1], CA, "tau(r_J)")
reg.add_bracket("pimax", tS[0], tS[1], CA, "largest prior with coexistence under C1 = tau(r_star); slot-free")
reg.add_bracket("Delta_rA", Delta(rA[0]), Delta(rA[1]), CA, "Delta(r_A) = k/(1 - tau(r_A))")
rN = (29 + iv.sqrt(ivq(216))) / 25
rN2 = frak_r(ivq(2 * k / rho))
log("   r_N = (29 + 6 sqrt 6)/25 =", ivstr(rN), "; frak_r(2k/rho) =", ivstr(rN2))
reg.add_iv("rN", rN, AN, "(29 + 6 sqrt 6)/25 = frak_r(2k/rho); display certified by interval")
rF = frak_r(ivq(k) * (1 + eiv))
rS = frak_r(4 * ivq(k) * (1 + eiv))
log("   r_F = frak_r(k/(1 - M)) = frak_r(k(1 + e)) =", ivstr(rF))
log("   r_S = frak_r(k/(rho m)) = frak_r(4k(1 + e)) =", ivstr(rS))
reg.add_iv("rF_B", rF, CA, "frak_r(k/(1 - M)) with 1 - M = 1/(1 + e)")
reg.add_iv("rS_B", rS, CA, "frak_r(k/(rho m)); full sales from here; also the full-order uniqueness bound")
a_ = M * ivq(h) - ivq(cH)
rC = (a_ + iv.sqrt(a_ * a_ + M * ((1 - M) * ivq(ell * ell) - ivq(p * p)))) / M
log("   r_C = [Mh - c_H + sqrt((Mh - c_H)^2 + M((1 - M) ell^2 - p^2))]/M =", ivstr(rC))
BrC = (ivq(ell * ell) - ivq(p * p)) / (2 * rC) + M * (ivq(h) - rC / 2 - ivq(ell * ell) / (2 * rC))
log("   check B_{r_C}(M) - c_H =", ivstr(BrC - ivq(cH)))
reg.add_iv("rC_B", rC, CA, "B_r(M) = c_H")
tA_iv = ivbr(*tA)
pA_lo = tA_iv / (tA_iv + (1 - tA_iv) * eiv)
log("   pi_A_lo = tau_A/(tau_A + (1 - tau_A) e) in", ivstr(pA_lo))
reg.add_iv("piA_lo_B", pA_lo, CA, "lower end of the prior window: M(pi) = tau(r_A)")
reg.add_iv("margin_piA_lo_B", ivq(pi_half) - pA_lo, CA, "1/2 - piA_lo_B")
reg.add_bracket("margin_piA_hi", tA[0] - pi_half, tA[1] - pi_half, CA, "tau(r_A) - 1/2")
log("   ordering margins (r units); each gap subtracts the whole bracket of each root:")
rA_iv, rJ_iv = ivbr(rA[0], rA[1]), ivbr(rJ[0], rJ[1])
gaps = [("rA_r0", rA_iv - ivq(r0)), ("rF_rA", rF - rA_iv), ("rN_rF", rN - rF),
        ("rJ_rN", rJ_iv - rN), ("rS_rJ", rS - rJ_iv), ("r1_rS", ivq(r1) - rS),
        ("rC_r1", rC - ivq(r1)), ("r2_rC", ivq(r2) - rC)]
for nm, g in gaps:
    log(f"     {nm}: {ivstr(g)} sign {ivsign(g)}")
    reg.add_iv(f"gap_{nm}_B", g, CA, "difference of consecutive thresholds at B")

# ------------------------------------------------------------------ G. entry along the branches
log("\nG. Entry along the branches at B (prior 1/2)")


def mb_entry(r):
    return ivq(rho) + ivq(1 - rho) * b * ivq(Delta(r)) / (2 * ivq(k))


def th_entry(r):
    D, t = ivq(Delta(r)), ivq(tau(r))
    return ivq(rho) + (b / 2) * (ivq(k) - ivq(rho) * D * (1 - t)) / (D * (1 - t) ** 2)


eA = ivq(rho) + ivq(1 - rho) * b / (2 * (1 - tA_iv))
log("   entry at r_A on the threshold point: rho + (1 - rho) b/(2(1 - tau_A)) =", ivstr(eA))
reg.add_iv("entry_rA_B", eA, CA, "entry at r_A: the threshold equilibrium (investor and challenger indifferent)")
for r, nm in ((Fr(7, 5), "r140"), (Fr(29, 20), "r145")):
    v = mb_entry(r)
    log(f"   mixed recruiting branch at r = {r}: entry {ivstr(v)}; below E1: {ivsign(E1 - v)}")
    reg.add_iv(f"entry_mb_{nm}_B", v, CA, f"rho + (1 - rho) b Delta(r)/(2k) at r = {r}")
for r, nm in ((Fr(31, 20), "r155"), (Fr(8, 5), "r160"), (Fr(33, 20), "r165")):
    v = th_entry(r)
    estar = k / J(r)
    log(f"   r = {r}: full branch entry = E1 {ivstr(E1)}; threshold branch (challenger mixes) entry {ivstr(v)};"
        f" e* = k/J = {d9(estar)}; challenger preparation prob. {d6((estar - rho) / (1 - rho))}")
    reg.add_iv(f"entry_th_{nm}_B", v, CA, f"threshold branch entry at r = {r} (challenger mixes)")
    reg.add_dec_exact(f"estar_{nm}", estar, AN, f"entry after a purchase on the threshold branch at r = {r}")
log("   threshold-branch entry at r_J equals rho (k = rho J).")
# interior rates at sample strengths (prior 1/2)
log("\n   Interior rates at prior 1/2 (effective rates s = lambda sigma_H(+1), t = lambda sigma_L(-1))")
for r in (Fr(7, 5), Fr(29, 20)):
    sb = b * (ivq(Delta(r)) / ivq(k) - 2)
    log(f"   r = {r}: recruiting mixed purchase rate s = b(Delta/k - 2) = {ivstr(sb)}; s/lambda = {ivstr(sb / lam)}")
for r in (Fr(9, 5), Fr(19, 10)):
    sa = b * (ivq(rho * Delta(r) / k) - 2)
    log(f"   r = {r}: non-recruiting mixed rate s = t = b(rho Delta/k - 2) = {ivstr(sa)}; s/lambda = {ivstr(sa / lam)}")
for r in (Fr(2), Fr(21, 10)):
    tt = b * (ivq(rho * Delta(r) / k) - 2)
    log(f"   r = {r}: low-class sale rate t = {ivstr(tt)}; t/lambda = {ivstr(tt / lam)}")

# ------------------------------------------------------------------ I. each hypothesis is needed
log("\nI. Each hypothesis of Proposition 2 is needed (calibration B, prior 1/2)")
bl = b + lam
log("   b + lambda =", ivstr(bl), "; above 1/2:", ivsign(bl - ivq(Fr(1, 2))))
reg.add_iv("b_plus_lambda_B", bl, CA, "b + lambda; the Laplace sufficient ownership condition transfers when it exceeds 1/2")
# (a) drop B_0(pi) < c_H: c_H = 47/10, strengths (6/5, 3, 8)
cH_ex, r2_ex = Fr(47, 10), Fr(8)


def Bx(r, mu_iv):
    a = auction(r)
    return ivq(a["gL"]) + mu_iv * ivq(a["gH"] - a["gL"])


nec = {
    "k_minus_Delta0": ivq(k - Delta(r0)),
    "cH_minus_B1_pi": ivq(cH_ex) - Bx(r1, ivq(pi_half)),
    "B1_M_minus_cH": Bx(r1, M) - ivq(cH_ex),
    "kstrong_r1": ivq(rho) * m * ivq(Delta(r1)) - ivq(k),
    "kstrong_r2": ivq(rho) * m * ivq(Delta(r2_ex)) - ivq(k),
    "cH_minus_B2_M": ivq(cH_ex) - Bx(r2_ex, M),
    "cH_minus_B0_pi": ivq(cH_ex) - Bx(r0, ivq(pi_half)),
}
for key, val in nec.items():
    log(f"   c_H = 47/10, strengths (6/5, 3, 8): {key:16s} {ivstr(val)} sign {ivsign(val)}")
log("   B_0(1/2) =", B(r0, pi_half), "> 47/10: both cost types prepare at the weak incumbent; entry 1.")
reg.add_frac("nec_cH", cH_ex, IN, "example: c_H = 47/10")
reg.add_frac("nec_r2", r2_ex, IN, "example: third strength 8")
reg.add_dec_exact("nec_margin_kweak", k - Delta(r0), AN, "example: k - Delta_0")
reg.add_dec_exact("nec_margin_prior_r1", cH_ex - B(r1, pi_half), AN, "example: c_H - B_1(1/2) = 49/120")
reg.add_iv("nec_margin_recruit_B", nec["B1_M_minus_cH"], CA, "example: B_1(M) - c_H")
reg.add_iv("nec_margin_kstrong_B", nec["kstrong_r1"], CA, "example: rho kappa Delta_1 - k")
reg.add_iv("nec_margin_return_B", nec["cH_minus_B2_M"], CA, "example: c_H - B_2(M) at r = 8")
reg.add_dec_exact("nec_margin_weakcost", cH_ex - B(r0, pi_half), AN, "example: c_H - B_0(1/2) = -5/48 < 0")
reg.add_dec_exact("nec_entry_r0", Fr(1), AN, "example: entry at the weak incumbent is 1")
# (b) other single failures on the benchmark path
log("   Delta(31/20) =", Delta(Fr(31, 20)), "=", d9(Delta(Fr(31, 20))), "> k: (H2, left) fails at 31/20")
k2 = ivq(rho) * m * ivq(Delta(Fr(2))) - ivq(k)
log("   rho kappa Delta(2) - k =", ivstr(k2), "< 0: (H2, right) fails at r = 2")
reg.add_dec_exact("Delta_r155", Delta(Fr(31, 20)), AN, "Delta(31/20) = 121/1240")
reg.add_iv("margin_kstrong_r2pt0_B", k2, CA, "rho kappa Delta(2) - k < 0")

# ------------------------------------------------------------------ J. exact constants printed in the proofs
log("\nJ. Exact constants printed in the proofs")
from p1_common import peval, pmul, psub, pder, DELTA_NUM, ONE_MINUS_TAU_NUM, DELTA_DEN, TAU_DEN, lam_A, beta_A  # noqa: E402
J_num, J_den = pmul(DELTA_NUM, ONE_MINUS_TAU_NUM), pmul(DELTA_DEN, TAU_DEN)
QJ = psub(pmul(pder(J_num), J_den), pmul(J_num, pder(J_den)))
QJ_int = [2 * c for c in QJ]
consts = {
    "J_r0": (J(r0), "J(6/5)"),
    "rhoJ_r1": (rho * J(r1), "rho J(3)"),
    "rhoJ_r2": (rho * J(r2), "rho J(18/5)"),
    "QJ_r0": (peval(QJ_int, r0), "2 x numerator of J' at 6/5 (integer form)"),
    "B_r0_half": (B(r0, pi_half), "B_{6/5}(1/2)"),
    "Delta_r155_frac": (Delta(Fr(31, 20)), "Delta(31/20)"),
}
for key, (val, note) in consts.items():
    log(f"   {key}: {val} = {d9(val)} ({note})")
    reg.add_frac(key, val, AN, note)
# Lemma 1(c) example: lambda = 6/17, beta = 2/5, prior 1/2
lx, bx = Fr(6, 17), Fr(2, 5)
bbx, b0x = (1 - lx) * bx, (1 - lx) * (1 - 2 * bx)
mu0x = (b0x + lx) / (2 * b0x + lx)
Mx = (bbx + lx) / (2 * bbx + lx)
log("   Lemma 1(c) example (lambda 6/17, beta 2/5): mu(0) =", mu0x, "> M =", Mx)
reg.add_frac("ex_beta_mu0", mu0x, AN, "Lemma 1(c): zero-order posterior with class H abstaining, class L never abstaining")
reg.add_frac("ex_beta_M", Mx, AN, "Lemma 1(c): M at lambda 6/17, beta 2/5")
# longer displays of entry at r1
E1_lo, E1_hi = ivends(E1)
log("   entry at r1, seven places: ends round to", round_dec(E1_lo, 7), "and", round_dec(E1_hi, 7))
reg.add("entry_r1_B_7", value_str(E1), round_dec(E1_lo, 7), CA,
        f"entry at r1, seven decimals; outward enclosure {ivstr(E1)}")
beta_u = iv.mpf('0.294655575684807914696610854717407893')  # the earlier study's unrounded beta (36 digits)
E1_u = ivq(rho) + ivq(1 - rho) * (beta_u / (1 + u * beta_u) + (u * beta_u / (1 + u * beta_u)) / 2)
Eu_lo, Eu_hi = ivends(E1_u)
log("   entry at r1 with the earlier study's unrounded beta:", ivstr(E1_u), "; seven places:",
    round_dec(Eu_lo, 7), "and", round_dec(Eu_hi, 7))
reg.add("entry_r1_unroundedbeta_7", value_str(E1_u), round_dec(Eu_lo, 7), CA,
        "entry at r1 with beta = 0.294655575684807914696610854717407893 (earlier study);"
        f" outward enclosure {ivstr(E1_u)}")

# ------------------------------------------------------------------ K. calibration A comparison values (exact)
log("\nK. Calibration A values quoted for comparison (exact)")
bA = (1 - lam_A) * beta_A
MA = (lam_A + bA) / (lam_A + 2 * bA)
log("   calibration A: b =", bA, " M =", MA)
for r, nm in ((Fr(31, 20), "r155"), (Fr(8, 5), "r160"), (Fr(33, 20), "r165")):
    D, t = Delta(r), tau(r)
    ent = rho + (bA / 2) * (k - rho * J(r)) / (D * (1 - t) ** 2)
    log(f"   threshold branch entry at {r}, calibration A: {ent} = {d9(ent)}")
    reg.add_dec_exact(f"entry_th_{nm}_A", ent, AN, f"threshold branch entry at r = {r}, calibration A")
dA = k / (1 - MA)
rFA = frak_r(ivq(dA))
log("   r_F at calibration A = frak_r(k/(1 - 29/40)) = frak_r(4/55) =", ivstr(rFA))
reg.add_iv("rF_A", rFA, AN, "frak_r(k/(1 - 29/40)) = frak_r(4/55); calibration A")

# ------------------------------------------------------------------ H. compare with known values
log("\nH. Comparison with the values listed in the brief (BRIEF section 3)")
known = [("entry at r1", E1, "0.522757"), ("ownership at r1", own1, "0.3244"), ("r_C", rC, "3.592659"),
         ("return margin in posterior", mg["return_post"], "about 0.0003"), ("prior lo", p_lo, "0.467850"),
         ("prior hi", p_hi, "0.500424"), ("r_F", rF, "1.467127"), ("r_N", rN, "1.747878")]
for nm, v, kv in known:
    log(f"   {nm:28s} computed {ivstr(v, 9)}  brief {kv}")
log(f"   r_A computed {qbrstr(rA[0], rA[1], 9)}  brief 1.393958")
log("   r_F at calibration A: frak_r(k/(1 - 29/40)) = frak_r(4/55) =", ivstr(frak_r(ivq(Fr(4, 55)))),
    "(the brief marks 1.460985 as the calibration A value)")

# ------------------------------------------------------------------ L. derived strict inequalities
log("\nL. Derived strict inequalities used in the proofs (margins at the benchmark)")
derived = [
    ("margin_Delta_pos_B", Delta(r0), "min of Delta on [r0, r2] = Delta(r0) = 1/60 > 0 (Delta increasing for r > ell)"),
    ("margin_gHgL_B", h - r2 / 2 - ell * ell / (2 * r2),
     "min of g_H - g_L = h - r/2 - ell^2/(2r) on [r0, r2], at r2: 1451/180 > 0 (decreasing for r > ell)"),
    ("margin_J_r0_B", k - J(r0), "k - J(r0) = 1283/92400 > 0: r0 < r_A"),
    ("margin_rhoJ_r1_B", rho * J(r1) - k, "rho J(r1) - k = 7/240 > 0: r_J < r1"),
    ("margin_rhoJ_r2_B", rho * J(r2) - k, "rho J(r2) - k > 0: Lemma 4(b)"),
    ("margin_rhoJ_2_B", rho * J(Fr(2)) - k, "rho J(2) - k = 11/11200 > 0: r_J < 2, the range of Lemma 4(c)"),
    ("margin_tau_r2_3q_B", Fr(3, 4) - tau(r2), "3/4 - tau(r2) = 27/1451 > 0: M < 3/4 on the band"),
]
for key, val, note in derived:
    log(f"   {key:22s} {val} = {d9(val)}  ({note})")
    reg.add_dec_exact(key, val, AN, note)
    reg.add_frac(key + "_frac", val, AN, "exact form of " + key)
# tau(r_N) - 1/2 (r_N < r_J): tau increasing, so tau(r_N) >= tau(r0); interval value at r_N
rN_lo, rN_hi = ivends(rN)
tauN = (tau(rN_lo), tau(rN_hi))
log(f"   margin_tau_rN_half_B   tau(r_N) - 1/2 in {qbrstr(tauN[0] - pi_half, tauN[1] - pi_half)}: r_N < r_J")
reg.add_bracket("margin_tau_rN_half_B", tauN[0] - pi_half, tauN[1] - pi_half, CA,
                "tau(r_N) - 1/2 > 0: r_N < r_J (bracket from the r_N enclosure; tau increasing)")
tA_3q = (Fr(3, 4) - tA[1], Fr(3, 4) - tA[0])
log(f"   margin_tauA_3q_B       3/4 - tau_A in {qbrstr(*tA_3q)}: r_A < r_N(pi) at every prior (Prop. 5, Step 3)")
reg.add_bracket("margin_tauA_3q_B", tA_3q[0], tA_3q[1], CA, "3/4 - tau(r_A) = 1 - rho - tau_A > 0 (Prop. 5, Step 3)")
pm_tA = (tS[0] - tA[1], tS[1] - tA[0])
log(f"   margin_pimax_tauA_B    pi_max - tau_A in {qbrstr(*pm_tA)}: r_A < r_star")
reg.add_bracket("margin_pimax_tauA_B", pm_tA[0], pm_tA[1], CA, "pi_max - tau_A = tau(r_star) - tau(r_A) > 0: r_A < r_star")
uk = ivq(u_k) - u
log(f"   margin_u_kstrong_B     19/3 - u = {ivstr(uk)} (implied by the band)")
reg.add_iv("margin_u_kstrong_B", uk, CA, "19/3 - u: the right side of (H2) at r1 (implied by u < 2686/1559)")

# ------------------------------------------------------------------ N. the CM endpoint at pi = pi_max
log("\nN. The CM endpoint at r = r_star, pi = pi_max = tau(r_star) (calibration B)")
log("   Exact ties by definition: tau(r_star) = pi_max and rho Delta(r_star) pi_max = k.")
rs_iv = ivbr(rS_[0], rS_[1])
D_rs = ivbr(Delta(rS_[0]), Delta(rS_[1]))       # Delta increasing
pm_iv = ivbr(tS[0], tS[1])                         # tau increasing
Mpm = pm_iv * eiv / (pm_iv * eiv + 1 - pm_iv)      # M(pi) with 1 + u = e
b0B = b0
mu0 = pm_iv * b0B / (pm_iv * b0B + (1 - pm_iv) * (b0B + lam))
cm_ret = D_rs * (1 - Mpm) - ivq(k)
cm_J = D_rs * (1 - pm_iv) - ivq(k)
cm_entry = ivq(rho) + ivq(1 - rho) * (b + pm_iv * lam)
log("   r_star in", ivstr(rs_iv), "; pi_max in", ivstr(pm_iv))
log("   M(pi_max) =", ivstr(Mpm))
log("   zero-order posterior in the informative tuple (H buys fully, L abstains) =", ivstr(mu0),
    "; pi_max - mu0 =", ivstr(pm_iv - mu0), "sign", ivsign(pm_iv - mu0))
log("   J(r_star) - k = Delta(r_star)(1 - pi_max) - k =", ivstr(cm_J), "sign", ivsign(cm_J))
log("   full-purchase return Delta(r_star)(1 - M(pi_max)) - k =", ivstr(cm_ret), "sign", ivsign(cm_ret))
log("   entry in the informative tuple: rho + (1 - rho)(b + pi_max lambda) =", ivstr(cm_entry))
reg.add_iv("M_pimax_B", Mpm, CA, "M(pi_max) at calibration B")
reg.add_iv("mu0_pimax_B", mu0, CA, "zero-order posterior at the CM endpoint (H buys fully, L abstains)")
reg.add_iv("margin_cmend_B", cm_ret, CA,
           "Delta(r_star)(1 - M(pi_max)) - k > 0: strict full-purchase return at the CM endpoint (also under I0)")
reg.add_iv("entry_cmend_B", cm_entry, CA, "entry of the informative tuple at the CM endpoint r_star, pi = pi_max")

reg.write(REGISTRY)
log(f"\nRegistry: {len(reg.rows)} rows written to {REGISTRY}")
log("Rows whose 6-place display is not certified by both exact ends:",
    ", ".join(reg.uncertified) if reg.uncertified else "none")
log.close()
