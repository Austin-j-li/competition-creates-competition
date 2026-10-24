"""Working ranges of the knobs and branch endpoints for the second-knob candidate.

Prints (computer-assisted at each listed grid point; exact rational brackets for endpoints):
  A. lam on a 1/100 grid at theta = 1/10: (ii) unique informative equilibrium at r1 = 3;
     (P3) no trade plus a strictly rising pure-entry partial-buy/BNS branch at 1.55, 1.60, 1.65;
  B. theta on a 1/100 grid at lam = 7/10: the same two tests;
  C. endpoints of the partial-buy branch, the BNS segment and no trade at (theta, lam) = (1/10, 7/10);
  D. trading costs in the access-to-prices comparison.
Run from the repository root (about 2 minutes; use the slot wrapper):
  bash audit/microstructure_search_2026_10_22/scripts/_slots/run_slot.sh .venv/bin/python \
      audit/microstructure_search_2026_10_22/scripts/T1_egj_two_sided/t1_refine.py
"""
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from t1_core import bench, auction, Iv, r_of_spread, fmt
from t1_solver import enumerate_equilibria

R3 = (F(31, 20), F(8, 5), F(33, 20))


def val(v):
    return v.mid() if isinstance(v, Iv) else v


def tests(th, lam):
    """Returns (ii_ok, label at r1, E at r1, P3_ok, E triple)."""
    eqs, und, M = enumerate_equilibria(bench(r=F(3), theta=th, lam=lam))
    ii = len(eqs) == 1 and eqs[0]['label'] != 'NT' and val(eqs[0]['out']['E']) > F(1, 4)
    lab = eqs[0]['label'] if len(eqs) == 1 else f'{len(eqs)} equilibria'
    E1 = float(val(eqs[0]['out']['E'])) if len(eqs) == 1 else float('nan')
    branch = []
    co = True
    for r in R3:
        e, u, m = enumerate_equilibria(bench(r=r, theta=th, lam=lam))
        co &= any(q['label'] == 'NT' for q in e) and any(q['label'] != 'NT' for q in e)
        branch.append([Iv.of(q['out']['E']) for q in e
                       if q['label'] in ('partial buy, no sell', 'BNS') and not q['chall_mix']])
    up = co and all(branch) and any(x.hi < y.lo and y.hi < z.lo
                                    for x in branch[0] for y in branch[1] for z in branch[2])
    trip = None
    if up:
        trip = [max(float(x.mid()) for x in b) for b in branch]
    return ii, lab, E1, up, trip


def K(th, a, rho):
    ph = 1 - 2 * th
    d = ph - th
    return rho * th * ph / (2 * ph - a * d) + th * ph / (2 * th + a * d)


def J(th, a, rho):
    ph = 1 - 2 * th
    d = ph - th
    return rho * (ph * (1 - a) / (2 - a) + th * (ph - a * d) / (2 * ph - a * d))


def main():
    print('A. lam grid at theta = 1/10 (rules M, X, IC)')
    rng_ii, rng_p3 = [], []
    for i in range(5, 101):
        lam = F(i, 100)
        ii, lab, E1, up, trip = tests(F(1, 10), lam)
        if ii:
            rng_ii.append(lam)
        if up:
            rng_p3.append(lam)
        if True:
            print(f"  lam={float(lam):.2f}: r1 -> {lab} (E={E1:.6f}), (ii) {ii}; Prop.3 upward {up}"
                  + (f" E = {trip[0]:.6f} < {trip[1]:.6f} < {trip[2]:.6f}" if trip else ''))
    both = [l for l in rng_ii if l in rng_p3]
    print(f"  (ii) holds for lam in {[float(x) for x in (min(rng_ii), max(rng_ii))] if rng_ii else None} (grid, {len(rng_ii)} points)")
    print(f"  Prop. 3 upward holds for lam in {[float(x) for x in (min(rng_p3), max(rng_p3))] if rng_p3 else None} (grid, {len(rng_p3)} points)")
    print(f"  both hold for lam in {[float(x) for x in (min(both), max(both))] if both else None} ({len(both)} grid points; contiguous: "
          f"{len(both) == (int(max(both) * 100) - int(min(both) * 100) + 1) if both else None})")

    print('\nB. theta grid at lam = 7/10 (rules M, X, IC)')
    rng_ii, rng_p3 = [], []
    for i in range(1, 34):
        th = F(i, 100)
        ii, lab, E1, up, trip = tests(th, F(7, 10))
        if ii:
            rng_ii.append(th)
        if up:
            rng_p3.append(th)
        print(f"  theta={float(th):.2f}: r1 -> {lab} (E={E1:.6f}), (ii) {ii}; Prop.3 upward {up}"
              + (f" E = {trip[0]:.6f} < {trip[1]:.6f} < {trip[2]:.6f}" if trip else ''))
    both = [t for t in rng_ii if t in rng_p3]
    print(f"  both hold for theta in {[float(x) for x in (min(both), max(both))] if both else None} ({len(both)} grid points)")

    print('\nC. Branch endpoints at theta = 1/10, lam = 7/10 (exact rational brackets)')
    th, lam = F(1, 10), F(7, 10)
    P = bench(theta=th, lam=lam)
    rho, k = P['rho'], P['k']
    ph = 1 - 2 * th
    d = ph - th

    def a_tau(r):
        tau = auction(bench(r=r))['tau']
        return th * (2 * tau - 1) / (d * (1 - tau))

    def g(r):
        # K(a_tau(r)) - k/Delta(r): the branch starts where this changes sign
        A = auction(bench(r=r))
        return K(th, a_tau(r), rho) - k / A['D']
    lo, hi = F(13, 10), F(16, 10)
    print(f"  sign of K(a_tau(r)) - k/Delta(r): at {float(lo)}: {g(lo) > 0}, at {float(hi)}: {g(hi) > 0}")
    for _ in range(70):
        m = (lo + hi) / 2
        if (g(m) > 0) == (g(lo) > 0):
            lo = m
        else:
            hi = m
    print(f"  lower end of the pure partial-buy branch (x=1 posterior reaches tau): r in [{float(lo):.12f}, {float(hi):.12f}]")
    Klam = K(th, lam, rho)
    rhi = r_of_spread(k / Klam)
    print(f"  upper end (buy rate reaches lam, K(lam) = {fmt(Klam)}): r = frak r(k/K(lam)) in [{float(rhi.lo):.12f}, {float(rhi.hi):.12f}]")
    E_end = rho + (1 - rho) * (th + lam * ph / 2)
    print(f"  entry at the upper end (= BNS entry) = rho + (1-rho)(theta + lam phi/2) = {fmt(E_end)}")
    # BNS segment: x=1 posterior under BNS and L's no-sale condition J(lam) <= k/Delta
    mu1 = (th + lam * d) / (2 * th + lam * d)
    tau_r = lambda r: auction(bench(r=r))['tau']
    lo, hi = F(3, 2), F(9, 2)
    for _ in range(70):
        m = (lo + hi) / 2
        if mu1 >= tau_r(m):
            lo = m
        else:
            hi = m
    print(f"  BNS keeps recruiting at x=1 (posterior {fmt(mu1)}) for r up to [{float(lo):.10f}, {float(hi):.10f}]")
    Jl = J(th, lam, rho)
    rJ = r_of_spread(k / Jl)
    print(f"  under BNS class L stays out while k/Delta >= J(lam) = {fmt(Jl)}, i.e. r <= {float(rJ.hi):.10f}")
    rIC = r_of_spread(2 * k / (rho * (1 - th)))
    print(f"  no trade exists (IC) for r <= {float(rIC.hi):.10f}; (passive) for r <= {float(r_of_spread(2 * k / rho).hi):.10f}")
    # monotone entry on the branch: K decreasing in a (analytical); print K' sign check on a grid
    signs = all(K(th, F(i, 200), rho) > K(th, F(i + 1, 200), rho) for i in range(0, 200))
    print(f"  K strictly decreasing on a = 0, 1/200, ..., 1: {signs}")

    print('\nD. Trading costs at r1 = 3 (theta = 1/10, lam = 7/10): k (pi a + (1 - pi) b)')
    P = bench(r=F(3), theta=th, lam=lam)
    fb, _, _ = enumerate_equilibria(P)
    hd, _, _ = enumerate_equilibria(P, hidden=True)
    for name, eqs in (('feedback', fb), ('hidden', hd)):
        for q in eqs:
            tc = P['k'] * (P['pi'] * Iv.of(q['a']) + (1 - P['pi']) * Iv.of(q['b']))
            print(f"  {name}: {q['label']}: trading cost {float(tc.mid()):.9f}, R_T {float(Iv.of(q['out']['RT']).mid()):.9f},"
                  f" W {float(Iv.of(q['out']['W']).mid()):.9f}")


if __name__ == '__main__':
    main()
