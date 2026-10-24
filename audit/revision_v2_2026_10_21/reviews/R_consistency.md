# Consistency review: revised manuscript at commit ac4e37e

Documents: `overleaf/paper-revision/main.tex` (3421 lines) and
`overleaf/paper-revision/online_appendix.tex` (3912 lines), with the nine
generated tables in `overleaf/paper-revision/tables/`.
Standard: `BRIEF.md` §0–§1 and `INTEGRATION.md` (X1–X17, U1–U4, R1–R23).
Numbers standard: `reconciliation.csv` and `NUMERICS.md`.
Line numbers refer to commit `ac4e37e`. This review edits no manuscript file.

Method, in brief. Each check ran on the two source files and the tables.
Symbol checks used exact-string searches plus a full read of Sections 1–8,
Appendices A.1–A.8, and Online Appendix A–C.9 and E.
A print-only script compared every decimal with at least four decimal places
against all 6269 numeric values in `reconciliation.csv`.
A second print-only script collected all labels and all reference targets.
Findings that restate an open integration point carry its identifier.

Counts: 4 blocking, 14 should fix, 26 minor. Total 44.
Items 37–44 are prose items. Each gives a tighter replacement.

## Blocking

### 1. The letter G names the class value cdf and bargaining profit (U2)

Loci: `main.tex:1288` (equation (14)), `main.tex:3046`,
`online_appendix.tex:1309`–`1310` (OA.44), `online_appendix.tex:1425`
(OA.50), `online_appendix.tex:3237`, and the axis labels of Figure 4
(`figures/bargaining_weight.pdf`, text layer reads `Gθ,η`, `GH,η`).

Problem. `G_j` is the central new object of the revision: the class value
cdf. The same letter then denotes challenger profit under bargaining,
`G_{\theta,\eta}`, `G_{H,\eta}`, `G_{L,\eta}`. A reader meets `G_{H,\eta}`
two sections after `G_H` became a cdf. Equation (OA.50) adds a third use:
realized profit `G(R,v,p)`. One symbol carries three meanings.

Replacement. Write bargaining profit with the profit letter `g`, as a
function of the value and the weight. Keep `G` for cdfs only.

- `main.tex:1288`: replace
  `G_{\theta,\eta}&=(1-\eta)\mathbb E[(\theta-R)_+],\\`
  with
  `g_\eta(\theta)&=(1-\eta)\mathbb E[(\theta-R)_+],\\`
- `main.tex:1282`–`1283` needs no change. The words already say
  "challenger profit".
- `main.tex:3046`: replace "which gives \(G_{\theta,\eta}\) in
  \eqref{eq:paper-14}" with "which gives \(g_\eta(\theta)\) in
  \eqref{eq:paper-14}".
- `online_appendix.tex:1309`–`1310`: replace `G_{H,\eta}` with
  `g_{H,\eta}` and `G_{L,\eta}` with `g_{L,\eta}`. Lowercase `g_{j,\eta}`
  matches `g_j`, the second-price class profit.
- `online_appendix.tex:1425`: replace `G(R,v,p)=(v-\max(p,R))_+.`
  with `g(R,v,p)=(v-\max(p,R))_+.` Add no gloss. The next display already
  integrates it into `g_v`.
- `online_appendix.tex:3237`: replace `\(G_{\theta,\eta}\)` with
  `\(g_\eta(\theta)\)`.
- Figure 4 and the C.7 output header (`online_appendix.tex:3248`,
  `G_H_eta, G_L_eta`) are pipeline output. Rename the renderer labels to
  `g_H_eta, g_L_eta` and re-render Figure 4. Do not hand-edit the PDF.
  The CSV column names may stay if the contract requires them (R17).
  The figure labels and the text must match after the re-render.

### 2. Generated table notes still state five strict margins and use c_L (U1)

Loci: `tables/table2_equilibrium_controls.tex:32`,
`tables/table3_extensions.tex:23`,
`tables/table_extensions_margins.tex:24`–`25`,
`tables/table_signal_grid.tex:42`,
`tables/table_reserve_details.tex:25`,
`tables/table1_auction_primitives.tex:17`,
`tables/table4_reserve_comparisons.tex` (second note),
`online_appendix.tex:2301`–`2302`.

Problem. Proposition 2 now has four strict conditions: (A1) and (A2).
Display (OA.77) defines five `ζ` quantities. The fifth, `ζ_L = B_{r_1}(m)`,
is a recorded quantity, not a hypothesis (Online Appendix C.1 says so at
lines 2296–2298). The table notes still call all five "strict margins of
Proposition 2" or "strict sufficient inequalities". Three notes also print
the retired symbol `c_L`. The notes contradict the text that carries them.
Fix the renderer strings and regenerate. Do not hand-edit the tables.

Replacement note text for the renderer:

- Table 2 note. Replace "The five strict margins of Proposition 2 at
  $(r_0,r_1)=(1.2,3)$ are" with "The four strict margins of Proposition 2
  at $(r_0,r_1)=(1.2,3)$ and the recorded floor profit are". Keep the five
  numbers and their order.
- Table 3 note. Replace "(all five margins strictly positive)" with
  "(all four strict margins strictly positive; the recorded floor profit
  $\zeta_L$ is not a hypothesis)".
- Margins table, first note. Replace "The five strict sufficient
  inequalities of the relevant proposition (low cost, high cost at the
  prior, high cost at the ceiling, weak-economy trade, strong-economy
  trade)" with "The four strict sufficient inequalities of the relevant
  proposition (high cost at the prior, high cost at the ceiling,
  weak-economy trade, strong-economy trade) and the recorded floor profit
  $\zeta_L$, which is not a hypothesis".
- Margins table, parameter note. Replace each vector
  "$(h,\ell,p,\rho,c_L,c_H,b,k)=(\dots,0,\dots)$" with the seven-slot form
  of Appendix A.8: "$(h,\ell,p,\rho,c_H,b,k)=(\dots)$". Drop the `0` entry.
- Signal-grid note. Replace "$c_L=0$, " with "". Replace "the smallest of
  the five conditions in \eqref{eq:oa-oa-29}" with "the smallest of the
  four conditions in \eqref{eq:oa-oa-29}".
- Reserve-details note. Replace "Floor margin is $B_r(m)-c_L$" with
  "Floor profit is $B_r(m)$".
- Table 1 note. Replace "across challenger types" with
  "across challenger classes".
- Table 4 note. Replace "the uniform derivative bound with a positive
  low-cost floor for full orders" with "the uniform derivative bound and
  the zero-cost entry floor for full orders".
- `online_appendix.tex:2301`–`2302`. Replace "Verify all margins before
  assigning an analytical equilibrium label." with "Verify the four strict
  margins before assigning an analytical equilibrium label. The floor
  profit \(\zeta_L\) needs no strict sign."

### 3. General-prior claims rest on displays printed at the equal prior

Loci: (a) `main.tex:3114`–`3115` (A.41); (b) `main.tex:2655`–`2660`
(A.24) with proof lines 2684–2686, and `online_appendix.tex:965`–`978`
(OA.26); (c) `online_appendix.tex:934`–`957` (OA.24);
(d) `main.tex:2825`–`2850` (A.5 definitions).

Problem. The brief requires `π` in general statements and `1/2` only in the
point-mass benchmark. Four general displays still hard-code the equal
prior, and no scope sentence marks them as benchmark formulas.
(a) Proposition A.9 holds "under the conditions of Proposition 2", which
allow every `π`. Its proceeds gain carries the factor `(1-\rho)/2`.
That factor is false at `π ≠ 1/2` as printed.
(b) Proposition A.6 inherits the general prior from Proposition 2.
Display (A.24) writes `B_{r_1}(m)`, `B_{r_0}(1/2)`, `B_{r_1}(M)`.
(c) Display (OA.24) omits the `logit π` term that (A.22) of the paper
includes. The two documents print different formulas for one object.
(d) Appendix A.5 builds `π = 1/2` into (A.27) and Step 4. The appendix
never states that restriction. Only the Online Appendix scope note
(line 251) states it, for its own A.7.

Replacement.

- (a) `main.tex:3114`–`3115`. Replace
  `\Delta\mathcal R_T&=\frac{1-\rho}{2} \left[\alpha_H(t_H-t_0)+\alpha_L(t_L-t_0)\right]>0,`
  with
  `\Delta\mathcal R_T&=(1-\rho)\left[\pi\alpha_H(t_H-t_0)+(1-\pi)\alpha_L(t_L-t_0)\right]>0,`
  The benchmark value does not change. Online Appendix C.9
  (line 3384) keeps `/2`. That exercise states the benchmark, so its
  display stays.
- (b) In (A.24) and (OA.26), replace `B_{r_1}(m)` with
  `B_{r_1}(m(\pi))`, `B_{r_0}(1/2)` with `B_{r_0}(\pi)`, and
  `B_{r_1}(M)` with `B_{r_1}(M(\pi))`. In the two proofs replace
  `e(1/2)=\rho` with `e(\pi)=\rho` and "close enough to \(M\)" with
  "close enough to \(M(\pi)\)".
- (c) `online_appendix.tex:935`–`937`. Replace the right side of (OA.24)
  with the right side of (A.22):
  `=\operatorname{logit}\pi +2\log\cosh\left(\frac{x+1}{2b}\right) -2\log\cosh\left(\frac{x-1}{2b}\right).`
  Replace line 948 "giving the open posterior range \((m,M)\)" with
  "giving the open posterior range \((m(\pi),M(\pi))\)". Replace
  line 951 `w=\sqrt{\tau/(1-\tau)}` with
  `w=\sqrt{\tau(1-\pi)/[(1-\tau)\pi]}`. Replace line 957
  `\(\mathsf E=\rho+(1-\rho)(\alpha_H+\alpha_L)/2\)` with
  `\(\mathsf E=\rho+(1-\rho)[\pi\alpha_H+(1-\pi)\alpha_L]\)`.
- (d) Insert after `main.tex:2827` ("accuracies") one scope sentence:
  "This appendix keeps the point-mass values and the prior \(\pi=1/2\);
  the formulas below use that prior."

### 4. Appendix A.11 and exercise C.6b cite an example the reader cannot see (R23)

Loci: `online_appendix.tex:1586`–`1590` and
`online_appendix.tex:3157`–`3159`.

Problem. Both passages evaluate "the reserve example that the earlier
construction used". This version removed that construction. The passages
also use two undefined symbols for its pooled posterior: `\bar\mu`
(A.11) and `\bar\mu_c` (C.6b), with gross profit `3\bar\mu`. No definition
survives in either document. The retirement argument needs no numbers:
gross profit is nonnegative, so a zero-cost buyer prepares at any pooled
price with positive gross profit, and by the tie rule at zero.

Replacement.

- `online_appendix.tex:1586`–`1590`. Replace the three sentences from
  "In the reserve example" to "before any pricing or trading check."
  with one sentence: "At any pooled price with positive gross profit, a
  zero-cost buyer prepares, so a prescribed nonpreparation at that price
  fails its first buyer check."
- `online_appendix.tex:3157`–`3161`. Replace the four sentences from
  "At its pooled price" to "no member of the family is a continuation."
  with two sentences: "At its pooled price, gross profit exceeded the
  positive low cost at separate prices but fell below it at the pooled
  price, so the buyer stayed out there. Under the declared cost law the
  low cost is zero, gross profit is nonnegative, and the buyer prepares
  at the pooled price. The prescribed policy fails its first buyer
  check, and no member of the family is a continuation."

## Should fix

### 5. Class objects still carry the value index θ (U3)

Loci, paper: `main.tex:2895` and `3003` (capital `\Theta`, undefined in
the paper), `main.tex:3083` (`(\Theta,R,C,Z)`), `main.tex:3120`
(`t_\theta`, "each state's"), `main.tex:3192`–`3193`
(`\sum_{\theta\in\{H,L\}}`), `main.tex:3331`–`3343` (`e_\theta`,
`\mu_\theta`, "in state \(\theta\)").
Loci, Online Appendix: `online_appendix.tex:323`–`329` (`\Theta`,
`\sigma_\Theta`, `q_\Theta`), `344`–`353` (`a_\theta`), `363`
(`\mathbf1\{\Theta=H\}`), `509` (`t_\theta`), `586` (`\mid\Theta`),
`609`–`613` (`F_\theta`, `U_\theta`), `663` (`e_\theta`), `688`
(`(S,\Theta)`), `790` (`F_\theta`), `1085`–`1104` (`\Theta`),
`1328` (`(\Theta,R,C,Z)`), `1386` (`t_\theta`), `1396`
(`\bar e_\theta`, `g_\theta`), `1523`–`1560` (`q_\theta`, `\mu_\theta`,
`\bar e_\theta`, `t_\theta`), `2193` (`\max_\theta`, `U_\theta`,
`d\sigma_\theta`).
Word loci: "state" for class at `main.tex:1187`, `2854`, `2920`–`2921`,
`3186`; `online_appendix.tex:662` ("State-specific"), `1123`
("true-state"), `1386`–`1389` ("each state's", "state-specific").

Problem. In the revised model `θ` is the challenger's value. The class is
`j`. These loci index class objects by `θ` or sum over `θ ∈ {H,L}`.
The same subscript then means a value in Sections 2–3 and a class in the
later appendices. Per-value objects keep `θ`: `t(\theta)`, `g(\theta)`,
`\mathcal V_\theta(R)` (`main.tex:3063`), and `G_j` expectations.
Do not touch those.

Replacement rule. Apply at every locus above.

- Class random variable: replace `\Theta` with `J`. Item 6 frees `J`
  by removing the constants `J_H, J_L`. At `online_appendix.tex:323`
  write "let \(J\in\{L,H\}\) have equal probabilities". At
  `main.tex:2895` write `\(J\perp X\mid T,\qquad Y\perp X\mid J .\)`
  At `main.tex:3083` and `online_appendix.tex:1328` write
  `\((J,R,C,Z)\)`.
- Class-indexed objects: replace the subscript `\theta` with `j`, and
  `_{\theta\in\{H,L\}}` with `_{j\in\{H,L\}}`. Examples:
  `main.tex:3192` becomes
  `&=t_0(p,r)+\frac12\sum_{j\in\{H,L\}}e_j(p,r;\sigma) [t_j(p,r)-t_0(p,r)],\\`
  `main.tex:3337` becomes "\(\mu_j(z;p)\) is the posterior reached in
  class \(j\) at noise realization \(z\)".
  `main.tex:3120` becomes "where the second line averages
  \(t_j-t_0>0\) over each class's additional-entry probability."
  `online_appendix.tex:663` becomes
  "\(e_j=\rho+(1-\rho)\alpha_j\)".
- Words: replace "state-conditioned" with "class-conditioned",
  "true-state entry" with "class-conditional entry", "in each state"
  with "in each class" (except `online_appendix.tex:1748`, which
  describes another paper's model and stays), "State-specific entry is"
  with "Class-conditional entry is".
- Benchmark scope in Appendix A.7. The sums at `main.tex:3192` and
  `3331` also carry the weight `1/2`. That weight is correct in the
  point-mass benchmark. Make the scope explicit once. Insert after
  `main.tex:3136` ("domain}"): "This appendix works in the point-mass
  benchmark, so the prior is \(1/2\) and class expectations carry equal
  weights."

### 6. The residual integral F_j(s) collides with the incumbent cdf F

Loci: `main.tex:1910`–`1938` (A.4)–(A.6), `main.tex:1956`–`1965`
(A.7, constants `J_H, J_L, K`), `main.tex:2469`–`2473`,
`online_appendix.tex:522`–`567` (`F_\epsilon`, OA.10–OA.13),
`online_appendix.tex:609`–`613`, `783`–`792` (OA.22),
`online_appendix.tex:1788`–`1789` (OA.66), `online_appendix.tex:1943`.

Problem. `F` is the incumbent's cdf. `F_0, F_1, F_2` are incumbent laws.
`F_j(s) = \int f\,A_j` is neither. It is the expected residual at order
magnitude `s`. The same object appears with three indexings: `F_j`,
`F_\theta`, and sign-indexed `F_\epsilon`. Appendix A.12 already names
this object `\bar A_j(q)` (`online_appendix.tex:1649`). Two names denote
one object, and one name denotes two objects.

Replacement. Use the A.12 name everywhere. Replace `F_j(s)` with
`\bar A_j(s)`, `F_H(s)` with `\bar A_H(s)`, `F_L(s)` with
`\bar A_L(s)`, `F_\theta(s)` with `\bar A_j(s)`, and `F_\epsilon(s)`
with `\bar A_\epsilon(s)` in the generic convolution lemma only.
Derivatives follow: `F_j'(s)` becomes `\bar A_j'(s)`.
Display (A.4) becomes:

```
\bar A_H(s)&=\int f(x-s)A_H(x)\,dx,\qquad
&\bar A_L(s)=\int f(x+s)A_L(x)\,dx,\\
U_j(s)&=s\bar A_j(s)-ks.
```

Remove the constants `J_H, J_L, J`. At `main.tex:1956` write
`\(\bar A_H(1)=(1-\pi)K,\qquad \bar A_L(1)=\pi K,\)` and keep `K`.
At `main.tex:1962` write "so at \(\pi=1/2\) the two coincide,
\(\bar A_H(1)=\bar A_L(1)=K/2\)". At `main.tex:1964`–`1965` write
"\(\bar A_j(s)\ge e^{-(1-s)/b}\bar A_j(1)\)" and
"\(k<(1-1/b)\min\{\bar A_H(1),\bar A_L(1)\}\)".
At `online_appendix.tex:244`–`247` apply the same names.
At `online_appendix.tex:783`–`784` replace (OA.22) line 1 with
`\(\bar A_H(1)=\bar A_L(1) =\Delta_T\int e(x)\frac{f(x-1)f(x+1)}{f(x-1)+f(x+1)}\,dx.\)`
Item 5 then uses the freed letter `J` for the class variable.

### 7. The letter D names three objects

Loci: `D(u)=G_L(u)-G_H(u)` at `main.tex:316` (keep);
signals price loading `D=e_Hw_H-e_Lw_L` at `main.tex:2860`–`2967`
(A.28)–(A.35) and `online_appendix.tex:1140`–`1255`;
value gap `D=h-\ell` at `online_appendix.tex:2753`–`2755`.
The subscripted dividend `D_0` (`online_appendix.tex:1405`, `2352`)
stays. It carries its subscript at every use.

Problem. One letter, three meanings. The signals `D` also hides its role:
it is the loading on the public posterior in the price.

Replacement.

- Signals loading: replace `D` with `\Delta_P` at every locus in
  Appendix A.5 and Online Appendix A.7. First definition becomes
  `D&=e_Hw_H-e_Lw_L.` → `\Delta_P&=e_Hw_H-e_Lw_L.`
  At `main.tex:2865`–`2867` replace "\(D\) carries the two rates
  separately" with "the price loading \(\Delta_P\) carries the two
  rates separately".
- C.4 value gap: replace `D` with `\Gamma` at
  `online_appendix.tex:2753`–`2755`. In the point-mass case
  `\Gamma = h-\ell` already (`main.tex:2703`). The three lines become
  "let \(\Gamma=h-\ell\) and examine \(\delta_n=\Gamma2^{-n}\)"
  (item 26 renames the index), "\(r_1=\ell+\delta_n\) and
  \(r_0=\ell+\delta_n^2/\Gamma\)". The CSV column names `delta` and `j`
  stay (R17).

### 8. Two names for the entry flow set, and a third use of script E

Loci: `main.tex:2422`–`2424`, `2498` (`\mathcal E_f`);
`online_appendix.tex:1642`–`1704` (`\mathcal X_\tau`);
`main.tex:3172`–`3184` and `online_appendix.tex:1495`
(`\mathcal E(p,r)`, the continuation set; keep).

Problem. `\{x:\mu(x)\ge\tau\}` is `\mathcal E_f` in Proposition A.5 and
`\mathcal X_\tau` in Appendix A.12. Script `E` also names the
continuation set. Sans-serif `\mathsf E` is total entry, and
`\mathsf E_f` (`main.tex:2431`) sits one display below `\mathcal E_f`.
Font alone carries the distinction.

Replacement. Keep `\mathcal E(p,r)` for continuations. Use
`\mathcal X` for every entry flow set. Replace `\mathcal E_f` with
`\mathcal X_f` at `main.tex:2422`, `2423`, `2424`, `2498`.
Definition line becomes
`&\mathcal X_f&=\{x:\mu_f(x;\pi)\ge\tau\},\\`
No other text changes. `\mathcal X_\tau` in A.12 stays.

### 9. Laplace density ℓ_b, and entry symbols e_r, P_r (R22)

Loci: `online_appendix.tex:806`, `823` (`\ell_b`);
`online_appendix.tex:900`–`908` (`e_r`, `P_r`).

Problem. `\ell` is the low benchmark value. `\ell_b` is a density.
The paper dropped the `r` subscript from the entry and price schedules
in equation (9). The Online Appendix price construction reintroduces it.
One schedule then has two names across the two documents.

Replacement.

- `online_appendix.tex:806`. Replace "Set \(b=1/L\) and
  \(\ell_b(z)=e^{-|z|/b}/(2b)\)" with "Set \(b=1/L\) and write
  \(f^{\mathrm{Lap}}_b(z)=e^{-|z|/b}/(2b)\) for the Laplace density".
  Line 823 becomes "Equality at a positive \(t\) requires
  \(f=f^{\mathrm{Lap}}_b\)".
- `online_appendix.tex:900`–`908`. Replace `e_r(\mu)` with `e(\mu)` and
  `P_r(\mu)` with `P(\mu)` (five occurrences). Insert before the display
  one clause. Line 898 "Then" becomes "Fix the incumbent strength \(r\).
  Then the schedules of equation (9) of the paper read". The display
  then matches (9) symbol for symbol.

### 10. The Online Appendix scope note patches formulas that the body prints at π = 1/2

Loci: scope note `online_appendix.tex:188`–`276`; body displays
`online_appendix.tex:489` (`w_L>0`), `512` (floor `ρmΔ_T`), `601`
(price with `/2`), `609`–`613` (bound with `m`), `646`–`648`
(`τ∈(1/2,M)`, `x^*`), `663`–`664` (entry `/2`, ownership `e_H/2`).

Problem. The scope note instructs the reader to read general-`π` formulas
into displays that print the benchmark versions. Item 3 covers the loci
the note omits. These loci are listed in the note, but the printed body
still contradicts the note at sight. One case is strictness, not the
prior: line 489 assumes `w_L>0`. The scope note (lines 273–274) and
Appendix A.2 of the paper use `w_L\ge0`. A patch list at the front of a
59-page appendix will drift again at the next edit.

Replacement. Print the general forms in the body. Then delete scope
items 1–3 and keep items 4–5 with the closing paragraph.

- Line 489: replace "put \(w_L=t_L-t_0>0\)" with
  "put \(w_L=t_L-t_0\ge0\)".
- Line 512: replace "Both residuals are bounded in
  \([\rho m\Delta_T,\Delta_T]\)" with "Both residuals are bounded below
  by \(\rho\kappa(\pi)\Delta_T\) and above by \(\Delta_T\)".
- Line 601: replace "\(P=t_0+\rho[(t_H+t_L)/2-t_0]\)" with
  "\(P=t_0+\rho[\pi t_H+(1-\pi)t_L-t_0]\)".
- Lines 609–613: replace \(\rho m\Delta_T(r_1)\) with
  \(\rho\kappa(\pi)\Delta_T(r_1)\) in both lines.
- Lines 646–648: replace "\(B_{r_1}(1/2)<B_{r_0}(1/2)<c_H<B_{r_1}(M)\)
  imply \(\tau\in(1/2,M)\)" with
  "\(B_{r_1}(\pi)<B_{r_0}(\pi)<c_H<B_{r_1}(M(\pi))\) imply
  \(\tau\in(\pi,M(\pi))\)". Replace
  "\(x^*=b\operatorname{logit}(\tau)/2\in(0,1)\)" with
  "\(x^*=\frac b2[\operatorname{logit}\tau-\operatorname{logit}\pi]\in(0,1)\)".
- Lines 663–664: replace "total entry is \((e_H+e_L)/2\), and
  high-quality ownership is \(e_H/2\) because \(h>r\)" with "total
  entry is \(\pi e_H+(1-\pi)e_L\), and high-class ownership is
  \(\pi e_H\) because \(h>r\)".
- Scope note: delete items 1–3 (lines 203–248). Keep the opening
  paragraph, item 4 (A.7 equal prior), item 5 (reserve term), and the
  closing paragraph. Renumber the two kept items as 1 and 2.

### 11. The introduction omits the strict class gap (R21)

Locus: `main.tex:207`, first sentence.

Problem. The sentence claims the reversal "for every pair of classes
with stochastically higher values in the high class and equal chances of
a value below the reserve". Those restrictions allow `G_H = G_L`.
Proposition 2 needs a strict gap above the reserve:
`E_H[max{θ,p}] > E_L[max{θ,p}]` (line 820). Section 5.2 states it
(line 1132). The introduction does not.

Replacement. Replace "for every prior and every pair of classes with
stochastically higher values in the high class and equal chances of a
value below the reserve" with "for every prior and every pair of classes
that differs above the reserve, with stochastically higher values in the
high class and equal chances of a value below the reserve".

### 12. Sections 2.3 and 5.1 state the same noise claims twice (R18)

Loci: `main.tex:408`–`425` (Section 2.3) against
`main.tex:1067`–`1078` (Section 5.1); exponential pair at
`main.tex:427`–`429` against `main.tex:459`–`463`.

Problem. Both passages state the clipped log odds, the failure of
Gaussian noise, the thinnest tails, and the most informative experiment.
Section 2.3 also states the exponential-difference construction twice in
32 lines: once as a microfoundation, once inside the roles paragraph.
Keep the full statements in Section 2.3, where the model needs them.
Section 5.1 needs only the class result and the numbers.

Replacement.

- Delete the paragraph `main.tex:1074`–`1078` ("Under full orders, the
  Laplace log odds … strictly inside \((0,1)\)"). It repeats lines
  409–416 without change.
- Replace `main.tex:1067`–`1072` (six sentences) with two sentences:
  "Laplace noise is the extreme member of the class, as
  \hyperref[sec-trading-and-timing]{Section 2.3} states. Online
  Appendix A.6 proves the tail bound and the flow comparison, and its
  price construction carries the comparison to prices."
- In the roles paragraph, replace `main.tex:461`–`463` ("With
  independent exponential amounts of mean \(b\), their net demand has
  exactly the Laplace density in \eqref{eq:paper-2}.") with "Their net
  demand is the first Laplace construction above."

### 13. Section 6.3 introduces the value classes a second time (R20)

Loci: first introduction `main.tex:1149`–`1153` (Section 5.2);
second introduction `main.tex:1343`–`1347` (Section 6.3).

Problem. Section 5.2 now presents the ±0.05 classes as the running
example. It even attributes them forward: "the value classes of
Section 6.3". Section 6.3 then defines them again from nothing.
One definition must own the example.

Replacement.

- `main.tex:1150`–`1152`. Replace "In the value classes of
  \hyperref[sec-design]{Section 6.3}, values are uniform" with "Let
  values be uniform within each class,". The sentence then defines the
  example where it stands.
- `main.tex:1343`–`1347`. Replace the five sentences from "To avoid
  making exclusion depend" to "preparation reveals the exact value."
  with two sentences: "The comparison uses the value classes of
  \hyperref[sec-acquisition-values]{Section 5.2}: uniform bands of
  half-width \(\varepsilon_V=0.05\) around \(\ell\) and \(h\), equal
  priors, and an investor who observes only the class. The bands keep
  exclusion away from a value atom."

### 14. Lemma OA.2 repeats Proposition 2, and the first lemma has no number (R19)

Loci: unnumbered extremality lemma `online_appendix.tex:820`–`830`;
Lemma OA.1 at `1010`; Lemma OA.2 at `1025`–`1043`.
No text cites either numbered lemma by number. The labels
`result-lemma-oa-1` and `result-lemma-oa-2` have no `\hyperref` uses.

Problem. Lemma OA.2 is Proposition 2 at a general prior, restricted to
benchmark values. Proposition 2 now holds at every prior for general
classes. The lemma adds nothing. The extremality lemma, which Section
5.1 uses, carries no number, while two unused lemmas carry numbers.

Replacement.

- Delete Lemma OA.2 and its proof paragraph (lines 1023–1043, including
  the `\Needspace` line). At line 1006 replace "Two further stability
  results are recorded for completeness." with "One further stability
  result is recorded for completeness."
- Give the extremality lemma the first number. At line 820–821 replace
  `{\textbf{Lemma (Laplace extremality; analytical).}}` with
  `{\textbf{Lemma OA.1 (Laplace extremality; analytical).}}`
  At line 1010–1011 replace `{\textbf{Lemma OA.1 (analytical).}}` with
  `{\textbf{Lemma OA.2 (analytical).}}`
  Swap the two labels with their headings: `result-lemma-oa-laplace-extreme`
  becomes `result-lemma-oa-1` content-wise. Simpler and safe: keep all
  labels unchanged and change only the printed numbers. No reference
  breaks, because references use labels.

### 15. The C.0 tie rule still thresholds entry at c_L

Locus: `online_appendix.tex:2112` (continuation controls listing).

Problem. The listing reads "lower plateau enters at B(m) = c_L".
The symbol `c_L` no longer exists in the model. Worse, the line states a
threshold comparison that the revision removed: entry at the lower
plateau now follows from `B(m) ≥ 0`, with the tie rule at equality.
The declaration lines `c\_L = 0` (lines 2025, 2042, 2055) and the schema
names at lines 2222, 2782, 2787 state the zero value. They may stay as
schema names (R17). Only this line uses `c_L` as a live threshold.
Fix the contract source as well as the manuscript listing.

Replacement. Replace line 2112 with
`\NormalTok{           upper plateau enters at tau = M; lower plateau enters at B(m) >= 0;}`

### 16. The word "type" names cost realizations and classes

Loci: `main.tex:354` ("The other type's cost is zero"),
`main.tex:3289` ("the expensive type"), `main.tex:1324`–`1325`
("across challenger types"), `main.tex:1004` (Figure 2 note,
"high- and low-type support magnitudes"),
`online_appendix.tex:1331` ("The high-cost type remains out"),
`online_appendix.tex:2682` ("both high-cost private-signal types"),
`online_appendix.tex:2960` ("the high-cost type enters").

Problem. The notation sheet reserves "type" for the investor's
information. Cost realizations are not types in the revised model, and
"types" at `main.tex:1325` means classes. Investor uses stay: "each
type" (`online_appendix.tex:591`), "low-type concavity"
(`main.tex:2246`), and the B-section headings. One locus,
`main.tex:354`, also lacks an antecedent: no cost "type" is defined.

Replacement.

- `main.tex:354`: replace "The other type's cost is zero: a low-cost
  challenger" with "The low cost is zero: a low-cost challenger".
- `main.tex:3289`: replace "the expensive type on it" with
  "the high-cost realization on it".
- `main.tex:1325`: replace "across challenger types" with
  "across challenger classes".
- `main.tex:1004`: replace "its high- and low-type support magnitudes"
  with "its support magnitudes after good and bad news".
- `online_appendix.tex:1331`: replace "The high-cost type remains out"
  with "The high-cost realization stays out".
- `online_appendix.tex:2682`: replace "both high-cost private-signal
  types stay out" with "the high-cost realization stays out after
  either private signal".
- `online_appendix.tex:2960`: replace "the high-cost type enters" with
  "the high-cost realization enters".

### 17. Proposition A.5 states the uniform case; Section 5.1 claims the class result in general

Loci: statement `main.tex:2406`–`2412` (`B_{r_0}`, `Δ_T(r_0)`);
claim `main.tex:1062`–`1063` ("extends the equilibrium comparison to
this class"); compare Proposition 2 at `main.tex:795`–`801`
(`B_{F_0}`, `Δ_T(F_0)`).

Problem. Proposition A.5 writes its conditions with uniform-incumbent
symbols `r_0, r_1`. Its nonemptiness clause also fixes uniform
strengths. Section 5.1 presents it as the comparison for the noise
class without the uniform restriction. Either the proposition covers
general `F_0, F_1` or Section 5.1 overstates its scope. The proof uses
only `t_0, t_j, g_j, Δ_T` and first-order strengthening (lines
2460–2461), so the general statement is available.

Replacement. State the general form. At `main.tex:2403`–`2412` replace
"Replace the upper posterior in \eqref{eq:paper-a2} by
\(\bar\mu_f(\pi)\), so that \[ B_{r_0}(\pi)<c_H<B_{r_1}(\bar\mu_f(\pi)). \]"
with "Replace the upper posterior in \eqref{eq:paper-a2} by
\(\bar\mu_f(\pi)\), so that \[ B_{F_0}(\pi)<c_H<B_{F_1}(\bar\mu_f(\pi)). \]"
Replace the next display
"\(\Delta_T(r_0)<k<(1-L)\rho\kappa(\pi)\Delta_T(r_1)\)" with
"\(\Delta_T(F_0)<k<(1-L)\rho\kappa(\pi)\Delta_T(F_1)\)".
In the same statement replace `g_L(r_1)`, `g_H(r_1)` with `g_L(F_1)`,
`g_H(F_1)`, and `W_H(r_1)`, `W_H(r_0)` with `W_H(F_1)`, `W_H(F_0)`.
Keep `r_0, r_1, r_2` in the nonemptiness sentence and in the proof's
uniform construction. They belong there.

### 18. Five bibliography records have no citation (R1)

Loci: `main.tex:1485` (Edmans 2009), `1545` (Kotz et al. 2001),
`1552` (Krishna 2010), `1631` (Vickrey 1961), `1636` (Ye 2007).
Each key occurs once in the file: its `\bibitem`. No `\citeproc` uses it.

Problem. Two records have natural homes in new text. Three have none.
Uncited records suggest support that the text never claims.

Replacement.

- Cite Kotz et al. at `main.tex:429`–`430`. Replace "It is Laplace if
  it is Gaussian with an exponential variance, as with a random number
  of liquidity traders." with "It is Laplace if it is Gaussian with an
  exponential variance, as with a random number of liquidity traders
  (\citeproc{ref-KotzKozubowskiPodgorski2001}{Kotz et al. 2001})."
- Cite Edmans (2009) at `main.tex:218`–`222`. Replace "and large
  holders trade, monitor, or intervene as prices feed back to firm
  decisions (\citeproc{ref-EdmansGoldsteinJiang2015}{Edmans et al.
  2015}, Section II.E;" with "and large holders trade on their
  information (\citeproc{ref-Edmans2009}{Edmans 2009}), monitor, or
  intervene as prices feed back to firm decisions
  (\citeproc{ref-EdmansGoldsteinJiang2015}{Edmans et al. 2015},
  Section II.E;".
- Delete the three remaining records: lines 1552–1555 (Krishna),
  1631–1635 (Vickrey), 1636 to the end of that record (Ye).
  Delete each `\bibitem` block in full.

## Minor

### 19. Ten equation labels name a different number than their tag shows

Loci: `main.tex:796` (`eq:paper-a2` shows (A1)), `801`
(`eq:paper-a3` shows (A2)), `3262`–`3404` (`eq:paper-a-50` to
`eq:paper-a-57` show (A.45) to (A.52)).

Problem. References resolve correctly today. The hazard is the next
edit: a writer who trusts the label name will cite the wrong condition.
The two condition labels are the dangerous pair. They swap the old
numbering exactly.

Replacement. Rename the labels to match the tags, in both definition
and every `\eqref`. Occurrences in total, definitions included:
`eq:paper-a2` 10, `eq:paper-a3` 14, each `eq:paper-a-5x` at most 2.
Search each key before the rename and replace all. Map: `eq:paper-a2` → `eq:paper-cond-1`,
`eq:paper-a3` → `eq:paper-cond-2`, `eq:paper-a-50` → `eq:paper-a-45`,
and so on through `eq:paper-a-57` → `eq:paper-a-52`. The target names
`eq:paper-a-45` to `eq:paper-a-49` are currently unused. No tag changes.
No printed text changes.

### 20. The noise class 𝒞_L uses the class letter L

Loci: `main.tex:1058`, `2374`, `2399`, `2594` (`\mathcal C_{1/b}`);
`online_appendix.tex:801`–`802`, `821`, `824`.

Problem. The subscript `L` is the score bound. In the same displays `L`
also names the low class (`Pr_L` at line 814). One letter, two roles,
sometimes in one paragraph.

Replacement. Rename the class of densities to `\mathcal N_L` at all
seven loci. First definition becomes "Let \(\mathcal N_L\) denote the
positive, absolutely continuous densities \(f\) with \(|f'|\le Lf\)
almost everywhere". `\mathcal C_{1/b}` becomes `\mathcal N_{1/b}`.

### 21. The letter ν is a flow measure and Student degrees of freedom

Loci: measure `ν(dx)` at `online_appendix.tex:206`, `345`–`358`;
degrees of freedom at `online_appendix.tex:2069`.

Problem. Both uses are standard in their fields. They sit in one
document with no warning. The Student use needs no symbol at all: the
parameter takes one value.

Replacement. At `online_appendix.tex:2068`–`2070` replace "The Student
law has \(\nu=3\) degrees of freedom and scale
\(b(\nu+1)/(2\sqrt{\nu})\)" with "The Student law has three degrees of
freedom and scale \(2b/\sqrt3\)". The values agree:
\(b(3+1)/(2\sqrt3)=2b/\sqrt3\), and at \(b=2\) the scale is
2.3094010767585034 as in `NUMERICS.md`. Keep `ν` for the measure.

### 22. Local names W and Y_n in the logistic decomposition collide with W_H and Y

Loci: `online_appendix.tex:827`–`828`, `880`–`888`.

Problem. `W` is the tail sum of Laplace components. Elsewhere `W_H` is
a win probability and `\mathcal W` is welfare. `Y_n` are Laplace
components. Elsewhere `Y` is the buyer's private signal. Both names are
local to one proof, so the risk is small. Renaming costs five lines.

Replacement. Rename the components `Z_n` (noise parts, like `Z`).
Line 828 becomes "\(W\overset d=\sum_{n=2}^{\infty}Y_n\) and the
\(Y_n\) are" → "the remainder \(\sum_{n=2}^{\infty}Z_n\), where the
\(Z_n\) are". Lines 880–888: replace `Y_n` with `Z_n` (three uses),
`Z_{\mathrm{Lap}}=Y_1` with `Z_{\mathrm{Lap}}=Z_1`, and
"independent of \(W=\sum_{n\ge2}Y_n\)" with "independent of the
remainder \(\sum_{n\ge2}Z_n\)". Then delete `W` from line 887:
"The product identity gives \(Z_{\mathrm{log}}\overset d=Z_1+\sum_{n\ge2}Z_n\)".

### 23. Two small g collisions: the inversion map g(P) and the flow density g(x)

Loci: `online_appendix.tex:478`–`481`; `online_appendix.tex:1362`–`1365`
(OA.47).

Problem. `g` is acquisition profit throughout. Online Appendix A.3 uses
`g(P)` for the price-inversion map. Appendix A.9 uses `g(x)` for the
marginal flow density. Each use is local and defined. Each invites a
wrong first reading.

Replacement.

- Line 478: replace "The function \(g(P)=[P-t_0-e(P)(t_L-t_0)]/[e(P)\Delta_T]\)"
  with "The function \(\iota(P)=[P-t_0-e(P)(t_L-t_0)]/[e(P)\Delta_T]\)".
  Line 480: replace "\(\mu_X(X)=g(P(X))\)" with "\(\mu_X(X)=\iota(P(X))\)".
- Line 1362: replace "the marginal full-order flow density
  \(g(x)=[f(x-1)+f(x+1)]/2\)" with "the marginal full-order flow density
  \(\bar f(x)=[f(x-1)+f(x+1)]/2\)". Line 1365: replace `g(x)` with
  `\bar f(x)` inside (OA.47).

### 24. The scalar bound Ā collides with the expected-residual functions

Loci: scalar at `main.tex:2975` (`=:\overline A`), `2982`
(`\overline A(r_0)`), `online_appendix.tex:2155`–`2159`;
functions `\bar A_j(q)` at `online_appendix.tex:1649`–`1698`, and at
every locus of item 6 after its rename.

Problem. `\overline A` (a number) and `\bar A_j` (a function) differ by
a subscript alone. Item 6 widens the function's use, so fix the scalar
now.

Replacement. Rename the scalar to `A^+`. Line 2975 becomes
"\(\le(2a-1)[\Delta_T+(1-\rho)(2d-1)w_H]=:A^+\)." Line 2982 becomes
"earn at most \(s(A^+(r_0)-k)<0\)". In Online Appendix C.0 replace
`A\le\overline A` with `A\le A^+`, `\overline A e^{-(T-1)/b}` with
`A^+ e^{-(T-1)/b}`, and `2\overline A/[1+e^{(T-1)/b}]` with
`2A^+/[1+e^{(T-1)/b}]`.

### 25. The entry-set probability a(q) collides with accuracy a and flow densities a_j

Loci: `online_appendix.tex:1644`–`1696` (`a(q)`, `a'(q)`);
accuracy `a` at `main.tex:2831`; densities `a_H, a_L` at `main.tex:665`.

Problem. Three objects share `a`. The A.12 object is a tail probability
of the entry set after an order. At full orders it equals the paper's
`\alpha_j`: `a(1) = α_H`, `a(-1) = α_L` against the full-order schedule.

Replacement. Rename `a(q)` to `\alpha(q)` at lines 1644, 1645, 1689,
1692, 1696. Line 1644 becomes "Let
\(\alpha(q)=\int_{\mathcal X_\tau}f(x-q)\,dx\) and
\(\bar e(q)=\rho+(1-\rho)\alpha(q)\)". No formula changes.

### 26. The C.4 sequence index j collides with the class index

Loci: `online_appendix.tex:2753`–`2772` (`\delta_j`, "integer \(j\)
from 1 through 20", "sequence of failed and successful \(j\) values").

Problem. `j` is the quality class in both documents. Here it counts a
halving sequence. The CSV column `j` (line 2787) is a schema name and
stays (R17).

Replacement. In the text only, replace the index `j` with `n`:
`\(\delta_n=\Gamma2^{-n}\)` (item 7 gives `\Gamma`), "for integer
\(n\) from \texttt{1} through \texttt{20}", "\(r_1=\ell+\delta_n\)",
"\(r_0=\ell+\delta_n^2/\Gamma\)", "Keep the sequence of failed and
successful \(n\) values." Add no gloss for the CSV column. Its header
line already lists it among schema names.

### 27. Cost-component cdfs H_L, H_H borrow the class subscripts

Loci: `online_appendix.tex:961`, `1371`, `1375`.

Problem. `H_L` and `H_H` are the low-cost and high-cost component laws
inside `H_C`. Their subscripts read as class labels. `H` alone also
names the high class in `t_H, g_H, e_H` on the same pages.

Replacement. Write the components as superscripts of the mixture:
`H_C^0` (low) and `H_C^1` (high). Line 961 becomes "let
\(H_C=\rho H_C^0+(1-\rho)H_C^1\), with atomless component laws".
Line 1371 becomes "For an atomless high-cost component \(H_C^1\)".
Line 1375: replace `H_H(dc)` with `H_C^1(dc)`.

### 28. The interval half-width η in the proof of Proposition 1(c) collides with the bargaining weight

Loci: `main.tex:1781`–`1783`.

Problem. The proof puts a uniform law on `[x_1-\eta, x_1+\eta]` and
sends `\eta\to0`. From Section 6.2 on, `\eta` is the seller's Nash
weight. The proof use comes first, so a reader who meets `\eta` again
at (14) must discard the first meaning.

Replacement. Rename the half-width to `\delta` (three uses). Lines
1781–1783 become "Let \(F\) be uniform on \([x_1-\delta,x_1+\delta]\)
and let \(\tilde F\) be the same law shifted to \(x_2\). Then
\(\tilde F\le F\), and as \(\delta\to0\), …". Bare `\delta` is otherwise
unused in the paper; `\delta_0` (Dirac) at line 2301 keeps its
subscript.

### 29. Two local T names: many-class mean proceeds T_X and the truncation bound T

Loci: `main.tex:2753`–`2786` (`T_X`); `online_appendix.tex:2156`–`2159`
(`[-T,T]`, `T>1`). Keep: signal `T` (Appendix A.5), subscript labels in
`\Delta_T, \mathcal R_T`, and transfer `T_\eta` (14). Those are
entrenched and defined at first use.

Problem. `T_X` is a posterior mean of proceeds `t_j`. Its name suggests
the signal `T` at flow `X`. The truncation `T` is a flow bound with no
relation to either.

Replacement.

- Rename `T_X` to `\bar t_X` at `main.tex:2754`, `2755`, `2774`,
  `2786`. First definition becomes "where \(\bar t_X\) is the posterior
  mean of the class proceeds at flow \(X\)".
- Rename the truncation bound to `\bar x` at
  `online_appendix.tex:2156`–`2159`: "a Laplace truncation outside
  \([-\bar x,\bar x]\), \(\bar x>1\), loses at most
  \(A^+ e^{-(\bar x-1)/b}\)" (item 24 gives `A^+`), and
  "\(2A^+/[1+e^{(\bar x-1)/b}]\)".

### 30. The support endpoint is r̄ in the model and R_max under bargaining

Loci: `\bar r` at `main.tex:303`–`305`, `584`–`585`, `1785`;
`R_{\max}` at `main.tex:1281`, `3025`.

Problem. One object, two symbols. `R_{\max}` also suggests a maximum
realization of the random variable `R` as a separate primitive.

Replacement. Replace `R_{\max}` with `\bar r` at both loci.
Line 1281 becomes "For an incumbent distribution supported on
\([0,\bar r]\), with \(\ell<\bar r<h\) and \(0\le\eta<1\)".
Line 3024–3025 becomes "let \(R\) have any distribution supported on
\([0,\bar r]\) with \(0<\ell<\bar r<h\)".

### 31. One stray B_p(m) among the B_{p,r} objects

Locus: `main.tex:3257`; compare `main.tex:3219`, `online_appendix.tex:1530`.

Problem. The seller appendix defines `B_{p,r}(\mu)`. The endpoint
paragraph writes `B_p(m)` once. The value `m(h-p)` does not depend on
`r` in that region, but the missing subscript reads as a new object.

Replacement. Replace "gross profit is \(B_p(m)=m(h-p)\)" with "gross
profit is \(B_{p,r}(m)=m(h-p)\), which does not depend on \(r\) in this
region".

### 32. The signal posterior λ_X uses the price-impact letter

Loci: `main.tex:2839`–`3000` (eight uses), `online_appendix.tex:1097`–
`1239` (including `\lambda_{\mathrm{req},y}`), `online_appendix.tex:2684`.

Problem. The brief bans new uses of `λ`. This use predates the revision
and has one meaning: `\Pr(T=+\mid X)`. It breaks no internal rule. It
does break the field convention: microstructure readers read `λ` as
price impact, never as a posterior. No price-impact object competes in
this paper, so the cost of keeping it is a first-reading stumble only.

Replacement (optional, but one name is cheaper than a gloss at every
use). Rename `\lambda_X` to `\varpi_X` and `\lambda_{\mathrm{req},y}`
to `\varpi_{\mathrm{req},y}\) at all loci above. First definition
becomes "and \(\varpi_X=a_+/(a_++a_-)=\Pr(T=+\mid X)\)". If the author
keeps `λ_X`, add four words at `main.tex:2839`: replace "and
\(\lambda_X=a_+/(a_++a_-)=\Pr(T=+\mid X)\)" with "and the signal
posterior \(\lambda_X=a_+/(a_++a_-)=\Pr(T=+\mid X)\) (not a price
impact)".

### 33. Four missing pointers between the two documents

Loci: `main.tex:224` (stake extension, no pointer);
`main.tex:1247`–`1252` (C.9 numbers, no pointer);
`online_appendix.tex:3775` ("Appendix A.7", ambiguous);
`main.tex:3370`–`3371` (parameter vectors omit the prior).

Problem. Each target exists and each number checks. The reader cannot
find the target from the citing sentence.

Replacement.

- `main.tex:223`–`224`: replace "a stake enters only as an extension."
  with "a stake enters only as an extension (Online Appendix A.12)."
- `main.tex:1252`: after "1.831923 trading units per share of float."
  insert "(Online Appendix C.9 computes both quantities.)" as its own
  sentence before "Holders who do not trade".
- `online_appendix.tex:3775`: replace "the conditional laws of Appendix
  A.7" with "the conditional laws of Appendix A.7 above". The same
  appendix means the paper's A.7 at lines 1593 and 2140, each with the
  qualifier "of the paper". Keep those two as they stand.
- `main.tex:3371`: after "\(c_H\) otherwise." insert "The prior is
  \(\pi=1/2\) in each vector."

### 34. One typeset slip in Appendix A.8

Locus: `main.tex:3411`.

Problem. The source reads `\(\varepsilon_V=\) 0.05.` The number sits
outside math mode and sets in text figures after a space.

Replacement. Replace "The atomless-value half-width is
\(\varepsilon_V=\) 0.05." with "The atomless-value half-width is
\(\varepsilon_V=0.05\)."

### 35. The class spread formula appears in two algebraic writings

Loci: `main.tex:1158` (`[(r-\ell)^2+\varepsilon_V^2/3]/(2r)`);
`online_appendix.tex:1475` (OA.52, `(r-\ell)^2/(2r)+\varepsilon_V^2/(6r)`).

Problem. The values are equal. The writings differ. A reader who
compares the two displays must redo the division to confirm one result.

Replacement. At `online_appendix.tex:1475` replace
`\Delta_T=\frac{(r-\ell)^2}{2r}+\frac{\varepsilon_V^2}{6r}.` with
`\Delta_T=\frac{(r-\ell)^2+\varepsilon_V^2/3}{2r}.`
Keep the paper's display as the standard form.

### 36. Locked convention clashes that need no rename

Loci: `r` (incumbent strength; auctions read reserve price), `b` (noise
scale; auctions read a bid), `p` (reserve; asset pricing reads a price),
throughout both files and the numerical contract.

Problem. Each symbol breaks a field convention. Each is also a column
name and a declared input in the numerical contract (R17). The text
defines each at first use and never uses the conventional meaning.
A rename would churn the contract for no internal gain.

Replacement. None. Record as flagged exceptions. If a referee presses,
the one-line defense already exists at first definition: reserve `p`
(`main.tex:364`), strength `r` (`main.tex:306`–`307`), scale `b`
(`main.tex:389`).

## Minor, prose (new passages only)

### 37. [Prose] The nonemptiness disclaimer appears twice and adds no scope

Loci: `main.tex:2741`–`2743`; `online_appendix.tex:1003`–`1004`.

Problem. Both constructions end with a denial: "not a statement about
effect size". The claims already state their exact scope: a nonempty
open set, for every ranked pair. The denial limits a claim that no
sentence makes. It also repeats across the two documents in near-identical
words.

Replacement. Delete both sentences. At `main.tex:2741`–`2743` keep
"with the low cost fixed at zero." and end the paragraph there.
At `online_appendix.tex:1002`–`1004` keep "All inequalities have strict
slack and persist by continuity." and end there.

### 38. [Prose] The proof of Proposition A.5 repeats one sentence and states its conclusion before its support

Locus: `main.tex:2506`–`2514`.

Problem. "Both conditional densities integrate to one" appears at lines
2508 and 2513. The Blackwell sentence (line 2511–2512) precedes the
sentence that supports informativeness (`\bar\mu_f(\pi)>\pi`, line
2514). The paragraph reads as two drafts merged without a final pass.

Replacement. Replace lines 2506–2514 with:
"The entry formula and the stated ownership condition follow. The
likelihood ratio is not constant: both conditional densities integrate
to one, so a constant ratio would equal one, and \(f\) would be
two-periodic. No positive integrable density is two-periodic. The
nonconstant ratio therefore exceeds one on a set of positive measure,
so \(\bar\mu_f(\pi)>\pi\) and the strong price experiment is
informative. It strictly Blackwell-dominates the weak constant
experiment."

### 39. [Prose] Two meta sentences describe the manuscript instead of the model

Loci: `online_appendix.tex:257`; `online_appendix.tex:1041`–`1043`.

Problem. "No claim here extends the displayed equal-prior sufficient
inequalities…" negates a claim in the voice of a response letter.
"Neither supplemental lemma is required to generate a reported
numerical value in the present manuscript" reports on the drafting
process. Neither sentence helps a reader use the results. Item 14
deletes the second lemma in any case.

Replacement. Delete both sentences. The scope item then ends at "The
buyer's private-signal maps update the public class posterior by Bayes'
rule." The lemma block then ends at line 1041, "…persists for nearby
priors." (Item 14 removes that block entirely; apply item 14 first and
this deletion is moot for the second locus.)

### 40. [Prose] The bargaining disclaimer appears in both documents

Loci: `main.tex:3054`–`3056`; `online_appendix.tex:1319`–`1322`.

Problem. Each proof of the bargaining signs ends by denying a result
about other games: first-price auctions, private-value bargaining,
bargaining-and-trading equilibria. The institution's four elements
already fix the scope (`main.tex:3013`–`3018`). One denial is enough,
and it belongs with the institution's full specification in the Online
Appendix.

Replacement. In the paper, keep the positive clause and delete the
denial. Replace lines 3054–3056 with "That boundary is a property of
this institution's payment rule. Online Appendix A.8 treats the
endpoints. \(\square\)" Keep the Online Appendix sentences unchanged.

### 41. [Prose] Two local denials guard against readings the text never invites

Loci: `online_appendix.tex:1020`–`1021` (Lemma OA.2 after item 14);
`online_appendix.tex:1534`–`1535`.

Problem. "it does not solve an unbounded-order game" and "not an
assertion that every continuation has them" both spend a sentence on a
scope limit that the hypotheses already state. The position bound sits
in the lemma's setup. The regularity conditions sit in the sentence
before.

Replacement.

- Line 1020–1021: replace "This perturbation retains the position
  bound; it does not solve an unbounded-order game." with "The position
  bound stays at one."
- Line 1534–1535: delete "These assumptions are sufficient, not an
  assertion that every continuation has them." The next sentences give
  the sufficient conditions directly.

### 42. [Prose] Two topic sentences overstate, then the text walks them back

Loci: `main.tex:437`–`439`; `main.tex:715`–`716`.

Problem. "The class claim is therefore about tail weight and bounded
inference, not about a fit of one law to noise demand." The negative
half defends against an empirical-fit reading that no sentence asserts.
"Price sufficiency holds in every candidate equilibrium. The entry
floor needs no condition." The derivation two displays later needs
\(\Delta_T>0\) (lines 727–728). Proposition A.2 states that premise.
The topic sentence omits it.

Replacement.

- Lines 437–439: replace with "The class claim concerns tail weight and
  bounded inference."
- Lines 715–716: replace with "Price sufficiency needs no entry-floor
  condition. It needs \(\Delta_T>0\), so that the price carries a spread
  to invert."

### 43. [Prose] Section 5.3 repeats one sentence frame back to back

Locus: `main.tex:1196`–`1197`.

Problem. "These conditions allow arbitrary mixed signal-contingent
orders … These conditions allow the buyer's signal to be more accurate
…" Two adjacent sentences share subject, verb, and function. One merged
sentence carries both facts.

Replacement. Replace both sentences with "The conditions allow
arbitrary mixed signal-contingent orders, every unilateral deviation to
an order in \([-1,1]\), and a buyer signal more accurate than the
investor's."

### 44. [Prose] Three new sentences need a split each

Loci: `main.tex:448`; `main.tex:1050`; `main.tex:1269`–`1270`.

Problem. Each sentence carries two independent claims. The claims are
sound. The packing slows the first read and hides which half a later
reference cites.

Replacement.

- Line 448. Replace "The trading stage follows the single-auction model
  of Kyle (\citeproc{ref-Kyle1985}{1985}), with binary information,
  bounded orders, a linear trading cost, Laplace noise, and a terminal
  payoff that depends on the price through preparation." with "The
  trading stage follows the single-auction model of Kyle
  (\citeproc{ref-Kyle1985}{1985}). It has binary information, bounded
  orders, a linear trading cost, and Laplace noise. Its terminal payoff
  depends on the price through preparation."
- Line 1050. Replace the single sentence with: "Outside the three
  certified points and the shaded analytical regions, the branches in
  Figure~\ref{fig:2} are numerical continuations from the search in
  Online Appendix C.2. That search also examined further pure and
  finite-support mixed profiles. The full correspondence at
  intermediate strengths is open."
- Lines 1269–1270. Replace "The dividend is a diagnostic on the
  financial claim: no bidder pays it, the seller cannot choose it, and
  acquisition surplus excludes it. The online matched-price panel
  reports it beside the hidden and feedback rows." with "The dividend
  is a diagnostic on the financial claim. No bidder pays it, the seller
  cannot choose it, and acquisition surplus excludes it. The online
  matched-price panel reports it beside the hidden and feedback rows."

## Checks that pass

These checks ran in full and found no further problem. They are not
numbered findings.

- **c_L.** The mathematical symbol `c_L` occurs in neither source file.
  The low cost is zero by construction: \(C\in\{0,c_H\}\) at
  `main.tex:353`. The only `c\_L` strings are schema names that state
  the zero value, plus finding 15 and the table notes of finding 2.
- **Conditions.** No literal `(A3)` survives in either file. The four
  literal `(A1)` and `(A2)` mentions in the Online Appendix
  (lines 601, 773, 964, 1012) each match the new tags: high-cost
  exclusion is (A1), the trading-cost window is (A2). Every paper
  mention uses `\eqref`. The label names are finding 19.
- **Prior.** Sections 2–4, 5.2, Appendices A.1–A.2, and the A.4
  nonemptiness construction write `π`, `m(π)`, `M(π)`, `κ(π)`
  throughout. Every other `1/2` is one of: a benchmark statement, an
  accuracy in `(1/2,1)`, the bargaining weight `η = 1/2`, a threshold
  bound such as `α_H > 1/2`, or `b > 1/2` in the certificate argument.
  The exceptions are findings 3 and 10.
- **Removed results.** The labels `result-proposition-a-10`,
  `price-pooling-at-fixed-orders`, and `result-proposition-oa-3` occur
  nowhere. No sentence cites Proposition A.10 or the old Online
  Appendix price-pooling result. The three C.6b mentions outside its
  own subsection (lines 2119 and 3354, and the subsection title at
  3152) are retirement statements. The word "pooling" elsewhere means
  zero orders (Proposition A.4) or posterior plateaus. Both survive
  under the zero cost and are correctly described.
- **Equation tags.** Paper tags run (1)–(14), (A1), (A2), (A.1)–(A.52)
  with no gap and no duplicate. Online Appendix tags run (OA.1)–(OA.79)
  with no gap. The reused labels `eq:oa-oa-57` to `eq:oa-oa-64` now
  carry the A.12 displays, and no reference to the removed A.11
  displays survives.
- **Cross-references.** The label script found 149 labels in the paper
  and 129 in the Online Appendix, no duplicates, and zero
  `\hyperref`, `\eqref`, or `\ref` targets missing from their own
  file. Literal references from the Online Appendix to the paper check
  out: Propositions 1, 2, 3 and A.1–A.8 at lines 313, 464, 580, 688,
  712, 959, 961, 1063, 1303; equation (11) at line 1640; (A.21) at
  line 877; (A.41) at line 3381; Appendix A.7 at lines 1593 and 2140.
  Paper references to Online Appendix A.6, A.11, C.2–C.6, and C.9 all
  land on existing subsections. The gaps are finding 33.
- **Numbers.** The reconciliation script matched every decimal with at
  least four decimal places in both files against
  `reconciliation.csv`, at its printed precision. Three values needed a
  manual verdict: the certificate bounds at `main.tex:2281`–`2285`
  print \(-0.000000000096\), \(-0.000000000121\),
  \(-0.000000000242\). The registry values are \(-9.624\text{e-}11\),
  \(-1.213\text{e-}10\), \(-2.429\text{e-}10\). Each printed bound is
  the stored bound rounded toward zero, so each printed inequality
  `Ψ ≤ printed value < 0` still holds. No change needed.
  Changed values appear only at their new values: low-cost inputs are
  gone from the text vectors (finding 2 covers the tables), the surplus
  levels 2.632301 and 2.552083 sit in the regenerated tables, and the
  floor event reads `p_L = h` (A.45). The retired pool values
  (0.272979, 0.303265, 0.151805, 0.125000 as a pool entry, 0.687364,
  0.609643) and the old floor value 6.281718 occur nowhere. The node
  `6.280` in C.6c is the declared sampled node, correctly described.
  Entry 0.522760 at `main.tex:1164` is the uniform-classes value
  (reconciliation row `cell.reserve_comparisons.uniform_classes…E`),
  not a mistyped 0.522757. All eight C.9 quantities print at their
  registry values in Sections 5.1, 6.1, A.12, and C.9. No number in
  either document lacks a reconciliation source. The release-gate PASS
  itself is recorded in `NUMERICS.md`; this review did not rerun it.
- **Benchmark language.** "High-value" and "low-value" for the
  challenger survive only in point-mass passages (Sections 4.2, 4.3,
  6.2, 6.3 Panel A context, Appendices A.3 and A.7), as X1c–d intend.
  General passages say "class". The slips are finding 16.
- **Certificate index.** Proposition 3 and (13) use `i` throughout
  (X3). No `v_j` or `r_j` certificate remnant survives.
- **Allocation values.** `\mathcal V_0, \mathcal V_\theta` (X4) occur
  only at `main.tex:3061`–`3066`. No `W_0(R)` or `W_\theta(R)`
  survives. `W_H, W_j` mean win probabilities everywhere else, and
  `\mathcal W` means welfare. The two fonts stay distinct in print.
  The local `W` of the Euler product is finding 22.

Out of scope, not audited: `talk.tex` and `script.tex` in the clone
(U4). They still use `c_L` and the old condition tags by the
integration record. This review covers the two manuscript documents
and their tables only.

## Rename summary for the integrator

One row per clash. "Locked" means the change also touches pipeline
output or the numerical contract.

| Current | Replacement | Finding | Locked |
|---|---|---|---|
| `G_{\theta,\eta}`, `G_{H,\eta}`, `G_{L,\eta}` | `g_\eta(\theta)`, `g_{H,\eta}`, `g_{L,\eta}` | 1 | Figure 4 re-render |
| `G(R,v,p)` | `g(R,v,p)` | 1 | no |
| class index `\theta`, `\Theta` | `j`, `J` | 5 | no |
| `F_j(s)`, `F_\theta(s)`, `F_\epsilon(s)` | `\bar A_j(s)`, `\bar A_\epsilon(s)` | 6 | no |
| `J_H, J_L, J` | `\bar A_H(1)`, `\bar A_L(1)` inline | 6 | no |
| signals `D` | `\Delta_P` | 7 | no |
| C.4 gap `D` | `\Gamma` | 7 | CSV names stay |
| `\mathcal E_f` | `\mathcal X_f` | 8 | no |
| `\ell_b` | `f^{\mathrm{Lap}}_b` | 9 | no |
| `e_r`, `P_r` | `e`, `P` | 9 | no |
| `eq:paper-a2/a3`, `eq:paper-a-50…57` | `eq:paper-cond-1/2`, `eq:paper-a-45…52` | 19 | no |
| `\mathcal C_L` | `\mathcal N_L` | 20 | no |
| Student `\nu` | words, scale \(2b/\sqrt3\) | 21 | no |
| `Y_n`, `W` (Euler product) | `Z_n`, inline sum | 22 | no |
| `g(P)`, `g(x)` | `\iota(P)`, `\bar f(x)` | 23 | no |
| scalar `\overline A` | `A^+` | 24 | no |
| A.12 `a(q)` | `\alpha(q)` | 25 | no |
| C.4 index `j` | `n` (text only) | 26 | CSV name stays |
| `H_L, H_H` | `H_C^0, H_C^1` | 27 | no |
| proof dummy `\eta` | `\delta` | 28 | no |
| `T_X`, truncation `T` | `\bar t_X`, `\bar x` | 29 | no |
| `R_{\max}` | `\bar r` | 30 | no |
| `B_p(m)` | `B_{p,r}(m)` | 31 | no |
| `\lambda_X` | `\varpi_X` (optional) | 32 | no |
| table-note `c_L`, five margins | finding 2 texts | 2 | renderer |
| tie rule `B(m) = c_L` | `B(m) >= 0` | 15 | contract source |
