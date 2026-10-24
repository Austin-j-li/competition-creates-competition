"""C4: closed forms of the benchmark equilibrium branch (kappa = 0, only HH buys in round 1). Print-only.

On this branch (memo, Result 7):
  round-1 posteriors  mu1(g) = (1, a, a, a)/(1+3a),  mu1(b) = (a, 1, 1, 1)/(a+3)
  P(j2=H | g) = (1+a)/(1+3a),  P(j2=H | b) = (1+a)/(a+3)
  challenger 1's gain  Gamma1(g) = (1-rho) gL + D_r (1-rho+a)/(1+3a),  Gamma1(b) = (1-rho) gL + D_r (1+a-rho a)/(a+3)
  after d1 = 0 with full purchases by the j2=H types in round 2, the posterior on j2=H after (S1, S2):
      gg: (1+a)/(1+a+2a^2), gb: (1+a)/(3+a), bg: (1+a)/(1+3a), bb: a(1+a)/(2+a+a^2)
It prints these numbers, the cost thresholds that define the entry windows, and the entry probabilities.
Run from the repository root with .venv/bin/python.
"""
from mpmath import mp, mpf, exp

mp.dps = 30
h, l, p, rho, k = mpf(10), mpf(1), mpf('0.5'), mpf('0.25'), mpf('0.02')
a = exp(-mpf(1) / 2)


def objs(r):
    tH = r / 2 + p * p / (2 * r)
    gH = h - tH
    gL = (l * l - p * p) / (2 * r)
    DT = (r - l) ** 2 / (2 * r)
    return gL, gH - gL, DT


def main():
    q = {'g': (1 + a) / (1 + 3 * a), 'b': (1 + a) / (a + 3)}
    post2 = {'gg': (1 + a) / (1 + a + 2 * a * a), 'gb': (1 + a) / (3 + a), 'bg': (1 + a) / (1 + 3 * a),
             'bb': a * (1 + a) / (2 + a + a * a)}
    pg = (1 + 3 * a) / (4 * (1 + a))
    print(f'a = {mp.nstr(a, 12)}; P(S1 = g) = (1+3a)/(4(1+a)) = {mp.nstr(pg, 12)}')
    print('round-1 posterior on j2 = H:', {S: mp.nstr(v, 10) for S, v in q.items()})
    print('two-round posterior on j2 = H after d1 = 0 (full purchases by j2=H types in round 2):',
          {S: mp.nstr(v, 10) for S, v in post2.items()})
    print('two-round bound psi2(1/2) = 1/(1+a^2) =', mp.nstr(1 / (1 + a * a), 10),
          '(the gg posterior is below it because round 1 informs j2 only through HH)')
    for r in (mpf('1.2'), mpf(3), mpf('3.6')):
        gL, D, DT = objs(r)
        B = lambda m: gL + D * m
        G1g = (1 - rho) * gL + D * (1 - rho + a) / (1 + 3 * a)
        G1b = (1 - rho) * gL + D * (1 + a - rho * a) / (a + 3)
        print(f'\nr = {r}: D_r = {mp.nstr(D, 10)}, DT = {mp.nstr(DT, 10)}, k - DT = {mp.nstr(k - DT, 6)}')
        print(f'  challenger 1 gain: Gamma1(g) = {mp.nstr(G1g, 10)}, Gamma1(b) = {mp.nstr(G1b, 10)}')
        print(f'  challenger 2 gain after d1=0 at the round-1 posterior: B(q_g) = {mp.nstr(B(q["g"]), 10)}, B(q_b) = {mp.nstr(B(q["b"]), 10)}')
        print('  challenger 2 gain after d1=0 and a round-2 signal: ' +
              ', '.join(f'{S}: {mp.nstr(B(v), 10)}' for S, v in post2.items()))
        print(f'  lone challenger: B(1/2) = {mp.nstr(B(mpf(1) / 2), 10)}, B(M1) = {mp.nstr(B(1 / (1 + a)), 10)}')
    # entry probabilities on the branch for the two cost windows
    pgg_H, pgg_L = 1 / (1 + a), a / (1 + a)
    e_after_g0 = rho + (1 - rho) * (q['g'] * pgg_H + (1 - q['g']) * pgg_L)   # enters after (g, 0, g) only
    E2_r1 = rho * rho + (1 - rho) * (pg * e_after_g0 + (1 - pg) * rho)
    E2_r0 = rho * rho + (1 - rho) * (pg * 1 + (1 - pg) * rho)
    print(f'\nE2 when challenger 2 enters after (g, d1=0) for sure: {mp.nstr(E2_r0, 10)}')
    print(f'E2 when challenger 2 enters after (g, d1=0, g) only: {mp.nstr(E2_r1, 10)}')
    print(f'P(d2=1 | d1=0) in the two cases: {mp.nstr(pg + (1 - pg) * rho, 10)}, {mp.nstr(pg * e_after_g0 + (1 - pg) * rho, 10)}')


if __name__ == '__main__':
    main()
