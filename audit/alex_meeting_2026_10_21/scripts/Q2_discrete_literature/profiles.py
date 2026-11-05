"""Print-only: which pure profiles (q_h, q_l) survive one-step deviations?

Two-sided order set {-1,0,1}, noise {-1,0,1} with probability 1/3 each, presence
probability lam, benchmark vector of the paper, k varied. Off-path flows use the
Intuitive Criterion belief: X=+2 -> mu=1, X=-2 -> mu=0 (wrong-direction trades
are strictly dominated). A trader who is indifferent does not trade.
Per-unit payoff of buying in state theta at flow x: e(mu_x) * Delta_T * (1{theta=h} - mu_x).
"""
from fractions import Fraction as F

h, ell, p, rho, cL, cH = 10.0, 1.0, 0.5, 0.25, 1.0, 6.0
Z = {-1: F(1, 3), 0: F(1, 3), 1: F(1, 3)}


def objects(r):
    gH = h - r / 2 - p * p / (2 * r)
    gL = (ell * ell - p * p) / (2 * r)
    return gH, gL, (r - ell) ** 2 / (2 * r)


def entry(mu, gH, gL):
    B = gL + mu * (gH - gL)
    return rho * (B >= cL) + (1 - rho) * (B >= cH)


def law(q, lam):
    out = {}
    for z, pz in Z.items():
        out[z] = out.get(z, 0) + (1 - lam) * pz
        out[q + z] = out.get(q + z, 0) + lam * pz
    return out


def mu_flow(qh, ql, lam):
    lh, ll = law(qh, lam), law(ql, lam)
    mu = {}
    for x in range(-2, 3):
        a, b = lh.get(x, F(0)), ll.get(x, F(0))
        mu[x] = float(a / (a + b)) if a + b > 0 else (1.0 if x > 0 else 0.0)  # IC off path
    return mu


def payoff(theta, q, mu, gH, gL, DT, k):
    tot = 0.0
    for z, pz in Z.items():
        x = q + z
        e = entry(mu[x], gH, gL)
        tot += float(pz) * q * e * DT * ((1.0 if theta == "h" else 0.0) - mu[x])
    return tot - k * abs(q)


def is_eq(qh, ql, lam, r, k):
    gH, gL, DT = objects(r)
    mu = mu_flow(qh, ql, lam)
    for theta, q in (("h", qh), ("l", ql)):
        # the on-path *mixture over the investor being absent* is irrelevant for the type's own choice
        best = max((payoff(theta, a, mu, gH, gL, DT, k), -abs(a)) for a in (-1, 0, 1))
        if (payoff(theta, q, mu, gH, gL, DT, k), -abs(q)) != best:
            return False
    return True


NAMES = {(0, 0): "NT", (1, -1): "T", (1, 0): "BNS", (0, -1): "SNB"}
r = 3.0
gH, gL, DT = objects(r)
print(f"r={r}: Delta_T={DT:.5f}; tau-entry threshold at mu=(c_H-g_L)/(g_H-g_L)={(cH-gL)/(gH-gL):.4f}")
for lam in (F(1), F(19, 20), F(9, 10), F(17, 20), F(4, 5), F(3, 5), F(1, 2)):
    print(f"\n-- lam = {lam}")
    prev = None
    for i in range(0, 241):
        kk = i * 0.00025 * DT / 0.6667            # k from 0 to about 0.15 Delta_T-scale
        eqs = [n for pr, n in NAMES.items() if is_eq(pr[0], pr[1], lam, r, kk)]
        if eqs != prev:
            print(f"   k/Delta_T from {kk/DT:.4f}: pure equilibria = {eqs}")
            prev = eqs
