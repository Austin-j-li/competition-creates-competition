"""Three-identity slot engine (informed, liquidity, one strategic third party), exact arithmetic.

Identity probabilities: informed lam, third party chi, liquidity 1 - lam - chi.
The third party has finitely many types; each type submits one pure order and has its own
terminal-value and own-payoff rules. The outside challenger sees the price (here: the flow,
since the three prices are checked to be distinct) and conditions on "not in the slot".
"""
from fractions import Fraction as F
from common import RHO, CH, K, PI, Bf, entry_C1, post, dec

XS = (-1, 0, 1)


def engine(o, lam, chi, eta, s, t, types, ent_override=None, chall_in_third=True):
    """
    eta: liquidity order law {-1: ., 0: ., 1: .}.
    s, t: informed H purchase and L sale probabilities.
    types: list of dicts with keys
        name, prob (sums to 1 over types), q (order in XS),
        V(j, e) -> E[V_T | class j, entry e, type],
        own_entry: None (entry follows the outside rule) or a number (the type's own entry),
        A(e) -> the type's own non-trade payoff at entry e (already averaged over the class).
    Returns masses, posteriors, entry, prices, and payoffs.
    """
    lq = 1 - lam - chi
    aH0 = {1: lam * s + lq * eta[1], -1: lq * eta[-1], 0: lam * (1 - s) + lq * eta[0]}
    aL0 = {1: lq * eta[1], -1: lam * t + lq * eta[-1], 0: lam * (1 - t) + lq * eta[0]}
    third = {x: chi * sum(ty["prob"] for ty in types if ty["q"] == x) for x in XS}
    aH = {x: aH0[x] + third[x] for x in XS}
    aL = {x: aL0[x] + third[x] for x in XS}
    mu_mm = {x: post(aH[x], aL[x]) for x in XS}
    # the outside challenger conditions on "not in the slot" only when the third party is the challenger itself
    mu_out = {x: post(aH0[x], aL0[x]) for x in XS} if chall_in_third else dict(mu_mm)
    e_out = {x: entry_C1(o, mu_out[x]) for x in XS}
    if ent_override:
        e_out.update(ent_override)

    def e_type(ty, x):
        return e_out[x] if ty["own_entry"] is None else ty["own_entry"]

    price, val_third = {}, {}
    for x in XS:
        num = PI * aH0[x] * (o["t0"] + e_out[x] * o["wH"]) + (1 - PI) * aL0[x] * (o["t0"] + e_out[x] * o["wL"])
        for ty in types:
            if ty["q"] == x:
                num += chi * ty["prob"] * (PI * ty["V"]("H", e_type(ty, x)) + (1 - PI) * ty["V"]("L", e_type(ty, x)))
        den = PI * aH[x] + (1 - PI) * aL[x]
        price[x] = num / den if den > 0 else None
    pay = {j: {q: (q * (o["t0"] + e_out[q] * o["w" + j] - price[q]) - K * abs(q)) if price[q] is not None else None
               for q in XS} for j in "HL"}
    pay3 = {}
    for ty in types:
        pay3[ty["name"]] = {}
        for q in XS:
            if price[q] is None:
                pay3[ty["name"]][q] = None
                continue
            e = e_type(ty, q)
            vbar = PI * ty["V"]("H", e) + (1 - PI) * ty["V"]("L", e)
            pay3[ty["name"]][q] = q * (vbar - price[q]) - K * abs(q) + ty["A"](e)
    prob = {x: PI * aH[x] + (1 - PI) * aL[x] for x in XS}
    # entry and ownership: outside challenger uses e_out; in-slot types use their own entry
    E = sum(PI * aH0[x] * e_out[x] + (1 - PI) * aL0[x] * e_out[x] for x in XS)
    OH = sum(PI * aH0[x] * e_out[x] for x in XS)
    for ty in types:
        e = e_type(ty, ty["q"])
        E += chi * ty["prob"] * e
        OH += PI * chi * ty["prob"] * e
    T = sum(prob[x] * price[x] for x in XS if price[x] is not None)
    return dict(aH=aH, aL=aL, aH0=aH0, aL0=aL0, mu_mm=mu_mm, mu_out=mu_out, e_out=e_out, price=price,
                pay=pay, pay3=pay3, prob=prob, E=E, OH=OH, T=T)


def argmax_set(d):
    vals = {q: v for q, v in d.items() if v is not None}
    mx = max(vals.values())
    return {q for q, v in vals.items() if v == mx}, mx


def informed_ok(ev, s, t, inv="IM"):
    okH = okL = True
    argH, _ = argmax_set(ev["pay"]["H"])
    argL, _ = argmax_set(ev["pay"]["L"])
    suppH = {1} if s == 1 else ({0} if s == 0 else {0, 1})
    suppL = {-1} if t == 1 else ({0} if t == 0 else {0, -1})
    okH = suppH <= argH and not (inv == "I0" and 0 in argH and suppH != {0})
    okL = suppL <= argL and not (inv == "I0" and 0 in argL and suppL != {0})
    return okH, okL


def third_ok(ev, types):
    out = {}
    for ty in types:
        arg, mx = argmax_set(ev["pay3"][ty["name"]])
        out[ty["name"]] = ty["q"] in arg
    return out


def chall_ok(o, ev, rule="C1"):
    for x in XS:
        B = Bf(o, ev["mu_out"][x])
        e = ev["e_out"][x]
        if B > CH and e != 1:
            return False
        if B < CH and e != RHO:
            return False
        if B == CH and rule == "C1" and e != 1:
            return False
    return True


def prices_distinct(ev):
    ps = [ev["price"][x] for x in XS if ev["price"][x] is not None]
    return len(ps) == len(set(ps))
