# Second independent calculation: fifty digit table values from sign enumeration.
# Prints values only.
from fractions import Fraction
from mpmath import mp, mpf, exp

mp.dps = 50


def auction_mp(rs):
    r = mpf(rs)
    p = mpf("0.5")
    ell = mpf(1)
    h = mpf(10)
    t0 = p * (1 - p / r)
    tH = r / 2 + p * p / (2 * r)
    tL = ell - (ell * ell - p * p) / (2 * r)
    gH = h - r / 2 - p * p / (2 * r)
    gL = (ell * ell - p * p) / (2 * r)
    delta = tH - tL
    wH = tH - t0
    wL = tL - t0
    return t0, gH, gL, delta, wH, wL


def entry_mp(gL, gH, mu):
    b = gL + mu * (gH - gL)
    if b >= 6:
        return mpf(1)
    return mpf("0.25")


a = exp(mpf(-1) / 2)
u = 1 / (1 + a)
v = a / (1 + a)
signs = [1, -1]


def sign_prob(s, order):
    if order == 1:
        if s == 1:
            return u
        return v
    if s == 1:
        return v
    return u


def dl_S_mp(rs, beta1, beta_plus, beta_minus, ks):
    t0, gH, gL, delta, wH, wL = auction_mp(rs)
    k = mpf(ks)
    beta2 = {1: mpf(beta_plus), -1: mpf(beta_minus)}
    b1 = mpf(beta1)
    p1H = {}
    p1L = {}
    for s in signs:
        p1H[s] = b1 * sign_prob(s, 1) + (1 - b1) * sign_prob(s, 0)
        p1L[s] = sign_prob(s, 0)
    mu1 = {}
    for s in signs:
        mu1[s] = p1H[s] / (p1H[s] + p1L[s])
    p2H = {}
    p2L = {}
    for s1 in signs:
        for s2 in signs:
            b = beta2[s1]
            p2H[(s1, s2)] = b * sign_prob(s2, 1) + (1 - b) * sign_prob(s2, 0)
            p2L[(s1, s2)] = sign_prob(s2, 0)
    mu2 = {}
    e2 = {}
    P2 = {}
    for s1 in signs:
        for s2 in signs:
            num = p1H[s1] * p2H[(s1, s2)]
            den = num + p1L[s1] * p2L[(s1, s2)]
            m = num / den
            mu2[(s1, s2)] = m
            e = entry_mp(gL, gH, m)
            e2[(s1, s2)] = e
            P2[(s1, s2)] = t0 + e * (wL + delta * m)
    EVH = {}
    EVL = {}
    P1 = {}
    for s1 in signs:
        evH = mpf(0)
        evL = mpf(0)
        for s2 in signs:
            evH = evH + p2H[(s1, s2)] * (t0 + e2[(s1, s2)] * wH)
            evL = evL + p2L[(s1, s2)] * (t0 + e2[(s1, s2)] * wL)
        EVH[s1] = evH
        EVL[s1] = evL
        P1[s1] = mu1[s1] * evH + (1 - mu1[s1]) * evL
    gross2H = {}
    for s1 in signs:
        g = mpf(0)
        for s2 in signs:
            g = g + sign_prob(s2, 1) * (t0 + e2[(s1, s2)] * wH - P2[(s1, s2)])
        gross2H[s1] = g
    gross1H = mpf(0)
    for s1 in signs:
        gross1H = gross1H + sign_prob(s1, 1) * (EVH[s1] - P1[s1])
    ent = mpf(0)
    own = mpf(0)
    for s1 in signs:
        for s2 in signs:
            pH = mpf("0.5") * p1H[s1] * p2H[(s1, s2)]
            pL = mpf("0.5") * p1L[s1] * p2L[(s1, s2)]
            ent = ent + (pH + pL) * e2[(s1, s2)]
            own = own + pH * e2[(s1, s2)]
    # Total profit given H as sum of unit profits under candidate orders.
    # First unit profit mean given H and candidate first order mix.
    # For pure candidates beta1 is 0 or 1. Use order means directly.
    # Expected purchases given H.
    exp_second = mpf(0)
    for s1 in signs:
        # P(s1|H) under candidate first mix.
        exp_second = exp_second + p1H[s1] * beta2[s1]
    expN = b1 + exp_second
    # Profit: first unit earns gross1H-k if bought. Second unit earns mean over s1.
    # Second gross mean given H: sum_s1 P(s1|H, first order as candidate?) Careful:
    # p1H already mixes first order. Second buyer profit conditional on s1 is gross2H-k.
    # Mean second profit = sum_s1 p1H[s1] * beta2[s1] * (gross2H[s1]-k) ??? No:
    # gross2H is mean over s2 given buy. If second order mixes, profit scales.
    # For pure beta2, this holds. First profit needs care when beta1 mixes.
    # All cases here use pure beta1, beta2. Then p1H is law under that pure order.
    first_prof = mpf(0)
    if b1 == 1:
        first_prof = gross1H - k
    second_prof = mpf(0)
    for s1 in signs:
        second_prof = second_prof + p1H[s1] * beta2[s1] * (gross2H[s1] - k)
    total_prof = first_prof + second_prof
    total_cost = k * expN
    return {"mu1": mu1, "mu2": mu2, "e2": e2, "P1": P1, "P2": P2,
            "gross1H": gross1H, "gross2H": gross2H, "entry": ent, "own": own,
            "expN": expN, "cost": total_cost, "prof": total_prof}


cases = [
    ("no trade r=1.2", "1.2", 0, 0, 0, "0.02"),
    ("full r=1.7", "1.7", 1, 1, 1, "0.02"),
    ("full r=3 k=0.02", "3", 1, 1, 1, "0.02"),
    ("full r=3.6", "3.6", 1, 1, 1, "0.02"),
    ("full r=3 k=0.09", "3", 1, 1, 1, "0.09"),
    ("timing r=3 k=0.11", "3", 1, 1, 0, "0.11"),
    ("full r=3 k=0.11 forced", "3", 1, 1, 1, "0.11"),
]
for (label, rs, b1, bp, bm, ks) in cases:
    res = dl_S_mp(rs, b1, bp, bm, ks)
    print(label, "r=", rs, "k=", ks)
    print("  entry =", mp.nstr(res["entry"], 20))
    print("  ownH =", mp.nstr(res["own"], 20))
    print("  costH =", mp.nstr(res["cost"], 20))
    print("  profH sum =", mp.nstr(res["prof"], 20))
    print("  gross1H =", mp.nstr(res["gross1H"], 20))
    print("  gross2H+ =", mp.nstr(res["gross2H"][1], 20),
          " gross2H- =", mp.nstr(res["gross2H"][-1], 20))
    print("  e2:", {kk: mp.nstr(vv, 6) for kk, vv in res["e2"].items()})
    print("  P1+ =", mp.nstr(res["P1"][1], 20), " P1- =", mp.nstr(res["P1"][-1], 20))
print()

print("Three-point Design S profit formula 13 at T=2, r=3")
RHO = Fraction(1, 4)
Delta = Fraction(2, 3)
wH = Fraction(9, 8)
s = Fraction(2, 3)
pi = Fraction(1, 2)
for k in [Fraction(1, 50), Fraction(1, 10)]:
    total = Fraction(0)
    for t in [1, 2]:
        inner = s * (1 - pi) * (RHO * Delta + (1 - RHO) * wH * (1 - s ** (2 - t))) - k
        total = total + (s ** (t - 1)) * inner
        print("  t=", t, "term inner =", str(inner), "~", format(float(inner), ".12f"))
    print("  k=", str(k), "Pi formula13 =", str(total), "~", format(float(total), ".12f"))
print()
print("Low belief gain B(m2) at b=2")
m2v = a * a / (1 + a * a)
for rs in ["1.2", "1.7", "3", "3.6"]:
    t0x, gHx, gLx, deltax, wHx, wLx = auction_mp(rs)
    Bm2 = gLx + m2v * (gHx - gLx)
    Bv = gLx + v * (gHx - gLx)
    print("  r =", rs, "B(m2) =", mp.nstr(Bm2, 20), "B(v) =", mp.nstr(Bv, 20),
          "gL =", mp.nstr(gLx, 20))
print("End of second calculation.")
