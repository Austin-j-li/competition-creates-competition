"""Print calculations for the mathematical review. No acceptance predicates."""

from __future__ import annotations

import hashlib
import math
import subprocess
from pathlib import Path

from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import expit, logsumexp
from scipy.stats import t as student


ROOT = Path(__file__).resolve().parents[4]
CLONE = ROOT / "overleaf/paper-revision"


def payoffs(r: float, p: float = 0.5, ell: float = 1.0,
            h: float = 10.0) -> dict[str, float]:
    t0 = p * (1 - p / r)
    th = r / 2 + p * p / (2 * r)
    gl = (ell * ell - p * p) / (2 * r)
    tl = ell - gl
    return {"t0": t0, "th": th, "tl": tl, "gh": h - th,
            "gl": gl, "delta": th - tl}


def gross(v: dict[str, float], belief: float) -> float:
    return v["gl"] + belief * (v["gh"] - v["gl"])


def bounds(prior: float, b: float = 2.0) -> tuple[float, float, float]:
    odds = math.log(prior / (1 - prior))
    low, high = expit(odds - 2 / b), expit(odds + 2 / b)
    return low, high, min(low, 1 - high)


def laplace_sf(z: float, b: float = 2.0) -> float:
    return 0.5 * math.exp(-z / b) if z >= 0 else 1 - 0.5 * math.exp(z / b)


def log_density(x: float, law: str, b: float = 2.0) -> float:
    if law == "Laplace":
        return -math.log(2 * b) - abs(x) / b
    if law == "logistic":
        z = -abs(x / b)
        return z - math.log(b) - 2 * math.log1p(math.exp(z))
    if law == "sech":
        z = abs(x / b)
        return -math.log(math.pi * b) - z + math.log(2) - math.log1p(math.exp(-2 * z))
    scale = b * 4 / (2 * math.sqrt(3))
    return float(student.logpdf(x, df=3, scale=scale))


def posterior(x: float, law: str, prior: float = 0.5) -> float:
    return float(expit(math.log(prior / (1 - prior))
                       + log_density(x - 1, law) - log_density(x + 1, law)))


def integrate_piecewise(fn, points: list[float]) -> float:
    ordered = [-math.inf] + sorted(set(points)) + [math.inf]
    return sum(quad(fn, left, right, epsabs=1e-12, epsrel=1e-12)[0]
               for left, right in zip(ordered, ordered[1:]))


def threshold(cost: float, law: str, v: dict[str, float],
              prior: float = 0.5) -> float:
    tau = (cost - v["gl"]) / (v["gh"] - v["gl"])
    return brentq(lambda x: posterior(x, law, prior) - tau, -50, 50)


def benchmark() -> None:
    print("BENCHMARK PAYOFFS AND ENTRY")
    rho, k, b, cost = 0.25, 0.02, 2.0, 6.0
    m, M, _ = bounds(0.5)
    for r in (1.2, 1.55, 1.60, 1.65, 3.0, 3.6):
        v = payoffs(r)
        print(f"r={r:.2f} delta={v['delta']:.12f} B(prior)={gross(v, .5):.12f} "
              f"B(m)={gross(v, m):.12f} B(M)={gross(v, M):.12f} "
              f"no-trade margin={k-rho*v['delta']/2:.12f}")
    v = payoffs(3.0)
    tau = (cost - v["gl"]) / (v["gh"] - v["gl"])
    print(f"strong threshold belief={tau:.12f}")
    profits = {}
    alpha = {}
    for law in ("Laplace", "logistic"):
        star = threshold(cost, law, v)
        if law == "Laplace":
            ah, al = laplace_sf(star - 1), laplace_sf(star + 1)
        else:
            ah, al = expit(-(star - 1) / b), expit(-(star + 1) / b)
        alpha[law] = (ah, al)
        entry = rho + (1 - rho) * (ah + al) / 2
        print(f"{law}: x*={star:.12f} alpha_H={ah:.12f} alpha_L={al:.12f} "
              f"entry={entry:.12f}")
        atomless_points = [-1.0, 1.0, threshold(5.9, law, v), threshold(6.1, law, v)]
        def atomless_integrand(x):
            high_fraction = min(1.0, max(0.0, (gross(v, posterior(x, law)) - 5.9) / .2))
            e = rho + (1 - rho) * high_fraction
            return e * (math.exp(log_density(x - 1, law))
                        + math.exp(log_density(x + 1, law))) / 2
        print(f"{law}: atomless-cost entry="
              f"{integrate_piecewise(atomless_integrand, atomless_points):.12f}")
        if law == "Laplace":
            for regime in ("access", "hidden"):
                def pi_integrand(x):
                    lh, ll = log_density(x - 1, law), log_density(x + 1, law)
                    e = rho + (1 - rho) * (x >= star) if regime == "access" else rho
                    return v["delta"] * e * math.exp(lh + ll - float(logsumexp([lh, ll])))
                profits[regime] = integrate_piecewise(pi_integrand, [-1.0, star, 1.0])
    ah, al = alpha["Laplace"]
    gain = (1 - rho) * ((v["th"] - v["t0"]) * ah
                        + (v["tl"] - v["t0"]) * al) / 2
    weak = payoffs(1.2)
    omega_u = 2 * b * ((1 - 1 / b) * rho * m * v["delta"] - k) / ((1 - rho) * (v["th"] - v["t0"]))
    omega_0 = 2 * b * (k - weak["delta"]) / ((1 - rho) * (weak["th"] - weak["t0"]))
    print(f"gross profit with access={profits['access']:.12f}")
    print(f"gross profit with hidden prices={profits['hidden']:.12f}")
    print(f"proceeds gain={gain:.12f}; gain/profit={gain/profits['access']:.12f}")
    print(f"Omega_U={omega_u:.12f}; Omega_0={omega_0:.12f}")
    eh, el = rho+(1-rho)*ah, rho+(1-rho)*al
    allocation_without = (3.0**2-.5**2)/(2*3.0)
    surplus_feedback = allocation_without + (eh*(v["gh"]+.5**2/3)+el*(v["gl"]+.5**2/3))/2
    surplus_feedback -= cost*(1-rho)*(ah+al)/2
    surplus_hidden = allocation_without + rho*(v["gh"]+v["gl"]+2*.5**2/3)/2
    print(f"net acquisition surplus with access={surplus_feedback:.12f}")
    print(f"net acquisition surplus with hidden prices={surplus_hidden:.12f}")
    print("ADDITIONAL NOISE LAWS AT FULL ORDERS")
    for law in ("sech", "Student"):
        if law == "sech":
            lo = threshold(cost, law, v)
            ah = 2 / math.pi * math.atan(math.exp(-(lo - 1) / b))
            al = 2 / math.pi * math.atan(math.exp(-(lo + 1) / b))
            interval = f"[{lo:.12f}, infinity)"
        else:
            nu, scale = 3, b * 4 / (2 * math.sqrt(3))
            w = (tau / (1 - tau)) ** (2 / (nu + 1))
            aa = w - 1
            bb = -2 * (w + 1)
            cc = (w - 1) * (1 + nu * scale * scale)
            root = math.sqrt(bb * bb - 4 * aa * cc)
            lo, hi = (-bb - root) / (2 * aa), (-bb + root) / (2 * aa)
            ah = student.cdf(hi - 1, nu, scale=scale) - student.cdf(lo - 1, nu, scale=scale)
            al = student.cdf(hi + 1, nu, scale=scale) - student.cdf(lo + 1, nu, scale=scale)
            interval = f"[{lo:.12f}, {hi:.12f}]"
        print(f"{law}: entry set={interval}; "
              f"entry={rho+(1-rho)*(ah+al)/2:.12f}")


def atomless_scope() -> None:
    print("ATOMLESS-COST STATEMENT AT A DIFFERENT PRIOR")
    r0, r1, prior, cost, eps, rho, k = 1.05, 3.0, .7, 6.0, .1, .25, .005
    weak, strong = payoffs(r0), payoffs(r1)
    m, M, _ = bounds(.5)
    mp, Mp, kp = bounds(prior)
    print(f"r0={r0}, r1={r1}, prior={prior}, c_H={cost}, epsilon_C={eps}, rho={rho}, k={k}")
    print(f"printed low support: {2*eps:.12f} < B_r1(m)={gross(strong, m):.12f}")
    print(f"printed high window: B_r0(1/2)={gross(weak,.5):.12f} < "
          f"{cost-eps:.12f} < {cost+eps:.12f} < B_r1(M)={gross(strong,M):.12f}")
    print(f"general order window: delta_r0={weak['delta']:.12f} < {k:.12f} < "
          f"{.5*rho*kp*strong['delta']:.12f}")
    print(f"actual weak prior profit={gross(weak,prior):.12f}; high support upper={cost+eps:.12f}")
    print("The unique weak order is zero, and every cost realization prepares: entry=1.")
    print(f"actual posterior bounds: m(pi)={mp:.12f}, M(pi)={Mp:.12f}")


def welfare_scope() -> None:
    print("WELFARE WITH MASS BELOW THE RESERVE")
    rho, p, r1, c, k, admissible = .25, .5, 3.0, 3.0, .01, .5
    m, M, _ = bounds(.5)
    weak, strong = payoffs(1.2), payoffs(r1)
    print("G_L=(delta_0+delta_1)/2; G_H=(delta_0+delta_10)/2; prior=1/2")
    print(f"cost window: {.5*gross(weak,.5):.12f} < {c:.12f} < {.5*gross(strong,M):.12f}")
    print(f"order window: {.5*weak['delta']:.12f} < {k:.12f} < {.5*rho*m*.5*strong['delta']:.12f}")
    tau = (c - .5 * strong["gl"]) / (.5 * (strong["gh"] - strong["gl"]))
    star = math.log(tau / (1 - tau))
    def integrand(x, admission):
        mixture = (math.exp(log_density(x-1,"Laplace")) + math.exp(log_density(x+1,"Laplace"))) / 2
        return (1-rho) * mixture * (.5*gross(strong,posterior(x,"Laplace"))-c+p*p/r1*admission)
    actual = quad(lambda x: integrand(x, admissible), star, 1, epsabs=1e-12)[0]
    actual += quad(lambda x: integrand(x, admissible), 1, math.inf, epsabs=1e-12)[0]
    printed = quad(lambda x: integrand(x, 1.0), star, 1, epsabs=1e-12)[0]
    printed += quad(lambda x: integrand(x, 1.0), 1, math.inf, epsabs=1e-12)[0]
    print(f"actual allocation surplus gain={actual:.12f}")
    print(f"formula (A.41) as printed={printed:.12f}; excess={printed-actual:.12f}")


def many_classes() -> None:
    print("THREE-CLASS STRICT REGION")
    priors, values = (.25, .25, .5), (.99, 1.01, 10.0)
    m, M, _ = bounds(.5)
    for r in (1.2, 3.0):
        t = [val - (val*val-.25)/(2*r) if val < r else r/2+.25/(2*r) for val in values]
        g = [val-tv for val, tv in zip(values, t)]
        candidates = []
        for mask in range(8):
            weights = [priors[i] * (math.e if mask & (1 << i) else 1) for i in range(3)]
            candidates.append(sum(w*tv for w, tv in zip(weights,t))/sum(weights))
        gamma = min(min(candidates)-max(t[:2]), t[2]-max(candidates))
        print(f"r={r}: t={t}; g={g}; prior profit={sum(w*gv for w,gv in zip(priors,g)):.12f}; "
              f"range={max(t)-min(t):.12f}; gamma={gamma:.12f}; ")
        if r == 3:
            print(f"strong marginal bound={.5*.25*gamma:.12f}; high-group upper profit="
                  f"{(g[0]+g[1])*(1-M)/2+g[2]*M:.12f}; k=.02, c_H=6")


def source_receipt() -> None:
    print("SOURCE RECEIPT")
    print(subprocess.run(["git", "-C", str(CLONE), "rev-parse", "HEAD"],
                         text=True, capture_output=True).stdout.strip())
    for name in ("main.tex", "online_appendix.tex"):
        print(f"{name}: sha256={hashlib.sha256((CLONE/name).read_bytes()).hexdigest()}")


if __name__ == "__main__":
    source_receipt()
    benchmark()
    atomless_scope()
    welfare_scope()
    many_classes()
