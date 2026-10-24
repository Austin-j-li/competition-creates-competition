"""Independent print-only check for memo C10_other.

Base: discrete Laplace noise, buy-only orders, c_L = 0.
Arithmetic: mpmath at 50 digits; exact rationals where marked.
This script prints numbers. It makes no test claims.
"""
from fractions import Fraction as Fr

import mpmath as mp

mp.mp.dps = 50

H = mp.mpf(10)
ELL = mp.mpf(1)
P = mp.mpf("0.5")
RHO = mp.mpf("0.25")
K = mp.mpf("0.02")
CH = mp.mpf(5)
PI = mp.mpf("0.5")
B = mp.mpf(2)
A = mp.exp(-1 / B)


def auction(r, cH=CH, a=A):
    d = {}
    d["r"] = r
    d["a"] = a
    d["cH"] = cH
    d["t0"] = P * (1 - P / r)
    d["tH"] = r / 2 + P * P / (2 * r)
    d["tL"] = ELL - (ELL * ELL - P * P) / (2 * r)
    d["gH"] = H - r / 2 - P * P / (2 * r)
    d["gL"] = (ELL * ELL - P * P) / (2 * r)
    d["Delta"] = d["tH"] - d["tL"]
    d["Delta_formula"] = (r - ELL) ** 2 / (2 * r)
    d["w"] = d["tL"] - d["t0"]
    d["tau"] = (cH - d["gL"]) / (d["gH"] - d["gL"])
    d["T"] = d["tau"] / (1 - d["tau"])
    d["phi1"] = a * d["T"] / (1 + a * d["T"])
    d["phi3"] = d["T"] / (a + d["T"])
    return d


def Bgain(d, mu, s=mp.mpf(0)):
    base = d["gL"] + mu * (d["gH"] - d["gL"])
    return base + s * (d["w"] + d["Delta"] * mu)


def e_of(d, mu):
    return mp.mpf(1) if mu >= d["tau"] else RHO


def mu_gb(d, phi):
    a = d["a"]
    if phi == 0:
        return mp.mpf(0), mp.mpf(0)
    if phi == 1:
        return mp.mpf(1), mp.mpf(1)
    om = phi / (1 - phi)
    return (om / a) / (1 + om / a), (om * a) / (1 + om * a)


def G1_closed(d, phi, eg, eb):
    a = d["a"]
    return (
        d["Delta"]
        * a
        * (1 - phi)
        / (1 + a)
        * (eg / (a + (1 - a) * phi) + eb / (1 - (1 - a) * phi))
    )


def profile_fb(d, phi):
    mg, mb = mu_gb(d, phi)
    return e_of(d, mg), e_of(d, mb), mg, mb


def G0(d, phi):
    return e_of(d, phi) * d["Delta"] * (1 - phi)


def G1_at(d, phi):
    eg, eb, mg, mb = profile_fb(d, phi)
    return G1_closed(d, phi, eg, eb), eg, eb


def outcome_fb(d, phi, eg, eb):
    a = d["a"]
    pg = (phi + a * (1 - phi)) / (1 + a)
    pb = (a * phi + 1 - phi) / (1 + a)
    pgh = phi / (1 + a)
    pbh = a * phi / (1 + a)
    e_entry = eg * pg + eb * pb
    oh = eg * pgh + eb * pbh
    phi_val = d["w"] * e_entry + d["Delta"] * oh
    return e_entry, oh, phi_val


def outcome_nt(d, phi):
    e = e_of(d, phi)
    return e, e * phi, e * (d["w"] + d["Delta"] * phi)


def phi_star(d):
    phi_nt = max(d["tau"], 1 - K / d["Delta"])
    g_at_3 = G1_closed(d, d["phi3"], mp.mpf(1), mp.mpf(1))
    phi_fb = d["phi3"] if g_at_3 > K else mp.inf
    star = min(phi_nt, phi_fb)
    return star, phi_nt, phi_fb, g_at_3


def cond_c(d):
    star, phi_nt, phi_fb, g_at_3 = phi_star(d)
    gamma = d["Delta"] + (1 - RHO) * d["w"] / star
    ell1 = RHO * d["w"] + gamma * d["phi1"]
    val = outcome_fb(d, d["phi1"], mp.mpf(1), RHO)[2]
    return {
        "star": star,
        "phi_nt": phi_nt,
        "phi_fb": phi_fb,
        "g_at_3": g_at_3,
        "gamma": gamma,
        "margin": ell1 - val,
        "ell_pi": RHO * d["w"] + gamma * PI,
    }


def f6(x):
    return mp.nstr(x, 8)


def direct_G1(d, phi, eg, eb, zmax=300):
    # Direct sum over Z for an H investor who buys one unit.
    a = d["a"]
    c = (1 - a) / (1 + a)
    mg, mb = mu_gb(d, phi)
    total = mp.mpf(0)
    for z in range(-zmax, zmax + 1):
        pz = c * a ** abs(z)
        if z >= 0:
            total += pz * eg * d["Delta"] * (1 - mg)
        else:
            total += pz * eb * d["Delta"] * (1 - mb)
    tail = 2 * a ** (zmax + 1) / (1 + a)
    return total, tail


def section_d1_d3():
    print("== A. Benchmark objects and D1 closed form ==")
    print("a =", mp.nstr(A, 20))
    for rs in ["1.2", "3", "3.6", "4.2"]:
        d = auction(mp.mpf(rs))
        star = cond_c(d)
        print(
            "r", rs, "Delta", f6(d["Delta"]), "DeltaFormulaDiff",
            mp.nstr(d["Delta"] - d["Delta_formula"], 3),
            "w", f6(d["w"]), "tau", f6(d["tau"]), "T", f6(d["T"]),
            "phi1", f6(d["phi1"]), "phi3", f6(d["phi3"]),
            "phiNT", f6(star["phi_nt"]), "phiFB", f6(star["phi_fb"]),
            "phi*", f6(star["star"]), "G1(phi3;1,1)-k",
            f6(star["g_at_3"] - K), "C margin", f6(star["margin"]),
        )
    d = auction(mp.mpf(3))
    for phis in ["0.2", "0.5", "0.65", "0.8"]:
        phi = mp.mpf(phis)
        eg, eb, mg, mb = profile_fb(d, phi)
        closed = G1_closed(d, phi, eg, eb)
        direct, tail = direct_G1(d, phi, eg, eb)
        print(
            "D1 phi", phis, "profile", f6(eg), f6(eb),
            "mu_g", f6(mg), "mu_b", f6(mb),
            "closed", mp.nstr(closed, 15),
            "direct", mp.nstr(direct, 15),
            "diff", mp.nstr(closed - direct, 3),
            "tailBound", mp.nstr(tail, 3),
            "boundRatio G1(1,1)/(Delta(1-phi))",
            f6(G1_closed(d, phi, mp.mpf(1), mp.mpf(1)) / (d["Delta"] * (1 - phi))),
        )
    print()
    print("== B. Condition C grid, phi star scan, main tables ==")
    margins = []
    for i in range(41):
        r = mp.mpf("1.2") + i * mp.mpf("0.2")
        cc = cond_c(auction(r))
        margins.append((cc["margin"], r, cc["star"]))
    margins.sort(key=lambda t: t[0])
    print("smallest C margins on r=1.2..9.2 step .2:")
    for mval, r, star in margins[:5]:
        print("  r", f6(r), "margin", mp.nstr(mval, 12), "phi*", f6(star))
    # fine scan for a fall in phi star
    prev = None
    falls = []
    min_margin = (mp.inf, None)
    r = mp.mpf("1.2")
    while r <= mp.mpf("9.8"):
        cc = cond_c(auction(r))
        if cc["margin"] < min_margin[0]:
            min_margin = (cc["margin"], r)
        if prev is not None and cc["star"] < prev[1] - mp.mpf("1e-12"):
            falls.append((prev[0], prev[1], r, cc["star"]))
        prev = (r, cc["star"])
        r += mp.mpf("0.01")
    print("fine scan step .01: falls in phi* count", len(falls))
    for item in falls[:10]:
        print("  fall", [f6(x) for x in item])
    print("fine scan smallest C margin", mp.nstr(min_margin[0], 12),
          "at r", f6(min_margin[1]))
    for rs in ["1.2", "1.4", "1.6", "1.8", "2", "3", "3.6", "4.2"]:
        d = auction(mp.mpf(rs))
        cc = cond_c(d)
        star = cc["star"]
        wpass = PI / star
        estar = RHO + (1 - RHO) * wpass
        phistar_val = d["w"] * estar + d["Delta"] * PI
        g0 = G0(d, PI)
        g1, eg, eb = G1_at(d, PI)
        nt = outcome_nt(d, PI)
        fb = outcome_fb(d, PI, eg, eb)
        print(
            "r", rs, "mode phiNT/phi3", f6(cc["phi_nt"]), f6(d["phi3"]),
            "phi*", f6(star), "pass", f6(wpass), "E*", f6(estar),
            "Phi*", f6(phistar_val), "ell(pi)", f6(cc["ell_pi"]),
            "base NT exists(G0<=k)", g0 <= K, "G0", f6(g0),
            "base FB exists(G1>k)", g1 > K, "G1", f6(g1),
            "base FB E OH Phi", f6(fb[0]), f6(fb[1]), f6(fb[2]),
            "base NT E OH Phi", f6(nt[0]), f6(nt[1]), f6(nt[2]),
        )


def gap_scan(r, n=2000):
    d = auction(r)
    star = cond_c(d)["star"]
    gaps = []
    both = []
    cur_gap = None
    cur_both = None
    for i in range(n + 1):
        phi = mp.mpf(i) / n
        nt_ok = G0(d, phi) <= K
        fb_ok = G1_at(d, phi)[0] > K
        if not nt_ok and not fb_ok:
            if cur_gap is None:
                cur_gap = [phi, phi]
            else:
                cur_gap[1] = phi
        elif cur_gap is not None:
            gaps.append(tuple(cur_gap))
            cur_gap = None
        if nt_ok and fb_ok:
            if cur_both is None:
                cur_both = [phi, phi]
            else:
                cur_both[1] = phi
        elif cur_both is not None:
            both.append(tuple(cur_both))
            cur_both = None
    if cur_gap is not None:
        gaps.append(tuple(cur_gap))
    if cur_both is not None:
        both.append(tuple(cur_both))
    print("r", f6(r), "phi*", f6(star),
          "gap grid ranges", [(f6(x), f6(y)) for x, y in gaps],
          "both grid ranges", [(f6(x), f6(y)) for x, y in both])


def branch_outcome_pref_fb(d, phi):
    g1, eg, eb = G1_at(d, phi)
    fb_ok = g1 > K
    nt_ok = G0(d, phi) <= K
    if fb_ok:
        out = outcome_fb(d, phi, eg, eb)
        return out, "FB", nt_ok
    if nt_ok:
        return outcome_nt(d, phi), "NT", nt_ok
    return None, "NONE", nt_ok


def section_d4_d6():
    print()
    print("== C. Pure-equilibrium gaps and coexistence (grid) ==")
    for rs in ["1.2", "1.4", "1.5", "1.6", "1.8", "3"]:
        gap_scan(mp.mpf(rs))
    print()
    print("== D. Symmetric signals (D4 and Table D) ==")
    d3 = auction(mp.mpf(3))
    print("r3 true a: d1=1-phi1", f6(1 - d3["phi1"]), "d2=phi3", f6(d3["phi3"]),
          "Pg(1/2)", f6((PI + A * (1 - PI)) / (1 + A)))
    for rs in ["1.2", "3", "3.6", "4.2"]:
        d = auction(mp.mpf(rs))
        row = []
        for ds in ["0.5", "0.55", "0.6", "0.65", "0.7", "0.75", "1"]:
            dv = mp.mpf(ds)
            outs = []
            labels = []
            for phi in [dv, 1 - dv]:
                out, lab, nt_ok = branch_outcome_pref_fb(d, phi)
                outs.append(out)
                labels.append(lab + ("+NT" if (lab == "FB" and nt_ok) else ""))
            if outs[0] is None or outs[1] is None:
                row.append(ds + ":NONE " + "/".join(labels))
            else:
                eavg = (outs[0][0] + outs[1][0]) / 2
                oavg = (outs[0][1] + outs[1][1]) / 2
                row.append(ds + ":E=" + f6(eavg) + " OH=" + f6(oavg)
                           + " " + "/".join(labels))
        print("r", rs, " | ".join(row))
    print()
    print("== E. D5 ceilings and value of disclosure; D6 numbers ==")
    m1 = 1 / (1 + A)
    print("M1 good posterior at pi=1/2", mp.nstr(m1, 15),
          "m1", mp.nstr(A / (1 + A), 15))

    def bisect(fun, lo, hi, iters=200):
        flo = fun(lo)
        for _ in range(iters):
            mid = (lo + hi) / 2
            if flo * fun(mid) <= 0:
                hi = mid
            else:
                lo = mid
                flo = fun(lo)
        return (lo + hi) / 2

    root_market = bisect(lambda r: Bgain(auction(r), m1) - CH,
                         mp.mpf(3), mp.mpf(5))
    root_disc = bisect(lambda r: H - r / 2 - P * P / (2 * r) - CH,
                       mp.mpf(9), mp.mpf("9.999"))
    print("market ceiling B_r(M1)=cH root", mp.nstr(root_market, 12))
    print("disclosure ceiling gH=cH root", mp.nstr(root_disc, 12),
          "closed form (10+sqrt(99))/2", mp.nstr((10 + mp.sqrt(99)) / 2, 12))
    for rs in ["1.2", "1.75", "3", "3.6", "4.0", "4.2"]:
        d = auction(mp.mpf(rs))
        cc = cond_c(d)
        star = cc["star"]
        estar = RHO + (1 - RHO) * PI / star
        phistar_val = d["w"] * estar + d["Delta"] * PI
        out, lab, nt_ok = branch_outcome_pref_fb(d, PI)
        base_phi = out[2] if out is not None else mp.nan
        print("value r", rs, "base label", lab, "Phi*", f6(phistar_val),
              "base Phi", f6(base_phi), "gain", f6(phistar_val - base_phi))
    for rs in ["3", "3.6", "4.2", "5", "7"]:
        d = auction(mp.mpf(rs))
        star = cond_c(d)["star"]
        kmax_star = G1_closed(d, star, mp.mpf(1), mp.mpf(1))
        g1, eg, eb = G1_at(d, PI)
        print("kmax r", rs, "at phi*", f6(kmax_star),
              "at 1/2 with its FB profile", f6(g1),
              "profile", f6(eg), f6(eb))
    d = auction(mp.mpf(3))
    print("r3 no-market pass pi/tau", f6(PI / d["tau"]),
          "entry", f6(RHO + (1 - RHO) * PI / d["tau"]),
          "Delta(1-tau)", f6(d["Delta"] * (1 - d["tau"])))
    # sensitivity rows
    for label, cH, bv, rho_v, pi_v in [
        ("cH=4", mp.mpf(4), B, RHO, PI),
        ("cH=6", mp.mpf(6), B, RHO, PI),
        ("cH=8", mp.mpf(8), B, RHO, PI),
        ("b=1.5", CH, mp.mpf("1.5"), RHO, PI),
        ("b=4", CH, mp.mpf(4), RHO, PI),
        ("b=10", CH, mp.mpf(10), RHO, PI),
        ("rho=0.1", CH, B, mp.mpf("0.1"), PI),
        ("rho=0.5", CH, B, mp.mpf("0.5"), PI),
        ("pi=0.3", CH, B, RHO, mp.mpf("0.3")),
    ]:
        av = mp.exp(-1 / bv)
        dv = auction(mp.mpf(3), cH=cH, a=av)
        star, phi_nt, phi_fb, g3 = phi_star(dv)
        wpass = pi_v / star
        ev = rho_v + (1 - rho_v) * wpass
        g1, eg, eb = G1_at(dv, pi_v)
        out, lab, _n = branch_outcome_pref_fb(dv, pi_v)
        print("sens", label, "phi*", f6(star), "pass", f6(wpass),
              "E*", f6(ev), "market label", lab,
              "market E", f6(out[0]) if out else "NONE")


def section_exact():
    print()
    print("== F. Exact rational check at a=3/5, r=3 (surrogate a) ==")
    a = Fr(3, 5)
    r = Fr(3)
    p = Fr(1, 2)
    rho = Fr(1, 4)
    cH = Fr(5)
    kk = Fr(1, 50)
    t0 = p * (1 - p / r)
    tH = r / 2 + p * p / (2 * r)
    tL = 1 - (1 - p * p) / (2 * r)
    gH = 10 - r / 2 - p * p / (2 * r)
    gL = (1 - p * p) / (2 * r)
    delta = tH - tL
    w = tL - t0
    tau = (cH - gL) / (gH - gL)
    big_t = tau / (1 - tau)
    phi1 = a * big_t / (1 + a * big_t)
    phi3 = big_t / (a + big_t)
    print("tau", tau, float(tau), "T", big_t, float(big_t))
    print("phi1", phi1, float(phi1), "phi3", phi3, float(phi3),
          "d1=1-phi1", 1 - phi1, float(1 - phi1), "d2", phi3, float(phi3))

    def g1(phi, eg, eb):
        return delta * a * (1 - phi) / (1 + a) * (
            eg / (a + (1 - a) * phi) + eb / (1 - (1 - a) * phi))

    def out_fb(phi, eg, eb):
        pg = (phi + a * (1 - phi)) / (1 + a)
        pb = (a * phi + 1 - phi) / (1 + a)
        e_entry = eg * pg + eb * pb
        oh = eg * phi / (1 + a) + eb * a * phi / (1 + a)
        return e_entry, oh, w * e_entry + delta * oh

    star = phi3
    gamma = delta + (1 - rho) * w / star
    ell1 = rho * w + gamma * phi1
    margin = ell1 - out_fb(phi1, Fr(1), rho)[2]
    print("G1(phi3;1,1)-k", g1(phi3, Fr(1), Fr(1)) - kk,
          float(g1(phi3, Fr(1), Fr(1)) - kk))
    print("C margin exact", margin, float(margin))
    print("phiNT exact", max(tau, 1 - kk / delta), float(max(tau, 1 - kk / delta)))
    # support line on a rational grid over pure outcomes
    worst = Fr(-10)
    worst_phi = None
    for i in range(1001):
        phi = Fr(i, 1000)
        ell = rho * w + gamma * phi
        # NT outcome if NT exists; FB outcome if FB exists
        e_nt = Fr(1) if phi >= tau else rho
        g0 = e_nt * delta * (1 - phi)
        vals = []
        if g0 <= kk:
            vals.append(e_nt * (w + delta * phi))
        if phi == 0:
            eg = eb = rho
        elif phi == 1:
            eg = eb = Fr(1)
        else:
            om = phi / (1 - phi)
            mg_ok = om / a >= big_t
            mb_ok = om * a >= big_t
            eg = Fr(1) if mg_ok else rho
            eb = Fr(1) if mb_ok else rho
        if g1(phi, eg, eb) > kk:
            vals.append(out_fb(phi, eg, eb)[2])
        for v in vals:
            if v - ell > worst:
                worst = v - ell
                worst_phi = phi
    print("largest Phi-ell on 1001 rational priors (pure values only)",
          worst, float(worst), "at phi", worst_phi)
    # D4 formulas in exact arithmetic
    oh_half = Fr(1, 2) * (1 + rho * a) / (1 + a)
    for dnum in [Fr(11, 20), Fr(3, 5), Fr(13, 20), Fr(7, 10), Fr(3, 4)]:
        # branch outcomes by profile alone (FB formulas)
        def branch(phi):
            if phi < phi1:
                eg = eb = rho
            elif phi < phi3:
                eg, eb = Fr(1), rho
            else:
                eg = eb = Fr(1)
            return out_fb(phi, eg, eb)
        hi = branch(dnum)
        lo = branch(1 - dnum)
        eavg = (hi[0] + lo[0]) / 2
        oavg = (hi[1] + lo[1]) / 2
        print("D4 exact d", dnum, float(dnum), "E", eavg, float(eavg),
              "OH", oavg, float(oavg), "OH-OH(1/2)", oavg - oh_half,
              float(oavg - oh_half))


def section_toehold_public():
    print()
    print("== G. Public toehold with bids held truthful (T1) ==")
    m1 = 1 / (1 + A)
    low_m = A / (1 + A)
    d0 = auction(mp.mpf("1.2"))
    d1 = auction(mp.mpf(3))

    def bisect_dec(fun, lo, hi, iters=200):
        flo = fun(lo)
        for _ in range(iters):
            mid = (lo + hi) / 2
            if flo * fun(mid) <= 0:
                hi = mid
            else:
                lo = mid
                flo = fun(lo)
        return (lo + hi) / 2

    for ss in ["0", "0.1", "0.2", "0.3", "0.5", "1"]:
        s = mp.mpf(ss)
        width = Bgain(d1, m1, s) - Bgain(d0, PI, s)
        # threshold mu for B^s=cH at each r (linear in mu)
        def tau_s(d):
            intercept = d["gL"] + s * d["w"]
            slope = (d["gH"] - d["gL"]) + s * d["Delta"]
            return (CH - intercept) / slope
        fun = lambda r: Bgain(auction(r), m1, s) - CH
        f_lo = fun(mp.mpf("1.01"))
        f_hi = fun(mp.mpf("9.999"))
        root = bisect_dec(fun, mp.mpf("1.01"), mp.mpf("9.999")) \
            if f_lo * f_hi < 0 else mp.nan
        print("s", ss, "window width", f6(width),
              "Bs r0(1/2)", f6(Bgain(d0, PI, s)),
              "Bs r1(M1)", f6(Bgain(d1, m1, s)),
              "Bs r1(m1)", f6(Bgain(d1, low_m, s)),
              "tau_s r1", f6(tau_s(d1)), "tau_s r0", f6(tau_s(d0)),
              "ceiling root in (1,10)", f6(root),
              "Bs at r=9.999,M1", f6(Bgain(auction(mp.mpf("9.999")), m1, s)))
    s_star = (CH - Bgain(d0, PI)) / (d0["w"] + d0["Delta"] * PI)
    print("s star at r0", mp.nstr(s_star, 12),
          "denominator w+Delta/2", f6(d0["w"] + d0["Delta"] * PI))
    d42 = auction(mp.mpf("4.2"))
    print("r4.2 Bs(M1) s=0", f6(Bgain(d42, m1)), "s=0.1",
          f6(Bgain(d42, m1, mp.mpf("0.1"))),
          "Bs(m1) s=0.1", f6(Bgain(d42, low_m, mp.mpf("0.1"))))
    # derivative check by central difference and by formula
    for rs in ["1.2", "3", "4.2"]:
        for ss in ["0", "0.5", "1"]:
            s = mp.mpf(ss)
            hh = mp.mpf("1e-6")
            r = mp.mpf(rs)
            num = (Bgain(auction(r + hh), PI, s)
                   - Bgain(auction(r - hh), PI, s)) / (2 * hh)
            d = auction(r)
            tl_p = (ELL * ELL - P * P) / (2 * r * r)
            t0_p = P * P / (r * r)
            de_p = mp.mpf("0.5") - ELL * ELL / (2 * r * r)
            formula = -(1 - s) * tl_p - s * t0_p - (1 - s) * PI * de_p
            print("deriv r", rs, "s", ss, "numeric", f6(num),
                  "formula", f6(formula))
    # disclosure with a stake: phi star from tau_s, same Delta and a
    for ss in ["0", "0.2", "0.5", "1"]:
        s = mp.mpf(ss)
        d = auction(mp.mpf(3))
        intercept = d["gL"] + s * d["w"]
        slope = (d["gH"] - d["gL"]) + s * d["Delta"]
        tau_s = (CH - intercept) / slope
        big_ts = tau_s / (1 - tau_s)
        phi1s = A * big_ts / (1 + A * big_ts)
        phi3s = big_ts / (A + big_ts)
        phi_nts = max(tau_s, 1 - K / d["Delta"])
        g3 = G1_closed(d, phi3s, mp.mpf(1), mp.mpf(1))
        star = phi3s if g3 > K else phi_nts
        star = min(phi_nts, star) if g3 > K else phi_nts
        gamma = d["Delta"] + (1 - RHO) * d["w"] / star
        margin = (RHO * d["w"] + gamma * phi1s
                  - outcome_fb(d, phi1s, mp.mpf(1), RHO)[2])
        print("toehold disclosure s", ss, "tau_s", f6(tau_s),
              "phi3_s", f6(phi3s), "phiNT_s", f6(phi_nts),
              "phi*_s used", f6(star), "pass", f6(PI / star),
              "E*", f6(RHO + (1 - RHO) * PI / star),
              "C_s margin", f6(margin), "G1(phi3_s)-k", f6(g3 - K))
    print()
    print("== H. What truthful bids hide: low type bids with a stake ==")
    # Low type bid b in [p, r]. Proceeds t(b) and bidder total payoff G_L(b).
    for rs in ["1.2", "3", "4.2"]:
        r = mp.mpf(rs)
        d = auction(r)
        for ss in ["0.1", "0.5", "1"]:
            s = mp.mpf(ss)
            bstar = (ELL + s * r) / (1 + s)
            def t_of_b(b):
                return b - b * b / (2 * r) + P * P / (2 * r)
            def g_low_total(b):
                num = (P * (ELL - (1 - s) * P) + (b - P) * ELL
                       - (1 - s) * (b * b - P * P) / 2 + s * b * (r - b))
                return num / r
            gain_opt = g_low_total(bstar) - s * d["t0"]
            gain_truth = d["gL"] + s * (d["tL"] - d["t0"])
            print("r", rs, "s", ss, "b*", f6(bstar),
                  "tL truthful", f6(d["tL"]), "tL(b*)", f6(t_of_b(bstar)),
                  "Delta truthful", f6(d["Delta"]),
                  "Delta with b*", f6(d["tH"] - t_of_b(bstar)),
                  "L entry gain truthful-bid formula", f6(gain_truth),
                  "L entry gain at b*", f6(gain_opt),
                  "difference", f6(gain_opt - gain_truth))


def region_probs(shift):
    # Total flow regions x<=0, x=1, x>=2 when total shift is shift.
    a = A
    c = (1 - a) / (1 + a)

    def p_le(t):
        if t < 0:
            return a ** (-t) / (1 + a)
        return 1 - a ** (t + 1) / (1 + a)

    def p_ge(t):
        if t > 0:
            return a ** t / (1 + a)
        if t == 0:
            return 1 / (1 + a)
        return 1 - p_le(t - 1)

    z1 = 1 - shift
    return [p_le(-shift), c * a ** abs(z1), p_ge(2 - shift)]


def hidden_prices(d, beta, sig_lo, sig_hi):
    # Cleaned-flow posteriors at pi=1/2 under investor buy prob beta (H only).
    lr_g = (1 - beta) + beta / A
    lr_b = (1 - beta) + beta * A
    mu_g = lr_g / (1 + lr_g)
    mu_b = lr_b / (1 + lr_b)
    hi_enters_good = mu_g >= d["tau"]
    hi_enters_bad = mu_b >= d["tau"]
    num = [mp.mpf(0)] * 3
    den = [mp.mpf(0)] * 3
    entry_prob = mp.mpf(0)
    oh_prob = mp.mpf(0)
    for is_h, pj in [(True, PI), (False, 1 - PI)]:
        tj = d["tH"] if is_h else d["tL"]
        qi_dist = [(1, beta), (0, 1 - beta)] if is_h else [(0, mp.mpf(1))]
        for is_lo, pc in [(True, RHO), (False, 1 - RHO)]:
            qc = sig_lo if is_lo else sig_hi
            for qi, pqi in qi_dist:
                if pqi == 0:
                    continue
                probs = region_probs(qi + qc)
                for s_idx in range(3):
                    good = (s_idx == 2) or (s_idx == 1 and qc == 0)
                    if is_lo:
                        enters = True
                    else:
                        enters = hi_enters_good if good else hi_enters_bad
                    val = tj if enters else d["t0"]
                    wt = pj * pc * pqi * probs[s_idx]
                    num[s_idx] += wt * val
                    den[s_idx] += wt
                    if enters:
                        entry_prob += wt
                        if is_h:
                            oh_prob += wt
    prices = [num[i] / den[i] for i in range(3)]
    return prices, mu_g, mu_b, entry_prob, oh_prob


def hidden_gains(d, beta, sig_lo, sig_hi):
    prices, mu_g, mu_b, entry_prob, oh_prob = hidden_prices(
        d, beta, sig_lo, sig_hi)
    hi_g = mu_g >= d["tau"]
    hi_b = mu_b >= d["tau"]

    def enters(is_lo, good):
        if is_lo:
            return True
        return hi_g if good else hi_b

    # Investor of class is_h deviates to buy one unit.
    inv_gain = {}
    for is_h in [True, False]:
        tj = d["tH"] if is_h else d["tL"]
        total = mp.mpf(0)
        for is_lo, pc in [(True, RHO), (False, 1 - RHO)]:
            qc = sig_lo if is_lo else sig_hi
            probs = region_probs(1 + qc)
            for s_idx in range(3):
                good = (s_idx == 2) or (s_idx == 1 and qc == 0)
                val = tj if enters(is_lo, good) else d["t0"]
                total += pc * probs[s_idx] * (val - prices[s_idx])
        inv_gain[is_h] = total - K
    # Challenger of cost type is_lo deviates to buy one unit.
    ch_gain = {}
    for is_lo in [True, False]:
        total = mp.mpf(0)
        for is_h, pj in [(True, PI), (False, 1 - PI)]:
            tj = d["tH"] if is_h else d["tL"]
            qi_dist = [(1, beta), (0, 1 - beta)] if is_h else [(0, mp.mpf(1))]
            for qi, pqi in qi_dist:
                if pqi == 0:
                    continue
                probs = region_probs(qi + 1)
                for s_idx in range(3):
                    good = (s_idx == 2)
                    val = tj if enters(is_lo, good) else d["t0"]
                    total += pj * pqi * probs[s_idx] * (val - prices[s_idx])
        ch_gain[is_lo] = total - K
    return prices, inv_gain, ch_gain, entry_prob, oh_prob


def section_hidden():
    print()
    print("== I. Hidden unit (T3): own region computation ==")
    for rs in ["1.2", "3", "3.6", "4.2"]:
        d = auction(mp.mpf(rs))
        print("r", rs, "tau", f6(d["tau"]))
        eqs = []
        for beta in [0, 1]:
            for sig_lo in [0, 1]:
                for sig_hi in [0, 1]:
                    prices, inv, chg, eprob, ohprob = hidden_gains(
                        d, mp.mpf(beta), sig_lo, sig_hi)
                    ok_beta = inv[True] > 0 if beta == 1 else inv[True] <= 0
                    ok_l = inv[False] <= 0
                    ok_lo = chg[True] > 0 if sig_lo == 1 else chg[True] <= 0
                    ok_hi = chg[False] > 0 if sig_hi == 1 else chg[False] <= 0
                    is_eq = ok_beta and ok_l and ok_lo and ok_hi
                    if is_eq:
                        eqs.append((beta, sig_lo, sig_hi))
                    print("  beta", beta, "sigL", sig_lo, "sigH", sig_hi,
                          "eq", is_eq,
                          "invH net", f6(inv[True]),
                          "invL net", f6(inv[False]),
                          "challLo net", f6(chg[True]),
                          "challHi net", f6(chg[False]),
                          "E", f6(eprob), "OH", f6(ohprob),
                          "prices", [f6(x) for x in prices])
        print("  equilibria in the 8 pure profiles:", eqs)
        # dominance grid over mixed beta and all price-schedule sigma profiles
        lo_vals = []
        hi_vals = []
        for bnum in range(5):
            beta = mp.mpf(bnum) / 4
            for sig_lo in [0, 1]:
                for sig_hi in [0, 1]:
                    _p, _inv, chg, _e, _o = hidden_gains(
                        d, beta, sig_lo, sig_hi)
                    lo_vals.append((chg[True], beta, sig_lo, sig_hi))
                    hi_vals.append((chg[False], beta, sig_lo, sig_hi))
        lo_vals.sort(key=lambda t: t[0])
        hi_vals.sort(key=lambda t: t[0])
        print("  grid beta in {0,.25,.5,.75,1} x 4 sigma schedules:")
        print("   smallest low-cost net", f6(lo_vals[0][0]),
              "at beta,sigL,sigH", f6(lo_vals[0][1]), lo_vals[0][2],
              lo_vals[0][3])
        print("   largest high-cost net", f6(hi_vals[-1][0]),
              "at beta,sigL,sigH", f6(hi_vals[-1][1]), hi_vals[-1][2],
              hi_vals[-1][3])
        # investor gross gain at the claimed equilibrium profile
        beta_claim = mp.mpf(0) if rs == "1.2" else mp.mpf(1)
        _p, inv, _c, eprob, ohprob = hidden_gains(d, beta_claim, 1, 0)
        g1, eg, eb = G1_at(d, PI)
        print("  claimed profile investor gross (net+k)", f6(inv[True] + K),
              "baseline G1 at 1/2 (its profile)", f6(g1),
              "baseline G1 with (1,rho) forced",
              f6(G1_closed(d, PI, mp.mpf(1), RHO)),
              "E", f6(eprob), "OH", f6(ohprob))


def section_details():
    print()
    print("== J. Switch, thin gap, k ranges, interval bound ==")
    for rs in ["1.40", "1.41", "1.42", "1.43", "1.50"]:
        d = auction(mp.mpf(rs))
        cc = cond_c(d)
        print("switch r", rs, "phiNT", f6(cc["phi_nt"]),
              "phi3", f6(d["phi3"]), "phiFB", f6(cc["phi_fb"]),
              "phi*", f6(cc["star"]),
              "G1(phi3;1,1)-k", mp.nstr(cc["g_at_3"] - K, 8),
              "E*", f6(RHO + (1 - RHO) * PI / cc["star"]))

    def bisect(fun, lo, hi, iters=200):
        flo = fun(lo)
        for _ in range(iters):
            mid = (lo + hi) / 2
            if flo * fun(mid) <= 0:
                hi = mid
            else:
                lo = mid
                flo = fun(lo)
        return (lo + hi) / 2

    root_switch = bisect(
        lambda r: G1_closed(auction(r), auction(r)["phi3"],
                            mp.mpf(1), mp.mpf(1)) - K,
        mp.mpf("1.40"), mp.mpf("1.45"))
    print("root of G1(phi3(r);1,1)=k near switch", mp.nstr(root_switch, 12))
    for rs in ["1.8", "3"]:
        d = auction(mp.mpf(rs))
        root_fb = bisect(lambda phi: G1_closed(d, phi, mp.mpf(1), mp.mpf(1)) - K,
                         d["phi3"], mp.mpf("0.999"))
        print("thin gap r", rs, "FB (1,1) root", mp.nstr(root_fb, 12),
              "phiNT", f6(max(d["tau"], 1 - K / d["Delta"])),
              "gap width phiNT-root",
              mp.nstr(max(d["tau"], 1 - K / d["Delta"]) - root_fb, 8))
    # D6 k ranges at r=3 by direct formulas
    d = auction(mp.mpf(3))
    for ks in ["0.02", "0.2", "0.25", "0.3"]:
        kv = mp.mpf(ks)
        phi_nt = max(d["tau"], 1 - kv / d["Delta"])
        g3 = G1_closed(d, d["phi3"], mp.mpf(1), mp.mpf(1))
        phi_fb = d["phi3"] if g3 > kv else mp.inf
        star = min(phi_nt, phi_fb)
        gamma = d["Delta"] + (1 - RHO) * d["w"] / star
        margin = (RHO * d["w"] + gamma * d["phi1"]
                  - outcome_fb(d, d["phi1"], mp.mpf(1), RHO)[2])
        print("k range r3 k", ks, "phiNT", f6(phi_nt), "phiFB", f6(phi_fb),
              "phi*", f6(star), "C margin at this k", f6(margin),
              "G1(phi3;1,1)", f6(g3))
    # Interval bound for condition C at r=3 with a=exp(-1/2)
    iv = mp.iv
    ai = iv.exp(iv.mpf([-1, -1]) / 2)
    ri = iv.mpf([3, 3])
    pi_ = iv.mpf([1, 1]) / 2
    rhoi = iv.mpf([1, 1]) / 4
    t0 = pi_ * (1 - pi_ / ri)
    tH = ri / 2 + pi_ * pi_ / (2 * ri)
    tL = 1 - (1 - pi_ * pi_) / (2 * ri)
    gH = 10 - ri / 2 - pi_ * pi_ / (2 * ri)
    gL = (1 - pi_ * pi_) / (2 * ri)
    delta = tH - tL
    w = tL - t0
    tau = (5 - gL) / (gH - gL)
    big_t = tau / (1 - tau)
    phi1 = ai * big_t / (1 + ai * big_t)
    phi3 = big_t / (ai + big_t)
    gamma = delta + (1 - rhoi) * w / phi3
    pg = (phi1 + ai * (1 - phi1)) / (1 + ai)
    pb = (ai * phi1 + 1 - phi1) / (1 + ai)
    e_entry = pg + rhoi * pb
    oh = phi1 / (1 + ai) + rhoi * ai * phi1 / (1 + ai)
    val = w * e_entry + delta * oh
    margin_iv = (rhoi * w + gamma * phi1) - val
    print("interval a", ai)
    print("interval C margin at r=3 (phi*=phi3 branch)", margin_iv)


def main():
    section_d1_d3()
    section_d4_d6()
    section_exact()
    section_toehold_public()
    section_hidden()
    section_details()


if __name__ == "__main__":
    main()
