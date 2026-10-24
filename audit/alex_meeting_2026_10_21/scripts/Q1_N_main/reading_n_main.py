"""Reading N, main line: nature draws the challenger's value distribution.

Print-only script for memo Q1_N_main.md. It
  1. computes t_0, t_j, g_j, W_j for type cdfs G_H, G_L and a uniform
     incumbent from the integral formulas of the memo (Claims 1-2),
  2. recomputes the same objects by direct double integration of the
     sale rule (OA.50) and prints the discrepancy,
  3. prints the split identity, the spread kernel, and the comparative
     statics in r (Claims 3-4), including the reserve jump,
  4. evaluates the Proposition 2 analog with a general prior (Claims 6-10)
     at the benchmark vector and at stated repaired vectors.

Run from the repository root:
  .venv/bin/python audit/alex_meeting_2026_10_21/scripts/Q1_N_main/reading_n_main.py
"""
from __future__ import annotations

import math
from dataclasses import dataclass, replace

from scipy import integrate, optimize

QUAD = dict(epsabs=1e-13, epsrel=1e-12, limit=500)


# ----------------------------------------------------------------- type laws
@dataclass(frozen=True)
class Mix:
    """Finite mixture of atoms ('atom', x, w) and uniform pieces ('unif', a, b, w)."""
    name: str
    parts: tuple

    def cdf(self, u: float) -> float:  # Pr(theta <= u)
        s = 0.0
        for c in self.parts:
            if c[0] == "atom":
                s += c[2] * (c[1] <= u)
            else:
                _, a, b, w = c
                s += w * min(max((u - a) / (b - a), 0.0), 1.0)
        return s

    def cdf_left(self, u: float) -> float:  # Pr(theta < u)
        s = 0.0
        for c in self.parts:
            if c[0] == "atom":
                s += c[2] * (c[1] < u)
            else:
                _, a, b, w = c
                s += w * min(max((u - a) / (b - a), 0.0), 1.0)
        return s

    def top(self) -> float:
        return max(c[1] if c[0] == "atom" else c[2] for c in self.parts)

    def knots(self) -> list[float]:
        k: list[float] = []
        for c in self.parts:
            k += [c[1]] if c[0] == "atom" else [c[1], c[2]]
        return k

    def expect(self, phi, extra=()) -> float:
        s = 0.0
        for c in self.parts:
            if c[0] == "atom":
                s += c[2] * phi(c[1])
            else:
                _, a, b, w = c
                s += w * pquad(phi, a, b, extra) / (b - a)
        return s


def atom(x: float) -> Mix:
    return Mix(f"atom({x})", (("atom", x, 1.0),))


def unif(a: float, b: float) -> Mix:
    return Mix(f"U[{a},{b}]", (("unif", a, b, 1.0),))


def pquad(fun, lo: float, hi: float, points=()) -> float:
    """Quadrature split at the given points (kinks and jumps)."""
    if hi <= lo:
        return 0.0
    pts = sorted({lo, hi, *[x for x in points if lo < x < hi]})
    return sum(integrate.quad(fun, a, b, **QUAD)[0] for a, b in zip(pts[:-1], pts[1:]))


# ------------------------------------------------------------- auction layer
@dataclass(frozen=True)
class Pay:
    r: float
    p: float
    t0: float
    tH: float
    tL: float
    gH: float
    gL: float
    WH: float
    WL: float

    @property
    def DT(self) -> float:
        return self.tH - self.tL

    @property
    def gap(self) -> float:
        return self.gH - self.gL

    def B(self, mu: float) -> float:
        return self.gL + mu * (self.gH - self.gL)


def F_unif(r: float):
    return lambda u: min(max(u / r, 0.0), 1.0)


def pay_formula(r: float, p: float, GH: Mix, GL: Mix) -> Pay:
    """Claims 1-2: integral formulas with the reserve jump p F(p)."""
    F = F_unif(r)
    t0 = p * (1.0 - F(p))

    def t_j(G: Mix) -> float:
        jump = p * F(p) * (1.0 - G.cdf_left(p))
        body = pquad(lambda u: (1.0 - G.cdf(u)) * (1.0 - F(u)), p, r, [*G.knots()])
        return t0 + jump + body

    def g_j(G: Mix) -> float:
        return pquad(lambda u: (1.0 - G.cdf(u)) * F(u), p, max(G.top(), p), [*G.knots(), r])

    def W_j(G: Mix) -> float:
        return G.expect(lambda v: F(v) * (v >= p), extra=[p, r])

    return Pay(r, p, t0, t_j(GH), t_j(GL), g_j(GH), g_j(GL), W_j(GH), W_j(GL))


def T_real(R: float, v: float, p: float) -> float:
    """OA.50 target proceeds, challenger with value v has prepared."""
    if v < p:
        return p if R >= p else 0.0
    return max(p, min(R, v))


def G_real(R: float, v: float, p: float) -> float:
    return max(v - max(p, R), 0.0)


def pay_oracle(r: float, p: float, GH: Mix, GL: Mix) -> Pay:
    """Direct double integration of OA.50 over R ~ U[0, r] and theta ~ G_j."""
    def EF(fun, v):
        return pquad(lambda R: fun(R, v, p), 0.0, r, [p, v]) / r

    t0 = pquad(lambda R: p if R >= p else 0.0, 0.0, r, [p]) / r
    out = []
    for G in (GH, GL):
        out.append(G.expect(lambda v: EF(T_real, v), extra=[p, r]))
    for G in (GH, GL):
        out.append(G.expect(lambda v: EF(G_real, v), extra=[p, r]))
    for G in (GH, GL):
        out.append(G.expect(lambda v: pquad(lambda R: 1.0 if (v >= p and R < v) else 0.0,
                                            0.0, r, [p, v]) / r, extra=[p, r]))
    return Pay(r, p, t0, *out)


def D_fun(GH: Mix, GL: Mix):
    return lambda u: GL.cdf(u) - GH.cdf(u)


def D_left_p(p: float, GH: Mix, GL: Mix) -> float:
    return GL.cdf_left(p) - GH.cdf_left(p)


def split_rhs(r: float, p: float, GH: Mix, GL: Mix) -> float:
    """Claim 3: Delta_T + (g_H - g_L) = p F(p) D(p-) + int_p^inf D."""
    D = D_fun(GH, GL)
    top = max(GH.top(), GL.top(), p)
    return p * F_unif(r)(p) * D_left_p(p, GH, GL) + pquad(D, p, top, [*GH.knots(), *GL.knots()])


def kernel_DT(r: float, p: float, GH: Mix, GL: Mix) -> float:
    """Claim 3: Delta_T = E_F[phi(R)], phi = p D(p-) below p, int_p^R D above p."""
    D = D_fun(GH, GL)
    knots = [*GH.knots(), *GL.knots()]

    def phi(R: float) -> float:
        if R < p:
            return p * D_left_p(p, GH, GL)
        return pquad(D, p, R, knots)

    return pquad(phi, 0.0, r, [p, *knots]) / r


def dDT_dr_formula(r: float, p: float, GH: Mix, GL: Mix) -> float:
    """Claim 4(d), eq. (N10): d Delta_T / dr = r^-2 [int_p^r u D(u) du - p^2 D(p-)]."""
    D = D_fun(GH, GL)
    body = pquad(lambda u: u * D(u), p, r, [*GH.knots(), *GL.knots()])
    return (body - p * p * D_left_p(p, GH, GL)) / (r * r)


# --------------------------------------------------------- trading layer
def m_of(pi: float, b: float) -> float:
    return pi / (pi + (1.0 - pi) * math.exp(2.0 / b))


def M_of(pi: float, b: float) -> float:
    return pi / (pi + (1.0 - pi) * math.exp(-2.0 / b))


def logit(x: float) -> float:
    return math.log(x / (1.0 - x))


def lap_pdf(z: float, b: float) -> float:
    return math.exp(-abs(z) / b) / (2.0 * b)


def lap_sf(z: float, b: float) -> float:
    return 1.0 - 0.5 * math.exp(z / b) if z <= 0 else 0.5 * math.exp(-z / b)


@dataclass(frozen=True)
class Econ:
    name: str
    GH: Mix
    GL: Mix
    p: float = 0.5
    pi: float = 0.5
    rho: float = 0.25
    c_L: float = 1.0
    c_H: float = 6.0
    b: float = 2.0
    k: float = 0.02
    r0: float = 1.2
    r1: float = 3.0
    r2: float = 3.6


def full_orders(P: Pay, e: Econ) -> dict:
    """Eq. (12) analog with prior pi: closed forms and a direct quadrature check."""
    m, M = m_of(e.pi, e.b), M_of(e.pi, e.b)
    tau = (e.c_H - P.gL) / P.gap
    if tau > M:
        xs, aH, aL = float("nan"), 0.0, 0.0
    elif tau <= m:
        xs, aH, aL = float("nan"), 1.0, 1.0
    else:
        xs = 0.5 * e.b * (logit(tau) - logit(e.pi)) if tau < M else 1.0
        aH, aL = lap_sf(xs - 1.0, e.b), lap_sf(xs + 1.0, e.b)
    eH, eL = e.rho + (1 - e.rho) * aH, e.rho + (1 - e.rho) * aL
    out = dict(tau=tau, xs=xs, aH=aH, aL=aL, eH=eH, eL=eL,
               E=e.pi * eH + (1 - e.pi) * eL,
               OH=e.pi * eH * P.WH,
               adm=e.pi * eH * (1 - e.GH.cdf_left(e.p)) + (1 - e.pi) * eL * (1 - e.GL.cdf_left(e.p)),
               RT=P.t0 + e.pi * eH * (P.tH - P.t0) + (1 - e.pi) * eL * (P.tL - P.t0))
    # direct check: posterior root, crossing probabilities, and J_H, J_L (A.7)
    mu = lambda x: e.pi * lap_pdf(x - 1, e.b) / (e.pi * lap_pdf(x - 1, e.b) + (1 - e.pi) * lap_pdf(x + 1, e.b))
    if m < tau < M:
        xr = optimize.brentq(lambda x: mu(x) - tau, -1.0, 1.0, xtol=1e-15)
        aH_d = pquad(lambda x: lap_pdf(x - 1, e.b), xr, 80.0, [1.0])
        aL_d = pquad(lambda x: lap_pdf(x + 1, e.b), xr, 80.0, [1.0])
    else:
        xr, aH_d, aL_d = float("nan"), aH, aL
    ent = lambda x: e.rho + (1 - e.rho) * (1.0 if (m < tau < M and x >= xr) or tau <= m else 0.0)
    pts = [-1.0, 1.0] + ([xr] if m < tau < M else [])
    JH = pquad(lambda x: lap_pdf(x - 1, e.b) * ent(x) * P.DT * (1 - mu(x)), -80.0, 80.0, pts)
    JL = pquad(lambda x: lap_pdf(x + 1, e.b) * ent(x) * P.DT * mu(x), -80.0, 80.0, pts)
    out.update(xr=xr, aH_d=aH_d, aL_d=aL_d, JH=JH, JL=JL)
    return out


def classify(P: Pay, e: Econ) -> dict:
    """Sufficient bounds of Claims 8 and 10 in one economy."""
    m, M = m_of(e.pi, e.b), M_of(e.pi, e.b)
    lam = min(m, 1 - M)
    floor = e.c_L < P.B(m)
    emax = e.rho if P.B(M) < e.c_H else 1.0
    sup_paper = P.DT
    sup_sharp = emax * P.DT * max(1 - m, M)
    glob = (1 - 1 / e.b) * e.rho * lam * P.DT
    e_prior = e.rho + (1 - e.rho) * (P.B(e.pi) >= e.c_H)
    nt_exists = e_prior * P.DT * max(e.pi, 1 - e.pi) <= e.k
    res = dict(floor=floor, sup_paper=sup_paper, sup_sharp=sup_sharp, glob=glob,
               nt_exists=nt_exists, e_prior=e_prior)
    if not floor:
        res["regime"] = "floor fails (bounds do not apply)"
    elif sup_paper < e.k or sup_sharp < e.k:
        res["regime"] = "unique no trade"
        res.update(E=e_prior, OH=e.pi * e_prior * P.WH,
                   adm=e_prior * (e.pi * (1 - e.GH.cdf_left(e.p)) + (1 - e.pi) * (1 - e.GL.cdf_left(e.p))),
                   RT=P.t0 + e_prior * ((1 - e.pi) * (P.tL - P.t0) + e.pi * (P.tH - P.t0)))
    elif glob > e.k:
        res["regime"] = "unique full orders"
        res.update(full_orders(P, e))
    else:
        res["regime"] = "unresolved by sufficient bounds"
        fo = full_orders(P, e)
        res["fo_exists"] = e.k < (1 - 1 / e.b) * min(fo["JH"], fo["JL"])
        res["nt_OH"] = e.pi * e_prior * P.WH
        res.update({f"fo_{kk}": v for kk, v in fo.items()})
    return res


def conditions(e: Econ, P0: Pay, P1: Pay, P2: Pay) -> dict:
    m, M = m_of(e.pi, e.b), M_of(e.pi, e.b)
    lam = min(m, 1 - M)
    gb = lambda P: (1 - 1 / e.b) * e.rho * lam * P.DT
    return dict(
        rank=(P0.DT > 0 and P1.DT > 0 and P0.gap > 0 and P1.gap > 0),
        A1=(0 <= e.c_L < P1.B(m)),
        A2=(P0.B(e.pi) < e.c_H < P1.B(M)),
        A3=(P0.DT < e.k < gb(P1)),
        iii=(e.c_L < P2.B(m) and P2.B(M) < e.c_H and e.k < gb(P2) and P2.DT > 0),
        A1_win=(0.0, P1.B(m)), A2_win=(P0.B(e.pi), P1.B(M)), A3_win=(P0.DT, gb(P1)),
        iii_cH_floor=P2.B(M), iii_k_cap=gb(P2),
    )


# ------------------------------------------------------------------ printing
def fmt(x: float, n: int = 6) -> str:
    return f"{x:.{n}f}" if isinstance(x, float) and math.isfinite(x) else str(x)


def show_validation(e: Econ) -> None:
    print(f"  validation, {e.name}: formula vs direct integration of OA.50")
    worst = 0.0
    for r in (e.r0, e.r1, e.r2):
        A, Bo = pay_formula(r, e.p, e.GH, e.GL), pay_oracle(r, e.p, e.GH, e.GL)
        diffs = [abs(getattr(A, f) - getattr(Bo, f)) for f in ("t0", "tH", "tL", "gH", "gL", "WH", "WL")]
        worst = max(worst, *diffs)
        split_err = abs(A.DT + A.gap - split_rhs(r, e.p, e.GH, e.GL))
        kern_err = abs(A.DT - kernel_DT(r, e.p, e.GH, e.GL))
        print(f"    r={r:<5} t0={fmt(A.t0)} tH={fmt(A.tH)} tL={fmt(A.tL)} gH={fmt(A.gH)} gL={fmt(A.gL)}"
              f" DT={fmt(A.DT)} WH={fmt(A.WH)} WL={fmt(A.WL)}")
        print(f"           max|formula-oracle|={max(diffs):.2e}  |split identity err|={split_err:.2e}"
              f"  |kernel err|={kern_err:.2e}")
    print(f"    worst discrepancy over r0,r1,r2: {worst:.2e}")


def show_econ(e: Econ) -> None:
    m, M = m_of(e.pi, e.b), M_of(e.pi, e.b)
    P0, P1, P2 = (pay_formula(r, e.p, e.GH, e.GL) for r in (e.r0, e.r1, e.r2))
    c = conditions(e, P0, P1, P2)
    print(f"  {e.name}: GH={e.GH.name} GL={e.GL.name} p={e.p} pi={e.pi} rho={e.rho} c_L={e.c_L}"
          f" c_H={e.c_H} b={e.b} k={e.k} (r0,r1,r2)=({e.r0},{e.r1},{e.r2})")
    print(f"    m(pi)={fmt(m)} M(pi)={fmt(M)} 1-M(pi)={fmt(1 - M)} lambda(pi)={fmt(min(m, 1 - M))}"
          f"  D(p-)={fmt(D_left_p(e.p, e.GH, e.GL))}")
    print(f"    ranking signs DT>0, gH>gL at r0,r1: {c['rank']}")
    print(f"    (A1) c_L in [0, {fmt(c['A1_win'][1])}): {c['A1']}")
    print(f"    (A2) c_H in ({fmt(c['A2_win'][0])}, {fmt(c['A2_win'][1])}): {c['A2']}")
    print(f"    (A3) k   in ({fmt(c['A3_win'][0])}, {fmt(c['A3_win'][1])}): {c['A3']}")
    print(f"    (iii) at r2: needs c_H > B_r2(M)={fmt(c['iii_cH_floor'])}, k < {fmt(c['iii_k_cap'])}: {c['iii']}")
    for tag, P in (("r0", P0), ("r1", P1), ("r2", P2)):
        s = classify(P, e)
        line = (f"    {tag}={P.r:<5} DT={fmt(P.DT)} B(pi)={fmt(P.B(e.pi))} B(M)={fmt(P.B(M))}"
                f"  regime: {s['regime']}")
        print(line)
        if s["regime"] == "unique no trade":
            print(f"           entry={fmt(s['E'])} O_H={fmt(s['OH'])} admissible={fmt(s['adm'])} proceeds={fmt(s['RT'])}"
                  f"  (no-trade eq. exists: {s['nt_exists']})")
        elif s["regime"] == "unique full orders":
            print(f"           tau={fmt(s['tau'])} x*={fmt(s['xs'])} aH={fmt(s['aH'])} aL={fmt(s['aL'])}"
                  f" e_H={fmt(s['eH'])} e_L={fmt(s['eL'])}")
            print(f"           entry={fmt(s['E'])} O_H={fmt(s['OH'])} admissible={fmt(s['adm'])} proceeds={fmt(s['RT'])}"
                  f"  W_H={fmt(P.WH)}")
            print(f"           direct check: |x*-root|={abs(s['xs'] - s['xr']) if math.isfinite(s['xs']) else 0:.1e}"
                  f" |aH-direct|={abs(s['aH'] - s['aH_d']):.1e} |aL-direct|={abs(s['aL'] - s['aL_d']):.1e}"
                  f"  J_H={fmt(s['JH'])} J_L={fmt(s['JL'])} pi*J_H-(1-pi)*J_L={e.pi * s['JH'] - (1 - e.pi) * s['JL']:.1e}")
        elif s["regime"].startswith("unresolved"):
            print(f"           no-trade eq. exists: {s['nt_exists']} (its entry={fmt(s['e_prior'])}"
                  f" O_H={fmt(s['nt_OH'])}); full-order eq. exists (A.7 test): {s['fo_exists']}"
                  f" (its entry={fmt(s['fo_E'])} O_H={fmt(s['fo_OH'])})")
    s0, s1 = classify(P0, e), classify(P1, e)
    if s0["regime"] == "unique no trade" and s1["regime"] == "unique full orders":
        ratio_needed = e.rho / s1["eH"]
        print(f"    ownership test: W_H(r1)/W_H(r0)={fmt(P1.WH / P0.WH)} vs rho/e_H(r1)={fmt(ratio_needed)}"
              f" -> O_H rises: {P1.WH / P0.WH > ratio_needed}")


def main() -> None:
    eps = 0.05
    cls_H, cls_L = unif(10 - eps, 10 + eps), unif(1 - eps, 1 + eps)
    E0 = Econ("case 0, binary benchmark", atom(10.0), atom(1.0))
    E1 = Econ("case 1, value classes eps=0.05, p=0.5", cls_H, cls_L)
    E1h = replace(E1, name="case 1h, value classes eps=0.05, p=1.1", p=1.1)
    GH2a = Mix("0.1U[0,0.5]+0.9U[0.5,19.5]", (("unif", 0.0, 0.5, 0.1), ("unif", 0.5, 19.5, 0.9)))
    GL2a = Mix("0.1U[0,0.5]+0.9U[0.5,2.5]", (("unif", 0.0, 0.5, 0.1), ("unif", 0.5, 2.5, 0.9)))
    E2a = Econ("case 2a, wide overlap, equal mass below p", GH2a, GL2a)
    E2b = Econ("case 2b, wide overlap, unequal mass below p", unif(0.2, 19.8), unif(0.2, 2.8))
    E2c = Econ("case 2c, as 2a with rho=0.95 (H type can lose)", GH2a, GL2a, rho=0.95)

    print("=" * 100)
    print("A. Payoff formulas versus direct integration (Claims 1-3)")
    print("=" * 100)
    for e in (E0, E1, E1h, E2a, E2b, E2c):
        show_validation(e)

    print()
    print("=" * 100)
    print("B. Comparative statics in r (Claim 4): d Delta_T/dr formula vs finite difference, and the reserve jump")
    print("=" * 100)
    for e in (E1, E1h, E2a, E2b):
        Dp = D_left_p(e.p, e.GH, e.GL)
        print(f"  {e.name}: D(p-)={fmt(Dp)}  (jump p F(p) D(p-) = p^2 D(p-)/r)")
        for r in (0.6, 0.8, 1.0, 1.2, 1.5, 1.9, 2.5, 3.0, 3.6):
            if r <= e.p:
                continue
            h_ = 1e-5
            fd = (pay_formula(r + h_, e.p, e.GH, e.GL).DT - pay_formula(r - h_, e.p, e.GH, e.GL).DT) / (2 * h_)
            print(f"    r={r:<4} DT={fmt(pay_formula(r, e.p, e.GH, e.GL).DT)}"
                  f"  dDT/dr formula={fmt(dDT_dr_formula(r, e.p, e.GH, e.GL))} finite diff={fmt(fd)}")
    print("  uniform closed form (N6) and d g_H/dr = -r^-2 int_p^r u[1-G_H(u)]du, cases 2a and 2b:")
    for e in (E2a, E2b):
        for r in (0.8, 1.2, 3.0):
            P = pay_formula(r, e.p, e.GH, e.GL)
            Dp = D_left_p(e.p, e.GH, e.GL)
            sq = lambda G: G.expect(lambda v: (max(r - v, 0.0) ** 2) * (v >= e.p), extra=[e.p, r])
            n10 = Dp * ((r - e.p) ** 2 + 2 * e.p ** 2) / (2 * r) + (sq(e.GL) - sq(e.GH)) / (2 * r)
            h_ = 1e-5
            fd = (pay_formula(r + h_, e.p, e.GH, e.GL).gH - pay_formula(r - h_, e.p, e.GH, e.GL).gH) / (2 * h_)
            fo = -pquad(lambda u: u * (1 - e.GH.cdf(u)), e.p, r, e.GH.knots()) / r ** 2
            print(f"    {e.name[:7]} r={r:<4} DT={fmt(P.DT, 9)} (N6)={fmt(n10, 9)}"
                  f"  dgH/dr formula={fmt(fo)} finite diff={fmt(fd)}")
    p = 1.1
    for r in (1.2, math.sqrt(3) * p, 3.0):
        print(f"  binary/class closed form at p=1.1: r={r:.6f} DT=r/2-p+3p^2/(2r)={fmt(r / 2 - p + 1.5 * p * p / r)}")

    print()
    print("=" * 100)
    print("C. A risk ranking (mean-preserving spread): G_H=U[1,3], G_L=atom(2), p=0.5 (Claim 5)")
    print("=" * 100)
    for r in (1.5, 2.0, 2.5, 3.0, 4.0):
        P = pay_formula(r, 0.5, unif(1.0, 3.0), atom(2.0))
        print(f"  r={r:<4} DT={fmt(P.DT)} gH-gL={fmt(P.gap)} sum={fmt(P.DT + P.gap)}")

    print()
    print("=" * 100)
    print("D. Proposition 2 analog at the benchmark cost vector (Claims 6-10)")
    print("=" * 100)
    for e in (E0, E1, E1h, E2a, E2b, E2c,
              replace(E1, name="case 3a, value classes, pi=0.3", pi=0.3),
              replace(E1, name="case 3b, value classes, pi=0.7", pi=0.7)):
        show_econ(e)
        print()

    print("=" * 100)
    print("E. Repaired vectors (stated variants) where the benchmark vector fails a condition")
    print("=" * 100)
    repaired = [
        replace(E2a, name="case 2a repaired", r0=1.0, k=0.01, c_H=None),
        replace(E2b, name="case 2b repaired (rho=0.85)", rho=0.85, r0=1.0, k=None, c_H=None),
        replace(E2c, name="case 2c repaired (rho=0.95)", k=None, c_H=None),
        replace(E1, name="case 3a repaired, pi=0.3", pi=0.3, r0=1.1, k=None, c_H=None),
        replace(E1, name="case 3b repaired, pi=0.7", pi=0.7, r0=1.1, k=None, c_H=None),
    ]
    for e in repaired:
        e = choose(e)
        show_econ(e)
        print()

    print("=" * 100)
    print("F. How much inadmissible-mass gap D(p-) the sufficient conditions tolerate (numerical diagnostic)")
    print("   G_H=U[0.5,19.5]; G_L=delta*U[0,0.5]+(1-delta)*U[0.5,2.5]; p=0.5, pi=1/2, b=2; c_L=0 allowed")
    print("   feasible pair (r0<r1): DT(r0) < (1-1/b) rho lambda DT(r1) and B_r0(pi) < B_r1(M)")
    print("=" * 100)
    scan_admissibility()


def scan_admissibility() -> None:
    p, pi, b = 0.5, 0.5, 2.0
    m, M = m_of(pi, b), M_of(pi, b)
    lam = min(m, 1 - M)
    grid = [round(0.55 + 0.05 * i, 4) for i in range(150)]  # 0.55 .. 8.0
    GH = unif(0.5, 19.5)
    for delta in (0.0, 0.01, 0.02, 0.05, 0.1, 0.2):
        GL = Mix(f"delta={delta}", (("unif", 0.0, 0.5, delta), ("unif", 0.5, 2.5, 1 - delta))) if delta > 0 \
            else unif(0.5, 2.5)
        pays = {r: pay_formula(r, p, GH, GL) for r in grid}
        rmin = min(grid, key=lambda r: pays[r].DT)
        line = f"  delta=D(p-)={delta:<5} min_r DT={fmt(pays[rmin].DT)} at r={rmin:<5}"
        for rho in (0.25, 0.5, 0.85):
            best, arg = 0.0, None
            for i, r0 in enumerate(grid):
                if r0 > 3.0:
                    break
                for r1 in grid[i + 1:]:
                    P0, P1 = pays[r0], pays[r1]
                    if not (P0.B(pi) < P1.B(M) and P1.gap > 0 and P0.gap > 0 and P1.DT > 0):
                        continue
                    ratio = (1 - 1 / b) * rho * lam * P1.DT / max(P0.DT, 1e-300)
                    if ratio > best:
                        best, arg = ratio, (r0, r1)
            tag = "feasible" if best > 1 else "infeasible"
            line += f" | rho={rho}: best ratio={best:.3g} {tag} at {arg}"
        print(line)


def choose(e: Econ) -> Econ:
    """Fill c_H, k, r2 from the condition windows: c_H at the midpoint of the joint
    (A2)/(iii) window, k at the geometric midpoint of the (A3) window, r2 the first
    grid strength above r1 at which B_r2(M) < c_H."""
    m, M = m_of(e.pi, e.b), M_of(e.pi, e.b)
    P0, P1 = pay_formula(e.r0, e.p, e.GH, e.GL), pay_formula(e.r1, e.p, e.GH, e.GL)
    lo, hi = P0.B(e.pi), P1.B(M)
    c_H = e.c_H if e.c_H is not None else 0.5 * (lo + hi)
    gb = (1 - 1 / e.b) * e.rho * min(m, 1 - M) * P1.DT
    k = e.k if e.k is not None else math.sqrt(P0.DT * gb)
    r2 = e.r2
    r = e.r1
    while r < 30:
        r = round(r + 0.05, 4)
        if pay_formula(r, e.p, e.GH, e.GL).B(M) < c_H:
            r2 = r
            break
    return replace(e, c_H=round(c_H, 6), k=round(k, 6), r2=r2)


if __name__ == "__main__":
    main()
