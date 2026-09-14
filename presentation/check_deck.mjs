/* Offline structural check: the slide records satisfy DESIGN.md.
 * Ids, acts, statuses, minutes, widget elements, "If asked" notes, no hedge in slide copy,
 * no registry number in a headline, and the notation rule: every symbol that appears in
 * LaTeX on a slide is defined on that slide or an earlier one. */
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
global.window={};
require('./content.js');

const enc=l=>encodeURIComponent(l);
const H={m:(l,c)=>`<div class="equation ${c||''}" data-latex="${enc(l)}"></div>`,mi:l=>`<span data-latex="${enc(l)}"></span>`,v:()=>'§V§',pct:()=>'§P§',fmt:()=>'§F§',link:()=>''};
const slides=window.createSlides(H), main=slides.filter(s=>!s.backup), problems=[];
const glossary=typeof window.createGlossary==='function'?window.createGlossary(H):null;
if(!glossary)problems.push('content.js does not export createGlossary');
const keys=new Set((glossary||[]).map(g=>g.key));

const need={preview:['preview-vline'],auction:['auction-vline','auction-r','auction-r-value','auction-readout','data-choice="quality"','data-reset="auction"'],dial:['dial-vline','dial-r','dial-r-value','dial-profit','dial-spread','dial-curves','data-choice="dial-preset"'],tape:['tape-plot','tape-x','tape-x-value','tape-demo','tape-readout','data-reset="tape"'],economies:['economies-compare','economies-view','data-choice="benchmark"'],control:['control-plot','control-readout','data-choice="experiment"'],coexist:['coexist-plot'],bargaining:['seller-weight','seller-weight-value','bargaining-plot','bargaining-readout','data-choice="eta"'],certificates:['certificate-table'],reserve:['reserve-table'],access:['access-table'],glossary:['glossary-table'],title:['title-ambient']};
const statuses=new Set(['','analytical','computer-assisted','numerical diagnostic','open','input']);
const acts=['question','preview','model','equilibrium','results','next'];
const hedge=/not an empirical estimate|not an equilibrium simulation|not a joint calibration|no claim of/i;
const headline=/<(h1|h2|p class="display[^"]*"|div class="callout"|p class="metric[^"]*")[^>]*>[^<]*§[PFV]§/;

let defined=new Set();
for(const s of slides){
  for(const k of ['id','act','title','body','notes','source','minutes','widget','status'])if(s[k]===undefined)problems.push(`${s.id}: missing ${k}`);
  if(!statuses.has(s.status))problems.push(`${s.id}: status "${s.status}" is not in the paper's vocabulary`);
  if(!s.backup&&!acts.includes(s.act))problems.push(`${s.id}: act "${s.act}"`);
  if(!/If asked:/.test(s.notes))problems.push(`${s.id}: notes lack an "If asked:" line`);
  if(s.widget&&!need[s.widget])problems.push(`${s.id}: unknown widget ${s.widget}`);
  for(const n of need[s.widget]||[])if(!s.body.includes(n))problems.push(`${s.id}: widget ${s.widget} lacks ${n}`);
  if(hedge.test(s.body))problems.push(`${s.id}: hedge in slide copy`);
  if(!s.backup&&(headline.test(s.body)||/§[PFV]§/.test(s.title)))problems.push(`${s.id}: registry number in a headline element`);
  for(const k of s.defines||[]){if(!keys.has(k))problems.push(`${s.id}: defines unknown key ${k}`);defined.add(k);}
  for(const d of s.body.matchAll(/data-defs="([^"]*)"/g))for(const k of d[1].split(','))if(!keys.has(k.trim()))problems.push(`${s.id}: definition strip names unknown key ${k}`);
  const latex=[...s.body.matchAll(/data-latex="([^"]*)"/g)].map(x=>decodeURIComponent(x[1])).join('\n');
  for(const g of glossary||[]){
    let re;try{re=new RegExp(g.pattern);}catch(e){problems.push(`glossary ${g.key}: bad pattern`);continue;}
    if(re.test(latex)&&!defined.has(g.key))problems.push(`${s.id}: uses ${g.key} before it is defined`);
  }
}
for(const k of keys)if(!slides.some(s=>(s.defines||[]).includes(k)))problems.push(`glossary key never defined on a slide: ${k}`);
const minutes=main.reduce((a,s)=>a+s.minutes,0);
if(Math.abs(minutes-40)>1e-9)problems.push(`main slides sum to ${minutes} minutes, not 40`);
console.log(`${slides.length} slides (${main.length} main, ${slides.length-main.length} backup), ${minutes} minutes, ${keys.size} glossary keys`);
if(problems.length){console.error(problems.join('\n'));process.exit(1);}
console.log('Deck contract satisfied.');
