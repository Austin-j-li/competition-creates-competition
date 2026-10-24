"""C4: interval-arithmetic certificate for pure equilibria at benchmark points. Print-only.

For one parameter point this script
  1. builds every round-2 subgame that can follow a pure round-1 profile (16 profiles x 2 signals x 2 decisions),
     and classifies each of its 64 pure candidates (4 investor types buy or not; challenger-2 high-cost entry
     at each signal) as CERTIFIED (every equilibrium inequality holds strictly on the enclosure),
     REFUTED (some inequality fails on the whole enclosure) or UNDECIDED;
  2. classifies every round-1 pure candidate (16 investor profiles x 4 challenger-1 entry patterns) that
     uses certified round-2 continuations.
All arithmetic uses mpmath interval arithmetic with a = exp(-1/2) enclosed; the parameters are exact rationals.
A certified candidate is an equilibrium; REFUTED candidates are not.  Strict inequalities are required for
CERTIFIED, so equilibria that rely on an exact tie are reported as UNDECIDED.  For an informative candidate,
CERTIFIED also requires the two prices of the round to differ on the whole enclosure, so that the challenger
reads the signal from the price.  Separately, for every informative pure round-2 investor profile the script
tests whether a pooled price (a common entry probability at both signals, any value in [rho, 1]) is possible.
Where it is, the pooled candidate (entry set at the pooled belief, which is the round-2 prior) is tested
against the investor inequalities; the script reports the pooled candidates it cannot refute.
Round-1 pooling is not tested.
Run from the repository root:
    .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/C4_sequential/c4_certify.py
"""
from fractions import Fraction as F
from itertools import product

from mpmath import iv

iv.dps = 40
ST = ('HH', 'HL', 'LH', 'LL')
SIG = ('g', 'b')


def I(fr):
    fr = F(fr)
    return iv.mpf(fr.numerator) / iv.mpf(fr.denominator)


def pos(x):
    return x.a > 0


def neg(x):
    return x.b < 0


class IModel:
    def __init__(self, r, cH, kappa='0', h='10', l='1', p='1/2', rho='1/4', k='1/50', b='2'):
        self.r, self.cH, self.rho, self.k = I(r), I(cH), I(rho), I(k)
        h, l, p, r_ = I(h), I(l), I(p), I(r)
        kap = I(kappa)
        self.a = iv.exp(-1 / I(b))
        a = self.a
        self.prior = {'HH': (1 + kap) / 4, 'HL': (1 - kap) / 4, 'LH': (1 - kap) / 4, 'LL': (1 + kap) / 4}
        t0 = p * (1 - p / r_)
        tH = r_ / 2 + p * p / (2 * r_)
        tL = l - (l * l - p * p) / (2 * r_)
        gH = h - tH
        gL = (l * l - p * p) / (2 * r_)
        DT = (r_ - l) ** 2 / (2 * r_)
        self.gL, self.D = gL, gH - gL
        self.t = {'H': tH, 'L': tL}
        self.g = {'H': gH, 'L': gL}
        T = {'HH': h, 'HL': l + DT, 'LH': l + DT, 'LL': l}
        self.base = {1: {s: self.t[s[0]] for s in ST}, 0: {s: t0 for s in ST}}
        self.inc = {1: {s: T[s] - self.t[s[0]] for s in ST}, 0: {s: self.t[s[1]] - t0 for s in ST}}
        self.pbuy = {'g': 1 / (1 + a), 'b': a / (1 + a)}
        self.one = iv.mpf(1)

    def psig(self, S, beta):
        a = self.a
        pg = (a + beta * (1 - a)) / (1 + a)
        return pg if S == 'g' else 1 - pg

    def post(self, nu, beta, S):
        w = {s: nu[s] * self.psig(S, beta[s]) for s in ST}
        z = w['HH'] + w['HL'] + w['LH'] + w['LL']
        return {s: w[s] / z for s in ST}

    def gain2(self, d1, mu):
        if d1 == 1:
            return self.D * mu['LH']
        return self.gL + self.D * (mu['HH'] + mu['LH'])

    def r2(self, nu, d1, beta, ehigh):
        """ehigh[S] in {0,1}: challenger-2 high-cost entry. Returns (status, node)."""
        rho = self.rho
        e = {S: rho + (1 - rho) * ehigh[S] for S in SIG}
        mu = {S: self.post(nu, beta, S) for S in SIG}
        V = {S: {s: self.base[d1][s] + e[S] * self.inc[d1][s] for s in ST} for S in SIG}
        P = {S: sum((mu[S][s] * V[S][s] for s in ST), iv.mpf(0)) for S in SIG}
        conds = []
        for S in SIG:
            gam = self.gain2(d1, mu[S]) - self.cH
            conds.append(gam if ehigh[S] == 1 else -gam)
        for s in ST:
            Pi = sum((self.pbuy[S] * (V[S][s] - P[S]) for S in SIG), iv.mpf(0)) - self.k
            conds.append(Pi if beta[s] == 1 else -Pi)
        # price separation: if the two posteriors differ, the two prices must differ (the challenger reads the signal)
        informative = any(beta[s].a != beta[u].a for s in ST for u in ST)
        gap = P['g'] - P['b']
        if informative:
            conds.append(gap if gap.a > 0 else -gap)
        status = 'CERTIFIED' if all(pos(c) for c in conds) else ('REFUTED' if any(neg(c) for c in conds[:-1] if informative) or (not informative and any(neg(c) for c in conds)) else 'UNDECIDED')
        margin = min(c.a for c in conds)
        W = {s: sum((self.psig(S, beta[s]) * V[S][s] for S in SIG), iv.mpf(0)) for s in ST}
        G1 = {s: sum((self.psig(S, beta[s]) * (self.g[s[0]] * (1 - e[S]) + (self.D if s == 'HL' else 0) * e[S])
                      for S in SIG), iv.mpf(0)) for s in ST}
        return status, dict(beta=beta, ehigh=ehigh, e=e, W=W, G1=G1, P=P, margin=margin, mu=mu, gap=gap)

    def r2_pooled_refuted(self, nu, d1, beta):
        """A pooled-price continuation for this investor profile: the challenger cannot tell the two signals
        apart, so it decides at the pooled belief, which is the round-2 prior nu.  Returns 'REFUTED' if the
        pooled entry is determined and some investor inequality certainly fails, else 'UNDECIDED'."""
        rho = self.rho
        gam = self.gain2(d1, nu) - self.cH
        if not (pos(gam) or neg(gam)):
            return 'UNDECIDED'
        e = iv.mpf(1) if pos(gam) else rho
        mu = {S: self.post(nu, beta, S) for S in SIG}
        V = {s: self.base[d1][s] + e * self.inc[d1][s] for s in ST}
        P = {S: sum((mu[S][s] * V[s] for s in ST), iv.mpf(0)) for S in SIG}
        for s in ST:
            Pi = sum((self.pbuy[S] * (V[s] - P[S]) for S in SIG), iv.mpf(0)) - self.k
            c = Pi if beta[s].a == 1 else -Pi
            if neg(c):
                return 'REFUTED'
        return 'UNDECIDED'

    def r2_pooling_excluded(self, nu, d1, beta):
        """True if, with a common entry probability at both signals (any value in [rho, 1]), the two prices
        certainly differ.  Then no pooled-price continuation exists for this investor profile."""
        rho = self.rho
        mu = {S: self.post(nu, beta, S) for S in SIG}
        gaps = []
        for e in (rho, iv.mpf(1)):
            P = {S: sum((mu[S][s] * (self.base[d1][s] + e * self.inc[d1][s]) for s in ST), iv.mpf(0)) for S in SIG}
            gaps.append(P['g'] - P['b'])
        return all(pos(g) for g in gaps) or all(neg(g) for g in gaps)

    def r1(self, alpha, e1high, cont):
        rho = self.rho
        e1 = {S: rho + (1 - rho) * e1high[S] for S in SIG}
        mu = {S: self.post(self.prior, alpha, S) for S in SIG}
        Y = {S: {s: e1[S] * cont[(S, 1)]['W'][s] + (1 - e1[S]) * cont[(S, 0)]['W'][s] for s in ST} for S in SIG}
        P = {S: sum((mu[S][s] * Y[S][s] for s in ST), iv.mpf(0)) for S in SIG}
        conds = []
        for S in SIG:
            gam = sum((mu[S][s] * cont[(S, 1)]['G1'][s] for s in ST), iv.mpf(0)) - self.cH
            conds.append(gam if e1high[S] == 1 else -gam)
        for s in ST:
            Pi = sum((self.pbuy[S] * (Y[S][s] - P[S]) for S in SIG), iv.mpf(0)) - self.k
            conds.append(Pi if alpha[s] == 1 else -Pi)
        status = 'CERTIFIED' if all(pos(c) for c in conds) else ('REFUTED' if any(neg(c) for c in conds) else 'UNDECIDED')
        gap = P['g'] - P['b']
        informative = any(alpha[s].a != alpha[u].a for s in ST for u in ST)
        if status == 'CERTIFIED' and informative and not (pos(gap) or neg(gap)):
            status = 'UNDECIDED'
        return status, min(c.a for c in conds), P


def run(r, cH, kappa='0'):
    m = IModel(r, cH, kappa)
    print(f'\n=== r = {r}, c_H = {cH}, kappa = {kappa} ===')
    zero, one = iv.mpf(0), iv.mpf(1)
    certified_r1 = []
    undecided = 0
    r2_report = {}
    pool_checked = [0]
    pool_open = []
    pool_refuted = [0]
    for prof in product((0, 1), repeat=4):
        alpha = {s: (one if v else zero) for s, v in zip(ST, prof)}
        mu1 = {S: m.post(m.prior, alpha, S) for S in SIG}
        cont_options = {}
        for S in SIG:
            for d in (0, 1):
                certs = []
                n_und = 0
                for bprof in product((0, 1), repeat=4):
                    beta = {s: (one if v else zero) for s, v in zip(ST, bprof)}
                    if len(set(bprof)) > 1:
                        pool_checked[0] += 1
                        if not m.r2_pooling_excluded(mu1[S], d, beta):
                            if m.r2_pooled_refuted(mu1[S], d, beta) != 'REFUTED':
                                pool_open.append((prof, S, d, bprof))
                            else:
                                pool_refuted[0] += 1
                    for eh in product((0, 1), repeat=2):
                        st, node = m.r2(mu1[S], d, beta, dict(zip(SIG, eh)))
                        if st == 'CERTIFIED':
                            certs.append(node)
                        elif st == 'UNDECIDED':
                            n_und += 1
                cont_options[(S, d)] = certs
                r2_report[(prof, S, d)] = (len(certs), n_und)
                undecided += n_und
        keys = [(S, d) for S in SIG for d in (0, 1)]
        if any(len(cont_options[kk]) == 0 for kk in keys):
            continue
        for sel in product(*[range(len(cont_options[kk])) for kk in keys]):
            cont = {kk: cont_options[kk][i] for kk, i in zip(keys, sel)}
            for e1h in product((0, 1), repeat=2):
                st, marg, P = m.r1(alpha, dict(zip(SIG, e1h)), cont)
                if st == 'CERTIFIED':
                    certified_r1.append((prof, e1h, cont, marg, P))
                elif st == 'UNDECIDED':
                    undecided += 1
    # round-2 uniqueness summary
    multi = {k_: v for k_, v in r2_report.items() if v[0] != 1}
    print(f'round-2 subgames after pure round-1 profiles: {len(r2_report)}; '
          f'with exactly one certified pure equilibrium: {len(r2_report) - len(multi)}')
    for k_, v in sorted(multi.items()):
        print(f'   profile {k_[0]} S1={k_[1]} d1={k_[2]}: certified pure equilibria {v[0]}, undecided candidates {v[1]}')
    print(f'undecided candidates in total (rounds 1 and 2): {undecided}')
    print(f'round-2 pooling: informative pure investor profiles checked {pool_checked[0]}; '
          f'pooled prices possible but the pooled candidate refuted for {pool_refuted[0]}; '
          f'pooled candidate not refuted for {len(pool_open)}')
    for item in pool_open[:5]:
        print('   pooling not excluded at', item)
    print(f'certified pure equilibria of the whole game: {len(certified_r1)}')
    for prof, e1h, cont, marg, P in certified_r1:
        print(f'  round-1 buyers {dict(zip(ST, prof))}, challenger-1 high-cost entry (g,b) = {e1h}, '
              f'smallest round-1 margin lower bound = {iv.nstr(marg, 8)}')
        print(f'    P1(g) = {iv.nstr(P["g"], 12)}, P1(b) = {iv.nstr(P["b"], 12)} (certified gap {iv.nstr(P["g"] - P["b"], 8)})')
        for kk in sorted(cont):
            c = cont[kk]
            print(f'    after S1={kk[0]}, d1={kk[1]}: buyers {[s for s in ST if c["beta"][s].a > 0.5]}, '
                  f'challenger-2 high-cost entry (g,b) = {(c["ehigh"]["g"], c["ehigh"]["b"])}, '
                  f'smallest margin lower bound = {iv.nstr(c["margin"], 8)}, price gap {iv.nstr(c["gap"], 6)}')


if __name__ == '__main__':
    for cH in ('5', '29/5'):
        for r in ('6/5', '3', '18/5'):
            run(r, cH)
    run('3', '5', '1/2')
