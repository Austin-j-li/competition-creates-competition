/* Page 7: payoffs in the auction, for a prepared rival with value theta, as the incumbent's
   value R rises. Shapes and proportions from the boxes of master_dump/slide08.txt: p sits at 0.377 theta on both
   axes and the R axis runs to 2.045 theta. Below R = p the rival wins and pays p; between p and
   theta it pays R; above theta the incumbent wins and pays theta. The solid area is what
   shareholders are paid, max{p, min(R, theta)}; the screened area above it is what the rival
   keeps, theta - max{p, R}. Axes are on from arrival; click 1 wipes the two areas in from left to
   right as R rises, and the brackets and labels arrive as the edge passes them.
   In the reading view only, a pointer over the plot shows a thin vertical line at that R with
   the two heights outlined. */
(function () {
  'use strict';
  const NS = 'http://www.w3.org/2000/svg';
  const W = 780, H = 500;
  const X0 = 64;                 // the value axis
  const PW = 700;                // plot width
  const U = PW / 2.045;          // theta, in px, on both axes
  const P = 0.3773 * U;          // the reserve p
  const YB = 418;                // the R axis
  const XP = X0 + P, XT = X0 + U, XR = X0 + PW;
  const YT = YB - U, YP = YB - P;
  const YBR = YT - 30;           // the brackets
  const WIPE = 450;
  const EASE_WIPE = 'cubic-bezier(.33,1,.68,1)';

  function svg(tag, attrs, parent) {
    const el = document.createElementNS(NS, tag);
    Object.entries(attrs || {}).forEach(([k, v]) => el.setAttribute(k, v));
    if (parent) parent.append(el);
    return el;
  }

  // the shareholders' height at R (px from the axis), and the rival's on top of it
  function heights(x) {
    const r = x - X0;
    const share = Math.max(P, Math.min(r, U));
    const rival = Math.max(U - Math.max(P, r), 0);
    return { share, rival };
  }

  TALK.figure('payoff', {
    mount(el, ctx) {
      this.el = el;
      this.ctx = ctx;
      this.anims = [];
      el.style.width = W + 'px';
      el.style.height = H + 'px';

      // layer 1: the areas, the line at R = theta, the brackets and the area labels; wiped as one
      const wipe = this.wipe = document.createElement('div');
      wipe.className = 'payoff-wipe';
      el.append(wipe);
      const a = svg('svg', { class: 'fig-svg', viewBox: `0 0 ${W} ${H}`, width: W, height: H, 'aria-hidden': 'true' }, wipe);
      const defs = svg('defs', {}, a);
      this.screens = ['a', 'b'].map((letter, i) => {
        const pat = svg('pattern', { id: `scr-${letter}-payoff`, patternUnits: 'userSpaceOnUse', patternTransform: `rotate(${i ? 135 : 45})` }, defs);
        const path = svg('path', { class: 'screen-line' }, pat);
        return { p: pat, path };
      });
      const kink = `L${XP} ${YP}L${XT} ${YT}`;
      svg('path', { class: 'area-rival', d: `M${X0} ${YT}V${YP}${kink}Z` }, a);
      svg('path', { class: 'area-share', d: `M${X0} ${YB}V${YP}${kink}H${XR}V${YB}Z` }, a);
      svg('path', { class: 'payoff-edge', d: `M${X0} ${YP}${kink}H${XR}` }, a);
      svg('path', { class: 'payoff-edge payoff-top', d: `M${X0} ${YT}H${XT}` }, a);
      svg('path', { class: 'payoff-theta', d: `M${XT} ${YT}V${YB}` }, a);
      svg('path', { class: 'bracket', d: `M${X0 + 2} ${YBR + 10}V${YBR}H${XT - 5}V${YBR + 10}` }, a);
      svg('path', { class: 'bracket', d: `M${XT + 5} ${YBR + 10}V${YBR}H${XR}V${YBR + 10}` }, a);
      this.label(wipe, 'bracket-label', (X0 + XT) / 2, 0, 'rival wins', null, 'center');
      this.label(wipe, 'bracket-label', (XT + XR) / 2, 0, 'incumbent wins', null, 'center');
      // each area's label is one block: its words, then its height
      this.label(wipe, 'area-label area-label-rival', X0 + 16, YT + 12, 'to the rival', 'rivalH', 'block');
      this.label(wipe, 'area-label area-label-share', XT + 40, YT + 0.40 * U, 'to shareholders', 'shareH', 'block');

      // layer 2: axes, ticks and their labels, on from arrival
      const b = this.axes = svg('svg', { class: 'fig-svg payoff-axes', viewBox: `0 0 ${W} ${H}`, width: W, height: H, 'aria-hidden': 'true' }, el);
      svg('path', { class: 'ax', d: `M${X0} ${YT - 18}V${YB}H${XR + 8}` }, b);
      [XP, XT].forEach(x => svg('path', { class: 'ax-tick', d: `M${x} ${YB}v9` }, b));
      [YP, YT].forEach(y => svg('path', { class: 'ax-tick', d: `M${X0} ${y}h-9` }, b));
      const ticks = document.createElement('div');
      ticks.className = 'payoff-ticks';
      el.append(ticks);
      this.label(ticks, 'ax-label', XP, YB + 12, null, 'p', 'center');
      this.label(ticks, 'ax-label', XT, YB + 12, null, 'theta', 'center');
      this.label(ticks, 'ax-label', X0 - 16, YP, null, 'p', 'right-mid');
      this.label(ticks, 'ax-label', X0 - 16, YT, null, 'theta', 'right-mid');
      this.label(ticks, 'ax-title', X0 + PW / 2, YB + 46, 'incumbent’s value ', 'R', 'center');

      // the reading view's probe: a thin line at R and the two heights outlined
      const g = this.probe = svg('g', { class: 'payoff-probe' }, b);
      this.probeLine = svg('path', { class: 'probe-line' }, g);
      this.probeShare = svg('rect', { class: 'probe-box probe-share', width: 18 }, g);
      this.probeRival = svg('rect', { class: 'probe-box probe-rival', width: 18 }, g);
      el.addEventListener('pointermove', e => this.point(e));
      el.addEventListener('pointerleave', () => this.unpoint());
      this.look();
    },

    label(parent, cls, x, y, word, key, align) {
      const span = document.createElement('span');
      span.className = 'fig-label ' + cls;
      span.style.left = x + 'px';
      span.style.top = y + 'px';
      if (align === 'center') span.style.transform = 'translateX(-50%)';
      else if (align === 'right-mid') span.style.transform = 'translate(-100%, -50%)';
      if (align === 'block') {
        const head = document.createElement('span');
        head.className = 'area-head';
        head.textContent = word;
        const math = document.createElement('span');
        math.className = 'area-math';
        math.innerHTML = this.ctx.math['setupfigs.' + key];
        span.append(head, math);
        parent.append(span);
        return span;
      }
      if (word) span.append(document.createTextNode(word));
      if (key) span.insertAdjacentHTML('beforeend', this.ctx.math['setupfigs.' + key]);
      parent.append(span);
      return span;
    },

    look() {
      const pitch = parseFloat(getComputedStyle(this.el).getPropertyValue('--scr-pitch')) || 9;
      this.screens.forEach(({ p, path }) => {
        p.setAttribute('width', pitch); p.setAttribute('height', pitch);
        path.setAttribute('d', `M0 0V${pitch}`);
      });
    },

    point(e) {
      if (!document.body.classList.contains('is-reading') || !this.wipe.classList.contains('is-on')) return;
      const m = this.axes.getScreenCTM();
      if (!m) return;
      const pt = new DOMPoint(e.clientX, e.clientY).matrixTransform(m.inverse());
      if (pt.x < X0 + 2 || pt.x > XR || pt.y < YT - 40 || pt.y > YB) { this.unpoint(); return; }
      const { share, rival } = heights(pt.x);
      this.probeLine.setAttribute('d', `M${pt.x} ${YT - 18}V${YB}`);
      this.probeShare.setAttribute('x', pt.x - 9);
      this.probeShare.setAttribute('y', YB - share);
      this.probeShare.setAttribute('height', share);
      this.probeRival.setAttribute('x', pt.x - 9);
      this.probeRival.setAttribute('y', YB - share - rival);
      this.probeRival.setAttribute('height', rival);
      this.probeRival.style.display = rival > 0.5 ? '' : 'none';
      this.probe.classList.add('is-on');
    },

    unpoint() { this.probe.classList.remove('is-on'); },

    setStep(step, opts) {
      this.finish();
      this.unpoint();
      const on = step >= 1;
      this.wipe.classList.toggle('is-on', on);
      if (!on || !opts.animate || opts.dir !== 1 || opts.from.page !== opts.page || opts.from.step !== 0) return;
      // ink laid down as R rises: one hard edge sweeps the areas, brackets and labels together
      const a = this.wipe.animate([
        { clipPath: `inset(-20px ${W - X0}px -20px 0)` },
        { clipPath: 'inset(-20px -20px -20px 0)' },
      ], { duration: WIPE, easing: EASE_WIPE, fill: 'both' });
      this.anims.push(a);
      this.moving = true;
      this.release = TALK.motion({ finish: () => this.finish() });
      const batch = this.anims;
      a.finished.then(() => { if (this.anims === batch) this.finish(); }, () => {});
    },

    finish() {
      const a = this.anims || [];
      this.anims = [];
      this.moving = false;
      if (this.release) { this.release(); this.release = null; }
      a.forEach(x => x.cancel());
    },
    isMoving() { return !!this.moving; },
  });
})();
