"""Above the ceiling: [Pr(W|1)-Pr(W|-1)] / [P(1)-P(-1)] = s/Delta_T (slot-free). Benchmark r_2=3.6. Prints only."""
import math
h, ell, p, rho = 10.0, 1.0, 0.5, 0.25
u = math.e - 1
M = (1 + u) / (2 + u); m = 1 - M; vt = M - m
for r in (3.6, 5.0, 8.0):
    s = 1 - ell / r
    Delta = (r - ell) ** 2 / (2 * r)
    WL = ell / r
    w = lambda mu: WL + mu * s
    pw1, pwm1 = rho * w(M), rho * w(m)         # entry = rho at every order above the ceiling
    S = rho * Delta * vt                        # price spread above ceiling
    print(f"r={r}: Pr(W|1)-Pr(W|-1) = {pw1-pwm1:.6f}, S = {S:.6f}, ratio = {(pw1-pwm1)/S:.6f}, s/Delta = {s/Delta:.6f} = 2/(r-ell) = {2/(r-ell):.6f}")
# recruitment share of covariance at r_1
fbar = 0.36367592463787557
cls = fbar * rho * vt * (2 / 3)
rec = fbar * (1 - rho) * (M + (1 - M) / 3)
print("class, recruitment, share:", cls, rec, rec / (cls + rec))
print("rho*lam/2 =", rho * 0.3361217689151212 / 2)
