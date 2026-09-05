/* charts.js: Plotly builders for Figures 1 to 4 of the handout.
 *
 * Reads window.CCC_DATA (emitted by handout/data.py) and the CSS tokens on <html>.
 * Mirrors the drawing conventions of numerics/render/figures.py: no in-figure titles,
 * panel labels outside the axes, broken lines at unresolved nodes, interval bars on the
 * certified points at true scale. Never solves, never changes a parameter, never drops a branch.
 */
(function () {
  'use strict';

  var CCC = (window.CCC = window.CCC || {});
  var CONFIG = { displayModeBar: false, responsive: true, scrollZoom: false, doubleClick: 'reset' };
  var GAP = 0.005; // base mesh of the r grid; breaks appear at gaps wider than 1.5 * GAP
  var HEIGHT = { wide: 380, stacked: 600, fig2: 540 };

  var FALLBACK = {
    bg: '#ffffff', surface: '#ffffff', ink: '#1a1a1a', muted: '#6b6b6b', grid: '#e6e6e6', line: '#cfcfcf',
    accent: '#5b3df5', accentSoft: 'rgba(91,61,245,0.14)', c2: '#c98a1b', c3: '#5f6b7a',
    regionA: 'rgba(91,61,245,0.08)', regionB: 'rgba(201,138,27,0.10)', regionC: 'rgba(95,107,122,0.10)',
    fontSans: 'ui-sans-serif, -apple-system, "Segoe UI", Roboto, sans-serif',
    fontMono: 'ui-monospace, SFMono-Regular, Menlo, monospace'
  };
  var VARS = {
    bg: '--bg', surface: '--surface', ink: '--ink', muted: '--muted', grid: '--grid', line: '--line',
    accent: '--accent', accentSoft: '--accent-soft', c2: '--c2', c3: '--c3',
    regionA: '--region-a', regionB: '--region-b', regionC: '--region-c',
    fontSans: '--font-sans', fontMono: '--font-mono'
  };

  function tokens() {
    var cs = getComputedStyle(document.documentElement);
    var out = {};
    Object.keys(VARS).forEach(function (k) {
      var v = cs.getPropertyValue(VARS[k]);
      v = v ? v.trim() : '';
      out[k] = v || FALLBACK[k];
    });
    return out;
  }

  function formatNumber(x) {
    if (x === null || x === undefined) return 'n/a';
    return String(x);
  }

  /* Split a long digit string into readable chunks for a hover label. */
  function chunk(s, n) {
    s = String(s);
    if (s.length <= n) return s;
    var parts = [];
    for (var i = 0; i < s.length; i += n) parts.push(s.slice(i, i + n));
    return parts.join('<br>&nbsp;&nbsp;');
  }

  /* Sort by x and insert null where consecutive nodes are farther apart than gap*1.5 or |dy| > jump.
   * Returns {x, y, idx}; idx maps each output position to the input index (null at breaks) so the
   * caller can align customdata. Mirrors _broken_series in numerics/render/figures.py. */
  function brokenSeries(xs, ys, gap, jump) {
    gap = gap === undefined ? GAP : gap;
    jump = jump === undefined ? 0.02 : jump;
    var order = [];
    for (var i = 0; i < xs.length; i++) order.push(i);
    order.sort(function (a, b) { return xs[a] - xs[b]; });
    var x = [], y = [], idx = [];
    for (var k = 0; k < order.length; k++) {
      var i0 = order[k];
      if (k > 0) {
        var ip = order[k - 1];
        if (xs[i0] - xs[ip] > gap * 1.5 || Math.abs(ys[i0] - ys[ip]) > jump) {
          x.push(null); y.push(null); idx.push(null);
        }
      }
      x.push(xs[i0]); y.push(ys[i0]); idx.push(i0);
    }
    return { x: x, y: y, idx: idx };
  }

  function pick(arr, idx) {
    return idx.map(function (i) { return i === null ? null : arr[i]; });
  }

  function axis(t, extra) {
    var a = {
      showline: true, linecolor: t.line, linewidth: 1, gridcolor: t.grid, gridwidth: 1,
      zeroline: false, ticks: 'outside', tickcolor: t.line, ticklen: 4,
      tickfont: { size: 12, color: t.ink }, title: { font: { size: 13, color: t.ink }, standoff: 8 },
      showspikes: false, automargin: true
    };
    if (extra) Object.keys(extra).forEach(function (k) { a[k] = extra[k]; });
    return a;
  }

  function baseLayout(t) {
    return {
      paper_bgcolor: 'rgba(0,0,0,0)',
      plot_bgcolor: 'rgba(0,0,0,0)',
      font: { family: t.fontSans, color: t.ink, size: 13 },
      margin: { l: 56, r: 16, t: 60, b: 52 },
      hoverlabel: { bgcolor: t.surface, bordercolor: t.line, namelength: -1,
        font: { family: t.fontMono, size: 12, color: t.ink } },
      legend: { orientation: 'h', x: 0, xanchor: 'left', y: 1, yanchor: 'bottom',
        font: { size: 12, color: t.ink }, bgcolor: 'rgba(0,0,0,0)', itemwidth: 30 },
      uirevision: 'ccc',
      showlegend: true,
      hovermode: 'x unified',
      dragmode: false,
      autosize: true,
      annotations: [],
      shapes: []
    };
  }

  /* Panel label outside the axes, top left, in the margin (paper convention). */
  function panelLabel(t, text, xaxisKey, yaxisKey) {
    return {
      text: text, showarrow: false,
      xref: xaxisKey + ' domain', yref: yaxisKey + ' domain',
      x: 0, y: 1, xanchor: 'left', yanchor: 'bottom', xshift: -52, yshift: 16,
      font: { size: 13, color: t.ink }
    };
  }

  function panelLabels(layout, t, keys) {
    keys = keys || [['(a)', 'x', 'y'], ['(b)', 'x2', 'y2']];
    layout.annotations = layout.annotations || [];
    keys.forEach(function (k) { layout.annotations.push(panelLabel(t, k[0], k[1], k[2])); });
    return layout;
  }

  /* Axis domains for two panels: side by side (wide) or stacked (narrow / fig2). */
  function twoPanels(layout, stacked) {
    if (stacked) {
      layout.xaxis.domain = [0, 1]; layout.xaxis.anchor = 'y';
      layout.yaxis.domain = [0.58, 1]; layout.yaxis.anchor = 'x';
      layout.xaxis2.domain = [0, 1]; layout.xaxis2.anchor = 'y2';
      layout.yaxis2.domain = [0, 0.42]; layout.yaxis2.anchor = 'x2';
    } else {
      layout.xaxis.domain = [0, 0.45]; layout.xaxis.anchor = 'y';
      layout.yaxis.domain = [0, 1]; layout.yaxis.anchor = 'x';
      layout.xaxis2.domain = [0.57, 1]; layout.xaxis2.anchor = 'y2';
      layout.yaxis2.domain = [0, 1]; layout.yaxis2.anchor = 'x2';
    }
    return layout;
  }

  function line(color, dash, width) {
    return { color: color, dash: dash || 'solid', width: width || 2, shape: 'linear' };
  }

  /* ------------------------------------------------------------------ Figure 1 */
  function fig1(D, t, opts) {
    var F = D.fig1;
    var narrow = !!(opts && opts.narrow);
    var traces = [];
    var cdA = F.r.map(function (_, i) { return [formatNumber(F.Delta_T[i]), formatNumber(F.d_Delta_T_dr[i])]; });
    traces.push({
      type: 'scatter', mode: 'lines', name: 'Δ<sub>T</sub>(r)',
      x: F.r, y: F.Delta_T, customdata: cdA, line: line(t.accent, 'solid', 2.2),
      xaxis: 'x', yaxis: 'y', legendgroup: 'DT',
      hovertemplate: 'Δ<sub>T</sub> = %{customdata[0]}<br>dΔ<sub>T</sub>/dr = %{customdata[1]}<extra>Δ<sub>T</sub></extra>'
    });
    var mus = F.mu.slice().sort(function (a, b) { return Number(b) - Number(a); }); // M, 1/2, m
    var style = {};
    style[mus[0]] = { color: t.accent, dash: 'solid', width: 2.2 };
    style[mus[1]] = { color: t.c2, dash: 'dash', width: 2.2 };
    style[mus[2]] = { color: t.c3, dash: 'dot', width: 2.6 };
    mus.forEach(function (mu) {
      var B = F.B[mu], dB = F.dB[mu];
      var label = F.mu_label[mu] || mu;
      var cd = F.r.map(function (_, i) { return [formatNumber(B[i]), formatNumber(dB[i])]; });
      traces.push({
        type: 'scatter', mode: 'lines', name: 'μ = ' + label,
        x: F.r, y: B, customdata: cd, line: line(style[mu].color, style[mu].dash, style[mu].width),
        xaxis: 'x2', yaxis: 'y2', legendgroup: 'B' + label,
        hovertemplate: 'B<sub>r</sub>(' + label + ') = %{customdata[0]}<br>dB/dr = %{customdata[1]}<extra>μ = ' + label + '</extra>'
      });
    });
    var layout = baseLayout(t);
    layout.height = narrow ? HEIGHT.stacked : HEIGHT.wide;
    layout.xaxis = axis(t, { title: { text: 'incumbent strength <i>r</i>' }, range: [1.0, 3.8], tick0: 1, dtick: 0.5 });
    layout.yaxis = axis(t, { title: { text: 'information spread Δ<sub><i>T</i></sub>(<i>r</i>)' }, range: [0, 1.1] });
    layout.xaxis2 = axis(t, { title: { text: 'incumbent strength <i>r</i>' }, range: [1.0, 3.8], tick0: 1, dtick: 0.5 });
    layout.yaxis2 = axis(t, { title: { text: 'challenger gross profit <i>B<sub>r</sub></i>(μ)' }, range: [1.5, 7.5] });
    twoPanels(layout, narrow);
    panelLabels(layout, t);
    return { traces: traces, layout: layout };
  }

  /* ------------------------------------------------------------------ Figure 2 */
  var BRANCH_STYLE = [
    { key: 'pooling', name: 'no trade', color: 'accent', dash: 'solid', width: 2.2, ycol: 'q_H', jumpB: 0.02 },
    { key: 'full_orders', name: 'full orders', color: 'c2', dash: 'solid', width: 2.2, ycol: 'q_H', jumpB: 0.02 },
    { key: 'asymmetric', name: 'asymmetric orders (1, −v)', color: 'accent', dash: 'dash', width: 2.2, ycol: 'v', jumpB: 0.2 },
    { key: 'symmetric_interior', name: 'symmetric interior orders (u, −u)', color: 'c3', dash: 'dot', width: 2.6, ycol: 'q_H', jumpB: 0.2 }
  ];

  function fig2(D, t) {
    var F = D.fig2;
    var traces = [];
    var th = F.thresholds || {};
    var regions = F.regions || {};
    var xr = F.x_range || [1.0, 3.8];

    BRANCH_STYLE.forEach(function (s) {
      var br = F.branches[s.key];
      if (!br || !br.r || !br.r.length) return;
      var col = t[s.color];
      var cd = br.r.map(function (_, i) {
        return [formatNumber(br.E[i]), formatNumber(br.q_H[i]), formatNumber(br.q_L[i]),
          formatNumber(br.O_H ? br.O_H[i] : null), br.uniqueness_status ? br.uniqueness_status[i] : ''];
      });
      var a = brokenSeries(br.r, br.E, GAP, 0.02);
      traces.push({
        type: 'scatter', mode: 'lines', name: s.name, legendgroup: s.key,
        x: a.x, y: a.y, customdata: pick(cd, a.idx), connectgaps: false,
        line: line(col, s.dash, s.width), xaxis: 'x', yaxis: 'y',
        hovertemplate: 'E = %{customdata[0]}<br>O<sub>H</sub> = %{customdata[3]}<br>(q<sub>H</sub>, q<sub>L</sub>) = (%{customdata[1]}, %{customdata[2]})<br>uniqueness: %{customdata[4]}<extra>' + s.name + '</extra>'
      });
      var yb = br[s.ycol];
      var b = brokenSeries(br.r, yb, GAP, s.jumpB);
      var what = s.ycol === 'v' ? 'v' : (s.key === 'symmetric_interior' ? 'u' : 'q<sub>H</sub>');
      traces.push({
        type: 'scatter', mode: 'lines', name: s.name, legendgroup: s.key, showlegend: false,
        x: b.x, y: b.y, customdata: pick(cd, b.idx), connectgaps: false,
        line: line(col, s.dash, s.width), xaxis: 'x2', yaxis: 'y2',
        hovertemplate: what + ' = %{y}<br>(q<sub>H</sub>, q<sub>L</sub>) = (%{customdata[1]}, %{customdata[2]})<extra>' + s.name + '</extra>'
      });
    });

    var certs = (F.certificates || []).filter(function (c) { return c.accepted === 'true'; });
    if (certs.length) {
      var cx = certs.map(function (c) { return Number(c.r); });
      var eMid = certs.map(function (c) { return Number(c.E_mid); });
      var vMid = certs.map(function (c) { return Number(c.v_mid); });
      var cdC = certs.map(function (c) {
        return [c.r, chunk(c.E_lower, 32), chunk(c.E_upper, 32), c.E_halfwidth, c.v_lower, c.v_upper, c.v_halfwidth];
      });
      var marker = { symbol: 'diamond', size: 9, color: t.ink, line: { width: 1, color: t.surface } };
      traces.push({
        type: 'scatter', mode: 'markers', name: 'certified equilibria (Proposition 3)', legendgroup: 'certified',
        x: cx, y: eMid, customdata: cdC, marker: marker, xaxis: 'x', yaxis: 'y',
        error_y: { type: 'data', symmetric: false, visible: true, color: t.ink, thickness: 1.2, width: 8,
          array: certs.map(function (c, i) { return Number(c.E_upper) - eMid[i]; }),
          arrayminus: certs.map(function (c, i) { return eMid[i] - Number(c.E_lower); }) },
        hovertemplate: 'r = %{customdata[0]}<br>E ∈ [%{customdata[1]},<br>&nbsp;&nbsp;%{customdata[2]}]<br>half-width %{customdata[3]}<extra>certified</extra>'
      });
      traces.push({
        type: 'scatter', mode: 'markers', name: 'certified equilibria (Proposition 3)', legendgroup: 'certified', showlegend: false,
        x: cx, y: vMid, customdata: cdC, marker: marker, xaxis: 'x2', yaxis: 'y2',
        error_y: { type: 'data', symmetric: false, visible: true, color: t.ink, thickness: 1.2, width: 8,
          array: certs.map(function (c, i) { return Number(c.v_upper) - vMid[i]; }),
          arrayminus: certs.map(function (c, i) { return vMid[i] - Number(c.v_lower); }) },
        hovertemplate: 'r = %{customdata[0]}<br>v ∈ [%{customdata[4]}, %{customdata[5]}]<br>half-width %{customdata[6]}<extra>certified</extra>'
      });
    }

    var layout = baseLayout(t);
    layout.height = HEIGHT.fig2;
    layout.margin = { l: 56, r: 16, t: 84, b: 52 };
    layout.dragmode = 'zoom';
    layout.xaxis = axis(t, { range: xr.slice(), tick0: 1, dtick: 0.5, showticklabels: false, domain: [0, 1], anchor: 'y' });
    layout.yaxis = axis(t, { title: { text: 'total entry <i>E</i>' }, range: [0.12, 0.62],
      tickvals: [0.25, 0.35, 0.45, 0.55], domain: [0.56, 1], anchor: 'x' });
    layout.xaxis2 = axis(t, { title: { text: 'incumbent strength <i>r</i>' }, range: xr.slice(), tick0: 1, dtick: 0.5,
      matches: 'x', domain: [0, 1], anchor: 'y2' });
    layout.yaxis2 = axis(t, { title: { text: 'order magnitude' }, range: [-0.05, 1.12],
      tickvals: [0, 0.25, 0.5, 0.75, 1], domain: [0, 0.44], anchor: 'x2' });
    // legend sits above the threshold labels: paper y offset computed from the fixed height
    var plotH = HEIGHT.fig2 - layout.margin.t - layout.margin.b;
    layout.legend.y = 1 + 30 / plotH;

    function regionShape(range, color) {
      if (!range || range.length !== 2) return null;
      return { type: 'rect', xref: 'x', yref: 'paper', x0: range[0], x1: range[1], y0: 0, y1: 1,
        fillcolor: color, line: { width: 0 }, layer: 'below' };
    }
    [regionShape(regions.no_trade_unique, t.regionA), regionShape(regions.full_orders_unique, t.regionB),
      regionShape(regions.multiplicity, t.regionC)].forEach(function (s) { if (s) layout.shapes.push(s); });

    var thKeys = [['pooling_existence', 'r<sub>N</sub>'], ['full_orders_unique_sufficient', 'r<sub>U</sub>'], ['high_cost_ceiling', 'r<sub>C</sub>']];
    thKeys.forEach(function (k) {
      var row = th[k[0]];
      if (!row) return;
      var v = Number(row.value);
      layout.shapes.push({ type: 'line', xref: 'x', yref: 'paper', x0: v, x1: v, y0: 0, y1: 1,
        line: { color: t.muted, width: 1, dash: 'dot' }, layer: 'below' });
      layout.annotations.push({ text: k[1], showarrow: false, xref: 'x', x: v, yref: 'y domain', y: 1,
        yanchor: 'bottom', yshift: 3, font: { size: 12, color: t.muted },
        hovertext: k[1].replace(/<[^>]+>/g, '') + ' = ' + (row.value_str || formatNumber(row.value)) + (row.interpretation ? '<br>' + row.interpretation : '') });
    });

    function caption(range, text) {
      if (!range || range.length !== 2) return;
      layout.annotations.push({ text: text, showarrow: false, xref: 'x', x: (range[0] + range[1]) / 2,
        yref: 'y domain', y: 0.03, yanchor: 'bottom', font: { size: 11, color: t.muted }, align: 'center' });
    }
    caption(regions.no_trade_unique, 'no trade<br>unique');
    caption(regions.multiplicity, 'several<br>equilibria');
    caption(regions.full_orders_unique, 'full orders unique');
    panelLabels(layout, t);
    return { traces: traces, layout: layout };
  }

  /* ------------------------------------------------------------------ Figure 3 */
  function fig3(D, t, opts) {
    var F = D.fig3;
    var narrow = !!(opts && opts.narrow);
    var traces = [];
    var styles = [
      { key: 'Laplace', color: t.accent, dash: 'solid', endName: 'Laplace, plateau (tie rule)', open: false },
      { key: 'logistic', color: t.c2, dash: 'dash', endName: 'logistic, bound unattained', open: true }
    ];
    styles.forEach(function (s) {
      var S = F[s.key];
      if (!S) return;
      var xs = [], mass = [], E = [], cd = [];
      var end = null;
      for (var i = 0; i < S.M_minus_tau.length; i++) {
        var row = [formatNumber(S.posterior_upper_tail_mass[i]), formatNumber(S.E[i]), formatNumber(S.x_star ? S.x_star[i] : null)];
        if (S.M_minus_tau[i] > 0) { xs.push(S.M_minus_tau[i]); mass.push(S.posterior_upper_tail_mass[i]); E.push(S.E[i]); cd.push(row); }
        else if (S.M_minus_tau[i] === 0) end = { x: 0, mass: S.posterior_upper_tail_mass[i], E: S.E[i], cd: row };
      }
      traces.push({
        type: 'scatter', mode: 'lines', name: s.key, legendgroup: s.key,
        x: xs, y: mass, customdata: cd, line: line(s.color, s.dash, 2.2), xaxis: 'x', yaxis: 'y',
        hovertemplate: 'Pr(μ<sub>X</sub> ≥ τ) = %{customdata[0]}<br>x* = %{customdata[2]}<extra>' + s.key + '</extra>'
      });
      traces.push({
        type: 'scatter', mode: 'lines', name: s.key, legendgroup: s.key, showlegend: false,
        x: xs, y: E, customdata: cd, line: line(s.color, s.dash, 2.2), xaxis: 'x2', yaxis: 'y2',
        hovertemplate: 'E = %{customdata[1]}<br>x* = %{customdata[2]}<extra>' + s.key + '</extra>'
      });
      if (end) {
        var marker = s.open
          ? { symbol: 'circle-open', size: 9, color: s.color, line: { width: 1.6, color: s.color } }
          : { symbol: 'circle', size: 9, color: s.color, line: { width: 1, color: s.color } };
        traces.push({
          type: 'scatter', mode: 'markers', name: s.endName, legendgroup: s.key + '-end',
          x: [end.x], y: [end.mass], customdata: [end.cd], marker: marker, xaxis: 'x', yaxis: 'y',
          hovertemplate: 'M − τ = 0<br>Pr(μ<sub>X</sub> ≥ τ) = %{customdata[0]}<br>x* = %{customdata[2]}<extra>' + s.endName + '</extra>'
        });
        traces.push({
          type: 'scatter', mode: 'markers', name: s.endName, legendgroup: s.key + '-end', showlegend: false,
          x: [end.x], y: [end.E], customdata: [end.cd], marker: marker, xaxis: 'x2', yaxis: 'y2',
          hovertemplate: 'M − τ = 0<br>E = %{customdata[1]}<br>x* = %{customdata[2]}<extra>' + s.endName + '</extra>'
        });
      }
    });
    var layout = baseLayout(t);
    layout.height = narrow ? HEIGHT.stacked : HEIGHT.wide;
    layout.xaxis = axis(t, { title: { text: 'threshold distance <i>M</i> − τ' }, range: [-0.01, 0.24], tick0: 0, dtick: 0.05 });
    layout.yaxis = axis(t, { title: { text: 'Pr(μ<sub><i>X</i></sub> ≥ τ) under full orders' }, range: [-0.02, 0.55] });
    layout.xaxis2 = axis(t, { title: { text: 'threshold distance <i>M</i> − τ' }, range: [-0.01, 0.24], tick0: 0, dtick: 0.05 });
    layout.yaxis2 = axis(t, { title: { text: 'total entry <i>E</i>' }, range: [0.22, 0.66] });
    twoPanels(layout, narrow);
    panelLabels(layout, t);
    return { traces: traces, layout: layout };
  }

  /* ------------------------------------------------------------------ Figure 4 */
  function fig4(D, t, opts) {
    var F = D.fig4;
    var narrow = !!(opts && opts.narrow);
    var traces = [];
    var keys = Object.keys(F).sort(function (a, b) { return Number(a) - Number(b); });
    var styles = [
      { key: keys[0], color: t.accent, dash: 'solid', word: 'weak' },
      { key: keys[1], color: t.c2, dash: 'dash', word: 'strong' }
    ];
    styles.forEach(function (s) {
      var S = F[s.key];
      if (!S) return;
      var cd = S.eta.map(function (_, i) { return [formatNumber(S.Delta_eta[i]), formatNumber(S.G_H_eta[i]), formatNumber(S.G_L_eta[i])]; });
      var who = s.word + ' incumbent, r = ' + s.key;
      traces.push({
        type: 'scatter', mode: 'lines', name: who, legendgroup: 'D' + s.key,
        x: S.eta, y: S.Delta_eta, customdata: cd, line: line(s.color, s.dash, 2.2), xaxis: 'x', yaxis: 'y',
        hovertemplate: 'Δ<sub>η</sub> = %{customdata[0]}<extra>' + who + '</extra>'
      });
    });
    styles.forEach(function (s) {
      var S = F[s.key];
      if (!S) return;
      var cd = S.eta.map(function (_, i) { return [formatNumber(S.Delta_eta[i]), formatNumber(S.G_H_eta[i]), formatNumber(S.G_L_eta[i])]; });
      traces.push({
        type: 'scatter', mode: 'lines', name: 'G<sub>H</sub>, ' + s.word, legendgroup: 'GH' + s.key,
        x: S.eta, y: S.G_H_eta, customdata: cd, line: line(s.color, 'solid', 2.2), xaxis: 'x2', yaxis: 'y2',
        hovertemplate: 'G<sub>H,η</sub> = %{customdata[1]}<extra>G<sub>H</sub>, ' + s.word + ' (r = ' + s.key + ')</extra>'
      });
      traces.push({
        type: 'scatter', mode: 'lines', name: 'G<sub>L</sub>, ' + s.word, legendgroup: 'GL' + s.key,
        x: S.eta, y: S.G_L_eta, customdata: cd, line: line(s.color, 'dash', 2.2), xaxis: 'x2', yaxis: 'y2',
        hovertemplate: 'G<sub>L,η</sub> = %{customdata[2]}<extra>G<sub>L</sub>, ' + s.word + ' (r = ' + s.key + ')</extra>'
      });
    });
    var layout = baseLayout(t);
    layout.height = narrow ? HEIGHT.stacked : HEIGHT.wide;
    layout.xaxis = axis(t, { title: { text: 'seller bargaining weight η' }, range: [0, 1], tick0: 0, dtick: 0.25 });
    layout.yaxis = axis(t, { title: { text: 'information spread Δ<sub>η</sub>' }, range: [0, 10.5] });
    layout.xaxis2 = axis(t, { title: { text: 'seller bargaining weight η' }, range: [0, 1], tick0: 0, dtick: 0.25 });
    layout.yaxis2 = axis(t, { title: { text: 'challenger profit <i>G</i><sub>θ,η</sub>' }, type: 'log',
      range: [Math.log10(3e-3), Math.log10(60)], tickvals: [0.01, 0.1, 1, 10], ticktext: ['0.01', '0.1', '1', '10'] });
    twoPanels(layout, narrow);
    [['x', 'y'], ['x2', 'y2']].forEach(function (k) {
      layout.shapes.push({ type: 'line', xref: k[0], yref: k[1] + ' domain', x0: 0.5, x1: 0.5, y0: 0, y1: 1,
        line: { color: t.muted, width: 1, dash: 'dot' }, layer: 'below' });
      layout.annotations.push({ text: 'η = 1/2', showarrow: false, xref: k[0], x: 0.5, yref: k[1] + ' domain', y: 0.02,
        yanchor: 'bottom', font: { size: 11, color: t.muted } });
    });
    panelLabels(layout, t);
    return { traces: traces, layout: layout };
  }

  /* ------------------------------------------------------------------ mounting */
  var builders = { fig1: fig1, fig2: fig2, fig3: fig3, fig4: fig4 };
  var records = {};
  var mounted = {};   // id -> {el, narrow, ro}
  var pending = [];
  var FIGURE_NUMBER = { fig1: 1, fig2: 2, fig3: 3, fig4: 4 };

  function isEager() {
    if (typeof CCC.eager === 'boolean') return CCC.eager;
    try { return /[?&]eager=1/.test(location.search); } catch (e) { return false; }
  }

  function notice(id) {
    var n = FIGURE_NUMBER[id];
    var where = n ? 'see Figure ' + n + ' in the manuscript.' : 'this panel needs the chart library.';
    return '<p class="chart-notice">Chart library unavailable; ' + where + '</p>';
  }

  function buildSpec(id, el) {
    var narrow = el.clientWidth > 0 && el.clientWidth < 640;
    var spec = builders[id](window.CCC_DATA, tokens(), { narrow: narrow });
    spec.narrow = narrow;
    return spec;
  }

  function mount(id) {
    var el = document.getElementById('chart-' + id);
    var builder = builders[id];
    if (!el || !builder) {
      records[id] = { mounted: false, traces: 0, reason: !el ? 'no mount element' : 'no builder' };
      return records[id];
    }
    if (mounted[id]) return records[id];
    if (typeof Plotly === 'undefined' || !window.CCC_DATA) {
      el.innerHTML = notice(id);
      records[id] = { mounted: false, traces: 0, reason: typeof Plotly === 'undefined' ? 'plotly unavailable' : 'no data' };
      return records[id];
    }
    var spec;
    try {
      spec = buildSpec(id, el);
    } catch (err) {
      records[id] = { mounted: false, traces: 0, reason: 'builder error: ' + (err && err.message) };
      if (window.console) console.error('[ccc] chart builder failed', id, err);
      return records[id];
    }
    el.innerHTML = '';
    var p = Plotly.newPlot(el, spec.traces, spec.layout, CONFIG);
    pending.push(p);
    mounted[id] = { el: el, narrow: spec.narrow, ro: null, timer: null };
    records[id] = { mounted: true, traces: spec.traces.length, narrow: spec.narrow };
    if (typeof ResizeObserver !== 'undefined') {
      var ro = new ResizeObserver(function () {
        var m = mounted[id];
        if (!m) return;
        clearTimeout(m.timer);
        m.timer = setTimeout(function () {
          var narrow = el.clientWidth > 0 && el.clientWidth < 640;
          if (narrow !== m.narrow) { react(id); }
          else { try { Plotly.Plots.resize(el); } catch (e) { /* container hidden */ } }
        }, 120);
      });
      ro.observe(el);
      mounted[id].ro = ro;
    }
    return records[id];
  }

  function react(id) {
    var m = mounted[id];
    if (!m || typeof Plotly === 'undefined') return;
    var spec = buildSpec(id, m.el);
    m.narrow = spec.narrow;
    records[id] = { mounted: true, traces: spec.traces.length, narrow: spec.narrow };
    pending.push(Plotly.react(m.el, spec.traces, spec.layout, CONFIG));
  }

  function rerender() {
    Object.keys(mounted).forEach(react);
  }

  function observe(id, el) {
    if (typeof IntersectionObserver === 'undefined') { mount(id); return; }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { io.disconnect(); mount(id); }
      });
    }, { rootMargin: '200px 0px' });
    io.observe(el);
  }

  function mountAll() {
    var ids = Object.keys(builders);
    ids.forEach(function (id) {
      var el = document.getElementById('chart-' + id);
      if (!el || mounted[id]) return;
      if (isEager()) mount(id); else observe(id, el);
    });
    return Promise.all(pending.slice()).then(function () { return status(); });
  }

  function register(id, builder, figureNumber) {
    builders[id] = builder;
    if (figureNumber) FIGURE_NUMBER[id] = figureNumber;
    if (!records[id]) records[id] = { mounted: false, traces: 0, reason: 'not mounted' };
  }

  function status() {
    var out = {};
    Object.keys(builders).forEach(function (id) {
      out[id] = records[id] ? Object.assign({}, records[id]) : { mounted: false, traces: 0, reason: 'not mounted' };
    });
    return out;
  }

  document.addEventListener('ccc:themechange', function () { rerender(); });

  CCC.charts = {
    mount: mount, mountAll: mountAll, rerender: rerender, status: status, register: register,
    tokens: tokens, baseLayout: baseLayout, brokenSeries: brokenSeries, panelLabels: panelLabels,
    twoPanels: twoPanels, axis: axis, formatNumber: formatNumber, config: CONFIG, builders: builders
  };
})();
