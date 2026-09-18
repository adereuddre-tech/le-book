# -*- coding: utf-8 -*-
"""Lot 10 — `halfOn` : une chaîne au lieu d'un tableau, et un gestionnaire non gardé.

Trouvé par `tools/cover2.js`, qui force chaque choix de chaque anecdote :
`TypeError: e.halfOn.forEach is not a function`.

Deux défauts distincts :
1. Une anecdote écrit `halfOn:'ZW'` (chaîne) là où toutes les autres écrivent un tableau.
   Le gestionnaire des anecdotes de desk tolère les deux (`Array.isArray(...)?...:[...]`),
   celui du conseil et des exigences appelle `.forEach` directement et casse.
2. Ce même gestionnaire appelle `setK(IDX[sy], …)` sans garder `IDX[sy]!==undefined`, ce que
   l'invariant 3 interdit : sur un univers réduit, le marché cité peut ne pas exister et on
   écrit alors dans `S.k[undefined]`. Silencieux, et bien pire qu'une exception.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
e.rep("""e:{tcMultOn:['ZW'],tcMult:0.6,halfOn:'ZW'}""",
      """e:{tcMultOn:['ZW'],tcMult:0.6,halfOn:['ZW']}""")
e.rep("""  if(e.zeroOn)e.zeroOn.forEach(sy=>setK(IDX[sy],0));
  if(e.halfOn)e.halfOn.forEach(sy=>{const i=IDX[sy];setK(i,Math.trunc(S.k[i]/2))});""",
"""  /* tableau ou symbole seul, et jamais d'écriture sur un marché fermé (invariant 3) */
  const syms=v=>(Array.isArray(v)?v:[v]).filter(sy=>IDX[sy]!==undefined);
  if(e.zeroOn)syms(e.zeroOn).forEach(sy=>setK(IDX[sy],0));
  if(e.halfOn)syms(e.halfOn).forEach(sy=>{const i=IDX[sy];setK(i,Math.trunc(S.k[i]/2))});""")

# ── deux textes qui offrent des milliards à un fonds de 100 millions ──
# `cover2.js` relève 27 textes libellés en milliards ; 25 parlent du monde extérieur (une
# adjudication du Trésor, un rachat d'entreprise) et sont légitimes. Deux parlent de l'argent
# du joueur et ne le sont pas.
e.rep("""Je peux prendre 4 Md$ de contrats à mi-fourchette.""",
      """Je peux prendre 400 M$ de contrats à mi-fourchette.""")
e.rep("""  p:"12 Md$ disponibles immédiatement, assortis d'une fenêtre de rachat trimestrielle sans préavis.",""",
      """  p:"Une souscription de 12 % de votre encours, disponible immédiatement, assortie d'une fenêtre de rachat trimestrielle sans préavis.",""")
e.done("lot 10 — halfOn normalise et garde")
