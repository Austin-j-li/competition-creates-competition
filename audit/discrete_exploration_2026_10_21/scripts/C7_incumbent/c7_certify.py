"""C7 interval certificate at the benchmark (print only).

Uses mpmath interval arithmetic. Each inequality is printed with the interval of its margin.
A margin interval that lies wholly above zero certifies the inequality.
Benchmark: h=10, ell=1, p=1/2, rho=1/4, c_L=0, c_H=5, b=2, k=1/50, pi=1/2, r_0=6/5, r_1=3.
"""
from mpmath import iv, mpf, nstr

iv.dps = 60
one = iv.mpf(1)
h, l, p, rho, cH, k = iv.mpf(10), one, one / 2, one / 4, iv.mpf(5), one / 50
a = iv.exp(-one / 2)
m1, M1 = a / (1 + a), one / (1 + a)


def show(name, x):
    print(f'{name:60s} [{nstr(mpf(x.a), 15)}, {nstr(mpf(x.b), 15)}]')


def margin(name, x):
    status = 'certified > 0' if x.a > 0 else ('certified < 0' if x.b < 0 else 'NOT certified')
    print(f'{name:60s} [{nstr(mpf(x.a), 12)}, {nstr(mpf(x.b), 12)}]  {status}')


def auction(r):
    t0 = p * (1 - p / r)
    tL = l - (l**2 - p**2) / (2 * r)
    gH = h - r / 2 - p**2 / (2 * r)
    gL = (l**2 - p**2) / (2 * r)
    DT = (r - l)**2 / (2 * r)
    return t0, tL, gH, gL, DT


def Dlow(mu, a_, r):
    """Challenger gross profit at belief U[a_, r] for p <= a_ <= ell."""
    return mu * (h - (a_ + r) / 2) + (1 - mu) * (l - a_)**2 / (2 * (r - a_))


r0, r1 = iv.mpf(6) / 5, iv.mpf(3)
t0, tL, gH, gL, DT = auction(r1)
show('a = exp(-1/2)', a)
show('m1', m1)
show('M1', M1)
print('\n-- Weak incumbent r_0 = 6/5 --')
margin('k - Delta_T(r_0)  (unique no trade)', k - auction(r0)[4])
margin('c_H - B_{r0}(1/2)  (no high-cost entry at the prior)', cH - (auction(r0)[3] + (auction(r0)[2] - auction(r0)[3]) / 2))
print('\n-- Strong incumbent r_1 = 3: continuation conditions --')
margin('c_H - B_{r1}(1/2)  (Case A at every posterior <= 1/2)', cH - (gL + (gH - gL) / 2))
margin('B_{r1}(M1) - c_H  (good news recruits high cost without jumps)', gL + M1 * (gH - gL) - cH)
margin('c_H - M1 (h - r1)  (deterrence feasible)', cH - M1 * (h - r1))
margin('c_H - M1 (h - (ell + r1)/2)  (threshold below ell: condition N)', cH - M1 * (h - (l + r1) / 2))
margin('D(M1;[p,r1]) - c_H  (threshold above p: interior)', Dlow(M1, p, r1) - cH)
print('\n-- Threshold, bid, and outcomes at r_1 --')
E = M1 * h + (1 - M1) * l
const = M1 * (2 * h - r1) * r1 + (1 - M1) * l**2 - 2 * cH * r1
Rhat = (E - cH) - iv.sqrt((E - cH)**2 - const)
show('R_hat* = J* (root of the deterrence quadratic)', Rhat)
show('D(M1;[R_hat*, r1]) (equals c_H)', Dlow(M1, Rhat, r1))
margin('R_hat* - p', Rhat - p)
margin('ell - R_hat*', l - Rhat)
entry_jump = rho + (1 - rho) * Rhat / (2 * r1)
entry_base = rho + (1 - rho) / 2
OH_jump = (rho + (1 - rho) * M1 * Rhat / r1) / 2
OH_base = (rho + (1 - rho) * M1) / 2
show('entry, jump model = rho + (1-rho) R_hat*/(2 r1)', entry_jump)
show('entry, base model = rho + (1-rho)/2', entry_base)
show('O_H, jump model = (rho + (1-rho) M1 R_hat*/r1)/2', OH_jump)
show('O_H, base model = (rho + (1-rho) M1)/2', OH_base)
show('preemption probability = (1 - R_hat*/r1)/2', (1 - Rhat / r1) / 2)
margin('entry_jump - rho  (Prop. 2(ii) analog survives)', entry_jump - rho)
margin('O_H jump - rho/2', OH_jump - rho / 2)
print('\n-- Trading at r_1 --')
margin('m1 rho Delta_T(r1) - k  (residual floor beats cost: unique full buying)', m1 * rho * DT - k)
show('Pi_jump(1) + k = 2 rho m1 M1 Delta_T', 2 * rho * m1 * M1 * DT)
show('Pi_base(1) + k = (1+rho) m1 M1 Delta_T', (1 + rho) * m1 * M1 * DT)
show('Pi(0) + k = rho Delta_T / 2', rho * DT / 2)
print('\n-- Prices at r_1 under full buying --')
J = Rhat
PG = ((Rhat**2 + p**2) / 2 + (1 - rho) * J * (r1 - Rhat)
      + rho * (M1 * (r1**2 - Rhat**2) / 2 + (1 - M1) * ((l**2 - Rhat**2) / 2 + l * (r1 - l)))) / r1
PB = t0 + rho * (tL - t0 + DT * m1)
show('P_G (jump model, closed form)', PG)
show('P_B', PB)
margin('P_G - P_B  (price reveals the posterior)', PG - PB)
print('\n-- Transfer at r_1 (good news, then ex ante with Pr(good) = 1/2) --')
gainG = ((1 - rho) * (l - J)**2 / 2 + (1 - rho) * (M1 * (r1**2 - l**2) / 2 + ((1 - M1) * l - J) * (r1 - l))) / r1
show('incumbent gain = target loss, at good news', gainG)
show('incumbent gain = target loss, ex ante', gainG / 2)
margin('incumbent gain at good news', gainG)
print('\n-- Three-point model: deterrence at the revealing flow (mu = 1) --')
for cHx in (iv.mpf(6), iv.mpf(5)):
    margin(f'(h - r1) - c_H with c_H={iv.nstr(cHx,3)}  (positive: no jump deters)', (h - r1) - cHx)
