"""Recompute the numbers of chapter 01 (the paper in brief) from the primitives.

Run: python3 verify/01_brief.py
The script prints. It does not assert anything.

Parts:
  1. The benchmark slot: lambda, b, b0, u, M(1/2), m(1/2), kappa(1/2).
  2. Acquisition payoffs at r0, r1, r2 (paper (6)) and tau(r).
  3. The three hypotheses (H1)-(H3) of Proposition 2 and their margins.
  4. The three equilibria: orders, posteriors, entry after each order,
     prices, entry, high-class ownership, expected target proceeds.
  5. The two controls of Table 3 (frozen full orders, hidden price).
  6. The admissible band of u at the prior 1/2.
  7. Cross-checks of the coexistence strengths r_A, r_F, r_N, r_C and
     entry at r_A (chapter 08 derives them).
  8. Cross-checks of the research numbers at 1.55, 1.60, 1.65
     (chapter 09 derives them).
"""

from fractions import Fraction as Fr
from pathlib import Path
import re

import mpmath as mp

mp.mp.dps = 40

SNAPSHOT = Path("/tmp/ccc_slot_scan/guide/manuscript_c78e2c3/slot/manuscript/numbers.tex")


def registry():
    if not SNAPSHOT.exists():
        return {}
    pat = re.compile(r"\\csname reg@([A-Za-z0-9_]+)\\endcsname\{([^}]*)\}")
    return dict(pat.findall(SNAPSHOT.read_text()))


REG = registry()


def reg(key):
    return REG.get(key, "(not in registry)")


def d6(x):
    return f"{float(x):.6f}"


def mpf(x):
    if isinstance(x, Fr):
        return mp.mpf(x.numerator) / x.denominator
    return mp.mpf(x)


# ---------------------------------------------------------------------------
# Primitives (paper Section 4.2).
# ---------------------------------------------------------------------------
h, ell, p, rho, cH, k, pi = Fr(10), Fr(1), Fr(1, 2), Fr(1, 4), Fr(6), Fr(1, 50), Fr(1, 2)
STRENGTHS = {"r0": Fr(6, 5), "r1": Fr(3), "r2": Fr(18, 5)}
beta = mp.mpf("0.294655")  # exact decimal declaration
u = mp.e - 1  # 1 + u = e

# ---------------------------------------------------------------------------
# 1. The slot.
# ---------------------------------------------------------------------------
lam = u * beta / (1 + u * beta)  # from u = lambda / ((1 - lambda) beta)
b = (1 - lam) * beta
b0 = (1 - lam) * (1 - 2 * beta)


def M_of(prior, uu=u):
    prior = mpf(prior)
    return prior * (1 + uu) / (prior * (1 + uu) + 1 - prior)


def m_of(prior, uu=u):
    prior = mpf(prior)
    return prior / (prior + (1 - prior) * (1 + uu))


M, m = M_of(pi), m_of(pi)
kappa = min(m, 1 - M)

print("=" * 78)
print("1. The benchmark slot (1+u = e, beta = 0.294655)")
print("=" * 78)
print(f"  u = e - 1          = {d6(u)}   registry u_B {reg('u_B')}")
print(f"  lambda = u beta/(1+u beta) = {d6(lam)}   registry lambda_B {reg('lambda_B')}")
print(f"  b = (1-lambda) beta = {d6(b)}   registry b_B {reg('b_B')}")
print(f"  b0 = (1-lambda)(1-2beta) = {d6(b0)}   registry b0_B {reg('b0_B')}   (b0 >= b: {b0 >= b})")
print(f"  check lambda/b = {d6(lam / b)}")
print(f"  M(1/2) = e/(1+e)   = {d6(M)}   registry M_half_B {reg('M_half_B')}")
print(f"  m(1/2) = 1/(1+e)   = {d6(m)}   registry m_half_B {reg('m_half_B')}")
print(f"  kappa(1/2) = min(m, 1-M) = {d6(kappa)};  1/(2+u) = {d6(1 / (2 + u))}")

# ---------------------------------------------------------------------------
# 2. Payoffs.
# ---------------------------------------------------------------------------


def payoffs(r):
    t0 = p * (1 - p / r)
    tH = r / 2 + p**2 / (2 * r)
    tL = ell - (ell**2 - p**2) / (2 * r)
    gH = h - tH
    gL = (ell**2 - p**2) / (2 * r)
    D = (r - ell) ** 2 / (2 * r)
    tau = (cH - gL) / (gH - gL)
    return dict(t0=t0, tH=tH, tL=tL, gH=gH, gL=gL, D=D, tau=tau)


PAY = {n: payoffs(r) for n, r in STRENGTHS.items()}


def B(n, mu):
    P = PAY[n]
    return mpf(P["gL"]) + mpf(mu) * mpf(P["gH"] - P["gL"])


print("\n" + "=" * 78)
print("2. Payoffs and thresholds")
print("=" * 78)
for n, r in STRENGTHS.items():
    P = PAY[n]
    print(f"  {n} = {r}: B(1/2) = {d6(B(n, Fr(1, 2)))}, Delta = {P['D']} = {d6(P['D'])},"
          f" tau = {P['tau']} = {d6(P['tau'])}, B(M) = {d6(B(n, M))}")

# ---------------------------------------------------------------------------
# 3. Hypotheses.
# ---------------------------------------------------------------------------
print("\n" + "=" * 78)
print("3. Hypotheses of Proposition 2 at the benchmark")
print("=" * 78)
D0, D1, D2 = (mpf(PAY[n]["D"]) for n in ["r0", "r1", "r2"])
print(f"  (H1) B0(pi) = {d6(B('r0', pi))} < cH = 6 < B1(M) = {d6(B('r1', M))}"
      f"   margins {d6(6 - B('r0', pi))} and {d6(B('r1', M) - 6)}"
      f"   registry margin_weakcost_B {reg('margin_weakcost_B')}, margin_recruit_B {reg('margin_recruit_B')}")
print(f"  (H2) Delta0 = {d6(D0)} < k = 0.02 < rho kappa Delta1 = {d6(mpf(rho) * kappa * D1)}"
      f"   margins {d6(mpf(k) - D0)} and {d6(mpf(rho) * kappa * D1 - mpf(k))}"
      f"   registry margin_kweak_B {reg('margin_kweak_B')}, margin_kstrong_B {reg('margin_kstrong_B')}")
print(f"  (H3) B2(M) = {d6(B('r2', M))} < cH = 6   margin {d6(6 - B('r2', M))}"
      f"   registry margin_return_B {reg('margin_return_B')}")
print(f"  At r2: rho kappa Delta2 - k = {d6(mpf(rho) * kappa * D2 - mpf(k))}"
      f"   registry margin_kstrong2_B {reg('margin_kstrong2_B')}")
print(f"  Ratio Delta0/Delta1 = {d6(D0 / D1)} < rho kappa = {d6(mpf(rho) * kappa)}"
      " (the trading-cost window is nonempty)")

# ---------------------------------------------------------------------------
# 4. The three equilibria.
# ---------------------------------------------------------------------------
ORDERS = [-1, 0, 1]
eta = {-1: beta, 0: 1 - 2 * beta, 1: beta}


def outcome(n, sigH, sigL, see_price=True):
    """Bayes posteriors, entry (rule C1), prices and aggregates for a profile."""
    P = PAY[n]
    t0, tH, tL, D = (mpf(P[x]) for x in ["t0", "tH", "tL", "D"])
    tau = mpf(P["tau"])
    f = {j: {x: (1 - lam) * eta[x] + lam * s[x] for x in ORDERS}
         for j, s in [("H", sigH), ("L", sigL)]}
    pr = {x: mpf(pi) * f["H"][x] + (1 - mpf(pi)) * f["L"][x] for x in ORDERS}
    mu = {x: mpf(pi) * f["H"][x] / pr[x] for x in ORDERS}
    if see_price:
        e = {x: mpf(1) if mu[x] >= tau else mpf(rho) for x in ORDERS}
    else:
        e = {x: mpf(1) if mpf(pi) >= tau else mpf(rho) for x in ORDERS}
    price = {x: t0 + e[x] * (tL - t0 + D * mu[x]) for x in ORDERS}
    entry = sum(pr[x] * e[x] for x in ORDERS)
    entry_H = sum(f["H"][x] * e[x] for x in ORDERS)
    own_H = mpf(pi) * entry_H * 1  # W_H = 1: a high-value challenger always wins
    proceeds = sum(pr[x] * price[x] for x in ORDERS)
    return dict(mu=mu, e=e, price=price, entry=entry, entry_H=entry_H, own=own_H, proceeds=proceeds)


NONE = {-1: 0, 0: 1, 1: 0}
BUY = {-1: 0, 0: 0, 1: 1}
SELL = {-1: 1, 0: 0, 1: 0}

EQ = {
    "r0": outcome("r0", NONE, NONE),
    "r1": outcome("r1", BUY, SELL),
    "r2": outcome("r2", BUY, SELL),
}

print("\n" + "=" * 78)
print("4. Equilibria of Proposition 2 (orders: r0 none; r1, r2 class H buys, class L sells)")
print("=" * 78)
REGK = {
    "r0": dict(entry="entry_r0", own="own_r0", proceeds="p4_base_r0_proceeds",
               price={-1: "price_r0", 0: "price_r0", 1: "price_r0"}),
    "r1": dict(entry="entry_r1_B", own="own_r1_B", proceeds="p4_base_r1_proceeds",
               price={-1: "price_r1_m1_B", 0: "price_r1_0_B", 1: "price_r1_p1_B"}),
    "r2": dict(entry="entry_r2", own="own_r2_B", proceeds="p4_base_r2_proceeds",
               price={-1: "price_r2_m1_B", 0: "price_r2_0_B", 1: "price_r2_p1_B"}),
}
for n in ["r0", "r1", "r2"]:
    E = EQ[n]
    rk = REGK[n]
    print(f"\n  {n}:")
    print("    posteriors (sale, none, purchase): " + ", ".join(d6(E['mu'][x]) for x in ORDERS))
    print("    entry after each order:            " + ", ".join(d6(E['e'][x]) for x in ORDERS))
    print("    prices:                            " + ", ".join(d6(E['price'][x]) for x in ORDERS)
          + "   registry " + ", ".join(reg(rk['price'][x]) for x in ORDERS))
    print(f"    informative (prices differ): {len(set(round(float(E['price'][x]), 12) for x in ORDERS)) > 1}")
    print(f"    entry E = {d6(E['entry'])}   registry {reg(rk['entry'])}")
    print(f"    entry given class H = {d6(E['entry_H'])}")
    print(f"    high-class ownership O_H = {d6(E['own'])}   registry {reg(rk['own'])}")
    print(f"    expected target proceeds = {d6(E['proceeds'])}   registry {reg(rk['proceeds'])}")
print(f"\n  Entry formula at r1: rho + (1-rho)(b + pi lambda) = {d6(mpf(rho) + (1 - mpf(rho)) * (b + mpf(pi) * lam))}")
print(f"  Ownership formula at r1: pi [rho + (1-rho)(b + lambda)] = {d6(mpf(pi) * (mpf(rho) + (1 - mpf(rho)) * (b + lam)))}")
print(f"  Entry ratio r1/r0 = {d6(EQ['r1']['entry'] / EQ['r0']['entry'])}")

# ---------------------------------------------------------------------------
# 5. Controls.
# ---------------------------------------------------------------------------
print("\n" + "=" * 78)
print("5. Controls of Table 3")
print("=" * 78)
FZ0 = outcome("r0", BUY, SELL)
HD0 = outcome("r0", NONE, NONE, see_price=False)
HD1 = outcome("r1", BUY, SELL, see_price=False)
print(f"  Frozen full orders at r0: entry {d6(FZ0['entry'])} (registry {reg('p4_frozen_r0_entry')}),"
      f" O_H {d6(FZ0['own'])} (registry {reg('p4_frozen_r0_own')}),"
      f" proceeds {d6(FZ0['proceeds'])} (registry {reg('p4_frozen_r0_proceeds')})")
print(f"  Frozen full orders at r1: entry {d6(EQ['r1']['entry'])}; at r2 (above r_C): entry {d6(EQ['r2']['entry'])}")
print(f"  Hidden price at r0: entry {d6(HD0['entry'])}, O_H {d6(HD0['own'])}, proceeds {d6(HD0['proceeds'])}")
print(f"  Hidden price at r1: entry {d6(HD1['entry'])}, O_H {d6(HD1['own'])}, proceeds {d6(HD1['proceeds'])}"
      f" (registry {reg('p4_hidden_r1_proceeds')})")
print(f"  Exact decrease r1 -> r2 with frozen orders = Pr(purchase)(1-rho) = {d6(EQ['r1']['entry'] - EQ['r2']['entry'])}"
      f"   registry p4_control_crossing_r1_r2 {reg('p4_control_crossing_r1_r2')}")

# ---------------------------------------------------------------------------
# 6. The band of u at the prior 1/2.
# ---------------------------------------------------------------------------
print("\n" + "=" * 78)
print("6. Admissible band: tau(r1) < M(1/2) < tau(r2), with M(1/2) = (1+u)/(2+u)")
print("=" * 78)
for n in ["r1", "r2"]:
    t = PAY[n]["tau"]
    # (1+u)/(2+u) = t  <=>  u = (2t - 1)/(1 - t)
    ub = (2 * t - 1) / (1 - t)
    print(f"  tau({n}) = {t}: u = (2 tau - 1)/(1 - tau) = {ub} = {d6(ub)}")
print(f"  registry u_lo_frac {reg('u_lo_frac')}, u_hi_frac {reg('u_hi_frac')}; benchmark u = {d6(u)}")

# ---------------------------------------------------------------------------
# 7. Coexistence strengths (cross-check; chapter 08 derives them).
# ---------------------------------------------------------------------------
print("\n" + "=" * 78)
print("7. Coexistence strengths at the benchmark slot (cross-check)")
print("=" * 78)


def Dr(r):
    return (r - 1) ** 2 / (2 * r)


def taur(r):
    return (48 * r - 3) / (4 * (20 * r - r**2 - 1))


kk, rr = mpf(k), mpf(rho)
rN = mp.findroot(lambda r: rr * Dr(r) / 2 - kk, 1.7)
rA = mp.findroot(lambda r: Dr(r) * (1 - taur(r)) - kk, 1.4)
rF = mp.findroot(lambda r: Dr(r) * (1 - M) - kk, 1.45)
rC = mp.findroot(lambda r: taur(r) - M, 3.5)
print(f"  r_N (rho Delta/2 = k):        {d6(rN)}   registry rN {reg('rN')}")
print(f"  r_A (Delta (1 - tau) = k):     {d6(rA)}   registry rA {reg('rA')}")
print(f"  r_F (Delta (1 - M) = k):       {d6(rF)}   registry rF_B {reg('rF_B')}")
print(f"  r_C (tau = M):                 {d6(rC)}   registry rC_B {reg('rC_B')}")
eA = rr + (1 - rr) * min(b * Dr(rA) / (2 * kk), b + lam / 2)
print(f"  entry on the branch at r_A:    {d6(eA)}   registry entry_rA_B {reg('entry_rA_B')}")

# ---------------------------------------------------------------------------
# 8. Research (cross-check; chapter 09 derives it).
# ---------------------------------------------------------------------------
print("\n" + "=" * 78)
print("8. Research branch: 2 a lambda = Delta(r) m_lambda - k, a = 1/40 (cross-check)")
print("=" * 78)
a = mp.mpf(1) / 40


def m_lam(lmb):
    ul = lmb / ((1 - lmb) * beta)
    return 1 / (2 + ul)


for rs, key in [("1.55", "r155"), ("1.60", "r160"), ("1.65", "r165")]:
    r = mp.mpf(rs)
    lr = mp.findroot(lambda x: 2 * a * x - (Dr(r) * m_lam(x) - kk), 0.25)
    ent = rr + (1 - rr) * (beta + (mp.mpf(1) / 2 - beta) * lr)
    print(f"  r = {rs}: lambda_R = {d6(lr)} (registry {reg('res_lambda_' + key)}),"
          f" entry = {d6(ent)} (registry {reg('res_entry_' + key)})")
