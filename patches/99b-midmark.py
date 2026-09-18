# -*- coding: utf-8 -*-
"""Lot 14 — le ruban rend la courbe du mi-parcours inutile, et il prend son temps.

1. Le ruban de P&L est maintenant affiché en permanence pendant le trimestre : la courbe
   de performance cumulée du mi-parcours faisait double emploi. Supprimée. Le texte dit
   désormais ce que le graphique ne disait pas — quelle part du gain de l'année vient des
   positions directionnelles que le joueur porte à cet instant.
2. Le tracé du ruban se déroule sur trois secondes, et l'événement n'apparaît qu'ensuite :
   on regarde le marché bouger avant d'apprendre ce qui l'a fait bouger.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()

# ── 1. mi-parcours : plus de courbe, un texte qui décompose ──
e.rep(""" const navB=S.nav;
 resultCard(`TRIMESTRE ${S.q+1} · MI-PARCOURS`,p>=0?"Le book est en gains latents":"Le book est en pertes latentes",
  [`À mi-trimestre, vos positions directionnelles valent <em class="${cls(p)}">${sgn(p,1)} · ${mn(p*navB)}</em>, non réalisés. Rien n'est encaissé, mais les investisseurs et le comité reçoivent le rapport hebdomadaire et réagissent : ${gz(g.lp,g.rc,'always')}.`,""",
""" const navB=S.nav;
 /* part du gain de l'année portée par les positions ouvertes, en points d'indice */
 const y=ytdIdx(),tot=y.now-100;
 const dir=(p*S.nav/Math.max(1e-9,S.navQ0))*(S.idx/Math.max(1e-9,y.base))*100;
 resultCard(`TRIMESTRE ${S.q+1} · MI-PARCOURS`,p>=0?"Le book est en gains latents":"Le book est en pertes latentes",
  [`Le fonds est à <em class="${cls(tot)}">${sgn(tot/100,1)}</em> depuis le début de l'année. Sur ce total, <em class="${cls(dir)}">${dir>=0?'+':'−'}${dec(Math.abs(dir),1)} point${Math.abs(dir)>=2?'s':''}</em> viennent des positions directionnelles que vous portez en ce moment — <em class="${cls(p)}">${sgn(p,1)} · ${mn(p*navB)}</em> de gains latents, rien n'est encaissé. Le reste est déjà acquis : dépêches soldées, collatéral, incidents. Les investisseurs et le comité reçoivent le rapport hebdomadaire et réagissent : ${gz(g.lp,g.rc,'always')}.`,""")
e.rep("""  "Poursuivre le trimestre",stepEvents,
  {top:navBox(`PERFORMANCE NETTE CUMULÉE · T1 À T${S.q+1} EN COURS`,idxSeries(p*0.5),{anim:1,trough:1,prov:1})});""",
"""  "Poursuivre le trimestre",stepEvents);   /* le ruban est déjà à l'écran : pas de doublon */""")

# ── 2. trois secondes de tracé avant l'événement ──
e.rep(""".tape .navdraw{animation-duration:1.4s}""",
""".tape .navdraw{animation-duration:3s;animation-timing-function:linear}
/* l'événement se découvre une fois le ruban tracé : on voit le marché bouger, puis on
   apprend pourquoi. Sous « mouvement réduit », tout est visible d'emblée. */
.evhold{opacity:0;pointer-events:none;animation:evshow .5s ease-out 3s forwards}
@keyframes evshow{to{opacity:1;pointer-events:auto}}
@media (prefers-reduced-motion:reduce){.evhold{opacity:1;pointer-events:auto;animation:none}}""")
e.rep("""app.innerHTML=statusBar()+`<div class="evwrap fade">
  <div class="evc""",
"""app.innerHTML=statusBar()+`<div class="evwrap fade${S.phase==='events'?' evhold':''}">
  <div class="evc""",4)

e.done("lot 14 — mi-parcours et rythme du ruban")
