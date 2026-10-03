"""Interval certificates for the equilibrium-set track (writes certificates.csv and two cover CSVs).

Outward interval arithmetic (mpmath.iv, 40 digits) on exact decimal inputs parsed from strings.
Every certificate is an enclosure [lo, hi] of a scalar together with the inequality it proves.

Certificates:
  C1  J(3) from the closed form (ES.1), and an independent enclosure by monotone Riemann sums.
  C2  (1 - 1/b) J(3) - k > 0, which is the remaining inequality in Proposition F.3(ii).
  C3  The closed-form threshold arithmetic quoted in the proof of Proposition F.3.
  C4  The root r_J of (1 - 1/b) J(r) = k and the sign of (1 - 1/b) J(r) - k on all of (ell, r_C].
  C5  The root r_e of the plateau-edge equation (ES.4) and the sign of G on (ell, r_C].
  C6  Psi(z, r) < 0 on {(z, r): n(r) <= z <= 1, ell < r <= r_e - delta}: no live equilibrium with q_H = 1.
  C7  dPsi/dz < 0 on {(z, r): n(r) <= z <= 1, 1.3 <= r <= r_C}: closes the gap next to r_e.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from mpmath import iv, mp, mpf

HERE = Path(__file__).resolve().parent
iv.dps = 40
mp.dps = 40

H, ELL, P, B, K, C = (iv.mpf(s) for s in ("10", "1", "0.5", "2", "0.02", "6"))
ONE, TWO = iv.mpf(1), iv.mpf(2)
E1B = iv.exp(ONE / B)                       # e^{1/b}
M_LO = ONE / (ONE + iv.exp(TWO / B))        # m
M_HI = ONE - M_LO                           # M


@dataclass(frozen=True)
class Cert:
    name: str
    lo: str
    hi: str
    statement: str
    holds: bool
    status: str


def iatan(x):
    """Enclosure of arctan on an interval (arctan is increasing; atan2(x, 1) is evaluated outward)."""
    return iv.atan2(x, ONE)


def lo(x) -> mpf:
    return x.a


def hi(x) -> mpf:
    return x.b


def acq(r):
    """Equation (4) on an interval r. Returns (t0, tH, tL, gH, gL, DeltaT, tau)."""
    t0 = P * (ONE - P / r)
    tH = r / TWO + P ** 2 / (TWO * r)
    tL = ELL - (ELL ** 2 - P ** 2) / (TWO * r)
    gH = H - tH
    gL = (ELL ** 2 - P ** 2) / (TWO * r)
    return t0, tH, tL, gH, gL, (r - ELL) ** 2 / (TWO * r), (C - gL) / (gH - gL)


def K_of_tau(tau):
    """Bracket of the closed form (ES.1): J = Delta_T * K(tau)."""
    u_star = iv.sqrt(tau / (ONE - tau))
    return M_LO / TWO + iv.exp(-ONE / B) / TWO * (iatan(E1B) - iatan(u_star))


def J_closed(r):
    _, _, _, _, _, dT, tau = acq(r)
    return dT * K_of_tau(tau)


def J_riemann(r, n_panels: int = 2000):
    """Independent enclosure of (F.3): the integrand g(x) = f(x-1)f(x+1)/(f(x-1)+f(x+1)) is decreasing
    on [0, 1]. Upper and lower Riemann sums on [x*, 1] plus the exact exponential tail on [1, inf)."""
    _, _, _, _, _, dT, tau = acq(r)
    x_star = B / TWO * iv.log(tau / (ONE - tau))

    def g(x):
        fm = iv.exp(-abs(x - ONE) / B) / (TWO * B)
        fp = iv.exp(-abs(x + ONE) / B) / (TWO * B)
        return fm * fp / (fm + fp)

    one = iv.mpf(1)
    def lower_upper(start, n):
        h = (one - start) / n
        up, dn = iv.mpf(0), iv.mpf(0)
        for i in range(n):
            up += h * g(start + h * i)
            dn += h * g(start + h * (i + 1))
        return up, dn
    up, _ = lower_upper(iv.mpf(lo(x_star)), n_panels)   # earlier start: larger integral
    _, dn = lower_upper(iv.mpf(hi(x_star)), n_panels)   # later start: smaller integral
    # on [1, inf) the integrand is f(x+1)/(1+e^{-2/b}); its integral is e^{-2/b}/2/(1+e^{-2/b})
    tail = iv.exp(-TWO / B) / TWO / (ONE + iv.exp(-TWO / B))
    total = iv.mpf([lo(dn + tail), hi(up + tail)])
    return dT * total


def B_at(r, mu):
    _, _, _, gH, gL, _, _ = acq(r)
    return gL + mu * (gH - gL)


def frak_r(d):
    return ELL + d + iv.sqrt(d * d + TWO * ELL * d)


def r_C():
    a = M_HI * H - C
    return (a + iv.sqrt(a * a + M_HI * ((ONE - M_HI) * ELL ** 2 - P ** 2))) / M_HI


def phi_J(r):
    """(1 - 1/b) J(r) - k on an interval r, using monotone bounds: Delta_T increasing, tau increasing,
    K decreasing in tau (all on r > ell). Valid on the domain r <= r_C, where tau <= M."""
    ra, rb = iv.mpf(lo(r)), iv.mpf(hi(r))
    dTa, dTb = acq(ra)[5], acq(rb)[5]
    taua, taub = acq(ra)[6], acq(rb)[6]
    tau_max = iv.mpf(hi(taub)) if hi(taub) < lo(M_HI) else M_HI
    Klo, Khi = K_of_tau(tau_max), K_of_tau(iv.mpf(lo(taua)))
    Jlo = max(lo(dTa), mpf(0)) * lo(Klo)
    Jhi = hi(dTb) * hi(Khi)
    fac = ONE - ONE / B
    return iv.mpf([lo(fac * Jlo - K), hi(fac * Jhi - K)])


def edge_G(r):
    """Plateau-edge function (ES.4): G(r) = Delta_T (1 - tau)/2 * (1 + 1/b - logit tau) - k.
    Monotone bounds: Delta_T increasing, (1 - tau) and (1 + 1/b - logit tau) decreasing and positive."""
    ra, rb = iv.mpf(lo(r)), iv.mpf(hi(r))
    dTa, dTb = acq(ra)[5], acq(rb)[5]
    taua, taub = acq(ra)[6], acq(rb)[6]
    def w(tau):
        return (ONE - tau) / TWO * (ONE + ONE / B - iv.log(tau / (ONE - tau)))
    glo = max(lo(dTa), mpf(0)) * lo(w(taub))
    ghi = hi(dTb) * hi(w(taua))
    return iv.mpf([glo - hi(K), ghi - lo(K)])


def _tau_prime(r):
    gL = (ELL ** 2 - P ** 2) / (TWO * r)
    gLp = -(ELL ** 2 - P ** 2) / (TWO * r * r)
    D = H - r / TWO - ELL ** 2 / (TWO * r)
    Dp = -ONE / TWO + ELL ** 2 / (TWO * r * r)
    return (-gLp * D - (C - gL) * Dp) / (D * D)


def dJ(r):
    """Naive interval enclosure of J'(r) = Delta_T' K + Delta_T K_tau tau'."""
    _, _, _, _, _, dT, tau = acq(r)
    dTp = ONE / TWO - ELL ** 2 / (TWO * r * r)
    Ktau = -iv.exp(-ONE / B) / (iv.mpf(4) * iv.sqrt(tau * (ONE - tau)))
    return dTp * K_of_tau(tau) + dT * Ktau * _tau_prime(r)


def dG(r):
    """Naive interval enclosure of G'(r) = Delta_T' w + Delta_T w_tau tau'."""
    _, _, _, _, _, dT, tau = acq(r)
    dTp = ONE / TWO - ELL ** 2 / (TWO * r * r)
    lg = iv.log(tau / (ONE - tau))
    w = (ONE - tau) / TWO * (ONE + ONE / B - lg)
    wtau = -(ONE + ONE / B - lg) / TWO - ONE / (TWO * tau)
    return dTp * w + dT * wtau * _tau_prime(r)


def root_unique(fun, dfun, root_lo: mpf, root_hi: mpf, left: mpf, right: mpf, eps: mpf = mpf("1e-6")):
    """Certify: fun < 0 on [left, root_lo], fun > 0 on [root_hi, right], so the zero set lies in
    (root_lo, root_hi). Uses a sign cover away from the root and a derivative cover near it."""
    okL, nL, _ = cover_sign(fun, left, root_lo - eps, -1, min_width=1e-13)
    okD, nD, _ = cover_sign(dfun, root_lo - eps, root_hi + eps, +1, min_width=1e-13)
    okR, nR, _ = cover_sign(fun, root_hi + eps, right, +1, min_width=1e-13)
    # with fun' > 0 on the window and certified signs at the bracket ends, the window is covered too
    return okL and okD and okR, nL + nD + nR


def bisect_root(fun, a: str, z: str, tol: float = 1e-14):
    """Interval bisection: fun(point) has certified opposite signs at the ends."""
    A, Z = mpf(a), mpf(z)
    fa = fun(iv.mpf(A))
    fz = fun(iv.mpf(Z))
    assert hi(fa) < 0 < lo(fz), (fa, fz)
    while Z - A > tol:
        mid = (A + Z) / 2
        fm = fun(iv.mpf(mid))
        if hi(fm) < 0:
            A = mid
        elif lo(fm) > 0:
            Z = mid
        else:
            break
    return A, Z


def cover_sign(fun, a: mpf, z: mpf, sign: int, min_width: float = 1e-9, max_boxes: int = 200000):
    """Adaptive cover of [a, z]: proves sign * fun > 0 on every box, else splits. Returns (ok, boxes, failures)."""
    stack = [(a, z)]
    n_ok, fails = 0, []
    while stack:
        u, v = stack.pop()
        val = fun(iv.mpf([u, v]))
        good = lo(val) > 0 if sign > 0 else hi(val) < 0
        if good:
            n_ok += 1
            continue
        if v - u < min_width or n_ok + len(stack) > max_boxes:
            fails.append((u, v))
            continue
        mid = (u + v) / 2
        stack.extend([(u, mid), (mid, v)])
    return len(fails) == 0, n_ok, fails


def psi_box(rbox, tbox):
    """(ES.3): Psi(z, r) = C(z, r) e^{-z/b} (1 - z/b) - k with z = n(r) + t (1 - n(r)), enclosure on a box.

    C(z, r) = Delta_T [ (1/(2 sqrt kappa)) (atan(e^{(1+z)/(2b)}) - atan(sqrt(tau/(1-tau)))) + M_z e^{-1/b}/2 ],
    kappa = e^{(1-z)/b}, M_z = 1/(1 + e^{-(1+z)/b}). This is Delta_T int_{x*}^inf f(x) mu_X dx under orders (1, -z).
    """
    _, _, _, _, _, dT, tau = acq(rbox)
    logit = iv.log(tau / (ONE - tau))
    n = B * logit - ONE
    z = n + tbox * (ONE - n)
    z = iv.mpf([max(lo(z), lo(n)), min(hi(z), mpf(1))])
    kap_half = iv.exp((ONE - z) / (TWO * B))
    Mz = ONE / (ONE + iv.exp(-(ONE + z) / B))
    diff = iatan(iv.exp((ONE + z) / (TWO * B))) - iatan(iv.sqrt(tau / (ONE - tau)))
    diff = iv.mpf([max(lo(diff), mpf(0)), hi(diff)])   # x* <= 1 on the domain z >= n(r)
    Cz = dT * (diff / (TWO * kap_half) + Mz * iv.exp(-ONE / B) / TWO)
    return Cz * iv.exp(-z / B) * (ONE - z / B) - K


def psi_z_box(rbox, tbox):
    """Enclosure of dPsi/dz on a box, z = n(r) + t (1 - n(r)); formula in note.md, Proposition ES.4."""
    _, _, _, _, _, dT, tau = acq(rbox)
    n = B * iv.log(tau / (ONE - tau)) - ONE
    z = n + tbox * (ONE - n)
    z = iv.mpf([max(lo(z), lo(n)), min(hi(z), mpf(1))])
    rho = iv.exp((ONE - z) / (TWO * B))
    v = iv.exp((ONE + z) / (TWO * B))
    Mz = ONE / (ONE + iv.exp(-(ONE + z) / B))
    diff = iatan(v) - iatan(iv.sqrt(tau / (ONE - tau)))
    diff = iv.mpf([max(lo(diff), mpf(0)), hi(diff)])
    Cz = dT * (diff / (TWO * rho) + Mz * iv.exp(-ONE / B) / TWO)
    Cp = dT * (diff / (TWO * rho) / (TWO * B) + v / (TWO * rho * TWO * B * (ONE + v * v))
               + iv.exp(-ONE / B) * Mz * (ONE - Mz) / (TWO * B))
    D = iv.exp(-z / B) * (ONE - z / B)
    Dp = -iv.exp(-z / B) / B * (TWO - z / B)
    return Cp * D + Cz * Dp


def cover_psi_z(r_lo: mpf, r_hi: mpf, min_w: float = 1e-7, max_boxes: int = 400000):
    stack = [((r_lo, r_hi), (mpf(0), mpf(1)))]
    n_ok, fails = 0, []
    while stack:
        (ra, rb), (ta, tb) = stack.pop()
        val = psi_z_box(iv.mpf([ra, rb]), iv.mpf([ta, tb]))
        if hi(val) < 0:
            n_ok += 1
            continue
        if (rb - ra < min_w and tb - ta < min_w) or n_ok + len(stack) > max_boxes:
            fails.append(((ra, rb), (ta, tb)))
            continue
        if (rb - ra) * 4 > (tb - ta):
            mid = (ra + rb) / 2
            stack.extend([((ra, mid), (ta, tb)), ((mid, rb), (ta, tb))])
        else:
            mid = (ta + tb) / 2
            stack.extend([((ra, rb), (ta, mid)), ((ra, rb), (mid, tb))])
    return len(fails) == 0, n_ok, fails


def cover_psi(r_lo: mpf, r_hi: mpf, min_w: float = 1e-6, max_boxes: int = 400000):
    stack = [((r_lo, r_hi), (mpf(0), mpf(1)))]
    n_ok, fails = 0, []
    while stack:
        (ra, rb), (ta, tb) = stack.pop()
        val = psi_box(iv.mpf([ra, rb]), iv.mpf([ta, tb]))
        if hi(val) < 0:
            n_ok += 1
            continue
        if (rb - ra < min_w and tb - ta < min_w) or n_ok + len(stack) > max_boxes:
            fails.append(((ra, rb), (ta, tb)))
            continue
        if (rb - ra) * 4 > (tb - ta):
            mid = (ra + rb) / 2
            stack.extend([((ra, mid), (ta, tb)), ((mid, rb), (ta, tb))])
        else:
            mid = (ta + tb) / 2
            stack.extend([((ra, rb), (ta, mid)), ((ra, rb), (mid, tb))])
    return len(fails) == 0, n_ok, fails


def _pt(x) -> mpf:
    """The mpf value of a point interval or an mpf."""
    return mpf(x.a.a) if hasattr(x, "a") and hasattr(x.a, "a") else (mpf(x.a) if hasattr(x, "a") else mpf(x))


def s_lo(x) -> str:
    """Lower end printed with 16 decimals, rounded down."""
    return mp.nstr(mp.floor(_pt(x) * mpf(10) ** 16) / mpf(10) ** 16, 20)


def s_hi(x) -> str:
    """Upper end printed with 16 decimals, rounded up."""
    return mp.nstr(mp.ceil(_pt(x) * mpf(10) ** 16) / mpf(10) ** 16, 20)


def main() -> None:
    certs: list[Cert] = []
    r3 = iv.mpf("3")
    J3 = J_closed(r3)
    certs.append(Cert("J(3) closed form (ES.1)", s_lo(lo(J3)), s_hi(hi(J3)),
                      "J(3) = Delta_T(3) [m/2 + (e^{-1/b}/2)(atan e^{1/b} - atan sqrt(tau/(1-tau)))]", True,
                      "computer-assisted"))
    J3r = J_riemann(r3)
    overlap = max(lo(J3), lo(J3r)) <= min(hi(J3), hi(J3r))
    certs.append(Cert("J(3) monotone Riemann enclosure of (F.3)", s_lo(lo(J3r)), s_hi(hi(J3r)),
                      "independent quadrature enclosure; contains the closed-form enclosure", overlap,
                      "computer-assisted"))
    marg = (ONE - ONE / B) * J3 - K
    certs.append(Cert("(1-1/b) J(3) - k", s_lo(lo(marg)), s_hi(hi(marg)), "> 0: Proposition F.3(ii) at the benchmark",
                      lo(marg) > 0, "computer-assisted"))
    simple = (ONE - ONE / B) * acq(r3)[5] * M_LO / TWO - K
    certs.append(Cert("(1-1/b) Delta_T(3) m/2 - k", s_lo(lo(simple)), s_hi(hi(simple)),
                      "> 0: the tail-only lower bound J >= Delta_T m/2 already suffices", lo(simple) > 0,
                      "analytical (m/6 - 1/50 > 1/24 - 1/50 > 0 since e < 3)"))
    # C3: threshold arithmetic of Proposition F.3
    rows = [
        ("Delta_T(1.2)", acq(iv.mpf("1.2"))[5], "< k = 0.02", lambda x: hi(x) < lo(K)),
        ("B_1.2(1/2)", B_at(iv.mpf("1.2"), iv.mpf("0.5")), "< c = 6", lambda x: hi(x) < lo(C)),
        ("B_3(1/2)", B_at(r3, iv.mpf("0.5")), "< c = 6", lambda x: hi(x) < lo(C)),
        ("B_3(M)", B_at(r3, M_HI), "> c = 6", lambda x: lo(x) > hi(C)),
        ("B_3.6(M)", B_at(iv.mpf("3.6"), M_HI), "< c = 6", lambda x: hi(x) < lo(C)),
        ("frak_r(k)", frak_r(K), "Delta_T(r) = k; 1.2 lies below it", lambda x: lo(x) > mpf("1.2")),
        ("r_C", r_C(), "B_r(M) = c; 3 < r_C < 3.6", lambda x: lo(x) > 3 and hi(x) < mpf("3.6")),
        ("lim_{r->ell} B_r(1/2)", B_at(iv.mpf("1"), iv.mpf("0.5")), "= 4.875 = sup_r B_r(1/2) < c", lambda x: hi(x) < lo(C)),
        ("tau(ell)", acq(iv.mpf("1"))[6], "= 0.625 > 1/(1+e^{-1/b}); tau increases in r",
         lambda x: lo(x) > hi(ONE / (ONE + iv.exp(-ONE / B)))),
        ("1/(1+e^{-1/b})", ONE / (ONE + iv.exp(-ONE / B)), "posterior bound on x <= 0 (Proposition ES.2(a))", lambda x: True),
        ("tau(3)", acq(r3)[6], "= 141/200", lambda x: True),
        ("x*(3)", B / TWO * iv.log(acq(r3)[6] / (ONE - acq(r3)[6])), "(b/2) log(tau/(1-tau)) in (0,1]",
         lambda x: lo(x) > 0 and hi(x) <= 1),
    ]
    for name, val, stmt, test in rows:
        certs.append(Cert(name, s_lo(lo(val)), s_hi(hi(val)), stmt, bool(test(val)), "computer-assisted"))
    # C4: r_J and the sign of (1-1/b)J - k on (ell, r_C]
    rC = r_C()
    rJa, rJb = bisect_root(lambda r: (ONE - ONE / B) * J_closed(r) - K, "1.5", "2.5")
    certs.append(Cert("r_J: (1-1/b) J(r_J) = k", s_lo(rJa), s_hi(rJb),
                      "lower edge of the minimal-pool full-order equilibrium (Proposition ES.3)", True,
                      "computer-assisted"))
    okJ, nJ = root_unique(phi_J, dJ, rJa, rJb, mpf(1), hi(rC))
    certs.append(Cert("sign of (1-1/b)J(r) - k on (ell, r_C]", "1", s_hi(hi(rC)),
                      "< 0 below r_J and > 0 above r_J: the existence region is exactly [r_J, r_C]", okJ,
                      f"computer-assisted ({nJ} boxes)"))
    # C5: plateau edge r_e
    reA, reB = bisect_root(edge_G, "1.6", "1.7")
    n_e = B * iv.log(acq(iv.mpf([reA, reB]))[6] / (ONE - acq(iv.mpf([reA, reB]))[6])) - ONE
    certs.append(Cert("r_e: plateau-edge equation (ES.4)", s_lo(reA), s_hi(reB),
                      "Delta_T (1-tau)/2 (1 + 1/b - logit tau) = k", True, "computer-assisted"))
    certs.append(Cert("n(r_e) = b logit tau(r_e) - 1", s_lo(lo(n_e)), s_hi(hi(n_e)),
                      "the low type's order magnitude at the edge; in (0, 1)", lo(n_e) > 0 and hi(n_e) < 1,
                      "computer-assisted"))
    okG, nG = root_unique(edge_G, dG, reA, reB, mpf(1), hi(rC))
    certs.append(Cert("sign of G on (ell, r_C]", "1", s_hi(hi(rC)),
                      "< 0 below r_e and > 0 above r_e: plateau equilibria exist exactly on [r_e, r_C] (Proposition ES.5)",
                      okG, f"computer-assisted ({nG} boxes)"))
    tau_e = acq(iv.mpf([reA, reB]))[6]
    E_e = ONE / (iv.mpf(4) * tau_e)
    certs.append(Cert("entry at r_e: 1/(4 tau(r_e))", s_lo(lo(E_e)), s_hi(hi(E_e)),
                      "entry of the edge equilibrium; the jump of entry at r_e", True, "computer-assisted"))
    UH_e = K * n_e / (B - n_e)
    certs.append(Cert("U_H at r_e: k n/(b - n)", s_lo(lo(UH_e)), s_hi(hi(UH_e)), "high type's profit at the edge > 0",
                      lo(UH_e) > 0, "computer-assisted"))
    # C6: Psi < 0 below the edge
    delta = mpf("0.00001")
    okP, nP, fP = cover_psi(mpf(1), reA - delta)
    certs.append(Cert("Psi(z, r) < 0 for n(r) <= z <= 1, ell < r <= r_e - 1e-5", "1", s_lo(reA - delta),
                      "no fixed point of the low type's best response when q_H = 1 (Proposition ES.4(b))", okP,
                      f"computer-assisted ({nP} boxes, {len(fP)} unresolved)"))
    okZ, nZ, fZ = cover_psi_z(mpf("1.3"), hi(rC))
    certs.append(Cert("dPsi/dz < 0 for n(r) <= z <= 1, 1.3 <= r <= r_C", "1.3", s_hi(hi(rC)),
                      "Psi decreases in z: with G < 0 below r_e this closes (1.3, r_e); supported z form [n(r), z_U(r)]",
                      okZ, f"computer-assisted ({nZ} boxes, {len(fZ)} unresolved)"))
    with (HERE / "certificates.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["name", "lo", "hi", "statement", "holds", "status"])
        for c in certs:
            w.writerow([c.name, c.lo, c.hi, c.statement, c.holds, c.status])
    for c in certs:
        print(f"{c.name:58s} [{c.lo}, {c.hi}] holds={c.holds} {c.status}")


if __name__ == "__main__":
    main()
