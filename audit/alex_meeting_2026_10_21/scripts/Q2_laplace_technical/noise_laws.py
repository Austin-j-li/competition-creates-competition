"""Noise laws used in the Q2 technical memo (print-only support module).

Each law gives log-density, survival function, score psi = -(log f)',
the score bound L = sup|psi| (inf if unbounded) and the variance.
"""
from __future__ import annotations

import math

import numpy as np
from scipy import special, stats


class Laplace:
    def __init__(self, b: float):
        self.b = b
        self.name = f"Laplace(b={b:.4g})"
        self.L = 1.0 / b
        self.kinks = [0.0]

    def logpdf(self, z):
        z = np.asarray(z, dtype=float)
        return -np.abs(z) / self.b - math.log(2.0 * self.b)

    def sf(self, z):
        z = np.asarray(z, dtype=float)
        return np.where(z < 0, 1.0 - 0.5 * np.exp(np.minimum(z, 0.0) / self.b),
                        0.5 * np.exp(-np.maximum(z, 0.0) / self.b))

    def score(self, z):
        return np.sign(np.asarray(z, dtype=float)) / self.b

    def var(self):
        return 2.0 * self.b ** 2


class Logistic:
    def __init__(self, s: float):
        self.s = s
        self.name = f"Logistic(s={s:.4g})"
        self.L = 1.0 / s
        self.kinks = []

    def logpdf(self, z):
        a = np.abs(np.asarray(z, dtype=float)) / self.s
        return -a - math.log(self.s) - 2.0 * np.log1p(np.exp(-a))

    def sf(self, z):
        return special.expit(-np.asarray(z, dtype=float) / self.s)

    def score(self, z):
        return np.tanh(np.asarray(z, dtype=float) / (2.0 * self.s)) / self.s

    def var(self):
        return math.pi ** 2 * self.s ** 2 / 3.0


class HypSecant:
    """f(z) = sech(z/b) / (pi b); score tanh(z/b)/b, bound 1/b."""

    def __init__(self, b: float):
        self.b = b
        self.name = f"HypSecant(b={b:.4g})"
        self.L = 1.0 / b
        self.kinks = []

    def logpdf(self, z):
        a = np.abs(np.asarray(z, dtype=float)) / self.b
        logcosh = a + np.log1p(np.exp(-2.0 * a)) - math.log(2.0)
        return -math.log(math.pi * self.b) - logcosh

    def sf(self, z):
        z = np.asarray(z, dtype=float)
        return np.where(z >= 0, (2.0 / math.pi) * np.arctan(np.exp(-np.maximum(z, 0.0) / self.b)),
                        1.0 - (2.0 / math.pi) * np.arctan(np.exp(np.minimum(z, 0.0) / self.b)))

    def score(self, z):
        return np.tanh(np.asarray(z, dtype=float) / self.b) / self.b

    def var(self):
        return math.pi ** 2 * self.b ** 2 / 4.0


class StudentT:
    def __init__(self, nu: float, sigma: float):
        self.nu, self.sigma = nu, sigma
        self.name = f"Student-t(nu={nu:g}, sigma={sigma:.4g})"
        self.L = (nu + 1.0) / (2.0 * sigma * math.sqrt(nu))
        self.kinks = []

    @classmethod
    def with_bound(cls, nu: float, L: float):
        return cls(nu, (nu + 1.0) / (2.0 * L * math.sqrt(nu)))

    def logpdf(self, z):
        return stats.t.logpdf(np.asarray(z, dtype=float), self.nu, scale=self.sigma)

    def sf(self, z):
        return stats.t.sf(np.asarray(z, dtype=float), self.nu, scale=self.sigma)

    def score(self, z):
        z = np.asarray(z, dtype=float)
        return (self.nu + 1.0) * z / (self.nu * self.sigma ** 2 + z ** 2)

    def var(self):
        return self.sigma ** 2 * self.nu / (self.nu - 2.0) if self.nu > 2 else math.inf


class Gaussian:
    def __init__(self, sigma: float):
        self.sigma = sigma
        self.name = f"Gaussian(sigma={sigma:.4g})"
        self.L = math.inf
        self.kinks = []

    def logpdf(self, z):
        return stats.norm.logpdf(np.asarray(z, dtype=float), scale=self.sigma)

    def sf(self, z):
        return stats.norm.sf(np.asarray(z, dtype=float), scale=self.sigma)

    def score(self, z):
        return np.asarray(z, dtype=float) / self.sigma ** 2

    def var(self):
        return self.sigma ** 2


class NormalLaplace:
    """Laplace(b) + independent N(0, s^2): Kyle-type Gaussian noise plus a Laplace component."""

    def __init__(self, b: float, s: float):
        self.b, self.s = b, s
        self.name = f"Laplace(b={b:.4g})+N(0,{s:.4g}^2)"
        self.L = 1.0 / b
        self.kinks = []

    def _logT(self, z):
        z = np.asarray(z, dtype=float)
        b, s = self.b, self.s
        log_t1 = -z / b + special.log_ndtr(z / s - s / b)
        log_t2 = z / b + special.log_ndtr(-z / s - s / b)
        return log_t1, log_t2

    def logpdf(self, z):
        b, s = self.b, self.s
        log_t1, log_t2 = self._logT(z)
        return -math.log(2.0 * b) + s * s / (2.0 * b * b) + np.logaddexp(log_t1, log_t2)

    def sf(self, z):
        z = np.asarray(z, dtype=float)
        b, s = self.b, self.s
        c = s * s / (2.0 * b * b)
        term2 = 0.5 * np.exp(z / b + c + special.log_ndtr(-(z / s + s / b)))
        term3 = 0.5 * np.exp(-z / b + c + special.log_ndtr(z / s - s / b))
        return stats.norm.sf(z / s) - term2 + term3

    def score(self, z):
        log_t1, log_t2 = self._logT(z)
        return np.tanh((log_t1 - log_t2) / 2.0) / self.b

    def var(self):
        return 2.0 * self.b ** 2 + self.s ** 2
