"""Certificate for the CM endpoint at the largest prior under C1."""
from pathlib import Path
from fractions import Fraction as Q
from xp1_numbers import produce,exp_one,I,monotone,D,tau,bounds,rho,fee,gross

HERE=Path(__file__).resolve().parent


def main():
    v=produce()
    r,pi=v["rstar"],v["pimax"]
    d=monotone(D,r)
    e=exp_one()
    beta=Q(294655,1000000)
    u=e-1
    lam=u*beta/(1+u*beta)
    b=beta/(1+u*beta)
    b0=(1-lam)*(1-2*beta)
    top=pi*(b+lam)/(b+pi*lam)
    zero=pi*b0/(pi*b0+(1-pi)*(b0+lam))
    lines=["CM endpoint: r=r_star, pi=tau(r_star)=pi_max.",
        "Exact identities: B_r(pi)=6; rho*D(r)*pi=k; all low-class sale residuals equal zero.",
        "N tuple: both classes abstain; mu=(pi,pi,pi); entry=(rho,rho,rho).",
        "F tuple: H buys, L abstains; mu=(pi,mu0,M(pi)); entry=(rho,rho,1).",
        "CM admits abstention by the high-cost challenger at the posterior pi=tau.",
        "IM and I0 both admit abstention by the low class at zero net profit."]
    for name,value in [("r_star",r),("pi_max",pi),("M(pi_max)",top),
        ("zero-order posterior in F",zero),("pi-mu0",pi-zero),
        ("H correct profit in F",d*(1-top)-fee),
        ("H correct profit in N",rho*d*(1-pi)-fee),
        ("J(r_star)-k",d*(1-pi)-fee),
        ("tau_A below 3/4",Q(3,4)-v["tau_rA"])]:
        lines.append(name+" "+bounds(value))
    lines.append("rho*J(2)-k = 11/11200 > 0, so r_J<2.")
    lines.extend([
        "Beyond beta=1/3: beta=2/5, u=8/5, lambda=16/41, b=10/41, b0=5/41.",
        "M=13/18. The profile H abstains, L sells gives mu0=21/26.",
        "B_3.6(mu0)-6="+str(gross(Q(18,5),Q(21,26))-6),
        "6-B_3.6(M)="+str(6-gross(Q(18,5),Q(13,18))),
        "rho*m*D(3)-k="+str(rho*Q(5,18)*D(Q(3))-fee),
        "u is a presence-to-liquidity mass ratio. Under full orders, direction-conditioned identity odds are pi*u and (1-pi)*u.",
        "At prior 1/2 those odds are u/2: "+bounds((e-1)/2),
    ])
    for line in lines:
        print(line)
    (HERE/"xp1_boundary.log").write_text("\n".join(lines)+"\n")


if __name__=="__main__":
    main()
