"""Price-contingent reserve: high-precision print-only computation.

Two independent routes to the seller optimum:
  route G: dense grid over the reserve;
  route C: finite candidate list from the regime derivatives.
The script prints both. It holds no checks that halt execution.
"""
from fractions import Fraction as Fr
from mpmath import mp, mpf, exp

mp.dps = 50

H = mpf(10); ELL = mpf(1); RHO = mpf("0.25"); K = mpf("0.02"); BPAR = mpf(2)
CH = mpf(5)
A = exp(-1 / BPAR)
M1 = 1 / (1 + A)          # good-news posterior under full buying
m1 = A / (1 + A)          # bad-news posterior under full buying
print("a =", A)
print("m1 =", m1, " M1 =", M1, " m1+M1 =", m1 + M1, " m1*M1 =", m1 * M1)


def auction(p, r):
    """Return t0,tH,tL,gH,gL,Delta for reserve p, incumbent U[0,r]."""
    p = mpf(p); r = mpf(r)
    if p > H:
        return (mpf(0),) * 6
    if p <= ELL:
        t0 = p * (1 - p / r)
        tH = r / 2 + p ** 2 / (2 * r)
        tL = ELL - (ELL ** 2 - p ** 2) / (2 * r)
        gH = H - r / 2 - p ** 2 / (2 * r)
        gL = (ELL ** 2 - p ** 2) / (2 * r)
    elif p <= r:
        t0 = p * (1 - p / r)
        tH = r / 2 + p ** 2 / (2 * r)
        tL = t0
        gH = H - tH
        gL = mpf(0)
    else:
        t0 = mpf(0); tH = p; tL = mpf(0); gH = H - p; gL = mpf(0)
    return t0, tH, tL, gH, gL, tH - tL


def Bgain(p, mu, r):
    _, _, _, gH, gL, _ = auction(p, r)
    return gL + mu * (gH - gL)


def entry(p, mu, r, cH=CH):
    b = Bgain(p, mu, r)
    e = RHO if b >= 0 else mpf(0)
    if b >= cH:
        e = e + (1 - RHO)
    return e


def S_of(p, mu, r, e=None):
    t0, tH, tL, _, _, _ = auction(p, r)
    if e is None:
        e = entry(p, mu, r)
    return t0 + e * (tL - t0 + mu * (tH - tL))


def p_bar(mu, r, cH=CH):
    """Largest reserve with B >= cH, by bisection. None if B(0) < cH."""
    if Bgain(mpf(0), mu, r) < cH:
        return None
    lo, hi = mpf(0), H
    for _ in range(200):
        mid = (lo + hi) / 2
        if Bgain(mid, mu, r) >= cH:
            lo = mid
        else:
            hi = mid
    return lo


def seller_grid(mu, r, step="0.005"):
    step = mpf(step); best_p = mpf(0); best_v = S_of(mpf(0), mu, r)
    p = step
    while p <= H:
        v = S_of(p, mu, r)
        if v > best_v:
            best_v, best_p = v, p
        p += step
    return best_p, best_v


def seller_candidates(mu, r):
    """Finite candidate list. Returns list of (value, p, label, attained)."""
    r = mpf(r); mu = mpf(mu)
    cand = []
    pb = p_bar(mu, r)
    # boundary points with their own entry value
    for p, lab in [(mpf(0), "0"), (ELL, "ell"), (r, "r"), (H, "h")]:
        cand.append((S_of(p, mu, r), p, lab, True))
    if pb is not None:
        cand.append((S_of(pb, mu, r), pb, "pbar(e=1)", True))
        cand.append((S_of(pb, mu, r, e=RHO), pb, "pbar+(e=rho,limit)", False))
    # regime I, e=rho interior: p = r(1-rho)/(2-3rho)
    pI = r * (1 - RHO) / (2 - 3 * RHO)
    if 0 < pI <= ELL:
        cand.append((S_of(pI, mu, r, e=RHO), pI, "I-rho", Bgain(pI, mu, r) < CH))
        cand.append((S_of(pI, mu, r), pI, "I-rho-actual", True))
    # regime II interior for e in {rho,1}: p = r(1-e*mu)/(2-3e*mu)
    for e, lab in [(RHO, "II-rho"), (mpf(1), "II-1")]:
        den = 2 - 3 * e * mu
        if den > 0:
            pII = r * (1 - e * mu) / den
            if ELL < pII <= r:
                att = (Bgain(pII, mu, r) >= CH) if e == 1 else (Bgain(pII, mu, r) < CH)
                cand.append((S_of(pII, mu, r, e=e), pII, lab, att))
                cand.append((S_of(pII, mu, r), pII, lab + "-actual", True))
    # just above ell (regime II limit at ell)
    t0, tH, tL, _, _, _ = auction(ELL, r)
    # regime II values at ell: tL=t0
    for e, lab in [(RHO, "ell+-rho"), (mpf(1), "ell+-1")]:
        v = t0 + e * mu * (tH - t0)
        cand.append((v, ELL, lab, False))
    cand.sort(key=lambda t: t[0], reverse=True)
    return cand, pb


print("\n=== Exact rational auction objects at p=1/2 (fractions) ===")
for rF in [Fr(6, 5), Fr(3), Fr(18, 5)]:
    pF, lF, hF = Fr(1, 2), Fr(1), Fr(10)
    t0 = pF * (1 - pF / rF); tH = rF / 2 + pF * pF / (2 * rF)
    tL = lF - (lF * lF - pF * pF) / (2 * rF)
    gH = hF - rF / 2 - pF * pF / (2 * rF); gL = (lF * lF - pF * pF) / (2 * rF)
    print(f"r={float(rF)}: t0={t0} tH={tH} tL={tL} gH={gH} gL={gL} DT={tH-tL}")

print("\n=== Seller best response: grid (G) vs candidates (C) ===")
for r in [mpf("1.2"), mpf(3), mpf("3.6"), mpf(5), mpf(7), mpf(9)]:
    for mu, lab in [(m1, "m1"), (mpf("0.5"), "1/2"), (M1, "M1")]:
        pg, vg = seller_grid(mu, r)
        cand, pb = seller_candidates(mu, r)
        feas = [c for c in cand if c[3]]
        vc, pc, lc, att = feas[0] if feas else cand[0]
        e_star = entry(pg, mu, r)
        _, _, _, _, _, Dg = auction(pg, r)
        print(f"r={r} mu={lab}({mp.nstr(mu,6)}): G p*={mp.nstr(pg,6)} V={mp.nstr(vg,8)} e*={e_star} D*={mp.nstr(Dg,6)}"
              f" | C best={lc} p={mp.nstr(pc,6)} V={mp.nstr(vc,8)} att={att} | pbar={mp.nstr(pb,6) if pb is not None else 'none'}"
              f" | B(0.5)={mp.nstr(Bgain(mpf('0.5'),mu,r),8)} S(0.5)={mp.nstr(S_of(mpf('0.5'),mu,r),8)} rho*mu*h={mp.nstr(RHO*mu*H,8)}")

print("\n=== Candidate detail at r=3 (top 5 per mu) ===")
for mu, lab in [(m1, "m1"), (mpf("0.5"), "1/2"), (M1, "M1")]:
    cand, pb = seller_candidates(mu, mpf(3))
    print(f"mu={lab} pbar={mp.nstr(pb,8) if pb is not None else 'none'}")
    for v, p, l, att in cand[:5]:
        print(f"   {l}: p={mp.nstr(p,8)} V={mp.nstr(v,10)} attained={att} B={mp.nstr(Bgain(p,mu,mpf(3)),8)}")


def mu_pair(beta):
    """Posteriors (bad, good) when H buys with prob beta, L never buys."""
    RG = (1 - beta) + beta / A
    RB = (1 - beta) + beta * A
    return RB / (1 + RB), RG / (1 + RG)


def K_contingent(beta, r):
    muB, muG = mu_pair(beta)
    out = mpf(0); detail = []
    for mu, prob_buy_reach in [(muG, M1), (muB, m1)]:
        pstar, _ = seller_grid(mu, r, step="0.01")
        e = entry(pstar, mu, r)
        _, _, _, _, _, D = auction(pstar, r)
        out += prob_buy_reach * e * D * (1 - mu)
        detail.append((mu, pstar, e, D))
    return out, detail


print("\n=== Investor gross buy profit K(beta), contingent reserve ===")
for r in [mpf("1.2"), mpf(3), mpf("3.6"), mpf(7), mpf(9)]:
    for beta in [mpf(0), mpf("0.25"), mpf("0.5"), mpf("0.75"), mpf(1)]:
        kv, det = K_contingent(beta, r)
        print(f"r={r} beta={beta}: K={mp.nstr(kv,8)} net={mp.nstr(kv-K,8)} "
              f"G(mu={mp.nstr(det[0][0],5)},p={mp.nstr(det[0][1],4)},e={det[0][2]},D={mp.nstr(det[0][3],5)}) "
              f"B(mu={mp.nstr(det[1][0],5)},p={mp.nstr(det[1][1],4)},e={det[1][2]},D={mp.nstr(det[1][3],5)})")

print("\n=== Outcomes: contingent vs committed p=0.5, full buying ===")
for r in [mpf("1.2"), mpf(3), mpf("3.6"), mpf(5), mpf(7), mpf(9)]:
    # contingent
    vals = {}
    for lab, mu in [("G", M1), ("B", m1)]:
        pstar, v = seller_grid(mu, r, step="0.005")
        vals[lab] = (pstar, v, entry(pstar, mu, r))
    # unconditional: P(good)=1/2 exactly under full buying
    proc_c = (vals["G"][1] + vals["B"][1]) / 2
    # entry: E[e(mu)] with P(good)=1/2
    ent_c = (vals["G"][2] + vals["B"][2]) / 2
    # state entry: e_H = M1*eG + m1*eB (P(good|H)=M1); e_L = m1*eG + M1*eB
    eH_c = M1 * vals["G"][2] + m1 * vals["B"][2]
    own_c = eH_c / 2  # Pr(H, entry); H challenger wins whenever prepared (h>r, admissible if p<=h)
    # committed 0.5
    p0 = mpf("0.5")
    eG0, eB0 = entry(p0, M1, r), entry(p0, m1, r)
    proc_0 = (S_of(p0, M1, r) + S_of(p0, m1, r)) / 2
    ent_0 = (eG0 + eB0) / 2
    own_0 = (M1 * eG0 + m1 * eB0) / 2
    print(f"r={r}: contingent pG={mp.nstr(vals['G'][0],5)} pB={mp.nstr(vals['B'][0],5)} proc={mp.nstr(proc_c,8)} entry={mp.nstr(ent_c,6)} OH={mp.nstr(own_c,8)}"
          f" || p=0.5 proc={mp.nstr(proc_0,8)} entry={mp.nstr(ent_0,6)} OH={mp.nstr(own_0,8)} eG={eG0} eB={eB0}")

print("\n=== No-trade candidate (mu=1/2): deviation profit e*D*/2 ===")
for r in [mpf("1.2"), mpf(3), mpf("3.6"), mpf(7), mpf(9)]:
    pstar, v = seller_grid(mpf("0.5"), r, step="0.005")
    e = entry(pstar, mpf("0.5"), r)
    _, _, _, _, _, D = auction(pstar, r)
    print(f"r={r}: p*(1/2)={mp.nstr(pstar,5)} e*={e} D*={mp.nstr(D,6)} dev gross={mp.nstr(e*D/2,8)} k={K} V={mp.nstr(v,8)}")

print("\n=== Committed reserve scan (full-buying selection when K1>k) ===")
def K_fixed(beta, r, p):
    muB, muG = mu_pair(beta)
    _, _, _, _, _, D = auction(p, r)
    return M1 * entry(p, muG, r) * D * (1 - muG) + m1 * entry(p, muB, r) * D * (1 - muB)

for r in [mpf("1.2"), mpf(3), mpf(9)]:
    best = None
    rows = []
    plist = [mpf(i) / 4 for i in range(0, 41)] + [mpf("0.5")]
    for p in plist:
        k1 = K_fixed(mpf(1), r, p); k0 = K_fixed(mpf(0), r, p)
        if k1 > K:
            eG, eB = entry(p, M1, r), entry(p, m1, r)
            proc = (S_of(p, M1, r) + S_of(p, m1, r)) / 2
            ent = (eG + eB) / 2; mode = "fullbuy"
        elif k0 <= K:
            e = entry(p, mpf("0.5"), r)
            proc = S_of(p, mpf("0.5"), r); ent = e; mode = "notrade"
        else:
            proc, ent, mode = mpf(0), mpf(0), "mixed?"
        rows.append((proc, p, mode, ent, k0, k1))
        if best is None or proc > best[0]:
            best = (proc, p, mode, ent, k0, k1)
    rows.sort(key=lambda t: t[0], reverse=True)
    print(f"r={r} best committed: proc={mp.nstr(best[0],8)} p={best[1]} mode={best[2]} entry={mp.nstr(best[3],6)} K0={mp.nstr(best[4],6)} K1={mp.nstr(best[5],6)}")
    for row in rows[:4]:
        print(f"    proc={mp.nstr(row[0],8)} p={row[1]} mode={row[2]} entry={mp.nstr(row[3],6)}")

print("\n=== Equilibrium outcomes (selection: full buying if K1>k, else no trade if K0<=k) ===")
def sale_probs(p, mu, r, e):
    """Sale and two-bidder probabilities conditional on mu, reserve p, entry rate e."""
    pr_ge = mpf(0) if p > r else (1 - p / r)
    # conditional on entry: type H always admissible (p<=h); type L admissible iff p<=ell
    sale_given_entry = mu * 1 + (1 - mu) * (1 if p <= ELL else pr_ge)
    two_given_entry = mu * pr_ge + (1 - mu) * (pr_ge if p <= ELL else mpf(0))
    sale = e * sale_given_entry + (1 - e) * pr_ge
    two = e * two_given_entry
    return sale, two

for r in [mpf("1.2"), mpf(3), mpf("3.6"), mpf(5), mpf(7), mpf(9)]:
    # contingent equilibrium mode from K values on coarse beta grid (detail above)
    k0c, _ = K_contingent(mpf(0), r); k1c, _ = K_contingent(mpf(1), r)
    if k1c > K:
        mode_c = "fullbuy"
        tot_p = tot_e = tot_s = tot_t = mpf(0); eH = mpf(0)
        for mu, ps in [(M1, mpf("0.5")), (m1, mpf("0.5"))]:
            pstar, v = seller_grid(mu, r, step="0.005")
            e = entry(pstar, mu, r); s_, t_ = sale_probs(pstar, mu, r, e)
            tot_p += ps * v; tot_e += ps * e; tot_s += ps * s_; tot_t += ps * t_
        pG, _ = seller_grid(M1, r, step="0.005"); pB, _ = seller_grid(m1, r, step="0.005")
        eH = M1 * entry(pG, M1, r) + m1 * entry(pB, m1, r)
        own = eH / 2
    else:
        mode_c = "notrade"; tot_p = tot_e = tot_s = tot_t = own = mpf(0)
    # committed p=0.5 equilibrium
    p0 = mpf("0.5"); k1f = K_fixed(mpf(1), r, p0); k0f = K_fixed(mpf(0), r, p0)
    if k1f > K:
        mode_f = "fullbuy"
        eG, eB = entry(p0, M1, r), entry(p0, m1, r)
        proc_f = (S_of(p0, M1, r) + S_of(p0, m1, r)) / 2; ent_f = (eG + eB) / 2
        own_f = (M1 * eG + m1 * eB) / 2
        sG, tG = sale_probs(p0, M1, r, eG); sB, tB = sale_probs(p0, m1, r, eB)
        sale_f, two_f = (sG + sB) / 2, (tG + tB) / 2
    elif k0f <= K:
        mode_f = "notrade"; e = entry(p0, mpf("0.5"), r)
        proc_f = S_of(p0, mpf("0.5"), r); ent_f = e; own_f = e / 2
        sale_f, two_f = sale_probs(p0, mpf("0.5"), r, e)
    else:
        mode_f = "mixed"; proc_f = ent_f = own_f = sale_f = two_f = mpf(0)
    print(f"r={r}: CONT mode={mode_c} K0={mp.nstr(k0c,6)} K1={mp.nstr(k1c,6)} proc={mp.nstr(tot_p,8)} entry={mp.nstr(tot_e,6)} OH={mp.nstr(own,8)} sale={mp.nstr(tot_s,6)} two={mp.nstr(tot_t,6)}"
          f" || FIXED0.5 mode={mode_f} K0={mp.nstr(k0f,6)} K1={mp.nstr(k1f,6)} proc={mp.nstr(proc_f,8)} entry={mp.nstr(ent_f,6)} OH={mp.nstr(own_f,8)} sale={mp.nstr(sale_f,6)} two={mp.nstr(two_f,6)}")

print("\n=== p*(mu)=h on mu in [m1,M1]? mu grid step 0.01; and min K(beta), beta step 0.02 ===")
for r in [mpf("1.2"), mpf(3)]:
    allh = True; worst = None
    i = 0
    while i <= 24:
        mu = m1 + (M1 - m1) * mpf(i) / 24
        pstar, v = seller_grid(mu, r, step="0.01")
        if pstar != H:
            allh = False; worst = (mu, pstar, v)
        i += 1
    print(f"r={r}: p*=h at all 25 mu points: {allh} counterexample={worst}")
    mink = None; argb = None; j = 0
    while j <= 50:
        beta = mpf(j) / 50
        kv, _ = K_contingent(beta, r)
        if mink is None or kv < mink:
            mink, argb = kv, beta
        j += 1
    print(f"r={r}: min K(beta) on grid = {mp.nstr(mink,8)} at beta={argb}; k={K}")

print("\n=== Sensitivity: cH=6 seller best at r=3 ===")
CH_BAK = CH
for mu, lab in [(m1, "m1"), (M1, "M1")]:
    # recompute with cH=6 through explicit entry override on grid
    bestp, bestv = mpf(0), mpf(-1); p = mpf(0)
    while p <= H:
        b = Bgain(p, mu, mpf(3)); e = RHO + (1 - RHO if b >= 6 else mpf(0))
        v = S_of(p, mu, mpf(3), e=e)
        if v > bestv:
            bestv, bestp = v, p
        p += mpf("0.005")
    print(f"cH=6 mu={lab}: p*={mp.nstr(bestp,5)} V={mp.nstr(bestv,8)} B(0)={mp.nstr(Bgain(mpf(0),mu,mpf(3)),8)}")

print("\n=== After-preparation timing, entry observable (r=3) ===")
r = mpf(3)
for mu, lab in [(m1, "m1"), (mpf("0.5"), "1/2"), (M1, "M1")]:
    # given entry, seller maximizes mu*tH+(1-mu)*tL over grid
    bestp, bestv = mpf(0), mpf(-1)
    p = mpf(0)
    while p <= H:
        _, tH, tL, _, _, _ = auction(p, r)
        v = mu * tH + (1 - mu) * tL
        if v > bestv:
            bestv, bestp = v, p
        p += mpf("0.005")
    print(f"mu={lab}: p_given_entry={mp.nstr(bestp,5)} proceeds={mp.nstr(bestv,8)} B_at_that_p={mp.nstr(Bgain(bestp,mu,r),8)} "
          f"|| no-entry best t0: p=r/2={mp.nstr(r/2,4)} t0={mp.nstr(auction(r/2,r)[0],8)} (r/4={mp.nstr(r/4,6)})")
