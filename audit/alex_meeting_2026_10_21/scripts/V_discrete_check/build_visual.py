"""Print a self-contained viewer of the equal-noise calculation."""
import json
from pathlib import Path

p=Path(__file__).parent
data=[]
for line in (p/'equal_sweep.jsonl').open():
    v=json.loads(line)
    if v.get('kind')!='config':continue
    z=v['params'];menus={}
    for m in v['menus']:
        row=next(x for x in m['grid'] if abs(x['k']-.02)<1e-10)
        menus[m['menu']]=[[round(e['E'],10),round(e['O_H'],10),e['self_pool'],e['a'],e['b']]
                          for e in row['equilibria'] if e['strict']]
    data.append([z['c_L'],z['lam'],z['r'],menus])

html='''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Discrete equilibrium calculations</title><link rel="icon" href="data:,">
<style>
body{font:14px var(--font-sans,system-ui);color:var(--foreground,#222);margin:0;background:transparent}
.controls{display:flex;gap:18px;flex-wrap:wrap;align-items:end;margin:0 0 14px}
label{display:grid;gap:5px;font-size:12px;color:var(--muted-foreground,#666)}
select{font:inherit;color:var(--foreground,#222);background:var(--background,white);border:1px solid var(--border,#bbb);border-radius:5px;padding:6px 10px}
.note{color:var(--muted-foreground,#666);font-size:12px;line-height:1.5;margin:9px 0}
.legend{display:flex;gap:18px;flex-wrap:wrap;font-size:12px;margin:8px 0}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:5px}
svg{display:block;width:100%;height:290px;overflow:visible}
table{border-collapse:collapse;width:100%;font-size:13px}th,td{text-align:left;padding:8px 6px;border-bottom:1px solid var(--border,#ddd)}
th{font-weight:600;color:var(--muted-foreground,#555)}td:first-child,th:first-child{padding-left:0}
.slider{display:flex;align-items:center;gap:10px;margin:12px 0}.slider input{flex:1;min-width:0;width:0;accent-color:#16867a}.slider strong{white-space:nowrap;flex-shrink:0}
</style></head><body>
<div class="controls"><label>Investor presence<select id="lam"><option value="0.8">λ = 0.8</option><option value="1">λ = 1</option><option value="0.5">λ = 0.5</option><option value="0.7">λ = 0.7</option><option value="0.9">λ = 0.9</option></select></label>
<label>Low preparation cost<select id="cl"><option value="1">cL = 1 · original</option><option value="0.02">cL = 0.02 · entry floor</option></select></label>
<span class="note">Equal noise · k = 0.02 · prescribed investor tie rule</span></div>
<div class="legend"><span><i class="dot" style="background:#377fc2"></i>Buy only</span><span><i class="dot" style="background:#c08627"></i>Sell only</span><span><i class="dot" style="background:#148574"></i>Two sided</span><span>Hollow point: extra zero-entry pool</span></div>
<svg id="chart" viewBox="0 0 680 290" role="img" aria-label="Entry probability across incumbent strengths"></svg>
<div class="slider"><label for="r">Selected strength</label><input id="r" type="range" min="1.05" max="9.95" step="0.05" value="3"><strong id="rv">r = 3.00</strong></div>
<table><thead><tr><th>Menu / price schedule</th><th>Entry</th><th>High-value ownership</th></tr></thead><tbody id="rows"></tbody></table>
<p class="note">Every dot is a strict equilibrium outcome on the strength grid. Distinct dots at one strength are separate equilibria. High-value ownership means ownership by the high-value challenger.</p>
<script>
const data=DATA;const colors={M1:'#377fc2',M2:'#c08627',M3:'#148574'};
const names={M1:'Buy only',M2:'Sell only',M3:'Two sided'};const chart=document.getElementById('chart');
function draw(){let rows=data.filter(x=>x[0]===+cl.value&&x[1]===+lam.value).sort((a,b)=>a[2]-b[2]);
const W=Math.max(320,chart.clientWidth);chart.setAttribute('viewBox',`0 0 ${W} 290`);
const x=v=>48+(v-1)/9*(W-68),y=v=>250-v/.65*226;
let svg='';for(let t=0;t<=.6+.001;t+=.1){svg+=`<line x1="48" y1="${y(t)}" x2="${W-20}" y2="${y(t)}" stroke="currentColor" opacity=".12"/><text x="39" y="${y(t)+4}" text-anchor="end" font-size="11" fill="currentColor">${t.toFixed(1)}</text>`;}
for(let t=1;t<=10;t++){svg+=`<text x="${x(t)}" y="271" text-anchor="middle" font-size="11" fill="currentColor">${t}</text>`;}
svg+=`<text x="48" y="13" font-size="12" fill="currentColor">Entry probability</text><text x="${W-20}" y="289" text-anchor="end" font-size="11" fill="currentColor">Incumbent strength r</text>`;
svg+=`<line x1="${x(+r.value)}" y1="21" x2="${x(+r.value)}" y2="250" stroke="currentColor" opacity=".35" stroke-dasharray="3 3"/>`;
for(const row of rows){for(const [menu,eqs] of Object.entries(row[3])){for(const eq of eqs){svg+=`<circle cx="${x(row[2])}" cy="${y(eq[0])}" r="${eq[2]?3:1.8}" fill="${eq[2]?'var(--background,white)':colors[menu]}" stroke="${colors[menu]}" stroke-width="${eq[2]?1.4:0}" opacity=".85"/>`;}}}
chart.innerHTML=svg;const selected=rows.reduce((a,b)=>Math.abs(a[2]-r.value)<Math.abs(b[2]-r.value)?a:b);
document.getElementById('rv').textContent='r = '+selected[2].toFixed(2);
document.getElementById('rows').innerHTML=Object.entries(selected[3]).flatMap(([m,eqs])=>eqs.map(e=>`<tr><td style="color:${colors[m]}">${names[m]}${e[2]?' · extra pool':''}</td><td>${e[0].toFixed(6)}</td><td>${e[1].toFixed(6)}</td></tr>`)).join('');
}
['cl','lam','r'].forEach(id=>document.getElementById(id).addEventListener('input',draw));window.addEventListener('resize',draw);draw();
</script></body></html>'''
print(html.replace('DATA',json.dumps(data,separators=(',',':'))))
