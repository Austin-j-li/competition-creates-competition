"""Independent check of the equilibrium correspondence in memos/B_dlaplace_theory.md (print only).

Two routes, compared at every strength r of a grid:
  brute force: direct sums over integer flows |x| <= 90, a grid of 2001 purchase rates s = lam*beta_H,
               bisection at every sign change of K(s) - k and at every change of the entry pattern;
               the half-line reduction is NOT used;
  analytic:    the closed-form classification of the memo (two posteriors, piecewise K, quadratic roots).
Both list every equilibrium outcome under the conventional rules (investor and challenger may mix at
indifference) and mark which ones survive the zero-at-indifference investor rule and the
enter-at-indifference challenger rule. The script prints mismatches and the strengths at which the
analytic list changes. Nothing is asserted.

Run from the repository root (through the slot wrapper; about one minute):
    bash audit/discrete_exploration_2026_10_21/scripts/_slots/run_slot.sh .venv/bin/python \
        audit/discrete_exploration_2026_10_21/scripts/B_dlaplace_theory/correspondence.py
"""
import time
import numpy as np

H, ELL, P = 10.0, 1.0, 0.5
TOL_S = 1e-6


def auction(r):
    return dict(t0=P * (1 - P / r), tH=r / 2 + P * P / (2 * r), tL=ELL - (ELL * ELL - P * P) / (2 * r),
                gH=H - r / 2 - P * P / (2 * r), gL=(ELL * ELL - P * P) / (2 * r), D=(r - ELL) ** 2 / (2 * r))


class Model:
    def __init__(self, pi, lam, b, cH, rho, k, X=90):
        self.pi, self.lam, self.b, self.cH, self.rho, self.k = pi, lam, b, cH, rho, k
        self.a = np.exp(-1.0 / b)
        self.x = np.arange(-X, X + 2)
        c = (1 - self.a) / (1 + self.a)
        self.f0 = c * self.a ** np.abs(self.x)        # P(Z = x): flow law without a purchase
        self.f1 = c * self.a ** np.abs(self.x - 1)    # P(Z = x - 1): flow law after a purchase
        self.g = 1 / (1 + self.a)
        self.d = 2 * self.g - 1

    # ---------- brute force (direct flow sums) ----------
    def post(self, s):
        s = np.atleast_1d(s)
        pH = (1 - s)[:, None] * self.f0[None, :] + s[:, None] * self.f1[None, :]
        pL = self.f0[None, :]
        return self.pi * pH / (self.pi * pH + (1 - self.pi) * pL)

    def entry_of(self, r, mu):
        o = auction(r)
        return self.rho + (1 - self.rho) * ((o["gL"] + mu * (o["gH"] - o["gL"])) >= self.cH)

    def K_direct(self, r, s, entry=None):
        mu = self.post(s)
        if entry is None:
            entry = self.entry_of(r, mu)
        return auction(r)["D"] * np.sum(self.f1[None, :] * entry * (1 - mu), axis=1), entry

    def bisect_piece(self, r, lo, hi, entry):
        flo = self.K_direct(r, lo, entry[None, :])[0][0] - self.k
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            fm = self.K_direct(r, mid, entry[None, :])[0][0] - self.k
            if (fm > 0) == (flo > 0):
                lo, flo = mid, fm
            else:
                hi = mid
        return 0.5 * (lo + hi)

    def switch_points(self, r, lo, hi, flows):
        """For each flow index in flows, the purchase rate in [lo, hi] at which its entry changes."""
        out = []
        o = auction(r)
        for j in flows:
            a_, b_ = lo, hi
            e_lo = (o["gL"] + self.post(a_)[0, j] * (o["gH"] - o["gL"])) >= self.cH
            for _ in range(80):
                mid = 0.5 * (a_ + b_)
                e_mid = (o["gL"] + self.post(mid)[0, j] * (o["gH"] - o["gL"])) >= self.cH
                if e_mid == e_lo:
                    a_ = mid
                else:
                    b_ = mid
            out.append(0.5 * (a_ + b_))
        return np.array(out)

    def brute(self, r, ns=2001):
        """Return the list of equilibria (kind, s, zeta) under the conventional rules, and the jump spread."""
        k = self.k
        s = np.linspace(0.0, self.lam, ns)
        Kv, ent = self.K_direct(r, s)
        eqs, spread = [], 0.0
        if Kv[0] <= k:
            eqs.append(("NT", 0.0, None, Kv[0] - k))
        if Kv[-1] >= k:
            eqs.append(("full", self.lam, None, Kv[-1] - k))
        jump = np.any(ent[1:] != ent[:-1], axis=1)
        cross = (Kv[:-1] - k) * (Kv[1:] - k) < 0
        for i in np.where(jump | cross)[0]:
            if not jump[i]:
                eqs.append(("mixed", self.bisect_piece(r, s[i], s[i + 1], ent[i]), None, 0.0))
                continue
            changed = np.where(ent[i] != ent[i + 1])[0]
            sw = self.switch_points(r, s[i], s[i + 1], changed)
            spread = max(spread, float(sw.max() - sw.min()))
            sl, sr = float(sw.min()), float(sw.max())
            KL = self.K_direct(r, sl, ent[i][None, :])[0][0]
            KR = self.K_direct(r, sr, ent[i + 1][None, :])[0][0]
            if (Kv[i] - k) * (KL - k) < 0:
                eqs.append(("mixed", self.bisect_piece(r, s[i], sl, ent[i]), None, 0.0))
            if (KR - k) * (Kv[i + 1] - k) < 0:
                eqs.append(("mixed", self.bisect_piece(r, sr, s[i + 1], ent[i + 1]), None, 0.0))
            if min(KL, KR) <= k <= max(KL, KR):
                zeta = (k - KL) / (KR - KL)
                eqs.append(("mixed+challenger", 0.5 * (sl + sr), zeta, 0.0))
        return eqs, spread

    # ---------- analytic classification (closed forms of the memo) ----------
    def Np(self, s):
        return 1 - self.g + self.pi * self.d * s

    def Nm(self, s):
        return self.g - self.pi * self.d * s

    def mu_up(self, s):
        return self.pi * (1 - self.g + self.d * s) / self.Np(s)

    def K_closed(self, r, s, eu):
        kap = (1 - self.pi) * self.g * (1 - self.g)
        return auction(r)["D"] * kap * (eu / self.Np(s) + self.rho / self.Nm(s))

    def analytic(self, r):
        k, rho, lam = self.k, self.rho, self.lam
        o = auction(r)
        tau = (self.cH - o["gL"]) / (o["gH"] - o["gL"])
        ss = None
        if self.pi < tau < self.mu_up(lam):
            ss = (1 - self.g) * (tau - self.pi) / (self.pi * self.d * (1 - tau))
        eqs = []
        K0 = self.K_closed(r, 0.0, rho)
        if K0 <= k:
            eqs.append(("NT", 0.0, None, K0 - k))
        eu_full = 1.0 if ss is not None else (1.0 if tau <= self.pi else rho)
        KF = self.K_closed(r, lam, eu_full)
        if KF >= k:
            eqs.append(("full", lam, None, KF - k))
        pieces = [(0.0, ss, rho), (ss, lam, 1.0)] if ss is not None else [(0.0, lam, eu_full)]
        kap = (1 - self.pi) * self.g * (1 - self.g)
        q = k / (o["D"] * kap)
        for lo, hi, eu in pieces:
            # q y^2 - (q d - rho + eu) y - q g(1-g) + eu g + rho(1-g) = 0, with y = pi d s
            A2, A1, A0 = q, -(q * self.d - rho + eu), -q * self.g * (1 - self.g) + eu * self.g + rho * (1 - self.g)
            disc = A1 * A1 - 4 * A2 * A0
            if disc < 0:
                continue
            for y in [(-A1 - np.sqrt(disc)) / (2 * A2), (-A1 + np.sqrt(disc)) / (2 * A2)]:
                sv = y / (self.pi * self.d)
                if lo + 1e-12 < sv < hi - 1e-12:
                    eqs.append(("mixed", sv, None, 0.0))
        if ss is not None:
            KL, KR = self.K_closed(r, ss, rho), self.K_closed(r, ss, 1.0)
            if KL <= k <= KR:
                eqs.append(("mixed+challenger", ss, (k - KL) / (KR - KL), 0.0))
        return eqs, ss


def survives(kind, margin, rule_inv, rule_ch):
    """Which equilibria survive a tie-rule pair. I0: investor chooses zero at indifference."""
    if rule_inv == "I0" and kind in ("mixed", "mixed+challenger"):
        return False
    if rule_inv == "I0" and kind == "full" and margin <= 0:
        return False
    if rule_ch == "C1" and kind == "mixed+challenger":
        return False
    return True


def signature(eqs, rule_inv, rule_ch):
    kinds = sorted(e[0] for e in eqs if survives(e[0], e[3], rule_inv, rule_ch))
    return "+".join(kinds) if kinds else "NONE"


def match(e1, e2):
    if len(e1) != len(e2):
        return False
    a = sorted((e[0], round(e[1], 5)) for e in e1)
    b = sorted((e[0], round(e[1], 5)) for e in e2)
    return all(x[0] == y[0] and abs(x[1] - y[1]) < 1e-4 for x, y in zip(a, b))


def run(label, m, rgrid):
    t0 = time.time()
    mism, worst_spread, worst_ds = 0, 0.0, 0.0
    sig_prev = {rp: None for rp in [("IM", "CM"), ("IM", "C1"), ("I0", "CM")]}
    print(f"\n=== {label}: pi={m.pi}, lam={m.lam}, b={m.b}, c_H={m.cH:.10g}, rho={m.rho}, k={m.k} ===")
    changes = []
    for r in rgrid:
        o = auction(r)
        if o["gL"] + m.pi * (o["gH"] - o["gL"]) >= m.cH:
            continue  # prior recruits; outside the stated domain
        eb, spread = m.brute(r)
        ea, ss = m.analytic(r)
        worst_spread = max(worst_spread, spread)
        if not match(eb, ea):
            mism += 1
            if mism <= 8:
                print(f"  MISMATCH r={r:.4f}: brute={[(e[0], round(e[1], 6)) for e in eb]} analytic={[(e[0], round(e[1], 6)) for e in ea]}")
        else:
            for x, y in zip(sorted(eb, key=lambda e: (e[0], e[1])), sorted(ea, key=lambda e: (e[0], e[1]))):
                worst_ds = max(worst_ds, abs(x[1] - y[1]))
        for rp in sig_prev:
            sg = signature(ea, *rp)
            if sg != sig_prev[rp]:
                changes.append((rp, r, sg))
                sig_prev[rp] = sg
    print(f"  grid points: {len(rgrid)}; mismatches brute vs analytic: {mism}; largest |s difference| on matches: {worst_ds:.2e};"
          f" largest spread of entry-switch points across flows: {worst_spread:.2e}; time {time.time() - t0:.1f}s")
    for rp in sig_prev:
        print(f"  rules {rp[0]}/{rp[1]}: regions (first grid strength with each new equilibrium list)")
        for (rr, r, sg) in [c for c in changes if c[0] == rp]:
            print(f"     from r = {r:.4f}: {sg}")


def window_mid(pi, b, r0=1.2, r1=3.0):
    a = np.exp(-1 / b)
    M1 = pi / (pi + (1 - pi) * a)
    o0, o1 = auction(r0), auction(r1)
    lo = o0["gL"] + pi * (o0["gH"] - o0["gL"])
    hi = o1["gL"] + M1 * (o1["gH"] - o1["gL"])
    return 0.5 * (lo + hi)


def main():
    rgrid = np.round(np.arange(1.0025, 6.0001, 0.0025), 6)
    run("benchmark", Model(0.5, 1.0, 2.0, 5.0, 0.25, 0.02), rgrid)
    run("variant c_H = 5.2", Model(0.5, 1.0, 2.0, 5.2, 0.25, 0.02), rgrid)
    run("prior 0.3", Model(0.3, 1.0, 2.0, window_mid(0.3, 2.0), 0.25, 0.02), rgrid)
    run("prior 0.7", Model(0.7, 1.0, 2.0, window_mid(0.7, 2.0), 0.25, 0.02), rgrid)
    run("presence 0.8", Model(0.5, 0.8, 2.0, 5.0, 0.25, 0.02), rgrid)
    # a case without feedback (rho close to one) and a high trading cost: the zero-at-indifference
    # investor rule can leave no equilibrium where K_F <= k < K_0
    run("no-feedback case rho = 0.95, k = 0.3", Model(0.5, 1.0, 2.0, 5.0, 0.95, 0.3), rgrid)


if __name__ == "__main__":
    main()
