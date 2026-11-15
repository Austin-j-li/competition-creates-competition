/* Slide13: both endpoints are proportional to shareholder spread, about the gain-axis origin. */
(function () {
  'use strict';
  const NS = 'http://www.w3.org/2000/svg';
  const EASE = 'cubic-bezier(.16,1,.3,1)';
  const O = (223 - 48) * 5 / 3;
  const LO = 82 * 5 / 3, HI = 164 * 5 / 3, SCALE = 2.8;
  const Y = [95, 175];
  function svg(tag, attrs, parent) {
    const el = document.createElementNS(NS, tag);
    Object.entries(attrs).forEach(([k, v]) => el.setAttribute(k, v)); parent.append(el); return el;
  }
  TALK.figure('gain', {
    mount(el, ctx) {
      this.el = el; this.ctx = ctx; this.anims = [];
      // The shared look wipes ordinary reveals. These two schematics own their geometry's
      // motion, so finish only the look's additional wipe on our figure groups.
      document.addEventListener('talk:state', event => {
        if (event.detail.page !== ctx.page) return;
        el.getAnimations({ subtree: true }).forEach(animation => {
          if (!this.anims.includes(animation) && animation.effect.getKeyframes().some(frame => 'clipPath' in frame)) animation.finish();
        });
      });
      const root = svg('svg', { viewBox: '0 0 1440 275', 'aria-hidden': 'true' }, el);
      const axis = svg('g', { 'data-step': 3 }, root);
      svg('path', { class: 'blocks-line', d: `M${O} 218H1083M${O} 218v9` }, axis);
      svg('path', { class: 'blocks-line cost-line', d: 'M619.17 35V218' }, axis);
      const axisLabels = document.createElement('div'); axisLabels.dataset.step = 3; el.append(axisLabels);
      this.label(axisLabels, 'center word-strong', 619.17, 0, 'order cost ', 'cost');
      this.label(axisLabels, 'center', O, 237, '', 'zero');
      const title = this.label(axisLabels, 'center', 687, 237, 'gain ', 'gain');
      title.append(document.createTextNode(' before order cost'));
      this.rows = [this.row(root, 0, 1, 3), this.row(root, 1, SCALE, 4)];
    },
    label(parent, cls, x, y, word, key) {
      const span = document.createElement('span'); span.className = 'fig-label ' + cls;
      span.style.left = x + 'px'; span.style.top = y + 'px';
      if (key) span.innerHTML = word + this.ctx.math['blocks.' + key]; else span.textContent = word;
      parent.append(span); return span;
    },
    row(root, i, scale, step) {
      const outer = svg('g', { 'data-step': step, transform: `translate(${O} ${Y[i]})` }, root);
      const line = svg('path', { class: 'blocks-line ' + (i ? 'gain-large-line' : ''), 'vector-effect': 'non-scaling-stroke', d: `M${LO * scale} 0H${HI * scale}M${LO * scale} -13v26M${HI * scale} -13v26` }, outer);
      const labels = document.createElement('div'); labels.dataset.step = step; this.el.append(labels);
      const lower = this.label(labels, i ? '' : 'center', O + LO * scale - 2, Y[i] - 45, '', 'minimum');
      const upper = this.label(labels, 'center', O + HI * scale + 2, Y[i] - 45, '', 'maximum');
      const words = [
        this.label(labels, 'word-strong', 0, Y[i] - 15, i ? 'large shareholder spread' : 'small shareholder spread'),
        this.label(labels, '', 1083, Y[i] - 15, i ? 'buys in class H, sells in class L' : 'informed trader sends no order'),
      ];
      return { line, lower, upper, words };
    },
    animate(el, frames, timing) {
      const a = el.animate(frames, { easing: EASE, fill: 'both', ...timing }); this.anims.push(a); return a;
    },
    setStep(step, opts) {
      this.finish();
      if (!opts.animate || opts.dir !== 1 || opts.from.page !== opts.page) return;
      if (step === 3) {
        this.animate(this.rows[0].line, [{ clipPath: 'inset(-20px 100% -20px 0)' }, { clipPath: 'inset(-20px 0 -20px 0)' }], { duration: 350 });
      } else if (step === 4 && opts.from.step === 3) {
        const r = this.rows[1], dy = Y[0] - Y[1];
        // Copy the small interval, drop it intact, then scale both endpoints about gain zero.
        this.animate(r.line, [
          { offset: 0, transform: `translateY(${dy}px) scaleX(${1 / SCALE})`, strokeWidth: '3px' },
          { offset: 200 / 550, transform: `translateY(0px) scaleX(${1 / SCALE})`, strokeWidth: '3px' },
          { offset: 1, transform: 'translateY(0px) scaleX(1)', strokeWidth: '8px' },
        ], { duration: 550, easing: 'linear' });
        [r.lower, r.upper].forEach((label, i) => {
          const bound = i ? HI : LO, adjust = i ? 2 : -2;
          this.animate(label, [
            { offset: 0, left: (O + bound + adjust) + 'px', top: (Y[0] - 45) + 'px', translate: '-50% 0' },
            { offset: 200 / 550, left: (O + bound + adjust) + 'px', top: (Y[1] - 45) + 'px', translate: '-50% 0' },
            { offset: 1, left: (O + bound * SCALE + adjust) + 'px', top: (Y[1] - 45) + 'px', translate: i ? '-50% 0' : '0% 0' },
          ], { duration: 550, easing: 'linear' });
        });
        r.words.forEach(label => this.animate(label, [{ opacity: 0 }, { opacity: 1 }], { delay: 310, duration: 240 }));
      }
      if (!this.anims.length) return;
      this.release = TALK.motion({ finish: () => this.finish() });
      const batch = this.anims;
      Promise.all(batch.map(a => a.finished)).then(() => { if (batch === this.anims) this.finish(); }, () => {});
    },
    finish() {
      const batch = this.anims || []; this.anims = [];
      if (this.release) { this.release(); this.release = null; }
      batch.forEach(a => a.cancel());
    },
    isMoving() { return !!this.anims.length; },
  });
})();
