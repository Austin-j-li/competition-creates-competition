**Independent verification of commit `904924f`**

Ten corrections PASS. M2 FAILS the broader propagation check: two supplementary summaries retain the old scope. All eleven local corrections pass. Every consumer named in the supplied propagation map also passes.

I inspected commit `904924f5477eb7f04f3826cf37f10e95745e3691` with `git show`. Its parent is `38172dfb8bb9bcd93f6fed3ef40dd56962dcb864`, as the brief specifies. The branch `slot-revision` contains the commit. All manuscript evidence below comes from this commit, not the current worktree.

I read the complete brief, SCAN.md, the math reports, the reconciliation reports, and the fixer's report. The audit reports exist on disk but are absent from the reviewed commit. Their contents define the agreed findings; they do not replace source verification.

Paths and line numbers below refer to `slot/manuscript/` at the reviewed commit. The extra M2 consumers fall outside the supplied propagation map. I distinguish that residual defect from the successful local repair.

**M1 — PASS: lower boundary of the admissible region.**

The statement at `appendix/A3_proposition2.tex:168–172` and proof at `:207–211` now distinguish the three strengths correctly. At the lower boundary,

\[
u=\frac{82}{59},\qquad M=\frac{141}{200},\qquad m=\frac{59}{200}.
\]

Independent auction calculations give

\[
\Delta_T(r_0)-k=-\frac1{300},\qquad
\rho m\Delta_T(r_1)-k=\frac7{240},\qquad
\rho m\Delta_T(r_2)-k=\frac{7091}{144000}.
\]

Thus every correct order loses at the weak strength. Every correct order earns a positive payoff at the two stronger strengths. Wrong orders lose at least the cost. Abstention at the weak strength and full orders at the stronger strengths are therefore unique.

The purchase posterior equals the entry threshold at the middle strength. Rule C1 gives recruitment; rule CM permits entry after a purchase anywhere in the stated interval. `sections/04_equilibrium_results.tex:123–125` remains correct. `appendix/A4_coexistence.tex:3–7` assumes the strict open band, so it makes no conflicting boundary claim.

**M2 — FAIL: local repair passes; supplementary propagation remains incomplete.**

The proposition and proof at `appendix/A6_robustness.tex:8–35` correctly impose

\[
\mathcal L_i(\theta,R\mid j,S)=G_j\otimes F_i.
\]

This condition excludes both signal information about the incumbent value and conditional dependence between the two values. The independent cost adds no class information. Conditional gross profit is therefore the stated class average. Stochastic dominance lowers that profit at each fixed posterior. Under C1, the indicator difference gives exactly

\[
\mathsf E_0-\mathsf E_1
=\Pr\{B_{F_1}(\mu(S))<C\le B_{F_0}(\mu(S))\}.
\]

Every named consumer passes:

- `sections/04_equilibrium_results.tex:188–197` states the conditional law and independent cost requirement.
- `sections/08_empirical.tex:10–16` states the same restrictions.
- `appendix/A6_robustness.tex:38–53` verifies the conditional law for the frozen slot.
- Table `tab:outcomes`, Panel B, at `sections/04_equilibrium_results.tex:219–235`, describes this frozen slot.
- `appendix/A9_parameters.tex:166–167` explicitly restricts its margin to full orders held fixed.

I recomputed Panel B from the auction formulas and the fixed order law. Entry at both strengths rounds to 0.522757. Ownership rounds to 0.324401. Proceeds round to 0.503998 and 0.872531. The A.9 profit margin rounds to 0.879842898. These values agree with the unchanged registry.

The residual defect lies outside the supplied map. `comparison.tex:204` still attributes the conclusion to “every experiment and every independent cost law.” `slides.tex:445` likewise says “any fixed price experiment” without the restriction. The counterexample that motivated M2 still defeats that unrestricted claim. This is an inherited propagation omission, not a new defect in the corrected proposition.

**Exact correction:** replace the first Slot sentence at `comparison.tex:204` with:

> Proposition A.3 fixes the joint law of the class \(j\) and the signal \(S\), with an independent cost law. Each economy satisfies \(\mathcal L_i(\theta,R\mid j,S)=G_j\otimes F_i\). Under rule C1, entry does not rise.

Replace the bullet at `slides.tex:445` with:

> Fix the joint law of \((j,S)\) and an independent cost law. Require \(\mathcal L_i(\theta,R\mid j,S)=G_j\otimes F_i\). A stronger incumbent weakly lowers gross profit at each belief, so entry does not rise under rule C1.

The numerical frozen-order summaries need no change. I made neither correction.

**M3 — PASS: separate sale-rate notation.**

The definition at `appendix/A4_coexistence.tex:204–206` and all nine affected source lines use \(s_-^*\). The tuple and proof use this symbol consistently at `:263–277` and `:317–322`.

Solving the low-class indifference condition gives

\[
\rho\Delta_T\frac{\pi b}{b+(1-\pi)t}=k
\quad\Longrightarrow\quad
t=\frac{b(\pi\rho\Delta_T/k-1)}{1-\pi}.
\]

At prior one half, this is the stated interior rate \(b(\rho\Delta_T/k-2)\). The zero and full-rate boundaries are unchanged. The definition of \(s_-\) and its three regimes in `sections/04_equilibrium_results.tex:277–295` agree.

A search of the committed manuscript found no prior use of \(s_-^*\) at the parent commit. Every remaining \(t_L\) occurrence denotes target proceeds, including the slides and comparison note. The threshold purchase rate \(s^*\) remains distinct.

**M4 — PASS: exact witness for the signal comparison.**

The witness at `appendix/A6_robustness.tex:468–479` satisfies the proposition and the extra exclusion condition. I derived it independently from the auction formulas and Bayes' rule. I did not import the fixer's calculations.

The unchanged inputs of \(S(B)\) are

\[
(h,\ell,p)=(10,1,1/2),\quad
(\rho,c_H,k)=(17/20,357/50,3/200),\quad
(r_0,r_1)=(11/10,23/10).
\]

With the new slot and the stated accuracies, I obtain

\[
b=\frac15,\quad M=\frac8{11},\quad m=\frac3{11},\quad
\mu_+=\frac{13}{22},\quad
\phi_+(\mu_+)=\frac{13}{16},\quad
\phi_-(\mu_+)=\frac{13}{40}.
\]

Direct auction integration gives \(\Delta_T(r_0)=1/220\), \(\Delta_T(r_1)=169/460\), and \(D^+(r_0)=149/4400\). The five exact margins are

\[
\begin{aligned}
c_H-B_{r_0}(d)&=\frac{21}{400}>0,\\
B_{r_1}(\phi_+(\mu_+))-c_H&=\frac{1363}{36800}>0,\\
k-(2a_T-1)D^+(r_0)&=\frac{2}{1375}>0,\\
(2a_T-1)\rho m\Delta_T(r_1)-k&=\frac{603}{31625}>0,\\
c_H-B_{r_1}(\phi_-(\mu_+))&=\frac{76753}{18400}>0.
\end{aligned}
\]

All match the new display. The slot obeys the model's liquidity restriction, and \(d=3/4>7/10=a_T\). The claims in `sections/06_robustness.tex:59–79` remain consistent. The witness changes the slot; it does not claim feasibility at the unchanged benchmark B.

**M5 — PASS: net sale payoff and its zero.**

The general payoff at `appendix/A6_robustness.tex:426` gives the corrected expression at `:543`:

\[
U_-(-1)=(2a_T-1)\frac{b}{2b+t}\rho\Delta_T(3)-k
=\frac{b}{15(2b+t)}-\frac1{50}.
\]

Its derivative is \(-b/[15(2b+t)^2]<0\). Its unique zero is \(t=4b/3\). At this rate, the gross payoff is exactly \(1/50\), and the net payoff is zero. The rate exceeds the preparation threshold \(15b/19\) and stays below \(\lambda\), since \(\lambda/b=\mathrm e-1>4/3\). The public posterior is \(21/50\), as stated. The equilibrium summary at `sections/06_robustness.tex:82–86` remains consistent.

**M6 — PASS: weak effect of dispersion.**

`sections/06_robustness.tex:44–45` now says “weakly raises.” It agrees with `appendix/A6_robustness.tex:266–267`. For fixed incumbent value, the acquisition-profit function is convex in challenger value. A mean-preserving spread therefore gives the weak inequality after each expectation and at each fixed belief.

Strictness need not hold. A point mass at 10 and a uniform class on \([199/20,201/20]\) both give \(g_H=203/24\) at \(r=3\). The relevant payoff is affine throughout those supports. Searches of `slides.tex` and `comparison.tex` found no duplicate of the erroneous dispersion claim.

**M7 — PASS: research patterns and variable entry.**

`appendix/A5_research.tex:292–330` now limits its reference to equilibrium patterns. It states and derives entry at the middle benchmark strength as

\[
\mathsf E_1=\rho+(1-\rho)\left[\beta+(1/2-\beta)\bar\lambda\right].
\]

Lemma `lem:a5-strong` forces research at the cap and full orders. Only a purchase recruits at this strength. Its probability is

\[
\Pr(X=1)=\tfrac12(\bar b+\bar\lambda)+\tfrac12\bar b
=\beta+(1/2-\beta)\bar\lambda.
\]

This proves the new entry formula. At cap \(33/100\), the formula gives exactly \(41745131/80000000\), or 0.5218141375. Independent calculations give positive margins for both cap bounds and both cost bounds at that cap.

`sections/05_research.tex:166–172` uses the same scope and formula. `appendix/A9_parameters.tex:134–147` explicitly fixes the benchmark cap and cost, so its numerical margins remain valid. The numerical entry in `sections/05_research.tex:64–66` remains restricted to its declared benchmark cap.

**M8 — PASS: the entry ceiling in the introduction.**

`sections/01_introduction.tex:98–99` now uses “Above the entry ceiling.” This matches `sections/08_empirical.tex:40–46` and `appendix/A8_empirical.tex:169–191`.

Under full orders above the ceiling, entry equals \(\rho\) after every order. Thus the order-entry covariance is zero. The conditional win gap remains \((M-m)(1-\ell/r)>0\) in the benchmark domain. At \(r_1\), a purchase still recruits, so the old broader phrase was incorrect.

The slot statements at `slides.tex:550` and `comparison.tex:215,354–358` already use the ceiling. The similar phrase at `comparison.tex:347` describes the historical Laplace draft; it is not the corrected Slot statement.

**M9 — PASS: signed profit gap.**

`appendix/A6_robustness.tex:269–271` now labels the registry value as the signed gap \(B_{r_1}(M(3/10))-c_H\). From the model,

\[
M(3/10)=\frac{3\mathrm e}{7+3\mathrm e},\qquad
B_3(M)-6=\frac18+\frac{25}{3}M-6.
\]

Rational bounds on Euler's number give a value that rounds to \(-1.390821\). The registry stores that sign and value. The no-recruitment conclusion and `sections/06_robustness.tex:37–40` remain correct.

**M10 — PASS: zero research and strict abstention.**

`appendix/A5_research.tex:172–176` restricts positive purchase payoffs to positive research. It cites Step 1 for Z. For R and T, the purchase payoff equals \(2a\hat\lambda>0\). At the cap, it is at least that value.

In Z, Step 1 at `:118–122` gives \(U_H(1)=U_L(-1)=\rho\Delta_T/2-k<0\). For example, at \(r=31/20\), this payoff is exactly \(-387/49600\). Wrong orders also lose. Thus abstention is strict in Z, and the strict-choice statements at `:112` and `:238–239` remain correct.

**M11 — PASS: scope of the class examples.**

Both `appendix/A6_robustness.tex:237–240` and `:250–255` now separate the moderate-gap row from the four three-strength reversal rows. The moderate-gap row retains its blank third-strength cell at `:206–207`.

I recomputed the auction expectations from point values and exact integrals over each uniform class. The moderate-gap row has four positive H1–H2 margins. The four other reversal rows also have positive H3 margins. The same-means point row fails recruitment at the middle strength, as stated. These computations support the new scope without any implicit third economy for the moderate-gap row.

**Commit scope and verification record.**

The commit changes exactly nine files: A.3–A.6 and Sections 1, 4, 5, 6, and 8. Its 65 added lines and 41 deleted lines belong to the eleven fixes or their named consumers. No unrelated passage changes. The commit does not change the registry, figures, numerical programs, slides, or comparison note.

The added source contains no literal decimal token. The new numerical displays use exact fractions or existing registry macros. I found no new notation clash or local mathematical error.

I ran `/tmp/ccc_slot_scan/verify/recompute.py` as a calculation worksheet with real manuscript inputs. It prints exact fractions and evaluations from rational bounds on Euler's number. It contains no assertions. Its output is `/tmp/ccc_slot_scan/verify/recompute.log`.

No test, test suite, manuscript build, checkout, commit, or repository edit ran. The report and calculation files are the only files I wrote. This review does not claim PDF layout verification. The fixer's separate build claim is not evidence of a build in this review.
