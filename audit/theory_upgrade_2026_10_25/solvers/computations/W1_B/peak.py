from mpmath import mp, mpf, findroot, diff, sqrt
mp.dps = 30
h, l, p, cH, k = mpf(10), mpf(1), mpf(1)/2, mpf(6), mpf(1)/50
def Delta(r): return (r-l)**2/(2*r)
def gH(r): return h - r/2 - p**2/(2*r)
def gL(r): return (l**2-p**2)/(2*r)
def tau(r): return (cH-gL(r))/(gH(r)-gL(r))
def J(r): return Delta(r)*(1-tau(r))
rpk = findroot(lambda r: diff(J, r), mpf(5))
rgc = findroot(lambda r: gH(r)-cH, mpf(8))
print("benchmark J peaks at r =", rpk, " J =", J(rpk), " tau there =", tau(rpk), "; gH = cH at r =", rgc)
# product Delta*(gH-cH) peak (where (E) stops holding)
rE = findroot(lambda r: diff(lambda x: Delta(x)*(gH(x)-cH), r), mpf(5))
print("Delta*(gH-cH) peaks at r =", rE, " tau there =", tau(rE))
# elasticities at r0 and r2
for r in [mpf(6)/5, mpf(18)/5]:
    eD = diff(Delta, r)/Delta(r); em = -diff(gH, r)/(gH(r)-cH)
    print(f"r={float(r)}: eps_Delta={float(eD):.4f} eps_m={float(em):.4f} ratio={float(eD/em):.3f} sigma={float(Delta(r)/9):.4f}")
# the referee family elasticities at z=7
print("the referee z=7: eps_Delta = 1/6 =", 1/6, " eps_m = 1/(8-7) = 1;  ratio", 1/6)
