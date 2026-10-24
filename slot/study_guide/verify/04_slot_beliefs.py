"""Print the order laws, beliefs and prices used in chapter 04. No assertions."""

from fractions import Fraction as Q

import mpmath as mp

mp.mp.dps = 60


def decimal(value: Q | mp.mpf) -> str:
    """Print 12 decimal places without a binary float conversion."""
    number = mp.mpf(value.numerator) / value.denominator if isinstance(value, Q) else value
    return mp.nstr(number, 13)


def order_law(lam: Q | mp.mpf, beta: Q | mp.mpf, profile: tuple) -> tuple:
    """Return the conditional law on the ordered menu (-1, 0, 1)."""
    eta = (beta, 1 - 2 * beta, beta)
    return tuple((1 - lam) * mass + lam * informed for mass, informed in zip(eta, profile))


def posterior(pi: Q | mp.mpf, high: Q | mp.mpf, low: Q | mp.mpf) -> Q | mp.mpf:
    return pi * high / (pi * high + (1 - pi) * low)


def print_profile(name: str, lam: Q | mp.mpf, beta: Q | mp.mpf, pi: Q | mp.mpf,
                  high_profile: tuple, low_profile: tuple) -> None:
    high = order_law(lam, beta, high_profile)
    low = order_law(lam, beta, low_profile)
    print(name)
    u = lam/((1-lam)*beta)
    bottom = pi/(pi+(1-pi)*(1+u))
    top = pi*(1+u)/(pi*(1+u)+1-pi)
    print(f"  bounds: m={decimal(bottom)}, M={decimal(top)}")
    for order, fh, fl in zip((-1, 0, 1), high, low):
        print(f"  x={order:+d}: f_H={decimal(fh)}, f_L={decimal(fl)}, "
              f"LR={decimal(fh / fl)}, posterior={decimal(posterior(pi, fh, fl))}")


def main() -> None:
    beta, pi = mp.mpf("0.294655"), mp.mpf(1) / 2
    u = mp.e - 1
    lam = u * beta / (1 + u * beta)
    b, b0 = (1 - lam) * beta, (1 - lam) * (1 - 2 * beta)
    bottom = pi / (pi + (1 - pi) * (1 + u))
    top = pi * (1 + u) / (pi * (1 + u) + 1 - pi)
    print("Benchmark primitives: beta=0.294655, pi=1/2, 1+u=e")
    for name, value in (("lambda", lam), ("b", b), ("b0", b0), ("u", u),
                        ("bottom m", bottom), ("top M", top)):
        print(f"{name} = {decimal(value)}")
    print_profile("Full orders", lam, beta, pi, (0, 0, 1), (1, 0, 0))
    print_profile("Mixed profile with wrong signs", Q(1, 3), Q(1, 4), Q(2, 5),
                  (Q(1, 5), Q(3, 10), Q(1, 2)), (Q(3, 5), Q(3, 10), Q(1, 10)))
    print_profile("One-sided profile outside beta<=1/3", Q(6, 17), Q(2, 5), Q(1, 2),
                  (0, 1, 0), (1, 0, 0))
    lam_bad, beta_bad = Q(6, 17), Q(2, 5)
    b_bad, b0_bad = (1 - lam_bad) * beta_bad, (1 - lam_bad) * (1 - 2 * beta_bad)
    top_bad = (b_bad + lam_bad) / (2 * b_bad + lam_bad)
    zero_bad = (b0_bad + lam_bad) / (2 * b0_bad + lam_bad)
    print(f"  exact: b={b_bad}, b0={b0_bad}, M={top_bad}, mu(0)={zero_bad}, "
          f"mu(0)-M={zero_bad - top_bad}")
    # A possible price partition for the probability calculation alone.
    # It is not a competitive price map when the entry floor and spread are positive.
    high = order_law(lam, beta, (0, 0, 1))
    low = order_law(lam, beta, (1, 0, 0))
    pool = posterior(pi, high[0] + high[1], low[0] + low[1])
    print(f"Belief if a price pools sale and zero: {decimal(pool)}")
    h, ell, reserve, strength, cost = Q(10), Q(1), Q(1, 2), Q(3), Q(6)
    t0 = reserve * (1-reserve/strength)
    tH = strength/2+reserve**2/(2*strength)
    tL = ell-(ell**2-reserve**2)/(2*strength)
    spread, rho = tH-tL, Q(1, 4)
    gH, gL = h-tH, ell-tL
    tau = (cost-gL)/(gH-gL)
    print(f"At r=3: tau={tau} = {decimal(tau)}")
    for order, belief, entry in ((-1, bottom, rho), (0, pi, rho), (1, top, mp.mpf(1))):
        price = t0 + entry * (tL - t0 + spread * belief)
        recovered = (price - t0 - entry * (tL - t0)) / (entry * spread)
        print(f"  x={order:+d}: e={decimal(entry)}, P={decimal(price)}, "
              f"posterior recovered from P={decimal(recovered)}")
    print(f"Laplace scale s=2: exp(2/s)={decimal(mp.exp(1))}, "
          f"matched top posterior={decimal(mp.e / (1 + mp.e))}")


if __name__ == "__main__":
    main()
