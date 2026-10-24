"""Focused display checks for the handout and the shared chart code. Run after build.py.

    python3 handout/check_display.py

Python and Node standard libraries only. Each block prints PASS or raises. The checks keep the
guarantees of the display rules in handout/README.md:

- source manifest binding, continuation deduplication and finite table values;
- the two published PDFs are the pinned working-paper files, and the Read-the-paper tab states
  their page counts and text date as read from the files;
- every displayed number equals the registry value under the builder's display rule, carries
  its registry key and status, and no unbound decimal sits in the prose;
- status words come from the paper's vocabulary, in spans and in the evidence columns;
- every public anchor of the 2 October 2026 page, legacy anchors included, is still present;
- the page ships only the locked faces (Fira Sans, Fira Mono, the symbol fallback) and makes
  no network request;
- the chart builders and the SVG renderer break lines at unresolved nodes, mark multiplicity
  nodes, keep interval bars, the two shaded uniqueness regions, and closed and open
  endpoints, keep eta = 1 only on the linear panel, and leave the release data unchanged.
"""
from __future__ import annotations

import hashlib
import html
import importlib.util
import json
import re
import subprocess
from pathlib import Path
from unittest.mock import patch

import data
import tables_html

print = __import__("functools").partial(print, flush=True)  # keep the order with the Node block

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
_spec = importlib.util.spec_from_file_location("handout_build", HERE / "build.py")
build = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(build)

VOCABULARY = ("analytical", "computer-assisted", "numerical diagnostic", "open", "input")
PDF_SHA256 = {
    "main_filled.pdf": "d67ae249d7a971383031ecad3e16377e3727b58739f1442bdd53075606cbbfde",
    "online_appendix_filled.pdf": "70f739fdf9dcc676da79d70c8fac1e1ed6bbf249f3fdb16cdf69d921dd3cfcbd",
}
# Anchors that external links use. The legacy anchors are retired section and table names.
LEGACY_ANCHORS = (
    "sec-01-claim", "sec-03-model-ingredients", "sec-03-model-timing", "sec-02-position", "sec-04-two-returns",
    "sec-03-model", "sec-05-results", "sec-05-results-benchmark", "table-2", "sec-appendix", "sec-05-results-prop3",
    "prop-3", "table-certificates", "table-thresholds", "sec-08-statics", "table-1", "table-statics", "table-signs",
    "sec-09-outlook", "sec-07-welfare", "sec-06-robustness", "sec-09-outlook-theory", "sec-09-outlook-empirics",
)
PUBLIC_IDS = (
    "main", "toc", "theme-toggle", "sec-setting", "sec-setting-information", "model-brief", "setting-detail",
    "table-dictionary", "sec-mechanism", "sec-mechanism-payments", "incentive-brief", "sec-mechanism-trading",
    "equilibrium-brief", "chart-fig1", "model-detail", "sec-03-model-values", "sec-03-model-trading",
    "sec-03-model-equilibrium", "sec-03-model-benchmark", "sec-04-two-returns-payoffs", "sec-04-two-returns-prop1",
    "sec-04-two-returns-inference", "sec-04-two-returns-trading", "sec-04-two-returns-explorer", "explorer",
    "sec-evidence", "main-result", "prop-2", "sec-evidence-control", "result-detail", "sec-05-results-prop2",
    "correspondence-detail", "chart-fig2", "benchmark-detail", "sec-implications", "sec-implications-terms",
    "sale-detail", "sec-07-welfare-access", "table-welfare", "sec-07-welfare-bargaining", "chart-fig4",
    "sec-07-welfare-reserve", "table-4", "sec-implications-robustness", "extensions-detail", "sec-06-robustness-noise",
    "chart-fig3", "sec-06-robustness-values", "sec-06-robustness-signals", "table-3", "sec-implications-next",
)

# ------------------------------------------------------------------ source binding and tables
D, _ = data.build_data(ROOT)
D = json.loads(data.emit_js(D))
assert len(D["fig2"]["branches"]["mixed"]["r"]) == 1
assert D["fig2"]["mixed_supports"] and D["fig2"]["unresolved_nodes"]
assert "multiplicity" not in D["fig2"]["regions"]
original = data.read_csv


def duplicate(root, rel):
    rows = original(root, rel)
    if rel == "numerics/correspondence.csv":
        rows.append(next(r for r in rows if r["accepted"] == "true").copy())
    return rows


with patch.object(data, "read_csv", duplicate):
    try:
        data._fig2(ROOT)
        raise AssertionError("accepted duplicate was not rejected")
    except data.DataError as e:
        assert "duplicate" in str(e)
with patch.object(data, "sha256", return_value="changed"):
    try:
        data.build_data(ROOT)
        raise AssertionError("changed source was not rejected")
    except data.DataError as e:
        assert "manifest" in str(e)
for fmt in (tables_html.d6, tables_html.sci):
    for invalid in ("NaN", "Infinity"):
        try:
            fmt(invalid)
            raise AssertionError("nonfinite scalar was not rejected")
        except tables_html.TableError:
            pass
for invalid in ("NaN", "Infinity"):
    try:
        tables_html.three_decimals(tables_html.Decimal(invalid))
        raise AssertionError("nonfinite scalar was not rejected by the reading precision")
    except tables_html.TableError:
        pass
print("PASS source manifest binding, continuation deduplication and finite table values")

# ------------------------------------------------------------------ the published PDFs
page = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
for name, expected in PDF_SHA256.items():
    body = (ROOT / "docs" / name).read_bytes()
    assert hashlib.sha256(body).hexdigest() == expected, f"{name} is not the pinned working-paper file"
    facts = build.pdf_facts(ROOT / "docs" / name)
    assert f'{facts["pages"]} pages' in page and facts["sha256"] in page, f"the paper tab misstates {name}"
main = build.pdf_facts(ROOT / "docs" / "main_filled.pdf")
assert f'Text revision of {main["created"]}' in page and f'Text revised {main["created"]}' in page
print(f"PASS release PDFs are byte-identical; the paper tab states {main['pages']} and "
      f"{build.pdf_facts(ROOT / 'docs' / 'online_appendix_filled.pdf')['pages']} pages and the text date {main['created']}")

# ------------------------------------------------------------------ numbers and status words
registry = {r["name"]: r for r in data.read_csv(ROOT, "numerics/quantity_registry.csv")}
body = page.split("<main", 1)[1]
n = 0
for m in re.finditer(r'<span class="q" data-q="([^"]+)" data-status="([^"]+)" data-precision="([^"]+)" data-value="([^"]*)" title="[^"]*">([^<]*)</span>', page):
    key, status, precision, value, text = m.groups()
    row = registry[key]
    shown, rule = build.shown_value(row)
    assert status == row["status"] and status in VOCABULARY, f"{key}: status {status}"
    assert html.unescape(value) == row["value"], f"{key}: value attribute differs from the registry"
    assert (text, precision) == (shown, rule), f"{key}: shows {text} at {precision}; the rule gives {shown} at {rule}"
    n += 1
assert n == len(re.findall(r'<span class="q"', page)), "a number span lacks its key, status, precision or value"
k = 0
for m in re.finditer(r'<span class="q-math" data-q="([^"]+)" data-shown="([^"]*)" data-status="([^"]*)" title="[^"]*">(.*?)</span>', page, re.S):
    keys, shown, statuses, math = m.group(1).split(), html.unescape(m.group(2)).split("|"), m.group(3).split("|"), m.group(4)
    for key, s, st in zip(keys, shown, statuses, strict=True):
        assert build.shown_value(registry[key])[0] == s and st == registry[key]["status"] and st in VOCABULARY, key
        assert s in html.unescape(math), f"{key}: the formula does not print {s}"
        k += 1
# No result is typed into the prose: outside number spans, mathematics, tables, scripts and the
# build line, no decimal with two or more places may appear.
prose = re.sub(r"<script\b.*?</script>|<style\b.*?</style>|<table\b.*?</table>|<span class=\"q[^\"]*\"[^>]*>.*?</span>"
               r"|\\\(.*?\\\)|\\\[.*?\\\]|<p class=\"build-meta\">.*?</p>|<code>.*?</code>|<pre\b.*?</pre>", " ", body, flags=re.S)
stray = re.findall(r"(?<![\w.])\d+\.\d{2,}(?![\w.])", re.sub(r"<[^>]+>", " ", prose))
assert not stray, f"unbound decimals in the prose: {stray[:8]}"
for m in re.finditer(r'data-status="([^"]+)"', page):
    assert all(s in VOCABULARY for s in m.group(1).split("|")), m.group(1)
for m in re.finditer(r'<td class="basis">([^<]*)</td>', page):
    word = m.group(1).replace(" (not accepted)", "")
    assert word in VOCABULARY or word in ("yes", "no"), f"evidence column prints {word!r}"
print(f"PASS {n} number spans and {k} numbers in formulas equal the registry under the display rule; "
      "status words are in the paper's vocabulary; no decimal is typed into the prose")

# ------------------------------------------------------------------ anchors, faces, network
for i in LEGACY_ANCHORS:
    assert re.search(rf'<span id="{i}" class="legacy-anchor"', page), f"legacy anchor {i} is missing"
for i in PUBLIC_IDS:
    assert f'id="{i}"' in page, f"public id {i} is missing"
families = set(re.findall(r'@font-face \{ font-family: "([^"]+)"', page))
assert families == {"Fira Sans", "Fira Mono", "CCC Symbols"}, families
assert not re.search(r'<(?:script|link|img|iframe)\b[^>]*(?:src|href)="(?:https?:)?//', page), "a network request"
print(f"PASS {len(LEGACY_ANCHORS)} legacy anchors and {len(PUBLIC_IDS)} public ids present; "
      "only Fira Sans, Fira Mono and the symbol fallback; no network request")

# ------------------------------------------------------------------ charts: builders and renderer
script = r'''
const fs=require('node:fs'), vm=require('node:vm'), assert=require('node:assert/strict');
const D=JSON.parse(fs.readFileSync(0,'utf8'));
const context={window:{addEventListener(){}}, document:{addEventListener(){}}, getComputedStyle(){return {getPropertyValue(){return ''}}}, URLSearchParams, console};
vm.createContext(context);
for(const file of ['charts.js','explorer.js']) vm.runInContext(fs.readFileSync('handout/'+file,'utf8'),context);
const C=context.window.CCC, t=C.charts.tokens(), before=JSON.stringify(D);
const runs=(xs)=>{let r=0,open=false;for(const x of xs){if(x===null){open=false;}else if(!open){r++;open=true;}}return r;};
const subpaths=(svg,i)=>{const g=new RegExp('<g class="trace" data-trace="'+i+'">(.*?)</g>').exec(svg);if(!g)return -1;const p=/<path class="tr-line" d="([^"]*)"/.exec(g[1]);return p?(p[1].match(/M/g)||[]).length:0;};
// broken series: duplicate and missing nodes break the line
const b=C.charts.brokenSeries([1,2,2,3],[.1,.2,.3,.4],10,10,[1,2,3]);
for(const i of [1,2]){const j=b.idx.indexOf(i);assert.equal(b.idx[j-1],null);assert.equal(b.idx[j+1],null)}
assert.equal(C.charts.brokenSeries([1,3],[.1,.2],10,10,[1,2,3]).x[1],null);
// Figure 2: spec
const f2=C.charts.builders.fig2(D,t,{narrow:false});
assert.equal(f2.traces.find(x=>x.name==='preparation ceiling').marker.symbol.join(','),'circle,circle-open');
assert.equal(f2.layout.shapes.filter(x=>x.type==='rect').length,2);
const ticks=f2.layout.shapes.filter(x=>x.type==='line' && x.y1===.025).length;
assert.equal(ticks,D.fig2.multiplicity_nodes.length*2);
const certs=D.fig2.certificates.filter(c=>c.accepted==='true').length;
assert.ok(certs>0 && f2.traces.filter(x=>x.error_y).length===2);
assert.equal(f2.traces.find(x=>x.name==='mixed diagnostic').marker.symbol,'diamond-open');
// Figure 2: rendered
const s2=C.charts.svgMarkup(f2,t,900).svg;
assert.equal((s2.match(/<rect class="shape-rect"/g)||[]).length,2,'two shaded uniqueness regions');
assert.equal((s2.match(/class="err-bar"/g)||[]).length,2*certs,'interval bars on every certified point');
assert.ok(/mk-circle-open/.test(s2)&&/mk-circle"/.test(s2),'closed and open ceiling markers');
assert.ok(/mk-diamond-open/.test(s2)&&/mk-diamond"/.test(s2),'certified and mixed diamonds');
const lineShapes=(s2.match(/<line class="shape-line"/g)||[]).length;
assert.ok(lineShapes>=ticks,'multiplicity ticks drawn');
let broken=0;
f2.traces.forEach((tr,i)=>{if(!/lines/.test(tr.mode))return;const want=runs(tr.x.map((x,j)=>x===null||tr.y[j]===null?null:x));const got=subpaths(s2,i);assert.equal(got,want,'trace '+tr.name+' keeps its breaks');if(want>1)broken++;});
assert.ok(broken>0,'some branch is broken at unresolved nodes');
// Figure 3: closed endpoints in both panels, for both laws
const f3=C.charts.builders.fig3(D,t,{narrow:true});
for(const trace of f3.traces.filter(x=>/plateau|zero tail/.test(x.name))) assert.equal(trace.marker.symbol,'circle');
const s3=C.charts.svgMarkup(f3,t,700).svg;
assert.equal((s3.match(/mk-circle"/g)||[]).length,4); assert.ok(!/mk-circle-open/.test(s3));
// Figure 4: eta = 1 only on the linear panel; the log panel has positive values only
const f4=C.charts.builders.fig4(D,t,{narrow:false});
for(const trace of f4.traces){ if(trace.xaxis==='x') assert.equal(trace.x.at(-1),1); else { assert.ok(trace.x.every(x=>x<1)); assert.ok(trace.y.every(y=>y>0)); } }
assert.equal(f4.layout.yaxis2.type,'log');
C.charts.svgMarkup(f4,t,900); C.charts.svgMarkup(C.charts.builders.fig1(D,t,{narrow:true}),t,400);
// the explorer's closed forms keep the tie rule at the ceiling
const P=Object.fromEntries(Object.entries(D.inputs).map(([k,v])=>[k,Number(v)])), cf=C.explorer.closedForms(P,3);
assert.ok(C.explorer.closedForms({...P,c_H:cf.B_M},3).E>P.rho);
assert.equal(C.explorer.closedForms({...P,c_H:cf.B_M+1e-10},3).E,P.rho);
assert.equal(C.explorer.closedForms({...P,c_H:cf.B_m},3).E,1);
const partial=C.explorer.closedForms({...P,c_H:(cf.B_m+cf.B_prior)/2},3);
assert.ok(partial.E<1 && partial.E>P.rho);
assert.equal(JSON.stringify(D),before,'builders or renderer mutated release data');
console.log('PASS charts: breaks at unresolved nodes ('+broken+' broken branches), '+ticks+' multiplicity ticks, '+(2*certs)+' interval bars, two shaded regions, closed and open endpoints, eta = 1 on the linear panel only, release data unchanged');
'''
subprocess.run(["node", "-e", script], input=json.dumps(D), text=True, cwd=ROOT, check=True)
