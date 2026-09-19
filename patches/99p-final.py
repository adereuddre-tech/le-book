# -*- coding: utf-8 -*-
"""Lot 27 — jauge d'exposition retirée, ruban recalé sur le net, annonces en confiance."""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()

# 1. la jauge d'exposition s'en va
old=e.s[e.s.index("   ${(()=>{const gr=w.reduce((a,v)=>a+Math.abs(v),0);"):e.s.index("""   <button class="fg" data-gauge="risk\"""")]
e.rep(old,"")

# 2. le ruban n'apparaît qu'une fois le trimestre lancé, pas sur les écrans d'annonce
e.rep("""function phaseLive(){
 save('phaseLive');""","""function phaseLive(){
 S.live=true;   /* le ruban ne s'affiche qu'à partir d'ici : avant, la performance ne bouge pas */
 save('phaseLive');""")
e.rep("""${S.phase==='events'?tapeBand():ticker()}""",
      """${(S.phase==='events'&&S.live)?tapeBand():ticker()}""")
e.rep(""" S.pendingTC=0;S.freeAdjUsed=false;""",""" S.pendingTC=0;S.freeAdjUsed=false;S.live=false;""")

# 3. les annonces de jauges parlent la même langue que la barre d'état
e.rep("""function gz(lp,rc,opt){
 const p=[];
 if(Math.abs(lp||0)>=0.05||opt==='always')p.push(`<span class="${cls(lp)}">investisseurs ${sd1(lp)}</span>`);
 if(Math.abs(rc||0)>=0.05||opt==='always')p.push(`<span class="${cls(rc)}">comité ${sd1(rc)}</span>`);
 return p.join(' • ');
}""",
"""/* Un seul chiffre, celui de la barre d'état : de combien la confiance va bouger. Le détail
   par canal — investisseurs, comité — reste lisible en seconde ligne quand il éclaire, mais
   le nombre qui compte est celui que le joueur voit en haut de l'écran. */
function gz(lp,rc,opt){
 const l0=S&&S.lp!==undefined?S.lp:60,r0=S&&S.rc!==undefined?S.rc:60;
 const c0=0.6*Math.min(l0,r0)+0.4*(l0+r0)/2;
 const l1=Math.max(0,Math.min(100,l0+(lp||0))),r1=Math.max(0,Math.min(100,r0+(rc||0)));
 const d=0.6*Math.min(l1,r1)+0.4*(l1+r1)/2-c0;
 if(Math.abs(d)<0.05&&opt!=='always')return '';
 const who=[];
 if(Math.abs(lp||0)>=0.05)who.push(`investisseurs ${sd1(lp)}`);
 if(Math.abs(rc||0)>=0.05)who.push(`comité ${sd1(rc)}`);
 return `<span class="${cls(d)}">confiance ${sd1(d)}</span>`
  +(who.length?` <span class="dim-g">(${who.join(', ')})</span>`:'');
}""")

# 4. après la clôture, le ruban doit finir sur le chiffre NET affiché en haut
e.rep(""" S.prevRel=qTotal-med;""",
""" /* Le ruban suivait la performance AVANT commission de performance ; la tuile « Perf. »
    affiche le net. D'où deux chiffres différents au débriefing — +107,5 % contre +89,5 %.
    On prolonge le ruban jusqu'à l'indice net réellement réalisé : il finit désormais
    exactement sur le chiffre du haut de l'écran. */
 if(S.tape&&S.tape.pts&&S.tape.pts.length>2){
  const y0=Math.floor((S.q)/4)*4;let base=1;for(let i=0;i<y0;i++)base*=(1+S.rets[i]);
  const tgt=S.idx/Math.max(1e-9,base)*100,last=S.tape.pts[S.tape.pts.length-1];
  if(Math.abs(tgt-last)>0.02){
   S.tape.from=S.tape.pts.length-1;
   bridgePts(last,tgt,18,hash32('settle'+S.q,S.seed),tapeVol(18)*0.5).forEach(z=>S.tape.pts.push(z));
  }
 }
 S.prevRel=qTotal-med;""")

e.done("lot 27 — exposition retiree, ruban net, annonces en confiance")
