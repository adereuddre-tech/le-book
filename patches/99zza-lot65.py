# -*- coding: utf-8 -*-
"""Lot 65 — panneau du haut, disposition A choisie par Antoine : le nuage risque/profit occupe une
colonne de droite sur la hauteur de deux rangées ; à gauche, confiance · carton · trésorerie puis
les quatre facteurs en tuiles compactes (flèches et valeur, sans barre). Le blason passe dans la
tuile d'encours."""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
e.rep("""<button class="tile" data-gauge="cap"><span><i>${S.fundName.split(' ')[0]}""","""<button class="tile" data-gauge="cap"><span><i><span class="crestmini">${crestSvg(S.crest||0,15)}</span>${S.fundName.split(' ')[0]}""")
e.rep("""  <div class="srow">
   <span class="crestbadge">${crestSvg(S.crest||0,26)}</span>
""","""  <div class="sgrid"><div class="sl">
  <div class="srow">
""")
e.rep("""  <div class="srow">
   ${[0,1,2,3].map(fg).join('')}
   <button class="fg rmt" data-gauge="risk" style="flex:2.8">${riskMap(sp)}</button>
  </div>""","""  <div class="srow fcomp">
   ${[0,1,2,3].map(fg).join('')}
  </div></div>
   <button class="fg rmt" data-gauge="risk">${riskMap(sp)}</button>
  </div>""")
e.rep("""<span class="fl">${FACT[k].nm.split(' ')[0].slice(0,9)}</span>""","""<span class="fl">${['Crois.','Infl.','Dollar','Appét.'][k]||FACT[k].nm.slice(0,6)}</span>""")
e.rep(" const W=big?320:150,H=big?210:66,"," const W=big?320:150,H=big?210:118,")
e.rep(".mbox.redbox{",""".sgrid{display:flex;gap:6px;margin-top:5px;align-items:stretch}
.sgrid .sl{flex:1.45;display:flex;flex-direction:column;gap:5px;min-width:0}
.sgrid .sl .srow{margin-top:0}
.sgrid .tile{padding:4px 5px}.sgrid .tile b{font-size:13.5px;overflow:visible;text-overflow:clip;white-space:nowrap}.sgrid .tile.gauge>span{display:flex;flex-wrap:wrap;justify-content:space-between;gap:0 4px}.sgrid .tile.gauge span i{font-size:11px!important;overflow:visible!important;text-overflow:clip!important;flex:0 0 auto}
.sgrid .tile.gauge{flex:1.45!important}.sgrid .tile.gold{flex:1.35!important}.sgrid .tile.gold span{font-size:10.5px}
.sgrid .tile.cardt{flex:0 0 24px;padding:1px}.sgrid .tile.cardt svg{width:14px;height:19px}
.srow.fcomp{gap:4px}.srow.fcomp .fg{padding:3px 2px 2px}.srow.fcomp .fg .ft2{display:none}
.srow.fcomp .fg .fl{font-size:9px}
.sgrid .fg.rmt{flex:1;min-width:0;padding:3px 4px;display:flex}
.sgrid .rmap{height:100%;min-height:108px}
.crestmini{display:inline-block;vertical-align:-3px;margin-right:4px}.crestmini svg{display:block}
.mbox.redbox{""")
e.rep("return [c0,'#E8C547','#F3EEE4'].find(","return ['#E8C547',c0,'#F3EEE4'].find(")
e.done("lot 65 — panneau du haut, disposition A")
