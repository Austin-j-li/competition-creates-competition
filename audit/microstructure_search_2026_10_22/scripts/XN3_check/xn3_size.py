#!/usr/bin/env python3
"""Independent exact check of N3, Extension A (order size choice), selected claims only.

Menu {-2,-1,0,1,2}, cost k|q|, informed probability lam = 1/5, liquidity law
eta(+-1) = 1/20, eta(+-2) = 5/28, eta(0) = 19/35. Rule C1 for the challenger.
Every candidate is verified by the payoff of every order for each class.
Irrational roots are enclosed by exact rational bisection; every comparison is printed at both ends.
The program prints results only.
"""
from fractions import Fraction as Fr

RHO, K, LAM = Fr(1, 4), Fr(1, 50), Fr(1, 5)
ETA = {-2: Fr(5, 28), -1: Fr(1, 20), 0: Fr(19, 35), 1: Fr(1, 20), 2: Fr(5, 28)}
ORDERS = (-2, -1, 0, 1, 2)


def delta(r):
    return (r - 1) ** 2 / (2 * r)


def tau(r):
    return (48 * r - 3) / (4 * (20 * r - r * r - 1))


def dec(x, n=12):
    return f"{float(x):.{n}f}"


def evaluate(r, sH, sL, e_override=None):
    """Posteriors, entry (C1) and every order payoff for given class strategies."""
    Dl, t = delta(r), tau(r)
    fH = {q: (1 - LAM) * ETA[q] + LAM * sH.get(q, Fr(0)) for q in ORDERS}
    fL = {q: (1 - LAM) * ETA[q] + LAM * sL.get(q, Fr(0)) for q in ORDERS}
    mu = {q: fH[q] / (fH[q] + fL[q]) for q in ORDERS}
    e = {q: (Fr(1) if mu[q] >= t else RHO) for q in ORDERS}
    if e_override:
        e.update(e_override)
    UH = {q: q * e[q] * Dl * (1 - mu[q]) - K * abs(q) for q in ORDERS}
    UL = {q: -q * e[q] * Dl * mu[q] - K * abs(q) for q in ORDERS}
    E = sum((fH[q] + fL[q]) / 2 * e[q] for q in ORDERS)
    return dict(mu=mu, e=e, UH=UH, UL=UL, E=E)


def check(name, r, sH, sL):
    ev = evaluate(r, sH, sL)
    supH = [q for q in ORDERS if sH.get(q, 0) > 0]
    supL = [q for q in ORDERS if sL.get(q, 0) > 0]
    mH, mL = max(ev["UH"].values()), max(ev["UL"].values())
    gapH = min([ev["UH"][q] for q in supH]) - mH
    gapL = min([ev["UL"][q] for q in supL]) - mL
    unusedH = max([ev["UH"][q] for q in ORDERS if q not in supH], default=None)
    unusedL = max([ev["UL"][q] for q in ORDERS if q not in supL], default=None)
    print(f"  {name}: r={r}, tau={dec(tau(r))}")
    print("    mu  :", " ".join(f"{q:+d}:{dec(ev['mu'][q], 9)}" for q in ORDERS))
    print("    e   :", " ".join(f"{q:+d}:{dec(ev['e'][q], 4)}" for q in ORDERS))
    print("    U_H :", " ".join(f"{q:+d}:{dec(ev['UH'][q], 9)}" for q in ORDERS))
    print("    U_L :", " ".join(f"{q:+d}:{dec(ev['UL'][q], 9)}" for q in ORDERS))
    print(f"    support H {supH}, support L {supL}; support minus best: H {dec(gapH, 15)}, L {dec(gapL, 15)}; "
          f"best unused: H {dec(unusedH, 9) if unusedH is not None else '-'}, L {dec(unusedL, 9) if unusedL is not None else '-'}")
    print(f"    aggregate entry E = {ev['E']} = {dec(ev['E'])}")
    return ev


def bisect(f, lo, hi, width=Fr(1, 10 ** 16)):
    flo = f(lo)
    while hi - lo > width:
        m = (lo + hi) / 2
        if (f(m) > 0) == (flo > 0):
            lo, flo = m, f(m)
        else:
            hi = m
    return lo, hi


def main():
    b1, b2 = (1 - LAM) * ETA[1], (1 - LAM) * ETA[2]
    print(f"Extension A check: lam={LAM}, b1={b1}, b2={b2}, sum of eta={sum(ETA.values())}")
    print()
    print("== A1. Middle strengths: H mixes between +1 and 0 (C1) ==")
    ents = []
    for r in (Fr(31, 20), Fr(8, 5), Fr(33, 20)):
        Dl = delta(r)
        A1 = b1 * (Dl / K - 2)
        s = A1 / LAM
        print(f"  r={r}: A1={A1}, sigma_H(+1)={s} = {dec(s)}, mu(+1) should be 1-k/Delta={1 - K / Dl}")
        ev = check("rising branch", r, {1: s, 0: 1 - s}, {0: Fr(1)})
        print(f"    1/4 + 3*Delta/4 = {Fr(1, 4) + 3 * Dl / 4}")
        ents.append(ev["E"])
        check("no informed trade", r, {0: Fr(1)}, {0: Fr(1)})
    print(f"  strict rise of the branch: {ents[0] < ents[1] < ents[2]}")
    print()

    print("== A2. r=3: H buys two; L mixes between -1 and -2 ==")
    r = Fr(3)
    Dl = delta(r)

    def g7(x):
        return (RHO * Dl * b1 / (2 * b1 + x) - K) - 2 * (RHO * Dl * b2 / (2 * b2 + LAM - x) - K)

    print(f"  eq. (7) difference at 0: {g7(Fr(0))}, at 1/5: {g7(LAM)}")
    lo, hi = bisect(g7, Fr(0), LAM)
    for x in (lo, hi):
        check(f"x={dec(x, 15)}", r, {2: Fr(1)}, {-1: x / LAM, -2: 1 - x / LAM})
    print()

    print("== A3. r=3.6: strict +-2 floor equilibrium ==")
    r = Fr(18, 5)
    check("floor", r, {2: Fr(1)}, {-2: Fr(1)})
    print()
    print("== A4. Second equilibria: H mixes +1 (recruits) and +2 (does not); L sells two ==")
    for r in (Fr(3), Fr(18, 5)):
        Dl = delta(r)

        def g8(x):
            return (Dl * b1 / (2 * b1 + x) - K) - 2 * (RHO * Dl * b2 / (2 * b2 + LAM - x) - K)

        print(f"  r={r}: eq. (8) difference at 0: {dec(g8(Fr(0)))}, at 1/5: {dec(g8(LAM))}")
        lo, hi = bisect(g8, Fr(0), LAM)
        for x in (lo, hi):
            check(f"x={dec(x, 15)}", r, {1: x / LAM, 2: 1 - x / LAM}, {-2: Fr(1)})
        print()
        if r == 3:
            print("  r=3 again: H mixes as in eq. (8); L mixes between -1 and -2 as in eq. (7)")

            def g7(y):
                return (RHO * Dl * b1 / (2 * b1 + y) - K) - 2 * (RHO * Dl * b2 / (2 * b2 + LAM - y) - K)

            ylo, yhi = bisect(g7, Fr(0), LAM)
            for x, y in ((lo, ylo), (hi, yhi)):
                check(f"x={dec(x, 15)}, y={dec(y, 15)}", r, {1: x / LAM, 2: 1 - x / LAM},
                      {-1: y / LAM, -2: 1 - y / LAM})
            print()


if __name__ == "__main__":
    main()
