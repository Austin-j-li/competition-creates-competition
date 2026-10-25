# W2-ownership: Solver F

**Status: PARTIAL HANDOFF.** Coordinator stopped this solver before the Python
checks. Below, "Derived" means I derived it by hand from the manuscript
formulas I read. "Read" means I read the value/statement in the source and did
**not** recompute it. "Conjectured/open" means not proved here. No scratch
script was written: `audit/theory_upgrade_2026_10_25/solvers/computations/W2_F/` was created but is empty
(the continuation should put its recomputation script there, per the brief:
print results, no assertions/tests).

Sources actually read: `BRIEF_common.md`, `W2.md`, `SCAN.md`,
`sections/02_model.tex` (model, eq. classes, `W_H` def. at line 225-228),
`sections/04_equilibrium_results.tex:11-70` (Prop. 2), `sections/05_research.tex`
(Prop. 4), `appendix/A1_payoffs.tex:109-214`, `appendix/A3_proposition2.tex:75-86`,
`appendix/A5_research.tex:1-201, 233-284` (research branch, proof of 4(a) at
266-284), `appendix/A6_robustness.tex:8-195` (Props. A.3, A.4, A.5) and
`383-489` (A.7), `appendix/A8_empirical.tex:166-193` (A.13), the ownership rows
of `scan/reduction_A3_A5.md`, and registry values in `numbers.tex`
(`beta_B=0.294655`, `res_a=1/40`, `res_cap=lambda_B=0.336122`, benchmark
`res_lambda/res_entry/res_own` at `r=1.55,1.60,1.65`, `own_r0=0.125`,
`own_r1_B=0.324401`, `prim_r0/r1/r2=6/5,3,18/5`).

## Candidate 1: Same-incumbent ownership multiplier (factorization theorem)
Angle: reformulate
Intuition: High-class ownership is exactly a product of an information term
(class-H entry) and a direct auction term (win probability against this
incumbent). A stronger incumbent moves them in opposite directions, so no
general level claim is possible; but the ownership created *relative to the
same incumbent with only ready (zero-cost) buyers* is exactly the information
term, and it rises with no condition on `W_H` at all.

Formal statement (**derived**, modulo the branch entry formulas read from
Lemma `lem:a5-middle`):
For any equilibrium at incumbent law `F`, let `e_j(F)=Pr(enter|j)`. Because
(cost, order) are independent of `(θ,R)` given the class, and preparation
depends only on price (= function of order) and cost,

`O_H(F) = π · e_H(F) · W_H(F)`,  `W_H(F)=E_H[F(θ)1{θ≥p}]`,

and similarly `O_L=(1-π)e_L W_L`. Define the same-incumbent floor
`O_H^0(F)=πρW_H(F)` (only zero-cost challengers ever prepare) and, for
`W_H(F)>0`, the multiplier `M_H = O_H/O_H^0 = e_H/ρ`. Then:

- (Prop. 4 research branch, prior 1/2) `e_H^R = ρ+(1-ρ)[β+(1-β)λ_R]`, since
  class H reaches a purchase with probability `(1-λ_R)β+λ_R = β+(1-β)λ_R` and
  only a purchase recruits. Hence
  `M_H^R = 1 + ((1-ρ)/ρ)[β+(1-β)Λ(Δ)]`, a strictly increasing function of `Δ`
  on the branch (using `Λ'(Δ)>0`, SCAN headline 4; I did **not** re-derive
  `Λ'(Δ)` in full — see open steps). So `M_H^R` rises weakly along any FOSD
  path and strictly where `Δ` rises strictly, for **any** `W_H` path.
- At each branch point the coexisting zero-research equilibrium (Z) of
  `lem:a5-middle` has `e_H=ρ`, so `O_H^R(F)/O_H^Z(F)=M_H^R` and
  `O_H^R(F)-O_H^Z(F)=π(e_H^R-ρ)W_H(F)>0` whenever `W_H(F)>0`: research
  strictly creates high-class ownership *at the same incumbent*,
  unconditionally. (The **difference** still carries `W_H`, so its size is
  not monotone across strengths; only the ratio cancels `W_H`. Worth stating
  explicitly — the floated "difference cancels" phrasing is wrong.)
- (Prop. 2) `M_H=1` at `F_0` and `M_H=1+((1-ρ)/ρ)(b+λ)` at `F_1`,
  unconditionally, replacing the iff-condition for this normalized object.
- Decomposition across strengths:
  `Δ log O_H = Δ log M_H + Δ log W_H` — information channel (+) vs direct
  competition channel (−). This identity is the sharp statement of the
  weakness.

Derivation: factorization as above (same independence argument as
A3 Step 4, lines 82-86, which I read). Entry formulas read from
`lem:a5-middle` (A5:136-138, 198-200) and A5:280-282.

Conditions: none on `W_H` beyond `W_H>0` for the ratio. Branch existence
conditions unchanged (`1/2<τ<1`, `ρΔ<2k`, `φ_a≥0`, `λ_R<λ̄`).

Benchmark check (**read, not recomputed**): registry gives on the branch
`res_own=0.298422, 0.309302, 0.319260` at `r=1.55,1.60,1.65` with `W_H=1`, so
there `M_H = O_H/(0.5·0.25) = 8·O_H ≈ 2.387, 2.474, 2.554` — the continuation
must verify these divisions and the underlying `e_H` in Python.

What is lost: the level `O_H` can still fall (the known counterexample).
Honestly: `M_H` is class-H entry rescaled, `e_H/ρ`. Defence (to be written
up): by the factorization, *any* same-`F` ownership ratio must equal an entry
ratio, so this is the sharp separation of channels, not an evasion; but the
continuation should present it as a decomposition + within-`F` equilibrium
comparison, not as if it were a new level prediction.

## Candidate 2: Keep the level claim under "never outbid / no extra overtopping", with the sharp elasticity frontier
Angle: primitive condition
Intuition: The original claim is exactly the statement that the proportional
entry gain beats the proportional win-probability loss. The plainest
primitive that kills the second term is that no incumbent on the path can
outbid a high-class challenger; a strictly weaker primitive is that the
strengthening never puts extra incumbent mass above high-class values.

Formal statement (**derived**):
- Sharp frontier (necessary and sufficient, no slack): for `s_1<s_2` on the
  branch, `O_H(s_2)>O_H(s_1)` iff
  `W_H(s_2)/W_H(s_1) > e_H(s_1)/e_H(s_2)`, i.e. `-Δlog W_H < Δlog e_H`.
  Locally (where differentiable): iff
  `-W_H'/W_H < (1-ρ)(1-β)λ_R' / [ρ+(1-ρ)(β+(1-β)λ_R)]`.
  (Same condition as SCAN Part 1, Prop. 4 row — read there; the algebra from
  `O_H=½W_H e_H^R` is one line.)
- Sufficient primitive, headline form (**Never Outbid**):
  `ess inf supp G_H ≥ sup_s ess sup supp F_s`. Then `F_s(θ)=1` `G_H`-a.s.,
  so `W_H(F_s)=1` for all `s` and Prop. 4(a)'s level claim holds verbatim;
  Prop. 2's condition reduces to `e_H>ρ`. Economic name: "a class-H
  challenger outbids every incumbent on the path."
- Weaker primitive (**No Extra Overtopping**): `F_s(y)` is constant in `s`
  for every `y ∈ supp G_H` (strengthening reallocates incumbent mass only
  below/above high-class values without changing the cumulative at those
  values). Then `W_H` is constant (possibly `<1`) and the level claim again
  holds. Hierarchy: Never Outbid ⊂ No Extra Overtopping ⊂ sharp frontier.
  For point-mass `H=h` this is just "`F_s(h)` constant in `s`"; for
  `U[0,r]` it holds iff `r≤h` on the path. Never Outbid is **far from
  necessary**: the frontier tolerates any proportional `W_H` loss below the
  proportional `e_H` gain.

Benchmark check (**hand arithmetic on read values; continuation to verify in
Python**): `h=10`, path strengths `r∈[6/5,18/5]` (BRIEF), so Never Outbid
holds with margin `h-r_2 = 10-18/5 = 6.4` (`h/r_2≈2.78`); on the research
branch `r≤r̄_R≈1.677633` (read), margin `≥8.32`. Slack of the frontier at the
benchmark: Prop. 2 ownership ratio `0.324401/0.125≈2.60` (read), so `W_H`
could fall by up to `≈61%` from `F_0` to `F_1` and ownership would still
rise. On the research branch, using read `λ_R(r_R)=0.193853`,
cap `0.336122`, `β≈0.294655`, `ρ=1/4`: `e_H` goes `≈0.574→0.649`, ratio
`≈1.13`, tolerating an `≈12%` end-to-end `W_H` fall. **These two numbers are
my mental arithmetic — flagged unverified.**

What is lost: Never Outbid excludes exactly the realistic case where even a
good challenger sometimes loses to the incumbent; as a stand-alone fix it
just restates the benchmark's `r<h` (02_model eq. order). Best presented as
the second sentence of Candidate 1's theorem, with the frontier as a remark.

## Candidate 3: High-class share of challenger acquisitions
Angle: reformulate
Intuition: Even when stronger incumbents reduce total high-class takeovers,
the takeovers that still happen can be increasingly high-class: research
raises H entry and lowers L entry, so the composition of challenger wins
shifts to H provided the low class's win chance erodes proportionally at
least as fast.

Formal statement (**derived formula; monotonicity conditional**):
Let `S_H = O_H/(O_H+O_L) = Pr(H | challenger acquires)` (denominator `>0`).
Then the odds form is

`O_H/O_L = [π/(1-π)] · (e_H/e_L) · (W_H/W_L)`,
`Δ log odds = Δ log(e_H/e_L) + Δ log(W_H/W_L)`.

On the research branch `e_H=ρ+(1-ρ)[β+(1-β)λ_R]` rises and
`e_L=ρ+(1-ρ)β(1-λ_R)` falls in `λ_R`, so `e_H/e_L` strictly rises with `Δ`
(**derived**). Hence `S_H` rises on the branch **iff/under the condition**
that `W_L/W_H` is nonincreasing along the path ("strengthening erodes the
low class's win chance proportionally at least as much as the high's").
Sufficient instances I could verify by hand: (i) `W_H=1` path (then `S_H`
adds nothing to Candidate 2); (ii) point-mass classes with `R~U[0,r]` for
**all** `r`, including `r>h` where the level claim fails:
`W_L/W_H = ℓ/r` for `r≤h` (falling) and `=ℓ/h` for `r≥h` (constant), using
`W_j=min(value,r)/r`. So `S_H` rescues a rising-ownership-*composition*
claim exactly in the counterexample family.

Why the extra condition is needed (**derived example; continuation to
double-check**): class ranking alone does not sign `W_L/W_H`. Take
`L: Pr(θ=2)=Pr(θ=10)=1/2`, `H: Pr(θ=5/2)=49/100, Pr(θ=10)=51/100`
(check `G_H≤G_L`: on `[2,2.5)`: `0≤1/2`; on `[2.5,10)`: `0.49≤0.5`). With
`W_j=E_F[1-G_j(R)]`, `F_0=U[2.1,2.4]` gives `(W_L,W_H)=(0.5,1)`, ratio `0.5`;
the FOSD-stronger `F_1=U[2.6,9]` gives `(0.5,0.51)`, ratio `≈0.98`: the ratio
**rises**. This kills the lemma "ranking ⇒ ratio falls"; it does not by
itself give a full equilibrium counterexample to `S_H` (open — would need
the entry channel small, e.g. `ρ→1`, plus branch conditions; I did not
construct it).

**Conjectured/open:** whether hazard-rate order of `G_H` over `G_L`
(survival ratio `(1-G_L)/(1-G_H)` nonincreasing) makes `W_L/W_H` fall under
*arbitrary* FOSD strengthening. I had a tilting proof attempt
(`W_L/W_H = E_{μ_F}[q(R)]`, `μ_F ∝ (1-G_H)dF`, `q` decreasing) but did not
establish that `μ_{F_s}` is FOSD-increasing in `s`; a random discrete search
in Python was planned and not run. Do not state this without proof or
counterexample.

Benchmark check: in the known counterexample (`r:11→12`, values in `W2.md`),
`S_H` should rise since `W_L/W_H=ℓ/h=0.1` is constant and `e_H/e_L` rises —
**not yet computed** (continuation: compute `e_L`, `O_L`, `S_H` at both `r`).

What is lost: `S_H` can rise while both `O_H` and total challenger
acquisitions fall; it is a selection/composition prediction, observable only
among completed challenger wins.

## Importance of the weakness
(**Partly derived, partly judgement; parameter magnitudes from `W2.md`,
log-splits are my mental arithmetic — unverified.**)
The counterexample is not knife-edge or exotic: same classes as the
benchmark, but `r=11,12>h=10` so H loses with probability `1/11,1/6`
(`W_H=10/r`); `ρ=0.05`, `β=0.2`, `c_H=2.5`, cap non-binding. The one
parameter that looks extreme, `a=5` vs benchmark `1/40`, is largely scale:
interior research needs `a ≈ (Δm_λ-k)/(2λ)`, and here `Δ≈4.5-4.9` vs
benchmark `Δ≈0.1` on the branch; `a/Δ` is `≈1.1` vs `≈0.26`. Mechanism of
failure: for `r>h`, `-dlogW_H/dlogr=1` exactly, while `λ_R` responds
weakly (entry `+0.96%`, `e_H≈+2%`, `W_H −8.3%`, `O_H −6.4%` over
`r:11→12` — recompute). Strict inequalities throughout should make the
failure an open set in parameters (continuity argument; branch margins
`φ_a>0`, `ρΔ<2k`, `τ∈(1/2,1)`, `λ_R<λ̄` **not yet evaluated**).
Economically: the paper's core mechanism (competition → spread → research
→ entry) is untouched; what fails is only the last step from entry to
*completed* high-class takeovers once the incumbent can outbid H — arguably
the realistic case, since the benchmark's `W_H=1` needs H synergies above
every incumbent value. Severity: a scope/statement problem, not an error in
the benchmark theorem as written (benchmark imposes `r<h`, 02_model eq.
order) and not in Prop. 2 / A.4 / A.5, which already carry the correct
`W_H` condition (04:35-39, A6:92-93, A6:185-189 — read).

## Other findings (errors in the manuscript, anything surprising)
- No error found in the ownership statements I read: Prop. 2 (iff condition,
  plus the sufficient form at 04:65-67, which I checked by hand:
  `b+λ>1/2` ⇒ bracket `>(1+ρ)/2`, times `(1+ρ)W_H(F_1)≥2ρW_H(F_0)` gives the
  claim), A.4 (A6:92-93), A.5's construction (A6:183-189 chooses `r_1` near
  `v_*` so the `W_H` loss is small — consistent with Candidate 2's frontier),
  A.7's ownership line (A6:489, valid under its stated `r_1<h`), A.13
  (benchmark-only `h>r`). The hazard is only in *generalizing* Prop. 4(a)
  and in unqualified prose (cf. SCAN conflation items on 05:44-46).
- Useful identity I derived for the continuation (verify):
  `m_λ = β(1-λ)/[2β+(1-2β)λ]` has `dm_λ/dλ = -β/[2β+(1-2β)λ]^2`, giving
  `Λ'(Δ) = m_λ / (2a + Δβ/[2β+(1-2β)λ]^2) > 0` from `2aλ=Δm_λ-k`.
- Surprising (to quantify, **conjectured from mental arithmetic**): at
  benchmark research parameters `Λ'(Δ)` is large (`a=1/40`), so even a
  hypothetical `W_H∝1/r` loss would roughly break even against the entry
  gain near `r=1.55-1.65`; the counterexample's failure needs the
  combination `r>h` *and* sluggish research (large effective `a/Δ`).

## Open steps for the continuation (in order)
1. Python script in `audit/theory_upgrade_2026_10_25/solvers/computations/W2_F/` (prints only):
   (a) reproduce the counterexample table (`Δ=9-49.5/r`, `γ=49.5/r`,
   `g_L=0.375/r`, `τ=(2.5r-0.375)/49.5` for `r>h` — my hand formulas),
   solve `2aλ=Δm_λ-k` for `λ_R`, check branch margins
   (`φ_a=Δ(1-τ)-k-2aλ_E≥0`, `λ_E=β(2τ-1)/[β+(1-2β)(1-τ)]`, `ρΔ<2k`,
   `λ_R<0.9`), and compute `e_H,e_L,O_H,O_L,M_H,S_H`, entrant share
   `πe_H/(πe_H+(1-π)e_L)`, and the log decomposition at `r=11,12`;
   (b) benchmark branch at `r=1.55,1.60,1.65` with `β=0.294655` (exact
   decimal per A9 — confirm), `a=1/40`, `Δ=(r-1)^2/(2r)`: confirm registry
   `λ_R, entry, own`, then compute `M_H`, `S_H`, and the tolerable `W_H`
   losses claimed in Candidate 2 (branch start `r_R≈1.501023` to cap
   `r≈1.677633`, and Prop. 2's `F_0→F_1`);
   (c) verify the `Λ'(Δ)` formula numerically against finite differences;
   (d) random discrete search: does hazard-rate order imply
   `W_L/W_H` falls under arbitrary FOSD shifts? (Candidate 3 conjecture.)
2. Decide presentation: my recommendation is Candidate 1 as the Prop. 4(a)
   replacement (decomposition + multiplier + within-`F` comparison), the
   first paragraph of Candidate 2 as its level corollary ("in particular if
   class H outbids every incumbent on the path"), Candidate 3 as a separate
   composition remark for the empirical section. Check this against
   SCAN "Decisions for Austin" #3.
3. Re-check every "mental arithmetic" number above before citing; several
   (branch `e_H≈0.574→0.649`, `≈12%` tolerance, counterexample log-splits)
   are flagged unverified.
4. Sweep remaining ownership consumers I did not read: `sections/06-08`
   prose summaries of A.4/A.5/A.7 and `comparison.tex`/`slides.tex` rows
   (SCAN Part 5), to confirm none states an unconditional level claim.
