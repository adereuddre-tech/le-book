const fs=require('fs');const {JSDOM,VirtualConsole}=require('jsdom');
const a=process.argv.slice(2);const file=a[0],seed=+a[1]||1;
const opt=k=>{const i=a.indexOf('--'+k);return i>=0?a[i+1]:null};
const sage=a.includes('--sage');
const cfg={prof:opt('prof')||['syst','fonda','flux'][seed%3],vol:'std',size:opt('size')||'mid',univ:opt('univ')||'ext',dur:opt('dur')||'express'};
let errs=[];const vc=new VirtualConsole();vc.on('jsdomError',e=>errs.push('jsdom:'+(e.message||e)));
vc.on('error',e=>errs.push('console.error:'+e));
const html=fs.readFileSync(file,'utf8');
function mk(pre){return new JSDOM(html,{runScripts:'dangerously',url:'https://x.test/',pretendToBeVisual:true,virtualConsole:vc,
 beforeParse(w){w.scrollTo=()=>{};w.onerror=(m,s,l,c,e)=>errs.push('onerror:'+m+' @'+l+':'+c);
  let x=seed*9301+49297;w.Math.random=()=>{x=(x*9301+49297)%233280;return x/233280};
  w.setInterval=()=>0;w.setTimeout=(f)=>{try{f()}catch(e){errs.push('timeout:'+e.message)}return 0};w.clearInterval=()=>{};if(pre)w.localStorage.setItem('lebook_save_v2',pre);}})}
let dom=mk(null);
let w=dom.window,d=w.document;const $=s=>d.querySelector(s);
const RES=+(opt('resume')||0);let resumed=0;
const click=el=>{try{el.click()}catch(e){errs.push('click:'+e.message)}};
let r=seed*7+3;const rnd=()=>{r=(r*1103515245+12345)%2147483648;return r/2147483648};
const stats={events:0,follow:0,none:0,qs:0,screens:0};const plog=[];
let steps=0,done=false;
w.eval(`window.__chk=[];if(typeof evPlans!=="undefined")(function(){const R=resolveEvent;window.resolveEvent=function(ev,touched,o,imm,navB){
 const e0=Object.assign({},S.evImmG),n0=S.evLog.length,p=S.sc.p;const r=R.apply(this,arguments);
 const L=S.evLog[S.evLog.length-1];const si=/poursuivi/.test(document.querySelector('.rescard h3').textContent)?0:1;
 const dl=L.lp-e0.lp-o.gz[si].lp,dr=L.rc-e0.rc-o.gz[si].rc;
 const pnlShown=o.pay[si],tot=L.pnl;
 window.__chk.push({dl,dr,si,p,exp:imm+o.pay[si]*(S.nav? 1:1)});
 if(Math.abs(dl)>1e-6||Math.abs(dr)>1e-6)window.__bad=(window.__bad||0)+1;
 return r}})()`);
w.eval(`window.__v=[];window.__nav=0;window.__navbad=[];window.__red={};
(function(){const PQ=planQuarter;let n=0;window.planQuarter=function(){
  if(S.q>=1&&window.__forceRed){const id=REDC[n%REDC.length].id;n++;const keep=REDC.slice();REDC.length=0;REDC.push(keep.find(c=>c.id===id));S.redLast=null;
   S.redNext=redDraw(weights(S.k));REDC.length=0;keep.forEach(c=>REDC.push(c))}
  return PQ.apply(this,arguments)};
 const CO=commitOrders;window.commitOrders=function(){const sp=riskShown(weights(S.k)).total,id=S.redOn&&S.redC?S.redC.id:'-';
  window.__red[id]=(window.__red[id]||0)+1;
  const v=[];if(S.k.some((x,i)=>Math.abs(x)>kCap(i)))v.push('cap');if(id==='cap'&&S.k.some(x=>Math.abs(x)>2))v.push('cap2');
  if(id==='risk'&&sp>0.7*S.tgt+1e-9)v.push('risk');if(id==='noadd'&&sp>S.tgt+1e-9)v.push('noadd');if(id==='lines'&&S.k.filter(x=>x).length>4)v.push('lines');
  if(id==='budget'&&S.bud.risk<5)v.push('budget:'+S.bud.risk);if((id==='shut'||id==='class')&&S.redC.syms.some(sy=>S.k[IDX[sy]]))v.push('shut');
  if(Math.abs(S.maxk)>(S.capK||5))v.push('maxk');
  if(v.length)window.__v.push(S.q+':'+id+':'+v.join('/'));return CO.apply(this,arguments)};
 const RQ=resolveQuarter;window.resolveQuarter=function(){const id=S.redOn&&S.redC?S.redC.id:'-';const r=RQ.apply(this,arguments);
  if(id==='collat'&&!(S.colRes&&S.colRes.nm==='Collatéral renforcé'))window.__v.push('collat');return r};
})()`);
if(a.includes('--red'))w.eval('window.__forceRed=1');
const navChk=()=>{try{if(d.querySelector('#send')){const n=w.eval(`[...document.querySelectorAll('.seg button')].filter(b=>!b.disabled&&S.k[+b.dataset.i]!==+b.dataset.v&&(!segAfford(+b.dataset.i,+b.dataset.v)||Math.abs(+b.dataset.v)>kCap(+b.dataset.i))).length`);w.__aff=(w.__aff||0)+n;w.__affN=(w.__affN||0)+1;const L=[...d.querySelectorAll('.seg button:not([disabled])')];for(let z=0;z<3&&L.length;z++)click(L[Math.floor(rnd()*L.length)])}}catch(e){}try{const t=d.querySelector('#navtile');if(t){const e=w.eval('moneyB(navNow())');if(t.textContent!==e)w.__navbad.push(t.textContent+'≠'+e);w.__nav++}}catch(e){}};
const SIG=[];while(steps++<3000&&!done){navChk();
 if(steps%1===0){const h=(d.querySelector('h1,h2,h3')||{}).textContent||'?';const b=[...d.querySelectorAll('button')].filter(x=>!x.disabled).map(x=>x.id||x.className).join(',').slice(0,90);const sg=h+' :: '+b;if(SIG[SIG.length-1]!==sg)SIG.push(sg);if(SIG.length>400)SIG.shift()}
 const t=$('#tutooff');if(t){click(t);continue}
 if($('#again')){done=true;break}
 if($('#found')){click($('#found'));continue}
 if($('#go')&&$('#picks')){for(const k in cfg){const c=$(`.card[data-key="${k}"][data-id="${cfg[k]}"]`);if(c)click(c)}
  const sd=$('#sd');sd.value=String(seed);click($('#go'));continue}
 if($('#send')){w.eval(`try{const R=recoBook();S.k=R.k.map(v=>Math.max(-S.maxk,Math.min(S.maxk,Math.round(v))));drawRows();renderRisk();refreshSend()}catch(e){window.__e=e.message}`);
  if(w.__e){errs.push('reco:'+w.__e);w.__e=null}
  if($('#send').disabled&&$('#fitbook'))click($('#fitbook'));
  stats.qs++;if($('#send').disabled){errs.push('book bloque');break}click($('#send'));continue}
 const ev=d.querySelectorAll('.choice.evopt:not([disabled])');
 if(ev.length){stats.events++;
  const pl=w.eval(`JSON.stringify({p:S.sc.p,s:[...document.querySelectorAll('.choice.evopt')].map(b=>b.textContent.replace(/\\s+/g,' '))})`);
  plog.push(pl);
  if(RES&&stats.events===RES&&!resumed){resumed=1;const sv=w.localStorage.getItem('lebook_save_v2');dom=mk(sv);w=dom.window;d=w.document;
   const rb=d.querySelector('#resume');if(!rb){errs.push('pas de bouton reprendre');break}rb.click();stats.resumedTo=(d.querySelector('.evopt')?'dépêche':d.querySelector('.rescard')?'résultat':d.querySelector('h3')?d.querySelector('h3').textContent.slice(0,40):'?');continue}
  const i=sage?ev.length-1:Math.min(ev.length-1,rnd()<0.6?0:1);stats[i===0?'follow':'none']++;
  w.__lg0=w.eval('S.lp+"|"+S.rc');
  click(ev[i]);continue}
 const ch=d.querySelectorAll('.choice:not([disabled])');
 if(ch.length){click(ch[sage?ch.length-1:Math.floor(rnd()*ch.length)]);continue}
 const cc=d.querySelectorAll('.card.commgo');
 if(cc.length){click(cc[sage?1:Math.floor(rnd()*cc.length)]);continue}   /* annonce : un clic vaut validation */
 {const co=[...d.querySelectorAll('.coll:not([disabled])')],qk='c'+w.eval('S.q');if(co.length&&!sage&&w.__colq!==qk){w.__colq=qk;click(co[Math.floor(rnd()*co.length)])}}
 let hit=false;for(const id of ['#ok','#go2','#rgo','#pgo','#nx','#go']){const b=$(id);if(b&&!b.disabled){click(b);hit=true;break}}
 if(hit)continue;
 const any=[...d.querySelectorAll('button.cta,button.buy')].filter(b=>!b.disabled);
 if(any.length){click(any[0]);continue}
 errs.push('bloqué: '+d.body.textContent.slice(0,200));break;
}
const chk=w.eval('window.__chk')||[];const res={resumed,bad:w.eval('window.__bad||0'),npo:chk.filter(c=>c.si===0).length,pbar:chk.reduce((a,c)=>a+c.p,0)/Math.max(1,chk.length),seed,cfg,sage,done,steps,errs:errs.slice(0,5),nerr:errs.length,stats,over:w.eval('S&&S.over'),q:w.eval('S&&S.q'),nav:w.eval('S&&S.nav'),viol:w.eval('window.__v'),red:w.eval('window.__red'),navN:w.__nav,affBad:w.__aff||0,affN:w.__affN||0,navBad:(w.__navbad||[]).slice(0,3),xev:w.eval('(S.usedX||[]).length'),capK:w.eval('S.capK'),cards:w.eval('JSON.stringify(S.cards&&S.cards.log)')};
if(a.includes('--log'))res.plog=plog.slice(0,3);if(!done)res.sig=SIG.slice(-6);
console.log(JSON.stringify(res));
