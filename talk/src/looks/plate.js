/* plate.js: ink is laid down.
   On each click of the plate look, the step's new elements are wiped in behind a hard edge
   (clip-path, as a press pass lays an area; a line is drawn along its direction). When a click
   brings marks in the orange accent and other marks, the others go down first and the orange
   120 ms later. (The names isGreen and green below test for the accent.)
   Text is set in 240 ms, lines and areas take 380 ms. Web Animations inside #stage, so a key press
   finishes them; nothing runs under ?static=1, ?motion=0 or reduced motion (the engine marks no
   new elements then). The bars on page 11 animate themselves, so they are left alone. */
(function () {
  'use strict';
  var doc = document;
  var EASE = 'cubic-bezier(.16,1,.3,1)';
  var SECOND_INK = 120;
  var running = null;

  function accentOf() {
    return getComputedStyle(doc.body).getPropertyValue('--accent').trim();
  }

  var probe = null;
  function toRgb(css) {
    if (!probe) { probe = doc.createElement('span'); probe.style.display = 'none'; doc.body.appendChild(probe); }
    probe.style.color = '';
    probe.style.color = css;
    return getComputedStyle(probe).color;
  }

  function isSvg(el) { return el instanceof SVGElement; }

  function isGreen(el, green) {
    if (!green) return false;
    var cs = getComputedStyle(el);
    if (isSvg(el)) {
      return cs.stroke === green || cs.fill === green || cs.color === green;
    }
    if (cs.color === green) return true;
    if (el.matches('[data-inc="1"]') && el.closest('table.matrix')) return true;
    return false;
  }

  function hasGreenInside(el, green) {
    if (isGreen(el, green)) return true;
    var all = el.querySelectorAll('*');
    for (var i = 0; i < all.length && i < 40; i++) if (isGreen(all[i], green)) return true;
    return false;
  }

  // which way the ink travels: along the mark's own long direction
  function axisOf(el) {
    var r;
    try { r = el.getBoundingClientRect(); } catch (e) { return 'x'; }
    if (isSvg(el) && r.height > 2.2 * r.width) return 'y';
    return 'x';
  }

  function keyframes(el, axis, svg) {
    var box = svg ? ' stroke-box' : '';
    if (axis === 'y') {
      return [
        { clipPath: 'inset(0 0 100% 0)' + box },
        { clipPath: 'inset(0 0 0 0)' + box },
      ];
    }
    var pad = svg ? '0' : '-0.3em';          // keep ascenders and descenders of set type
    return [
      { clipPath: 'inset(' + pad + ' 100% ' + pad + ' 0)' + box },
      { clipPath: 'inset(' + pad + ' -2px ' + pad + ' 0)' + box },
    ];
  }

  function lay(el, delay, dur) {
    var svg = isSvg(el);
    var anim;
    try {
      anim = el.animate(keyframes(el, axisOf(el), svg), { duration: dur, delay: delay, easing: EASE, fill: 'both' });
    } catch (e) { return null; }
    // when it ends, drop the clip so nothing stays clipped
    anim.finished.then(function () { try { anim.cancel(); } catch (e) { /* gone */ } }, function () { /* cancelled */ });
    return anim;
  }

  function onState(ev) {
    if (doc.body.dataset.look !== 'plate') return;
    var d = ev.detail || {};
    if (running) { running.finish(); }
    if (!d.animate || !d.newEls || !d.newEls.length) return;
    if (TALK.reduced && TALK.reduced()) return;

    var els = [].slice.call(d.newEls).filter(function (el) {
      return !el.closest('.fig[data-fig="bars"]') && !el.classList.contains('bars-note');
    });
    if (!els.length) return;

    var green = toRgb(accentOf());
    var groups = els.map(function (el) { return { el: el, green: hasGreenInside(el, green) }; });
    var both = groups.some(function (g) { return g.green; }) && groups.some(function (g) { return !g.green; });
    var anims = [];
    groups.forEach(function (g) {
      var area = isSvg(g.el) || g.el.matches('td, th') || g.el.classList.contains('is-band');
      var dur = area ? 380 : 240;
      var delay = both && g.green ? SECOND_INK : 0;
      var a = lay(g.el, delay, dur);
      if (a) anims.push(a);
    });
    if (!anims.length) return;

    var done = false;
    var handle = {
      finish: function () {
        if (done) return;
        done = true;
        anims.forEach(function (a) { try { a.finish(); a.cancel(); } catch (e) { /* ignore */ } });
        if (unregister) unregister();
        if (running === handle) running = null;
      },
    };
    var unregister = TALK.motion(handle);
    running = handle;
    Promise.all(anims.map(function (a) { return a.finished; })).then(handle.finish, handle.finish);
  }

  doc.addEventListener('talk:state', onState);
})();
