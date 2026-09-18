# -*- coding: utf-8 -*-
"""Lot 12 — l'attribution factorielle ne bouclait pas.

Mesuré par `tools/attrchk.js` sur 92 clôtures réelles : le brut du trimestre vaut en moyenne
+884 pb, la somme des quatre barres affichées +697 pb. L'échelle est bonne (pente du brut sur
la somme des facteurs : 0,99 ; R² 0,89), mais il manque en moyenne **187 pb par trimestre**,
et rien ne le disait. Ce résidu est la part propre des marchés — le terme e_i·z_i du modèle,
plus le portage et l'effet du stop — c'est-à-dire précisément ce qui n'est PAS un pari macro.

Un joueur qui lit « croissance +120 pb, inflation −40 pb » et qui voit +884 pb en haut de
l'écran ne peut pas savoir si son book a marché parce qu'il avait raison sur la macro ou
parce qu'un marché a bougé pour ses raisons à lui. On ajoute donc la cinquième ligne, et le
total boucle.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
e.rep(""" const amx=Math.max(0.001,...o.attr.map(Math.abs));
 let att='';FACT.forEach((f,k)=>{const v=o.attr[k],wd=Math.abs(v)/amx*50;""",
""" /* ce que les quatre facteurs n'expliquent pas : part propre des marchés, portage, stop */
 const resid=o.gross-o.attr.reduce((a,b)=>a+b,0);
 const amx=Math.max(0.001,...o.attr.map(Math.abs),Math.abs(resid));
 let att='';FACT.forEach((f,k)=>{const v=o.attr[k],wd=Math.abs(v)/amx*50;""")
e.rep(""" let byl=lines.map(z=>`<div class="attr"><span class="an"><span cla""",
""" {const wd=Math.abs(resid)/amx*50;
  att+=`<div class="attr"><span class="an">Part propre des marchés <span style="font-family:var(--mono);font-size:11px;color:var(--dimmer)">hors macro</span></span><span class="av ${cls(resid)}">${sgn(resid,1)} · ${M$(resid*o.nav0)}</span></div>
   <div class="bar2"><span class="mid"></span><i style="${resid>=0?'left:50%':'right:50%'};width:${wd}%;background:${resid>=0?'var(--long)':'var(--short)'};opacity:.55"></i></div>
   <p class="note" style="margin-top:6px">Les quatre facteurs plus la part propre font le brut des positions, ${sgn(o.gross,1)}. La part propre est ce qui a bougé pour des raisons de marché et non de macro : c'est la portion de votre trimestre qui ne dit rien de la justesse de vos paris.</p>`;}
 let byl=lines.map(z=>`<div class="attr"><span class="an"><span cla""")
e.done("lot 12 — part propre dans l'attribution")
