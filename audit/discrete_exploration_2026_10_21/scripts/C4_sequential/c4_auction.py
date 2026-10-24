"""C4: auction objects with an incumbent R ~ U[0, r] and up to two challengers with values in {l, h}.

Print-only. Closed forms are compared with direct numerical integration over R.
Second-price auction with reserve p; equal highest bids are broken at random.
Run from the repository root:
    .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/C4_sequential/c4_auction.py
"""
from scipy.integrate import quad

h, l, p = 10.0, 1.0, 0.5


def outcome(vals):
    """vals: dict name -> value. Returns (payment to target, dict of expected surplus, allocation value)."""
    adm = {k: v for k, v in vals.items() if v >= p}
    surplus = {k: 0.0 for k in vals}
    if not adm:
        return 0.0, surplus, 0.0
    top = max(adm.values())
    winners = [k for k, v in adm.items() if v == top]
    others = sorted([v for k, v in adm.items() if k not in winners], reverse=True)
    if len(winners) >= 2:
        pay = top
    else:
        pay = max(p, others[0]) if others else p
    for w in winners:
        surplus[w] = (top - pay) / len(winners)
    return pay, surplus, top


def integrate(r, chal):
    """chal: dict of prepared challengers name -> value. Integrate over R ~ U[0, r]."""
    names = ['inc'] + list(chal)
    brk = sorted({x for x in [p, l] if 0 < x < r})

    def f(R, what, name=None):
        vals = {'inc': R}
        vals.update(chal)
        pay, sur, top = outcome(vals)
        if what == 'pay':
            return pay
        if what == 'alloc':
            return top
        return sur[name]

    out = {}
    out['pay'] = quad(lambda R: f(R, 'pay'), 0, r, points=brk, limit=200)[0] / r
    out['alloc'] = quad(lambda R: f(R, 'alloc'), 0, r, points=brk, limit=200)[0] / r
    for n in names:
        out['sur_' + n] = quad(lambda R, n=n: f(R, 'sur', n), 0, r, points=brk, limit=200)[0] / r
    return out


def closed(r):
    t0 = p * (1 - p / r)
    tH = r / 2 + p**2 / (2 * r)
    tL = l - (l**2 - p**2) / (2 * r)
    gH = h - tH
    gL = (l**2 - p**2) / (2 * r)
    DT = (r - l)**2 / (2 * r)
    D = gH - gL
    return dict(t0=t0, tH=tH, tL=tL, gH=gH, gL=gL, DT=DT, D=D,
                T_HH=h, T_HL=l + DT, T_LH=l + DT, T_LL=l,
                A0=(r**2 - p**2) / (2 * r), Al=l + DT, Ah=h)


def main():
    print('C4 auction objects: closed forms against direct integration (h=10, l=1, p=0.5)')
    worst = 0.0
    for r in [1.2, 2.0, 3.0, 3.6, 4.2, 6.0]:
        c = closed(r)
        print(f'\nr = {r}')
        print('  t0={t0:.9f} tH={tH:.9f} tL={tL:.9f} gH={gH:.9f} gL={gL:.9f} DT={DT:.9f} D_r=gH-gL={D:.9f}'.format(**c))
        print(f'  split identity DT + (gH-gL) - (h-l) = {c["DT"] + c["D"] - (h - l):.2e}')
        vh = {'H': h, 'L': l}
        rows = []
        # no challenger
        o = integrate(r, {})
        rows.append(('none', o['pay'], c['t0'], {}, o))
        # one challenger
        for j1 in 'HL':
            o = integrate(r, {'c1': vh[j1]})
            rows.append((f'only {j1}', o['pay'], c['t' + j1], {'c1': c['g' + j1]}, o))
        # two challengers
        G = {('H', 'H'): (0.0, 0.0), ('H', 'L'): (c['D'], 0.0), ('L', 'H'): (0.0, c['D']), ('L', 'L'): (0.0, 0.0)}
        for j1 in 'HL':
            for j2 in 'HL':
                o = integrate(r, {'c1': vh[j1], 'c2': vh[j2]})
                g1, g2 = G[(j1, j2)]
                rows.append((f'both {j1}{j2}', o['pay'], c['T_' + j1 + j2], {'c1': g1, 'c2': g2}, o))
        for name, pay_num, pay_cf, gains, o in rows:
            err = abs(pay_num - pay_cf)
            for k_, g in gains.items():
                err = max(err, abs(o['sur_' + k_] - g))
            tot = o['pay'] + sum(o[k_] for k_ in o if k_.startswith('sur_'))
            ident = abs(tot - o['alloc'])
            worst = max(worst, err, ident)
            gtxt = ' '.join(f'{k_[4:]}:{o[k_]:.6f}' for k_ in o if k_.startswith('sur_'))
            print(f'  {name:8s} proceeds num={pay_num:.9f} closed={pay_cf:.9f} | surplus {gtxt} | '
                  f'alloc={o["alloc"]:.6f} | max|err|={err:.1e} | proceeds+surplus-alloc={ident:.1e}')
        # allocation value checks
        print(f'  allocation closed forms: none={c["A0"]:.6f} max-class-l={c["Al"]:.6f} max-class-h={c["Ah"]:.6f}')
        # spread-rent table
        print('  spread across challenger 2 class, given challenger 1:')
        print(f'    challenger 1 absent : T(H)-T(L) = tH-tL = {c["tH"] - c["tL"]:.6f}; gains of c2 (H,L) = ({c["gH"]:.6f}, {c["gL"]:.6f})')
        print(f'    challenger 1 class H: T_HH-T_HL = {c["T_HH"] - c["T_HL"]:.6f} (= D_r {c["D"]:.6f}); gains of c2 (H,L) = (0, 0)')
        print(f'    challenger 1 class L: T_LH-T_LL = {c["T_LH"] - c["T_LL"]:.6f} (= DT {c["DT"]:.6f}); gains of c2 (H,L) = ({c["D"]:.6f}, 0)')
        # increments of proceeds from challenger 2's entry, given challenger 1 prepared
        print('  proceeds increment from challenger 2 entry, given challenger 1 prepared:')
        print(f'    HH: h - tH = {h - c["tH"]:.6f} (gH {c["gH"]:.6f}); HL: T_HL - tH = {c["T_HL"] - c["tH"]:.6f} (gL {c["gL"]:.6f}); '
              f'LH: T_LH - tL = {c["T_LH"] - c["tL"]:.6f} (DT+gL {c["DT"] + c["gL"]:.6f}); LL: l - tL = {l - c["tL"]:.6f} (gL {c["gL"]:.6f})')
    print(f'\nlargest discrepancy over all cells and strengths: {worst:.2e}')


if __name__ == '__main__':
    main()
