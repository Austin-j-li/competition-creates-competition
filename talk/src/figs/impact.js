/* Small figures of the predictions backups (B13), drawn in code from the shape boxes of the master
   (960 x 540 pt pages; 1 pt = 5/3 px on the stage).
   variant "b50": the price line with the three prices, the two impacts as spans above it, and the
                  entry part of the purchase impact (slide52.txt, shapes 5 to 17);
   variant "b51": the three price levels P(1), P(0), P(-1) with a brace for each impact
                  (slide53.txt, shapes 7 to 14).
   Marks carry their meaning by position and by weight; the one orange mark is the entry part,
   where the price brings the costly rival in. Nothing moves. */
(function () {
  'use strict';
  const NS = 'http://www.w3.org/2000/svg';
  const K = 5 / 3;

  function svg(tag, attrs, parent) {
    const el = document.createElementNS(NS, tag);
    Object.entries(attrs || {}).forEach(([k, v]) => el.setAttribute(k, v));
    if (parent) parent.append(el);
    return el;
  }

  function label(parent, cls, x, y, html, anchor) {
    const span = document.createElement('span');
    span.className = 'fig-label ' + cls;
    span.style.left = x + 'px';
    span.style.top = y + 'px';
    span.dataset.anchor = anchor || 'center';
    span.innerHTML = html;
    parent.append(span);
    return span;
  }

  // a left brace "{" from y0 to y1, its tip pointing left, drawn in the box x .. x + w
  function brace(x, y0, y1, w) {
    const mid = (y0 + y1) / 2, h = w / 2;
    return `M${x + w} ${y0}Q${x + h} ${y0} ${x + h} ${y0 + h}L${x + h} ${mid - h}Q${x + h} ${mid} ${x} ${mid}` +
      `Q${x + h} ${mid} ${x + h} ${mid + h}L${x + h} ${y1 - h}Q${x + h} ${y1} ${x + w} ${y1}`;
  }

  function priceLine(el, M) {
    // slide52.txt: x px = (x pt - 48) 5/3, y px = (y pt - 83) 5/3
    const X = (x) => (x - 48) * K, Y = (y) => (y - 83) * K;
    const root = svg('svg', { class: 'fig-svg', viewBox: '0 0 1440 150', 'aria-hidden': 'true' }, el);
    const y = Y(123.3);
    svg('path', { class: 'imp-line', d: `M${X(216)} ${y}H${X(912)}` }, root);
    svg('path', { class: 'imp-entry', d: `M${X(638.7)} ${y}H${X(844.9)}` }, root);
    [['sale-order price', 267.6, 'sale'], ['no-order price', 453.1, 'none'], ['purchase price', 844.9, 'buy']].forEach(([word, x, id]) => {
      svg('path', { class: 'imp-tick', d: `M${X(x)} ${Y(116.1)}V${Y(130.5)}` }, root);
      label(el, 'imp-label', X(x), Y(134.1), word);
    });
    label(el, 'imp-label imp-entry-label', X(668.2 + 42.75), Y(134.1), 'entry part');
    const span = (cls, x0, x1) => {
      const yy = Y(106);
      svg('path', { class: 'imp-span ' + cls, d: `M${X(x0)} ${yy}H${X(x1)}` }, root);
      svg('path', { class: 'imp-span imp-cap ' + cls, d: `M${X(x0)} ${yy - 9}V${yy + 9}M${X(x1)} ${yy - 9}V${yy + 9}` }, root);
    };
    span('imp-sale', 270.1, 450.5);
    span('imp-buy', 455.7, 842.3);
    label(el, 'imp-label imp-sale-label', X(274.9 + 85.45), Y(83 + 20.2), 'sale-order impact ' + M['scope.Iminus'], 'bottom');
    label(el, 'imp-label imp-buy-label', X(563.6 + 85.45), Y(83 + 20.2), 'purchase impact ' + M['scope.Iplus'], 'bottom');
  }

  function levels(el, M) {
    // slide53.txt: x px = (x pt - 756.8) 5/3, y px = (y pt - 107) 5/3
    const X = (x) => (x - 756.8) * K, Y = (y) => (y - 107) * K;
    const root = svg('svg', { class: 'fig-svg', viewBox: '0 0 260 460', 'aria-hidden': 'true' }, el);
    [[120.8, 'scope.P1'], [285.2, 'scope.P0'], [365.2, 'scope.Pm1']].forEach(([y, key]) => {
      svg('path', { class: 'imp-level', d: `M${X(778.2)} ${Y(y)}H${X(860.1)}` }, root);
      label(el, 'imp-label imp-level-label', X(864.3), Y(y), M[key], 'left');
    });
    svg('path', { class: 'imp-brace imp-buy', d: brace(X(756.8), Y(122.6), Y(283.4), 11.4 * K) }, root);
    svg('path', { class: 'imp-brace imp-sale', d: brace(X(756.8), Y(285.2), Y(363.4), 11.4 * K) }, root);
  }

  TALK.figure('impact', {
    mount(el, ctx) {
      if (ctx.variant === 'b51') levels(el, ctx.math); else priceLine(el, ctx.math);
    },
    setStep() {},
  });
})();
