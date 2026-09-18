# -*- coding: utf-8 -*-
"""Lot 10 — deux effets d'événement que personne n'appliquait.

Trouvés par `tools/cover.js` : il compare les clés d'effet écrites dans les anecdotes avec
celles que le code lit réellement. Deux clés n'étaient lues nulle part, alors que le moteur
sait parfaitement les traiter :

- `carry` — « Un book de portage vous est proposé », option « Allouer 10 % du risque ».
  Le texte annonce « environ +0,6 % par trimestre, effacé et au-delà dans un choc », et
  `resolveQuarter` contient exactement cette règle (`if(S.carry)gross+=... -0.035 : 0.006`).
  Mais rien ne posait `S.carry`. Le joueur acceptait un book de portage qui n'existait pas.
- `leak` — « Nouvelle obligation de reporting position par position », option « Se conformer
  strictement ». Le texte annonce que le marché se place devant vos grosses positions, et
  `tcost` applique bien `×1,45` sur les positions de plus de deux unités quand `S.leak` est
  vrai. Mais rien ne posait `S.leak`.

Deux lignes manquantes, dans le même bloc que `noise`, `flighty`, `stopQ` et `leakQ`.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
e.rep("""  if(e.flighty)S.flighty=true;
  if(e.stopQ)S.stopQ=true;
  if(e.noAddQ)S.noAddQ=true;
  if(e.leakQ)S.leakQ=true;""",
"""  if(e.flighty)S.flighty=true;
  if(e.stopQ)S.stopQ=true;
  if(e.noAddQ)S.noAddQ=true;
  if(e.leakQ)S.leakQ=true;
  if(e.carry)S.carry=true;   /* book de portage : le moteur le lit, personne ne le posait */
  if(e.leak)S.leak=true;     /* positions publiées : idem */""")
e.done("lot 10 — deux effets morts branches")
