"""Benchmark numbers for the winner gap: reproduce the paper's values, then the full hump in r.
Prints only; no assertions."""
import math

h, ell, p, rho, c_H, k, pi = 10.0, 1.0, 0.5, 0.25, 6.0, 1 / 50, 0.5
beta = 294655 / 10**6
e = math.e
u = e - 1                      # 1 + u = e
M = (1 + u) / (2 + u)          # top posterior at prior 1/2
m = 1 / (2 + u)
vartheta = M - m
print("M, m, vartheta =", M, m, vartheta)
print("paper theta_B  = 0.462117")

# slot: b = (1-lam)*beta, u = lam/b  ->  lam = u*b ; b = (1-lam)beta
# solve lam: lam = u*(1-lam)*beta -> lam = u*beta/(1+u*beta)
lam = u * beta / (1 + u * beta)
b = (1 - lam) * beta
fbar = b + lam / 2
v = 2 * b + lam
print("lam, b, fbar, v =", lam, b, fbar, v, " (paper vol_full_B = 0.727352)")
print("check u = lam/b:", lam / b, " vartheta = lam/v:", lam / v)


def W(r, theta):
    """win probability of a prepared challenger with value theta vs U[0,r]"""
    return min(theta / r, 1.0)


def gap(r):
    return W(r, h) - W(r, ell)


for r in (1.2, 3.0, 3.6):
    print(f"r={r}: W_H={W(r,h):.4f} W_L={W(r,ell):.4f} W_H-W_L={gap(r):.6f} winner-gap={vartheta*gap(r):.6f}")
print("paper wgap_r1_B = 0.308078, wgap_r2_B = 0.333751")

# covariance decomposition
def Delta(r):
    return (r - ell) ** 2 / (2 * r) if r <= h else None


def B_r(r, mu):
    gH = h - r / 2 - p * p / (2 * r)
    gL = (ell**2 - p**2) / (2 * r)
    return gL + mu * (gH - gL)


rC = 3.592659
for r, chi in ((3.0, 1), (3.6, 0)):
    s = gap(r)
    w1 = M * W(r, h) + (1 - M) * W(r, ell)
    class_ch = fbar * rho * vartheta * s
    rec_ch = fbar * (1 - rho) * chi * w1
    print(f"r={r}: chi={chi}, B_r(M)={B_r(r,M):.4f} vs c_H={c_H}")
    print(f"   class channel={class_ch:.6f} recruitment channel={rec_ch:.6f} total={class_ch+rec_ch:.6f}")
    print(f"   alt formula rho*lam/2*s = {rho*lam/2*s:.6f}  (class channel only)")
print("paper cov_win_r1_B = 0.251863, cov_win_r2_B = 0.030344")

# winner-impact asymmetry (purchase impact on winning minus sale impact on winning)
for r, chi in ((3.0, 1), (3.6, 0)):
    s = gap(r)
    w = lambda mu: W(r, ell) + mu * s
    e_plus = rho + (1 - rho) * chi
    pw1, pw0, pwm1 = e_plus * w(M), rho * w(0.5), rho * w(m)
    print(f"r={r}: Pr(W|1)={pw1:.5f} Pr(W|0)={pw0:.5f} Pr(W|-1)={pwm1:.5f}")
    print(f"   purchase impact={pw1-pw0:.5f}, sale impact={pw0-pwm1:.5f}, difference={(pw1-pw0)-(pw0-pwm1):.5f}"
          f"  (1-rho)*chi*w1 = {(1-rho)*chi*w(M):.5f}")

# full hump of the benchmark classes
print("\nHump of the benchmark gap (vartheta * E_F D):")
for r in (0.8, 1.0, 1.2, 2.0, 3.0, 3.6, 5.0, 8.0, 10.0, 12.0, 15.0, 20.0, 40.0):
    print(f"  r={r:5.1f}  gap={vartheta*gap(r):.5f}   split prob={gap(r):.5f}   Lambda=W_H/W_L={W(r,h)/W(r,ell):.4f}")

# margins: where is the benchmark relative to the peak at r=h?
print("\nmargin h - r_max =", h - 3.6, " ratio h/r_max =", h / 3.6)
# D(r) - avg D for uniform: equals ell/r
for r in (1.2, 3.0, 3.6):
    print(f"  r={r}: D(r)-avg = {1 - (r-ell)/r:.4f} = ell/r = {ell/r:.4f}")
