"""Research economy at prior 1/2: point-mass classes h, l; incumbent U[0,r]; reserve p.
Pure functions; floats are fine for exploration (not certificates)."""
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class Prim:
    h: float; l: float; p: float; rho: float; cH: float; k: float; beta: float; lbar: float; a: float

def Delta(P, r):  # h > r > l >= p
    return (r - P.l)**2 / (2*r)
def gL(P, r):
    return (P.l**2 - P.p**2) / (2*r)
def gamma(P, r):
    return (2*r*P.h - r*r - P.l**2) / (2*r)
def tau(P, r):
    return (P.cH - gL(P, r)) / gamma(P, r)
def J(P, r):
    return Delta(P, r) * (1 - tau(P, r))
def t0(P, r):
    return P.p * (1 - P.p / r)
def tL(P, r):
    return P.l + (P.p**2 - P.l**2) / (2*r)
def fr(P, d):  # root above l of Delta(r)=d
    return P.l + d + math.sqrt(d*d + 2*P.l*d)

def m_of(P, lam):
    return (1 - lam) * P.beta / (2*P.beta + lam*(1 - 2*P.beta))
def M_of(P, lam):
    return 1 - m_of(P, lam)
def mprime(P, lam):
    return -P.beta / (2*P.beta + lam*(1 - 2*P.beta))**2
def lamE(P, t):  # recruitment intensity, M_lam = tau, for 1/2 < tau < 1
    if t >= 1: return float('inf')
    if t <= 0.5: return 0.0
    return P.beta*(2*t - 1) / (P.beta + (1 - 2*P.beta)*(1 - t))

def bisect(f, lo, hi, n=200):
    flo = f(lo)
    for _ in range(n):
        mid = 0.5*(lo + hi)
        if (f(mid) > 0) == (flo > 0):
            lo, flo = mid, f(mid)
        else:
            hi = mid
    return 0.5*(lo + hi)

def Lam(P, D):   # R / RQ research: 2a lam = D m_lam - k  (needs D > 2k)
    if D <= 2*P.k: return 0.0
    return bisect(lambda x: 2*P.a*x - D*m_of(P, x) + P.k, 0.0, 1.0)
def LamF(P, D):  # RF research: 2a lam = (1+rho) D m_lam - 2k
    if (1 + P.rho)*D/2 <= 2*P.k: return 0.0
    return bisect(lambda x: 2*P.a*x - (1 + P.rho)*D*m_of(P, x) + 2*P.k, 0.0, 1.0)
def lamS(P):
    return (1 - P.rho)*P.k / (2*P.a*P.rho)
def lam_star(P, D):
    L = Lam(P, D)
    return L if L <= lamS(P) else LamF(P, D)
def lamQ(P, D):  # non-recruiting full-orders research: a lam = rho D m_lam - k
    if P.rho*D/2 <= P.k: return 0.0
    return bisect(lambda x: P.a*x - P.rho*D*m_of(P, x) + P.k, 0.0, 1.0)

def Dstar(P, lam):  # inverse of lam_star
    if lam <= lamS(P):
        return (2*P.a*lam + P.k) / m_of(P, lam)
    return (2*P.a*lam + 2*P.k) / ((1 + P.rho)*m_of(P, lam))

def entry(P, lam):
    return P.rho + (1 - P.rho)*(P.beta + (0.5 - P.beta)*lam)

def sale_rate(P, D, lam):
    """informed sale probability t of class L given research lam (IM): 0 / interior / lam"""
    bh = (1 - lam)*P.beta
    if P.rho*D/2 <= P.k: return 0.0
    if P.rho*D*m_of(P, lam) >= P.k: return lam
    return bh*(P.rho*D/P.k - 2)

def check_eq(P, r, lam_hat, sH, sL, rule_C='C1', verbose=True, label=''):
    """Recompute everything at a candidate tuple and report each condition (no assertions)."""
    D, tu = Delta(P, r), tau(P, r)
    bh, bh0 = (1 - lam_hat)*P.beta, (1 - lam_hat)*(1 - 2*P.beta)
    eta = {-1: P.beta, 0: 1 - 2*P.beta, 1: P.beta}
    fH = {q: (1 - lam_hat)*eta[q] + lam_hat*sH.get(q, 0.0) for q in (-1, 0, 1)}
    fL = {q: (1 - lam_hat)*eta[q] + lam_hat*sL.get(q, 0.0) for q in (-1, 0, 1)}
    mu = {q: fH[q] / (fH[q] + fL[q]) for q in (-1, 0, 1)}
    e = {q: (P.rho if mu[q] < tu - 1e-12 else 1.0) for q in (-1, 0, 1)}  # C1
    wL = tL(P, r) - t0(P, r)
    Pr = {q: t0(P, r) + e[q]*(wL + D*mu[q]) for q in (-1, 0, 1)}
    UH = {1: e[1]*D*(1 - mu[1]) - P.k, 0: 0.0, -1: -e[-1]*D*(1 - mu[-1]) - P.k}
    UL = {-1: e[-1]*D*mu[-1] - P.k, 0: 0.0, 1: -e[1]*D*mu[1] - P.k}
    V = 0.5*max(UH.values()) + 0.5*max(UL.values())
    lam_opt = min(P.lbar, V / P.a)
    tol = 1e-7
    okH = all(sH.get(q, 0) < 1e-12 or UH[q] >= max(UH.values()) - tol for q in (-1, 0, 1))
    okL = all(sL.get(q, 0) < 1e-12 or UL[q] >= max(UL.values()) - tol for q in (-1, 0, 1))
    okE7 = abs(lam_opt - lam_hat) < 1e-6
    # prices reveal posteriors
    okP = all((abs(Pr[q] - Pr[q2]) < 1e-12) == (abs(mu[q] - mu[q2]) < 1e-12) for q in (-1,0,1) for q2 in (-1,0,1))
    ent = sum(0.5*(fH[q] + fL[q])*e[q] for q in (-1, 0, 1))
    if verbose:
        print(f"[{label}] r={r:.6f} D={D:.6f} tau={tu:.6f} lam^={lam_hat:.6f}")
        print(f"   mu(-1,0,1)=({mu[-1]:.5f},{mu[0]:.5f},{mu[1]:.5f})  e=({e[-1]},{e[0]},{e[1]})  M_lam={M_of(P,lam_hat):.5f}")
        print(f"   UH(1)={UH[1]:.6f} UL(-1)={UL[-1]:.6f} V={V:.6f} V/a={V/P.a:.6f} lam_opt={lam_opt:.6f}")
        print(f"   E5 H ok={okH}  E5 L ok={okL}  E7 ok={okE7}  prices reveal posteriors={okP}  entry={ent:.6f}")
    return okH and okL and okE7 and okP, ent
