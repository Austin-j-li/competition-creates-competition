#!/usr/bin/env python3
"""Independent exact check of N3, Extensions B and C (costly research in the order slot).

Written from the primitives. It does not import any other program of the team.
Exact rational arithmetic (fractions.Fraction) everywhere except the clearly marked
floating-point welfare diagnostics of the grid. The program prints results only.

Model (as stated by N3, Extension B):
  - The investor chooses a private success probability lam in [0, lam_bar] at cost (a/2) lam^2,
    before it learns the class.
  - Success: the investor learns the class j in {H, L} (prior 1/2) and fills the single slot
    with an order in {-1, 0, 1} at cost k|q|.
  - Failure: a liquidity trader fills the slot: sell, wait, buy with probabilities beta, 1-2beta, beta.
  - Competitive market makers see the order; the challenger sees the price and its cost.
  - The paper's second-price auction with reserve p; incumbent value R ~ U[0, r].

Structural facts used by the enumerator (derived in memo XN3_check.md, section 3):
  (F1) H's purchase payoff depends only on alpha = Pr(buy | H); L's sale payoff only on sigma.
  (F2) mu(-1) <= 1/2 < tau(r) and mu(0) <= 1/2: only the purchase can recruit.
  (F3) A mixing class earns zero, so lam > 0 needs a strict full purchase by H.
  The equilibrium types for lam > 0 are therefore:
      H buys fully; L abstains (L0), sells fully (L1) or mixes (Lint);
      entry after a purchase: e+ = 1 ("hi"), e+ = rho ("lo"), or a challenger mixture ("th", rule CM).
  Each type gives one research equation F(lam) = 0 with F strictly increasing on lam >= 0.
"""
from fractions import Fraction as Fr
import hashlib
import platform
import sys

# ----------------------------------------------------------------------------------------------
# Benchmark primitives
# ----------------------------------------------------------------------------------------------
H_VAL, L_VAL, P = Fr(10), Fr(1), Fr(1, 2)
RHO, C_H, K = Fr(1, 4), Fr(6), Fr(1, 50)
PI = Fr(1, 2)
BETA = Fr(1, 3)
LAM_BAR_N3, A_N3 = Fr(6, 17), Fr(1, 40)
STRENGTHS = [Fr(6, 5), Fr(31, 20), Fr(8, 5), Fr(33, 20), Fr(3), Fr(18, 5)]
MIDDLE = [Fr(31, 20), Fr(8, 5), Fr(33, 20)]


def dec(x, n=12):
    """Decimal display of a Fraction (display only)."""
    return f"{float(x):.{n}f}"


# ----------------------------------------------------------------------------------------------
# Auction objects by direct integration (midpoint rule on linear pieces is exact)
# ----------------------------------------------------------------------------------------------
def expect(r, f, kinks):
    pts = sorted({Fr(0), r} | {x for x in kinks if 0 < x < r})
    tot = Fr(0)
    for lo, hi in zip(pts[:-1], pts[1:]):
        tot += (hi - lo) * f((lo + hi) / 2)
    return tot / r


AUCTION_CACHE = {}


def auction(r):
    if r in AUCTION_CACHE:
        return AUCTION_CACHE[r]
    kinks = [P, L_VAL, H_VAL]
    t0 = expect(r, lambda u: P if u >= P else Fr(0), kinks)
    tH = expect(r, lambda u: min(H_VAL, max(P, u)), kinks)
    tL = expect(r, lambda u: min(L_VAL, max(P, u)), kinks)
    gH = expect(r, lambda u: max(Fr(0), H_VAL - max(P, u)), kinks)
    gL = expect(r, lambda u: max(Fr(0), L_VAL - max(P, u)), kinks)
    SH = expect(r, lambda u: max(H_VAL, u), kinks)
    SL = expect(r, lambda u: max(L_VAL, u), kinks)
    S0 = expect(r, lambda u: u if u >= P else Fr(0), kinks)
    out = dict(r=r, t0=t0, tH=tH, tL=tL, gH=gH, gL=gL, SH=SH, SL=SL, S0=S0,
               Delta=tH - tL, tau=(C_H - gL) / (gH - gL))
    AUCTION_CACHE[r] = out
    return out


def closed_forms(r):
    return dict(t0=P * (1 - P / r), tH=r / 2 + P * P / (2 * r), tL=L_VAL - (L_VAL ** 2 - P * P) / (2 * r),
                Delta=(r - L_VAL) ** 2 / (2 * r), tau=(48 * r - 3) / (4 * (20 * r - r * r - 1)))


# ----------------------------------------------------------------------------------------------
# Order-flow objects of the unit slot with a full high-class purchase
# ----------------------------------------------------------------------------------------------
def liq(lam):
    return (1 - lam) * BETA


def d_full(lam):
    """1 - mu(+1) when H buys for sure: b / (2b + lam)."""
    b = liq(lam)
    return b / (2 * b + lam)


def lam_of_d(delta):
    """Inverse of d_full on (0, 1/2]."""
    return BETA * (1 - 2 * delta) / (BETA + delta * (1 - 2 * BETA))


def F_res(lam, a, E, Kc, Dl):
    """Research equation: F = 0  <=>  (E*Dl*d(lam) - Kc)/2 = a*lam.  F rises strictly on lam >= 0."""
    D = 2 * BETA + lam * (1 - 2 * BETA)
    return 2 * a * lam * D + Kc * D - E * Dl * BETA * (1 - lam)


def bracket_root(a, E, Kc, Dl, width=Fr(1, 10 ** 18)):
    lo, hi = Fr(0), Fr(1)
    while hi - lo > width:
        m = (lo + hi) / 2
        if F_res(m, a, E, Kc, Dl) < 0:
            lo = m
        else:
            hi = m
    return lo, hi


def flow_laws(lam, alpha, sigma):
    """Class-conditional order laws {q: prob}. Wrong-signed informed orders are never used."""
    b = liq(lam)
    w = (1 - lam) * (1 - 2 * BETA)
    fH = {1: b + lam * alpha, 0: w + lam * (1 - alpha), -1: b}
    fL = {1: b, 0: w + lam * (1 - sigma), -1: b + lam * sigma}
    return fH, fL


def describe(r, lam, alpha, sigma, e_plus_override=None):
    """All posteriors, entries, payoffs of every order, research value and aggregate entry."""
    A = auction(r)
    Dl, tau = A["Delta"], A["tau"]
    fH, fL = flow_laws(lam, alpha, sigma)
    mu, e = {}, {}
    for q in (1, 0, -1):
        mu[q] = fH[q] / (fH[q] + fL[q])
        e[q] = Fr(1) if mu[q] >= tau else RHO
    if e_plus_override is not None:
        e[1] = e_plus_override
    payH = {1: e[1] * Dl * (1 - mu[1]) - K, 0: Fr(0), -1: -e[-1] * Dl * (1 - mu[-1]) - K}
    payL = {-1: e[-1] * Dl * mu[-1] - K, 0: Fr(0), 1: -e[1] * Dl * mu[1] - K}
    V = (max(payH.values()) + max(payL.values())) / 2
    prob = {q: (fH[q] + fL[q]) / 2 for q in (1, 0, -1)}
    E_agg = sum(prob[q] * e[q] for q in (1, 0, -1))
    eH = sum(fH[q] * e[q] for q in (1, 0, -1))
    return dict(mu=mu, e=e, payH=payH, payL=payL, V=V, E=E_agg, eH=eH, fH=fH, fL=fL, prob=prob)


# ----------------------------------------------------------------------------------------------
# Complete enumeration of equilibria of the research game at one strength
# ----------------------------------------------------------------------------------------------
def interval_contains_root(a, E, Kc, Dl, lo, lo_closed, hi, hi_closed):
    """Is the unique positive root of F in the interval?  Decided by exact signs of F (F increasing)."""
    if lo is not None:
        f = F_res(lo, a, E, Kc, Dl)
        if lo_closed and f > 0:
            return False
        if (not lo_closed) and f >= 0:
            return False
    if hi is not None:
        f = F_res(hi, a, E, Kc, Dl)
        if hi_closed and f < 0:
            return False
        if (not hi_closed) and f <= 0:
            return False
    return True


def in_interval(x, lo, lo_closed, hi, hi_closed):
    if lo is not None and (x < lo or (x == lo and not lo_closed)):
        return False
    if hi is not None and (x > hi or (x == hi and not hi_closed)):
        return False
    return True


def intersect(i1, i2):
    """Intervals as (lo, lo_closed, hi, hi_closed); None means unbounded. An empty interval is None."""
    if i1 is None or i2 is None:
        return None
    lo1, lc1, hi1, hc1 = i1
    lo2, lc2, hi2, hc2 = i2
    if lo1 is None or (lo2 is not None and lo2 > lo1):
        lo, lc = lo2, lc2
    elif lo2 is None or lo1 > lo2:
        lo, lc = lo1, lc1
    else:
        lo, lc = lo1, lc1 and lc2
    if hi1 is None or (hi2 is not None and hi2 < hi1):
        hi, hc = hi2, hc2
    elif hi2 is None or hi1 < hi2:
        hi, hc = hi1, hc1
    else:
        hi, hc = hi1, hc1 and hc2
    if lo is not None and hi is not None and (lo > hi or (lo == hi and not (lc and hc))):
        return None
    return (lo, lc, hi, hc)


def enumerate_eq(r, lam_bar, a, rule="C1", hidden=False):
    """Every equilibrium of the research game. rule: C1 (prepare at a tie) or CM (mixture allowed).
    hidden=True: the challenger does not see the price, so entry is rho after every order."""
    A = auction(r)
    Dl, tau = A["Delta"], A["tau"]
    eqs = []
    # Zero research: all posteriors 1/2 < tau; best order earns rho*Delta/2 - k.
    if RHO * Dl / 2 <= K:
        eqs.append(dict(kind="zero", lam=Fr(0), lam_br=None, sigma=Fr(0), alpha=Fr(0), e_plus=RHO,
                        piece="-", regime="-"))
    lam_bar_iv = (Fr(0), False, lam_bar, True)
    l_sells = RHO * Dl / 2 > K
    lamL = lam_of_d(K / (RHO * Dl)) if l_sells else None
    lamE = lam_of_d(1 - tau)
    pieces = []
    if l_sells:
        pieces.append(("L1", (Fr(0), False, lamL, True)))
        pieces.append(("Lint", (lamL, False, None, False)))
    else:
        pieces.append(("L0", (Fr(0), False, None, False)))
    if hidden:
        regimes = [("lo", RHO, (None, False, None, False))]
    else:
        regimes = [("hi", Fr(1), (lamE, rule == "C1", None, False)),
                   ("lo", RHO, (None, False, lamE, False))]
    for reg_name, e_plus, reg_iv in regimes:
        for pc_name, pc_iv in pieces:
            iv = intersect(intersect(reg_iv, pc_iv), lam_bar_iv)
            if iv is None:
                continue
            E = e_plus + (RHO if pc_name == "L1" else 0)
            Kc = K * (2 if pc_name == "L1" else 1)
            lo, lc, hi, hc = iv
            # interior research: root of F strictly below lam_bar
            if E * Dl > 2 * Kc:
                iv_int = intersect(iv, (None, False, lam_bar, False))
                if iv_int is not None and interval_contains_root(a, E, Kc, Dl, *iv_int):
                    br = bracket_root(a, E, Kc, Dl)
                    eqs.append(dict(kind="interior", lam=None, lam_br=br, e_plus=e_plus, piece=pc_name,
                                    regime=reg_name, E=E, Kc=Kc))
            # research at the ceiling
            if in_interval(lam_bar, *iv) and F_res(lam_bar, a, E, Kc, Dl) <= 0:
                eqs.append(dict(kind="ceiling", lam=lam_bar, lam_br=None, e_plus=e_plus, piece=pc_name,
                                regime=reg_name, E=E, Kc=Kc))
    # Challenger mixture at the recruitment threshold (rule CM only)
    if rule == "CM" and not hidden and Fr(0) < lamE <= lam_bar:
        if l_sells and lamE <= lamL:
            pc_name, gL = "L1", RHO * Dl * (1 - tau) - K
        else:
            pc_name, gL = ("Lint" if l_sells else "L0"), Fr(0)
        if lamE < lam_bar:
            e_star = (2 * a * lamE + K - gL) / (Dl * (1 - tau))
            if RHO < e_star < 1 and e_star * Dl * (1 - tau) - K > 0:
                eqs.append(dict(kind="threshold", lam=lamE, lam_br=None, e_plus=e_star, piece=pc_name,
                                regime="th"))
        else:
            e_min = max(RHO, (2 * a * lam_bar + K - gL) / (Dl * (1 - tau)))
            if e_min <= 1:
                eqs.append(dict(kind="threshold-interval", lam=lamE, lam_br=None, e_plus=e_min, piece=pc_name,
                                regime="th"))
    return eqs, dict(Delta=Dl, tau=tau, lamE=lamE, lamL=lamL, l_sells=l_sells)


def sigma_for(r, lam, piece):
    if piece == "L1":
        return Fr(1)
    if piece in ("L0", "-"):
        return Fr(0)
    A = auction(r)
    Dl = A["Delta"]
    b = liq(lam)
    # Lint: rho*Delta*b/(2b + lam*sigma) = k
    return (RHO * Dl * b / K - 2 * b) / lam


def eq_details(r, eq):
    """Return details at a rational lam, or at both ends of a root bracket (enclosure)."""
    lams = [eq["lam"]] if eq["lam"] is not None else list(eq["lam_br"])
    out = []
    for lam in lams:
        alpha = Fr(1) if lam > 0 else Fr(0)
        sigma = sigma_for(r, lam, eq["piece"]) if lam > 0 else Fr(0)
        override = eq["e_plus"] if eq["kind"].startswith("threshold") else None
        out.append((lam, alpha, sigma, describe(r, lam, alpha, sigma, override)))
    return out


def welfare(r, lam, alpha, sigma, det, a):
    """Proceeds, net surplus (after preparation costs), research cost, informed trading cost."""
    A = auction(r)
    fH, fL, e = det["fH"], det["fL"], det["e"]
    proceeds = Fr(0)
    surplus = Fr(0)
    for f, t, S in ((fH, A["tH"], A["SH"]), (fL, A["tL"], A["SL"])):
        for q in (1, 0, -1):
            prep_high = (e[q] - RHO) / (1 - RHO)
            proceeds += PI * f[q] * (A["t0"] + e[q] * (t - A["t0"]))
            surplus += PI * f[q] * (A["S0"] + e[q] * (S - A["S0"]) - (1 - RHO) * prep_high * C_H)
    research_cost = a * lam * lam / 2
    trade_cost = lam * K * (alpha + sigma) / 2
    return proceeds, surplus, research_cost, trade_cost


def eq_line(r, eq):
    dets = eq_details(r, eq)
    lam_txt = (f"lam = {eq['lam']} = {dec(eq['lam'])}" if eq["lam"] is not None
               else f"lam in [{dec(eq['lam_br'][0], 15)}, {dec(eq['lam_br'][1], 15)}]")
    lines = [f"    type={eq['kind']}, regime={eq['regime']}, low class={eq['piece']}, {lam_txt}"]
    for lam, alpha, sigma, det in dets:
        mu, e = det["mu"], det["e"]
        lines.append(
            "      at lam=%s: alpha=%s sigma=%s | mu(+1,0,-1)=(%s, %s, %s) | e(+1,0,-1)=(%s, %s, %s)" % (
                dec(lam), dec(alpha, 6), dec(sigma, 6), dec(mu[1]), dec(mu[0]), dec(mu[-1]),
                dec(e[1], 6), dec(e[0], 6), dec(e[-1], 6)))
        lines.append(
            "        payH(+1,0,-1)=(%s, 0, %s)  payL(-1,0,+1)=(%s, 0, %s)  V=%s  a*lam=%s  E=%s" % (
                dec(det["payH"][1]), dec(det["payH"][-1]), dec(det["payL"][-1]), dec(det["payL"][1]),
                dec(det["V"]), dec(A_CUR[0] * lam), dec(det["E"])))
    return lines, dets


A_CUR = [A_N3]


def report_strength(r, lam_bar, a, rule):
    A_CUR[0] = a
    eqs, info = enumerate_eq(r, lam_bar, a, rule)
    print(f"  r = {r} ({dec(r, 3)}), rule {rule}: Delta={info['Delta']}, tau={info['tau']} = {dec(info['tau'])}, "
          f"lam_E={info['lamE']} = {dec(info['lamE'])}, low class can sell: {info['l_sells']}")
    print(f"    number of equilibria: {len(eqs)}")
    for eq in eqs:
        lines, _ = eq_line(r, eq)
        for ln in lines:
            print(ln)
    return eqs


def main():
    src = open(__file__, "rb").read()
    print("XN3 check: Extension B and C of N3 (research in the order slot)")
    print("python", platform.python_version(), "| source sha256", hashlib.sha256(src).hexdigest()[:16])
    print(f"benchmark: h={H_VAL}, l={L_VAL}, p={P}, rho={RHO}, c_H={C_H}, k={K}, pi={PI}, beta={BETA}")
    print(f"N3 calibration: lam_bar={LAM_BAR_N3}, a={A_N3}")
    print()

    # ---------------- Section A: auction objects ----------------
    print("== A. Auction objects: direct integration against the closed forms ==")
    for r in STRENGTHS:
        A = auction(r)
        cf = closed_forms(r)
        diffs = [A[key] - cf[key] for key in ("t0", "tH", "tL", "Delta", "tau")]
        ident = (A["tH"] + A["gH"] - H_VAL, A["tL"] + A["gL"] - L_VAL)
        print(f"  r={r}: t0={A['t0']}, tH={A['tH']}, tL={A['tL']}, Delta={A['Delta']}, tau={A['tau']}; "
              f"differences from closed forms {diffs}; t+g-theta {ident}; "
              f"B(1/2)-c_H={PI * A['gH'] + (1 - PI) * A['gL'] - C_H}")
    print()

    # ---------------- Section B: the benchmark ----------------
    print("== B. Every equilibrium at the N3 benchmark (lam_bar=6/17, a=1/40) ==")
    bench = {}
    for rule in ("C1", "CM"):
        print(f" -- challenger rule {rule} --")
        for r in STRENGTHS:
            bench[(r, rule)] = report_strength(r, LAM_BAR_N3, A_N3, rule)
        print()

    # ---------------- Section C: middle strengths, the rising branch ----------------
    print("== C. Middle strengths: the positive branch, brackets, strict rise ==")
    ents = []
    for r in MIDDLE:
        eqs = [eq for eq in bench[(r, "C1")] if eq["kind"] != "zero"]
        for eq in eqs:
            lo, hi = eq["lam_br"]
            Elo, Ehi = Fr(1, 2) + lo / 8, Fr(1, 2) + hi / 8
            mlo, mhi = 1 - d_full(lo), 1 - d_full(hi)
            ents.append((r, Elo, Ehi))
            print(f"  r={r}: lam_R in [{dec(lo, 15)}, {dec(hi, 15)}]; mu(+1) in [{dec(mlo, 15)}, {dec(mhi, 15)}]; "
                  f"E in [{dec(Elo, 15)}, {dec(Ehi, 15)}]; 1/2+lam/8 check vs describe: "
                  f"{dec(eq_details(r, eq)[0][3]['E'] - Elo, 3)}")
            # N3's brackets of Table eq. (12)
    n3_br = {Fr(31, 20): (Fr(1, 4), Fr(251, 1000)), Fr(8, 5): (Fr(293, 1000), Fr(294, 1000)),
             Fr(33, 20): (Fr(332, 1000), Fr(333, 1000))}
    for r, (lo, hi) in n3_br.items():
        Dl = auction(r)["Delta"]
        print(f"  N3 bracket r={r}: F({lo})={F_res(lo, A_N3, 1, K, Dl)}, F({hi})={F_res(hi, A_N3, 1, K, Dl)}")
    strict = all(ents[i][2] < ents[i + 1][1] for i in range(len(ents) - 1))
    print(f"  strict rise of entry across 1.55, 1.60, 1.65 (upper end of one bracket below lower end of next): {strict}")
    # threshold branch under CM
    for r in MIDDLE:
        for eq in bench[(r, "CM")]:
            if eq["kind"] == "threshold":
                lamE = eq["lam"]
                Eagg = RHO + (eq["e_plus"] - RHO) * (liq(lamE) + lamE / 2)
                print(f"  CM threshold r={r}: lam_E={dec(lamE)}, e*={dec(eq['e_plus'], 6)}, aggregate entry={dec(Eagg, 6)}")
    print()

    # ---------------- Section D: price access at r = 3 ----------------
    print("== D. Price access at r=3 (lam_bar=6/17, a=1/40) ==")
    r = Fr(3)
    acc = [eq for eq in bench[(r, "C1")]]
    hid, _ = enumerate_eq(r, LAM_BAR_N3, A_N3, "C1", hidden=True)
    print(f"  equilibria with access: {len(acc)}; hidden: {len(hid)}")
    for name, eq_list, hidden in (("access", acc, False), ("hidden", hid, True)):
        for eq in eq_list:
            lam = eq["lam"]
            sig = sigma_for(r, lam, eq["piece"])
            det = describe(r, lam, Fr(1), sig)
            if hidden:
                det["e"] = {1: RHO, 0: RHO, -1: RHO}
            pr, su, rc, tc = welfare(r, lam, Fr(1), sig, det, A_N3)
            print(f"  {name}: lam={lam}, sigma={sig}, proceeds={pr}, net surplus={su}, research cost={rc}, "
                  f"trade cost={tc}")
            if name == "access":
                pa, sa, ra, ta = pr, su, rc, tc
            else:
                ph, sh, rh, th = pr, su, rc, tc
    print(f"  proceeds gain = {pa - ph} = {dec(pa - ph)}; net surplus gain = {sa - sh} = {dec(sa - sh)}; "
          f"research-cost difference = {ra - rh}; trade-cost difference = {ta - th}")
    # 3.6 resource cost of research
    r = Fr(18, 5)
    print(f"  r=3.6: research cost C(6/17) = {A_N3 * LAM_BAR_N3 ** 2 / 2}; plus trade cost "
          f"{A_N3 * LAM_BAR_N3 ** 2 / 2 + LAM_BAR_N3 * K}")
    print()

    # ---------------- Section E: Extension C (no ceiling) ----------------
    print("== E. Extension C: lam in [0, 1] ==")
    for a in (A_N3, Fr(1, 4)):
        for rule in ("C1", "CM"):
            print(f" -- a={a}, rule {rule} --")
            for r in (Fr(3), Fr(18, 5)):
                report_strength(r, Fr(1), a, rule)
    # thresholds a_3 and a_3.6
    print(" -- cost thresholds for a floor equilibrium (lo regime with both full trades) --")
    thr = {}
    for r in (Fr(3), Fr(18, 5)):
        A = auction(r)
        Dl, tau = A["Delta"], A["tau"]
        lamE = lam_of_d(1 - tau)
        v = RHO * Dl * (1 - tau) - K
        thr[r] = v / lamE
        hi_v = ((1 + RHO) * Dl * (1 - tau) - 2 * K) / 2
        print(f"  r={r}: v_*={v} = {dec(v)}, lam_E={lamE}; floor equilibrium exists iff a > {v / lamE} = "
              f"{dec(v / lamE)}; recruiting equilibrium (no ceiling) exists iff a < {hi_v / lamE} = {dec(hi_v / lamE)}")
    print(f"  a_3 < a_3.6: {thr[Fr(3)] < thr[Fr(18, 5)]}")
    lamE36 = lam_of_d(1 - auction(Fr(18, 5))["tau"])
    print(f"  N3 eq. (20): C'(lam_E)={A_N3 * lamE36}; v_* - C'(lam_E) = "
          f"{RHO * auction(Fr(18, 5))['Delta'] * (1 - auction(Fr(18, 5))['tau']) - K - A_N3 * lamE36}")
    print()

    # ---------------- Section F: cost ranges at the ceiling 6/17 ----------------
    print("== F. Cost ranges with lam_bar = 6/17 ==")
    lb = LAM_BAR_N3
    D155, D160, D165 = (auction(x)["Delta"] for x in MIDDLE)
    tau155 = auction(Fr(31, 20))["tau"]
    lamE155 = lam_of_d(1 - tau155)
    a_low_n3 = (D165 * d_full(lb) - K) / 2 / lb
    a_low_rise = (D160 * d_full(lb) - K) / 2 / lb
    a_up = (D155 * (1 - tau155) - K) / (2 * lamE155)
    print(f"  N3 lower end (capacity slack at 1.65): {a_low_n3} = {dec(a_low_n3)}")
    print(f"  weaker lower end (capacity slack at 1.60; then entry at 1.65 = 1/2 + lam_bar/8): {a_low_rise} = {dec(a_low_rise)}")
    print(f"  upper end (recruitment strict at 1.55): {a_up} = {dec(a_up)}")
    for x in MIDDLE:
        A = auction(x)
        le = lam_of_d(1 - A["tau"])
        print(f"    r={x}: recruitment needs a < {(A['Delta'] * (1 - A['tau']) - K) / (2 * le)}"
              f" = {dec((A['Delta'] * (1 - A['tau']) - K) / (2 * le))}; capacity slack needs a > "
              f"{dec((A['Delta'] * d_full(lb) - K) / 2 / lb)}")
    A3 = auction(Fr(3))
    cap3 = (((1 + RHO) * A3["Delta"] * d_full(lb) - 2 * K) / 2) / lb
    cap3h = (RHO * A3["Delta"] * d_full(lb) - K) / lb
    print(f"  r=3 with access: research at the ceiling iff a <= {cap3} = {dec(cap3)}")
    print(f"  r=3 hidden: research at the ceiling iff a <= {cap3h} = {dec(cap3h)}")
    print(f"  r=3: a floor equilibrium appears iff a > a_3 = {thr[Fr(3)]} = {dec(thr[Fr(3)])}")
    A36 = auction(Fr(18, 5))
    cap36 = (RHO * A36["Delta"] * d_full(lb) - K) / lb
    print(f"  r=3.6: research at the ceiling iff a <= {cap36} = {dec(cap36)}")
    print()

    # ---------------- Section G: sensitivity grid ----------------
    print("== G. Sensitivity grid over the ceiling lam_bar and the cost a (rule C1; CM extras counted) ==")
    print("  Columns: P1 = unique zero research at 1.2; P2 = unique equilibrium at 3 with entry > rho;")
    print("  P3 = unique equilibrium at 3.6 with entry rho and positive research; COEX = zero research and a")
    print("  positive pure-entry branch at all three middle strengths; RISE = that branch has strictly rising entry;")
    print("  ACC = proceeds and net surplus (after research and trade costs) rise with access at 3 (float diagnostic).")
    lam_bars = [Fr(3, 10), Fr(82, 259), Fr(8, 25), Fr(1, 3), Fr(6, 17), Fr(9, 25), Fr(2686, 7363), Fr(37, 100),
                Fr(2, 5), Fr(1, 2), Fr(1)]
    a_vals = [Fr(1, 200), Fr(1, 100), Fr(1, 64), Fr(1, 50), Fr(1, 40), Fr(1, 32), Fr(1, 25), Fr(1, 20),
              Fr(1, 12), Fr(1, 10), Fr(1, 8), Fr(1, 4), Fr(1, 2)]
    header = "  lam_bar      a        P1 P2 P3 COEX RISE ACC | E(3)     E(3.6)   middle entries        #eq(1.55..3.6)"
    print(header)
    all_ok = []
    for lb in lam_bars:
        for a in a_vals:
            A_CUR[0] = a
            res = {}
            for r in STRENGTHS:
                res[r] = enumerate_eq(r, lb, a, "C1")[0]
            p1 = len(res[Fr(6, 5)]) == 1 and res[Fr(6, 5)][0]["kind"] == "zero"

            def ent(r, eq):
                return eq_details(r, eq)[0][3]["E"]

            e3 = [ent(Fr(3), eq) for eq in res[Fr(3)]]
            e36 = [ent(Fr(18, 5), eq) for eq in res[Fr(18, 5)]]
            p2 = len(e3) == 1 and e3[0] > RHO
            p3 = (len(e36) == 1 and e36[0] == RHO and res[Fr(18, 5)][0]["kind"] != "zero")
            coex, mids = True, []
            for r in MIDDLE:
                kinds = [eq["kind"] for eq in res[r]]
                pos = [eq for eq in res[r] if eq["kind"] != "zero" and eq["regime"] == "hi"]
                if "zero" not in kinds or len(pos) != 1:
                    coex = False
                    mids.append(None)
                else:
                    dets = eq_details(r, pos[0])
                    mids.append((dets[0][3]["E"], dets[-1][3]["E"]))
            rise = coex and all(mids[i][1] < mids[i + 1][0] for i in range(2))
            acc = None
            if p2:
                eqa = res[Fr(3)][0]
                hid = enumerate_eq(Fr(3), lb, a, "C1", hidden=True)[0]
                if len(hid) == 1:
                    vals = []
                    for eq, hidden in ((eqa, False), (hid[0], True)):
                        lam = eq["lam"] if eq["lam"] is not None else sum(eq["lam_br"]) / 2
                        sig = sigma_for(Fr(3), lam, eq["piece"])
                        det = describe(Fr(3), lam, Fr(1), sig)
                        if hidden:
                            det["e"] = {1: RHO, 0: RHO, -1: RHO}
                        pr, su, rc, tc = welfare(Fr(3), lam, Fr(1), sig, det, a)
                        vals.append((float(pr), float(su - rc - tc)))
                    acc = vals[0][0] > vals[1][0] and vals[0][1] > vals[1][1]
            nums = ",".join(str(len(res[r])) for r in STRENGTHS[1:])
            mid_txt = " ".join(dec(m[0], 4) if m else "  -   " for m in mids)
            e3_txt = dec(e3[0], 4) if len(e3) == 1 else f"{len(e3)} eq"
            e36_txt = dec(e36[0], 4) if len(e36) == 1 else f"{len(e36)} eq"
            flag = lambda b: "Y " if b else ("- " if b is None else "n ")
            print(f"  {str(lb):12s} {str(a):8s} {flag(p1)} {flag(p2)} {flag(p3)} {flag(coex)}   {flag(rise)}   "
                  f"{flag(acc)}  | {e3_txt:8s} {e36_txt:8s} {mid_txt:22s} {nums}")
            if p1 and p2 and p3 and coex and rise:
                all_ok.append((lb, a))
    print()
    print("  Grid points where P1, P2, P3, COEX and RISE all hold:")
    for lb, a in all_ok:
        print(f"    lam_bar={lb} ({dec(lb, 4)}), a={a} ({dec(a, 4)})")
    print()
    print("  Endpoint strip for the ceiling (independent of a):")
    l3 = lam_of_d(1 - auction(Fr(3))["tau"])
    l36 = lam_of_d(1 - auction(Fr(18, 5))["tau"])
    print(f"    recruitment at 3 needs lam >= lam_E(3) = {l3} = {dec(l3)}")
    print(f"    floor at 3.6 for every research choice iff lam_bar < lam_E(3.6) = {l36} = {dec(l36)}")
    print()

    # ---------------- Section H: the region where every Extension B claim holds (rule C1) ----------------
    print("== H. Region of (lam_bar, a) for all Extension B claims (rule C1) ==")
    print("  P2 and P3 hold iff lam_E(3) <= lam_bar < lam_E(3.6) and a <= a_3 (section E).")
    print("  Coexistence at 1.55 needs a < a_up; strict rise needs lam_R(1.60) < lam_bar, i.e. a > a_lo(lam_bar).")
    D160 = auction(Fr(8, 5))["Delta"]
    for lb in (l3, Fr(1, 3), LAM_BAR_N3, Fr(9, 25), l36):
        a_lo = (D160 * d_full(lb) - K) / (2 * lb)
        print(f"    lam_bar={lb} ({dec(lb, 6)}): a_lo={a_lo} = {dec(a_lo, 6)}; a_up={dec(a_up, 6)}; "
              f"ratio a_up/a_lo={dec(a_up / a_lo, 3)}")
    # CM check of uniqueness at 3 and 3.6 on the small cost grid at lam_bar = 6/17
    print("  rule CM, lam_bar=6/17: number of equilibria at (3, 3.6) for each cost")
    for a in a_vals:
        A_CUR[0] = a
        n3 = len(enumerate_eq(Fr(3), LAM_BAR_N3, a, "CM")[0])
        n36 = len(enumerate_eq(Fr(18, 5), LAM_BAR_N3, a, "CM")[0])
        print(f"    a={a}: {n3}, {n36}")


if __name__ == "__main__":
    main()
