"""First-principles solver for the three-point, buy-only trading stage.

Exact rational arithmetic throughout (fractions.Fraction).  Nothing in this
module uses the closed forms of the memo:

* auction objects come from piecewise integrals over the uniform incumbent;
* flow laws come from the convolution of orders with the noise law;
* posteriors come from Bayes' rule;
* prices come from competitive pricing, over every partition of the on-path
  flows into price blocks (the challenger sees the price only);
* investor payoffs are evaluated against the fixed candidate schedule.

The module prints nothing.  Drivers in this folder call it and print.
"""
from fractions import Fraction as F
from itertools import product

EQUAL_NOISE = {-1: F(1, 3), 0: F(1, 3), 1: F(1, 3)}


# ---------------------------------------------------------------------------
# Auction stage: uniform incumbent on [0, r], reserve p, second-price rule.
# A challenger value is either a point mass or a uniform band [lo, hi].
# Each object is a piecewise polynomial of degree <= 2 in the value theta,
# with breaks at p and r.  Pieces: (-inf, p), [p, r), [r, +inf).
# ---------------------------------------------------------------------------

def _pieces(name, p, r):
    """Coefficients (a0, a1, a2) of a0 + a1*theta + a2*theta^2 on each piece."""
    t0 = p * (r - p) / r
    alloc0 = (r * r - p * p) / (2 * r)
    if name == "t":        # expected target proceeds with this challenger
        return [(t0, F(0), F(0)),
                (p * p / (2 * r), F(1), F(-1) / (2 * r)),
                ((r * r + p * p) / (2 * r), F(0), F(0))]
    if name == "g":        # challenger's expected gross acquisition profit
        return [(F(0), F(0), F(0)),
                (-p * p / (2 * r), F(0), F(1) / (2 * r)),
                (-(r * r + p * p) / (2 * r), F(1), F(0))]
    if name == "alloc":    # expected allocation value with this challenger
        return [(alloc0, F(0), F(0)),
                (r / 2, F(0), F(1) / (2 * r)),
                (F(0), F(1), F(0))]
    if name == "win":      # probability that this challenger acquires
        return [(F(0), F(0), F(0)),
                (F(0), F(1) / r, F(0)),
                (F(1), F(0), F(0))]
    raise ValueError(name)


def _eval_point(name, theta, p, r):
    a = _pieces(name, p, r)
    idx = 0 if theta < p else (1 if theta < r else 2)
    a0, a1, a2 = a[idx]
    return a0 + a1 * theta + a2 * theta * theta


def _eval_band(name, lo, hi, p, r):
    """Average of the piecewise polynomial over theta uniform on [lo, hi]."""
    a = _pieces(name, p, r)
    breaks = [None, p, r, None]
    total = F(0)
    for idx in range(3):
        left = lo if breaks[idx] is None else max(lo, breaks[idx])
        right = hi if breaks[idx + 1] is None else min(hi, breaks[idx + 1])
        if right <= left:
            continue
        a0, a1, a2 = a[idx]
        total += (a0 * (right - left) + a1 * (right ** 2 - left ** 2) / 2
                  + a2 * (right ** 3 - left ** 3) / 3)
    return total / (hi - lo)


def auction_objects(h, ell, p, r, band=None):
    """t0, tH, tL, gH, gL, alloc0, allocH, allocL, winH, winL.

    band=None uses point masses at h and ell.  band=eps uses uniform value
    classes [h-eps, h+eps] and [ell-eps, ell+eps].
    """
    t0 = p * (r - p) / r
    alloc0 = (r * r - p * p) / (2 * r)
    out = {"t0": t0, "alloc0": alloc0}
    for cls, v in (("H", h), ("L", ell)):
        for name in ("t", "g", "alloc", "win"):
            if band is None:
                val = _eval_point(name, v, p, r)
            else:
                val = _eval_band(name, v - band, v + band, p, r)
            out[name + cls] = val
    out["DeltaT"] = out["tH"] - out["tL"]
    return out


# ---------------------------------------------------------------------------
# Trading stage.
# ---------------------------------------------------------------------------

def flow_laws(lam, bH, bL, noise=EQUAL_NOISE):
    """Pr(X = x | class) for buy-only orders q in {0, 1}, presence lam."""
    flows = sorted(set(list(noise.keys()) + [z + 1 for z in noise]))
    fH, fL = {}, {}
    for x in flows:
        n0 = noise.get(x, F(0))
        n1 = noise.get(x - 1, F(0))
        fH[x] = (1 - lam) * n0 + lam * ((1 - bH) * n0 + bH * n1)
        fL[x] = (1 - lam) * n0 + lam * ((1 - bL) * n0 + bL * n1)
    return flows, fH, fL


def set_partitions(items):
    items = list(items)
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    for part in set_partitions(rest):
        for i in range(len(part)):
            yield part[:i] + [[first] + part[i]] + part[i + 1:]
        yield [[first]] + part


def decision_options(B, c, rule, xi_grid):
    """Preparation probabilities of one cost type with gross profit B, cost c."""
    if B > c:
        return [F(1)]
    if B < c:
        return [F(0)]
    return [F(1)] if rule == "E" else list(xi_grid)


def solve(par, bH, bL, offpath="IC", inv_rule="Z", ch_rule="E",
          xi_grid=(F(0), F(1, 2), F(1)), noise=EQUAL_NOISE, band=None,
          objects=None):
    """Every equilibrium continuation at the order profile (bH, bL).

    Returns a list of dicts.  Each dict is one consistent price schedule at
    which (bH, bL) are investor best responses under inv_rule.
    offpath: 'IC' (belief 1 at an unused flow that only a purchase reaches),
    'passive' (prior), 'adverse' (belief 0), or a Fraction (that belief).
    inv_rule: 'Z' (zero at indifference), 'M' (any mixture at indifference),
    or 'none' (no optimality check: return every consistent schedule).
    objects: optional dict of auction objects that replaces the uniform
    second-price objects (used for the bargaining institution).
    """
    h, ell, p, r = par["h"], par["ell"], par["p"], par["r"]
    rho, cL, cH, k = par["rho"], par["cL"], par["cH"], par["k"]
    lam, pi = par["lam"], par["pi"]
    A = auction_objects(h, ell, p, r, band) if objects is None else objects
    t0, tH, tL, gH, gL = A["t0"], A["tH"], A["tL"], A["gH"], A["gL"]
    flows, fH, fL = flow_laws(lam, bH, bL, noise)
    w = {x: pi * fH[x] + (1 - pi) * fL[x] for x in flows}
    on = [x for x in flows if w[x] > 0]
    off = [x for x in flows if w[x] == 0]
    mu = {x: pi * fH[x] / w[x] for x in on}

    def Bof(m):
        return gL + m * (gH - gL)

    if offpath == "IC":
        v_off = F(1)
    elif offpath == "passive":
        v_off = pi
    elif offpath == "adverse":
        v_off = F(0)
    else:
        v_off = F(offpath)

    results = []
    for part in set_partitions(on):
        nu = []
        for blk in part:
            wb = sum(w[x] for x in blk)
            nu.append(sum(pi * fH[x] for x in blk) / wb)
        opts = []
        for b in range(len(part)):
            dl = decision_options(Bof(nu[b]), cL, ch_rule, xi_grid)
            dh = decision_options(Bof(nu[b]), cH, ch_rule, xi_grid)
            opts.append([(a, c) for a in dl for c in dh])
        for choice in product(*opts):
            ent, dLx, dHx, price, post = {}, {}, {}, {}, {}
            for b, blk in enumerate(part):
                dlb, dhb = choice[b]
                e = rho * dlb + (1 - rho) * dhb
                for x in blk:
                    ent[x], dLx[x], dHx[x] = e, dlb, dhb
                    price[x] = t0 + e * (tL - t0 + (tH - tL) * mu[x])
                    post[x] = nu[b]
            ok = True
            for b, blk in enumerate(part):
                if len(set(price[x] for x in blk)) != 1:
                    ok = False
            blockprices = [price[blk[0]] for blk in part]
            if len(set(blockprices)) != len(blockprices):
                ok = False
            if not ok:
                continue
            # Unused flows: price from the shared off-path belief.
            off_opts = []
            for x in off:
                dl = decision_options(Bof(v_off), cL, ch_rule, xi_grid)
                dh = decision_options(Bof(v_off), cH, ch_rule, xi_grid)
                off_opts.append([(a, c) for a in dl for c in dh])
            for ochoice in product(*off_opts):
                ent2, dL2, dH2 = dict(ent), dict(dLx), dict(dHx)
                price2, post2 = dict(price), dict(post)
                ok2 = True
                for j, x in enumerate(off):
                    dlb, dhb = ochoice[j]
                    e = rho * dlb + (1 - rho) * dhb
                    P = t0 + e * (tL - t0 + (tH - tL) * v_off)
                    for b, blk in enumerate(part):
                        if P == blockprices[b] and e != ent[blk[0]]:
                            ok2 = False
                    ent2[x], dL2[x], dH2[x] = e, dlb, dhb
                    price2[x], post2[x] = P, v_off
                if not ok2:
                    continue
                # Investor payoffs against the fixed schedule.
                U = {}
                for cls, tc in (("H", tH), ("L", tL)):
                    tot = F(0)
                    for z, nz in noise.items():
                        x = z + 1
                        tot += nz * (t0 + ent2[x] * (tc - t0) - price2[x])
                    U[cls] = tot - k
                eq = True
                for cls, b in (("H", bH), ("L", bL)):
                    if inv_rule == "none":
                        continue
                    if inv_rule == "Z":
                        best = F(1) if U[cls] > 0 else F(0)
                        if b != best:
                            eq = False
                    else:
                        if b > 0 and U[cls] < 0:
                            eq = False
                        if b < 1 and U[cls] > 0:
                            eq = False
                if not eq:
                    continue
                results.append(_outcomes(par, A, flows, on, fH, fL, w, ent2,
                                         dL2, dH2, price2, post2, U, bH, bL,
                                         part))
    return results


def _outcomes(par, A, flows, on, fH, fL, w, ent, dL, dH, price, post, U,
              bH, bL, part):
    pi, lam, rho, cL, cH = par["pi"], par["lam"], par["rho"], par["cL"], par["cH"]
    t0, tH, tL = A["t0"], A["tH"], A["tL"]
    eH = sum(fH[x] * ent[x] for x in on)
    eL = sum(fL[x] * ent[x] for x in on)
    E = pi * eH + (1 - pi) * eL
    OH = pi * eH * A["winH"]
    RT = sum(pi * fH[x] * (t0 + ent[x] * (tH - t0))
             + (1 - pi) * fL[x] * (t0 + ent[x] * (tL - t0)) for x in on)
    alloc = sum(pi * fH[x] * (A["alloc0"] + ent[x] * (A["allocH"] - A["alloc0"]))
                + (1 - pi) * fL[x] * (A["alloc0"] + ent[x] * (A["allocL"] - A["alloc0"]))
                for x in on)
    cost = sum(w[x] * (rho * dL[x] * cL + (1 - rho) * dH[x] * cH) for x in on)
    W = alloc - cost
    highcost = sum(w[x] * (1 - rho) * dH[x] for x in on)
    var = sum(w[x] * post[x] ** 2 for x in on) - pi ** 2
    profit = lam * (pi * bH * U["H"] + (1 - pi) * bL * U["L"])
    return {"bH": bH, "bL": bL, "E": E, "OH": OH, "RT": RT, "W": W,
            "Var": var, "profit": profit, "UH": U["H"], "UL": U["L"],
            "eH": eH, "eL": eL, "highcost": highcost,
            "price": {x: price[x] for x in flows if x in price},
            "post": {x: post[x] for x in flows if x in post},
            "entry": {x: ent[x] for x in flows if x in ent},
            "onpath": list(on),
            "blocks": [sorted(b) for b in part]}


def equilibria(par, grid, **kw):
    """All equilibria over a grid of order profiles (bH, bL)."""
    out = []
    for bH in grid:
        for bL in grid:
            out.extend(solve(par, bH, bL, **kw))
    return out


def deviation_max(par, pi_entry_mid, noise=EQUAL_NOISE, vgrid=None):
    """Largest high-class deviation payoff over off-path beliefs at flow 2.

    pi_entry_mid: entry at the two interior flows under no trade.
    Returns (max payoff, maximizing belief) over vgrid (rule E at ties).
    """
    h, ell, p, r = par["h"], par["ell"], par["p"], par["r"]
    rho, cL, cH, k, pi = par["rho"], par["cL"], par["cH"], par["k"], par["pi"]
    A = auction_objects(h, ell, p, r)
    gH, gL, D = A["gH"], A["gL"], A["DeltaT"]
    best, arg = None, None
    for v in vgrid:
        B = gL + v * (gH - gL)
        e = rho * (1 if B >= cL else 0) + (1 - rho) * (1 if B >= cH else 0)
        val = (noise[-1] * pi_entry_mid * D * (1 - pi)
               + noise[0] * pi_entry_mid * D * (1 - pi)
               + noise[1] * e * D * (1 - v) - k)
        if best is None or val > best:
            best, arg = val, v
    return best, arg
