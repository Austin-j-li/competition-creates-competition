"""Print-only checks for the economic case for Laplace noise (memo Q2_laplace_economic).

Run:  .venv/bin/python audit/alex_meeting_2026_10_21/scripts/Q2_laplace_economic/laplace_economic.py

The script computes and prints. It asserts nothing.
Parts:
  A. Three microfoundations give the Laplace law (mpmath quadrature, Monte Carlo).
  B. Discrete analogues give the two-sided geometric law.
  C. Maximum entropy at a fixed mean absolute noise.
  D. Score bound and posterior bounds for several noise laws.
  E. Variance-gamma family: score bound against the gamma shape.
  F. Closure of the bounded-score class under mixtures and convolution.
  G. Posterior range under full orders: Laplace, logistic, Student t, Gaussian.
"""
import numpy as np
import mpmath as mp
from scipy import special, signal, stats

mp.mp.dps = 30
rng = np.random.default_rng(20261021)
B = 2.0  # benchmark Laplace scale b


def laplace_pdf(z, b=B):
    return np.exp(-np.abs(z) / b) / (2 * b)


print("=" * 72)
print("A. Three microfoundations of Laplace(b), b =", B)
print("=" * 72)

# A1. Difference of two iid exponentials with mean b: exact density by quadrature.
def pdf_exp_diff(z, b=B):
    z = mp.mpf(z)
    lo = max(mp.mpf(0), -z)
    f = lambda s: (1 / b) * mp.e ** (-(s + z) / b) * (1 / b) * mp.e ** (-s / b)
    return mp.quad(f, [lo, lo + 10 * b, mp.inf])

print("A1. Buy volume minus sell volume, each Exp(mean b): density vs Laplace")
for z in [-6, -2, 0, 1, 3, 8]:
    print(f"   z={z:>3}: quad={mp.nstr(pdf_exp_diff(z), 12):>16}   Laplace={laplace_pdf(z):.12f}")

# A2. Normal with exponential variance: V ~ Exp(mean 2 b^2), Z | V ~ N(0, V).
def pdf_normal_exp_var(z, b=B):
    z = mp.mpf(z)
    mean_v = 2 * b ** 2
    f = lambda v: mp.e ** (-z ** 2 / (2 * v)) / mp.sqrt(2 * mp.pi * v) * mp.e ** (-v / mean_v) / mean_v
    return mp.quad(f, [0, 1, 10, 100, mp.inf])

print("A2. N(0,V), V ~ Exp(mean 2 b^2): density vs Laplace")
for z in [-6, -2, 0.5, 1, 3, 8]:
    print(f"   z={z:>4}: quad={mp.nstr(pdf_normal_exp_var(z), 12):>16}   Laplace={laplace_pdf(z):.12f}")

# A3. Brownian motion (volatility sigma) at an independent exponential time T ~ Exp(mean tau):
#     Var(W_T | T) = sigma^2 T, mean of mixing variance = sigma^2 tau = 2 b^2, so b^2 = sigma^2 tau / 2.
sigma, tau = 1.3, 2 * B ** 2 / 1.3 ** 2
print(f"A3. Brownian noise flow, sigma={sigma}, mean horizon tau={tau:.6f} => b = sqrt(sigma^2 tau/2) = {np.sqrt(sigma**2*tau/2):.6f}")
T = rng.exponential(tau, 4_000_000)
W = rng.normal(0.0, sigma * np.sqrt(T))
print("   Monte Carlo (4e6 draws) vs Laplace:")
print(f"     E|W|        = {np.mean(np.abs(W)):.4f}  (Laplace: b = {B})")
print(f"     excess kurt = {stats.kurtosis(W):.3f}  (Laplace: 3)")
for z in [1, 3, 6]:
    print(f"     P(W > {z}) = {np.mean(W > z):.5f}   Laplace: {0.5*np.exp(-z/B):.5f}")

# A4. Characteristic functions at a few t
print("A4. Characteristic function 1/(1+b^2 t^2) vs Monte Carlo for the three stories")
Eb = rng.exponential(B, 2_000_000) - rng.exponential(B, 2_000_000)
V = rng.exponential(2 * B ** 2, 2_000_000)
Nv = rng.normal(0, np.sqrt(V))
for t in [0.1, 0.3, 0.6]:
    exact = 1 / (1 + B ** 2 * t ** 2)
    print(f"   t={t}: exact={exact:.5f}  exp-diff={np.mean(np.cos(t*Eb)):.5f}  "
          f"normal-exp-var={np.mean(np.cos(t*Nv)):.5f}  BM-at-exp-time={np.mean(np.cos(t*W)):.5f}")

print()
print("=" * 72)
print("B. Discrete analogues: two-sided geometric pmf  c * th^|n|,  c = (1-th)/(1+th)")
print("=" * 72)
# B1. Geometric number N of fair +-1 orders; P(N=n) = (1-s) s^n.  Net sum S.
s = 0.9
th = (1 - np.sqrt(1 - s ** 2)) / s
Nmax = 4000
# distribution of sum of N Rademacher via binomial: S = 2K - N, K~Bin(N,1/2)
ns = np.arange(-40, 41)
pmf = np.zeros(len(ns))
for N in range(0, Nmax + 1):
    wN = (1 - s) * s ** N
    if wN < 1e-18:
        break
    # P(S=n) = C(N,(N+n)/2)/2^N when N+n even and |n|<=N
    for j, n in enumerate(ns):
        if (N + n) % 2 == 0 and abs(n) <= N:
            pmf[j] += wN * np.exp(special.gammaln(N + 1) - special.gammaln((N + n) / 2 + 1)
                                  - special.gammaln((N - n) / 2 + 1) - N * np.log(2))
c = (1 - th) / (1 + th)
print(f"B1. Geometric count (s={s}) of fair +-1 orders; theta=(1-sqrt(1-s^2))/s = {th:.6f}")
for n in [0, 1, 2, 5, 10, 20]:
    j = list(ns).index(n)
    print(f"   n={n:>2}: pmf={pmf[j]:.10f}   c*th^|n|={c*th**abs(n):.10f}")

# B2. Buy count and sell count each geometric(th) (e.g. Poisson with exponential intensity)
q = 0.55
pg = lambda n: (1 - q) * q ** n
print(f"B2. Net of two iid geometric counts, ratio q={q}")
for n in [0, 1, 3, 7]:
    tot = sum(pg(j) * pg(j + abs(n)) for j in range(0, 400))
    print(f"   n={n}: pmf={tot:.10f}   (1-q)/(1+q) q^|n|={(1-q)/(1+q)*q**abs(n):.10f}")

print()
print("=" * 72)
print("C. Maximum entropy at fixed E|Z| = b (differential entropy, nats)")
print("=" * 72)
h_lap = 1 + np.log(2 * B)
sd_gauss = B * np.sqrt(np.pi / 2)           # E|Z| = sigma sqrt(2/pi) = b
h_gauss = 0.5 * np.log(2 * np.pi * np.e * sd_gauss ** 2)
s_logis = B / (2 * np.log(2))               # E|Z| = 2 s ln 2 = b
h_logis = np.log(s_logis) + 2
nu = 3
# Student t, nu=3, scale chosen so that E|Z| = b: E|T_nu| = 2 sqrt(nu) Gamma((nu+1)/2)/(sqrt(pi)(nu-1)Gamma(nu/2))
e_abs_std = 2 * np.sqrt(nu) * special.gamma((nu + 1) / 2) / (np.sqrt(np.pi) * (nu - 1) * special.gamma(nu / 2))
sc_t = B / e_abs_std
h_t = stats.t(nu, scale=sc_t).entropy()
print(f"   Laplace    : {h_lap:.5f}")
print(f"   Gaussian   : {h_gauss:.5f}")
print(f"   Logistic   : {h_logis:.5f}")
print(f"   Student t3 : {h_t:.5f}")
print("   (all four have E|Z| = b; Laplace is largest, as the Gibbs-inequality argument says)")

print()
print("=" * 72)
print("D. Score bound and posterior bounds, b = 2 (sensitivity of orders = 2)")
print("=" * 72)
eps = 2 / B
L = np.exp(eps)
print(f"   Laplace: sup|f'/f| = 1/b = {1/B:.4f};  sup LR = e^(2/b) = {L:.6f}")
print(f"            m = 1/(1+e^(2/b)) = {1/(1+L):.6f},  M = {1-1/(1+L):.6f}")
print(f"            DP reading: eps = 2/b = {eps:.3f}; e^eps = {L:.6f}")
print()


def sup_ratio(logf, shift=2.0, lim=400.0, n=800_001):
    """sup over x of f(x)/f(x+shift) and of f(x+shift)/f(x), on a grid."""
    x = np.linspace(-lim, lim, n)
    d = logf(x) - logf(x + shift)
    return float(np.exp(np.max(d))), float(np.exp(np.max(-d)))

laws = {}
laws["Laplace(b)"] = lambda x: -np.abs(x) / B - np.log(2 * B)
laws["Logistic(b)"] = lambda x: -x / B - np.log(B) - 2 * np.log1p(np.exp(-x / B))
for nu in [1, 3, 5]:
    s_t = B * (nu + 1) / (2 * np.sqrt(nu))   # scale with sup|score| = 1/B
    laws[f"Student t nu={nu}, scale {s_t:.3f}"] = (lambda nu, s_t: (lambda x: stats.t(nu, scale=s_t).logpdf(x)))(nu, s_t)
print("   sup|score| is set to 1/b = 0.5 for each law (matching rule: the paper's |f'| <= f/b).")
print("   The worst case over flows of the likelihood ratio for orders 2 apart:")
for name, lf in laws.items():
    x = np.linspace(-60, 60, 2_400_001)
    h = 1e-5
    sc = (lf(x + h) - lf(x - h)) / (2 * h)
    r1, r2 = sup_ratio(lf)
    Lf = max(r1, r2)
    print(f"   {name:<32} sup|score|={np.max(np.abs(sc)):.5f}  sup LR={Lf:.5f}  m_f={1/(1+Lf):.5f}  (paper's m={1/(1+L):.5f})")
sig = 1.0
x = np.linspace(-60, 60, 12001)
print(f"   Gaussian(sigma=1)                 |score| = |z|/sigma^2: at z=10 -> {10:.1f}, at z=30 -> {30:.1f}; no finite bound")
print(f"            LR for orders 1 and -1 at flow x: exp(2x/sigma^2): x=5 -> {np.exp(10):.3e}; m_f = 0")

print()
print("=" * 72)
print("E. Difference of two Gamma(kappa, scale b) volumes (symmetric variance gamma)")
print("=" * 72)
def vg_logpdf(z, kappa, b=B):
    z = mp.mpf(abs(z))
    nu = kappa - mp.mpf(1) / 2
    x = z / b
    return mp.log(x ** nu * mp.besselk(nu, x)) - mp.log(mp.sqrt(mp.pi) * mp.gamma(kappa) * b * 2 ** nu)

# density check against numerical convolution for kappa=2 at z=1.7
kap = 2
z0 = 1.7
conv = mp.quad(lambda s: mp.gammapdf(s + z0, kap, B) * mp.gammapdf(s, kap, B), [0, 10, 100, mp.inf]) if hasattr(mp, "gammapdf") else None
def gam(s, k, b):
    return s ** (k - 1) * mp.e ** (-s / b) / (mp.gamma(k) * b ** k)
conv = mp.quad(lambda s: gam(s + z0, kap, B) * gam(s, kap, B), [0, 10, 100, mp.inf])
print(f"   density check kappa=2, z=1.7: Bessel formula={mp.nstr(mp.e**vg_logpdf(z0,kap),12)}  convolution={mp.nstr(conv,12)}")
print("   sup |f'/f| over z>0 (score), per kappa; the paper needs <= 1/b = 0.5:")
for kap in [0.6, 0.75, 1.0, 1.5, 2.0, 3.0, 6.0]:
    zs = [mp.mpf(10) ** e for e in np.linspace(-6, 2, 400)]
    h = mp.mpf(10) ** -12
    vals = []
    for zz in zs:
        zz = mp.mpf(zz)
        d = (vg_logpdf(zz * (1 + h), kap) - vg_logpdf(zz * (1 - h), kap)) / (2 * h * zz)
        vals.append(abs(d))
    print(f"   kappa={kap:<4}: sup score on grid z in [1e-6,1e2] = {float(max(vals)):.4f}  excess kurtosis = {3/kap:.3f}")
print("   Reading: kappa >= 1 keeps the score at or below 1/b (equal at kappa=1, Laplace); kappa < 1 has an unbounded score at z -> 0.")

print()
print("=" * 72)
print("F. Closure of the class {|f'| <= f/b}: mixtures and convolutions")
print("=" * 72)
# Laplace(b=2) convolved with N(0, 1): score bound stays <= 1/b
h = 0.002
zg = np.arange(-80, 80 + h, h)
fl = laplace_pdf(zg)
phi = stats.norm.pdf(np.arange(-12, 12 + h, h), scale=1.0)
conv = signal.fftconvolve(fl, phi, mode="same") * h
mid = (np.abs(zg) < 40)
sc = np.zeros_like(zg); sc[mid] = np.gradient(np.log(conv[mid]), h)
print(f"   Laplace(2) + N(0,1): sup|score| on |z|<40 = {np.max(np.abs(sc[mid])):.5f}  (bound 1/b = 0.5; the excess in the 5th decimal is grid error); score at z=0 is {sc[len(zg)//2]:.5f}, at z=3 is {sc[np.argmin(np.abs(zg-3))]:.5f}, at z=30 is {sc[np.argmin(np.abs(zg-30))]:.5f}")
# scale mixture of Laplace scales in [2, 4]: score bound 1/2
bs = np.array([2.0, 3.0, 4.0]); ws = np.array([0.3, 0.4, 0.3])
fm = sum(w * laplace_pdf(zg, bb) for w, bb in zip(ws, bs))
scm = np.gradient(np.log(fm), h)
print(f"   Mixture of Laplace scales (2,3,4): sup|score| = {np.max(np.abs(scm[mid])):.5f}  (bound 1/min b = 0.5)")
# asymmetric Laplace: buy volume mean 2, sell volume mean 3
def al_pdf(z, bb, bs_):
    return np.where(z >= 0, np.exp(-z / bb), np.exp(z / bs_)) / (bb + bs_)
fa = al_pdf(zg, 2.0, 3.0)
sca = np.gradient(np.log(fa), h)
print(f"   Asymmetric Laplace (buy mean 2, sell mean 3): sup|score| = {np.max(np.abs(sca[mid])):.5f}  (bound 1/min(b_B,b_S) = 0.5)")
print("   Check of the claim in the memo: bounded score is stable under mixtures and under convolution with any law.")

print()
print("=" * 72)
print("G. Posterior under full orders (q=+1 in H, q=-1 in L), equal priors: mu(x) = f(x-1)/(f(x-1)+f(x+1))")
print("   Symmetric laws with sup|score| <= 1/b: |log-odds(x)| <= min(2|x|,2)/b, with equality for Laplace.")
print("=" * 72)
def mu_from_logf(lf, x):
    d = lf(x - 1) - lf(x + 1)
    return 1 / (1 + np.exp(-d))
gauss_sd = B * np.sqrt(np.pi / 2)
gl = lambda x: stats.norm.logpdf(x, scale=gauss_sd)
tl = laws["Student t nu=3, scale 2.309"]   # same sup|score| = 1/b as Laplace and logistic
xs = np.array([0.0, 2.0, 5.0, 10.0, 20.0, 40.0])
print(f"   x            : {xs}")
print(f"   Laplace      : {np.round(mu_from_logf(laws['Laplace(b)'], xs), 6)}")
print(f"   Logistic     : {np.round(mu_from_logf(laws['Logistic(b)'], xs), 6)}")
print(f"   Student t3   : {np.round(mu_from_logf(tl, xs), 6)}   (sup|score| = 1/b; mu falls back toward 1/2 in the far tail)")
print(f"   Gaussian(E|Z|=b): {np.round(mu_from_logf(gl, xs), 6)}   -> reaches 1: no bound M < 1")
print(f"   M for Laplace(b)={B}: {1-1/(1+L):.6f}")
print("   Residual advantage factor (1 - mu) at x=40: Laplace =",
      f"{1-mu_from_logf(laws['Laplace(b)'], np.array([40.0]))[0]:.6f}",
      "; Gaussian =", f"{1-mu_from_logf(gl, np.array([40.0]))[0]:.3e}")


print()
print("=" * 72)
print("H. Fixed-profile entry at the strong benchmark (full orders), several noise laws")
print("   (h,l,p,rho,c_L,c_H,b,k) = (10,1,0.5,0.25,1,6,2,0.02), r_1 = 3. Fixed-profile: not an equilibrium check.")
print("=" * 72)
h_, l_, p_, rho_, cH_, r1_ = 10.0, 1.0, 0.5, 0.25, 6.0, 3.0
gL = (l_ ** 2 - p_ ** 2) / (2 * r1_)
gH = h_ - r1_ / 2 - p_ ** 2 / (2 * r1_)
tau_ = (cH_ - gL) / (gH - gL)
print(f"   g_L={gL:.6f}  g_H={gH:.6f}  tau={tau_:.6f}  (paper: Laplace M={1-1/(1+np.exp(2/B)):.6f} must exceed tau)")

dx = 0.001
xg = np.arange(-300, 300 + dx, dx)

def entry_for(logf, label):
    fH = np.exp(logf(xg - 1)); fL = np.exp(logf(xg + 1))
    mu = 1 / (1 + np.exp(logf(xg + 1) - logf(xg - 1)))
    mask = mu >= tau_ - 1e-12
    aH = np.sum(fH[mask]) * dx; aL = np.sum(fL[mask]) * dx
    E = rho_ + (1 - rho_) * (aH + aL) / 2
    n_int = int(np.sum(np.diff(mask.astype(int)) != 0))
    print(f"   {label:<34} sup mu={mu.max():.5f}  alpha_H={aH:.5f} alpha_L={aL:.5f}  entry E={E:.6f}  threshold-set edges={n_int}")
    return E

entry_for(laws["Laplace(b)"], "Laplace(b=2)  [paper: 0.522757]")
entry_for(laws["Logistic(b)"], "Logistic(b=2) [paper: 0.301509]")
nu_ = 2.0
def vg_logf(z, kappa=2.0, b=B):
    x = np.maximum(np.abs(z) / b, 1e-12)
    nu_v = kappa - 0.5
    return nu_v * np.log(x) + np.log(special.kve(nu_v, x)) - x - np.log(np.sqrt(np.pi) * special.gamma(kappa) * b * 2 ** nu_v)
entry_for(vg_logf, "Var-gamma kappa=2, scale b=2")
for nu in [5, 3, 1]:
    s_t = B * (nu + 1) / (2 * np.sqrt(nu))
    entry_for((lambda nu, s_t: (lambda x: stats.t(nu, scale=s_t).logpdf(x)))(nu, s_t), f"Student t nu={nu} (sup score 1/b)")
entry_for(gl, "Gaussian (E|Z| = b)")

print()
print("   Asymmetric Laplace: buy-volume mean b_B = 2, sell-volume mean b_S = 3.")
bB, bS = 2.0, 3.0
lal = lambda z: np.where(z >= 0, -z / bB, z / bS) - np.log(bB + bS)
mu_inf = lambda x: 1 / (1 + np.exp(lal(x + 1) - lal(x - 1)))
print(f"   mu(+200) = {float(mu_inf(np.array([200.0]))[0]):.6f}  vs 1/(1+e^(-2/b_B)) = {1/(1+np.exp(-2/bB)):.6f}")
print(f"   mu(-200) = {float(mu_inf(np.array([-200.0]))[0]):.6f}  vs 1/(1+e^(2/b_S))  = {1/(1+np.exp(2/bS)):.6f}")

print()
print("Pointwise check of |log-odds_f(x)| <= min(2|x|, 2)/b for symmetric laws with sup|score| = 1/b (max over x of the gap, must be <= 0):")
xx = np.linspace(-30, 30, 60001)
for name in ["Laplace(b)", "Logistic(b)", "Student t nu=1, scale 2.000", "Student t nu=3, scale 2.309", "Student t nu=5, scale 2.683"]:
    lf = laws[name]
    lo = np.abs(lf(xx - 1) - lf(xx + 1))
    env = np.minimum(2 * np.abs(xx), 2) / B
    print(f"   {name:<32} max(|log-odds| - envelope) = {np.max(lo - env):.2e}")
