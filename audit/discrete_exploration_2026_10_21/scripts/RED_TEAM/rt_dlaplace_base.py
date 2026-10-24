"""Red team: the base buy-only discrete-Laplace model at c_H = 5 (print only).

Recomputes, from the closed forms of B1/B2, the objects that carry the conclusions:
posteriors, the c_H window, the ceiling, the feedback numbers, the branch boundaries
r_I, r_F, r_N, r_U, the equilibrium set on [1.40, 1.75] under each pair of tie rules,
the single-crossing check for r_I and r_U, and the welfare numbers at r = 3.
Run from the repository root with .venv/bin/python. No assertions.
"""
from mpmath import mp, mpf, exp, sqrt, findroot

mp.dps = 40
h, l, p, rho, k, b = mpf(10), mpf(1), mpf(1) / 2, mpf(1) / 4, mpf(1) / 50, mpf(2)
cH, pi, lam = mpf(5), mpf(1) / 2, mpf(1)
a = exp(-1 / b)
gam = 1 / (1 + a)          # Pr(Z >= 0) = M_1
m1 = a / (1 + a)           # Pr(Z >= 1) = m_1
M1 = gam
dlt = 2 * gam - 1          # (1-a)/(1+a)
kap = (1 - pi) * gam * (1 - gam)


def auction(r):
    t0 = p * (1 - p / r)
    tH = r / 2 + p ** 2 / (2 * r)
    tL = l - (l ** 2 - p ** 2) / (2 * r)
    gH = h - tH
    gL = (l ** 2 - p ** 2) / (2 * r)
    DT = (r - l) ** 2 / (2 * r)
    return t0, tH, tL, gH, gL, DT


def B(r, mu):
    _, _, _, gH, gL, _ = auction(r)
    return gL + mu * (gH - gL)


def tau(r):
    _, _, _, gH, gL, _ = auction(r)
    return (cH - gL) / (gH - gL)


def Nplus(s):
    return 1 - gam + pi * dlt * s


def Nminus(s):
    return gam - pi * dlt * s


def mu_plus(s):
    return pi * (1 - gam + dlt * s) / Nplus(s)


def K(r, s, ep, em):
    DT = auction(r)[5]
    return DT * kap * (ep / Nplus(s) + em / Nminus(s))


def s_star(r):
    t = tau(r)
    return (1 - gam) * (t - pi) / (pi * dlt * (1 - t))


def rfrak(d):
    return l + d + sqrt(d ** 2 + 2 * l * d)


def r_ceiling(mu):
    return (mu * h - cH + sqrt((mu * h - cH) ** 2 + mu * ((1 - mu) * l ** 2 - p ** 2))) / mu


def eq_set(r):
    """Outcomes at strength r (B2 Result 5), for each rule pair. Returns dict."""
    K0 = K(r, 0, rho, rho)
    ss = s_star(r)
    recruit = mu_plus(lam) >= tau(r)
    out = {}
    if recruit and 0 < ss < lam:
        KF = K(r, lam, 1, rho)
        Krs = K(r, ss, rho, rho)
        K1s = K(r, ss, 1, rho)
        # pieces fall strictly in s for pi <= 1/2 (B2 Result 3c)
        rows = []
        rows.append(("N", k >= K0, k >= K0, rho))
        rows.append(("F", k <= KF, k < KF, rho + (1 - rho) * Nplus(lam)))
        if Krs < k < K0:
            s_t = findroot(lambda s: K(r, s, rho, rho) - k, (mpf(0), ss))
            rows.append(("s~ (entry rho)", True, False, rho))
        if KF < k < K1s:
            s_h = findroot(lambda s: K(r, s, 1, rho) - k, (ss, lam))
            rows.append(("s^ (recruits)", True, False, rho + (1 - rho) * Nplus(s_h)))
        if Krs <= k <= K1s:
            zeta = (Nplus(ss) * (k / (auction(r)[5] * kap) - rho / Nminus(ss)) - rho) / (1 - rho)
            rows.append(("s* (CM only)", True, False, rho + (1 - rho) * zeta * Nplus(ss)))
        out["rows"] = rows
        out["K0"], out["KF"], out["Krs"], out["K1s"], out["ss"] = K0, KF, Krs, K1s, ss
    else:
        KF = K(r, lam, rho, rho)
        rows = [("N", k >= K0, k >= K0, rho), ("F (entry rho)", k <= KF, k < KF, rho)]
        if KF < k < K0:
            rows.append(("s~ (entry rho)", True, False, rho))
        out["rows"] = rows
        out["K0"], out["KF"], out["ss"] = K0, KF, ss
    return out


print("=== constants ===")
print("a =", a, " m1 =", m1, " M1 =", M1, " delta =", dlt, " kappa =", kap)
print("Lambda = 2*gamma*(1-gamma) =", 2 * gam * (1 - gam))
print("B_1.2(1/2) =", B(mpf('1.2'), pi), " B_3(M1) =", B(mpf(3), M1), " B_4.2(M1) =", B(mpf('4.2'), M1))
print("B_3.6(M1) =", B(mpf('3.6'), M1), " B_1(M1) =", B(mpf(1) + mpf(10) ** -12, M1))
print("r_C (c_H=5, mu=M1) =", r_ceiling(M1))
print("Delta_T(1.2) =", auction(mpf('1.2'))[5], " Delta_T(3) =", auction(mpf(3))[5])
print("rho*m1*Delta_T(3) =", rho * m1 * auction(mpf(3))[5], " rho*Lambda*Delta_T(3) =", rho * 2 * gam * (1 - gam) * auction(mpf(3))[5])

print("\n=== feedback at r = 3 (gross and net of k) ===")
g_with = K(mpf(3), 1, 1, rho)
g_fix = K(mpf(3), 1, rho, rho)
print("entry after good news:  gross", g_with, " net", g_with - k)
print("entry fixed at rho:     gross", g_fix, " net", g_fix - k)
print("closed form 2*rho*a*Delta_T/(1+a)^2 - k =", 2 * rho * a * auction(mpf(3))[5] / (1 + a) ** 2 - k)
print("feedback condition (1+rho)a/(1+a)^2 > rho/2:", (1 + rho) * a / (1 + a) ** 2, ">", rho / 2)

print("\n=== entry and ownership at r = 3 under full purchases ===")
print("E = rho + (1-rho)*N_+(1) =", rho + (1 - rho) * Nplus(1), " N_+(1) =", Nplus(1))
print("O_H = pi*[rho + (1-rho)*(1-gamma+delta)] =", pi * (rho + (1 - rho) * (1 - gam + dlt)))

print("\n=== branch boundaries ===")
KFhat = kap * (1 / Nplus(lam) + rho / Nminus(lam))
rF = rfrak(k / KFhat)
rN = rfrak(k / (rho * (1 - pi)))
print("r_F =", rF, " (B1 formula:", rfrak(k * (1 + a) ** 2 / ((1 + rho) * a)), ")")
print("r_N =", rN, " paper r_N = rfrak(2k/rho) =", rfrak(2 * k / rho))
print("rfrak(k/(rho*Lambda)) =", rfrak(k / (rho * 2 * gam * (1 - gam))), " rfrak(2k) =", rfrak(2 * k))


def f_I(r):
    return K(r, s_star(r), 1, rho) - k


def f_U(r):
    return K(r, s_star(r), rho, rho) - k


rI = findroot(f_I, (mpf('1.3'), mpf('1.5')))
rU = findroot(f_U, (mpf('1.7'), mpf('1.9')))
print("r_I (K_1(s*(r)) = k) =", rI)
print("r_U (K_rho(s*(r)) = k) =", rU)

print("\n=== single-crossing check on a fine grid (numerical diagnostic) ===")
lo, hi, n = mpf('1.05'), mpf('3.9'), 5700
grid = [lo + (hi - lo) * i / n for i in range(n + 1)]
for name, f in (("K_1(s*(r)) - k", f_I), ("K_rho(s*(r)) - k", f_U)):
    vals = [(r, f(r)) for r in grid if 0 < s_star(r) < lam]
    changes = [(vals[i][0], vals[i + 1][0]) for i in range(len(vals) - 1) if (vals[i][1] > 0) != (vals[i + 1][1] > 0)]
    print(name, ": grid points", len(vals), " range of r", vals[0][0], "to", vals[-1][0], " sign changes", len(changes), changes)
print("s*(r) in (0, 1) for r in [", min(r for r in grid if 0 < s_star(r) < lam), ",", max(r for r in grid if 0 < s_star(r) < lam), "]")

print("\n=== equilibrium set near [1.40, 1.77] (c_H = 5) ===")
print("columns: outcome | exists under IM | exists under I0 | entry")
for rr in ['1.40', '1.405', '1.41', '1.42', '1.43', '1.44', '1.443', '1.445', '1.45', '1.5', '1.55', '1.6', '1.65', '1.7', '1.74', '1.747', '1.748', '1.75', '1.76', '1.762', '1.765', '1.77']:
    r = mpf(rr)
    o = eq_set(r)
    rows = o["rows"]
    txt = "; ".join(f"{nm}: IM={'y' if im else 'n'} I0={'y' if i0 else 'n'} E={mp.nstr(E, 7)}" for nm, im, i0, E in rows if im or i0)
    print(f"r={rr}: {txt}")

print("\n=== welfare at r = 3 (access to prices) ===")
r = mpf(3)
t0, tH, tL, gH, gL, DT = auction(r)
eH_acc = rho + (1 - rho) * (1 - gam + dlt)
eL_acc = rho + (1 - rho) * (1 - gam)
E_acc = pi * eH_acc + (1 - pi) * eL_acc
RT_acc = t0 + pi * eH_acc * (tH - t0) + (1 - pi) * eL_acc * (tL - t0)
RT_hid = t0 + rho * (pi * (tH - t0) + (1 - pi) * (tL - t0))
W_acc = (r ** 2 - p ** 2) / (2 * r) + pi * eH_acc * (gH + p ** 2 / r) + (1 - pi) * eL_acc * (gL + p ** 2 / r) - cH * (E_acc - rho)
W_hid = (r ** 2 - p ** 2) / (2 * r) + rho * (pi * (gH + p ** 2 / r) + (1 - pi) * (gL + p ** 2 / r))
print("R_T access", RT_acc, " hidden", RT_hid, " gain", RT_acc - RT_hid)
print("W (preparation costs only) access", W_acc, " hidden", W_hid, " gain", W_acc - W_hid)
print("W (also minus trading cost pi*k) access", W_acc - pi * k, " hidden", W_hid - pi * k)
print("investor gross profit: access", pi * g_with, " hidden", pi * g_fix)
