"""Exact rational checks (a = 3/5, benchmark auction values, c_H = 5, rho = 1/4, k = 1/50, pi = 1/2).

Prints exact fractions for: the closed form of the investor's gain, the symmetric-signal entry identity,
the valley size, the support-line margin, and a grid comparison of the outcome function with the chord.
No assertions: each line prints a value and a Boolean for the reader.
"""
from fractions import Fraction as Fr
from common import *
import branch, pieces as pc

set_mode('exact')
par = P()
a, rho, k = par.a, par.rho, par.k
half = Fr(1, 2)
print('a =', a, ' rho =', rho, ' k =', k)

r = Fr(3)
A = auction(par, r)
tau_r = tau(par, A)
T = tau_r / (1 - tau_r)
print('r=3: Delta_T =', A['DT'], ' w_L =', A['wL'], ' tau =', tau_r, ' T =', T, '=', float(T), ' a*T =', a * T, ' T/a =', T / a, ' 1/a =', 1 / a)
print('A2-type window 1 < T <= 1/a:', 1 < T <= 1 / a)
phi1 = a * T / (1 + a * T)
phi2 = tau_r
phi3 = T / (a + T)
d1 = 1 - phi1
d2 = phi3
print('phi_1 (aT) =', phi1, '=', float(phi1), ' phi_2 (tau) =', phi2, ' phi_3 (T/a) =', phi3, '=', float(phi3))
print('valley bounds d_1 = 1 - phi_1 =', d1, '=', float(d1), '  d_2 = phi_3 =', d2, '=', float(d2), ' d1<d2:', d1 < d2)

# (1) closed form of G1 + k
def G1_closed(phi, eg, eb):
    return A['DT'] * a * (1 - phi) / (1 + a) * (eg / (a + (1 - a) * phi) + eb / (1 - (1 - a) * phi))
for phi, eg, eb in [(half, Fr(1), rho), (Fr(7, 10), Fr(1), rho), (Fr(8, 10), Fr(1), Fr(1)), (Fr(1, 5), rho, rho)]:
    direct = branch.gain_buy(par, A, phi, Fr(1))[0] + k
    print(f"G1+k at phi={phi}: closed={G1_closed(phi, eg, eb)} direct={direct} equal={G1_closed(phi, eg, eb) == direct}")

# (2) symmetric signal: entry and ownership in three zones
def sym(d):
    res = []
    for ph in (d, 1 - d):
        eqs, G0, G1 = branch.equilibria(par, A, ph)
        o = dict(eqs)['FB'] if len(eqs) == 2 else eqs[0][1]
        res.append(o)
    return (res[0]['E'] + res[1]['E']) / 2, (res[0]['OH'] + res[1]['OH']) / 2, (res[0]['Pi'] + res[1]['Pi']) / 2 - A['t0']
E0, O0, P0 = sym(half)
print('no disclosure: E =', E0, ' O_H =', O0, ' Pi-t0 =', P0)
Pg = lambda ph: (ph + (1 - ph) * a) / (1 + a)
for d in [Fr(52, 100), d1 - Fr(1, 1000), d1 + Fr(1, 1000), Fr(55, 100), Fr(65, 100), d2 - Fr(1, 1000), d2, d2 + Fr(1, 1000), Fr(9, 10)]:
    E, O, Pi = sym(d)
    zone = 'below d1' if d <= d1 else ('valley' if d < d2 else 'above d2')
    pred = (1 + rho) / 2 if zone != 'valley' else rho + (1 - rho) * Pg(d) / 2
    print(f"d={float(d):.4f} {zone:9s} E={float(E):.6f} (pred {float(pred):.6f}, equal={E == pred})  O_H={float(O):.6f} (no disc {float(O0):.6f})  Pi-t0={float(Pi):.6f} (no disc {float(P0):.6f})")

# (3) support-line margin at phi_3 with chord through (0, rho*wL) and (phi3, wL + DT*phi3)
wL, DT = A['wL'], A['DT']
gamma = DT + (1 - rho) * wL / phi3
line = lambda x: rho * wL + gamma * x
PhiaT = pc.piece_values(par, A, 'FB', Fr(1), rho, phi1)['Pi'] - A['t0']
print('chord slope gamma =', gamma, '=', float(gamma))
print('margin at phi_1: chord - Phi_(1,rho) =', line(phi1) - PhiaT, '=', float(line(phi1) - PhiaT), ' positive:', line(phi1) - PhiaT > 0)
print('FB(1,1) exists at phi_3: G1 - k =', G1_closed(phi3, Fr(1), Fr(1)) - k, ' positive:', G1_closed(phi3, Fr(1), Fr(1)) - k > 0)
print('NT with e=1 does not exist below phi_3: G0 at phi_3 =', DT * (1 - phi3) - k, ' positive:', DT * (1 - phi3) - k > 0)

# (4) grid comparison: outcome function vs chord, exact, on 1000 rational priors
worst = None
cnt_gap = 0
for i in range(0, 1001):
    ph = Fr(i, 1000)
    eqs, G0, G1 = branch.equilibria(par, A, ph)
    if not eqs:
        cnt_gap += 1
        continue
    for lab, o in eqs:
        ex = (o['Pi'] - A['t0']) - line(ph)
        if worst is None or ex > worst[0]:
            worst = (ex, ph, lab)
print('largest (Phi - chord) over the rational grid (all pure equilibria):', float(worst[0]), 'at phi =', float(worst[1]), worst[2], '; priors without a pure equilibrium on the grid:', cnt_gap)

# (5) policy values
w = half / phi3
E_star = rho + (1 - rho) * w
print('optimal policy: weight on phi_3 =', w, '=', float(w), ' E* =', E_star, '=', float(E_star), ' O_H* = 1/2')
Pistar = wL * E_star + DT * half
print('Pi* - t0 =', Pistar, '=', float(Pistar), ' vs no disclosure', float(P0), ' vs full disclosure', float(((1 - half) * (rho * wL) + half * (wL + DT))))
