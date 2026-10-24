"""Brute-force enumeration of equilibria of the three-point stake model (exact fractions; print only).

For each stake omega the script scans a rational grid of investor mixing pairs (bH, bL).
At each on-path profile it builds the entry schedule from the challenger rule, and lets the
high-cost challenger mix only where a flow posterior equals tau exactly. Investor conditions are
checked from the primitive payoffs in tp_lib.payoffs (no closed form is used for the checks).
Off-path flows (no trade: flow 2; pooled buying: flow -1) are scanned over beliefs.

Usage (repo root):
    .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/C5_stake/tp_enumerate.py
"""
import os
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tp_lib import BENCH, R0, R1, R2, auction, tau_of, flows, posterior, payoffs, gains  # noqa: E402

PAR = BENCH
RHO = PAR["rho"]


def entry_vector(a, mu, phi_free):
    """e[x] for x in -1..2 from posteriors mu[x] (None = off path handled by caller).
    phi_free: dict flow -> phi to use where posterior equals tau."""
    e = {}
    for x in (-1, 0, 1, 2):
        m = mu[x]
        ph = None
        if m is not None:
            b = a["gL"] + m * (a["gH"] - a["gL"])
            if b > PAR["cH"]:
                ph = F(1)
            elif b < PAR["cH"]:
                ph = F(0)
            else:
                ph = phi_free.get(x, F(1))
        e[x] = RHO + (1 - RHO) * ph if ph is not None else None
    return e


def classify_on_path(a, omega, bH, bL):
    """Return list of equilibrium records at an on-path profile (all four flows have positive mass)."""
    fH, fL = flows(bH, bL)
    mu = {x: posterior(fH, fL, x) for x in (-1, 0, 1, 2)}
    if any(m is None for m in mu.values()):
        return None  # off path flow: handled elsewhere
    tau_flows = []
    for x in (-1, 0, 1, 2):
        b = a["gL"] + mu[x] * (a["gH"] - a["gL"])
        if b == PAR["cH"]:
            tau_flows.append(x)
    results = []
    if not tau_flows:
        e = entry_vector(a, mu, {})
        pay = payoffs(a, PAR, omega, bH, bL, e, mu)
        g = gains(pay)
        ok = ok_conditions(bH, bL, g)
        if ok:
            results.append(dict(phi={}, gains=g, e=e, mu=mu, strict=strict_ok(bH, bL, g)))
        return results
    if len(tau_flows) > 1:
        return [dict(note="two flows at tau", phi={}, gains={}, e={}, mu=mu, strict=False)]
    x0 = tau_flows[0]
    e0 = entry_vector(a, mu, {x0: F(0)})
    e1 = entry_vector(a, mu, {x0: F(1)})
    g0 = gains(payoffs(a, PAR, omega, bH, bL, e0, mu))
    g1 = gains(payoffs(a, PAR, omega, bH, bL, e1, mu))
    # gains are affine in phi: g(phi) = g0 + phi (g1 - g0). Find phi in [0,1] meeting both conditions.
    lo, hi = F(0), F(1)
    for j, bj in (("H", bH), ("L", bL)):
        s = g1[j] - g0[j]
        c = g0[j]
        if 0 < bj < 1:     # need g = 0
            if s == 0:
                if c != 0:
                    return []
            else:
                root = -c / s
                lo, hi = max(lo, root), min(hi, root)
        elif bj == 1:      # need g >= 0
            if s == 0:
                if c < 0:
                    return []
            elif s > 0:
                lo = max(lo, -c / s)
            else:
                hi = min(hi, -c / s)
        else:              # bj == 0 need g <= 0
            if s == 0:
                if c > 0:
                    return []
            elif s > 0:
                hi = min(hi, -c / s)
            else:
                lo = max(lo, -c / s)
    if lo > hi:
        return []
    # report the interval of phi; the strict challenger rule needs phi = 1 inside the interval
    phi_set = (lo, hi)
    gg = {j: g0[j] + hi * (g1[j] - g0[j]) for j in g0}
    strict = (hi == F(1)) and strict_ok(bH, bL, {j: g0[j] + F(1) * (g1[j] - g0[j]) for j in g0})
    return [dict(phi={x0: phi_set}, gains=gg, e=e1, mu=mu, strict=strict)]


def ok_conditions(bH, bL, g):
    for j, bj in (("H", bH), ("L", bL)):
        if bj == 0 and g[j] > 0:
            return False
        if bj == 1 and g[j] < 0:
            return False
        if 0 < bj < 1 and g[j] != 0:
            return False
    return True


def strict_ok(bH, bL, g):
    """Prescribed investor tie rule: pure orders only; a buyer needs a strictly positive gain."""
    for j, bj in (("H", bH), ("L", bL)):
        if bj not in (0, 1):
            return False
        if bj == 1 and g[j] <= 0:
            return False
        if bj == 0 and g[j] > 0:
            return False
    return True


def offpath_support(a, omega, bH, bL, beliefs):
    """For no trade (bH=bL=0, flow 2 off path) or pooled buying (1,1; flow -1 off path):
    list the supporting (belief, phi) pairs among the scanned beliefs."""
    fH, fL = flows(bH, bL)
    mu = {x: posterior(fH, fL, x) for x in (-1, 0, 1, 2)}
    off = [x for x in mu if mu[x] is None]
    x_off = off[0]
    sup = []
    tau = tau_of(a, PAR)
    for m in beliefs:
        mu_try = dict(mu)
        mu_try[x_off] = m
        b = a["gL"] + m * (a["gH"] - a["gL"])
        phis = [F(0)] if b < PAR["cH"] else ([F(1)] if b > PAR["cH"] else [F(0), F(1, 4), F(1, 2), F(3, 4), F(1)])
        for ph in phis:
            e = {}
            for x in (-1, 0, 1, 2):
                if x == x_off:
                    e[x] = RHO + (1 - RHO) * ph
                else:
                    ph_x = phi_x(a, mu_try[x])
                    e[x] = RHO + (1 - RHO) * ph_x
            pay = payoffs(a, PAR, omega, bH, bL, e, mu_try)
            g = gains(pay)
            if ok_conditions(bH, bL, g):
                sup.append((m, ph, g))
    return sup


def phi_x(a, m):
    b = a["gL"] + m * (a["gH"] - a["gL"])
    if b > PAR["cH"]:
        return F(1)
    if b < PAR["cH"]:
        return F(0)
    return F(1)


def d1_and_ic_for_no_trade(a, omega):
    """Compute D1 and Intuitive-Criterion beliefs at flow 2 under no trade; return verdicts."""
    tau = tau_of(a, PAR)
    mus = [F(i, 400) for i in range(401)] + ([tau] if tau <= 1 else [])
    resp = []
    for m in mus:
        b = a["gL"] + m * (a["gH"] - a["gL"])
        phis = [F(0)] if b < PAR["cH"] else ([F(1)] if b > PAR["cH"] else [F(0), F(1, 2), F(1)])
        for ph in phis:
            resp.append((m, ph))
    gH, gL = {}, {}
    for (m, ph) in resp:
        mu = {-1: F(1, 2), 0: F(1, 2), 1: F(1, 2), 2: m}
        e = {-1: RHO, 0: RHO, 1: RHO, 2: RHO + (1 - RHO) * ph}
        g = gains(payoffs(a, PAR, omega, F(0), F(0), e, mu))
        gH[(m, ph)] = g["H"]
        gL[(m, ph)] = g["L"]
    maxH, maxL = max(gH.values()), max(gL.values())
    # IC: deviation equilibrium-dominated for t if max gain < 0
    dom_H, dom_L = maxH < 0, maxL < 0
    # D1: L deleted if every response with gL >= 0 has gH > 0 (proper subset test)
    setL = {r for r in resp if gL[r] >= 0}
    setH0 = {r for r in resp if gH[r] > 0}
    d1_deletes_L = setL.issubset(setH0) and len(setH0) > 0
    out = dict(maxH=maxH, maxL=maxL, ic_L_dominated=dom_L, ic_H_dominated=dom_H,
               d1_deletes_L=d1_deletes_L)
    # belief 1 outcome
    m1 = F(1)
    e = {-1: RHO, 0: RHO, 1: RHO, 2: RHO + (1 - RHO) * phi_x(a, m1)}
    mu = {-1: F(1, 2), 0: F(1, 2), 1: F(1, 2), 2: m1}
    g1 = gains(payoffs(a, PAR, omega, F(0), F(0), e, mu))
    out["gain_H_at_belief1"] = g1["H"]
    out["gain_L_at_belief1"] = g1["L"]
    # NT survives IC / D1?
    if dom_L and not dom_H:
        out["IC_belief"] = 1
        out["NT_survives_IC"] = g1["H"] <= 0
    else:
        out["IC_belief"] = "free"
        out["NT_survives_IC"] = True if (maxH <= 0 and maxL <= 0) else None
    if d1_deletes_L:
        out["D1_belief"] = 1
        out["NT_survives_D1"] = g1["H"] <= 0
    else:
        out["D1_belief"] = "free"
        out["NT_survives_D1"] = None
    return out


def outcome(a, rec, bH, bL):
    e = rec["e"]
    if not e or any(v is None for v in e.values()):
        return None
    fH, fL = flows(bH, bL)
    eH = sum(fH[x] * e[x] for x in e)
    eL = sum(fL[x] * e[x] for x in e)
    return dict(E=(eH + eL) / 2, OH=eH / 2, eL=eL, eH=eH)


def outcome_phi(a, rec, bH, bL):
    """Entry and ownership with the challenger mixing probability phi taken from the equilibrium record."""
    e = dict(rec["e"])
    if rec["phi"]:
        for x, (lo, hi) in rec["phi"].items():
            e[x] = RHO + (1 - RHO) * hi
    fH, fL = flows(bH, bL)
    eH = sum(fH[x] * e[x] for x in e)
    eL = sum(fL[x] * e[x] for x in e)
    return dict(E=(eH + eL) / 2, OH=eH / 2)


def run(r, omega_list, label):
    a = auction(r, PAR)
    tau = tau_of(a, PAR)
    print(f"\n=== {label}: r={r} tau={tau} ({float(tau):.6f}) ===")
    # grid axis: multiples of 1/60 plus the exact recruiting limit beta_max and a few multiples of it
    axis_set = {F(i, 60) for i in range(61)}
    if 0 < tau < 1:
        bm = 1 / tau - 1
        for i in range(1, 6):
            axis_set.add(bm * F(i, 5))
    base_axis = sorted(v for v in axis_set if 0 <= v <= 1)
    N = 60
    for om in omega_list:
        axis = list(base_axis)
        # add the L-indifference point on the axis (first-principles root is found by bisection below)
        found = []
        for bH in axis:
            for bL in axis:
                if bL > bH + F(1, 10**9):
                    continue  # reversed profiles are scanned separately below (kept for completeness)
                if (bH == 0 and bL == 0) or (bH == 1 and bL == 1):
                    continue
                recs = classify_on_path(a, om, bH, bL)
                if recs:
                    for rec in recs:
                        found.append((bH, bL, rec))
        # reversed profiles (bL > bH): coarse scan
        rev = []
        for i in range(0, N + 1, 3):
            for j in range(0, N + 1, 3):
                bH, bL = F(i, N), F(j, N)
                if bL <= bH or (bH == 0 and bL == 0):
                    continue
                recs = classify_on_path(a, om, bH, bL)
                if recs:
                    rev.append((bH, bL))
        # bisection for the L-indifference root at bH = 1 (first principles)
        root = bisect_L(a, om)
        # report
        print(f"\n omega = {om} ({float(om):.6f})")
        cont = [(bH, bL, rec) for (bH, bL, rec) in found if bL == 0 and 0 < bH < 1 and not rec["phi"]]
        found = [x for x in found if x not in cont]
        if cont:
            Es = [outcome(a, rec, bH, bL)["E"] for (bH, bL, rec) in cont]
            print(f"   H-mixing continuum (bL=0): {len(cont)} grid points, bH from {cont[0][0]} to {cont[-1][0]}, "
                  f"E from {float(min(Es)):.6f} to {float(max(Es)):.6f}")
        for bH, bL, rec in found:
            o = outcome(a, rec, bH, bL)
            phi = {x: (str(v[0]), str(v[1])) for x, v in rec["phi"].items()} if rec["phi"] else {}
            o2 = outcome_phi(a, rec, bH, bL)
            print(f"   EQ bH={bH} bL={bL}  phi={phi}  strict={rec['strict']}  "
                  + (f"E={float(o2['E']):.6f} O_H={float(o2['OH']):.6f}" if o2 else ""))
        if root is not None:
            fH_, fL_ = flows(F(1), root)
            mu_ = {x: posterior(fH_, fL_, x) for x in (-1, 0, 1, 2)}
            e_ = entry_vector(a, mu_, {})
            g_ = gains(payoffs(a, PAR, om, F(1), root, e_, mu_))
            print(f"   interior L-mix root (bH=1) bisection: bL~{float(root):.9f}; gains at root: "
                  f"H={float(g_['H']):.9f} L={float(g_['L']):.3e}")
        print(f"   reversed profiles supported on the coarse scan: {len(rev)}")
        # no-trade
        beliefs = [F(i, 200) for i in range(201)] + ([tau] if tau <= 1 else [])
        sup = offpath_support(a, om, F(0), F(0), beliefs)
        print(f"   no trade (bH=bL=0): supported by {len(sup)} (belief,phi) pairs"
              + (f"; belief range [{float(min(s[0] for s in sup))},{float(max(s[0] for s in sup))}]" if sup else ""))
        d = d1_and_ic_for_no_trade(a, om)
        print(f"     maxH gain={float(d['maxH']):.6f} maxL gain={float(d['maxL']):.6f}; "
              f"IC: L dominated={d['ic_L_dominated']}, belief={d['IC_belief']}, NT survives IC={d['NT_survives_IC']}; "
              f"D1 deletes L={d['d1_deletes_L']}, belief={d['D1_belief']}, NT survives D1={d['NT_survives_D1']}")
        # pooled buying
        sup11 = offpath_support(a, om, F(1), F(1), beliefs)
        print(f"   pooled buying (bH=bL=1): supported by {len(sup11)} (belief,phi) pairs")


def bisect_L(a, om):
    """Find bL in (0, beta_max] with gain_L = 0 at bH = 1 by exact bisection (first principles)."""
    tau = tau_of(a, PAR)
    if not (0 < tau < 1):
        return None
    bmax = 1 / tau - 1

    def gL(bL):
        e_fl = flows(F(1), bL)
        fH, fL = e_fl
        mu = {x: posterior(fH, fL, x) for x in (-1, 0, 1, 2)}
        e = entry_vector(a, mu, {})
        return gains(payoffs(a, PAR, om, F(1), bL, e, mu))["L"]
    lo, hi = F(0), bmax - F(1, 10**12)
    if gL(lo) > 0 or gL(hi) < 0:
        return None
    for _ in range(80):
        mid = (lo + hi) / 2
        if gL(mid) < 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


if __name__ == "__main__":
    rho, k = PAR["rho"], PAR["k"]

    def thr(r):
        a = auction(r, PAR)
        tau = tau_of(a, PAR)
        wH = (3 * k - rho * a["D"]) / ((1 - rho) * a["wH"])
        O2 = ((rho + tau) * a["D"] + 3 * k) / ((1 - rho) * a["wL"])
        O1 = ((1 + rho) * a["D"] + 3 * k) / ((1 - rho) * a["wL"])
        return wH, O2, O1

    wH1, Om2, Om1 = thr(R1)
    run(R1, [F(0), F(1), Om2, F(23, 10), Om1, Om1 + F(1, 100), F(5), F(50)], "STRONG r1")
    wH0, Om2_0, Om1_0 = thr(R0)
    run(R0, [F(0), F(1, 10), wH0, wH0 + F(1, 1000), Om2_0, Om1_0, Om1_0 + F(1, 100), F(1)], "WEAK r0")
    run(F(3, 2), [F(0), F(1, 10), F(1, 5), F(1, 2)], "r = 3/2 (between r0 and the zero-stake cutoff)")
    run(F(2), [F(0), F(1), F(3, 2)], "r = 2 (just above the zero-stake cutoff 1.9732)")
    run(F(9), [F(0), F(1), F(10), F(1000)], "r = 9 (above the ceiling 7.9686: no high-cost entry at any belief)")
