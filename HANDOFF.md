# Le Book — note de reprise

Jeu de gérant de hedge fund global macro. Fichier unique `index.html` (~492 ko),
publié sur GitHub Pages : https://adereuddre-tech.github.io/le-book/
Dépôt : `adereuddre-tech/le-book`, branche `main`.

## Méthode de travail (à respecter)

- **Réponses en français.**
- **Patchs Python ciblés**, jamais de réécriture du fichier. Chaque patch utilise une
  fonction `rep(old, new, k=1)` qui *assert* le nombre d'occurrences avant de remplacer :
  une ancre ambiguë doit faire échouer le patch, pas produire un remplacement au hasard.
- **Test jsdom d'une partie complète avant publication.** Le harnais est versionné dans
  `tools/` (voir `tools/README.md`) : le récupérer depuis le dépôt en début de session,
  puis `npm i jsdom`.
  - `play.js <fichier> <graine> [--sage] [--size small|mid|mega] [--univ fin|com|ext] [--dur express|normal|saison] [--prof syst|fonda|flux] [--resume N]`
    joue une partie entière jusqu'à `#again` et compte les erreurs (`window.onerror` + jsdomError).
    Le book est posé via `recoBook()`. Une sonde enveloppe `resolveEvent` et compte les écarts
    entre jauges affichées dans le bouton de dépêche et jauges appliquées (0 exigé).
    `--resume N` capture la sauvegarde à la N-ième dépêche, recharge la page à froid et finit la partie.
    Régression type : 9 combinaisons taille × univers, deux styles de jeu, 0 erreur exigée.
    Une partie « normal » prend 3 à 10 s sur un seul cœur : lancer les lots détachés
    (`setsid nohup … &`) et relire le fichier de résultats, sinon la limite de 300 s tombe.
  - `cover3.js` : appelle `evPlans` sur toutes les dépêches ouvertes × 3 styles × 2 univers,
    avec et sans interdiction du comité ; vérifie la forme, l'absence de NaN, que suivre gagne
    plus en poursuite et perd plus en retournement.
  - Captures mobiles (380 px) : Playwright avec `/opt/pw-browsers/chromium-1194/chrome-linux/chrome` ;
    fermer les info-bulles (`.mbox`) et attendre la fin de l'animation `fade` avant la capture.
  - `cover.js` / `cover2.js` : couverture forcée des nouvelles anecdotes / dépêches, chaque choix.
  - `goalchk.js` : rejoue les 108 prédicats d'objectif sur des contextes réels.
  - Anciens outils perdus, non reconstruits : `cover.js`/`cover2.js` (anecdotes/dépêches),
    `goalchk.js` (108 prédicats d'objectif), `resumechk.js` (reprise à chaque point de sauvegarde),
    `featchk.js`, `flowchk.js`, `mprobe2.js`.
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
- **Dépêches** (lot Q) : `screenMacroEvent` → `evPlans(ev,touched)` chiffre deux options,
  `follow` (+2 unités dans le sens du choc) et `none` (« Laisser le modèle » pour `syst`,
  « Ne pas réagir » sinon ; toujours en dernier, c'est le choix du minuteur). Suite du mouvement
  binaire : `S.sc={p,m:[mPoursuite,mRetournement]}`, p ∈ [0,30 ; 0,70]. Tout est déterministe
  une fois `S.sc` tiré : `resolveEvent(ev,touched,plan,imm,navB)` applique exactement les montants
  et les jauges affichés. Coût de suivre : frais (×1,9 + 1,25 pb de glissement), écart au book de
  départ (≤ −3 comité), variation de note de vol ex-ante (±3), dérogation au modèle (−3, `syst`),
  interdiction du comité `S.noAddQ` (−6). Aides pures : `pnlGz`, `riskRc`, `reactGz`.
- **Jauges** : `gauge()` mémorise `S.lastG={lp,rc,lp0,rc0}` ; la barre d'état affiche `lp0 →lp`
  via `gArrow` hors page de book. La clôture du trimestre et les événements du conseil écrivent
  aussi `S.lastG`.
- **Annonce** : ids `none`/`prud`/`fort`. `prud` = « Communication standard », objectif entier,
  sélectionnée par défaut ; `fort` = deux fois l'objectif.
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
9. Dépêches : montants et jauges affichés dans un bouton = montants et jauges appliqués. La
   probabilité affichée `S.sc.ph` est une **lecture** (bruit selon recherche et style) ; l'issue
   est tirée sur la vraie probabilité `S.sc.p`.
10. `S.sc` est validé par forme (`m.length===2`) : une sauvegarde d'avant le lot Q le fait retirer.

## Livré

- **Lot Q** (commit `f2723a2`) : dépêches à deux options, mouvement binaire, tableau
  probabilité / P&L / investisseurs / comité dans chaque bouton, « P&L immédiat ».
- **Lot R** (commit `0e5f5a6`) : jauges Risque et Coûts T alignées, valeurs entières,
  annonce standard par défaut (objectif entier, forte = ×2), flèches `61 →58`,
  concurrence classée par cumul sans « vs vous », brut au net en montants seuls.
  Libellé de jauge raccourci en « Invest. ».
- **Nettoyage** : CSS de l'ancienne barre de couleurs et `applyEventChoice` supprimés,
  lignes « Achat de sources » (toujours nulles) retirées des tableaux, derniers `sgn(x,2)`
  passés à une décimale, coût des ordres affiché en pb. Harnais versionné dans `tools/`.

- **Lot S — simplifications et équilibrage** :
  - `RISKARCH`/`DESKS` réduits à une entrée figée ; achat de sources retiré (`buyRumor`, `qRumor`,
    `mgrQ.rum`, `c.info`) ; haut fait « Tout entendre » = trimestre positif avec recherche renforcée ;
    volet « détail marché par marché » des dépêches retiré ; virgule décimale partout (`dec`).
  - Dépêches : `S.sc={p,ph,ver,m}`. Lecture ±16/±10/±5 pts selon la recherche, ×0,6 pour le flux,
    +4 pts de biais de poursuite pour le quant, une probabilité vérifiée par trimestre pour le
    fondamental (`S.evVerified`).
  - Pop-up des coûts : « payé par le fonds » / « payé par vous » ; valeur du point de base corrigée.
  - Bogue corrigé : la source « vérifiée » du fondamental pouvait être fausse.
  - Intuition du flux affichée sous la lecture du desk (écran du book).
  - Univers : champs `edge` (rendement des signaux T/C/V) et `lpMult` (nervosité investisseurs) :
    bac à sable 0,75 / 0,90, grand bassin 1 / 1, monde entier 1,5 / 1,05.
  - Styles : quant F 0,85 et T/C/V 0,45, capture 0,50, investisseurs ×0,90, et son modèle
    (`recoBook`) ne vise que 80 % de la vol cible (`modelScale`) ; fondamental +4 sources,
    coûts ×1,08.
  - Budgets : salle de marché 4/18/36 pb (réduit : coûts ×1,45) ; contrôle des risques 4/12/16 pb,
    incidents de base 9 %, gravité `RISKS=[2,1.5,0.75]`, comité −1/0/+2 à chaque clôture ;
    recherche 4/18/80 pb.

## Calibration (bot intelligent, `tools/bot.js`)

Méthode : parties appariées (même graine, même style) entre une option et le standard ;
`tools/calib.py`. Le bruit est grand (σ du score ≈ 30 M$ sur 2 ans) : compter 150 parties par
option pour un écart de 2 M$. Les budgets sont payés par la société de gestion, qui ne touche que
20 % de la performance : un budget n'est rentable que si son effet sur le fonds vaut environ cinq
fois son coût. Campagnes : `tools/runner.js` + `tools/loop.sh` sur une **copie figée** du jeu (champ `file`
du plan) : `loop.sh` relit le fichier à chaque tranche, une modification en cours de campagne
fausse les résultats.

### Résultats de calibration (parties de 2 ans, bot intelligent)

| Option | Mesure | Verdict |
|---|---|---|
| Durée longue / courte | score +18 / −16 vs standard, σ plus / moins élevé | conforme |
| Grande / petite taille | +14 / −5, σ 44 / 20 vs 27 | conforme |
| Mandat agressif / prudent | +16 / −6, σ 47 / 18 | conforme |
| Monde entier / bac à sable | ≈ +6 σ 41 / −5 σ 24 (après `edge` 1,5 / 0,75) | conforme |
| Styles quant / fondamental / flux | 28,7 σ 26 / 36,7 σ 33 / 52,6 σ 38 (70 graines appariées) | conforme ; survie du quant 43 % à surveiller |
| Recherche renforcée | rapportait 2,3× son coût à 60 pb → 80 pb (visé ≈ 1,5×) | réglé par proportion, non remesuré |
| Contrôle renforcé | ne rapportait rien à 20 pb → 16 pb et comité +2 | réglé, non remesuré |
| Salle de marché renforcée | ≈ 5,6× ± 2,4 à 30 pb → 36 pb | réglé, incertain |
| Niveaux réduits | recherche et contrôle : perte > économie ; salle de marché : bruit ± 4 M$ | à remesurer |

Limites : le budget total ne pèse qu'environ 13 % des commissions, et l'effet d'un niveau
(2 à 6 M$ sur 2 ans) est de l'ordre de l'erreur type à 80 parties. Remesurer les budgets
demande environ 300 parties appariées par niveau, sur copie figée.

## Reste à faire

### Plus loin
- Production de texte : objectif de 200 anecdotes d'exécution (145 aujourd'hui) et
  300 dépêches (269), plus la démultiplication des textes de débriefing.
- Équilibrage des styles : mesuré sur 24 parties seulement, l'écart est dans le bruit.
  Une mesure sérieuse demande ~200 parties par style.
