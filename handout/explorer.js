/* Explore the benchmark path of the order-slot version.
 *
 * A slider on incumbent strength r. At each r the widget lists the equilibria that Appendix A4 of
 * the manuscript gives on the benchmark path (prior 1/2; an indifferent investor may mix; an
 * indifferent high-cost challenger prepares), and for the chosen one it shows the posterior after
 * each order against the preparation threshold, entry and the price after each order, total entry
 * and high-class ownership. The chart below is Figure 3: entry along the whole path, every form.
 *
 * All arithmetic is CCC.slot in figures.js: the closed forms of the manuscript at the registry
 * declarations. The marked strengths are registry rows. Nothing here searches for an equilibrium.
 * ES2019, no modules. Exposes window.CCC.explorer.
 */
(function () {
  'use strict';

  var CCC = (window.CCC = window.CCC || {});
  var STEP = 0.005;
  var NAMES = { N: 'No informed trade', R: 'Mixed purchase that recruits', F: 'Full purchase', Q: 'Mixed orders at the floor' };
  var ORDERS = [['-1', 'Sale'], ['0', 'No order'], ['1', 'Purchase']];
  var state = { initialised: false, P: null, r: NaN, preset: null, sel: null, el: {}, rafPending: false, pendingR: NaN };

  function d6(v) { return isFinite(v) ? v.toFixed(6) : '—'; }
  function prob(v) {
    if (Math.abs(v - 1) < 1e-12) return 'probability one';
    if (Math.abs(v) < 1e-12) return 'probability zero';
    return 'probability ' + d6(v);
  }
  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text !== undefined && text !== null) e.textContent = String(text);
    return e;
  }
  function markup(tag, cls, html) { var e = el(tag, cls); e.innerHTML = html; return e; }
  function fmtR(v) { var s = v.toFixed(3); return s.charAt(s.length - 1) === '0' ? v.toFixed(2) : s; }

  /* ---------- the sentence that describes one form ---------- */
  function describe(f, P) {
    var low;
    if (f.t === 0) low = 'class <i>L</i> abstains';
    else if (Math.abs(f.sellL - 1) < 1e-12) low = 'class <i>L</i> sells with probability one';
    else low = 'class <i>L</i> sells with ' + prob(f.sellL);
    if (f.id === 'N') return 'Neither class trades. Every order leaves the posterior at the prior and has the same price, so only a zero-cost challenger prepares.';
    if (f.id === 'R') return 'Class <i>H</i> buys with ' + prob(f.buyH) + ' and otherwise abstains; ' + low + '. ' +
      (Math.abs(f.mu['1'] - f.A.tau) < 1e-9 ? 'A purchase just reaches the threshold and recruits a high-cost challenger; the purchase earns exactly the trading cost.'
        : 'A purchase lifts the posterior above the threshold and recruits a high-cost challenger.');
    if (f.id === 'Q') return 'Class <i>H</i> buys and class <i>L</i> sells, each with ' + prob(f.buyH) + '. The purchase posterior stays below the threshold, so no order recruits a high-cost challenger.';
    return 'Class <i>H</i> buys with probability one; ' + low + '. ' + (f.e['1'] === 1
      ? 'A purchase reaches the top posterior and recruits a high-cost challenger.'
      : 'Above the entry ceiling the top posterior falls short of the threshold, so no order recruits a high-cost challenger and entry is at its floor.');
  }

  /* ---------- the posterior after each order, on a belief line ---------- */
  function beliefLine(f, P) {
    var wide = !state.el.root || state.el.root.clientWidth > 560;
    var W = wide ? 640 : 380, H = 118, lo = 0.2, hi = 0.8, L = 16, R = 16, y = 70, gap = wide ? 52 : 40;
    function X(v) { return L + (v - lo) / (hi - lo) * (W - L - R); }
    var tau = f.A.tau, out = '';
    out += '<rect class="bl-band" x="' + X(P.m).toFixed(1) + '" y="' + (y - 16) + '" width="' + (X(P.M) - X(P.m)).toFixed(1) + '" height="32"/>';
    out += '<line class="bl-axis" x1="' + L + '" x2="' + (W - R) + '" y1="' + y + '" y2="' + y + '"/>';
    for (var v = lo; v <= hi + 1e-9; v += (wide ? 0.1 : 0.2)) {
      out += '<line class="bl-tick" x1="' + X(v).toFixed(1) + '" x2="' + X(v).toFixed(1) + '" y1="' + y + '" y2="' + (y + 5) + '"/>' +
        '<text class="bl-tick-label" x="' + X(v).toFixed(1) + '" y="' + (y + 19) + '" text-anchor="middle">' + v.toFixed(1) + '</text>';
    }
    out += '<line class="bl-tau" x1="' + X(tau).toFixed(1) + '" x2="' + X(tau).toFixed(1) + '" y1="' + (y - 30) + '" y2="' + (y + 8) + '"/>' +
      '<text class="bl-tau-label" x="' + X(tau).toFixed(1) + '" y="' + (y - 34) + '" text-anchor="middle">threshold τ(r)</text>';
    out += '<text class="bl-band-label" x="' + X(P.m).toFixed(1) + '" y="' + (y + 34) + '" text-anchor="start">m</text>' +
      '<text class="bl-band-label" x="' + X(P.M).toFixed(1) + '" y="' + (y + 34) + '" text-anchor="end">M</text>';
    var used = [];
    ORDERS.forEach(function (o, i) {
      var mu = f.mu[o[0]], x = X(mu), lift = 0;
      used.forEach(function (u) { if (Math.abs(u - x) < gap) lift += 1; });
      used.push(x);
      var cls = 'bl-mark ' + (o[0] === '1' ? (f.e['1'] === 1 ? 'bl-recruit' : 'bl-buy') : (o[0] === '-1' ? 'bl-sell' : 'bl-none'));
      var path = o[0] === '1' ? 'M' + x + ',' + (y - 8) + 'l7,12h-14z' : (o[0] === '-1' ? 'M' + x + ',' + (y + 8) + 'l7,-12h-14z' : '');
      out += path ? '<path class="' + cls + '" d="' + path + '"/>' : '<circle class="' + cls + '" cx="' + x.toFixed(1) + '" cy="' + y + '" r="6"/>';
      out += '<text class="bl-mark-label" x="' + x.toFixed(1) + '" y="' + (y - 14 - 13 * lift) + '" text-anchor="middle">' + o[1].toLowerCase() + '</text>';
    });
    return '<svg class="belief-line" viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="Posterior after each order against the threshold">' + out + '</svg>';
  }

  /* ---------- Figure 3: entry along the benchmark path ---------- */
  function path(D, t, opts) {
    var S = CCC.slot, P = S.inputs(D), narrow = !!(opts && opts.narrow), C = CCC.charts, ENT = S.plateau(P), traces = [];
    function seg(name, group, lo, hi, fy, color, dash, width, show, ax, ay, n) {
      var xs = S.grid(lo, hi, n || 80);
      return { type: 'scatter', mode: 'lines', name: name, legendgroup: group, showlegend: show, x: xs, y: xs.map(fy),
        line: { color: color, dash: dash || 'solid', width: width || 2.6 }, xaxis: ax, yaxis: ay,
        customdata: xs.map(function (r) { return [fy(r).toFixed(6)]; }), hovertemplate: 'entry = %{customdata[0]}<extra>' + group + '</extra>' };
    }
    function dot(x, y, color, open, ax, ay, key, size, symbol) {
      return { type: 'scatter', mode: 'markers', name: key, showlegend: false, x: [x], y: [y], xaxis: ax, yaxis: ay,
        marker: { symbol: symbol || (open ? 'circle-open' : 'circle'), size: size || 8, color: color }, hovertemplate: 'skip' };
    }
    [['x', 'y', true], ['x2', 'y2', false]].forEach(function (p) {
      var ax = p[0], ay = p[1], show = p[2];
      traces.push(seg('N: no informed trade', 'N', P.r0, P.rN, function () { return P.rho; }, t.ink, 'solid', 2.6, show, ax, ay));
      traces.push(seg('R: mixed purchase that recruits', 'R', P.rA, P.rF, function (r) { return S.entryR(P, r); }, t.info, 'dash', 2.6, show, ax, ay));
      traces.push(seg('F: full purchase', 'F', P.rF, P.rC, function () { return ENT; }, t.info, 'solid', 2.6, show, ax, ay, 160));
      traces.push(seg('F: full purchase', 'F', P.rC, P.r2, function () { return P.rho; }, t.info, 'solid', 2.6, false, ax, ay, 20));
      traces.push(seg('Q: mixed orders at the floor', 'Q', P.rN, P.rJ, function () { return P.rho; }, t.c3, 'dashdot', 2.6, show, ax, ay));
      traces.push(seg('T: threshold branch (if an indifferent challenger may mix)', 'T', P.rA, P.rJ, function (r) { return S.entryT(P, r); }, t.muted, 'dash', 1.2, show, ax, ay));
      traces.push(dot(P.rA, P.entry_rA, t.info, false, ax, ay, 'R'));
      traces.push(dot(P.rF, ENT, t.info, false, ax, ay, 'F'));
      traces.push(dot(P.rC, ENT, t.info, false, ax, ay, 'F'));
      traces.push(dot(P.rC, P.rho, t.info, true, ax, ay, 'F'));
      // Q excludes both endpoints (large open circles); T, under challenger mixing, includes r_J;
      // N includes r_N, so its filled marker is drawn last, inside Q's open circle.
      traces.push(dot(P.rN, P.rho, t.c3, true, ax, ay, 'Q', 12));
      traces.push(dot(P.rJ, P.rho, t.c3, true, ax, ay, 'Q', 12));
      traces.push(dot(P.rJ, P.rho, t.muted, false, ax, ay, 'T', 7, 'diamond'));
      traces.push(dot(P.rN, P.rho, t.ink, false, ax, ay, 'N', 6));
    });
    var r = isFinite(state.r) ? state.r : P.r0;
    var eqs = S.equilibria(P, r);
    var layout = C.baseLayout(t);
    layout.height = narrow ? 640 : 400;
    layout.margin.t = 46;
    layout.xaxis = C.axis(t, { title: { text: 'incumbent strength <i>r</i>' }, range: [P.r0, P.r2], tickvals: [1.2, 1.6, 2, 2.4, 2.8, 3.2, 3.6] });
    layout.yaxis = C.axis(t, { title: { text: 'entry' }, range: [0.15, 0.62], tickvals: [0.2, 0.3, 0.4, 0.5, 0.6] });
    layout.xaxis2 = C.axis(t, { title: { text: 'incumbent strength <i>r</i>' }, range: [1.25, 2.35], tickvals: [1.4, 1.6, 1.8, 2, 2.2] });
    layout.yaxis2 = C.axis(t, { title: { text: 'entry' }, range: [0.12, 0.62], tickvals: [0.2, 0.3, 0.4, 0.5, 0.6] });
    layout.margin.l = 64;
    C.twoPanels(layout, narrow);
    if (!narrow) { layout.xaxis.domain = [0, 0.36]; layout.xaxis2.domain = [0.46, 1]; }
    ['x', 'x2'].forEach(function (ax) {
      var ay = ax === 'x2' ? 'y2' : 'y';
      layout.shapes.push({ type: 'rect', xref: ax, yref: ay + ' domain', x0: P.rA, x1: P.rN, y0: 0, y1: 1, fillcolor: t.regionB, line: { width: 0 }, layer: 'below' });
      var marks = ax === 'x' ? [['rA', 'A', 0], ['rN', 'N', 1], ['rC', 'C', 0]] : [['rA', 'A', 0], ['rF', 'F', 1], ['rN', 'N', 0], ['rJ', 'J', 1], ['rS', 'S', 0]];
      marks.forEach(function (m) {
        layout.shapes.push({ type: 'line', xref: ax, yref: ay + ' domain', x0: P[m[0]], x1: P[m[0]], y0: 0, y1: 1, line: { color: t.line, width: 1, dash: '2 3' }, layer: 'below' });
        layout.annotations.push({ text: '<i>r</i><sub>' + m[1] + '</sub>', showarrow: false, xref: ax, yref: ay + ' domain', x: P[m[0]], y: 1,
          xanchor: 'center', yanchor: 'bottom', yshift: 2 + 15 * m[2], font: { size: 11, color: t.muted }, hovertext: 'r_' + m[1] + ' = ' + P.display[m[0]] });
      });
      layout.shapes.push({ type: 'line', xref: ax, yref: ay + ' domain', x0: r, x1: r, y0: 0, y1: 1, line: { color: t.ink, width: 1.4 } });
    });
    layout.annotations.push({ text: 'T endpoint (challenger mixing)', showarrow: false, xref: 'x2', yref: 'y2', x: P.rJ, y: P.rho,
      xanchor: 'center', yanchor: 'top', yshift: -9, font: { size: 10, color: t.muted } });
    layout.annotations.push({ text: 'coexistence', showarrow: false, xref: 'x2', yref: 'y2', x: (P.rA + P.rN) / 2, y: 0.135, xanchor: 'center', yanchor: 'bottom', font: { size: 11, color: t.muted } });
    eqs.forEach(function (f) {
      var color = f.id === 'N' ? t.ink : (f.id === 'Q' ? t.c3 : t.info);
      ['x', 'x2'].forEach(function (ax) {
        traces.push({ type: 'scatter', mode: 'markers', name: 'at r: ' + f.id, showlegend: false, x: [r], y: [f.E], xaxis: ax, yaxis: ax === 'x2' ? 'y2' : 'y',
          marker: { symbol: 'diamond', size: 11, color: color, line: { color: t.bg, width: 1.5 } }, customdata: [[f.E.toFixed(6)]],
          hovertemplate: 'entry = %{customdata[0]}<extra>' + NAMES[f.id] + ' at the chosen r</extra>' });
      });
    });
    C.panelLabels(layout, t);
    return { traces: traces, layout: layout };
  }

  /* ---------- DOM ---------- */
  /* Named presets set the exact registry strength. sub: the symbol's subscript (none for a plain
     strength); exact: whether the registry display is the exact value (a declared fraction) or a
     rounded root, printed with an approximation sign. */
  function presets(P) {
    return [{ sub: '0', key: 'r0', exact: true }, { sub: 'A', key: 'rA', exact: false }, { sub: '', key: 'r160', exact: true },
      { sub: 'N', key: 'rN', exact: false }, { sub: 'S', key: 'rS', exact: false }, { sub: '1', key: 'r1', exact: true },
      { sub: 'C', key: 'rC', exact: false }, { sub: '2', key: 'r2', exact: true }].map(function (p) {
      p.value = P[p.key];
      p.display = P.display[p.key];
      return p;
    });
  }
  function presetLabel(p, html) {
    var sym = p.sub ? (html ? '<i>r</i><sub>' + p.sub + '</sub>' : 'r_' + p.sub) : '';
    var r = html ? '<i>r</i>' : 'r', rel = p.exact ? ' = ' : ' ≈ ';
    return sym ? r + ' = ' + sym + rel + p.display : r + ' = ' + p.display;
  }

  function buildDOM(root) {
    var P = state.P;
    root.classList.add('explorer');
    while (root.firstChild) root.removeChild(root.firstChild);
    var head = el('div', 'explorer-head');
    head.appendChild(el('span', 'explorer-title', 'Explore the benchmark path'));
    root.appendChild(head);

    var controls = el('div', 'explorer-controls');
    var lab = el('label', 'explorer-label', 'Incumbent strength r');
    lab.setAttribute('for', 'explorer-r');
    controls.appendChild(lab);
    var range = document.createElement('input');
    // step "any": a named preset keeps its exact registry strength; free movement snaps to a STEP grid in JS.
    range.type = 'range'; range.id = 'explorer-r'; range.min = String(P.r0); range.max = String(P.r2); range.step = 'any';
    range.value = String(P.r160);
    controls.appendChild(range);
    var out = el('output', 'live explorer-r-value', '');
    out.setAttribute('for', 'explorer-r');
    controls.appendChild(out);
    var pre = el('div', 'explorer-presets');
    presets(P).forEach(function (p) {
      var b = markup('button', 'preset', p.sub ? '<i>r</i><sub>' + p.sub + '</sub>' : '<i>r</i> = ' + p.display);
      b.type = 'button';
      b.title = presetLabel(p, false);
      b.addEventListener('click', function () { setR(p.value, p); });
      pre.appendChild(b);
    });
    controls.appendChild(pre);
    root.appendChild(controls);

    var readouts = el('div', 'explorer-readouts'), cells = {};
    [['Delta', 'Δ<sub>T</sub>(r)'], ['gH', 'g<sub>H</sub>'], ['gL', 'g<sub>L</sub>'], ['Bhalf', 'B<sub>r</sub>(1/2)'], ['BM', 'B<sub>r</sub>(M)'], ['tau', 'τ(r)']].forEach(function (c) {
      var cell = el('div', 'readout');
      cell.appendChild(markup('span', 'readout-label', c[1]));
      var v = el('span', 'live readout-value', '');
      cell.appendChild(v);
      readouts.appendChild(cell);
      cells[c[0]] = v;
    });
    root.appendChild(readouts);

    var picker = el('div', 'eq-picker');
    picker.setAttribute('role', 'group');
    picker.setAttribute('aria-label', 'Equilibria at this strength');
    root.appendChild(picker);
    var detail = el('div', 'eq-detail');
    detail.setAttribute('aria-live', 'polite');
    root.appendChild(detail);

    var fig = el('figure', 'chart explorer-figure');
    fig.tabIndex = 0;
    var mount = el('div', 'chart-mount');
    mount.id = 'chart-explorer';
    mount.setAttribute('aria-label', 'Entry against incumbent strength in every equilibrium of the benchmark path');
    fig.appendChild(mount);
    fig.appendChild(markup('figcaption', '', '<strong>Figure 3.</strong> Entry along the benchmark path at the prior 1/2, in every equilibrium. Panel (a) covers the path from <i>r</i><sub>0</sub> to <i>r</i><sub>2</sub>; panel (b) enlarges the strengths around the shaded coexistence interval from <i>r</i><sub>A</sub> to <i>r</i><sub>N</sub>. N has no informed trade, R is a mixed purchase that recruits, F a full high-class purchase (the low class abstains up to <i>r</i><sub>N</sub>, mixes up to <i>r</i><sub>S</sub>, then sells), Q mixed orders without recruitment. The thin dashed T branch exists only when an indifferent high-cost challenger may prepare with any probability. Filled markers belong to a branch and open markers do not: N includes its endpoint at <i>r</i><sub>N</sub>; Q excludes both endpoints. Under challenger mixing, T includes its endpoint at <i>r</i><sub>J</sub>. The vertical line and the diamonds at the chosen strength follow the slider.'));
    root.appendChild(fig);

    state.el = { root: root, range: range, out: out, cells: cells, picker: picker, detail: detail, mount: mount };
    range.addEventListener('input', function () { schedule(snap(Number(range.value))); });
    range.addEventListener('change', function () { schedule(snap(Number(range.value))); });
    picker.addEventListener('click', function (ev) {
      var b = ev.target.closest ? ev.target.closest('button[data-eq]') : null;
      if (!b) return;
      state.sel = b.getAttribute('data-eq');
      render(state.r);
    });
  }

  function render(r) {
    var S = CCC.slot, P = state.P, E = state.el;
    state.r = r;
    if (state.preset && state.preset.value !== r) state.preset = null;
    var A = S.auction(P, r), eqs = S.equilibria(P, r);
    var shown = state.preset ? presetLabel(state.preset, false) : 'r = ' + fmtR(r);
    E.out.innerHTML = state.preset ? presetLabel(state.preset, true) : fmtR(r);
    E.out.title = shown;
    if (E.range.value !== String(r)) E.range.value = String(r);
    E.range.setAttribute('aria-valuetext', shown);
    E.cells.Delta.textContent = d6(A.Delta);
    E.cells.gH.textContent = d6(A.gH);
    E.cells.gL.textContent = d6(A.gL);
    E.cells.Bhalf.textContent = d6(A.B(0.5));
    E.cells.BM.textContent = d6(A.B(P.M));
    E.cells.tau.textContent = d6(A.tau);
    if (!eqs.some(function (f) { return f.id === state.sel; })) state.sel = eqs.length ? eqs[eqs.length - 1].id : null;
    E.picker.innerHTML = '<span class="eq-picker-label">' + (eqs.length > 1 ? eqs.length + ' equilibria at this strength' : 'One equilibrium at this strength') + '</span>' +
      eqs.map(function (f) {
        return '<button type="button" data-eq="' + f.id + '" aria-pressed="' + (f.id === state.sel ? 'true' : 'false') + '"><b>' + f.id + '</b> ' + NAMES[f.id] + '</button>';
      }).join('');
    var f = eqs.filter(function (x) { return x.id === state.sel; })[0];
    if (!f) { E.detail.innerHTML = ''; moveMarker(); return; }
    var rows = ORDERS.map(function (o) {
      var x = o[0];
      return '<tr><th scope="row">' + o[1] + '</th><td class="num">' + d6(f.fH[x]) + '</td><td class="num">' + d6(f.fL[x]) + '</td><td class="num">' + d6(f.mu[x]) +
        '</td><td class="num">' + (f.e[x] === 1 ? '1' : d6(f.e[x])) + '</td><td class="num">' + d6(f.price[x]) + '</td></tr>';
    }).join('');
    E.detail.innerHTML = '<p class="eq-summary">' + describe(f, P) + '</p>' + beliefLine(f, P) +
      '<div class="table-wrap"><table class="eq-table"><thead><tr><th>Order</th><th class="num">Probability, class <i>H</i></th><th class="num">Probability, class <i>L</i></th>' +
      '<th class="num">Posterior μ</th><th class="num">Entry</th><th class="num">Price</th></tr></thead><tbody>' + rows + '</tbody></table></div>' +
      '<p class="eq-totals"><span>Entry <b class="live">' + d6(f.E) + '</b></span><span>High-class ownership <b class="live">' + d6(f.O_H) + '</b></span>' +
      '<span>Gross profit at the top posterior <b class="live">' + d6(A.B(P.M)) + '</b> against the high cost <b>' + P.display.c_H + '</b></span></p>';
    moveMarker();
  }

  function moveMarker() {
    if (!CCC.charts || typeof CCC.charts.update !== 'function') return;
    try { CCC.charts.update('explorer'); } catch (e) { /* not mounted yet */ }
  }

  /* A dragged value snaps to the STEP grid from r_0, so the printed strength is the computed one. */
  function snap(v) {
    var P = state.P;
    var g = Math.round((Math.round((v - P.r0) / STEP) * STEP + P.r0) * 1000) / 1000;
    state.preset = null;
    state.el.range.value = String(g);
    return g;
  }

  function schedule(r) {
    state.pendingR = r;
    if (state.rafPending) return;
    state.rafPending = true;
    window.requestAnimationFrame(function () { state.rafPending = false; render(state.pendingR); });
  }

  function setR(r, preset) {
    var v = Math.min(state.P.r2, Math.max(state.P.r0, Number(r)));
    if (!isFinite(v)) return;
    state.preset = preset && preset.value === v ? preset : null;
    state.el.range.value = String(v);
    render(v);
  }

  var lastWide = null;
  window.addEventListener('resize', function () {
    if (!state.initialised) return;
    var wide = state.el.root.clientWidth > 560;
    if (wide !== lastWide) { lastWide = wide; render(state.r); }
  });

  function init() {
    if (state.initialised) return;
    var root = document.getElementById('explorer');
    if (!root || !CCC.slot) return;
    state.P = CCC.slot.inputs();
    buildDOM(root);
    setR(state.P.r160, presets(state.P).filter(function (p) { return p.key === 'r160'; })[0]);
    if (CCC.charts && typeof CCC.charts.register === 'function') {
      CCC.charts.register('explorer', path, 3);
      CCC.charts.mount('explorer');
    }
    state.initialised = true;
  }

  function status() {
    var st = CCC.charts && CCC.charts.status ? CCC.charts.status().explorer : null;
    return { initialised: state.initialised, r: state.r, selected: state.sel, mounted: !!(st && st.mounted) };
  }

  CCC.explorer = { init: init, setR: setR, status: status, path: path, select: function (id) { state.sel = id; render(state.r); } };
})();
