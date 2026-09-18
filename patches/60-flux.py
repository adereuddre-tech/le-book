# -*- coding: utf-8 -*-
"""Lot 6 — le gérant de flux doit se planter un peu plus souvent que le discrétionnaire.

Mesure de référence (30 graines par style, bot intelligent, copie figée) : le flux survivait
67 % du temps contre 60 % au fondamental, tout en affichant le meilleur score (30,8 M$ contre
26,9). Un style censé être le plus risqué ne peut pas être à la fois le plus rentable et le
plus sûr.

Vérifié dans `tools/bot.js` : le book est dimensionné sur `S.tgt*0.95*modelScale` et **pas**
sur `ddMax`. Le seuil de liquidation est donc un vrai levier pour ce style — baisser `ddMax`
ne fait pas réduire les positions en compensation.

Repli maximal des vingt survivants « flux », décroissant :
0,159 · 0,127 · 0,112 · 0,109 · 0,076 · 0,075 · 0,066 · 0,055 · … puis rien au-dessus de 0,055.
Il y a un trou net entre 0,109 et 0,076 : quatre parties passent tout près du bord, les autres
croisent très loin. Des positions 12,5 % plus grosses (`modelScale` 1,20 → 1,35) portent ces
quatre-là à 0,179 / 0,143 / 0,126 / 0,123, et un seuil ramené à 0,13 les fait toutes basculer.

Trois réglages, tous cohérents avec ce qu'est ce style — un gérant qui joue les flux à
l'intuition, taille gros, et dont la méthode est illisible de l'extérieur :
  - `modelScale` 1,20 → 1,35 : il vise 35 % au-dessus de la volatilité cible.
  - `ddMax` 0,16 → 0,13 : prime broker et investisseurs coupent plus tôt.
  - `incMult` 1,0 → 1,25 : un desk qui tourne vite a plus d'accidents d'exploitation.
`lpMult` reste à 1,60 : le flux ne mourait qu'une fois sur dix des investisseurs, ce n'est pas
là qu'est le problème.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
e.rep("""lpMult:1.60,ddMax:0.16,modelScale:1.20,incMult:1.0""",
      """lpMult:1.60,ddMax:0.13,modelScale:1.35,incMult:1.25""")
e.done("lot 6 — le flux paie sa prise de risque")
