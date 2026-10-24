"""Independent exact check of the one-slot liquidity model (T2 variants V3 buy and V3 two).

One public order slot. With probability lam the informed investor fills it and sees the class.
Otherwise a liquidity trader of the same unit size fills it:
  buy-only: buys with probability beta, else abstains;
  two-sided: sells, abstains, buys with probabilities (beta, 1 - 2 beta, beta).
No separate noise. Competitive price. The challenger sees the price.

Print-only. Every economic comparison uses fractions.Fraction; decimals are for display.
Run from the repository root:
  .venv/bin/python audit/microstructure_search_2026_10_22/scripts/X_check/v3_check.py
"""
from fractions import Fraction as F
from math import isqrt
import itertools

import mpmath

H, L, P, RHO, CL, CH, K, PI = F(10), F(1), F(1, 2), F(1, 4), F(0), F(6), F(1, 50), F(1, 2)
R0, R1, R2 = F(6, 5), F(3), F(18, 5)
BETA, LAM = F(1, 3), F(6, 17)


def dec(x, n=10):
    return f"{float(x):.{n}f}"


def show(name, x, n=10):
    print(f"  {name} = {x}  (~{dec(x, n)})")


def head(text):
    print()
    print("=" * 100)
    print(text)
    print("=" * 100)


# ----------------------------------------------------------------------------------------------
# Auction objects by direct integration over R ~ U[0, r] (not from the paper's closed forms)
# ----------------------------------------------------------------------------------------------
def expect(pieces, r):
    """E[f(R)] for R ~ U[0, r]; f(R) = a + b R on [lo, hi); hi = None means no upper limit."""
    tot = F(0)
    for lo, hi, a, b in pieces:
        lo2 = max(lo, F(0))
        hi2 = r if hi is None else min(hi, r)
        if hi2 > lo2:
            tot += a * (hi2 - lo2) + b * (hi2 * hi2 - lo2 * lo2) / 2
    return tot / r


def objects(r):
    r = F(r)
    t0 = expect([(P, None, P, F(0))], r)  # incumbent alone buys at p when R >= p

    def t(th):  # second-price proceeds with a prepared challenger th >= p: max(p, min(R, th))
        return expect([(F(0), P, P, F(0)), (P, th, F(0), F(1)), (th, None, th, F(0))], r)

    def g(th):  # challenger keeps (th - max(p, R))_+
        return expect([(F(0), P, th - P, F(0)), (P, th, th, F(-1))], r)

    def s(th):  # allocation value max(th, R) when th >= p
        return expect([(F(0), th, th, F(0)), (th, None, F(0), F(1))], r)

    s0 = expect([(P, None, F(0), F(1))], r)  # allocation value R 1{R >= p} without the challenger
    o = dict(r=r, t0=t0, tH=t(H), tL=t(L), gH=g(H), gL=g(L), sH=s(H), sL=s(L), s0=s0)
    o["D"] = o["tH"] - o["tL"]
    return o


def closed(r):
    r = F(r)
    return dict(t0=P * (1 - P / r), tH=r / 2 + P * P / (2 * r), tL=L - (L * L - P * P) / (2 * r),
                gH=H - r / 2 - P * P / (2 * r), gL=(L * L - P * P) / (2 * r), D=(r - L) ** 2 / (2 * r))


def Bf(o, mu):
    return o["gL"] + mu * (o["gH"] - o["gL"])


def tau(o):
    return (CH - o["gL"]) / (o["gH"] - o["gL"])


def entry_C1(o, mu):
    # c_L = 0 type always prepares (gross profit >= 0); c_H type prepares iff B >= c_H (tie: prepare)
    return RHO + (1 - RHO) * (1 if Bf(o, mu) >= CH else 0)


# ----------------------------------------------------------------------------------------------
# The one-slot flow model
# ----------------------------------------------------------------------------------------------
def menu(variant):
    return [0, 1] if variant == "buy" else [-1, 0, 1]


def liq(variant, beta):
    return {0: 1 - beta, 1: beta} if variant == "buy" else {-1: beta, 0: 1 - 2 * beta, 1: beta}


def masses(variant, beta, lam, sig):
    eta = liq(variant, beta)
    return {x: (1 - lam) * eta[x] + lam * sig.get(x, F(0)) for x in menu(variant)}


def evaluate(variant, beta, lam, o, sH, sL, ent=None):
    """All objects of a candidate profile. ent overrides the C1 entry schedule (for CM ties)."""
    aH = masses(variant, beta, lam, sH)
    aL = masses(variant, beta, lam, sL)
    xs = menu(variant)
    mu = {x: PI * aH[x] / (PI * aH[x] + (1 - PI) * aL[x]) for x in xs}
    e = {x: entry_C1(o, mu[x]) for x in xs}
    if ent:
        e.update(ent)
    price = {x: o["t0"] + e[x] * (o["tL"] - o["t0"] + o["D"] * mu[x]) for x in xs}
    val = {j: {x: o["t0"] + e[x] * (o["t" + j] - o["t0"]) for x in xs} for j in "HL"}
    # informed payoff conditional on filling the slot: the flow equals its own order q
    pay = {j: {q: q * (val[j][q] - price[q]) - K * abs(q) for q in xs} for j in "HL"}
    # uninformed filler with only the trading payoff: class is independent of its order
    vU = {x: o["t0"] + e[x] * (o["tL"] - o["t0"] + o["D"] * PI) for x in xs}
    payU = {q: q * (vU[q] - price[q]) - K * abs(q) for q in xs}
    prob = {x: PI * aH[x] + (1 - PI) * aL[x] for x in xs}
    E = sum(prob[x] * e[x] for x in xs)
    eH = sum(aH[x] * e[x] for x in xs)
    OH = PI * eH  # h > r, so a prepared class-H challenger always wins
    return dict(aH=aH, aL=aL, mu=mu, e=e, price=price, pay=pay, payU=payU, prob=prob, E=E, eH=eH, OH=OH)


def best_response_ok(pay, sig, inv):
    mx = max(pay.values())
    arg = {q for q, v in pay.items() if v == mx}
    supp = {q for q, w in sig.items() if w > 0}
    if not supp <= arg:
        return False
    if inv == "I0" and 0 in arg and supp != {0}:
        return False
    return True


# ----------------------------------------------------------------------------------------------
# Classification of all equilibria of V3 (own derivation; see the memo)
#   H purchase return: e_+ * D * b / (2b + s), with s = lam * P(q = 1 | H), b = (1 - lam) beta.
#   L sale return (two-sided): rho * D * b / (2b + t), with t = lam * P(q = -1 | L).
#   Each return falls strictly in its own rate on each entry piece, so indifference has
#   at most one solution per piece; the candidates below are exhaustive.
# ----------------------------------------------------------------------------------------------
def H_candidates(o, b, lam, chall, inv):
    D, tt = o["D"], tau(o)

    def mup(s):
        return (b + s) / (2 * b + s)

    def ret(s, e):
        return e * D * b / (2 * b + s)

    sstar = b * (2 * tt - 1) / (1 - tt)  # mu_+(s) >= tau iff s >= sstar
    out = []
    # no informed purchase: mu_+ = 1/2 < tau, entry rho
    if ret(F(0), RHO) <= K:
        out.append(("s=0", F(0), RHO))
    # full purchase
    m = mup(lam)
    if m != tt:
        e = F(1) if m > tt else RHO
        if (ret(lam, e) >= K) if inv == "IM" else (ret(lam, e) > K):
            out.append(("s=lam (full)", lam, e))
    else:
        out.append(("s=lam with challenger tie: inspect", lam, None))
    if inv == "IM":
        for e_piece in (RHO, F(1)):
            s = b * (e_piece * D / K - 2)
            if 0 < s < lam and s != sstar:
                e = F(1) if mup(s) > tt else RHO
                if e == e_piece:
                    out.append((f"interior s, entry piece {e_piece}", s, e))
        if 0 < sstar < lam:
            estar = K * (2 * b + sstar) / (D * b)
            ok = (estar == 1) if chall == "C1" else (RHO <= estar <= 1)
            if ok:
                out.append(("threshold s=s*, challenger mixes", sstar, estar))
    return out, sstar


def L_candidates(o, b, lam, inv):
    D = o["D"]

    def ret(t):
        return RHO * D * b / (2 * b + t)

    out = []
    if ret(F(0)) <= K:
        out.append(("t=0", F(0)))
    if (ret(lam) >= K) if inv == "IM" else (ret(lam) > K):
        out.append(("t=lam (full)", lam))
    if inv == "IM":
        t = b * (RHO * D / K - 2)
        if 0 < t < lam:
            out.append(("interior t", t))
    return out


def solve_V3(variant, beta, lam, r, chall="C1", inv="IM", verbose=True):
    o = objects(r)
    b = (1 - lam) * beta
    Hc, sstar = H_candidates(o, b, lam, chall, inv)
    Lc = L_candidates(o, b, lam, inv) if variant == "two" else [("t=0 (buy-only menu)", F(0))]
    eqs = []
    for (hl, s, eplus), (ll, t) in itertools.product(Hc, Lc):
        if eplus is None:
            continue
        sH = {1: s / lam, 0: 1 - s / lam}
        sL = {-1: t / lam, 0: 1 - t / lam} if variant == "two" else {0: F(1)}
        ent = {1: eplus}
        ev = evaluate(variant, beta, lam, o, sH, sL, ent)
        # zero-flow tie under CM would need its own mixture; report it if it arises
        tie0 = variant == "two" and Bf(o, ev["mu"][0]) == CH
        okH = best_response_ok(ev["pay"]["H"], sH, inv)
        okL = best_response_ok(ev["pay"]["L"], sL, inv)
        # the entry value at flow 1 must be a best reply of the challenger
        Bp = Bf(o, ev["mu"][1])
        if Bp > CH:
            okC = eplus == 1
        elif Bp < CH:
            okC = eplus == RHO
        else:
            okC = (eplus == 1) if chall == "C1" else (RHO <= eplus <= 1)
        eqs.append(dict(hl=hl, ll=ll, s=s, t=t, ev=ev, ok=(okH and okL and okC), tie0=tie0))
    if verbose:
        print(f"  [{variant}, r={r} (~{dec(r, 7)}), challenger {chall}, investor {inv}] "
              f"tau={dec(tau(o), 8)}, s*={dec(sstar, 8)}, lam={dec(lam, 6)}")
        for q in eqs:
            ev = q["ev"]
            mus = ", ".join(f"mu({x})={ev['mu'][x]} ~{dec(ev['mu'][x], 6)}" for x in sorted(ev["mu"]))
            print(f"    H: {q['hl']:<36} L: {q['ll']:<20} verified={q['ok']}  zero-flow tie={q['tie0']}")
            print(f"       P(q=1|H,I)={q['s'] / lam}  P(q=-1|L,I)={q['t'] / lam}  {mus}")
            print(f"       entry E={ev['E']} (~{dec(ev['E'], 7)})  e_H={ev['eH']}  O_H={ev['OH']} "
                  f"(~{dec(ev['OH'], 7)})  e(1)={ev['e'][1]}")
            print(f"       informed payoffs H={ {k: str(v) for k, v in ev['pay']['H'].items()} }")
            print(f"       informed payoffs L={ {k: str(v) for k, v in ev['pay']['L'].items()} }")
            print(f"       uninformed filler payoffs={ {k: str(v) for k, v in ev['payU'].items()} }")
    return o, eqs, sstar


# ----------------------------------------------------------------------------------------------
# Small exact polynomial tools (coefficients low to high degree)
# ----------------------------------------------------------------------------------------------
def pn(c):
    c = [F(x) for x in c]
    while len(c) > 1 and c[-1] == 0:
        c.pop()
    return c


def padd(a, b):
    n = max(len(a), len(b))
    return pn([(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)])


def pscale(a, s):
    return pn([s * x for x in a])


def pmul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return pn(out)


def pder(a):
    return pn([i * a[i] for i in range(1, len(a))] or [0])


def pev(a, x):
    v = F(0)
    for c in reversed(a):
        v = v * x + c
    return v


def prem(a, b):
    a = list(a)
    while len(a) >= len(b) and any(a):
        f = a[-1] / b[-1]
        sh = len(a) - len(b)
        for i in range(len(b)):
            a[sh + i] -= f * b[i]
        a = pn(a)
        if len(a) < len(b) or (len(a) == 1 and a[0] == 0):
            break
    return pn(a)


def sturm_count(p, lo, hi):
    """Number of distinct real roots of p in (lo, hi]."""
    seq = [p, pder(p)]
    while len(seq[-1]) > 1 or seq[-1][0] != 0:
        r = pscale(prem(seq[-2], seq[-1]), -1)
        if len(r) == 1 and r[0] == 0:
            break
        seq.append(r)

    def changes(x):
        vals = [pev(q, x) for q in seq]
        vals = [v for v in vals if v != 0]
        return sum(1 for u, v in zip(vals, vals[1:]) if (u > 0) != (v > 0))

    return changes(lo) - changes(hi)


def bisect(fun, lo, hi, n=48):
    flo = fun(lo)
    for _ in range(n):
        mid = (lo + hi) / 2
        fm = fun(mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return lo, hi


def sqrt_bracket(num, den, digits=14):
    """Rational bracket of sqrt(num/den)."""
    sc = 10 ** digits
    lo = F(isqrt(num * sc * sc // den), sc)
    return lo, lo + F(1, sc)


# ================================================================================================
def main():
    head("0. Auction objects: direct integration against the paper's closed forms (eq. (4))")
    for r in (R0, F(31, 20), F(8, 5), F(33, 20), R1, R2):
        o, c = objects(r), closed(r)
        diffs = {k: o[k] - c[k] for k in c}
        print(f"  r={r}: t0={o['t0']} tH={o['tH']} tL={o['tL']} gH={o['gH']} gL={o['gL']} D={o['D']}")
        print(f"         integration minus closed form: {diffs}")
        print(f"         t+g identity: tH+gH-h={o['tH'] + o['gH'] - H}, tL+gL-l={o['tL'] + o['gL'] - L}")
        print(f"         tau={tau(o)} (~{dec(tau(o), 8)}), B_r(1/2)={Bf(o, PI)} (~{dec(Bf(o, PI), 6)})")

    head("1. Claim 1: every flow on path, every posterior interior, for every informed strategy")
    print("  Posterior at flow x is a_H/(a_H+a_L); a_H rises in sigma_H only, a_L in sigma_L only,")
    print("  so its extremes over all mixed strategies sit at pure profiles. Enumerate them.")
    for variant in ("buy", "two"):
        xs = menu(variant)
        for beta, lam in ((BETA, LAM), (F(1, 100), F(99, 100)), (F(49, 100) if variant == "two" else F(99, 100), F(1, 100))):
            lo = {x: F(1) for x in xs}
            hi = {x: F(0) for x in xs}
            minmass = {x: F(1) for x in xs}
            for qH in xs:
                for qL in xs:
                    aH = masses(variant, beta, lam, {qH: F(1)})
                    aL = masses(variant, beta, lam, {qL: F(1)})
                    for x in xs:
                        mu = aH[x] / (aH[x] + aL[x])
                        lo[x], hi[x] = min(lo[x], mu), max(hi[x], mu)
                        minmass[x] = min(minmass[x], aH[x], aL[x])
            print(f"  {variant} beta={beta} lam={lam}:")
            for x in xs:
                print(f"    flow {x:+d}: min class mass={minmass[x]} (liquidity part {(1 - lam) * liq(variant, beta)[x]}),"
                      f" posterior range [{dec(lo[x], 6)}, {dec(hi[x], 6)}]")
    print("  Boundary cases (liquidity mass by flow; a zero means that flow can lose its common support):")
    for variant, beta in (("two", F(1, 2)), ("buy", F(1)), ("buy", F(0))):
        print(f"    {variant} beta={beta}: liquidity masses {{x: (1-lam) eta}} = "
              f"{ {x: str((1 - LAM) * v) for x, v in liq(variant, beta).items()} }")

    print("  Scope: the menu is finite. The paper lets the investor deviate to any order in [-1, 1].")
    print("  A fractional order q in (0, 1) reaches an unused flow. Its payoff for class H, by belief there:")
    for r in (F(31, 20), R1, R2):
        o = objects(r)
        bb = (1 - LAM) * BETA
        Mx = (bb + LAM) / (2 * bb + LAM)
        full = entry_C1(o, Mx) * o["D"] * (1 - Mx) - K
        q = F(99, 100)
        passive = q * (RHO * o["D"] * (1 - PI) - K)  # belief stays at the prior; B_r(1/2) < c_H, entry rho
        informed = q * (entry_C1(o, F(1)) * o["D"] * (1 - F(1)) - K)  # belief: informed class H
        print(f"    r={r}: full unit purchase {full} (~{dec(full, 5)}); q=99/100 with prior belief {dec(passive, 5)};"
              f" q=99/100 with belief 1 {dec(informed, 5)}")

    head("2. Claim 2: the Proposition 2 strip and every inequality that defines it")
    o0, o1, o2 = objects(R0), objects(R1), objects(R2)
    t1, t2 = tau(o1), tau(o2)
    show("tau(3)", t1)
    show("tau(18/5)", t2)
    print("  Top posterior at full orders: M = (b+lam)/(2b+lam), b = (1-lam) beta; u = lam/b; M = (1+u)/(2+u).")
    print("  (a) c_H window, lower end at r_1=3: B_3(M) > c_H  <=>  M > tau(3)  <=>  u > (2tau-1)/(1-tau)")
    print("  (b) c_H window, upper end at r_2=3.6: B_3.6(M) < c_H  <=>  M < tau(3.6)")
    u_lo, u_hi = (2 * t1 - 1) / (1 - t1), (2 * t2 - 1) / (1 - t2)
    show("u lower = (2tau(3)-1)/(1-tau(3))", u_lo)
    show("u upper = (2tau(3.6)-1)/(1-tau(3.6))", u_hi)
    for beta in (F(1, 10), F(1, 3), F(2, 5), F(9, 10)):
        lam_lo, lam_hi = u_lo * beta / (1 + u_lo * beta), u_hi * beta / (1 + u_hi * beta)
        T2lo, T2hi = 82 * beta / (59 + 82 * beta), 2686 * beta / (1559 + 2686 * beta)
        b_lo, b_hi = (1 - lam_lo) * beta, (1 - lam_hi) * beta
        M_lo, M_hi = (b_lo + lam_lo) / (2 * b_lo + lam_lo), (b_hi + lam_hi) / (2 * b_hi + lam_hi)
        print(f"  beta={beta}: lam in ({lam_lo}, {lam_hi}) ~ ({dec(lam_lo, 6)}, {dec(lam_hi, 6)});"
              f" T2 formula gives ({T2lo}, {T2hi}); M at ends = ({M_lo}, {M_hi})")
    print("  (c) trading-cost window, weak end at 1.2: every unit residual <= D(1.2), so need D(1.2) < k")
    show("D(1.2) - k", o0["D"] - K)
    print("  (d) trading-cost window, strong end at 3: correctly signed residual >= rho D (1 - M) for every")
    print("      candidate, so full orders are unique if rho D(3) (1 - M) > k  <=>  M < 1 - k/(rho D(3))")
    show("1 - k/(rho D(3))", 1 - K / (RHO * o1["D"]))
    show("1 - k/(rho D(3.6))", 1 - K / (RHO * o2["D"]))
    print("      Both exceed tau(3.6), so (d) is slack on the strip. The paper's (1 - 1/b) factor has no analog.")
    print("  (e) other conditions:")
    show("    B_1.2(1/2) - c_H  (no recruitment at r_0, A1 lower side)", Bf(o0, PI) - CH)
    show("    B_3(1/2) - c_H    (A.9 hypothesis: no recruitment at the prior)", Bf(o1, PI) - CH)
    show("    B_3.6(1/2) - c_H", Bf(o2, PI) - CH)
    print(f"    h - r_2 = {H - R2} > 0, so W_H = 1 and ownership rises iff e_H > rho")
    print("    tau'(r) has numerator 4[48(20r - r^2 - 1) - (48r - 3)(20 - 2r)]; expand:")
    num_tau = pn([-3, 48])
    den_tau = pscale(pn([-1, 20, -1]), 4)
    tder = padd(pmul(pder(num_tau), den_tau), pscale(pmul(num_tau, pder(den_tau)), -1))
    print(f"    tau' numerator coefficients (low to high) = {[str(c) for c in tder]}; discriminant "
          f"{tder[1] ** 2 - 4 * tder[2] * tder[0]} < 0 with positive leading term, so tau rises in r.")
    for r in (R1, R2):
        dn = pev(den_tau, r)
        show(f"    tau'({r})", pev(tder, r) / dn ** 2, 6)
    show("  strip width in M: tau(3.6) - tau(3)", t2 - t1)

    head("3. Claim 3: example beta = 1/3, lam = 6/17")
    b = (1 - LAM) * BETA
    M = (b + LAM) / (2 * b + LAM)
    show("b", b)
    show("M", M)
    print(f"  strip at beta=1/3: 82/259={dec(F(82, 259), 6)} < lam={dec(LAM, 6)} < 2686/7363={dec(F(2686, 7363), 6)}")
    for variant in ("buy", "two"):
        for r in (R0, R1, R2):
            for chall, inv in (("C1", "IM"), ("CM", "IM"), ("C1", "I0")):
                solve_V3(variant, BETA, LAM, r, chall, inv, verbose=(chall, inv) == ("C1", "IM") or r == R0)
    print("  Count of verified equilibria by variant, strength and tie rules:")
    for variant in ("buy", "two"):
        for r in (R0, R1, R2):
            row = []
            for chall, inv in (("C1", "IM"), ("CM", "IM"), ("C1", "I0"), ("CM", "I0")):
                _, eqs, _ = solve_V3(variant, BETA, LAM, r, chall, inv, verbose=False)
                ok = [q for q in eqs if q["ok"]]
                row.append(f"{chall}/{inv}: {len(ok)} [" + "; ".join(f"{q['hl']} | {q['ll']} E={q['ev']['E']}" for q in ok) + "]")
            print(f"    {variant} r={r}: " + "  ".join(row))
    print("  Uniqueness bounds over every candidate (mixtures and CM ties included):")
    print(f"    r=1.2: max unit residual D - k = {o0['D'] - K}  (< 0: every nonzero order loses)")
    for o in (o1, o2):
        print(f"    r={o['r']}: min correctly signed residual rho D (1-M) - k = {RHO * o['D'] * (1 - M) - K} "
              f"(~{dec(RHO * o['D'] * (1 - M) - K, 6)}); wrong-signed orders pay -e D(1-mu) - k < 0")
    print("  Ceiling: B_r(M) = c_H. Clear 8r: 8r(B_r(M) - c_H) is a quadratic in r. Interpolate it from")
    print("  three integration-based values and check a fourth point.")
    pts = [F(2), F(3), F(4)]
    vals = [8 * r * (Bf(objects(r), M) - CH) for r in pts]
    # Lagrange interpolation for a quadratic c0 + c1 r + c2 r^2
    poly = [F(0)]
    for i, xi in enumerate(pts):
        li = [F(1)]
        for j, xj in enumerate(pts):
            if j != i:
                li = pmul(li, pscale(pn([-xj, 1]), 1 / (xi - xj)))
        poly = padd(poly, pscale(li, vals[i]))
    chk = F(7, 2)
    print(f"    8r(B_r(M)-6) = {[str(c) for c in poly]} (low to high); check at r=7/2: "
          f"{pev(poly, chk)} vs {8 * chk * (Bf(objects(chk), M) - CH)}")
    print(f"    times -10: {[str(-10 * c) for c in poly]}  ->  29 r^2 - 100 r - 1 = 0, r_C = (50 + sqrt(2529))/29")
    print(f"    dB_r(M)/dr = -M/2 - (3 - 4M)/(8 r^2) with 3 - 4M = {3 - 4 * M} > 0: strictly falling, one root.")
    lo, hi = sqrt_bracket(2529, 1)
    rc_lo, rc_hi = (50 + lo) / 29, (50 + hi) / 29
    print(f"    r_C in [{dec(rc_lo, 14)}, {dec(rc_hi, 14)}]; B(M)-c_H at ends: "
          f"{float(Bf(objects(rc_lo), M) - CH):.3e} and {float(Bf(objects(rc_hi), M) - CH):.3e}")
    print(f"    uniqueness of full orders on [3, 3.6]: rho D(r)(1-M) - k rises with D(r); at r=3 it is "
          f"{RHO * o1['D'] * (1 - M) - K} > 0")

    head("4. Claim 4: coexistence, branch structure, and entry at 1.55, 1.60, 1.65")
    # J(r) = D(r)(1 - tau(r)) = (r-1)^2 (32r - 4r^2 - 1) / (8 r (20r - r^2 - 1))
    for r in (R0, F(3, 2), F(5, 3), R1):
        o = objects(r)
        Jint = o["D"] * (1 - tau(o))
        Jcl = (r - 1) ** 2 * (32 * r - 4 * r * r - 1) / (8 * r * (20 * r - r * r - 1))
        print(f"  check J({r}): integration {Jint}, closed form {Jcl}")
    Np = padd(pmul(pmul(pn([-1, 1]), pn([-1, 1])), pn([-1, 32, -4])),
              pscale(pmul(pn([0, 8]), pn([-1, 20, -1])), -K))
    print(f"  numerator of J - k: {[str(c) for c in Np]} (low to high); denominator 8r(20r-r^2-1) > 0 on [1, 19]")
    rN_lo, rN_hi = bisect(lambda r: (r - 1) ** 2 / (2 * r) - 2 * K / RHO, F(1), F(3))
    rF_lo, rF_hi = bisect(lambda r: (r - 1) ** 2 / (2 * r) - K / (1 - M), F(1), F(3))
    rA_lo, rA_hi = bisect(lambda r: pev(Np, r), F(1), F(3))
    print(f"  r_N: D = 2k/rho = {2 * K / RHO}; bracket [{dec(rN_lo, 12)}, {dec(rN_hi, 12)}]; closed (29+6sqrt6)/25 "
          f"~ {dec((29 + 6 * mpmath.sqrt(6)) / 25, 12)}")
    print(f"  r_F: D = k/(1-M) = {K / (1 - M)}; bracket [{dec(rF_lo, 12)}, {dec(rF_hi, 12)}]")
    print(f"  r_A: J = k; bracket [{dec(rA_lo, 12)}, {dec(rA_hi, 12)}]; signs {pev(Np, rA_lo) < 0}, {pev(Np, rA_hi) > 0}")
    print(f"  Sturm: roots of J-k numerator in (1, r_N upper] = {sturm_count(Np, F(1), rN_hi)}; "
          f"in (1, 18/5] = {sturm_count(Np, F(1), R2)}; J(1) - k = {-K}")
    print(f"  tau(r_N upper) = {dec(tau(objects(rN_hi)), 8)} < M = {dec(M, 8)}: s* < lam on the interval")
    print(f"  B_r(1/2) at r_N upper = {dec(Bf(objects(rN_hi), PI), 6)} < 6: no-trade entry is rho")
    # T2's derivative polynomial for V3, in y = r - 1
    Dn = pmul(pn([0, 8]), pn([-1, 20, -1]))
    N1 = pmul(pmul(pn([-1, 1]), pn([-1, 1])), pn([-1, 32, -4]))
    dJ = padd(pmul(pder(N1), Dn), pscale(pmul(N1, pder(Dn)), -1))
    # substitute r = 1 + y
    sub = [F(0)]
    powy = [F(1)]
    for c in dJ:
        sub = padd(sub, pscale(powy, c))
        powy = pmul(powy, pn([1, 1]))
    t2poly = pn([0, 972, 2268, 1440, 3, -136, 4])
    ratio = [sub[i] / t2poly[i] if t2poly[i] != 0 else (sub[i] if i < len(sub) else None) for i in range(len(t2poly))]
    print(f"  dJ/dr numerator in y=r-1: {[str(c) for c in sub]}")
    print(f"  ratio to T2's y(972+2268y+1440y^2+3y^3-136y^4+4y^5): {[str(x) for x in ratio]}")
    for r, lab in ((F(31, 20), "1.55"), (F(8, 5), "1.60"), (F(33, 20), "1.65")):
        for variant in ("buy", "two"):
            for chall, inv in (("C1", "IM"), ("CM", "IM"), ("C1", "I0")):
                solve_V3(variant, BETA, LAM, r, chall, inv, verbose=(variant == "buy" or chall == "CM"))
    print("  Branch structure across strengths (V3 buy, C1/IM unless stated):")
    for r in (F(7, 5), F(29, 20), F(3, 2), F(31, 20), F(8, 5), F(33, 20), F(17, 10), F(7, 4), F(9, 5)):
        _, eqs, _ = solve_V3("buy", BETA, LAM, r, "C1", "IM", verbose=False)
        _, eqsm, _ = solve_V3("buy", BETA, LAM, r, "CM", "IM", verbose=False)
        lst = "; ".join(f"{q['hl']} E~{dec(q['ev']['E'], 6)}" for q in eqs if q["ok"])
        lstm = "; ".join(f"{q['hl']} E~{dec(q['ev']['E'], 6)}" for q in eqsm if q["ok"] and "threshold" in q["hl"])
        print(f"    r={dec(r, 3)}: {lst}" + (f" | CM adds: {lstm}" if lstm else ""))
    print("  Threshold-mixture entry (CM), exact:")
    Es = []
    for r in (F(31, 20), F(8, 5), F(33, 20)):
        _, eqs, _ = solve_V3("buy", BETA, LAM, r, "CM", "IM", verbose=False)
        for q in eqs:
            if "threshold" in q["hl"] and q["ok"]:
                Es.append(q["ev"]["E"])
                print(f"    r={r}: E* = {q['ev']['E']} (~{dec(q['ev']['E'], 8)}), challenger entry at flow 1 = "
                      f"{dec(q['ev']['e'][1], 6)}")
    if len(Es) == 3:
        print(f"    differences: E(1.60)-E(1.55) = {dec(Es[1] - Es[0], 8)}, E(1.65)-E(1.60) = {dec(Es[2] - Es[1], 8)}")
    print("  Any strictly rising selection across 1.55 < 1.60 < 1.65 from the informative sets "
          "{E*(r), 37/68}?")
    sets = [[Es[0], F(37, 68)], [Es[1], F(37, 68)], [Es[2], F(37, 68)]] if len(Es) == 3 else []
    rising = [c for c in itertools.product(*sets) if c[0] < c[1] < c[2]]
    print(f"    rising selections found: {len(rising)}")

    head("5. Claim 5: Proposition A.9 analog at r = 3 (both regimes solved from primitives)")
    o = o1
    for variant in ("buy", "two"):
        _, eqs, _ = solve_V3(variant, BETA, LAM, R1, "C1", "IM", verbose=False)
        acc = [q for q in eqs if q["ok"]][0]
        sH = {1: acc["s"] / LAM, 0: 1 - acc["s"] / LAM}
        sL = {-1: acc["t"] / LAM, 0: 1 - acc["t"] / LAM} if variant == "two" else {0: F(1)}
        # hidden price: challenger keeps the prior; B_3(1/2) < c_H so entry is rho at every flow
        hid_ent = {x: RHO for x in menu(variant)}
        # hidden-price investor: check full orders are best responses and zero is not
        evh = evaluate(variant, BETA, LAM, o, sH, sL, hid_ent)
        print(f"  {variant}: hidden-price investor payoffs H={ {k: str(v) for k, v in evh['pay']['H'].items()} }, "
              f"L={ {k: str(v) for k, v in evh['pay']['L'].items()} }")
        print(f"    full orders best responses under hidden price: H {best_response_ok(evh['pay']['H'], sH, 'I0')}, "
              f"L {best_response_ok(evh['pay']['L'], sL, 'I0')}")
        res = {}
        for name, ent in (("access", None), ("hidden", hid_ent)):
            ev = evaluate(variant, BETA, LAM, o, sH, sL, ent)
            proceeds = F(0)
            surplus = F(0)
            for j, a in (("H", ev["aH"]), ("L", ev["aL"])):
                pj = PI if j == "H" else 1 - PI
                for x in menu(variant):
                    e = ev["e"][x]
                    hc = (e - RHO) / (1 - RHO)  # high-cost preparation probability
                    proceeds += pj * a[x] * (o["t0"] + e * (o["t" + j] - o["t0"]))
                    surplus += pj * a[x] * (o["s0"] + e * (o["s" + j] - o["s0"]) - (1 - RHO) * hc * CH - RHO * CL)
            tc = LAM * sum((PI if j == "H" else 1 - PI) * sum(w * K * abs(q) for q, w in sg.items())
                           for j, sg in (("H", sH), ("L", sL)))
            res[name] = (proceeds, surplus, tc)
            print(f"    {name}: proceeds={proceeds} (~{dec(proceeds, 6)}), net surplus={surplus} "
                  f"(~{dec(surplus, 6)}), informed trading cost={tc}")
        print(f"    access - hidden: proceeds {res['access'][0] - res['hidden'][0]}, net surplus "
              f"{res['access'][1] - res['hidden'][1]}, trading cost {res['access'][2] - res['hidden'][2]}")

    head("6. Claim 6: an uninformed filler with only the trading payoff")
    print("  Payoffs printed with each outcome above ('uninformed filler payoffs'). Summary of maxima over nonzero orders:")
    for variant in ("buy", "two"):
        for r in (R0, F(7, 5), F(31, 20), F(8, 5), F(33, 20), R1, R2):
            for chall in ("C1", "CM"):
                _, eqs, _ = solve_V3(variant, BETA, LAM, r, chall, "IM", verbose=False)
                for q in eqs:
                    if q["ok"]:
                        pu = q["ev"]["payU"]
                        best_nonzero = max(v for k, v in pu.items() if k != 0)
                        print(f"    {variant} r={dec(r, 3)} {chall} {q['hl']:<36}: best nonzero uninformed payoff "
                              f"{dec(best_nonzero, 6)} vs zero order 0")

    head("7. Claim 7: equal posteriors, unequal payoff thresholds (buy-only geometric base)")
    a = F(11, 29)
    c = (1 - a) / (1 + a)

    def f(z):
        return c * a ** abs(z)

    gam = 1 / (1 + a)
    print(f"  base noise f(z) = (1-a)/(1+a) a^|z|, a = {a}; gamma = 1/(1+a) = {gam}")
    print("  informed investor always present; class H buys one unit, class L abstains; prior 1/2.")
    for x in range(-3, 5):
        mu = f(x - 1) / (f(x - 1) + f(x))
        print(f"    flow {x:+d}: posterior {mu}")
    Z = 120
    tail_trunc = sum(f(z) for z in range(0, Z + 1))
    print(f"  P(Z >= 0) truncated at {Z}: {dec(tail_trunc, 15)}; closed form gamma = {dec(gam, 15)}; "
          f"remainder bound {dec(c * a ** (Z + 1) / (1 - a), 3)}")
    o = o1
    tbase = tau(o)
    for name, ep, em in (("hidden price", RHO, RHO), ("price access", F(1) if gam >= tbase else RHO, RHO)):
        Kb_trunc = sum(f(z) * (ep if z + 1 >= 1 else em) * o["D"] * (1 - (gam if z + 1 >= 1 else 1 - gam))
                       for z in range(-Z, Z + 1))
        Kb = gam * ep * o["D"] * (1 - gam) + (1 - gam) * em * o["D"] * gam
        lam_s, beta_s = F(9, 20), F(1, 2)
        ev = evaluate("buy", beta_s, lam_s, o, {1: F(1)}, {0: F(1)}, {1: ep, 0: em})
        Ks = ev["pay"]["H"][1] + K
        print(f"  {name}: base K = {Kb} (~{dec(Kb, 6)}; truncated sum ~{dec(Kb_trunc, 6)}); "
              f"slot K (beta=1/2, lam=9/20) = {Ks} (~{dec(Ks, 6)}); slot posterior at flow 1 = {ev['mu'][1]}")
        print(f"     slot P(x=1|H)={ev['aH'][1]}, P(x=1|L)={ev['aL'][1]}; base P(X>=1|H)={gam}, P(X>=1|L)={1 - gam}")

    head("8. Why the strip is narrow")
    show("tau(3)", t1, 6)
    show("tau(3.6)", t2, 6)
    ML = mpmath.e / (1 + mpmath.e)
    rcL = (10 * ML - 6 + mpmath.sqrt((10 * ML - 6) ** 2 + ML * (F(3, 4) - ML))) / ML
    print(f"  Laplace (b=2) top posterior e/(1+e) = {mpmath.nstr(ML, 10)}; its ceiling r_C = {mpmath.nstr(rcL, 12)}")
    print(f"  tau(3.6) - e/(1+e) = {mpmath.nstr(mpmath.mpf(t2.numerator) / t2.denominator - ML, 6)}")
    print(f"  e/(1+e) - tau(3) = {mpmath.nstr(ML - mpmath.mpf(t1.numerator) / t1.denominator, 6)}")
    print("  Partial derivatives of B_r(mu) at r=3, mu=29/40:")
    print(f"    dB/dmu = gH - gL = {o1['gH'] - o1['gL']};  dB/dr = -mu/2 - (3-4mu)/(8 r^2) = "
          f"{-M / 2 - (3 - 4 * M) / (8 * 9)}")


if __name__ == "__main__":
    main()
