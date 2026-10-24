"""Print the N2 calculations. Run from the project root. No files are written."""

from dataclasses import dataclass
from itertools import product

import mpmath as mp


mp.mp.dps = 45


@dataclass(frozen=True)
class Parameters:
    p: mp.mpf = mp.mpf("0.5")
    rho: mp.mpf = mp.mpf("0.25")
    c_L: mp.mpf = mp.mpf("1")
    c_H: mp.mpf = mp.mpf("6")
    b: mp.mpf = mp.mpf("2")
    k: mp.mpf = mp.mpf("0.02")


def show(label: str, values: tuple[mp.mpf, ...]) -> None:
    print(label + ": " + ", ".join(mp.nstr(value, 15) for value in values))


def dot(left: tuple[mp.mpf, ...], right: tuple[mp.mpf, ...]) -> mp.mpf:
    return sum((x * y for x, y in zip(left, right)), mp.mpf("0"))


def uniform_payoffs(
    par: Parameters, r: mp.mpf, center: mp.mpf, width: mp.mpf
) -> tuple[mp.mpf, mp.mpf]:
    """Average the auction payoffs over one uniform value distribution."""
    lower, upper = center - width, center + width
    t_0 = par.p * (1 - par.p / r)
    below = max(mp.mpf("0"), min(upper, par.p) - lower)
    a, z = max(lower, par.p), min(upper, r)
    g_integral = mp.mpf("0")
    if z > a:
        g_integral += ((z**3 - a**3) / 3 - par.p**2 * (z - a)) / (2 * r)
    a = max(lower, r, par.p)
    if upper > a:
        g_integral += (upper**2 - a**2) / 2
        g_integral -= (r / 2 + par.p**2 / (2 * r)) * (upper - a)
    a = max(lower, par.p)
    theta_integral = max(mp.mpf("0"), (upper**2 - a**2) / 2) if upper > a else mp.mpf("0")
    t_integral = t_0 * below + theta_integral - g_integral
    return t_integral / (2 * width), g_integral / (2 * width)


def bounds(
    par: Parameters, prior: tuple[mp.mpf, ...], values: tuple[mp.mpf, ...]
) -> tuple[mp.mpf, mp.mpf]:
    """Optimize a mean over likelihood weights with ratio at most exp(2/b)."""
    cap = mp.exp(2 / par.b)
    means = []
    for weights in product((mp.mpf("1"), cap), repeat=len(prior)):
        mass = tuple(prob * weight for prob, weight in zip(prior, weights))
        means.append(dot(mass, values) / sum(mass))
    return min(means), max(means)


def posterior(
    par: Parameters, prior: tuple[mp.mpf, ...], orders: tuple[mp.mpf, ...], x: mp.mpf
) -> tuple[mp.mpf, ...]:
    mass = tuple(prob * mp.exp(-abs(x - order) / par.b) for prob, order in zip(prior, orders))
    return tuple(value / sum(mass) for value in mass)


def flow_objects(
    par: Parameters,
    prior: tuple[mp.mpf, ...],
    orders: tuple[mp.mpf, ...],
    target: tuple[mp.mpf, ...],
    profit: tuple[mp.mpf, ...],
    x: mp.mpf,
) -> tuple[tuple[mp.mpf, ...], mp.mpf, mp.mpf, mp.mpf, mp.mpf]:
    belief = posterior(par, prior, orders, x)
    mean_t, mean_g = dot(belief, target), dot(belief, profit)
    score = tuple(-mp.sign(x - order) / par.b for order in orders)
    derivative = dot(belief, tuple((value - mean_t) * slope for value, slope in zip(target, score)))
    density = sum(prob * mp.exp(-abs(x - order) / par.b) for prob, order in zip(prior, orders)) / (2 * par.b)
    return belief, mean_t, mean_g, derivative, density


def cluster_example(par: Parameters) -> None:
    print("N2: three uniform distributions; the two low types share the sell order")
    centers = tuple(map(mp.mpf, ("1", "1.02", "10")))
    width = mp.mpf("0.05")
    prior = tuple(map(mp.mpf, ("0.25", "0.25", "0.5")))
    orders = tuple(map(mp.mpf, ("-1", "-1", "1")))
    show("centers", centers)
    show("half-width, p, rho, c_L, c_H, b, k", (width, par.p, par.rho, par.c_L, par.c_H, par.b, par.k))
    show("prior", prior)
    m = 1 / (1 + mp.exp(2 / par.b))
    for r in tuple(map(mp.mpf, ("1.2", "3", "3.6"))):
        pairs = tuple(uniform_payoffs(par, r, center, width) for center in centers)
        target, profit = tuple(pair[0] for pair in pairs), tuple(pair[1] for pair in pairs)
        lower_t, upper_t = bounds(par, prior, target)
        lower_g, upper_g = bounds(par, prior, profit)
        d = min(lower_t - max(target[:2]), target[2] - upper_t)
        show("r", (r,))
        show("t_j", target)
        show("g_j", profit)
        show("T_min, T_max, B_min, B_max", (lower_t, upper_t, lower_g, upper_g))
        show("target range, d, global marginal lower bound", (max(target) - min(target), d, (1 - 1 / par.b) * par.rho * d))
        show("profit at prior", (dot(prior, profit),))
        determinant = (target[1] - target[0]) * (profit[2] - profit[0]) - (target[2] - target[0]) * (profit[1] - profit[0])
        show("collinearity determinant", (determinant,))
        if r == mp.mpf("3"):
            low_g = (profit[0] + profit[1]) / 2
            tau = (par.c_H - low_g) / (profit[2] - low_g)
            x_star = par.b / 2 * mp.log(tau / (1 - tau))
            alpha_H = 1 - mp.exp((x_star - 1) / par.b) / 2
            alpha_L = mp.exp(-(x_star + 1) / par.b) / 2
            entry = par.rho + (1 - par.rho) * (alpha_H + alpha_L) / 2
            ownership = (par.rho + (1 - par.rho) * alpha_H) / 2
            show("m, M, tau, x_star", (m, 1 - m, tau, x_star))
            show("entry, high-class ownership", (entry, ownership))
            for x in tuple(map(mp.mpf, ("-1", "0", "1"))):
                belief = posterior(par, prior, orders, x)
                show("flow, T, B", (x, dot(belief, target), dot(belief, profit)))
    print()


def collision_example(par: Parameters) -> None:
    print("N2: a nonmonotone order profile; profit is not a function of target proceeds")
    r, width = mp.mpf("3"), mp.mpf("0.05")
    centers = tuple(map(mp.mpf, ("1", "2", "10")))
    prior = tuple(map(mp.mpf, ("0.15", "0.15", "0.7")))
    orders = tuple(map(mp.mpf, ("1", "-1", "0")))
    pairs = tuple(uniform_payoffs(par, r, center, width) for center in centers)
    target, profit = tuple(pair[0] for pair in pairs), tuple(pair[1] for pair in pairs)
    x_left = mp.mpf("-0.95")
    left = flow_objects(par, prior, orders, target, profit, x_left)
    x_right = mp.findroot(
        lambda x: dot(posterior(par, prior, orders, x), target) - left[1],
        (mp.mpf("0"), mp.mpf("1")), solver="bisect", maxsteps=200,
    )
    right = flow_objects(par, prior, orders, target, profit, x_right)
    weight_left, weight_right = left[4] / abs(left[3]), right[4] / abs(right[3])
    price_belief = tuple((weight_left * a + weight_right * z) / (weight_left + weight_right) for a, z in zip(left[0], right[0]))
    t_0 = par.p * (1 - par.p / r)
    fixed_entry_price = t_0 + par.rho * (left[1] - t_0)
    show("centers", centers)
    show("prior", prior)
    show("orders", orders)
    show("t_j", target)
    show("g_j", profit)
    show("left x, T, B", (x_left, left[1], left[2]))
    show("left posterior", left[0])
    show("right x, T, B", (x_right, right[1], right[2]))
    show("right posterior", right[0])
    show("conditional weights of the two branches", (weight_left / (weight_left + weight_right), weight_right / (weight_left + weight_right)))
    show("posterior conditional on T", price_belief)
    show("B conditional on T; fixed-entry price", (dot(price_belief, profit), fixed_entry_price))
    print("At c_H=6 the two flow-based entry decisions differ.")
    print("At c_H=20, entry=rho at every flow. Price then reveals T; the displayed posterior is the actual price posterior.")
    print("This is a competitive auction continuation. Investor optimality is not imposed.")
    print()


def action_collision(par: Parameters) -> None:
    print("N2: exact price collision across different flow-based entry decisions")
    # Uniform values on [0,0.1], [3,3.1], [101.95,102.05].
    target = (mp.mpf(5) / 12, mp.mpf(37) / 24, mp.mpf(37) / 24)
    profit = (mp.mpf("0"), mp.mpf(181) / 120, mp.mpf(12055) / 120)
    mu_high = (mp.mpf(9) / 10, mp.mpf(17) / 200, mp.mpf(3) / 200)
    mu_low = (mp.mpf(3) / 5, mp.mpf(39) / 100, mp.mpf(1) / 100)
    amplitude = par.b / 4 * mp.log(mp.mpf(117) / 17)
    prior_odds = mp.sqrt((mp.mpf(183) / 17) * (mp.mpf(61) / 39))
    group_prior = prior_odds / (1 + prior_odds)
    prior = (group_prior * mp.mpf(60) / 61, 1 - group_prior, group_prior / 61)
    orders = (amplitude, -amplitude, amplitude)
    t_0, high_cost = mp.mpf(5) / 12, mp.mpf("1.61")
    high_price = dot(mu_high, target)
    low_price = t_0 + par.rho * (dot(mu_low, target) - t_0)
    show("c_L, c_H for this variant", (mp.mpf("0"), high_cost))
    show("order amplitude", (amplitude,))
    show("prior", prior)
    show("positive-tail posterior", posterior(par, prior, orders, mp.mpf("2")))
    show("negative-tail posterior", posterior(par, prior, orders, mp.mpf("-2")))
    show("positive-tail T, B, flow-based price", (dot(mu_high, target), dot(mu_high, profit), high_price))
    show("negative-tail T, B, flow-based price", (dot(mu_low, target), dot(mu_low, profit), low_price))
    print("A price-based entry rule cannot equal 1 and rho at this shared price.")
    print("This profile is not an equilibrium. It shows failure of the flow-based price construction.")


if __name__ == "__main__":
    parameters = Parameters()
    cluster_example(parameters)
    collision_example(parameters)
    action_collision(parameters)
