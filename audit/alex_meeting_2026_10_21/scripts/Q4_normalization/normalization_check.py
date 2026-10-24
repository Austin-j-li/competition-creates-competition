"""Q4 normalization: print-only checks.  No assertions.

Run from the repository root:
    .venv/bin/python audit/alex_meeting_2026_10_21/scripts/Q4_normalization/normalization_check.py

Part 1  Reproduce the benchmark numbers from eq. (4), (9), (12) and the A.9 accounting.
Part 2  Rescale all money primitives by lambda.  Rescale the flow unit.
Part 3  Move c_L inside its window.
Part 4  Identities used in the memo.
Part 5  Other normalizations: p -> 0 as a shift of B; moderate vector in c_L = 1 units.

Entry, ownership and revenue are computed two ways: closed form (12), and a direct
calculation from the primitives (auction by numerical integration over R, entry from
the preparation rule applied to the flow density).
"""
import math
from scipy import integrate
from scipy.optimize import brentq

BENCH = dict(h=10.0, l=1.0, p=0.5, rho=0.25, cL=1.0, cH=6.0, b=2.0, k=0.02)
R0, R1, R2 = 1.2, 3.0, 3.6
MODERATE = dict(h=2.0, l=1.0, p=0.5, rho=0.25, cL=0.3, cH=0.89, b=2.0, k=0.002)
MOD_R0, MOD_R1 = 1.05, 1.5


# ---------- auction layer ----------
def auction_closed(P, r):
    h, l, p = P["h"], P["l"], P["p"]
    t0 = p * (1 - p / r)
    tH = r / 2 + p * p / (2 * r)
    tL = l - (l * l - p * p) / (2 * r)
    gH = h - r / 2 - p * p / (2 * r)
    gL = (l * l - p * p) / (2 * r)
    return dict(t0=t0, tH=tH, tL=tL, gH=gH, gL=gL, dT=tH - tL)


def auction_numeric(P, r):
    """Same objects by integrating the payment rule over R ~ U[0, r]."""
    h, l, p = P["h"], P["l"], P["p"]

    def mean(fun, pts):
        v, _ = integrate.quad(fun, 0, r, points=pts, limit=200)
        return v / r

    pts = [x for x in (p, l) if 0 < x < r]
    t0 = mean(lambda R: p if R >= p else 0.0, pts)
    tH = mean(lambda R: max(p, min(R, h)), pts)
    tL = mean(lambda R: max(p, min(R, l)), pts)
    gH = mean(lambda R: max(h - max(p, R), 0.0), pts)
    gL = mean(lambda R: max(l - max(p, R), 0.0), pts)
    return dict(t0=t0, tH=tH, tL=tL, gH=gH, gL=gL, dT=tH - tL)


def B(a, mu):
    return a["gL"] + mu * (a["gH"] - a["gL"])


# ---------- information layer (flow bound ub, Laplace scale b) ----------
def bounds(b, ub=1.0):
    m = 1.0 / (1.0 + math.exp(2 * ub / b))
    return m, 1 - m


def surv(z, b):  # Laplace survival function
    return 0.5 * math.exp(-z / b) if z > 0 else 1 - 0.5 * math.exp(z / b)


def dens(z, b):
    return math.exp(-abs(z) / b) / (2 * b)


def mu_x(x, b, ub=1.0):
    return 1.0 / (1.0 + math.exp(-(abs(x + ub) - abs(x - ub)) / b))


def cutoff_flow(tau, b, ub=1.0):
    """Smallest x with mu_x(x) >= tau (tie rule: enter at equality)."""
    m, M = bounds(b, ub)
    if tau <= m:
        return -math.inf
    if tau > M:
        return math.inf
    if tau >= M:
        return ub
    return brentq(lambda x: mu_x(x, b, ub) - tau, -ub, ub, xtol=1e-14)


def tail_prob(xc, b, q):
    """Pr(X >= xc) when X = q + Z."""
    if xc == -math.inf:
        return 1.0
    if xc == math.inf:
        return 0.0
    return surv(xc - q, b)


def tau_of(a, c):
    return (c - a["gL"]) / (a["gH"] - a["gL"])


def full_order_outcome(P, r, ub=1.0, a=None):
    """Direct calculation under full orders (ub, -ub), from the preparation rule."""
    a = a or auction_numeric(P, r)
    b, rho = P["b"], P["rho"]
    # low-cost type: prepares where B(mu) >= cL ; high-cost: where B(mu) >= cH
    xL = cutoff_flow(tau_of(a, P["cL"]), b, ub)
    xH = cutoff_flow(tau_of(a, P["cH"]), b, ub)
    eH = rho * tail_prob(xL, b, +ub) + (1 - rho) * tail_prob(xH, b, +ub)
    eL = rho * tail_prob(xL, b, -ub) + (1 - rho) * tail_prob(xH, b, -ub)
    E = 0.5 * (eH + eL)
    OH = 0.5 * eH
    RT = a["t0"] + 0.5 * (eH * (a["tH"] - a["t0"]) + eL * (a["tL"] - a["t0"]))
    # allocation surplus net of paid costs (A.40): W0 + E[ 1{prep} (B(mu_X) + p^2/r - C) ]
    p = P["p"]
    W0 = (r * r - p * p) / (2 * r)

    def piece(xc, cost, weight):
        if xc == math.inf:
            return 0.0
        lo = -40.0 if xc == -math.inf else xc

        def integrand(x):
            f = 0.5 * (dens(x - ub, b) + dens(x + ub, b))
            return f * (B(a, mu_x(x, b, ub)) + p * p / r - cost)

        pts = [v for v in (-ub, ub) if v > lo]
        v1, _ = integrate.quad(integrand, lo, 40.0, points=pts, limit=400)
        return weight * v1

    W = W0 + piece(xL, P["cL"], rho) + piece(xH, P["cH"], 1 - rho)
    return dict(E=E, OH=OH, RT=RT, W=W, eH=eH, eL=eL, tauH=tau_of(a, P["cH"]), xH=xH)


def closed_form_12(P, r):
    a = auction_closed(P, r)
    b, rho = P["b"], P["rho"]
    tau = tau_of(a, P["cH"])
    xs = (b / 2) * math.log(tau / (1 - tau))
    aH = 1 - 0.5 * math.exp((xs - 1) / b)
    aL = 0.5 * math.exp(-(xs + 1) / b)
    E = rho + (1 - rho) * (aH + aL) / 2
    OH = 0.5 * (rho + (1 - rho) * aH)
    RT = a["t0"] + 0.5 * ((rho + (1 - rho) * aH) * (a["tH"] - a["t0"])
                          + (rho + (1 - rho) * aL) * (a["tL"] - a["t0"]))
    return dict(tau=tau, xstar=xs, aH=aH, aL=aL, E=E, OH=OH, RT=RT)


def window(P, r0, r1, r2=None):
    m, M = bounds(P["b"])
    a0, a1 = auction_closed(P, r0), auction_closed(P, r1)
    out = dict(
        BL=B(a1, m),
        A2lo=B(a0, 0.5),
        A2hi=B(a1, M),
        A3lo=a0["dT"],
        A3hi=(1 - 1 / P["b"]) * P["rho"] * m * a1["dT"],
    )
    if r2:
        a2 = auction_closed(P, r2)
        out["BL2"] = B(a2, m)
        out["A2hi2"] = B(a2, M)
    return out


def investor_marginal(P, r, ub=1.0, ngrid=11):
    """U'(s) = d/ds [ s (F(s) - k) ] for the correctly signed order in state H,
    against the full-order candidate schedule (price and entry as in eq. 9)."""
    a = auction_numeric(P, r)
    b, rho, k = P["b"], P["rho"], P["k"]
    xL = cutoff_flow(tau_of(a, P["cL"]), b, ub)
    xH = cutoff_flow(tau_of(a, P["cH"]), b, ub)

    def e_of(x):
        return rho * (x >= xL) + (1 - rho) * (x >= xH)

    def FH(s):
        def integrand(x):
            mu = mu_x(x, b, ub)
            return dens(x - s, b) * e_of(x) * a["dT"] * (1 - mu)

        pts = sorted(set([-ub, ub] + [v for v in (xL, xH) if abs(v) < 40]))
        v, _ = integrate.quad(integrand, -40, 40, points=pts, limit=800)
        return v

    h_step = 1e-4
    vals = []
    for i in range(ngrid):
        s = ub * i / (ngrid - 1)
        U = lambda t: t * (FH(t) - k)
        lo, hi = max(0.0, s - h_step), min(ub, s + h_step)
        vals.append((U(hi) - U(lo)) / (hi - lo))
    return min(vals), max(vals)


def fmt(x, n=6):
    return f"{x:.{n}f}"


def scaled(P, lam):
    Q = dict(P)
    for key in ("h", "l", "p", "cL", "cH", "k"):
        Q[key] = lam * P[key]
    return Q


# =====================================================================
print("PART 1. Reproduce the benchmark (eq. 4, 9, 12; A.9 accounting)")
a0c, a1c = auction_closed(BENCH, R0), auction_closed(BENCH, R1)
a0n, a1n = auction_numeric(BENCH, R0), auction_numeric(BENCH, R1)
print("  closed form r1:", {k: fmt(v) for k, v in a1c.items()})
print("  numeric  r1  :", {k: fmt(v) for k, v in a1n.items()})
print("  B_r0(1/2)=%s  B_r1(1/2)=%s (paper: 4.804167, 4.291667)" % (fmt(B(a0c, .5)), fmt(B(a1c, .5))))
print("  Delta_T(r0)=%s Delta_T(r1)=%s (paper: 0.016667, 0.666667)" % (fmt(a0c["dT"]), fmt(a1c["dT"])))
cf = closed_form_12(BENCH, R1)
print("  eq.(12) at r1:", {k: fmt(v) for k, v in cf.items()})
d1 = full_order_outcome(BENCH, R1)
print("  direct at r1 :", {k: fmt(v) for k, v in d1.items() if k in ("E", "OH", "RT", "W", "tauH")})
print("  paper: E=0.522757  O_H=0.324192  R_T=0.872392  W=2.382301")
cf2 = closed_form_12(BENCH, R2)
print("  r2: tau=%s (>M? M=%s)  -> no expensive entry, E = rho = 0.25" %
      (fmt(cf2["tau"]), fmt(bounds(BENCH['b'])[1])))
w = window(BENCH, R0, R1, R2)
print("  window:", {k: fmt(v) for k, v in w.items()})
lo, hi = investor_marginal(BENCH, R1)
print("  investor marginal profit U'(s) on s in [0,1] at r1: min %s max %s (positive => full orders)" % (fmt(lo), fmt(hi)))

# =====================================================================
print("\nPART 2. Rescale money by lambda (h, l, p, r, cL, cH, k all times lambda)")
base = full_order_outcome(BENCH, R1)
for lam in (1 / 7, 3.7, 100.0):
    Q = scaled(BENCH, lam)
    out = full_order_outcome(Q, lam * R1)
    cfq = closed_form_12(Q, lam * R1)
    lo, hi = investor_marginal(Q, lam * R1)
    print("  lambda=%8.5f  E=%s O_H=%s tau=%s | R_T/lam=%s W/lam=%s | closed-form E=%s | U'/lam min=%s" %
          (lam, fmt(out["E"]), fmt(out["OH"]), fmt(out["tauH"]), fmt(out["RT"] / lam),
           fmt(out["W"] / lam), fmt(cfq["E"]), fmt(lo / lam)))
print("  base          E=%s O_H=%s R_T=%s W=%s" % (fmt(base["E"]), fmt(base["OH"]), fmt(base["RT"]), fmt(base["W"])))
lam = 3.7
Q = scaled(BENCH, lam)
a_b, a_q = auction_closed(BENCH, R1), auction_closed(Q, lam * R1)
print("  price level at mu=0.6 (e=1 branch not used; entry rho): P_base=%s  P_scaled/lam=%s" % (
    fmt(a_b['t0'] + 0.25 * (a_b['tL'] - a_b['t0'] + a_b['dT'] * 0.6)),
    fmt((a_q['t0'] + 0.25 * (a_q['tL'] - a_q['t0'] + a_q['dT'] * 0.6)) / lam)))
print("  moderate vector, lambda=1/0.3 (c_L becomes 1):")
Qm = scaled(MODERATE, 1 / 0.3)
for nm, P_, r_ in (("   original", MODERATE, MOD_R1), ("   rescaled", Qm, MOD_R1 / 0.3)):
    o = full_order_outcome(P_, r_)
    print("    %s: h=%s l=%s p=%s cL=%s cH=%s k=%s r1=%s -> E=%s O_H=%s" % (
        nm, fmt(P_['h'], 4), fmt(P_['l'], 4), fmt(P_['p'], 4), fmt(P_['cL'], 4), fmt(P_['cH'], 4),
        fmt(P_['k'], 5), fmt(r_, 4), fmt(o["E"]), fmt(o["OH"])))

print("\n  Flow unit: replace |q| <= 1 by |q| <= u and b by u*b (k unchanged)")
for u in (0.37, 5.0):
    P_ = dict(BENCH)
    P_["b"] = u * BENCH["b"]
    out = full_order_outcome(P_, R1, ub=u)
    # investor marginal profit per unit of flow scales with u; compare U'(s)/u? Orders in [0,u].
    print("    u=%5.2f  E=%s O_H=%s  (m=%s)" % (u, fmt(out["E"]), fmt(out["OH"]), fmt(bounds(P_["b"], u)[0])))

# =====================================================================
print("\nPART 3. Move c_L inside its window (benchmark; window is [0, min(B_r1(m), B_r2(m))) )")
print("  B_r1(m)=%s  B_r2(m)=%s" % (fmt(w["BL"]), fmt(w["BL2"])))
for cL in (0.0, 0.125, 0.5, 1.0, 2.0, 2.2, 2.26):
    P_ = dict(BENCH)
    P_["cL"] = cL
    o = full_order_outcome(P_, R1)
    o0 = full_order_outcome(P_, R0)
    lo, _ = investor_marginal(P_, R1, ngrid=5)
    print("  cL=%5.3f  r1: E=%s O_H=%s R_T=%s W=%s  min U'=%s | r0 hidden-price entry rule: low-cost enters at 1/2? %s" %
          (cL, fmt(o["E"]), fmt(o["OH"]), fmt(o["RT"]), fmt(o["W"]), fmt(lo),
           B(auction_closed(P_, R0), 0.5) >= cL))
print("  W shift check: W(cL=1) - W(cL=0) = %s ; -rho*1 = %s" % (
    fmt(full_order_outcome(BENCH, R1)["W"] - full_order_outcome({**BENCH, 'cL': 0.0}, R1)["W"]), fmt(-0.25)))
print("  Sufficient for A1 regardless of b, rho, h: cL <= g_L(r1) = %s" % fmt(a1c["gL"]))
print("  Diagnostic only (frozen full orders, NOT an equilibrium claim): cL just above B_r1(m)")
for cL in (w["BL"] - 0.01, w["BL"] + 0.05, w["BL"] + 0.5):
    P_ = dict(BENCH)
    P_["cL"] = cL
    o = full_order_outcome(P_, R1)
    print("    cL=%s  frozen-profile E=%s" % (fmt(cL, 4), fmt(o["E"])))

print("\n  Moderate vector window:")
wm = window(MODERATE, MOD_R0, MOD_R1)
print("   ", {k: fmt(v) for k, v in wm.items()})
for cL in (0.0, 0.3, 0.9 * wm["BL"]):
    P_ = dict(MODERATE)
    P_["cL"] = cL
    o = full_order_outcome(P_, MOD_R1)
    print("    cL=%s  E=%s O_H=%s" % (fmt(cL, 4), fmt(o["E"]), fmt(o["OH"])))
print("    paper: entry 0.526805 at r1")

# =====================================================================
print("\nPART 4. Identities (benchmark r1; also random draws)")
import random
random.seed(1)
for trial in range(3):
    h = random.uniform(3, 12)
    l = random.uniform(0.5, 2)
    p = random.uniform(0.05, 0.95) * l
    r = random.uniform(1.05, 0.95 * h / l) * l
    P_ = dict(h=h, l=l, p=p)
    a = auction_closed(P_, r)
    print("  h=%.3f l=%.3f p=%.3f r=%.3f: tH+gH-h=%.2e  tL+gL-l=%.2e  (gH-gL)-(h-l-dT)=%.2e  B(mu)-[B0(mu)-p^2/(2r)] at mu=.4: %.2e" % (
        h, l, p, r, a["tH"] + a["gH"] - h, a["tL"] + a["gL"] - l, (a["gH"] - a["gL"]) - (h - l - a["dT"]),
        B(a, .4) - (B(auction_closed(dict(h=h, l=l, p=0.0), r), .4) - p * p / (2 * r))))
for (l_, r_) in ((1.0, 3.0), (1.771, 2.405)):
    d_ = auction_closed(dict(h=10.0, l=l_, p=0.3 * l_), r_)["dT"]
    print("  Delta_T(r) = l*(cosh(ln(r/l)) - 1):  l=%s r=%s: %s vs %s" % (l_, r_, fmt(d_), fmt(l_ * (math.cosh(math.log(r_ / l_)) - 1))))
print("  tau_low (A2 in belief units) = (B_r0(1/2) - g_L(r1)) / (g_H(r1) - g_L(r1)) = %s" % fmt((B(a0c, .5) - a1c["gL"]) / (a1c["gH"] - a1c["gL"])))

# =====================================================================
print("\nPART 5. Other normalizations")
print("  p -> 0 is not a unit choice. Benchmark with p=0 instead of 0.5 (same other numbers):")
P0 = dict(BENCH)
P0["p"] = 0.0
c0 = closed_form_12(P0, R1)
print("    E=%s (p=0.5: %s)  tau=%s (p=0.5: %s)" % (fmt(c0["E"]), fmt(cf["E"]), fmt(c0["tau"]), fmt(cf["tau"])))
shift = BENCH["p"] ** 2 / (2 * R1)
Pshift = dict(P0)
Pshift["cH"] = BENCH["cH"] + shift
c1 = closed_form_12(Pshift, R1)
print("    p=0 with cH raised by p^2/(2 r1) = %s : E=%s  (equals the p=0.5 value)" % (fmt(shift), fmt(c1["E"])))
print("    the shift is p^2/(2r): at r0 = %s, at r1 = %s, at r2 = %s (it differs across r)" % (
    fmt(BENCH["p"] ** 2 / (2 * R0)), fmt(shift), fmt(BENCH["p"] ** 2 / (2 * R2))))
print("  Reduced form: E and O_H depend on (rho, b, tau_1) only. Two economies with the same tau_1, rho, b:")
Pa = dict(BENCH)
Pb = scaled(dict(BENCH, h=7.0, l=1.0, p=0.3, k=0.01), 1.0)
# choose cH in economy b to hit the same tau at r=2.5
ab = auction_closed(Pb, 2.5)
Pb["cH"] = ab["gL"] + cf["tau"] * (ab["gH"] - ab["gL"])
cb = closed_form_12(Pb, 2.5)
print("    benchmark: tau=%s E=%s O_H=%s | other economy (h=7, p=0.3, r1=2.5, cH=%s): tau=%s E=%s O_H=%s" % (
    fmt(cf["tau"]), fmt(cf["E"]), fmt(cf["OH"]), fmt(Pb["cH"]), fmt(cb["tau"]), fmt(cb["E"]), fmt(cb["OH"])))
print("  A3 in ratio form: k_hat = k/Delta_T(r1) must lie in (Delta_T(r0)/Delta_T(r1), (1-1/b) rho m):")
m_, M_ = bounds(BENCH["b"])
print("    k_hat=%s  lower=%s  upper=%s" % (fmt(BENCH["k"] / a1c["dT"]), fmt(a0c["dT"] / a1c["dT"]),
                                            fmt((1 - 1 / BENCH["b"]) * BENCH["rho"] * m_)))
print("  Cost positions in the windows: v = cL/B_r1(m), u = (cH - B_r0(1/2))/(B_r1(M) - B_r0(1/2))")
print("    benchmark: v=%s  u=%s" % (fmt(BENCH["cL"] / w["BL"]), fmt((BENCH["cH"] - w["A2lo"]) / (w["A2hi"] - w["A2lo"]))))
