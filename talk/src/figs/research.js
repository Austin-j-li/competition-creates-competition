/* The research chart: research λ against incumbent strength r (page 18, data-variant="p18"), and
   research and entry against strength in two small panels (backup B12, second page,
   data-variant="b47"). Curves and printed numbers come from TALK.data: the closed forms of
   handout/figures.js (lambdaR, entryResearch) as written by build_data_charts.py into
   src/data_charts.json (TALK.data.extra.charts.research), and the numbers table. The page file holds
   the words (HTML .fig-label spans with data-place); this module only places them.

   It shares the entry chart's drawing conventions and classes (figs.css): .ax, .br-none, .br-up,
   .br-floor, .br-drop, .dot, .dot-end, .shade, .bracket. Motion is the entry chart's: a forward click
   draws its lines left to right behind a clip that grows along x, each dot arriving when the line
   reaches it; areas wipe along x. Web Animations only, so a key press finishes it.               */
(function () {
  'use strict';

  const NS = 'http://www.w3.org/2000/svg';
  const DRAW_EASE = [0.33, 1, 0.68, 1];
  const EASE = 'cubic-bezier(.16,1,.3,1)';

  /* page 18: the master's boxes (960 x 540 pt) times 5/3, the mount's origin at (42, 105) pt */
  const P18 = {
    W: 850, H: 482,
    F: { x0: 126.67, x1: 843.33, y0: 412, y1: 96.67 },
    bracketY: 63.33, bracketH: 10,
  };
  /* B12: two panels side by side */
  const B47 = {
    W: 980, H: 450,
    panels: {
      lambda: { x0: 112, x1: 452, y0: 350, y1: 70 },
      entry: { x0: 618, x1: 958, y0: 350, y1: 70 },
    },
  };

  function el(tag, attrs, parent) {
    const n = document.createElementNS(NS, tag);
    if (attrs) Object.keys(attrs).forEach((k) => n.setAttribute(k, attrs[k]));
    if (parent) parent.appendChild(n);
    return n;
  }

  function bezierTimeAt(p, b) {
    const [x1, y1, x2, y2] = b;
    const cub = (t, a, c) => 3 * a * t * (1 - t) * (1 - t) + 3 * c * t * t * (1 - t) + t * t * t;
    let lo = 0;
    let hi = 1;
    for (let i = 0; i < 40; i++) {
      const s = (lo + hi) / 2;
      if (cub(s, y1, y2) < p) lo = s; else hi = s;
    }
    return cub((lo + hi) / 2, x1, x2);
  }

  const poly = (pts) => pts.map((q) => q[0].toFixed(2) + ',' + q[1].toFixed(2)).join(' ');

  TALK.figure('research', {
    mount(mountEl, ctx) {
      const data = ctx.data || {};
      const R = ((data.extra || {}).charts || {}).research;
      if (!R) { console.error('research: no data (src/data_charts.json)'); return; }
      this.el = mountEl;
      this.v = ctx.variant || ctx.page;
      this.R = R;
      this.nums = data.numbers || {};
      this.anims = [];
      this.step = 0;
      this.uid = 'research-' + ctx.page;
      this.stepGroups = new Map();
      this.made = [];
      this.anchors = {};

      const box = this.v === 'b47' ? B47 : P18;
      this.box = box;
      const svg = el('svg', { class: 'fig-svg', viewBox: `0 0 ${box.W} ${box.H}`, width: box.W, height: box.H, 'aria-hidden': 'true' });
      mountEl.insertBefore(svg, mountEl.firstChild);
      this.svg = svg;
      const defs = el('defs', {}, svg);
      this.defs = defs;
      this.screens = ['a', 'b'].map((letter, i) => {
        const p = el('pattern', { id: `scr-${letter}-research`, patternUnits: 'userSpaceOnUse', patternTransform: `rotate(${i ? 135 : 45})` }, defs);
        return { p, path: el('path', { class: 'screen-line' }, p) };
      });
      const clip = el('clipPath', { id: 'clip-' + this.uid, clipPathUnits: 'userSpaceOnUse' }, defs);
      this.clipRect = el('rect', { class: 'draw-clip', x: 0, y: -60, width: box.W, height: box.H + 120 }, clip);

      const L = {};
      ['shade', 'grid', 'axes', 'lines', 'markers', 'dots'].forEach((k) => { L[k] = el('g', { class: 'layer-' + k }, svg); });
      this.L = L;
      this._g = {};
      this.group = (layer, step) => {
        if (!step) return L[layer];
        const key = layer + ':' + step;
        if (!this._g[key]) {
          const g = el('g', { 'data-step': step, class: 'step-g' }, L[layer]);
          this._g[key] = g;
          if (!this.stepGroups.has(step)) this.stepGroups.set(step, []);
          this.stepGroups.get(step).push(g);
        }
        return this._g[key];
      };

      if (this.v === 'b47') this.drawB47(); else this.drawP18();
      this.look();
    },

    numText(id) {
      const n = this.nums[id];
      if (!n) { console.error('research: no number ' + id); return '?'; }
      return n.text;
    },

    label(cls, html, o) {
      const s = document.createElement('span');
      s.className = 'fig-label ' + cls;
      s.innerHTML = html;
      if (o.step) s.dataset.step = o.step;
      this.el.appendChild(s);
      this.made.push({ s, o });
      return s;
    },

    put(s, x, y, ax, ay) {
      s.style.left = (x - ax * s.offsetWidth).toFixed(1) + 'px';
      s.style.top = (y - ay * s.offsetHeight).toFixed(1) + 'px';
    },

    /* ------------------------------------------------------------ page 18 */
    drawP18() {
      const R = this.R;
      const spec = R.pages.p18;
      const F = P18.F;
      const S = R.strengths;
      const [rx0, rx1] = spec.x_range;
      const [ry0, ry1] = spec.y_range;
      const sx = (r) => F.x0 + (r - rx0) / (rx1 - rx0) * (F.x1 - F.x0);
      const sy = (y) => F.y0 - (y - ry0) / (ry1 - ry0) * (F.y0 - F.y1);
      this.sx = sx;
      this.sy = sy;
      const L = this.L;
      const g = this.group;
      const CHART = 2;          // the chart arrives with the second click (the dump's order)
      const ENTRY = 3;
      const SHADE = 4;

      // axes: the strength axis at the foot; research 0 stands a little above it, as in the master
      el('path', { class: 'ax', d: `M${F.x0} ${F.y1}V${F.y0}H${F.x1}` }, g('axes', CHART));
      spec.y_ticks.forEach((t) => {
        const y = sy(t.y);
        el('line', { class: 'ax-tick', x1: F.x0 - 8, x2: F.x0, y1: y, y2: y }, g('axes', CHART));
        let html = this.numText(t.num);
        if (t.prefix_label) html = (TALK.math[t.prefix_label] || '?') + (t.prefix_join || ' ') + html;
        this.label('ax-label', html, { x: F.x0 - 14, y, ax: 1, ay: 0.5, step: CHART });
      });
      spec.x_ticks.forEach((t) => {
        const x = sx(t.r);
        el('line', { class: 'ax-tick', x1: x, x2: x, y1: F.y0, y2: F.y0 + 8 }, g('axes', CHART));
        this.label('ax-label', this.numText(t.num), { x, y: F.y0 + 14, ax: 0.5, ay: 0, step: CHART });
      });

      // shading over the strengths with more than one equilibrium, with its bracket
      const xa = sx(S[spec.shade.from]);
      const xb = sx(S[spec.shade.to]);
      const sg = g('shade', SHADE);
      this.shadeRect = el('rect', { class: 'shade', x: xa, y: F.y1, width: xb - xa, height: F.y0 - F.y1 }, sg);
      el('line', { class: 'shade-edge', x1: xa, x2: xa, y1: F.y1, y2: F.y0 }, sg);
      el('line', { class: 'shade-edge', x1: xb, x2: xb, y1: F.y1, y2: F.y0 }, sg);
      const by = P18.bracketY;
      el('path', { class: 'bracket', d: `M${xa} ${by + P18.bracketH}V${by}H${xb}V${by + P18.bracketH}` }, g('lines', SHADE));
      this.anchors.bracket = { x: (xa + xb) / 2, y: by - 6 };

      // no research: research 0 from the left edge to r_N, where that equilibrium ends
      const y0 = sy(0);
      el('polyline', { class: 'br br-none', points: poly([[F.x0, y0], [sx(S.rN), y0]]) }, g('lines', CHART));
      el('circle', { class: 'dot dot-stop', cx: sx(S.rN), cy: y0, r: 6 }, g('dots', CHART));

      // a purchase attracts the costly rival: research rises from r_R to the cap, then stays at the
      // cap past the right edge (an arrowhead at the axis' end)
      const yCap = sy(R.cap);
      const tip = F.x1;
      const AW = 17;
      const AH = 9;
      const rise = R.rise.lambda.map(([r, l]) => [sx(r), sy(l)]);
      rise.push([tip - AW + 1, yCap]);
      el('polyline', { class: 'br br-up', points: poly(rise) }, g('lines', CHART));
      el('path', { class: 'arrow', d: `M${tip - AW} ${yCap - AH}L${tip} ${yCap}L${tip - AW} ${yCap + AH}Z` }, g('lines', CHART));
      el('circle', { class: 'dot dot-end', cx: rise[0][0], cy: rise[0][1], r: 6 }, g('dots', CHART));

      // the weak incumbent
      const xr0 = sx(S.r0);
      el('circle', { class: 'dot', 'data-inc': 0, cx: xr0, cy: y0, r: 8 }, g('dots', CHART));

      this.anchors.p18 = { sx, sy, F, S, y0, yCap, rise };
      this.steps = { CHART, ENTRY, SHADE };
    },

    /* ------------------------------------------------------------ B12, second page */
    drawB47() {
      const R = this.R;
      const spec = R.pages.b47;
      const S = R.strengths;
      const [rx0, rx1] = spec.x_range;
      const L = this.L;
      this.panels = {};
      ['lambda', 'entry'].forEach((name) => {
        const F = B47.panels[name];
        const [ry0, ry1] = spec.panels[name].y_range;
        const sx = (r) => F.x0 + (r - rx0) / (rx1 - rx0) * (F.x1 - F.x0);
        const sy = (y) => F.y0 - (y - ry0) / (ry1 - ry0) * (F.y0 - F.y1);
        this.panels[name] = { F, sx, sy };
        el('path', { class: 'ax', d: `M${F.x0} ${F.y1}V${F.y0}H${F.x1}` }, L.axes);
        // marked strengths: dotted keylines in both panels; their symbols stand over panel (a), as
        // in the master
        ['rR', 'rcap', 'rN', 'rQ', 'rC'].forEach((at) => {
          const x = sx(S[at]);
          const lift = name === 'lambda' && at === 'rcap' ? 34 : 0;
          el('line', { class: 'guide', x1: x, x2: x, y1: F.y1 - 4 - lift, y2: F.y0 }, L.grid);
        });
        // the three incumbents on the strength axis
        ['r0', 'r1', 'r2'].forEach((at) => {
          const x = sx(S[at]);
          el('line', { class: 'ax-tick', x1: x, x2: x, y1: F.y0, y2: F.y0 + 8 }, L.axes);
        });
        const isL = name === 'lambda';
        const lo = isL ? 0 : R.rho;
        const top = isL ? R.cap : R.entry_cap;
        const tick = (y) => el('line', { class: 'ax-tick', x1: F.x0 - 8, x2: F.x0, y1: sy(y), y2: sy(y) }, L.axes);
        tick(lo);
        tick(top);
        // the cap: a dotted level from the axis to r_lambda-bar, where research reaches it
        if (isL) el('line', { class: 'guide', x1: F.x0, x2: sx(S.rcap), y1: sy(top), y2: sy(top) }, L.grid);
        // zero research (entry rho) on [r0, rN]
        el('polyline', { class: 'br br-none', points: poly([[sx(S.r0), sy(lo)], [sx(S.rN), sy(lo)]]) }, L.lines);
        el('circle', { class: 'dot dot-stop', cx: sx(S.rN), cy: sy(lo), r: 6 }, L.markers);
        // floor-entry research on (r_N, r_Q): research lambda_Q rises from zero, entry stays at rho;
        // the branch ends in an open circle at r_Q
        const fe = R.floor_entry[name].map(([r, y]) => [sx(r), sy(y)]);
        el('polyline', { class: 'br br-q', points: poly(fe) }, L.lines);
        el('circle', { class: 'dot dot-open', cx: sx(S.rQ), cy: sy(isL ? R.floor_entry.lambda_rQ : R.rho), r: 7 }, L.markers);
        // recruiting research: rises from r_R to the cap at r_lambda-bar, holds at the cap to r_C
        const pts = R.rise[name].map(([r, y]) => [sx(r), sy(y)]);
        pts.push([sx(S.rC), sy(top)]);
        el('polyline', { class: 'br br-up', points: poly(pts) }, L.lines);
        el('circle', { class: 'dot dot-end', cx: pts[0][0], cy: pts[0][1], r: 6 }, L.markers);
        el('circle', { class: 'dot dot-end', cx: sx(S.rcap), cy: sy(top), r: 6 }, L.markers);
        el('circle', { class: 'dot dot-end', cx: sx(S.rC), cy: sy(top), r: 6 }, L.markers);
        // past r_C only the cap remains and a purchase no longer brings the rival in: the master
        // draws it in the floor-entry pattern (research at the cap, entry rho, from an open circle)
        const after = isL ? R.cap : R.rho;
        el('polyline', { class: 'br br-q', points: poly([[sx(S.rC), sy(after)], [sx(S.r2), sy(after)]]) }, L.lines);
        if (!isL) el('circle', { class: 'dot dot-open', cx: sx(S.rC), cy: sy(after), r: 7 }, L.markers);
        // the incumbents' equilibria: zero research at r0, the cap at r1 and r2
        [['r0', lo, 0], ['r1', top, 1], ['r2', after, 2]].forEach(([at, y, inc]) => {
          el('circle', { class: 'dot', 'data-inc': inc, cx: sx(S[at]), cy: sy(y), r: 8 }, L.dots);
        });
      });
      this.steps = {};
    },

    /* ------------------------------------------------------------ labels */
    place() {
      if (!this.box) return;
      this.made.forEach(({ s, o }) => this.put(s, o.x, o.y, o.ax, o.ay));
      if (this.v === 'b47') return this.placeB47();
      const A = this.anchors.p18;
      if (!A) return;
      const { sx, F, S, y0, yCap, rise } = A;
      this.el.querySelectorAll(':scope > .fig-label[data-place]').forEach((s) => {
        switch (s.dataset.place) {
          case 'ytitle': this.put(s, F.x0 - 14, F.y1 - 4, 1, 0.5); break;
          case 'xtitle': this.put(s, (F.x0 + F.x1) / 2, F.y0 + 42, 0.5, 0); break;
          case 'bracket': s.style.textAlign = 'center'; this.put(s, this.anchors.bracket.x, this.anchors.bracket.y, 0.5, 1); break;
          case 'r0': this.put(s, sx(S.r0), y0 - 16, 0.5, 1); break;
          case 'none': this.put(s, sx(S.rR) + 14, y0 - 16, 0, 1); break;
          case 'cap': this.put(s, sx(S.rcap) + 24, yCap - 16, 0, 1); break;
          case 'attracts': this.put(s, sx(S.rcap) + 24, yCap + 14, 0, 0); break;
          case 'entry-cap': this.put(s, sx(S.rcap) + 24, yCap + 14 + 80, 0, 0); break;
          case 'entry-rR': this.put(s, rise[0][0] - 18, rise[0][1], 1, 0.5); break;
          default: console.error('research: unknown label place ' + s.dataset.place);
        }
      });
    },

    placeB47() {
      const S = this.R.strengths;
      const R = this.R;
      this.el.querySelectorAll(':scope > .fig-label[data-place]').forEach((s) => {
        const [kind, arg, panel] = s.dataset.place.split(':');
        const P = this.panels[panel || arg] || this.panels.lambda;
        const { F, sx, sy } = P;
        const isL = P === this.panels.lambda;
        const yLo = sy(isL ? 0 : R.rho);
        const yTop = sy(isL ? R.cap : R.entry_cap);
        switch (kind) {
          // the axis titles run up the axis, as in the master; the panel letters stand above them
          case 'ytitle': this.put(s, F.x0 - (isL ? 92 : 128), (F.y0 + F.y1) / 2, 0.5, 0.5); break;
          case 'panel': this.put(s, F.x0 - (isL ? 106 : 142), 0, 0, 0); break;
          case 'xtitle': this.put(s, (F.x0 + F.x1) / 2, F.y0 + 50, 0.5, 0); break;
          case 'ytick': {
            const y = arg === 'lo' ? (isL ? 0 : R.rho) : (isL ? R.cap : R.entry_cap);
            this.put(s, F.x0 - 14, sy(y), 1, 0.5);
            break;
          }
          case 'inc': this.put(s, sx(S[arg]), F.y0 + 12, 0.5, 0); break;
          case 'guide': {
            // r_R and r_N stand at one height, r_lambda-bar between them one step higher
            // r_N stands just right of its keyline, clear of r_lambda-bar's (as in the master)
            const level = arg === 'rcap' ? 1 : 0;
            if (arg === 'rN') this.put(s, sx(S[arg]) + 3, F.y1 - 8, 0, 1);
            else this.put(s, sx(S[arg]), F.y1 - 8 - level * 34, 0.5, 1);
            break;
          }
          case 'zero': this.put(s, sx(S.r0) + 16, yLo - 12, 0, 1); break;
          case 'recruiting': this.put(s, (sx(S.rQ) + sx(S.rC)) / 2, yTop - 12, 0.5, 1); break;
          case 'floor': {
            const yQ = isL ? sy(R.floor_entry.lambda_rQ) : yLo;
            if (isL) this.put(s, sx(S.rQ) + 16, (yQ + yLo) / 2, 0, 0.5);
            else this.put(s, sx(S.rQ) + 14, yLo - 12, 0, 1);
            break;
          }
          default: console.error('research: unknown label place ' + s.dataset.place);
        }
      });
    },

    look() {
      if (!this.el) return;
      // the look's line screen and its ink: the entry chart's, which the look sets (on page 18 the
      // region is screened as page 17's is)
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
      if (this.shadeRect) {
        const fill = getComputedStyle(this.el).getPropertyValue('--fig-shade-fill').trim() || 'var(--fig-shade)';
        this.shadeRect.style.fill = fill.replace(/#scr-([ab])-entry/, '#scr-$1-research');
      }
      this.place();
    },

    /* ------------------------------------------------------------ steps and motion */
    setStep(step, opts) {
      if (!this.box) return;
      this.stopMotion();
      this.step = step;
      const o = opts || {};
      const forwardClick = o.animate && o.from && o.from.page === o.page && step === o.from.step + 1;
      if (forwardClick) this.play(step);
      if (o.animate) this.guard(step);
    },

    /* The look's script (plate.js) lays every new step element in with a clip-path wipe of its own,
       which would replace this figure's drawing (a CSS clip-path overrides the clip-path attribute).
       The engine calls setStep before it announces the state, so a microtask queued here runs after
       the look has started its wipes: finish those on this figure's SVG step groups and keep the
       figure's own motion. */
    guard(step) {
      const groups = this.stepGroups.get(step) || [];
      if (!groups.length) return;
      queueMicrotask(() => groups.forEach((g) => g.getAnimations({ subtree: true }).forEach((a) => {
        // finish (not cancel): the look then clears its clip itself and its text wipes run on
        if (!this.anims.includes(a)) { try { a.finish(); } catch (err) { /* gone */ } }
      })));
    },

    play(step) {
      const all = this.stepGroups.get(step) || [];
      const axes = all.filter((g) => g.closest('.layer-axes'));
      const groups = all.filter((g) => !g.closest('.layer-dots') && !g.closest('.layer-axes'));
      const dots = all.filter((g) => g.closest('.layer-dots'));
      const easing = `cubic-bezier(${DRAW_EASE.join(',')})`;
      // axes arrive with the text; they carry no data
      axes.forEach((g) => this.anims.push(g.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 220, easing: EASE })));
      let xa = Infinity;
      let xb = -Infinity;
      groups.forEach((g) => {
        let b;
        try { b = g.getBBox(); } catch (err) { b = null; }
        if (b && (b.width || b.height)) { xa = Math.min(xa, b.x); xb = Math.max(xb, b.x + b.width); }
      });
      if (!(xb > xa)) return;
      // the lines are drawn as strength rises: a clip that grows along x over this click's marks
      const pad = 14;
      const x0 = xa - pad;
      const span = xb - xa + 2 * pad;
      const dur = Math.round(Math.min(450, 300 + span / 3));
      this.clipRect.setAttribute('x', x0.toFixed(1));
      this.clipRect.setAttribute('width', span.toFixed(1));
      groups.forEach((g) => g.setAttribute('clip-path', `url(#clip-${this.uid})`));
      const a = this.clipRect.animate([{ transform: 'scaleX(0)' }, { transform: 'scaleX(1)' }], { duration: dur, easing });
      this.anims.push(a);
      a.finished.then(() => groups.forEach((g) => g.removeAttribute('clip-path')), () => {});
      dots.forEach((g) => g.querySelectorAll('circle').forEach((c) => {
        const p = Math.max(0, Math.min(1, (+c.getAttribute('cx') - x0) / span));
        const delay = Math.round(dur * bezierTimeAt(p, DRAW_EASE));
        this.anims.push(c.animate([{ opacity: 0, transform: 'scale(.4)' }, { opacity: 1, transform: 'scale(1)' }],
          { duration: 160, delay, easing: EASE, fill: 'backwards' }));
      }));
    },

    stopMotion() {
      this.anims.forEach((a) => { try { a.cancel(); } catch (err) { /* gone */ } });
      this.anims = [];
      if (this.svg) this.svg.querySelectorAll('[clip-path]').forEach((g) => g.removeAttribute('clip-path'));
    },

    finish() {
      this.anims.forEach((a) => { try { a.finish(); } catch (err) { /* gone */ } });
      this.stopMotion();
    },

    isMoving() {
      return this.anims.some((a) => a.playState === 'running');
    },
  });
})();
