/* lot 209 (lot C) : accident de levier et appel de marge — part du book coupée sur 5 crans (0, 25, 50, 75, 100 %),
   plus la couverture payée par la trésorerie. 0 % : pile ou face (comme avant) ; 50 % : le prix sûr d'avant ;
   25 % : moitié pari, moitié coupe ; 75 et 100 % : plus d'impact, mais un comité rassuré et un book allégé.
   Chaque cran affiche exactement ce qui sera appliqué (perte du fonds, trésorerie, confiance, book). */
function tailOpts(te){const L=te.L,hA=0.5*L,hB=1.8*L,c50=0.8*L+Math.min(0.08,te.imp),G=te.good;
 const mix=(a,b,w)=>a*(1-w)+b*w;
 return [{id:'hold',x:0,fA:hA,fB:hB,cA:-2,cB:-10,m:0},
  {id:'cut25',x:0.25,fA:mix(hA,c50,0.5),fB:mix(hB,c50,0.5),cA:-3,cB:-7,m:0},
  {id:'cut',x:0.5,fA:c50,fB:c50,cA:-4,cB:-4,m:0},
  {id:'cut75',x:0.75,fA:c50+0.1*L,fB:c50+0.1*L,cA:-2,cB:-2,m:0},
  {id:'cut100',x:1,fA:c50+0.2*L,fB:c50+0.2*L,cA:0,cB:0,m:0},
  {id:'hedge',x:0,fA:0.5*L,fB:0.5*L,cA:-3,cB:-3,m:0.30*L}]
  .map(o=>Object.assign(o,{f:G?o.fA:o.fB,c:G?o.cA:o.cB,fE:(o.fA+o.fB)/2}))}
function screenTail(te){
 const ev=TAILEV[te.i]||TAILEV[0],O=tailOpts(te),nav=S.nav,L=te.L;
 const row=(a,b)=>`<div class="gzr"><span>${a}</span>${b}</div>`;
 const LAB={hold:ev.o[0],cut25:'Couper un quart du book',cut:ev.o[1],cut75:'Couper les trois quarts du book',cut100:'Tout solder',hedge:ev.o[2]};
 const kOf=o=>S.k.map(v=>o.x===0.5||o.x===1?Math.trunc(v*(1-o.x)):Math.sign(v)*Math.round(Math.abs(v)*(1-o.x)));   /* 50 % : règle d'avant ; 25 et 75 % : au plus proche */
 const body=o=>(o.fA!==o.fB||o.cA!==o.cB
   ?row('une chance sur deux',`<b class="neg-g">−${mm(o.fA*nav)} · confiance ${sd1(o.cA)}</b>`)+row('une chance sur deux',`<b class="neg-g">−${mm(o.fB*nav)} · confiance ${sd1(o.cB)}</b>`)
   :row('fonds',`<b class="neg-g">−${mm(o.f*nav)} · ${sgnp(-o.f,1)}</b>`)+row('confiance',`<b class="${cls(o.c)}">${o.c?sd1(o.c):'inchangée'}</b>`))
  +(o.m?row('votre trésorerie',`<b class="neg-g">−${mm(o.m*nav)}</b>`):'')
  +(o.x>0?row('book',`<b>positions × ${dec(1-o.x,2)}</b>`)+bkD(kOf(o),0,false):'');
 const CUT=O.findIndex(o=>o.id==='cut');
 app.innerHTML=statusBar()+`<div class="evwrap fade">
  <div class="evcard bad">${evHead(ev.who,'risk')}<h3>${ev.t}</h3><p>${ev.p}</p>
   <p class="note">${ev.mg?'Appel de marge':'Accident de levier'} : votre book tourne à ${pct(RQ(te.sp))} de risque. En dessous de ${dec(TAIL.x0*50,0)} %, il ne serait pas arrivé.</p></div>
  <p class="note" style="margin:12px 0 0">Part du book que vous coupez, ou couverture payée par votre trésorerie :</p>
  <div class="evsel" style="grid-template-columns:repeat(6,1fr)">${O.map((o,k)=>`<button class="evstep tlstep ${o.id==='hedge'?'zr':o.x===0?'up':'dn'}${k===CUT?' on':''}" data-t="${k}"><b>${o.id==='hedge'?'🛡':Math.round(o.x*100)}</b><small>${o.id==='hedge'?'couvrir':o.x===0?'tenir':'% coupé'}</small></button>`).join('')}</div>
  <div class="evpan" id="tlpan"></div><button class="cta" id="tlok" style="margin-top:10px">Valider</button></div>`;
 let sel=CUT;const pan=k=>{const o=O[k];document.getElementById('tlpan').innerHTML=`<div class="choice" style="cursor:default"><b>${LAB[o.id]}</b><span>${body(o)}</span></div>`;
  app.querySelectorAll('.tlstep').forEach(b=>b.classList.toggle('on',+b.dataset.t===k));sel=k};pan(CUT);
 app.querySelectorAll('.tlstep').forEach(b=>b.onclick=()=>pan(+b.dataset.t));
 const act=k=>{clearTimer();
  const o=O[k],loss=o.f*nav;
  S.nav-=loss;S.qIncM-=loss;
  if(o.m){S.mgrCosts+=o.m*nav;S.qTailMgr=(S.qTailMgr||0)+o.m*nav}
  if(o.x>0){const r0=typeof liveRet==='function'?liveRet():0;S.k=kOf(o);const r1=typeof liveRet==='function'?liveRet():0;S.qEvM=(S.qEvM||0)+(r0-r1)*S.navQ0}
  const g=gauge(o.c,0,`${ev.mg?'Appel de marge':'Accident de levier'} : ${ev.t}`);
  S.evLog.push({t:ev.t,pnl:-o.f,m:-loss,lp:g.lp,rc:g.rc});(S.tails=S.tails||[]).push({q:S.q,t:ev.t,f:o.f,id:o.id});
  S.tailDone=true;S.tailEv=0;try{refreshGain()}catch(err){}
  const res=o.id==='hold'?(te.good?'La tempête passe sans emporter le book. Cette fois.':'La tempête emporte tout ce qui dépasse.')
   :o.id==='cut25'?(te.good?'Un quart du book coupé, le reste a tenu.':'Un quart du book coupé, le reste a pris la tempête.')
   :o.id==='cut'?'Le book est coupé de moitié, au pire prix de la séance.':o.id==='cut75'?'Les trois quarts du book sont coupés, dans un marché qui fuit.'
   :o.id==='cut100'?'Tout est soldé. Le comité respire, le carnet d\'ordres moins.':'La couverture tient. Elle a coûté ce qu\'on vous a demandé.';
  app.innerHTML=statusBar()+`<div class="evwrap fade"><div class="evcard rescard ${o.f>0.05?'bad':''}"><h3>${res}</h3>
   <div class="kv"><span>Coût pour le fonds</span><b class="neg-g">−${mm(loss)} · ${sgnp(-o.f,1)}</b></div>
   ${o.m?`<div class="kv"><span>Payé par votre trésorerie</span><b class="neg-g">−${mm(o.m*nav)}</b></div>`:''}
   <div class="kv"><span>Confiance</span><b class="${cls(g.lp)}">${sd1(g.lp)}</b></div></div>
   <button class="cta" id="ok">Poursuivre le trimestre</button></div>`;
  document.getElementById('ok').onclick=()=>stepEvents();window.scrollTo(0,0);
 };
 document.getElementById('tlok').onclick=()=>act(sel);
 armTimer(()=>act(CUT),ev.mg?'sans choix : le prime broker liquide la moitié':'sans choix : le desk coupe la moitié du book');
}
