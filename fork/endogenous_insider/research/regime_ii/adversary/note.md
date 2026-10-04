---
title: "Breaking Proposition 2 without the floor: the adversary's ledger"
subtitle: "Adversary and economics track, regime II team"
date: "2026-10-03"
---

This note belongs to `fork/endogenous_insider/research/regime_ii/`. It uses the notation of `paper/main.md`, of the CD note (`research/cost_distribution/note.md`), and of the theory note (`theory/note.md`, results R.1 to R.12 and Proposition 2'). The question is the team's: replace the floor (A1) by the regime II condition (A1'), $B_{r_1}(m)<c_L<B_{r_1}(\tfrac12)$, and decide what survives of Proposition 2. The adversary's job is to break the regime II version. Every claim carries its status: analytical, computer-assisted, numerical diagnostic, or open. All numbers come from `attack.py` and the CSV files in this folder (Section 7).

## 1. Short answer

The regime II version of Proposition 2 breaks in two separate ways. The theory and numerics tracks found the first: at the paper's trading cost, equilibria with less entry than at $r_0$ exist once $c_L$ passes $2.9844$ (starved family), and a replacement bound (A3') on the trading cost restores unique full orders. The adversary adds the second, which does not depend on the trading cost at all: **the share $\rho$ of cheap challengers.** In regime II every full-order equilibrium pools the lower plateau, so it loses at least $\rho\Pr(X\le-1)$ of cheap entry, and it gains at most $(1-\rho)\Pr(\mu_X\ge\tau_H)$ of expensive entry. The gain beats the loss only when $\rho$ is small. At the benchmark this is $\rho<0.5154$ at the floor and $\rho<0.2502$ at $c_L=3.46$ (Theorem AD.1, analytical; Table 1). A verified example at the paper's own $k=0.02$ and $r_0=1.2$ with $\rho=0.6$, $c_L=2.4$ satisfies (A1'), (A2), (A3) and (A3'), has full orders in every equilibrium, and has entry at most $0.538<0.6$ in every equilibrium (Section 3, computer-assisted). So condition (A4') of Proposition 2' is not a technical closure: it is a restriction on $\rho$ that excludes half of the parameter space.

The second message is a confirmation. Every other attack fails. The clean window $c_L\in(2.3662,2.9844]$ at the paper's trading cost and $\rho=0.25$ survives low-type mixtures, pools that end below zero, islands, and partial buys (Section 5, numerical diagnostic). The high type's full purchase along the starved family is now certified by a derivative argument, not only on a grid (Section 4). The replacement (A3') is correct but, at $\rho=0.25$, it cannot be met with the paper's $r_0=1.2$ (Section 6).

What survives, in one line: part (i) always; informed trading, an informative price and Blackwell dominance always under the right side of (A3); unique full orders only under (A3'); entry and ownership above their $r_0$ values only when $\rho$ is below the curves of Table 1, which is Proposition 2' with (A4') made explicit in $\rho$; part (iii) as "entry falls below $\rho$" (R.12).

## 2. The attack ledger

| # | target | attack | result | status |
|---|---|---|---|---|
| 1 | Prop 2' (ii), entry | large $\rho$: the plateau pool costs $\rho\Pr(X\le-1)$, the top gains $(1-\rho)\Pr(\mu_X\ge\tau_H)$ | breaks for $\rho\ge\rho_E^*=0.5154$ at every regime II $c_L$; exact curve in Table 1 | analytical; examples computer-assisted |
| 2 | Prop 2' (ii), ownership | same | breaks for $\rho>\rho_O^*=0.7428$ at every regime II $c_L$ | analytical |
| 3 | R.10(b), high type in the starved family | certificate: envelope far from $q=1$, derivative sign near it | 54 members certified, margins $\ge5\times10^{-4}$ (far), $\ge0.009$ (near) | computer-assisted (floating-point quadrature) |
| 4 | the clean window $(2.59,2.98]$ at $k=0.02$ | low-type two-point mixtures, pools ending in $[-1,0.5]$, islands, 745 consistent schedules | every schedule has one local maximum per type; no fixed point | numerical diagnostic |
| 5 | (A3') | feasibility with the paper's $r_0$ | empty at $(r_0,\rho)=(1.2,0.25)$; needs $r_0\le1.157$ | closed form |
| 6 | teammates' numbers | independent quadrature | starved member at $c_L=3.5$, thresholds $3.6498$, $3.8945$, $3.4607$, $K(3)=0.00648$ all reproduced | computer-assisted / closed form |
| 7 | weak upper end of (A1') | $c_L=B_{r_1}(\tfrac12)$ with the tie rule | adds nothing new: the half-line family is cut only by the investor test, entry down to $0.0638$ | analytical (CD.7 referee fix) |

## 3. The share of cheap challengers breaks the entry reversal

All objects are at $r_1$. Write $\pi_0=\Pr(X\le-1)=\tfrac14(1+e^{-2/b})$ for the lower plateau under full orders and $a=\tfrac12(\alpha_H+\alpha_L)=S_X(x^*)$ for the probability of expensive entry under full orders without a pool, with $\alpha_H,\alpha_L,x^*$ from (12). Both depend only on $b$ and $\tau_H$. At the benchmark $\pi_0=0.34197$ and $a=0.36368$.

**Theorem AD.1 (the cheap-type share; analytical).** *Assume (A1') and (A2). (a) In every equilibrium at $r_1$ with full orders,*

$$
\mathsf E\le\mathsf E_0(\tau_L,\rho)<\mathsf E_0^+(\rho):=\rho(1-\pi_0)+(1-\rho)a,
\qquad
e_H\le e_{H,0}(\tau_L,\rho)<e_{H}^+(\rho):=\rho\,S(-2)+(1-\rho)\alpha_H .
$$

*(b) Put $\rho_E^*=a/(a+\pi_0)$ and $\rho_O^*=\alpha_H/(\alpha_H+F(-2))$. If $\rho\ge\rho_E^*$, every full-order equilibrium at every $c_L$ in regime II has $\mathsf E<\rho$. If $\rho>\rho_O^*$, every full-order equilibrium at every $c_L$ in regime II has $\mathsf O_H<\rho/2$.*

*(c) The full-order equilibrium with the minimal pool exists whenever $k\le(1-\tfrac1b)\Delta_T(r_1)\,m/2$; this holds under (A3) when $\rho\le\tfrac12$, and at the benchmark for every $\rho$ since $(1-\tfrac1b)\Delta_T m/2=0.0448>0.02$. Under (A3') every equilibrium has full orders (R.6), so (b) then holds in every equilibrium.*

*At the benchmark $\rho_E^*=0.51538$ and $\rho_O^*=0.74278$ ($r_1=3$); $0.5262$ and $0.7506$ at $r_1=2.5$; $0.5026$ and $0.7331$ at $r_1=3.5$.*

*Proof.* (a) Under full orders the forced pool is $Z_0=(-\infty,z_0)$ with $z_0=\tfrac b2\operatorname{logit}\tau_L\in(-1,0)$ (CD.7(a)), and every equilibrium pool $N$ contains $Z_0$ (CD.2(c)). Entry is $\mathsf E=\int_{N^c}\varphi(\mu_X)\,dP$ by (R.0) and $\varphi\ge0$, so $\mathsf E\le\int_{Z_0^c}\varphi(\mu_X)\,dP=\mathsf E_0$. On $Z_0^c=[z_0,\infty)$ the cheap type enters everywhere and the expensive type enters on $[x^*,\infty)$, so $\mathsf E_0=\rho S_X(z_0)+(1-\rho)S_X(x^*)$. Since $z_0>-1$ and $S_X$ is strictly decreasing, $S_X(z_0)<S_X(-1)=1-\pi_0$, which gives the strict bound. The same argument with the high-type flow law gives $e_H\le e_{H,0}=\rho S(z_0-1)+(1-\rho)\alpha_H<\rho S(-2)+(1-\rho)\alpha_H$. (b) $\mathsf E_0^+(\rho)-\rho=a-\rho(a+\pi_0)\le0$ exactly when $\rho\ge\rho_E^*$; then $\mathsf E<\mathsf E_0^+\le\rho$. For ownership, $e_H^+(\rho)-\rho=(1-\rho)\alpha_H-\rho F(-2)<0$ exactly when $\rho>\rho_O^*$, and $\mathsf O_H=e_H/2$ because $h>r$. (c) By CD.7(d) the minimal pool is consistent, and it is an equilibrium if $k\le(1-\tfrac1b)J_G(z_0)$. By Lemma CD.6 with $g_M=1$, $J_G(z_0)\ge\Delta_T m/2$ (the upper plateau term alone). Under (A3), $k<(1-\tfrac1b)\rho m\Delta_T\le(1-\tfrac1b)m\Delta_T/2$ when $\rho\le\tfrac12$. The last claim is Proposition R.6. $\square$

The bound in (a) is attained in the limit $c_L\downarrow B_{r_1}(m)$. So the theorem says more than "large $\rho$ fails": it says that entry is discontinuous at the floor. At $c_L=B_{r_1}(m)$ the tie rule keeps the cheap type on the plateau and $\mathsf E=\rho+(1-\rho)a$; one cent above, the plateau becomes a pool and entry drops by $\rho\pi_0$. At the benchmark with $\rho=0.25$ this is a drop from $0.5228$ to $0.4371$; with $\rho=0.6$, from $0.7455$ to $0.5400$, below the $r_0$ value $0.6$.

**The exact curve.** Under (A3') the equilibrium set is all consistent pools (R.6), and the smallest entry over it is the bathtub value of R.7. Table 1 gives, for each $c_L$, the largest $\rho$ at which the reversal holds in every equilibrium: the root of $\mathsf E_0-V_E=\rho$ (all pools) and of $\mathsf E_0=\rho$ (minimal pool only). The all-pools column is the exact boundary of (A4'); its value $0.2502$ at $c_L=3.46$ is the theory track's threshold $3.4607$ read the other way.

**Table 1. Largest $\rho$ at which the reversal holds in every full-order equilibrium, $r_1=3$** (`rho_curve.csv`; minimal-pool columns are closed-form roots, all-pools columns are fractional-knapsack values on cells of width $0.002$, numerical diagnostic).

| $c_L$ | $\tau_L$ | entry, all pools | entry, minimal pool | ownership, all pools | ownership, minimal pool |
|---|---|---|---|---|---|
| 2.37 | 0.269 | 0.5034 | 0.5151 | 0.7332 | 0.7426 |
| 2.50 | 0.285 | 0.4488 | 0.5056 | 0.6760 | 0.7350 |
| 2.80 | 0.321 | 0.3950 | 0.4866 | 0.5979 | 0.7181 |
| 3.00 | 0.345 | 0.3574 | 0.4755 | 0.5410 | 0.7070 |
| 3.46 | 0.400 | 0.2502 | 0.4535 | 0.3787 | 0.6820 |
| 3.74 | 0.434 | 0.1654 | 0.4418 | 0.2504 | 0.6668 |
| 4.00 | 0.465 | 0.0676 | 0.4317 | 0.1023 | 0.6526 |
| 4.20 | 0.489 | 0.0007 | 0.4244 | 0.0010 | 0.6416 |

[Referee fix: the two all-pools entries in this last row should be $0$, not $0.0007$ and $0.0010$. An independent knapsack (cells $10^{-3}$ and $2.5\times10^{-4}$, same answer) gives $\inf\mathsf E=0.0635\rho$ and $\inf e_H=0.0841\rho$ at $c_L=4.20$, so both are below $\rho$ for every $\rho>0$. At $(c_L,\rho)=(4.20,0.0007)$ the worst pool has belief $0.488901<\tau_L=0.489$ and $\mathsf E=4.49\times10^{-5}$, and it is an accepted equilibrium at $k=0.9K(4.20)$. The all-pools thresholds in the other rows are confirmed to four decimals.]

So the region where Proposition 2' delivers the entry reversal is the set below the third column: a triangle in $(c_L,\rho)$ with its corner at $(B_{r_1}(\tfrac12),0)$ [Referee fix: the corner is at $c_L=4.1498$, not at $B_{r_1}(\tfrac12)=4.2917$: the entry threshold tends to $4.14978$ as $\rho\downarrow0$ ($4.14959$ at $\rho=10^{-4}$, $4.14773$ at $10^{-3}$), because the worst pool keeps a fixed share of the expensive entry whatever $\rho$ is] and its top at the floor limit $\rho_E^*=0.5154$ (the all-pools and minimal-pool thresholds meet there, because the pool budget vanishes at the floor; at $c_L=2.3662$ the all-pools root is already $0.5145$). For the paper's $\rho=0.25$ it is $c_L\le3.46$; for $\rho=0.4$ it is $c_L\le2.7716$; for $\rho\ge0.5154$ it is empty.

**A verified example** (`counterexamples.csv`, rows 1 to 8; computer-assisted at floating-point quadrature). Benchmark primitives, $k=0.02$, $r_0=1.2$, $r_1=3$, $\rho=0.6$, $c_L=2.4$, so $\tau_L=0.273$ and the economy is in regime II. Conditions: (A1') holds; (A2) holds ($B_{1.2}(\tfrac12)=4.804<6<6.217$); (A3) holds ($0.0167<0.02<0.0538$); (A3') holds ($K(2.4)=0.0234\ge0.02$). By R.6 every equilibrium has orders $(1,-1)$ and a pool $N\supseteq(-\infty,-0.979)$. The minimal pool: belief $0.2690<\tau_L$, probability $0.345$, both types' full orders are the unique global best responses (regret $0$, certificates: far margins $0.0090$ and $0.0037$, near margins $0.143$ and $0.055$). Outcomes: $\mathsf E=0.5382<0.6$, $e_H=0.701$, $e_L=0.375$, $\mathsf O_H=0.350>0.3$. Every other consistent pool has lower entry (R.7). So at $r_1$ the price is informative, the investor trades fully, and total entry is below its $r_0$ level in every equilibrium, while high-value ownership is above it. With $\rho=0.75$ or $0.8$ ownership fails too ($\mathsf O_H=0.372<0.375$ and $0.379<0.4$). With $\rho=0.5$ the minimal pool still passes ($\mathsf E=0.509>0.5$), as $\rho_E^*=0.5154$ says, but the all-pools threshold at $c_L=2.4$ is $0.4807$, so some equilibrium already fails.

The numerics track tested the bound with its own cutoff-scan engine (numerics #5, `numerics/rho_check.csv`): at $c_L=B_{r_1}(m)+10^{-4}$ the equilibrium has $\mathsf E=0.5154$ when $\rho=0.5154$, and for $\rho\ge0.5154$ no equilibrium has $\mathsf E>\rho$ at any of its regime II points; at $\rho=0.5$ and $c_L=2.666$ the reversal fails in every equilibrium it finds. These agree with Theorem AD.1 and Table 1 ($0.5145$ at $c_L=2.3662$, $0.4488$ at $2.5$).

The decomposition of the example is the whole story. Expensive entry recruited by good prices: $(1-\rho)a=0.4\times0.3637=0.1455$. Cheap entry lost in the pool: $\rho\Pr(Z_0)=0.6\times0.3455=0.2073$. Net: $-0.062$.

## 4. The high type along the starved family is certified

Proposition R.10(a) proves the low type's side of the starved family in closed form; part (b) checks the high type on a grid. The adversary tried to break the high type's full purchase and could not. `starved_hcheck.csv` certifies $q_H=1$ at 54 members ($c_L\in\{3,3.1,3.25,3.5,3.75,3.9\}$, nine shorts $v$ from $0.05$ to $v_H$), with the method of `model.certify`:

- far from $q=1$: on every cell of a 401-point grid at distance at least $0.06$ from $1$, $U_H(s)\le\min$ of the two endpoint envelopes built from $|F_H'|\le F_H/b$ (each envelope is convex in $s$, so its maximum is at a cell end); the largest such bound is below $U_H(1)$ by at least $5.1\times10^{-4}$;
- near $q=1$: on a grid of step $0.0005$ on $[0.94,1]$, $U_H'(s)=F_H+sF_H'-k$ is computed by quadrature ($F_H'=(H_+-H_-)/b$ from the parts of $F_H$ above and below the kernel centre), and $|U_H''|\le F_H(2/b+1/b^2)+\Delta_T/b^2$ bounds its change between grid points; $U_H'$ exceeds that slack by at least $0.0092$, so $U_H$ is strictly increasing on $[0.94,1]$.

The identity $U_H(1)=kv/(b-v)$ of R.10(a) holds to $10^{-6}$ at every member. The members with $\bar\mu_N<\tau_L$ are exactly those the theory track lists (for instance $v\ge0.655$ at $c_L=3.25$, $v\ge0.482$ at $c_L=3.5$). Status of R.10(b) after this check: computer-assisted at floating-point quadrature; an interval enclosure is still open.

## 5. The clean window survives mixtures and odd pools

The open item of both tracks is $c_L\in(2.59,2.9844]$ at $k=0.02$, $\rho=0.25$: full orders are no longer forced over pure half-line schedules, but no equilibrium with $\mathsf E\le\rho$ is known. The adversary's attack there is the low type's mixture. Mixing lowers both ends of the posterior range (Jensen on $e^{\pm(1+v)/b}$), so a mixture over $\{0,-1\}$ with weight $0.788$ on $-1$ keeps every belief below $\tau_H$ and still pools for $c_L>2.512$, below the pure-order break point $2.5833$ of Lemma R.11. If such a mixture were an equilibrium it would kill the candidate $c_L+c_H\le2B_{r_1}(\tfrac12)$.

It is not, and the reason is structural. Write $F_-(s)$ and $F_+(s)$ for the parts of $F_L(s)$ from flows below and above the kernel centre $-s$. Then $F_L'=(F_--F_+)/b$ and $F_L''=(F_L-A_L(-s)\mathbf 1_A(-s))/b^2$, so

$$
U_L''(s)=\frac1b\Big[2(F_--F_+)+\frac sb\big(F_-+F_+-A_L(-s)\mathbf 1_A(-s)\big)\Big]
\le\frac1b\Big[F_-\Big(2+\frac sb\Big)-F_+\Big(2-\frac sb\Big)\Big].
$$

If the entry set satisfies $\inf A\ge-s_0$, then $F_-=0$ on $[s_0,1]$ and $U_L$ is strictly concave there (analytical; this is the exponential form in the proof of R.10(a)). A mixture therefore needs a second support point below $s_0=-\inf A$ and a non-concave payoff there, which needs $F_-\ge F_+(2-s/b)/(2+s/b)$, about $0.6F_+$ at $b=2$: the residual-weighted mass of the entry set below $-s$ must be at least sixty percent of the mass above. With the pool at the bottom and $A_L=\rho\Delta_T\mu_X$ smallest there, this does not happen.

The lattice audit (`mixed_window.csv`, numerical diagnostic): $c_L\in\{2.6,2.7,2.8,2.9,2.98\}$, high type at $1$, low type mixing over $\{-v_1,-v_2\}$ with $v_1\in\{0,0.2,0.4,0.6\}$, $v_2\in\{0.5,0.7,0.74,0.9,1\}$, weights $\{0.2,0.5,0.8\}$, pools $(-\infty,x')$ with $x'\in\{-1,\dots,0.5\}$, with or without an island $[0.6,1.1)$ or a top pool $[1.5,\infty)$. Of $745$ consistent schedules ($28$ at $c_L=2.6$, $273$ at $2.98$), every one gives each type a payoff with exactly one local maximum on a 101-point grid. The low type's best response is always a single short of size at least $0.77$, above $v_H=0.7424$, so against every starved schedule the low type wants to short enough to recruit the expensive type. At every best response $F_-=0$. No schedule has the low type indifferent between its two support points. This agrees with the numerics track's random audit (numerics #4) and with its all-pool lattice LP, which finds only $(1,-1)$ feasible for $c_L\le3.05$.

Verdict on the window: open as a theorem, but no attack from mixtures, islands, pools below zero, or partial buys produces a counterexample. The candidate sufficient condition $c_L+c_H\le2B_{r_1}(\tfrac12)$ stands for pure orders (R.11) and is untouched by the mixtures tried here.

## 6. Where (A3') can and cannot be met

(A3') is $\Delta_T(r_0)<k\le K(c_L)$ with $K\le\tfrac12(1-\tfrac1b)\rho m\Delta_T(r_1)$ near the floor and smaller above it. Since $\Delta_T(r_0)=(r_0-\ell)^2/(2r_0)$, the largest weak strength compatible with (A3') is $r_0^{\max}=\ell+K+\sqrt{K^2+2\ell K}$ (`a3prime_feasible.csv`, closed form):

| $\rho$ | $c_L=2.37$ | $2.5$ | $3.0$ | $3.46$ |
|---|---|---|---|---|
| 0.25 | 1.157 | 1.140 | 1.120 | 1.110 |
| 0.5 | 1.229 | 1.203 | 1.174 | 1.158 |
| 0.6 | 1.254 | 1.225 | 1.193 | 1.175 |

At the paper's $\rho=0.25$, (A3') is empty for $r_0=1.2$ at every regime II $c_L$, and $k=0.02$ is never allowed ($K\le0.0107$). Proposition 2' therefore cannot be illustrated at the paper's benchmark triple $(r_0,k,\rho)=(1.2,0.02,0.25)$; it needs a weaker weak incumbent and a smaller trading cost, as in the theory track's example $(1.1,0.008)$. Since $K$ is linear in $\rho$, $K$ at the floor reaches $0.02$ at $\rho=0.4462$; above that share the paper's $r_0$ and $k$ are allowed near the floor, which is exactly where Theorem AD.1 bites. So in the $(c_L,\rho)$ plane the two conditions pull apart: (A3') wants $\rho$ large, (A4') wants $\rho$ small. At $r_0=1.2$ and $k=0.02$ their intersection is a sliver above the floor: $\rho\in(0.4462,0.5154)$ with $c_L\le2.3677$ at $\rho=0.46$, $c_L\le2.3752$ at $\rho=0.48$, $c_L\le2.3726$ at $\rho=0.5$, and $c_L\le2.3669$ at $\rho=0.51$ (the binding condition switches from (A3') to (A4') at about $\rho=0.49$). Proposition 2' holds there, with entry between $0.5024$ and $0.5106$ against $\rho=0.5$.

## 7. Economics: what regime II means for the paper's story

**Who prepares.** In regime I the cheap type prepares at every price and the expensive type prepares after good prices. In regime II the cheap type prepares at the prior and after good prices, but not after bad prices. Information now moves both types. The expensive type is recruited by good news; the cheap type is deterred by bad news.

**Why bad prices deter the cheap type.** Its cost exceeds the profit at the worst belief $m$. Under full orders the posterior on the lower plateau $x\le-1$ is exactly $m$, so the plateau is a no-entry region with probability $\pi_0=0.342$. The region is self-fulfilling and can be larger than the plateau: the market maker prices every flow where nobody enters at $t_0$, the challenger sees $t_0$ and holds a pooled belief below $\tau_L$, and nobody enters. Any Borel set with pooled belief below $\tau_L$ works, which is why entry is never unique (R.3, R.7).

**Two forces.** Entry changes by $(1-\rho)\Pr(\text{good news})-\rho\Pr(\text{pool})$. Competition creates competition when the first term wins. The weight on the second term is the share of cheap challengers. This is Theorem AD.1: the paper's result in regime II is a statement about economies where cheap challengers are rare. When they are common, a stronger incumbent that makes the price informative destroys more cheap preparation after bad news than it creates expensive preparation after good news, and total entry falls below its uninformative level. The force is new relative to the paper: with the floor, information can only add entry (Proposition A.3 is about a fixed experiment; here the experiment changes and the cheap type responds to it).

**Information sorts even when it does not recruit.** In the $\rho=0.6$ example entry falls but high-value ownership rises: $e_L$ falls from $0.6$ to $0.375$ while $e_H$ rises from $0.6$ to $0.701$. The pool sits on low flows, which are more likely in the low state, so the cheap entry it removes is mostly low-value entry. Ownership survives for $\rho<\rho_O^*=0.743$, entry only for $\rho<\rho_E^*=0.515$. The paper's "competition creates competition" becomes, in regime II, "competition sorts competition": the price channel raises the quality of entrants over a wider range than it raises their number.

**A third effect through trading.** The pool removes the short seller's residual on low flows. The low type then shorts less, and a short below $v_H$ keeps every belief below $\tau_H$. Information then recruits nobody and only deters (the starved family). This is a feedback from the entry side to the trading side that regime I does not have, and it is the reason the paper's trading-cost bound (A3) stops working above $c_L=2.9844$ at the benchmark.

**For the paper's framing of (A1).** The paper calls the floor "part of the mechanism, not a numerical regularizer" because it supplies a base return to informed trading. Regime II shows a second job of the floor: it fixes the cheap type's entry at $\rho$ regardless of the price, so that information can only recruit. Without it the floor's first job survives (the cheap type still enters at the prior, so trading is still worthwhile) but the second does not. The honest statement is that (A1) is sufficient for the reversal and not necessary, and that its weakest replacement is a joint restriction on $c_L$ and $\rho$ (Table 1) together with the smaller trading cost (A3').

## 8. Draft replacement paragraph for Section 4.1

The result survives in a restricted form, so here is a draft for the paragraph that discusses condition (A1), to replace "Condition (A1) ensures that low-cost preparation is worthwhile even at the lowest feasible belief. ... The floor is therefore part of the mechanism, not a numerical regularizer."

> Condition (A1) is a participation floor: low-cost preparation is worthwhile even at the lowest feasible belief. It does two jobs. First, some preparation makes the target's proceeds sensitive to challenger quality before favorable information recruits additional preparation, which supplies a base return to revealing that quality through trading. Second, it makes low-cost preparation insensitive to the price, so that information can only add entry. The first job survives without the floor: if $c_L$ lies between $B_{r_1}(m)$ and $B_{r_1}(1/2)$, the low-cost challenger still prepares at the prior, no uninformative-price equilibrium exists, and every equilibrium at $r_1$ has correctly signed informed trading and an informative price. The second job does not. Unfavorable prices then deter the low-cost challenger, every equilibrium pools a positive-probability set of unfavorable flows at the no-entry price, on-path entry is no longer unique, and total entry rises above $\rho$ only if the expensive entry recruited by favorable prices exceeds the cheap entry lost in the pool. The balance depends on the share of low-cost challengers: at the benchmark the reversal holds in every equilibrium only for $\rho$ below about one half near $B_{r_1}(m)$ and below $0.25$ at $c_L=3.46$, and it needs a trading cost below a smaller bound than (A3), because the pool also weakens the short seller's incentive. The appendix of the online supplement states the exact conditions. The floor is therefore part of the mechanism in two senses: it supplies the base return to informed trading, and it keeps information from deterring the entry it is meant to create.

## 9. Open items

1. Theorem AD.1 covers full-order equilibria. Under (A3) alone, partial-order equilibria with $\mathsf E\ge\rho$ at large $\rho$ are not excluded, so "every equilibrium" at $\rho\ge\rho_E^*$ is proved only under (A3'). Status: open under (A3), analytical under (A3').
2. The window $(2.59,2.9844]$ at $k=0.02$, $\rho=0.25$: no counterexample from any class tried; a proof that $U_L$ has one maximum against every consistent schedule would close it. Status: open.
3. An interval enclosure of the starved family's high-type check. Status: open (floating-point certificate done).
4. Whether $\rho_E^*$ depends on $r_1$ through $\tau_H$ only is exact; a version for the moderate-value specification of Section 5.2 is not computed. Status: open.

## 10. Files

- `model.py`: economy, Laplace helpers, full-order closed forms ($z_0$, $x^*$, $\mathsf E_0$, $e_{H,0}$, $J_{\min}$, $K$), $\rho^*$ formulas, fractional-knapsack bathtub, quadrature evaluator for finite mixtures with arbitrary pools, global best response, and the certificate. Independent of the numerics and theory code.
- `attack.py`: writes `rho_star.csv`, `rho_floor.csv`, `rho_curve.csv`, `halfline_thresholds.csv`, `a3prime_feasible.csv`, `counterexamples.csv`, `starved_hcheck.csv`, `mixed_window.csv`. Run `python3 attack.py all` (about three minutes) and `python3 attack.py mixed` (about six minutes).
- Status of CSV rows: closed-form rows are marked; `counterexamples.csv` rows with both certificates are computer-assisted at floating-point quadrature; everything else is a numerical diagnostic.
