#!/usr/bin/env python3
"""An economy with beta > 1/3 in which the zero order recruits although B(M(pi)) < c_H.

Point-mass classes h = 10 and ell = 1, reserve p = 1/2, incumbent uniform on [0, 3], zero preparation
cost with probability rho = 1/4 and c_H = 33/4 otherwise, trading cost k = 1/20, prior pi = 9/10, and the
slot lambda = 1/2, beta = 2/5. Class H abstains and class L sells. The program computes the posteriors,
entry, prices and order payoffs of the tuple that these orders and the threshold entry rule define,
in exact rational arithmetic. It prints; it checks nothing by assertion.

Usage: python3 o2_exclusion.py
"""

from fractions import Fraction as Fr

h, ell, p, r = Fr(10), Fr(1), Fr(1, 2), Fr(3)
rho, c_H, k, pi = Fr(1, 4), Fr(33, 4), Fr(1, 20), Fr(9, 10)
lam, beta = Fr(1, 2), Fr(2, 5)

b = (1 - lam) * beta
b0 = (1 - lam) * (1 - 2 * beta)
u = lam / b
eta = {-1: beta, 0: 1 - 2 * beta, 1: beta}

# Uniform incumbent on [0, r] with ell <= r <= h.
t0 = p * (1 - p / r)
tH = r / 2 + p * p / (2 * r)
tL = ell - (ell * ell - p * p) / (2 * r)
gH = h - r / 2 - p * p / (2 * r)
gL = (ell * ell - p * p) / (2 * r)
Delta = tH - tL
gamma = gH - gL
tau = (c_H - gL) / gamma


def B(mu):
    return gL + mu * gamma


def posterior(fH, fL):
    return pi * fH / (pi * fH + (1 - pi) * fL)


M = pi * (1 + u) / (pi * (1 + u) + 1 - pi)
m = pi / (pi + (1 - pi) * (1 + u))

sigma = {"H": {-1: Fr(0), 0: Fr(1), 1: Fr(0)}, "L": {-1: Fr(1), 0: Fr(0), 1: Fr(0)}}
f = {j: {x: (1 - lam) * eta[x] + lam * sigma[j][x] for x in (-1, 0, 1)} for j in "HL"}
mu = {x: posterior(f["H"][x], f["L"][x]) for x in (-1, 0, 1)}
ent = {x: (Fr(1) if mu[x] > tau else rho) for x in (-1, 0, 1)}
w = lambda z: tL - t0 + Delta * z
P = {x: t0 + ent[x] * w(mu[x]) for x in (-1, 0, 1)}
U = {
    ("H", 1): ent[1] * Delta * (1 - mu[1]) - k,
    ("H", -1): -ent[-1] * Delta * (1 - mu[-1]) - k,
    ("L", -1): ent[-1] * Delta * mu[-1] - k,
    ("L", 1): -ent[1] * Delta * mu[1] - k,
}

print("Slot: b = {}, b_0 = {}, u = lambda/b = {}; b_0 < b because beta > 1/3".format(b, b0, u))
print("Auction at r = 3: t_0 = {}, t_H = {}, t_L = {}, g_H = {}, g_L = {}".format(t0, tH, tL, gH, gL))
print("  Delta_T = {} = {:.6f}, g_H - g_L = {} = {:.6f}".format(Delta, float(Delta), gamma, float(gamma)))
print("  tau = {} = {:.6f}".format(tau, float(tau)))
print("Posterior bounds at the prior: m = {} = {:.6f}, M = {} = {:.6f}".format(m, float(m), M, float(M)))
print("  B(M) = {} = {:.6f}; c_H - B(M) = {} = {:.6f}".format(B(M), float(B(M)), c_H - B(M), float(c_H - B(M))))
print("Orders: class H abstains, class L sells")
for x in (-1, 0, 1):
    print("  order {:+d}: f_H = {}, f_L = {}, posterior = {} = {:.6f}, B = {:.6f}, entry = {}, price = {} = {:.6f}".format(
        x, f["H"][x], f["L"][x], mu[x], float(mu[x]), float(B(mu[x])), ent[x], P[x], float(P[x])))
print("  posterior after no order minus M: {} = {:.6f}".format(mu[0] - M, float(mu[0] - M)))
print("  posterior after no order minus tau: {} = {:.6f}".format(mu[0] - tau, float(mu[0] - tau)))
print("  tau minus M: {} = {:.6f}".format(tau - M, float(tau - M)))
print("Order payoffs against the tuple (abstention pays 0)")
for key, val in U.items():
    print("  class {}, order {:+d}: {} = {:.6f}".format(key[0], key[1], val, float(val)))
print("Trading-cost window for these orders: rho Delta_T (1 - pi) = {} < k = {} < rho Delta_T m = {}".format(
    rho * Delta * (1 - pi), k, rho * Delta * m))
print("Prices ordered as posteriors: P(-1) < P(1) < P(0):", P[-1] < P[1] < P[0])

print("Price-preimage posterior bounds for sets containing a nonzero order")
for group in ((-1,), (1,), (-1, 0), (0, 1), (-1, 1), (-1, 0, 1)):
    fH = sum((f["H"][x] for x in group), Fr(0))
    fL = sum((f["L"][x] for x in group), Fr(0))
    belief = posterior(fH, fL)
    print("  orders {}: posterior = {}, lower gap = {}, upper gap = {}".format(group, belief, belief-m, M-belief))
