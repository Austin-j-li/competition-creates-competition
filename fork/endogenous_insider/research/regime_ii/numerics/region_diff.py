"""Compare the threshold solvers with the cutoff scan, point by point. Prints the disagreements; writes nothing.

For every scan point in summary_region.csv: below c_L* the scan should find the reversal in all equilibria; at or above
c_L* it should find a break. A scan point that disagrees is either a window narrower than the cutoff step, a pool the
scan cannot see (islands), or a gap in a threshold solver. Each case is listed for inspection.
"""
import csv
import math

th = list(csv.DictReader(open("thresholds.csv")))
sm = list(csv.DictReader(open("summary_region.csv")))


def f(x):
    try:
        return float(x)
    except ValueError:
        return math.nan


bad = []
tot = ok = 0
for t in th:
    r1, rho, cs = f(t["r1"]), t["rho"], f(t["cL_star"])
    for s in sm:
        if s["rho"] != rho or abs(f(s["r"]) - r1) > 1e-9 or s["regime"] == "I":
            continue
        c = f(s["cL"])
        rev = s["reversal_all"] == "true"
        holds_pred = math.isnan(cs) or c < cs - 1e-9
        tot += 1
        if holds_pred == rev:
            ok += 1
        else:
            bad.append((rho, r1, round(c, 4), round(cs, 4) if not math.isnan(cs) else "nan", t["binding"],
                        "scan holds" if rev else "scan breaks", s["n_eq"], s["n_unresolved"]))
print("regime II scan points", tot, "agree", ok, "disagree", len(bad))
for b in bad:
    print(b)
