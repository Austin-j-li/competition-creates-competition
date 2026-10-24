"""C4: evaluate the analytical sufficient conditions of the memo (Results 3 to 6). Print-only.

psi1(q) = q / (q + a (1-q))      largest posterior of an event with prior q after one binary signal
psi2(q) = q / (q + a^2 (1-q))    largest posterior after two signals (any buy-only mixtures)
Conditions (memo Section 3):
  NC   no entry cascade:      c_H > psi2(pi_LH) * D_r
  R2HH round-2 HH buys:       (1 - psi2(pi_HH)) * rho * D_r > k            (after d1 = 1, under NC)
  R2LH round-2 LH never buys: a^2 [(1-rho) DT + rho D_r] > rho DT           (after d1 = 1, under NC)
  R1HH round-1 HH buys:       rho^2 (1 - psi1(pi_HH)) * D_r > k             (under NC)
  NC is implied by c_H > B_r(1/2) when psi2(pi_LH) <= 1/2; for kappa = 0 this is b >= 2 / ln 3.
Run from the repository root with .venv/bin/python.
"""
import math

h, l, p, rho, k = 10.0, 1.0, 0.5, 0.25, 0.02


def objs(r):
    tH = r / 2 + p * p / (2 * r)
    gH = h - tH
    gL = (l * l - p * p) / (2 * r)
    DT = (r - l) ** 2 / (2 * r)
    return gH, gL, DT, gH - gL


def psi(q, a, n):
    return q / (q + a ** n * (1 - q))


def main():
    print('b* = 2/ln 3 =', 2 / math.log(3), '(kappa = 0: psi2(1/4) <= 1/2 iff b >= b*)')
    for b in (1.2, 1.5, 2.0, 3.0):
        a = math.exp(-1 / b)
        print(f'\nb = {b}: a = {a:.6f}, a^2 = {a * a:.6f}')
        for kappa in (-0.5, 0.0, 0.5):
            piLH = (1 - kappa) / 4
            piHH = (1 + kappa) / 4
            p2LH, p2HH, p1HH = psi(piLH, a, 2), psi(piHH, a, 2), psi(piHH, a, 1)
            print(f'  kappa = {kappa:+.1f}: pi_LH = {piLH:.3f}, psi2(pi_LH) = {p2LH:.6f}, '
                  f'psi2(pi_HH) = {p2HH:.6f}, psi1(pi_HH) = {p1HH:.6f}')
            for r in (1.2, 2.0, 3.0, 3.6, 4.2):
                gH, gL, DT, D = objs(r)
                ncth = p2LH * D
                Bh = gL + D / 2
                r2hh = (1 - p2HH) * rho * D
                r2lh = a * a * ((1 - rho) * DT + rho * D) - rho * DT
                r1hh = rho * rho * (1 - p1HH) * D
                print(f'    r = {r}: D_r = {D:.6f}; NC threshold psi2*D_r = {ncth:.6f} vs B_r(1/2) = {Bh:.6f} '
                      f'({"implied by c_H > B_r(1/2)" if ncth < Bh else "NOT implied: window (B_r(1/2), psi2*D_r]"}); '
                      f'R2HH bound = {r2hh:.4f} (>k: {r2hh > k}); R2LH slack = {r2lh:.4f} (>0: {r2lh > 0}); '
                      f'R1HH bound = {r1hh:.4f} (>k: {r1hh > k})')


if __name__ == '__main__':
    main()
