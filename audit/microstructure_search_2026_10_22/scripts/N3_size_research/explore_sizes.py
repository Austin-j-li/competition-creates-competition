"""Print-only float exploration of the size menu in the V3 slot.

Run from the repository root:
  .venv/bin/python audit/microstructure_search_2026_10_22/scripts/N3_size_research/explore_sizes.py
No assertions. Results are diagnostics; exact work is in exact_sizes.py.
"""
from fractions import Fraction as F

K = 0.02
RHO = 0.25


def auction(r):
    delta = (r - 1.0) ** 2 / (2.0 * r)
    g_l = 3.0 / (8.0 * r)
    g_h = 10.0 - r / 2.0 - 1.0 / (8.0 * r)
    tau = (6.0 - g_l) / (g_h - g_l)
    return delta, tau


def h_candidates(r, lam, b1, b2):
    delta, tau = auction(r)
    b = {1: b1, 2: b2}
    out = []

    def mu(s, a):
        return (b[s] + a) / (2 * b[s] + a)

    def ee(s, a):
        return 1.0 if mu(s, a) >= tau - 1e-12 else RHO

    def u(s, a):
        return s * (ee(s, a) * delta * b[s] / (2 * b[s] + a) - K)

    if u(1, 0.0) <= 1e-9 and u(2, 0.0) <= 1e-9:
        out.append(("H0", (0.0, 0.0)))
    for s in (1, 2):
        o = 3 - s
        if u(s, lam) >= u(o, 0.0) - 1e-9 and u(s, lam) >= -1e-9:
            a = (lam, 0.0) if s == 1 else (0.0, lam)
            out.append((f"Hconc{s}", a))
    for s in (1, 2):
        o = 3 - s
        for e in (RHO, 1.0):
            a = b[s] * (e * delta / K - 2.0)
            if 0.0 < a < lam:
                m = mu(s, a)
                ok = (m >= tau - 1e-9) if e == 1.0 else (m < tau + 1e-9)
                if ok and u(o, 0.0) <= 1e-9:
                    av = (a, 0.0) if s == 1 else (0.0, a)
                    out.append((f"Hpart{s}e{e}", av))
    # full mix over sizes, by common total payoff T
    for e1 in (RHO, 1.0):
        for e2 in (RHO, 1.0):
            es = {1: e1, 2: e2}

            def alloc(t):
                return tuple(b[s] * (es[s] * delta / (t / s + K) - 2.0) for s in (1, 2))

            tmax = min(s * (es[s] * delta / 2.0 - K) for s in (1, 2))
            if tmax <= 0:
                continue
            lo, hi = 0.0, tmax * (1 - 1e-10)
            slo = sum(alloc(lo))
            shi = sum(alloc(hi))
            if not (slo > lam > shi):
                continue
            for _ in range(200):
                mid = (lo + hi) / 2
                if sum(alloc(mid)) > lam:
                    lo = mid
                else:
                    hi = mid
            a = alloc((lo + hi) / 2)
            if min(a) <= 1e-10:
                continue
            ok = True
            for i, s in enumerate((1, 2)):
                m = mu(s, a[i])
                if es[s] == 1.0 and m < tau - 1e-7:
                    ok = False
                if es[s] == RHO and m >= tau + 1e-7:
                    ok = False
            if ok:
                out.append((f"Hmix e=({e1},{e2}) T={(lo+hi)/2:.6f}", a))
    # both sizes with abstention, T = 0
    for e1 in (RHO, 1.0):
        for e2 in (RHO, 1.0):
            es = {1: e1, 2: e2}
            a = tuple(b[s] * (es[s] * delta / K - 2.0) for s in (1, 2))
            if min(a) > 0 and sum(a) < lam - 1e-9:
                ok = True
                for i, s in enumerate((1, 2)):
                    m = mu(s, a[i])
                    if es[s] == 1.0 and m < tau - 1e-7:
                        ok = False
                    if es[s] == RHO and m >= tau + 1e-7:
                        ok = False
                if ok:
                    out.append((f"Hmix0 e=({e1},{e2})", a))
    # de-duplicate near-identical allocations
    uniq = []
    for name, a in out:
        if not any(abs(a[0] - x[1][0]) < 1e-6 and abs(a[1] - x[1][1]) < 1e-6 for x in uniq):
            uniq.append((name, a))
    return uniq


def l_candidates(r, lam, b1, b2):
    delta, tau = auction(r)
    b = {1: b1, 2: b2}
    out = []

    def v(s, x):
        return s * (RHO * delta * b[s] / (2 * b[s] + x) - K)

    if v(1, 0.0) <= 1e-9 and v(2, 0.0) <= 1e-9:
        out.append(("L0", (0.0, 0.0)))
    for s in (1, 2):
        o = 3 - s
        if v(s, lam) >= v(o, 0.0) - 1e-9 and v(s, lam) >= -1e-9:
            a = (lam, 0.0) if s == 1 else (0.0, lam)
            out.append((f"Lconc{s}", a))
    for s in (1, 2):
        o = 3 - s
        a = b[s] * (RHO * delta / K - 2.0)
        if 0.0 < a < lam and v(o, 0.0) <= 1e-9:
            av = (a, 0.0) if s == 1 else (0.0, a)
            out.append((f"Lpart{s}", av))

    def alloc(t):
        return tuple(b[s] * (RHO * delta / (t / s + K) - 2.0) for s in (1, 2))

    tmax = min(s * (RHO * delta / 2.0 - K) for s in (1, 2))
    if tmax > 0:
        lo, hi = 0.0, tmax * (1 - 1e-10)
        if sum(alloc(lo)) > lam > sum(alloc(hi)):
            for _ in range(200):
                mid = (lo + hi) / 2
                if sum(alloc(mid)) > lam:
                    lo = mid
                else:
                    hi = mid
            a = alloc((lo + hi) / 2)
            if min(a) > 1e-10:
                out.append((f"Lmix T={(lo+hi)/2:.6f}", a))
    a = tuple(b[s] * (RHO * delta / K - 2.0) for s in (1, 2))
    if min(a) > 0 and sum(a) < lam - 1e-9:
        out.append(("Lmix0", a))
    uniq = []
    for name, a in out:
        if not any(abs(a[0] - x[1][0]) < 1e-6 and abs(a[1] - x[1][1]) < 1e-6 for x in uniq):
            uniq.append((name, a))
    return uniq


def report(label, lam, beta1, beta2):
    eta0 = 1 - 2 * (beta1 + beta2)
    b1, b2 = (1 - lam) * beta1, (1 - lam) * beta2
    print(f"\n=== {label}: lam={lam:.6f} beta1={beta1:.6f} beta2={beta2:.6f} eta0={eta0:.6f} b1={b1:.6f} b2={b2:.6f}")
    for s, bb in ((1, b1), (2, b2)):
        print(f"  size{s}: u={lam/bb:.4f} Mfull={(bb+lam)/(2*bb+lam):.6f}")
    for r in (1.2, 1.55, 1.60, 1.65, 3.0, 3.6):
        delta, tau = auction(r)
        hs = h_candidates(r, lam, b1, b2)
        ls = l_candidates(r, lam, b1, b2)
        print(f" r={r}: Delta={delta:.6f} tau={tau:.6f} rhoD/2-k={RHO*delta/2-K:+.6f}")
        for hn, A in hs:
            for ln, S in ls:
                # entry
                rec = 0.0
                mus = []
                for i, s in enumerate((1, 2)):
                    bb = (b1, b2)[i]
                    m = (bb + A[i]) / (2 * bb + A[i])
                    mus.append(m)
                    if m >= tau:
                        rec += bb + A[i] / 2
                ah0 = (1 - lam) * eta0 + lam - A[0] - A[1]
                al0 = (1 - lam) * eta0 + lam - S[0] - S[1]
                mu0 = ah0 / (ah0 + al0) if ah0 + al0 > 0 else 0.5
                p0 = (ah0 + al0) / 2
                if mu0 >= tau:
                    rec += p0
                entry = RHO + 0.75 * rec
                print(f"   {hn} A={A} | {ln} S={S} | mu+={mus} mu0={mu0:.4f} E={entry:.6f}")


def main():
    lam = 6 / 17
    # Set A: size 1 common (calibration A), size 2 rare
    report("A common1 rare2", lam, 1 / 3, 1 / 20)
    # Set B: size 1 rare, size 2 common with M2 = 12/17
    report("B rare1 common2", lam, 1 / 20, 30 / 77)
    # Set C: both sizes in the strip, size 2 near the top
    # u1 = 1.45, u2 = 1.70 at lam=6/17 -> beta_s = lam/(u_s*(1-lam))
    b_1 = lam / 1.45
    b_2 = lam / 1.70
    report("C both in strip", lam, b_1 / (1 - lam), b_2 / (1 - lam))


if __name__ == "__main__":
    main()
