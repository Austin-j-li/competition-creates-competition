"""Interval certificates for asymmetric equilibria (Online Appendix B; ported from the
collaborator's certify_asymmetric.py with predicates recorded instead of asserted).

Exact decimal strings enter mpmath interval arithmetic directly; no binary float intermediate.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import mpmath as mp

from .params import Controls, Primitives

iv = mp.iv


def I(x):
    return iv.mpf(x)


def lo(x) -> float:
    return float(x.a)


def hi(x) -> float:
    return float(x.b)


def mid(x) -> float:
    return (lo(x) + hi(x)) / 2


def atan(x):
    return iv.atan2(x, I(1))


def expit(x):
    return 1 / (1 + iv.exp(-x))


@dataclass
class CertificateRecord:
    r: str
    v_lower: str
    v_upper: str
    predicates: dict = field(default_factory=dict)
    values: dict = field(default_factory=dict)
    failures: list[str] = field(default_factory=list)

    @property
    def accepted(self) -> bool:
        return not self.failures and all(self.predicates.values())


class UnresolvedOrdering(Exception):
    pass


def primitives_iv(prim: Primitives, r):
    p, ell, h = I(prim.p), I(prim.ell), I(prim.h)
    return dict(t0=p * (1 - p / r), tH=r / 2 + p * p / (2 * r), tL=ell - (ell * ell - p * p) / (2 * r),
                gH=h - r / 2 - p * p / (2 * r), gL=(ell * ell - p * p) / (2 * r), Delta=(r - ell) ** 2 / (2 * r))


def objects(prim: Primitives, r, v, s, sgn: int, at_low_candidate: bool = False):
    """Enclose (U(s), U'(s), F(s), E) for the profile q_H = 1, q_L = -v, deviation magnitude s, sign sgn.

    `v` and `s` may be intervals. Raises UnresolvedOrdering when the cut ordering cannot be proved.
    """
    u = I(1)
    b, rho, k, cH = I(prim.b), I(prim.rho), I(prim.k), I(prim.c_H)
    P = primitives_iv(prim, r)
    D = P["Delta"]
    tau = (cH - P["gL"]) / (P["gH"] - P["gL"])
    xs = (b * iv.ln(tau / (1 - tau)) + u - v) / 2
    mu_hi = expit((u + v) / b)
    mu_lo = 1 - mu_hi
    if not (lo(tau) > 0.5 and hi(tau) < lo(mu_hi)):
        raise UnresolvedOrdering("threshold ordering 1/2 < tau < M_v not proved")
    center = sgn * s
    c = (u - v) / 2
    cuts = [("left", -v), ("entry", xs), ("right", u)]
    if not at_low_candidate and not (sgn == 1 and lo(s) == 1.0 and hi(s) == 1.0):
        cuts.append(("center", center))
    cuts.sort(key=lambda item: mid(item[1]))
    for (_, x), (_, y) in zip(cuts[:-1], cuts[1:]):
        if not hi(x) < lo(y):
            raise UnresolvedOrdering(f"cut ordering not proved: {x} vs {y}")
    points = [(None, None)] + cuts + [(None, None)]
    F = I(0)
    Fp = I(0)
    for j in range(len(points) - 1):
        left, right = points[j][1], points[j + 1][1]
        if left is None:
            test = mid(right) - 10
        elif right is None:
            test = mid(left) + 10
        else:
            test = (mid(left) + mid(right)) / 2
        left_of_center = test < mid(center)
        e = rho if test < mid(xs) else I(1)
        if test < mid(-v):
            coeff = (1 - mu_lo) if sgn == 1 else mu_lo
            interior = False
        elif test > 1.0:
            coeff = (1 - mu_hi) if sgn == 1 else mu_hi
            interior = False
        else:
            interior = True
        if not interior:
            if left_of_center:
                val = I(".5") * ((iv.exp((right - center) / b) if right is not None else I(0))
                                 - (iv.exp((left - center) / b) if left is not None else I(0)))
            else:
                val = I(".5") * ((iv.exp(-(left - center) / b) if left is not None else I(0))
                                 - (iv.exp(-(right - center) / b) if right is not None else I(0)))
            part = e * D * coeff * val
        else:
            tL = iv.exp((left - c) / b)
            tR = iv.exp((right - c) / b)
            if sgn == 1 and left_of_center:
                primitive, fac = (lambda t: atan(t)), iv.exp((c - center) / b) / 2
            elif sgn == 1 and not left_of_center:
                primitive, fac = (lambda t: -1 / t - atan(t)), iv.exp((center - c) / b) / 2
            elif sgn == -1 and left_of_center:
                primitive, fac = (lambda t: t - atan(t)), iv.exp((c - center) / b) / 2
            else:
                primitive, fac = (lambda t: atan(t)), iv.exp((center - c) / b) / 2
            part = e * D * fac * (primitive(tR) - primitive(tL))
        F += part
        Fp += sgn * (-1 if left_of_center else 1) * part / b
    U = s * (F - k)
    Up = F + s * Fp - k
    alphaH = 1 - iv.exp((xs - u) / b) / 2
    alphaL = iv.exp(-(xs + v) / b) / 2
    E = rho + (1 - rho) * (alphaH + alphaL) / 2
    return U, Up, F, E


def certify(prim: Primitives, r_s: str, vl_s: str, vr_s: str, controls: Controls, n: int | None = None) -> CertificateRecord:
    iv.dps = controls.interval_decimal_precision
    n = controls.certificate_derivative_intervals if n is None else n
    rec = CertificateRecord(r_s, vl_s, vr_s)
    r, vl, vr = I(r_s), I(vl_s), I(vr_s)
    v = iv.mpf([vl_s, vr_s])
    P = primitives_iv(prim, r)
    try:
        psi_l = objects(prim, r, vl, vl, -1, True)[1]
        psi_r = objects(prim, r, vr, vr, -1, True)[1]
    except UnresolvedOrdering as ex:
        rec.failures.append(f"endpoint evaluation: {ex}")
        return rec
    rec.values.update(Psi_left=psi_l, Psi_right=psi_r)
    rec.predicates["psi_left_positive"] = lo(psi_l) > 0
    rec.predicates["psi_right_negative"] = hi(psi_r) < 0
    # support and cost predicates (Lemma 1 bound m uses the global posterior bound)
    global_m = 1 / (1 + iv.exp(2 / I(prim.b)))
    low_cost_margin = P["gL"] + global_m * (P["gH"] - P["gL"]) - I(prim.c_L)
    high_prior_margin = I(prim.c_H) - (P["gH"] + P["gL"]) / 2
    pooling_margin = I(prim.k) - I(prim.rho) * P["Delta"] / 2
    rec.values.update(low_cost_margin=low_cost_margin, high_prior_margin=high_prior_margin, pooling_margin=pooling_margin)
    rec.predicates["support"] = lo(I(prim.p)) < lo(I(prim.ell)) < lo(r) and hi(r) < lo(I(prim.h))
    rec.predicates["low_cost_floor"] = lo(low_cost_margin) > 0
    rec.predicates["high_cost_prior_exclusion"] = lo(high_prior_margin) > 0
    rec.predicates["pooling_exists_margin"] = lo(pooling_margin) > 0
    # threshold ordering throughout the bracket and the uniform high-type cover
    b = I(prim.b)
    lip = 2 * P["Delta"] / b + P["Delta"] / (b * b)
    vals = []
    try:
        for j in range(n + 1):
            s = I(j) / I(n)
            vals.append(objects(prim, r, v, s, 1)[1])
        rec.predicates["threshold_ordering"] = True
    except UnresolvedOrdering as ex:
        rec.failures.append(f"high-type cover: {ex}")
        rec.predicates["threshold_ordering"] = False
        return rec
    min_lower = min(x.a for x in vals)
    gamma = min_lower - lip / (2 * n)
    rec.values.update(Gamma_H=gamma, L_U=lip, mesh_min_lower=min_lower, mesh_intervals=n)
    rec.predicates["gamma_H_positive"] = lo(gamma) > 0
    # entry enclosure over the bracket and payoffs
    try:
        U_root, _, _, E = objects(prim, r, v, v, -1, True)
        U_high = objects(prim, r, v, I(1), 1)[0]
    except UnresolvedOrdering as ex:
        rec.failures.append(f"entry enclosure: {ex}")
        return rec
    rec.values.update(E=E, U_low=U_root, U_high=U_high)
    rec.predicates["low_type_concavity"] = lo(b) > 0.5  # OA.60 requires b > 1/2 (structural, holds for b = 2)
    return rec


def outward(x, digits: int, side: str) -> str:
    """Decimal string rounded outward: 'lower' rounds down, 'upper' rounds up."""
    from decimal import ROUND_CEILING, ROUND_FLOOR, Decimal
    val = mp.mpf(x.a) if side == "lower" else mp.mpf(x.b)
    d = Decimal(mp.nstr(val, 60, strip_zeros=False))
    q = Decimal(1).scaleb(-digits)
    return format(d.quantize(q, rounding=ROUND_FLOOR if side == "lower" else ROUND_CEILING), "f")


def endpoint_str(x, side: str, digits: int = 60) -> str:
    """Exact binary endpoint converted to a decimal string with outward directed rounding."""
    from decimal import Context, ROUND_CEILING, ROUND_FLOOR, Decimal
    lo_t, hi_t = x._mpi_  # raw endpoint tuples (sign, man, exp, bc)
    sign, man, exp, _ = lo_t if side == "lower" else hi_t
    if man == 0:
        return "0"
    from decimal import localcontext
    with localcontext() as big:
        big.prec = 2000  # exact: a 170-bit mantissa times a power of two needs far fewer digits
        exact = Decimal(int(man)) * (Decimal(2) ** int(exp))
        if sign:
            exact = -exact
    ctx = Context(prec=digits, rounding=ROUND_FLOOR if side == "lower" else ROUND_CEILING)
    return format(ctx.plus(exact), "f")
