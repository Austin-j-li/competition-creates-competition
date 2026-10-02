/* Explore incumbent strength for the handout.
 *
 * Shared formula block (keep byte-identical with the docstring in handout/crosscheck.py):
 *
 *   t_0 = p (1 - p/r);  t_H = r/2 + p^2/(2r);  t_L = ell - (ell^2 - p^2)/(2r)
 *   g_H = h - r/2 - p^2/(2r);  g_L = (ell^2 - p^2)/(2r);  Delta_T = (r - ell)^2/(2r)
 *   m = 1/(1 + exp(2/b));  M = 1 - m;  B(mu) = g_L + mu (g_H - g_L)
 *   tau = (c_H - g_L)/(g_H - g_L)
 *     c_H > B(M): E = rho, O_H = rho/2, x* = +inf, alpha_H = alpha_L = 0
 *     c_H <= B(m): x* = -inf, alpha_H = alpha_L = 1, E = 1, O_H = 1/2
 *     otherwise  : x* = (b/2) log(tau/(1-tau)); alpha_H = S_Laplace(x*-1); alpha_L = S_Laplace(x*+1)
 *                  E = rho + (1-rho)/2 (alpha_H + alpha_L);  O_H = (rho + (1-rho) alpha_H)/2
 *   chips: A1 = B(m) - c_L; A2a = c_H - B(1/2); A2b = B(M) - c_H;
 *          A3_no_trade = k - Delta_T; A3_full = (1 - 1/b) rho m Delta_T - k
 *   rr(d) = ell + d + sqrt(d^2 + 2 ell d); r_k = rr(k); r_N = rr(2k/rho); r_U = rr(k/((1-1/b) rho m))
 *   r_C = (M h - c_H + sqrt((M h - c_H)^2 + M ((1-M) ell^2 - p^2))) / M
 *
 * Sources: paper/main.md eq. (4), (7), (12), conditions (A1) to (A3), and (A.1), (A.2).
 * This is arithmetic on the sufficient conditions of Proposition 2 and the full-order
 * candidate (12) at the benchmark primitives with only r moving. It never solves for an
 * equilibrium; validated branches live in window.CCC_DATA.fig2 (Figure 2).
 * ES2019, no modules. Exposes window.CCC.explorer.
 */
(function () {
  'use strict';

  var TOL = 1e-9;
  var R_MIN = 1.0;
  var R_MAX = 3.8;
  var R_STEP = 0.005;

  var CCC = (window.CCC = window.CCC || {});
  var state = {
    initialised: false,
    P: null,
    r: NaN,
    lastSelfTest: null,
    el: {},
    markerIndex: -1,
    rafPending: false,
    pendingR: NaN,
    mounted: false
  };

  /* ---------- inputs ---------- */

  function readInputs() {
    var D = window.CCC_DATA || {};
    var src = D.inputs || {};
    var keys = ['h', 'ell', 'p', 'rho', 'c_L', 'c_H', 'b', 'k', 'r_weak', 'r_strong', 'r_collapse'];
    var P = {};
    for (var i = 0; i < keys.length; i++) {
      P[keys[i]] = Number(src[keys[i]]);
      if (!isFinite(P[keys[i]])) {
        throw new Error('[ccc] explorer: missing or non-numeric input ' + keys[i]);
      }
    }
    return P;
  }

  /* ---------- closed forms ---------- */

  function closedForms(P, r) {
    var h = P.h, ell = P.ell, p = P.p, rho = P.rho, c_L = P.c_L, c_H = P.c_H, b = P.b, k = P.k;
    var inDomain = p < ell && ell < r && r < h;
    var t_0 = p * (1 - p / r);
    var t_H = r / 2 + p * p / (2 * r);
    var t_L = ell - (ell * ell - p * p) / (2 * r);
    var g_H = h - r / 2 - p * p / (2 * r);
    var g_L = (ell * ell - p * p) / (2 * r);
    var Delta_T = (r - ell) * (r - ell) / (2 * r);
    var m = 1 / (1 + Math.exp(2 / b));
    var M = 1 - m;
    var B = function (mu) { return g_L + mu * (g_H - g_L); };
    var tau = (c_H - g_L) / (g_H - g_L);
    var x_star, alpha_H, alpha_L;
    if (c_H > B(M)) {
      x_star = Infinity; alpha_H = 0; alpha_L = 0;
    } else if (c_H <= B(m)) {
      x_star = -Infinity; alpha_H = 1; alpha_L = 1;
    } else {
      x_star = (b / 2) * Math.log(tau / (1 - tau));
      alpha_H = x_star <= 1 ? 1 - Math.exp((x_star - 1) / b) / 2 : Math.exp(-(x_star - 1) / b) / 2;
      alpha_L = x_star <= -1 ? 1 - Math.exp((x_star + 1) / b) / 2 : Math.exp(-(x_star + 1) / b) / 2;
    }
    var E = rho + (1 - rho) / 2 * (alpha_H + alpha_L);
    var O_H = (rho + (1 - rho) * alpha_H) / 2;
    var rr = function (d) { return ell + d + Math.sqrt(d * d + 2 * ell * d); };
    var r_k = rr(k);
    var r_N = rr(2 * k / rho);
    var r_U = rr(k / ((1 - 1 / b) * rho * m));
    var disc = (M * h - c_H) * (M * h - c_H) + M * ((1 - M) * ell * ell - p * p);
    var r_C = disc >= 0 ? (M * h - c_H + Math.sqrt(disc)) / M : NaN;
    var chips = {
      A1: { ok: c_L < B(m), margin: B(m) - c_L },
      A2a: { ok: B(0.5) < c_H, margin: c_H - B(0.5) },
      A2b: { ok: c_H < B(M), margin: B(M) - c_H },
      A3_no_trade: { ok: Delta_T < k, margin: k - Delta_T },
      A3_full: { ok: (1 - 1 / b) * rho * m * Delta_T > k, margin: (1 - 1 / b) * rho * m * Delta_T - k }
    };
    return {
      r: r, inDomain: inDomain,
      t_0: t_0, t_H: t_H, t_L: t_L, g_H: g_H, g_L: g_L, Delta_T: Delta_T,
      m: m, M: M, B_m: B(m), B_prior: B(0.5), B_M: B(M),
      tau: tau, x_star: x_star, alpha_H: alpha_H, alpha_L: alpha_L, E: E, O_H: O_H,
      chips: chips, r_k: r_k, r_N: r_N, r_U: r_U, r_C: r_C
    };
  }

  /* ---------- formatting ---------- */

  function fmt6(v) {
    if (v === Infinity) return '∞';
    if (v === -Infinity) return '−∞';
    if (typeof v !== 'number' || isNaN(v)) return '—';
    return v.toFixed(6);
  }

  function fmtSigned(v) {
    if (!isFinite(v)) return fmt6(v);
    var s = fmt3(Math.abs(v));
    return (v < 0 ? '−' : '+') + s;
  }

  /* Display-only rounding; the exact value stays in each node's title attribute.
     Three decimals, or three significant digits for magnitudes below 0.01 so that a
     small nonzero margin never reads as zero. */
  function fmt3(v) {
    if (typeof v !== 'number' || !isFinite(v)) return fmt6(v);
    var a = Math.abs(v);
    if (a !== 0 && a < 0.01) return v.toPrecision(3);
    return v.toFixed(3);
  }

  /* Slider value: two decimals, a third only when the 0.005 step needs it. */
  function fmtR(v) {
    if (typeof v !== 'number' || !isFinite(v)) return fmt6(v);
    var s = v.toFixed(3);
    return s.charAt(s.length - 1) === '0' ? v.toFixed(2) : s;
  }

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text !== undefined && text !== null) e.textContent = String(text);
    return e;
  }

  /* ---------- tokens and layout helpers (fall back if charts.js lacks them) ---------- */

  var TOKEN_DEFAULTS = {
    '--bg': '#ffffff', '--surface': '#f7f7fa', '--ink': '#161616', '--muted': '#6b6b76',
    '--grid': '#e6e6ec', '--line': '#d8d8e0', '--accent': '#5b3df5', '--accent-soft': '#ece7ff',
    '--c2': '#c98a1b', '--c3': '#5f6b7a', '--region-a': 'rgba(91,61,245,0.08)',
    '--region-b': 'rgba(201,138,27,0.10)', '--region-c': 'rgba(95,107,122,0.10)',
    '--font-sans': 'ui-sans-serif, -apple-system, "Segoe UI", Roboto, sans-serif',
    '--font-mono': 'ui-monospace, SFMono-Regular, Menlo, monospace'
  };

  function tokens() {
    if (CCC.charts && typeof CCC.charts.tokens === 'function') {
      try { return CCC.charts.tokens(); } catch (e) { /* fall through */ }
    }
    var cs = getComputedStyle(document.documentElement);
    var t = {};
    Object.keys(TOKEN_DEFAULTS).forEach(function (name) {
      var v = cs.getPropertyValue(name).trim();
      t[name.slice(2).replace(/-([a-z0-9])/g, function (_, c) { return c.toUpperCase(); })] = v || TOKEN_DEFAULTS[name];
    });
    return t;
  }

  function tok(t, key, fallbackVar) {
    if (t && t[key] !== undefined) return t[key];
    var alt = key.replace(/[A-Z0-9]/g, function (c) { return '-' + c.toLowerCase(); });
    if (t && t[alt] !== undefined) return t[alt];
    return TOKEN_DEFAULTS[fallbackVar];
  }

  function baseLayout(t) {
    if (CCC.charts && typeof CCC.charts.baseLayout === 'function') {
      try { return CCC.charts.baseLayout(t); } catch (e) { /* fall through */ }
    }
    var ink = tok(t, 'ink', '--ink'), grid = tok(t, 'grid', '--grid'), muted = tok(t, 'muted', '--muted');
    return {
      paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
      font: { family: tok(t, 'fontSans', '--font-sans'), color: ink, size: 13 },
      margin: { l: 56, r: 16, t: 28, b: 48 },
      xaxis: { gridcolor: grid, zeroline: false, ticks: 'outside', tickcolor: grid, linecolor: grid, color: muted, title: { font: { color: ink } } },
      yaxis: { gridcolor: grid, zeroline: false, ticks: 'outside', tickcolor: grid, linecolor: grid, color: muted, title: { font: { color: ink } } },
      hoverlabel: { font: { family: tok(t, 'fontSans', '--font-sans') } },
      uirevision: 'ccc'
    };
  }

  function brokenSeries(xs, ys, gap, jump) {
    if (CCC.charts && typeof CCC.charts.brokenSeries === 'function') {
      try { return CCC.charts.brokenSeries(xs, ys, gap, jump); } catch (e) { /* fall through */ }
    }
    var X = [], Y = [];
    for (var i = 0; i < xs.length; i++) {
      if (i > 0) {
        var dx = xs[i] - xs[i - 1];
        var dy = Math.abs(ys[i] - ys[i - 1]);
        if (dx > gap || dy > jump) { X.push(xs[i - 1] + dx / 2); Y.push(null); }
      }
      X.push(xs[i]); Y.push(ys[i]);
    }
    return { x: X, y: Y };
  }

  /* ---------- chart builder ---------- */

  function rGrid() {
    var xs = [];
    var n = Math.round((R_MAX - R_MIN) / R_STEP);
    for (var i = 0; i <= n; i++) {
      var r = Math.round((R_MIN + i * R_STEP) * 1000) / 1000;
      if (r > state.P.ell) xs.push(r);
    }
    return xs;
  }

  function builder(D, t, opts) {
    var narrow = !!(opts && opts.narrow);
    var P = state.P;
    var xs = rGrid();
    var Es = [], hover = [];
    for (var i = 0; i < xs.length; i++) {
      var cf = closedForms(P, xs[i]);
      Es.push(cf.E);
      hover.push('τ = ' + fmt6(cf.tau) + '<br>x* = ' + fmt6(cf.x_star) +
        '<br>α_H = ' + fmt6(cf.alpha_H) + '<br>α_L = ' + fmt6(cf.alpha_L));
    }
    var b0 = closedForms(P, P.r_strong);
    var broken = brokenSeries(xs, Es, R_STEP * 1.5, 0.02);
    var hoverBroken = [];
    for (var j = 0, k2 = 0; j < broken.x.length; j++) {
      if (broken.y[j] === null) { hoverBroken.push(''); } else { hoverBroken.push(hover[k2++]); }
    }
    var accent = tok(t, 'accent', '--accent'), c2 = tok(t, 'c2', '--c2'), c3 = tok(t, 'c3', '--c3');
    var muted = tok(t, 'muted', '--muted'), ink = tok(t, 'ink', '--ink');
    var traces = [
      {
        type: 'scatter', mode: 'lines', name: 'full-order candidate E(r), eq. (12)',
        x: broken.x, y: broken.y, connectgaps: false,
        line: { color: accent, width: 2, dash: 'dash' },
        customdata: hoverBroken,
        hovertemplate: 'E = %{y:.6f}<br>%{customdata}<extra></extra>'
      },
      {
        type: 'scatter', mode: 'lines', name: 'entry floor ρ',
        x: [R_MIN, R_MAX], y: [P.rho, P.rho],
        line: { color: c3, width: 1.4, dash: 'dot' },
        hovertemplate: 'ρ = %{y:.6f}<extra></extra>'
      }
    ];
    var fo = D && D.fig2 && D.fig2.branches && D.fig2.branches.full_orders;
    if (fo && fo.r && fo.E) {
      traces.push({
        type: 'scatter', mode: 'markers', name: 'accepted full-order branch (Figure 2)',
        x: fo.r, y: fo.E,
        marker: { color: c2, size: 4, opacity: 0.75 },
        hovertemplate: 'accepted E = %{y:.6f}<extra></extra>'
      });
    }
    var layout = baseLayout(t);
    layout.height = 450;
    layout.xaxis = Object.assign({}, layout.xaxis, {
      title: { text: 'Incumbent strength r', font: { color: ink } }, range: [R_MIN, R_MAX],
      tickvals: [1.0, 1.5, 2.0, 2.5, 3.0, 3.5]
    });
    layout.yaxis = Object.assign({}, layout.yaxis, {
      title: { text: 'entry E under full orders', font: { color: ink } }, range: [0.12, 0.60],
      tickvals: [0.25, 0.35, 0.45, 0.55]
    });
    layout.hovermode = 'x unified';
    layout.showlegend = true;
    layout.legend = { orientation: 'h', x: 0, y: 1.08, yanchor: 'bottom', font: { size: 11, color: muted }, bgcolor: 'rgba(0,0,0,0)' };
    layout.margin = Object.assign({}, layout.margin, { t: narrow ? 110 : 80 });
    var regA = tok(t, 'regionA', '--region-a'), regB = tok(t, 'regionB', '--region-b');
    var shapes = [
      { type: 'rect', xref: 'x', yref: 'paper', x0: R_MIN, x1: b0.r_k, y0: 0, y1: 1, fillcolor: regA, line: { width: 0 }, layer: 'below' },
      { type: 'rect', xref: 'x', yref: 'paper', x0: b0.r_U, x1: R_MAX, y0: 0, y1: 1, fillcolor: regB, line: { width: 0 }, layer: 'below' },
      { type: 'line', xref: 'x', yref: 'paper', x0: b0.r_C, x1: b0.r_C, y0: 0, y1: 1, line: { color: muted, width: 1, dash: 'dot' }, layer: 'below' }
    ];
    var rNow = isFinite(state.r) ? state.r : P.r_weak;
    shapes.push({ type: 'line', xref: 'x', yref: 'paper', x0: rNow, x1: rNow, y0: 0, y1: 1, line: { color: ink, width: 1.2 } });
    state.markerIndex = shapes.length - 1;
    layout.shapes = shapes;
    layout.annotations = [
      { xref: 'x', yref: 'paper', x: (R_MIN + b0.r_k) / 2, y: 0.03, text: 'Δ<sub>T</sub> &lt; k', showarrow: false, font: { size: 10, color: muted } },
      { xref: 'x', yref: 'paper', x: (b0.r_U + b0.r_C) / 2, y: 0.03, text: '(1−1/b)ρmΔ<sub>T</sub> &gt; k', showarrow: false, font: { size: 10, color: muted } },
      { xref: 'x', yref: 'paper', x: b0.r_C, y: 1.0, text: 'r<sub>C</sub>', showarrow: false, xanchor: 'left', yanchor: 'bottom', font: { size: 11, color: muted } }
    ];
    return { traces: traces, layout: layout };
  }

  /* ---------- DOM ---------- */

  var READOUTS = [
    ['t_0', 't₀'], ['t_H', 'tʜ'], ['t_L', 'tʟ'], ['g_H', 'gʜ'], ['g_L', 'gʟ'], ['Delta_T', 'Δᴛ'],
    ['B_m', 'Bᵣ(m)'], ['B_prior', 'Bᵣ(1/2)'], ['B_M', 'Bᵣ(M)'],
    ['tau', 'τ'], ['x_star', 'x*'], ['alpha_H', 'αʜ'], ['alpha_L', 'αʟ'], ['E', 'E'], ['O_H', 'Oʜ']
  ];

  var CHIPS = [
    ['A1', '(A1) cʟ < Bᵣ(m)'],
    ['A2a', '(A2) Bᵣ(1/2) < cʜ'],
    ['A2b', '(A2) cʜ < Bᵣ(M)'],
    ['A3_no_trade', '(A3) no trade: Δᴛ < k'],
    ['A3_full', '(A3) full orders: (1−1/b)ρmΔᴛ > k']
  ];

  var BOUNDS = [['r_k', 'r(k)'], ['r_N', 'rɴ'], ['r_U', 'rᴜ'], ['r_C', 'rᴄ']];

  function buildDOM(root) {
    var P = state.P;
    root.classList.add('explorer');
    while (root.firstChild) root.removeChild(root.firstChild);

    var head = el('div', 'explorer-head');
    head.appendChild(el('span', 'explorer-title', 'Explore incumbent strength'));
    var badge = el('span', 'badge');
    badge.hidden = true;
    head.appendChild(badge);
    root.appendChild(head);

    var controls = el('div', 'explorer-controls');
    var label = el('label', 'explorer-label', 'Incumbent strength r');
    label.setAttribute('for', 'explorer-r');
    controls.appendChild(label);
    var range = document.createElement('input');
    range.type = 'range'; range.id = 'explorer-r'; range.min = String(R_MIN); range.max = String(R_MAX);
    range.step = String(R_STEP); range.value = String(P.r_weak);
    range.setAttribute('aria-label', 'Incumbent strength r');
    controls.appendChild(range);
    var rValue = el('output', 'live explorer-r-value', fmtR(P.r_weak));
    rValue.title = String(P.r_weak);
    rValue.setAttribute('for', 'explorer-r');
    controls.appendChild(rValue);
    var presets = el('div', 'explorer-presets');
    [['r = ' + P.r_weak, P.r_weak], ['r = ' + P.r_strong, P.r_strong], ['r = ' + P.r_collapse, P.r_collapse]].forEach(function (pr) {
      var btn = el('button', 'preset', pr[0]);
      btn.type = 'button';
      btn.addEventListener('click', function () { setR(pr[1]); });
      presets.appendChild(btn);
    });
    var resetBtn = el('button', 'preset reset', 'Reset');
    resetBtn.type = 'button';
    resetBtn.addEventListener('click', reset);
    presets.appendChild(resetBtn);
    controls.appendChild(presets);
    root.appendChild(controls);

    var warn = el('p', 'explorer-warning', 'outside the maintained ordering (1): p < ℓ < r < h');
    warn.hidden = true;
    root.appendChild(warn);

    var readouts = el('div', 'explorer-readouts');
    var readoutEls = {};
    READOUTS.forEach(function (pair) {
      var cell = el('div', 'readout');
      cell.appendChild(el('span', 'readout-label', pair[1]));
      var v = el('span', 'live readout-value', '');
      cell.appendChild(v);
      readouts.appendChild(cell);
      readoutEls[pair[0]] = v;
    });
    root.appendChild(readouts);

    var chips = el('div', 'explorer-chips');
    var chipEls = {};
    CHIPS.forEach(function (pair) {
      var c = el('span', 'chip na', pair[1]);
      chips.appendChild(c);
      chipEls[pair[0]] = c;
    });
    root.appendChild(chips);

    var bounds = el('div', 'explorer-bounds');
    var boundEls = {};
    BOUNDS.forEach(function (pair) {
      var bnd = el('span', 'bound');
      bnd.appendChild(el('span', 'bound-label', pair[1] + ' = '));
      var v = el('span', 'live bound-value', '');
      bnd.appendChild(v);
      bounds.appendChild(bnd);
      boundEls[pair[0]] = v;
    });
    bounds.appendChild(el('span', 'bounds-note', 'from (A.1) and (A.2)'));
    root.appendChild(bounds);

    var mount = el('div', 'chart-mount');
    mount.id = 'chart-explorer';
    mount.setAttribute('role', 'img');
    mount.setAttribute('aria-label', 'Full-order candidate entry against incumbent strength');
    root.appendChild(mount);

    root.appendChild(el('p', 'explorer-note',
      'These formulas check Proposition 2 and preparation under full investor orders, ' +
      'holding all parameters except incumbent strength fixed. They do not solve for an equilibrium. ' +
      'Figure 2 distinguishes certified equilibria from numerical search results.'));

    state.el = { root: root, badge: badge, range: range, rValue: rValue, warn: warn,
      readouts: readoutEls, chips: chipEls, bounds: boundEls, mount: mount };

    range.addEventListener('input', function () { scheduleUpdate(Number(range.value)); });
    range.addEventListener('change', function () { scheduleUpdate(Number(range.value)); });
  }

  /* ---------- updates ---------- */

  function isBenchmark(r) {
    var P = state.P;
    return Number(r) === Number(P.r_weak) || Number(r) === Number(P.r_strong) || Number(r) === Number(P.r_collapse);
  }

  function render(r) {
    var P = state.P, E = state.el;
    state.r = r;
    var cf = closedForms(P, r);
    E.rValue.textContent = fmtR(r);
    E.rValue.title = String(r);
    E.warn.hidden = cf.inDomain;
    READOUTS.forEach(function (pair) {
      var v = cf[pair[0]];
      var node = E.readouts[pair[0]];
      node.textContent = cf.inDomain ? fmt3(v) : '—';
      node.title = cf.inDomain ? String(v) : '';
    });
    CHIPS.forEach(function (pair) {
      var chip = cf.chips[pair[0]];
      var node = E.chips[pair[0]];
      node.className = 'chip ' + (cf.inDomain ? (chip.ok ? 'pass' : 'fail') : 'na');
      node.textContent = pair[1] + ' · margin ' + (cf.inDomain ? fmtSigned(chip.margin) : '—');
      node.title = cf.inDomain ? String(chip.margin) : '';
    });
    BOUNDS.forEach(function (pair) {
      var node = E.bounds[pair[0]];
      node.textContent = fmt3(cf[pair[0]]);
      node.title = String(cf[pair[0]]);
    });
    var showBadge = cf.inDomain && isBenchmark(r) && state.lastSelfTest && state.lastSelfTest.ok;
    E.badge.hidden = !showBadge;
    E.badge.textContent = showBadge ? "Benchmark verified against the paper's numerical results" : '';
    moveMarker(r);
  }

  function moveMarker(r) {
    var mount = state.el.mount;
    if (!mount || state.markerIndex < 0 || typeof Plotly === 'undefined' || !mount.layout) return;
    var upd = {};
    upd['shapes[' + state.markerIndex + '].x0'] = r;
    upd['shapes[' + state.markerIndex + '].x1'] = r;
    try { Plotly.relayout(mount, upd); } catch (e) { /* chart not mounted yet */ }
  }

  function scheduleUpdate(r) {
    state.pendingR = r;
    if (state.rafPending) return;
    state.rafPending = true;
    window.requestAnimationFrame(function () {
      state.rafPending = false;
      render(state.pendingR);
    });
  }

  function setR(r) {
    var v = Number(r);
    if (!isFinite(v)) return;
    v = Math.min(R_MAX, Math.max(R_MIN, v));
    if (state.el.range) state.el.range.value = String(v);
    render(v);
  }

  function reset() { setR(state.P.r_weak); }

  /* ---------- self-test against the embedded CSV rows ---------- */

  function num(s) {
    if (typeof s === 'number') return s;
    var t = String(s).trim().toLowerCase();
    if (t === 'inf' || t === 'unattainable') return Infinity;
    if (t === '-inf' || t === 'always') return -Infinity;
    return Number(s);
  }

  function selfTest() {
    var D = window.CCC_DATA || {};
    var T = D.tables || {};
    var P = state.P || readInputs();
    var diffs = [], n = 0, worst = { name: null, diff: 0 };
    function compare(name, ours, theirs) {
      n += 1;
      var ok, d;
      if (!isFinite(ours) || !isFinite(theirs)) { ok = ours === theirs; d = ok ? 0 : Infinity; }
      else { d = Math.abs(ours - theirs); ok = d <= TOL; }
      if (d > worst.diff) worst = { name: name, diff: d };
      if (!ok) diffs.push({ name: name, ours: ours, csv: theirs, diff: d });
    }
    var i, row, cf;
    var prim = (T.auction_primitives || []).filter(function (r) { return r.parameter_set === 'base'; });
    for (i = 0; i < prim.length; i++) {
      row = prim[i]; cf = closedForms(P, num(row.r));
      ['t_0', 't_H', 't_L', 'g_H', 'g_L', 'Delta_T', 'B_m', 'B_prior', 'B_M'].forEach(function (col) {
        compare('auction_primitives r=' + row.r + ' ' + col, cf[col], num(row[col]));
      });
    }
    if (!prim.length) diffs.push({ name: 'auction_primitives missing', ours: NaN, csv: NaN, diff: Infinity });
    var ctrl = (T.equilibrium_controls || []).filter(function (r) {
      return r.parameter_set === 'base' && r.noise === 'Laplace' && r.cost_law === 'atoms' && r.accepted === 'true';
    });
    var wanted = [['feedback', P.r_strong], ['feedback', P.r_collapse], ['frozen', P.r_weak]];
    wanted.forEach(function (w) {
      var hit = null;
      for (i = 0; i < ctrl.length; i++) {
        if (ctrl[i].experiment === w[0] && Number(ctrl[i].r) === Number(w[1])) { hit = ctrl[i]; break; }
      }
      if (!hit) { diffs.push({ name: 'equilibrium_controls missing ' + w[0] + ' r=' + w[1], ours: NaN, csv: NaN, diff: Infinity }); return; }
      cf = closedForms(P, Number(hit.r));
      var cols = w[0] === 'feedback' ? ['E', 'O_H', 'tau', 'x_star'] : ['E', 'O_H', 'x_star'];
      cols.forEach(function (col) { compare('equilibrium_controls ' + w[0] + ' r=' + hit.r + ' ' + col, cf[col], num(hit[col])); });
    });
    var ext = (T.extensions || []).filter(function (r) {
      return r.parameter_set === 'base' && r.noise === 'Laplace' && r.cost_law === 'atoms';
    });
    for (i = 0; i < ext.length; i++) {
      row = ext[i];
      var weak = closedForms(P, num(row.r_weak)), strong = closedForms(P, num(row.r_strong));
      compare('extensions zeta_L', strong.chips.A1.margin, num(row.zeta_L));
      compare('extensions zeta_H0', weak.chips.A2a.margin, num(row.zeta_H0));
      compare('extensions zeta_H1', strong.chips.A2b.margin, num(row.zeta_H1));
      compare('extensions zeta_0', weak.chips.A3_no_trade.margin, num(row.zeta_0));
      compare('extensions zeta_1', strong.chips.A3_full.margin, num(row.zeta_1));
    }
    if (!ext.length) diffs.push({ name: 'extensions missing', ours: NaN, csv: NaN, diff: Infinity });
    var thr = {};
    (T.thresholds || []).forEach(function (r) { thr[r.boundary] = r; });
    cf = closedForms(P, P.r_strong);
    [['pooling_unique_sufficient', 'r_k'], ['pooling_existence', 'r_N'], ['full_orders_unique_sufficient', 'r_U'],
      ['high_cost_ceiling', 'r_C'], ['m', 'm'], ['M', 'M']].forEach(function (pair) {
      if (thr[pair[0]]) compare('thresholds ' + pair[0], cf[pair[1]], num(thr[pair[0]].value));
      else diffs.push({ name: 'thresholds missing ' + pair[0], ours: NaN, csv: NaN, diff: Infinity });
    });
    var result = { ok: diffs.length === 0, n: n, worst: worst, diffs: diffs };
    state.lastSelfTest = result;
    if (!state.selfTestLogged) {
      state.selfTestLogged = true;
      if (result.ok) console.log('[ccc] self-test passed (' + n + ' comparisons)');
      else console.error('[ccc] self-test FAILED', diffs);
    }
    return result;
  }

  /* ---------- lifecycle ---------- */

  function mountChart() {
    var mount = state.el.mount;
    if (!mount) return;
    if (CCC.charts && typeof CCC.charts.register === 'function') {
      CCC.charts.register('explorer', builder);
    }
    if (CCC.charts && typeof CCC.charts.mount === 'function' && typeof CCC.charts.register === 'function') {
      CCC.charts.mount('explorer');
      state.mounted = !!CCC.charts.status().explorer.mounted;
      return;
    }
    if (typeof Plotly === 'undefined') {
      mount.textContent = 'Chart library unavailable; the readouts above remain live.';
      return;
    }
    var spec = builder(window.CCC_DATA, tokens(), mount.clientWidth < 640);
    Plotly.newPlot(mount, spec.traces, spec.layout, { displayModeBar: false, responsive: true }).then(function () {
      state.mounted = true;
      moveMarker(state.r);
    });
    document.addEventListener('ccc:themechange', function () {
      var s = builder(window.CCC_DATA, tokens(), mount.clientWidth < 640);
      Plotly.react(mount, s.traces, s.layout, { displayModeBar: false, responsive: true }).then(function () { moveMarker(state.r); });
    });
  }

  function init() {
    if (state.initialised) return;
    var root = document.getElementById('explorer');
    if (!root) return;
    state.P = readInputs();
    buildDOM(root);
    selfTest();
    render(state.P.r_weak);
    mountChart();
    document.addEventListener('ccc:themechange', function () {
      window.setTimeout(function () { moveMarker(state.r); }, 0);
    });
    state.initialised = true;
  }

  function status() {
    return { initialised: state.initialised, r: state.r, mounted: CCC.charts && CCC.charts.status().explorer ? CCC.charts.status().explorer.mounted : state.mounted, selfTest: state.lastSelfTest };
  }

  CCC.explorer = { init: init, setR: setR, reset: reset, selfTest: selfTest, status: status, closedForms: closedForms, builder: builder };
})();
