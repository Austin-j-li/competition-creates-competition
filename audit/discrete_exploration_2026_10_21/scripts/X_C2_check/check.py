# Independent check calculations for two-round claims.
# Exact rational arithmetic where inputs are rational.
# Fifty digit arithmetic for the exponential case.
# This file prints values only.
from fractions import Fraction
from mpmath import mp, mpf, exp

mp.dps = 50

H_V = Fraction(10)
ELL = Fraction(1)
P_RES = Fraction(1, 2)
RHO = Fraction(1, 4)
C_H = Fraction(6)


def auction(r):
    t0 = P_RES * (1 - P_RES / r)
    tH = r / 2 + P_RES * P_RES / (2 * r)
    tL = ELL - (ELL * ELL - P_RES * P_RES) / (2 * r)
    gH = H_V - r / 2 - P_RES * P_RES / (2 * r)
    gL = (ELL * ELL - P_RES * P_RES) / (2 * r)
    delta = tH - tL
    wH = tH - t0
    wL = tL - t0
    return {"t0": t0, "tH": tH, "tL": tL, "gH": gH, "gL": gL,
            "Delta": delta, "wH": wH, "wL": wL}


def gain(obj, mu):
    return obj["gL"] + mu * (obj["gH"] - obj["gL"])


def entry(obj, mu):
    if gain(obj, mu) >= C_H:
        return Fraction(1)
    return RHO


def price_final(obj, mu):
    e = entry(obj, mu)
    return obj["t0"] + e * (obj["wL"] + obj["Delta"] * mu)


def show_frac(label, value):
    print(label + " = " + str(value) + "  ~ " + format(float(value), ".12f"))


print("=== Auction objects ===")
for r in [Fraction(6, 5), Fraction(17, 10), Fraction(3), Fraction(18, 5)]:
    o = auction(r)
    print("r =", str(r), "~", format(float(r), ".4f"))
    for key in ["t0", "tH", "tL", "gH", "gL", "Delta", "wH", "wL"]:
        show_frac("  " + key, o[key])
    show_frac("  B(1/2)", gain(o, Fraction(1, 2)))
    show_frac("  W = wH - rho*wL", o["wH"] - RHO * o["wL"])
    show_frac("  D = rho*Delta", RHO * o["Delta"])
print()

# --- Discrete-Laplace sign model, Design S, brute force from Bayes rule ---
# Sign + means flow at least 1. Sign - means flow at most 0.
# Under order 1: P(+) = u, P(-) = v. Under order 0: P(+) = v, P(-) = u.

def dl_uv(a):
    u = 1 / (1 + a)
    v = a / (1 + a)
    return u, v


def dl_sign_prob(sign, order, u, v):
    if order == 1:
        if sign == 1:
            return u
        return v
    if sign == 1:
        return v
    return u


def dl_S_eval(r, a, beta1, beta_plus, beta_minus, k):
    o = auction(r)
    u, v = dl_uv(a)
    beta2 = {1: beta_plus, -1: beta_minus}
    signs = [1, -1]
    # First sign law under candidate. Class L order is 0.
    p_s1_H = {}
    p_s1_L = {}
    for s in signs:
        p_s1_H[s] = beta1 * dl_sign_prob(s, 1, u, v) + (1 - beta1) * dl_sign_prob(s, 0, u, v)
        p_s1_L[s] = dl_sign_prob(s, 0, u, v)
    mu1 = {}
    for s in signs:
        num = Fraction(1, 2) * p_s1_H[s]
        den = num + Fraction(1, 2) * p_s1_L[s]
        mu1[s] = num / den
    # Second sign law under candidate.
    p_s2_H = {}
    p_s2_L = {}
    for s1 in signs:
        for s2 in signs:
            b = beta2[s1]
            p_s2_H[(s1, s2)] = b * dl_sign_prob(s2, 1, u, v) + (1 - b) * dl_sign_prob(s2, 0, u, v)
            p_s2_L[(s1, s2)] = dl_sign_prob(s2, 0, u, v)
    mu2 = {}
    e2 = {}
    P2 = {}
    for s1 in signs:
        for s2 in signs:
            num = Fraction(1, 2) * p_s1_H[s1] * p_s2_H[(s1, s2)]
            den = num + Fraction(1, 2) * p_s1_L[s1] * p_s2_L[(s1, s2)]
            m = num / den
            mu2[(s1, s2)] = m
            e2[(s1, s2)] = entry(o, m)
            P2[(s1, s2)] = price_final(o, m)
    # First price from tower rule. Value mean given class and signs is t0+e2*w.
    P1 = {}
    EV_H_s1 = {}
    EV_L_s1 = {}
    for s1 in signs:
        evH = Fraction(0)
        evL = Fraction(0)
        for s2 in signs:
            evH = evH + p_s2_H[(s1, s2)] * (o["t0"] + e2[(s1, s2)] * o["wH"])
            evL = evL + p_s2_L[(s1, s2)] * (o["t0"] + e2[(s1, s2)] * o["wL"])
        EV_H_s1[s1] = evH
        EV_L_s1[s1] = evL
        P1[s1] = mu1[s1] * evH + (1 - mu1[s1]) * evL
    # Second round purchase profits. Buyer uses order 1 sign law.
    gross2H = {}
    gross2L = {}
    for s1 in signs:
        gH = Fraction(0)
        gL = Fraction(0)
        for s2 in signs:
            pr = dl_sign_prob(s2, 1, u, v)
            gH = gH + pr * (o["t0"] + e2[(s1, s2)] * o["wH"] - P2[(s1, s2)])
            gL = gL + pr * (o["t0"] + e2[(s1, s2)] * o["wL"] - P2[(s1, s2)])
        gross2H[s1] = gH
        gross2L[s1] = gL
    # First round purchase profits. Future law stays at candidate.
    gross1H = Fraction(0)
    gross1L = Fraction(0)
    for s1 in signs:
        pr = dl_sign_prob(s1, 1, u, v)
        gross1H = gross1H + pr * (EV_H_s1[s1] - P1[s1])
        gross1L = gross1L + pr * (EV_L_s1[s1] - P1[s1])
    # Entry and ownership under candidate.
    tot_entry = Fraction(0)
    own_H = Fraction(0)
    for s1 in signs:
        for s2 in signs:
            pH = Fraction(1, 2) * p_s1_H[s1] * p_s2_H[(s1, s2)]
            pL = Fraction(1, 2) * p_s1_L[s1] * p_s2_L[(s1, s2)]
            tot_entry = tot_entry + (pH + pL) * e2[(s1, s2)]
            own_H = own_H + pH * e2[(s1, s2)]
    out = {"o": o, "u": u, "v": v, "mu1": mu1, "mu2": mu2, "e2": e2, "P1": P1, "P2": P2,
           "gross2H": gross2H, "gross2L": gross2L, "gross1H": gross1H, "gross1L": gross1L,
           "entry": tot_entry, "ownH": own_H}
    return out


# --- Discrete-Laplace, Design R, brute force over sign plans ---
# Candidate: first buy prob sigH, sigL. Second buy prob pol[(cls,n,s1)].
# cls is H or L. n is first order 0 or 1. s1 is first sign.

def dl_R_eval(r, a, sigH, sigL, pol, k):
    o = auction(r)
    u, v = dl_uv(a)
    signs = [1, -1]
    sig = {"H": sigH, "L": sigL}
    prior = {"H": Fraction(1, 2), "L": Fraction(1, 2)}
    w = {"H": o["wH"], "L": o["wL"]}
    # Joint law of class, inventory, signs under candidate.
    joint = {}
    for cls in ["H", "L"]:
        for n in [0, 1]:
            pn = sig[cls] if n == 1 else (1 - sig[cls])
            for s1 in signs:
                p1 = dl_sign_prob(s1, n, u, v)
                b = pol[(cls, n, s1)]
                for s2 in signs:
                    p2 = b * dl_sign_prob(s2, 1, u, v) + (1 - b) * dl_sign_prob(s2, 0, u, v)
                    joint[(cls, n, s1, s2)] = prior[cls] * pn * p1 * p2
    mu2 = {}
    e2 = {}
    P2 = {}
    for s1 in signs:
        for s2 in signs:
            num = Fraction(0)
            den = Fraction(0)
            for cls in ["H", "L"]:
                for n in [0, 1]:
                    den = den + joint[(cls, n, s1, s2)]
                    if cls == "H":
                        num = num + joint[(cls, n, s1, s2)]
            m = num / den
            mu2[(s1, s2)] = m
            e2[(s1, s2)] = entry(o, m)
            P2[(s1, s2)] = price_final(o, m)
    P1 = {}
    for s1 in signs:
        num = Fraction(0)
        den = Fraction(0)
        acc = Fraction(0)
        for cls in ["H", "L"]:
            for n in [0, 1]:
                for s2 in signs:
                    pj = joint[(cls, n, s1, s2)]
                    den = den + pj
                    acc = acc + pj * (o["t0"] + e2[(s1, s2)] * w[cls])
        P1[s1] = acc / den
    # Deviation values. Plan is choice of second order for each first sign.
    # Value mean given class and signs is t0+e2*w. Prices stay at candidate.
    def plan_value(cls, n, q2plus, q2minus):
        q2 = {1: q2plus, -1: q2minus}
        total = Fraction(0)
        for s1 in signs:
            p1 = dl_sign_prob(s1, n, u, v)
            q = q2[s1]
            inner = Fraction(0)
            for s2 in signs:
                p2 = dl_sign_prob(s2, q, u, v)
                val = o["t0"] + e2[(s1, s2)] * w[cls]
                inner = inner + p2 * ((n + q) * val - q * P2[(s1, s2)])
            inner = inner - n * P1[s1] - k * n
            # second order cost: subtract k*q outside s2 mean
            inner = inner - k * q
            total = total + p1 * inner
        # Subtract value of doing nothing baseline shift: values include t0 terms.
        # Doing nothing gives 0 by construction below via recentering.
        return total
    # Recenter: plan with n=0,q=0 must give 0. It gives 0 already since n+q=0.
    Ubest = {}
    Uall = {}
    for cls in ["H", "L"]:
        for n in [0, 1]:
            best = None
            store = {}
            for qp in [0, 1]:
                for qm in [0, 1]:
                    val = plan_value(cls, n, qp, qm)
                    store[(qp, qm)] = val
                    if best is None or val > best:
                        best = val
            Ubest[(cls, n)] = best
            Uall[(cls, n)] = store
    # Second increments given first sign and inventory.
    gamma = {}
    for cls in ["H", "L"]:
        for n in [0, 1]:
            for s1 in signs:
                cont1 = Fraction(0)
                cont0 = Fraction(0)
                for s2 in signs:
                    val = o["t0"] + e2[(s1, s2)] * w[cls]
                    cont1 = cont1 + dl_sign_prob(s2, 1, u, v) * ((n + 1) * val - P2[(s1, s2)])
                    cont0 = cont0 + dl_sign_prob(s2, 0, u, v) * (n * val)
                gamma[(cls, n, s1)] = (cont1 - k) - cont0
    # Entry and ownership under candidate.
    tot_entry = Fraction(0)
    own_H = Fraction(0)
    expN_H = Fraction(0)
    for key in joint:
        cls, n, s1, s2 = key
        tot_entry = tot_entry + joint[key] * e2[(s1, s2)]
        if cls == "H":
            own_H = own_H + joint[key] * e2[(s1, s2)]
    # Expected purchases given H: first mean plus second mean.
    # Second mean needs policy mean over inventory and first sign.
    return {"o": o, "u": u, "v": v, "mu2": mu2, "e2": e2, "P1": P1, "P2": P2,
            "Ubest": Ubest, "Uall": Uall, "gamma": gamma,
            "entry": tot_entry, "ownH": own_H}


print("=== Discrete-Laplace, a=3/5, Design S full purchase, brute force ===")
A35 = Fraction(3, 5)
for (r, k) in [(Fraction(3), Fraction(9, 100)), (Fraction(17, 10), Fraction(1, 50)),
               (Fraction(3), Fraction(11, 100))]:
    res = dl_S_eval(r, A35, Fraction(1), Fraction(1), Fraction(1), k)
    o = res["o"]
    print("r =", str(r), "k =", str(k))
    show_frac("  u", res["u"])
    show_frac("  v", res["v"])
    show_frac("  mu1(+)", res["mu1"][1])
    show_frac("  mu1(-)", res["mu1"][-1])
    show_frac("  mu2(++)", res["mu2"][(1, 1)])
    show_frac("  mu2(+-)", res["mu2"][(1, -1)])
    show_frac("  mu2(--)", res["mu2"][(-1, -1)])
    show_frac("  B(1/2)", gain(o, Fraction(1, 2)))
    show_frac("  B(u)", gain(o, res["u"]))
    show_frac("  B(M2)", gain(o, res["mu2"][(1, 1)]))
    show_frac("  Cminus brute gross2H after -", res["gross2H"][-1])
    show_frac("  Cplus brute gross2H after +", res["gross2H"][1])
    show_frac("  C1 brute gross1H", res["gross1H"])
    show_frac("  gross1L", res["gross1L"])
    show_frac("  gross2L after +", res["gross2L"][1])
    show_frac("  gross2L after -", res["gross2L"][-1])
    show_frac("  Cminus - k", res["gross2H"][-1] - k)
    show_frac("  Cplus - k", res["gross2H"][1] - k)
    show_frac("  C1 - k", res["gross1H"] - k)
    show_frac("  entry", res["entry"])
    show_frac("  ownH", res["ownH"])
    show_frac("  P1(+)", res["P1"][1])
    show_frac("  P1(-)", res["P1"][-1])
    show_frac("  P2(++)", res["P2"][(1, 1)])
    show_frac("  P2(+-)", res["P2"][(1, -1)])
    show_frac("  P2(--)", res["P2"][(-1, -1)])
    # Closed forms from memo equations 39 to 41 for comparison.
    u = res["u"]
    v = res["v"]
    M2 = res["mu2"][(1, 1)]
    Dv = RHO * o["Delta"]
    Cminus_f = Dv * (u / 2 + v * M2)
    Cplus_f = o["Delta"] * (u * (1 - M2) + v * RHO / 2)
    C1_f = u * v * (2 * Dv + (1 - RHO) * (o["wH"] * u - o["wL"] * v))
    show_frac("  Cminus formula", Cminus_f)
    show_frac("  Cplus formula", Cplus_f)
    show_frac("  C1 formula", C1_f)
    show_frac("  diff Cminus brute-formula", res["gross2H"][-1] - Cminus_f)
    show_frac("  diff Cplus brute-formula", res["gross2H"][1] - Cplus_f)
    show_frac("  diff C1 brute-formula", res["gross1H"] - C1_f)
    print("  e2:", {kk: str(vv) for kk, vv in res["e2"].items()})
print()

print("=== Discrete-Laplace, a=3/5, Design S no trade ===")
for (r, k) in [(Fraction(3), Fraction(9, 100)), (Fraction(17, 10), Fraction(1, 50))]:
    res = dl_S_eval(r, A35, Fraction(0), Fraction(0), Fraction(0), k)
    o = res["o"]
    print("r =", str(r), "k =", str(k))
    show_frac("  mu2 all", res["mu2"][(1, 1)])
    show_frac("  gross single buy H (gross1H)", res["gross1H"])
    show_frac("  rho*Delta/2", RHO * o["Delta"] / 2)
    show_frac("  gross1H - k", res["gross1H"] - k)
    show_frac("  gross2H after +", res["gross2H"][1])
    show_frac("  entry", res["entry"])
print()

print("=== Discrete-Laplace timing candidate, a=3/5, Design S ===")
# Candidate: buy first, buy second only after good first sign.
for (r, k) in [(Fraction(3), Fraction(11, 100))]:
    res = dl_S_eval(r, A35, Fraction(1), Fraction(1), Fraction(0), k)
    o = res["o"]
    print("r =", str(r), "k =", str(k), "beta_plus=1 beta_minus=0")
    show_frac("  mu2(-,+) [should stay v]", res["mu2"][(-1, 1)])
    show_frac("  mu2(-,-)", res["mu2"][(-1, -1)])
    show_frac("  v", res["v"])
    show_frac("  gross2H after - (deviation buy)", res["gross2H"][-1])
    show_frac("  D*u", RHO * o["Delta"] * res["u"])
    show_frac("  gross2H after - minus k", res["gross2H"][-1] - k)
    show_frac("  gross2H after + minus k", res["gross2H"][1] - k)
    show_frac("  gross1H minus k", res["gross1H"] - k)
    show_frac("  entry", res["entry"])
print()

print("=== Discrete-Laplace, a=3/5, Design R full purchase ===")
def dl_full_pol():
    pol = {}
    for cls in ["H", "L"]:
        for n in [0, 1]:
            for s1 in [1, -1]:
                if cls == "H":
                    pol[(cls, n, s1)] = Fraction(1)
                else:
                    pol[(cls, n, s1)] = Fraction(0)
    return pol


def dl_notrade_pol():
    pol = {}
    for cls in ["H", "L"]:
        for n in [0, 1]:
            for s1 in [1, -1]:
                pol[(cls, n, s1)] = Fraction(0)
    return pol


for (r, k) in [(Fraction(3), Fraction(9, 100)), (Fraction(17, 10), Fraction(1, 50))]:
    resR = dl_R_eval(r, A35, Fraction(1), Fraction(0), dl_full_pol(), k)
    resS = dl_S_eval(r, A35, Fraction(1), Fraction(1), Fraction(1), k)
    print("r =", str(r), "k =", str(k), "candidate full")
    show_frac("  Ubest H n=1", resR["Ubest"][("H", 1)])
    show_frac("  Ubest H n=0", resR["Ubest"][("H", 0)])
    show_frac("  Ubest H diff (1-0)", resR["Ubest"][("H", 1)] - resR["Ubest"][("H", 0)])
    show_frac("  Ubest L n=1", resR["Ubest"][("L", 1)])
    show_frac("  Ubest L n=0", resR["Ubest"][("L", 0)])
    for cls in ["H", "L"]:
        for n in [0, 1]:
            for s1 in [1, -1]:
                print("  gamma", cls, "n=", n, "s1=", s1, "=", str(resR["gamma"][(cls, n, s1)]),
                      "~", format(float(resR["gamma"][(cls, n, s1)]), ".12f"))
    # Memo formula 45 value.
    C1 = resS["gross1H"]
    Cp = resS["gross2H"][1]
    Cm = resS["gross2H"][-1]
    u = resS["u"]
    v = resS["v"]
    f45 = (C1 - k) + (u - v) * (Cp - Cm)
    show_frac("  memo formula 45 from S gross values", f45)
    show_frac("  brute diff minus formula 45",
              (resR["Ubest"][("H", 1)] - resR["Ubest"][("H", 0)]) - f45)
    # Retained addition after good sign.
    o = resR["o"]
    show_frac("  wH*(u-v)*(1-rho)", o["wH"] * (u - v) * (1 - RHO))
    show_frac("  gammaH n=1 plus minus gammaH n=0 plus",
              resR["gamma"][("H", 1, 1)] - resR["gamma"][("H", 0, 1)])
    show_frac("  gammaH n=1 minus - gammaH n=0 minus",
              resR["gamma"][("H", 1, -1)] - resR["gamma"][("H", 0, -1)])
    show_frac("  entry R", resR["entry"])
    print("  Uall H n=1:", {kk: str(vv) for kk, vv in resR["Uall"][("H", 1)].items()})
    print("  Uall H n=0:", {kk: str(vv) for kk, vv in resR["Uall"][("H", 0)].items()})
    print("  Uall L n=1:", {kk: str(vv) for kk, vv in resR["Uall"][("L", 1)].items()})
print()

print("=== Discrete-Laplace, a=3/5, Design R no trade ===")
for (r, k) in [(Fraction(3), Fraction(9, 100)), (Fraction(17, 10), Fraction(1, 50))]:
    resR = dl_R_eval(r, A35, Fraction(0), Fraction(0), dl_notrade_pol(), k)
    print("r =", str(r), "k =", str(k))
    show_frac("  Ubest H n=1", resR["Ubest"][("H", 1)])
    show_frac("  Ubest H n=0", resR["Ubest"][("H", 0)])
    show_frac("  Ubest L n=1", resR["Ubest"][("L", 1)])
    for cls in ["H", "L"]:
        for n in [0, 1]:
            for s1 in [1, -1]:
                print("  gamma", cls, "n=", n, "s1=", s1, "~",
                      format(float(resR["gamma"][(cls, n, s1)]), ".12f"))
print()

print("=== Design R timing candidate, a=3/5, r=3, k=11/100 ===")
pol_time = {}
for cls in ["H", "L"]:
    for n in [0, 1]:
        for s1 in [1, -1]:
            if cls == "H" and s1 == 1:
                pol_time[(cls, n, s1)] = Fraction(1)
            else:
                pol_time[(cls, n, s1)] = Fraction(0)
resRT = dl_R_eval(Fraction(3), A35, Fraction(1), Fraction(0), pol_time, Fraction(11, 100))
resST = dl_S_eval(Fraction(3), A35, Fraction(1), Fraction(1), Fraction(0), Fraction(11, 100))
show_frac("  Ubest H n=1", resRT["Ubest"][("H", 1)])
show_frac("  Ubest H n=0", resRT["Ubest"][("H", 0)])
show_frac("  diff", resRT["Ubest"][("H", 1)] - resRT["Ubest"][("H", 0)])
show_frac("  Ubest L n=1", resRT["Ubest"][("L", 1)])
for cls in ["H", "L"]:
    for n in [0, 1]:
        for s1 in [1, -1]:
            print("  gamma", cls, "n=", n, "s1=", s1, "~",
                  format(float(resRT["gamma"][(cls, n, s1)]), ".12f"))
# Memo formula 48 needs C1 and Cplus from timing candidate.
C1t = resST["gross1H"]
Cpt = resST["gross2H"][1]
ut = resST["u"]
vt = resST["v"]
f48 = (C1t - Fraction(11, 100)) + (ut - vt) * (Cpt - Fraction(11, 100))
show_frac("  memo formula 48 from S gross values", f48)
show_frac("  brute diff minus formula 48",
          (resRT["Ubest"][("H", 1)] - resRT["Ubest"][("H", 0)]) - f48)
print()

print("=== One-round gross formula check, a=3/5 ===")
# One round, prior 1/2, candidate buy prob beta. Entry stays at rho if B(u)<6.
def one_round_gross(r, a, beta):
    o = auction(r)
    u, v = dl_uv(a)
    # Posteriors after + and - under candidate beta.
    p_plus_H = beta * u + (1 - beta) * v
    p_plus_L = v
    p_minus_H = beta * v + (1 - beta) * u
    p_minus_L = u
    mu_plus = p_plus_H / (p_plus_H + p_plus_L)
    mu_minus = p_minus_H / (p_minus_H + p_minus_L)
    e_plus = entry(o, mu_plus)
    e_minus = entry(o, mu_minus)
    # Buyer sign law is order 1.
    gross = o["Delta"] * (u * e_plus * (1 - mu_plus) + v * e_minus * (1 - mu_minus))
    return gross, mu_plus, mu_minus, e_plus, e_minus


for r in [Fraction(3), Fraction(17, 10)]:
    o = auction(r)
    Dv = RHO * o["Delta"]
    print("r =", str(r))
    for beta in [Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(1)]:
        g, mup, mum, ep, em = one_round_gross(r, A35, beta)
        a = A35
        f47 = (2 * a * Dv) / ((2 * a + beta * (1 - a)) * (2 - beta * (1 - a)))
        print("  beta =", str(beta), "mu+ =", str(mup), "mu- =", str(mum),
              "e+ =", str(ep), "e- =", str(em))
        show_frac("    gross brute", g)
        show_frac("    formula 47", f47)
        show_frac("    diff", g - f47)
        show_frac("    D/2 minus gross", Dv / 2 - g)
print()

print("=== Interval bounds for a in [3/5, 61/100] ===")
# Component bounds. u falls in a. v rises in a. M2 falls in a. 1-M2 rises in a.
# uv = a/(1+a)^2 rises for a<1.
A_LO = Fraction(3, 5)
A_HI = Fraction(61, 100)
u_min = 1 / (1 + A_HI)
u_max = 1 / (1 + A_LO)
v_min = A_LO / (1 + A_LO)
v_max = A_HI / (1 + A_HI)
M2_min = 1 / (1 + A_HI * A_HI)
M2_max = 1 / (1 + A_LO * A_LO)
omM2_min = 1 - M2_max
omM2_max = 1 - M2_min
show_frac("  u_min", u_min)
show_frac("  u_max", u_max)
show_frac("  v_min", v_min)
show_frac("  v_max", v_max)
show_frac("  M2_min", M2_min)
show_frac("  M2_max", M2_max)
show_frac("  1-M2_min", omM2_min)


def interval_lower_bounds(r, k):
    o = auction(r)
    Dv = RHO * o["Delta"]
    Cm_low = Dv * (u_min / 2 + v_min * M2_min)
    Cp_low = o["Delta"] * (u_min * omM2_min + v_min * RHO / 2)
    uv_min = A_LO / ((1 + A_LO) * (1 + A_LO))
    inner_low = 2 * Dv + (1 - RHO) * (o["wH"] * u_min - o["wL"] * v_max)
    C1_low = uv_min * inner_low
    # Upper bound for Cminus, for Cplus minus Cminus.
    Cm_high = Dv * (u_max / 2 + v_max * M2_max)
    Bu_high = gain(o, u_max)
    BM2_low = gain(o, M2_min)
    return {"Cm_low": Cm_low, "Cp_low": Cp_low, "C1_low": C1_low, "Cm_high": Cm_high,
            "Bu_high": Bu_high, "BM2_low": BM2_low, "o": o}


for (r, k) in [(Fraction(3), Fraction(9, 100)), (Fraction(17, 10), Fraction(1, 50))]:
    bnd = interval_lower_bounds(r, k)
    print("r =", str(r), "k =", str(k))
    show_frac("  Cm_low", bnd["Cm_low"])
    show_frac("  Cm_low - k", bnd["Cm_low"] - k)
    show_frac("  Cp_low", bnd["Cp_low"])
    show_frac("  Cp_low - k", bnd["Cp_low"] - k)
    show_frac("  C1_low", bnd["C1_low"])
    show_frac("  C1_low - k", bnd["C1_low"] - k)
    show_frac("  Cm_high", bnd["Cm_high"])
    show_frac("  Cp_low - Cm_high", bnd["Cp_low"] - bnd["Cm_high"])
    show_frac("  6 - B(u_max)", Fraction(6) - bnd["Bu_high"])
    show_frac("  B(M2_min) - 6", bnd["BM2_low"] - Fraction(6))
    # Low class retained deviation upper bound, memo equation 46 without last term.
    # Exact expression: wL*(u-v)*(1-rho) - Delta*(u*M2 + v*rho/2) - k.
    # Upper bound: max first term minus min second term minus k.
    # u-v = (1-a)/(1+a) falls in a. Max at A_LO.
    o = bnd["o"]
    diff_max = (1 - A_LO) / (1 + A_LO)
    second_min = o["Delta"] * (u_min * M2_min + v_min * RHO / 2)
    up46 = o["wL"] * diff_max * (1 - RHO) - second_min - k
    show_frac("  eq46 upper bound (full second term)", up46)
    # Memo drops v*rho/2 inside brackets for its upper bound. That gives larger value.
    second_min_drop = o["Delta"] * (u_min * M2_min)
    up46_drop = o["wL"] * diff_max * (1 - RHO) - second_min_drop - k
    show_frac("  eq46 upper bound (drop v term)", up46_drop)
print()

print("=== Subdivision check for interval, 50 parts ===")
# On each part, bound components by endpoints. Print smallest lower bounds.
def subdiv_min(r, k, parts):
    o = auction(r)
    Dv = RHO * o["Delta"]
    bestCm = None
    bestCp = None
    bestC1 = None
    worstBu = None
    worstBM = None
    for i in range(parts):
        lo = A_LO + (A_HI - A_LO) * Fraction(i, parts)
        hi = A_LO + (A_HI - A_LO) * Fraction(i + 1, parts)
        umin = 1 / (1 + hi)
        umax = 1 / (1 + lo)
        vmin = lo / (1 + lo)
        vmax = hi / (1 + hi)
        Mmin = 1 / (1 + hi * hi)
        Mmax = 1 / (1 + lo * lo)
        ommin = 1 - Mmax
        Cm_low = Dv * (umin / 2 + vmin * Mmin)
        Cp_low = o["Delta"] * (umin * ommin + vmin * RHO / 2)
        uvmin = lo / ((1 + lo) * (1 + lo))
        inner_low = 2 * Dv + (1 - RHO) * (o["wH"] * umin - o["wL"] * vmax)
        C1_low = uvmin * inner_low
        Bu = gain(o, umax)
        BM = gain(o, Mmin)
        if bestCm is None or Cm_low < bestCm:
            bestCm = Cm_low
        if bestCp is None or Cp_low < bestCp:
            bestCp = Cp_low
        if bestC1 is None or C1_low < bestC1:
            bestC1 = C1_low
        if worstBu is None or Bu > worstBu:
            worstBu = Bu
        if worstBM is None or BM < worstBM:
            worstBM = BM
    return bestCm, bestCp, bestC1, worstBu, worstBM


for (r, k) in [(Fraction(3), Fraction(9, 100)), (Fraction(17, 10), Fraction(1, 50))]:
    cm, cp, c1, bu, bm = subdiv_min(r, k, 50)
    print("r =", str(r))
    show_frac("  subdiv Cm_low - k", cm - k)
    show_frac("  subdiv Cp_low - k", cp - k)
    show_frac("  subdiv C1_low - k", c1 - k)
    show_frac("  subdiv 6 - max B(u)", Fraction(6) - bu)
    show_frac("  subdiv min B(M2) - 6", bm - Fraction(6))
print()

print("=== Exponential enclosure by alternating sums ===")
# exp(-1/2) = sum (-1/2)^n / n!. Terms fall in size. Sums alternate about limit.
def alt_sum(n):
    s = Fraction(0)
    term = Fraction(1)
    # term_n = (-1/2)^n / n!. Build by recurrence.
    s = Fraction(1)
    cur = Fraction(1)
    for j in range(1, n + 1):
        cur = cur * Fraction(-1, 2) / j
        s = s + cur
    return s


for n in [4, 5, 6, 7, 8, 9, 10, 11]:
    show_frac("  S" + str(n), alt_sum(n))
S9 = alt_sum(9)
S10 = alt_sum(10)
print("  S9 < S10 ?", S9 < S10)
print("  interval [606530/10^6, 606531/10^6] =",
      str(Fraction(606530, 1000000)), str(Fraction(606531, 1000000)))
print("  S9 in interval ?", Fraction(606530, 1000000) <= S9 <= Fraction(606531, 1000000))
print("  S10 in interval ?", Fraction(606530, 1000000) <= S10 <= Fraction(606531, 1000000))
print("  [29/48, 233/384] decimal:", float(Fraction(29, 48)), float(Fraction(233, 384)))
print("  S4, S5 check:", str(alt_sum(4)), str(alt_sum(5)))
print()

print("=== Benchmark certificate with rational enclosure ===")
A_B_LO = Fraction(606530, 1000000)
A_B_HI = Fraction(606531, 1000000)
# M2 falls in a. m2 = 1-M2 rises in a.
M2_b_min = 1 / (1 + A_B_HI * A_B_HI)
M2_b_max = 1 / (1 + A_B_LO * A_B_LO)
m2_b_min = 1 - M2_b_max
m2_b_max = 1 - M2_b_min
show_frac("  M2 min", M2_b_min)
show_frac("  M2 max", M2_b_max)
show_frac("  m2 min", m2_b_min)
show_frac("  m2 max", m2_b_max)
K_B = Fraction(1, 50)
for r in [Fraction(6, 5), Fraction(3), Fraction(18, 5)]:
    o = auction(r)
    print("r =", str(r))
    show_frac("  Delta", o["Delta"])
    show_frac("  Delta - k", o["Delta"] - K_B)
    show_frac("  rho*m2_min*Delta", RHO * m2_b_min * o["Delta"])
    show_frac("  rho*m2_min*Delta - k", RHO * m2_b_min * o["Delta"] - K_B)
    show_frac("  B(1/2) - 6", gain(o, Fraction(1, 2)) - 6)
    show_frac("  B(M2_min) - 6", gain(o, M2_b_min) - 6)
    show_frac("  B(M2_max) - 6", gain(o, M2_b_max) - 6)
    show_frac("  6 - B(M2_max)", Fraction(6) - gain(o, M2_b_max))
print()

print("=== Fifty digit benchmark values ===")
a_mp = exp(mpf(-1) / 2)
u_mp = 1 / (1 + a_mp)
v_mp = a_mp / (1 + a_mp)
M2_mp = 1 / (1 + a_mp * a_mp)
m2_mp = a_mp * a_mp / (1 + a_mp * a_mp)
print("  a =", mp.nstr(a_mp, 30))
print("  u =", mp.nstr(u_mp, 30))
print("  v =", mp.nstr(v_mp, 30))
print("  M2 =", mp.nstr(M2_mp, 30))
print("  m2 =", mp.nstr(m2_mp, 30))
E2_mp = mpf("0.25") + mpf("0.75") / 2 * (u_mp * u_mp + v_mp * v_mp)
OH_mp = mpf("0.25") / 2 + mpf("0.75") / 2 * u_mp * u_mp
print("  E2 (entry only after ++) =", mp.nstr(E2_mp, 30))
print("  OH2 =", mp.nstr(OH_mp, 30))
# Gross values at b=2 with fifty digits, by closed forms.
def auction_float(r_float):
    # r_float is mpf. Other inputs are exact decimals.
    p = mpf("0.5")
    ell = mpf(1)
    h = mpf(10)
    t0 = p * (1 - p / r_float)
    tH = r_float / 2 + p * p / (2 * r_float)
    tL = ell - (ell * ell - p * p) / (2 * r_float)
    gH = h - r_float / 2 - p * p / (2 * r_float)
    gL = (ell * ell - p * p) / (2 * r_float)
    delta = tH - tL
    wH = tH - t0
    wL = tL - t0
    return t0, tH, tL, gH, gL, delta, wH, wL


for rs in ["1.2", "1.7", "3", "3.6"]:
    t0, tH, tL, gH, gL, delta, wH, wL = auction_float(mpf(rs))
    B_half = gL + mpf("0.5") * (gH - gL)
    B_u = gL + u_mp * (gH - gL)
    B_M2 = gL + M2_mp * (gH - gL)
    Dmp = mpf("0.25") * delta
    Cm = Dmp * (u_mp / 2 + v_mp * M2_mp)
    Cp = delta * (u_mp * (1 - M2_mp) + v_mp * mpf("0.25") / 2)
    C1 = u_mp * v_mp * (2 * Dmp + mpf("0.75") * (wH * u_mp - wL * v_mp))
    print("  r =", rs)
    print("    Delta =", mp.nstr(delta, 20), " B(1/2) =", mp.nstr(B_half, 20))
    print("    B(u) =", mp.nstr(B_u, 20), " B(M2) =", mp.nstr(B_M2, 20))
    print("    Cminus =", mp.nstr(Cm, 20), " Cplus =", mp.nstr(Cp, 20), " C1 =", mp.nstr(C1, 20))
    print("    Cminus-0.02 =", mp.nstr(Cm - mpf("0.02"), 20))
    print("    rho*m2*Delta =", mp.nstr(mpf("0.25") * m2_mp * delta, 20))
    # Prices for r=3 full case.
    if rs == "3":
        Pmm = t0 + mpf("0.25") * (wL + delta * m2_mp)
        Pmid = t0 + mpf("0.25") * (wL + delta * mpf("0.5"))
        Ppp = t0 + (wL + delta * M2_mp)
        # First prices: mean of final price given first sign.
        # Given s1=+, P(s2=+|s1=+) = ? Joint: P(++)/(P(++)+P(+-)).
        # P(++) = .5 u^2 + .5 v^2. P(+-)= .5 u v + .5 v u = u v.
        p_pp = mpf("0.5") * u_mp * u_mp + mpf("0.5") * v_mp * v_mp
        p_pm = u_mp * v_mp
        p_mp_ = u_mp * v_mp
        p_mm = mpf("0.5") * v_mp * v_mp + mpf("0.5") * u_mp * u_mp
        P1p = (p_pp * Ppp + p_pm * Pmid) / (p_pp + p_pm)
        P1m = (p_mp_ * Pmid + p_mm * Pmm) / (p_mp_ + p_mm)
        print("    P2(--) =", mp.nstr(Pmm, 20), " P2(mid) =", mp.nstr(Pmid, 20),
              " P2(++) =", mp.nstr(Ppp, 20))
        print("    P1(-) =", mp.nstr(P1m, 20), " P1(+) =", mp.nstr(P1p, 20))
        PiH = C1 + u_mp * Cp + v_mp * Cm - 2 * mpf("0.02")
        print("    PiH full k=0.02 =", mp.nstr(PiH, 20))
print()

print("=== Posterior ceiling bound value ===")
t0f, tHf, tLf, gHf, gLf, deltaf, wHf, wLf = auction_float(mpf(3))
Wf = wHf - mpf("0.25") * wLf
bound54 = (Wf - mpf("0.02")) / (Wf - mpf("0.02") + mpf("0.02") * a_mp * a_mp)
print("  W(r=3) =", mp.nstr(Wf, 20))
print("  bound 54 =", mp.nstr(bound54, 20))
o3 = auction(Fraction(3))
show_frac("  W exact", o3["wH"] - RHO * o3["wL"])
print()

# --- Three-point model ---
# Flow x = q + Z. Z uniform on -1,0,1. q in 0,1.

def tp_prob(x, order):
    if order == 0:
        if x in (-1, 0, 1):
            return Fraction(1, 3)
        return Fraction(0)
    if x in (0, 1, 2):
        return Fraction(1, 3)
    return Fraction(0)


def tp_R_eval(r, sigH, sigL, pol, k, priorH=Fraction(1, 2)):
    # pol[(cls,n,x1)] is second buy prob. cls H/L, n first order, x1 first flow.
    # Completion: unused upper flow 2 gets belief 1. Other unused keeps prior belief.
    o = auction(r)
    flows = [-1, 0, 1, 2]
    sig = {"H": sigH, "L": sigL}
    prior = {"H": priorH, "L": 1 - priorH}
    w = {"H": o["wH"], "L": o["wL"]}
    joint = {}
    for cls in ["H", "L"]:
        for n in [0, 1]:
            pn = sig[cls] if n == 1 else (1 - sig[cls])
            for x1 in flows:
                p1 = tp_prob(x1, n)
                b = pol[(cls, n, x1)]
                for x2 in flows:
                    p2 = b * tp_prob(x2, 1) + (1 - b) * tp_prob(x2, 0)
                    joint[(cls, n, x1, x2)] = prior[cls] * pn * p1 * p2
    # First beliefs. Denominator zero only for x1=2 with no first buys.
    mu1 = {}
    for x1 in flows:
        num = Fraction(0)
        den = Fraction(0)
        for cls in ["H", "L"]:
            for n in [0, 1]:
                for x2 in flows:
                    den = den + joint[(cls, n, x1, x2)]
                    if cls == "H":
                        num = num + joint[(cls, n, x1, x2)]
        if den == 0:
            if x1 == 2:
                mu1[x1] = Fraction(1)
            else:
                mu1[x1] = priorH
        else:
            mu1[x1] = num / den
    mu2 = {}
    e2 = {}
    P2 = {}
    for x1 in flows:
        for x2 in flows:
            num = Fraction(0)
            den = Fraction(0)
            for cls in ["H", "L"]:
                for n in [0, 1]:
                    den = den + joint[(cls, n, x1, x2)]
                    if cls == "H":
                        num = num + joint[(cls, n, x1, x2)]
            if den == 0:
                if x2 == 2:
                    m = Fraction(1)
                else:
                    m = mu1[x1]
            else:
                m = num / den
            mu2[(x1, x2)] = m
            e2[(x1, x2)] = entry(o, m)
            P2[(x1, x2)] = price_final(o, m)
    P1 = {}
    for x1 in flows:
        den = Fraction(0)
        acc = Fraction(0)
        for cls in ["H", "L"]:
            for n in [0, 1]:
                for x2 in flows:
                    pj = joint[(cls, n, x1, x2)]
                    den = den + pj
                    acc = acc + pj * (o["t0"] + e2[(x1, x2)] * w[cls])
        if den == 0:
            # Price at unused first flow from completion belief and candidate future.
            # Use final price function at mu1 with no further learning as placeholder.
            # Deviation buyer reaches x1=2. Future law after x1 uses candidate policy.
            # Compute mean value given completion class H and candidate second law.
            # Candidate second law after x1=2: need inventory law. Use H with n from sig?
            # Simpler: price from mu1 and expected entry under candidate second buys.
            # For candidates in this check, second buy after x1=2 is 0, so mu stays mu1.
            P1[x1] = price_final(o, mu1[x1])
        else:
            P1[x1] = acc / den
    # For unused x1 with den 0, refine P1 by direct mean over x2 under completion.
    # Completion says class H. Inventory law for price: market must hold a law.
    # Candidates here set second order 0 after x1=2 for every inventory.
    # Then e2 uses mu2 completion and P1 equals mean of P2 under zero order.
    # The placeholder above equals that value when second order is 0. Print will show.
    def plan_value(cls, n, q2map):
        total = Fraction(0)
        for x1 in flows:
            p1 = tp_prob(x1, n)
            if p1 == 0:
                continue
            q = q2map[x1]
            inner = Fraction(0)
            for x2 in flows:
                p2 = tp_prob(x2, q)
                if p2 == 0:
                    continue
                val = o["t0"] + e2[(x1, x2)] * w[cls]
                inner = inner + p2 * ((n + q) * val - q * P2[(x1, x2)])
            inner = inner - n * P1[x1] - k * n - k * q
            total = total + p1 * inner
        return total
    # Plans: second order for each first flow. 16 plans.
    plans = []
    for mask in range(16):
        qmap = {}
        for idx, x1 in enumerate(flows):
            qmap[x1] = (mask >> idx) & 1
        plans.append(qmap)
    Ubest = {}
    Ubest_plan = {}
    for cls in ["H", "L"]:
        for n in [0, 1]:
            best = None
            bestp = None
            for qmap in plans:
                val = plan_value(cls, n, qmap)
                if best is None or val > best:
                    best = val
                    bestp = dict(qmap)
            Ubest[(cls, n)] = best
            Ubest_plan[(cls, n)] = bestp
    gamma = {}
    for cls in ["H", "L"]:
        for n in [0, 1]:
            for x1 in flows:
                cont1 = Fraction(0)
                cont0 = Fraction(0)
                for x2 in flows:
                    val = o["t0"] + e2[(x1, x2)] * w[cls]
                    cont1 = cont1 + tp_prob(x2, 1) * ((n + 1) * val - P2[(x1, x2)])
                    cont0 = cont0 + tp_prob(x2, 0) * (n * val)
                gamma[(cls, n, x1)] = (cont1 - k) - cont0
    tot_entry = Fraction(0)
    own_H = Fraction(0)
    for key in joint:
        cls, n, x1, x2 = key
        tot_entry = tot_entry + joint[key] * e2[(x1, x2)]
        if cls == "H":
            own_H = own_H + joint[key] * e2[(x1, x2)]
    # Expected purchases given H under candidate.
    expN_H = Fraction(0)
    # First mean.
    expN_H = expN_H + sigH
    # Second mean: sum over n,x1 P(n,x1|H) * pol.
    sec = Fraction(0)
    for n in [0, 1]:
        pn = sigH if n == 1 else (1 - sigH)
        for x1 in flows:
            sec = sec + pn * tp_prob(x1, n) * pol[("H", n, x1)]
    expN_H = expN_H + sec
    # Net profit given H under candidate (on path plan value with candidate orders).
    # Candidate orders may mix. Compute mean over first mix and second mix directly.
    # Use law of joint plus prices: profit mean given H.
    # Profit = (n+q2)*val - n*P1 - q2*P2 - k*(n+q2). q2 random with prob pol.
    # Joint already averages over q2 mix via p2 law, but q2 value itself needs mean.
    # Compute by enumeration over n,x1,q2,x2.
    profH = Fraction(0)
    for n in [0, 1]:
        pn = sigH if n == 1 else (1 - sigH)
        for x1 in flows:
            p1 = tp_prob(x1, n)
            b = pol[("H", n, x1)]
            for q in [0, 1]:
                pq = b if q == 1 else (1 - b)
                for x2 in flows:
                    p2 = tp_prob(x2, q)
                    val = o["t0"] + e2[(x1, x2)] * w["H"]
                    term = (n + q) * val - n * P1[x1] - q * P2[(x1, x2)] - k * (n + q)
                    profH = profH + pn * p1 * pq * p2 * term
    return {"o": o, "mu1": mu1, "mu2": mu2, "e2": e2, "P1": P1, "P2": P2,
            "Ubest": Ubest, "Ubest_plan": Ubest_plan, "gamma": gamma,
            "entry": tot_entry, "ownH": own_H, "expN_H": expN_H, "profH": profH,
            "joint": joint}


print("=== Three-point thresholds and ceiling ===")
o3 = auction(Fraction(3))
show_frac("  Delta r=3", o3["Delta"])
show_frac("  wH", o3["wH"])
show_frac("  wL", o3["wL"])
show_frac("  D=rho*Delta", RHO * o3["Delta"])
show_frac("  K at pi=1/2, e=rho", Fraction(2, 3) * Fraction(1, 2) * RHO * o3["Delta"])
show_frac("  J=(1-rho)*wH/3", (1 - RHO) * o3["wH"] / 3)
show_frac("  B(1/2) r=3", gain(o3, Fraction(1, 2)))
show_frac("  gH r=3 (=B(1))", o3["gH"])
show_frac("  B(0)=gL", o3["gL"])
# Ceiling root: gH(r)=6 gives r^2-8r+1/4=0. Larger root 4+sqrt(63/4).
from mpmath import sqrt as mpsqrt
rC_mp = 4 + mpsqrt(mpf(63) / 4)
print("  rC =", mp.nstr(rC_mp, 30))
print("  4+sqrt(16-1/4) =", mp.nstr(4 + mpsqrt(mpf(16) - mpf("0.25")), 30))
print()

print("=== Three-point Design R mixed candidate, r=3, k=3/20, beta=26/81 ===")
BETA_MIX = Fraction(26, 81)
pol_mix = {}
for cls in ["H", "L"]:
    for n in [0, 1]:
        for x1 in [-1, 0, 1, 2]:
            if cls == "H" and n == 1 and x1 in (0, 1):
                pol_mix[(cls, n, x1)] = Fraction(1)
            else:
                pol_mix[(cls, n, x1)] = Fraction(0)
resM = tp_R_eval(Fraction(3), BETA_MIX, Fraction(0), pol_mix, Fraction(3, 20))
print("  mu1:", {kk: str(vv) for kk, vv in resM["mu1"].items()})
for x1 in [-1, 0, 1, 2]:
    row = {}
    for x2 in [-1, 0, 1, 2]:
        row[x2] = str(resM["mu2"][(x1, x2)])
    print("  mu2 x1=", x1, row)
show_frac("  (1-beta)/(2-beta)", (1 - BETA_MIX) / (2 - BETA_MIX))
show_frac("  Ubest H n=1", resM["Ubest"][("H", 1)])
show_frac("  Ubest H n=0", resM["Ubest"][("H", 0)])
show_frac("  Ubest L n=1", resM["Ubest"][("L", 1)])
show_frac("  Ubest L n=0", resM["Ubest"][("L", 0)])
print("  best plan H n=1 (orders by x1 -1,0,1,2):", resM["Ubest_plan"][("H", 1)])
print("  best plan H n=0:", resM["Ubest_plan"][("H", 0)])
print("  best plan L n=1:", resM["Ubest_plan"][("L", 1)])
for cls in ["H", "L"]:
    for n in [0, 1]:
        for x1 in [-1, 0, 1, 2]:
            print("  gamma", cls, "n=", n, "x1=", x1, "=", str(resM["gamma"][(cls, n, x1)]),
                  "~", format(float(resM["gamma"][(cls, n, x1)]), ".12f"),
                  " candidate pol =", str(pol_mix[(cls, n, x1)]))
show_frac("  entry", resM["entry"])
show_frac("  ownH", resM["ownH"])
show_frac("  E[N|H]", resM["expN_H"])
show_frac("  E[kN|H]", Fraction(3, 20) * resM["expN_H"])
show_frac("  PiH candidate mean", resM["profH"])
show_frac("  P1 middle (x1=0)", resM["P1"][0])
show_frac("  P1 lower (x1=-1)", resM["P1"][-1])
show_frac("  P1 upper (x1=2)", resM["P1"][2])
# Memo equation checks.
Kv = Fraction(1, 18)
Jv = Fraction(9, 32)
show_frac("  K+nJ-k n=1", Kv + Jv - Fraction(3, 20))
show_frac("  K-k n=0", Kv - Fraction(3, 20))
show_frac("  (2/3)*D*(1-mu-) with D=1/6", Fraction(2, 3) * Fraction(1, 6) * (1 - Fraction(55, 136)))
show_frac("  GammaL(1) formula 26",
          (1 - RHO) * o3["wL"] / 3 - (1 + RHO) * o3["Delta"] / 3 - Fraction(3, 20))
# U1H(1) formula 25.
f25 = Fraction(5, 3) * (Kv - Fraction(3, 20)) + Fraction(2, 3) * (1 - BETA_MIX / 2) * Jv
show_frac("  formula 25 U1H(1)", f25)
# U1L(1) formula 27.
Dv3 = Fraction(1, 6)
f27 = Fraction(2, 3) * (-Dv3 / 2 - BETA_MIX * Jv / 2) - o3["Delta"] / 3 - Fraction(3, 20)
show_frac("  formula 27 U1L(1) with q2=0 plan", f27)
print()

print("=== Three-point no-trade deviation at k=3/20 (Design R) ===")
pol_zero = {}
for cls in ["H", "L"]:
    for n in [0, 1]:
        for x1 in [-1, 0, 1, 2]:
            pol_zero[(cls, n, x1)] = Fraction(0)
resZ = tp_R_eval(Fraction(3), Fraction(0), Fraction(0), pol_zero, Fraction(3, 20))
show_frac("  Ubest H n=1 (two-order deviation value)", resZ["Ubest"][("H", 1)])
show_frac("  Ubest H n=0", resZ["Ubest"][("H", 0)])
print("  best plan H n=1:", resZ["Ubest_plan"][("H", 1)])
print("  mu1:", {kk: str(vv) for kk, vv in resZ["mu1"].items()})
for cls in ["H", "L"]:
    for n in [0, 1]:
        for x1 in [-1, 0, 1, 2]:
            print("  gamma", cls, "n=", n, "x1=", x1, "~",
                  format(float(resZ["gamma"][(cls, n, x1)]), ".12f"))
print()

print("=== Three-point full purchase, Designs R and S values, r=3 ===")
# Full candidate for R: H buys first. Second: buy after middle flows, stop after reveal.
# After x1=-1, H inventory must be 0 on path (buy cannot give -1). Candidate sets 0.
# After x1=2, stop. For off-path n=0 after middle, candidate for R full check:
# memo says second order is one after either middle flow. That is for n=1 on path.
# For brute best response, Ubest covers n=0 plans. Candidate pol for prices needs
# aggregate second law. On path n=1 with prob 1 in H, so pol for n=0 does not affect prices.
# Set pol H middle =1 for both n to match memo wording. Prices same either way.
pol_full = {}
for cls in ["H", "L"]:
    for n in [0, 1]:
        for x1 in [-1, 0, 1, 2]:
            if cls == "H" and x1 in (0, 1):
                pol_full[(cls, n, x1)] = Fraction(1)
            else:
                pol_full[(cls, n, x1)] = Fraction(0)
for k in [Fraction(1, 50), Fraction(1, 10)]:
    resF = tp_R_eval(Fraction(3), Fraction(1), Fraction(0), pol_full, k)
    print("k =", str(k))
    show_frac("  Ubest H n=1", resF["Ubest"][("H", 1)])
    show_frac("  Ubest H n=0", resF["Ubest"][("H", 0)])
    show_frac("  diff", resF["Ubest"][("H", 1)] - resF["Ubest"][("H", 0)])
    show_frac("  Ubest L n=1", resF["Ubest"][("L", 1)])
    print("  best plan H n=1:", resF["Ubest_plan"][("H", 1)])
    print("  best plan H n=0:", resF["Ubest_plan"][("H", 0)])
    for cls in ["H", "L"]:
        for n in [0, 1]:
            for x1 in [-1, 0, 1, 2]:
                print("  gamma", cls, "n=", n, "x1=", x1, "=", str(resF["gamma"][(cls, n, x1)]),
                      "~", format(float(resF["gamma"][(cls, n, x1)]), ".12f"))
    show_frac("  entry", resF["entry"])
    show_frac("  ownH", resF["ownH"])
    show_frac("  E[N|H]", resF["expN_H"])
    show_frac("  E[kN|H]", k * resF["expN_H"])
    show_frac("  PiH candidate mean (R)", resF["profH"])
    show_frac("  P1 unresolved x1=0", resF["P1"][0])
    show_frac("  P2 unresolved (0,0)", resF["P2"][(0, 0)])
    print("  mu1:", {kk: str(vv) for kk, vv in resF["mu1"].items()})
print()

print("=== Three-point Design S formulas, T=2 ===")
# Active outcome with pi=1/2, e0=e(pi)=rho, e1=1.
s_val = Fraction(2, 3)
for T in [1, 2, 3]:
    ET = RHO + (1 - RHO) * Fraction(1, 2) * (1 - s_val ** T)
    OH = Fraction(1, 2) * RHO + (1 - RHO) * Fraction(1, 2) * (1 - s_val ** T)
    EN = sum([s_val ** (t - 1) for t in range(1, T + 1)], Fraction(0))
    print("T =", T)
    show_frac("  E_T formula 12", ET)
    show_frac("  O_H formula 12", OH)
    show_frac("  E[N|H] formula 12", EN)
# Price path formula 15 at T=2, t=1 unresolved.
o3b = auction(Fraction(3))
P1U = o3b["t0"] + RHO * (o3b["wL"] + Fraction(1, 2) * o3b["Delta"]) + Fraction(1, 2) * (1 - RHO) * o3b["wH"] * (1 - s_val ** 1)
show_frac("  P1U formula 15 T=2 t=1", P1U)
show_frac("  final unresolved price P(1/2)", price_final(o3b, Fraction(1, 2)))
print()
print("End of independent calculations.")

