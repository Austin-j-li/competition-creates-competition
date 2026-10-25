from mpmath import mp, mpf, e as E, findroot
mp.dps = 30
u = E-1; beta = mpf(294655)/10**6; lam = u*beta/(1+u*beta); b=(1-lam)*beta
pi0 = mpf('0.6'); f1 = b+pi0*lam; fm = b+(1-pi0)*lam; EX=f1-fm; v=f1+fm
def betap(pip):
    lp = EX/(2*pip-1); bp=(v-lp)/2; return bp/(1-lp)
root = findroot(lambda x: betap(x)-mpf(1)/3, mpf('0.68'))
print("beta' = 1/3 at pi' =", root, " check beta'(0.66) =", betap(mpf('0.66')), " beta'(0.69)=", betap(mpf('0.69')))
