"""Red-team check 3: the log-Lipschitz class, Laplace extremality, and logistic = Laplace + noise.

Print-only. Run from the repository root with .venv/bin/python.
"""
import numpy as np
from mpmath import mp, mpf, quad, exp, log, pi as PI, sinh, sqrt, inf

mp.dps = 25
b = mpf(2)

# ---- paper's logistic density (A.21): f_log(z) = e^{-z/b} / (b (1+e^{-z/b})^2)  -> standard logistic, scale b
f_lap = lambda z: exp(-abs(z) / b) / (2 * b)
f_log = lambda z: exp(-z / b) / (b * (1 + exp(-z / b))**2)
print("=== 1. Characteristic functions at common scale b=2 ===")
for t in [mpf('0.1'), mpf('0.5'), mpf(1), mpf(2)]:
    cf_log = quad(lambda z: mp.cos(t * z) * f_log(z), [-inf, 0, inf])
    cf_lap = 1 / (1 + b**2 * t**2)
    cf_log_formula = PI * b * t / sinh(PI * b * t)
    prod = mpf(1)
    for n in range(1, 4000):
        prod /= (1 + b**2 * t**2 / n**2)
    print(f"   t={float(t):.1f}: CF_log(numeric)={float(cf_log):.12f}  pi b t/sinh={float(cf_log_formula):.12f}  "
          f"Euler product(n<4000)={float(prod):.12f}  ratio CF_log/CF_lap={float(cf_log/cf_lap):.12f} (=CF of W, must be a valid CF <=1)")

print()
print("=== 2. Convolution: Laplace(b) * W, W density (3/(8b)) sech^4(z/(2b)), reproduces the logistic density ===")
f_W = lambda z: (3 / (8 * b)) * mp.sech(z / (2 * b))**4
print(f"   int W = {float(quad(f_W, [-inf, 0, inf])):.12f}")
for z in [mpf(0), mpf('0.7'), mpf(2), mpf(5)]:
    conv = quad(lambda u: f_lap(z - u) * f_W(u), [-inf, z - 1, z, z + 1, inf])
    print(f"   z={float(z):.1f}: (Laplace*W)(z)={float(conv):.12f}  f_log(z)={float(f_log(z)):.12f}")
print("   Verdict: logistic(b) = Laplace(b) + independent W at the paper's parametrization (scale b in both).")

print()
print("=== 3. Blackwell comparison at full orders (1,-1): G(tau) = E[(mu - tau)_+], prior 1/2 ===")
def G_curve(f, taus):
    out = []
    for tau in taus:
        def integrand(x):
            aH = f(x - 1); aL = f(x + 1)
            mu = aH / (aH + aL)
            return max(mu - tau, 0) * (aH + aL) / 2
        out.append(quad(integrand, [-inf, -1, 0, 1, inf]))
    return out
taus = [mpf(x) for x in ['0.3', '0.4', '0.5', '0.55', '0.6', '0.65', '0.7', '0.72']]
G_lap = G_curve(f_lap, taus)
G_log = G_curve(f_log, taus)
s_var = b * sqrt(6) / PI           # logistic scale with the Laplace variance 2b^2
f_log_v = lambda z: exp(-z / s_var) / (s_var * (1 + exp(-z / s_var))**2)
G_logv = G_curve(f_log_v, taus)
print("   tau     G_Laplace   G_logistic(common b)  diff     G_logistic(matched var)  diff")
for tau, a, c, d in zip(taus, G_lap, G_log, G_logv):
    print(f"   {float(tau):.2f}   {float(a):.6f}    {float(c):.6f}          {float(a-c):+.6f}   {float(d):.6f}            {float(a-d):+.6f}")
print("   Verdict: at common scale, Laplace >= logistic at every tau (dominance); at matched variance the sign changes (curves cross).")

print()
print("=== 4. Entry at the strong benchmark under full orders: Laplace vs logistic (paper's numbers) ===")
h, ell, p, rho, cH, k = mpf(10), mpf(1), mpf('0.5'), mpf('0.25'), mpf(6), mpf('0.02')
r1 = mpf(3)
gL = (ell**2 - p**2) / (2 * r1); gH = h - r1 / 2 - p**2 / (2 * r1); DT = (r1 - ell)**2 / (2 * r1)
tau = (cH - gL) / (gH - gL)
m = 1 / (1 + exp(2 / b)); M = 1 - m
def entry(f):
    # alpha_theta = Pr(mu_f(q_theta + Z) >= tau)
    def mu(x):
        aH = f(x - 1); aL = f(x + 1)
        return aH / (aH + aL)
    aH = quad(lambda z: f(z) * (1 if mu(1 + z) >= tau else 0), [-inf, -3, -1, 0, 1, 3, inf])
    aL = quad(lambda z: f(z) * (1 if mu(-1 + z) >= tau else 0), [-inf, -3, -1, 0, 1, 3, 10, inf])
    return rho + (1 - rho) * (aH + aL) / 2, aH, aL
E_lap = rho + (1 - rho) * ((1 - exp(((b / 2) * log(tau / (1 - tau)) - 1) / b) / 2) + exp(-((b / 2) * log(tau / (1 - tau)) + 1) / b) / 2) / 2
E_log, aH_log, aL_log = entry(f_log)
# paper's closed form (A.23)
A = exp(1 / b); w = sqrt(tau / (1 - tau))
xs_log = b * log((A * w - 1) / (A - w))
aH_cf = 1 / (1 + exp((xs_log - 1) / b)); aL_cf = 1 / (1 + exp((xs_log + 1) / b))
E_log_cf = rho + (1 - rho) * (aH_cf + aL_cf) / 2
print(f"   tau={float(tau):.4f}, m={float(m):.6f}, M={float(M):.6f}")
print(f"   Laplace closed form entry = {float(E_lap):.6f} (paper 0.522757)")
print(f"   Logistic entry, closed form (A.23): x*_log={float(xs_log):.9f} (paper 5.424598398), entry={float(E_log_cf):.6f} (paper 0.301509); indicator quadrature gave {float(E_log):.6f}")
print("   Entry is not ordered by Blackwell dominance (Pr(mu >= tau) is not convex in mu); both numbers stand.")

print()
print("=== 5. R16 ingredients for the Student t member (nu=3, L=1/2) ===")
nu = mpf(3); L = mpf('0.5'); sigma = (nu + 1) / (2 * L * sqrt(nu))
print(f"   sigma for L=1/2: {float(sigma):.6f} (memo: 2.309)")
f_t = lambda z: mp.gamma((nu + 1) / 2) / (mp.gamma(nu / 2) * sqrt(nu * PI) * sigma) * (1 + (z / sigma)**2 / nu)**(-(nu + 1) / 2)
score = lambda z: (nu + 1) * z / (nu * sigma**2 + z**2)
zs = np.linspace(-30, 30, 6001)
print(f"   max |score| on grid: {max(float(abs(score(mpf(z)))) for z in zs):.6f}  (attained at |z|=sigma sqrt(nu)={float(sigma*sqrt(nu)):.4f})")
mu_t = lambda x: f_t(x - 1) / (f_t(x - 1) + f_t(x + 1))
xs = np.linspace(-20, 40, 12001)
mus = [float(mu_t(mpf(x))) for x in xs]
imax = int(np.argmax(mus))
print(f"   sup mu_t(x) under full orders = {mus[imax]:.6f} at x={xs[imax]:.3f} (memo: 0.7291 at 4.12); M={float(M):.6f}; tau={float(tau):.4f} < sup mu_t: {tau < mus[imax]}")
print(f"   K_f = e^{{2L}} = {float(exp(2*L)):.4f}; m_f = 1/(1+K_f) = {float(1/(1+exp(2*L))):.6f} >= m (Laplace) = {float(m):.6f}")
E_t, aH_t, aL_t = entry(f_t)
print(f"   Student t entry = {float(E_t):.6f} (memo 0.3750)")
