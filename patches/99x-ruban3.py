# -*- coding: utf-8 -*-
"""Lot 35 — le ruban : concurrents vivants, mi-parcours et clôture en cinq secondes.

Constats (captures 380 px du lot 34 et lecture du code) :
  1. `rivalTapes()` appelle `rivRet(j,t)` dans un try/catch muet — et `rivRet` n'existe pas.
     ReferenceError avalée, g = 0 : pendant tout le trimestre, les quatre concurrents restent
     à plat et ne bougent qu'à la clôture. C'était exactement la demande non tenue.
  2. Leurs pastilles s'empilent en colonne au bord droit, cachées par le découpage tant que le
     dévoilement n'y est pas arrivé ; traits à 42 % d'opacité, 1,1 px : peu lisibles.
  3. Mi-parcours : aucun graphique propre. Clôture : ruban statique, résultat affiché d'emblée.
  4. Le tracé des dépêches dure 5 s mais le texte (`.evhold`) paraît à 3 s.
  5. Avec les écussons assortis au nom (lot 34), le joueur peut porter le même écusson qu'un
     concurrent (sommet, clé de voûte, faucon, étoile) : sa pastille doit se distinguer.

Ce que fait le lot :
  - `rivRet(j,t,q)` : P&L d'un concurrent à l'instant t, **pur** (hash32/prng32, aucun tirage
    de `rng`, donc aucun flux nommé décalé). Même forme que `rivalReturns` sans le terme
    idiosyncratique, que la clôture révèle : le trimestre les voit suivre les facteurs
    réalisés, la clôture les pose sur leur vrai résultat par un dernier segment.
  - `tapeTick` retient l'instant t de chaque segment (`S.tape.ts`) et le début du trimestre
    (`S.tape.q0`) : les concurrents avancent segment pour segment avec le joueur, et le
    dernier segment de clôture est commun (18 points), donc les courbes restent alignées.
  - Pastilles des concurrents hors découpage, qui suivent leur courbe pendant le dévoilement ;
    traits plus épais et plus opaques ; pastille du joueur plus grande, cerclée de blanc.
  - `opt.draw` : 3 s pour les dépêches (aligné sur `.evhold`), 5 s au mi-parcours et à la
    clôture. Compteur synchronisé sur la tête du tracé (`data-vals`, `theatre()`).
  - Mi-parcours et clôture : grand ruban rejoué depuis le début du trimestre en 5 s, résultat
    révélé ensuite (`.thold`, jamais combinée à `.fade` — piège du lot 26). Un toucher sur
    l'écran saute l'animation. « Mouvement réduit » : tout visible d'emblée.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
def between(a,b):
    assert e.s.count(a)==1,'debut ambigu %r'%a[:60]
    i=e.s.index(a); j=e.s.index(b,i); return e.s[i:j]

# ── 1. tapeTick : instants des segments, début du trimestre ─────────────────────
e.rep("  S.tape={y:yk,q:S.q,pts,seg:0};\n }\n const tgt=y.now,last=S.tape.pts[S.tape.pts.length-1];",
      "  S.tape={y:yk,q:S.q,pts,seg:0,q0:pts.length-1,ts:[]};\n }\n const tgt=y.now,last=S.tape.pts[S.tape.pts.length-1];")
e.rep("""  bridgePts(last,tgt,TAPEM,hash32('tapeq'+S.q+'_'+(S.tape.seg++),S.seed),tapeVol(TAPEM))
    .forEach(x=>S.tape.pts.push(x));
  if(S.tape.pts.length>3000){const cut=S.tape.pts.length-3000;
    S.tape.pts.splice(0,cut);S.tape.from=Math.max(0,S.tape.from-cut)}""",
"""  bridgePts(last,tgt,TAPEM,hash32('tapeq'+S.q+'_'+(S.tape.seg++),S.seed),tapeVol(TAPEM))
    .forEach(x=>S.tape.pts.push(x));
  (S.tape.ts=S.tape.ts||[]).push(qElapsed());   /* les concurrents avancent au même instant */
  if(S.tape.pts.length>3000){const cut=S.tape.pts.length-3000;
    S.tape.pts.splice(0,cut);S.tape.from=Math.max(0,S.tape.from-cut);S.tape.q0=Math.max(0,(S.tape.q0||0)-cut)}""")

# ── 2. clôture : le dernier segment est toujours posé (18 points), concurrents alignés ──
e.rep("""  if(Math.abs(tgt-last)>0.02){
   S.tape.from=S.tape.pts.length-1;
   bridgePts(last,tgt,18,hash32('settle'+S.q,S.seed),tapeVol(18)*0.5).forEach(z=>S.tape.pts.push(z));
  }""",
"""  /* toujours posé, même minuscule : les concurrents font le même dernier pas, sur 18 points */
  S.tape.from=S.tape.pts.length-1;S.tape.settled=S.q;   /* avant S.q++ : c'est le trimestre du ruban */
  bridgePts(last,tgt,18,hash32('settle'+S.q,S.seed),tapeVol(18)*(Math.abs(tgt-last)>0.02?0.5:0.1)).forEach(z=>S.tape.pts.push(z));""")

# ── 3. concurrents : rivRet réel et courbes alignées sur celle du joueur ────────
old=between("function rivalTapes(){","function tapeBand(){")
e.rep(old,"""/* P&L d'un concurrent à l'instant t du trimestre q. Pur : aucun tirage de rng. Même forme
   que rivalReturns (adresse sur les facteurs réalisés), sans le bruit propre, que la clôture
   révèle. */
function rivRet(j,t,q){
 const r=S.rivals&&S.rivals[j];if(!r||!S.f||!S.f.length)return 0;
 let e=0;for(let k=0;k<K;k++){const u=prng32(hash32('rivk'+j+'_'+q+'_'+k,S.seed))();
  e+=(u<r.skill?1:-1)*Math.sign(S.f[k]||1)*S.f[k]}
 return t*((r.vol/2)*(0.70*e/2)-0.008);
}
function rivalTapes(){
 if(!S.rivals||!S.tape)return [];
 const tq=S.tape.q,y0=S.tape.y,closed=S.q>tq&&S.tape.settled===tq;
 const ts=S.tape.ts&&S.tape.ts.length?S.tape.ts
   :Array.from({length:S.tape.seg||0},(_,k)=>(k+1)/Math.max(1,S.tape.seg)*qElapsed());   /* sauvegarde d'avant le lot 35 */
 return S.rivals.map((r,j)=>{
  const pts=[100];let v=1;
  for(let i=y0;i<tq;i++){const g=(r.hist&&r.hist[i])||0,nv=v*(1+g);
   bridgePts(v*100,nv*100,TAPEM,hash32('riv'+j+'_'+i,S.seed),tapeVol(TAPEM)*0.30).forEach(z=>pts.push(z));v=nv}
  /* trimestre en cours : un segment par segment du joueur, au même instant t */
  let last=v*100;
  ts.forEach((t,k)=>{const nv=v*(1+rivRet(j,t,tq))*100;
   bridgePts(last,nv,TAPEM,hash32('rivq'+j+'_'+tq+'_'+k,S.seed),tapeVol(TAPEM)*0.26).forEach(z=>pts.push(z));last=nv});
  /* clôture : leur vrai résultat, bruit propre compris, sur le même dernier pas que vous */
  if(closed){const nv=v*(1+((r.hist&&r.hist[tq])||0))*100;
   bridgePts(last,nv,18,hash32('rivs'+j+'_'+tq,S.seed),tapeVol(18)*0.3).forEach(z=>pts.push(z))}
  return {nm:r.nm,crest:RIVCREST[j%4],pts};
 });
}
""")

# ── 4. tapeSvg : pastilles qui suivent leur courbe, durée réglable, compteur ────
old=between("function tapeSvg(p,from,opt){","/* Courbes des concurrents sur la même fenêtre.")
new=r"""function tapeSvg(p,from,opt){
 opt=opt||{};
 const W=320,H=opt.h||78,pad=6,n=p.length,rv=opt.rivals||[];
 /* échelle symétrique : le zéro est l'axe, toujours au milieu */
 let m=1e-6;p.forEach(v=>m=Math.max(m,Math.abs(v-100)));
 rv.forEach(r=>r.pts.forEach(v=>m=Math.max(m,Math.abs(v-100))));
 m*=1.18;
 const lo=100-m,hi=100+m;
 const x=i=>pad+i*(W-2*pad)/Math.max(1,n-1),y=v=>H-pad-(v-lo)/(hi-lo)*(H-2*pad);
 const y0=y(100),id='tp'+(NGID++);
 const f=n=>n.toFixed(1);
 let body='';
 tapePieces(p,x,y,100).forEach(s=>{
  const c=s.up?TAPE_UP:TAPE_DN,pts=s.pts.map(q=>f(q[0])+','+f(q[1])).join(' ');
  body+=`<path d="M${f(s.pts[0][0])},${f(y0)} L${pts} L${f(s.pts[s.pts.length-1][0])},${f(y0)}Z" fill="${c}" opacity=".20"/>`
      +`<polyline points="${pts}" fill="none" stroke="${c}" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"/>`;
 });
 const base=`<line x1="0" y1="${f(y0)}" x2="${W}" y2="${f(y0)}" stroke="#5B6E8C" stroke-width="1"/>`;
 /* un grand ruban rejoue aussi le premier trimestre de l'année, qui part de l'indice 0 */
 const anim=opt.anim&&from<n-1&&(from>0||(opt.zero&&from===0)),DRAW=opt.draw||3,NS=40;
 const at=j=>Math.round(from+(n-1-from)*j/NS);        /* indice du joueur à l'image j */
 /* concurrents : trait de la couleur de leur écusson, pastille qui suit la courbe */
 let riv='',rmk='';const used=[];
 rv.forEach((r,j)=>{
  const q=r.pts,cr=r.crest!==undefined?r.crest:RIVCREST[j%4],col=CRESTS[cr%CRESTS.length].a;
  const qi=i=>q[Math.min(q.length-1,Math.max(0,Math.round(i*(q.length-1)/Math.max(1,n-1))))];
  const pts=q.map((v,i)=>f(x(i*(n-1)/Math.max(1,q.length-1)))+','+f(y(v))).join(' ');
  riv+=`<polyline points="${pts}" fill="none" stroke="${col}" stroke-width="1.5" opacity=".72" stroke-linejoin="round"/>`;
  const ex=x(n-1),ey0=y(q[q.length-1]);let ey=ey0;
  /* on écarte les pastilles qui se chevauchent à l'arrivée ; l'écart est gardé pendant la course */
  /* décalage alterné, au-dessus puis au-dessous, plutôt qu'une colonne qui dévale */
  for(let t=1;used.some(v=>Math.abs(v-ey)<11)&&t<12;t++)ey=ey0+(t%2?1:-1)*11*Math.ceil(t/2);
  ey=Math.max(8,Math.min(H-8,ey));used.push(ey);
  const mk=crestMark(cr,ex,ey,5.8);
  rmk+=anim?`<g><animateTransform attributeName="transform" type="translate" dur="${DRAW}s" fill="freeze"
    values="${Array.from({length:NS+1},(_,k)=>f(x(at(k))-ex)+' '+f(y(qi(at(k)))-ey0)).join(';')}"/>${mk}</g>`:mk;
 });
 /* l'écusson du fonds marque la tête : plus grand, cerclé de blanc, pour ne jamais se
    confondre avec un concurrent qui porterait le même */
 const hx=x(n-1),hy=y(p[n-1]),myC=S&&S.crest!==undefined?S.crest:0;
 const me=`<circle cx="${f(hx)}" cy="${f(hy)}" r="8.6" fill="none" stroke="#F3EEE4" stroke-width="1.5"/>${crestMark(myC,hx,hy,7)}`;
 const vals=anim?Array.from({length:NS+1},(_,k)=>p[at(k)]):[p[n-1]];
 const dv=` data-vals="${vals.map(v=>v.toFixed(2)).join(';')}" data-dur="${anim?DRAW:0}"`;
 if(!anim){
  const head=`<g><animateTransform attributeName="transform" type="translate" dur="1.9s" repeatCount="indefinite"
    values="0 0;${f(-hx*0.14)} ${f(-hy*0.14)};0 0"/>
   <g><animateTransform attributeName="transform" type="scale" dur="1.9s" repeatCount="indefinite"
     values="1 1;1.14 1.14;1 1"/>${me}</g></g>`;
  return `<svg class="navc" viewBox="0 0 ${W} ${H}" aria-hidden="true"${dv}>${base}${riv}${body}${rmk}${head}</svg>`;
 }
 /* la fenêtre s'élargit à droite : la géométrie ne bouge pas, seul le dévoilement avance */
 const x0=x(from),id2='c'+id;
 return `<svg class="navc" viewBox="0 0 ${W} ${H}" aria-hidden="true"${dv}>
  <defs><clipPath id="${id2}" clipPathUnits="userSpaceOnUse">
   <rect x="0" y="-${H*4}" height="${H*9}" width="${f(x0)}">
    <animate attributeName="width" from="${f(x0)}" to="${W}" dur="${DRAW}s" fill="freeze"/></rect>
  </clipPath></defs>
  ${base}<g clip-path="url(#${id2})">${riv}${body}</g>${rmk}
  <g><animateTransform attributeName="transform" type="translate" dur="${DRAW}s" fill="freeze"
    values="${Array.from({length:NS+1},(_,k)=>f(x(at(k))-hx)+' '+f(y(p[at(k)])-hy)).join(';')}"/>${me}</g></svg>`;
}
/* Le compteur d'un grand ruban suit la tête du tracé, image par image ; un toucher sur
   l'écran saute l'animation et révèle ce qui attendait (.thold). */
function theatre(root){
 if(!root)return;
 const fmt=v=>(v>=100?'+':'−')+dec(Math.abs(v-100),1)+'\u00a0%';
 root.querySelectorAll('.tape').forEach(tp=>{
  const sv=tp.querySelector('svg[data-vals]'),c=tp.querySelector('.cnt');if(!sv||!c)return;
  const vals=sv.dataset.vals.split(';').map(Number),dur=(+sv.dataset.dur||0)*1000,t0=Date.now(),suf=c.dataset.suf||'';
  const put=v=>{c.textContent=fmt(v)+suf;c.className='cnt '+(v>=100?'pos-g':'neg-g')};
  /* borné en nombre d'images : une horloge figée (harnais, onglet suspendu) ne boucle pas */
  const kmax=Math.ceil(dur/60)+10;
  const tick=k=>{if(!c.isConnected)return;
   const u=dur?Math.min(1,(Date.now()-t0)/dur):1;
   if(root.classList.contains('skip')||u>=1||k>kmax){put(vals[vals.length-1]);return}
   put(vals[Math.round(u*(vals.length-1))]);setTimeout(()=>tick(k+1),60)};
  tick(0);
 });
 root.addEventListener('click',()=>{root.classList.add('skip');
  root.querySelectorAll('svg').forEach(s=>{try{s.setCurrentTime(60)}catch(err){}})},{once:true});
}
"""
e.rep(old,new)

# ── 5. dépêches : 3 s, comme .evhold ───────────────────────────────────────────
e.rep("${tapeSvg(p,S.tape.from||0,{anim:1,rivals:rivalTapes()})}</div>`;",
      "${tapeSvg(p,S.tape.from||0,{anim:1,draw:3,rivals:rivalTapes()})}</div>`;")
# le ruban du bandeau cède la place au grand ruban au mi-parcours
e.rep("</div>${(S.phase==='events'&&S.live)?tapeBand():ticker()}</div>`;",
      "</div>${(S.phase==='events'&&S.live&&!S.bigTape)?tapeBand():ticker()}</div>`;")
e.rep("function stepEvents(){\n save('stepEvents');","function stepEvents(){\n S.bigTape=false;\n save('stepEvents');")

# ── 6. CSS : révélation différée, saut, mouvement réduit ─────────────────────────
e.rep("@media (prefers-reduced-motion:reduce){.evhold{opacity:1;pointer-events:auto;animation:none}}",
      "@media (prefers-reduced-motion:reduce){.evhold{opacity:1;pointer-events:auto;animation:none}}\n"
      "/* grand ruban : ce qui attend la fin du tracé. Jamais sur un élément .fade (voir .evhold) */\n"
      ".thold{opacity:0;pointer-events:none;animation:evshow .6s ease-out 5s forwards}\n"
      ".skip .thold{animation:none;opacity:1;pointer-events:auto}\n"
      ".tape.big .tapehead b{font-size:17px}\n"
      "@media (prefers-reduced-motion:reduce){.thold{opacity:1;pointer-events:auto;animation:none}}")

# ── 7. resultCard : un bloc avant la carte, et la carte qui attend ──────────────
e.rep("""app.innerHTML=statusBar()+`<div class="evwrap fade"><div class="kicker">${kick}</div>
  <div class="rescard"><h3>${title}</h3>""","""const hold=extra&&extra.hold?' thold':'';
 app.innerHTML=statusBar()+`<div class="evwrap fade"><div class="kicker">${kick}</div>${(extra&&extra.pre)||''}
  <div class="rescard${hold}"><h3>${title}</h3>""")
e.rep("""  <button class="cta" id="rgo">${btn}</button></div>`;
 document.getElementById('rgo').onclick=()=>{next();window.scrollTo(0,0)};window.scrollTo(0,0);""",
"""  <button class="cta${hold}" id="rgo">${btn}</button></div>`;
 document.getElementById('rgo').onclick=()=>{next();window.scrollTo(0,0)};window.scrollTo(0,0);
 if(hold)theatre(app.querySelector('.evwrap'));   /* racine propre à l'écran : ses écouteurs meurent avec lui */""")

# ── 8. mi-parcours : le trimestre rejoué en 5 s, puis le verdict ─────────────────
e.rep("""  "Poursuivre le trimestre",stepEvents);   /* le ruban est déjà à l'écran : pas de doublon */""",
"""  "Poursuivre le trimestre",stepEvents,midTape());""")
e.rep("function screenMidMark(){","""function midTape(){
 try{tapeTick()}catch(err){return {}}
 const p=S.tape&&S.tape.pts||[];if(p.length<3)return {};
 S.bigTape=true;refreshStatus();   /* le petit ruban du bandeau s'efface : pas de doublon */
 return {hold:1,pre:`<div class="tape big" style="margin:4px 0 14px"><div class="tapehead"><span>T${S.q+1} JUSQU'ICI · DEPUIS JANVIER</span>
   <b class="cnt">—</b></div>
   ${tapeSvg(p,S.tape.q0||0,{h:150,anim:1,draw:5,zero:1,rivals:rivalTapes()})}</div>`};
}
function screenMidMark(){""")

# ── 9. clôture : le trimestre rejoué en 5 s, le résultat ensuite ────────────────
e.rep("""   <div class="big ${cls(o.qTotal)}">${sgn(o.qTotal,1)}</div>
   <div class="num ${cls(o.qTotal)}" style="font-size:18px;margin-top:4px">""","""   <div class="big thold ${cls(o.qTotal)}">${sgn(o.qTotal,1)}</div>
   <div class="num thold ${cls(o.qTotal)}" style="font-size:18px;margin-top:4px">""")
e.rep("""<div class="tape" style="margin-top:12px"><div class="tapehead">
    <span>LE TRIMESTRE, HEURE PAR HEURE</span><b class="${S.tape.pts[S.tape.pts.length-1]>=100?'pos-g':'neg-g'}">${sgnp((S.tape.pts[S.tape.pts.length-1]-100)/100,1)} DEPUIS JANVIER</b></div>
    ${tapeSvg(S.tape.pts,0,{h:132,rivals:rivalTapes()})}</div>`""","""<div class="tape big" style="margin-top:12px"><div class="tapehead">
    <span>LE TRIMESTRE · DEPUIS JANVIER</span><b class="cnt">—</b></div>
    ${tapeSvg(S.tape.pts,S.tape.q0||0,{h:150,anim:1,draw:5,zero:1,rivals:rivalTapes()})}</div>`""")
e.rep("""  ${warn.map(t=>`<div class="flag" style="margin-top:12px">${t}</div>`).join('')}
  <div class="block"><div class="blockhead"><h2>La concurrence</h2>""","""  <div class="thold">${warn.map(t=>`<div class="flag" style="margin-top:12px">${t}</div>`).join('')}
  <div class="block"><div class="blockhead"><h2>La concurrence</h2>""")
e.rep("""${lines.length?`<div class="block"><details><summary style="font-size:15px;color:var(--txt);font-weight:600">Par marché · rendement et contribution</summary>${byl}</details></div>`:''}  <button class="cta" id="nx">""",
"""${lines.length?`<div class="block"><details><summary style="font-size:15px;color:var(--txt);font-weight:600">Par marché · rendement et contribution</summary>${byl}</details></div>`:''}</div>
  <button class="cta" id="nx">""")
e.rep(" document.getElementById('nx').onclick=()=>{\n  if(S.over||S.q>=QT())"," theatre(app.querySelector('.pnlhead').parentElement);\n document.getElementById('nx').onclick=()=>{\n  if(S.over||S.q>=QT())")
e.done("lot 35 — ruban : concurrents vivants, mi-parcours et cloture theatraux")
