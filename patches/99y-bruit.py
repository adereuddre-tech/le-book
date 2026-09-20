# -*- coding: utf-8 -*-
"""Lot 36 — le bruit du ruban à la bonne échelle.

Constat, rendu visible par le compteur du lot 35 : au mi-parcours d'un trimestre qui finit à
+1,0 %, le compteur monte à +12,1 % puis redescend. Le ruban racontait une histoire que le
fonds n'a pas vécue.

Cause : `tapeVol(m) = 1,4 × vol_cible / √m` — une amplitude par pas calée sur la volatilité
**annuelle**, quelle que soit la durée couverte par le segment. Un pont brownien de m pas
d'amplitude v par pas s'écarte au milieu d'environ v·√m/2, soit ici 0,7 × vol annuelle : 14 %
pour un mandat à 20 %. Et les segments de dépêche ne couvrent qu'un huitième de trimestre tout
en portant ce même bruit.

Correction : l'écart-type d'un chemin sur une fraction dt de trimestre vaut σ_trimestre·√dt,
avec σ_trimestre = vol annuelle / 2 (la convention déjà utilisée par `rivalReturns` et
`liveRet`). Donc amplitude par pas = (vol/2)·√(dt/m), l'écart au milieu du pont valant
(vol/2)·√dt/2 — 2,5 % pour un trimestre entier à 20 % de vol cible, au lieu de 14 %.
`tapeTick` mesure dt sur l'avancement réel de la file de dépêches ; les concurrents prennent
leur propre volatilité au lieu d'un facteur forfaitaire (0,30 / 0,26).

Aucun tirage de `rng` n'est touché : seuls les ponts de décor changent de forme.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
e.rep("function tapeVol(m){return Math.max(0.006,(S.tgt||0.05)*1.4/Math.sqrt(m))}",
 "/* Amplitude par pas d'un pont de m points couvrant la fraction dt d'un trimestre, pour une\n"
 "   volatilité annuelle v (vol cible du mandat par défaut, celle du concurrent pour eux).\n"
 "   σ_trimestre = v/2 ; l'écart au milieu du pont vaut (v/2)·√dt/2. */\n"
 "function tapeVol(m,dt,v){return Math.max(0.0008,((v===undefined?(S.tgt||0.05):v)/2)*Math.sqrt(Math.max(0.01,dt===undefined?1:dt)/m))}")
# clôtures déjà connues : un trimestre entier
e.rep("bridgePts(v*100,nv*100,TAPEM,hash32('tape'+(yk+i),S.seed),tapeVol(TAPEM)).forEach(x=>pts.push(x));v=nv});",
      "bridgePts(v*100,nv*100,TAPEM,hash32('tape'+(yk+i),S.seed),tapeVol(TAPEM,1)).forEach(x=>pts.push(x));v=nv});")
# segment en cours : la fraction de trimestre réellement écoulée depuis le segment précédent
e.rep("""  bridgePts(last,tgt,TAPEM,hash32('tapeq'+S.q+'_'+(S.tape.seg++),S.seed),tapeVol(TAPEM))
    .forEach(x=>S.tape.pts.push(x));
  (S.tape.ts=S.tape.ts||[]).push(qElapsed());   /* les concurrents avancent au même instant */""",
"""  const t1=qElapsed(),t0=(S.tape.ts&&S.tape.ts.length)?S.tape.ts[S.tape.ts.length-1]:0;
  bridgePts(last,tgt,TAPEM,hash32('tapeq'+S.q+'_'+(S.tape.seg++),S.seed),tapeVol(TAPEM,t1-t0))
    .forEach(x=>S.tape.pts.push(x));
  (S.tape.ts=S.tape.ts||[]).push(t1);   /* les concurrents avancent au même instant */""")
# concurrents : leur propre volatilité
e.rep("bridgePts(v*100,nv*100,TAPEM,hash32('riv'+j+'_'+i,S.seed),tapeVol(TAPEM)*0.30).forEach(z=>pts.push(z));v=nv}",
      "bridgePts(v*100,nv*100,TAPEM,hash32('riv'+j+'_'+i,S.seed),tapeVol(TAPEM,1,r.vol)).forEach(z=>pts.push(z));v=nv}")
e.rep("""  ts.forEach((t,k)=>{const nv=v*(1+rivRet(j,t,tq))*100;
   bridgePts(last,nv,TAPEM,hash32('rivq'+j+'_'+tq+'_'+k,S.seed),tapeVol(TAPEM)*0.26).forEach(z=>pts.push(z));last=nv});""",
"""  ts.forEach((t,k)=>{const nv=v*(1+rivRet(j,t,tq))*100;
   bridgePts(last,nv,TAPEM,hash32('rivq'+j+'_'+tq+'_'+k,S.seed),tapeVol(TAPEM,t-(k?ts[k-1]:0),r.vol)).forEach(z=>pts.push(z));last=nv});""")
# derniers pas de clôture : quelques jours, pas un trimestre
e.rep("bridgePts(last,nv,18,hash32('rivs'+j+'_'+tq,S.seed),tapeVol(18)*0.3).forEach(z=>pts.push(z))}",
      "bridgePts(last,nv,18,hash32('rivs'+j+'_'+tq,S.seed),tapeVol(18,0.04,r.vol)).forEach(z=>pts.push(z))}")
e.rep("bridgePts(last,tgt,18,hash32('settle'+S.q,S.seed),tapeVol(18)*(Math.abs(tgt-last)>0.02?0.5:0.1)).forEach(z=>S.tape.pts.push(z));",
      "bridgePts(last,tgt,18,hash32('settle'+S.q,S.seed),tapeVol(18,0.04)).forEach(z=>S.tape.pts.push(z));")
e.done("lot 36 — bruit du ruban a la bonne echelle")
