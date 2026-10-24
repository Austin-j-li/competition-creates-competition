"""C4 core: two potential challengers in sequence, discrete-Laplace noise, buy-only orders.

Model (memo C4_sequential.md, Section 2):
  state s = (j1, j2) in {HH, HL, LH, LL}; prior pi_HH = pi_LL = (1+kappa)/4, pi_HL = pi_LH = (1-kappa)/4.
  Round t: short-lived informed investor buys (q=1) or not; flow X = q + Z, Z discrete Laplace,
  P(Z=z) = (1-a)/(1+a) a^|z|, a = exp(-1/b).  The flow matters only through S = 1{X >= 1}:
      P(S=g | s, beta) = (a + beta (1-a)) / (1+a);  a buyer reaches g with prob 1/(1+a).
  Round 1: challenger 1 sees P1 and its cost, decides d1 (public).
  Round 2: challenger 2 sees P1, d1, P2 and its cost, decides d2.
  Auction: second-price, reserve p, incumbent R ~ U[0, r], prepared challengers with values in {l, h}.

Equilibrium search (print-only):
  * For a fixed entry pattern, every investor type's buy margin is U_s - K(beta), where
    U_s = sum_S P(S | buy) V_s(S) and K(beta) = sum_S P(S | buy) P(S; beta) + k is common to all types.
    Best responses therefore follow the order of U_s: buyers are the top classes; at most one class
    (a set of types with equal U_s) can mix.  Types with equal U_s use the same mixture (memo 2.4).
  * Challenger mixing at an exact tie (gain = c_H) is searched with one mixing investor class.
Tie rules: challenger prepares at indifference; the selected investor rule is no trade at indifference,
and the correspondence also lists investor mixtures.
"""
import math
from itertools import product

import numpy as np

ST = ('HH', 'HL', 'LH', 'LL')
SIG = ('g', 'b')
TOL = 1e-10


class Model:
    def __init__(self, r, cH, kappa=0.0, h=10.0, l=1.0, p=0.5, rho=0.25, k=0.02, b=2.0):
        self.r, self.cH, self.kappa, self.h, self.l, self.p = r, cH, kappa, h, l, p
        self.rho, self.k, self.b = rho, k, b
        a = math.exp(-1.0 / b)
        self.a = a
        self.prior = {'HH': (1 + kappa) / 4, 'HL': (1 - kappa) / 4, 'LH': (1 - kappa) / 4, 'LL': (1 + kappa) / 4}
        t0 = p * (1 - p / r)
        tH = r / 2 + p * p / (2 * r)
        tL = l - (l * l - p * p) / (2 * r)
        gH = h - tH
        gL = (l * l - p * p) / (2 * r)
        DT = (r - l) ** 2 / (2 * r)
        self.t0, self.tH, self.tL, self.gH, self.gL, self.DT = t0, tH, tL, gH, gL, DT
        self.D = gH - gL
        self.t = {'H': tH, 'L': tL}
        self.g = {'H': gH, 'L': gL}
        self.T = {'HH': h, 'HL': l + DT, 'LH': l + DT, 'LL': l}
        # terminal value given s, d1, and challenger 2 entry probability e: base + e * inc
        self.base = {1: {s: self.t[s[0]] for s in ST}, 0: {s: t0 for s in ST}}
        self.inc = {1: {s: self.T[s] - self.t[s[0]] for s in ST}, 0: {s: self.t[s[1]] - t0 for s in ST}}
        self.pbuy = {'g': 1 / (1 + a), 'b': a / (1 + a)}
        # allocation values
        self.A0 = (r * r - p * p) / (2 * r)
        self.Al = l + DT
        self.Ah = h

    # ---------- signals and beliefs ----------
    def psig(self, S, beta):
        pg = (self.a + beta * (1 - self.a)) / (1 + self.a)
        return pg if S == 'g' else 1 - pg

    def post(self, nu, beta, S):
        w = {s: nu[s] * self.psig(S, beta[s]) for s in ST}
        z = sum(w.values())
        return {s: w[s] / z for s in ST}

    def gain2(self, d1, mu):
        """Challenger 2's expected gross gain at posterior mu over states."""
        if d1 == 1:
            return self.D * mu['LH']
        return self.gL + self.D * (mu['HH'] + mu['LH'])

    def B(self, mu_high):
        return self.gL + self.D * mu_high

    # ---------- round 2 ----------
    def _r2_eval(self, nu, d1, beta, e):
        mu = {S: self.post(nu, beta, S) for S in SIG}
        V = {S: {s: self.base[d1][s] + e[S] * self.inc[d1][s] for s in ST} for S in SIG}
        P = {S: sum(mu[S][s] * V[S][s] for s in ST) for S in SIG}
        U = {s: sum(self.pbuy[S] * V[S][s] for S in SIG) for s in ST}
        K = sum(self.pbuy[S] * P[S] for S in SIG) + self.k
        Pi = {s: U[s] - K for s in ST}
        Gam = {S: self.gain2(d1, mu[S]) for S in SIG}
        return mu, V, P, Pi, Gam

    def _entry_ok(self, Gam, e, tie_mix=None):
        for S in SIG:
            if tie_mix == S:
                if abs(Gam[S] - self.cH) > 1e-8:
                    return False
                continue
            want = 1.0 if Gam[S] >= self.cH else self.rho
            if abs(e[S] - want) > 1e-12:
                return False
        return True

    def _inv_ok(self, beta, Pi, mixing):
        """Correspondence check. Returns (ok, strict) where strict means pure with strict margins."""
        strict = True
        for s in ST:
            if s in mixing:
                if abs(Pi[s]) > 1e-8:
                    return False, False
                strict = False
            elif beta[s] == 1.0:
                if Pi[s] < -TOL:
                    return False, False
                if Pi[s] <= TOL:
                    strict = False
            else:
                if Pi[s] > TOL:
                    return False, False
                if Pi[s] >= -TOL:
                    strict = False
        return True, strict

    def _classes(self, U):
        order = sorted(ST, key=lambda s: -U[s])
        classes = []
        for s in order:
            if classes and abs(U[classes[-1][0]] - U[s]) <= 1e-12:
                classes[-1].append(s)
            else:
                classes.append([s])
        return classes

    def _scan_roots(self, f, lo=0.0, hi=1.0, n=400):
        xs = np.linspace(lo, hi, n + 1)[1:-1]
        vals = np.array([f(x) for x in xs])
        roots = []
        for i in range(len(xs) - 1):
            if vals[i] == 0.0:
                roots.append(xs[i])
            elif vals[i] * vals[i + 1] < 0:
                a_, b_ = xs[i], xs[i + 1]
                fa = vals[i]
                for _ in range(80):
                    m = 0.5 * (a_ + b_)
                    fm = f(m)
                    if fa * fm <= 0:
                        b_ = m
                    else:
                        a_, fa = m, fm
                roots.append(0.5 * (a_ + b_))
        return roots

    def gain2_range(self, nu, d1):
        """Bounds on challenger 2's gain over every round-2 strategy profile (one-round likelihood bound)."""
        a = self.a
        if d1 == 1:
            q = nu['LH']
            hi = self.D * q / (q + a * (1 - q))
            lo = self.D * q * a / (q * a + (1 - q))
        else:
            q = nu['HH'] + nu['LH']
            hi = self.B(q / (q + a * (1 - q)))
            lo = self.B(q * a / (q * a + (1 - q)))
        return lo, hi

    def round2(self, nu, d1, nscan=200):
        """All round-2 equilibria at public prior nu after decision d1 (correspondence)."""
        rho = self.rho
        out = []
        seen = set()
        lo, hi = self.gain2_range(nu, d1)
        # entry values that some strategy profile can support at a signal
        feas = [x for x, okk in ((rho, lo < self.cH), (1.0, hi >= self.cH)) if okk]
        tie_possible = lo <= self.cH <= hi

        def record(beta, e, mixing, tie_mix):
            mu, V, P, Pi, Gam = self._r2_eval(nu, d1, beta, e)
            if not self._entry_ok(Gam, e, tie_mix):
                return
            ok, strict = self._inv_ok(beta, Pi, mixing)
            if not ok:
                return
            key = tuple(round(beta[s], 7) for s in ST) + tuple(round(e[S], 7) for S in SIG)
            if key in seen:
                return
            seen.add(key)
            out.append(self._r2_pack(nu, d1, beta, e, mu, V, P, Pi, Gam, mixing, tie_mix, strict))

        for eg, eb in product(feas, repeat=2):
            e = {'g': eg, 'b': eb}
            V = {S: {s: self.base[d1][s] + e[S] * self.inc[d1][s] for s in ST} for S in SIG}
            U = {s: sum(self.pbuy[S] * V[S][s] for S in SIG) for s in ST}
            classes = self._classes(U)
            for m in range(len(classes) + 1):
                beta = {s: 0.0 for s in ST}
                for c in classes[:m]:
                    for s in c:
                        beta[s] = 1.0
                record(dict(beta), e, (), None)
                if m < len(classes):
                    cls = classes[m]

                    def f(x, beta=beta, cls=cls, e=e):
                        bb = dict(beta)
                        for s in cls:
                            bb[s] = x
                        return self._r2_eval(nu, d1, bb, e)[3][cls[0]]
                    for x in self._scan_roots(f, n=nscan):
                        bb = dict(beta)
                        for s in cls:
                            bb[s] = x
                        record(bb, e, tuple(cls), None)
        # challenger mixing at a tie, with one mixing investor class
        if not tie_possible:
            return out
        for Stie in SIG:
            other = 'b' if Stie == 'g' else 'g'
            for eo in feas:
                # the class order depends on e(Stie); try both extreme orders and use the mixing class directly
                for cls in self._candidate_classes(d1):
                    rest = [s for s in ST if s not in cls]
                    for pure in product((0.0, 1.0), repeat=len(rest)):
                        beta = {s: v for s, v in zip(rest, pure)}

                        def gtie(x, beta=beta, cls=cls):
                            bb = dict(beta)
                            for s in cls:
                                bb[s] = x
                            mu = self.post(nu, bb, Stie)
                            return self.gain2(d1, mu) - self.cH
                        if gtie(1e-9) * gtie(1 - 1e-9) > 0:
                            continue  # the gain is monotone in one class's purchase probability
                        for x in self._scan_roots(gtie, n=nscan):
                            bb = dict(beta)
                            for s in cls:
                                bb[s] = x
                            # solve investor indifference of cls for e(Stie): margin is affine in e(Stie)
                            e0 = {Stie: rho, other: eo}
                            e1 = {Stie: 1.0, other: eo}
                            m0 = self._r2_eval(nu, d1, bb, e0)[3][cls[0]]
                            m1 = self._r2_eval(nu, d1, bb, e1)[3][cls[0]]
                            if abs(m1 - m0) < 1e-15:
                                continue
                            et = rho + (1 - rho) * (-m0) / (m1 - m0)
                            if rho + 1e-9 < et < 1 - 1e-9:
                                record(bb, {Stie: et, other: eo}, tuple(cls), Stie)
        return out

    def _candidate_classes(self, d1):
        if d1 == 0:
            return [['HH', 'LH'], ['HL', 'LL']]
        return [[s] for s in ST]

    def r2_build(self, nu, d1, beta, e, mixing=(), tie_mix=None):
        """Round-2 node at given strategies.  Returns (valid, node).  tie_mix: signal where the challenger
        mixes; validity then requires an exact tie there."""
        mu, V, P, Pi, Gam = self._r2_eval(nu, d1, beta, e)
        valid = self._entry_ok(Gam, e, tie_mix)
        ok, strict = self._inv_ok(beta, Pi, mixing)
        node = self._r2_pack(nu, d1, beta, e, mu, V, P, Pi, Gam, mixing, tie_mix, strict and tie_mix is None)
        return valid and ok, node

    def _r2_pack(self, nu, d1, beta, e, mu, V, P, Pi, Gam, mixing, tie_mix, strict):
        # per-state expectations
        ebar = {s: sum(self.psig(S, beta[s]) * e[S] for S in SIG) for s in ST}
        W = {s: sum(self.psig(S, beta[s]) * V[S][s] for S in SIG) for s in ST}
        G1 = {}
        if d1 == 1:
            for s in ST:
                g1 = self.g[s[0]]
                G1[s] = sum(self.psig(S, beta[s]) * (g1 * (1 - e[S]) + (self.D if s == 'HL' else 0.0) * e[S]) for S in SIG)
        prob_trade = sum(nu[s] * beta[s] for s in ST)
        return dict(nu=nu, d1=d1, beta=beta, e=e, mu=mu, P=P, Pi=Pi, Gam=Gam, mixing=mixing,
                    tie_mix=tie_mix, strict=strict, ebar=ebar, W=W, G1=G1, prob_trade=prob_trade)

    # ---------- round 1 ----------
    def _r1_eval(self, alpha, e1, cont):
        """cont[(S, d1)] = selected round-2 equilibrium.  Returns round-1 objects."""
        mu = {S: self.post(self.prior, alpha, S) for S in SIG}
        Y = {S: {s: e1[S] * cont[(S, 1)]['W'][s] + (1 - e1[S]) * cont[(S, 0)]['W'][s] for s in ST} for S in SIG}
        P = {S: sum(mu[S][s] * Y[S][s] for s in ST) for S in SIG}
        U = {s: sum(self.pbuy[S] * Y[S][s] for S in SIG) for s in ST}
        K = sum(self.pbuy[S] * P[S] for S in SIG) + self.k
        Pi = {s: U[s] - K for s in ST}
        Gam = {S: sum(mu[S][s] * cont[(S, 1)]['G1'][s] for s in ST) for S in SIG}
        return mu, Y, P, Pi, Gam

    def _entry1_ok(self, Gam, e1, tie_mix=None):
        for S in SIG:
            if tie_mix == S:
                if abs(Gam[S] - self.cH) > 1e-8:
                    return False
                continue
            want = 1.0 if Gam[S] >= self.cH else self.rho
            if abs(e1[S] - want) > 1e-12:
                return False
        return True

    def continuations(self, alpha):
        mu = {S: self.post(self.prior, alpha, S) for S in SIG}
        return {(S, d): self.round2(mu[S], d) for S in SIG for d in (0, 1)}

    def _signature(self, cont):
        def bc(x):
            return '0' if x == 0.0 else ('1' if x == 1.0 else 'm')

        def ec(x):
            return 'r' if abs(x - self.rho) < 1e-12 else ('1' if x == 1.0 else 't')
        return tuple((kk, ''.join(bc(cont[kk]['beta'][s]) for s in ST), ''.join(ec(cont[kk]['e'][S]) for S in SIG))
                     for kk in sorted(cont))

    def nc_holds(self):
        """No-cascade condition of the memo: c_H > psi2(pi_LH) * D_r."""
        q = self.prior['LH']
        return self.cH > self.D * q / (q + self.a ** 2 * (1 - q))

    def round1(self, mixed=True, nscan=120, fixed=None, ties=True):
        """All round-1 equilibria with pure or one-type-mixing investor 1 (all round-2 selections).

        fixed: types whose round-1 action is pinned by a dominance bound (checked by the caller),
        for example {'HH': 1.0, 'LL': 0.0}.  Only the other types are scanned for mixtures.
        """
        rho = self.rho
        fixed = fixed or {}
        mix_types = [s for s in ST if s not in fixed]
        out = []
        seen = set()
        cache = {}

        def conts(alpha):
            key = tuple(round(alpha[s], 12) for s in ST)
            if key not in cache:
                cache[key] = self.continuations(alpha)
            return cache[key]

        def check_add(alpha, e1, cont, mixing, tie_mix):
            mu, Y, P, Pi, Gam = self._r1_eval(alpha, e1, cont)
            if not self._entry1_ok(Gam, e1, tie_mix):
                return
            ok, strict = self._inv_ok(alpha, Pi, mixing)
            if not ok:
                return
            onkeys = [kk for kk in sorted(cont) if (kk[1] == 1 and e1[kk[0]] > 0) or (kk[1] == 0 and e1[kk[0]] < 1)]
            onpath = tuple((tuple(round(cont[kk]['beta'][s], 6) for s in ST), tuple(round(cont[kk]['e'][S], 6) for S in SIG))
                           for kk in onkeys)
            key = tuple(round(alpha[s], 6) for s in ST) + tuple(round(e1[S], 6) for S in SIG) + onpath
            if key in seen:
                return
            seen.add(key)
            out.append(self._pack(alpha, e1, cont, mu, Y, P, Pi, Gam, mixing, tie_mix, strict))

        def try_profile(alpha, mixing, tie_mix=None, e1_fixed=None):
            C = conts(alpha)
            keys = [(S, d) for S in SIG for d in (0, 1)]
            if any(len(C[kk]) == 0 for kk in keys):
                out.append(dict(alpha=alpha, empty_continuation=[kk for kk in keys if len(C[kk]) == 0]))
                return
            patterns = [e1_fixed] if e1_fixed else [{'g': x, 'b': y} for x, y in product((rho, 1.0), repeat=2)]
            for sel in product(*[range(len(C[kk])) for kk in keys]):
                cont = {kk: C[kk][i] for kk, i in zip(keys, sel)}
                for e1 in patterns:
                    check_add(alpha, e1, cont, mixing, tie_mix)

        for prof in product((0.0, 1.0), repeat=4):
            try_profile(dict(zip(ST, prof)), ())
        if mixed:
            keys = [(S, d) for S in SIG for d in (0, 1)]

            def branches(al):
                """All continuation selections at al, each with a discrete signature."""
                C = conts(al)
                if any(len(C[kk]) == 0 for kk in keys):
                    return []
                res = []
                for sel in product(*[range(len(C[kk])) for kk in keys]):
                    cont = {kk: C[kk][i] for kk, i in zip(keys, sel)}
                    res.append((self._signature(cont), cont))
                return res

            def scan(base_alpha, s_mix, fun, mask=None):
                """fun(al, cont) -> scalar.  Returns roots in (0,1) along continuation branches.
                mask(sig) coarsens the branch signature (used where an entry code switches at the root)."""
                mask = mask or (lambda sg: sg)
                xs = np.linspace(0, 1, nscan + 1)[1:-1]
                data = {}
                for x in xs:
                    al = dict(base_alpha)
                    al[s_mix] = x
                    for sig, cont in branches(al):
                        data.setdefault(mask(sig), []).append((x, fun(al, cont)))
                roots = []
                step = xs[1] - xs[0]
                for sig, pts in data.items():
                    for (x0, v0), (x1, v1) in zip(pts, pts[1:]):
                        if x1 - x0 > 1.5 * step or not (np.isfinite(v0) and np.isfinite(v1)) or v0 * v1 > 0:
                            continue
                        a_, b_, fa = x0, x1, v0
                        ok = True
                        for _ in range(60):
                            mid = 0.5 * (a_ + b_)
                            al = dict(base_alpha)
                            al[s_mix] = mid
                            match = [c for sg, c in branches(al) if mask(sg) == sig]
                            if not match:
                                ok = False
                                break
                            fm = fun(al, match[0])
                            if fa * fm <= 0:
                                b_ = mid
                            else:
                                a_, fa = mid, fm
                        if ok:
                            roots.append(0.5 * (a_ + b_))
                return roots

            for s_mix in mix_types:
                rest = [s for s in ST if s != s_mix]
                for prof in product((0.0, 1.0), repeat=3):
                    base_alpha = dict(zip(rest, prof))
                    if any(base_alpha.get(s) != v for s, v in fixed.items()):
                        continue
                    # investor 1 indifference, challenger 1 pure
                    for eg, eb in product((rho, 1.0), repeat=2):
                        e1 = {'g': eg, 'b': eb}
                        for x in scan(base_alpha, s_mix, lambda al, cont, e1=e1, s_mix=s_mix: self._r1_eval(al, e1, cont)[3][s_mix]):
                            al = dict(base_alpha)
                            al[s_mix] = x
                            try_profile(al, (s_mix,), None, e1)
                    if not ties:
                        continue
                    # challenger 1 mixes at a tie on one signal; investor type s_mix mixes
                    for Stie in SIG:
                        other = 'b' if Stie == 'g' else 'g'
                        for x in scan(base_alpha, s_mix, lambda al, cont, Stie=Stie: self._r1_eval(al, {'g': rho, 'b': rho}, cont)[4][Stie] - self.cH):
                            al = dict(base_alpha)
                            al[s_mix] = x
                            for sig, cont in branches(al):
                                for eo in (rho, 1.0):
                                    lo_ = {Stie: rho, other: eo}
                                    hi_ = {Stie: 1.0, other: eo}
                                    m0 = self._r1_eval(al, lo_, cont)[3][s_mix]
                                    m1 = self._r1_eval(al, hi_, cont)[3][s_mix]
                                    if abs(m1 - m0) < 1e-15:
                                        continue
                                    et = rho + (1 - rho) * (-m0) / (m1 - m0)
                                    if rho + 1e-9 < et < 1 - 1e-9:
                                        try_profile(al, (s_mix,), Stie, {Stie: et, other: eo})
                    # cross-round tie: investor 1 mixes so that challenger 2 is indifferent at (S1, d1, S2),
                    # and challenger 2 mixes there so that investor 1 is indifferent; round-2 investors pure
                    for kk in keys:
                        for S2 in SIG:
                            o2 = 'b' if S2 == 'g' else 'g'
                            idx = SIG.index(S2)

                            def msk(sg, kk=kk, idx=idx):
                                return tuple((k_, b_, (e_[:idx] + '*' + e_[idx + 1:]) if k_ == kk else e_) for k_, b_, e_ in sg)
                            for x in scan(base_alpha, s_mix, lambda al, cont, kk=kk, S2=S2: cont[kk]['Gam'][S2] - self.cH, msk):
                                al = dict(base_alpha)
                                al[s_mix] = x
                                for sig, cont in branches(al):
                                    c = cont[kk]
                                    if c['mixing'] or c['tie_mix']:
                                        continue
                                    if abs(c['Gam'][S2] - self.cH) > 1e-7:
                                        continue
                                    for eg, eb in product((rho, 1.0), repeat=2):
                                        e1 = {'g': eg, 'b': eb}

                                        def marg(e2, c=c, cont=cont, al=al, e1=e1, kk=kk, S2=S2, o2=o2):
                                            _, node = self.r2_build(c['nu'], kk[1], c['beta'], {S2: e2, o2: c['e'][o2]}, (), S2)
                                            cc = dict(cont)
                                            cc[kk] = node
                                            return self._r1_eval(al, e1, cc)[3][s_mix], cc
                                        m0, _ = marg(rho)
                                        m1, _ = marg(1.0)
                                        if abs(m1 - m0) < 1e-15:
                                            continue
                                        et = rho + (1 - rho) * (-m0) / (m1 - m0)
                                        if not (rho + 1e-9 < et < 1 - 1e-9):
                                            continue
                                        valid, node = self.r2_build(c['nu'], kk[1], c['beta'], {S2: et, o2: c['e'][o2]}, (), S2)
                                        if not valid:
                                            continue
                                        cc = dict(cont)
                                        cc[kk] = node
                                        check_add(al, e1, cc, (s_mix,), None)
        return out

    def _scan_roots_nan(self, f, n=120):
        xs = np.linspace(0, 1, n + 1)[1:-1]
        vals = np.array([f(x) for x in xs])
        roots = []
        for i in range(len(xs) - 1):
            v0, v1 = vals[i], vals[i + 1]
            if not (np.isfinite(v0) and np.isfinite(v1)):
                continue
            if v0 * v1 < 0:
                a_, b_, fa = xs[i], xs[i + 1], v0
                for _ in range(60):
                    m = 0.5 * (a_ + b_)
                    fm = f(m)
                    if not np.isfinite(fm):
                        break
                    if fa * fm <= 0:
                        b_ = m
                    else:
                        a_, fa = m, fm
                roots.append(0.5 * (a_ + b_))
        return roots

    def _pack(self, alpha, e1, cont, mu, Y, P, Pi, Gam, mixing, tie_mix, strict):
        rho = self.rho
        pr = self.prior
        # outcome probabilities by state
        E1 = E2 = E12 = OH = 0.0
        proceeds = alloc = 0.0
        cost1 = cost2 = 0.0
        trade1 = sum(pr[s] * alpha[s] for s in ST)
        trade2 = 0.0
        for s in ST:
            for S1 in SIG:
                p1 = pr[s] * self.psig(S1, alpha[s])
                e = e1[S1]
                cost1 += p1 * (e - rho) * self.cH  # high-cost type prepares with prob (e - rho)
                for d1, pd in ((1, e), (0, 1 - e)):
                    if pd <= 0:
                        continue
                    c2 = cont[(S1, d1)]
                    trade2 += p1 * pd * c2['beta'][s]
                    for S2 in SIG:
                        p2 = p1 * pd * self.psig(S2, c2['beta'][s])
                        e2 = c2['e'][S2]
                        cost2 += p2 * (e2 - rho) * self.cH
                        E1 += p2 * d1
                        E2 += p2 * e2
                        E12 += p2 * d1 * e2
                        # proceeds and allocation, averaging over challenger 2's decision
                        for d2, q2 in ((1, e2), (0, 1 - e2)):
                            if q2 <= 0:
                                continue
                            w = p2 * q2
                            proceeds += w * self.value(s, d1, d2)
                            alloc += w * self.allocation(s, d1, d2)
                            OH += w * (1.0 if ((d1 and s[0] == 'H') or (d2 and s[1] == 'H')) else 0.0)
        res = dict(alpha=alpha, e1=e1, cont=cont, mu1=mu, P1=P, Pi1=Pi, Gam1=Gam, mixing=mixing, tie_mix=tie_mix,
                   strict=strict, E1=E1, E2=E2, E12=E12, OH=OH, proceeds=proceeds, alloc=alloc,
                   prepcost=cost1 + cost2, trade1=trade1, trade2=trade2,
                   tradecost=self.k * (trade1 + trade2))
        res['net_surplus'] = alloc - cost1 - cost2
        # conditional entry of challenger 2; undefined (nan) when the conditioning event has probability ~0
        res['p2_given_1'] = E12 / E1 if E1 > 1e-12 else float('nan')
        res['p2_given_0'] = (E2 - E12) / (1 - E1) if E1 < 1 - 1e-12 else float('nan')
        res['pure_all'] = strict and all(cont[kk]['strict'] for kk in cont
                                         if (kk[1] == 1 and e1[kk[0]] > 0) or (kk[1] == 0 and e1[kk[0]] < 1))
        return res

    def value(self, s, d1, d2):
        if d1 and d2:
            return self.T[s]
        if d1:
            return self.t[s[0]]
        if d2:
            return self.t[s[1]]
        return self.t0

    def allocation(self, s, d1, d2):
        classes = []
        if d1:
            classes.append(s[0])
        if d2:
            classes.append(s[1])
        if not classes:
            return self.A0
        return self.Ah if 'H' in classes else self.Al

    # ---------- single-challenger reference (the round-2 game after d1 = 0 at the uniform prior) ----------
    def single(self):
        nu = dict(self.prior)
        res = []
        for eq in self.round2(nu, 0):
            E = sum(nu[s] * eq['ebar'][s] for s in ST)
            res.append(dict(beta=eq['beta'], e=eq['e'], E=E, strict=eq['strict'], mixing=eq['mixing'], tie=eq['tie_mix']))
        return res


def fmt_beta(beta):
    return ' '.join(f'{s}:{beta[s]:.4g}' for s in ST)


def describe(m, eq, indent='  '):
    """Text summary of one full equilibrium."""
    L = []
    L.append(f"{indent}round 1: investor buys [{fmt_beta(eq['alpha'])}]  mixing={eq['mixing'] or '-'}"
             f"  entry1 g={eq['e1']['g']:.4f} b={eq['e1']['b']:.4f}  tie={eq['tie_mix'] or '-'}  pure&strict={eq['pure_all']}")
    for S in SIG:
        mu = eq['mu1'][S]
        L.append(f"{indent}  S1={S}: mu1[{fmt_beta(mu)}] P1={eq['P1'][S]:.6f} Gamma1={eq['Gam1'][S]:.6f}")
    L.append(f"{indent}  margins1 [{fmt_beta(eq['Pi1'])}]")
    for S in SIG:
        for d in (1, 0):
            c = eq['cont'][(S, d)]
            onp = (d == 1 and eq['e1'][S] > 0) or (d == 0 and eq['e1'][S] < 1)
            L.append(f"{indent}  after S1={S}, d1={d}{'' if onp else ' (off path)'}: buys [{fmt_beta(c['beta'])}]"
                     f" entry2 g={c['e']['g']:.4f} b={c['e']['b']:.4f}; Gamma2 g={c['Gam']['g']:.4f} b={c['Gam']['b']:.4f};"
                     f" P2 g={c['P']['g']:.5f} b={c['P']['b']:.5f}; mix={c['mixing'] or '-'} tie={c['tie_mix'] or '-'}")
    L.append(f"{indent}  E1={eq['E1']:.6f} E2={eq['E2']:.6f} both={eq['E12']:.6f} "
             f"P(d2|d1=1)={eq['p2_given_1']:.6f} P(d2|d1=0)={eq['p2_given_0']:.6f} O_H={eq['OH']:.6f}")
    L.append(f"{indent}  proceeds={eq['proceeds']:.6f} alloc={eq['alloc']:.6f} prepcost={eq['prepcost']:.6f} "
             f"net surplus={eq['net_surplus']:.6f} tradecost={eq['tradecost']:.6f}")
    return '\n'.join(L)
