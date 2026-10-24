# Independent print-only check of the costly-acquisition memo (C6).
# Auction objects and equal noise use exact fractions.
# Discrete-Laplace calculations use 50-digit arithmetic and direct sums over integer flows.
# Run: .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/X_C6_check/check.py
from fractions import Fraction as F
import mpmath as mp

mp.mp.dps = 50
NFL = 300                       # flows |z| <= NFL in the direct sums
TOL = mp.mpf(10) ** -40         # numerical tie tolerance: "prepares at a tie"

H, ELL, PR = F(10), F(1), F(1, 2)
RHO, KTR, PI, BN = F(1, 4), F(1, 50), F(1, 2), 2
CH5, CH6 = F(5), F(6)


def mpf(x):
    if isinstance(x, F):
        return mp.mpf(x.numerator) / mp.mpf(x.denominator)
    return mp.mpf(x)


def hd(title):
    print()
    print("=" * 100)
    print(title)
    print("=" * 100)


def nf(x, d=15):
    return mp.nstr(x, d)


# ---------------------------------------------------------------- auction objects
def unif_mean(fn, r):
    """Exact mean of a function that is linear between the breakpoints 0, p, l, r (evaluate at midpoints)."""
    pts = [F(0), PR, ELL, F(r)]
    tot = F(0)
    for u0, u1 in zip(pts[:-1], pts[1:]):
        tot += fn((u0 + u1) / 2) * (u1 - u0)
    return tot / F(r)


def auction_closed(r):
    r = F(r)
    t0 = PR * (1 - PR / r)
    tH = r / 2 + PR ** 2 / (2 * r)
    tL = ELL - (ELL ** 2 - PR ** 2) / (2 * r)
    gH = H - r / 2 - PR ** 2 / (2 * r)
    gL = (ELL ** 2 - PR ** 2) / (2 * r)
    return dict(r=r, t0=t0, tH=tH, tL=tL, gH=gH, gL=gL, DT=(r - ELL) ** 2 / (2 * r), wL=tL - t0)


def auction_direct(r):
    """Same objects from the second-price rules, by exact integration over R ~ U[0, r]."""
    r = F(r)
    t0 = unif_mean(lambda u: PR if u >= PR else F(0), r)            # reserve paid if R >= p
    tH = unif_mean(lambda u: max(PR, u), r)                         # high challenger pays max(p, R)
    tL = unif_mean(lambda u: max(PR, min(u, ELL)), r)               # low challenger: target gets max(p, min(R, l))
    gH = unif_mean(lambda u: max(H - max(PR, u), F(0)), r)
    gL = unif_mean(lambda u: max(ELL - max(PR, u), F(0)), r)
    return dict(r=r, t0=t0, tH=tH, tL=tL, gH=gH, gL=gL, DT=tH - tL, wL=tL - t0)


def Bf(au, mu):
    return au["gL"] + mu * (au["gH"] - au["gL"])


def tau_of(au, cH):
    return (cH - au["gL"]) / (au["gH"] - au["gL"])


def au_mp(au):
    return {k: mpf(v) for k, v in au.items()}


# ---------------------------------------------------------------- discrete Laplace noise
class DL:
    def __init__(self, b=BN):
        self.a = mp.exp(-mp.mpf(1) / b)
        self.d = 1 - self.a
        self.c0 = (1 - self.a) / (1 + self.a)
        self.pw = [self.a ** i for i in range(NFL + 6)]
        self.m = self.a / (1 + self.a)
        self.M = 1 / (1 + self.a)

    def n(self, z):
        return self.c0 * self.pw[abs(z)]

    def tail(self):          # P(|Z| > NFL)
        return 2 * self.a ** (NFL + 1) / (1 + self.a)


PIm, RHOm, KTRm = mpf(PI), mpf(RHO), mpf(KTR)


def post_flow(dl, s, x, pi=None):
    """Posterior at flow x from the flow laws: class H buys with probability s, class L never buys."""
    pi = PIm if pi is None else pi
    fH = (1 - s) * dl.n(x) + s * dl.n(x - 1)
    fL = dl.n(x)
    return pi * fH / (pi * fH + (1 - pi) * fL)


def entry_from_mu(aum, cH, mu):
    return RHOm + (1 - RHOm) * (1 if Bf(aum, mu) >= mpf(cH) - TOL else 0)


def brute_D(dl, au, cH, s, who="H", force_e=None):
    """Gross return of one purchase, summed over integer flows x = 1 + z, |z| <= NFL."""
    aum = au_mp(au)
    tot = mp.mpf(0)
    for z in range(-NFL, NFL + 1):
        x = 1 + z
        mu = post_flow(dl, s, x)
        e = entry_from_mu(aum, cH, mu) if force_e is None else force_e
        price = aum["t0"] + e * (aum["wL"] + aum["DT"] * mu)
        ev = aum["t0"] + e * (aum["wL"] + (aum["DT"] if who == "H" else 0))
        tot += dl.n(z) * (ev - price)
    return tot


def closed_D(dl, au, cH, s):
    """Two-region closed form derived independently (regions x <= 0 and x >= 1)."""
    aum = au_mp(au)
    a, d = dl.a, dl.d
    y = PIm * d * s
    mum = PIm * (1 - d * s) / (1 - y)
    mup = PIm * (a + d * s) / (a + y)
    em = entry_from_mu(aum, cH, mum)
    ep = entry_from_mu(aum, cH, mup)
    C = aum["DT"] * (1 - PIm) * a / (1 + a)
    return C * (em / (1 - y) + ep / (a + y)), mum, mup, em, ep


def find_sE(dl, au, cH):
    """Smallest s with posterior at flow x=1 reaching the entry threshold (bisection on flow-level Bayes)."""
    tau = mpf(tau_of(au, cH))
    if post_flow(dl, mp.mpf(1), 1) < tau - TOL:
        return None, tau
    lo, hi = mp.mpf(0), mp.mpf(1)
    for _ in range(170):
        mid = (lo + hi) / 2
        if post_flow(dl, mid, 1) >= tau:
            hi = mid
        else:
            lo = mid
    return hi, tau


def vcut(dl, au, cH, s):
    D = closed_D(dl, au, cH, s)[0]
    return PIm * (D - KTRm)


def solve_psi(dl, au, cH, kappa):
    """All equilibrium acquisition probabilities. Scan on a grid, then refine by bisection on each smooth branch."""
    kap = mpf(kappa)
    sE, tau = find_sE(dl, au, cH)

    def G(s):
        D = closed_D(dl, au, cH, s)[0]
        return PIm * max(D - KTRm, 0) - kap

    out = []
    if G(mp.mpf(0)) <= TOL:
        out.append(("corner0", mp.mpf(0)))
    if G(mp.mpf(1)) >= -TOL:
        out.append(("corner1", mp.mpf(1)))
    grid = [mp.mpf(i) / 2000 for i in range(0, 2001)]
    if sE is not None and 0 < sE < 1:
        grid = sorted(set(grid + [sE, sE - mp.mpf(10) ** -30]))
    jump_lo = (sE - mp.mpf(10) ** -30) if (sE is not None and 0 < sE < 1) else None
    for s0, s1 in zip(grid[:-1], grid[1:]):
        if jump_lo is not None and s0 == jump_lo:
            continue                      # bracket across the entry jump: not a root of a continuous branch
        g0, g1 = G(s0), G(s1)
        if g0 > 0 >= g1:
            lo, hi = s0, s1
            for _ in range(160):
                mid = (lo + hi) / 2
                if G(mid) > 0:
                    lo = mid
                else:
                    hi = mid
            root = (lo + hi) / 2
            if 0 < root < 1:
                out.append(("interior", root))
    # root exactly at the entry threshold (tie rule gives entry): G(sE) == 0 within tolerance
    if sE is not None and 0 < sE < 1 and abs(G(sE)) < TOL:
        out.append(("interior_at_sE", sE))
    return out, sE, tau


def outcomes(dl, au, cH, s):
    """Entry and high-class ownership from flow laws (direct sums over |x| <= NFL)."""
    aum = au_mp(au)
    E = mp.mpf(0)
    OH = mp.mpf(0)
    for x in range(-NFL, NFL + 2):
        fH = (1 - s) * dl.n(x) + s * dl.n(x - 1)
        fL = dl.n(x)
        mu = PIm * fH / (PIm * fH + (1 - PIm) * fL)
        e = entry_from_mu(aum, cH, mu)
        E += (PIm * fH + (1 - PIm) * fL) * e
        OH += PIm * fH * e
    return E, OH


def welfare(dl, au, cH, psi, kappa, xi):
    """Total surplus from first principles: allocation value less preparation, research and (if a resource) trade cost."""
    r = au["r"]
    aum = au_mp(au)
    V0 = mpf(unif_mean(lambda u: u if u >= PR else F(0), r))
    Vh = mpf(unif_mean(lambda u: max(u, H), r))
    Vl = mpf(unif_mean(lambda u: max(u, ELL), r))
    s = psi
    tot = mp.mpf(0)
    for x in range(-NFL, NFL + 2):
        fH = (1 - s) * dl.n(x) + s * dl.n(x - 1)
        fL = dl.n(x)
        mu = PIm * fH / (PIm * fH + (1 - PIm) * fL)
        hi = 1 if Bf(aum, mu) >= mpf(cH) - TOL else 0
        e = RHOm + (1 - RHOm) * hi
        tot += PIm * fH * (e * Vh + (1 - e) * V0) + (1 - PIm) * fL * (e * Vl + (1 - e) * V0)
        tot -= (PIm * fH + (1 - PIm) * fL) * (1 - RHOm) * hi * mpf(cH)
    tot -= psi * mpf(kappa) + xi * PIm * psi * KTRm
    return tot


def memo_dW(dl, au, cH, psi, kappa, xi):
    """Closed form for the welfare change at positive research above the entry threshold (my derivation)."""
    aum = au_mp(au)
    a, d = dl.a, dl.d
    y = PIm * d * psi
    Qp = (a + y) / (1 + a)
    mup = PIm * (a + d * psi) / (a + y)
    hi = 1 if Bf(aum, mup) >= mpf(cH) - TOL else 0
    gain = (1 - RHOm) * Qp * (Bf(aum, mup) - mpf(cH) + mpf(PR) ** 2 / aum["r"]) if hi else mp.mpf(0)
    return gain - psi * mpf(kappa) - xi * PIm * psi * KTRm


# ================================================================================ SECTION 0
hd("0. Auction objects: closed forms against direct integration (exact fractions)")
for r in [F(6, 5), F(3), F(18, 5), F(21, 5)]:
    c, dct = auction_closed(r), auction_direct(r)
    same = all(c[k] == dct[k] for k in ["t0", "tH", "tL", "gH", "gL", "DT"])
    print(f"r={float(r):4.1f}: closed==direct {same};  Delta_T={c['DT']} ({float(c['DT']):.6f});  "
          f"g_H={float(c['gH']):.6f}  g_L={float(c['gL']):.6f}  B(1/2)={Bf(c, PI)} ({float(Bf(c, PI)):.6f})")

dl = DL()
print()
print(f"a = exp(-1/2) = {nf(dl.a, 30)};  m = a/(1+a) = {nf(dl.m, 20)};  M = 1/(1+a) = {nf(dl.M, 20)};  d = 1-a = {nf(dl.d, 20)}")
print(f"mass outside |z|<={NFL}: {nf(dl.tail(), 5)}")
# noise law as a difference of two independent geometric counts (direct convolution)
for z in [0, 1, -2, 3]:
    conv = sum((1 - dl.a) ** 2 * dl.a ** (2 * n + abs(z)) for n in range(0, 600))
    print(f"P(Z={z:2d}): difference of geometric counts {nf(conv, 25)}   closed form {nf(dl.n(z), 25)}")

# ================================================================================ SECTION 1
hd("1. Posteriors with a mixed acquisition probability psi (flow-level Bayes); containment in [m, M]")
au3 = auction_closed(3)
for s in [mp.mpf(0), mp.mpf("0.1"), mp.mpf("0.4108902"), mp.mpf("0.5"), mp.mpf("0.8631322"), mp.mpf(1)]:
    vals = set()
    for x in range(-60, 62):
        vals.add(nf(post_flow(dl, s, x), 30))
    lo_x = post_flow(dl, s, 0)
    hi_x = post_flow(dl, s, 1)
    y = PIm * dl.d * s
    cl_m = PIm * (1 - dl.d * s) / (1 - y)
    cl_p = PIm * (dl.a + dl.d * s) / (dl.a + y)
    print(f"s={nf(s, 8):>10}: distinct posteriors over x in [-60,61]: {len(vals)};  mu(x<=0)={nf(lo_x, 12)}  mu(x>=1)={nf(hi_x, 12)};"
          f"  closed forms agree: {abs(lo_x - cl_m) < TOL and abs(hi_x - cl_p) < TOL}")
print(f"mu(x<=0, s=1) equals m: {abs(post_flow(dl, mp.mpf(1), 0) - dl.m) < TOL};  mu(x>=1, s=1) equals M: {abs(post_flow(dl, mp.mpf(1), 1) - dl.M) < TOL}")
ok = True
for i in range(0, 1001):
    s = mp.mpf(i) / 1000
    a0, a1 = post_flow(dl, s, 0), post_flow(dl, s, 1)
    ok = ok and (dl.m - TOL <= a0 <= PIm + TOL) and (PIm - TOL <= a1 <= dl.M + TOL)
print(f"on a 1001-point grid of s: m <= mu_- <= 1/2 <= mu_+ <= M holds: {ok}")

# ================================================================================ SECTION 2
hd("2. D_r(s): direct sum over flows (N=300) against my two-region closed form, r=3, c_H=5")
sE5, tau5 = find_sE(dl, au3, CH5)
print(f"tau = {nf(tau5, 20)} (exact {tau_of(au3, CH5)});  M > tau: {dl.M > tau5};  s_E (bisection on flow-level Bayes) = {nf(sE5, 25)}")
cl_sE = dl.a * (tau5 - PIm) / (PIm * dl.d * (1 - tau5))
print(f"closed-form s_E = a(tau-pi)/(pi d (1-tau)) = {nf(cl_sE, 25)};  difference {nf(abs(cl_sE - sE5), 3)}")
print(f"tail bound on the omitted gross payoff: Delta_T * 2 a^(N+1)/(1+a) = {nf(mpf(au3['DT']) * dl.tail(), 5)}")
for s in [mp.mpf(0), mp.mpf("0.2"), sE5 - mp.mpf(10) ** -30, sE5, mp.mpf("0.8"), mp.mpf(1)]:
    b = brute_D(dl, au3, CH5, s)
    c, mum, mup, em, ep = closed_D(dl, au3, CH5, s)
    print(f"s={nf(s, 12):>14}: brute {nf(b, 25)}  closed {nf(c, 25)}  |diff| {nf(abs(b - c), 3)}  entry (lower,upper)=({nf(em, 4)},{nf(ep, 4)})")

# ================================================================================ SECTION 3
hd("3. Cost cutoffs at r=3, c_H=5 (research value = pi*(D - k))")
v0 = vcut(dl, au3, CH5, mp.mpf(0))
vEm = vcut(dl, au3, CH5, sE5 - mp.mpf(10) ** -30)
vEp = vcut(dl, au3, CH5, sE5)
v1 = vcut(dl, au3, CH5, mp.mpf(1))
print(f"v_0   = {nf(v0, 20)}    exact 19/600 = {nf(mpf(F(19, 600)), 20)}")
print(f"v_E^- = {nf(vEm, 20)}")
print(f"v_E^+ = {nf(vEp, 20)}")
print(f"v_1   = {nf(v1, 20)}    closed form (5/12) a/(1+a)^2 - 1/100 = {nf(mpf(F(5, 12)) * dl.a / (1 + dl.a) ** 2 - mpf(F(1, 100)), 20)}")
print(f"v_0 < v_1: {v0 < v1};  rho*m*Delta_T(3) = {nf(RHOm * dl.m * mpf(au3['DT']), 12)};  (rho*m*Delta_T - k)/2 = {nf((RHOm * dl.m * mpf(au3['DT']) - KTRm) / 2, 12)}")
# monotonicity of the value inside each entry regime, and the upward jump
vals = [(mp.mpf(i) / 2000, vcut(dl, au3, CH5, mp.mpf(i) / 2000)) for i in range(0, 2001)]
lo_dec = all(v1_ < v0_ for (s0_, v0_), (s1_, v1_) in zip(vals[:-1], vals[1:]) if s1_ < sE5)
up_dec = all(v1_ < v0_ for (s0_, v0_), (s1_, v1_) in zip(vals[:-1], vals[1:]) if s0_ >= sE5)
print(f"value strictly falls in s on [0, s_E): {lo_dec};  strictly falls on [s_E, 1]: {up_dec};  jump up at s_E: {nf(vEp - vEm, 12)}")

# ================================================================================ SECTION 4
hd("4. Equilibrium acquisition sets at r=3, c_H=5 (corners from G(0), G(1); interior roots by scan + bisection)")
print("kappa     | equilibria: (kind, psi) -> entry E, high-class ownership O_H")
for kap in [F(2, 100), F(3, 100), F(5, 100), F(9, 100), F(94, 1000), F(95, 1000)]:
    sol, sE, tau = solve_psi(dl, au3, CH5, kap)
    parts = []
    for kind, psi in sol:
        E, OH = outcomes(dl, au3, CH5, psi)
        parts.append(f"({kind}, psi={nf(psi, 14)}) E={nf(E, 14)} O_H={nf(OH, 12)}")
    print(f"{float(kap):<9} | " + "  ;  ".join(parts) if parts else f"{float(kap):<9} | none")

print()
print("Residuals at the interior roots (brute-force flows): investor indifference pi*(D_brute - k) - kappa")
for kap in [F(3, 100), F(9, 100), F(94, 1000)]:
    sol, sE, tau = solve_psi(dl, au3, CH5, kap)
    for kind, psi in sol:
        if kind.startswith("interior"):
            Db = brute_D(dl, au3, CH5, psi)
            DbL = brute_D(dl, au3, CH5, psi, who="L") - KTRm
            print(f"kappa={float(kap)}: psi={nf(psi, 14)}  residual={nf(PIm * (Db - KTRm) - mpf(kap), 3)}  "
                  f"D_brute - k = {nf(Db - KTRm, 10)} > 0 (strict buy);  low-class purchase payoff (net) = {nf(DbL, 8)} < 0;  psi >= s_E: {psi >= sE}")

print()
print("Cross-check of the interior roots against the quadratic L y^2 + [C(rho-e) - L d] y + C(rho a + e) - L a = 0 (y = pi d s), my own derivation")
for kap, e in [(F(3, 100), RHO), (F(9, 100), F(1)), (F(94, 1000), F(1))]:
    a, d = dl.a, dl.d
    L = KTRm + mpf(kap) / PIm
    C = mpf(au3["DT"]) * (1 - PIm) * a / (1 + a)
    ee = mpf(e)
    A2, B1, C0 = L, C * (RHOm - ee) - L * d, C * (RHOm * a + ee) - L * a
    disc = B1 * B1 - 4 * A2 * C0
    roots = [(-B1 - mp.sqrt(disc)) / (2 * A2), (-B1 + mp.sqrt(disc)) / (2 * A2)]
    print(f"kappa={float(kap)}, e_+={e}: s roots = " + ", ".join(nf(y / (PIm * d), 14) for y in roots))

# ================================================================================ SECTION 5
hd("5. Claim 3: kappa=0.02, c_H=5, strengths 1.2, 3, 3.6 and 4.2")
kap = F(2, 100)
for r in [F(6, 5), F(3), F(18, 5), F(21, 5)]:
    au = auction_closed(r)
    sol, sE, tau = solve_psi(dl, au, CH5, kap)
    Dmin = min(closed_D(dl, au, CH5, mp.mpf(i) / 500)[0] for i in range(0, 501))
    Dmax = max(closed_D(dl, au, CH5, mp.mpf(i) / 500)[0] for i in range(0, 501))
    bound = RHOm * dl.m * mpf(au["DT"])
    res = []
    for kind, psi in sol:
        E, OH = outcomes(dl, au, CH5, psi)
        res.append(f"{kind} psi={nf(psi, 6)} E={nf(E, 12)} O_H={nf(OH, 12)}")
    print(f"r={float(r):4.1f}: Delta_T={float(au['DT']):.6f}  B_r(1/2)={float(Bf(au, PI)):.6f} (<5: {Bf(au, PI) < 5})  B_r(M)={nf(Bf(au_mp(au), dl.M), 12)} (>=5: {Bf(au_mp(au), dl.M) >= 5})")
    print(f"        min_s D = {nf(Dmin, 10)}, max_s D = {nf(Dmax, 10)}, rho*m*Delta_T = {nf(bound, 10)}, k = {float(KTR)};  "
          f"min_s pi(D-k) = {nf(PIm * (Dmin - KTRm), 10)} vs kappa = {float(kap)};  Delta_T < k: {au['DT'] < KTR}")
    print("        equilibria: " + ("; ".join(res) if res else "none"))

print()
Qp = sum(PIm * ((1 - 1) * dl.n(x) + 1 * dl.n(x - 1)) + (1 - PIm) * dl.n(x) for x in range(1, NFL + 2))
E1_, O1_ = outcomes(dl, au3, CH5, mp.mpf(1))
print(f"r=3, psi=1: Pr(flow x >= 1) by direct sum = {nf(Qp, 25)} (exact 1/2);  E = {nf(E1_, 20)} vs rho+(1-rho)/2 = 0.625;  "
      f"O_H = {nf(O1_, 20)} vs rho/2 + (1-rho)/(2(1+a)) = {nf(RHOm / 2 + (1 - RHOm) / (2 * (1 + dl.a)), 20)}")
print()
print("Rational bounds in the memo's proof of claim 3 (exact fractions)")
a_lo, a_hi = F(3, 5), F(2, 3)
m_lo, M_lo, M_hi = a_lo / (1 + a_lo), 1 / (1 + a_hi), 1 / (1 + a_lo)
print(f"e^(1/2) < 33/20 < 5/3: {F(33, 20) < F(5, 3)} => a > 3/5;  e^(1/2) > 3/2 => a < 2/3.  m > {m_lo}, {M_lo} < M < {M_hi}")
au12 = auction_closed(F(6, 5))
au42 = auction_closed(F(21, 5))
print(f"(1/2)[rho*(3/8)*Delta_T(3) - k] = {F(1, 2) * (RHO * m_lo * auction_closed(3)['DT'] - KTR)} = {float(F(1, 2) * (RHO * m_lo * auction_closed(3)['DT'] - KTR)):.6f} > 1/50: {F(1, 2) * (RHO * m_lo * auction_closed(3)['DT'] - KTR) > F(1, 50)}")
print(f"Delta_T(6/5) = {au12['DT']} < k=1/50: {au12['DT'] < KTR};  B_{{6/5}}(1/2) = {Bf(au12, PI)} < 5: {Bf(au12, PI) < 5}")
print(f"B_3(3/5) = {Bf(au3, F(3, 5))} > 5: {Bf(au3, F(3, 5)) > 5};   B_{{21/5}}(5/8) = {Bf(au42, F(5, 8))} < 5: {Bf(au42, F(5, 8)) < 5}")
print(f"tau(3, c_H=5) = {tau_of(au3, CH5)} = {float(tau_of(au3, CH5))};  117/200 = {F(117, 200)};  tau < 3/5 < M: {tau_of(au3, CH5) < F(3, 5)}")
# ceiling r_C: B_r(M) = 5
lo, hi = mp.mpf(3), mp.mpf(5)
for _ in range(170):
    mid = (lo + hi) / 2
    g = (mpf(H) - mid / 2 - mpf(PR) ** 2 / (2 * mid)) * dl.M + (1 - dl.M) * (mpf(ELL ** 2 - PR ** 2) / (2 * mid))
    if g >= 5:
        lo = mid
    else:
        hi = mid
print(f"ceiling r_C solving B_r(M)=5: {nf(lo, 20)}")

# ================================================================================ SECTION 6
hd("6. Claim 2: coexistence at r=3, c_H=5, kappa=0.05")
kap5 = F(5, 100)
print(f"v_0 = {nf(v0, 12)} <= {float(kap5)} <= v_1 = {nf(v1, 12)}: {v0 <= mpf(kap5) <= v1};  strict: {v0 < mpf(kap5) < v1}")
print(f"net gain of acquiring against the schedule of psi=0: {nf(v0 - mpf(kap5), 8)} (<0, so psi=0 is a best reply);  against the schedule of psi=1: {nf(v1 - mpf(kap5), 8)} (>0, so psi=1 is a best reply)")
print(f"exact-rational chain: 19/600 < 1/20: {F(19, 600) < F(1, 20)};  (5/12)(15/64) - 1/100 = {F(5, 12) * F(15, 64) - F(1, 100)} > 1/20: {F(5, 12) * F(15, 64) - F(1, 100) > F(1, 20)};  "
      f"a/(1+a)^2 at a=3/5: {F(3, 5) / (1 + F(3, 5)) ** 2}")
# sensitivity: coexistence survives small parameter changes
print("Robustness grid at r=3, c_H=5: does v_0 < kappa < v_1 hold when one input moves?")
for lab, cH_, kk, rr, rho_ in [("base", 5, F(1, 50), F(3), F(1, 4)), ("k=0.015", 5, F(3, 200), F(3), F(1, 4)), ("k=0.025", 5, F(1, 40), F(3), F(1, 4)),
                               ("r=2.8", 5, F(1, 50), F(14, 5), F(1, 4)), ("r=3.3", 5, F(1, 50), F(33, 10), F(1, 4)), ("c_H=4.9", F(49, 10), F(1, 50), F(3), F(1, 4)),
                               ("c_H=5.2", F(52, 10), F(1, 50), F(3), F(1, 4))]:
    auu = auction_closed(rr)
    Dm0 = closed_D(dl, auu, cH_, mp.mpf(0))[0]
    Dm1 = closed_D(dl, auu, cH_, mp.mpf(1))[0]
    pv0 = PIm * (Dm0 - mpf(kk))
    pv1 = PIm * (Dm1 - mpf(kk))
    print(f"   {lab:8s}: v_0={nf(pv0, 8)}  v_1={nf(pv1, 8)}  kappa=0.05 inside [v_0, v_1]: {pv0 < mpf(kap5) < pv1}")

# ================================================================================ SECTION 7
hd("7. Claim 4: c_H=6 blocks expensive entry (b=2, pi=1/2, buy-only)")
print("(a) largest posterior over all buy-only strategy pairs (class H buys w.p. sH, class L buys w.p. sL), flows -40..41")
best, arg = mp.mpf(0), None
for i in range(0, 11):
    for j in range(0, 11):
        sh, sl = mp.mpf(i) / 10, mp.mpf(j) / 10
        for x in range(-40, 42):
            fH = (1 - sh) * dl.n(x) + sh * dl.n(x - 1)
            fL = (1 - sl) * dl.n(x) + sl * dl.n(x - 1)
            mu = PIm * fH / (PIm * fH + (1 - PIm) * fL)
            if mu > best:
                best, arg = mu, (sh, sl, x)
print(f"max posterior {nf(best, 20)} at (sH, sL, x) = ({nf(arg[0], 3)}, {nf(arg[1], 3)}, {arg[2]});  M = {nf(dl.M, 20)}")
print(f"   profile 'only class H buys' at x=1: posterior {nf(post_flow(dl, mp.mpf(1), 1), 20)};  profile 'only class L buys' at x=0: posterior "
      f"{nf(PIm * dl.n(0) / (PIm * dl.n(0) + (1 - PIm) * dl.n(-1)), 20)}  (both equal M)")
print("(b) gross profit at the highest posterior, B_r(M), against c_H=6")
au1 = auction_closed(F(1))
print(f"B_1(mu) = {au1['gL']} + {au1['gH'] - au1['gL']} mu   (limit r -> l = 1)")
print(f"B_1(M) = {nf(Bf(au_mp(au1), dl.M), 20)}  <  6: {Bf(au_mp(au1), dl.M) < 6};  gap to 6: {nf(6 - Bf(au_mp(au1), dl.M), 10)}")
mx = mp.mpf(-100)
for i in range(1, 900):
    rr = F(1) + F(i, 100)
    mx = max(mx, Bf(au_mp(auction_closed(rr)), dl.M))
print(f"max over r in (1, 10) on a 0.01 grid of B_r(M): {nf(mx, 12)}  (< 6: {mx < 6});  g_H' < 0 and g_L' < 0 because p < r and p < l")
Bm_chain = F(3, 8) + 9 * F(5, 8)
print("(c) exact chain: e^(1/2) <= 1+1/2+(1/8)/(1-1/6) =", F(1) + F(1, 2) + F(1, 8) / (1 - F(1, 6)), "= 33/20 < 5/3:", F(33, 20) < F(5, 3),
      "=> a >= 20/33 > 3/5 => M <= 33/53 <", F(5, 8), "; B_1(5/8) =", Bm_chain, ";  B_1(33/53) =", F(3, 8) + 9 * F(33, 53), "=", float(F(3, 8) + 9 * F(33, 53)))
bstar = 1 / mp.log(mp.mpf(5) / 3)
print(f"c_H=6 stays blocked iff M(b) < 5/8 iff b > 1/ln(5/3) = {nf(bstar, 12)}; the paper's b=2 clears this by {nf(2 - bstar, 6)}")
for bb in [mp.mpf("1.90"), mp.mpf("1.9576"), mp.mpf("1.96"), mp.mpf(2), mp.mpf(3)]:
    aa = mp.exp(-1 / bb)
    MM = 1 / (1 + aa)
    print(f"   b={nf(bb, 5):>7}: M={nf(MM, 8)}  B_1(M)={nf(Bf(au_mp(au1), MM), 8)}  can reach 6 as r -> 1: {Bf(au_mp(au1), MM) >= 6}")

# ================================================================================ SECTION 8
hd("8. Claim 5: public acquisition, r=3, c_H=5")
print("Continuation after an observed acquisition: the high class buys with probability beta, so the effective s equals beta.")
umin = min(closed_D(dl, au3, CH5, mp.mpf(i) / 1000)[0] - KTRm for i in range(0, 1001))
print(f"min over beta in [0,1] of D(beta) - k = {nf(umin, 10)} > 0: {umin > 0}  => beta = 1 is the only continuation (beta=0 and any interior beta need D = k or D <= k)")
Vpub = PIm * (brute_D(dl, au3, CH5, mp.mpf(1)) - KTRm)
print(f"V_public = pi*(D(1) - k), direct flow sum = {nf(Vpub, 15)}  (equals closed-form v_1: {abs(Vpub - v1) < TOL})")
for kap in [F(2, 100), F(5, 100), F(9, 100), F(95, 1000)]:
    pub = "psi = 1 only" if mpf(kap) < Vpub else ("psi = 0 only" if mpf(kap) > Vpub else "every psi")
    sol, sE, tau = solve_psi(dl, au3, CH5, kap)
    hid = ", ".join(f"{k_}:{nf(p_, 8)}" for k_, p_ in sol)
    print(f"kappa={float(kap):<6}: public -> {pub};   hidden -> {hid}")
print(f"At kappa=0.05 under public acquisition, a deviation from psi=0 pays pi(D(1)-k) - kappa = {nf(Vpub - mp.mpf('0.05'), 10)} > 0, so psi = 0 fails.")

# ================================================================================ SECTION 9
hd("9. Claim 6: welfare from first principles (allocation value - preparation costs - research cost - trade cost if a resource)")
print("Allocation-gain identity W_theta - W_0 = g_theta + p^2/r (exact fractions)")
for rr in [F(6, 5), F(3), F(18, 5), F(21, 5)]:
    au = auction_closed(rr)
    W0 = unif_mean(lambda u: u if u >= PR else F(0), rr)
    Wh = unif_mean(lambda u: max(u, H), rr)
    Wl = unif_mean(lambda u: max(u, ELL), rr)
    print(f"   r={float(rr):4.1f}: W_h - W_0 = g_H + p^2/r: {Wh - W0 == au['gH'] + PR ** 2 / rr};  W_l - W_0 = g_L + p^2/r: {Wl - W0 == au['gL'] + PR ** 2 / rr}")
print()
cases = [("r=3, kappa=0.02, psi=1", F(3), F(2, 100), "corner1"), ("r=3, kappa=0.094, upper-branch root", F(3), F(94, 1000), "interior"),
         ("r=3, kappa=0.03, lower-branch root", F(3), F(3, 100), "interior"), ("r=3, kappa=0.09, upper-branch root", F(3), F(9, 100), "interior"),
         ("r=4.2, kappa=0.02, psi=1", F(21, 5), F(2, 100), "corner1")]
for lab, rr, kap, want in cases:
    au = auction_closed(rr)
    sol, sE, tau = solve_psi(dl, au, CH5, kap)
    pick = [p_ for k_, p_ in sol if k_.startswith(want)]
    # for the lower-branch case pick the root below s_E; for the upper-branch case the root above
    if lab.startswith("r=3, kappa=0.03"):
        pick = [p_ for p_ in pick if p_ < sE]
    psi = pick[0]
    E0, O0 = outcomes(dl, au, CH5, mp.mpf(0))
    E1, O1 = outcomes(dl, au, CH5, psi)
    for xi in [1, 0]:
        dW = welfare(dl, au, CH5, psi, kap, xi) - welfare(dl, au, CH5, mp.mpf(0), kap, xi)
        form = memo_dW(dl, au, CH5, psi, kap, xi)
        print(f"{lab:38s} psi={nf(psi, 12)}  E: {nf(E0, 6)} -> {nf(E1, 12)}  xi={xi}: dW(first principles) = {nf(dW, 14)}  closed form = {nf(form, 14)}")
    gross = welfare(dl, au, CH5, psi, kap, 0) - welfare(dl, au, CH5, mp.mpf(0), kap, 0) + psi * mpf(kap)
    print(f"{'':38s} entry benefit before research and trade costs = {nf(gross, 14)}")

# ================================================================================ SECTION 10
hd("10. Claim 7: the no-entry-response purchase profit at r_1 = 3 (full research, s = 1)")
D_noresp = brute_D(dl, au3, CH5, mp.mpf(1), force_e=RHOm)
D_resp = brute_D(dl, au3, CH5, mp.mpf(1))
print(f"purchase profit with entry held at rho after good news: D - k = {nf(D_noresp - KTRm, 15)}")
print(f"   closed form 2*rho*Delta_T*a/(1+a)^2 - k = {nf(2 * RHOm * mpf(au3['DT']) * dl.a / (1 + dl.a) ** 2 - KTRm, 15)}")
print(f"purchase profit with expensive entry after good news : D - k = {nf(D_resp - KTRm, 15)}")
print(f"   closed form Delta_T*(1+rho)*a/(1+a)^2 - k = {nf(mpf(au3['DT']) * (1 + RHOm) * dl.a / (1 + dl.a) ** 2 - KTRm, 15)}")
print(f"ex ante research values (times pi): {nf(PIm * (D_noresp - KTRm), 12)} and {nf(PIm * (D_resp - KTRm), 12)}")
print(f"flat-price case (s=0): rho*(1-pi)*Delta_T - k = {RHO * (1 - PI) * au3['DT'] - KTR} = {float(RHO * (1 - PI) * au3['DT'] - KTR):.6f}")
print(f"other round numbers near 0.060: rho*m*Delta_T - k = {nf(RHOm * dl.m * mpf(au3['DT']) - KTRm, 8)};  rho*Delta_T/2 - k = {float(RHO * au3['DT'] / 2 - KTR):.6f}")

print()
print("Tail bound used in the memo, recomputed at N=400: Delta_T * 2 a^401/(1+a) =", nf(mpf(au3["DT"]) * 2 * dl.a ** 401 / (1 + dl.a), 8))
print("Test of one possible source of the brief's 0.060: noise support cut to |z| <= K and renormalised (s=1, entry held at rho)")
for K in [2, 3, 4, 5, 6, 8, 12]:
    w = {z: dl.n(z) for z in range(-K, K + 1)}
    tot_w = sum(w.values())
    w = {z: v / tot_w for z, v in w.items()}
    acc = mp.mpf(0)
    for z in range(-K, K + 1):
        x = 1 + z
        fH = w.get(x - 1, mp.mpf(0))
        fL = w.get(x, mp.mpf(0))
        mu = PIm * fH / (PIm * fH + (1 - PIm) * fL)
        acc += w[z] * RHOm * mpf(au3["DT"]) * (1 - mu)
    print(f"   K={K:2d}: purchase profit without entry response = {nf(acc - KTRm, 8)}")

# ================================================================================ SECTION 11
hd("11. Claim 1: equal noise Z in {-1,0,1} (exact fractions)")


def eqn(au, cH, s, rule="limit"):
    """Flow laws, posteriors, entry for equal noise; rule is the belief at flow 2 when s=0: 'limit' (=1), or a number."""
    fH = {-1: (1 - s) / 3, 0: F(1, 3), 1: F(1, 3), 2: s / 3}
    fL = {-1: F(1, 3), 0: F(1, 3), 1: F(1, 3), 2: F(0)}
    rows = {}
    for x in [-1, 0, 1, 2]:
        tot = PI * fH[x] + (1 - PI) * fL[x]
        mu = (PI * fH[x] / tot) if tot > 0 else (F(1) if rule == "limit" else F(rule))
        e = RHO + (1 - RHO) * (1 if Bf(au, mu) >= cH else 0)
        rows[x] = (fH[x], fL[x], mu, e)
    return rows


def Dequal(au, cH, s, rule="limit"):
    rows = eqn(au, cH, s, rule)
    return sum(F(1, 3) * rows[x][3] * au["DT"] * (1 - rows[x][2]) for x in [0, 1, 2])


for r in [F(6, 5), F(3), F(18, 5)]:
    au = auction_closed(r)
    print(f"r={float(r)}: B_r(1/2)={float(Bf(au, PI)):.4f} < 6;  g_H={float(au['gH']):.4f} >= 6: {au['gH'] >= 6}")
    for s in [F(0), F(1, 10), F(1, 2), F(1)]:
        rows = eqn(au, CH6, s)
        D = Dequal(au, CH6, s)
        E = sum((PI * rows[x][0] + (1 - PI) * rows[x][1]) * rows[x][3] for x in rows)
        OH = PI * sum(rows[x][0] * rows[x][3] for x in rows)
        mus = {x: str(rows[x][2]) for x in rows}
        print(f"    s={str(s):>5}: posteriors {mus}  D={D} ({float(D):.6f})  E={E} ({float(E):.5f}) O_H={OH} ({float(OH):.5f})")
    Vbar = PI * max(F(2, 3) * RHO * (1 - PI) * au["DT"] - KTR, 0)
    print(f"    Vbar_3(r) = {Vbar} = {float(Vbar):.8f};  memo: 0 at 1.2, 4/225 at 3, 629/21600 at 3.6")
print()
d_k = 3 * (KTR + F(1, 100) / PI) / (2 * RHO * (1 - PI))
rk = mpf(ELL) + mpf(d_k) + mp.sqrt(mpf(d_k) ** 2 + 2 * mpf(ELL) * mpf(d_k))
lo, hi = mp.mpf(1) + mp.mpf(10) ** -9, mp.mpf(10)
for _ in range(170):
    mid = (lo + hi) / 2
    val = mpf(PI) * (mp.mpf(2) / 3 * RHOm * (1 - PIm) * (mid - 1) ** 2 / (2 * mid) - KTRm)
    if val >= mp.mpf(1) / 100:
        hi = mid
    else:
        lo = mid
print(f"kappa=1/100: d_kappa = {d_k};  closed-form r_kappa = {nf(rk, 15)};  bisection on Vbar_3(r)=kappa: {nf(hi, 15)}")
r_ret = 4 + mp.sqrt(63) / 2
gH_ret = mpf(H) - r_ret / 2 - mpf(PR) ** 2 / (2 * r_ret)
print(f"return strength: r = 4 + sqrt(63)/2 = {nf(r_ret, 15)};  g_H there = {nf(gH_ret, 15)} (should equal c_H = 6)")

print()
print("Dependence on the belief at the off-path flow 2 when psi=0, r=3, kappa=0.02 (value of research at s=0 versus s>0):")
au = auction_closed(F(3))
for rule, name in [("limit", "mu_2 = 1 (memo's completion)"), (F(1, 2), "mu_2 = 1/2 (passive)"), (F(0), "mu_2 = 0")]:
    D0 = Dequal(au, CH6, F(0), rule)
    D1 = Dequal(au, CH6, F(1, 2), rule)
    V0_, V1_ = PI * max(D0 - KTR, 0), PI * max(D1 - KTR, 0)
    gap = f"kappa in ({float(V1_):.6f}, {float(V0_):.6f}) has no equilibrium" if V0_ > V1_ else "no gap"
    print(f"   {name:30s}: V(0) = {V0_} ({float(V0_):.6f}),  V(s>0) = {V1_} ({float(V1_):.6f});  {gap}")

# ================================================================================ SECTION 12
hd("12. Side check: would a non-acquirer gain by buying uninformed? (gross payoff; the memo forbids this)")
for rr, lab in [(F(3), "r=3"), (F(21, 5), "r=4.2")]:
    au = auction_closed(rr)
    aum = au_mp(au)
    worst = mp.mpf(-100)
    for i in range(0, 101):
        s = mp.mpf(i) / 100
        tot = mp.mpf(0)
        for z in range(-NFL, NFL + 1):
            x = 1 + z
            mu = post_flow(dl, s, x)
            e = entry_from_mu(aum, CH5, mu)
            tot += dl.n(z) * e * aum["DT"] * (PIm - mu)
        worst = max(worst, tot)
    print(f"discrete Laplace {lab}: largest gross payoff of an uninformed purchase over s in [0,1] = {nf(worst, 10)} (<= 0, so the net payoff is below -k)")
print("Analytic form of the uninformed gross payoff: Delta_T*y*(1-pi)*[a*e_-/((1+a)(1-y)) - e_+/((1+a)(a+y))], y = pi d s")
for s in [mp.mpf("0.3"), mp.mpf("0.7"), mp.mpf(1)]:
    y = PIm * dl.d * s
    cl_, mum_, mup_, em_, ep_ = closed_D(dl, au3, CH5, s)
    ana = mpf(au3["DT"]) * y * (1 - PIm) * (dl.a * em_ / ((1 + dl.a) * (1 - y)) - ep_ / ((1 + dl.a) * (dl.a + y)))
    tot = mp.mpf(0)
    aum_ = au_mp(au3)
    for z in range(-NFL, NFL + 1):
        mu = post_flow(dl, s, 1 + z)
        tot += dl.n(z) * entry_from_mu(aum_, CH5, mu) * aum_["DT"] * (PIm - mu)
    print(f"   s={nf(s, 3)}: analytic {nf(ana, 15)}   direct sum {nf(tot, 15)}")
au = auction_closed(F(3))
worst = max(
    sum(F(1, 3) * eqn(au, CH6, s)[x][3] * au["DT"] * (PI - eqn(au, CH6, s)[x][2]) for x in [0, 1, 2]) for s in [F(0), F(1, 10), F(1, 2), F(1)])
print(f"equal noise r=3: largest gross payoff of an uninformed purchase over s in {{0,1/10,1/2,1}} = {worst} ({float(worst):.6f})")

# ================================================================================ SECTION 13
hd("13. Memo's regime table at r=3, c_H=5: equilibria on both sides of each cutoff (kappa shown to 9 digits)")
eps = mp.mpf(10) ** -9
cuts = [("v_E^-", vEm), ("v_0", v0), ("v_1", v1), ("v_E^+", vEp)]
tests = [("0.01 (below v_E^-)", mp.mpf("0.01"))]
for nm, c in cuts:
    tests += [(f"{nm} - 1e-9", c - eps), (f"{nm} exactly", c), (f"{nm} + 1e-9", c + eps)]
tests += [("0.10 (above v_E^+)", mp.mpf("0.10"))]
for lab, kap in tests:
    sol, sE, tau = solve_psi(dl, au3, CH5, kap)
    print(f"kappa = {nf(kap, 10):>12} ({lab:20s}): " + (", ".join(f"{k_}:{nf(p_, 6)}" for k_, p_ in sol) if sol else "none"))
print("Memo's table: kappa <= v_E^- -> {1};  v_E^- < kappa < v_0 -> {interior<s_E, 1};  v_0 <= kappa <= v_1 -> {0, 1};  v_1 < kappa <= v_E^+ -> {0, root in [s_E,1)};  kappa > v_E^+ -> {0}")
print("(exact-endpoint rows rely on the numerical tie tolerance 1e-40; 'exactly' for v_E^- and v_E^+ uses values computed from the left limit and the tie rule)")

# ================================================================================ SECTION 14
hd("14. Convention check: what if the indifferent challenger could mix at the entry threshold (psi = s_E)?")
print("At psi = s_E the upper posterior equals tau. With mixing, the entry rate e_+ in [rho, 1] is free, and the investor is indifferent when")
print("pi*(D - k) = kappa, i.e. e_+ = (L/C - rho/(1-y)) (a + y) with L = k + kappa/pi, C = Delta_T (1-pi) a/(1+a), y = pi d s_E.")
aum3 = au_mp(au3)
a_, d_ = dl.a, dl.d
yE = PIm * d_ * sE5
C3 = aum3["DT"] * (1 - PIm) * a_ / (1 + a_)
for kap in [mp.mpf("0.02"), mp.mpf("0.0295"), mp.mpf("0.03"), mp.mpf("0.05"), mp.mpf("0.09"), mp.mpf("0.0940"), mp.mpf("0.095")]:
    L = KTRm + kap / PIm
    e_star = (L / C3 - RHOm / (1 - yE)) * (a_ + yE)
    # direct flow check with the entry rate forced to e_star at the upper flows
    tot = mp.mpf(0)
    for z in range(-NFL, NFL + 1):
        x = 1 + z
        mu = post_flow(dl, sE5, x)
        e = e_star if x >= 1 else RHOm
        price = aum3["t0"] + e * (aum3["wL"] + aum3["DT"] * mu)
        ev = aum3["t0"] + e * (aum3["wL"] + aum3["DT"])
        tot += dl.n(z) * (ev - price)
    resid = PIm * (tot - KTRm) - kap
    ok_ = RHOm <= e_star <= 1
    print(f"kappa={nf(kap, 5):>7}: e_+ needed = {nf(e_star, 8):>12}  admissible: {ok_};  direct-sum residual {nf(resid, 3)}")
print("So the tie rule 'the indifferent challenger prepares' removes a third equilibrium (psi = s_E, partial expensive entry) for kappa in [v_E^-, v_E^+].")

print()
print("done")
