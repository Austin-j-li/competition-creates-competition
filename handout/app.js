/* Page shell: theme, tabs, progress, table of contents, collapsibles, stepper, math, self-check.
   Plain ES2019, no modules. KaTeX is a local copy loaded before this script. Runs on
   DOMContentLoaded. */
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
  /* The slides once stored their theme under "ccc-deck-theme"; one key now serves both. */
  try {
    var oldDeck = window.localStorage.getItem("ccc-deck-theme");
    if (oldDeck !== null) {
      if (readStored() === null && (oldDeck === "light" || oldDeck === "dark")) window.localStorage.setItem(STORAGE_KEY, oldDeck);
      window.localStorage.removeItem("ccc-deck-theme");
    }
  } catch (e) { /* private mode */ }
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

  /* ---------- tabs: research brief, read the paper, seminar talk ---------- */
  var TABS = ["brief", "paper", "talk"];
  function tabFromHash() {
    var h = window.location.hash;
    var m = /^#tab-(paper|talk)$/.exec(h);
    return m ? m[1] : "brief";
  }
  function showTab(name, opts) {
    opts = opts || {};
    if (TABS.indexOf(name) < 0) name = "brief";
    TABS.forEach(function (n) {
      var tab = document.getElementById("tablink-" + n);
      var panel = document.getElementById("panel-" + n);
      var on = n === name;
      if (tab) { tab.setAttribute("aria-selected", on ? "true" : "false"); tab.tabIndex = on ? 0 : -1; }
      if (panel) panel.hidden = !on;
    });
    document.documentElement.setAttribute("data-tab", name);
    if (opts.push) {
      try { history.replaceState(null, "", name === "brief" ? window.location.pathname + window.location.search : "#tab-" + name); }
      catch (e) { /* file URL */ }
    }
    if (name === "paper") mountViewer();
    if (opts.focus) { var tb = document.getElementById("tablink-" + name); if (tb) tb.focus(); }
    try { document.dispatchEvent(new CustomEvent("ccc:tabchange", { detail: { tab: name } })); }
    catch (e) { recordError("tabchange dispatch: " + e.message); }
  }
  CCC.showTab = showTab;
  function initTabs() {
    var list = document.querySelector("[role=tablist]");
    if (!list) return;
    list.addEventListener("click", function (ev) {
      var tab = ev.target.closest ? ev.target.closest("[role=tab]") : null;
      if (!tab) return;
      ev.preventDefault();
      showTab(tab.getAttribute("data-tab"), { push: true });
    });
    list.addEventListener("keydown", function (ev) {
      var tab = ev.target.closest ? ev.target.closest("[role=tab]") : null;
      if (!tab) return;
      var i = TABS.indexOf(tab.getAttribute("data-tab")), j = -1;
      if (ev.key === "ArrowRight") j = (i + 1) % TABS.length;
      else if (ev.key === "ArrowLeft") j = (i + TABS.length - 1) % TABS.length;
      else if (ev.key === "Home") j = 0;
      else if (ev.key === "End") j = TABS.length - 1;
      if (j < 0) return;
      ev.preventDefault();
      showTab(TABS[j], { push: true, focus: true });
    });
    // links that open a tab from inside the page
    document.addEventListener("click", function (ev) {
      var a = ev.target.closest ? ev.target.closest("a[data-open-tab]") : null;
      if (!a) return;
      ev.preventDefault();
      showTab(a.getAttribute("data-open-tab"), { push: true, focus: true });
      window.scrollTo(0, 0);
    });
    showTab(tabFromHash());
  }

  /* The inline PDF viewer mounts on first visit to the paper tab, so the PDF loads only on demand. */
  var viewerMounted = false;
  function mountViewer() {
    var host = document.querySelector("[data-viewer]");
    if (!host) return;
    if (!viewerMounted) {
      viewerMounted = true;
      host.addEventListener("click", function (ev) {
        var b = ev.target.closest ? ev.target.closest("[data-viewer-src]") : null;
        if (!b) return;
        setViewer(b.getAttribute("data-viewer-src"), b.getAttribute("data-viewer-title"));
      });
      var first = host.querySelector("[data-viewer-src]");
      if (first) setViewer(first.getAttribute("data-viewer-src"), first.getAttribute("data-viewer-title"));
    }
  }
  function setViewer(src, title) {
    var host = document.querySelector("[data-viewer]");
    var frame = host.querySelector("iframe");
    if (!frame) {
      frame = document.createElement("iframe");
      host.querySelector(".viewer-frame").appendChild(frame);
    }
    frame.title = title + ", inline viewer";
    frame.src = src + "#view=FitH";
    Array.prototype.forEach.call(host.querySelectorAll("[data-viewer-src]"), function (b) {
      b.setAttribute("aria-pressed", b.getAttribute("data-viewer-src") === src ? "true" : "false");
    });
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
      bar.style.transform = "scaleX(" + frac.toFixed(4) + ")";
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
    if (/^tab-(paper|talk)$/.test(id)) { showTab(id.slice(4)); return; }
    var target = document.getElementById(id);
    if (!target) return;
    var panel = target.closest ? target.closest("[role=tabpanel]") : null;
    if (panel && panel.hidden) showTab(panel.getAttribute("data-panel"));
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
    window.addEventListener("hashchange", function () {
      if (!window.location.hash) { showTab("brief"); return; }
      revealHash();
    });
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
  var SKIP = /^(SCRIPT|NOSCRIPT|STYLE|TEXTAREA|PRE|CODE)$/;
  function renderMathIn(root) {
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        var p = n.parentNode;
        if (!p || SKIP.test(p.nodeName) || (p.closest && p.closest(".katex"))) return NodeFilter.FILTER_REJECT;
        return /\\[\(\[]/.test(n.nodeValue) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_SKIP;
      }
    });
    var nodes = [], node;
    while ((node = walker.nextNode())) nodes.push(node);
    nodes.forEach(function (n) {
      var text = n.nodeValue, frag = document.createDocumentFragment(), i = 0, m;
      var re = /\\\(([\s\S]+?)\\\)|\\\[([\s\S]+?)\\\]/g;
      while ((m = re.exec(text))) {
        if (m.index > i) frag.appendChild(document.createTextNode(text.slice(i, m.index)));
        var display = m[2] !== undefined;
        var span = document.createElement("span");
        try {
          window.katex.render(display ? m[2] : m[1], span, { displayMode: display, throwOnError: false, trust: false });
        } catch (e) {
          recordError("KaTeX render: " + e.message);
          span.textContent = m[0];
          span.className = "katex-error";
        }
        frag.appendChild(span);
        i = m.index + m[0].length;
      }
      if (i < text.length) frag.appendChild(document.createTextNode(text.slice(i)));
      n.parentNode.replaceChild(frag, n);
    });
  }
  function renderMath() {
    return new Promise(function (resolve) {
      if (!window.katex || typeof window.katex.render !== "function") {
        recordError("KaTeX unavailable; math left as source");
        resolve(false);
        return;
      }
      try { renderMathIn(document.body); } catch (e) { recordError("KaTeX render: " + e.message); }
      katexErrors = document.querySelectorAll(".katex-error").length;
      resolve(true);
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
      theme: currentTheme(),
      tab: document.documentElement.getAttribute("data-tab"),
      fonts: document.fonts ? Array.prototype.filter.call(document.fonts, function (f) { return f.status === "loaded"; }).map(function (f) { return f.family + " " + f.weight + " " + f.style; }) : []
    };
  };

  /* ---------- boot ---------- */
  var readyResolve;
  CCC.ready = new Promise(function (res) { readyResolve = res; });

  function boot() {
    try { initTheme(); } catch (e) { recordError("theme: " + e.message); }
    try { initTabs(); } catch (e) { recordError("tabs: " + e.message); }
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
