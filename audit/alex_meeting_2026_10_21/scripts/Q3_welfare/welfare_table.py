"""Print-only welfare accounting at the benchmark vector.

Computes each group's expected payoff at r0 and r1, with and without
price access (Section 6.1 / Prop. A.9 of the paper). No assertions:
identity residuals are printed for visual inspection.
Run: .venv/bin/python audit/alex_meeting_2026_10_21/scripts/Q3_welfare/welfare_table.py
"""
import mpmath as mp

mp.mp.dps = 30

# Benchmark vector (Appendix A.8)
h, ell, p = mp.mpf(10), mp.mpf(1), mp.mpf("0.5")
rho, cL, cH = mp.mpf("0.25"), mp.mpf(1), mp.mpf(6)
b, k = mp.mpf(2), mp.mpf("0.02")
omega = mp.mpf("0.5")  # illustrative liquidity-trader share of float


def auction(r):
    t0 = p * (1 - p / r)
    tH = r / 2 + p**2 / (2 * r)
    tL = ell - (ell**2 - p**2) / (2 * r)
    gH = h - r / 2 - p**2 / (2 * r)
    gL = (ell**2 - p**2) / (2 * r)
    DT = (r - ell) ** 2 / (2 * r)
    I0 = (r - p) ** 2 / (2 * r)          # incumbent, no entry
    IL = (r - ell) ** 2 / (2 * r)        # incumbent, entry with low challenger (= DT)
    IH = mp.mpf(0)                       # incumbent, entry with high challenger (h > r)
    return dict(t0=t0, tH=tH, tL=tL, gH=gH, gL=gL, DT=DT, I0=I0, IL=IL, IH=IH)


def f(z):
    return mp.exp(-abs(z) / b) / (2 * b)


def mu_full(x):
    """Posterior under full orders (1,-1)."""
    aH, aL = f(x - 1), f(x + 1)
    return aH / (aH + aL)


def gross_informed_profit(r, access):
    """Pi = E[q(V_T-P)] under full orders, via residual advantages (eq. 11)."""
    A = auction(r)
    DT = A["DT"]
    if access:
        tau = (cH - A["gL"]) / (A["gH"] - A["gL"])
    else:
        tau = None

    def e_of(mu):
        if not access:
            return rho
        return rho + (1 - rho) * (1 if mu >= tau else 0)

    def integrand_H(x):
        mu = mu_full(x)
        return f(x - 1) * e_of(mu) * DT * (1 - mu)

    def integrand_L(x):
        mu = mu_full(x)
        return f(x + 1) * e_of(mu) * DT * mu

    # split at kink points -1, x*, 1 for accuracy
    pts = [mp.ninf, -1, 1, mp.inf]
    if access:
        xs = (b / 2) * mp.log(tau / (1 - tau))
        pts = [mp.ninf, -1, xs, 1, mp.inf]
    EH = mp.quad(integrand_H, pts)
    EL = mp.quad(integrand_L, pts)
    return (EH + EL) / 2, EH, EL


def regime(r, access, trading):
    A = auction(r)
    t0, tH, tL, gH, gL = A["t0"], A["tH"], A["tL"], A["gH"], A["gL"]
    I0, IL, IH = A["I0"], A["IL"], A["IH"]
    if trading and access:
        tau = (cH - gL) / (gH - gL)
        xs = (b / 2) * mp.log(tau / (1 - tau))
        aH = 1 - mp.mpf("0.5") * mp.exp((xs - 1) / b)
        aL = mp.mpf("0.5") * mp.exp(-(xs + 1) / b)
    else:
        tau = xs = None
        aH = aL = mp.mpf(0)
    eH = rho + (1 - rho) * aH
    eL = rho + (1 - rho) * aL
    E_entry = (eH + eL) / 2
    RT = t0 + (eH * (tH - t0) + eL * (tL - t0)) / 2
    incumbent = ((1 - eH) * I0 + eH * IH + (1 - eL) * I0 + eL * IL) / 2
    chal_gross = (eH * gH + eL * gL) / 2
    prep_cost = rho * cL + (1 - rho) * cH * (aH + aL) / 2
    # challenger net, split by cost type (low always enters; high enters iff mu>=tau)
    gbar = (gH + gL) / 2
    chal_net = rho * (gbar - cL) + (1 - rho) * (aH * (gH - cH) + aL * (gL - cH)) / 2
    Wsurplus = RT + incumbent + chal_gross - prep_cost
    if trading:
        Pi, EH, EL = gross_informed_profit(r, access)
        inv_net = Pi - k
    else:
        Pi, EH, EL, inv_net = mp.mpf(0), mp.mpf(0), mp.mpf(0), mp.mpf(0)
    noise_fin = omega * RT - Pi           # liquidity traders (financial only)
    lt = (1 - omega) * RT                 # long-term holders
    init_sh = RT - Pi                     # total initial shareholders (omega cancels)
    return dict(r=r, access=access, trading=trading, tau=tau, xs=xs, aH=aH, aL=aL,
                eH=eH, eL=eL, E=E_entry, RT=RT, incumbent=incumbent,
                chal_gross=chal_gross, chal_net=chal_net, prep=prep_cost,
                W=Wsurplus, Pi=Pi, EH=EH, EL=EL, inv_net=inv_net,
                noise=noise_fin, lt=lt, init=init_sh, **A)


regs = {
    "r0 access (eqm: no trade)": regime(mp.mpf("1.2"), True, False),
    "r0 hidden (eqm: no trade)": regime(mp.mpf("1.2"), False, False),
    "r1 access (eqm: full)": regime(mp.mpf(3), True, True),
    "r1 hidden (eqm: full)": regime(mp.mpf(3), False, True),
    "r1 no investor (counterfactual)": regime(mp.mpf(3), True, False),
}

rows = [
    ("Entry E", "E"), ("e_H", "eH"), ("e_L", "eL"),
    ("alpha_H", "aH"), ("alpha_L", "aL"), ("tau", "tau"), ("x*", "xs"),
    ("Seller / target proceeds R_T (=E[V_T])", "RT"),
    ("Long-term holders (1-omega)R_T", "lt"),
    ("Liquidity traders, financial omega*R_T - Pi", "noise"),
    ("Initial shareholders total R_T - Pi", "init"),
    ("Informed investor gross Pi", "Pi"),
    ("Informed investor net Pi - k", "inv_net"),
    ("  of which state-H buy leg E[A_H|H]", "EH"),
    ("  of which state-L sell leg E[A_L|L]", "EL"),
    ("Market makers (expected)", None),
    ("Incumbent", "incumbent"),
    ("Challenger gross (entry-weighted)", "chal_gross"),
    ("Challenger net of prep costs", "chal_net"),
    ("Expected prep costs paid", "prep"),
    ("Acquisition surplus W (net of prep)", "W"),
]
names = list(regs)
print(f"{'object':52s}" + "".join(f"{n:>34s}" for n in names))
for label, key in rows:
    cells = ""
    for n in names:
        v = mp.mpf(0) if key is None else regs[n][key]
        cells += f"{'--':>34s}" if v is None else f"{mp.nstr(v, 10):>34s}"
    print(f"{label:52s}{cells}")

print()
ra, rh, rn = regs["r1 access (eqm: full)"], regs["r1 hidden (eqm: full)"], regs["r1 no investor (counterfactual)"]
r0 = regs["r0 access (eqm: no trade)"]
dR = ra["RT"] - rn["RT"]
print("Key comparisons at r1 (trade scale lambda = 1):")
print("  entry gain in proceeds, access vs no investor:  ", mp.nstr(dR, 10))
print("  investor gross with access Pi_acc:              ", mp.nstr(ra["Pi"], 10))
print("  investor gross hidden    Pi_hid:                ", mp.nstr(rh["Pi"], 10))
print("  net shareholder gain (b)-(a) = dR - Pi_acc:     ", mp.nstr(dR - ra["Pi"], 10))
print("  break-even trade scale lambda* = dR/Pi_acc:     ", mp.nstr(dR / ra["Pi"], 10))
print("  net shareholder gain (b)-(c) = dR-(Pi_acc-Pi_hid):", mp.nstr(dR - (ra["Pi"] - rh["Pi"]), 10))
print("  break-even scale for access alone dR/(Pi_acc-Pi_hid):", mp.nstr(dR / (ra["Pi"] - rh["Pi"]), 10))
print("  shareholder loss (c)-(a) = -Pi_hid:             ", mp.nstr(-rh["Pi"], 10))
print("  cross-r shareholder change S(r1,acc)-S(r0):     ", mp.nstr(ra["init"] - r0["init"], 10))
print("    = direct auction effect (hidden r1 minus r0 proceeds):", mp.nstr(rh["RT"] - r0["RT"], 10))
print("    + feedback entry gain:", mp.nstr(dR, 10), " - trading loss:", mp.nstr(ra["Pi"], 10))
print()
print("Identity residuals (should print near 0):")
for n in names:
    g = regs[n]
    # W decomposition: W = R_T + incumbent + challenger net
    print(f"  {n:34s} W-(RT+inc+chal_net) = {mp.nstr(g['W'] - (g['RT'] + g['incumbent'] + g['chal_net']), 4)}"
          f"   tH-tL-DT = {mp.nstr(g['tH'] - g['tL'] - g['DT'], 4)}"
          f"   IL-DT = {mp.nstr(g['IL'] - g['DT'], 4)}")
print()
print("Paper cross-checks (Table 2): R_T r0=0.392708, r1 acc=0.872392, r1 hid=0.614583;")
print("  W r1 acc=2.382301, hid=2.302083; E r1=0.522757; O_H r1=0.324192.")
print("  O_H here (r1 acc) =", mp.nstr((ra["eH"]) / 2, 10), "(high challenger always wins when prepared)")
print()
print("Closed-form check for Pi under full orders (J = m + (1/2) e^{-1/b} gd(1/b)):")
m_ = 1 / (1 + mp.exp(2 / b))
gd = lambda y: 2 * mp.atan(mp.exp(y)) - mp.pi / 2
J = m_ + mp.mpf("0.5") * mp.exp(-1 / b) * gd(1 / b)
A1 = auction(mp.mpf(3))
Pi_hid_cf = rho * A1["DT"] * J
xs = ra["xs"]
J_tail = m_ / 2 + mp.mpf("0.25") * mp.exp(-1 / b) * (gd(1 / b) - gd(xs / b))
Pi_acc_cf = A1["DT"] * (rho * J + (1 - rho) * J_tail)
print("  J =", mp.nstr(J, 12), " J_tail(x*) =", mp.nstr(J_tail, 12))
print("  Pi_hid closed form =", mp.nstr(Pi_hid_cf, 12), " quadrature =", mp.nstr(rh["Pi"], 12))
print("  Pi_acc closed form =", mp.nstr(Pi_acc_cf, 12), " quadrature =", mp.nstr(ra["Pi"], 12))
print()
print("Split of the (b)-(a) shareholder gain at r1 by subgroup (omega =", mp.nstr(omega, 3), "):")
print("  long-term holders: (1-omega)*dR        =", mp.nstr((1 - omega) * dR, 10))
print("  liquidity traders: omega*dR - Pi_acc   =", mp.nstr(omega * dR - ra["Pi"], 10))
print("  liquidity break-even omega* = Pi_acc/dR =", mp.nstr(ra["Pi"] / dR, 10))
print("  liquidity gain from access alone (b)-(c): omega*dR-(Pi_acc-Pi_hid) =",
      mp.nstr(omega * dR - (ra["Pi"] - rh["Pi"]), 10))
