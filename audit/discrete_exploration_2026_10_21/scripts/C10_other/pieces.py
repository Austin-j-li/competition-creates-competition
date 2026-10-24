"""Exact piece structure of the branch-game outcome as a function of the prior phi.

Within a cell the entry profile and the equilibrium label are constant, and every outcome
(E, O_H, Pi) is LINEAR in phi.  Cell edges are: the three entry thresholds in odds
(a*T, T, T/a), the roots of G0 = 0 (two entry levels) and the roots of G1 = 0 (three profiles).
G0 and G1 are strictly decreasing in phi inside a profile, so each root is unique and found by bisection.
"""
from common import *
import branch


def odds_to_phi(w):
    return w / (1 + w)


def piece_values(par, A, lab, eg, eb, phi):
    """E, O_H, Pi at prior phi for the label and the entry profile (extends linearly)."""
    a = par.a
    beta = 1 if lab == 'FB' else 0
    q = branch.region_probs(phi, beta, a)
    E = eg * (q['gH'] + q['gL']) + eb * (q['bH'] + q['bL'])
    OH = eg * q['gH'] + eb * q['bH']
    return dict(E=E, OH=OH, Pi=A['t0'] + A['wL'] * E + A['DT'] * OH)


def G_profile(par, A, lab, eg, eb, phi, s=0):
    """Investor's gain from a unit at prior phi, profile (eg, eb), label (NT: schedules flat)."""
    a = par.a
    if lab == 'NT':
        return eg * A['DT'] * (1 - phi) - par.k
    mu_g, mu_b, q = branch.posteriors(phi, 1, a)
    return (1 / (1 + a)) * eg * A['DT'] * (1 - mu_g) + (a / (1 + a)) * eb * A['DT'] * (1 - mu_b) - par.k


def root_decreasing(f, lo, hi, iters=None):
    """Root of a strictly decreasing f on [lo, hi] if f(lo) > 0 > f(hi); else None."""
    iters = iters or (200 if MODE['m'] == 'hp' else 60)
    flo, fhi = f(lo), f(hi)
    if flo <= 0 or fhi >= 0:
        return None
    for _ in range(iters):
        mid = (lo + hi) / 2
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def structure(par, A, s=0):
    a, rho = par.a, par.rho
    t = tau(par, A, s)
    out = dict(tau=t)
    if not (0 < t < 1):
        out['thr'] = None
        return out
    T = t / (1 - t)
    thr = dict(aT=odds_to_phi(a * T), T=odds_to_phi(T), Ta=odds_to_phi(T / a))
    out['T'] = T
    out['thr'] = thr
    # profile intervals for FB: (rho,rho) on [0,aT), (1,rho) on [aT,T/a), (1,1) on [T/a,1]
    prof = [(rho, rho, K(0), thr['aT']), (K(1), rho, thr['aT'], thr['Ta']), (K(1), K(1), thr['Ta'], K(1))]
    roots = []
    G1roots = []
    for eg, eb, lo, hi in prof:
        f = lambda x, eg=eg, eb=eb: G_profile(par, A, 'FB', eg, eb, x, s)
        # tiny offsets keep the endpoints inside the open interval for the sign test
        r = root_decreasing(f, lo, hi)
        G1roots.append(r)
        if r is not None:
            roots.append(r)
    G0roots = []
    for e, lo, hi in ((rho, K(0), thr['T']), (K(1), thr['T'], K(1))):
        f = lambda x, e=e: G_profile(par, A, 'NT', e, e, x, s)
        r = root_decreasing(f, lo, hi)
        G0roots.append(r)
        if r is not None:
            roots.append(r)
    out['G1roots'] = G1roots
    out['G0roots'] = G0roots
    edges = sorted(set([K(0), K(1), thr['aT'], thr['T'], thr['Ta']] + roots))
    out['edges'] = edges
    return out


def cells(par, A, sel, s=0):
    """List of cells: dict(lo, hi, lab, eg, eb) with a constant equilibrium selection."""
    st = structure(par, A, s)
    if st['thr'] is None:
        return None, st
    edges = st['edges']
    a, rho = par.a, par.rho
    T = st['T']
    cs = []
    for i in range(len(edges) - 1):
        lo, hi = edges[i], edges[i + 1]
        if hi - lo <= K(1, 10 ** 40) if MODE['m'] == 'hp' else hi == lo:
            continue
        mid = (lo + hi) / 2
        v = _select_at(par, A, mid, sel, s)
        if v is None:
            cs.append(dict(lo=lo, hi=hi, lab='GAP', eg=None, eb=None))
        else:
            cs.append(dict(lo=lo, hi=hi, lab=v[0], eg=v[1]['eg'], eb=v[1]['eb']))
    return cs, st


def _select_at(par, A, phi, sel, s=0):
    eqs, G0, G1 = branch.equilibria(par, A, phi, s)
    if not eqs:
        return None
    if len(eqs) == 1:
        return eqs[0]
    d = dict(eqs)
    if sel == 'inf':
        return ('FB', d['FB'])
    if sel == 'nt':
        return ('NT', d['NT'])
    key = (lambda t: t[1]['Pi'])
    return max(eqs, key=key) if sel == 'best' else min(eqs, key=key)


def hull_points(par, A, sel, s=0):
    """Vertices (phi, Pi, tag) for the upper hull: both one-sided limits at every cell edge."""
    cs, st = cells(par, A, sel, s)
    if cs is None:
        return None, st, None
    pts = []
    for c in cs:
        if c['lab'] == 'GAP':
            continue
        for ph, side in ((c['lo'], 'R'), (c['hi'], 'L')):
            v = piece_values(par, A, c['lab'], c['eg'], c['eb'], ph)
            pts.append((ph, v['Pi'], f"{c['lab']}({mp.nstr(c['eg'],3)},{mp.nstr(c['eb'],3)}){side}", c, v))
    return pts, st, cs


def upper_hull(points):
    pts = sorted(points, key=lambda t: (t[0], t[1]))
    hull = []
    for p in pts:
        while len(hull) >= 2:
            (x1, y1), (x2, y2) = hull[-2][:2], hull[-1][:2]
            if (x2 - x1) * (p[1] - y1) - (y2 - y1) * (p[0] - x1) >= 0:
                hull.pop()
            else:
                break
        hull.append(p)
    return hull


def policy_at(hull, pi):
    """Return (value, left vertex, right vertex, weight on right)."""
    for i in range(len(hull) - 1):
        x1, y1 = hull[i][:2]
        x2, y2 = hull[i + 1][:2]
        if x1 <= pi <= x2:
            w = (pi - x1) / (x2 - x1)
            return (1 - w) * y1 + w * y2, hull[i], hull[i + 1], w
    return None
