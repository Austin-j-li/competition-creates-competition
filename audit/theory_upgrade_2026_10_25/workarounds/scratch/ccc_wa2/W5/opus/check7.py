from mpmath import mp, mpf
mp.dps=30
# raw-test 'if' direction can fail only for large rho with small w_L: w_L=0, pi=0.9, u=20, rho=0.8
pi, u, rho = mpf('0.9'), mpf(20), mpf('0.8')
M = pi*(1+u)/(pi*(1+u)+1-pi); m = pi/(pi+(1-pi)*(1+u))
lhs = (1-rho)*M; rhs = rho*((pi-m)-(M-pi))
print("M",M,"m",m,"(1-rho)M",lhs,"rho*bracket",rhs, "recruitment fails to make I+>I-:", lhs<rhs)
