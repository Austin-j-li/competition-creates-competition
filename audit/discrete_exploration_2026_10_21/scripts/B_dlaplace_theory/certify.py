"""Interval-arithmetic enclosures of the benchmark inequalities in memos/B_dlaplace_theory.md.

Every printed quantity is an interval that contains the exact value. The script prints each margin
and whether its whole interval lies above zero. It prints only; nothing is asserted.

Run from the repository root:
    .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/B_dlaplace_theory/certify.py
"""
from mpmath import iv

iv.dps = 50

H, ELL, P = iv.mpf(10), iv.mpf(1), iv.mpf(1) / 2
RHO, K = iv.mpf(1) / 4, iv.mpf(1) / 50
PI = iv.mpf(1) / 2


def obj(r):
    return dict(t0=P * (1 - P / r), tH=r / 2 + P**2 / (2 * r), tL=ELL - (ELL**2 - P**2) / (2 * r),
                gH=H - r / 2 - P**2 / (2 * r), gL=(ELL**2 - P**2) / (2 * r), D=(r - ELL) ** 2 / (2 * r))


def B(r, mu):
    o = obj(r)
    return o["gL"] + mu * (o["gH"] - o["gL"])


def frak(dd):
    return ELL + dd + iv.sqrt(dd**2 + 2 * ELL * dd)


def line(name, x):
    width = x.delta
    print(f"  {name:62s} {iv.nstr(x.a, 13)[1:-1].split(',')[0]:>20s}  (interval width {iv.nstr(width, 2)[1:-1].split(',')[0]})"
          f"  whole interval above zero: {bool(x > 0)}")


def main():
    for cH_text in ["5", "5.2"]:
        cH = iv.mpf(cH_text)
        a = iv.exp(-iv.mpf(1) / 2)
        g = 1 / (1 + a)
        M1 = g
        Lam = 2 * g * (1 - g)
        r0, r1 = iv.mpf("1.2"), iv.mpf(3)
        r2 = iv.mpf("4.2") if cH_text == "5" else iv.mpf("3.6")
        print(f"=== c_H = {cH_text}, b = 2, pi = 1/2, lam = 1, k = 1/50, rho = 1/4; r2 = {iv.nstr(r2.a, 3)} ===")
        line("(A2) c_H - B_r0(1/2)", cH - B(r0, PI))
        line("(A2) B_r1(M1) - c_H", B(r1, M1) - cH)
        line("(A2') c_H - B_r2(M1)", cH - B(r2, M1))
        line("(A3) k - (1 - pi) D(r0)", K - (1 - PI) * obj(r0)["D"])
        line("(A3) rho Lambda D(r1) - k", RHO * Lam * obj(r1)["D"] - K)
        line("brief bound: rho m1 D(r1) - k", RHO * (1 - g) * obj(r1)["D"] - K)
        # coexistence interval (r_F, r_N] and the ceiling
        KF_hat = g * (1 - g) * (1 + RHO)
        rF, rN = frak(K / KF_hat), frak(K / (RHO * (1 - PI)))
        Mh = M1 * H - cH
        rC = (Mh + iv.sqrt(Mh**2 + M1 * ((1 - M1) * ELL**2 - P**2))) / M1
        print(f"  enclosures: r_F = {iv.nstr(rF, 16)}, r_N = {iv.nstr(rN, 16)}, r_C = {iv.nstr(rC, 16)}")
        line("r_N - r_F (coexistence interval length)", rN - rF)
        line("r_C - r_N (recruitment feasible on the whole interval)", rC - rN)
        line("feedback: K_F/K_0 - 1 = 2 g(1-g)(1+rho)/rho - 1", 2 * g * (1 - g) * (1 + RHO) / RHO - 1)
        for rt in ["1.55", "1.6", "1.65"]:
            r = iv.mpf(rt)
            o = obj(r)
            K0 = RHO * (1 - PI) * o["D"]
            KF = o["D"] * g * (1 - g) * (1 + RHO)
            line(f"r={rt}: k - K_0 (no trade survives)", K - K0)
            line(f"r={rt}: K_F - k (full buying survives)", KF - K)
            line(f"r={rt}: B_r(M1) - c_H (good news recruits)", B(r, M1) - cH)
            line(f"r={rt}: c_H - B_r(1/2) (prior does not recruit)", cH - B(r, PI))
        print()


if __name__ == "__main__":
    main()
