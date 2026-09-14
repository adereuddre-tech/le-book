# Le Book — note de reprise

À coller en entier au début d'une nouvelle conversation, avec : « voici l'état du projet, reprends à partir de là ».

## Où est le jeu
- Dépôt : `github.com/adereuddre-tech/le-book` — `index.html` (~315 ko, tout le jeu) et ce fichier.
- En ligne : `https://adereuddre-tech.github.io/le-book/` (GitHub Pages, `main`, racine).
- Autonome : pas de build, pas de dépendance. Seules les polices viennent de Google Fonts.
- **Le fichier se télécharge sans jeton** : `curl https://raw.githubusercontent.com/adereuddre-tech/le-book/main/index.html` (vérifié, 200). Inutile de le joindre à un projet.
- Publier demande un jeton GitHub *fine-grained* avec accès au dépôt et **Contents : read and write** ; l'activation de Pages est déjà faite.

## Méthode de travail éprouvée
1. Télécharger `index.html`, le copier en `lebookNN.html` dans un bac à sable.
2. Patcher avec un script Python à base de `rep(ancien, nouveau)` qui **assert le nombre d'occurrences** — jamais de réécriture globale, jamais de regex large : deux régressions sérieuses sont venues de là.
3. Tester avec jsdom (`npm install jsdom`) en pilotant une partie complète : `#found` → `#go` → boucle sur `#pgo`, `#rgo`, `#buds`/`#ok`, `#send` (+ `[data-buyall]`, `#applymodel`), `#commok`, `#go2`, `.choice`, `#nx`, jusqu'à `#again`. Écouter `window.addEventListener('error')` et exiger zéro erreur.
4. Publier via l'API GitHub : `GET` puis `PUT /repos/adereuddre-tech/le-book/contents/index.html` avec le `sha` courant, corps JSON écrit dans un fichier temporaire (`-d @fichier`) car la ligne de commande déborde.

## Architecture du fichier
Un seul `<script>` :
1. **Univers** — `INSTR` (15 marchés : 3 actions, 3 taux, 3 devises, 3 matières, 3 exotiques), `BASE_B` (matrice 15×4), `REG` (7 régimes), `TRANS` (Markov), `RUMORS` (~72), `MACROEV` (~139), `TRADER_EXEC` (~60), `TRADER_MID` (~40), `STAKE` (24), `INCIDENTS`, `BOARDEV`, `FEATS` (18), `PRESS_SRC` / `PRESS_EXTRA`.
2. **Choix d'ouverture** — `PROFILES`, `RISKARCH`, `DESKS`, `SIZES`, `VOLP`, `BUDGET`, `RECO` (option recommandée, toujours au milieu de sa liste et présélectionnée).
3. **Aléa** — `mulberry32` avec `rngState` global sérialisable, `gauss`, `pick`, `drawK`, `uni`.
4. **Risque et coûts** — `weights`, `pvol`, `riskContrib`, `varDecomp`, `tcost` (demi-fourchette + impact en racine du notionnel).
5. **État** — `S` unique ; `newGame`, `planQuarter`, `drawReturns`, `recoBook` (book conseillé, systématique seulement, calibré sur la vol cible).
6. **Rendu** — `statusBar` (10 jauges + bandeau), `showGauge`, `ticker`, `avatar` (SVG procédural), `armTimer` (minuteur circulaire flottant), tous les `screenX`, `resultCard`, `phase`.
7. **Déroulé** — `phaseOpen → screenBudget → phaseDesk → screenPlay → screenComm → phaseExec → screenExec → phaseLive → stepEvents → resolveQuarter → phaseClose → screenDebrief → screenBoard`.

## Invariants à ne pas casser
- **`S.idx`** : indice de performance par part, base 1. Sert au classement contre les rivaux, au repli, à la perte maximale et au déclenchement de la commission de performance. **Ne jamais comparer `S.nav` à `S.aum0`** — l'encours bouge avec les flux.
- **`S.nav`** en milliards de dollars quelle que soit la taille (0,1 / 1 / 10 au départ).
- **Brut au net exactement additif** : `perfM = grossM + collM + tcM + feeM + evM + incM`, pourcentages sur `S.navQ0`, flux de capitaux sur une ligne séparée.
- **Frais** calculés sur `navQ0` puis convertis sur `navBefore` ; plus haut historique sur `S.idx`.
- **Budget d'exploitation et achat de sources à la charge du gérant** (`S.mgrCosts`), débités en temps réel. Score = `S.mgrFees − S.mgrCosts`, affiché par `score()` à trois chiffres significatifs.
- **Sauvegarde** : `S` + `rngState` + matrice `b` ; file d'événements sérialisée par titre (`evTag`/`evFromTag`), jamais par référence.
- **Montants** : `mm`, `moneyB`, `score`, et `pickU`/`inU` pour n'avoir qu'une seule unité par tableau.
- **Tableaux** : libellés qui reviennent à la ligne, jamais de troncature par points de suspension ; valeurs insécables à droite.

## Calibrage actuel
- Budget d'exploitation : réduit 8 pb / standard **55 pb (2,2 % par an)** / renforcé 126 pb par trimestre.
- Rumeurs : 1,4 / 3,5 / 8 pb selon la fiabilité, 5,5 pb pour une pré-annonce, × 1,3 / 1,0 / 0,6 selon le budget recherche.
- Unité de risque = vol cible ÷ 8 ; positions de −5 à +5, surlevier au-delà de ±3.
- Tailles : boutique 100 M$ (permissive), fonds établi 1 Md$ (le mieux calibré, recommandé), mastodonte 10 Md$ (très dur).

## Reste à faire
1. Quadrupler `TRADER_EXEC` (60 → 160) et doubler `MACROEV` (139 → ~280). Pure production de texte.
2. Rééquilibrer les tailles : la boutique est trop permissive, le mastodonte presque injouable.
3. Idées proposées, non validées : appels de marge forcés, corrélation réalisée affichée contre celle du modèle, plafond de capacité, lock-up et gates, second gérant, objectif secret par partie, mode saison sur quatre ans, revente de rumeur à un concurrent, ordres conditionnels, exotiques réservés aux fonds ≥ 1 Md$, fusion de deux postes de budget, tutoriel du premier trimestre.
