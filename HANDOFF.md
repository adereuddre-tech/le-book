# Le Book — note de reprise

Ce fichier sert à reprendre le développement dans une nouvelle conversation sans repartir de zéro.
Colle-le en entier au début de la discussion, avec la phrase : « voici l'état du projet, reprends à partir de là ».

## Où est le jeu
- Dépôt : `github.com/adereuddre-tech/le-book` — un seul fichier, `index.html` (~300 ko), plus ce `HANDOFF.md`.
- En ligne : `https://adereuddre-tech.github.io/le-book/` (GitHub Pages, branche `main`, racine).
- Le jeu est entièrement autonome : aucune dépendance, aucun build. Seules les polices viennent de Google Fonts.

## Méthode de travail éprouvée
1. Récupérer `index.html`, le copier en `lebookNN.html` dans un bac à sable.
2. Écrire un script Python de patch (`rep(ancien, nouveau)` avec assertion sur le nombre d'occurrences) plutôt que de réécrire le fichier : les remplacements ciblés évitent de casser le reste.
3. Tester avec jsdom (`npm install jsdom`) en pilotant une partie complète par clics simulés : `#found` → `#go` → boucle sur `#pgo`, `#rgo`, `#buds`/`#ok`, `#send`, `#commok`, `#go2`, `.choice`, `#nx`, jusqu'à `#again`. Écouter `window.addEventListener('error')`.
4. Publier via l'API GitHub (`PUT /repos/.../contents/index.html` avec le `sha` courant).

## Architecture du fichier
Un seul `<script>`, sections numérotées :
1. **Univers** — `INSTR` (15 marchés), `BASE_B` (matrice factorielle 15×4), `REG` (7 régimes macro), `TRANS` (chaîne de Markov), `SIG`, `RUMORS` (~72), `MACROEV` (~139 dépêches), `TRADER_EXEC` (~60 anecdotes d'exécution), `TRADER_MID` (~40 interactions), `STAKE` (24 exigences), `INCIDENTS`, `BOARDEV`, `FEATS` (18 hauts faits).
2. **Choix d'ouverture** — `PROFILES`, `RISKARCH`, `DESKS`, `SIZES`, `VOLP`, `BUDGET`, `RECO`.
3. **Aléa** — `mulberry32` avec `rngState` global (sérialisable), `gauss`, `pick`, `drawK`, `uni`.
4. **Risque et coûts** — `weights`, `pvol`, `riskContrib`, `varDecomp`, `tcost` (demi-fourchette + impact en racine du notionnel).
5. **État** — `S`, objet unique ; `newGame`, `planQuarter` (tire régime, facteurs, événements, rumeurs, matrice dérivée), `drawReturns`.
6. **Rendu** — `statusBar` (10 jauges), `showGauge` (pop-ups), `ticker`, `avatar` (SVG procédural), `screenIntro`/`screenSetup`/`screenBudget`/`screenPlay`/`screenComm`/`screenExec`/`screenMacroEvent`/`screenTraderEvent`/`screenRivalEvent`/`screenIncident`/`screenDebrief`/`screenBoard`/`screenFinal`/`screenHall`.
7. **Déroulé** — `phaseOpen → screenBudget → phaseDesk → screenPlay → screenComm → phaseExec → screenExec → phaseLive → stepEvents → resolveQuarter → phaseClose → screenDebrief → screenBoard`.

## Invariants à ne pas casser
- **`S.idx`** est l'indice de performance par part (base 1). Il sert au classement contre les rivaux, au repli, à la perte maximale et au déclenchement de la commission de performance. **Ne jamais comparer `S.nav` à `S.aum0`** : l'encours bouge avec les souscriptions et les rachats.
- **`S.nav`** est en milliards de dollars, quelle que soit la taille du fonds (0,1 / 1 / 10 au départ).
- Le **brut au net** doit rester exactement additif : `perfM = grossM + collM + tcM + feeM + evM + incM`, pourcentages rapportés à `S.navQ0`, flux de capitaux sur une ligne séparée.
- Les **frais** sont calculés sur `navQ0` puis convertis sur `navBefore` ; le plus haut historique est celui de `S.idx`, pas de l'encours.
- Le **budget d'exploitation et l'achat de sources** sont à la charge du gérant (`S.mgrCosts`), pas du fonds. Le score est `S.mgrFees − S.mgrCosts`.
- La **sauvegarde** sérialise `S` + `rngState` + la matrice `b` ; la file d'événements est sérialisée par titre (`evTag`/`evFromTag`), jamais par référence.
- Les **montants** passent par `mm`, `moneyB`, `score`, `pickU`/`inU` : une seule unité par tableau.

## Reste à faire, par ordre de valeur décroissante
1. Quadrupler le pool d'anecdotes d'exécution (60 aujourd'hui, cible 160) et doubler les dépêches macro (139).
2. Équilibrage : la taille « mastodonte » reste très difficile, la « boutique » très permissive ; le mode 1 Md$ est le mieux calibré.
3. Idées en attente de validation : voir la liste soumise en fin de conversation (marchés qui ferment, contraintes de mandat, deuxième gérant, saisons, etc.).
