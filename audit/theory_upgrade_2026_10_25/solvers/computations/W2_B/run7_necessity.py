"""Point masses, uniform incumbent, rho = 1/4: does ownership ever rise on the research branch at r > h?
Brute force over cH, k, beta, a, r, including near-free research and k close to Delta*m.
Also: where d ln eH / d ln r crosses 1 on the benchmark branch; tau = 1 strength at the benchmark cost.
"""
import sys
import numpy as np
from math import sqrt, e as EU
sys.path.insert(0, 'audit/theory_upgrade_2026_10_25/solvers/computations/W2_B')
from model import branch, eps_e

for hl in [10.0, 5.0, 3.0]:
    h, ell, p = hl, 1.0, 0.5
    n_branch = n_rise = 0
    max_gap = -9
    for cH in np.linspace(0.3, h / 2, 25):
        for k in [0.01, 0.05, 0.2, 0.5, 1.0, 1.5, 2.0, 3.0]:
            for beta in [0.05, 0.1, 0.2, 0.25, 0.3, 1 / 3, 0.4, 0.45]:
                for a in [1e-6, 1e-4, 1e-2, 0.1, 1.0]:
                    prm = dict(h=h, ell=ell, p=p, cH=cH, rho=0.25, k=k, beta=beta, a=a, cap=0.999)
                    for r in h * np.array([1.0001, 1.01, 1.05, 1.1, 1.2, 1.4, 1.7, 2.0]):
                        b = branch(r, prm)
                        if not b.get('on_branch'):
                            continue
                        n_branch += 1
                        ee, lam, _ = eps_e(b['Delta'], prm)
                        eta = (2 * r - h - ell) / (h + ell)
                        max_gap = max(max_gap, ee - eta)
                        if ee > eta:
                            n_rise += 1
    print(f"h/ell={hl}: rho=1/4 branch points at r>h: {n_branch}, rising: {n_rise}, max(eps_e - eta) = {max_gap:.4f}, "
          f"(h-ell)/(h+ell) = {(h-ell)/(h+ell):.4f}")

# benchmark: d ln eH / d ln r crossing 1
u = EU - 1
beta = 0.294655
bm = dict(h=10, ell=1, p=0.5, cH=6.0, rho=0.25, k=0.02, beta=beta, a=1 / 40, cap=u * beta / (1 + u * beta))
lo, hi = 1.60, 1.65
for _ in range(60):
    mid = (lo + hi) / 2
    b = branch(mid, bm)
    ee, _, _ = eps_e(b['Delta'], bm)
    val = ee * mid * 0.5 * (1 - 1 / mid ** 2) / b['Delta']
    lo, hi = (mid, hi) if val > 1 else (lo, mid)
print("benchmark: strength elasticity of eH equals 1 at r =", lo)
# tau = 1 at cH = 6 for r < h: 10 - r/2 - 1/(8r) = 6
print("benchmark: recruitment possible only for r <", (32 + sqrt(1024 - 16)) / 8, "(tau<1 needs gH > cH)")
