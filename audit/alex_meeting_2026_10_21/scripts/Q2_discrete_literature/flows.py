"""Print-only: flow posteriors in the discrete (EGJ-style) microstructure.

Noise z in {-1,0,1} with probabilities (1/3,1/3,1/3). The investor is present
with probability lam and plays q_theta; if absent the order is 0. The flow is
X = q + z. Print Pr(X|h), Pr(X|l), the posterior mu_X = Pr(h|X) (prior 1/2),
and a label. Then print the benchmark challenger objects.
"""
from fractions import Fraction as F

Z = {-1: F(1, 3), 0: F(1, 3), 1: F(1, 3)}
PROFILES = {
    "NT  (0,0)":   (0, 0),
    "T   (+1,-1)": (1, -1),
    "BNS (+1,0)":  (1, 0),
    "SNB (0,-1)":  (0, -1),
}


def flow_law(q, lam):
    law = {}
    for z, pz in Z.items():
        law[z] = law.get(z, 0) + (1 - lam) * pz          # investor absent: q = 0
        law[q + z] = law.get(q + z, 0) + lam * pz        # investor present
    return law


def report(lam):
    print(f"\n=== presence probability lambda = {lam} ===")
    for name, (qh, ql) in PROFILES.items():
        lh, ll = flow_law(qh, lam), flow_law(ql, lam)
        print(f"-- {name}")
        for x in range(-2, 3):
            ph, pl = lh.get(x, F(0)), ll.get(x, F(0))
            if ph + pl == 0:
                print(f"   X={x:+d}: off path (probability 0 under this profile)")
                continue
            mu = ph / (ph + pl)
            tag = "reveals h" if mu == 1 else "reveals l" if mu == 0 else (
                "prior" if mu == F(1, 2) else "interior")
            print(f"   X={x:+d}: Pr|h={str(ph):>5} Pr|l={str(pl):>5}  mu={str(mu):>5}  {tag}")


for lam in (F(1), F(1, 2)):
    report(lam)

# Benchmark challenger objects (eq. 4 of the paper), uniform incumbent.
h, ell, p, rho, cL, cH, b = 10.0, 1.0, 0.5, 0.25, 1.0, 6.0, 2.0
import math
print("\n=== benchmark objects at r_0, r_1, r_2 ===")
m = 1 / (1 + math.exp(2 / b))
for r in (1.2, 3.0, 3.6):
    gH = h - r / 2 - p * p / (2 * r)
    gL = (ell * ell - p * p) / (2 * r)
    B = lambda mu: gL + mu * (gH - gL)
    tau = (cH - gL) / (gH - gL)
    print(f"r={r}: g_L={gL:.4f} g_H={gH:.4f} B(0)=g_L={gL:.4f} B(m)={B(m):.4f} "
          f"B(1/2)={B(0.5):.4f} B(1)={gH:.4f} tau={tau:.4f}  c_L={cL} <= B(0)? {cL <= gL}")


# ---------------------------------------------------------------------------
# Part 2. Can a price that pools several flows at t_0 fool the challenger?
# A pool S is priced at t_0 (nobody enters). It is self-fulfilling only if
#   (i) S holds every flow whose own posterior is below mu_L (the posterior at
#       which the low-cost type is just willing to prepare),
#   (ii) S holds at least one flow whose own posterior is at or above mu_L,
#   (iii) the pooled posterior is below mu_L.
# ---------------------------------------------------------------------------
from itertools import combinations


def pools(profile, lam, mu_L):
    qh, ql = PROFILES[profile]
    lh, ll = flow_law(qh, lam), flow_law(ql, lam)
    flows = [x for x in range(-2, 3) if lh.get(x, 0) + ll.get(x, 0) > 0]
    mu = {x: lh.get(x, F(0)) / (lh.get(x, F(0)) + ll.get(x, F(0))) for x in flows}
    must = {x for x in flows if mu[x] < mu_L}
    found = []
    for k in range(1, len(flows) + 1):
        for S in combinations(flows, k):
            if not must <= set(S):
                continue
            if all(mu[x] < mu_L for x in S):
                continue                      # this is the ordinary outcome
            ph = sum(lh.get(x, F(0)) for x in S)
            pl = sum(ll.get(x, F(0)) for x in S)
            if float(ph / (ph + pl)) < mu_L:
                found.append(S)
    return found


print("\n=== pooling-at-t_0 check (benchmark, c_L = 1) ===")
for r in (1.2, 3.0, 3.6):
    gH = h - r / 2 - p * p / (2 * r)
    gL = (ell * ell - p * p) / (2 * r)
    mu_L = (cL - gL) / (gH - gL)
    for lam in (F(1), F(1, 2)):
        for name in PROFILES:
            res = pools(name, lam, mu_L)
            print(f"r={r} mu_L={mu_L:.4f} lam={lam} {name}: self-fulfilling pools = {res}")

# ---------------------------------------------------------------------------
# Part 3. Floor of the posterior in the buy-only variant (H buys, L does not).
# Lowest reachable flow is X=-1, with mu = (1-lam)/(2-lam).
# Need c_L < B(floor), i.e. floor > mu_L.
# ---------------------------------------------------------------------------
print("\n=== buy-only floor (Prop. A.2 needs c_L < B(floor)) ===")
for r in (1.2, 3.0):
    gH = h - r / 2 - p * p / (2 * r)
    gL = (ell * ell - p * p) / (2 * r)
    mu_L = (cL - gL) / (gH - gL)
    lam_max = (1 - 2 * mu_L) / (1 - mu_L)
    print(f"r={r}: mu_L={mu_L:.4f}; floor (1-lam)/(2-lam) > mu_L iff lam < {lam_max:.4f}")
print("two-sided (T) profile: X=-2 reveals l for every lam, so the floor is 0.")

# ---------------------------------------------------------------------------
# Part 4. Thresholds and entry at lam = 1, benchmark k = 0.02, buy-only.
# Deviation profit of h (buy) = (2/3) * e(1/2) * Delta_T / 2 - k  (flows 0, 1 at mu=1/2;
# flow 2 reveals h).  Two-sided T needs (1/3) * e(1/2) * Delta_T/2 > k for both types.
# ---------------------------------------------------------------------------
print("\n=== lam = 1 thresholds (flow unit 1, noise {-1,0,1}) ===")
k = 0.02
for r in (1.2, 3.0, 3.6):
    DT = (r - ell) ** 2 / (2 * r)
    gH = h - r / 2 - p * p / (2 * r)
    gL = (ell * ell - p * p) / (2 * r)
    e_half = rho + (1 - rho) * (1 if gL + 0.5 * (gH - gL) >= cH else 0)
    k_NT = e_half * DT / 3
    k_T = e_half * DT / 6
    print(f"r={r}: Delta_T={DT:.5f} e(1/2)={e_half:.3f}  "
          f"T iff k<{k_T:.5f}; BNS/SNB iff {k_T:.5f}<=k<{k_NT:.5f}; NT iff k>={k_NT:.5f}; k={k}")

r = 3.0
gH = h - r / 2 - p * p / (2 * r)
gL = (ell * ell - p * p) / (2 * r)
e1 = rho + (1 - rho) * (1 if gH >= cH else 0)
eh = rho + (1 - rho) * (1 if gL + 0.5 * (gH - gL) >= cH else 0)
e0 = rho if cL <= gL else 0.0
entry = (1 / 6) * e1 + (2 / 3) * eh + (1 / 6) * e0
print(f"\nbuy-only, lam=1, r_1=3: entry = 1/6*{e1} + 2/3*{eh} + 1/6*{e0} = {entry:.4f} (no-trade entry = {rho})")
for r2 in (3.6, 8.5):
    gH2 = h - r2 / 2 - p * p / (2 * r2)
    print(f"r={r2}: g_H = B(1) = {gH2:.4f}; high-cost type enters after a revealed h? {gH2 >= cH}")

# Two-sided T at lam = 1, r_1 = 3: flows 2,1 reveal h (prob 1/3 overall),
# flow 0 has mu = 1/2 (prob 1/3), flows -1,-2 reveal l (prob 1/3).
entry_T = (1 / 3) * e1 + (1 / 3) * eh + (1 / 3) * e0
entry_T_cL0 = (1 / 3) * e1 + (1 / 3) * eh + (1 / 3) * rho
print(f"two-sided T, lam=1, r_1=3: entry = {entry_T:.4f} with c_L=1; "
      f"{entry_T_cL0:.4f} if c_L <= g_L (low-cost type also enters at mu=0); no-trade entry = {rho}")
