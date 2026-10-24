"""C7 model: the incumbent may answer the price with a binding public jump bid.

Base: discrete-Laplace noise, buy-only orders, c_L = 0, Reading N with point masses.
All integrands are piecewise linear in R between listed breakpoints, so the midpoint
rule on each piece is exact. Arithmetic uses mpmath at the working precision.
This file defines functions only. It prints nothing.
"""
from mpmath import mp, mpf, exp, sqrt

mp.dps = 50


class Par:
    """Benchmark auction values; team choices c_L = 0 and c_H = 5."""

    def __init__(self, h=10, ell=1, p='0.5', rho='0.25', cH=5, b=2, k='0.02', pi='0.5'):
        self.h, self.ell, self.p = mpf(h), mpf(ell), mpf(p)
        self.rho, self.cH, self.b = mpf(rho), mpf(cH), mpf(b)
        self.k, self.pi = mpf(k), mpf(pi)
        self.a = exp(-1 / self.b)


def auction(par, r):
    h, l, p = par.h, par.ell, par.p
    t0 = p * (1 - p / r)
    tH = r / 2 + p**2 / (2 * r)
    tL = l - (l**2 - p**2) / (2 * r)
    gH = h - r / 2 - p**2 / (2 * r)
    gL = (l**2 - p**2) / (2 * r)
    DT = (r - l)**2 / (2 * r)
    return dict(t0=t0, tH=tH, tL=tL, gH=gH, gL=gL, DT=DT)


def integ(f, pts, lo, hi):
    """Exact integral of a piecewise-linear f on [lo, hi]; pts holds every kink."""
    xs = sorted(set([lo, hi] + [x for x in pts if lo < x < hi]))
    return sum((v - u) * f((u + v) / 2) for u, v in zip(xs[:-1], xs[1:]))


def gross(par, mu, R):
    """Challenger gross profit against incumbent value R; payment max(p, R)."""
    pay = max(par.p, R)
    return mu * (par.h - pay) + (1 - mu) * max(par.ell - pay, 0)


def D(par, r, mu, a, c=None):
    """Challenger gross profit when its belief is R ~ U[a, c] (default c = r)."""
    c = r if c is None else c
    if c - a <= 0:
        return gross(par, mu, a)
    return integ(lambda R: gross(par, mu, R), [par.p, par.ell], a, c) / (c - a)


def B_prior(par, r, mu):
    A = auction(par, r)
    return A['gL'] + mu * (A['gH'] - A['gL'])


def jump_level(par, mu, Rhat):
    """Inverse of the indifference map R_hat(J): the bid that makes type R_hat indifferent."""
    if Rhat <= par.ell:
        return Rhat
    return par.ell + (Rhat - par.ell) * mu * (1 - par.rho) / (1 - par.rho * mu)


def threshold(par, r, mu):
    """Deterrence threshold R_hat* = max(p, a*), where D(mu; [a*, r]) = c_H."""
    h, l, p, cH = par.h, par.ell, par.p, par.cH
    if D(par, r, mu, p) <= cH:
        return p, 'corner'
    if D(par, r, mu, l) <= cH:
        E = mu * h + (1 - mu) * l
        const = mu * (2 * h - r) * r + (1 - mu) * l**2 - 2 * cH * r
        root = (E - cH) - sqrt((E - cH)**2 - const)
        return root, 'interior<=ell'
    return 2 * (h - cH / mu) - r, 'interior>ell'


def continuation(par, r, mu, jump=True):
    """Selected continuation at posterior mu. Returns case, threshold, bid, entry by group."""
    cH, rho = par.cH, par.rho
    if D(par, r, mu, 0) < cH:
        return dict(case='A', Rhat=r, J=None, sub='', e_silent=rho, hi_in_silent=0)
    if (not jump) or mu * (par.h - r) >= cH:
        return dict(case='B', Rhat=r, J=None, sub='', e_silent=1, hi_in_silent=1)
    Rhat, sub = threshold(par, r, mu)
    return dict(case='C', Rhat=Rhat, J=jump_level(par, mu, Rhat), sub=sub,
                e_silent=1, hi_in_silent=1)


def per_type(par, mu, R, cont, theta):
    """Proceeds, incumbent payoff, challenger net payoff, surplus for class theta and type R."""
    p, l, rho, cH = par.p, par.ell, par.rho, par.cH
    th = par.h if theta == 'h' else l
    W0 = R if R >= p else mpf(0)
    Wth = max(th, R)
    if cont['J'] is not None and R >= cont['Rhat']:
        J = cont['J']
        pay_in = R if th > R else max(J, th)          # target receipt with entry
        inc_in = 0 if th > R else R - max(J, th)
        ch_gross = max(th - R, 0)
        proc = rho * pay_in + (1 - rho) * J
        inc = rho * inc_in + (1 - rho) * (R - J)
        chal = rho * ch_gross
        surplus = rho * Wth + (1 - rho) * R
        return proc, inc, chal, surplus
    hi = cont['hi_in_silent']
    if th > R:
        pay_in, inc_in = max(p, R), mpf(0)
    else:
        pay_in, inc_in = max(p, th), R - max(p, th)
    ch_gross = max(th - max(p, R), 0)
    inc_out = R - p if R >= p else mpf(0)
    proc_out = p if R >= p else mpf(0)
    e = rho + (1 - rho) * hi
    proc = e * pay_in + (1 - e) * proc_out
    inc = e * inc_in + (1 - e) * inc_out
    chal = rho * ch_gross + (1 - rho) * hi * (ch_gross - cH)
    surplus = rho * Wth + (1 - rho) * (hi * (Wth - cH) + (1 - hi) * W0)
    return proc, inc, chal, surplus


def evaluate(par, r, mu, jump=True):
    """Expectations over R ~ U[0, r] at posterior mu under the selected continuation."""
    cont = continuation(par, r, mu, jump)
    pts = [par.p, par.ell, cont['Rhat']] + ([cont['J']] if cont['J'] is not None else [])
    out = {}
    for th in ('h', 'l'):
        for j, name in enumerate(('proc', 'inc', 'chal', 'surplus')):
            out[name + '_' + th] = integ(lambda R: per_type(par, mu, R, cont, th)[j], pts, 0, r) / r
    res = dict(cont)
    for name in ('proc', 'inc', 'chal', 'surplus'):
        res[name] = mu * out[name + '_h'] + (1 - mu) * out[name + '_l']
    res['S'] = out['proc_h'] - out['proc_l']
    res['P'] = res['proc']
    if cont['case'] == 'C':
        res['entry'] = par.rho + (1 - par.rho) * cont['Rhat'] / r
        res['preempt'] = 1 - cont['Rhat'] / r
    else:
        res['entry'] = cont['e_silent']
        res['preempt'] = mpf(0)
    res['entry_h'] = res['entry']   # entry does not depend on the class given mu
    return res


def news(par, beta):
    """Discrete-Laplace buy-only flows: good (x >= 1) and bad (x <= 0) posteriors and probabilities."""
    a, pi = par.a, par.pi
    pG_H = beta / (1 + a) + (1 - beta) * a / (1 + a)
    pG_L = a / (1 + a)
    pB_H, pB_L = 1 - pG_H, 1 - pG_L
    muG = pi * pG_H / (pi * pG_H + (1 - pi) * pG_L)
    muB = pi * pB_H / (pi * pB_H + (1 - pi) * pB_L)
    return dict(muG=muG, muB=muB, pG_H=pG_H, pG_L=pG_L, pB_H=pB_H, pB_L=pB_L,
                pG=pi * pG_H + (1 - pi) * pG_L, pB=pi * pB_H + (1 - pi) * pB_L)


def purchase_payoff(par, r, beta, jump=True):
    """High-class investor's expected net payoff from q = 1 against the schedule induced by beta."""
    n = news(par, beta)
    a = par.a
    eG, eB = evaluate(par, r, n['muG'], jump), evaluate(par, r, n['muB'], jump)
    return (1 / (1 + a)) * (1 - n['muG']) * eG['S'] + (a / (1 + a)) * (1 - n['muB']) * eB['S'] - par.k


def outcome(par, r, beta, jump=True):
    """Ex ante outcomes at investor strategy beta (low class never buys)."""
    n = news(par, beta)
    eG, eB = evaluate(par, r, n['muG'], jump), evaluate(par, r, n['muB'], jump)
    pi = par.pi
    out = dict(beta=beta, muG=n['muG'], muB=n['muB'], PG=eG['P'], PB=eB['P'],
               caseG=eG['case'] + eG['sub'], caseB=eB['case'] + eB['sub'],
               RhatG=eG['Rhat'], JG=eG['J'], SG=eG['S'], SB=eB['S'])
    out['entry'] = n['pG'] * eG['entry'] + n['pB'] * eB['entry']
    out['O_H'] = pi * (n['pG_H'] * eG['entry'] + n['pB_H'] * eB['entry'])
    out['preempt'] = n['pG'] * eG['preempt'] + n['pB'] * eB['preempt']
    for name in ('proc', 'inc', 'chal', 'surplus'):
        out[name] = n['pG'] * eG[name] + n['pB'] * eB[name]
    out['entry_goodnews'] = eG['entry']
    return out
