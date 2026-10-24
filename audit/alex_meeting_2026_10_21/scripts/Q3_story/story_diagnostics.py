"""Print-only diagnostics for memo Q3_story (who the investors are, and t_0).

Run from the project root:
    .venv/bin/python audit/alex_meeting_2026_10_21/scripts/Q3_story/story_diagnostics.py

The script computes and prints. It asserts nothing and writes no files.
Parts:
  A. Auction objects and the entry increments t_theta - t_0 at r_0, r_1, r_2.
  B. Where t_0 enters the price: the jump of P at the entry threshold.
  C. Laplace noise as liquidity sales minus liquidity purchases; split of the
     informed profit between the two sides (full orders, r_1).
  D. Sign of the shareholder gain from price access as c_H crosses B_r(1/2).
  E. Sign and size of the stake incentive at the fixed full-order schedule.
  F. A reserve that excludes the low value: t_L = t_0 and the spread Delta_T(r).
"""
import math

import numpy as np
from scipy.integrate import quad

H, ELL, P_RES, RHO, C_L, C_H, B, K = 10.0, 1.0, 0.5, 0.25, 1.0, 6.0, 2.0, 0.02
R0, R1, R2 = 1.2, 3.0, 3.6
M_LO = 1.0 / (1.0 + math.exp(2.0 / B))
M_HI = 1.0 - M_LO


def f(z, b=B):
    return math.exp(-abs(z) / b) / (2.0 * b)


def objects(r, p=P_RES, ell=ELL, h=H):
    t0 = p * (1.0 - p / r)
    tH = r / 2.0 + p * p / (2.0 * r)
    tL = ell - (ell * ell - p * p) / (2.0 * r)
    gH = h - r / 2.0 - p * p / (2.0 * r)
    gL = (ell * ell - p * p) / (2.0 * r)
    return dict(t0=t0, tH=tH, tL=tL, gH=gH, gL=gL, DT=tH - tL)


def B_r(o, mu):
    return o["gL"] + mu * (o["gH"] - o["gL"])


def mu_full(x):
    # posterior of H at flow x under full orders, from the log likelihood ratio
    return 1.0 / (1.0 + math.exp((abs(x - 1.0) - abs(x + 1.0)) / B))


def entry_full(o, x, c_h=C_H, access=True):
    """Cost-averaged entry at flow x under full orders (c_L < B_r(m) assumed)."""
    mu = mu_full(x) if access else 0.5
    return RHO + (1.0 - RHO) * (1.0 if B_r(o, mu) >= c_h else 0.0)


def threshold_flow(o, c_h=C_H):
    tau = (c_h - o["gL"]) / (o["gH"] - o["gL"])
    if tau <= M_LO:
        return tau, -math.inf
    if tau >= M_HI:
        return tau, math.inf
    return tau, (B / 2.0) * math.log(tau / (1.0 - tau))


def integrate(fun, xstar):
    pts = sorted({-1.0, 1.0} | ({xstar} if math.isfinite(xstar) else set()))
    edges = [-math.inf] + pts + [math.inf]
    return sum(quad(fun, lo, hi, limit=200)[0] for lo, hi in zip(edges[:-1], edges[1:]))


def proceeds(o, c_h=C_H, access=True):
    """Expected target proceeds R_T under full orders (q_H, q_L) = (1, -1)."""
    _, xs = threshold_flow(o, c_h)
    eH = integrate(lambda x: f(x - 1.0) * entry_full(o, x, c_h, access), xs)
    eL = integrate(lambda x: f(x + 1.0) * entry_full(o, x, c_h, access), xs)
    RT = o["t0"] + 0.5 * (eH * (o["tH"] - o["t0"]) + eL * (o["tL"] - o["t0"]))
    return RT, eH, eL


def surplus(o, r, eH, eL, c_h=C_H, access=True):
    """Acquisition surplus net of preparation costs (Appendix A.6 accounting)."""
    w0 = (r * r - P_RES ** 2) / (2.0 * r)
    w = {t: ((r * r + t * t) / (2.0 * r) if t < r else t) for t in (ELL, H)}
    alloc = 0.5 * (eH * w[H] + (1 - eH) * w0) + 0.5 * (eL * w[ELL] + (1 - eL) * w0)
    # high-cost preparation probability, averaged over states
    hc = 0.5 * ((eH - RHO) + (eL - RHO))
    return alloc - RHO * C_L - hc * c_h


print("=" * 72)
print("A. Auction objects; entry raises proceeds in both states")
print("=" * 72)
for name, r in (("r_0", R0), ("r_1", R1), ("r_2", R2)):
    o = objects(r)
    print(f"{name}={r}: t0={o['t0']:.6f} tL={o['tL']:.6f} tH={o['tH']:.6f} "
          f"tL-t0={o['tL'] - o['t0']:.6f} tH-t0={o['tH'] - o['t0']:.6f} DeltaT={o['DT']:.6f}")
print("Limit p -> 0 at r_1: t0 -> 0, tL - t0 ->", f"{ELL - ELL * ELL / (2 * R1):.6f}",
      "(the entry increment survives the normalization)")

print()
print("=" * 72)
print("B. Price jump at the entry threshold: P(tau+) - P(tau-) = (1-rho)(w_L + DeltaT tau)")
print("=" * 72)
o1 = objects(R1)
tau, xs = threshold_flow(o1)
wL = o1["tL"] - o1["t0"]
jump = (1 - RHO) * (wL + o1["DT"] * tau)
print(f"r_1: tau={tau:.6f} x*={xs:.6f} w_L=t_L-t_0={wL:.6f} jump={jump:.6f}")
print(f"  share of the jump from w_L: {(1 - RHO) * wL / jump:.4f}; "
      f"price would fall across the jump only if w_L < -DeltaT*tau = {-o1['DT'] * tau:.6f}")
print(f"  A3 slack at r_1: (1-1/b) rho m DeltaT - k = "
      f"{(1 - 1 / B) * RHO * M_LO * o1['DT'] - K:.6f}")

print()
print("=" * 72)
print("C. Laplace noise Z = Zplus - Zminus (independent exponentials, mean b)")
print("=" * 72)
rng = np.random.default_rng(20261021)
n = 2_000_000
zp, zm = rng.exponential(B, n), rng.exponential(B, n)
z = zp - zm
for lo, hi in ((-1.5, -0.5), (-0.25, 0.25), (0.5, 1.5)):
    sel = (z > lo) & (z < hi)
    zc = z[sel]
    print(f"  Z in ({lo},{hi}): MC E[Z+|Z]={zp[sel].mean():.4f}  formula "
          f"E[max(Z,0)]+b/2={np.maximum(zc, 0).mean() + B / 2:.4f}; MC E[Z-|Z]={zm[sel].mean():.4f}"
          f"  formula={np.maximum(-zc, 0).mean() + B / 2:.4f}")
print(f"  MC density check at 0: hist={np.mean(np.abs(z) < 0.01) / 0.02:.4f}  f(0)={f(0):.4f}")

for access in (True, False):
    _, xs1 = threshold_flow(o1)

    def adv_H(x):
        e = entry_full(o1, x, access=access)
        mu = mu_full(x)
        return e * o1["DT"] * (1.0 - mu)

    def adv_L(x):
        e = entry_full(o1, x, access=access)
        mu = mu_full(x)
        return e * o1["DT"] * mu

    # Informed gross profit: state H buys 1 (Z = x - 1), state L sells 1 (Z = x + 1).
    PiH = integrate(lambda x: f(x - 1.0) * adv_H(x), xs1)
    PiL = integrate(lambda x: f(x + 1.0) * adv_L(x), xs1)
    Pi = 0.5 * (PiH + PiL)
    # Liquidity trading gains E[Zplus (V-P)] and -E[Zminus (V-P)], using E[Z+-|Z] = Z^+- + b/2.
    # In state H, V-P = +A_H at flow x and Z = x - 1; in state L, V-P = -A_L and Z = x + 1.
    gain_buy = 0.5 * integrate(lambda x: f(x - 1.0) * max(x - 1.0, 0.0) * adv_H(x), xs1) \
        - 0.5 * integrate(lambda x: f(x + 1.0) * max(x + 1.0, 0.0) * adv_L(x), xs1)
    gain_sell = -(0.5 * integrate(lambda x: f(x - 1.0) * max(1.0 - x, 0.0) * adv_H(x), xs1)
                  - 0.5 * integrate(lambda x: f(x + 1.0) * max(-x - 1.0, 0.0) * adv_L(x), xs1))
    lab = "access" if access else "hidden"
    print(f"  r_1 {lab}: informed gross Pi={Pi:.6f} (legs {PiH:.6f}, {PiL:.6f}); "
          f"liquidity buyers' gain={gain_buy:.6f}; liquidity sellers' gain={gain_sell:.6f}; "
          f"sum={gain_buy + gain_sell:.6f}")
    print(f"      expected units: buyers b={B}, sellers b={B}; per-unit loss buyers={-gain_buy / B:.6f}, "
          f"sellers={-gain_sell / B:.6f}")

print()
print("=" * 72)
print("D. Price access and expected proceeds at r_1 as c_H varies (full orders)")
print("=" * 72)
print(f"  B_r1(m)={B_r(o1, M_LO):.6f}  B_r1(1/2)={B_r(o1, 0.5):.6f}  B_r1(M)={B_r(o1, M_HI):.6f}")
print("  c_H    tau     E_acc    E_hid    R_T acc   R_T hid   dR_T      W acc     W hid     dW")
for ch in (3.0, 3.6, 4.0, 4.25, 4.35, 5.0, 6.0, 6.8):
    ta, _ = threshold_flow(o1, ch)
    RTa, eHa, eLa = proceeds(o1, ch, True)
    RTh, eHh, eLh = proceeds(o1, ch, False)
    Wa = surplus(o1, R1, eHa, eLa, ch, True)
    Wh = surplus(o1, R1, eHh, eLh, ch, False)
    print(f"  {ch:4.2f}  {ta:6.4f}  {0.5 * (eHa + eLa):7.5f}  {0.5 * (eHh + eLh):7.5f}  "
          f"{RTa:8.6f}  {RTh:8.6f}  {RTa - RTh:+8.6f}  {Wa:8.6f}  {Wh:8.6f}  {Wa - Wh:+8.6f}")
print("  (c_L=1 < B_r1(m) in every row, so the floor and the A.6 bound hold; orders are full.)")

print()
print("=" * 72)
print("E. Stake incentive at the fixed full-order schedule, r_1 (illustrative)")
print("=" * 72)
_, xs1 = threshold_flow(o1)
for theta, inc, q in (("H", o1["tH"] - o1["t0"], 1.0), ("L", o1["tL"] - o1["t0"], -1.0)):
    d_entry = (1 - RHO) * f(xs1 - q)   # d/dq Pr(q + Z >= x*) at the candidate order
    print(f"  state {theta}: d entry/dq at q={q:+.0f} is {d_entry:.6f} > 0; "
          f"marginal stake value per unit stake = {inc * d_entry:.6f} (favours buying)")
slack = (1 - 1 / B) * RHO * M_LO * o1["DT"] - K
print(f"  A3 slack (lower bound on the marginal trading profit, net of k): {slack:.6f}")
print(f"  ratio of the L-state marginal stake value to this slack: "
      f"{(o1['tL'] - o1['t0']) * (1 - RHO) * f(xs1 + 1.0) / slack:.2f}")

print()
print("=" * 72)
print("F. Reserve that excludes the low value (atom model, ell < p < r)")
print("=" * 72)


def objects_excl(r, p, h=H):
    """Low-value challenger has no admissible bid: t_L = t_0 and g_L = 0."""
    t0 = p * (1.0 - p / r)
    tH = r / 2.0 + p * p / (2.0 * r)
    gH = h - r / 2.0 - p * p / (2.0 * r)
    return dict(t0=t0, tH=tH, tL=t0, gH=gH, gL=0.0, DT=tH - t0)


p_ex = 1.1
for r in (1.2, 1.5, math.sqrt(3) * p_ex, 2.5, 3.0, 3.6):
    o = objects_excl(r, p_ex)
    closed = ((r - p_ex) ** 2 + 2 * p_ex ** 2) / (2 * r)
    print(f"  p={p_ex} r={r:.4f}: t0={o['t0']:.6f} tL-t0={o['tL'] - o['t0']:.1f} "
          f"DeltaT={o['DT']:.6f} (closed form {closed:.6f}) dDeltaT/dr={(r * r - 3 * p_ex ** 2) / (2 * r * r):+.4f}")
m1 = 1.0 / (1.0 + math.exp(-1.0 / B))
print(f"  one-sided posterior bound M_1 = 1/(1+e^(-1/b)) = {m1:.6f}; two-sided M = {M_HI:.6f}")
o0 = objects(R0)
tau0 = (C_H - o0["gL"]) / (o0["gH"] - o0["gL"])
print(f"  benchmark r_0: tau_r0={tau0:.6f}; B_r0(M_1)={B_r(o0, m1):.6f} vs c_H={C_H}; "
      f"B_r0(M)={B_r(o0, M_HI):.6f}")
