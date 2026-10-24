#!/usr/bin/env python3
"""Floating-point cross-check of the research-game enumeration (numerical diagnostic).

It does not use the decoupling argument or the research quadratic of xn3_research.py.
For every grid point (lam, alpha, sigma) it computes the posteriors, the entry schedule (rule C1),
every order payoff, and three deviation gains:
  - class H: best order payoff minus the payoff of its strategy (alpha on +1, rest on 0);
  - class L: the same for (sigma on -1, rest on 0);
  - research: best success probability against the fixed schedule minus the actual choice.
Wrong-signed orders are in the menu of each deviation, so their exclusion is also checked.
Grid points whose largest gain is below a tolerance are grouped into clusters and printed.
The program prints results only.
"""
import numpy as np

RHO, CH, K, P, ELL, BETA = 0.25, 6.0, 0.02, 0.5, 1.0, 1.0 / 3.0


def auction(r):
    delta = (r - ELL) ** 2 / (2 * r)
    tau = (48 * r - 3) / (4 * (20 * r - r * r - 1))
    return delta, tau


def scan(r, lam_bar, a, n_lam=3531, n_mix=101, tol=1e-8):
    delta, tau = auction(r)
    lams = np.linspace(0.0, lam_bar, n_lam)
    mix = np.linspace(0.0, 1.0, n_mix)
    hits = []
    for lam in lams:
        b = (1 - lam) * BETA
        al = mix[:, None]
        sg = mix[None, :]
        fHp, fLp = b + lam * al, b + 0 * al
        fHm, fLm = b + 0 * sg, b + lam * sg
        mup = fHp / (fHp + fLp)
        mum = fHm / (fHm + fLm)
        ep = np.where(mup >= tau, 1.0, RHO) + 0 * sg
        em = np.where(mum >= tau, 1.0, RHO)
        UHp = ep * delta * (1 - mup) - K
        UHm = -em * delta * (1 - mum) - K
        ULm = em * delta * mum - K
        ULp = -ep * delta * mup - K
        bestH = np.maximum(np.maximum(UHp, UHm), 0.0)
        bestL = np.maximum(np.maximum(ULm, ULp), 0.0)
        gainH = bestH - al * UHp
        gainL = bestL - sg * ULm
        V = (bestH + bestL) / 2
        z = np.minimum(lam_bar, V / a)
        gainR = (z * V - a * z * z / 2) - (lam * V - a * lam * lam / 2)
        if lam > 0:
            res = np.maximum(np.maximum(gainH, gainL), gainR)
        else:
            res = gainR + 0 * gainH
        idx = np.argwhere(res < tol)
        for i, j in idx:
            hits.append((lam, mix[i], mix[j], res[i, j], float(ep[i, j] if lam > 0 else RHO)))
    return hits


def cluster(hits, lam_step):
    """Group hits by contiguous lam and identical (alpha, sigma, e+)."""
    groups = {}
    for lam, al, sg, res, ep in hits:
        key = (round(al, 6), round(sg, 6), ep) if lam > 0 else ("any", "any", ep)
        groups.setdefault(key, []).append((lam, res))
    out = []
    for key, items in groups.items():
        items.sort()
        cur = [items[0]]
        for it in items[1:]:
            if it[0] - cur[-1][0] <= 1.5 * lam_step:
                cur.append(it)
            else:
                out.append((key, cur))
                cur = [it]
        out.append((key, cur))
    return out


def main():
    # (lam_bar, a, r, tol, n_mix); lam_bar = 0.9999 stands for the case without a ceiling
    cases = [(6 / 17, 1 / 40, r, 1e-8, 101) for r in (1.2, 1.55, 1.6, 1.65, 3.0, 3.6)]
    cases += [(0.9999, 1 / 40, 3.0, 1e-5, 1001), (0.9999, 1 / 40, 3.6, 1e-5, 1001),
              (0.9999, 1 / 4, 3.0, 1e-8, 101), (0.9999, 1 / 4, 3.6, 1e-8, 101)]
    for lam_bar, a, r, tol, n_mix in cases:
        n_lam = 3531 if lam_bar < 0.5 else 10000
        hits = scan(r, lam_bar, a, n_lam=n_lam, n_mix=n_mix, tol=tol)
        step = lam_bar / (n_lam - 1)
        print(f"r={r}, lam_bar={lam_bar:.6f}, a={a}, mixing grid {n_mix}: {len(hits)} grid points with all gains < {tol}")
        # collapse lam=0 hits (strategies irrelevant) and near-zero spurious points
        cl = cluster(hits, step)
        for key, items in sorted(cl, key=lambda kv: kv[1][0][0]):
            lams = [x[0] for x in items]
            best = min(items, key=lambda x: x[1])
            if key[0] == "any":
                print(f"    lam=0 (strategies irrelevant): min gain {best[1]:.2e}")
                continue
            if max(lams) < 2e-3:
                continue  # continuity artefact next to zero research
            print(f"    alpha={key[0]}, sigma={key[1]}, e+={key[2]}: lam in [{min(lams):.5f}, {max(lams):.5f}], "
                  f"best lam {best[0]:.6f} (gain {best[1]:.1e}), points {len(items)}")
        print()


if __name__ == "__main__":
    main()
