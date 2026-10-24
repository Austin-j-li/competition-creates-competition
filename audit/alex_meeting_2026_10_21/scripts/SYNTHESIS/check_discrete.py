"""Red-team check 4: discrete trading menus with three-point noise.

Print-only. Exact rationals. Run from the repository root with .venv/bin/python.
"""
from fractions import Fraction as Fr
from math import sqrt

h, ell, p, rho, cL, cH, k = Fr(10), Fr(1), Fr(1, 2), Fr(1, 4), Fr(1), Fr(6), Fr(1, 50)


def auction(r):
    t0 = p * (1 - p / r)
    tH = r / 2 + p * p / (2 * r)
    tL = ell - (ell * ell - p * p) / (2 * r)
    gH = h - r / 2 - p * p / (2 * r)
    gL = (ell * ell - p * p) / (2 * r)
    return t0, tH, tL, gH, gL


def entry(r, mu):
    t0, tH, tL, gH, gL = auction(r)
    B = gL + mu * (gH - gL)
    return rho * (B >= cL) + (1 - rho) * (B >= cH)


def flows(menu, qH, qL, lam, noise=(Fr(1, 3), Fr(1, 3), Fr(1, 3))):
    """Return dict flow -> (Pr(x|H), Pr(x|L)) for pure orders qH, qL (when present, prob lam)."""
    out = {}
    for x in range(-2, 3):
        out[x] = [Fr(0), Fr(0)]
    for j, q in ((0, qH), (1, qL)):
        for z, pz in zip((-1, 0, 1), noise):
            out[q + z][j] += lam * pz
            out[0 + z][j] += (1 - lam) * pz
    return {x: tuple(v) for x, v in out.items() if v[0] + v[1] > 0}


def payoff(r, menu, qH, qL, lam, deviate_type, dev_order, ic_belief=True):
    """Expected gross-minus-cost payoff of deviate_type (0=H,1=L) choosing dev_order against the schedule
    induced by (qH,qL). Off-path flows get the Intuitive Criterion belief (H if reached by a buy, L if by a sale),
    or the prior if ic_belief is False."""
    t0, tH, tL, gH, gL = auction(r)
    DT = tH - tL
    fl = flows(menu, qH, qL, lam)
    total = Fr(0)
    for z, pz in zip((-1, 0, 1), (Fr(1, 3),) * 3):
        x = dev_order + z
        if x in fl:
            aH, aL = fl[x]
            mu = aH / (aH + aL)
        else:
            mu = (Fr(1) if dev_order > 0 else Fr(0)) if ic_belief else Fr(1, 2)
        e = entry(r, mu)
        resid = e * DT * ((1 - mu) if deviate_type == 0 else -mu)
        total += pz * resid * dev_order
    return total - k * abs(dev_order)


print("=== 1. Buy-only menu {0,1}, lambda=1: H's gain from buying against any schedule = rho*Delta_T/3 - k ===")
for r in [Fr(6, 5), Fr(3), Fr(18, 5), Fr(17, 2)]:
    t0, tH, tL, gH, gL = auction(r)
    DT = tH - tL
    gain_vs_nt = payoff(r, 'buy', 0, 0, Fr(1), 0, 1)
    gain_vs_full = payoff(r, 'buy', 1, 0, Fr(1), 0, 1)
    print(f"   r={float(r):4.1f}: rho*DT/3-k = {float(rho*DT/3-k):+.6f}; H buy vs no-trade schedule (IC belief at 2) = {float(gain_vs_nt):+.6f}; "
          f"vs full-purchase schedule = {float(gain_vs_full):+.6f}; L buy vs full = {float(payoff(r,'buy',1,0,Fr(1),1,1)):+.6f}")
rT = ell + 3 * k / rho + sqrt((3 * k / rho)**2 + 2 * ell * 3 * k / rho)
rCD = h - cH + sqrt(float((h - cH)**2 - p * p))
print(f"   cutoff r_T = frak r(3k/rho) = {rT:.9f};  r_C^D = h - c_H + sqrt((h-c_H)^2 - p^2) = {rCD:.9f}")

print()
print("=== 2. Benchmark entry path, buy-only, lambda=1, c_L=1 (floor fails at flow -1) ===")
for r in [Fr(6, 5), Fr(3), Fr(18, 5), Fr(17, 2)]:
    t0, tH, tL, gH, gL = auction(r)
    DT = tH - tL
    trade = (rho * DT / 3 > k)
    if trade:
        fl = flows('buy', 1, 0, Fr(1))
    else:
        fl = flows('buy', 0, 0, Fr(1))
    E = sum((aH + aL) / 2 * entry(r, aH / (aH + aL)) for aH, aL in fl.values())
    OH = sum(aH / 2 * entry(r, aH / (aH + aL)) for aH, aL in fl.values())
    print(f"   r={float(r):4.1f}: trade={trade}  E={E} = {float(E):.6f}  O_H={OH} = {float(OH):.6f}  g_H={float(gH):.4f} {'>=' if gH>=cH else '<'} c_H; g_L={float(gL):.4f} {'>=' if gL>=cL else '<'} c_L")

print()
print("=== 3. Factor 3/2: no-trade cutoff under the Intuitive Criterion vs passive belief at flow 2 ===")
r = Fr(3)
t0, tH, tL, gH, gL = auction(r); DT = tH - tL
print(f"   r=3: H's buy gain vs no trade, IC belief:      {float(payoff(r,'buy',0,0,Fr(1),0,1,True)+k):.6f} = rho*DT/3 = {float(rho*DT/3):.6f}")
print(f"   r=3: H's buy gain vs no trade, passive belief: {float(payoff(r,'buy',0,0,Fr(1),0,1,False)+k):.6f} = rho*DT/2 = {float(rho*DT/2):.6f}  (ratio {float((rho*DT/2)/(rho*DT/3))})")
print("   The passive-belief cutoff rho*DT/2 coincides with the continuous model's Prop. A.4 no-trade condition.")

print()
print("=== 4. Two-sided menu {-1,0,1} at r_1=3: pure-profile conditions as a function of lambda ===")
print("   T  iff k < k_T(lambda);  BNS iff k_T <= k < rho*DT/3;  SNB needs k >= rho*DT/6 + DT(1-lam)/(3(2-lam)) [e=1 at flow 1 when 1/(2-lam) >= tau]")
tau = (cH - gL) / (gH - gL)
lam_lower = 2 - 1 / tau
lam_upper = (1 - rho) / (1 - rho / 2)
print(f"   tau(r_1)={float(tau):.4f}; lambda_lower = 2 - 1/tau = {float(lam_lower):.6f} (=82/141: {lam_lower == Fr(82,141)}); lambda_upper = (1-rho)/(1-rho/2) = {float(lam_upper):.6f} (=6/7: {lam_upper == Fr(6,7)})")
for lam in [Fr(1, 2), Fr(3, 5), Fr(4, 5), Fr(17, 20), Fr(9, 10), Fr(1)]:
    mu1 = 1 / (2 - lam)
    e1 = entry(r, mu1)
    kT_H = rho * DT / 6 + e1 * DT * (1 - lam) / (3 * (2 - lam))      # H's gain under T from buying (needs > k)
    kT_L = (rho * DT / 3) * (Fr(1, 2) + (1 - lam) / (2 - lam))        # L's gain under T from selling
    kT = min(kT_H, kT_L)
    k_BNS_lo = (rho * DT / 3) * (Fr(1, 2) + (1 - lam) / (2 - lam))     # L must not sell under BNS: k >= this
    k_SNB_lo = rho * DT / 6 + e1 * DT * (1 - lam) / (3 * (2 - lam))    # H must not buy under SNB: k >= this
    k_NT = rho * DT / 3
    print(f"   lam={float(lam):.2f}: mu(+1)={float(mu1):.4f} e(+1)={float(e1):.2f}  T iff k<{float(kT):.4f}  BNS iff {float(k_BNS_lo):.4f}<=k<{float(k_NT):.4f}  "
          f"SNB iff {float(k_SNB_lo):.4f}<=k<{float(k_NT):.4f} -> SNB {'EMPTY' if k_SNB_lo >= k_NT else 'nonempty'};  benchmark k=0.02 {'< k_T: two-sided T' if k < kT else 'in partial-trade region'}")
print("   Direct deviation check at lam=4/5, k=0.02: ")
lam = Fr(4, 5)
for name, (qH, qL) in {'T': (1, -1), 'BNS': (1, 0), 'SNB': (0, -1), 'NT': (0, 0)}.items():
    best_dev = []
    for typ, q_eq in ((0, qH), (1, qL)):
        eq_pay = payoff(r, 'two', qH, qL, lam, typ, q_eq)
        devs = [(q, payoff(r, 'two', qH, qL, lam, typ, q)) for q in (-1, 0, 1) if q != q_eq]
        best_dev.append(max(v - eq_pay for _, v in devs))
    print(f"      {name}: max deviation gain (H, L) = ({float(best_dev[0]):+.5f}, {float(best_dev[1]):+.5f}) -> {'equilibrium' if max(best_dev) <= 0 else 'not an equilibrium'}")

print()
print("=== 5. Presence probability lambda, buy-only menu: E = rho + (1-rho) lam/6 (floor needs c_L <= B(m_lam)) ===")
for lam in [Fr(1, 10), Fr(1, 2), Fr(3, 4), Fr(9, 10), Fr(1)]:
    fl = flows('buy', 1, 0, lam)
    mlam = (1 - lam) / (2 - lam)
    t0, tH, tL, gH, gL = auction(Fr(3))
    Bm = gL + mlam * (gH - gL)
    E = sum((aH + aL) / 2 * entry(Fr(3), aH / (aH + aL)) for aH, aL in fl.values())
    print(f"   lam={float(lam):.2f}: m_lam={float(mlam):.4f} B(m_lam)={float(Bm):.4f} {'>=' if Bm >= cL else '<'} c_L=1;  E={float(E):.6f}  formula rho+(1-rho)lam/6={float(rho+(1-rho)*lam/6):.6f}")
lam_floor = None
# floor boundary: B(m_lam) = c_L -> m_lam = (cL - gL)/(gH - gL)
t0, tH, tL, gH, gL = auction(Fr(3))
muL = (cL - gL) / (gH - gL)
lam_floor = (1 - 2 * muL) / (1 - muL)
print(f"   buy-only floor at c_L=1, r=3: lambda <= {float(lam_floor):.6f} (=158/179: {lam_floor == Fr(158,179)})")
