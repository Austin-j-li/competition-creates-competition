"""Recompute the numbers of chapter 03 (the auction stage) from the primitives.

Run: python3 verify/03_auction.py
The script prints. It does not assert anything.

Parts:
  1. The six payoff terms of paper (6) at r0, r1, r2: closed form, and an
     independent exact integration of the piecewise-linear payment in R.
  2. The preparation threshold tau(r), two routes.
  3. The derivatives of paper (7), exact, and a central difference.
  4. The identities t+g = value, the surplus split, the entry gains w_L, w_H.
  5. The size of the change from r0 to r1.
  6. Proposition 1 for a non-uniform F and non-degenerate classes:
     paper (8) against a direct double expectation (mpmath quadrature).
  7. Proposition 1(c): the kernel xi(R) and the exclusion reserve 101/100.
"""

from fractions import Fraction as Fr
from pathlib import Path
import re

import mpmath as mp

mp.mp.dps = 30

SNAPSHOT = Path(__file__).resolve().parents[2] / "manuscript" / "numbers.tex"


def registry():
    """Read the manuscript registry, key -> printed string."""
    if not SNAPSHOT.exists():
        return {}
    text = SNAPSHOT.read_text()
    pat = re.compile(r"\\csname reg@([A-Za-z0-9_]+)\\endcsname\{([^}]*)\}")
    return dict(pat.findall(text))


REG = registry()


def reg(key):
    return REG.get(key, "(not in registry)")


def d6(x):
    return f"{float(x):.6f}"


# Primitives of the benchmark (paper Section 4.2).
h, ell, p, cH = Fr(10), Fr(1), Fr(1, 2), Fr(6)
STRENGTHS = {"r0": Fr(6, 5), "r1": Fr(3), "r2": Fr(18, 5)}


# ---------------------------------------------------------------------------
# 1. The six payoff terms.
# ---------------------------------------------------------------------------
def closed_form(r):
    t0 = p * (1 - p / r)
    tH = r / 2 + p**2 / (2 * r)
    tL = ell - (ell**2 - p**2) / (2 * r)
    gH = h - r / 2 - p**2 / (2 * r)
    gL = (ell**2 - p**2) / (2 * r)
    D = (r - ell) ** 2 / (2 * r)
    return dict(t0=t0, tH=tH, tL=tL, gH=gH, gL=gL, Delta=D)


def integrate_piecewise_linear(f, breaks):
    """Exact integral of a function that is linear between the breakpoints.

    On a linear piece [a, b] the integral is (b - a) times the value at the
    midpoint, and that value is the mean of the values at the two interior
    points a + (b-a)/3 and a + 2(b-a)/3. Interior points avoid any jump at a
    breakpoint.
    """
    total = Fr(0)
    for a, b in zip(breaks[:-1], breaks[1:]):
        if b <= a:
            continue
        x1, x2 = a + (b - a) / 3, a + 2 * (b - a) / 3
        total += (b - a) * (f(x1) + f(x2)) / 2
    return total


def by_integration(r):
    """Integrate the realized payments over R ~ U[0, r] (density 1/r)."""
    br = [Fr(0), p, ell, r]
    no_entry = lambda R: p if R >= p else Fr(0)
    pay_H = lambda R: max(p, R)  # target receives with a high-value entrant
    pay_L = lambda R: max(p, min(R, ell))  # target receives with a low-value entrant
    keep_H = lambda R: h - max(p, R)  # high-value entrant always wins
    keep_L = lambda R: max(ell - max(p, R), Fr(0))
    out = {}
    out["t0"] = integrate_piecewise_linear(no_entry, br) / r
    out["tH"] = integrate_piecewise_linear(pay_H, br) / r
    out["tL"] = integrate_piecewise_linear(pay_L, br) / r
    out["gH"] = integrate_piecewise_linear(keep_H, br) / r
    out["gL"] = integrate_piecewise_linear(keep_L, br) / r
    gap = lambda R: max(R - ell, Fr(0))  # (R - ell)_+
    out["Delta"] = integrate_piecewise_linear(gap, br) / r
    return out


REGKEY = {
    "t0": "p2_base_{}_t0", "tH": "p2_base_{}_th", "tL": "p2_base_{}_tl",
    "gH": "p2_base_{}_gh", "gL": "p2_base_{}_gl",
}
DELTA_KEY = {"r0": "Delta_r0", "r1": "Delta_r1", "r2": "Delta_r2"}
B_KEY = {"r0": "Bprior_r0", "r1": "Bprior_r1_B", "r2": "Bprior_r2"}
TAU_KEY = {"r0": "tau_r0", "r1": "tau_r1", "r2": "tau_r2"}

print("=" * 78)
print("1. Payoff terms of paper (6): closed form | piecewise integration | registry")
print("=" * 78)
CF = {}
for name, r in STRENGTHS.items():
    cf, it = closed_form(r), by_integration(r)
    CF[name] = cf
    print(f"\n{name} = {r} ({float(r)})")
    for key in ["t0", "tH", "tL", "gH", "gL", "Delta"]:
        rk = DELTA_KEY[name] if key == "Delta" else REGKEY[key].format(name)
        print(f"  {key:6s} exact {str(cf[key]):>10s} = {d6(cf[key])}"
              f" | integral {d6(it[key])} | registry {reg(rk)}")
    B = cf["gL"] + Fr(1, 2) * (cf["gH"] - cf["gL"])
    print(f"  B(1/2) exact {B} = {d6(B)} | registry {reg(B_KEY[name])}")

# ---------------------------------------------------------------------------
# 2. Preparation threshold.
# ---------------------------------------------------------------------------
print("\n" + "=" * 78)
print("2. tau(r) = (cH - gL)/(gH - gL) and the closed form (48r-3)/(4(20r-r^2-1))")
print("=" * 78)
for name, r in STRENGTHS.items():
    cf = CF[name]
    tau1 = (cH - cf["gL"]) / (cf["gH"] - cf["gL"])
    tau2 = (48 * r - 3) / (4 * (20 * r - r**2 - 1))
    print(f"  {name}: tau = {tau1} = {d6(tau1)}; closed form {tau2}; registry {reg(TAU_KEY[name])}")
r_ell = ell
print(f"  at r = ell = 1: tau = {(48 * r_ell - 3) / (4 * (20 * r_ell - r_ell**2 - 1))} (above the prior 1/2)")

# ---------------------------------------------------------------------------
# 3. Derivatives.
# ---------------------------------------------------------------------------
print("\n" + "=" * 78)
print("3. Derivatives of paper (7): exact | central difference (step 1e-6)")
print("=" * 78)


def derivs(r):
    dD = Fr(1, 2) - ell**2 / (2 * r**2)
    dgH = -Fr(1, 2) + p**2 / (2 * r**2)
    dgL = -(ell**2 - p**2) / (2 * r**2)
    return dD, dgH, dgL


for name, r in STRENGTHS.items():
    dD, dgH, dgL = derivs(r)
    hstep = Fr(1, 10**6)
    num = {}
    for key in ["Delta", "gH", "gL"]:
        num[key] = (closed_form(r + hstep)[key] - closed_form(r - hstep)[key]) / (2 * hstep)
    dB = (dgL + dgH) / 2
    print(f"  {name}: Delta' = {dD} = {d6(dD)} (num {d6(num['Delta'])});"
          f" gH' = {dgH} = {d6(dgH)} (num {d6(num['gH'])});"
          f" gL' = {dgL} = {d6(dgL)} (num {d6(num['gL'])});"
          f" dB(1/2)/dr = {d6(dB)}")
    # quotient-rule form of Delta'
    q = (2 * (r - ell) * 2 * r - 2 * (r - ell) ** 2) / (4 * r**2)
    print(f"       quotient rule (2(r-l)2r - 2(r-l)^2)/(4r^2) = {q}; (r-l)(r+l)/(2r^2) = {(r-ell)*(r+ell)/(2*r**2)}")

# ---------------------------------------------------------------------------
# 4. Identities.
# ---------------------------------------------------------------------------
print("\n" + "=" * 78)
print("4. Identities: tH+gH = h, tL+gL = ell, Delta+gH-gL = h-ell, w_L, w_H, gH-gL")
print("=" * 78)
for name, r in STRENGTHS.items():
    cf = CF[name]
    wL, wH = cf["tL"] - cf["t0"], cf["tH"] - cf["t0"]
    print(f"  {name}: tH+gH = {cf['tH']+cf['gH']}, tL+gL = {cf['tL']+cf['gL']},"
          f" Delta+gH-gL = {cf['Delta']+cf['gH']-cf['gL']},"
          f" w_L = {wL} = {d6(wL)}, w_H = {wH} = {d6(wH)},"
          f" gH-gL = {cf['gH']-cf['gL']} = {d6(cf['gH']-cf['gL'])}")
    # closed forms of w_L and w_H
    wL_cf = (ell - p) - (ell**2 - 3 * p**2) / (2 * r)
    wH_cf = r / 2 - p + 3 * p**2 / (2 * r)
    print(f"       w_L closed form (l-p)-(l^2-3p^2)/(2r) = {wL_cf}; w_H closed form r/2-p+3p^2/(2r) = {wH_cf}")

# ---------------------------------------------------------------------------
# 5. Size of the change.
# ---------------------------------------------------------------------------
print("\n" + "=" * 78)
print("5. Size of the change from r0 to r1")
print("=" * 78)
B0 = (CF["r0"]["gH"] + CF["r0"]["gL"]) / 2
B1 = (CF["r1"]["gH"] + CF["r1"]["gL"]) / 2
B2 = (CF["r2"]["gH"] + CF["r2"]["gL"]) / 2
print(f"  Delta(r1)/Delta(r0) = {CF['r1']['Delta'] / CF['r0']['Delta']}")
print(f"  Delta(r2)/Delta(r0) = {CF['r2']['Delta'] / CF['r0']['Delta']} = {d6(CF['r2']['Delta'] / CF['r0']['Delta'])}")
print(f"  B(1/2): r0 {B0}, r1 {B1}, r2 {B2}")
print(f"  B(1/2) falls by {B0 - B1} = {d6(B0 - B1)} from r0 to r1,"
      f" relative fall {d6((B0 - B1) / B0)} = {100 * float((B0 - B1) / B0):.2f}%")
print(f"  B(1/2) falls by {B1 - B2} = {d6(B1 - B2)} from r1 to r2,"
      f" relative fall {100 * float((B1 - B2) / B1):.2f}%")
print(f"  Probability that the incumbent beats a low-value challenger, (r-l)/r:"
      + "".join(f" {n} {(r - ell) / r} = {d6((r - ell) / r)};" for n, r in STRENGTHS.items()))

# ---------------------------------------------------------------------------
# 6. Proposition 1 for a non-uniform F and non-degenerate classes.
# ---------------------------------------------------------------------------
print("\n" + "=" * 78)
print("6. Paper (8) against a direct double expectation (mpmath quadrature)")
print("=" * 78)
pm = mp.mpf(1) / 2


def F_pow(rbar):
    """F(y) = (y/rbar)^2 on [0, rbar]: a continuous incumbent law."""
    rbar = mp.mpf(rbar)
    return lambda y: mp.mpf(0) if y <= 0 else (min(y / rbar, 1)) ** 2


# Class H: theta uniform on [2, 10]. Class L: atom 1/2 at 1, and uniform on [1, 4] with weight 1/2.
def G_H(y):
    if y < 2:
        return mp.mpf(0)
    if y < 10:
        return (y - 2) / 8
    return mp.mpf(1)


def G_L(y):
    if y < 1:
        return mp.mpf(0)
    if y < 4:
        return mp.mpf(1) / 2 + (y - 1) / 6
    return mp.mpf(1)


def class_expect(j, fn, kinks=()):
    """E_j[fn(theta)] for the two example classes (with the atom of class L).

    The kinks are points where fn has a kink in theta (here the top of the
    incumbent support); they split the quadrature interval.
    """
    if j == "H":
        pts = sorted(set([mp.mpf(2), mp.mpf(10)] + [mp.mpf(x) for x in kinks if 2 < x < 10]))
        return mp.quad(lambda th: fn(th) / 8, pts)
    pts = sorted(set([mp.mpf(1), mp.mpf(4)] + [mp.mpf(x) for x in kinks if 1 < x < 4]))
    return fn(mp.mpf(1)) / 2 + mp.quad(lambda th: fn(th) / 6, pts)


def direct(F, rbar):
    """Direct expectation of the realized payments over R ~ F and theta ~ G_j."""
    rbar = mp.mpf(rbar)
    dens = lambda y: 2 * y / rbar**2  # density of F_pow on [0, rbar]

    def t_of_theta(th):
        # target receives max{p, min(R, theta)} for theta >= p (all values here are >= 1 > p)
        pts = sorted(set([mp.mpf(0), pm, min(th, rbar), rbar]))
        return mp.quad(lambda R: max(pm, min(R, th)) * dens(R), pts)

    def g_of_theta(th):
        pts = sorted(set([mp.mpf(0), pm, min(th, rbar), rbar]))
        return mp.quad(lambda R: max(th - max(pm, R), 0) * dens(R), pts)

    t0 = mp.quad(lambda R: (pm if R >= pm else 0) * dens(R), [0, pm, rbar])
    out = {"t0": t0}
    for j in ["H", "L"]:
        out["t" + j] = class_expect(j, t_of_theta, kinks=(rbar,))
        out["g" + j] = class_expect(j, g_of_theta, kinks=(rbar,))
    return out


def formula8(F):
    """Paper (8) and the t_j formula of Appendix A.1, by quadrature."""
    D = lambda y: G_L(y) - G_H(y)
    t0 = pm * (1 - F(pm))
    out = {"t0": t0}
    # Under the class ranking G_j(p^-) = 0, so the reserve terms vanish.
    for j, G in [("H", G_H), ("L", G_L)]:
        out["t" + j] = t0 + pm * F(pm) * (1 - 0) + mp.quad(lambda y: (1 - G(y)) * (1 - F(y)), [pm, 1, 2, 3, 4, 10])
        out["g" + j] = mp.quad(lambda y: (1 - G(y)) * F(y), [pm, 1, 2, 3, 4, 10])
    out["Delta"] = pm * F(pm) * 0 + mp.quad(lambda y: (1 - F(y)) * D(y), [pm, 1, 2, 3, 4, 10])
    return out


EmaxH = class_expect("H", lambda th: max(th, pm))
EmaxL = class_expect("L", lambda th: max(th, pm))
for rbar in [2, 3]:
    F = F_pow(rbar)
    a, b = direct(F, rbar), formula8(F)
    print(f"\n  F(y) = (y/{rbar})^2 on [0,{rbar}]; G_H = U[2,10]; G_L = (1/2) atom at 1 + (1/2) U[1,4]")
    for key in ["t0", "tH", "tL", "gH", "gL"]:
        print(f"    {key}: direct {mp.nstr(a[key], 12)} | formula {mp.nstr(b[key], 12)}")
    print(f"    Delta: direct tH-tL {mp.nstr(a['tH'] - a['tL'], 12)} | formula (8) {mp.nstr(b['Delta'], 12)}")
    print(f"    split: Delta+gH-gL = {mp.nstr(b['Delta'] + b['gH'] - b['gL'], 12)};"
          f" E_H max(theta,p) - E_L max(theta,p) = {mp.nstr(EmaxH - EmaxL, 12)}")
    print(f"    t_j >= t0: tH-t0 = {mp.nstr(a['tH'] - a['t0'], 8)}, tL-t0 = {mp.nstr(a['tL'] - a['t0'], 8)}")
FA, FB = formula8(F_pow(2)), formula8(F_pow(3))
print("\n  Strengthening F=(y/2)^2 -> F~=(y/3)^2 (F~ <= F pointwise):")
print(f"    Delta {mp.nstr(FA['Delta'], 10)} -> {mp.nstr(FB['Delta'], 10)}"
      f"; gH {mp.nstr(FA['gH'], 10)} -> {mp.nstr(FB['gH'], 10)}"
      f"; gL {mp.nstr(FA['gL'], 10)} -> {mp.nstr(FB['gL'], 10)}")

# ---------------------------------------------------------------------------
# 7. Proposition 1(c): the kernel and the exclusion reserve.
# ---------------------------------------------------------------------------
print("\n" + "=" * 78)
print("7. Proposition 1(c): kernel xi(R) and the exclusion reserve p = 101/100")
print("=" * 78)
pe = Fr(101, 100)
print(f"  registry rsv_points_excl = {reg('rsv_points_excl')}")
print("  Point masses h = 10, ell = 1 < p: the low class never meets the reserve, D(p^-) = 1.")
print("  xi(R) = p for R < p (only class H buys, at p); xi(R) = R - p for p <= R < h.")
print(f"  jump of xi at p: from {pe} down to 0")


def spread_excl(r):
    # E xi(R) for R ~ U[0, r], p < r < h
    return (pe**2 + (r - pe) ** 2 / 2) / r


def spread_excl_via8(r):
    # p F(p) D(p^-) + int_p^r [1 - F(y)] D(y) dy with D = 1 on (p, h), F(y) = y/r
    return pe * (pe / r) * 1 + ((r - pe) - (r**2 - pe**2) / (2 * r))


for r in [Fr(6, 5), Fr(3, 2), Fr(7, 4), Fr(2), Fr(3)]:
    s1, s2 = spread_excl(r), spread_excl_via8(r)
    print(f"  r = {str(r):>4s}: Delta_T = {s1} = {d6(s1)} (via (8): {s2})")
r_turn = mp.sqrt(3) * mp.mpf(101) / 100
print(f"  dDelta/dr = (r^2 - 3p^2)/(2r^2): negative below r = sqrt(3) p = {mp.nstr(r_turn, 8)}")
print("  For comparison, the class ranking at p = 1/2 gives xi(R) = (R - 1)_+, nondecreasing.")
