/* Page shell: theme, progress, table of contents, collapsibles, stepper, math, self-check.
   Plain ES2019, no modules, no dependencies. Runs on DOMContentLoaded; CDN scripts are deferred
   and therefore already executed by then. */
(function () {
  "use strict";

  /* ---------- error collector (installed before anything else) ---------- */
  var errors = [];
  function recordError(msg) {
    errors.push(String(msg));
    if (errors.length > 200) errors.shift();
    var banner = document.getElementById("debug-banner");
    if (banner && !banner.hidden) banner.textContent = errors.join("\n");
  }
  window.addEventListener("error", function (ev) {
    var where = ev.filename ? " (" + ev.filename + ":" + ev.lineno + ")" : "";
    recordError((ev.message || "error") + where);
  });
  window.addEventListener("unhandledrejection", function (ev) {
    var r = ev.reason;
    recordError("unhandled rejection: " + (r && r.message ? r.message : String(r)));
  });

  var CCC = (window.CCC = window.CCC || {});
  var params = new URLSearchParams(window.location.search);
  CCC.eager = params.get("lazy") === "1" ? false : true; // charts mount eagerly unless ?lazy=1
  CCC.openAll = params.get("eager") === "1";              // ?eager=1 also opens every <details>
  CCC.debug = params.get("debug") === "1";
  CCC.errors = errors;

  var mql = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;
  var STORAGE_KEY = "ccc-theme";

  /* ---------- theme ---------- */
  function readStored() {
    try { return window.localStorage.getItem(STORAGE_KEY); } catch (e) { return null; }
  }
  function writeStored(v) {
    try { window.localStorage.setItem(STORAGE_KEY, v); } catch (e) { /* private mode */ }
  }
  function currentTheme() {
    var t = document.documentElement.getAttribute("data-theme");
    return t === "dark" ? "dark" : "light";
  }
  function updateToggle() {
    var btn = document.getElementById("theme-toggle");
    if (!btn) return;
    var t = currentTheme();
    btn.textContent = t === "dark" ? "Light" : "Dark";
    btn.setAttribute("aria-label", "Switch to " + (t === "dark" ? "light" : "dark") + " theme");
  }
  function applyTheme(name, persist) {
    var t = name === "dark" ? "dark" : "light";
    document.documentElement.setAttribute("data-theme", t);
    if (persist) writeStored(t);
    updateToggle();
    try {
      document.dispatchEvent(new CustomEvent("ccc:themechange", { detail: { theme: t } }));
    } catch (e) { recordError("themechange dispatch: " + e.message); }
  }
  CCC.theme = {
    get: currentTheme,
    set: function (name) { applyTheme(name, true); },
    toggle: function () { applyTheme(currentTheme() === "dark" ? "light" : "dark", true); }
  };
  function initTheme() {
    var q = params.get("theme");
    if (q === "light" || q === "dark") applyTheme(q, false);
    var btn = document.getElementById("theme-toggle");
    if (btn) btn.addEventListener("click", CCC.theme.toggle);
    updateToggle();
    if (mql) {
      var onChange = function (ev) {
        if (readStored() === null && !(params.get("theme") === "light" || params.get("theme") === "dark")) {
          applyTheme(ev.matches ? "dark" : "light", false);
        }
      };
      if (typeof mql.addEventListener === "function") mql.addEventListener("change", onChange);
      else if (typeof mql.addListener === "function") mql.addListener(onChange);
    }
  }

  /* ---------- progress bar ---------- */
  function initProgress() {
    var bar = document.getElementById("progress");
    if (!bar) return;
    var ticking = false;
    function update() {
      ticking = false;
      var doc = document.documentElement;
      var max = doc.scrollHeight - window.innerHeight;
      var frac = max > 0 ? Math.min(1, Math.max(0, window.scrollY / max)) : 0;
      bar.style.width = (frac * 100).toFixed(2) + "%";
    }
    function onScroll() {
      if (!ticking) { ticking = true; window.requestAnimationFrame(update); }
    }
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    update();
  }

  /* ---------- table of contents: drawer on narrow screens, scrollspy ---------- */
  function initTocDrawer() {
    var nav = document.getElementById("toc");
    if (!nav) return;
    var list = nav.querySelector("ol");
    if (!list) return;
    var wrapped = false;
    function apply() {
      var narrow = window.innerWidth < 1024;
      if (narrow && !wrapped) {
        var details = document.createElement("details");
        details.className = "toc-drawer";
        var summary = document.createElement("summary");
        summary.textContent = "Contents";
        details.appendChild(summary);
        list.parentNode.insertBefore(details, list);
        details.appendChild(list);
        wrapped = true;
      } else if (!narrow && wrapped) {
        var d = nav.querySelector("details.toc-drawer");
        if (d) { nav.insertBefore(list, d); d.parentNode.removeChild(d); }
        wrapped = false;
      }
    }
    apply();
    window.addEventListener("resize", apply);
    // close the drawer after a link is chosen on narrow screens
    nav.addEventListener("click", function (ev) {
      var a = ev.target.closest ? ev.target.closest("a") : null;
      if (a && wrapped) {
        var d = nav.querySelector("details.toc-drawer");
        if (d) d.open = false;
      }
    });
  }

  function initScrollspy() {
    var nav = document.getElementById("toc");
    var main = document.getElementById("main");
    if (!nav || !main) return;
    var headings = Array.prototype.slice.call(main.querySelectorAll("section.sec > h2"));
    // an h2 without an id borrows its section's id so the TOC link (#sec-…) matches
    headings.forEach(function (h) {
      if (!h.id) { var sec = h.closest("section.sec"); if (sec && sec.id) h.id = sec.id + "-h2"; }
    });
    headings = headings.filter(function (h) { return !!h.id; });
    if (!headings.length) return;
    var links = {};
    Array.prototype.forEach.call(nav.querySelectorAll("a[href^='#']"), function (a) {
      var key = a.getAttribute("href").slice(1);
      links[key] = a;
      links[key + "-h2"] = a; // section link also answers for its heading
    });
    var active = null;
    function setActive(id) {
      if (id === active) return;
      if (active && links[active]) links[active].removeAttribute("aria-current");
      active = id;
      if (id && links[id]) {
        links[id].setAttribute("aria-current", "location");
        // keep the active link in view inside the sticky nav
        var a = links[id];
        var box = nav.getBoundingClientRect();
        var r = a.getBoundingClientRect();
        // adjust only the nav's own scroll position; scrollIntoView would also move the page
        if (r.top < box.top) nav.scrollTop -= (box.top - r.top) + 8;
        else if (r.bottom > box.bottom) nav.scrollTop += (r.bottom - box.bottom) + 8;
      }
    }
    function fallback() {
      var cutoff = window.innerHeight * 0.3;
      var pick = null;
      for (var i = 0; i < headings.length; i++) {
        if (headings[i].getBoundingClientRect().top <= cutoff) pick = headings[i];
        else break;
      }
      setActive(pick ? pick.id : headings[0].id);
    }
    if ("IntersectionObserver" in window) {
      var visible = {};
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) { visible[en.target.id] = en.isIntersecting; });
        var pick = null;
        for (var i = 0; i < headings.length; i++) {
          if (visible[headings[i].id]) { pick = headings[i]; break; }
        }
        if (pick) setActive(pick.id); else fallback();
      }, { rootMargin: "-15% 0px -75% 0px", threshold: 0 });
      headings.forEach(function (h) { io.observe(h); });
    }
    var ticking = false;
    window.addEventListener("scroll", function () {
      if (!ticking) {
        ticking = true;
        window.requestAnimationFrame(function () { ticking = false; fallback(); });
      }
    }, { passive: true });
    fallback();
  }

  /* ---------- collapsibles ---------- */
  function openAncestors(el) {
    var node = el;
    while (node && node !== document.body) {
      if (node.tagName === "DETAILS") node.open = true;
      node = node.parentNode;
    }
  }
  function revealHash() {
    var id;
    try { id = decodeURIComponent(window.location.hash.slice(1)); } catch (e) { return; }
    if (!id) return;
    var target = document.getElementById(id);
    if (!target) return;
    openAncestors(target);
    if (target.tagName === "DETAILS") target.open = true;
    // A browser cannot scroll to an anchor until its enclosing disclosure is open.
    window.requestAnimationFrame(function () { target.scrollIntoView({ behavior: "instant", block: "start" }); });
  }
  function initDetails() {
    if (CCC.openAll) {
      Array.prototype.forEach.call(document.querySelectorAll("details"), function (d) {
        if (!d.classList.contains("toc-drawer")) d.open = true;
      });
    }
    revealHash();
    window.addEventListener("hashchange", revealHash);
    // links to ids inside closed details (same page) open them before the jump
    document.addEventListener("click", function (ev) {
      var a = ev.target.closest ? ev.target.closest("a[href^='#']") : null;
      if (!a) return;
      var t = document.getElementById(a.getAttribute("href").slice(1));
      if (t) openAncestors(t);
    });
  }

  /* ---------- stepper ---------- */
  function initSteppers() {
    Array.prototype.forEach.call(document.querySelectorAll("[data-stepper]"), function (list) {
      var items = Array.prototype.slice.call(list.querySelectorAll("li[data-step]"));
      if (!items.length) return;
      var panel = document.createElement("div");
      panel.className = "stepper-panel";
      panel.setAttribute("aria-live", "polite");
      list.parentNode.insertBefore(panel, list.nextSibling);
      var current = -1;
      function select(i, focus) {
        if (i < 0) i = items.length - 1;
        if (i >= items.length) i = 0;
        items.forEach(function (li, j) {
          if (j === i) li.setAttribute("aria-current", "step");
          else li.removeAttribute("aria-current");
          var b = li.querySelector(".step-btn");
          if (b) b.setAttribute("aria-pressed", j === i ? "true" : "false");
        });
        var note = items[i].querySelector(".step-note");
        panel.innerHTML = note ? note.innerHTML : "";
        current = i;
        if (focus) {
          var b2 = items[i].querySelector(".step-btn");
          if (b2) b2.focus();
        }
      }
      items.forEach(function (li, i) {
        var btn = li.querySelector(".step-btn");
        if (!btn) return;
        btn.addEventListener("click", function () { select(i, false); });
      });
      list.addEventListener("keydown", function (ev) {
        if (ev.key === "ArrowRight" || ev.key === "ArrowDown") { ev.preventDefault(); select(current + 1, true); }
        else if (ev.key === "ArrowLeft" || ev.key === "ArrowUp") { ev.preventDefault(); select(current - 1, true); }
        else if (ev.key === "Home") { ev.preventDefault(); select(0, true); }
        else if (ev.key === "End") { ev.preventDefault(); select(items.length - 1, true); }
      });
      select(0, false);
    });
  }

  /* ---------- math ---------- */
  var katexErrors = 0;
  function renderMath() {
    return new Promise(function (resolve) {
      function run() {
        if (typeof window.renderMathInElement !== "function") {
          recordError("KaTeX auto-render unavailable; math left as source");
          resolve(false);
          return;
        }
        try {
          window.renderMathInElement(document.body, {
            delimiters: [
              { left: "\\[", right: "\\]", display: true },
              { left: "\\(", right: "\\)", display: false }
            ],
            throwOnError: false,
            ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code"]
          });
        } catch (e) {
          recordError("KaTeX render: " + e.message);
        }
        katexErrors = document.querySelectorAll(".katex-error").length;
        resolve(true);
      }
      if (typeof window.renderMathInElement === "function") run();
      else if (document.readyState === "complete") run();
      else window.addEventListener("load", run, { once: true });
    });
  }

  /* ---------- debug banner ---------- */
  function initDebug() {
    if (!CCC.debug) return;
    var banner = document.getElementById("debug-banner");
    if (!banner) return;
    banner.hidden = false;
    banner.textContent = errors.length ? errors.join("\n") : "no errors collected";
    window.setInterval(function () {
      banner.textContent = errors.length ? errors.join("\n") : "no errors collected";
    }, 1000);
  }

  /* ---------- self check ---------- */
  function countUnresolved() {
    var main = document.getElementById("main") || document.body;
    var walker = document.createTreeWalker(main, NodeFilter.SHOW_TEXT, null);
    var re = /\[\[[A-Za-z0-9_]+\]\]/;
    var n = 0;
    var node;
    while ((node = walker.nextNode())) {
      if (re.test(node.nodeValue)) n++;
    }
    return n;
  }
  CCC.selfCheck = function () {
    var details = document.querySelectorAll("details");
    var open = 0;
    Array.prototype.forEach.call(details, function (d) { if (d.open) open++; });
    return {
      charts: (CCC.charts && typeof CCC.charts.status === "function") ? CCC.charts.status() : {},
      katexErrors: katexErrors,
      unresolvedPlaceholders: countUnresolved(),
      explorer: (CCC.explorer && typeof CCC.explorer.status === "function") ? CCC.explorer.status() : null,
      consoleErrors: errors.slice(),
      details: { total: details.length, open: open },
      theme: currentTheme()
    };
  };

  /* ---------- boot ---------- */
  var readyResolve;
  CCC.ready = new Promise(function (res) { readyResolve = res; });

  function boot() {
    try { initTheme(); } catch (e) { recordError("theme: " + e.message); }
    try { initProgress(); } catch (e) { recordError("progress: " + e.message); }
    try { initTocDrawer(); } catch (e) { recordError("toc drawer: " + e.message); }
    try { initScrollspy(); } catch (e) { recordError("scrollspy: " + e.message); }
    try { initDetails(); } catch (e) { recordError("details: " + e.message); }
    try { initSteppers(); } catch (e) { recordError("stepper: " + e.message); }
    try { initDebug(); } catch (e) { recordError("debug: " + e.message); }

    renderMath().then(function () {
      try {
        if (CCC.charts && typeof CCC.charts.mountAll === "function") CCC.charts.mountAll();
      } catch (e) { recordError("charts.mountAll: " + e.message); }
      try {
        if (CCC.explorer && typeof CCC.explorer.init === "function") CCC.explorer.init();
      } catch (e) { recordError("explorer.init: " + e.message); }
      // give lazy mounts and the explorer's first draw a tick before resolving
      window.setTimeout(function () { revealHash(); readyResolve(CCC.selfCheck()); }, 0);
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
