/* Bot « intelligent » : lit ce que le joueur voit (sources, lectures, intuition, tableaux des boutons)
   et joue une partie complète. Usage module : playGame({file,seed,prof,vol,size,univ,dur,bud:[e,r,s],policy}) */
const fs=require('fs');const {JSDOM,VirtualConsole}=require('jsdom');
const CACHE={};
const num=t=>parseFloat(String(t).replace('−','-').replace(',','.'));
function utilText(t){
  t=t.replace(/\s+/g,' ');let u=0;
  for(const m of t.matchAll(/(investisseurs|comité|confiance)\s*([+−-])\s*(\d+)/gi))u+=(m[2]==='+'?1:-1)*(+m[3]);
  for(const m of t.matchAll(/(\d+)\s*%\s*de (?:risque[^:]*:\s*)?([+−-])\s*(\d+(?:,\d+)?)\s*%/g))u+=8*(+m[1]/100)*(m[2]==='+'?1:-1)*num(m[3]);
  for(const m of t.matchAll(/sinon\s*([+−-])\s*(\d+(?:,\d+)?)\s*%/g)){const p=t.match(/(\d+)\s*%\s*de/);u+=8*(1-(p?+p[1]/100:0.5))*(m[1]==='+'?1:-1)*num(m[2])}
  for(const m of t.matchAll(/(^|[^\d])([+−-])(\d+(?:,\d+)?)\s*pb/g))u+=0.08*(m[2]==='+'?1:-1)*num(m[3]);
  for(const m of t.matchAll(/[Cc]oûts?[^×]{0,30}×\s*(\d+(?:,\d+)?)/g))u-=1.5*(num(m[1])-1);
  for(const m of t.matchAll(/[Cc]oûts?\s*−\s*(\d+)\s*%/g))u+=0.015*num(m[1]);
  if(/risque d'incident|fuite/.test(t))u-=0.5;
  return u;
}
/* lot 199 : risque de faillite. Le bot vise une trésorerie minimale après book (FLOORS, fraction de l'encours, commission
   de gestion du trimestre comprise) : la réserve sert aux ajustements du trimestre. En cours de trimestre, il n'exécute
   un ordre de dépêche que si la trésorerie reste ≥ 0 à la clôture attendue (trésorerie − coût + commission de gestion). */
/* lot 233 : équipe du bot par style [front, back] et réserve de caisse ; le flux, plus sobre (calibration : 30 parties par variante,
   [3,2] 57 % de survie / 16,4 M$, [2,1] 50 % / 5,5, [1,1] 60 % / 10,6, [1,0] 47 % / 5,1) */
const BUD0={syst:[3,2],fonda:[3,2],flux:[1,1]},RES0={flux:0.6};
const FLOORS={syst:0.02,fonda:0.02,flux:0.04},FLOORK=0;
/* lot 211 (lot D) : seuil de netteté du signal avant de réagir à une dépêche, par style (o.theta pour forcer) */
const THETA0={syst:0.8,fonda:0.4,flux:0};   /* FLOORK : échelle. Bot 206 : 0 (plancher retiré, garde conservée) — un bot moins prudent, exposé au risque de faillite */
function playGame(o){
  const file=o.file||'index.html';const html=CACHE[file]||(CACHE[file]=fs.readFileSync(file,'utf8'));
  const errs=[];const vc=new VirtualConsole();vc.on('jsdomError',e=>errs.push(String(e.message||e)));
  let x=o.seed*9301+49297;
  const dom=new JSDOM(html,{runScripts:'dangerously',url:'https://x.test/',pretendToBeVisual:true,virtualConsole:vc,
    beforeParse(w){w.scrollTo=()=>{};w.onerror=(m)=>errs.push('onerror:'+m);w.Math.random=()=>{x=(x*9301+49297)%233280;return x/233280};
      w.setInterval=()=>0;w.clearInterval=()=>{};w.setTimeout=f=>{try{f()}catch(e){errs.push('t:'+e.message)}return 0}}});
  const w=dom.window,d=w.document,$=s=>d.querySelector(s),click=el=>{try{el.click()}catch(e){errs.push('click:'+e.message)}};
  const cfg={prof:o.prof,vol:o.vol||'std',size:o.size||'mid',univ:o.univ||'com',dur:o.dur||'normal'};
  const FLOOR=o.floor!=null?o.floor:(FLOORS[o.prof]||0)*(o.fk!=null?o.fk:FLOORK);
  const THETA=o.theta!=null?{syst:o.theta,fonda:o.theta,flux:o.theta}:THETA0;   /* lot 199 */
  const budArg=o.bud||BUD0[o.prof];   /* lot 233 : équipe par style */   /* lot 92 : [front, back] ; ancien fichier : [salle, contrôle, recherche] */   /* lot 45 : sept crans, le standard est le cran 3 */const smart=!o.policy||o.policy==='smart',dumb=o.policy==='dumb';   /* dumb : book au hasard, choix au hasard */
  w.eval(`refreshStatus=function(){};toast=function(){};window.__plan=null;(function(){const E=evPlans;window.evPlans=function(){const r=E.apply(this,arguments);window.__plan=r;return r}})()`);
  if(o.probe)w.eval(o.probe);          /* sonde injectée dans la page, avant la partie */
  if(o.pre)w.eval(o.pre);   /* sonde injectée avant la partie (tools/expchk.js…) */
  const st={ev:0,follow:0,verified:0};let steps=0,done=false;
  while(steps++<4000&&!done){
    if($('#tutooff')){click($('#tutooff'));continue}
    if($('#again')){done=true;break}
    if($('#found')){click($('#found'));continue}
    if($('#go')&&$('#picks')){for(const k in cfg){const c=$(`.card[data-key="${k}"][data-id="${cfg[k]}"]`);if(c)click(c);else if(!['vol','univ','arch','desk'].includes(k))errs.push('carte absente '+k)}
      $('#sd').value=String(o.seed);click($('#go'));continue}
    const lv=$('#buds .lvl');
    if(lv){const nw=!!$('#buds .lvl[data-b="fo"]'),ids=nw?['fo','bo']:['exec','risk','res'],bud=budArg&&budArg.length===ids.length?budArg:(nw?[3,2]:[3,3,3]);let ch=false;
      /* lot 39 : onze crans, et les plus chers se verrouillent quand la caisse ne suit pas —
         on prend alors le cran le plus haut encore ouvert sous celui demandé */
      ids.forEach((b,i)=>{let e=null;
        const res=o.reserve!=null?o.reserve:(RES0[o.prof]!=null?RES0[o.prof]:0.35),okR=j=>j===0||w.eval(`(S.budPrev&&${j}<=S.budPrev['${b}'])||budgetBpIf('${b}',${j})*1e-4*budNav()<=Math.min(${1-res}*(mgrCash()+(S.qOps||0)),mgrCash()+(S.qOps||0)-${o.fbud===false?0:FLOOR}*S.nav)`);   /* lot 199 : l'équipe ne mange pas le plancher */   /* garde une réserve pour les ordres */
        for(let j=bud[i];j>=0;j--){const c=$(`#buds .lvl[data-b="${b}"][data-i="${j}"]`);if(c&&!c.disabled&&okR(j)){e=c;break}}
        if(e&&!e.classList.contains('on')){click(e);ch=true}});
      if(ch)continue}
    if($('#send')){
      w.eval(`(()=>{const smart=${smart};
        if(${dumb}){S.k=S.k.map((v,i)=>mktOpen(i)?Math.round((Math.random()*2-1)*Math.min(3,S.maxk)):0);return}
        /* lot 67 : plus de cible de volatilité — le bot intelligent choisit l'échelle de son book qui maximise
           le rendement attendu (profitBook : collatéral, impact, drain, accidents de levier compris) moins une
           aversion égale au drain de volatilité. Le « naïf » garde le book du modèle. */
        const best=raw=>{let bk=null,bu=-1e9;for(let a=0.1;a<=4.01;a+=0.1){const k=raw.map(z=>Math.max(-S.maxk,Math.min(S.maxk,Math.round(z*a))));
          const sg=riskShown(weights(k)).total,u=profitBook(k)-(${o.av===undefined?1:o.av}>0?0.5*sg*sg/4+tailExp(sg):0)-${o.av===undefined?1:o.av}*0.5*sg*sg/4;if(${o.lim===false?'false':'true'}&&typeof limVol==='function'&&pvol(weights(k))>limVol()*0.97&&bk)continue;if(u>bu){bu=u;bk=k}}return bk};
        if(!smart){const R=recoBook();S.k=R.k.map(v=>Math.max(-S.maxk,Math.min(S.maxk,Math.round(v))));return}
        if(S.prof==='syst'){const R=recoBook();const mx=Math.max(1e-9,...R.k.map(Math.abs));S.k=best(R.k.map(v=>v/mx));return}
        const {W,f:f0}=styleEst();const f=[...f0];
        if(S.hunch)f[S.hunch.k]+=(S.hunch.up?1:-1)*1.03;   /* lot 118 : intuition juste 80 % du temps (1,2 à 85 %) */
        const sc=INSTR.map((x,i)=>{let v=0;for(let k=0;k<K;k++)v+=x.b[k]*f[k]*Math.max(W.F,0.5);
          if(S.tcvEst)v+=0.24*W.T*S.tcvEst.t[i]+0.20*W.C*S.tcvEst.c[i]+0.18*W.V*S.tcvEst.v[i]*((S.prof==='fonda'&&S.cat&&S.cat.includes(i))?(typeof CATM!=='undefined'?CATM:2):1);
          v+=W.X*0.30*S.crowd[i];return v});
        const mx=Math.max(0.001,...sc.map(Math.abs));const raw=sc.map(v=>v/mx*3);
        S.k=best(raw.map(z=>z/3));})()`);
      /* lot 199 : plancher de trésorerie après book (risque de faillite). Le bot retire des ordres, les plus chers d'abord,
         jusqu'à ce que la trésorerie après paiement atteigne `floor` × encours : de quoi payer impacts, dépêches et accidents
         en cours de trimestre, sans dépôt de bilan à la clôture. Plancher par défaut : voir FLOORS. */
      w.eval(`(()=>{const fl=${FLOOR}*S.nav,tc0=liveTC();for(let g=0;g<600;g++){if(mgrCash()>=fl-1e-12||liveTC()<=0.5*tc0)break;   /* jamais moins de la moitié du book */let bi=-1,bv=0;
        for(let i=0;i<N;i++){const d=S.k[i]-S.k0[i];if(Math.abs(d)<1e-9)continue;const t=tcost(d,i).cost;if(t>bv){bv=t;bi=i}}
        if(bi<0)break;S.k[bi]-=Math.sign(S.k[bi]-S.k0[bi])}})()`);
      if($('#send').disabled&&$('#fitbook'))click($('#fitbook'));
      w.eval('window.__sps=(window.__sps||[]).concat(riskShown(weights(S.k)).total)');
      if($('#send').disabled){errs.push('book bloque');break}
      click($('#send'));continue}
    /* lot 208 : rivalité à 5 crans — utilité lue sur le panneau de chaque cran (comme les autres choix), coût déduit */
    const rvs=d.querySelectorAll('.rvstep');
    if(rvs.length&&$('#rvok')){let bu=-1e9,bj=-1;const nav=w.eval('S.nav*1000');
      rvs.forEach((b,j)=>{if(b.disabled)return;click(b);const t=($('#rvpan>.pcell.on')||$('#rvpan')||{}).textContent||'';   /* lot 224 */let u=utilText(t);
        const m=t.match(/Coût\s*([\d\s,]+)\s*(k\$|M\$)/);if(m){const v=parseFloat(m[1].replace(/\s/g,'').replace(',','.'))*(m[2]==='k$'?1e-3:1);u-=8*100*v/nav}
        if(!smart)u=Math.random();if(u>bu){bu=u;bj=j}});
      if(bj<0)bj=[...rvs].findIndex(b=>b.dataset.a==='none');st.rv=(st.rv||0)+1;click(rvs[bj]);click($('#rvok'));continue}
    /* lot 207 : dépêche à 5 crans — même utilité qu'avant, sur tous les crans ouverts ; clic sur le cran puis « Valider » */
    const evs=d.querySelectorAll('.evstep');
    if(evs.length&&$('#evok')){st.ev++;
      const ok=[];evs.forEach(b=>{ok[+b.dataset.i]=!b.disabled});   /* lot 214 : ordre d'affichage ≠ ordre des crans */
      let i=w.eval(`(()=>{const P=window.__plan,SC=S.sc;if(!P)return -1;const ph=[SC.ph,1-SC.ph];
        const lo=Math.min(S.lp,S.rc),beta=1+Math.max(0,(45-lo)/8);
        const U=P.map(o=>ph.reduce((a,p,s)=>a+p*(o.pay[s]*1e4*0.35+beta*(o.gz[s].lp)),0));
        if(${o.guard===false?'false':'true'}){const cash=mgrCash();P.forEach((o,j)=>{if((o.cost||0)>1e-12&&cash-o.cost<0)U[j]=-1e9})}
        const ok=${JSON.stringify(ok)};
        if(!${smart})return Math.random()<0.6?0:P.findIndex(o=>o.n===0);
        /* lot 211 (lot D) : seuil de netteté par style — z = (U − U_rien) / écart-type de cet écart entre les deux scénarios */
        const TH=${JSON.stringify(THETA)}[S.prof]||0,nn=P.findIndex(o=>o.n===0);
        const z=j=>{const d=ph.map((p,s)=>(P[j].pay[s]-P[nn].pay[s])*1e4*0.35+beta*(P[j].gz[s].lp-P[nn].gz[s].lp));const m=ph[0]*d[0]+ph[1]*d[1],sd=Math.abs(d[0]-d[1])*Math.sqrt(ph[0]*ph[1]);return sd>1e-9?m/sd:(m>0?9:-9)};
        let bi=nn;P.forEach((o,j)=>{if(ok[j]&&j!==nn&&z(j)>=TH&&U[j]>U[bi]+1e-9)bi=j});return bi})()`);
      if(i<0||!ok[i])i=+[...evs].find(b=>b.classList.contains('zr')).dataset.i;
      if(w.eval('S.sc&&S.sc.ver'))st.verified++;
      const nn=w.eval(`(window.__plan&&window.__plan[${i}])?window.__plan[${i}].n:0`);
      if(nn>0)st.follow++;if(nn<0)st.contra=(st.contra||0)+1;if(Math.abs(nn)===1)st.half=(st.half||0)+1;
      click([...evs].find(b=>+b.dataset.i===i));click($('#evok'));continue}
    const ev=d.querySelectorAll('.choice.evopt');const evOk=[...ev].map(b=>!b.disabled);
    if(ev.length){st.ev++;
      let i=w.eval(`(()=>{const P=window.__plan,SC=S.sc;if(!P)return 1;const ph=[SC.ph,1-SC.ph];
        const lo=Math.min(S.lp,S.rc),beta=1+Math.max(0,(45-lo)/8);
        const U=P.map(o=>ph.reduce((a,p,s)=>a+p*(o.pay[s]*1e4*0.35+beta*(o.gz[s].lp+(typeof cf==='function'?0:o.gz[s].rc))),0));
        /* lot 199 : pas d'ordre qui mettrait la clôture attendue dans le rouge */
        if(${o.guard===false?'false':'true'}){const cash=mgrCash();P.forEach((o,j)=>{if((o.cost||0)>1e-12&&cash-o.cost<0)U[j]=-1e9})}
        if(${smart}){let bi=U[0]>U[1]?0:1;if(U[bi]<=-1e8)bi=P.length-1;return bi}
        return Math.random()<0.6?0:1})()`);
      if(!evOk[i])i=ev.length-1;
      if(w.eval('S.sc&&S.sc.ver'))st.verified++;
      if(i===0)st.follow++;click(ev[i]);continue}
    /* tuyau du prime broker (espérance positive) : le bot le prend */
    if($('.choice[data-tip="1"]')){st.tip=(st.tip||0)+1;click($('.choice[data-tip="1"]'));continue}
    /* accident de levier : le bot intelligent minimise perte du fonds + 2 × ce que paie sa trésorerie */
    /* lot 209 : accident à 5 crans + couverture — minimise perte attendue du fonds + 2 × trésorerie (garde) */
    if($('.tlstep')&&$('#tlok')){const bs=[...d.querySelectorAll('.tlstep')];
      const c=JSON.parse(w.eval(`JSON.stringify(tailOpts(S.tailEv).map(o=>o.fE+2*o.m-0.0005*(o.cA+o.cB)/2+(${o.guard===false?'false':'true'}&&o.m&&mgrCash()-o.m*S.nav<0?1e3:0)))`));
      let bi=-1,bc=1e9;bs.forEach((b,j)=>{const v=smart?c[j]:Math.random();if(!b.disabled&&v<bc){bc=v;bi=j}});
      if(bi<0)bi=2;st.tail=(st.tail||0)+1;st['t_'+bi]=(st['t_'+bi]||0)+1;click(bs[bi]);click($('#tlok'));continue}
    const chs=[...d.querySelectorAll('.choice')].filter(b=>!b.disabled);
    if(chs.length){let bi=chs.length-1;
      if(smart){let bu=-1e9;const cash=w.eval('S&&S.phase==="events"?mgrCash():null');chs.forEach((c,j)=>{let u=utilText(c.textContent);
        const m=/(?:Coût|vous)\s*[−-]?\s*([\d\s,]+)\s*(k\$|M\$)/.exec(c.textContent.replace(/\u00a0/g,' '));
        if(o.guard!==false&&m&&cash!=null){const v=parseFloat(m[1].replace(/\s/g,'').replace(',','.'))*(m[2]==='k$'?1e-6:1e-3);if(cash-v<0)u-=50}
        if(u>bu+1e-9){bu=u;bi=j}})}
      else bi=Math.floor(Math.random()*chs.length);
      click(chs[bi]);continue}
    const cc=d.querySelectorAll('.card.commgo');
    if(cc.length){click(cc[0]);continue}   /* annonce standard (lot 89 : premier cran) : un clic vaut validation */
    if(o.bon!=null&&$('#nx')){const b=$('.bnp[data-i="'+o.bon+'"]');if(b&&!b.classList.contains('on'))click(b)}
    let hit=false;for(const id of ['#ok','#go2','#rgo','#pgo','#nx','#go']){const b=$(id);if(b&&!b.disabled){click(b);hit=true;break}}
    if(hit)continue;
    const any=[...d.querySelectorAll('button.cta,button.buy')].filter(b=>!b.disabled);
    if(any.length){click(any[0]);continue}
    errs.push('bloqué');break;
  }
  const r=JSON.parse(w.eval(`JSON.stringify({score:(S.mgrFees-S.mgrCosts)*1000,fees:S.mgrFees*1000,costs:S.mgrCosts*1000,q:S.q,qtot:S.qtot,over:S.over,ret:S.idx-1,nav:S.nav*1000,bud:S.bud,lp:S.lp,rc:S.rc,feats:Object.keys(S.fl||{}).length,red:(S.cards||{}).r||0,yel:((S.cards||{}).log||[]).filter(x=>x.c==='jaune').length,tails:(S.tails||[]).length,sp:(window.__sps||[]).reduce((a,b)=>a+b,0)/Math.max(1,(window.__sps||[]).length),riv:S.rivals.map(r=>+(r.cum-1).toFixed(3))})`));
  if(o.collect){try{r.probe=JSON.parse(w.eval(o.collect))}catch(e){r.probe={err:e.message}}}
  w.close();
  return Object.assign(r,{cfg,floor:FLOOR,budIn:budArg,done,steps,nerr:errs.length,err:errs[0],st});
}
module.exports={playGame,utilText};
if(require.main===module){
  const a=process.argv.slice(2),g=k=>{const i=a.indexOf('--'+k);return i>=0?a[i+1]:null};
  const r=playGame({file:g('file')||'index.html',seed:+(g('seed')||1),prof:g('prof')||'fonda',vol:g('vol'),size:g('size'),univ:g('univ'),dur:g('dur'),
    bud:g('bud')?g('bud').split(',').map(Number):undefined,policy:g('policy')||'smart'});
  console.log(JSON.stringify(r));
}
