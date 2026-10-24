Exact calculations: [reconcile_exact.py](scripts/ext_2/reconcile_exact.py). The repository remains unchanged. No tests ran.

FINDING VERDICT:

- Name: The general control omits independence from incumbent value
- Verdict: CONFIRM WITH CHANGE
- Severity you assign: Critical
- Reason: The fixed law of \((j,S)\) in A.6:9–22 does not restrict the relation between \(S\) and \(R\). For the proposed continuous mixtures, direct integration gives conditional profits \((87/8,3)\) in economy zero and \(103/16\) after either signal in economy one. With zero-cost probability \(1/4\) and positive cost \(6\), entry rises from \(5/8\) to \(1\), despite \(F_1\le F_0\). This counterexample makes the proposition false as stated, so I raise the severity from High to Critical. The frozen-order control remains correct under its stated slot structure.
- Better fix: Require \(\mathcal L_i(\theta,R\mid j,S)=G_j\otimes F_i\), with the independent cost law; this also excludes dependence between values conditional on the signal.

FINDING VERDICT:

- Name: The private-signal feasibility argument lacks an analytical witness
- Verdict: CONFIRM
- Severity you assign: Mid
- Reason: A.6:462–463 does not establish feasibility: the four inequalities can jointly restrict the accuracies without an explicit inequality between them. Retain the declared values of \(S(B)\), and set \((\lambda,\beta)=(1/3,3/10)\). Bayes' rule gives
  \[
  b=\frac15,\quad M=\frac8{11},\quad m=\frac3{11},\quad
  \mu_+=\frac{13}{22},\quad
  \phi_+(\mu_+)=\frac{13}{16},\quad
  \phi_-(\mu_+)=\frac{13}{40}.
  \]
  My exact calculations give the private, joint, weak-trade, strong-trade, and other-pair margins, respectively,
  \[
  \frac{21}{400},\quad
  \frac{1363}{36800},\quad
  \frac{2}{1375},\quad
  \frac{603}{31625},\quad
  \frac{76753}{18400}.
  \]
  All five margins are positive, so this witness proves feasibility with \(d=3/4>a_T=7/10\).
- Better fix: Replace the final inference with this exact witness and its positive margins.

FINDING VERDICT:

- Name: A sale payoff omits its execution cost
- Verdict: CONFIRM
- Severity you assign: Mid
- Reason: Above the preparation threshold, A.6:422 gives the net sale payoff
  \[
  U_-(-1)=(2a_T-1)\frac{b}{2b+t}\rho\Delta_T(3)-k
  =\frac1{15}\frac{b}{2b+t}-\frac1{50}.
  \]
  Here \(2a_T-1=2/5\), \(\rho=1/4\), and \(\Delta_T(3)=2/3\). At \(t=4b/3\), the printed gross expression equals \(1/50\), while the net payoff equals zero. Thus A.6:527 omits the cost or the gross-return qualifier; the equilibrium rate remains correct.
- Better fix: Display the net payoff, then derive its zero at \(t=4b/3\).

FINDING VERDICT:

- Name: The dispersion claim omits “weakly”
- Verdict: CONFIRM
- Severity you assign: Mid
- Reason: Convexity gives a weak increase, as A.6:263–264 correctly states. At \(r=3\) and \(p=1/2\), both the point mass at \(10\) and \(U[199/20,201/20]\) lie above every incumbent value. The rent kernel is affine throughout these supports, so both distributions give
  \[
  g_H=10-\left(\frac32+\frac1{24}\right)=\frac{203}{24}.
  \]
  With the low class unchanged, gross profit is therefore unchanged at every belief. Section 6:45 needs the weak qualifier.
- Better fix: Replace “raises gross profit at every belief” with “weakly raises gross profit at every belief.”

Effect on my earlier report: I retract the general-control approval and the “no Critical or High issue” conclusion. The private-signal and equilibrium conclusions remain valid subject to these corrections.
