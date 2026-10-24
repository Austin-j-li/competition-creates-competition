"""Recompute chapter 12 from slot probabilities. Print values; no tests."""
import mpmath as mp

mp.mp.dps = 60
N = mp.mpf
RHO, FEE, P = N(1) / 4, N(1) / 50, N(1) / 2
BETA = N("0.294655")
U = mp.e - 1
LAM = U * BETA / (1 + U * BETA)
B = (1 - LAM) * BETA
VOLUME = 2 * B + LAM


def show(label: str, *values: N) -> None:
    print(label + ":", "  ".join(mp.nstr(v, 14) for v in values))


def auction(r: N) -> tuple[N, ...]:
    t0 = P * (1 - P / r)
    th = r / 2 + P * P / (2 * r)
    gl = (1 - P * P) / (2 * r)
    tl = 1 - gl
    return t0, th, tl, 10 - th, gl, th - tl


def full(r: N, u: N = U) -> None:
    theta = u / (2 + u)
    m, top = (1 - theta) / 2, (1 + theta) / 2
    lam, b = VOLUME * theta, VOLUME * (1 - theta) / 2
    t0, th, tl, gh, gl, delta = auction(r)
    chi = N(int(gl + top * (gh - gl) >= 6))
    mus = (m, N(1) / 2, top)
    masses = (VOLUME / 2, 1 - VOLUME, VOLUME / 2)
    es = (RHO, RHO, RHO + (1 - RHO) * chi)
    a = tuple(tl - t0 + delta * mu for mu in mus)
    prices = tuple(t0 + e * ax for e, ax in zip(es, a))
    entry = sum(mass * e for mass, e in zip(masses, es))
    mean = sum(mass * price for mass, price in zip(masses, prices))
    sale = prices[1] - prices[0]
    spread = prices[2] - prices[0]
    component = RHO * delta * theta
    entry_component = (1 - RHO) * chi * a[2]
    wins = tuple(mu + (1 - mu) / r for mu in mus)
    cov_entry = masses[0] * (es[2] - es[0])
    cov_win = masses[0] * (es[2] * wins[2] - es[0] * wins[0])
    announcements = tuple((1 - e) * ax for e, ax in zip(es, a))
    no_prep = tuple(-e * ax for e, ax in zip(es, a))
    prep_mean = sum(mass * e * dp for mass, e, dp in zip(masses, es, announcements)) / entry
    show(f"r={r}, u={u}: entry; prices [-1,0,1]", entry, *prices)
    show("spread; class part; entry part; entry share; impacts sale,buy", spread, component,
         entry_component, entry_component / spread, sale, prices[2] - prices[1])
    recovered = 2 * sale / (RHO * delta)
    show("identified theta, lambda, beta", recovered, VOLUME * recovered,
         VOLUME * (1 - recovered) / (2 * (1 - VOLUME * recovered)))
    show("prepared win probabilities [-1,0,1]; gap", *wins, wins[2] - wins[0])
    show("covariance entry, winner", cov_entry, cov_win)
    show("preparation announcement changes", *announcements)
    show("no-preparation announcement changes (hypothetical if e=1)", *no_prep)
    show("mean preparation-report change; mean price; zero-minus-mean", prep_mean, mean, prices[1] - mean)
    show("weighted mean over both reports", sum(mass * (e * dp + (1 - e) * dn)
         for mass, e, dp, dn in zip(masses, es, announcements, no_prep)))
    show("sale net profit", RHO * delta * m - FEE)


def main() -> None:
    theta = U / (2 + U)
    show("slot volume, informed share, presence", VOLUME, theta, LAM)
    full(N(3))
    full(N(18) / 5)
    print("\nSAME COUNTS: u'=8/5")
    full(N(3), N(8) / 5)
    show("counts lower share; incentive upper shares r1,r2", 3 - 2 / VOLUME,
         1 - 2 * FEE / (RHO * auction(N(3))[5]),
         1 - 2 * FEE / (RHO * auction(N(18) / 5)[5]))
    show("share 0.9: beta, sale net profit at r1",
         VOLUME * N("0.1") / (2 * (1 - VOLUME * N("0.9"))),
         RHO * auction(N(3))[5] * N("0.05") - FEE)
    from fractions import Fraction as Fr
    def tau(r: Fr) -> Fr:
        return (48 * r - 3) / (4 * (20 * r - r * r - 1))
    lo, hi = 2 * tau(Fr(3)) - 1, 2 * tau(Fr(18, 5)) - 1
    print("band of shares 2tau(r1)-1, 2tau(r2)-1:", lo, hi, float(lo), float(hi))
    show("weakest correct-order bound in the band at r1", RHO * N(2) / 3 * (1 - N(4245) / 5804) - FEE)
    m = 1 / (1 + mp.e)
    d = FEE / (RHO * m)
    rs = 1 + d + mp.sqrt(d * d + 2 * d)
    top = 1 - m
    x = top * 10 - 6
    rc = (x + mp.sqrt(x * x + top * ((1 - top) - P * P))) / top
    show("exact rS; exact rC", rs, rc)
    r_test = N("2.1241481")
    show("sale net profit at r=2.1241481 (above the display 2.124148)", RHO * auction(r_test)[5] * m - FEE)
    t0, _, tl, _, _, delta = auction(rc)
    show("spread fall just above rC", (1 - RHO) * (tl - t0 + delta * top))
    print("\nPURCHASES ONLY AT r=8/5")
    mean = LAM / 2
    volume = 2 * B + LAM / 2
    mu0 = (1 - 2 * B - LAM) / (2 - 4 * B - LAM)
    show("mean, volume, recovered lambda,b; zero posterior; sale-minus-zero price",
         mean, volume, 2 * mean, (volume - mean) / 2, mu0,
         RHO * auction(N(8) / 5)[5] * (N(1) / 2 - mu0))


if __name__ == "__main__":
    main()
