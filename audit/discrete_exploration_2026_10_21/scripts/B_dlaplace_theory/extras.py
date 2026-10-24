"""Two print-only diagnostics for memos/B_dlaplace_theory.md.

1. A prior above one half: the purchase payoff on the entry-rho piece is U-shaped in s, so one
   piece can carry two mixed equilibria. Brute force (direct flow sums) vs the analytic quadratic.
2. Robustness of the structure to the noise law: the discrete-Laplace law, a perturbed law that is
   not geometric on each half-line, and a discretized Gaussian law with the same variance.
   For each law: posterior spread on each half-line under full purchases, the no-trade payoff K_0,
   the full-purchase payoff K_F, and the equilibrium list at four strengths.
Nothing is asserted.

Run from the repository root (through the slot wrapper):
    bash audit/discrete_exploration_2026_10_21/scripts/_slots/run_slot.sh .venv/bin/python \
        audit/discrete_exploration_2026_10_21/scripts/B_dlaplace_theory/extras.py
"""
import importlib.util
import pathlib
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("corr", HERE / "correspondence.py")
corr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(corr)


class GeneralNoise(corr.Model):
    """Same brute-force routines, any positive noise law on the integers |z| <= X."""

    def __init__(self, pmf, pi, lam, cH, rho, k, X=90, label=""):
        super().__init__(pi, lam, 2.0, cH, rho, k, X)
        z = np.arange(-X - 1, X + 2)
        w = pmf(z.astype(float))
        w = w / w.sum()
        lookup = dict(zip(z.tolist(), w.tolist()))
        self.f0 = np.array([lookup[int(x)] for x in self.x])
        self.f1 = np.array([lookup[int(x) - 1] for x in self.x])
        self.label = label


def main():
    print("=== 1. Prior 0.7: two mixed roots on the entry-rho piece ===")
    cH = corr.window_mid(0.7, 2.0)
    for k in [0.0632, 0.0620, 0.0640]:
        m = corr.Model(0.7, 1.0, 2.0, cH, 0.25, k)
        r = 3.5
        eb, _ = m.brute(r, ns=4001)
        ea, ss = m.analytic(r)
        o = corr.auction(r)
        tau = (cH - o["gL"]) / (o["gH"] - o["gL"])
        Kmin = m.K_closed(r, 1 / (2 * m.pi), 0.25)
        print(f"  r={r}, k={k}: tau={tau:.6f} > M1(0.7)={m.mu_up(1.0):.6f} (no recruitment);"
              f" K_rho(0)={m.K_closed(r, 0.0, 0.25):.6f}, min K_rho at s=1/(2 pi): {Kmin:.6f}, K_rho(1)={m.K_closed(r, 1.0, 0.25):.6f}")
        print(f"     brute:    {[(e[0], round(e[1], 6)) for e in eb]}")
        print(f"     analytic: {[(e[0], round(e[1], 6)) for e in ea]}")

    print("\n=== 2. Robustness of the structure to the noise law (pi = 1/2, lam = 1, c_H = 5, k = 0.02) ===")
    a = np.exp(-0.5)
    var = 2 * a / (1 - a) ** 2
    laws = [
        ("discrete Laplace", lambda z: a ** np.abs(z)),
        ("perturbed: a^|z| (1 + 0.1 cos z)", lambda z: a ** np.abs(z) * (1 + 0.1 * np.cos(z))),
        ("perturbed: a^|z| (1 + 0.3 cos z)", lambda z: a ** np.abs(z) * (1 + 0.3 * np.cos(z))),
        (f"discretized Gaussian, variance {var:.4f}", lambda z: np.exp(-z * z / (2 * var))),
    ]
    for name, pmf in laws:
        m = GeneralNoise(pmf, 0.5, 1.0, 5.0, 0.25, 0.02, label=name)
        mu = m.post(np.array([1.0]))[0]
        up, dn = mu[m.x >= 1], mu[m.x <= 0]
        print(f"\n  {name}")
        print(f"     full purchases: posterior on x>=1 in [{up.min():.6f}, {up.max():.6f}], on x<=0 in [{dn.min():.6f}, {dn.max():.6f}]")
        ratio = m.f1 / m.f0
        print(f"     one-step ratio f(x-1)/f(x): on x>=1 in [{ratio[m.x >= 1].min():.4f}, {ratio[m.x >= 1].max():.4g}],"
              f" on x<=0 in [{ratio[m.x <= 0].min():.4g}, {ratio[m.x <= 0].max():.4f}]")
        for r in [1.2, 1.6, 3.0, 4.2, 6.0]:
            K0 = m.K_direct(r, np.array([0.0]))[0][0]
            KF = m.K_direct(r, np.array([1.0]))[0][0]
            eb, _ = m.brute(r, ns=2001)
            mu1 = m.post(np.array([1.0]))[0]
            ent = m.entry_of(r, mu1)
            E = np.sum(0.5 * (m.f0 + m.f1) * ent)
            print(f"     r={r}: K_0={K0:.6f} (rho D/2={0.125 * corr.auction(r)['D']:.6f}), K_F={KF:.6f};"
                  f" entry under full purchases {E:.6f}; equilibria {[(e[0], round(e[1], 4)) for e in eb]}")


if __name__ == "__main__":
    main()
