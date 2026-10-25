from math import e, sqrt


def bisect_increasing(fun, left, right):
    for _ in range(100):
        mid = (left + right) / 2
        if fun(mid) < 0:
            left = mid
        else:
            right = mid
    return (left + right) / 2


def m(lam, beta):
    return beta * (1 - lam) / (2 * beta + (1 - 2 * beta) * lam)


def lam_e(tau, beta):
    return beta * (2 * tau - 1) / (beta + (1 - 2 * beta) * (1 - tau))


def lam_r(delta, a, k, beta):
    return bisect_increasing(lambda lam: 2 * a * lam - delta * m(lam, beta) + k, 0, 1)


def lam_recruit(delta, a, k, beta, rho):
    return bisect_increasing(
        lambda lam: 2 * a * lam - delta * m(lam, beta) + k
        - max(rho * delta * m(lam, beta) - k, 0), 0, 1
    )


def auction(r, c_h):
    g_l = 0.375 / r
    g_h = 10 - r / 2 - 0.125 / r
    delta = (r - 1) ** 2 / (2 * r)
    tau = (c_h - g_l) / (g_h - g_l)
    return delta, tau


def strength(delta):
    return 1 + delta + sqrt(delta * (delta + 2))


def branch_row(r, c_h, a, k, beta, rho, cap):
    delta, tau = auction(r, c_h)
    lam = min(cap, lam_recruit(delta, a, k, beta, rho))
    b = (1 - lam) * beta
    b0 = (1 - lam) * (1 - 2 * beta)
    if rho * delta <= 2 * k:
        sale = 0.0
    elif rho * delta * m(lam, beta) >= k:
        sale = 1.0
    else:
        sale = b / lam * (rho * delta / k - 2)
    mu_minus = b / (2 * b + lam * sale)
    mu_zero = b0 / (2 * b0 + lam * (1 - sale))
    mu_plus = 1 - m(lam, beta)
    u_h = delta * m(lam, beta) - k
    u_l = rho * delta * mu_minus - k
    value = (u_h + max(u_l, 0)) / 2
    entry = rho + (1 - rho) * (beta + (0.5 - beta) * lam)
    t0 = 0.5 * (1 - 0.5 / r)
    w_l = 1 - 0.375 / r - t0
    prices = (t0 + rho * (w_l + delta * mu_minus),
              t0 + rho * (w_l + delta * mu_zero),
              t0 + w_l + delta * mu_plus)
    return dict(r=r, delta=delta, tau=tau, lam=lam, sale=sale,
                mu_minus=mu_minus, mu_zero=mu_zero, mu_plus=mu_plus,
                recruitment_margin=mu_plus - tau, u_h=u_h, u_l=u_l,
                value_minus_a_lam=value - a * lam, entry=entry,
                price_minus=prices[0], price_zero=prices[1], price_plus=prices[2])


def show_row(row):
    print(' '.join(f'{key}={value:.10f}' for key, value in row.items()))


print('BENCHMARK')
beta = 0.294655
cap = (e - 1) * beta / (1 + (e - 1) * beta)
a, k, rho, c_h = 0.025, 0.02, 0.25, 6
delta_cap = (2 * a * cap + k) / m(cap, beta)
r_cap, r_n = strength(delta_cap), strength(2 * k / rho)
def phi(r):
    delta, tau = auction(r, c_h)
    return delta * (1 - tau) - k - 2 * a * lam_e(tau, beta)
r_start = bisect_increasing(phi, 1.2, 1.75)
lower_j = (11 / 72) * (19 / 55) - (9 / 56) * (16875 / 211288)
upper_lame_prime = beta * (16875 / 211288) / (beta + (1 - 2 * beta) * (19 / 55)) ** 2
print(f'beta={beta:.10f} cap={cap:.12f} m_cap={m(cap,beta):.12f}')
print(f'r_start={r_start:.12f} r_cap={r_cap:.12f} r_n={r_n:.12f} strength_margin={r_n-r_cap:.12f}')
print(f'cap_before_selling_margin={2*k*m(cap,beta)-rho*(2*a*cap+k):.12f}')
print(f'delta_cap={delta_cap:.12f} delta_n={2*k/rho:.12f} spread_margin={2*k/rho-delta_cap:.12f}')
print(f'cost_bound_no_selling={k/(2*cap)*(2*m(cap,beta)/rho-1):.12f}')
print(f'lower_j_prime={lower_j:.12f} upper_lame_prime={upper_lame_prime:.12f} a_mono={lower_j/(2*upper_lame_prime):.12f} lower_phi_prime={lower_j-2*a*upper_lame_prime:.12f}')
print(f'phi_left={phi(1.2):.12f} phi_right={phi(1.75):.12f} lambda_sell={k*(1-rho)/(2*a*rho):.12f}')
for r in (r_start, 1.55, 1.6, 1.65, r_cap):
    show_row(branch_row(r, c_h, a, k, beta, rho, cap))

print('the referee COUNTEREXAMPLE CONTINUED')
c_h, k, rho, beta, a, cap = 4.5, 0.5, 0.5, 0.2, 0.01, 0.4
delta_cap = (2 * a * cap + k) / m(cap, beta)
r_cap, r_n = strength(delta_cap), strength(2 * k / rho)
def phi_referee(r):
    delta, tau = auction(r, c_h)
    return delta * (1 - tau) - k - 2 * a * lam_e(tau, beta)
r_start = bisect_increasing(phi_referee, 4, 5)
print(f'r_start={r_start:.12f} r_n={r_n:.12f} r_cap={r_cap:.12f} cap_before_selling_margin={2*k*m(cap,beta)-rho*(2*a*cap+k):.12f} lambda_sell={k*(1-rho)/(2*a*rho):.12f}')
for r in (r_start, 5, r_n, 6, 6.5, 7, r_cap):
    show_row(branch_row(r, c_h, a, k, beta, rho, cap))

print('FULL SELLING BEFORE THE CAP')
c_h, k, rho, beta, a, cap = 4.7, 0.1, 0.5, 0.2, 1.0, 0.3
lambda_sell = k * (1 - rho) / (2 * a * rho)
delta_full = k / (rho * m(lambda_sell, beta))
delta_cap = (2 * a * cap + 2 * k) / ((1 + rho) * m(cap, beta))
r_n, r_full, r_cap = strength(2 * k / rho), strength(delta_full), strength(delta_cap)
def phi_full(r):
    delta, tau = auction(r, c_h)
    return delta * (1 - tau) - k - 2 * a * lam_e(tau, beta)
r_start = bisect_increasing(phi_full, 2.0, r_n)
print(f'r_start={r_start:.12f} r_n={r_n:.12f} r_full={r_full:.12f} r_cap={r_cap:.12f} lambda_sell={lambda_sell:.12f}')
for r in (r_start, r_n, r_full, 3, 4, 5, r_cap):
    show_row(branch_row(r, c_h, a, k, beta, rho, cap))

print('MODEST CHANGE FROM THE BENCHMARK')
c_h, k, rho, beta, a = 6, 0.02, 0.3, 0.294655, 0.025
cap = (e - 1) * beta / (1 + (e - 1) * beta)
delta_cap = (2 * a * cap + k) / m(cap, beta)
print(f'critical_rho={2*k*m(cap,beta)/(2*a*cap+k):.12f} r_n={strength(2*k/rho):.12f} r_cap={strength(delta_cap):.12f}')
for r in (strength(2 * k / rho), strength(delta_cap)):
    show_row(branch_row(r, c_h, a, k, beta, rho, cap))

print('J INCREASING DOES NOT GIVE PHI SINGLE CROSSING')
beta, a, k = 0.2, 1.7, 0.55
def narrow_phi(delta):
    tau = 4 / (9 - delta)
    return delta * (1 - tau) - k - 2 * a * lam_e(tau, beta)
root_up = bisect_increasing(narrow_phi, 1.01, 2.0)
root_down = bisect_increasing(lambda d: -narrow_phi(d), 2.5, 2.99)
print(f'delta_cross_up={root_up:.12f} delta_cross_down={root_down:.12f}')
for delta in (1.1, 2.0, 2.5, 2.9, 2.99):
    tau = 4 / (9 - delta)
    j = delta * (1 - tau)
    j_prime = 1 - 36 / (9 - delta) ** 2
    print(f'delta={delta:.10f} tau={tau:.10f} J={j:.10f} J_prime={j_prime:.10f} phi={narrow_phi(delta):.10f}')
