"""C3 ex ante profits and expected proceeds. Print only."""
from fractions import Fraction as F
from mpmath import mp, mpf, e

mp.dps = 50
print("Three-point r=3 cH=6 delta=0.95")
t0 = F(5, 12)
wL = F(11, 24)
DT = F(2, 3)
gH = F(203, 24)
cH = F(6)
rho = F(1, 4)
for name, E, OH in [("one", F(3, 8), F(1, 4)), ("delay", F(11, 24), F(1, 3))]:
    EV = t0 + wL * E + DT * OH
    print(f" {name}: E[V]={EV}={float(EV):.6f}")
profit_one_high = F(1, 6) * (gH - cH)
Wmid = F(977, 2880)
profit_del_high = profit_one_high + F(2, 3) * Wmid
print(f" high-cost ex ante profit one={profit_one_high}={float(profit_one_high):.6f} delay={profit_del_high}={float(profit_del_high):.6f}")

print()
print("Discrete-Laplace r=3 cH=5 delta=0.95")
a = e ** (-mpf(1) / 2)
M1 = 1 / (1 + a)
m1 = a / (1 + a)
t0m = mpf("0.41666666666666666666666666666666666666666666666667")
wLm = mpf(11) / 24
DTm = mpf(2) / 3
Eone = mpf("0.625")
OHone = mpf("0.35842224920069546173958771215456567953247976199084")
Edel = mpf("0.44874721584880413319802297873424479185744633078577")
OHdel = mpf("0.27029585712509752833859920152168807546120292738373")
for name, E, OH in [("one", Eone, OHone), ("delay", Edel, OHdel)]:
    print(f" {name}: E[V]={t0m + wLm*E + DTm*OH}")
print(f" high-cost ex ante profit one={mpf('0.5')*mpf('0.31216109334878803865750471454590398961066137757426')}")
print(f" high-cost ex ante profit delay={mpf('0.5')*mpf('0.480330724120125131131717370044884107947635394595')}")
print(f" low-cost ex ante gross B(1/2)={mpf(103)/24}")
print()
print("Derivatives at r=3")
m1v = a / (1 + a)
M1v = 1 / (1 + a)
M2v = 1 / (1 + a * a)
gLp = -mpf("0.75") / 18
DTp = mpf(1) / 2 - mpf(1) / 18
for name, mu in [("m1", m1v), ("1/2", mpf("0.5")), ("M1", M1v), ("M2", M2v)]:
    print(f" B'({name})={gLp - mu*DTp}")
Pv = M1v * M1v + m1v * m1v
for delta in [mpf("0.9"), mpf("0.95")]:
    dWN = Pv * delta * (gLp - M2v * DTp) - (gLp - M1v * DTp)
    print(f" delta={delta}: d(W-N)/dr at M1 r=3 = {dWN} P={Pv}")
