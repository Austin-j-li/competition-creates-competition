from fractions import Fraction as Q

# Direct integration of the auction rent over a uniform incumbent law.
def uniform_rent(v, lo, hi, p):
    value = Q(0)
    if lo < min(hi, p):
        value += (min(hi, p) - lo) * max(v - p, Q(0))
    left, right = max(lo, p), min(hi, v)
    if right > left:
        value += v * (right - left) - (right**2 - left**2) / 2
    return value / (hi - lo)

p = Q(1, 2)
mean_rent = lambda lo, hi: sum(uniform_rent(v, lo, hi, p) for v in (Q(12), Q(11))) / 2
low, high0, high1 = mean_rent(Q(0), Q(1)), mean_rent(Q(8), Q(9)), mean_rent(Q(9), Q(10))
rho, cost = Q(1, 4), Q(6)
entry = lambda rent: rho + (1-rho) * int(rent >= cost)
print('Fixed information: conditional profits economy 0:', low, high0)
print('Fixed information: conditional profit economy 1:', (low + high1) / 2)
print('Fixed information: entry economy 0, economy 1:', (entry(low)+entry(high0))/2, entry((low+high1)/2))
print('Fixed information: unconditional profits:', (low+high0)/2, (low+high1)/2)

h, ell = Q(10), Q(1)
r0, r1, rho, cost, k = Q(11,10), Q(23,10), Q(17,20), Q(357,50), Q(3,200)
a, d, lam, beta = Q(7,10), Q(3,4), Q(1,3), Q(3,10)
b = (1-lam)*beta
M, m = (b+lam)/(2*b+lam), b/(2*b+lam)
mu = (1-a)+(2*a-1)*M
phi_plus = d*mu/(d*mu+(1-d)*(1-mu))
phi_minus = (1-d)*mu/((1-d)*mu+d*(1-mu))

def B(r, belief):
    return belief*uniform_rent(h,Q(0),r,p)+(1-belief)*uniform_rent(ell,Q(0),r,p)

def delta(r):
    return (r-ell)**2/(2*r)

def wH(r):
    return (r*r+p*p)/(2*r)-p*(1-p/r)

Dplus = delta(r0)+(1-rho)*(2*d-1)*wH(r0)
print('Private signals: b, M, m, mu_plus, phi_plus, phi_minus:', b,M,m,mu,phi_plus,phi_minus)
for name, value in (
    ('private', cost-B(r0,d)),
    ('joint', B(r1,phi_plus)-cost),
    ('weak trade', k-(2*a-1)*Dplus),
    ('strong trade', (2*a-1)*rho*m*delta(r1)-k),
    ('other pair', cost-B(r1,phi_minus)),
):
    print('Private signals margin:', name, value)

# Above the sale threshold, both classes prepare only at zero cost.
rho, k, r = Q(1,4), Q(1,50), Q(3)
coefficient = (2*a-1)*rho*delta(r)
rate_over_b = coefficient/k-2
nu = 1/(2+rate_over_b)
print('Sale payoff: coefficient, t/b, gross, net:', coefficient, rate_over_b, coefficient*nu, coefficient*nu-k)
print('Sale payoff: threshold gap in t/b:', rate_over_b-Q(15,19))

# The spread interval lies above r, so the rent kernel is affine there.
lo, hi = Q(199,20), Q(201,20)
point = uniform_rent(Q(10),Q(0),r,p)
spread = (uniform_rent(lo,Q(0),r,p)+uniform_rent(hi,Q(0),r,p))/2
print('Dispersion: point-class rent, spread-class rent:', point, spread)
