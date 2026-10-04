"""Independent evaluation of closed-form claims: K(cL), xbar, half-line thresholds, rho_E*, rho_O*, (A4'') etc."""
import csv, math
from scipy import optimize
from model import *

def K_of(P):
    a = auction(P); xb = xbar(P); b = P.b
    return (1 - 1 / b) * P.rho * a.DT * min(a.tauL * S(xb + 1, b), a.m * S(xb, b))

def halfline_thresholds(P):
    """x_E: S_X(x)=rho; x_O: S(x-1)=rho; thresholds B(mubar(x))."""
    b = P.b
    xE = optimize.brentq(lambda x: SX(x, b) - P.rho, 0.0, 30.0, xtol=1e-13)
    xO = optimize.brentq(lambda x: S(x - 1, b) - P.rho, 0.0, 30.0, xtol=1e-13)
    # investor-test end x_k for k=.02 (x'>=1): (1-1/b)*0.5*DT*m*exp(-(x-1)/b) = k
    a = auction(P)
    xk = 1 + b * math.log((1 - 1 / b) * a.m * a.DT / (2 * P.k))
    return xE, xO, B(P, mubar(xE, b)), B(P, mubar(xO, b)), xk

def rho_stars(P):
    a = auction(P); b = P.b
    pi0 = 0.25 * (1 + math.exp(-2 / b))
    xs = xstar(P)
    aH, aL = S(xs - 1, b), S(xs + 1, b)
    aa = 0.5 * (aH + aL)
    return pi0, aa, aa / (aa + pi0), aH / (aH + F(-2, b))

if __name__ == "__main__":
    P = Prm(r=3.0, k=0.02, rho=0.25)
    a = auction(P)
    print("B(m),B(1/2),B(M)", B(P, a.m), B(P, .5), B(P, a.M), "tauH", a.tauH, "xstar", xstar(P), "vH", P.b*logit(a.tauH)-1)
    print("(A3) right side", (1-1/P.b)*P.rho*a.m*a.DT)
    print("break point 2B(1/2)-cH", 2*B(P, .5)-P.cH)
    print("K table:")
    for cL in (2.37, 2.4, 2.5, 3.0, 3.5):
        Q = with_(P, cL=cL)
        print(" cL=%.2f tauL=%.4f xbar=%.4f pibar=%.4f K=%.5f" % (cL, auction(Q).tauL, xbar(Q), 0.5*(F(xbar(Q)-1,2)+F(xbar(Q)+1,2)), K_of(Q)))
    # K = .008 root
    c8 = optimize.brentq(lambda c: K_of(with_(P, cL=c)) - 0.008, 2.37, 4.0)
    print("K(cL)=0.008 at cL=%.4f" % c8)
    print("K at floor+: %.5f ; half of (A3): %.5f" % (K_of(with_(P, cL=B(P, a.m)+1e-9)), 0.5*(1-1/P.b)*P.rho*a.m*a.DT))
    xE, xO, tE, tO, xk = halfline_thresholds(P)
    print("half-line: xE=%.4f xO=%.4f thrE=%.4f thrO=%.4f x_k=%.4f" % (xE, xO, tE, tO, xk))
    pi0, aa, rE, rO = rho_stars(P)
    print("pi0=%.5f a=%.5f rhoE*=%.5f rhoO*=%.5f" % (pi0, aa, rE, rO))
    for r1 in (2.5, 3.0, 3.5):
        Q = with_(P, r=r1); print(" r1=%.1f rhoE*,rhoO* =" % r1, rho_stars(Q)[2:])
    # (A4'') sufficient condition at benchmark
    def a4pp(cL):
        Q = with_(P, cL=cL); aq = auction(Q); b = Q.b
        z = z0(Q); xb = xbar(Q); xs = xstar(Q)
        Pz = 0.5*(F(z-1,b)+F(z+1,b)); Hz = 0.5*F(z-1,b)
        B0 = aq.tauL*Pz - Hz
        E0 = Q.rho*SX(z,b) + (1-Q.rho)*SX(xs,b)
        pibar = 0.5*(F(xb-1,b)+F(xb+1,b))
        return E0 - Q.rho*(pibar - Pz) - (1-Q.rho)*min(SX(xs,b), B0/(aq.tauH-aq.tauL)) - Q.rho
    print("(A4'') root:", optimize.brentq(a4pp, 2.37, 4.2))
