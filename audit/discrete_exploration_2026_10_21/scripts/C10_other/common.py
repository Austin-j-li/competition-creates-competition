"""Shared objects for the C10 study (print-only; no assertions).

Two number modes:
  'hp'    : mpmath, 60 digits, a = exp(-1/b) with b = 2 (the paper's scale).
  'exact' : fractions.Fraction, a = 3/5 (a rational stand-in for the noise ratio).
Every function takes numbers of the active mode.
"""
from fractions import Fraction as Fr
import mpmath as mp

mp.mp.dps = 60
MODE = {'m': 'hp'}


def set_mode(m):
    MODE['m'] = m


def K(n, d=1):
    """A constant n/d in the active mode."""
    if MODE['m'] == 'exact':
        return Fr(n, d)
    return mp.mpf(n) / mp.mpf(d)


def num(x):
    """Convert a Fraction to the active mode."""
    if isinstance(x, Fr):
        return K(x.numerator, x.denominator)
    return x


def a_of_mode(b=2):
    if MODE['m'] == 'exact':
        return Fr(3, 5)
    return mp.e ** (-mp.mpf(1) / mp.mpf(b))


def fl(x):
    return float(x)


class P:
    """Parameter record (benchmark auction values, c_L = 0)."""

    def __init__(self, h=10, l=1, p=Fr(1, 2), rho=Fr(1, 4), k=Fr(1, 50), cH=5, b=2):
        self.h = num(Fr(h))
        self.l = num(Fr(l))
        self.p = num(Fr(p))
        self.rho = num(Fr(rho))
        self.k = num(Fr(k))
        self.cH = num(Fr(cH))
        self.a = a_of_mode(b)


def auction(par, r):
    r = num(Fr(r)) if isinstance(r, (int, Fr)) else r
    h, l, p = par.h, par.l, par.p
    t0 = p * (1 - p / r)
    tH = r / 2 + p * p / (2 * r)
    tL = l - (l * l - p * p) / (2 * r)
    gH = h - r / 2 - p * p / (2 * r)
    gL = (l * l - p * p) / (2 * r)
    DT = tH - tL
    wL = tL - t0
    return dict(t0=t0, tH=tH, tL=tL, gH=gH, gL=gL, DT=DT, wL=wL, r=r)


def Bgain(A, mu):
    return A['gL'] + mu * (A['gH'] - A['gL'])


def tau(par, A, s=0):
    """Posterior threshold for high-cost entry; toehold s adds s*(wL + DT*mu) to the gain."""
    s = num(Fr(s)) if isinstance(s, (int, Fr)) else s
    c0 = A['gL'] + s * A['wL']
    c1 = (A['gH'] - A['gL']) + s * A['DT']
    return (par.cH - c0) / c1


def entry(par, A, mu, s=0):
    """e(mu) = rho + (1-rho) 1{gain(mu) >= cH}; challenger prepares at indifference."""
    s = num(Fr(s)) if isinstance(s, (int, Fr)) else s
    g = A['gL'] + s * A['wL'] + mu * ((A['gH'] - A['gL']) + s * A['DT'])
    return par.rho + (1 - par.rho) * (1 if g >= par.cH else 0)
