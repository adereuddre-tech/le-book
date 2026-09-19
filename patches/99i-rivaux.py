# -*- coding: utf-8 -*-
"""Lot 21 — les concurrents jouent vraiment, et leur ruban le montre.

Découverte en ouvrant le code plutôt qu'en réécrivant : les concurrents ont DÉJÀ un vrai
book (`rv.k`) et un vrai rendement calculé sur les mêmes rendements réalisés que le joueur
(`rivRet(j,t)` = Σ wᵢ rᵢ + collatéral − leurs coûts), avec une fraction de trimestre `t`
déjà prévue dans la signature. Rien à inventer : il manquait deux branchements.

1. Leurs rendements trimestriels n'étaient nulle part conservés (`rv.hist` n'existait pas),
   donc mon `rivalTapes()` du lot 18 lisait `undefined` et les traçait à plat sur les
   trimestres déjà clos.
2. Pendant le trimestre en cours, je les prolongeais sans dérive faute de mieux. `rivRet(j,t)`
   donne leur P&L réel à l'instant t, exactement comme `liveRet()` pour le joueur.

Résultat : leurs courbes sont désormais corrélées à la vôtre par le marché. Quand un choc
d'inflation tombe, on voit lequel était positionné comme vous et lequel s'en sort.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()

e.rep(""" S.rivals.forEach((rv,j)=>{rv.last=rr[j];rv.cum*=(1+rr[j])});""",
""" S.rivals.forEach((rv,j)=>{rv.last=rr[j];rv.cum*=(1+rr[j]);(rv.hist=rv.hist||[]).push(rr[j])});""")
e.rep("""  const segs=Math.max(1,Math.round((S.tape&&S.tape.seg)||1));
  for(let k=0;k<segs;k++)
   bridgePts(v*100,v*100,TAPEM,hash32('rivq'+j+'_'+S.q+'_'+k,S.seed),tapeVol(TAPEM)*0.22).forEach(z=>pts.push(z));
  return {nm:r.nm,pts};""",
"""  /* trimestre en cours : leur P&L réel à l'instant t, même formule que la vôtre */
  const segs=Math.max(1,Math.round((S.tape&&S.tape.seg)||1)),t=qElapsed();
  let g=0;try{g=rivRet(j,t)}catch(err){g=0}
  for(let k=0;k<segs;k++){
   const u=(k+1)/segs,nv=v*(1+g*u);
   bridgePts(v*(1+g*(k/segs))*100,nv*100,TAPEM,hash32('rivq'+j+'_'+S.q+'_'+k,S.seed),tapeVol(TAPEM)*0.26).forEach(z=>pts.push(z));
  }
  return {nm:r.nm,pts};""")

e.done("lot 21 — les concurrents jouent vraiment")
