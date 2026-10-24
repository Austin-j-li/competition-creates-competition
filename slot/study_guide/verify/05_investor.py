"""Print the residual returns and order payoffs used in chapter 05. No assertions."""

from fractions import Fraction as Q

import mpmath as mp

mp.mp.dps = 60


def as_mp(value: Q | mp.mpf) -> mp.mpf:
    return mp.mpf(value.numerator) / value.denominator if isinstance(value, Q) else value


def show(name: str, value: Q | mp.mpf) -> None:
    print(f"{name} = {mp.nstr(as_mp(value), 13)}")


def beliefs(pi: mp.mpf, u: mp.mpf) -> tuple[mp.mpf, mp.mpf]:
    return pi / (pi + (1 - pi) * (1 + u)), pi * (1 + u) / (1 + pi * u)


def main() -> None:
    u, rho, k = mp.e - 1, mp.mpf(1) / 4, mp.mpf(1) / 50
    pi = mp.mpf(1) / 2
    bottom, top = beliefs(pi, u)
    kappa = min(bottom, 1 - top)
    show("kappa(1/2)", kappa)
    for name, strength, mu_minus, mu_plus, entry_minus, entry_plus in (
        ("weak", Q(6, 5), pi, pi, rho, rho),
        ("strong", Q(3), bottom, top, rho, mp.mpf(1)),
        ("very strong", Q(18, 5), bottom, top, rho, rho),
    ):
        spread_q = (strength - 1) ** 2 / (2 * strength)
        spread = as_mp(spread_q)
        kh = entry_plus * spread * (1 - mu_plus)
        kl = entry_minus * spread * mu_minus
        print(f"\n{name}: r={strength}, Delta={spread_q}")
        show("universal lower bound rho*kappa*Delta", rho * kappa * spread)
        show("universal upper bound Delta", spread)
        show("Delta-k", spread - k)
        show("rho*kappa*Delta-k", rho * kappa * spread - k)
        show("K_H", kh)
        show("K_L", kl)
        # Print all three choices at the stated candidate's fixed prices and entry.
        for class_name, payoffs in (
            ("H", (-entry_minus * spread * (1 - mu_minus) - k, mp.mpf(0), kh - k)),
            ("L", (kl - k, mp.mpf(0), -entry_plus * spread * mu_plus - k)),
        ):
            print(f"  {class_name}: U(-1), U(0), U(1) = "
                  + ", ".join(mp.nstr(value, 13) for value in payoffs))
    print("\nPrior symmetry at 1+u=e")
    for prior in (Q(1, 4), Q(1, 2), Q(3, 4)):
        bottom, top = beliefs(as_mp(prior), u)
        print(f"pi={prior}: m={mp.nstr(bottom, 13)}, 1-M={mp.nstr(1-top, 13)}, "
              f"kappa={mp.nstr(min(bottom, 1-top), 13)}")
    # Bayes-consistent mixed profile, including wrong-signed orders.
    # With e=rho at r=3, all price beliefs are below tau, so entry is optimal.
    lam, beta, prior = Q(1, 3), Q(1, 4), Q(2, 5)
    profiles = ((Q(1, 5), Q(3, 10), Q(1, 2)), (Q(3, 5), Q(3, 10), Q(1, 10)))
    laws = tuple(tuple((1-lam)*eta+lam*mass for eta, mass in zip((beta, 1-2*beta, beta), profile))
                 for profile in profiles)
    post = tuple(prior*fh/(prior*fh+(1-prior)*fl) for fh, fl in zip(*laws))
    reserve, strength, ell = Q(1, 2), Q(3), Q(1)
    t0 = reserve*(1-reserve/strength)
    tl = ell-(ell**2-reserve**2)/(2*strength)
    spread = (strength-ell)**2/(2*strength)
    print("\nMixed, wrong-signed candidate at r=3 (not investor optimal)")
    print("posteriors =", ", ".join(str(value) for value in post))
    u_mixed = lam/((1-lam)*beta)
    bottom_mixed = prior/(prior+(1-prior)*(1+u_mixed))
    top_mixed = prior*(1+u_mixed)/(prior*(1+u_mixed)+1-prior)
    lower = Q(1, 4) * min(bottom_mixed, 1-top_mixed) * spread
    kh, kl = Q(1, 4) * spread * (1-post[2]), Q(1, 4) * spread * post[0]
    print(f"rho*kappa*Delta={lower}; K_H={kh}; K_L={kl}; Delta={spread}")
    for order, belief in zip((-1, 0, 1), post):
        price = t0 + Q(1, 4) * (tl-t0+spread*belief)
        print(f"  x={order:+d}: posterior={belief}, P={price}")


if __name__ == "__main__":
    main()
