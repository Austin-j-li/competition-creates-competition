"""C4: uniqueness over mixed strategies at the weak incumbent r0 = 6/5 (kappa = 0). Print-only.

Analytical steps (memo, Results 4-6) pin everything except investor 1's purchase probabilities
(alpha_HL, alpha_LH) in [0,1]^2:
  * (NC) holds, so challenger 2 enters with prob. rho after d1 = 1, and W_s(S1, 1) = V_s (constants);
  * after d1 = 1 only HH buys (LL, LH never; HL never because nu_min * rho * D_r > (1 - nu_min) * DT);
  * after d1 = 0 nobody trades because DT(r0) < k, so challenger 2 decides at the round-1 posterior;
  * in round 1, HH buys and LL does not.
This script covers [0,1]^2 by interval boxes.  On each box it encloses the round-1 posteriors, every
admissible entry response (an entry probability is the interval [rho, 1] at both signals unless the gain
is certainly below c_H at both signals; this hull also covers challenger mixing at ties and pooled prices), and the purchase margins
of HL and LH.  A box is closed when both margins are certainly negative: then no equilibrium has
alpha_HL > 0 or alpha_LH > 0 inside it.  Boxes are split until closed or until a depth limit.
Run from the repository root:
    .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/C4_sequential/c4_unique_r0.py
"""
from fractions import Fraction as F

from mpmath import iv

iv.dps = 30
ST = ('HH', 'HL', 'LH', 'LL')


def I(fr):
    fr = F(fr)
    return iv.mpf(fr.numerator) / iv.mpf(fr.denominator)


def setup(r, cH):
    h, l, p, rho, k = I(10), I(1), I('1/2'), I('1/4'), I('1/50')
    r = I(r)
    a = iv.exp(-1 / I(2))
    t0 = p * (1 - p / r)
    tH = r / 2 + p * p / (2 * r)
    tL = l - (l * l - p * p) / (2 * r)
    gH = h - tH
    gL = (l * l - p * p) / (2 * r)
    DT = (r - l) ** 2 / (2 * r)
    D = gH - gL
    t = {'H': tH, 'L': tL}
    V = {'HH': tH + rho * gH, 'HL': tH + rho * gL, 'LH': tL + rho * (DT + gL), 'LL': tL + rho * gL}
    G1 = {'HH': (1 - rho) * gH, 'HL': (1 - rho) * gH + rho * D, 'LH': (1 - rho) * gL, 'LL': (1 - rho) * gL}
    return dict(a=a, rho=rho, k=k, cH=I(cH), t0=t0, t=t, gL=gL, D=D, DT=DT, V=V, G1=G1,
                prior={s: I('1/4') for s in ST}, pbuy={'g': 1 / (1 + a), 'b': a / (1 + a)})


def pin_checks(c):
    a, rho, D, DT, k = c['a'], c['rho'], c['D'], c['DT'], c['k']
    q = I('1/4')
    nu_min = q * a * a / (q * a * a + (1 - q))
    print('  pinned steps (each must be a certain inequality):')
    print(f'    NC: c_H - psi2(1/4) D_r = {iv.nstr(c["cH"] - D * q / (q + a * a * (1 - q)), 8)}  (> 0)')
    print(f'    round 2 after d1=0, no trade: k - DT = {iv.nstr(k - DT, 8)}  (> 0)')
    print(f'    round 2 after d1=1, HH buys: (1 - psi2) rho D_r - k = {iv.nstr((1 - q / (q + a * a * (1 - q))) * rho * D - k, 8)}  (> 0)')
    print(f'    round 2 after d1=1, HL never: nu_min rho D_r - (1 - nu_min) DT = {iv.nstr(nu_min * rho * D - (1 - nu_min) * DT, 8)}  (> 0)')
    print(f'    round 2 after d1=1, LH never: a^2[(1-rho)DT + rho D_r] - rho DT = {iv.nstr(a * a * ((1 - rho) * DT + rho * D) - rho * DT, 8)}  (> 0)')
    print(f'    round 1, HH buys: rho^2 (1 - psi1(1/4)) D_r - k = {iv.nstr(rho * rho * (1 - q / (q + a * (1 - q))) * D - k, 8)}  (> 0)')


def margins(c, X, Y):
    a, rho = c['a'], c['rho']
    beta = {'HH': iv.mpf(1), 'HL': X, 'LH': Y, 'LL': iv.mpf(0)}
    out = {}
    e1s, e2s = {}, {}
    mus = {}
    for S in ('g', 'b'):
        P = {}
        for s in ST:
            pg = (a + beta[s] * (1 - a)) / (1 + a)
            P[s] = pg if S == 'g' else 1 - pg
        z = sum((c['prior'][s] * P[s] for s in ST), iv.mpf(0))
        mu = {s: c['prior'][s] * P[s] / z for s in ST}
        # tighter enclosure of each posterior: mu_s = 1 / (1 + sum_{s'} pi_s' P_s' / (pi_s P_s))
        for s in ST:
            rest = sum((c['prior'][u] * P[u] for u in ST if u != s), iv.mpf(0))
            alt = 1 / (1 + rest / (c['prior'][s] * P[s]))
            lo = max(mu[s].a, alt.a)
            hi = min(mu[s].b, alt.b)
            mu[s] = iv.mpf([lo, hi])
        mus[S] = mu
    # entry hulls: rho at both signals only if the gain is certainly below c_H at both signals
    # (a pooled price gives a convex combination of the two gains, so this also covers pooling)
    gam1 = {S: sum((mus[S][s] * c['G1'][s] for s in ST), iv.mpf(0)) for S in ('g', 'b')}
    B2 = {S: c['gL'] + c['D'] * (mus[S]['HH'] + mus[S]['LH']) for S in ('g', 'b')}
    low1 = all(gam1[S].b < c['cH'] for S in ('g', 'b'))
    low2 = all(B2[S].b < c['cH'] for S in ('g', 'b'))
    for S in ('g', 'b'):
        e1s[S] = iv.mpf([rho, rho]) if low1 else iv.mpf([rho, 1])
        e2s[S] = iv.mpf([rho, rho]) if low2 else iv.mpf([rho, 1])
    for s in ('HL', 'LH'):
        tot = iv.mpf(0)
        for S in ('g', 'b'):
            e1, e2 = e1s[S], e2s[S]
            diff = iv.mpf(0)
            for u in ST:
                if u == s:
                    continue
                dV = c['V'][s] - c['V'][u]
                dW = e2 * (c['t'][s[1]] - c['t'][u[1]])
                diff += mus[S][u] * (e1 * dV + (1 - e1) * dW)
            tot += c['pbuy'][S] * diff
        out[s] = tot - c['k']
    return out


def run(r, cH, max_depth=14):
    c = setup(r, cH)
    print(f'\n=== r = {r}, c_H = {cH}, kappa = 0 ===')
    pin_checks(c)
    stack = [(F(0), F(1), F(0), F(1), 0)]
    closed = 0
    open_boxes = []
    worst = {'HL': -1e9, 'LH': -1e9}
    while stack:
        x0, x1, y0, y1, d = stack.pop()
        m = margins(c, iv.mpf([I(x0).a, I(x1).b]), iv.mpf([I(y0).a, I(y1).b]))
        if m['HL'].b < 0 and m['LH'].b < 0:
            closed += 1
            worst['HL'] = max(worst['HL'], float(m['HL'].b))
            worst['LH'] = max(worst['LH'], float(m['LH'].b))
            continue
        if d >= max_depth:
            open_boxes.append((x0, x1, y0, y1, m))
            continue
        xm, ym = (x0 + x1) / 2, (y0 + y1) / 2
        stack += [(x0, xm, y0, ym, d + 1), (xm, x1, y0, ym, d + 1), (x0, xm, ym, y1, d + 1), (xm, x1, ym, y1, d + 1)]
    print(f'  boxes closed: {closed}; boxes left open at depth {max_depth}: {len(open_boxes)}')
    print(f'  largest certified upper bound of the margins on closed boxes: HL {worst["HL"]:.6f}, LH {worst["LH"]:.6f}')
    for x0, x1, y0, y1, m in open_boxes[:10]:
        print(f'   open box alpha_HL in [{float(x0):.5f},{float(x1):.5f}], alpha_LH in [{float(y0):.5f},{float(y1):.5f}]: '
              f'margin HL {iv.nstr(m["HL"], 6)}, LH {iv.nstr(m["LH"], 6)}')
    if not open_boxes:
        print('  result: every equilibrium has alpha_HL = alpha_LH = 0 in round 1.')


if __name__ == '__main__':
    run('6/5', '5')
    run('6/5', '29/5')
