"""Extension exercises for the three-point model (exact rationals, print only).

Run from the repository root:
  .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/A_three_point/tp_extensions.py

Sections:
  A. presence table at r = 3
  B. Section 4.2 controls and Section 6.1 access to prices
  C. Section 6.3 reserve comparison (point masses and value bands)
  D. moderate-value specification (Section 5.2)
  E. bargaining institution (Section 6.2) with the discrete trading stage
  F. complementary private signals (Proposition A.7 analog)
  G. atomless preparation costs (Proposition A.6 analog)
  H. three-point noise away from equal probabilities (knife-edge lemma)
"""
import sys
from fractions import Fraction as F

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import tp_first_principles as fp  # noqa: E402
import tp_closed_form as cf  # noqa: E402

BENCH = {"h": F(10), "ell": F(1), "p": F(1, 2), "rho": F(1, 4), "cL": F(0),
         "cH": F(6), "k": F(1, 50), "r": F(3), "lam": F(1), "pi": F(1, 2)}
GRID = [F(0), F(1, 4), F(1, 2), F(3, 4), F(1)]


def fmt(x):
    if isinstance(x, F):
        if x.denominator == 1:
            return f"{x.numerator}"
        return f"{x.numerator}/{x.denominator} ({float(x):.6f})"
    return str(x)


def par_with(**kw):
    q = dict(BENCH)
    q.update(kw)
    return q


def show_eq(par, label, **kw):
    eqs = fp.equilibria(par, kw.pop("grid", GRID), **kw)
    seen = set()
    print(f"  {label}: {len(eqs)} equilibrium schedule(s)")
    for e in eqs:
        key = (e["bH"], e["bL"], tuple(sorted(e["entry"].items())))
        if key in seen:
            continue
        seen.add(key)
        print(f"    bH={fmt(e['bH'])} bL={fmt(e['bL'])} entry="
              f"{ {x: fmt(v) for x, v in e['entry'].items()} }")
        print(f"      E={fmt(e['E'])} O_H={fmt(e['OH'])} R_T={fmt(e['RT'])} "
              f"W={fmt(e['W'])}")
        print(f"      Var={fmt(e['Var'])} profit={fmt(e['profit'])} "
              f"U_H(buy)={fmt(e['UH'])}")
    return eqs


# ---------------------------------------------------------------------------
def section_A():
    print("=" * 78)
    print("A. Presence table at r = 3 (benchmark, c_L = 0, pi = 1/2, rules Z, E, IC)")
    for lam in (F(1, 10), F(1, 4), F(1, 2), F(3, 4), F(9, 10), F(1)):
        par = par_with(lam=lam)
        eqs = fp.equilibria(par, GRID)
        for e in eqs:
            c = cf.outcomes(par, lam * e["bH"], e["bH"])
            print(f"  lam={fmt(lam)}: bH={fmt(e['bH'])} E={fmt(e['E'])} "
                  f"O_H={fmt(e['OH'])} R_T={fmt(e['RT'])} W={fmt(e['W'])} "
                  f"Var={fmt(e['Var'])} profit={fmt(e['profit'])}")
            print(f"      closed form E - first principles: {fmt(c['E'] - e['E'])};"
                  f" formula rho+(1-rho)pi*lam/3 = "
                  f"{fmt(par['rho'] + (1 - par['rho']) * par['pi'] * lam / 3)}")


# ---------------------------------------------------------------------------
def hidden_economy(par, bH):
    """Challenger cannot see the price: entry e_r(pi) at every flow."""
    A = fp.auction_objects(par["h"], par["ell"], par["p"], par["r"])
    t0, tH, tL, gH, gL = A["t0"], A["tH"], A["tL"], A["gH"], A["gL"]
    pi, rho, cH, k, lam = par["pi"], par["rho"], par["cH"], par["k"], par["lam"]
    Bpi = gL + pi * (gH - gL)
    dH = F(1) if Bpi >= cH else F(0)
    e = rho + (1 - rho) * dH
    flows, fH, fL = fp.flow_laws(lam, bH, F(0))
    w = {x: pi * fH[x] + (1 - pi) * fL[x] for x in flows}
    mu = {x: (pi * fH[x] / w[x]) if w[x] > 0 else F(1) for x in flows}
    price = {x: t0 + e * (tL - t0 + (tH - tL) * mu[x]) for x in flows}
    UH = sum(fp.EQUAL_NOISE[z] * (t0 + e * (tH - t0) - price[z + 1])
             for z in (-1, 0, 1)) - k
    RT = t0 + e * (pi * (tH - t0) + (1 - pi) * (tL - t0))
    alloc = (A["alloc0"] + e * (pi * (A["allocH"] - A["alloc0"])
                                + (1 - pi) * (A["allocL"] - A["alloc0"])))
    W = alloc - (1 - rho) * dH * cH
    return {"entry": e, "UH": UH, "RT": RT, "W": W}


def section_B():
    print("=" * 78)
    print("B. Controls (Section 4.2) and access to prices (Section 6.1)")
    for r in (F(6, 5), F(3)):
        par = par_with(r=r)
        fixed = cf.outcomes(par, F(1), F(1))
        hid0 = hidden_economy(par, F(0))
        hid1 = hidden_economy(par, F(1))
        print(f"  r={fmt(r)}: frozen full buying entry E={fmt(fixed['E'])};"
              f" hidden-price entry={fmt(hid0['entry'])};"
              f" hidden-price U_H(buy) against full buying={fmt(hid1['UH'])};"
              f" feedback U_H(buy)={fmt(fixed['UH'])}")
    par = par_with(r=F(3))
    fb = cf.outcomes(par, F(1), F(1))
    hid = hidden_economy(par, F(1))
    print(f"  r=3 access to prices: R_T feedback={fmt(fb['RT'])},"
          f" hidden={fmt(hid['RT'])}, difference={fmt(fb['RT'] - hid['RT'])}")
    print(f"                        W feedback={fmt(fb['W'])},"
          f" hidden={fmt(hid['W'])}, difference={fmt(fb['W'] - hid['W'])}")
    o = cf.objects(par)
    print("  formula (1-rho)(pi lam/3) w_H =",
          fmt((1 - par['rho']) * par['pi'] * par['lam'] / 3 * o['wH']))
    print("  formula (1-rho)(pi lam/3)(g_H - c_H + p^2/r) =",
          fmt((1 - par['rho']) * par['pi'] * par['lam'] / 3
              * (o['gH'] - par['cH'] + par['p'] ** 2 / par['r'])))
    print("  Region II (c_H = 4, r = 3): access to prices")
    for lam in (F(1), F(1, 2)):
        par = par_with(cH=F(4), lam=lam)
        fb = cf.outcomes(par, lam, F(1))
        hid = hidden_economy(par, F(1))
        print(f"    lam={fmt(lam)}: R_T feedback={fmt(fb['RT'])} hidden="
              f"{fmt(hid['RT'])} diff={fmt(fb['RT'] - hid['RT'])};"
              f" W feedback={fmt(fb['W'])} hidden={fmt(hid['W'])}"
              f" diff={fmt(fb['W'] - hid['W'])};"
              f" U_H feedback={fmt(fb['UH'])} hidden={fmt(hid['UH'])}")


# ---------------------------------------------------------------------------
def reserve_case(r, p, band, ch_rule="E"):
    par = par_with(r=r, p=p)
    A = fp.auction_objects(par["h"], par["ell"], p, r, band)
    eqs = fp.equilibria(par, GRID, band=band, ch_rule=ch_rule,
                        xi_grid=(F(0), F(1, 2), F(1)))
    out = []
    for e in eqs:
        # sale and two-admissible-bidder probabilities
        prR = (r - p) / r if p < r else F(0)
        admH = F(1) if par["h"] >= p else F(0)
        admL_mass = F(1) if (band is None and par["ell"] >= p) else F(0)
        if band is not None:
            lo, hi = par["ell"] - band, par["ell"] + band
            admL_mass = max(F(0), min(F(1), (hi - max(p, lo)) / (hi - lo)))
        Aprob = par["pi"] * e["eH"] * admH + (1 - par["pi"]) * e["eL"] * admL_mass
        S = prR + Aprob - prR * Aprob
        C2 = prR * Aprob
        out.append((e, A, S, C2))
    return out


def section_C():
    print("=" * 78)
    print("C. Reserve comparison (Section 6.3), c_L = 0, benchmark otherwise")
    for band in (None, F(1, 20)):
        lab = "point masses" if band is None else "value bands +/- 1/20"
        print(f"  {lab}:")
        for r in (F(6, 5), F(3)):
            for p in (F(1, 2), F(11, 10)):
                for (e, A, S, C2) in reserve_case(r, p, band):
                    print(f"    r={fmt(r)} p={fmt(p)}: DeltaT={fmt(A['DeltaT'])}"
                          f" gL={fmt(A['gL'])} bH={fmt(e['bH'])}"
                          f" E={fmt(e['E'])} R_T={fmt(e['RT'])}"
                          f" sale={fmt(S)} two-admissible={fmt(C2)}")
    print("  rule X at the low-cost indifference (p = 11/10 > ell, posterior 0):")
    for r in (F(6, 5), F(3)):
        seen = set()
        for (e, A, S, C2) in reserve_case(r, F(11, 10), None, ch_rule="X"):
            key = (e["E"], e["RT"])
            if key in seen:
                continue
            seen.add(key)
            print(f"    r={fmt(r)}: entry at flow -1={fmt(e['entry'][-1])}"
                  f" E={fmt(e['E'])} R_T={fmt(e['RT'])}")


# ---------------------------------------------------------------------------
def section_D():
    print("=" * 78)
    print("D. Moderate values (h=2, ell=1, p=1/2, rho=1/4, c_H=89/100,"
          " k=1/500), c_L = 0")
    base = {"h": F(2), "ell": F(1), "p": F(1, 2), "rho": F(1, 4), "cL": F(0),
            "cH": F(89, 100), "k": F(1, 500), "lam": F(1), "pi": F(1, 2)}
    for r in (F(21, 20), F(3, 2), F(19, 10), F(199, 100)):
        par = dict(base)
        par["r"] = r
        o = cf.objects(par)
        Kr, K1 = cf.K_values(par)
        print(f"  r={fmt(r)}: B(1/2)={fmt(cf.B(par, F(1, 2)))} gH={fmt(o['gH'])}"
              f" K_rho={fmt(Kr)} region={cf.region(par)}")
        show_eq(par, "equilibria")
    print(f"  h/2 - p^2/(2h) = {fmt(base['h'] / 2 - base['p'] ** 2 / (2 * base['h']))}"
          f" versus c_H = {fmt(base['cH'])}")


# ---------------------------------------------------------------------------
def bargaining_objects(par, eta):
    """Verifiable-value institution, zero reserve, uniform incumbent [0, r]."""
    r, h, ell = par["r"], par["h"], par["ell"]

    def Emin(theta):
        return theta - theta * theta / (2 * r) if theta < r else r / 2

    ER = r / 2
    out = {"t0": eta * ER}
    for cls, th in (("H", h), ("L", ell)):
        emin = Emin(th)
        emax = ER + th - emin
        out["t" + cls] = (1 - eta) * emin + eta * emax
        out["g" + cls] = (1 - eta) * (th - emin)
        out["win" + cls] = min(th / r, F(1))
        out["alloc" + cls] = emax
    out["alloc0"] = ER
    out["DeltaT"] = out["tH"] - out["tL"]
    return out


def section_E():
    print("=" * 78)
    print("E. Bargaining institution with the discrete stage (zero reserve)")
    for eta in (F(0), F(1, 4), F(1, 2), F(3, 4)):
        for r in (F(6, 5), F(3)):
            par = par_with(r=r)
            ob = bargaining_objects(par, eta)
            Delta = ob["DeltaT"]
            formula = eta * (par["h"] - par["ell"]) + (1 - 2 * eta) * (r - par["ell"]) ** 2 / (2 * r)
            Bpi = ob["gL"] + par["pi"] * (ob["gH"] - ob["gL"])
            ebar = F(1) if Bpi >= par["cH"] else par["rho"]
            K = F(2, 3) * ebar * (1 - par["pi"]) * Delta
            eqs = fp.equilibria(par, GRID, objects=ob)
            bset = sorted(set(e["bH"] for e in eqs))
            Es = sorted(set(e["E"] for e in eqs))
            print(f"  eta={fmt(eta)} r={fmt(r)}: Delta_eta={fmt(Delta)}"
                  f" (formula {fmt(formula)}) G_L={fmt(ob['gL'])}"
                  f" B(pi)={fmt(Bpi)} K_eta={fmt(K)} -> bH={[fmt(b) for b in bset]}"
                  f" E={[fmt(x) for x in Es]}")
    print("  small cost k = 1/500 with eta = 1/4 (window K_eta(r0) <= k < K_eta(r1)?)")
    for eta in (F(1, 4),):
        for r in (F(6, 5), F(3)):
            par = par_with(r=r, k=F(1, 500))
            ob = bargaining_objects(par, eta)
            print(f"    eta={fmt(eta)} r={fmt(r)}: K_eta="
                  f"{fmt(F(2, 3) * par['rho'] * (1 - par['pi']) * ob['DeltaT'])}")


# ---------------------------------------------------------------------------
def signals_economy(par, a, d, bplus, bminus):
    """Complementary signals: investor sees T (accuracy a), buyer sees Y (d).

    Canonical schedule: the price reveals the public posterior.  Returns
    payoffs of both investor signals and outcome measures.
    """
    A = fp.auction_objects(par["h"], par["ell"], par["p"], par["r"])
    t0, tH, tL, gH, gL = A["t0"], A["tH"], A["tL"], A["gH"], A["gL"]
    wH, wL = tH - t0, tL - t0
    rho, cL, cH, k, lam = par["rho"], par["cL"], par["cH"], par["k"], par["lam"]
    pi = F(1, 2)
    pT = {"H": {"+": a, "-": 1 - a}, "L": {"+": 1 - a, "-": a}}
    pY = {"H": {"+": d, "-": 1 - d}, "L": {"+": 1 - d, "-": d}}
    beta = {"+": bplus, "-": bminus}
    noise = fp.EQUAL_NOISE
    flows = (-1, 0, 1, 2)

    def fx_T(T, x):
        b = lam * beta[T]
        return (1 - b) * noise.get(x, F(0)) + b * noise.get(x - 1, F(0))

    fstate = {th: {x: sum(pT[th][T] * fx_T(T, x) for T in "+-") for x in flows}
              for th in "HL"}
    wx = {x: pi * fstate["H"][x] + (1 - pi) * fstate["L"][x] for x in flows}
    mu = {x: (pi * fstate["H"][x] / wx[x]) if wx[x] > 0 else a for x in flows}

    def entry_state(m):
        es = {}
        for th in "HL":
            tot = F(0)
            for y in "+-":
                if y == "+":
                    phi = d * m / (d * m + (1 - d) * (1 - m))
                else:
                    phi = (1 - d) * m / ((1 - d) * m + d * (1 - m))
                B = gL + phi * (gH - gL)
                tot += pY[th][y] * (rho * (1 if B >= cL else 0)
                                    + (1 - rho) * (1 if B >= cH else 0))
            es[th] = tot
        return es

    ent = {x: entry_state(mu[x]) for x in flows}
    price = {x: t0 + mu[x] * ent[x]["H"] * wH + (1 - mu[x]) * ent[x]["L"] * wL
             for x in flows}
    U = {}
    for T in "+-":
        qH = pi * pT["H"][T] / (pi * pT["H"][T] + (1 - pi) * pT["L"][T])
        tot = F(0)
        for z in (-1, 0, 1):
            x = z + 1
            val = t0 + qH * ent[x]["H"] * wH + (1 - qH) * ent[x]["L"] * wL
            tot += noise[z] * (val - price[x])
        U[T] = tot - k
    eH = sum(fstate["H"][x] * ent[x]["H"] for x in flows if wx[x] > 0)
    eL = sum(fstate["L"][x] * ent[x]["L"] for x in flows if wx[x] > 0)
    E = pi * eH + (1 - pi) * eL
    Dhalf = (entry_state(F(1, 2))["L"] * (tH - tL)
             + (entry_state(F(1, 2))["H"] - entry_state(F(1, 2))["L"]) * wH)
    return {"U": U, "E": E, "mu": mu, "ent": ent, "Dhalf": Dhalf}


def section_F():
    print("=" * 78)
    print("F. Complementary signals (Proposition A.7 analog), paper example with c_L = 0")
    base = {"h": F(10), "ell": F(1), "p": F(1, 2), "rho": F(85, 100), "cL": F(0),
            "cH": F(714, 100), "k": F(15, 1000), "lam": F(1), "pi": F(1, 2)}
    a, d = F(70, 100), F(75, 100)
    for r in (F(11, 10), F(23, 10)):
        par = dict(base)
        par["r"] = r
        o = cf.objects(par)
        phi_plus_a = d * a / (d * a + (1 - d) * (1 - a))
        phi_minus_a = (1 - d) * a / ((1 - d) * a + d * (1 - a))
        print(f"  r={fmt(r)}: B(d)={fmt(cf.B(par, d))} B(phi+(a))="
              f"{fmt(cf.B(par, phi_plus_a))} B(phi-(a))={fmt(cf.B(par, phi_minus_a))}"
              f" c_H={fmt(par['cH'])}")
        Ksig = (2 * a - 1) * par["rho"] * o["DeltaT"] / 3
        print(f"    K_sig=(2a-1) rho DeltaT/3={fmt(Ksig)} k={fmt(par['k'])}")
        for bp, bm in ((F(0), F(0)), (F(1), F(0)), (F(1), F(1)), (F(0), F(1))):
            res = signals_economy(par, a, d, bp, bm)
            print(f"    profile (beta+, beta-)=({fmt(bp)}, {fmt(bm)}):"
                  f" U(+)={fmt(res['U']['+'])} U(-)={fmt(res['U']['-'])}"
                  f" E={fmt(res['E'])}")
        res = signals_economy(par, a, d, F(1), F(0))
        print(f"    (2a-1) D(1/2)/3 - k = "
              f"{fmt((2 * a - 1) * res['Dhalf'] / 3 - par['k'])}")
        Ef = par["rho"] + (1 - par["rho"]) * par["lam"] / 6 * (a * d + (1 - a) * (1 - d))
        print(f"    formula entry under full buying = rho + (1-rho)(lam/6)"
              f"[ad+(1-a)(1-d)] = {fmt(Ef)}")


# ---------------------------------------------------------------------------
def section_G():
    print("=" * 78)
    print("G. Atomless preparation costs (Proposition A.6 analog)")
    print("  low component uniform on [0, eL]; high component uniform on"
          " [c_H - eC, c_H + eC]")
    eL, eC = F(1, 50), F(1, 10)
    for r in (F(6, 5), F(3), F(7), F(791, 100), F(797, 100), F(8), F(9)):
        par = par_with(r=r)
        o = cf.objects(par)

        def ent(mu):
            Bv = o["gL"] + mu * (o["gH"] - o["gL"])
            lowpart = min(F(1), max(F(0), Bv / eL))
            hp = min(F(1), max(F(0), (Bv - (par["cH"] - eC)) / (2 * eC)))
            return par["rho"] * lowpart + (1 - par["rho"]) * hp

        pi = par["pi"]
        K = F(2, 3) * ent(pi) * (1 - pi) * o["DeltaT"]
        # full buying, lam = 1, pi = 1/2: flow weights 1/6, 1/3, 1/3, 1/6
        Efull = (ent(F(0)) + 4 * ent(pi) + ent(F(1))) / 6
        print(f"  r={fmt(r)}: gL={fmt(o['gL'])} (needs eL <= gL: {eL <= o['gL']})"
              f" e(0)={fmt(ent(F(0)))} e(1/2)={fmt(ent(pi))} e(1)={fmt(ent(F(1)))}"
              f" K={fmt(K)} trade={K > par['k']} entry(full)={fmt(Efull)}")


# ---------------------------------------------------------------------------
def section_H():
    print("=" * 78)
    print("H. Three-point noise (a, d, c) away from equal probabilities,"
          " r = 3, pi = 1/2, lam = 1")
    laws = [(F(1, 3), F(1, 3), F(1, 3)), (F(1, 10), F(1, 5), F(7, 10)),
            (F(7, 10), F(1, 5), F(1, 10)), (F(1, 4), F(1, 2), F(1, 4)),
            (F(3, 10), F(1, 3), F(11, 30))]
    for (a, d, c) in laws:
        noise = {-1: a, 0: d, 1: c}
        par = par_with()
        print(f"  noise (a,d,c)=({fmt(a)}, {fmt(d)}, {fmt(c)}):")
        o = cf.objects(par)
        Kdev = (1 - par["pi"]) * o["DeltaT"] * par["rho"] * (a + d)
        print(f"    no-trade deviation value K(0) = (1-pi) DeltaT rho (a+d)"
              f" = {fmt(Kdev)}")
        for b in (F(1, 4), F(1, 2), F(3, 4), F(1)):
            res = fp.solve(par, b, F(0), inv_rule="none", noise=noise)
            for e in res[:1]:
                print(f"    bH={fmt(b)}: gross buy value K(s)={fmt(e['UH'] + par['k'])}"
                      f" posteriors={ {x: fmt(v) for x, v in e['post'].items()} }"
                      f" entry={ {x: fmt(v) for x, v in e['entry'].items()} }")
        K1 = fp.solve(par, F(1), F(0), inv_rule="none", noise=noise)[0]["UH"] + par["k"]
        kmid = (Kdev + K1) / 2
        print(f"    K(lam) = {fmt(K1)}; test cost k = (K(0) + K(lam))/2 = {fmt(kmid)}")
        q = par_with(k=kmid)
        fine = [F(j, 20) for j in range(21)]
        signs = []
        for b in fine:
            e = fp.solve(q, b, F(0), inv_rule="none", noise=noise)[0]
            signs.append("+" if e["UH"] > 0 else ("0" if e["UH"] == 0 else "-"))
        print(f"    sign of U_H(buy) at bH = 0, 1/20, ..., 1: {''.join(signs)}")
        for rule in ("Z", "M"):
            eqs = fp.equilibria(q, fine, inv_rule=rule, noise=noise)
            print(f"    k={fmt(kmid)} rule {rule}: equilibria on the grid, bH ="
                  f" {sorted(set(fmt(e['bH']) for e in eqs))}")


def main():
    section_A()
    section_B()
    section_C()
    section_D()
    section_E()
    section_F()
    section_G()
    section_H()


if __name__ == "__main__":
    main()
