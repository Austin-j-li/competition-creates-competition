/* deck.js: the slide engine of the /talk/ page.
 *
 * The 47 slides are pre-rendered sections in the page (build.py, render.mjs). This script scales
 * the 1600 x 900 stage, steps through reveals ([data-step]), follows the backup links of
 * talk.tex (a goto button jumps to a \hypertarget; Back returns to the frame and step it came
 * from), and opens the overview, the speaker notes and the notation. Widgets draw figures with
 * handout/charts.js from window.CCC_DATA and the closed forms in handout/explorer.js; none
 * solves an equilibrium.
 * Keys: Right, Space, PageDown next; Left, PageUp previous; Home, End; O overview; N notes;
 * G notation; T theme; F fullscreen; R reset the slide; Escape back from a backup or close.
 * ES2019, no modules, no network. Exposes window.DECK for inspection.
 */
(function () {
  'use strict';
  var CCC = (window.CCC = window.CCC || {});
  var errors = [];
  window.addEventListener('error', function (e) { errors.push(String(e.message)); });
  window.addEventListener('unhandledrejection', function (e) { errors.push(String(e.reason)); });
  var doc = document.documentElement, D = window.CCC_DATA, META = window.CCC_DECK || {}, NOTES = window.CCC_NOTES || {};
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) { /* private mode */ } }
  };

  var slides = $$('.slide');
  var ids = slides.map(function (s) { return s.id; });
  var targetOf = {};
  slides.forEach(function (s) { (s.dataset.targets || '').split(' ').forEach(function (t) { if (t) targetOf[t] = s.id; }); });
  var mainCount = slides.filter(function (s) { return s.dataset.backup !== 'true'; }).length;
  var index = 0, step = 0, steps = {}, returns = [];
  var widgets = {};

  /* ---------- stage ---------- */
  function scale() {
    var stage = $('#stage');
    var s = Math.max(0.1, Math.min(stage.clientWidth / 1600, stage.clientHeight / 900));
    doc.style.setProperty('--stage-scale', String(s));
    return s;
  }
  addEventListener('resize', scale);

  /* ---------- theme ---------- */
  function setTheme(t) {
    doc.dataset.theme = t === 'dark' ? 'dark' : 'light';
    var b = $('#theme');
    b.textContent = doc.dataset.theme === 'dark' ? 'Light' : 'Dark';
    b.setAttribute('aria-pressed', String(doc.dataset.theme === 'dark'));
    store.set('ccc-theme', doc.dataset.theme);
    renderWidget(true);
  }

  /* ---------- reveals and navigation ---------- */
  function maxStep(i) {
    var s = slides[i === undefined ? index : i];
    return $$('[data-step]', s).reduce(function (a, e) { return Math.max(a, Number(e.dataset.step) || 0); }, 0);
  }
  function update() {
    var s = slides[index], backup = s.dataset.backup === 'true';
    $$('[data-step]', s).forEach(function (e) {
      var on = Number(e.dataset.step) <= step;
      e.classList.toggle('shown', on);
      e.setAttribute('aria-hidden', String(!on));
    });
    steps[index] = step;
    var num = s.dataset.num;
    if (!backup) s.style.setProperty('--progress', (100 * Number(num) / 16).toFixed(1) + '%');
    $('#counter').textContent = backup ? num : (num === '0' ? 'title' : num + ' / 16');
    var ms = maxStep();
    $('#progress-label').textContent = ms ? 'step ' + (step + 1) + ' of ' + (ms + 1) : (backup ? 'backup' : '');
    $('#previous').disabled = index === 0 && step === 0;
    $('#next').disabled = step === ms && (index === slides.length - 1 || (!backup && index === mainCount - 1));
    $('#return').hidden = !backup;
    $$('#rail li').forEach(function (li) {
      var part = li.dataset.part, cur = s.dataset.part;
      li.classList.toggle('current', part === cur);
      li.classList.toggle('done', !backup && part !== 'B' && Number(part) < Number(cur));
    });
    var w = widgets[s.dataset.widget];
    if (w && w.step) { try { w.step(s, step); } catch (e) { errors.push(s.id + ': ' + e.message); } }
  }
  function go(i, opts) {
    opts = opts || {};
    if (typeof i === 'string') i = ids.indexOf(i);
    if (i < 0 || i >= slides.length) return;
    index = i;
    var ms = maxStep(i);
    step = opts.step === 'last' ? ms : Math.max(0, Math.min(ms, opts.step !== undefined ? opts.step : (steps[i] || 0)));
    slides.forEach(function (s, j) { var on = j === i; s.classList.toggle('active', on); s.setAttribute('aria-hidden', String(!on)); s.inert = !on; });
    update();
    renderWidget(false);
    if (!opts.keepHash) { try { history.replaceState(null, '', '#' + slides[i].id); } catch (e) { /* file URL */ } }
    var s = slides[i];
    $('#announcer').textContent = (s.dataset.backup === 'true' ? 'Backup ' : 'Slide ') + s.dataset.num + ': ' + s.dataset.title;
  }
  function next() {
    if (step < maxStep()) { step++; update(); return; }
    var backup = slides[index].dataset.backup === 'true';
    if (!backup && index === mainCount - 1) return;
    if (index < slides.length - 1) go(index + 1, { step: 0 });
  }
  function previous() {
    if (step > 0) { step--; update(); return; }
    var backup = slides[index].dataset.backup === 'true';
    if (backup && index === mainCount) return;
    if (index > 0) go(index - 1, { step: 'last' });
  }
  /* A goto button jumps to a \hypertarget and remembers where it came from. */
  function follow(target) {
    var id = targetOf[target];
    if (!id) { errors.push('unknown link target ' + target); return; }
    returns.push({ index: index, step: step });
    go(id, { step: 0 });
  }
  /* Back returns to the place the link was followed from; without one, to the link's target. */
  function back(target) {
    if (returns.length) { var r = returns.pop(); go(r.index, { step: r.step }); return; }
    var id = target ? targetOf[target] : null;
    if (!id) {
      var s = slides[index], b = $('.goto.back', s);
      id = b ? targetOf[b.dataset.back] : (s.dataset.origin || null);
    }
    if (id) go(id, { step: 'last' });
  }
  function reset() {
    step = 0;
    var s = slides[index], w = widgets[s.dataset.widget];
    if (w && w.reset) w.reset(s);
    update();
    renderWidget(true);
  }

  /* ---------- panels ---------- */
  function panel(title, html) {
    $('#panel-title').textContent = title;
    $('#panel-body').innerHTML = html;
    renderTex($('#panel-body'));
    var dlg = $('#panel');
    if (!dlg.open) dlg.showModal();
  }
  function closePanel() { var d = $('#panel'); if (d.open) d.close(); $('#stage').focus({ preventScroll: true }); }
  function partName(p) { var x = (META.parts || []).filter(function (q) { return String(q.n) === String(p); })[0]; return x ? x.name : ''; }
  function overview() {
    var html = '<p class="notes-meta">All 47 frames of the Beamer deck in their order. F10a and F10b share number 10; backups A1 to A29 follow the conclusion.</p>';
    (META.parts || []).forEach(function (p) {
      var items = (META.frames || []).filter(function (f) { return String(f.part) === String(p.n); });
      if (!items.length) return;
      html += '<section class="overview-part"><h3>' + esc(p.n === 'B' ? 'Backups' : p.n + ' · ' + p.name) + '</h3><div class="overview-grid">';
      items.forEach(function (f) {
        var cur = slides[index].id === f.id;
        html += '<button type="button" class="ov' + (f.backup ? ' backup' : '') + (cur ? ' current' : '') + '" data-jump="' + esc(f.id) + '"' + (cur ? ' aria-current="true"' : '') + '><small>' + esc(f.label) + (f.backup ? ' · from ' + esc(f.origin.toUpperCase()) : '') + '</small>' + esc(f.title) + '</button>';
      });
      html += '</div></section>';
    });
    panel('Overview', html);
  }
  function notes() {
    var s = slides[index], n = NOTES[s.dataset.label] || {};
    panel('Speaker notes · ' + s.dataset.label,
      '<p class="notes-meta">' + esc(n.timing || '') + (s.dataset.backup === 'true' ? '' : ' · planned ' + esc(s.dataset.minutes) + ' min') + '</p>' +
      '<h3>' + esc(s.dataset.title) + '</h3><div class="notes-body">' + (n.html || '<p>No notes.</p>') + '</div>' +
      '<p class="notes-meta">Source: ' + esc(n.source || '') + '</p>' +
      (s.dataset.backup === 'true' ? '' : '<p class="notes-meta">' + esc(META.checkpoints || '') + '</p>'));
  }
  function notationTable() {
    var rows = [];
    (META.notation || []).forEach(function (col) { col.forEach(function (r) { rows.push(r); }); });
    return '<table><tbody>' + rows.map(function (r) { return '<tr><td>' + r[0] + '</td><td>' + r[1] + '</td></tr>'; }).join('') + '</tbody></table>';
  }
  function notation() { panel('Notation', '<div class="panel-notation">' + notationTable() + '</div>'); }
  function help() {
    panel('Controls', '<div class="help">' +
      '<span><kbd>→</kbd> <kbd>Space</kbd></span><span>next step, then the next slide</span>' +
      '<span><kbd>←</kbd></span><span>previous step or slide</span>' +
      '<span><kbd>Home</kbd> <kbd>End</kbd></span><span>title, conclusion</span>' +
      '<span><kbd>O</kbd></span><span>overview of all 47 frames</span>' +
      '<span><kbd>N</kbd></span><span>speaker notes</span>' +
      '<span><kbd>G</kbd></span><span>notation</span>' +
      '<span><kbd>T</kbd></span><span>dark or light theme</span>' +
      '<span><kbd>F</kbd></span><span>fullscreen</span>' +
      '<span><kbd>R</kbd></span><span>reset the slide</span>' +
      '<span><kbd>Esc</kbd></span><span>back from a backup slide, or close a panel</span></div>' +
      '<p class="notes-meta">Numbers carry their registry key, status and source on hover. Figures read the paper\'s figure data; slider readouts evaluate closed forms and solve no equilibrium.</p>');
  }
  function fullscreen() {
    try { if (document.fullscreenElement) document.exitFullscreen(); else doc.requestFullscreen(); }
    catch (e) { /* not available */ }
  }

  /* ---------- mathematics in notes and panels ---------- */
  function renderTex(root) {
    $$('.tex[data-tex]', root).forEach(function (el) {
      if (el.dataset.done) return;
      try { katex.render(el.dataset.tex, el, { throwOnError: false }); el.dataset.done = '1'; }
      catch (e) { el.textContent = el.dataset.tex; }
    });
  }

  /* ---------- charts ---------- */
  function tokens() { return CCC.charts.tokens(); }
  function P() { return CCC.explorer.closedForms ? readInputs() : null; }
  function readInputs() {
    var o = {};
    Object.keys(D.inputs).forEach(function (k) { o[k] = Number(D.inputs[k]); });
    return o;
  }
  function vline(x, color, dash) {
    return { type: 'line', xref: 'x', yref: 'y domain', x0: x, x1: x, y0: 0, y1: 1, line: { color: color, width: 1, dash: dash || 'dot' }, layer: 'below' };
  }
  function label(x, text, color, yref, side) {
    return { text: text, xref: 'x', x: x, yref: yref || 'y domain', y: 1, yanchor: 'bottom', xanchor: side || 'center', yshift: 3, font: { size: 15, color: color } };
  }
  /* X1: the target-payoff spread and challenger profit at the prior against strength. */
  function specX1(t) {
    var F = D.fig1, half = F.mu.filter(function (m) { return Number(m) === 0.5; })[0];
    var inp = readInputs();
    var cd = F.r.map(function (_, i) { return [F.Delta_T[i]]; }), cdB = F.r.map(function (_, i) { return [F.B[half][i]]; });
    var traces = [
      { mode: 'lines', name: 'target-payoff spread Δ<sub>T</sub>', x: F.r, y: F.Delta_T, customdata: cd, line: { color: t.info, width: 3 }, xaxis: 'x', yaxis: 'y',
        hovertemplate: 'Δ<sub>T</sub> = %{customdata[0]}<extra>figure data</extra>' },
      { mode: 'lines', name: 'challenger profit at the prior B<sub>r</sub>(1/2)', x: F.r, y: F.B[half], customdata: cdB, line: { color: t.ink, width: 3 }, xaxis: 'x2', yaxis: 'y2',
        hovertemplate: 'B<sub>r</sub>(1/2) = %{customdata[0]}<extra>figure data</extra>' }
    ];
    var layout = { height: 330, margin: { l: 70, r: 20, t: 40, b: 56 }, shapes: [], annotations: [],
      xaxis: { domain: [0, 0.45], anchor: 'y', range: [1, 3.8], dtick: 0.5, tick0: 1, title: { text: 'incumbent strength <i>r</i>' } },
      yaxis: { domain: [0, 1], anchor: 'x', range: [0, 1.1], title: { text: 'target-payoff spread Δ<sub><i>T</i></sub>' } },
      xaxis2: { domain: [0.57, 1], anchor: 'y2', range: [1, 3.8], dtick: 0.5, tick0: 1, title: { text: 'incumbent strength <i>r</i>' } },
      yaxis2: { domain: [0, 1], anchor: 'x2', range: [3.8, 5.2], title: { text: 'profit at the prior <i>B<sub>r</sub></i>(1/2)' } } };
    [['x', 'y'], ['x2', 'y2']].forEach(function (k, j) {
      [[inp.r_weak, 'weak <i>r</i><sub>0</sub> = ' + D.inputs.r_weak], [inp.r_strong, 'strong <i>r</i><sub>1</sub> = ' + D.inputs.r_strong]].forEach(function (m) {
        layout.shapes.push({ type: 'line', xref: k[0], yref: k[1] + ' domain', x0: m[0], x1: m[0], y0: 0, y1: 1, line: { color: t.muted, width: 1.2, dash: 'dot' }, layer: 'below' });
        layout.annotations.push({ text: m[1], xref: k[0], x: m[0], yref: k[1] + ' domain', y: 1, yanchor: 'bottom', yshift: 4, font: { size: 15, color: t.muted } });
      });
      layout.annotations.push({ text: j ? '(b)' : '(a)', panel: true, xref: k[0] + ' domain', yref: k[1] + ' domain', x: 0, y: 1, xanchor: 'left', yanchor: 'bottom', xshift: -62, yshift: 4, font: { size: 16, color: t.ink } });
    });
    return { traces: traces, layout: layout };
  }
  /* X2: profit at the worst, prior and best belief, with the two cost lines and a strength marker. */
  function specX2(t, r) {
    var F = D.fig1, inp = readInputs();
    var mus = F.mu.slice().sort(function (a, b) { return Number(b) - Number(a); });
    var names = ['best price <i>M</i>', 'prior 1/2', 'worst price <i>m</i>'], dashes = ['solid', 'dash', 'dot'];
    var traces = mus.map(function (mu, j) {
      return { mode: 'lines', name: 'B<sub>r</sub>(' + F.mu_label[mu] + '), ' + names[j].replace(/<[^>]+>/g, ''), x: F.r, y: F.B[mu], customdata: F.r.map(function (_, i) { return [F.B[mu][i]]; }),
        line: { color: j === 2 ? t.c3 : t.ink, width: 2.6, dash: dashes[j] }, xaxis: 'x', yaxis: 'y', hovertemplate: 'B<sub>r</sub>(' + F.mu_label[mu] + ') = %{customdata[0]}<extra>figure data</extra>' };
    });
    var c = CCC.explorer.closedForms(inp, r);
    traces.push({ mode: 'markers', name: 'closed forms at the slider', showlegend: false, x: [r, r, r], y: [c.B_M, c.B_prior, c.B_m],
      marker: { symbol: 'circle', size: 11, color: t.accent, line: { width: 2, color: t.bg } }, hovertemplate: 'skip' });
    var layout = { height: 300, margin: { l: 64, r: 16, t: 34, b: 52 }, shapes: [], annotations: [],
      xaxis: { domain: [0, 1], anchor: 'y', range: [1, 3.8], dtick: 0.5, tick0: 1, title: { text: 'incumbent strength <i>r</i>' } },
      yaxis: { domain: [0, 1], anchor: 'x', range: [0.5, 7.5], dtick: 1, tick0: 1, title: { text: 'expected gross profit <i>B<sub>r</sub></i>(μ)' } } };
    [[inp.c_H, 'expensive cost <i>c<sub>H</sub></i> = ' + D.inputs.c_H, 'solid'], [inp.c_L, 'cheap cost <i>c<sub>L</sub></i> = ' + D.inputs.c_L, 'dash']].forEach(function (cst) {
      layout.shapes.push({ type: 'line', xref: 'x domain', yref: 'y', x0: 0, x1: 1, y0: cst[0], y1: cst[0], line: { color: t.cost, width: 2, dash: cst[2] }, layer: 'below' });
      layout.annotations.push({ text: cst[1], xref: 'x domain', x: 0, xanchor: 'left', xshift: 8, yref: 'y', y: cst[0], yanchor: 'bottom', yshift: 3, bgcolor: t.bg, font: { size: 15, color: t.cost } });
    });
    [[inp.r_weak, 'weak <i>r</i><sub>0</sub>'], [inp.r_strong, 'strong <i>r</i><sub>1</sub>'], [inp.r_collapse, 'stronger still <i>r</i><sub>2</sub>']].forEach(function (mk) {
      layout.shapes.push(vline(mk[0], t.muted));
      layout.annotations.push(label(mk[0], mk[1], t.muted));
    });
    layout.shapes.push({ type: 'line', xref: 'x', yref: 'y domain', x0: r, x1: r, y0: 0, y1: 1, line: { color: t.accent, width: 2 } });
    var iL = F.r.length - 1;
    mus.forEach(function (mu, j) {
      layout.annotations.push({ text: names[j], xref: 'x', x: Number(F.r[iL]), xanchor: 'right', yref: 'y', y: Number(F.B[mu][iL]), yanchor: 'bottom', yshift: 4, bgcolor: t.bg, font: { size: 14, color: t.muted } });
    });
    return { traces: traces, layout: layout, closed: c };
  }
  /* One panel of Figure 2 (Figure X5 of the talk), keeping every display rule of the builder. */
  function specX5(t, which) {
    var full = CCC.charts.builders.fig2(D, t, { narrow: false });
    var L = full.layout, keepX = which === 'a' ? 'x' : 'x2', keepY = which === 'a' ? 'y' : 'y2';
    var traces = full.traces.filter(function (tr) { return (tr.xaxis || 'x') === keepX; }).map(function (tr) {
      var o = {}; Object.keys(tr).forEach(function (k) { o[k] = tr[k]; });
      o.xaxis = 'x'; o.yaxis = 'y';
      if (which === 'b' && tr.showlegend === false && tr.legendgroup && !/mixed supports/.test(tr.name)) o.showlegend = true;
      return o;
    });
    var xa = {}, ya = {};
    Object.keys(L[keepX === 'x' ? 'xaxis2' : 'xaxis2']).forEach(function (k) { xa[k] = L.xaxis2[k]; });
    xa.domain = [0, 1]; xa.anchor = 'y'; delete xa.matches;
    Object.keys(L[keepY === 'y' ? 'yaxis' : 'yaxis2']).forEach(function (k) { ya[k] = L[keepY === 'y' ? 'yaxis' : 'yaxis2'][k]; });
    ya.domain = [0, 1]; ya.anchor = 'x';
    var shapes = L.shapes.filter(function (s) { return s.yref === 'paper' || s.yref === keepY + ' domain'; }).map(function (s) {
      var o = {}; Object.keys(s).forEach(function (k) { o[k] = s[k]; }); if (o.yref === keepY + ' domain') o.yref = 'y domain'; return o;
    });
    var anns = L.annotations.filter(function (a) { return !a.panel && (a.yref === 'y domain'); });
    return { traces: traces, layout: { height: 360, margin: { l: 64, r: 20, t: 36, b: 56 }, xaxis: xa, yaxis: ya, shapes: shapes, annotations: anns } };
  }
  function bigger(spec, height) {
    spec.layout.height = height;
    spec.layout.margin = { l: 70, r: 20, t: 40, b: 60 };
    return spec;
  }
  var chartState = {};
  function drawChart(el, spec, key) {
    var st = chartState[key] || (chartState[key] = { hidden: {} });
    st.width = 0;
    st.zoom = 1.4; // slides are read from a distance: draw narrow and scale up
    CCC.charts.draw(el, spec, tokens(), st);
    el.setAttribute('data-mounted', 'true');
    return st;
  }

  /* ---------- widgets ---------- */
  var INFOSETS = {
    seller: 'Seller: commits to the sale rule, a cash second-price auction with reserve p, before any trading. The rule is public.',
    investor: 'Investor: knows the challenger\'s value θ. Trades the target\'s stock against noise traders; has no control rights and cannot bid.',
    makers: 'Market makers: see only total order flow, not who traded. Price the share at expected sale proceeds, which anticipates entry.',
    challenger: 'Challenger: sees the stock price and its own cost C, never the order flow, θ or R. Paying C reveals θ and permits a bid.',
    bidders: 'Bidders: the incumbent knows its value R ~ U[0, r], and r is public. A prepared challenger knows θ. Both bid truthfully.'
  };
  widgets.infosets = {
    render: function (s) {
      $$('.tl', s).forEach(function (b) {
        b.setAttribute('aria-pressed', 'false');
        b.onclick = b.onfocus = b.onmouseenter = function () {
          $$('.tl', s).forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
          $('#f4-infoset').textContent = INFOSETS[b.dataset.info];
        };
      });
    }
  };
  widgets.cases = {
    render: function (s) {
      $$('.segmented button', s).forEach(function (b) {
        b.onclick = function () {
          var on = b.getAttribute('aria-pressed') !== 'true';
          $$('.segmented button', s).forEach(function (x) { x.setAttribute('aria-pressed', String(on && x === b)); });
          $$('tr[data-row]', s).forEach(function (tr) { tr.classList.toggle('hl', on && tr.dataset.row === b.dataset.case); });
        };
      });
    },
    reset: function (s) { $$('.segmented button', s).forEach(function (x) { x.setAttribute('aria-pressed', 'false'); }); $$('tr.hl', s).forEach(function (tr) { tr.classList.remove('hl'); }); }
  };
  widgets.x1 = { render: function (s) { drawChart($('#x1', s), specX1(tokens()), 'x1'); } };
  var x2r = null;
  widgets.x2 = {
    render: function (s) {
      var input = $('#x2-r', s), inp = readInputs();
      if (x2r === null) x2r = inp.r_strong;
      input.value = String(x2r);
      input.oninput = function () { x2r = Number(input.value); widgets.x2.draw(s); };
      widgets.x2.draw(s);
    },
    draw: function (s) {
      var spec = specX2(tokens(), x2r), c = spec.closed, inp = readInputs();
      drawChart($('#x2', s), spec, 'x2');
      $('#x2-r-value', s).textContent = x2r.toFixed(2);
      var f = function (x) { return x.toFixed(3); };
      var chip = function (ok, text, margin) { return '<span class="chip ' + (ok ? 'ok' : 'no') + '">' + text + ' ' + (ok ? 'holds' : 'fails') + ' (' + (margin >= 0 ? '+' : '−') + Math.abs(margin).toFixed(3) + ')</span>'; };
      $('#x2-readout', s).innerHTML = '<p>At <i>r</i> = <b>' + x2r.toFixed(2) + '</b>: B<sub>r</sub>(M) = <b>' + f(c.B_M) + '</b>, B<sub>r</sub>(1/2) = <b>' + f(c.B_prior) + '</b>, B<sub>r</sub>(m) = <b>' + f(c.B_m) + '</b></p>' +
        '<p>' + chip(inp.c_L < c.B_m, 'cheap entry after any price', c.B_m - inp.c_L) + chip(c.B_M > inp.c_H, 'expensive entry after the best price', c.B_M - inp.c_H) + '</p>' +
        '<p class="note">Closed forms at the declared inputs with only r moving: a fixed-order calculation, not an equilibrium solver.</p>';
    },
    reset: function () { x2r = readInputs().r_strong; }
  };
  widgets.controls = {
    render: function (s) {
      var pick = function (row) {
        $$('.segmented button', s).forEach(function (x) { x.setAttribute('aria-pressed', String(x.dataset.row === row)); });
        $$('tr[data-row]', s).forEach(function (tr) { tr.classList.toggle('hl', tr.dataset.row === row); });
        var tr = $('tr[data-row="' + row + '"]', s), vals = $$('td .q', tr).map(function (q) { return q.dataset.shown; });
        var status = $('.status', tr) ? $('.status', tr).innerHTML : '';
        var bar = function (lab, v) { return '<div class="bar-row"><span>' + lab + '</span><div class="bar' + (row === 'eq' ? ' info' : '') + '" style="transform:scaleX(' + Number(v) + ')"></div><span class="num">' + v + '</span></div>'; };
        $('#f11-bars', s).innerHTML = '<p class="small">Entry</p>' + bar('<i>r</i><sub>0</sub>', vals[0]) + bar('<i>r</i><sub>1</sub>', vals[1]) + '<span class="status">' + status + '</span>';
      };
      $$('.segmented button', s).forEach(function (b) { b.onclick = function () { pick(b.dataset.row); }; });
      pick(($('.segmented button[aria-pressed="true"]', s) || {}).dataset ? $('.segmented button[aria-pressed="true"]', s).dataset.row : 'eq');
    },
    reset: function (s) { $$('.segmented button', s).forEach(function (x) { x.setAttribute('aria-pressed', String(x.dataset.row === 'eq')); }); }
  };
  widgets.access = {
    render: function (s) {
      $$('.segmented button', s).forEach(function (b) {
        b.onclick = function () {
          var on = b.getAttribute('aria-pressed') !== 'true';
          $$('.segmented button', s).forEach(function (x) { x.setAttribute('aria-pressed', String(on && x === b)); });
          $$('[data-col]', $('table', s)).forEach(function (c) { c.classList.toggle('hl', on && c.dataset.col === b.dataset.col); });
        };
      });
    },
    reset: function (s) { $$('.segmented button', s).forEach(function (x) { x.setAttribute('aria-pressed', 'false'); }); $$('.hl', s).forEach(function (c) { c.classList.remove('hl'); }); }
  };
  widgets.x3 = { render: function (s) { drawChart($('#x3', s), bigger(CCC.charts.builders.fig3(D, tokens(), { narrow: false }), 300), 'x3'); } };
  widgets.x4 = { render: function (s) { drawChart($('#x4', s), bigger(CCC.charts.builders.fig4(D, tokens(), { narrow: false }), 330), 'x4'); } };
  widgets.x5a = { render: function (s) { drawChart($('#x5a', s), specX5(tokens(), 'a'), 'x5a'); } };
  widgets.x5b = { render: function (s) { drawChart($('#x5b', s), specX5(tokens(), 'b'), 'x5b'); } };
  widgets.notation = {
    render: function (s) {
      var host = $('#notation-table', s);
      if (host.dataset.done) return;
      host.innerHTML = (META.notation || []).map(function (col) {
        return '<table><thead><tr><th>Symbol</th><th>Meaning</th></tr></thead><tbody>' + col.map(function (r) { return '<tr><td>' + r[0] + '</td><td>' + r[1] + '</td></tr>'; }).join('') + '</tbody></table>';
      }).join('');
      host.dataset.done = '1';
    }
  };
  widgets.columns = {
    render: function (s) {
      $$('[data-col]', s).forEach(function (c) {
        c.onmouseenter = function () { $$('[data-col]', s).forEach(function (x) { x.style.opacity = x.dataset.col === c.dataset.col ? '1' : '0.4'; }); };
        c.onmouseleave = function () { $$('[data-col]', s).forEach(function (x) { x.style.opacity = ''; }); };
      });
    }
  };

  function renderWidget(force) {
    var s = slides[index], w = widgets[s.dataset.widget];
    if (!w || !w.render) return;
    if (!force && s.dataset.rendered === '1' && !/^x/.test(s.dataset.widget)) return;
    try { w.render(s); s.dataset.rendered = '1'; } catch (e) { errors.push(s.id + ': ' + e.message); }
  }

  /* Disclosures inside slides: the arithmetic line of F7 and the signal-grid line of F13. */
  document.addEventListener('click', function (e) {
    var tg = e.target.closest && e.target.closest('[data-toggle]');
    if (tg) {
      var t = document.getElementById(tg.dataset.toggle), open = tg.getAttribute('aria-expanded') !== 'true';
      tg.setAttribute('aria-expanded', String(open)); if (t) t.hidden = !open;
      return;
    }
    var gt = e.target.closest && e.target.closest('.goto[data-target]');
    if (gt) { follow(gt.dataset.target); return; }
    var bk = e.target.closest && e.target.closest('.goto[data-back]');
    if (bk) { back(bk.dataset.back); return; }
    var jump = e.target.closest && e.target.closest('[data-jump]');
    if (jump) { closePanel(); returns = []; go(jump.dataset.jump, { step: 0 }); return; }
    var railBtn = e.target.closest && e.target.closest('#rail button');
    if (railBtn) { var first = slides.filter(function (s) { return s.dataset.part === railBtn.dataset.part; })[0]; if (first) { returns = []; go(first.id, { step: 0 }); } }
  });
  $('#previous').onclick = previous;
  $('#next').onclick = next;
  $('#return').onclick = function () { back(); };
  $('#overview').onclick = overview;
  $('#notes').onclick = notes;
  $('#notation').onclick = notation;
  $('#help').onclick = help;
  $('#fullscreen').onclick = fullscreen;
  $('#theme').onclick = function () { setTheme(doc.dataset.theme === 'dark' ? 'light' : 'dark'); };
  $('#close-panel').onclick = closePanel;
  $('#panel').addEventListener('click', function (e) { if (e.target === $('#panel')) closePanel(); });
  document.addEventListener('keydown', function (e) {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    if ($('#panel').open) { if (e.key === 'Escape') { e.preventDefault(); closePanel(); } return; }
    var tag = e.target && e.target.tagName;
    if (tag === 'INPUT' && (e.key === 'ArrowLeft' || e.key === 'ArrowRight')) return;
    if ((tag === 'BUTTON' || tag === 'A') && (e.key === ' ' || e.key === 'Enter')) return;
    if (e.target.closest && e.target.closest('.figure') && (e.key === 'ArrowLeft' || e.key === 'ArrowRight')) return;
    var k = e.key.length === 1 ? e.key.toLowerCase() : e.key;
    var map = {
      ArrowRight: next, PageDown: next, ' ': next, ArrowLeft: previous, PageUp: previous,
      Home: function () { returns = []; go(0, { step: 0 }); }, End: function () { returns = []; go(mainCount - 1, { step: 0 }); },
      o: overview, n: notes, g: notation, t: function () { setTheme(doc.dataset.theme === 'dark' ? 'light' : 'dark'); },
      f: fullscreen, r: reset, '?': help, Escape: function () { if (slides[index].dataset.backup === 'true') back(); }
    };
    if (map[k]) { e.preventDefault(); map[k](); }
  });

  /* ---------- rail and start ---------- */
  $('#rail').innerHTML = (META.parts || []).map(function (p) {
    return '<li data-part="' + esc(p.n) + '"><button type="button" data-part="' + esc(p.n) + '">' + esc(p.name) + '</button></li>';
  }).join('');
  scale();
  setTheme(doc.dataset.theme);
  addEventListener('hashchange', function () {
    var h = location.hash.slice(1);
    if (ids.indexOf(h) >= 0 && h !== slides[index].id) { returns = []; go(h, { step: 0, keepHash: true }); }
  });
  var start = location.hash.slice(1);
  go(ids.indexOf(start) >= 0 ? start : 0, { step: 0, keepHash: true });
  window.DECK = {
    go: go, next: next, previous: previous, back: back, follow: follow, reset: reset, setTheme: setTheme,
    slides: function () { return slides.map(function (s) { return s.id; }); },
    selfCheck: function () {
      return { errors: errors.slice(), slides: slides.length, active: slides[index].id, step: step, theme: doc.dataset.theme, scale: scale(),
        mathErrors: $$('.katex-error, .math-error').length, numbers: $$('.q').length };
    },
    /* Walk every slide with all reveals shown; list bodies that overflow the 1600 x 900 stage. */
    audit: function () {
      var out = [], keep = { index: index, step: step };
      slides.forEach(function (s, i) {
        go(i, { step: 'last', keepHash: true });
        var body = $('.slide-body', s) || s;
        if (body.scrollHeight > body.clientHeight + 2 || body.scrollWidth > body.clientWidth + 2) out.push({ id: s.id, over: body.scrollHeight - body.clientHeight, wide: body.scrollWidth - body.clientWidth });
      });
      go(keep.index, { step: keep.step, keepHash: true });
      return out;
    }
  };
})();
