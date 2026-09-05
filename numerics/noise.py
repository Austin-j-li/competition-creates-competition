"""Noise laws: Laplace and logistic at scale b (eq. 2, eq. 19, OA.23)."""
from __future__ import annotations

import numpy as np

from .params import Noise


def pdf(noise: Noise, z: np.ndarray, b: float) -> np.ndarray:
    z = np.asarray(z, dtype=float)
    if noise == Noise.LAPLACE:
        return np.exp(-np.abs(z) / b) / (2 * b)
    u = z / (2 * b)
    return 1.0 / (4 * b * np.cosh(u) ** 2)


def dpdf(noise: Noise, z: np.ndarray, b: float) -> np.ndarray:
    """Derivative of the density (Laplace: a.e., sign convention at 0 irrelevant)."""
    z = np.asarray(z, dtype=float)
    if noise == Noise.LAPLACE:
        return -np.sign(z) * pdf(noise, z, b) / b
    return -np.tanh(z / (2 * b)) * pdf(noise, z, b) / b


def survival(noise: Noise, z: np.ndarray, b: float) -> np.ndarray:
    """Pr(Z >= z)."""
    z = np.asarray(z, dtype=float)
    if noise == Noise.LAPLACE:
        return np.where(z < 0, 1 - 0.5 * np.exp(z / b), 0.5 * np.exp(-z / b))
    return 1.0 / (1.0 + np.exp(z / b))


def cdf(noise: Noise, z: np.ndarray, b: float) -> np.ndarray:
    return 1.0 - survival(noise, z, b)


def log_slope_bound(noise: Noise, b: float) -> float:
    """L with |f'| <= L f a.e. Both laws give 1/b."""
    return 1.0 / b


def variance(noise: Noise, b: float) -> float:
    if noise == Noise.LAPLACE:
        return 2 * b * b
    return b * b * np.pi ** 2 / 3


def tail_bound(noise: Noise, T: float, b: float, A_bar: float) -> float:
    """Per-unit gross-profit loss from truncating outside [-T, T] for |q| <= 1 (C.0)."""
    if noise == Noise.LAPLACE:
        return A_bar * np.exp(-(T - 1) / b)
    return 2 * A_bar / (1 + np.exp((T - 1) / b))


def posterior_bounds(b: float) -> tuple[float, float]:
    """m = (1 + e^{2/b})^{-1}, M = 1 - m (Lemma 1)."""
    m = 1.0 / (1.0 + np.exp(2.0 / b))
    return m, 1.0 - m
