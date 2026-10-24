"""Who gains? Ledger of the stake equilibria (exact fractions for the three-point model; mpmath for D-Laplace).

Both models share one ledger: a list of flow classes c with posterior mu_c and entry e_c, and the class
probabilities of a buyer and of a non-buyer in each type. Print only.

Run from the repository root:
    .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/C5_stake/welfare.py
"""
import os
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tp_lib as T  # noqa: E402
import dl_lib as DL  # noqa: E402
from dl_enumerate import equilibria as dl_equilibria  # noqa: E402
from dl_thresholds import consts as dl_consts, thresholds as dl_thresholds  # noqa: E402
from mpmath import mp, mpf, nstr  # noqa: E402

mp.dps = 40


def ledger(a, par, classes, pbuy, pnot, bH, bL, omega, base_entry=None):
    """classes: dict c -> (mu_c, phi_c). pbuy/pnot: dict c -> probability of class c after buying / not buying.

    Returns dict of ledger lines. Works for Fractions and mpf alike.
    """
    rho, cH, cL, k = par["rho"], par["cH"], par["cL"], par["k"]
    D, wL, wH, t0, r = a["D"], a["wL"], a["wH"], a["t0"], a["r"]
    p = par["p"]
    e = {c: rho + (1 - rho) * classes[c][1] for c in classes}
    mu = {c: classes[c][0] for c in classes}
    PH = {c: bH * pbuy[c] + (1 - bH) * pnot[c] for c in classes}
    PL = {c: bL * pbuy[c] + (1 - bL) * pnot[c] for c in classes}
    eH = sum(PH[c] * e[c] for c in classes)
    eL = sum(PL[c] * e[c] for c in classes)
    half = 1 / (1 + 1) if not isinstance(D, F) else F(1, 2)
    E = (eH + eL) * half
    OH = eH * half
    T_ = t0 + half * (wH * eH + wL * eL)                     # target proceeds per share
    # challenger: gross profit minus cost, averaged over costs and flows
    Pc = {c: half * (PH[c] + PL[c]) for c in classes}
    B = lambda m: a["gL"] + m * (a["gH"] - a["gL"])
    PiC = sum(Pc[c] * (rho * (B(mu[c]) - cL) + (1 - rho) * classes[c][1] * (B(mu[c]) - cH)) for c in classes)
    # incumbent
    Pi0 = (r - p) ** 2 / (2 * r)
    PiI = half * ((1 - eH) * Pi0) + half * ((1 - eL) * Pi0 + eL * D)
    # investor trading: gross profit of a buyer by type
    residH = {c: e[c] * D * (1 - mu[c]) for c in classes}
    residL = {c: -e[c] * D * mu[c] for c in classes}
    grossH = sum(pbuy[c] * residH[c] for c in classes)
    grossL = sum(pbuy[c] * residL[c] for c in classes)
    tradeH = bH * (grossH - k)
    tradeL = bL * (grossL - k)
    noise_loss = half * (bH * grossH + bL * grossL)          # noise traders lose what the investor gains
    stakeH = omega * (t0 + wH * eH)
    stakeL = omega * (t0 + wL * eL)
    cost = k * half * (bH + bL)
    S = T_ + PiI + PiC - cost                                # total surplus (k is a resource cost)
    # cross-check: value of the winner minus preparation costs, from the auction primitives
    V0 = (r * r - p * p) / (2 * r)
    Vl = (r * r + par["l"] ** 2) / (2 * r)
    Vh = par["h"]
    prep = sum(Pc[c] * (rho * cL + (1 - rho) * classes[c][1] * cH) for c in classes)
    S_direct = half * ((1 - eH) * V0 + eH * Vh) + half * ((1 - eL) * V0 + eL * Vl) - prep - cost
    return dict(E=E, OH=OH, eH=eH, eL=eL, T=T_, PiC=PiC, PiI=PiI, grossH=grossH, grossL=grossL,
                tradeH=tradeH, tradeL=tradeL, noise_loss=noise_loss, stakeH=stakeH, stakeL=stakeL,
                stake_ex_ante=half * (stakeH + stakeL), S=S,
                inv_total_ex_ante=half * (stakeH + tradeH + stakeL + tradeL), S_check=S - S_direct)


def fmt(x):
    try:
        return f"{float(x):.6f}"
    except TypeError:
        return nstr(x, 8)


def show(label, L):
    keys = ("E", "OH", "T", "PiC", "PiI", "noise_loss", "tradeH", "tradeL", "inv_total_ex_ante", "S", "S_check")
    print(f"  {label:34s} " + " ".join(f"{k_}={fmt(L[k_])}" for k_ in keys))


def three_point(r, rows):
    par = T.BENCH
    a = T.auction(r, par)
    third = F(1, 3)
    # classes: flows -1,0,1,2. posterior and phi are supplied per row
    for label, (bH, bL, omega, phi2) in rows.items():
        fH, fL = T.flows(bH, bL)
        classes = {}
        for x in (-1, 0, 1, 2):
            s = fH[x] + fL[x]
            m = fH[x] / s if s != 0 else F(1, 2)
            ph = F(0)
            if x == 2:
                ph = phi2
            classes[x] = (m, ph)
        pbuy = {-1: F(0), 0: third, 1: third, 2: third}
        pnot = {-1: third, 0: third, 1: third, 2: F(0)}
        L = ledger(a, par, classes, pbuy, pnot, bH, bL, omega)
        show(label, L)


def dl_rows(r, rows):
    par = DL.BENCH
    a = DL.auction(r, par)
    aa, delta, g0, g1 = dl_consts(par)
    for label, (bH, bL, omega, phiG) in rows.items():
        M, m = DL.posteriors(bH, bL, par)
        classes = {"G": (M, phiG), "B": (m, mpf(0))}
        pbuy = {"G": g1, "B": 1 - g1}
        pnot = {"G": g0, "B": 1 - g0}
        L = ledger(a, par, classes, pbuy, pnot, bH, bL, omega)
        show(label, L)


if __name__ == "__main__":
    par = T.BENCH
    rho, k = par["rho"], par["k"]
    print("THREE-POINT MODEL, r1 = 3 (c_L = 0). Columns: E entry, OH high-value ownership, T target proceeds per share,")
    print("PiC challenger net profit, PiI incumbent profit, noise_loss, tradeH/tradeL investor net trading by type,")
    print("inv_total_ex_ante investor payoff incl. stake, S total surplus (k as resource cost).")
    a1 = T.auction(T.R1, par)
    tau1 = T.tau_of(a1, par)
    bmax = 1 / tau1 - 1
    Om2 = ((rho + tau1) * a1["D"] + 3 * k) / ((1 - rho) * a1["wL"])
    Om1 = ((1 + rho) * a1["D"] + 3 * k) / ((1 - rho) * a1["wL"])

    def e2_mix(om):
        return (3 * k + rho * a1["D"] + rho * om * a1["wL"]) / (om * a1["wL"] - a1["D"] * tau1)

    def phi_of(e2):
        return (e2 - rho) / (1 - rho)

    def beta_star(om):
        den = om * a1["wL"] * (1 - rho) - rho * a1["D"] - 3 * k
        return a1["D"] / den - 1

    rows = {}
    # hidden price: entry rho everywhere, same investor orders as S for the trading part
    rows["S (any omega <= Omega1)"] = (F(1), F(0), F(0), F(1))
    om_mid = F(23, 10)
    rows[f"M beta*={float(beta_star(om_mid)):.4f}, omega=2.3"] = (F(1), beta_star(om_mid), om_mid, F(1))
    rows["M at beta_max, omega=Omega2"] = (F(1), bmax, Om2, F(1))
    for om in (F(3), F(5), F(10), F(100)):
        rows[f"M' omega={om}"] = (F(1), bmax, om, phi_of(e2_mix(om)))
    three_point(T.R1, rows)

    print("\nHidden-price reference at r1 (entry rho at every flow; investor buys/sells as in S): ")
    # entry rho everywhere
    classes = {x: (F(1, 2), F(0)) for x in (-1, 0, 1, 2)}
    third = F(1, 3)
    pbuy = {-1: F(0), 0: third, 1: third, 2: third}
    pnot = {-1: third, 0: third, 1: third, 2: F(0)}
    # posteriors for the trading residual under hidden price: use the S posteriors but entry rho
    fH, fL = T.flows(F(1), F(0))
    cl = {x: ((fH[x] / (fH[x] + fL[x])), F(0)) for x in (-1, 0, 1, 2)}
    L = ledger(a1, par, cl, pbuy, pnot, F(1), F(0), F(0))
    show("hidden price, S orders", L)

    print("\nTHREE-POINT MODEL, r0 = 6/5")
    a0 = T.auction(T.R0, par)
    tau0 = T.tau_of(a0, par)
    rows0 = {"no trade (entry rho)": (F(0), F(0), F(0), F(0)),
             "S (omega in (0.1805, 0.2723])": (F(1), F(0), F(1, 5), F(1))}
    # no trade: flow 2 unused; classes posterior 1/2 with phi 0 for on-path flows
    three_point(T.R0, rows0)

    print("\nDISCRETE LAPLACE, r1 = 3 (c_H = 5)")
    t1 = dl_thresholds(DL.R1, DL.BENCH)
    rows = {"S (omega<=Omega1)": (mpf(1), mpf(0), mpf(0), mpf(1))}
    for om in (mpf("3.5"), mpf(5), mpf(20), mpf(100)):
        eqs = dl_equilibria(DL.R1, om)
        for eq in eqs:
            if eq["kind"] == "M":
                rows[f"M omega={nstr(om,4)}"] = (eq["bH"], eq["bL"], om, mpf(1))
            if eq["kind"] == "M'":
                rows[f"M' omega={nstr(om,4)}"] = (eq["bH"], eq["bL"], om, eq["phiG"])
    dl_rows(DL.R1, rows)
