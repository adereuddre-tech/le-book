# -*- coding: utf-8 -*-
"""Lot 22 — le comité jugeait une autre volatilité que celle affichée au joueur.

Symptôme : augmenter un short faisait MONTER la jauge comité, alors que la jauge risque
était déjà à 29 sur 30.

Cause : deux grandeurs différentes portant le même nom.
  - la jauge de la barre d'état affiche `riskShown(w).total`, c'est-à-dire la volatilité
    sous stress de corrélation plus la variance des dépêches en cours ;
  - le comité, lui, jugeait `pvol(w)`, la volatilité brute, systématiquement plus basse.
Dans la capture : la jauge dit 29/30, le comité voit 26,5/30. Le joueur se croit au mandat
alors que le comité le trouve trop timide ; en montant son short il se rapproche du mandat
AUX YEUX DU COMITÉ, donc la note s'améliore. Le comportement était correct, la lecture
impossible. Le comité juge désormais exactement le chiffre affiché.

Second correctif : la note était une marche d'escalier — un +3 forfaitaire n'importe où dans
la bande. Elle décroît maintenant continûment de +3 au centre du mandat à 0 au bord de la
bande, puis devient une sanction. Être pile sur son mandat vaut mieux qu'en frôler le bord.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()

e.rep("""function riskRc(k){
 const w=weights(k),sp=pvol(w),vd=varDecomp(w),fmax=Math.max(...vd.fv)/vd.tot;""",
"""function riskRc(k){
 const w=weights(k),sp=riskShown(w).total,vd=varDecomp(w),fmax=Math.max(...vd.fv)/vd.tot;""")
e.rep("""function riskGauge(why,bonus){
 const w=weights(S.k),sp=pvol(w),vd=varDecomp(w),fmax=Math.max(...vd.fv)/vd.tot;""",
"""function riskGauge(why,bonus){
 const w=weights(S.k),sp=riskShown(w).total,vd=varDecomp(w),fmax=Math.max(...vd.fv)/vd.tot;""")
e.rep(""" let d=dev<band?3:-(dev-band)*32*SIZE().rcNeg;
 if(fmax>0.75)d-=3*SIZE().rcNeg;if(sp<0.02)d-=4;
 return d;""",
""" let d=dev<band?3*(1-dev/band):-(dev-band)*32*SIZE().rcNeg;
 if(fmax>0.75)d-=3*SIZE().rcNeg;if(sp<0.02)d-=4;
 return d;""")
e.rep(""" let d=dev<band?3:-(dev-band)*32*SIZE().rcNeg;
 if(fmax>0.75)d-=3*SIZE().rcNeg;if(sp<0.02)d-=4;d+=(bonus||0);
 const txt=dev<band?`vol ex-ante ${pct(sp)} dans la bande`:`vol ex-ante ${pct(sp)} hors de la bande ±${(band*100).toFixed(0)} %`;""",
""" let d=dev<band?3*(1-dev/band):-(dev-band)*32*SIZE().rcNeg;
 if(fmax>0.75)d-=3*SIZE().rcNeg;if(sp<0.02)d-=4;d+=(bonus||0);
 const txt=dev<band?`vol ex-ante ${pct(sp)} contre ${pct(S.tgt,0)} de mandat, dans la bande`
   :`vol ex-ante ${pct(sp)} contre ${pct(S.tgt,0)} de mandat, ${sp>S.tgt?'au-dessus':'en dessous'} de la bande ±${(band*100).toFixed(0)} %`;""")

e.done("lot 22 — le comite juge la volatilite affichee")
