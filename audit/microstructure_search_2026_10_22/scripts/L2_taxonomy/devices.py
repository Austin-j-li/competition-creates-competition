"""L2: fixed-profile posterior statistics of microstructure devices at the benchmark.

Print-only. No assertions. For each device the informative profile is fixed:
buy-only: class H buys one unit, class L does not trade;
two-sided: class H buys one unit, class L sells one unit.
Prior pi = 1/2. Benchmark: h=10, l=1, p=0.5, rho=0.25, c_L=0.
Reported per device:
  Mmax    largest attained posterior (over flows with P_H > 0)
  revH    P_H mass of flows with posterior exactly 1 (revealing H)
  entry   rho + (1-rho) * P(posterior >= tau(r)), at r = 1.2, 3, 3.6 and the stated c_H
  U       H's purchase payoff coefficient (units of Delta_T) with entry at r=3
  V       H's deviation payoff coefficient from no trade (units of Delta_T), IC belief at off-path flows
  rC      r at which B_r(Mmax) = c_H (ceiling)
"""
import math
import numpy as np
from scipy.optimize import brentq
from scipy.stats import norm

h, l, p, rho = 10.0, 1.0, 0.5, 0.25
pi = 0.5


def gH(r): return h - r / 2 - p * p / (2 * r)
def gL(r): return (l * l - p * p) / (2 * r)
def Br(r, mu): return gL(r) + mu * (gH(r) - gL(r))
def tau(r, cH): return (cH - gL(r)) / (gH(r) - gL(r))


def stats(name, PH, PL, cH, PN=None, note="", PB=None, PS=None):
    """PH, PL: arrays of flow probabilities (same support grid) under the profile.
    PN: flow law under no trade (noise only); flows with PN == 0 are off path under no trade."""
    PH = np.asarray(PH, float); PL = np.asarray(PL, float)
    # PB, PS: flow laws of a buy order and a sell order, conditional on the investor being present
    PB = PH if PB is None else np.asarray(PB, float)
    PS = PL if PS is None else np.asarray(PS, float)
    w = pi * PH + (1 - pi) * PL
    mu = np.where(w > 0, pi * PH / np.where(w > 0, w, 1), 0.0)
    onH = PH > 1e-15
    Mmax = mu[onH].max()
    revH = PH[onH & (mu > 1 - 1e-12)].sum()
    out = []
    for r in (1.2, 3.0, 3.6):
        rec = (Br(r, mu) >= cH - 1e-12) & (w > 0)
        out.append(rho + (1 - rho) * w[rec].sum())
    r = 3.0
    rec = (Br(r, mu) >= cH - 1e-12)
    e = np.where(rec, 1.0, rho)
    U = (PB * e * (1 - mu)).sum()
    if PN is None:
        V = rho * (1 - pi) * PB.sum()
    else:
        on = np.asarray(PN, float) > 1e-15
        V = rho * (1 - pi) * PB[on].sum()
    UL = (PS * e * mu).sum()
    f = lambda rr: Br(rr, Mmax) - cH
    try:
        rC = brentq(f, 1.0001, 9.99) if f(1.0001) > 0 else float('nan')
    except ValueError:
        rC = float('nan')
    print(f"{name:46s} cH={cH:3.1f} Mmax={Mmax:.4f} revH={revH:.4f} entry(1.2,3,3.6)=({out[0]:.3f},{out[1]:.3f},{out[2]:.3f}) U={U:.4f} V={V:.4f} UL(sell)={UL:.4f} rC={rC:.3f} {note}")


print("tau(r) at benchmark, c_H=6:", {r: round(tau(r, 6), 5) for r in (1.2, 1.55, 1.65, 3.0, 3.5927, 3.6)})
print("tau(r) at benchmark, c_H=5:", {r: round(tau(r, 5), 5) for r in (1.2, 3.0, 3.6, 4.2)})
print("paper M(b=2)=1/(1+exp(-1)) =", round(1 / (1 + math.exp(-1)), 5))
print("g_H(r)=6 at r=", round(brentq(lambda r: gH(r) - 6, 1.01, 9.9), 4))
print()

# --- continuous noise, two-sided orders +-1, grid quadrature ---
xs = np.linspace(-80, 80, 320001); dx = xs[1] - xs[0]
def cont(name, pdf, cH, buy_only=False):
    fH = pdf(xs - 1.0); fL = pdf(xs) if buy_only else pdf(xs + 1.0)
    PH = fH * dx; PL = fL * dx
    stats(name, PH, PL, cH, PN=pdf(xs) * dx)
for cH in (6.0,):
    cont("Laplace b=2, two-sided (paper)", lambda z: np.exp(-np.abs(z) / 2) / 4, cH)
    cont("Laplace b=2, buy-only", lambda z: np.exp(-np.abs(z) / 2) / 4, cH, True)
    s = math.sqrt(8.0)
    cont("Normal var 8, two-sided", lambda z: norm.pdf(z, scale=s), cH)
    cont("Normal var 8, buy-only", lambda z: norm.pdf(z, scale=s), cH, True)
    cont("Normal var 2, two-sided", lambda z: norm.pdf(z, scale=math.sqrt(2)), cH)
    # logistic with scale matching Laplace variance? use scale s_l with var = pi^2 s^2/3 = 8
    sl = math.sqrt(8 * 3) / math.pi
    cont("Logistic var 8, two-sided", lambda z: np.exp(-z / sl) / (sl * (1 + np.exp(-z / sl)) ** 2), cH)
    # uniform [-1,1], two-sided pure orders
    cont("Uniform[-1,1] noise, two-sided", lambda z: np.where(np.abs(z) <= 1, 0.5, 0.0), cH)
    cont("Uniform[-3,3] noise, two-sided", lambda z: np.where(np.abs(z) <= 3, 1 / 6, 0.0), cH)
    # one-sided exponential noise u>0, rate lam; buy-only: H buys 1
    for lam in (1.0, 0.5):
        cont(f"One-sided exp(rate {lam}), buy-only", lambda z, lam=lam: np.where(z > 0, lam * np.exp(-lam * np.where(z > 0, z, 0)), 0.0), cH, True)
print()

# --- discrete noise on integers ---
X = np.arange(-60, 61)
XMAX = 55  # report statistics on |x| <= XMAX to avoid truncation artifacts at the grid edge
def disc(name, noise, cH, mode, lam=1.0, note=""):
    """noise: dict z->prob. mode 'buy' or 'two'. lam: presence of informed (additive-noise models)."""
    def law(q):
        P = np.zeros(len(X))
        for z, pz in noise.items():
            P[(X == q + z)] += pz
        return P
    N0 = law(0)
    PH = lam * law(1) + (1 - lam) * N0
    PL = (lam * law(-1) + (1 - lam) * N0) if mode == 'two' else N0
    m = np.abs(X) <= XMAX
    PH = np.where(m, PH, 0.0); PL = np.where(m, PL, 0.0); N0 = np.where(m, N0, 0.0)
    stats(name, PH, PL, cH, PN=N0, note=note, PB=np.where(m, law(1), 0.0), PS=np.where(m, law(-1), 0.0))

tp = {-1: 1/3, 0: 1/3, 1: 1/3}
a = math.exp(-0.5)
dl = {z: (1 - a) / (1 + a) * a ** abs(z) for z in range(-120, 121)}
for cH in (6.0, 5.0):
    disc("3-pt buy-only lam=1", tp, cH, 'buy', 1.0)
    disc("3-pt buy-only lam=0.6", tp, cH, 'buy', 0.6)
    disc("3-pt two-sided lam=1", tp, cH, 'two', 1.0)
    disc("3-pt two-sided lam=0.6", tp, cH, 'two', 0.6)
    disc("3-pt two-sided lam=0.8", tp, cH, 'two', 0.8)
    disc("disc-Laplace b=2 buy-only", dl, cH, 'buy')
    disc("disc-Laplace b=2 two-sided", dl, cH, 'two')
    disc("unequal 3-pt (.25,.5,.25) buy-only", {-1: .25, 0: .5, 1: .25}, cH, 'buy')
    disc("unequal 3-pt (.4,.2,.4) buy-only", {-1: .4, 0: .2, 1: .4}, cH, 'buy')
print()

# --- binomial buy noise (N noise buyers, each buys one unit w.p. 1/2), buy-only ---
from math import comb
for cH in (6.0, 5.0):
    for N in (2, 4, 8, 20):
        nz = {z: comb(N, z) / 2 ** N for z in range(N + 1)}
        disc(f"Binomial N={N} noise buyers, buy-only", nz, cH, 'buy')
print()

# --- one-sided geometric noise z>=0, buy-only ---
for cH in (6.0, 5.0):
    for aa in (math.exp(-1), 0.5, 0.2):
        ng = {z: (1 - aa) * aa ** z for z in range(0, 80)}
        disc(f"One-sided geometric a={aa:.3f}, buy-only", ng, cH, 'buy', note=f"M=1/(1+a)={1/(1+aa):.4f}")
print()

# --- exclusive arrival (mixture): informed w.p. lam, else liquidity trader buys/sells w.p. (1-nu)/2, none w.p. nu ---
def mixture(name, lam, nu, cH, mode):
    # flows -1,0,+1
    liq = {-1: (1 - nu) / 2, 0: nu, 1: (1 - nu) / 2}
    PH = np.zeros(3); PL = np.zeros(3); PN = np.zeros(3)
    idx = {-1: 0, 0: 1, 1: 2}
    for f_, pf in liq.items():
        PH[idx[f_]] += (1 - lam) * pf; PL[idx[f_]] += (1 - lam) * pf; PN[idx[f_]] += (1 - lam) * pf
    PH[idx[1]] += lam
    if mode == 'two':
        PL[idx[-1]] += lam
    else:
        PL[idx[0]] += lam  # L present, no order
    PN[idx[0]] += lam      # informed present, no order
    PB = np.array([0.0, 0.0, 1.0]); PS = np.array([1.0, 0.0, 0.0])
    stats(name, PH, PL, cH, PN=PN, PB=PB, PS=PS)
for cH in (6.0, 5.0):
    for lam in (0.3, 0.46, 0.6, 0.8):
        mixture(f"Exclusive arrival two-sided lam={lam}, nu=0", lam, 0.0, cH, 'two')
    mixture("Exclusive arrival buy-only lam=0.46, nu=0", 0.46, 0.0, cH, 'buy')
    mixture("Exclusive arrival two-sided lam=0.46, nu=0.5", 0.46, 0.5, cH, 'two')
print()

# --- coarse observation: only S = 1{X>=1} observed (3-pt noise, buy-only) ---
for cH in (6.0, 5.0):
    PH = np.array([1/3, 2/3]); PL = np.array([2/3, 1/3])   # S=0, S=1
    stats("3-pt buy-only, sign S=1{X>=1} observed", PH, PL, cH, PN=PL)
    # two-sided 3-pt, observe sign of X in {-,0,+}: H buys, L sells
    # X=q+z: sign classes: X<=-1, X=0, X>=1
    PHs = np.array([1/3 * 0 + 0, 1/3 + 0, 2/3]) # H: z=-1->0; z=0->1; z=1->2 => S: X=0 w.p.1/3, X>=1 w.p. 2/3
    PLs = np.array([2/3, 1/3, 0])
    stats("3-pt two-sided, sign(X) observed", PHs, PLs, cH, PN=np.array([1/3, 1/3, 1/3]))

# --- slot device: informed investor w.p. lam, else a liquidity trader (buy w.p. beta, sell w.p. beta, none otherwise),
#     plus separate additive three-point noise (the combination studied by lever T2) ---
def slot(name, lam, beta, cH, mode, noise=tp):
    def law_order(q):
        P = np.zeros(len(X))
        for z, pz in noise.items():
            P[(X == q + z)] += pz
        return P
    liq = (1 - lam) * (beta * law_order(1) + beta * law_order(-1) + (1 - 2 * beta) * law_order(0))
    PB = law_order(1); PS = law_order(-1)
    PH = lam * PB + liq
    PL = lam * (PS if mode == 'two' else law_order(0)) + liq
    N0 = beta * law_order(1) + beta * law_order(-1) + (1 - 2 * beta) * law_order(0)   # no trade: slot order is liquidity only
    N0 = (1 - lam) * N0 + lam * law_order(0)
    m = np.abs(X) <= XMAX
    stats(name, np.where(m, PH, 0), np.where(m, PL, 0), cH, PN=np.where(m, N0, 0), PB=np.where(m, PB, 0), PS=np.where(m, PS, 0))
print()
for cH in (6.0,):
    slot("Slot + 3-pt noise, buy-only, beta=1/3, lam=6/17", 6/17, 1/3, cH, 'buy')
    slot("Slot + 3-pt noise, two-sided, beta=1/3, lam=6/17", 6/17, 1/3, cH, 'two')
    slot("Slot + 3-pt noise, buy-only, beta=1/3, lam=0.6", 0.6, 1/3, cH, 'buy')
    slot("Slot, no noise (3-pt weight on 0), two-sided, beta=1/3, lam=6/17", 6/17, 1/3, cH, 'two', noise={0: 1.0})
