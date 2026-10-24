"""Closed forms of the memo for the three-point, buy-only model with c_L = 0.

Exact rational arithmetic.  These functions encode the characterization
(Results 4 to 7 of the memo).  The driver compares them with the
first-principles solver in tp_first_principles.py.
"""
from fractions import Fraction as F


def objects(par):
    h, ell, p, r = par["h"], par["ell"], par["p"], par["r"]
    t0 = p * (1 - p / r)
    tH = r / 2 + p * p / (2 * r)
    tL = ell - (ell * ell - p * p) / (2 * r)
    gH = h - r / 2 - p * p / (2 * r)
    gL = (ell * ell - p * p) / (2 * r)
    D = (r - ell) ** 2 / (2 * r)
    return {"t0": t0, "tH": tH, "tL": tL, "gH": gH, "gL": gL, "DeltaT": D,
            "wH": tH - t0, "wL": tL - t0}


def B(par, mu):
    o = objects(par)
    return o["gL"] + mu * (o["gH"] - o["gL"])


def tau(par):
    o = objects(par)
    return (par["cH"] - o["gL"]) / (o["gH"] - o["gL"])


def m_lam(par):
    pi, lam = par["pi"], par["lam"]
    return pi * (1 - lam) / (1 - pi * lam)


def region(par):
    """Region I-V of the memo (by the threshold belief tau)."""
    t, m, pi = tau(par), m_lam(par), par["pi"]
    if t <= m:
        return "I"
    if t < pi:
        return "II"
    if t == pi:
        return "III"
    if t <= 1:
        return "IV"
    return "V"


def K_values(par):
    o = objects(par)
    pi, rho = par["pi"], par["rho"]
    Kr = F(2, 3) * rho * (1 - pi) * o["DeltaT"]
    K1 = F(2, 3) * (1 - pi) * o["DeltaT"]
    return Kr, K1


def K_rule_E(par):
    Kr, K1 = K_values(par)
    return K1 if tau(par) <= par["pi"] else Kr


def schedule(par, s, xi=None):
    """Posteriors, flow weights, entry and prices at effective purchase s.

    xi: optional dict flow -> high-cost preparation probability, used only at
    flows whose posterior equals tau (challenger mixing).  Rule E otherwise.
    """
    o = objects(par)
    pi, rho = par["pi"], par["rho"]
    t = tau(par)
    mu = {-1: pi * (1 - s) / (1 - pi * s), 0: pi, 1: pi}
    w = {-1: (1 - pi * s) / 3, 0: F(1, 3), 1: F(1, 3)}
    if s > 0:
        mu[2] = F(1)
        w[2] = pi * s / 3
    ent = {}
    for x, m in mu.items():
        if xi is not None and x in xi and m == t:
            ent[x] = rho + (1 - rho) * xi[x]
        else:
            ent[x] = rho + (1 - rho) * (1 if m >= t else 0)
    price = {x: o["t0"] + ent[x] * (o["wL"] + o["DeltaT"] * mu[x]) for x in mu}
    return mu, w, ent, price


def outcomes(par, s, bH, xi=None):
    o = objects(par)
    pi, rho, cH, lam, k, p, r = (par["pi"], par["rho"], par["cH"], par["lam"],
                                 par["k"], par["p"], par["r"])
    mu, w, ent, price = schedule(par, s, xi)
    e2 = ent.get(2, F(0))
    eH = ((1 - s) * ent[-1] + ent[0] + ent[1] + s * e2) / 3
    eL = (ent[-1] + ent[0] + ent[1]) / 3
    E = pi * eH + (1 - pi) * eL
    OH = pi * eH
    RT = o["t0"] + pi * eH * o["wH"] + (1 - pi) * eL * o["wL"]
    Wrho = ((r * r - p * p) / (2 * r)
            + rho * (pi * o["gH"] + (1 - pi) * o["gL"] + p * p / r))
    W = Wrho + sum(w[x] * (ent[x] - rho) * (B(par, mu[x]) - cH + p * p / r)
                   for x in mu)
    var = pi * s * (1 - pi) ** 2 / (3 * (1 - pi * s))
    Kbuy = (ent[0] + ent[1]) / 3 * (1 - pi) * o["DeltaT"]
    profit = lam * pi * bH * (Kbuy - k) if bH > 0 else F(0)
    return {"E": E, "OH": OH, "RT": RT, "W": W, "Var": var,
            "profit": profit, "UH": Kbuy - k, "price": price, "post": mu,
            "entry": ent}


def predicted_beta(par, inv_rule="Z", offpath="IC"):
    """Equilibrium purchase probabilities of the present high class (rule E).

    Returns a list of exact values, or the string 'interval' for [0, 1],
    or [] when no equilibrium exists.
    """
    o = objects(par)
    K = K_rule_E(par)
    k = par["k"]
    ebar = (F(3, 2) * K) / ((1 - par["pi"]) * o["DeltaT"])
    if offpath == "IC":
        Knt = K
    elif offpath == "passive":
        Knt = ebar * (1 - par["pi"]) * o["DeltaT"]
    else:
        raise ValueError(offpath)
    out = []
    if k < K or (k == K and inv_rule == "M"):
        out.append(F(1))
    if k >= Knt:
        out.append(F(0))
    if k == K and inv_rule == "M":
        return "interval"
    return out
