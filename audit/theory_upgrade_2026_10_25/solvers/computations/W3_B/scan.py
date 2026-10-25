"""Independent scanner for equilibria with research at prior 1/2 (scratch, prints only).

At a fixed strength (Delta, tau), for each conjectured intensity lam on a grid, it lists the
trading-stage equilibria at presence lam from the high/low-class lemmas of A4 (which hold at
any presence), computes the research value V and the residual min{lbar, V/a} - lam, and then
locates research fixed points by sign changes within one trading form, plus the cap and zero.
Rules: investor IM or I0; challenger C1 (an indifferent high-cost challenger prepares).
"""
import sys
sys.path.insert(0, 'audit/theory_upgrade_2026_10_25/solvers/computations/W3_B')
from model import *


def trading_forms(lam, Delta, tau, P, rule="IM"):
    """Return list of dicts: trading equilibria at presence lam (prior 1/2), C1."""
    rho, k, beta = P.rho, P.k, P.beta
    out = []
    if lam <= 0:
        return out
    b = (1 - lam) * beta
    b0 = (1 - lam) * (1 - 2 * beta)
    mu_plus = lambda s: (b + s) / (2 * b + s)
    mu_minus = lambda t: b / (2 * b + t)
    sstar = b * (2 * tau - 1) / (1 - tau)
    # high-class pairs
    highs = []
    # N
    if rho * Delta * 0.5 < k or (rule == "IM" and rho * Delta * 0.5 <= k) or (rule == "I0" and rho * Delta * 0.5 <= k):
        highs.append(("N", 0.0, rho))
    if rule == "IM":
        sQ = b * (rho * Delta / k - 2)
        if 0 < sQ < lam and mu_plus(sQ) < tau:
            highs.append(("Q", sQ, rho))
        sR = b * (Delta / k - 2)
        if sstar < sR < lam:
            highs.append(("R", sR, 1.0))
        if 0 < sstar < lam and abs(Delta * (1 - tau) - k) < 1e-15:
            highs.append(("T", sstar, 1.0))
    # F
    Mlam = mu_plus(lam)
    e1 = 1.0 if Mlam >= tau else rho
    KH = e1 * Delta * (1 - Mlam)
    if (rule == "IM" and KH >= k) or (rule == "I0" and KH > k):
        highs.append(("F", lam, e1))
    # low-class rate
    lows = []
    if rho * Delta * 0.5 <= k:
        lows.append(("n", 0.0))
    if rule == "IM" and rho * Delta * m_of(lam, P) < k < rho * Delta * 0.5:
        lows.append(("q", b * (rho * Delta / k - 2)))
    mlam = mu_minus(lam)
    if (rule == "IM" and rho * Delta * mlam >= k) or (rule == "I0" and rho * Delta * mlam > k):
        lows.append(("f", lam))
    for (hn, s, e1) in highs:
        for (ln, t) in lows:
            UH = e1 * Delta * (1 - mu_plus(s)) - k
            UL = rho * Delta * mu_minus(t) - k
            V = 0.5 * max(0.0, UH) + 0.5 * max(0.0, UL)
            # zero-order posterior and entry
            fH0 = b0 + lam - s
            fL0 = b0 + lam - t
            mu0 = fH0 / (fH0 + fL0)
            e0 = 1.0 if mu0 >= tau else rho
            pr1 = b + s / 2
            prm = b + t / 2
            pr0 = 1 - pr1 - prm
            ent = e1 * pr1 + rho * prm + e0 * pr0
            out.append(dict(form=hn + ln, s=s, t=t, e1=e1, V=V, UH=UH, UL=UL, mu1=mu_plus(s),
                            mum=mu_minus(t), mu0=mu0, entry=ent))
    return out


def key(f):
    return f['form'][0] + ('+' if f['e1'] == 1 else 'o')


def research_equilibria(r, P, rule="IM", n=4000):
    A = auction(P, r)
    Delta, tau = A['Delta'], A['tau']
    res = []
    # zero research
    if P.rho * Delta / 2 <= P.k:
        res.append(dict(lam=0.0, form="Z", entry=P.rho))
    grid = [P.lbar * (i + 0.5) / n for i in range(n)]
    prev = {}
    for lam in grid:
        cur = {}
        for f in trading_forms(lam, Delta, tau, P, rule):
            cur[key(f)] = min(P.lbar, f['V'] / P.a) - lam
        for form, val in cur.items():
            if form in prev:
                lam0, v0 = prev[form]
                if (v0 > 0) != (val > 0):
                    def g(x, form=form):
                        for f in trading_forms(x, Delta, tau, P, rule):
                            if key(f) == form:
                                return min(P.lbar, f['V'] / P.a) - x
                        return float('nan')
                    try:
                        root = bisect(g, lam0, lam, it=80)
                    except ValueError:
                        root = 0.5 * (lam0 + lam)
                    info = [f for f in trading_forms(root, Delta, tau, P, rule) if key(f) == form]
                    jump = abs(g(root - 1e-9) - g(root + 1e-9)) > 1e-6 if root > 1e-8 else False
                    if info:
                        res.append(dict(lam=root, form=info[0]['form'] + ('+' if info[0]['e1'] == 1 else 'o') + (' JUMP' if jump else ''), entry=info[0]['entry'], mu1=info[0]['mu1'],
                                        mum=info[0]['mum'], t=info[0]['t'], UL=info[0]['UL'], UH=info[0]['UH']))
        prev = {fm: (lam, v) for fm, v in cur.items()}
    # cap
    for f in trading_forms(P.lbar, Delta, tau, P, rule):
        if f['V'] / P.a >= P.lbar:
            res.append(dict(lam=P.lbar, form=f['form'] + "@cap", entry=f['entry'], mu1=f['mu1'], mum=f['mum'],
                            t=f['t'], UL=f['UL'], UH=f['UH']))
    return A, res


if __name__ == "__main__":
    pass
