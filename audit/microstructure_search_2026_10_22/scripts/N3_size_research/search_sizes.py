"""Print-only float search: both full posteriors below tau(3.6).

Looks for a full mix at 1.55, 1.60, 1.65 with exactly one recruiting
size and rising entry, plus clean outcomes at 3 and 3.6.
"""
import sys

sys.path.insert(0, "audit/microstructure_search_2026_10_22/scripts/N3_size_research")
from explore_sizes import h_candidates, l_candidates, auction, RHO


def entry_of(r, lam, b1, b2, eta0, A, S):
    delta, tau = auction(r)
    rec = 0.0
    for i, bb in enumerate((b1, b2)):
        m = (bb + A[i]) / (2 * bb + A[i])
        if m >= tau:
            rec += bb + A[i] / 2
    ah0 = (1 - lam) * eta0 + lam - A[0] - A[1]
    al0 = (1 - lam) * eta0 + lam - S[0] - S[1]
    mu0 = ah0 / (ah0 + al0) if ah0 + al0 > 0 else 0.5
    if mu0 >= tau:
        rec += (ah0 + al0) / 2
    return RHO + 0.75 * rec


def main():
    hits = []
    for lam in (0.15, 0.20, 0.25, 0.28, 0.30):
        for u1 in (0.9, 1.1, 1.3, 1.45, 1.55, 1.65, 1.72):
            for u2 in (0.9, 1.1, 1.3, 1.45, 1.55, 1.65, 1.72):
                b1, b2 = lam / u1, lam / u2
                beta1, beta2 = b1 / (1 - lam), b2 / (1 - lam)
                eta0 = 1 - 2 * (beta1 + beta2)
                if eta0 < 0.03:
                    continue
                # intermediate: look for Hmix with mixed entry flags in the name
                seq = []
                ok = True
                for r in (1.55, 1.60, 1.65):
                    hs = h_candidates(r, lam, b1, b2)
                    ls = l_candidates(r, lam, b1, b2)
                    if len(ls) != 1 or ls[0][0] != "L0":
                        ok = False
                        break
                    cand = [h for h in hs if h[0].startswith("Hmix e=(1.0,0.25)") or h[0].startswith("Hmix e=(0.25,1.0)")]
                    if len(cand) != 1:
                        ok = False
                        break
                    seq.append(entry_of(r, lam, b1, b2, eta0, cand[0][1], (0.0, 0.0)))
                if not ok:
                    continue
                if not (seq[0] < seq[1] < seq[2]):
                    continue
                # strong strengths: collect entry sets
                sets = {}
                clean = True
                for r in (3.0, 3.6):
                    hs = h_candidates(r, lam, b1, b2)
                    ls = l_candidates(r, lam, b1, b2)
                    es = sorted({round(entry_of(r, lam, b1, b2, eta0, A, S), 6) for _, A in hs for _, S in ls})
                    sets[r] = es
                hits.append((lam, u1, u2, eta0, seq, sets))
    print(f"hits: {len(hits)}")
    for lam, u1, u2, eta0, seq, sets in hits[:40]:
        print(f"lam={lam} u1={u1} u2={u2} eta0={eta0:.3f} rising={[round(x,6) for x in seq]} E3={sets[3.0]} E36={sets[3.6]}")


if __name__ == "__main__":
    main()
