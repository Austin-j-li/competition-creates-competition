"""N2, extension B: two order slots with fresh informed arrivals (calibration beta = 1/3, lam = 1/6, u = 3/5).

Part 1: r = 3. Unique full orders. Exact price path, informed residuals, the early-trader term
        w_L (E[e|H,h] - E[e|L,h]), price access (Prop. A.9 analog).
Part 2: r in {31/20, 8/5, 33/20} and a strength grid. Every margin of the classification lemma is printed,
        then every equilibrium: no trade (NT), full-full (FF), and the threshold branch (TH, challenger mixes).

Print-only. All economic quantities use fractions.Fraction. Run from the repository root:
  .venv/bin/python audit/microstructure_search_2026_10_22/scripts/N2_dynamics/two_slot_fresh.py
"""
import sys
import os
from fractions import Fraction as F
from itertools import product

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from n2_common import RHO, K, R1, R2, MID, objects, entry, B, CH, dec, head  # noqa: E402

BETA, LAM = F(1, 3), F(1, 6)
B_ = (1 - LAM) * BETA           # liquidity buy (or sell) mass per slot
C0 = (1 - LAM) * (1 - 2 * BETA)  # liquidity zero mass per slot
U = LAM / B_
Q = (1, 0, -1)


def law(rates, j, h):
    """Slot order law at history h for class j. rates: dict (slot, history) -> (a, s)."""
    a, s = rates[h]
    if j == "H":
        return {1: B_ + a, 0: C0 + LAM - a, -1: B_}
    return {1: B_, 0: C0 + LAM - s, -1: B_ + s}


def solve_path(o, rates, zeta=None):
    """Posteriors, entry, prices for a two-slot profile. zeta: optional dict terminal -> preparation prob."""
    hist1 = [(q,) for q in Q]
    hist2 = [(q1, q2) for q1 in Q for q2 in Q]
    pr = {("H", ()): F(1), ("L", ()): F(1)}
    for j in ("H", "L"):
        for h in hist1:
            pr[(j, h)] = law(rates, j, ())[h[0]]
        for h in hist2:
            pr[(j, h)] = pr[(j, h[:1])] * law(rates, j, h[:1])[h[1]]
    mu = {h: pr[("H", h)] / (pr[("H", h)] + pr[("L", h)]) for h in [()] + hist1 + hist2}
    e = {}
    for h in hist2:
        if zeta is not None and h in zeta:
            e[h] = RHO + (1 - RHO) * zeta[h]
        else:
            e[h] = entry(o, mu[h])
    # expected entry given class and an interim history
    Ee = {}
    for j in ("H", "L"):
        for h in [()] + hist1:
            tot, w = F(0), F(0)
            for hh in hist2:
                if hh[:len(h)] == h:
                    p = pr[(j, hh)] / pr[(j, h)]
                    tot += p * e[hh]
                    w += p
            Ee[(j, h)] = tot / w
    price = {}
    for h in hist2:
        price[h] = o["t0"] + e[h] * (o["wL"] + o["D"] * mu[h])
    for h in [()] + hist1:
        vH = o["t0"] + o["wH"] * Ee[("H", h)]
        vL = o["t0"] + o["wL"] * Ee[("L", h)]
        price[h] = mu[h] * vH + (1 - mu[h]) * vL
    Dh = {h: o["wH"] * Ee[("H", h)] - o["wL"] * Ee[("L", h)] for h in [()] + hist1}
    for h in hist2:
        Dh[h] = e[h] * o["D"]
    ent = sum((pr[("H", h)] + pr[("L", h)]) / 2 * e[h] for h in hist2)
    return dict(mu=mu, e=e, Ee=Ee, price=price, Dh=Dh, entry=ent, pr=pr)


def residuals(o, sol):
    """Gross informed returns of a buy (H) and a sale (L) at each decision node."""
    out = {}
    for h in [()] + [(q,) for q in Q]:
        hb, hs = h + (1,), h + (-1,)
        out[("H", h)] = (1 - sol["mu"][hb]) * sol["Dh"][hb]
        out[("L", h)] = sol["mu"][hs] * sol["Dh"][hs]
    return out


def full_rates():
    return {h: (LAM, LAM) for h in [()] + [(q,) for q in Q]}


def part1():
    head("Part 1. r = 3, full orders at every node (unique by the margin below)")
    o = objects(R1)
    M1 = (1 + U) / (2 + U)
    M2 = (1 + U) ** 2 / (1 + (1 + U) ** 2)
    print(f"  beta = {BETA}, lam = {LAM}, b = {B_}, c0 = {C0}, u = {U}; M_1 = {M1}, M_2 = {M2} (~{dec(M2, 6)})")
    print(f"  tau(3) = {o['tau']} <= M_2 = {M2} < tau(3.6) = {objects(R2)['tau']}: "
          f"{o['tau'] <= M2 < objects(R2)['tau']}")
    for r in (R1, R2):
        oo = objects(r)
        print(f"  uniqueness margin at r = {r}: rho Delta (1 - M_2) - k = {RHO * oo['D'] * (1 - M2) - K}")
    sol = solve_path(o, full_rates())
    res = residuals(o, sol)
    print(f"  entry E_2(3) = {sol['entry']} (~{dec(sol['entry'], 6)})")
    print("  history   posterior        entry   price            (static P(mu) for interim nodes)")
    for h in [()] + [(q,) for q in Q] + [(a, b) for a in Q for b in Q]:
        stat = ""
        if len(h) < 2:
            ps = o["t0"] + entry(o, sol["mu"][h]) * (o["wL"] + o["D"] * sol["mu"][h])
            stat = f"static {dec(ps, 6)}"
        ee = sol["e"][h] if len(h) == 2 else (sol["Ee"][("H", h)] * sol["mu"][h]
                                                + sol["Ee"][("L", h)] * (1 - sol["mu"][h]))
        print(f"  {str(h):9s} {str(sol['mu'][h]):8s} (~{dec(sol['mu'][h], 4)})  {dec(ee, 4)}  "
              f"{str(sol['price'][h]):16s} (~{dec(sol['price'][h], 6)})  {stat}")
    print("  price impact of a buy:")
    for h in [()] + [(q,) for q in Q]:
        print(f"    at {str(h):6s}: P(h,+) - P(h) = {dec(sol['price'][h + (1,)] - sol['price'][h], 6)};"
              f"  P(h) - P(h,-) = {dec(sol['price'][h] - sol['price'][h + (-1,)], 6)}")
    print("  informed gross returns (k = 1/50):")
    for key, v in res.items():
        print(f"    {key[0]} at {str(key[1]):6s}: {v} (~{dec(v, 6)})")
    hb = (1,)
    eh, el = sol["Ee"][("H", hb)], sol["Ee"][("L", hb)]
    prem = o["wL"] * (eh - el)
    print(f"  slot-1 buy: D(+) = Delta E[e|H,+] + w_L (E[e|H,+] - E[e|L,+]) = {dec(o['D'] * eh, 6)} + "
          f"{dec(prem, 6)} = {dec(sol['Dh'][hb], 6)}")
    print(f"  early-trader term share of D(+): {dec(prem / sol['Dh'][hb], 4)}")
    print(f"  slot-1 H return (1 - mu_1(+)) D(+) = {dec(res[('H', ())], 6)};"
          f" slot-2 H return at + : {dec(res[('H', (1,))], 6)}")
    # expected informed profit per slot (conditional on an informed arrival), class H
    p1 = res[("H", ())] - K
    p2 = sum(sol["pr"][("H", (q,))] * max(res[("H", (q,))] - K, F(0)) for q in Q)
    print(f"  class-H expected net profit: slot 1 = {dec(p1, 6)}, slot 2 = {dec(p2, 6)}")
    # price access versus hidden price (Prop. A.9 analog)
    hid = {h: entry(o, F(1, 2)) for h in [(a, b) for a in Q for b in Q]}
    sol_h = solve_path(o, full_rates(), zeta={h: F(0) for h in hid})
    for r in (R1,):
        Mh = max(sol_h["mu"].values())
        print(f"  hidden price: entry = {sol_h['entry']}; margin rho Delta (1 - M_2) - k = "
              f"{RHO * o['D'] * (1 - Mh) - K} (full orders also forced)")
    dR = F(0)
    dW = F(0)
    for h in [(a, b) for a in Q for b in Q]:
        if sol["e"][h] > RHO:
            Dx = (sol["pr"][("H", h)] + sol["pr"][("L", h)]) / 2
            dR += (1 - RHO) * Dx * (o["wL"] + o["D"] * sol["mu"][h])
            dW += (1 - RHO) * Dx * (B(o, sol["mu"][h]) - CH + F(1, 4) / o["r"])
    print(f"  price access raises proceeds by {dR} (~{dec(dR, 6)}) and net surplus by {dW} (~{dec(dW, 6)})")
    print(f"  ceiling r_C(M_2) solves B_r(M_2) = 6 (see n_slots_ladder.py for the closed form)")


def kthr(o, a1, T, estar):
    """Slot-1 class-H return on the threshold branch, as a function of a1."""
    a2 = B_ * (T * B_ / (B_ + a1) - 1)
    eH = RHO + (estar - RHO) * (B_ + a2)
    eL = RHO + (estar - RHO) * B_
    D = o["wH"] * eH - o["wL"] * eL
    return B_ / (2 * B_ + a1) * D, a2


def classify(r, verbose=True):
    o = objects(r)
    T = o["tau"] / (1 - o["tau"])
    M1 = (1 + U) / (2 + U)
    lines = []
    ok = True
    # lemma margins
    m = {
        "L slot 1: rho Delta/2 - k (<0)": RHO * o["D"] / 2 - K,
        "no recruit after a slot-1 sale: (1+u) - T (<0)": (1 + U) - T,
        "L slot 2: rho Delta M_1 - k (<0)": RHO * o["D"] * M1 - K,
        "H slot 2 at 0: rho Delta (1 - 5/13) - k (<0)": RHO * o["D"] * (1 - F(5, 13)) - K,
        "recruited interior impossible: 1 - k/Delta - M_2 (>0)": 1 - K / o["D"] - (1 + U) ** 2 / (1 + (1 + U) ** 2),
        "only (+,+) can recruit: T - (1+u) (>0)": T - (1 + U),
    }
    for key, v in m.items():
        good = (v < 0) if "(<0)" in key else (v > 0)
        ok = ok and good
        lines.append(f"    {key}: {dec(v, 6)} {'ok' if good else 'FAILS'}")
    eqs = []
    # NT
    if RHO * o["D"] / 2 <= K:
        eqs.append(("NT", RHO, "a1 = 0"))
    # FF
    ff_valid = (1 + U) ** 2 >= T
    sol = solve_path(o, {(): (LAM, F(0)), (1,): (LAM, F(0)), (0,): (F(0), F(0)), (-1,): (F(0), F(0))})
    res = residuals(o, sol)
    k1 = res[("H", ())]
    k2 = res[("H", (1,))]
    if ff_valid and k1 >= K and k2 >= K:
        eqs.append(("FF", sol["entry"], f"slot-1 return {dec(k1, 6)}, slot-2 return at + {dec(k2, 6)}"))
    # TH (challenger mixes at (+,+); investor rule IM)
    estar = K / (o["D"] * (1 - o["tau"]))
    if RHO <= estar <= 1:
        lo = B_ * (T / (1 + U) - 1)
        hi = min(LAM, B_ * (T - 1))
        if lo < hi:
            klo, _ = kthr(o, lo, T, estar)
            khi, _ = kthr(o, hi, T, estar)
            if khi >= K and hi == LAM:
                a1 = LAM
                note = "a1 = lam"
            elif klo > K > khi:
                x, y = lo, hi
                for _ in range(80):
                    mid = (x + y) / 2
                    if kthr(o, mid, T, estar)[0] > K:
                        x = mid
                    else:
                        y = mid
                a1 = (x + y) / 2
                note = f"a1/lam in [{dec(x / LAM, 9)}, {dec(y / LAM, 9)}]"
            else:
                a1 = None
                note = "no root"
            if a1 is not None:
                ent = RHO + (estar - RHO) * B_ ** 2 * (1 + T) / 2
                a2 = kthr(o, a1, T, estar)[1]
                eqs.append(("TH", ent, f"{note}; a2/lam ~ {dec(a2 / LAM, 6)}; high-cost prep prob at (+,+) "
                                       f"{dec((estar - RHO) / (1 - RHO), 6)}"))
    if verbose:
        print(f"  r = {r} (~{dec(o['r'], 4)}): tau = {dec(o['tau'], 6)}, T = {dec(T, 6)}")
        for ln in lines:
            print(ln)
        for name, ent, note in eqs:
            print(f"    {name}: entry = {ent if name != 'TH' else dec(ent, 10)} (~{dec(ent, 6)}); {note}")
    return ok, eqs


def part2():
    head("Part 2. Intermediate strengths: lemma margins and the complete equilibrium list")
    for r in MID:
        classify(r)
    head("Part 2b. Strength grid (classification valid only where every margin is ok)")
    print("   r      lemma  NT     FF entry   TH entry")
    for i in range(30, 76, 2):
        r = F(100 + i * 1, 100)
        ok, eqs = classify(r, verbose=False)
        d = {n: e for n, e, _ in eqs}
        print(f"  {dec(r, 2):6s} {'ok  ' if ok else 'no  '}  {'yes' if 'NT' in d else 'no ':3s}   "
              f"{dec(d['FF'], 6) if 'FF' in d else '   -    ':10s} {dec(d['TH'], 6) if 'TH' in d else '   -'}")


if __name__ == "__main__":
    part1()
    part2()
