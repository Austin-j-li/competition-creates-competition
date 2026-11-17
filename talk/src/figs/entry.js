/* The entry chart: entry against incumbent strength, one module for pages 19, 20 and 22
   (data-variant="p14|p16|p17"). Every curve, mark and printed number comes from TALK.data
   (src/data.json); the page file holds the words (HTML .fig-label spans inside the mount), and
   this module only places them. The plot frame has the same box on every page: the master's
   boxes (960 x 540 pt) times 5/3, shifted so that its top line of labels starts at the mount.

   Steps are the engine's: every SVG group and label with data-step is shown by the engine.
   This module adds the motion of a forward click (lines drawn left to right behind a clip that
   grows along x, each dot arriving when the line reaches it), page 20's turn of the full model
   into a pale trace, and the strength control (key S).                                       */
(function () {
  'use strict';

  const NS = 'http://www.w3.org/2000/svg';
  const W = 850;                      // the mount, in stage px (pages 19, 20, 22)
  const H = 570;
  const F = { x0: 116.67, x1: 825, y0: 483.33, y1: 91.67 };   // plot frame: left, right, bottom, top
  const BOX = { W, H, F };            // a variant may bring a box of its own (spec.box)
  const BRACKET_Y = 58;               // the brackets over the plot
  const BRACKET_H = 10;
  const DRAW_EASE = [0.33, 1, 0.68, 1];
  const EASE = 'cubic-bezier(.16,1,.3,1)';

  /* what each page shows, and at which click (0 = on arrival); names are data.json's */
  const VARIANTS = {
    p14: {
      strokes: [
        { segs: ['none.a'], cls: 'br-none', step: 1 },
        { segs: ['informed.ramp', 'informed.flat'], cls: 'br-up', step: 2 },
        { segs: ['informed.drop'], cls: 'br-drop', step: 3 },
        { segs: ['informed.floor'], cls: 'br-floor', step: 3 },
        { segs: ['none.b'], cls: 'br-none', step: 4 },
        { segs: ['none.dashed'], cls: 'br-mixed', step: 4 },
      ],
      markers: { rA: 2, rC: 2, rJ: 4 },
      dots: [1, 2, 3],
      brackets: [1, 2, 3],
      shade: 4,
      xlabelSteps: { 'p14.chart.x.rA': 2, 'p14.chart.x.rJ': 4 },
      ctlFrom: 4,
    },
    p16: {
      full: [
        { segs: ['none.a', 'none.b'], cls: 'br-none' },
        { segs: ['informed.ramp', 'informed.flat'], cls: 'br-up' },
        { segs: ['informed.floor'], cls: 'br-floor' },
      ],
      traceStep: 2,
      strokes: [
        { segs: ['fixed.flat'], cls: 'cmp-fixed', step: 2, line: 'fixed' },
        { segs: ['fixed.drop'], cls: 'cmp-drop', step: 2 },
        { segs: ['fixed.floor'], cls: 'cmp-fixed', step: 2, line: 'fixed' },
        { segs: ['hidden'], cls: 'cmp-hidden', step: 2, line: 'hidden' },
      ],
      markers: {},
      dots: [0, 0, 0],
      brackets: [],
      shade: null,
      xtickSteps: { 'p16.chart.x.rC': 2 },
      xlabelSteps: { 'p16.chart.x.rC': 2 },
      ctlFrom: 0,
    },
    p17: {
      strokes: [
        { segs: ['none.a', 'none.b'], cls: 'br-none', step: 0 },
        { segs: ['none.dashed'], cls: 'br-mixed', step: 0 },
        { segs: ['informed.ramp', 'informed.flat'], cls: 'br-up', step: 0 },
        { segs: ['informed.drop'], cls: 'br-drop', step: 0 },
        { segs: ['informed.floor'], cls: 'br-floor', step: 0 },
      ],
      markers: { rA: 0, rC: 0, rJ: 0 },
      dots: [0, 0, 0],
      brackets: [1, 1, 1],
      shade: 1,
      xlabelSteps: { 'p17.chart.x.rA': 1, 'p17.chart.x.rJ': 1 },
      ctlFrom: 0,
    },
  };

  function el(tag, attrs, parent) {
    const n = document.createElementNS(NS, tag);
    if (attrs) Object.keys(attrs).forEach((k) => n.setAttribute(k, attrs[k]));
    if (parent) parent.appendChild(n);
    return n;
  }

  // time at which an ease-out bezier reaches progress p (for a dot met by a growing clip)
  function bezierTimeAt(p, b) {
    const [x1, y1, x2, y2] = b;
    const cub = (t, a, c) => 3 * a * t * (1 - t) * (1 - t) + 3 * c * t * t * (1 - t) + t * t * t;
    let lo = 0;
    let hi = 1;
    for (let i = 0; i < 40; i++) {          // y(s) is monotone: find s with y(s) = p, return x(s)
      const s = (lo + hi) / 2;
      if (cub(s, y1, y2) < p) lo = s; else hi = s;
    }
    return cub((lo + hi) / 2, x1, x2);
  }

  TALK.figure('entry', {
    mount(mountEl, ctx) {
      const data = ctx.data || {};
      const v = ctx.variant || ctx.page;
      const spec = VARIANTS[v];
      if (!spec) { console.error('entry: no variant ' + v); return; }
      const curves = data.curves;
      const extra = ((data.extra || {}).charts || {}).entry_pages || {};
      const pageSpec = curves.pages[v] || extra[v];
      if (!pageSpec) { console.error('entry: no page data for ' + v); return; }
      this.bx = spec.box || BOX;
      const { F, W, H } = this.bx;
      this.el = mountEl;
      this.v = v;
      this.spec = spec;
      this.data = data;
      this.curves = curves;
      this.pageSpec = pageSpec;
      this.anims = [];
      this.step = 0;
      this.uid = 'entry-' + ctx.page;

      const [rx0, rx1] = pageSpec.x_range;
      const [ry0, ry1] = pageSpec.y_range;
      this.sx = (r) => F.x0 + (r - rx0) / (rx1 - rx0) * (F.x1 - F.x0);
      this.sy = (y) => F.y0 - (y - ry0) / (ry1 - ry0) * (F.y0 - F.y1);
      const segs = curves.segments;
      this.yRho = segs['none.a'].points[0][1];
      this.yTop = segs['informed.flat'].points[0][1];
      const br = curves.breaks;

      const svg = el('svg', { class: 'fig-svg', viewBox: `0 0 ${W} ${H}`, width: W, height: H, 'aria-hidden': 'true' });
      mountEl.insertBefore(svg, mountEl.firstChild);
      this.svg = svg;

      // the two line screens a look may point a fill at, and this mount's clip for drawing
      const defs = el('defs', {}, svg);
      this.screens = ['a', 'b'].map((letter, i) => {
        const p = el('pattern', { id: `scr-${letter}-entry`, patternUnits: 'userSpaceOnUse', patternTransform: `rotate(${i ? 135 : 45})` }, defs);
        return { p, path: el('path', { class: 'screen-line' }, p) };
      });
      const clip = el('clipPath', { id: 'clip-' + this.uid, clipPathUnits: 'userSpaceOnUse' }, defs);
      this.clipRect = el('rect', { class: 'draw-clip', x: 0, y: -60, width: W, height: H + 120 }, clip);

      // layers, bottom to top
      const L = {};
      ['shade', 'grid', 'axes', 'trace', 'full', 'lines', 'drops', 'markers', 'dots', 'ctl'].forEach((k) => {
        L[k] = el('g', { class: 'layer-' + k }, svg);
      });
      this.L = L;
      this.stepGroups = new Map();       // step -> [groups]
      const group = (layer, step) => {
        if (!step) return L[layer];
        const key = layer + ':' + step;
        this._g = this._g || {};
        if (!this._g[key]) {
          const g = el('g', { 'data-step': step, class: 'step-g' }, L[layer]);
          this._g[key] = g;
          if (!this.stepGroups.has(step)) this.stepGroups.set(step, []);
          this.stepGroups.get(step).push(g);
        }
        return this._g[key];
      };

      // the plot frame: an unpainted box that carries between pages 19, 20 and 22
      el('rect', { class: 'plot-frame', ...(spec.noCarry ? {} : { 'data-carry': 'frame' }), x: F.x0, y: F.y1, width: F.x1 - F.x0, height: F.y0 - F.y1, fill: 'none', stroke: 'none' }, L.axes);

      // axes and ticks
      el('path', { class: 'ax', d: `M${F.x0} ${F.y1}V${F.y0}H${F.x1 + 8}` }, L.axes);
      const numText = (id) => (data.numbers[id] ? data.numbers[id].text : (console.error('entry: no number ' + id), '?'));
      pageSpec.y_ticks.forEach((t) => {
        const y = this.sy(t.y);
        el('line', { class: 'ax-tick', x1: F.x0 - 8, x2: F.x0, y1: y, y2: y }, L.axes);
        let html = numText(t.num);
        if (t.prefix_tex) {
          const key = t.prefix_tex === '\\rho' ? 'entry.rho' : null;
          if (!key || !TALK.math[key]) console.error('entry: no label for ' + t.prefix_tex);
          html = (TALK.math[key] || '') + (t.prefix_join || ' ') + html;
        }
        this.label('ax-label', html, { place: 'yt', x: F.x0 - 14, y, ax: 1, ay: 0.5 });
      });
      pageSpec.x_ticks.forEach((t) => {
        const x = this.sx(t.r);
        const tickStep = (spec.xtickSteps || {})[t.num] || 0;
        el('line', { class: 'ax-tick', x1: x, x2: x, y1: F.y0, y2: F.y0 + 8 }, group('axes', tickStep));
        if (t.num) this.label('ax-label', numText(t.num), { x, y: F.y0 + 14, ax: 0.5, ay: 0, step: (spec.xlabelSteps || {})[t.num] || 0 });
      });

      // incumbents: a tick on the strength axis from arrival, a dot on its branch
      this.incs = spec.noIncumbents ? [] : curves.incumbents;
      this.incs.forEach((inc) => {
        const x = this.sx(inc.r);
        el('line', { class: 'inc-tick', 'data-inc': inc.inc, x1: x, x2: x, y1: F.y0, y2: F.y0 - 12 }, L.axes);
      });

      // guides: a dotted keyline at each strength the page's text names (b25); its symbol is the
      // page's own label (data-place="guide:<at>")
      this.guides = {};
      (pageSpec.guides || []).forEach((gd) => {
        const x = this.sx(gd.r);
        this.guides[gd.at] = x;
        el('line', { class: 'guide', x1: x, x2: x, y1: F.y1 - 4, y2: F.y0 }, L.grid);
      });

      // shade: the strengths where two equilibria coexist
      if (spec.shade != null && pageSpec.shade) {
        const g = group('shade', spec.shade);
        const xa = this.sx(pageSpec.shade.r[0]);
        const xb = this.sx(pageSpec.shade.r[1]);
        el('rect', { class: 'shade', x: xa, y: F.y1, width: xb - xa, height: F.y0 - F.y1 }, g);
        el('line', { class: 'shade-edge', x1: xa, x2: xa, y1: F.y1, y2: F.y0 }, g);
        el('line', { class: 'shade-edge', x1: xb, x2: xb, y1: F.y1, y2: F.y0 }, g);
      }

      // brackets over the plot
      this.brackets = [];
      (pageSpec.brackets || []).forEach((b, i) => {
        const step = spec.brackets[i] || 0;
        const xa = this.sx(br[b.from].r) + (b.from === 'lo' ? 0 : 4);
        const xb = this.sx(br[b.to].r) - (b.to === 'hi' ? 0 : 4);
        el('path', { class: 'bracket', d: `M${xa} ${BRACKET_Y + BRACKET_H}V${BRACKET_Y}H${xb}V${BRACKET_Y + BRACKET_H}` }, group('lines', step));
        this.brackets.push({ xa, xb });
      });

      // strokes: the full model's branches, page 20's comparison lines
      const pts = (names) => {
        const out = [];
        names.forEach((n) => {
          const s = segs[n];
          if (!s) { console.error('entry: no segment ' + n); return; }
          s.points.forEach((p) => {
            const q = [this.sx(p[0]), this.sy(p[1])];
            const last = out[out.length - 1];
            if (!last || Math.abs(last[0] - q[0]) > 1e-6 || Math.abs(last[1] - q[1]) > 1e-6) out.push(q);
          });
        });
        return out;
      };
      this.strokes = [];
      const stroke = (s, parent, cls) => {
        const p = pts(s.segs);
        const node = el('polyline', { class: 'br ' + cls, points: p.map((q) => q[0].toFixed(2) + ',' + q[1].toFixed(2)).join(' ') }, parent);
        this.strokes.push({ node, pts: p, segs: s.segs, line: s.line || null });
        return node;
      };
      if (spec.full) {
        // page 20: the full model, which becomes a pale trace when the comparison lines arrive
        this.fullG = el('g', { class: 'full-model' }, L.full);
        spec.full.forEach((s) => stroke(s, this.fullG, s.cls));
        const tg = group('trace', spec.traceStep);
        spec.full.forEach((s) => stroke(s, tg, 'br-trace'));
      }
      // a connector that runs down the page (the drop at 3.59) sits in a layer of its own, so that it
      // can be drawn downward while the rest of its click is drawn along x
      spec.strokes.forEach((s) => stroke(s, group(/drop/.test(s.cls) ? 'drops' : 'lines', s.step), s.cls));

      // endpoint markers
      (pageSpec.markers || []).forEach((m) => {
        const step = spec.markers[m.at];
        if (step == null) return;
        el('circle', {
          class: m.fill === 'open' ? 'dot dot-open' : 'dot dot-end',
          cx: this.sx(m.r), cy: this.sy(m.y), r: 5,
        }, group('markers', step));
      });

      if (pageSpec.end_dot) {
        const d = pageSpec.end_dot;
        el('circle', { class: 'dot dot-stop', cx: this.sx(d.r), cy: this.sy(d.y), r: 6 }, L.markers);
      }

      // incumbent dots
      this.dots = this.incs.map((inc, i) => el('circle', {
        class: 'dot', 'data-inc': inc.inc, ...(spec.noCarry ? {} : { 'data-carry': 'dot-' + inc.inc }),
        cx: this.sx(inc.r), cy: this.sy(inc.y), r: 8,
      }, group('dots', spec.dots[i] || 0)));

      this.place();
      this.look();
      this.buildControl();
    },

    /* an HTML label made here (numbers); words come from the page */
    label(cls, html, o) {
      const s = document.createElement('span');
      s.className = 'fig-label ' + cls;
      s.innerHTML = html;
      if (o.step) s.dataset.step = o.step;
      this.el.appendChild(s);
      this.made = this.made || [];
      this.made.push({ s, o });
      return s;
    },

    put(s, x, y, ax, ay) {
      const w = s.offsetWidth;
      const h = s.offsetHeight;
      s.style.left = (x - ax * w).toFixed(1) + 'px';
      s.style.top = (y - ay * h).toFixed(1) + 'px';
    },

    /* place every label: anchors in the plot's own coordinates */
    place() {
      if (!this.bx) return;
      const { F } = this.bx;
      const sx = this.sx;
      const sy = this.sy;
      const br = this.curves.breaks;
      const inc = (i) => this.incs[i];
      (this.made || []).forEach(({ s, o }) => this.put(s, o.x, o.y, o.ax, o.ay));
      this.el.querySelectorAll(':scope > .fig-label[data-place]').forEach((s) => {
        const [kind, arg] = s.dataset.place.split(':');
        const i = +arg;
        switch (kind) {
          case 'ytitle': this.put(s, F.x0 - 14, F.y1 + 4, 1, 0.5); break;
          case 'xtitle': this.put(s, (F.x0 + F.x1) / 2, F.y0 + (this.spec.noIncumbents ? 34 : 64), 0.5, 0.5); break;
          case 'inc': {
            // the symbol sits at the same place on pages 19, 20 and 22; a word runs to its left.
            // Until the click that draws its point (page 19), a label stands over its tick on the
            // strength axis: that is where page 17's column heads land, and it rises on that click.
            const r = inc(i);
            const x = sx(r.r) + [28, 25, 102][i];
            const yPoint = i === 1 ? sy(this.yTop) - 14 - s.offsetHeight : sy(this.yRho) + 16;
            const yTick = F.y0 - 18 - s.offsetHeight;
            s.dataset.rise = (yTick - yPoint).toFixed(1);
            const atPoint = this.step >= ((this.spec.dots || [])[i] || 0);
            s.style.left = x.toFixed(1) + 'px';
            s.style.top = (atPoint ? yPoint : yTick).toFixed(1) + 'px';
            break;
          }
          case 'bracket': {
            const b = this.brackets[i];
            if (!b) break;
            s.style.textAlign = i === 0 ? 'left' : 'center';
            if (i === 0) this.put(s, b.xa, BRACKET_Y - 6, 0, 1);
            else this.put(s, (b.xa + b.xb) / 2, BRACKET_Y - 6, 0.5, 1);
            break;
          }
          case 'shade': this.put(s, sx(br.rJ.r) + 13, (sy(this.yRho) + F.y0) / 2 + 10, 0, 0.5); break;
          case 'model': this.put(s, sx(br.rF.r) + 17, sy(this.yTop) + 20, 0, 0); break;
          case 'cmp-fixed': this.put(s, F.x0 + 167, sy(this.yTop) - 16, 0, 1); break;
          case 'cmp-hidden': this.put(s, F.x0 + 167, sy(this.yRho) + 18, 0, 0); break;
          case 'branch': {
            // page 22: each branch named beside it, right of the region with two equilibria:
            // the informed branch under its flat stretch, the other over the floor
            if (i === 0) this.put(s, sx(br.rJ.r) + 20, sy(this.yTop) + 16, 0, 0);
            else this.put(s, sx(br.rJ.r) + 20, sy(this.yRho) - 14, 0, 1);
            break;
          }
          case 'guide': {
            // the symbol of a marked strength over the plot; close strengths stand at two heights
            const x = this.guides[arg];
            if (x == null) break;
            const level = (this.spec.guideLevels || {})[arg] || 0;
            this.put(s, x, F.y1 - 8 - level * 34, 0.5, 1);
            break;
          }
          case 'line': {
            // b25: the two markets' names, set beside their lines
            if (arg === 'informative') this.put(s, sx(2.6), sy(this.yTop) - 12, 0.5, 1);
            else this.put(s, F.x0 + 10, sy(this.yRho) + 14, 0, 0);
            break;
          }
          default: console.error('entry: unknown label place ' + s.dataset.place);
        }
      });
    },

    look() {
      if (!this.el) return;
      const cs = getComputedStyle(this.el);
      const pitch = parseFloat(cs.getPropertyValue('--scr-pitch')) || 9;
      this.screens.forEach(({ p, path }) => {
        p.setAttribute('width', pitch);
        p.setAttribute('height', pitch);
        path.setAttribute('d', `M0 0V${pitch}`);
      });
      this.place();
      if (this.ctlOpen) this.renderControl(false);
    },

    /* ------------------------------------------------------------ steps and motion */

    setStep(step, opts) {
      if (!this.spec) return;
      this.stopMotion();
      this.step = step;
      this.draw = null;
      this.place();                       // the incumbents' labels stand where this step has them
      if (this.fullG) this.fullG.style.visibility = step >= this.spec.traceStep ? 'hidden' : '';
      if (this.ctlOpen) {
        if (step < this.spec.ctlFrom) this.control.close();
        else this.renderControl(false);
      }
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
      queueMicrotask(() => {
        groups.forEach((g) => g.getAnimations({ subtree: true }).forEach((a) => {
          // finish (not cancel): the look then clears its clip itself and its text wipes run on
          if (!this.anims.includes(a)) { try { a.finish(); } catch (err) { /* gone */ } }
        }));
        this.timeLabels(step);
      });
    },

    /* The look wipes this click's HTML labels at once, so a number such as 1.39 would read "1.3"
       for a moment, and a label would be set before its line reaches it. Each label is set when
       the drawing clip reaches its left edge: a number appears whole, words keep the look's wipe. */
    timeLabels(step) {
      const d = this.draw;
      if (!d) return;
      this.el.querySelectorAll(':scope > .fig-label[data-step="' + step + '"]').forEach((s) => {
        const left = parseFloat(s.style.left) || 0;
        const p = Math.max(0, Math.min(1, (left - d.x0) / d.span));
        const at = d.lead + Math.round(d.dur * bezierTimeAt(p, DRAW_EASE));
        const whole = s.classList.contains('ax-label');
        s.getAnimations().forEach((a) => {
          const kf = a.effect && a.effect.getKeyframes ? a.effect.getKeyframes() : [];
          if (!kf.some((f) => 'clipPath' in f)) return;
          try { a.effect.updateTiming(whole ? { delay: at, duration: 1 } : { delay: at }); } catch (err) { /* gone */ }
        });
      });
    },

    play(step) {
      const all = this.stepGroups.get(step) || [];
      const groups = all.filter((g) => !g.closest('.layer-dots') && !g.closest('.layer-trace') && !g.closest('.layer-drops'));
      const dots = all.filter((g) => g.closest('.layer-dots'));
      const drops = [];
      all.filter((g) => g.closest('.layer-drops')).forEach((g) => g.querySelectorAll('.br').forEach((n) => drops.push(n)));
      // the drawing: a clip that grows along x over everything this click brings
      let xa = Infinity;
      let xb = -Infinity;
      groups.forEach((g) => {
        let b;
        try { b = g.getBBox(); } catch (err) { b = null; }
        if (b && (b.width || b.height)) { xa = Math.min(xa, b.x); xb = Math.max(xb, b.x + b.width); }
      });
      dots.forEach((g) => g.querySelectorAll('circle').forEach((c) => { const x = +c.getAttribute('cx'); xa = Math.min(xa, x); xb = Math.max(xb, x); }));
      const easing = `cubic-bezier(${DRAW_EASE.join(',')})`;
      const DROP = 200;
      const dropX = drops.map((n) => n.getBBox().x);
      // a click that begins with a drop (page 19, click 3) draws the drop first, downward, and then
      // the line that leaves its foot; a drop met later (page 20) is drawn when the line reaches it
      const pad = 14;
      const x0 = xa - pad;
      const span = xb - xa + 2 * pad;
      const leads = dropX.length > 0 && dropX.every((x) => x <= xa + pad);
      const lead = leads ? DROP : 0;
      const dur = Math.round(Math.min(450, 300 + span / 3));
      this.draw = xb > xa ? { x0, span, dur, lead } : null;
      if (xb > xa) {
        this.clipRect.setAttribute('x', x0.toFixed(1));
        this.clipRect.setAttribute('width', span.toFixed(1));
        groups.forEach((g) => g.setAttribute('clip-path', `url(#clip-${this.uid})`));
        const a = this.clipRect.animate([{ transform: 'scaleX(0)' }, { transform: 'scaleX(1)' }],
          { duration: dur, delay: lead, easing, fill: 'backwards' });
        this.anims.push(a);
        a.finished.then(() => this.unclip(groups), () => {});
      }
      // the drop: its own clip, a rectangle that grows downward from the top of the drop
      drops.forEach((n, i) => {
        const b = n.getBBox();
        const w = parseFloat(getComputedStyle(n).strokeWidth) || 4;
        const id = `clip-${this.uid}-drop-${i}`;
        let cp = this.svg.querySelector('#' + id);
        if (!cp) {
          cp = el('clipPath', { id, clipPathUnits: 'userSpaceOnUse' }, this.svg.querySelector('defs'));
          el('rect', { class: 'draw-clip draw-clip-y' }, cp);
        }
        const r = cp.firstChild;
        r.setAttribute('x', (b.x - w - 6).toFixed(1));
        r.setAttribute('width', (b.width + 2 * w + 12).toFixed(1));
        r.setAttribute('y', (b.y - w).toFixed(1));
        r.setAttribute('height', (b.height + 2 * w).toFixed(1));
        n.setAttribute('clip-path', `url(#${id})`);
        const p = xb > xa ? Math.max(0, Math.min(1, (b.x - x0) / span)) : 0;
        const delay = leads ? 0 : Math.round(dur * bezierTimeAt(p, DRAW_EASE));
        const a = r.animate([{ transform: 'scaleY(0)' }, { transform: 'scaleY(1)' }],
          { duration: DROP, delay, easing: 'cubic-bezier(.33,0,.67,1)', fill: 'backwards' });
        this.anims.push(a);
        a.finished.then(() => n.removeAttribute('clip-path'), () => {});
      });
      // each dot arrives when the line reaches it
      if (!(xb > xa)) return;
      dots.forEach((g) => g.querySelectorAll('circle').forEach((c) => {
        const p = Math.max(0, Math.min(1, (+c.getAttribute('cx') - x0) / span));
        const delay = lead + Math.round(dur * bezierTimeAt(p, DRAW_EASE));
        this.anims.push(c.animate([{ opacity: 0, transform: 'scale(.4)' }, { opacity: 1, transform: 'scale(1)' }],
          { duration: 160, delay, easing: EASE, fill: 'backwards' }));
        // the incumbent's label rises from its tick to its point as the point arrives
        const lab = c.dataset.inc != null && this.el.querySelector(`:scope > .inc-label[data-inc="${c.dataset.inc}"]`);
        const rise = lab ? parseFloat(lab.dataset.rise) || 0 : 0;
        if (rise) {
          this.anims.push(lab.animate([{ transform: `translateY(${rise}px)` }, { transform: 'none' }],
            { duration: 320, delay, easing: EASE, fill: 'backwards' }));
        }
      }));
      // page 20: the full model fades to its trace as the comparison lines are drawn
      if (this.fullG && step === this.spec.traceStep) {
        this.anims.push(this.fullG.animate([{ opacity: 1, visibility: 'visible' }, { opacity: 0, visibility: 'visible' }],
          { duration: 320, easing: EASE }));
      }
    },

    unclip(groups) {
      groups.forEach((g) => g.removeAttribute('clip-path'));
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

    /* ------------------------------------------------------------ the strength control */

    buildControl() {
      const self = this;
      this.ctlIndex = 0;
      this.ctlOpen = false;
      this.control = {
        open() {
          if (self.step < self.spec.ctlFrom) return false;
          self.ctlOpen = true;
          self.renderControl(false);
          return true;
        },
        close() {
          self.ctlOpen = false;
          self.clearControl();
        },
        move(dir) {
          // a press during the marker's move finishes that move; the next press goes on
          if ((self.ctlAnims || []).some((a) => a.playState === 'running')) {
            self.ctlAnims.forEach((a) => { try { a.finish(); } catch (err) { /* gone */ } });
            return;
          }
          const n = self.data.marks.length;
          const k = Math.max(0, Math.min(n - 1, self.ctlIndex + (dir > 0 ? 1 : -1)));
          if (k === self.ctlIndex) return;
          self.ctlIndex = k;
          self.renderControl(true);
        },
      };
    },

    clearControl() {
      if (this.ctlAnims) this.ctlAnims.forEach((a) => { try { a.cancel(); } catch (err) { /* gone */ } });
      this.ctlAnims = [];
      while (this.L.ctl.firstChild) this.L.ctl.removeChild(this.L.ctl.firstChild);
      this.el.querySelectorAll(':scope > .ctl-readout').forEach((n) => n.remove());
      this.svg.classList.remove('has-ctl');
    },

    // the equilibria shown at stop m: the full model's (data.marks), and on page 20 the
    // comparison lines once they are on the page
    ctlPoints(m) {
      const out = [];
      m.equilibria.forEach((e) => out.push({ y: e.y, line: 'model', num: e.entry_num }));
      if (this.v === 'p16' && this.step >= this.spec.traceStep) {
        ['fixed', 'hidden'].forEach((line) => {
          const y = this.lineAt(line, m.r);
          if (y == null) return;
          const tick = this.pageSpec.y_ticks.find((t) => Math.abs(t.y - y) < 1e-6 && t.num && this.data.numbers[t.num] && this.data.numbers[t.num].key);
          out.push({ y, line, num: tick ? tick.num : null });
        });
      }
      const kept = [];
      out.forEach((p) => {
        const q = kept.find((c) => Math.abs(this.sy(c.y) - this.sy(p.y)) < 1);
        if (q) { q.lines.push(p.line); if (!q.num) q.num = p.num; } else kept.push(Object.assign({ lines: [p.line] }, p));
      });
      return kept;
    },

    // the y of a comparison line at strength r, read from its segments (end rules of data.json)
    lineAt(line, r) {
      const names = line === 'fixed' ? ['fixed.flat', 'fixed.floor'] : ['hidden'];
      for (const n of names) {
        const s = this.curves.segments[n];
        const p = s.points;
        const a = p[0][0];
        const b = p[p.length - 1][0];
        const inA = r > a + 1e-9 || (Math.abs(r - a) <= 1e-9 && !(s.start && s.start.included === false));
        const inB = r < b - 1e-9 || (Math.abs(r - b) <= 1e-9 && !(s.end && s.end.included === false));
        if (inA && inB) {
          for (let k = 1; k < p.length; k++) {
            if (r <= p[k][0] + 1e-9) {
              const t = (r - p[k - 1][0]) / ((p[k][0] - p[k - 1][0]) || 1);
              return p[k - 1][1] + t * (p[k][1] - p[k - 1][1]);
            }
          }
        }
      }
      return null;
    },

    renderControl(moving) {
      const { F, W } = this.bx;
      const prevX = this.ctlX;
      this.clearControl();
      const m = this.data.marks[this.ctlIndex];
      if (!m) return;
      const g = this.L.ctl;
      const nums = this.data.numbers;
      this.svg.classList.add('has-ctl');
      this.data.marks.forEach((s) => {
        const x = this.sx(s.r);
        el('line', { class: 'ctl-stop', x1: x, x2: x, y1: F.y1 - 12, y2: F.y1 }, g);
      });
      const x = this.sx(m.r);
      this.ctlX = x;
      const mk = el('path', { class: 'ctl-marker' }, g);
      const pts = this.ctlPoints(m);
      const dots = pts.map((p) => el('circle', { class: 'ctl-dot', 'data-line': p.line, cx: x, cy: this.sy(p.y), r: 12 }, g));
      // readouts: the strength at the marker's foot, entry at each dot
      const made = [];
      const foot = document.createElement('span');
      foot.className = 'fig-label ctl-readout';
      foot.dataset.role = 'r';
      foot.innerHTML = (TALK.math['entry.r'] || '') + ' = ' + (nums[m.num] ? nums[m.num].text : '?');
      this.el.appendChild(foot);
      const obstacles = this.obstacles(x);
      const fixedThings = obstacles.slice(0, -1);       // everything but the marker itself
      const fw = foot.offsetWidth;
      const fh = foot.offsetHeight;
      let placed = false;
      // nearest first: under the marker's foot, then beside it, then further up and further out
      const footPlaces = [];
      [0, 60, 110, 160].forEach((d) => [18, 58, 98, 138, 178].forEach((up) => {
        if (d === 0) footPlaces.push([up, x, 0.5], [up, x + 10, 0], [up, x - 10, 1]);
        else footPlaces.push([up, x + 10 + d, 0], [up, x - 10 - d, 1]);
      }));
      for (const [up, fx, ax] of footPlaces) {
        const b = { x: fx - ax * fw, y: F.y0 - up - fh, w: fw, h: fh };
        if (b.x < F.x0 + 4 || b.x + b.w > W) continue;
        if (this.hits(b, fixedThings)) continue;
        this.put(foot, fx, F.y0 - up, ax, 1);
        placed = true;
        break;
      }
      if (!placed) this.put(foot, x, F.y0 - 18, 0.5, 1);
      made.push(foot);
      obstacles.push(this.box(foot));
      // on page 20 a dot may belong to the full model or to a comparison line: say which, in the
      // page's own words
      const who = (line) => {
        const n = line === 'model' ? this.el.querySelector(':scope > .model-label')
          : this.el.querySelector(`:scope > .cmp-label[data-cmp="${line}"]`);
        return n ? n.textContent.trim() : '';
      };
      // the highest dot first: the top of the plot is the most crowded
      pts.slice().sort((a, b) => b.y - a.y).forEach((p) => {
        if (!p.num || !nums[p.num]) return;          // no registry number behind this value
        const s = document.createElement('span');
        s.className = 'fig-label ctl-readout';
        s.dataset.role = 'entry';
        s.dataset.line = p.line;
        s.textContent = nums[p.num].text;
        if (this.v === 'p16') {
          (p.lines || [p.line]).map(who).filter(Boolean).forEach((name) => {
            const w = document.createElement('span');
            w.className = 'ctl-who';
            w.textContent = name;
            s.appendChild(w);
          });
        }
        this.el.appendChild(s);
        // the control's other dots are obstacles too, so a value never sits beside a dot not its own
        const others = pts.filter((q) => q !== p).map((q) => ({ x: x - 16, y: this.sy(q.y) - 16, w: 32, h: 32 }));
        this.placeReadout(s, x, this.sy(p.y), obstacles.concat(others));
        obstacles.push(this.box(s));
        made.push(s);
      });
      // the marker runs from the top of the plot to the axis, broken where it would cross a label
      const gaps = [];
      this.el.querySelectorAll(':scope > .fig-label').forEach((s) => {
        if (getComputedStyle(s).visibility !== 'visible') return;
        const b = this.box(s);
        if (b.x <= x + 4 && b.x + b.w >= x - 4) gaps.push([b.y - 5, b.y + b.h + 5]);
      });
      gaps.sort((a, b) => a[0] - b[0]);
      let d = '';
      let y = F.y1;
      gaps.forEach(([a, b]) => {
        if (b <= y) return;
        if (a > y) d += `M${x} ${y}V${Math.min(a, F.y0)}`;
        y = Math.max(y, b);
      });
      if (y < F.y0) d += `M${x} ${y}V${F.y0}`;
      mk.setAttribute('d', d || `M${x} ${F.y0}V${F.y0}`);
      if (moving && !TALK.reduced() && prevX != null && Math.abs(prevX - x) > 0.5) {
        const dx = prevX - x;
        this.ctlAnims.push(mk.animate([{ transform: `translateX(${dx}px)` }, { transform: 'none' }], { duration: 180, easing: EASE }));
        dots.concat(made).forEach((n) => this.ctlAnims.push(n.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 120, delay: 90, easing: EASE, fill: 'backwards' })));
      }
    },

    // a label's box in the mount, measured from what is drawn: the label's own box together
    // with an incumbent's word, which sits outside it
    box(s) {
      const host = this.el.getBoundingClientRect();
      const k = (host.width / this.el.offsetWidth) || 1;
      const r = s.getBoundingClientRect();
      let x0 = r.left, y0 = r.top, x1 = r.right, y1 = r.bottom;
      s.querySelectorAll('.inc-word').forEach((w) => {
        const q = w.getBoundingClientRect();
        x0 = Math.min(x0, q.left); y0 = Math.min(y0, q.top);
        x1 = Math.max(x1, q.right); y1 = Math.max(y1, q.bottom);
      });
      return { x: (x0 - host.left) / k, y: (y0 - host.top) / k, w: (x1 - x0) / k, h: (y1 - y0) / k };
    },

    // what a readout must not touch: the page's visible labels, the visible strokes and dots,
    // the marker itself
    obstacles(mx) {
      const { F } = this.bx;
      const out = [];
      this.el.querySelectorAll(':scope > .fig-label:not(.ctl-readout)').forEach((s) => {
        if (getComputedStyle(s).visibility !== 'visible') return;
        out.push(this.box(s));
      });
      this.strokes.forEach((st) => {
        if (getComputedStyle(st.node).visibility !== 'visible') return;
        const half = (parseFloat(getComputedStyle(st.node).strokeWidth) || 4) / 2 + 3;
        out.push({ poly: st.pts, half });
      });
      this.svg.querySelectorAll('.dot').forEach((c) => {
        if (getComputedStyle(c).visibility !== 'visible') return;
        const cx = +c.getAttribute('cx');
        const cy = +c.getAttribute('cy');
        out.push({ x: cx - 12, y: cy - 12, w: 24, h: 24 });
      });
      out.push({ x: mx - 4, y: F.y1, w: 8, h: F.y0 - F.y1 });
      return out;
    },

    hits(b, obs) {
      const pad = 3;
      return obs.some((o) => {
        if (o.poly) {
          for (let k = 1; k < o.poly.length; k++) {
            const [ax, ay] = o.poly[k - 1];
            const [bx, by] = o.poly[k];
            const n = Math.max(1, Math.ceil(Math.hypot(bx - ax, by - ay) / 3));
            for (let j = 0; j <= n; j++) {
              const px = ax + (bx - ax) * j / n;
              const py = ay + (by - ay) * j / n;
              if (px > b.x - o.half && px < b.x + b.w + o.half && py > b.y - o.half && py < b.y + b.h + o.half) return true;
            }
          }
          return false;
        }
        return b.x < o.x + o.w + pad && b.x + b.w + pad > o.x && b.y < o.y + o.h + pad && b.y + b.h + pad > o.y;
      });
    },

    placeReadout(s, x, y, obs) {
      const { F, W } = this.bx;
      const w = s.offsetWidth;
      const h = s.offsetHeight;
      const g = 12;
      // places around the dot, nearest first: above, below, beside, then further out
      const cands = [];
      [0, 30, 60, 90, 120, 160, 200, 240].forEach((dx) => {
        [0, 30, 60, 90].forEach((dy) => {
          cands.push([x + g + dx, y - g - h - dy], [x + g + dx, y + g + dy], [x - g - w - dx, y - g - h - dy], [x - g - w - dx, y + g + dy]);
        });
        cands.push([x + g + 4 + dx, y - h / 2], [x - g - 4 - w - dx, y - h / 2]);
      });
      const dist = (c) => Math.hypot(c[0] + w / 2 - x, c[1] + h / 2 - y);
      cands.sort((a, b) => dist(a) - dist(b));
      // inside the plot: right of the entry axis, above the strength axis
      const inside = (b) => b.x >= F.x0 + 6 && b.x + b.w <= W && b.y >= F.y1 - 30 && b.y + b.h <= F.y0 - 2;
      let best = cands[0];
      for (const [cx, cy] of cands) {
        const b = { x: cx, y: cy, w, h };
        if (inside(b) && !this.hits(b, obs)) { best = [cx, cy]; break; }
      }
      s.style.left = best[0].toFixed(1) + 'px';
      s.style.top = best[1].toFixed(1) + 'px';
    },
  });
})();
