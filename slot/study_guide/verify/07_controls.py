"""Chapter 07 (controls): recompute every number of the chapter from the primitives.

Exact fractions for rational quantities; mpmath at 50 digits for quantities that
depend on Euler's number (the benchmark slot has 1 + u = e). The script prints;
it checks nothing by assertion.
"""
from fractions import Fraction as Fr
import mpmath as mp

mp.mp.dps = 50

# Benchmark primitives.
h, ell, p = Fr(10), Fr(1), Fr(1, 2)
rho, cH, k, pi = Fr(1, 4), Fr(6), Fr(1, 50), Fr(1, 2)
r0, r1, r2 = Fr(6, 5), Fr(3), Fr(18, 5)
beta = mp.mpf("0.294655")
u = mp.e - 1
lam = u * beta / (1 + u * beta)
b = (1 - lam) * beta
M = (1 + u) / (2 + u)          # top posterior at the prior 1/2
m = 1 - M                      # bottom posterior at the prior 1/2


def payoffs(r):
    """Equation (6) of the paper: t0, tH, tL, gH, gL, Delta for R ~ U[0, r]."""
    t0 = p * (1 - p / r)
    tH = r / 2 + p * p / (2 * r)
    tL = ell - (ell * ell - p * p) / (2 * r)
    gH = h - r / 2 - p * p / (2 * r)
    gL = (ell * ell - p * p) / (2 * r)
    return t0, tH, tL, gH, gL, tH - tL


def B(r, mu):
    t0, tH, tL, gH, gL, D = payoffs(r)
    return gL + mu * (gH - gL)


def tau(r):
    t0, tH, tL, gH, gL, D = payoffs(r)
    return (cH - gL) / (gH - gL)


def to_mp(x):
    return mp.mpf(x.numerator) / x.denominator if isinstance(x, Fr) else x


def f(x, digits=6):
    return mp.nstr(mp.mpf(x.numerator) / x.denominator if isinstance(x, Fr) else x, digits)


print("=" * 72)
print("1. Fixed-information control: the two counterexamples")
print("=" * 72)


def mean_max_p_R_uniform(lo, hi, pp):
    """E[max(p, R)] for R ~ U[lo, hi], exact."""
    lo, hi, pp = Fr(lo), Fr(hi), Fr(pp)
    if pp <= lo:
        return (lo + hi) / 2
    if pp >= hi:
        return pp
    w = hi - lo
    return pp * (pp - lo) / w + (hi * hi - pp * pp) / (2 * w)


# Example A (audit math_ext_1): signal informative about R.
print("\nExample A: the signal tells the challenger about the incumbent.")
pA, rhoA, cA = Fr(1, 2), Fr(1, 4), Fr(6)
vals = [Fr(12), Fr(11)]                 # class values, equal priors
Etheta = sum(vals) / 2                  # signal independent of class: belief 1/2
low = mean_max_p_R_uniform(0, 1, pA)    # component U[0,1]
high0 = mean_max_p_R_uniform(8, 9, pA)  # component U[8,9]
high1 = mean_max_p_R_uniform(9, 10, pA) # component U[9,10]
print(f"  E[theta | S] = {Etheta}  (both values exceed every incumbent value)")
print(f"  E[max(p,R)]: U[0,1] -> {low}, U[8,9] -> {high0}, U[9,10] -> {high1}")
g0_low, g0_high = Etheta - low, Etheta - high0
print(f"  Economy 0 (S reports the component): gross profit {g0_low} = {float(g0_low)} "
      f"after S=low, {g0_high} = {float(g0_high)} after S=high")
pay1 = (low + high1) / 2
g1 = Etheta - pay1
print(f"  Economy 1 (S independent of R): E[max(p,R)] = {pay1}; gross profit {g1} = {float(g1)} after either signal")
E0 = rhoA + (1 - rhoA) * (Fr(1, 2) * (g0_low >= cA) + Fr(1, 2) * (g0_high >= cA))
E1 = rhoA + (1 - rhoA) * (1 if g1 >= cA else 0)
print(f"  Entry: economy 0 = {E0}, economy 1 = {E1}")
print(f"  Unconditional gross profit: economy 0 = {(g0_low + g0_high) / 2}, economy 1 = {g1}")
# F1 <= F0 (first-order stochastic dominance): compare CDFs on a grid of rationals.
def cdf_mix(x, a, bb):
    x = Fr(x)
    c1 = min(max(x, Fr(0)), Fr(1))                       # U[0,1] part
    c2 = min(max(x - a, Fr(0)), bb - a) / (bb - a)   # U[a,bb] part
    return (c1 + c2) / 2
worst = min(cdf_mix(Fr(i, 20), 8, 9) - cdf_mix(Fr(i, 20), 9, 10) for i in range(0, 221))
print(f"  min over x of F0(x) - F1(x) on a grid of step 1/20 in [0,11]: {worst} (grid display; the upward shift of the upper component proves F1 <= F0)")

# Example B (final audit F_core): signal informative about theta within a class.
print("\nExample B: the signal tells the challenger about its value within a class.")
pB, rhoB, cB = Fr(1, 2), Fr(1, 4), Fr(21, 10)
GL, GH = [Fr(1), Fr(3)], [Fr(2), Fr(4)]
pay0 = mean_max_p_R_uniform(0, Fr(1, 2), pB)
pay1 = mean_max_p_R_uniform(0, Fr(3, 5), pB)
print(f"  E[max(p,R)]: R~U[0,1/2] -> {pay0}, R~U[0,3/5] -> {pay1}")
Eth0 = (sum(GL) / 2 + sum(GH) / 2) / 2
g0 = Eth0 - pay0
print(f"  Economy 0 (theta independent of S): E[theta|S] = {Eth0}, gross profit {g0} after either signal")
Eth_lo = (GL[0] + GH[0]) / 2
Eth_hi = (GL[1] + GH[1]) / 2
g1_lo, g1_hi = Eth_lo - pay1, Eth_hi - pay1
print(f"  Economy 1 (S selects the lower or upper value): E[theta|S] = {Eth_lo}, {Eth_hi}; "
      f"gross profit {g1_lo} = {float(g1_lo):.6f}, {g1_hi} = {float(g1_hi):.6f}")
E0 = rhoB + (1 - rhoB) * (1 if g0 >= cB else 0)
E1 = rhoB + (1 - rhoB) * (Fr(1, 2) * (g1_lo >= cB) + Fr(1, 2) * (g1_hi >= cB))
print(f"  Entry: economy 0 = {E0}, economy 1 = {E1}")
print(f"  Class gross profits g_L, g_H: economy 0 = {sum(GL)/2 - pay0}, {sum(GH)/2 - pay0}; "
      f"economy 1 = {sum(GL)/2 - pay1}, {sum(GH)/2 - pay1} (both fall)")

print("\nCommon tie probability q: difference of the two preparation rules, case by case.")
print("  C < B1: 0;  C = B1 < B0: 1 - q;  B1 < C < B0: 1;  C = B0 > B1: q;  C > B0: 0;  B0 = B1: 0")

print("=" * 72)
print("2. Benchmark slot and the preparation threshold")
print("=" * 72)
print(f"  lambda = {mp.nstr(lam, 12)}, b = {mp.nstr(b, 12)}, b + lambda = {mp.nstr(b + lam, 12)}, "
      f"b + lambda/2 = {mp.nstr(b + lam / 2, 12)}")
print(f"  M(1/2) = {mp.nstr(M, 12)}, m(1/2) = {mp.nstr(m, 12)}")
for r in (Fr(1), r0, r1, r2):
    print(f"  tau({r}) = {tau(r)} = {f(tau(r), 8)};  closed form (48r-3)/(4(20r-r^2-1)) = "
          f"{(48 * r - 3) / (4 * (20 * r - r * r - 1))}")
print("  d tau/dr has the sign of 12 r^2 - (3/2) r + 3; discriminant =", Fr(9, 4) - 4 * 12 * 3)
Mh_c = M * h - cH
rC = (Mh_c + mp.sqrt(Mh_c ** 2 + M * ((1 - M) * ell ** 2 - p ** 2))) / M
gHc = to_mp(h) - rC / 2 - to_mp(p * p) / (2 * rC)
gLc = to_mp(ell * ell - p * p) / (2 * rC)
print(f"  entry ceiling r_C = {mp.nstr(rC, 12)};  B_rC(M) - c_H = {mp.nstr(gLc + M * (gHc - gLc) - to_mp(cH), 5)}")

print("=" * 72)
print("3. Table 3 decoded: prices, entry, ownership, proceeds")
print("=" * 72)


def report(r, profile, see_price, label):
    """profile: 'zero' or 'full'. see_price: challenger sees the price (True) or not."""
    t0, tH, tL, gH, gL, D = map(to_mp, payoffs(r))
    wH, wL = tH - t0, tL - t0
    b0 = (1 - lam) * (1 - 2 * beta)
    if profile == "zero":
        fH = {-1: b, 0: b0 + lam, 1: b}
        fL = {-1: b, 0: b0 + lam, 1: b}
    else:
        fH = {-1: b, 0: b0, 1: b + lam}
        fL = {-1: b + lam, 0: b0, 1: b}
    post = {x: fH[x] / (fH[x] + fL[x]) for x in (-1, 0, 1)}
    if see_price:
        ent = {x: (1 if B(r, post[x]) >= cH else rho) for x in (-1, 0, 1)}
    else:
        ent = {x: (1 if B(r, mp.mpf(1) / 2) >= cH else rho) for x in (-1, 0, 1)}
    ent = {x: to_mp(Fr(e)) if isinstance(e, (int, Fr)) else e for x, e in ent.items()}
    price = {x: t0 + ent[x] * (wL + D * post[x]) for x in (-1, 0, 1)}
    eH = sum(fH[x] * ent[x] for x in (-1, 0, 1))
    eL = sum(fL[x] * ent[x] for x in (-1, 0, 1))
    E = (eH + eL) / 2
    OH = eH / 2                          # W_H = 1 in the benchmark (h > r)
    RT = t0 + (eH * wH + eL * wL) / 2
    Eprice = sum((fH[x] + fL[x]) / 2 * price[x] for x in (-1, 0, 1))
    KH = ent[1] * D * (1 - post[1])
    KL = ent[-1] * D * post[-1]
    print(f"\n  {label} (r = {r})")
    print(f"    posteriors (sale, zero, purchase) = {mp.nstr(post[-1], 7)}, {mp.nstr(post[0], 7)}, {mp.nstr(post[1], 7)}")
    print(f"    entry after (sale, zero, purchase) = {mp.nstr(ent[-1], 7)}, {mp.nstr(ent[0], 7)}, {mp.nstr(ent[1], 7)}")
    print(f"    prices (sale, zero, purchase) = {mp.nstr(price[-1], 7)}, {mp.nstr(price[0], 7)}, {mp.nstr(price[1], 7)}")
    print(f"    entry by class e_H = {mp.nstr(eH, 8)}, e_L = {mp.nstr(eL, 8)}; total entry = {mp.nstr(E, 8)}")
    print(f"    high-class ownership = {mp.nstr(OH, 8)}; proceeds = {mp.nstr(RT, 8)}; E[P(X)] = {mp.nstr(Eprice, 8)}")
    print(f"    gross returns K_H = {mp.nstr(KH, 8)}, K_L = {mp.nstr(KL, 8)}; net K_H - k = {mp.nstr(KH - to_mp(k), 8)}, "
          f"K_L - k = {mp.nstr(KL - to_mp(k), 8)}")
    return E, OH, RT


print("\n Payoff inputs:")
for r in (r0, r1, r2):
    t0, tH, tL, gH, gL, D = payoffs(r)
    print(f"  r = {r}: t0 = {t0}, tH = {tH}, tL = {tL}, Delta = {D}, w_H = {tH - t0}, w_L = {tL - t0}, "
          f"B(1/2) = {B(r, Fr(1, 2))} = {f(B(r, Fr(1, 2)), 7)}, B(M) = {mp.nstr(B(r, M), 8)}, B(m) = {mp.nstr(B(r, m), 8)}")

print("\n Panel A: equilibrium")
report(r0, "zero", True, "weak incumbent, zero orders")
report(r1, "full", True, "strong incumbent, full orders")
report(r2, "full", True, "very strong incumbent, full orders")
print("\n Panel B: full orders held fixed")
EB0, _, _ = report(r0, "full", True, "frozen full orders at r0 (a control, not an equilibrium)")
EB1, _, _ = report(r1, "full", True, "frozen full orders at r1 (the equilibrium)")
EB2, _, _ = report(r2, "full", True, "frozen full orders at r2 (the equilibrium)")
print("\n Panel C: the challenger does not see the price")
report(r0, "zero", False, "hidden price at r0")
report(r1, "full", False, "hidden price at r1")

print("\n Crossing probabilities of Proposition A.3 under frozen full orders")
for (ra, rb) in ((r0, r1), (r1, r2)):
    prob = 0
    fH = {-1: b, 0: (1 - lam) * (1 - 2 * beta), 1: b + lam}
    fL = {-1: b + lam, 0: (1 - lam) * (1 - 2 * beta), 1: b}
    post = {x: fH[x] / (fH[x] + fL[x]) for x in (-1, 0, 1)}
    for x in (-1, 0, 1):
        px = (fH[x] + fL[x]) / 2
        for C, pc in ((0, rho), (cH, 1 - rho)):
            if B(rb, post[x]) < C <= B(ra, post[x]):
                prob += px * to_mp(Fr(pc))
    print(f"  from r = {ra} to r = {rb}: Pr(B_b(mu) < C <= B_a(mu)) = {mp.nstr(prob, 8)}")
print(f"  entry difference r1 -> r2 under frozen orders = {mp.nstr(EB1 - EB2, 8)}; (1-rho)(b+lambda/2) = "
      f"{mp.nstr((1 - rho) * (b + lam / 2), 8)}")
print(f"  frozen entry below r_C: rho + (1-rho)(b+lambda/2) = {mp.nstr(rho + (1 - rho) * (b + lam / 2), 10)}")

print("\n Hidden price at r1: the trading bound with e = rho")
D1 = to_mp(payoffs(r1)[5])
print(f"  rho*kappa*Delta_1 = {mp.nstr(rho * m * D1, 8)} > k = {float(k)}: margin {mp.nstr(rho * m * D1 - k, 8)}")
print(f"  hidden price after a purchase uses e = rho: K_H = rho*Delta*(1-M) = {mp.nstr(rho * D1 * (1 - M), 8)}")
