"""Independent floating-point search for equilibria of the T6 model (shares no code with t6_core).

For a parameter point and a list of strengths it builds the flow laws from scratch, evaluates both
classes' net purchase and sale payoffs on a grid of effective rates (A, S) in [0, lam]^2 with the
entry rule "prepare when the posterior is at least tau", and reports:
  * corners that satisfy both best-response conditions;
  * edge roots of the mover's payoff (bisection), split into pure-entry roots and roots at an entry jump
    (the latter are the challenger-mixing equilibria);
  * interior points where both payoffs change sign inside a grid cell with a fixed entry pattern,
    refined by Newton's method.
Usage: python t6_crosscheck.py LAM BETA THETA R1 [R2 ...]   (rationals as a/b)
Prints only.
"""
import sys
from fractions import Fraction
import numpy as np

H, ELL, PRES, RHO, CH, KC = 10.0, 1.0, 0.5, 0.25, 6.0, 0.02


def auction(r):
    t0 = PRES * (1 - PRES / r)
    tH = (PRES ** 2 + (r ** 2 - PRES ** 2) / 2) / r
    tL = (PRES ** 2 + (ELL ** 2 - PRES ** 2) / 2 + (r - ELL) * ELL) / r
    gH = H - tH
    gL = ((ELL - PRES) * PRES + (ELL - PRES) ** 2 / 2) / r
    D = tH - tL
    return t0, tH, tL, gH, gL, D


def laws(lam, beta, theta, A, S):
    """Class flow laws on x = -2..2 by direct convolution of the slot law and the noise law."""
    c = (1 - lam) * beta
    noise = {-1: theta, 0: 1 - 2 * theta, 1: theta}
    slotH = {1: c + A, 0: 1 - 2 * c - A, -1: c}
    slotL = {1: c, 0: 1 - 2 * c - S, -1: c + S}
    fH = {x: 0.0 for x in range(-2, 3)}
    fL = {x: 0.0 for x in range(-2, 3)}
    for q, pq in slotH.items():
        for z, pz in noise.items():
            fH[q + z] = fH[q + z] + pq * pz
    for q, pq in slotL.items():
        for z, pz in noise.items():
            fL[q + z] = fL[q + z] + pq * pz
    return fH, fL


def payoffs(lam, beta, theta, r, A, S, e_override=None):
    t0, tH, tL, gH, gL, D = auction(r)
    tau = (CH - gL) / (gH - gL)
    fH, fL = laws(lam, beta, theta, A, S)
    mu = {x: fH[x] / (fH[x] + fL[x]) for x in fH}
    e = {x: (1.0 if mu[x] >= tau else RHO) for x in mu}
    if e_override:
        e.update(e_override)
    noise = {-1: theta, 0: 1 - 2 * theta, 1: theta}
    buy = sum(pz * e[1 + z] * D * (1 - mu[1 + z]) for z, pz in noise.items()) - KC
    sell = sum(pz * e[-1 + z] * D * mu[-1 + z] for z, pz in noise.items()) - KC
    pat = tuple(int(mu[x] >= tau) for x in range(-2, 3))
    probs = {x: 0.5 * (fH[x] + fL[x]) for x in fH}
    E = sum(probs[x] * e[x] for x in probs)
    return buy, sell, pat, E, mu, e, tau


def search(lam, beta, theta, r, N=241):
    out = []
    tol = 1e-12
    grid = np.linspace(0.0, lam, N)
    # corners
    for A in (0.0, lam):
        for S in (0.0, lam):
            b, s, pat, E, mu, e, tau = payoffs(lam, beta, theta, r, A, S)
            okH = b <= tol if A == 0 else b >= -tol
            okL = s <= tol if S == 0 else s >= -tol
            if okH and okL:
                out.append(('corner', A, S, E, pat))
    # edges
    for fixed, val in (('S', 0.0), ('S', lam), ('A', 0.0), ('A', lam)):
        vals = []
        for t in grid:
            A, S = (t, val) if fixed == 'S' else (val, t)
            b, s, pat, E, mu, e, tau = payoffs(lam, beta, theta, r, A, S)
            vals.append((b if fixed == 'S' else s, s if fixed == 'S' else b, pat))
        for i in range(N - 1):
            g1, g2 = vals[i][0], vals[i + 1][0]
            if g1 * g2 > 0:
                continue
            lo, hi = grid[i], grid[i + 1]
            jump = vals[i][2] != vals[i + 1][2]
            for _ in range(80):
                m = 0.5 * (lo + hi)
                A, S = (m, val) if fixed == 'S' else (val, m)
                gm = payoffs(lam, beta, theta, r, A, S)[0 if fixed == 'S' else 1]
                A1, S1 = (lo, val) if fixed == 'S' else (val, lo)
                g_lo = payoffs(lam, beta, theta, r, A1, S1)[0 if fixed == 'S' else 1]
                if g_lo * gm <= 0:
                    hi = m
                else:
                    lo = m
            m = 0.5 * (lo + hi)
            if m <= 1e-12 or m >= lam - 1e-12:
                continue
            A, S = (m, val) if fixed == 'S' else (val, m)
            b, s, pat, E, mu, e, tau = payoffs(lam, beta, theta, r, A, S)
            A1, S1 = (lo, val) if fixed == 'S' else (val, lo)
            A2, S2 = (hi, val) if fixed == 'S' else (val, hi)
            pat_lo = payoffs(lam, beta, theta, r, A1, S1)[2]
            pat_hi = payoffs(lam, beta, theta, r, A2, S2)[2]
            other = s if fixed == 'S' else b
            ok_other = other <= tol if val == 0 else other >= -tol
            if not ok_other:
                continue
            if pat_lo != pat_hi:
                # root at an entry jump: the challenger mixes at the tied flow
                xs = [x for x in range(-2, 3) if pat_lo[x + 2] != pat_hi[x + 2]]
                ov_lo = {x: RHO for x in xs}
                ov_hi = {x: 1.0 for x in xs}
                g_lo = payoffs(lam, beta, theta, r, A, S, ov_lo)[0 if fixed == 'S' else 1]
                g_hi = payoffs(lam, beta, theta, r, A, S, ov_hi)[0 if fixed == 'S' else 1]
                if g_lo <= 0 <= g_hi:
                    w = -g_lo / (g_hi - g_lo)
                    ov = {x: RHO + w * (1 - RHO) for x in xs}
                    E2 = payoffs(lam, beta, theta, r, A, S, ov)[3]
                    out.append((f'edge {fixed}={val:.4f} jump', A, S, E2, pat_lo))
            else:
                out.append((f'edge {fixed}={val:.4f}', A, S, E, pat))
    # interior cells with fixed entry pattern
    G = np.zeros((N, N, 2))
    PAT = {}
    for i, A in enumerate(grid):
        for j, S in enumerate(grid):
            b, s, pat, E, mu, e, tau = payoffs(lam, beta, theta, r, A, S)
            G[i, j] = (b, s)
            PAT[(i, j)] = pat
    found = []
    for i in range(1, N - 2):
        for j in range(1, N - 2):
            pats = {PAT[(i, j)], PAT[(i + 1, j)], PAT[(i, j + 1)], PAT[(i + 1, j + 1)]}
            if len(pats) != 1:
                continue
            bH = G[i:i + 2, j:j + 2, 0]
            bL = G[i:i + 2, j:j + 2, 1]
            if bH.min() > 0 or bH.max() < 0 or bL.min() > 0 or bL.max() < 0:
                continue
            pat = PAT[(i, j)]
            ov = {x: (1.0 if pat[x + 2] else RHO) for x in range(-2, 3)}
            x = np.array([grid[i], grid[j]]) + 0.5 * (grid[1] - grid[0])
            for _ in range(50):
                f0 = np.array(payoffs(lam, beta, theta, r, x[0], x[1], ov)[:2])
                h = 1e-8
                J = np.zeros((2, 2))
                for k in range(2):
                    xp = x.copy()
                    xp[k] += h
                    J[:, k] = (np.array(payoffs(lam, beta, theta, r, xp[0], xp[1], ov)[:2]) - f0) / h
                try:
                    x = x - np.linalg.solve(J, f0)
                except np.linalg.LinAlgError:
                    break
            f0 = np.array(payoffs(lam, beta, theta, r, x[0], x[1], ov)[:2])
            if np.max(np.abs(f0)) < 1e-11 and 0 < x[0] < lam and 0 < x[1] < lam:
                if payoffs(lam, beta, theta, r, x[0], x[1])[2] == pat:
                    if not any(abs(x[0] - y[0]) < 1e-7 and abs(x[1] - y[1]) < 1e-7 for y in found):
                        found.append(tuple(x))
                        E = payoffs(lam, beta, theta, r, x[0], x[1], ov)[3]
                        out.append(('interior', x[0], x[1], E, pat))
    return out


def main():
    lam, beta, theta = (float(Fraction(v)) for v in sys.argv[1:4])
    for rs in sys.argv[4:]:
        r = float(Fraction(rs))
        res = search(lam, beta, theta, r)
        print(f"lam={lam:.6f} beta={beta:.6f} theta={theta:.6f} r={r:.4f}: {len(res)} equilibria")
        for kind, A, S, E, pat in sorted(res, key=lambda t: (t[1], t[2])):
            print(f"   {kind:22s} A={A:.6f} S={S:.6f} entry={E:.6f} recruit-pattern(x=-2..2)={pat}")


if __name__ == '__main__':
    main()
