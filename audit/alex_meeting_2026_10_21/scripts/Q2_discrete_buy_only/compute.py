"""Print the discrete buy-only calculations. Run from the repository root.

This program has no assertions and writes no output files.
"""

from dataclasses import dataclass, replace
from typing import Optional

import mpmath as mp


mp.mp.dps = 60


@dataclass(frozen=True)
class Parameters:
    h: mp.mpf = mp.mpf("10")
    ell: mp.mpf = mp.mpf("1")
    p: mp.mpf = mp.mpf("0.5")
    rho: mp.mpf = mp.mpf("0.25")
    c_L: mp.mpf = mp.mpf("1")
    c_H: mp.mpf = mp.mpf("6")
    k: mp.mpf = mp.mpf("0.02")


@dataclass(frozen=True)
class Auction:
    t_0: mp.mpf
    t_L: mp.mpf
    t_H: mp.mpf
    g_L: mp.mpf
    g_H: mp.mpf
    delta: mp.mpf


@dataclass(frozen=True)
class Flow:
    x: int
    a_H: mp.mpf
    a_L: mp.mpf
    weight: mp.mpf
    mu: Optional[mp.mpf]
    entry: Optional[mp.mpf]
    price: Optional[mp.mpf]


def auction(par: Parameters, r: mp.mpf) -> Auction:
    return Auction(
        par.p * (1 - par.p / r),
        par.ell - (par.ell**2 - par.p**2) / (2 * r),
        r / 2 + par.p**2 / (2 * r),
        (par.ell**2 - par.p**2) / (2 * r),
        par.h - r / 2 - par.p**2 / (2 * r),
        (r - par.ell) ** 2 / (2 * r),
    )


def gross(par: Parameters, r: mp.mpf, mu: mp.mpf) -> mp.mpf:
    obj = auction(par, r)
    return obj.g_L + mu * (obj.g_H - obj.g_L)


def entry(par: Parameters, r: mp.mpf, mu: mp.mpf) -> mp.mpf:
    benefit = gross(par, r, mu)
    # The challenger enters at exact indifference.
    low = benefit >= par.c_L - mp.mpf("1e-50")
    high = benefit >= par.c_H - mp.mpf("1e-50")
    return par.rho * int(low) + (1 - par.rho) * int(high)


def flow_rows(
    par: Parameters,
    r: mp.mpf,
    beta_H: mp.mpf,
    beta_L: mp.mpf = mp.mpf("0"),
    presence: mp.mpf = mp.mpf("1"),
    noise: tuple[mp.mpf, mp.mpf, mp.mpf] = (mp.mpf(1) / 3,) * 3,
) -> tuple[Flow, ...]:
    a, b, c = noise
    s_H, s_L = presence * beta_H, presence * beta_L
    h_law = ((1 - s_H) * a, b + s_H * (a - b), c + s_H * (b - c), s_H * c)
    l_law = ((1 - s_L) * a, b + s_L * (a - b), c + s_L * (b - c), s_L * c)
    obj = auction(par, r)
    rows = []
    for x, a_H, a_L in zip((-1, 0, 1, 2), h_law, l_law):
        weight = (a_H + a_L) / 2
        # Only (beta_H,beta_L)=(0,0) receives the specified off-path completion.
        mu = a_H / (a_H + a_L) if weight else (mp.mpf(1) if x == 2 else None)
        e = entry(par, r, mu) if mu is not None else None
        price = obj.t_0 + e * (obj.t_L - obj.t_0 + obj.delta * mu) if e is not None else None
        rows.append(Flow(x, a_H, a_L, weight, mu, e, price))
    return tuple(rows)


def outcomes(par: Parameters, r: mp.mpf, beta_H: mp.mpf) -> tuple[mp.mpf, mp.mpf]:
    rows = flow_rows(par, r, beta_H)
    total_entry = sum(row.weight * row.entry for row in rows if row.weight)
    high_ownership = sum(row.a_H * row.entry / 2 for row in rows if row.weight)
    return total_entry, high_ownership


def buy_payoffs(par: Parameters, r: mp.mpf, beta_H: mp.mpf) -> tuple[mp.mpf, mp.mpf]:
    rows = flow_rows(par, r, beta_H)
    delta = auction(par, r).delta
    gain_H = sum(row.entry * delta * (1 - row.mu) / 3 for row in rows if row.x >= 0)
    gain_L = sum(-row.entry * delta * row.mu / 3 for row in rows if row.x >= 0)
    return gain_H - par.k, gain_L - par.k


def strength_at_spread(par: Parameters, d: mp.mpf) -> mp.mpf:
    return par.ell + d + mp.sqrt(d**2 + 2 * par.ell * d)


def gross_buy_general(
    par: Parameters,
    r: mp.mpf,
    s: mp.mpf,
    noise: tuple[mp.mpf, mp.mpf, mp.mpf],
) -> mp.mpf:
    a, b, c = noise
    d_0 = 2 * b + s * (a - b)
    d_1 = 2 * c + s * (b - c)
    mu_0, mu_1 = (b + s * (a - b)) / d_0, (c + s * (b - c)) / d_1
    return auction(par, r).delta * (
        a * b * entry(par, r, mu_0) / d_0
        + b * c * entry(par, r, mu_1) / d_1
    )


def fmt(value: Optional[mp.mpf], digits: int = 14) -> str:
    return "off path" if value is None else mp.nstr(value, digits)


def main() -> None:
    par = Parameters()
    cutoff = strength_at_spread(par, 3 * par.k / par.rho)
    entry_ceiling = par.h - par.c_H + mp.sqrt((par.h - par.c_H) ** 2 - par.p**2)
    print("Method: direct finite sums; mpmath decimal precision =", mp.mp.dps)
    print("Inputs:", par)
    print("Laplace scale b does not enter the discrete model.")
    print("Trade cutoff r_T =", fmt(cutoff, 40))
    print("Expensive-entry ceiling r_C =", fmt(entry_ceiling, 40))
    print("Minimum B_r(1/3), for 1 < r < 10, is its r=10 limit:", fmt(gross(par, mp.mpf(10), mp.mpf(1) / 3)))
    print("Benchmark point outcomes and buy payoffs against the equilibrium schedule:")
    for r in map(mp.mpf, ("1.2", "3", "3.6", "8.5")):
        margin = auction(par, r).delta * entry(par, r, mp.mpf("0.5")) / 3 - par.k
        beta = mp.mpf(int(margin > 0))
        E, O_H = outcomes(par, r, beta)
        U_H, U_L = buy_payoffs(par, r, beta)
        print("r", fmt(r), "beta_H", fmt(beta), "E", fmt(E), "O_H", fmt(O_H), "U_H(buy)", fmt(U_H), "U_L(buy)", fmt(U_L), "g_L", fmt(auction(par, r).g_L))
        for row in flow_rows(par, r, beta):
            print("  x", row.x, "Pr(X)", fmt(row.weight), "mu", fmt(row.mu), "entry", fmt(row.entry), "price", fmt(row.price))

    print("Benchmark equilibrium set on the r grid (the prescribed investor tie rule):")
    grid = tuple(map(mp.mpf, ("1.05", "1.2", "1.5", "1.8", "1.95"))) + (cutoff,) + tuple(map(mp.mpf, ("2", "2.5", "3", "3.6", "5", "7.9"))) + (entry_ceiling,) + tuple(map(mp.mpf, ("8", "8.5", "9.9")))
    for r in grid:
        margin = auction(par, r).delta * entry(par, r, mp.mpf("0.5")) / 3 - par.k
        at_tie = abs(margin) < mp.mpf("1e-45")
        beta = mp.mpf(0) if at_tie else mp.mpf(int(margin > 0))
        E, O_H = outcomes(par, r, beta)
        label = "{0}; conventional tie rule: beta_H in [0,1]" if at_tie else "{" + str(int(beta)) + "}"
        print("r", fmt(r), "beta_H set", label, "beta_L {0}", "E", fmt(E), "O_H", fmt(O_H))

    print("Cutoff outcomes if conventional mixing at indifference replaces the prescribed tie rule:")
    for beta in map(mp.mpf, ("0", "0.25", "0.5", "0.75", "1")):
        E, O_H = outcomes(par, cutoff, beta)
        print("beta_H", fmt(beta), "E", fmt(E), "O_H", fmt(O_H), "H buy payoff", fmt(buy_payoffs(par, cutoff, beta)[0]))

    print("A floor-valid variant: c_L=0.02; all other monetary parameters stay fixed:")
    floor_par = replace(par, c_L=mp.mpf("0.02"))
    for r in map(mp.mpf, ("1.2", "3", "3.6", "8.5")):
        beta = mp.mpf(int(auction(floor_par, r).delta * floor_par.rho / 3 > floor_par.k))
        E, O_H = outcomes(floor_par, r, beta)
        print("r", fmt(r), "beta_H", fmt(beta), "E", fmt(E), "O_H", fmt(O_H), "g_H", fmt(auction(floor_par, r).g_H))

    print("Presence extension at r=3, c_L=0.02, beta_H=1:")
    for presence in map(mp.mpf, ("0.1", "0.5", "0.9", "1")):
        rows = flow_rows(floor_par, mp.mpf(3), mp.mpf(1), presence=presence)
        E = sum(row.weight * row.entry for row in rows)
        O_H = sum(row.a_H * row.entry / 2 for row in rows)
        print("lambda", fmt(presence), "mu(-1)", fmt(rows[0].mu), "E", fmt(E), "O_H", fmt(O_H))

    print("General-noise examples at Delta_T=1, rho=0.25:")
    r = strength_at_spread(par, mp.mpf(1))
    for name, noise, cost, high_cost in (
        ("multiplicity", tuple(map(mp.mpf, ("0.1", "0.2", "0.7"))), "0.045", "6"),
        ("mixed interval; no equilibrium with forced no-trade ties", tuple(map(mp.mpf, ("0.7", "0.2", "0.1"))), "0.08", "12"),
    ):
        general_par = replace(floor_par, k=mp.mpf(cost), c_H=mp.mpf(high_cost))
        K_0 = gross_buy_general(general_par, r, mp.mpf(0), noise)
        K_1 = gross_buy_general(general_par, r, mp.mpf(1), noise)
        root = mp.findroot(lambda s: gross_buy_general(general_par, r, s, noise) - general_par.k, (mp.mpf("0.01"), mp.mpf("0.99")))
        print(name, "r", fmt(r), "noise", tuple(fmt(x) for x in noise), "k", fmt(general_par.k), "K(0)", fmt(K_0), "K(1)", fmt(K_1), "conventional mixed beta_H", fmt(root), "root payoff", fmt(gross_buy_general(general_par, r, root, noise) - general_par.k))

    print("Price partitions outside the cost floor, with c_L=3 and fixed beta_H=1:")
    pool_par = replace(par, c_L=mp.mpf(3))
    for r in map(mp.mpf, ("3", "3.1")):
        obj = auction(pool_par, r)
        e_bar = entry(pool_par, r, mp.mpf("0.5"))
        e_H = entry(pool_par, r, mp.mpf(1))
        print("r", fmt(r), "B(1/3)", fmt(gross(pool_par, r, mp.mpf(1) / 3)), "B(1/2)", fmt(gross(pool_par, r, mp.mpf("0.5"))), "H payoff, one inactive interior", fmt(obj.delta * e_bar / 6 - pool_par.k), "E, one inactive interior", fmt(e_bar / 3 + e_H / 6), "E, both interiors active", fmt(2 * e_bar / 3 + e_H / 6))


if __name__ == "__main__":
    main()
