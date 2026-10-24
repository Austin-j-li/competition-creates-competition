"""Exhaustive equilibrium enumeration for the two-sided three-point model with weights
(theta, 1 - 2 theta, theta), theta != 1/3, presence lam, c_L = 0, prior pi.

Method (every step exact or in rational interval arithmetic):
  * dominance leaves effective rates (a, b) in [0, lam]^2 (H buys with rate a, L sells with rate b);
  * the lines mu_x = tau (x = -1, 0, 1) are linear in (a, b) and cut the square into entry cells;
  * corners, edges, open cells, line segments (challenger mixing) and line crossings are
    enumerated separately;
  * inside a cell the indifference conditions are bivariate quadratics N_H = 0, N_L = 0;
    their common roots come from the resultant in a (degree <= 4 in b), isolated by Sturm
    sequences with rational endpoints, and from a = (A2 B0 - A0 B2)/(A1 B2 - A2 B1);
  * every root is enclosed in a rational box; sign conditions are checked on the box.

The module prints nothing. t1_scan.py and t1_certificates.py call it.
"""
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from t1_core import FLOWS, auction, noise, Iv, sqrt_bounds

# ---------------------------------------------------------------------------
# Bivariate polynomials in (a, b): dict {(i, j): coeff}.
# ---------------------------------------------------------------------------


def P_(c0=0, ca=0, cb=0):
    p = {}
    for key, c in (((0, 0), c0), ((1, 0), ca), ((0, 1), cb)):
        c = F(c)
        if c != 0:
            p[key] = c
    return p


def padd(*ps):
    out = {}
    for p in ps:
        for key, c in p.items():
            out[key] = out.get(key, F(0)) + c
    return {k_: c for k_, c in out.items() if c != 0}


def pscale(p, s):
    s = F(s) if not isinstance(s, F) else s
    return {k_: c * s for k_, c in p.items() if c * s != 0}


def pmul(p, q):
    out = {}
    for (i1, j1), c1 in p.items():
        for (i2, j2), c2 in q.items():
            key = (i1 + i2, j1 + j2)
            out[key] = out.get(key, F(0)) + c1 * c2
    return {k_: c for k_, c in out.items() if c != 0}


def peval(p, a, b):
    tot = None
    for (i, j), c in p.items():
        term = c * (a ** i) * (b ** j) if not isinstance(a, Iv) and not isinstance(b, Iv) else \
            Iv.of(a) ** i * Iv.of(b) ** j * c
        tot = term if tot is None else tot + term
    if tot is None:
        return F(0) if not (isinstance(a, Iv) or isinstance(b, Iv)) else Iv(0)
    return tot


def coeffs_in_a(p):
    """p as sum_i A_i(b) a^i; returns list of univariate coefficient lists in b."""
    deg = max((i for (i, j) in p), default=0)
    out = []
    for i in range(deg + 1):
        dj = max((j for (ii, j) in p if ii == i), default=-1)
        out.append([p.get((i, j), F(0)) for j in range(dj + 1)] if dj >= 0 else [])
    return out


# ---------------------------------------------------------------------------
# Univariate polynomials: lists of Fraction coefficients, low to high.
# ---------------------------------------------------------------------------


def utrim(c):
    c = list(c)
    while c and c[-1] == 0:
        c.pop()
    return c


def uadd(p, q):
    n = max(len(p), len(q))
    return utrim([(p[i] if i < len(p) else 0) + (q[i] if i < len(q) else 0) for i in range(n)])


def uneg(p):
    return [-c for c in p]


def umul(p, q):
    if not p or not q:
        return []
    out = [F(0)] * (len(p) + len(q) - 1)
    for i, c1 in enumerate(p):
        for j, c2 in enumerate(q):
            out[i + j] += c1 * c2
    return utrim(out)


def ueval(p, x):
    tot = F(0) if not isinstance(x, Iv) else Iv(0)
    for c in reversed(p):
        tot = tot * x + c
    return tot


def uderiv(p):
    return utrim([i * p[i] for i in range(1, len(p))])


def udivmod(p, q):
    p, q = utrim(p), utrim(q)
    if not q:
        raise ZeroDivisionError
    out = [F(0)] * max(len(p) - len(q) + 1, 1)
    r = list(p)
    while len(utrim(r)) >= len(q) and utrim(r):
        r = utrim(r)
        s = len(r) - len(q)
        c = r[-1] / q[-1]
        out[s] = c
        for i, qc in enumerate(q):
            r[s + i] -= c * qc
        r = utrim(r)
    return utrim(out), utrim(r)


def sturm(p):
    seq = [utrim(p), uderiv(p)]
    while seq[-1] and len(seq[-1]) > 1:
        _, r = udivmod(seq[-2], seq[-1])
        if not r:
            break
        seq.append(uneg(r))
    return [s for s in seq if s]


def sign_changes(seq, x):
    signs = []
    for s in seq:
        v = ueval(s, x)
        if v != 0:
            signs.append(v > 0)
    return sum(1 for i in range(1, len(signs)) if signs[i] != signs[i - 1])


def deflate(p, x0):
    """Divide out every factor (t - x0) with x0 rational."""
    p = utrim(p)
    while p and ueval(p, x0) == 0:
        p, rem = udivmod(p, [-x0, F(1)])
        if rem:
            raise ArithmeticError('deflation failed')
    return p


def isolate(p, lo, hi, width=F(1, 2 ** 90)):
    """Brackets (l, u) with lo < l < u < hi, one distinct root of p in (l, u), none at l, u.
    Rational roots found during bisection are returned as (x, x)."""
    p = utrim(p)
    if len(p) <= 1:
        return []
    p = deflate(deflate(p, lo), hi)
    if len(p) <= 1:
        return []
    seq = sturm(p)
    out = []
    stack = [(lo, hi)]
    while stack:
        l, u = stack.pop()
        n = sign_changes(seq, l) - sign_changes(seq, u)
        if n == 0:
            continue
        if n == 1 and u - l <= width:
            out.append((l, u))
            continue
        m = (l + u) / 2
        if ueval(p, m) == 0:
            out.append((m, m))
            # remove the rational root and continue on both sides
            q = deflate(p, m)
            sub = isolate(q, l, u, width) if len(q) > 1 else []
            out.extend(s for s in sub if s != (m, m))
            continue
        stack.append((l, m))
        stack.append((m, u))
    return sorted(set(out))


def resultant_a(pH, pL):
    """Resultant in a of two polynomials quadratic (or lower) in a; univariate in b."""
    A = coeffs_in_a(pH)
    Bc = coeffs_in_a(pL)
    while len(A) < 3:
        A.append([])
    while len(Bc) < 3:
        Bc.append([])
    A0, A1, A2 = A[:3]
    B0, B1, B2 = Bc[:3]
    if not utrim(A2):
        raise ValueError('N_H not quadratic in a')
    if not utrim(B2) and not utrim(B1):
        # N_L does not depend on a: resultant is N_L^2 (up to a constant)
        return umul(B0, B0), (A0, A1, A2, B0, B1, B2)
    if not utrim(B2):
        # quadratic and linear: A2 B0^2 - A1 B0 B1 + A0 B1^2
        R = uadd(uadd(umul(A2, umul(B0, B0)), uneg(umul(A1, umul(B0, B1)))), umul(A0, umul(B1, B1)))
        return R, (A0, A1, A2, B0, B1, B2)
    t1 = uadd(umul(A2, B0), uneg(umul(A0, B2)))
    t2 = uadd(umul(A2, B1), uneg(umul(A1, B2)))
    t3 = uadd(umul(A1, B0), uneg(umul(A0, B1)))
    R = uadd(umul(t1, t1), uneg(umul(t2, t3)))
    return R, (A0, A1, A2, B0, B1, B2)


# ---------------------------------------------------------------------------
# The model in polynomial form.
# ---------------------------------------------------------------------------


class Model:
    def __init__(self, P, belief='IC', hidden=False):
        self.P = P
        self.hidden = hidden
        self.A = auction(P)
        th = P['theta']
        self.n = noise(th)
        self.th, self.ph = th, 1 - 2 * th
        self.d = self.ph - self.th
        self.pi, self.rho, self.lam = P['pi'], P['rho'], P['lam']
        self.kD = P['k'] / self.A['D']
        self.tau = self.A['tau']
        pi, n = self.pi, self.n
        # flow laws as linear polynomials
        self.fH, self.fL, self.Dn = {}, {}, {}
        for x in FLOWS:
            self.fH[x] = P_(n.get(x, 0), n.get(x - 1, 0) - n.get(x, 0), 0)
            self.fL[x] = P_(n.get(x, 0), 0, n.get(x + 1, 0) - n.get(x, 0))
            self.Dn[x] = padd(pscale(self.fH[x], pi), pscale(self.fL[x], 1 - pi))
        # lines mu_x = tau  <=>  Lx = pi fH (1 - tau) - (1 - pi) fL tau = 0 ; Lx > 0 means mu_x > tau
        self.L = {x: padd(pscale(self.fH[x], pi * (1 - self.tau)), pscale(self.fL[x], -(1 - pi) * self.tau))
                  for x in (-1, 0, 1)}
        # extreme flows: posterior 1 at +2 and 0 at -2 when used
        self.e2 = self.entry_fixed(F(1))
        self.em2 = self.entry_fixed(F(0))
        if belief == 'IC':
            self.v_plus, self.v_minus = F(1), F(0)
        elif belief == 'passive':
            self.v_plus, self.v_minus = F(1, 2), F(1, 2)
        else:
            self.v_plus, self.v_minus = belief
        self.e_vplus = self.entry_fixed(self.v_plus)
        self.e_vminus = self.entry_fixed(self.v_minus)
        if hidden:
            # the challenger cannot see the price: its belief is the prior at every flow
            e_pi = self.entry_fixed(self.pi)
            if e_pi is None:
                e_pi = F(1)
            self.e_hidden = e_pi
            self.e2 = self.em2 = self.e_vplus = self.e_vminus = e_pi

    def Bmu(self, mu):
        return self.A['gL'] + mu * (self.A['gH'] - self.A['gL'])

    def entry_fixed(self, mu):
        val = self.Bmu(mu) - self.P['cH']
        if val > 0:
            return F(1)
        if val < 0:
            return self.rho
        return None  # tie: free in [rho, 1]

    # ---- payoff numerators for a given entry triple (e_-1, e_0, e_1) ----
    def NH(self, e0, e1, off=F(0)):
        """Numerator of (G_H - k)/Delta over D_0 D_1; off = deviation term at an unused +2."""
        th, ph, pi = self.th, self.ph, self.pi
        t1 = pscale(pmul(self.fL[0], self.Dn[1]), th * e0 * (1 - pi))
        t2 = pscale(pmul(self.fL[1], self.Dn[0]), ph * e1 * (1 - pi))
        t3 = pscale(pmul(self.Dn[0], self.Dn[1]), -(self.kD - off))
        return padd(t1, t2, t3)

    def NL(self, em1, e0, off=F(0)):
        """Numerator of (G_L - k)/Delta over D_-1 D_0; off = deviation term at an unused -2."""
        th, ph, pi = self.th, self.ph, self.pi
        t1 = pscale(pmul(self.fH[-1], self.Dn[0]), ph * em1 * pi)
        t2 = pscale(pmul(self.fH[0], self.Dn[-1]), th * e0 * pi)
        t3 = pscale(pmul(self.Dn[-1], self.Dn[0]), -(self.kD - off))
        return padd(t1, t2, t3)

    def off_H(self, a):
        """H's deviation term at +2 when a = 0 (unused flow), per unit Delta."""
        if (isinstance(a, Iv) and a.lo > 0) or (not isinstance(a, Iv) and a > 0):
            return F(0)
        e = self.e_vplus if self.e_vplus is not None else F(1)
        return self.th * e * (1 - self.v_plus)

    def off_L(self, b):
        if (isinstance(b, Iv) and b.lo > 0) or (not isinstance(b, Iv) and b > 0):
            return F(0)
        e = self.e_vminus if self.e_vminus is not None else F(1)
        return self.th * e * self.v_minus

    # ---- direct (exact or interval) evaluation ----
    def gains(self, a, b, e):
        """G_H/Delta and G_L/Delta (gross, per unit Delta) at (a, b) for entry dict e on x=-1,0,1."""
        pi = self.pi
        D0, D1, Dm1 = (peval(self.Dn[x], a, b) for x in (0, 1, -1))
        gH = self.th * e[0] * (1 - pi) * peval(self.fL[0], a, b) / D0 + \
            self.ph * e[1] * (1 - pi) * peval(self.fL[1], a, b) / D1 + self.off_H(a)
        gL = self.ph * e[-1] * pi * peval(self.fH[-1], a, b) / Dm1 + \
            self.th * e[0] * pi * peval(self.fH[0], a, b) / D0 + self.off_L(b)
        return gH, gL

    def wrong_way(self, a, b, e):
        """Gross gains (per unit Delta) of the wrong-way orders: H sells, L buys (both <= 0)."""
        pi, th, ph = self.pi, self.th, self.ph
        mu = {x: pi * peval(self.fH[x], a, b) / peval(self.Dn[x], a, b) for x in (-1, 0, 1)}
        mu[2] = F(1) if not (a == 0) else self.v_plus
        mu[-2] = F(0) if not (b == 0) else self.v_minus
        ee = dict(e)
        ee[2] = self.e2 if not (a == 0) else (self.e_vplus or F(1))
        ee[-2] = self.em2 if not (b == 0) else (self.e_vminus or F(1))
        # H sells: reaches x = -2, -1, 0 with weights th, ph, th; residual -e (1 - mu)
        hs = -(th * ee[-2] * (1 - mu[-2]) + ph * ee[-1] * (1 - mu[-1]) + th * ee[0] * (1 - mu[0]))
        # L buys: reaches 0, 1, 2; residual -e mu
        lb = -(th * ee[0] * mu[0] + ph * ee[1] * mu[1] + th * ee[2] * mu[2])
        return hs, lb

    def outcomes(self, a, b, e):
        """E, O_H, R_T, W (exact or interval) for entry dict e on x = -1, 0, 1."""
        pi, rho, A = self.pi, self.rho, self.A
        ee = dict(e)
        ee[2] = self.e2 if self.e2 is not None else F(1)
        ee[-2] = self.em2
        E = 0
        OH = 0
        for x in FLOWS:
            fh, fl = peval(self.fH[x], a, b), peval(self.fL[x], a, b)
            E = E + (fh * pi + fl * (1 - pi)) * ee[x]
            OH = OH + fh * pi * ee[x]
        RT = A['t0'] + OH * A['wH'] + (E - OH) * A['wL']
        W = A['base'] + OH * (A['gH'] + A['pF']) + (E - OH) * (A['gL'] + A['pF']) - self.P['cH'] * (E - rho)
        return dict(E=E, OH=OH, RT=RT, W=W)

    def sign_L(self, x, a, b):
        if self.hidden:
            return 1 if self.e_hidden == 1 else -1
        v = peval(self.L[x], a, b)
        if isinstance(v, Iv):
            return 1 if v.lo > 0 else (-1 if v.hi < 0 else None)
        return (v > 0) - (v < 0)


# ---------------------------------------------------------------------------
# Enumeration.
# ---------------------------------------------------------------------------


def _cond_ok(val, kind, strict_full=False):
    """val = G/Delta - k/Delta (exact or Iv). kind: 'zero' (rate 0), 'full', 'mix'.
    Returns True, False or None (undecided)."""
    if isinstance(val, Iv):
        if kind == 'zero':
            return True if val.hi <= 0 else (False if val.lo > 0 else None)
        if kind == 'full':
            if strict_full:
                return True if val.lo > 0 else (False if val.hi <= 0 else None)
            return True if val.lo >= 0 else (False if val.hi < 0 else None)
        return None
    if kind == 'zero':
        return val <= 0
    if kind == 'full':
        return val > 0 if strict_full else val >= 0
    return val == 0


def _kind(rate, lam):
    if rate == 0:
        return 'zero'
    if rate == lam:
        return 'full'
    return 'mix'


def _entry_choices(M, a, b):
    """For each interior flow: fixed entry, or None for a tie (exact a, b only)."""
    out = {}
    for x in (-1, 0, 1):
        s = M.sign_L(x, a, b)
        out[x] = F(1) if s > 0 else (M.rho if s < 0 else None)
    return out


def _point_feasible(M, a, b, kindH, kindL, strict_full):
    """Exact rational point (a, b): feasibility over free entry rates at tied flows.
    Returns list of (e dict) representative solutions with sigma choices, or []."""
    ch = _entry_choices(M, a, b)
    free = [x for x in (-1, 0, 1) if ch[x] is None]
    rho = M.rho
    # candidate values for free rates: endpoints and solutions of active constraints
    cands = []
    grids = {x: [rho, F(1)] for x in free}

    def evals(e):
        gH, gL = M.gains(a, b, e)
        return gH - M.kD, gL - M.kD

    import itertools
    base = {x: ch[x] for x in (-1, 0, 1) if ch[x] is not None}
    # enumerate endpoint combinations and one-dimensional solves
    sols = []
    for combo in itertools.product(*[grids[x] for x in free]) if free else [()]:
        e = dict(base)
        e.update(dict(zip(free, combo)))
        sols.append(e)
    # add solves where an indifference binds: vary one free rate at a time
    for x in free:
        for combo in itertools.product(*[grids[y] for y in free if y != x]) if len(free) > 1 else [()]:
            e = dict(base)
            e.update(dict(zip([y for y in free if y != x], combo)))
            for which in ('H', 'L'):
                e_lo = dict(e)
                e_lo[x] = rho
                e_hi = dict(e)
                e_hi[x] = F(1)
                v_lo = evals(e_lo)[0 if which == 'H' else 1]
                v_hi = evals(e_hi)[0 if which == 'H' else 1]
                if v_hi != v_lo:
                    t = -v_lo / (v_hi - v_lo)
                    if 0 <= t <= 1:
                        e_t = dict(e)
                        e_t[x] = rho + t * (1 - rho)
                        sols.append(e_t)
    # two free rates with both indifferences binding
    if len(free) >= 2:
        for x, y in itertools.permutations(free, 2):
            others = [z for z in free if z not in (x, y)]
            for combo in itertools.product(*[grids[z] for z in others]) if others else [()]:
                e = dict(base)
                e.update(dict(zip(others, combo)))
                # linear system in (ex, ey)
                def lin(which):
                    vals = {}
                    for ex in (F(0), F(1)):
                        for ey in (F(0), F(1)):
                            ee = dict(e)
                            ee[x], ee[y] = ex, ey
                            vals[(ex, ey)] = evals(ee)[0 if which == 'H' else 1]
                    c0 = vals[(0, 0)]
                    cx = vals[(1, 0)] - c0
                    cy = vals[(0, 1)] - c0
                    return c0, cx, cy
                h0, hx, hy = lin('H')
                l0, lx, ly = lin('L')
                det = hx * ly - hy * lx
                if det != 0:
                    ex = (-h0 * ly + hy * l0) / det
                    ey = (-hx * l0 + h0 * lx) / det
                    if rho <= ex <= 1 and rho <= ey <= 1:
                        ee = dict(e)
                        ee[x], ee[y] = ex, ey
                        sols.append(ee)
    good = []
    for e in sols:
        if any(not (rho <= e[x] <= 1) for x in (-1, 0, 1)):
            continue
        vH, vL = evals(e)
        if _cond_ok(vH, kindH, strict_full) and _cond_ok(vL, kindL, strict_full):
            good.append(e)
    return good, free


def _label(a, b, lam):
    names = {('zero', 'zero'): 'NT', ('full', 'full'): 'T', ('full', 'zero'): 'BNS', ('zero', 'full'): 'SNB'}
    ka = 'mix' if isinstance(a, Iv) else _kind(a, lam)
    kb = 'mix' if isinstance(b, Iv) else _kind(b, lam)
    if (ka, kb) in names:
        return names[(ka, kb)]
    return {'zero': 'no buy', 'full': 'full buy', 'mix': 'partial buy'}[ka] + ', ' + \
        {'zero': 'no sell', 'full': 'full sell', 'mix': 'partial sell'}[kb]


def _record(M, a, b, e, kind, cert, extra=''):
    out = M.outcomes(a, b, e)
    sig = {x: (e[x] - M.rho) / (1 - M.rho) if not isinstance(e[x], Iv) else (e[x] - M.rho) / (1 - M.rho)
           for x in (-1, 0, 1)}
    cm = [x for x in (-1, 0, 1) if (isinstance(sig[x], Iv) and not (sig[x].hi == 0 or sig[x].lo == 1)) or
          (not isinstance(sig[x], Iv) and 0 < sig[x] < 1)]
    return dict(a=a, b=b, e=e, label=_label(a, b, M.lam), kind=kind, cert=cert, chall_mix=cm, out=out, note=extra)


def enumerate_equilibria(P, belief='IC', investor='M', challenger='X', hidden=False):
    """All equilibria at P. investor in {'M','Z'}; challenger in {'X','E'}.
    hidden=True: the challenger cannot see the price (entry fixed at the prior's level).
    Returns (list of records, list of undecided notes, model)."""
    M = Model(P, belief, hidden)
    lam, rho = M.lam, M.rho
    strict_full = investor == 'Z'
    eqs, undecided = [], []

    def keep_e(e, rec_free):
        """Rule E: tied flows must prepare (sigma = 1)."""
        if challenger == 'X':
            return True
        return all(e[x] == 1 for x in rec_free)

    # ---------------- corners ----------------
    for a in (F(0), lam):
        for b in (F(0), lam):
            good, free = _point_feasible(M, a, b, _kind(a, lam), _kind(b, lam), strict_full)
            good = [e for e in good if keep_e(e, free)]
            if good:
                # report the rule-E selection if feasible, else the first
                pref = [e for e in good if all(e[x] == 1 for x in free)]
                e = (pref or good)[0]
                rec = _record(M, a, b, e, 'corner', 'exact', 'ties at flows %s' % free if free else '')
                if free:
                    Es = sorted(set(M.outcomes(a, b, g)['E'] for g in good))
                    rec['E_range'] = (Es[0], Es[-1])
                eqs.append(rec)
    if investor == 'Z':
        return eqs, undecided, M

    # ---------------- edges ----------------
    edges = [('a', F(0)), ('a', lam), ('b', F(0)), ('b', lam)]  # (fixed variable, value)
    for fixed, val in edges:
        # parametrize: if fixed == 'b', t = a varies (H indifferent); else t = b varies (L indifferent)
        def ab(t):
            return (t, val) if fixed == 'b' else (val, t)
        mover = 'H' if fixed == 'b' else 'L'
        # breakpoints from lines
        bps = []
        for x in ((-1, 0, 1) if not M.hidden else ()):
            Lx = M.L[x]
            if fixed == 'b':
                c1 = Lx.get((1, 0), F(0))
                c0 = Lx.get((0, 0), F(0)) + Lx.get((0, 1), F(0)) * val
            else:
                c1 = Lx.get((0, 1), F(0))
                c0 = Lx.get((0, 0), F(0)) + Lx.get((1, 0), F(0)) * val
            if c1 != 0:
                t0 = -c0 / c1
                if 0 < t0 < lam:
                    bps.append(t0)
        bps = sorted(set(bps))
        pts = [F(0)] + bps + [lam]
        # open sub-intervals
        for lo, hi in zip(pts[:-1], pts[1:]):
            mid = (lo + hi) / 2
            a_m, b_m = ab(mid)
            e = {x: (F(1) if M.sign_L(x, a_m, b_m) > 0 else rho) for x in (-1, 0, 1)}
            if mover == 'H':
                N = M.NH(e[0], e[1], F(0))
                # collapse b = val
                uni = {}
                for (i, j), c in N.items():
                    uni[i] = uni.get(i, F(0)) + c * val ** j
                upoly = utrim([uni.get(i, F(0)) for i in range(max(uni) + 1)]) if uni else []
            else:
                N = M.NL(e[-1], e[0], F(0))
                uni = {}
                for (i, j), c in N.items():
                    uni[j] = uni.get(j, F(0)) + c * val ** i
                upoly = utrim([uni.get(j, F(0)) for j in range(max(uni) + 1)]) if uni else []
            if not upoly:
                undecided.append(f'edge {fixed}={val}: indifference holds on all of ({lo},{hi}) (continuum)')
                continue
            for (l, u) in isolate(upoly, lo, hi):
                tI = Iv(l, u) if l != u else l
                a_, b_ = ab(tI)
                # pattern consistency on the enclosure
                okpat = True
                for x in (-1, 0, 1):
                    s = M.sign_L(x, a_, b_)
                    want = 1 if e[x] == 1 else -1
                    if s is None:
                        okpat = None
                    elif s != want:
                        okpat = False
                if okpat is False:
                    continue
                gH, gL = M.gains(a_, b_, e)
                other = (gL - M.kD) if mover == 'H' else (gH - M.kD)
                other_kind = _kind(val, lam)
                ok = _cond_ok(other, other_kind)
                if ok is False:
                    continue
                if ok is None or okpat is None:
                    undecided.append(f'edge {fixed}={val}, root in [{float(l):.12g},{float(u):.12g}]: undecided sign')
                    continue
                eqs.append(_record(M, a_, b_, e, 'edge', 'exact' if l == u else 'enclosure'))
        # breakpoints with challenger mixing (rule X) or rule-E selection
        for t0 in bps:
            a_, b_ = ab(t0)
            kindH = 'mix' if mover == 'H' else _kind(a_, lam)
            kindL = 'mix' if mover == 'L' else _kind(b_, lam)
            good, free = _point_feasible(M, a_, b_, kindH, kindL, False)
            good = [e for e in good if keep_e(e, free)]
            if good:
                rec = _record(M, a_, b_, good[0], 'edge-line', 'exact', 'ties at flows %s' % free)
                Es = sorted(set(M.outcomes(a_, b_, g)['E'] for g in good))
                rec['E_range'] = (Es[0], Es[-1])
                eqs.append(rec)

    # ---------------- open cells ----------------
    import itertools
    for sig in itertools.product((0, 1), repeat=3):
        e = {x: (F(1) if s else rho) for x, s in zip((-1, 0, 1), sig)}
        NH = M.NH(e[0], e[1])
        NL = M.NL(e[-1], e[0])
        R, (A0, A1, A2, B0, B1, B2) = resultant_a(NH, NL)
        R = utrim(R)
        if not R:
            undecided.append(f'cell {sig}: resultant vanishes identically')
            continue
        den = uadd(umul(A1, B2), uneg(umul(A2, B1)))
        num = uadd(umul(A2, B0), uneg(umul(A0, B2)))
        for (l, u) in isolate(R, F(0), lam):
            bI = Iv(l, u) if l != u else l
            dv = ueval(den, bI)
            if (isinstance(dv, Iv) and dv.lo <= 0 <= dv.hi) or (not isinstance(dv, Iv) and dv == 0):
                # fall back: solve N_H(., b) = 0 directly and test N_L
                undecided.append(f'cell {sig}: degenerate elimination near b in [{float(l):.6g},{float(u):.6g}]')
                continue
            aI = ueval(num, bI) / dv
            if isinstance(aI, Iv):
                if aI.hi <= 0 or aI.lo >= lam:
                    continue
                if aI.lo <= 0 or aI.hi >= lam:
                    undecided.append(f'cell {sig}: root at the boundary a ~ {float(aI.mid()):.6g}')
                    continue
            else:
                if not (0 < aI < lam):
                    continue
            okpat = True
            for x in (-1, 0, 1):
                s = M.sign_L(x, aI, bI)
                want = 1 if sig[(-1, 0, 1).index(x)] else -1
                if s is None:
                    okpat = None
                elif s != want:
                    okpat = False
            if okpat is False:
                continue
            if okpat is None:
                undecided.append(f'cell {sig}: root on a line, b in [{float(l):.6g},{float(u):.6g}]')
                continue
            eqs.append(_record(M, aI, bI, e, 'cell', 'exact' if l == u and not isinstance(aI, Iv) else 'enclosure'))

    if challenger == 'E' or hidden:
        return eqs, undecided, M

    # ---------------- line segments: challenger mixing at one flow ----------------
    for x in (-1, 0, 1):
        Lx = M.L[x]
        ca, cb, c0 = Lx.get((1, 0), F(0)), Lx.get((0, 1), F(0)), Lx.get((0, 0), F(0))
        if ca == 0 and cb == 0:
            continue
        # parametrize the line: if ca != 0, a = alpha + beta * t with t = b; else b = const, t = a
        if ca != 0:
            alpha, beta = -c0 / ca, -cb / ca

            def ab_of(t, alpha=alpha, beta=beta):
                return (alpha + beta * t, t)
            sub = lambda p, alpha=alpha, beta=beta: _sub_a_linear(p, alpha, beta)
        else:
            bconst = -c0 / cb

            def ab_of(t, bconst=bconst):
                return (t, bconst)
            sub = lambda p, bconst=bconst: _sub_b_const(p, bconst)
        # t-range where the point is inside (0, lam)^2
        tlo, thi = _line_range(ca, cb, c0, lam)
        if tlo is None:
            continue
        others = [y for y in (-1, 0, 1) if y != x]
        for so in itertools.product((0, 1), repeat=2):
            base = {y: (F(1) if s else rho) for y, s in zip(others, so)}
            if x == 1:
                eq_poly = sub(M.NL(base[-1], base[0]))      # L indifferent, e1 free
            elif x == -1:
                eq_poly = sub(M.NH(base[0], base[1]))       # H indifferent, e-1 free
            else:
                # both depend on e0: N_H = PH + e0 QH, N_L = PL + e0 QL ; eliminate e0
                PH = sub(M.NH(F(0), base[1]))
                QH = uadd(sub(M.NH(F(1), base[1])), uneg(PH))
                PL = sub(M.NL(base[-1], F(0)))
                QL = uadd(sub(M.NL(base[-1], F(1))), uneg(PL))
                eq_poly = uadd(umul(PH, QL), uneg(umul(PL, QH)))
            eq_poly = utrim(eq_poly)
            if not eq_poly:
                undecided.append(f'line {x}, others {so}: identity (continuum)')
                continue
            for (l, u) in isolate(eq_poly, tlo, thi):
                tI = Iv(l, u) if l != u else l
                a_, b_ = ab_of(tI)
                # pattern of the other flows
                okpat = True
                for y in others:
                    s = M.sign_L(y, a_, b_)
                    want = 1 if base[y] == 1 else -1
                    if s is None:
                        okpat = None
                    elif s != want:
                        okpat = False
                if okpat is False:
                    continue
                if okpat is None:
                    undecided.append(f'line {x}: crossing near t={float(tI.mid() if isinstance(tI, Iv) else tI):.6g}')
                    continue
                # solve the free entry rate from the remaining indifference
                e_lo = dict(base)
                e_lo[x] = rho
                e_hi = dict(base)
                e_hi[x] = F(1)
                gH_lo, gL_lo = M.gains(a_, b_, e_lo)
                gH_hi, gL_hi = M.gains(a_, b_, e_hi)
                if x == 1:
                    lo_v, hi_v = gH_lo - M.kD, gH_hi - M.kD
                elif x == -1:
                    lo_v, hi_v = gL_lo - M.kD, gL_hi - M.kD
                else:
                    lo_v, hi_v = gH_lo - M.kD, gH_hi - M.kD
                # fraction t in [0,1] with lo_v + t (hi_v - lo_v) = 0
                tt = (-lo_v) / (hi_v - lo_v) if not _maybe_zero(hi_v - lo_v) else None
                if tt is None:
                    undecided.append(f'line {x}: flat free-rate response')
                    continue
                inside = _in01(tt)
                if inside is False:
                    continue
                if inside is None:
                    undecided.append(f'line {x}: mixing probability near 0 or 1')
                    continue
                e = dict(base)
                e[x] = rho + tt * (1 - rho)
                if x == 0:
                    # check L's indifference holds too (it must, by elimination)
                    pass
                eqs.append(_record(M, a_, b_, e, 'line', 'enclosure' if isinstance(tI, Iv) or isinstance(tt, Iv) else 'exact'))
    # ---------------- crossings of two lines ----------------
    for x, y in ((-1, 0), (-1, 1), (0, 1)):
        Lx, Ly = M.L[x], M.L[y]
        a1, b1, c1 = Lx.get((1, 0), F(0)), Lx.get((0, 1), F(0)), Lx.get((0, 0), F(0))
        a2, b2, c2 = Ly.get((1, 0), F(0)), Ly.get((0, 1), F(0)), Ly.get((0, 0), F(0))
        det = a1 * b2 - a2 * b1
        if det == 0:
            continue
        a_ = (-c1 * b2 + c2 * b1) / det
        b_ = (-a1 * c2 + a2 * c1) / det
        if 0 < a_ < lam and 0 < b_ < lam:
            good, free = _point_feasible(M, a_, b_, 'mix', 'mix', False)
            if good:
                rec = _record(M, a_, b_, good[0], 'crossing', 'exact', 'ties at flows %s' % free)
                eqs.append(rec)
    return eqs, undecided, M


def _maybe_zero(v):
    if isinstance(v, Iv):
        return v.lo <= 0 <= v.hi
    return v == 0


def _in01(t):
    if isinstance(t, Iv):
        if t.lo > 0 and t.hi < 1:
            return True
        if t.hi < 0 or t.lo > 1:
            return False
        return None
    return 0 < t < 1 if not (t == 0 or t == 1) else None


def _sub_a_linear(p, alpha, beta):
    """Substitute a = alpha + beta t, b = t into bivariate p; returns univariate in t."""
    out = []
    lin = [alpha, beta]
    for (i, j), c in p.items():
        term = [c]
        for _ in range(i):
            term = umul(term, lin)
        term = umul(term, [F(0)] * j + [F(1)])
        out = uadd(out, term)
    return utrim(out)


def _sub_b_const(p, bc):
    out = {}
    for (i, j), c in p.items():
        out[i] = out.get(i, F(0)) + c * bc ** j
    return utrim([out.get(i, F(0)) for i in range(max(out) + 1)]) if out else []


def _line_range(ca, cb, c0, lam):
    """Range of the parameter t on the line inside the open square (0, lam)^2."""
    if ca != 0:
        alpha, beta = -c0 / ca, -cb / ca
        lo, hi = F(0), lam
        # need 0 < alpha + beta t < lam
        if beta == 0:
            if not (0 < alpha < lam):
                return None, None
        else:
            t1, t2 = (0 - alpha) / beta, (lam - alpha) / beta
            lo, hi = max(lo, min(t1, t2)), min(hi, max(t1, t2))
        if lo >= hi:
            return None, None
        return lo, hi
    bconst = -c0 / cb
    if not (0 < bconst < lam):
        return None, None
    return F(0), lam
