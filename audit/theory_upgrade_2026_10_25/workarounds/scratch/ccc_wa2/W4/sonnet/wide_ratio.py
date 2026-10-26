"""Wide-classes economy of Table A6: absolute gap vs Lambda = E_H[min(theta,r)]/E_L[min(theta,r)] along U[0,r]. Prints only."""
import numpy as np

# G_L = U[0.6,1.4], G_H = U[1,19]
def capped_mean_unif(a, b, r):
    # E[min(theta, r)] for theta ~ U[a,b]
    if r <= a:
        return r
    if r >= b:
        return (a + b) / 2
    return ((r * r - a * a) / 2 + r * (b - r)) / (b - a)

print("wide classes: Lambda(r)=E_H[min(theta,r)]/E_L[min(theta,r)], gap s(r)=(E_H cap - E_L cap)/r, S_H/S_L")
for r in (1.0, 1.4, 2.0, 4.5, 5.5, 6.08, 8.0, 12.0, 19.0, 25.0, 50.0):
    eH, eL = capped_mean_unif(1, 19, r), capped_mean_unif(0.6, 1.4, r)
    print(f"  r={r:5.2f}: Lambda={eH/eL:7.4f}  s={ (eH-eL)/r:7.4f}  W_H={eH/r:7.4f} W_L={eL/r:7.4f}")

# S_H/S_L on a grid, to confirm the HR order for this pair
ys = np.linspace(0.0, 1.39, 8)
SL = lambda y: np.clip((1.4 - y) / 0.8, 0, 1) if y >= 0.6 else 1.0
SH = lambda y: np.clip((19 - y) / 18, 0, 1) if y >= 1 else 1.0
print("S_H/S_L on [0,1.39]:", [round(float(SH(y) / SL(y)), 4) for y in ys])
