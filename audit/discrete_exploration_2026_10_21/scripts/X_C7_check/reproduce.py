"""Independent auction calculations and equilibrium candidates; print results only."""

from pathlib import Path
import mpmath as mp

mp.mp.dps = 70
Q = mp.mpf
H, L, P, RHO, COST, K = map(Q, ("10", "1", ".5", ".25", "5", ".02"))
A = mp.exp(-Q(".5"))
BAD, GOOD = A / (1 + A), 1 / (1 + A)
OUT = Path(__file__).resolve().parent
LINES = []


def emit(label, *values):
    text = label + " " + " ".join(mp.nstr(v, 56) if isinstance(v, mp.mpf) else str(v) for v in values)
    LINES.append(text)
    print(text, flush=True)


def midpoint_root(function, low, high, steps=230):
    fl = function(low)
    for _ in range(steps):
        mid = (low + high) / 2
        fm = function(mid)
        if fl * fm <= 0:
            high = mid
        else:
            low, fl = mid, fm
    return (low + high) / 2


def positive_integral(value, low, high):
    end = min(value, high)
    if end <= low:
        return Q(0)
    return value * (end - low) - (end * end - low * low) / 2


def challenger_integral(value, low, high):
    end = min(P, high)
    below = max(Q(0), end - low) * max(Q(0), value - P)
    return below + positive_integral(value, max(low, P), high)


def average_gain(mu, low, high):
    return (mu * challenger_integral(H, low, high) + (1 - mu) * challenger_integral(L, low, high)) / (high - low)


def excess_integral(floor, low, high):
    start = max(low, floor)
    if start >= high:
        return Q(0)
    return ((high - floor) ** 2 - (start - floor) ** 2) / 2


def continuation(mu, r, cost=COST, jump=True):
    prior_gain = average_gain(mu, Q(0), r)
    if prior_gain < cost:
        return "A", r, Q(0), RHO
    if not jump or mu * (H - r) >= cost:
        return "B", r, Q(0), Q(1)
    if average_gain(mu, P, r) <= cost:
        cutoff = P
    else:
        cutoff = midpoint_root(lambda z: average_gain(mu, z, r) - cost, P, r - Q("1e-66"))
    if cutoff <= L:
        bid = cutoff
    else:
        bid = L + (cutoff - L) * mu * (1 - RHO) / (1 - RHO * mu)
    return "C", cutoff, bid, RHO + (1 - RHO) * cutoff / r


def proceeds_integral(value, low, high, floor=P):
    length = high - low
    if length <= 0:
        return Q(0)
    if value == H:
        return floor * length + excess_integral(floor, low, high)
    ceiling = max(floor, L)
    if floor >= L:
        return floor * length
    return floor * length + excess_integral(floor, low, high) - excess_integral(ceiling, low, high)


def conditional_values(mu, r, cost=COST, jump=True):
    case, cutoff, bid, entry = continuation(mu, r, cost, jump)
    no_entry_all = P * (r - P)
    if case != "C":
        e = entry
        th = (e * proceeds_integral(H, Q(0), r) + (1 - e) * no_entry_all) / r
        tl = (e * proceeds_integral(L, Q(0), r) + (1 - e) * no_entry_all) / r
        incumbent = e * (1 - mu) * excess_integral(L, Q(0), r) / r
        incumbent += (1 - e) * excess_integral(P, Q(0), r) / r
        challenger = e * average_gain(mu, Q(0), r) - (e - RHO) * cost
        return (case, cutoff, bid, entry, th, tl, incumbent, challenger)
    no_entry_jump = bid * (r - cutoff)
    th = (proceeds_integral(H, Q(0), cutoff) + RHO * proceeds_integral(H, cutoff, r, bid) + (1 - RHO) * no_entry_jump) / r
    tl = (proceeds_integral(L, Q(0), cutoff) + RHO * proceeds_integral(L, cutoff, r, bid) + (1 - RHO) * no_entry_jump) / r
    incumbent = (1 - mu) * excess_integral(L, Q(0), cutoff) / r
    incumbent += ((1 - RHO) * excess_integral(bid, cutoff, r) + RHO * (1 - mu) * excess_integral(max(L, bid), cutoff, r)) / r
    gain_silent = (mu * challenger_integral(H, Q(0), cutoff) + (1 - mu) * challenger_integral(L, Q(0), cutoff)) / r
    gain_jump = (mu * challenger_integral(H, cutoff, r) + (1 - mu) * challenger_integral(L, cutoff, r)) / r
    challenger = gain_silent - (1 - RHO) * cost * cutoff / r + RHO * gain_jump
    return (case, cutoff, bid, entry, th, tl, incumbent, challenger)


def posteriors(beta):
    return (1 - beta * (1 - A)) / (2 - beta * (1 - A)), (1 + beta * (1 / A - 1)) / (2 + beta * (1 / A - 1))


def trade_gain(beta, r, jump=True):
    mb, mg = posteriors(beta)
    cb, cg = conditional_values(mb, r, jump=jump), conditional_values(mg, r, jump=jump)
    return BAD * (1 - mb) * (cb[4] - cb[5]) + GOOD * (1 - mg) * (cg[4] - cg[5]) - K


def allocation_surplus(mu, r, values, cost):
    case, cutoff, _, entry = values[:4]
    if case != "C":
        value_with_entry = mu * H * r + (1 - mu) * (r * r + L * L) / 2
        value_without_entry = (r * r - P * P) / 2
        return (entry * value_with_entry + (1 - entry) * value_without_entry) / r - (entry - RHO) * cost
    value_silent = mu * H * cutoff + (1 - mu) * (L * cutoff + excess_integral(L, Q(0), cutoff))
    value_jump_with_entry = mu * H * (r - cutoff) + (1 - mu) * (L * (r - cutoff) + excess_integral(L, cutoff, r))
    value_jump_without_entry = (r * r - cutoff * cutoff) / 2
    return (value_silent + RHO * value_jump_with_entry + (1 - RHO) * value_jump_without_entry - (1 - RHO) * cost * cutoff) / r


def aggregate(beta, r, jump=True, cost=COST):
    mb, mg = posteriors(beta)
    cb, cg = conditional_values(mb, r, cost, jump), conditional_values(mg, r, cost, jump)
    high_good = BAD + beta * (GOOD - BAD)
    low_good = BAD
    mass_good = (high_good + low_good) / 2
    entry = (1 - mass_good) * cb[3] + mass_good * cg[3]
    ownership = ((1 - high_good) * cb[3] + high_good * cg[3]) / 2
    proceeds = ((1 - high_good) * cb[4] + high_good * cg[4] + (1 - low_good) * cb[5] + low_good * cg[5]) / 2
    incumbent = (1 - mass_good) * cb[6] + mass_good * cg[6]
    challenger = (1 - mass_good) * cb[7] + mass_good * cg[7]
    surplus = (1 - mass_good) * allocation_surplus(mb, r, cb, cost) + mass_good * allocation_surplus(mg, r, cg, cost)
    preemption = (1 - mass_good) * (1 - cb[1] / r) + mass_good * (1 - cg[1] / r)
    return entry, ownership, proceeds, incumbent, challenger, surplus, preemption


def scan_roots(r, jump=True, mesh=90):
    roots = []
    old_beta, old_gain = Q(0), trade_gain(Q(0), r, jump)
    for index in range(1, mesh + 1):
        beta = Q(index) / mesh
        gain = trade_gain(beta, r, jump)
        if old_gain * gain < 0:
            root = midpoint_root(lambda z: trade_gain(z, r, jump), old_beta, beta)
            residual = trade_gain(root, r, jump)
            if abs(residual) < Q("1e-50"):
                roots.append(root)
            else:
                emit("DISCONTINUITY", r, root, residual)
        old_beta, old_gain = beta, gain
    return roots


def base_entry_boundary_gain(r):
    low_gain = (L * L - P * P) / (2 * r)
    high_gain = H - r / 2 - P * P / (2 * r)
    tau = (COST - low_gain) / (high_gain - low_gain)
    beta = (2 * tau - 1) / ((1 / A - 1) * (1 - tau))
    mb, mg = posteriors(beta)
    gap = (r - L) ** 2 / (2 * r)
    return gap * (BAD * RHO * (1 - mb) + GOOD * (1 - mg)) - K


emit("PRECISION", mp.mp.dps)
emit("POSTERIORS", BAD, GOOD)
emit("FIELDS", "entry ownership proceeds incumbent challenger surplus preemption")
for r, beta in ((Q("1.2"), Q(0)), (Q(3), Q(1)), (Q("3.6"), Q(1)), (Q("4.2"), Q(1))):
    emit("BASE", r, *aggregate(beta, r, False))
    emit("JUMP", r, *aggregate(beta, r, True))
    emit("INVESTOR", r, trade_gain(beta, r, False), trade_gain(beta, r, True))
    for jump in (False, True):
        values = aggregate(beta, r, jump)
        emit("ACCOUNTING_RESIDUAL", r, jump, values[2] + values[3] + values[4] - values[5])

for mu in (BAD, Q(".5"), GOOD):
    values = conditional_values(mu, Q(3))
    emit("CONTINUATION_R3", mu, *values[:4], "spread", values[4] - values[5], "price", mu * values[4] + (1 - mu) * values[5])
emit("COST_5.05_R3", *aggregate(Q(1), Q(3), True, Q("5.05")))
emit("CONDITION_N_MARGIN", COST - GOOD * (H - (L + Q(3)) / 2))

for beta in map(Q, ("0", ".25", ".5", ".75", "1")):
    emit("CONSTANT_SPREAD_PROFIT_R3", beta, trade_gain(beta, Q(3)))

for r in map(Q, ("1.41", "1.43", "1.44", "1.6", "1.75", "1.76", "1.765", "1.79", "1.795")):
    for jump in (False, True):
        roots = scan_roots(r, jump)
        emit("BRANCHES", r, "jump" if jump else "base", "no_trade", trade_gain(Q(0), r, jump) <= 0, "full", trade_gain(Q(1), r, jump) >= 0, "roots", *roots)
        for beta in roots:
            mb, mg = posteriors(beta)
            emit("ROOT_DETAIL", r, jump, beta, mb, mg, *continuation(mg, r, jump=jump), "residual", trade_gain(beta, r, jump), "outcomes", *aggregate(beta, r, jump))

for r in map(Q, ("2.05", "2.45", "2.85", "3.05", "3.45", "3.85", "4.05")):
    emit("ENTRY_PATH", r, aggregate(Q(1), r, False)[0], aggregate(Q(1), r, True)[0])

strength_inverse = lambda gap: L + gap + mp.sqrt(gap * gap + 2 * L * gap)
emit("BASE_COEXISTENCE", strength_inverse(K / ((1 + RHO) * BAD * GOOD)), strength_inverse(2 * K / RHO))
emit("BASE_INTERIOR_LEFT", midpoint_root(base_entry_boundary_gain, Q("1.40"), Q("1.41")))
emit("THRESHOLDS", H - COST / GOOD, 2 * (H - COST / GOOD) - L, midpoint_root(lambda r: average_gain(GOOD, Q(0), r) - COST, Q(3), Q(5)), midpoint_root(lambda r: average_gain(GOOD, P, r) - COST, Q(3), Q(4)))

# A separating private offer gives both parties their continuation payoff.
mu, r, e = Q(".5"), Q(3), Q(1)
for value in map(Q, (".5", ".8", "1.5", "2.5")):
    seller_value = e * (mu * value + (1 - mu) * min(value, L)) + (1 - e) * P
    emit("LOCKUP_EQUALITY", value, seller_value, value - seller_value, "gain", Q(0))

# A bid above the low value excludes every weak type from the survivor set.
mu, r, bid = GOOD, Q(3), Q(2)
cutoff = L + (bid - L) * (1 - RHO * mu) / (mu * (1 - RHO))
emit("POOLING_DEVIATION", "bid", bid, "survivor_cutoff", cutoff, "largest_survivor_gain", mu * (H - cutoff), "cost", COST)
emit("POOLING_DEVIATION_STRONG_TYPE_GAIN", (r - bid) * (1 - RHO * mu) - (1 - mu) * (r - L))

# The three-point purchase residual is zero at the revealing top flow.
emit("THREE_POINT_R3", "gross", RHO * (Q(3) - L) ** 2 / (6 * Q(3)), "net", RHO * (Q(3) - L) ** 2 / (6 * Q(3)) - K, "deterrence_floor", H - Q(3))

# Continuous Laplace flows, full orders of opposite signs, and cost six.
r, cost, scale = Q(3), Q(6), Q(2)
lower, upper = 1 / (1 + mp.exp(1)), 1 / (1 + mp.exp(-1))
tau = midpoint_root(lambda mu: average_gain(mu, Q(0), r) - cost, Q(".5"), upper)
corner_mu = midpoint_root(lambda mu: average_gain(mu, P, r) - cost, tau, upper)
flow_of = lambda mu: scale * mp.log(mu / (1 - mu)) / 2
flow_tau, flow_corner = flow_of(tau), flow_of(corner_mu)
density_h = lambda x: mp.exp(-abs(x - 1) / scale) / (2 * scale)
density_l = lambda x: mp.exp(-abs(x + 1) / scale) / (2 * scale)


def laplace_vector(x):
    dh, dl = density_h(x), density_l(x)
    mu = dh / (dh + dl)
    cj, cb = conditional_values(mu, r, cost), conditional_values(mu, r, cost, False)
    mass = (dh + dl) / 2
    extra = (1 - RHO) * (1 - cj[1] / r) * (cost - average_gain(mu, cj[1], r)) if cj[0] == "C" else Q(0)
    return [mass * cb[3], mass * cj[3], dh * cb[3] / 2, dh * cj[3] / 2, mass * extra]


boundaries = [-mp.inf, Q(-1), flow_tau, flow_corner, Q(1), mp.inf]
laplace = [mp.quad(lambda x: laplace_vector(x)[index], boundaries) for index in range(5)]
emit("LAPLACE_FLOW_BOUNDARIES", flow_tau, flow_corner)
emit("LAPLACE_BASE_JUMP_ENTRY_OWNERSHIP_SURPLUS_INCREMENT", *laplace)
emit("LAPLACE_MIN_PREPARATION_GAIN", lower * (H - r), "ORDER_BOUND", (1 - 1 / scale) * RHO * lower * (r - L) ** 2 / (2 * r))
(OUT / "independent_output.txt").write_text("\n".join(LINES) + "\n")
