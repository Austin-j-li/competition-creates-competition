from mpmath import mp, mpf, e as E, sqrt, diff
mp.dps = 30
# share identity (pi-m)/(M-m) = Pr(1)/v, class component = I- * v / Pr(1)
u = E-1; beta = mpf(294655)/10**6; lam = u*beta/(1+u*beta); b=(1-lam)*beta
def Mf(pi): return pi*(1+u)/(pi*(1+u)+1-pi)
def mf(pi): return pi/(pi+(1-pi)*(1+u))
for pi in [mpf('0.2'), mpf('0.5'), mpf('0.8')]:
    M, m = Mf(pi), mf(pi); P1 = b+pi*lam; Pm = b+(1-pi)*lam; v = P1+Pm
    print(f"pi={float(pi)}: (pi-m)/(M-m)={float((pi-m)/(M-m)):.6f}  Pr1/v={float(P1/v):.6f}   P1*(M-pi)={float(P1*(M-pi)):.6f} Pm*(pi-m)={float(Pm*(pi-m)):.6f} pi(1-pi)lam={float(pi*(1-pi)*lam):.6f}")

# Trend counterexample: point masses, uniform incumbent, high reserve
def model(h, ell, p, cH, r):
    t0 = p*(1-p/r); tH = r/2 + p**2/(2*r); tL = ell - (ell**2-p**2)/(2*r)
    gH = h - r/2 - p**2/(2*r); gL = (ell**2-p**2)/(2*r)
    D = tH-tL; tau=(cH-gL)/(gH-gL)
    return t0,tH,tL,gH,gL,D,tau
h, ell, p, cH, rho, k = mpf(10), mpf(1), mpf('0.95'), mpf(6), mpf(1)/4, mpf(1)/250
pi = mpf(1)/2; M, m = Mf(pi), mf(pi)
print("\nCounterexample: h=10, ell=1, p=0.95, c_H=6, rho=1/4, k=1/250, benchmark slot, prior 1/2")
for r in [mpf('1.42'), mpf('1.5'), mpf('1.6'), mpf('1.7'), mpf('1.8'), mpf('1.9')]:
    t0,tH,tL,gH,gL,D,tau = model(h,ell,p,cH,r)
    A = lambda mu: tL-t0+D*mu
    chi = 1 if M>=tau else 0
    S = rho*D*(M-m) + (1-rho)*chi*A(M)
    KH = (1 if M>=tau else rho)*D*(1-M); KL = rho*D*m
    print(f"r={float(r):.2f}: tau={float(tau):.4f} (pi<tau: {pi<tau}, M>=tau: {M>=tau}) D={float(D):.5f} wL={float(tL-t0):.5f} A(M)={float(A(M)):.5f} "
          f"S={float(S):.5f} I+={float(rho*D*(M-pi)+(1-rho)*chi*A(M)):.5f} rho*kappa*D-k={float(rho*m*D-k):+.5f} KH-k={float(KH-k):+.4f}")
# derivative of A_r(M) in r for uniform/point-mass: [ell^2-3p^2+M(r^2-ell^2)]/(2r^2)
print("benchmark: ell^2-3p^2 =", 1-3*0.25, " p threshold ell/sqrt3 =", float(1/sqrt(3)))
