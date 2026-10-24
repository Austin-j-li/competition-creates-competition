from fractions import Fraction as F
from math import factorial

p, ell, h, rho, k = F(1, 2), F(1), F(10), F(1, 4), F(1, 50)
u = F(82, 59)
M = (1 + u) / (2 + u)
m = 1 - M

def proceeds(r):
    low = ell - (ell**2 - p**2) / (2 * r)
    high = r / 2 + p**2 / (2 * r)
    return low, high

print('Lower boundary: u =', u, 'M =', M, 'm =', m)
for r in (F(6, 5), F(3), F(18, 5)):
    low, high = proceeds(r)
    spread = high - low
    print('r =', r, 't_L =', low, 't_H =', high, 'Delta =', spread)
    print('Delta - k =', spread - k)
    print('rho*m*Delta - k =', rho * m * spread - k)
    print('B(M) - c_H =', (ell - low) + M * ((h - high) - (ell - low)) - 6)
    print('full-order purchase profit with entry one =', spread * (1 - M) - k)

e_lo = sum((F(1, factorial(n)) for n in range(111)), F(0))
e_hi = e_lo + F(112, 111 * factorial(111))
beta = F(294655, 1000000)

def lam(e):
    return (e - 1) * beta / (1 + (e - 1) * beta)

def decimal_bound(x, places, upper=False):
    scale = 10**places
    v = x.numerator * scale // x.denominator
    if upper and F(v, scale) < x:
        v += 1
    return str(v // scale) + '.' + str(v % scale).zfill(places)

lambda_lo, lambda_hi = lam(e_lo), lam(e_hi)
print('Calibration B lambda enclosure =', decimal_bound(lambda_lo, 18), decimal_bound(lambda_hi, 18, True))
low, high = proceeds(F(3))
spread = high - low
margin_lo = rho * spread / (1 + e_hi) - k
margin_hi = rho * spread / (1 + e_lo) - k
print('Low-class full-sale margin at r=3 =', decimal_bound(margin_lo, 18), decimal_bound(margin_hi, 18, True))
print('Target proceeds at r=3 =', low)
print('Target proceeds minus sale rate enclosure =', decimal_bound(low - lambda_hi, 18), decimal_bound(low - lambda_lo, 18, True))
