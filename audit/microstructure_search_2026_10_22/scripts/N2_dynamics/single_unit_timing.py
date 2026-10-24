"""N2, extension C: one informed investor with one unit and a choice of trade date (two slots).

Model. Class j in {H, L}, prior 1/2. With probability lam an informed investor is present for the whole
window and sees j. At each slot a liquidity trader draws an order from eta = (beta, 1-2beta, beta) on
(-1, 0, 1), unless the informed investor trades at that slot: its unit order (H buys, L sells) then
replaces the liquidity order. The investor trades at most once. x_j = P(trade at slot 1 | present);
y_j(q1) = P(trade at slot 2 | present, waited, liquidity order q1 at slot 1). Market makers see the
orders; P_t = E[V_T | orders so far]. The challenger sees the prices and decides after slot 2.
Menus: two-sided (both classes trade) and buy-only (class L never trades).

Print-only. Prices, posteriors and payoffs are computed exactly with fractions.Fraction at rational
strategies; mixing rates are located by rational bisection and reported as brackets.
Run from the repository root:
  .venv/bin/python audit/microstructure_search_2026_10_22/scripts/N2_dynamics/single_unit_timing.py
"""
import sys
import os
import random
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from n2_common import RHO, K, R1, R2, objects, dec, head  # noqa: E402

Q = (1, 0, -1)


class Model:
    def __init__(self, r, lam, beta, menu, access=True):
        self.o = objects(r)
        self.lam, self.beta, self.menu, self.access = lam, beta, menu, access
        self.eta = {1: beta, 0: 1 - 2 * beta, -1: beta} if menu == "two" else {1: beta, 0: 1 - beta, -1: F(0)}
        self.own = {"H": 1, "L": -1}

    def u(self):
        lam, beta = self.lam, self.beta
        if self.menu == "two":
            return lam / ((1 - lam) * beta)
        return lam * (1 - beta) / beta

    def hist_prob(self, j, h, st):
        """P(order history h | class j). st: dict with x[j], y[j][q1]."""
        lam, eta = self.lam, self.eta
        x = st["x"][j]
        o = self.own[j]
        q1 = h[0]
        if len(h) == 1:
            return (1 - lam * x) * eta[q1] + lam * x * (1 if q1 == o else 0)
        q2 = h[1]
        y = st["y"][j][q1]
        p = (1 - lam) * eta[q1] * eta[q2]
        p += lam * x * (1 if q1 == o else 0) * eta[q2]
        p += lam * (1 - x) * eta[q1] * (y * (1 if q2 == o else 0) + (1 - y) * eta[q2])
        return p

    def solve(self, st, zeta=None):
        o = self.o
        hs1 = [(q,) for q in Q if self.eta[q] > 0 or q == 1 or (self.menu == "two")]
        hs2 = [(a, b) for (a,) in hs1 for b in Q]
        mu, pr = {}, {}
        for h in hs1 + hs2:
            ph, pl = self.hist_prob("H", h, st), self.hist_prob("L", h, st)
            pr[h] = (ph, pl)
            mu[h] = ph / (ph + pl) if ph + pl > 0 else None
        e = {}
        for h in hs2:
            if mu[h] is None:
                e[h] = None
                continue
            if not self.access:
                e[h] = RHO
            else:
                bval = o["gL"] + mu[h] * (o["gH"] - o["gL"])
                if zeta is not None and h in zeta and bval == 6:
                    e[h] = RHO + (1 - RHO) * zeta[h]
                else:
                    e[h] = F(1) if bval >= 6 else RHO
        price = {}
        for h in hs2:
            if mu[h] is not None:
                price[h] = o["t0"] + e[h] * (o["wL"] + o["D"] * mu[h])
        for h in hs1:
            if mu[h] is None:
                continue
            tot, w = F(0), F(0)
            for j, wj in (("H", o["wH"]), ("L", o["wL"])):
                for b in Q:
                    hh = h + (b,)
                    pj = pr[hh][0] if j == "H" else pr[hh][1]
                    if pj > 0:
                        tot += pj * (o["t0"] + e[hh] * wj)
                        w += pj
            price[h] = tot / w
        ent = sum((pr[h][0] + pr[h][1]) / 2 * e[h] for h in hs2 if e[h] is not None)
        return dict(mu=mu, e=e, price=price, pr=pr, entry=ent, hs1=hs1, hs2=hs2)

    def values(self, sol, j):
        """Net payoffs for class j (present): trade now; trade at slot 2 after q1; continuation of waiting."""
        o, eta = self.o, self.eta
        oj = self.own[j]
        wj = o["wH"] if j == "H" else o["wL"]
        sgn = 1 if j == "H" else -1
        h1 = (oj,)
        val_after = sum(eta[b] * (o["t0"] + sol["e"][h1 + (b,)] * wj) for b in Q if eta[b] > 0)
        now = sgn * (val_after - sol["price"][h1]) - K
        later = {}
        for (q1,) in sol["hs1"]:
            if eta[q1] == 0:
                continue
            hh = (q1, oj)
            later[q1] = sgn * (o["t0"] + sol["e"][hh] * wj - sol["price"][hh]) - K
        wait = sum(eta[q1] * max(v, F(0)) for q1, v in later.items())
        return now, later, wait


def bisect(fn, lo, hi, it=60):
    flo = fn(lo)
    for _ in range(it):
        mid = (lo + hi) / 2
        if (fn(mid) > 0) == (flo > 0):
            lo, flo = mid, fn(mid)
        else:
            hi = mid
    return lo, hi


def cap_check():
    head("1. Cap lemma: max likelihood ratio over histories and random strategies (two slots)")
    rnd = random.Random(20261023)
    for menu, lam, beta in (("two", F(6, 17), F(1, 3)), ("buy", F(9, 22), F(1, 5))):
        m = Model(R1, lam, beta, menu)
        cap = 1 + m.u()
        worst = F(0)
        for _ in range(4000):
            st = {"x": {"H": F(rnd.randint(0, 20), 20), "L": F(rnd.randint(0, 20), 20) if menu == "two" else F(0)},
                  "y": {"H": {q: F(rnd.randint(0, 20), 20) for q in Q},
                        "L": {q: (F(rnd.randint(0, 20), 20) if menu == "two" else F(0)) for q in Q}}}
            for h in [(a,) for a in Q] + [(a, b) for a in Q for b in Q]:
                ph, pl = m.hist_prob("H", h, st), m.hist_prob("L", h, st)
                if pl > 0 and ph > 0:
                    worst = max(worst, ph / pl, pl / ph)
        print(f"  menu {menu}: lam = {lam}, beta = {beta}, 1 + u = {cap} (~{dec(cap, 6)}), "
              f"max ratio found = {worst} (~{dec(worst, 6)}); M = {cap / (1 + cap)} (~{dec(cap / (1 + cap), 6)})")


def slot2_solve(m, st, j):
    """Given x and the other class's y, set y_j(q1) at each node by its own optimality (1-D)."""
    for (q1,) in [(q,) for q in Q]:
        if m.eta[q1] == 0:
            continue

        def ret(y):
            st2 = {"x": dict(st["x"]), "y": {c: dict(st["y"][c]) for c in st["y"]}}
            st2["y"][j][q1] = y
            sol = m.solve(st2)
            return m.values(sol, j)[1][q1]

        r0, r1 = ret(F(0)), ret(F(1))
        if r1 >= 0:
            st["y"][j][q1] = F(1)
        elif r0 <= 0:
            st["y"][j][q1] = F(0)
        else:
            lo, hi = bisect(ret, F(0), F(1), 50)
            st["y"][j][q1] = (lo + hi) / 2
    return st


def timing_equilibrium(m, mover, fixed_x_other=None, label=""):
    """Outer 1-D search on x_mover; inner 1-D optimality of y at slot-2 nodes for the mover.
    The other class plays x = fixed_x_other with y chosen optimally off path (buy-only: L passive)."""
    other = "L" if mover == "H" else "H"

    def build(x):
        st = {"x": {mover: x, other: fixed_x_other if fixed_x_other is not None else F(0)},
              "y": {"H": {q: F(1) for q in Q}, "L": {q: (F(1) if m.menu == "two" else F(0)) for q in Q}}}
        if m.menu == "buy":
            st["x"]["L"] = F(0)
            st["y"]["L"] = {q: F(0) for q in Q}
        for _ in range(3):
            st = slot2_solve(m, st, mover)
        return st

    def gap(x):
        st = build(x)
        sol = m.solve(st)
        now, later, wait = m.values(sol, mover)
        return now - wait, st, sol

    g0, _, _ = gap(F(0))
    g1, st1, sol1 = gap(F(1))
    print(f"  {label}: gap(now - wait) at x_{mover} = 0: {dec(g0, 6)}; at x_{mover} = 1: {dec(g1, 6)}")
    if g1 >= 0:
        return F(1), st1, sol1
    if g0 <= 0:
        st0 = build(F(0))
        return F(0), st0, m.solve(st0)
    lo, hi = bisect(lambda x: gap(x)[0], F(0), F(1), 40)
    x = (lo + hi) / 2
    st = build(x)
    print(f"    interior x_{mover} in [{dec(lo, 10)}, {dec(hi, 10)}]")
    return x, st, m.solve(st)


def report(m, st, sol, who=("H", "L")):
    print(f"    strategies: x = {{H: {dec(st['x']['H'], 6)}, L: {dec(st['x']['L'], 6)}}}, "
          f"y_H = {[dec(st['y']['H'][q], 4) for q in Q]}, y_L = {[dec(st['y']['L'][q], 4) for q in Q]}")
    mus = {h: dec(v, 4) for h, v in sol["mu"].items() if v is not None}
    print(f"    posteriors: {mus}")
    print(f"    entry = {dec(sol['entry'], 6)}; max posterior = {dec(max(v for v in sol['mu'].values() if v is not None), 6)}")
    for j in who:
        if m.menu == "buy" and j == "L":
            continue
        now, later, wait = m.values(sol, j)
        print(f"    class {j}: trade now {dec(now, 6)}, trade at slot 2 after q1 = "
              f"{ {q: dec(v, 6) for q, v in later.items()} }, wait value {dec(wait, 6)}")


def immediate(m):
    st = {"x": {"H": F(1), "L": F(1) if m.menu == "two" else F(0)},
          "y": {"H": {q: F(1) for q in Q}, "L": {q: (F(1) if m.menu == "two" else F(0)) for q in Q}}}
    return st, m.solve(st)


def main():
    cap_check()

    head("2. Buy-only menu (beta = 1/5, lam = 9/22, so 1 + u = 29/11 and M = 29/40)")
    for r, access in ((R1, True), (R1, False), (R2, True)):
        m = Model(r, F(9, 22), F(1, 5), "buy", access)
        print(f"  r = {r}, price access = {access}")
        st, sol = immediate(m)
        print("   immediate profile (H trades at slot 1):")
        report(m, st, sol)
        x, st, sol = timing_equilibrium(m, "H", label="   equilibrium search over x_H")
        print(f"   equilibrium: x_H = {dec(x, 8)}")
        report(m, st, sol)

    head("3. Two-sided menu (beta = 1/3, lam = 6/17, so 1 + u = 29/11 and M = 29/40)")
    for r, access in ((R1, True), (R2, True), (R1, False)):
        m = Model(r, F(6, 17), F(1, 3), "two", access)
        print(f"  r = {r}, price access = {access}")
        st, sol = immediate(m)
        print("   immediate profile (both classes trade at slot 1):")
        report(m, st, sol)
        print("   class H trades at slot 1; search over class L's timing:")
        x, st, sol = timing_equilibrium(m, "L", fixed_x_other=F(1), label="   L search")
        print(f"   candidate: x_L = {dec(x, 8)}")
        report(m, st, sol)
        nowH, laterH, waitH = m.values(sol, "H")
        print(f"   check class H at this candidate: now - wait = {dec(nowH - waitH, 6)} "
              f"({'H immediate is optimal' if nowH >= waitH else 'H prefers to wait: not an equilibrium'})")


def gap_scan(m, mover, fixed_x_other, grid=50):
    """All sign changes of now - wait for the mover on a grid of x (other class fixed)."""
    other = "L" if mover == "H" else "H"

    def gap(x):
        st = {"x": {mover: x, other: fixed_x_other},
              "y": {"H": {q: F(1) for q in Q}, "L": {q: (F(1) if m.menu == "two" else F(0)) for q in Q}}}
        if m.menu == "buy":
            st["x"]["L"], st["y"]["L"] = F(0), {q: F(0) for q in Q}
        st = slot2_solve(m, st, mover)
        sol = m.solve(st)
        now, _, wait = m.values(sol, mover)
        return now - wait, st, sol

    xs = [F(i, grid) for i in range(grid + 1)]
    gs = [gap(x)[0] for x in xs]
    eqs = []
    if gs[0] <= 0:
        eqs.append(F(0))
    for i in range(grid):
        if (gs[i] > 0) != (gs[i + 1] > 0):
            lo, hi = bisect(lambda x: gap(x)[0], xs[i], xs[i + 1], 40)
            eqs.append((lo + hi) / 2)
    if gs[-1] >= 0:
        eqs.append(F(1))
    out = []
    for x in eqs:
        g, st, sol = gap(x)
        out.append((x, g, st, sol))
    return out


def symmetric_timing(m):
    """Both classes use the same first-date rate x; slot-2 trades are strictly profitable (y = 1)."""
    def build(x):
        return {"x": {"H": x, "L": x}, "y": {"H": {q: F(1) for q in Q}, "L": {q: F(1) for q in Q}}}

    def gap(x):
        sol = m.solve(build(x))
        now, _, wait = m.values(sol, "H")
        return now - wait

    g0, g1 = gap(F(0)), gap(F(1))
    print(f"   symmetric search: gap at x = 0: {dec(g0, 6)}; at x = 1: {dec(g1, 6)}")
    if g0 > 0 > g1:
        lo, hi = bisect(gap, F(0), F(1), 40)
        x = (lo + hi) / 2
        print(f"   interior x_H = x_L in [{dec(lo, 10)}, {dec(hi, 10)}]")
        st = build(x)
        return x, st, m.solve(st)
    return None, None, None


def welfare_gain(m, sol):
    """Prop. A.9 analog: access equilibrium against any hidden-price equilibrium (entry rho there)."""
    o = m.o
    dR, dW = F(0), F(0)
    for h in sol["hs2"]:
        if sol["mu"][h] is None:
            continue
        p = (sol["pr"][h][0] + sol["pr"][h][1]) / 2
        de = sol["e"][h] - RHO
        dR += p * de * (o["wL"] + o["D"] * sol["mu"][h])
        dW += p * de * (o["gL"] + sol["mu"][h] * (o["gH"] - o["gL"]) - 6 + F(1, 4) / o["r"])
    return dR, dW


def extra():
    head("4. Buy-only, r = 3, price access: every first-date rate x_H that is an equilibrium (grid 1/50 + bisection)")
    m = Model(R1, F(9, 22), F(1, 5), "buy", True)
    for x, g, st, sol in gap_scan(m, "H", F(0)):
        print(f"  x_H = {dec(x, 10)}: gap = {dec(g, 8)}; entry = {dec(sol['entry'], 6)}; "
              f"max posterior = {dec(max(v for v in sol['mu'].values() if v is not None), 6)}")
        report(m, st, sol, who=("H",))

    head("5. Two-sided, r = 3.6 (access) and r = 3 (hidden): symmetric mixed timing")
    for r, access in ((R2, True), (R1, False)):
        m = Model(r, F(6, 17), F(1, 3), "two", access)
        print(f"  r = {r}, price access = {access}")
        for j in ("H", "L"):
            oo = m.o
            print(f"   slot-2 trade margin rho Delta (1 - M) - k = {dec(RHO * oo['D'] * (1 - F(29, 40)) - K, 6)} (> 0: y = 1)")
            break
        x, st, sol = symmetric_timing(m)
        if x is not None:
            report(m, st, sol)

    head("6. Two-sided, access: class H at slot 1, class L delays; r = 3 and the middle strengths")
    for r in (R1, F(31, 20), F(8, 5), F(33, 20)):
        m = Model(r, F(6, 17), F(1, 3), "two", True)
        print(f"  r = {r}: no trade is an equilibrium iff rho Delta/2 <= k: {RHO * m.o['D'] / 2 <= K}")
        res = gap_scan(m, "L", F(1))
        for x, g, st, sol in res:
            nowH, _, waitH = m.values(sol, "H")
            print(f"   x_L = {dec(x, 10)}: L gap = {dec(g, 8)}; entry = {dec(sol['entry'], 8)}; "
                  f"H now - wait = {dec(nowH - waitH, 6)} -> {'equilibrium' if nowH >= waitH else 'not an equilibrium'}")
            if r == R1 and nowH >= waitH:
                dR, dW = welfare_gain(m, sol)
                print(f"     Prop. A.9 analog: proceeds rise by {dec(dR, 6)}, net surplus by {dec(dW, 6)}"
                      f" (trading cost lam k in both regimes)")
                report(m, st, sol)


def jump_equilibrium():
    head("7. Buy-only, r = 3: the challenger-mixing equilibrium at the entry jump of history (+,0)")
    lam, beta = F(9, 22), F(1, 5)
    m = Model(R1, lam, beta, "buy", True)
    T1 = m.o["tau"] / (1 - m.o["tau"])
    xs = beta * (T1 - 1 + lam) / lam
    print(f"  likelihood ratio of (+,0) = 1 - lam + lam x / beta equals T1 = {T1} at x* = {xs} (~{dec(xs, 10)})")
    st = {"x": {"H": xs, "L": F(0)}, "y": {"H": {q: F(1) for q in Q}, "L": {q: F(0) for q in Q}}}

    def gap(z):
        sol = m.solve(st, zeta={(1, 0): z})
        now, later, wait = m.values(sol, "H")
        return now - wait

    g0, g1 = gap(F(0)), gap(F(1))
    print(f"  H gap with zeta(+,0) = 0: {dec(g0, 8)}; with zeta(+,0) = 1: {dec(g1, 8)}")
    if g0 < 0 < g1:
        lo, hi = bisect(gap, F(0), F(1), 50)
        z = (lo + hi) / 2
        sol = m.solve(st, zeta={(1, 0): z})
        print(f"  zeta* in [{dec(lo, 10)}, {dec(hi, 10)}]; entry = {dec(sol['entry'], 8)}")
        report(m, st, sol, who=("H",))
        for q1 in (1, 0):
            stt = {"x": dict(st["x"]), "y": {c: dict(st["y"][c]) for c in st["y"]}}
            print(f"   slot-2 return after q1 = {q1}: {dec(m.values(sol, 'H')[1][q1], 6)} (> 0, so y = 1 is optimal)")


if __name__ == "__main__":
    main()
    extra()
    jump_equilibrium()
