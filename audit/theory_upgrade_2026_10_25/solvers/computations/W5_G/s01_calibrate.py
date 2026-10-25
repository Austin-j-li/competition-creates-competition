"""Reproduce registry values at prior 1/2 to check the implementation."""
import sys
sys.path.insert(0, "audit/theory_upgrade_2026_10_25/solvers/computations/W5_G")
from mpmath import mp, mpf, nstr, findroot
from model import *

s = slot()
u, lam, b, b0 = s["u"], s["lam"], s["b"], s["b0"]
half = mpf(1) / 2
M, m = Mtop(half, u), mbot(half, u)
print("u", nstr(u, 8), " registry u_B 1.718282")
print("lambda", nstr(lam, 8), " registry 0.336122")
print("b", nstr(b, 8), " registry 0.195615")
print("b0", nstr(b0, 8), " registry 0.272648")
print("M(1/2)", nstr(M, 8), " registry 0.731059;  m(1/2)", nstr(m, 8), " registry 0.268941")
print("M-5/8", nstr(M - mpf(5) / 8, 8), " registry 0.106059")
DS = k / (rho * m)
rS = fr(DS)
print("D_S", nstr(DS, 8), " registry 0.297463;  r_S", nstr(rS, 9), " registry 2.124148")
# r_C closed form
rC = (M * h - cH + mp.sqrt((M * h - cH) ** 2 + M * ((1 - M) * ell**2 - p**2))) / M
print("r_C", nstr(rC, 9), " registry 3.592659;  tau(r_C)-M", nstr(auction(rC)["tau"] - M, 5))
print("r_C - r_S", nstr(rC - rS, 8), " registry 1.468510")
theta = u / (2 + u)
r1, r2 = mpf(3), mpf(18) / 5
for r in (r1, r2):
    F = full_orders(half, r)
    cls = rho * F["a"]["D"] * (F["M"] - F["m"])
    ent = F["S"] - cls
    print(f"r={nstr(r,4)}: class comp {nstr(cls,8)}  entry comp {nstr(ent,8)}  S {nstr(F['S'],8)}  "
          f"share {nstr(ent/F['S'],5)}  tau {nstr(F['a']['tau'],8)}")
    print("   Pbar", nstr(F["Pbar"], 8), " P(0)", nstr(F["P"][0], 8), " P(0)-Pbar", nstr(F["P"][0] - F["Pbar"], 8),
          " T", nstr(F["T"], 8))
print("registry: ba_class_r1 0.077020 ba_entry_r1 0.709279 ba_r1 0.786299 ba_share 90.2% ba_r2 0.108469")
print("registry: pbar_r1 0.872531 p_neutral_r1 0.614583 pdrop_neutral_r1 -0.257948")
bbar = b + lam / 2
print("cov_entry_r1 = (1-rho) bbar =", nstr((1 - rho) * bbar, 8), " registry 0.272757")
print("v", nstr(2 * b + lam, 8), " registry vol_full_B 0.727352")
# spread jump at r_C
FL = full_orders(half, rC)
print("S at r_C (C1, left limit)", nstr(FL["S"], 8), " registry 0.969913")
print("S right of r_C", nstr(FL["S"] - (1 - rho) * A(rC, M), 8), " registry 0.108078;  jump",
      nstr((1 - rho) * A(rC, M), 8), " registry 0.861835")
# announcement means at r1, r2 (full orders)
for r in (r1, r2):
    F = full_orders(half, r)
    PA = sum(F["prob"][x] * F["ent"][x] for x in (-1, 0, 1))
    mean = sum(F["prob"][x] * F["ent"][x] / PA * (1 - F["ent"][x]) * A(r, F["post"][x]) for x in (-1, 0, 1))
    print(f"prep-report mean at r={nstr(r,3)}: {nstr(mean,8)}")
print("registry: evprep_mean_r1 0.160592 evprep_mean_r2 0.701042")
# informed share bound at r1
print("theta_bar(r1)=1-2k/(rho D)", nstr(1 - 2 * k / (rho * auction(r1)["D"]), 8), " registry 0.760000")
