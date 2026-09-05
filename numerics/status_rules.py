"""Status vocabulary and classification rules shared by the correspondence and reserve exercises (S3-10, S3-13).

Vocabulary (paper): analytical, computer-assisted, numerical diagnostic, open. Two further outcomes are
needed for search bookkeeping and are never confused with the paper's result labels:

- ``rejected``: a candidate was formed and validated, and validation produced a deviation or identity
  witness (the witness is kept in ``unresolved_reason``).
- ``no candidate``: the search path terminated without forming a candidate (a sign change of Psi across
  a discontinuity, or a local |Psi| minimum bounded away from zero by more than the numerical resolution).

Tangency rule. A local minimum of |Psi| without a sign change is compared with the numerical resolution
of Psi at the minimiser: ten times the quadrature error estimate plus the tail bound of the derivative
convolution, floored at ``TANGENCY_RESOLUTION_FLOOR`` (which also covers the minimiser tolerance). A
minimum within the resolution is an unresolved tangency (``open``); a minimum above it is a resolved
non-root (``no candidate``). The same function is meant to be called by C.6 (see the deferred patch).
"""
from __future__ import annotations

from dataclasses import dataclass

from .deviations import Convolution

ANALYTICAL = "analytical"
COMPUTER_ASSISTED = "computer-assisted"
NUMERICAL_DIAGNOSTIC = "numerical diagnostic"
OPEN = "open"
REJECTED = "rejected"
NO_CANDIDATE = "no candidate"

TANGENCY_RESOLUTION_FLOOR = 1e-8   # covers the bounded-minimiser tolerance (xatol 1e-10) times an O(1) slope of Psi
TANGENCY_QUADRATURE_FACTOR = 10.0


@dataclass(frozen=True)
class TangencyVerdict:
    status: str          # open | no candidate
    resolution: float
    reason: str


def tangency_resolution(psi: Convolution) -> float:
    return max(TANGENCY_RESOLUTION_FLOOR, TANGENCY_QUADRATURE_FACTOR * (abs(psi.error) + abs(psi.tail_bound)))


def classify_tangency(residual: float, psi_at_min: Convolution) -> TangencyVerdict:
    """Classify a local |Psi| minimum that did not change sign and whose candidate failed validation."""
    res = tangency_resolution(psi_at_min)
    if residual <= res:
        return TangencyVerdict(OPEN, res, f"local |Psi| minimum {residual:.3e} within the numerical resolution {res:.1e}: unresolved tangency")
    return TangencyVerdict(NO_CANDIDATE, res,
                           f"local |Psi| minimum {residual:.3e} exceeds the numerical resolution {res:.1e}: resolved non-root, no candidate formed")


def pooling_existence_label(coefficient_margin: float, in_domain: bool, accepted: bool) -> tuple[str, str]:
    """Pooling existence from the sign of k - e0 Delta_T / 2 (the linear coefficient that decides it), not from acceptance.

    Returns (existence_status, note). A disagreement between the analytical sign and validation is recorded as
    open with the reason, never silently resolved either way.
    """
    if coefficient_margin >= 0 and accepted:
        if in_domain:
            return ANALYTICAL, "pooling coefficient k - e0 Delta_T/2 >= 0 within the maintained domain"
        return f"{ANALYTICAL} (outside maintained domain; prior entry rule evaluated)", "pooling coefficient k - e0 Delta_T/2 >= 0 with the actual prior entry e0"
    if coefficient_margin < 0 and not accepted:
        return REJECTED, f"pooling coefficient k - e0 Delta_T/2 = {coefficient_margin:.3e} < 0: a small order is profitable"
    if coefficient_margin >= 0 and not accepted:
        return OPEN, f"pooling coefficient nonnegative ({coefficient_margin:.3e}) but validation breached"
    return OPEN, f"pooling coefficient negative ({coefficient_margin:.3e}) but no deviation witness found on the scan"
