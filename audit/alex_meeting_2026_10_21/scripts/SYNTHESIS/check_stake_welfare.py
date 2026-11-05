"""Red-team checks 5 and 6: stake thresholds and the welfare ledger at the benchmark.

Print-only. Run from the repository root with .venv/bin/python.
"""
from mpmath import mp, mpf, quad, exp, log, atan, inf, pi as PI

mp.dps = 30
h, ell, p, rho, cL, cH, b, k = (mpf(10), mpf(1), mpf('0.5'), mpf('0.25'), mpf(1), mpf(6), mpf(2), mpf('0.02'))
r0, r1, r2 = mpf('1.2'), mpf(3), mpf('3.6')


def auction(r):
    t0 = p * (1 - p / r); tH = r / 2 + p**2 / (2 * r); tL = ell - (ell**2 - p**2) / (2 * r)
    gH = h - r / 2 - p**2 / (2 * r); gL = (ell**2 - p**2) / (2 * r)
    return t0, tH, tL, gH, gL


m = 1 / (1 + exp(2 / b)); M = 1 - m
f = lambda z: exp(-abs(z) / b) / (2 * b)
t0, tH, tL, gH, gL = auction(r1)
DT = tH - tL; wL = tL - t0; wH = tH - t0
tau = (cH - gL) / (gH - gL); xs = (b / 2) * log(tau / (1 - tau))
mu = lambda x: 1 / (1 + exp(-(2 / b) * max(-1, min(1, x))))
e = lambda x: rho + (1 - rho) * (1 if mu(x) >= tau else 0)

print("=== 5. Stake thresholds (Q3_stake) ===")
slack = (1 - 1 / b) * rho * m * DT - k
Omega_U = 2 * b * slack / ((1 - rho) * wH)
t00, tH0, tL0, gH0, gL0 = auction(r0)
Omega_0 = 2 * b * (k - (tH0 - tL0)) / ((1 - rho) * (tH0 - t00))
print(f"   r1: t0={float(t0):.6f} tL={float(tL):.6f} tH={float(tH):.6f} wL={float(wL):.6f} wH={float(wH):.6f} DT={float(DT):.6f} tau={float(tau):.6f} x*={float(xs):.6f}")
print(f"   (A3) slack = (1-1/b) rho m DT - k = {float(slack):.6f}")
print(f"   Omega_U = 2b*slack/((1-rho) wH) = {float(Omega_U):.9f}   (memo 0.0114336479)")
print(f"   Omega_0 = 2b[k - DT(r0)]/((1-rho) wH(r0)) = {float(Omega_0):.9f}   (memo 0.0430976431)")
# J = G_L(-1) = int f(x+1) e(x) DT mu(x) dx  (L's gross residual integral at q=-1)
J_quad = quad(lambda x: f(x + 1) * e(x) * DT * mu(x), [-inf, -1, 0, xs, 1, inf])
J_closed = (DT / 2) * ((1 + rho) * m + exp(-1 / b) * (rho * (atan(exp(xs / b)) - atan(exp(-1 / b))) + atan(exp(1 / b)) - atan(exp(xs / b))))
print(f"   J = G_L(-1): quadrature {float(J_quad):.12f}, closed form (S17) {float(J_closed):.12f}   (memo 0.14073122728)")
# marginal stake value per unit stake in state L at q=-1 under the full-order schedule: wL (1-rho) f(x*+1)
stake_L = wL * (1 - rho) * f(xs + 1)
stake_H = wH * (1 - rho) * f(xs - 1)
print(f"   stake derivative per unit stake at the full-order schedule: L at q=-1: {float(stake_L):.6f} (story memo 0.033717); H at q=1: {float(stake_H):.6f} (story memo 0.197784)")
print(f"   ratio (L stake derivative)/(A3 slack) = {float(stake_L/slack):.2f}   (story memo: about 14)")
# Omega_loc: marginal trading profit of L at q=-1 against the full-order schedule divided by the stake derivative
GLprime = (J_quad - rho * m * DT) / b
marg_trade = J_quad + GLprime - k   # -dU_L^0/dq at q=-1 : G + (-1)*G'... careful: U_L^0(q) = -q G(q) - k|q|; d/dq at q=-1^+: -G(-1) + G'(-1) + k ... use memo's (S16)
Omega_loc = ((1 - 1 / b) * J_quad + rho * m * DT / b - k) / stake_L
print(f"   Omega_loc = [(1-1/b) J + rho m DT/b - k] / [wL (1-rho) f(x*+1)] = {float(Omega_loc):.9f}   (memo 2.1584629814)")
print(f"   Reconciliation: Omega_U uses worst-case stake derivative (1-rho) wH/(2b) = {float((1-rho)*wH/(2*b)):.6f} per unit stake and worst-case slack {float(slack):.6f};")
print(f"      '14 times' uses the actual L stake derivative {float(stake_L):.6f} and the same slack -> omega = 1/14 = {float(slack/stake_L):.4f};")
print(f"      Omega_loc uses the actual stake derivative and the actual marginal trading profit {float((1-1/b)*J_quad + rho*m*DT/b - k):.6f} -> 2.158.")
# no trade at r0 survives every stake: constant schedule -> stake term has zero derivative
print(f"   r0: against the no-trade schedule entry is rho at every flow, so the stake term is constant in q; correctly signed deviation earns |q|(rho DT(r0)/2 - k) = |q|*{float(rho*(tH0-tL0)/2 - k):+.6f} < 0 for every omega.")
print(f"   (A2) check at r0: B_r0(1/2)={float(gL0 + (gH0-gL0)/2):.6f} < c_H=6 < B_r0(M)={float(gL0 + M*(gH0-gL0)):.6f}: expensive entry feasible at favorable beliefs at r0 (stake memo premise correction confirmed)")

print()
print("=== 6. Welfare ledger (Q3_welfare / Q3_story) at r1 ===")
alphaH = 1 - exp((xs - 1) / b) / 2; alphaL = exp(-(xs + 1) / b) / 2
E = rho + (1 - rho) * (alphaH + alphaL) / 2
dRT = (1 - rho) / 2 * (alphaH * wH + alphaL * wL)
RT_acc = t0 + ((rho + (1 - rho) * alphaH) * wH + (rho + (1 - rho) * alphaL) * wL) / 2
RT_hid = t0 + rho * (wH + wL) / 2
phi = lambda x: f(x - 1) * f(x + 1) / (f(x - 1) + f(x + 1))
Pi_acc = DT * quad(lambda x: e(x) * phi(x), [-inf, -1, 0, xs, 1, inf])
Pi_hid = DT * rho * quad(phi, [-inf, -1, 0, 1, inf])
Pi_acc_H = quad(lambda x: f(x - 1) * e(x) * DT * (1 - mu(x)), [-inf, -1, 0, xs, 1, inf])
print(f"   entry E={float(E):.6f} alpha_H={float(alphaH):.6f} alpha_L={float(alphaL):.6f}")
print(f"   R_T access={float(RT_acc):.6f} (paper 0.872392), hidden={float(RT_hid):.6f} (paper 0.614583), Delta R_T={float(dRT):.6f} (paper dividend 0.257809)")
print(f"   Pi^acc={float(Pi_acc):.6f} (memo 0.1407) = H-leg {float(Pi_acc_H):.6f} = J above {float(J_quad):.6f};  Pi^hid={float(Pi_hid):.6f} (memo 0.0691)")
print(f"   lambda* = Delta R_T / Pi^acc = {float(dRT/Pi_acc):.4f} (memo 1.832); net gain at lambda=1: {float(dRT - Pi_acc):+.4f}")
print()
print("   Screening region (Q3_story S4b): c_H in (B_r1(m), B_r1(1/2)] -> informative price lowers proceeds. Example c_H=4 at r1:")
cH2 = mpf(4); tau2 = (cH2 - gL) / (gH - gL); xs2 = (b / 2) * log(tau2 / (1 - tau2))
aH2 = 1 - exp((xs2 - 1) / b) / 2 if xs2 > -1 else 1 - 0  # general: Pr(1+Z >= xs2)
aH2 = quad(lambda z: f(z), [xs2 - 1, inf]); aL2 = quad(lambda z: f(z), [xs2 + 1, inf])
RT_acc2 = t0 + ((rho + (1 - rho) * aH2) * wH + (rho + (1 - rho) * aL2) * wL) / 2
RT_hid2 = t0 + (wH + wL) / 2   # hidden entry = 1 since B(1/2) >= c_H
print(f"      B_r1(m)={float(gL + m*(gH-gL)):.4f}, B_r1(1/2)={float(gL + (gH-gL)/2):.4f}, tau={float(tau2):.4f} (<1/2), x*={float(xs2):.4f}")
print(f"      R_T access={float(RT_acc2):.6f} < R_T hidden={float(RT_hid2):.6f}: access lowers proceeds by {float(RT_hid2-RT_acc2):.6f} (deterrence through information)")
