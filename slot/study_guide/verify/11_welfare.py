"""Recompute chapter 11 from auction cash flows. Print values; no tests."""
import mpmath as mp

mp.mp.dps = 60
N = mp.mpf
RHO, PI, COST, FEE = N(1) / 4, N(1) / 2, N(6), N(1) / 50
BETA = N("0.294655")
U = mp.e - 1
LAM = U * BETA / (1 + U * BETA)
B = (1 - LAM) * BETA
M = mp.e / (1 + mp.e)
MLOW = 1 - M


def show(label: str, *values: N) -> None:
    print(label + ":", "  ".join(mp.nstr(v, 14) for v in values))


def kernel(r: N, p: N, v: N) -> tuple[N, N, N]:
    t0 = p * max(1 - p / r, N(0))
    if v < p:
        return t0, N(0), N(0)
    if r <= p:
        return p, v - p, N(1)
    if v <= r:
        g = (v * v - p * p) / (2 * r)
        return v - g, g, v / r
    t = r / 2 + p * p / (2 * r)
    return t, v - t, N(1)


def outcomes(r: N, p: N, cost: N = COST, hidden: bool = False) -> tuple[N, ...]:
    t0 = p * max(1 - p / r, N(0))
    th, gh, _ = kernel(r, p, N(10))
    tl, gl, _ = kernel(r, p, N(1))
    delta = th - tl
    # At these declared nodes, the global bounds select zero or full orders.
    full = RHO * MLOW * delta > FEE
    mu = (MLOW, PI, M) if full else (PI, PI, PI)
    fh = (B, 1 - 2 * B - LAM, B + LAM) if full else (B, 1 - 2 * B, B)
    fl = (B + LAM, 1 - 2 * B - LAM, B) if full else fh
    e = tuple(RHO + (1 - RHO) * N(int(gl + (PI if hidden else z) * (gh - gl) >= cost)) for z in mu)
    eh = sum(fh[j] * e[j] for j in range(3))
    el = sum(fl[j] * e[j] for j in range(3))
    entry = PI * eh + (1 - PI) * el
    admiss = PI * eh * N(int(10 >= p)) + (1 - PI) * el * N(int(1 >= p))
    incumbent = max(1 - p / r, N(0))
    two = incumbent * admiss
    sale = incumbent + admiss - two
    proceeds = t0 + PI * eh * (th - t0) + (1 - PI) * el * (tl - t0)
    base_value = (r * r - p * p) / (2 * r) if r > p else N(0)
    surplus = base_value
    for value, prob, erate, profit in ((N(10), PI, eh, gh), (N(1), 1 - PI, el, gl)):
        if value >= p:
            surplus += prob * erate * (profit + p * min(p / r, N(1)))
    surplus -= cost * (entry - RHO)
    return (entry, sale, two, proceeds, surplus, RHO * MLOW * delta - FEE,
            cost - (gl + PI * (gh - gl)), gl + M * (gh - gl) - cost)


def main() -> None:
    access = outcomes(N(3), N(1) / 2)
    hidden = outcomes(N(3), N(1) / 2, hidden=True)
    show("access: proceeds, surplus", access[3], access[4])
    show("hidden: proceeds, surplus", hidden[3], hidden[4])
    gain = access[3] - hidden[3]
    show("gains: proceeds, surplus", gain, access[4] - hidden[4])
    delta = N(2) / 3
    transfer = LAM * delta * (PI * (1 - M) + (1 - PI) * RHO * MLOW)
    show("gross transfer, conditional gross, break-even z, resource cost", transfer, transfer / LAM, gain / transfer, LAM * FEE)
    t0, th, tl = N(5) / 12, N(37) / 24, N(7) / 8
    show("w_H, w_L at r1 (9/8, 11/24); p F_1(p) (1/12)", th - t0, tl - t0, (N(1) / 2) ** 2 / 3)
    gl1, gh1 = N(1) / 8, N(203) / 24
    low_profit = gl1 + MLOW * (gh1 - gl1)
    show("outside region: B_1(m) - 12/5; bracket B_1(m) - c_H + pF_1(p)", low_profit - N(12) / 5,
         low_profit - N(12) / 5 + N(1) / 12)
    seen_low = outcomes(N(3), N(1) / 2, N(12) / 5)
    hidden_low = outcomes(N(3), N(1) / 2, N(12) / 5, hidden=True)
    show("outside region (cost 12/5): proceeds and surplus changes", seen_low[3] - hidden_low[3], seen_low[4] - hidden_low[4])

    print("\nNASH PAYMENT: omega, spread at weak, spread at strong, change")
    for omega in (N(0), N(1) / 4, N(1) / 2, N(3) / 4):
        weak = 9 * omega + (1 - 2 * omega) / 60
        strong = 9 * omega + (1 - 2 * omega) * N(2) / 3
        show("payment", omega, weak, strong, strong - weak)

    print("\nRESERVE TABLE: entry, sale, two admissible, proceeds, surplus, T,C,J")
    for p in (N(1) / 2, N(101) / 100, N(31) / 20):
        for r in (N(6) / 5, N(3)):
            show(f"p={p}, r={r}", *outcomes(r, p))
    ph = mp.sqrt(2 * 3 * (10 - COST / M) - 9)
    weak_top = 10 - COST / M
    show("strict deterrence reserve endpoints p_H, weak top", ph, weak_top)
    # Trade margin rho*kappa*min(Delta_0, Delta_1) - k at both ends (Delta_0 = p since r0 < p).
    for p in (ph, weak_top):
        d1 = N(3) / 2 - p + 3 * p * p / 6
        show(f"trade margin at p={mp.nstr(p, 8)}", RHO * MLOW * min(p, d1) - FEE)
    show("payment gap coefficient", N(2) / 3 - N(1) / 60)


if __name__ == "__main__":
    main()
