# -*- coding: utf-8 -*-
"""Lot 15 — le texte des événements avait disparu, et le ruban manquait de nerf.

1. RÉGRESSION du lot 14 : `.fade{animation:fade .3s ease}` et `.evhold{...animation:evshow...}`
   étaient posées sur le MÊME élément. `animation` est une propriété raccourcie, pas
   cumulative : la dernière règle de la feuille l'emporte entièrement. `.fade` gagnait, son
   animation sans `fill-mode` se terminait en 0,3 s, et l'élément retombait sur le
   `opacity:0` déclaré par `.evhold`. Le texte de chaque dépêche restait donc invisible pour
   toujours. Les deux classes sont désormais exclusives.
2. Le ruban est tracé à un pas horaire sur treize semaines : 48 points par segment au lieu
   de 9, et une amplitude calée sur la volatilité cible du mandat plutôt qu'une constante.
3. Le trait ne se redessine plus depuis le début : la partie déjà vue est posée d'emblée,
   seule la portion nouvelle se trace en trois secondes.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()

# ── 1. plus jamais deux animations sur le même élément ──
e.rep("""app.innerHTML=statusBar()+`<div class="evwrap fade${S.phase==='events'?' evhold':''}">
  <div class="evc""",
"""app.innerHTML=statusBar()+`<div class="evwrap ${S.phase==='events'?'evhold':'fade'}">
  <div class="evc""",4)
e.rep(""".evhold{opacity:0;pointer-events:none;animation:evshow .5s ease-out 3s forwards}
@keyframes evshow{to{opacity:1;pointer-events:auto}}""",
""".evhold{opacity:0;pointer-events:none;animation:evshow .55s ease-out 3s forwards}
@keyframes evshow{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none;pointer-events:auto}}""")

# ── 2. pas horaire : beaucoup plus de points, amplitude tirée de la volatilité du mandat ──
e.rep("""    bridgePts(v*100,nv*100,16,hash32('tape'+(yk+i),S.seed),0.010).forEach(x=>pts.push(x));v=nv});""",
"""    bridgePts(v*100,nv*100,TAPEM,hash32('tape'+(yk+i),S.seed),tapeVol(TAPEM)).forEach(x=>pts.push(x));v=nv});""")
e.rep("""  const vol=Math.max(0.004,(S.tgt||0.05)/6);
  bridgePts(last,tgt,9,hash32('tapeq'+S.q+'_'+(S.tape.seg++),S.seed),vol).forEach(x=>S.tape.pts.push(x));
  if(S.tape.pts.length>420)S.tape.pts.splice(0,S.tape.pts.length-420);""",
"""  S.tape.from=S.tape.pts.length-1;   /* le trait ne redessine que ce qui vient d'arriver */
  bridgePts(last,tgt,TAPEM,hash32('tapeq'+S.q+'_'+(S.tape.seg++),S.seed),tapeVol(TAPEM))
    .forEach(x=>S.tape.pts.push(x));
  if(S.tape.pts.length>3000){const cut=S.tape.pts.length-3000;
    S.tape.pts.splice(0,cut);S.tape.from=Math.max(0,S.tape.from-cut)}""")
e.rep("""/* Le ruban. Le passé est stocké, jamais recalculé ; seul le présent s'allonge. */""",
"""/* Un trimestre fait treize semaines ; à un pas horaire, cela fait quelques centaines de
   points. L'amplitude par pas est calée sur la volatilité cible du mandat et non sur une
   constante : un fonds agressif a un ruban plus nerveux, ce qui est la vérité. */
const TAPEM=48;
function tapeVol(m){return Math.max(0.006,(S.tgt||0.05)*1.4/Math.sqrt(m))}
/* Le ruban. Le passé est stocké, jamais recalculé ; seul le présent s'allonge. */""")

# ── 3. tracé partiel : l'ancien est posé, le nouveau se dessine ──
e.rep("""function tapeBand(){
 try{tapeTick()}catch(err){return ticker()}
 const p=S.tape&&S.tape.pts||[];
 if(p.length<3)return ticker();
 const v=p[p.length-1],up=v>=100;
 return `<div class="tape"><div class="tapehead"><span>P&amp;L DU FONDS · ANNÉE ${1+Math.floor(S.q/4)}</span>
   <b class="${up?'pos-g':'neg-g'}">${up?'+':'−'}${dec(Math.abs(v-100),1)} %</b></div>
  ${navChart(p,{h:78,base:100,anim:1,pulse:1})}</div>`;
}""",
"""/* Deux traits : celui qu'on a déjà vu, posé d'emblée, et celui qui vient d'arriver, qui se
   dessine en trois secondes. Le remplissage du nouveau segment apparaît avec lui, pour ne pas
   révéler d'avance où la courbe va. */
function tapeSvg(p,from){
 const W=320,H=78,pad=5,n=p.length;
 let lo=Math.min(100,...p),hi=Math.max(100,...p);
 const sp=(hi-lo)||1;lo-=sp*0.12;hi+=sp*0.12;
 const px=i=>pad+i*(W-2*pad)/(n-1),py=v=>H-pad-(v-lo)/(hi-lo)*(H-2*pad);
 const pt=i=>px(i).toFixed(1)+','+py(p[i]).toFixed(1);
 const col=p[n-1]>=100?'#4FA98C':'#C4576F',id='tp'+(NGID++);
 const k=Math.max(0,Math.min(n-1,from|0));
 const seg=(a,b)=>{const o=[];for(let i=a;i<=b;i++)o.push(pt(i));return o};
 const area=(a,b)=>{const o=seg(a,b);
   return 'M'+px(a).toFixed(1)+','+(H-pad)+' L'+o.join(' L')+' L'+px(b).toFixed(1)+','+(H-pad)+'Z'};
 return `<svg class="navc" viewBox="0 0 ${W} ${H}" aria-hidden="true">
  <defs><linearGradient id="${id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${col}" stop-opacity=".30"/><stop offset="1" stop-color="${col}" stop-opacity="0"/></linearGradient></defs>
  ${k>0?`<path d="${area(0,k)}" fill="url(#${id})"/>`:''}
  ${k<n-1?`<path class="tapefill" d="${area(k,n-1)}" fill="url(#${id})"/>`:''}
  <line x1="0" y1="${py(100).toFixed(1)}" x2="${W}" y2="${py(100).toFixed(1)}" stroke="#35496A" stroke-width="1" stroke-dasharray="3 4"/>
  ${k>0?`<polyline points="${seg(0,k).join(' ')}" fill="none" stroke="${col}" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"/>`:''}
  ${k<n-1?`<polyline class="tapedraw" points="${seg(k,n-1).join(' ')}" fill="none" stroke="${col}" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"/>`:''}
  <circle class="tapehead2" cx="${px(n-1).toFixed(1)}" cy="${py(p[n-1]).toFixed(1)}" r="3" fill="${col}">
   <animate attributeName="r" values="3;6;3" dur="1.8s" repeatCount="indefinite"/></circle></svg>`;
}
function tapeBand(){
 try{tapeTick()}catch(err){return ticker()}
 const p=S.tape&&S.tape.pts||[];
 if(p.length<3)return ticker();
 const v=p[p.length-1],up=v>=100;
 return `<div class="tape"><div class="tapehead"><span>P&amp;L DU FONDS · ANNÉE ${1+Math.floor(S.q/4)}</span>
   <b class="${up?'pos-g':'neg-g'}">${up?'+':'−'}${dec(Math.abs(v-100),1)} %</b></div>
  ${tapeSvg(p,S.tape.from||0)}</div>`;
}""")
e.rep(""".tape .navdraw{animation-duration:3s;animation-timing-function:linear}""",
""".tapedraw{stroke-dasharray:4000;stroke-dashoffset:4000;animation:navdr 3s linear forwards}
.tapefill{opacity:0;animation:tapefade 3s linear forwards}
@keyframes tapefade{to{opacity:1}}
@media (prefers-reduced-motion:reduce){.tapedraw{animation:none;stroke-dashoffset:0}.tapefill{animation:none;opacity:1}}""")

e.done("lot 15 — texte des evenements restaure, ruban horaire et tracé partiel")
