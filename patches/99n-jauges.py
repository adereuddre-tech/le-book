# -*- coding: utf-8 -*-
"""Lot 26 — écusson dans la barre, jauge d'exposition, jauge de risque assagie."""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()

# 1 + 2. libellé complet, et l'écusson du fonds à gauche de la jauge
e.rep("""<span><i>Confiance</i>""","""<span><i>Confiance des investisseurs</i>""")
e.rep("""  </div>
  <div class="srow">
   ${(()=>{if(S.phase!=='book'||!S.k0)return '';""",
"""  </div>
  <div class="srow">
   <span class="crestbadge">${crestSvg(S.crest||0,26)}</span>
   ${(()=>{if(S.phase!=='book'||!S.k0)return '';""")

# 3. la jauge de risque : plus de bande ni de pastille, un trait discret, des couleurs sobres
e.rep("""<span class="ft2 lin"><span class="band" style="left:${(1-band)*50}%;width:${band*100}%"></span><em style="left:50%"></em><i style="left:0;width:${Math.min(100,rk*50)}%;background:${rcol}"></i></span>""",
"""<span class="ft2 lin"><span class="mand" style="left:50%"></span><i style="left:0;width:${Math.min(100,rk*50)}%;background:${rcol}"></i></span>""")
e.rep(""" const rhue=145-140*Math.pow(Math.min(1,rdev),0.62);
 const rcol=`hsl(${rhue.toFixed(0)} 62% ${(52+8*Math.min(1,rdev)).toFixed(0)}%)`;""",
""" /* teintes sobres, dans la gamme du reste du jeu : vert de mousse, ocre, brique */
 const rhue=150-140*Math.pow(Math.min(1,rdev),0.62);
 const rcol=`hsl(${rhue.toFixed(0)} ${(30+18*Math.min(1,rdev)).toFixed(0)}% ${(46+6*Math.min(1,rdev)).toFixed(0)}%)`;""")
e.rep(""".chips i.sure{""",
""".crestbadge{display:flex;align-items:center;padding:0 2px;line-height:0;flex-shrink:0}
.ft2 .mand{position:absolute;top:-2px;bottom:-2px;width:1px;background:var(--dimmer);opacity:.7}
.chips i.sure{""")

# 4. exposition brute aux marchés, entre l'appétit et le risque
e.rep("""   ${[0,1,2,3].map(fg).join('')}
   <button class="fg" data-gauge="risk\"""",
"""   ${[0,1,2,3].map(fg).join('')}
   ${(()=>{const gr=w.reduce((a,v)=>a+Math.abs(v),0);
     return `<button class="fg" data-gauge="expo"><span class="fl">Exposition</span><span class="tri none">&nbsp;</span><span class="ft2 lin"><i style="left:0;width:${Math.min(100,gr*20)}%;background:hsl(210 26% 50%)"></i></span><b>${gr.toFixed(1)}×</b></button>`})()}
   <button class="fg" data-gauge="risk\"""")
e.rep(""" else if(id==='risk'){""",
""" else if(id==='expo'){
  const w=weights(S.k),gr=w.reduce((a,v)=>a+Math.abs(v),0),net=w.reduce((a,v)=>a+v,0);
  openModal('Exposition aux marchés',`<p>Le notionnel que vous portez, rapporté à l'encours du fonds. <em>${gr.toFixed(2)}×</em> en brut : c'est la somme des positions en valeur absolue, longues et courtes confondues. <em>${net>=0?'+':'−'}${Math.abs(net).toFixed(2)}×</em> en net, c'est-à-dire ce qui reste une fois les longues et les courtes compensées.</p>
   <p class="note">L'exposition n'est pas le risque : un book brut de 4× réparti sur des marchés qui s'annulent peut être moins volatil qu'un book de 1× concentré sur un seul facteur. La jauge Risque, elle, tient compte des corrélations. Les deux se lisent ensemble — un écart important entre elles signale un book qui repose sur des compensations, et les compensations se défont dans les crises.</p>`);
 }
 else if(id==='risk'){""")

e.done("lot 26 — ecusson, exposition, jauge de risque")
