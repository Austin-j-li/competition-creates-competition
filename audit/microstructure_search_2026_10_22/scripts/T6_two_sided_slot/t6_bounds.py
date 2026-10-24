"""Exact numbers behind the analytical results of T6 (print only).

Sections:
  A. Auction objects at the benchmark strengths, checked against piecewise integration.
  B. Prop. 2(iii) forces M <= tau(18/5); the implied caps on lam (every beta) and the failure of lam = 7/10.
  C. For theta <= 1/3 and M <= tau(18/5): the lower bounds that force full two-sided trade at r = 3 and 18/5.
  D. The full-trade posteriors and entry at r = 3 as functions of (lam, beta, theta).
  E. The two branch bounds at r = 31/20 (theta <= 1/3): no buyer-mixing branch with pure entry.
  F. Can the zero flow recruit (the only way a sale can gain from recruitment)? Its largest posterior.
Run from the repository root:
  .venv/bin/python audit/microstructure_search_2026_10_22/scripts/T6_two_sided_slot/t6_bounds.py
"""
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from t6_core import bench, auction, auction_by_integration, r_of_spread, fmt  # noqa: E402

RHO, K = F(1, 4), F(1, 50)
STR = (F(6, 5), F(31, 20), F(8, 5), F(33, 20), F(3), F(18, 5))


def A_at(r):
    return auction(bench(r=r))


def main():
    print('=' * 100)
    print('A. Auction objects (paper eq. (4)); difference to piecewise integration must be zero')
    for r in STR:
        a = A_at(r)
        b = auction_by_integration(bench(r=r))
        diff = max(abs(a[key] - b[key]) for key in ('t0', 'tH', 'tL', 'gH', 'gL', 'D'))
        print(f"r = {fmt(r)}: Delta = {fmt(a['D'])}, k/Delta = {fmt(K / a['D'])}, tau = {fmt(a['tau'])}, "
              f"1 - tau = {fmt(1 - a['tau'])}, max |diff| = {diff}")
    rN = r_of_spread(2 * K / RHO)
    print(f"r_N (rho Delta / 2 = k) in {rN}")

    print('=' * 100)
    print('B. Prop. 2(iii) and the presence cap')
    t3, t36 = A_at(F(3))['tau'], A_at(F(18, 5))['tau']
    D36 = A_at(F(18, 5))['D']
    print(f"tau(3) = {fmt(t3)}, tau(18/5) = {fmt(t36)}")
    print(f"rho Delta(18/5) (1 - tau(18/5)) - k = {fmt(RHO * D36 * (1 - t36) - K)}  (> 0: full purchase at 18/5)")
    u_lo, u_hi = t3 / (1 - t3) - 1, t36 / (1 - t36) - 1
    print(f"M = (c + lam)/(2c + lam) = (1 + u)/(2 + u), u = lam / c;  M in [tau(3), tau(18/5)) <=> u in [{fmt(u_lo)}, {fmt(u_hi)})")
    print(f"lam < u_hi beta / (1 + u_hi beta); at beta = 1/2: lam < {fmt(u_hi / 2 / (1 + u_hi / 2))}")
    print(f"lam = 7/10 needs beta > (7/10) / (u_hi (3/10)) = {fmt(F(7, 10) / (u_hi * F(3, 10)))} > 1/2: impossible")
    for lam in (F(7, 10), F(3, 5), F(1, 2), F(23, 50)):
        bmin = lam / (u_hi * (1 - lam))
        print(f"   lam = {fmt(lam)}: (iii) needs beta > {fmt(bmin)}")

    print('=' * 100)
    print('C. theta <= 1/3, M <= tau(18/5): lower bound rho (1 - theta)(1 - M) on G/Delta for every profile')
    for r in (F(3), F(18, 5)):
        a = A_at(r)
        lb = RHO * F(2, 3) * (1 - t36)
        print(f"r = {fmt(r)}: rho (2/3)(1 - tau(18/5)) = {fmt(lb)} vs k/Delta = {fmt(K / a['D'])}; margin {fmt(lb - K / a['D'])}")

    print('=' * 100)
    print('D. Full two-sided trade: posteriors and entry at r = 3 (exact, selected points)')
    for lam, beta, theta in ((F(5, 11), F(1, 2), F(71, 200)), (F(9, 20), F(49, 100), F(3, 10)),
                             (F(2, 5), F(9, 20), F(1, 10)), (F(1, 3), F(3, 10), F(1, 10))):
        c = (1 - lam) * beta
        ph = 1 - 2 * theta
        w, x = 2 * c + lam, 1 - 2 * c - lam
        M = (c + lam) / (2 * c + lam)
        mu1 = ((c + lam) * ph + x * theta) / ((2 * c + lam) * ph + 2 * x * theta)
        p2, p1 = theta * w / 2, ph * w / 2 + theta * x
        E3 = RHO + (1 - RHO) * ((p2 if M >= t3 else 0) + (p1 if mu1 >= t3 else 0))
        print(f"lam={fmt(lam)}, beta={fmt(beta)}, theta={fmt(theta)}: M = {fmt(M)}, mu_1 = {fmt(mu1)}, "
              f"Pr(X=2) = {fmt(p2)}, Pr(X=1) = {fmt(p1)}, E(3) = {fmt(E3)}")
    print('At beta = 1/2 (x = 0): mu_1 = M and E(3) = 1/4 + (3/8)(1 - theta); E(3) = 0.522757 at theta = '
          f'{fmt(1 - (F(522757, 1000000) - RHO) * 8 / 3)}')

    print('=' * 100)
    print('E. Buyer-mixing branches with no sale at r = 31/20 (theta <= 1/3)')
    a = A_at(F(31, 20))
    kD = K / a['D']
    lb12 = (1 - F(1, 3)) * (1 - t36) + RHO * F(1, 3) / 2
    ub2 = (RHO + 1 - a['tau']) / 3
    print(f"k/Delta(31/20) = {fmt(kD)}")
    print(f"recruiting set {{1,2}}: payoff > (1 - theta)(1 - tau(18/5)) + rho theta / 2 >= {fmt(lb12)}  (> k/Delta)")
    print(f"recruiting set {{2}}:   payoff < rho (1 - theta)/2 + theta (1 - tau) <= (rho + 1 - tau)/3 = {fmt(ub2)}  (< k/Delta)")
    print(f"no recruitment:        payoff < rho/2 = {fmt(RHO / 2)}  (< k/Delta)")
    # strength below which a {1,2} branch could exist
    d_hat = K / lb12
    print(f"a {{1,2}} buyer-mixing branch needs k/Delta(r) > {fmt(lb12)}, i.e. r < {r_of_spread(d_hat)}")
    for r in (F(8, 5), F(33, 20)):
        aa = A_at(r)
        print(f"   r = {fmt(r)}: k/Delta = {fmt(K / aa['D'])}, (rho + 1 - tau)/3 = {fmt((RHO + 1 - aa['tau']) / 3)}")

    print('=' * 100)
    print('F. The zero flow under a full purchase and no sale: LR_0 = 1 + lam |d| / L0 (theta > 1/3)')
    for r in (F(31, 20), F(33, 20)):
        tt = A_at(r)['tau']
        need = tt / (1 - tt)
        print(f"r = {fmt(r)}: recruitment at x = 0 needs LR_0 >= {fmt(need)}")
    # sup over the strip: beta = 1/2 maximises lam for given u; scan theta and u on rational grids
    for th100 in range(34, 50, 2):
        theta = F(th100, 100)
        ph, dd = 1 - 2 * theta, 3 * theta - 1
        vals = []
        for ui in range(0, 34):
            u = u_lo + (u_hi - u_lo) * F(ui, 33)
            for beta in (F(1, 2), F(2, 5), F(1, 4)):
                lam = u * beta / (1 + u * beta)
                c = (1 - lam) * beta
                L0 = 2 * c * theta + (1 - 2 * c) * ph
                vals.append((1 + lam * dd / L0, float(u), float(beta)))
        m = max(vals)
        print(f"theta = {fmt(theta)}: largest LR_0 on the strip grid = {float(m[0]):.6f} at u = {m[1]:.4f}, beta = {m[2]}")


if __name__ == '__main__':
    main()
