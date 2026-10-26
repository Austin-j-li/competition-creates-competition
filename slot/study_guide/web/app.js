/* Study guide shell: local math, contents, theme, charts, and self-checks. */
(function () {
  "use strict";
  var CCC = window.CCC = window.CCC || {};
  var errors = [];
  var katexErrors = 0;
  function recordError(message) {
    errors.push(String(message));
    var banner = document.getElementById("debug-banner");
    if (banner && !banner.hidden) banner.textContent = errors.join("\n");
  }
  window.addEventListener("error", function (event) {
    recordError((event.message || "error") + (event.filename ? " (" + event.filename + ":" + event.lineno + ")" : ""));
  });
  window.addEventListener("unhandledrejection", function (event) {
    recordError("unhandled rejection: " + (event.reason && event.reason.message ? event.reason.message : String(event.reason)));
  });
  CCC.errors = errors;
  CCC.debug = new URLSearchParams(window.location.search).get("debug") === "1";

  function currentTheme() { return document.documentElement.getAttribute("data-theme") === "dark" ? "dark" : "light"; }
  function applyTheme(theme, persist) {
    theme = theme === "dark" ? "dark" : "light";
    document.documentElement.setAttribute("data-theme", theme);
    var button = document.getElementById("theme-toggle");
    if (button) {
      button.textContent = theme === "dark" ? "Light" : "Dark";
      button.setAttribute("aria-label", "Switch to " + (theme === "dark" ? "light" : "dark") + " theme");
    }
    if (persist) {
      try { localStorage.setItem("ccc-guide-theme", theme); } catch (e) { /* private mode */ }
    }
    document.dispatchEvent(new CustomEvent("ccc:themechange", { detail: { theme: theme } }));
  }
  CCC.theme = { get: currentTheme, set: function (theme) { applyTheme(theme, true); }, toggle: function () { applyTheme(currentTheme() === "dark" ? "light" : "dark", true); } };
  function initTheme() {
    var button = document.getElementById("theme-toggle");
    if (button) button.addEventListener("click", CCC.theme.toggle);
    applyTheme(currentTheme(), false);
    var query = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;
    if (query) query.addEventListener("change", function (event) {
      var stored = null;
      try { stored = localStorage.getItem("ccc-guide-theme"); } catch (e) { stored = null; }
      if (!stored) applyTheme(event.matches ? "dark" : "light", false);
    });
  }

  var SKIP = /^(SCRIPT|NOSCRIPT|STYLE|TEXTAREA|PRE|CODE)$/;
  function renderMathIn(root) {
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: function (node) {
        var parent = node.parentNode;
        if (!parent || SKIP.test(parent.nodeName) || parent.namespaceURI === "http://www.w3.org/2000/svg" ||
            (parent.closest && parent.closest(".katex"))) return NodeFilter.FILTER_REJECT;
        return /\\[\(\[]/.test(node.nodeValue) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_SKIP;
      }
    });
    var nodes = [], node;
    while ((node = walker.nextNode())) nodes.push(node);
    nodes.forEach(function (textNode) {
      var text = textNode.nodeValue, fragment = document.createDocumentFragment(), index = 0, match;
      var pattern = /\\\(([\s\S]+?)\\\)|\\\[([\s\S]+?)\\\]/g;
      while ((match = pattern.exec(text))) {
        if (match.index > index) fragment.appendChild(document.createTextNode(text.slice(index, match.index)));
        var display = match[2] !== undefined;
        var span = document.createElement(display ? "div" : "span");
        if (display) span.className = "math-block";
        var source = display ? match[2] : match[1];
        var equationId = /\\htmlId\{([^}]+)\}\{\}/.exec(source);
        if (equationId) {
          if (!textNode.parentNode.id) span.id = equationId[1];
          source = source.replace(/\\htmlId\{[^}]+\}\{\}/, "");
        }
        try {
          window.katex.render(source, span, {
            displayMode: display, throwOnError: false, trust: false, strict: "ignore"
          });
        } catch (error) {
          recordError("KaTeX: " + error.message);
          span.textContent = match[0];
          span.className += " katex-error";
        }
        fragment.appendChild(span);
        index = match.index + match[0].length;
      }
      if (index < text.length) fragment.appendChild(document.createTextNode(text.slice(index)));
      textNode.parentNode.replaceChild(fragment, textNode);
    });
  }
  function renderMath() {
    if (!window.katex) {
      recordError("KaTeX unavailable; equations remain as source");
      return;
    }
    renderMathIn(document.body);
    katexErrors = document.querySelectorAll(".katex-error").length;
  }

  function initToc() {
    var nav = document.getElementById("toc");
    var desktop = nav.querySelector(".toc-desktop");
    var mobileBody = nav.querySelector(".toc-mobile-body");
    function place() {
      if (window.innerWidth < 1024) {
        if (desktop.parentNode !== mobileBody) mobileBody.appendChild(desktop);
      } else if (desktop.parentNode !== nav) nav.appendChild(desktop);
    }
    place();
    window.addEventListener("resize", place);
    nav.querySelector(".toc-mobile summary").addEventListener("click", function () {
      window.requestAnimationFrame(function () { if (window.innerWidth < 1024) desktop.style.display = "block"; });
    });
    var input = document.getElementById("toc-search");
    var empty = document.getElementById("toc-empty");
    input.addEventListener("input", function () {
      var query = input.value.trim().toLowerCase(), count = 0;
      nav.querySelectorAll(".toc-part").forEach(function (part) {
        var visible = 0;
        part.querySelectorAll("li[data-searchable]").forEach(function (item) {
          var show = !query || item.getAttribute("data-searchable").indexOf(query) !== -1;
          item.hidden = !show;
          if (show) visible += 1;
        });
        part.hidden = visible === 0;
        count += visible;
      });
      empty.hidden = count !== 0;
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "/" && !/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName)) {
        event.preventDefault();
        if (window.innerWidth < 1024) nav.querySelector(".toc-mobile").open = true;
        input.focus();
      }
    });
  }

  function openAncestors(element) {
    var node = element;
    while (node && node !== document.body) {
      if (node.tagName === "DETAILS") node.open = true;
      node = node.parentNode;
    }
  }
  function revealHash() {
    if (!window.location.hash) return;
    var id;
    try { id = decodeURIComponent(window.location.hash.slice(1)); } catch (e) { return; }
    var target = document.getElementById(id);
    if (!target) return;
    openAncestors(target);
    window.requestAnimationFrame(function () { target.scrollIntoView({ behavior: "instant", block: "start" }); });
  }
  function initLinks() {
    document.addEventListener("click", function (event) {
      var link = event.target.closest ? event.target.closest("a[href^='#']") : null;
      if (!link) return;
      var target = document.getElementById(link.getAttribute("href").slice(1));
      if (target) openAncestors(target);
    });
    window.addEventListener("hashchange", revealHash);
    revealHash();
  }

  function initSectionNavigation() {
    var host = document.getElementById("section-nav-inner");
    if (!host || !("IntersectionObserver" in window)) return;
    var chapters = Array.prototype.slice.call(document.querySelectorAll(".chapter"));
    var current = null;
    function select(chapter) {
      if (!chapter || chapter === current) return;
      current = chapter;
      var heading = chapter.querySelector("h2");
      host.innerHTML = "";
      var title = document.createElement("h2");
      title.textContent = "In this chapter";
      host.appendChild(title);
      var list = document.createElement("ol");
      chapter.querySelectorAll("h3[id]").forEach(function (subheading) {
        var item = document.createElement("li"), link = document.createElement("a");
        link.href = "#" + subheading.id;
        link.textContent = subheading.textContent;
        item.appendChild(link);
        list.appendChild(item);
      });
      host.appendChild(list);
      document.querySelectorAll(".toc-part a[aria-current]").forEach(function (link) { link.removeAttribute("aria-current"); });
      var active = document.querySelector(".toc-part a[href='#" + heading.id + "']");
      if (active) active.setAttribute("aria-current", "location");
    }
    var visible = new Map();
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) { visible.set(entry.target, entry.isIntersecting); });
      var chosen = chapters.find(function (chapter) { return visible.get(chapter); });
      if (chosen) select(chosen);
    }, { rootMargin: "-10% 0px -70% 0px", threshold: 0 });
    chapters.forEach(function (chapter) { observer.observe(chapter); });
    select(chapters[0]);
  }

  CCC.selfCheck = function () {
    var ids = {}, duplicates = [];
    document.querySelectorAll("[id]").forEach(function (element) {
      if (ids[element.id]) duplicates.push(element.id);
      ids[element.id] = true;
    });
    var brokenLinks = [];
    document.querySelectorAll("a[href^='#']").forEach(function (link) {
      var href = link.getAttribute("href");
      if (href.length > 1 && !document.getElementById(href.slice(1))) brokenLinks.push(href);
    });
    return {
      chapters: document.querySelectorAll(".chapter").length,
      parts: document.querySelectorAll(".part").length,
      tables: document.querySelectorAll("table").length,
      diagrams: document.querySelectorAll(".diagram").length,
      katexErrors: katexErrors,
      duplicateIds: duplicates,
      brokenLinks: brokenLinks,
      charts: CCC.charts && CCC.charts.status ? CCC.charts.status() : {},
      explorer: CCC.explorer && CCC.explorer.status ? CCC.explorer.status() : null,
      consoleErrors: errors.slice(),
      theme: currentTheme()
    };
  };
  var readyResolve;
  CCC.ready = new Promise(function (resolve) { readyResolve = resolve; });
  function boot() {
    try { initTheme(); } catch (e) { recordError(e.message); }
    try { initToc(); } catch (e) { recordError(e.message); }
    try { initLinks(); } catch (e) { recordError(e.message); }
    try { renderMath(); } catch (e) { recordError(e.message); }
    try { if (CCC.explorer) CCC.explorer.init(); } catch (e) { recordError(e.message); }
    try { if (CCC.charts) CCC.charts.mountAll(); } catch (e) { recordError(e.message); }
    try { initSectionNavigation(); } catch (e) { recordError(e.message); }
    if (CCC.debug) {
      var banner = document.getElementById("debug-banner");
      banner.hidden = false;
      banner.textContent = errors.length ? errors.join("\n") : "No errors collected";
    }
    readyResolve(CCC.selfCheck());
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
