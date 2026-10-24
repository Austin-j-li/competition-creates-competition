"""Buy-only trading stage of the discrete-Laplace model at an arbitrary prior phi.

The informed investor (class H with prob phi) buys one unit with probability beta;
class L never buys (see memo, Result 1). Noise Z has P(z) = (1-a)/(1+a) a^|z|.
Flow regions: 'good' = x >= 1 (z >= 0 if the unit is bought), 'bad' = x <= 0.
Everything here is for a fixed schedule: the price takes two values, one per region.
"""
from common import *


def region_probs(phi, beta, a):
    """Return dict with P(region, class) for the two flow regions."""
    PgH = ((1 - beta) * a + beta) / (1 + a)   # P(x>=1 | H)
    PgL = a / (1 + a)                          # P(x>=1 | L)
    PbH = 1 - PgH
    PbL = 1 - PgL
    return dict(gH=phi * PgH, gL=(1 - phi) * PgL, bH=phi * PbH, bL=(1 - phi) * PbL)


def posteriors(phi, beta, a):
    q = region_probs(phi, beta, a)
    mu_g = q['gH'] / (q['gH'] + q['gL'])
    mu_b = q['bH'] / (q['bH'] + q['bL'])
    return mu_g, mu_b, q


def gain_buy(par, A, phi, beta, s=0):
    """Gain of the H-investor from one unit, against the schedules induced by beta."""
    a = par.a
    mu_g, mu_b, q = posteriors(phi, beta, a)
    eg = entry(par, A, mu_g, s)
    eb = entry(par, A, mu_b, s)
    G = (1 / (1 + a)) * eg * A['DT'] * (1 - mu_g) + (a / (1 + a)) * eb * A['DT'] * (1 - mu_b) - par.k
    return G, eg, eb, mu_g, mu_b, q


def outcome(par, A, phi, beta, s=0):
    """Entry, high-class ownership, target proceeds at the schedules induced by beta."""
    a = par.a
    mu_g, mu_b, q = posteriors(phi, beta, a)
    eg = entry(par, A, mu_g, s)
    eb = entry(par, A, mu_b, s)
    Pg = q['gH'] + q['gL']
    Pb = q['bH'] + q['bL']
    E = eg * Pg + eb * Pb
    OH = eg * q['gH'] + eb * q['bH']
    Pi = A['t0'] + A['wL'] * E + A['DT'] * OH
    return dict(E=E, OH=OH, Pi=Pi, eg=eg, eb=eb, mu_g=mu_g, mu_b=mu_b)


def equilibria(par, A, phi, s=0):
    """Pure equilibria (beta in {0,1}); investor selects zero at a tie.

    Returns list of (label, outcome dict).  'NT' = no trade, 'FB' = full buying by H.
    """
    out = []
    G0 = gain_buy(par, A, phi, 0, s)[0]
    G1 = gain_buy(par, A, phi, 1, s)[0]
    if G0 <= 0:
        out.append(('NT', outcome(par, A, phi, 0, s)))
    if G1 > 0:
        out.append(('FB', outcome(par, A, phi, 1, s)))
    return out, G0, G1


def mixed_roots(par, A, phi, s=0, n=2000):
    """Diagnostic: interior beta with G(beta)=0 (conventional correspondence). Bisection on sign changes."""
    pts = [K(i, n) for i in range(n + 1)]
    vals = [gain_buy(par, A, phi, b, s)[0] for b in pts]
    roots = []
    for i in range(n):
        if vals[i] > 0 and vals[i + 1] < 0 or vals[i] < 0 and vals[i + 1] > 0:
            lo, hi = pts[i], pts[i + 1]
            slo = vals[i] > 0
            for _ in range(80 if MODE['m'] == 'hp' else 40):
                mid = (lo + hi) / 2
                gm = gain_buy(par, A, phi, mid, s)[0]
                if (gm > 0) == slo:
                    lo = mid
                else:
                    hi = mid
            roots.append((lo + hi) / 2)
    return roots
