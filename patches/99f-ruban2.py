# -*- coding: utf-8 -*-
"""Lot 18 — le ruban : fenêtre qui s'élargit, zéro comme axe, concurrents, accueil.

- Plus de zoom ni de suivi. La géométrie est fixe, et le tracé se découvre de gauche à
  droite : la fenêtre s'élargit à droite à mesure que le trait progresse, en 5 s.
- Le zéro est l'axe des abscisses : l'échelle verticale est rendue symétrique autour de
  100, la ligne de base est donc toujours au milieu et sert de repère fixe.
- On n'anime que s'il s'est passé quelque chose : en dessous de 5 pb de variation, aucun
  point n'est ajouté et le ruban est rendu statique. Le graphique reste ancré.
- Les quatre concurrents sont tracés en traits fins estompés, une couleur chacun, avec une
  pastille à leur initiale au bout de leur courbe. Pendant le trimestre en cours leur
  résultat n'est pas connu : leur trait prolonge leur dernière clôture sans dérive, ce qui
  est la vérité — on ne sait pas encore ce qu'ils font.
- L'accueil montre une année complète tirée au hasard à chaque affichage, avec le même
  dessin et les mêmes concurrents que dans le jeu.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()

# ── couleurs et pastilles des concurrents ──
e.rep("""const TAPE_UP='#3FCF8E',TAPE_DN='#F2545B';""",
"""const TAPE_UP='#3FCF8E',TAPE_DN='#F2545B';
const RIVCOL=['#7C8FF0','#D9B06A','#A98CE0','#5FBFC4'];
function rivTag(nm){const w=String(nm||'').replace(/^(le|la|les|l')\\s+/i,'').split(/[\\s'’-]+/).filter(Boolean);
 return ((w[0]||'?')[0]+(w[1]?w[1][0]:'')).toUpperCase()}""")

# ── rendu : plus de zoom, zéro au centre, concurrents ──
e.rep(""" const W=320,H=opt.h||78,pad=5,n=p.length;
 let lo=Math.min(100,...p),hi=Math.max(100,...p);
 const sp=(hi-lo)||1;lo-=sp*0.14;hi+=sp*0.14;
 const x=i=>pad+i*(W-2*pad)/Math.max(1,n-1),y=v=>H-pad-(v-lo)/(hi-lo)*(H-2*pad);""",
""" const W=320,H=opt.h||78,pad=5,n=p.length,rv=opt.rivals||[];
 /* échelle symétrique : le zéro est l'axe, toujours au milieu */
 let m=1e-6;p.forEach(v=>m=Math.max(m,Math.abs(v-100)));
 rv.forEach(r=>r.pts.forEach(v=>m=Math.max(m,Math.abs(v-100))));
 m*=1.18;
 const lo=100-m,hi=100+m;
 const x=i=>pad+i*(W-2*pad)/Math.max(1,n-1),y=v=>H-pad-(v-lo)/(hi-lo)*(H-2*pad);""")
e.rep(""" const headC=p[n-1]>=100?TAPE_UP:TAPE_DN;
 const base=`<line x1="0" y1="${f(y0)}" x2="${W}" y2="${f(y0)}" stroke="#4A5C78" stroke-width="1" stroke-dasharray="2 3"/>`;""",
""" const headC=p[n-1]>=100?TAPE_UP:TAPE_DN;
 const base=`<line x1="0" y1="${f(y0)}" x2="${W}" y2="${f(y0)}" stroke="#5B6E8C" stroke-width="1"/>`;
 /* concurrents : traits fins estompés, pastille à l'initiale au bout */
 let riv='';const used=[];
 rv.forEach((r,j)=>{
  const c=RIVCOL[j%4],q=r.pts,pts=q.map((v,i)=>f(x(i*(n-1)/Math.max(1,q.length-1)))+','+f(y(v))).join(' ');
  riv+=`<polyline points="${pts}" fill="none" stroke="${c}" stroke-width=".9" opacity=".28" stroke-linejoin="round"/>`;
  const ex=x(n-1);let ey=y(q[q.length-1]);
  /* on écarte les pastilles qui se chevauchent, sinon elles s'empilent au bord droit */
  while(used.some(v=>Math.abs(v-ey)<9.5))ey+=9.5;
  ey=Math.max(7,Math.min(H-7,ey));used.push(ey);
  riv+=`<circle cx="${f(ex)}" cy="${f(ey)}" r="5.4" fill="${c}" opacity=".92"/>`
     +`<text x="${f(ex)}" y="${f(ey+2)}" text-anchor="middle" font-size="5.6" font-weight="700" fill="#0E1621" font-family="ui-monospace,monospace">${rivTag(r.nm)}</text>`;
 });""")
e.rep(""" if(!opt.anim||from<=0||from>=n-1){
  return `<svg class="navc" viewBox="0 0 ${W} ${H}" aria-hidden="true">${base}${body}
   <circle cx="${f(x(n-1))}" cy="${f(y(p[n-1]))}" r="3" fill="${headC}">
    <animate attributeName="r" values="3;6;3" dur="1.8s" repeatCount="indefinite"/></circle></svg>`;
 }""",
""" const head=`<circle cx="${f(x(n-1))}" cy="${f(y(p[n-1]))}" r="3" fill="${headC}">
    <animate attributeName="r" values="3;6;3" dur="1.8s" repeatCount="indefinite"/></circle>`;
 if(!opt.anim||from<=0||from>=n-1){
  return `<svg class="navc" viewBox="0 0 ${W} ${H}" aria-hidden="true">${base}${riv}${body}${head}</svg>`;
 }""")
# la fenêtre s'élargit à droite, sans zoom ni suivi
old=e.s[e.s.index(" /* fenêtre glissante : la tête reste au centre"):e.s.index("e.rep") if False else e.s.index("function tapeBand(){")]
e.rep(old,
""" /* la fenêtre s'élargit à droite : la géométrie ne bouge pas, seul le dévoilement avance */
 const DRAW=5,x0=x(from);
 const id2='c'+id;
 return `<svg class="navc" viewBox="0 0 ${W} ${H}" aria-hidden="true">
  <defs><clipPath id="${id2}" clipPathUnits="userSpaceOnUse">
   <rect x="0" y="-${H*4}" height="${H*9}" width="${f(x0)}">
    <animate attributeName="width" from="${f(x0)}" to="${W}" dur="${DRAW}s" fill="freeze"/></rect>
  </clipPath></defs>
  ${base}<g clip-path="url(#${id2})">${riv}${body}</g>
  <circle cx="${f(x0)}" cy="${f(y(p[from]))}" r="3.4" fill="${headC}">
   <animate attributeName="cx" values="${(()=>{const a=[];for(let j=0;j<=40;j++){const i=Math.round(from+(n-1-from)*j/40);a.push(f(x(i)))}return a.join(';')})()}" dur="${DRAW}s" fill="freeze"/>
   <animate attributeName="cy" values="${(()=>{const a=[];for(let j=0;j<=40;j++){const i=Math.round(from+(n-1-from)*j/40);a.push(f(y(p[i])))}return a.join(';')})()}" dur="${DRAW}s" fill="freeze"/>
   <animate attributeName="r" values="3;6;3" dur="1.8s" begin="${DRAW}s" repeatCount="indefinite"/></circle></svg>`;
}
""")

# ── on n'ajoute des points que s'il s'est vraiment passé quelque chose ──
e.rep(""" const tgt=y.now,last=S.tape.pts[S.tape.pts.length-1];
 if(Math.abs(tgt/last-1)>1e-9){""",
""" const tgt=y.now,last=S.tape.pts[S.tape.pts.length-1];
 S.tape.from=S.tape.pts.length-1;   /* rien de neuf : rendu statique */
 if(Math.abs(tgt-last)>0.05){       /* 5 pb : en deçà, le P&L fait du surplace */""")
e.rep("""  S.tape.from=S.tape.pts.length-1;   /* le trait ne redessine que ce qui vient d'arriver */
  bridgePts""","""  bridgePts""")

# ── les concurrents, sur le même axe des temps ──
e.rep("""function tapeBand(){""",
"""/* Courbes des concurrents sur la même fenêtre. Leurs clôtures connues sont des points
   d'ancrage ; le trimestre en cours prolonge leur dernière valeur sans dérive, puisque leur
   résultat n'est pas encore connu. */
function rivalTapes(){
 if(!S.rivals)return [];
 const y0=Math.floor(S.q/4)*4;
 let base=1;for(let i=0;i<y0;i++)base*=(1+S.rets[i]);
 return S.rivals.map((r,j)=>{
  const pts=[100];let v=1;
  for(let i=y0;i<S.q;i++){const g=(r.hist&&r.hist[i])||0,nv=v*(1+g);
   bridgePts(v*100,nv*100,TAPEM,hash32('riv'+j+'_'+i,S.seed),tapeVol(TAPEM)*0.30).forEach(z=>pts.push(z));v=nv}
  const segs=Math.max(1,Math.round((S.tape&&S.tape.seg)||1));
  for(let k=0;k<segs;k++)
   bridgePts(v*100,v*100,TAPEM,hash32('rivq'+j+'_'+S.q+'_'+k,S.seed),tapeVol(TAPEM)*0.22).forEach(z=>pts.push(z));
  return {nm:r.nm,pts};
 });
}
function tapeBand(){""")
e.rep("""  ${tapeSvg(p,S.tape.from||0,{anim:1})}</div>`;""",
      """  ${tapeSvg(p,S.tape.from||0,{anim:1,rivals:rivalTapes()})}</div>`;""")
e.rep("""    ${tapeSvg(S.tape.pts,0,{h:132})}</div>`""",
      """    ${tapeSvg(S.tape.pts,0,{h:132,rivals:rivalTapes()})}</div>`""")

# ── accueil : une année complète, tirée au hasard à chaque affichage ──
e.rep("""function heroNav(){
 const st=[1.9,2.6,-0.7,3.4,1.9,4.2,1.1,-2.6,-5.8,-4.4,-6.3,-2.1,1.5,3.2,2.1,4.6,3.0,5.2,2.4,3.9,4.7,6.4];
 const a=[100];st.forEach(x=>a.push(a[a.length-1]*(1+x/100)));return a;
}""",
"""/* Une année complète, tirée au hasard à chaque affichage de l'accueil : quatre trimestres
   pour vous, quatre pour chacun des concurrents, dessinés comme dans le jeu. */
function heroYear(){
 const sd=(Math.random()*1e9)|0,r=prng32(sd);
 const gq=k=>{const u=prng32(sd+k*7919);return (u()+u()+u()-1.5)*0.16};
 const mk=(seed,vol)=>{const pts=[100];let v=1;
  for(let q=0;q<4;q++){const g=gq(seed*4+q),nv=v*(1+g);
   bridgePts(v*100,nv*100,44,hash32('hero'+seed+'_'+q,sd),vol).forEach(z=>pts.push(z));v=nv}
  return {v,pts}};
 const me=mk(1,0.030);
 const rivals=RIVALS.map((x,j)=>({nm:x.nm,pts:mk(11+j,0.011).pts}));
 return {pts:me.pts,fin:me.v,rivals};
}""")
e.rep("""const nv=heroNav();let pk=nv[0],dd=0;nv.forEach(v=>{pk=Math.max(pk,v);dd=Math.max(dd,1-v/pk)});""",
      """const HY=heroYear(),nv=HY.pts;let pk=nv[0],dd=0;nv.forEach(v=>{pk=Math.max(pk,v);dd=Math.max(dd,1-v/pk)});""")
e.rep("""   <div class="navcap">UNE PARTIE, HUIT TRIMESTRES</div>
   ${navChart(nv,{col:'#D9B06A',anim:1,trough:1,h:118})}
   <div class="navrow"><span>DÉPART ${dec(nv[0],0)}</span><span class="neg-g">REPLI −${dec(dd*100,0)} %</span><span class="pos-g">ARRIVÉE ${dec(nv[nv.length-1],0)}</span></div>""",
"""   <div class="navcap">UNE ANNÉE, VOUS ET LES QUATRE AUTRES</div>
   ${tapeSvg(nv,0,{h:122,rivals:HY.rivals})}
   <div class="navrow"><span>REPLI MAX −${dec(dd*100,1)} %</span><span class="${nv[nv.length-1]>=100?'pos-g':'neg-g'}">VOUS ${nv[nv.length-1]>=100?'+':'−'}${dec(Math.abs(nv[nv.length-1]-100),1)} %</span></div>""")

e.done("lot 18 — ruban ancre, concurrents, accueil")
