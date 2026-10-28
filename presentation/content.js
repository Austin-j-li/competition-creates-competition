/* content.js: the frames of slot/manuscript/slides.tex as web slides, in the Beamer order.
 *
 * This file is kept by hand. presentation/check_deck.mjs compares it with slides.tex on every
 * build: frame order, labels, titles, subtitles, hypertargets, the link graph, every registry key
 * that slides.tex prints with \reg{key}, and every rounded number it prints with \regr{key}{digits}.
 * Edit slides.tex first, then this file. The words of every frame are the slide text of
 * presentation/SLIDEPACK_45_VERBATIM.md, printed exactly.
 *
 * Contract. window.createDeck(H) returns { frames, glossary, notation }. H is supplied by the
 * renderer (presentation/render.mjs) or by the check, never by this file:
 *   H.m(latex)                 inline mathematics
 *   H.d(latex)                 display mathematics
 *                              In both, {{key}} prints the registry display of key inside the formula,
 *                              {{key|3}} the value rounded to three decimals, as \regr{key}{3} does;
 *                              \reg{key} does the same as {{key}} where a subtitle must read as in slides.tex.
 *   H.q(key[, digits])         a registry number in running text: the display that \reg{key} prints,
 *                              or with digits the rounded value that \regr{key}{digits} prints.
 *   H.v(key)                   the registry value as a number, for layout only (never before slide 16).
 *   H.go(target, text)         a link button to a \hypertarget name, as \hyperlink does.
 *   H.back(target)             the Back button of a backup frame.
 *   H.endFrame(label)          optional; called once per frame after its fields are built.
 * Frame record: { id, label, num, part, title, short, subtitle, targets, minutes, defines, widget,
 *   body, backup, origin, cls }. title is the slides.tex title argument verbatim; short names a frame
 *   without a title; cls adds a class to the slide. Reveals use data-step="n" on elements of the body.
 * Layout words: the takeaway is the bold ruled line at the foot of the body; the foot zone under it
 * holds citations, credits and scope limits in small type; a small line inside the body is small type.
 * ES2019, no modules, no DOM access.
 */
(function () {
  'use strict';
  var T = String.raw;

  function createDeck(H) {
    var m = H.m, d = H.d, q = H.q, go = H.go, back = H.back;
    /* the bold takeaway of a main slide; plain() is the unbolded takeaway that a reused backup keeps */
    var take = function (s, step) { return '<p class="takeaway"' + (step !== undefined ? ' data-step="' + step + '"' : '') + '><b>' + s + '</b></p>'; };
    var plainTake = function (s) { return '<p class="takeaway">' + s + '</p>'; };
    var foot = function () { return '<div class="footzone">' + Array.prototype.slice.call(arguments).map(function (s) { return '<p class="foot">' + s + '</p>'; }).join('') + '</div>'; };
    var smallLine = function (s, step) { return '<p class="smallline"' + (step !== undefined ? ' data-step="' + step + '"' : '') + '>' + s + '</p>'; };
    var gray = function (s) { return '<p class="grayline">' + s + '</p>'; };
    var nav = function () { return '<p class="nav">' + Array.prototype.slice.call(arguments).join(' ') + '</p>'; };
    var ul = function (items, cls) {
      return '<ul' + (cls ? ' class="' + cls + '"' : '') + '>' + items.map(function (it) {
        return typeof it === 'string' ? '<li>' + it + '</li>' : '<li data-step="' + it[0] + '">' + it[1] + '</li>';
      }).join('') + '</ul>';
    };
    var ol = function (items, cls) {
      return '<ol' + (cls ? ' class="' + cls + '"' : '') + '>' + items.map(function (it) {
        return typeof it === 'string' ? '<li>' + it + '</li>' : '<li data-step="' + it[0] + '">' + it[1] + '</li>';
      }).join('') + '</ol>';
    };
    /* a booktabs table: head cells, then rows of cells; a row may be { cls, cells } or { panel } */
    var table = function (cls, head, rows) {
      return '<table class="' + cls + '"><thead><tr>' + head.map(function (h) { return '<th>' + h + '</th>'; }).join('') + '</tr></thead><tbody>' +
        rows.map(function (r) {
          if (r.panel) return '<tr class="panel"><td colspan="' + head.length + '"><em>' + r.panel + '</em></td></tr>';
          var cells = r.cells || r, attr = (r.cls ? ' class="' + r.cls + '"' : '') + (r.row ? ' data-row="' + r.row + '"' : '');
          return '<tr' + attr + '>' + cells.map(function (c) { return '<td>' + c + '</td>'; }).join('') + '</tr>';
        }).join('') + '</tbody></table>';
    };
    var cols3 = function (a, b, c, steps) {
      steps = steps || [0, 0, 0];
      return '<div class="cols3">' + [a, b, c].map(function (x, i) { return '<div class="rcol" data-step="' + steps[i] + '">' + x + '</div>'; }).join('') + '</div>';
    };
    var b1 = function (target, n) { return go(target, 'Backup B' + n); };

    var F = [];
    /* Helpers run while the body is built, just before frame() is called; endFrame lets the
       renderer attribute what it recorded to this frame. */
    function frame(o) { if (H.endFrame) H.endFrame(o.label); if (o.subtitle === undefined) o.subtitle = ''; F.push(o); }

    /* ================================================================ Part I. Why the question matters */

    frame({ id: 'f0', label: 'S0', num: '0', part: 1, minutes: 0.5, targets: [], defines: [], widget: 'title', short: 'Title',
      title: 'Competition Creates Competition: Stock Prices and the Discovery of Takeover Bidders', subtitle: '',
      body: '<div class="cover"><h1>Competition Creates Competition:<br>Stock Prices and the Discovery of Takeover Bidders</h1>' +
        '<p class="cover-author">Austin Li · Department of Economics, University College London</p>' +
        '<p class="hint">→ or Space to advance · O overview · N notes · G notation · ? help</p></div>' });

    frame({ id: 's1', label: 'S1', num: '1', part: 1, minutes: 2, targets: [], defines: [], widget: '', cls: 'bigtitle',
      title: 'Does a stronger bidder in a merger auction always deter others from entering?', subtitle: 'Why the answer matters',
      body:
        cols3('<b>Sellers must find the second buyer.</b> A public sale tries to discover one more buyer. Does a visible strong buyer help the search, or end the search?',
          '<b>Buyers pay before they know.</b> Diligence costs money before any offer exists. Does a strong rival kill the case for diligence, or make the market signal worth more?',
          '<b>Prices move before bids move.</b> Early price action may cause the second bid. The price may not only forecast the bid.', [0, 1, 2]) +
        foot('One more bidder carries first-order value in Bulow and Klemperer (1996). This paper holds the sale rule fixed and studies entry into the sale.') });

    frame({ id: 's2', label: 'S2', num: '2', part: 1, minutes: 2, targets: ['main:s2'], defines: [], widget: '',
      title: 'The received answer: a stronger rival pays less for your diligence', subtitle: 'Deterrence at fixed information',
      body:
        ul([[0, 'A buyer pays to check the books before it can bid.'],
          [1, 'A stronger first buyer raises the price a winning second buyer must pay.'],
          [2, 'The same diligence then earns less. Fewer buyers prepare.']], 'roomy') +
        take('The logic holds when what the buyer knows stays fixed.', 3) +
        foot('Fishman (1988); Hirshleifer and Png (1989). Auction entry: Samuelson (1985); McAfee and McMillan (1987); Levin and Smith (1994); Gentry and Stroup (2019).',
          'In Fishman, the first buyer chooses a preemptive bid. Below, strength is a public type, not a chosen bid.') +
        nav(b1('app:b1', 1)) });

    frame({ id: 's3', label: 'S3', num: '3', part: 1, minutes: 2, targets: [], defines: [], widget: '',
      title: 'Three literatures each hold one piece fixed', subtitle: 'What each strand keeps, and what each strand misses',
      body:
        table('t-lit3', ['Strand', 'Closest work', 'Keeps', 'Misses here'], [
          ['Costly entry into auctions', 'Fishman (1988); Roberts and Sweeting (2013)', 'Costly preparation and selective entry', 'A market before preparation'],
          ['Prices guide real decisions', '<b>Dow, Goldstein and Guembel (2017)</b>; Edmans, Goldstein and Jiang (2015)', 'A price that changes a real choice', 'Entry under a sale rule that splits surplus'],
          ['Informed trade around takeovers', 'Kyle and Vila (1991); Luo (2005)', 'Informed orders and price learning', 'An outside trader before entry, with no stake']]) +
        take('Each strand freezes the object that moves in this paper.', 1) +
        nav(b1('app:b1', 1)) });

    frame({ id: 's4', label: 'S4', num: '4', part: 1, minutes: 2, targets: [], defines: [], widget: '',
      title: 'This paper: strength can pay for the signal that brings the rival in', subtitle: 'Contribution and roadmap',
      body:
        '<p class="bigline"><b>A stronger first buyer taxes the second buyer’s profit and pays for information about that buyer. Entry rises when the information payment beats the tax.</b></p>' +
        '<p class="formal" data-step="1">Keep deterrence at each belief. Add a market before preparation. The outside trader holds the claim that gains what the entrant loses.</p>' +
        cols3('<b>Weak rival:</b> flat price, entry at its floor.', '<b>Strong rival:</b> live price, entry above its floor.',
          '<b>Very strong rival:</b> live price, entry back at its floor.', [2, 2, 2]) +
        '<p class="roadmap">Model → Mechanism → Main result and control → Path and research → Scope and tests</p>' });

    /* ================================================================ Part II. Model */

    frame({ id: 's5', label: 'S5', num: '5', part: 2, minutes: 1.5, targets: [], defines: ['p'], widget: '',
      title: 'One buyer is ready. One buyer still decides.', subtitle: 'The decision interval · Paper §2.1',
      body:
        '<div class="flow flow-3">' +
          '<div class="box">Sale is public; one buyer is ready</div><span class="arrow" aria-hidden="true">→</span>' +
          '<div class="box">Target stock still trades</div><span class="arrow" aria-hidden="true">→</span>' +
          '<div class="box box-cost">Second buyer decides — pay for diligence, or stay out</div>' +
        '</div>' +
        '<p class="ruled-line">Cash second-price auction with reserve ' + m('p>0') + ', committed before trade. Highest admissible bid wins and pays ' +
          m(T`\max\{p,\ \text{highest rival bid}\}`) + '. No sale without an admissible bid.</p>' +
        foot('Disclosure records show this window: Imprivata (2016); Boone and Mulherin (2007); Gentry and Stroup (2019).') });

    frame({ id: 's6', label: 'S6', num: '6', part: 2, minutes: 2, targets: ['main:s6'],
      defines: ['R', 'F', 'r', 'class', 'pi', 'theta', 'C', 'rho', 'c_H', 'y', 'D'], widget: '',
      title: 'Who draws what, and who sees it', subtitle: 'Values, classes, costs · Paper §2.2',
      body:
        table('t-inv', ['Object', 'Law', 'Who learns it, and when'], [
          ['First buyer value ' + m('R'), 'Continuous ' + m('F') + ' on ' + m(T`[0,\bar r]`), 'First buyer before bids; ' + m('F') + ' itself is public'],
          ['Fit class ' + m(T`j\in\{H,L\}`), 'Prior ' + m(T`\pi=\Pr(H)\in(0,1)`), 'Specialist investor before trade; no one else'],
          ['Second buyer value ' + m(T`\theta`), m('G_j') + ' given class, finite mean, atoms allowed', 'Second buyer only after it pays ' + m('C')],
          ['Diligence bill ' + m('C'), m('0') + ' with chance ' + m(T`\rho\in(0,1)`) + '; else ' + m('c_H>0'), 'Second buyer after the price']]) +
        ul(['Class ranking: ' + m(T`G_H(y)\le G_L(y)`) + ' for every ' + m('y') + ', and ' + m(T`G_H(p^-)=G_L(p^-)=0`) + '. In words: ' + m('H') + ' first-order dominates ' + m('L') + ', and every value clears the reserve.',
          'The pair ' + m(T`(j,\theta)`) + ', the value ' + m('R') + ', the bill ' + m('C') + ', and the slot draws are mutually independent. The bill carries no news about fit.',
          'A strength path ' + m(T`\{F_r\}`) + ' orders distributions by first-order dominance. Higher ' + m('r') + ' means a stronger first buyer, with all else fixed.'], 'small') +
        smallLine('Write ' + m(T`D(y)=G_L(y)-G_H(y)`) + ' for the class gap at value ' + m('y') + '.') +
        foot('Strength as a public distribution follows type-based valuation differences in Gorbenko and Malenko (2014). Class-indexed values with costly revelation follow selective entry in Roberts and Sweeting (2013).') +
        nav(b1('app:b2', 2)) });

    frame({ id: 's7', label: 'S7', num: '7', part: 2, minutes: 2, targets: ['main:s7'],
      defines: ['lambda', 'q', 'k', 'beta', 'X', 'P', 'V_T', 'b', 'u'], widget: '',
      title: 'One trade happens before the diligence decision', subtitle: 'The order slot · Paper §2.3',
      body:
        '<div class="slotflow">' +
          '<div class="slotsrc">' +
            '<div class="sbox"><b>Specialist investor</b> — fills the slot with probability ' + m(T`\lambda`) + '; sees class ' + m('j') + '; picks ' + m(T`q\in\{-1,0,1\}`) + '; a nonzero order costs ' + m('k>0') + '</div>' +
            '<div class="sbox"><b>Liquidity trader</b> — fills the slot with probability ' + m(T`1-\lambda`) + '; sells, does nothing, or buys with chances ' + m(T`\beta,\ 1-2\beta,\ \beta`) + ', where ' + m(T`0<\beta\le 1/3`) + '</div>' +
          '</div>' +
          '<span class="arrow" aria-hidden="true">→</span>' +
          '<div class="sbox slotbox"><b>Order slot</b> — one public order ' + m(T`X\in\{-1,0,1\}`) + '; no observer sees who filled it</div>' +
          '<span class="arrow" aria-hidden="true">→</span>' +
          '<div class="sbox makerbox"><b>Market makers</b> — see ' + m('X') + ' only; set ' + m(T`P=\mathbb{E}[V_T\mid X]`) + ', where ' + m('V_T') + ' is the sale proceeds per share</div>' +
          '<span class="arrow" aria-hidden="true">→</span>' +
          '<div class="sbox sbox-cost"><b>Second buyer</b> — sees the price ' + m('P') + ' and bill ' + m('C') + '; sees neither ' + m('X') + ' nor ' + m('j') + '</div>' +
        '</div>' +
        '<p class="ruled-line small">A liquidity order in one direction arrives with probability ' + m(T`b=(1-\lambda)\beta`) + '. Set ' + m(T`u=\lambda/b`) + '. The number ' + m('1+u') + ' caps the likelihood ratio of one order.</p>' +
        foot('Alternative arrival: Dow and Gorton (1997). Unit orders and unit cost: Edmans, Goldstein and Jiang (2015). Zero-profit pricing: Glosten and Milgrom (1985); Kyle (1985).') +
        nav(b1('app:b11', 11)) });

    frame({ id: 's8', label: 'S8', num: '8', part: 2, minutes: 2, targets: [], defines: ['t_0', 'tj', 'gj', 'Delta_T', 'mu', 'B', 'W'], widget: '',
      title: 'The auction splits each value between shareholders and the buyer', subtitle: 'Payoff objects · Paper §2.4 and §3.1',
      body:
        '<p>Take a prepared second buyer with value ' + m(T`\theta\ge p`) + '. It pays ' + m(T`\max\{p,R\}`) + ' when it wins. The first buyer pays ' + m(T`\theta`) + ' when it wins.</p>' +
        d(T`t(\theta)=\max\{p,\min(R,\theta)\},\qquad g(\theta)=(\theta-\max\{p,R\})_+,\qquad t(\theta)+g(\theta)=\theta`) +
        ul(['Class means: ' + m(T`t_j=\mathbb{E}_j[t(\theta)]`) + ' and ' + m(T`g_j=\mathbb{E}_j[g(\theta)]`) + ' for ' + m(T`j\in\{H,L\}`) + '. Without entry, ' + m(T`t_0=p[1-F(p)]`) + '.',
          'Target-payoff spread: ' + m(T`\Delta_T=t_H-t_L`) + '. Read it as: how much more shareholders get with a good fit than with a poor fit.',
          'At belief ' + m(T`\mu=\Pr(H)`) + ', expected buyer profit is ' + m(T`B(\mu)=g_L+\mu(g_H-g_L)`) + '.',
          'Win chance: ' + m(T`W_j(F)=\mathbb{E}_j[F(\theta)\mathbf 1\{\theta\ge p\}]`) + '. Class ' + m('H') + ' outbids ' + m('F') + ' when ' + m('W_H(F)=1') + '.'], 'mid') +
        take('The traded claim and the entrant claim sum to the same value. Strength moves the split.', 1) });

    frame({ id: 's9', label: 'S9', num: '9', part: 2, minutes: 1.5, targets: ['main:s9'], defines: ['x', 'e', 'U', 'sfE', 'sfO'], widget: '',
      title: 'Equilibrium: orders, prices, beliefs, preparation, bids', subtitle: 'Definition · Paper §2.4',
      body:
        ol(['<b>Orders.</b> One distribution over ' + m(T`\{-1,0,1\}`) + ' for each class. Mixing and wrong-signed orders are allowed.',
          '<b>Beliefs and prices.</b> ' + m(T`\mu(x)=\Pr(H\mid X=x)`) + ' by Bayes’ rule. Every order can come from each class, so no off-path belief arises. Prices are competitive:' +
            d(T`P(x)=t_0+e(x)\,\bigl[t_L-t_0+\Delta_T\,\mu(x)\bigr]`),
          '<b>Preparation.</b> ' + m('e(x)') + ' is the chance the second buyer prepares after price ' + m('P(x)') + '. A zero bill always prepares. A bill ' + m('c_H') + ' prepares exactly at beliefs with ' + m(T`B(\mu)\ge c_H`) + '.',
          '<b>Investor choice.</b> Class ' + m('j') + ' picks ' + m('q') + ' to maximise ' + m(T`U_j(q)=q\,\bigl[t_0+e(q)(t_j-t_0)-P(q)\bigr]-k|q|`) + ' at the candidate prices and entry rule.',
          '<b>Bids.</b> Each prepared bidder with value at or above ' + m('p') + ' bids its value.'], 'defs') +
        smallLine('Default tie rules: an indifferent investor may mix over best orders; an indifferent buyer at bill ' + m('c_H') + ' prepares. Proposition 2 holds under all four tie-rule pairs.') +
        '<p class="ruled-line small">Entry ' + m(T`\mathsf{E}`) + ' = chance the second buyer prepares. Ownership ' + m(T`\mathsf{O}_H`) + ' = chance a good-fit second buyer wins. Takeover share = chance the winner is a good fit, given the second buyer wins.</p>' +
        '<p class="small">Strengthen ' + m('F') + '. Solve the equilibrium again in full. Nothing carries across economies except the primitives.</p>' +
        nav(b1('app:b3', 3)) });

    /* ================================================================ Part III. Mechanism */

    frame({ id: 's10', label: 'S10', num: '10', part: 3, minutes: 1.5, targets: [], defines: [], widget: 'cases',
      title: 'Win or lose, the second buyer sets what shareholders get', subtitle: 'Payment cases at each ' + m('R') + ' · Paper §3.1 · General',
      body:
        table('t-cases', ['First buyer value ' + m('R'), 'Good fit ' + m('H'), 'Poor fit ' + m('L'), 'Gap in target proceeds'], [
          { row: 'low', cells: [m('R') + ' low, at or below poor-fit values', 'Wins, pays ' + m(T`\max\{p,R\}`), 'Wins, pays ' + m(T`\max\{p,R\}`), 'None'] },
          { row: 'high', cells: [m('R') + ' high, above poor-fit values', 'May win, pays ' + m(T`\max\{p,R\}`), 'Loses; first buyer pays the poor-fit bid', '<b>Fit decides proceeds</b>'] }]) +
        '<p class="lead">Slice the fit gap at each value level ' + m('y>p') + '. The slice reaches shareholders when the first buyer outbids the second buyer at that level and pays its bid. The slice stays with the second buyer in the other case.</p>' +
        take('A stronger first buyer outbids at more levels. More slices reach shareholders.', 1) });

    frame({ id: 's11', label: 'S11', num: '11', part: 3, minutes: 2, targets: ['main:s11'], defines: [], widget: '',
      title: 'Strength takes from the buyer and gives to the signal', subtitle: 'Proposition 1 · Paper §3.1 · General result',
      body:
        '<div class="propblock">' + ol(['At each fixed belief, a stronger first buyer weakly lowers expected buyer profit ' + m(T`B(\mu)`) + '.',
          'Under the class ranking, a stronger first buyer weakly raises the shareholder spread ' + m(T`\Delta_T`) + '.'], 'props') + '</div>' +
        d(T`\Delta_T(F)+g_H(F)-g_L(F)=\mathbb{E}_H[\max\{\theta,p\}]-\mathbb{E}_L[\max\{\theta,p\}]`) +
        '<p>The right side does not depend on ' + m('F') + '. Strength leaves the fit gap the same size. Strength moves the gap between pockets.</p>' +
        take('Deterrence and informativeness come from the same shift. One force creates the other.', 1) +
        foot('Strict signs hold under the overlap conditions in Proposition 1. Detail: Backup B5.') +
        nav(b1('app:b5', 5)) });

    frame({ id: 's12', label: 'S12', num: '12', part: 3, minutes: 2, targets: [], defines: ['m_M', 'tau'], widget: '',
      title: 'One order can point. It cannot prove.', subtitle: 'Belief band and threshold · Paper §3.2 and §3.4 · General',
      body:
        d(T`m(\pi)=\frac{\pi}{\pi+(1-\pi)(1+u)}\ \le\ \mu\ \le\ \frac{\pi(1+u)}{\pi(1+u)+1-\pi}=M(\pi)\quad \text{after every order, under every strategy}`) +
        /* the band of beliefs one order can produce; schematic positions, no numbers */
        '<div class="beliefbar" aria-hidden="true"><div class="track"><div class="band" style="left:28%;width:44%"></div>' +
          '<span class="tick" style="left:28%"></span><span class="tick" style="left:50%"></span><span class="tick" style="left:72%"></span></div>' +
          '<div class="scale"><span style="left:28%">' + m(T`m(\pi)`) + '</span><span style="left:50%">' + m(T`\pi`) + '</span><span style="left:72%">' + m(T`M(\pi)`) + '</span></div></div>' +
        ul(['Price reads belief off. With entry at least ' + m(T`\rho`) + ' and ' + m(T`\Delta_T>0`) + ', the price rises strictly in ' + m(T`\mu`) + '. The second buyer recovers ' + m(T`\mu`) + ' from ' + m('P') + '.',
          'Threshold ' + m(T`\tau=(c_H-g_L)/(g_H-g_L)`) + ', when ' + m('g_H>g_L') + '. A bill ' + m('c_H') + ' pays exactly when ' + m(T`\mu\ge\tau`) + '.',
          'Exclusion bound: once ' + m(T`B(M(\pi))<c_H`) + ', no order recruits a buyer at bill ' + m('c_H') + ', in equilibrium or out of equilibrium.',
          'Two-numbers rule: when ' + m(T`\Delta_T>0`) + ' and ' + m('g_H>g_L') + ', orders, beliefs, and preparation depend on the auction only through ' + m(T`\Delta_T`) + ' and ' + m(T`\tau`) + '.'], 'small') +
        take('The best signal in this market stops at ' + m(T`M(\pi)`) + '. Recruitment lives or dies at that cap.', 1) +
        foot('The two-numbers rule holds with all other primitives and tie rules fixed. Price levels also need ' + m('t_0') + ' and ' + m('t_L') + '. Ownership also needs ' + m('W_H') + '.') });

    frame({ id: 's13', label: 'S13', num: '13', part: 3, minutes: 1.5, targets: [], defines: ['K', 'kappa'], widget: 'gain',
      title: 'A correct order keeps a slice the price cannot take', subtitle: 'Trading bounds · Paper §3.3 · General',
      body:
        d(T`K_H=e(1)\,\Delta_T\,[1-\mu(1)],\qquad K_L=e(-1)\,\Delta_T\,\mu(-1)`) +
        d(T`\rho\,\kappa(\pi)\,\Delta_T\ \le\ K_H,\,K_L\ \le\ \Delta_T,\qquad \kappa(\pi)=\min\{m(\pi),\,1-M(\pi)\}`) +
        '<div class="split gainsplit">' +
          '<div class="col">' +
            ul(['Read the gain as: entry chance ' + m(T`\times`) + ' shareholder spread ' + m(T`\times`) + ' doubt the price leaves behind.',
              'Rational pricing charges for expected entry. The band leaves residual doubt. The zero-bill floor ' + m(T`\rho`) + ' turns doubt into a floor on gain.',
              'A wrong-signed order never pays. Each class trades exactly when its correct-order gain beats ' + m('k') + '.'], 'small') +
          '</div>' +
          '<div class="col"><div class="figure nolegend" id="gain" tabindex="0" aria-label="Figure. The ceiling and the floor of the gain of a correct order against strength, and the order cost k, on a log scale; symbols only."></div></div>' +
        '</div>' +
        take('Compare each bound with ' + m('k') + '. Ceiling below ' + m('k') + ': no trade. Floor above ' + m('k') + ': full orders.', 1) +
        foot('Both bounds hold under every candidate profile, pure or mixed.') });

    /* ================================================================ Part IV. Main result */

    frame({ id: 's14', label: 'S14', num: '14', part: 4, minutes: 2, targets: ['main:s14'], defines: ['F_012', 'Delta_n', 'e_HL'], widget: '',
      title: 'A stronger first buyer can bring the second buyer in', subtitle: 'Proposition 2 · Paper §4.1 · General result',
      body:
        table('t-prop2', ['', 'Weak ' + m('F_0'), 'Strong ' + m('F_1'), 'Very strong ' + m('F_2')], [
          ['Fund orders', 'None', 'Buys on good fit; sells on poor fit', 'Buys on good fit; sells on poor fit'],
          ['Beliefs after sale, no order, purchase', m(T`\pi,\ \pi,\ \pi`), m(T`m(\pi),\ \pi,\ M(\pi)`), m(T`m(\pi),\ \pi,\ M(\pi)`)],
          ['Price', 'One price; no news', m(T`P(-1)<P(0)<P(1)`), 'Three prices; still news'],
          ['Entry', m(T`\rho`), '<b>' + m(T`\boldsymbol{\rho+(1-\rho)(b+\pi\lambda)>\rho}`) + '</b>', 'Back to ' + m(T`\rho`)]]) +
        ul(['(H1) ' + m(T`B_0(\pi)<c_H<B_1(M(\pi))`) + ' — profit at the prior falls short of the bill at ' + m('F_0') + '; profit at top news covers the bill at ' + m('F_1') + '.',
          '(H2) ' + m(T`\Delta_0<k<\rho\kappa(\pi)\Delta_1`) + ' — trade cannot pay at ' + m('F_0') + ' and must pay at ' + m('F_1') + '.',
          '(H3) ' + m(T`B_2(M(\pi))<c_H`) + ' — even top news cannot pay the bill at ' + m('F_2') + '.'], 'conds') +
        '<div class="result-lines">' +
          '<p>Classes meet the ranking. ' + m('F_1') + ' first-order strengthens ' + m('F_0') + '. ' + m('F_2') + ' first-order strengthens ' + m('F_1') + '. All other primitives stay fixed.</p>' +
          '<p>Each outcome is unique under all four tie-rule pairs. Conditions (H1)–(H3) hold together on an open set.</p>' +
          '<p>Good-fit ownership rises exactly when ' + m(T`e_HW_H(F_1)>\rho W_H(F_0)`) + ', where ' + m(T`e_H=\rho+(1-\rho)(b+\lambda)`) + '. Ownership rises for sure when ' + m('W_H(F_1)=1') + '.</p>' +
        '</div>' +
        take('Entry rises, then returns. The price stays live after entry dies.', 1) +
        nav(b1('app:b6', 6)) });

    function pstep(n, src, text) {
      return '<div class="pbox"><span class="ptag"><b>' + n + '</b>Slide ' + src + '</span>' + text + '</div>';
    }
    frame({ id: 's15', label: 'S15', num: '15', part: 4, minutes: 1.5, targets: [], defines: [], widget: '',
      title: 'The bounds settle each economy before any guess', subtitle: 'Proof map for Proposition 2 · Paper §4.1',
      body:
        '<div class="proofmap">' +
          pstep(1, 13, 'At ' + m('F_0') + ', (H2) gives ' + m(T`\Delta_0<k`) + '. By the trading bound, each correct order earns less than ' + m('k') + ' under every profile. No trade survives.') +
          '<span class="arrow" aria-hidden="true">→</span>' +
          pstep(2, 13, 'At ' + m('F_1') + ', (H2) gives ' + m(T`\rho\kappa(\pi)\Delta_1>k`) + '. By the trading bound, each correct order earns more than ' + m('k') + ' under every profile. Full orders survive alone.') +
          '<span class="arrow" aria-hidden="true">→</span>' +
          pstep(3, 12, 'Full orders at ' + m('F_1') + ' give belief ' + m(T`M(\pi)`) + ' after a purchase. By (H1), ' + m(T`B_1(M(\pi))>c_H`) + '. A purchase pays the bill. Other orders do not reach ' + m(T`M(\pi)`) + '.') +
          '<span class="arrow" aria-hidden="true">→</span>' +
          pstep(4, 12, 'At ' + m('F_2') + ', trade stays full by the same bound logic. By (H3) and the exclusion bound, ' + m(T`B_2(M(\pi))<c_H`) + '. No order pays the high bill. Entry returns to ' + m(T`\rho`) + '.') +
        '</div>' +
        take('Each step binds for every profile. That is why each outcome stands alone.', 1) +
        nav(b1('app:b6', 6)) });

    frame({ id: 's16', label: 'S16', num: '16', part: 4, minutes: 1.5, targets: ['main:s16'], defines: ['h', 'ell', 'r_01', 'r_2', 'r_C'], widget: 'beliefs',
      title: 'In the example, only a purchase clears the bar', subtitle: 'Illustration of Proposition 2 · Paper §4.2, Corollary 1 · Example only',
      body:
        '<div class="split beliefsplit">' +
          '<div class="col">' +
            '<div class="figure nolegend" id="beliefs" tabindex="0" aria-label="Figure. The threshold belief against strength, with the band of beliefs one order can produce; arrow keys move the cursor."></div>' +
            '<div class="slider"><label for="beliefs-r">' + m('r') + '</label><input type="range" id="beliefs-r" min="0" max="240" step="1" value="180"><output id="beliefs-r-value" for="beliefs-r">3.00</output></div>' +
          '</div>' +
          '<div class="col text">' +
            '<p class="caption">Threshold ' + m(T`\tau(r)`) + ' against strength ' + m('r') + '. Grey band: beliefs one order can produce, from ' + m(T`m({{prim_pi}})`) + ' to ' + m(T`M({{prim_pi}})`) + '.</p>' +
            ul(['Prior ' + m(T`{{prim_pi}}`) + ' stays below ' + m(T`\tau(r)`) + ' at each strength. A flat price never pays the high bill.',
              'Top signal ' + m(T`M({{prim_pi}})={{M_half_B}}`) + ' clears ' + m(T`\tau(r_1)={{tau_r1}}`) + ' at the strong incumbent.',
              'Curves meet at the entry ceiling ' + m(T`r_C\approx{{rC_B|3}}`) + ', just below ' + m(T`r_2={{prim_r2}}`) + '. Past ' + m('r_C') + ', no signal pays the bill.'], 'small') +
          '</div>' +
        '</div>' +
        take('The figure draws (H1) and (H3). The example proves nothing.', 1) +
        foot('Example inputs: ' + m(T`h={{prim_h}}`) + ', ' + m(T`\ell={{prim_ell}}`) + ', ' + m(T`\pi={{prim_pi}}`) + ', ' + m(T`p={{prim_p}}`) + ', ' + m(T`\rho={{prim_rho}}`) + ', ' + m(T`c_H={{prim_cH}}`) + ', ' + m(T`k={{prim_k}}`) +
          '; uniform ' + m('R') + ' on ' + m('[0,r]') + '; ' + m(T`r_0={{prim_r0}}`) + ', ' + m(T`r_1={{prim_r1}}`) + ', ' + m(T`r_2={{prim_r2}}`) + '. Full inputs and region: Backup B4.') +
        nav(b1('app:b4', 4)) });

    frame({ id: 's17', label: 'S17', num: '17', part: 4, minutes: 1.5, targets: [], defines: [], widget: '',
      title: 'In the example, entry rises while buyer profit falls', subtitle: 'Illustration of Proposition 2 · Paper §4.2, Corollary 1 · Example only',
      body:
        table('t-out', ['', 'Weak ' + m(T`r_0={{prim_r0}}`), 'Strong ' + m(T`r_1={{prim_r1}}`), 'Very strong ' + m(T`r_2={{prim_r2}}`)], [
          ['Buyer keeps at prior, ' + m(T`B_r({{prim_pi}})`), q('Bprior_r0'), q('Bprior_r1_B'), q('Bprior_r2')],
          ['Shareholder spread, ' + m(T`\Delta_T(r)`), q('Delta_r0'), q('Delta_r1'), q('Delta_r2')],
          ['Fund orders (good fit, poor fit)', m(T`(0,\ 0)`), m(T`(1,\ {-1})`), m(T`(1,\ {-1})`)],
          ['Price', 'Flat', 'Informative', 'Informative'],
          ['Entry', q('entry_r0'), '<b>' + q('entry_r1_B') + '</b>', q('entry_r2')],
          ['Good-fit ownership', q('own_r0'), '<b>' + q('own_r1_B') + '</b>', q('own_r2_B')]]) +
        take('Profit falls at each step. The signal value rises. Entry follows the signal, then hits its cap.', 1) +
        foot('(H1)–(H3) hold exactly when the top signal sits between the two bars: ' + m(T`\tau(r_1)<M({{prim_pi}})<\tau(r_2)`) + '. Region and margins: Backup B4. Full payoff and outcome tables: Backup B6.') +
        nav(b1('app:b4', 4), b1('app:b6', 6)) });

    frame({ id: 's18', label: 'S18', num: '18', part: 4, minutes: 2, targets: [], defines: [], widget: 'controls',
      title: 'Freeze the news, and strength only scares buyers off', subtitle: 'Fixed-information control · Paper §4.2 and Proposition A.2 · General',
      body:
        '<div class="propblock theorem">' +
          '<p>Fix the law of class and signal, the class value laws, and the cost law. A stronger first buyer can only lower entry.</p>' +
          '<p>Entry falls by exactly the chance that the bill sits between buyer profit at the two strengths.</p>' +
        '</div>' +
        '<div class="split wide">' +
          table('t-controls', ['Entry', 'Weak ' + m('r_0'), 'Strong ' + m('r_1')], [
            { row: 'eq', cells: ['Full model, orders re-solved', q('entry_r0'), '<b>' + q('entry_r1_B') + '</b>'] },
            { row: 'frozen', cells: ['Full orders held fixed at each strength', q('p4_frozen_r0_entry'), q('p4_frozen_r1_entry')] },
            { row: 'hidden', cells: ['Second buyer cannot see the price', q('p4_hidden_r0_entry'), q('p4_hidden_r1_entry')] }]) +
          '<div class="bars" id="f11-bars" aria-live="polite"></div>' +
        '</div>' +
        smallLine('Row 2 at ' + m('r_0') + ' is a control, not an equilibrium. In the slot, fixed order laws give the same belief after each order at each strength.') +
        take('The rise needs the signal itself to change with strength. Frozen news gives flat entry, then a fall past the ceiling.', 1) +
        nav(b1('app:b6', 6)) });

    /* ================================================================ Part V. Path and research */

    frame({ id: 's19', label: 'S19', num: '19', part: 5, minutes: 1.5, targets: ['main:s19'], defines: [], widget: 'region',
      title: 'Quiet and loud markets can sit at the same strength', subtitle: 'Proposition 3 · Paper §4.3 · General result, default tie rules',
      body:
        '<div class="split regionsplit">' +
          '<div class="col"><div class="figure nolegend" id="region" tabindex="0" aria-label="Figure. The coexistence region in the plane of the spread and the threshold, with the path of the example; arrow keys move the cursor."></div></div>' +
          '<div class="col text">' +
            d(T`\pi<\tau\le M(\pi),\qquad \frac{k}{1-\tau}\ \le\ \Delta_T\ \le\ \frac{k}{\rho\max\{\pi,1-\pi\}}`) +
            ul(['Inside this region, two markets coexist. Quiet market: no fund trade, one price, entry ' + m(T`\rho`) + '. Loud market: only a purchase recruits, and entry is' +
                d(T`\rho+(1-\rho)\min\Bigl\{\frac{(1-\pi)\,b\,\Delta_T}{k},\ b+\pi\lambda\Bigr\}`),
              'Entry in the loud market rises strictly with ' + m(T`\Delta_T`) + ' while the good-fit fund mixes. Entry stays flat once the good-fit fund buys for sure. The loud market is unique inside the region.',
              'Self-confirming logic, market by market. Expect no recruitment: one order earns at most the floor return, so silence pays. Expect recruitment: a purchase lifts entry, so trade pays.'], 'small') +
          '</div>' +
        '</div>' +
        smallLine('Scope: class ranking, ' + m(T`\Delta_T>0`) + ', ' + m('g_H>g_L') + ', default tie rules. In general, strengths with coexistence need not form one interval. Interval results: Backup B7.') +
        take('Between the Proposition 2 economies, the market can sit in either mood at one strength.', 1) +
        nav(b1('app:b7', 7)) });

    frame({ id: 's20', label: 'S20', num: '20', part: 5, minutes: 1.5, targets: [], defines: ['r_AFNJS'], widget: 'coex',
      title: 'In the example, both markets live between $r_A$ and $r_N$', subtitle: 'Illustration of Proposition 3 · Paper §4.3, Corollary 2 · Example only',
      body:
        '<div class="figure wide nolegend" id="coex" tabindex="0" aria-label="Figure. Entry against strength in each equilibrium of the example, with the coexistence band; arrow keys move the cursor."></div>' +
        '<p class="caption">Entry against strength ' + m('r') + '. Shaded band: coexistence interval ' + m('[r_A,r_N]') + '.</p>' +
        ul(['Loud entry starts at ' + q('entry_rA_B') + ' when ' + m(T`r_A\approx{{rA|3}}`) + ' opens the band. Quiet entry stays at ' + q('entry_r0') + '.',
          'Loud entry rises to ' + q('entry_plateau_B') + ' at ' + m(T`r_F\approx{{rF_B|3}}`) + ', where the good-fit fund buys for sure. Loud entry then stays flat.',
          'The quiet market dies at ' + m(T`r_N\approx{{rN|3}}`) + '. Loud entry holds to ' + m('r_C') + ', then drops to its floor.'], 'small') +
        take('Along one path, entry can climb, sit flat, then fall — with a jump when the loud market opens.', 1) +
        foot('Full equilibrium list and marked strengths ' + m('r_J') + ', ' + m('r_S') + ': Backup B7.') +
        nav(b1('app:b7', 7)) });

    frame({ id: 's21', label: 'S21', num: '21', part: 5, minutes: 2, targets: ['main:s21'], defines: ['a_cap', 'mlam'], widget: '',
      title: 'Make the fund pay for its view, and strength buys more views', subtitle: 'Proposition 4 · Paper §5 · General result at prior ' + m('1/2'),
      body:
        '<div class="setup">' +
          '<p>One change only. Before it learns the class, the fund picks research ' + m(T`\lambda\in[0,\bar\lambda]`) + ' at cost ' + m(T`(a/2)\lambda^2`) + '. Success has chance ' + m(T`\lambda`) + ', reveals the class, and fills the slot. Failure hands the slot to liquidity.</p>' +
          '<p>More research adds fund orders and removes liquidity cover. The prior is ' + m('1/2') + ' throughout this block.</p>' +
        '</div>' +
        '<p class="definition">At research ' + m(T`\lambda`) + ', write ' + m(T`M_\lambda`) + ' for the top belief after a purchase. Recruitment intensity ' + m(T`\lambda_E(\tau)`) + ' solves ' + m(T`M_\lambda=\tau`) + ': a full purchase recruits exactly at or past this research level.</p>' +
        ul(['In the recruiting equilibrium, research ' + m(T`\min\{\lambda_R(\Delta_T),\bar\lambda\}`) + ' rises strictly with ' + m(T`\Delta_T`) + ' until the cap, then stays at the cap.',
          'Entry ' + m(T`\rho+(1-\rho)[\beta+(1/2-\beta)\lambda]`) + ' rises with research. Good-fit entry rises with research. Poor-fit entry falls.',
          'The recruiting equilibrium exists exactly when ' + m(T`\Delta_T>2k`) + ' and ' + m(T`\tau\le M_\lambda`) + ' at ' + m(T`\lambda=\min\{\lambda_R(\Delta_T),\bar\lambda\}`) + '.'], 'small') +
        smallLine('Research level ' + m(T`\lambda_R(\Delta_T)`) + ' solves ' + m(T`2a\lambda=\Delta_T m_\lambda-k`) + ' away from a paying sure sale. Full condition: Backup B8. Scope: default tie rules, ' + m(T`\tau>1/2`) + '.') +
        take('A wider spread pays for more digging. More digging brings more good-fit buyers in.', 1) +
        nav(b1('app:b8', 8)) });

    frame({ id: 's22', label: 'S22', num: '22', part: 5, minutes: 1.5, targets: [], defines: ['r_R'], widget: 'research',
      title: 'In the example, research and entry climb together', subtitle: 'Illustration of Proposition 4 · Paper §5, research corollary · Example only',
      body:
        '<div class="figure wide nolegend" id="research" tabindex="0" aria-label="Figure. Research and entry against strength in each research equilibrium of the example; arrow keys move the cursor."></div>' +
        '<p class="caption">Research ' + m(T`\lambda`) + ' and entry against strength ' + m('r') + '. Research cost ' + m(T`a={{res_a}}`) + '. Cap ' + m(T`\bar\lambda={{res_cap}}`) + '.</p>' +
        ul(['Recruiting research opens at ' + m(T`r_R\approx{{res_rR|3}}`) + '. Entry there is ' + q('res_entry_rR') + '.',
          'Research reaches the cap at ' + m(T`r_{\bar\lambda}\approx{{res_rcap|3}}`) + '. Entry reaches ' + q('res_entry_cap') + ' and holds to ' + m('r_C') + '.',
          'Zero research coexists on ' + m('[r_0,r_N]') + '. At ' + m('r_1') + ' and ' + m('r_2') + ' the sole outcome sits at the cap and matches Proposition 2.'], 'small') +
        take('At the cap, the research economy is the Proposition 2 economy. One model, one dial.', 1) +
        foot('Floor-entry research branch, cap region, and three-strength table: Backup B8.') +
        nav(b1('app:b8', 8)) });

    /* ================================================================ Part VI. Scope, money, tests */

    frame({ id: 's23', label: 'S23', num: '23', part: 6, minutes: 1.5, targets: ['main:s23'], defines: [], widget: '',
      title: 'The result does not rest on the example\'s shape', subtitle: 'Scope checks · Paper §6 · Each row keeps the slot and varies one part',
      body:
        table('t-scope', ['Change one part', 'Result'], [
          ['Any diligence-bill law', 'Low bills and high bills, with atoms or without atoms, inside the (H1) window keep the rise. A smooth high-bill group turns the ceiling drop into a ramp.'],
          ['Any ranked fit classes, any prior', 'Some strengths and bills always deliver the reversal. Point-mass fits are not the kind case.'],
          ['Many fit classes', 'The reversal holds under a separation condition. Without separation, one price can carry two fit mixes.'],
          ['Second buyer has its own signal', 'At prior ' + m('1/2') + ', the rise can hold when the buyer’s signal beats the fund’s signal. In the stated signal example, entry needs both signals.']]) +
        take('The slot carries the mechanism. The shapes around the slot can change.', 1) +
        foot('Formal statements and the six-economy table: Backup B9. Continuous order sizes: Backup B11.') +
        nav(b1('app:b9', 9), b1('app:b11', 11)) });

    frame({ id: 's24', label: 'S24', num: '24', part: 6, minutes: 1.5, targets: ['main:s24'], defines: ['omega'], widget: '',
      title: 'Let the buyer see the price, and shareholders gain', subtitle: 'Price access and sale terms · Paper §7',
      body:
        '<div class="split accesssplit">' +
          '<div class="col">' +
            '<p class="small">At the strong incumbent ' + m('F_1') + ', under (H1)–(H3), price access raises expected target proceeds and surplus net of diligence bills.</p>' +
            '<p class="small">Why: fund orders stay full when the price hides, so trading cost matches in both worlds. Access adds only diligence where profit covers the bill.</p>' +
          '</div>' +
          '<div class="col">' +
            table('t-access2', ['', 'Expected target proceeds', 'Surplus net of preparation costs'], [
              ['Price seen', q('p2_base_r1_proceeds'), q('p2_base_r1_surplus')],
              ['Price hidden', q('p2_base_hidden_proceeds'), q('p2_base_hidden_surplus')]]) +
          '</div>' +
        '</div>' +
        smallLine('Scope: inside the recruitment region, where the high bill does not pay at the prior. Outside that region, a live price can deter diligence after a sale. Detail: Backup B10.') +
        '<p class="ruled-line small"><b>Payment rule (separate bargaining set-up).</b> Competition moves the spread with the sign of ' + m(T`1-2\omega`) + ', where ' + m(T`\omega`) + ' is seller bargaining weight. Second price is ' + m(T`\omega=0`) + ': full weight on the runner-up bid.</p>' +
        '<p class="small"><b>Reserve.</b> A reserve that excludes the poor fit can make the price live at both strengths. Entry then sits flat in strength. Strict deterrence needs still more.</p>' +
        take('Sale terms set two prices at once: the price to win, and the price that speaks before entry.', 1) +
        nav(b1('app:b10', 10)) });

    /* The three price levels: the purchase impact sits above P(0), the sale impact below. Positions are schematic. */
    function brace(x0, x1, y0, y1) {
      var xm = (x0 + x1) / 2, ym = (y0 + y1) / 2, r = Math.min((x1 - x0) / 2, (y1 - y0) / 4);
      return 'M' + x1 + ',' + y0 + ' Q' + xm + ',' + y0 + ' ' + xm + ',' + (y0 + r) + ' L' + xm + ',' + (ym - r) + ' Q' + xm + ',' + ym + ' ' + x0 + ',' + ym +
        ' Q' + xm + ',' + ym + ' ' + xm + ',' + (ym + r) + ' L' + xm + ',' + (y1 - r) + ' Q' + xm + ',' + y1 + ' ' + x1 + ',' + y1;
    }
    var impact = '<div class="impact" aria-label="Three price levels P(−1), P(0) and P(1); the purchase impact above P(0) is larger than the sale impact below it.">' +
      '<svg viewBox="0 0 40 320" width="40" height="320" aria-hidden="true">' +
        '<path class="brace info" d="' + brace(6, 34, 24, 196) + '"/>' +
        '<path class="brace muted" d="' + brace(10, 34, 204, 296) + '"/>' +
      '</svg>' +
      '<div class="lvl" style="top:20px"><span class="lvl-line"></span>' + m('P(1)') + '</div>' +
      '<div class="lvl" style="top:200px"><span class="lvl-line"></span>' + m('P(0)') + '</div>' +
      '<div class="lvl" style="top:300px"><span class="lvl-line"></span>' + m('P(-1)') + '</div>' +
    '</div>';
    frame({ id: 's25', label: 'S25', num: '25', part: 6, minutes: 2, targets: ['main:s25'], defines: [], widget: '',
      title: 'A recruiting purchase moves the price more than a sale', subtitle: 'Predictions · Paper §8 · Full two-sided trade, prior below ' + m(T`\tau`),
      body:
        '<div class="split testsplit">' +
          '<div class="col">' +
            '<p class="small">Weight each price impact by how often its order occurs. Weighted purchase impact beats weighted sale impact exactly when a purchase recruits the second buyer.</p>' +
            ul(['At prior ' + m('1/2') + ', order frequencies match. Compare raw impacts: ' + m('P(1)-P(0)') + ' against ' + m('P(0)-P(-1)') + '.',
              'The price gap ' + m('P(1)-P(-1)') + ' splits into a class part, ' + m(T`\rho\Delta_T[M(\pi)-m(\pi)]`) + ', and an entry part. The entry part is positive exactly under recruitment, and it sits wholly in the purchase impact.'], 'xs') +
            ol(['Entry can rise with first-buyer strength only when the price lands before diligence starts. Hide the price, and entry can only fall.',
              'Past the entry ceiling, orders stop predicting entry. Orders keep predicting the winner.',
              'At prior ' + m('1/2') + ', order counts cannot separate slot types. Prices can.'], 'xs predictions') +
            '<p class="small"><b>Date the price before diligence starts. Record the zero order.</b></p>' +
          '</div>' +
          '<div class="col">' + impact + '</div>' +
        '</div>' +
        smallLine('In the example at ' + m('r_1') + ', the entry part is ' + q('ba_share_r1_B') + ' of the price gap. Fund-share and announcement detail: Backup B12.') +
        take('Test recruitment in prices first. The sharpest test needs no auction object.', 1) +
        nav(b1('app:b12', 12)) });

    frame({ id: 's26', label: 'S26', num: '26', part: 6, minutes: 0.5, targets: [], defines: [], widget: '',
      title: 'Competition can create competition', subtitle: 'Conclusion',
      body:
        ol([[0, 'A stronger first buyer taxes the second buyer’s profit.'],
          [1, 'The same strength pays for information about that buyer.'],
          [2, 'Entry follows the winner of that race.']], 'conclusion') +
        '<p class="chain" data-step="3">Wider spread → trade pays → live price → good news pays the bill → second buyer enters</p>' +
        '<p class="lastline" data-step="4">Next step: the seller picks sale terms with this whole chain live.</p>' });

    /* ================================================================ backup frames */

    function backup(o) { o.part = 'B'; o.minutes = 0; o.backup = true; o.num = o.label; o.defines = o.defines || []; o.widget = o.widget || ''; frame(o); }
    function tr3(a, b, c) { return [a, b, c]; }

    var REFS = [
      ['Admati and Pfleiderer (2009). <em>Rev. Financ. Stud.</em> 22.', 'Betton, Eckbo, Thompson and Thorburn (2014). <em>J. Finance</em> 69.', 'Bond, Edmans and Goldstein (2012). <em>Annu. Rev. Financ. Econ.</em> 4.',
        'Boone and Mulherin (2007). <em>J. Finance</em> 62.', 'Bulow and Klemperer (1996). <em>Amer. Econ. Rev.</em> 86.', 'Dow and Gorton (1997). <em>J. Finance</em> 52.',
        'Dow, Goldstein and Guembel (2017). <em>J. Eur. Econ. Assoc.</em> 15.', 'Edmans, Goldstein and Jiang (2012). <em>J. Finance</em> 67.'],
      ['Edmans, Goldstein and Jiang (2015). <em>Amer. Econ. Rev.</em> 105.', 'Fishman (1988). <em>RAND J. Econ.</em> 19.', 'Foucault and Frésard (2014). <em>J. Financ. Econ.</em> 111.',
        'Gorbenko and Malenko (2014). <em>J. Finance</em> 69.', 'Hirshleifer and Png (1989). <em>Rev. Financ. Stud.</em> 2.', 'Levin and Smith (1994). <em>Amer. Econ. Rev.</em> 84.',
        'Samuelson (1985). <em>Econ. Letters</em> 17.', 'Schwert (1996). <em>J. Finance</em> 51.']
    ];
    backup({ id: 'b1', label: 'B1', origin: 's2', targets: ['app:b1'], title: 'References', subtitle: '',
      body: '<div class="refs">' + REFS.map(function (col) { return '<ul>' + col.map(function (r) { return '<li>' + r + '</li>'; }).join('') + '</ul>'; }).join('') + '</div>' + nav(back('main:s2')) });

    backup({ id: 'b2', label: 'B2', origin: 's6', targets: ['app:b2'], widget: 'notation', defines: ['e_r', 'q_HL'], title: 'Notation', subtitle: '',
      body: '<div class="notation" id="notation-table"></div>' + nav(back('main:s6')) });

    backup({ id: 'b3', label: 'B3', origin: 's9', targets: ['app:b3'], title: 'Equilibrium in full: six conditions and tie rules', subtitle: '',
      body:
        ul(['<b>Tuple:</b> order laws for each class, a price for each order in ' + m(T`\{-1,0,1\}`) + ', beliefs at each price, the entry rule, the bids',
          '<b>Prices:</b> ' + m(T`P(X)=\mathbb{E}[V_T\mid X]`) + ' at each order, with entry at that price inside ' + m('V_T'),
          '<b>Beliefs:</b> Bayes rule from the order laws at each price. Every order is on path, so no off-path belief enters',
          '<b>Entry:</b> the zero cost always prepares; cost ' + m('c_H') + ' prepares exactly at prices with ' + m(T`B_r(\mu)\ge c_H`),
          '<b>Investor:</b> the order law puts weight only on best replies at the stated price and entry rules, net of cost ' + m('k'),
          '<b>Bids:</b> each bidder bids its value in the second-price auction',
          '<b>Tie rules:</b> a tied investor may mix; a tied cost ' + m('c_H') + ' type prepares. Proposition 2 holds under all four tie rules'], 'small') +
        '<p class="small">Proposition 2 holds under all four tie-rule pairs. Propositions 3 and 4 use the default tie rules.</p>' +
        nav(back('main:s9')) });

    backup({ id: 'b4', label: 'B4', origin: 's16', targets: ['app:b4'], title: 'The example: inputs, recruitment region, and margins', subtitle: '',
      body:
        '<div class="twotables">' +
          table('t-inputs2', ['Input', 'Value', 'Meaning'], [
            tr3(m(T`h`) + ', ' + m(T`\ell`), q('prim_h') + ', ' + q('prim_ell'), 'class ' + m('H') + ' and class ' + m('L') + ' values'),
            tr3(m('p'), q('prim_p'), 'reserve price'),
            tr3(m(T`\pi`) + ', ' + m(T`\rho`), q('prim_pi') + ', ' + q('prim_rho'), 'prior on ' + m('H') + '; probability of zero cost'),
            tr3('Costs ' + m('0') + ', ' + m('c_H') + ', ' + m('k'), m('0') + ', ' + q('prim_cH') + ', ' + q('prim_k'), 'preparation costs; cost of a nonzero order'),
            tr3(m(T`\beta`) + ', ' + m(T`\lambda`), q('beta_B') + ', ' + q('lambda_B'), 'liquidity order chance; informed presence chance'),
            tr3(m('u') + ', ' + m('b'), q('u_B') + ', ' + q('b_B'), 'mass ratio ' + m(T`u=\lambda/b`) + '; here ' + m(T`1+u=e`)),
            tr3(m(T`r_0,r_1,r_2`), q('prim_r0') + ', ' + q('prim_r1') + ', ' + q('prim_r2'), 'weak, strong, stronger still')]) +
          table('t-region', ['Object', 'Region', 'Example'], [
            tr3('Mass ratio ' + m('u') + ' (Corollary 1)', m(T`({{u_lo}},{{u_hi}})`), q('u_B')),
            tr3('Top posterior ' + m('M') + ' at prior ' + q('prim_pi'), m(T`({{M_lo}},{{M_hi}})`), q('M_half_B')),
            tr3('Liquidity chance ' + m(T`\beta`), m(T`0<\beta\le 1/3`), q('beta_B')),
            tr3('Presence chance ' + m(T`\lambda`) + ' at that ' + m(T`\beta`), 'from ' + m(T`u=\lambda/((1-\lambda)\beta)`), q('lambda_B')),
            tr3('Prior ' + m(T`\pi`) + ' for Proposition 2', m(T`({{prior_lo_B}},{{prior_hi_B}})`), q('prim_pi')),
            tr3('Research cost ' + m('a') + ' (Proposition A.1)', m(T`({{res_a_lo}},{{res_a_up}})`), q('res_a')),
            tr3('Research cap ' + m(T`\bar\lambda`), m(T`({{res_cap_lo}},{{res_cap_hi}})`), q('res_cap'))]) +
        '</div>' +
        gray('Each region is cut out by strict inequalities, so the results hold on an open set of inputs.') +
        nav(back('main:s16')) });

    backup({ id: 'b5', label: 'B5', origin: 's11', targets: ['app:b5'], title: 'Proposition 1 in full: forms, strict signs, equal admissibility', subtitle: '',
      body:
        ul([m(T`\Delta_T(F)=pF(p)D(p^-)+\int_p^\infty[1-F(y)]D(y)\,dy`) + ' and ' + m(T`g_j(F)=\int_p^\infty[1-G_j(y)]F(y)\,dy`) + '.',
          'Profit falls strictly exactly when ' + m(T`\int_p^\infty[1-G_j(y)][F(y)-\tilde F(y)]\,dy>0`) + '. Spread rises strictly exactly when ' + m(T`\int_p^\infty[F(y)-\tilde F(y)]D(y)\,dy>0`) + '.',
          'Without the class ranking, the reserve term ' + m(T`pF(p)D(p^-)`) + ' can reverse the spread sign. Equal admissibility is the exact fix.'], 'roomy') +
        nav(back('main:s11')) });

    backup({ id: 'b6', label: 'B6', origin: 's14', targets: ['app:b6'], title: 'Proposition 2 in full: tuples, payoff tables, control panels', subtitle: '',
      body:
        '<ol class="steps">' +
          '<li><b>Bounds for every profile:</b> posterior band ' + m(T`m\le\mu\le M`) + '; gain per unit at most ' + m(T`\Delta_T`) + '; entry at least ' + m(T`\rho`) + '</li>' +
          '<li><b>Weak ' + m('r_0') + ':</b> ' + m(T`\Delta_T(r_0)<k`) + ' makes each nonzero order lose in expectation. A quiet market is the sole outcome; entry is ' + m(T`\rho`) + '</li>' +
          '<li><b>Strong ' + m('r_1') + ':</b> ' + m(T`k<\rho\kappa\,\Delta_T(r_1)`) + ' makes each correct order pay under every profile; a wrong-signed order always loses. Orders are ' + m('(1,-1)') + '</li>' +
          '<li><b>Entry at ' + m('r_1') + ':</b> a buy order gives belief ' + m('M') + ' with ' + m(T`B_{r_1}(M)>c_H`) + ', so cost ' + m('c_H') + ' prepares after a buy order. Entry exceeds ' + m(T`\rho`) + '</li>' +
          '<li><b>Return at ' + m('r_2') + ':</b> trade still pays, but ' + m(T`B_{r_2}(M)<c_H`) + ' keeps cost ' + m('c_H') + ' out at every price. Entry is ' + m(T`\rho`) + '</li>' +
        '</ol>' +
        '<p class="small">Ownership: with ' + m(T`W_H(F)=\mathbb{E}_H[F(\theta)\mathbf{1}\{\theta\ge p\}]`) + ', class ' + m('H') + ' ownership rises exactly if ' + m(T`[\rho+(1-\rho)(b+\lambda)]W_H(F_1)>\rho W_H(F_0)`) + '.</p>' +
        '<p class="small">Share rises exactly when ' + m(T`e_HW_H(F_1)W_L(F_0)>e_LW_H(F_0)W_L(F_1)`) + '; in the example, share rises from ' + m(T`{{share_H_r0}}`) + ' to ' + m(T`{{share_H_r1_B}}`) + '.</p>' +
        nav(back('main:s14')) });

    backup({ id: 'b6b', label: 'B6b', origin: 's14', targets: [], title: 'Proposition 2 in full: tuples, payoff tables, control panels', subtitle: '',
      body:
        '<p class="xs">Under full orders, class ' + m('H') + ' faces a buy order with chance ' + m(T`\lambda+b`) + ' and class ' + m('L') + ' with chance ' + m('b') + '.</p>' +
        d(T`e_H=\rho+(1-\rho)(\lambda+b),\qquad e_L=\rho+(1-\rho)b,\qquad \text{entry}=\pi e_H+(1-\pi)e_L`) +
        '<div class="twocol">' +
          ul(['At ' + m('r_1') + ', cost ' + m('c_H') + ' prepares after a buy order and only after a buy order. Class entry rates are ' + m('e_H') + ' and ' + m('e_L'),
            'At the example’s prior, entry is ' + m(T`{{entry_r1_B}}`) + ' and class ' + m('H') + ' ownership is ' + m(T`{{own_r1_B}}`),
            'At ' + m('r_0') + ', a quiet market gives a flat price, so entry is ' + m(T`{{entry_r0}}`) + ' and ownership is ' + m(T`{{own_r0}}`)], 'xs') +
          ul(['At ' + m('r_2') + ', no price covers ' + m('c_H') + ', so entry is ' + m(T`{{entry_r2}}`) + ' and ownership is ' + m(T`{{own_r2_B}}`) + ', with full orders',
            m(T`B_r(\pi)`) + ' equals ' + m(T`{{Bprior_r0}}`) + ', ' + m(T`{{Bprior_r1_B}}`) + ', ' + m(T`{{Bprior_r2}}`) + ' at ' + m('r_0') + ', ' + m('r_1') + ', ' + m('r_2')], 'xs') +
        '</div>' +
        table('t-payoffs', ['', m(T`r_0={{prim_r0}}`), m(T`r_1={{prim_r1}}`), m(T`r_2={{prim_r2}}`)], [
          ['Proceeds without entry, ' + m('t_0'), q('p2_base_r0_t0'), q('p2_base_r1_t0'), q('p2_base_r2_t0')],
          ['Proceeds with a high-class challenger, ' + m('t_H'), q('p2_base_r0_th'), q('p2_base_r1_th'), q('p2_base_r2_th')],
          ['Proceeds with a low-class challenger, ' + m('t_L'), q('p2_base_r0_tl'), q('p2_base_r1_tl'), q('p2_base_r2_tl')],
          ['Target-payoff spread, ' + m(T`\Delta_T`), q('Delta_r0'), q('Delta_r1'), q('Delta_r2')],
          ['Gross profit of class ' + m('H') + ', ' + m('g_H'), q('p2_base_r0_gh'), q('p2_base_r1_gh'), q('p2_base_r2_gh')],
          ['Gross profit of class ' + m('L') + ', ' + m('g_L'), q('p2_base_r0_gl'), q('p2_base_r1_gl'), q('p2_base_r2_gl')],
          ['Gross profit at the prior, ' + m(T`B_r({{prim_pi}})`), q('Bprior_r0'), q('Bprior_r1_B'), q('Bprior_r2')],
          ['Preparation threshold, ' + m(T`\tau(r)`), q('tau_r0'), q('tau_r1'), q('tau_r2')]]) +
        nav(back('main:s14')) });

    backup({ id: 'b6c', label: 'B6c', origin: 's14', targets: [], title: 'Proposition 2 in full: tuples, payoff tables, control panels', subtitle: '',
      body:
        table('t-panels', ['', m(T`r_0={{prim_r0}}`), m(T`r_1={{prim_r1}}`), m(T`r_2={{prim_r2}}`)], [
          { panel: 'Panel A. Equilibrium (Proposition 2)' },
          ['Informed orders, classes ' + m('H') + ' and ' + m('L'), m('(0,0)'), m('(1,-1)'), m('(1,-1)')],
          ['Posterior after a sale', q('p2_base_r0_mu_minus'), q('p2_base_r1_mu_minus'), q('p2_base_r2_mu_minus')],
          ['Posterior after no order', q('p2_base_r0_mu_zero'), q('p2_base_r1_mu_zero'), q('p2_base_r2_mu_zero')],
          ['Posterior after a purchase', q('p2_base_r0_mu_plus'), q('p2_base_r1_mu_plus'), q('p2_base_r2_mu_plus')],
          ['High-cost preparation', 'none', 'after a purchase', 'none'],
          ['Price after a sale', q('price_r0'), q('price_r1_m1_B'), q('price_r2_m1_B')],
          ['Price after no order', q('price_r0'), q('price_r1_0_B'), q('price_r2_0_B')],
          ['Price after a purchase', q('price_r0'), q('price_r1_p1_B'), q('price_r2_p1_B')],
          ['Entry ' + m(T`\mathsf{E}`), q('entry_r0'), q('entry_r1_B'), q('entry_r2')],
          ['High-class ownership ' + m(T`\mathsf{O}_H`), q('own_r0'), q('own_r1_B'), q('own_r2_B')],
          ['Expected target proceeds', q('p4_base_r0_proceeds'), q('p4_base_r1_proceeds'), q('p4_base_r2_proceeds')],
          { panel: 'Panel B. Full orders held fixed (Proposition A.2)' },
          ['Entry ' + m(T`\mathsf{E}`), q('p4_frozen_r0_entry'), q('p4_frozen_r1_entry'), ''],
          ['High-class ownership ' + m(T`\mathsf{O}_H`), q('p4_frozen_r0_own'), q('p4_frozen_r1_own'), ''],
          ['Expected target proceeds', q('p4_frozen_r0_proceeds'), q('p4_frozen_r1_proceeds'), ''],
          { panel: 'Panel C. The challenger does not see the price' },
          ['Informed orders, classes ' + m('H') + ' and ' + m('L'), m('(0,0)'), m('(1,-1)'), ''],
          ['Entry ' + m(T`\mathsf{E}`), q('p4_hidden_r0_entry'), q('p4_hidden_r1_entry'), ''],
          ['High-class ownership ' + m(T`\mathsf{O}_H`), q('p4_hidden_r0_own'), q('p4_hidden_r1_own'), ''],
          ['Expected target proceeds', q('p4_hidden_r0_proceeds'), q('p4_hidden_r1_proceeds'), '']]) +
        nav(back('main:s14')) });

    backup({ id: 'b7', label: 'B7', origin: 's19', targets: ['app:b7'], title: 'Coexistence in full: interval parts and marked strengths', subtitle: '',
      body:
        table('t-thresh', ['Strength', 'Value in the example', 'Role'], [
          tr3(m('r_A'), m(T`{{rA}}`), 'first strength with an informative market'),
          tr3(m('r_F'), m(T`{{rF_B}}`), 'first strength with a certain purchase in it'),
          tr3(m('r_N'), m(T`{{rN}}`), 'last strength with a quiet market'),
          tr3(m('r_J'), m(T`{{rJ}}`), 'the full purchase is alone from here'),
          tr3(m('r_S'), m(T`{{rS_B}}`), 'low class sells for certain from here'),
          tr3(m('r_C'), m(T`{{rC_B}}`), 'entry ceiling: the top posterior stops short of ' + m('c_H') + ' above ' + m('r_C'))]) +
        ul(['Before ' + m('r_A') + ', a purchase cannot pay at any mix rate, so no informative market exists',
          'On ' + m('[r_A,r_F)') + ', the mix rate adjusts with strength and entry rises with it',
          'From ' + m('r_F') + ' to ' + m('r_N') + ', a full purchase coexists with a quiet market and entry in it is constant',
          'Past ' + m('r_N') + ', a quiet market fails: a unit order against the flat price pays. Mixed orders at the entry floor join the full purchase on ' + m('(r_N,r_J)') + '. From ' + m('r_J') + ', the full purchase is alone'], 'xs') +
        '<p class="xs">In general, strengths with coexistence need not form one interval. Sure-purchase strengths form one interval. Under the nonfalling product ' + m(T`\Delta_T(g_H-c_H)`) + ', the whole set forms one interval at each prior.</p>' +
        nav(back('main:s19')) });

    backup({ id: 'b8', label: 'B8', origin: 's21', targets: ['app:b8'], title: 'Research in full: first-order condition, branches, cap region', subtitle: '',
      body:
        d(T`2a\lambda=\Delta_T m_\lambda-k+(\rho\Delta_T m_\lambda-k)^+`) +
        ul(['Research picks ' + m(T`\lambda`) + ' in ' + m(T`[0,\bar\lambda]`) + ' before the slot, at cost ' + m(T`\tfrac{a}{2}\lambda^2`) + ' (Proposition 4)',
          'In the example, ' + m(T`a={{res_a}}`) + ' and the cap is ' + m(T`\bar\lambda={{res_cap}}`) + '. The marked strengths are ' + m(T`r_R\approx{{res_rR}}`) + ', ' + m(T`r_{\bar\lambda}\approx{{res_rcap}}`) + ', ' + m(T`r_N\approx{{res_rN}}`) + ', ' + m(T`r_Q\approx{{res_rQ}}`) + ', ' + m(T`r_C\approx{{res_rC}}`),
          'Zero research, with entry ' + m(T`\rho`) + ', is an equilibrium exactly on ' + m('[r_0,r_N]'),
          'Recruiting research is an equilibrium exactly on ' + m('[r_R,r_C]') + ': research rises from ' + m(T`{{res_lambda_rR}}`) + ' to the cap on ' + m(T`[r_R,r_{\bar\lambda})`) + ' and stays at the cap on ' + m(T`[r_{\bar\lambda},r_C]`) + '; entry rises from ' + m(T`{{res_entry_rR}}`) + ' to ' + m(T`{{res_entry_cap}}`) + ' and keeps that value up to ' + m('r_C')], 'small') +
        '<p class="small">Zero research on ' + m('[r_0,r_N]') + '; recruiting research on ' + m('[r_R,r_C]') + '; floor-entry research on ' + m('(r_N,r_Q)') + ' and ' + m('(r_C,r_2]') + ', with ' + m(T`r_Q\approx{{res_rQ|3}}`) + '.</p>' +
        nav(back('main:s21')) });

    backup({ id: 'b8b', label: 'B8b', origin: 's21', targets: [], title: 'Research in full: first-order condition, branches, cap region', subtitle: '',
      body:
        ul(['Floor-entry research, in which both classes trade after a success, no order recruits and entry is ' + m(T`\rho`) + ', is an equilibrium exactly on ' + m('(r_N,r_Q)') + ' and on ' + m('(r_C,r_2]') + '; there is no other equilibrium',
          'At ' + m(T`{{str_r155}}`) + ', ' + m(T`{{str_r160}}`) + ' and ' + m(T`{{str_r165}}`) + ' there are exactly two equilibria: zero research, and recruiting research below the cap (class ' + m('H') + ' buys after a success, class ' + m('L') + ' abstains). Research is ' + m(T`{{res_lambda_r155}}`) + ', <span class="nw">' + m(T`{{res_lambda_r160}}`) + ',</span> ' + m(T`{{res_lambda_r165}}`) + '. Entry is ' + m(T`{{res_entry_r155}}`) + ', <span class="nw">' + m(T`{{res_entry_r160}}`) + ',</span> ' + m(T`{{res_entry_r165}}`),
          'The unique equilibrium has zero research at ' + m('r_0') + ', recruiting research at the cap at ' + m('r_1') + ' and floor-entry research at the cap at ' + m('r_2') + ', where entry is ' + m(T`\rho`)], 'small') +
        gray('Costly research with an alternative arrival follows Dow and Gorton 1997.') +
        nav(back('main:s21')) });

    var panel = function (head, text) { return '<div class="rpanel"><b>' + head + '</b>' + text + '</div>'; };
    backup({ id: 'b9', label: 'B9', origin: 's23', targets: ['app:b9'], title: 'Scope in full: costs, classes, separation, signals', subtitle: '',
      body:
        '<div class="panels4">' +
          panel('Cost laws (A.3)', '<p>The reversal holds with atoms or without atoms; an atomless high component turns the drop at the entry ceiling into a ramp</p>') +
          panel('General values, priors (A.4)', '<p>Proposition 2 holds for every ranked pair and prior at suitable costs, under (H1)–(H3) with ' + m(T`m(\pi)`) + ', ' + m(T`M(\pi)`) + '</p>') +
          panel('Many classes (A.5)', '<p>The result holds under a separation condition on class proceeds; without it one price can pool two posteriors</p><p>Without separation, two orders can carry two fit mixes at one price.</p>') +
          panel('Private signals (A.6)', '<p>In the example, accuracies ' + m(T`({{sig_comp_aT}},{{sig_comp_d}})`) + ' give entry ' + m(T`{{p4_comp_b_r0_entry}}\to{{p4_comp_b_r1_entry}}`) + '; without the challenger signal entry is ' + m(T`{{p4_comp_b_no_y_r1_entry}}`) + ' at both strengths</p>') +
        '</div>' +
        nav(back('main:s23')) });

    var E = function (lo, hi) { return m(T`U[{{` + lo + T`}},{{` + hi + T`}}]`); };
    backup({ id: 'b9b', label: 'B9b', origin: 's23', targets: [], title: 'Scope in full: costs, classes, separation, signals', subtitle: '',
      body:
        '<table class="t-econ"><thead>' +
          '<tr class="panel"><td colspan="9"><em>Panel A. Primitives</em></td></tr>' +
          '<tr><th>Economy</th><th>Low class</th><th>High class</th><th>' + m(T`\pi`) + '</th><th>' + m('c_H') + '</th><th>' + m('k') + '</th><th>' + m('r_0') + '</th><th>' + m('r_1') + '</th><th>' + m('r_2') + '</th></tr>' +
        '</thead><tbody>' +
          ['<tr><td>Moderate gap</td><td>' + m(T`{{p2_input_moderate_low_lo}}`) + '</td><td>' + m(T`{{p2_input_moderate_high_lo}}`) + '</td><td>' + q('p2_input_moderate_pi') + '</td><td>' + q('p2_input_moderate_cost') + '</td><td>' + q('p2_input_moderate_k') + '</td><td>' + q('p2_input_moderate_r0') + '</td><td>' + q('p2_input_moderate_r1') + '</td><td></td></tr>',
            '<tr><td>Narrow bands</td><td>' + E('p2_input_bands_low_lo', 'p2_input_bands_low_hi') + '</td><td>' + E('p2_input_bands_high_lo', 'p2_input_bands_high_hi') + '</td><td>' + q('p2_input_bands_pi') + '</td><td>' + q('p2_input_bands_cost') + '</td><td>' + q('p2_input_bands_k') + '</td><td>' + q('p2_input_bands_r0') + '</td><td>' + q('p2_input_bands_r1') + '</td><td>' + q('p2_input_bands_r2') + '</td></tr>',
            '<tr><td>Low prior</td><td>' + m(T`{{p2_input_ex_a_low_lo}}`) + '</td><td>' + m(T`{{p2_input_ex_a_high_lo}}`) + '</td><td>' + q('p2_input_ex_a_pi') + '</td><td>' + q('p2_input_ex_a_cost') + '</td><td>' + q('p2_input_ex_a_k') + '</td><td>' + q('p2_input_ex_a_r0') + '</td><td>' + q('p2_input_ex_a_r1') + '</td><td>' + q('p2_input_ex_a_r2') + '</td></tr>',
            '<tr><td>High prior</td><td>' + m(T`{{p2_input_ex_b_low_lo}}`) + '</td><td>' + m(T`{{p2_input_ex_b_high_lo}}`) + '</td><td>' + q('p2_input_ex_b_pi') + '</td><td>' + q('p2_input_ex_b_cost') + '</td><td>' + q('p2_input_ex_b_k') + '</td><td>' + q('p2_input_ex_b_r0') + '</td><td>' + q('p2_input_ex_b_r1') + '</td><td>' + q('p2_input_ex_b_r2') + '</td></tr>',
            '<tr><td>Wide classes</td><td>' + E('p2_input_ex_c_low_lo', 'p2_input_ex_c_low_hi') + '</td><td>' + E('p2_input_ex_c_high_lo', 'p2_input_ex_c_high_hi') + '</td><td>' + q('p2_input_ex_c_pi') + '</td><td>' + q('p2_input_ex_c_cost') + '</td><td>' + q('p2_input_ex_c_k') + '</td><td>' + q('p2_input_ex_c_r0') + '</td><td>' + q('p2_input_ex_c_r1') + '</td><td>' + q('p2_input_ex_c_r2') + '</td></tr>',
            '<tr class="last-a"><td>Same means, points</td><td>' + m(T`{{p2_input_ex_d_low_lo}}`) + '</td><td>' + m(T`{{p2_input_ex_d_high_lo}}`) + '</td><td>' + q('p2_input_ex_d_pi') + '</td><td>' + q('p2_input_ex_d_cost') + '</td><td>' + q('p2_input_ex_d_k') + '</td><td>' + q('p2_input_ex_d_r0') + '</td><td>' + q('p2_input_ex_d_r1') + '</td><td>' + q('p2_input_ex_d_r2') + '</td></tr>',
            '<tr class="panel"><td colspan="9"><em>Panel B. Outcomes</em></td></tr>',
            '<tr class="subhead"><th>Economy</th><th>Entry ' + m(T`\mathsf{E}_0`) + '</th><th>Entry ' + m(T`\mathsf{E}_1`) + '</th><th colspan="6">High-class ownership ' + m(T`\mathsf{O}_{H,1}`) + '</th></tr>',
            '<tr><td>Moderate gap</td><td>' + q('p2_moderate_r0_entry') + '</td><td>' + q('p2_moderate_r1_entry') + '</td><td colspan="6">' + q('p2_moderate_r1_ownership') + '</td></tr>',
            '<tr><td>Narrow bands</td><td>' + q('p2_bands_r0_entry') + '</td><td>' + q('p2_bands_r1_entry') + '</td><td colspan="6">' + q('p2_bands_r1_ownership') + '</td></tr>',
            '<tr><td>Low prior</td><td>' + q('p2_ex_a_r0_entry') + '</td><td>' + q('p2_ex_a_r1_entry') + '</td><td colspan="6">' + q('p2_ex_a_r1_ownership') + '</td></tr>',
            '<tr><td>High prior</td><td>' + q('p2_ex_b_r0_entry') + '</td><td>' + q('p2_ex_b_r1_entry') + '</td><td colspan="6">' + q('p2_ex_b_r1_ownership') + '</td></tr>',
            '<tr><td>Wide classes</td><td>' + q('p2_ex_c_r0_entry') + '</td><td>' + q('p2_ex_c_r1_entry') + '</td><td colspan="6">' + q('p2_ex_c_r1_ownership') + '</td></tr>',
            '<tr><td>Same means, points</td><td>' + q('p2_ex_d_r0_entry') + '</td><td>' + q('p2_ex_d_r1_entry') + '</td><td colspan="6">' + q('p2_ex_d_r1_ownership') + '</td></tr>'].join('') +
        '</tbody></table>' +
        nav(back('main:s23')) });

    backup({ id: 'b10', label: 'B10', origin: 's24', targets: ['app:b10'], title: 'Sale terms in full: access, payment rule, reserves', subtitle: '',
      body:
        ul(['<b>Price access (A.7):</b> at ' + m('r_1') + ', proceeds gain equals ' + m(T`{{p2_access_proceeds_gain}}`) + ' and net surplus gain equals ' + m(T`{{p2_access_surplus_gain}}`),
          'Orders and trade costs are the same in the two access cases at ' + m('r_1') + '. Access adds preparation only after a purchase',
          '<b>Reserve (A.9):</b> at the reserve ' + m(T`{{rsv_points_excl}}`) + ', which excludes the low class, full orders hold at both strengths and entry is flat',
          'Strict deterrence needs reserve ' + m(T`{{rsv_deter}}`) + ', a level that excludes the low class and the weak incumbent',
          '<b>Payment rule (A.8):</b> with seller share ' + m(T`\omega`) + ', the spread response weakly has the sign of ' + m(T`1-2\omega`) + '; strictly when ' + m(T`\omega\ne1/2`) + ' and ' + m(T`\mathbb{E}[(R-\ell)_+]`) + ' changes strictly'], 'small') +
        '<p class="small">Preparation, sale, and two admissible bidders are three distinct events once a reserve can exclude.</p>' +
        nav(back('main:s24')) });

    backup({ id: 'b11', label: 'B11', origin: 's7', targets: ['app:b11'], defines: ['s_noise'], title: 'Continuous order sizes need a convention', subtitle: '',
      body:
        ul(['The slot set-up uses unit orders ' + m(T`\{-1,0,1\}`) + ', so every order is on path and no off-path belief enters',
          'A menu of continuous order sizes needs a convention for the sizes that no class uses, as in Edmans, Goldstein and Jiang 2015',
          'Additive liquidity flow also keeps every size on path',
          'With Laplace noise of scale ' + m(T`\xi`) + ' and full unit orders, the top posterior equals the slot value ' + m(T`M(\pi)`) + ' when ' + m(T`1+u=e^{2/\xi}`),
          'The two set-ups then share the posterior bounds. They differ in the probability that each class reaches the top posterior'], 'small') +
        plainTake('Unit orders keep prices on path at every order.') +
        nav(back('main:s7')) });

    backup({ id: 'b12', label: 'B12', origin: 's25', targets: ['app:b12'], title: 'Predictions in full: fund share, winners, announcements, clusters', subtitle: '',
      body:
        ul(['Mean order under full two-sided trade is ' + m(T`\lambda(2\pi-1)`) + '. Counts name fund presence only when the prior is known and differs from ' + m('1/2') + '.',
          'At prior ' + m('1/2') + ', sale impact plus volume name presence when entry sits at its floor after a sale and after no order, with payoff scale ' + m(T`\rho\Delta_T`) + ' known.',
          'Winner gap after purchase against sale equals ' + m(T`[M(\pi)-m(\pi)]`) + ' times the class gap in chances to beat the first buyer.',
          'A report that reveals preparation alone carries a positive mean price change exactly when preparation stayed uncertain after some order. Both reports together average to zero.',
          'At one middle strength, sale processes can form two clusters: quiet prices with mean order zero, or live prices with mean order ' + m(T`\lambda/2`) + '.',
          'Count diligence starts, not public offers alone. Date first-buyer strength from public records before the diligence call.'], 'small') +
        nav(back('main:s25')) });

    /* ================================================================ notation (B2 and the G panel) */
    /* Rows of the B2 table in slides.tex. One source feeds the B2 slide and the notation panel. */
    var notation = [
      [[m(T`R;\ r`), 'incumbent value ' + m(T`R\sim U[0,r]`) + '; strength ' + m('r')],
        [m(T`\{F_r\}`), 'strength path; orders distributions by first-order dominance; higher ' + m('r') + ' means a stronger first buyer, with all else fixed'],
        [m(T`j\in\{H,L\};\ G_j`), 'challenger class; value law in class ' + m('j')],
        [m('D(y)'), m(T`G_L(y)-G_H(y)`) + ', the class gap at value ' + m('y')],
        [m(T`h,\ell;\ \pi`), 'the example’s class values; prior on ' + m('H')],
        [m('p'), 'reserve price, not the stock price'],
        [m(T`0,c_H;\ \rho`), 'preparation costs; ' + m(T`\rho`) + ' is the zero-cost probability'],
        [m(T`t_0,t_H,t_L`), 'proceeds with no entry, a class ' + m('H') + ' challenger, a class ' + m('L') + ' challenger'],
        [m(T`\Delta_T`), 'target-payoff spread ' + m('t_H-t_L')],
        [m(T`g_H,g_L;\ B_r(\mu)`), 'class profits before cost; profit at belief ' + m(T`\mu`)],
        [m('W_j(F)'), 'win chance: ' + m(T`\mathbb{E}_j[F(\theta)\mathbf 1\{\theta\ge p\}]`)]],
      [[m(T`\lambda;\ \beta`), 'informed presence chance; liquidity order chance'],
        [m(T`b;\ u`), m(T`b=(1-\lambda)\beta`) + '; mass ratio ' + m(T`u=\lambda/b`)],
        [m(T`X;\ P;\ V_T`), 'slot order; stock price; proceeds per share'],
        [m(T`\mu;\ m,M;\ \kappa`), 'belief ' + m(T`\Pr(H\mid P)`) + '; bounds; ' + m(T`\kappa=\min\{m,1-M\}`)],
        [m(T`\tau(r)`), 'preparation threshold: ' + m(T`B_r(\tau)=c_H`)],
        [m(T`e_r(\mu)`), 'entry probability at belief ' + m(T`\mu`)],
        [m(T`\mathsf{E}`), 'entry: chance the second buyer prepares'],
        [m(T`\mathsf{O}_H`), 'ownership: chance a good-fit second buyer wins'],
        [m('(q_H,q_L)'), 'investor orders after class ' + m('H') + ', class ' + m('L')],
        [m('W_H(F)'), 'class ' + m('H') + ' win chance at reserve ' + m('p') + ' against incumbent law ' + m('F')],
        [m(T`a;\ \bar\lambda;\ \omega`), 'research cost; cap; seller share in A.8']]
    ];

    /* Every symbol the slides use, with the pattern that finds it in a slide's LaTeX. The check
       fails if a symbol appears before the frame that defines it (frames in deck order). */
    var S = '(^|[^\\\\a-zA-Z_^])';
    var glossary = [
      { key: 'p', pattern: S + 'p(?![a-zA-Z])' },
      { key: 'R', pattern: S + 'R(?![a-zA-Z])' }, { key: 'F', pattern: S + 'F(?![a-zA-Z])' }, { key: 'r', pattern: S + 'r(?![a-zA-Z_])' },
      { key: 'class', pattern: T`G_j|` + S + T`j(?![a-zA-Z])` }, { key: 'pi', pattern: T`\\pi` }, { key: 'theta', pattern: T`\\theta` },
      { key: 'C', pattern: S + 'C(?![a-zA-Z])' }, { key: 'rho', pattern: T`\\rho` }, { key: 'c_H', pattern: 'c_H' },
      { key: 'y', pattern: S + 'y(?![a-zA-Z])' }, { key: 'D', pattern: S + 'D(?![a-zA-Z])' },
      { key: 'lambda', pattern: T`\\lambda` }, { key: 'q', pattern: S + 'q(?![a-zA-Z_])' }, { key: 'k', pattern: S + 'k(?![a-zA-Z_])' },
      { key: 'beta', pattern: T`\\beta` }, { key: 'X', pattern: S + 'X(?![a-zA-Z])' }, { key: 'P', pattern: S + 'P(?![a-zA-Z_])' },
      { key: 'V_T', pattern: 'V_T' }, { key: 'b', pattern: S + 'b(?![a-zA-Z])' }, { key: 'u', pattern: S + 'u(?![a-zA-Z])' },
      { key: 't_0', pattern: 't_0' }, { key: 'tj', pattern: T`t_(H|L|j)` }, { key: 'gj', pattern: 'g_(H|L|j)' },
      { key: 'Delta_T', pattern: T`\\Delta_T` }, { key: 'mu', pattern: T`\\mu(?!_)` }, { key: 'B', pattern: S + 'B(?![a-zA-Z])' },
      { key: 'W', pattern: 'W_(H|L|j)' },
      { key: 'x', pattern: S + 'x(?![a-zA-Z])' }, { key: 'e', pattern: S + 'e(?![a-zA-Z_])' }, { key: 'U', pattern: 'U_j' },
      { key: 'sfE', pattern: T`\\mathsf\{E\}` }, { key: 'sfO', pattern: T`\\mathsf\{O\}` },
      { key: 'm_M', pattern: S + '[mM](?![a-zA-Z_])' }, { key: 'tau', pattern: T`\\tau` },
      { key: 'K', pattern: S + 'K_' }, { key: 'kappa', pattern: T`\\kappa` },
      { key: 'F_012', pattern: 'F_[012]' }, { key: 'Delta_n', pattern: T`\\Delta_[012]` }, { key: 'e_HL', pattern: 'e_(H|L)' },
      { key: 'h', pattern: S + 'h(?![a-zA-Z])' }, { key: 'ell', pattern: T`\\ell` }, { key: 'r_01', pattern: 'r_[01]' },
      { key: 'r_2', pattern: 'r_2' }, { key: 'r_C', pattern: 'r_C' }, { key: 'r_AFNJS', pattern: 'r_(A|F|N|J|S)' },
      { key: 'a_cap', pattern: S + 'a(?![a-zA-Z_])|' + T`\\bar\\lambda` }, { key: 'mlam', pattern: T`[mM]_\\lambda|\\lambda_(E|R)` },
      { key: 'r_R', pattern: 'r_R' }, { key: 'omega', pattern: T`\\omega` },
      { key: 'e_r', pattern: 'e_r' }, { key: 'q_HL', pattern: 'q_(H|L)' }, { key: 's_noise', pattern: T`\\xi` }
    ];

    return { frames: F, glossary: glossary, notation: notation };
  }

  if (typeof window !== 'undefined') window.createDeck = createDeck;
})();
