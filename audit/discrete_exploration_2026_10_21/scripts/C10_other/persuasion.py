"""Target disclosure as persuasion over branch priors (discrete-Laplace, buy-only).

A disclosure policy is a distribution of public branch priors phi with mean pi.
Branch outcome: pure equilibrium of the trading stage at phi (see branch.py).
Selection rules when NT and FB both exist:
  'inf'  : full buying (the informative equilibrium)
  'nt'   : no trade
  'best' : the one with the higher target proceeds
  'worst': the one with the lower target proceeds
If no pure equilibrium exists the branch is 'GAP' (an interior mixture is needed; reported, not used).
"""
from common import *
import branch


def branch_value(par, A, phi, sel, s=0):
    eqs, G0, G1 = branch.equilibria(par, A, phi, s)
    if not eqs:
        return None
    if len(eqs) == 1:
        lab, o = eqs[0]
    else:
        d = dict(eqs)
        if sel == 'inf':
            lab, o = 'FB', d['FB']
        elif sel == 'nt':
            lab, o = 'NT', d['NT']
        elif sel == 'best':
            lab, o = max(eqs, key=lambda t: t[1]['Pi'])
        else:
            lab, o = min(eqs, key=lambda t: t[1]['Pi'])
    return lab, o


def regime_key(par, A, phi, sel, s=0):
    v = branch_value(par, A, phi, sel, s)
    if v is None:
        return ('GAP',)
    lab, o = v
    return (lab, o['eg'], o['eb'])


def breakpoints(par, A, sel, s=0, n=400):
    """Find phi where the regime key changes, by bisection between grid points."""
    bps = []
    prev_phi = K(1, 4 * n)
    prev_key = regime_key(par, A, prev_phi, sel, s)
    for i in range(1, n):
        phi = K(i, n)
        key = regime_key(par, A, phi, sel, s)
        if key != prev_key:
            lo, hi = prev_phi, phi
            klo = prev_key
            for _ in range(70 if MODE['m'] == 'hp' else 30):
                mid = (lo + hi) / 2
                km = regime_key(par, A, mid, sel, s)
                if km == klo:
                    lo = mid
                else:
                    hi = mid
            bps.append((lo, hi))
        prev_phi, prev_key = phi, key
    return bps


def vertices(par, A, sel, s=0, n=400):
    """Candidate vertices of the upper hull: grid points and both sides of every regime change."""
    pts = []
    grid = [K(i, n) for i in range(1, n)] + [K(1, 10 ** 6), 1 - K(1, 10 ** 6)]
    for phi in grid:
        v = branch_value(par, A, phi, sel, s)
        if v is not None:
            pts.append((phi, v[1]['Pi'], v[0], phi))
    for lo, hi in breakpoints(par, A, sel, s, n):
        for phi in (lo, hi):
            v = branch_value(par, A, phi, sel, s)
            if v is not None:
                pts.append((phi, v[1]['Pi'], v[0], phi))
        # one-sided limits of the lower piece at hi and of the upper piece at lo
        vlo = branch_value(par, A, lo, sel, s)
        vhi = branch_value(par, A, hi, sel, s)
        if vlo is not None and vhi is not None:
            for ph, v in ((hi, vlo), (lo, vhi)):
                pts.append((ph, v[1]['Pi'] if False else extend_piece(par, A, ph, v, s), v[0] + '*', ph))
    pts.sort(key=lambda t: t[0])
    return pts


def extend_piece(par, A, phi, v, s=0):
    """Value at phi of the linear piece (label, eg, eb) taken from a neighbouring prior."""
    lab, o = v
    a = par.a
    beta = 1 if lab == 'FB' else 0
    q = branch.region_probs(phi, beta, a)
    eg, eb = o['eg'], o['eb']
    E = eg * (q['gH'] + q['gL']) + eb * (q['bH'] + q['bL'])
    OH = eg * q['gH'] + eb * q['bH']
    return A['t0'] + A['wL'] * E + A['DT'] * OH


def upper_hull(points):
    """points: list of (x, y, ...). Returns the upper concave hull vertices (monotone chain)."""
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


def cav_at(hull, x):
    for i in range(len(hull) - 1):
        x1, y1 = hull[i][:2]
        x2, y2 = hull[i + 1][:2]
        if x1 <= x <= x2:
            w = (x - x1) / (x2 - x1)
            return (1 - w) * y1 + w * y2, hull[i], hull[i + 1], w
    return None
