"""Random test of Lemma R.5 (pool cap) and of the residual bounds inside Proposition R.6.
Random order laws (1-2 atoms per type, correct signs), random consistent pools containing Z0.
For each draw we compare left sides with the claimed bounds; the largest ratio must stay below 1."""
import csv, math, random
from scipy import optimize
from model import *

def crossing(P, oH, oL, tau):
    g = lambda x: posterior(oH, oL, x, P.b) - tau
    xs = [-30 + 60 * i / 600 for i in range(601)]
    vals = [g(x) for x in xs]
    if vals[0] >= 0:
        return -math.inf
    if vals[-1] < 0:
        return math.inf
    for i in range(600):
        if vals[i] < 0 <= vals[i + 1]:
            return optimize.brentq(g, xs[i], xs[i + 1], xtol=1e-13)

def rand_orders(rng, sign):
    n = rng.choice((1, 1, 2))
    qs = [sign * rng.choice((1.0, rng.random(), rng.random(), rng.random() * 0.3 + 0.7)) for _ in range(n)]
    ws = [rng.random() + 0.05 for _ in range(n)]
    s = sum(ws)
    return tuple((q, w / s) for q, w in zip(qs, ws))

def draw(rng, P, a):
    for _ in range(200):
        oH = rand_orders(rng, +1); oL = rand_orders(rng, -1)
        zc = crossing(P, oH, oL, a.tauL)
        if zc == -math.inf:
            continue            # no flow with posterior below tauL: pool impossible
        pool = [(-math.inf, zc)] if zc != math.inf else [(-math.inf, math.inf)]
        # extras: random intervals above zc
        extras = []
        for _ in range(rng.choice((0, 1, 1, 2, 3))):
            lo = zc + rng.random() * 4 if zc != math.inf else 0
            extras.append((lo, lo + rng.random() * rng.choice((0.05, 0.3, 1.0, 3.0))))
        # half-line extension option: pool up to a random cutoff, then bisection to make belief just below tauL
        mode = rng.choice(("extras", "halfline_max"))
        if mode == "halfline_max":
            def pb(c): return pool_belief(P, oH, oL, ((-math.inf, c),)) - a.tauL
            hi = zc
            if pb(40) < 0:
                hi = 40
            else:
                hi = optimize.brentq(pb, zc, 40, xtol=1e-12) - 1e-9
            pool = [(-math.inf, hi)]
        else:
            pool = pool + extras
            pool.sort()
            # merge overlap
            m = []
            for lo, hi in pool:
                if m and lo <= m[-1][1]:
                    m[-1] = (m[-1][0], max(m[-1][1], hi))
                else:
                    m.append((lo, hi))
            pool = m
        pool = tuple(pool)
        if pool_belief(P, oH, oL, pool) < a.tauL:
            return oH, oL, pool
    return None

def run(cL, n, seed=1):
    rng = random.Random(seed)
    P = Prm(cL=cL, r=3.0, k=0.02, rho=0.25); a = auction(P); b = P.b
    xb = xbar(P)
    pibar = 0.5 * (F(xb - 1, b) + F(xb + 1, b))
    worst = dict(PH=0, PL=0, PN=0, s=0, ms=0, FL=1e9, FH=1e9)
    cnt = 0
    for _ in range(n):
        d = draw(rng, P, a)
        if d is None:
            continue
        oH, oL, pool = d
        cnt += 1
        pH = sum(prob(oH, max(lo, -LIM), min(hi, LIM), b) for lo, hi in pool)
        pL = sum(prob(oL, max(lo, -LIM), min(hi, LIM), b) for lo, hi in pool)
        worst['PH'] = max(worst['PH'], pH / F(xb - 1, b))
        worst['PL'] = max(worst['PL'], pL / F(xb + 1, b))
        worst['PN'] = max(worst['PN'], 0.5 * (pH + pL) / pibar)
        pcs = entry_pieces(P, oH, oL, pool)
        for s in (0.25, 0.6, 1.0):
            pplus = sum(prob(((s, 1.0),), max(lo, -LIM), min(hi, LIM), b) for lo, hi in pool)
            pminus = sum(prob(((-s, 1.0),), max(lo, -LIM), min(hi, LIM), b) for lo, hi in pool)
            worst['s'] = max(worst['s'], pplus / F(xb, b), pminus / F(xb + s, b))
            FL = (payoff(P, 'L', -s, pcs, oH, oL) + P.k * s) / s
            FH = (payoff(P, 'H', s, pcs, oH, oL) + P.k * s) / s
            bL = P.rho * a.tauL * a.DT * S(xb + s, b)
            bH = P.rho * a.m * a.DT * S(xb, b)
            worst['FL'] = min(worst['FL'], FL / bL)
            worst['FH'] = min(worst['FH'], FH / bH)
    return cnt, worst

if __name__ == "__main__":
    rows = []
    for cL in (2.4, 2.8, 3.0, 3.5):
        cnt, w = run(cL, 700, seed=int(cL * 100))
        print(cL, cnt, {k: round(v, 5) for k, v in w.items()}, flush=True)
        rows.append(dict(cL=cL, draws=cnt, **w))
    with open('random_tests.csv', 'w', newline='') as fh:
        wr = csv.DictWriter(fh, fieldnames=list(rows[0])); wr.writeheader(); wr.writerows(rows)
