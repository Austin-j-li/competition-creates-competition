"""Certificate for one T6 parameter point (print only).

Usage: python t6_certify.py LAM BETA THETA [BOX_HALF_WIDTH_DENOMINATOR [STRENGTHS]]
  (rationals as a/b; default point 9/20 12/25 71/200 and box half-widths 1/2000;
   STRENGTHS is a comma list of three middle strengths, default 31/20,8/5,33/20; section E runs only
   for the default strengths and a nonzero box denominator)

Sections:
  A. The point: c, u, M; full-trade posteriors and entry at r = 3.
  B. Prop. 2: closed-form uniqueness bounds at r = 3 and 18/5; full enumeration at 6/5, 3, 18/5 under the four
     rule sets.
  C. Prop. 3: full enumeration at 31/20, 8/5, 33/20 under the four rule sets; the selected branch with exact
     root brackets, monotonicity certificate, pattern and no-sale checks, entry enclosures; branch endpoints.
  D. Prop. A.9 at r = 3: the hidden-price game and the gains from price access.
  E. An open box around the point on which every sign condition of B and C holds (rational intervals).
"""
import sys
import itertools
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from t6_core import bench, enumerate_equilibria, fmt, fl, Iv, sign_of, r_of_spread, r_ceiling, FLOWS  # noqa: E402
import t6_branch as tb  # noqa: E402

RHO = F(1, 4)
RULES = (('M', 'X'), ('M', 'E'), ('Z', 'X'), ('Z', 'E'))
MID = (F(31, 20), F(8, 5), F(33, 20))


def show_eqs(P, r, rules=RULES, hidden=False):
    P = dict(P)
    P['r'] = r
    res = {}
    for inv, ch in rules:
        eqs, und, M = enumerate_equilibria(P, investor=inv, challenger=ch, hidden=hidden)
        res[(inv, ch)] = (eqs, und, M)
        print(f"  r = {fmt(r)}, investor rule {inv}, challenger rule {ch}{' (hidden prices)' if hidden else ''}: "
              f"{len(eqs)} equilibria, {len(und)} undecided")
        for u in und:
            print('     UNDECIDED:', u)
        for q in eqs:
            mu = M.posteriors(q['a'], q['s'])
            o = q['out']
            hs, lb = M.wrong_way(q['a'] if not isinstance(q['a'], Iv) else q['a'].mid(),
                                 q['s'] if not isinstance(q['s'], Iv) else q['s'].mid(),
                                 {x: (q['e'][x] if not isinstance(q['e'][x], Iv) else q['e'][x].mid()) for x in FLOWS})
            print(f"     {q['label']:24s} [{q['where']}, {q['cert']}] A = {fmt(q['a'])}, S = {fmt(q['s'])}")
            print(f"        entry by flow (x=-2..2): {', '.join(fmt(q['e'][x], 4) for x in FLOWS)};"
                  f" challenger mixes at {q['chall_mix'] or 'none'}")
            print(f"        posteriors: {', '.join(f'{fl(mu[x]):.6f}' for x in FLOWS)}")
            print(f"        E = {fmt(o['E'])}, O_H = {fmt(o['OH'])}, R_T = {fmt(o['RT'])}, W = {fmt(o['W'])}, "
                  f"trading cost = {fmt(o['cost'])}")
            print(f"        wrong-way gross gains per unit Delta: H sells {float(hs):.6f}, L buys {float(lb):.6f}")
    return res


def main():
    args = sys.argv[1:]
    lam, beta, theta = (F(v) for v in args[:3]) if len(args) >= 3 else (F(9, 20), F(12, 25), F(71, 200))
    boxden = int(args[3]) if len(args) >= 4 else 2000
    global MID
    default_mid = MID
    if len(args) >= 5:
        MID = tuple(F(v) for v in args[4].split(','))
    P = bench(lam=lam, beta=beta, theta=theta)
    c = (1 - lam) * beta
    ph, d = 1 - 2 * theta, 1 - 3 * theta
    u = lam / c
    M = (c + lam) / (2 * c + lam)
    chi = 1 - 2 * c - lam
    w = 2 * c + lam
    tau3, tau36 = tb.auc(F(3))[1], tb.auc(F(18, 5))[1]
    print('=' * 110)
    print(f"A. Point: lam = {fmt(lam)}, beta = {fmt(beta)}, theta = {fmt(theta)}")
    print(f"   c = (1 - lam) beta = {fmt(c)}, u = lam/c = {fmt(u)}, M = {fmt(M)}; phi = {fmt(ph)}, d = {fmt(d)}")
    print(f"   M - tau(3) = {fmt(M - tau3)}, tau(18/5) - M = {fmt(tau36 - M)}")
    mu1T = ((c + lam) * ph + chi * theta) / (w * ph + 2 * chi * theta)
    print(f"   full trade: mu_1 = {fmt(mu1T)} (minus tau(3): {fmt(mu1T - tau3)}), mu_2 = M, mu_0 = 1/2")
    p2, p1 = theta * w / 2, ph * w / 2 + theta * chi
    E3 = RHO + (1 - RHO) * (p2 + p1)
    print(f"   Pr(X=2) = {fmt(p2)}, Pr(X=1) = {fmt(p1)}; entry at r = 3: {fmt(E3)} (paper 0.522757)")
    print(f"   ceilings: r_C(M) in {r_ceiling(P, M)}, r_C(mu_1) in {r_ceiling(P, mu1T)}")
    print(f"   liquidity share of slot purchases under full trade: c/(c + lam/2) = {fmt(c / (c + lam / 2))}")

    print('=' * 110)
    print('B. Prop. 2')
    L0 = 2 * c * theta + (1 - 2 * c) * ph
    if d < 0:
        bound = RHO * theta * (1 / (2 + lam * (-d) / L0) + 1 - M)
        print(f"   theta > 1/3 bound: rho theta [1/(2 + lam|d|/L0) + 1 - M] = {fmt(bound)}")
    else:
        bound = RHO * (1 - theta) * (1 - M)
        print(f"   theta <= 1/3 bound: rho (1 - theta)(1 - M) = {fmt(bound)}")
    for r in (F(3), F(18, 5)):
        print(f"   r = {fmt(r)}: bound - k/Delta = {fmt(bound - tb.kappa(r))}")
    for r in (F(6, 5), F(3), F(18, 5)):
        show_eqs(P, r)

    print('=' * 110)
    print('C. Prop. 3')
    for r in MID:
        show_eqs(P, r)
    print('  Selected branch: no sale, recruitment only at x = 2, pure entry.')
    rA, sA = tb.r_A(lam, beta, theta)
    rF, sF = tb.r_F(lam, beta, theta)
    rN = r_of_spread(2 * F(1, 50) / RHO)
    print(f"   branch start r_A (K2(A_2(r)) = k/Delta) in [{float(rA[0]):.12f}, {float(rA[1]):.12f}], signs {sA}")
    print(f"   full purchase r_F (K2(lam) = k/Delta) in [{float(rF[0]):.12f}, {float(rF[1]):.12f}], signs {sF}")
    print(f"   no-trade boundary r_N in {rN}")
    # the branch exists at every strength in (r_A, r_F]: K2(A_2(r)) - k/Delta(r) > 0, adaptive interval bisection in r
    def G(rI):
        D, tau = tb.auc(rI)
        return tb.K2(lam, beta, theta, c * (2 * tau - 1) / (1 - tau)) - F(1, 50) / D
    stack, ncell, bad = [(rA[1], rF[1], 0)], 0, 0
    while stack:
        a_, b_, dep = stack.pop()
        if G(Iv(a_, b_)).lo > 0:
            ncell += 1
            continue
        if dep > 40:
            bad += 1
            continue
        m_ = (a_ + b_) / 2
        stack += [(a_, m_, dep + 1), (m_, b_, dep + 1)]
    print(f"   K2(A_2(r)) > k/Delta(r) on [r_A upper end, r_F upper end]: {bad == 0} ({ncell} interval cells, {bad} failed)")
    Es = []
    for r in MID:
        a2 = tb.A2(lam, beta, theta, r)
        kp = tb.K2_prime(lam, beta, theta, lam)
        br, sg = tb.root_A(lam, beta, theta, r)
        print(f"   r = {fmt(r)}: A_2 = {fmt(a2)}; K2'(lam) = {fmt(kp)} (< 0 with K2 convex: K2 falls on [0, lam])")
        if br is None:
            full = tb.K2(lam, beta, theta, lam) - tb.kappa(r)
            print(f"      no interior root (endpoint signs {sg}); K2(lam) - k/Delta = {fmt(full)} -> full purchase (BNS)")
            Aiv = Iv(lam)
        else:
            Aiv = Iv(*br)
            print(f"      root A in [{float(br[0]):.15f}, {float(br[1]):.15f}], signs at A_2 and lam: {sg}; "
                  f"alpha = A/lam in {Aiv / lam}")
        E = RHO + (1 - RHO) * theta * (2 * c + Aiv) / 2
        Es.append(E)
        mus = tb.posts(lam, beta, theta, lam)
        print(f"      entry on branch in {E}")
        print(f"      pattern at A = lam: mu_0 = {fmt(mus[0])} vs tau = {fmt(tb.auc(r)[1])}; mu_1 = {fmt(mus[1])}, "
              f"mu_-1 = {fmt(mus[-1])}")
        # no sale: sup of the sale payoff over A in [0, lam], by subdivision
        sup = None
        n = 64
        for i in range(n):
            box = Iv(lam * i / n, lam * (i + 1) / n)
            v = tb.gL_noside(lam, beta, theta, box)
            sup = v.hi if sup is None else max(sup, v.hi)
        print(f"      sale payoff per unit Delta on (A, 0), A in [0, lam]: at most {float(sup):.6f} < k/Delta = "
              f"{float(tb.kappa(r)):.6f}: {sup < tb.kappa(r)}")
        print(f"      no-trade deviation payoff: rho Delta/2 - k = {fmt(RHO * tb.auc(r)[0] / 2 - F(1, 50))}")
    gl_bns = tb.gL_noside(lam, beta, theta, lam)
    print(f"   BNS sale payoff per unit Delta = {fmt(gl_bns)}; k/Delta(r_N) = rho/2 = 1/8: BNS has no sale up to r_N: {gl_bns < RHO / 2}")
    print(f"   entry enclosures disjoint and ordered: {Es[0].hi < Es[1].lo and Es[1].hi < Es[2].lo}; "
          f"gaps at least {float(Es[1].lo - Es[0].hi):.6f} and {float(Es[2].lo - Es[1].hi):.6f}")

    print('=' * 110)
    print('D. Prop. A.9 at r = 3')
    res_h = show_eqs(P, F(3), rules=(('M', 'X'),), hidden=True)
    res_f = enumerate_equilibria(dict(P, r=F(3)))
    qf = res_f[0][0]
    for qh in res_h[('M', 'X')][0]:
        dR = qf['out']['RT'] - qh['out']['RT']
        dW = qf['out']['W'] - qh['out']['W']
        print(f"   vs hidden-price {qh['label']}: Delta R_T = {fmt(dR)}, Delta W = {fmt(dW)}, "
              f"trading costs {fmt(qf['out']['cost'])} and {fmt(qh['out']['cost'])}")

    print('=' * 110)
    if MID != default_mid or boxden == 0:
        print('E. Open box: skipped (non-default middle strengths, or box denominator 0)')
        return
    hw = F(1, boxden)
    print(f"E. Open box: |lam - {lam}| <= {hw}, |beta - {beta}| <= {hw}, |theta - {theta}| <= {hw} (closed box)")
    conds = box_conditions()
    ncell = 4
    worst = {name: None for name in conds}
    for i, j, k in itertools.product(range(ncell), repeat=3):
        lI = Iv(lam - hw + 2 * hw * i / ncell, lam - hw + 2 * hw * (i + 1) / ncell)
        bI = Iv(beta - hw + 2 * hw * j / ncell, beta - hw + 2 * hw * (j + 1) / ncell)
        tI = Iv(theta - hw + 2 * hw * k / ncell, theta - hw + 2 * hw * (k + 1) / ncell)
        for name, fn in conds.items():
            v = fn(lI, bI, tI)
            worst[name] = v.lo if worst[name] is None else min(worst[name], v.lo)
    allpos = True
    for name, v in worst.items():
        allpos = allpos and v > 0
        print(f"   {name:62s} lower bound {float(v):+.3e}")
    print(f"   every margin positive on all {ncell ** 3} cells: {allpos}")


def box_conditions():
    """Margins that must be positive (each a function of rational intervals lam, beta, theta)."""
    t3, t36 = tb.auc(F(3))[1], tb.auc(F(18, 5))[1]

    def Mf(l, b, t):
        c = (1 - l) * b
        return (c + l) / (2 * c + l)

    def mu1T(l, b, t):
        c = (1 - l) * b
        ph = 1 - 2 * t
        chi = 1 - 2 * c - l
        return ((c + l) * ph + chi * t) / ((2 * c + l) * ph + 2 * chi * t)

    def ubound(l, b, t):
        c = (1 - l) * b
        ph, dneg = 1 - 2 * t, 3 * t - 1
        L0 = 2 * c * t + (1 - 2 * c) * ph
        return RHO * t * (1 / (2 + l * dneg / L0) + 1 - Mf(l, b, t))

    def gl_sup(l, b, t, r):
        n = 16
        sup = None
        for i in range(n):
            A = Iv(i * l.lo / n, (i + 1) * l.hi / n)
            v = tb.gL_noside(l, b, t, A)
            sup = v.hi if sup is None else max(sup, v.hi)
        return Iv(tb.kappa(r) - sup)

    out = {
        'M - tau(3)': lambda l, b, t: Mf(l, b, t) - t3,
        'tau(18/5) - M': lambda l, b, t: t36 - Mf(l, b, t),
        'mu_1(full trade) - tau(3)  [entry level at 3]': lambda l, b, t: mu1T(l, b, t) - t3,
        'uniqueness bound - k/Delta(3)': lambda l, b, t: ubound(l, b, t) - tb.kappa(F(3)),
        'uniqueness bound - k/Delta(18/5)': lambda l, b, t: ubound(l, b, t) - tb.kappa(F(18, 5)),
        '3 theta - 1  [theta > 1/3: convexity, bound of B]': lambda l, b, t: 3 * t - 1,
        'K2(A_2(31/20)) - k/Delta(31/20)  [branch exists at 1.55]':
            lambda l, b, t: tb.K2(l, b, t, tb.A2(l, b, t, F(31, 20))) - tb.kappa(F(31, 20)),
        'K2(A_2(8/5)) - k/Delta(8/5)':
            lambda l, b, t: tb.K2(l, b, t, tb.A2(l, b, t, F(8, 5))) - tb.kappa(F(8, 5)),
        'k/Delta(8/5) - K2(lam)  [partial at 1.60]': lambda l, b, t: tb.kappa(F(8, 5)) - tb.K2(l, b, t, l),
        'K2(lam) - k/Delta(33/20)  [full at 1.65]': lambda l, b, t: tb.K2(l, b, t, l) - tb.kappa(F(33, 20)),
        'lam - A_2(33/20)  [segment nonempty]': lambda l, b, t: l - tb.A2(l, b, t, F(33, 20)),
        '-K2\'(lam)  [K2 falls on the segment]': lambda l, b, t: -tb.K2_prime(l, b, t, l),
        'tau(31/20) - mu_0(lam, 0)  [x = 0 never recruits]':
            lambda l, b, t: tb.auc(F(31, 20))[1] - tb.posts(l, b, t, l)[0],
        'k/Delta(33/20) - sup sale payoff on (A, 0)  [no sale]': lambda l, b, t: gl_sup(l, b, t, F(33, 20)),
    }
    return out


if __name__ == '__main__':
    main()
