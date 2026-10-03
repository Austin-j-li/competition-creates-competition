# Research on the endogenous insider (October 2026)

This folder reopens the fork in `../mechanism.md`. The fork removes the randomness of the preparation cost. One known cost $c$ replaces the two-point cost, so the floor $\rho$ is gone. The investor's knowledge of $\theta$ is then material for the target's stock only in some equilibria.

Five tracks extend the fork. Each track has its own folder with `note.md`, code, and CSV outputs. A referee checked the four theory and numerics tracks. The referee reports are in `<track>/referee/review.md`. Referee corrections inside the notes carry the mark "[Referee fix: ...]".

Nothing here is part of the manuscript, its numerical contract, or its release gate. Status labels use the paper's vocabulary. The renderers write PDF figures. The PDFs are not committed; run each track's renderer to make them.

## Main results

### 1. The fork's open item 1 is closed

Three tracks found the same closed form for the existence statistic (F.3). Under full orders and the minimal pool,

$$
J(r)=\Delta_T\Big[\tfrac m2+\tfrac{e^{-1/b}}{2}\Big(\arctan e^{1/b}-\arctan\sqrt{\tfrac{\tau}{1-\tau}}\Big)\Big].
$$

The bound $J\ge\Delta_T m/2$ gives $(1-1/b)J(3)\ge m/6>1/24>k$. So Proposition F.3 holds at the benchmark by closed-form arithmetic (analytical). An interval enclosure gives $J(3)\in[0.0955028924240038,\,0.0955028924240039]$ (computer-assisted). Sources: `equilibrium_set/` Lemma ES.1 and Prop ES.1; `selection_design/` Lemma S.2; `cost_distribution/` Lemma CD.6.

### 2. The live region is now exact

- The F.2(c) test is also necessary. The minimal-pool full-order equilibrium exists exactly on $[r_J,r_C]$, with $r_J=2.01552$ (analytical characterization; the endpoint is computer-assisted).
- Live equilibria with $q_H=1$ exist exactly on $[r_e,r_C]$, with $r_e=1.65859$ (computer-assisted).
- At $r_e$ entry jumps from $0.384$ to $0$. The entry set shrinks to the top price atom. This is a boundary collision, not a fold.
- No equilibrium has wrong-signed orders, and the low type never mixes (analytical). A search found no live equilibrium with a mixed or interior high-type order (numerical diagnostic).
- Entry sets with holes are equilibria too. At full orders, any measurable $A\subseteq[x^*,\infty)$ with enough information mass works (analytical).

Source: `equilibrium_set/`. One referee refutation: in F.3(ii) as stated (full orders), $r_1$ must lie in $(r_J,r_C)$, not in $[r_e,r_C]$.

### 3. The investor is an insider if and only if it trades

In every equilibrium, the materiality of $\theta$ at flow $x$ is $\mathbf 1_A(x)\Delta_T$. These statements are equivalent: $\theta$ is material ex ante; the entry set has positive probability; some investor type trades; the price is informative; the equilibrium is not $\mathcal D$ (Prop M.1, analytical).

Ex ante materiality factors as probability times magnitude: $\Pr(X\in A\mid\theta)\cdot\Delta_T$ (Prop M.2, analytical). This is the legal materiality test for merger information in Basic Inc. v. Levinson (1988). In the fork the probability leg is endogenous to the insider's own trade. Under Rule 14e-3 the "substantial step" (preparation) comes after the trade and because of it. Source: `materiality/`, with 25 BibTeX entries in `refs.bib` (19 fully verified, 6 marked partly). This track had no referee.

### 4. One theorem for every cost distribution

Let the cost have any CDF $G$. Materiality at a price is $\Delta_T\,G(B_r(\mu_P))$ (Lemma CD.1, analytical). Insider status then depends on where the lowest cost $c_0$ sits against $B_r(m)<B_r(\tfrac12)<B_r(M)$:

| Regime | Lowest cost | Insider status |
|---|---|---|
| I (the paper's floor) | $c_0<B_r(m)$ | insider at every price, in every equilibrium |
| II | $B_r(m)\le c_0\le B_r(\tfrac12)$ | insider in every equilibrium; pools possible |
| III (the fork) | $B_r(\tfrac12)<c_0\le B_r(M)$ | an equilibrium outcome (for small $k$) |
| IV | $c_0>B_r(M)$ | bystander in every equilibrium |

The boundary cases at equality follow the tie rule; see Theorem CD.3. Two further results matter for the paper:

- No vanishing cost perturbation selects the live equilibrium over $\mathcal D$ (Theorem CD.14, analytical). The lowest added cost selects only the pool size.
- Entry equals $\mathbb E[G(B_r(\mu_P))]$, a Jensen gap. With an affine $G$ and a floor, information never moves total entry (Prop CD.11).

Source: `cost_distribution/`.

### 5. A backstop at the quiet price selects the insider

A uniform preparation subsidy removes $\mathcal D$ exactly when $s\ge c-B_r(\tfrac12)$. At the benchmark this subsidy always costs the seller more than it gains (Prop S.3, analytical).

A backstop works better. It pays the challenger $\bar s\ge c-B_r(\tfrac12)$ only if it prepares at the quiet price $t_0$. In $\mathcal D$ the quiet price carries the prior, so the challenger would claim the backstop and $\mathcal D$ breaks. In a live equilibrium the quiet price carries bad news, so nobody claims it. The backstop removes $\mathcal D$ at zero cost on the path (Prop S.5, analytical). At $r=3$ it works for $\bar s\in[1.7083,\,2.8051)$. Then the investor is an insider in every equilibrium (Corollary S.6).

Limits: the seller must commit, and the rule must depend on $r$, because where no live equilibrium exists the backstop leaves no equilibrium at all. A reserve price cannot remove $\mathcal D$ (Prop S.8). Disclosure of order flow only shrinks the pool. Source: `selection_design/`.

### 6. Competition is necessary for information production

Let the investor pay $\kappa>0$ to learn $\theta$. Outside $(\mathfrak r(k),r_C]$ the investor never learns $\theta$, however cheap learning is (Prop G.5, analytical). Inside, an acquisition equilibrium exists whenever $\kappa\le U^*(r)=J(r)-k$ (Prop G.2, analytical). $U^*$ rises from $0.020$ at $r_J$ to $0.106$ at $r_C$ and then drops to zero: a ramp with a cliff.

The threshold $\tau>\tfrac12$ turns acquisition into a strategic complement. With exogenous materiality (Remark G.1) it is a substitute and the equilibrium is unique. If acquisition is observable, forward induction selects the live equilibrium, and a higher $\kappa$ selects a smaller pool (Prop G.6, under a stated restriction). Source: `info_acquisition/`.

## When is the investor an insider?

The tracks give one answer in four layers.

1. **Knows $\theta$.** Exogenous in the paper and the fork; a choice once learning costs $\kappa$ (track 6).
2. **$\theta$ is material.** True exactly when the investor trades (track 3). The lowest preparation cost decides whether this is guaranteed, possible, or impossible (track 4).
3. **Which equilibrium.** Cost perturbations do not select. A backstop at the quiet price (track 5) or observable acquisition (track 6) does.
4. **Competition.** Below $\mathfrak r(k)$ trading cannot pay; above $r_C$ the challenger never listens. Between them, competition makes an insider possible (track 2 gives the exact range).

## Next steps, in order of value

1. **Test whether the paper can drop (A1).** Regime II keeps an insider in every equilibrium without the floor. Show whether Proposition 2's entry reversal survives there (`cost_distribution/` open items).
2. **Add the backstop to `mechanism.md`** after F.3, with Corollary S.6, and extend Prop S.5(v) to partial-order pools.
3. **Close the high-type "only if"** in `equilibrium_set/`: show that $\sigma_H=\delta_1$ maximizes the low type's necessary statistic.
4. **Game B of information acquisition** at $\lambda<1$: the uninformed trader's short and its effect on the ceiling.
5. **A referee pass on `materiality/`**, which was not refereed.
