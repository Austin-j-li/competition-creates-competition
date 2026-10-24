"""Textbook facts about the Laplace law, checked by quadrature and by characteristic functions.

Print-only. Run from the repository root:
    .venv/bin/python audit/alex_meeting_2026_10_21/scripts/Q2_laplace_technical/g3_textbook_facts.py

Laplace(b): density e^{-|z|/b}/(2b), characteristic function 1/(1 + b^2 t^2).
 1. E1 - E2, with E1, E2 independent exponential of mean b, is Laplace(b).
 2. sqrt(V) N, with N standard normal and V exponential of mean 2 b^2, is Laplace(b).
 3. W(T), Brownian motion at an independent exponential time T of mean 2 b^2, is Laplace(b).
 4. Logistic(s) is the independent sum of Laplace(s/n), n >= 1 (Euler product for sinh).
 5. The hyperbolic secant law sech(z/b)/(pi b) is the sum of Laplace(b/(2n-1)), n >= 1.
"""
from __future__ import annotations

import mpmath as mp

mp.mp.dps = 30
b = mp.mpf(2)


def laplace_pdf(z):
    return mp.e ** (-abs(z) / b) / (2 * b)


print("1. Difference of two exponentials (mean b each): density of E1 - E2 by convolution")
for z in (-3, -0.5, 0, 0.7, 2, 6):
    z = mp.mpf(z)
    lo = max(mp.mpf(0), z)
    conv = mp.quad(lambda u: (1 / b) * mp.e ** (-u / b) * (1 / b) * mp.e ** (-(u - z) / b), [lo, mp.inf])
    print(f"   z = {float(z):5.2f}: convolution {mp.nstr(conv, 15):>20s}   Laplace {mp.nstr(laplace_pdf(z), 15):>20s}")
print("   cf: E[e^{it(E1-E2)}] = 1/(1 - i b t) * 1/(1 + i b t) = 1/(1 + b^2 t^2)")
for t in (0.3, 1.0, 2.5):
    t = mp.mpf(t)
    lhs = 1 / (1 - 1j * b * t) / (1 + 1j * b * t)
    print(f"   t = {float(t):4.1f}: product {mp.nstr(lhs, 15)}   Laplace cf {mp.nstr(1 / (1 + b * b * t * t), 15)}")

print("\n2./3. Normal variance mixture, V ~ exponential with mean 2 b^2 (= Brownian motion at an exponential time)")
mean_v = 2 * b * b
for z in (0, 0.5, 1, 3, 8):
    z = mp.mpf(z)
    mix = mp.quad(lambda v: mp.npdf(z, 0, mp.sqrt(v)) * mp.e ** (-v / mean_v) / mean_v, [0, 1, 10, mp.inf])
    print(f"   z = {float(z):4.1f}: mixture density {mp.nstr(mix, 15):>20s}   Laplace {mp.nstr(laplace_pdf(z), 15):>20s}")
print("   cf: E[exp(-t^2 V / 2)] = 1/(1 + t^2 E[V] / 2) = 1/(1 + b^2 t^2) when E[V] = 2 b^2")

print("\n4. Logistic(s) = sum over n >= 1 of independent Laplace(s/n): pi s t / sinh(pi s t) = prod 1/(1 + s^2 t^2 / n^2)")
s = b
for t in (0.1, 0.4, 1.0):
    t = mp.mpf(t)
    lhs = mp.pi * s * t / mp.sinh(mp.pi * s * t)
    rhs = mp.nprod(lambda n: 1 / (1 + (s * t / n) ** 2), [1, mp.inf])
    print(f"   t = {float(t):4.1f}: logistic cf {mp.nstr(lhs, 18)}   product {mp.nstr(rhs, 18)}")
print("   Logistic(s) = Laplace(s) + W, W independent with density (3/(8s)) sech^4(z/(2s)); check of its cf:")
for t in (0.1, 0.4, 1.0):
    t = mp.mpf(t)
    kcf = mp.quad(lambda z: mp.cos(t * z) * 3 / (8 * s) * mp.sech(z / (2 * s)) ** 4, [-mp.inf, 0, mp.inf])
    target = (1 + s * s * t * t) * mp.pi * s * t / mp.sinh(mp.pi * s * t)
    print(f"   t = {float(t):4.1f}: cf of W {mp.nstr(kcf, 18)}   (1 + s^2 t^2) x logistic cf {mp.nstr(target, 18)}")

print("\n5. Hyperbolic secant sech(z/b)/(pi b): cf sech(pi b t / 2) = prod 1/(1 + b^2 t^2/(2n-1)^2)")
for t in (0.1, 0.4, 1.0):
    t = mp.mpf(t)
    cf = mp.quad(lambda z: mp.cos(t * z) * mp.sech(z / b) / (mp.pi * b), [-mp.inf, 0, mp.inf])
    prod = mp.nprod(lambda n: 1 / (1 + (b * t / (2 * n - 1)) ** 2), [1, mp.inf])
    print(f"   t = {float(t):4.1f}: cf by quadrature {mp.nstr(cf, 18)}   sech(pi b t/2) {mp.nstr(mp.sech(mp.pi * b * t / 2), 18)}   product {mp.nstr(prod, 18)}")
