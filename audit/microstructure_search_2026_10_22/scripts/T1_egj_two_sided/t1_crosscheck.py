"""Independent floating-point cross-check of the exact solver (numerical diagnostic).

It shares no code with t1_solver.py. It computes posteriors by Bayes' rule from the order
strategies directly, and searches for equilibria by brute force:
  * corners: direct test;
  * edges: sign changes of the indifference gap on a 4001-point grid, refined by bisection;
  * interior: on a 401 x 401 grid, cells where both indifference gaps change sign are refined
    by a damped Newton step and then tested;
  * challenger mixing: on each line mu_x = tau (sampled at 4001 points), the free entry rate
    is solved from one indifference and the other is tested for a sign change.
It prints, for each test point, the equilibria of both methods side by side.

Run from the repository root (about 1 to 3 minutes; use the slot wrapper):
  bash audit/microstructure_search_2026_10_22/scripts/_slots/run_slot.sh .venv/bin/python \
      audit/microstructure_search_2026_10_22/scripts/T1_egj_two_sided/t1_crosscheck.py
"""
import sys
from fractions import Fraction as F
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from t1_core import bench  # parameter record only
from t1_solver import enumerate_equilibria


class FloatModel:
    def __init__(self, P, belief='IC'):
        g = {key: float(v) for key, v in P.items()}
        h, ell, p, r = g['h'], g['ell'], g['p'], g['r']
        self.t0 = p * (1 - p / r)
        self.tH = r / 2 + p * p / (2 * r)
        self.tL = ell - (ell * ell - p * p) / (2 * r)
        self.gH = h - r / 2 - p * p / (2 * r)
        self.gL = (ell * ell - p * p) / (2 * r)
        self.D = self.tH - self.tL
        self.cH, self.rho, self.k, self.pi, self.lam = g['cH'], g['rho'], g['k'], g['pi'], g['lam']
        th = g['theta']
        self.noise = {-1: th, 0: 1 - 2 * th, 1: th}
        self.vp, self.vm = (1.0, 0.0) if belief == 'IC' else (0.5, 0.5)

    def B(self, mu):
        return self.gL + mu * (self.gH - self.gL)

    def flows(self, a, b):
        """Class laws from strategies: H buys w.p. a (effective), L sells w.p. b."""
        fH, fL = {}, {}
        for x in range(-2, 3):
            fH[x] = (1 - a) * self.noise.get(x, 0) + a * self.noise.get(x - 1, 0)
            fL[x] = (1 - b) * self.noise.get(x, 0) + b * self.noise.get(x + 1, 0)
        return fH, fL

    def beliefs(self, a, b):
        fH, fL = self.flows(a, b)
        mu = {}
        for x in range(-2, 3):
            den = self.pi * fH[x] + (1 - self.pi) * fL[x]
            mu[x] = self.pi * fH[x] / den if den > 1e-300 else (self.vp if x > 0 else self.vm)
        return mu

    def entry(self, mu, sig=None):
        e = {}
        for x, m in mu.items():
            e[x] = 1.0 if self.B(m) >= self.cH else self.rho
        if sig:
            for x, s in sig.items():
                e[x] = self.rho + (1 - self.rho) * s
        return e

    def gaps(self, a, b, sig=None):
        """Net gains of H buying and L selling (gross minus k)."""
        mu = self.beliefs(a, b)
        e = self.entry(mu, sig)
        gH = sum(pz * e[1 + z] * self.D * (1 - mu[1 + z]) for z, pz in self.noise.items())
        gL = sum(pz * e[-1 + z] * self.D * mu[-1 + z] for z, pz in self.noise.items())
        return gH - self.k, gL - self.k, mu, e

    def entry_rate(self, a, b, sig=None):
        fH, fL = self.flows(a, b)
        mu = self.beliefs(a, b)
        e = self.entry(mu, sig)
        return sum((self.pi * fH[x] + (1 - self.pi) * fL[x]) * e[x] for x in range(-2, 3))


def brute(P, belief='IC'):
    M = FloatModel(P, belief)
    lam = M.lam
    out = []
    tol = 1e-12

    def ok(rate, gap):
        if rate <= 1e-12:
            return gap <= 1e-12
        if rate >= lam - 1e-12:
            return gap >= -1e-12
        return abs(gap) <= 1e-9

    # corners
    for a in (0.0, lam):
        for b in (0.0, lam):
            gH, gL, mu, e = M.gaps(a, b)
            if ok(a, gH) and ok(b, gL):
                out.append(('corner', a, b, M.entry_rate(a, b)))
    # edges
    ts = np.linspace(0, lam, 4001)[1:-1]
    for fixed, val in (('b', 0.0), ('b', lam), ('a', 0.0), ('a', lam)):
        def gap(t):
            a, b = (t, val) if fixed == 'b' else (val, t)
            gH, gL, mu, e = M.gaps(a, b)
            return (gH if fixed == 'b' else gL), (gL if fixed == 'b' else gH)
        vals = np.array([gap(t)[0] for t in ts])
        for i in range(len(ts) - 1):
            if vals[i] == 0 or vals[i] * vals[i + 1] < 0:
                lo, hi = ts[i], ts[i + 1]
                flo = vals[i]
                for _ in range(80):
                    m = 0.5 * (lo + hi)
                    fm = gap(m)[0]
                    if (fm < 0) == (flo < 0):
                        lo, flo = m, fm
                    else:
                        hi = m
                t = 0.5 * (lo + hi)
                own, other = gap(t)
                if abs(own) < 1e-9 and ok(val, other):
                    a, b = (t, val) if fixed == 'b' else (val, t)
                    out.append(('edge', a, b, M.entry_rate(a, b)))
    # interior (pure entry cells): grid sign test then Newton
    n = 401
    grid = np.linspace(0, lam, n)[1:-1]
    GH = np.zeros((len(grid), len(grid)))
    GL = np.zeros_like(GH)
    for i, a in enumerate(grid):
        for j, b in enumerate(grid):
            GH[i, j], GL[i, j], _, _ = M.gaps(a, b)
    found = []
    for i in range(len(grid) - 1):
        for j in range(len(grid) - 1):
            sH = np.sign(GH[i:i + 2, j:j + 2])
            sL = np.sign(GL[i:i + 2, j:j + 2])
            if sH.min() < 0 < sH.max() and sL.min() < 0 < sL.max():
                a, b = 0.5 * (grid[i] + grid[i + 1]), 0.5 * (grid[j] + grid[j + 1])
                for _ in range(60):
                    h = 1e-9
                    f0 = np.array(M.gaps(a, b)[:2])
                    Ja = (np.array(M.gaps(a + h, b)[:2]) - f0) / h
                    Jb = (np.array(M.gaps(a, b + h)[:2]) - f0) / h
                    J = np.column_stack([Ja, Jb])
                    try:
                        step = np.linalg.solve(J, f0)
                    except np.linalg.LinAlgError:
                        break
                    a, b = a - step[0], b - step[1]
                    if not (0 < a < lam and 0 < b < lam):
                        break
                if 0 < a < lam and 0 < b < lam:
                    gH, gL, mu, e = M.gaps(a, b)
                    if abs(gH) < 1e-10 and abs(gL) < 1e-10:
                        if not any(abs(a - fa) < 1e-7 and abs(b - fb) < 1e-7 for fa, fb in found):
                            found.append((a, b))
                            out.append(('cell', a, b, M.entry_rate(a, b)))
    # challenger mixing where a line mu_x = tau crosses an edge (one class at a bound)
    tau = (M.cH - M.gL) / (M.gH - M.gL)
    for fixed, val in (('b', 0.0), ('b', lam), ('a', 0.0), ('a', lam)):
        for x in (-1, 0, 1):
            def mux(t):
                a, b = (t, val) if fixed == 'b' else (val, t)
                return M.beliefs(a, b)[x] - tau
            ts2 = np.linspace(0, lam, 4001)[1:-1]
            vals = np.array([mux(t) for t in ts2])
            for i in range(len(ts2) - 1):
                if vals[i] * vals[i + 1] < 0:
                    lo, hi = ts2[i], ts2[i + 1]
                    for _ in range(80):
                        m = 0.5 * (lo + hi)
                        if (mux(m) < 0) == (vals[i] < 0):
                            lo = m
                        else:
                            hi = m
                    t = 0.5 * (lo + hi)
                    a, b = (t, val) if fixed == 'b' else (val, t)
                    gH0, gL0, _, _ = M.gaps(a, b, {x: 0.0})
                    gH1, gL1, _, _ = M.gaps(a, b, {x: 1.0})
                    own0, own1 = (gH0, gH1) if fixed == 'b' else (gL0, gL1)
                    oth0, oth1 = (gL0, gL1) if fixed == 'b' else (gH0, gH1)
                    if own1 == own0:
                        continue
                    s = -own0 / (own1 - own0)
                    if 0 < s < 1:
                        other = oth0 + s * (oth1 - oth0)
                        if ok(val, other):
                            out.append((f'edge-line{x}', a, b, M.entry_rate(a, b, {x: s})))
    # challenger mixing on the lines mu_x = tau, interior of the square
    tau = (M.cH - M.gL) / (M.gH - M.gL)
    for x in (-1, 0, 1):
        pts = []
        for i, a in enumerate(np.linspace(0, lam, 801)[1:-1]):
            # solve mu_x(a, b) = tau for b on (0, lam) by bisection on a fine grid
            bs = np.linspace(0, lam, 801)[1:-1]
            mus = np.array([M.beliefs(a, b)[x] - tau for b in bs])
            for j in range(len(bs) - 1):
                if mus[j] * mus[j + 1] < 0:
                    lo, hi = bs[j], bs[j + 1]
                    for _ in range(60):
                        m = 0.5 * (lo + hi)
                        if (M.beliefs(a, m)[x] - tau < 0) == (mus[j] < 0):
                            lo = m
                        else:
                            hi = m
                    pts.append((a, 0.5 * (lo + hi)))
        # along the sampled line points, solve sigma_x from the indifference that depends on it
        prev = None
        for (a, b) in pts:
            gH0, gL0, _, _ = M.gaps(a, b, {x: 0.0})
            gH1, gL1, _, _ = M.gaps(a, b, {x: 1.0})
            if x == 1:
                s = -gH0 / (gH1 - gH0) if gH1 != gH0 else None
                other = gL0
            elif x == -1:
                s = -gL0 / (gL1 - gL0) if gL1 != gL0 else None
                other = gH0
            else:
                s = -gH0 / (gH1 - gH0) if gH1 != gH0 else None
                other = None if s is None else (gL0 + s * (gL1 - gL0))
            val = other if (s is not None and 0 < s < 1) else None
            if prev is not None and val is not None and prev[2] is not None and prev[2] * val < 0:
                out.append((f'line{x}', a, b, M.entry_rate(a, b, {x: s})))
            prev = (a, b, val)
    return out


def main():
    pts = [dict(r=F(2), lam=F(1), theta=F(333, 1000)),
           dict(r=F(31, 20), lam=F(1), theta=F(1, 4)),
           dict(r=F(3), lam=F(1), theta=F(1, 4)),
           dict(r=F(31, 20), lam=F(4, 5), theta=F(3, 20)),
           dict(r=F(33, 20), lam=F(4, 5), theta=F(3, 20)),
           dict(r=F(3), lam=F(4, 5), theta=F(3, 20)),
           dict(r=F(18, 5), lam=F(1), theta=F(1, 10)),
           dict(r=F(3), lam=F(1), theta=F(3, 20)),
           dict(r=F(33, 20), lam=F(1), theta=F(2, 5)),
           dict(r=F(8, 5), lam=F(4, 5), theta=F(1, 5))]
    for kw in pts:
        P = bench(**kw)
        eqs, und, Mx = enumerate_equilibria(P)
        ex = sorted(float(q['out']['E'].mid() if hasattr(q['out']['E'], 'mid') else q['out']['E']) for q in eqs)
        bf = brute(P)
        bfE = sorted(round(q[3], 6) for q in bf)
        print(f"r={float(kw['r']):.3f} lam={float(kw['lam']):.2f} theta={float(kw['theta']):.3f}:")
        print(f"   exact solver ({len(eqs)} eq, {len(und)} undecided): E = " + ', '.join(f'{v:.6f}' for v in ex))
        print(f"   brute force  ({len(bf)} eq): " + ', '.join(f'{q[0]}:{q[3]:.6f}' for q in sorted(bf, key=lambda q: q[3])))


if __name__ == '__main__':
    main()
