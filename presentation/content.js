/* content.js: the 50 frames of talk/talk.tex as web slides, in the Beamer order.
 *
 * This file is kept by hand. presentation/check_deck.mjs compares it with talk/talk.tex on every
 * build: frame order, labels, titles, subtitles, hypertargets, the link graph, and every number
 * that talk.tex tags with a "% source:" comment. Edit talk.tex first, then this file.
 *
 * Contract. window.createDeck(H) returns { frames, glossary, notation }. H is supplied by the
 * renderer (presentation/render.mjs) or by the check, never by this file:
 *   H.m(latex)                 inline mathematics
 *   H.d(latex)                 display mathematics
 *   H.q(key, shown)            a number from numerics/quantity_registry.csv. key is a registry
 *                              name, "-name" (negated) or "name+name" (a sum); several keys
 *                              separated by spaces must all match. shown is the string talk.tex
 *                              prints; the renderer stops the build unless shown rounds from
 *                              the registry value at its own precision.
 *   H.qm(latex, key, shown)    the same number inside mathematics; latex contains shown. For
 *                              several numbers, pass [[key, shown], ...] instead of key, shown.
 *   H.qk(html, keys)           provenance for a formula that names a quantity but prints no
 *                              number of it (M = 1 - m).
 *   H.tx(file, row, col, value, text, latex)
 *                              a number printed in tables/<file>: the line that starts with
 *                              `row` ("Panel A:" or "Panel B:" selects a panel; "#count:..." counts
 *                              rows), cell `col` (0 = the label, 1 = the first value). text, if
 *                              given, is the shown form (an absolute value); latex shows it as
 *                              mathematics.
 *   H.go(target, text)         a link button to a \hypertarget name, as \hyperlink does.
 *   H.back(target)             the Back button of a backup frame.
 *   H.status(text)             a status word in the paper's vocabulary.
 *   H.endFrame(label)          optional; called once per frame after its fields are built.
 * Frame record: { id, label, num, part, title, titleQ, subtitle, targets, minutes, defines,
 *   widget, body }. title is the talk.tex title argument verbatim; titleQ maps a number in the
 *   title to its registry key. Reveals use data-step="n" on elements of the body.
 * ES2019, no modules, no DOM access.
 */
(function () {
  'use strict';
  var T = String.raw;

  function createDeck(H) {
    var m = H.m, d = H.d, q = H.q, qm = H.qm, tx = H.tx, go = H.go, back = H.back, st = H.status;
    var info = function (s) { return '<span class="info">' + s + '</span>'; };
    var cost = function (s) { return '<span class="cost">' + s + '</span>'; };
    var key = function (s) { return '<span class="keyidea">' + s + '</span>'; };
    var gray = function (s) { return '<p class="grayline">' + s + '</p>'; };
    var cite = function (s) { return '<span class="graycite">' + s + '</span>'; };
    var take = function (s, step) { return '<p class="takeaway"' + (step !== undefined ? ' data-step="' + step + '"' : '') + '>' + s + '</p>'; };
    var nav = function () { return '<p class="nav">' + Array.prototype.slice.call(arguments).join(' ') + '</p>'; };
    var ul = function (items, cls) {
      return '<ul' + (cls ? ' class="' + cls + '"' : '') + '>' + items.map(function (it) {
        return typeof it === 'string' ? '<li>' + it + '</li>' : '<li data-step="' + it[0] + '">' + it[1] + '</li>';
      }).join('') + '</ul>';
    };

    var F = [];
    /* Helpers run while the body is built, just before frame() is called; endFrame lets the
       renderer attribute what it recorded to this frame. */
    function frame(o) { if (H.endFrame) H.endFrame(o.label); F.push(o); }

    /* ================================================================ main frames */

    frame({ id: 'f0', label: 'F0', num: '0', part: 1, minutes: 0.25, targets: [], defines: [], widget: 'title',
      title: 'Competition Creates Competition: Stock Prices and the Discovery of Takeover Bidders', subtitle: '',
      body: '<div class="cover"><h1>Competition Creates Competition:<br>Stock Prices and the Discovery of Takeover Bidders</h1>' +
        '<p class="cover-author">Austin Li</p><p class="cover-inst">Department of Economics<br>University College London</p>' +
        '<p class="hint">→ or Space to advance · O overview · N notes · G notation · ? help</p></div>' });

    frame({ id: 'f1', label: 'F1', num: '1', part: 1, minutes: 1.5, targets: ['main:interval'], defines: [], widget: '',
      title: 'The target is for sale, and its stock still trades',
      subtitle: 'The setup',
      body:
        '<div class="flow flow-3">' +
          '<div class="box" data-step="1">Sale is public; one bidder is already in</div><span class="arrow" data-step="2" aria-hidden="true">→</span>' +
          '<div class="box" data-step="2">Target stock still trades</div><span class="arrow" data-step="3" aria-hidden="true">→</span>' +
          '<div class="box box-cost" data-step="3">Second bidder decides: pay to prepare, or stay out</div>' +
        '</div>' +
        ul([[4, 'One bidder is ready: confidentiality agreement signed, due diligence done. Call it the <b>incumbent</b>'],
          [4, 'Its type, strategic or financial, is a public clue to its strength. Its own value stays private ' + cite('Gorbenko and Malenko 2014')],
          [5, 'A second bidder is not ready. Call it the <b>challenger</b>'],
          [5, 'To bid, the challenger must first <b>prepare</b>: due diligence, finance, approvals'],
          [5, 'This step costs money and time. The paper calls it <b>entry</b>']]) +
        take('This paper is about that window: after the sale turns public, before the challenger decides whether to enter.', 6) +
        nav(go('app:interval', 'Which deals fit')) });

    frame({ id: 'f1b', label: 'F1b', num: '2', part: 1, minutes: 1.25, targets: ['main:evidence'], defines: [], widget: '',
      title: 'Does a stronger incumbent keep the challenger out?',
      subtitle: 'Earlier theory holds the challenger\'s information fixed',
      body:
        ul([[0, '<b>Earlier theory</b> says yes'],
          [0, 'A stronger incumbent raises the price the challenger pays when it wins'],
          [0, 'So preparation pays less, and fewer challengers enter ' + cite('Fishman 1988; Hirshleifer and Png 1989')],
          [1, 'This answer holds the challenger\'s information fixed'],
          [1, 'Here the challenger sees the stock price before it decides whether to enter']], 'roomy') +
        take(key('The claim:') + ' the stock price can flip the answer. A stronger incumbent can pull the challenger in.', 2) +
        nav(go('app:evidence', 'Empirical pilot')) });

    /* Past work: one row per line of work. The citations sit under each row label; talk.tex
       prints them in one gray line under the table. */
    var PAST = [
      ['Strong incumbents deter entry', 'Fishman 1988; Hirshleifer and Png 1989', 'A stronger incumbent cuts the gain from entry', 'A stock market before entry'],
      ['Entry into auctions is a choice', 'Samuelson 1985; Levin and Smith 1994; Persico 2000', 'Costs and rules decide who enters and what bidders learn', 'What a market price tells bidders before they enter'],
      ['Firms learn from stock prices', 'Dow, Goldstein and Guembel 2017; Edmans, Goldstein and Jiang 2012, 2015', 'Prices carry information that firms use for real decisions', 'An incumbent whose strength changes what the price reveals']
    ];
    frame({ id: 'f3', label: 'F3', num: '3', part: 1, minutes: 1.5, targets: ['main:lit', 'main:refs'], defines: [], widget: '',
      title: 'What past work shows, and what it does not cover',
      subtitle: 'Three lines of work meet in this paper',
      body:
        '<table class="t-past"><thead><tr><th></th><th>It shows</th><th>It does not cover</th></tr></thead><tbody>' +
          PAST.map(function (r, i) { return '<tr data-step="' + i + '"><th>' + r[0] + '<span class="graycite">' + r[1] + '</span></th><td>' + r[2] + '</td><td>' + r[3] + '</td></tr>'; }).join('') +
        '</tbody></table>' +
        take('A stronger incumbent makes entry pay less but can make the price more informative. The second effect is new.', 3) +
        nav(go('app:lit', 'Related work'), go('app:refs', 'References')) });

    frame({ id: 'f2', label: 'F2', num: '4', part: 1, minutes: 1.75, targets: [], defines: [], widget: '',
      title: 'This paper', subtitle: '',
      body:
        '<p class="lead">An investor who knows the challenger\'s value trades the target\'s stock before the challenger decides. The stock is worth what the sale pays. The model solves for trade and entry in equilibrium.</p>' +
        ul([[0, key('Competition creates competition.') + ' A stronger incumbent can make an uninformative stock price informative. Entry rises, although the challenger\'s expected auction profit before any news falls'],
          [1, '<b>Why:</b> a strong incumbent can beat a low-value challenger, but cannot beat a high-value one. Therefore, the sale price depends more on the challenger\'s value. The investor trades on this, and good news in the price makes costly preparation pay'],
          [2, '<b>The channel is information.</b> Hold fixed what the challenger learns from the price, and a stronger incumbent cannot raise entry']], 'claims') +
        take('A stronger incumbent does not always keep the challenger out. When the target\'s stock trades, entry depends on what the price reveals first.', 3) });

    frame({ id: 'f4', label: 'F4', num: '5', part: 2, minutes: 2.0, targets: ['main:omit', 'main:info'],
      defines: ['R', 'r', 'theta', 'h', 'ell', 'p', 'C', 'c_L', 'c_H', 'rho'], widget: '',
      title: 'Model: a second-price auction for the target',
      subtitle: 'Who moves, who knows what, and when',
      body:
        '<div class="timeline" role="group" aria-label="Timeline of moves">' +
          '<div class="tl"><span class="tl-n">1</span><b>Seller</b>announces the sale rule before any trade</div>' +
          '<div class="tl"><span class="tl-n">2</span><b>Investor</b>learns the challenger\'s value; trades the target\'s stock</div>' +
          '<div class="tl"><span class="tl-n">3</span><b>Market makers</b>see total order flow only; set the stock price</div>' +
          '<div class="tl tl-cost"><span class="tl-n">4</span><b>Challenger</b>sees the price and its own cost; enters or stays out</div>' +
          '<div class="tl"><span class="tl-n">5</span><b>Bidders</b>the incumbent and an entered challenger bid their values</div>' +
        '</div>' +
        ul(['<b>Sale rule:</b> a cash second-price auction with reserve price ' + m('p') + ', the minimum the seller accepts (not the stock price). The highest bid wins and pays the larger of ' + m('p') + ' and the other bid. Each bidder bids its value',
          '<b>Incumbent:</b> value ' + m('R') + ', uniform on ' + m('[0,r]') + '. The strength ' + m('r') + ' is public; only the incumbent knows ' + m('R'),
          '<b>Challenger:</b> type ' + m(T`\theta=H`) + ' or ' + m('L') + ', equally likely, with value ' + m('h') + ' or ' + m(T`\ell`) + '. It learns ' + m(T`\theta`) + ' only if it prepares',
          m(T`0<p<\ell<r<h`) + ': the incumbent can beat a low-value challenger, but cannot beat a high-value one',
          cost('<b>Cost:</b> one challenger draws one cost: ' + m('c_L') + ' with probability ' + m(T`\rho`) + ', otherwise ' + m('c_H') + ', independent of ' + m(T`\theta`))], 'small') +
        nav(go('app:omit', 'What is left out'), go('app:info', 'Why would the investor know?')) });

    frame({ id: 'f4b', label: 'F4b', num: '6', part: 2, minutes: 1.5, targets: ['main:eq', 'main:orders', 'main:laplace', 'main:notation'],
      defines: ['mu', 'm_M', 'b', 'k', 'q_HL', 'q', 'X_Z', 'P'], widget: '',
      title: 'Trading and the stock price',
      subtitle: 'Before entry: the challenger sees the price and its own cost, not the order flow, ' + m(T`\theta`) + ' or ' + m('R'),
      body:
        ul([[0, '<b>Investor:</b> knows ' + m(T`\theta`) + ' and places an order ' + m('q') + ' in ' + m('[-1,1]') + ', at a trading cost of ' + m('k') + ' per unit. Its orders after ' + m('H') + ' and after ' + m('L') + ' are ' + m('(q_H,q_L)')],
          [1, '<b>Order flow:</b> ' + m('X=q+Z') + ', where the noise ' + m('Z') + ' is Laplace with scale ' + m('b>1')],
          [2, '<b>Price:</b> a share pays the sale proceeds. The model sets its payoff without a sale to zero. Market makers set ' + m(T`P=\mathbb{E}[\text{share payoff}\mid X]`) + ', allowing for entry and the auction'],
          [3, '<b>Belief:</b> ' + m(T`\mu=\Pr(\theta=H\mid P)`) + ', the probability of high value after the price. For any orders, noise keeps ' + m(T`m\le\mu\le M`) + ', where ' + m('m=1/(1+e^{2/b})') + ' and ' + m('M=1-m')],
          [4, '<b>Equilibrium:</b> each agent maximizes expected monetary payoff given the others. Prices equal expected payoffs; beliefs follow Bayes\' rule. The investor may randomize its order (mixed orders) and deviate to any ' + m('q') + ' in ' + m('[-1,1]')]], 'roomy') +
        nav(go('app:eq', 'Equilibrium'), go('app:orders', 'Orders, units, costs'), go('app:laplace', 'Why Laplace noise'), go('app:notation', 'Notation')) });

    frame({ id: 'f5', label: 'F5', num: '7', part: 3, minutes: 2.25, targets: ['main:payoffs', 'main:payrule'],
      defines: ['Delta_T', 't_theta', 'g_HL', 'F_rbar', 'B'], widget: 'cases',
      title: 'One auction, two claims, opposite responses',
      subtitle: 'Cash second-price auction with reserve ' + m('p') + ': who wins and who pays at incumbent value ' + m('R'),
      body:
        '<div class="segmented" role="group" aria-label="Incumbent value"><button type="button" data-case="low" aria-pressed="false">' + m(T`R\le\ell`) + '</button><button type="button" data-case="high" aria-pressed="false">' + m(T`R>\ell`) + '</button></div>' +
        '<table class="t-cases"><thead><tr><th>Incumbent value</th><th>High-value challenger</th><th>Low-value challenger</th><th>Gap in target proceeds</th></tr></thead><tbody>' +
          '<tr data-row="low"><td>' + m(T`R\le\ell`) + '</td><td>wins, pays ' + m(T`\max\{p,R\}`) + '</td><td>wins, pays ' + m(T`\max\{p,R\}`) + '</td><td class="gap">' + m('0') + '</td></tr>' +
          '<tr data-row="high"><td>' + m(T`R>\ell`) + '</td><td>wins, pays ' + m('R') + '</td><td>loses; incumbent pays ' + m(T`\ell`) + '</td><td class="gap">' + m(T`R-\ell`) + '</td></tr>' +
        '</tbody></table>' +
        '<p class="small" data-step="1">As incumbent strength ' + m('r') + ' rises:</p>' +
        '<div class="two-lines" data-step="1">' +
          '<div class="info">' + m(T`\Delta_T=t_H-t_L=\mathbb{E}[(R-\ell)_+]`) + ' <span class="arrowword">↑</span><span class="gloss">target-payoff spread = expected gap (last column)</span></div>' +
          '<div>' + m(T`g_H=\mathbb{E}[(h-\max\{p,R\})_+]`) + ' <span class="arrowword">↓</span><span class="gloss">high-value challenger\'s profit before preparation cost</span></div>' +
          '<div>' + m(T`B_r(\mu)=g_L+\mu(g_H-g_L)`) + ' <span class="arrowword">↓</span><span class="gloss">challenger\'s expected gross profit at belief ' + m(T`\mu`) + '</span></div>' +
        '</div>' +
        gray(m(T`t_\theta`) + ' = expected target proceeds when a ' + m(T`\theta`) + '-challenger enters. Replacing ' + m('h') + ' with ' + m(T`\ell`) + ' in the profit formula gives ' + m('g_L') + '. Proposition 1: both signs hold weakly for any first-order strengthening, ' + m(T`R\sim F`) + ' on ' + m(T`[0,\bar r]`) + ', ' + m(T`\ell<\bar r<h`) + ' (strictly in the uniform case, ' + m(T`\bar r=r`) + ').') +
        take('One shift, opposite signs: the challenger keeps less, and target proceeds depend more on its value.', 2) +
        nav(go('app:payoffs', 'Closed forms'), go('app:payrule', 'Other payment rules')) });

    /* The declared benchmark inputs: one row per input, with its registry key. */
    var BENCH = [
      [m('h'), q('base_h', '10'), 'high challenger value'],
      [m(T`\ell`), q('base_ell', '1'), 'low challenger value'],
      [m('p'), q('base_p', '0.5'), 'reserve price'],
      [m(T`\rho`), q('base_rho', '0.25'), 'probability of the cheap cost'],
      [m('c_L'), q('base_c_low', '1'), 'cheap preparation cost'],
      [m('c_H'), q('base_c_high', '6'), 'expensive preparation cost'],
      [m('b'), q('base_b', '2'), 'noise scale; then ' + qm(T`m\approx0.27`, 'base_m', '0.27')],
      [m('k'), q('base_k', '0.02'), 'trading cost per unit'],
      [m('r_0,r_1,r_2'), q('base_r_weak', '1.2') + ', ' + q('base_r_strong', '3') + ', ' + q('base_r_collapse', '3.6'), 'weak, strong, stronger still incumbent']
    ];
    frame({ id: 'f5b', label: 'F5b', num: '8', part: 3, minutes: 0.75, targets: ['main:scale'], defines: ['r_01', 'r_2'], widget: '',
      title: 'Numerical Exercise: the benchmark', subtitle: '',
      body:
        '<table class="t-inputs t-bench-in"><thead><tr><th>Input</th><th>Value</th><th>Meaning</th></tr></thead><tbody>' +
          BENCH.map(function (r) { return '<tr><th>' + r[0] + '</th><td>' + r[1] + '</td><td>' + r[2] + '</td></tr>'; }).join('') +
        '</tbody></table>' +
        gray('Units are arbitrary. The inputs illustrate the theorem; they are not estimates from data.') +
        take('Only the incumbent\'s strength changes between ' + m('r_0') + ', ' + m('r_1') + ' and ' + m('r_2') + '.') +
        nav(go('app:scale', 'Why these inputs?')) });

    frame({ id: 'f6', label: 'F6', num: '9', part: 3, minutes: 1.25, targets: [], defines: [], widget: 'x1',
      title: 'A stronger incumbent: spread up, profit down',
      subtitle: 'Auction payoffs conditional on entry; trading and entry choices are not yet solved',
      body:
        '<div class="figure" id="x1" tabindex="0" aria-label="Figure X1. Target-payoff spread and challenger profit at the prior against incumbent strength; arrow keys move the cursor."></div>' +
        take('From ' + m('r_0') + ' to ' + m('r_1') + ', the ' + info('spread') + ' rises ' + q('base_spread_weak', '0.0167') + ' → ' + q('base_spread_strong', '0.667') + ' and the challenger\'s profit at the prior falls ' + q('base_profit_prior_weak', '4.80') + ' → ' + q('base_profit_prior_strong', '4.29') + '. At any fixed belief, a stronger incumbent lowers profit. It also makes the stock payoff depend more on the challenger\'s value.') });

    frame({ id: 'f8', label: 'F8', num: '10', part: 4, minutes: 2.0, targets: ['main:suff', 'main:floor'], defines: [], widget: 'x2',
      title: 'Only good news makes expensive preparation pay',
      subtitle: 'What the challenger does at each belief ' + m(T`\mu`) + '; benchmark picture at left',
      body:
        '<div class="split">' +
          '<div class="col">' +
            '<div class="figure" id="x2" aria-label="Figure X2. Challenger profit at the worst, prior and best belief against incumbent strength, with the two cost lines."></div>' +
            '<div class="slider"><label for="x2-r">incumbent strength ' + m('r') + '</label><input type="range" id="x2-r" min="1.05" max="3.8" step="0.01" value="3"><output id="x2-r-value" for="x2-r">3.00</output></div>' +
            '<div id="x2-readout" class="readout" aria-live="polite"></div>' +
          '</div>' +
          '<div class="col text">' +
            '<p data-step="1">' + cost('<b>Low-cost floor</b>') + ' ' + m(T`c_L<B_{r_1}(m)`) + ': cheap preparation pays at every price, so entry is at least ' + m(T`\rho`) + '</p>' +
            '<p data-step="2"><b>Entry probability:</b> ' + m(T`\Pr(\text{the challenger prepares})=\rho`) + ' when ' + m(T`B_r(\mu)<c_H`) + ', and ' + m('1') + ' when ' + m(T`B_r(\mu)\ge c_H`) + '</p>' +
            '<p data-step="3">' + cost('<b>High-cost window</b>') + ' ' + m(T`B_{r_0}(1/2)<c_H<B_{r_1}(M)`) + ': at the weak prior, expensive preparation does not pay. It pays after the best news at ' + m('r_1') + '. At ' + m('r_2') + ', even the best news falls short</p>' +
            '<p data-step="4"><b>Why price reveals ' + m(T`\mu`) + ':</b> a low-cost challenger always enters. A higher chance of high value raises expected sale proceeds. Extra entry after good news raises them further. Thus higher beliefs give higher prices</p>' +
          '</div>' +
        '</div>' +
        nav(go('app:suff', 'Reading the price'), go('app:floor', 'Why entry must stay positive')) });

    frame({ id: 'f7', label: 'F7', num: '11', part: 4, minutes: 2.25, targets: ['main:bound'], defines: [], widget: '',
      title: 'Trading pays only against a strong incumbent',
      subtitle: 'When does what the investor knows cover the trading cost ' + m('k') + '?',
      body:
        '<p class="small"><b>Residual advantage per unit, before the trading cost:</b></p>' +
        '<p class="center small">' + m(T`\begin{aligned}\text{Buy after }H:&\quad \text{expected share payoff}-\text{price}\\ \text{Sell after }L:&\quad \text{price}-\text{expected share payoff}\end{aligned}`) + '</p>' +
        '<table class="t-factors"><tbody><tr><td>Residual advantage per unit ' + m('=') + '</td>' +
          '<td data-step="1">entry probability<br>(' + m(T`\ge\rho`) + ', low-cost floor)</td><td data-step="2">' + m(T`\times`) + '</td>' +
          '<td data-step="2" class="info">target-payoff spread ' + m(T`\Delta_T`) + '</td><td data-step="3">' + m(T`\times`) + '</td>' +
          '<td data-step="3">belief in other type<br>' + m(T`1-\mu`) + ' after ' + m('H') + '<br>' + m(T`\mu`) + ' after ' + m('L') + '<br>(both ' + m(T`\ge m`) + ')</td></tr></tbody></table>' +
        '<p class="center" data-step="3">' + m(T`\rho\,m\,\Delta_T\ \le\ \text{advantage}\ \le\ \Delta_T`) + '</p>' +
        ul([[4, '<b>Weak ' + m('r_0') + ':</b> advantage ' + m(T`\le\Delta_T(r_0)<k`) + ', so every nonzero order loses in expectation: no trade, ' + m('(0,0)')],
          [5, '<b>Strong ' + m('r_1') + ':</b> each extra unit earns at least ' + m(T`(1-1/b)\,\rho m\Delta_T(r_1)>k`) + ', so full orders ' + m('(1,-1)')]], 'small') +
        '<p class="grayline" data-step="6">' + info('<b>Trading-cost window</b>') + ' ' + m(T`\Delta_T(r_0)<k<(1-1/b)\,\rho m\Delta_T(r_1)`) + '. The factor ' + m('1-1/b') + ' allows for the order\'s own price impact.</p>' +
        take('The same shift that lowers the challenger\'s profit switches informed trading on.', 6) +
        nav(go('app:bound', 'Why full orders are optimal')) });

    frame({ id: 'f9', label: 'F9', num: '12', part: 5, minutes: 2.5, targets: ['main:proof', 'main:margins', 'main:forces'], defines: [], widget: '',
      title: 'Proposition 2: a stronger incumbent can raise entry',
      subtitle: 'Weak ' + m('r_0') + ', strong ' + m('r_1') + ', stronger still ' + m('r_2') + '; all other primitives equal',
      body:
        '<div class="resultbox"><p class="resultbox-title">Proposition 2, under the three conditions below</p>' +
          '<p class="propitem" data-step="0"><span class="propnum">(i)</span><b>Weak ' + m('r_0') + ':</b> no trade, ' + m('(q_H,q_L)=(0,0)') + '; the price is uninformative; entry ' + m(T`=\rho`) + '</p>' +
          '<p class="propitem" data-step="1"><span class="propnum">(ii)</span><b>Strong ' + m('r_1') + ':</b> full orders ' + m('(1,-1)') + '; the price is informative; entry ' + m(T`>\rho`) + '; a high-value challenger acquires the target more often</p>' +
          '<p class="propitem" data-step="2"><span class="propnum">(iii)</span><b>Stronger still, ' + m('r_2') + ',</b> where the low-cost floor and profitable trading persist but ' + m(T`B_{r_2}(M)<c_H`) + ': full orders, entry back to ' + m(T`\rho`) + '</p>' +
        '</div>' +
        '<div class="split narrow" data-step="3">' +
          '<table class="t-conditions"><tbody>' +
            '<tr><td>' + cost('<b>Low-cost floor</b>') + '</td><td>' + m(T`c_L<B_{r_1}(m)`) + '</td></tr>' +
            '<tr><td>' + cost('<b>High-cost window</b>') + '</td><td>' + m(T`B_{r_0}(1/2)<c_H<B_{r_1}(M)`) + '</td></tr>' +
            '<tr><td>' + info('<b>Trading-cost window</b>') + '</td><td>' + m(T`\Delta_T(r_0)<k<(1-1/b)\,\rho m\Delta_T(r_1)`) + '</td></tr>' +
          '</tbody></table>' +
          '<p class="grayline">(i)–(ii): possible for every ' + m(T`h>\ell`) + '. Small input changes preserve the result. (iii): the benchmark and nearby. Orders and entry at equilibrium prices are unique under truthful bids.</p>' +
        '</div>' +
        take(info('wider ' + m(T`\Delta_T`) + ' → informed trading pays → informative price → good news clears ' + m('c_H') + ' → the challenger prepares at high cost'), 4) +
        nav(go('app:proof', 'Proof logic'), go('app:margins', 'How the conditions hold'), go('app:forces', 'Two forces side by side')) });

    function benchmarkTable(withR2) {
      var c = function (s) { return withR2 ? s : ''; };
      return '<p class="small-note">Entry ' + qm(T`\rho=0.25`, 'base_rho', '0.25') + ': the challenger enters only when its cost is low. High-value ownership = Pr(a high-value challenger acquires the target).</p>' +
        '<table class="t-bench' + (withR2 ? ' with-r2' : '') + '"><thead><tr><th></th>' +
          '<th>weak<br>' + qm('r_0=1.2', 'base_r_weak', '1.2') + '</th><th class="strong">strong<br>' + qm(T`\boldsymbol{r_1=3}`, 'base_r_strong', '3') + '</th>' +
          c('<th>stronger still<br>' + qm('r_2=3.6', 'base_r_collapse', '3.6') + '</th>') + '</tr></thead><tbody>' +
          '<tr data-step="1"><th>Gross auction profit before news ' + m('B_r(1/2)') + '</th><td>' + q('base_profit_prior_weak', '4.80') + '</td><td class="strong">' + q('base_profit_prior_strong', '4.29') + '</td>' + c('<td class="words">lower still</td>') + '</tr>' +
          '<tr data-step="1"><th>' + info('Target-payoff spread ' + m(T`\Delta_T`)) + '</th><td>' + q('base_spread_weak', '0.0167') + '</td><td class="strong">' + q('base_spread_strong', '0.667') + '</td>' + c('<td class="words">wider still</td>') + '</tr>' +
          '<tr data-step="2"><th>Investor orders ' + m('(q_H,q_L)') + '</th><td>' + m('(0,0)') + '</td><td class="strong">' + m(T`\boldsymbol{(1,-1)}`) + '</td>' + c('<td>' + m('(1,-1)') + '</td>') + '</tr>' +
          '<tr data-step="2"><th>Price</th><td>uninformative</td><td class="strong">informative</td>' + c('<td>informative</td>') + '</tr>' +
          '<tr data-step="3"><th>Entry</th><td>' + q('base_entry_weak', '0.250') + '</td><td class="strong">' + q('base_entry_strong', '0.523') + '</td>' + c('<td>' + q('base_entry_collapse', '0.250') + '</td>') + '</tr>' +
          '<tr data-step="3"><th>High-value ownership</th><td>' + q('base_ownership_weak', '0.125') + '</td><td class="strong">' + q('base_ownership_strong', '0.324') + '</td>' + c('<td>' + tx('table2_equilibrium_controls.tex', 'Very strong incumbent ($r=3.6$)', 4, '0.125') + '</td>') + '</tr>' +
        '</tbody></table>' +
        '<p class="small" data-step="3">Trading check: ' + qm(T`\Delta_T(r_0)=0.0167`, 'base_spread_weak', '0.0167') + qm('{}<k=0.02', 'base_k', '0.02') + qm(T`{}<0.0224=(1-1/b)\,\rho m\Delta_T(r_1)`, 'base_k+base_margin_strong_trade', '0.0224') + '</p>';
    }

    frame({ id: 'f10a', label: 'F10a', num: '13', part: 6, minutes: 1.5, targets: [], defines: [], widget: '',
      title: 'At the benchmark, entry rises from 0.250 to 0.523', titleQ: { '0.250': 'base_entry_weak', '0.523': 'base_entry_strong' },
      subtitle: 'Benchmark inputs; unique orders and entry at equilibrium prices',
      body: benchmarkTable(false) +
        take('Entry rises ' + q('base_entry_change_pp', '27.28') + ' percentage points while the challenger\'s profit at the prior falls: good news makes high-cost preparation worthwhile.', 4) });

    frame({ id: 'f10b', label: 'F10b', num: '13', part: 6, minutes: 1.0, targets: ['main:entry', 'main:cert'], defines: [], widget: '', noframenumbering: true,
      title: 'At the benchmark, entry rises from 0.250 to 0.523', titleQ: { '0.250': 'base_entry_weak', '0.523': 'base_entry_strong' },
      subtitle: 'Benchmark inputs; unique orders and entry at equilibrium prices',
      body: benchmarkTable(true) +
        take('Rise, then fall: past a ceiling strength even the best price cannot cover ' + m('c_H') + '.') +
        nav(go('app:entry', 'How entry is computed'), go('app:cert', 'Which equilibrium?')) });

    frame({ id: 'f11', label: 'F11', num: '14', part: 6, minutes: 2.25, targets: ['main:controls', 'main:welfare'], defines: [], widget: 'controls',
      title: 'Hold information fixed, and a stronger incumbent cannot raise entry',
      subtitle: 'Entry at ' + qm('r_0=1.2', 'base_r_weak', '1.2') + ' and ' + qm('r_1=3', 'base_r_strong', '3') + '; compare the full model with two information controls',
      body:
        '<div class="segmented" role="group" aria-label="Which row"><button type="button" data-row="eq" aria-pressed="true">Full model</button><button type="button" data-row="frozen" aria-pressed="false">Same orders</button><button type="button" data-row="hidden" aria-pressed="false">Price hidden</button></div>' +
        '<div class="split wide">' +
        '<table class="t-controls"><thead><tr><th></th><th>' + qm('r_0=1.2', 'base_r_weak', '1.2') + '</th><th>' + qm('r_1=3', 'base_r_strong', '3') + '</th><th>Direction</th></tr></thead><tbody>' +
          '<tr data-row="eq"><th>Full model<span class="sub">(price seen, trading re-solved)</span></th><td>' + q('base_entry_weak', '0.250') + '</td><td><b>' + q('base_entry_strong', '0.523') + '</b></td><td>' + m(T`\uparrow`) + '</td></tr>' +
          '<tr class="panel"><td colspan="4"><em>Information controls</em></td></tr>' +
          '<tr data-row="frozen"><th>Same informative orders ' + m('(1,-1)') + '<span class="sub">(imposed at both strengths; control, not an equilibrium at ' + m('r_0') + ')</span></th><td>' + q('base_frozen_entry_weak', '0.562') + '</td><td>' + q('base_frozen_entry_strong', '0.523') + '</td><td>' + m(T`\downarrow`) + '</td></tr>' +
          '<tr data-row="hidden"><th>Price hidden from challenger<span class="sub">(equilibrium of the no-price-access game)</span></th><td>' + q('base_hidden_entry_weak', '0.250') + '</td><td>' + q('base_hidden_entry_strong', '0.250') + '</td><td>flat</td></tr>' +
        '</tbody></table>' +
        '<div class="bars" id="f11-bars" aria-live="polite"></div>' +
        '</div>' +
        gray('The price-hidden row is implied by the high-cost window. Without the price, expensive preparation never pays and only the entry floor remains.') +
        take('Hold fixed what the challenger learns from the price. A stronger incumbent then cannot raise entry.') +
        nav(go('app:controls', 'Controls in detail'), go('app:welfare', 'Price level or information?')) });

    frame({ id: 'f12', label: 'F12', num: '15', part: 7, minutes: 1.5, targets: ['main:corr'], defines: [], widget: '',
      title: 'At intermediate strength, equilibria coexist',
      subtitle: 'Proposition 3: informative trade and no trade coexist at each strength shown',
      body:
        '<table class="t-cert"><thead><tr><th>Strength ' + m('r') + '</th><th>' + m('q_H') + '</th><th>' + m('q_L') + '</th><th>Entry</th></tr></thead><tbody>' +
          '<tr><td>' + q('cert_a_r', '1.55') + '</td><td>1</td><td>' + qm(T`\approx-0.460`, '-cert_a_v_interval', '-0.460') + '</td><td>' + qm(T`\approx0.545`, 'cert_a_entry_interval', '0.545') + '</td></tr>' +
          '<tr><td>' + q('cert_b_r', '1.60') + '</td><td>1</td><td>' + qm(T`\approx-0.707`, '-cert_b_v_interval', '-0.707') + '</td><td>' + qm(T`\approx0.549`, 'cert_b_entry_interval', '0.549') + '</td></tr>' +
          '<tr><td>' + q('cert_c_r', '1.65') + '</td><td>1</td><td>' + qm(T`\approx-0.903`, '-cert_c_v_interval', '-0.903') + '</td><td>' + qm(T`\approx0.551`, 'cert_c_entry_interval', '0.551') + '</td></tr>' +
        '</tbody></table>' +
        '<p class="small-note">Hover a value for its full enclosure, with outward endpoints.</p>' +
        ul([[1, 'The investor buys fully after good news and sells partly after bad news. At each listed strength, entry exceeds ' + q('base_entry_strong', '0.523') + ' at ' + m('r_1')],
          [1, 'Each economy also has a no-trade equilibrium with entry ' + qm(T`\rho=0.25`, 'base_rho', '0.25')],
          [1, 'The search does not find every possible equilibrium at other strengths']]) +
        take('At each strength shown, informative trade and no trade are both equilibria. The proof does not connect these points with a continuous branch.', 2) +
        nav(go('app:corr', 'Equilibria across strengths')) });

    frame({ id: 'f13', label: 'F13', num: '16', part: 7, minutes: 1.5, targets: ['main:robust'], defines: [], widget: 'footnote',
      title: 'The entry reversal survives four model changes',
      subtitle: 'Entry, weak to strong; each row has its own parameters',
      body:
        '<table class="t-robust"><thead><tr><th>Model</th><th>Weak</th><th>Strong</th></tr></thead><tbody>' +
          '<tr data-step="0"><th>Benchmark: Laplace noise, two cost levels</th><td>' + q('base_entry_weak', '0.250') + '</td><td>' + q('base_entry_strong', '0.523') + '</td></tr>' +
          '<tr data-step="1"><th>Continuous costs, half-width ' + q('cost_halfwidth', '0.1') + '</th><td>' + tx('table3_extensions.tex', 'Laplace, cost mixture', 1, '0.250') + '</td><td>' + q('cost_mix_laplace_entry_strong', '0.523') + '</td></tr>' +
          '<tr data-step="2"><th>Logistic noise</th><td>' + tx('table3_extensions.tex', 'logistic, cost atoms', 1, '0.250') + '</td><td>' + q('logistic_entry_strong', '0.302') + '</td></tr>' +
          '<tr data-step="3"><th>Small value gap, ' + qm('h=2', 'moderate_h', '2') + ', ' + qm(T`\ell=1`, 'moderate_ell', '1') + '</th><td>' + q('moderate_entry_weak', '0.250') + '</td><td>' + q('moderate_entry_strong', '0.527') + '</td></tr>' +
          '<tr data-step="4"><th>Complementary signals (different facts): investor accuracy ' + q('signal_trader_accuracy_value', '0.70') + ', challenger accuracy ' + q('signal_buyer_accuracy_value', '0.75') + '; ' + qm(T`\rho=0.85`, 'signal_rho', '0.85') + ', strengths ' + q('signal_r_weak', '1.1') + ' vs ' + q('signal_r_strong', '2.3') + '</th><td>' + q('signal_entry_weak', '0.850') + '</td><td>' + q('signal_entry_strong', '0.879') + '</td></tr>' +
        '</tbody></table>' +
        '<p class="grayline">Rows differ in ' + m(T`\rho`) + ' and strengths; compare within a row, not across rows.</p>' +
        '<div class="grayline"><button type="button" class="toggle-line" aria-expanded="false" data-toggle="f13-grid">Across 25 accuracy pairs</button><span id="f13-grid" hidden>: entry rises in ' + tx('table_signal_grid.tex', '#count:met', 0, '6') + ' that meet Proposition A.7, stays unchanged in ' + tx('table_signal_grid.tex', '#count:unchanged', 0, '9') + ', and falls in ' + tx('table_signal_grid.tex', '#count:falls', 0, '10') + '. In the last ' + tx('table_signal_grid.tex', '#count:falls', 0, '10') + ', the challenger already enters after its own good news against the weak incumbent.</span></div>' +
        take('The ' + m(T`r_0\to r_1`) + ' reversal survives continuous costs, logistic noise, a small value gap and complementary private signals.', 5) +
        nav(go('app:robust', 'Full table')) });

    frame({ id: 'f14', label: 'F14', num: '17', part: 7, minutes: 1.0, targets: ['main:reserve'], defines: [], widget: 'access',
      title: 'Price access raises proceeds and surplus at $r_1$',
      subtitle: 'Incumbent held at ' + qm('r_1=3', 'base_r_strong', '3') + '; price seen or hidden; trading re-solved in both',
      body:
        '<div class="segmented" role="group" aria-label="Highlight a column"><button type="button" data-col="1" aria-pressed="false">Price observed</button><button type="button" data-col="2" aria-pressed="false">Price hidden</button></div>' +
        '<table class="t-access"><thead><tr><th></th><th data-col="1">Price observed</th><th data-col="2">Price hidden</th><th>Gain</th></tr></thead><tbody>' +
          '<tr><th>Expected target proceeds</th><td data-col="1">' + q('base_revenue_feedback', '0.872') + '</td><td data-col="2">' + q('base_revenue_hidden', '0.615') + '</td><td>' + q('base_revenue_gain', '0.258') + '</td></tr>' +
          '<tr><th>Acquisition surplus net of preparation costs</th><td data-col="1">' + tx('table2_equilibrium_controls.tex', 'Net acquisition surplus', 1, '2.38') + '</td><td data-col="2">' + tx('table2_equilibrium_controls.tex', 'Net acquisition surplus', 2, '2.30') + '</td><td>' + q('base_net_surplus_gain', '0.0802') + '</td></tr>' +
        '</tbody></table>' +
        ul(['<b>Surplus:</b> the final owner\'s value less preparation costs. The sale price moves money between the buyer and shareholders', 'The investor uses the same full orders in both economies, so trading costs coincide', 'Extra entry occurs only when the expected gain from the auction covers the preparation cost. It can also prevent a failed sale']) +
        gray('Gain from unrounded values. At ' + m('r_0') + ' prices are uninformative, so there is no gain. The comparison holds the sale rule and the incumbent distribution fixed.') +
        nav(go('app:reserve', 'Reserve')) });

    frame({ id: 'f15', label: 'F15', num: '18', part: 8, minutes: 1.0, targets: [], defines: [], widget: '',
      title: 'Three predictions',
      subtitle: 'Public sales: the incumbent is ready; the challenger can still choose whether to prepare',
      body:
        ul([[0, '<b>A stronger incumbent can draw the challenger in</b> when the stock price comes before the entry decision. Without that price, a stronger incumbent cannot raise entry'],
          [1, '<b>A challenger that prepares after good news wins more often.</b> In the benchmark, the high-value share among challengers that prepare equals ' + m(T`\mu`) + ', the probability of high value implied by the price'],
          [2, '<b>Beyond the ceiling, entry no longer responds to price.</b> Cheap entry and profitable trade must persist. The price stays informative, but even the best news cannot cover ' + m('c_H')]], 'roomy') +
        gray('Outcome: the start of diligence. A valid test must use the price before that decision. Returns before a bid can also reflect an expected bid (Schwert 1996; Online Appendix D).') });

    frame({ id: 'f16', label: 'F16', num: '19', part: 8, minutes: 1.0, targets: [], defines: [], widget: '',
      title: 'Conclusion', subtitle: '',
      body:
        ul([key('A stronger incumbent can bring the challenger in:') + ' at the benchmark, entry rises from ' + q('base_entry_weak', '0.250') + ' to ' + q('base_entry_strong', '0.523') + ' although the challenger\'s expected auction profit before any news falls',
          '<b>Why:</b> a stronger incumbent makes sale proceeds depend more on the challenger\'s value. The investor trades on this information. Good news then makes high-cost preparation worthwhile.',
          '<b>Implication:</b> a stronger incumbent can attract entry because it changes what the stock price reveals before the challenger prepares.'], 'conclusion') });

    /* ================================================================ backup frames */

    function backup(o) { o.part = 'B'; o.minutes = 0; o.backup = true; o.num = o.label; frame(o); }

    backup({ id: 'a1', label: 'A1', origin: 'f1', targets: ['app:interval'], defines: [], widget: '',
      title: 'Which deals fit the decision interval?', subtitle: '',
      body:
        ul(['A disclosed approach, a public strategic review or an open contest can create the interval. The sale must become public before the challenger commits',
          'The challenger can then use the stock price before it decides whether to prepare',
          'Incumbent strength is its public value distribution. Its actual value remains private',
          'Imprivata\'s proxy separates an unsolicited approach, buyer outreach, and interest that depends on further diligence. These records show costly preparation. They do not test whether the price causes entry ' + cite('Imprivata 2016; Boone and Mulherin 2007; Gentry and Stroup 2019')], 'roomy') +
        gray('A deal fits only if the sale is public before the challenger decides. Online Appendix D sets out the date checks.') +
        nav(back('main:interval')) });

    backup({ id: 'a2', label: 'A2', origin: 'f1b', targets: ['app:evidence'], defines: [], widget: '',
      title: 'How the empirical pilot would work', subtitle: '',
      body:
        ul(['<b>Pilot (Online Appendix D):</b> use disclosures to date approaches, buyer contacts, diligence, proposals and final selection',
          'Separate when an event occurred from when it first became public',
          '<b>First requirement:</b> the sale is public while the challenger can still choose whether to prepare',
          '<b>Outcome:</b> the start of costly preparation; measure the price before this decision',
          '<b>Caution:</b> returns before a bid can also reflect an expected bid ' + cite('Schwert 1996')], 'roomy') +
        gray('Online Appendix D sets out the pilot design for the predictions of Section 7.') +
        nav(back('main:evidence')) });

    var LIT = [
      ['Dow, Goldstein and Guembel (2017)', 'investment feeds back on information', 'auction profit falls; the target-payoff spread rises'],
      ['Edmans, Goldstein and Jiang (2015)', 'real actions curb bad-news trading', 'incumbent strength changes what the price reveals'],
      ['Edmans, Goldstein and Jiang (2012)', 'prices affect takeover activity', 'a challenger learns its own value'],
      ['Fishman (1988);<br>Hirshleifer and Png (1989)', 'stronger rivals deter preparation', 'deterrence holds at fixed information (Prop. A.3)'],
      ['Levin and Smith (1994);<br>Gentry and Stroup (2019)', 'bidders choose whether to enter', 'entry responds to the price'],
      ['Roberts and Sweeting (2013)', 'selective entry shapes procedure', 'optimal sale terms remain open'],
      ['Persico (2000)', 'formats shape bidders\' information', 'the informed party is not a bidder'],
      ['Luo (2005)', 'learning from announcement returns', 'learning precedes entry'],
      ['Betton et al. (2014); Lin et al. (2025)', 'negotiation feedback; payment choice', 'cash payment fixed; the challenger chooses whether to prepare'],
      ['Cornelli and Li (2002)', 'arbitrage positions affect tenders', 'the investor does not tender'],
      ['Pernoud and Gleyze (2026);<br>Liu and Bernhardt (2022);<br>Carlin et al. (2026)', 'learning own values and rivals;<br>post-auction feedback;<br>bidder-pool choice', 'the informed party trades outside the auction, before entry']
    ];
    backup({ id: 'a3', label: 'A3', origin: 'f3', targets: ['app:lit'], defines: [], widget: 'rows',
      title: 'Related work in more detail',
      subtitle: 'A stronger incumbent lowers auction profit but can make the stock price more informative',
      body:
        '<table class="t-lit hover-rows"><thead><tr><th>Earlier work</th><th>Result</th><th>This paper</th></tr></thead><tbody>' +
        LIT.map(function (r) { return '<tr><td>' + r[0] + '</td><td>' + r[1] + '</td><td>' + r[2] + '</td></tr>'; }).join('') +
        '</tbody></table>' + nav(back('main:lit')) });

    backup({ id: 'a4', label: 'A4', origin: 'f4', targets: ['app:omit'], defines: [], widget: '',
      title: 'What the model leaves out, and why', subtitle: '',
      body:
        '<table class="t-omit"><tbody>' +
          '<tr><th>In the model</th><td>Neither bidder trades. The investor has no initial position, cannot bid, tender or acquire, and has no control rights. The sale applies to all target shares. No shareholder can hold out. An investor who knows the challenger has low value cannot profit in expectation from a purchase that mimics good news.</td></tr>' +
          '<tr><th>Outside the model</th><td>A bidder\'s advance target-share stake (a toehold) ' + cite('Bulow, Huang and Klemperer 1999') + '; shareholder holdouts ' + cite('Grossman and Hart 1980') + '; announced bids or large initial bids as signals ' + cite('Fishman 1988') + ' (strength here is a distribution); incumbent or target manipulation and the investor\'s choice to acquire information ' + cite('Goldstein and Guembel 2008') + '; trading and entry under first-price auctions or bargaining.</td></tr>' +
        '</tbody></table>' +
        take('The model makes no claim about how a bidder\'s advance target-share stake affects entry.') +
        nav(back('main:omit')) });

    backup({ id: 'a5', label: 'A5', origin: 'f4', targets: ['app:info'], defines: ['a_d'], widget: '',
      title: 'Complementary, not superior, information', subtitle: '',
      body:
        ul(['The challenger knows its own integration plans; a specialist investor may know the target\'s customers, technology and product demand',
          'These are different facts about the same acquisition match',
          'Preparation (diligence) is what reveals the exact value to the challenger',
          'In the benchmark, the investor knows the challenger\'s acquisition value and the challenger does not. Section 5.3 gives each a private signal',
          'The reversal holds with challenger signal accuracy ' + qm('d=0.75', 'signal_buyer_accuracy_value', '0.75') + ' above investor accuracy ' + qm('a=0.70', 'signal_trader_accuracy_value', '0.70')], 'roomy') +
        nav(go('app:signals', 'Signals and entry'), back('main:info')) });

    backup({ id: 'a6', label: 'A6', origin: 'a5', targets: ['app:signals'], defines: ['TY', 'e_HL'], widget: '',
      title: 'The price helps a challenger with its own signal', subtitle: '',
      body:
        ul(['Investor signal ' + m('T') + ' (accuracy ' + m('a') + '), challenger signal ' + m('Y') + ' (accuracy ' + m('d') + '); the challenger uses ' + m(T`\Pr(H\mid P,\,Y=y)`) + ', ' + m('P') + ' = stock price',
          'Entry can differ by value: ' + m('e_H') + ' and ' + m('e_L') + ' are preparation probabilities for high- and low-value challengers. The price still reveals the market\'s belief',
          'Example: ' + qm('a=0.70', 'signal_trader_accuracy_value', '0.70') + ', ' + qm('d=0.75', 'signal_buyer_accuracy_value', '0.75') + ': entry ' + q('signal_entry_weak', '0.850') + ' → ' + q('signal_entry_strong', '0.879') + '; ' + qm(T`\rho=0.85`, 'signal_rho', '0.85') + ', ' + qm('c_H=7.14', 'signal_c_high', '7.14') + ', ' + qm('k=0.015', 'signal_k', '0.015') + ', strengths ' + q('signal_r_weak', '1.1') + ' vs ' + q('signal_r_strong', '2.3')], 'small') +
        '<table class="t-grid"><thead><tr><th>Pairs</th><th>Signal accuracies (25 pairs)</th><th>Entry change (pp)</th></tr></thead><tbody>' +
          '<tr><td>' + tx('table_signal_grid.tex', '#count:met', 0, '6') + '</td><td>meet Prop. A.7</td><td>rises ' + tx('table_signal_grid.tex', '0.71 & 0.74', 4, '2.81') + ' to ' + tx('table_signal_grid.tex', '0.72 & 0.75', 4, '3.09') + '</td></tr>' +
          '<tr><td>' + tx('table_signal_grid.tex', '#count:unchanged', 0, '9') + '</td><td>' + m(T`d\le0.75`) + ', condition not met</td><td>unchanged</td></tr>' +
          '<tr><td>' + tx('table_signal_grid.tex', '#count:falls', 0, '10') + '</td><td>' + m(T`d\ge0.76`) + '</td><td>falls ' + tx('table_signal_grid.tex', '0.72 & 0.77', 4, '-4.03', '4.03') + ' to ' + tx('table_signal_grid.tex', '0.68 & 0.76', 4, '-4.49', '4.49') + '</td></tr>' +
        '</tbody></table>' +
        take('The theorem covers ' + tx('table_signal_grid.tex', '#count:met', 0, '6') + ' pairs; the other 19 report computed entry. The price can help a challenger that has its own signal.') +
        nav(back('app:info')) });

    backup({ id: 'a7', label: 'A7', origin: 'f4b', targets: ['app:eq'], defines: ['sigma'], widget: '',
      title: 'Equilibrium and the two comparisons', subtitle: '',
      body:
        ul(['<b>Equilibrium:</b> the investor may randomize its order. The price accounts for entry; the challenger updates its belief and chooses whether to prepare. Bidders bid their values. The investor may deviate to any ' + m(T`q\in[-1,1]`),
          'Order flow ' + m('X=q+Z') + ', Laplace noise ' + m('Z') + ' with scale ' + m('b') + '; stock price ' + m('P(X)') + ' = expected target payoff given ' + m('X'),
          '<b>Two comparisons kept apart:</b> to check one investor order, hold the price and entry rules fixed. To compare incumbent strengths, solve those rules again',
          '<b>Uniqueness</b> covers investor orders and entry at prices that occur in equilibrium, under truthful bids'], 'roomy') +
        nav(back('main:eq')) });

    function t1(row, a, b) {
      return '<td>' + tx('table1_auction_primitives.tex', row, 1, a) + '</td><td>' + tx('table1_auction_primitives.tex', row, 2, b) + '</td>';
    }
    backup({ id: 'a8', label: 'A8', origin: 'f5', targets: ['app:payoffs'], defines: ['t_0', 'F_rbar'], widget: '',
      title: 'Acquisition payoffs in closed form', subtitle: '',
      body:
        d(T`\begin{aligned}&t_0=p(1-p/r), && t_H=r/2+p^2/(2r), && t_L=\ell-(\ell^2-p^2)/(2r),\\ &g_H=h-r/2-p^2/(2r), && g_L=(\ell^2-p^2)/(2r), && \Delta_T=(r-\ell)^2/(2r)\end{aligned}`) +
        '<table class="t-prim"><thead><tr><th></th><th>weak ' + qm('r_0=1.2', 'base_r_weak', '1.2') + '</th><th>strong ' + qm('r_1=3', 'base_r_strong', '3') + '</th></tr></thead><tbody>' +
          '<tr><th>Proceeds without a challenger, ' + m('t_0') + '</th>' + t1('Proceeds without a challenger', '0.292', '0.417') + '</tr>' +
          '<tr><th>Proceeds with a high-value challenger, ' + m('t_H') + '</th>' + t1('Proceeds with a high-value challenger', '0.704', '1.54') + '</tr>' +
          '<tr><th>Proceeds with a low-value challenger, ' + m('t_L') + '</th>' + t1('Proceeds with a low-value challenger', '0.688', '0.875') + '</tr>' +
          '<tr><th>Gross profit of a high-value challenger, ' + m('g_H') + '</th>' + t1('Gross profit of a high-value challenger', '9.30', '8.46') + '</tr>' +
          '<tr><th>Gross profit of a low-value challenger, ' + m('g_L') + '</th>' + t1('Gross profit of a low-value challenger', '0.313', '0.125') + '</tr>' +
          '<tr><th>' + info('Target-payoff spread, ' + m(T`\Delta_T=t_H-t_L`)) + '</th><td>' + q('base_spread_weak', '0.0167') + '</td><td>' + q('base_spread_strong', '0.667') + '</td></tr>' +
          '<tr><th>Expected gross profit at the prior, ' + m('B_r(1/2)') + '</th><td>' + q('base_profit_prior_weak', '4.80') + '</td><td>' + q('base_profit_prior_strong', '4.29') + '</td></tr>' +
        '</tbody></table>' +
        gray('Proposition 1 holds for any ' + m('F') + ' on ' + m(T`[0,\bar r]`) + ', ' + m(T`\ell<\bar r<h`) + '; strict when the change in ' + m('F') + ' has positive integral over the relevant range.') +
        take('These formulas use uniform incumbent values. The opposite effects also hold for other incumbent value distributions.') +
        nav(back('main:payoffs')) });

    backup({ id: 'a9', label: 'A9', origin: 'f5', targets: ['app:payrule'], defines: ['eta'], widget: 'x4',
      title: 'The payment rule decides the sign of the spread effect', subtitle: '',
      body:
        '<div class="split">' +
          '<div class="col"><div class="figure" id="x4" tabindex="0" aria-label="Figure X4. Target-payoff spread and challenger profit against the seller bargaining weight; arrow keys move the cursor."></div></div>' +
          '<div class="col text">' +
            '<p>Alternative rule: values are verifiable and the reserve is zero. The seller receives the runner-up\'s value plus share ' + m(T`\eta`) + ' of the gap to the winner\'s value</p>' +
            '<p>A stronger incumbent cannot raise challenger profit. The spread ' + info(m(T`\Delta_\eta`)) + m(T`=\eta(h-\ell)+(1-2\eta)\,\mathbb{E}[(R-\ell)_+]`) + ' weakly rises if ' + m(T`\eta<1/2`) + ', stays unchanged at ' + m(T`\eta=1/2`) + ', and weakly falls if ' + m(T`\eta>1/2`) + ', for any ' + m(T`R\sim F`) + ' on ' + m(T`[0,\bar r]`) + ', ' + m(T`\ell<\bar r<h`) + ', ' + m(T`0\le\eta<1`) + '</p>' +
          '</div>' +
        '</div>' +
        take('This result covers sale payments. Trading and entry under bargaining or first-price auctions remain unsolved.') +
        nav(back('main:payrule')) });

    backup({ id: 'a10', label: 'A10', origin: 'f7', targets: ['app:bound'], defines: ['U_Pi'], widget: '',
      title: 'Why the investor\'s order is unique', subtitle: '',
      body:
        ul(['<b>Weak:</b> gain per unit is at most ' + m(T`\Delta_T(r_0)<k`) + '. Every nonzero order loses in expectation; the belief stays at ' + m('1/2'),
          '<b>Strong:</b> let ' + m(T`s\in[0,1]`) + ' be order size in the profitable direction. ' + m(T`\Pi_\theta(s)`) + ' is expected gain per unit before cost; ' + m(T`U_\theta(s)`) + ' is expected profit:']) +
        d(T`U_\theta(s)=s\,\Pi_\theta(s)-ks,\qquad U_\theta'(s)\ \ge\ (1-1/b)\,\rho m\,\Delta_T(r_1)-k\ >\ 0\quad\text{on }[0,1]`) +
        ul(['The bound holds for every order size under any candidate equilibrium with the low-cost entry floor, even when investor orders mix',
          '<b>False good news:</b> an investor who knows value is low has a negative expected gain if it buys to mimic good news. It still pays ' + m('k'),
          'Incumbent or target manipulation and toeholds: outside the model (A4)']) +
        nav(back('main:bound')) });

    backup({ id: 'a11', label: 'A11', origin: 'f4b', targets: ['app:orders'], defines: [], widget: '',
      title: 'Orders, units and the trading cost', subtitle: '',
      body:
        ul([m(T`q\in[-1,1]`) + ' is a small order in target shares, measured in the same units as noise. It gives no control of the target. The investor starts with no position',
          m('k') + ' is the cost per unit to execute or hold the position. The order also affects the price; that price effect is separate',
          '<b>Why full orders are optimal:</b> gain per unit is at least ' + m(T`\rho m\Delta_T`) + '. The noise bound limits the loss from price impact to a fraction ' + m('1/b'),
          'The expected gain from each extra unit exceeds ' + m('k') + ' throughout ' + m('[0,1]') + '. Full orders are the unique best response; A10 gives the bound',
          'Against the weak incumbent, ' + m(T`\Delta_T(r_0)<k`) + ', so every nonzero order loses in expectation'], 'roomy') +
        nav(back('main:orders')) });

    backup({ id: 'a12', label: 'A12', origin: 'f4b', targets: ['app:notation'], defines: [], widget: 'notation',
      title: 'Notation', subtitle: '',
      body: '<div class="notation" id="notation-table"></div>' + nav(back('main:notation')) });

    backup({ id: 'a13', label: 'A13', origin: 'f8', targets: ['app:suff'], defines: ['mu_X'], widget: '',
      title: 'The price reveals the market\'s belief', subtitle: '',
      body:
        ul(['Even when the investor randomizes its order, Laplace noise bounds the belief from flow (likelihood ratio within ' + m(T`e^{\pm2/b}`) + '):']) +
        d(T`\begin{gathered}\mu_X(x)=\Pr(H\mid X=x)\in[m,M]\\ P=t_0+e(P)[t_L-t_0+\Delta_T\mu_X]\\ \mu_X=\frac{P-t_0-e(P)(t_L-t_0)}{e(P)\Delta_T}\end{gathered}`) +
        ul([m('t_0') + ' = expected target proceeds without a challenger; ' + m('e(P)') + ' = preparation probability after price ' + m('P'),
          m(T`e(P)\ge\rho>0`) + ' and ' + m(T`\Delta_T>0`) + ', so the denominator is positive. The price therefore reveals ' + m(T`\mu_X`),
          'This also holds when some prices have positive probability or entry jumps at a threshold']) +
        take('The challenger can recover the market\'s probability of high value from the price alone.') +
        nav(back('main:suff')) });

    backup({ id: 'a14', label: 'A14', origin: 'f4b', targets: ['app:laplace'], defines: ['f', 'x_star', 'eps_C'], widget: 'x3',
      title: 'Laplace and logistic noise: what changes', subtitle: '',
      body:
        '<div class="figure wide" id="x3" tabindex="0" aria-label="Figure X3. Posterior tail and entry against the threshold distance, Laplace and logistic noise; arrow keys move the cursor."></div>' +
        ul(['Both noise densities ' + m('f') + ' satisfy ' + m(T`|f'|\le f/b`) + ', so the same trading bound applies',
          'With Laplace noise, beliefs reach ' + m('m') + ' and ' + m('M') + ' at finite flows. With logistic noise, they approach those bounds only in the tails (' + qm(T`x^*\approx5.42`, 'logistic_flow_threshold', '5.42') + ', about ' + q('logistic_threshold_noise_sd', '1.5') + ' noise standard deviations from the center)',
          'Entry with logistic noise is ' + q('logistic_entry_strong', '0.302') + ' versus ' + q('base_entry_strong', '0.523') + ' with Laplace noise; continuous costs (' + qm(T`\varepsilon_C=0.1`, 'cost_halfwidth', '0.1') + '): Laplace ' + q('cost_mix_laplace_entry_strong', '0.523') + ' and logistic ' + q('cost_mix_logistic_entry_strong', '0.301') + '. The noise laws share ' + m('b') + ' but have different variances. These values do not rank their information content'], 'small') +
        nav(back('main:laplace')) });

    backup({ id: 'a15', label: 'A15', origin: 'f8', targets: ['app:floor'], defines: [], widget: '',
      title: 'Why low-cost preparation must pay after every price', subtitle: '',
      body:
        ul(['The ' + cost('low-cost floor') + ' keeps entry ' + m(T`\ge\rho`) + ' after every price. The price reveals the market\'s belief; the investor\'s gain per unit is at least ' + m(T`\rho m\Delta_T`),
          'If low-cost preparation does not pay after bad news, entry can stop there. Different flows can then receive the same price',
          'If low-cost preparation does not pay at the prior, no preparation and no trade can be an equilibrium, provided no other source links target value to challenger value',
          'At the benchmark, ' + qm(T`B_{r_1}(m)-c_L=1.37`, 'base_margin_low_cost', '1.37') + ': low-cost preparation pays even after the worst news',
          'With the price hidden, entry is ' + q('base_hidden_entry_weak base_hidden_entry_strong', '0.250') + ' at both strengths: only low-cost preparation pays',
          'The extension with continuous costs also keeps low-cost entry positive after every price'], 'roomy') +
        nav(back('main:floor')) });

    backup({ id: 'a16', label: 'A16', origin: 'f9', targets: ['app:proof'], defines: ['alpha'], widget: '',
      title: 'Proof logic in four steps', subtitle: '',
      body:
        '<ol class="steps">' +
          '<li data-step="0"><b>Weak economy:</b> no nonzero order covers ' + m('k') + ' in expectation; no trade; entry ' + m(T`\rho`) + '</li>' +
          '<li data-step="1"><b>Strong economy:</b> the global bound (A10) forces full orders</li>' +
          '<li data-step="2">Under full orders, the belief needed for costly preparation lies in ' + m('(1/2,M)') + '. Let ' + m(T`\alpha_\theta`) + ' be the chance of news above that threshold given type ' + m(T`\theta`) + '. Then ' + m(T`\alpha_H>\alpha_L`) + ': extra entry favors high-value challengers</li>' +
          '<li data-step="3"><b>Information:</b> the strong price can reproduce the weak signal by discarding information. A type-independent rule cannot do the reverse. This is strict Blackwell dominance</li>' +
        '</ol>' +
        '<p data-step="4"><b>Part (iii):</b> with the floor and profitable trading still in place at ' + m('r_2') + ', ' + m(T`B_{r_2}(M)<c_H`) + ' removes expensive entry.</p>' +
        take('Step 2 rules out other trading outcomes, even when the investor may randomize its order.', 4) +
        nav(back('main:proof')) });

    backup({ id: 'a17', label: 'A17', origin: 'f9', targets: ['app:margins'], defines: [], widget: '',
      title: 'For every $h>\\ell$, some inputs satisfy all three conditions', subtitle: '',
      body:
        '<table class="t-margins"><thead><tr><th colspan="3">Positive gaps inside the benchmark conditions</th></tr></thead><tbody>' +
          '<tr><td>' + cost('Low-cost floor') + '</td><td>' + m(T`B_{r_1}(m)-c_L`) + '</td><td>' + q('base_margin_low_cost', '1.37') + '</td></tr>' +
          '<tr><td>' + cost('High-cost window') + ', weak prior</td><td>' + m(T`c_H-B_{r_0}(1/2)`) + '</td><td>' + q('base_margin_high_prior', '1.20') + '</td></tr>' +
          '<tr><td>' + cost('High-cost window') + ', best strong price</td><td>' + m(T`B_{r_1}(M)-c_H`) + '</td><td>' + q('base_margin_high_ceiling', '0.217') + '</td></tr>' +
          '<tr><td>' + info('Trading-cost window') + ', weak</td><td>' + m(T`k-\Delta_T(r_0)`) + '</td><td>' + q('base_margin_weak_trade', '0.00333') + '</td></tr>' +
          '<tr><td>' + info('Trading-cost window') + ', strong</td><td>' + m(T`(1-1/b)\rho m\Delta_T(r_1)-k`) + '</td><td>' + q('base_margin_strong_trade', '0.00241') + '</td></tr>' +
          '<tr class="total"><td>Smallest gap</td><td></td><td>' + q('base_minimum_theorem_margin', '0.00241') + '</td></tr>' +
        '</tbody></table>' +
        ul(['For every ' + m(T`h>\ell`) + ', choose ' + m('r_0<r_1') + ' near ' + m(T`\ell`) + '. Then choose ' + m('k') + ', ' + m('c_H') + ' and ' + m('c_L') + ' strictly inside the stated intervals',
          'This proves that suitable inputs exist. It does not estimate a typical effect. In the separate example with ' + qm('h=2', 'moderate_h', '2') + ': minimum margin ' + qm(T`8.01\times10^{-4}`, 'moderate_minimum_theorem_margin', T`8.01\times10^{-4}`),
          'Part (iii) is not claimed for every ' + m(T`h>\ell`)], 'small') +
        nav(back('main:margins')) });

    backup({ id: 'a18', label: 'A18', origin: 'f9', targets: ['app:forces'], defines: [], widget: 'columns',
      title: 'Two forces from one payment rule', subtitle: '',
      body:
        '<table class="t-forces hover-cols"><thead><tr><th></th><th data-col="1">Deterrence</th><th data-col="2" class="info">Information</th></tr></thead><tbody>' +
          '<tr><th>What changes</th><td data-col="1">challenger profit ' + m(T`B_r(\mu)\downarrow`) + ' at every belief</td><td data-col="2">' + info('target-payoff spread ' + m(T`\Delta_T\uparrow`)) + '</td></tr>' +
          '<tr><th>Who responds</th><td data-col="1">the challenger, at a given belief</td><td data-col="2">the investor, then the price, then the challenger\'s belief</td></tr>' +
          '<tr><th>What it needs</th><td data-col="1">hold information fixed</td><td data-col="2">positive entry after every price; the challenger sees the price before preparation</td></tr>' +
          '<tr><th>Effect on entry</th><td data-col="1"><b>weakly ' + m(T`\downarrow`) + '</b> ' + cite('(Prop. A.3)') + '</td><td data-col="2">can rise when trading pays and good news covers ' + cost(m('c_H')) + '</td></tr>' +
        '</tbody></table>' +
        take('Under Proposition 2\'s conditions: ' + info('stronger incumbent → wider ' + m(T`\Delta_T`) + ' → informed trading pays → informative price → good news clears') + ' ' + cost(m('c_H')) + ' ' + info('→ the challenger prepares at high cost')) +
        nav(back('main:forces')) });

    var A19_IN = [['h', 'base_h', '10', 'moderate_h', '2'], [T`\ell`, 'base_ell', '1', 'moderate_ell', '1'], ['p', 'base_p', '0.5', 'moderate_p', '0.5'],
      [T`\rho`, 'base_rho', '0.25', 'moderate_rho', '0.25'], ['c_L', 'base_c_low', '1', 'moderate_c_low', '0.3'], ['c_H', 'base_c_high', '6', 'moderate_c_high', '0.89'],
      ['b', 'base_b', '2', 'moderate_b', '2'], ['k', 'base_k', '0.02', 'moderate_k', '0.002']];
    backup({ id: 'a19', label: 'A19', origin: 'f5b', targets: ['app:scale'], defines: [], widget: '',
      title: 'The examples use chosen inputs, not estimates', subtitle: '',
      body:
        '<div class="split narrow">' +
          '<table class="t-inputs"><thead><tr><th>Input</th><th>Benchmark</th><th>Smaller gap</th></tr></thead><tbody>' +
            A19_IN.map(function (r) { return '<tr><th>' + m(r[0]) + '</th><td>' + q(r[1], r[2]) + '</td><td>' + q(r[3], r[4]) + '</td></tr>'; }).join('') +
          '</tbody></table>' +
          '<table class="t-outcomes"><thead><tr><th></th><th>Benchmark</th><th>Smaller gap</th></tr></thead><tbody>' +
            '<tr><th>Strengths</th><td>' + q('base_r_weak', '1.2') + ' → ' + q('base_r_strong', '3') + '</td><td>' + q('moderate_r_weak', '1.05') + ' → ' + q('moderate_r_strong', '1.5') + '</td></tr>' +
            '<tr><th>Entry</th><td>' + q('base_entry_weak', '0.250') + ' → ' + q('base_entry_strong', '0.523') + '</td><td>' + q('moderate_entry_weak', '0.250') + ' → ' + q('moderate_entry_strong', '0.527') + '</td></tr>' +
            '<tr><th>Minimum theorem margin</th><td>' + q('base_minimum_theorem_margin', '0.00241') + '</td><td>' + qm(T`8.01\times10^{-4}`, 'moderate_minimum_theorem_margin', T`8.01\times10^{-4}`) + '</td></tr>' +
          '</tbody></table>' +
        '</div>' +
        gray('Units are arbitrary. These values illustrate the theorem; they are not estimates from data. Suitable inputs exist for every ' + m(T`h>\ell`) + ' (A17).') +
        take('A separate example with ' + qm('h=2', 'moderate_h', '2') + ' gives a rise of similar size (' + q('moderate_entry_weak', '0.250') + ' → ' + q('moderate_entry_strong', '0.527') + '). Other inputs change too; this comparison does not isolate the effect of ' + m('h') + '.') +
        nav(back('main:scale')) });

    backup({ id: 'a20', label: 'A20', origin: 'f10b', targets: ['app:entry'], defines: ['tau', 'x_star', 'alpha', 'e_HL', 'E_O', 'r_C'], widget: '',
      title: 'How entry and ownership are computed', subtitle: '',
      body:
        '<p class="small">At ' + m('r_1') + ', full orders ' + m('(1,-1)') + ' and Laplace noise give:</p>' +
        d(T`\begin{gathered}\tau=\frac{c_H-g_L}{g_H-g_L}\quad\text{($c_H$ = expensive cost)},\qquad x^*=\frac b2\log\frac{\tau}{1-\tau},\qquad \alpha_\theta=\Pr(X\ge x^*\mid\theta)\\ e_H=\rho+(1-\rho)\alpha_H,\qquad e_L=\rho+(1-\rho)\alpha_L,\qquad \mathsf E=\frac{e_H+e_L}{2},\qquad \mathsf O_H=\frac{e_H}{2}\end{gathered}`) +
        ul([m(T`\tau`) + ' is the belief needed to cover ' + m('c_H') + '. ' + m(T`\alpha_\theta`) + ' is the chance of ' + m(T`X\ge x^*`) + ' given type ' + m(T`\theta`) + '. ' + m(T`\mathsf E`) + ' is preparation probability. Every prepared high-value challenger wins, so ' + m(T`\mathsf O_H=e_H/2`),
          'The high-cost window puts ' + m(T`\tau\in(1/2,M)`) + ' and ' + m(T`x^*\in(0,1)`) + '; ' + m(T`\alpha_H>\alpha_L`),
          'The benchmark ceiling is ' + qm(T`r_C\approx3.59`, 'base_r_high_cost_ceiling', '3.59') + '. As ' + m('r') + ' approaches ' + m('r_C') + ' from below, entry approaches ' + q('base_laplace_entry_ceiling_left_limit', '0.506') + '. Above that strength, ' + m(T`\tau>M`) + ', so high-cost preparation stops',
          'Expected target proceeds are ' + tx('table2_equilibrium_controls.tex', 'Weak incumbent ($r=1.2$)', 5, '0.393') + ' at ' + m('r_0') + ', ' + tx('table2_equilibrium_controls.tex', 'Strong incumbent ($r=3$)', 5, '0.872') + ' at ' + m('r_1') + ', and ' + tx('table2_equilibrium_controls.tex', 'Very strong incumbent ($r=3.6$)', 5, '0.664') + ' at ' + m('r_2')], 'small') +
        nav(back('main:entry')) });

    function certRow(letter, r, v, e, cover) {
      return '<tr><td>' + q('cert_' + letter + '_r', r) + '</td><td>' + qm(v, '-cert_' + letter + '_v_interval', v) + '</td><td>' + qm(e, 'cert_' + letter + '_entry_interval', e) + '</td><td>' + q('cert_' + letter + '_high_derivative_lower', cover) + '</td></tr>';
    }
    backup({ id: 'a21', label: 'A21', origin: 'f10b', targets: ['app:cert'], defines: [], widget: '',
      title: 'Which outcomes are unique, and which coexist?', subtitle: '',
      body:
        '<p class="small">Orders and entry at equilibrium prices are unique at the two strengths in the main comparison. At three intermediate strengths, informative trade and no trade coexist.</p>' +
        '<table class="t-enclosures"><thead><tr><th>' + m('r') + '</th><th>' + m(T`q_L\in`) + '</th><th>Entry ' + m(T`\mathsf E\in`) + '</th><th>' + m('H') + ' marginal profit ' + m(T`\ge`) + '</th></tr></thead><tbody>' +
          certRow('a', '1.55', T`[-0.46031620,\,-0.46031618]`, T`[0.5450528898,\,0.5450528922]`, '0.0000761777') +
          certRow('b', '1.60', T`[-0.70747539,\,-0.70747537]`, T`[0.5487563062,\,0.5487563085]`, '0.0027531948') +
          certRow('c', '1.65', T`[-0.90333201,\,-0.90333198]`, T`[0.5513607988,\,0.5513608020]`, '0.0054921767') +
        '</tbody></table>' +
        ul(['<b>After low value:</b> profit is strictly concave in sale size. Marginal profit changes sign inside each listed interval (' + q('cert_a_psi_left_lower', '0.000000000114') + ' and ' + qm('-0.000000000096', 'cert_a_psi_right_upper', '-0.000000000096') + ' at ' + qm('r=1.55', 'cert_a_r', '1.55') + ')',
          '<b>After high value:</b> marginal profit stays positive at every purchase size, for every order in the listed interval',
          '<b>The proof does not:</b> establish a unique informative equilibrium, rule out other equilibria with random investor orders, or connect these strengths with a continuous branch'], 'small') +
        nav(back('main:cert')) });

    function t2(row, a, b, c) {
      return '<td>' + tx('table2_equilibrium_controls.tex', row, 3, a) + '</td><td>' + tx('table2_equilibrium_controls.tex', row, 4, b) + '</td><td>' + tx('table2_equilibrium_controls.tex', row, 5, c) + '</td>';
    }
    backup({ id: 'a22', label: 'A22', origin: 'f11', targets: ['app:controls'], defines: [], widget: '',
      title: 'Information controls in detail', subtitle: '',
      body:
        ul(['Proposition A.3 holds the challenger\'s information and cost distribution fixed. A stronger incumbent then cannot raise entry. The fixed-order control holds investor orders constant',
          'Full orders are imposed at ' + m('r_0') + ': they lose in expectation because ' + m(T`\Delta_T(r_0)<k`) + '. At ' + m('r_1') + ', full orders are the equilibrium'], 'small') +
        '<table class="t-detail"><thead><tr><th></th><th>' + m('r') + '</th><th>Entry ' + m(T`\mathsf E`) + '</th><th>High-value ownership ' + m(T`\mathsf O_H`) + '</th><th>Target proceeds</th></tr></thead><tbody>' +
          '<tr><th><em>Equilibria of the feedback game</em></th><td>1.2</td>' + t2('Weak incumbent ($r=1.2$)', '0.250', '0.125', '0.393') + '</tr>' +
          '<tr><th></th><td>3</td>' + t2('Strong incumbent ($r=3$)', '0.523', '0.324', '0.872') + '</tr>' +
          '<tr><th></th><td>3.6</td>' + t2('Very strong incumbent ($r=3.6$)', '0.250', '0.125', '0.664') + '</tr>' +
          '<tr class="panel"><td colspan="5"><em>Frozen informative orders</em> (control, not an equilibrium at ' + m('r_0') + ')</td></tr>' +
          '<tr><th></th><td>1.2</td>' + t2('Frozen informative orders, $r=1.2$', '0.562', '0.351', '0.520') + '</tr>' +
          '<tr><th></th><td>3</td>' + t2('Frozen informative orders, $r=3$', '0.523', '0.324', '0.872') + '</tr>' +
          '<tr class="panel"><td colspan="5"><em>Price hidden from challenger</em> (equilibrium of the no-price-access game)</td></tr>' +
          '<tr><th></th><td>1.2</td>' + t2('Price hidden, $r=1.2$', '0.250', '0.125', '0.393') + '</tr>' +
          '<tr><th></th><td>3</td>' + t2('Price hidden, $r=3$', '0.250', '0.125', '0.615') + '</tr>' +
        '</tbody></table>' +
        gray('With the price hidden, the challenger prepares only at low cost. At ' + m('r_1') + ', the investor still trades full orders.') +
        nav(back('main:controls')) });

    backup({ id: 'a23', label: 'A23', origin: 'f11', targets: ['app:welfare'], defines: ['D_0'], widget: '',
      title: 'Price level or information?', subtitle: '',
      body:
        ul(['Add a fixed outside dividend ' + qm('D_0=0.257809', 'base_matched_dividend', '0.257809') + ' to the stock in the price-hidden economy. It raises the payoff and price equally, so investor profit and entry stay unchanged. Mean stock prices now match, but entry still differs.',
          'At ' + m('r_1') + ', extra entry occurs only when the expected auction gain covers preparation cost. Surplus also gains from sales that otherwise fail the reserve. Sale payments only move money between parties',
          'The added dividend does not change the auction and is excluded from surplus. This comparison does not rank incumbent strengths or sale rules'], 'roomy') +
        nav(back('main:welfare')) });

    backup({ id: 'a24', label: 'A24', origin: 'f12', targets: ['app:corr'], defines: ['r_PNU'], widget: 'x5a',
      title: 'Entry across incumbent strengths', subtitle: '',
      body:
        '<div class="figure wide" id="x5a" tabindex="0" aria-label="Figure X5, panel (a). Entry across incumbent strength: branches broken at unresolved nodes, certified intervals, uniqueness shading; arrow keys move the cursor."></div>' +
        gray('Black dots: proved equilibria; exact intervals in A21. Curves: computed candidates, with gaps where the search found none.') +
        '<p class="small">No trade is unique below ' + qm(T`r_P\approx1.22`, 'base_r_pool_unique_sufficient', '1.22') + '; it remains an equilibrium through ' + qm(T`r_N\approx1.75`, 'base_r_no_trade_exact', '1.75') + '. Full orders are unique above ' + qm(T`r_U\approx2.84`, 'base_r_full_unique_sufficient', '2.84') + '. High-cost preparation is impossible above ' + qm(T`r_C\approx3.59`, 'base_r_high_cost_ceiling', '3.59') + '. Shading marks the unique ranges. The full equilibrium set at intermediate strengths remains open.</p>' +
        nav(go('app:corrb', 'Order sizes'), back('main:corr')) });

    backup({ id: 'a25', label: 'A25', origin: 'a24', targets: ['app:corrb'], defines: [], widget: 'x5b',
      title: 'Investor orders across incumbent strengths', subtitle: '',
      body:
        '<div class="figure wide" id="x5b" tabindex="0" aria-label="Figure X5, panel (b). Order magnitudes across incumbent strength; arrow keys move the cursor."></div>' +
        gray('Black dots: proved equilibria; exact intervals in A21. Curves: computed candidates, with gaps where the search found none. Triangles show possible orders in a random-order candidate.') +
        '<p class="small">No trade uses ' + m('(0,0)') + '. At the three proved strengths, sale sizes are ' + m(T`|q_L|\approx`) + q('cert_a_v_interval', '0.460') + ', ' + q('cert_b_v_interval', '0.707') + ', ' + q('cert_c_v_interval', '0.903') + '. The proof does not establish a branch between these points or the mixed-order candidate.</p>' +
        nav(back('app:corr')) });

    function t3(row, cells) {
      return cells.map(function (c) { return '<td>' + tx('table3_extensions.tex', row, c[0], c[1]) + '</td>'; }).join('');
    }
    backup({ id: 'a26', label: 'A26', origin: 'f13', targets: ['app:robust'], defines: [], widget: '',
      title: 'Entry and ownership under model changes', subtitle: '',
      body:
        '<table class="t-full"><thead><tr><th></th><th>' + m(T`\rho`) + '; strengths</th><th>' + m(T`\mathsf E`) + ' weak</th><th>' + m(T`\mathsf E`) + ' strong</th><th>Change (pp)</th><th>' + m(T`\mathsf O_H`) + ' weak</th><th>' + m(T`\mathsf O_H`) + ' strong</th></tr></thead><tbody>' +
          '<tr><th>Laplace, two cost levels</th><td>' + q('base_rho', '0.25') + '; ' + q('base_r_weak', '1.2') + '→' + q('base_r_strong', '3') + '</td>' + t3('Laplace, cost atoms', [[1, '0.250'], [2, '0.523']]) + '<td>' + q('base_entry_change_pp', '27.28') + '</td>' + t3('Laplace, cost atoms', [[4, '0.125'], [5, '0.324']]) + '</tr>' +
          '<tr><th>Laplace, continuous costs</th><td>0.25; 1.2→3</td>' + t3('Laplace, cost mixture', [[1, '0.250']]) + '<td>' + q('cost_mix_laplace_entry_strong', '0.523') + '</td>' + t3('Laplace, cost mixture', [[3, '27.27'], [4, '0.125'], [5, '0.324']]) + '</tr>' +
          '<tr><th>Logistic, two cost levels</th><td>0.25; 1.2→3</td>' + t3('logistic, cost atoms', [[1, '0.250']]) + '<td>' + q('logistic_entry_strong', '0.302') + '</td>' + t3('logistic, cost atoms', [[3, '5.15'], [4, '0.125'], [5, '0.162']]) + '</tr>' +
          '<tr><th>Logistic, continuous costs</th><td>0.25; 1.2→3</td>' + t3('logistic, cost mixture', [[1, '0.250']]) + '<td>' + q('cost_mix_logistic_entry_strong', '0.301') + '</td>' + t3('logistic, cost mixture', [[3, '5.14'], [4, '0.125'], [5, '0.162']]) + '</tr>' +
          '<tr><th>Smaller value gap (' + m('h=2') + ')</th><td>' + q('moderate_rho', '0.25') + '; ' + q('moderate_r_weak', '1.05') + '→' + q('moderate_r_strong', '1.5') + '</td><td>' + q('moderate_entry_weak', '0.250') + '</td><td>' + q('moderate_entry_strong', '0.527') + '</td><td>' + q('moderate_entry_change_pp', '27.68') + '</td>' + t3('Moderate values', [[4, '0.125'], [5, '0.327']]) + '</tr>' +
          '<tr><th>Signals (' + m('a=0.70') + ', ' + m('d=0.75') + ')</th><td>' + q('signal_rho', '0.85') + '; ' + q('signal_r_weak', '1.1') + '→' + q('signal_r_strong', '2.3') + '</td><td>' + q('signal_entry_weak', '0.850') + '</td><td>' + q('signal_entry_strong', '0.879') + '</td><td>' + q('signal_entry_change_pp', '2.94') + '</td>' + t3('$a=0.70$, $d=0.75$', [[4, '0.425'], [5, '0.449']]) + '</tr>' +
        '</tbody></table>' +
        ul(['Smallest positive gaps in the theorem conditions: benchmark ' + qm(T`2.41\times10^{-3}`, 'base_minimum_theorem_margin', T`2.41\times10^{-3}`) + ', smaller gap ' + qm(T`8.01\times10^{-4}`, 'moderate_minimum_theorem_margin', T`8.01\times10^{-4}`) + ', signals ' + qm(T`1.45\times10^{-3}`, 'signal_minimum_theorem_margin', T`1.45\times10^{-3}`),
          'Each row uses its own inputs. ' + m(T`\mathsf E`) + ' is preparation probability; ' + m(T`\mathsf O_H`) + ' is high-value ownership probability. Percentage-point changes use unrounded values'], 'small') +
        take('The rise from ' + m('r_0') + ' to ' + m('r_1') + ' holds in every row; the ' + m('r_2') + ' fall is shown for the benchmark only.') +
        nav(back('main:robust')) });

    function t4(row, cells) {
      return cells.map(function (c) { return '<td>' + (c[2] ? q(c[2], c[1]) : tx('table4_reserve_comparisons.tex', row, c[0], c[1])) + '</td>'; }).join('');
    }
    var PB = 'Panel B:';
    backup({ id: 'a27', label: 'A27', origin: 'f14', targets: ['app:reserve'], defines: ['eps_V'], widget: '',
      title: 'A higher reserve can raise proceeds; the best reserve is unknown', subtitle: '',
      body:
        '<p class="small">Values are uniform around the low and high class centers: compare ' + qm('p=0.5', 'base_p', '0.5') + ' vs ' + qm('p=1.1', 'value_reserve_high', '1.1') + ' (class half-width ' + qm(T`\varepsilon_V=0.05`, 'value_band_halfwidth', '0.05') + '). A bid is admissible if it meets the reserve.</p>' +
        '<table class="t-reserve"><thead><tr><th>Economy, reserve</th><th>Preparation</th><th>Sale</th><th>Two admissible bidders</th><th>Expected proceeds</th><th>Trading</th></tr></thead><tbody>' +
          '<tr><th>Weak ' + m('r=1.2') + ', ' + m('p=0.5') + '</th>' + t4(PB + 'Weak ($r=1.2$), $p=0.5$', [[1, '0.250'], [2, '0.688'], [3, '0.146'], [4, '0.393', 'value_revenue_weak_low_p']]) + '<td>no trade</td></tr>' +
          '<tr><th>Weak ' + m('r=1.2') + ', ' + m('p=1.1') + '</th>' + t4(PB + 'Weak ($r=1.2$), $p=1.1$', [[1, '0.540', 'value_entry_weak_high_p'], [2, '0.392'], [3, '0.0280'], [4, '0.432', 'value_revenue_weak_high_p']]) + '<td>full orders</td></tr>' +
          '<tr><th>Strong ' + m('r=3') + ', ' + m('p=0.5') + '</th>' + t4(PB + 'Strong ($r=3$), $p=0.5$', [[1, '0.523'], [2, '0.920'], [3, '0.436'], [4, '0.872', 'value_revenue_strong_low_p']]) + '<td>full orders</td></tr>' +
          '<tr><th>Strong ' + m('r=3') + ', ' + m('p=1.1') + '</th>' + t4(PB + 'Strong ($r=3$), $p=1.1$', [[1, '0.512', 'value_entry_strong_high_p'], [2, '0.749'], [3, '0.200'], [4, '1.01', 'value_revenue_strong_high_p']]) + '<td>full orders</td></tr>' +
        '</tbody></table>' +
        '<p class="grayline">The analogous comparison for binary values uses reserves ' + qm('p=0.5', 'base_p', '0.5') + ' and ' + tx('table4_reserve_comparisons.tex', 'Panel A:Weak ($r=1.2$), $p=1.01$', 0, '1.01', null, 'p=1.01') + '.</p>' +
        ul(['Preparation can rise while the chances of a sale and two admissible bids fall']) +
        take('The higher reserve raises proceeds in these cases. The best reserve remains unknown.') +
        nav(go('app:pool', 'Same orders, different prices'), back('main:reserve')) });

    backup({ id: 'a28', label: 'A28', origin: 'a27', targets: ['app:pool'], defines: ['kappa'], widget: '',
      title: 'Same orders, different prices', subtitle: '',
      body:
        '<p class="small">Proposition A.10: at reserve ' + qm('p=7', 'pool_reserve', '7') + ' and strength ' + m('r_0') + ', each cutoff ' + m(T`\kappa\in[-\log2,\,0]`) + ' gives an equilibrium with orders ' + m('(1,-1)') + '. All flows ' + m(T`X<\kappa`) + ' receive price zero.</p>' +
        '<table class="t-pool"><thead><tr><th></th><th>' + m(T`\kappa=-\log2`) + '</th><th>' + m(T`\kappa=0`) + '</th></tr></thead><tbody>' +
          '<tr><th>Belief at price zero</th><td>' + q('pool_posterior_cutoff_low', '0.273') + '</td><td>' + q('pool_posterior_cutoff_high', '0.303') + '</td></tr>' +
          '<tr><th>Entry</th><td>' + q('pool_entry_cutoff_low', '0.152') + '</td><td>' + q('pool_entry_cutoff_high', '0.125') + '</td></tr>' +
          '<tr><th>Expected target proceeds</th><td>' + q('pool_revenue_cutoff_low', '0.687') + '</td><td>' + q('pool_revenue_cutoff_high', '0.610') + '</td></tr>' +
        '</tbody></table>' +
        ul(['The orders stay fixed, but the price rule, beliefs and entry change', 'The benchmark\'s positive entry floor rules out this pool of flow beliefs']) +
        take('To choose a reserve, the seller must compare complete price and entry rules. Investor orders alone do not determine the outcome.') +
        nav(back('app:reserve')) });

    var REFS = [
      ['Betton, Eckbo, Thompson and Thorburn (2014). <em>J. Finance</em> 69.', 'Boone and Mulherin (2007). <em>J. Finance</em> 62.', 'Bulow, Huang and Klemperer (1999). <em>J. Polit. Econ.</em> 107.',
        'Carlin, Liu, Officer, Pernoud and Tu (2026). NBER Working Paper 34846.', 'Cornelli and Li (2002). <em>Rev. Financ. Stud.</em> 15.', 'Dow, Goldstein and Guembel (2017). <em>J. Eur. Econ. Assoc.</em> 15.',
        'Edmans, Goldstein and Jiang (2012). <em>J. Finance</em> 67.', 'Edmans, Goldstein and Jiang (2015). <em>Amer. Econ. Rev.</em> 105.', 'Fishman (1988). <em>RAND J. Econ.</em> 19.'],
      ['Gentry and Stroup (2019). <em>J. Financ. Econ.</em> 132.', 'Goldstein and Guembel (2008). <em>Rev. Econ. Stud.</em> 75.', 'Gorbenko and Malenko (2014). <em>J. Finance</em> 69.', 'Grossman and Hart (1980). <em>Bell J. Econ.</em> 11.',
        'Hirshleifer and Png (1989). <em>Rev. Financ. Stud.</em> 2.', 'Imprivata, Inc. (2016). Definitive merger proxy, Form DEFM14A.', 'Levin and Smith (1994). <em>Amer. Econ. Rev.</em> 84.',
        'Lin, Ma, Yang and Zhu (2025). Working paper.', 'Liu and Bernhardt (2022). Working paper.', 'Luo (2005). <em>J. Finance</em> 60.', 'Pernoud and Gleyze (2026). Working paper.',
        'Persico (2000). <em>Econometrica</em> 68.', 'Roberts and Sweeting (2013). <em>Amer. Econ. Rev.</em> 103.',
        'Samuelson (1985). <em>Econ. Lett.</em> 17.', 'Schwert (1996). <em>J. Financ. Econ.</em> 41.']
    ];
    backup({ id: 'a29', label: 'A29', origin: 'f3', targets: ['app:refs'], defines: [], widget: '',
      title: 'References', subtitle: '',
      body: '<div class="refs">' + REFS.map(function (col) { return '<ul>' + col.map(function (r) { return '<li>' + r + '</li>'; }).join('') + '</ul>'; }).join('') + '</div>' + nav(back('main:refs')) });

    /* ================================================================ notation (A12 and the G panel) */
    /* Rows of the A12 table in talk.tex, in the order the symbols are introduced. One source feeds
       the A12 slide and the notation panel. */
    var notation = [
      [[m('R') + '; ' + m('r'), 'incumbent value ' + m(T`R\sim U[0,r]`) + '; ' + m('r') + ' = incumbent strength'],
        [m(T`\theta\in\{H,L\}`) + '; ' + m(T`h,\ell`), 'challenger type; value ' + m('h') + ' or ' + m(T`\ell`)],
        [m('p'), 'reserve price (not the stock price)'],
        [m('C') + '; ' + m('c_L,c_H') + '; ' + m(T`\rho`), 'preparation cost; low and high levels; ' + m(T`\rho=\Pr(C=c_L)`)],
        [m('t_H,t_L'), 'expected target proceeds when a high / low-value challenger enters'],
        [m(T`\Delta_T`), 'target-payoff spread ' + m('t_H-t_L')],
        [m('g_H,g_L'), 'expected auction profit before preparation cost, for each value']],
      [[m('r_0,r_1'), 'weak, strong incumbent'],
        [m(T`\mu`), 'probability of high value after the price: ' + m(T`\Pr(\theta=H\mid P)`)],
        [m('m,M'), 'bounds on ' + m(T`\mu`) + ': ' + m('m=1/(1+e^{2/b})') + ', ' + m('M=1-m')],
        [m('b'), 'Laplace noise scale; ' + m('b>1')],
        [m('k'), 'trading cost per unit'],
        [m('(q_H,q_L)'), 'orders after a high / low challenger value'],
        [m(T`B_r(\mu)`), 'challenger\'s expected gross profit at belief ' + m(T`\mu`)],
        [m('r_2'), 'stronger still incumbent']]
    ];

    /* Every symbol the slides use, with the pattern that finds it in a slide's LaTeX. The check
       fails if a symbol appears before the frame that defines it (frames in deck order). */
    var glossary = [
      { key: 'R', pattern: T`(^|[^\\a-zA-Z_^])R(?![a-zA-Z])` }, { key: 'r', pattern: T`(^|[^\\a-zA-Z_^])r(?![a-zA-Z_])` },
      { key: 'theta', pattern: T`\\theta` }, { key: 'h', pattern: T`(^|[^\\a-zA-Z_^])h(?![a-zA-Z])` }, { key: 'ell', pattern: T`\\ell` },
      { key: 'p', pattern: T`(^|[^\\a-zA-Z_^])p(?![a-zA-Z])` }, { key: 'C', pattern: T`(^|[^\\a-zA-Z_^])C(?![a-zA-Z])` },
      { key: 'c_L', pattern: 'c_L' }, { key: 'c_H', pattern: 'c_H' }, { key: 'rho', pattern: T`\\rho` },
      { key: 'Delta_T', pattern: T`\\Delta_T` }, { key: 't_theta', pattern: T`t_(H|L|\\theta)` }, { key: 'g_HL', pattern: 'g_(H|L)' },
      { key: 'r_01', pattern: 'r_[01]' }, { key: 'mu', pattern: T`\\mu(?!_)` }, { key: 'm_M', pattern: T`(^|[^\\a-zA-Z_^])[mM](?![a-zA-Z])` },
      { key: 'b', pattern: T`(^|[^\\a-zA-Z_^])b(?![a-zA-Z])` }, { key: 'k', pattern: T`(^|[^\\a-zA-Z_^])k(?![a-zA-Z])` },
      { key: 'q_HL', pattern: 'q_(H|L)' }, { key: 'B', pattern: 'B_' }, { key: 'r_2', pattern: 'r_2' },
      { key: 'a_d', pattern: T`(^|[^\\a-zA-Z_^])[ad]=` }, { key: 'TY', pattern: T`(^|[^\\a-zA-Z_^])(T|Y)(?![a-zA-Z_])` },
      { key: 'P', pattern: T`(^|[^\\a-zA-Z_^])P(?![a-zA-Z])` }, { key: 'e_HL', pattern: 'e_(H|L)' }, { key: 'sigma', pattern: T`\\sigma` },
      { key: 'q', pattern: T`(^|[^\\a-zA-Z_^])q(?![a-zA-Z_])` }, { key: 'X_Z', pattern: T`(^|[^\\a-zA-Z_^])(X|Z)(?![a-zA-Z])` },
      { key: 't_0', pattern: 't_0' }, { key: 'F_rbar', pattern: T`\\bar r|(^|[^\\a-zA-Z_^])F(?![a-zA-Z])` }, { key: 'eta', pattern: T`\\eta` },
      { key: 'U_Pi', pattern: T`U_\\theta|\\Pi` }, { key: 'mu_X', pattern: T`\\mu_X` }, { key: 'f', pattern: T`(^|[^\\a-zA-Z_^])f(?![a-zA-Z])` },
      { key: 'x_star', pattern: T`x\^\*` }, { key: 'eps_C', pattern: T`\\varepsilon_C` }, { key: 'alpha', pattern: T`\\alpha` },
      { key: 'tau', pattern: T`\\tau` }, { key: 'E_O', pattern: T`\\mathsf (E|O)` }, { key: 'r_C', pattern: 'r_C' },
      { key: 'D_0', pattern: 'D_0' }, { key: 'r_PNU', pattern: 'r_(P|N|U)' }, { key: 'eps_V', pattern: T`\\varepsilon_V` },
      { key: 'kappa', pattern: T`\\kappa` }
    ];

    return { frames: F, glossary: glossary, notation: notation };
  }

  if (typeof window !== 'undefined') window.createDeck = createDeck;
})();
