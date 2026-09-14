/* Presentation engine for "Competition Creates Competition".
 *
 * Reads window.CCC_DATA (registry, tables, fig1..fig4) and
 * window.CCC.explorer.closedForms for arithmetic on the declared primitives.
 * It never solves for an equilibrium and never rounds a certified interval inward.
 * Slides arrive as records from window.createSlides(H); see presentation/REDESIGN_SPEC.md.
 */
(function(){
'use strict';

/* ---------- data and formatting ---------- */
const D=window.CCC_DATA;
const P=Object.fromEntries(Object.entries(D.inputs).map(([k,x])=>[k,Number(x)]));
const $=(s,root)=>(root||document).querySelector(s);
const $$=(s,root)=>[...(root||document).querySelectorAll(s)];
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const m=(latex,cls='')=>`<div class="equation ${cls}" data-latex="${esc(latex)}"></div>`;
const mi=latex=>`<span class="math-inline" data-inline="true" data-latex="${esc(latex)}"></span>`;
const reg=k=>{if(!D.registry[k])throw Error('Missing registry key: '+k);return D.registry[k];};
const v=k=>esc(reg(k).display.replace(/\\%/g,'%'));
const val=k=>Number(reg(k).value);
const pct=k=>(100*val(k)).toFixed(1)+'%';
const fmt=(k,n=3)=>val(k).toFixed(n);
const pc=(n,d=1)=>(100*Number(n)).toFixed(d)+'%';
const num=(n,d=3)=>Number(n).toFixed(d);
const cf=r=>window.CCC.explorer.closedForms(P,Number(r));
const eqRow=(r,experiment='feedback')=>{const rows=D.tables.equilibrium_controls.filter(x=>x.parameter_set==='base'&&x.noise==='Laplace'&&x.cost_law==='atoms'&&x.accepted==='true'&&Number(x.r)===Number(r)&&x.experiment===experiment);if(rows.length!==1)throw Error('Ambiguous benchmark row');return rows[0];};
/* Outward rounding of a decimal string: never narrows a certified interval. */
function outward(s,up,digits=8){const negative=String(s).trim().startsWith('-');const [whole,dec='']=String(s).replace('-','').split('.');const head=(dec+'0'.repeat(digits)).slice(0,digits);const rest=dec.slice(digits);const unit=BigInt('1'+'0'.repeat(digits));let n=BigInt(whole)*unit+BigInt(head||'0');const away=negative?!up:up;if(away&&/[1-9]/.test(rest))n++;const body=`${n/unit}.${String(n%unit).padStart(digits,'0')}`;return negative?'-'+body:body;}

const errors=[];
window.addEventListener('error',e=>errors.push(e.message));
window.addEventListener('unhandledrejection',e=>errors.push(String(e.reason)));

/* ---------- slides ---------- */
const H={m,mi,v,pct,fmt,link:()=>''};
const slides=window.createSlides(H);
const main=slides.filter(s=>!s.backup);
const ACTS=['question','preview','model','equilibrium','results','next'];
const DETAIL={s10:'b6',s12:'b1',s13:'b2',s15:'b1',s19:'b3',s21:'b4',s22:'b7'};
const stampWord=status=>status==='input'?'declaration':status;
const near=(e,sel)=>e&&e.target&&e.target.closest?e.target.closest(sel):null;
const plain=t=>String(t==null?'':t).replace(/<[^>]*>/g,'').replace(/&[a-z]+;/gi,' ').replace(/\s+/g,' ').trim();

function slideHTML(s,i){
  const heading=plain(s.title)||'Competition creates competition';
  const head=[s.kicker?`<p class="kicker">${s.kicker}</p>`:'',s.title?`<h2>${s.title}</h2>`:'',s.subtitle?`<p class="sub">${s.subtitle}</p>`:''].join('');
  const foot=[s.status?`<span class="stamp" data-status="${esc(s.status)}">${esc(stampWord(s.status))}</span>`:'',
    `<span class="source">${esc(s.source||'')}</span>`,
    DETAIL[s.id]?`<button class="detail" data-goto="${DETAIL[s.id]}">Technical detail</button>`:''].join('');
  return `<section class="slide" id="${esc(s.id)}" data-act="${esc(s.act||'')}" data-widget="${esc(s.widget||'')}" data-status="${esc(s.status||'')}" aria-label="${esc((i+1)+'. '+heading)}" aria-hidden="true" inert>`+
    `<header class="slide-head">${head}</header>`+
    `<div class="slide-body">${s.body||''}</div>`+
    `<footer class="slide-foot">${foot}</footer></section>`;
}
$('#deck').innerHTML=slides.map(slideHTML).join('');
$('#acts').innerHTML=ACTS.map(a=>`<li data-act="${a}" style="--p:0">${a}</li>`).join('');

function math(root=document){root.querySelectorAll('[data-latex]').forEach(el=>{try{if(!window.katex)throw Error('Equation renderer unavailable');katex.render(el.dataset.latex,el,{displayMode:!el.dataset.inline,throwOnError:true,trust:false});}catch(e){errors.push(e.message);el.textContent='Equation unavailable. See the accompanying paper.';el.classList.add('math-error');}});}
math();

/* ---------- glossary: one source, three surfaces ----------
 * The definition strips, the notation panel and the b6 widget all read
 * window.createGlossary. Nothing here invents an entry or drops one.
 */
const GROUPS=['values','preparation','trading','prices','derived','outcomes','institutions'];
let glossary=[];
try{
  if(typeof window.createGlossary!=='function')throw Error('Glossary source unavailable: content.js exports no createGlossary');
  glossary=window.createGlossary(H)||[];
}catch(e){errors.push(e.message);}
const GLOSS=new Map(glossary.map(e=>[e.key,e]));
const introducedBy=new Map();
slides.forEach((s,i)=>{(s.defines||[]).forEach(k=>{if(!introducedBy.has(k))introducedBy.set(k,i);});});
function introduced(key){
  const i=introducedBy.get(key);
  if(i===undefined)return '—';
  return slides[i].backup?'B'+(i-main.length+1):String(i+1).padStart(2,'0');
}
function glossaryRow(e){return `<tr><td>${mi(e.latex)}</td><td>${esc(e.meaning)}</td><td>${esc(introduced(e.key))}</td></tr>`;}
function glossaryHTML(tableClass){
  const placed=new Set();
  let rows='';
  GROUPS.forEach(group=>{
    const entries=glossary.filter(e=>e.group===group);
    if(!entries.length)return;
    entries.forEach(e=>placed.add(e.key));
    rows+=`<tr class="group"><td colspan="3">${esc(group)}</td></tr>`+entries.map(glossaryRow).join('');
  });
  /* An entry with an unrecognised group is shown, never silently dropped. */
  const rest=glossary.filter(e=>!placed.has(e.key));
  if(rest.length){
    errors.push('Glossary entries outside the declared groups: '+rest.map(e=>e.key+' ('+e.group+')').join(', '));
    rows+=`<tr class="group"><td colspan="3">ungrouped</td></tr>`+rest.map(glossaryRow).join('');
  }
  return `<table class="data-table ${esc(tableClass)}"><thead><tr><th>Symbol</th><th>Meaning</th><th>Introduced</th></tr></thead><tbody>${rows}</tbody></table>`;
}
function defsKeys(el){return String(el.dataset.defs||'').split(',').map(k=>k.trim()).filter(Boolean);}
function fillDefs(){
  $$('.defs[data-defs]').forEach(el=>{
    const items=defsKeys(el).map(key=>{
      const e=GLOSS.get(key);
      if(!e){errors.push('Definition strip refers to an undefined symbol: '+key);return '';}
      return `<div><dt>${mi(e.latex)}</dt><dd>${esc(e.meaning)}</dd></div>`;
    }).join('');
    el.innerHTML=`<dl>${items}</dl>`;
    math(el);
  });
}
function undefinedDefs(){return [...new Set($$('.defs[data-defs]').flatMap(defsKeys).filter(k=>!GLOSS.has(k)))];}
fillDefs();

/* ---------- interaction state ---------- */
let index=0, step=0, returnTo=null, stageScale=1;
const steps=new Map();
const state={quality:'H',auctionR:0.8,dialR:P.r_weak,tapeX:-1.5,benchmark:'weak',compare:false,experiment:'feedback',eta:0.25};
const motion=matchMedia('(prefers-reduced-motion:reduce)');
const printing=()=>document.documentElement.dataset.printing==='true';
const still=()=>motion.matches||printing();
const storage={get(k){try{return localStorage.getItem(k);}catch{return null;}},set(k,x){try{localStorage.setItem(k,x);}catch{}}};

/* ---------- stage geometry ---------- */
function scaleStage(){
  if(printing()){$('#stage').style.setProperty('--stage-scale','1');return;}
  stageScale=Math.max(0.05,Math.min(innerWidth/1600,(innerHeight-56)/900));
  $('#stage').style.setProperty('--stage-scale',String(stageScale));
}
addEventListener('resize',scaleStage);
addEventListener('load',scaleStage);
document.addEventListener('fullscreenchange',scaleStage);
scaleStage();

/* ---------- navigation ---------- */
function maxStep(i=index){return Math.max(0,...$$(`#${slides[i].id} [data-step]`).map(e=>Number(e.dataset.step)));}
function counterText(){return slides[index].backup
  ?`B${index-main.length+1} / ${slides.length-main.length}`
  :`${String(index+1).padStart(2,'0')} / ${main.length}`;}
function progressText(){
  if(maxStep())return `Reveal ${step+1} of ${maxStep()+1}`;
  if(slides[index].backup)return 'Technical discussion';
  return `${slides[index].minutes} min`;
}
function updateRail(){
  const current=slides[index], backup=!!current.backup;
  $$('#acts li').forEach(li=>{
    const act=li.dataset.act, inAct=main.filter(s=>s.act===act);
    let p=0;
    if(!backup){
      const position=inAct.findIndex(s=>s.id===current.id);
      if(position>=0)p=inAct.length?(position+1)/inAct.length:0;
      else p=ACTS.indexOf(act)<ACTS.indexOf(current.act)?1:0;
    }
    li.style.setProperty('--p',String(p));
    if(!backup&&act===current.act)li.setAttribute('data-current','');else li.removeAttribute('data-current');
  });
  $('#acts').dataset.label=backup?'Technical discussion':'';
}
function updateReveals(){
  const slide=slides[index], node=$('#'+slide.id);
  node.querySelectorAll('[data-step]').forEach(el=>{
    const shown=Number(el.dataset.step)<=step;
    el.classList.toggle('shown',shown);
    el.setAttribute('aria-hidden',String(!shown));
    el.inert=!shown;
  });
  steps.set(index,step);
  const widget=W[slide.widget];
  if(widget&&typeof widget.onStep==='function')widget.onStep(maxStep()?step:Number.MAX_SAFE_INTEGER);
  $('#counter').textContent=counterText();
  $('#progress-label').textContent=progressText();
  $('#previous').disabled=index===0&&step===0;
  $('#next').disabled=(index===main.length-1||index===slides.length-1)&&step===maxStep();
}
function go(id,opts={}){
  const i=typeof id==='number'?id:slides.findIndex(s=>s.id===id);
  if(i<0||i>=slides.length)return;
  const previous=index;
  if(slides[i].backup&&!slides[previous].backup&&!opts.history)returnTo={index:previous,step};
  index=i;
  step=Math.max(0,Math.min(maxStep(i),opts.step??steps.get(i)??0));
  $$('.slide').forEach((el,j)=>{const active=j===i;el.classList.toggle('active',active);el.setAttribute('aria-hidden',String(!active));el.inert=!active;});
  $('#'+slides[i].id).scrollTop=0;
  $('#return').hidden=!slides[i].backup;
  updateRail();
  updateReveals();
  if(!opts.history&&slides[i].id!==location.hash.slice(1))history.pushState({slide:i,step},'',`#${slides[i].id}`);
  $('#announcer').textContent=`${plain(slides[i].title)||'Competition creates competition'}, ${i+1} of ${slides.length}`;
  $('#stage').focus({preventScroll:true});
}
function next(){if(step<maxStep()){step++;updateReveals();return;}if(index===main.length-1||index===slides.length-1)return;go(index+1,{step:0});}
function previous(){if(step>0){step--;updateReveals();return;}if(index>0)go(index-1,{step:maxStep(index-1)});}
function returnTalk(){if(returnTo){const target=returnTo;returnTo=null;go(target.index,{step:target.step});}else go(main[main.length-1].id);}
$('#previous').onclick=previous;$('#next').onclick=next;$('#return').onclick=returnTalk;
window.addEventListener('popstate',()=>{const id=location.hash.slice(1);go(slides.some(s=>s.id===id)?id:0,{history:true});});
document.addEventListener('click',e=>{const b=near(e,'[data-goto]');if(b){if($('#panel').open)$('#panel').close();go(b.dataset.goto);}});

/* ---------- chrome ---------- */
function theme(value){
  const doc=document.documentElement;
  if(value==='light')doc.dataset.theme='light';else delete doc.dataset.theme;
  $('#theme').textContent=value==='light'?'After hours':'Projector';
  $('#theme').setAttribute('aria-pressed',String(value==='light'));
  storage.set('ccc-deck-theme',value);
}
theme(storage.get('ccc-deck-theme')==='light'?'light':'dark');
$('#theme').onclick=()=>theme(document.documentElement.dataset.theme==='light'?'dark':'light');

let hudTimer=null;
function showHud(hold){
  document.body.classList.add('hud-visible');
  clearTimeout(hudTimer);
  if(!hold)hudTimer=setTimeout(()=>document.body.classList.remove('hud-visible'),2500);
}
document.addEventListener('mousemove',()=>showHud(false));
document.addEventListener('focusin',e=>showHud(!!near(e,'.hud')));
document.addEventListener('focusout',e=>{if(near(e,'.hud'))showHud(false);});
showHud(false);

function motionUpdate(){document.body.classList.toggle('motion',!motion.matches);}
motion.addEventListener('change',()=>{motionUpdate();renderAll();});
motionUpdate();

async function fullscreen(){try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen();}catch{showPanel('Fullscreen','<p>Use your browser’s fullscreen control to present.</p>');}}
$('#fullscreen').onclick=fullscreen;
document.addEventListener('fullscreenchange',()=>{$('#fullscreen').textContent=document.fullscreenElement?'Exit fullscreen':'Fullscreen';});

function showPanel(title,html){$('#panel-title').textContent=title;$('#panel-body').innerHTML=html;$('#panel').showModal();}
$('#close-panel').onclick=()=>$('#panel').close();
$('#panel').addEventListener('click',e=>{if(e.target===$('#panel'))$('#panel').close();});
function overview(){
  showPanel('The talk',`<p class="small muted">${main.length} slides / ${main.reduce((n,s)=>n+s.minutes,0)} minutes. Technical discussion slides follow the conclusion.</p><div class="overview-grid">${slides.map((s,i)=>`<button data-goto="${s.id}"><small>${s.backup?'BACKUP '+(i-main.length+1):String(i+1).padStart(2,'0')+' / '+s.minutes+' MIN'}</small>${esc(plain(s.title)||'Competition creates competition')}</button>`).join('')}</div>`);
}
function notes(){
  const elapsed=main.slice(0,Math.min(index,main.length)).reduce((n,s)=>n+s.minutes,0);
  const slide=slides[index];
  showPanel('Speaker notes',`<p class="note-time">${slide.backup?'Technical discussion':`${elapsed}-${elapsed+slide.minutes} minutes`}</p><h3>${esc(plain(slide.title)||'Competition creates competition')}</h3><div class="notes-pane">${esc(slide.notes||'')}</div><p class="small muted">${esc(slide.source||'')}</p><div class="notes-actions"><button id="download-notes">Save all notes</button><button id="print-deck">Print deck</button></div>`);
  $('#download-notes').onclick=downloadNotes;
  $('#print-deck').onclick=()=>{$('#panel').close();window.print();};
}
function notesText(){return slides.map((s,i)=>`## ${s.backup?'Backup '+(i-main.length+1):i+1}. ${plain(s.title)||'Competition creates competition'}\n\n${s.minutes?s.minutes+' minutes.\n\n':''}${s.notes||''}\n\nSource: ${s.source||''}\n`).join('\n');}
function downloadNotes(){
  const body='# Competition Creates Competition\n\n'+main.reduce((n,s)=>n+s.minutes,0)+'-minute presentation by Austin Li.\n\n'+notesText();
  const url=URL.createObjectURL(new Blob([body],{type:'text/markdown'}));
  const a=document.createElement('a');a.href=url;a.download='speaker-notes.md';a.click();
  setTimeout(()=>URL.revokeObjectURL(url),1000);
}
function notation(){showPanel('Notation',glossaryHTML('glossary'));math($('#panel-body'));}
function help(){showPanel('Presentation controls','<div class="help-grid"><kbd>→ / Space</kbd><span>Reveal the next point, then advance</span><kbd>←</kbd><span>Undo a reveal, then go back</span><kbd>O</kbd><span>Open the slide overview</span><kbd>N</kbd><span>Read the current speaker notes</span><kbd>G</kbd><span>Open the notation glossary</span><kbd>F</kbd><span>Toggle fullscreen</span><kbd>T</kbd><span>Switch the projector theme</span><kbd>R</kbd><span>Reset the current interaction and reveals</span><kbd>Esc</kbd><span>Close a panel or return from a technical detour</span><kbd>Home / End</kbd><span>Go to the title or conclusion</span></div><p class="small muted">Use Tab to reach controls. Arrow keys adjust a focused slider. All assets and linked papers work offline.</p>');}
$('#overview').onclick=overview;$('#notes').onclick=notes;$('#help').onclick=help;
if($('#glossary'))$('#glossary').onclick=notation;
document.addEventListener('keydown',e=>{
  if($('#panel').open){if(e.key==='Escape')return;return;}
  if(e.target&&e.target.matches&&(e.target.matches('input,select,textarea')||e.target.isContentEditable))return;
  if(near(e,'button,a')&&[' ','Enter'].includes(e.key))return;
  const actions={'ArrowRight':next,'PageDown':next,' ':next,'ArrowLeft':previous,'PageUp':previous,
    'Home':()=>go(main[0].id,{step:0}),'End':()=>go(main[main.length-1].id,{step:0}),
    'o':overview,'n':notes,'g':notation,'f':fullscreen,'t':()=>$('#theme').click(),'r':resetCurrent,
    'Escape':()=>{if(slides[index].backup)returnTalk();}};
  if(actions[e.key]){e.preventDefault();actions[e.key]();}
});

/* ---------- drawing helpers ----------
 * Every shape carries its spec class and a presentation-attribute default, so the
 * figure reads correctly before deck.css styles it and deck.css always wins.
 */
const AXIS='stroke="var(--l)" stroke-width="1.4" fill="none"';
const GRID='stroke="var(--l)" stroke-width="1" fill="none" opacity="0.55"';
const TICKA='fill="var(--m)" font-size="15"';
const LABELA='fill="var(--t2)" font-size="16"';
const CURVEA='fill="none" stroke="var(--a)" stroke-width="2.6" stroke-linejoin="round"';
const CURVEB='fill="none" stroke="var(--ghost)" stroke-width="2.2" stroke-linejoin="round"';
const MARKEDA='stroke="var(--m)" stroke-width="1.2" stroke-dasharray="7 6" fill="none"';
const POINTA='fill="var(--a)"';
const NODEA='fill="var(--a)" stroke="var(--g)" stroke-width="2"';
const CERTA='stroke="var(--a2)" stroke-width="4" fill="none" stroke-linecap="round"';
const SHADEA='fill="var(--a-soft)" stroke="none"';
const BARA='fill="var(--a)"', BARB='fill="var(--ghost)"';
const VLINE='stroke="var(--l)" stroke-width="1.4" fill="none"';
const VLACC='stroke="var(--a)" stroke-width="2.4" fill="none"';

function svg(content,label,w=720,h=330,cls=''){return `<svg class="plot ${cls}" viewBox="0 0 ${w} ${h}" role="img" aria-label="${esc(label)}" preserveAspectRatio="xMidYMid meet"><title>${esc(label)}</title>${content}</svg>`;}
function text(x,y,t,cls='label',anchor='start',attrs=''){return `<text x="${x}" y="${y}" class="${cls}" text-anchor="${anchor}" ${attrs}>${esc(t)}</text>`;}
function line(x1,y1,x2,y2,cls='axis',attrs=''){return `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" class="${cls}" ${attrs}/>`;}
function graph({series,xmin,xmax,ymin=0,ymax,xticks,yticks,xfmt,yfmt,xlabel='',ylabel='',marker,group='',under='',extra='',w=720,h=330,label=''}){
  const left=74,right=w-26,top=38,bottom=h-56;
  const X=x=>left+(x-xmin)/(xmax-xmin)*(right-left);
  const Y=y=>bottom-(y-ymin)/(ymax-ymin)*(bottom-top);
  const frame={X,Y,left,right,top,bottom};
  const fy=yfmt||(y=>num(y,ymax>10?0:1)), fx=xfmt||(x=>num(x,1));
  let c=typeof under==='function'?under(frame):under;
  (yticks||[ymin,(ymin+ymax)/2,ymax]).forEach(y=>{c+=line(left,Y(y),right,Y(y),'grid',GRID)+text(left-12,Y(y)+5,fy(y),'tick','end',TICKA);});
  c+=line(left,top,left,bottom,'axis',AXIS)+line(left,bottom,right,bottom,'axis',AXIS);
  (xticks||[xmin,(xmin+xmax)/2,xmax]).forEach(x=>{c+=line(X(x),bottom,X(x),bottom+6,'axis',AXIS)+text(X(x),bottom+26,fx(x),'tick','middle',TICKA);});
  if(ylabel)c+=text(left,22,ylabel,'label','start',LABELA);
  if(xlabel)c+=text(right,h-8,xlabel,'tick','end',TICKA);
  let body='';
  for(const s of series){
    let path='',move=true;
    for(const point of s.points){
      if(!point||!Number.isFinite(point[1])){move=true;continue;}
      path+=(move?'M':'L')+X(point[0]).toFixed(2)+','+Y(point[1]).toFixed(2)+' ';
      move=false;
    }
    body+=`<path d="${path.trim()}" class="curve ${s.cls||''}" ${s.cls==='secondary'?CURVEB:CURVEA} ${s.dash?'stroke-dasharray="7 6"':''}/>`;
  }
  if(marker){
    body+=line(X(marker.x),top,X(marker.x),bottom,'marked',MARKEDA);
    marker.ys.forEach((y,j)=>{
      body+=`<circle cx="${X(marker.x).toFixed(2)}" cy="${Y(y).toFixed(2)}" r="6" class="point" ${POINTA}/>`;
      if(marker.labels)body+=text(X(marker.x)>w*0.66?X(marker.x)-12:X(marker.x)+12,Y(y)-12,marker.labels[j],'label',X(marker.x)>w*0.66?'end':'start',LABELA);
    });
  }
  c+=group?`<g class="${group}">${body}</g>`:body;
  c+=typeof extra==='function'?extra(frame):extra;
  return svg(c,label||(ylabel+' versus '+xlabel),w,h);
}
function bars(labels,values,{max=0.65,ylabel='Preparation probability',notes=[],w=720,h=330}={}){
  const left=76,right=w-30,top=42,bottom=h-62;
  const span=(right-left)/labels.length;
  let c='';
  [0,0.25,0.5].filter(x=>x<=max).forEach(x=>{const y=bottom-x/max*(bottom-top);c+=line(left,y,right,y,'grid',GRID)+text(left-12,y+5,pc(x,0),'tick','end',TICKA);});
  c+=line(left,bottom,right,bottom,'axis',AXIS);
  if(ylabel)c+=text(left,22,ylabel,'label','start',LABELA);
  values.forEach((x,i)=>{
    const cx=left+span*(i+0.5), height=Number(x)/max*(bottom-top), barw=Math.min(104,span*0.4);
    c+=`<rect data-bar="${i}" x="${(cx-barw/2).toFixed(2)}" y="${(bottom-height).toFixed(2)}" width="${barw.toFixed(2)}" height="${Math.max(0,height).toFixed(2)}" class="bar-fill ${i===0?'secondary':''}" ${i===0?BARB:BARA}/>`
      +text(cx,bottom-height-14,pc(x),'label','middle',LABELA)
      +text(cx,bottom+28,labels[i],'label','middle',LABELA);
    if(notes[i])c+=text(cx,bottom+52,notes[i],'tick','middle',TICKA);
  });
  return svg(c,labels.map((l,i)=>`${l}: ${pc(values[i])}`).join('; '),w,h);
}
function choice(name,value){$$(`[data-choice="${name}"]`).forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.value===String(value))));}
function countTo(el,from,to,duration,format){
  if(!el)return;
  if(el._raf){cancelAnimationFrame(el._raf);el._raf=null;}
  clearTimeout(el._settle);
  if(still()||!Number.isFinite(from)){el.textContent=format(to);return;}
  const t0=performance.now();
  const settle=()=>{if(el._raf){cancelAnimationFrame(el._raf);el._raf=null;}el.textContent=format(to);};
  el._settle=setTimeout(settle,duration+250);
  const frame=now=>{
    const k=Math.min(1,(now-t0)/duration), eased=1-Math.pow(1-k,3);
    el.textContent=format(from+(to-from)*eased);
    if(k<1)el._raf=requestAnimationFrame(frame);else{el._raf=null;clearTimeout(el._settle);}
  };
  el._raf=requestAnimationFrame(frame);
}
function acknowledge(selector){if(still())return;const el=$(selector);if(el&&el.animate)el.animate([{opacity:0.35,transform:'translateY(10px)'},{opacity:1,transform:'translateY(0)'}],{duration:400,easing:'cubic-bezier(.2,.7,.2,1)'});}
/* Layers toggle with the hidden attribute; the inline display keeps SVG groups
 * hidden even where a user agent does not apply [hidden] inside an <svg>. */
function setLayer(el,shown){if(!el)return;el.classList.toggle('off',!shown);if(shown)el.removeAttribute('hidden');else el.setAttribute('hidden','');el.style.display=shown?'':'none';}

/* Shared value line: values 0..h mapped across the drawing width. */
function vlGeometry(w=1000,max=P.h){const left=64,right=w-64;return {left,right,X:x=>left+(Number(x)/max)*(right-left)};}
function vlAxis(g,y,{integers=true}={}){
  let c=line(g.X(0),y,g.X(P.h),y,'vl-axis',VLINE);
  if(integers)for(let n=0;n<=P.h;n++){
    c+=line(g.X(n),y-6,g.X(n),y+6,'vl-tick',VLINE);
    c+=text(g.X(n),y+26,String(n),'vl-label tick','middle',TICKA);
  }
  return c;
}

/* ---------- widgets ---------- */
const W={};

W.title={
  render(){
    const host=$('#title-ambient');if(!host)return;
    const w=620,h=240,g=vlGeometry(w),y=140;
    let c=`<rect class="vl-support vl-breathe" x="${g.X(0).toFixed(1)}" y="${y-46}" width="${(g.X(P.r_strong)-g.X(0)).toFixed(1)}" height="34" style="--breathe:${(P.r_weak/P.r_strong).toFixed(3)}" ${SHADEA}/>`;
    c+=line(g.X(0),y,g.X(P.h),y,'vl-axis',VLINE);
    [[P.p,'p'],[P.ell,'ℓ'],[P.h,'h']].forEach(([x,lab])=>{
      c+=line(g.X(x),y-13,g.X(x),y+13,'vl-tick',VLINE)+text(g.X(x),y+40,lab,'vl-label','middle',LABELA);
    });
    host.innerHTML=svg(c,'Ambient value line',w,h,'ambient');
  },
  reset(){this.render();}
};

/* The mechanism in words before any symbol: one value line, one stretching range,
 * two claims on the same surplus. No number is drawn here. */
W.preview={
  shown:0,
  render(){
    const host=$('#preview-vline');if(!host)return;
    const w=1000,h=200,g=vlGeometry(w),y=104;
    const barTop=44,barH=20;
    let c=`<rect id="preview-support" class="vl-support" x="${g.X(0).toFixed(1)}" y="${barTop}" width="${(g.X(P.r_strong)-g.X(0)).toFixed(1)}" height="${barH}" ${SHADEA} style="transform-box:fill-box;transform-origin:left center"/>`;
    c+=text(g.X(0)+6,barTop-10,'incumbent’s range','vl-label','start',LABELA);
    c+=line(g.X(0),y,g.X(P.h),y,'vl-axis',VLINE);
    [[P.p,'reserve','middle',y-14],[P.ell,'low challenger','middle',y+30],[P.h,'high challenger','end',y+30]].forEach(([x,label,anchor,ly])=>{
      c+=line(g.X(x),y-10,g.X(x),y+10,'vl-tick',VLINE)+text(g.X(x),ly,label,'vl-label',anchor,LABELA);
    });
    const keepsFrom=g.X(P.r_strong), keepsTo=g.X(P.h);
    const shareFrom=g.X(P.ell), shareTo=g.X(P.r_strong);
    let brackets='<g class="preview-brackets">';
    brackets+=line(keepsFrom,54,keepsTo,54,'marked',MARKEDA)+line(keepsFrom,54,keepsFrom,70,'marked',MARKEDA)+line(keepsTo,54,keepsTo,70,'marked',MARKEDA);
    brackets+=text((keepsFrom+keepsTo)/2,34,'what the challenger keeps','label','middle',LABELA);
    brackets+=line(shareFrom,162,shareTo,162,'marked',MARKEDA)+line(shareFrom,150,shareFrom,162,'marked',MARKEDA)+line(shareTo,150,shareTo,162,'marked',MARKEDA);
    brackets+=text(g.X(0)+6,186,'what shareholders receive depends on the challenger','label','start',LABELA);
    brackets+='</g>';
    host.innerHTML=svg(c+brackets,'Value line in words: the reserve, the two challenger values, the incumbent’s range, and the two claims on the surplus',w,h,'vline');
    this.layer();
  },
  layer(){
    const host=$('#preview-vline');if(!host)return;
    const support=host.querySelector('#preview-support');
    if(support)support.style.transform=`scaleX(${this.shown>=1?'1':(P.r_weak/P.r_strong).toFixed(4)})`;
    setLayer(host.querySelector('.preview-brackets'),this.shown>=2);
  },
  onStep(s){this.shown=s;this.layer();},
  reset(){this.shown=0;this.render();}
};

W.auction={
  init(){
    const slider=$('#auction-r');
    if(slider){slider.min='0';slider.max=String(P.r_strong);slider.step='0.05';slider.value=String(state.auctionR);}
  },
  render(){
    const R=state.auctionR, theta=state.quality==='H'?P.h:P.ell;
    const win=theta>R, price=Math.max(P.p,Math.min(R,theta)), profit=win?theta-price:0;
    const slider=$('#auction-r');
    if(slider){slider.max=String(P.r_strong);slider.value=String(R);}
    const readValue=$('#auction-r-value');if(readValue)readValue.textContent=num(R,2);
    choice('quality',state.quality);
    const host=$('#auction-vline');
    if(host){
      const w=1000,h=150,g=vlGeometry(w),y=96;
      let c=`<rect class="vl-support" x="${g.X(0).toFixed(1)}" y="52" width="${(g.X(P.r_strong)-g.X(0)).toFixed(1)}" height="20" ${SHADEA}/>`;
      c+=text(g.X(P.r_strong)+14,68,'R ~ U[0, r]','vl-label','start',LABELA);
      c+=vlAxis(g,y);
      c+=line(g.X(P.p),46,g.X(P.p),y+14,'vl-reserve',MARKEDA)+text(g.X(P.p),38,'p','vl-label','middle',LABELA);
      c+=text(g.X(P.ell),y+44,'ℓ','vl-label','middle',LABELA)+text(g.X(P.h),y+44,'h','vl-label','middle',LABELA);
      c+=line(g.X(theta),y-24,g.X(theta),y+24,'vl-tick accent',VLACC);
      c+=text(g.X(theta),y-32,state.quality==='H'?'θ = h':'θ = ℓ','vl-label accent',g.X(theta)>w*0.9?'end':'middle',LABELA);
      c+=`<circle class="vl-marker" cx="${g.X(R).toFixed(1)}" cy="${y}" r="7" ${POINTA}/>`;
      c+=text(g.X(R),y-18,'R = '+num(R,2),'vl-label tick','middle',TICKA);
      host.innerHTML=svg(c,`Value line: reserve ${P.p}, incumbent support up to ${P.r_strong}, realised R ${num(R,2)}`,w,h,'vline');
    }
    const readout=$('#auction-readout');
    if(readout)readout.innerHTML=`<div class="readout"><p class="kicker">${win?'Challenger':'Incumbent'} wins${theta===R?' (display tie rule)':''}</p><span class="metric accent">${num(price,2)}</span><p class="metric-label">Payment to target shareholders</p></div>`+
      `<div class="readout"><p class="kicker">Challenger gross profit</p><span class="metric">${num(profit,2)}</span><p class="metric-label">Before the preparation cost</p></div>`;
  },
  reset(){state.quality='H';state.auctionR=0.8;this.render();}
};

W.dial={
  rMax:3.6,rMin:1.01,
  init(){
    const slider=$('#dial-r');
    if(slider){slider.min=String(this.rMin);slider.max=String(this.rMax);slider.step='0.01';slider.value=String(state.dialR);}
    const host=$('#dial-vline');
    if(host){
      const w=1000,h=150,g=vlGeometry(w),y=96;
      const full=(g.X(this.rMax)-g.X(0)).toFixed(1);
      let c=`<rect id="dial-support" class="vl-support" x="${g.X(0).toFixed(1)}" y="52" width="${full}" height="20" ${SHADEA} style="transform-box:fill-box;transform-origin:left center"/>`;
      c+=text(g.X(0),44,'R ~ U[0, r]','vl-label','start',LABELA);
      c+=vlAxis(g,y);
      c+=line(g.X(P.p),46,g.X(P.p),y+14,'vl-reserve',MARKEDA)+text(g.X(P.p),38,'p','vl-label','middle',LABELA);
      c+=text(g.X(P.ell),y+44,'ℓ','vl-label','middle',LABELA)+text(g.X(P.h),y+44,'h','vl-label','middle',LABELA);
      c+=`<circle id="dial-edge" class="vl-marker" cx="${g.X(state.dialR).toFixed(1)}" cy="${y}" r="7" ${POINTA}/>`;
      host.innerHTML=svg(c,'Value line: the incumbent support stretches with r',w,h,'vline');
      this.geometry=g;
    }
  },
  render(){
    const r=state.dialR, c=cf(r), f=D.fig1;
    const slider=$('#dial-r');if(slider)slider.value=String(r);
    const readValue=$('#dial-r-value');if(readValue)readValue.textContent=num(r,2);
    choice('dial-preset',r===P.r_weak?'weak':r===P.r_strong?'strong':'');
    const support=$('#dial-support');
    if(support)support.style.transform=`scaleX(${(r/this.rMax).toFixed(4)})`;
    const edge=$('#dial-edge');
    if(edge&&this.geometry)edge.setAttribute('cx',this.geometry.X(r).toFixed(1));
    const profit=$('#dial-profit .metric'), spread=$('#dial-spread .metric');
    countTo(profit,Number(profit&&profit.textContent),c.B_prior,500,x=>num(x,3));
    countTo(spread,Number(spread&&spread.textContent),c.Delta_T,500,x=>num(x,3));
    const curves=$('#dial-curves');
    if(curves)curves.innerHTML=`<div class="plot-shell">${graph({
        series:[{points:f.r.map((x,i)=>[Number(x),Number(f.B['0.5'][i])])}],
        xmin:1,xmax:3.8,ymin:3.8,ymax:5.2,yticks:[4,4.5,5],xticks:[1,2,3,3.8],
        xlabel:'Incumbent strength r',ylabel:'Expected challenger profit B(½)',
        marker:{x:r,ys:[c.B_prior],labels:[num(c.B_prior,3)]},w:520,h:300})}</div>`+
      `<div class="plot-shell">${graph({
        series:[{points:f.r.map((x,i)=>[Number(x),Number(f.Delta_T[i])])}],
        xmin:1,xmax:3.8,ymin:0,ymax:1.1,yticks:[0,0.5,1],xticks:[1,2,3,3.8],
        xlabel:'Incumbent strength r',ylabel:'Target-payoff spread ΔT',
        marker:{x:r,ys:[c.Delta_T],labels:[num(c.Delta_T,3)]},w:520,h:300})}</div>`;
  },
  reset(){state.dialR=P.r_weak;this.render();}
};

function posterior(x){const likelihood=Math.exp((Math.abs(x+1)-Math.abs(x-1))/P.b);return likelihood/(1+likelihood);}

W.tape={
  shown:0,
  init(){
    const slider=$('#tape-x');
    if(slider){slider.min='-3';slider.max='3';slider.step='0.02';slider.value=String(state.tapeX);}
  },
  render(){
    const x=state.tapeX, c=cf(P.r_strong), mu=posterior(x);
    const high=c.g_L+mu*(c.g_H-c.g_L)>=P.c_H;
    const entry=high?1:P.rho;
    const price=c.t_0+entry*(c.t_L-c.t_0+c.Delta_T*mu);
    const slider=$('#tape-x');if(slider)slider.value=String(x);
    const readValue=$('#tape-x-value');if(readValue)readValue.textContent=num(x,2);
    const host=$('#tape-plot');
    if(host){
      const points=Array.from({length:151},(_,i)=>{const t=-3+i*0.04;return [t,posterior(t)];});
      host.innerHTML=graph({
        series:[{points}],xmin:-3,xmax:3,ymin:0,ymax:1,xticks:[-3,-1,0,1,3],yticks:[0,0.5,1],
        xlabel:'Order flow X',ylabel:'Posterior Pr(H | X)',
        marker:{x,ys:[mu],labels:[pc(mu)]},group:'tape-curve',
        under:({X,Y,top,bottom,left,right})=>
          `<rect class="shade" x="${left}" y="${top}" width="${(X(-1)-left).toFixed(1)}" height="${bottom-top}" ${SHADEA}/>`+
          `<rect class="shade" x="${X(1).toFixed(1)}" y="${top}" width="${(right-X(1)).toFixed(1)}" height="${bottom-top}" ${SHADEA}/>`,
        extra:({X,Y,left,right})=>`<g class="tape-tau">`+
          line(left,Y(c.tau),right,Y(c.tau),'marked',MARKEDA)+
          text(left+10,Y(c.tau)-12,'High-cost threshold τ = '+num(c.tau,3),'tick','start',TICKA)+`</g>`,
        w:760,h:340,label:'Posterior probability of the high value state against order flow'});
    }
    const readout=$('#tape-readout');
    if(readout)readout.innerHTML=`<div class="readout"><p class="kicker">Observed target price</p><span class="metric">${num(price,3)}</span></div>`+
      `<div class="readout"><p class="kicker">Cost-averaged preparation at this flow</p><span class="metric accent">${pc(entry,0)}</span></div>`+
      `<p class="small">${high?'Both cost realizations prepare.':'Only the low-cost realization prepares.'}</p>`+
      `<p class="small muted">The price reveals the posterior. The challenger never observes order flow directly.</p>`;
    this.layer();
  },
  layer(){
    const host=$('#tape-plot');
    if(host){setLayer(host.querySelector('.tape-curve'),this.shown>=1);setLayer(host.querySelector('.tape-tau'),this.shown>=2);}
    setLayer($('#tape-readout'),this.shown>=3);
  },
  onStep(s){this.shown=s;this.layer();},
  reset(){state.tapeX=-1.5;this.render();}
};

function economyCard(r,label){
  const row=eqRow(r);
  return `<article class="economy ${Number(r)===P.r_strong?'strong':''}"><h3>${esc(label)} / r = ${esc(String(r))}</h3>`+
    `<p class="metric-label">Preparation probability</p><span class="metric ${Number(r)===P.r_strong?'accent':''}">${pc(row.E)}</span>`+
    `<p>${Number(row.q_H)===0?'No informed orders; no price information.':'Full informed orders; informative prices.'}</p>`+
    `<p class="small muted">Orders: q<sub>H</sub> = ${esc(String(Number(row.q_H)))}, q<sub>L</sub> = ${esc(String(Number(row.q_L)))}</p></article>`;
}
W.economies={
  render(){
    choice('benchmark',state.benchmark);
    const compare=$('#economies-compare');
    if(compare)compare.setAttribute('aria-pressed',String(state.compare));
    const view=$('#economies-view');if(!view)return;
    const caption='<p class="plot-caption">At the declared benchmark.</p>';
    if(state.compare){view.innerHTML=`<div class="comparison">${economyCard(P.r_weak,'Weak')}${economyCard(P.r_strong,'Strong')}</div>`+caption;return;}
    const strong=state.benchmark==='strong', r=strong?P.r_strong:P.r_weak;
    view.innerHTML=`<div class="split">${economyCard(r,strong?'Strong':'Weak')}<div class="stack"><p class="display">${strong?'Information makes<br><i>costly preparation pay.</i>':'Trading cannot<br><i>cover its cost.</i>'}</p><p class="small muted">Analytical uniqueness of trading and on-path preparation.</p></div></div>`+caption;
  },
  reset(){state.benchmark='weak';state.compare=false;this.render();}
};

W.control={
  render(){
    const host=$('#control-plot');
    const previous=host?[...host.querySelectorAll('[data-bar]')].map(e=>Number(e.getAttribute('height'))):[];
    const frozen=state.experiment==='frozen';
    const weak=eqRow(P.r_weak,state.experiment), strong=eqRow(P.r_strong,state.experiment);
    choice('experiment',state.experiment);
    if(host){
      host.innerHTML=bars(['Weak incumbent','Strong incumbent'],[Number(weak.E),Number(strong.E)]);
      if(!still())host.querySelectorAll('[data-bar]').forEach((el,i)=>{
        const height=Number(el.getAttribute('height'));
        if(!height)return;
        el.style.transformBox='fill-box';el.style.transformOrigin='center bottom';
        el.animate([{transform:`scaleY(${previous[i]?previous[i]/height:1})`},{transform:'scaleY(1)'}],{duration:650,easing:'cubic-bezier(.2,.7,.2,1)'});
      });
    }
    const readout=$('#control-readout');
    if(readout)readout.innerHTML=`<p class="display">${frozen?'Entry <i>falls.</i>':'Entry <i>rises.</i>'}</p>`+
      `<p class="num">${pc(weak.E)} → ${pc(strong.E)}</p>`+
      `<p>${frozen?'The information experiment stays fixed. Lower acquisition profits deter preparation.':'Rival strength changes trading incentives and the information available before preparation.'}</p>`+
      `<p class="small muted">${frozen?'Fixed full-order diagnostic. The weak-incumbent profile is not an equilibrium; it admits profitable trading deviations.':'Analytical equilibrium comparison under Proposition 2. The information experiment is endogenous.'}</p>`;
  },
  reset(){state.experiment='feedback';this.render();}
};

W.coexist={
  shown:0,
  render(){
    const host=$('#coexist-plot');if(!host)return;
    const w=1100,h=420,left=120,right=w-60,top=56,bottom=h-90;
    const rMin=Number(D.fig2&&D.fig2.x_range?D.fig2.x_range[0]:1), rMax=3.8, eMax=0.65;
    const X=r=>left+(Number(r)-rMin)/(rMax-rMin)*(right-left);
    const Y=e=>bottom-(Number(e)/eMax)*(bottom-top);
    let c='';
    [0,0.25,0.5].forEach(e=>{c+=line(left,Y(e),right,Y(e),'grid',GRID)+text(left-14,Y(e)+5,pc(e,0),'tick','end',TICKA);});
    c+=line(left,top,left,bottom,'axis',AXIS)+line(left,bottom,right,bottom,'axis',AXIS);
    [1,1.5,2,2.5,3,3.5,3.8].forEach(r=>{c+=line(X(r),bottom,X(r),bottom+6,'axis',AXIS)+text(X(r),bottom+26,num(r,1),'tick','middle',TICKA);});
    c+=text(left,26,'Preparation probability','label','start',LABELA)+text(right,h-10,'Incumbent strength r','tick','end',TICKA);

    let nodes='';
    [P.r_weak,P.r_strong,P.r_collapse].forEach(r=>{
      const row=eqRow(r);
      nodes+=`<circle class="node" cx="${X(r).toFixed(1)}" cy="${Y(row.E).toFixed(1)}" r="9" ${NODEA}/>`
        +text(X(r),Y(row.E)-22,pc(row.E),'tick','middle',TICKA)
        +text(X(r),bottom+52,'r = '+Number(r),'tick','middle',TICKA);
    });

    const rows=(D.tables.certificates||[]).filter(row=>row.accepted==='true');
    let certs='';
    rows.forEach(row=>{
      const lower=Number(outward(row.E_lower,false)), upper=Number(outward(row.E_upper,true));
      let y1=Y(upper), y2=Y(lower);
      if(y2-y1<12){const mid=(y1+y2)/2;y1=mid-6;y2=mid+6;}
      const x=X(row.r);
      certs+=`<g class="cert"><title>${esc('r = '+row.r+': E in ['+row.E_lower+', '+row.E_upper+']')}</title>`
        +line(x,y1,x,y2,'cert',CERTA)
        +line(x-9,y1,x+9,y1,'cert',CERTA)
        +line(x-9,y2,x+9,y2,'cert',CERTA)+`</g>`;
    });
    if(rows.length){
      /* One shared label: the three certified intervals sit within 0.01 of each other. */
      const lo=outward(rows.map(r=>r.E_lower).sort()[0],false,3), hi=outward(rows.map(r=>r.E_upper).sort().slice(-1)[0],true,3);
      const xs=rows.map(r=>X(r.r)), xm=(Math.min(...xs)+Math.max(...xs))/2, yTop=Math.min(...rows.map(r=>Y(Number(outward(r.E_upper,true)))));
      certs+=text(xm,yTop-40,rows.length+' certified equilibria','label','middle',LABELA)
        +text(xm,yTop-18,'E in ['+lo+', '+hi+']','tick','middle',TICKA)
        +text(xm,bottom+52,'r = '+rows[0].r+' to '+rows[rows.length-1].r,'tick','middle',TICKA);
    }

    const pooling=D.fig2&&D.fig2.thresholds&&D.fig2.thresholds.pooling_existence;
    const rPool=pooling?Number(pooling.value):NaN;
    let level='';
    if(Number.isFinite(rPool)){
      level=`<g class="pooling">`+line(X(rMin),Y(P.rho),X(rPool),Y(P.rho),'marked',MARKEDA)
        +text(X(rPool)+10,Y(P.rho)+5,'pooling coexists','label','start',LABELA)+`</g>`;
    }
    const collapseRow=eqRow(P.r_collapse);
    const annotation=`<g class="collapse-note">`+text(X(P.r_collapse)-16,Y(collapseRow.E)+34,'E = ρ','label','end',LABELA)
      +line(X(P.r_collapse)-14,Y(collapseRow.E)+28,X(P.r_collapse)-2,Y(collapseRow.E)+10,'marked',MARKEDA)+`</g>`;

    c+=`<g class="nodes">${nodes}</g><g class="certificates">${certs}${level}</g>${annotation}`;
    host.innerHTML=svg(c,'Preparation at three analytically established strengths and three certified equilibria; points are not connected',w,h);
    this.layer();
  },
  layer(){
    const host=$('#coexist-plot');if(!host)return;
    setLayer(host.querySelector('.nodes'),this.shown>=1);
    setLayer(host.querySelector('.certificates'),this.shown>=2);
    setLayer(host.querySelector('.collapse-note'),this.shown>=3);
  },
  onStep(s){this.shown=s;this.layer();},
  reset(){this.render();}
};

W.bargaining={
  render(){
    const eta=state.eta;
    const slider=$('#seller-weight');if(slider)slider.value=String(eta);
    const readValue=$('#seller-weight-value');if(readValue)readValue.textContent=num(eta,2);
    choice('eta',eta);
    const groups=[P.r_weak,P.r_strong].map(r=>D.fig4[String(r)]);
    if(groups.some(g=>!g))throw Error('Missing declared bargaining series');
    const series=groups.map((g,i)=>({points:g.eta.map((x,j)=>[Number(x),Number(g.Delta_eta[j])]),cls:i?'':'secondary'}));
    const ys=groups.map(g=>{
      const i=g.eta.findIndex(x=>Math.abs(Number(x)-eta)<1e-8);
      if(i<0)throw Error('No declared bargaining weight');
      return Number(g.Delta_eta[i]);
    });
    const host=$('#bargaining-plot');
    if(host)host.innerHTML=graph({series,xmin:0,xmax:1,ymin:0,ymax:P.h-P.ell,yticks:[0,3,6,9],xticks:[0,0.5,1],
      xlabel:'Seller weight η',ylabel:'Target-payoff spread',marker:{x:eta,ys},
      extra:({left})=>text(left+12,78,'Amber: strong incumbent','tick','start',TICKA)+text(left+12,100,'Grey: weak incumbent','tick','start',TICKA),
      w:760,h:340});
    const readout=$('#bargaining-readout');
    if(readout){
      readout.innerHTML=`<p class="kicker">Seller weight η = ${num(eta,2)}</p>`+
        `<p class="display">${eta<0.5?'The spread<br><i>widens.</i>':eta>0.5?'The spread<br><i>narrows.</i>':'The strength effect<br><i>vanishes.</i>'}</p>`+
        m(String.raw`\Delta_\eta=\eta(h-\ell)+(1-2\eta)\mathbb E[(R-\ell)_+]`,'eq-small')+
        `<p class="small muted">${eta===1?'At η = 1, challenger profits are zero. This is a payment-stage endpoint.':'Challenger profits weakly fall as the incumbent strengthens.'}</p>`;
      math(readout);
    }
  },
  reset(){state.eta=0.25;this.render();}
};

W.certificates={
  render(){
    const host=$('#certificate-table');if(!host)return;
    host.innerHTML=`<table class="data-table"><thead><tr><th>Strength r</th><th>Low-type order magnitude</th><th>Preparation interval</th></tr></thead><tbody>`+
      D.tables.certificates.map(c=>`<tr><td class="num">${esc(c.r)}</td><td class="num">[${esc(c.v_lower)}, ${esc(c.v_upper)}]</td><td class="num" title="${esc(c.E_lower+' to '+c.E_upper)}">[${esc(outward(c.E_lower,false))}, ${esc(outward(c.E_upper,true))}]</td></tr>`).join('')+
      `</tbody></table>`;
  },
  reset(){this.render();}
};

W.reserve={
  render(){
    const host=$('#reserve-table');if(!host)return;
    const rows=D.tables.reserve_comparisons||[];
    const short=t=>String(t||'').split(' (')[0];
    host.innerHTML=`<table class="data-table dense"><thead><tr><th>Value law</th><th>Reserve p</th><th>Strength r</th><th>Orders q<sub>H</sub> / q<sub>L</sub></th><th>Preparation e<sub>H</sub> / e<sub>L</sub></th><th>Entry E</th><th>Revenue R<sub>T</sub></th><th>Status</th></tr></thead><tbody>`+
      rows.map(row=>`<tr title="${esc(row.status)}"><td>${esc(row.value_law.replace('_',' '))}</td><td class="num">${esc(row.p)}</td><td class="num">${esc(row.r)}</td>`+
        `<td class="num">${num(row.q_H,0)} / ${num(row.q_L,0)}</td><td class="num">${num(row.e_H,3)} / ${num(row.e_L,3)}</td>`+
        `<td class="num">${num(row.E,3)}</td><td class="num">${num(row.R_T,3)}</td><td>${esc(short(row.status))}</td></tr>`).join('')+
      `</tbody></table>`;
  },
  reset(){this.render();}
};

/* Access to prices: the two economies at the strong incumbent, registry values only. */
W.access={
  render(){
    const host=$('#access-table');if(!host)return;
    const rows=[
      ['Preparation probability',pct('base_hidden_entry_strong'),pct('base_entry_strong')],
      ['Expected target proceeds',fmt('base_revenue_hidden',3),fmt('base_revenue_feedback',3)],
      ['Net acquisition surplus gain','reference','+'+fmt('base_net_surplus_gain',3)]
    ];
    host.innerHTML=`<table class="data-table"><thead><tr><th>At r = ${v('base_r_strong')}</th><th>Price hidden</th><th>Price observed</th></tr></thead><tbody>`+
      rows.map(([label,hidden,observed])=>`<tr><td>${esc(label)}</td><td>${esc(hidden)}</td><td>${esc(observed)}</td></tr>`).join('')+
      `</tbody></table>`;
  },
  reset(){this.render();}
};

W.glossary={
  render(){
    const host=$('#glossary-table');if(!host)return;
    host.innerHTML=glossaryHTML('dense');
    math(host);
  },
  reset(){this.render();}
};

/* ---------- widget plumbing ---------- */
function widgetOf(i=index){return W[slides[i].widget];}
function renderAll(){Object.keys(W).forEach(name=>{try{W[name].render();}catch(e){errors.push(name+': '+e.message);}});}
function initWidgets(){Object.keys(W).forEach(name=>{try{if(W[name].init)W[name].init();}catch(e){errors.push(name+': '+e.message);}});}
function resetCurrent(){
  step=0;
  const widget=widgetOf();
  if(widget&&widget.reset){try{widget.reset();}catch(e){errors.push(e.message);}}
  updateReveals();
}
document.addEventListener('click',e=>{
  const pick=near(e,'[data-choice]');
  if(pick){
    const name=pick.dataset.choice, value=pick.dataset.value;
    if(name==='quality'){state.quality=value;W.auction.render();acknowledge('#auction-readout');}
    if(name==='dial-preset'){state.dialR=value==='strong'?P.r_strong:P.r_weak;W.dial.render();}
    if(name==='benchmark'){state.benchmark=value;state.compare=false;W.economies.render();acknowledge('#economies-view');}
    if(name==='experiment'){state.experiment=value;W.control.render();}
    if(name==='eta'){state.eta=Number(value);W.bargaining.render();acknowledge('#bargaining-readout');}
  }
  const reset=near(e,'[data-reset]');
  if(reset){
    const name=reset.dataset.reset;
    if(W[name]&&W[name].reset){W[name].reset();step=0;updateReveals();}
    else resetCurrent();
  }
  if(near(e,'#economies-compare')){state.compare=!state.compare;W.economies.render();acknowledge('#economies-view');}
  if(near(e,'#tape-demo')){state.tapeX=state.tapeX<cf(P.r_strong).x_star?1.5:-1.5;W.tape.render();acknowledge('#tape-readout');}
});
document.addEventListener('input',e=>{
  const id=e.target.id, value=Number(e.target.value);
  if(id==='auction-r'){state.auctionR=value;W.auction.render();}
  if(id==='dial-r'){state.dialR=value;W.dial.render();}
  if(id==='tape-x'){state.tapeX=value;W.tape.render();}
  if(id==='seller-weight'){state.eta=value;W.bargaining.render();}
});

initWidgets();
renderAll();

/* ---------- checks, print and public surface ---------- */
const formulaCheck=window.CCC.explorer.selfTest();
if(!formulaCheck.ok)errors.push('Benchmark formula self-check failed');
function selfCheck(){
  return {
    slides:slides.length,mainSlides:main.length,
    minutes:main.reduce((n,s)=>n+s.minutes,0),
    widgets:Object.keys(W),
    glossaryKeys:glossary.length,
    undefinedDefs:undefinedDefs(),
    stageScale,
    formulaCheck,
    mathErrors:$$('.math-error,.katex-error').length,
    errors:[...errors],
    unresolved:document.body.innerText.includes('[['),
    active:slides[index].id,
    step
  };
}
let savedPrintState=null;
window.addEventListener('beforeprint',()=>{
  document.documentElement.dataset.printing='true';
  document.getAnimations().forEach(a=>{try{a.finish();}catch{}});
  savedPrintState={state:{...state},theme:document.documentElement.dataset.theme||'dark'};
  state.compare=true;state.experiment='frozen';state.tapeX=1.5;
  W.tape.shown=3;W.coexist.shown=3;W.preview.shown=2;
  renderAll();
  theme('light');
  scaleStage();
  $$('.slide').forEach(s=>{
    s.inert=false;s.setAttribute('aria-hidden','false');
    s.querySelectorAll('[data-step]').forEach(el=>{el.classList.add('shown');el.inert=false;el.setAttribute('aria-hidden','false');});
  });
});
window.addEventListener('afterprint',()=>{
  delete document.documentElement.dataset.printing;
  if(savedPrintState){
    Object.assign(state,savedPrintState.state);
    theme(savedPrintState.theme);
    savedPrintState=null;
  }
  W.tape.shown=step;W.coexist.shown=step;W.preview.shown=step;
  renderAll();
  scaleStage();
  go(index,{history:true,step});
});
/* Layout audit: walks every slide with all reveals shown and reports bodies that overflow the
 * stage or columns whose content is wider than the column. Run `await DECK.audit()` in the console. */
async function audit(){
  const saved={index,step}, out=[];
  for(const s of slides){
    go(s.id,{step:99,history:true});
    await new Promise(r=>setTimeout(r,40));
    const el=$('#'+s.id), body=el.querySelector('.slide-body'), head=el.querySelector('.slide-head'), foot=el.querySelector('.slide-foot');
    const kids=[...body.children], top=Math.min(...kids.map(k=>k.getBoundingClientRect().top)), bottom=Math.max(...kids.map(k=>k.getBoundingClientRect().bottom));
    const vertical=body.scrollHeight-body.clientHeight, up=head.getBoundingClientRect().bottom-top, down=bottom-foot.getBoundingClientRect().top;
    const wide=[...el.querySelectorAll('.split>*,.stack,.equation,.defs,.plot-shell,.controls')].filter(n=>n.scrollWidth>n.clientWidth+2).map(n=>n.className.split(' ')[0]+':'+(n.scrollWidth-n.clientWidth));
    if(vertical>2||up>0||down>8||wide.length)out.push({id:s.id,vertical,up:Math.round(up),down:Math.round(down),wide});
  }
  go(saved.index,{step:saved.step,history:true});
  return out;
}
window.DECK={audit,go,next,previous,reset:resetCurrent,selfCheck,state,slides,widgets:Object.keys(W),eqRow,cf,posterior,renderAll,notesText,theme};
const opening=location.hash.slice(1);
go(slides.some(s=>s.id===opening)?opening:0,{history:true,step:0});
window.DECK.ready=document.fonts.ready.then(()=>selfCheck());
})();
