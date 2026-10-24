"""Independent check of memo C1 (two-sided orders, discrete-Laplace noise).

Print-only. 50-digit arithmetic. Run from the repository root:
    .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/X_C1_check/exact.py

Model. Noise Z = G1 - G2, P(Z = z) = (1-a)/(1+a) a^|z|, a = exp(-1/b).
Orders q in {-1, 0, 1}; flow X = q + Z. Prior 1/2 unless stated. c_L = 0.
Entry at posterior mu: rho + (1-rho) 1{B_r(mu) >= c_H} (prepare at indifference).
Price P(x) = t0 + e(x) (tL - t0 + DT mu(x)).
"""
from mpmath import mp, mpf, exp, sqrt, log, nstr

mp.dps = 50

H_VAL = mpf(10)
ELL = mpf(1)
P_RES = mpf("0.5")
RHO = mpf("0.25")
B_SCALE = mpf(2)
K_COST = mpf("0.02")
A = exp(-1 / B_SCALE)
D = 1 - A
HALF = mpf(1) / 2
XMAX = 330  # a^330 = e^-165, far below 1e-50
ORDERS = (-1, 0, 1)


def s(x, n=12):
    return nstr(x, n)


def pmf(z):
    return (1 - A) / (1 + A) * A ** abs(z)


def prims(r):
    r = mpf(r)
    t0 = P_RES * (1 - P_RES / r)
    tH = r / 2 + P_RES ** 2 / (2 * r)
    tL = ELL - (ELL ** 2 - P_RES ** 2) / (2 * r)
    gH = H_VAL - r / 2 - P_RES ** 2 / (2 * r)
    gL = (ELL ** 2 - P_RES ** 2) / (2 * r)
    DT = (r - ELL) ** 2 / (2 * r)
    return dict(t0=t0, tH=tH, tL=tL, gH=gH, gL=gL, DT=DT)


def Bval(r, mu):
    pr = prims(r)
    return pr["gL"] + mu * (pr["gH"] - pr["gL"])


def tau(r, cH):
    pr = prims(r)
    return (cH - pr["gL"]) / (pr["gH"] - pr["gL"])


def rr(dd):
    """Root above ell of Delta_T(r) = dd."""
    return ELL + dd + sqrt(dd ** 2 + 2 * ELL * dd)


def entry(r, cH, mu):
    return RHO + (1 - RHO) * (1 if Bval(r, mu) >= cH else 0)


# ---------------------------------------------------------------- direct sums
def lik(sig, x):
    return sum(sig[q] * pmf(x - q) for q in ORDERS)


def direct_posterior(sH, sL, x, pi=HALF):
    lh, ll = lik(sH, x), lik(sL, x)
    return pi * lh / (pi * lh + (1 - pi) * ll)


def direct_payoff(r, cH, sH, sL, theta, q):
    """Expected payoff of order q for type theta against the candidate (sH, sL)."""
    pr = prims(r)
    tot = mpf(0)
    for x in range(-XMAX, XMAX + 1):
        mu = direct_posterior(sH, sL, x)
        e = entry(r, cH, mu)
        price = pr["t0"] + e * (pr["tL"] - pr["t0"] + pr["DT"] * mu)
        tth = pr["tH"] if theta == "H" else pr["tL"]
        value = pr["t0"] + e * (tth - pr["t0"])
        tot += pmf(x - q) * q * (value - price)
    return tot - K_COST * abs(q)


def direct_entry_own(r, cH, sH, sL):
    """Entry probability and high-class ownership by direct sums."""
    E = mpf(0)
    OH = mpf(0)
    for x in range(-XMAX, XMAX + 1):
        mu = direct_posterior(sH, sL, x)
        e = entry(r, cH, mu)
        pH, pL = lik(sH, x), lik(sL, x)
        E += e * (pH + pL) / 2
        OH += e * pH / 2
    return E, OH


# ------------------------------------------------------------- region algebra
ALPHA = A / (1 + A)          # P(Z >= 1)
BETA = 1 / (1 + A)           # P(Z >= 0)
GAMMA = (1 - A) / (1 + A)    # P(Z = 0)
DELTA = A ** 2 / (1 + A)     # P(Z >= 2)
PHI = A * (1 - A) / (1 + A)  # P(Z = 1)
MASS = {1: (BETA, PHI, DELTA), 0: (ALPHA, GAMMA, ALPHA), -1: (DELTA, PHI, BETA)}
R_UP = (1 / A, A, A)    # f(x-1)/f(x) on regions x>=1, x=0, x<=-1
R_DN = (A, A, 1 / A)    # f(x+1)/f(x) on the same regions
m1 = A / (1 + A)
M1 = 1 / (1 + A)
m = A ** 2 / (1 + A ** 2)
M = 1 / (1 + A ** 2)


def sig(um, u0, up):
    return {-1: mpf(um), 0: mpf(u0), 1: mpf(up)}


def region_post(sH, sL, pi=HALF):
    out = []
    for i in range(3):
        lh = sH[0] + sH[1] * R_UP[i] + sH[-1] * R_DN[i]
        ll = sL[0] + sL[1] * R_UP[i] + sL[-1] * R_DN[i]
        out.append(pi * lh / (pi * lh + (1 - pi) * ll))
    return out


def region_payoffs(r, cH, mus, es=None):
    """Payoffs of every order for both types against a schedule on the three regions."""
    pr = prims(r)
    if es is None:
        es = [entry(r, cH, mu) for mu in mus]
    out = {}
    for q in ORDERS:
        gh = sum(MASS[q][i] * es[i] * (1 - mus[i]) for i in range(3)) * pr["DT"]
        gl = sum(MASS[q][i] * es[i] * mus[i] for i in range(3)) * pr["DT"]
        out[("H", q)] = q * gh - K_COST * abs(q)
        out[("L", q)] = -q * gl - K_COST * abs(q)
    return out


def uv(u, v):
    u, v = mpf(u), mpf(v)
    return sig(0, 1 - u, u), sig(v, 1 - v, 0)


def post_uv(u, v):
    sH, sL = uv(u, v)
    return region_post(sH, sL)


def gains_uv(r, cH, u, v, es=None):
    """Gross gains G_H (unit buy) and G_L (unit sale) at candidate (u, v)."""
    pr = prims(r)
    mus = post_uv(u, v)
    if es is None:
        es = [entry(r, cH, mu) for mu in mus]
    gh = pr["DT"] * sum(MASS[1][i] * es[i] * (1 - mus[i]) for i in range(3))
    gl = pr["DT"] * sum(MASS[-1][i] * es[i] * mus[i] for i in range(3))
    return gh, gl, mus, es


def bisect(fn, lo, hi, it=220):
    flo = fn(lo)
    for _ in range(it):
        mid = (lo + hi) / 2
        fm = fn(mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


print("=" * 78)
print("A. Posteriors by direct convolution (claim 1)")
print("=" * 78)
print("a =", s(A, 20), "  d = 1-a =", s(D, 20))
cases = {
    "full (1,-1)": (sig(0, 0, 1), sig(1, 0, 0)),
    "buy only (1,0)": (sig(0, 0, 1), sig(0, 1, 0)),
    "sell only (0,-1)": (sig(0, 1, 0), sig(1, 0, 0)),
    "none (0,0)": (sig(0, 1, 0), sig(0, 1, 0)),
    "mixed, wrong orders 1": (sig("0.2", "0.3", "0.5"), sig("0.6", "0.1", "0.3")),
    "mixed, wrong orders 2": (sig("0.7", "0.2", "0.1"), sig("0.05", "0.15", "0.8")),
    "mixed, wrong orders 3": (sig("0.15", "0.45", "0.4"), sig("0.35", "0.6", "0.05")),
}
for name, (sH, sL) in cases.items():
    vals = {x: direct_posterior(sH, sL, x) for x in range(-12, 13)}
    up = [vals[x] for x in range(1, 13)]
    dn = [vals[x] for x in range(-12, 0)]
    reg = region_post(sH, sL)
    print(f"{name:24s} mu(x>=1) in [{s(min(up))}, {s(max(up))}] spread {s(max(up) - min(up), 3)}")
    print(f"{'':24s} mu(0) = {s(vals[0])};  mu(x<=-1) in [{s(min(dn))}, {s(max(dn))}] spread {s(max(dn) - min(dn), 3)}")
    print(f"{'':24s} region formula minus direct: "
          f"{s(reg[0] - vals[5], 3)}, {s(reg[1] - vals[0], 3)}, {s(reg[2] - vals[-5], 3)}")
sH, sL = cases["full (1,-1)"]
print("Full orders: M =", s(M, 15), " m =", s(m, 15))
print("  M - 1/(1+e^(-2/b)) =", s(M - 1 / (1 + exp(-2 / B_SCALE)), 3),
      "  m - 1/(1+e^(2/b)) =", s(m - 1 / (1 + exp(2 / B_SCALE)), 3))
worst = mpf(0)
for x in range(-12, 13):
    paper = 1 / (1 + exp(-(abs(x + 1) - abs(x - 1)) / B_SCALE))   # paper eq. (A.8)
    worst = max(worst, abs(paper - direct_posterior(sH, sL, x)))
print("  max |discrete posterior - paper eq. (A.8)| over integers -12..12 =", s(worst, 3))
print("General prior pi = 0.3, full orders, posteriors by region:",
      [s(v) for v in region_post(sH, sL, pi=mpf("0.3"))])
print("  direct at x = 4, 0, -4:", [s(direct_posterior(sH, sL, x, pi=mpf("0.3"))) for x in (4, 0, -4)])

# Bounds over a simplex grid of strategies (wrong-signed orders included).
grid = []
n = 10
for i in range(n + 1):
    for j in range(n + 1 - i):
        grid.append(sig(mpf(i) / n, mpf(n - i - j) / n, mpf(j) / n))
lo, hi = mpf(1), mpf(0)
argl = argh = None
for sH_ in grid:
    for sL_ in grid:
        for i, mu in enumerate(region_post(sH_, sL_)):
            if mu < lo:
                lo, argl = mu, (sH_, sL_, i)
            if mu > hi:
                hi, argh = mu, (sH_, sL_, i)
print(f"Bounds over {len(grid)}^2 strategy pairs: min mu = {s(lo)}, max mu = {s(hi)}")
print("  attained at sigma_H, sigma_L, region =",
      [s(argh[0][q], 3) for q in ORDERS], [s(argh[1][q], 3) for q in ORDERS], argh[2],
      "| min:", [s(argl[0][q], 3) for q in ORDERS], [s(argl[1][q], 3) for q in ORDERS], argl[2])

print()
print("=" * 78)
print("B. Region masses: closed forms against summed pmf")
print("=" * 78)
summ = lambda lo_, hi_: sum(pmf(z) for z in range(lo_, hi_ + 1))
for name, val, chk in (("alpha=P(Z>=1)", ALPHA, summ(1, XMAX)), ("beta=P(Z>=0)", BETA, summ(0, XMAX)),
                       ("gamma=P(Z=0)", GAMMA, pmf(0)), ("delta=P(Z>=2)", DELTA, summ(2, XMAX)),
                       ("phi=P(Z=1)", PHI, pmf(1))):
    print(f"  {name:15s} {s(val, 15)}  closed - summed = {s(val - chk, 3)}")
print("  m1 =", s(m1), " M1 =", s(M1), " m =", s(m), " M =", s(M))

print()
print("=" * 78)
print("C. Coefficients (gains are Delta_T times these)")
print("=" * 78)
J1, J2 = BETA * m, DELTA * M
cT = J1 * (1 + RHO) + PHI * RHO / 2
cconst = RHO * (BETA * m + PHI / 2 + DELTA * M)
Pplus = (BETA + DELTA) / 2
print("  beta*m =", s(J1, 15), " delta*M =", s(J2, 15), " diff =", s(J1 - J2, 3))
print("  full trade, entry (1,rho,rho): c_T =", s(cT, 15))
print("  full trade, entry rho everywhere:", s(cconst, 15), " (/rho =", s(cconst / RHO, 15), ")")
print("  no trade, entry rho: rho/2 =", s(RHO / 2))
print("  recruitment adds (1-rho)*J =", s((1 - RHO) * J1, 15))
print("  P(X>=1) under full orders =", s(Pplus, 15), "  closed form (1+a^2)/(2(1+a)) =",
      s((1 + A ** 2) / (2 * (1 + A)), 15))
E_T = RHO + (1 - RHO) * Pplus
OH_T = (RHO + (1 - RHO) * BETA) / 2
print("  full-trade entry E =", s(E_T, 15), "  ownership O_H =", s(OH_T, 15))
cBNS_H = ALPHA * BETA * (1 + RHO)
cBNS_L = DELTA * M1 + RHO * m1 * (PHI + BETA)
cSNB_L = ALPHA * BETA * (1 + RHO)
cSNB_H = (BETA + PHI) * m1 + DELTA * RHO * BETA
print("  BNS (1,0) with recruitment: H coef", s(cBNS_H, 15), " L-deviation coef", s(cBNS_L, 15))
print("    gap", s(cBNS_H - cBNS_L, 15), "  (1-a)alpha(beta-rho alpha) =",
      s(D * ALPHA * (BETA - RHO * ALPHA), 15))
print("  SNB (0,1) with recruitment at + and 0: L coef", s(cSNB_L, 15), " H-deviation coef", s(cSNB_H, 15))
print("    gap H-L", s(cSNB_H - cSNB_L, 15), "  (1-a)alpha(alpha-rho beta) =",
      s(D * ALPHA * (ALPHA - RHO * BETA), 15), "  a - rho =", s(A - RHO, 6))
cBNS0_H = 2 * RHO * ALPHA * BETA
cBNS0_L = RHO * (DELTA * M1 + (PHI + BETA) * m1)
print("  BNS/SNB at constant entry: trader coef", s(cBNS0_H, 15), " deviation coef", s(cBNS0_L, 15))

# Cross-check the region gains with direct sums at r = 1.55, c_H = 6.
print("  cross-check at r=1.55, c_H=6 (region minus direct, full orders and (1,0)):")
for name, (u_, v_) in (("(1,1)", (1, 1)), ("(1,0)", (1, 0)), ("(0.4,0.7)", ("0.4", "0.7"))):
    sH, sL = uv(u_, v_)
    rp = region_payoffs(mpf("1.55"), mpf(6), region_post(sH, sL))
    dH = direct_payoff(mpf("1.55"), mpf(6), sH, sL, "H", 1)
    dL = direct_payoff(mpf("1.55"), mpf(6), sH, sL, "L", -1)
    print(f"    {name}: H buy {s(rp[('H', 1)] - dH, 3)}, L sell {s(rp[('L', -1)] - dL, 3)}")

print()
print("=" * 78)
print("D. Auction primitives (memo section 5 table)")
print("=" * 78)
for r in ("1.2", "1.55", "3", "3.6"):
    r = mpf(r)
    pr = prims(r)
    print(f"  r={s(r, 4):5s} DT={s(pr['DT'], 8)} B(1/2)={s(Bval(r, HALF), 8)} B(M1)={s(Bval(r, M1), 8)} "
          f"B(M)={s(Bval(r, M), 8)} tau5={s(tau(r, 5), 8)} tau6={s(tau(r, 6), 8)}")

print()
print("=" * 78)
print("E. c_H window and ceilings (claim 3)")
print("=" * 78)
r0, r1, r2 = mpf("1.2"), mpf(3), mpf("3.6")
print("  B_r0(1/2) =", s(Bval(r0, HALF), 15), "  B_r1(M) =", s(Bval(r1, M), 15),
      "  B_r1(M1) =", s(Bval(r1, M1), 15))
print("  two-sided window width - buy-only width =", s(Bval(r1, M) - Bval(r1, M1), 10))


def ceiling(cH, top):
    q = top * H_VAL - cH
    return (q + sqrt(q ** 2 + top * ((1 - top) * ELL ** 2 - P_RES ** 2))) / top


for cH in (mpf(5), mpf(6)):
    rc = ceiling(cH, M)
    rb = ceiling(cH, M1)
    print(f"  c_H={s(cH, 2)}: r_C (B_r(M)=c_H) = {s(rc, 15)}  residual B-c_H = {s(Bval(rc, M) - cH, 3)}")
    print(f"         buy-only ceiling (B_r(M1)=c_H) = {s(rb, 15)}  residual = {s(Bval(rb, M1) - cH, 3)}")
print("  paper r_C (c_H=6) printed 3.592658519; discrete minus printed =",
      s(ceiling(mpf(6), M) - mpf("3.592658519"), 3))
print("  B_1(M1) =", s(Bval(mpf(1), M1), 12), "  B_(1+1e-6)(M1) =", s(Bval(1 + mpf("1e-6"), M1), 12))

print()
print("=" * 78)
print("F. Thresholds in r (k = 0.02)")
print("=" * 78)
thr = {
    "r_N = rr(2k/rho) (no-trade existence)": rr(2 * K_COST / RHO),
    "rr(k) (sufficient no-trade uniqueness)": rr(K_COST),
    "paper r_U = rr(k/((1-1/b) rho m))": rr(K_COST / ((1 - 1 / B_SCALE) * RHO * m)),
    "discrete rr(k/(rho m)) (sufficient full uniqueness)": rr(K_COST / (RHO * m)),
    "full-trade existence rr(k/c_T)": rr(K_COST / cT),
    "BNS recruited, lower end rr(k/cBNS_H)": rr(K_COST / cBNS_H),
    "BNS recruited, upper end rr(k/cBNS_L)": rr(K_COST / cBNS_L),
    "BNS/SNB constant entry, lower end": rr(K_COST / cBNS0_H),
    "BNS/SNB constant entry, upper end": rr(K_COST / cBNS0_L),
    "full trade at constant entry exists above": rr(K_COST / cconst),
}
for name, val in thr.items():
    print(f"  {name:52s} {s(val, 13)}")
print("  paper printed r_N = 1.747877538; discrete minus printed =", s(thr["r_N = rr(2k/rho) (no-trade existence)"] - mpf("1.747877538"), 3))
print("  paper printed rr(k) = 1.220997512; discrete minus printed =", s(rr(K_COST) - mpf("1.220997512"), 3))
print("  paper printed r_U = 2.837416964; formula minus printed =", s(thr["paper r_U = rr(k/((1-1/b) rho m))"] - mpf("2.837416964"), 3))

print()
print("=" * 78)
print("G. Proposition 2 analog at the benchmark (claim 2) and claim 8")
print("=" * 78)
print("  DT(r0) =", s(prims(r0)["DT"], 12), "  rho m DT(r1) =", s(RHO * m * prims(r1)["DT"], 12),
      "  (1-1/b) rho m DT(r1) =", s((1 - 1 / B_SCALE) * RHO * m * prims(r1)["DT"], 12))
sH, sL = uv(1, 1)
mus = region_post(sH, sL)
for cH in (5, 6):
    es = [entry(r1, cH, mu) for mu in mus]
    pr = prims(r1)
    prices = [pr["t0"] + es[i] * (pr["tL"] - pr["t0"] + pr["DT"] * mus[i]) for i in range(3)]
    print(f"  c_H={cH}, r1, full orders: entry by region {[s(e, 4) for e in es]}, prices {[s(x, 8) for x in prices]}")
print("  t0, tL, tH at r1:", s(prims(r1)["t0"], 8), s(prims(r1)["tL"], 8), s(prims(r1)["tH"], 8))
for cH in (5, 6):
    for r in (r0, r1, r2):
        if r == r0:
            sH, sL = uv(0, 0)
        else:
            sH, sL = uv(1, 1)
        E, OH = direct_entry_own(r, cH, sH, sL)
        print(f"  c_H={cH} r={s(r, 3)}: E = {s(E, 10)}, O_H = {s(OH, 10)}")
sH, sL = uv(1, 0)
for cH in (5, 6):
    E, OH = direct_entry_own(r1, cH, sH, sL)
    print(f"  buy-only full buying at r1, c_H={cH}: E = {s(E, 10)}, O_H = {s(OH, 10)}")
# Net gains at r1.
pr = prims(r1)
print("  r1 full trade net with recruitment:", s(cT * pr["DT"] - K_COST, 10),
      " with entry rho everywhere:", s(cconst * pr["DT"] - K_COST, 10))
print("  r1 buy-only net with recruitment:", s(cBNS_H * pr["DT"] - K_COST, 10),
      " with entry rho everywhere:", s(cBNS0_H * pr["DT"] - K_COST, 10))
dL = direct_payoff(r1, mpf(5), *uv(1, 0), "L", -1)
print("  r1, c_H=5, candidate (1,0): L's sale earns (direct sum)", s(dL, 10))
dL6 = direct_payoff(r1, mpf(6), *uv(1, 0), "L", -1)
print("  r1, c_H=6, candidate (1,0): L's sale earns (direct sum)", s(dL6, 10))

# Brute-force illustration of uniqueness over a strategy grid (wrong-signed orders included).
for label, r in (("r0", r0), ("r1", r1)):
    worst_nonzero = mpf(-10)
    worst_margin = mpf(10)
    for sH_ in grid:
        for sL_ in grid:
            mus_ = region_post(sH_, sL_)
            for cH in (5, 6):
                pay = region_payoffs(r, cH, mus_)
                if label == "r0":
                    worst_nonzero = max(worst_nonzero, pay[("H", 1)], pay[("H", -1)], pay[("L", 1)], pay[("L", -1)])
                else:
                    worst_margin = min(worst_margin, pay[("H", 1)] - max(mpf(0), pay[("H", -1)]),
                                       pay[("L", -1)] - max(mpf(0), pay[("L", 1)]))
    if label == "r0":
        print(f"  r0: best nonzero order payoff over all {len(grid)}^2 candidates and both c_H = {s(worst_nonzero, 8)}")
    else:
        print(f"  r1: least margin of the correct order over every other order = {s(worst_margin, 8)}")

print()
print("=" * 78)
print("H. Coexistence nets (claim 4)")
print("=" * 78)
for r in ("1.515898", "1.55", "1.6", "1.65", "1.747878"):
    r = mpf(r)
    DT = prims(r)["DT"]
    print(f"  r={s(r, 8)}: DT={s(DT, 8)}  NT net = {s(RHO * DT / 2 - K_COST, 6)}  T net = {s(cT * DT - K_COST, 6)}"
          f"  B(1/2)={s(Bval(r, HALF), 6)}  B(M)={s(Bval(r, M), 6)}")
for r in ("1.55", "1.6", "1.65"):
    for cH in (5, 6):
        r_ = mpf(r)
        nt = direct_payoff(r_, mpf(cH), *uv(0, 0), "H", 1)
        t_h = direct_payoff(r_, mpf(cH), *uv(1, 1), "H", 1)
        t_l = direct_payoff(r_, mpf(cH), *uv(1, 1), "L", -1)
        print(f"  direct sums r={r} c_H={cH}: NT buy deviation {s(nt, 8)}; T: H {s(t_h, 8)}, L {s(t_l, 8)}")

print()
print("=" * 78)
print("I. Paper Laplace values for comparison (eq. 12, eq. A.14)")
print("=" * 78)
for cH in (5, 6):
    t_ = tau(r1, cH)
    xs = B_SCALE / 2 * log(t_ / (1 - t_))
    aH = 1 - exp((xs - 1) / B_SCALE) / 2
    aL = exp(-(xs + 1) / B_SCALE) / 2
    print(f"  c_H={cH}: tau={s(t_, 8)} x*={s(xs, 8)} E={s(RHO + (1 - RHO) / 2 * (aH + aL), 8)} "
          f"O_H={s((RHO + (1 - RHO) * aH) / 2, 8)}")
print("  eq. (A.14) limit at r_C:", s(RHO + (1 - RHO) / 4 * (1 + exp(-2 / B_SCALE)), 8))

print()
print("=" * 78)
print("J. Narrow branch (1, v(r)) with entry (1, rho, rho) (claim 6)")
print("=" * 78)
es_rec = [mpf(1), RHO, RHO]
es_const = [RHO, RHO, RHO]


def gl_rec(r, v):
    return gains_uv(r, None, 1, v, es=es_rec)[1]


def gh_rec(r, v):
    return gains_uv(r, None, 1, v, es=es_rec)[0]


# With w = v d: (1+a)/a * dG_L/dw / DT = a^2/(1+a-aw)^2 + e0 a d/(1+a-w)^2 - e0 a/(a^2+a+w)^2,
# where e0 = rho in pattern (1,rho,rho) and the factor e+ = 1 multiplies the first term;
# in the constant pattern every term carries rho. The derivative rises in w, so its sign at w = 0
# (times (1+a)^2) decides monotonicity on the whole edge.
print("  pattern (1,rho,rho): slope at v=0 times (1+a)^2 = a^2 + rho a d - rho/a =",
      s(A ** 2 + RHO * A * D - RHO / A, 10), " (positive => G_L(1,v) rises in v)")
print("  constant entry: slope sign at v=0, a^2 + a d - 1/a =", s(A ** 2 + A * D - 1 / A, 10),
      "; at v=1, d(1/(4a) - a/(1+a^2)^2) =", s(D * (1 / (4 * A) - A / (1 + A ** 2) ** 2), 10))
for vv in ("0", "0.2", "0.4", "0.6", "0.8", "0.9", "1"):
    g = gains_uv(mpf(2), None, 1, mpf(vv), es=es_const)
    print(f"    constant entry, u=1, v={vv}: G_L/(rho DT) = {s(g[1] / (RHO * prims(2)['DT']), 10)}"
          f"  G_H/(rho DT) = {s(g[0] / (RHO * prims(2)['DT']), 10)}")
for r in ("1.520", "1.525", "1.530"):
    r = mpf(r)
    vv = bisect(lambda v: gl_rec(r, v) - K_COST, mpf(0), mpf(1))
    P_ = (BETA + (1 - vv) * ALPHA + vv * DELTA) / 2
    mup = post_uv(1, vv)[0]
    print(f"  r={s(r, 5)}: v={s(vv, 10)} E={s(RHO + (1 - RHO) * P_, 10)} O_H={s((RHO + (1 - RHO) * BETA) / 2, 10)}"
          f"  H net={s(gh_rec(r, vv) - K_COST, 6)}  mu+={s(mup, 8)} tau6={s(tau(r, 6), 8)} tau5={s(tau(r, 5), 8)}")


def v_tau(r, cH):
    t_ = tau(r, cH)
    return (1 - (1 - t_) / (A * t_)) / D


r_up6 = bisect(lambda r: gl_rec(r, v_tau(r, 6)) - K_COST, mpf("1.516"), mpf("1.5338"))
print("  c_H=6 upper end (root meets mu+ = tau): r =", s(r_up6, 12), " v =", s(v_tau(r_up6, 6), 10))
print("  c_H=5 upper end (root reaches v=0): r =", s(rr(K_COST / cBNS_L), 12))

print()
print("=" * 78)
print("K. Challenger-mixing points at r = 1.55, 1.60, 1.65 (claims 6, 7)")
print("=" * 78)
for r in ("1.55", "1.6", "1.65"):
    r = mpf(r)
    pr = prims(r)
    DT = pr["DT"]
    # c_H = 6, edge u = 1, mu+ = tau.
    t6 = tau(r, 6)
    vs = v_tau(r, 6)
    mus = post_uv(1, vs)
    eL = (K_COST / DT - RHO * (PHI * mus[1] + BETA * mus[2])) / (DELTA * mus[0])
    ghn = DT * (BETA * eL * (1 - mus[0]) + RHO * PHI * (1 - mus[1]) + RHO * DELTA * (1 - mus[2])) - K_COST
    P_ = (BETA + (1 - vs) * ALPHA + vs * DELTA) / 2
    E6 = RHO + (eL - RHO) * P_
    # Mirror point (u*, 1) for c_H = 6.
    us = (A / D) * (t6 * A / (1 - t6) - 1)
    musm = post_uv(us, 1)
    eH = (K_COST / DT - RHO * (PHI * (1 - musm[1]) + DELTA * (1 - musm[2]))) / (BETA * (1 - musm[0]))
    gln = DT * (DELTA * eH * musm[0] + RHO * PHI * musm[1] + RHO * BETA * musm[2]) - K_COST
    # c_H = 5, edge v = 0, mu+ = tau.
    t5 = tau(r, 5)
    up = A * (2 * t5 - 1) / (D * (1 - t5))
    mus5 = post_uv(up, 0)
    eH5 = (K_COST / DT - RHO * (PHI * (1 - mus5[1]) + DELTA * (1 - mus5[2]))) / (BETA * (1 - mus5[0]))
    gln5 = DT * (DELTA * eH5 * mus5[0] + RHO * PHI * mus5[1] + RHO * BETA * mus5[2]) - K_COST
    P5 = ((1 - up) * ALPHA + up * BETA + ALPHA) / 2
    E5 = RHO + (eH5 - RHO) * P5
    print(f"  r={s(r, 4)} c_H=6 (1,v*): v*={s(vs, 9)} mu+={s(mus[0], 8)} mu0={s(mus[1], 6)} e_L*={s(eL, 9)} "
          f"H net={s(ghn, 6)} E={s(E6, 9)}")
    print(f"           mirror (u*,1): u*={s(us, 9)} mu0={s(musm[1], 6)} e_H*={s(eH, 9)} L net at e_H*={s(gln, 6)}")
    print(f"         c_H=5 (u_p,0): u_p={s(up, 9)} e_H*={s(eH5, 9)} L net={s(gln5, 6)} E={s(E5, 9)}")

print()
print("=" * 78)
print("L. Baseline-tie equilibria that memo C1 does not report (50-digit direct sums)")
print("=" * 78)
print("  Entry uses the actual posteriors and the prepare-at-indifference rule. Payoffs are")
print("  direct sums over flows; an equilibrium needs: a mixing type at zero net, a type at a")
print("  full order with net >= 0, an abstaining type with net <= 0 for both orders.")


def report(label, r, cH, u, v):
    sH, sL = uv(u, v)
    mus = region_post(sH, sL)
    es = [entry(r, cH, mu) for mu in mus]
    pay = {(th, q): direct_payoff(r, cH, sH, sL, th, q) for th, q in (("H", 1), ("H", -1), ("L", -1), ("L", 1))}
    E, OH = direct_entry_own(r, cH, sH, sL)
    print(f"  {label}: r={s(r, 10)} c_H={cH} u={s(u, 10)} v={s(v, 10)}")
    print(f"     posteriors {[s(x, 8) for x in mus]} tau={s(tau(r, cH), 8)} entry {[s(x, 3) for x in es]}")
    print(f"     H: buy {s(pay[('H', 1)], 6)}, sell {s(pay[('H', -1)], 6)};  L: sell {s(pay[('L', -1)], 6)}, "
          f"buy {s(pay[('L', 1)], 6)};  E={s(E, 9)} O_H={s(OH, 9)}")


# 1. c_H = 5, partial buys, no sales, recruitment at + (H indifferent).
r = mpf("1.42")
t5 = tau(r, 5)
u_lo = A * (2 * t5 - 1) / (D * (1 - t5))
uu = bisect(lambda u: gains_uv(r, None, u, 0, es=es_rec)[0] - K_COST, u_lo + mpf("1e-30"), mpf(1))
report("PB-NS with recruitment", r, 5, uu, 0)
# 2-3. c_H = 6, constant entry, full buys and partial sales, and its mirror.
r = mpf("1.825")
vv = bisect(lambda v: gains_uv(r, None, 1, v, es=es_const)[1] - K_COST, mpf(0), v_tau(r, 6))
report("FB-PS at constant entry", r, 6, 1, vv)
report("mirror PB-FS at constant entry", r, 6, vv, 1)
# 4-5. symmetric interior points at constant entry.
for r, cH in ((mpf("1.78"), 6), (mpf("1.755"), 5)):
    ss = bisect(lambda x: gains_uv(r, None, x, x, es=es_const)[0] - K_COST, mpf(0), mpf("0.9"))
    report("symmetric interior at constant entry", r, cH, ss, ss)
# 6. c_H = 6, constant entry, partial buys, no sales.
r = mpf("1.77")
uu = bisect(lambda u: gains_uv(r, None, u, 0, es=es_const)[0] - K_COST, mpf("0.2"), mpf(1))
report("PB-NS at constant entry", r, 6, uu, 0)
# 7. c_H = 6, asymmetric interior point at constant entry (both types mix).
u7 = mpf("0.1")
v7 = bisect(lambda v: (lambda g: g[0] - g[1])(gains_uv(mpf(2), None, u7, v, es=es_const)[:2]),
            mpf("0.2"), mpf("0.35"))
g7 = gains_uv(mpf(2), None, u7, v7, es=es_const)[0] / (RHO * prims(2)["DT"])
r7 = rr(K_COST / (RHO * g7))
report("asymmetric interior at constant entry", r7, 6, u7, v7)
