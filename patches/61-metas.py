# -*- coding: utf-8 -*-
"""Lot 6 (fin) — textes de vitrine et d'aide restés à l'ancienne version du jeu.

Le titre, la description et l'aperçu de partage annonçaient « un fonds global macro de
100 milliards », « quinze marchés » et « des rumeurs à acheter ». Le fonds fait 75 à 150 M$,
il y a 25 marchés, et les sources ne s'achètent plus depuis le lot S. Deux textes d'aide
annonçaient aussi des montants « en milliards ».
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()

e.rep("""<title>Le Book — prenez les commandes d'un fonds global macro de 100 milliards</title>""",
      """<title>Le Book — prenez les commandes d'un fonds global macro</title>""")
e.rep("""<meta name="description" content="Un jeu de gestion : quinze marchés, huit trimestres, quatre concurrents, des investisseurs nerveux et un comité des risques qui vous surveille. Prouvez que ce n'était pas de la chance.">""",
      """<meta name="description" content="Un jeu de gestion : vingt-cinq marchés, huit trimestres, quatre concurrents, des investisseurs nerveux et un comité des risques qui vous surveille. Prouvez que ce n'était pas de la chance.">""")
e.rep("""<meta property="og:title" content="Le Book — un fonds global macro de 100 milliards">""",
      """<meta property="og:title" content="Le Book — un fonds global macro">""")
e.rep("""<meta property="og:description" content="Quinze marchés, trois tailles de fonds, huit trimestres, quatre concurrents, des rumeurs à acheter et des dépêches qui vous interrompent. Prouvez que ce n'était pas de la chance.">""",
      """<meta property="og:description" content="Vingt-cinq marchés, trois tailles de fonds, huit trimestres, quatre concurrents, des sources incertaines et des dépêches qui vous interrompent. Prouvez que ce n'était pas de la chance.">""")
e.rep("""<p>À vous de décider vos positions sur <strong>15 marchés</strong> — actions, taux, devises, matières premières, exotiques — à l'achat ou à la vente. Le desk vous remonte des rumeurs à acheter, le monde vous envoie des dépêches,""",
      """<p>À vous de décider vos positions sur <strong>jusqu'à 25 marchés</strong> — actions, taux, devises, matières premières, exotiques — à l'achat ou à la vente. Le desk vous remonte ses sources, le monde vous envoie des dépêches,""")
e.rep("""dimensionnée en inverse de la vol du marché ; le notionnel correspondant s'affiche en milliards.""",
      """dimensionnée en inverse de la vol du marché ; le notionnel correspondant s'affiche à côté de chaque ordre.""")
e.rep("""openModal('Capital',`<p>Encours net du fonds, en milliards de dollars, tel que le voient les investisseurs.""",
      """openModal('Capital',`<p>Encours net du fonds, tel que le voient les investisseurs.""")

e.done("lot 6 — textes de vitrine remis à jour")
