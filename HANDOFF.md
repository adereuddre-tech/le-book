# Le Book — note de reprise

Jeu de gérant de hedge fund global macro. Fichier unique `index.html` (~492 ko),
publié sur GitHub Pages : https://adereuddre-tech.github.io/le-book/
Dépôt : `adereuddre-tech/le-book`, branche `main`.

## Méthode de travail (à respecter)

- **Réponses en français.**
- **Patchs Python ciblés**, jamais de réécriture du fichier. Chaque patch utilise une
  fonction `rep(old, new, k=1)` qui *assert* le nombre d'occurrences avant de remplacer :
  une ancre ambiguë doit faire échouer le patch, pas produire un remplacement au hasard.
- **Test jsdom d'une partie complète avant publication.** Harnais dans le bac à sable :
  - `play.js <fichier> <graine> [--sage] [--size small|mid|mega] [--univ fin|com|ext] [--dur express|normal|saison] [--prof syst|fonda|flux]`
    joue une partie entière jusqu'à `#again` et compte les erreurs (`window.onerror` + jsdomError).
    Régression type : 9 combinaisons taille × univers, deux styles de jeu, 0 erreur exigée.
  - `cover.js` / `cover2.js` : couverture forcée des nouvelles anecdotes / dépêches, chaque choix.
  - `goalchk.js` : rejoue les 108 prédicats d'objectif sur des contextes réels.
  - `resumechk.js` : capture la sauvegarde à chaque point, recharge la page à froid, vérifie la reprise.
  - `featchk.js`, `evchk.js`, `flowchk.js`, `mprobe2.js` : difficulté des hauts faits, cohérence
    jauges/résultat des dépêches, corrélation flux/performance, marge utilisée.
- Publication par l'API GitHub (`GET` du sha puis `PUT` sur `contents/index.html`).

## Architecture du fichier

- **Marchés** : `INSTR_ALL` (25 marchés, 5 classes × 5), champ `rk` = rang d'ouverture.
  `MKPERCL={small:3,mid:4,mega:5}` (marchés par classe), `NCLASS={fin:3,com:4,ext:5}` (classes).
  `setUniverse(size,univ)` reconstruit `INSTR`, `N`, `IDX`, `GRP` **et filtre les sept pools
  d'événements** pour qu'aucun marché fermé ne soit cité.
- **Corrélation** : modèle à 4 facteurs (croissance, inflation, dollar, appétit).
  `b` = charges par marché, `COV` construite dans `buildCov()`. Définie-positivité par construction.
  λmin ≈ 0,21 (9 marchés) à 0,12 (25 marchés). |b| moyen 0,369, aucune charge sous 0,15.
- **Choix initiaux (5)** : style (`PROFILES`), risque du mandat (`VOLP`), taille (`SIZES`),
  univers (`UNIVS`), durée (`DUREES`). `RISKARCH` et `DESKS` existent encore mais sont **figés**
  (`arch:'std'`, `desk:'inhouse'`, exécution ×1,00, masse salariale 5 pb) et retirés de l'écran.
- **Pouvoirs propres** : `syst` → book du modèle (`#applymodel`, affiché pour lui seul) ;
  `fonda` → `verified:true`, une source certaine par trimestre dans `genRumors` ;
  `flux` → `hunch:true`, `S.hunch={k,up}` posé dans `planQuarter`, annoncé à l'écran du desk.
- **Budgets** (`BUDGET`, 3 × [4, 18, 40] pb) : salle de marché → coûts `EXECM`, débauchage `RETM`,
  bruit des indicateurs `TCVQ` ; contrôle des risques → incidents `RISKM`/`RISKS`, bande du comité
  `BANDB` via `bandNow()` ; recherche macro → nombre `RESN`, fiabilité `RESREL`, pré-annonces `RESR`.
- **Sources** : toutes ouvertes, `price=0`, plus d'achat. Nombre et qualité pilotés par la recherche.
- **Objectifs** : `QGOALS` (108), tirés à chaque trimestre dans `planQuarter`, soldés à la clôture,
  prédicats sur le contexte de `goalCtx()`. **Le prédicat `t` ne survit pas à `JSON.stringify`** :
  `loadGame` réhydrate `S.goal` depuis `QGOALS` par son nom.
- **Hauts faits** : `FEATS` (36) en 5 paliers (`TIERS`), prédicats `tq` (clôture de trimestre) et
  `tf` (rapport final) ; quatre restent attribués par le code au moment de l'action.
- **Qualificatifs de trimestre** : `QNAMES` (89), prédicats sur le vecteur factoriel réalisé `S.f`,
  les trois génériques marqués `gen:1` ne sortent qu'en dernier recours. `qRegime()`.
- **Textes** : `MACROEV` (269 dépêches), `TRADER_EXEC` (145 anecdotes d'exécution), `TRADER_MID`,
  `STAKE`, `INCIDENTS`, `BOARDEV`, `RUMORS`, `PRESS_SRC` (24), `PRESS_EXTRA`.
- **Sauvegarde** : clé `lebook_save_v2`, `save(point,extra)` / `loadGame()`, table `RESUME`.

## Invariants à ne pas casser

1. `setUniverse` doit tourner **avant** toute restauration de `b` dans `loadGame` : sinon `d.b`
   est plus court que `INSTR` et `normB` lève. C'était la cause du bouton « reprendre » cassé.
2. Un échec de reprise **ne doit pas** appeler `clearSave()`.
3. Tout effet d'événement ou d'exigence citant un symbole doit passer par `IDX[sym]` **gardé**
   (`IDX.X!==undefined`), et les pools sont filtrés par `setUniverse`.
4. Ne jamais relire le journal des jauges par décalage d'indice : l'effet immédiat d'une dépêche
   est stocké dans `S.evImmG`.
5. Le book **repart à plat chaque trimestre** (`S.k` et `S.k0` remis à zéro dans `planQuarter`).
6. Format unique des effets de jauge : `gz(lp,rc)` → « investisseurs −3 • comité −2 ».
   Lignes label/valeur : `gzRows(lp,rc)`.
7. `pk(arr,n)` est un tirage déterministe à mélange avalanche ; le XOR final doit rester `>>>0`
   sinon l'indice devient négatif.
8. Pourcentages à **une** décimale partout (les multiplicateurs et le Sharpe gardent deux).

## Reste à faire (demandé, non livré)

### Lot Q — refonte des événements trimestriels
- Garder le texte descriptif du haut, parfait tel quel.
- « Effet immédiat » → **« P&L immédiat »**.
- Ne garder que **deux options**, nommées selon le style de gestion :
  « suivre le mouvement » et « laisser le modèle » / « ne pas réagir ».
- Supprimer la barre de couleurs des cartes d'option (jugée illisible).
- Chaque description d'option doit tenir **dans le bouton**.
- Mouvement de marché **binaire** : poursuite ou retournement, probabilités **binomiales**.
- Dans chaque bouton, un tableau épuré donnant pour chacun des deux mouvements :
  probabilité, P&L en M$ ou k$, impact investisseurs, impact comité.
- Le choix doit toujours être une prise de risque : gain possible, au prix de coûts de
  transaction, de jauges, et d'un décalage du book par rapport au portefeuille cible.

### Lot R — affichage
- Jauges « Risque » et « Coûts T » : aligner en hauteur sur les jauges de facteurs macro.
- Jauges de facteurs et de risque : valeurs **entières**, sans décimale.
- « Ce que vous annoncez » : communication standard = **l'objectif trimestriel entier**
  (et non la moitié), **sélectionnée par défaut** ; conviction forte = **deux fois** l'objectif.
- Jauges investisseurs et comité en cours de trimestre : afficher `61 → 58` avec flèche et
  couleurs, comme sur la page de book, au lieu de la valeur entre parenthèses.
- Résultat du trimestre → « La concurrence » : classer par **performance cumulée**,
  supprimer la colonne « vs vous ».
- Résultat du trimestre → « Du brut au net » : supprimer la colonne en % de l'encours.

### Plus loin
- Production de texte : objectif de 200 anecdotes d'exécution (145 aujourd'hui) et
  300 dépêches (269), plus la démultiplication des textes de débriefing.
- Équilibrage des styles : mesuré sur 24 parties seulement, l'écart est dans le bruit.
  Une mesure sérieuse demande ~200 parties par style.
