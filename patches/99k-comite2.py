# -*- coding: utf-8 -*-
"""Lot 23 — performance affichée avec le latent, et comité vraiment déplafonné.

1. La tuile « Perf. » montrait `S.idx-1`, c'est-à-dire la performance des trimestres CLOS.
   Le ruban, lui, intègre le latent du trimestre en cours. D'où deux chiffres différents à
   l'écran pour la même chose. La tuile intègre désormais `liveRet()`, la même grandeur que
   le ruban et que le mi-parcours.
2. Le comité annonçait −20 et n'appliquait que −15 : `gauge()` borne à ±15 dans les deux sens.
   C'est une violation de « affiché = appliqué », et cela rendait toute aggravation de la
   sanction invisible au-delà du plafond. La borne basse passe à −80 pour le comité ; la
   borne haute reste à +15, parce qu'aucun bienfait ne justifie de gagner 80 points d'un coup.
3. La sanction devient surlinéaire : `(dev−band)·32·(1+(dev−band))`. Dans la capture, un
   risque à 70 pour un mandat à 30 donnait −21 ; il donne maintenant environ −67. Elle reste
   proportionnelle à `SIZE().rcNeg` et adossée à `bandNow()`, donc **le budget de contrôle
   des risques élargit toujours la bande** et amortit la sanction : dépenser reste utile.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()

e.rep(""" dlp=Math.max(-15,Math.min(15,dlp||0));drc=Math.max(-15,Math.min(15,drc||0));""",
""" /* le comité peut sanctionner très au-delà de 15 points quand le risque explose le mandat ;
    aucun bienfait, en revanche, ne justifie d'en gagner autant d'un coup */
 dlp=Math.max(-15,Math.min(15,dlp||0));drc=Math.max(-80,Math.min(15,drc||0));""")
e.rep(""" let d=dev<band?3*(1-dev/band):-(dev-band)*32*SIZE().rcNeg;
 if(fmax>0.75)d-=3*SIZE().rcNeg;if(sp<0.02)d-=4;
 return d;""",
""" const ex=Math.max(0,dev-band);
 let d=dev<band?3*(1-dev/band):-ex*32*(1+ex)*SIZE().rcNeg;
 if(fmax>0.75)d-=3*SIZE().rcNeg;if(sp<0.02)d-=4;
 return d;""")
e.rep(""" let d=dev<band?3*(1-dev/band):-(dev-band)*32*SIZE().rcNeg;
 if(fmax>0.75)d-=3*SIZE().rcNeg;if(sp<0.02)d-=4;d+=(bonus||0);""",
""" const ex=Math.max(0,dev-band);
 let d=dev<band?3*(1-dev/band):-ex*32*(1+ex)*SIZE().rcNeg;
 if(fmax>0.75)d-=3*SIZE().rcNeg;if(sp<0.02)d-=4;d+=(bonus||0);""")
e.rep(""" const dd=1-S.idx/S.peakIdx,cum=S.idx-1;""",
""" /* la performance affichée doit dire la même chose que le ruban : latent compris */
 const lat=(S.phase==='events'&&typeof liveRet==='function')?liveRet():0;
 const ixL=S.idx*(1+lat);
 const dd=1-ixL/Math.max(S.peakIdx,ixL),cum=ixL-1;""")

e.done("lot 23 — perf latente, comite deplafonne")
