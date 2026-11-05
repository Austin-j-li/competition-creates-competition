# Q4. Normalization: can we set $c_L = 1$ and simplify the calculation?

Memo to the author. Date: 21 October 2026.
Script: `audit/alex_meeting_2026_10_21/scripts/Q4_normalization/normalization_check.py`
(printed output saved next to it in `output.txt`).

Short answer. Setting $c_L = 1$ is a legal choice of unit, but it simplifies nothing. The reason is that $c_L$ appears in no closed form of the paper. It appears only in participation-floor inequalities. Two other moves do simplify: choose the unit by $\ell = 1$, and treat $c_L$ as a slack parameter (work with $c_L = 0$). Details follow.

---

## 1. Question and reading

The supervisor asked: "for the low/high cost, can we normalize $c_L$ to be 1 and simplify some of the calculation?"

I read this in three parts.

1. Is $c_L = 1$ without loss of generality (WLOG)?
2. Does it shorten any formula?
3. If not, which normalization does, and what does each choice cost?

I compare these normalizations: $c_L = 1$, $c_L = 0$, $\ell = 1$, $h - \ell = 1$, $p \to 0$, and costs written as ratios. I use the Overleaf master (`overleaf/paper/main.tex`, `online_appendix.tex`). Line numbers below refer to `main.tex` unless I write "OA".

## 2. Formal setup

Notation is the paper's. Money primitives, all measured per target share:

$$
h,\ \ell,\ p,\ r,\ c_L,\ c_H,\ k \qquad (\text{also } \varepsilon_C,\ \varepsilon_V,\ \text{the seller's reserve, a dividend}).
$$

The incumbent value $R \sim U[0,r]$ is also in money. Dimensionless primitives: $\rho$, $b$, the prior $1/2$, the bargaining weight $\eta$.

Flow primitives: orders $q$, noise $Z$, flow $X = q + Z$, the order bound $\bar u = 1$, and the noise scale $b$. In the paper, $\bar u = 1$ fixes the flow unit. So $b$ is a ratio: noise scale divided by the largest order.

The target standalone value is already normalized to $0$ (Section 2.2). That fixes the *location* of money.

The auction objects are eq. (4). I write $\Delta_T(r) = (r-\ell)^2/(2r)$ and $B_r(\mu) = g_L + \mu(g_H - g_L)$.

## 3. Results

### 3.1 Money scale invariance — **analytical**

**Claim 1.** Fix $\lambda > 0$. Multiply every money primitive by $\lambda$: $h, \ell, p, c_L, c_H, k$, and the incumbent support $r$ (so $R \to \lambda R$). Keep $\rho, b$ and the order bound unchanged. Then:

- the set of equilibria is unchanged in orders, beliefs $\mu_X$, preparation decisions, and ownership;
- the entry probability $\mathsf E$ and ownership $\mathsf O_H$ are unchanged;
- prices, target revenue $\mathcal R_T$, net surplus $\mathcal W$, and investor payoffs are multiplied by $\lambda$;
- conditions (A1)–(A3) hold in one economy if and only if they hold in the other.

*Derivation.*

*Step 1: auction.* Bids are truthful. With values $\lambda\theta$, reserve $\lambda p$, and incumbent value $\lambda R$, the winner does not change. Each payment is $\max\{\lambda p, \cdot\}$ of scaled bids, so it equals $\lambda$ times the old payment. Each rent scales by $\lambda$ pointwise. So $t_0, t_H, t_L, g_H, g_L$ and $B_r(\mu)$ scale by $\lambda$. Check with eq. (4): $t_0 = p(1 - p/r)$ becomes $\lambda p (1 - \lambda p/(\lambda r)) = \lambda t_0$. Also $\Delta_T = (r - \ell)^2/(2r)$ is homogeneous of degree one.

*Step 2: beliefs.* The flow posterior $\mu_X$ depends only on the order distributions and on the noise density $f$. None of these contain money. So $\mu_X$ is unchanged. This includes eq. (7) and the bounds $m, M$.

*Step 3: preparation.* The rule is $\mathbf 1\{B_r(\mu) \ge C\}$. Both sides scale by $\lambda$. So the rule is unchanged.

*Step 4: pricing.* $V_T$ is a money payoff per share. It scales by $\lambda$ given the same preparation. So $P(X) = \mathbb E[V_T \mid X]$ scales by $\lambda$.

*Step 5: investor.* The payoff $q(V_T - P) - k|q|$ becomes $\lambda\,[q(V_T - P) - k|q|]$ when $k \to \lambda k$. The maximizers are the same.

*Step 6: conditions.* (A1) compares $c_L$ with $B$. (A2) compares $c_H$ with two values of $B$. (A3) compares $k$ with $\Delta_T$ times the pure numbers $(1 - 1/b)\rho m$. Each inequality compares degree-one quantities. So it is invariant.

*Degree table.*

| Degree 1 (scales with $\lambda$) | Degree 0 (unchanged) |
|---|---|
| $h, \ell, p, r, c_L, c_H, k$; $t_\cdot, g_\cdot, B_r, \Delta_T$; $P$, $\mathcal R_T$, $\mathcal W$ | $\rho, b, m, M$; $\mu_X$; $\tau, x^*, \alpha_H, \alpha_L$; $\mathsf E, \mathsf O_H$; orders $(q_H, q_L)$ |

Consequence. Every statement of the paper holds in every money unit. This includes the computer-assisted Proposition 3: the certified order magnitudes $v_j$ and entry enclosures $\mathsf E_j$ are unit-free, and the strengths $r_j$ scale. The same holds for general $F$ (Proposition 1), since $F_\lambda(u) = F(u/\lambda)$ and both integrals in eq. (6) are degree one.

*Numerical diagnostic.* With $\lambda \in \{1/7,\ 3.7,\ 100\}$, entry stays 0.522757 and $\mathsf O_H$ stays 0.324192. Also $\mathcal R_T/\lambda = 0.872392$ and $\mathcal W/\lambda = 2.382301$. The investor's marginal profit divided by $\lambda$ stays at 0.106958 (see Section 5).

### 3.2 The flow unit, and the role of $k$ — **analytical**

**Claim 2.** The order bound $|q| \le 1$ fixes a second unit, the unit of shares. If the bound is $\bar u$ and the noise scale is $b' = \bar u\,b$, the economy is equivalent to the paper's economy with scale $b$. Only $b = b'/\bar u$ matters. The cost $k$ is money per share. So $k$ scales with the money unit $\lambda$ only, and a change of flow unit leaves $k$ unchanged.

*Derivation.* Put $q' = \bar u q$, $Z' = \bar u Z$ (Laplace with scale $\bar u b$), $X' = \bar u X$. The log likelihood ratio of two orders is $(|x'-q'_1| - |x'-q'_2|)/b' = (|x-q_1| - |x-q_2|)/b$. So beliefs are unchanged. The investor's payoff is $q'(V_T - P) - k|q'| = \bar u\,[q(V_T - P) - k|q|]$ with the same $k$. A positive factor does not change maximizers. The bounds $m = 1/(1 + e^{2\bar u/b'})$ and (A3) factor $(1 - \bar u/b')$ reduce to the paper's $m$ and $(1 - 1/b)$.

Why $k$ is per share. $V_T$ and $P$ are money per share. $q$ is in shares. The term $k|q|$ must be money. So $k$ has units money per share, the same as a price.

Consequence. The paper's "$b > 1$" is not a normalization. It is the restriction that the noise scale exceeds the largest order. It is used in (A3) through $(1 - 1/b) > 0$.

*Numerical diagnostic.* With $\bar u = 0.37$ and $\bar u = 5$ (and $b' = \bar u\cdot 2$), entry is 0.522757 and $\mathsf O_H$ is 0.324192.

### 3.3 Where $c_L$ enters — **analytical** (by reading; inventory)

The brief's claim is that $c_L$ appears only in (A1) and the weaker floor variants. My search of `main.tex` and `online_appendix.tex` gives a longer list. Every item is a participation-floor inequality, its equality event, or an accounting level. None is a closed form of (4), (9), (11), or (12).

| # | Where | What $c_L$ does |
|---|---|---|
| 1 | L301–302, OA L207–208 | Definition: $0 \le c_L < c_H$ |
| 2 | L508, Prop. A.2 (L1351), OA L298 | Floor $c_L < B_r(m)$: entry $\ge \rho$, price sufficiency (10), residual bound (11) |
| 3 | L584 (A1), proof Step 1 (L1476), OA.1 | Floor at $r_1$; by monotonicity of $B_r$ in $r$ it gives the floor at $r_0$ |
| 4 | L605, proof of part (iii) (L1535) | A **separate, stronger** floor $c_L < B_{r_2}(m)$. Benchmark: $B_{r_2}(m) = 2.272 < B_{r_1}(m) = 2.366$ |
| 5 | L622–635 | Weaker-floor discussion: $B_r(m) < c_L \le B_r(1/2)$ and $c_L > B_r(1/2)$. Verbal; no proposition |
| 6 | L1584, OA L625 | Domain $\mathcal D$ of Prop. A.4 |
| 7 | L1887–1893 (A.24), OA L751–753, L1944 | Atomless costs: $c_L - \varepsilon_C \ge 0$ and $c_L + \varepsilon_C < B_{r_1}(m)$ |
| 8 | L2006, OA.29; Lemma OA.2 | Signal and prior variants: $c_L < B_{r_1}(\phi_-(\mu_-))$ and $c_L < B_{r_1}(\mu_-)$. These floors are stronger |
| 9 | L2339–2448, OA L1457–1474 | Price-pooling example (Prop. A.10): $3\bar\mu_c < 1 = c_L$ |
| 10 | L2475–2487, L2508, OA L2763–2773 | Reserve events: $p_L = h - c_L/m$; $B(M) = Mc_L/m < c_H$; $m g_H = m c_H/M > c_L$ |
| 11 | Table 2 Panel C | The **level** of $\mathcal W$ (cost paid by the low-cost type) |
| 12 | L2591–2614, OA.77, OA.78 | Parameter vectors; margin $\zeta_L$; the choice $c_L = B_{r_1}(m)/2$ |

Verdict.

- **Confirmed** for the closed forms. $c_L$ is absent from (4), (5), (9), (10), (11), (12), from $\mathsf E$, $\mathsf O_H$, $\mathcal R_T$, from Props. 1, A.1, A.3, from (A.6), and from the changes $\Delta\mathcal W$ and $\Delta\mathcal R_T$ in (A.41).
- **Refuted** as "only (A1)". It also appears in items 4, 6–10 and 11. The main extra items are the separate floor at $r_2$, the atomless-cost windows, the pooling example, the reserve events, and the $\mathcal W$ level.

### 3.4 $c_L$ is slack inside its window — **analytical**

**Claim 3.** Fix all primitives except $c_L$. Let $c_L$ and $c_L'$ both lie in $[0, \min\{B_{r_1}(m),\ B_{r_2}(m)\})$. (For parts (i) and (ii) only, the window is $[0, B_{r_1}(m))$.) Then the two economies have the same equilibrium set in orders, prices, beliefs, and entry. Hence they have the same $\mathsf E$, $\mathsf O_H$, and $\mathcal R_T$. The level of $\mathcal W$ differs by exactly $-\rho(c_L' - c_L)$. The difference $\Delta\mathcal W$ in (A.41) is unchanged.

*Derivation.* Every price posterior lies in $[m, M]$ (Prop. A.1). Since $B_r(\mu) \ge B_r(m) > c_L$ at every feasible belief, the low-cost type prepares at every price, for both values of $c_L$. The market maker's pricing rule and the investor's payoff use the challenger's decision only through the entry probability $e$. That function is the same. So the equilibrium conditions are identical. The cost $c_L$ is paid by the low-cost type, which prepares in every case. It enters only the ex post challenger payoff and $\mathcal W$, as the constant $-\rho c_L$. This constant is the same in both economies of any comparison. $\square$

*Numerical diagnostic.* At $r_1$ with $c_L \in \{0,\ 0.125,\ 0.5,\ 1,\ 2,\ 2.2,\ 2.26\}$, entry, ownership, and $\mathcal R_T$ stay at 0.522757, 0.324192, 0.872392. The investor's minimum marginal profit stays at 0.106958. $\mathcal W$ moves from 2.632301 ($c_L = 0$) to 2.382301 ($c_L = 1$): a shift of $-0.25 = -\rho\cdot 1$. On the moderate vector, entry stays 0.526805 for $c_L \in \{0,\ 0.3,\ 0.4469\}$ (window upper bound 0.4965).

**Corollary 3a (a price-free sufficient floor) — analytical.** For $p < \ell$, $g_L(r) = (\ell^2 - p^2)/(2r) > 0$ and $B_r(\mu) > g_L(r)$ for all $\mu > 0$. So $c_L \le g_L(r_*)$ implies $c_L < B_{r_*}(m)$, for any $b$, $\rho$, $h$. At $c_L = 0$ the floor holds at every strength in $(\ell, h)$. The sufficient bound is coarse: $g_L(r_1) = 0.125$ against the exact $B_{r_1}(m) = 2.366$.

### 3.5 Three identities that shorten the algebra — **analytical**

**Claim 4.** (a) $t_\theta + g_\theta = \theta$ for $\theta \in \{\ell, h\}$. (b) $g_H - g_L = (h - \ell) - \Delta_T(r)$. (c) $B_r(\mu) = B^{(0)}_r(\mu) - \dfrac{p^2}{2r}$, where $B^{(0)}$ is the value at $p = 0$. (d) $\Delta_T(r) = \ell\,[\cosh\ln(r/\ell) - 1]$ for the uniform incumbent.

*Derivation.* (a) For a high-value challenger, the target gets $\max\{p, R\}$ and the challenger gets $h - \max\{p, R\}$. The sum is $h$. For a low-value challenger with $R \le \ell$: payment $\max\{p, R\}$ plus rent $\ell - \max\{p, R\}$ gives $\ell$. With $R > \ell$ the incumbent wins and pays $\ell$ (as $p < \ell$), and the challenger earns $0$. The sum is $\ell$. This holds for any incumbent law $F$.
(b) Subtract the two identities in (a): $g_H - g_L = (h - \ell) - (t_H - t_L)$. Check against eq. (4): $g_H - g_L = h - r/2 - \ell^2/(2r)$ and $(h - \ell) - (r - \ell)^2/(2r) = h - r/2 - \ell^2/(2r)$. They match. For general $F$ this is $\int_\ell^h F(u)\,du = (h - \ell) - \int_\ell^{\bar r}[1 - F]\,du$, which agrees with eq. (6).
(c) In eq. (4), $g_H$ and $g_L$ both contain $-p^2/(2r)$ and nothing else with $p$. So $B_r(\mu) = (1-\mu)g_L + \mu g_H$ shifts by $-p^2/(2r)$ for every $\mu$.
(d) $(r-\ell)^2/(2r) = \tfrac12(r/\ell + \ell/r)\,\ell - \ell$. With $r = \ell e^s$, this is $\ell(\cosh s - 1)$. $\square$

Reading of (b). The gap in challenger value, $h - \ell$, is split between the target ($\Delta_T$) and the challenger ($g_H - g_L$, the slope of $B$). Proposition 1 says that a stronger incumbent moves value from the second part to the first. Identity (b) states this as one line: $d\Delta_T = -d(g_H - g_L)$.

Consequence of (d). The thresholds of Proposition A.4 have the form $\mathfrak r(d) = \ell\exp\operatorname{arccosh}(1 + d/\ell)$. This equals $\ell + d + \sqrt{d^2 + 2\ell d}$.

*Numerical diagnostic.* Identities (a)–(c) hold to $10^{-15}$ at three random parameter draws; (d) is checked at a draw with $\ell \ne 1$ (see `output.txt`, Part 4).

### 3.6 What determines the outcome — **analytical**

**Claim 5.** At $r_1$, the outcome $(\mathsf E, \mathsf O_H)$ is a function of $(\rho, b, \tau_1)$ alone, where $\tau_1 = (c_H - g_L(r_1))/(g_H(r_1) - g_L(r_1))$. At $r_0$ and $r_2$ the entry is $\rho$. All other primitives enter only through the inequalities (A1)–(A3) and through $\tau_1$.

*Derivation.* Read eq. (12). It contains $\rho$, $b$, and $\tau$. The price and the preparation rule enter only via $\tau$. Parts (i) and (iii) give $\mathsf E = \rho$.

*Numerical diagnostic.* An economy with $(h, p, r_1, c_H, k) = (7, 0.3, 2.5, 4.09475, 0.01)$ and the same $\tau_1 = 0.705$, $\rho = 0.25$, $b = 2$ gives $\mathsf E = 0.522757$ and $\mathsf O_H = 0.324192$, as in the benchmark.

Window in belief units. (A2) says $\tau_1 \in (\underline\tau, M)$ with $\underline\tau = (B_{r_0}(1/2) - g_L(r_1))/(g_H(r_1) - g_L(r_1))$. At the benchmark, $\underline\tau = 0.5615$ (hand-computed from printed quantities: $(4.804167 - 0.125)/8.333333$), $M = 0.7311$, $\tau_1 = 0.7050$. Condition (A3) reads, in the ratio $\hat k = k/\Delta_T(r_1)$:

$$
\frac{\Delta_T(r_0)}{\Delta_T(r_1)} < \hat k < \Big(1 - \frac1b\Big)\rho\, m .
$$

Benchmark: $0.0250 < 0.0300 < 0.0336$. The window is non-empty if and only if $\Delta_T(r_0)/\Delta_T(r_1) < (1 - 1/b)\rho m$. This is a condition on the two strengths and on $(\rho, b)$ only. It does not involve any money unit.

### 3.7 Comparison of normalizations — **analytical** (verdicts), with the numerical support above

"WLOG" means: every economy in the paper's parameter space is the image of an economy that satisfies the normalization, by Claim 1. "Restriction" means: some economies of the paper are excluded, or an economic channel is removed.

| Normalization | Status | What gets simpler | What it removes or costs |
|---|---|---|---|
| $\ell = 1$ | **WLOG.** $\ell > 0$ by eq. (1). Already used in all three vectors of A.8. | Eq. (4), (5), (A.10), (A.11), (A.13), (A.25): the term $\ell^2$ becomes $1$. $h$ becomes the ratio $h/\ell$ ("gap"). $p \in (0,1)$. | Nothing. |
| $h - \ell = 1$ | **WLOG.** | $g_H - g_L = 1 - \Delta_T$. (A.25) becomes $1$. | $\ell$ stays free. The benchmark has $\ell = 1/9$. Section 5.2 and the A.8 construction use the *ratio* $h/\ell$, so they lose their natural reading. |
| $h = 1$ | **WLOG.** | All values lie in $(0, 1)$: $0 < p < \ell < r < 1$. Useful for grids. | $\ell$ stays free; eq. (4) keeps its $\ell^2$ term. |
| $c_L = 1$ | **WLOG only if $c_L > 0$.** It excludes the boundary $c_L = 0$ that the paper admits ($0 \le c_L$). | Only (A1): it becomes $B_{r_1}(m) > 1$. No formula in (4), (9), (12) contains $c_L$. | The other primitives become awkward. The moderate vector, in $c_L = 1$ units, is $(h, \ell, p, c_H, k, r_1) = (6.667,\ 3.333,\ 1.667,\ 2.967,\ 0.00667,\ 5)$. It gives the same entry 0.526805. The benchmark is unchanged only because $c_L = \ell = 1$ there. |
| $c_L = 0$ | **Restriction** (a corner of the window). **Outcome-equivalent** to every $c_L$ in the window for Prop. 2 (Claim 3). | (A1) is automatic (Cor. 3a). The floor holds at every $r$. Prop. A.2 and the domain $\mathcal D$ lose one condition. The weaker-floor paragraph goes away. | See the list below. |
| $p \to 0$ | **Restriction**, not a unit choice (Section 3.8). | $t_0 = 0$; $p^2$ terms vanish. | The reserve (Section 6.3, A.7). The numbers change. |
| Costs as ratios | **WLOG** if the ratio is a position inside a window (Section 3.9). $c_H/c_L$ is *not* useful. | (A1), (A2) become statements about numbers in $[0,1)$. | $c_H/c_L$ is undefined at $c_L = 0$ and carries no content: it ranges from $2.64$ to $\infty$ with no effect on the outcome. |

What $c_L = 0$ costs, beyond Prop. 2:

1. The weaker-floor paragraph (L622–635) is no longer reachable by varying $c_L$. It stays a statement about an economy with $c_L > B_r(m)$.
2. The atomless-cost result (A.24) needs one-sided or off-centre windows. The condition $c_L - \varepsilon_C \ge 0$ forces $\varepsilon_C = 0$ if the window is centred at $0$.
3. The pooling example of Prop. A.10 has no floor failure to show. At $c_L = 0$, gross profit $3\bar\mu_c > 0 = c_L$, so the low-cost type prepares at the zero price, and the pool disappears. The example needs $c_L > 0$.
4. The reserve event $p_L = h - c_L/m$ moves to $p_L = h$, where there is no rent.
5. The level of $\mathcal W$ rises by $\rho c_L$. In Table 2, Panel C, the level $2.382301$ becomes $2.632301$, and $2.302083$ becomes $2.552083$. The gain $0.080218$ does not change.
6. The story. The text of Section 2.1 says preparation is "cheap for some buyers". At $c_L = 0$ the low-cost type is a buyer that is *ready at no cost*. This reads as exogenous participation: with probability $\rho$ a second bidder is present. It is a clean reading, but it differs from "a small positive cost".

### 3.8 The reserve $p$ and the level $t_0$ — **analytical**

**Claim 6.** (a) Removing $t_0$ is free: it needs no condition on $p$. (b) Setting $p \to 0$ is not WLOG for the numbers. (c) The effect of $p$ on entry is a shift of the cost: $p$ acts like an extra preparation cost $p^2/(2r)$.

*Derivation.* (a) In eq. (10)–(11), $t_0$ enters the price only as a level. It cancels in $A_H$ and $A_L$, and it is not in $B_r$ or $e_r$. The deterministic shift $\tilde V_T = V_T - t_0$ is the dividend-invariance of Section 6.1. It changes $P$ and $\mathcal R_T$ by the constant $t_0$ and nothing else. Within each economy $t_0$ is a known constant. (If Q3 adds an initial stake $\omega$, the term $\omega t_0$ is still a constant in the investor's payoff, so it still drops out of the order decision.)
(b) and (c). By Claim 4(c), $B_r(\mu) \ge c$ if and only if $B_r^{(0)}(\mu) \ge c + p^2/(2r)$. The shift depends on $r$: $0.1042$ at $r_0$, $0.0417$ at $r_1$, $0.0347$ at $r_2$. So no single change of $c_H$ removes $p$ from all three economies.

*Numerical diagnostic.* At $p = 0$ and the other benchmark values: $\tau = 0.7000$ and $\mathsf E = 0.525733$. At $p = 0.5$: $\tau = 0.7050$ and $\mathsf E = 0.522757$. With $p = 0$ and $c_H$ raised by $p^2/(2r_1) = 0.041667$, entry is 0.522757 again.

Consequence. At $p = 0$ every proof step of Prop. 2 goes through, although eq. (1) of the paper requires $p > 0$. All inequalities stay strict. By their openness, the claim then holds for small $p > 0$. But $p$ is the seller's instrument in Section 6.3 and A.7. Setting it to $0$ removes that part of the paper. It also does not answer Q3 (who holds the shares): the netting of $t_0$ is available without it.

### 3.9 Costs as positions in their windows — **analytical** (definition) and a **numerical diagnostic**

Define

$$
v = \frac{c_L}{B_{r_1}(m)} \in [0,1), \qquad
u = \frac{c_H - B_{r_0}(1/2)}{B_{r_1}(M) - B_{r_0}(1/2)} \in (0,1).
$$

(A1) is $v < 1$. (A2) is $u \in (0,1)$. The two windows are separate intervals, and they cannot overlap: $c_L < B_{r_1}(m) \le B_{r_0}(m) < B_{r_0}(1/2) < c_H$. So $c_L < c_H$ follows from (A1) and (A2); it need not be assumed. The OA.78 construction chooses $v = 1/2$, $u = 1/2$. At the benchmark, $v = 0.4226$ and $u = 0.8463$.

## 4. What changes relative to the current paper

**Survive unchanged.** Props. 1, 2, 3, A.1–A.9 and all closed forms. Claim 1 and Claim 2 show that they hold in every unit. Nothing is lost by $\ell = 1$.

**Change under the recommended choice** (Section 7):

| Item | Change |
|---|---|
| Section 2.2 | One sentence: money is measured in units of the low acquisition value, $\ell = 1$. |
| Eq. (4), (5) | Shorter, as in Section 7 below. |
| Eq. (12) | Same form. Only $\tau$'s denominator can be written $h - 1 - \Delta_T(r_1)$. |
| (A1) | Becomes automatic at $c_L = 0$; or stays, with a remark. |
| Prop. A.2, A.4 hypotheses | The condition $c_L < B_r(m)$ disappears at $c_L = 0$. |
| Section 4.1, L612–635 | The weaker-floor paragraph moves to a remark or an appendix note. |
| (A.24), A.6 | Low-cost window needs to be one-sided if $c_L = 0$. |
| Prop. A.10, (A.50) | Keep $c_L > 0$ in the reserve appendix, or state that they need it. |
| Table 2, Panel C | If the benchmark uses $c_L = 0$: $\mathcal W$ levels shift by $+0.25$. Nothing else changes. |
| A.8 vectors | $\ell = 1$ already. Set $c_L = 0$ only if the author chooses that path. |

**Fail.** Nothing fails. Two things do not carry over to $c_L = 0$: Prop. A.10's example and the reserve event $p_L$.

## 5. Numerical example

Script: `scripts/Q4_normalization/normalization_check.py`, output in `output.txt`. Benchmark vector $(h, \ell, p, \rho, c_L, c_H, b, k) = (10, 1, 0.5, 0.25, 1, 6, 2, 0.02)$ and $(r_0, r_1, r_2) = (1.2, 3, 3.6)$.

*Reproduction (numerical diagnostic).* The auction objects, computed by integrating the payment rule over $R$, match eq. (4). Eq. (12) gives $\tau = 0.705000$, $x^* = 0.871222$, $\mathsf E = 0.522757$, $\mathsf O_H = 0.324192$, $\mathcal R_T = 0.872392$. A direct calculation (entry rule applied to the flow density, with $c_L$ in the rule) gives the same, plus $\mathcal W = 2.382301$. These agree with Table 2. Windows: $B_{r_1}(m) = 2.366179$, $B_{r_2}(m) = 2.272133$, $B_{r_0}(1/2) = 4.804167$, $B_{r_1}(M) = 6.217155$.

*Full orders are optimal (numerical diagnostic).* The marginal profit of a correctly signed order, computed against the candidate price and entry schedule on a grid of $s \in [0,1]$, is between 0.106958 and 0.140009. It is positive.

*Rescaling.* See Section 3.1 and 3.2. Entry and ownership do not change under $\lambda \in \{1/7, 3.7, 100\}$ or under a change of flow unit $\bar u \in \{0.37, 5\}$.

*Moving $c_L$.* See Section 3.4. Entry, ownership, and revenue do not change for $c_L \in [0, 2.26]$.

*Outside the window (diagnostic only).* If the orders are frozen at $(1, -1)$ and $c_L$ is raised to 2.4162, just above $B_{r_1}(m)$, entry from the direct calculation is 0.435974. This is not an equilibrium statement. It shows only that the window edge matters.

## 6. Open issues and risks

1. **The weaker-floor claims (L622–635) are open.** The text says total entry exceeds $\rho$ only if high-cost recruitment outweighs low-cost deterrence. I did not prove or test this. Only Claim 3 is established, and it concerns $c_L$ inside the window.
2. **Equilibria for $c_L$ outside the window are open.** The frozen-profile number above is not an equilibrium result.
3. **Atomless costs.** At $c_L = 0$ the window must be changed (for example $[0, 2\varepsilon_C]$). This needs a short rewrite of (A.24) and Prop. A.6. I did not rewrite the proof.
4. **Interaction with Q1.** If the challenger's value law changes, $\ell$ is no longer a primitive. The unit then has to come from another quantity (for instance $\mathbb E[\theta \mid L]$ or the scale of $G_L$). The advice "$\ell = 1$" belongs to the binary-value model.
5. **Interaction with Q3.** Claim 6(a) says $t_0$ can be netted out. Whether an investor stake changes the *story* is a Q3 question. I only checked that $t_0$ stays a constant in the payoff.
6. **Numerical layer.** Absolute tolerances in the numerical controls are in money units. A unit change moves their meaning. The repository already works at $\ell = 1$.
7. **Interpretation risk.** At $c_L = 0$ the low-cost type no longer "prepares" in a costly sense. A reader may ask whether "entry" is then a choice. The honest reading is exogenous participation with probability $\rho$.

## 7. Recommendation

In priority order.

1. **Do not normalize $c_L$ to 1.** It is legal for $c_L > 0$ but it shortens no formula. It makes the moderate vector awkward. It adds a case ($c_L = 0$) that the paper admits.
2. **Adopt $\ell = 1$ as the unit of money.** It is WLOG, it matches every parameter vector, and it shortens the auction layer. Say in Section 2.2: "Money is measured in units of the low acquisition value, $\ell = 1$. By Claim 1, no result depends on this choice."
3. **Treat $c_L$ as a slack parameter.** Add a remark under Proposition 2: "The outcome does not depend on $c_L$ in $[0, B_{r_1}(m))$; take $c_L = 0$ in all calculations." This half is free: it loses no content. The second half trades content. Setting $c_L = 0$ in the baseline, and keeping $c_L > 0$ only in the reserve appendix, removes the floor condition from the main text and the weaker-floor detour. It also removes the Prop. A.10 example, the event $p_L$, the centred atomless window, and the $\mathcal W$ level (Section 3.7). The author must decide whether that trade is worth it, and which reading of the low-cost type to present (a small cost or a ready buyer). I do not make that content choice.
4. **Leave $p$ alone.** Net out $t_0$ by the dividend argument if a simpler price formula is wanted. Do not take $p \to 0$.
5. **Add the identities of Claim 4** to Section 3.1. They shorten Proposition 1 and (5) to one line each.
6. **State the ratio form of (A3)** and the belief form of (A2). They make the nonemptiness proof unit-free.

### Rewrite under $\ell = 1$ (and $c_L$ free in its window; write $c \equiv c_H$)

Support: $0 < p < 1 < r < h$.

Eq. (4):

$$
\begin{aligned}
t_0 &= p\Big(1 - \frac pr\Big), & t_H &= \frac r2 + \frac{p^2}{2r}, & t_L &= 1 - \frac{1 - p^2}{2r},\\
g_H &= h - \frac r2 - \frac{p^2}{2r}, & g_L &= \frac{1 - p^2}{2r}, & \Delta_T(r) &= \frac{(r-1)^2}{2r}.
\end{aligned}
$$

Added identities: $t_\theta + g_\theta = \theta$, and

$$
B_r(\mu) = \frac{1 - p^2}{2r} + \mu\,\big[h - 1 - \Delta_T(r)\big].
$$

Eq. (12): the same expressions, with

$$
\tau = \frac{c - g_L}{h - 1 - \Delta_T(r_1)}, \quad x^* = \frac b2\log\frac{\tau}{1 - \tau}, \quad \alpha_H = 1 - \tfrac12 e^{(x^*-1)/b},\ \ \alpha_L = \tfrac12 e^{-(x^*+1)/b},
$$

$$
\mathsf E = \rho + \frac{1-\rho}{2}(\alpha_H + \alpha_L), \qquad \mathsf O_H = \tfrac12[\rho + (1-\rho)\alpha_H].
$$

Eq. (12) contains no money level and no $c_L$. No money normalization can shorten it. Only $\tau$'s denominator changes.

Conditions:

- (A1): $0 \le c_L < B_{r_1}(m)$. It holds for every $c_L \le (1 - p^2)/(2r_1)$, and in particular for $c_L = 0$.
- (A2): $B_{r_0}(\tfrac12) < c < B_{r_1}(M)$, with $B_r(\mu)$ as above. Equivalent form: $\tau_1 \in (\underline\tau, M)$.
- (A3): $\dfrac{(r_0 - 1)^2}{2r_0} < k < \Big(1 - \dfrac1b\Big)\rho\, m\,\dfrac{(r_1 - 1)^2}{2r_1}$. Equivalent form: $\hat k = k/\Delta_T(r_1) \in \big(\Delta_T(r_0)/\Delta_T(r_1),\ (1 - 1/b)\rho m\big)$.

Thresholds: $\mathfrak r(d) = 1 + d + \sqrt{d^2 + 2d}$ and $r_N = \mathfrak r(2k/\rho)$, $r_U = \mathfrak r\big(k/((1 - 1/b)\rho m)\big)$.

## 8. Plain summary

The supervisor asked whether we can set the low preparation cost to 1. We can, as a choice of unit, if the cost is above zero. But it does not make anything simpler. The low cost does not appear in any formula that gives the result. It appears only in a condition saying that the cheap buyer always prepares.

Two facts explain this. First, changing the money unit changes nothing real. If we multiply every value, cost, and price by the same number, then orders, beliefs, entry, and who owns the target stay the same. Second, anywhere inside the allowed range, the low cost has no effect. We checked this on the benchmark: entry stays at 0.522757 for any low cost from 0 to 2.26. Only a surplus total that nets out costs shifts, by a constant.

What does help is a different unit. Measure money in units of the low acquisition value, so $\ell = 1$. The paper's vectors already do this. It shortens the auction formulas. The entry formula (12) cannot be shortened, because it has no money in it.

We also found two short identities. The value gap between a high and a low challenger splits into the target's share and the challenger's share. And the reserve acts like an extra cost that shrinks as the incumbent grows. So we should not set the reserve to zero.

Our advice: use $\ell = 1$. Say that the low cost is slack, and compute with a low cost of zero. Keep a positive low cost only where the reserve appendix needs it.
