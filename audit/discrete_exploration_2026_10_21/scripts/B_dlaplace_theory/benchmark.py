"""Print-only evaluation of the theory results in memos/B_dlaplace_theory.md (50-digit arithmetic).

The script evaluates the closed forms of the memo at stated parameters: thresholds, the
equilibrium set at a fixed strength under each tie-rule pair, the Table 2 analog, the general
prior, presence, and the c_H variant. It prints values only. Nothing is asserted.

Run from the repository root:
    .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/B_dlaplace_theory/benchmark.py
"""
from mpmath import mp, mpf, exp, sqrt, nstr, sech

mp.dps = 50


def show(x, d=10):
    return nstr(x, d)


class Econ:
    """Primitives; defaults are the team benchmark (c_L = 0, c_H = 5)."""

    def __init__(self, h=10, ell=1, p="0.5", rho="0.25", cH=5, k="0.02", b=2, pi="0.5", lam=1):
        self.h, self.ell, self.p = mpf(h), mpf(ell), mpf(p)
        self.rho, self.cH, self.k, self.b = mpf(rho), mpf(cH), mpf(k), mpf(b)
        self.pi, self.lam = mpf(pi), mpf(lam)
        self.a = exp(-1 / self.b)
        self.g = 1 / (1 + self.a)          # P(good news | buy) = P(Z >= 0)
        self.d = 2 * self.g - 1            # (1 - a)/(1 + a)

    # auction objects, paper eq. (4)
    def obj(self, r):
        h, l, p = self.h, self.ell, self.p
        return dict(t0=p * (1 - p / r), tH=r / 2 + p**2 / (2 * r), tL=l - (l**2 - p**2) / (2 * r),
                    gH=h - r / 2 - p**2 / (2 * r), gL=(l**2 - p**2) / (2 * r), D=(r - l) ** 2 / (2 * r),
                    ERp=(r**2 - p**2) / (2 * r))

    def B(self, r, mu):
        o = self.obj(r)
        return o["gL"] + mu * (o["gH"] - o["gL"])

    def tau(self, r):
        o = self.obj(r)
        return (self.cH - o["gL"]) / (o["gH"] - o["gL"])

    # information structure under s = lam * beta_H, beta_L = 0
    def Np(self, s):
        return 1 - self.g + self.pi * self.d * s

    def Nm(self, s):
        return self.g - self.pi * self.d * s

    def mu_up(self, s):
        return self.pi * (1 - self.g + self.d * s) / self.Np(s)

    def mu_dn(self, s):
        return self.pi * (self.g - self.d * s) / self.Nm(s)

    def M1(self):
        return self.pi / (self.pi + (1 - self.pi) * self.a)

    def m1(self):
        return self.pi * self.a / (self.pi * self.a + 1 - self.pi)

    def kappa(self):
        return (1 - self.pi) * self.g * (1 - self.g)

    def K(self, r, s, eu, ed):
        return self.obj(r)["D"] * self.kappa() * (eu / self.Np(s) + ed / self.Nm(s))

    def s_star(self, r):
        """Purchase rate at which the good-news posterior equals tau (None if not in (0, lam])."""
        t = self.tau(r)
        if t <= self.pi:
            return None
        v = (1 - self.g) * (t - self.pi) / (self.pi * self.d * (1 - t))
        return v if v <= self.lam else None

    def Lambda(self):
        """min over y in [0, pi*d*lam] of (1-pi) g(1-g) [1/(1-g+y) + 1/(g-y)]."""
        ymax = self.pi * self.d * self.lam
        y = min(ymax, self.d / 2)
        return self.kappa() * (1 / (1 - self.g + y) + 1 / (self.g - y))

    def outcomes(self, r, s, zeta):
        """Outcomes when the high-cost type enters with probability zeta after good news, never after bad news."""
        o = self.obj(r)
        rho, pi, g, d = self.rho, self.pi, self.g, self.d
        eu = rho + (1 - rho) * zeta
        ed = rho
        pupH, pupL = 1 - g + d * s, 1 - g
        eH = pupH * eu + (1 - pupH) * ed
        eL = pupL * eu + (1 - pupL) * ed
        E = pi * eH + (1 - pi) * eL
        OH = pi * eH
        RT = o["t0"] + pi * eH * (o["tH"] - o["t0"]) + (1 - pi) * eL * (o["tL"] - o["t0"])
        W = o["ERp"] + pi * eH * (o["gH"] + self.p**2 / r) + (1 - pi) * eL * (o["gL"] + self.p**2 / r) - self.cH * (E - rho)
        Kg = self.K(r, s, eu, ed)
        return dict(E=E, OH=OH, RT=RT, W=W, Pi_gross=pi * s * Kg, Pi_net=pi * s * (Kg - self.k), K=Kg)


def frak_r(ell, dd):
    return ell + dd + sqrt(dd**2 + 2 * ell * dd)


def bisect(fun, lo, hi, n=200):
    flo = fun(lo)
    for _ in range(n):
        mid = (lo + hi) / 2
        fm = fun(mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


def r_ceiling(e, mu):
    """Root of B_r(mu) = c_H above ell (paper eq. A.11 with M -> mu)."""
    h, l, p, c = e.h, e.ell, e.p, e.cH
    return (mu * h - c + sqrt((mu * h - c) ** 2 + mu * ((1 - mu) * l**2 - p**2))) / mu


def thresholds(e, verbose=True):
    pi, rho, k, lam = e.pi, e.rho, e.k, e.lam
    out = {}
    out["r_N"] = frak_r(e.ell, k / (rho * (1 - pi)))
    out["r_NT_suff"] = frak_r(e.ell, k / (1 - pi))
    out["r_U_suff"] = frak_r(e.ell, k / (rho * e.Lambda()))
    out["r_C"] = r_ceiling(e, e.mu_up(lam))
    KF_hat = e.kappa() * (1 / e.Np(lam) + rho / e.Nm(lam))
    out["r_F"] = frak_r(e.ell, k / KF_hat)
    # r_I: K_1(s*(r)) = k ; r_U: K_rho(s*(r)) = k, on (ell, r_C)
    def f_I(r):
        s = e.s_star(r)
        return e.K(r, s, mpf(1), rho) - k
    def f_U(r):
        s = e.s_star(r)
        return e.K(r, s, rho, rho) - k
    lo, hi = e.ell + mpf("1e-30"), out["r_C"] - mpf("1e-30")
    if e.s_star(lo) is None:
        lo = bisect(lambda r: e.tau(r) - pi, e.ell + mpf("1e-9"), out["r_C"]) + mpf("1e-25")
    out["r_I"] = bisect(f_I, lo, hi) if f_I(lo) < 0 < f_I(hi) else None
    out["r_U"] = bisect(f_U, lo, hi) if f_U(lo) < 0 < f_U(hi) else None
    if verbose:
        for kk in ["r_I", "r_F", "r_N", "r_U", "r_C", "r_NT_suff", "r_U_suff"]:
            print(f"   {kk:10s} = {show(out[kk], 15) if out[kk] is not None else 'none'}")
    return out


def eq_set(e, r):
    """Equilibrium set at strength r, assuming pi <= 1/2 and B_r(pi) < c_H (memo, Result 5)."""
    rho, k, lam = e.rho, e.k, e.lam
    res = []
    K0 = e.K(r, mpf(0), rho, rho)
    ss = e.s_star(r)
    full_rec = ss is not None and ss < lam
    KF = e.K(r, lam, mpf(1) if full_rec else rho, rho)
    # rules: I0 = investor picks 0 at indifference; IM = any mixture. C1 = enter at indifference; CM = any mixture.
    if k >= K0:
        res.append(("no trade", mpf(0), mpf(0), "all rules"))
    if k < KF:
        res.append(("full", lam, mpf(1) if full_rec else mpf(0), "all rules"))
    elif k == KF:
        res.append(("full", lam, mpf(1) if full_rec else mpf(0), "IM only"))
    if ss is None or not full_rec:
        Kl = e.K(r, lam, rho, rho)
        if Kl < k < K0:
            st = bisect(lambda s: e.K(r, s, rho, rho) - k, mpf(0), lam)
            res.append(("mixed, entry rho", st, mpf(0), "IM only"))
        return res, dict(K0=K0, KF=KF)
    Krs, K1s = e.K(r, ss, rho, rho), e.K(r, ss, mpf(1), rho)
    if Krs < k < K0:
        st = bisect(lambda s: e.K(r, s, rho, rho) - k, mpf(0), ss)
        res.append(("mixed below s*, entry rho", st, mpf(0), "IM only"))
    if Krs <= k <= K1s:
        # K(s*; zeta) = D kappa [(rho + (1-rho) zeta)/N+ + rho/N-] = k, solved for zeta
        zeta = ((k / (e.obj(r)["D"] * e.kappa()) - rho / e.Nm(ss)) * e.Np(ss) - rho) / (1 - rho)
        res.append(("mixed at s*, challenger mixes", ss, zeta, "IM and CM"))
    if KF < k < K1s:
        st = bisect(lambda s: e.K(r, s, mpf(1), rho) - k, ss, lam)
        res.append(("mixed above s*, recruitment", st, mpf(1), "IM only"))
    return res, dict(K0=K0, KF=KF, Kr_star=Krs, K1_star=K1s, s_star=ss)


def print_eq(e, r):
    res, Ks = eq_set(e, r)
    print(f"  r = {show(r, 6)}: " + ", ".join(f"{kk}={show(v, 8)}" for kk, v in Ks.items()))
    for name, s, zeta, rule in res:
        oc = e.outcomes(r, s, zeta)
        print(f"     {name:32s} s={show(s,8):>12s} zeta={show(zeta,8):>12s} [{rule}]  E={show(oc['E'],8)}"
              f" O_H={show(oc['OH'],8)} R_T={show(oc['RT'],8)}")


def prop2_check(e, r0, r1, r2):
    pi, rho, k, lam = e.pi, e.rho, e.k, e.lam
    o0, o1, o2 = e.obj(r0), e.obj(r1), e.obj(r2)
    print(f"  (A1) c_L = 0 < B_r(m1(pi)) at r2: B = {show(e.B(r2, e.m1()), 10)}")
    print(f"  (A2) B_r0(pi) = {show(e.B(r0, pi), 12)} < c_H = {show(e.cH, 6)} <= B_r1(mu+(lam)) = {show(e.B(r1, e.mu_up(lam)), 12)}")
    print(f"  (A2') B_r2(mu+(lam)) = {show(e.B(r2, e.mu_up(lam)), 12)} < c_H  [part (iii)]")
    print(f"  (A3) (1-pi) D(r0) = {show((1 - pi) * o0['D'], 12)} < k = {show(k, 6)} < rho Lambda D(r1) = {show(rho * e.Lambda() * o1['D'], 12)}")
    print(f"       Lambda = {show(e.Lambda(), 15)}; at pi = 1/2, lam = 1 it equals (1/2) sech^2(1/(2b)) = {show(sech(1 / (2 * e.b))**2 / 2, 15)}")
    for lab, r, s, z in [("r0", r0, mpf(0), mpf(0)), ("r1", r1, lam, mpf(1)), ("r2", r2, lam, mpf(0))]:
        oc = e.outcomes(r, s, z)
        print(f"  {lab} = {show(r,4)}: E = {show(oc['E'],12)}, O_H = {show(oc['OH'],12)}, R_T = {show(oc['RT'],12)},"
              f" W = {show(oc['W'],12)}, investor gross = {show(oc['Pi_gross'],12)}, net = {show(oc['Pi_net'],12)}")
    print(f"  closed forms at r1: E = rho + (1-rho)(pi + (1-pi)a)/(1+a) = {show(rho + (1 - rho) * (pi + (1 - pi) * e.a) / (1 + e.a), 12)};"
          f" O_H = pi[rho + (1-rho)/(1+a)] = {show(pi * (rho + (1 - rho) / (1 + e.a)), 12)}")


def table2(e, r0, r1, r2):
    rho = e.rho
    print("  Panel A (equilibrium outcomes)")
    for lab, r, s, z in [("weak r0", r0, mpf(0), mpf(0)), ("strong r1", r1, e.lam, mpf(1)), ("very strong r2", r2, e.lam, mpf(0))]:
        oc = e.outcomes(r, s, z)
        print(f"    {lab:16s} r={show(r,4):5s} s={show(s,3)}  E={show(oc['E'],6)}  O_H={show(oc['OH'],6)}  R_T={show(oc['RT'],6)}  W={show(oc['W'],6)}")
    print("  Panel B (controls)")
    for r in [r0, r1]:
        up, dn = e.mu_up(e.lam), e.mu_dn(e.lam)
        zu = mpf(1) if e.B(r, up) >= e.cH else mpf(0)
        zd = mpf(1) if e.B(r, dn) >= e.cH else mpf(0)
        oc = e.outcomes(r, e.lam, zu)
        print(f"    frozen full orders r={show(r,4)}: B(mu+)={show(e.B(r, up),8)}, B(mu-)={show(e.B(r, dn),8)}"
              f"  E={show(oc['E'],6)}  O_H={show(oc['OH'],6)}  R_T={show(oc['RT'],6)}  (zeta at bad news = {zd})")
    for r in [r0, r1]:
        # hidden price: entry rho at every flow; investor order from K_rho
        Kmax = e.K(r, mpf(0), rho, rho)
        Kmin = e.K(r, e.lam, rho, rho)
        s = mpf(0) if Kmax <= e.k else (e.lam if Kmin > e.k else None)
        oc = e.outcomes(r, s, mpf(0))
        print(f"    price hidden r={show(r,4)}: K_rho(0)={show(Kmax,8)}, K_rho(lam)={show(Kmin,8)} -> s={show(s,3)}"
              f"  E={show(oc['E'],6)}  O_H={show(oc['OH'],6)}  R_T={show(oc['RT'],6)}  W={show(oc['W'],6)}"
              f"  investor gross={show(oc['Pi_gross'],8)} net={show(oc['Pi_net'],8)}")
    acc = e.outcomes(r1, e.lam, mpf(1))
    hid = e.outcomes(r1, e.lam, mpf(0))
    print(f"  Panel C (access at r1 = {show(r1,4)})")
    for kk, lab in [("RT", "target proceeds"), ("W", "net acquisition surplus (c_L = 0)"),
                    ("Pi_gross", "investor gross profit"), ("Pi_net", "investor net profit")]:
        print(f"    {lab:36s} observed={show(acc[kk],8)}  hidden={show(hid[kk],8)}  gain={show(acc[kk]-hid[kk],8)}")
    o1 = e.obj(r1)
    up = e.mu_up(e.lam)
    dW = (1 - rho) * e.Np(e.lam) * (e.B(r1, up) - e.cH + e.p**2 / r1)
    dR = (1 - rho) * (e.pi * (1 - e.g + e.d * e.lam) * (o1["tH"] - o1["t0"]) + (1 - e.pi) * (1 - e.g) * (o1["tL"] - o1["t0"]))
    print(f"    closed forms: dW = (1-rho) N+ [B(mu+) - c_H + p^2/r] = {show(dW,10)};  dR_T = {show(dR,10)}")


def main():
    print("=== 1. Team benchmark: pi = 1/2, lam = 1, b = 2, c_H = 5, k = 0.02, rho = 0.25, c_L = 0 ===")
    e = Econ()
    print(f"  a = {show(e.a,15)}, gamma = {show(e.g,15)}, delta = {show(e.d,15)}, m1 = {show(e.m1(),15)}, M1 = {show(e.M1(),15)}")
    print("  Thresholds:")
    th = thresholds(e)
    print("  Proposition 2 analog at (r0, r1, r2) = (1.2, 3, 4.2):")
    prop2_check(e, mpf("1.2"), mpf(3), mpf("4.2"))
    print("  c_H window for parts (i)-(ii): (B_1.2(1/2), B_3(M1)] =", f"({show(e.B(mpf('1.2'), e.pi),10)}, {show(e.B(mpf(3), e.M1()),10)}]")
    print("  part (iii) at r2 = 4.2 needs c_H >", show(e.B(mpf("4.2"), e.M1()), 10), "; at r2 = 3.6 needs c_H >", show(e.B(mpf("3.6"), e.M1()), 10))
    print("  Feedback ratio K_F/K_0 at lam = 1 = 2 gamma(1-gamma)(1+rho)/rho =", show(2 * e.g * (1 - e.g) * (1 + e.rho) / e.rho, 12))

    print("\n=== 2. Equilibrium set across strengths (benchmark) ===")
    for r in ["1.05", "1.2", "1.3", "1.4", "1.42", "1.44", "1.45", "1.5", "1.55", "1.6", "1.65", "1.7", "1.74", "1.75", "1.76", "1.77", "1.8", "2", "3", "3.6", "3.98", "4.2", "6"]:
        r = mpf(r)
        if e.B(r, e.pi) >= e.cH:
            print(f"  r = {r}: prior recruits; outside the stated domain")
            continue
        print_eq(e, r)

    print("\n=== 3. Table 2 analog (benchmark, r = 1.2, 3, 4.2) ===")
    table2(e, mpf("1.2"), mpf(3), mpf("4.2"))
    print("  matched dividend (Section 6.1 analog) = gain in mean price = gain in R_T above")

    print("\n=== 4. Variant c_H = 5.2: the paper's strengths (1.2, 3, 3.6) ===")
    e2 = Econ(cH="5.2")
    thresholds(e2)
    prop2_check(e2, mpf("1.2"), mpf(3), mpf("3.6"))
    table2(e2, mpf("1.2"), mpf(3), mpf("3.6"))
    for r in ["1.5", "1.6", "1.7"]:
        print_eq(e2, mpf(r))

    print("\n=== 5. Window dependence on b (pi = 1/2, r0 = 1.2, r1 = 3) ===")
    for b in ["1", "1.5", "2", "3", "4", "4.044", "5"]:
        eb = Econ(b=b)
        top = eb.B(mpf(3), eb.M1())
        print(f"  b={b:6s} M1={show(eb.M1(),10)}  c_H window top B_3(M1)={show(top,10)} (bottom {show(eb.B(mpf('1.2'), eb.pi),10)})"
              f"  k window top rho Lambda D(3) = {show(eb.rho * eb.Lambda() * eb.obj(mpf(3))['D'],10)}  r_C(c_H=5) = {show(r_ceiling(eb, eb.M1()),10)}")
    eb = Econ()
    target = eb.B(mpf("1.2"), mpf("0.5"))
    o3 = eb.obj(mpf(3))
    Mneed = (target - o3["gL"]) / (o3["gH"] - o3["gL"])
    from mpmath import log
    bcrit = 1 / log(Mneed / (1 - Mneed))
    print(f"  window closes when M1 = {show(Mneed,12)}, i.e. b = 1/logit(M1) = {show(bcrit,12)}")

    print("\n=== 6. General prior (lam = 1, b = 2): c_H at the window midpoint ===")
    for pi in ["0.3", "0.5", "0.7"]:
        ep = Econ(pi=pi)
        lo, hi = ep.B(mpf("1.2"), ep.pi), ep.B(mpf(3), ep.M1())
        cH = (lo + hi) / 2
        ep = Econ(pi=pi, cH=cH)
        print(f"  pi = {pi}: m1(pi) = {show(ep.m1(),10)}, M1(pi) = {show(ep.M1(),10)}; c_H window ({show(lo,10)}, {show(hi,10)}], use c_H = {show(cH,10)}")
        th = thresholds(ep)
        r2 = th["r_C"] * mpf("1.1")
        prop2_check(ep, mpf("1.2"), mpf(3), r2)
        print(f"  K_0 = rho(1-pi)D, K_F/K_0 at lam=1: {show(ep.kappa() * (1/ep.Np(1) + ep.rho/ep.Nm(1)) / (ep.rho * (1 - ep.pi)), 10)}")
        if mpf(pi) <= mpf("0.5"):
            for r in ["1.5", "1.6", "1.7", "2"]:
                print_eq(ep, mpf(r))

    print("\n=== 7. Presence probability (pi = 1/2, c_H = 5, b = 2) ===")
    e3 = Econ()
    t3 = e3.tau(mpf(3))
    lam_need = (1 - e3.g) * (2 * t3 - 1) / (e3.d * (1 - t3))
    print(f"  recruitment at r1 = 3 under full buying needs mu+(lam) >= tau(3) = {show(t3,12)}, i.e. lam >= {show(lam_need,12)}")
    for lam in ["0.5", "0.8", "1"]:
        el = Econ(lam=lam)
        print(f"  lam = {lam}: mu+ = {show(el.mu_up(el.lam),10)}, mu- = {show(el.mu_dn(el.lam),10)}, Lambda = {show(el.Lambda(),10)}")
        thresholds(el)
        for r in ["1.2", "1.6", "3", "4.2"]:
            print_eq(el, mpf(r))

    print("\n=== 8. Deterrence case: the prior already recruits (c_H = 4, r = 3, pi = 1/2, lam = 1) ===")
    e4 = Econ(cH=4)
    r = mpf(3)
    o = e4.obj(r)
    t = e4.tau(r)
    s_minus = e4.g * (e4.pi - t) / (e4.pi * e4.d * (1 - t))
    print(f"  B_3(1/2) = {show(e4.B(r, e4.pi),10)} >= c_H = 4; tau = {show(t,10)}; bad news deters once s > s_- = {show(s_minus,10)}")
    # hidden price: both cost types enter at every flow; orders: K with entry 1 everywhere
    K_hidden_min = e4.K(r, mpf(1), mpf(1), mpf(1))
    print(f"  hidden price: entry 1; K(1; 1, 1) = {show(K_hidden_min,10)} > k, so full purchases; R_T = (t_H + t_L)/2 = {show((o['tH'] + o['tL'])/2,10)}")
    W_hid = o["ERp"] + e4.pi * (o["gH"] + e4.p**2 / r) + (1 - e4.pi) * (o["gL"] + e4.p**2 / r) - e4.cH * (1 - e4.rho)
    acc = e4.outcomes(r, mpf(1), mpf(1))
    print(f"  K on the bad-news-deterring piece at s = 1: {show(e4.K(r, mpf(1), mpf(1), e4.rho),10)}; on s < s_- with entry 1: K(s_-; 1, 1) = {show(e4.K(r, s_minus, mpf(1), mpf(1)),10)}")
    print(f"  access: E = {show(acc['E'],10)}, R_T = {show(acc['RT'],10)}, W = {show(acc['W'],10)};  hidden: E = 1, R_T = {show((o['tH'] + o['tL'])/2,10)}, W = {show(W_hid,10)}")
    print(f"  access changes R_T by {show(acc['RT'] - (o['tH'] + o['tL'])/2,10)} and W by {show(acc['W'] - W_hid,10)}")


if __name__ == "__main__":
    main()
