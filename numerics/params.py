"""Parameter records and input declarations (Online Appendix C.0).

Every declared input is stored as its exact decimal string. Float views are derived
on demand; certificate code (Appendix B) parses the strings directly into interval
arithmetic without a binary intermediate.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from decimal import Decimal
from enum import Enum
from typing import Mapping


class Noise(str, Enum):
    LAPLACE = "Laplace"
    LOGISTIC = "logistic"


class CostLaw(str, Enum):
    ATOMS = "atoms"
    UNIFORM_MIXTURE = "uniform_mixture"


@dataclass(frozen=True)
class Primitives:
    """Exact decimal primitives (h, ell, p, rho, c_L, c_H, b, k) plus laws."""

    h: str
    ell: str
    p: str
    rho: str
    c_L: str
    c_H: str
    b: str
    k: str
    noise: Noise = Noise.LAPLACE
    cost_law: CostLaw = CostLaw.ATOMS
    cost_halfwidth: str = "0"
    fundamental_prior_H: str = "0.5"
    parameter_set: str = "base"

    # float views -----------------------------------------------------------
    @property
    def fh(self) -> float:
        return float(Decimal(self.h))

    @property
    def fell(self) -> float:
        return float(Decimal(self.ell))

    @property
    def fp(self) -> float:
        return float(Decimal(self.p))

    @property
    def frho(self) -> float:
        return float(Decimal(self.rho))

    @property
    def fc_L(self) -> float:
        return float(Decimal(self.c_L))

    @property
    def fc_H(self) -> float:
        return float(Decimal(self.c_H))

    @property
    def fb(self) -> float:
        return float(Decimal(self.b))

    @property
    def fk(self) -> float:
        return float(Decimal(self.k))

    @property
    def feps_C(self) -> float:
        return float(Decimal(self.cost_halfwidth))

    def with_(self, **kw) -> "Primitives":
        return replace(self, **kw)

    def columns(self) -> Mapping[str, str]:
        """Parameter columns in the C.0 transliteration."""
        return {
            "h": self.h, "ell": self.ell, "p": self.p, "rho": self.rho,
            "c_L": self.c_L, "c_H": self.c_H, "b": self.b, "k": self.k,
        }


@dataclass(frozen=True)
class Controls:
    """Numerical controls declaration (C.0)."""

    quadrature_absolute_target: float = 1e-11
    quadrature_relative_target: float = 1e-11
    probability_acceptance: float = 1e-8
    price_identity_acceptance: float = 1e-8
    entry_optimality_acceptance: float = 1e-8
    deviation_gain_acceptance: float = 1e-7
    independent_formula_acceptance: float = 1e-9
    initial_order_intervals: int = 400
    refined_order_intervals: int = 800
    initial_flow_halfwidth: float = 40.0
    interval_decimal_precision: int = 50
    certificate_derivative_intervals: int = 200
    certificate_refined_intervals: int = 400
    probability_display_decimals: int = 6

    def tightened(self) -> "Controls":
        """Refinement pass: double order resolution, tighten integration targets by 10."""
        return replace(
            self,
            quadrature_absolute_target=self.quadrature_absolute_target / 10,
            quadrature_relative_target=self.quadrature_relative_target / 10,
            initial_order_intervals=self.refined_order_intervals,
            refined_order_intervals=2 * self.refined_order_intervals,
        )

    def as_dict(self) -> dict:
        return dict(self.__dict__)


CONTROLS = Controls()

# --- Declarations (C.0) -------------------------------------------------------
BENCHMARK = Primitives(
    h="10", ell="1", p="0.5", rho="0.25", c_L="1", c_H="6", b="2", k="0.02",
    parameter_set="base",
)
BENCHMARK_STRENGTHS = {"r_weak": "1.2", "r_strong": "3", "r_collapse": "3.6"}
BENCHMARK_EXTRA = {
    "cost_halfwidth": "0.1",
    "value_band_halfwidth": "0.05",
    "binary_alternative_reserve": "1.01",
    "atomless_alternative_reserve": "1.1",
}

MODERATE = Primitives(
    h="2", ell="1", p="0.5", rho="0.25", c_L="0.3", c_H="0.89", b="2", k="0.002",
    parameter_set="moderate",
)
MODERATE_STRENGTHS = {"r_weak": "1.05", "r_strong": "1.5"}

SIGNAL = Primitives(
    h="10", ell="1", p="0.5", rho="0.85", c_L="1", c_H="7.14", b="2", k="0.015",
    parameter_set="signal",
)
SIGNAL_STRENGTHS = {"r_weak": "1.1", "r_strong": "2.3"}
SIGNAL_ACCURACIES = {"a": "0.70", "d": "0.75"}
SIGNAL_SWEEP_A = ["0.68", "0.69", "0.70", "0.71", "0.72"]
SIGNAL_SWEEP_D = ["0.73", "0.74", "0.75", "0.76", "0.77"]

CERTIFICATE_BRACKETS = [
    ("1.55", "0.46031618", "0.46031620"),
    ("1.60", "0.70747537", "0.70747539"),
    ("1.65", "0.90333198", "0.90333201"),
]

CORRESPONDENCE_MESH = ("1.005", "3.800", "0.005")
CORRESPONDENCE_OFFSETS = ("0.0001", "0.001")


def decimal_range(start: str, stop: str, step: str) -> list[str]:
    """Exact decimal arithmetic progression, inclusive of stop when reached exactly."""
    s, e, d = Decimal(start), Decimal(stop), Decimal(step)
    out = []
    x = s
    while x <= e:
        out.append(str(x.normalize()) if x != x.to_integral() else str(x.quantize(Decimal(1))))
        x += d
    return out
