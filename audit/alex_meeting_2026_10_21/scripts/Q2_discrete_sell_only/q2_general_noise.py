#!/usr/bin/env python3
"""General three-point noise (pi_-, pi_0, pi_+): equilibrium finder (print-only).

Memo: audit/alex_meeting_2026_10_21/memos/Q2_discrete_sell_only.md, Claim 10.

The non-trading type never trades (memo Claim 2), so a candidate is the
trading probability s in [0, 1] of the trading type (L in the sell-only menu,
H in the buy-only menu).  For each s the script builds the posteriors, the
flow-measurable entry and price schedule, and the trader's net payoff U(s).
Equilibria are:
  * s = 0 with U(0) <= 0 (Intuitive-Criterion belief at the off-path flow);
  * s = 1 with U(1) >= 0;
  * interior roots of U on intervals where the entry pattern is constant;
  * "jump" points s_hat where a camouflage posterior equals a preparation
    threshold and U jumps across zero.  These need the indifferent
    challenger to mix, which the paper's tie rule does not allow.
Every number printed is a numerical diagnostic.  No assertion is made.

Run:  .venv/bin/python audit/alex_meeting_2026_10_21/scripts/Q2_discrete_sell_only/q2_general_noise.py
"""
import numpy as np
from scipy.optimize import brentq

BENCH = dict(h=10.0, l=1.0, p=0.5, rho=0.25, cL=1.0, cH=6.0, k=0.02)
FLOWS = {'sell': (-2, -1, 0, 1), 'buy': (-1, 0, 1, 2)}
TOL = 1e-12


def auction(par, r):
    h, l, p = par['h'], par['l'], par['p']
    return dict(t0=p * (1 - p / r), tH=r / 2 + p * p / (2 * r),
                tL=l - (l * l - p * p) / (2 * r),
                gH=h - r / 2 - p * p / (2 * r), gL=(l * l - p * p) / (2 * r),
                DT=(r - l) ** 2 / (2 * r))


class Economy:
    def __init__(self, par, r, menu, noise, lam=1.0):
        self.par, self.r, self.menu = par, r, menu
        self.noise, self.lam = tuple(noise), lam
        self.a = a = auction(par, r)
        span = a['gH'] - a['gL']
        self.tauL = (par['cL'] - a['gL']) / span
        self.tauH = (par['cH'] - a['gL']) / span
        self.step = -1 if menu == 'sell' else 1
        self.trader = 'L' if menu == 'sell' else 'H'

    def law(self, theta, s):
        sig = self.lam * s if theta == self.trader else 0.0
        out = {x: 0.0 for x in FLOWS[self.menu]}
        for z, pz in zip((-1, 0, 1), self.noise):
            out[z] += (1 - sig) * pz
            out[z + self.step] += sig * pz
        return out

    def posteriors(self, s):
        lH, lL = self.law('H', s), self.law('L', s)
        mu, on = {}, {}
        for x in FLOWS[self.menu]:
            tot = lH[x] + lL[x]
            if tot > TOL:
                mu[x], on[x] = lH[x] / tot, True
            else:  # Intuitive Criterion: the flow is reached only by the trader
                mu[x], on[x] = (0.0 if self.menu == 'sell' else 1.0), False
        return mu, on, lH, lL

    def entry_at(self, mu, override=None, x=None):
        if override is not None and x in override:
            return override[x]
        e = 0.0
        if mu >= self.tauL - TOL:
            e += self.par['rho']
        if mu >= self.tauH - TOL:
            e += 1 - self.par['rho']
        return e

    def evaluate(self, s, override=None):
        mu, on, lH, lL = self.posteriors(s)
        a = self.a
        e = {x: self.entry_at(mu[x], override, x) for x in mu}
        U = {}
        for th in ('H', 'L'):
            g = 0.0
            for z, pz in zip((-1, 0, 1), self.noise):
                x = z + self.step  # both types face the same one-directional menu
                g += pz * self.step * e[x] * a['DT'] * ((1.0 if th == 'H' else 0.0) - mu[x])
            U[th] = g - self.par['k']
        E = 0.5 * sum((lH[x] + lL[x]) * e[x] for x in mu)
        OH = 0.5 * sum(lH[x] * e[x] for x in mu)
        zero = [x for x in mu if on[x] and e[x] == 0.0]
        pooled, ok = None, True
        if len({round(mu[x], 12) for x in zero}) > 1:
            mH = sum(lH[x] for x in zero)
            mL = sum(lL[x] for x in zero)
            pooled = mH / (mH + mL)
            ok = self.entry_at(pooled) == 0.0
        return dict(mu=mu, on=on, e=e, U=U, E=E, OH=OH, pooled=pooled, pool_ok=ok)

    def Utr(self, s, override=None):
        return self.evaluate(s, override)['U'][self.trader]

    def breakpoints(self):
        """s in (0,1) where an on-path posterior equals tau_L or tau_H.

        Each conditional flow law is affine in s, Pr(x|theta) = A + s*D, so
        mu(x; s) = tau is a linear equation in s.
        """
        lH0, lL0 = self.law('H', 0.0), self.law('L', 0.0)
        lH1, lL1 = self.law('H', 1.0), self.law('L', 1.0)
        pts = []
        for x in FLOWS[self.menu]:
            AH, DH = lH0[x], lH1[x] - lH0[x]
            AL, DL = lL0[x], lL1[x] - lL0[x]
            for tau in (self.tauL, self.tauH):
                if not 0.0 < tau < 1.0:
                    continue
                coef = (1 - tau) * DH - tau * DL
                rhs = tau * AL - (1 - tau) * AH
                if abs(coef) < TOL:
                    continue
                sh = rhs / coef
                if 1e-9 < sh < 1 - 1e-9:
                    pts.append((sh, x, tau))
        return sorted(pts)

    def equilibria(self):
        eqs = []
        if self.Utr(0.0) <= 0:
            eqs.append(('pure', 0.0, None))
        if self.Utr(1.0) >= 0:
            eqs.append(('pure', 1.0, None))
        bps = self.breakpoints()
        cuts = [0.0] + [b[0] for b in bps] + [1.0]
        for lo, hi in zip(cuts[:-1], cuts[1:]):
            if hi - lo < 1e-9:
                continue
            ss = np.linspace(lo + 1e-9, hi - 1e-9, 401)
            vals = [self.Utr(s) for s in ss]
            for i in range(len(ss) - 1):
                if vals[i] * vals[i + 1] < 0:
                    root = brentq(self.Utr, ss[i], ss[i + 1], xtol=1e-14)
                    eqs.append(('mixed (investor)', root, None))
        for sh, x, tau in bps:
            left, right = self.Utr(sh - 1e-9), self.Utr(sh + 1e-9)
            if min(left, right) < 0 < max(left, right):
                # challenger mixes at flow x; entry there moves between levels
                mu_x = self.posteriors(sh)[0][x]
                lo_e = self.entry_at(mu_x - 1e-7)
                hi_e = self.entry_at(mu_x + 1e-7)
                ulo = self.Utr(sh, {x: lo_e})
                uhi = self.Utr(sh, {x: hi_e})
                if (ulo - uhi) != 0:
                    w = ulo / (ulo - uhi)
                    e_mix = lo_e + w * (hi_e - lo_e)
                    eqs.append(('jump (challenger mixes)', sh, (x, tau, e_mix)))
        return eqs


def fmt(v, nd=4):
    return f"{v:.{nd}f}"


def describe(econ, kind, s, extra):
    override = None if extra is None else {extra[0]: extra[2]}
    ev = econ.evaluate(s, override)
    other = 'H' if econ.trader == 'L' else 'L'
    flows = FLOWS[econ.menu]
    post = " ".join(f"{x}:{fmt(ev['mu'][x], 3)}{'' if ev['on'][x] else '*'}" for x in flows)
    ent = " ".join(f"{x}:{fmt(ev['e'][x], 3)}" for x in flows)
    s = float(s)
    line = (f"    {kind:24s} s={fmt(s, 6)}  E={fmt(ev['E'])}  O_H={fmt(ev['OH'])}  "
            f"U_{other}(trade)={fmt(ev['U'][other])}")
    if extra is not None:
        line += f"  [mixing at X={extra[0]}, tau={fmt(extra[1])}, entry there={fmt(extra[2])}]"
    if not ev['pool_ok']:
        line += "  [zero-entry pool inconsistent]"
    print(line)
    print(f"      posteriors {post}")
    print(f"      entry      {ent}")


def run(label, par, r, menu, noise, lam=1.0, show_U=True):
    econ = Economy(par, r, menu, noise, lam)
    print(f"\n[{label}] menu={menu} r={r} noise={noise} lam={lam} "
          f"tau_L={fmt(econ.tauL)} tau_H={fmt(econ.tauH)} Delta_T={fmt(econ.a['DT'])} k={par['k']}")
    if show_U:
        ss = [0.0, 0.25, 0.5, 0.75, 1.0]
        print("    U_trader(s): " + "  ".join(f"s={s}: {fmt(econ.Utr(s), 5)}" for s in ss))
    bps = econ.breakpoints()
    if bps:
        print("    entry breakpoints: " + ", ".join(f"s={fmt(b[0])} (X={b[1]}, tau={fmt(b[2])})" for b in bps))
    eqs = econ.equilibria()
    if not eqs:
        print("    no equilibrium found")
    for kind, s, extra in eqs:
        describe(econ, kind, s, extra)
    return eqs


def sweep(label, par, menu, noise, rs, lam=1.0):
    """Group strengths r by the equilibrium pattern and print each r-range.

    Pattern = (number of equilibria under the tie rule, number that need the
    challenger to mix, which pure profiles exist, entry at each pure profile).
    """
    print(f"\n[{label}] sweep over r: menu={menu} noise={noise} costs (c_L, c_H)=({par['cL']}, {par['cH']}) k={par['k']}")
    rows = []
    for r in rs:
        econ = Economy(par, r, menu, noise, lam)
        eqs = econ.equilibria()
        tie_ok = [e for e in eqs if not e[0].startswith('jump')]
        pures = tuple(sorted(s for kind, s, _ in eqs if kind == 'pure'))
        ent = {s: econ.evaluate(s)['E'] for s in pures}
        key = (len(tie_ok), len(eqs) - len(tie_ok), pures,
               tuple(round(ent[s], 6) for s in pures))
        if rows and rows[-1][2] == key:
            rows[-1][1] = r
        else:
            rows.append([r, r, key, ent])
    for r_lo, r_hi, key, ent in rows:
        pure_txt = ", ".join(f"s={s:g} (E={ent[s]:.4f})" for s in key[2]) or "none"
        print(f"    r in [{r_lo:.3f}, {r_hi:.3f}]: {key[0]} equilibria under the tie rule "
              f"(pure: {pure_txt}; {key[0] - len(key[2])} with investor mixing), "
              f"{key[1]} more that need the challenger to mix")


def main():
    par = dict(BENCH)
    third = (1 / 3, 1 / 3, 1 / 3)
    print("General-noise equilibrium finder.  Benchmark costs unless stated.")

    print("\n--- E1. Leading case cross-check (equal probabilities) ---")
    for r in (1.2, 3.0, 9.0):
        run('E1', par, r, 'sell', third)

    print("\n--- E2. Symmetric unimodal noise (1/4, 1/2, 1/4) ---")
    for r in (1.2, 3.0, 9.0):
        run('E2', par, r, 'sell', (0.25, 0.5, 0.25))
    sweep('E2-sell', par, 'sell', (0.25, 0.5, 0.25), np.arange(1.01, 9.995, 0.005))
    sweep('E2-buy', par, 'buy', (0.25, 0.5, 0.25), np.arange(1.01, 9.995, 0.005))
    sweep('E1-sell (equal noise)', par, 'sell', (1 / 3, 1 / 3, 1 / 3), np.arange(1.01, 9.995, 0.005))

    print("\n--- E3. Recruitment at a camouflage flow: noise (0.2, 0.6, 0.2), r = 1.7 ---")
    run('E3-sell', par, 1.7, 'sell', (0.2, 0.6, 0.2))
    run('E3-buy', par, 1.7, 'buy', (0.2, 0.6, 0.2))
    sweep('E3-sell', par, 'sell', (0.2, 0.6, 0.2), np.arange(1.01, 9.995, 0.005))
    sweep('E3-buy', par, 'buy', (0.2, 0.6, 0.2), np.arange(1.01, 9.995, 0.005))

    print("\n--- E4. Information complementarity without entry feedback: noise (0.4, 0.4, 0.2), c_H = 7, r = 2 ---")
    par4 = dict(par, cH=7.0)
    run('E4-sell', par4, 2.0, 'sell', (0.4, 0.4, 0.2))
    run('E4-buy', par4, 2.0, 'buy', (0.4, 0.4, 0.2))
    sweep('E4-sell', par4, 'sell', (0.4, 0.4, 0.2), np.arange(1.01, 9.995, 0.005))
    sweep('E4-buy', par4, 'buy', (0.4, 0.4, 0.2), np.arange(1.01, 9.995, 0.005))

    print("\n--- E5. Deterrence at a camouflage flow (EGJ channel): noise (0.2, 0.6, 0.2), "
          "c_L = 2.5, c_H = 7, r = 3, k = 0.03 ---")
    par5 = dict(par, cL=2.5, cH=7.0, k=0.03)
    run('E5-sell', par5, 3.0, 'sell', (0.2, 0.6, 0.2))
    run('E5-sell, k = 0.02', dict(par5, k=0.02), 3.0, 'sell', (0.2, 0.6, 0.2))

    print("\n--- E6. Full-trading payoffs coincide across menus (Bayes identity), any noise ---")
    for noise in (third, (0.25, 0.5, 0.25), (0.4, 0.4, 0.2), (0.1, 0.3, 0.6)):
        es = Economy(par, 3.0, 'sell', noise)
        eb = Economy(par, 3.0, 'buy', noise)
        print(f"    noise={noise}: sell-only U_L(1)={fmt(es.Utr(1.0), 6)}  buy-only U_H(1)={fmt(eb.Utr(1.0), 6)}"
              f"  | no-trade deviation: sell U_L(0)={fmt(es.Utr(0.0), 6)}  buy U_H(0)={fmt(eb.Utr(0.0), 6)}")


if __name__ == '__main__':
    main()
