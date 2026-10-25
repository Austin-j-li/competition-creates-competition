# W5-symmetry-tests: Solver F

> **HANDOFF STATUS (coordinator-requested phase-out, partial work).** Everything below
> the line "Status of each item" was derived by hand in this work periods from
> `overleaf/slot/appendix/A8_empirical.tex`, `sections/02_model.tex:142-213`,
> `appendix/A1_payoffs.tex:109-161`, `appendix/A2_beliefs_trading.tex:110-230`, and
> `SCAN.md` Part 1 (rows A.11, A.12, Cor. A.3, A.14). **No python was run and there are
> no scratch scripts:** `/tmp/ccc_wa2/W5/Solver F/` was never created and holds
> nothing useful. A successor solver must run the numeric checks listed as "Open".
> Numbers quoted below are analytic formulas evaluated by rough mental arithmetic
> only where flagged `[unverified arithmetic]`; do not cite them without recomputing.

## Status of each item

- **Derived (hand algebra, internally cross-checked against the manuscript formulas):**
  general-π full-order posteriors/counts; posterior-move formulas and their ratio;
  the count-weighted impact statistic and entry-component recovery; the four-regime
  sign classification; A.12/Cor.A.3 count identities at general π; price identification
  inversion at known π; A.14(i),(ii),(iv) at general π via the martingale identity;
  A.14(iii) exact positivity condition; exact pairwise condition for `A_F(M)` to rise
  under an FOSD strengthening, from A1's `t_j` formula.
- **Conjectured / sketched only:** price+count identification of (λ, π) jointly when π
  is unknown (algebra sketched, uniqueness argument only outlined); the claim that at
  benchmark `ρ=1/4` the naive test has false positives for π<1/2 but no false
  negatives for π>1/2 when `w_L≥0` (needs the scan in "Open"); branch-R formula at
  general π (inferred by analogy with the π=1/2 formula, not checked against A4).
- **Open (must still be done):** (1) all benchmark numerics by python — slot from
  `β=294655/10^6` (A8:254) and `1+u=e` (A9:23-25, `λ=uβ/(1+uβ)`), `r_S, r_C, r_1, r_2`,
  off-prior illustrations; (2) verify full-order incentive margins at the off-prior
  illustration points; (3) compute the `A_F(M)`-falls counterexample numbers;
  (4) finish/check the unknown-π identification algebra; (5) check tie-rule (C1 vs CM)
  boundary statements at `μ=τ` and at `π=τ`.

## Setup used throughout (general π, full orders)

Slot: `b=(1-λ)β`, `b0=(1-λ)(1-2β)`, `u=λ/b`, `a=1+u`. Full orders
`σ_H=δ_1, σ_L=δ_{-1}` give, on orders `(-1,0,1)`,
`f_H=(b,b0,b+λ)`, `f_L=(b+λ,b0,b)`, posteriors `(m(π), π, M(π))` with
(`sections/02_model.tex:148-149`)

```
M(π) = aπ/(1+uπ),        m(π) = π/(1+u(1-π)),
1-M(π) = (1-π)/(1+uπ),
M-π = π(1-π)u/(1+uπ),    π-m = π(1-π)u/(1+u(1-π)).        (*)
```

Hence `(M-π)-(π-m) = π(1-π)u²(1-2π)/[(1+uπ)(1+u(1-π))]`: the level asymmetry is
exactly `sign(1-2π)`, zero iff `π=1/2`. Counts:

```
p_1 := Pr(X=1) = b+πλ = b(1+uπ),   p_{-1} = b+(1-π)λ = b(1+u(1-π)),
p_0 = b0 = 1-2b-λ,   v := Pr(X≠0) = 2b+λ,   E[X] = λ(2π-1).
```

Key martingale identity (from `(*)`): `p_1(M-π) = p_{-1}(π-m) = π(1-π)λ`, i.e.

```
(M-π)/(π-m) = p_{-1}/p_1.                                          (**)
```

Prices (A2 Lemma A.2(b)): `P(x)=t_0+e(x)A_F(μ(x))`, `A_F(μ)=w_L+Δμ`,
`w_L=t_L-t_0≥0`, `Δ=Δ_T`. "Purchase-only recruitment" regime: `π<τ` (equiv.
`B_F(π)<c_H` when `γ>0`), so `e(-1)=e(0)=ρ`, `e(1)=e_+∈[ρ,1]`
(`=ρ+(1-ρ)χ`, `χ=1{M≥τ}` under C1). Full orders are an equilibrium only if
`K_L=ρΔ·m(π)>k` and `K_H=e_+Δ(1-M(π))>k` (A2 Lemma A.3); sufficient: `ρΔ·κ(π)>k`,
`κ(π)=min{m(π),1-M(π)}`.

## Candidate 1: Count-weighted impacts — every A8 test at every prior
Angle: reformulate
Intuition: Bayes plausibility already weights the two posterior moves to equality:
`p_1(M-π)=p_{-1}(π-m)`. So weight the two price impacts by the opposite order
frequencies and the prior-driven asymmetry cancels exactly, with no need to know
π, u, Δ or ρ. The same identity turns A.12's nonidentification into a sharp
dichotomy (counts identify the slot iff `π≠1/2`, given π known) and A.14 needs
no symmetry at all.
Formal statement: Under full orders at any prior `π∈(0,1)`, any ranked classes and
continuous `F` with `Δ>0`, writing `I_+=P(1)-P(0)`, `I_-=P(0)-P(-1)`:

(i) `I_- = ρΔ(π-m)` and, in the purchase-only regime `π<τ`,
`I_+ = ρΔ(M-π) + (e_+-ρ)A_F(M)`. Spread `S = ρΔ(M-m) + (e_+-ρ)A_F(M)`
(class component `ρΔ(M-m)`, entry component `(e_+-ρ)A_F(M)`; at `π=1/2`,
`M-m=ϑ=u/(2+u)`, recovering A.11(i)).

(ii) **Prior-free test.** `T := p_1 I_+ - p_{-1} I_- = p_1(e_+-ρ)A_F(M)`.
So `T>0` iff a purchase raises entry above the floor (`e_+>ρ`, given `A_F(M)>0`),
and the entry component is recovered from prices and order frequencies alone:
`(e_+-ρ)A_F(M) = I_+ - (p_{-1}/p_1) I_-`; class component
`= I_-·v/p_1`. At `π=1/2`, `p_1=p_{-1}` and this is A.11(ii). Only the ratio
`p_{-1}/p_1` is needed, so zero orders need not be counted for the test itself
(`P(0)` is still needed to form the impacts).

(iii) **Locating τ (bonus, derived).** For arbitrary threshold entry under full
orders, `T = p_1(e_+-e_0)A_F(M) - p_{-1}(e_0-e_{-1})A_F(m)`. With two-point entry
`{ρ,1}`: `T>0` iff `π<τ≤M` (purchase recruits), `T<0` iff `m<τ≤π` (a sale
de-recruits relative to no order), `T=0` iff `τ>M` or `τ≤m`. Boundary cases at
equalities follow the tie rule — `[open: state C1/CM cases precisely]`.

(iv) **Counts (A.12/Cor.A.3 dichotomy).** Known `π≠1/2`: counts point-identify the
slot under full orders, `λ=(p_1-p_{-1})/(2π-1)`, `b=(v-λ)/2`, `β=b/(1-λ)`,
informed share of nonzero orders `ϑ_π=λ/v` (directional shares `πλ/p_1`,
`(1-π)λ/p_{-1}`). A.12(a)'s one-parameter family exists only at `π=1/2`.
Known `π=1/2`: A.12(a),(b),(d) unchanged. Unknown π: counts identify `v`,
`λ(2π-1)` and `p_{-1}/p_1` only — a one-dimensional identified set in `(b,λ,π)`
`[open: write the feasibility inequalities β'≤1/3 etc. in this parametrisation]`.
Purchases only (`σ_H=δ_1,σ_L=δ_0`): `p_1=b+πλ`, `p_{-1}=b`, `E[X]=πλ`, so
`b=p_{-1}` and (π known) `λ=E[X]/π` at every π — Cor.A.3 survives verbatim with
`2E[X]→E[X]/π`. Branch R, `s_+=λσ_H(1)`: counts give `b` and `π s_+=E[X]`, never
`λ` alone `[conjectured general-π s_+ formula: s_+ = b[(Δ-k)(1-π)-kπ]/(kπ) from
K_H=k, μ(1)=1-k/Δ — NOT checked against A4]`.

(v) **Price identification (A.12(d)).** Given `ρ,Δ` and known π:
`s:=I_-/(ρΔ)=π-m(π,u)` is strictly increasing in `u` with inverse
`u = s/[(1-π)(π-s)]`; then `b=v/(2+u)`, `λ=uv/(2+u)`. Redundant for `π≠1/2`
(counts already identify), essential at `π=1/2`. `[Conjectured extension, algebra
only sketched: with π unknown, p_{-1}s=π(1-π)λ and E[X]=λ(2π-1) give
t=2π-1 as the root in (-1,1) of t²+4φt-1=0, φ=p_{-1}s/E[X]; then λ=E[X]/t.
Successor: verify uniqueness/sign handling and the E[X]=0 case.]`

(vi) **Announcements (A.14) at every π.** (i),(ii) are already general
(cost independence only). (iii) Pooled preparation-report mean
`= Σ_x p_x e(x)[1-e(x)]A_F(μ(x)) / Pr(A) ≥ 0`, strictly positive iff some order has
`e(x)<1` and `A_F(μ(x))>0`; sufficient in *every* equilibrium: `π<τ` and `Δ>0`
(some `x` has `μ(x)≤π<τ`, hence `e(x)=ρ`, and `A_F(μ)≥Δμ>0` since posteriors are
interior). If `m(π)≥τ` then `e≡1` and the mean is exactly 0. (iv) Under full
orders and `π<τ`: `P̄ = Σ p_x P(x) = t_0+ρA_F(π)+(e_+-ρ)p_1 A_F(M)` because
`Σ p_x A_F(μ(x))=A_F(π)` by affinity + martingale; hence
`P(0)-P̄ = -(e_+-ρ)(b+πλ)A_F(M)` while `μ(0)=π` — A.14(iv) with
`b+λ/2 → b+πλ`, and a shorter proof (no `m+M=1`).

Derivation: `(*)` by direct subtraction from the odds forms; `(**)` since
`p_1=b(1+uπ)`, `p_{-1}=b(1+u(1-π))`. (i) from `P(x)=t_0+e(x)A_F(μ(x))` and
`A_F` affine with slope Δ. (ii): fixed-entry counterfactual impacts satisfy
`p_1 I_+^{e0}-p_{-1} I_-^{e0}=e_0Δ[p_1(M-π)-p_{-1}(π-m)]=0` by `(**)`;
subtracting gives (iii), and `e_0=e_{-1}=ρ` gives (ii). (iv)-(vi) as above.
Conditions: full-order pattern (equilibrium requires the `K_H,K_L>k` margins above,
which are *not* automatic off `π=1/2` — `[unverified arithmetic: at benchmark slot
u=e-1, π=0.3 gives κ(π)≈0.136 vs κ(1/2)≈0.269, so ρΔκ>k needs Δ≳0.59, i.e. r≳2.8
in the benchmark family — recompute]`); `A_F(M)>0` (true if `Δ>0`); regime `π<τ`
for the purchase-only reading.
Benchmark check: `[OPEN — not run.] Successor script: β=0.294655, u=e-1,
λ=uβ/(1+uβ)≈0.336, b≈0.196 [unverified]; M(1/2)=e/(1+e)≈0.7311, ϑ≈0.4621.
Compute at π∈{0.3,0.5,0.7}, r=3 (Δ=2/3, τ=(6-0.375/r)/(10-r/2-0.5/r)≈0.705
[unverified]): posteriors, K margins, χ, I_±, naive I_+-I_- vs T. Expected:
π=0.3 ⇒ M≈0.538<τ, χ=0, but naive I_+-I_-=ρΔ(M+m-2π)>0 (≈45% of I_-
[unverified]) — false positive; T=0. π=0.7 ⇒ χ=1, naive bias negative but small
relative to entry term.`
What is lost: the bare statement "purchase impact exceeds sale impact" (needs
frequencies); A.12's "counts cannot identify the informed share" (false off
π=1/2 given π known — replaced by the sharper dichotomy). Nothing else: the
test still needs no auction objects.

## Candidate 2: Keep the original claims — π=1/2 is necessary, and name the trend condition
Angle: primitive condition
Intuition: Symmetry is not a convenient normalisation for A.11(ii)/A.12(a): the
no-recruitment bias `ρΔ[(M-π)-(π-m)]` has the sign of `1-2π` for every `u>0`, so
for any `π<1/2` the naive test reports recruitment that is not there. Separately,
A.11(iv)'s entry-component trend is exactly one inequality pitting a competition
effect against a reserve-failure effect.
Formal statement: (a) The test `I_+>I_- ⟺ χ=1` (for all `Δ>0, A_F(M)>0`) and
count-nonidentification at known π each hold iff `π=1/2`. (b) For an FOSD pair
`F̃≤F` (F̃ stronger), `δ=F-F̃≥0`, all challenger values `≥p`:
`A_F̃(M)-A_F(M) = -p·δ(p) + ∫_p^∞ [(1-G_L(y)) + M·D(y)] δ(y) dy`.
So the entry component weakly rises iff
`∫_p^∞ [(1-G_L)+MD]δ ≥ p·δ(p)` — call the path **entry-premium increasing at M**.
Necessary and sufficient pair by pair (zero distance from necessary).
Derivation: (a) `I_+-I_- = ρΔ[(M-π)-(π-m)] + (1-ρ)χA_F(M)` with the bracket
`∝(1-2π)` by `(*)`; take `χ=0`, `π<1/2`. Counts: `E[X]=λ(2π-1)`. (b) From A1:133-135,
`t_j-t_0 = pF(p)[1-G_j(p^-)] + ∫_p^∞[1-G_j][1-F]`; with values `≥p`,
`A_F(μ)=pF(p)+∫_p^∞[1-G_μ][1-F]`, `1-G_μ=(1-G_L)+μD`; difference the pair.
Economics: `α_M(R)=p` for `R<p`, `∫_p^R[(1-G_L)+MD]` for `R≥p`, has
`A_F(M)=E_Fα_M(R)`; `α_M` jumps *down* at `p` — a strengthening that mainly moves
incumbents from just below the reserve to just above it destroys the entry
premium (without entry the barely-admissible incumbent pays `p` anyway).
Conditions: Transparent sufficient primitives for the trend: (S1) incumbent always
admissible on the path, `F_s(p)=0`; (S2) constant reserve-failure probability,
`F_s(p)` constant. Both kill the `-pδ(p)` term. **The benchmark satisfies neither**
(`F(p)=p/r∈[0.14,0.42]` on `r∈[1.2,3.6]`) but satisfies the sharp condition:
`A_r(M)=1/2-1/(8r)+M(r²-2r+1)/(2r)`, `dA_r/dr = M/2 + (1-4M)/(8r²) > 0` for all
`r>1` since it rearranges to `r²>1-1/(4M)` `[derived by hand; successor: evaluate
the minimum margin on the path numerically, and the general-π version with
M=M(π)]`.
Benchmark check: `[OPEN.] Compute min_{r∈[r_S,r_C]} dA_r/dr at M≈0.7311; also verify
the counterexample in Candidate 3 violates the integral inequality.`
What is lost: nothing in the statements; the cost is two named hypotheses
(symmetric prior; entry-premium-increasing path) in place of "benchmark/FOSD".

## Candidate 3: Trend-free A.11(iv)-(v) in the (Δ, τ) plane
Angle: reformulate
Intuition: Half of A.11(iv) needs no extra condition at all: everything driven by
Δ alone rises under FOSD by Proposition 1. Only the entry component's *trend* is
path-shape-dependent; its *level* and its disappearance at the ceiling are not.
Formal statement: Fix the slot and π<τ along an FOSD path with full orders.
Class component `ρΔ(M-m)`, sale impact `ρΔ(π-m)`, and (after the ceiling) both
impacts and `S` are weakly increasing in strength, strictly iff
`∫_p^∞ D·δ>0` (Prop. 1). While recruiting (`τ(F)≤M(π)`, a down-set since τ weakly
rises under FOSD when `c_H≥g_L, γ>0`), `S = ρΔ(M-m) + (1-ρ)A_F(M)` with no trend
claimed for the second term; at any ceiling crossing where `χ` drops `1→0` and
`Δ, A_F(M)` are continuous, `S` and `I_+` fall by `(1-ρ)A_F(M)>0`, `I_-` continuous.
Derivation: Candidate 1(i) formulas + Prop. 1(b); τ monotonicity per SCAN Part 1
notation paragraph. Counterexample to any general entry trend `[conjectured
numbers, OPEN to verify]`: benchmark classes `ℓ=1,h=10,p=1/2`; `F`: 90% `U[0,1/2]`
+ 10% `U[9,10]`; `F̃`: 90% `U[1/2,1]` + 10% `U[9,10]` (shift the low component
across the reserve). `Δ=Eξ(R)`, `ξ(R)=(min(R,10)-1)_+`, is identical under both;
`A_F(M)` falls because `α_M` drops from `p=1/2` (R<p) to mean `1/4` on `[p,1]`:
expected `A: 0.45+high → 0.225+high`. Successor: compute exactly, and a variant
with the high component shifted up slightly so Δ strictly rises while A falls.
Conditions: full orders + `π<τ` only; continuity of `Δ(s), w_L(s)` for the jump
size (state it; do not claim a unique ceiling without single-crossing of `τ(s)-M`).
Benchmark check: `[OPEN.] Reproduce A.11(iv) as the special case via Candidate 2's
derivative; compute r_S (ρΔ(r)m=k), r_C (B_r(M)=6).`
What is lost: "both components rise while recruiting" as a general-path claim
(kept at the benchmark, and under Candidate 2's condition in general).

## Importance of the weakness
`[Draft — successor to finalise after numerics.]` (a) The symmetric prior is
knife-edge, but the failure is one-signed and quantifiable: without recruitment,
relative bias `(I_+-I_-)/I_- = p_{-1}/p_1 - 1 = λ(1-2π)/(b+πλ)`, zero only at
π=1/2 and ~45% at π=0.3 at the benchmark slot `[unverified]`. The economics
survives intact once impacts are count-weighted — arguably a better test.
Conjectured asymmetry `[OPEN scan]`: for π>1/2 a false negative needs
`(1-ρ)A_F(M) ≤ ρΔ[(π-m)-(M-π)]`; with `A_F(M)≥ΔM` and benchmark `ρ=1/4` this may
never bind, so the naive test may fail only by over-reporting recruitment.
(b) Count nonidentification is the `π=1/2` limit of weak identification:
`λ̂=(p̂_1-p̂_{-1})/(2π-1)` has variance inflated by `1/(2π-1)²`, and with π
itself unknown a one-dimensional nonidentification survives — the paper's message
needs restating, not retracting. (c) The `A_F(M)` trend failure needs a
strengthening concentrated at reserve-crossing; scale-type paths (benchmark)
satisfy it with margin `[to quantify]`. A.14 is essentially unaffected.

## Other findings (errors in the manuscript, anything surprising)
- A.14(iv)'s proof (A8:230-232) uses `m+M=1` and equal order probabilities; the
  martingale proof in Candidate 1(vi) is shorter and prior-free. No error, just
  unnecessary symmetry. Similarly A.14(iii)'s proof can replace `1/2` by `π`
  verbatim (condition `B_F(π)<c_H`).
- §08:21-22 ("this test needs no knowledge of the auction objects") remains true
  for the count-weighted test at every π, provided order frequencies are recorded;
  the floated prior-adjusted version `ρΔ[(M-π)-(π-m)]` would *not* have this
  property (needs π and ρΔ) — the count-weighted form strictly dominates it.
- `[Not checked; successor may verify]` A8:8 defines `ϑ=2M-1=M-m`, both equalities
  π=1/2-only; at general π the two split (`M-m` is the class-component factor,
  `λ/v` the informed share, and neither equals `2M-1`).
- No other manuscript errors found in A8/A1/A2 within the time available; A8's
  benchmark claims themselves (incl. `t_L-t_0=1/2-1/(8r)` rising, A8:6) check out
  against A1's formulas by hand.

## Handoff: suggested successor script (not yet written)
`/tmp/ccc_wa2/W5/Solver F/checks.py` should print (no assertions): benchmark
slot and `M,m,ϑ,v`; `r_S,r_C`; table over `π∈{0.3,0.4,0.5,0.6,0.7} × r∈{2,3}` of
posteriors, `κ(π)`, `ρΔm-k`, `e_+Δ(1-M)-k`, `τ(r)`, `χ`, `I_±`, naive vs `T`,
recovered entry component; the false-negative scan
`max_{π∈(1/2,1)} ρ[(π-m)-(M-π)]/((1-ρ)M)` at `u=e-1, ρ=1/4`; `min dA_r/dr` on
`[1.2,3.6]`; the Candidate 3 counterexample's `Δ, A_F(M), w_L` under `F, F̃` by
numerical integration of `ξ, α_M`; and `1/(2π-1)²` at `π=0.55, 0.6`.
