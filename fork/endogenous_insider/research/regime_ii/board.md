
## 2026-10-03 numerics #1 (start)
Numerics track online. Plan: exact panel-quadrature engine for pure-order profiles with half-line pools (cutoff families) plus mixed-profile search; sweep c_L at r1=3, then (r1, rho). Reversal test used: E > rho AND O_H > rho/2 (E(r0)=G(B_r0(1/2))=rho exactly when c_L<=B_r0(1/2)<c_H; B_r0(1/2)=4.804 at r0=1.2, so it holds for all regime II c_L). Note: no-trade exists at r1 iff rho*Delta_T(r1) <= 2k (CD.4); at r1=3 it fails for rho in {0.1,0.25,0.5}. First numbers to follow.
Status: plan only. Request to theory: post any candidate replacement for (A3) as a formula in (r1,rho,c_L,b,k) so I can test it on the grid.

## 2026-10-03 theory #1
Notation at r1: tau_L=B^{-1}(c_L) in (m,1/2), tau_H=B^{-1}(c_H). mubar(x')=F_Z(x'-1)/(F_Z(x'-1)+F_Z(x'+1)). xbar(tau_L) solves mubar(xbar)=tau_L.
(1) Part (i) at r0 survives unchanged (needs only c_L<=B_r0(1/2)<c_H, Delta_T(r0)<k). Analytical.
(2) No-trade/zero orders at r1 excluded iff rho*Delta_T(r1)>2k (CD.4); (A3) right side implies it. Analytical.
(3) Pool cap, any orders/mixtures/pool shapes: Pr(N|H)<F_Z(xbar-1), Pr(N|L)<F_Z(xbar+1), Pr(N)<(F_Z(xbar-1)+F_Z(xbar+1))/2. Proof: ROC region of Lap(1) vs Lap(-1) contains every (Pr(N|H),Pr(N|L)). Analytical.
(4) COUNTEREXAMPLE family (closed form, analytical): full orders, pool (-inf,x'), x'>=x*: e=1 on [x',inf), E=(S(x'-1)+S(x'+1))/2, e_H=S(x'-1). Equilibrium iff mubar(x')<tau_L and k<=(1-1/b)J(x'), J=Delta_T m e^{-(x'-1)/b}/2 for x'>=1 (Lemma CD.8 exact).
 Benchmark rho=.25: E=rho at x'=1.6265 -> fails for c_L>3.6498; e_H=rho at x'=2.3863 -> O_H fails for c_L>3.8945. Investor test ends at x'=2.614.
 Note: under (A3) right side, e_H at the family end x_k is k/((1-1/b)m Delta_T) < rho, so O_H<rho/2 is always reachable if tau_L > mubar(x_k).
Request numerics: check these two c_L thresholds; search islands/partial shorts for LOWER E at c_L in (2.37,3.65).

## 2026-10-03 numerics #2 (first counterexample, partial short)
r1=3, rho=.25, c_L=3.5 (tau_L=.405, regime II). VERIFIED by independent quad (verify.py, regret<2e-13, pool belief .3484<tau_L):
 pool cutoff x'=0.5, orders (q_H,q_L)=(1,-0.7196): E=0.1103, O_H=0.0763, pool prob .559. E<rho=.25, O_H<rho/2=.125: reversal FAILS.
 Mechanism: partial short keeps max posterior M_q=.7026<tau_H=.705, so the expensive type never enters; only the cheap type enters, on 44% of flows: E=rho*.441.
 Same c_L also has full-order equilibria with pools (E=.309..412 > rho), so uniqueness fails and the lowest-E member is the partial-short one.
 At c_L=3.0 I found only full-order (1,-1) members (E>=.38) so far; threshold for partial-short failure lies in (3.0,3.5). Sweep running.
 Status: numerical diagnostic + quad check (computer-assisted at 1e-8, not interval). Theory: your 3.6498/3.8945 are full-order thresholds; partial shorts beat them (c_L=3.5 < 3.6498). Will test your two numbers in the sweep.

## 2026-10-03 theory #2
STARVED family (new failure mode). Orders (1,-v), v<v_H:=b*logit(tau_H)-1 (=0.7424), so mu<tau_H everywhere: no expensive entry. Pool (-inf,x'), x'>=0, e=rho on [x',inf). L payoff s*C_L*e^{-s/b}-ks is strictly concave (A in [0,inf)); FOC C_L(v,x') e^{-v/b}(1-v/b)=k, C_L=rho*Delta_T*int_{x'}^inf e^{-x/b}mu_X/(2b)dx. E=rho*(S(x'-1)+S(x'+v))/2<rho.
 Benchmark k=.02: exists iff c_L>2.9846 (inf at v->v_H, x'=0.439, pool belief 0.3431); E in [0.064,0.112]; H full buy checked on grid only. k=.015 -> c_L>3.396; k=.01 -> 3.783. Status: L side analytical, H side numerical diagnostic.
 So at benchmark k, Prop 2(ii) fails for c_L>~2.985. Every equilibrium has a pool under (A3) right side (pool-free => full orders => pool). Analytical.
Island pools (full orders, knapsack worst case): E<rho for c_L>~3.46 (grid; investor test passes at k=.02).
Request numerics: (a) confirm starved threshold 2.9846 and look for mixed/q_H<1 starved equilibria at c_L in (2.37,2.98); (b) does any eq have E<=rho for c_L<2.98 at k=.02?

## 2026-10-03 theory #3
Agree with numerics' c_L=3.5 member (x'=.5, v=.7196, E=.1103): it lies on my starved family (at c_L=3.5: v in [.4532,.7424], x' in [.4388,1.0982], E in [.0883,.1124]).
Why the sweep missed c_L=3.0: the window there is tiny, v in [.7344,.7424], x' in [.4388,.4607], E~.112. At c_L=2.99: v in [.7396,.7424]. Below 2.9846: none (pure (1,-v), half-line pool, x'>=0).
Coming next from theory: forcing bound K(c_L)=(1-1/b) rho Delta_T min{tau_L S(xbar+1), m S(xbar)}; if k<K, EVERY eq has full orders and every consistent pool N is an eq; inf E is then an exact fractional-knapsack value. Benchmark: K(2.4)~.0098, so k=.02 is outside.

## 2026-10-03 theory #4
Forcing (Prop R.6, analytical): if k <= K(c_L)=(1-1/b) rho Delta_T(r1) min{tau_L S(xbar+1), m S(xbar)}, every eq at r1 has (1,-1) and the eq set is {(1,-1)} x {all Borel N >= Z_0 with pool belief < tau_L}. Proof: ROC/Jensen bound Pr(Z-s in N)<F(xbar+s), Pr(Z+s in N)<F(xbar), residuals >= rho*tau_L*Delta_T (L) and rho*m*Delta_T (H) on A.
 K at rho=.25: c_L=2.37: .01068; 2.5: .00858; 3.0: .00648; 3.5: .00529. So k=.02 is OUTSIDE; Prop 2' needs smaller k (e.g. k=.008, r0=1.1 works for c_L in (2.366,2.53]).
Exact entry range under forcing (Prop R.7): E in (E0-V_E, E0], e_H in (eH0-V_H, eH0]; V = bathtub (fractional knapsack) value; worst pool = Z_0 + mid band + island just above x* + part of plateau [1,inf).
 Sharp c_L thresholds (rho=.25): E>rho iff c_L<=3.4607; O_H>rho/2 iff c_L<=3.7408. rho=.1: 3.920/4.004; rho=.35: 3.037/3.528; rho=.5: 2.373/3.130.
Starved threshold vs k (pure (1,-v), half-line pool, x'>=0): k=.02: 2.9844; .015: 3.3954; .01: 3.7831; .0075: 3.9367.
Files: theory/formulas.py, theory/thresholds.py -> *.csv. Request numerics: does your island/mixed search find E<=rho at k=.02 for c_L<2.98? That is the open gap.

## 2026-10-03 theory #5
Correction to theory #4: with r0=1.1, k=.008, Prop 2' applies for c_L in (2.3662, 2.5867] (K(c_L)=.008 at 2.5867), not 2.53.
Checks (theory/checks_*.csv): ROC pool bounds hold on 4000 random mixed-order/random-pool draws (max violation -2.8e-5). At k=.008, c_L in {2.4,2.5}: all consistent pure half-line schedules give full best responses, min marginal payoff .048.
Agree with numerics eq_r3 partial-pool rows: your c_L=4.29 family starts at cutoff .4388, q_L=-.7424, E=.1124 = my starved limit member.
Universal bound (any k, any eq, analytical): E > rho*(1-pibar(tau_L)), e_H > rho*S(xbar-1). c_L=3.0: E>.102 (starved min there .112). c_L=3.5: E>.073 (starved .088).

## 2026-10-03 theory #6
Pure-schedule forcing map at r1=3, rho=.25 (theory/checks_forcing_map.csv; numerical diagnostic): k_pure = inf over consistent pure (q_H,q_L) + half-line pools of min_s d/ds[sF(s)].
 c_L=2.37: .0596; 2.45: .0572; 2.55: .0538; 2.65: .0192; 2.75: .0175; 2.95: .0147. Worst schedules above 2.6 are partial shorts (1,-.7) with voluntary pools.
 Break point = B(1-tau_H)=2.5833 (analytical): for pure orders, a pool needs min belief 1-M_q<tau_L; if tau_L<=1-tau_H this forces M_q>tau_H, so a starved profile cannot pool. Above it, starved schedules exist and weaken the short.
 So at k=.02: c_L<=2.58 -> full orders forced over pure half-line schedules, then knapsack gives E>rho (numerical diagnostic). (2.58,2.98): forcing fails for some schedules but no starved fixed point found. >2.984: fails.
Island check at k=.02 (checks_island.csv): bathtub worst pools pass the investor test; c_L=3.5 gives E=.2408<rho.

## 2026-10-03 numerics #3 (r1=3, rho=.25 sweep of c_L in [2.30,4.35], 90 pts, 4534 equilibria found; quad verification running)
 Regime I control (c_L<=B(m)=2.3662): unique (1,-1), E=.5228, O_H=.3242, no pools. Matches paper benchmark.
 Regime II, c_L in (2.3662, 2.975]: every found eq is (1,-1) with a half-line pool; trading outcome unique, entry NOT unique (E from .376 to .437 at 2.975). Reversal holds in every found eq (E>.25, O_H>.125).
 First failure on my grid: c_L=3.000 (partial short qL=-.7344, cutoff .461, E=.1117, O_H=.0773). Agrees with theory's starved threshold 2.9846 (grid .025 brackets it).
 For c_L>=3.95 the starved family reaches qL=0 (L abstains, H buys 1, cutoff 1.906): E=.0638, O_H=.0397. c_L>=B(1/2): no-trade/dead appear (regime III).
 Knapsack LP (full orders, all pools, sufficient J test k=.02): min E = .2502 at c_L=3.46 (theory 3.4607 confirmed); J constraint not binding at k=.02. Status: numerical diagnostic.
 Next: pool-LP over ALL pools and a lattice of pure orders (answers theory's gap (b) for c_L<2.98), mixed audit, then (r1,rho) region.

## 2026-10-03 theory #7
Agree with numerics #3 on all four points (2.975 clean, failure at 3.000 with q_L=-.7344/cutoff .461 = my window member, knapsack 3.4607, regime I control).
Your q_L=0 members (c_L>=3.95, cutoff 1.906, E=.0638) are the v=0 corner of my starved family: L abstains iff C_L(0,x')<=k. Matches my E range lower end .064 at k=.02. I add the corner to the note.
Note draft: theory/note.md. Proposition 2' = (A1') + (A2) + (A3') k<=K(c_L) + (A4') bathtub inf E>=rho, inf e_H>=rho. Exact under (A3'); benchmark thresholds 3.4607 / 3.7408.
Answer for the paper's k=.02: fails for c_L>2.9844 (numerical diagnostic), >3.6498 (analytical). Sufficient candidate c_L+c_H<=2B_r1(1/2) (=2.5833) is open as a theorem.
Request numerics (most useful now): mixed-L audit and partial-order island pools at c_L in (2.58,2.98) and at 2.50 (inside the candidate). A failure there would kill the candidate.

## 2026-10-03 theory #8 (closing)
Read numerics verify log: 4534 of 4534 rows accepted, max regret 2.1e-17. Thanks; this backs the clean range up to 2.975.
Final note: theory/note.md. Code and CSVs: theory/formulas.py, thresholds.py, checks.py (rerun: python3 thresholds.py; python3 checks.py).
Summary. (A1') taken with a strict lower end (c_L=B_r1(m) is regime I) and a strict upper end.
 (i) survives (Lemma R.1, analytical).
 (ii) under (A3) right side: informed trading, informative price, Blackwell dominance survive (analytical); every equilibrium has a no-entry pool, so entry is not unique.
 Replacement for (A3): (A3') Delta_T(r0) < k <= K(c_L) forces unique (1,-1) (analytical). Entry and O_H then need (A4') bathtub bound: exact at the benchmark, c_L<=3.4607 (entry), <=3.7408 (ownership).
 At the paper's k=.02: fails for c_L>2.9844 (starved family, numerical diagnostic) and >3.6498 (half-line, analytical). c_L<=2.59 clean on the forcing map (numerical diagnostic).
 (iii) becomes E<rho and O_H<rho/2 at every r2 with B_r2(M)<c_H (analytical).
Open for numerics/adversary: mixed-L and partial-order islands in (2.59,2.98) and at 2.50; certify the high type in the starved family.

## 2026-10-03 numerics #4 (verification, all-pool LP, mixed, exact starved threshold; r1=3, rho=.25, k=.02)
 Independent quad check (verify.py, no engine code): all 4534 rows of eq_r3 accepted; max regret 2e-17; |E-E_quad|<1e-10. Status for these rows: computer-assisted (floating quad, not interval).
 Pool LP over ALL measurable pools (islands, any shape) x lattice of pure orders (qH in {1,.8,.6,.4,.2,0}, qL step .05): for c_L in (2.3662, 3.05] only (1,-1) is feasible; min E over all pools = .4347 (c_L=2.37), .385 (2.7), .3405 (3.0): all > rho; min O_H >= .241 > .125. Islands do lower E below the half-line value (2.7: .385 vs .394) but never to rho. => theory gap (b): no E<=rho equilibrium found for c_L<2.984 at k=.02. Lattice misses narrow windows, so the exact window solver below carries the threshold.
 Exact starved threshold (engine BR for L, x_a=x_b): c_L*=2.98437 at (r1,rho,k)=(3,.25,.02). Theory 2.9844 CONFIRMED.
 Mixed profiles: audit of 1500 random consistent schedules per c_L (pure/two-atom orders, half-line/island pools): each type's payoff has exactly ONE local max every time, so best responses are unique. Bridge mixtures between the full and the partial pure equilibrium: none (the path crosses plateau posterior = tau_H, payoff jumps +.0017 -> -.016, tie rule puts the crossing on the high side). Lattice two-atom search (c_L=2.9,3.5; 4 pools; both types): 0 found. Status: numerical diagnostic, NOT exhaustive.
 Running: thresholds.csv (c_L* by mechanism for r1 in [1.5,3.6], rho in {.1,.25,.5}), then region scan + verification.

## 2026-10-03 adversary #1 (start)
Adversary online. Read theory #1-#8 and numerics #1-#3, theory/note.md, lattice LP and mixed audit. Plan: (a) independent quad re-check of the starved member at c_L=3.5 and of the H side of the starved family with a Lipschitz envelope between grid points (|F'|<=F/b), to tighten R.10(b); (b) attack Proposition 2' itself through rho: at the floor c_L->B(m)+, the minimal pool already has E_0 = rho(1-pi_0)+(1-rho)a with pi_0=Pr(X<=-1)=.342, a=(alpha_H+alpha_L)/2=.3637, so E_0<rho for every regime II c_L once rho >= a/(a+pi_0) = .5154 (closed form); under (A3') that is EVERY equilibrium. Ownership: e_H0<rho once rho > alpha_H/(alpha_H+F(-2)) = .7428. Will verify a full example (rho=.6, c_L=2.4, k=.02, r0=1.2: (A3') holds since K scales with rho) by global best response. (c) targeted mixed-L search in the window (2.59,2.98] with pools ending below 0, plus a concavity diagnostic: U_L is strictly concave on [max(0,-inf A),1] (F_-=0 there), so L can mix only with a short smaller than -inf A. (d) note: (A3') is empty at the paper's r0=1.2, rho=.25 since K<=.0107<Delta_T(1.2)=.0167; needs r0<1.148.
Status: plan; numbers in (b) are closed-form evaluations, to be checked. Request theory: confirm E(N)<=E_0 for every full-order pool (R.0) so the rho bound is analytical.

## 2026-10-03 numerics #5 (test of adversary's rho floor; r1=3, k=.02, c_H=6; numerics/rho_check.csv)
 Claim CONFIRMED numerically: at c_L=B(m)+1e-4 the single equilibrium has E=.5154 when rho=.5154 (closed form a/(a+pi_0)=.5154), E=.5108 at rho=.5, .5256 at .55, .5403 at .6. For rho>=.5154 no equilibrium has E>rho at ANY c_L in regime II (scan at B(m)+1e-4, +.05, +.30: E_max<=rho).
 It bites below .5154 too: rho=.5, c_L=2.4162: E in [.4797,.5083], so E>rho in some equilibria, not all. At c_L=2.6662 E_max=.4961<.5: reversal fails in EVERY equilibrium. rho=.45: holds at 2.4162, fails in some at 2.6662.
 Status: numerical diagnostic (engine cutoff scan, 0 unresolved starts). So Prop 2' needs a rho condition; for rho=.5 the c_L window is almost empty (theory's 2.373).
 Request adversary/theory: state the rho bound as an assumption of (A4'); I will report the full (r1,rho) map next.

## 2026-10-03 adversary #2 (results; files in adversary/: model.py, attack.py, *.csv)
1. COUNTEREXAMPLE TO PROP 2' THROUGH rho (closed form + quad check). Under full orders every pool N contains Z_0, so E(N) <= E_0(tau_L,rho) < E_0^+ := rho(1-pi_0)+(1-rho)a, pi_0=(1+e^{-2/b})/4=.34197, a=(alpha_H+alpha_L)/2=.36368 (depends on b, tau_H only). So E<rho in EVERY full-order equilibrium at EVERY regime II c_L iff rho >= rho_E*=a/(a+pi_0)=.51538 (r1=3; .5262 at r1=2.5, .5026 at r1=3.5). Ownership: e_H0<rho iff rho>rho_O*=alpha_H/(alpha_H+F(-2))=.74278. Verified example at the paper's k=.02, r0=1.2: rho=.6, c_L=2.4: (A1'),(A2),(A3) and (A3') all hold (K=.0234>=k), minimal pool accepted, regret 0, both certificates pass, E=.5382<.6, O_H=.3505>.3; eL=.375, eH=.701: bad prices remove mostly LOW-value cheap entry. rho=.75/.8: E and O_H both fail. So (A4') is not a technicality: it fails for all c_L once rho>.515. Status: analytical (the bound) + computer-assisted float quad (examples).
2. Starved family H side: certified (envelope far from q=1 + derivative sign near it, |F'|<=F/b, |U''| bound) on 54 members, c_L in {3,...,3.9}: far margin>=5e-4, near>=.009; U_H(1)=kv/(b-v) to 1e-6. Upgrades R.10(b) to computer-assisted (float quad). starved_hcheck.csv.
3. Re-checks: numerics c_L=3.5 member accepted (E=.11029, belief .3484), half-line thresholds 3.6498/3.8945 reproduced exactly, bathtub 3.4607 -> inf E=.250001, K(3)=.00648.
4. Window (2.59,2.98]: lattice of L two-point mixtures {-v1,-v2}, w in {.2,.5,.8}, H=1, cutoffs -1..0.5, islands: 745 consistent schedules, every one has ONE local max per type; L's BR is a single short >=.77>v_H; F_-=0 at every BR (U_L in its concave regime). No mixed or starved fixed point. Agrees with numerics #4.
5. (A3') is EMPTY at the paper's (r0,k,rho)=(1.2,.02,.25): K<=.0107<Delta_T(1.2)=.0167; needs r0<=1.157 (floor) or 1.12 (c_L=3). At rho=.5 the floor allows r0<1.229 and k=.02 (K=.0214). a3prime_feasible.csv.
Request theory: state rho_E* in Prop 2' as a necessary condition on rho (closed form) and add the rho=.6 example to the ledger; numerics: please re-run rho=.6, c_L=2.4 minimal pool through verify.py.

## 2026-10-03 adversary #3 (closing)
Read numerics #5: thanks, your E=.5154 at rho=.5154 and the "no equilibrium beats rho for rho>=.5154" scan match Theorem AD.1 (adversary/note.md, Section 3; analytical, full proof: E(N)<=E_0<E_0^+=rho(1-pi_0)+(1-rho)a for every full-order pool). Your rho=.5, c_L=2.666 failure in every eq matches my exact curve (rho_curve.csv: all-pools threshold .4488 at c_L=2.5, .3950 at 2.8).
Answer to your request: the rho condition is already inside (A4') (inf E >= rho is a condition on rho); the explicit form is rho < rho_E(c_L) with rho_E(B(m)+)=a/(a+pi_0)=.5154 and rho_E(c_L) decreasing to 0 at B(1/2) (Table 1 of my note). Theory: please add rho_E^* as a stated necessary condition in Prop 2' and the rho=.6, c_L=2.4 example (A1',A2,A3,A3' all hold; E=.5382<.6 in every eq) to the ledger.
Final ledger (adversary/note.md): breaks found: large rho (analytical); confirmed teammates' starved/half-line/bathtub numbers; H side of starved family certified (float quad, 54 members); window (2.59,2.98] survives L-mixtures/islands/pools below 0 (745 schedules, one peak each); (A3') empty at (r0,k,rho)=(1.2,.02,.25), overlap of (A3') and (A4') at the paper's r0,k is rho in (.446,.515) within .01 of the floor. Economics + draft Section 4.1 paragraph in Sections 7-8. Files: adversary/model.py, attack.py, 8 CSVs. Rerun: python3 attack.py all; python3 attack.py mixed.

## 2026-10-03 numerics #6 (region map r1 in [1.5,3.6] x rho in {.1,.25,.5}, k=.02; numerics/thresholds.csv, eq_region.csv; numerical diagnostic, 142 threshold members re-checked by independent quad: all accepted)
 Region where the reversal holds in every found eq = c_L in (B(m), c*). r1=3: rho=.25 c*=2.9844 (partial (1,-v), both types confirmed; theory 2.9844 matches to 5e-9); rho=.5 c*=2.3726 (island knapsack; theory 2.372568 matches to 2e-5); rho=.1: no break found in regime II (E stays >.1; 288 unconverged BR starts above 3.3 = open).
 rho=.25 over r1: c* = 2.86-2.99 for r1 in [2.4,3.5]; =B(m) from r1=3.6 (ceiling B(M)<c_H); no-trade eq for r1<=1.7; r1=1.9 holds on all of regime II. rho=.5: island bound 2.29-2.58 for r1>=2.
 NEW FAMILY (not in theory notes): low-trade eqs, both types order q<1, minimal pool, E=rho and O_H=rho/2 EXACTLY. They exist for k in [k_LT, rho Delta_T/2): r1=3,rho=.25: k in [.062,.083], q* up to .87 (klow.csv). At k=.02 they miss r1=3 but empty regime II at (r1,rho)=(2.4-2.6,.1),(1.8,.25),(1.5,.5). So (A3) left side must be k<k_LT, not only no-trade.
 Correction to my #4: first starved solver did not check the high type; wrong for rho=.1 and low r1. Replaced by a solver that confirms both types (same answer at (3,.25)).
 Theory checks: knapsack thresholds at 6 rho agree to <=1.6e-5; starved vs k (4 values) 5e-9; K(c_L)=.0098 at 2.4 is conservative: every random consistent pool is a (1,-1) eq up to k=.04 (fails at .06); scan k_U=.057 at 2.4, .050 at 2.9 (kscan.csv).
 Candidate c_L<=2B(1/2)-c_H: safe at rho=.25 (r1 2..3.5); FAILS at rho=.5 (c*=2.373 < 2.583 at r1=3) and where low-trade/no-trade bind. (iii) collapse at r2=3.8,4,5: E=rho exactly in regime I; E<rho, O_H<rho/2 in all found eq in regime II.
 Open: exact all-pool LP over the region (running), rho=.5 sweep, note.md. Request: any teammate objection to low-trade as a separate branch of (A3)?

## 2026-10-03 numerics #7 (closing; numerics/note.md, tables.txt, fig_regime_ii.pdf; all numerical diagnostic unless noted)
 Correction to #6. I wrote "(A3) left side must be k<k_LT". That was misleading. The paper's (A3) right side, (1-1/b) rho m Delta_T(r1), is at most .37 of k_LT in all 13 rows computed. So (A3) excludes the low-trade band. The band matters where (A3) fails at k=.02. There the right side holds only for rho=.25 with r1>=2.9 and rho=.5 with r1>=2.2, never for rho=.1. The region map marks every other cell with an asterisk.
 Exact pool LP over the region (792 points) lowers c* at two cells: (rho=.25, r1=2.0) to 3.9307 (partial: 4.0320) and (rho=.5, r1=1.9) to 2.6046 (partial: 2.9009). The members are confirmed by the engine and 33 of 33 pass the independent quadrature check. These LP values are upper bounds, because the order lattice is coarse.
 Adversary's floor: the minimal-pool equilibrium exists at all 400 c_L values of a fine grid and its E falls with c_L. So rho>=.5154 breaks E>rho at every regime II c_L (r1=3).
 Open: rho=.1 above c_L=2.6 (288 starts did not converge); one point with no equilibrium found (r1=1.6, rho=.5, c_L=2.8969); mixed profiles beyond two atoms; low-trade band mapped only at r1=3 and four other points; (iii) run for rho=.25 only.
 Request theory: state the (A3) replacement as k < min{k_LT, k_S, k_U} and do not claim "(A3) holds" in the asterisk cells.

## 2026-10-03 numerics referee #1 (start; check_numerics/, new code: model.py, bathtub.py, starved.py)
Read board and all three notes. Independent engine: adaptive quad (QUADPACK) per entry piece, global best response on a 101-401 point grid plus polish of every local max. Own knapsack on 1e-3 cells.
 AGREE so far (computer-assisted, float quad): regime I E=.52276 O_H=.32419; r0=1.2 E=.25 O_H=.125 exactly (zero orders); all 12 bathtub thresholds of theory Table 2 (rho .1 to .5, entry and ownership) agree to <=1e-4 (e.g. rho=.25: 3.46068 / 3.74079); worst pools at k=.02 accepted for c_L up to 3.5 (c_L=3.5: E=.24089, theory .2408; c_L=3.0: .34036) and FAIL at c_L=4.0 (L regret 1.2e-3); starved family: threshold 2.98437 (x'=.43885, pool belief .343125), members at c_L=3.0 (v=.7344, x'=.4606, E=.11166, O_H=.07727) accepted, regret<2e-18, H best response q=1 on 401-pt grid.
 Next: K(c_L), half-line thresholds, rho_E*/rho_O* and the rho=.6 example, c_L=2.975 entry range, R.5/R.6 random tests, R.11 break, low-trade, collapse. Request: none yet.

## 2026-10-04 theory referee #1 (check_theory/; own code referee.py, no imports from other tracks)
Read board, three notes, CD note. Proofs of R.1, R.2, R.4, R.5, R.6, R.7, R.8, R.11, R.12 checked line by line: no gap found so far. Table 1 reproduced by an independent cell knapsack (all entries within 1e-4).
CONFLICT FOUND (numerics vs theory Table 3): numerics kscan.csv says k_S(2.9)=.0718 ("no starved eq below") and the note says "(A3) is sufficient and not sharp for c_L up to 2.9". FALSE. At c_L=2.9, k=.0224 (inside (A3): .0167<.0224<.022412), orders (1,-.73), pool (-inf,.1913): pool belief .3277<tau_L=.333, both best responses at the candidate (regret 0, own quad), E=.1227<rho, O_H=.0833. Numerics' own starved.window also finds it (x' in [.154,.259]). Cause: kscan.k_starved bisects on a NON-monotone predicate (window exists for k in about [.021,.03], then not, then again near .07). Theory Table 3 (2.8326 at k=.0224) is right. Status: numerical diagnostic.
Also: the low-trade family needs no pool and no expensive entry; R.3(b) proves every eq has a pool under (A3) right side, so (A3) excludes low-trade ANALYTICALLY (not only on 13 rows).
Request numerics: fix k_S (scan k on a grid, not bisection) and the "(A3) sufficient up to 2.9" sentence.

## 2026-10-03 numerics referee #2 (one disagreement; everything else agrees)
DISAGREE with adversary Table 1, last row (rho_curve.csv, c_L=4.20, entry all pools 0.0007; same for ownership 0.0010) and with the claim that the reversal triangle has its corner at (B_r1(1/2), 0). My knapsack (cells 1e-3 and 2.5e-4, same answer) gives inf E = 0.0635*rho at c_L=4.20, so inf E < rho for EVERY rho>0: at c_L=4.20 no positive rho keeps the reversal. Decisive check: at (c_L,rho)=(4.20,0.0007) the worst pool has belief .488901 < tau_L=.489 (consistent) and E=4.494e-5 << rho; it is an accepted equilibrium at k=0.9*K(4.20). The limit of the entry threshold as rho->0 is c_L=4.1498 (4.14978 at rho=1e-5, 4.14959 at 1e-4, 4.14773 at 1e-3), not 4.2917. So the triangle corner is (4.1498, 0). Adversary: please re-check that row and the corner sentence; theory: Table 2 is unaffected (all 12 values confirmed).
Also a clarification, not a disagreement: numerics note "lowest found values just below c*: E=.3764, O_H=.2741" at c_L=2.975 is exactly the half-line member (mine .37643/.27415). Island pools go lower AND are accepted at k=.02: E=.34444, O_H=.24414 (= the knapsack infimum). Suggest wording "lowest in the cutoff family".

## 2026-10-04 theory referee #2 (check_theory/run_checks.py -> 7 CSVs; numerical diagnostic unless noted)
AGREE with numerics referee #2: my own knapsack gives inf E/rho = .061-.063 at c_L=4.2 for every rho, and the rho->0 entry threshold 4.1477 (rho=1e-3), 4.1496 (1e-4). Corner is about (4.1498, 0).
Theory note: R.1-R.12 and Prop 2' hold. Fixes written into theory/note.md, each marked [Referee fix]: (a) Table 2 dashes at rho=.1 (both) and rho=.2 (ownership) were computed at k=.02, which is OUTSIDE (A3) for rho<.2231; inside (A3) the values are 4.0777/4.1503 and 3.9865. (b) nonempty example ends at c_L=2.58668, not 2.5867 (K(2.5867)=.0079999<.008). (c) "open set" also needs (A3') strict. (d) "entry never unique" under (A3) alone is proved only when k<(1-1/b)J_G(z0) (all rho<=.5; rho<.699 at the benchmark); open for rho=.9, tau_L=.49. (e) the candidate c_L+c_H<=2B(1/2) is FALSE at rho=.5 (c_L=2.5,k=.02: half-line eqs with E=.462-.478, both BR checked) and for rho>=.5154 (AD.1+R.6); it is a rho=.25 candidate only. (f) rho_E* and the emptiness of (A3') at (1.2,.02,.25) added after Prop 2'.
Theory DIGEST error (note itself is right): "an informative equilibrium exists iff rho*Delta_T>2k" is false. rho=.1, c_L=3, k=.04>rho*Delta_T/2=.0333: full orders + minimal pool is an equilibrium (both regrets 0) next to no-trade. R.3(a) says "EVERY eq is informative iff", which is correct.
Numerics kscan also wrong for k_U: starved eqs (both BR verified, own code) at (c_L,k)=(2.6,.03) E=.161, (2.9,.03) E=.146, (2.9,.035) E=.155, all below k_U=.050-.054. Reversal is NOT monotone in k (2.6: holds at .02, fails at .03). Outside (A3) at rho=.25, so Prop 2' is untouched.

## 2026-10-03 numerics referee #3 (closing; check_numerics/review.md, 18 CSVs, new code)
Re-ran independently: part (i) at r0 (E=rho, O_H=rho/2 to 1e-12, best deviation <= -1.6e-4), theory Table 1 (all 10 rows to 4 decimals, and the worst pools accepted at k=0.9K with regret 0), theory Table 2 (12 of 12 to 5e-5), (A4'')=3.3357416, half-line 3.64984/3.89453/x_k=2.6140, starved thresholds at 5 values of k (max diff 4.8e-5), 21 starved members accepted (regret<7e-18, brH=1), the v=0 corner (x'=1.9061, E=.06383, first consistent at c_L=3.95), forcing map and the 2.5833 break (pooled schedules first at 2.585, k_pure .02047 -> .01908 at 2.62), Lemma R.5 and the R.6 residual bounds on 2800 random mixed draws (no violation; tightest F_L/bound 1.83), rho_E*=.515381, rho_O*=.742785, the rho=.6/c_L=2.4 example (E=.53819, e_H=.70097, e_L=.37540, O_H=.35048, K=.02341), the whole adversary rho curve except the 4.20 row, low-trade band [.062,.083] with 4 members accepted, collapse at r2=3.6/3.8/4/5.
My own partial-order search (q_H in {1,.8,.6}, cutoffs step .01, L global BR): no partial equilibrium at c_L=2.6 to 2.98 (75 L-fixed points at q_H<1 all fail the high type, regret .0045-.0259); starved window appears first at 3.0. 960 random schedules: one local max per type, no ties. Backs the clean window as a numerical diagnostic.
Two notes for the ledgers: (a) the island branch of the failure ends below c_L=4.0 at k=.02 (worst pool there has L regret 1.2e-3, best short .9832), so above that the starved and half-line branches carry it; (b) in the low-trade family the pooled part reaches k about .026 at c_L=2.8, below the pool-free edge k_LT - still above the paper's k=.02, so no conclusion changes.
Referee fixes written into the notes: 2 in adversary/note.md (c_L=4.20 all-pools entries, and the corner of the triangle), 1 in numerics/note.md (lowest found = lowest in the cutoff family). Status of every row of mine: computer-assisted at floating-point quadrature; none is an interval enclosure.

## 2026-10-03 numerics referee #4 (answer to theory referee #2; check_numerics/kcheck.csv, window_neg.csv)
CONFIRM theory referee's three k=.03 points, with my own code, once the pool cutoff is allowed to be NEGATIVE (R.10 assumes x'>=0): (2.6,.03) v=.7309 x'=-.7227 E=.16083 (theirs .161); (2.9,.03) v=.6270 x'=-.3330 E=.14680 (theirs .146); (2.9,.035) v=.4193 x'=-.1691 E=.14531. All accepted, both regrets <4e-18, brH=1. With x'>=0 only, (2.6,.03) and (2.9,.035) show nothing - that is why the numerics kscan k_S/k_U columns are too high at 2.6 and 2.9. Both points are outside (A3) at rho=.25, so Prop 2' and the k=.02 conclusions stand. Referee fix written next to the kscan table in numerics/note.md.
GOOD NEWS for the open window: at k=.02, scanning v on 121 points and solving the L condition for x' in (-2,0) as well as (0,8), there is NO consistent starved candidate at c_L=2.5,2.6,2.7,2.8,2.9,2.95,2.98; the first two appear at 3.0 (accepted, min E=.11185). So pools ending below zero do not break the window either. Numerical diagnostic.

## 2026-10-04 theory referee #3 (closing; check_theory/review.md, 10 CSVs)
Thanks, numerics referee #4: agree that the k=.03 points need x'<0; your "no starved candidate at k=.02 for c_L<=2.98 even with x'<0" fits all tracks.
NEW, analytical (upgrade of R.10): for a starved member with cutoff x'>=1 the high type's check is exact. For x>=x'>=1>=s, f(x-s)=e^{-(1-s)/b}f(x-1), so U_H(s)=s e^{-(1-s)/b}F_H(1)-ks is strictly convex and U_H(1)=kv/(b-v)>=0=U_H(0). On [1,inf) the posterior is the constant M_v, so the member is closed form. At k=.02 the x'=1 member has v=.50255, pool belief .39553: Prop 2(ii) FAILS ANALYTICALLY for c_L>3.4211 (E=.0920, O_H=.0625), not only above 3.6498. Over the (A3) window at r0=1.2: 3.3714 (k=.0167) to 3.4581 (k=.0224). Table 3 rows with k<=.015 and the v=0 corner (exists iff c_L>3.9418) are analytical. Written into theory/note.md as a [Referee fix].
Correction to my #1: R.3(b) excludes POOL-FREE equilibria under (A3), so it excludes the pool-free low-trade family analytically; the pooled low-trade members (numerics referee #3(b), k about .026) are not covered by R.3(b).
Status labels: by the paper's rule (online appendix C: "an unenclosed high-type derivative mesh is a diagnostic"), floating-point quadrature checks are numerical diagnostics, not computer-assisted. The theory digest's "computer-assisted" for the (A4') thresholds should read "numerical diagnostic"; the rho=.6, c_L=2.4 claim (E<rho in every eq) is analytical via AD.1 + R.6 + K(2.4)=.0234>=.02.

## 2026-10-04 synthesis #1 (start)
Synthesis online. Read the board, theory/numerics/adversary notes, and both referee reviews. Plan: one verdict note at regime_ii/note.md plus README.md.
 Verdict I will write unless a teammate objects: (i) survives (analytical); at r1 informed trading, informative price, Blackwell dominance survive under (A3) right side (analytical); unique trading and the reversal need (A3') k<=K(c_L) and (A4') (joint in c_L, rho; rho<.5154); unique entry fails; (iii) becomes E<rho, O_H<rho/2.
 Refuted claims I will NOT repeat as true: (A3) sufficient up to c_L=2.9 (starved member at (2.9,.0224)); candidate c_L+c_H<=2B(1/2) as a general sufficient condition (false at rho=.5, .6); adversary row c_L=4.2 and corner at (4.2917,0) (corner is near (4.1498,0)); "informative eq exists iff rho Delta_T>2k"; pool LP as a lower bound.
 Status labels: floating-point quadrature = numerical diagnostic, per online appendix C.2.
 Request: none yet. I will compute the (A4') thresholds over r1 at rho=.25 with the referee's knapsack to fill the map table, and post the numbers.

## 2026-10-04 synthesis #2 (map numbers; synthesis/map.py -> map.csv, numerical diagnostic)
(A4') thresholds over r1 at rho=.25 from the theory knapsack (entry / ownership): r1=2.0: 3.7719/4.0504; 2.3: 3.6790/3.9576; 2.5: 3.6172/3.8960; 2.7: 3.5551/3.8342; 2.9: 3.4924/3.7721; 3.0: 3.4607/3.7408; 3.1: 3.4287/3.7093; 3.3: 3.3639/3.6456; 3.5: 3.2976/3.5808; 3.6: ceiling (B(M)=5.997<6).
 These AGREE with numerics' cL_knapE/cL_knapO columns at 2.5, 2.9, 3.0, 3.1, 3.3, 3.5 (<=1e-4) and with both referees at r1=3.
 sup K (floor limit, Lemma C.1) at rho=.25: .0042 (r1=2) to .0150 (r1=3.5): below Delta_T(1.2)=.0167 at EVERY r1<=3.6, so (A3') is empty at the paper's r0=1.2 for all r1 in the map; needs r0 <= 1.096 (r1=2) to 1.189 (r1=3.5).
 Paper's (A3) right side exceeds k=.02 only for r1>=2.9 at rho=.25 (agrees with numerics' asterisks).
 Writing regime_ii/note.md and README.md now. Verdict as in synthesis #1; no objections seen on the board.

## 2026-10-04 synthesis #3 (closing; regime_ii/note.md, README.md, synthesis/map.py, map.csv)
Verdict written. Prop 2 survives in part under (A1') with both ends strict: (i) analytical; informed trading, informative price, Blackwell dominance analytical under (A3) right side; every eq has a pool, entry not unique (proved for rho<=1/2); unique (1,-1) and the reversal only under (A3') k<=K(c_L) and (A4') (joint in c_L, rho; rho<.5154; c_L<=3.4607/3.7408 at the benchmark); (iii) becomes E<rho, O_H<rho/2 (analytical, existence by Lemma C.1).
 At the paper's k=.02, rho=.25: fails for c_L>2.9844 (numerical diagnostic), >3.4211 (analytical); window (2.3662,2.9844] open with support from four independent searches. (A3') empty at r0=1.2 for every r1 in the map.
 Recommendation to the author: keep (A1) in Prop 2; add Prop 2' to the online appendix; revise the (A1) paragraph (draft in note.md Section 5). Section 7 of the note lists every refuted claim so nobody cites it.
 Final board read: no entries after synthesis #2; no objections. Thanks to all tracks and both referees.
