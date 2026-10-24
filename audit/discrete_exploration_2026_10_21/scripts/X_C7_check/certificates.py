"""Finite rational enclosures and deviations; print results only."""

from fractions import Fraction as F
from pathlib import Path
import mpmath as mp

mp.mp.dps = 70
LINES = []


class Band:
    def __init__(self, lo, hi=None):
        self.lo = F(lo)
        self.hi = self.lo if hi is None else F(hi)

    def __add__(self, other):
        other = as_band(other)
        return Band(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return Band(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + (-as_band(other))

    def __rsub__(self, other):
        return as_band(other) + (-self)

    def __mul__(self, other):
        other = as_band(other)
        values = [self.lo * other.lo, self.lo * other.hi, self.hi * other.lo, self.hi * other.hi]
        return Band(min(values), max(values))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = as_band(other)
        return self * Band(1 / other.hi, 1 / other.lo)

    def __rtruediv__(self, other):
        return as_band(other) / self


def as_band(value):
    return value if isinstance(value, Band) else Band(value)


def show(label, value):
    value = as_band(value)
    convert = lambda x: mp.nstr(mp.mpf(x.numerator) / x.denominator, 58)
    text = f"{label} [{convert(value.lo)}, {convert(value.hi)}] positive={value.lo > 0} negative={value.hi < 0}"
    print(text)
    LINES.append(text)


term, total = F(1), F(1)
odd, even = F(0), F(1)
for index in range(1, 91):
    term *= F(-1, 2 * index)
    total += term
    if index % 2:
        odd = total
    else:
        even = total
a = Band(odd, even)
bad, good = a / (1 + a), 1 / (1 + a)
rho, h, ell, p, cost, r, k = map(F, (".25", "10", "1", ".5", "5", "3", ".02"))


def gross(mu, cut):
    return mu * (h - (cut + r) / 2) + (1 - mu) * (ell - cut) * (ell - cut) / (2 * (r - cut))


lo = F("0.93590073908012834872292351338292634245041815586720")
hi = F("0.93590073908012834872292351338292634245041815586721")
cut = Band(lo, hi)
show("EXP_NEG_HALF", a)
show("WEAK_STRENGTH_MARGIN", k - F(1, 60))
show("PRIOR_NO_ENTRY_MARGIN_R3", cost - F(103, 24))
show("CONDITION_N_MARGIN", cost - 8 * good)
show("BID_INTERIOR_MARGIN", gross(good, p) - cost)
show("CUTOFF_LOWER_SIGN", gross(good, lo) - cost)
show("CUTOFF_UPPER_SIGN", gross(good, hi) - cost)
show("FULL_PURCHASE_MARGIN", bad * rho * F(2, 3) / (1 + rho) - k)
show("ENTRY_R3", rho + (1 - rho) * cut / (2 * r))
show("OWNERSHIP_R3", rho / 2 + (1 - rho) * good * cut / (2 * r))
show("PREEMPTION_R3", (1 - cut / r) / 2)
loss = (1 - rho) * ((ell - cut) * (ell - cut) / 2 + good * (r * r - ell * ell) / 2 + ((1 - good) * ell - cut) * (r - ell)) / (2 * r)
show("PROCEEDS_LOSS_R3", loss)
show("ALTERNATIVE_BID_ENTRY_R3", Band(rho + (1 - rho) * ell / (2 * r)))
show("ALTERNATIVE_BID_OWNERSHIP_R3", rho / 2 + (1 - rho) * good * ell / (2 * r))
show("ALTERNATIVE_BID_SURPLUS_INCREMENT_R3", (1 - rho) * (1 - ell / r) * (cost - 8 * good) / 2)
show("ALTERNATIVE_WEAK_ENTRY", rho + (1 - rho) * p / F(6, 5))
ceiling = Band("3.98609657163840441876587802420118742637846223232605", "3.98609657163840441876587802420118742637846223232606")
for label, strength in (("CEILING_LOWER_SIGN", ceiling.lo), ("CEILING_UPPER_SIGN", ceiling.hi)):
    prior_gain = good * h - good * strength / 2 + ((1 - good) * ell * ell - p * p) / (2 * strength)
    show(label, prior_gain - cost)
show("ENTRY_AT_EXACT_CEILING", rho + (1 - rho) * p / (2 * ceiling))

# Exact deviation from silence at a feasible public posterior.
mu, bid = F(3, 5), F(2)
survivor = ell + (bid - ell) * (1 - rho * mu) / (mu * (1 - rho))
show("SILENCE_DEVIATION_CUTOFF", survivor)
show("SILENCE_DEVIATION_RECEIVER_GAIN", mu * (h - survivor))
show("SILENCE_DEVIATION_RECEIVER_COST_MARGIN", cost - mu * (h - survivor))
show("SILENCE_DEVIATION_BELIEF_FREE_COST_MARGIN", cost - mu * (h - bid))
show("SILENCE_DEVIATION_SENDER_GAIN_AT_R3", (r - bid) * (1 - rho * mu) - (1 - mu) * (r - ell))
mu, lower_bid = F(11, 20), F(99, 100)
show("LARGE_BID_CONTINUUM_COUNTEREXAMPLE_GROSS_UPPER", mu * h + (1 - mu) * ell - lower_bid)
show("LARGE_BID_CONTINUUM_COUNTEREXAMPLE_SENDER_GAIN", (1 - rho) * (ell - lower_bid))

# A false separating lockup menu permits a stronger type to copy a lower offer.
show("LOCKUP_MIMIC_GAIN", F(3, 2) - F(1))

# Two rational cutoff values give opposite profit signs in Case C.
r = F(8, 5)
gap = (r - ell) * (r - ell) / (2 * r)
for cut in (F(13, 10), F(7, 5)):
    mu = cost / (h - (cut + r) / 2)
    bid = ell + (cut - ell) * mu * (1 - rho) / (1 - rho * mu)
    beta = a * (2 * mu - 1) / ((1 - a) * (1 - mu))
    mb = (1 - beta * (1 - a)) / (2 - beta * (1 - a))
    spread = ((cut - ell) ** 2 + rho * ((r - bid) ** 2 - (cut - bid) ** 2)) / (2 * r)
    profit = bad * (1 - mb) * rho * gap + good * (1 - mu) * spread - k
    show(f"MIXTURE_BETA_AT_CUTOFF_{cut}", beta)
    show(f"MIXTURE_PROFIT_AT_CUTOFF_{cut}", profit)

(Path(__file__).resolve().parent / "rational_output.txt").write_text("\n".join(LINES) + "\n")
