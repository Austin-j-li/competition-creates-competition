"""Print-only numerical illustration for Reading C (challenger chooses).

Benchmark vector from the brief: (h, l, p, rho, cL, cH, b, k)
= (10, 1, 0.5, 0.25, 1, 6, 2, 0.02), with (r0, r1, r2) = (1.2, 3, 3.6).
Incumbent R ~ U[0, r]. Closed forms for g(theta) and t(theta) appear
in the memo. This script only computes values and prints them.
"""

from mpmath import mp, quad

mp.dps = 30

H, ELL, P, RHO, CL, CH, BPAR, KPAR = 10.0, 1.0, 0.5, 0.25, 1.0, 6.0, 2.0, 0.02
RS = (1.2, 3.0, 3.6)


def cdf(u, r):
    if u <= 0:
        return 0.0
    if u >= r:
        return 1.0
    return u / r


def g_closed(theta, r):
    if theta <= P:
        return 0.0
    if theta <= r:
        return (theta**2 - P**2) / (2 * r)
    return theta - r / 2 - P**2 / (2 * r)


def t_closed(theta, r):
    if theta < P:
        return P * (1 - P / r)
    if theta <= r:
        return theta - (theta**2 - P**2) / (2 * r)
    return r / 2 + P**2 / (2 * r)


def g_integral(theta, r):
    if theta <= P:
        return 0.0
    cuts = [P, theta] if theta <= r else [P, r, theta]
    return float(quad(lambda u: min(max(u / r, 0.0), 1.0), cuts))


def t_integral(theta, r):
    if theta < P:
        return P * (1 - P / r)
    cuts = [P, theta] if theta <= r else [P, r, theta]
    return P + float(quad(lambda u: 1 - min(max(u / r, 0.0), 1.0), cuts))


def mean_plan(points_weights, func, r):
    return sum(w * func(th, r) for th, w in points_weights)


print("Benchmark (h, l, p, rho, cL, cH, b, k) = "
      f"({H:g}, {ELL:g}, {P:g}, {RHO:g}, {CL:g}, {CH:g}, {BPAR:g}, {KPAR:g})")
print(f"Incumbent strengths (r0, r1, r2) = {RS}")
print()

print("1. Functions g and t at r = 3 (closed form, integral form, sum)")
print(f"{'theta':>6} {'g closed':>10} {'g integr':>10} {'t closed':>10} "
      f"{'t integr':>10} {'g+t':>10}")
for th in (0.0, 0.4, 0.5, 1.0, 2.0, 3.0, 5.5, 10.0):
    print(f"{th:6.2f} {g_closed(th, 3.0):10.6f} {g_integral(th, 3.0):10.6f} "
          f"{t_closed(th, 3.0):10.6f} {t_integral(th, 3.0):10.6f} "
          f"{g_closed(th, 3.0) + t_closed(th, 3.0):10.6f}")
print(f"No-entry proceeds t0 at r = 3: {P * (1 - P / 3.0):.6f}")
print(f"Jump size p*F(p) at r = 3: {P * cdf(P, 3.0):.6f}")
print()

print("2. Second differences on an equal grid at r = 3, step 0.5, theta in [0.5, 3]")
print("   g second differences should print positive. t should print negative.")
grid = [0.5 + 0.5 * i for i in range(6)]
for name, func in (("g", g_closed), ("t", t_closed)):
    vals = [func(th, 3.0) for th in grid]
    second = [vals[i + 1] - 2 * vals[i] + vals[i - 1] for i in range(1, len(vals) - 1)]
    print(f"   {name}: " + ", ".join(f"{v:+.6f}" for v in second))
print()

print("3. Menu A (benchmark straddle). Safe: value 5.5 for sure.")
print("   Risky: values 1 and 10 with probability 1/2 each. Both means: 5.5.")
safe_a = [(5.5, 1.0)]
risky_a = [(ELL, 0.5), (H, 0.5)]
print(f"{'r':>5} {'g safe':>10} {'g risky':>10} {'premium':>10} {'DeltaT/2':>10} "
      f"{'t safe':>10} {'t risky':>10} {'t diff':>10}")
for r in RS:
    gs = mean_plan(safe_a, g_closed, r)
    gr = mean_plan(risky_a, g_closed, r)
    ts = mean_plan(safe_a, t_closed, r)
    tr = mean_plan(risky_a, t_closed, r)
    delta_t = (r - ELL) ** 2 / (2 * r)
    print(f"{r:5.2f} {gs:10.6f} {gr:10.6f} {gr - gs:10.6f} {delta_t / 2:10.6f} "
          f"{ts:10.6f} {tr:10.6f} {ts - tr:10.6f}")
print(f"Costs: cL = {CL:g}, cH = {CH:g}. Compare each g bar with the costs.")
print()

print("4. Menu B (interior spread). Safe: value 0.9 for sure.")
print("   Risky: values 0.6 and 1.2 with probability 1/2 each. Both means: 0.9.")
safe_b = [(0.9, 1.0)]
risky_b = [(0.6, 0.5), (1.2, 0.5)]
print(f"{'r':>5} {'g safe':>10} {'g risky':>10} {'premium':>10} {'d2/(2r)':>10} "
      f"{'t safe':>10} {'t risky':>10}")
for r in RS:
    gs = mean_plan(safe_b, g_closed, r)
    gr = mean_plan(risky_b, g_closed, r)
    ts = mean_plan(safe_b, t_closed, r)
    tr = mean_plan(risky_b, t_closed, r)
    print(f"{r:5.2f} {gs:10.6f} {gr:10.6f} {gr - gs:10.6f} {0.3**2 / (2 * r):10.6f} "
          f"{ts:10.6f} {tr:10.6f}")
print()

print("5. Reserve straddle at r = 3. Safe: value 0.4 for sure (below p).")
print("   Risky: values 0 and 0.8 with probability 1/2 each. Both means: 0.4.")
safe_r = [(0.4, 1.0)]
risky_r = [(0.0, 0.5), (0.8, 0.5)]
for name, plan in (("safe ", safe_r), ("risky", risky_r)):
    print(f"   {name}: g bar = {mean_plan(plan, g_closed, 3.0):.6f}, "
          f"t bar = {mean_plan(plan, t_closed, 3.0):.6f}")
print()

print("6. Mean-risk trade-off. Safe: value 5.5 for sure (mean 5.5).")
print("   Risky: values 1 and 9 with probability 1/2 each (mean 5.0).")
print("   Printed diff = g bar(risky) - g bar(safe). Formula: r/4 - 1 + 0.25/r.")
print("   The formula needs 1 < r < 5.5. All printed r values meet it.")
risky_c = [(1.0, 0.5), (9.0, 0.5)]
for r in (1.2, 2.0, 3.0, 3.6, 3.7320508, 4.5, 5.0):
    diff = mean_plan(risky_c, g_closed, r) - mean_plan(safe_a, g_closed, r)
    print(f"   r = {r:9.6f}: diff = {diff:+.6f}, formula = {r / 4 - 1 + 0.25 / r:+.6f}")
print()

print("7. Paper cross-check values (equation 4 and Section 4.2 quantities)")
for r in RS:
    t0 = P * (1 - P / r)
    th_ = r / 2 + P**2 / (2 * r)
    tl = ELL - (ELL**2 - P**2) / (2 * r)
    gh = H - r / 2 - P**2 / (2 * r)
    gl = (ELL**2 - P**2) / (2 * r)
    print(f"   r = {r:.2f}: t0 = {t0:.6f}, tH = {th_:.6f}, tL = {tl:.6f}, "
          f"gH = {gh:.6f}, gL = {gl:.6f}, DeltaT = {th_ - tl:.6f}, "
          f"B(1/2) = {(gh + gl) / 2:.6f}")
