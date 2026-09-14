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
      'the cheap cost realisation, worth paying even after the worst feasible news',
      'preparation', String.raw`c_L`),

    g('c_H', String.raw`c_H`,
      'the expensive cost realisation, worth paying only after favourable news',
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
  const S = (id, o) => ({
    id,
    act: o.act || '',
    kicker: o.kicker || '',
    title: o.title || '',
    subtitle: o.subtitle || '',
    body: o.body || '',
    notes: o.notes || '',
    source: o.source || '',
    minutes: o.minutes === undefined ? 0 : o.minutes,
    widget: o.widget || '',
    backup: o.backup === true,
    status: o.status || '',
    defines: o.defines || []
  });
  const rev = (n, html) => `<div class="reveal" data-step="${n}">${html}</div>`;
  const controls = (name, options) => `<div class="segmented" role="group" aria-label="${name}">${options.map(([value, label]) => `<button data-choice="${name}" data-value="${value}" aria-pressed="false">${label}</button>`).join('')}</div>`;
  const defs = keys => `<div class="defs" data-defs="${keys}"></div>`;
  const declaration = `Benchmark declaration: h = ${v('base_h')}, ℓ = ${v('base_ell')}, p = ${v('base_p')}, ρ = ${v('base_rho')}, c<sub>L</sub> = ${v('base_c_low')}, c<sub>H</sub> = ${v('base_c_high')}, b = ${v('base_b')}, k = ${v('base_k')}.`;

  return [

    S('s01', {
      act: 'question',
      kicker: '',
      title: '',
      subtitle: '',
      widget: 'title',
      status: '',
      minutes: 0.5,
      body: `<div class="hero"><div class="stack"><h1>Competition<br><i>creates</i><br>competition.</h1><p class="sub">Stock prices and the discovery of takeover bidders</p><p class="byline">Austin Li</p></div><div id="title-ambient"></div></div>`,
      notes: 'Open with the sentence and hold for a beat. The title is a claim about direction, not about magnitude: a stronger rival lowers what a prospective buyer earns from winning, and can still bring that buyer into the contest, because the stock price it watches before committing to preparation becomes more informative. Everything in the next forty minutes is a comparison between declared economies, not an empirical estimate and not a calibration to any transaction. Say who I am, that the paper is single-authored, and that I would rather take questions as they arise than save them. If asked: the whole talk is the benchmark paper; the endogenous-research fork is separate work and is not in this deck.',
      source: 'Competition Creates Competition: Stock Prices and the Discovery of Takeover Bidders.'
    }),

    S('s02', {
      act: 'question',
      kicker: 'The institution',
      title: 'A public sale, a traded stock, and a buyer deciding whether to <i>prepare</i>.',
      subtitle: 'The interval this paper is about, described before any notation.',
      widget: '',
      status: '',
      minutes: 2.5,
      body: `<div class="timeline"><article><strong>Sale opportunity</strong><p>The chance to buy the target becomes publicly understood.</p></article><article><strong>The stock trades</strong><p>Investors who follow the target can still act on what they know.</p></article><article class="reveal" data-step="1"><strong>One buyer prepared</strong><p>An approaching party has done its diligence and can bid.</p></article><article class="reveal" data-step="1"><strong>Another deciding</strong><p>A second buyer has not committed the verification, financing and capacity an offer requires.</p></article><article class="reveal" data-step="2"><strong>Executable bids</strong><p>Only prepared buyers can submit binding offers.</p></article><article class="reveal" data-step="2"><strong>Acquisition</strong><p>Ownership is settled.</p></article></div>${rev(3, '<div class="callout">Imprivata’s definitive proxy separates an unsolicited approach, outreach to a list of potential buyers, and indications of interest conditional on further diligence: three distinct dates, in that order, in one disclosure record.</div>')}`,
      notes: 'The model needs an interval, not a date. A disclosed approach, an announced strategic review or an open contest can create one; none does so automatically. A wholly confidential process that becomes public only after the buyer set is fixed does not qualify, because no prospective buyer could have watched the price when it mattered. Preparation is a participation cost, not an optional report: a buyer that declines it stays out rather than bidding its prior expected value. The Imprivata chronology shows that this staged structure exists in the disclosure record. It is not evidence that a price drew any buyer in, which is what an empirical study would have to establish. If asked: whether a given deal fits is a question about its own chronology, and this paper settles it for no transaction.',
      source: 'Section 1.1; Online Appendix D. Imprivata (2016); Boone and Mulherin (2007).'
    }),

    S('s03', {
      act: 'question',
      kicker: 'The myth',
      title: 'Stronger rivals <i>deter</i> entry.',
      subtitle: 'Hold the buyer’s information fixed and the logic is airtight.',
      widget: '',
      status: '',
      minutes: 2,
      body: `<div class="split"><div class="stack"><p class="display">A stronger rival means less profit from winning.</p><p class="display muted">Less profit means less reason to pay to compete.</p>${rev(1, '<div class="callout">Every one of these holds the information available before the entry decision fixed. That is the assumption this paper moves.</div>')}</div><div class="references"><p><strong>Fishman (1988)</strong><br>A preemptive high bid deters a rival that must pay an investigation cost before it can bid at all.</p><p><strong>Hirshleifer and Png (1989)</strong><br>Costly information acquisition before entry is discouraged when the expected surplus from winning falls.</p><p><strong>Levin and Smith (1994)</strong><br>Entry is an equilibrium object: bidders mix into an auction until the expected return to participating is driven to zero.</p><p><strong>Gentry and Stroup (2019)</strong><br>Takeover competition forms before public bidding, and the identity of who enters is selected, not random.</p><p><strong>Roberts and Sweeting (2013)</strong><br>When entry is selective, the seller’s choice of procedure changes who shows up, not only what they pay.</p></div></div>`,
      notes: 'Take the received logic seriously before departing from it. A stronger rival raises the payment a winning buyer must make, so the return to the costly preparation that precedes an executable bid falls, and fewer buyers find that preparation worthwhile. Nothing in my paper overturns any of these results; the deterrence force survives intact and reappears as a formal statement two acts from now. What they share is a fixed information environment before the entry decision. Once the price a buyer can watch is itself an equilibrium object, competition moves it, and the two forces can point in opposite directions. If asked: yes, this is the standard comparative static, and I reproduce it exactly when I hold the price experiment fixed on the control slide.',
      source: 'Section 1; Proposition 1. Fishman (1988); Hirshleifer and Png (1989); Levin and Smith (1994); Gentry and Stroup (2019); Roberts and Sweeting (2013).'
    }),

    S('s04', {
      act: 'question',
      kicker: 'The question',
      title: 'Can a stronger rival <i>bring</i> a buyer in?',
      subtitle: 'One question, one answer, and three things the rest of the talk has to show.',
      widget: '',
      status: '',
      minutes: 2,
      body: `<p class="display">Yes, on an open set of primitives, because competition changes what the price <i>reveals</i> before the buyer decides.</p><div class="split">${rev(1, '<div class="stack"><p class="kicker">Reversal</p><p>Preparation rises with rival strength, and so does the chance that the better buyer ends up owning the target.</p></div>')}${rev(2, '<div class="stack"><p class="kicker">Control</p><p>Hold the information the price carries fixed and ordinary deterrence comes straight back.</p></div>')}${rev(3, '<div class="stack"><p class="kicker">Coexistence</p><p>In between, informative and uninformative outcomes can both be equilibria at the same primitives.</p></div>')}</div>`,
      notes: 'State the question in the form a theorist can refuse. I am not claiming that deterrence is wrong; I am claiming that it can be outweighed, and I owe you the set of primitives on which that happens. The answer has three parts and the talk delivers them in order. The reversal is the theorem. The control is the diagnostic that says the information channel, and not something else in the model, is doing the work. The coexistence result is the honest boundary: I do not have the full correspondence between the two economies, and I will not pretend that a monotone path joins them. If asked: the open set is described by three strict inequalities, and I show them explicitly rather than asserting non-emptiness.',
      source: 'Sections 1 and 4; Propositions 2 and 3; Proposition A.3.'
    }),

    S('s05', {
      act: 'preview',
      kicker: 'The mechanism in one picture',
      title: 'Two claims on one <i>surplus</i>.',
      subtitle: 'No notation yet. Just the value line and what each party holds.',
      widget: 'preview',
      status: '',
      minutes: 1.5,
      body: `<div class="split wide"><div class="plot-shell"><div id="preview-vline"></div><p class="plot-caption">One value line: the reserve, the two values a challenger can have, and the range the rival’s value is drawn from.</p></div><div class="stack">${rev(1, '<div class="callout">Stretch the rival’s range upward and what the challenger keeps if it wins shrinks at every belief.</div>')}${rev(2, '<div class="callout">The same stretch widens the gap between what shareholders receive from a high-value challenger and from a low-value one.</div>')}${rev(3, '<div class="callout">An investor who knows which challenger this is can trade on that gap, and the price it moves reaches the challenger before it has to pay to prepare.</div>')}</div></div>`,
      notes: 'This is the whole paper without a symbol in it. The sale rule splits one acquisition surplus into two claims. The buyer holds what it keeps if it prepares, bids and wins. Target shareholders hold what the auction pays them. A stronger rival raises the payment a winning high-value buyer must make, which shrinks the first claim, and at the same time widens the spread in the second, because a losing low-value buyer merely sets what the rival pays. Those two movements are the opposition the rest of the talk formalises. Draw the brackets slowly; most of the questions later are really questions about this picture. If asked: the direction of both movements is a property of the payment rule, and the bargaining slide shows an institution where the second one reverses.',
      source: 'Sections 1 and 3.1; Proposition 1.'
    }),

    S('s06', {
      act: 'preview',
      kicker: 'Antecedents',
      title: 'Learning from prices, and what is <i>new</i> here.',
      subtitle: 'Where the mechanism sits, and the one thing it adds.',
      widget: '',
      status: '',
      minutes: 1,
      body: `<div class="references three"><p><strong>Dow, Goldstein and Guembel (2017)</strong><br>A real investment decision that responds to the price creates the incentive to produce information about it.</p><p><strong>Edmans, Goldstein and Jiang (2015)</strong><br>Corrective real decisions can discourage trading on bad news, because rational pricing anticipates the correction.</p><p><strong>Luo (2005)</strong><br>Acquirers learn from announcement returns, but at the completion stage, after the participation decision studied here.</p><p><strong>Persico (2000)</strong><br>The auction format changes bidders’ incentives to acquire information; here the informed party is outside the auction.</p><p><strong>Betton, Eckbo, Thompson and Thorburn (2014)</strong><br>Takeover negotiations with stock-market feedback, once a deal has been initiated rather than before a buyer decides to prepare.</p></div>${rev(1, '<div class="callout">The increment: two claims on one surplus that respond to competition in opposite directions, and the participation reversal that opposition makes possible.</div>')}`,
      notes: 'One minute, placed here so the audience knows what kind of object is coming. The closest antecedent is Dow, Goldstein and Guembel, where a real decision feeds back into information production. What the sale rule adds is a division: the traded claim and the entrant’s claim are two parts of one surplus, and a change in competition moves them against each other. That opposition, and the reversal in participation it can produce, is the increment over generic learning from prices. The informed party here trades a payoff that is not the entrant’s profit, which is what separates this from information acquisition inside an auction. If asked: I also exclude toeholds, free riding and endogenous investor research, and I say why in the model section.',
      source: 'Section 1. Dow, Goldstein and Guembel (2017); Edmans, Goldstein and Jiang (2015); Luo (2005); Persico (2000); Betton et al. (2014).'
    }),

    S('s07', {
      act: 'model',
      kicker: 'Players and values',
      title: 'Two bidders, one target, one <i>reserve</i>.',
      subtitle: 'The incumbent is already prepared. The challenger is not.',
      widget: '',
      status: 'input',
      minutes: 1.5,
      defines: ['R', 'r', 'theta', 'ell', 'h', 'p'],
      body: `<div class="split"><div class="stack">${m(String.raw`R\sim U[0,r]`)}${m(String.raw`\theta\in\{\ell,h\}`)}${m(String.raw`0<p<\ell<r<h`)}<p class="small muted">Standalone value is normalised to zero; everything is per target share.</p></div>${defs('R,r,theta,ell,h,p')}</div>`,
      notes: 'Only what the mechanism needs. The incumbent has already prepared and bids its own value, which stays private until the auction. Its strength is the public distribution of that value, conditional on what the record reveals when the opportunity becomes visible, so raising it is a first-order stochastic shift rather than an announced offer, which keeps signalling and negotiation outside the paper. The challenger does not know its own value: preparation is what reveals it. Values, the preparation cost and noise demand are mutually independent. The seller commits to a cash second-price auction with the reserve before any trading happens. If asked: the uniform distribution is for the closed forms only; Proposition 1 is stated for any continuous incumbent distribution.',
      source: 'Sections 2.1 and 2.2; equation (1); Online Appendix C.0.'
    }),

    S('s08', {
      act: 'model',
      kicker: 'Preparation',
      title: 'A cost that must be paid before an <i>executable</i> bid.',
      subtitle: 'One challenger, one realised cost, drawn after the price is seen.',
      widget: '',
      status: 'input',
      minutes: 1.5,
      defines: ['C', 'c_L', 'c_H', 'rho', 'e'],
      body: `<div class="split"><div class="stack">${m(String.raw`\Pr(C=c_L)=\rho,\quad \Pr(C=c_H)=1-\rho`, 'eq-small')}${m(String.raw`0\le c_L<c_H`, 'eq-small')}${m(String.raw`e\in\{0,1\}`, 'eq-small')}<p class="small muted">Paying the cost reveals the challenger’s value and permits a bid; declining leaves it outside the sale.</p></div>${defs('C,c_L,c_H,rho,e')}</div>`,
      notes: 'One challenger with one realised cost, not a cheap buyer and an expensive buyer side by side. The two realisations have different jobs. The cheap one is a participation floor: some preparation happens at every feasible price, which keeps target proceeds sensitive to who the challenger is. The expensive one is the responsive margin that a favourable price recruits. Without a floor the two sides unravel together: nobody prepares, proceeds carry no information about quality, and there is nothing left to trade on. So information here means information about the challenger’s acquisition value, valuable only because participation is already positive. If asked: why not drop the stochastic cost? The low-cost floor is what keeps the investor an insider at every price; removing it is a different model and outside this talk.',
      source: 'Section 2.1; Proposition 2, condition (A1); Proposition A.6.'
    }),

    S('s09', {
      act: 'model',
      kicker: 'Trading',
      title: 'An informed investor, noise demand, and a <i>competitive</i> price.',
      subtitle: 'Neither bidder trades. The investor cannot acquire the target.',
      widget: '',
      status: 'input',
      minutes: 2,
      defines: ['q', 'Z', 'b', 'X', 'k', 'P', 'mu'],
      body: `<div class="split"><div class="stack">${m(String.raw`q\in[-1,1]`, 'eq-small')}${m(String.raw`X=q+Z,\quad Z\sim\mathrm{Laplace}(0,b)`, 'eq-small')}${m(String.raw`P(X)=\mathbb E[\,\text{target proceeds}\mid X\,]`, 'eq-small')}${m(String.raw`\mu=\Pr(\theta=h\mid X)`, 'eq-small')}<p class="small muted">The investor pays a linear cost k per unit traded and holds no initial position.</p></div>${defs('q,Z,b,X,k,P,mu')}</div>`,
      notes: 'Four information sets and no overlap between trading and bidding. The investor observes the challenger’s value and nothing about the incumbent beyond its public distribution; it has no position, no control rights and no route to acquiring the target, so this is not a toehold or a free-riding story. Market makers see aggregate flow and only aggregate flow, and they price the preparation each price will induce, so nothing here rests on mispricing. The trading cost is an execution or carrying friction, separate from the adverse-selection impact the pricing rule already generates. The benchmark gives the investor perfect information and the buyer none, which is the extreme case; the robustness slide removes both extremes. If asked: the bound on orders is a normalised trading unit, not ownership, and uniqueness allows arbitrary mixtures within it.',
      source: 'Section 2.2; equations (2) and (3); Online Appendix C.0.'
    }),

    S('s10', {
      act: 'model',
      kicker: 'Timing',
      title: 'Sale rule, order, price, cost, preparation, <i>bids</i>.',
      subtitle: 'The price arrives before the buyer has to commit.',
      widget: '',
      status: 'input',
      minutes: 1.5,
      body: `<div class="timeline"><article><strong>Sale rule</strong><p>The seller commits publicly to the auction and its reserve ${mi(String.raw`p`)}.</p></article><article><strong>Order</strong><p>The investor learns the challenger’s value and submits ${mi(String.raw`q`)}.</p></article><article><strong>Price</strong><p>Market makers see flow and set ${mi(String.raw`P(X)`)}.</p></article><article class="reveal" data-step="1"><strong>Cost</strong><p>The challenger draws ${mi(String.raw`C`)} privately.</p></article><article class="reveal" data-step="1"><strong>Preparation</strong><p>It observes the price and its cost and chooses ${mi(String.raw`e`)}.</p></article><article class="reveal" data-step="2"><strong>Bids</strong><p>Prepared bidders learn ${mi(String.raw`R`)} and ${mi(String.raw`\theta`)} and bid truthfully.</p></article></div><p class="small muted">${declaration}</p>`,
      notes: 'Read the order of moves out loud once; it is the only thing on this slide that matters. The sale rule is committed before any trading, so the seller is not reacting to the price. The challenger sees the price and its own cost, never the order flow, the investor’s information or the incumbent’s realised value. Bids are truthful and weakly dominant, so the auction stage adds no strategic content. The parameter line at the bottom is a declaration, not an estimate and not a calibration: it fixes the economy in which the later figures are drawn. Everything in the talk is a comparison between declared economies. If asked: press G at any point and the full notation panel opens, so no symbol has to be remembered.',
      source: 'Section 2.2; Online Appendix C.0 input declarations.'
    }),

    S('s11', {
      act: 'model',
      kicker: 'The auction',
      title: 'Who wins, who pays, who <i>keeps</i> the surplus.',
      subtitle: 'Acquisition arithmetic, conditional on the challenger having prepared.',
      widget: 'auction',
      status: 'analytical',
      minutes: 2,
      defines: ['g_H', 'g_L', 't', 'Delta_T', 'B'],
      body: `<div class="split wide"><div class="stack"><div class="plot-shell"><div id="auction-vline"></div><p class="plot-caption">Challenger value and realised incumbent value, per target share.</p></div><div class="controls">${controls('quality', [['H', 'High challenger'], ['L', 'Low challenger']])}<label for="auction-r">Realised incumbent value R</label><input id="auction-r" type="range" min="0" max="3" step="0.05" value="0.8"><output id="auction-r-value" for="auction-r"></output><button data-reset="auction">Reset</button></div><div class="row">${m(String.raw`g_H=h-\frac r2-\frac{p^2}{2r},\qquad g_L=\frac{\ell^2-p^2}{2r}`, 'eq-small')}</div><div class="row">${m(String.raw`\Delta_T=t_H-t_L=\frac{(r-\ell)^2}{2r},\qquad B_r(\mu)=\mu\,g_H+(1-\mu)\,g_L`, 'eq-small')}</div></div><div class="stack"><div id="auction-readout" class="stack"></div>${defs('g_H,g_L,t,Delta_T,B')}</div></div>`,
      notes: 'Walk the value line rather than the algebra. Start with a high-value challenger and a low realised incumbent value: the challenger wins and pays the reserve. Drag the realised value upward and the challenger still wins but pays more, so its profit falls one for one with the payment. Now switch to the low-value challenger and cross its value: below it the challenger wins and pays the incumbent’s bid; above it the incumbent wins and the challenger’s own bid sets what the incumbent pays. That asymmetry is the entire source of the spread. This display is auction arithmetic conditional on preparation, not an equilibrium simulation, and ties are broken toward the incumbent for drawing only. If asked: the same comparison holds for any continuous incumbent distribution, which is what Proposition 1 states.',
      source: 'Section 3.1; equations (4) and (5); Table 1.'
    }),

    S('s12', {
      act: 'equilibrium',
      kicker: 'Equilibrium',
      title: 'Prices are Bayesian; deviations hold schedules <i>fixed</i>.',
      subtitle: 'What an equilibrium is here, and the two comparisons that must not be confused.',
      widget: '',
      status: '',
      minutes: 2,
      defines: ['sigma', 'mu_P', 'e_schedule'],
      body: `<div class="split wide"><div class="stack">${m(String.raw`(\sigma_H,\sigma_L;\;P,\;\mu_P,\;e)`)}<div class="conditions"><div class="cond"><b>1</b><p class="job">Pricing is Bayesian: the price is the expected terminal payoff of a target share given order flow, anticipating the preparation it will induce.</p><div class="formal">${m(String.raw`P(X)=\mathbb E[\,\text{target proceeds}\mid X\,]`, 'eq-small')}</div></div><div class="cond"><b>2</b><p class="job">The investor’s orders are optimal against a fixed price rule and a fixed preparation schedule, and may be arbitrary mixtures.</p></div><div class="cond"><b>3</b><p class="job">The challenger prepares exactly when expected gross profit at the posterior it reads off the price covers its realised cost.</p><div class="formal">${m(String.raw`B_r(\mu_P)\ge C`, 'eq-small')}</div></div><div class="cond"><b>4</b><p class="job">Prepared bidders bid truthfully, which is weakly dominant in the second-price auction.</p></div></div></div><div class="stack"><div class="split"><div class="stack"><p class="kicker">A deviation</p><p>The investor changes its order against a fixed price function and preparation schedule. It does not get to reprice the market.</p></div><div class="stack"><p class="kicker">A comparison</p><p>A primitive changes, and prices, trading and preparation are re-solved together.</p></div></div>${defs('sigma,mu_P,e_schedule')}</div></div>`,
      notes: 'One slide, and it prevents half the objections. An equilibrium is conditional order distributions, a measurable price function, Bayesian beliefs given the observed price, optimal preparation and truthful bidding. Beliefs are Bayesian including at atoms, so price jumps and entry jumps are permitted and the arguments never need differentiable prices. The uniqueness claims later use the deviation notion and allow every continuous deviation from arbitrary mixtures, so no candidate order profile is assumed anywhere. The comparison notion is what the two economies later are: strength changes and everything is re-solved. Confusing the two is the fastest way to misread the control slide. If asked: yes, the price can have atoms, and price sufficiency still holds, which is Proposition A.2.',
      source: 'Section 2.3; Propositions A.1 and A.2.'
    }),

    S('s13', {
      act: 'equilibrium',
      kicker: 'What the price reveals',
      title: 'Bounded posteriors, a threshold, and a residual <i>advantage</i>.',
      subtitle: 'One order-flow realisation in the strong economy, at full orders.',
      widget: 'tape',
      status: 'analytical',
      minutes: 3,
      defines: ['m', 'M', 'tau', 'x_star', 'A_H'],
      body: `<div class="split wide"><div class="stack"><div class="plot-shell"><div id="tape-plot"></div><p class="plot-caption">Posterior against order flow; break-even belief marked; at the declared benchmark.</p></div><div class="controls"><label for="tape-x">Order flow X</label><input id="tape-x" type="range" min="-3" max="3" step="0.02" value="-1.5"><output id="tape-x-value" for="tape-x"></output><button id="tape-demo">Cross the threshold</button><button data-reset="tape">Reset</button></div><div class="row">${m(String.raw`m=\frac1{1+e^{2/b}},\quad M=1-m,\quad \tau=\frac{c_H-g_L}{g_H-g_L},\quad x^*=\frac b2\log\frac{\tau}{1-\tau}`, 'eq-small')}</div><div class="row">${m(String.raw`A_H(x)=e(x)\,\Delta_T\,[1-\mu(x)]`, 'eq-small')}</div></div><div class="stack"><div id="tape-readout" class="stack"></div>${defs('m,M,tau,x_star,A_H')}</div></div>`,
      notes: 'Drag the tape from a heavy sale to a heavy purchase. Bounded likelihood ratios under this noise law keep the posterior inside a band and flat outside the full-order interval, which is why the plateau matters later. Market makers price the preparation each flow induces, so the anticipated increase in proceeds is already in the price; what the investor keeps is the residual, which is preparation probability times the payoff spread times the market’s remaining uncertainty. When the posterior crosses the break-even belief, the expensive cost realisation prepares as well. This is one realisation inside a declared economy, not a re-solved model, and the readout averages over cost realisations at that flow. The challenger sees the price, not the flow. If asked: the bounds come from the noise law alone and hold for every candidate order distribution, mixtures included.',
      source: 'Sections 3.2 and 3.3; equations (7) to (12); Propositions A.1 and A.2.'
    }),

    S('s14', {
      act: 'results',
      kicker: 'Proposition 1',
      title: 'One auction, two claims, <i>opposite</i> responses.',
      subtitle: 'Move the distribution of incumbent value, not a realised draw.',
      widget: 'dial',
      status: 'analytical',
      minutes: 2.5,
      body: `<div class="split wide"><div class="stack"><div class="plot-shell"><div id="dial-vline"></div><p class="plot-caption">The incumbent’s range stretches as strength rises.</p></div><div class="plot-shell"><div id="dial-curves"></div><p class="plot-caption">Gross challenger profit and the target-payoff spread against strength, annotated at the declared benchmark.</p></div><div class="controls"><label for="dial-r">Incumbent strength r</label><input id="dial-r" type="range" min="1.01" max="3.6" step="0.01" value="1.2"><output id="dial-r-value" for="dial-r"></output>${controls('dial-preset', [['weak', 'Weak'], ['strong', 'Strong']])}</div></div><div class="stack"><div class="readout" id="dial-profit"><p class="kicker">Gross profit at the prior</p><p class="metric"></p></div><div class="readout" id="dial-spread"><p class="kicker">Target-payoff spread</p><p class="metric"></p></div>${rev(1, '<p class="display">The challenger keeps <i>less</i> at every belief; shareholders’ proceeds become more sensitive to who the challenger is.</p>')}</div></div>`,
      notes: 'This is the engine of the paper, so give it the time. Keep the distinction from the auction slide explicit: there we moved a realised draw, here we move the distribution. Drag from the weak preset to the strong preset and the two readouts move against each other. Gross acquisition profit at the prior falls because the winning payment rises. The spread rises because the gap between what shareholders receive from a winning high-value challenger and from a winning incumbent widens. Both are acquisition-stage payoffs, with no claim that any point along the slider is an equilibrium, and nothing is solved in the deck. If asked: the spread is the expectation of the incumbent value above the low value, truncated below, so it rises under any first-order strengthening, not only the uniform one.',
      source: 'Proposition 1; equations (4) to (6); Figure 1.'
    }),

    S('s15', {
      act: 'results',
      kicker: 'Proposition 2',
      title: 'Three conditions, one <i>open</i> set.',
      subtitle: 'Strict inequalities, jointly satisfiable, and not a knife edge.',
      widget: '',
      status: 'analytical',
      minutes: 2,
      defines: ['r_0', 'r_1'],
      body: `<div class="conditions"><div class="cond"><b>A1</b><p class="job">Cheap preparation is worthwhile even after the worst feasible news.</p><div class="formal reveal" data-step="1">${m(String.raw`0\le c_L<B_{r_1}(m)`, 'eq-small')}</div></div><div class="cond"><b>A2</b><p class="job">Expensive preparation needs favourable news, and only the strong economy can supply it.</p><div class="formal reveal" data-step="2">${m(String.raw`B_{r_0}(1/2)<c_H<B_{r_1}(M)`, 'eq-small')}</div></div><div class="cond"><b>A3</b><p class="job">Trading loses money in the weak economy and pays at every correctly signed order in the strong one.</p><div class="formal reveal" data-step="3">${m(String.raw`\Delta_T(r_0)<k<\left(1-\tfrac1b\right)\rho\,m\,\Delta_T(r_1)`, 'eq-small')}</div></div></div>${rev(4, '<p class="display">Then trading and on-path preparation are <i>unique</i> in both economies, and preparation is strictly higher against the stronger incumbent.</p>')}${defs('r_0,r_1')}`,
      notes: 'Read each condition by its job before showing the inequality. A1 is the participation floor. A2 places the expensive cost above anything the weak economy can justify and below what the best feasible strong-economy belief delivers, which puts the break-even belief strictly inside the feasible band. A3 puts the trading cost above every possible informational return in the weak economy and below a global bound on marginal trading profit in the strong one. These are strict inequalities on a nonempty open set, so this is not a knife edge, and uniqueness comes from global bounds rather than from searching over candidate profiles. If asked: why not drop the stochastic cost? The low-cost floor is what keeps the investor an insider at every price; endogenising it is a different model and outside this talk.',
      source: 'Proposition 2, parts (i) and (ii); conditions (A1) to (A3); Appendix A.'
    }),

    S('s16', {
      act: 'results',
      kicker: 'Proposition 2, seen',
      title: 'Stronger competition <i>raises</i> preparation.',
      subtitle: 'Same primitives in both economies. Only incumbent strength differs.',
      widget: 'economies',
      status: 'analytical',
      minutes: 2,
      defines: ['E', 'O_H'],
      body: `<div class="split wide"><div class="stack"><div id="economies-view"></div><p class="plot-caption">Preparation and high-value ownership in the two economies, at the declared benchmark.</p><div class="controls">${controls('benchmark', [['weak', 'Weak incumbent'], ['strong', 'Strong incumbent']])}<button id="economies-compare">Compare both</button></div></div><div class="stack">${m(String.raw`\mathsf E=\Pr(\text{the challenger prepares})`, 'eq-small')}${m(String.raw`\mathsf O_H=\Pr(\text{a high-value challenger owns the target})`, 'eq-small')}${defs('E,O_H')}</div></div>`,
      notes: 'Show the weak economy first: no trade, an uninformative price, preparation at the floor, because the investor’s best possible gross advantage is below its trading cost. Then the strong economy: correctly signed full orders, an informative price, and the expensive cost realisation preparing after favourable flows. Then compare them side by side. In each economy the trading outcome and the on-path preparation outcome are unique, allowing arbitrary mixtures and every continuous deviation, so neither is a selected equilibrium. These are model outputs at declared primitives, not empirical estimates and not a joint calibration. High-value ownership rises with preparation because the extra entry is tilted toward high values. If asked: the deterrence force is unchanged between the panels; what moves is the information experiment, and the next slide isolates exactly that.',
      source: 'Proposition 2; Section 4.2; Table 2, Panel A.'
    }),

    S('s17', {
      act: 'results',
      kicker: 'Control one',
      title: 'Freeze the information and deterrence <i>returns</i>.',
      subtitle: 'Hold the investor’s orders at their informative level while strength rises.',
      widget: 'control',
      status: 'numerical diagnostic',
      minutes: 2,
      body: `<div class="split wide"><div class="stack"><div class="plot-shell"><div id="control-plot"></div><p class="plot-caption">Preparation in the weak and strong economies, at the declared benchmark.</p></div><div class="controls">${controls('experiment', [['feedback', 'Endogenous information'], ['frozen', 'Fixed information']])}</div></div><div class="stack"><div id="control-readout" class="stack"></div>${rev(1, '<p class="display">With the price experiment held fixed, a stronger rival can only <i>remove</i> a reason to prepare.</p>')}</div></div>`,
      notes: 'This is the decisive diagnostic, and the slide to come back to whenever someone doubts the channel. Under endogenous information, preparation rises with strength. Switch to the frozen experiment, which holds the investor’s orders at their informative level in both economies, and preparation falls, exactly as the received logic predicts. That statement is general: at every belief and every cost realisation, lower gross acquisition profit can only remove a preparation incentive, for any fixed information experiment. The frozen weak-incumbent profile is a control and not an investor equilibrium, since full orders are unprofitable there and admit profitable deviations. Its only job is to isolate the ordinary deterrence force. If asked: in the strong economy the frozen profile coincides with the equilibrium profile, so the whole difference between the panels comes from the weak economy.',
      source: 'Proposition A.3; Section 4.2; Table 2, Panel B.'
    }),

    S('s18', {
      act: 'results',
      kicker: 'Control two',
      title: 'Change the payment rule and the sign <i>flips</i>.',
      subtitle: 'A zero-reserve, verifiable-value bargaining institution instead of the auction.',
      widget: 'bargaining',
      status: 'analytical',
      minutes: 2,
      defines: ['eta', 'Delta_eta'],
      body: `<div class="split wide"><div class="stack"><div class="plot-shell"><div id="bargaining-plot"></div><p class="plot-caption">Target-payoff spread against the seller’s bargaining weight, at the declared benchmark.</p></div><div class="controls"><label for="seller-weight">Seller bargaining weight &eta;</label><input id="seller-weight" type="range" min="0" max="1" step="0.01" value="0.25"><output id="seller-weight-value" for="seller-weight"></output>${controls('eta', [['0.25', 'Below one half'], ['0.5', 'At one half'], ['0.75', 'Above one half']])}</div></div><div class="stack"><div id="bargaining-readout" class="stack"></div>${m(String.raw`\Delta_\eta=\eta\,(h-\ell)+(1-2\eta)\,\mathbb E[(R-\ell)_+]`, 'eq-small')}${defs('eta,Delta_eta')}</div></div>`,
      notes: 'Drag the weight and watch the sign of the comparative static change. Take a realised incumbent value above the low challenger value. A winning high-value challenger pays a blend of that value and its own, with sensitivity to the rival equal to one minus the seller’s weight. A losing low-value challenger leaves the rival paying, with sensitivity equal to the weight. Competition widens the spread precisely when the first exceeds the second, so the effect is positive below one half, zero at one half and negative above it, and the readout draws that flip. Challenger profit still weakly falls everywhere. This is payment-stage comparative statics only: trading, preparation and welfare under bargaining are not solved. If asked: no entry reversal is claimed under bargaining, and the weight equal to one is excluded from the declared domain.',
      source: 'Proposition A.8; Section 6.2; equation (14); Figure 4.'
    }),

    S('s19', {
      act: 'results',
      kicker: 'Proposition 3',
      title: 'Between the two economies, equilibria <i>coexist</i>.',
      subtitle: 'Three established nodes, certified intervals, and no path between them.',
      widget: 'coexist',
      status: 'computer-assisted',
      minutes: 3,
      defines: ['r_2'],
      body: `<div class="split wide"><div class="stack"><div class="plot-shell"><div id="coexist-plot"></div><p class="plot-caption">Preparation against incumbent strength; certified intervals at the declared benchmark.</p></div></div><div class="stack">${rev(3, `<p class="display">Push strength far enough and even the best feasible news cannot cover the <i>expensive</i> cost.</p>`)}${rev(3, m(String.raw`B_{r_2}(M)<c_H\quad\Longrightarrow\quad \mathsf E=\rho`, 'eq-small'))}${defs('r_2')}</div></div>`,
      notes: 'Three things in order. First the analytical nodes: the two economies plus the collapse strength. They are points, and I do not join them. Second the certified nodes, where interval arithmetic encloses exact informative equilibria with strictly ordered preparation, each coexisting with no trade at the same parameters, because against an uninformative price a unilateral order cannot cover its cost. Third the collapse: where even the upper posterior bound fails to justify the expensive cost, trading stays informative but preparation returns to the floor. Participation is therefore not monotone in strength. The intermediate correspondence is open; the searches return continuations found, and absence of a branch establishes nothing. If asked: which equilibrium and why? I select none. I report every branch I can certify and read no monotone path into the gaps.',
      source: 'Proposition 2, part (iii); Proposition 3; Figure 2; Section 4.3.'
    }),

    S('s20', {
      act: 'next',
      kicker: 'Robustness',
      title: 'The mechanism <i>survives</i> changes in primitives.',
      subtitle: 'Preparation in the weak and the strong economy, specification by specification.',
      widget: '',
      status: 'analytical',
      minutes: 1.5,
      body: `<table class="data-table"><thead><tr><th>Specification</th><th>Weak incumbent</th><th>Strong incumbent</th></tr></thead><tbody><tr><td>Laplace noise, atomic costs</td><td>${pct('base_entry_weak')}</td><td class="highlight">${pct('base_entry_strong')}</td></tr><tr><td>Logistic noise, atomic costs</td><td>${pct('base_entry_weak')}</td><td>${pct('logistic_entry_strong')}</td></tr><tr><td>Laplace noise, atomless costs</td><td>${pct('base_entry_weak')}</td><td>${pct('cost_mix_laplace_entry_strong')}</td></tr><tr><td>Moderate acquisition values</td><td>${pct('moderate_entry_weak')}</td><td>${pct('moderate_entry_strong')}</td></tr><tr><td>Complementary private signals</td><td>${pct('signal_entry_weak')}</td><td>${pct('signal_entry_strong')}</td></tr></tbody></table><p class="small muted">Each row is its own declared comparison at the declared benchmark, with its own sufficient conditions; levels are not comparable across rows.</p>`,
      notes: 'Take the rows as separate theorems rather than as a robustness sweep. Logistic noise has the same bounded log-density derivative, so the global trading bounds survive; what changes is where posterior mass sits, which is why the level differs. Narrow atomless cost supports preserve both the participation floor and the responsive expensive margin, so the cost atom is not doing the work. The moderate-value row removes the tenfold gap between acquisition values; what matters is where incumbent strength sits relative to the low value. The last row is the one that answers the obvious objection: the buyer there holds a more accurate private signal than the investor and the reversal still happens, because the signals are about different things. If asked: the moderate-value and private-signal rows use distinct parameter vectors, so this is not one joint calibration.',
      source: 'Propositions A.5, A.6 and A.7; Sections 5.1 to 5.3; Table 3.'
    }),

    S('s21', {
      act: 'next',
      kicker: 'What comes next',
      title: 'Evidence, and the <i>seller’s</i> problem.',
      subtitle: 'What I would have to build, and what the theory still owes.',
      widget: '',
      status: 'open',
      minutes: 1.5,
      body: `<div class="split"><div class="conditions"><div class="cond"><b>When</b><p class="job">Was the sale opportunity publicly visible, and from which date?</p></div><div class="cond reveal" data-step="1"><b>What</b><p class="job">When did costly preparation begin, rather than a public bid?</p></div><div class="cond reveal" data-step="2"><b>Why</b><p class="job">Could the price have changed that decision, rather than anticipated it?</p></div></div><div class="stack"><p class="kicker">The seller’s problem</p><p>Terms change both what a winner pays and what the price can reveal before anyone prepares.</p>${rev(3, '<p>Fixed-reserve comparisons with supported trading continuations establish feasible improvements.</p>')}${rev(4, '<p class="muted">The optimal reserve stays open: several continuations can share the same orders because the price-pooling rule differs, so an envelope of found revenues is not the seller’s solution.</p>')}</div></div>`,
      notes: 'Three empirical requirements in order of difficulty. A publicly understood sale opportunity that remains contestable while a buyer decides; a stock that merely trades during a confidential negotiation does not qualify, and the date an event occurred differs from the date it became public. An outcome closer to the model than counts of announced offers: the start of substantive diligence, or a proposal that required costly preparation. And separation of learning from prices from prices that already reflect anticipated bidder arrival. The Online Appendix proposes an institutional pilot that reconstructs those chronologies from disclosure records. It is a design only; no sample has been assembled and no identification strategy is reported. If asked: the welfare comparison behind the seller’s problem, and the matched-price diagnostic that separates level from content, are on the access backup slide.',
      source: 'Sections 6.3 and 7; Appendix A.7; Online Appendix C.6 and D.'
    }),

    S('s22', {
      act: 'next',
      kicker: '',
      title: 'Competition <i>creates</i> competition.',
      subtitle: '',
      widget: '',
      status: '',
      minutes: 0.5,
      body: `${rev(1, '<p class="endline">A stronger rival can make information worth <i>trading</i> on.</p>')}${rev(2, '<p class="endline">That information can make preparation worth <i>paying</i> for.</p>')}<div class="controls"><button data-goto="s14">The two claims</button><button data-goto="s15">Proposition 2</button><button data-goto="s17">The control</button><button data-goto="b1">Technical slides</button></div>`,
      notes: 'Two lines, then stop talking. The first is the trading margin, the second the participation margin, and the paper is the claim that the second can outweigh the direct deterrence force on an open set of primitives. Say plainly what the result is not: it is a sufficient-condition result resting on a participation floor and on a payment rule that loads weight on the runner-up, and it is a comparison between declared economies rather than an estimate of anything. Stay here for the discussion and use the buttons to jump back to the dial, the theorem or the information control. If asked: the sources, both PDFs and the provenance hashes are on the last backup slide.',
      source: 'Section 8; Competition Creates Competition: Stock Prices and the Discovery of Takeover Bidders.'
    }),

    S('b1', {
      act: 'backup',
      kicker: 'Global bounds',
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
      kicker: 'Why Laplace',
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
      kicker: 'Certificates',
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
      kicker: 'Access to prices',
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
      kicker: 'Reserve comparisons',
      title: 'Fixed-reserve comparisons with <i>supported</i> continuations.',
      subtitle: 'Preparation, a completed sale, and two admissible bidders are different events.',
      widget: 'reserve',
      status: 'numerical diagnostic',
      backup: true,
      body: `<div id="reserve-table"></div><p class="small muted">Per target share; the listed nodes have analytical support from the global trading bounds.</p>`,
      notes: 'The higher reserve excludes the low value class, which changes both the payment a winner makes and the gap in target proceeds across challenger types, and it can support informative trading even against a weak incumbent. That is why the table reports preparation, sale and two admissible bidders separately: once the reserve excludes bidders, a positive preparation probability is not evidence of more acquisition competition, and an excluded incumbent facing one possibly inadmissible challenger is not a two-bidder contest. To avoid making exclusion turn on a value atom, the second panel uses atomless value classes around the two levels. This demonstrates a feasible improvement over the original reserve, not an optimal one. If asked: the exploratory reserve summary is reported online with its unresolved counts, and I do not treat its maximum as the seller’s solution.',
      source: 'Section 6.3; Appendix A.7; Table 4; Online Appendix C.6.'
    }),

    S('b6', {
      act: 'backup',
      kicker: 'Notation',
      title: 'Every symbol in the <i>talk</i>.',
      subtitle: 'One definition, grouped by the role the symbol plays.',
      widget: 'glossary',
      status: '',
      backup: true,
      body: `<div id="glossary-table"></div>`,
      notes: 'This table is the same source as the definition strips on the model slides and the panel that opens with G, so a symbol is defined once and rendered in three places. Groups follow the structure of the model rather than the order of introduction: values and the sale rule, the preparation cost, trading, prices and beliefs, the derived objects that carry the mechanism, and the outcome measures reported in the tables. If a question turns on notation, open this rather than scrolling back, because every slide in the talk introduces its symbols where they first appear and none of them is reused with a second meaning. If asked: the transliterations here are the same column names used in the recorded numerical outputs, so the table and the data agree by construction.',
      source: 'Section 2; Online Appendix C.0 notation.'
    }),

    S('b7', {
      act: 'backup',
      kicker: 'Sources',
      title: 'Sources and research <i>boundaries</i>.',
      subtitle: 'The benchmark paper and its recorded numerical outputs.',
      widget: '',
      status: '',
      backup: true,
      body: `<div class="split"><div class="stack"><p><a href="main_filled.pdf" target="_blank" rel="noopener">The working paper</a></p><p><a href="online_appendix_filled.pdf" target="_blank" rel="noopener">The Online Appendix</a></p><p><a href="provenance.json" target="_blank" rel="noopener">Data-source hashes</a></p></div><div class="references"><p><strong>Auction entry</strong><br>Fishman (1988); Hirshleifer and Png (1989); Levin and Smith (1994); Gentry and Stroup (2019); Roberts and Sweeting (2013); Persico (2000).</p><p><strong>Prices and real decisions</strong><br>Dow, Goldstein and Guembel (2017); Edmans, Goldstein and Jiang (2015); Goldstein and Guembel (2008); Luo (2005).</p><p><strong>Takeover setting</strong><br>Boone and Mulherin (2007); Betton et al. (2014); Cornelli and Li (2002); Imprivata (2016).</p></div></div>`,
      notes: 'Everything numerical in this deck is bound to recorded outputs by hash; the presentation build reruns no solver and establishes no result of its own, and the interactive panels only evaluate existing closed forms. Results keep separate labels throughout: analytical, computer-assisted, numerical diagnostic and open, with declared parameters marked as declarations. The boundaries I would name without prompting are the participation floor, the dependence of the sign on the payment rule, the open intermediate correspondence, the unsolved seller problem, and the absence of any empirical sample. Both PDFs and the provenance file are local, so they open offline during discussion. If asked: the full bibliography and the contribution discussion are in the manuscript rather than on this slide.',
      source: 'paper/main.md; paper/online_appendix.md; quantity registry and passed run manifests.'
    })

  ];
};
