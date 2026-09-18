# -*- coding: utf-8 -*-
"""Lot 7 — `tcBp` du contexte d'objectif était mille fois trop petit.

Trouvé par `tools/goalchk.js` reconstruit : sur 104 clôtures réelles, les objectifs
« L'exécution frugale » (tcBp < 15) et « L'exécution chirurgicale » (tcBp < 8, bonus 0,10 —
la deuxième plus grosse prime du jeu) étaient vrais **à tous les coups**.

Cause : `tcBp = |tcM| / (navB*1000) * 1e4`. `tcM` est en Md$ et `navB` aussi ; le `*1000`
ramenait le dénominateur en M$ et divisait le résultat par mille. Défaut antérieur aux lots
1 à 6, invisible parce que les deux objectifs étaient simplement toujours gagnés.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
e.rep("""tcBp:Math.abs(S.qPnl?S.qPnl.tcM:0)/Math.max(1e-9,navB*1000)*1e4,""",
      """tcBp:Math.abs(S.qPnl?S.qPnl.tcM:0)/Math.max(1e-9,navB)*1e4,""")

# ── seuils recalés sur la distribution réellement mesurée ──
# Coût d'exécution par trimestre, 104 clôtures, bot intelligent, après la correction d'unité :
#   décile 19 · quartile 26 · médiane 33 · quartile 60 · décile 83 · max 142 pb de l'encours.
# Les seuils écrits (15, 12, 10, 8 pb) dataient d'un monde où ouvrir un book coûtait 4 pb :
# corrigés, ils devenaient tous inatteignables. Recalés sur des quantiles, prime croissante
# avec la rareté.
e.rep("""coûts de transaction du trimestre sous 15 points de base de l'encours.",t:c=>c.tcBp<15,b:0.06}""",
      """coûts de transaction du trimestre sous 26 points de base de l'encours.",t:c=>c.tcBp<26,b:0.06}""")
e.rep("""Garder les coûts de transaction sous 8 points de base de l'encours.",t:c=>c.tcBp<8,b:0.10}""",
      """Garder les coûts de transaction sous 16 points de base de l'encours.",t:c=>c.tcBp<16,b:0.10}""")
e.rep("""garder les coûts de transaction sous 12 points de base.",t:c=>c.budExec===2&&c.tcBp<12,b:0.08}""",
      """garder les coûts de transaction sous 22 points de base.",t:c=>c.budExec===2&&c.tcBp<22,b:0.08}""")
e.rep("""iane avec moins de dix points de base de coûts de transaction.",t:c=>c.rel>0&&c.tcBp<10,b:0.12}""",
      """iane avec moins de vingt points de base de coûts de transaction.",t:c=>c.rel>0&&c.tcBp<20,b:0.12}""")
e.done("lot 7 — seuils de cout recales")
