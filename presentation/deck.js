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
  /* The footline prints "n / total" on a main frame; a backup prints its label alone. */
  slides.forEach(function (s) { var n = s.querySelector('.foot-num'); if (n && s.dataset.backup !== 'true') n.dataset.total = String(TOTAL); });
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
  /* Back returns to the place the link was followed from when that is the button's target (B2 has one
     return button for each of frames 11, 12 and 13); otherwise to the button's target. */
  function back(target) {
    var want = target ? targetOf[target] : null;
    if (returns.length && (!want || slides[returns[returns.length - 1].index].id === want)) { var r = returns.pop(); go(r.index, { step: r.step }); return; }
    returns = [];
    var id = want;
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
    var html = '<p class="notes-meta">All ' + slides.length + ' frames of the Beamer deck in their order: the title, slides 1 to ' + TOTAL + ', then the ' + (slides.length - mainCount) + ' backup frames.</p>';
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
      '<p class="notes-meta">Numbers carry their registry key on hover. Figures draw closed forms of the paper in the example and solve no equilibrium.</p>');
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

  /* Frame 14: the close-up of the threshold belief between the strong incumbent r_1 and the very strong
     incumbent r_2 (panel (b) of the belief figure of slides.tex), with the top belief M(1/2), the band
     up to it from tau(r_1), and the three values the Beamer figure prints. */
  function specBeliefs(t) {
    var Bf = D.fig.belief, I = D.fig.inputs, r1 = I.r1, r2 = I.r2, M = I.M, t1 = regNum('tau_r1'), t2 = regNum('tau_r2');
    var xs = [], ys = [];
    Bf.r.forEach(function (r, i) { if (r >= r1 - 1e-9 && r <= r2 + 1e-9) { xs.push(r); ys.push(Bf.tau[i]); } });
    var traces = [{ mode: 'lines', name: 'threshold belief τ(<i>r</i>)', x: xs, y: ys, customdata: pts(xs, ys), line: line(t, t.cost, 'solid', 3.4), hovertemplate: 'τ(<i>r</i>) = %{customdata[0]}<extra>threshold belief</extra>' }];
    var layout = { height: 290, margin: { l: 62, r: 14, t: 34, b: 50 }, shapes: [], annotations: [],
      xaxis: { domain: [0, 1], anchor: 'y', range: [r1, r2], tickvals: [r1, 3.2, 3.4, r2], ticktext: ['r₁', '3.2', '3.4', 'r₂'], title: { text: 'incumbent strength, <i>r</i>' } },
      yaxis: { domain: [0, 1], anchor: 'x', range: [0.70, 0.735], tickvals: [0.70, 0.71, 0.72, 0.73], ticktext: ['0.70', '0.71', '0.72', '0.73'], title: { text: 'belief, τ(<i>r</i>) and <i>M</i>(1/2)' } } };
    layout.shapes.push({ type: 'rect', xref: 'x domain', yref: 'y', x0: 0, x1: 1, y0: t1, y1: M, fillcolor: t.regionB, layer: 'below' });
    layout.shapes.push({ type: 'line', xref: 'x domain', yref: 'y', x0: 0, x1: 1, y0: M, y1: M, line: { color: t.info, width: 3 }, layer: 'below' });
    layout.shapes.push({ type: 'line', xref: 'x domain', yref: 'y', x0: 0, x1: 1, y0: t1, y1: t1, line: { color: t.info, width: 1.2 }, layer: 'below' });
    layout.shapes.push({ type: 'line', xref: 'x domain', yref: 'y', x0: 0, x1: 1, y0: t2, y1: t2, line: { color: t.bg, width: 1.2, dash: 'dash' }, layer: 'below' });
    layout.shapes.push(vline(r2, t.muted));
    layout.annotations.push(at('τ(<i>r</i><sub>2</sub>) ≈ ' + reg('tau_r2'), r1 + 0.02, t2, t.ink, { yshift: 6, size: 12 }));
    layout.annotations.push(at('<i>M</i>(1/2) ≈ ' + reg('M_half_B'), r1 + 0.02, M, t.ink, { yanchor: 'top', yshift: -6, size: 12 }));
    layout.annotations.push(at('band for <i>M</i>(1/2)', r2 - 0.02, t1 + 0.0042, t.ink, { xanchor: 'right', yshift: 0, size: 12 }));
    layout.annotations.push(at('τ(<i>r</i><sub>1</sub>) = ' + reg('tau_r1'), r2 - 0.02, t1, t.ink, { xanchor: 'right', yshift: 4, size: 12 }));
    traces.push(dot([r1], [t1], t.cost, false, 'x', 'y', 11));
    traces.push(dot([r2], [t2], t.cost, true, 'x', 'y', 11));
    return { traces: traces, layout: layout };
  }

  /* B3: the coexistence region at the prior 1/2 in the plane of the spread and the threshold, with the example's path. */
  function specRegion(t) {
    var G = D.fig.region, I = D.fig.inputs, navy = t.accent, brick = t.info;
    var left = G.left, top = I.M;
    var xs = left.Delta.concat([G.D_N, G.D_N]), ys = left.tau.concat([top, 0.5]);
    var traces = [
      { mode: 'lines', name: 'coexistence region', showlegend: false, x: xs.concat([xs[0]]), y: ys.concat([ys[0]]), fill: 'toself', fillcolor: t.regionB, line: { color: t.regionB, width: 0.1 }, hovertemplate: 'skip' },
      // closed edges: Δ_T = k/(1−τ), Δ_T = 2k/ρ and τ = M(π); the edge τ = π is open and stays the dotted prior line
      { mode: 'lines', name: 'coexistence region', x: left.Delta.concat([G.D_N, G.D_N]), y: left.tau.concat([top, 0.5]), line: line(t, t.ink, 'solid', 2), hovertemplate: 'skip' },
      { mode: 'lines', name: 'Δ<sub>T</sub> = k/(1−M)', x: [G.D_F, G.D_F], y: [0.5, top], line: line(t, t.ink, 'dash', 1.4), hovertemplate: 'skip' },
      { mode: 'lines', name: 'path of the example', x: G.path.Delta, y: G.path.tau, customdata: G.path.r.map(function (r) { return [r.toFixed(3)]; }), line: line(t, brick, 'solid', 3),
        hovertemplate: '<i>r</i> = %{customdata[0]}<extra>path of the example</extra>' }
    ];
    var layout = { height: 300, margin: { l: 60, r: 12, t: 30, b: 52 }, shapes: [], annotations: [],
      xaxis: { domain: [0, 1], anchor: 'y', range: [0, 0.2], tickvals: [0, 0.1, 0.2], ticktext: ['0.0', '0.1', '0.2'], title: { text: 'shareholder spread, Δ<sub><i>T</i></sub>' } },
      yaxis: { domain: [0, 1], anchor: 'x', range: [0.48, 0.765], tickvals: [0.5, 0.6, 0.7], ticktext: ['0.5', '0.6', '0.7'], title: { text: 'threshold, τ' } } };
    layout.annotations.push(panelTag('(b)', 'x', 'y', t));
    layout.shapes.push({ type: 'line', xref: 'x domain', yref: 'y', x0: 0, x1: 1, y0: I.pi, y1: I.pi, line: { color: t.muted, width: 1.2, dash: 'dot' }, layer: 'below' });
    layout.annotations.push(at('π = ' + reg('prim_pi'), 0.004, I.pi, t.ink, { yanchor: 'top', yshift: -3, size: 12 }));
    layout.shapes.push({ type: 'line', xref: 'x', yref: 'y', x0: 0, x1: G.D_F, y0: top, y1: top, line: { color: t.ink, width: 1.2, dash: 'dot' }, layer: 'below' });
    layout.annotations.push(at('<i>M</i>(1/2)', 0.004, top, t.ink, { yshift: 3, size: 12 }));
    var Mk = G.marks;
    traces.push(dot([Mk.prim_r0[0]], [Mk.prim_r0[1]], t.ink, false, 'x', 'y', 10));
    traces.push(dot([Mk.rA[0], Mk.rF_B[0], Mk.rN[0]], [Mk.rA[1], Mk.rF_B[1], Mk.rN[1]], brick, false, 'x', 'y', 10));
    layout.annotations.push(at('<i>r</i><sub>0</sub>', Mk.prim_r0[0], Mk.prim_r0[1], t.ink, { xanchor: 'left', yanchor: 'top', yshift: -6, xshift: 2, size: 13 }));
    layout.annotations.push(at('<i>r</i><sub>A</sub>', Mk.rA[0], Mk.rA[1], brick, { xanchor: 'right', yanchor: 'bottom', xshift: -2, yshift: 6, size: 13 }));
    layout.annotations.push(at('<i>r</i><sub>F</sub>', Mk.rF_B[0], Mk.rF_B[1], brick, { xanchor: 'left', yanchor: 'bottom', xshift: 0, yshift: 8, size: 13 }));
    layout.annotations.push(at('<i>r</i><sub>N</sub>', Mk.rN[0], Mk.rN[1], brick, { xanchor: 'left', yanchor: 'top', xshift: 4, yshift: -6, size: 13 }));
    layout.annotations.push(at('coexistence', (G.D_F + G.D_N) / 2, 0.705, t.ink, { xanchor: 'center', size: 13 }));
    return { traces: traces, layout: layout };
  }

  /* B3, page 2: entry in each equilibrium at the prior, the whole path (a) and the marked strengths (c). */
  function specCoex(t) {
    var E = D.fig.entry, I = D.fig.inputs, B = D.fig.bounds;
    var brick = t.info, grey = t.c3, traces = [], layout = { height: 215, margin: { l: 52, r: 10, t: 40, b: 46 }, shapes: [], annotations: [] };
    var panels = [{ x: 'x', y: 'y', dom: [0, 0.39], range: [1.2, 3.6], tickvals: [1.2, 2.0, 2.8, 3.6], tag: '(a)' },
      { x: 'x2', y: 'y2', dom: [0.49, 1], range: [1.26, 2.4], tickvals: [1.4, 1.8, 2.2], tag: '(c)' }];
    panels.forEach(function (P, j) {
      layout['xaxis' + (j ? '2' : '')] = { domain: P.dom, anchor: P.y, range: P.range, tickvals: P.tickvals, ticktext: P.tickvals.map(function (v) { return v.toFixed(1); }), title: { text: 'incumbent strength, <i>r</i>' } };
      layout['yaxis' + (j ? '2' : '')] = { domain: [0, 1], anchor: P.x, range: [0.17, 0.62], dtick: 0.1, tick0: 0.2, title: { text: j ? '' : 'entry, <i>E</i>' } };
      layout.shapes.push(band(B.rA, B.rN, t.regionB, P.x));
      var tag = panelTag(P.tag, P.x, P.y, t); tag.xshift = j ? -40 : -50; layout.annotations.push(tag);
      function add(name, br, color, dash, w, grp) {
        traces.push({ mode: 'lines', name: name, legendgroup: grp || name, showlegend: false, x: br.r, y: br.y, customdata: pts(br.r, br.y), xaxis: P.x, yaxis: P.y,
          line: line(t, color, dash, w), hovertemplate: 'entry = %{customdata[0]}<extra>' + name + '</extra>' });
      }
      add('T threshold pair', E.T, t.ink, 'dash', 1.4);
      add('N uninformative market', E.N, t.ink, 'solid', 3.2);
      add('Q mixed orders at the entry floor', E.Q, grey, 'dashdot', 3);
      add('R mixed purchase that recruits', E.R, brick, 'dash', 3.2);
      add('F full purchase', E.F, brick, 'solid', 3.2);
      add('F above r_C', E.F_floor, brick, 'solid', 3.2, 'F full purchase');
      var end = function (a) { return a[a.length - 1]; };
      traces.push(dot([E.R.r[0], E.F.r[0], end(E.F.r)], [E.R.y[0], E.F.y[0], end(E.F.y)], brick, false, P.x, P.y, 8));
      traces.push(dot([end(E.N.r), end(E.Q.r)], [end(E.N.y), end(E.Q.y)], grey, true, P.x, P.y, 9));
      traces.push(dot([E.F_floor.r[E.F_floor.r.length - 1]], [E.F_floor.y[0]], brick, true, P.x, P.y, 9));
    });
    var lab = function (txt, x, ax) { layout.annotations.push({ text: txt, xref: ax, x: x, yref: (ax === 'x2' ? 'y2' : 'y') + ' domain', y: 1, yanchor: 'bottom', yshift: 4, xanchor: 'center', font: { size: 12, color: t.muted } }); layout.shapes.push(vline(x, t.muted, 'dot', ax)); };
    lab('<i>r</i><sub>C</sub>', B.rC_B, 'x');
    layout.shapes.push(vline(B.rA, t.muted, 'dot', 'x'), vline(B.rN, t.muted, 'dot', 'x'));
    lab('<i>r</i><sub>A</sub>', B.rA, 'x2'); lab('<i>r</i><sub>F</sub>', B.rF_B, 'x2'); lab('<i>r</i><sub>N</sub>', B.rN, 'x2'); lab('<i>r</i><sub>J</sub>', B.rJ, 'x2'); lab('<i>r</i><sub>S</sub>', B.rS_B, 'x2');
    layout.shapes.push({ type: 'line', xref: 'x', yref: 'y', x0: 1.3, x1: 2.4, y0: 0.585, y1: 0.585, line: { color: t.muted, width: 1.4 }, layer: 'above' });
    layout.annotations.push(at('(c)', 2.45, 0.585, t.muted, { yanchor: 'middle', yshift: 0, size: 12 }));
    layout.annotations.push(at('F', 3.1, E.F.y[0], brick, { xanchor: 'center', yshift: 5, size: 13 }));
    layout.annotations.push(at('F', I.r2, I.rho, brick, { xanchor: 'right', xshift: -6, yshift: 8, size: 13 }));
    layout.annotations.push(at('N', 1.3, I.rho, t.ink, { xanchor: 'center', yshift: 5, size: 13 }));
    layout.annotations.push(at('R', B.rA, E.R.y[0], brick, { xref: 'x2', yref: 'y2', xanchor: 'right', xshift: -6, yshift: 2, size: 13 }));
    layout.annotations.push(at('F', 2.33, E.F.y[0], brick, { xref: 'x2', yref: 'y2', xanchor: 'center', yshift: 5, size: 13 }));
    layout.annotations.push(at('T', 1.86, 0.31, t.ink, { xref: 'x2', yref: 'y2', xanchor: 'center', yshift: 0, size: 13 }));
    layout.annotations.push(at('Q', (B.rN + B.rJ) / 2, I.rho, grey, { xref: 'x2', yref: 'y2', xanchor: 'center', yanchor: 'top', yshift: -6, size: 13 }));
    layout.annotations.push(at('N', 1.28, I.rho, t.ink, { xref: 'x2', yref: 'y2', xanchor: 'left', yanchor: 'top', yshift: -6, size: 13 }));
    layout.annotations.push(at('coexistence', (B.rA + B.rN) / 2, 0.18, t.ink, { xref: 'x2', yref: 'y2', xanchor: 'center', yshift: 2, size: 12 }));
    return { traces: traces, layout: layout };
  }

  /* B12, page 2: research (a) and total entry (b) along the path in each research equilibrium, with the
     example strengths of B12, page 4 and r_1, r_2 marked. */
  function specResearch(t) {
    var R = D.fig.research, I = D.fig.inputs, B = D.fig.bounds, rho = I.rho;
    var brick = t.info, grey = t.c3, traces = [], layout = { height: 234, margin: { l: 58, r: 10, t: 44, b: 46 }, shapes: [], annotations: [] };
    var panels = [{ x: 'x', y: 'y', name: 'λ', ylab: 'research <i>λ</i>', range: [-0.03, 0.42], dtick: 0.1, tick0: 0, dom: [0, 0.43] },
      { x: 'x2', y: 'y2', name: 'entry', ylab: 'total entry <i>E</i>', range: [0.2, 0.58], dtick: 0.1, tick0: 0.2, dom: [0.6, 1] }];
    var ex = ['155', '160', '165'];
    panels.forEach(function (P, j) {
      layout['xaxis' + (j ? '2' : '')] = { domain: P.dom, anchor: P.y, range: [I.r0, I.r2], tickvals: [1.2, 2.0, 2.8, 3.6], ticktext: ['1.2', '2.0', '2.8', '3.6'], title: { text: 'strength, weak to very strong' } };
      layout['yaxis' + (j ? '2' : '')] = { domain: [0, 1], anchor: P.x, range: P.range, dtick: P.dtick, tick0: P.tick0, title: { text: P.ylab } };
      layout.annotations.push(panelTag(j ? '(b)' : '(a)', P.x, P.y, t));
      var zero = j ? rho : 0, cap = j ? R.plateau : R.cap_value, ys = j ? R.recruit.entry : R.recruit.lambda;
      var fy = j ? R.floor.entry : R.floor.lambda, fcap = j ? rho : R.cap_value;
      var seg = function (name, xs, yv, color, dash) {
        traces.push({ mode: 'lines', name: name, showlegend: false, x: xs, y: yv, xaxis: P.x, yaxis: P.y, line: line(t, color, dash), customdata: pts(xs, yv),
          hovertemplate: P.name + ' = %{customdata[0]}<extra>' + name + '</extra>' });
      };
      seg('zero research', R.zero.r, R.zero.r.map(function () { return zero; }), t.ink);
      seg('recruiting research', R.recruit.r, ys, brick, 'dash');
      seg('recruiting research', R.cap.r, R.cap.r.map(function () { return cap; }), brick);
      seg('floor-entry research', R.floor.r, fy, grey, 'dashdot');
      seg('floor-entry research', R.floor_cap.r, R.floor_cap.r.map(function () { return fcap; }), grey, 'dashdot');
      var end = function (a) { return a[a.length - 1]; };
      traces.push(dot([end(R.floor.r)], [end(fy)], grey, true, P.x, P.y, 9));
      traces.push(dot([B.res_rR], [ys[0]], brick, false, P.x, P.y, 8));
      // the example strengths: r_0, the three middle strengths of B12 page 4 (both equilibria), r_N, r_1 and r_2
      var exr = ex.map(function (s) { return regNum('str_r' + s); });
      var exv = ex.map(function (s) { return regNum(j ? 'res_entry_r' + s : 'res_lambda_r' + s); });
      traces.push(dot([I.r0].concat(exr, [B.res_rN]), [zero, zero, zero, zero, zero], t.ink, false, P.x, P.y, 8));
      traces.push(dot(exr.concat([B.res_rcap, I.r1, I.r2]), exv.concat([cap, cap, j ? rho : cap]), t.ink, false, P.x, P.y, 8));
      [[B.res_rR, 'r<sub>R</sub>', 0], [B.res_rcap, 'r<sub>λ̄</sub>', 1], [B.res_rN, 'r<sub>N</sub>', 0], [B.res_rQ, 'r<sub>Q</sub>', 0], [B.res_rC, 'r<sub>C</sub>', 0]].forEach(function (mk) {
        layout.shapes.push(vline(mk[0], t.muted, 'dot', P.x));
        if (!j) layout.annotations.push({ text: mk[1].replace(/^r/, '<i>r</i>'), xref: P.x, x: mk[0], yref: P.y + ' domain', y: 1, yanchor: 'bottom', yshift: 4 + mk[2] * 15, xanchor: 'center', font: { size: 12, color: t.muted } });
      });
    });
    layout.shapes.push({ type: 'line', xref: 'x', yref: 'y', x0: I.r0, x1: B.res_rcap, y0: R.cap_value, y1: R.cap_value, line: { color: t.muted, width: 1.2, dash: 'dot' }, layer: 'below' });
    layout.annotations.push(at('zero', 1.22, 0, t.ink, { yshift: 6, size: 12 }));
    layout.annotations.push(at('recruiting', 2.3, R.cap_value, brick, { xanchor: 'center', yshift: 5, size: 12 }));
    layout.annotations.push(at('floor-entry', 2.2, 0.2, grey, { xanchor: 'left', size: 12 }));
    layout.annotations.push(at('zero', 1.22, I.rho, t.ink, { xref: 'x2', yref: 'y2', yanchor: 'top', yshift: -5, size: 12 }));
    layout.annotations.push(at('recruiting', 2.8, R.plateau, brick, { xref: 'x2', yref: 'y2', xanchor: 'center', yshift: 5, size: 12 }));
    layout.annotations.push(at('floor-entry', 2.2, I.rho + 0.05, grey, { xref: 'x2', yref: 'y2', xanchor: 'left', yshift: 0, size: 12 }));
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

  /* ---------- widgets: the four figures ---------- */
  widgets.beliefs = { render: function (s) { drawChart($('#beliefs', s), specBeliefs(tokens()), 'beliefs'); } };
  widgets.region = { render: function (s) { drawChart($('#region', s), specRegion(tokens()), 'region'); } };
  widgets.coex = { render: function (s) { drawChart($('#coex', s), specCoex(tokens()), 'coex'); } };
  widgets.research = { render: function (s) { drawChart($('#research', s), specResearch(tokens()), 'research'); } };

  function renderWidget(force) {
    var s = slides[index], w = widgets[s.dataset.widget];
    if (!w || !w.render) return;
    if (!force && s.dataset.rendered === '1' && !/^(beliefs|region|coex|research)$/.test(s.dataset.widget)) return;
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
    var gt = e.target.closest && e.target.closest('.goto[data-target], .xlink[data-target]');
    if (gt) { e.preventDefault(); follow(gt.dataset.target); return; }
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
