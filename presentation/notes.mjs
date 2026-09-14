/* Speaker notes as Markdown from the slide records. Reads the CCC_DATA JSON on stdin so the
 * registry-bound numbers in slide copy resolve exactly as they do in the deck. */
import {createRequire} from 'node:module';
import fs from 'node:fs';
const require=createRequire(import.meta.url);
const D=JSON.parse(fs.readFileSync(0,'utf8'));
global.window={};
require('./content.js');
const reg=k=>{if(!D.registry[k])throw Error('Missing registry key: '+k);return D.registry[k];};
const H={m:()=>'',mi:()=>'',v:k=>reg(k).display.replace(/\\%/g,'%'),pct:k=>(100*Number(reg(k).value)).toFixed(1)+'%',fmt:(k,n=3)=>Number(reg(k).value).toFixed(n),link:()=>''};
const slides=window.createSlides(H), main=slides.filter(s=>!s.backup);
const plain=t=>String(t||'').replace(/<[^>]*>/g,'').replace(/&[a-z]+;/gi,' ').replace(/\s+/g,' ').trim();
let out='# Competition Creates Competition\n\nSpeaker notes. 40-minute talk by Austin Li; '+main.length+' main slides, '+(slides.length-main.length)+' technical discussion slides.\n\n';
let elapsed=0;
for(const [i,s] of slides.entries()){
  const label=s.backup?'Backup '+(i-main.length+1):String(i+1);
  out+=`## ${label}. ${plain(s.title)||'Competition creates competition'}\n\n`;
  if(!s.backup){out+=`${elapsed} to ${elapsed+s.minutes} minutes (${s.minutes} min). Status: ${s.status||'none'}.\n\n`;elapsed+=s.minutes;}
  out+=`${s.notes}\n\nSource: ${s.source}\n\n`;
}
process.stdout.write(out);
