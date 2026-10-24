"""Hidden toehold: the challenger buys one unit (cost kC) after it learns its cost C, before the price.

Discrete-Laplace noise, buy-only investor (class H buys w.p. beta), challenger buy decision S(C) in {0,1}.
The unit is small: it changes the flow, not the challenger's entry gain.  All sums are exact over three flow regions
{x <= 0}, {x = 1}, {x >= 2}: the likelihood ratios of every pair of hypotheses (j, S) are constant on each region.
Prices are competitive; the challenger observes the region (price) and its own S and C.
Pure profiles (beta, sigmaL, sigmaH); investor tie -> no trade, challenger tie -> no trade, entry tie -> prepare.
"""
import sys, itertools
from common import *

set_mode('hp')
par = P()
a = par.a
rho = par.rho
half = K(1, 2)


def nz_prob(lo, hi):
    """P(Z in [lo, hi]) for the discrete Laplace; lo or hi may be None for -inf / +inf."""
    # CDF-style closed forms
    c = (1 - a) / (1 + a)
    def tail_up(m):  # P(Z >= m)
        if m >= 1:
            return c * a ** m / (1 - a)
        if m <= 0:
            return 1 - tail_up(1 - m * 0 + (-m + 1)) if False else 1 - (c * a ** (1 - m) / (1 - a))
    # P(Z>=m) for m>=1 = a^m/(1+a);  for m<=0 = 1 - P(Z>=-m+1)*... use symmetry
    def ge(m):
        if m >= 1:
            return a ** m / (1 + a)
        return 1 - a ** (1 - m) / (1 + a)  # P(Z >= m) = 1 - P(Z <= m-1) = 1 - P(Z >= 1-m)
    up = ge(lo) if lo is not None else K(1)
    dn = ge(hi + 1) if hi is not None else K(0)
    return up - dn


REG = [(None, 0), (1, 1), (2, None)]  # regions of x


def region_prob(shift):
    """P(x in region | x = shift + Z) for the three regions."""
    out = []
    for lo, hi in REG:
        zl = None if lo is None else lo - shift
        zh = None if hi is None else hi - shift
        out.append(nz_prob(zl, zh))
    return out


def solve_profile(A, beta, sL, sH, kC):
    prior = {'H': half, 'L': half}
    pC = {'L': rho, 'H': 1 - rho}
    S = {'L': sL, 'H': sH}
    qI = {'H': beta, 'L': 0}
    t = {'H': A['tH'], 'L': A['tL']}
    def mixrp(j, shift):
        if j == 'L':
            return region_prob(shift)
        r0_, r1_ = region_prob(shift), region_prob(shift + 1)
        return [(1 - beta) * r0_[i] + beta * r1_[i] for i in range(3)]
    def lik(j, C):
        return mixrp(j, S[C])
    groups = [[0], [1], [2]]          # regions the challenger can tell apart (refined below)
    for _ in range(6):
        gid = {}
        for gi, g in enumerate(groups):
            for R in g:
                gid[R] = gi
        def mu_C(R, s_own):
            g = groups[gid[R]]
            pH = sum(mixrp('H', s_own)[x] for x in g)
            pL = sum(mixrp('L', s_own)[x] for x in g)
            return pH / (pH + pL)
        def e_hc(R, s_own):
            return K(1) if Bgain(A, mu_C(R, s_own)) >= par.cH else K(0)
        ent = {}
        for R in range(3):
            ent[('L', R)] = K(1)
            ent[('H', R)] = e_hc(R, S['H'])
        price = []
        joint = {}
        for R in range(3):
            num_ = K(0)
            den = K(0)
            for j in 'HL':
                for C in 'LH':
                    pr = prior[j] * pC[C] * lik(j, C)[R]
                    joint[(j, C, R)] = pr
                    num_ += pr * (A['t0'] + ent[(C, R)] * (t[j] - A['t0']))
                    den += pr
            price.append(num_ / den)
        # regroup: regions with equal prices are pooled for the challenger
        newg = []
        used = set()
        for R in range(3):
            if R in used:
                continue
            g = [R]
            for R2 in range(R + 1, 3):
                if abs(price[R] - price[R2]) <= K(1, 10 ** 30):
                    g.append(R2)
                    used.add(R2)
            newg.append(g)
        if newg == groups:
            break
        groups = newg
    def V(j, C, R, e=None):
        e = ent[(C, R)] if e is None else e
        return A['t0'] + e * (t[j] - A['t0'])
    def inv_gain(j):
        g = K(0)
        for C in 'LH':
            rp = region_prob(1 + S[C])
            for R in range(3):
                g += pC[C] * rp[R] * (V(j, C, R) - price[R])
        return g - par.k
    gH = inv_gain('H')
    gL = inv_gain('L')
    def chal_gain(C):
        """Gain of buying one unit (the payoff of not buying is zero)."""
        tot = K(0)
        for j in 'HL':
            rp = mixrp(j, 1)
            for R in range(3):
                e = K(1) if C == 'L' else e_hc(R, 1)
                tot += prior[j] * rp[R] * (A['t0'] + e * (t[j] - A['t0']) - price[R])
        return tot - kC
    cLg = chal_gain('L')
    cHg = chal_gain('H')
    ok_inv = (gH > 0) if beta == 1 else (gH <= 0)
    ok_invL = gL <= 0
    ok_cL = (cLg > 0) if sL == 1 else (cLg <= 0)
    ok_cH = (cHg > 0) if sH == 1 else (cHg <= 0)
    E = K(0)
    OH = K(0)
    for (j, C, R), pr in joint.items():
        E += pr * ent[(C, R)]
        if j == 'H':
            OH += pr * ent[(C, R)]
    Pi = A['t0'] + A['wL'] * E + A['DT'] * OH
    return dict(ok=ok_inv and ok_invL and ok_cL and ok_cH, gH=gH, gL=gL, cL=cLg, cH=cHg, E=E, OH=OH, Pi=Pi, price=price, groups=groups)


if __name__ == '__main__':
    kC = par.k if len(sys.argv) < 2 else K(int(sys.argv[1]), 1000)
    print('challenger trading cost kC =', mp.nstr(kC, 4), '; investor cost k =', mp.nstr(par.k, 4))
    for r in [Fr(6, 5), Fr(3), Fr(18, 5), Fr(21, 5)]:
        A = auction(par, r)
        print(f"\nr={float(r)}  DT={mp.nstr(A['DT'],5)} wL={mp.nstr(A['wL'],5)}")
        for beta, sL, sH in itertools.product((0, 1), repeat=3):
            o = solve_profile(A, beta, sL, sH, kC)
            tag = 'EQ ' if o['ok'] else '   '
            print(f" {tag}beta={beta} sL={sL} sH={sH}  gains: H-inv={mp.nstr(o['gH'],5):>9} L-inv={mp.nstr(o['gL'],5):>9} cL={mp.nstr(o['cL'],5):>9} cH={mp.nstr(o['cH'],5):>9} | E={mp.nstr(o['E'],5)} OH={mp.nstr(o['OH'],5)} Pi-t0={mp.nstr(o['Pi']-A['t0'],5)} groups={o['groups']}")
