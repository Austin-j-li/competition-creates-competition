/* The talk follows paper/main.md. Quantities come only from the bound registry.
   Symbols are introduced progressively: every entry below is defined on the slide
   named in `defines`, and the definition strip renders it beside the mathematics. */

window.createGlossary = function (H) {
  const g = (key, latex, meaning, group, pattern) => ({key, latex, meaning, group, pattern});
  return [

    g('R', String.raw`R`,
      'the prepared incumbent’s own acquisition value, drawn from its public range and private until it bids',
      'values', String.raw`(?<![A-Za-z\\])R(?![A-Za-z_])`),

    g('r', String.raw`r`,
      'incumbent strength: the upper end of the incumbent’s value range; a larger r is a first-order stochastic strengthening',
      'values', String.raw`(?<![A-Za-z\\])r(?![A-Za-z_0-9])`),

    g('theta', String.raw`\theta`,
      'the challenger’s acquisition value, high or low with equal prior odds, which it learns only by preparing',
      'values', String.raw`\\theta`),

    g('ell', String.raw`\ell`,
      'the low acquisition value a challenger can turn out to have',
      'values', String.raw`\\ell`),

    g('h', String.raw`h`,
      'the high acquisition value a challenger can turn out to have',
      'values', String.raw`(?<![A-Za-z\\])h(?![A-Za-z_])`),

    g('p', String.raw`p`,
      'the reserve in the cash second-price auction the seller commits to before trading',
      'institutions', String.raw`(?<![A-Za-z\\])p(?![A-Za-z_])`),

    g('C', String.raw`C`,
      'the preparation cost the challenger draws privately after it has seen the price',
      'preparation', String.raw`(?<![A-Za-z\\])C(?![A-Za-z_])`),

    g('c_L', String.raw`c_L`,
      'the low preparation cost; under A1 it is worthwhile at every feasible belief',
      'preparation', String.raw`c_L`),

    g('c_H', String.raw`c_H`,
      'the high preparation cost; A2 makes preparation responsive to favourable information',
      'preparation', String.raw`c_H`),

    g('rho', String.raw`\rho`,
      'the probability that the realised preparation cost is the cheap one',
      'preparation', String.raw`\\rho`),

    g('e', String.raw`e`,
      'whether the challenger prepares; averaged over cost realisations it is the preparation probability at a price',
      'preparation', String.raw`(?<![A-Za-z\\])e(?=\(|_|\s|$|\\)`),

    g('q', String.raw`q`,
      'the informed investor’s order, bounded by one normalised unit in each direction',
      'trading', String.raw`(?<![A-Za-z\\])q(?![A-Za-z])`),

    g('Z', String.raw`Z`,
      'noise demand, independent of values and costs, with a Laplace density',
      'trading', String.raw`(?<![A-Za-z\\])Z(?![A-Za-z_])`),

    g('b', String.raw`b`,
      'the scale of noise demand; it sets how much any single order can reveal',
      'trading', String.raw`(?<![A-Za-z\\])b(?![A-Za-z_])`),

    g('X', String.raw`X`,
      'aggregate order flow, the investor’s order plus noise, and all the market makers see',
      'trading', String.raw`(?<![A-Za-z\\])X(?![A-Za-z_])`),

    g('k', String.raw`k`,
      'the investor’s linear trading cost per unit, a friction distinct from price impact',
      'trading', String.raw`(?<![A-Za-z\\])k(?![A-Za-z_])`),

    g('P', String.raw`P`,
      'the price competitive market makers set from order flow, and the only market signal the challenger sees',
      'prices', String.raw`(?<![A-Za-z\\])P(?![A-Za-z])`),

    g('mu', String.raw`\mu`,
      'a posterior probability that the challenger is the high-value one',
      'prices', String.raw`\\mu(?!_P)`),

    g('g_H', String.raw`g_H`,
      'gross acquisition profit for a high-value challenger, before its preparation cost',
      'derived', String.raw`g_H`),

    g('g_L', String.raw`g_L`,
      'gross acquisition profit for a low-value challenger, before its preparation cost',
      'derived', String.raw`g_L`),

    g('t', String.raw`t_0,\;t_L,\;t_H`,
      'expected target proceeds with no prepared challenger, with a low-value one, and with a high-value one',
      'derived', String.raw`(?<![A-Za-z\\])t_(0|L|H)`),

    g('Delta_T', String.raw`\Delta_T`,
      'target-payoff spread: the gap in target proceeds between a high- and a low-value challenger, per share',
      'derived', String.raw`\\Delta_T`),

    g('B', String.raw`B_r(\mu)`,
      'the challenger’s expected gross acquisition profit at a belief, before the preparation cost',
      'derived', String.raw`(?<![A-Za-z\\])B(?=_|\()`),

    g('sigma', String.raw`\sigma_H,\;\sigma_L`,
      'the investor’s order distributions, one for each challenger value, which may be arbitrary mixtures',
      'trading', String.raw`\\sigma`),

    g('mu_P', String.raw`\mu_P`,
      'the posterior the challenger recovers from the observed price alone',
      'prices', String.raw`\\mu_P`),

    g('e_schedule', String.raw`e(\cdot)`,
      'the preparation schedule: what the challenger does at each price, held fixed while a deviation is evaluated',
      'preparation', String.raw`(?!)`),

    g('m', String.raw`m`,
      'the lowest posterior any order flow can produce under the noise law',
      'prices', String.raw`(?<![A-Za-z\\])m(?![A-Za-z_])`),

    g('M', String.raw`M`,
      'the highest posterior any order flow can produce, the mirror image of the lowest',
      'prices', String.raw`(?<![A-Za-z\\])M(?![A-Za-z_])`),

    g('tau', String.raw`\tau`,
      'the belief at which expensive preparation exactly breaks even',
      'derived', String.raw`\\tau`),

    g('x_star', String.raw`x^*`,
      'the order flow at which the posterior first reaches that break-even belief',
      'derived', String.raw`x\^\*|x^\*|x_\*`),

    g('A_H', String.raw`A_H`,
      'what buying on good news still earns the investor after competitive pricing takes the anticipated part away',
      'derived', String.raw`A_H`),

    g('A_L', String.raw`A_L`,
      'what selling on bad news still earns the investor after competitive pricing',
      'derived', String.raw`A_L`),

    g('r_0', String.raw`r_0`,
      'the weak incumbent in the main comparison',
      'values', String.raw`r_0`),

    g('r_1', String.raw`r_1`,
      'the strong incumbent in the main comparison',
      'values', String.raw`r_1`),

    g('r_2', String.raw`r_2`,
      'a still stronger incumbent, at which even the best feasible news cannot justify expensive preparation',
      'values', String.raw`r_2`),

    g('E', String.raw`\mathsf E`,
      'the preparation probability in an economy, the chance the challenger pays its cost',
      'outcomes', String.raw`\\mathsf E`),

    g('O_H', String.raw`\mathsf O_H`,
      'the probability that a high-value challenger ends up owning the target',
      'outcomes', String.raw`\\mathsf O_H`),

    g('eta', String.raw`\eta`,
      'the seller’s bargaining weight in the alternative payment rule',
      'institutions', String.raw`\\eta`),

    g('Delta_eta', String.raw`\Delta_\eta`,
      'the target-payoff spread under that bargaining rule, at a given weight',
      'derived', String.raw`\\Delta_\\eta`),

    g('V_T', String.raw`V_T`,
      'the terminal payoff of one target share, what the traded claim finally delivers',
      'prices', String.raw`V_T`),

    g('d', String.raw`d`,
      'a deterministic external dividend added to the traded claim in the matched-price diagnostic',
      'prices', String.raw`(?<![A-Za-z\\])d(?![A-Za-z_])`)

  ];
};

window.createSlides = function (H) {
  const {m, mi, v, pct, fmt} = H;
  const S = (id, o) => ({id, act:'', kicker:'', title:'', subtitle:'', body:'', notes:'', source:'', minutes:0, widget:'', backup:false, status:'', defines:[], theme:'light', speakingMinutes:o.minutes||0, ...o});
  const rev = (n, html) => `<div class="reveal" data-step="${n}">${html}</div>`;
  const controls = (name, options) => `<div class="segmented" role="group" aria-label="${name}">${options.map(([value,label])=>`<button data-choice="${name}" data-value="${value}" aria-pressed="false">${label}</button>`).join('')}</div>`;
  const defs = keys => `<div class="defs" data-defs="${keys}"></div>`;
  const declaration = `h = ${v('base_h')}, ℓ = ${v('base_ell')}, p = ${v('base_p')}, ρ = ${v('base_rho')}, c<sub>L</sub> = ${v('base_c_low')}, c<sub>H</sub> = ${v('base_c_high')}, b = ${v('base_b')}, k = ${v('base_k')}`;
  const arrow = '<span class="connector" aria-hidden="true">→</span>';
  const flow = (items, cls='') => `<div class="flow ${cls}">${items.map((x,i)=>`${i?arrow:''}<div class="flow-node">${x}</div>`).join('')}</div>`;
  const notes = (text, answer) => `${text} If asked: ${answer}`;
  return [
    S('s01', {act:'puzzle', theme:'dark', minutes:0.5,
      body:`<div class="hero"><p class="author">Austin Li <span>UCL School of Management</span></p><h1>Competition<br><span>creates competition.</span></h1><div class="hero-bottom"><p class="hero-subtitle">Stock prices and the discovery<br>of takeover bidders</p><div class="hero-signal" aria-hidden="true"><span></span><span></span><span></span><span></span><span></span><span></span><span></span></div></div></div>`,
      notes:notes('A stronger incumbent can make a second buyer more willing to incur preparation costs. The claim concerns an equilibrium information channel. Introduce the question verbally and move promptly to the decision facing the buyer.','The talk develops sufficient conditions in a theoretical model. The benchmark numbers are model illustrations.'),source:'Competition Creates Competition: Stock Prices and the Discovery of Takeover Bidders.'}),
    S('s02', {act:'puzzle',minutes:1.5,title:'A buyer must decide<br>before it knows enough.',
      subtitle:'Preparing an executable bid requires a costly commitment.',
      body:`<div class="decision-window"><div class="window-edge"><span>Public sale opportunity</span><p>The target can be acquired.</p></div><div class="window-middle"><div class="market-line"><span></span></div><strong>The stock keeps trading</strong><p>The potential buyer can observe the market while deciding.</p></div><div class="window-edge"><span>Executable proposal</span><p>Preparation costs have been incurred.</p></div></div>${rev(1,'<div class="takeaway">The relevant interval is public and still open to another buyer.</div>')}<p class="small">Imprivata’s 2016 proxy distinguishes approaches, outreach, and indications conditional on diligence. This motivates the stage structure, not the price-learning mechanism.</p>`,
      notes:notes('Explain preparation as diligence, verification, financing and the capacity needed to submit an executable proposal. One buyer is already prepared. The challenger can watch prices before committing. A confidential sale revealed only after participation is settled does not fit. The institutional example documents stages, not a causal effect of prices.','An empirical application must establish the public decision window transaction by transaction. See Section 1.1 and Online Appendix D.'),source:'Section 1.1; Imprivata (2016); Boone and Mulherin (2007).'}),
    S('s03', {act:'puzzle',minutes:1,title:'A stronger rival leaves<br>less to win.',
      subtitle:'The conventional deterrence force, holding information fixed.',
      body:`${flow(['<span>Stronger incumbent</span><strong>A tougher auction</strong>','<span>Challenger</span><strong>Lower acquisition profit</strong>','<span>Preparation</span><strong>Less reason to pay</strong>'])}${rev(1,'<p class="large-note">That logic remains intact in this paper.</p>')}`,
      notes:notes('Start from acquisition-stage economics. At every fixed posterior a first-order strengthening of the incumbent reduces the challenger’s expected gross acquisition profit. For a fixed cost draw this can only remove an incentive to prepare. Do not describe this as a false claim or claim that all previous papers assume away learning.','Proposition 1 establishes the payoff comparison. Proposition A.3 gives the fixed-experiment preparation comparison.'),source:'Proposition 1; Proposition A.3. Entry literature: Levin and Smith (1994); Gentry and Stroup (2019).'}),
    S('s04', {act:'puzzle',minutes:1.25,title:'The buyer’s information<br>need not stay fixed.',
      body:`<div class="channel-diagram">${flow(['<span>Competition</span><strong>Target payments change</strong>','<span>Investor</span><strong>Trading incentives change</strong>'])}${rev(1,flow(['<span>Stock market</span><strong>The price reveals information</strong>','<span>Challenger</span><strong>The preparation decision changes</strong>'],'return-flow'))}</div>${rev(2,'<p class="takeaway">Competition changes the information available before commitment.</p>')}`,
      notes:notes('Introduce the possible feedback in words. A traded target share is a claim on acquisition payments. A change in the payment sensitivity to challenger quality affects informed trading. The resulting price may help the buyer learn before paying to prepare. This is a candidate mechanism whose equilibrium validity is established later.','The price is competitively set and already anticipates preparation. The mechanism does not rely on market makers ignoring the real response.'),source:'Sections 1 and 3.'}),
    S('s05', {act:'puzzle',theme:'dark',minutes:1,title:'When does competition<br>recruit another bidder?',
      body:`<div class="question-frame"><p class="display">Can the information effect<br>outweigh direct deterrence?</p><div class="question-balance"><div><span>At a fixed belief</span><strong>Less profit</strong></div><span class="balance-mark">/</span><div><span>In equilibrium</span><strong>More useful information</strong></div></div></div>`,
      notes:notes('State the exact research question. Compare economies that differ only in incumbent strength and solve the trading, pricing and preparation schedules again in each. The object is costly preparation, not a count of expressions of interest or public bids.','The theorem identifies a nonempty open set of primitives. It is not a general monotonicity result across all strengths.'),source:'Section 4.1; Proposition 2.'}),
    S('s06', {act:'puzzle',minutes:1.25,title:'Bidder participation meets<br>learning from prices.',
      body:`<div class="literature-map"><article><h3>Endogenous participation</h3><p>Preparation costs shape who enters the auction.</p><p class="citation">Levin &amp; Smith (1994)<br>Gentry &amp; Stroup (2019)<br>Persico (2000): information acquisition</p></article><article><h3>Prices and real decisions</h3><p>Real decisions and incentives to produce information interact.</p><p class="citation">Dow, Goldstein &amp; Guembel (2017)<br>Edmans, Goldstein &amp; Jiang (2015)<br>Luo (2005): completion decisions</p></article></div><div class="literature-bridge"><strong>This paper</strong><p>The sale rule links the entrant’s profit to the information sensitivity of a different claim: target shares.</p></div>`,
      notes:notes('Spend just over one minute locating the paper. The closest antecedent is Dow, Goldstein and Guembel, where a real investment decision feeds back into information production. Here acquisition surplus is split into two claims, and competition moves the returns to information in opposite directions. Persico studies information acquisition by bidders; here the informed investor is outside the auction. Luo studies learning at completion, after the preparation margin here.','The fuller related-work discussion is Section 1, including negotiations with market feedback, toeholds and tendering. Avoid a blanket priority claim.'),source:'Section 1, related research.'}),
    S('s07', {act:'puzzle',minutes:1.5,title:'The payment rule links<br>competition to information.',
      body:`<div class="contribution-list"><article><span>Mechanism</span><p>A stronger incumbent lowers buyer profits but increases the sensitivity of target proceeds to challenger value.</p></article>${rev(1,'<article><span>Result</span><p>Under sufficient conditions, informative trading recruits additional preparation against the stronger incumbent.</p></article>')}${rev(2,'<article><span>Comparison</span><p>Holding the information experiment fixed restores the deterrence prediction.</p></article>')}</div>`,
      notes:notes('Preview the answer before the formal setup. The contribution is the opposition between returns to information, plus a sufficient-condition theorem that resolves trading and preparation jointly. Uniqueness concerns trading and on-path preparation in the compared economies. The fixed-information control establishes what explains the reversal.','Off-path pricing rules need not be unique. Intermediate strengths may admit multiple equilibria.'),source:'Propositions 1 and 2; Proposition A.3.'}),
    S('s08', {act:'model',minutes:1.5,status:'input',title:'Who knows what?',defines:['R','r','theta','ell','h','p'],
      body:`<div class="cast-new"><article><span class="role-symbol">${mi('R')}</span><h3>Incumbent</h3><p>Already prepared. Knows its own acquisition value.</p>${m(String.raw`R\sim U[0,r]`,'eq-small')}</article><article><span class="role-symbol">${mi(String.raw`\theta`)}</span><h3>Challenger</h3><p>Learns its value by preparing. Equal prior probabilities.</p>${m(String.raw`\theta\in\{\ell,h\}`,'eq-small')}</article><article><span class="role-symbol">${mi(String.raw`\theta`)}</span><h3>Investor</h3><p>Knows challenger value. Trades target shares and cannot acquire the target.</p></article></div><div class="model-line">${m(String.raw`0<p<\ell<r<h`,'eq-small')}<p>The seller commits to a cash second-price auction with reserve ${mi('p')}. A larger ${mi('r')} strengthens the incumbent’s value distribution.</p></div>`,
      notes:notes('Define the three economic roles and the seller. Incumbent strength is the public distribution of acquisition value, not an announced bid. The challenger has equal prior odds of high and low value. All agents are risk neutral. Values, cost and noise demand are mutually independent. Standalone value is zero and all quantities are per target share.','Neither bidder trades. There are no toeholds, tendering or shareholder holdout. The uniform distribution gives closed forms; Proposition 1 allows general continuous incumbent distributions.'),source:'Sections 2.1–2.2; equation (1).'}),
    S('s09', {act:'model',minutes:1.5,status:'input',title:'Preparation makes<br>an executable bid possible.',defines:['C','c_L','c_H','rho','e'],
      body:`<div class="split"><div class="stack"><p class="large-note">One challenger.<br>One privately realised cost.</p>${m(String.raw`C=\begin{cases}c_L&\text{with probability }\rho\\c_H&\text{with probability }1-\rho\end{cases}`,'eq-small')}${m(String.raw`0\le c_L<c_H,\qquad 0<\rho<1`,'eq-small')}</div><div class="choice-tree"><article><span>Prepare: ${mi('e=1')}</span><h3>Pay ${mi('C')}</h3><p>Learn acquisition value and become eligible to bid.</p></article><article><span>Stay out: ${mi('e=0')}</span><h3>No executable offer</h3><p>The buyer cannot submit a bid at its prior expected value.</p></article></div></div>`,
      notes:notes('The cost is required for an executable proposal, rather than an optional research report. The draw occurs privately after the price is seen and is independent of values. There is one challenger, not simultaneous low-cost and high-cost buyers. Under the theorem, low-cost draws create a preparation floor, while high-cost draws respond to favourable information.','The extension with narrow atomless cost supports shows the reversal need not depend on cost atoms.'),source:'Section 2.1; Proposition A.6.'}),
    S('s10', {act:'model',minutes:2,status:'input',title:'Trading precedes<br>the preparation decision.',defines:['q','Z','b','X','k','P','mu','V_T'],
      body:`<div class="market-model"><div class="stack">${m(String.raw`q\in[-1,1],\quad X=q+Z`)}${m(String.raw`Z\sim\mathrm{Laplace}(0,b),\quad b>1`,'eq-small')}${m(String.raw`\text{Investor profit: }q[V_T-P(X)]-k|q|`,'eq-small')}<p>The investor sees ${mi(String.raw`\theta`)} and pays ${mi('k|q|')}, with ${mi('k>0')}. Market makers observe only aggregate flow ${mi('X')}.</p></div><div class="equation-feature">${m(String.raw`P(X)=\mathbb E[V_T\mid X]`)}<p>${mi('V_T')} is the terminal payoff of a target share. The challenger observes the price and its cost.</p></div></div><div class="timeline compact"><article><strong>Sale rule</strong></article><article><strong>Trade</strong></article><article><strong>Price</strong></article><article><strong>Cost draw</strong></article><article><strong>Prepare</strong></article><article><strong>Bid</strong></article></div><p class="small">Write ${mi(String.raw`\mu`)} for the posterior probability of high challenger value. The challenger does not observe order flow.</p>`,
      notes:notes('Read the timing once. The seller commits before trading; the investor observes quality and trades; market makers set the price from flow; the challenger observes price, draws cost and decides; prepared bidders bid truthfully. The market price incorporates expected participation. The linear trading cost is a separate friction from price impact.','Bounded orders are small normalised trading units, not ownership. The investor has no initial position. The investor payoff is q times the difference between terminal proceeds and price, less the trading cost.'),source:'Section 2.2; equations (2)–(3).'}),
    S('s11', {act:'model',minutes:1.5,status:'analytical',title:'Who wins, and who pays?',widget:'auction',defines:['t'],
      body:`<div class="split wide"><div class="stack"><div id="auction-vline" class="plot-shell"></div><div class="controls">${controls('quality',[['H','High value'],['L','Low value']])}<label for="auction-r">Incumbent value</label><input id="auction-r" type="range" min="0" max="3" step="0.05" value="0.8"><output id="auction-r-value"></output><button data-reset="auction">Reset</button></div><p class="large-note">A high-value challenger wins.<br>A low-value challenger can lose.</p><p class="small">Conditional on preparation, ${mi('t_H')} and ${mi('t_L')} denote expected target proceeds by challenger type. Without preparation, proceeds are ${mi('t_0')}.</p></div><div id="auction-readout" class="stack"></div></div>`,
      notes:notes('Move the realised incumbent value. A high-value challenger wins and pays the larger of the reserve and incumbent value. A low-value challenger wins below its own value and loses above it. When it loses, its bid sets the incumbent’s payment. All expected payoffs integrate over the incumbent distribution. The display is auction arithmetic conditional on preparation.','A bid at the reserve is admissible. With continuous incumbent value, acquisition-value ties have probability zero. Do not confuse changing a realised draw here with shifting the distribution later.'),source:'Section 3.1; equation (4).'}),
    S('s12', {act:'model',minutes:1.5,status:'input',title:'Prices and preparation<br>must be jointly consistent.',defines:['sigma','mu_P','e_schedule'],
      body:`<div class="equilibrium-chain">${flow(['<span>Investor</span><strong>Optimal orders</strong>','<span>Market makers</span><strong>Competitive price</strong>','<span>Challenger</span><strong>Optimal preparation</strong>'])}<p class="loop-caption">Anticipated preparation determines the payoff that investors trade.</p></div><div class="split"><div class="rule-block"><h3>Test a deviation</h3><p>Hold the candidate price and preparation schedules fixed. Allow every order and arbitrary mixtures.</p></div><div class="rule-block"><h3>Compare economies</h3><p>Change incumbent strength and solve those schedules again.</p></div></div><p class="small">${mi(String.raw`\sigma_H,\sigma_L`)} are conditional order distributions. ${mi(String.raw`\mu_P`)} is the belief given price. ${mi(String.raw`e(\cdot)`)} is the preparation schedule.</p>`,
      notes:notes('Define equilibrium as conditional investor order distributions, a measurable competitive price, Bayesian beliefs from price, optimal preparation and truthful bidding. The distinction between deviations and comparative statics is essential. Changing an order does not cause market makers to re-solve their strategy. Comparing strengths does.','All continuous deviations and arbitrary mixed orders are allowed. The appendix gives the measure-theoretic treatment and null-set invariance.'),source:'Section 2.3; Online Appendix A.'}),
    S('s13', {act:'mechanism',minutes:2,status:'analytical',title:'A stronger incumbent<br>reduces acquisition profit.',defines:['g_H','g_L','B'],
      body:`<div class="split wide"><div class="stack"><p class="small">Expected acquisition profit before preparation costs</p>${m(String.raw`B_r(\mu)=\mu g_H(r)+(1-\mu)g_L(r)`)}<div class="equation-feature">${m(String.raw`\text{Prepare iff }B_r(\mu_P)\ge C`)}</div><p>${mi('g_H')} and ${mi('g_L')} are profits conditional on high and low value.</p></div><div class="derivative-statement">${m(String.raw`\left.\frac{\partial B_r(\mu)}{\partial r}\right|_\mu<0`,'eq-big')}<p>At every fixed belief,<br>the preparation incentive falls.</p></div></div>`,
      notes:notes('Tie the formal preparation rule to the institutional decision. Conditional profits fall because a stronger incumbent raises the price the challenger must beat. A posterior is the probability weight on high quality. Holding it fixed, the weighted profit falls. Equality leads to preparation under the declared convention.','The comparative static extends to first-order stochastic strengthening of a continuous incumbent distribution. The closed forms are in the payoff appendix slide.'),source:'Proposition 1; equations (4)–(6); Proposition A.3.'}),
    S('s14', {act:'mechanism',minutes:2.5,status:'analytical',title:'The same competition<br>widens the target-payoff spread.',defines:['Delta_T'],
      body:`<div class="payoff-cases"><article><h3>Incumbent value below ${mi(String.raw`\ell`)}</h3><p>Either challenger type wins and pays the same amount.</p><strong>No difference in target proceeds</strong></article><article class="accent-case"><h3>Incumbent value above ${mi(String.raw`\ell`)}</h3><p>A high-value challenger pays ${mi('R')}. A low-value challenger loses, and the incumbent pays ${mi(String.raw`\ell`)}.</p><strong>The difference is ${mi(String.raw`R-\ell`)}</strong></article></div><div class="equation-ribbon">${m(String.raw`\Delta_T(r)\equiv t_H-t_L=\mathbb E[(R-\ell)_+]=\frac{(r-\ell)^2}{2r}`)}${m(String.raw`\Delta_T'(r)>0`,'eq-small')}</div>`,
      notes:notes('This is the key payment argument. Below the low value both challenger types face the same winning payment. Above it, payments diverge across types. The stronger incumbent increases the expected positive part of its value above the low value. This makes the investor’s information more relevant to the traded payoff. A wider spread alone is not yet an equilibrium trading result.','For a general incumbent distribution the spread is the integral of its survival function above the low value. This yields the first-order stochastic comparative static.'),source:'Proposition 1; equations (4)–(6).'}),
    S('s15', {act:'mechanism',minutes:2.5,status:'analytical',title:'A price can reveal<br>the belief needed to prepare.',defines:['m','M'],
      body:`<div class="inference-steps"><article><span>Noise limits learning</span>${m(String.raw`m\le\mu_X\le M,\quad m=\frac{1}{1+e^{2/b}},\quad M=1-m`,'eq-small')}<p>The same bounds hold for the price posterior.</p></article><article><span>Low-cost preparation sustains the claim</span>${m(String.raw`c_L<B_r(m)\quad\Longrightarrow\quad e(P)\ge\rho>0`,'eq-small')}</article><article class="reveal" data-step="1"><span>Competitive pricing can be inverted</span>${m(String.raw`P=t_0+e(P)[t_L-t_0+\Delta_T\mu_X]`,'eq-small')}${m(String.raw`\mu_X=\frac{P-t_0-e(P)(t_L-t_0)}{e(P)\Delta_T}`,'eq-small')}</article></div>`,
      notes:notes('Spend time on the bridge from market makers to the buyer. Noise bounds the market-maker posterior for all order strategies. The low-cost floor ensures positive preparation, so the denominator of the inversion is positive. Although the buyer observes price alone, the equilibrium schedule lets it recover the posterior based on flow. The argument permits price jumps and atoms. The detailed threshold display is available in backup.','This result requires the preparation floor and positive spread. Without a floor, pooling and price sufficiency require separate analysis. See Propositions A.1 and A.2.'),source:'Section 3.2; equations (7)–(10); Propositions A.1–A.2.'}),
    S('s16', {act:'mechanism',minutes:2,status:'analytical',title:'Two claims respond<br>in opposite directions.',widget:'dial',defines:['A_H'],
      body:`<div class="split wide"><div class="stack"><div id="dial-vline"></div><div id="dial-curves"></div><div class="controls"><label for="dial-r">Strength r</label><input id="dial-r" type="range" min="1.01" max="3.6" step="0.01" value="1.2"><output id="dial-r-value"></output>${controls('dial-preset',[['weak','Weak'],['strong','Strong']])}</div></div><div class="stack"><div class="paired-readouts"><div id="dial-profit" class="readout"><p>Buyer profit at the prior</p><p class="metric"></p></div><div id="dial-spread" class="readout"><p>Target-payoff spread</p><p class="metric"></p></div></div>${m(String.raw`A_H(x)=e(P(x))\Delta_T[1-\mu_X(x)]`,'eq-small')}<p class="small">${mi('A_H')} is the investor’s residual advantage from buying in the high state. Preparation and residual uncertainty also matter.</p></div></div>`,
      notes:notes('Move between the declared weak and strong settings. The slider displays acquisition-stage payoffs, not an equilibrium solution at each strength. The profit curve falls while the spread rises. Competitive pricing incorporates expected preparation, but leaves a quality-informed investor a residual advantage. This advantage scales with the spread, preparation probability and remaining uncertainty. The theorem will compare global bounds to trading costs.','The low-state selling advantage has the analogous posterior factor. The global trading proof accounts for the way a larger order shifts the distribution of prices.'),source:'Figure 1; equations (5) and (11). Slider: acquisition-stage arithmetic.'}),
    S('s17', {act:'results',minutes:2,status:'analytical',title:'Three conditions establish<br>the reversal.',defines:['r_0','r_1'],
      subtitle:'Compare weak and strong incumbents: ℓ < r₀ < r₁ < h. Hold all other primitives fixed.',
      body:`<div class="theorem-conditions"><article><div><span>A1</span><h3>A preparation floor</h3><p>Low-cost preparation is worthwhile even at the worst feasible belief.</p></div>${m(String.raw`0\le c_L<B_{r_1}(m)`,'eq-small')}</article><article class="reveal" data-step="1"><div><span>A2</span><h3>A responsive high-cost margin</h3><p>The weak prior is insufficient. Favourable strong-economy news can justify preparation.</p></div>${m(String.raw`B_{r_0}(1/2)<c_H<B_{r_1}(M)`,'eq-small')}</article><article class="reveal" data-step="2"><div><span>A3</span><h3>Trading incentives switch</h3><p>Global bounds exclude trade in the weak economy and force full orders in the strong one.</p></div>${m(String.raw`\Delta_T(r_0)<k<\left(1-\frac1b\right)\rho m\Delta_T(r_1)`,'eq-small')}</article></div>`,
      notes:notes('Define r0 and r1 explicitly as the two strengths. Read each assumption by its job. A2 does not say the weak economy could never have favourable information; it compares the weak prior with a strong upper posterior. A3 is what forces the actual weak outcome to be uninformative. All declared benchmark assumptions remain in force. These sufficient conditions hold on a nonempty open set.','The right-hand side of A3 bounds marginal trading profits globally. It is stronger than merely evaluating profits at full orders.'),source:'Proposition 2, assumptions (A1)–(A3).'}),
    S('s18', {act:'results',theme:'dark',minutes:2,status:'analytical',title:'Stronger competition<br>can raise preparation.',defines:['E','O_H'],
      body:`<div class="theorem-result"><article><span>Weak incumbent</span>${m(String.raw`(q_H,q_L)=(0,0)`)}${m(String.raw`\mathsf E(r_0)=\rho`)}<p>An uninformative price.<br>Only low-cost preparation.</p></article><article class="reveal" data-step="1"><span>Strong incumbent</span>${m(String.raw`(q_H,q_L)=(1,-1)`)}${m(String.raw`\mathsf E(r_1)>\rho`)}<p>An informative price.<br>Additional high-cost preparation.</p></article></div><div class="theorem-scope"><p>Unique trading and on-path preparation under A1–A3, allowing arbitrary mixed orders.</p><p>${mi(String.raw`\mathsf O_H(r_1)>\mathsf O_H(r_0)`)}: high-value challenger ownership also rises. Off-path pricing rules need not be unique.</p></div>`,
      notes:notes('State Proposition 2. E is the probability the challenger prepares. OH is the unconditional probability the challenger has high value and acquires the target. In the weak economy every nonzero order has a gross advantage below its cost. In the strong economy every increase in a correctly signed order raises profit. Full orders generate favourable prices that recruit the high-cost margin.','The strong experiment strictly Blackwell dominates the uninformative weak experiment. Uniqueness does not extend to all off-path pricing specifications or every intermediate strength.'),source:'Proposition 2; analytical result.'}),
    S('s19', {act:'results',minutes:2,status:'analytical',title:'The benchmark makes<br>the reversal concrete.',widget:'economies',
      body:`<div id="economies-view"></div><div class="controls">${controls('benchmark',[['weak','Weak incumbent'],['strong','Strong incumbent']])}<button id="economies-compare">Compare both</button></div><p class="small">Declared model illustration: ${declaration}. Only incumbent strength differs between these economies.</p>`,
      notes:notes('Compare the two economies side by side. Distinguish preparation from high-value ownership. The additional preparation is tilted toward high challenger value. All values are illustrative outputs under the declared parameters; none is an empirical estimate. The theorem supports the endpoints rather than a continuous path between them.','The registry and Table 2 bind the displayed values. A comparison of strengths re-solves investor orders and preparation, whereas the next slide fixes the information experiment.'),source:'Section 4.2; Table 2, Panel A; validated benchmark registry.'}),
    S('s20', {act:'results',minutes:2,status:'numerical diagnostic',title:'Hold information fixed<br>and deterrence returns.',widget:'control',
      body:`<div class="split wide"><div class="stack"><div id="control-plot"></div><div class="controls">${controls('experiment',[['feedback','Equilibrium information'],['frozen','Same informative orders']])}</div></div><div class="stack"><div id="control-readout"></div><p class="large-note">The changing information experiment explains the reversal.</p><p class="small">Full informative orders are a counterfactual in the weak economy. They would not be chosen there in equilibrium.</p></div></div>`,
      notes:notes('Switch from feedback to the fixed-order comparison. When the information experiment is held fixed, lower acquisition profit at every posterior can only reduce preparation. In the strong economy the informative orders coincide with the equilibrium profile. In the weak economy they are imposed and unprofitable. The general fixed-experiment statement is analytical; these magnitudes are its numerical illustration.','The control holds informative orders fixed and constructs consistent prices. It does not hold a price level constant. Proposition A.3 gives the general comparison.'),source:'Proposition A.3; Section 4.2; Table 2, Panel B.'}),
    S('s21', {act:'scope',minutes:2.5,speakingMinutes:2,title:'The reversal has<br>a defined scope.',
      body:`<div class="scope-layout"><div class="stack"><h3>What survives</h3><div class="scope-row"><strong>Different noise</strong><span>Logistic example</span></div><div class="scope-row"><strong>Continuous costs</strong><span>Narrow atomless supports</span></div><div class="scope-row"><strong>Different knowledge</strong><span>A better-informed buyer can still learn from price</span></div><p class="small">Each extension has its own sufficient conditions and declared primitives.</p></div><div class="scope-boundary"><h3>What the theorem does not trace</h3><p>At intermediate strengths, informative and uninformative equilibria can coexist.</p><p>A still stronger incumbent can make high-cost preparation unprofitable even at the best feasible belief.</p><p class="small">Analytical endpoints, computer-assisted existence at selected nodes, and numerical searches remain distinct.</p></div></div>`,
      notes:notes('This slide deliberately separates robustness from the scope of the correspondence. Extensions show the mechanism under alternative primitives; they are not one common calibration. In the private-signal example the buyer has a more accurate signal, but the investor contributes complementary information. Intermediate coexistence prevents reading a smooth hump from the endpoints. Pause here if questions have accumulated; the planned timing includes some discussion allowance.','Backup slides show the full robustness table, the certified intervals, and the unjoined correspondence nodes. A failed search is not proof that an equilibrium does not exist.'),source:'Propositions 2–3 and A.5–A.7; Sections 4.3 and 5.'}),
    S('s22', {act:'scope',minutes:2.5,speakingMinutes:2,title:'Information access matters.<br>So does the payment rule.',
      body:`<div class="implication-grid"><article><h3>Access to prices</h3><p>At fixed incumbent strength and sale terms, price access raises expected target proceeds and net acquisition surplus in the benchmark.</p><div class="small-results"><span>Expected target proceeds</span><strong>${fmt('base_revenue_hidden',3)} <span>to</span> ${fmt('base_revenue_feedback',3)}</strong></div><p class="small">Analytical comparison. Per target share. Trading and pricing are re-solved in both economies.</p></article><article><h3>Sale terms</h3><p>Reserves and bargaining alter the sensitivity of target proceeds to challenger value.</p><p class="large-note">They change the information incentives as well as the payments.</p><p class="small">The optimal sale mechanism remains open. Bargaining results describe acquisition-stage payoffs.</p></article></div>`,
      notes:notes('Keep the comparison precise. Proposition A.9 changes price access under fixed strength and sale rule. Both economies have full orders, so trading costs are equal. The comparison does not rank incumbent strengths or alternative mechanisms. Changing the payment rule can reverse the spread response; solving trading and preparation under bargaining is separate work.','The access backup includes the matched-price dividend diagnostic. Reserve comparisons establish feasible supported outcomes, not an optimum over all equilibrium continuations.'),source:'Propositions A.8–A.9; Section 6; Table 2, Panel C.'}),
    S('s23', {act:'next',minutes:1,speakingMinutes:0.5,status:'open',title:'The seller’s design problem<br>is the next step.',
      body:`<div class="split"><div class="stack"><h3>Theory</h3><p class="large-note">Choose terms while accounting for the information and preparation they induce.</p><p>Multiple trading and price-pooling continuations make the seller’s objective an equilibrium-design problem.</p></div><div class="stack"><h3>Empirical work</h3><div class="research-steps"><p>Establish the public decision window.</p><p>Date substantive preparation.</p><p>Separate price learning from anticipated entry.</p></div><p class="small">A research agenda, not an empirical finding.</p></div></div>`,
      notes:notes('Spend one minute on the agenda, or shorten it if discussion has consumed the two-minute allowance. The next theory problem is the seller’s choice of terms and commitment timing with endogenous trading and possible price pooling. The empirical programme starts from process chronology, not a regression on announced bidder counts.','An envelope of found reserve revenues is not the seller’s solution. The empirical design and its outstanding identification challenges are in Online Appendix D.'),source:'Sections 6.3 and 7; Online Appendix C.6 and D.'}),
    S('s24', {act:'next',theme:'dark',minutes:1,speakingMinutes:0.5,title:'Competition changes<br>what a buyer can learn.',
      body:`<div class="closing"><p class="display">A stronger rival can make information<br>worth trading on.</p><p class="display accent">That information can make preparation<br>worth paying for.</p><p class="closing-author">Austin Li <span>Competition Creates Competition</span></p></div><div class="controls closing-links"><button data-goto="s17">The conditions</button><button data-goto="s20">The comparison</button><button data-goto="b1">Technical appendix</button><a href="main_filled.pdf" target="_blank" rel="noopener">Read the paper</a></div>`,
      notes:notes('Return to the original puzzle and stop. The payment rule links the entrant’s claim to a traded claim with different information incentives. Under the theorem’s conditions the information effect outweighs the direct deterrence force. The talk contains 38 minutes of planned exposition plus two minutes for interruptions, allocated within the final four slides in the running schedule.','Use the conditions, fixed-information comparison, or appendix links for discussion. The result remains conditional on the specified information and participation environment.'),source:'Section 8; Proposition 2.'}),

    S('b1', {
      act: 'backup',
      kicker: '',
      title: 'The trading outcome is pinned by <i>global</i> bounds.',
      subtitle: 'Arbitrary mixed orders and every continuous deviation are allowed.',
      widget: '',
      status: 'analytical',
      backup: true,
      defines: ['A_L'],
      body: `<div class="stack">${m(String.raw`\rho\,m\,\Delta_T\;\le\;A_H(x),\,A_L(x)\;\le\;\Delta_T`)}<div class="split"><div class="stack"><p class="kicker">Weak economy</p>${m(String.raw`\Delta_T(r_0)<k`, 'eq-small')}<p class="small">Every nonzero order has gross advantage below its cost.</p></div><div class="stack"><p class="kicker">Strong economy</p>${m(String.raw`k<\left(1-\tfrac1b\right)\rho\,m\,\Delta_T(r_1)`, 'eq-small')}<p class="small">Every increase in a correctly signed order pays for itself.</p></div></div>${defs('A_L')}</div>`,
      notes: 'The residual advantage is preparation probability times the payoff spread times the market’s remaining uncertainty, and the likelihood-ratio bounds together with the participation floor bracket it before any candidate order profile is chosen. The strong-economy condition is not a pointwise comparison of the residual with the trading cost. A larger order also shifts the distribution over prices and therefore over preparation states, and the bounded log-density derivative controls that second effect; the factor involving the noise scale comes from exactly there. That is why uniqueness covers mixed strategies and every continuous deviation rather than a two-point comparison. If asked: the full derivation is in Appendix A, and the measure-theoretic construction, including null-set invariance under deviations, is in the Online Appendix.',
      source: 'Propositions A.1 and A.2; equation (11); proof of Proposition 2.'
    }),

    S('b2', {
      act: 'backup',
      kicker: '',
      title: 'Bounded posteriors and the <i>plateau</i>.',
      subtitle: 'The noise law sets where posterior mass sits, not only where the bounds are.',
      widget: '',
      status: 'analytical',
      backup: true,
      body: `<div class="split"><div class="stack">${m(String.raw`e^{-2/b}\le\frac{f(x-q)}{f(x-q')}\le e^{2/b}`, 'eq-small')}${m(String.raw`m=\frac1{1+e^{2/b}},\qquad M=1-m`, 'eq-small')}<p class="small muted">Bounds ${v('base_m')} and ${v('base_M')} at the declared scale.</p></div><div class="stack"><p class="kicker">Laplace</p><p class="small">The upper bound is attained on a positive-probability tail, so preparation at indifference is real.</p><p class="kicker">Logistic</p><p class="small">The same bounds, reached only in the limit. Strong-economy preparation is ${pct('logistic_entry_strong')} against ${pct('base_entry_strong')}.</p></div></div>`,
      notes: 'Bounded likelihood ratios are what make the posterior bounded, and both noise laws have a log-density derivative bounded by the reciprocal of the scale, so the global trading bounds hold for both. The difference is where the mass sits. Laplace assigns positive probability to the flat region outside the full-order interval, so the upper bound is attained and the convention that an indifferent challenger prepares has bite. The logistic posterior approaches the same bounds only as flow diverges, so preparation is lower at the same declared scale. The comparison holds scale fixed rather than variance, and it is not a Blackwell ranking of the two noise laws. If asked: Proposition A.5 restates the equilibrium comparison under logistic noise, and Figure 3 plots the tail against threshold distance.',
      source: 'Section 3.2; equations (7) and (8); Proposition A.5; Section 5.1; Figure 3.'
    }),

    S('b3', {
      act: 'backup',
      kicker: '',
      title: 'Three <i>computer-assisted</i> equilibria.',
      subtitle: 'Enclosures at declared nodes, each coexisting with no trade.',
      widget: 'certificates',
      status: 'computer-assisted',
      backup: true,
      body: `<div id="certificate-table"></div><p class="small muted">Displayed intervals are rounded outward.</p>`,
      notes: 'The method is interval arithmetic. For the low-value investor, global strict concavity reduces optimality to a marginal-profit root, and opposite endpoint signs place that root inside the reported enclosure. For the high-value investor, a uniform derivative bound verifies that full purchases dominate every smaller order throughout the root bracket, and wrong-signed orders are unprofitable. The resulting preparation enclosures are disjoint and strictly ordered upward, which establishes the cross-economy ordering without assuming a branch. These are existence results at three declared strengths, not uniqueness claims and not a selected path, so I do not join the points. Each node also admits no trade at the same parameters. If asked: the full intervals, the certificate margins and the acceptance tolerances are in the recorded outputs, Appendix A and Online Appendix B.',
      source: 'Proposition 3; Section 4.3; Online Appendix B; numerics certificates output.'
    }),

    S('b4', {
      act: 'backup',
      kicker: '',
      title: 'Seeing the price <i>improves</i> acquisition outcomes.',
      subtitle: 'Fixed incumbent strength. Trading and pricing re-solved in both economies.',
      widget: 'access',
      status: 'analytical',
      backup: true,
      defines: ['V_T', 'd'],
      body: `<div class="split wide"><div class="stack"><div id="access-table"></div><p class="small muted">Per target share, net of preparation costs, with transfers between bidders, shareholders and traders excluded.</p></div><div class="stack"><p class="kicker">Matched price</p>${m(String.raw`(V_T+d)-(P+d)=V_T-P`, 'eq-big')}<p class="small">A deterministic external dividend of ${fmt('base_matched_dividend', 3)} in the price-hidden economy raises the terminal payoff and the price by the same amount, so trading incentives, revenue, surplus and preparation are unchanged while the mean financial price matches the feedback economy.</p>${defs('V_T,d')}</div></div>`,
      notes: 'This comparison changes access to the price at fixed incumbent strength; it does not change strength, the sale rule or the noise law. The global trading bound forces full orders even when the challenger cannot use the price, so both economies generate the same order-flow experiment and identical trading costs, and what differs is whether the buyer can condition on it. Each additional preparation decision contributes at least the cost it incurs in conditional expectation, and the gain also includes sales that would otherwise fail the reserve. The matched-price diagnostic answers the objection that the welfare difference is about the level of the price rather than its information content. If asked: the dividend is a diagnostic, not a feasible mechanism, it is paid by no bidder, and it raises no revenue.',
      source: 'Proposition A.9; Section 6.1; Table 2, Panel C and matched-price panel.'
    }),

    S('b5', {
      act: 'backup',
      kicker: '',
      title: 'Fixed-reserve comparisons with <i>supported</i> continuations.',
      subtitle: 'Preparation, a completed sale, and two admissible bidders are different events.',
      widget: 'reserve',
      status: 'numerical diagnostic',
      backup: true,
      body: `<div id="reserve-table"></div><p class="small muted">Per target share; the listed nodes have analytical support from the global trading bounds.</p>`,
      notes: 'The higher reserve excludes the low value class, which changes both the payment a winner makes and the gap in target proceeds across challenger types, and it can support informative trading even against a weak incumbent. That is why the table reports preparation, sale and two admissible bidders separately: once the reserve excludes bidders, a positive preparation probability is not evidence of more acquisition competition, and an excluded incumbent facing one possibly inadmissible challenger is not a two-bidder contest. To avoid making exclusion turn on a value atom, the second panel uses atomless value classes around the two levels. This demonstrates a feasible improvement over the original reserve, not an optimal one. If asked: the exploratory reserve summary is reported online with its unresolved counts, and I do not treat its maximum as the seller’s solution.',
      source: 'Section 6.3; Appendix A.7; Table 4; Online Appendix C.6.'
    }),

    S('b7', {
      act: 'backup',
      kicker: '',
      title: 'Sources and research <i>boundaries</i>.',
      subtitle: 'The benchmark paper and its recorded numerical outputs.',
      widget: '',
      status: '',
      backup: true,
      body: `<div class="split"><div class="stack"><p><a href="main_filled.pdf" target="_blank" rel="noopener">The working paper</a></p><p><a href="online_appendix_filled.pdf" target="_blank" rel="noopener">The Online Appendix</a></p><p><a href="provenance.json" target="_blank" rel="noopener">Data-source hashes</a></p></div><div class="references"><p><strong>Auction entry</strong><br>Fishman (1988); Hirshleifer and Png (1989); Levin and Smith (1994); Gentry and Stroup (2019); Roberts and Sweeting (2013); Persico (2000).</p><p><strong>Prices and real decisions</strong><br>Dow, Goldstein and Guembel (2017); Edmans, Goldstein and Jiang (2015); Goldstein and Guembel (2008); Luo (2005).</p><p><strong>Takeover setting</strong><br>Boone and Mulherin (2007); Betton et al. (2014); Cornelli and Li (2002); Imprivata (2016).</p></div></div>`,
      notes: 'Everything numerical in this deck is bound to recorded outputs by hash; the presentation build reruns no solver and establishes no result of its own, and the interactive panels only evaluate existing closed forms. Results keep separate labels throughout: analytical, computer-assisted, numerical diagnostic and open, with declared parameters marked as declarations. The boundaries I would name without prompting are the participation floor, the dependence of the sign on the payment rule, the open intermediate correspondence, the unsolved seller problem, and the absence of any empirical sample. Both PDFs and the provenance file are local, so they open offline during discussion. If asked: the full bibliography and the contribution discussion are in the manuscript rather than on this slide.',
      source: 'paper/main.md; paper/online_appendix.md; quantity registry and passed run manifests.'
    }),

    S('b8', {
      act: 'backup',
      kicker: '',
      title: 'Between the two economies, equilibria <i>coexist</i>.',
      subtitle: 'Three established nodes, certified intervals, and no path between them.',
      widget: 'coexist',
      status: 'computer-assisted',
      minutes: 0,
      backup: true,
      defines: ['r_2'],
      body: `<div class="split wide"><div class="stack"><div class="plot-shell"><div id="coexist-plot"></div><p class="plot-caption">Preparation against incumbent strength; certified intervals at the declared benchmark.</p></div></div><div class="stack">${rev(3, `<p class="display">Push strength far enough and even the best feasible news cannot cover the <i>expensive</i> cost.</p>`)}${rev(3, m(String.raw`B_{r_2}(M)<c_H\quad\Longrightarrow\quad \mathsf E=\rho`, 'eq-small'))}${defs('r_2')}</div></div>`,
      notes: 'Three things in order. First the analytical nodes: the two economies plus the collapse strength. They are points, and I do not join them. Second the certified nodes, where interval arithmetic encloses exact informative equilibria with strictly ordered preparation, each coexisting with no trade at the same parameters, because against an uninformative price a unilateral order cannot cover its cost. Third the collapse: where even the upper posterior bound fails to justify the expensive cost, trading stays informative but preparation returns to the floor. Participation is therefore not monotone in strength. The intermediate correspondence is open; the searches return continuations found, and absence of a branch establishes nothing. If asked: which equilibrium and why? I select none. I report every branch I can certify and read no monotone path into the gaps.',
      source: 'Proposition 2, part (iii); Proposition 3; Figure 2; Section 4.3.'
    }),

    S('b9', {
      act: 'backup',
      kicker: '',
      title: 'The mechanism <i>survives</i> changes in primitives.',
      subtitle: 'Preparation in the weak and the strong economy, specification by specification.',
      widget: '',
      status: 'analytical',
      minutes: 0,
      backup: true,
      body: `<table class="data-table"><thead><tr><th>Specification</th><th>Weak incumbent</th><th>Strong incumbent</th></tr></thead><tbody><tr><td>Laplace noise, atomic costs</td><td>${pct('base_entry_weak')}</td><td class="highlight">${pct('base_entry_strong')}</td></tr><tr><td>Logistic noise, atomic costs</td><td>${pct('base_entry_weak')}</td><td>${pct('logistic_entry_strong')}</td></tr><tr><td>Laplace noise, atomless costs</td><td>${pct('base_entry_weak')}</td><td>${pct('cost_mix_laplace_entry_strong')}</td></tr><tr><td>Moderate acquisition values</td><td>${pct('moderate_entry_weak')}</td><td>${pct('moderate_entry_strong')}</td></tr><tr><td>Complementary private signals</td><td>${pct('signal_entry_weak')}</td><td>${pct('signal_entry_strong')}</td></tr></tbody></table><p class="small muted">Each row is its own declared comparison at the declared benchmark, with its own sufficient conditions; levels are not comparable across rows.</p>`,
      notes: 'Take the rows as separate theorems rather than as a robustness sweep. Logistic noise has the same bounded log-density derivative, so the global trading bounds survive; what changes is where posterior mass sits, which is why the level differs. Narrow atomless cost supports preserve both the participation floor and the responsive expensive margin, so the cost atom is not doing the work. The moderate-value row removes the tenfold gap between acquisition values; what matters is where incumbent strength sits relative to the low value. The last row is the one that answers the obvious objection: the buyer there holds a more accurate private signal than the investor and the reversal still happens, because the signals are about different things. If asked: the moderate-value and private-signal rows use distinct parameter vectors, so this is not one joint calibration.',
      source: 'Propositions A.5, A.6 and A.7; Sections 5.1 to 5.3; Table 3.'
    }),

    S('b10', {
      act: 'backup',
      kicker: '',
      title: 'Change the payment rule and the sign <i>flips</i>.',
      subtitle: 'A zero-reserve, verifiable-value bargaining institution instead of the auction.',
      widget: 'bargaining',
      status: 'analytical',
      minutes: 0,
      backup: true,
      defines: ['eta', 'Delta_eta'],
      body: `<div class="split wide"><div class="stack"><div class="plot-shell"><div id="bargaining-plot"></div><p class="plot-caption">Target-payoff spread against the seller’s bargaining weight, at the declared benchmark.</p></div><div class="controls"><label for="seller-weight">Seller bargaining weight &eta;</label><input id="seller-weight" type="range" min="0" max="1" step="0.01" value="0.25"><output id="seller-weight-value" for="seller-weight"></output>${controls('eta', [['0.25', 'Below one half'], ['0.5', 'At one half'], ['0.75', 'Above one half']])}</div></div><div class="stack"><div id="bargaining-readout" class="stack"></div>${m(String.raw`\Delta_\eta=\eta\,(h-\ell)+(1-2\eta)\,\mathbb E[(R-\ell)_+]`, 'eq-small')}${defs('eta,Delta_eta')}</div></div>`,
      notes: 'Drag the weight and watch the sign of the comparative static change. Take a realised incumbent value above the low challenger value. A winning high-value challenger pays a blend of that value and its own, with sensitivity to the rival equal to one minus the seller’s weight. A losing low-value challenger leaves the rival paying, with sensitivity equal to the weight. Competition widens the spread precisely when the first exceeds the second, so the effect is positive below one half, zero at one half and negative above it, and the readout draws that flip. Challenger profit still weakly falls everywhere. This is payment-stage comparative statics only: trading, preparation and welfare under bargaining are not solved. If asked: no entry reversal is claimed under bargaining, the weight equal to one is a payment-stage endpoint with zero challenger profit.',
      source: 'Proposition A.8; Section 6.2; equation (14); Figure 4.'
    }),

    S('b11', {
      act: 'backup',
      kicker: '',
      title: 'Bounded posteriors, a threshold, and a residual <i>advantage</i>.',
      subtitle: 'One order-flow realisation in the strong economy, at full orders.',
      widget: 'tape',
      status: 'analytical',
      minutes: 0,
      backup: true,
      defines: ['m', 'M', 'tau', 'x_star', 'A_H'],
      body: `<div class="split wide"><div class="stack"><div class="plot-shell"><div id="tape-plot"></div><p class="plot-caption">Posterior against order flow; break-even belief marked; at the declared benchmark.</p></div><div class="controls"><label for="tape-x">Order flow X</label><input id="tape-x" type="range" min="-3" max="3" step="0.02" value="-1.5"><output id="tape-x-value" for="tape-x"></output><button id="tape-demo">Cross the threshold</button><button data-reset="tape">Reset</button></div><div class="row">${m(String.raw`m=\frac1{1+e^{2/b}},\quad M=1-m,\quad \tau=\frac{c_H-g_L}{g_H-g_L},\quad x^*=\frac b2\log\frac{\tau}{1-\tau}`, 'eq-small')}</div><div class="row">${m(String.raw`A_H(x)=e(x)\,\Delta_T\,[1-\mu(x)]`, 'eq-small')}</div></div><div class="stack"><div id="tape-readout" class="stack"></div>${defs('m,M,tau,x_star,A_H')}</div></div>`,
      notes: 'Drag the tape from a heavy sale to a heavy purchase. Bounded likelihood ratios under this noise law keep the posterior inside a band and flat outside the full-order interval, which is why the plateau matters later. Market makers price the preparation each flow induces, so the anticipated increase in proceeds is already in the price; what the investor keeps is the residual, which is preparation probability times the payoff spread times the market’s remaining uncertainty. When the posterior crosses the break-even belief, the expensive cost realisation prepares as well. This is one realisation inside a declared economy, not a re-solved model, and the readout averages over cost realisations at that flow. The challenger sees the price, not the flow. If asked: the bounds come from the noise law alone and hold for every candidate order distribution, mixtures included.',
      source: 'Sections 3.2 and 3.3; equations (7) to (12); Propositions A.1 and A.2.'
    }),
    S('b12', {act:'backup',backup:true,status:'analytical',title:'The acquisition-stage payoffs.',
      body:`<div class="split"><div class="stack">${m(String.raw`t_0=p(1-p/r)`)}${m(String.raw`t_H=r/2+p^2/(2r)`)}${m(String.raw`t_L=\ell-(\ell^2-p^2)/(2r)`)}</div><div class="stack">${m(String.raw`g_H=h-r/2-p^2/(2r)`)}${m(String.raw`g_L=(\ell^2-p^2)/(2r)`)}${m(String.raw`\Delta_T=(r-\ell)^2/(2r)`)}</div></div><p>All expectations integrate over the incumbent’s uniform value distribution. Quantities are per target share.</p>`,
      notes:notes('These are the exact closed forms used by the main deck widgets. Profit is conditional on challenger type and before preparation cost. Expected target proceeds without preparation depend on whether the incumbent clears the reserve.','Proposition 1 extends the directional comparisons to general continuous incumbent distributions.'),source:'Section 3.1; equation (4).'}),
    ...['values,institutions','preparation,trading','prices','derived,outcomes'].map((groups,i)=>S('b'+(13+i),{act:'backup',backup:true,title:['Values and sale terms.','Preparation and trading.','Prices and beliefs.','Derived payoffs and outcomes.'][i],widget:'glossary',body:`<div class="glossary-page" data-glossary-groups="${groups}"></div>`,notes:notes('Notation definitions use the same glossary source as the main presentation and the G-key panel.','The definitions retain the paper’s notation and identify the first slide where each symbol appears.'),source:'Section 2; Online Appendix C.0.'}))
  ];
};
