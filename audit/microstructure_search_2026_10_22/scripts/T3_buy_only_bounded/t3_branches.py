"""Branch and window analysis for T3 candidates.

Print-only. Float scans are numerical diagnostics. The B1 certificates at
r = 31/20, 8/5, 33/20 use exact rational arithmetic (fractions): alpha_T and
sigma_T are exact, alpha_A is bracketed by exact payoff sign evaluations.
"""
import sys
from fractions import Fraction as F
from math import sqrt, comb

sys.path.insert(0, "audit/microstructure_search_2026_10_22/scripts/T3_buy_only_bounded")
from t3_exact import auction, evaluate, b1, Bval, RHO, K  # noqa: E402

KF, RHOF = 0.02, 0.25


def Delta(r):
    return (r - 1.0) ** 2 / (2 * r)


def tau(r):
    gL = 3.0 / (8 * r)
    gH = 10 - r / 2 - 1.0 / (8 * r)
    return (6 - gL) / (gH - gL)


def r_of_Delta(d):
    return 1 + d + sqrt(d * d + 2 * d)


def rC(mu):
    """Root above 1 of B_r(mu) = 6, or inf if B stays above 6 up to h=10 cap use."""
    if mu <= 0:
        return float("inf")
    disc = (mu * 10 - 6) ** 2 + mu * ((1 - mu) - 0.25)
    return (mu * 10 - 6 + sqrt(max(disc, 0.0))) / mu


# ---------------- B1 closed forms (float) ----------------

def b1_mu(alpha, th):
    d = 1 - 3 * th
    mu0 = ((1 - 2 * th) - alpha * d) / (2 * (1 - 2 * th) - alpha * d)
    mu1 = (th + alpha * d) / (2 * th + alpha * d)
    return mu0, mu1


def b1_S(alpha, th, e0, e1):
    d = 1 - 3 * th
    D0 = 2 * (1 - 2 * th) - alpha * d
    D1 = 2 * th + alpha * d
    return th * (1 - 2 * th) * (e0 / D0 + e1 / D1)


def b1_U(alpha, r, th):
    t = tau(r)
    mu0, mu1 = b1_mu(alpha, th)
    e0 = 1.0 if mu0 >= t else RHOF
    e1 = 1.0 if mu1 >= t else RHOF
    return Delta(r) * b1_S(alpha, th, e0, e1) - KF


def b1_alpha_star(r, th):
    t = tau(r)
    if th < 1 / 3:
        return th * (2 * t - 1) / ((1 - 3 * th) * (1 - t))
    if th > 1 / 3:
        return (1 - 2 * th) * (2 * t - 1) / ((3 * th - 1) * (1 - t))
    return None


def b1_entry(alpha, th, e_rec, side):
    """Entry with recruiting-flow entry rate e_rec; side='low' theta<1/3 (flow1)."""
    if side == "low":
        wrec_plus_top = th + alpha * (1 - 2 * th) / 2  # w1 + w2
        w_top = alpha * th / 2
        w_rec = wrec_plus_top - w_top
    else:
        w_rec = (1 - 2 * th) + alpha * (3 * th - 1) / 2  # w0
        w_top = alpha * th / 2
    return RHOF + (e_rec - RHOF) * w_rec + (1 - RHOF) * w_top


def b1_branch_table(th, lam):
    side = "low" if th < 1 / 3 else "high"
    CN = RHOF * (1 - th) / 2
    rN = r_of_Delta(KF / CN)
    mu_rec_lam = b1_mu(lam, th)[1] if side == "low" else b1_mu(lam, th)[0]
    # r_F: first crossing of U(lam; r) from below
    rF = None
    rs = [1.01 + 0.001 * i for i in range(2990)]
    prev = b1_U(lam, rs[0], th)
    for r in rs[1:]:
        cur = b1_U(lam, r, th)
        if prev < 0 <= cur:
            lo, hi = r - 0.001, r
            for _ in range(60):
                mid = (lo + hi) / 2
                if b1_U(lam, mid, th) < 0:
                    lo = mid
                else:
                    hi = mid
            rF = (lo + hi) / 2
            break
        prev = cur
    print(f"\nB1 theta={th} lambda={lam}: C_N={CN:.6f} r_N={rN:.6f} r_F={rF} "
          f"mu_rec(lam)={mu_rec_lam:.6f} rC(mu_rec)={rC(mu_rec_lam):.6f}")
    for r in (1.55, 1.60, 1.65, 3.0, 3.6):
        astar = b1_alpha_star(r, th)
        unt = Delta(r) * CN - KF
        ufull = b1_U(lam, r, th)
        line = f" r={r}: U_NTdev={unt:+.6f} U_full={ufull:+.6f} alpha*={astar}"
        if astar is not None and 0 <= astar <= lam:
            e0, e1 = (RHOF, 1.0) if side == "low" else (1.0, RHOF)
            uplus = Delta(r) * b1_S(astar, th, e0, e1) - KF
            uminus = Delta(r) * b1_S(astar, th, RHOF, RHOF) - KF
            line += f" U(a*-)={uminus:+.6f} U(a*+)={uplus:+.6f}"
            if uplus > 0 > ufull:
                lo, hi = astar, lam
                for _ in range(80):
                    mid = (lo + hi) / 2
                    if Delta(r) * b1_S(mid, th, e0, e1) - KF > 0:
                        lo = mid
                    else:
                        hi = mid
                aA = (lo + hi) / 2
                line += f" alpha_A={aA:.6f} E_A={b1_entry(aA, th, 1.0, side):.6f}"
            if uminus < 0 < uplus:
                d = 1 - 3 * th
                D0 = 2 * (1 - 2 * th) - astar * d
                D1 = 2 * th + astar * d
                target = KF / (Delta(r) * th * (1 - 2 * th))
                if side == "low":
                    eT = D1 * (target - RHOF / D0)
                else:
                    eT = D0 * (target - RHOF / D1)
                line += f" e_T={eT:.6f} E_T={b1_entry(astar, th, eT, side):.6f}"
        print(line)


# ---------------- Exact B1 certificates ----------------

def certificates(theta):
    print(f"\n=== Exact certificates B1 theta={theta}, lambda=1 ===")
    f = b1(theta)
    CN = RHO * (1 - theta) / 2
    for r in (F(31, 20), F(8, 5), F(33, 20)):
        a = auction(r)
        t = a["tau"]
        D = a["D"]
        unt = D * CN - K
        # alpha* exact (theta < 1/3 branch)
        astar = theta * (2 * t - 1) / ((1 - 3 * theta) * (1 - t))
        ev_star = evaluate(f, astar, 1, a)
        mu1_star = ev_star["mu"][1]
        # sigma_T exact: solve S = k/D for e1 at alpha*
        d = 1 - 3 * theta
        D0 = 2 * (1 - 2 * theta) - astar * d
        D1 = 2 * theta + astar * d
        target = K / (D * theta * (1 - 2 * theta))
        eT = D1 * (target - RHO / D0)
        sigT = (eT - RHO) / (1 - RHO)
        # entry on T branch: masses
        w = ev_star["w"]
        ET = RHO + (eT - RHO) * w[1] + (1 - RHO) * w[2]
        # alpha_A bracket by exact bisection on U(alpha) with rule E
        lo, hi = astar, F(1)
        ulo = evaluate(f, lo, 1, a)["U"][1]
        uhi = evaluate(f, hi, 1, a)["U"][1]
        bracket = "none"
        eA_lo = eA_hi = None
        if ulo > 0 > uhi:
            for _ in range(70):
                mid = (lo + hi) / 2
                if evaluate(f, mid, 1, a)["U"][1] > 0:
                    lo = mid
                else:
                    hi = mid
            bracket = f"[{float(lo):.8f}, {float(hi):.8f}] width={float(hi-lo):.2e}"
            eA_lo = RHO + (1 - RHO) * (theta + lo * (1 - 2 * theta) / 2)
            eA_hi = RHO + (1 - RHO) * (theta + hi * (1 - 2 * theta) / 2)
        print(f" r={r}: tau={t} ({float(t):.6f}) U_NTdev={unt} ({float(unt):+.6f})")
        print(f"   alpha_T={astar} ({float(astar):.6f}) mu1(alpha_T)-tau={mu1_star - t} "
              f"sigma_T={sigT} ({float(sigT):.6f}) E_T={ET} ({float(ET):.6f})")
        print(f"   alpha_A bracket {bracket} U(a*)={ulo} ({float(ulo):+.6f}) U(1)={uhi} ({float(uhi):+.6f})")
        if eA_lo is not None:
            print(f"   E_A in [{float(eA_lo):.8f}, {float(eA_hi):.8f}]")


# ---------------- Generic float evaluator for B2/B4 windows ----------------

def convf(f, g):
    out = {}
    for x, px in f.items():
        for y, py in g.items():
            out[x + y] = out.get(x + y, 0.0) + px * py
    return out


def trif(N, th):
    f = {0: 1.0}
    for _ in range(N):
        f = convf(f, {-1: th, 0: 1 - 2 * th, 1: th})
    return f


def binf(N, be):
    return {j: comb(N, j) * be ** j * (1 - be) ** (N - j) for j in range(N + 1)}


def gen_U(f, alpha, r, q=1, e_forced=None):
    t = tau(r)
    flows = sorted(set(f) | {z + q for z in f})
    mu, ent = {}, {}
    for x in flows:
        fL = f.get(x, 0.0)
        fH = (1 - alpha) * fL + alpha * f.get(x - q, 0.0)
        den = fH + fL
        mu[x] = fH / den if den > 0 else 1.0
        ent[x] = e_forced if e_forced is not None else (1.0 if mu[x] >= t else RHOF)
    gross = sum(f[z] * ent[z + q] * (1 - mu[z + q]) for z in f)
    entry = 0.0
    for x in flows:
        fL = f.get(x, 0.0)
        fH = (1 - alpha) * fL + alpha * f.get(x - q, 0.0)
        entry += 0.5 * (fH + fL) * ent[x]
    return Delta(r) * gross - KF, entry


def gen_window(name, f, lam=1.0, q=1):
    b = max(f)
    CN = RHOF * (1 - f[b]) / 2 if q == 1 else None
    rN = r_of_Delta(KF / CN) if CN else float("nan")
    rF = None
    rs = [1.01 + 0.002 * i for i in range(1495)]
    prev = gen_U(f, lam, rs[0], q)[0]
    for r in rs[1:]:
        cur = gen_U(f, lam, r, q)[0]
        if prev < 0 <= cur and rF is None:
            rF = r
            break
        prev = cur
    print(f"\n{name}: f(b)={f[b]:.6f} C_N={CN} r_N={rN:.4f} r_F(first crossing, grid)={rF}")
    for r in (1.55, 1.60, 1.65, 3.0):
        unt = gen_U(f, 0.0, r, q)[0]
        ufull, efull = gen_U(f, lam, r, q)
        # root scan on alpha grid
        roots = []
        al = [0.002 * i for i in range(501)]
        vals = [gen_U(f, x, r, q)[0] for x in al]
        for i in range(len(al) - 1):
            if vals[i] > 0 >= vals[i + 1] or vals[i] < 0 <= vals[i + 1]:
                roots.append((round(al[i], 3), round(gen_U(f, al[i], r, q)[1], 4)))
        # hidden-economy minimum payoff on grid (r=3 only meaningful)
        hid_min = min(gen_U(f, x, r, q, e_forced=RHOF)[0] for x in al[::10])
        print(f" r={r}: U_NTdev={unt:+.5f} U_full={ufull:+.5f} E_full={efull:.4f} "
              f"signchanges(alpha,E)={roots[:6]} minU_hidden(grid)={hid_min:+.5f}")


def main():
    print("tau at 1.55/1.6/1.65:", [round(tau(r), 6) for r in (1.55, 1.6, 1.65)])
    print("Delta at 1.55/1.6/1.65:", [round(Delta(r), 6) for r in (1.55, 1.6, 1.65)])

    for th, lam in [(0.14, 1.0), (0.15, 1.0), (0.20, 1.0), (0.22, 1.0), (0.25, 1.0),
                    (0.40, 1.0), (0.45, 1.0), (0.15, 0.9), (0.15, 0.75), (0.20, 0.8), (0.20, 0.5)]:
        b1_branch_table(th, lam)

    certificates(F(3, 20))
    certificates(F(7, 50))

    print("\n########## Working-range scan B1 lambda=1 (float diagnostic) ##########")
    flags = {"recruit_r1": [], "gap_recruit": [], "full_window_nonempty": [],
             "full_window_covers_155_165": [], "alphaA_at_three": [], "all_three": []}
    th = 0.02
    rows = []
    while th <= 0.4901:
        side_low = th < 1 / 3
        mu_rec = b1_mu(1.0, th)[1] if side_low else b1_mu(1.0, th)[0]
        rec = mu_rec >= tau(3.0)
        e0, e1 = (RHOF, 1.0) if side_low else (1.0, RHOF)
        CT = b1_S(1.0, th, e0, e1)
        CN = RHOF * (1 - th) / 2
        gap = CT > CN
        rN = r_of_Delta(KF / CN)
        rF = r_of_Delta(KF / CT) if CT > 0 else float("inf")
        top = min(rN, rC(mu_rec))
        win = gap and rF <= top
        covers = win and rF <= 1.55 and top >= 1.65
        okA = True
        for r in (1.55, 1.60, 1.65):
            astar = b1_alpha_star(r, th)
            if astar is None or not (0 <= astar <= 1):
                okA = False
                break
            uplus = Delta(r) * b1_S(astar, th, e0, e1) - KF
            ufull = Delta(r) * CT - KF if mu_rec >= tau(r) else b1_U(1.0, r, th)
            if not (uplus > 0 > ufull and r <= rN):
                okA = False
                break
        rows.append((round(th, 3), rec, gap, win, covers, okA))
        th += 0.005

    def spans(idx):
        out, cur = [], None
        for row in rows:
            if row[idx]:
                cur = [row[0], row[0]] if cur is None else [cur[0], row[0]]
            else:
                if cur:
                    out.append(tuple(cur))
                cur = None
        if cur:
            out.append(tuple(cur))
        return out

    print(" recruit at r1 (interior):", spans(1))
    print(" feedback gap > 0 (recruit pattern):", spans(2))
    print(" NT+full window nonempty:", spans(3))
    print(" NT+full window covers [1.55,1.65]:", spans(4))
    print(" alpha_A + NT at 1.55,1.60,1.65:", spans(5))
    both = [(r[0], r[1] and r[5]) for r in rows]
    out, cur = [], None
    for x, ok in both:
        if ok:
            cur = [x, x] if cur is None else [cur[0], x]
        else:
            if cur:
                out.append(tuple(cur))
            cur = None
    if cur:
        out.append(tuple(cur))
    print(" recruit_r1 AND alphaA_three:", out)

    print("\n########## Lambda scan at theta=0.15 and 0.20 (float diagnostic) ##########")
    for th in (0.15, 0.20):
        side = "low"
        e0, e1 = RHOF, 1.0
        CN = RHOF * (1 - th) / 2
        rN = r_of_Delta(KF / CN)
        print(f"theta={th} r_N={rN:.4f}")
        lam = 0.30
        while lam <= 1.001:
            mu_rec = b1_mu(lam, th)[1]
            CT = b1_S(lam, th, e0, e1)
            rF = r_of_Delta(KF / CT)
            top = min(rN, rC(mu_rec))
            win = CT > CN and rF <= top
            okA = all(
                (lambda r: (b1_alpha_star(r, th) is not None
                            and 0 <= b1_alpha_star(r, th) < lam
                            and Delta(r) * b1_S(b1_alpha_star(r, th), th, e0, e1) - KF > 0
                            > Delta(r) * CT - KF))(r)
                for r in (1.55, 1.60, 1.65))
            print(f" lam={lam:.3f} mu1={mu_rec:.4f} recruit_r1={mu_rec >= tau(3.0)} "
                  f"CT={CT:.4f} rF={rF:.4f} window_top={top:.4f} window={win} alphaA3={okA}")
            lam += 0.05

    print("\n########## B2/B4 windows (float diagnostic) ##########")
    gen_window("B2a N=2 th=1/3", trif(2, 1 / 3))
    gen_window("B2a N=3 th=1/3", trif(3, 1 / 3))
    gen_window("B2a N=3 th=1/5", trif(3, 0.2))
    gen_window("B2a N=5 th=1/3", trif(5, 1 / 3))
    gen_window("B2b N=3 beta=1/4", binf(3, 0.25))
    gen_window("B2b N=3 beta=1/2", binf(3, 0.5))
    gen_window("B4 geom5", {-2: 0.1, -1: 0.2, 0: 0.4, 1: 0.2, 2: 0.1})
    gen_window("B3xB2 N=2 th=1/3 q=2", trif(2, 1 / 3), q=2)


if __name__ == "__main__":
    main()
