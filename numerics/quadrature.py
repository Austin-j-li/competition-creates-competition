"""Segment-wise Gauss–Legendre integration over the full line with explicit tail handling."""
from __future__ import annotations

import numpy as np

from .noise import dpdf, pdf, survival, tail_bound
from .params import Noise

_GL_CACHE: dict[int, tuple[np.ndarray, np.ndarray]] = {}


def gl_nodes(n: int) -> tuple[np.ndarray, np.ndarray]:
    if n not in _GL_CACHE:
        _GL_CACHE[n] = np.polynomial.legendre.leggauss(n)
    return _GL_CACHE[n]


def segments(points: list[float], max_len: float) -> list[tuple[float, float]]:
    pts = sorted(set(points))
    out = []
    for a, b in zip(pts[:-1], pts[1:]):
        if b - a <= 1e-15:
            continue
        n = max(1, int(np.ceil((b - a) / max_len)))
        edges = np.linspace(a, b, n + 1)
        out.extend(zip(edges[:-1], edges[1:]))
    return out


def integrate_segments(fun, segs: list[tuple[float, float]], n: int) -> float:
    xg, wg = gl_nodes(n)
    a = np.array([s[0] for s in segs])
    b = np.array([s[1] for s in segs])
    half = 0.5 * (b - a)
    mid = 0.5 * (a + b)
    x = mid[:, None] + half[:, None] * xg[None, :]
    vals = fun(x.ravel()).reshape(x.shape)
    return float(np.sum(half[:, None] * wg[None, :] * vals))


def convolve_full_line(noise: Noise, b: float, kernel_kind: str, kmult: float, A, breakpoints: list[float],
                       center: float, hull: tuple[float, float], A_const_left: float | None,
                       A_const_right: float | None, max_len: float | None = None, n: int = 48,
                       tail_target: float = 1e-14, A_bar: float = 1.0) -> tuple[float, float, float]:
    """Return (value, quadrature_error_estimate, tail_bound) of  int kmult*K(x - center) A(x) dx.

    `kernel_kind` is "pdf" (K = f) or "dpdf" (K = f'). `A` is vectorized in x. On the exterior
    of the extended hull the residual is constant when the constants are supplied (Laplace: the
    posterior is constant outside the support hull), and the tails are integrated analytically.
    Otherwise the exterior is integrated numerically out to a distance at which the C.0 tail
    bound falls below `tail_target`, and that bound is returned.
    """
    max_len = b if max_len is None else max_len
    kernel = (lambda z: pdf(noise, z, b)) if kernel_kind == "pdf" else (lambda z: dpdf(noise, z, b))
    lo = min(hull[0], center)
    hi = max(hull[1], center)
    pts = [lo, hi, center, *[p for p in breakpoints if lo <= p <= hi]]
    segs = segments(pts, max_len)
    f_int = lambda x: kmult * kernel(x - center) * A(x)
    val = integrate_segments(f_int, segs, n)
    err = abs(val - integrate_segments(f_int, segs, n // 2))
    tb = 0.0
    if A_const_left is not None and A_const_right is not None and noise == Noise.LAPLACE:
        val += kmult * A_const_left * _laplace_kernel_mass(b, kernel_kind, -np.inf, lo - center)
        val += kmult * A_const_right * _laplace_kernel_mass(b, kernel_kind, hi - center, np.inf)
    else:
        T = max(hi - lo, 1.0) + b * np.log(max(A_bar, 1e-300) / tail_target + 1.0) + 1.0
        ext_segs = segments([lo - T, lo], max_len) + segments([hi, hi + T], max_len)
        v2 = integrate_segments(f_int, ext_segs, n)
        err += abs(v2 - integrate_segments(f_int, ext_segs, n // 2))
        val += v2
        tb = abs(kmult) * tail_bound(noise, T, b, A_bar)
    return val, err, tb


def _laplace_kernel_mass(b: float, kernel_kind: str, z0: float, z1: float) -> float:
    """Exact integral of f or f' over [z0, z1] (Laplace), endpoints may be infinite."""
    if kernel_kind == "pdf":
        s0 = 1.0 if z0 == -np.inf else float(survival(Noise.LAPLACE, z0, b))
        s1 = 0.0 if z1 == np.inf else float(survival(Noise.LAPLACE, z1, b))
        return s0 - s1
    fz = lambda z: 0.0 if not np.isfinite(z) else float(np.exp(-abs(z) / b) / (2 * b))
    return fz(z1) - fz(z0)
