"""Accessible HTML and SVG diagrams for the study guide."""

from html import escape


def _figure(label: str, modifier: str, visual: str, caption_html: str, prefix: str) -> str:
    return (
        f'<figure class="diagram {modifier}" id="{escape(label, quote=True)}">'
        f"{visual}"
        f"<figcaption><strong>{prefix}</strong> {caption_html}</figcaption>"
        "</figure>"
    )


def _svg(label: str, classes: str, view_box: str, title: str, description: str, content: str) -> str:
    safe_label = escape(label, quote=True)
    marker_id = escape(label.replace(":", "-") + "-arrow", quote=True)
    content = content.replace("url(#diagram-arrow)", f"url(#{marker_id})")
    return (
        f'<svg class="diagram-svg {classes}" viewBox="{view_box}" '
        f'role="img" aria-labelledby="{safe_label}-title {safe_label}-description" '
        f'preserveAspectRatio="xMidYMid meet">'
        f'<title id="{safe_label}-title">{escape(title)}</title>'
        f'<desc id="{safe_label}-description">{escape(description)}</desc>'
        f'<defs><marker id="{marker_id}" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"></path></marker></defs>'
        f"{content}</svg>"
    )


def _brief_chain() -> str:
    content = r"""
<g class="flow-grid" font-family="inherit" fill="currentColor" font-size="17" text-anchor="middle">
  <g class="flow-node information-channel">
    <rect x="30" y="35" width="320" height="112" rx="10" fill="none" stroke="currentColor"></rect>
    <text x="190" y="72"><tspan x="190">Stronger incumbent</tspan><tspan x="190" dy="28">\(F\) falls; \(r\) rises</tspan></text>
  </g>
  <g class="flow-node information-channel">
    <rect x="380" y="35" width="320" height="112" rx="10" fill="none" stroke="currentColor"></rect>
    <text x="540" y="66"><tspan x="540">Larger target-payoff spread</tspan><tspan x="540" dy="28">\(\Delta_T=t_H-t_L\)</tspan><tspan x="540" dy="25">between classes</tspan></text>
  </g>
  <g class="flow-node information-channel">
    <rect x="730" y="35" width="320" height="112" rx="10" fill="none" stroke="currentColor"></rect>
    <text x="890" y="62"><tspan x="890">Residual advantage</tspan><tspan x="890" dy="28">\(\rho\,\kappa(\pi)\,\Delta_T \gt k\)</tspan><tspan x="890" dy="25">for a correctly signed order</tspan></text>
  </g>
  <g class="flow-node information-channel">
    <rect x="730" y="220" width="320" height="112" rx="10" fill="none" stroke="currentColor"></rect>
    <text x="890" y="260"><tspan x="890">Informative orders</tspan><tspan x="890" dy="30">class \(H\) buys; class \(L\) sells</tspan></text>
  </g>
  <g class="flow-node information-channel">
    <rect x="380" y="220" width="320" height="112" rx="10" fill="none" stroke="currentColor"></rect>
    <text x="540" y="252"><tspan x="540">A purchase lifts the belief</tspan><tspan x="540" dy="28">to \(M(\pi)\), above \(\tau\)</tspan></text>
  </g>
  <g class="flow-node information-channel">
    <rect x="30" y="220" width="320" height="112" rx="10" fill="none" stroke="currentColor"></rect>
    <text x="190" y="250"><tspan x="190">High-cost challenger prepares</tspan><tspan x="190" dy="28">after a purchase</tspan><tspan x="190" dy="25">entry rises above \(\rho\)</tspan></text>
  </g>
  <g class="flow-arrow information-channel" fill="none" stroke="currentColor" stroke-width="3" marker-end="url(#diagram-arrow)">
    <path d="M350 91 H374"></path><path d="M700 91 H724"></path>
    <path d="M890 147 V214"></path><path d="M730 276 H706"></path><path d="M380 276 H356"></path>
  </g>
  <g class="flow-node deterrence-channel">
    <rect x="30" y="410" width="500" height="92" rx="10" fill="none" stroke="currentColor"></rect>
    <text x="280" y="444"><tspan x="280">Direct deterrence: gross profit \(B_F(\mu)\) falls</tspan><tspan x="280" dy="27">at every \(\mu\)</tspan></text>
  </g>
  <g class="flow-arrow deterrence-channel" fill="none" stroke="currentColor" stroke-width="3">
    <path d="M30 91 H12 V456 H24" marker-end="url(#diagram-arrow)"></path>
    <path d="M530 456 H570 V338" stroke-dasharray="8 6" marker-end="url(#diagram-arrow)"></path>
    <text x="585" y="405" text-anchor="start" stroke="none" fill="currentColor"><tspan x="585">raises \(\tau\):</tspan><tspan x="585" dy="25">works against entry</tspan></text>
  </g>
</g>"""
    return _svg(
        "fig:01_brief-chain",
        "flow-grid",
        "0 0 1080 530",
        "Information and deterrence channels",
        "A stronger incumbent increases the target-payoff spread, induces informative trading, and can recruit a high-cost challenger. Its direct effect lowers gross profit and opposes entry.",
        content,
    )


def _model_timing() -> str:
    content = r"""
<g class="timeline" font-family="inherit" fill="currentColor" text-anchor="middle">
  <path class="timeline-axis" d="M38 80 H1160" fill="none" stroke="currentColor" stroke-width="3" marker-end="url(#diagram-arrow)"></path>
  <g class="timeline-moves" font-size="16">
    <g class="timeline-move"><circle cx="110" cy="80" r="9"></circle><text x="110" y="52" font-weight="700">1</text><rect x="20" y="125" width="180" height="190" rx="9" fill="none" stroke="currentColor"></rect><text x="110" y="158"><tspan x="110">Seller announces a</tspan><tspan x="110" dy="24">cash second-price</tspan><tspan x="110" dy="24">auction with</tspan><tspan x="110" dy="24">reserve \(p\)</tspan></text></g>
    <g class="timeline-move"><circle cx="306" cy="80" r="9"></circle><text x="306" y="52" font-weight="700">2</text><rect x="216" y="125" width="180" height="190" rx="9" fill="none" stroke="currentColor"></rect><text x="306" y="170"><tspan x="306">Investor learns</tspan><tspan x="306" dy="26">the class \(j\)</tspan></text></g>
    <g class="timeline-move"><circle cx="502" cy="80" r="9"></circle><text x="502" y="52" font-weight="700">3</text><rect x="412" y="125" width="180" height="190" rx="9" fill="none" stroke="currentColor"></rect><text x="502" y="153"><tspan x="502">Slot draw: investor</tspan><tspan x="502" dy="23">with probability \(\lambda\),</tspan><tspan x="502" dy="23">or liquidity trader,</tspan><tspan x="502" dy="23">places</tspan><tspan x="502" dy="23">\(X\in\{-1,0,1\}\)</tspan></text></g>
    <g class="timeline-move"><circle cx="698" cy="80" r="9"></circle><text x="698" y="52" font-weight="700">4</text><rect x="608" y="125" width="180" height="190" rx="9" fill="none" stroke="currentColor"></rect><text x="698" y="158"><tspan x="698">Market makers</tspan><tspan x="698" dy="24">see \(X\) and set</tspan><tspan x="698" dy="24">\(P=\mathbb{E}[V_T\mid X]\)</tspan></text></g>
    <g class="timeline-move"><circle cx="894" cy="80" r="9"></circle><text x="894" y="52" font-weight="700">5</text><rect x="804" y="125" width="180" height="190" rx="9" fill="none" stroke="currentColor"></rect><text x="894" y="151"><tspan x="894">Challenger sees \(P\),</tspan><tspan x="894" dy="23">learns its cost \(C\),</tspan><tspan x="894" dy="23">then decides</tspan><tspan x="894" dy="23">whether to prepare</tspan></text></g>
    <g class="timeline-move"><circle cx="1090" cy="80" r="9"></circle><text x="1090" y="52" font-weight="700">6</text><rect x="1000" y="125" width="180" height="190" rx="9" fill="none" stroke="currentColor"></rect><text x="1090" y="151"><tspan x="1090">Prepared bidders</tspan><tspan x="1090" dy="23">learn values and</tspan><tspan x="1090" dy="23">bid truthfully;</tspan><tspan x="1090" dy="23">payoffs are realized</tspan></text></g>
  </g>
  <text class="timeline-note" x="600" y="355" font-size="16">The price forms before the challenger decides, so market prices can affect real entry.</text>
</g>"""
    return _svg(
        "fig:02_model-timing",
        "timeline",
        "0 0 1200 380",
        "Sequence of six moves",
        "The seller announces the auction, the investor learns the class, the order slot is drawn, market makers set the price, the challenger decides whether to prepare, and prepared bidders learn values and bid.",
        content,
    )


def _auction_proceeds() -> str:
    content = r"""
<g class="proceeds-plot" font-family="inherit" fill="currentColor" font-size="17">
  <path class="proceeds-gap" d="M380 300 L720 100 L720 300 Z" fill="currentColor" opacity="0.14"></path>
  <g class="plot-axes" fill="none" stroke="currentColor" stroke-width="2.5">
    <path d="M100 470 H825" marker-end="url(#diagram-arrow)"></path>
    <path d="M100 470 V55" marker-end="url(#diagram-arrow)"></path>
  </g>
  <g class="plot-ticks" stroke="currentColor" stroke-width="2">
    <path d="M250 463 V477 M380 463 V477 M720 463 V477 M93 390 H107 M93 300 H107"></path>
  </g>
  <g class="plot-tick-labels" text-anchor="middle">
    <text x="100" y="502">\(0\)</text><text x="250" y="502">\(p\)</text><text x="380" y="502">\(\ell\)</text><text x="720" y="502">\(r\)</text>
    <text x="78" y="396" text-anchor="end">\(p\)</text><text x="78" y="306" text-anchor="end">\(\ell\)</text>
    <text x="465" y="545" font-size="19">incumbent value \(R\)</text>
    <text x="28" y="245" font-size="19" text-anchor="middle" transform="rotate(-90 28 245)">target receives</text>
  </g>
  <g class="proceeds-no-entry" fill="none" stroke="currentColor" stroke-width="4" stroke-dasharray="3 8" stroke-linecap="round" opacity="0.65">
    <path d="M100 470 H250 M250 390 H720"></path><path d="M250 464 V396" stroke-width="2"></path>
  </g>
  <path class="proceeds-high" d="M100 390 H250 L720 100" fill="none" stroke="currentColor" stroke-width="5"></path>
  <path class="proceeds-low" d="M100 390 H250 L380 300 H720" fill="none" stroke="currentColor" stroke-width="5" stroke-dasharray="12 7"></path>
  <g class="plot-line-labels">
    <text x="405" y="190">high: \(\max\{p,R\}\)</text>
    <text x="500" y="282">low: \(\max\{p,\min(R,\ell)\}\)</text>
    <text x="485" y="423">no entry: \(p\,\mathbf{1}\{R\ge p\}\)</text>
    <text x="590" y="225" font-weight="700">gap \((R-\ell)_+\)</text>
  </g>
  <text class="plot-note" x="100" y="580" font-size="15">Sketch for \(p \lt \ell \lt r\). The challenger lines coincide when \(R\le\ell\).</text>
</g>"""
    return _svg(
        "fig:03_auction-proceeds",
        "proceeds-plot",
        "0 0 850 605",
        "Target proceeds by incumbent value",
        "High-value challenger proceeds are the maximum of the reserve and incumbent value. Low-value challenger proceeds cap at ell. Their shaded difference is the positive part of R minus ell. No-entry proceeds are shown separately.",
        content,
    )


def _registry_display(registry: dict[str, dict[str, str]], key: str) -> str:
    row = registry[key]
    return escape(row.get("display") or row["value"])


def _strength_map(registry: dict[str, dict[str, str]]) -> str:
    keys = ("prim_r0", "rA", "rF_B", "rN", "rJ", "rS_B", "prim_r1", "rC_B", "prim_r2")
    values = {key: _registry_display(registry, key) for key in keys}
    entry = _registry_display(registry, "entry_r1_B")
    content = rf"""
<g class="strength-map" font-family="inherit" fill="currentColor" font-size="16">
  <path class="strength-axis" d="M105 105 H1325" fill="none" stroke="currentColor" stroke-width="2.5" marker-end="url(#diagram-arrow)"></path>
  <text x="1340" y="111">\(r\)</text>
  <g class="strength-ticks" stroke="currentColor" stroke-width="2">
    <path d="M130 96 V114 M275 96 V114 M405 96 V114 M535 96 V114 M665 96 V114 M795 96 V114 M945 96 V114 M1105 96 V114 M1260 96 V114"></path>
  </g>
  <g class="strength-labels" text-anchor="middle" font-size="18">
    <text x="130" y="76">\(r_0\)</text><text x="275" y="76">\(r_A\)</text><text x="405" y="76">\(r_F\)</text><text x="535" y="76">\(r_N\)</text><text x="665" y="76">\(r_J\)</text><text x="795" y="76">\(r_S\)</text><text x="945" y="76">\(r_1\)</text><text x="1105" y="76">\(r_C\)</text><text x="1260" y="76">\(r_2\)</text>
  </g>
  <g class="strength-values registry-values" text-anchor="middle" font-size="14">
    <text x="130" y="141">{values['prim_r0']}</text><text x="275" y="141">{values['rA']}</text><text x="405" y="141">{values['rF_B']}</text><text x="535" y="141">{values['rN']}</text><text x="665" y="141">{values['rJ']}</text><text x="795" y="141">{values['rS_B']}</text><text x="945" y="141">{values['prim_r1']}</text><text x="1105" y="141">{values['rC_B']}</text><text x="1260" y="141">{values['prim_r2']}</text>
  </g>
  <g class="branch-labels" text-anchor="end" font-weight="700">
    <text x="105" y="211">N</text><text x="105" y="291">informative</text><text x="105" y="371">Q</text><text x="105" y="451">coexistence</text><text x="105" y="551">low class</text>
  </g>
  <g class="branch-n" fill="none" stroke="currentColor" stroke-width="7">
    <path d="M130 205 H535"></path><text x="332" y="190" text-anchor="middle" fill="currentColor" stroke="none">no informed trade; entry \(\rho\)</text>
  </g>
  <g class="branch-r" fill="none" stroke="currentColor" stroke-width="7">
    <path d="M275 285 H405" stroke-dasharray="10 7"></path><text x="340" y="267" text-anchor="middle" fill="currentColor" stroke="none">R: mixed purchase recruits</text>
  </g>
  <g class="branch-f" fill="none" stroke="currentColor" stroke-width="7">
    <path d="M405 285 H1105"></path><path class="entry-floor" d="M1105 285 H1260" opacity="0.45"></path>
    <text x="755" y="267" text-anchor="middle" fill="currentColor" stroke="none">F: full purchase; entry {entry} at \(r_1\)</text>
    <text x="1182" y="318" text-anchor="middle" fill="currentColor" stroke="none">F; entry \(\rho\)</text>
  </g>
  <g class="branch-q" fill="none" stroke="currentColor" stroke-width="7" opacity="0.65">
    <path d="M535 365 H665"></path><text x="680" y="371" fill="currentColor" stroke="none">mixed orders; entry \(\rho\)</text>
  </g>
  <g class="branch-coexistence">
    <rect x="275" y="430" width="260" height="34" rx="5" fill="currentColor" opacity="0.12"></rect>
    <text x="405" y="453" text-anchor="middle">\([r_A,r_N]\): N and informative equilibria</text>
  </g>
  <g class="low-class-behavior" fill="none" stroke="currentColor" stroke-width="3">
    <path d="M130 525 V545 H535 V525 M535 545 H795 V525 M795 545 H1260 V525"></path>
    <g fill="currentColor" stroke="none" text-anchor="middle">
      <text x="332" y="580">abstains</text><text x="665" y="580">mixes</text><text x="1028" y="580">sells fully</text>
    </g>
  </g>
  <text class="strength-note" x="130" y="625" font-size="14">Benchmark path at prior \(1/2\), rules IM and C1. Threshold order is shown, not scale.</text>
</g>"""
    return _svg(
        "fig:08-map",
        "strength-map",
        "0 0 1400 650",
        "Equilibrium strength path",
        "As incumbent strength rises, the path shows no informed trade, recruiting mixed purchases, full purchases, mixed orders at the entry floor, coexistence, and low-class abstention, mixing, and full selling.",
        content,
    )


def _svg_text(source: str) -> str:
    replacements = (
        (r"\mathbb{E}", "𝔼"), (r"\mathbf{1}", "1"), (r"\Delta_T", "Δ_T"),
        (r"\kappa", "κ"), (r"\lambda", "λ"), (r"\rho", "ρ"), (r"\tau", "τ"),
        (r"\pi", "π"), (r"\ell", "ℓ"), (r"\mu", "μ"), (r"\gt", ">"),
        (r"\lt", "<"), (r"\ge", "≥"), (r"\le", "≤"), (r"\in", "∈"),
        (r"\mid", "|"), (r"\max", "max"), (r"\min", "min"), (r"\{", "{"),
        (r"\}", "}"), (r"\(", ""), (r"\)", ""), (r"\,", " "), ("\\", ""),
    )
    for command, text in replacements:
        source = source.replace(command, text)
    return source


def render_diagram(label: str, caption_html: str, registry: dict[str, dict[str, str]]) -> str:
    """Render one supported study-guide figure with its trusted HTML caption."""
    if label == "fig:01_brief-chain":
        return _figure(label, "diagram-chain", _svg_text(_brief_chain()), caption_html, "Mechanism.")
    if label == "fig:02_model-timing":
        return _figure(label, "diagram-timing", _svg_text(_model_timing()), caption_html, "Timing.")
    if label == "fig:03_auction-proceeds":
        return _figure(label, "diagram-proceeds", _svg_text(_auction_proceeds()), caption_html, "Target proceeds.")
    if label == "fig:08-map":
        return _figure(label, "diagram-strength", _svg_text(_strength_map(registry)), caption_html, "Strength path.")
    raise ValueError(f"Unknown diagram label: {label}")
