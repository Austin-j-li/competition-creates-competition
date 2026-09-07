"""Focused presentation regressions. Run after build.py; requires Python stdlib and Node."""
from pathlib import Path
from unittest.mock import patch
import hashlib
import json
import subprocess
import data
import tables_html

ROOT = Path(__file__).resolve().parents[1]
D, _ = data.build_data(ROOT)
D = json.loads(data.emit_js(D))
assert len(D['fig2']['branches']['mixed']['r']) == 1
assert D['fig2']['mixed_supports'] and D['fig2']['unresolved_nodes']
assert 'multiplicity' not in D['fig2']['regions']
original = data.read_csv

def duplicate(root, rel):
    rows = original(root, rel)
    if rel == 'numerics/correspondence.csv':
        rows.append(next(r for r in rows if r['accepted'] == 'true').copy())
    return rows

with patch.object(data, 'read_csv', duplicate):
    try:
        data._fig2(ROOT)
        raise AssertionError('accepted duplicate was not rejected')
    except data.DataError as e:
        assert 'duplicate' in str(e)
with patch.object(data, 'sha256', return_value='changed'):
    try:
        data.build_data(ROOT)
        raise AssertionError('changed source was not rejected')
    except data.DataError as e:
        assert 'manifest' in str(e)
for fmt in (tables_html.d6, tables_html.sci):
    for invalid in ('NaN', 'Infinity'):
        try:
            fmt(invalid)
            raise AssertionError('nonfinite scalar was not rejected')
        except tables_html.TableError:
            pass
for name, expected in {
    'main_filled.pdf': 'e912d0db3746763d0d1c8e28003ea548609379970786a15081e25891a952eceb',
    'online_appendix_filled.pdf': '4567b920b2f9a9fe88d846812e7f3da88db78907e961e02e1f80dc08f4da832b',
}.items():
    assert hashlib.sha256((ROOT / 'docs' / name).read_bytes()).hexdigest() == expected

script = r'''
const fs=require('node:fs'), vm=require('node:vm'), assert=require('node:assert/strict');
const D=JSON.parse(fs.readFileSync(0,'utf8'));
const context={window:{addEventListener(){}}, document:{addEventListener(){}}, getComputedStyle(){return {getPropertyValue(){return ''}}}, URLSearchParams, console};
vm.createContext(context);
for(const file of ['charts.js','explorer.js']) vm.runInContext(fs.readFileSync('handout/'+file,'utf8'),context);
const C=context.window.CCC, t=C.charts.tokens(), before=JSON.stringify(D);
const b=C.charts.brokenSeries([1,2,2,3],[.1,.2,.3,.4],10,10,[1,2,3]);
for(const i of [1,2]){const j=b.idx.indexOf(i);assert.equal(b.idx[j-1],null);assert.equal(b.idx[j+1],null)}
assert.equal(C.charts.brokenSeries([1,3],[.1,.2],10,10,[1,2,3]).x[1],null);
const f2=C.charts.builders.fig2(D,t,{narrow:false});
assert.equal(f2.traces.find(x=>x.name==='preparation ceiling').marker.symbol.join(','),'circle,circle-open');
assert.equal(f2.layout.shapes.filter(x=>x.type==='rect').length,2);
assert.equal(f2.layout.shapes.filter(x=>x.type==='line' && x.y1===.025).length,D.fig2.multiplicity_nodes.length*2);
const f3=C.charts.builders.fig3(D,t,{narrow:true});
for(const trace of f3.traces.filter(x=>x.name==='logistic, zero tail at bound')) assert.equal(trace.marker.symbol,'circle');
const f4=C.charts.builders.fig4(D,t,{narrow:false});
for(const trace of f4.traces) {
 if(trace.xaxis==='x') assert.equal(trace.x.at(-1),1);
 else { assert.ok(trace.x.every(x=>x<1)); assert.ok(trace.y.every(y=>y>0)); }
}
const P=Object.fromEntries(Object.entries(D.inputs).map(([k,v])=>[k,Number(v)])), cf=C.explorer.closedForms(P,3);
assert.ok(C.explorer.closedForms({...P,c_H:cf.B_M},3).E>P.rho);
assert.equal(C.explorer.closedForms({...P,c_H:cf.B_M+1e-10},3).E,P.rho);
assert.equal(C.explorer.closedForms({...P,c_H:cf.B_m},3).E,1);
const partial=C.explorer.closedForms({...P,c_H:(cf.B_m+cf.B_prior)/2},3);
assert.ok(partial.E<1 && partial.E>P.rho);
assert.equal(JSON.stringify(D),before,'builders mutated release data');
console.log('PASS scientific display: branch identity, gaps, multiplicity nodes, endpoints, entry ties and immutable chart data');
'''
subprocess.run(['node', '-e', script], input=json.dumps(D), text=True, cwd=ROOT, check=True)
print('PASS source manifest binding, finite table values and byte-identical release PDFs')
