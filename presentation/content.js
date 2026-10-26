/* content.js: the frames of slot/manuscript/slides.tex as web slides, in the Beamer order.
 *
 * This file is kept by hand. presentation/check_deck.mjs compares it with slides.tex on every
 * build: frame order, labels, titles, subtitles, hypertargets, the link graph, and every registry key
 * that slides.tex prints with \reg{key}. Edit slides.tex first, then this file.
 *
 * Contract. window.createDeck(H) returns { frames, glossary, notation }. H is supplied by the
 * renderer (presentation/render.mjs) or by the check, never by this file:
 *   H.m(latex)                 inline mathematics
 *   H.d(latex)                 display mathematics
 *                              In both, {{key}} prints the registry display of key inside the formula;
 *                              \reg{key} does the same where a subtitle must read as in slides.tex.
 *   H.q(key)                   a registry number in running text: the display that \reg{key} prints.
 *   H.v(key)                   the registry value as a number, for layout only.
 *   H.go(target, text)         a link button to a \hypertarget name, as \hyperlink does.
 *   H.back(target)             the Back button of a backup frame.
 *   H.endFrame(label)          optional; called once per frame after its fields are built.
 * Frame record: { id, label, num, part, title, short, subtitle, targets, minutes, defines, widget,
 *   body, backup, origin }. title is the slides.tex title argument verbatim (empty on Q1, which has
 *   none); short names a frame without a title. Reveals use data-step="n" on elements of the body.
 * ES2019, no modules, no DOM access.
 */
(function () {
  'use strict';
  var T = String.raw;

  function createDeck(H) {
    var m = H.m, d = H.d, q = H.q, go = H.go, back = H.back;
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
    function frame(o) { if (H.endFrame) H.endFrame(o.label); if (o.subtitle === undefined) o.subtitle = ''; F.push(o); }

    /* ================================================================ main frames */

    frame({ id: 'f0', label: 'F0', num: '0', part: 1, minutes: 0.25, targets: [], defines: [], widget: 'title', short: 'Title',
      title: 'Competition Creates Competition: Stock Prices and the Discovery of Takeover Bidders', subtitle: '',
      body: '<div class="cover"><h1>Competition Creates Competition:<br>Stock Prices and the Discovery of Takeover Bidders</h1>' +
        '<p class="cover-author">Austin Li</p><p class="cover-inst">Department of Economics<br>University College London</p>' +
        '<p class="hint">→ or Space to advance · O overview · N notes · G notation · ? help</p></div>' });

    frame({ id: 'q1', label: 'Q1', num: '1', part: 1, minutes: 1.5, targets: [], defines: [], widget: '', short: 'The question', title: '',
      body:
        '<p class="bigq">' + key('Does a stronger bidder in a merger auction<br>scare off its competitor, or draw in more competition?') + '</p>' +
        ul([[1, 'A competitor pays to check the books before it can bid'],
          [2, 'A first bidder bids high at the start to preempt the competitor'],
          [3, 'To the target, one more bidder beats the best negotiation']], 'roomy') +
        '<p class="grayline" data-step="3">Fishman 1988 | Bulow and Klemperer 1996</p>' });

    frame({ id: 'q2', label: 'Q2', num: '2', part: 1, minutes: 1.25, targets: ['main:refs'], defines: [], widget: '',
      title: 'The traditional answer: strength deters entry', subtitle: 'Strength cuts the gain from entry',
      body:
        ul([[0, 'The bidder already in, the <b>incumbent</b>, is ready to bid'],
          [1, 'The next bidder, the <b>challenger</b>, must first <b>prepare</b>: diligence, finance, approvals'],
          [2, 'A stronger incumbent raises the price a victorious challenger pays'],
          [3, 'So preparation pays less, and fewer challengers prepare'],
          [4, 'A challenger prepares only when preparation pays']], 'roomy') +
        gray('Fishman 1988; Hirshleifer and Png 1989 | Samuelson 1985; Levin and Smith 1994') +
        take('A stronger incumbent lowers the return to preparation, so fewer challengers prepare.', 5) +
        nav(go('app:refs', 'References')) });

    frame({ id: 'q3', label: 'Q3', num: '3', part: 1, minutes: 1.0, targets: [], defines: [], widget: '',
      title: 'Competition creates competition', subtitle: 'The channel is information in the stock price',
      body:
        ul([[0, 'An outside investor knows the challenger class and can fill one order slot'],
          [1, 'A stronger incumbent shifts a value gap to target shareholders'],
          [2, 'Sale proceeds then depend more on the challenger class'],
          [3, 'Informed trade pays, so the price becomes informative. Good news then covers a high cost'],
          [4, 'So a stronger incumbent can draw the challenger in']], 'roomy') +
        take(key('The channel is information.') + ' Hold price information fixed, and a stronger incumbent does not raise entry.', 5) });

    frame({ id: 'f1', label: 'F1', num: '4', part: 2, minutes: 1.0, targets: [], defines: [], widget: '',
      title: 'The target is for sale, and its stock still trades', subtitle: 'The decision interval',
      body:
        '<div class="flow flow-3">' +
          '<div class="box" data-step="1">Sale is public; one bidder is already in</div><span class="arrow" data-step="2" aria-hidden="true">→</span>' +
          '<div class="box" data-step="2">Target stock still trades</div><span class="arrow" data-step="3" aria-hidden="true">→</span>' +
          '<div class="box box-cost" data-step="3">Second bidder decides: pay to prepare, or stay out</div>' +
        '</div>' +
        ul([[4, 'One bidder is ready: the <b>incumbent</b>'],
          [4, 'Incumbent type gives a public clue to strength. Incumbent value stays private ' + cite('Gorbenko and Malenko 2014')],
          [5, 'A second bidder is not ready: the <b>challenger</b>'],
          [5, 'To bid, the challenger must first <b>prepare</b>: due diligence, finance, approvals'],
          [5, 'That step costs money and time. The probability that the challenger prepares is <b>entry</b>']]) +
        take('That interval runs from the sale becoming public to the challenger decision.', 6) });

    frame({ id: 'f2', label: 'F2', num: '5', part: 2, minutes: 2.0, targets: ['main:notation'],
      defines: ['R', 'r', 'class', 'pi', 'h', 'ell', 'p', 'rho', 'c_H'], widget: 'infosets', short: 'Model',
      title: 'Model: a second-price auction for the target', subtitle: 'Who moves, who knows what, and when',
      body:
        '<div class="timeline" role="group" aria-label="Timeline; select a step to see its information set">' +
          '<button type="button" class="tl" data-info="seller"><span class="tl-n">1</span><b>Seller</b>announces the sale rule before any trade</button>' +
          '<button type="button" class="tl" data-info="slot"><span class="tl-n">2</span><b>Order slot</b>one unit order reaches the market</button>' +
          '<button type="button" class="tl" data-info="makers"><span class="tl-n">3</span><b>Market makers</b>see the order only; set the stock price</button>' +
          '<button type="button" class="tl tl-cost" data-info="challenger"><span class="tl-n">4</span><b>Challenger</b>sees the price and its own cost; prepares or stays out</button>' +
          '<button type="button" class="tl" data-info="bidders"><span class="tl-n">5</span><b>Bidders</b>the incumbent and a prepared challenger bid values</button>' +
        '</div>' +
        '<p class="infoset" id="f2-infoset" aria-live="polite">Select a step to see what that agent observes.</p>' +
        ul([[1, '<b>Sale rule:</b> cash second-price auction with reserve ' + m('p') + '. The top bid wins and pays ' + m(T`\max\{p,\text{other bid}\}`) + '. Each bidder bids its value'],
          [2, '<b>Incumbent:</b> value ' + m(T`R\sim U[0,r]`) + '. Strength ' + m('r') + ' is public; only the incumbent knows ' + m('R')],
          [3, '<b>Challenger:</b> class ' + m(T`j\in\{H,L\}`) + ', prior ' + m(T`\pi`) + ' on ' + m('H') + ', value from ' + m('G_j') + '. The example uses point masses ' + m('h') + ' and ' + m(T`\ell`)],
          [3, 'The challenger learns its value after preparation, not before'],
          [4, cost('<b>Cost:</b> zero with probability ' + m(T`\rho`) + ', else ' + m('c_H>0') + ', with no link to class')]], 'small') +
        nav(go('app:notation', 'Notation')) });

    frame({ id: 'f3', label: 'F3', num: '6', part: 2, minutes: 2.0, targets: [],
      defines: ['Delta_T', 'tj', 'gj', 'B', 'mu', 'r_01'], widget: 'cases',
      title: 'One auction, two claims, opposite responses', subtitle: 'Who wins and who pays at incumbent value ' + m('R') + '; in the example ' + m(T`p<\ell<r<h`),
      body:
        '<div class="segmented" role="group" aria-label="Incumbent value"><button type="button" data-case="low" aria-pressed="false">' + m(T`R\le\ell`) + '</button><button type="button" data-case="high" aria-pressed="false">' + m(T`R>\ell`) + '</button></div>' +
        '<table class="t-cases"><thead><tr><th>Incumbent value</th><th>Class ' + m('H') + ' challenger</th><th>Class ' + m('L') + ' challenger</th><th>Gap in target proceeds</th></tr></thead><tbody>' +
          '<tr data-row="low"><td>' + m(T`R\le\ell`) + '</td><td>wins, pays ' + m(T`\max\{p,R\}`) + '</td><td>wins, pays ' + m(T`\max\{p,R\}`) + '</td><td class="gap">' + m('0') + '</td></tr>' +
          '<tr data-row="high"><td>' + m(T`R>\ell`) + '</td><td>wins, pays ' + m('R') + '</td><td>loses; incumbent pays ' + m(T`\ell`) + '</td><td class="gap">' + m(T`R-\ell`) + '</td></tr>' +
        '</tbody></table>' +
        '<p class="small" data-step="1">As incumbent strength ' + m('r') + ' rises:</p>' +
        '<div class="two-lines" data-step="1">' +
          '<div class="info">' + m(T`\Delta_T=t_H-t_L=\mathbb{E}[(R-\ell)_+]`) + ' <span class="arrowword">↑</span><span class="gloss">target-payoff spread</span></div>' +
          '<div>' + m('g_j') + ' <span class="arrowword">↓</span><span class="gloss">class ' + m('j') + ' auction profit before cost</span></div>' +
          '<div>' + m(T`B_r(\mu)=g_L+\mu(g_H-g_L)`) + ' <span class="arrowword">↓</span><span class="gloss">gross profit at belief ' + m(T`\mu`) + '</span></div>' +
        '</div>' +
        gray(m('t_j') + ' is expected target proceeds with a class ' + m('j') + ' challenger. Proposition 1: profit falls weakly under any first-order strengthening; the spread rises weakly for ranked classes.') +
        '<p class="small" data-step="2">In the example, the spread moves ' + q('Delta_r0') + ' → ' + q('Delta_r1') + ' from ' + m('r_0') + ' to ' + m('r_1') + ', and profit at the prior moves ' + q('Bprior_r0') + ' → ' + q('Bprior_r1_B') + '.</p>' +
        take('Challenger profit falls weakly. The target-payoff spread rises weakly.', 3) });

    frame({ id: 'f4', label: 'F4', num: '7', part: 3, minutes: 1.75, targets: ['main:slot'],
      defines: ['lambda', 'q', 'k', 'beta', 'X', 'P', 'V_T', 'b', 'u'], widget: '',
      title: 'The order slot: one trade before the decision', subtitle: 'The challenger sees the price, not the order and not the class',
      body:
        '<div class="slotflow">' +
          '<div class="slotsrc">' +
            '<div class="sbox" data-step="1"><b>Informed investor</b><span class="chance">with probability ' + m(T`\lambda`) + '</span>sees class ' + m('j') + '; picks ' + m(T`q\in\{-1,0,1\}`) + '. A nonzero order costs ' + m('k') + '</div>' +
            '<div class="sbox" data-step="2"><b>Liquidity trader</b><span class="chance">with probability ' + m(T`1-\lambda`) + '</span>sale, no order or buy, with chances ' + m(T`\beta,\ 1-2\beta,\ \beta`) + '</div>' +
          '</div>' +
          '<span class="arrow" data-step="3" aria-hidden="true">→</span>' +
          '<div class="sbox slotbox" data-step="3"><b>Order slot</b>one public order ' + m(T`X\in\{-1,0,1\}`) + '<small>no observer sees who filled it; the draw has no link to class, costs or ' + m('R') + '</small></div>' +
          '<span class="arrow" data-step="4" aria-hidden="true">→</span>' +
          '<div class="sbox" data-step="4"><b>Market makers</b>see ' + m('X') + ' and set<br>' + m(T`P=\mathbb{E}[V_T\mid X]`) + '<small>' + m('V_T') + ' = sale proceeds per share</small></div>' +
          '<span class="arrow" data-step="5" aria-hidden="true">→</span>' +
          '<div class="sbox sbox-cost" data-step="5"><b>Challenger</b>sees ' + m('P') + '<small>not ' + m('X') + ', not ' + m('j') + '</small></div>' +
        '</div>' +
        '<p class="small" data-step="6">Set ' + m(T`b=(1-\lambda)\beta`) + ' and ' + m(T`u=\lambda/b`) + ': the informed presence mass relative to the liquidity mass in one direction. The number ' + m('1+u') + ' is the largest likelihood ratio of an order. The bound ' + m(T`0<\beta\le 1/3`) + ' holds throughout. An indifferent investor may mix over its best orders and an indifferent high-cost challenger prepares.</p>' +
        take('Every order can come from either class. No price reveals the class with certainty.', 7) +
        nav(go('app:slot', 'Equilibrium object')) });

    frame({ id: 'f5', label: 'F5', num: '8', part: 3, minutes: 1.75, targets: ['main:belief'],
      defines: ['m_M', 'e_r', 't_0'], widget: 'orders',
      title: 'The price tells the challenger a bounded belief', subtitle: 'Belief ' + m(T`\mu=\Pr(H\mid P)`) + ' and the entry rule ' + m(T`e_r(\mu)`),
      body:
        d(T`m(\pi)=\frac{\pi}{\pi+(1-\pi)(1+u)}\ \le\ \mu\ \le\ \frac{\pi(1+u)}{\pi(1+u)+1-\pi}=M(\pi)\qquad\text{for every investor strategy}`) +
        '<div class="segmented" role="group" aria-label="Order in the slot"><button type="button" data-order="-1" aria-pressed="false">Sale ' + m('X=-1') + '</button><button type="button" data-order="0" aria-pressed="false">No order ' + m('X=0') + '</button><button type="button" data-order="1" aria-pressed="false">Buy ' + m('X=1') + '</button></div>' +
        '<table class="t-orders"><thead><tr><th>Full orders at the example’s prior</th><th data-order="-1">Sale ' + m('X=-1') + '</th><th data-order="0">No order ' + m('X=0') + '</th><th data-order="1">Buy ' + m('X=1') + '</th></tr></thead><tbody>' +
          '<tr><td>Belief ' + m(T`\mu`) + '</td><td data-order="-1">' + q('m_half_B') + '</td><td data-order="0">' + q('prim_pi') + '</td><td data-order="1">' + q('M_half_B') + '</td></tr>' +
        '</tbody></table>' +
        '<div class="beliefbar" id="f5-bar" aria-hidden="true"><div class="track"><div class="band" style="left:' + (100 * H.v('m_half_B')).toFixed(2) + '%;width:' + (100 * (H.v('M_half_B') - H.v('m_half_B'))).toFixed(2) + '%"></div>' +
          '<span class="tick" style="left:' + (100 * H.v('m_half_B')).toFixed(2) + '%"></span><span class="tick" style="left:50%"></span><span class="tick" style="left:' + (100 * H.v('M_half_B')).toFixed(2) + '%"></span>' +
          '<span class="pin" id="f5-pin" hidden></span></div><div class="scale"><span style="left:0">0</span><span style="left:' + (100 * H.v('m_half_B')).toFixed(2) + '%">' + m('m') + '</span><span style="left:50%">' + m('\\pi') + '</span><span style="left:' + (100 * H.v('M_half_B')).toFixed(2) + '%">' + m('M') + '</span><span style="left:100%">1</span></div></div>' +
        '<p class="infoset" id="f5-say" aria-live="polite">Select an order to see where the belief goes.</p>' +
        ul([[1, 'Price at belief ' + m(T`\mu`) + ': ' + m(T`P_r(\mu)=t_0+e_r(\mu)\bigl(t_L-t_0+\Delta_T\mu\bigr)`)],
          [1, 'Entry rule: ' + m(T`e_r(\mu)=\rho+(1-\rho)\,\mathbf{1}\{B_r(\mu)\ge c_H\}`) + ', since the zero cost always pays'],
          [1, 'Entry at least ' + m(T`\rho`) + ' and ' + m(T`\Delta_T>0`) + ' let the challenger recover ' + m(T`\mu`) + ' from ' + m('P')]], 'small') +
        take('A buy order moves belief up to ' + m('M(\\pi)') + '. Belief stays short of one.', 2) +
        nav(go('app:belief', 'Posterior bounds')) });

    function tr3(a, b, c, step) {
      return '<tr' + (step !== undefined ? ' data-step="' + step + '"' : '') + '><td>' + a + '</td><td>' + b + '</td><td>' + c + '</td></tr>';
    }
    frame({ id: 'f6', label: 'F6', num: '9', part: 3, minutes: 1.0, targets: ['main:bench'], defines: ['r_2'], widget: '',
      title: 'The example: only incumbent strength changes', subtitle: 'Declared inputs; units are arbitrary',
      body:
        '<table class="t-inputs"><thead><tr><th>Input</th><th>Value</th><th>Meaning</th></tr></thead><tbody>' +
          tr3(m(T`h,\ \ell`), q('prim_h') + ', ' + q('prim_ell'), 'class ' + m('H') + ' and class ' + m('L') + ' values', 1) +
          tr3(m('p'), q('prim_p'), 'reserve price', 1) +
          tr3(m(T`\pi,\ \rho`), q('prim_pi') + ', ' + q('prim_rho'), 'prior on ' + m('H') + '; probability of zero cost', 2) +
          tr3('Costs ' + m(T`0,\ c_H,\ k`), '0, ' + q('prim_cH') + ', ' + q('prim_k'), 'preparation costs; cost of a nonzero order', 2) +
          tr3(m(T`\beta,\ \lambda`), q('beta_B') + ', ' + q('lambda_B'), 'liquidity order chance; informed presence chance', 3) +
          tr3(m(T`u,\ b`), q('u_B') + ', ' + q('b_B'), 'mass ratio ' + m(T`u=\lambda/b`) + '; here ' + m(T`1+u=e`), 3) +
          tr3(m(T`r_0,\ r_1,\ r_2`), q('prim_r0') + ', ' + q('prim_r1') + ', ' + q('prim_r2'), 'weak, strong, stronger still', 4) +
        '</tbody></table>' +
        gray('The inputs illustrate the results.') +
        take('Comparisons vary ' + m('r') + ' across ' + m('r_0') + ', ' + m('r_1') + ' and ' + m('r_2') + ' and hold all else fixed.', 4) +
        nav(go('app:bench', 'Recruitment region')) });

    frame({ id: 'f7', label: 'F7', num: '10', part: 4, minutes: 2.5, targets: [], defines: ['kappa', 'q_HL'], widget: 'gain',
      title: 'Trade pays only against a strong incumbent', subtitle: 'Residual gain per unit, before the order cost ' + m('k') + '; Lemma A.3',
      body:
        '<div class="split gainsplit">' +
          '<div class="col">' +
            ul([[1, 'Buy after ' + m('H') + ': expected share payoff less price. Sell after ' + m('L') + ': price less expected share payoff'],
              [2, 'Each correct order earns at most ' + info(m(T`\Delta_T`)) + ' before cost, under every profile'],
              [3, 'Set ' + m(T`\kappa=\min\{m,1-M\}`) + '. Each correct order earns at least ' + m(T`\rho\kappa`) + info(m(T`\Delta_T`)) + ' before cost']], 'small') +
            '<table class="t-trade" data-step="4"><thead><tr><th></th><th>Trading bound</th><th>Orders ' + m('(q_H,q_L)') + '</th></tr></thead><tbody>' +
              '<tr><th>Weak ' + m('r_0') + '</th><td class="nw">' + info(m(T`\Delta_T(r_0)={{Delta_r0}}`)) + ' ' + m(T`<k={{prim_k}}`) + '</td><td>' + m('(0,0)') + ': quiet market</td></tr>' +
              '<tr><th>Strong ' + m('r_1') + '</th><td class="nw">' + m(T`\rho\kappa\,\Delta_T(r_1)-k={{margin_kstrong_B}}>0`) + '</td><td>' + m('(1,-1)') + ': full orders</td></tr>' +
            '</tbody></table>' +
            gray(info('<b>Trading-cost window (H2):</b>') + ' ' + m(T`\Delta_T(r_0)<k<\rho\kappa\,\Delta_T(r_1)`) + ', at prior ' + m(T`\pi`) + '.') +
          '</div>' +
          '<div class="col"><div class="figure" id="gain" tabindex="0" aria-label="Figure. The gain of a correctly signed order against incumbent strength, in units of the order cost k, between its floor and its ceiling; arrow keys move the cursor."></div></div>' +
        '</div>' +
        take('The same rise in ' + m('r') + ' that lowers challenger profit makes a correct order cover ' + m('k') + '.', 4) });

    frame({ id: 'f8', label: 'F8', num: '11', part: 4, minutes: 2.25, targets: [], defines: ['tau', 'r_C'], widget: 'beliefs',
      title: 'Only good news makes high-cost preparation pay', subtitle: 'Preparation threshold ' + m(T`\tau(r)=(c_H-g_L)/(g_H-g_L)`) + ', with ' + m(T`B_r(\tau)=c_H`),
      body:
        '<div class="split beliefsplit">' +
          '<div class="col">' +
            '<div class="figure" id="beliefs" tabindex="0" aria-label="Figure. The threshold belief against incumbent strength, with the band of beliefs a price can induce."></div>' +
            '<div class="slider"><label for="beliefs-r">incumbent strength ' + m('r') + '</label><input type="range" id="beliefs-r" min="0" max="240" step="1" value="180"><output id="beliefs-r-value" for="beliefs-r">3.00</output></div>' +
          '</div>' +
          '<div class="col text">' +
            ul([[1, 'Zero cost always pays; cost ' + m('c_H') + ' pays exactly at beliefs at or past ' + m(T`\tau(r)`)],
              [2, 'Preparation thresholds: <span class="nw">' + m(T`\tau(r_0)={{tau_r0}}`) + '</span>, <span class="nw">' + m(T`\tau(r_1)={{tau_r1}}`) + '</span>, <span class="nw">' + m(T`\tau(r_2)={{tau_r2}}`) + '</span>; top posterior <span class="nw">' + m(T`M={{M_half_B}}`) + '</span>'],
              [3, 'At ' + m('r_1') + ', a purchase clears the threshold. Past the entry ceiling ' + m('r_C') + ', no order clears it']], 'small') +
            '<div id="beliefs-readout" class="readout" aria-live="polite"></div>' +
          '</div>' +
        '</div>' +
        take('The entry ceiling ' + m('r_C') + ' sits just below ' + m('r_2') + '.', 3) });

    frame({ id: 'f9', label: 'F9', num: '12', part: 4, minutes: 2.0, targets: ['main:prop2'], defines: ['F_W'], widget: '',
      title: 'Proposition 2: a stronger incumbent can raise entry', subtitle: 'Weak ' + m('r_0') + ', strong ' + m('r_1') + ', stronger still ' + m('r_2') + '; all other inputs equal',
      body:
        '<div class="resultbox"><p class="resultbox-title">Proposition 2, under the conditions below</p>' +
          '<p class="propitem" data-step="0"><span class="propnum">(i)</span><b>Weak ' + m('r_0') + ':</b> quiet market, ' + m('(q_H,q_L)=(0,0)') + '; price flat; entry ' + m(T`=\rho`) + '</p>' +
          '<p class="propitem" data-step="1"><span class="propnum">(ii)</span><b>Strong ' + m('r_1') + ':</b> full orders ' + m('(1,-1)') + '; price informative; entry ' + m(T`>\rho`) + '</p>' +
          '<p class="propitem" data-step="2"><span class="propnum">(iii)</span><b>Stronger still ' + m('r_2') + ':</b> full orders; price informative; entry back to ' + m(T`\rho`) + '</p>' +
        '</div>' +
        '<table class="t-conditions" data-step="3"><tbody>' +
          '<tr><td>' + cost('<b>(H1) High-cost window</b>') + '</td><td>' + m(T`B_{r_0}(\pi)<c_H<B_{r_1}(M)`) + '</td></tr>' +
          '<tr><td>' + info('<b>(H2) Trading-cost window</b>') + '</td><td>' + m(T`\Delta_T(r_0)<k<\rho\kappa\,\Delta_T(r_1),\ \kappa=\min\{m,1-M\}`) + '</td></tr>' +
          '<tr><td><b>(H3) Exclusion condition</b></td><td>' + m(T`B_{r_2}(M)<c_H`) + '</td></tr>' +
        '</tbody></table>' +
        '<p class="small" data-step="4">Ownership in part (ii) rises exactly if ' + m(T`[\rho+(1-\rho)(b+\lambda)]\,W_H(F_1)>\rho\,W_H(F_0)`) + ', with ' + m('W_H(F)') + ' as the class ' + m('H') + ' win chance at reserve ' + m('p') + '. If class ' + m('H') + ' outbids ' + m('F_1') + ', ownership rises and class ' + m('H') + '’s takeover share does not fall.</p>' +
        gray('The outcome is unique in each part, under all four tie rules. Each condition is a strict inequality: the parts hold on an open set of inputs.') +
        take(info('wider ' + m(T`\Delta_T`) + ' → trade pays → informative price → good news clears ' + m('c_H') + ' → entry at high cost'), 5) +
        nav(go('app:prop2', 'Proof structure')) });

    frame({ id: 'f10', label: 'F10', num: '13', part: 5, minutes: 1.5, targets: ['main:outcome'], defines: [], widget: '',
      title: 'In the example, entry rises and then returns', subtitle: 'Corollary 1: unique orders and entry at on-path prices',
      body:
        '<p class="small-note">Entry is the probability that the challenger prepares. Ownership is the probability that a class ' + m('H') + ' challenger acquires the target.</p>' +
        '<table class="t-bench with-r2"><thead><tr><th></th><th>weak ' + m('r_0') + '</th><th class="strong">strong ' + m('r_1') + '</th><th>stronger still ' + m('r_2') + '</th></tr></thead><tbody>' +
          '<tr data-step="1"><th>Strength ' + m('r') + '</th><td>' + q('prim_r0') + '</td><td class="strong">' + q('prim_r1') + '</td><td>' + q('prim_r2') + '</td></tr>' +
          '<tr data-step="1"><th>Gross profit at prior ' + m(T`B_r(\pi)`) + '</th><td>' + q('Bprior_r0') + '</td><td class="strong">' + q('Bprior_r1_B') + '</td><td>' + q('Bprior_r2') + '</td></tr>' +
          '<tr data-step="1"><th>' + info('Spread ' + m(T`\Delta_T`)) + '</th><td>' + q('Delta_r0') + '</td><td class="strong">' + q('Delta_r1') + '</td><td>' + q('Delta_r2') + '</td></tr>' +
          '<tr data-step="2"><th>Orders ' + m('(q_H,q_L)') + '</th><td>' + m('(0,0)') + '</td><td class="strong">' + m(T`\boldsymbol{(1,-1)}`) + '</td><td>' + m('(1,-1)') + '</td></tr>' +
          '<tr data-step="2"><th>Price</th><td>flat</td><td class="strong">informative</td><td>informative</td></tr>' +
          '<tr data-step="3"><th>Entry</th><td>' + q('entry_r0') + '</td><td class="strong">' + q('entry_r1_B') + '</td><td>' + q('entry_r2') + '</td></tr>' +
          '<tr data-step="3"><th>Class ' + m('H') + ' ownership</th><td>' + q('own_r0') + '</td><td class="strong">' + q('own_r1_B') + '</td><td>' + q('own_r2_B') + '</td></tr>' +
        '</tbody></table>' +
        gray('Corollary 1: (H1)–(H3) hold together exactly for ' + m(T`{{u_lo_frac}}<u<{{u_hi_frac}}`) + ', that is, ' + m(T`\tau(r_1)<M<\tau(r_2)`) + '; here ' + m(T`u={{u_B}}`) + '.') +
        take('Past the entry ceiling ' + m(T`r_C\approx{{rC_B}}`) + ', the top posterior cannot cover ' + m('c_H') + '.', 4) +
        nav(go('app:outcome', 'Entry formulas')) });

    frame({ id: 'f11', label: 'F11', num: '14', part: 5, minutes: 1.75, targets: [], defines: [], widget: 'controls',
      title: 'Hold information fixed: a stronger incumbent can only lower entry', subtitle: 'Entry at ' + m('r_0') + ' and ' + m('r_1') + ' in the full model and in two controls; Proposition A.2',
      body:
        '<div class="segmented" role="group" aria-label="Which row"><button type="button" data-row="eq" aria-pressed="true">Full model</button><button type="button" data-row="frozen" aria-pressed="false">Same full orders</button><button type="button" data-row="hidden" aria-pressed="false">Price hidden</button></div>' +
        '<div class="split wide">' +
        '<table class="t-controls"><thead><tr><th></th><th>' + m('r_0') + '</th><th>' + m('r_1') + '</th><th>Direction</th></tr></thead><tbody>' +
          '<tr data-row="eq"><th>Full model: price seen, trade re-solved</th><td>' + q('entry_r0') + '</td><td><b>' + q('entry_r1_B') + '</b></td><td>up</td></tr>' +
          '<tr data-row="frozen"><th>Same full orders at both strengths</th><td>' + q('p4_frozen_r0_entry') + '</td><td>' + q('p4_frozen_r1_entry') + '</td><td>constant</td></tr>' +
          '<tr data-row="hidden"><th>Price hidden from the challenger</th><td>' + q('p4_hidden_r0_entry') + '</td><td>' + q('p4_hidden_r1_entry') + '</td><td>constant</td></tr>' +
        '</tbody></table>' +
        '<div class="bars" id="f11-bars" aria-live="polite"></div>' +
        '</div>' +
        ul([[1, 'Given the class and the signal, the two values keep their class and incumbent laws, and cost is independent of class, values and signal. A stronger incumbent then cuts ' + m(T`B_r(\mu)`) + ' at each belief: entry can only fall'],
          [2, 'Frozen full orders give the same entry up to the entry ceiling ' + m('r_C') + ', then ' + m(T`\rho`) + '. At ' + m('r_0') + ' the control is not an equilibrium'],
          [3, 'With the price hidden, cost ' + m('c_H') + ' never pays at the prior, so entry stays at ' + m(T`\rho`)]], 'small') +
        take('The rise comes from a change in what the price reveals. At a fixed belief, a stronger incumbent weakly lowers gross profit.', 4) });

    frame({ id: 'f12', label: 'F12', num: '15', part: 6, minutes: 0.75, targets: [], defines: [], widget: 'region',
      title: 'Quiet and informative markets coexist', subtitle: 'Proposition 3 at a fixed presence probability ' + m(T`\lambda`) + ': where both exist',
      body:
        '<div class="split regionsplit">' +
          '<div class="col"><div class="figure" id="region" tabindex="0" aria-label="Figure. The coexistence region in the plane of the target-payoff spread and the preparation threshold, with the path of the example from weak to strong incumbents; arrow keys move the cursor."></div></div>' +
          '<div class="col text">' +
            ul([[1, 'A quiet market and an informative market coexist exactly when' + d(T`\begin{gathered}\pi<\tau\le M(\pi),\\[2pt] \frac{k}{1-\tau}\le\Delta_T\le\frac{k}{\rho\max\{\pi,1-\pi\}}\end{gathered}`)],
              [2, 'The informative market is then unique: class ' + m('L') + ' abstains, only a purchase recruits a high-cost challenger'],
              [3, 'Entry rises with the spread while class ' + m('H') + ' mixes its purchase, and is constant once it buys for sure'],
              [4, 'Lower bound: a purchase that reaches ' + m(T`\tau`) + ' covers ' + m('k') + '. Upper bound: an order against a flat price earns at most ' + m('k')]], 'small') +
          '</div>' +
        '</div>' +
        take('The spread and the preparation threshold decide where both markets exist.', 5) });

    frame({ id: 'f12b', label: 'F12b', num: '16', part: 6, minutes: 0.75, targets: ['main:coex'], defines: ['r_AFNJS'], widget: 'coex',
      title: 'In the example, coexistence runs from $r_A$ to $r_N$', subtitle: 'Corollary 2: entry along the path of strengths',
      body:
        '<div class="figure wide nolegend" id="coex" tabindex="0" aria-label="Figure. Entry against incumbent strength in each equilibrium of the example, with the coexistence band; arrow keys move the cursor."></div>' +
        '<p class="small keyline"><b class="k-n">N</b> quiet market <b class="k-r">R</b> mixed purchase that recruits <b class="k-r">F</b> full purchase <b class="k-q">Q</b> mixed orders at the entry floor <b class="k-t">T</b> threshold pair</p>' +
        ul([[1, 'On ' + m(T`[{{rA}},{{rN}}]`) + ', a quiet market and an informative market coexist; class ' + m('H') + ' mixes its purchase up to ' + q('rF_B') + ' and buys for sure from there'],
          [2, 'Entry rises strictly on ' + m('[r_A,r_F]') + ', stays at ' + q('entry_r1_B') + ' up to the entry ceiling ' + m('r_C') + ' and returns to ' + m(T`\rho`) + ' above it'],
          [3, 'The path uses the slot band of Corollary 1, ' + m(T`\tau(r_1)<M<\tau(r_2)`)]], 'small') +
        take('Coexistence spans ' + m('[r_A,r_N]') + '.', 3) +
        nav(go('app:coex', 'Marked strengths')) });

    frame({ id: 'f13', label: 'F13', num: '17', part: 6, minutes: 1.5, targets: ['main:research'], defines: ['a_cap', 'r_R'], widget: 'research',
      title: 'Competition creates research', subtitle: 'Proposition 4 at the prior ' + m(T`\reg{prim_pi}`) + ': costly research sets presence ' + m(T`\lambda`) + ', with a cap ' + m(T`\bar\lambda`),
      body:
        '<p class="small">Research costs ' + m(T`\tfrac{a}{2}\lambda^2`) + '. A success reveals the class and fills the slot. When a purchase recruits, research rises with the spread up to the cap, and entry rises with research. At ' + q('str_r155') + ', ' + q('str_r160') + ', ' + q('str_r165') + ' research is ' + q('res_lambda_r155') + ', ' + q('res_lambda_r160') + ', ' + q('res_lambda_r165') + ' and entry is ' + q('res_entry_r155') + ', ' + q('res_entry_r160') + ', ' + q('res_entry_r165') + '.</p>' +
        '<div class="figure wide nolegend" id="research" tabindex="0" aria-label="Figure. Research and entry against incumbent strength in each research equilibrium of the example; arrow keys move the cursor."></div>' +
        '<p class="grayline" data-step="1">Corollary 3: zero research on ' + m('[r_0,r_N]') + '; recruiting research on ' + m(T`[r_R,r_C]\approx[{{res_rR}},{{res_rC}}]`) + ', below the cap until ' + m(T`r_{\bar\lambda}\approx{{res_rcap}}`) + ' and at the cap from there, with entry rising from ' + q('res_entry_rR') + ' to ' + q('res_entry_cap') + ' and then constant; floor-entry research on ' + m('(r_N,r_Q)') + ' and on ' + m('(r_C,r_2]') + '.</p>' +
        take('Research and entry rise together; research at the cap holds up to the entry ceiling ' + m('r_C') + '.', 2) +
        nav(go('app:research', 'Research in detail')) });

    function rrow(a, b) { return '<tr><th>' + a + '</th><td>' + b + '</td></tr>'; }
    frame({ id: 'f14', label: 'F14', num: '18', part: 6, minutes: 1.0, targets: ['main:robust'], defines: ['omega'], widget: '',
      title: 'The reversal survives changes to the model', subtitle: 'Each row keeps the slot and varies one part of the set-up',
      body:
        '<table class="t-robust roomy"><thead><tr><th>Change</th><th>Result</th></tr></thead><tbody>' +
          '<tr data-step="1"><th>Preparation cost laws (A.3)</th><td>Reversal holds with atoms or none; entry at ' + m('r_1') + ' equals ' + q('p4_atomless_r1_entry') + ' with the example’s band</td></tr>' +
          '<tr data-step="2"><th>Value classes, priors (A.4, A.5)</th><td>Holds for every ranked pair and prior at suitable costs; at the example’s costs the prior range is ' + m(T`({{prior_lo_B}},\,{{prior_hi_B}})`) + '; many classes need separation</td></tr>' +
          '<tr data-step="3"><th>Complementary signals (A.6)</th><td>In the example, with accuracies ' + m(T`({{sig_comp_aT}},\,{{sig_comp_d}})`) + ', entry ' + q('p4_comp_b_r0_entry') + ' → ' + q('p4_comp_b_r1_entry') + '</td></tr>' +
          '<tr data-step="4"><th>Payment rule (A.8)</th><td>The spread response weakly has the sign of ' + m(T`1-2\omega`) + ' for seller share ' + m(T`\omega`) + '; sale terms sit in the next frame</td></tr>' +
        '</tbody></table>' +
        take('One slot and unit orders carry the result across cost, value and signal variants.', 5) +
        nav(go('app:robust', 'Extensions'), go('app:sizes', 'Order sizes')) });

    frame({ id: 'f15', label: 'F15', num: '19', part: 6, minutes: 1.0, targets: ['main:welfare'], defines: [], widget: 'access',
      title: 'Price access raises proceeds and surplus', subtitle: 'Proposition A.7 at ' + m('r_1') + ': price seen or price hidden, trade re-solved',
      body:
        '<div class="segmented" role="group" aria-label="Highlight a column"><button type="button" data-col="1" aria-pressed="false">Price seen</button><button type="button" data-col="2" aria-pressed="false">Price hidden</button></div>' +
        '<table class="t-access roomy"><thead><tr><th></th><th data-col="1">Price seen</th><th data-col="2">Price hidden</th><th>Gain</th></tr></thead><tbody>' +
          '<tr><th>Expected target proceeds</th><td data-col="1">' + q('p2_base_r1_proceeds') + '</td><td data-col="2">' + q('p2_base_hidden_proceeds') + '</td><td>' + q('p2_access_proceeds_gain') + '</td></tr>' +
          '<tr><th>Surplus net of preparation costs</th><td data-col="1">' + q('p2_base_r1_surplus') + '</td><td data-col="2">' + q('p2_base_hidden_surplus') + '</td><td>' + q('p2_access_surplus_gain') + '</td></tr>' +
        '</tbody></table>' +
        ul([[1, 'Surplus is acquisition surplus net of preparation costs; transfers net out'],
          [2, 'Price access adds preparation only after a purchase, at beliefs that cover ' + m('c_H')],
          [3, 'Reserves (A.9): at a reserve that excludes the low class entry is flat; strict deterrence at ' + q('rsv_deter') + ' also excludes the weak incumbent']], 'roomy') +
        nav(go('app:welfare', 'Sale terms in detail')) });

    frame({ id: 'f16', label: 'F16', num: '20', part: 7, minutes: 1.0, targets: [], defines: [], widget: '',
      title: 'Empirical implications', subtitle: 'Public sales with a ready incumbent and a challenger free to prepare; Propositions A.10–A.13',
      body:
        ul([[1, '<b>Entry:</b> a stronger incumbent can raise preparation starts, at prices set before the start; with the price hidden, it can only lower them'],
          [2, '<b>Price gap:</b> under full two-sided trade at a prior below the preparation threshold, the weighted purchase impact exceeds the weighted sale impact exactly when a purchase recruits. At ' + m('r_1') + ' the price gap is ' + q('ba_r1_B') + ', with entry component ' + q('ba_share_r1_B') + ' of it; above ' + m('r_C') + ' the entry component is zero'],
          [3, '<b>Informed share:</b> full two-sided trade is the unique outcome for ' + m(T`r_S<r<h`) + ', ' + m(T`r_S\approx{{rS_B}}`) + '. With entry ' + m(T`\rho`) + ' after a sale and no order and ' + m(T`\rho\Delta_T`) + ' known, the sale impact and the mean order then identify presence and prior'],
          [4, '<b>Winners:</b> under full two-sided trade, orders predict the winner when class ' + m('H') + ' outbids class ' + m('L') + ', even above the entry ceiling ' + m('r_C') + ', where they no longer predict entry']], 'mid') +
        gray('The outcome is the start of costly preparation. A valid test uses the price before that start. Returns before a bid can also reflect an expected bid (Schwert 1996).') +
        take('Strength, early prices and preparation starts must be measured together.', 5) });

    frame({ id: 'f17', label: 'F17', num: '21', part: 7, minutes: 0.75, targets: [], defines: [], widget: '',
      title: 'Conclusion', subtitle: '',
      body:
        ul([[0, key('A stronger incumbent can bring the challenger in:') + ' in the example, entry ' + q('entry_r0') + ' → ' + q('entry_r1_B') + ', then back to ' + q('entry_r2') + ' at ' + m('r_2')],
          [1, '<b>Why:</b> strength shifts a value gap to shareholders, trade pays in the slot, and a buy order makes high-cost preparation pay'],
          [2, '<b>Implication:</b> competition in the auction can create competition for entry, via the stock price before preparation']], 'conclusion') });

    /* ================================================================ backup frames */

    function backup(o) { o.part = 'B'; o.minutes = 0; o.backup = true; o.num = o.label; o.defines = o.defines || []; o.widget = o.widget || ''; frame(o); }

    var REFS = [
      ['Betton, Eckbo, Thompson and Thorburn (2014). <em>J. Finance</em> 69.', 'Bond, Edmans and Goldstein (2012). <em>Annu. Rev. Financ. Econ.</em> 4.', 'Boone and Mulherin (2007). <em>J. Finance</em> 62.',
        'Bulow and Klemperer (1996). <em>Amer. Econ. Rev.</em> 86.', 'Dow and Gorton (1997). <em>J. Finance</em> 52.', 'Dow, Goldstein and Guembel (2017). <em>J. Eur. Econ. Assoc.</em> 15.',
        'Edmans, Goldstein and Jiang (2012). <em>J. Finance</em> 67.', 'Edmans, Goldstein and Jiang (2015). <em>Amer. Econ. Rev.</em> 105.'],
      ['Fishman (1988). <em>RAND J. Econ.</em> 19.', 'Foucault and Frésard (2014). <em>J. Financ. Econ.</em> 111.', 'Gorbenko and Malenko (2014). <em>J. Finance</em> 69.',
        'Hirshleifer and Png (1989). <em>Rev. Financ. Stud.</em> 2.', 'Levin and Smith (1994). <em>Amer. Econ. Rev.</em> 84.', 'Samuelson (1985). <em>Econ. Letters</em> 17.', 'Schwert (1996). <em>J. Finance</em> 51.']
    ];
    backup({ id: 'a1', label: 'A1', origin: 'q2', targets: ['app:refs'], title: 'References', subtitle: '',
      body: '<div class="refs">' + REFS.map(function (col) { return '<ul>' + col.map(function (r) { return '<li>' + r + '</li>'; }).join('') + '</ul>'; }).join('') + '</div>' + nav(back('main:refs')) });

    backup({ id: 'a2', label: 'A2', origin: 'f2', targets: ['app:notation'], widget: 'notation', title: 'Notation', subtitle: '',
      body: '<div class="notation" id="notation-table"></div>' + nav(back('main:notation')) });

    backup({ id: 'a3', label: 'A3', origin: 'f4', targets: ['app:slot'], title: 'The equilibrium object in the slot model', subtitle: '',
      body:
        ul(['<b>Tuple:</b> order laws for each class, a price for each order in ' + m(T`\{-1,0,1\}`) + ', beliefs at each price, the entry rule, the bids',
          '<b>Prices:</b> ' + m(T`P(X)=\mathbb{E}[V_T\mid X]`) + ' at each order, with entry at that price inside ' + m('V_T'),
          '<b>Beliefs:</b> Bayes rule from the order laws at each price. Every order is on path, so no off-path belief enters',
          '<b>Entry:</b> the zero cost always prepares; cost ' + m('c_H') + ' prepares exactly at prices with ' + m(T`B_r(\mu)\ge c_H`),
          '<b>Investor:</b> the order law puts weight only on best replies at the stated price and entry rules, net of cost ' + m('k'),
          '<b>Bids:</b> each bidder bids its value in the second-price auction',
          '<b>Tie rules:</b> a tied investor may mix; a tied cost ' + m('c_H') + ' type prepares. Proposition 2 holds under all four tie rules'], 'small') +
        nav(back('main:slot')) });

    backup({ id: 'a4', label: 'A4', origin: 'f5', targets: ['app:belief'], title: 'Posterior bounds hold for every strategy', subtitle: '',
      body:
        d(T`\Pr(X{=}1\mid H)\le\lambda+b,\qquad \Pr(X{=}1\mid L)\ge b,\qquad b=(1-\lambda)\beta`) +
        ul(['A buy order in class ' + m('H') + ' comes from the investor or from a liquidity buy. In class ' + m('L') + ', a liquidity buy alone gives chance at least ' + m('b'),
          'For nonzero orders the bounds need no bound on ' + m(T`\beta`) + ' past ' + m(T`\beta<1/2`) + '. The bound ' + m(T`\beta\le 1/3`) + ' covers the zero order',
          'Likelihood ratios for ' + m('H') + ' against ' + m('L') + ' then stay in ' + m(T`[1/(1+u),\,1+u]`) + ' at every order, for every investor strategy',
          'Bayes rule turns that band into ' + m(T`m(\pi)\le\mu\le M(\pi)`) + ' at every price',
          'At the example’s prior, the band is ' + m(T`[{{m_half_B}},\,{{M_half_B}}]`) + '. Full orders attain both ends'], 'small') +
        take('The uniqueness argument applies the bounds to every profile.') +
        nav(back('main:belief')) });

    backup({ id: 'a5', label: 'A5', origin: 'f6', targets: ['app:bench'], title: 'Recruitment and research regions in the example', subtitle: '',
      body:
        '<table class="t-region"><thead><tr><th>Object</th><th>Region</th><th>Example</th></tr></thead><tbody>' +
          tr3('Mass ratio ' + m('u') + ' (Corollary 1)', m(T`({{u_lo}},\,{{u_hi}})`), q('u_B')) +
          tr3('Top posterior ' + m('M') + ' at prior ' + q('prim_pi'), m(T`({{M_lo}},\,{{M_hi}})`), q('M_half_B')) +
          tr3('Liquidity chance ' + m(T`\beta`), m(T`0<\beta\le 1/3`), q('beta_B')) +
          tr3('Presence chance ' + m(T`\lambda`) + ' at that ' + m(T`\beta`), 'from ' + m(T`u=\lambda/((1-\lambda)\beta)`), q('lambda_B')) +
          tr3('Prior ' + m(T`\pi`) + ' for Proposition 2', m(T`({{prior_lo_B}},\,{{prior_hi_B}})`), q('prim_pi')) +
          tr3('Research cost ' + m('a') + ' (Proposition A.1)', m(T`({{res_a_lo}},\,{{res_a_up}})`), q('res_a')) +
          tr3('Research cap ' + m(T`\bar\lambda`), m(T`({{res_cap_lo}},\,{{res_cap_hi}})`), q('res_cap')) +
        '</tbody></table>' +
        gray('Each region is cut out by strict inequalities: the results hold on an open set of inputs.') +
        nav(back('main:bench')) });

    backup({ id: 'a6', label: 'A6', origin: 'f9', targets: ['app:prop2'], title: 'Proof structure of Proposition 2', subtitle: '',
      body:
        '<ol class="steps">' +
          '<li data-step="0"><b>Bounds for every profile:</b> posterior band ' + m(T`m\le\mu\le M`) + '; gain per unit at most ' + m(T`\Delta_T`) + '; entry at least ' + m(T`\rho`) + '</li>' +
          '<li data-step="1"><b>Weak ' + m('r_0') + ':</b> ' + m(T`\Delta_T(r_0)<k`) + ' makes each nonzero order lose in expectation. A quiet market is the sole outcome; entry is ' + m(T`\rho`) + '</li>' +
          '<li data-step="2"><b>Strong ' + m('r_1') + ':</b> ' + m(T`k<\rho\kappa\,\Delta_T(r_1)`) + ' makes each correct order pay under every profile; a wrong-signed order always loses. Orders are ' + m('(1,-1)') + '</li>' +
          '<li data-step="3"><b>Entry at ' + m('r_1') + ':</b> a buy order gives belief ' + m('M') + ' with ' + m(T`B_{r_1}(M)>c_H`) + ', so cost ' + m('c_H') + ' prepares after a buy order. Entry exceeds ' + m(T`\rho`) + '</li>' +
          '<li data-step="4"><b>Return at ' + m('r_2') + ':</b> trade still pays, but ' + m(T`B_{r_2}(M)<c_H`) + ' keeps cost ' + m('c_H') + ' out at every price. Entry is ' + m(T`\rho`) + '</li>' +
        '</ol>' +
        '<p class="small" data-step="5">Ownership: with ' + m(T`W_H(F)=\mathbb{E}_H[F(\theta)\mathbf{1}\{\theta\ge p\}]`) + ', class ' + m('H') + ' ownership rises exactly if ' + m(T`[\rho+(1-\rho)(b+\lambda)]\,W_H(F_1)>\rho\,W_H(F_0)`) + '.</p>' +
        nav(back('main:prop2')) });

    backup({ id: 'a7', label: 'A7', origin: 'f10', targets: ['app:outcome'], defines: ['e_HL'], title: 'Entry and ownership in the example', subtitle: '',
      body:
        '<p class="small">Under full orders, class ' + m('H') + ' faces a buy order with chance ' + m(T`\lambda+b`) + ' and class ' + m('L') + ' with chance ' + m('b') + '.</p>' +
        d(T`e_H=\rho+(1-\rho)(\lambda+b),\qquad e_L=\rho+(1-\rho)b,\qquad \text{entry}=\pi e_H+(1-\pi)e_L`) +
        ul(['At ' + m('r_1') + ', cost ' + m('c_H') + ' prepares after a buy order and only after a buy order. Class entry rates are ' + m('e_H') + ' and ' + m('e_L'),
          'At the example’s prior, entry is ' + q('entry_r1_B') + ' and class ' + m('H') + ' ownership is ' + q('own_r1_B'),
          'At ' + m('r_0') + ', a quiet market gives a flat price, so entry is ' + q('entry_r0') + ' and ownership is ' + q('own_r0'),
          'At ' + m('r_2') + ', no price covers ' + m('c_H') + ', so entry is ' + q('entry_r2') + ' and ownership is ' + q('own_r2_B') + ', with full orders',
          m(T`B_r(\pi)`) + ' equals ' + q('Bprior_r0') + ', ' + q('Bprior_r1_B') + ', ' + q('Bprior_r2') + ' at ' + m('r_0') + ', ' + m('r_1') + ', ' + m('r_2')], 'small') +
        nav(back('main:outcome')) });

    backup({ id: 'a8', label: 'A8', origin: 'f12b', targets: ['app:coex'], title: 'Marked strengths of the coexistence region', subtitle: '',
      body:
        '<table class="t-thresh"><thead><tr><th>Strength</th><th>Value in the example</th><th>Role</th></tr></thead><tbody>' +
          tr3(m('r_A'), q('rA'), 'first strength with an informative market') +
          tr3(m('r_F'), q('rF_B'), 'first strength with a certain purchase in it') +
          tr3(m('r_N'), q('rN'), 'last strength with a quiet market') +
          tr3(m('r_J'), q('rJ'), 'the full purchase is alone from here') +
          tr3(m('r_S'), q('rS_B'), 'low class sells for certain from here') +
          tr3(m('r_C'), q('rC_B'), 'entry ceiling: top posterior stops short of ' + m('c_H') + ' past ' + m('r_C')) +
        '</tbody></table>' +
        ul(['Before ' + m('r_A') + ', a purchase cannot pay at any mix rate, so no informative market exists',
          'On ' + m('[r_A,r_F)') + ', the mix rate adjusts with strength and entry rises with it',
          'From ' + m('r_F') + ' to ' + m('r_N') + ', a full purchase coexists with a quiet market and entry in it is constant',
          'Past ' + m('r_N') + ', a quiet market fails: a unit order against the flat price pays. Mixed orders at the entry floor join the full purchase on ' + m('(r_N,r_J)') + '; from ' + m('r_J') + ' the full purchase is alone'], 'small') +
        nav(back('main:coex')) });

    backup({ id: 'a9', label: 'A9', origin: 'f13', targets: ['app:research'], title: 'Research in detail', subtitle: '',
      body:
        ul(['Research picks ' + m(T`\lambda`) + ' in ' + m(T`[0,\bar\lambda]`) + ' before the slot, at cost ' + m(T`\tfrac{a}{2}\lambda^2`) + ' (Proposition 4)',
          'In the example, ' + m('a={{res_a}}') + ' and the cap is ' + m(T`\bar\lambda={{res_cap}}`) + '. The marked strengths are ' + m(T`r_R\approx{{res_rR}}`) + ', ' + m(T`r_{\bar\lambda}\approx{{res_rcap}}`) + ', ' + m(T`r_N\approx{{res_rN}}`) + ', ' + m(T`r_Q\approx{{res_rQ}}`) + ', ' + m(T`r_C\approx{{res_rC}}`),
          'Zero research, with entry ' + m(T`\rho`) + ', is an equilibrium exactly on ' + m('[r_0,r_N]'),
          'Recruiting research is an equilibrium exactly on ' + m('[r_R,r_C]') + ': research rises from ' + q('res_lambda_rR') + ' to the cap on ' + m(T`[r_R,r_{\bar\lambda})`) + ' and stays at the cap on ' + m(T`[r_{\bar\lambda},r_C]`) + '; entry rises from ' + q('res_entry_rR') + ' to ' + q('res_entry_cap') + ' and keeps that value up to ' + m('r_C'),
          'Floor-entry research, in which both classes trade after a success, no order recruits and entry is ' + m(T`\rho`) + ', is an equilibrium exactly on ' + m('(r_N,r_Q)') + ' and on ' + m('(r_C,r_2]') + '; there is no other equilibrium',
          'At ' + q('str_r155') + ', ' + q('str_r160') + ' and ' + q('str_r165') + ' there are exactly two equilibria: zero research, and recruiting research below the cap (class ' + m('H') + ' buys after a success, class ' + m('L') + ' abstains). Research is ' + q('res_lambda_r155') + ', ' + q('res_lambda_r160') + ', ' + q('res_lambda_r165') + ' and entry is ' + q('res_entry_r155') + ', ' + q('res_entry_r160') + ', ' + q('res_entry_r165'),
          'The unique equilibrium has zero research at ' + m('r_0') + ', recruiting research at the cap at ' + m('r_1') + ' and floor-entry research at the cap at ' + m('r_2') + ', where entry is ' + m(T`\rho`)], 'small') +
        gray('Costly research with an alternative arrival has precedent in Dow and Gorton 1997.') +
        nav(back('main:research')) });

    backup({ id: 'a10', label: 'A10', origin: 'f14', targets: ['app:robust'], title: 'Extensions in detail', subtitle: '',
      body:
        '<table class="t-ext"><thead><tr><th>Variant</th><th>Statement in the slot set-up</th></tr></thead><tbody>' +
          '<tr><th>General values, priors (A.4)</th><td>Proposition 2 holds for every ranked pair and prior at suitable costs, under (H1)–(H3) with ' + m(T`m(\pi)`) + ', ' + m(T`M(\pi)`) + '</td></tr>' +
          '<tr><th>Many classes (A.5)</th><td>The result holds under a separation condition on class proceeds; without it one price can pool two posteriors</td></tr>' +
          '<tr><th>Cost laws (A.3)</th><td>The reversal holds with atoms or none; an atomless high component turns the drop at the entry ceiling into a ramp</td></tr>' +
          '<tr><th>Private signals (A.6)</th><td>In the example, accuracies ' + m(T`({{sig_comp_aT}},\,{{sig_comp_d}})`) + ' give entry ' + q('p4_comp_b_r0_entry') + ' → ' + q('p4_comp_b_r1_entry') + '; without the challenger signal entry is ' + q('p4_comp_b_no_y_r1_entry') + ' at both strengths</td></tr>' +
          '<tr><th>Price access (A.7)</th><td>Shareholders gain in total at every trade scale below ' + q('p2_access_break_even') + '</td></tr>' +
          '<tr><th>Payment rule (A.8)</th><td>The spread response weakly has the sign of ' + m(T`1-2\omega`) + '; strictly when ' + m(T`\omega\ne1/2`) + ' and ' + m(T`\mathbb{E}[(R-\ell)_+]`) + ' changes strictly</td></tr>' +
        '</tbody></table>' +
        nav(back('main:robust')) });

    backup({ id: 'a11', label: 'A11', origin: 'f14', targets: ['app:sizes'], defines: ['s_noise'], title: 'Continuous order sizes need a convention', subtitle: '',
      body:
        ul(['The slot set-up uses unit orders ' + m(T`\{-1,0,1\}`) + ', so every order is on path and no off-path belief enters',
          'A menu of continuous order sizes needs a convention for the sizes that no class uses, as in Edmans, Goldstein and Jiang 2015',
          'Another route keeps every size on path through additive liquidity flow',
          'With Laplace noise of scale ' + m(T`\xi`) + ' and full unit orders, the top posterior equals the slot value ' + m('M(\\pi)') + ' when ' + m(T`1+u=e^{2/\xi}`),
          'The two set-ups then share the posterior bounds. They differ in the probability that each class reaches the top posterior'], 'roomy') +
        take('Unit orders keep prices on path at every order.') +
        nav(back('main:robust')) });

    backup({ id: 'a12', label: 'A12', origin: 'f15', targets: ['app:welfare'], title: 'Sale terms in detail', subtitle: '',
      body:
        ul(['<b>Price access (A.7):</b> at ' + m('r_1') + ', proceeds gain equals ' + q('p2_access_proceeds_gain') + ' and net surplus gain equals ' + q('p2_access_surplus_gain'),
          'Orders and trade costs match in the two access cases at ' + m('r_1') + '; access adds preparation after a purchase only',
          '<b>Reserve (A.9):</b> at the reserve ' + q('rsv_points_excl') + ', which excludes the low class, full orders hold at both strengths and entry is flat',
          'Strict deterrence needs reserve ' + q('rsv_deter') + ', a level that excludes the low class and the weak incumbent',
          '<b>Payment rule (A.8):</b> with seller share ' + m(T`\omega`) + ', the spread response weakly has the sign of ' + m(T`1-2\omega`) + '; strictly when ' + m(T`\omega\ne1/2`) + ' and ' + m(T`\mathbb{E}[(R-\ell)_+]`) + ' changes strictly'], 'small') +
        nav(back('main:welfare')) });

    /* ================================================================ notation (A2 and the G panel) */
    /* Rows of the A2 table in slides.tex. One source feeds the A2 slide and the notation panel. */
    var notation = [
      [[m(T`R;\ r`), 'incumbent value ' + m(T`R\sim U[0,r]`) + '; strength ' + m('r')],
        [m(T`j\in\{H,L\};\ G_j`), 'challenger class; value law in class ' + m('j')],
        [m(T`h,\ell;\ \pi`), 'the example’s class values; prior on ' + m('H')],
        [m('p'), 'reserve price, not the stock price'],
        [m(T`0,c_H;\ \rho`), 'preparation costs; ' + m(T`\rho`) + ' is the zero-cost probability'],
        [m(T`t_0,t_H,t_L`), 'proceeds with no entry, a class ' + m('H') + ' challenger, a class ' + m('L') + ' challenger'],
        [m(T`\Delta_T`), 'target-payoff spread ' + m('t_H-t_L')],
        [m(T`g_H,g_L;\ B_r(\mu)`), 'class profits before cost; profit at belief ' + m(T`\mu`)]],
      [[m(T`\lambda;\ \beta`), 'informed presence chance; liquidity order chance'],
        [m(T`b;\ u`), m(T`b=(1-\lambda)\beta`) + '; mass ratio ' + m(T`u=\lambda/b`)],
        [m(T`X;\ P;\ V_T`), 'slot order; stock price; proceeds per share'],
        [m(T`\mu;\ m,M;\ \kappa`), 'belief ' + m(T`\Pr(H\mid P)`) + '; bounds; ' + m(T`\kappa=\min\{m,1-M\}`)],
        [m(T`\tau(r)`), 'preparation threshold: ' + m(T`B_r(\tau)=c_H`)],
        [m(T`e_r(\mu)`), 'entry probability at belief ' + m(T`\mu`)],
        [m('(q_H,q_L)'), 'investor orders after class ' + m('H') + ', class ' + m('L')],
        [m('W_H(F)'), 'class ' + m('H') + ' win chance at reserve ' + m('p') + ' against incumbent law ' + m('F')],
        [m(T`a;\ \bar\lambda;\ \omega`), 'research cost; cap; seller share in A.8']]
    ];

    /* Every symbol the slides use, with the pattern that finds it in a slide's LaTeX. The check
       fails if a symbol appears before the frame that defines it (frames in deck order). */
    var S = '(^|[^\\\\a-zA-Z_^])';
    var glossary = [
      { key: 'R', pattern: S + 'R(?![a-zA-Z])' }, { key: 'r', pattern: S + 'r(?![a-zA-Z_])' },
      { key: 'class', pattern: T`G_j|` + S + T`j(?![a-zA-Z])` }, { key: 'pi', pattern: T`\\pi` },
      { key: 'h', pattern: S + 'h(?![a-zA-Z])' }, { key: 'ell', pattern: T`\\ell` }, { key: 'p', pattern: S + 'p(?![a-zA-Z])' },
      { key: 'rho', pattern: T`\\rho` }, { key: 'c_H', pattern: 'c_H' },
      { key: 'Delta_T', pattern: T`\\Delta_T` }, { key: 'tj', pattern: T`t_(H|L|j)` }, { key: 'gj', pattern: 'g_(H|L|j)' },
      { key: 'B', pattern: 'B_' }, { key: 'mu', pattern: T`\\mu(?!_)` }, { key: 'r_01', pattern: 'r_[01]' },
      { key: 'lambda', pattern: T`\\lambda` }, { key: 'q', pattern: S + 'q(?![a-zA-Z_])' }, { key: 'k', pattern: S + 'k(?![a-zA-Z_])' },
      { key: 'beta', pattern: T`\\beta` }, { key: 'X', pattern: S + 'X(?![a-zA-Z])' }, { key: 'P', pattern: S + 'P(?![a-zA-Z_])' },
      { key: 'V_T', pattern: 'V_T' }, { key: 'b', pattern: S + 'b(?![a-zA-Z])' }, { key: 'u', pattern: S + 'u(?![a-zA-Z])' },
      { key: 'm_M', pattern: S + '[mM](?![a-zA-Z])' }, { key: 'e_r', pattern: 'e_r' }, { key: 't_0', pattern: 't_0' },
      { key: 'r_2', pattern: 'r_2' }, { key: 'kappa', pattern: T`\\kappa` }, { key: 'q_HL', pattern: 'q_(H|L)' },
      { key: 'tau', pattern: T`\\tau` }, { key: 'r_C', pattern: 'r_C' },
      { key: 'F_W', pattern: T`W_H|F_[01]` }, { key: 'r_AFNJS', pattern: 'r_(A|F|N|J|S)' },
      { key: 'a_cap', pattern: S + 'a(?![a-zA-Z_])|' + T`\\bar\\lambda` }, { key: 'r_R', pattern: 'r_R' },
      { key: 'omega', pattern: T`\\omega` }, { key: 'e_HL', pattern: 'e_(H|L)' }, { key: 's_noise', pattern: T`\\xi` }
    ];

    return { frames: F, glossary: glossary, notation: notation };
  }

  if (typeof window !== 'undefined') window.createDeck = createDeck;
})();
