"""Cross-check of the equilibrium classification (Propositions 3 and 5) from the flow law (print only).

For each strength r on a grid, the script solves the two one-dimensional investor problems
from first principles: flow masses, Bayes posteriors, the entry response at each order,
competitive prices, and the class payoffs. It lists every candidate of each kind
(abstain, interior below or above the entry threshold, at the threshold, full order),
keeps the candidates that pass every equilibrium condition, and forms the product of the
two classes. It then compares the result with the table of Proposition 3 and, at other
priors, with the coexistence sets of Proposition 5 and the remark on the other tie rules.

Calibration A (lambda = 6/17, beta = 1/3) uses exact fractions. Calibration B
(1 + u = e, beta = 0.294655) uses outward intervals. At a zero rate the posterior equals
the prior exactly, so every comparison there uses exact fractions in both calibrations;
an exact tie between the prior and the threshold is decided exactly. A condition that an
interval cannot decide is printed as UNDETERMINED.
Run from the repository root:
  .venv/bin/python audit/slot_manuscript_2026_10_23/scripts/P1_core/p1_enumerate.py
"""
from fractions import Fraction as Fr

from mpmath import iv

from p1_common import (HERE, Log, tau, Delta, J, rho, k, r0, r2, beta_B, lam_A, beta_A,
                       ivq, ivends, bisect_root, frak_r, round_dec)

log = Log(HERE / "p1_enumerate.log")


# ------------------------------------------------------------------ number layer
class Exact:
    name = "A (exact)"

    @staticmethod
    def c(x):
        return Fr(x)

    @staticmethod
    def sign(x):
        return (x > 0) - (x < 0)

    @staticmethod
    def fmt(x):
        return round_dec(x, 6)


class Interval:
    name = "B (interval)"

    @staticmethod
    def c(x):
        return ivq(x) if isinstance(x, (int, Fr)) else x

    @staticmethod
    def sign(x):
        if x.a > 0:
            return 1
        if x.b < 0:
            return -1
        if x.a == 0 and x.b == 0:
            return 0
        return None

    @staticmethod
    def fmt(x):
        lo, hi = ivends(x)
        dlo, dhi = round_dec(lo, 6), round_dec(hi, 6)
        return dlo if dlo == dhi else f"{dlo}..{dhi}"


UNDET = []
CTX = {"where": ""}


def cmp(N, a, b):
    """Sign of a - b; exact when both are Fractions; None when an interval cannot decide."""
    if isinstance(a, (int, Fr)) and isinstance(b, (int, Fr)):
        return (a > b) - (a < b)
    s = N.sign(N.c(a) - N.c(b))
    if s is None:
        UNDET.append(CTX["where"])
    return s


def ok_return(s, inv_rule):
    """Investor condition on a traded order: return >= k under IM, > k under I0."""
    return s is not None and (s > 0 or (s == 0 and inv_rule == "IM"))


# ------------------------------------------------------------------ one class problem
def class_candidates(N, r, pi, lam, b, cls, inv_rule, ch_rule):
    """Equilibrium candidates of one class. cls = 'H' (purchase, rate s) or 'L' (sale, rate t).
    Returns a list of (label, rate, posterior at the traded order, entry there or None for 'any')."""
    D_ex, t_ex = Delta(r), tau(r)
    D, t_ = N.c(D_ex), N.c(t_ex)
    om = N.c(pi) / (1 - N.c(pi))
    rhoN, kN = N.c(rho), N.c(k)

    def post(rate):  # posterior at the traded order
        if cls == "H":
            odds = om * (b + rate) / b
        else:
            odds = om * b / (b + rate)
        return odds / (1 + odds)

    def gross(mu, e):  # gross return of the correct order
        return e * D * (1 - mu) if cls == "H" else e * D * mu

    out = []
    # abstain: the traded order has posterior pi exactly (exact arithmetic)
    g1 = D_ex * ((1 - pi) if cls == "H" else pi)  # gross return per unit of entry
    s0 = (pi > t_ex) - (pi < t_ex)
    if s0 < 0:
        e0 = rho
    elif s0 > 0:
        e0 = Fr(1)
    else:  # challenger tie at the prior: C1 prepares; CM may use rho, the entry that best supports abstention
        e0 = Fr(1) if ch_rule == "C1" else rho
    if e0 * g1 <= k:
        out.append(("abstain", N.c(0), N.c(pi), N.c(e0)))
    # full order
    mu = post(N.c(lam) if isinstance(lam, Fr) else lam)
    sf = cmp(N, mu, t_)
    if sf is not None:
        if sf < 0:
            if ok_return(cmp(N, gross(mu, rhoN), kN), inv_rule):
                out.append(("full-floor", lam, mu, rhoN))
        elif sf > 0:
            if ok_return(cmp(N, gross(mu, N.c(1)), kN), inv_rule):
                out.append(("full-full", lam, mu, N.c(1)))
        elif ch_rule == "C1":
            if ok_return(cmp(N, gross(mu, N.c(1)), kN), inv_rule):
                out.append(("full-full", lam, mu, N.c(1)))
        else:  # CM tie at the full-order posterior: some entry in [rho, 1] must support the order
            if ok_return(cmp(N, gross(mu, N.c(1)), kN), inv_rule):
                out.append(("full-tie", lam, mu, None))
    if inv_rule == "IM":
        # interior, below and above the threshold: gross(mu, e) = k
        for tag, e, e_ex in (("floor", rhoN, rho), ("full", N.c(1), Fr(1))):
            target_ex = k / (e_ex * D_ex)
            if (1 - target_ex if cls == "H" else target_ex) == pi:
                continue  # the root posterior equals the prior: the rate is exactly zero, not interior
            target = kN / (e * D)  # = 1 - mu for H, mu for L
            mu_star = 1 - target if cls == "H" else target
            if N.sign(mu_star) is not None and N.sign(mu_star) <= 0:
                continue
            if N.sign(1 - mu_star) is not None and N.sign(1 - mu_star) <= 0:
                continue
            odds = mu_star / (1 - mu_star)
            rate = b * (odds / om - 1) if cls == "H" else b * (om / odds - 1)
            ok_rate = cmp(N, rate, 0) == 1 and cmp(N, rate, lam) == -1
            side = cmp(N, mu_star, t_)
            ok_side = (side == -1) if tag == "floor" else (side == 1)
            if ok_rate and ok_side:
                out.append(("interior-" + tag, rate, mu_star, e))
        # at the threshold (a threshold equal to the prior gives the rate zero exactly)
        if t_ex == pi:
            return out
        odds_t = t_ / (1 - t_)
        rate = b * (odds_t / om - 1) if cls == "H" else b * (om / odds_t - 1)
        if cmp(N, rate, 0) == 1 and cmp(N, rate, lam) == -1:
            ret_full = gross(t_, N.c(1))
            if ch_rule == "C1":
                if cmp(N, ret_full, kN) == 0:
                    out.append(("threshold", rate, t_, N.c(1)))
            else:
                estar = kN / ret_full
                if cmp(N, estar, rhoN) >= 0 and cmp(N, estar, 1) <= 0:
                    out.append(("threshold", rate, t_, estar))
    return out


def equilibria(N, r, pi, lam, b, inv_rule, ch_rule):
    CTX["where"] = f"calibration {N.name}, prior {pi}, r = {r}, rules {inv_rule}/{ch_rule}"
    Hc = class_candidates(N, r, pi, lam, b, "H", inv_rule, ch_rule)
    Lc = class_candidates(N, r, pi, lam, b, "L", inv_rule, ch_rule)
    b0 = (1 - lam) - 2 * b
    t_ex = tau(r)
    t_ = N.c(t_ex)
    om = N.c(pi) / (1 - N.c(pi))
    piN = N.c(pi)
    eqs = []
    for hl, s, muP, eP in Hc:
        for ll, t, muM, eM in Lc:
            if hl == "abstain" and ll == "abstain":
                s0 = (pi > t_ex) - (pi < t_ex)  # the zero-order posterior is pi exactly
            else:
                odds0 = om * (b0 + lam - s) / (b0 + lam - t)
                s0 = cmp(N, odds0 / (1 + odds0), t_)
            if s0 is None:
                eqs.append((hl, ll, None, None, "zero order undetermined"))
                continue
            # entry after the zero order enters no payoff; at a tie C1 prepares and CM may use rho
            e0 = N.c(rho) if s0 == -1 else (N.c(1) if (s0 == 1 or ch_rule == "C1") else N.c(rho))
            if eP is None or eM is None:
                eqs.append((hl, ll, None, None, "entry after a traded order is any value in a range"))
                continue
            prP = piN * (b + s) + (1 - piN) * b
            prM = piN * b + (1 - piN) * (b + t)
            pr0 = 1 - prP - prM
            Ent = prP * eP + prM * eM + pr0 * e0
            own = piN * ((b + s) * eP + b * eM + (b0 + lam - s) * e0)
            z = "zero order recruits" if s0 == 1 else ("zero order tie" if s0 == 0 else "zero order floor")
            eqs.append((hl, ll, Ent, own, z))
    return eqs


def label(hl, ll):
    H = {"abstain": "H0", "interior-floor": "Hmix-floor", "interior-full": "Hmix-recruit",
         "threshold": "Hthreshold", "full-full": "Hfull-recruit", "full-floor": "Hfull-floor",
         "full-tie": "Hfull-tie"}[hl]
    L = {"abstain": "L0", "interior-floor": "Lmix", "full-floor": "Lfull", "interior-full": "Lmix-recruit",
         "threshold": "Lthreshold", "full-full": "Lfull-recruit", "full-tie": "Lfull-tie"}[ll]
    return H + "/" + L


# ------------------------------------------------------------------ predicted table at prior 1/2
def predicted(r, th, inv_rule, ch_rule):
    rA, rF, rN, rJ, rS, rC = th
    out = set()
    if r <= rN:
        out.add("H0/L0")
    if rA < r < rF and inv_rule == "IM":
        out.add("Hmix-recruit/L0")
    if rF < r <= rN or (r == rF and inv_rule == "IM"):
        out.add("Hfull-recruit/L0")
    if rN < r < rS and inv_rule == "IM":
        out.add("Hfull-recruit/Lmix")
        if r < rJ:
            out.add("Hmix-floor/Lmix")
    if rS < r < rC or (r == rS and inv_rule == "IM"):
        out.add("Hfull-recruit/Lfull")
    if r > rC:
        out.add("Hfull-floor/Lfull")
    if ch_rule == "CM" and inv_rule == "IM" and rA < r < rJ:
        out.add("Hthreshold/L0" if r <= rN else "Hthreshold/Lmix")
    return out


def thresholds(M):
    """Threshold displays for the grid comparison (no grid point lies within 1e-6 of a threshold)."""
    rA = bisect_root(lambda r: J(r) - k, r0, r2)[0]
    rJ = bisect_root(lambda r: rho * J(r) - k, r0, r2)[0]
    if isinstance(M, Fr):
        rF = frak_r(ivq(k / (1 - M))).a
        rS = frak_r(ivq(k / (rho * (1 - M)))).a
        rC = bisect_root(lambda r: tau(r) - M, Fr(3), r2)[0]
    else:
        rF = frak_r(ivq(k) / (1 - M)).a
        rS = frak_r(ivq(k) / (ivq(rho) * (1 - M))).a
        a_ = M * 10 - 6  # closed form of B_r(M) = c_H at the benchmark (h = 10, c_H = 6, ell = 1, p = 1/2)
        rC = (a_ + iv.sqrt(a_ * a_ + M * ((1 - M) - ivq(Fr(1, 4))))) / M
    rN = frak_r(ivq(2 * k / rho)).a
    vals = []
    for x in (rA, rF, rN, rJ, rS, rC):
        vals.append(Fr(x) if isinstance(x, Fr) else ivends(x)[0])
    return tuple(vals)


grid = [Fr(120 + i, 100) for i in range(0, 241)]
for N, lam, beta in ((Exact, lam_A, beta_A), (Interval, None, beta_B)):
    if N is Exact:
        b = (1 - lam) * beta
        M = (lam + b) / (lam + 2 * b)
    else:
        u = iv.e - 1
        beta_iv = ivq(beta)
        lam = u * beta_iv / (1 + u * beta_iv)
        b = beta_iv / (1 + u * beta_iv)
        M = (1 + u) / (2 + u)
    th = thresholds(M)
    log(f"\n=== Calibration {N.name}; prior 1/2; thresholds rA, rF, rN, rJ, rS, rC =",
        ", ".join(round_dec(x, 6) for x in th))
    mismatches = 0
    rows = []
    for rule in (("IM", "C1"), ("IM", "CM"), ("I0", "C1"), ("I0", "CM")):
        for r in grid:
            eqs = equilibria(N, r, Fr(1, 2), lam, b, *rule)
            found = {label(e[0], e[1]) for e in eqs}
            pred = predicted(r, th, *rule)
            if found != pred:
                mismatches += 1
                log(f"   MISMATCH {rule} r = {r}: found {sorted(found)} predicted {sorted(pred)}")
            if rule == ("IM", "C1") and r in (Fr(6, 5), Fr(139, 100), Fr(7, 5), Fr(145, 100), Fr(147, 100),
                                               Fr(155, 100), Fr(160, 100), Fr(165, 100), Fr(174, 100),
                                               Fr(175, 100), Fr(19, 10), Fr(197, 100), Fr(2), Fr(212, 100),
                                               Fr(213, 100), Fr(3), Fr(359, 100), Fr(36, 10)):
                rows.append((r, eqs))
            if rule == ("IM", "CM") and r in (Fr(155, 100), Fr(160, 100), Fr(165, 100), Fr(19, 10)):
                rows.append((r, [e for e in eqs if "threshold" in e[0]]))
    log(f"   grid points: {len(grid)} x 4 tie-rule pairs; mismatches with the table: {mismatches}")
    log("   Sample equilibria (label, entry, high-class ownership, zero order):")
    for r, eqs in rows:
        for hl, ll, Ent, own, z in eqs:
            log(f"     r = {round_dec(r, 2)}: {label(hl, ll):28s} entry {N.fmt(Ent) if Ent is not None else 'tie':>9s}"
                f"  ownership {N.fmt(own) if own is not None else 'tie':>9s}  {z}")
    for rule in (("I0", "C1"), ("I0", "CM")):
        empty = [r for r in grid if not equilibria(N, r, Fr(1, 2), lam, b, *rule)]
        if empty:
            log(f"   Under {rule[0]} and {rule[1]} the equilibrium set is empty at {len(empty)} grid points,"
                f" from {round_dec(min(empty), 2)} to {round_dec(max(empty), 2)}")


# ------------------------------------------------------------------ coexistence at other priors
def predicted_coexist(N, r, pi, Mpi, inv_rule, ch_rule):
    """Coexistence from Proposition 5 (C1) and the remark on the other tie rules."""
    t, D = tau(r), Delta(r)
    n_ok = rho * D * max(pi, 1 - pi) <= k
    strict_full = cmp(N, N.c(D) * (1 - Mpi), N.c(k)) == 1
    if pi < t:
        ok = n_ok and J(r) >= k and cmp(N, N.c(t), Mpi) <= 0
        return ok and (strict_full if inv_rule == "I0" else True)
    if pi == t and ch_rule == "CM":
        ok = n_ok and J(r) > k
        return ok and (strict_full if inv_rule == "I0" else True)
    return False


def coexist_found(eqs):
    labs = {label(e[0], e[1]) for e in eqs}
    return "H0/L0" in labs and len(labs) > 1


fine = [Fr(240 + i, 200) for i in range(0, 481)]  # step 1/200 on [1.2, 3.6]
priors = (Fr(3, 10), Fr(39, 100), Fr(40, 100), Fr(45, 100), Fr(1, 2), Fr(55, 100), Fr(62, 100),
          Fr(16, 25), Fr(645, 1000), Fr(69, 107), Fr(649, 1000), Fr(651, 1000), Fr(66, 100))
log("\n=== Coexistence at other priors: strengths on the grid of step 1/200 on [1.2, 3.6]")
log("   The prior 69/107 equals tau(3/2), a grid strength in (r_A, r_star); 16/25 equals tau(11/8) < tau(r_A).")
log("   At a grid point where the prior equals the threshold, C1 and CM differ.")
for N, lam, beta in ((Exact, lam_A, beta_A), (Interval, None, beta_B)):
    if N is Exact:
        b = (1 - lam) * beta
        u_ = lam / b
    else:
        u_ = iv.e - 1
        beta_iv = ivq(beta)
        lam = u_ * beta_iv / (1 + u_ * beta_iv)
        b = beta_iv / (1 + u_ * beta_iv)
    log(f"\n   Calibration {N.name}")
    total, mism = 0, 0
    for rule in (("IM", "C1"), ("IM", "CM"), ("I0", "C1"), ("I0", "CM")):
        for pi in priors:
            Mpi = N.c(pi) * (1 + u_) / (N.c(pi) * (1 + u_) + 1 - N.c(pi))
            co, bad = [], []
            for r in fine:
                eqs = equilibria(N, r, pi, lam, b, *rule)
                f = coexist_found(eqs)
                pr = predicted_coexist(N, r, pi, Mpi, *rule)
                total += 1
                if f:
                    co.append(r)
                if f != pr:
                    bad.append(r)
            mism += len(bad)
            rng = (f"{round_dec(min(co), 3)} to {round_dec(max(co), 3)} ({len(co)} points)" if co
                   else "none")
            log(f"   {rule[0]}/{rule[1]} prior {round_dec(pi, 6)}: coexistence on grid points {rng};"
                f" differences from the predicted set: {len(bad)}"
                + (f" at {[str(x) for x in bad]}" if bad else ""))
    log(f"   cases: {total}; differences from the predicted sets: {mism}")

log(f"\nUndetermined interval comparisons: {len(UNDET)}")
for w in UNDET:
    log("   ", w)
log.close()
