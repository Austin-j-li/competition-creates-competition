"""Independent cash-flow reconstruction of the P5 registry.

Run from the repository root with .venv/bin/python and redirect stdout to
scripts/XP5/run_log.txt. Outputs stay in this directory. No checked module
is imported or executed. Every calculation uses rational or interval arithmetic.
"""
from __future__ import annotations

import csv
import hashlib
import math
import platform
from decimal import Decimal, localcontext, ROUND_HALF_EVEN, ROUND_FLOOR, ROUND_CEILING
from datetime import datetime, timezone
from fractions import Fraction as F
from pathlib import Path

import mpmath
from mpmath import iv, mp

iv.dps = 90
mp.dps = 120
HERE = Path(__file__).resolve().parent
TEAM = HERE.parents[1]


def lift(value):
    value = F(value)
    return iv.mpf(value.numerator) / value.denominator


def bounds(value):
    return tuple(mp.make_mpf(part) for part in value._mpi_)


def interval_text(value):
    """Print decimal bounds outwards from the exact binary endpoints."""
    output = []
    for endpoint, direction in zip(value._mpi_, (ROUND_FLOOR, ROUND_CEILING)):
        sign, mantissa, exponent, _ = endpoint
        with localcontext() as ctx:
            ctx.prec = 1200
            exact = Decimal(mantissa) * Decimal(2) ** exponent
            if sign:
                exact = -exact
            if exact:
                quantum = Decimal(1).scaleb(exact.adjusted() - 95)
                exact = exact.quantize(quantum, rounding=direction)
            output.append(str(exact))
    return f"[{output[0]}, {output[1]}]"


def show(label, value):
    print(f"{label}: {interval_text(value)}")


# For n >= N+1, successive Taylor terms have ratio at most 1/(N+2).
# The exact upper tail is therefore 1/(N+1)! divided by 1-1/(N+2).
N = 120
e_partial = sum((F(1, math.factorial(n)) for n in range(N + 1)), F(0))
e_tail = F(1, math.factorial(N + 1)) / (1 - F(1, N + 2))
E = lift(e_partial) + iv.mpf([0, 1]) * lift(e_tail)
rho, cost, k = lift("1/4"), lift(6), lift("1/50")
beta = lift("0.294655")
u = E - 1
lam = 1 - 1 / (1 + beta * u)
b = (1 - lam) * beta
d = b + lam / 2
M, m = (b + lam) / (2 * b + lam), b / (2 * b + lam)
theta = lam / (lam + 2 * b)


def auction(r):
    """Integrals of actual payments, split at the reserve and low value."""
    p, ell, h = lift("1/2"), lift(1), lift(10)
    no_entry = p * (r - p) / r
    high = (p * p + (r * r - p * p) / 2) / r
    low = (p * p + (ell * ell - p * p) / 2 + ell * (r - ell)) / r
    low_rent = ((ell - p) * p + ell * (ell - p) - (ell * ell - p * p) / 2) / r
    return no_entry, high, low, h - high, low_rent


def threshold(r):
    _, _, _, gh, gl = auction(r)
    return (cost - gl) / (gh - gl)


def delta(r):
    _, high, low, _, _ = auction(r)
    return high - low


def profit(r, belief):
    _, _, _, gh, gl = auction(r)
    return belief * gh + (1 - belief) * gl


def inverse_delta(D):
    return 1 + D + iv.sqrt(D * (D + 2))


def candidate(r, high_buy, low_sale, presence=lam, liquidity=beta, buy_entry=None, hidden=False):
    """Enumerate class, slot identity, order, and independent cost states."""
    qset = (-1, 0, 1)
    mass = {q: (1 - presence) * (liquidity if q else 1 - 2 * liquidity) for q in qset}
    high_law = {q: mass[q] for q in qset}
    low_law = {q: mass[q] for q in qset}
    high_law[1] += presence * high_buy
    high_law[0] += presence * (1 - high_buy)
    low_law[-1] += presence * low_sale
    low_law[0] += presence * (1 - low_sale)
    freq = {q: (high_law[q] + low_law[q]) / 2 for q in qset}
    posterior = {q: high_law[q] / (high_law[q] + low_law[q]) for q in qset}
    entry = {}
    for q in qset:
        belief = lift("1/2") if hidden else posterior[q]
        margin = profit(r, belief) - cost
        lower, upper = bounds(margin)
        if q == 1 and buy_entry is not None:
            entry[q] = buy_entry
        elif lower > 0:
            entry[q] = lift(1)
        elif upper < 0:
            entry[q] = rho
        else:
            raise ValueError(f"Entry sign unresolved at {q}: {interval_text(margin)}")
    base, high, low, _, _ = auction(r)
    # Class cash flows arise from the actual preparation probability.
    class_high = {q: (1 - entry[q]) * base + entry[q] * high for q in qset}
    class_low = {q: (1 - entry[q]) * base + entry[q] * low for q in qset}
    price = {q: posterior[q] * class_high[q] + (1 - posterior[q]) * class_low[q] for q in qset}
    after_prepare = {q: posterior[q] * high + (1 - posterior[q]) * low for q in qset}
    mean_order = sum((q * freq[q] for q in qset), lift(0))
    mean_price = sum((freq[q] * price[q] for q in qset), lift(0))
    total_entry = sum((freq[q] * entry[q] for q in qset), lift(0))
    winner = {q: posterior[q] + (1 - posterior[q]) / r for q in qset}
    total_winner = sum((freq[q] * entry[q] * winner[q] for q in qset), lift(0))
    cov_entry = sum((q * freq[q] * entry[q] for q in qset), lift(0)) - mean_order * total_entry
    cov_winner = sum((q * freq[q] * entry[q] * winner[q] for q in qset), lift(0)) - mean_order * total_winner
    return dict(freq=freq, posterior=posterior, entry=entry, price=price,
                prepared_change={q: after_prepare[q] - price[q] for q in qset},
                absent_change={q: base - price[q] for q in qset},
                high_payoff={q: q * (class_high[q] - price[q]) - abs(q) * k for q in qset},
                low_payoff={q: q * (class_low[q] - price[q]) - abs(q) * k for q in qset},
                volume=freq[-1] + freq[1], mean_order=mean_order, mean_price=mean_price,
                total_entry=total_entry, winner=winner, total_winner=total_winner,
                cov_entry=cov_entry, cov_winner=cov_winner,
                high_ownership=sum((high_law[q] * entry[q] / 2 for q in qset), lift(0)),
                spread=price[1] - price[-1], sell_impact=price[0] - price[-1],
                buy_impact=price[1] - price[0])


r0, r1, r2 = lift("6/5"), lift(3), lift("18/5")
r155, r160, r165 = lift("31/20"), lift("8/5"), lift("33/20")
rF = inverse_delta(k / m)
rS = inverse_delta(k / (rho * m))
rN = inverse_delta(2 * k / rho)
# Solve the independently integrated gross-profit equation after multiplication by 2r.
a = 10 * M - cost
rC = (a + iv.sqrt(a * a + M * (lift("3/4") - M))) / M
o0 = candidate(r0, lift(0), lift(0))
o1 = candidate(r1, lift(1), lift(1))
o2 = candidate(r2, lift(1), lift(1))
oU = {tag: candidate(r, lift(1), lift(0)) for tag, r in ((155, r155), (160, r160), (165, r165))}
v = o1["volume"]
class1 = rho * delta(r1) * theta
entry1 = o1["spread"] - class1
leftC = candidate(rC, lift(1), lift(1), buy_entry=lift(1))
rightC = candidate(rC, lift(1), lift(1), buy_entry=rho)
alt_u = lift("8/5")
alt_lam = v * alt_u / (2 + alt_u)
alt_beta = (v - alt_lam) / (2 * (1 - alt_lam))
alt = candidate(r1, lift(1), lift(1), presence=alt_lam, liquidity=alt_beta)

values = dict(
    u_p5_B=u, lambda_p5_B=lam, beta_p5_B=beta, b_p5_B=b,
    M_p5_B=M, m_p5_B=m, d_slot_B=d,
    vol_none_B=o0["volume"], vol_buy_B=oU[160]["volume"], vol_full_B=v,
    theta_B=theta, theta_pct_B=theta,
    margin_obs_beta_B=lift("1/3") - beta,
    margin_obs_u_hi_B=lift("2686/1559") - u,
    margin_obs_buy_recruit_B=M - threshold(r1),
    margin_obs_ceiling_B=threshold(r2) - M,
    rC_check_B=rC, margin_obs_r2_above_rC_B=r2-rC,
    margin_obs_full_orders_r1_B=rho * delta(r1) * m - k,
    margin_obs_full_orders_r2_B=rho * delta(r2) * m - k,
    margin_obs_weak_r0_B=k - delta(r0),
    margin_obs_neutral_r1_B=cost - profit(r1, lift("1/2")),
    rF_check_B=rF, rS_p5_B=rS, rN_check_B=rN,
    margin_obs_rF_B=r155-rF, margin_obs_rN_B=rN-r165,
    margin_obs_lowsell_r165_B=k - rho * delta(r165) / 2,
    margin_obs_buy_r155_B=delta(r155) * m - k,
    margin_obs_buy_recruit_r165_B=profit(r165, M) - cost,
    theta_lo=2 * threshold(r1) - 1, theta_hi=2 * threshold(r2) - 1,
    own_p5_r1_B=o1["high_ownership"], entry_floor_obs=rho,
    entry_plateau_B=o1["total_entry"], entry_jump_B=o1["total_entry"] - rho,
    entry_r2_obs_B=o2["total_entry"], ba_class_r1_B=class1, ba_entry_r1_B=entry1,
    ba_r1_B=o1["spread"], ba_share_r1_B=entry1 / o1["spread"],
    ba_ratio_r1_B=o1["spread"] / class1,
    impact_sell_r1_B=o1["sell_impact"], impact_buy_r1_B=o1["buy_impact"],
    impact_asym_r1_B=o1["buy_impact"] - o1["sell_impact"],
    ba_r2_B=o2["spread"], impact_sell_r2_B=o2["sell_impact"],
    pbar_r1_B=o1["mean_price"], p_neutral_r1_B=o1["price"][0],
    pdrop_neutral_r1_B=o1["price"][0] - o1["mean_price"],
    pdrop_neutral_r2_B=o2["price"][0] - o2["mean_price"],
    ba_rC_left_B=leftC["spread"], ba_rC_right_B=rightC["spread"],
    ba_jump_rC_B=leftC["spread"] - rightC["spread"],
    pbar_jump_rC_B=rightC["mean_price"] - leftC["mean_price"],
    alt_lambda_B=alt_lam, alt_beta_B=alt_beta, alt_theta_B=alt_lam/v,
    alt_ba_r1_B=alt["spread"], alt_entry_r1_B=alt["total_entry"],
    theta_min_counts_B=(3*v-2)/v,
    imb_buy_B=oU[160]["mean_order"],
    theta_buy_B=(lam/2)/oU[160]["volume"],
    theta_buy_pct_B=(lam/2)/oU[160]["volume"],
    U_entry_B=oU[160]["total_entry"],
    ba_U_r160_B=oU[160]["spread"],
    U_gap_r160_B=oU[160]["price"][-1]-oU[160]["price"][0],
    U_mu0_B=oU[160]["posterior"][0], U_sell_mu_B=oU[160]["posterior"][-1],
    ba_U_r155_B=oU[155]["spread"], ba_U_r165_B=oU[165]["spread"],
)
for tag, outcome in (("r1", o1), ("r2", o2)):
    values[f"wgap_{tag}_B"] = outcome["winner"][1] - outcome["winner"][-1]
    values[f"cov_entry_{tag}_B"] = outcome["cov_entry"]
    values[f"cov_win_{tag}_B"] = outcome["cov_winner"]
    values[f"win_prob_{tag}_B"] = outcome["total_winner"]
    for q, direction in ((-1, "sale"), (0, "neutral"), (1, "buy")):
        values[f"wprep_{'sell' if q == -1 else direction}_{tag}_B"] = outcome["winner"][q]
        values[f"price_{tag}_{direction}_B"] = outcome["price"][q]
        values[f"evA_{tag}_{direction}_B"] = outcome["prepared_change"][q]
        if tag == "r2" or q != 1:
            values[f"evAr_{tag}_{direction}_B"] = outcome["prepared_change"][q] / outcome["price"][q]
            values[f"evN_{tag}_{direction}_B"] = outcome["absent_change"][q]
            values[f"evNr_{tag}_{direction}_B"] = outcome["absent_change"][q] / outcome["price"][q]


def rounded_endpoint(value, quantum):
    result = Decimal(mp.nstr(value, 110)).quantize(quantum, rounding=ROUND_HALF_EVEN)
    return abs(result) if result == 0 else result


def main():
    print("XP5 independent reconstruction; rational Taylor enclosure and 90-digit interval arithmetic")
    print(f"UTC {datetime.now(timezone.utc).isoformat()}")
    print(f"Python {platform.python_version()}; mpmath {mpmath.__version__}")
    print(f"Taylor degree {N}; exact tail bound {e_tail}")
    show("e", E)
    sources = [TEAM / "proofs/P5_observables.tex", TEAM / "memos/P5_observables.md",
               TEAM / "registry/P5_observables.csv", TEAM / "scripts/P5_observables/p5_observables.py",
               TEAM / "proofs/P1_core.tex", TEAM / "BRIEF.md", Path(__file__).resolve()]
    source_hashes = {source: hashlib.sha256(source.read_bytes()).hexdigest() for source in sources}
    for source, digest in source_hashes.items():
        print(f"SHA256 {source.relative_to(TEAM)} {digest}")
    registry = list(csv.DictReader((TEAM / "registry/P5_observables.csv").open()))
    comparison = []
    with localcontext() as ctx:
        ctx.prec = 140
        for index, row in enumerate(registry, 1):
            key = row["key"]
            if key not in values:
                comparison.append(dict(row=index, key=key, verdict="open", note="No independent formula"))
                continue
            actual = values[key]
            lower, upper = bounds(actual)
            percent = row["display"].endswith(r"\%")
            raw_display = row["display"].replace(r"\%", "")
            display_decimal = Decimal(raw_display)
            quantum = Decimal(1).scaleb(display_decimal.as_tuple().exponent)
            scale = 100 if percent else 1
            rounded_lo = rounded_endpoint(lower * scale, quantum)
            rounded_hi = rounded_endpoint(upper * scale, quantum)
            verdict = "confirmed" if rounded_lo == display_decimal == rounded_hi else "differs"
            reported = lift(row["value"])
            difference = actual - reported
            comparison.append(dict(row=index, key=key, verdict=verdict, display=row["display"],
                                   recomputed=interval_text(actual), value_delta=interval_text(difference),
                                   display_lo=str(rounded_lo), display_hi=str(rounded_hi), note=row["note"]))
    with (HERE / "registry_recompute.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["row", "key", "verdict", "display", "recomputed", "value_delta", "display_lo", "display_hi", "note"])
        writer.writeheader()
        writer.writerows(comparison)
    for row in comparison:
        print(f"ROW {row['row']:03} {row['key']}: {row['verdict']} display={row.get('display')} interval={row.get('recomputed')}")
    print(f"Registry rows {len(registry)}; confirmed {sum(r['verdict']=='confirmed' for r in comparison)}; other {sum(r['verdict']!='confirmed' for r in comparison)}")
    print(f"Unused independent keys: {sorted(set(values)-{r['key'] for r in registry})}")
    print("\nFixed candidate payoffs, in order -1, 0, 1")
    hidden = [("hidden N r0", candidate(r0, lift(0), lift(0), hidden=True)),
              ("hidden F r1", candidate(r1, lift(1), lift(1), hidden=True)),
              ("hidden F r2", candidate(r2, lift(1), lift(1), hidden=True))]
    for label, outcome in (("N r0", o0), ("F r1", o1), ("F r2", o2), *((f"U {tag}", out) for tag, out in oU.items()), *hidden):
        for class_name in ("high", "low"):
            for q in (-1, 0, 1):
                show(f"{label} {class_name} q={q}", outcome[f"{class_name}_payoff"][q])
        for q in (-1, 0, 1):
            expected_change = outcome["entry"][q] * outcome["prepared_change"][q] + (1 - outcome["entry"][q]) * outcome["absent_change"][q]
            show(f"{label} mean announcement change x={q}", expected_change)
    print("\nAdditional strict margins and corrections")
    for label, number in (("M-5/8", M-lift("5/8")), ("rC-rS", rC-rS), ("rC-rN", rC-rN), ("10-rS", 10-rS),
                          ("u-82/59", u-lift("82/59")), ("rS-2.124148", rS-lift("2.124148")),
                          ("rho Delta(2.1241481) m-k", rho*delta(lift("2.1241481"))*m-k),
                          ("counts full-equilibrium upper theta at r1", 1-2*k/(rho*delta(r1))),
                          ("counts full-equilibrium upper theta at r2", 1-2*k/(rho*delta(r2)))):
        show(label, number)
    for rr in (lift(4), lift(5)):
        oc = candidate(rr, lift(1), lift(1))
        show(f"entry component at r={mp.nstr(bounds(rr)[0],2)}", oc["spread"]-rho*delta(rr)*theta)
    # The full-order law at theta=0.9 fits the counts but fails low-class optimality.
    bad_theta = lift("9/10")
    bad_lam = v * bad_theta
    bad_beta = (v-bad_lam)/(2*(1-bad_lam))
    bad = candidate(r1, lift(1), lift(1), presence=bad_lam, liquidity=bad_beta)
    show("theta .9 beta", bad_beta)
    show("theta .9 full-order low sale payoff at r1", bad["low_payoff"][-1])
    print("\nChallenger mixture at its threshold, r=1.60")
    tau = threshold(r160)
    s = b*(2*tau-1)/(1-tau)
    alpha = s/lam
    e_mix = k/(delta(r160)*(1-tau))
    mixed = candidate(r160, alpha, lift(0), buy_entry=e_mix)
    for label, number in (("H purchase probability", alpha), ("buy posterior minus tau", mixed["posterior"][1]-tau),
                          ("entry after buy", e_mix), ("entry-rho", e_mix-rho), ("1-entry", 1-e_mix),
                          ("H buy payoff", mixed["high_payoff"][1]), ("L sale payoff", mixed["low_payoff"][-1])):
        show(label, number)
    print("\nIdentification from independent execution prices")
    theta_hat = 2*o1["sell_impact"]/(rho*delta(r1))
    lambda_hat = o1["volume"]*theta_hat
    beta_hat = (o1["volume"]-lambda_hat)/(2*(1-lambda_hat))
    for label, number in (("theta reconstruction error", theta_hat-theta),
                          ("lambda reconstruction error", lambda_hat-lam), ("beta reconstruction error", beta_hat-beta)):
        show(label, number)
    print("\nAnnouncement samples conditional on preparation")
    for tag, outcome in (("r1", o1), ("r2", o2)):
        weighted_dollar = sum((outcome["freq"][q]*outcome["entry"][q]*outcome["prepared_change"][q] for q in (-1,0,1)), lift(0))
        weighted_return = sum((outcome["freq"][q]*outcome["entry"][q]*outcome["prepared_change"][q]/outcome["price"][q] for q in (-1,0,1)), lift(0))
        show(f"{tag} mean dollar change conditional on A", weighted_dollar/outcome["total_entry"])
        show(f"{tag} mean return conditional on A", weighted_return/outcome["total_entry"])
    print("\nExact rational source values at calibration A")
    # Direct substitution in the class cash flows; these values need no exponential constant.
    la, be, ro = F(6,17), F(1,3), F(1,4)
    ba = (1-la)*be
    ma, da, th = (ba+la)/(2*ba+la), ba+la/2, la/(2*ba+la)
    for r in (F(3), F(18,5)):
        t0, tH, tL = F(1,2)*(1-F(1,2)/r), r/2+F(1,8)/r, 1-F(3,8)/r
        D = tH-tL
        J = int((1-ma)*(1-tL)+ma*(10-tH) >= 6)
        A = {"sale":tL-t0+D*(1-ma), "neutral":tL-t0+D/2, "buy":tL-t0+D*ma}
        entry = {"sale":ro,"neutral":ro,"buy":ro+(1-ro)*J}
        prices = {name:t0+entry[name]*a for name,a in A.items()}
        spread = prices["buy"]-prices["sale"]
        print(f"A r={r}: M={ma}, theta={th}, volume={2*da}, spread={spread}, entry share={(1-ro)*J*A['buy']/spread}")
        print(f"A r={r}: class component={ro*D*th}, total entry={ro+(1-ro)*J*da}")
        print(f"A r={r}: winner gap={th*(1-1/r)}, Pbar={t0+ro*A['neutral']+(1-ro)*J*da*A['buy']}, neutral change={-(1-ro)*J*da*A['buy']}")
        print(f"A r={r}: prepare changes={[(1-entry[name])*A[name] for name in ('sale','neutral','buy')]}")
        print(f"A r={r}: entry covariance={da*(1-ro)*J}, winner covariance={da*(entry['buy']*(ma+(1-ma)/r)-ro*((1-ma)+ma/r))}")
    print(f"A buy-only: volume={2*ba+la/2}, informed share={(la/2)/(2*ba+la/2)}, mean order={la/2}")
    print("\nEnd-of-run source hashes")
    for source, digest in source_hashes.items():
        current = hashlib.sha256(source.read_bytes()).hexdigest()
        print(f"SOURCE {source.relative_to(TEAM)} unchanged={current == digest}")
    output = HERE / "registry_recompute.csv"
    print(f"OUTPUT SHA256 {output.name} {hashlib.sha256(output.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()
