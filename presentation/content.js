/* content.js: the frames of slot/manuscript/slides.tex as web slides, in the Beamer order.
 *
 * This file is kept by hand. presentation/check_deck.mjs compares it with slides.tex on every
 * build: frame order, labels, frame numbers, titles, subtitles, hypertargets, the link graph with
 * its texts, every registry key that slides.tex prints with \reg{key} (as often as it prints it),
 * every rounded number it prints with \regr{key}{digits}, and the words outside mathematics and
 * diagrams, in order. Edit slides.tex in Overleaf first, then this file. The timing of each main
 * frame is the timing line of slot/manuscript/slides_script.md.
 *
 * Contract. window.createDeck(H) returns { frames, notation }. H is supplied by the renderer
 * (presentation/render.mjs) or by the check, never by this file:
 *   H.m(latex)                 inline mathematics
 *   H.d(latex)                 display mathematics
 *                              In both, {{key}} prints the registry display of key inside the formula,
 *                              {{key|3}} the value rounded to three decimals, as \regr{key}{3} does;
 *                              \reg{key} does the same as {{key}} where a subtitle must read as in slides.tex.
 *   H.q(key[, digits])         a registry number in running text.
 *   H.v(key)                   the registry value as a number, for layout only.
 *   H.go(target, text)         a link button in the footline, as \hyperlink{target}{\beamergotobutton{text}}.
 *   H.back(target[, text])     a return button, as \BackButton{target} ("Back") or \beamerreturnbutton{text}.
 *   H.link(target, text)       an inline text link, as \hyperlink{target}{text}.
 *   H.endFrame(label)          optional; called once per frame after its fields are built.
 * Frame record: { id, label, num, part, title, short, subtitle, targets, minutes, widget, body,
 *   backup, origin, cls }. title is the slides.tex title argument verbatim; num is the Beamer frame
 *   number of a main frame and the \BackupId of a backup page; cls adds classes to the slide (the body
 *   size of a frame that does not use \Body: sz-n \normalsize, sz-f \footnotesize, sz-x \scriptsize).
 * Layout: presentation/DESIGN.md section 11 names the class for each Beamer macro. A diagram (a TikZ
 *   picture of slides.tex) sits inside dg(), which the word check skips; its labels are the node texts.
 * ES2019, no modules, no DOM access.
 */
(function () {
  'use strict';
  var T = String.raw;

  function createDeck(H) {
    var m = H.m, d = H.d, q = H.q, go = H.go, back = H.back, link = H.link;
    var args = function (a) { return Array.prototype.slice.call(a); };

    /* ---------------------------------------------------------------- the macros of ccc-journal.sty */
    var P = function (s, cls) { return '<p' + (cls ? ' class="' + cls + '"' : '') + '>' + s + '</p>'; };
    var st = function (tag, html) { return '<div class="statement"><p class="statement-tag">' + tag + '</p>' + html + '</div>'; };
    var gloss = function (s) { return '<p class="gloss">' + s + '</p>'; };
    var gray = function (s) { return '<p class="grayline">' + s + '</p>'; };
    var intuition = function (s) { return '<p class="intuition">' + s + '</p>'; };
    var takeaway = function (s) { return '<p class="takeaway">' + s + '</p>'; };
    var footline = function () { return '<div class="footzone">' + args(arguments).map(function (s) { return '<p class="footline">' + s + '</p>'; }).join('') + '</div>'; };
    var smallline = function (s) { return '<p class="smallline">' + s + '</p>'; };
    var large = function (s) { return '<p class="largeline">' + s + '</p>'; };
    var ruleL = '<hr class="rule-light">';
    var vfill = '<div class="vfill"></div>';
    var vsp = function (px) { return '<div class="vsp" style="height:' + px + 'px"></div>'; };
    var nav = function () { return '<p class="nav">' + args(arguments).join(' ') + '</p>'; };
    var colhead = function (s) { return '<b class="colhead">' + s + '</b>'; };
    var strip = function (cur) {
      return '<ul class="model-strip">' + ['Players', 'Timing', 'Information', 'Actions', 'Payoffs', 'Equilibrium'].map(function (n, i) {
        return '<li' + (cur.indexOf(i + 1) >= 0 ? ' class="current"' : '') + '>' + n + '</li>';
      }).join('') + '</ul>';
    };
    var deflist = function (rows, labelPx) {
      return '<dl class="deflist"' + (labelPx ? ' style="grid-template-columns:' + labelPx + 'px minmax(0,1fr)"' : '') + '>' +
        rows.map(function (r) { return '<dt>' + r[0] + '</dt><dd>' + r[1] + '</dd>'; }).join('') + '</dl>';
    };
    /* lists: gap is \itemsep in design pixels */
    var list = function (tag) {
      return function (items, gap, cls) {
        return '<' + tag + (cls ? ' class="' + cls + '"' : '') + (gap !== undefined ? ' style="--gap:' + gap + 'px"' : '') + '>' +
          items.map(function (it) { return '<li>' + it + '</li>'; }).join('') + '</' + tag + '>';
      };
    };
    var ul = list('ul'), ol = list('ol');
    /* Beamer columns and minipages: [fraction of the text width, html]; the rest of the width is the gap. */
    var cols = function (spec, cls) {
      return '<div class="jcols' + (cls ? ' ' + cls : '') + '">' + spec.map(function (c) {
        return '<div class="jcol" style="width:' + (c[0] * 100).toFixed(1) + '%">' + c[1] + '</div>';
      }).join('') + '</div>';
    };
    var center = function (html, cls) { return '<div class="jcenter' + (cls ? ' ' + cls : '') + '">' + html + '</div>'; };
    /* A booktabs table. widths: column widths in design pixels (1 cm of the Beamer page is 100 px) or
       null; align: one letter per column (l, c); rows: arrays of cells, 'mid' for a \midrule, or
       { panel: html } for a row across all columns. */
    var table = function (o) {
      var n = o.head.length, al = o.align || 'l'.repeat(n);
      var cell = function (tag, c, i) { return '<' + tag + (al[i] === 'c' ? ' class="c"' : '') + '>' + c + '</' + tag + '>'; };
      var col = o.widths ? '<colgroup>' + o.widths.map(function (w) { return w ? '<col style="width:' + w + 'px">' : '<col>'; }).join('') + '</colgroup>' : '';
      var mid = false, body = '';
      o.rows.forEach(function (r) {
        if (r === 'mid') { mid = true; return; }
        var cls = mid ? ' class="mid"' : '';
        mid = false;
        if (r.panel !== undefined) body += '<tr' + cls + '><td colspan="' + n + '">' + r.panel + '</td></tr>';
        else if (r.head) body += '<tr' + cls + '>' + r.head.map(function (c, i) { return cell('td', c, i); }).join('') + '</tr>';
        else body += '<tr' + cls + '>' + r.map(function (c, i) { return c === null ? '' : cell('td', c, i); }).join('') + '</tr>';
      });
      return '<table class="tj' + (o.cls ? ' ' + o.cls : '') + '"' + (o.width ? ' style="width:' + o.width + 'px"' : '') + '>' + col +
        '<thead><tr>' + o.head.map(function (c, i) { return cell('th', c, i); }).join('') + '</tr></thead><tbody>' + body + '</tbody></table>';
    };
    var dg = function (html, cls) { return '<div class="diagram' + (cls ? ' ' + cls : '') + '"><!--dg-->' + html + '<!--/dg--></div>'; };
    var fig = function (id, label, cls) { return '<div class="figure plain nolegend' + (cls ? ' ' + cls : '') + '" id="' + id + '" tabindex="0" aria-label="' + label + '"></div>'; };

    /* ---------------------------------------------------------------- the drawing macros of slides.tex */
    /* SVG text with italic symbols: _x_ prints x in italic; ^sub^ is a subscript. */
    var svgText = function (s) {
      return s.replace(/_([^_]+)_/g, '<tspan font-style="italic">$1</tspan>').replace(/\^([^^]+)\^/g, '<tspan dy="0.3em" font-size="70%">$1</tspan><tspan dy="-0.3em"> </tspan>');
    };
    var text = function (x, y, s, o) {
      o = o || {};
      return '<text x="' + x + '" y="' + y + '" text-anchor="' + (o.anchor || 'middle') + '" class="' + (o.cls || 'dg-ink') + '"' + (o.size ? ' font-size="' + o.size + '"' : '') + '>' + svgText(s) + '</text>';
    };
    /* a horizontal curly brace from x0 to x1 whose tip points up at height y */
    var brace = function (x0, x1, y, cls) {
      var a = 10, mid = (x0 + x1) / 2;
      return '<path class="dg-brace ' + cls + '" d="M' + x0 + ',' + y + ' q0,-' + a + ' ' + a + ',-' + a + ' H' + (mid - a) + ' q' + a + ',0 ' + a + ',-' + a +
        ' q0,' + a + ' ' + a + ',' + a + ' H' + (x1 - a) + ' q' + a + ',0 ' + a + ',' + a + '"/>';
    };
    var tick = function (x, cls) { return '<line class="' + (cls || 'dg-tick') + '" x1="' + x + '" y1="72" x2="' + x + '" y2="108"/>'; };
    var arrow = function (x0, y0, x1, y1) { return '<line class="dg-arrow" x1="' + x0 + '" y1="' + y0 + '" x2="' + x1 + '" y2="' + y1 + '" marker-end="url(#dg-tip)"/>'; };
    var TIP = '<defs><marker id="dg-tip" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="dg-tipfill"/></marker></defs>';
    var svg = function (w, h, scale, body, label) {
      return '<svg class="dg-svg" viewBox="0 0 ' + w + ' ' + h + '" width="' + Math.round(w * scale) + '" height="' + Math.round(h * scale) + '" role="img" aria-label="' + label + '">' + TIP + body + '</svg>';
    };
    /* \SplitLine[<earlier x>]{<x of R>}{<label of R>} of frame 8; x in cm on a 13 cm line, 100 px a cm. */
    var splitLine = function (x, lab) {
      x *= 100;
      return svg(1320, 215, 1, '<line class="dg-axis" x1="0" y1="90" x2="1300" y2="90"/>' +
        tick(30) + text(30, 140, '0') + tick(220) + tick(1150) + tick(x, 'dg-tick accent') +
        text(220, 152, 'reserve _p_') + text(1150, 152, 'rival’s value _θ_') + text(x, 200, lab, { cls: 'dg-accent' }) +
        brace(35, x - 5, 60, 'info') + text((35 + x - 5) / 2, 38, 'target proceeds', { cls: 'dg-info' }) +
        brace(x + 5, 1145, 60, 'cost') + text((x + 5 + 1145) / 2, 38, 'gross auction profit', { cls: 'dg-cost' }) +
        text(1190, 56, 'one draw _R_', { anchor: 'start', cls: 'dg-muted', size: 25 }),
        'The number line of one draw R between the reserve p and the rival’s value θ: target proceeds below R, gross auction profit above it.');
    };
    /* \GapLine{<earlier x>}{<x>} of frame 10. */
    var gapLine = function (x0, x, scale) {
      x0 *= 100; x *= 100;
      return svg(1320, 215, scale, '<line class="dg-axis" x1="0" y1="90" x2="1300" y2="90"/>' +
        tick(x0, 'dg-tick faded') + arrow(x0 + 10, 120, x - 10, 120) + tick(150) + tick(1150) + tick(x, 'dg-tick accent') +
        text(150, 152, 'poor-synergy value') + text(1150, 152, 'good-synergy value') + text(x, 200, 'incumbent’s value moves right', { cls: 'dg-accent' }) +
        brace(155, x - 5, 60, 'info') + text((155 + x - 5) / 2, 38, 'shareholders’ part', { cls: 'dg-info' }) +
        brace(x + 5, 1145, 60, 'cost') + text((x + 5 + 1145) / 2, 38, 'rival’s part', { cls: 'dg-cost' }),
        'The synergy value gap between the poor-synergy and the good-synergy value, split at the incumbent’s value: the shareholders’ part below it, the rival’s part above it.');
    };

    var F = [];
    function frame(o) { if (H.endFrame) H.endFrame(o.label); if (o.subtitle === undefined) o.subtitle = ''; o.widget = o.widget || ''; o.targets = o.targets || []; F.push(o); }
    function main(o) { o.backup = false; frame(o); }

    /* ================================================================ title and frames 1 to 4 */

    main({ id: 'f0', label: 'S0', num: '0', part: 1, minutes: 0.5, widget: 'title', short: 'Title',
      title: 'Competition Creates Competition: Stock Prices and the Discovery of Takeover Bidders',
      body: '<div class="cover"><h1>Competition Creates Competition:<br>Stock Prices and the Discovery of Takeover Bidders</h1>' +
        '<p class="cover-author">Austin Li</p><p class="cover-inst">Department of Economics, University College London</p></div>' });

    main({ id: 's1', label: 'S1', num: '1', part: 1, minutes: 2.5, targets: ['main:s1'], cls: 'bigtitle sz-n',
      title: 'Does a stronger incumbent always keep the rival out?', subtitle: 'Why the answer matters',
      body: vsp(77) +
        cols([[0.31, colhead('Seller') + 'A public sale must find a rival bidder. A stronger incumbent can help find one, or end the search.'],
          [0.31, colhead('Rival') + 'Preparation costs money before a bid is possible. The stock price can show whether the cost may pay.'],
          [0.31, colhead('Price') + 'Stock trade comes before preparation. A price move can cause entry, not only forecast it.']]) +
        vfill +
        footline('One extra bidder can change sale proceeds at first order (Bulow and Klemperer, 1996). Here the sale rule stays fixed. The object is entry.') });

    main({ id: 's2', label: 'S2', num: '2', part: 1, minutes: 1.5, targets: ['main:s2'], cls: 'sz-n',
      title: 'The received answer: strength cannot raise entry', subtitle: 'When what the rival can learn stays fixed',
      body: vsp(21) +
        ul(['The rival pays to learn its value before it can bid.',
          'A stronger incumbent weakly cuts the rival’s expected auction profit at a fixed belief.',
          'Some preparation costs then fail to pay. Entry cannot rise.',
          'Fishman (1988): a chosen preemptive bid. Here: a public strength shift. The value itself stays private.'], 28) +
        takeaway('This holds when pre-preparation information stays fixed.') +
        footline('Fishman (1988); Hirshleifer and Png (1989). Auction entry: Samuelson (1985); McAfee and McMillan (1987); Levin and Smith (1994); Gentry and Stroup (2019).') });

    main({ id: 's3', label: 'S3', num: '3', part: 1, minutes: 1, targets: ['main:s3'],
      title: 'Where the paper sits: price feedback meets costly entry',
      body: vsp(10) +
        table({ widths: [460, 430, 530], cls: 'stretch-135', head: ['Strand', 'Core idea', 'Difference here'], rows: [
          ['<b>Price feedback</b> — Dow, Goldstein and Guembel (2017, closest antecedent); Edmans, Goldstein and Jiang (2015)', 'Price guides a real decision', 'The decision is rival preparation'],
          ['<b>Costly entry</b> — Fishman (1988); Roberts and Sweeting (2013)', 'Preparation cost deters entry', 'Price news can rise with incumbent strength'],
          ['<b>Takeover trade</b> — Edmans, Goldstein and Jiang (2012); Kyle and Vila (1991)', 'Trade moves target prices', 'Outside informed trader, no initial position, no target control']] }) +
        takeaway('An outside informed trader can put synergy news in the price. Incumbent strength can raise the return to that trade.') +
        nav(go('app:b14', 'B14')) });

    main({ id: 's4', label: 'S4', num: '4', part: 1, minutes: 1.5, targets: ['main:s4'],
      title: 'This paper: a stronger incumbent can recruit the rival',
      body: large('A stronger incumbent weakly cuts the rival’s profit at each belief. It can also widen the shareholder spread. Informed trade can then pay, and the price can recruit the rival.') +
        vsp(13) +
        ol(['<b>Non-monotone entry:</b> entry can rise from the weak to the strong incumbent, then return to its floor. Each case has a unique outcome (Proposition 2).',
          '<b>Value split:</b> strength weakly cuts rival profit and weakly widens the shareholder spread (Proposition 1).',
          '<b>Information control:</b> with pre-preparation information fixed, a stronger incumbent cannot raise entry.'], 14) +
        vsp(16) +
        P('Extensions: costly research by the informed trader; gains for sellers from a visible price; a purchase-impact prediction.') +
        vfill + ruleL +
        P('Roadmap: Model ' + m(T`\rightarrow`) + ' Mechanism and main result ' + m(T`\rightarrow`) + ' Fixed-information control ' + m(T`\rightarrow`) + ' Extensions and prediction.', 'roadline') });

    /* ================================================================ the model: frames 5 to 9 */

    main({ id: 's5', label: 'S5', num: '5', part: 2, minutes: 1.5, targets: ['main:s5'],
      title: 'Players and the sale rule',
      body: strip([1]) +
        P('A listed target has standalone value ' + m('0') + '. Values and costs are per share. All agents are risk neutral.') +
        deflist([
          ['Incumbent', '<b>incumbent bidder, already prepared:</b> it knows its value ' + m('R') + ' and faces no further preparation cost. ' + m(T`R\sim F`) + '; ' + m('F') + ' is public, continuous on ' + m(T`[0,\bar r]`) + ', and others do not observe the draw before bids. <b>Stronger</b> means a replacement ' + m(T`\widetilde F`) + ' with ' + m(T`\widetilde F(y)\le F(y)`) + ' for each ' + m('y') + '.'],
          ['Rival', '<b>potential rival bidder:</b> sees the price, then decides whether to prepare. <b>Synergy class:</b> ' + m('j=H') + ' (good synergy) or ' + m('j=L') + ' (poor synergy), with prior ' + m(T`\pi=\Pr(j=H)\in(0,1)`) + '. Its value ' + m(T`\theta`) + ' has law ' + m('G_j') + ' in class ' + m('j') + '; each ' + m('G_j') + ' has a finite mean.'],
          ['Class ranking', m(T`G_H(y)\le G_L(y)`) + ' for each ' + m('y') + ' — class ' + m('H') + ' draws weakly higher values. Also ' + m(T`\theta\ge p`) + ' almost surely under each ' + m('G_j') + ', where ' + m('p>0') + ' is the auction reserve below. The sale and the rival’s identity are public; its synergy class is not public.'],
          ['Preparation cost ' + m('C'), m('C=0') + ' with probability ' + m(T`\rho\in(0,1)`) + '; else ' + m('C=c_H>0') + ', the high cost (' + m('H') + ' in ' + m('c_H') + ' means high, not class ' + m('H') + '). Pay ' + m('C') + ' to learn ' + m(T`\theta`) + ' and to bid; a rival who does not pay cannot bid. (' + m(T`\rho`) + ' is the entry floor on frame 9.)'],
          ['Sale', 'the seller commits before trade to a cash second-price auction with reserve ' + m('p>0') + '. Sale proceeds go to target shareholders.']]) +
        vfill + ruleL +
        P('The pair ' + m(T`(j,\theta)`) + ', the value ' + m('R') + ', the cost ' + m('C') + ', and the trading-slot draws are independent. Neither bidder trades target shares. The next frame adds the trading slot: informed trader, liquidity trader, competitive market makers.', 'fs-f') });

    var timeline = (function () {
      var xs = [0, 295, 590, 885, 1180], off = 138, r = 24, labs = [
        'Seller commits: auction, reserve ' + m('p'), 'Trading slot: outcome ' + m('X'), 'Market makers set ' + m('P(X)'),
        'Rival sees ' + m('P') + ', learns ' + m('C') + ', prepares or stays out', 'Rival, if prepared, learns ' + m(T`\theta`) + '; bids; payoffs'];
      var marks = xs.map(function (x, i) {
        return '<circle class="dg-dot" cx="' + (x + off) + '" cy="26" r="' + r + '"/>' + text(x + off, 35, String(i + 1), { cls: 'dg-dotnum', size: 25 }) +
          (i < 4 ? arrow(x + off + r + 4, 26, xs[i + 1] + off - r - 4, 26) : '');
      }).join('');
      return '<div class="timeline">' + svg(1456, 54, 1, marks, 'Five steps in order, joined by arrows.') +
        '<div class="tl-labels">' + labs.map(function (l) { return '<p>' + l + '</p>'; }).join('') + '</div></div>';
    })();
    main({ id: 's6', label: 'S6', num: '6', part: 2, minutes: 2, targets: ['main:s6'],
      title: 'Timing: one trading slot, then preparation',
      body: strip([2]) + center(dg(timeline)) + ruleL +
        ul(['One trading slot comes before preparation. Its outcome is ' + m(T`X\in\{-1,0,1\}`) + ': ' + m('-1') + ' stock sale, ' + m('0') + ' no trade, ' + m('1') + ' stock purchase.',
          'With probability ' + m(T`\lambda\in(0,1)`) + ' — the informed presence — the slot goes to an outside informed trader. It observes the synergy class ' + m('j') + ' and chooses an order ' + m(T`q\in\{-1,0,1\}`) + '; each nonzero order costs ' + m('k>0') + '.',
          'With probability ' + m(T`1-\lambda`) + ', a liquidity trader fills the slot and submits ' + m('-1') + ', ' + m('0') + ', ' + m('1') + ' with probabilities ' + m(T`\beta`) + ', ' + m(T`1-2\beta`) + ', ' + m(T`\beta`) + ', where ' + m(T`0<\beta\le 1/3`) + '.',
          'Competitive market makers observe the outcome ' + m('X') + ' only. They set ' + m(T`P(X)=\mathbb{E}[V_T\mid X]`) + ', where ' + m('V_T') + ' is target proceeds per share. In equilibrium that expectation holds the rival’s entry response to the price.'], 4) });

    main({ id: 's7', label: 'S7', num: '7', part: 2, minutes: 2, targets: ['main:s7'],
      title: 'Information and choices',
      body: strip([3, 4]) +
        table({ widths: [490, 430, 510], cls: 'fs-f stretch-115', head: ['Player', 'Observes', 'Chooses'], rows: [
          ['Seller', 'public primitives', 'auction and reserve ' + m('p') + ', before trade'],
          ['Incumbent', 'its value ' + m('R'), 'bid ' + m('R') + ' if ' + m(T`R\ge p`)],
          ['Informed trader (slot with prob. ' + m(T`\lambda`) + ')', 'class ' + m('j') + ', not ' + m(T`\theta`), 'order ' + m('q') + '; cost ' + m('k') + ' if ' + m(T`q\ne0`)],
          ['Liquidity trader (slot with prob. ' + m(T`1-\lambda`) + ')', 'no private information', 'order drawn with ' + m(T`(\beta,\,1-2\beta,\,\beta)`)],
          ['Market makers', 'outcome ' + m('X') + ', not who traded', 'price ' + m(T`P(X)=\mathbb{E}[V_T\mid X]`)],
          ['Rival', 'price ' + m('P') + ' (not ' + m('X') + ' on its own), then cost ' + m('C') + '; knows neither ' + m('j') + ' nor ' + m(T`\theta`) + ' before it pays', 'prepare or stay out; if it prepares, learn ' + m(T`\theta`) + ', then bid ' + m(T`\theta`)]] }) +
        vsp(10) +
        P('Public primitives are common knowledge; the table lists each player’s own information.', 'fs-f') +
        vsp(16) +
        ul(['<b>Order belief:</b> ' + m(T`\mu(x)=\Pr(j=H\mid X=x)`) + ' — the belief of an observer who sees the realised outcome ' + m('X=x') + '.',
          '<b>Price belief:</b> ' + m(T`\bar\mu(\bar P)=\Pr(j=H\mid P(X)=\bar P)`) + ' — the rival’s belief. One price pools all outcomes with that price.'], 10) });

    main({ id: 's8', label: 'S8', num: '8', part: 2, minutes: 2, targets: ['main:s8'],
      title: 'Payoffs',
      body: strip([5]) + center(dg(splitLine(6.2, 'incumbent’s value _R_'))) +
        ul(['Fix a prepared rival with value ' + m(T`\theta\ge p`) + ', and average over ' + m('R') + '. Shareholders receive the auction payment ' + m(T`\max\{p,\min(R,\theta)\}`) + '; its mean is ' + m(T`t(\theta)`) + '. With ' + m(T`(z)_+=\max\{z,0\}`) + ', the rival’s gross profit is ' + m(T`g(\theta)=\mathbb E_R[(\theta-\max\{p,R\})_+]`) + ', before cost ' + m('C') + '. In expectation, ' + m(T`t(\theta)+g(\theta)=\theta`) + '.',
          m(T`\mathbb E_j`) + ' denotes expectation under ' + m('G_j') + '. Class means are ' + m(T`t_j=\mathbb E_j[t(\theta)]`) + ' and ' + m(T`g_j=\mathbb E_j[g(\theta)]`) + '. With no rival entry, the incumbent alone pays ' + m('p') + ' if ' + m(T`R\ge p`) + '; expected proceeds are ' + m(T`t_0=p[1-F(p)]`) + '.',
          '<b>Shareholder spread:</b> ' + m(T`\Delta_T=t_H-t_L`) + ' — extra expected target proceeds in class ' + m('H') + ' versus class ' + m('L') + ' if the rival prepares. <b>Rival gross profit</b> at belief ' + m(T`\mu`) + ' is ' + m(T`B(\mu)=g_L+\mu(g_H-g_L)`) + ', the ' + m(T`\mu`) + '-weighted mean of class gross profits, before ' + m('C') + '. Net gain from preparation: ' + m(T`B(\text{price belief})-C`) + '.',
          'The informed trader with order ' + m('q') + ' earns ' + m(T`q[V_T-P(q)]-k|q|`) + ', where ' + m('P(q)') + ' is the price after order ' + m('q') + '.'], 7) });

    main({ id: 's9', label: 'S9', num: '9', part: 2, minutes: 1.5, targets: ['main:s9'],
      title: 'Equilibrium with competitive prices',
      body: strip([6]) +
        P('Solution concept: perfect Bayesian equilibrium with break-even prices from competitive market makers.') + vsp(5) +
        deflist([
          ['Orders', 'let ' + m('e(x)') + ' be the probability that the rival prepares after realised outcome ' + m('X=x') + ', through the price ' + m('P(x)') + '. An informed trader who sees class ' + m('j') + ' gets expected net payoff ' + m(T`U_j(q)=q[t_0+e(q)(t_j-t_0)-P(q)]-k|q|`) + ' from chosen order ' + m('q') + '; the term ' + m(T`t_0+e(q)(t_j-t_0)`) + ' is expected target proceeds in class ' + m('j') + '. For each ' + m('j') + ', the informed trader puts positive probability only on orders ' + m('q') + ' that maximize ' + m('U_j(q)') + ', with the schedules ' + m(T`P(\cdot)`) + ' and ' + m(T`e(\cdot)`) + ' at their equilibrium values.'],
          ['Competitive prices', m(T`P(x)=\mathbb{E}[V_T\mid X=x]=t_0+e(x)[t_L-t_0+\Delta_T\,\mu(x)]`) + '. With entry, expected proceeds are ' + m(T`t_L+\mu(x)\Delta_T`) + '; without entry they are ' + m('t_0') + '. Zero-cost preparation below gives the entry floor ' + m(T`e(x)\ge\rho`) + '.'],
          ['Beliefs', 'the order belief ' + m(T`\mu(x)=\Pr(j=H\mid X=x)`) + ' follows Bayes’ rule. The rival’s price belief ' + m(T`\bar\mu(\bar P)=\Pr(j=H\mid P(X)=\bar P)`) + ' pools all outcomes with that price. It can differ from ' + m(T`\mu(x)`) + ' for any one pooled outcome. Liquidity trade gives each outcome positive probability in each class, so Bayes’ rule pins down order beliefs.'],
          ['Preparation and bids', 'a rival with ' + m('C=0') + ' prepares at each price. With ' + m('C=c_H') + ', it prepares if and only if ' + m(T`B(\bar\mu)\ge c_H`) + ' at its price belief. A prepared rival bids ' + m(T`\theta`) + '; the incumbent bids ' + m('R') + ' subject to the reserve.']], 300) });

    /* ================================================================ mechanism and main result: frames 10 to 14 */

    main({ id: 's10', label: 'S10', num: '10', part: 3, minutes: 2, targets: ['main:s10'],
      title: 'Strength lowers rival profit and widens the spread',
      body: st('Proposition 1',
          P('Let ' + m('F') + ' and ' + m(T`\widetilde F`) + ' be continuous incumbent value distributions, with ' + m(T`\widetilde F(y)\le F(y)`) + ' for every ' + m('y') + '.') +
          gloss('The new incumbent draws high values more often.') +
          P('Hold the reserve and the finite-mean class laws fixed.') +
          cols([[0.46, P('(a) For ' + m(T`j\in\{H,L\}`) + ' and every ' + m(T`\mu\in[0,1]`) + ',') + d(T`g_j(\widetilde F)\le g_j(F),\qquad B_{\widetilde F}(\mu)\le B_F(\mu).`) +
              P('Here ' + m(T`B_F(\mu)=g_L(F)+\mu[g_H(F)-g_L(F)]`) + '.')],
            [0.51, P('(b) Under the class ranking,') + d(T`G_H(y)\le G_L(y)\quad\text{for every }y,\qquad G_H(p^-)=G_L(p^-)=0,`) +
              P('the shareholder spread satisfies ' + m(T`\Delta_T(\widetilde F)\ge\Delta_T(F)`) + '.') + gloss('Good-synergy values are higher, and all meet the reserve.')]]) +
          P('Since both classes meet the reserve almost surely, ' + m(T`\Delta_T(F)+[g_H(F)-g_L(F)]=\mathbb E_H[\theta]-\mathbb E_L[\theta]`) + '. The right side does not depend on ' + m('F') + '.')) +
        center(dg(gapLine(5.4, 8.2, 0.6))) +
        intuition('A stronger incumbent can move part of the rival’s gain from good synergy to the target’s shareholders.') });

    main({ id: 's11', label: 'S11', num: '11', part: 3, minutes: 1.5, targets: ['main:s11'],
      title: 'Beliefs stay in a band, and the price reveals the belief',
      body: st('Belief bounds',
          P('Define' + m(T`\quad b=(1-\lambda)\beta,\qquad u=\dfrac{\lambda}{b},\qquad m(\pi)=\dfrac{\pi}{\pi+(1-\pi)(1+u)},\qquad M(\pi)=\dfrac{\pi(1+u)}{\pi(1+u)+1-\pi}.`)) +
          cols([[0.46, P('For every pure or mixed order strategy and every ' + m(T`x\in\{-1,0,1\}`) + ',') + d(T`0<\beta\le\frac13\quad\Longrightarrow\quad m(\pi)\le\mu(x)\le M(\pi).`) +
              gloss('With ' + m(T`\beta\le1/3`) + ', liquidity trade covers every outcome, including no trade.') + P('The price belief ' + m(T`\bar\mu`) + ' obeys the same bounds.')],
            [0.51, P('Suppose ' + m(T`\Delta_T>0`) + ', ' + m('g_H>g_L') + ' and ' + m(T`\rho\in(0,1)`) + '. Under Bayes’ rule, optimal preparation, competitive prices and truthful bids,') +
              d(T`\begin{aligned}&P(x)=P(x')\ \Longrightarrow\ \mu(x)=\mu(x'),\\&\Pr(H\mid P(X)=P(x))=\mu(x).\end{aligned}`)]]) +
          cols([[0.46, P('<b>Preparation rule.</b> Define the threshold ' + m(T`\tau=(c_H-g_L)/(g_H-g_L)`) + '.') + gloss('At the belief ' + m(T`\tau`) + ', rival gross profit equals the high cost.') +
              P('Under the default preparation rule,') + gloss('A rival at the threshold prepares.')],
            [0.51, d(T`\begin{aligned}&C=c_H:\quad\text{prepare exactly when }\mu(x)\ge\tau,\\&e(x)=\begin{cases}\rho,&\mu(x)<\tau,\\1,&\mu(x)\ge\tau.\end{cases}\end{aligned}`)]])) +
        intuition('A liquidity trader can place any order, so an order can move the belief but never settles the synergy class.') +
        nav(go('app:b2', 'B2')) });

    main({ id: 's12', label: 'S12', num: '12', part: 3, minutes: 1.5, targets: ['main:s12'],
      title: 'A correct order earns between a fixed share and all of the spread',
      body: st('Trading bounds',
          P('Let ' + m(T`\Delta_T\ge0`) + ' and ' + m('k>0') + '. Take any order profile with Bayes beliefs, competitive prices, truthful bids, and ' + m(T`e(x)\in[\rho,1]`) + '.') +
          gloss('The bounds hold for every trading plan, optimal or not.') +
          P('The gross gains from the correct orders are') + d(T`K_H=e(1)\Delta_T[1-\mu(1)],\qquad K_L=e(-1)\Delta_T\mu(-1).`) +
          P('Define ' + m(T`\kappa(\pi)=\min\{m(\pi),1-M(\pi)\}`) + '.') +
          gloss('The value ' + m(T`\kappa(\pi)`) + ' is the least doubt any order leaves.') +
          P('For either class ' + m(T`j\in\{H,L\}`) + ',') + d(T`\rho\kappa(\pi)\Delta_T\le K_j\le\Delta_T.`) +
          P('A wrong-signed order earns at most ' + m('-k<0') + '; abstention earns zero. The informed trader who sees class ' + m('H') + ' buys if ' + m('K_H>k') + ' and abstains if ' + m('K_H<k') + '. The informed trader who sees class ' + m('L') + ' sells if ' + m('K_L>k') + ' and abstains if ' + m('K_L<k') + '. At ' + m('K_j=k') + ', the correct order and abstention are both optimal, and any mixture of the two is optimal.')) +
        intuition('Gross gain scales with the shareholder spread and with the doubt an order leaves. Net gain subtracts ' + m('k') + ', so doubt alone does not pay.') +
        nav(go('app:b2', 'B2')) });

    main({ id: 's13', label: 'S13', num: '13', part: 3, minutes: 3, targets: ['main:s13'],
      title: 'Strength can raise entry, then return it to its floor',
      body: st('Proposition 2',
          P('Classes have finite means and satisfy ' + m(T`G_H\le G_L`) + ', ' + m(T`G_H(p^-)=G_L(p^-)=0`) + '. Steps ' + m(T`F_2\le F_1\le F_0`) + ': weak, strong, very strong. Fix the class laws and ' + m('p>0') + '; ' + m(T`\pi,\rho,\lambda\in(0,1)`) + '; ' + m(T`\beta\in(0,1/2)`) + ' (nonzero-order bounds only); and ' + m('c_H,k>0') + '. Write ' + m(T`\Delta_i=\Delta_T(F_i)`) + ' and ' + m('B_i=B_{F_i}') + '. Suppose') +
          cols([[0.42, P(m(T`\begin{array}{ll}\mathrm{(H1)}&B_0(\pi)<c_H<B_1(M(\pi)),\\\mathrm{(H2)}&\Delta_0<k<\rho\kappa(\pi)\Delta_1,\\\mathrm{(H3)}&B_2(M(\pi))<c_H.\end{array}`))],
            [0.55, gloss('(H1) Prior misses ' + m('c_H') + ' at ' + m('F_0') + '; a purchase clears it at ' + m('F_1') + '.') +
              gloss('(H2) Order cost stops trade at ' + m('F_0') + ', not at ' + m('F_1') + '.') +
              gloss('(H3) At ' + m('F_2') + ', even a purchase cannot pay ' + m('c_H') + '.')]], 'mt-6') +
          cols([[0.55, table({ cls: 'tight', head: ['Orders ' + m('(H,L)'), 'Beliefs ' + m('(-1,0,1)'), 'Entry ' + m('(-1,0,1)')], rows: [
              [m('F_0') + ' weak: ' + m('(0,0)'), m(T`(\pi,\pi,\pi)`), m(T`(\rho,\rho,\rho)`)],
              [m('F_1') + ' strong: ' + m('(1,-1)'), m(T`(m(\pi),\pi,M(\pi))`), m(T`(\rho,\rho,1)`)],
              [m('F_2') + ' very strong: ' + m('(1,-1)'), m(T`(m(\pi),\pi,M(\pi))`), m(T`(\rho,\rho,\rho)`)]] })],
            [0.42, P('Let ' + m(T`\mathsf E_i`) + ' denote total entry at ' + m('F_i') + '. Then') + d(T`\mathsf E_0=\mathsf E_2=\rho<\mathsf E_1=\rho+(1-\rho)(b+\pi\lambda).`) +
              P('The outcome is unique in each of the three economies, under all four pairs of tie rules.')]], 'mt-10')) +
        intuition('A wider shareholder spread pays the informed trader to trade, and a purchase recruits. At ' + m('F_2') + ', profit at the top belief stays below ' + m('c_H') + '.') +
        footline('Proof idea: the frame 11–12 bounds hold for each candidate outcome; strict gaps then fix orders, beliefs, and entry. Steps: ' + link('app:b2', 'B2') + '. Open set: frame 14. Exact form: ' + link('app:b1', 'B1') + '.') +
        nav(go('app:b1', 'B1'), go('app:b2', 'B2')) });

    main({ id: 's14', label: 'S14', num: '14', part: 3, minutes: 1.5, targets: ['main:s14'], widget: 'beliefs',
      title: 'Example: the top belief lies exactly between two thresholds',
      body: cols([[0.31, vsp(7) + fig('beliefs', 'Figure. The threshold belief τ(r) between the strong incumbent r_1 and the very strong incumbent r_2, with the top belief M(1/2); arrow keys move the cursor.')],
          [0.67, st('Corollary 1',
            P('The class values are point masses: ' + m(T`\theta=h`) + ' in class ' + m('H') + ' and ' + m(T`\theta=\ell`) + ' in class ' + m('L') + ', with ' + m(T`(h,\ell,p)=({{prim_h}},{{prim_ell}},{{prim_p}})`) + '. The incumbent has ' + m(T`R\sim\mathrm{Unif}[0,r]`) + '; a larger ' + m('r') + ' means a stronger incumbent. The three strengths are ' + m(T`(r_0,r_1,r_2)=({{prim_r0}},{{prim_r1}},{{prim_r2}})`) + '. At ' + m(T`\pi=1/2`) + ', in this family,') +
            d(T`\mathrm{(H1)}\text{--}\mathrm{(H3)}\quad\Longleftrightarrow\quad\tau(r_1)<M(1/2)<\tau(r_2),`) +
            P('where ' + m(T`\tau(r_1)={{tau_r1_frac}}`) + ' and ' + m(T`\tau(r_2)={{tau_r2_frac}}`) + '. The example sets ' + m(T`u=\mathrm e-1`) + ', where ' + m(T`\mathrm e`) + ' is Euler’s number, so the top belief after a purchase is ' + m(T`M(1/2)=\mathrm e/(1+\mathrm e)\simeq{{M_half_B}}`) + '.'))]]) +
        intuition('Against the strong incumbent, a purchase lifts the belief just above the threshold; against the very strong one, the threshold rises just above that belief.') +
        footline('Other inputs: ' + m(T`(\pi,\rho,c_H,k)=({{prim_pi}},{{prim_rho}},{{prim_cH}},{{prim_k}})`) + '; liquidity chance ' + m(T`\beta={{beta_B}}`) + ' (exact decimal); presence from ' + m(T`u=\lambda/[(1-\lambda)\beta]`) + '. Inputs and regions in full: ' + link('app:b10', 'B10') + '.') +
        nav(go('app:b10', 'B10')) });

    /* ================================================================ the control and the extensions: frames 15 to 18 */

    main({ id: 's15', label: 'S15', num: '15', part: 4, minutes: 2, targets: ['main:s15'],
      title: 'With fixed information, strength cannot raise entry',
      body: cols([[0.54, st('Fixed information',
            P('Fix the joint law of the class ' + m('j') + ' and the signal ' + m('S') + ' that the rival observes. Fix the class laws ' + m('G_j') + ', the reserve, and the preparation-cost law. In economy ' + m('i') + ', conditional on ' + m('(j,S)') + ', the values ' + m(T`\theta`) + ' and ' + m('R') + ' are independent, with laws ' + m('G_j') + ' and ' + m('F_i') + '. The cost ' + m('C') + ' is independent of the class, both values and ' + m('S') + '.') +
            gloss('What the rival can learn does not change. The signal adds no news about values past the class. The preparation cost carries no news about values.') +
            P('Let an indifferent rival prepare. If ' + m(T`F_1\le F_0`) + ', entry cannot rise:') + d(T`\mathsf E_1\le\mathsf E_0,`) +
            P('where ' + m(T`\mathsf E_i`) + ' is the probability of preparation in economy ' + m('i') + '.'))],
          [0.44, vsp(10) +
            table({ widths: [260, 155, 155], align: 'lcc', cls: 'fs-f stretch-130', head: ['Entry in the example', 'Weak', 'Strong'], rows: [
              ['Full model, orders solved again', 'At floor ' + m(T`\rho`), '<b>Above floor ' + m(T`\rho`) + '</b>'],
              ['Full informed orders imposed (control)', 'Above floor ' + m(T`\rho`), 'Above floor ' + m(T`\rho`)],
              ['Stock price hidden', 'At floor ' + m(T`\rho`), 'At floor ' + m(T`\rho`)]] }) +
            vsp(17) +
            P('In the middle row, the rival still reads the stock price, and full informed orders are imposed at both strengths; at the weak strength they are not optimal.', 'fs-f')]]) +
        intuition('With fixed information, a stronger incumbent only lowers the profit at each belief, so it can only remove reasons to prepare.') +
        nav(go('app:b11', 'B11')) });

    main({ id: 's16', label: 'S16', num: '16', part: 5, minutes: 1.5, targets: ['main:s16'],
      title: 'Costly research: spread, research, and total entry rise together',
      body: P('One change from frame 6. The informed trader now chooses presence ' + m(T`\lambda\in[0,\bar\lambda]`) + ' at cost ' + m(T`(a/2)\lambda^2`) + ', with ' + m('a>0') + ' and ' + m(T`0<\bar\lambda<1`) + '. With chance ' + m(T`\lambda`) + ' it learns the synergy class and fills the slot. Else liquidity fills the slot.') +
        st('Proposition 4',
          cols([[0.46, P('Assume the class ranking, ' + m(T`\pi=1/2`) + ', ' + m(T`\Delta_T>0`) + ', ' + m('g_H>g_L') + ' and ' + m(T`\tau>1/2`) + '.') +
              gloss('The prior alone does not justify the high cost.') +
              P('An indifferent informed trader may mix; an indifferent high-cost rival prepares. At presence ' + m(T`\lambda`) + ', write ' + m(T`M_\lambda`) + ' for the top belief after a purchase and ' + m(T`m_\lambda=1-M_\lambda`) + ' for the band floor. For ' + m(T`\Delta_T>2k`) + ', interior research ' + m(T`\lambda_R(\Delta_T)\in(0,1)`) + ' is the unique root of the first-order condition in ' + link('app:b12', 'B12') + '. Equilibrium research is ' + m(T`\widehat\lambda=\min\{\lambda_R(\Delta_T),\bar\lambda\}`) + '.')],
            [0.51, P('The recruiting equilibrium — the informed trader who learns class ' + m('H') + ' buys after success, and only a purchase recruits — exists exactly when') +
              d(T`\Delta_T>2k\qquad\text{and}\qquad\tau\le M_{\widehat\lambda}.`) +
              gloss('The spread pays for trade, and a purchase clears ' + m(T`\tau`) + '.') +
              P('Its research ' + m(T`\widehat\lambda`) + ' rises strictly with ' + m(T`\Delta_T`) + ' below the cap and stays constant at the cap. Total entry is') +
              d(T`\mathsf E=\rho+(1-\rho)[\beta+(1/2-\beta)\widehat\lambda].`) +
              P('As research rises, ' + m(T`\mathsf E`) + ' and class-' + m('H') + ' entry rise strictly, while class-' + m('L') + ' entry falls strictly.')]])) +
        intuition('A wider shareholder spread pays for research until the cap. More research sorts entry toward good synergy.') +
        footline('First-order condition, branches, class entry formulas, and the research figure: ' + link('app:b12', 'B12') + '. Fixed-research coexistence: ' + link('app:b3', 'B3') + '.') +
        nav(go('app:b3', 'B3'), go('app:b12', 'B12')) });

    main({ id: 's17', label: 'S17', num: '17', part: 5, minutes: 1.5, targets: ['main:s17'],
      title: 'At $F_1$, a visible price raises expected proceeds and net surplus',
      body: st('Price access',
          P('Hold the incumbent at ' + m('F_1') + ' (strong) under Proposition 2’s hypotheses. Compare price access with an economy where the rival sees neither the price nor the order. Hold all other primitives fixed; prices stay competitive in both economies.') +
          P('Let ' + m(T`\mathcal R`) + ' denote expected target proceeds and ' + m(T`\mathcal W`) + ' expected acquisition surplus net of preparation costs. Superscripts ' + m('1') + ' and ' + m('0') + ' denote price access and access to neither price nor order. Both economies keep unique full informed orders. Then') +
          d(T`\mathcal R^1>\mathcal R^0\qquad\text{and}\qquad\mathcal W^1>\mathcal W^0.`) +
          P('Access adds preparation after a purchase only, where ' + m(T`B_1(M(\pi))>c_H`) + '.')) +
        intuition('The visible price reveals the purchase belief ' + m(T`M(\pi)`) + '. The high-cost rival then prepares only where gross profit covers ' + m('c_H') + '.') +
        footline('Exact differences, example values, and the paper’s separate payment-rule and reserve comparisons: ' + link('app:b4', 'B4') + '.') +
        nav(go('app:b4', 'B4')) });

    var priceLine = svg(1360, 165, 0.8,
      '<line class="dg-axis" x1="0" y1="90" x2="1350" y2="90"/>' +
      '<line class="dg-entry" x1="820" y1="90" x2="1220" y2="90"/>' +
      tick(100) + tick(460) + tick(1220) +
      text(100, 145, 'sale-order price') + text(460, 145, 'no-order price') + text(1220, 145, 'purchase price') + text(960, 145, 'entry part', { cls: 'dg-info' }) +
      brace(105, 455, 58, 'muted') + text(280, 36, 'sale-order impact _I_^−^', { cls: 'dg-muted' }) +
      brace(465, 1215, 58, 'accent') + text(840, 36, 'purchase impact _I_^+^', { cls: 'dg-accent' }),
      'The three prices after a sale order, no order and a purchase: the sale-order impact, the purchase impact and the entry part of the purchase impact.');
    main({ id: 's18', label: 'S18', num: '18', part: 5, minutes: 1.5, targets: ['main:s18'],
      title: 'Purchase impact reveals recruitment',
      body: center(dg(priceLine)) +
        st('Weighted price impact',
          cols([[0.48, P('Assume the class ranking, ' + m(T`\Delta_T>0`) + ', ' + m('g_H>g_L') + ', full two-sided trade (the informed trader who sees class ' + m('H') + ' buys; the informed trader who sees class ' + m('L') + ' sells), and ' + m(T`\pi<\tau`) + '.') +
              gloss('At the prior, rival gross profit falls short of ' + m('c_H') + '.') +
              P('Define order frequencies ' + m(T`\bar f(x)=\Pr(X=x)`) + ' and impacts ' + m('I_+=P(1)-P(0)') + ' and ' + m('I_-=P(0)-P(-1)') + '.')],
            [0.49, P('Then ' + m(T`\bar f(1)=b+\pi\lambda`) + ', ' + m(T`\bar f(-1)=b+(1-\pi)\lambda`) + ', and') +
              d(T`\begin{aligned}&\bar f(1)I_+-\bar f(-1)I_->0\\&\Longleftrightarrow\ e(1)>\rho.\end{aligned}`) +
              P('At ' + m(T`\pi=1/2`) + ', the order frequencies are equal, so') + d(T`I_+>I_-\quad\Longleftrightarrow\quad e(1)>\rho.`)]])) +
        intuition('Recruitment adds an entry part to the purchase price. Weight by order frequency, and that part makes purchase impact exceed sale-order impact.') +
        footline('With no recruitment (' + m(T`e(x)=\rho`) + ' after each outcome), orders still predict the winner when ' + m('W_H>W_L') + ': ' + link('app:b13', 'B13') + '. The test needs the price dated before preparation starts, and a record of the no-trade outcome.') +
        nav(go('app:b13', 'B13')) });

    main({ id: 's19', label: 'S19', num: '19', part: 6, minutes: 1.5, targets: ['main:s19'], cls: 'sz-n',
      title: 'Competition can create competition',
      body: vsp(7) + large('A stronger incumbent can induce rival entry through a more informative stock price.') + vsp(21) +
        ul(['<b>Main result.</b> Entry rises against the strong incumbent and returns to its floor against the very strong one (Proposition 2, on an open set).',
          '<b>Discipline.</b> Strength weakly cuts rival gross profit and weakly widens the shareholder spread. Freeze what the rival can learn, and strength cannot raise entry.',
          '<b>Implication.</b> At the strong incumbent, a visible price raises expected target proceeds and net surplus. In data, recruitment sits in the frequency-weighted purchase impact.'], 25) +
        vfill + ruleL +
        P('With costly research, a wider shareholder spread also raises research until the cap, and sorts entry toward good synergy.', 'fs-s') });

    /* ================================================================ backups B1 to B16 */
    /* num is the \BackupId (the label without its page letter); origin is the frame of the first Back button. */
    function bk(o, backTarget) {
      o.backup = true; o.part = 'B'; o.minutes = 0;
      o.num = o.label.replace(/[a-z]+$/, '');
      o.origin = backTarget.replace(/^main:/, '');
      frame(o);
    }
    var B = function (t) { return nav(back(t)); };

    bk({ id: 'b1', label: 'B1', targets: ['app:b1'], cls: 'sz-f', title: 'Proposition 2 in exact form',
      body: ul(['Setup: the synergy laws satisfy the class ranking (good synergy first-order dominates poor synergy; each value meets the reserve ' + m('p') + ') and have finite means. The incumbent’s value law ' + m('F') + ' is continuous on ' + m(T`[0,\bar r]`) + ', with finite upper bound ' + m(T`\bar r`) + '. Laws ' + m('F_0') + ', ' + m('F_1') + ', ' + m('F_2') + ' satisfy ' + m(T`F_2\le F_1\le F_0`) + ', so each step is a first-order stochastic strengthening. Fixed: prior ' + m(T`\pi`) + ', entry floor ' + m(T`\rho`) + ' and presence ' + m(T`\lambda`) + ', each in ' + m('(0,1)') + '; liquidity chance ' + m(T`\beta\in(0,1/2)`) + '; high cost ' + m('c_H>0') + '; order cost ' + m('k>0') + '. Write ' + m(T`b=(1-\lambda)\beta`) + ' for the liquidity mass in one direction, and ' + m(T`\kappa(\pi)=\min\{m(\pi),1-M(\pi)\}`) + ' for the common lower bound on residual doubt, with band floor ' + m(T`m(\pi)`) + ' and top belief ' + m(T`M(\pi)`) + '.',
          'With ' + m('B_i') + ' rival gross profit and ' + m(T`\Delta_i`) + ' shareholder spread ' + m(T`\Delta_T`) + ' against ' + m('F_i') + ': (H1) ' + m(T`B_0(\pi)<c_H<B_1(M(\pi))`) + '. (H2) ' + m(T`\Delta_0<k<\rho\,\kappa(\pi)\,\Delta_1`) + '. (H3) ' + m(T`B_2(M(\pi))<c_H`) + '.',
          'Weak ' + m('F_0') + ': informed orders ' + m('(0,0)') + ' by synergy class (good, poor); belief ' + m(T`\mu(x)=\pi`) + ' after each order ' + m('x') + '; entry ' + m(T`e(x)=\rho`) + ' after each order; total entry ' + m(T`\rho`) + '; one stock price. Strong ' + m('F_1') + ': orders ' + m('(1,-1)') + '; beliefs after a sale, no order, a purchase are ' + m(T`(m(\pi),\pi,M(\pi))`) + '; entry is ' + m(T`(\rho,\rho,1)`) + '; prices rise strictly; total entry is ' + m(T`\rho+(1-\rho)(b+\pi\lambda)>\rho`) + '; entry under good synergy is ' + m(T`\rho+(1-\rho)(b+\lambda)`) + ', and under poor synergy ' + m(T`\rho+(1-\rho)b`) + '. Very strong ' + m('F_2') + ': orders and beliefs as at ' + m('F_1') + '; entry ' + m(T`\rho`) + ' after each order; total entry ' + m(T`\rho`) + '; three distinct prices.',
          'Ownership: ' + m(T`W_j(F)=\mathbb{E}_j[F(\theta)\mathbf{1}\{\theta\ge p\}]`) + ' is the win chance of a prepared rival in case ' + m('j') + ', where ' + m(T`\theta`) + ' is its value and the indicator ' + m(T`\mathbf{1}\{\theta\ge p\}`) + ' equals one when the value meets the reserve ' + m('p') + ', and zero otherwise. Good-synergy ownership rises from ' + m('F_0') + ' to ' + m('F_1') + ' exactly when ' + m(T`e_H W_H(F_1)>\rho\,W_H(F_0)`) + ', with ' + m('e_H') + ' entry under good synergy at ' + m('F_1') + '. If ' + m('W_H(F_1)=1') + ', good-synergy ownership rises from ' + m(T`\pi\rho`) + ' to ' + m(T`\pi e_H`) + ', and the good-synergy share of rival wins rises strictly exactly when ' + m('W_L(F_0)>0') + '.',
          'The outcome in each economy is unique under each of the four tie-rule pairs. With the example synergy values and reserve of ' + link('main:s14', 'frame 14') + ', (H1) to (H3) hold together on an open set of inputs.'], 0) +
        B('main:s13') }, 'main:s13');

    var returns = function () { return nav(back('main:s11', '11'), back('main:s12', '12'), back('main:s13', '13')); };
    bk({ id: 'b2', label: 'B2', targets: ['app:b2'], title: 'Why each outcome is unique', subtitle: 'Posterior bounds, entry and prices',
      body: ul(['<b>Lemma A.1</b> (order probabilities and beliefs), for any order plans: each order has positive probability in each synergy class. For a sale or a purchase, the chance of that order in class ' + m('j') + ' lies between ' + m('b') + ' and ' + m(T`b+\lambda`) + ', where ' + m(T`b=(1-\lambda)\beta`) + ' is the liquidity mass in one direction and ' + m(T`\lambda`) + ' is presence. With ' + m(T`u=\lambda/b`) + ', each nonzero order has likelihood ratio between ' + m('1/(1+u)') + ' and ' + m('1+u') + ', so the belief ' + m(T`\mu`) + ' after that order lies in ' + m(T`[m(\pi),M(\pi)]`) + ', where ' + m(T`M(\pi)=\pi(1+u)/[\pi(1+u)+1-\pi]`) + ' and ' + m(T`m(\pi)=\pi/[\pi+(1-\pi)(1+u)]`) + '. The no-order case lies in the same band when ' + m(T`\beta\le1/3`) + '. Under full orders, good synergy buys and poor synergy sells, the beliefs after a sale, no order, a purchase are ' + m(T`(m(\pi),\pi,M(\pi))`) + '. A belief at a price lies between the smallest and largest beliefs of the orders with that price.',
          '<b>Lemma A.2</b> (entry and prices): entry ' + m(T`e(x)\ge\rho`) + ' after each order ' + m('x') + ', with entry floor ' + m(T`\rho\in(0,1)`) + '. The price after order ' + m('x') + ' is ' + m(T`P(x)=t_0+e(x)[t_L-t_0+\Delta_T\,\mu(x)]`) + ', with proceeds ' + m('t_0') + ' without entry and ' + m('t_L') + ' under poor synergy. When ' + m(T`\Delta_T>0`) + ' and rival gross profit rises with the belief ' + m(T`\mu`) + ', equal prices give equal beliefs, so the price reveals ' + m(T`\mu(x)`) + '; entry is ' + m(T`\rho`) + ' when ' + m(T`\mu(x)<\tau`) + ' and ' + m('1') + ' when ' + m(T`\mu(x)\ge\tau`) + ', with threshold ' + m(T`\tau`) + ' (at ' + m(T`\mu(x)=\tau`) + ', any entry in ' + m(T`[\rho,1]`) + ' can hold when an indifferent high-cost rival may prepare with any probability); prices rise strictly with ' + m(T`\mu`) + '.'], 21) +
        returns() }, 'main:s11');

    var proofFlow = '<div class="pflow">' + [
      ['Weak: gain cap below ' + m('k'), m(T`K_j\le\Delta_0<k`)],
      ['Strong: gain floor above ' + m('k'), m(T`K_j\ge\rho\kappa(\pi)\Delta_1>k`)],
      ['Purchase reaches ' + m(T`M(\pi)`), m(T`B_1(M(\pi))>c_H`)],
      ['Very strong: ' + m(T`M(\pi)`) + ' falls short', m(T`B_2(M(\pi))<c_H`)]].map(function (b, i) {
        return (i ? '<span class="farrow" aria-hidden="true"></span>' : '') + '<div class="fbox pbox' + (i === 3 ? ' cost' : '') + '"><span class="ptag">' + (i + 1) + '</span>' + b[0] + '<br>' + b[1] + '</div>';
      }).join('') + '</div>';
    bk({ id: 'b2b', label: 'B2b', cls: 'sz-f', title: 'Why each outcome is unique', subtitle: 'Trading bounds and the four-step proof',
      body: ul(['<b>Lemma A.3</b> (informed trading): the gain before order cost ' + m('k') + ' from a correct purchase under good synergy is ' + m(T`K_H=e(1)\,\Delta_T\,[1-\mu(1)]`) + '; from a correct sale under poor synergy, ' + m(T`K_L=e(-1)\,\Delta_T\,\mu(-1)`) + '. Under every order plan, ' + m(T`\rho\,\Delta_T[1-M(\pi)]\le K_H\le\Delta_T`) + ' and ' + m(T`\rho\,\Delta_T\,m(\pi)\le K_L\le\Delta_T`) + '. With ' + m(T`\kappa(\pi)=\min\{m(\pi),1-M(\pi)\}`) + ', each gain lies between ' + m(T`\rho\,\kappa(\pi)\,\Delta_T`) + ' and ' + m(T`\Delta_T`) + '; the purchase bound uses ' + m(T`1-M(\pi)`) + ' and the sale bound uses ' + m(T`m(\pi)`) + '. A wrong-signed order earns at most ' + m('-k') + '. Good synergy buys when ' + m('K_H>k') + ' and stays out when ' + m('K_H<k') + '; poor synergy compares ' + m('K_L') + ' with ' + m('k') + ' in the same way.',
          'Four-step proof: 1. Weak: each gain is at most ' + m(T`\Delta_T`) + ', below ' + m('k') + ', so no informed order; the belief stays at the prior; entry stays at ' + m(T`\rho`) + '. 2. Strong: each gain is at least ' + m(T`\rho\,\kappa(\pi)\,\Delta_T`) + ', above ' + m('k') + ', so full orders hold under every candidate; beliefs are ' + m(T`(m(\pi),\pi,M(\pi))`) + '. 3. A purchase reaches ' + m(T`M(\pi)`) + ', rival gross profit there strictly exceeds the high cost, so entry after a purchase is ' + m('1') + '; after other orders entry stays at ' + m(T`\rho`) + '. 4. Very strong: full orders stay, but rival gross profit at ' + m(T`M(\pi)`) + ' falls short of the high cost, so entry returns to ' + m(T`\rho`) + ' after each order.'], 14) +
        vsp(21) + center(dg(proofFlow)) + vsp(14) +
        P('Each comparison is strict, so no tie rule changes the outcome.', 'fs-s') +
        returns() }, 'main:s11');

    bk({ id: 'b3', label: 'B3', targets: ['app:b3'], widget: 'region', title: 'Informative and uninformative markets at one strength', subtitle: 'Proposition 3 · Paper §4.3 · Default tie rules',
      body: cols([[0.29, vsp(7) + fig('region', 'Figure. The coexistence region at the prior in the plane of the shareholder spread and the threshold, with the path of the example; arrow keys move the cursor.')],
          [0.69, '<div class="fs-f">' + d(T`\pi<\tau\le M(\pi),\qquad \frac{k}{1-\tau}\ \le\ \Delta_T\ \le\ \frac{k}{\rho\max\{\pi,1-\pi\}}`) +
            ul(['Inside this region, two markets coexist. Uninformative market: no informed trade, one price, entry ' + m(T`\rho`) + '. Informative market: only a purchase recruits, and entry is' + d(T`\rho+(1-\rho)\min\Bigl\{\frac{(1-\pi)\,b\,\Delta_T}{k},\ b+\pi\lambda\Bigr\}`),
              'Entry in the informative market rises strictly with ' + m(T`\Delta_T`) + ' while the informed trader mixes on good synergy. Entry stays flat once the informed trader buys for sure on good synergy. The informative market is unique inside the region.',
              'Self-confirming logic, market by market. Expect no recruitment: one order earns at most the floor return, so silence pays. Expect recruitment: a purchase lifts entry, so trade pays.'], 4) + '</div>']]) +
        smallline('Scope: synergy ranking, ' + m(T`\Delta_T>0`) + ', ' + m('g_H>g_L') + ', default tie rules. In general, strengths with coexistence need not form one interval. Interval results: Backup B3, page 3.') +
        takeaway('Between the Proposition 2 economies, an uninformative and an informative equilibrium can coexist at one strength.') +
        B('main:s16') }, 'main:s16');

    bk({ id: 'b3b', label: 'B3b', widget: 'coex', title: 'Informative and uninformative markets at one strength', subtitle: 'Corollary 2 · Paper §4.3',
      body: center(fig('coex', 'Figure. Entry against strength in each equilibrium of the example: the whole path (a) and the strengths from r_A to past r_S (c), with the coexistence band; arrow keys move the cursor.', 'coexfig')) +
        P('Entry against strength ' + m('r') + '. Shaded band: coexistence interval ' + m('[r_A,r_N]') + '.', 'fs-f') +
        ul(['Informative entry starts at ' + m(T`{{entry_rA_B}}`) + ' when ' + m(T`r_A\approx{{rA|3}}`) + ' opens the band. Uninformative entry stays at ' + m(T`{{entry_r0}}`) + '.',
          'Informative entry rises to ' + m(T`{{entry_plateau_B}}`) + ' at ' + m(T`r_F\approx{{rF_B|3}}`) + ', where the informed trader buys for sure on good synergy. Informative entry then stays flat.',
          'The uninformative market dies at ' + m(T`r_N\approx{{rN|3}}`) + '. Informative entry holds to ' + m('r_C') + ', then drops to its floor.'], 0, 'fs-f') +
        takeaway('Along one path, entry can climb, sit flat, then fall — with a jump when the informative market opens.') +
        footline('Full equilibrium list and marked strengths ' + m('r_J') + ', ' + m('r_S') + ': Backup B3, page 3.') +
        B('main:s16') }, 'main:s16');

    bk({ id: 'b3c', label: 'B3c', title: 'Informative and uninformative markets at one strength', subtitle: 'Coexistence in full: interval parts and marked strengths',
      body: center(table({ cls: 'fs-f stretch-108', head: ['Strength', 'Value in the example', 'Role'], rows: [
          [m('r_A'), m(T`{{rA}}`), 'first strength with an informative market'],
          [m('r_F'), m(T`{{rF_B}}`), 'first strength with a certain purchase in it'],
          [m('r_N'), m(T`{{rN}}`), 'last strength with an uninformative market'],
          [m('r_J'), m(T`{{rJ}}`), 'the full purchase is alone from here'],
          [m('r_S'), m(T`{{rS_B}}`), 'the informed trader sells for certain on poor synergy from here'],
          [m('r_C'), m(T`{{rC_B}}`), 'entry ceiling: the top belief stops short of ' + m('c_H') + ' above ' + m('r_C')]] })) +
        ul(['Before ' + m('r_A') + ', a purchase cannot pay at any mix rate, so no informative market exists',
          'On ' + m('[r_A,r_F)') + ', the mix rate adjusts with strength and entry rises with it',
          'From ' + m('r_F') + ' to ' + m('r_N') + ', a full purchase coexists with an uninformative market and entry in it is constant',
          'Past ' + m('r_N') + ', an uninformative market fails: a unit order against the uninformative price pays. Mixed orders at the entry floor join the full purchase on ' + m('(r_N,r_J)') + '. From ' + m('r_J') + ', the full purchase is alone'], 5, 'fs-f') +
        P('In general, strengths with coexistence need not form one interval. Sure-purchase strengths form one interval. Under the nonfalling product ' + m(T`\Delta_T(g_H-c_H)`) + ', the whole set forms one interval at each prior.', 'fs-f') +
        B('main:s16') }, 'main:s16');

    bk({ id: 'b4', label: 'B4', targets: ['app:b4'], title: 'Price access and sale terms', subtitle: 'Price access and sale terms · Paper §7',
      body: cols([[0.53, P('At the strong incumbent ' + m('F_1') + ', under (H1)–(H3), price access raises expected target proceeds and surplus net of preparation costs.', 'fs-f') +
            P('Why: informed trader orders stay full when the price hides, so trading cost matches in both worlds. Access adds only preparation where profit covers the cost.', 'fs-f')],
          [0.45, table({ widths: [155, 210, 225], align: 'lcc', cls: 'fs-f stretch-120', head: ['', 'Expected target proceeds', 'Surplus net of preparation costs'], rows: [
            ['Price seen', q('p2_base_r1_proceeds'), q('p2_base_r1_surplus')],
            ['Price hidden', q('p2_base_hidden_proceeds'), q('p2_base_hidden_surplus')]] })]]) +
        smallline('Scope: inside the recruitment region, where the high cost does not pay at the prior. Outside that region, an informative price can deter preparation after a sale. Detail: Backup B4, page 2.') +
        ruleL +
        P('<b>Payment rule (separate bargaining set-up: zero reserve, point-mass classes, ' + m('R<h') + ').</b> Competition moves the spread with the sign of ' + m(T`1-2\omega`) + ', where ' + m(T`\omega`) + ' is seller bargaining weight. Second price is ' + m(T`\omega=0`) + ': full weight on the runner-up bid.') +
        P('<b>Reserve.</b> A reserve that excludes poor synergy can make the price informative at both strengths. Entry then sits flat in strength. Strict deterrence needs still more.') +
        takeaway('Sale terms set the payment to win and the information in the stock price before entry.') +
        B('main:s17') }, 'main:s17');

    bk({ id: 'b4b', label: 'B4b', title: 'Price access and sale terms', subtitle: 'Sale terms in full: access, payment rule, reserves',
      body: ul(['<b>Price access (A.7):</b> at ' + m('r_1') + ', proceeds gain equals ' + m(T`{{p2_access_proceeds_gain}}`) + ' and net surplus gain equals ' + m(T`{{p2_access_surplus_gain}}`),
          'Orders and trade costs are the same in the two access cases at ' + m('r_1') + '. Access adds preparation only after a purchase',
          '<b>Reserve (A.9):</b> at the reserve ' + m(T`{{rsv_points_excl}}`) + ', which excludes poor synergy, full orders hold at both strengths and entry is flat',
          'Strict deterrence needs reserve ' + m(T`{{rsv_deter}}`) + ', a level that excludes poor synergy and the weak incumbent',
          '<b>Payment rule (A.8):</b> zero reserve, point-mass classes, ' + m('R<h') + '. With seller share ' + m(T`\omega`) + ', the spread is ' + m(T`\Delta_\omega=\omega(h-\ell)+(1-2\omega)\mathbb{E}[(R-\ell)_+]`) + ', so its response weakly has the sign of ' + m(T`1-2\omega`) + '; strictly when ' + m(T`\omega\ne1/2`) + ' and ' + m(T`\mathbb{E}[(R-\ell)_+]`) + ' changes strictly'], 14) +
        vsp(7) +
        P('Exact differences at ' + m('F_1') + ', with ' + m(T`\mathcal R`) + ' expected target proceeds and ' + m(T`\mathcal W`) + ' expected surplus net of preparation costs; superscripts ' + m('1') + ' price access, ' + m('0') + ' neither price nor order:', 'fs-f') +
        '<div class="fs-f">' + d(T`\begin{aligned}\mathcal R^1-\mathcal R^0&=(1-\rho)\{\pi(b+\lambda)(t_H-t_0)+(1-\pi)b(t_L-t_0)\}>0,\\\mathcal W^1-\mathcal W^0&=(1-\rho)(b+\pi\lambda)\,[B_1(M(\pi))-c_H+pF_1(p)]>0.\end{aligned}`) + '</div>' +
        P('Preparation, sale, and two admissible bidders are three distinct events once a reserve can exclude.') +
        B('main:s17') }, 'main:s17');

    bk({ id: 'b5', label: 'B5', targets: ['app:b5'], cls: 'sz-n', title: 'Who the informed trader is',
      body: vsp(35) +
        ul(['The informed trader is an outsider with sector expertise. It holds no net position in the target before trade. It has no control rights, and it cannot acquire the target.',
          'Its information concerns the rival’s synergy class. It forms that view from its own research on the target’s customers, technology, and demand.',
          'It observes the synergy class, good synergy (' + m('H') + ') or poor synergy (' + m('L') + '). It does not observe the rival’s value.',
          'Neither bidder trades target shares. The informed trader stands outside the sale and earns only its trading payoff: sale proceeds per share minus the stock price on a purchase, the reverse on a sale, less order cost ' + m('k') + ' on a nonzero order.'], 42) +
        B('main:s6') }, 'main:s6');

    bk({ id: 'b6', label: 'B6', targets: ['app:b6'], title: 'Scope', subtitle: 'Scope checks · Paper §6 · Each row keeps the slot and varies one part',
      body: vsp(14) +
        table({ widths: [460, 1000], cls: 'stretch-130', head: ['Change one part', 'Result'], rows: [
          ['Any preparation-cost law', 'Under (H2), low costs below ' + m(T`B_1(m(\pi))`) + ' and high costs between ' + m(T`B_0(\pi)`) + ' and ' + m(T`B_1(M(\pi))`) + ', with atoms or without atoms, keep the rise. An atomless high-cost component turns the ceiling drop into a ramp.'],
          ['Any ranked classes with class ' + m('H') + ' higher in mean, any prior', 'For uniform incumbent values, an open set of strengths and costs delivers the reversal. Point-mass synergy values are not the kind case.'],
          ['Many synergy classes', 'The reversal holds under a separation condition. Without separation, one price can carry two synergy mixes.'],
          ['Rival has its own signal', 'At prior ' + m('1/2') + ', the rise can hold when the rival’s accuracy ' + m(T`\alpha_C`) + ' exceeds the informed trader’s accuracy ' + m(T`\alpha_I`) + '. In the stated signal example, entry needs both signals.']] }) +
        takeaway('The slot carries the mechanism. The shapes around the slot can change.') +
        footline('Formal statements and the six-economy table: Backup B6, pages 2 and 3. Continuous order sizes: Backup B15.') +
        B('main:s13') }, 'main:s13');

    bk({ id: 'b6b', label: 'B6b', title: 'Scope', subtitle: 'Scope in full: costs, synergy classes, separation, signals',
      body: vsp(7) +
        cols([[0.485, colhead('Cost laws (A.3)') + P('The reversal holds with atoms or without atoms; an atomless high component turns the drop at the entry ceiling into a ramp') + vsp(32) +
            colhead('Many synergy classes (A.5)') + P('The result holds under a separation condition on synergy proceeds; without it one price can pool two beliefs') + P('Without separation, two orders can carry two synergy mixes at one price.')],
          [0.485, colhead('General values, priors (A.4)') + P('Proposition 2 holds for every ranked pair with class ' + m('H') + ' higher in mean, and every prior, at suitable uniform incumbent values and costs, under (H1)–(H3) with ' + m(T`m(\pi)`) + ', ' + m(T`M(\pi)`)) + vsp(32) +
            colhead('Private signals (A.6)') + P('In the example, accuracies ' + m(T`(\alpha_I,\alpha_C)=({{sig_comp_aT}},{{sig_comp_d}})`) + ' give entry ' + m(T`{{p4_comp_b_r0_entry}}\to{{p4_comp_b_r1_entry}}`) + '; without the rival’s signal entry is ' + m(T`{{p4_comp_b_no_y_r1_entry}}`) + ' at both strengths')]]) +
        B('main:s13') }, 'main:s13');

    var U = function (a, b) { return m(T`U[{{` + a + T`}},{{` + b + T`}}]`); };
    var econ = function (name, k, poorU, goodU, noR2) {
      var c = function (x) { return q('p2_input_' + k + '_' + x); };
      return [name, poorU ? U('p2_input_' + k + '_low_lo', 'p2_input_' + k + '_low_hi') : m('{{p2_input_' + k + '_low_lo}}'),
        goodU ? U('p2_input_' + k + '_high_lo', 'p2_input_' + k + '_high_hi') : m('{{p2_input_' + k + '_high_lo}}'),
        c('pi'), c('cost'), c('k'), c('r0'), c('r1'), noR2 ? '' : c('r2')];
    };
    var out = function (name, k) { return '<tr><td>' + name + '</td><td class="c">' + q('p2_' + k + '_r0_entry') + '</td><td class="c">' + q('p2_' + k + '_r1_entry') + '</td><td colspan="6">' + q('p2_' + k + '_r1_ownership') + '</td></tr>'; };
    var row = function (cells, cls) { return '<tr' + (cls ? ' class="' + cls + '"' : '') + '>' + cells.map(function (c, i) { return '<td' + (i > 2 ? ' class="c"' : '') + '>' + c + '</td>'; }).join('') + '</tr>'; };
    bk({ id: 'b6c', label: 'B6c', title: 'Scope',
      body: center('<table class="tj fs-x stretch-100 econ"><thead><tr class="panel"><th colspan="9"><em>Panel A. Primitives</em></th></tr>' +
          '<tr><th>Economy</th><th>Poor synergy</th><th>Good synergy</th><th class="c">' + m(T`\pi`) + '</th><th class="c">' + m('c_H') + '</th><th class="c">' + m('k') + '</th><th class="c">' + m('r_0') + '</th><th class="c">' + m('r_1') + '</th><th class="c">' + m('r_2') + '</th></tr></thead><tbody>' +
          row(econ('Moderate gap', 'moderate', false, false, true)) + row(econ('Narrow bands', 'bands', true, true)) + row(econ('Low prior', 'ex_a')) +
          row(econ('High prior', 'ex_b')) + row(econ('Wide classes', 'ex_c', true, true)) + row(econ('Same means, points', 'ex_d')) +
          '<tr class="mid"><td colspan="9"><em>Panel B. Outcomes</em></td></tr>' +
          '<tr><td>Economy</td><td class="c">Entry ' + m(T`\mathsf{E}_0`) + '</td><td class="c">Entry ' + m(T`\mathsf{E}_1`) + '</td><td colspan="6">Good-synergy ownership ' + m(T`\mathsf{O}_{H,1}`) + '</td></tr>' +
          out('Moderate gap', 'moderate').replace('<tr>', '<tr class="mid">') + out('Narrow bands', 'bands') + out('Low prior', 'ex_a') + out('High prior', 'ex_b') + out('Wide classes', 'ex_c') + out('Same means, points', 'ex_d') +
          '</tbody></table>') +
        B('main:s13') }, 'main:s13');

    var slotFlow = '<div class="sflow">' +
      '<div class="fbox sf-inv"><b>Informed trader</b> — fills the slot with probability ' + m(T`\lambda`) + '; sees synergy ' + m('j') + '; picks ' + m(T`q\in\{-1,0,1\}`) + '; a nonzero order costs ' + m('k>0') + '</div>' +
      '<div class="fbox sf-liq"><b>Liquidity trader</b> — fills the slot with probability ' + m(T`1-\lambda`) + '; sells, does nothing, or buys with chances ' + m(T`\beta,\ 1-2\beta,\ \beta`) + ', where ' + m(T`0<\beta\le 1/3`) + '</div>' +
      '<div class="fbox sf-slot"><b>Order slot</b> — one public order ' + m(T`X\in\{-1,0,1\}`) + '; no observer sees who filled it</div>' +
      '<div class="fbox sf-mm"><b>Market makers</b> — see ' + m('X') + ' only; set ' + m(T`P=\mathbb{E}[V_T\mid X]`) + ', where ' + m('V_T') + ' is the sale proceeds per share</div>' +
      '<div class="fbox cost sf-sb"><b>Rival</b> — sees the price ' + m('P') + ' and cost ' + m('C') + '; sees neither ' + m('X') + ' nor ' + m('j') + '</div>' +
      '<span class="sf-a sf-a1"></span><span class="sf-elbow"></span><span class="sf-a sf-a2"></span><span class="sf-a sf-a3"></span></div>';
    bk({ id: 'b7', label: 'B7', targets: ['app:b7'], cls: 'sz-n', title: 'The order slot in full', subtitle: 'The order slot · Paper §2.3',
      body: vsp(14) + center(dg(slotFlow)) + vsp(14) + ruleL + vsp(14) +
        P('A liquidity order in one direction arrives with probability ' + m(T`b=(1-\lambda)\beta`) + '. Set ' + m(T`u=\lambda/b`) + '. The number ' + m('1+u') + ' caps the likelihood ratio of one order.', 'fs-s') +
        vfill +
        footline('Alternative arrival: Dow and Gorton (1997). Unit orders and unit cost: Edmans, Goldstein and Jiang (2015). Zero-profit pricing: Glosten and Milgrom (1985); Kyle (1985).') +
        B('main:s6') }, 'main:s6');

    bk({ id: 'b8', label: 'B8', targets: ['app:b8'], cls: 'sz-n', title: 'Payoffs and Proposition 1 in full', subtitle: 'Payoff objects · Paper §2.4 and §3.1',
      body: vsp(21) +
        P('Take a prepared rival with value ' + m(T`\theta\ge p`) + '. It pays ' + m(T`\max\{p,R\}`) + ' when it wins. The incumbent pays ' + m(T`\theta`) + ' when it wins.') +
        d(T`t(\theta)=\mathbb{E}_R\bigl[\max\{p,\min(R,\theta)\}\bigr],\qquad g(\theta)=\mathbb{E}_R\bigl[(\theta-\max\{p,R\})_+\bigr],\qquad t(\theta)+g(\theta)=\theta`) +
        P(m(T`\mathbb{E}_R`) + ' averages over the incumbent’s value ' + m(T`R\sim F`) + '.', 'fs-s') +
        ul(['Synergy means: ' + m(T`t_j=\mathbb{E}_j[t(\theta)]`) + ' and ' + m(T`g_j=\mathbb{E}_j[g(\theta)]`) + ' for ' + m(T`j\in\{H,L\}`) + '. Without entry, ' + m(T`t_0=p[1-F(p)]`) + '.',
          'Shareholder spread: ' + m(T`\Delta_T=t_H-t_L`) + '. Read it as: how much more shareholders get with good synergy than with poor synergy.',
          'At belief ' + m(T`\mu=\Pr(H)`) + ', expected rival gross profit is ' + m(T`B(\mu)=g_L+\mu(g_H-g_L)`) + '.',
          'Win chance: ' + m(T`W_j(F)=\mathbb{E}_j[F(\theta)\mathbf 1\{\theta\ge p\}]`) + '. A good-synergy rival outbids ' + m('F') + ' when ' + m('W_H(F)=1') + '.'], 10) +
        takeaway('The traded claim and the rival’s claim sum to the same value. Strength moves the split.') +
        B('main:s10') }, 'main:s10');

    bk({ id: 'b8s', label: 'B8s', title: 'Payoffs and Proposition 1 in full', subtitle: 'Proposition 1 · Paper §3.1',
      body: vsp(14) +
        st('Proposition 1',
          P('Let ' + m(T`\tilde F\le F`) + ' be a first-order stochastic strengthening of the distribution ' + m('F') + '.') +
          P('(a) For any class laws with finite means, gross auction profit ' + m('g_H') + ' and ' + m('g_L') + ' weakly fall. Rival profit ' + m(T`B(\mu)`) + ' weakly falls at each fixed belief ' + m(T`\mu`) + '.') +
          P('(b) Under the class ranking ' + m(T`G_H\le G_L`) + ', the shareholder spread ' + m(T`\Delta_T`) + ' weakly rises.') +
          P('Under the class ranking, ' + m(T`\Delta_T(F)+g_H(F)-g_L(F)=\mathbb{E}_H[\max\{\theta,p\}]-\mathbb{E}_L[\max\{\theta,p\}]`) + ', with the rival’s value ' + m(T`\theta`) + ' and reserve ' + m('p') + '.')) +
        vsp(21) +
        ul(['Intuition: one class value gap is fixed, and strength moves its split between target proceeds and rival gross profit.']) +
        B('main:s10') }, 'main:s10');

    bk({ id: 'b8b', label: 'B8b', cls: 'sz-n', title: 'Payoffs and Proposition 1 in full', subtitle: 'Proposition 1 in full: forms, strict signs, equal admissibility',
      body: vsp(21) +
        ul(['With class gap ' + m(T`D(y)=G_L(y)-G_H(y)`) + ': ' + m(T`\Delta_T(F)=pF(p)D(p^-)+\int_p^\infty[1-F(y)]D(y)\,dy`) + ' and ' + m(T`g_j(F)=\int_p^\infty[1-G_j(y)]F(y)\,dy`) + '.',
          'Profit falls strictly exactly when ' + m(T`\int_p^\infty[1-G_j(y)][F(y)-\tilde F(y)]\,dy>0`) + '. Spread rises strictly exactly when ' + m(T`\int_p^\infty[F(y)-\tilde F(y)]D(y)\,dy>0`) + '.',
          'Without the class ranking, the reserve term ' + m(T`pF(p)D(p^-)`) + ' can reverse the spread sign. With no class atom at the reserve, the spread weakly rises under every strengthening exactly when class ' + m('H') + ' dominates above the reserve and the classes have equal admissibility, ' + m(T`G_H(p^-)=G_L(p^-)`) + '.'], 35) +
        B('main:s10') }, 'main:s10');

    bk({ id: 'b9', label: 'B9', targets: ['app:b9'], cls: 'sz-f', title: 'Equilibrium in full',
      body: ul(['Tuple: ' + m(T`\mathcal{E}=(\sigma_H,\sigma_L,\mu,P,\bar\mu,\zeta)`) + ', with truthful bids. Order distribution in class ' + m('j') + ': ' + m(T`\sigma_j`) + ' on ' + m(T`\{-1,0,1\}`) + '. Order belief: ' + m(T`\mu(x)=\Pr(j=H\mid X=x)`) + '. Stock price after order ' + m('x') + ': ' + m('P(x)') + '. Belief at a price: ' + m(T`\bar\mu(\bar P)=\Pr(j=H\mid P(X)=\bar P)`) + '. High-cost preparation probability at price ' + m(T`\bar P`) + ': ' + m(T`\zeta(\bar P)`) + '. Cost ' + m('C=0') + ' prepares at each price.',
          'Liquidity probabilities: ' + m(T`\eta(-1)=\eta(1)=\beta`) + ' and ' + m(T`\eta(0)=1-2\beta`) + '. Order probability in class ' + m('j') + ': ' + m(T`f_j(x)=(1-\lambda)\eta(x)+\lambda\sigma_j(x)`) + ', with presence ' + m(T`\lambda`) + '. Entry after order ' + m('x') + ': ' + m(T`e(x)=\rho+(1-\rho)\zeta(P(x))`) + ', with entry floor ' + m(T`\rho`) + '.',
          '(E1) Order beliefs by Bayes’ rule: ' + m(T`\mu(x)=\pi f_H(x)/[\pi f_H(x)+(1-\pi)f_L(x)]`) + ' after each order ' + m('x') + ', with prior ' + m(T`\pi`) + '.',
          '(E2) Beliefs at a price by Bayes’ rule: ' + m(T`\bar\mu(\bar P)=\pi\sum_{x:\,P(x)=\bar P}f_H(x)\big/\sum_{x:\,P(x)=\bar P}[\pi f_H(x)+(1-\pi)f_L(x)]`) + ' at each price ' + m(T`\bar P`) + ' that occurs.',
          '(E3) Preparation: ' + m(T`\zeta(\bar P)=1`) + ' when rival gross profit ' + m(T`B(\bar\mu(\bar P))>c_H`) + ', and ' + m(T`\zeta(\bar P)=0`) + ' when ' + m(T`B(\bar\mu(\bar P))<c_H`) + ', with high cost ' + m('c_H') + '. At equality, the tie rule applies.',
          '(E4) Competitive prices: ' + m(T`P(x)=\mathbb{E}[V_T\mid X=x]`) + ' after each order ' + m('x') + ', with sale proceeds per share ' + m('V_T') + '. In payoff objects, ' + m(T`P(x)=t_0+e(x)[t_L-t_0+\Delta_T\,\mu(x)]`) + ', with shareholder spread ' + m(T`\Delta_T`) + ' and class proceeds ' + m('t_L') + ', ' + m('t_0') + ' from frame 8.',
          '(E5) Orders: ' + m(T`\sigma_j(q)>0`) + ' only when the order ' + m('q') + ' maximizes the informed trader’s class-' + m('j') + ' payoff ' + m(T`U_j(q)=q[t_0+e(q)(t_j-t_0)-P(q)]-k|q|`) + ', with order cost ' + m('k') + '. Prices ' + m('P') + ' and entry ' + m('e') + ' stay at the stated functions.',
          '(E6) Truthful bids: each prepared bidder with value at or above reserve ' + m('p') + ' bids its value.',
          'Tie rules, default pair: an indifferent informed trader may mix over its best orders, and an indifferent rival at cost ' + m('c_H') + ' prepares. Other rules: an indifferent informed trader abstains, or an indifferent rival at cost ' + m('c_H') + ' prepares with any probability.'], 7) +
        B('main:s9') }, 'main:s9');

    bk({ id: 'b10', label: 'B10', targets: ['app:b10'], title: 'The example in full',
      body: cols([[0.43, table({ widths: [null, 175, 255], cls: 'fs-x stretch-110', head: ['Input', 'Value', 'Meaning'], rows: [
            [m('h') + ', ' + m(T`\ell`), m(T`{{prim_h}}`) + ', ' + m(T`{{prim_ell}}`), 'good-synergy and poor-synergy values'],
            [m('p'), m(T`{{prim_p}}`), 'reserve price'],
            [m(T`\pi`) + ', ' + m(T`\rho`), m(T`{{prim_pi}}`) + ', ' + m(T`{{prim_rho}}`), 'prior on good synergy; probability of zero cost'],
            ['Costs ' + m('0') + ', ' + m('c_H') + ', ' + m('k'), m('0') + ', ' + m(T`{{prim_cH}}`) + ', ' + m(T`{{prim_k}}`), 'preparation costs; cost of a nonzero order'],
            [m(T`\beta`) + ', ' + m(T`\lambda`), m(T`{{beta_B}}`) + ', ' + m(T`{{lambda_B}}`), 'liquidity order chance; informed presence chance'],
            [m('u') + ', ' + m('b'), m(T`{{u_B}}`) + ', ' + m(T`{{b_B}}`), 'mass ratio ' + m(T`u=\lambda/b`) + '; here ' + m(T`1+u=\mathrm{e}`)],
            [m('r_0,r_1,r_2'), m(T`{{prim_r0}}`) + ', ' + m(T`{{prim_r1}}`) + ', ' + m(T`{{prim_r2}}`), 'weak, strong, stronger still']] })],
          [0.55, table({ widths: [245, 330, null], cls: 'fs-x stretch-110', head: ['Object', 'Region', 'Example'], rows: [
            ['Mass ratio ' + m('u') + ' (Corollary 1)', m(T`({{u_lo}},{{u_hi}})`), m(T`{{u_B}}`)],
            ['Top belief ' + m('M') + ' at prior ' + m(T`{{prim_pi}}`), m(T`({{M_lo}},{{M_hi}})`), m(T`{{M_half_B}}`)],
            ['Liquidity chance ' + m(T`\beta`), m(T`0<\beta\le 1/3`), m(T`{{beta_B}}`)],
            ['Presence chance ' + m(T`\lambda`) + ' at that ' + m(T`\beta`), 'from ' + m(T`u=\lambda/((1-\lambda)\beta)`), m(T`{{lambda_B}}`)],
            ['Prior ' + m(T`\pi`) + ' for Proposition 2', m(T`({{prior_lo_B}},{{prior_hi_B}})`), m(T`{{prim_pi}}`)],
            ['Research cost ' + m('a') + ' (Proposition A.1)', m(T`({{res_a_lo}},{{res_a_up}})`), m(T`{{res_a}}`)],
            ['Research cap ' + m(T`\bar\lambda`), m(T`({{res_cap_lo}},{{res_cap_hi}})`), m(T`{{res_cap}}`)]] })]]) +
        vsp(21) +
        gray('Each region is cut out by strict inequalities, so the results hold on an open set of inputs.') +
        B('main:s14') }, 'main:s14');

    var R3 = function (label, a, b, c, bold) { return [label, q(a), bold ? '<b>' + q(b) + '</b>' : q(b), q(c)]; };
    bk({ id: 'b11', label: 'B11', targets: ['app:b11'], title: 'Outcomes and controls in full', subtitle: 'Corollary 1 · Paper §4.2',
      body: vsp(10) +
        center(table({ widths: [560, 260, 260, 290], align: 'lccc', cls: 'stretch-115', head: ['', 'Weak ' + m(T`r_0={{prim_r0}}`), 'Strong ' + m(T`r_1={{prim_r1}}`), 'Very strong ' + m(T`r_2={{prim_r2}}`)], rows: [
          ['Rival profit at the prior, ' + m(T`B_r({{prim_pi}})`), q('Bprior_r0'), q('Bprior_r1_B'), q('Bprior_r2')],
          ['Shareholder spread, ' + m(T`\Delta_T(r)`), q('Delta_r0'), q('Delta_r1'), q('Delta_r2')],
          ['Informed trader orders (good synergy, poor synergy)', m(T`(0,\ 0)`), m(T`(1,\ {-1})`), m(T`(1,\ {-1})`)],
          ['Price', 'Uninformative', 'Informative', 'Informative'],
          R3('Entry', 'entry_r0', 'entry_r1_B', 'entry_r2', true),
          R3('Good-synergy ownership', 'own_r0', 'own_r1_B', 'own_r2_B', true)] })) +
        takeaway('At each step, rival gross profit falls and the shareholder spread rises. Entry rises against the strong incumbent and returns to its floor against the very strong one.') +
        footline('In the example at prior ' + m(T`{{prim_pi}}`) + ', (H1)–(H3) hold exactly when the top belief sits between the two thresholds: ' + m(T`\tau(r_1)<M({{prim_pi}})<\tau(r_2)`) + '. Region and margins: Backup B10. Fixed-information control: Backup B11, pages 2 and 3. Full payoff and outcome tables: Backup B11, pages 4 to 6.') +
        B('main:s15') }, 'main:s15');

    bk({ id: 'b11s', label: 'B11s', title: 'Outcomes and controls in full', subtitle: 'Fixed-information control · Paper §4.2 and Proposition A.2',
      body: vsp(7) + ruleL + vsp(10) +
        P('Fix the law of synergy and signal, the synergy value laws, and the cost law. A stronger incumbent cannot raise entry.') + vsp(8) +
        P('Entry falls by exactly the chance that the preparation cost ' + m('C') + ' sits between rival gross profit at the two strengths.') + vsp(3) + ruleL +
        center(table({ widths: [660, 260, 260], align: 'lcc', cls: 'fs-s stretch-105', head: ['Entry', 'Weak ' + m('r_0'), 'Strong ' + m('r_1')], rows: [
          ['Full model, orders re-solved', q('entry_r0'), '<b>' + q('entry_r1_B') + '</b>'],
          ['Full orders held fixed at each strength', q('p4_frozen_r0_entry'), q('p4_frozen_r1_entry')],
          ['Rival cannot see the price', q('p4_hidden_r0_entry'), q('p4_hidden_r1_entry')]] })) +
        smallline('Row 2 at ' + m('r_0') + ' is a control, not an equilibrium. In the slot, fixed order laws give the same belief after each order at each strength.') +
        takeaway('The rise needs the signal itself to change with strength. Frozen news gives flat entry, then a fall past the ceiling.') +
        B('main:s15') }, 'main:s15');

    bk({ id: 'b11f', label: 'B11f', title: 'Outcomes and controls in full', subtitle: 'The exact fall of entry under fixed information · Proposition A.2',
      body: vsp(21) +
        st('Proposition A.2 (Fixed information)',
          P('Fix the joint law of class ' + m('j') + ' and signal ' + m('S') + ', the class value laws ' + m('G_j') + ', and an independent cost law for preparation cost ' + m('C') + '. Conditional on ' + m('(j,S)') + ', the values ' + m(T`\theta`) + ' and ' + m('R') + ' are independent with laws ' + m('G_j') + ' and ' + m('F_i') + ' in economy ' + m('i') + ', with signal belief ' + m(T`\mu(S)=\Pr(j=H\mid S)`) + '. For a strengthening from ' + m('F_0') + ' to ' + m('F_1') + ', total entry ' + m(T`\mathsf{E}`) + ' falls by exactly ' + m(T`\mathsf{E}_0-\mathsf{E}_1=\Pr\{B_1(\mu(S))<C\le B_0(\mu(S))\}\ge0`) + ', with rival gross profit ' + m('B_i') + ' at ' + m('F_i') + '.')) +
        vsp(28) +
        ul(['The rival still reads the stock price ' + m('P') + ' here. The fixed object is the joint law of the signal and the class.']) +
        B('main:s15') }, 'main:s15');

    bk({ id: 'b11b', label: 'B11b', title: 'Outcomes and controls in full', subtitle: 'Proposition 2 in full: tuples, payoff tables, control panels',
      body: ol(['<b>Bounds for every profile:</b> belief band ' + m(T`m\le\mu\le M`) + '; gain per unit at most ' + m(T`\Delta_T`) + '; entry at least ' + m(T`\rho`),
          '<b>Weak ' + m('r_0') + ':</b> ' + m(T`\Delta_T(r_0)<k`) + ' makes each nonzero order lose in expectation. An uninformative market is the sole outcome; entry is ' + m(T`\rho`),
          '<b>Strong ' + m('r_1') + ':</b> ' + m(T`k<\rho\kappa\,\Delta_T(r_1)`) + ' makes each correct order pay under every profile; a wrong-signed order always loses. Orders are ' + m('(1,-1)'),
          '<b>Entry at ' + m('r_1') + ':</b> a buy order gives belief ' + m('M') + ' with ' + m(T`B_{r_1}(M)>c_H`) + ', so cost ' + m('c_H') + ' prepares after a buy order. Entry exceeds ' + m(T`\rho`),
          '<b>Return at ' + m('r_2') + ':</b> trade still pays, but ' + m(T`B_{r_2}(M)<c_H`) + ' keeps cost ' + m('c_H') + ' out at every price. Entry is ' + m(T`\rho`)], 10) +
        vsp(7) +
        P('Ownership: with ' + m(T`W_H(F)=\mathbb{E}_H[F(\theta)\mathbf{1}\{\theta\ge p\}]`) + ', good-synergy ownership rises exactly if ' + m(T`[\rho+(1-\rho)(b+\lambda)]W_H(F_1)>\rho W_H(F_0)`) + '.') + vsp(14) +
        P('Share rises exactly when ' + m(T`e_HW_H(F_1)W_L(F_0)>e_LW_H(F_0)W_L(F_1)`) + '; in the example, share rises from ' + m(T`{{share_H_r0}}`) + ' to ' + m(T`{{share_H_r1_B}}`) + '.') +
        B('main:s15') }, 'main:s15');

    var T3 = function (label, k) { return [label, q('p2_base_r0_' + k), q('p2_base_r1_' + k), q('p2_base_r2_' + k)]; };
    bk({ id: 'b11c', label: 'B11c', cls: 'sz-x', title: 'Outcomes and controls in full',
      body: P('Under full orders, a good-synergy rival faces a buy order with chance ' + m(T`\lambda+b`) + ', and a poor-synergy rival with chance ' + m('b') + '.', 'mt-n') +
        d(T`e_H=\rho+(1-\rho)(\lambda+b),\qquad e_L=\rho+(1-\rho)b,\qquad \text{entry}=\pi e_H+(1-\pi)e_L`) +
        cols([[0.49, ul(['At ' + m('r_1') + ', cost ' + m('c_H') + ' prepares after a buy order and only after a buy order. Synergy entry rates are ' + m('e_H') + ' and ' + m('e_L'),
            'At the example’s prior, entry is ' + m(T`{{entry_r1_B}}`) + ' and good-synergy ownership is ' + m(T`{{own_r1_B}}`),
            'At ' + m('r_0') + ', an uninformative market gives an uninformative price, so entry is ' + m(T`{{entry_r0}}`) + ' and ownership is ' + m(T`{{own_r0}}`)], 3)],
          [0.49, ul(['At ' + m('r_2') + ', no price covers ' + m('c_H') + ', so entry is ' + m(T`{{entry_r2}}`) + ' and ownership is ' + m(T`{{own_r2_B}}`) + ', with full orders',
            m(T`B_r(\pi)`) + ' equals ' + m(T`{{Bprior_r0}}`) + ', ' + m(T`{{Bprior_r1_B}}`) + ', ' + m(T`{{Bprior_r2}}`) + ' at ' + m('r_0') + ', ' + m('r_1') + ', ' + m('r_2')], 3)]]) +
        center(table({ widths: [640, null, null, null], align: 'lccc', cls: 'stretch-100', head: ['', m(T`r_0={{prim_r0}}`), m(T`r_1={{prim_r1}}`), m(T`r_2={{prim_r2}}`)], rows: [
          T3('Proceeds without entry, ' + m('t_0'), 't0'), T3('Proceeds with a good-synergy rival, ' + m('t_H'), 'th'), T3('Proceeds with a poor-synergy rival, ' + m('t_L'), 'tl'),
          ['Shareholder spread, ' + m(T`\Delta_T`), q('Delta_r0'), q('Delta_r1'), q('Delta_r2')],
          T3('Rival profit, good synergy, ' + m('g_H'), 'gh'), T3('Rival profit, poor synergy, ' + m('g_L'), 'gl'),
          ['Rival profit at the prior, ' + m(T`B_r({{prim_pi}})`), q('Bprior_r0'), q('Bprior_r1_B'), q('Bprior_r2')],
          ['Preparation threshold, ' + m(T`\tau(r)`), q('tau_r0'), q('tau_r1'), q('tau_r2')]] })) +
        B('main:s15') }, 'main:s15');

    var Q3 = function (label, a, b, c) { return [label, q(a), q(b), c ? q(c) : '']; };
    bk({ id: 'b11d', label: 'B11d', cls: 'sz-x', title: 'Outcomes and controls in full',
      body: center(table({ align: 'lccc', cls: 'stretch-098 mt-n', head: ['', m(T`r_0={{prim_r0}}`), m(T`r_1={{prim_r1}}`), m(T`r_2={{prim_r2}}`)], rows: [
          { panel: '<em>Panel A. Equilibrium (Proposition 2)</em>' },
          ['Informed orders, good synergy and poor synergy', m('(0,0)'), m('(1,-1)'), m('(1,-1)')],
          Q3('Belief after a sale', 'p2_base_r0_mu_minus', 'p2_base_r1_mu_minus', 'p2_base_r2_mu_minus'),
          Q3('Belief after no order', 'p2_base_r0_mu_zero', 'p2_base_r1_mu_zero', 'p2_base_r2_mu_zero'),
          Q3('Belief after a purchase', 'p2_base_r0_mu_plus', 'p2_base_r1_mu_plus', 'p2_base_r2_mu_plus'),
          ['High-cost preparation', 'none', 'after a purchase', 'none'],
          Q3('Price after a sale', 'price_r0', 'price_r1_m1_B', 'price_r2_m1_B'),
          Q3('Price after no order', 'price_r0', 'price_r1_0_B', 'price_r2_0_B'),
          Q3('Price after a purchase', 'price_r0', 'price_r1_p1_B', 'price_r2_p1_B'),
          Q3('Entry ' + m(T`\mathsf{E}`), 'entry_r0', 'entry_r1_B', 'entry_r2'),
          Q3('Good-synergy ownership ' + m(T`\mathsf{O}_H`), 'own_r0', 'own_r1_B', 'own_r2_B'),
          Q3('Expected target proceeds', 'p4_base_r0_proceeds', 'p4_base_r1_proceeds', 'p4_base_r2_proceeds'),
          'mid', { panel: '<em>Panel B. Full orders held fixed (Proposition A.2)</em>' },
          Q3('Entry ' + m(T`\mathsf{E}`), 'p4_frozen_r0_entry', 'p4_frozen_r1_entry'),
          Q3('Good-synergy ownership ' + m(T`\mathsf{O}_H`), 'p4_frozen_r0_own', 'p4_frozen_r1_own'),
          Q3('Expected target proceeds', 'p4_frozen_r0_proceeds', 'p4_frozen_r1_proceeds'),
          'mid', { panel: '<em>Panel C. The rival does not see the price</em>' },
          ['Informed orders, good synergy and poor synergy', m('(0,0)'), m('(1,-1)'), ''],
          Q3('Entry ' + m(T`\mathsf{E}`), 'p4_hidden_r0_entry', 'p4_hidden_r1_entry'),
          Q3('Good-synergy ownership ' + m(T`\mathsf{O}_H`), 'p4_hidden_r0_own', 'p4_hidden_r1_own'),
          Q3('Expected target proceeds', 'p4_hidden_r0_proceeds', 'p4_hidden_r1_proceeds')] })) +
        B('main:s15') }, 'main:s15');

    bk({ id: 'b12', label: 'B12', targets: ['app:b12'], title: 'Research in full', subtitle: 'Proposition 4 · Paper §5 · Prior ' + m('1/2'),
      body: vsp(4) +
        P('One change only. Before it learns the synergy, the informed trader picks research ' + m(T`\lambda\in[0,\bar\lambda]`) + ' at cost ' + m(T`(a/2)\lambda^2`) + '. Success has chance ' + m(T`\lambda`) + ', reveals the synergy, and fills the slot. Failure hands the slot to liquidity.', 'fs-s') + vsp(7) +
        P('More research adds informed trader orders and removes liquidity cover. The prior is ' + m('1/2') + ' throughout this block.', 'fs-s') +
        vsp(10) + ruleL + vsp(10) +
        P('At research ' + m(T`\lambda`) + ', write ' + m(T`M_\lambda`) + ' for the top belief after a purchase. Recruitment intensity ' + m(T`\lambda_E(\tau)`) + ' solves ' + m(T`M_\lambda=\tau`) + ': a full purchase recruits exactly at or past this research level.', 'fs-s') +
        ul(['In the recruiting equilibrium, research ' + m(T`\min\{\lambda_R(\Delta_T),\bar\lambda\}`) + ' rises strictly with ' + m(T`\Delta_T`) + ' until the cap, then stays at the cap.',
          'Entry ' + m(T`\rho+(1-\rho)[\beta+(1/2-\beta)\lambda]`) + ' rises with research. Good-synergy entry rises with research. Poor-synergy entry falls.',
          'The recruiting equilibrium exists exactly when ' + m(T`\Delta_T>2k`) + ' and ' + m(T`\tau\le M_\lambda`) + ' at ' + m(T`\lambda=\min\{\lambda_R(\Delta_T),\bar\lambda\}`) + '.'], 5, 'fs-s') +
        smallline('Interior research ' + m(T`\lambda_R(\Delta_T)`) + ' solves ' + m(T`2a\lambda=\Delta_T m_\lambda-k+(\rho\Delta_T m_\lambda-k)_+`) + ', with band floor ' + m(T`m_\lambda=1-M_\lambda`) + '. Branches: Backup B12, page 3. Scope: default tie rules, ' + m(T`\tau>1/2`) + '.') +
        takeaway('A wider spread pays for more research. More research brings in a good-synergy rival more often.') +
        B('main:s16') }, 'main:s16');

    bk({ id: 'b12b', label: 'B12b', widget: 'research', title: 'Research in full', subtitle: 'Research corollary · Paper §5',
      body: vsp(4) + center(fig('research', 'Figure. Research (a) and total entry (b) against strength in each research equilibrium of the example; arrow keys move the cursor.', 'researchfig')) +
        P('Research ' + m(T`\lambda`) + ' and entry against strength ' + m('r') + '. Research cost ' + m(T`a={{res_a}}`) + '. Cap ' + m(T`\bar\lambda={{res_cap}}`) + '.', 'fs-s') + vsp(7) +
        ul(['Recruiting research opens at ' + m(T`r_R\approx{{res_rR|3}}`) + '. Entry there is ' + m(T`{{res_entry_rR}}`) + '.',
          'Research reaches the cap at ' + m(T`r_{\bar\lambda}\approx{{res_rcap|3}}`) + '. Entry reaches ' + m(T`{{res_entry_cap}}`) + ' and holds to ' + m('r_C') + '.',
          'Zero research coexists on ' + m('[r_0,r_N]') + '. At ' + m('r_1') + ' and ' + m('r_2') + ' the sole outcome sits at the cap and matches Proposition 2.'], 5, 'fs-s') +
        takeaway('At the cap, the research economy is the Proposition 2 economy.') +
        footline('Floor-entry research branch, cap region, and three-strength table: Backup B12, pages 3 and 4.') +
        B('main:s16') }, 'main:s16');

    bk({ id: 'b12c', label: 'B12c', title: 'Research in full', subtitle: 'Research in full: first-order condition, branches, cap region',
      body: d(T`2a\lambda=\Delta_T m_\lambda-k+(\rho\Delta_T m_\lambda-k)_+`) +
        ul(['Research picks ' + m(T`\lambda`) + ' in ' + m(T`[0,\bar\lambda]`) + ' before the slot, at cost ' + m(T`\tfrac{a}{2}\lambda^2`) + ' (Proposition 4)',
          'In the example, ' + m(T`a={{res_a}}`) + ' and the cap is ' + m(T`\bar\lambda={{res_cap}}`) + '. The marked strengths are ' + m(T`r_R\approx{{res_rR}}`) + ', ' + m(T`r_{\bar\lambda}\approx{{res_rcap}}`) + ', ' + m(T`r_N\approx{{res_rN}}`) + ', ' + m(T`r_Q\approx{{res_rQ}}`) + ', ' + m(T`r_C\approx{{res_rC}}`),
          'Zero research, with entry ' + m(T`\rho`) + ', is an equilibrium exactly on ' + m('[r_0,r_N]'),
          'Recruiting research is an equilibrium exactly on ' + m('[r_R,r_C]') + ': research rises from ' + m(T`{{res_lambda_rR}}`) + ' to the cap on ' + m(T`[r_R,r_{\bar\lambda})`) + ' and stays at the cap on ' + m(T`[r_{\bar\lambda},r_C]`) + '; entry rises from ' + m(T`{{res_entry_rR}}`) + ' to ' + m(T`{{res_entry_cap}}`) + ' and keeps that value up to ' + m('r_C')], 10, 'fs-s') +
        vsp(14) +
        P('Zero research on ' + m('[r_0,r_N]') + '; recruiting research on ' + m('[r_R,r_C]') + '; floor-entry research on ' + m('(r_N,r_Q)') + ' and ' + m('(r_C,r_2]') + ', with ' + m(T`r_Q\approx{{res_rQ|3}}`) + '.', 'fs-s') +
        B('main:s16') }, 'main:s16');

    bk({ id: 'b12d', label: 'B12d', title: 'Research in full',
      body: vsp(14) +
        ul(['Floor-entry research, in which the informed trader trades in both synergy classes after a success, no order recruits and entry is ' + m(T`\rho`) + ', is an equilibrium exactly on ' + m('(r_N,r_Q)') + ' and on ' + m('(r_C,r_2]') + '; there is no other equilibrium',
          'At ' + m(T`{{str_r155}}`) + ', ' + m(T`{{str_r160}}`) + ' and ' + m(T`{{str_r165}}`) + ' there are exactly two equilibria: zero research, and recruiting research below the cap (the informed trader buys on good synergy after a success and abstains on poor synergy). Research is ' + m(T`{{res_lambda_r155}}`) + ', ' + m(T`{{res_lambda_r160}}`) + ', ' + m(T`{{res_lambda_r165}}`) + '. Entry is ' + m(T`{{res_entry_r155}}`) + ', ' + m(T`{{res_entry_r160}}`) + ', ' + m(T`{{res_entry_r165}}`),
          'The unique equilibrium has zero research at ' + m('r_0') + ', recruiting research at the cap at ' + m('r_1') + ' and floor-entry research at the cap at ' + m('r_2') + ', where entry is ' + m(T`\rho`)], 10, 'fs-s') +
        gray('Costly research with an alternative arrival follows Dow and Gorton 1997.') +
        B('main:s16') }, 'main:s16');

    var levels = (function () {
      var y = function (v) { return Math.round(300 - 100 * v); };
      var vbrace = function (x, y0, y1, cls) {   /* a vertical brace from y0 (top) to y1 (bottom), its tip pointing left */
        var a = 8, mid = (y0 + y1) / 2;
        return '<path class="dg-brace ' + cls + '" d="M' + x + ',' + y0 + ' q-' + a + ',0 -' + a + ',' + a + ' V' + (mid - a) + ' q0,' + a + ' -' + a + ',' + a + ' q' + a + ',0 ' + a + ',' + a + ' V' + (y1 - a) + ' q0,' + a + ' ' + a + ',' + a + '"/>';
      };
      return svg(220, 330, 1, [[0, 'P(−1)'], [0.9, 'P(0)'], [2.75, 'P(1)']].map(function (l) {
          return '<line class="dg-level" x1="30" y1="' + y(l[0]) + '" x2="145" y2="' + y(l[0]) + '"/>' + text(152, y(l[0]) + 10, '_P_' + l[1].slice(1), { anchor: 'start', size: 32 });
        }).join('') + vbrace(26, y(0.9), y(0.02), 'muted') + vbrace(26, y(2.73), y(0.92), 'info'),
        'Three price levels P(−1), P(0) and P(1); the purchase impact above P(0) is larger than the sale impact below it.');
    })();
    bk({ id: 'b13', label: 'B13', targets: ['app:b13'], title: 'Predictions in full', subtitle: 'Predictions · Paper §8 · Full two-sided trade, prior below ' + m(T`\tau`),
      body: cols([[0.80, '<div class="fs-f">' +
            P('Weight each price impact by how often its order occurs. Weighted purchase impact beats weighted sale impact exactly when a purchase recruits the rival.') + vsp(5) +
            ul(['At prior ' + m('1/2') + ', order frequencies match. Compare raw impacts: ' + m('P(1)-P(0)') + ' against ' + m('P(0)-P(-1)') + '.',
              'The price gap ' + m('P(1)-P(-1)') + ' splits into a synergy part, ' + m(T`\rho\Delta_T[M(\pi)-m(\pi)]`) + ', and an entry part. The entry part is positive exactly under recruitment, and it sits wholly in the purchase impact.'], 2) + vsp(3) +
            ol(['Entry can rise with incumbent strength only when the price lands before preparation starts. Hide the price, and entry can only fall.',
              'Past the entry ceiling, orders stop predicting entry. Orders keep predicting the winner when ' + m('W_H>W_L') + '.',
              'At prior ' + m('1/2') + ', order counts cannot separate slot types. Prices can.'], 2) + vsp(2) +
            P('<b>Date the price before preparation starts. Record the zero order.</b>') + '</div>'],
          [0.18, center(dg(levels))]]) +
        smallline('In the example at ' + m('r_1') + ', the entry part is ' + m(T`{{ba_share_r1_B}}`) + ' of the price gap. Informed-trader share and announcement detail: Backup B13, page 2.') +
        takeaway('Test recruitment in prices first. The sharpest test needs no auction object.') +
        B('main:s18') }, 'main:s18');

    bk({ id: 'b13b', label: 'B13b', title: 'Predictions in full',
      body: vsp(14) +
        ul(['Mean order under full two-sided trade is ' + m(T`\lambda(2\pi-1)`) + '. Counts name informed presence only when the prior is known and differs from ' + m('1/2') + '.',
          'At prior ' + m('1/2') + ', sale impact plus volume name presence when entry sits at its floor after a sale and after no order, with payoff scale ' + m(T`\rho\Delta_T`) + ' known.',
          'For a prepared rival, the winner gap after purchase against sale equals ' + m(T`[M(\pi)-m(\pi)](W_H-W_L)`) + ', with win chance ' + m('W_j') + ' in class ' + m('j') + '. The prediction is strict only when ' + m('W_H>W_L') + '.',
          'A report that reveals preparation alone carries a positive mean price change exactly when preparation stayed uncertain after some order. Both reports together average to zero.',
          'At one middle strength, sale processes can form two clusters: uninformative prices with mean order zero, or informative prices with mean order ' + m(T`\lambda/2`) + '.',
          'Count preparation starts, not public offers alone. Date incumbent strength from public records before the preparation decision.'], 18) +
        B('main:s18') }, 'main:s18');

    bk({ id: 'b13c', label: 'B13c', title: 'Predictions in full', subtitle: 'Weighted price impact and the winner · Proposition A.10',
      body: vsp(21) +
        ul(['Let order frequency be ' + m(T`\bar f(x)=\Pr(X=x)`) + ', purchase impact ' + m('I_+=P(1)-P(0)') + ', and sale impact ' + m('I_-=P(0)-P(-1)') + '. <b>Proposition A.10:</b> under full two-sided trade, class ' + m('H') + ' buys and class ' + m('L') + ' sells with probability one, and prior ' + m(T`\pi<{}`) + 'threshold ' + m(T`\tau`) + ', the weighted difference ' + m(T`\bar f(1)I_+-\bar f(-1)I_-`) + ' is positive exactly when entry after a purchase exceeds the floor, ' + m(T`e(1)>\rho`) + '. At prior ' + m(T`\pi=1/2`) + ' the frequencies agree, and the raw impacts ' + m('I_+') + ' and ' + m('I_-') + ' compare directly. The entry part of the price gap ' + m('P(1)-P(-1)') + ' sits in purchase impact ' + m('I_+') + '.',
          'Under the same full two-sided trade, where entry ' + m(T`e(x)=\rho`) + ' after each order, the order ' + m('X') + ' does not predict entry. It still predicts the winner exactly when the win chance ' + m('W_H') + ' exceeds ' + m('W_L') + ', with ' + m(T`W_j=\mathbb{E}_j[F(\theta)\mathbf{1}\{\theta\ge p\}]`) + ' for a prepared rival of class ' + m('j') + '; the indicator ' + m(T`\mathbf{1}\{\theta\ge p\}`) + ' is one when the value meets the reserve. For a prepared rival, the win-probability gap after a purchase against a sale is ' + m(T`[M(\pi)-m(\pi)](W_H-W_L)`) + '.'], 21) +
        B('main:s18') }, 'main:s18');

    bk({ id: 'b14', label: 'B14', targets: ['app:b14'], title: 'References and the full literature table', subtitle: 'What each strand gives the paper, and what the paper adds',
      body: table({ widths: [240, 430, 360, 340], cls: 'fs-f stretch-105', head: ['Strand', 'Closest work', 'Builds on', 'Adds'], rows: [
          ['Prices guide real decisions', 'Dow, Goldstein and Guembel (2017); Edmans, Goldstein and Jiang (2015); Bond, Edmans and Goldstein (2012); Foucault and Frésard (2014)', 'The price as an information source; real decisions feed back into the incentive to produce information', 'The decision is a rival’s entry, and the sale splits one value between shareholders and that rival'],
          ['Costly entry into auctions', 'Fishman (1988); Hirshleifer and Png (1989); Samuelson (1985); McAfee and McMillan (1987); Levin and Smith (1994); Roberts and Sweeting (2013); Gentry and Stroup (2019)', 'Costly preparation, deterrence and selective entry', 'Pre-entry information that moves with competition'],
          ['Takeover prices and trading', 'Edmans, Goldstein and Jiang (2012); Kyle and Vila (1991); Luo (2005); Betton, Eckbo, Thompson and Thorburn (2014)', 'Target prices shape takeovers; informed orders hide in liquidity trade; bidders learn from prices after a bid', 'An outside informed trader with no stake informs a rival bidder before it prepares']] }) +
        B('main:s3') }, 'main:s3');

    var refs = function (list) { return '<div class="refs2">' + list.map(function (r) { return '<p>' + r + '</p>'; }).join('') + '</div>'; };
    bk({ id: 'b14b', label: 'B14b', cls: 'sz-f', title: 'References and the full literature table',
      body: cols([[0.49, refs(['Admati and Pfleiderer (2009). <em>Rev. Financ. Stud.</em> 22.', 'Betton, Eckbo, Thompson and Thorburn (2014). <em>J. Finance</em> 69.',
            'Bond, Edmans and Goldstein (2012). <em>Annu. Rev. Financ. Econ.</em> 4.', 'Boone and Mulherin (2007). <em>J. Finance</em> 62.', 'Bulow and Klemperer (1996). <em>Amer. Econ. Rev.</em> 86.',
            'Dow and Gorton (1997). <em>J. Finance</em> 52.', 'Dow, Goldstein and Guembel (2017). <em>J. Eur. Econ. Assoc.</em> 15.', 'Edmans, Goldstein and Jiang (2012). <em>J. Finance</em> 67.',
            'Edmans, Goldstein and Jiang (2015). <em>Amer. Econ. Rev.</em> 105.', 'Fishman (1988). <em>RAND J. Econ.</em> 19.', 'Foucault and Frésard (2014). <em>J. Financ. Econ.</em> 111.',
            'Gentry and Stroup (2019). <em>J. Financ. Econ.</em> 132.'])],
          [0.49, refs(['Gorbenko and Malenko (2014). <em>J. Finance</em> 69.', 'Hirshleifer and Png (1989). <em>Rev. Financ. Stud.</em> 2.', 'Kyle and Vila (1991). <em>RAND J. Econ.</em> 22.',
            'Levin and Smith (1994). <em>Amer. Econ. Rev.</em> 84.', 'McAfee and McMillan (1987). <em>Econ. Letters</em> 23.', 'Luo (2005). <em>J. Finance</em> 60.',
            'Roberts and Sweeting (2013). <em>Amer. Econ. Rev.</em> 103.', 'Samuelson (1985). <em>Econ. Letters</em> 17.', 'Schwert (1996). <em>J. Finance</em> 51.'])]]) +
        B('main:s3') }, 'main:s3');

    bk({ id: 'b15', label: 'B15', targets: ['app:b15'], title: 'Continuous order sizes',
      body: vsp(14) +
        ul(['The slot set-up uses unit orders ' + m(T`\{-1,0,1\}`) + ', so every order is on path and no off-path belief enters',
          'A menu of continuous order sizes needs a convention for the sizes that no synergy class uses, as in Edmans, Goldstein and Jiang 2015',
          'Additive liquidity flow also keeps every size on path',
          'With Laplace noise of scale ' + m(T`\xi`) + ' and full unit orders, the top belief equals the slot value ' + m(T`M(\pi)`) + ' when ' + m(T`1+u=\mathrm{e}^{2/\xi}`),
          'The two set-ups then share the belief bounds. They differ in the probability that each synergy class reaches the top belief'], 14) +
        takeaway('Unit orders keep prices on path at every order.') +
        B('main:s7') }, 'main:s7');

    /* ================================================================ notation (B16 and the G panel) */
    /* The rows of the B16 tables of slides.tex: symbol, gloss, first defined. One source feeds the two
       B16 pages and the notation panel. */
    var NOTATION = [
      [[m('R') + ', ' + m('F'), 'incumbent’s value ' + m('R') + '; its distribution ' + m('F') + ', with ' + m(T`R\sim F`) + ' in the general model; in the paper’s example (frames 14–16 and their backups), ' + m('R') + ' is uniform on ' + m('[0,r]'), 'frame 5'],
        [m('j') + ', ' + m(T`\pi`) + ', ' + m(T`\theta`) + ', ' + m('G_j'), 'synergy class ' + m(T`j\in\{H,L\}`) + '; prior ' + m(T`\pi=\Pr(j=H)`) + '; rival’s value ' + m(T`\theta`) + '; class value law ' + m('G_j') + ' for ' + m(T`\theta`) + ' given ' + m('j'), 'frame 5'],
        [m('p'), 'reserve ' + m('p') + ' of the cash second-price auction', 'frame 5'],
        [m('C') + ', ' + m('c_H') + ', ' + m(T`\rho`), 'baseline preparation cost ' + m(T`C\in\{0,c_H\}`) + ' (B11 also allows any fixed independent cost law); high cost ' + m('c_H') + '; entry floor ' + m(T`\rho=\Pr(C=0)\in(0,1)`), 'frame 5'],
        [m('X') + ', ' + m('q') + ', ' + m(T`\lambda`) + ', ' + m(T`\beta`) + ', ' + m('k'), 'slot outcome ' + m('X') + '; the informed trader’s chosen order ' + m('q') + '; presence ' + m(T`\lambda`) + '; liquidity probability ' + m(T`\beta`) + '; order cost ' + m('k'), 'frame 6'],
        [m('P') + ', ' + m('V_T') + ', ' + m(T`\mathbb{E}[\cdot]`), 'stock price ' + m(T`P(X)=\mathbb{E}[V_T\mid X]`) + '; target proceeds per share ' + m('V_T') + '; expectation ' + m(T`\mathbb{E}[\cdot]`), 'frame 6'],
        [m(T`\mu(x)`) + ', ' + m(T`\bar\mu(\bar P)`), 'order belief ' + m(T`\mu(x)=\Pr(j=H\mid X=x)`) + '; belief at a price ' + m(T`\bar\mu(\bar P)=\Pr(j=H\mid P(X)=\bar P)`) + '. The two agree under Lemma A.2, with ' + m(T`\Delta_T>0`) + ', ' + m('g_H>g_L') + ', and ' + m(T`e(x)\ge\rho`), 'frames 7, 9, 11'],
        [m(T`t(\theta)`) + ', ' + m(T`g(\theta)`), 'expected target proceeds ' + m(T`t(\theta)`) + '; gross auction profit ' + m(T`g(\theta)`) + ', at value ' + m(T`\theta\ge p`), 'frame 8'],
        [m('t_j') + ', ' + m('g_j') + ', ' + m('t_0'), 'class means of ' + m(T`t(\theta)`) + ', ' + m(T`g(\theta)`) + ' in class ' + m('j') + '; proceeds with no entry ' + m('t_0=p[1-F(p)]'), 'frame 8'],
        [m(T`\Delta_T`) + ', ' + m(T`B(\mu)`), 'shareholder spread ' + m(T`\Delta_T=t_H-t_L`) + '; rival gross profit ' + m(T`B(\mu)=g_L+\mu(g_H-g_L)`) + ' at belief ' + m(T`\mu`) + ' (before ' + m('C') + ')', 'frame 8'],
        [m('e(x)') + ', ' + m(T`\mathsf{E}`), 'entry after order ' + m('x') + ', ' + m(T`e(x)\ge\rho`) + '; total entry ' + m(T`\mathsf{E}`) + ', the probability that the rival prepares', 'frame 9, B11']],
      [[m('U_j(q)'), 'payoff from order ' + m('q') + '; informed trader sees class ' + m('j'), 'frame 9'],
        [m(T`\tilde F`) + ', ' + m('F_i'), 'strengthening ' + m(T`\tilde F\le F`) + ' in B8; distributions ' + m('F_0') + ', ' + m('F_1') + ', ' + m('F_2') + ' in B1, with ' + m('B_i') + ', ' + m(T`\Delta_i`) + ' at ' + m('F_i'), 'B8, B1'],
        [m('b') + ', ' + m('u') + ', ' + m(T`m(\pi)`) + ', ' + m(T`M(\pi)`), 'liquidity mass ' + m(T`b=(1-\lambda)\beta`) + '; relative informed mass ' + m(T`u=\lambda/b`) + '; band floor ' + m(T`m(\pi)`) + '; top belief ' + m(T`M(\pi)`), 'frame 11, B2'],
        [m(T`\tau`) + ', ' + m(T`\kappa(\pi)`), 'threshold ' + m(T`\tau=(c_H-g_L)/(g_H-g_L)`) + ' when ' + m('g_H>g_L') + '; residual doubt ' + m(T`\kappa(\pi)=\min\{m(\pi),1-M(\pi)\}`), 'frame 12, B1'],
        [m('K_H') + ', ' + m('K_L'), 'gross returns of a purchase in class ' + m('H') + ' and a sale in class ' + m('L') + ', before order cost ' + m('k'), 'frame 12, B2'],
        [m('h') + ', ' + m(T`\ell`) + ', ' + m('r'), 'point-mass values ' + m('h') + ' (class ' + m('H') + ') and ' + m(T`\ell`) + ' (class ' + m('L') + '); strength ' + m('r') + ' with ' + m('R') + ' uniform on ' + m('[0,r]'), 'frame 14'],
        [m('S') + ', ' + m(T`\mu(S)`), 'fixed signal ' + m('S') + '; signal belief ' + m(T`\mu(S)=\Pr(j=H\mid S)`), 'frame 15, B11'],
        [m('a') + ', ' + m(T`\bar\lambda`) + ', ' + m(T`\lambda_R`) + ', ' + m(T`M_\lambda`) + ', ' + m(T`m_\lambda`), 'research cost coefficient ' + m('a>0') + ' in ' + m(T`(a/2)\lambda^2`) + '; research cap ' + m(T`\bar\lambda\in(0,1)`) + '; interior research ' + m(T`\lambda_R(\Delta_T)`) + '; top belief ' + m(T`M_\lambda`) + ' and band floor ' + m(T`m_\lambda`) + ' at presence ' + m(T`\lambda`), 'frame 16, B12'],
        [m(T`\bar f(x)`) + ', ' + m('I_+') + ', ' + m('I_-') + ', ' + m('W_j'), 'order frequency ' + m(T`\bar f(x)=\Pr(X=x)`) + '; purchase impact ' + m('I_+=P(1)-P(0)') + '; sale-order impact ' + m('I_-=P(0)-P(-1)') + '; win chance ' + m('W_j') + ' of a prepared class-' + m('j') + ' rival', 'frame 18, B13'],
        [m(T`\sigma_j`) + ', ' + m(T`\eta`) + ', ' + m('f_j(x)') + ', ' + m(T`\zeta`), 'order distribution ' + m(T`\sigma_j`) + '; liquidity probabilities ' + m(T`\eta`) + '; order probability ' + m('f_j(x)') + ' in class ' + m('j') + '; high-cost preparation probability ' + m(T`\zeta`) + ' at a price', 'B9'],
        [m('e_H') + ', ' + m('e_L') + ', ' + m('W_j(F)'), 'entry in class ' + m('H') + ', class ' + m('L') + '; win chance ' + m(T`W_j(F)=\mathbb{E}_j[F(\theta)\mathbf{1}\{\theta\ge p\}]`) + ' against distribution ' + m('F'), 'frame 16, B1, B13']]
    ];
    var notationTable = function (rows) { return table({ widths: [270, 960, 200], cls: 'fs-f notation-table', head: ['Symbol', 'Gloss', 'First defined'], rows: rows }); };
    bk({ id: 'b16', label: 'B16', targets: ['app:b16'], title: 'Notation', body: notationTable(NOTATION[0]) + B('main:s5') }, 'main:s5');
    bk({ id: 'b16b', label: 'B16b', title: 'Notation', body: notationTable(NOTATION[1]) + B('main:s5') }, 'main:s5');

    return { frames: F, notation: NOTATION };
  }

  if (typeof window !== 'undefined') window.createDeck = createDeck;
})();
