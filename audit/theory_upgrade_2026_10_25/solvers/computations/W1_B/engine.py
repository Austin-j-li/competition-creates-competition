# Reduced-form engine: point-mass classes h>l>p, continuous incumbent F given as a CDF function.
# Delta = int_l^h (1-F), gL = int_p^l F, gH = int_p^h F, gamma = gH - gL, tau = (cH - gL)/gamma.
from mpmath import mp, mpf, quad
mp.dps = 25

def auction(F, h, l, p, cH, pts=()):
    br = sorted(set([p, l, h] + [x for x in pts if p < x < h]))
    def integ(f, a, b):
        cuts = [a] + [x for x in br if a < x < b] + [b]
        return sum(quad(f, [cuts[i], cuts[i+1]]) for i in range(len(cuts)-1))
    D = integ(lambda y: 1 - F(y), l, h)
    gL = integ(F, p, l)
    gH = integ(F, p, h)
    gam = gH - gL
    tau = (cH - gL)/gam
    return dict(Delta=D, gL=gL, gH=gH, gam=gam, tau=tau, J=D*(1-tau))

def M_of(pi, u): return pi*(1+u)/(pi*(1+u)+1-pi)
def m_of(pi, u): return pi/(pi+(1-pi)*(1+u))

def coexist_criterion(Delta, tau, pi, rho, k, u):
    M = M_of(pi, u)
    return (Delta*(1-tau) >= k) and (pi < tau <= M) and (rho*Delta*max(pi, 1-pi) <= k)

def equilibria(Delta, tau, pi, rho, k, lam, beta):
    """Independent enumeration of equilibria (rules IM, C1) when pi < tau < 1, using the
    class-by-class structure: candidate purchase rates s in {0, lam, s*, roots of K_H=k},
    candidate sale rates t in {0, lam, roots of K_L=k}. Returns list of (label, s, t, e1, entry)."""
    b = (1-lam)*beta
    def mup(s): return pi*(b+s)/(b+pi*s)
    def mum(t): return pi*b/(b+(1-pi)*t)
    def ent(mu, tie_e=1):
        if mu > tau: return 1
        if mu < tau: return rho
        return tie_e
    out = []
    # high-class candidates
    Hc = []
    # s = 0
    if rho*Delta*(1-pi) <= k: Hc.append(('N', mpf(0), rho))
    # s = lam
    e1 = ent(mup(lam))
    if e1*Delta*(1-mup(lam)) >= k: Hc.append(('F', lam, e1))
    # interior with e=rho: rho*Delta*b/(b+pi s)*(1-pi)... 1-mup(s) = (1-pi)b/(b+pi s)
    # rho*Delta*(1-pi)*b/(b+pi s) = k  ->  s = (rho*Delta*(1-pi)*b/k - b)/pi
    sQ = (rho*Delta*(1-pi)*b/k - b)/pi
    if 0 < sQ < lam and mup(sQ) < tau: Hc.append(('Q', sQ, rho))
    sR = (Delta*(1-pi)*b/k - b)/pi
    if 0 < sR < lam and mup(sR) > tau: Hc.append(('R', sR, 1))
    if tau < 1:
        sstar = b*(tau-pi)/(pi*(1-tau))
        if 0 < sstar < lam and abs(Delta*(1-tau) - k) < mpf(10)**-15:   # C1: tie entry 1 needs J = k
            Hc.append(('T', sstar, 1))
    # low-class candidates (e(-1) = rho since mum <= pi < tau)
    Lc = []
    if rho*Delta*pi <= k: Lc.append(mpf(0))
    if rho*Delta*mum(lam) >= k: Lc.append(lam)
    tQ = (pi*rho*Delta*b/k - b)/(1-pi)
    if 0 < tQ < lam and rho*Delta*mum(tQ) > 0: Lc.append(tQ)
    for (lab, s, e1) in Hc:
        for t in Lc:
            if s + mpf(10)**-18 >= t:   # product lemma domain: s >= t gives mu0 <= pi < tau
                entry = rho + (e1 - rho)*(b + pi*s)
                out.append((lab, float(s), float(t), e1, float(entry)))
    return out
