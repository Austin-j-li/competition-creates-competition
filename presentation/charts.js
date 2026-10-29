/* charts.js: the SVG renderer of the slides' figures, without a chart library.
 *
 * A trimmed copy of the renderer in handout/charts.js (its tokens, geometry, SVG drawing, legend
 * and hover readout), kept here so that the slides depend on no other page's builders. A figure
 * is a plain spec { traces, layout }: traces carry x, y, line, marker, hovertemplate; the layout
 * carries axes, shapes and annotations. draw(el, spec, tokens, state) turns a spec into SVG with a
 * legend, a hover readout and a keyboard cursor (arrow keys move it, Shift moves it faster).
 * Neither the renderer nor the specs solve anything. ES2019, no modules. Exposes window.CCC.charts.
 */
(function () {
  'use strict';

  var CCC = (window.CCC = window.CCC || {});
  var SVGNS = 'http://www.w3.org/2000/svg';
  var FALLBACK = {
    bg: '#ffffff', surface: '#f2f2f2', ink: '#1c1c1c', muted: '#666666', grid: '#e6e6e6', line: '#c9c9c9',
    accent: '#1c1c1c', accentSoft: 'rgba(122,31,31,0.08)', c2: '#7a1f1f', c3: '#666666',
    regionA: 'rgba(28,28,28,0.07)', regionB: 'rgba(122,31,31,0.08)', regionC: 'rgba(102,102,102,0.12)',
    info: '#7a1f1f', cost: '#1c1c1c',
    fontSans: '"Libertinus Sans", "Libertinus Math", Arial, sans-serif',
    fontMono: 'ui-monospace, Menlo, monospace'
  };
  var VARS = {
    bg: '--bg', surface: '--surface', ink: '--ink', muted: '--muted', grid: '--grid', line: '--line',
    accent: '--chart-1', accentSoft: '--accent-soft', c2: '--chart-2', c3: '--chart-3',
    regionA: '--region-a', regionB: '--region-b', regionC: '--region-c',
    info: '--c-info', cost: '--c-cost',
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

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; });
  }
  function num(v) { return v === null || v === undefined || v === '' ? NaN : Number(v); }
  function px(v) { return (Math.round(v * 10) / 10).toString(); }

  /* Rich text in the trace-spec convention (<i>, <sub>, <sup>, <b>, entities) to SVG tspans, one line. */
  function rich(text) {
    // A subscript tspan shifts the baseline by 0.3 of its own (0.75) size; the text after it
    // carries the opposite shift in the parent size, so the baseline returns.
    var out = '', stack = [], pending = 0, re = /<(\/?)(i|sub|sup|b)>|<br\s*\/?>|([^<]+)/g, m;
    var s = String(text);
    function flush() {
      if (!pending) return '';
      var d = '<tspan dy="' + pending + 'em">​</tspan>';
      pending = 0;
      return d;
    }
    while ((m = re.exec(s))) {
      if (m[3] !== undefined) {
        var txt = esc(m[3].replace(/&nbsp;/g, ' ').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&'));
        if (pending) { out += '<tspan dy="' + pending + 'em">' + txt + '</tspan>'; pending = 0; }
        else out += txt;
      } else if (m[2]) {
        if (m[1]) {
          var tag = stack.pop();
          out += '</tspan>';
          if (tag === 'sub') pending += -0.225;
          else if (tag === 'sup') pending += 0.2625;
        } else {
          out += flush();
          stack.push(m[2]);
          if (m[2] === 'i') out += '<tspan font-style="italic">';
          else if (m[2] === 'b') out += '<tspan font-weight="600">';
          else if (m[2] === 'sub') out += '<tspan dy="0.3em" font-size="75%">';
          else out += '<tspan dy="-0.35em" font-size="75%">';
        }
      }
    }
    while (stack.length) { stack.pop(); out += '</tspan>'; }
    return out;
  }

  function niceTicks(lo, hi, n) {
    var span = hi - lo, step = Math.pow(10, Math.floor(Math.log10(span / n)));
    var err = span / n / step;
    if (err >= 7.5) step *= 10; else if (err >= 3.5) step *= 5; else if (err >= 1.5) step *= 2;
    var out = [];
    for (var v = Math.ceil(lo / step) * step; v <= hi + step * 1e-9; v += step) out.push(Math.round(v / step) * step);
    return out;
  }

  function tickText(v) {
    var s = String(Math.round(v * 1e9) / 1e9);
    return s.charAt(0) === '-' ? '−' + s.slice(1) : s;
  }

  function axisKey(ref) { return ref.replace(/ domain$/, ''); }
  function layoutKey(k, kind) { return kind + 'axis' + (k.length > 1 ? k.slice(1) : ''); }

  /* Build axis geometry for every axis named in the layout. */
  function geometry(spec, W) {
    var L = spec.layout, m = L.margin || { l: 56, r: 16, t: 40, b: 52 };
    var H = L.height || 380;
    var pw = Math.max(40, W - m.l - m.r), ph = Math.max(40, H - m.t - m.b);
    var axes = {};
    ['x', 'x2', 'y', 'y2'].forEach(function (k) {
      var kind = k.charAt(0), a = L[layoutKey(k, kind)];
      if (!a) return;
      var dom = a.domain || [0, 1], log = a.type === 'log';
      var range = a.range ? a.range.slice() : null;
      if (!range) {
        var lo = Infinity, hi = -Infinity;
        spec.traces.forEach(function (tr) {
          if ((tr[kind + 'axis'] || kind) !== k) return;
          (tr[kind] || []).forEach(function (v) { v = num(v); if (isFinite(v)) { lo = Math.min(lo, v); hi = Math.max(hi, v); } });
        });
        if (!isFinite(lo)) { lo = 0; hi = 1; }
        var pad = (hi - lo || 1) * 0.05; range = [lo - pad, hi + pad];
      }
      var p0, p1;
      if (kind === 'x') { p0 = m.l + dom[0] * pw; p1 = m.l + dom[1] * pw; }
      else { p0 = m.t + (1 - dom[0]) * ph; p1 = m.t + (1 - dom[1]) * ph; }
      var f = function (v) {
        v = num(v);
        if (log) v = v > 0 ? Math.log10(v) : NaN;
        return p0 + (v - range[0]) / (range[1] - range[0]) * (p1 - p0);
      };
      var ticks;
      if (a.tickvals) ticks = a.tickvals.map(function (v, i) { return { v: v, label: a.ticktext ? a.ticktext[i] : tickText(v) }; });
      else if (a.dtick) {
        ticks = [];
        var start = a.tick0 !== undefined ? a.tick0 : 0;
        var first = start + Math.ceil((range[0] - start) / a.dtick - 1e-9) * a.dtick;
        for (var v = first; v <= range[1] + 1e-9; v += a.dtick) ticks.push({ v: Math.round(v * 1e9) / 1e9, label: tickText(v) });
      } else ticks = niceTicks(range[0], range[1], 5).map(function (v) { return { v: v, label: tickText(v) }; });
      axes[k] = { key: k, kind: kind, a: a, map: f, p0: Math.min(p0, p1), p1: Math.max(p0, p1), range: range, log: log, ticks: ticks };
    });
    return { W: W, H: H, m: m, pw: pw, ph: ph, axes: axes };
  }

  function refX(G, ref, v) {
    if (ref === 'paper') return G.m.l + v * G.pw;
    var ax = G.axes[axisKey(ref)];
    if (/ domain$/.test(ref)) return ax.p0 + v * (ax.p1 - ax.p0);
    return ax.map(v);
  }
  function refY(G, ref, v) {
    if (ref === 'paper') return G.m.t + (1 - v) * G.ph;
    var ax = G.axes[axisKey(ref)];
    if (/ domain$/.test(ref)) return ax.p1 - v * (ax.p1 - ax.p0);
    return ax.map(v);
  }

  function dashArray(dash, w) {
    w = w || 2;
    if (!dash || dash === 'solid') return '';
    if (dash === 'dash') return (3 * w) + ' ' + (2 * w);
    if (dash === 'dot') return '0.1 ' + (2 * w);
    if (dash === 'dashdot') return (3 * w) + ' ' + (1.5 * w) + ' 0.1 ' + (1.5 * w);
    return dash;
  }

  function symbolPath(sym, x, y, size) {
    var r = size / 2;
    switch (sym) {
      case 'diamond': case 'diamond-open':
        r *= 1.25;
        return 'M' + px(x) + ',' + px(y - r) + 'L' + px(x + r) + ',' + px(y) + 'L' + px(x) + ',' + px(y + r) + 'L' + px(x - r) + ',' + px(y) + 'Z';
      case 'triangle-up':
        return 'M' + px(x) + ',' + px(y - r * 1.15) + 'L' + px(x + r) + ',' + px(y + r * 0.6) + 'L' + px(x - r) + ',' + px(y + r * 0.6) + 'Z';
      case 'triangle-down':
        return 'M' + px(x) + ',' + px(y + r * 1.15) + 'L' + px(x + r) + ',' + px(y - r * 0.6) + 'L' + px(x - r) + ',' + px(y - r * 0.6) + 'Z';
      case 'line-ns':
        return 'M' + px(x) + ',' + px(y - r * 1.6) + 'L' + px(x) + ',' + px(y + r * 1.6);
      default:
        return 'M' + px(x - r) + ',' + px(y) + 'a' + px(r) + ',' + px(r) + ' 0 1,0 ' + px(2 * r) + ',0a' + px(r) + ',' + px(r) + ' 0 1,0 ' + px(-2 * r) + ',0Z';
    }
  }

  function markerSvg(sym, x, y, size, color, lineSpec, bg, opacity) {
    var open = /-open$/.test(sym) || sym === 'line-ns';
    var d = symbolPath(sym, x, y, size);
    var sw = lineSpec && lineSpec.width !== undefined ? lineSpec.width : (open ? 1.6 : 0);
    var stroke = open ? color : (lineSpec && lineSpec.color ? lineSpec.color : color);
    return '<path class="mk mk-' + esc(sym) + '" d="' + d + '" fill="' + (open ? (sym === 'line-ns' ? 'none' : bg) : color) + '"' +
      ' stroke="' + stroke + '" stroke-width="' + (open ? Math.max(1.4, sw) : sw) + '"' + (opacity !== undefined ? ' opacity="' + opacity + '"' : '') + '/>';
  }

  function legendKey(tr, i) { return tr.legendgroup || ('trace-' + i); }

  function traceSvg(G, tr, bg) {
    var xa = G.axes[tr.xaxis || 'x'], ya = G.axes[tr.yaxis || 'y'];
    if (!xa || !ya) return '';
    var mode = tr.mode || 'lines', out = '';
    var xs = tr.x || [], ys = tr.y || [];
    if (/lines/.test(mode)) {
      var d = '', move = true;
      for (var i = 0; i < xs.length; i++) {
        var X = num(xs[i]), Y = num(ys[i]);
        var px1 = xa.map(X), py1 = ya.map(Y);
        if (!isFinite(px1) || !isFinite(py1)) { move = true; continue; }
        d += (move ? 'M' : 'L') + px(px1) + ',' + px(py1);
        move = false;
      }
      var ln = tr.line || {};
      var da = dashArray(ln.dash, ln.width);
      var filled = tr.fill === 'toself' && tr.fillcolor;
      if (d) out += '<path class="tr-line" d="' + d + (filled ? 'Z' : '') + '" fill="' + (filled ? tr.fillcolor : 'none') + '" stroke="' + ln.color + '" stroke-width="' + (ln.width || 2) + '"' +
        (da ? ' stroke-dasharray="' + da + '"' : '') + ' stroke-linecap="round" stroke-linejoin="round"/>';
    }
    if (tr.error_y && tr.error_y.visible !== false) {
      var e = tr.error_y, w = e.width || 6;
      for (var j = 0; j < xs.length; j++) {
        var cx = xa.map(xs[j]), yhi = ya.map(num(ys[j]) + num(e.array[j])), ylo = ya.map(num(ys[j]) - num(e.arrayminus[j]));
        if (!isFinite(cx) || !isFinite(yhi) || !isFinite(ylo)) continue;
        out += '<path class="err-bar" d="M' + px(cx) + ',' + px(ylo) + 'L' + px(cx) + ',' + px(yhi) + 'M' + px(cx - w / 2) + ',' + px(yhi) + 'L' + px(cx + w / 2) + ',' + px(yhi) +
          'M' + px(cx - w / 2) + ',' + px(ylo) + 'L' + px(cx + w / 2) + ',' + px(ylo) + '" stroke="' + e.color + '" stroke-width="' + (e.thickness || 1.2) + '" fill="none"/>';
      }
    }
    if (/markers/.test(mode)) {
      var mk = tr.marker || {};
      if (!(mode === 'lines+markers' && (mk.size || 6) <= 2)) {
        for (var k = 0; k < xs.length; k++) {
          var mx = xa.map(xs[k]), my = ya.map(ys[k]);
          if (!isFinite(mx) || !isFinite(my)) continue;
          var sym = Array.isArray(mk.symbol) ? mk.symbol[k] : (mk.symbol || 'circle');
          var size = Array.isArray(mk.size) ? mk.size[k] : (mk.size || 6);
          out += markerSvg(sym, mx, my, size, mk.color || (tr.line && tr.line.color), mk.line, bg, mk.opacity);
        }
      }
    }
    return out;
  }

  function shapeSvg(G, s) {
    var x0 = refX(G, s.xref || 'x', s.x0), x1 = refX(G, s.xref || 'x', s.x1);
    var y0 = refY(G, s.yref || 'y', s.y0), y1 = refY(G, s.yref || 'y', s.y1);
    if (![x0, x1, y0, y1].every(isFinite)) return '';
    var ln = s.line || {};
    if (s.type === 'rect') {
      return '<rect class="shape-rect" x="' + px(Math.min(x0, x1)) + '" y="' + px(Math.min(y0, y1)) + '" width="' + px(Math.abs(x1 - x0)) + '" height="' + px(Math.abs(y1 - y0)) + '" fill="' + s.fillcolor + '"' +
        (ln.width ? ' stroke="' + ln.color + '" stroke-width="' + ln.width + '"' : '') + '/>';
    }
    var da = dashArray(ln.dash, ln.width || 1);
    return '<line class="shape-line" x1="' + px(x0) + '" y1="' + px(y0) + '" x2="' + px(x1) + '" y2="' + px(y1) + '" stroke="' + (ln.color || '#888') + '" stroke-width="' + (ln.width || 1) + '"' + (da ? ' stroke-dasharray="' + da + '"' : '') + '/>';
  }

  function annotationSvg(G, a, bg) {
    var x = refX(G, a.xref || 'x', a.x) + (a.xshift || 0);
    var y = refY(G, a.yref || 'y', a.y) - (a.yshift || 0);
    if (!isFinite(x) || !isFinite(y)) return '';
    var size = (a.font && a.font.size) || 12, color = (a.font && a.font.color) || 'currentColor';
    var lines = String(a.text).split(/<br\s*\/?>/);
    var anchor = a.xanchor === 'left' ? 'start' : (a.xanchor === 'right' ? 'end' : 'middle');
    var lh = size * 1.2, total = lh * lines.length;
    var top = a.yanchor === 'bottom' ? y - total : (a.yanchor === 'top' ? y : y - total / 2);
    var out = '<text class="ann' + (a.panel ? ' panel-label' : '') + '" x="' + px(x) + '" font-size="' + size + '" fill="' + color + '" text-anchor="' + anchor + '"' +
      (a.bgcolor ? ' stroke="' + bg + '" stroke-width="4" paint-order="stroke" stroke-linejoin="round"' : '') + '>';
    lines.forEach(function (l, i) { out += '<tspan x="' + px(x) + '" y="' + px(top + lh * (i + 0.8)) + '">' + rich(l) + '</tspan>'; });
    out += (a.hovertext ? '<title>' + esc(a.hovertext) + '</title>' : '') + '</text>';
    return out;
  }

  function axesSvg(G, t) {
    var out = '';
    Object.keys(G.axes).forEach(function (k) {
      var ax = G.axes[k], a = ax.a;
      var other = G.axes[a.anchor || (ax.kind === 'x' ? 'y' + k.slice(1) : 'x' + k.slice(1))];
      if (!other) return;
      if (ax.kind === 'y') {
        var xl = other.p0, xr = other.p1;
        ax.ticks.forEach(function (tk) {
          var y = ax.map(tk.v);
          if (!isFinite(y) || y < ax.p0 - 0.5 || y > ax.p1 + 0.5) return;
          out += '<line class="grid" x1="' + px(xl) + '" x2="' + px(xr) + '" y1="' + px(y) + '" y2="' + px(y) + '" stroke="' + t.grid + '"/>';
          if (a.showticklabels !== false) out += '<text class="tick" x="' + px(xl - 7) + '" y="' + px(y + 4) + '" text-anchor="end" fill="' + t.ink + '">' + esc(tk.label) + '</text>';
          out += '<line x1="' + px(xl - 4) + '" x2="' + px(xl) + '" y1="' + px(y) + '" y2="' + px(y) + '" stroke="' + t.line + '"/>';
        });
        out += '<line class="axis-line" x1="' + px(xl) + '" x2="' + px(xl) + '" y1="' + px(ax.p0) + '" y2="' + px(ax.p1) + '" stroke="' + t.line + '"/>';
        if (a.title && a.title.text) {
          var cy = (ax.p0 + ax.p1) / 2, tx = xl - (G.m.l - 14);
          out += '<text class="axis-title" transform="translate(' + px(tx) + ',' + px(cy) + ') rotate(-90)" text-anchor="middle" fill="' + t.ink + '">' + rich(a.title.text) + '</text>';
        }
      } else {
        var yb = other.p1;
        ax.ticks.forEach(function (tk) {
          var x = ax.map(tk.v);
          if (!isFinite(x) || x < ax.p0 - 0.5 || x > ax.p1 + 0.5) return;
          out += '<line class="grid" x1="' + px(x) + '" x2="' + px(x) + '" y1="' + px(other.p0) + '" y2="' + px(yb) + '" stroke="' + t.grid + '"/>';
          out += '<line x1="' + px(x) + '" x2="' + px(x) + '" y1="' + px(yb) + '" y2="' + px(yb + 4) + '" stroke="' + t.line + '"/>';
          if (a.showticklabels !== false) out += '<text class="tick" x="' + px(x) + '" y="' + px(yb + 17) + '" text-anchor="middle" fill="' + t.ink + '">' + esc(tk.label) + '</text>';
        });
        out += '<line class="axis-line" x1="' + px(ax.p0) + '" x2="' + px(ax.p1) + '" y1="' + px(yb) + '" y2="' + px(yb) + '" stroke="' + t.line + '"/>';
        if (a.title && a.title.text) out += '<text class="axis-title" x="' + px((ax.p0 + ax.p1) / 2) + '" y="' + px(yb + 36) + '" text-anchor="middle" fill="' + t.ink + '">' + rich(a.title.text) + '</text>';
      }
    });
    return out;
  }

  function swatch(tr, bg) {
    var ln = tr.line || {}, mk = tr.marker || {}, mode = tr.mode || 'lines', s = '';
    if (/lines/.test(mode)) {
      var da = dashArray(ln.dash, Math.min(ln.width || 2, 2.2));
      s += '<line x1="2" x2="28" y1="7" y2="7" stroke="' + ln.color + '" stroke-width="' + Math.min(ln.width || 2, 2.4) + '"' + (da ? ' stroke-dasharray="' + da + '"' : '') + ' stroke-linecap="round"/>';
    }
    if (/markers/.test(mode) && (mode === 'markers' || (mk.size || 0) > 2)) {
      var sym = Array.isArray(mk.symbol) ? mk.symbol[0] : (mk.symbol || 'circle');
      s += markerSvg(sym, 15, 7, Math.min(9, Array.isArray(mk.size) ? 8 : (mk.size || 7)), mk.color, mk.line, bg);
      if (tr.error_y) s += '<path d="M15,1L15,13M11,1L19,1M11,13L19,13" stroke="' + tr.error_y.color + '" stroke-width="1" fill="none"/>';
    }
    return '<svg class="swatch" viewBox="0 0 30 14" width="30" height="14" aria-hidden="true">' + s + '</svg>';
  }

  /* Substitute a hovertemplate for point i. Returns {label, body}. */
  function hoverText(tr, i) {
    var tpl = tr.hovertemplate;
    if (!tpl || tpl === 'skip') return null;
    var cd = tr.customdata ? tr.customdata[i] : undefined;
    var label = tr.name || '';
    var ex = /<extra>([\s\S]*?)<\/extra>/.exec(tpl);
    if (ex) { label = ex[1]; tpl = tpl.replace(ex[0], ''); }
    var body = tpl.replace(/%\{([a-z]+)(?:\[(\d+)\])?(?::\.(\d+)f)?\}/g, function (_, field, k, dec) {
      var v;
      if (field === 'customdata') v = k !== undefined ? (cd ? cd[Number(k)] : undefined) : cd;
      else if (field === 'text') v = Array.isArray(tr.text) ? tr.text[i] : tr.text;
      else v = tr[field] ? tr[field][i] : undefined;
      if (v === undefined || v === null) return 'n/a';
      if (dec !== undefined) return Number(v).toFixed(Number(dec));
      return String(v);
    });
    return { label: label, body: body };
  }

  /* ------------------------------------------------------------------ chart objects */
  /* The SVG markup of a spec at width W. Pure: no DOM access, so the display check can call it. */
  function svgMarkup(spec, t, W, opts) {
    opts = opts || {};
    var hidden = opts.hidden || {};
    var G = geometry(spec, W);
    var bg = t.bg;
    var below = '', above = '', body = '';
    (spec.layout.shapes || []).forEach(function (s) { if (s.layer === 'below') below += shapeSvg(G, s); else above += shapeSvg(G, s); });
    var anns = '';
    (spec.layout.annotations || []).forEach(function (a) { anns += annotationSvg(G, a, bg); });
    var clips = '', clipId = 'clip-' + (opts.id || 'chart') + '-';
    var plots = {};
    spec.traces.forEach(function (tr) { plots[(tr.xaxis || 'x') + (tr.yaxis || 'y')] = [tr.xaxis || 'x', tr.yaxis || 'y']; });
    Object.keys(plots).forEach(function (k) {
      var xa = G.axes[plots[k][0]], ya = G.axes[plots[k][1]];
      if (!xa || !ya) return;
      clips += '<clipPath id="' + clipId + k + '"><rect x="' + px(xa.p0 - 6) + '" y="' + px(ya.p0 - 6) + '" width="' + px(xa.p1 - xa.p0 + 12) + '" height="' + px(ya.p1 - ya.p0 + 12) + '"/></clipPath>';
    });
    // group traces by subplot so each clips to its own axes
    var bySub = {};
    spec.traces.forEach(function (tr, i) {
      if (hidden[legendKey(tr, i)]) return;
      var k = (tr.xaxis || 'x') + (tr.yaxis || 'y');
      bySub[k] = (bySub[k] || '') + '<g class="trace" data-trace="' + i + '">' + traceSvg(G, tr, bg) + '</g>';
    });
    Object.keys(bySub).forEach(function (k) { body += '<g clip-path="url(#' + clipId + k + ')">' + bySub[k] + '</g>'; });
    var svg = '<svg class="plot" xmlns="' + SVGNS + '" viewBox="0 0 ' + G.W + ' ' + G.H + '" width="' + G.W + '" height="' + G.H + '" role="img" aria-label="' + esc(opts.label || 'Chart') + '"' +
      ' font-family="' + esc(t.fontSans) + '"><defs>' + clips + '</defs>' + below + axesSvg(G, t) + body + above + anns + '<g class="cursor"></g></svg>';
    return { svg: svg, G: G };
  }

  /* Draw a spec into el. Used by the handout figures and by the slides. */
  function draw(el, spec, t, state) {
    state = state || {};
    var hidden = state.hidden || (state.hidden = {});
    // state.zoom > 1 draws a narrower plot that CSS scales up, so text and marks grow together.
    var W = Math.max(280, Math.round((el.clientWidth || state.width || 640) / (state.zoom || 1)));
    var bg = t.bg;
    var out = svgMarkup(spec, t, W, { hidden: hidden, id: el.id, label: el.getAttribute('aria-label') || state.label });
    var G = out.G, svg = out.svg;

    // legend: one button per legend entry; a button toggles its legend group
    var legend = '', seenGroup = {}, seenTitle = {};
    spec.traces.forEach(function (tr, i) {
      if (tr.showlegend === false || !tr.name) return;
      var key = legendKey(tr, i);
      if (seenGroup[key]) return;
      seenGroup[key] = true;
      if (tr.legendgrouptitle && !seenTitle[tr.legendgrouptitle.text]) {
        seenTitle[tr.legendgrouptitle.text] = true;
        legend += '<span class="legend-title">' + tr.legendgrouptitle.text + '</span>';
      }
      legend += '<button type="button" class="legend-item" data-key="' + esc(key) + '" aria-pressed="' + (hidden[key] ? 'false' : 'true') + '">' + swatch(tr, bg) + '<span>' + tr.name + '</span></button>';
    });
    el.innerHTML = (legend ? '<div class="chart-legend" role="group" aria-label="Show or hide a series">' + legend + '</div>' : '') +
      '<div class="chart-canvas">' + svg + '<div class="chart-tip" hidden></div></div>';
    el.setAttribute('data-mounted', 'true');
    state.G = G; state.spec = spec; state.t = t;
    wire(el, state);
    return state;
  }

  /* Hover and keyboard readout: an x-unified cursor per subplot. */
  function wire(el, state) {
    var spec = state.spec, G = state.G;
    var svg = el.querySelector('svg.plot'), tip = el.querySelector('.chart-tip'), cur = svg.querySelector('.cursor');
    Array.prototype.forEach.call(el.querySelectorAll('.legend-item'), function (b) {
      b.addEventListener('click', function () {
        var k = b.getAttribute('data-key');
        state.hidden[k] = !state.hidden[k];
        draw(el, spec, state.t, state);
        var again = el.querySelector('.legend-item[data-key="' + k.replace(/"/g, '\\"') + '"]');
        if (again) again.focus();
      });
    });
    function subplotAt(sx, sy) {
      var best = null;
      Object.keys(G.axes).forEach(function (k) {
        var xa = G.axes[k];
        if (xa.kind !== 'x') return;
        var ya = G.axes[xa.a.anchor || ('y' + k.slice(1))];
        if (!ya) return;
        if (sx >= xa.p0 - 4 && sx <= xa.p1 + 4 && sy >= ya.p0 - 8 && sy <= ya.p1 + 8) best = [xa, ya];
      });
      return best;
    }
    function show(xa, ya, sx) {
      var rows = [], dots = '';
      spec.traces.forEach(function (tr, i) {
        if (state.hidden[legendKey(tr, i)]) return;
        if ((tr.xaxis || 'x') !== xa.key || (tr.yaxis || 'y') !== ya.key) return;
        var best = -1, bd = Infinity;
        (tr.x || []).forEach(function (v, j) {
          if (v === null || tr.y[j] === null) return;
          var d = Math.abs(xa.map(v) - sx);
          if (d < bd) { bd = d; best = j; }
        });
        if (best < 0 || bd > 8) return;
        var h = hoverText(tr, best);
        if (!h) return;
        var color = (tr.line && tr.line.color) || (tr.marker && tr.marker.color) || state.t.ink;
        rows.push('<div class="tip-row"><span class="tip-key" style="background:' + color + '"></span><span><b>' + h.label + '</b><br>' + h.body + '</span></div>');
        var py = ya.map(tr.y[best]);
        if (isFinite(py)) dots += '<circle cx="' + px(xa.map(tr.x[best])) + '" cy="' + px(py) + '" r="3.5" fill="' + color + '" stroke="' + state.t.bg + '" stroke-width="1.5"/>';
      });
      var xv = xa.range[0] + (sx - xa.p0) / (xa.p1 - xa.p0) * (xa.range[1] - xa.range[0]);
      cur.innerHTML = '<line x1="' + px(sx) + '" x2="' + px(sx) + '" y1="' + px(ya.p0) + '" y2="' + px(ya.p1) + '" stroke="' + state.t.muted + '" stroke-width="1"/>' + dots;
      if (!rows.length) { tip.hidden = true; return; }
      var titled = xa.a.title && xa.a.title.text ? xa : null;
      if (!titled) Object.keys(G.axes).forEach(function (k) { var o = G.axes[k]; if (!titled && o.kind === 'x' && (o.a.matches === xa.key || xa.a.matches === k) && o.a.title && o.a.title.text) titled = o; });
      var title = titled ? titled.a.title.text.replace(/<[^>]+>/g, '') : 'x';
      tip.innerHTML = '<div class="tip-head">' + esc(title) + ' ≈ ' + esc(xa.log ? Math.pow(10, xv).toPrecision(3) : xv.toFixed(3)) + '</div>' + rows.join('');
      tip.hidden = false;
      // Layout pixels, not screen pixels: the slides scale the whole stage with a transform.
      var cw = svg.parentNode.offsetWidth || svg.getBoundingClientRect().width, scale = cw / G.W;
      var left = sx * scale + 14, wTip = tip.offsetWidth;
      if (left + wTip > cw) left = Math.max(0, sx * scale - wTip - 14);
      tip.style.left = left + 'px';
      tip.style.top = Math.max(0, ya.p0 * scale) + 'px';
      state.cursor = { x: xa.key, y: ya.key, sx: sx };
    }
    function hide() { tip.hidden = true; cur.innerHTML = ''; }
    svg.addEventListener('pointermove', function (ev) {
      var box = svg.getBoundingClientRect(), scale = G.W / box.width;
      var sx = (ev.clientX - box.left) * scale, sy = (ev.clientY - box.top) * scale;
      var sp = subplotAt(sx, sy);
      if (!sp) { hide(); return; }
      show(sp[0], sp[1], Math.max(sp[0].p0, Math.min(sp[0].p1, sx)));
    });
    svg.addEventListener('pointerleave', hide);
    var host = el.closest('figure') || el;
    if (!host.__cccKeys) {
      host.__cccKeys = true;
      host.addEventListener('keydown', function (ev) {
        var st = el.__cccState;
        if (!st || ev.target.closest('button, input, a, summary')) return;
        if (ev.key === 'Escape') { el.querySelector('.chart-tip').hidden = true; el.querySelector('.cursor').innerHTML = ''; return; }
        if (ev.key !== 'ArrowLeft' && ev.key !== 'ArrowRight') return;
        ev.preventDefault();
        var Gs = st.G, c = st.cursor, xa, ya;
        if (c) { xa = Gs.axes[c.x]; ya = Gs.axes[c.y]; }
        else { xa = Gs.axes.x; ya = Gs.axes[xa.a.anchor || 'y']; }
        var step = (xa.p1 - xa.p0) * (ev.shiftKey ? 0.1 : 0.02);
        var sx = c ? c.sx + (ev.key === 'ArrowRight' ? step : -step) : xa.p0;
        st.show(xa, ya, Math.max(xa.p0, Math.min(xa.p1, sx)));
      });
    }
    state.show = show;
    el.__cccState = state;
  }

  CCC.charts = { tokens: tokens, draw: draw, svgMarkup: svgMarkup, hoverText: hoverText, geometry: geometry };
})();
