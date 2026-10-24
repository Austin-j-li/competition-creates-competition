/* figures.js: the closed forms of the order-slot benchmark and three figures of the handout.
 *
 * window.CCC.slot holds the closed forms of the manuscript (slot/manuscript/, Sections 3 to 5 and
 * Appendix A4), evaluated at the declarations in window.CCC_DATA (handout/slot_data.py, from the
 * slot registry). Marked strengths (r_A, r_F, r_N, r_J, r_S, r_C, r_R, r_U) are registry rows, never
 * recomputed here. The benchmark auction (point-mass classes h and ell, reserve p, incumbent uniform
 * on [0, r]) gives, for p < ell < r < h:
 *
 *   t_0 = p (1 - p/r);  t_H = r/2 + p^2/(2r);  t_L = ell - (ell^2 - p^2)/(2r)
 *   g_H = h - r/2 - p^2/(2r);  g_L = (ell^2 - p^2)/(2r);  Delta_T = (r - ell)^2/(2r)
 *   B(mu) = g_L + mu (g_H - g_L);  tau = (c_H - g_L)/(g_H - g_L)
 *
 * The slot at the prior 1/2: a liquidity order of each sign has mass b, no liquidity order b_0,
 * the investor is present with probability lambda. With informed purchase rate s (class H) and
 * informed sale rate t (class L), the order laws on (-1, 0, 1) are
 *   f_H = (b, b_0 + lambda - s, b + s),   f_L = (b + t, b_0 + lambda - t, b),
 * the posteriors are mu(1) = (b+s)/(2b+s), mu(-1) = b/(2b+t), mu(0) = f_H(0)/(f_H(0) + f_L(0)),
 * and the price is P(x) = t_0 + e(x) [t_L - t_0 + Delta_T mu(x)].
 * Equilibrium forms on the benchmark path (Appendix A4): N (s = 0), R (s = b(Delta_T/k - 2),
 * recruits after a purchase), F (s = lambda; recruits up to r_C), Q (s = t = b(rho Delta_T/k - 2)).
 * The low class sells at t = 0 up to r_N, t = b(rho Delta_T/k - 2) on (r_N, r_S), t = lambda from r_S.
 * Research (Section 5): lambda_R is the positive root of A x^2 + B x + C with A = 2a(1 - 2 beta),
 * B = 4 a beta + k (1 - 2 beta) + beta Delta_T, C = beta (2k - Delta_T); entry on that branch is
 * rho + (1 - rho)[beta + (1/2 - beta) lambda_R].
 *
 * The builders return specs for the renderer in charts.js. Nothing here solves for an equilibrium.
 * ES2019, no modules.
 */
(function () {
  'use strict';

  var CCC = (window.CCC = window.CCC || {});

  /* ------------------------------------------------------------------ closed forms */
  function inputs(D) {
    D = D || window.CCC_DATA || {};
    var P = {}, src = Object.assign({}, D.inputs || {}, D.derived || {});
    Object.keys(src).forEach(function (k) {
      var v = Number(src[k].x);
      if (!isFinite(v)) throw new Error('[ccc] slot input ' + k + ' is not numeric');
      P[k] = v;
    });
    P.display = {};
    Object.keys(src).forEach(function (k) { P.display[k] = src[k].display; });
    return P;
  }

  function auction(P, r) {
    var h = P.h, ell = P.ell, p = P.p;
    var a = {
      r: r,
      t0: p * (1 - p / r),
      tH: r / 2 + p * p / (2 * r),
      tL: ell - (ell * ell - p * p) / (2 * r),
      gH: h - r / 2 - p * p / (2 * r),
      gL: (ell * ell - p * p) / (2 * r),
      Delta: (r - ell) * (r - ell) / (2 * r)
    };
    a.B = function (mu) { return a.gL + mu * (a.gH - a.gL); };
    a.tau = (P.c_H - a.gL) / (a.gH - a.gL);
    a.J = a.Delta * (1 - a.tau);
    return a;
  }

  function lowRate(P, r, A) {
    if (r <= P.rN) return 0;
    if (r < P.rS) return P.b * (P.rho * A.Delta / P.k - 2);
    return P.lambda;
  }

  /* One equilibrium form at strength r: rates, posteriors, entry, prices, entry and ownership. */
  function form(P, r, id) {
    var A = auction(P, r), b = P.b, b0 = P.b0, lam = P.lambda, rho = P.rho;
    var s, t = lowRate(P, r, A), e1 = rho;
    if (id === 'N') { s = 0; t = 0; }
    else if (id === 'R') { s = b * (A.Delta / P.k - 2); e1 = 1; }
    else if (id === 'F') { s = lam; e1 = r <= P.rC ? 1 : rho; }
    else if (id === 'Q') { s = b * (rho * A.Delta / P.k - 2); t = s; }
    var fH = { '-1': b, '0': b0 + lam - s, '1': b + s };
    var fL = { '-1': b + t, '0': b0 + lam - t, '1': b };
    var mu = { '-1': b / (2 * b + t), '0': fH['0'] / (fH['0'] + fL['0']), '1': (b + s) / (2 * b + s) };
    var e = { '-1': rho, '0': rho, '1': e1 };
    var price = {}, E = 0, eH = 0;
    ['-1', '0', '1'].forEach(function (x) {
      price[x] = A.t0 + e[x] * (A.tL - A.t0 + A.Delta * mu[x]);
      E += 0.5 * (fH[x] + fL[x]) * e[x];
      eH += fH[x] * e[x];
    });
    return { id: id, r: r, A: A, s: s, t: t, buyH: s / lam, sellL: t / lam, fH: fH, fL: fL, mu: mu, e: e, price: price,
      E: E, O_H: P.pi * eH };
  }

  /* The equilibrium set that Appendix A4 lists at strength r of the benchmark path (prior 1/2,
     an indifferent investor may mix, an indifferent high-cost challenger prepares). */
  function equilibria(P, r) {
    var ids = [];
    if (r <= P.rN) ids.push('N');
    if (r >= P.rA && r < P.rF) ids.push('R');
    if (r >= P.rF) ids.push('F');
    if (r > P.rN && r < P.rJ) ids.push('Q');
    return ids.map(function (id) { return form(P, r, id); });
  }

  function entryR(P, r) { return P.rho + (1 - P.rho) * P.b * auction(P, r).Delta / (2 * P.k); }
  function entryT(P, r) {
    var A = auction(P, r);
    return P.rho + (P.b / 2) * (P.k - P.rho * A.J) / (A.Delta * (1 - A.tau) * (1 - A.tau));
  }
  function plateau(P) { return P.rho + (1 - P.rho) * (P.b + P.lambda / 2); }

  function lambdaR(P, r) {
    var D = auction(P, r).Delta, a = P.a, beta = P.beta, k = P.k;
    var A2 = 2 * a * (1 - 2 * beta), B1 = 4 * a * beta + k * (1 - 2 * beta) + beta * D, C0 = beta * (2 * k - D);
    return (-B1 + Math.sqrt(B1 * B1 - 4 * A2 * C0)) / (2 * A2);
  }
  function entryResearch(P, lam) { return P.rho + (1 - P.rho) * (P.beta + (0.5 - P.beta) * lam); }

  function grid(lo, hi, n) {
    var xs = [];
    for (var i = 0; i <= n; i++) xs.push(lo + (hi - lo) * i / n);
    return xs;
  }

  CCC.slot = { inputs: inputs, auction: auction, form: form, equilibria: equilibria, entryR: entryR, entryT: entryT,
    plateau: plateau, lambdaR: lambdaR, entryResearch: entryResearch, grid: grid };

  /* ------------------------------------------------------------------ shared drawing helpers */
  function d6(v) { return isFinite(v) ? Number(v).toFixed(6) : 'n/a'; }

  function vline(layout, xref, x, color, dash, width) {
    layout.shapes.push({ type: 'line', xref: xref, yref: (xref === 'x2' ? 'y2' : 'y') + ' domain', x0: x, x1: x, y0: 0, y1: 1,
      line: { color: color, width: width || 1, dash: dash || '2 3' }, layer: 'below' });
  }
  function hline(layout, xref, yref, y, color, dash, width) {
    layout.shapes.push({ type: 'line', xref: xref + ' domain', yref: yref, x0: 0, x1: 1, y0: y, y1: y,
      line: { color: color, width: width || 1.2, dash: dash || '5 4' }, layer: 'below' });
  }
  function label(layout, xref, yref, x, y, text, color, opts) {
    opts = opts || {};
    layout.annotations.push(Object.assign({ text: text, showarrow: false, xref: xref, yref: yref, x: x, y: y,
      xanchor: 'left', yanchor: 'bottom', bgcolor: true, font: { size: 11, color: color } }, opts));
  }
  function topLabel(layout, xref, x, text, color, level) {
    layout.annotations.push({ text: text, showarrow: false, xref: xref, yref: (xref === 'x2' ? 'y2' : 'y') + ' domain',
      x: x, y: 1, xanchor: 'center', yanchor: 'bottom', yshift: 2 + 14 * (level || 0), font: { size: 11, color: color } });
  }
  function points(name, xs, ys, color, keys, opts) {
    opts = opts || {};
    return Object.assign({ type: 'scatter', mode: 'markers', name: name, x: xs, y: ys, showlegend: false,
      marker: { symbol: opts.symbol || 'circle', size: opts.size || 8, color: color, line: { color: color, width: 1.4 } },
      customdata: keys, hovertemplate: (opts.hover || 'registry %{customdata[0]} = %{customdata[1]}') + '<extra>' + name + '</extra>' }, opts.extra || {});
  }

  /* ------------------------------------------------------------------ Figure 1: the two returns */
  function payoffs(D, t, opts) {
    var P = inputs(D), narrow = !!(opts && opts.narrow);
    var xs = grid(1, 3.8, 280), traces = [];
    traces.push({ type: 'scatter', mode: 'lines', name: 'spread Δ<sub>T</sub>(r)', x: xs, y: xs.map(function (r) { return auction(P, r).Delta; }),
      line: { color: t.info, width: 2.6 }, xaxis: 'x', yaxis: 'y', legendgroup: 'DT',
      customdata: xs.map(function (r) { return [d6(auction(P, r).Delta)]; }),
      hovertemplate: 'Δ<sub>T</sub> = %{customdata[0]}<extra>spread</extra>' });
    [['M', 'top posterior M', t.ink, 'solid', 2.2], ['half', 'prior 1/2', t.ink, 'dash', 2.2], ['m', 'bottom posterior m', t.c3, 'dot', 2.6]].forEach(function (s) {
      var mu = s[0] === 'half' ? 0.5 : P[s[0]];
      traces.push({ type: 'scatter', mode: 'lines', name: 'B<sub>r</sub> at the ' + s[1], x: xs, y: xs.map(function (r) { return auction(P, r).B(mu); }),
        line: { color: s[2], width: s[4], dash: s[3] }, xaxis: 'x2', yaxis: 'y2', legendgroup: 'B' + s[0],
        customdata: xs.map(function (r) { return [d6(auction(P, r).B(mu))]; }),
        hovertemplate: 'B<sub>r</sub> = %{customdata[0]}<extra>' + s[1] + '</extra>' });
    });
    var rs = ['r0', 'r1', 'r2'];
    traces.push(points('benchmark spread', rs.map(function (k) { return P[k]; }), rs.map(function (k, i) { return P['Delta_r' + i]; }), t.info,
      rs.map(function (k, i) { return ['Delta_r' + i, P.display['Delta_r' + i]]; }), { extra: { xaxis: 'x', yaxis: 'y' } }));
    traces.push(points('gross profit at the prior', rs.map(function (k) { return P[k]; }), rs.map(function (k, i) { return P['Bprior_r' + i]; }), t.ink,
      rs.map(function (k, i) { return [i === 1 ? 'Bprior_r1_B' : 'Bprior_r' + i, P.display['Bprior_r' + i]]; }), { extra: { xaxis: 'x2', yaxis: 'y2' } }));
    var C = CCC.charts, layout = C.baseLayout(t);
    layout.height = narrow ? 600 : 380;
    layout.xaxis = C.axis(t, { title: { text: 'incumbent strength <i>r</i>' }, range: [1, 3.8], tick0: 1, dtick: 0.5 });
    layout.yaxis = C.axis(t, { title: { text: 'target-payoff spread Δ<sub><i>T</i></sub>' }, range: [0, 1.15] });
    layout.xaxis2 = C.axis(t, { title: { text: 'incumbent strength <i>r</i>' }, range: [1, 3.8], tick0: 1, dtick: 0.5 });
    layout.yaxis2 = C.axis(t, { title: { text: 'gross profit <i>B<sub>r</sub></i>(μ)' }, range: [1.5, 7.5] });
    layout.margin.l = narrow ? 72 : 64;
    C.twoPanels(layout, narrow);
    hline(layout, 'x', 'y', P.k, t.info);
    label(layout, 'x domain', 'y', 0.98, P.k, 'trading cost <i>k</i> = ' + P.display.k, t.info, { xanchor: 'right' });
    hline(layout, 'x2', 'y2', P.c_H, t.cost);
    label(layout, 'x2 domain', 'y2', 0.02, P.c_H, 'high cost <i>c<sub>H</sub></i> = ' + P.display.c_H, t.cost);
    rs.forEach(function (k, i) { ['x', 'x2'].forEach(function (ax) { vline(layout, ax, P[k], t.line); topLabel(layout, ax, P[k], '<i>r</i><sub>' + i + '</sub>', t.muted); }); });
    C.panelLabels(layout, t);
    return { traces: traces, layout: layout };
  }

  /* ------------------------------------------------------------------ Figure 2: beliefs and the ceiling */
  function beliefs(D, t, opts) {
    var P = inputs(D), narrow = !!(opts && opts.narrow), traces = [];
    var xa = grid(P.r0, P.r2, 240), xb = grid(P.r1, P.r2, 120);
    function tauTrace(xs, ax, ay, show) {
      return { type: 'scatter', mode: 'lines', name: 'threshold τ(r)', x: xs, y: xs.map(function (r) { return auction(P, r).tau; }),
        line: { color: t.cost, width: 2.6 }, xaxis: ax, yaxis: ay, legendgroup: 'tau', showlegend: show,
        customdata: xs.map(function (r) { return [d6(auction(P, r).tau)]; }), hovertemplate: 'τ = %{customdata[0]}<extra>threshold</extra>' };
    }
    traces.push(tauTrace(xa, 'x', 'y', true));
    traces.push({ type: 'scatter', mode: 'lines', name: 'top posterior M', x: [P.r0, P.r2], y: [P.M, P.M], line: { color: t.info, width: 2, dash: 'dash' },
      xaxis: 'x', yaxis: 'y', legendgroup: 'M', customdata: [[P.display.M], [P.display.M]], hovertemplate: 'M(1/2) = %{customdata[0]}<extra>top posterior</extra>' });
    traces.push({ type: 'scatter', mode: 'lines', name: 'bottom posterior m', x: [P.r0, P.r2], y: [P.m, P.m], line: { color: t.info, width: 2, dash: 'dot' },
      xaxis: 'x', yaxis: 'y', legendgroup: 'm', customdata: [[P.display.m], [P.display.m]], hovertemplate: 'm(1/2) = %{customdata[0]}<extra>bottom posterior</extra>' });
    traces.push(points('benchmark thresholds', [P.r0, P.r1, P.r2], [P.tau_r0, P.tau_r1, P.tau_r2], t.cost,
      [['tau_r0', P.display.tau_r0], ['tau_r1', P.display.tau_r1], ['tau_r2', P.display.tau_r2]], { extra: { xaxis: 'x', yaxis: 'y' } }));
    traces.push(points('entry ceiling', [P.rC], [P.M], t.ink, [['rC_B', P.display.rC]], { symbol: 'circle-open', size: 10,
      hover: 'r<sub>C</sub> = %{customdata[1]}', extra: { xaxis: 'x', yaxis: 'y' } }));
    // (b) the strengths from r_1 to r_2: the band of top posteriors that put r_C between them
    traces.push(tauTrace(xb, 'x2', 'y2', false));
    traces.push({ type: 'scatter', mode: 'lines', name: 'top posterior M', x: [P.r1, P.r2], y: [P.M, P.M], line: { color: t.info, width: 2, dash: 'dash' },
      xaxis: 'x2', yaxis: 'y2', legendgroup: 'M', showlegend: false, customdata: [[P.display.M], [P.display.M]], hovertemplate: 'M(1/2) = %{customdata[0]}<extra>top posterior</extra>' });
    traces.push(points('band ends', [P.r1, P.r2], [P.tau_r1, P.tau_r2], t.cost, [['tau_r1', P.display.tau_r1], ['tau_r2', P.display.tau_r2]], { extra: { xaxis: 'x2', yaxis: 'y2' } }));
    traces.push(points('entry ceiling', [P.rC], [P.M], t.ink, [['rC_B', P.display.rC]], { symbol: 'circle-open', size: 10,
      hover: 'r<sub>C</sub> = %{customdata[1]}', extra: { xaxis: 'x2', yaxis: 'y2' } }));
    var C = CCC.charts, layout = C.baseLayout(t);
    layout.height = narrow ? 620 : 390;
    layout.xaxis = C.axis(t, { title: { text: 'incumbent strength <i>r</i>' }, range: [P.r0, P.r2], tickvals: [1.2, 1.6, 2, 2.4, 2.8, 3.2, 3.6] });
    layout.yaxis = C.axis(t, { title: { text: 'belief' }, range: [0.2, 0.84], tickvals: [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8] });
    layout.xaxis2 = C.axis(t, { title: { text: 'incumbent strength <i>r</i>' }, range: [P.r1, P.r2], tickvals: [3, 3.2, 3.4, 3.6] });
    layout.yaxis2 = C.axis(t, { title: { text: 'belief' }, range: [0.7, 0.735], tickvals: [0.7, 0.71, 0.72, 0.73] });
    layout.margin.l = 64;
    C.twoPanels(layout, narrow);
    if (!narrow) { layout.xaxis.domain = [0, 0.58]; layout.xaxis2.domain = [0.68, 1]; }
    layout.shapes.push({ type: 'rect', xref: 'x domain', yref: 'y', x0: 0, x1: 1, y0: P.m, y1: P.M, fillcolor: t.regionC, line: { width: 0 }, layer: 'below' });
    layout.shapes.push({ type: 'rect', xref: 'x2 domain', yref: 'y2', x0: 0, x1: 1, y0: P.tau_r1, y1: P.tau_r2, fillcolor: t.regionB, line: { width: 0 }, layer: 'below' });
    hline(layout, 'x', 'y', 0.5, t.muted, '2 3', 1);
    label(layout, 'x domain', 'y', 0.02, 0.5, 'prior 1/2', t.muted);
    label(layout, 'x domain', 'y', 0.02, P.M, 'reachable beliefs: from <i>m</i> to <i>M</i>', t.info);
    label(layout, 'x2 domain', 'y2', 0.97, P.tau_r1, 'band for <i>M</i>: τ(<i>r</i><sub>1</sub>) to τ(<i>r</i><sub>2</sub>)', t.muted, { xanchor: 'right' });
    [['x', P.r0, 'r</i><sub>0</sub>'], ['x', P.r1, 'r</i><sub>1</sub>'], ['x', P.r2, 'r</i><sub>2</sub>']].forEach(function (m) {
      vline(layout, m[0], m[1], t.line); topLabel(layout, m[0], m[1], '<i>' + m[2], t.muted);
    });
    vline(layout, 'x2', P.rC, t.muted); topLabel(layout, 'x2', P.rC, '<i>r</i><sub>C</sub>', t.ink);
    vline(layout, 'x', P.rC, t.muted);
    C.panelLabels(layout, t);
    return { traces: traces, layout: layout };
  }

  /* ------------------------------------------------------------------ Figure 4: research */
  function research(D, t, opts) {
    var P = inputs(D), narrow = !!(opts && opts.narrow), traces = [], ENT = plateau(P);
    var xb = grid(P.rR, P.rRbar, 160), lam = xb.map(function (r) { return lambdaR(P, r); });
    var nodes = (D.nodes || []).map(function (n) { return { r: Number(n.r.x), lam: Number(n.lambda.x), E: Number(n.entry.x), n: n }; });
    function flat(name, x0, x1, y, color, ax, ay, group, show, dash) {
      return { type: 'scatter', mode: 'lines', name: name, x: [x0, x1], y: [y, y], line: { color: color, width: 2.4, dash: dash || 'solid' },
        xaxis: ax, yaxis: ay, legendgroup: group, showlegend: show, hovertemplate: 'skip' };
    }
    traces.push(flat('zero research', P.r0, P.rN, 0, t.ink, 'x', 'y', 'zero', true));
    traces.push({ type: 'scatter', mode: 'lines', name: 'research branch', x: xb, y: lam, line: { color: t.info, width: 2.6, dash: 'dash' },
      xaxis: 'x', yaxis: 'y', legendgroup: 'branch', customdata: xb.map(function (r, i) { return [d6(lam[i]), d6(entryResearch(P, lam[i]))]; }),
      hovertemplate: 'λ = %{customdata[0]}<br>entry = %{customdata[1]}<extra>research branch</extra>' });
    traces.push(flat('research at the cap', P.rRbar, P.rN, P.cap, t.info, 'x', 'y', 'cap', true));
    traces.push(points('research at the three strengths', nodes.map(function (n) { return n.r; }), nodes.map(function (n) { return n.lam; }), t.ink,
      nodes.map(function (n) { return [n.n.lambda.key, n.n.lambda.display]; }), { extra: { xaxis: 'x', yaxis: 'y' } }));
    traces.push(flat('zero research', P.r0, P.rN, P.rho, t.ink, 'x2', 'y2', 'zero', false));
    traces.push({ type: 'scatter', mode: 'lines', name: 'research branch', x: xb, y: lam.map(function (l) { return entryResearch(P, l); }),
      line: { color: t.info, width: 2.6, dash: 'dash' }, xaxis: 'x2', yaxis: 'y2', legendgroup: 'branch', showlegend: false,
      customdata: xb.map(function (r, i) { return [d6(entryResearch(P, lam[i])), d6(lam[i])]; }),
      hovertemplate: 'entry = %{customdata[0]}<br>λ = %{customdata[1]}<extra>research branch</extra>' });
    traces.push(flat('research at the cap', P.rRbar, P.rN, ENT, t.info, 'x2', 'y2', 'cap', false));
    traces.push(points('entry at the three strengths', nodes.map(function (n) { return n.r; }), nodes.map(function (n) { return n.E; }), t.ink,
      nodes.map(function (n) { return [n.n.entry.key, n.n.entry.display]; }), { extra: { xaxis: 'x2', yaxis: 'y2' } }));
    traces.push(points('start of the branch', [P.rR], [P.lambda_rR], t.info, [['res_lambda_rR', P.display.lambda_rR]], { extra: { xaxis: 'x', yaxis: 'y' } }));
    traces.push(points('start of the branch', [P.rR], [P.entry_rR], t.info, [['res_entry_rR', P.display.entry_rR]], { extra: { xaxis: 'x2', yaxis: 'y2' } }));
    var C = CCC.charts, layout = C.baseLayout(t);
    layout.height = narrow ? 640 : 400;
    layout.margin.t = 44;
    layout.xaxis = C.axis(t, { title: { text: 'incumbent strength <i>r</i>' }, range: [P.r0, 2], tickvals: [1.2, 1.4, 1.6, 1.8, 2] });
    layout.yaxis = C.axis(t, { title: { text: 'research λ' }, range: [-0.02, 0.4], tickvals: [0, 0.1, 0.2, 0.3, 0.4] });
    layout.xaxis2 = C.axis(t, { title: { text: 'incumbent strength <i>r</i>' }, range: [P.r0, 2], tickvals: [1.2, 1.4, 1.6, 1.8, 2] });
    layout.yaxis2 = C.axis(t, { title: { text: 'entry' }, range: [0.2, 0.58], tickvals: [0.2, 0.3, 0.4, 0.5] });
    layout.margin.l = 64;
    C.twoPanels(layout, narrow);
    ['x', 'x2'].forEach(function (ax) {
      layout.shapes.push({ type: 'rect', xref: ax, yref: (ax === 'x2' ? 'y2' : 'y') + ' domain', x0: P.rN, x1: 2, y0: 0, y1: 1, fillcolor: t.regionC, line: { width: 0 }, layer: 'below' });
      vline(layout, ax, P.rR, t.line); topLabel(layout, ax, P.rR, '<i>r</i><sub>R</sub>', t.muted, 1);
      vline(layout, ax, P.rRbar, t.line); topLabel(layout, ax, P.rRbar, '<i>r̄</i><sub>R</sub>', t.muted, 0);
      vline(layout, ax, P.rN, t.line); topLabel(layout, ax, P.rN, '<i>r</i><sub>N</sub>', t.muted, 1);
    });
    hline(layout, 'x', 'y', P.cap, t.muted, '2 3', 1);
    label(layout, 'x domain', 'y', 0.02, P.cap, 'cap λ̄ = ' + P.display.cap, t.muted);
    C.panelLabels(layout, t);
    return { traces: traces, layout: layout };
  }

  if (CCC.charts && typeof CCC.charts.register === 'function') {
    // charts.js also carries the builders of the earlier (Laplace) figures; this page has no mounts for them.
    ['fig1', 'fig2', 'fig3', 'fig4'].forEach(function (id) { delete CCC.charts.builders[id]; });
    CCC.charts.register('payoffs', payoffs, 1);
    CCC.charts.register('beliefs', beliefs, 2);
    CCC.charts.register('research', research, 4);
  }
  CCC.figures = { payoffs: payoffs, beliefs: beliefs, research: research };
})();
