(function(){
const Dm=r=>(r-1)*(r-1)/(2*r), tau=r=>(48*r-3)/(4*(20*r-r*r-1));
const k=0.02,rho=0.25,b=11/51,rA=1.39395792,rF=1.46098466,rN=1.74787754,rC=3.45824703,EA=37/68;
const it=s=>`<tspan font-style="italic" font-family="Georgia,'Times New Roman',serif">${s}</tspan>`;
function frame(W,H,m,xr,yr){return{xs:x=>m.l+(x-xr[0])/(xr[1]-xr[0])*(W-m.l-m.r),ys:y=>H-m.b-(y-yr[0])/(yr[1]-yr[0])*(H-m.t-m.b)};}
function axes(W,H,m,xs,ys,xt,yt,fx,fy,xl,yl,fs){let s='';
 yt.forEach(v=>{s+=`<line class="grid" x1="${m.l}" x2="${W-m.r}" y1="${ys(v)}" y2="${ys(v)}"/><text class="tk" x="${m.l-7}" y="${ys(v)+fs*.35}" text-anchor="end" font-size="${fs}">${fy(v)}</text>`;});
 xt.forEach(v=>{s+=`<line class="ax" x1="${xs(v)}" x2="${xs(v)}" y1="${H-m.b}" y2="${H-m.b+4}"/><text class="tk" x="${xs(v)}" y="${H-m.b+fs+5}" text-anchor="middle" font-size="${fs}">${fx(v)}</text>`;});
 s+=`<line class="ax" x1="${m.l}" x2="${W-m.r}" y1="${H-m.b}" y2="${H-m.b}"/><text class="lab" x="${(m.l+W-m.r)/2}" y="${H-6}" text-anchor="middle" font-size="${fs}">${xl}</text><text class="lab" x="${m.l}" y="${m.t-10}" font-size="${fs}">${yl}</text>`;return s;}
function marks(xs,m,H,fs,end3){let s='';[[1.2,'r','₀'],[3,'r','₁'],[3.6,'r','₂']].forEach(([r,a,c])=>{const e=end3&&r===3;
 s+=`<line class="vd" x1="${xs(r)}" x2="${xs(r)}" y1="${m.t}" y2="${H-m.b}"/><text class="lab" x="${xs(r)+(e?-5:5)}" y="${m.t+12}" text-anchor="${e?'end':'start'}" font-size="${fs}">${it(a)}${c}</text>`;});return s;}
function chartTau(n){const W=n?420:680,H=n?330:300,fs=n?15:13,m={l:n?48:52,r:n?14:24,t:30,b:44},{xs,ys}=frame(W,H,m,[1,4.5],[.6,.8]);
 let s=`<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Recruitment threshold against incumbent strength">`;
 s+=`<rect class="band" x="${m.l}" y="${ys(.7313921)}" width="${W-m.l-m.r}" height="${ys(.705)-ys(.7313921)}"/>`;
 s+=axes(W,H,m,xs,ys,n?[1,2,3,4]:[1,1.5,2,2.5,3,3.5,4,4.5],[.6,.65,.7,.75,.8],v=>v,v=>v.toFixed(2),'incumbent strength '+it('r'),'posterior that the class is H',fs);
 s+=marks(xs,m,H,fs,true);
 const p=[];for(let i=0;i<=240;i++){const r=1+3.5*i/240;p.push(xs(r).toFixed(1)+','+ys(tau(r)).toFixed(1));}
 s+=`<polyline class="l1" points="${p.join(' ')}"/><line class="l3" x1="${m.l}" x2="${W-m.r}" y1="${ys(.7310586)}" y2="${ys(.7310586)}"/><line class="l2" x1="${m.l}" x2="${W-m.r}" y1="${ys(.725)}" y2="${ys(.725)}"/>`;
 [[3,.705],[3.6,.7313921]].forEach(([r,y])=>s+=`<circle class="dot1" cx="${xs(r)}" cy="${ys(y)}" r="4"/>`);
 s+=`<text class="lab c1t" x="${xs(n?1.55:1.6)}" y="${ys(n?.672:.668)}" font-size="${fs}">${it('τ')}(${it('r')})</text>`;
 s+=`<text class="lab c3t" x="${xs(4.45)}" y="${ys(.7310586)-6}" text-anchor="end" font-size="${fs}">paper ${it('M')} = 0.7311</text>`;
 s+=`<text class="lab c2t" x="${xs(n?1.08:1.15)}" y="${ys(.725)+fs+2}" font-size="${fs}">calibration A: ${it('M')} = 0.725</text>`;
 return s+'</svg>';}
function chartEntry(n){const W=n?420:680,H=n?340:300,fs=n?15:13,m={l:n?48:52,r:n?14:24,t:30,b:44},{xs,ys}=frame(W,H,m,[1,4],[.2,.6]);
 const Ei=r=>rho+(1-rho)*b*Dm(r)/(2*k);
 let s=`<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Equilibrium entry against incumbent strength">`;
 s+=`<rect class="band" x="${xs(rA)}" y="${m.t}" width="${xs(rN)-xs(rA)}" height="${H-m.t-m.b}"/>`;
 s+=axes(W,H,m,xs,ys,n?[1,2,3,4]:[1,1.5,2,2.5,3,3.5,4],[.2,.3,.4,.5,.6],v=>v,v=>v.toFixed(1),'incumbent strength '+it('r'),'probability of entry',fs);
 s+=marks(xs,m,H,fs,false);
 s+=`<line class="l2" x1="${xs(1)}" x2="${xs(rN)}" y1="${ys(.25)}" y2="${ys(.25)}"/><circle class="dot2" cx="${xs(rN)}" cy="${ys(.25)}" r="3.5"/>`;
 const p=[];for(let i=0;i<=60;i++){const r=rA+(rF-rA)*i/60;p.push(xs(r).toFixed(1)+','+ys(Ei(r)).toFixed(1));}p.push(xs(rC).toFixed(1)+','+ys(EA).toFixed(1));
 s+=`<polyline class="l1" points="${p.join(' ')}"/><line class="l1d" x1="${xs(rC)}" x2="${xs(rC)}" y1="${ys(EA)}" y2="${ys(.25)}"/><line class="l1" x1="${xs(rC)}" x2="${xs(4)}" y1="${ys(.25)}" y2="${ys(.25)}"/><circle class="dot1" cx="${xs(rA)}" cy="${ys(Ei(rA))}" r="3.5"/>`;
 [[1.2,.25],[3,.522757],[3.6,.25]].forEach(([r,y])=>s+=`<circle class="hol3" cx="${xs(r)}" cy="${ys(y)}" r="5.5"/>`);
 [[1.55,.545053],[1.6,.548756],[1.65,.551361]].forEach(([r,y])=>s+=`<rect class="dia3" x="${xs(r)-3.5}" y="${ys(y)-3.5}" width="7" height="7" transform="rotate(45 ${xs(r)} ${ys(y)})"/>`);
 s+=`<text class="lab c1t" x="${xs(2.55)}" y="${ys(EA)-9}" text-anchor="middle" font-size="${fs}">informative: 37/68 = 0.544</text>`;
 s+=`<text class="lab c2t" x="${xs(1.03)}" y="${ys(.25)-8}" font-size="${fs}">no informed trade</text>`;
 s+=`<text class="lab mut" x="${(xs(rA)+xs(rN))/2}" y="${ys(.375)}" text-anchor="middle" font-size="${fs-1}">both</text>`;
 return s+'</svg>';}
function chartResearch(n){const W=n?420:680,H=n?330:290,fs=n?15:13,m={l:n?48:52,r:n?14:24,t:30,b:44},{xs,ys}=frame(W,H,m,[1.3,1.9],[.2,.6]);
 const a=1/40,lc=6/17,rRec=1.51180346,rCap=1.67776618;
 const lamR=r=>{const d=Dm(r),B=4*a+k+d;return(-B+Math.sqrt(B*B+8*a*(d-2*k)))/(4*a);};
 const ER=r=>0.5+lamR(r)/8,Ei=r=>rho+(1-rho)*b*Dm(r)/(2*k);
 let s=`<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Entry with costly research at intermediate strengths">`;
 s+=axes(W,H,m,xs,ys,n?[1.3,1.5,1.7,1.9]:[1.3,1.4,1.5,1.6,1.7,1.8,1.9],[.2,.3,.4,.5,.6],v=>v.toFixed(1),v=>v.toFixed(1),'incumbent strength '+it('r'),'probability of entry',fs);
 [1.55,1.6,1.65].forEach(r=>s+=`<line class="vd" x1="${xs(r)}" x2="${xs(r)}" y1="${m.t}" y2="${H-m.b}"/>`);
 s+=`<line class="l2" x1="${xs(1.3)}" x2="${xs(rN)}" y1="${ys(.25)}" y2="${ys(.25)}"/><circle class="dot2" cx="${xs(rN)}" cy="${ys(.25)}" r="3.5"/>`;
 const q=[];for(let i=0;i<=40;i++){const r=rA+(rF-rA)*i/40;q.push(xs(r).toFixed(1)+','+ys(Ei(r)).toFixed(1));}q.push(xs(1.9).toFixed(1)+','+ys(EA).toFixed(1));
 s+=`<polyline class="l1d" points="${q.join(' ')}"/>`;
 const p=[];for(let i=0;i<=80;i++){const r=rRec+(rCap-rRec)*i/80;p.push(xs(r).toFixed(1)+','+ys(ER(r)).toFixed(1));}p.push(xs(1.9).toFixed(1)+','+ys(EA).toFixed(1));
 s+=`<polyline class="l1" points="${p.join(' ')}"/>`;
 [1.55,1.6,1.65].forEach(r=>s+=`<circle class="dot1" cx="${xs(r)}" cy="${ys(ER(r))}" r="4"/>`);
 [[1.55,.545053],[1.6,.548756],[1.65,.551361]].forEach(([r,y])=>s+=`<rect class="dia3" x="${xs(r)-3.5}" y="${ys(y)-3.5}" width="7" height="7" transform="rotate(45 ${xs(r)} ${ys(y)})"/>`);
 s+=`<text class="lab c1t" x="${xs(1.89)}" y="${ys(EA)+fs+12}" text-anchor="end" font-size="${fs}">research at the cap</text>`;
 s+=`<text class="lab c2t" x="${xs(1.31)}" y="${ys(.25)-8}" font-size="${fs}">no research</text>`;
 return s+'</svg>';}
function draw(){[['ch-tau',chartTau],['ch-entry',chartEntry],['ch-research',chartResearch]].forEach(([id,f])=>{const el=document.getElementById(id);if(!el)return;const n=(el.clientWidth||700)<520;if(el.dataset.n!==String(n)){el.innerHTML=f(n);el.dataset.n=String(n);}});}
draw();addEventListener('resize',draw);
})();
