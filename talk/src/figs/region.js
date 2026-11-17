/* The pictures of backup B3 redrawn from the closed forms (data-fig="region"):
     b24  the coexistence region in the plane of the shareholder spread and the threshold, with the
          example's path through it (the master's "Figure CoexRegion", panel (b));
     b25  entry against strength in the master's two panels, (a) the whole path and (c) the stretch
          around the band, with the branches N, R, F, Q, T ("Figure CoexPanelA", "Figure CoexPanelC").
   Every point comes from TALK.data.extra.charts.region (build_data_charts.py, closed forms of
   handout/figures.js; boundary strengths are registry rows) and every tick label from the numbers
   table. The page file holds the words (HTML .fig-label spans with data-place); this module only
   places them. Backups show whole: no clicks, no motion.                                          */
(function () {
  'use strict';

  const NS = 'http://www.w3.org/2000/svg';

  /* boxes in stage px: the master's picture boxes (960 x 540 pt) times 5/3, with its axes margins */
  const BOXES = {
    b24: { W: 420, H: 450, panels: { b: { x0: 82, x1: 398, y0: 372, y1: 50 } } },
    b25: {
      W: 980, H: 396,
      panels: {
        a: { x0: 80, x1: 352, y0: 306, y1: 100, ox: 0 },   // one plot box with (c): same top, same bottom
        c: { x0: 512, x1: 966, y0: 306, y1: 100, ox: 428 },
      },
    },
  };
  const R_DOT = 8;           // a marked point
  const R_OPEN = 7;          // an open circle (its ring is 3 px)
  const LEVEL = 34;          // one step up for a keyline's symbol that would touch its neighbour's

  function el(tag, attrs, parent) {
    const n = document.createElementNS(NS, tag);
    if (attrs) Object.keys(attrs).forEach((k) => n.setAttribute(k, attrs[k]));
    if (parent) parent.appendChild(n);
    return n;
  }
  const poly = (pts) => pts.map((q) => q[0].toFixed(2) + ',' + q[1].toFixed(2)).join(' ');

  TALK.figure('region', {
    mount(mountEl, ctx) {
      const data = ctx.data || {};
      const all = ((data.extra || {}).charts || {}).region;
      this.v = ctx.variant || ctx.page;
      if (!all || !all[this.v] || !BOXES[this.v]) { console.error('region: no data or box for ' + this.v); return; }
      this.D = all[this.v];
      this.box = BOXES[this.v];
      this.el = mountEl;
      this.nums = data.numbers || {};
      this.uid = 'region-' + ctx.page;
      this.made = [];
      this.anchors = {};
      const { W, H } = this.box;
      const svg = el('svg', { class: 'fig-svg', viewBox: `0 0 ${W} ${H}`, width: W, height: H, 'aria-hidden': 'true' });
      mountEl.insertBefore(svg, mountEl.firstChild);
      this.svg = svg;
      const defs = el('defs', {}, svg);
      this.defs = defs;
      this.screens = ['a', 'b'].map((letter, i) => {
        const p = el('pattern', { id: `scr-${letter}-region-${ctx.page}`, patternUnits: 'userSpaceOnUse', patternTransform: `rotate(${i ? 135 : 45})` }, defs);
        return { p, path: el('path', { class: 'screen-line' }, p) };
      });
      const L = {};
      ['shade', 'grid', 'axes', 'lines', 'marks', 'dots'].forEach((k) => { L[k] = el('g', { class: 'layer-' + k }, svg); });
      this.L = L;
      this.fills = [];
      if (this.v === 'b24') this.drawB24(); else this.drawB25();
      this.look();
    },

    numText(id) {
      const n = this.nums[id];
      if (!n) { console.error('region: no number ' + id); return '?'; }
      return n.text;
    },

    /* a panel's scales: data -> stage px */
    scales(F, xr, yr) {
      const sx = (x) => F.x0 + (x - xr[0]) / (xr[1] - xr[0]) * (F.x1 - F.x0);
      const sy = (y) => F.y0 - (y - yr[0]) / (yr[1] - yr[0]) * (F.y0 - F.y1);
      return { sx, sy, P: (q) => [sx(q[0]), sy(q[1])] };
    },

    /* L-shaped axes with outward ticks; tick labels are HTML from the numbers table */
    axes(F, s, xt, yt) {
      const L = this.L;
      el('path', { class: 'ax', d: `M${F.x0} ${F.y1}V${F.y0}H${F.x1}` }, L.axes);
      xt.forEach((t) => {
        const x = s.sx(t.v);
        el('line', { class: 'ax-tick', x1: x, x2: x, y1: F.y0, y2: F.y0 + 8 }, L.axes);
        this.made.push({ s: this.label('ax-label', this.numText(t.num)), x, y: F.y0 + 12, ax: 0.5, ay: 0 });
      });
      yt.forEach((t) => {
        const y = s.sy(t.v);
        el('line', { class: 'ax-tick', x1: F.x0 - 8, x2: F.x0, y1: y, y2: y }, L.axes);
        this.made.push({ s: this.label('ax-label', this.numText(t.num)), x: F.x0 - 12, y, ax: 1, ay: 0.5 });
      });
    },

    label(cls, html) {
      const s = document.createElement('span');
      s.className = 'fig-label ' + cls;
      s.innerHTML = html;
      this.el.appendChild(s);
      return s;
    },

    put(s, x, y, ax, ay) {
      s.style.left = (x - ax * s.offsetWidth).toFixed(1) + 'px';
      s.style.top = (y - ay * s.offsetHeight).toFixed(1) + 'px';
    },

    /* a screened area: its fill is the look's shade screen, redrawn in this figure's own pattern */
    area(pts, parent) {
      const n = el('polygon', { class: 'region-fill', points: poly(pts) }, parent);
      this.fills.push(n);
      return n;
    },

    arrowHead(tip, from, cls, parent, len = 17, half = 8) {
      const dx = tip[0] - from[0];
      const dy = tip[1] - from[1];
      const d = Math.hypot(dx, dy) || 1;
      const ux = dx / d;
      const uy = dy / d;
      const bx = tip[0] - ux * len;
      const by = tip[1] - uy * len;
      el('path', { class: cls, d: `M${tip[0].toFixed(2)} ${tip[1].toFixed(2)}L${(bx - uy * half).toFixed(2)} ${(by + ux * half).toFixed(2)}L${(bx + uy * half).toFixed(2)} ${(by - ux * half).toFixed(2)}Z` }, parent);
      return [tip[0] - ux * (len - 2), tip[1] - uy * (len - 2)];
    },

    /* ------------------------------------------------------------ b24: the region */
    drawB24() {
      const D = this.D;
      const F = this.box.panels.b;
      const s = this.scales(F, D.x_range, D.y_range);
      const { sx, sy, P } = s;
      const L = this.L;
      this.axes(F, s, D.x_ticks, D.y_ticks);

      // the region: screened, its three bounds solid, the prior pi dotted across the plot
      this.area(D.region.map(P), L.shade);
      el('polyline', { class: 'bound', points: poly(D.lower.map(P)) }, L.lines);
      el('polyline', { class: 'bound', points: poly(D.upper.map(P)) }, L.lines);
      el('polyline', { class: 'bound', points: poly(D.top.map(P)) }, L.lines);
      el('polyline', { class: 'bound-split', points: poly(D.split.map(P)) }, L.lines);
      const yM = sy(D.M);
      const yPi = sy(D.pi);
      el('line', { class: 'guide', x1: sx(D.x_lo), x2: P(D.top[0])[0], y1: yM, y2: yM }, L.grid);
      el('line', { class: 'guide', x1: sx(D.x_lo), x2: sx(D.x_hi), y1: yPi, y2: yPi }, L.grid);

      // the example's path: ink from r0 to r_A, then (where the informative market exists) green to
      // the arrowhead at the plot's edge
      const ink = D.path_ink.map(P);
      const up = D.path_up.map(P);
      el('polyline', { class: 'path path-ink', points: poly(ink) }, L.marks);
      const tip = up[up.length - 1];
      let back = up.length - 2;
      while (back > 0 && Math.hypot(tip[0] - up[back][0], tip[1] - up[back][1]) < 20) back -= 1;
      const end = this.arrowHead(tip, up[back], 'path-head path-up-head', L.marks);
      const line = up.filter((q) => q[0] <= end[0]);
      line.push(end);
      el('polyline', { class: 'path path-up', points: poly(line) }, L.marks);
      const M = D.marks;
      el('circle', { class: 'dot', cx: P(M.r0)[0], cy: P(M.r0)[1], r: R_DOT }, L.dots);
      ['rA', 'rF', 'rN'].forEach((n) => el('circle', { class: 'dot dot-end', cx: P(M[n])[0], cy: P(M[n])[1], r: R_DOT }, L.dots));

      this.anchors = {
        panel: [0, 0, 0, 0],
        ytitle: [18, (F.y0 + F.y1) / 2, 0.5, 0.5],
        xtitle: [(F.x0 + F.x1) / 2, F.y0 + 46, 0.5, 0],
        M: [sx(D.x_lo) + 8, yM - 8, 0, 1],
        pi: [sx(D.x_lo) + 8, yPi + 10, 0, 0],
        coex: [(sx(D.d_split) + sx(D.d_hi)) / 2, (yM + P(M.rF)[1]) / 2 - 22, 0.5, 0.5],
        r0: [P(M.r0)[0], P(M.r0)[1] + 18, 0.5, 0],
        rA: [P(M.rA)[0] - 10, P(M.rA)[1] - 16, 1, 1],
        rF: [P(M.rF)[0] + 16, P(M.rF)[1] - 16, 0, 1],
        rN: [P(M.rN)[0] + 12, P(M.rN)[1] + 16, 0, 0],
      };
    },

    /* ------------------------------------------------------------ b25: panels (a) and (c) */
    drawB25() {
      const D = this.D;
      const L = this.L;
      const S = D.strengths;
      const B = D.branches;
      this.pan = {};
      ['a', 'c'].forEach((name) => {
        const F = this.box.panels[name];
        const spec = D.panels[name];
        const s = this.scales(F, spec.x_range, spec.y_range);
        const { sx, sy, P } = s;
        this.pan[name] = { F, s };
        this.axes(F, s, spec.x_ticks, spec.y_ticks);
        // the branches stop at the panel's edges
        const clip = el('clipPath', { id: `clip-${this.uid}-${name}`, clipPathUnits: 'userSpaceOnUse' }, this.defs);
        el('rect', { x: F.x0, y: F.y1 - 30, width: F.x1 - F.x0, height: F.y0 - F.y1 + 30 }, clip);
        const g = (layer) => el('g', { 'clip-path': `url(#clip-${this.uid}-${name})` }, L[layer]);

        // the band [r_A, r_N]
        const xa = sx(S[D.shade.from]);
        const xb = sx(S[D.shade.to]);
        this.area([[xa, F.y1], [xb, F.y1], [xb, F.y0], [xa, F.y0]], g('shade'));
        // marked strengths: dotted keylines; in panel (c) each carries its symbol above the plot
        const levels = { rA: 1, rF: 0, rN: 1, rJ: 0, rS: 1, rC: 0 };
        spec.guides.forEach((at) => {
          const x = sx(S[at]);
          const lv = name === 'c' ? levels[at] : 0;
          const top = (at === 'rC' || name === 'c') ? F.y1 - 10 - lv * LEVEL : F.y1;
          el('line', { class: 'guide', x1: x, x2: x, y1: top, y2: F.y0 }, L.grid);
          this.anchors[`guide:${at}:${name}`] = [x, top - 4, 0.5, 1];
        });

        const lines = g('lines');
        el('polyline', { class: 'br br-thresh', points: poly(B.T.map(P)) }, lines);
        el('polyline', { class: 'br br-none', points: poly(B.N.map(P)) }, lines);
        el('polyline', { class: 'br br-q', points: poly(B.Q.map(P)) }, lines);
        el('polyline', { class: 'br br-floor', points: poly(B.Ffloor.map(P)) }, lines);
        el('polyline', { class: 'br br-mix', points: poly(B.R.map(P)) }, lines);
        el('polyline', { class: 'br br-up', points: poly(B.F.map(P)) }, lines);

        const dots = L.dots;
        const yRho = sy(D.rho);
        const yTop = sy(D.plateau);
        if (name === 'a') {
          el('circle', { class: 'dot dot-end', cx: sx(S.rC), cy: yTop, r: R_DOT }, dots);
          el('circle', { class: 'dot dot-open', cx: sx(S.rC), cy: yRho, r: R_OPEN }, dots);
          // the stretch panel (c) enlarges
          const yz = F.y1 - 20;     // above the plot, clear of the screened band it points along
          const x0 = sx(spec.zoom[0]);
          const x1 = sx(spec.zoom[1]);
          const e0 = this.arrowHead([x0, yz], [x1, yz], 'zoom-head', L.marks, 14, 7);
          const e1 = this.arrowHead([x1, yz], [x0, yz], 'zoom-head', L.marks, 14, 7);
          el('line', { class: 'zoom', x1: e0[0], x2: e1[0], y1: yz, y2: yz }, L.marks);
          const midF = (sx(S.rF) + sx(S.rC)) / 2;
          Object.assign(this.anchors, {
            'panel:a': [F.x0 - 80, 0, 0, 0],
            'ytitle:a': [18, (F.y0 + F.y1) / 2, 0.5, 0.5],
            'xtitle:a': [(F.x0 + F.x1) / 2, F.y0 + 46, 0.5, 0],
            'zoom:a': [x1 + 10, yz, 0, 0.5],
            // N under its line, centred in the band (where the line runs) and knocked out of its
            // screen: clear of the axis and of both guides
            'N:a': [(sx(S.rA) + sx(S.rN)) / 2, yRho + 10, 0.5, 0],
            'F:a': [Math.max(midF, x1 + 70), yTop - 12, 0.5, 1],
            'Ffloor:a': [sx(S.rC) - 16, yRho - 12, 1, 1],
          });
        } else {
          el('circle', { class: 'dot dot-end', cx: sx(S.rA), cy: sy(D.entry_rA), r: R_DOT }, dots);
          el('circle', { class: 'dot dot-end', cx: sx(S.rF), cy: yTop, r: R_DOT }, dots);
          el('circle', { class: 'dot dot-open', cx: sx(S.rN), cy: yRho, r: R_OPEN }, dots);
          el('circle', { class: 'dot dot-open', cx: sx(S.rJ), cy: yRho, r: R_OPEN }, dots);
          // T's letter beside its curve, past the band's right edge
          const tPts = B.T.map(P);
          const xT = sx(S.rN) + 34;
          const tAt = tPts.find((q) => q[0] >= xT) || tPts[tPts.length - 1];
          Object.assign(this.anchors, {
            'panel:c': [this.box.panels.c.ox, 0, 0, 0],
            'xtitle:c': [(F.x0 + F.x1) / 2, F.y0 + 46, 0.5, 0],
            'N:c': [F.x0 + 10, yRho + 12, 0, 0],
            'Q:c': [(sx(S.rN) + sx(S.rJ)) / 2, yRho + 12, 0.5, 0],
            'R:c': [sx(S.rA) - 12, sy(D.entry_rA) - 20, 1, 1],
            'T:c': [tAt[0] + 6, tAt[1] - 16, 0, 1],
            'F:c': [(sx(S.rS) + F.x1) / 2, yTop - 12, 0.5, 1],
            'coex:c': [(sx(S.rF) + sx(S.rN)) / 2, F.y0 - 10, 0.5, 1],
          });
        }
      });
    },

    /* ------------------------------------------------------------ labels and the look */
    place() {
      if (!this.box) return;
      this.made.forEach(({ s, x, y, ax, ay }) => this.put(s, x, y, ax, ay));
      this.el.querySelectorAll(':scope > .fig-label[data-place]').forEach((s) => {
        const a = this.anchors[s.dataset.place];
        if (!a) { console.error('region: unknown label place ' + s.dataset.place); return; }
        this.put(s, a[0], a[1], a[2], a[3]);
      });
    },

    look() {
      if (!this.el) return;
      // the look's line screen and its ink are set on the entry chart's mount: copy them, so the
      // region is screened as page 17's is
      const entry = document.querySelector('.fig[data-fig="entry"]');
      const src = entry ? getComputedStyle(entry) : getComputedStyle(this.el);
      ['--scr-ink', '--scr-w', '--scr-pitch'].forEach((k) => {
        const v = src.getPropertyValue(k).trim();
        if (v) this.el.style.setProperty(k, v);
      });
      const pitch = parseFloat(src.getPropertyValue('--scr-pitch')) || 9;
      this.screens.forEach(({ p, path }) => {
        p.setAttribute('width', pitch);
        p.setAttribute('height', pitch);
        path.setAttribute('d', `M0 0V${pitch}`);
      });
      const fill = getComputedStyle(this.el).getPropertyValue('--fig-shade-fill').trim() || 'var(--fig-shade)';
      const mine = fill.replace(/#scr-([ab])-entry/, `#scr-$1-region-${this.uid.slice(7)}`);
      this.fills.forEach((n) => { n.style.fill = mine; });
      this.place();
    },

    setStep() { if (this.box) this.place(); },
    finish() {},
    isMoving() { return false; },
  });
})();
