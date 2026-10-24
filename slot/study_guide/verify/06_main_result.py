"""Print the three tuples, exact region and H1 example in chapter 06. No assertions."""

from fractions import Fraction as Q

import mpmath as mp

mp.mp.dps = 60


def as_mp(value: Q | mp.mpf) -> mp.mpf:
    return mp.mpf(value.numerator) / value.denominator if isinstance(value, Q) else value


def text_number(value: Q | mp.mpf) -> str:
    return mp.nstr(as_mp(value), 13)


def auction(r: Q) -> tuple[Q, Q, Q, Q, Q, Q]:
    h, ell, p = Q(10), Q(1), Q(1, 2)
    t0 = p * (1-p/r)
    th = r/2+p*p/(2*r)
    tl = ell-(ell*ell-p*p)/(2*r)
    return t0, th, tl, h-th, ell-tl, th-tl


def main() -> None:
    beta, u = mp.mpf("0.294655"), mp.e-1
    lam = u*beta/(1+u*beta)
    b = (1-lam)*beta
    rho, pi, k, cost = Q(1, 4), Q(1, 2), Q(1, 50), Q(6)
    bottom, top = 1/(1+mp.e), mp.e/(1+mp.e)
    print("Exact rational auction quantities")
    for label, r in (("r0", Q(6, 5)), ("r1", Q(3)), ("r2", Q(18, 5))):
        t0, th, tl, gh, gl, spread = auction(r)
        tau = (cost-gl)/(gh-gl)
        bprior = gl+pi*(gh-gl)
        btop = as_mp(gl)+top*as_mp(gh-gl)
        print(f"{label}: r={r}; t0={t0}; tH={th}; tL={tl}; gH={gh}; gL={gl}; "
              f"Delta={spread}; B(prior)={bprior}; tau={tau}")
        print(f"  B(M)={text_number(btop)}; cH-B(prior)={text_number(cost-bprior)}; "
              f"B(M)-cH={text_number(btop-as_mp(cost))}")
        print(f"  k-Delta={text_number(k-spread)}; "
              f"rho*kappa*Delta-k={text_number(as_mp(rho)*bottom*as_mp(spread)-as_mp(k))}")
        beliefs = (as_mp(pi),)*3 if label == "r0" else (bottom, as_mp(pi), top)
        entry = (rho, rho, Q(1)) if label == "r1" else (rho,)*3
        for order, belief, ent in zip((-1, 0, 1), beliefs, entry):
            price = as_mp(t0)+as_mp(ent)*(as_mp(tl-t0)+as_mp(spread)*belief)
            print(f"  x={order:+d}: mu={text_number(belief)}; e={ent}; P={text_number(price)}")
    eh = as_mp(rho)+(1-as_mp(rho))*(b+lam)
    el = as_mp(rho)+(1-as_mp(rho))*b
    ent = as_mp(pi)*eh+(1-as_mp(pi))*el
    print("\nStrong-economy probabilities")
    for name, value in (("lambda", lam), ("b", b), ("b+lambda", b+lam),
                        ("Pr(X=1)", b+as_mp(pi)*lam), ("entry H", eh), ("entry L", el),
                        ("entry total", ent), ("ownership H", as_mp(pi)*eh)):
        print(f"{name} = {text_number(value)}")
    d = top*10-as_mp(cost)
    rc = (d+mp.sqrt(d*d+top*((1-top)-mp.mpf(1)/4)))/top
    print(f"entry ceiling r_C = {text_number(rc)}")
    print("\nExact slot band")
    t1 = (cost-auction(Q(3))[4])/(auction(Q(3))[3]-auction(Q(3))[4])
    t2 = (cost-auction(Q(18, 5))[4])/(auction(Q(18, 5))[3]-auction(Q(18, 5))[4])
    ulo, uhi = (2*t1-1)/(1-t1), (2*t2-1)/(1-t2)
    umax = rho*auction(Q(3))[5]/k-2
    for name, value in (("tau1", t1), ("tau2", t2), ("u lower", ulo),
                        ("u upper", uhi), ("u trading bound", umax),
                        ("weak-cost margin", cost-(auction(Q(6, 5))[3]+auction(Q(6, 5))[4])/2),
                        ("weak-trade margin", k-auction(Q(6, 5))[5])):
        print(f"{name} = {value} = {text_number(value)}")
    for name, value in (("lambda lower", as_mp(ulo)*beta/(1+as_mp(ulo)*beta)),
                        ("lambda upper", as_mp(uhi)*beta/(1+as_mp(uhi)*beta)),
                        ("prior lower", as_mp(t1)/(as_mp(t1)+(1-as_mp(t1))*mp.e)),
                        ("prior upper", as_mp(t2)/(as_mp(t2)+(1-as_mp(t2))*mp.e)),
                        ("prior H2 lower", 3*mp.e/(22+3*mp.e)),
                        ("prior H2 upper", 22/(22+3*mp.e))):
        print(f"{name} = {text_number(value)}")
    # Boundary at u=82/59: retain exact fractions throughout.
    beta_q = Q("0.294655")
    lam_q = ulo*beta_q/(1+ulo*beta_q)
    b_q = (1-lam_q)*beta_q
    m_q, top_q = 1/(2+ulo), (1+ulo)/(2+ulo)
    boundary_entry = rho+(1-rho)*(b_q+pi*lam_q)
    print("\nLower boundary u=82/59")
    print(f"lambda={lam_q}; b={b_q}; M={top_q}; m={m_q}")
    print(f"weak order upper net return={auction(Q(6, 5))[5]-k}")
    print(f"strong correct-order lower net return={rho*m_q*auction(Q(3))[5]-k}")
    print(f"C1 total entry={boundary_entry} = {text_number(boundary_entry)}")
    print(f"CM total entry spans [{rho}, {text_number(boundary_entry)}]")
    print("\nH1 cannot use the strong prior in place of the weak prior")
    alternative_cost = Q(47, 10)
    for r in (Q(6, 5), Q(3), Q(8)):
        t0, th, tl, gh, gl, spread = auction(r)
        print(f"r={r}: cH-B(prior)={alternative_cost-(gh+gl)/2}; "
              f"B(M)-cH={text_number(as_mp(gl)+top*as_mp(gh-gl)-as_mp(alternative_cost))}")
    print(f"Entry at r0 is 1; entry at r1 is {text_number(ent)}")


if __name__ == "__main__":
    main()
