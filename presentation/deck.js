/* deck.js: the slide engine of the /talk/ page.
 *
 * The slides are pre-rendered sections in the page (build.py, render.mjs). This script scales
 * the 1600 x 900 stage, steps through reveals ([data-step]), follows the backup links of
 * slides.tex (a goto button jumps to a \hypertarget; Back returns to the frame and step it came
 * from), and opens the overview, the speaker notes and the notation. Widgets draw figures with
 * CCC.charts.draw (presentation/charts.js) from the curves in window.CCC_DATA.fig, which build.py
 * computes from the closed forms of the paper (presentation/figdata.py); a widget reads those
 * curves and solves nothing.
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
  var TOTAL = META.total || 20;
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
    if (!backup) s.style.setProperty('--progress', (100 * Number(num) / TOTAL).toFixed(1) + '%');
    $('#counter').textContent = backup ? num : (num === '0' ? 'title' : num + ' / ' + TOTAL);
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
    var html = '<p class="notes-meta">All ' + slides.length + ' frames of the Beamer deck in their order: the title, slides 1 to ' + TOTAL + ', then the backups A1 to A' + (slides.length - mainCount) + '.</p>';
    var numOf = {};
    (META.frames || []).forEach(function (f) { numOf[f.id] = f.num; });
    (META.parts || []).forEach(function (p) {
      var items = (META.frames || []).filter(function (f) { return String(f.part) === String(p.n); });
      if (!items.length) return;
      html += '<section class="overview-part"><h3>' + esc(p.n === 'B' ? 'Backups' : p.n + ' · ' + p.name) + '</h3><div class="overview-grid">';
      items.forEach(function (f) {
        var cur = slides[index].id === f.id;
        html += '<button type="button" class="ov' + (f.backup ? ' backup' : '') + (cur ? ' current' : '') + '" data-jump="' + esc(f.id) + '"' + (cur ? ' aria-current="true"' : '') + '><small>' + (f.backup ? esc(f.label) + ' · from slide ' + esc(numOf[f.origin]) : f.num === '0' ? 'title' : 'slide ' + esc(f.num)) + '</small>' + esc(f.title) + '</button>';
      });
      html += '</div></section>';
    });
    panel('Overview', html);
  }
  function notes() {
    var s = slides[index], n = NOTES[s.dataset.label] || {};
    panel('Speaker notes · ' + (s.dataset.backup === 'true' ? s.dataset.label : 'slide ' + s.dataset.num),
      '<p class="notes-meta">' + esc(n.timing || '') + (s.dataset.backup === 'true' ? '' : ' · planned ' + esc(s.dataset.minutes) + ' min') + '</p>' +
      '<h3>' + esc(s.dataset.title) + '</h3><div class="notes-body">' + (n.html || '<p>No notes.</p>') + '</div>' +
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
      '<span><kbd>O</kbd></span><span>overview of all ' + slides.length + ' frames</span>' +
      '<span><kbd>N</kbd></span><span>speaker notes</span>' +
      '<span><kbd>G</kbd></span><span>notation</span>' +
      '<span><kbd>T</kbd></span><span>dark or light theme</span>' +
      '<span><kbd>F</kbd></span><span>fullscreen</span>' +
      '<span><kbd>R</kbd></span><span>reset the slide</span>' +
      '<span><kbd>Esc</kbd></span><span>back from a backup slide, or close a panel</span></div>' +
      '<p class="notes-meta">Numbers carry their registry key on hover. Figures draw closed forms of the paper at the benchmark; the slider reads those curves and solves no equilibrium.</p>');
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
  function reg(key) { return String(D.registry[key].display).replace(/\\%/g, '%'); }
  function regNum(key) { var p = String(D.registry[key].value).split('/'); return p.length === 2 ? Number(p[0]) / Number(p[1]) : Number(p[0]); }
  function vline(x, color, dash, xref) {
    return { type: 'line', xref: xref || 'x', yref: (xref === 'x2' ? 'y2' : 'y') + ' domain', x0: x, x1: x, y0: 0, y1: 1, line: { color: color, width: 1.2, dash: dash || 'dot' }, layer: 'below' };
  }
  function band(x0, x1, color, ax) {
    return { type: 'rect', xref: ax || 'x', yref: (ax === 'x2' ? 'y2' : 'y') + ' domain', x0: x0, x1: x1, y0: 0, y1: 1, fillcolor: color, layer: 'below' };
  }
  function label(x, text, color, o) {
    o = o || {};
    return { text: text, xref: o.xref || 'x', x: x, yref: (o.yref || 'y') + ' domain', y: o.y === undefined ? 1 : o.y, yanchor: o.yanchor || 'bottom', xanchor: o.xanchor || 'center', yshift: o.yshift === undefined ? 4 : o.yshift, xshift: o.xshift || 0, bgcolor: o.bg, font: { size: o.size || 15, color: color } };
  }
  function at(label, x, y, color, o) {
    o = o || {};
    return { text: label, xref: o.xref || 'x', x: x, yref: o.yref || 'y', y: y, xanchor: o.xanchor || 'left', yanchor: o.yanchor || 'bottom', xshift: o.xshift || 0, yshift: o.yshift === undefined ? 3 : o.yshift, bgcolor: true, font: { size: o.size || 15, color: color } };
  }
  function panelTag(text, xa, ya, t) {
    return { text: text, panel: true, xref: xa + ' domain', yref: ya + ' domain', x: 0, y: 1, xanchor: 'left', yanchor: 'bottom', xshift: -62, yshift: 4, font: { size: 16, color: t.ink } };
  }
  function pts(xs, ys, k) { return xs.map(function (_, i) { return [ys[i], k]; }); }
  function line(t, color, dash, w) { return { color: color, width: w || 3, dash: dash || 'solid' }; }
  function dot(x, y, color, open, xa, ya, size) {
    return { mode: 'markers', x: x, y: y, showlegend: false, hovertemplate: 'skip', xaxis: xa || 'x', yaxis: ya || 'y', marker: { symbol: open ? 'circle-open' : 'circle', size: size || 9, color: color } };
  }

  /* F7: the gain of a correctly signed order lies between its floor and its ceiling; compared with k. */
  function specGain(t) {
    var G = D.fig.gain, I = D.fig.inputs, B = D.fig.bounds, rS = B.rS_B;
    var traces = [
      { mode: 'lines', name: 'ceiling Δ<sub>T</sub>', x: G.r, y: G.upper, customdata: pts(G.r, G.upper), line: line(t, t.info), hovertemplate: '%{customdata[0]} <i>k</i><extra>ceiling Δ<sub>T</sub></extra>' },
      { mode: 'lines', name: 'floor ρκΔ<sub>T</sub>', x: G.r, y: G.lower, customdata: pts(G.r, G.lower), line: line(t, t.info, 'dash'), hovertemplate: '%{customdata[0]} <i>k</i><extra>floor ρκΔ<sub>T</sub></extra>' }
    ];
    var layout = { height: 395, margin: { l: 78, r: 20, t: 66, b: 56 }, shapes: [], annotations: [],
      xaxis: { domain: [0, 1], anchor: 'y', range: [1, 3.2], dtick: 0.5, tick0: 1, title: { text: 'incumbent strength <i>r</i>' } },
      yaxis: { domain: [0, 1], anchor: 'x', type: 'log', range: [-1.7, 1.8], tickvals: [0.1, 1, 10], ticktext: ['0.1', '1', '10'], title: { text: 'gain per correct order, in units of <i>k</i>' } } };
    layout.shapes.push(band(1, G.r_k, t.regionA), band(rS, 3.2, t.regionB));
    layout.shapes.push({ type: 'line', xref: 'x domain', yref: 'y', x0: 0, x1: 1, y0: 1, y1: 1, line: { color: t.cost, width: 2.4 }, layer: 'below' });
    layout.shapes.push(vline(I.r0, t.muted), vline(I.r1, t.muted));
    layout.annotations.push(at('cost <i>k</i>', 1.56, 1, t.cost, { xanchor: 'left', yshift: 4 }));
    layout.annotations.push(label(1.005, 'no trade only', t.muted, { xanchor: 'left', size: 14 }));
    layout.annotations.push(label((G.r_k + rS) / 2, 'Bounds inconclusive', t.muted, { size: 14, yshift: 24 }));
    layout.annotations.push(label(3.19, 'full orders only', t.muted, { xanchor: 'right', size: 14 }));
    layout.annotations.push({ text: 'weak <i>r</i><sub>0</sub>', xref: 'x', x: I.r0, xanchor: 'left', yref: 'y domain', y: 0, yanchor: 'bottom', xshift: 4, yshift: 6, font: { size: 15, color: t.muted } });
    layout.annotations.push({ text: 'strong <i>r</i><sub>1</sub>', xref: 'x', x: I.r1, xanchor: 'right', yref: 'y domain', y: 0, yanchor: 'bottom', xshift: -4, yshift: 6, font: { size: 15, color: t.muted } });
    var i0 = G.r.indexOf(I.r0), i1 = G.r.indexOf(I.r1);
    traces.push(dot([I.r0], [G.upper[i0]], t.info, false), dot([I.r1], [G.lower[i1]], t.info, false));
    return { traces: traces, layout: layout };
  }

  /* F8: the threshold belief against strength, the band of beliefs a price can induce, and the slider's strength. */
  var beliefsIndex = 180;
  function specBeliefs(t, i) {
    var Bf = D.fig.belief, I = D.fig.inputs, B = D.fig.bounds, r = Bf.r[i];
    var traces = [{ mode: 'lines', name: 'threshold belief τ(<i>r</i>)', x: Bf.r, y: Bf.tau, customdata: pts(Bf.r, Bf.tau), line: line(t, t.cost, 'solid', 3.4), hovertemplate: '%{customdata[0]}<extra>threshold belief τ(<i>r</i>)</extra>' }];
    var layout = { height: 330, margin: { l: 70, r: 20, t: 44, b: 54 }, shapes: [], annotations: [],
      xaxis: { domain: [0, 1], anchor: 'y', range: [1.2, 3.6], dtick: 0.4, tick0: 1.2, title: { text: 'incumbent strength <i>r</i>' } },
      yaxis: { domain: [0, 1], anchor: 'x', range: [0.2, 0.8], dtick: 0.1, tick0: 0.2, title: { text: 'belief' } } };
    layout.shapes.push({ type: 'rect', xref: 'x domain', yref: 'y', x0: 0, x1: 1, y0: I.m, y1: I.M, fillcolor: t.regionB, layer: 'below' });
    layout.shapes.push({ type: 'line', xref: 'x domain', yref: 'y', x0: 0, x1: 1, y0: I.pi, y1: I.pi, line: { color: t.muted, width: 1.2, dash: 'dash' }, layer: 'below' });
    [['prim_r0', 'weak <i>r</i><sub>0</sub>'], ['prim_r1', 'strong <i>r</i><sub>1</sub>'], ['prim_r2', 'still <i>r</i><sub>2</sub>']].forEach(function (mk) {
      var x = regNum(mk[0]); layout.shapes.push(vline(x, t.muted)); layout.annotations.push(label(x, mk[1], t.muted, { size: 14 }));
    });
    layout.annotations.push(at('<i>M</i> = ' + reg('M_half_B'), 1.22, I.M, t.info, { yshift: 3 }));
    layout.annotations.push(at('prior ' + reg('prim_pi'), 1.22, I.pi, t.muted, { yshift: 3 }));
    layout.annotations.push(at('<i>m</i> = ' + reg('m_half_B'), 1.22, I.m, t.info, { yanchor: 'top', yshift: -3 }));
    layout.annotations.push(at('<i>r</i><sub>C</sub>', B.rC_B, I.M, t.cost, { xanchor: 'center', yanchor: 'top', yshift: -8 }));
    traces.push(dot([B.rC_B], [I.M], t.cost, true, 'x', 'y', 11));
    layout.shapes.push({ type: 'line', xref: 'x', yref: 'y domain', x0: r, x1: r, y0: 0, y1: 1, line: { color: t.accent, width: 2 } });
    traces.push({ mode: 'markers', name: 'slider', showlegend: false, x: [r], y: [Bf.tau[i]], hovertemplate: 'skip', marker: { symbol: 'circle', size: 12, color: t.accent, line: { width: 2, color: t.bg } } });
    return { traces: traces, layout: layout };
  }

  /* F12: entry on each branch at the prior, whole path (a) and the strengths where the thresholds sit (b). */
  function specCoex(t) {
    var E = D.fig.entry, I = D.fig.inputs, B = D.fig.bounds;
    var navy = t.accent, brick = t.info, grey = t.c3, traces = [], layout = { height: 292, margin: { l: 66, r: 16, t: 50, b: 52 }, shapes: [], annotations: [] };
    var panels = [{ x: 'x', y: 'y', dom: [0, 0.47], range: [1.2, 3.6], dtick: 0.4, tick0: 1.2 }, { x: 'x2', y: 'y2', dom: [0.57, 1], range: [1.2, 2.4], dtick: 0.2, tick0: 1.2 }];
    panels.forEach(function (P, j) {
      layout['xaxis' + (j ? '2' : '')] = { domain: P.dom, anchor: P.y, range: P.range, dtick: P.dtick, tick0: P.tick0, title: { text: 'incumbent strength <i>r</i>' } };
      layout['yaxis' + (j ? '2' : '')] = { domain: [0, 1], anchor: P.x, range: [0.2, 0.58], dtick: 0.1, tick0: 0.2, title: { text: j ? '' : 'entry' } };
      layout.shapes.push(band(B.rA, B.rN, t.regionA, P.x));
      layout.annotations.push(panelTag(j ? '(b)' : '(a)', P.x, P.y, t));
      function add(name, br, color, dash, w, tpl, grp) {
        traces.push({ mode: 'lines', name: name, legendgroup: grp || name, showlegend: j === 0, x: br.r, y: br.y, customdata: pts(br.r, br.y), xaxis: P.x, yaxis: P.y,
          line: line(t, color, dash, w), hovertemplate: tpl + ' = %{customdata[0]}<extra>' + name + '</extra>' });
      }
      add('N: no informed trade', E.N, navy, 'solid', 3.2, 'entry');
      add('Q: mixed orders at the floor', E.Q, grey, 'dashdot', 3, 'entry');
      add('R: mixed purchase', E.R, brick, 'dash', 3.2, 'entry');
      add('F: full purchase', E.F, brick, 'solid', 3.2, 'entry');
      add('F above r_C', E.F_floor, brick, 'solid', 3.2, 'entry', 'F: full purchase');
      var end = function (a) { return a[a.length - 1]; };
      traces.push(dot([end(E.N.r), E.R.r[0], E.F.r[0], end(E.F.r)], [end(E.N.y), E.R.y[0], E.F.y[0], end(E.F.y)], navy, false, P.x, P.y, 8));
      traces.push(dot([E.Q.r[0], end(E.Q.r), E.F_floor.r[0]], [E.Q.y[0], end(E.Q.y), E.F_floor.y[0]], grey, true, P.x, P.y, 9));
    });
    var lab = function (txt, x, ax, lvl) { layout.annotations.push({ text: txt, xref: ax, x: x, yref: (ax === 'x2' ? 'y2' : 'y') + ' domain', y: 1, yanchor: 'bottom', yshift: 4 + lvl * 17, xanchor: 'center', font: { size: 14, color: t.muted } }); layout.shapes.push(vline(x, t.muted, 'dot', ax)); };
    lab('<i>r</i><sub>0</sub>', I.r0, 'x', 0); lab('<i>r</i><sub>1</sub>', I.r1, 'x', 0); lab('<i>r</i><sub>2</sub>', I.r2, 'x', 0); lab('<i>r</i><sub>C</sub>', B.rC_B, 'x', 1);
    lab('<i>r</i><sub>A</sub>', B.rA, 'x2', 0); lab('<i>r</i><sub>F</sub>', B.rF_B, 'x2', 1); lab('<i>r</i><sub>N</sub>', B.rN, 'x2', 0); lab('<i>r</i><sub>J</sub>', B.rJ, 'x2', 1); lab('<i>r</i><sub>S</sub>', B.rS_B, 'x2', 0);
    layout.annotations.push({ text: 'N and<br>informative<br>coexist', xref: 'x2', x: (B.rA + B.rN) / 2, yref: 'y2 domain', y: 0.45, yanchor: 'middle', xanchor: 'center', font: { size: 14, color: t.accent } });
    layout.annotations.push(at('N: no trade', 1.215, E.N.y[0], t.accent, { xref: 'x2', yref: 'y2', yshift: 4 }));
    layout.annotations.push(at('Q', (B.rN + B.rJ) / 2, E.Q.y[0], t.c3, { xref: 'x2', yref: 'y2', xanchor: 'center', yshift: 4 }));
    layout.annotations.push(at('R: mixed purchase', 1.455, 0.455, t.info, { xref: 'x2', yref: 'y2', yshift: 0 }));
    layout.annotations.push(at('F: full purchase', 1.62, E.F.y[0], t.info, { xref: 'x2', yref: 'y2', yshift: 4 }));
    layout.annotations.push(at('F', 2.6, E.F.y[0], t.info, { xref: 'x', yref: 'y', xanchor: 'center', yshift: 4 }));
    layout.annotations.push(at('N', 1.35, E.N.y[0], t.accent, { xref: 'x', yref: 'y', xanchor: 'center', yshift: 4 }));
    return { traces: traces, layout: layout };
  }

  /* F13: research intensity (a) and entry (b) on the strengths where the research branch lives. */
  function specResearch(t) {
    var R = D.fig.research, I = D.fig.inputs, B = D.fig.bounds, rho = I.rho;
    var navy = t.accent, brick = t.info, traces = [], layout = { height: 262, margin: { l: 70, r: 16, t: 50, b: 52 }, shapes: [], annotations: [] };
    var panels = [{ x: 'x', y: 'y', dom: [0, 0.47], name: 'λ', ylab: 'research intensity λ', range: [-0.03, 0.42], dtick: 0.1, tick0: 0 },
      { x: 'x2', y: 'y2', dom: [0.57, 1], name: 'E', ylab: 'total entry', range: [0.2, 0.58], dtick: 0.1, tick0: 0.2 }];
    panels.forEach(function (P, j) {
      layout['xaxis' + (j ? '2' : '')] = { domain: P.dom, anchor: P.y, range: [1.2, 2.0], dtick: 0.2, tick0: 1.2, title: { text: 'incumbent strength <i>r</i>' } };
      layout['yaxis' + (j ? '2' : '')] = { domain: [0, 1], anchor: P.x, range: P.range, dtick: P.dtick, tick0: P.tick0, title: { text: P.ylab } };
      layout.shapes.push(band(B.rN, 2.0, t.regionC, P.x));
      layout.annotations.push(panelTag(j ? '(b)' : '(a)', P.x, P.y, t));
      var zero = j ? rho : 0, cap = j ? R.plateau : R.cap_value, ys = j ? R.branch.entry : R.branch.lambda;
      traces.push({ mode: 'lines', name: 'zero research', legendgroup: 'zero', showlegend: j === 0, x: R.zero.r, y: R.zero.r.map(function () { return zero; }), xaxis: P.x, yaxis: P.y, line: line(t, navy), customdata: R.zero.r.map(function () { return [zero]; }), hovertemplate: P.name + ' = %{customdata[0]}<extra>zero research</extra>' });
      traces.push({ mode: 'lines', name: 'research branch', legendgroup: 'branch', showlegend: j === 0, x: R.branch.r, y: ys, xaxis: P.x, yaxis: P.y, line: line(t, brick, 'dash'), customdata: pts(R.branch.r, ys), hovertemplate: P.name + ' = %{customdata[0]}<extra>research branch</extra>' });
      traces.push({ mode: 'lines', name: 'research at the cap', legendgroup: 'cap', showlegend: j === 0, x: R.cap.r, y: R.cap.r.map(function () { return cap; }), xaxis: P.x, yaxis: P.y, line: line(t, brick), customdata: R.cap.r.map(function () { return [cap]; }), hovertemplate: P.name + ' = %{customdata[0]}<extra>research at the cap</extra>' });
      traces.push(dot([B.rN], [zero], navy, false, P.x, P.y, 8), dot([B.res_rR], [ys[0]], brick, false, P.x, P.y, 8), dot([B.res_rcap], [cap], brick, false, P.x, P.y, 8), dot([B.rN], [cap], brick, true, P.x, P.y, 9));
      [[B.res_rR, 'r<sub>R</sub>', 0], [B.res_rcap, 'r̄<sub>R</sub>', 0], [B.rN, 'r<sub>N</sub>', 1]].forEach(function (mk) {
        layout.shapes.push(vline(mk[0], t.muted, 'dot', P.x));
        layout.annotations.push({ text: mk[1].replace(/^r/, '<i>r</i>').replace('r̄', '<i>r̄</i>'), xref: P.x, x: mk[0], yref: P.y + ' domain', y: 1, yanchor: 'bottom', yshift: 4 + mk[2] * 17, xanchor: 'center', font: { size: 14, color: t.muted } });
      });
      layout.annotations.push({ text: 'beyond <i>r</i><sub>N</sub>', xref: P.x, x: (B.rN + 2.0) / 2, yref: P.y + ' domain', y: 0.5, yanchor: 'middle', xanchor: 'center', font: { size: 15, color: t.muted } });
    });
    layout.annotations.push(at('cap λ̄ = ' + reg('res_cap'), 1.21, D.fig.research.cap_value, t.muted, { yshift: 4, size: 14 }));
    layout.shapes.push({ type: 'line', xref: 'x', yref: 'y', x0: 1.2, x1: B.res_rcap, y0: R.cap_value, y1: R.cap_value, line: { color: t.muted, width: 1.2, dash: 'dot' }, layer: 'below' });
    layout.annotations.push(at('zero research', 1.21, 0, t.accent, { yshift: 5, size: 14 }));
    layout.annotations.push(at('research branch', 1.58, 0.14, t.info, { yshift: 0, size: 14 }));
    layout.annotations.push(at('zero research', 1.21, I.rho, t.accent, { xref: 'x2', yref: 'y2', yshift: 5, size: 14 }));
    layout.annotations.push(at('research branch', 1.50, 0.40, t.info, { xref: 'x2', yref: 'y2', yshift: 0, size: 14 }));
    layout.annotations.push(at(reg('res_entry_rR'), B.res_rR - 0.012, R.branch.entry[0], t.info, { xref: 'x2', yref: 'y2', xanchor: 'center', yanchor: 'top', yshift: -8, size: 14 }));
    layout.annotations.push(at(reg('res_entry_cap'), B.res_rcap, R.plateau, t.info, { xref: 'x2', yref: 'y2', xanchor: 'center', yshift: 8, size: 14 }));
    return { traces: traces, layout: layout };
  }

  var chartState = {};
  function drawChart(el, spec, key) {
    var st = chartState[key] || (chartState[key] = { hidden: {} });
    st.width = 0;
    st.zoom = 1.4; // slides are read from a distance: draw narrow and scale up
    if (el.classList.contains('nolegend')) spec.traces.forEach(function (tr) { tr.showlegend = false; });
    CCC.charts.draw(el, spec, tokens(), st);
    el.setAttribute('data-mounted', 'true');
    return st;
  }

  /* ---------- widgets ---------- */
  var INFOSETS = {
    seller: 'Seller: announces the sale rule, a cash second-price auction with reserve p, before any trade. The rule is public.',
    slot: 'Order slot: one public slot. With probability λ the informed investor fills it and sees the challenger’s class; otherwise a liquidity trader fills it. No one sees who filled it.',
    makers: 'Market makers: see the order X in the slot, not who placed it. They set the stock price P at expected sale proceeds per share, given X.',
    challenger: 'Challenger: sees the stock price and its own preparation cost. It does not see the order, the class or the incumbent’s value R. Paying the cost reveals its value.',
    bidders: 'Bidders: the incumbent knows R ∼ U[0, r], and r is public. An entered challenger knows its value. Each bids its value.'
  };
  widgets.infosets = {
    render: function (s) {
      $$('.tl', s).forEach(function (b) {
        b.setAttribute('aria-pressed', 'false');
        b.onclick = b.onfocus = b.onmouseenter = function () {
          $$('.tl', s).forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
          $('#f2-infoset').textContent = INFOSETS[b.dataset.info];
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
  /* F5: select an order to see the belief it induces under full orders. */
  widgets.orders = {
    render: function (s) {
      var say = {
        '-1': 'A sale comes from the informed investor in class L or from a liquidity sale in either class. The belief falls to m(π) = ' + reg('m_half_B') + ', the floor for every investor strategy.',
        '0': 'Only a liquidity trader abstains, in both classes with the same chance. The belief stays at the prior ' + reg('prim_pi') + '.',
        '1': 'A buy comes from the informed investor in class H or from a liquidity buy in either class. The belief rises to M(π) = ' + reg('M_half_B') + ', the ceiling for every investor strategy.'
      };
      var pos = { '-1': regNum('m_half_B'), '0': 0.5, '1': regNum('M_half_B') };
      var pick = function (o) {
        $$('.segmented button', s).forEach(function (x) { x.setAttribute('aria-pressed', String(x.dataset.order === o)); });
        $$('[data-order]', $('.t-orders', s)).forEach(function (c) { c.classList.toggle('hl', c.dataset.order === o); });
        var pin = $('#f5-pin', s); pin.hidden = false; pin.style.left = (100 * pos[o]).toFixed(2) + '%';
        $('#f5-say', s).textContent = say[o];
      };
      $$('.segmented button', s).forEach(function (b) { b.onclick = function () { pick(b.dataset.order); }; });
      widgets.orders.pick = pick;
    },
    reset: function (s) {
      $$('.segmented button', s).forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
      $$('.hl', s).forEach(function (c) { c.classList.remove('hl'); });
      $('#f5-pin', s).hidden = true; $('#f5-say', s).textContent = 'Select an order to see where the belief goes.';
    }
  };
  widgets.gain = { render: function (s) { drawChart($('#gain', s), specGain(tokens()), 'gain'); } };
  widgets.beliefs = {
    render: function (s) {
      var input = $('#beliefs-r', s);
      input.value = String(beliefsIndex);
      input.oninput = function () { beliefsIndex = Number(input.value); widgets.beliefs.draw(s); };
      widgets.beliefs.draw(s);
    },
    draw: function (s) {
      var Bf = D.fig.belief, I = D.fig.inputs, i = beliefsIndex, r = Bf.r[i];
      drawChart($('#beliefs', s), specBeliefs(tokens(), i), 'beliefs');
      $('#beliefs-r-value', s).textContent = r.toFixed(2);
      var clears = Bf.tau[i] <= I.M, f = function (x) { return x.toFixed(3); };
      $('#beliefs-readout', s).innerHTML =
        '<p>At <i>r</i> = <b>' + r.toFixed(2) + '</b>: τ(<i>r</i>) = <b>' + f(Bf.tau[i]) + '</b>, top belief <i>M</i> = <b>' + reg('M_half_B') + '</b>, <i>B<sub>r</sub></i>(<i>M</i>) = <b>' + f(Bf.B_M[i]) + '</b> against <i>c<sub>H</sub></i> = <b>' + reg('prim_cH') + '</b></p>' +
        '<p><span class="chip ' + (clears ? 'ok' : 'no') + '">' + (clears ? 'a buy order clears the threshold' : 'no order clears the threshold') + '</span></p>' +
        '<p class="note">Values on the plotted curve; the ceiling <i>r</i><sub>C</sub> = ' + reg('rC_B') + '.</p>';
    },
    reset: function () { beliefsIndex = 180; }
  };
  widgets.controls = {
    render: function (s) {
      var pick = function (row) {
        $$('.segmented button', s).forEach(function (x) { x.setAttribute('aria-pressed', String(x.dataset.row === row)); });
        $$('tr[data-row]', s).forEach(function (tr) { tr.classList.toggle('hl', tr.dataset.row === row); });
        var tr = $('tr[data-row="' + row + '"]', s), vals = $$('td .q', tr).map(function (q) { return { shown: q.textContent, v: regNum(q.dataset.q) }; });
        var bar = function (lab, o) { return '<div class="bar-row"><span>' + lab + '</span><div class="bar' + (row === 'eq' ? ' info' : '') + '" style="transform:scaleX(' + o.v + ')"></div><span class="num">' + o.shown + '</span></div>'; };
        $('#f11-bars', s).innerHTML = '<p class="small">Entry</p>' + bar('<i>r</i><sub>0</sub>', vals[0]) + bar('<i>r</i><sub>1</sub>', vals[1]);
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
  widgets.coex = { render: function (s) { drawChart($('#coex', s), specCoex(tokens()), 'coex'); } };
  widgets.research = { render: function (s) { drawChart($('#research', s), specResearch(tokens()), 'research'); } };
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

  function renderWidget(force) {
    var s = slides[index], w = widgets[s.dataset.widget];
    if (!w || !w.render) return;
    if (!force && s.dataset.rendered === '1' && !/^(gain|beliefs|coex|research)$/.test(s.dataset.widget)) return;
    try { w.render(s); s.dataset.rendered = '1'; } catch (e) { errors.push(s.id + ': ' + e.message); }
  }

  /* Disclosures inside slides, and the link buttons. */
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
  /* ?print=1 (the PDF export) draws every figure and table before the browser prints. */
  if (/[?&]print=1/.test(location.search)) {
    slides.forEach(function (s, i) { go(i, { step: 'last', keepHash: true }); });
    go(0, { step: 0, keepHash: true });
  }
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
