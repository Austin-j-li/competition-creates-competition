#!/usr/bin/env python
"""Independent exact check of memo C9.

Model: buy-only orders q in {0, 1}, three-point noise Z in {-1, 0, 1} with
probabilities (u, v, w) = (z_-, z_0, z_+), presence lam, prior pi, c_L = 0.
The investor may mix at zero profit. The high-cost challenger may mix at
B_r(mu) = c_H (tie rule "mix"), or must prepare ("enter"), or must not ("stay").

Every number is a fractions.Fraction. Decimal strings are for display only.
The script prints results. It makes no assertions.

Run from the repository root:
    .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/X_C9_check/check_c9.py
"""

from fractions import Fraction as F
from math import isqrt
import random

FLOWS = (-1, 0, 1, 2)

BENCH = {
    "h": F(10), "ell": F(1), "p": F(1, 2), "rho": F(1, 4),
    "cH": F(6), "cL": F(0), "k": F(1, 50), "lam": F(1), "pi": F(1, 2),
}
NOISE_C9 = {-1: F(2, 5), 0: F(2, 5), 1: F(1, 5)}  # (z_-, z_0, z_+)
R_POINTS = (F(63, 40), F(79, 50), F(317, 200))


def dec(q, n=6):
    """Exact rounding of a Fraction to n decimals, for display."""
    s = round(q * 10 ** n)
    sign = "-" if s < 0 else ""
    s = abs(s)
    return f"{sign}{s // 10 ** n}.{s % 10 ** n:0{n}d}"


# --------------------------------------------------------------- auction stage
def mean_uniform(fn, r, cuts):
    """Exact mean of fn(R) for R ~ U[0, r] when fn is affine between cuts.
    The midpoint rule is exact on every affine piece."""
    pts = [F(0)] + sorted(c for c in cuts if 0 < c < r) + [r]
    total = F(0)
    for a, b in zip(pts, pts[1:]):
        total += (b - a) * fn((a + b) / 2)
    return total / r


def auction(par, r):
    """Receipts and gross profits from the auction rules, not from closed forms."""
    h, ell, p = par["h"], par["ell"], par["p"]
    cuts = (p, ell)
    t0 = mean_uniform(lambda R: p if R >= p else F(0), r, cuts)
    tH = mean_uniform(lambda R: max(p, R), r, cuts)
    tL = mean_uniform(lambda R: max(p, min(R, ell)), r, cuts)
    gH = mean_uniform(lambda R: max(h - max(p, R), F(0)), r, cuts)
    gL = mean_uniform(lambda R: max(ell - max(p, R), F(0)), r, cuts)
    return {"t0": t0, "tH": tH, "tL": tL, "gH": gH, "gL": gL,
            "D": tH - tL, "aL": tL - t0, "tau": (par["cH"] - gL) / (gH - gL)}


def closed_forms(par, r):
    h, ell, p = par["h"], par["ell"], par["p"]
    return {"t0": p * (1 - p / r), "tH": r / 2 + p * p / (2 * r),
            "tL": ell - (ell * ell - p * p) / (2 * r),
            "gH": h - r / 2 - p * p / (2 * r),
            "gL": (ell * ell - p * p) / (2 * r), "D": (r - ell) ** 2 / (2 * r)}


# --------------------------------------------------------- beliefs and entry
def n_of(noise, z):
    return noise.get(z, F(0))


def beliefs(par, noise, alpha, off_mu):
    """Flow laws with q_L = 0 and Pr(q_H = 1) = alpha / lam; off_mu at unused flows."""
    pi = par["pi"]
    fH = {x: (1 - alpha) * n_of(noise, x) + alpha * n_of(noise, x - 1) for x in FLOWS}
    fL = {x: n_of(noise, x) for x in FLOWS}
    mu, on = {}, {}
    for x in FLOWS:
        den = pi * fH[x] + (1 - pi) * fL[x]
        on[x] = den > 0
        mu[x] = pi * fH[x] / den if den > 0 else off_mu
    return fH, fL, mu, on


def gain(A, mu):
    return A["gL"] + mu * (A["gH"] - A["gL"])


def entry_range(par, A, mu, tie):
    """(lowest, highest) optimal total entry rate at posterior mu.
    The low-cost type prepares at every belief because g_L > c_L = 0."""
    rho = par["rho"]
    d = gain(A, mu) - par["cH"]
    if d > 0:
        return F(1), F(1)
    if d < 0:
        return rho, rho
    return {"mix": (rho, F(1)), "enter": (F(1), F(1)), "stay": (rho, rho)}[tie]


def payoffs(par, A, noise, mu, e):
    """First principles: V_j(x) = t0 + e_x (t_j - t0), P_x = E[V_T | x].
    Returns gross purchase payoffs of both types (before the cost k) and prices."""
    VH = {x: A["t0"] + e[x] * (A["tH"] - A["t0"]) for x in FLOWS}
    VL = {x: A["t0"] + e[x] * (A["tL"] - A["t0"]) for x in FLOWS}
    price = {x: mu[x] * VH[x] + (1 - mu[x]) * VL[x] for x in FLOWS}
    gH = sum(n_of(noise, z) * (VH[1 + z] - price[1 + z]) for z in (-1, 0, 1))
    gL = sum(n_of(noise, z) * (VL[1 + z] - price[1 + z]) for z in (-1, 0, 1))
    return gH, gL, price


def gross_ext(par, A, noise, alpha, tie, off_mu, side):
    """Lowest (side 0) or highest (side 1) gross purchase payoff over optimal entry."""
    _, _, mu, _ = beliefs(par, noise, alpha, off_mu)
    e = {x: entry_range(par, A, mu[x], tie)[side] for x in FLOWS}
    return payoffs(par, A, noise, mu, e)[0]


# ------------------------------------------------------- exact root location
def is_square(q):
    if q < 0:
        return None
    rn, rd = isqrt(q.numerator), isqrt(q.denominator)
    return F(rn, rd) if rn * rn == q.numerator and rd * rd == q.denominator else None


def poly(c, x):
    return (c[0] * x + c[1]) * x + c[2]


def roots_open(c, lo, hi):
    """Roots of c[0] x^2 + c[1] x + c[2] in the open interval (lo, hi).
    Returns "identity" or a list of ("exact", q) and ("bracket", a, b) items.
    A bracket has a strict sign change and contains one irrational root."""
    c2, c1, c0 = c
    if c2 == 0 and c1 == 0:
        return "identity" if c0 == 0 else []
    if c2 == 0:
        q = -c0 / c1
        return [("exact", q)] if lo < q < hi else []
    disc = c1 * c1 - 4 * c2 * c0
    if disc < 0:
        return []
    s = is_square(disc)
    if s is not None:
        qs = sorted({(-c1 - s) / (2 * c2), (-c1 + s) / (2 * c2)})
        return [("exact", q) for q in qs if lo < q < hi]
    m = -c1 / (2 * c2)
    cuts = [lo] + ([m] if lo < m < hi else []) + [hi]
    out = []
    for a, b in zip(cuts, cuts[1:]):
        if poly(c, a) * poly(c, b) < 0:
            out.append(("bracket", a, b))
    return out


def indifference_poly(par, A, noise, e0, e1):
    """g(alpha) = k L0 L1 - a L1 - b L0 with K(alpha) = a/L0 + b/L1, where
    L_x = pi fH(x) + (1 - pi) fL(x) and fixed entry e0, e1 at flows 0 and 1.
    Since L0, L1 > 0, sign g = sign(k - K). Flow 2 has posterior one."""
    pi, k = par["pi"], par["k"]
    u, v, w = n_of(noise, -1), n_of(noise, 0), n_of(noise, 1)
    E00, E10 = v, pi * (u - v)
    E01, E11 = w, pi * (v - w)
    a = A["D"] * (1 - pi) * u * v * e0
    b = A["D"] * (1 - pi) * v * w * e1
    return (k * E10 * E11,
            k * (E00 * E11 + E10 * E01) - a * E11 - b * E10,
            k * E00 * E01 - a * E01 - b * E00)


def thresholds(par, A, noise):
    """alpha in (0, lam) where the flow-0 or flow-1 posterior equals tau,
    and flows whose posterior stays at tau for every alpha."""
    pi, lam, tau = par["pi"], par["lam"], A["tau"]
    u, v, w = n_of(noise, -1), n_of(noise, 0), n_of(noise, 1)
    pts, const = set(), []
    if not (0 < tau < 1):
        return [], []
    for x, (c0, c1, d) in {0: (v, u - v, v), 1: (w, v - w, w)}.items():
        lhs0 = pi * c0 * (1 - tau) - (1 - pi) * tau * d
        lhs1 = pi * c1 * (1 - tau)
        if lhs1 == 0:
            if lhs0 == 0:
                const.append(x)
            continue
        a = -lhs0 / lhs1
        if 0 < a < par["lam"]:
            pts.add(a)
    return sorted(pts), const


# ------------------------------------------------------------- enumeration
def profile(par, A, noise, alpha, e01, tie, off_mu):
    """Complete a candidate and check it from first principles."""
    pi, k = par["pi"], par["k"]
    fH, fL, mu, on = beliefs(par, noise, alpha, off_mu)
    e, notes = {}, []
    for x in FLOWS:
        lo, hi = entry_range(par, A, mu[x], tie)
        if x in e01:
            e[x] = e01[x]
            if not (lo <= e[x] <= hi):
                notes.append(f"entry at flow {x} not optimal")
        else:
            e[x] = lo
            if lo != hi and on[x]:
                notes.append(f"free entry at on-path flow {x}")
    gH, gL, price = payoffs(par, A, noise, mu, e)
    groups = {}
    for x in FLOWS:
        if on[x]:
            groups.setdefault(price[x], []).append(x)
    gap, entry_ok, one_entry = F(0), True, True
    for xs in groups.values():
        mH = sum(pi * fH[x] for x in xs)
        mL = sum((1 - pi) * fL[x] for x in xs)
        pooled = mH / (mH + mL)
        gap = max(gap, max(abs(pooled - mu[x]) for x in xs))
        one_entry = one_entry and len({e[x] for x in xs}) == 1
        lo, hi = entry_range(par, A, pooled, tie)
        entry_ok = entry_ok and all(lo <= e[x] <= hi for x in xs)
    pid = max(abs(price[x] - (A["t0"] + e[x] * (A["aL"] + A["D"] * mu[x]))) for x in FLOWS)
    # An off-path price may coincide with an on-path price only if the two
    # flows carry the same posterior and the same entry rate.
    clash = any((not on[x]) and price[x] in groups
                and any(mu[y] != mu[x] or e[y] != e[x] for y in groups[price[x]])
                for x in FLOWS)
    Wt = {x: pi * fH[x] + (1 - pi) * fL[x] for x in FLOWS}
    return {"alpha": alpha, "beta": alpha / par["lam"], "mu": mu, "e": e, "price": price,
            "UH1": gH - k, "UL1": gL - k, "gap": gap, "entry_ok": entry_ok,
            "one_entry": one_entry, "pid": pid, "clash": clash,
            "E": sum(Wt[x] * e[x] for x in FLOWS),
            "OH": sum(pi * fH[x] * e[x] for x in FLOWS),
            "margin1": gain(A, mu[1]) - par["cH"], "notes": notes, "groups": len(groups)}


def enumerate_eq(par, noise, r, tie="mix", off_mu=F(1), build=True):
    """Every equilibrium purchase probability of the high-quality investor.
    The low-quality investor never buys (strict dominance). off_mu is the common
    off-path belief at the unused flow 2 under no trade."""
    A = auction(par, r)
    lam, k, rho = par["lam"], par["k"], par["rho"]
    tpts, const = thresholds(par, A, noise)
    if const:
        return A, None, f"posterior constant at tau at flows {const}"
    out = []

    def add(kind, alpha, e01, extra=None):
        rec = {"kind": kind, "alpha": alpha, "extra": extra}
        if build:
            rec["prof"] = profile(par, A, noise, alpha, e01, tie, off_mu)
        out.append(rec)

    # no trade: some optimal entry makes a purchase weakly unprofitable
    if gross_ext(par, A, noise, F(0), tie, off_mu, 0) <= k:
        _, _, mu, _ = beliefs(par, noise, F(0), off_mu)
        add("no trade", F(0), {x: entry_range(par, A, mu[x], tie)[0] for x in (0, 1)})
    # full purchases: some optimal entry makes a purchase weakly profitable
    if gross_ext(par, A, noise, lam, tie, off_mu, 1) >= k:
        _, _, mu, _ = beliefs(par, noise, lam, off_mu)
        add("full purchase", lam, {x: entry_range(par, A, mu[x], tie)[1] for x in (0, 1)})
    # threshold points: k between the lowest and highest gross payoff
    for a in tpts:
        lo = gross_ext(par, A, noise, a, tie, off_mu, 0)
        hi = gross_ext(par, A, noise, a, tie, off_mu, 1)
        if lo <= k <= hi:
            _, _, mu, _ = beliefs(par, noise, a, off_mu)
            rng = {x: entry_range(par, A, mu[x], tie) for x in (0, 1)}
            at = [x for x in (0, 1) if rng[x][0] != rng[x][1]]
            if len(at) == 1 and hi > lo:
                x = at[0]
                ex = rng[x][0] + (k - lo) / (hi - lo) * (rng[x][1] - rng[x][0])
                e01 = {y: rng[y][0] for y in (0, 1)}
                e01[x] = ex
                add("threshold mixture", a, e01, {"flow": x, "sigma": (ex - rho) / (1 - rho)})
            elif len(at) == 0:
                add("threshold (pure entry)", a, {y: rng[y][0] for y in (0, 1)})
            else:
                out.append({"kind": "continuum at threshold", "alpha": a, "extra": rng})
    # open intervals between thresholds: entry is pure and constant
    cuts = [F(0)] + tpts + [lam]
    for a, b in zip(cuts, cuts[1:]):
        _, _, mu, _ = beliefs(par, noise, (a + b) / 2, off_mu)
        e0 = entry_range(par, A, mu[0], tie)[0]
        e1 = entry_range(par, A, mu[1], tie)[0]
        rs = roots_open(indifference_poly(par, A, noise, e0, e1), a, b)
        if rs == "identity":
            out.append({"kind": "continuum on interval", "alpha": (a, b), "extra": (e0, e1)})
            continue
        for item in rs:
            if item[0] == "exact":
                add("interior mixture", item[1], {0: e0, 1: e1}, {"entry01": (e0, e1)})
            else:
                out.append({"kind": "interior mixture (irrational root)",
                            "alpha": (item[1], item[2]), "extra": (e0, e1)})
    return A, out, None


def show(rec, indent="    "):
    print(f"{indent}kind: {rec['kind']}")
    if "prof" not in rec:
        print(f"{indent}  alpha: {rec['alpha']}  extra: {rec['extra']}")
        return
    P = rec["prof"]
    print(f"{indent}  beta = {P['beta']}  (~{dec(P['beta'])})")
    print(f"{indent}  posteriors (x=-1,0,1,2): " + ", ".join(str(P["mu"][x]) for x in FLOWS))
    print(f"{indent}  entry      (x=-1,0,1,2): " + ", ".join(str(P["e"][x]) for x in FLOWS))
    if rec["extra"] and "sigma" in rec["extra"]:
        print(f"{indent}  high-cost preparation probability at flow {rec['extra']['flow']}: "
              f"{rec['extra']['sigma']}  (~{dec(rec['extra']['sigma'])})")
    print(f"{indent}  U_H(1) = {P['UH1']}   U_L(1) = {P['UL1']}")
    print(f"{indent}  E = {P['E']}  (~{dec(P['E'])})   O_H = {P['OH']}  (~{dec(P['OH'])})")
    print(f"{indent}  flow-1 preparation margin B(mu_1) - c_H = {P['margin1']}")
    print(f"{indent}  price checks: max |pooled - flow posterior| = {P['gap']}, "
          f"one entry rate per price = {P['one_entry']}, challenger optimal = {P['entry_ok']}, "
          f"max |P - t0 - e(aL + D mu)| = {P['pid']}, off-path price clash = {P['clash']}, "
          f"price groups = {P['groups']}")
    if P["notes"]:
        print(f"{indent}  notes: {P['notes']}")


def kinds(res):
    return [rec["kind"] for rec in res]


# ===================================================================== main
def main():
    par = dict(BENCH)
    noise = NOISE_C9
    print("=" * 78)
    print("X_C9 independent check. Noise (z_-, z_0, z_+) =",
          tuple(noise[z] for z in (-1, 0, 1)))
    print("Parameters:", {key: str(val) for key, val in par.items()})

    # ---------------------------------------------------------- section A
    print("\n[A] Auction objects: rules-based integration versus the paper's closed forms")
    for r in R_POINTS:
        A, C = auction(par, r), closed_forms(par, r)
        same = all(A[key] == C[key] for key in C)
        print(f"  r = {r}: closed forms equal = {same}; Delta = {A['D']}, tau = {A['tau']}"
              f" (~{dec(A['tau'])}), g_L = {A['gL']} > c_L = 0: {A['gL'] > 0}, "
              f"a_L = {A['aL']} > 0: {A['aL'] > 0}, B(1/2) = {dec(gain(A, F(1, 2)))}, "
              f"g_H = {dec(A['gH'])}")

    # ---------------------------------------------------------- section B
    print("\n[B] Full enumeration at the three certificate strengths "
          "(both mixtures, directional completion)")
    store = {}
    for r in R_POINTS:
        A, res, err = enumerate_eq(par, noise, r)
        print(f"\n  r = {r} (~{dec(r, 4)}): {len(res)} equilibrium outcomes: {kinds(res)}")
        for rec in res:
            show(rec)
        store[r] = {rec["kind"]: rec["prof"] for rec in res}
        nt_dev = gross_ext(par, A, noise, F(0), "mix", F(1), 0) - par["k"]
        print(f"    no-trade purchase payoff under the completion = {nt_dev}")
        store[r]["nt_dev"] = nt_dev

    print("\n  Comparison with the values printed in memo C9:")
    memo = {
        F(63, 40): dict(bA=F(1258, 1487), EA=F(1567, 2974), ULA=F(-529, 7200),
                        mA=F(10921, 1421952), nt=F(-479, 50400),
                        bT=F(13249, 15791), sT=F(16652273, 16706878), ETd="0.525157"),
        F(79, 50): dict(bA=F(2090, 2319), EA=F(4137, 7730), ULA=F(-5887, 79000),
                        mA=F(3479731, 53151200), nt=F(-739, 79000),
                        bT=F(20791, 24734), sT=F(121328033, 124807764), ETd="0.520148"),
        F(317, 200): dict(bA=F(35450, 37031), EA=F(201299, 370310), ULA=F(-95823, 1268000),
                          mA=F(187972799, 1542902400), nt=F(-11671, 1268000),
                          bT=F(5303, 6297), sT=F(490344541, 517197798), ETd="0.515255"),
    }
    for r in R_POINTS:
        A_ = store[r]["interior mixture"]
        T_ = store[r]["threshold mixture"]
        m = memo[r]
        sigmaT = (T_["e"][1] - par["rho"]) / (1 - par["rho"])
        print(f"  r = {r}:")
        print(f"    beta_A  mine {A_['beta']}  memo {m['bA']}  equal {A_['beta'] == m['bA']}")
        print(f"    E_A     mine {A_['E']}  memo {m['EA']}  equal {A_['E'] == m['EA']}"
              f"  (~{dec(A_['E'])})")
        print(f"    U_L(1)  mine {A_['UL1']}  memo {m['ULA']}  equal {A_['UL1'] == m['ULA']}")
        print(f"    margin  mine {A_['margin1']}  memo {m['mA']}  equal {A_['margin1'] == m['mA']}")
        print(f"    O_H = E_A - 1/5: {A_['OH'] == A_['E'] - F(1, 5)}  (O_H = {A_['OH']})")
        print(f"    U_H(1)  on branch A = {A_['UH1']}")
        print(f"    no-trade payoff mine {store[r]['nt_dev']}  memo {m['nt']}  "
              f"equal {store[r]['nt_dev'] == m['nt']}")
        print(f"    beta_T  mine {T_['beta']}  memo {m['bT']}  equal {T_['beta'] == m['bT']}")
        print(f"    sigma_T mine {sigmaT}  memo {m['sT']}  equal {sigmaT == m['sT']}")
        print(f"    E_T     mine {T_['E']} (~{dec(T_['E'])})  memo ~{m['ETd']}  "
              f"equal to 6 dp {dec(T_['E']) == m['ETd']}")
        print(f"    U_H(1)  on branch T = {T_['UH1']}; U_L(1) = {T_['UL1']}; "
              f"flow-1 margin = {T_['margin1']}")
        print(f"    no-trade entry {store[r]['no trade']['E']}, ownership {store[r]['no trade']['OH']}")
    EA = [store[r]["interior mixture"]["E"] for r in R_POINTS]
    ET = [store[r]["threshold mixture"]["E"] for r in R_POINTS]
    print(f"  E_A differences: {EA[1] - EA[0]} (memo 47632/5747255, equal "
          f"{EA[1] - EA[0] == F(47632, 5747255)}), {EA[2] - EA[1]} (memo 240688/28624963, "
          f"equal {EA[2] - EA[1] == F(240688, 28624963)})")
    print(f"  E_T differences: {ET[1] - ET[0]} (~{dec(ET[1] - ET[0])}), "
          f"{ET[2] - ET[1]} (~{dec(ET[2] - ET[1])})")

    print("\n  Presence lam = 49/50 at r = 317/200:")
    par_l = dict(par, lam=F(49, 50))
    A, res, err = enumerate_eq(par_l, noise, F(317, 200))
    for rec in res:
        P = rec["prof"]
        print(f"    {rec['kind']}: alpha = {P['alpha']}, beta = {P['beta']}, E = {P['E']}")
    print("    memo: beta_A = 1772500/1814519, alpha_A = 35450/37031")

    # ---------------------------------------------------------- section C
    print("\n[C] The interval I = [63/40, 317/200]")
    print("  C.1 Identity B_r(mu_1(alpha_A)) - 6 = P(r) / (80 r (r-1)^2), at eight points:")

    def Ppoly(r):
        return -45 * r ** 4 + 514 * r ** 3 - 980 * r ** 2 + 454 * r - 15

    # Points where the root alpha_A keeps every flow mass positive, so that the
    # posterior formula applies; five points determine a quartic numerator.
    for r in (F(3, 2), F(31, 20), F(63, 40), F(79, 50), F(317, 200), F(8, 5), F(7, 4), F(9, 5)):
        A = auction(par, r)
        c = indifference_poly(par, A, noise, par["rho"], F(1))
        alphaA = -c[2] / c[1]          # u = v makes the equation linear (c[0] = 0)
        _, _, mu, _ = beliefs(par, noise, alphaA, F(1))
        lhs = gain(A, mu[1]) - par["cH"]
        rhs = Ppoly(r) / (80 * r * (r - 1) ** 2)
        print(f"    r = {r}: quadratic coefficient {c[0]}, alpha_A = {dec(alphaA)}, "
              f"identity holds {lhs == rhs}")
    print(f"  C.2 P(63/40) = {Ppoly(F(63, 40))} (memo 32763/102400); P(3/2) = {Ppoly(F(3, 2))}")
    r_lo, r_hi = F(8, 5), F(3, 2)
    bound = -180 * r_lo ** 3 + 1542 * r_hi ** 2 - 1960 * r_lo + 454
    print(f"      lower bound of P' on [3/2, 8/5] = {bound} (memo 2511/50)")
    print(f"      Delta at the ends of I: {auction(par, F(63, 40))['D']}, "
          f"{auction(par, F(317, 200))['D']} (memo 529/5040, 13689/126800)")

    print("  C.3 Enumeration on 101 rational points r = 63/40 + j/10000, j = 0..100")
    grid = [F(63, 40) + F(j, 10000) for j in range(101)]
    summary = {}
    for label, tie, off in (("mix, directional", "mix", F(1)),
                            ("mix, passive (1/2)", "mix", F(1, 2)),
                            ("enter at indifference, directional", "enter", F(1))):
        counts, kind_sets, EAs, ETs, worst = {}, set(), [], [], {}
        for r in grid:
            _, res, err = enumerate_eq(par, noise, r, tie, off)
            counts[len(res)] = counts.get(len(res), 0) + 1
            kind_sets.add(tuple(kinds(res)))
            for rec in res:
                P = rec["prof"]
                if rec["kind"] == "interior mixture":
                    EAs.append(P["E"])
                if rec["kind"] == "threshold mixture":
                    ETs.append(P["E"])
                bad = int(P["gap"] != 0 or not P["entry_ok"] or not P["one_entry"]
                          or P["pid"] != 0 or P["clash"] or bool(P["notes"]))
                worst["price or entry defect"] = worst.get("price or entry defect", 0) + bad
                if rec["kind"] in ("interior mixture", "threshold mixture"):
                    worst["U_H(1) != 0"] = worst.get("U_H(1) != 0", 0) + (P["UH1"] != 0)
                worst["U_L(1) >= 0"] = worst.get("U_L(1) >= 0", 0) + (P["UL1"] >= 0)
        print(f"    [{label}] outcome counts {counts}; outcome sets {sorted(kind_sets)}")
        print(f"      defects {worst}")
        if EAs:
            print(f"      E_A strictly increasing on the grid: "
                  f"{all(b > a for a, b in zip(EAs, EAs[1:]))}; range {dec(EAs[0])} to {dec(EAs[-1])}")
        if ETs:
            print(f"      E_T strictly decreasing on the grid: "
                  f"{all(b < a for a, b in zip(ETs, ETs[1:]))}; range {dec(ETs[0])} to {dec(ETs[-1])}")
        summary[label] = counts

    print("  C.4 No trade against every common off-path belief nu at flow 2")
    for r in (F(63, 40), F(317, 200)):
        A = auction(par, r)
        u, v, w = (noise[z] for z in (-1, 0, 1))
        base = A["D"] * (u + v) * par["rho"] / 2
        worst = base + w * A["D"] * max(par["rho"], 1 - A["tau"])
        split = base + w * A["D"]
        print(f"    r = {r}: sup over nu of the no-trade purchase payoff = {worst - par['k']} "
              f"(~{dec(worst - par['k'])}); if market maker and challenger could hold different "
              f"off-path beliefs: {dec(split - par['k'])}")
    print("    tau rises with r and Delta rises with r on I, so the sup is below")
    A1, A2 = auction(par, F(63, 40)), auction(par, F(317, 200))
    bnd = A2["D"] * (F(1, 10) + F(1, 5) * max(F(1, 4), 1 - A1["tau"])) - par["k"]
    print(f"    Delta(317/200) [1/10 + (1/5)(1 - tau(63/40))] - k = {dec(bnd, 8)}")

    # ---------------------------------------------------------- section D
    print("\n[D] Where branch A exists (benchmark noise)")
    lo, hi = F(3, 2), F(63, 40)
    for _ in range(60):
        mid = (lo + hi) / 2
        if Ppoly(mid) < 0:
            lo = mid
        else:
            hi = mid
    print(f"  lower end (P(r) = 0, branches A and T merge): r in [{dec(lo, 9)}, {dec(hi, 9)}]")
    # alpha_A = 1 <=> 11 Delta / 60 = k <=> Delta = 6/55 <=> 55 r^2 - 122 r + 55 = 0
    print("  upper end (alpha_A = 1, Delta = 6/55): r = (122 + sqrt(2784)) / 110 "
          f"~ {dec((122 + F(isqrt(2784 * 10 ** 30), 10 ** 15)) / 110, 9)}")
    print("  no-trade ceiling (Delta = 1/5): r = (12 + sqrt(44)) / 10 "
          f"~ {dec((12 + F(isqrt(44 * 10 ** 30), 10 ** 15)) / 10, 9)}")
    A = auction(par, F(317, 200))
    print(f"  full-purchase margin at r = 317/200: k - 11 Delta / 60 = {par['k'] - 11 * A['D'] / 60}")
    print("  tau = 2/3 (flow 1 stops recruiting under full purchases) at r = 1 + sqrt(288)/16 "
          f"~ {dec(1 + F(isqrt(288 * 10 ** 30), 10 ** 15) / 16, 6)}")
    for r in (F(157, 100), F(1574, 1000), F(15745, 10000), F(1586, 1000), F(1588, 1000),
              F(1589, 1000), F(16, 10), F(17, 10), F(186, 100), F(187, 100),
              F(19, 10), F(2), F(205, 100), F(207, 100)):
        _, res, err = enumerate_eq(par, noise, r)
        desc = ", ".join(f"{rec['kind']} (beta~{dec(rec['prof']['beta'], 4)}, "
                         f"E~{dec(rec['prof']['E'], 4)})" for rec in res)
        print(f"    r = {dec(r, 4)}: {desc}")

    # ---------------------------------------------------------- section E
    print("\n[E] Gap example of Proposition C9.5")
    par5 = dict(par, cH=F(83, 24), k=F(1, 10))
    noise5 = {-1: F(1, 5), 0: F(1, 5), 1: F(3, 5)}
    r5 = F(3)
    A5 = auction(par5, r5)
    print(f"  Delta = {A5['D']}, tau = {A5['tau']}, B(1/2) = {gain(A5, F(1, 2))} vs c_H = 83/24")
    for tie in ("enter", "stay", "mix"):
        _, res, err = enumerate_eq(par5, noise5, r5, tie)
        print(f"  tie rule '{tie}': {len(res)} outcomes {kinds(res)}")
        for rec in res:
            show(rec)
    for a in (F(0), F(1, 2), F(1)):
        print(f"    gross payoff at alpha = {a}: lowest {gross_ext(par5, A5, noise5, a, 'mix', F(1), 0)}, "
              f"highest {gross_ext(par5, A5, noise5, a, 'mix', F(1), 1)}")
    print("    gross payoff just above alpha = 1/2 (alpha = 1/2 + 1/10^9): "
          f"{dec(gross_ext(par5, A5, noise5, F(1, 2) + F(1, 10 ** 9), 'mix', F(1), 0), 9)}")
    print("    The no-trade test uses the completion nu = 1, which gives the smallest "
          "flow-2 residual (zero); no trade therefore fails under every off-path belief.")

    # ---------------------------------------------------------- section F
    print("\n[F] Role of the completion: equal noise, r = 3, k = 7/100, benchmark c_H")
    parF = dict(par, k=F(7, 100))
    noiseF = {-1: F(1, 3), 0: F(1, 3), 1: F(1, 3)}
    AF = auction(parF, F(3))
    print(f"  rho Delta / 3 = {parF['rho'] * AF['D'] / 3}, rho Delta / 2 = {parF['rho'] * AF['D'] / 2}, "
          f"tau = {AF['tau']}")
    for label, off in (("directional (nu = 1)", F(1)), ("passive (nu = 1/2)", F(1, 2)),
                       ("adverse (nu = 0)", F(0))):
        _, res, err = enumerate_eq(parF, noiseF, F(3), "mix", off)
        print(f"  {label}: {len(res)} outcomes {kinds(res)}")

    # ---------------------------------------------------------- section G
    print("\n[G] General-prior payoff formula of the memo versus first principles")
    for pi, alpha, e0, e1 in ((F(1, 3), F(2, 7), F(1, 3), F(7, 9)),
                              (F(4, 5), F(5, 6), F(1, 4), F(1))):
        parG = dict(par, pi=pi)
        noiseG = {-1: F(1, 2), 0: F(3, 10), 1: F(1, 5)}
        AG = auction(parG, F(5, 2))
        _, _, mu, _ = beliefs(parG, noiseG, alpha, F(1))
        e = {-1: F(1, 4), 0: e0, 1: e1, 2: F(1)}
        fp = payoffs(parG, AG, noiseG, mu, e)[0]
        u, v, w = (noiseG[z] for z in (-1, 0, 1))
        memoK = AG["D"] * (1 - pi) * (u * v * e0 / (v + pi * alpha * (u - v))
                                      + v * w * e1 / (w + pi * alpha * (v - w)))
        print(f"  pi = {pi}, alpha = {alpha}: first principles {fp}, memo formula {memoK}, "
              f"equal {fp == memoK}")
    root = 4 + F(isqrt(63 * 10 ** 30), 10 ** 15) / 2
    gH_at = lambda r: par["h"] - r / 2 - par["p"] ** 2 / (2 * r)
    print(f"  ceiling g_H(r) = 6 at r = 4 + sqrt(63)/2 ~ {dec(root, 6)}; "
          f"g_H(7.968) - 6 = {dec(gH_at(F(7968, 1000)) - 6, 6)}, "
          f"g_H(7.969) - 6 = {dec(gH_at(F(7969, 1000)) - 6, 6)}")

    # ---------------------------------------------------------- section H
    print("\n[H] Random exact sweep (numerical diagnostic): does an equilibrium always exist?")
    rng = random.Random(20261021)
    tally = {"mix": [0, 0, 0], "enter_low": [0, 0], "enter_high": [0, 0]}
    flags = {}
    first_gap = None
    for i in range(1500):
        p2 = dict(par)
        r = F(1) + F(rng.randint(1, 8999), 1000)
        raw = [rng.randint(1, 60) for _ in range(3)]
        s = sum(raw)
        nz = {-1: F(raw[0], s), 0: F(raw[1], s), 1: F(raw[2], s)}
        p2["pi"] = F(rng.randint(1, 9), 10)
        p2["lam"] = F(rng.randint(1, 10), 10)
        A0 = auction(p2, r)
        p2["cH"] = A0["gL"] + (A0["gH"] - A0["gL"]) * F(rng.randint(1, 1199), 1000)
        p2["k"] = A0["D"] * F(rng.randint(1, 999), 1000)
        A, res, err = enumerate_eq(p2, nz, r, "mix", F(1), build=False)
        if err:
            flags[err] = flags.get(err, 0) + 1
            continue
        tally["mix"][0] += 1
        tally["mix"][1] += (len(res) == 0)
        tally["mix"][2] += any(rec["kind"].startswith("threshold") for rec in res)
        A, res2, err2 = enumerate_eq(p2, nz, r, "enter", F(1), build=False)
        key = "enter_low" if gain(A, p2["pi"]) < p2["cH"] else "enter_high"
        tally[key][0] += 1
        tally[key][1] += (len(res2) == 0)
        if len(res2) == 0 and first_gap is None:
            first_gap = (r, nz, p2["pi"], p2["lam"], p2["cH"], p2["k"], kinds(res))
    print(f"  both mixtures: cases {tally['mix'][0]}, cases with no equilibrium {tally['mix'][1]}, "
          f"cases whose outcome set includes a challenger mixture {tally['mix'][2]}")
    print(f"  challenger enters at indifference, B(pi) < c_H: cases {tally['enter_low'][0]}, "
          f"no equilibrium {tally['enter_low'][1]}")
    print(f"  challenger enters at indifference, B(pi) >= c_H: cases {tally['enter_high'][0]}, "
          f"no equilibrium {tally['enter_high'][1]}")
    print(f"  skipped (posterior constant at tau): {flags}")
    if first_gap:
        r, nz, pi_, lam_, cH_, k_, kk = first_gap
        print(f"  first gap: r = {r}, noise = {[str(nz[z]) for z in (-1, 0, 1)]}, pi = {pi_}, "
              f"lam = {lam_}, c_H ~ {dec(cH_)}, k ~ {dec(k_)}; with both mixtures: {kk}")


if __name__ == "__main__":
    main()
