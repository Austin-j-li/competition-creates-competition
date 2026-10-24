FINDING VERDICT:
- Name: The cap region inherits a fixed benchmark outcome
- Verdict: CONFIRM
- Severity you assign: Mid
- Reason: A.5:292–294 invokes the whole benchmark proposition, but Section 5:65 includes a fixed entry number. At \(\bar\lambda=0.33\), the four region margins are \(0.039461120989455\), \(0.006720872993777\), \(0.002468642208197\), and \(0.011763302065145\). The strong-research margins at \(r_1\) and \(r_2\) also remain positive: \(0.017143805629407\) and \(0.035679609594749\). However, entry at \(r_1\) equals \(0.5218141375\), rather than \(0.522757\). The proof preserves the equilibrium patterns; its cross-reference gives the numerical claim excess scope.
- Better fix: Limit the cross-reference to equilibrium patterns, and give entry as \(\rho+(1-\rho)[\beta+(1/2-\beta)\bar\lambda]\).

FINDING VERDICT:
- Name: The introduction uses the wrong incumbent regime
- Verdict: CONFIRM
- Severity you assign: Mid
- Reason: The introduction at lines 98–99 includes the strong-incumbent economy \(r_1=3\), where orders do predict entry. Full orders give \(\Pr(X=1)=\Pr(X=-1)=b+\lambda/2\), so \(\mathbb E[X]=0\). Since \(e(1)=1\) and \(e(-1)=\rho\), the covariance equals \((1-\rho)(b+\lambda/2)=0.272756943478407>0\). The equation \(B_r(M)=6\) gives \(r_C=3.592658518794662\); above it, \(e\equiv\rho\) and the covariance is zero. Appendix A.8:174–175 states the correct scope.
- Better fix: Replace “Against a strong prepared bidder” with “Above the entry ceiling”.

FINDING VERDICT:
- Name: A shortfall appears with a negative magnitude
- Verdict: CONFIRM
- Severity you assign: Low
- Reason: At \(\pi=0.3\), the top posterior is \(M=0.3\mathrm e/(0.7+0.3\mathrm e)=0.538101526224449\). At \(r_1=3\), the auction integrals give \(g_H=203/24\) and \(g_L=1/8\). Thus \(B_3(M)-6=-1.390820614796259\), and the positive shortfall is \(1.390821\) to six places. A.6:267–268 attaches shortfall language to the signed gap; the numerical value and exclusion conclusion remain correct.
- Better fix: State the signed gap as \(B_{r_1}(M(0.3))-c_H=-1.390821\).

FINDING VERDICT:
- Name: A positive-purchase statement includes zero research
- Verdict: CONFIRM
- Severity you assign: Low
- Reason: A.5:172 includes Z in its claim of a positive purchase payoff. In Z, \(\hat\lambda=0\) and \(U_H(1)=\rho\Delta_T/2-k<0\), as Step 1 correctly states. At \(r=1.55\), \(\Delta_T=(r-1)^2/(2r)\) gives \(U_H(1)=-0.007802419354839\). The positive identity \(U_H(1)=2a\hat\lambda\) holds for R and T; the cap case gives the stated lower bound. Every investor choice remains strict, since Z requires strict abstention.
- Better fix: Restrict the positive-payoff sentence to positive research, and cite Step 1 for strict abstention in Z.

FINDING VERDICT:
- Name: The table claims a third-strength check without a third strength
- Verdict: CONFIRM
- Severity you assign: Low
- Reason: The moderate-gap row specifies \(r_0=21/20\) and \(r_1=3/2\), with a blank \(r_2\) cell. Its H1 margins are \(0.033452380952381\) and \(0.030137030410838\); its H2 margins are \(0.000809523809524\) and \(0.003602946278542\). These positive margins establish the two-strength comparison, with entry \(0.522756943478407\) at \(r_1\). H3 requires a specified third economy and \(B_{r_2}(M)<c_H\), which this row does not supply. Therefore, A.6:236–237 and 250–252 overstate the scope of the table's certificates.
- Better fix: State that the moderate-gap row satisfies H1–H2, while the other four reversal rows also satisfy H3.

These findings qualify my earlier coverage claims about the cap region, introduction, Step 5, and table scope. My four earlier findings and numerical conclusions remain unchanged.

I recomputed the values from auction integrals and order probabilities with `scripts/ext_1/reconcile.py`. The script only prints results. I ran no tests and made no repository changes.
