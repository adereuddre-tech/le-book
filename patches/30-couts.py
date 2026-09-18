# -*- coding: utf-8 -*-
"""Lot 3 — niveau et répartition des coûts de transaction.

Diagnostic mesuré sur le fichier publié : ouvrir un book complet coûtait 3,9 pb de l'encours,
soit 1,7 pb du notionnel traité — invisible. Mais suivre une dépêche coûtait
1,9 x le tarif PLUS un glissement forfaitaire de 12,5 pb du notionnel, soit 15,7 pb :
neuf fois le tarif d'un ordre préparé. Sur un trimestre, 90 % de la facture venait des
dépêches et 8 % des ordres — c'est-à-dire que l'écran qui demande au joueur d'arbitrer
l'exécution ne portait sur rien.

Correction : on relève le tarif de base (TCK) et on supprime le glissement forfaitaire, en
gardant une prime d'urgence de 60 % pour un ordre passé dans le feu de l'action. La facture
totale reste du même ordre (environ 2 % de l'encours par an, book entièrement reconstruit
chaque trimestre), mais la part visible et arbitrable passe d'environ 8 % à environ 35 %.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()

e.rep("""function tcost(dk,i){""",
"""/* Échelle générale des coûts d'exécution : fourchette, impact et glissement d'un desk
   discrétionnaire. Un ordre préparé revient à environ 5 pb du notionnel traité, davantage
   sur les marchés étroits (émergents, crypto, volatilité, carbone, fret). */
const TCK=3;
function tcost(dk,i){""")
e.rep(""" bp=x.s+x.c*Math.pow(bnE,pw)*(pw===0.5?1:1.9);""",
      """ bp=(x.s+x.c*Math.pow(bnE,pw)*(pw===0.5?1:1.9))*TCK;""")

# dépêches : prime d'urgence, plus de glissement forfaitaire
e.rep("""  const tc=tcost(d,i);const c=tc.cost*1.9*S.tcMultQ*(S.leakQ?1.45:1)+tc.bn*0.00125;""",
      """  const tc=tcost(d,i);const c=tc.cost*1.6*S.tcMultQ*(S.leakQ?1.45:1);""")
e.rep("""frais (×1,9 + 1,25 pb de glissement)""","""frais (×1,6, prime d'urgence)""",0)

# l'arbitrage d'exécution vaut pour tout le trimestre, pas pour les seuls ordres d'ouverture
e.rep("""  if(e.tcMult){let sub=0;
   if(e.tcMultOn){orders.forEach(o=>{if(e.tcMultOn.includes(INSTR[o.i].sym))sub+=o.t.cost})}else sub=tot;""",
"""  if(e.tcMult){let sub=0;
   if(e.tcMultOn){orders.forEach(o=>{if(e.tcMultOn.includes(INSTR[o.i].sym))sub+=o.t.cost})}
   else {sub=tot;S.tcMultQ*=e.tcMult}   /* la manière d'exécuter vaut aussi pour les ajustements du trimestre */""")

# l'enjeu de chaque option, chiffré dans le bouton
e.rep(""" app.innerHTML=statusBar()+`<div class="fade">
  <div class="block"><details open><summary style="font-size:15px;color:var(--txt);font-weight:600">Récapitulatif des ordres""",
""" /* l'enjeu réel de chaque option, en monnaie, sur la facture d'ouverture du trimestre */
 const stake=c=>{const x=c.e||{};if(!x.tcMult)return '';
  let sub=0;if(x.tcMultOn){orders.forEach(o=>{if(x.tcMultOn.includes(INSTR[o.i].sym))sub+=o.t.cost})}else sub=tot;
  const d=sub*(x.tcMult-1);if(Math.abs(d)<1e-9)return '';
  return ` <b class="${d<0?'pos-g':'neg-g'}">${d<0?'−':'+'}${mm(Math.abs(d))}</b> sur les ordres${x.tcMultOn?'':', et le même tarif sur vos ajustements du trimestre'}`};
 app.innerHTML=statusBar()+`<div class="fade">
  <div class="block"><details open><summary style="font-size:15px;color:var(--txt);font-weight:600">Récapitulatif des ordres""")
e.rep("""   ${ev.ch.map((c,i)=>`<button class="choice" data-i="${i}"><b>${c.b}</b><span>${c.s}</span></button>`).join('')}</div>`
   :`<button class="cta" id="go2">Lancer le trimestre</button>`}""",
"""   ${ev.ch.map((c,i)=>`<button class="choice" data-i="${i}"><b>${c.b}</b><span>${c.s}${stake(c)}</span></button>`).join('')}</div>`
   :`<button class="cta" id="go2">Lancer le trimestre</button>`}""")

e.done("lot 3 — coûts de transaction")
