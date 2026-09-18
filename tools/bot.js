/* Bot « intelligent » : lit ce que le joueur voit (sources, lectures, intuition, tableaux des boutons)
   et joue une partie complète. Usage module : playGame({file,seed,prof,vol,size,univ,dur,bud:[e,r,s],policy}) */
const fs=require('fs');const {JSDOM,VirtualConsole}=require('jsdom');
const CACHE={};
const num=t=>parseFloat(String(t).replace('−','-').replace(',','.'));
function utilText(t){
  t=t.replace(/\s+/g,' ');let u=0;
  for(const m of t.matchAll(/(investisseurs|comité)\s*([+−-])\s*(\d+)/gi))u+=(m[2]==='+'?1:-1)*(+m[3]);
  for(const m of t.matchAll(/(\d+)\s*%\s*de (?:risque[^:]*:\s*)?([+−-])\s*(\d+(?:,\d+)?)\s*%/g))u+=8*(+m[1]/100)*(m[2]==='+'?1:-1)*num(m[3]);
  for(const m of t.matchAll(/sinon\s*([+−-])\s*(\d+(?:,\d+)?)\s*%/g)){const p=t.match(/(\d+)\s*%\s*de/);u+=8*(1-(p?+p[1]/100:0.5))*(m[1]==='+'?1:-1)*num(m[2])}
  for(const m of t.matchAll(/(^|[^\d])([+−-])(\d+(?:,\d+)?)\s*pb/g))u+=0.08*(m[2]==='+'?1:-1)*num(m[3]);
  for(const m of t.matchAll(/[Cc]oûts?[^×]{0,30}×\s*(\d+(?:,\d+)?)/g))u-=1.5*(num(m[1])-1);
  for(const m of t.matchAll(/[Cc]oûts?\s*−\s*(\d+)\s*%/g))u+=0.015*num(m[1]);
  if(/risque d'incident|fuite/.test(t))u-=0.5;
  return u;
}
function playGame(o){
  const file=o.file||'index.html';const html=CACHE[file]||(CACHE[file]=fs.readFileSync(file,'utf8'));
  const errs=[];const vc=new VirtualConsole();vc.on('jsdomError',e=>errs.push(String(e.message||e)));
  let x=o.seed*9301+49297;
  const dom=new JSDOM(html,{runScripts:'dangerously',url:'https://x.test/',pretendToBeVisual:true,virtualConsole:vc,
    beforeParse(w){w.scrollTo=()=>{};w.onerror=(m)=>errs.push('onerror:'+m);w.Math.random=()=>{x=(x*9301+49297)%233280;return x/233280};
      w.setInterval=()=>0;w.clearInterval=()=>{};w.setTimeout=f=>{try{f()}catch(e){errs.push('t:'+e.message)}return 0}}});
  const w=dom.window,d=w.document,$=s=>d.querySelector(s),click=el=>{try{el.click()}catch(e){errs.push('click:'+e.message)}};
  const cfg={prof:o.prof,vol:o.vol||'std',size:o.size||'mid',univ:o.univ||'com',dur:o.dur||'normal'};
  const bud=o.bud||[1,1,1];const smart=o.policy!=='naive';
  w.eval(`refreshStatus=function(){};toast=function(){};window.__plan=null;(function(){const E=evPlans;window.evPlans=function(){const r=E.apply(this,arguments);window.__plan=r;return r}})()`);
  if(o.probe)w.eval(o.probe);          /* sonde injectée dans la page, avant la partie */
  const st={ev:0,follow:0,verified:0};let steps=0,done=false;
  while(steps++<4000&&!done){
    if($('#tutooff')){click($('#tutooff'));continue}
    if($('#again')){done=true;break}
    if($('#found')){click($('#found'));continue}
    if($('#go')&&$('#picks')){for(const k in cfg){const c=$(`.card[data-key="${k}"][data-id="${cfg[k]}"]`);if(c)click(c);else errs.push('carte absente '+k)}
      $('#sd').value=String(o.seed);click($('#go'));continue}
    const lv=$('#buds .lvl');
    if(lv){const ids=['exec','risk','res'];let ch=false;
      ids.forEach((b,i)=>{const e=$(`#buds .lvl[data-b="${b}"][data-i="${bud[i]}"]`);if(e&&!e.classList.contains('on')){click(e);ch=true}});
      if(ch)continue}
    if($('#send')){
      w.eval(`(()=>{const smart=${smart};
        if(!smart||S.prof==='syst'){const R=recoBook();S.k=R.k.map(v=>Math.max(-S.maxk,Math.min(S.maxk,Math.round(v))));return}
        const {W,f:f0}=styleEst();const f=[...f0];
        if(S.hunch)f[S.hunch.k]+=(S.hunch.up?1:-1)*1.2;
        const sc=INSTR.map((x,i)=>{let v=0;for(let k=0;k<K;k++)v+=x.b[k]*f[k]*Math.max(W.F,0.5);
          if(S.tcvEst)v+=0.24*W.T*S.tcvEst.t[i]+0.20*W.C*S.tcvEst.c[i]+0.18*W.V*S.tcvEst.v[i];
          v+=W.X*0.30*S.crowd[i];return v});
        const mx=Math.max(0.001,...sc.map(Math.abs));const raw=sc.map(v=>v/mx*3);
        const tg=S.tgt*0.95*(PROF().modelScale||1);let a=tg/Math.max(1e-9,pvol(weights(raw)));
        let k=raw.map(z=>Math.max(-S.maxk,Math.min(S.maxk,Math.round(z*a))));
        for(let it=0;it<8;it++){const v=pvol(weights(k));if(v<1e-9)break;const r=tg/v;if(r>0.95&&r<1.05)break;a*=r;k=raw.map(z=>Math.max(-S.maxk,Math.min(S.maxk,Math.round(z*a))))}
        S.k=k;})()`);
      if($('#send').disabled&&$('#fitbook'))click($('#fitbook'));
      if($('#send').disabled){errs.push('book bloque');break}
      click($('#send'));continue}
    const ev=d.querySelectorAll('.choice.evopt');
    if(ev.length){st.ev++;
      const i=w.eval(`(()=>{const P=window.__plan,SC=S.sc;if(!P)return 1;const ph=[SC.ph,1-SC.ph];
        const lo=Math.min(S.lp,S.rc),beta=1+Math.max(0,(45-lo)/8);
        const U=P.map(o=>ph.reduce((a,p,s)=>a+p*(o.pay[s]*1e4*0.35+beta*(o.gz[s].lp+o.gz[s].rc)),0));
        return ${smart}?(U[0]>U[1]?0:1):(Math.random()<0.6?0:1)})()`);
      if(w.eval('S.sc&&S.sc.ver'))st.verified++;
      if(i===0)st.follow++;click(ev[i]);continue}
    const chs=[...d.querySelectorAll('.choice')];
    if(chs.length){let bi=chs.length-1;
      if(smart){let bu=-1e9;chs.forEach((c,j)=>{const u=utilText(c.textContent);if(u>bu+1e-9){bu=u;bi=j}})}
      else bi=Math.floor(Math.random()*chs.length);
      click(chs[bi]);continue}
    const cc=d.querySelectorAll('.card.commgo');
    if(cc.length){click(cc[1]);continue}   /* annonce standard : un clic vaut validation */
    let hit=false;for(const id of ['#ok','#go2','#rgo','#pgo','#nx','#go']){const b=$(id);if(b&&!b.disabled){click(b);hit=true;break}}
    if(hit)continue;
    const any=[...d.querySelectorAll('button.cta,button.buy')].filter(b=>!b.disabled);
    if(any.length){click(any[0]);continue}
    errs.push('bloqué');break;
  }
  const r=JSON.parse(w.eval(`JSON.stringify({score:(S.mgrFees-S.mgrCosts)*1000,fees:S.mgrFees*1000,costs:S.mgrCosts*1000,q:S.q,qtot:S.qtot,over:S.over,ret:S.idx-1,nav:S.nav*1000,bud:S.bud,lp:S.lp,rc:S.rc,feats:Object.keys(S.fl||{}).length})`));
  if(o.collect){try{r.probe=JSON.parse(w.eval(o.collect))}catch(e){r.probe={err:e.message}}}
  w.close();
  return Object.assign(r,{cfg,budIn:bud,done,steps,nerr:errs.length,err:errs[0],st});
}
module.exports={playGame,utilText};
if(require.main===module){
  const a=process.argv.slice(2),g=k=>{const i=a.indexOf('--'+k);return i>=0?a[i+1]:null};
  const r=playGame({file:g('file')||'index.html',seed:+(g('seed')||1),prof:g('prof')||'fonda',vol:g('vol'),size:g('size'),univ:g('univ'),dur:g('dur'),
    bud:g('bud')?g('bud').split(',').map(Number):undefined,policy:g('policy')||'smart'});
  console.log(JSON.stringify(r));
}
