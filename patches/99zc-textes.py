# -*- coding: utf-8 -*-
"""Lot 40 — relecture des textes descriptifs contre les mécanismes à jour.

Chaque correction ci-dessous a été vérifiée contre la valeur lue dans le code, pas contre un
souvenir de lot. Les chiffres faux :
  - quant : « 60 % du mouvement capté » — `capture` vaut 0,50 ;
  - fondamental : « pré-annonces 10 pts plus souvent » — `rumBonus` 0,18 contre 0,05 : 13 pts ;
  - flux : « l'intuition ne se trompe qu'une fois sur quatorze » — `rng()<0.78` depuis le lot 30,
    elle se trompe environ une fois sur cinq ; « vise 120 % de la vol cible » — `modelScale` 1,35 ;
    incidents +25 % (`incMult` 1,25) jamais annoncés ;
  - mandat agressif : « une performance qui bouge trois fois plus » — 30 % contre 20 %, moitié
    plus ; « jusqu'à ±5 unités, en surlevier » — `maxk` vaut 5 pour tous les mandats ;
  - monde entier : « le fret et les dérivés climatiques réservés au mastodonte » — le fret (rang 4)
    s'ouvre dès le full-floor, seules les précipitations (rang 5) attendent le mastodonte ;
  - bac à sable : investisseurs 10 % moins nerveux (`lpMult` 0,90), jamais annoncé.
Les règles périmées :
  - tutoriel : « sous 4, le comité vous retire le mandat ; à zéro, les investisseurs partent »
    (morts supprimées au lot 25) et « les six jauges » ;
  - info-bulle d'exécution, pop-up des gains, pop-up des coûts, note du débriefing : « les coûts
    d'exécution ne touchent pas le fonds » — faux depuis le lot 38 (impact de marché) ;
  - « à sec, les niveaux de budget renforcés se verrouillent » — il y a onze crans ;
  - objectifs « porter la recherche / la salle au maximum » : le prédicat demande le cran 9
    « Renforcé » ou au-delà ;
  - « en deux ans » / « sur deux ans » : la durée se choisit (un, deux ou trois ans).
Les pouvoirs sur la lecture des dépêches (biais +4 pts du quant, lecture 40 % plus précise du
flux, probabilité exacte une fois par trimestre pour le fondamental) sont ajoutés aux fiches :
ils existent depuis le lot S et aucune fiche ne les disait.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
Q="'"   # chaînes JS entre guillemets doubles : apostrophe non échappée

# ── profils ────────────────────────────────────────────────────────────────────
e.rep("['g',\"le modèle recale vite : 60 % du mouvement capté après un ajustement\"]",
      "['g',\"le modèle recale vite : 50 % du mouvement capté après un ajustement\"],['b',\"le modèle aime la tendance : il surestime de 4 pts la probabilité qu"+Q+"une dépêche se prolonge\"]")
e.rep("['g',\"les pré-annonces d"+Q+"événements vous parviennent 10 pts plus souvent\"]",
      "['g',\"les pré-annonces d"+Q+"événements vous parviennent 13 pts plus souvent\"],['g',\"une fois par trimestre, la probabilité de suite d"+Q+"une dépêche vous est donnée exacte\"]")
e.rep("et elle ne se trompe qu"+Q+"une fois sur quatorze environ. Ne demandez pas comment\"]",
      "et elle ne se trompe qu"+Q+"environ une fois sur cinq. Ne demandez pas comment\"],['g',\"vous lisez les dépêches mieux que personne : probabilités 40 % plus précises\"]")
e.rep("['b',\"votre desk vise 120 % de la vol cible : plus de rendement, plus de secousses\"]",
      "['b',\"votre desk vise 135 % de la vol cible : plus de rendement, plus de secousses\"],['b',\"incidents opérationnels +25 % : on va vite, on vérifie peu\"]")

# ── mandats, univers ───────────────────────────────────────────────────────────
e.rep("Mêmes frais que les autres mandats : 2 % et 20 %, appliqués à une performance qui bouge trois fois plus.",
      "Mêmes frais que les autres mandats : 2 % et 20 %, appliqués à une performance qui bouge moitié plus que celle du mandat standard.")
e.rep("['g',\"unité de risque : 3,75 % de vol, positions 50 % plus grosses — jusqu"+Q+"à ±5 unités, en surlevier\"]",
      "['g',\"unité de risque : 3,75 % de vol : à nombre d"+Q+"unités égal, des positions 50 % plus grosses\"]")
e.rep("[\"b\",\"le fret et les dérivés climatiques restent réservés au mastodonte\"]",
      "[\"b\",\"le fret ne s"+Q+"ouvre qu"+Q+"à partir du full-floor, les dérivés climatiques qu"+Q+"au mastodonte\"]")
e.rep("[\"g\",\"univers lisible : chaque position se raconte en une phrase\"]",
      "[\"g\",\"univers lisible : chaque position se raconte en une phrase, et les investisseurs sont 10 % moins nerveux\"]")

# ── tutoriel et info-bulles ────────────────────────────────────────────────────
e.rep("""{id:0,t:"Les six jauges, en haut de l'écran",
  h:`<p>Tout le jeu se lit dans cette barre. <b>Investisseurs</b> et <b>Comité des risques</b> sont les deux jauges qui peuvent mettre fin à la partie : sous 4, le comité vous retire le mandat ; à zéro, les investisseurs partent. Elles ne réagissent pas à la même chose — les investisseurs regardent la performance et les rachats, le comité regarde la discipline de risque.</p>""",
"""{id:0,t:"Les jauges, en haut de l'écran",
  h:`<p>Tout le jeu se lit dans cette barre. La <b>confiance</b> résume deux jugements : celui des investisseurs, qui regardent la performance, et celui du comité des risques, qui regarde la discipline. Sous 20, l'un comme l'autre fait partir de l'argent par des rachats. La partie ne s'arrête que si l'encours tombe sous 40 % de son niveau de départ.</p>""")
e.rep("<p>Les chiffres annoncés dans les options sont exacts : « coûts −40 % » réduit vraiment de 40 % la facture de transaction du trimestre sur les marchés concernés. Les économies d'exécution se paient presque toujours en points de comité.</p>",
      "<p>Les chiffres annoncés dans les options sont exacts : « coûts −40 % » réduit vraiment de 40 % la facture de courtage, que paie votre société. Mais l'impact de marché, lui, est payé par le fonds, et il suit la manière d'exécuter : payer le bloc protège le prix moyen, négocier un rabais le dégrade. Chaque bouton annonce les deux, avec l'effet sur les jauges.</p>")

# ── pop-ups des gains et des coûts ─────────────────────────────────────────────
e.rep("En face, le budget d'exploitation et les coûts d'exécution sont à votre charge, pas à celle des investisseurs, et vous ne pouvez engager que ce que vous avez en caisse : à sec, les niveaux de budget renforcés se verrouillent et vous ne pouvez plus passer d'ordres coûteux.",
      "En face, le budget d'exploitation et la facture de courtage sont à votre charge — l'impact de marché, lui, est payé par le fonds — et vous ne pouvez engager que ce que vous avez en caisse : à sec, les crans de budget les plus chers se verrouillent et vous ne pouvez plus passer d'ordres coûteux.")
e.rep("<p>La jauge additionne deux factures. Seuls les <em>frais de gestion</em> sont payés par le fonds et pèsent sur sa performance — et ils vous sont versés dès l'ouverture du trimestre. Le <em>budget d'exploitation</em> et les <em>coûts de transaction</em> sont payés par votre société de gestion : ils ne touchent pas le fonds, ils viennent en déduction de vos gains, et vous ne pouvez engager que ce que vous avez en caisse. Un point de base vaut <em>${mm(S.nav*1e-4)}</em>.</p>",
      "<p>La jauge additionne deux factures. Le fonds paie les <em>frais de gestion</em>, qui vous sont versés dès l'ouverture du trimestre, et l'<em>impact de marché</em> de vos ordres, qui dégrade son prix moyen. Votre société de gestion paie le <em>budget d'exploitation</em> et la <em>facture de courtage</em> : ils viennent en déduction de vos gains, et vous ne pouvez engager que ce que vous avez en caisse. Un point de base vaut <em>${mm(S.nav*1e-4)}</em>.</p>")
e.rep("""[`Frais de gestion (${(VOL().mgmt*400).toFixed(1).replace('.',',')} % par an)`,`${(VOL().mgmt*1e4).toFixed(0)} pb`,inU(-VOL().mgmt*S.nav,UC)],""",
      """[`Frais de gestion (${(VOL().mgmt*400).toFixed(1).replace('.',',')} % par an)`,`${(VOL().mgmt*1e4).toFixed(0)} pb`,inU(-VOL().mgmt*S.nav,UC)],
     ...(S.execSlipQ?[['Impact de marché du trimestre',`${(-S.execSlipQ/S.nav*1e4).toFixed(0)} pb`,inU(S.execSlipQ,UC)]]:[]),""")
e.rep("['Coûts de transaction'+(S.phase==='book'?' (en préparation)':' (engagés)')",
      "['Facture de courtage'+(S.phase==='book'?' (en préparation)':' (engagée)')")

# ── débriefing ─────────────────────────────────────────────────────────────────
e.rep('<div class="attr"><span class="an">Dépêches, incidents et desk</span>',
      '<div class="attr"><span class="an">Dépêches, incidents, desk et impact de marché</span>')
e.rep("<p class=\"note\">Les coûts d'exécution du trimestre (${mm(-o.P.tcM)}) n'apparaissent pas ici : ils sont à votre charge, pas à celle du fonds.",
      "<p class=\"note\">La facture de courtage du trimestre (${mm(-o.P.tcM)}) n'apparaît pas ici : elle est à votre charge, pas à celle du fonds. L'impact de marché de vos ordres, lui, est compté plus haut, avec les dépêches et le desk.")

# ── objectifs : le prédicat demande le cran 9 « Renforcé » ou au-delà ──────────
e.rep('d:"Porter la recherche macro au maximum et battre la médiane des concurrents."',
      'd:"Porter la recherche macro au cran « Renforcé » ou au-delà, et battre la médiane des concurrents."')
e.rep('d:"Porter la salle de marché au maximum et garder les coûts de transaction sous 22 points de base."',
      'd:"Porter la salle de marché au cran « Renforcé » ou au-delà, et garder les coûts de transaction sous 22 points de base."')
e.rep('d:"Finir un trimestre positif avec une recherche macro renforcée."',
      'd:"Finir un trimestre positif avec la recherche macro au cran « Renforcé » ou au-delà."')

# ── la durée se choisit ─────────────────────────────────────────────────────────
e.rep("<strong>Votre objectif : encaisser le plus de commissions possible en deux ans sans vous faire débarquer.</strong>",
      "<strong>Votre objectif : encaisser le plus de commissions possible sur la durée de votre mandat sans vous faire débarquer.</strong>")
e.rep("<span>Encaisser le plus de commissions possible sur deux ans : la gestion sur l'encours, la performance au-dessus du plus haut historique. C'est votre score.</span>",
      "<span>Encaisser le plus de commissions possible sur la durée du mandat — un, deux ou trois ans : la gestion sur l'encours, la performance au-dessus du plus haut historique. C'est votre score.</span>")
e.done("lot 40 — textes descriptifs remis a jour")
