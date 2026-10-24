"""X4: complementary private signals (Prop. A.7) with the order slot. Print only.

Declared vector (online appendix C.0): h = 10, ell = 1, p = 0.5, rho = 0.85, c_L = 0, c_H = 7.14, k = 0.015,
r_weak = 1.1, r_strong = 2.3, a = 0.70, d = 0.75, prior 1/2. Grid (C.3): a in {0.68..0.72}, d in {0.73..0.77}.
The trading stage keeps the benchmark slot calibrations A and B.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as Fr
from mpmath import mp, mpf, exp, log, e as E_NUM
from common import EXACT, MP, show, auction, B, bounds, calibration_A, calibration_B
from slot_solver import SlotModel, fmt

RHO, CH, K, R0, R1 = "0.85", "7.14", "0.015", "1.1", "2.3"

# Paper, online appendix table (pinned commit): (a, d) -> (E weak, E strong, O_H weak, O_H strong, condition met)
PAPER_GRID = {
    ("0.68", "0.73"): (0.850000, 0.850000, 0.425000, 0.425000, False),
    ("0.68", "0.74"): (0.850000, 0.850000, 0.425000, 0.425000, False),
    ("0.68", "0.75"): (0.850000, 0.850000, 0.425000, 0.425000, False),
    ("0.68", "0.76"): (0.925000, 0.880132, 0.482000, 0.449575, False),
    ("0.68", "0.77"): (0.925000, 0.882492, 0.482750, 0.451741, False),
    ("0.69", "0.73"): (0.850000, 0.850000, 0.425000, 0.425000, False),
    ("0.69", "0.74"): (0.850000, 0.850000, 0.425000, 0.425000, False),
    ("0.69", "0.75"): (0.850000, 0.878570, 0.425000, 0.448157, True),
    ("0.69", "0.76"): (0.925000, 0.880909, 0.482000, 0.450290, False),
    ("0.69", "0.77"): (0.925000, 0.883109, 0.482750, 0.452331, False),
    ("0.70", "0.73"): (0.850000, 0.850000, 0.425000, 0.425000, False),
    ("0.70", "0.74"): (0.850000, 0.850000, 0.425000, 0.425000, False),
    ("0.70", "0.75"): (0.850000, 0.879438, 0.425000, 0.448942, True),
    ("0.70", "0.76"): (0.925000, 0.881610, 0.482000, 0.450945, False),
    ("0.70", "0.77"): (0.925000, 0.883674, 0.482750, 0.452879, False),
    ("0.71", "0.73"): (0.850000, 0.850000, 0.425000, 0.425000, False),
    ("0.71", "0.74"): (0.850000, 0.878066, 0.425000, 0.447687, True),
    ("0.71", "0.75"): (0.850000, 0.880215, 0.425000, 0.449658, True),
    ("0.71", "0.76"): (0.925000, 0.882247, 0.482000, 0.451551, False),
    ("0.71", "0.77"): (0.925000, 0.884195, 0.482750, 0.453392, False),
    ("0.72", "0.73"): (0.850000, 0.850000, 0.425000, 0.425000, False),
    ("0.72", "0.74"): (0.850000, 0.878915, 0.425000, 0.448457, True),
    ("0.72", "0.75"): (0.850000, 0.880919, 0.425000, 0.450315, True),
    ("0.72", "0.76"): (0.925000, 0.882833, 0.482000, 0.452115, False),
    ("0.72", "0.77"): (0.925000, 0.884680, 0.482750, 0.453877, False),
}


def phi(y, mu, d):
    if y > 0:
        return d * mu / (d * mu + (1 - d) * (1 - mu))
    return (1 - d) * mu / ((1 - d) * mu + d * (1 - mu))


def margins(F, S, a, d, laplace_m=None):
    a, d, rho, cH, k = F(a), F(d), F(RHO), F(CH), F(K)
    A0, A1 = auction(F, F(R0)), auction(F, F(R1))
    m, M = bounds(S["u"], F(Fr(1, 2)))
    mu_lo, mu_hi = (1 - a) + (2 * a - 1) * m, (1 - a) + (2 * a - 1) * M
    out = dict(
        private_only=cH - B(A0, d),
        joint=B(A1, phi(1, mu_hi, d)) - cH,
        weak_order=k - (2 * a - 1) * (A0["D"] + (1 - rho) * (2 * d - 1) * A0["wH"]),
        strong_order_slot=(2 * a - 1) * rho * min(m, 1 - M) * A1["D"] - k,
        low_cost=B(A1, phi(-1, mu_lo, d)),
    )
    if laplace_m is not None:
        out["strong_order_laplace"] = (1 - F(1) / 2) * laplace_m * (2 * a - 1) * rho * A1["D"] - k
    return out


def laplace_signal_outcome(a, d, r, orders_full=True, bscale=2):
    """Paper OA.39-OA.41 (Laplace noise, full orders by T at strength r; zero orders give the prior)."""
    a, d, rho, cH = MP(a), MP(d), MP(RHO), MP(CH)
    A = auction(MP, MP(r))
    tau = (cH - A["gL"]) / (A["gH"] - A["gL"])
    bscale = mpf(bscale)
    m = 1 / (1 + exp(2 / bscale))
    M = 1 - m
    S = lambda z: exp(-z / bscale) / 2 if z >= 0 else 1 - exp(z / bscale) / 2
    eHs, eLs = [], []
    for y in (1, -1):
        if 0 < tau < 1:
            mu_req = tau * (1 - d) / (d * (1 - tau) + tau * (1 - d)) if y > 0 else tau * d / ((1 - d) * (1 - tau) + tau * d)
        else:
            mu_req = mpf(-1) if tau <= 0 else mpf(2)
        if not orders_full:
            QH = QL = mpf(1) if mpf(1) / 2 >= mu_req else mpf(0)
        else:
            l_req = (mu_req - (1 - a)) / (2 * a - 1)
            if l_req <= m:
                QH = QL = mpf(1)
            elif l_req > M:
                QH = QL = mpf(0)
            else:
                xs = bscale / 2 * log(l_req / (1 - l_req))
                QH = a * S(xs - 1) + (1 - a) * S(xs + 1)
                QL = (1 - a) * S(xs - 1) + a * S(xs + 1)
        eHs.append((d if y > 0 else 1 - d) * QH)
        eLs.append(((1 - d) if y > 0 else d) * QL)
    eH = rho + (1 - rho) * sum(eHs)
    eL = rho + (1 - rho) * sum(eLs)
    return (eH + eL) / 2, eH / 2


def solve(F, S, a, d, r, verbose=False):
    A = auction(F, F(r))
    mod = SlotModel(F, S, A, Fr(1, 2) if F is EXACT else "1/2", a, d, RHO, CH, K)
    eqs, cm_s, cm_t = mod.equilibria()
    res = []
    for s, t, ks, kt in eqs:
        out = mod.outcome(s, t)
        ver = mod.verify(s, t)
        res.append((s, t, ks, kt, out, ver))
    return mod, res, cm_s, cm_t


def report_example(label, F, S):
    print("=" * 100)
    print(f"Declared example a = 0.70, d = 0.75, calibration {label}")
    m, M = bounds(S["u"], F(Fr(1, 2)))
    lap_m = 1 / (1 + E_NUM)
    mg = margins(F, S, "0.70", "0.75", laplace_m=(MP(lap_m) if F is MP else None))
    for kk, v in mg.items():
        print(f"   margin {kk}: {show(v)}")
    a, d = F("0.70"), F("0.75")
    mu_hi = (1 - a) + (2 * a - 1) * M
    print(f"   public bounds: mu_- = {show((1 - a) + (2 * a - 1) * m)}, mu_+ = {show(mu_hi)}; "
          f"phi_+(mu_+) = {show(phi(1, mu_hi, d))}, phi_-(mu_+) = {show(phi(-1, mu_hi, d))}")
    for r in (R0, R1):
        mod, res, cm_s, cm_t = solve(F, S, "0.70", "0.75", r)
        _, tau = mod.thresholds_mu()
        print(f"   r = {r}: tau = {show(tau)}; number of C1/IM equilibria = {len(res)}; CM-only buy mixtures {len(cm_s)}, sell {len(cm_t)}")
        for s, t, ks, kt, out, ver in res:
            print(f"      s = {show(s, 8)} ({ks}), t = {show(t, 8)} ({kt}): E = {show(out['E'])}, e_H = {show(out['eH'])}, "
                  f"e_L = {show(out['eL'])}, O_H = {show(out['OH'])}, R_T = {show(out['RT'], 10)}")
            for x, row in out["rows"].items():
                print(f"         Q = {x:+d}: mu = {show(row['mu'], 10)}, (I_+, I_-) = {row['I']}, P = {show(row['P'], 10)}")
            g = {T: fmt(ver["gains"][T][0], 4) for T in (1, -1)}
            U = {T: {q: fmt(u, 8) for q, u in ver["gains"][T][1].items()} for T in (1, -1)}
            print(f"         joint-law check: max|mu err| = {fmt(ver['err_mu'], 3)}, max|P err| = {fmt(ver['err_P'], 3)}, "
                  f"inversion err = {fmt(ver['err_inv'], 3)}, joint-posterior err = {fmt(ver['err_phi'], 3)}, distinct prices = {ver['prices_ok']}")
            print(f"         investor payoffs U(q) by signal: T=+ {U[1]}, T=- {U[-1]}; best-response gain T=+ {g[1]}, T=- {g[-1]}")
        for x, desc in cm_s:
            print(f"      CM-only buy rate s = {show(x, 8)}: {desc}")
        for x, desc in cm_t:
            print(f"      CM-only sell rate t = {show(x, 8)}: {desc}")


def grid(label, F, S):
    print("=" * 100)
    print(f"Accuracy grid, calibration {label}. Columns: a, d | slot: #eq weak, #eq strong, E weak, E strong, dE (pp), "
          f"O_H weak, O_H strong, min slot margin, met | paper: E strong, met | Laplace recomputed E strong")
    met_rows = []
    for (a_, d_), paper in PAPER_GRID.items():
        _, rw, cmw, cmw2 = solve(F, S, a_, d_, R0)
        _, rs, cms, cms2 = solve(F, S, a_, d_, R1)
        mg = margins(F, S, a_, d_)
        mmin = min(mg["private_only"], mg["joint"], mg["weak_order"], mg["strong_order_slot"], mg["low_cost"])
        met = mmin > 0
        if met:
            met_rows.append((a_, d_))
        Ew = rw[0][4]["E"] if len(rw) == 1 else None
        Es = rs[0][4]["E"] if len(rs) == 1 else None
        Ow = rw[0][4]["OH"] if len(rw) == 1 else None
        Os = rs[0][4]["OH"] if len(rs) == 1 else None
        orders_s = [(fmt(s, 6), fmt(t, 6)) for s, t, *_ in rs]
        orders_w = [(fmt(s, 6), fmt(t, 6)) for s, t, *_ in rw]
        maxgain = max(max(v[5]["gains"][1][0], v[5]["gains"][-1][0]) for v in rw + rs)
        E_lap, O_lap = laplace_signal_outcome(a_, d_, R1)
        dE = (Es - Ew) * 100 if (Es is not None and Ew is not None) else None
        print(f"   {a_} {d_} | {len(rw)} {len(rs)} | {fmt(Ew, 6) if Ew is not None else 'multi'} "
              f"{fmt(Es, 6) if Es is not None else 'multi'} {fmt(dE, 4) if dE is not None else '-'} "
              f"{fmt(Ow, 6) if Ow is not None else '-'} {fmt(Os, 6) if Os is not None else '-'} "
              f"{fmt(mmin, 8)} {'met' if met else 'not met'} | {paper[1]:.6f} {'met' if paper[4] else 'not met'} | {fmt(E_lap, 6)}"
              f"   [orders weak {orders_w}, strong {orders_s}; CM-only extra: {len(cmw) + len(cmw2) + len(cms) + len(cms2)}; max BR gain {fmt(maxgain, 3)}]")
    paper_met = [kk for kk, v in PAPER_GRID.items() if v[4]]
    print(f"   slot 'met' rows: {met_rows}")
    print(f"   paper 'met' rows: {paper_met}")
    print(f"   same set: {sorted(met_rows) == sorted(paper_met)}")


def main():
    SA = calibration_A()
    SB, _ = calibration_B()
    print("Laplace cross-check of the declared example (paper: E 0.850000 -> 0.879438; O_H 0.425000 -> 0.448942):")
    Ew, Ow = laplace_signal_outcome("0.70", "0.75", R0, orders_full=False)
    Es, Os = laplace_signal_outcome("0.70", "0.75", R1)
    print(f"   weak (zero orders): E = {mp.nstr(Ew, 10)}, O_H = {mp.nstr(Ow, 10)}; strong (full orders): E = {mp.nstr(Es, 10)}, O_H = {mp.nstr(Os, 10)}")
    report_example("A (exact)", EXACT, SA)
    report_example("B (40 digits)", MP, SB)
    grid("A (exact)", EXACT, SA)
    grid("B (40 digits)", MP, SB)


if __name__ == "__main__":
    main()
