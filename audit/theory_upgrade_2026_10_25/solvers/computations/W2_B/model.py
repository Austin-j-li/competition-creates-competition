"""Point-mass classes, uniform incumbent U[0,r], prior 1/2: research branch (R) objects.

Pure functions; used by the exploration scripts in this folder. Prints nothing on import.
"""
from math import sqrt


def auction(r, h, ell, p):
    """Return dict of t0, tH, tL, gH, gL, WH, WL for R ~ U[0,r], point classes h > ell >= p."""
    def tv(v):
        if v <= r:
            return v - (v * v - p * p) / (2 * r)
        return r / 2 + p * p / (2 * r)

    def gv(v):
        return v - tv(v)

    def Wv(v):
        return min(v / r, 1.0)

    t0 = p * (1 - p / r) if r >= p else 0.0
    return dict(t0=t0, tH=tv(h), tL=tv(ell), gH=gv(h), gL=gv(ell), WH=Wv(h), WL=Wv(ell))


def m_of(lam, beta):
    return beta * (1 - lam) / (2 * beta + (1 - 2 * beta) * lam)


def dm_of(lam, beta):
    return -beta / (2 * beta + (1 - 2 * beta) * lam) ** 2


def lam_R(Delta, a, k, beta):
    """Unique root in (0,1) of 2a(1-2b)l^2 + [4ab + k(1-2b) + b*Delta] l + b(2k - Delta) = 0, if Delta > 2k."""
    if Delta <= 2 * k:
        return None
    A = 2 * a * (1 - 2 * beta)
    B = 4 * a * beta + k * (1 - 2 * beta) + beta * Delta
    C = beta * (2 * k - Delta)
    if A == 0:
        return -C / B
    return (-B + sqrt(B * B - 4 * A * C)) / (2 * A)


def lam_E(tau, beta):
    return beta * (2 * tau - 1) / (beta + (1 - 2 * beta) * (1 - tau))


def branch(r, prm):
    """Research-branch objects at strength r; prm has h, ell, p, cH, rho, k, beta, a, cap."""
    au = auction(r, prm['h'], prm['ell'], prm['p'])
    Delta = au['tH'] - au['tL']
    gamma = au['gH'] - au['gL']
    tau = (prm['cH'] - au['gL']) / gamma if gamma > 0 else float('inf')
    lam = lam_R(Delta, prm['a'], prm['k'], prm['beta'])
    out = dict(r=r, Delta=Delta, gamma=gamma, tau=tau, lam=lam, **au)
    if lam is None or not (0.5 < tau < 1):
        out['on_branch'] = False
        return out
    lE = lam_E(tau, prm['beta'])
    rho, beta = prm['rho'], prm['beta']
    eH = rho + (1 - rho) * (beta + (1 - beta) * lam)
    eL = rho + (1 - rho) * beta * (1 - lam)
    out.update(lamE=lE, eH=eH, eL=eL, entry=(eH + eL) / 2, own=0.5 * eH * au['WH'],
               on_branch=(lam >= lE) and (lam < prm['cap']) and (rho * Delta <= 2 * prm['k']))
    return out


def eps_e(Delta, prm):
    """Elasticity of class-H entry e_H with respect to the spread on the branch."""
    a, k, beta, rho = prm['a'], prm['k'], prm['beta'], prm['rho']
    lam = lam_R(Delta, a, k, beta)
    m, dm = m_of(lam, beta), dm_of(lam, beta)
    dlam = m / (2 * a - Delta * dm)
    eH = rho + (1 - rho) * (beta + (1 - beta) * lam)
    return (1 - rho) * (1 - beta) * Delta * dlam / eH, lam, dlam
