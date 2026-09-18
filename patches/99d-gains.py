# -*- coding: utf-8 -*-
"""Lot 16 — trésorerie affichée, book verrouillé à la case, texte des dépêches immédiat.

1. La tuile « Vos gains » montrait `mgrNet()`, c'est-à-dire le gain PAR RAPPORT au capital de
   départ. Elle montre désormais la trésorerie réelle, `mgrCash()` : le chiffre affiché est
   exactement ce qu'il reste à dépenser, ce que promettaient déjà l'écran de budget et celui
   des ordres.
2. Le book verrouille à la case, comme l'écran des dépenses d'exploitation : toute position
   dont le coût ferait passer la facture au-dessus de la trésorerie est grisée et
   inactivable, au lieu de laisser construire un book pour le refuser à la validation.
3. Le texte des dépêches s'affiche tout de suite ; l'attente de trois secondes est retirée.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()

# ── 1. la tuile dit la trésorerie ──
e.rep("""<b id="gaintile" class="${mgrNet()>=0?'':'neg-g'}">${score(mgrNet())}</b>""",
      """<b id="gaintile" class="${mgrCash()>=0?'':'neg-g'}">${score(mgrCash())}</b>""")
e.rep(""" const v=mgrNet();e.textContent=score(v);e.className=v>=0?'':'neg-g'}""",
      """ const v=mgrCash();e.textContent=score(v);e.className=v>=0?'':'neg-g'}""")

# ── 2. verrou à la case sur le book ──
e.rep("""function segStyle(i,v,dis){
 if(dis)return 'opacity:.22';""",
"""/* Coût de la facture d'ordres si le marché i passait à la position v. Sert à griser les
   cases inabordables, exactement comme les niveaux de budget hors caisse. */
function costIf(i,v){
 let t=0;
 for(let j=0;j<N;j++){const d=(j===i?v:S.k[j])-S.k0[j];if(Math.abs(d)>1e-9)t+=tcost(d,j).cost}
 return t;
}
function segAfford(i,v){
 const purse=Math.max(0,mgrCash()+liveTC());
 return costIf(i,v)<=purse+1e-12;
}
function segStyle(i,v,dis){
 if(dis)return 'opacity:.22';""")
e.rep("""    const dis=Math.abs(v)>S.maxk,c=v<0?'neg':v>0?'pos':'zero';""",
"""    const dis=Math.abs(v)>S.maxk||!segAfford(i,v),c=v<0?'neg':v>0?'pos':'zero';""")
e.rep("""  <div class="kv" id="purse"></div>""",
      """  <div class="kv" id="purse"></div>
  <p class="note" id="pursenote" style="margin-top:-2px"></p>""")
e.rep(""" if(p)p.innerHTML=`<span>Ordres ${mm(c)} · trésorerie après paiement</span><b class="${rest>=0?'':'neg-g'}">${mm(rest)}</b>`
   +(ko?` <button class="buy" id="fitbook" style="margin-left:8px">Ramener le book au payable</button>`:'');""",
""" if(p)p.innerHTML=`<span>Ordres ${mm(c)} · trésorerie après paiement</span><b class="${rest>=0?'':'neg-g'}">${mm(rest)}</b>`
   +(ko?` <button class="buy" id="fitbook" style="margin-left:8px">Ramener le book au payable</button>`:'');
 {const nt=document.getElementById('pursenote');
  if(nt)nt.textContent=avail>0?`Les positions grisées coûteraient plus que votre trésorerie (${mm(avail)}).`
    :"Votre trésorerie est vide : vous ne pouvez plus passer d'ordre payant ce trimestre.";}""")
# les cases doivent être réévaluées à chaque changement de position
e.rep("""   updateRow(i);renderRisk();refreshStatus();refreshGain();refreshSend();""",
      """   drawRows();renderRisk();refreshStatus();refreshGain();refreshSend();""")

# ── 3. le texte des dépêches ne se fait plus attendre ──
e.rep("""app.innerHTML=statusBar()+`<div class="evwrap ${S.phase==='events'?'evhold':'fade'}">
  <div class="evc""",
"""app.innerHTML=statusBar()+`<div class="evwrap fade">
  <div class="evc""",4)

e.done("lot 16 — tresorerie, verrou a la case, texte immediat")
