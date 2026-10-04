/* content.js: the 47 frames of talk/talk.tex as web slides, in the Beamer order.
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

    frame({ id: 'f1', label: 'F1', num: '1', part: 1, minutes: 2.0, targets: ['main:interval', 'main:evidence'], defines: [], widget: '',
      title: 'Does a stronger incumbent keep the challenger out?',
      subtitle: 'The decision interval this paper is about',
      body:
        '<div class="flow flow-3">' +
          '<div class="box" data-step="1">Approach or review disclosed</div><span class="arrow" data-step="2" aria-hidden="true">→</span>' +
          '<div class="box" data-step="2">Target stock keeps trading</div><span class="arrow" data-step="3" aria-hidden="true">→</span>' +
          '<div class="box box-cost" data-step="3">Challenger decides whether to pay to prepare</div>' +
        '</div>' +
        ul([[4, 'The <b>incumbent</b> bidder is already prepared; the market knows how strong it is, not what it will bid'],
          [4, 'A <b>challenger</b> must first pay to prepare an executable bid (diligence, financing, approvals); paying is <b>entry</b>'],
          [4, '<b>Received answer:</b> a stronger rival lowers what preparation earns, so it deters entry ' + cite('Fishman 1988; Hirshleifer and Png 1989')],
          [4, '<b>But</b> the challenger decides while the stock trades, and it can watch the price']], 'small') +
        '<p class="grayline small-note" data-step="4">Imprivata\'s 2016 proxy separates an unsolicited approach, outreach to potential buyers, and indications of interest conditional on further diligence: a costly preparation stage, not a price drawing anyone in</p>' +
        take(key('The twist:') + ' what that price reveals depends on how strong the incumbent is', 5) +
        nav(go('app:interval', 'Which deals fit'), go('app:evidence', 'Evidence: a design')) });

    frame({ id: 'f2', label: 'F2', num: '2', part: 1, minutes: 2.0, targets: [], defines: [], widget: '',
      title: 'This paper', subtitle: '',
      body:
        '<p class="lead">An informed investor trades the target\'s stock, which pays off from the sale price, before a challenger decides whether to pay to prepare a takeover bid; prices are rational, and trading and entry are solved in equilibrium.</p>' +
        ul([[0, key('Competition creates competition') + ': a stronger incumbent can turn an uninformative stock price into an informative one and raise entry' +
              '<span class="bench">Benchmark: entry <b>' + q('base_entry_weak', '0.250') + ' → ' + q('base_entry_strong', '0.523') + '</b> while the challenger\'s profit before any news falls <b>' + q('base_profit_prior_weak', '4.80') + ' → ' + q('base_profit_prior_strong', '4.29') + '</b></span>'],
          [1, '<b>Two possible outcomes of one auction</b>: a strong incumbent can beat a low-value challenger but not a high-value one, so the challenger keeps less while the sale price depends more on who shows up; informed trading puts that into the stock price, and good news justifies expensive preparation'],
          [2, '<b>Information is the channel:</b> hold fixed what the price reveals, and a stronger incumbent cannot raise entry, as the textbook says ' + st('(sign analytical, Prop. A.3)')]], 'claims') +
        take('<b>Implication:</b> when the target trades, a stronger rival is not a pure deterrent, because who competes depends on what the price reveals before anyone prepares.', 3) });

    frame({ id: 'f3', label: 'F3', num: '3', part: 1, minutes: 0.75, targets: ['main:lit', 'main:refs'], defines: [], widget: '',
      title: 'What is new relative to learning from prices',
      subtitle: 'Four closest antecedents',
      body:
        ul([[0, '<b>Prices guide real decisions</b> ' + cite('Dow, Goldstein and Guembel 2017; Edmans, Goldstein and Jiang 2015') + ': here the sale rule splits one surplus into a traded claim and the challenger\'s claim, and competition moves them in opposite directions'],
          [1, '<b>Stronger incumbents deter</b> ' + cite('Fishman 1988') + ': kept intact; I add a market that trades before preparation'],
          [2, '<b>Auction entry is endogenous</b> ' + cite('Levin and Smith 1994') + ': here entry responds to what the price reveals']], 'roomy') +
        take('Increment: one sale rule moves the two claims oppositely, producing the entry reversal.', 3) +
        nav(go('app:lit', 'Related work'), go('app:refs', 'References')) });

    frame({ id: 'f4', label: 'F4', num: '4', part: 2, minutes: 2.75, targets: ['main:omit', 'main:info', 'main:eq'],
      defines: ['R', 'r', 'theta', 'h', 'ell', 'p', 'C', 'c_L', 'c_H', 'rho'], widget: 'infosets',
      title: 'Model: who moves, who knows what, and when',
      subtitle: 'The challenger sees the price and its own cost, never the order flow, ' + m(T`\theta`) + ' or ' + m(T`R`),
      body:
        '<div class="timeline" role="group" aria-label="Timeline; select a step to see its information set">' +
          '<button type="button" class="tl" data-info="seller"><span class="tl-n">1</span><b>Seller</b>commits to a cash second-price auction, reserve ' + m('p') + '</button>' +
          '<button type="button" class="tl" data-info="investor"><span class="tl-n">2</span><b>Investor</b>knows ' + m(T`\theta`) + '; trades the target\'s stock against noise traders</button>' +
          '<button type="button" class="tl" data-info="makers"><span class="tl-n">3</span><b>Market makers</b>see only total order flow; price the share at expected sale proceeds</button>' +
          '<button type="button" class="tl tl-cost" data-info="challenger"><span class="tl-n">4</span><b>Challenger</b>sees the price and its cost ' + m('C') + '; entry ' + m('=') + ' pay ' + m('C') + ', learn ' + m(T`\theta`) + ', can bid</button>' +
          '<button type="button" class="tl" data-info="bidders"><span class="tl-n">5</span><b>Bidders</b>incumbent value ' + m(T`R\sim U[0,r]`) + '; challenger worth ' + m('h') + ' or ' + m(T`\ell`) + '; bid truthfully</button>' +
        '</div>' +
        '<p class="infoset" id="f4-infoset" aria-live="polite">Select a step to see what that agent observes.</p>' +
        ul([m(T`0<p<\ell<r<h`) + ' (' + m('p') + ' = reserve, not the stock price): the incumbent can beat a low-value challenger, never a high-value one. Strength ' + m('r') + ' is public; only the incumbent knows its value ' + m('R') + '. Quality ' + m(T`\theta\in\{H,L\}`) + ' (worth ' + m('h') + ' or ' + m(T`\ell`) + '), equally likely, learned only by preparing.',
          cost('<b>Cost:</b> preparation cost ' + m(T`C\in\{c_L,c_H\}`) + ', ' + m(T`\Pr(C=c_L)=\rho`) + ', independent of ' + m(T`\theta`) + ' (cheap / expensive preparation)')], 'small') +
        nav(go('app:omit', 'What is left out'), go('app:info', 'Why would the investor know?'), go('app:eq', 'Equilibrium')) });

    frame({ id: 'f5', label: 'F5', num: '5', part: 3, minutes: 2.5, targets: ['main:payoffs', 'main:payrule'],
      defines: ['Delta_T', 't_theta', 'g_HL', 'F_rbar'], widget: 'cases',
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
          '<div>' + m(T`g_H=\mathbb{E}[(h-\max\{p,R\})_+]`) + ' <span class="arrowword">↓</span><span class="gloss">challenger\'s gross profit (' + m('g_L') + ' likewise)</span></div>' +
        '</div>' +
        gray(m(T`t_\theta`) + ' = expected target proceeds when a ' + m(T`\theta`) + '-challenger enters. Proposition 1 (analytical): both signs hold weakly for any first-order strengthening, ' + m(T`R\sim F`) + ' on ' + m(T`[0,\bar r]`) + ', ' + m(T`\ell<\bar r<h`) + ' (strictly in the uniform benchmark, ' + m(T`\bar r=r`) + ').') +
        take('One shift, opposite signs: challenger keeps less; target proceeds depend more on who it is.', 2) +
        nav(go('app:payoffs', 'Closed forms'), go('app:payrule', 'Other payment rules')) });

    frame({ id: 'f6', label: 'F6', num: '6', part: 3, minutes: 1.5, targets: [], defines: ['r_01'], widget: 'x1',
      title: 'A stronger incumbent: spread up, profit down',
      subtitle: 'Declared benchmark; weak ' + qm('r_0=1.2', 'base_r_weak', '1.2') + ', strong ' + qm('r_1=3', 'base_r_strong', '3') + '; auction-stage payoffs, before trading and entry',
      body:
        '<div class="figure" id="x1" tabindex="0" aria-label="Figure X1. Target-payoff spread and challenger profit at the prior against incumbent strength; arrow keys move the cursor."></div>' +
        '<p class="status-right">' + st('analytical (Proposition 1)') + '</p>' +
        take('From ' + m('r_0') + ' to ' + m('r_1') + ' the ' + info('spread') + ' rises ' + q('base_spread_weak', '0.0167') + ' → ' + q('base_spread_strong', '0.667') + ' while profit at the prior (before any news) falls ' + q('base_profit_prior_weak', '4.80') + ' → ' + q('base_profit_prior_strong', '4.29') + ': deterrence at every fixed belief, and more for the stock to reveal.') });

    frame({ id: 'f7', label: 'F7', num: '7', part: 4, minutes: 3.0, targets: ['main:bound', 'main:orders', 'main:notation'],
      defines: ['mu', 'm_M', 'b', 'k', 'q_HL'], widget: '',
      title: 'Trading pays only against a strong incumbent',
      subtitle: 'Orders ' + m(T`(q_H,q_L)\in[-1,1]`) + ' after a high / low challenger value; trading cost ' + m('k') + ' per unit; prices anticipate entry',
      body:
        '<p class="small">The price reveals the market\'s belief ' + m(T`\mu=\Pr(H)`) + ', kept by noise within ' + m('[m,M]') + ': ' + qm(T`m=1/(1+e^{2/b})\approx0.27`, 'base_m', '0.27') + ', ' + H.qk(m('M=1-m'), 'base_M') + ' (Laplace noise, scale ' + qm('b=2', 'base_b', '2') + ')</p>' +
        '<p class="small"><b>Residual advantage</b> = what the investor knows a share pays minus its price; entry ' + m(T`\ge\rho`) + ' because cheap preparation pays after any price (the low-cost floor, next frame).</p>' +
        '<table class="t-factors"><tbody><tr><td>Residual advantage per unit ' + m('=') + '</td>' +
          '<td data-step="1">entry probability<br>' + m(T`(\ge\rho)`) + '</td><td data-step="2">' + m(T`\times`) + '</td>' +
          '<td data-step="2" class="info">target-payoff spread ' + m(T`\Delta_T`) + '</td><td data-step="3">' + m(T`\times`) + '</td>' +
          '<td data-step="3">market\'s remaining uncertainty ' + m(T`(\ge m)`) + '</td></tr></tbody></table>' +
        '<p class="center" data-step="3">' + m(T`\rho\,m\,\Delta_T\ \le\ \text{advantage}\ \le\ \Delta_T`) + '</p>' +
        ul([[4, '<b>Weak ' + qm('r_0=1.2', 'base_r_weak', '1.2') + ':</b> advantage ' + qm(T`\le\Delta_T(r_0)=0.0167`, 'base_spread_weak', '0.0167') + qm('{}<k=0.02', 'base_k', '0.02') + ', so every order loses; no trade ' + m('(0,0)')],
          [5, '<b>Strong ' + qm('r_1=3', 'base_r_strong', '3') + ':</b> each extra unit earns ' + qm(T`\ge(1-1/b)\,\rho m\Delta_T(r_1)=0.0224>k`, 'base_k+base_margin_strong_trade', '0.0224') + ', so full orders ' + m('(1,-1)')]], 'small') +
        '<div class="grayline" data-step="6"><button type="button" class="toggle-line" aria-expanded="false" data-toggle="f7-arith">' + info('<b>Trading-cost window</b>') + ' ' + m(T`\Delta_T(r_0)<k<(1-1/b)\,\rho m\Delta_T(r_1)`) + ' (analytical)</button>' +
          '<span id="f7-arith" hidden>: with ' + qm(T`\rho=0.25`, 'base_rho', '0.25') + ', ' + qm(T`(1-1/2)\times0.25\times m\times0.667=0.0224`, 'base_k+base_margin_strong_trade', '0.0224') + ' ' + m('=k+{}') + 'theorem margin ' + q('base_margin_strong_trade', '0.00241') + '.</span></div>' +
        take('The same shift that lowers the challenger\'s profit switches informed trading on.', 6) +
        nav(go('app:bound', 'Global trading bound'), go('app:orders', 'Orders, units, costs'), go('app:notation', 'Notation')) });

    frame({ id: 'f8', label: 'F8', num: '8', part: 4, minutes: 2.25, targets: ['main:suff', 'main:laplace', 'main:floor'],
      defines: ['B', 'r_2'], widget: 'x2',
      title: 'Only good news makes expensive preparation pay',
      subtitle: m(T`B_r(\mu)=g_L+\mu(g_H-g_L)`) + ' at the worst, prior and best belief a price induces; ' + qm('c_L=1', 'base_c_low', '1') + ' (prob. ' + qm(T`\rho=0.25`, 'base_rho', '0.25') + '), ' + qm('c_H=6', 'base_c_high', '6'),
      body:
        '<div class="split">' +
          '<div class="col">' +
            '<div class="figure" id="x2" aria-label="Figure X2. Challenger profit at the worst, prior and best belief against incumbent strength, with the two cost lines."></div>' +
            '<div class="slider"><label for="x2-r">incumbent strength ' + m('r') + '</label><input type="range" id="x2-r" min="1.05" max="3.8" step="0.01" value="3"><output id="x2-r-value" for="x2-r">3.00</output></div>' +
            '<div id="x2-readout" class="readout" aria-live="polite"></div>' +
          '</div>' +
          '<div class="col text">' +
            '<p data-step="1">' + cost('<b>Low-cost floor</b>') + ' ' + m(T`c_L<B_{r_1}(m)`) + ': a cheap challenger enters after any price, so entry ' + m(T`\ge\rho`) + ' (the bound used on the previous frame)</p>' +
            '<p data-step="2">' + cost('<b>High-cost window</b>') + ' ' + qm(T`B_{r_0}(1/2)=4.80<c_H=6<B_{r_1}(M)`, [['base_profit_prior_weak', '4.80'], ['base_c_high', '6']]) + ': the expensive challenger stays out at the weak prior and enters after the best news against ' + m('r_1') + '. Beyond a ceiling strength, even the best price falls short (' + m('r_2') + ')</p>' +
            '<p class="status-line">' + st('analytical (Props. A.1, A.2, A.4); costs are inputs') + '</p>' +
          '</div>' +
        '</div>' +
        nav(go('app:suff', 'Reading the price'), go('app:laplace', 'Why Laplace noise'), go('app:floor', 'Is the floor doing the work?')) });

    frame({ id: 'f9', label: 'F9', num: '9', part: 5, minutes: 2.5, targets: ['main:proof', 'main:margins', 'main:forces'], defines: ['q'], widget: '',
      title: 'Proposition 2: a stronger incumbent can raise entry',
      subtitle: 'Weak ' + m('r_0') + ', strong ' + m('r_1') + ', stronger still ' + m('r_2') + '; all other primitives equal',
      body:
        '<div class="resultbox"><p class="resultbox-title">Proposition 2 (analytical), under the three conditions below</p>' +
          '<p class="propitem" data-step="0"><span class="propnum">(i)</span><b>Weak ' + m('r_0') + ':</b> unique outcome no trade, ' + m('(q_H,q_L)=(0,0)') + '; the price is uninformative; entry ' + m(T`=\rho`) + '</p>' +
          '<p class="propitem" data-step="1"><span class="propnum">(ii)</span><b>Strong ' + m('r_1') + ':</b> unique outcome full orders ' + m('(1,-1)') + '; the price is informative; entry ' + m(T`>\rho`) + '; a high-value challenger acquires the target more often</p>' +
          '<p class="propitem" data-step="2"><span class="propnum">(iii)</span><b>Stronger still, ' + m('r_2') + ',</b> where the low-cost floor and profitable trading persist but ' + m(T`B_{r_2}(M)<c_H`) + ': full orders, entry back to ' + m(T`\rho`) + '</p>' +
        '</div>' +
        '<div class="split narrow" data-step="3">' +
          '<table class="t-conditions"><tbody>' +
            '<tr><td>' + cost('<b>Low-cost floor</b>') + '</td><td>' + m(T`c_L<B_{r_1}(m)`) + '</td></tr>' +
            '<tr><td>' + cost('<b>High-cost window</b>') + '</td><td>' + m(T`B_{r_0}(1/2)<c_H<B_{r_1}(M)`) + '</td></tr>' +
            '<tr><td>' + info('<b>Trading-cost window</b>') + '</td><td>' + m(T`\Delta_T(r_0)<k<(1-1/b)\,\rho m\Delta_T(r_1)`) + '</td></tr>' +
          '</tbody></table>' +
          '<p class="grayline">(i)–(ii) on a nonempty open set of primitives, every ' + m(T`h>\ell`) + '; (iii) at the benchmark and nearby. Uniqueness: arbitrary mixed orders; every unilateral deviation ' + m(T`q\in[-1,1]`) + '.</p>' +
        '</div>' +
        take(info('wider ' + m(T`\Delta_T`) + ' → informed trading pays → informative price → good news clears ' + m('c_H') + ' → the expensive challenger enters'), 4) +
        nav(go('app:proof', 'Proof logic'), go('app:margins', 'Margins'), go('app:forces', 'Two forces side by side')) });

    function benchmarkTable(withR2) {
      var c = function (s) { return withR2 ? s : ''; };
      return '<p class="small-note">Entry = Pr(challenger prepares); entry ' + qm(T`\rho=0.25`, 'base_rho', '0.25') + ' = only the cheap challenger enters; high-value challenger ownership = Pr(high-value challenger acquires the target)</p>' +
        '<table class="t-bench' + (withR2 ? ' with-r2' : '') + '"><thead><tr><th></th>' +
          '<th>weak<br>' + qm('r_0=1.2', 'base_r_weak', '1.2') + '</th><th class="strong">strong<br>' + qm(T`\boldsymbol{r_1=3}`, 'base_r_strong', '3') + '</th>' +
          c('<th>stronger still<br>' + qm('r_2=3.6', 'base_r_collapse', '3.6') + '</th>') + '</tr></thead><tbody>' +
          '<tr data-step="1"><th>Challenger\'s profit at the prior ' + m('B_r(1/2)') + '</th><td>' + q('base_profit_prior_weak', '4.80') + '</td><td class="strong">' + q('base_profit_prior_strong', '4.29') + '</td>' + c('<td class="words">lower still</td>') + '</tr>' +
          '<tr data-step="1"><th>' + info('Target-payoff spread ' + m(T`\Delta_T`)) + '</th><td>' + q('base_spread_weak', '0.0167') + '</td><td class="strong">' + q('base_spread_strong', '0.667') + '</td>' + c('<td class="words">wider still</td>') + '</tr>' +
          '<tr data-step="2"><th>Investor orders ' + m('(q_H,q_L)') + '</th><td>' + m('(0,0)') + '</td><td class="strong">' + m(T`\boldsymbol{(1,-1)}`) + '</td>' + c('<td>' + m('(1,-1)') + '</td>') + '</tr>' +
          '<tr data-step="2"><th>Price</th><td>uninformative</td><td class="strong">informative</td>' + c('<td>informative</td>') + '</tr>' +
          '<tr data-step="3"><th>Entry</th><td>' + q('base_entry_weak', '0.250') + '</td><td class="strong">' + q('base_entry_strong', '0.523') + '</td>' + c('<td>' + q('base_entry_collapse', '0.250') + '</td>') + '</tr>' +
          '<tr data-step="3"><th>High-value ownership</th><td>' + q('base_ownership_weak', '0.125') + '</td><td class="strong">' + q('base_ownership_strong', '0.324') + '</td>' + c('<td>' + tx('table2_equilibrium_controls.tex', 'Very strong incumbent ($r=3.6$)', 4, '0.125') + '</td>') + '</tr>' +
        '</tbody></table>';
    }

    frame({ id: 'f10a', label: 'F10a', num: '10', part: 6, minutes: 1.5, targets: [], defines: [], widget: '',
      title: 'At the benchmark, entry rises from 0.250 to 0.523', titleQ: { '0.250': 'base_entry_weak', '0.523': 'base_entry_strong' },
      subtitle: 'Declared benchmark; units arbitrary (inputs in backup); unique equilibrium outcomes (analytical)',
      body: benchmarkTable(false) +
        take('Entry rises ' + q('base_entry_change_pp', '27.28') + ' percentage points while the challenger\'s profit at the prior falls: the price, not the prize, brings it in.', 4) });

    frame({ id: 'f10b', label: 'F10b', num: '10', part: 6, minutes: 1.0, targets: ['main:scale', 'main:entry', 'main:cert'], defines: [], widget: '', noframenumbering: true,
      title: 'At the benchmark, entry rises from 0.250 to 0.523', titleQ: { '0.250': 'base_entry_weak', '0.523': 'base_entry_strong' },
      subtitle: 'Declared benchmark; units arbitrary (inputs in backup); unique equilibrium outcomes (analytical)',
      body: benchmarkTable(true) +
        take('Rise, then fall: past a ceiling strength even the best price cannot cover ' + m('c_H') + '.') +
        nav(go('app:scale', 'Benchmark scale'), go('app:entry', 'How entry is computed'), go('app:cert', 'Which equilibrium?')) });

    frame({ id: 'f11', label: 'F11', num: '11', part: 6, minutes: 2.25, targets: ['main:controls', 'main:welfare'], defines: [], widget: 'controls',
      title: 'Freeze the information and deterrence returns',
      subtitle: 'Entry at ' + qm('r_0=1.2', 'base_r_weak', '1.2') + ' and ' + qm('r_1=3', 'base_r_strong', '3') + '; equilibria of the feedback game, then information controls',
      body:
        '<div class="segmented" role="group" aria-label="Which row"><button type="button" data-row="eq" aria-pressed="true">Equilibrium</button><button type="button" data-row="frozen" aria-pressed="false">Frozen orders</button><button type="button" data-row="hidden" aria-pressed="false">Price hidden</button></div>' +
        '<div class="split wide">' +
        '<table class="t-controls"><thead><tr><th></th><th>' + qm('r_0=1.2', 'base_r_weak', '1.2') + '</th><th>' + qm('r_1=3', 'base_r_strong', '3') + '</th><th>Direction</th><th>Status</th></tr></thead><tbody>' +
          '<tr data-row="eq"><th>Equilibrium of the feedback game<span class="sub">(price seen, trading re-solved)</span></th><td>' + q('base_entry_weak', '0.250') + '</td><td><b>' + q('base_entry_strong', '0.523') + '</b></td><td>' + m(T`\uparrow`) + '</td><td>' + st('analytical') + '</td></tr>' +
          '<tr class="panel"><td colspan="5"><em>Information controls</em></td></tr>' +
          '<tr data-row="frozen"><th>Frozen informative orders ' + m('(1,-1)') + '<span class="sub">(imposed at both strengths; control, not an equilibrium at ' + m('r_0') + ')</span></th><td>' + q('base_frozen_entry_weak', '0.562') + '</td><td>' + q('base_frozen_entry_strong', '0.523') + '</td><td>' + m(T`\downarrow`) + '</td><td>' + st('numerical diagnostic;<br>sign analytical (Prop. A.3)') + '</td></tr>' +
          '<tr data-row="hidden"><th>Price hidden from challenger<span class="sub">(equilibrium of the no-price-access game)</span></th><td>' + q('base_hidden_entry_weak', '0.250') + '</td><td>' + q('base_hidden_entry_strong', '0.250') + '</td><td>flat</td><td>' + st('analytical') + '</td></tr>' +
        '</tbody></table>' +
        '<div class="bars" id="f11-bars" aria-live="polite"></div>' +
        '</div>' +
        gray('The price-hidden row is implied by the high-cost window. Without the price, expensive preparation never pays and only the entry floor remains.') +
        take('Hold the price\'s information fixed and a stronger incumbent weakly lowers entry.') +
        nav(go('app:controls', 'Controls in detail'), go('app:welfare', 'Price level or information?')) });

    frame({ id: 'f12', label: 'F12', num: '12', part: 7, minutes: 1.5, targets: ['main:corr'], defines: [], widget: '',
      title: 'At intermediate strength, equilibria coexist',
      subtitle: 'Computer-assisted (Proposition 3): interval arithmetic on exact decimal inputs',
      body:
        '<table class="t-cert"><thead><tr><th>Strength ' + m('r') + '</th><th>' + m('q_H') + '</th><th>' + m('q_L') + ' (certified)</th><th>Entry (certified)</th></tr></thead><tbody>' +
          '<tr><td>' + q('cert_a_r', '1.55') + '</td><td>1</td><td>' + qm(T`\approx-0.460`, '-cert_a_v_interval', '-0.460') + '</td><td>' + qm(T`\approx0.545`, 'cert_a_entry_interval', '0.545') + '</td></tr>' +
          '<tr><td>' + q('cert_b_r', '1.60') + '</td><td>1</td><td>' + qm(T`\approx-0.707`, '-cert_b_v_interval', '-0.707') + '</td><td>' + qm(T`\approx0.549`, 'cert_b_entry_interval', '0.549') + '</td></tr>' +
          '<tr><td>' + q('cert_c_r', '1.65') + '</td><td>1</td><td>' + qm(T`\approx-0.903`, '-cert_c_v_interval', '-0.903') + '</td><td>' + qm(T`\approx0.551`, 'cert_c_entry_interval', '0.551') + '</td></tr>' +
        '</tbody></table>' +
        '<p class="small-note">Hover a certified value for its full enclosure, with outward endpoints.</p>' +
        ul([[1, 'Buy fully after good news, sell partially after bad news; certified entry rises from one strength to the next, above the ' + q('base_entry_strong', '0.523') + ' at ' + m('r_1')],
          [1, 'Each economy also has a no-trade equilibrium with entry ' + qm(T`\rho=0.25`, 'base_rho', '0.25') + ' ' + st('(analytical, Prop. A.4)')],
          [1, 'Elsewhere the numerical search is not exhaustive; the full correspondence is open']]) +
        take('At three certified strengths an informative equilibrium coexists with no trade; I claim nothing about entry between them.', 2) +
        nav(go('app:corr', 'Correspondence')) });

    frame({ id: 'f13', label: 'F13', num: '13', part: 7, minutes: 1.5, targets: ['main:robust'], defines: [], widget: 'footnote',
      title: 'The entry reversal survives four model changes',
      subtitle: 'Entry, weak to strong; each row its own analytical result and declared parameters (Prop. 2 (i)–(ii))',
      body:
        '<table class="t-robust"><thead><tr><th>Specification</th><th>Weak</th><th>Strong</th></tr></thead><tbody>' +
          '<tr data-step="0"><th>Benchmark: Laplace noise, two cost levels</th><td>' + q('base_entry_weak', '0.250') + '</td><td>' + q('base_entry_strong', '0.523') + '</td></tr>' +
          '<tr data-step="1"><th>Atomless costs, half-width ' + q('cost_halfwidth', '0.1') + '</th><td>' + tx('table3_extensions.tex', 'Laplace, cost mixture', 1, '0.250') + '</td><td>' + q('cost_mix_laplace_entry_strong', '0.523') + '</td></tr>' +
          '<tr data-step="2"><th>Logistic noise</th><td>' + tx('table3_extensions.tex', 'logistic, cost atoms', 1, '0.250') + '</td><td>' + q('logistic_entry_strong', '0.302') + '</td></tr>' +
          '<tr data-step="3"><th>Small value gap, ' + qm('h=2', 'moderate_h', '2') + ', ' + qm(T`\ell=1`, 'moderate_ell', '1') + '</th><td>' + q('moderate_entry_weak', '0.250') + '</td><td>' + q('moderate_entry_strong', '0.527') + '</td></tr>' +
          '<tr data-step="4"><th>Complementary signals (declared example): investor accuracy ' + q('signal_trader_accuracy_value', '0.70') + ', challenger accuracy ' + q('signal_buyer_accuracy_value', '0.75') + '; ' + qm(T`\rho=0.85`, 'signal_rho', '0.85') + ', strengths ' + q('signal_r_weak', '1.1') + ' vs ' + q('signal_r_strong', '2.3') + '</th><td>' + q('signal_entry_weak', '0.850') + '</td><td>' + q('signal_entry_strong', '0.879') + '</td></tr>' +
        '</tbody></table>' +
        '<p class="grayline">Rows differ in ' + m(T`\rho`) + ' and strengths; compare within a row, not across rows.</p>' +
        '<div class="grayline"><button type="button" class="toggle-line" aria-expanded="false" data-toggle="f13-grid">Signal grid, 25 accuracy cells</button><span id="f13-grid" hidden>: entry rises in the ' + tx('table_signal_grid.tex', '#count:met', 0, '6') + ' meeting Prop. A.7 (analytical) and is unchanged in ' + tx('table_signal_grid.tex', '#count:unchanged', 0, '9') + ' with challenger accuracy ' + m(T`{}\le0.75`) + '; it falls about 4 pp when challenger accuracy is ' + m(T`{}\ge0.76`) + ', because its own good signal already triggers entry against the weak incumbent (numerical diagnostic).</span></div>' +
        take('The ' + m(T`r_0\to r_1`) + ' reversal survives atomless costs, logistic noise, a small value gap and complementary private signals (declared example).', 5) +
        nav(go('app:robust', 'Full table')) });

    frame({ id: 'f14', label: 'F14', num: '14', part: 7, minutes: 1.0, targets: ['main:reserve'], defines: [], widget: 'access',
      title: 'Price access raises proceeds and surplus at $r_1$',
      subtitle: 'Incumbent held at ' + qm('r_1=3', 'base_r_strong', '3') + '; price seen or hidden; trading re-solved in both (Prop. A.9, analytical)',
      body:
        '<div class="segmented" role="group" aria-label="Highlight a column"><button type="button" data-col="1" aria-pressed="false">Price observed</button><button type="button" data-col="2" aria-pressed="false">Price hidden</button></div>' +
        '<table class="t-access"><thead><tr><th></th><th data-col="1">Price observed</th><th data-col="2">Price hidden</th><th>Gain</th></tr></thead><tbody>' +
          '<tr><th>Expected target proceeds</th><td data-col="1">' + q('base_revenue_feedback', '0.872') + '</td><td data-col="2">' + q('base_revenue_hidden', '0.615') + '</td><td>' + q('base_revenue_gain', '0.258') + '</td></tr>' +
          '<tr><th>Acquisition surplus net of preparation costs</th><td data-col="1">' + tx('table2_equilibrium_controls.tex', 'Net acquisition surplus', 1, '2.38') + '</td><td data-col="2">' + tx('table2_equilibrium_controls.tex', 'Net acquisition surplus', 2, '2.30') + '</td><td>' + q('base_net_surplus_gain', '0.0802') + '</td></tr>' +
        '</tbody></table>' +
        ul(['Same full orders in both economies, so trading costs coincide', 'Each extra entry happens only when its expected profit covers its cost']) +
        gray('Gain from unrounded values. At ' + m('r_0') + ' prices are uninformative, so there is no gain. The comparison holds the sale rule and the incumbent distribution fixed.') +
        nav(go('app:reserve', 'Reserve')) });

    frame({ id: 'f15', label: 'F15', num: '15', part: 8, minutes: 1.0, targets: [], defines: [], widget: '',
      title: 'Three predictions',
      subtitle: 'Public sale processes with one prepared bidder and a further buyer still deciding',
      body:
        ul([[0, '<b>A stronger bidder can draw a buyer in</b> when the price comes before the buyer\'s decision; without the price, a stronger bidder weakly lowers entry ' + st('(analytical, Prop. 2; Prop. A.3)')],
          [1, '<b>Buyers that prepare after good news win more often:</b> among buyers that prepare at a price, the share of high-value buyers is the price-implied posterior'],
          [2, '<b>Against a very strong bidder, entry stops responding</b> to the price, while the price stays informative ' + st('(analytical, Prop. 2(iii))')]], 'roomy') +
        gray('Outcome: the start of diligence, not public offers. Pre-bid returns also reflect anticipation of the bid, so each test dates the price before the decision (Schwert 1996; Online Appendix D).') });

    frame({ id: 'f16', label: 'F16', num: '16', part: 8, minutes: 1.0, targets: [], defines: [], widget: '',
      title: 'Conclusion', subtitle: '',
      body:
        ul([key('A stronger incumbent can bring the challenger in:') + ' at the benchmark, entry rises from ' + q('base_entry_weak', '0.250') + ' to ' + q('base_entry_strong', '0.523') + ' although the challenger\'s expected profit before any news falls',
          '<b>Why:</b> competition makes target proceeds more sensitive to who the challenger is; informed trading puts that into the price; good news draws in the expensive challenger. Freeze that information and deterrence returns.',
          '<b>Implication:</b> when the target trades, a stronger rival is not a pure deterrent, because who competes depends on what the price reveals before anyone prepares.'], 'conclusion') });

    /* ================================================================ backup frames */

    function backup(o) { o.part = 'B'; o.minutes = 0; o.backup = true; o.num = o.label; frame(o); }

    backup({ id: 'a1', label: 'A1', origin: 'f1', targets: ['app:interval'], defines: [], widget: '',
      title: 'Which deals have a decision interval', subtitle: '',
      body:
        ul(['A disclosed approach, an announced strategic review or an open contest can create one if the opportunity becomes public before the buyer set is fixed',
          'Only then can a prospective challenger watch the price while it decides',
          'Strength = the public distribution of the incumbent\'s value, not an announced bid',
          'Imprivata\'s proxy separates an unsolicited approach, outreach to potential buyers, and indications of interest conditional on diligence, which documents a costly preparation stage; the three predictions say how to test whether prices draw buyers into it ' + cite('Imprivata 2016; Boone and Mulherin 2007; Gentry and Stroup 2019')], 'roomy') +
        gray('Whether a deal fits is a question about its chronology; Online Appendix D shows how to date it (Section 2.1).') +
        nav(back('main:interval')) });

    backup({ id: 'a2', label: 'A2', origin: 'f1', targets: ['app:evidence'], defines: [], widget: '',
      title: 'Evidence: the pilot design', subtitle: '',
      body:
        ul(['<b>Pilot (Online Appendix D):</b> reconstruct from disclosure records the timing of approaches, public visibility, buyer contacts, diligence, proposals and final selection',
          'Separate when an event occurred from when it first became public',
          '<b>First requirement:</b> a publicly understood sale opportunity that stays contestable while a challenger decides',
          '<b>Outcome:</b> the decision to prepare; prices must precede it',
          '<b>Caution:</b> returns before a bid also reflect its anticipation ' + cite('Schwert 1996')], 'roomy') +
        gray('Online Appendix D sets out the pilot design for the predictions of Section 7.') +
        nav(back('main:evidence')) });

    var LIT = [
      ['Dow, Goldstein and Guembel (2017)', 'investment feeds back on information', 'one surplus, two opposed claims'],
      ['Edmans, Goldstein and Jiang (2015)', 'real actions curb bad-news trading', 'rivals shift claim sensitivity'],
      ['Edmans, Goldstein and Jiang (2012)', 'prices affect takeover activity', 'a challenger learns its own value'],
      ['Fishman (1988);<br>Hirshleifer and Png (1989)', 'stronger rivals deter preparation', 'kept at fixed information (Prop. A.3)'],
      ['Levin and Smith (1994);<br>Gentry and Stroup (2019)', 'the bidder pool is endogenous', 'entry responds to the price'],
      ['Roberts and Sweeting (2013)', 'selective entry shapes procedure', 'sale terms left open'],
      ['Persico (2000)', 'formats shape bidders\' information', 'the informed party is not a bidder'],
      ['Luo (2005)', 'learning from announcement returns', 'learning precedes entry'],
      ['Betton et al. (2014); Lin et al. (2025)', 'negotiation feedback; payment choice', 'cash fixed; entry of a new bidder'],
      ['Cornelli and Li (2002)', 'arbitrage positions affect tenders', 'the investor does not tender'],
      ['Pernoud and Gleyze (2026);<br>Liu and Bernhardt (2022);<br>Carlin et al. (2026)', 'learning own values and rivals;<br>post-auction feedback;<br>bidder-pool choice', 'the informed party trades outside the auction, before entry']
    ];
    backup({ id: 'a3', label: 'A3', origin: 'f3', targets: ['app:lit'], defines: [], widget: 'rows',
      title: 'Related work in more detail',
      subtitle: 'Increment: under one sale rule the two returns move oppositely, which produces the entry reversal',
      body:
        '<table class="t-lit hover-rows"><thead><tr><th>Work</th><th>Shows</th><th>Here</th></tr></thead><tbody>' +
        LIT.map(function (r) { return '<tr><td>' + r[0] + '</td><td>' + r[1] + '</td><td>' + r[2] + '</td></tr>'; }).join('') +
        '</tbody></table>' + nav(back('main:lit')) });

    backup({ id: 'a4', label: 'A4', origin: 'f4', targets: ['app:omit'], defines: [], widget: '',
      title: 'What the model leaves out, and why', subtitle: '',
      body:
        '<table class="t-omit"><tbody>' +
          '<tr><th>In the model</th><td>Neither bidder trades. The investor has no initial position, cannot bid, tender or acquire, and has no control rights. The sale binds all shares (no tendering or holdout). Every wrong-signed order loses against every candidate schedule, so the investor cannot profit by faking good news.</td></tr>' +
          '<tr><th>Outside the model</th><td>Toeholds ' + cite('Bulow, Huang and Klemperer 1999') + '; free riding ' + cite('Grossman and Hart 1980') + '; announced or jump bids as signals ' + cite('Fishman 1988') + ' (strength here is a distribution); incumbent or target manipulation and endogenous investor research ' + cite('Goldstein and Guembel 2008') + '; first-price and bargaining-with-trading equilibria.</td></tr>' +
        '</tbody></table>' +
        take('The paper does not solve toeholds, so it makes no statement on the direction of a toehold effect.') +
        nav(back('main:omit')) });

    backup({ id: 'a5', label: 'A5', origin: 'f4', targets: ['app:info'], defines: ['a_d'], widget: '',
      title: 'Complementary, not superior, information', subtitle: '',
      body:
        ul(['The challenger knows its own integration plans; a specialist investor may know the target\'s customers, technology and product demand',
          'Different facts about the same acquisition match',
          'Preparation (diligence) is what reveals the exact value to the challenger',
          'The benchmark\'s perfectly informed investor and uninformed challenger make the mechanism visible; Section 5.3 removes both extremes',
          'The reversal holds with challenger accuracy ' + qm('d=0.75', 'signal_buyer_accuracy_value', '0.75') + ' above investor accuracy ' + qm('a=0.70', 'signal_trader_accuracy_value', '0.70') + ' ' + st('(Prop. A.7, analytical)')], 'roomy') +
        nav(go('app:signals', 'The signal economy'), back('main:info')) });

    backup({ id: 'a6', label: 'A6', origin: 'a5', targets: ['app:signals'], defines: ['TY', 'P', 'e_HL'], widget: '',
      title: 'The price helps a challenger with its own signal', subtitle: '',
      body:
        ul(['Investor signal ' + m('T') + ' (accuracy ' + m('a') + '), challenger signal ' + m('Y') + ' (accuracy ' + m('d') + '); the challenger uses ' + m(T`\Pr(H\mid P,\,Y=y)`) + ', ' + m('P') + ' = stock price',
          'Entry is state dependent: ' + m('e_H') + ', ' + m('e_L') + ' = entry probability when the challenger is high / low value; the price still reveals the market posterior',
          'Declared example ' + qm('a=0.70', 'signal_trader_accuracy_value', '0.70') + ', ' + qm('d=0.75', 'signal_buyer_accuracy_value', '0.75') + ': entry ' + q('signal_entry_weak', '0.850') + ' → ' + q('signal_entry_strong', '0.879') + ' ' + st('(analytical, Prop. A.7)') + '; ' + qm(T`\rho=0.85`, 'signal_rho', '0.85') + ', ' + qm('c_H=7.14', 'signal_c_high', '7.14') + ', ' + qm('k=0.015', 'signal_k', '0.015') + ', strengths ' + q('signal_r_weak', '1.1') + ' vs ' + q('signal_r_strong', '2.3')], 'small') +
        '<table class="t-grid"><thead><tr><th>Cells</th><th>Accuracy grid (25 cells)</th><th>Entry change (pp)</th><th>Status</th></tr></thead><tbody>' +
          '<tr><td>' + tx('table_signal_grid.tex', '#count:met', 0, '6') + '</td><td>meet Prop. A.7</td><td>rises ' + tx('table_signal_grid.tex', '0.71 & 0.74', 4, '2.81') + ' to ' + tx('table_signal_grid.tex', '0.72 & 0.75', 4, '3.09') + '</td><td>' + st('analytical') + '</td></tr>' +
          '<tr><td>' + tx('table_signal_grid.tex', '#count:unchanged', 0, '9') + '</td><td>' + m(T`d\le0.75`) + ', condition not met</td><td>unchanged</td><td>' + st('numerical diagnostic') + '</td></tr>' +
          '<tr><td>' + tx('table_signal_grid.tex', '#count:falls', 0, '10') + '</td><td>' + m(T`d\ge0.76`) + '</td><td>falls ' + tx('table_signal_grid.tex', '0.72 & 0.77', 4, '-4.03', '4.03') + ' to ' + tx('table_signal_grid.tex', '0.68 & 0.76', 4, '-4.49', '4.49') + '</td><td>' + st('numerical diagnostic') + '</td></tr>' +
        '</tbody></table>' +
        take('The price matters when the challenger\'s own signal is informative but not decisive.') +
        nav(back('app:info')) });

    backup({ id: 'a7', label: 'A7', origin: 'f4', targets: ['app:eq'], defines: ['sigma', 'q', 'X_Z'], widget: '',
      title: 'Equilibrium and the two comparisons', subtitle: '',
      body:
        ul(['<b>Definition:</b> order distributions ' + m(T`\sigma_H,\sigma_L`) + ' (mixing allowed; any deviation ' + m(T`q\in[-1,1]`) + '); a rational price that anticipates entry; Bayesian beliefs from the price; optimal entry; truthful bids',
          'Order flow ' + m('X=q+Z') + ', Laplace noise ' + m('Z') + ' with scale ' + m('b') + '; stock price ' + m('P(X)') + ' = expected target payoff given ' + m('X'),
          '<b>Two comparisons kept apart:</b> a unilateral deviation is evaluated against fixed price and entry schedules; a cross-economy comparison re-solves them',
          '<b>Uniqueness</b> refers to trading and on-path entry under truthful bidding'], 'roomy') +
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
        gray('Proposition 1 (analytical) holds for any ' + m('F') + ' on ' + m(T`[0,\bar r]`) + ', ' + m(T`\ell<\bar r<h`) + '; strict when the change in ' + m('F') + ' has positive integral over the relevant range.') +
        take('The closed forms are the uniform case; the two signs are not a uniform-distribution artifact.') +
        nav(back('main:payoffs')) });

    backup({ id: 'a9', label: 'A9', origin: 'f5', targets: ['app:payrule'], defines: ['eta'], widget: 'x4',
      title: 'The payment rule decides the sign of the spread effect', subtitle: '',
      body:
        '<div class="split">' +
          '<div class="col"><div class="figure" id="x4" tabindex="0" aria-label="Figure X4. Target-payoff spread and challenger profit against the seller bargaining weight; arrow keys move the cursor."></div></div>' +
          '<div class="col text">' +
            '<p>Zero-reserve verifiable-value institution, Nash weight ' + m(T`\eta`) + ': seller gets ' + m(T`t_\eta=(1-\eta)\cdot{}`) + 'runner-up value' + m('{}+') + m(T`\eta\cdot{}`) + 'winner value</p>' +
            '<p>Stronger incumbent: challenger profit falls weakly for every ' + m(T`\eta`) + '. Spread ' + info(m(T`\Delta_\eta`)) + m(T`=\eta(h-\ell)+(1-2\eta)\,\mathbb{E}[(R-\ell)_+]`) + ' rises (weakly) if ' + m(T`\eta<1/2`) + ', falls (weakly) if ' + m(T`\eta>1/2`) + ', for any ' + m(T`R\sim F`) + ' on ' + m(T`[0,\bar r]`) + ', ' + m(T`\ell<\bar r<h`) + ', ' + m(T`0\le\eta<1`) + ' ' + st('(Prop. A.8, analytical)') + '</p>' +
          '</div>' +
        '</div>' +
        take('Payment stage only: an entry reversal under bargaining is not solved, and first-price equilibria are not solved.') +
        nav(back('main:payrule')) });

    backup({ id: 'a10', label: 'A10', origin: 'f7', targets: ['app:bound'], defines: ['U_Pi'], widget: '',
      title: 'Why trading is unique: a global bound', subtitle: '',
      body:
        ul(['<b>Weak:</b> gross advantage per unit ' + m(T`\le\Delta_T(r_0)<k`) + ', so every nonzero order loses and the posterior stays at ' + m('1/2'),
          '<b>Strong:</b> with ' + m(T`\Pi_\theta(s)`) + ' the expected residual per unit at order size ' + m('s') + ',']) +
        d(T`U_\theta(s)=s\,\Pi_\theta(s)-ks,\qquad U_\theta'(s)\ \ge\ (1-1/b)\,\rho m\,\Delta_T(r_1)-k\ >\ 0\quad\text{on }[0,1]`) +
        ul(['Holds against every candidate price and entry schedule, including mixed orders: global, not first-order',
          '<b>Investor manipulation (in-model):</b> both residual advantages in eq. (11) are positive under every candidate order distribution, so a wrong-signed order, such as a low-value investor buying to fake good news and trigger entry, has negative gross payoff and still pays ' + m('k'),
          'Incumbent or target manipulation and toeholds: outside the model (A4)']) +
        nav(back('main:bound')) });

    backup({ id: 'a11', label: 'A11', origin: 'f7', targets: ['app:orders'], defines: [], widget: '',
      title: 'Orders, units and the trading cost', subtitle: '',
      body:
        ul([m(T`q\in[-1,1]`) + ' is a normalized small trading unit, not ownership of the target, measured in the same units as the noise (scale ' + m('b') + '); the investor has no initial position',
          m('k') + ' is an execution or position-carrying friction, distinct from adverse-selection price impact, which competitive pricing already generates',
          '<b>Why a corner, unlike Kyle:</b> the per-unit advantage is at least ' + m(T`\rho m\Delta_T`) + ' because beliefs stay in ' + m('[m,M]') + ', and one more unit erodes it by at most a fraction ' + m('1/b') + ' (the haircut)',
          'So marginal profit stays above ' + m('k') + ' over the whole interval, and full orders are the unique best response (A10)',
          'Against the weak incumbent the same bounds make every order lose'], 'roomy') +
        nav(back('main:orders')) });

    backup({ id: 'a12', label: 'A12', origin: 'f7', targets: ['app:notation'], defines: [], widget: 'notation',
      title: 'Notation', subtitle: '',
      body: '<div class="notation" id="notation-table"></div>' + nav(back('main:notation')) });

    backup({ id: 'a13', label: 'A13', origin: 'f8', targets: ['app:suff'], defines: ['mu_X'], widget: '',
      title: 'The challenger can read the market\'s belief off the price', subtitle: '',
      body:
        ul(['Under any mixed orders the posterior from order flow is bounded (Laplace likelihood ratio within ' + m(T`e^{\pm2/b}`) + '):']) +
        d(T`\begin{gathered}\mu_X(x)=\Pr(H\mid X=x)\in[m,M]\\ \text{price}=t_0+(\text{entry probability at that price})\times(t_L-t_0+\Delta_T\,\mu)\end{gathered}`) +
        ul([m('t_0') + ' = expected target proceeds without a challenger',
          'The price is strictly increasing in ' + m(T`\mu`) + ', because entry ' + m(T`\ge\rho>0`) + ' and ' + m(T`\Delta_T>0`),
          'Atoms and entry jumps allowed; no differentiability needed ' + st('(Props. A.1–A.2, analytical)')]) +
        take('The price is a sufficient statistic for the market\'s belief, so the challenger loses nothing by seeing the price rather than the flow.') +
        nav(back('main:suff')) });

    backup({ id: 'a14', label: 'A14', origin: 'f8', targets: ['app:laplace'], defines: ['f', 'x_star', 'eps_C'], widget: 'x3',
      title: 'Why Laplace noise, and what logistic noise changes', subtitle: '',
      body:
        '<div class="figure wide" id="x3" tabindex="0" aria-label="Figure X3. Posterior tail and entry against the threshold distance, Laplace and logistic noise; arrow keys move the cursor."></div>' +
        ul(['Both noise densities ' + m('f') + ' satisfy ' + m(T`|f'|\le f/b`) + ', so the global trading bounds hold for both',
          'Laplace: the posterior reaches ' + m('[m,M]') + ' at finite flow; logistic: only as flow ' + m(T`\to\infty`) + ' (' + qm(T`x^*\approx5.42`, 'logistic_flow_threshold', '5.42') + ', about ' + q('logistic_threshold_noise_sd', '1.5') + ' noise s.d. from the center)',
          'Entry ' + q('logistic_entry_strong', '0.302') + ' vs ' + q('base_entry_strong', '0.523') + '; atomless costs (' + qm(T`\varepsilon_C=0.1`, 'cost_halfwidth', '0.1') + '): ' + q('cost_mix_laplace_entry_strong', '0.523') + ' and ' + q('cost_mix_logistic_entry_strong', '0.301') + '. Common scale ' + m('b') + ', not common variance; not a Blackwell ranking ' + st('(analytical, Props. A.5–A.6)')], 'small') +
        nav(back('main:laplace')) });

    backup({ id: 'a15', label: 'A15', origin: 'f8', targets: ['app:floor'], defines: [], widget: '',
      title: 'Why the model needs a low-cost floor', subtitle: '',
      body:
        ul(['The ' + cost('low-cost floor') + ' keeps entry ' + m(T`\ge\rho`) + ' after every price: the price reveals the posterior, the investor\'s edge is at least ' + m(T`\rho m\Delta_T`) + ', and information can only add entry',
          'If cheap preparation fails only at bad prices, bad prices deter it and flows can pool at one price',
          'If cheap preparation fails at the prior, no preparation and no trade form an equilibrium',
          'Theorem margin at the benchmark: ' + q('base_margin_low_cost', '1.37'),
          'The floor alone gives entry ' + q('base_hidden_entry_weak base_hidden_entry_strong', '0.250') + ' at both strengths when the price is hidden',
          'Atomless cost supports keep it ' + st('(Prop. A.6, analytical)')], 'roomy') +
        nav(back('main:floor')) });

    backup({ id: 'a16', label: 'A16', origin: 'f9', targets: ['app:proof'], defines: ['alpha'], widget: '',
      title: 'Proof logic in four steps', subtitle: '',
      body:
        '<ol class="steps">' +
          '<li data-step="0"><b>Weak economy:</b> no order covers ' + m('k') + '; no trade; entry ' + m(T`\rho`) + '</li>' +
          '<li data-step="1"><b>Strong economy:</b> the global bound (A10) forces full orders</li>' +
          '<li data-step="2">Under full orders the high-cost window puts the belief threshold inside ' + m('(1/2,M)') + ', so good news crosses it with positive probability; ' + m(T`\alpha_H>\alpha_L`) + ' (good news is likelier when the challenger is high value, ' + m(T`\alpha_\theta=\Pr(\text{order flow crosses the entry threshold}\mid\theta)`) + ') tilts extra entry to high values</li>' +
          '<li data-step="3"><b>Blackwell:</b> a constant kernel maps the strong experiment to the weak one; no state-independent kernel maps the constant experiment to the strong one</li>' +
        '</ol>' +
        '<p data-step="4"><b>Part (iii):</b> with the floor and profitable trading still in place at ' + m('r_2') + ', ' + m(T`B_{r_2}(M)<c_H`) + ' removes expensive entry.</p>' +
        take('What does the work: step 2, a bound that holds against every candidate schedule.', 4) +
        nav(back('main:proof')) });

    backup({ id: 'a17', label: 'A17', origin: 'f9', targets: ['app:margins'], defines: [], widget: '',
      title: 'Conditions are jointly satisfiable for every $h>\\ell$', subtitle: '',
      body:
        '<table class="t-margins"><thead><tr><th colspan="3">Theorem margins at the benchmark</th></tr></thead><tbody>' +
          '<tr><td>' + cost('Low-cost floor') + '</td><td>' + m(T`B_{r_1}(m)-c_L`) + '</td><td>' + q('base_margin_low_cost', '1.37') + '</td></tr>' +
          '<tr><td>' + cost('High-cost window') + ', weak prior</td><td>' + m(T`c_H-B_{r_0}(1/2)`) + '</td><td>' + q('base_margin_high_prior', '1.20') + '</td></tr>' +
          '<tr><td>' + cost('High-cost window') + ', best strong price</td><td>' + m(T`B_{r_1}(M)-c_H`) + '</td><td>' + q('base_margin_high_ceiling', '0.217') + '</td></tr>' +
          '<tr><td>' + info('Trading-cost window') + ', weak</td><td>' + m(T`k-\Delta_T(r_0)`) + '</td><td>' + q('base_margin_weak_trade', '0.00333') + '</td></tr>' +
          '<tr><td>' + info('Trading-cost window') + ', strong</td><td>' + m(T`(1-1/b)\rho m\Delta_T(r_1)-k`) + '</td><td>' + q('base_margin_strong_trade', '0.00241') + '</td></tr>' +
          '<tr class="total"><td>Minimum</td><td></td><td>' + q('base_minimum_theorem_margin', '0.00241') + '</td></tr>' +
        '</tbody></table>' +
        ul(['Nonemptiness for every ' + m(T`h>\ell`) + ' comes from a construction: take ' + m('r_0<r_1') + ' close to ' + m(T`\ell`) + ', then ' + m('k') + ', ' + m('c_H') + ', ' + m('c_L') + ' strictly inside their windows',
          'A mathematical construction, not slack at the benchmark and not an effect-size claim; moderate values ' + qm('h=2', 'moderate_h', '2') + ': minimum margin ' + qm(T`8.01\times10^{-4}`, 'moderate_minimum_theorem_margin', T`8.01\times10^{-4}`),
          'Part (iii) is not claimed for every ' + m(T`h>\ell`)], 'small') +
        nav(back('main:margins')) });

    backup({ id: 'a18', label: 'A18', origin: 'f9', targets: ['app:forces'], defines: [], widget: 'columns',
      title: 'Two forces from one payment rule', subtitle: '',
      body:
        '<table class="t-forces hover-cols"><thead><tr><th></th><th data-col="1">Deterrence</th><th data-col="2" class="info">Information</th></tr></thead><tbody>' +
          '<tr><th>What a stronger incumbent moves</th><td data-col="1">challenger profit ' + m(T`B_r(\mu)\downarrow`) + ' at every belief</td><td data-col="2">' + info('target-payoff spread ' + m(T`\Delta_T\uparrow`)) + '</td></tr>' +
          '<tr><th>Who responds</th><td data-col="1">the challenger, at a given belief</td><td data-col="2">the investor, then the price, then the challenger\'s belief</td></tr>' +
          '<tr><th>What it needs</th><td data-col="1">nothing</td><td data-col="2">entry after any price (' + cost('low-cost floor') + '); price seen before entry</td></tr>' +
          '<tr><th>Effect on entry</th><td data-col="1"><b>weakly ' + m(T`\downarrow`) + '</b> ' + cite('(Prop. A.3)') + '</td><td data-col="2">' + m(T`\uparrow`) + ' once trading pays and good news clears ' + cost(m('c_H')) + '</td></tr>' +
        '</tbody></table>' +
        take(info('stronger incumbent → wider ' + m(T`\Delta_T`) + ' → informed trading pays → informative price → good news clears') + ' ' + cost(m('c_H')) + ' ' + info('→ the expensive challenger enters')) +
        nav(back('main:forces')) });

    var A19_IN = [['h', 'base_h', '10', 'moderate_h', '2'], [T`\ell`, 'base_ell', '1', 'moderate_ell', '1'], ['p', 'base_p', '0.5', 'moderate_p', '0.5'],
      [T`\rho`, 'base_rho', '0.25', 'moderate_rho', '0.25'], ['c_L', 'base_c_low', '1', 'moderate_c_low', '0.3'], ['c_H', 'base_c_high', '6', 'moderate_c_high', '0.89'],
      ['b', 'base_b', '2', 'moderate_b', '2'], ['k', 'base_k', '0.02', 'moderate_k', '0.002']];
    backup({ id: 'a19', label: 'A19', origin: 'f10b', targets: ['app:scale'], defines: [], widget: '',
      title: 'Benchmark scale: declared, not calibrated', subtitle: '',
      body:
        '<div class="split narrow">' +
          '<table class="t-inputs"><thead><tr><th>Input</th><th>Benchmark</th><th>Moderate</th></tr></thead><tbody>' +
            A19_IN.map(function (r) { return '<tr><th>' + m(r[0]) + '</th><td>' + q(r[1], r[2]) + '</td><td>' + q(r[3], r[4]) + '</td></tr>'; }).join('') +
          '</tbody></table>' +
          '<table class="t-outcomes"><thead><tr><th></th><th>Benchmark</th><th>Moderate</th></tr></thead><tbody>' +
            '<tr><th>Strengths</th><td>' + q('base_r_weak', '1.2') + ' → ' + q('base_r_strong', '3') + '</td><td>' + q('moderate_r_weak', '1.05') + ' → ' + q('moderate_r_strong', '1.5') + '</td></tr>' +
            '<tr><th>Entry</th><td>' + q('base_entry_weak', '0.250') + ' → ' + q('base_entry_strong', '0.523') + '</td><td>' + q('moderate_entry_weak', '0.250') + ' → ' + q('moderate_entry_strong', '0.527') + '</td></tr>' +
            '<tr><th>Minimum theorem margin</th><td>' + q('base_minimum_theorem_margin', '0.00241') + '</td><td>' + qm(T`8.01\times10^{-4}`, 'moderate_minimum_theorem_margin', T`8.01\times10^{-4}`) + '</td></tr>' +
          '</tbody></table>' +
        '</div>' +
        gray('Units are arbitrary; magnitudes are not calibrated; the signs are the theorem; nonemptiness holds for every ' + m(T`h>\ell`) + ' (A17).') +
        take('A moderate economy with ' + qm('h=2', 'moderate_h', '2') + ' gives a rise of similar size (' + q('moderate_entry_weak', '0.250') + ' → ' + q('moderate_entry_strong', '0.527') + '), so the benchmark scale is a declaration, not the mechanism.') +
        nav(back('main:scale')) });

    backup({ id: 'a20', label: 'A20', origin: 'f10b', targets: ['app:entry'], defines: ['tau', 'x_star', 'alpha', 'e_HL', 'E_O', 'r_C'], widget: '',
      title: 'How entry and ownership are computed', subtitle: '',
      body:
        d(T`\begin{gathered}\tau=\frac{c_H-g_L}{g_H-g_L}\quad\text{($c_H$ = expensive cost)},\qquad x^*=\frac b2\log\frac{\tau}{1-\tau},\qquad \alpha_\theta=\Pr(X\ge x^*\mid\theta)\\ e_H=\rho+(1-\rho)\alpha_H,\qquad e_L=\rho+(1-\rho)\alpha_L,\qquad \mathsf E=\frac{e_H+e_L}{2},\qquad \mathsf O_H=\frac{e_H}{2}\end{gathered}`) +
        ul([m(T`\tau`) + ' = belief threshold for costly preparation; ' + m(T`\alpha_\theta`) + ' = probability that order flow crosses the entry threshold; entry ' + m(T`\mathsf E`) + ' = Pr(challenger prepares); high-value ownership ' + m(T`\mathsf O_H`) + ' = Pr(high-value challenger acquires the target)',
          'The high-cost window puts ' + m(T`\tau\in(1/2,M)`) + ' and ' + m(T`x^*\in(0,1)`) + '; ' + m(T`\alpha_H>\alpha_L`),
          'Above the ceiling strength ' + qm(T`r_C\approx3.59`, 'base_r_high_cost_ceiling', '3.59') + ', ' + m(T`\tau>M`) + '; the left-limit entry at ' + m('r_C') + ' is ' + q('base_laplace_entry_ceiling_left_limit', '0.506'),
          'Expected target proceeds ' + tx('table2_equilibrium_controls.tex', 'Weak incumbent ($r=1.2$)', 5, '0.393') + ' / ' + tx('table2_equilibrium_controls.tex', 'Strong incumbent ($r=3$)', 5, '0.872') + ' / ' + tx('table2_equilibrium_controls.tex', 'Very strong incumbent ($r=3.6$)', 5, '0.664') + ' at ' + m('r_0') + ' / ' + m('r_1') + ' / ' + m('r_2')], 'small') +
        nav(back('main:entry')) });

    function certRow(letter, r, v, e, cover) {
      return '<tr><td>' + q('cert_' + letter + '_r', r) + '</td><td>' + qm(v, '-cert_' + letter + '_v_interval', v) + '</td><td>' + qm(e, 'cert_' + letter + '_entry_interval', e) + '</td><td>' + q('cert_' + letter + '_high_derivative_lower', cover) + '</td></tr>';
    }
    backup({ id: 'a21', label: 'A21', origin: 'f10b', targets: ['app:cert'], defines: [], widget: '',
      title: 'Which equilibrium? What the proof certifies', subtitle: '',
      body:
        '<p class="small">The reversal (frames 9–10) compares economies in which trading and on-path entry are unique, so no selection is needed; multiplicity arises only between them (frame 12).</p>' +
        '<table class="t-enclosures"><thead><tr><th>' + m('r') + '</th><th>' + m(T`q_L\in`) + '</th><th>Entry ' + m(T`\mathsf E\in`) + '</th><th>High-type cover margin ' + m(T`\ge`) + '</th></tr></thead><tbody>' +
          certRow('a', '1.55', T`[-0.46031620,\,-0.46031618]`, T`[0.5450528898,\,0.5450528922]`, '0.0000761777') +
          certRow('b', '1.60', T`[-0.70747539,\,-0.70747537]`, T`[0.5487563062,\,0.5487563085]`, '0.0027531948') +
          certRow('c', '1.65', T`[-0.90333201,\,-0.90333198]`, T`[0.5513607988,\,0.5513608020]`, '0.0054921767') +
        '</tbody></table>' +
        ul(['<b>Low type:</b> global strict concavity; a sign change of its marginal profit at its own order brackets the root (' + q('cert_a_psi_left_lower', '0.000000000114') + ' and ' + qm('-0.000000000096', 'cert_a_psi_right_upper', '-0.000000000096') + ' at ' + qm('r=1.55', 'cert_a_r', '1.55') + ')',
          '<b>High type:</b> cover margin strictly positive over the whole bracket (last column)',
          '<b>Not proved:</b> uniqueness of the informative profile, absence of mixed equilibria, a branch between nodes'], 'small') +
        '<p class="status-line">' + st('computer-assisted (Proposition 3): interval arithmetic on exact decimal inputs') + '</p>' +
        nav(back('main:cert')) });

    function t2(row, a, b, c) {
      return '<td>' + tx('table2_equilibrium_controls.tex', row, 3, a) + '</td><td>' + tx('table2_equilibrium_controls.tex', row, 4, b) + '</td><td>' + tx('table2_equilibrium_controls.tex', row, 5, c) + '</td>';
    }
    backup({ id: 'a22', label: 'A22', origin: 'f11', targets: ['app:controls'], defines: [], widget: '',
      title: 'Information controls in detail', subtitle: '',
      body:
        ul(['Prop. A.3 ' + st('(analytical)') + ': at any fixed information experiment and cost law, entry weakly falls with strength; within fixed orders, not across order profiles that change with ' + m('r'),
          'The frozen weak profile is a control, not an equilibrium: full orders lose money there because ' + m(T`\Delta_T(r_0)<k`) + '; at ' + m('r_1') + ' it coincides with the equilibrium'], 'small') +
        '<table class="t-detail"><thead><tr><th></th><th>' + m('r') + '</th><th>Entry ' + m(T`\mathsf E`) + '</th><th>High-value ownership ' + m(T`\mathsf O_H`) + '</th><th>Target proceeds</th><th>Status</th></tr></thead><tbody>' +
          '<tr><th><em>Equilibria of the feedback game</em></th><td>1.2</td>' + t2('Weak incumbent ($r=1.2$)', '0.250', '0.125', '0.393') + '<td>' + st('analytical') + '</td></tr>' +
          '<tr><th></th><td>3</td>' + t2('Strong incumbent ($r=3$)', '0.523', '0.324', '0.872') + '<td>' + st('analytical') + '</td></tr>' +
          '<tr><th></th><td>3.6</td>' + t2('Very strong incumbent ($r=3.6$)', '0.250', '0.125', '0.664') + '<td>' + st('analytical') + '</td></tr>' +
          '<tr class="panel"><td colspan="6"><em>Frozen informative orders</em> (control, not an equilibrium at ' + m('r_0') + ')</td></tr>' +
          '<tr><th></th><td>1.2</td>' + t2('Frozen informative orders, $r=1.2$', '0.562', '0.351', '0.520') + '<td>' + st('numerical diagnostic') + '</td></tr>' +
          '<tr><th></th><td>3</td>' + t2('Frozen informative orders, $r=3$', '0.523', '0.324', '0.872') + '<td>' + st('numerical diagnostic') + '</td></tr>' +
          '<tr class="panel"><td colspan="6"><em>Price hidden from challenger</em> (equilibrium of the no-price-access game)</td></tr>' +
          '<tr><th></th><td>1.2</td>' + t2('Price hidden, $r=1.2$', '0.250', '0.125', '0.393') + '<td>' + st('analytical') + '</td></tr>' +
          '<tr><th></th><td>3</td>' + t2('Price hidden, $r=3$', '0.250', '0.125', '0.615') + '<td>' + st('analytical') + '</td></tr>' +
        '</tbody></table>' +
        gray('Price hidden: the challenger enters only at low cost (high-cost window); at ' + m('r_1') + ' the investor still trades full orders.') +
        nav(back('main:controls')) });

    backup({ id: 'a23', label: 'A23', origin: 'f11', targets: ['app:welfare'], defines: ['D_0'], widget: '',
      title: 'Price level or information?', subtitle: '',
      body:
        ul(['<b>Invariance diagnostic:</b> add a dividend ' + qm('D_0=0.257809', 'base_matched_dividend', '0.257809') + ' (the revenue gain from price access) to the traded claim in the price-hidden economy. Mean prices then match, but entry does not, so the information matters, not the price level. ' + st('(numerical diagnostic)'),
          'The revenue gain itself, ' + q('base_revenue_gain', '0.258') + ', is analytical',
          'Prop. A.9 at ' + m('r_1') + ': each extra entry is chosen only when expected gross profit covers its cost; the allocation gain includes that profit and sales that would otherwise fail the reserve; transfers excluded',
          'The dividend is not a sale mechanism and is excluded from surplus; no ranking of strengths or mechanisms'], 'roomy') +
        nav(back('main:welfare')) });

    backup({ id: 'a24', label: 'A24', origin: 'f12', targets: ['app:corr'], defines: ['r_PNU'], widget: 'x5a',
      title: 'Trading and entry across strengths: entry', subtitle: '',
      body:
        '<div class="figure wide" id="x5a" tabindex="0" aria-label="Figure X5, panel (a). Entry across incumbent strength: branches broken at unresolved nodes, certified intervals, uniqueness shading; arrow keys move the cursor."></div>' +
        '<p class="small">No trade unique for ' + qm(T`r<r_P\approx1.22`, 'base_r_pool_unique_sufficient', '1.22') + ', an equilibrium up to ' + qm(T`r_N\approx1.75`, 'base_r_no_trade_exact', '1.75') + '; full orders unique above ' + qm(T`r_U\approx2.84`, 'base_r_full_unique_sufficient', '2.84') + '; expensive entry impossible above ' + qm(T`r_C\approx3.59`, 'base_r_high_cost_ceiling', '3.59') + ' ' + st('(analytical, Prop. A.4; shaded: unique)') + '; full correspondence open.</p>' +
        nav(go('app:corrb', 'Order sizes'), back('main:corr')) });

    backup({ id: 'a25', label: 'A25', origin: 'a24', targets: ['app:corrb'], defines: [], widget: 'x5b',
      title: 'Trading and entry across strengths: orders', subtitle: '',
      body:
        '<div class="figure wide" id="x5b" tabindex="0" aria-label="Figure X5, panel (b). Order magnitudes across incumbent strength; arrow keys move the cursor."></div>' +
        '<p class="small">No trade is ' + m('(0,0)') + '. Certified nodes: ' + m(T`|q_L|\approx`) + q('cert_a_v_interval', '0.460') + ', ' + q('cert_b_v_interval', '0.707') + ', ' + q('cert_c_v_interval', '0.903') + ' (computer-assisted); the curve through them and the mixed candidate are numerical diagnostics; no branch between nodes is claimed.</p>' +
        nav(back('app:corr')) });

    function t3(row, cells) {
      return cells.map(function (c) { return '<td>' + tx('table3_extensions.tex', row, c[0], c[1]) + '</td>'; }).join('');
    }
    backup({ id: 'a26', label: 'A26', origin: 'f13', targets: ['app:robust'], defines: [], widget: '',
      title: 'Robustness in full', subtitle: '',
      body:
        '<table class="t-full"><thead><tr><th></th><th>' + m(T`\rho`) + '; strengths</th><th>' + m(T`\mathsf E`) + ' weak</th><th>' + m(T`\mathsf E`) + ' strong</th><th>Change (pp)</th><th>' + m(T`\mathsf O_H`) + ' weak</th><th>' + m(T`\mathsf O_H`) + ' strong</th></tr></thead><tbody>' +
          '<tr><th>Laplace, cost atoms</th><td>' + q('base_rho', '0.25') + '; ' + q('base_r_weak', '1.2') + '→' + q('base_r_strong', '3') + '</td>' + t3('Laplace, cost atoms', [[1, '0.250'], [2, '0.523']]) + '<td>' + q('base_entry_change_pp', '27.28') + '</td>' + t3('Laplace, cost atoms', [[4, '0.125'], [5, '0.324']]) + '</tr>' +
          '<tr><th>Laplace, cost mixture</th><td>0.25; 1.2→3</td>' + t3('Laplace, cost mixture', [[1, '0.250']]) + '<td>' + q('cost_mix_laplace_entry_strong', '0.523') + '</td>' + t3('Laplace, cost mixture', [[3, '27.27'], [4, '0.125'], [5, '0.324']]) + '</tr>' +
          '<tr><th>Logistic, cost atoms</th><td>0.25; 1.2→3</td>' + t3('logistic, cost atoms', [[1, '0.250']]) + '<td>' + q('logistic_entry_strong', '0.302') + '</td>' + t3('logistic, cost atoms', [[3, '5.15'], [4, '0.125'], [5, '0.162']]) + '</tr>' +
          '<tr><th>Logistic, cost mixture</th><td>0.25; 1.2→3</td>' + t3('logistic, cost mixture', [[1, '0.250']]) + '<td>' + q('cost_mix_logistic_entry_strong', '0.301') + '</td>' + t3('logistic, cost mixture', [[3, '5.14'], [4, '0.125'], [5, '0.162']]) + '</tr>' +
          '<tr><th>Moderate values (' + m('h=2') + ')</th><td>' + q('moderate_rho', '0.25') + '; ' + q('moderate_r_weak', '1.05') + '→' + q('moderate_r_strong', '1.5') + '</td><td>' + q('moderate_entry_weak', '0.250') + '</td><td>' + q('moderate_entry_strong', '0.527') + '</td><td>' + q('moderate_entry_change_pp', '27.68') + '</td>' + t3('Moderate values', [[4, '0.125'], [5, '0.327']]) + '</tr>' +
          '<tr><th>Signals (' + m('a=0.70') + ', ' + m('d=0.75') + ')</th><td>' + q('signal_rho', '0.85') + '; ' + q('signal_r_weak', '1.1') + '→' + q('signal_r_strong', '2.3') + '</td><td>' + q('signal_entry_weak', '0.850') + '</td><td>' + q('signal_entry_strong', '0.879') + '</td><td>' + q('signal_entry_change_pp', '2.94') + '</td>' + t3('$a=0.70$, $d=0.75$', [[4, '0.425'], [5, '0.449']]) + '</tr>' +
        '</tbody></table>' +
        ul(['Minimum theorem margins: base ' + qm(T`2.41\times10^{-3}`, 'base_minimum_theorem_margin', T`2.41\times10^{-3}`) + ', moderate ' + qm(T`8.01\times10^{-4}`, 'moderate_minimum_theorem_margin', T`8.01\times10^{-4}`) + ', signals ' + qm(T`1.45\times10^{-3}`, 'signal_minimum_theorem_margin', T`1.45\times10^{-3}`),
          'Distinct parameter vectors, not one joint calibration; all rows analytical (Props. 2, A.5–A.7); entry ' + m(T`\mathsf E`) + ' = Pr(challenger prepares), ' + m(T`\mathsf O_H`) + ' = high-value ownership; pp from unrounded probabilities'], 'small') +
        take('The rise from ' + m('r_0') + ' to ' + m('r_1') + ' holds in every row; the ' + m('r_2') + ' fall is shown for the benchmark only.') +
        nav(back('main:robust')) });

    function t4(row, cells) {
      return cells.map(function (c) { return '<td>' + (c[2] ? q(c[2], c[1]) : tx('table4_reserve_comparisons.tex', row, c[0], c[1])) + '</td>'; }).join('');
    }
    var PB = 'Panel B:';
    backup({ id: 'a27', label: 'A27', origin: 'f14', targets: ['app:reserve'], defines: ['eps_V'], widget: '',
      title: 'A higher reserve can raise proceeds; optimal terms are open', subtitle: '',
      body:
        '<p class="small">Value classes: ' + qm('p=0.5', 'base_p', '0.5') + ' vs ' + qm('p=1.1', 'value_reserve_high', '1.1') + ' (' + qm(T`\varepsilon_V=0.05`, 'value_band_halfwidth', '0.05') + ')</p>' +
        '<table class="t-reserve"><thead><tr><th>Economy, reserve</th><th>Preparation</th><th>Sale</th><th>Two admissible bidders</th><th>Expected proceeds</th><th>Trading</th></tr></thead><tbody>' +
          '<tr><th>Weak ' + m('r=1.2') + ', ' + m('p=0.5') + '</th>' + t4(PB + 'Weak ($r=1.2$), $p=0.5$', [[1, '0.250'], [2, '0.688'], [3, '0.146'], [4, '0.393', 'value_revenue_weak_low_p']]) + '<td>no trade</td></tr>' +
          '<tr><th>Weak ' + m('r=1.2') + ', ' + m('p=1.1') + '</th>' + t4(PB + 'Weak ($r=1.2$), $p=1.1$', [[1, '0.540', 'value_entry_weak_high_p'], [2, '0.392'], [3, '0.0280'], [4, '0.432', 'value_revenue_weak_high_p']]) + '<td>full orders</td></tr>' +
          '<tr><th>Strong ' + m('r=3') + ', ' + m('p=0.5') + '</th>' + t4(PB + 'Strong ($r=3$), $p=0.5$', [[1, '0.523'], [2, '0.920'], [3, '0.436'], [4, '0.872', 'value_revenue_strong_low_p']]) + '<td>full orders</td></tr>' +
          '<tr><th>Strong ' + m('r=3') + ', ' + m('p=1.1') + '</th>' + t4(PB + 'Strong ($r=3$), $p=1.1$', [[1, '0.512', 'value_entry_strong_high_p'], [2, '0.749'], [3, '0.200'], [4, '1.01', 'value_revenue_strong_high_p']]) + '<td>full orders</td></tr>' +
        '</tbody></table>' +
        '<p class="grayline">Binary values: ' + qm('p=0.5', 'base_p', '0.5') + ' vs ' + tx('table4_reserve_comparisons.tex', 'Panel A:Weak ($r=1.2$), $p=1.01$', 0, '1.01', null, 'p=1.01') + '. ' + st('Analytical at the listed nodes.') + '</p>' +
        ul(['Preparation, sale and two admissible bidders come apart']) +
        take('A feasible improvement, not an optimal reserve: optimal terms are open.') +
        nav(go('app:pool', 'Same orders, different prices'), back('main:reserve')) });

    backup({ id: 'a28', label: 'A28', origin: 'a27', targets: ['app:pool'], defines: ['kappa'], widget: '',
      title: 'Same orders, different prices', subtitle: '',
      body:
        '<p class="small">Prop. A.10 (analytical existence): at reserve ' + qm('p=7', 'pool_reserve', '7') + ' and ' + m('r_0') + ', the same full orders ' + m('(1,-1)') + ' support price pools below a cutoff ' + m(T`\kappa\in[-\log2,\,0]`) + '.</p>' +
        '<table class="t-pool"><thead><tr><th></th><th>' + m(T`\kappa=-\log2`) + '</th><th>' + m(T`\kappa=0`) + '</th></tr></thead><tbody>' +
          '<tr><th>Pooled belief</th><td>' + q('pool_posterior_cutoff_low', '0.273') + '</td><td>' + q('pool_posterior_cutoff_high', '0.303') + '</td></tr>' +
          '<tr><th>Entry</th><td>' + q('pool_entry_cutoff_low', '0.152') + '</td><td>' + q('pool_entry_cutoff_high', '0.125') + '</td></tr>' +
          '<tr><th>Expected target proceeds</th><td>' + q('pool_revenue_cutoff_low', '0.687') + '</td><td>' + q('pool_revenue_cutoff_high', '0.610') + '</td></tr>' +
        '</tbody></table>' +
        ul(['Same orders, different prices, beliefs, and entry', 'Does not arise on the benchmark support']) +
        take('A continuation must include the price rule, so the seller\'s problem cannot be solved over orders alone.') +
        nav(back('app:reserve')) });

    var REFS = [
      ['Betton, Eckbo, Thompson and Thorburn (2014). <em>J. Finance</em> 69.', 'Boone and Mulherin (2007). <em>J. Finance</em> 62.', 'Bulow, Huang and Klemperer (1999). <em>J. Polit. Econ.</em> 107.',
        'Carlin, Liu, Officer, Pernoud and Tu (2026). NBER Working Paper 34846.', 'Cornelli and Li (2002). <em>Rev. Financ. Stud.</em> 15.', 'Dow, Goldstein and Guembel (2017). <em>J. Eur. Econ. Assoc.</em> 15.',
        'Edmans, Goldstein and Jiang (2012). <em>J. Finance</em> 67.', 'Edmans, Goldstein and Jiang (2015). <em>Amer. Econ. Rev.</em> 105.', 'Fishman (1988). <em>RAND J. Econ.</em> 19.'],
      ['Gentry and Stroup (2019). <em>J. Financ. Econ.</em> 132.', 'Goldstein and Guembel (2008). <em>Rev. Econ. Stud.</em> 75.', 'Grossman and Hart (1980). <em>Bell J. Econ.</em> 11.',
        'Hirshleifer and Png (1989). <em>Rev. Financ. Stud.</em> 2.', 'Imprivata, Inc. (2016). Definitive merger proxy, Form DEFM14A.', 'Levin and Smith (1994). <em>Amer. Econ. Rev.</em> 84.',
        'Lin, Ma, Yang and Zhu (2025). Working paper.', 'Liu and Bernhardt (2022). Working paper.', 'Luo (2005). <em>J. Finance</em> 60.', 'Pernoud and Gleyze (2026). Working paper.',
        'Persico (2000). <em>Econometrica</em> 68.', 'Roberts and Sweeting (2013). <em>Amer. Econ. Rev.</em> 103.']
    ];
    backup({ id: 'a29', label: 'A29', origin: 'f3', targets: ['app:refs'], defines: [], widget: '',
      title: 'References', subtitle: '',
      body: '<div class="refs">' + REFS.map(function (col) { return '<ul>' + col.map(function (r) { return '<li>' + r + '</li>'; }).join('') + '</ul>'; }).join('') + '</div>' + nav(back('main:refs')) });

    /* ================================================================ notation (A12 and the G panel) */
    /* Rows of the A12 table in talk.tex, in the order the symbols are introduced. One source feeds
       the A12 slide and the notation panel. */
    var notation = [
      [[m('R') + '; ' + m('r'), 'incumbent value ' + m(T`R\sim U[0,r]`) + '; ' + m('r') + ' = incumbent strength'],
        [m(T`\theta\in\{H,L\}`) + '; ' + m(T`h,\ell`), 'challenger quality; worth ' + m('h') + ' or ' + m(T`\ell`)],
        [m('p'), 'reserve price (not the stock price)'],
        [m('C') + '; ' + m('c_L,c_H') + '; ' + m(T`\rho`), 'preparation cost; cheap, expensive; ' + m(T`\Pr(C=c_L)`)],
        [m('t_H,t_L'), 'expected target proceeds when a high / low-value challenger enters'],
        [m(T`\Delta_T`), 'target-payoff spread ' + m('t_H-t_L')],
        [m('g_H,g_L'), 'gross acquisition profit of a high / low-value challenger']],
      [[m('r_0,r_1'), 'weak, strong incumbent'],
        [m(T`\mu`), 'market\'s belief ' + m(T`\Pr(H)`) + ' revealed by the price'],
        [m('m,M'), 'bounds on ' + m(T`\mu`) + ': ' + m('m=1/(1+e^{2/b})') + ', ' + m('M=1-m')],
        [m('b'), 'scale of the Laplace noise'],
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
