/* Hand-built SVG charts for the mockups. Reads window.CCC_DATA.fig1 (figures_data/two_returns.csv)
 * and window.CCC.closed. Colours come from CSS variables, so the themes restyle the drawings.
 * Hover and arrow keys move a cursor that snaps to the CSV grid; the readout says "figure data".
 * The threshold chart's slider readout is a fixed-order calculation, not an equilibrium solver.
 * ES2019, no modules. Exposes window.CCC.charts.
 */
(function () {
  'use strict';
  var CCC = (window.CCC = window.CCC || {});
  var SVGNS = 'http://www.w3.org/2000/svg';

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function f3(x) { return Number(x).toPrecision(3); }
  function fmt(x, d) { return Number(x).toFixed(d === undefined ? 3 : d); }

  function frame(opts) {
    var w = opts.w, h = opts.h, left = opts.left || 58, right = w - (opts.right || 18), top = opts.top || 30, bottom = h - (opts.bottom || 44);
    var X = function (x) { return left + (x - opts.xmin) / (opts.xmax - opts.xmin) * (right - left); };
    var Y = function (y) { return bottom - (y - opts.ymin) / (opts.ymax - opts.ymin) * (bottom - top); };
    return { w: w, h: h, left: left, right: right, top: top, bottom: bottom, X: X, Y: Y };
  }

  function axes(F, o) {
    var s = '';
    (o.yticks || []).forEach(function (y) {
      s += '<line class="grid" x1="' + F.left + '" y1="' + F.Y(y).toFixed(1) + '" x2="' + F.right + '" y2="' + F.Y(y).toFixed(1) + '"/>';
      s += '<text class="tick" x="' + (F.left - 8) + '" y="' + (F.Y(y) + 4).toFixed(1) + '" text-anchor="end">' + esc(o.yfmt ? o.yfmt(y) : y) + '</text>';
    });
    s += '<line class="axis" x1="' + F.left + '" y1="' + F.top + '" x2="' + F.left + '" y2="' + F.bottom + '"/>';
    s += '<line class="axis" x1="' + F.left + '" y1="' + F.bottom + '" x2="' + F.right + '" y2="' + F.bottom + '"/>';
    (o.xticks || []).forEach(function (x) {
      s += '<line class="axis" x1="' + F.X(x).toFixed(1) + '" y1="' + F.bottom + '" x2="' + F.X(x).toFixed(1) + '" y2="' + (F.bottom + 5) + '"/>';
      s += '<text class="tick" x="' + F.X(x).toFixed(1) + '" y="' + (F.bottom + 20) + '" text-anchor="middle">' + esc(x) + '</text>';
    });
    if (o.ylabel) s += '<text class="label" x="' + F.left + '" y="' + (F.top - 12) + '">' + esc(o.ylabel) + '</text>';
    if (o.xlabel) s += '<text class="tick" x="' + F.right + '" y="' + (F.h - 6) + '" text-anchor="end">' + esc(o.xlabel) + '</text>';
    if (o.panel) s += '<text class="panel" x="' + (F.left - 48) + '" y="' + (F.top - 12) + '">' + esc(o.panel) + '</text>';
    return s;
  }

  function path(F, xs, ys, cls, dash) {
    var d = '', move = true;
    for (var i = 0; i < xs.length; i++) {
      var y = Number(ys[i]);
      if (!isFinite(y)) { move = true; continue; }
      d += (move ? 'M' : 'L') + F.X(Number(xs[i])).toFixed(1) + ',' + F.Y(y).toFixed(1) + ' ';
      move = false;
    }
    return '<path class="curve ' + cls + '" d="' + d.trim() + '"' + (dash ? ' stroke-dasharray="' + dash + '"' : '') + '/>';
  }

  function vline(F, x, label, cls, side) {
    var s = '<line class="marked ' + (cls || '') + '" x1="' + F.X(x).toFixed(1) + '" y1="' + F.top + '" x2="' + F.X(x).toFixed(1) + '" y2="' + F.bottom + '"/>';
    if (label) s += '<text class="tick" x="' + (F.X(x) + (side === 'left' ? -5 : 5)).toFixed(1) + '" y="' + (F.top + 12) + '" text-anchor="' + (side === 'left' ? 'end' : 'start') + '">' + esc(label) + '</text>';
    return s;
  }

  function nearest(arr, x) {
    var best = 0, d = Infinity;
    for (var i = 0; i < arr.length; i++) { var e = Math.abs(Number(arr[i]) - x); if (e < d) { d = e; best = i; } }
    return best;
  }

  /* Pointer and keyboard cursor over a frame; calls onMove(xValue) with the data x. */
  function cursor(svg, F, host, onMove, opts) {
    var hit = document.createElementNS(SVGNS, 'rect');
    hit.setAttribute('x', F.left); hit.setAttribute('y', F.top);
    hit.setAttribute('width', F.right - F.left); hit.setAttribute('height', F.bottom - F.top);
    hit.setAttribute('fill', 'transparent'); hit.setAttribute('class', 'hit');
    svg.appendChild(hit);
    function toX(ev) {
      var r = svg.getBoundingClientRect();
      var px = (ev.clientX - r.left) * (F.w / r.width);
      return opts.xmin + (px - F.left) / (F.right - F.left) * (opts.xmax - opts.xmin);
    }
    hit.addEventListener('pointermove', function (ev) { onMove(toX(ev)); });
    hit.addEventListener('pointerdown', function (ev) { onMove(toX(ev)); });
    host.addEventListener('keydown', function (ev) {
      if (ev.key !== 'ArrowLeft' && ev.key !== 'ArrowRight') return;
      if (ev.target && ev.target.tagName === 'INPUT') return;
      ev.preventDefault();
      var cur = Number(host.dataset.cursor || opts.start);
      onMove(cur + (ev.key === 'ArrowRight' ? 1 : -1) * (ev.shiftKey ? 0.1 : 0.01));
    });
  }

  /* X1: the two returns. Panel (a) Delta_T(r); panel (b) B_r(mu) at 1/2 (deck) or at m, 1/2, M (handout). */
  function twoReturns(host, o) {
    var D = window.CCC_DATA, f = D.fig1, P = CCC.closed.inputs();
    var mode = o.mode || 'deck';
    var w = o.width || 560, h = o.height || 300;
    var xmin = 1, xmax = 3.8;
    var A = frame({ w: w, h: h, xmin: xmin, xmax: xmax, ymin: 0, ymax: 1.1 });
    var ymaxB = mode === 'deck' ? 5.2 : 7.5, yminB = mode === 'deck' ? 3.8 : 2;
    var B = frame({ w: w, h: h, xmin: xmin, xmax: xmax, ymin: yminB, ymax: ymaxB });
    var marks = o.markers || [{ r: P.r_weak, label: 'weak r₀ = ' + P.r_weak }, { r: P.r_strong, label: 'strong r₁ = ' + P.r_strong }];
    var keys = Object.keys(f.B);
    var kM = keys[nearest(keys, 0.73)], kH = keys[nearest(keys, 0.5)], km = keys[nearest(keys, 0.27)];

    var sa = axes(A, { yticks: [0, 0.5, 1], xticks: [1, 1.5, 2, 2.5, 3, 3.5], ylabel: 'target-payoff spread Δ_T', xlabel: 'incumbent strength r', panel: '(a)' });
    marks.forEach(function (mk) { sa += vline(A, mk.r, mk.label, 'guide', mk.r > 2.6 ? 'left' : 'right'); });
    sa += path(A, f.r, f.Delta_T, 'info');
    sa += '<g class="cursor" data-panel="a"></g>';

    var sb = axes(B, { yticks: mode === 'deck' ? [4, 4.5, 5] : [2, 4, 6], xticks: [1, 1.5, 2, 2.5, 3, 3.5], ylabel: mode === 'deck' ? 'challenger profit at the prior, B_r(½)' : 'challenger profit B_r(μ)', xlabel: 'incumbent strength r', panel: '(b)' });
    marks.forEach(function (mk) { sb += vline(B, mk.r, '', 'guide'); });
    if (mode === 'deck') {
      sb += path(B, f.r, f.B[kH], 'ink');
    } else {
      sb += path(B, f.r, f.B[kM], 'ink'); sb += path(B, f.r, f.B[kH], 'ink2', '6 5'); sb += path(B, f.r, f.B[km], 'ink3', '2 4');
      var iL = f.r.length - 1;
      sb += '<text class="tick" x="' + (B.X(Number(f.r[iL])) - 4) + '" y="' + (B.Y(Number(f.B[kM][iL])) - 6) + '" text-anchor="end">best price (M)</text>';
      sb += '<text class="tick" x="' + (B.X(Number(f.r[iL])) - 4) + '" y="' + (B.Y(Number(f.B[kH][iL])) - 6) + '" text-anchor="end">prior (½)</text>';
      sb += '<text class="tick" x="' + (B.X(Number(f.r[iL])) - 4) + '" y="' + (B.Y(Number(f.B[km][iL])) - 6) + '" text-anchor="end">worst price (m)</text>';
    }
    sb += '<g class="cursor" data-panel="b"></g>';

    host.innerHTML = '<div class="panels">' +
      '<svg class="plot" viewBox="0 0 ' + w + ' ' + h + '" role="img" aria-label="Panel (a): target-payoff spread against incumbent strength">' + sa + '</svg>' +
      '<svg class="plot" viewBox="0 0 ' + w + ' ' + h + '" role="img" aria-label="Panel (b): challenger profit against incumbent strength">' + sb + '</svg>' +
      '</div><p class="readout" aria-live="polite"></p>';
    var svgs = host.querySelectorAll('svg'), ro = host.querySelector('.readout');
    var cA = svgs[0].querySelector('.cursor'), cB = svgs[1].querySelector('.cursor');
    function move(x) {
      x = Math.max(xmin, Math.min(xmax, x));
      var i = nearest(f.r, x), r = Number(f.r[i]);
      host.dataset.cursor = r;
      var dT = Number(f.Delta_T[i]), bH = Number(f.B[kH][i]);
      cA.innerHTML = '<line class="cursor-line" x1="' + A.X(r).toFixed(1) + '" y1="' + A.top + '" x2="' + A.X(r).toFixed(1) + '" y2="' + A.bottom + '"/><circle class="dot info" cx="' + A.X(r).toFixed(1) + '" cy="' + A.Y(dT).toFixed(1) + '" r="4.5"/>';
      var dots = '<line class="cursor-line" x1="' + B.X(r).toFixed(1) + '" y1="' + B.top + '" x2="' + B.X(r).toFixed(1) + '" y2="' + B.bottom + '"/>';
      var ys = mode === 'deck' ? [bH] : [Number(f.B[kM][i]), bH, Number(f.B[km][i])];
      ys.forEach(function (y) { dots += '<circle class="dot ink" cx="' + B.X(r).toFixed(1) + '" cy="' + B.Y(y).toFixed(1) + '" r="4.5"/>'; });
      cB.innerHTML = dots;
      ro.innerHTML = 'At r = <b>' + fmt(r, 3) + '</b>: Δ<sub>T</sub> = <b>' + fmt(dT, 4) + '</b>, B<sub>r</sub>(½) = <b>' + fmt(bH, 3) + '</b>' +
        (mode === 'deck' ? '' : ', B<sub>r</sub>(M) = <b>' + fmt(ys[0], 3) + '</b>, B<sub>r</sub>(m) = <b>' + fmt(ys[2], 3) + '</b>') +
        ' <span class="muted">figure data, figures_data/two_returns.csv; the two marked strengths carry registry values</span>';
    }
    cursor(svgs[0], A, host, move, { xmin: xmin, xmax: xmax, start: P.r_weak });
    cursor(svgs[1], B, host, move, { xmin: xmin, xmax: xmax, start: P.r_weak });
    move(o.start || P.r_weak);
    return { move: move };
  }

  /* X2: profit at three beliefs against strength, cost lines inside the picture, slider marker. */
  function thresholds(host, o) {
    var D = window.CCC_DATA, f = D.fig1, P = CCC.closed.inputs();
    var w = o.width || 640, h = o.height || 360;
    var xmin = 1, xmax = 3.8;
    var F = frame({ w: w, h: h, xmin: xmin, xmax: xmax, ymin: 0.5, ymax: 7.5, left: 50 });
    var keys = Object.keys(f.B);
    var kM = keys[nearest(keys, 0.73)], kH = keys[nearest(keys, 0.5)], km = keys[nearest(keys, 0.27)];
    var s = axes(F, { yticks: [1, 2, 3, 4, 5, 6, 7], xticks: [1, 1.5, 2, 2.5, 3, 3.5], ylabel: 'challenger expected gross profit B_r(μ)', xlabel: 'incumbent strength r' });
    s += '<line class="cost" x1="' + F.left + '" y1="' + F.Y(P.c_H).toFixed(1) + '" x2="' + F.right + '" y2="' + F.Y(P.c_H).toFixed(1) + '"/>';
    s += '<text class="tick cost-label" x="' + (F.left + 6) + '" y="' + (F.Y(P.c_H) - 5).toFixed(1) + '">expensive cost c_H = ' + P.c_H + '</text>';
    s += '<line class="cost" stroke-dasharray="6 5" x1="' + F.left + '" y1="' + F.Y(P.c_L).toFixed(1) + '" x2="' + F.right + '" y2="' + F.Y(P.c_L).toFixed(1) + '"/>';
    s += '<text class="tick cost-label" x="' + (F.left + 6) + '" y="' + (F.Y(P.c_L) - 5).toFixed(1) + '">cheap cost c_L = ' + P.c_L + '</text>';
    s += vline(F, P.r_weak, 'weak r₀', 'guide', 'right') + vline(F, P.r_strong, 'strong r₁', 'guide', 'left') + vline(F, P.r_collapse, 'stronger still r₂', 'guide', 'right');
    s += path(F, f.r, f.B[kM], 'ink') + path(F, f.r, f.B[kH], 'ink2', '6 5') + path(F, f.r, f.B[km], 'ink3', '2 4');
    var iL = f.r.length - 1;
    [[kM, 'best price (M)'], [kH, 'prior (½)'], [km, 'worst price (m)']].forEach(function (t) {
      s += '<text class="tick" x="' + (F.X(Number(f.r[iL])) - 4) + '" y="' + (F.Y(Number(f.B[t[0]][iL])) - 6) + '" text-anchor="end">' + t[1] + '</text>';
    });
    s += '<g class="cursor"></g>';
    host.innerHTML = '<svg class="plot" viewBox="0 0 ' + w + ' ' + h + '" role="img" aria-label="Challenger profit at the worst, prior and best belief against incumbent strength, with the two cost lines">' + s + '</svg>';
    var cur = host.querySelector('.cursor');
    function update(r) {
      var c = CCC.closed.closedForms(P, r);
      var x = F.X(r).toFixed(1);
      cur.innerHTML = '<line class="cursor-line" x1="' + x + '" y1="' + F.top + '" x2="' + x + '" y2="' + F.bottom + '"/>' +
        [c.B_M, c.B_prior, c.B_m].map(function (y) { return '<circle class="dot ink" cx="' + x + '" cy="' + F.Y(y).toFixed(1) + '" r="5"/>'; }).join('');
      return c;
    }
    return { update: update };
  }

  CCC.charts = { twoReturns: twoReturns, thresholds: thresholds, nearest: nearest, f3: f3, fmt: fmt };
})();
