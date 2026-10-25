"""Benchmark model objects for the W5 checks (order-slot version).

Pure functions; mpmath at 50 digits. No assertions: scripts print values.
"""
from mpmath import mp, mpf, e as E, sqrt

mp.dps = 50

# benchmark primitives
h, ell, p = mpf(10), mpf(1), mpf(1) / 2
rho, cH, k = mpf(1) / 4, mpf(6), mpf(1) / 50
beta_B = mpf(294655) / 10**6
u_B = E - 1


def slot(u=u_B, beta=beta_B):
    lam = u * beta / (1 + u * beta)
    b = (1 - lam) * beta
    b0 = (1 - lam) * (1 - 2 * beta)
    return dict(u=u, beta=beta, lam=lam, b=b, b0=b0)


def Mtop(pi, u):
    return pi * (1 + u) / (pi * (1 + u) + 1 - pi)


def mbot(pi, u):
    return pi / (pi + (1 - pi) * (1 + u))


# uniform incumbent on [0, r], point-mass classes (A1 closed forms)
def auction(r):
    t0 = p * (1 - p / r)
    tH = r / 2 + p**2 / (2 * r)
    tL = ell - (ell**2 - p**2) / (2 * r)
    gH = h - tH
    gL = (ell**2 - p**2) / (2 * r)
    D = tH - tL
    gam = gH - gL
    tau = (cH - gL) / gam
    wL = tL - t0
    return dict(t0=t0, tH=tH, tL=tL, gH=gH, gL=gL, D=D, gam=gam, tau=tau, wL=wL)


def A(r, mu):
    a = auction(r)
    return a["wL"] + a["D"] * mu


def fr(d):
    """root above ell of Delta_T(r) = d"""
    return ell + d + sqrt(d * d + 2 * ell * d)


def full_orders(pi, r, s=None, rule="C1"):
    """Full two-sided trade at prior pi: posteriors, counts, entry, prices, K margins.

    Entry: rho below tau, 1 at or above tau (rule C1)."""
    s = s or slot()
    u, lam, b, b0 = s["u"], s["lam"], s["b"], s["b0"]
    a = auction(r)
    M, m = Mtop(pi, u), mbot(pi, u)
    post = {-1: m, 0: pi, 1: M}
    ent = {x: (1 if post[x] >= a["tau"] else rho) for x in post}
    ent = {x: mpf(v) for x, v in ent.items()}
    P = {x: a["t0"] + ent[x] * (a["wL"] + a["D"] * post[x]) for x in post}
    prob = {1: b + pi * lam, -1: b + (1 - pi) * lam, 0: b0}
    KH = ent[1] * a["D"] * (1 - M)
    KL = ent[-1] * a["D"] * m
    Ip = P[1] - P[0]
    Im = P[0] - P[-1]
    Pbar = sum(prob[x] * P[x] for x in post)
    T = prob[1] * Ip - prob[-1] * Im
    return dict(a=a, M=M, m=m, post=post, ent=ent, P=P, prob=prob, KH=KH, KL=KL,
                Ip=Ip, Im=Im, Pbar=Pbar, T=T, S=P[1] - P[-1])
