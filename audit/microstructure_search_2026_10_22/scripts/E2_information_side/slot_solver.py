"""Complete equilibrium classification of the order slot (two-sided unit menu) with
  - class prior pi, investor signal T of accuracy a (a = 1: the investor sees the class),
  - challenger signal Y of accuracy d (d = 1/2: no private signal),
  - atomic costs {0, c_H} with Pr(0) = rho.
Print-only helpers; the run never stops on a condition.

Equilibrium objects. s = lam * Pr(q = 1 | T = +), t = lam * Pr(q = -1 | T = -).
Wrong-signed orders are strictly dominated: their gross residual is minus a positive number.
A buy reaches Q = 1 with certainty and its return depends on s only; a sale reaches Q = -1 and its
return depends on t only. So the equilibrium set is a product S* x T*.
Tie rules: investor IM (any mixture at indifference); challenger C1 (prepare at indifference).
CM threshold mixtures (challenger mixes at a recruitment threshold) are listed separately.
"""
from fractions import Fraction as Fr
from mpmath import mpf, mp


class SlotModel:
    def __init__(self, F, S, A, pi, a, d, rho, cH, k):
        self.F, self.S, self.A = F, S, A
        self.pi, self.a, self.d = F(pi), F(a), F(d)
        self.rho, self.cH, self.k = F(rho), F(cH), F(k)
        self.lam, self.b, self.c = S["lam"], S["b"], S["c"]
        pi, a = self.pi, self.a
        self.pTp = pi * a + (1 - pi) * (1 - a)
        self.pTm = 1 - self.pTp
        self.hP = pi * a / self.pTp
        self.hM = pi * (1 - a) / self.pTm
        self.exact = isinstance(self.pi, Fr)

    # ---------- beliefs
    def mu_of_lam(self, l):
        return self.hP * l + self.hM * (1 - l)

    def lam_of_mu(self, mu):
        return (mu - self.hM) / (self.hP - self.hM)

    def mu1(self, s):
        l = self.pTp * (self.b + s) / (self.pTp * (self.b + s) + self.pTm * self.b)
        return self.mu_of_lam(l)

    def mum1(self, t):
        l = self.pTp * self.b / (self.pTp * self.b + self.pTm * (self.b + t))
        return self.mu_of_lam(l)

    def mu0(self, s, t):
        cl = self.c + self.lam
        l = self.pTp * (cl - s) / (self.pTp * (cl - s) + self.pTm * (cl - t))
        return self.mu_of_lam(l)

    def s_of_mu(self, mu):
        l = self.lam_of_mu(mu)
        return l * self.pTm * self.b / (self.pTp * (1 - l)) - self.b

    def t_of_mu(self, mu):
        l = self.lam_of_mu(mu)
        return self.pTp * self.b * (1 - l) / (l * self.pTm) - self.b

    def phi(self, y, mu):
        d = self.d
        if y > 0:
            return d * mu / (d * mu + (1 - d) * (1 - mu))
        return (1 - d) * mu / ((1 - d) * mu + d * (1 - mu))

    def Bv(self, mu):
        return self.A["gL"] + mu * (self.A["gH"] - self.A["gL"])

    def ind(self, mu):
        """C1 indicators (I_+, I_-) for high-cost preparation at public posterior mu."""
        return tuple(1 if self.Bv(self.phi(y, mu)) >= self.cH else 0 for y in (1, -1))

    def entry_rates(self, I):
        rho, d = self.rho, self.d
        Ip, Im = I
        eH = rho + (1 - rho) * (d * Ip + (1 - d) * Im)
        eL = rho + (1 - rho) * ((1 - d) * Ip + d * Im)
        return eH, eL

    def DeltaP(self, I):
        eH, eL = self.entry_rates(I)
        return eH * self.A["wH"] - eL * self.A["wL"]

    def thresholds_mu(self):
        """Public posteriors at which I_+ or I_- switches (phi_y(mu) = tau), when tau is in (0, 1)."""
        A, d = self.A, self.d
        tau = (self.cH - A["gL"]) / (A["gH"] - A["gL"])
        out = []
        if 0 < tau < 1:
            out.append(tau * (1 - d) / (d * (1 - tau) + tau * (1 - d)))  # phi_+ = tau
            out.append(tau * d / ((1 - d) * (1 - tau) + tau * d))  # phi_- = tau
        return sorted(set(out)), tau

    # ---------- returns
    def Rbuy(self, s, I=None):
        mu = self.mu1(s)
        I = self.ind(mu) if I is None else I
        return (self.hP - mu) * self.DeltaP(I)

    def Rsell(self, t, I=None):
        mu = self.mum1(t)
        I = self.ind(mu) if I is None else I
        return (mu - self.hM) * self.DeltaP(I)

    def _close(self, x, y):
        if self.exact:
            return x == y
        return abs(x - y) <= mpf(10) ** (-30)

    def one_side(self, side):
        """All equilibrium rates on one side. Returns (C1 list, CM-only list).
        Each C1 item: (rate, kind). Each CM item: (rate, mixing description)."""
        lam, k = self.lam, self.k
        if side == "buy":
            R, mu_of, rate_of_mu = self.Rbuy, self.mu1, self.s_of_mu
            gap = lambda mu: self.hP - mu
        else:
            R, mu_of, rate_of_mu = self.Rsell, self.mum1, self.t_of_mu
            gap = lambda mu: mu - self.hM
        mus, _ = self.thresholds_mu()
        brk = []
        for m_ in mus:
            if not (self.hM < m_ < self.hP):
                continue
            x = rate_of_mu(m_)
            if 0 < x < lam:
                brk.append((x, m_))
        brk.sort()
        cuts = [self.F(0)] + [x for x, _ in brk] + [lam]
        c1, cm = [], []
        if R(self.F(0)) <= k:
            c1.append((self.F(0), "zero"))
        if R(lam) >= k:
            c1.append((lam, "full"))
        # interior roots on each piece (state taken at the piece midpoint; checked again at the root)
        for x0, x1 in zip(cuts, cuts[1:]):
            mid = (x0 + x1) / 2
            I = self.ind(mu_of(mid))
            D = self.DeltaP(I)
            mu_star = (self.hP - k / D) if side == "buy" else (self.hM + k / D)
            if not (self.hM < mu_star < self.hP):
                continue
            x = rate_of_mu(mu_star)
            if 0 < x < lam and x0 <= x <= x1 and self.ind(mu_of(x)) == I and self._close(R(x), k):
                c1.append((x, f"interior, state {I}"))
        # CM threshold mixtures
        for x, m_ in brk:
            i = cuts.index(x)
            I_a = self.ind(mu_of(x - (x - cuts[i - 1]) / 1000))
            I_b = self.ind(mu_of(x + (cuts[i + 1] - x) / 1000))
            I_c1 = self.ind(mu_of(x))
            D_a, D_b = self.DeltaP(I_a), self.DeltaP(I_b)
            need = k / gap(m_)
            if D_a != D_b and min(D_a, D_b) <= need <= max(D_a, D_b) and not self._close(need, self.DeltaP(I_c1)):
                z = (need - D_a) / (D_b - D_a)
                cm.append((x, f"challenger mixes: weight {fmt(z, 6)} on state {I_b}, rest on {I_a}"))
        return c1, cm

    # ---------- outcomes
    def outcome(self, s, t):
        F, lam, b, c, pi = self.F, self.lam, self.b, self.c, self.pi
        a = self.a
        # class-conditional flow laws
        PQ_Tp = {1: b + s, 0: c + lam - s, -1: b}
        PQ_Tm = {1: b, 0: c + lam - t, -1: b + t}
        mus = {1: self.mu1(s), 0: self.mu0(s, t), -1: self.mum1(t)}
        eH = eL = F(0)
        rows = {}
        for x in (1, 0, -1):
            pH = a * PQ_Tp[x] + (1 - a) * PQ_Tm[x]
            pL = (1 - a) * PQ_Tp[x] + a * PQ_Tm[x]
            I = self.ind(mus[x])
            eHx, eLx = self.entry_rates(I)
            eH += pH * eHx
            eL += pL * eLx
            P = self.A["t0"] + mus[x] * eHx * self.A["wH"] + (1 - mus[x]) * eLx * self.A["wL"]
            rows[x] = dict(mu=mus[x], I=I, P=P, pH=pH, pL=pL)
        E = pi * eH + (1 - pi) * eL
        RT = self.A["t0"] + pi * eH * self.A["wH"] + (1 - pi) * eL * self.A["wL"]
        return dict(E=E, eH=eH, eL=eL, OH=pi * eH, RT=RT, rows=rows)

    def equilibria(self):
        Sb, Sbm = self.one_side("buy")
        Ts, Tsm = self.one_side("sell")
        eq = [(s, t, ks, kt) for s, ks in Sb for t, kt in Ts]
        return eq, Sbm, Tsm

    # ---------- brute-force verification from the joint law
    def verify(self, s, t):
        """Recompute posteriors, prices, joint posteriors and investor payoffs by summing over
        (J, T, identity, order, Y, C). Returns max errors and the best-response gains."""
        F, lam, beta = self.F, self.S["lam"], self.S["beta"]
        pi, a, d, rho, cH, k = self.pi, self.a, self.d, self.rho, self.cH, self.k
        A = self.A
        sig = {1: {1: s / lam, 0: 1 - s / lam, -1: F(0)}, -1: {1: F(0), 0: 1 - t / lam, -1: t / lam}}
        liq = {1: beta, 0: 1 - 2 * beta, -1: beta}
        joint = {}  # (J, T, Q, Y) -> prob
        for J, pJ in (("H", pi), ("L", 1 - pi)):
            for T in (1, -1):
                pT = (a if T == 1 else 1 - a) if J == "H" else ((1 - a) if T == 1 else a)
                for Q in (1, 0, -1):
                    pQ = lam * sig[T][Q] + (1 - lam) * liq[Q]
                    for Y in (1, -1):
                        pY = (d if Y == 1 else 1 - d) if J == "H" else ((1 - d) if Y == 1 else d)
                        joint[(J, T, Q, Y)] = pJ * pT * pQ * pY

        def pr(**cond):
            tot = F(0)
            for (J, T, Q, Y), p in joint.items():
                if all({"J": J, "T": T, "Q": Q, "Y": Y}[kk] == vv for kk, vv in cond.items()):
                    tot += p
            return tot

        Bv = self.Bv
        prepare = {}  # (Q, Y, C) -> 0/1, using the direct joint posterior Pr(H | Q, Y)
        for Q in (1, 0, -1):
            for Y in (1, -1):
                post = pr(J="H", Q=Q, Y=Y) / pr(Q=Q, Y=Y)
                for C, pC in ((F(0), rho), (cH, 1 - rho)):
                    prepare[(Q, Y, C)] = 1 if C <= Bv(post) else 0
        costs = ((F(0), rho), (cH, 1 - rho))
        w = {"H": A["wH"], "L": A["wL"]}

        def V_given(Q, Jdist):
            """E[V_T | Q, class distribution Jdist] with Y drawn from the class law."""
            tot = F(0)
            for J, pJ in Jdist.items():
                for Y in (1, -1):
                    pY = (d if Y == 1 else 1 - d) if J == "H" else ((1 - d) if Y == 1 else d)
                    for C, pC in costs:
                        tot += pJ * pY * pC * (A["t0"] + prepare[(Q, Y, C)] * w[J])
            return tot

        out = self.outcome(s, t)
        err_mu = err_P = F(0)
        P = {}
        for Q in (1, 0, -1):
            muQ = pr(J="H", Q=Q) / pr(Q=Q)
            P[Q] = V_given(Q, {"H": muQ, "L": 1 - muQ})
            err_mu = max(err_mu, abs(muQ - out["rows"][Q]["mu"]))
            err_P = max(err_P, abs(P[Q] - out["rows"][Q]["P"]))
        # posterior recovery from the price (paper eq. A.34) and the joint update (A.31)
        err_inv = err_phi = F(0)
        for Q in (1, 0, -1):
            I = out["rows"][Q]["I"]
            eH, eL = self.entry_rates(I)
            DP = eH * A["wH"] - eL * A["wL"]
            mu_inv = (P[Q] - A["t0"] - eL * A["wL"]) / DP
            err_inv = max(err_inv, abs(mu_inv - out["rows"][Q]["mu"]))
            for Y in (1, -1):
                direct = pr(J="H", Q=Q, Y=Y) / pr(Q=Q, Y=Y)
                err_phi = max(err_phi, abs(direct - self.phi(Y, out["rows"][Q]["mu"])))
        # investor payoffs: J independent of Q given T
        gains = {}
        for T in (1, -1):
            hT = self.hP if T == 1 else self.hM
            U = {q: (q * (V_given(q, {"H": hT, "L": 1 - hT}) - P[q]) - k * abs(q)) if q != 0 else F(0) for q in (1, 0, -1)}
            cand = sum(sig[T][q] * U[q] for q in (1, 0, -1))
            gains[T] = (max(U.values()) - cand, U)
        prices_distinct = len({P[1], P[0], P[-1]}) == 3 or (out["rows"][1]["mu"] == out["rows"][0]["mu"] == out["rows"][-1]["mu"])
        return dict(err_mu=err_mu, err_P=err_P, err_inv=err_inv, err_phi=err_phi, gains=gains,
                    prices=P, prices_ok=prices_distinct)


def fmt(x, digits=10):
    if isinstance(x, Fr):
        return mp.nstr(mpf(x.numerator) / x.denominator, digits)
    return mp.nstr(x, digits)
