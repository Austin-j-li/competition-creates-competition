"""Print independent reserve calculations from the auction payment rule."""

from fractions import Fraction as F
from pathlib import Path
from hashlib import sha256
from math import factorial, isqrt
from datetime import datetime, timezone
import json
import mpmath as mp

mp.mp.dps = 60
ROOT = Path(__file__).resolve().parent
D = mp.mpf
H, L, RHO, CH, COST = D(10), D(1), D('0.25'), D(5), D('0.02')
A = mp.exp(-D('0.5'))
M, SMALL = 1 / (1 + A), A / (1 + A)


def auction(r, p):
    if p <= L:
        t0 = p * (1 - p / r)
        th = (r * r + p * p) / (2 * r)
        tl = L - (L * L - p * p) / (2 * r)
        return t0, th, tl, H - th, (L * L - p * p) / (2 * r)
    if p <= r:
        t0 = p * (1 - p / r)
        th = (r * r + p * p) / (2 * r)
        return t0, th, t0, H - th, D(0)
    return D(0), p, D(0), H - p, D(0)


def gain(r, p, mu):
    _, _, _, gh, gl = auction(r, p)
    return mu * gh + (1 - mu) * gl


def cap(r, mu, cost):
    b0 = gain(r, D(0), mu)
    if cost > b0:
        return None
    if cost == 0:
        return H
    if cost >= gain(r, L, mu):
        return mp.sqrt(2 * r * (b0 - cost))
    if cost >= gain(r, r, mu):
        return mp.sqrt(2 * r * (H - cost / mu) - r * r)
    return H - cost / mu


def reserve(r, mu, cl=D(0), high=CH):
    cuts = [(cap(r, mu, cl), RHO), (cap(r, mu, high), 1 - RHO)]
    pts = {D(0), L, r, H}
    pts.update(p for p, _ in cuts if p is not None)
    for e in (D(0), RHO, D(1)):
        if e < D(2) / 3:
            p = r * (1 - e) / (2 - 3 * e)
            if 0 < p < L:
                pts.add(p)
        z = e * mu
        if z < D(2) / 3:
            p = r * (1 - z) / (2 - 3 * z)
            if L < p < r:
                pts.add(p)
    rows = []
    for p in sorted(pts):
        e = sum(w for boundary, w in cuts if boundary is not None and p <= boundary)
        t0, th, tl, _, _ = auction(r, p)
        val = (1 - e) * t0 + e * (mu * th + (1 - mu) * tl)
        rows.append((val, p, e, th - tl))
    return max(rows, key=lambda row: (row[0], -row[1]))


def beliefs(beta):
    good = 1 + beta * (1 / A - 1)
    bad = 1 + beta * (A - 1)
    return good / (1 + good), bad / (1 + bad)


def buying(r, beta, cl=D(0)):
    good, bad = beliefs(beta)
    vg, pg, eg, dg = reserve(r, good, cl)
    vb, pb, eb, db = reserve(r, bad, cl)
    return M * eg * dg * (1 - good) + SMALL * eb * db * (1 - bad)


def show(label, *values):
    print(label, *(mp.nstr(v, 35) if not isinstance(v, str) else v for v in values))


def exact_certificate():
    e_lower = sum((F(1, 2) ** n / factorial(n) for n in range(21)), F(0))
    first_tail = F(1, 2) ** 21 / factorial(21)
    e_upper = e_lower + first_tail / (1 - F(1, 44))
    lo_m, hi_mu = 1 / (1 + e_upper), e_upper / (1 + e_upper)
    hi_m, lo_mu = 1 / (1 + e_lower), e_lower / (1 + e_lower)
    print('EXACT exp(1/2) enclosure', e_lower, e_upper)
    print('EXACT posterior enclosure', lo_m, hi_mu)
    for r in (F(6, 5), F(3)):
        delta = (r - 1) ** 2 / (2 * r)
        low_feasible = (F(5) - 1 / (2 * r)) / (F(10) - r / 2 - 1 / (2 * r))
        z = lo_m / 4
        ii_floor_max = r * (1 - 2 * z * z) / (2 * (2 - 3 * z))
        gaps = {
            'floor_I': lo_m * (F(10) - delta) / 4 - 3 * r / 16 - F(1, 4),
            'floor_II': F(5, 2) * lo_m - ii_floor_max,
            'entry_I': low_feasible * (F(5, 2) - delta) - 1,
            'entry_II': F(5) - r / 4 - (F(15, 2) - r / 4) * hi_mu,
            'entry_III': F(5) - F(15, 2) * hi_mu,
            'no_entry': F(5, 2) * lo_m - r / 4,
        }
        for name, gap in gaps.items():
            print('EXACT GAP', r, name, 'positive=', gap > 0, 'over_0.025=', gap > F(1, 40), 'decimal=', float(gap))
        if r == F(6, 5):
            tight_ii = F(5) - r / 4 - (F(15, 2) - r / 4) * (F(5) / (10 - r))
            gaps['entry_II'] = tight_ii
            print('EXACT cL=1 r=1.2 minimum competitor gap=', float(min(gaps.values()) - F(1, 4)),
                  'positive=', min(gaps.values()) > F(1, 4))
            print('EXACT cL=1 r=1.2 entry-II when cap exceeds r gap=',
                  float(F(5) / (10 - r) * (F(5, 2) - r) - F(1, 4)))
    print('EXACT fixed p=1/2, r=3', F(5, 12), F(37, 24), F(7, 8), F(203, 24), F(1, 8))
    ml, mh = F('0.37754066879814'), F('0.37754066879815')
    ul, uh = F('0.62245933120185'), F('0.62245933120186')
    print('EXACT coarse posterior enclosure valid=', ml < lo_m < hi_m < mh, ul < lo_mu < hi_mu < uh)
    zlo, zhi = ml / 4, mh / 4
    value_lo = 3 * (1 - 2 * zhi ** 2) / (2 * (2 - 3 * zlo))
    bad_p_hi = 3 * (1 - zhi) / (2 - 3 * zhi)
    print('EXACT cL=1 r=3 bad floor-II lower bound=', float(value_lo),
          'beats I=', value_lo > F(3, 4) + mh / 6,
          'beats extract=', value_lo > F(5, 2) * mh - F(1, 4),
          'beats no-entry=', value_lo > F(3, 4),
          'low preparation strict=', ml * (F(17, 2) - bad_p_hi ** 2 / 6) > 1,
          'expensive impossible=', F(1, 6) + F(25, 3) * mh < 5)
    scale = 10 ** 20
    p_square_lower, p_square_upper = 6 * (10 - 5 / ul) - 9, 6 * (10 - 5 / uh) - 9
    def sqrt_bounds(x):
        n = isqrt(x.numerator * scale * scale // x.denominator)
        return F(n, scale), F(n + 1, scale)
    pl, _ = sqrt_bounds(p_square_lower)
    _, ph = sqrt_bounds(p_square_upper)
    t0_lower = ph * (1 - ph / 3)
    ac_lo = 10 * ul - 5 + (1 - uh) * t0_lower
    zlo, zhi = ul / 4, uh / 4
    floor_ii_hi = 3 * (1 - 2 * zlo ** 2) / (2 * (2 - 3 * zhi))
    print('EXACT cL=1 r=3 good cap bounds=', float(pl), float(ph),
          'accommodation lower=', float(ac_lo),
          'beats I=', ac_lo > 1 + uh * F(2, 3),
          'beats floor I bound=', ac_lo > F(13, 16) + uh / 6,
          'beats floor II bound=', ac_lo > floor_ii_hi,
          'beats extraction=', ac_lo > F(5, 2) * uh - F(1, 4),
          'beats no-entry=', ac_lo > F(3, 4),
          'no expensive III=', uh * 7 < 5)
    print('EXACT cL=1 r=3 buying lower bound=', float(F(1, 6) * (lo_m * (1 - lo_m) + lo_m / 2)),
          'above k=', F(1, 6) * (lo_m * (1 - lo_m) + lo_m / 2) > F(1, 50))


def main():
    show('POSTERIORS a,m,M,good', A, SMALL, M, D('0.5'))
    exact_certificate()
    for r in (D('1.2'), D(3), D('3.6'), D(5), D(7), D(9)):
        for cl in (D(0), D('0.000001'), D('0.1'), D(1)):
            if r > 3 and cl > 0:
                continue
            for name, mu in (('m', SMALL), ('prior', D('0.5')), ('M', M)):
                row = reserve(r, mu, cl)
                show('SELLER r,cL,mu,V,p,e,spread', r, cl, name, *row)
            good = reserve(r, M, cl)
            bad = reserve(r, SMALL, cl)
            show('OUTCOME r,cL,proceeds,entry,ownership', r, cl, (good[0] + bad[0]) / 2,
                 (good[2] + bad[2]) / 2, (M * good[2] + SMALL * bad[2]) / 2)
            vals = [buying(r, D(i) / 100, cl) for i in range(101)]
            show('BUYING r,cL,K0,K1,min101', r, cl, vals[0], vals[-1], min(vals))
    p = cap(D(3), M, CH)
    t0, th, tl, _, _ = auction(D(3), p)
    show('ACCOMMODATION cap,S,exclusion,gap', p, M * th + (1 - M) * tl, RHO * M * H,
         RHO * M * H - M * th - (1 - M) * tl)
    show('OBSERVABLE r=3,M', RHO * M * H + (1 - RHO) * D(3) / 4)
    show('EXTRA boundK0,boundK1,bad_gain,cH6_max_gain', RHO * H * (M * SMALL + SMALL / 2),
         RHO * D(2) / 3 * (M * SMALL + SMALL / 2),
         gain(D(3), reserve(D(3), SMALL, D(1))[1], SMALL), gain(D(3), D(0), M))
    r = D('3.6')
    v, p, entry, _ = reserve(r, M)
    show('HIDDEN_SUNK r=3.6,M,original_p,entry,original_V,deviation_V', r, M, p, entry, v, entry * M * H)
    summary = {
        'date_utc': datetime.now(timezone.utc).isoformat(),
        'precision_digits': mp.mp.dps,
        'parameters': {'h': '10', 'ell': '1', 'rho': '0.25', 'cH': '5', 'k': '0.02', 'b': '2'},
        'script_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        'source_commit': '9b9bf3ce1a94d5017042192e61c9ceb800d310ba',
        'method': 'Finite stationary points and participation boundaries; exact rational bounds for all posteriors.',
    }
    original = ROOT.parent / 'C8_reserve'
    rerun = ROOT / 'original_rerun.txt'
    if rerun.exists():
        summary['original_output_sha256'] = sha256((original / 'output.txt').read_bytes()).hexdigest()
        summary['rerun_output_sha256'] = sha256(rerun.read_bytes()).hexdigest()
        summary['outputs_identical'] = (original / 'output.txt').read_bytes() == rerun.read_bytes()
        summary['original_script_sha256'] = sha256((original / 'c8_reserve.py').read_bytes()).hexdigest()
    (ROOT / 'receipt.json').write_text(json.dumps(summary, indent=2) + '\n')


if __name__ == '__main__':
    main()
