"""Print W1 economic calculations; no assertions or repository mutations."""
from fractions import Fraction as Q
from math import exp, sqrt

h, ell, p, rho, c_H, k = map(Q, ['10', '1', '0.5', '0.25', '6', '0.02'])
r0, r2 = Q(6, 5), Q(18, 5)
d = h - ell
u = exp(1) - 1
beta = Q('0.294655')
lam = u * float(beta) / (1 + u * float(beta))
b = (1 - lam) * float(beta)
M = (1 + u) / (2 + u)

def uniform(r):
    delta = (r - ell) ** 2 / (2 * r)
    gamma = d - delta
    g_H = h - r / 2 - p * p / (2 * r)
    g_L = (ell * ell - p * p) / (2 * r)
    tau = (c_H - g_L) / gamma
    J = delta * (1 - tau)
    delta_prime = (r * r - ell * ell) / (2 * r * r)
    profit_loss = (r * r - p * p) / (2 * r * r)
    J_prime = (d * (g_H - c_H) * delta_prime - delta * gamma * profit_loss) / gamma ** 2
    return delta, gamma, g_H, g_L, tau, J, J_prime

L = (r0 * r0 - p * p) / (r0 * r0 - ell * ell)
k_max = d * rho * rho / (4 * L)
print('bounded profit loss:', 'L', L, float(L), 'k_max', k_max, float(k_max), 'margin', float(k_max - k))
print('uniform cost coverage:', float(h - r2 - c_H))
print('point-class relaxed cost cap:', float(h - r2 + ell / 2 - p * p / (2 * r2)))
print('slot lambda,b,M:', lam, b, M)
for r in [r0, Q('1.4'), Q('1.5'), Q(2), r2]:
    print('uniform r; Delta,gamma,gH,gL,tau,J,Jprime:', float(r), *[float(v) for v in uniform(r)])
lower, upper = float(r0), float(r2)
for _ in range(100):
    middle = (lower + upper) / 2
    if uniform(middle)[5] < k:
        lower = middle
    else:
        upper = middle
r_A = (lower + upper) / 2
delta_N = float(2 * k / rho)
r_N = 1 + delta_N + sqrt(delta_N ** 2 + 2 * delta_N)
delta_F = float(k) / (1 - M)
r_F = 1 + delta_F + sqrt(delta_F ** 2 + 2 * delta_F)
print('r_A,r_F,r_N:', r_A, r_F, r_N)
for r in [r_A, r_F, r_N]:
    delta, gamma, g_H, g_L, tau, J, J_prime = uniform(r)
    entry = float(rho) + (1 - float(rho)) * min(b * float(delta) / (2 * float(k)), b + lam / 2)
    print('benchmark boundary r,tau,J,entry:', r, float(tau), float(J), entry)
tau_A = float(uniform(r_A)[4])
pi_lo = tau_A / (tau_A + (1 - tau_A) * exp(1))
print('prior start pi_lo,1-rho-tau_A:', pi_lo, 1 - float(rho) - tau_A)
print('slot-specific start margins:', 1 - tau_A - float(rho) * max(pi_lo, 1 - pi_lo), 1 - tau_A - float(rho) * tau_A)

print('known location example: z,Delta,tau,J,no-trade return')
for z in [Q(7), Q('7.5')]:
    delta, gamma = z - ell, h - z
    tau = Q(2) / gamma
    print(*[float(v) for v in [z, delta, tau, delta * (1 - tau), rho * delta / 2]])

def mixture(m_low, m_high):
    delta = Q('0.1') * (m_high - ell)
    g_L = Q('0.9') * (ell - m_low)
    gamma = d - delta
    g_H = gamma + g_L
    tau = (c_H - g_L) / gamma
    return delta, g_L, g_H, tau, delta * (1 - tau), rho * delta / 2

print('mixture stage; Delta,gL,gH,tau,J,no-trade return')
for label, m_low, m_high in [('start', Q('.6'), Q('1.57')), ('middle', Q('.98'), Q('1.57')), ('end', Q('.98'), Q('1.8'))]:
    print(label, *[float(v) for v in mixture(m_low, m_high)])
delta0 = Q('.057')
gL_critical = c_H - (d - delta0) + k * (d - delta0) / delta0
down = (Q('.36') - gL_critical) / Q('.342')
linear = float(d + Q('.018') - c_H + k)
delta_back = (linear - sqrt(linear ** 2 - 4 * float(k * d))) / 2
back = 1 + (delta_back - float(delta0)) / float(Q('.08') - delta0)
print('disconnected set endpoints:', float(down), back, 'return spread:', delta_back)
print('strictly increasing spread perturbation at middle:', *[float(v) for v in mixture(Q('.98'), Q('1.571'))])

print('spread classes: G_L uniform[.75,1.1], G_H uniform[9,11]')
v_L, v_H = Q('.925'), Q(10)
m2_L = (Q('.75') ** 2 + Q('.75') * Q('1.1') + Q('1.1') ** 2) / 3
gap = v_H - v_L
for r in [r0, Q(2), r2]:
    delta = r / 2 - v_L + m2_L / (2 * r)
    gamma = gap - delta
    g_H = v_H - r / 2 - p * p / (2 * r)
    g_L = (m2_L - p * p) / (2 * r)
    tau = (c_H - g_L) / gamma
    delta_prime = (r * r - m2_L) / (2 * r * r)
    profit_loss = (r * r - p * p) / (2 * r * r)
    J_prime = (gap * (g_H - c_H) * delta_prime - delta * gamma * profit_loss) / gamma ** 2
    print('r,Delta,tau,J,Jprime:', *[float(v) for v in [r, delta, tau, delta * (1 - tau), J_prime]])

r_extended = Q('1.01')
L_extended = (r_extended ** 2 - p ** 2) / (r_extended ** 2 - ell ** 2)
print('nonnecessity: r0,L,k_max:', float(r_extended), float(L_extended), float(d * rho ** 2 / (4 * L_extended)))
