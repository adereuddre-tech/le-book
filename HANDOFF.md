# Le Book — note de reprise

Jeu de gérant de hedge fund global macro. Fichier unique `index.html` (~492 ko),
publié sur GitHub Pages : https://adereuddre-tech.github.io/le-book/
Dépôt : `adereuddre-tech/le-book`, branche `main`.

## Méthode de travail (à respecter)

- **Réponses en français.**
- **Patchs Python ciblés**, jamais de réécriture du fichier. Chaque patch utilise une
  fonction `rep(old, new, k=1)` qui *assert* le nombre d'occurrences avant de remplacer :
  une ancre ambiguë doit faire échouer le patch, pas produire un remplacement au hasard.
- **Un lot par fichier, rejouable.** `base.html` est le fichier publié intact, `patches/NN-*.py`
  applique un lot chacun (via `patches/_lib.py`), `build.sh` reconstruit `index.html` en
  rejouant tout dans l'ordre. Une session coupée ne perd rien : il suffit de relancer
  `./build.sh`. Chaque patch porte en tête le constat mesuré qui le justifie.
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
  - `camp.sh` : campagne n graines × 3 styles sur une copie figée, vers un fichier de résultats
    dépouillé par `summ2.py` (score, écart-type, médiane, survie, causes de fin).
  - `cover.js` : audit **statique** des effets d'événement. Compare les clés écrites dans les
    anecdotes avec celles que le code lit réellement (une clé que personne ne lit est un effet
    mort : le joueur paie, rien n'arrive), vérifie qu'aucun effet de jauge ne dépasse la borne
    ±15 de `gauge()` — au-delà le texte promet plus que ce qui est appliqué — et qu'aucun
    effet de trésorerie ne sort d'une bande plausible de l'encours.
  - `cover2.js` : couverture **forcée**. Ouvre chaque anecdote de chaque pool et clique chaque
    choix (662 choix), en vérifiant qu'aucune erreur n'est levée, qu'aucun « undefined »,
    « NaN » ni « [object » n'apparaît dans ce que le joueur lit, et que l'état reste fini.
    Signale aussi les textes libellés en milliards, hérités du fonds à 100 Md$.
  - `evgchk.js` : vérifie que la flèche de la barre d'état, sur le bilan d'une dépêche,
    raconte la même chose que la ligne « Effets » de la carte.
  - `budchk.js` : contrôle la contrainte de trésorerie au premier trimestre, aux trois tailles.
  - `goalchk.js` : rejoue les 108 prédicats d'objectif et les 36 prédicats de haut fait sur
    des contextes **réels**, capturés à chaque clôture et à chaque fin de partie par une sonde
    injectée dans la page (`playGame({probe,collect})`). Signale : prédicat qui lève, prédicat
    qui ne rend pas un booléen, prédicat jamais vrai, prédicat toujours vrai, et prédicat qui
    lit un champ absent du contexte — ce dernier cas rend `false` en silence et c'est le plus
    vicieux. Indispensable parce que le jeu évalue ces prédicats dans un `try/catch` muet :
    `FEATS.forEach(f=>{if(f.tq){try{...}catch(e){}}})`. Un prédicat cassé ne dit rien.
    Il imprime aussi la distribution du coût d'exécution par trimestre.
  - `powerchk.js` : vérifie les pouvoirs propres des styles. À rejouer **avant et après** tout
    lot touchant aux sources ou aux dépêches, et à comparer au fichier publié.
  - Anciens outils perdus, non reconstruits : `flowchk.js`, `mprobe2.js`. `goalchk.js` couvre
    ce que faisait `featchk.js`.
- Publication par l'API GitHub (`GET` du sha puis `PUT` sur `contents/index.html`). Le bac à
  sable ne contient aucun jeton : il faut en fournir un (fine-grained PAT, *Contents:
  read and write*) à chaque session, ou publier à la main.

## Architecture du fichier

- **Marchés** : `INSTR_ALL` (25 marchés, 5 classes × 5), champ `rk` = rang d'ouverture.
  `MKPERCL={small:3,mid:4,mega:5}` (marchés par classe), `NCLASS={fin:3,com:4,ext:5}` (classes).
  `setUniverse(size,univ)` reconstruit `INSTR`, `N`, `IDX`, `GRP` **et filtre les sept pools
  d'événements** pour qu'aucun marché fermé ne soit cité.
- **Flux aléatoires nommés** : `reseed(canal)` reseme le générateur depuis
  `hash32(graine, canal, trimestre)` à chaque frontière de phase — `mkt` (régime et vecteur
  factoriel), `ev` (file d'événements), `mat` (dérive de la matrice, ruptures, T/C/V,
  rendements réalisés), `riv`, `rum`, `sc<N>` (l'issue de la N-ième dépêche), `res` (clôture).
  Le chemin de marché d'un trimestre ne dépend donc plus de ce que les autres phases ont
  consommé. Ne pas ajouter de tirage avant un `reseed` en croyant que c'est sans effet : c'est
  précisément l'inverse, tout tirage inséré **après** un resemis décale son canal.
  La sauvegarde est inchangée : `rngState` enregistre la position, les resemis sont rejoués.
- **Corrélation** : modèle à 4 facteurs (croissance, inflation, dollar, appétit).
  `b` = charges par marché, `COV` construite dans `buildCov()`. Définie-positivité par construction.
  λmin ≈ 0,21 (9 marchés) à 0,12 (25 marchés). |b| moyen 0,369, aucune charge sous 0,15.
- **Économie du gérant** : la société de gestion a une trésorerie. `mgrNet()` = commissions
  encaissées − tout ce qui a été payé, coûts d'exécution du trimestre en cours compris ;
  `mgrCash()` = `mgrNet()` + `S.mgrCap0` (capital de départ, 2 % de l'encours initial).
  **Commission de gestion versée à l'ouverture** du trimestre (fin de `planQuarter`,
  `S.qMgmtM`) ; **performance et bonus d'objectif à la clôture**. Les coûts d'exécution sont
  à la charge du gérant (`S.mgrCosts`), plus du fonds : `tcM` est affiché au débriefing mais
  n'entre pas dans `perfM`. On ne peut engager que ce qu'on a en caisse : niveaux de budget
  verrouillés (`budgetBpIf`), et sur le book chaque **case** de position est grisée dès que
  son coût dépasse la trésorerie (`costIf`, `segAfford`) — mesuré : 0 % de cases grisées à
  trésorerie confortable, 55 % à 20 k$, 91 % à zéro, la colonne « 0 » restant toujours
  ouverte pour pouvoir se mettre à plat. La validation reste gardée (`refreshSend`, `fitBook`).
  Un book inchangé ne coûte rien et n'est jamais bloqué — pas d'impasse possible.
  La tuile « Vos gains » affiche `mgrCash()`, donc exactement ce qui reste à dépenser ; le
  score conservé pour le palmarès et les campagnes reste `mgrNet()`, qui en diffère du capital
  de départ (50 pb de l'encours initial).
- **Coûts de transaction** : `TCK=3` multiplie le tarif de base dans `tcost`. Un ordre préparé
  revient à ~5 pb du notionnel, ~13 à 38 pb de l'encours pour ouvrir un book complet. Suivre
  une dépêche coûte `tc.cost*1.6` (prime d'urgence) — l'ancien glissement forfaitaire de
  12,5 pb du notionnel a été supprimé, il représentait 90 % de la facture et ne se voyait
  nulle part. Un arbitrage d'exécution non restreint à des marchés nommés agit aussi sur
  `S.tcMultQ`, donc sur les ajustements du trimestre.
- **Effets d'événement** : la famille `cashM` (montants fixes en M$) **n'existe plus**. Tout
  effet de trésorerie est un `cash` proportionnel à l'encours. Les 49 anciennes valeurs,
  calibrées pour un fonds de 100 Md$, ponctionnaient 1,6 M$ par trimestre sur un fonds de
  100 M$ ; divisées par 20 et converties en pb, textes affichés réécrits avec elles.
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
- **Objectifs** : `QGOALS` (108), bonus = `goalBon(g)` = `g.b * GOALB * S.aum0` avec
  `GOALB=0.25`. Tirés à chaque trimestre dans `planQuarter`, soldés à la clôture,
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
- **Ruban de P&L en direct** : dès `S.phase==='events'`, `tapeBand()` remplace le bandeau
  d'informations dans `statusBar`. Chaque segment est un **pont brownien géométrique**
  (`bridgePts`) : bruit cumulé en log moins sa dérive terminale, puis exponentielle — texture
  de cours, extrémités clouées. La cible est `liveRet()`, qui est la formule de clôture `grQ`
  avec la fraction de trimestre écoulée `t` à la place de 1, collatéral compris : le ruban
  tombe donc exactement sur le chiffre du débriefing (46 clôtures sur 52 à moins de 0,5 pb ;
  les 6 autres sont les trimestres où le stop, l'appel de marge ou le portage s'appliquent
  **dans** la clôture, après le dernier événement — le ruban ne peut pas les connaître).
  Les points déjà tracés sont stockés dans `S.tape` et jamais recalculés. Le tracé dure
  **3 s** et les quatre écrans d'événement du trimestre (dépêche, desk, rivalité, incident)
  portent la classe `.evhold`, qui les révèle une fois le ruban tracé : on voit le marché
  bouger avant d'apprendre pourquoi. Les cartes de bilan, elles, s'affichent tout de suite —
  ce ne sont pas des événements. Le mi-parcours n'a plus de courbe : elle faisait doublon
  avec le ruban ; son texte dit à la place quelle part du gain de l'année vient des positions
  encore ouvertes.
  Densité : `TAPEM=48` points par segment, amplitude `tapeVol()` calée sur la volatilité
  cible du mandat — un pas horaire sur treize semaines, quelques centaines de points par
  trimestre. `tapeSvg(pts,from)` dessine **deux** polylignes : la portion déjà vue, posée
  d'emblée, et la portion nouvelle seule, animée en 3 s. `S.tape.from` marque la frontière.
  **Piège de CSS** : `animation` est une propriété raccourcie, pas cumulative. `.fade` et
  `.evhold` posées sur le même élément faisaient gagner la dernière règle de la feuille ;
  `.fade` se terminait en 0,3 s sans `fill-mode` et l'élément retombait sur le `opacity:0`
  de `.evhold` — le texte de chaque dépêche restait invisible pour toujours. Les deux classes
  sont exclusives ; ne jamais les recombiner.
  **Piège** : `mulberry32` écrit dans le `rngState` global. Tout décor aléatoire doit passer
  par `prng32`, qui est pur — sinon les flux nommés du lot 11 se décalent en silence.
- **Courbes de NAV** : `navChart(vals,opts)` dessine, `navBox(cap,vals,opts)` encadre avec
  légende, `idxSeries(extra)` fournit la série (produit cumulé de `S.rets`, base 100 — la
  performance nette que lit l'investisseur, pas l'encours, donc insensible aux flux).
  Utilisées à l'accueil (partie imaginaire, `heroNav()`), à mi-trimestre (avec le point
  latent), à la clôture et au rapport final. `resultCard` accepte `extra.top`.
- **Accueil** : `introTicker()`, courbe héros, `mktWall()` (les 25 marchés, 5 × 5, teintés par
  classe), `introRivals()` (les 4 concurrents avec `avatar()`).
- **Sauvegarde** : clé `lebook_save_v2`, `save(point,extra)` / `loadGame()`, table `RESUME`.
  `phaseExec` n'existe plus comme écran ; la table `RESUME` la redirige vers `screenExec`
  pour que les sauvegardes antérieures restent reprenables.

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
11. Les charges factorielles respectent **Σb² ≤ 0,92** (`normB` rescale au-delà et fait
    retomber une charge d'un cran sans prévenir). Viser 0,87 au plus : la dérive trimestrielle
    ajoute 0,035 de bruit par facteur. Crans affichés (`rowInfo`) : |b| < 0,15 → 0 ;
    < 0,32 → 1 ; < 0,55 → 2 ; ≥ 0,55 → 3. Une charge calée à 0,58 clignote entre 2 et 3.
12. Aucun effet d'événement ne doit être libellé en montant fixe. Le fonds fait 75 à 150 M$ ;
    tout montant en dur se retrouve à des dizaines de pour cent de l'encours.
13. Le gérant ne peut jamais être définitivement bloqué : la commission de gestion (50 pb)
    dépasse toujours le budget minimum (15 pb), et un book inchangé est toujours validable.

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

- **Lots 1 à 5** (méthode : `base.html` = fichier publié intact, `patches/NN-*.py` = un lot par
  fichier avec ancres assertées, `build.sh` rejoue tout dans l'ordre — le travail est
  reproductible depuis le fichier publié) :
  - *Lot 1* : charges factorielles ES, MXEF, NQ, TN, GBL, R, OAT, GC, BTC ; « silence radio »
    ramené à investisseurs 0 / comité 0. Trois demandes ne tenaient pas dans le budget de
    variance : NQ, MXEF et GBL ont vu une charge **non demandée** rognée.
  - *Lot 2* : économie du gérant (ci-dessus), bonus d'objectif ÷4.
  - *Lot 3* : coûts de transaction rééquilibrés (ci-dessus), enjeu de chaque option
    d'exécution chiffré en monnaie dans le bouton.
  - *Lot 4* : `cashM` → `cash` ÷20 ; exécution en une seule étape (détail replié, coût total
    toujours visible) ; annonce validée au clic ; pré-annonces « undefined » (la file
    contenait des dépêches de rivalité sans champ `t`) ; pastille « ✓ vérifiée » au lieu d'un
    préfixe qui débordait ; nowcast durable (`tcvPerm`, payé par le gérant via `mgrM`) ;
    « ancien du desk » relibellé.
  - *Lot 7* : `goalchk.js` reconstruit, et ce qu'il a trouvé (ci-dessous).
  - *Lot 6* : réglage du style flux (ci-dessous).
  - *Lot 5* : accueil refondu, courbes de NAV partout. Bug corrigé : le tracé final partait de
    `S.navs[0]=100` contre des encours en Md$ — une falaise verticale invisible depuis
    longtemps.

- **Lots 32 à 36** (ménage, virgules, noms, ruban) :
  - **Lot 32 — ménage des anciennes morts.** Depuis le lot 25 la seule fin est `S.over='nav'`
    (encours sous 40 % du départ). Les trois verdicts inatteignables ('dd', 'lp', 'rc') sont
    supprimés ; `if(S.over)` couvre les vieilles sauvegardes. La case « Comité » de la barre
    d'état était rendue avec `display:none` : supprimée, sa pop-up fondue dans celle de la
    Confiance (les deux composantes, la formule, les seuils 24 / 20 / 13 / 40 %). La barre de
    la jauge Confiance affichait `S.lp` au lieu de `conf()`. Six textes périmés réécrits
    (règles, présentation, pop-up Capital, les deux profils : le flux annonçait 16 % alors que
    son seuil est 13 % depuis le lot 6).
  - **Lot 33 — virgules.** L'invariant 8 n'était pas tenu : 74 gabarits `${x.toFixed(n)}`,
    dont 57 dans du texte (passés par `dec`), 17 dans des attributs SVG (laissés : une virgule
    casse le dessin), plus 8 concaténations. Le patch refuse une expression sans parenthèses
    qui changerait de sens dans `dec(...)`.
  - **Lot 34 — noms ×3.** `NAME1` passe de 40 à 120 (3 600 combinaisons). Les 80 nouveaux sont
    écrits par thème d'écusson et `NAMECREST` relie 108 noms à leur écusson : « Proposez-m'en
    un » propose l'écusson assorti tant que le joueur n'a pas cliqué un écusson (`crestPicked`).
    Un nom long réduit son corps (`fitN`) au lieu de déborder de la saisie.
  - **Lot 35 — ruban vivant et théâtral.** `rivalTapes` appelait `rivRet(j,t)`, **fonction
    inexistante** : ReferenceError avalée par un `try/catch` muet, donc les concurrents restaient
    plats pendant tout le trimestre. `rivRet(j,t,q)` est écrit, **pur** (hash32/prng32) : même
    forme que `rivalReturns` sans le terme idiosyncratique, que la clôture révèle par un dernier
    pas de 18 points commun au joueur et aux concurrents. `S.tape.ts` retient l'instant de chaque
    segment et `S.tape.q0` le début du trimestre, ce qui aligne les courbes. Pastilles des
    concurrents hors découpage, qui suivent leur courbe ; pastille du joueur cerclée de blanc
    (depuis le lot 34 il peut porter le même écusson qu'un concurrent). `opt.draw` : 3 s pour
    les dépêches (aligné sur `.evhold`), 5 s au mi-parcours et à la clôture, où le grand ruban
    rejoue le trimestre avec un compteur calé sur la tête du tracé (`data-vals`, `theatre()`),
    le résultat révélé ensuite (`.thold`), et un toucher qui saute l'animation.
  - **Lot 36 — bruit du ruban.** `tapeVol` calait l'amplitude sur la volatilité *annuelle* quelle
    que soit la durée du segment : un pont s'écartait de ±14 % au milieu d'un trimestre à +1 %.
    Désormais `tapeVol(m,dt,v)` = (v/2)·√(dt/m), `dt` mesuré sur l'avancement réel de la file de
    dépêches, les concurrents avec leur propre volatilité.

  Vérifications : régression 18 parties identiques au bit près (mêmes NAV finales qu'avant le
  lot 32 : aucun de ces lots ne touche un tirage de `rng`), `cover2` 662 choix sans anomalie,
  `cover3` 2 700 plans, `goalchk` 108 prédicats, reprise à froid, `uichk2` adapté.

- **Lot 37 — l'exécution pèse.** Mesuré d'abord (`tools/execprobe.js`, 18 parties, 112
  trimestres) : facture d'ordres médiane **15,6 pb de l'encours** (p90 30), soit 27 % du revenu
  trimestriel du gérant (p90 99 %) — mais **entièrement à sa charge**, donc sans effet sur la
  performance du fonds ni sur les jauges ; et sur 435 choix d'exécution, 7 seulement touchaient
  les investisseurs. Multiplier le multiplicateur de coûts aurait menti (les textes des boutons
  sont écrits à la main : invariant 9), donc on ajoute un canal : **la facture reste au gérant,
  la dégradation du prix moyen reste dans le fonds.**
  - `execSlipAmt(excess)` : au-delà du tarif standard, le fonds perd `EXECSLIP`=12 fois le
    surcoût, plafonné à 1,2 % de l'encours par choix ; en dessous il gagne 0,35 fois autant.
    L'asymétrie est le garde-fou : symétrique, « exécuter au rabais » devenait de l'argent
    gratuit (~0,4 % par trimestre sans risque).
  - `execGz(m,leak)` : le comité sanctionne l'écart au tarif standard **dans les deux sens**
    (3,5 points par unité, borné à −4) ; une fuite coûte 2 aux investisseurs, 1 au comité, et
    deux lignes de clôture le rappellent si les positions ont circulé (`S.leakQ`).
  - Les ajustements passés au tarif hérité du trimestre (`S.tcMultQ`, fuite ×1,45) glissent de
    la même façon : c'est là que les options « coûts −35 % avec fuite » se paient vraiment.
  - `stake()` annonce avant le clic l'effet sur les ordres, sur le fonds et sur les jauges, par
    les mêmes fonctions que l'application. Le bilan d'exécution passe en tableau visible au lieu
    d'être replié dans « Le détail ». `sd1` n'affiche plus « −0 ».
  - Hors périmètre volontaire : les ajustements pris **dans une dépêche** (`resolveEvent`), dont
    les montants sont chiffrés par `evPlans` — y toucher demanderait de refaire le chiffrage des
    deux options, et l'invariant 9 ne pardonne pas l'à-peu-près.
  - Effet mesuré (30 parties appariées, 3 styles) : **49 % des trimestres** portent un effet de
    prix moyen (0 % avant), |effet| médian 0,4 pb, p90 26 pb, décile bas −20 pb, extrême
    −110 pb. Score moyen 18,9 → 18,4 M$ et survie 19/30 → 18/30 : dans le bruit (erreur type
    ≈ 5 M$), donc l'équilibre général n'est pas déplacé — seule la variance des choix augmente.

- **Lot 38 — l'impact de marché payé par le fonds** (`patches/99za-impact.py`, mesure
  `tools/execmeas.js`). Après le lot 37, une anecdote d'exécution pesait encore vingt-cinq fois
  moins qu'une anecdote de desk (fonds : moyenne −0,7 pb contre −19,6). Ajout du canal qui
  manque, l'impact de marché : `execImpactAmt(bill,m,leak)` = `IMPK` (2,4) × facture standard,
  corrigé par `m^-1,2` (payer le bloc protège le prix, négocier un rabais le dégrade — ce qui
  **inverse le sens du lot 37**, qui punissait le fonds dans les deux sens), +60 % en cas de
  fuite, plafond 1,5 % de l'encours. Payé **à chaque trimestre**, anecdote ou pas (~30 pb). En
  contrepartie la facture de courtage passe aux trois quarts (`EXECM` 1,35 / 0,75 / 0,50) :
  ce que le gérant payait en commissions, le fonds le paie en prix moyen. À la clôture :
  investisseurs −2 si l'impact du trimestre dépasse 35 pb, comité −2 si l'exécution s'est
  écartée du standard de plus de 35 %.
- **Lot 39 — budget à onze crans** (`patches/99zb-budget11.py`). Minimum inchangé, maximum
  doublé : salle de marché 2 → 100 pb, contrôle 4 → 48, recherche 4 → 128. Les anciens niveaux
  sont les crans **0 / 4 / 8**, aux mêmes prix et avec les mêmes effets : la calibration
  antérieure reste valable. Chaque bénéfice devient un tableau de onze valeurs monotone qui
  passe par les anciennes (`EXECM`, `RETM`, `TCVQ`, `RISKM`, `RISKS`, `BANDB`, `RISKRC`, `RESN`,
  `RESREL`, `RESR`, `RESPH`, `STARP`) ; les deux crans au-delà prolongent nettement la pente
  (coûts ×0,30, incidents ×0,04, bande ±60 %, comité +4 par clôture, 16 sources, lecture ±2 pts,
  recrue du trimestre 60 %). `BUDMAX`=8 : seuil « renforcé » pour objectifs et hauts faits.
  Les libellés d'effets sont **calculés** (`budEf`), plus recopiés. Écran : chaque bouton ne
  porte que son coût (pb en gros, monnaie dessous), le nom et le rang du cran choisi s'affichent
  au-dessus de la rangée, ses effets dessous ; deux rangées de six et cinq (55 px à 380 px).
  Sauvegardes : `loadGame` remonte les anciens crans 0/1/2 sur 0/4/8 (`tools/budmig.js`).
  - Vérifié : les bénéfices s'appliquent bien (graine 5, fondamental : sources 10 → 13 → 20,
    bande 18 → 25 → 60 %, coûts d'exécution 425 → 204 → 76 pb cumulés, incidents 2 → 1 → 0
    aux crans 0 / 4 / 10).
  - **Mesure (bot, 30 parties par réglage, trois styles)** : tout au cran 0 = 16,3 ± 3,2 M$
    (survie 15/30) ; cran 4 = **21,7 ± 3,5** (19) ; cran 8 = 15,0 ± 2,7 (20) ; cran 10 =
    **6,1 ± 1,6** (19). L'optimum reste au milieu, ce qui est sain, mais les deux crans du haut
    ne peuvent pas se rentabiliser : tout au maximum coûte 281 pb par trimestre, 2,8 M$ sur
    100 M$, quand la commission de gestion trimestrielle en rapporte 0,5 et le revenu total du
    gérant ~2. Aucune amélioration de bénéfice ne comble cet écart tant que le budget est payé
    par le gérant seul — voir « À trancher ».

- **Lot 40 — relecture des textes** (`patches/99zc-textes.py`). Chaque chiffre des fiches vérifié
  contre la valeur du code : capture du quant 50 % (pas 60), pré-annonces du fondamental +13 pts
  (pas 10), intuition du flux juste ~4 fois sur 5 (pas 13 sur 14), cible du desk de flux 135 %
  (pas 120), incidents du flux +25 % (jamais annoncés), mandat agressif « moitié plus » (pas
  « trois fois »), ±5 unités pour tous les mandats, fret ouvert dès le full-floor, bac à sable
  moins nerveux. Tutoriel, info-bulle d'exécution, pop-ups des gains et des coûts, note du
  débriefing : remis d'accord avec les lots 25 (une seule fin) et 38 (impact payé par le fonds).
  Objectifs de budget : « au cran Renforcé ou au-delà ». Durée : un, deux ou trois ans. Pouvoirs
  de lecture des dépêches ajoutés aux trois fiches. Aucun effet sur le jeu (NAV identiques).

- **Lot 41 — tailles réelles** (`99zd-tailles.py`) : 100 M$ / 1 Md$ / 10 Md$, `capX` 1 (la loi en
  racine carrée du notionnel fait le coût). `DEPTH` (profondeur des carnets, Md$) : impact
  × √(1 + notionnel/profondeur). Tous les marchés de l'univers sont dans `INSTR` ; ceux de rang
  > `OPENRK` sont fermés (`kCap`=0, `clampK`, pools filtrés par `applyPools`). Ouverture d'un
  rang à 1,4× puis 2× l'encours initial (`unlockNav`), à la clôture, avec carte dorée ; `S.openRk`
  sauvegardé. Le desk du modèle évite les carnets trop étroits pour sa taille.
- **Lot 42 — indice du gérant** (`99ze-score.py`) : chaque concurrent tient un compte de gérant
  (`rivalMgrQuarter` : gestion, performance, budget standard, facture type ; champs `mAum`,
  `mHwm`, `mgr`). `mgrIndex()` = 100 + 100 × (P − médian) / max(|médian|, 1 % d'encours par an).
  Rapport final, palmarès (classé sur l'indice), partage ; hauts faits de gains en multiples de
  l'encours initial.
- **Lots 43-44 — cartes dorées et bonus** (`99zf-bonus.py`) : `goldPop` / `goldLater` / `goldFlush`,
  visuels SVG `GV`. Existants mis en scène (hauts faits, objectif tenu, recrue, premier plus
  haut historique) ; nouveaux : ouverture de marchés, blocs, prime brokerage, dark pools, main
  chaude, FT, fonds de l'année, économiste de la Fed, trader star, Jackson Hole, fonds
  souverain, carte blanche, trade du siècle, cygne noir. Tirages purs (`bonusDraw`), jamais au
  milieu d'une dépêche.
- **Lot 45 — sept crans** (`99zg-budget7.py`) : crans 0/3/5 = anciens niveaux, max 1,5× l'ancien ;
  une ligne de sept boutons ; migration 11 → 7 et 3 → 7. `BUDMAX`=5. Bot : budget par défaut [3,3,3].
- **Lot 46 — trois concurrents stylés** (`99zh-rivaux.py`) : Médaillon (quant), Pont-Levis
  (fondamental), Citadelle (flux) ; `rivalE` partagé par `rivalReturns` et `rivRet`. Rendements
  médians mesurés 21 / 20 / 17 % par an ; indice médian du bot ≈ 100 (full-floor) à 150.
  Millénaire retiré. Mastodonte : adresse des concurrents +0,03 ; investisseurs : écart à la
  médiane ×85 (au lieu de 115).

- **Lot 47 — fin plus douce, abandon, minuteurs en pause** (`99zi-fin.py`) : fin de partie sous
  5 % de l'encours initial (`NAVEND`, −95 %) ; bouton « Abandonner » sous « Trimestre suivant »
  (confirmation, verdict « Vous avez rendu les clés », `S.over='quit'`) ; le minuteur des dépêches
  ne décompte pas tant qu'une fenêtre (`#modal` affichée) ou une carte dorée est ouverte.
  **Spirale des rachats corrigée** : le repli qui déclenchait les rachats était `S.maxdd`, maximum
  sur la partie (rachats à chaque clôture une fois franchi) et calculé sur l'encours (les rachats
  creusaient le repli qui les déclenchait). Désormais repli de performance (`S.idx` contre
  `S.hwmIdx`), déclenché seulement par un nouveau plus bas (+2 pts, `S.ddHit`), réarmé à la moitié
  du seuil. Survie du bot (15 parties par taille) : boutique 14, full-floor 11, mastodonte 10,
  contre 12 / 7 / 5 avant cette correction. Concurrents : 25 / 28 / 22 % par an ; indice médian
  du bot 242 / 87 / 142 (boutique : adresse des concurrents −0,01 au lieu de −0,05).

- **Lot 48 — lissage et difficulté par taille** (`99zj-lissage.py`) : budgets en courbe régulière
  bp(i) = min + (max − min)·(i/6)^p, p choisi pour garder le standard au cran 3 (salle 2·3·9·18·32·51·75,
  contrôle 4·5·8·12·18·26·36, recherche 4·5·9·18·35·60·96) ; effets interpolés au nouveau prix sur la
  courbe prix → effet des onze crans (lot 39). Page « Le trimestre se déroule » supprimée
  (`phaseLive` entre directement dans les dépêches). Cartes dorées plus rares (trade du siècle 15 %,
  FT +10 pts, main chaude 5 trimestres, fonds de l'année >10 %, souverain ×1,6 et confiance 78,
  carte blanche 4 trimestres, croissance ×1,3 / 1,6 / 2,2). Adresse des concurrents par taille :
  +0,05 / +0,05 / +0,09 (difficulté croissante avec la taille).
  Mesure (bot, 21 parties par taille) : indice médian du gérant 215 / 140 / 94, survie 20 / 16 / 14
  sur 21 ; concurrents 29 / 25 / 23 % par an (quant / fondamental / flux) ; 14 à 19 cartes dorées
  par partie, dont une majorité d'objectifs tenus et de hauts faits.

- **Lot 49 — refonte des choix de départ** (`99zk-difficulte.py`). Plus de choix de taille, d'univers
  ni de risque : 100 M$, vol cible 20 %, 2 % de gestion pour tous. `SIZES` porte trois niveaux de
  difficulté (ids small / mid / mega conservés) : adresse des concurrents, vigilance du comité,
  voracité et nervosité des investisseurs, commission de performance 15 / 20 / 25 % (`perfFee`).
  Marchés : trois par classe au départ, 4e rang à 1,4× l'encours, 5e au double ; exotiques
  (`S.exoOpen`) ouverts la première fois que le joueur finit premier d'un trimestre (carte or).
  Score : gain net cumulé du gérant (l'indice reste calculé, plus affiché). Flux clients par
  concurrent : 0,5 × sensibilité (quant 0,6, fondamental 1,0, flux 1,6) × écart de performance,
  ±6 % par concurrent, sorties × `flowMult`, confiance < 40 en plus ; détail dans le débriefing
  (`S.qFlowBy`). Emblèmes des concurrents (pont-levis, médaillon, trident) ajoutés à `CRESTS`
  après les douze du joueur (`NPC`), `RIVCREST=[12,13,14,13]`. Cartes en trois paliers (bronze,
  argent, or) : `tier` sur chaque carte, couleurs et visuels recolorés par palier.
  Migration : `S.exoOpen` absent → ouvert si l'univers était « monde entier » ; `OPENRK` déduit de
  l'encours initial pour les anciens full-floor et mastodontes.
  Mesure (bot, 21 parties par niveau) : gains médians 15,0 / 16,4 / 15,8 M$, survie 20 / 16 / 16,
  flux nets cumulés +18 % / −28 % / −60 % de l'encours initial, exotiques ouverts dans 21 / 18 / 16
  parties, 18 à 20 cartes par partie ; concurrents 27 / 32 / 21 % par an.

- **Lot 50** (`99zl-book.py`) : difficile à 30 % ; drapeaux / pictogrammes (`MFLAG`) et symboles de
  classe (`CSYM`) dans le book ; badge « 🔒 140 M$ » ou « 🔒 1er d'un trimestre » sur les marchés
  fermés. **Ruban = tuile Perf.** : `qElapsed()` vaut 0 avant le lancement du trimestre (la tuile
  affichait le latent d'un trimestre entier sur les écrans d'exécution et d'annonce), et le ruban
  couvre désormais tout le mandat (base 100 au lancement, comme la tuile). Sonde
  `tools/tapeprobe.js` : 0 écart sur 1 265 rendus (174 avant). Grand ruban en 3 s. Comité : risque
  affiché > 2 × cible → −10 − 40 × (ratio − 2), borné à −40, investisseurs −4, avertissement dans le
  book. Correctif : la « médiane » des concurrents prenait le meilleur des trois.
  Mesure (21 parties par niveau) : gains médians 15,0 / 14,3 / 18,6 M$, survie 20 / 17 / 15, flux
  nets cumulés +12 % / −44 % / −75 %.

- **Lot 51 — rendement attendu ± 2σ** (`99zm-attendu.py`) : `expRet(i)` = σ·(Σ b·f̂ + 0,12 T̂ + 0,10 Ĉ + 0,08 V̂)
  + dérive, avec les SEULES informations du joueur (`S.factEst`, `S.tcvEst`) ; incertitude
  σ·√(Σ b²·`EXPVF` + propre² + bruit des lectures). `expBook(k)` au niveau du book (bloc `#xbook`).
  Dosage : facile = chiffre + intervalle + barre, moyen = chiffre + barre, difficile = sens et
  étoiles de conviction. Calibration `tools/expchk.js` (option `pre` ajoutée à `bot.js`) : écart
  type des z 0,97, 95,1 % des mouvements dans ± 2σ (marchés), book 0,95 / 97,6 %.
- **Lot 52 — signaux par style** (`99zn-styles.py`) : `STYLESIG` (quant portage, flux tendance,
  discrétionnaire valeur) lu avec un bruit ×0,3, les autres ×1,3 ; quant : classement du portage
  au-dessus du book ; flux : tendance du trimestre à mi-parcours (`fluxMid`) ; discrétionnaire :
  deux catalyseurs par trimestre (`S.cat`, tirage pur) où le terme de valeur compte double dans
  `drawReturns` pour tous — seul lui le sait (badge ⚡, pris en compte dans son `expRet`).
  Le signal du style s'affiche en premier et en gras.
- **Lot 53 — cartons du comité** (`99zo-cartons.py`) : `conf()` = `S.lp`. Plus de rachat « comité »
  ni de mandat réduit sous 13. Cartons à la clôture (`S.cards`, `S.qCard`) : rouge pour risque
  > 2× cible, perte > 2,2 σ, appel de marge, deuxième jaune ; jaune pour book validé (`S.kVal`)
  au-dessus de la bande, > 75 % du risque sur un facteur, book vide, patience du comité en baisse
  de 25 points dans le trimestre. Rouge : mandat ±3 au trimestre suivant (`S.redNext`/`S.redOn`),
  5 % d'encours, confiance −6. Quatre trimestres propres retirent un jaune. `gz()` affiche
  « confiance ±x » et « ⚖️ ±y ». Desk du flux ramené à 120 % de la cible (135 % hors bande).
  Mesure (moyen, 15 parties) : 1,4 jaune et 0,9 rouge par partie.

- **Lot 54 — lecture du book** (`99zp-lecture.py`) : attendu du book dans la tuile « Risque » de la
  barre d'état (visible sur tous les écrans du trimestre, dosé par difficulté) ; par marché, la barre
  disparaît au profit de « unité » (gain attendu pour le fonds d'une unité, ± 2σ en facile) et
  « risque » (contribution d'Euler au risque affiché, en points, somme = chiffre de la barre ; sans
  position, l'effet d'une unité ajoutée : `riskPts`, `riskAdd`). Signaux toujours dans l'ordre
  Tendance · Portage · Valeur, celui du style en gras léger. Le détail d'un marché agrège facteurs
  (exposition × lecture → effet), signaux, dérive, attendu, intervalle, gain par unité, risque
  (`expParts`).
- **Lot 55 — nettoyage** (`99zq-nettoyage.py`) : desk à trois sources visibles (les autres repliées),
  lecture consolidée repliée, aide des sources réécrite ; book sans la ligne des codes d'exposition,
  marchés fermés sur une ligne ; débriefing : flux clients en tête, « Du brut au net » replié,
  « Ce qu'ils en disent » = confiance et carton. La tuile « Vos gains » affiche le score (elle
  montrait la trésorerie, 500 k$ de plus que « Cumul depuis le début »). Hauteur à 380 px : book
  6 180 → 3 258 px, débriefing 2 449 → 2 118 px.

- **Lot 56 — nettoyage, deuxième passe** (`99zr-nettoyage2.py`) : expositions factorielles revenues
  dans le book (ligne d'info : expositions à gauche, « unité » et « risque » à droite, ordre en
  dessous seulement s'il existe). Budget : intro d'une ligne, description de chaque poste dans le
  repli « À quoi sert ce budget · les sept crans ». Annonce : attendu du book, promesse, « confiance
  +x · −y », et en facile / moyen la chance de tenir d'après l'attendu (Φ logistique). Exécution :
  deux lignes (ordres, impact), le reste dans le détail ; enjeux des options en ligne (ils étaient
  en `<b>`, affichés en bloc). Dépêches : « Effets » masqué quand rien ne bouge, colonnes Confiance /
  ⚖️, minuteur compact, le résultat ne répète plus son titre. Hauteurs à 380 px : budget 1 667 →
  1 231, annonce 1 305 → 1 062, exécution 1 394 → 1 086, résultat de dépêche 822 → 801.

- **Lot 58** (`99zt-lot58.py`) — demandes d'Antoine :
  - **NAV** : tuile d'encours = `navNow()` seule (latent des positions et collatéral couru compris,
    même formule que `liveRet`), plus de flèche ni d'ancienne valeur. `chk58.js` compare la tuile à
    `moneyB(navNow())` à chaque écran : 0 écart sur ~3 000 rendus.
  - **Comité sans jauge** : `cf(lp,rc)` = lp + rc/2, arrondi à l'entier, borné ±15. `gauge()` n'applique
    plus que `cf` à la confiance (`S.rc` continue de courir en cachette pour le jaune « griefs
    accumulés ») et renvoie `{lp:cf, rc:brut}` ; `evPlans` porte dans `gz[s].lp` la somme exacte des
    `cf` appel par appel (invariant 9, sonde `play.js` : 0 écart). **Les valeurs du journal (`evLog`,
    `gLog`, `S.evImmG`, `lastG`) sont déjà repliées : les afficher par `gz(x,0)`, jamais `gz(lp,rc)`.**
    Les 277 mentions « comité ±N / investisseurs ±N » des textes sont lues en confiance à l'affichage
    par `fxTxt(s,e)` (valeur recalculée sur `e`, groupe conditionnel `riskLp/riskRc` à part,
    « confiance inchangée » si les deux se compensent). Colonne ⚖️ des dépêches, lignes comité des
    résultats, de l'incident et du débriefing supprimées.
  - **Carton** : tuile `cardTile()` (vide / jaune / rouge), clic → pop-up `card`. Un rouge tire
    `redDraw()` parmi `REDC` (9 : plafond ±2, risque ≤ 70 % de la cible, stop ex post −4 %, 3 marchés
    fermés, classe fermée, collatéral renforcé, 4 lignes, contrôle au cran 5, gel des renforcements),
    jamais deux fois de suite la même ; `S.redNext` (objet) → `S.redC`/`S.redOn` dans `planQuarter`.
    Garde : `redBlock()` bloque « Passer les ordres », `fitBook()` ramène le book dans la contrainte
    puis au payable ; « Suivre » grisé sous `risk`/`noadd`. Marchés fermés : `S.shut[sym]===S.q`
    dans `mktOpen`. `chk58.js --red` force un rouge à chaque trimestre et vérifie chaque contrainte au
    moment de la validation : 12 parties de 12 trimestres, les 9 couvertes, 0 violation.
  - **Plafond de position** : `S.capK` 3 au départ ; « Accès aux blocs » (encours ×1,2) → ±4,
    « Accès aux blocs · premier cercle » (×1,5) → ±5. `S.maxk` recalculé à chaque `planQuarter`.
    Sauvegardes antérieures : `capK` absent → 5.
  - **Événements extrêmes** : 10 dépêches `x:1` dans `MACROEV`, hors tirage ordinaire, jamais
    pré-annoncées ; `XPROB`=0,15 par trimestre à partir de T2 (tirage pur `hash32('xev'+q)`). `shut`
    ferme des marchés : aucun ordre dans la dépêche, fermés au fonds le trimestre suivant.
  - **Collatéral** : bloc sur l'écran du budget, `COLL` (Trésor / monétaire +0,3 % 5 % de −2 % /
    repo +0,7 % 10 % de −4 % / titrisations +1,4 % 20 % de −6 %, par trimestre). `colYield()` dans la
    clôture et le ruban ; perte tirée à la clôture (`hash32('coll'+q)`), ligne au débriefing.
  - **Budget** : crans hors trésorerie grisés (ils étaient `disabled` sans style) ; un budget reconduit
    qui dépasse la caisse redescend à l'ouverture. « Suivre » grisé si la trésorerie ne suit pas.
  - **Risque marginal** par marché : `riskMarg` = (R(k+1) − R(k−1))/2 en points (book vide : effet
    d'une unité), à la place de la contribution d'Euler.
  - Outils : `play.js` et `bot.js` ignorent les boutons désactivés, `play.js` choisit un placement de
    collatéral au hasard, `bot.js` lit « confiance ±N ». Nouveau `tools/chk58.js`.
  - Mesures : régression 18 parties, `cover2` 662 choix, `cover3` 2 952 plans, reprise à froid :
    0 erreur, 0 écart. Bot, 14 graines × 3 styles, avant → après : score moyen quant 23,2 → 20,9,
    fondamental 23,9 → 14,8, flux 33,3 → 23,4 M$ ; survie 14 / 13 / 12 → 14 / 12 / 11. La baisse
    vient surtout du plafond ±3 et des extrêmes ; le bot laisse le collatéral au Trésor.

- **Lot 59** (`99zu-lot59.py`) :
  - **Double facturation supprimée** : suivre une dépêche ou une rivalité retirait le coût des ordres
    de l'encours (`S.nav-=cost`) ET l'ajoutait à la facture du gérant. Le fonds ne paie plus ; les
    montants des boutons de dépêche sont hors coûts (même calcul des deux côtés, invariant 9).
  - **Collatéral** : rendement du trimestre affiché (taux / 4 + surcroît) ; `colY(o)` fait varier le
    surcroît de ±35 % par trimestre (tirage pur `hash32('coly'+id+q)`). Espérances moyennes mesurées :
    0 / +0,20 / +0,40 / +0,59 % par trimestre, ~0,5 inversion d'ordre par trimestre.
  - **Difficulté** : commissions 15 / 20 / 25 % (difficile : 30 → 25 %). Difficile : flux clients ×2,1
    dans les deux sens (`flowMult`, nouveau `flowIn`), concurrents les plus adroits (`rivSkill` 0,12).
  - **Fondamental** : deux sources vérifiées, +6 sources, trois catalyseurs (`CATM`=3, pour tous les
    marchés, seul le fondamental les voit), signal de valeur 0,10 (`SIGW`, `drawReturns`), capture 0,60,
    `modelScale` 1,10.
  - **Bot** : `--policy dumb` (book et choix au hasard) ; l'ancien « naive » reprend le book du modèle
    et gagne presque autant que « smart ». `bot.js` exploite les catalyseurs du fondamental.
  - Mesures (graines appariées, M$, moyenne / écart-type) : styles, bot intelligent, trois difficultés :
    quant 15,9 / 12,6, fondamental 19,9 / 15,0, flux 20,1 / 17,0. Bot intelligent : moyen 19,1 / 16,2
    (p10–p90 3–37), difficile 17,8 / 16,3 (p10–p90 1–46), facile 17,6 / 12,6. Bot nul : 5,6 / 6,6 / 6,7.
    Erreur type ≈ 3 M$ : la forme est là, les marges ne sont pas démontrées.
  - Contrôles : régression 18 parties, `cover3` 2 952 plans, `chk58 --red` 12 trimestres, reprise à
    froid : 0 erreur, 0 écart.

- **Lot 60** (`99zv-lot60.py`) :
  - **Lignes de marché** identiques aux trois niveaux (fin de l'« affichage dosé ») : grille ordre
    (achat / vente / aucun, en unités), attendu d'une unité ± 2σ, risque +1 et −1 unité (points de
    risque total), coût de fourchette, impact de marché (`tcost` renvoie `spr` et `imp`).
  - **Risque avec bruit d'estimation** : `covE()` = facteurs × `EXPVF` (1,15) + idiosyncrasique +
    bruit des signaux T/C/V (`SIGW²·(sigNoise²+0,1)`, comme `expRet`), en cache. `pvol`,
    `riskContrib`, `volStress` la lisent. `COV` reste le modèle générateur.
  - **Cases grisées** : `updateRow` revoit toutes les cases à chaque clic (seule la ligne touchée
    l'était). `chk58.js` compte les cases actives non payables : 0.
  - **Collatéral** : espérance du trimestre versée au fonds à la validation du budget (`S.qColM`,
    base `S.colBaseNav`), écart versé à la clôture ; `grQ`, `collM`, `liveRet`, `navNow` en tiennent compte.
  - **Équilibrage** : facile `lpNeg` 0,60, `flowIn` 0,60 ; difficile `flowMult` 1,60, `flowIn` 2,60 ;
    fondamental +5 sources ; flux `ddMax` 0,16. Bot intelligent (8 graines × 3 styles) : facile
    16,2 / 12,4, moyen 19,2 / 15,5, difficile 19,9 / 19,3 (progression en moyenne et en variance).
    Bot nul (6 × 3) : 5,8 / 5,7 / 6,6 — pas de progression négative mesurable. Styles, bot intelligent :
    quant 18,7 / 17,5, fondamental 18,1 / 14,6, flux 18,5 / 16,0 — à plat. Erreur type ≈ 3 M$ par
    cellule : il faut ~30 graines par combinaison pour trancher.

- **Lot 61** (`99zw-lot61.py`) : collatéral de nouveau versé en entier à la clôture (acquis au fonds).
  `profitBook(k)` = collatéral espéré + Σ w·attendu − impact des ordres en cours (`tcost().imp`) −
  ½σ²/4 (drain de volatilité, σ = risque affiché bruit compris) ; affiché « profit » dans la tuile
  Risque (aussi book vide : c'est alors le collatéral seul) et, par marché, « Profit +1 » =
  profitBook(k+1) − profitBook(k), deux décimales. Grille : ordre | risque −1 | profit +1 | risque +1 |
  coût | impact. Facteurs : plus de cadre ni de soulignement. Tuile dorée = **Trésorerie**
  (`mgrCash`, capital de départ compris), les gains restent dans sa pop-up : c'est la trésorerie qui
  borne les cases, et les « gains » négatifs du premier trimestre faisaient croire à un défaut de
  grisage (`chk58 --tight` : 0 case fautive). Budget : « reste pour les ordres » et mise en garde.

- **Lot 62** (`99zx-lot62.py`) : tuile Risque = nuage `riskMap(sp)` (choix B d'Antoine) : risque
  annualisé en abscisse, profit du trimestre en ordonnée, bande du mandat et cible, zéro de profit,
  concurrents (`rivPt` : espérance fermée de `rivalE`, même convention que `profitBook`), book de début
  de trimestre en fantôme relié au book courant (doré, rouge au-dessus de la bande). En-tête : risque %
  et profit % (deux décimales).

- **Lot 63** (`99zy-lot63.py`) : plus de capital de départ (`mgrCash()` = `mgrNet()`, trésorerie =
  gains nets). Choix du collatéral → `refreshStatus()` (profit du panneau à jour). Lignes de marché :
  indicateurs T/C/V au-dessus, expositions en toutes lettres, « Ordre … coût », puis « +1 profit / risque »
  et « −1 profit / risque » (risque en %) ; impact retiré de l'affichage (il est dans le profit).
  Nuage : axes en bas / à gauche, valeurs du joueur en blanc au bord des axes, plus de point initial,
  zoom sur la bande, les concurrents et le joueur. Ruban (`tapeSvg`) : échelle limitée à l'étendue des
  quatre fonds, trait du joueur de sa couleur de blason (`myCol`, jamais celle d'un concurrent).
  Carton rouge : pop-up rouge (`.redbox`) à la clôture. Dépêches : confiance avant la décision, confiance
  finale par issue dans la colonne Confiance, « 62 → 58 » au résultat.

- **Lot 64** (`99zz-lot64.py`) : minuteur des dépêches selon la difficulté (facile 45–60 s, moyen
  25–35 s, difficile 15–25 s). Sources : mode d'emploi, lecture consolidée et matrice dans un seul volet
  replié. Budget : le texte trésorerie / ordres passe dans un 2ᵉ écran de tutoriel (4 écrans : jauges,
  budget, sources, facteurs). Tuile Trésorerie en M$ à une décimale (`treso`). `bridgePts` : bruit au
  moins proportionnel à l'ampleur du pas (plus de rampes droites). Nuage : point du joueur à sa couleur
  (`myCol`), concurrents à la leur (`rivCol`), sans libellés d'axes, profit à une décimale ; clic →
  grand nuage (noms, valeurs, bande) en tête de la pop-up Risque (`window.__pre` lu par `openModal`).
  Carton rouge « marchés fermés » / « classe interdite » : lignes à contribution positive au risque du
  book de fin de trimestre, puis taille de position ; le hasard seulement à book vide.

- **Lot 65** (`99zza-lot65.py`) : panneau du haut en disposition A (choix d'Antoine) : `.sgrid` = colonne
  gauche (confiance · carton · trésorerie, puis quatre facteurs compacts sans barre, `.fcomp`) et nuage
  risque/profit à droite sur deux rangées (viewBox 150 × 118). Blason dans la tuile d'encours
  (`.crestmini`). Point du joueur doré par défaut (`myCol` : or, puis couleur du blason, puis ivoire).

- **Lot 66** (`99zzb-lot66.py`) — demandes d'Antoine :
  - **Panneau du haut** : encours + performance (et repli) dans une seule tuile `.aum` ; 2ᵉ ligne Trésorerie ·
    Confiance · Carton ; nuage sur toute la hauteur de la colonne de droite (`.rmt` en position relative, `.rmap`
    absolu : le bas suit celui des facteurs). La pop-up « cap » reprend la performance par trimestre.
  - **Plus de mandat de volatilité.** `S.tgt` (20 %) ne sert plus que de référence au modèle (`recoBook`) et au bruit
    du ruban. `riskRc` ne note plus que le book vide ; `previewGauge`, clôture, drapeaux du book, pop-ups, textes,
    presse et débriefing ne parlent plus de cible ni de bande. `bandNow()` n'a plus d'effet visible.
  - **Accidents de levier** : `TAIL={x0:0.25,w:0.35,p:0.50}`, `tailP(sp)` = 0 sous 25 % de risque, 50 % à 60 %, ×`TAILM`
    (budget contrôle, 1,48 → 0,30). `tailL(sp)` perte de référence (plafond 0,62), L = gravité × tailL ≤ 0,40.
    `TAILEV` (12). Tirage pur `hash32('tail'+q)` en fin de file (`stepEvents`, `S.tailEv`/`S.tailDone`, remis à zéro
    dans `planQuarter`) ; `screenTail` : tenir (½ : 0,3 L, ½ : 1,5 L), couper la moitié du book (0,5 L + impact ×5,
    ≤ 8 %), couvrir (0,30 L fonds + 0,20 L trésorerie, grisé hors trésorerie). Perte dans `S.qIncM`, `S.tails`.
    `tailExp` entre dans `profitBook` (donc « profit +1 ») et dans `rivPt`.
  - **Cartons** sur pertes et replis : rouge trimestre ≤ −12 %, repli ≥ 25 % (puis +5 pts), appel de marge, 2ᵉ jaune ;
    jaune trimestre ≤ −5 %, repli ≥ 12 % (puis +4 pts, réarmé sous 8 %), 10 pts sous la médiane, book vide, griefs.
    `S.bandTight` resserre ces seuils. `S.inBand` = trimestres sans carton (carte blanche). Haut fait « Irréprochable »
    = aucun carton sur 8 trimestres (`nocard`).
  - **Concurrents** : `RIVSTRAT` — Médaillon « Kelly fractionnaire » (26 %), Pont-Levis « Conviction » (16 % + 26 × force
    du scénario), Citadelle « Plein levier » (34 %). `rivVolQ` posé dans `planQuarter` (`rv.vq`, sans tirage), borné par
    `rivCapVol` = mêmes règles que le joueur (12 marchés, +4 à 1,4×, +4 à 2× ; plafond ±3/4/5 à 1×/1,2×/1,5×).
    Rendement `(v/2)(RIVK·e + bruit) − 0,8 % − rivDrag(v) − rivTail` ; `RIVK` 0,35 → 0,20 (l'adresse se dilue quand le
    book grossit). Colonne « Risque » et stratégie au débriefing, stratégies à l'accueil.
  - **Nuage** ancré à l'origine, sans pointillés ni bande, zoom sur le fonds le plus risqué, zone d'accidents teintée ;
    petit format : points et libellés en HTML (%), pas de déformation.
  - **Rubans** (`tapeSvg`) : échelle log bornée aux tracés, traits fins tous les 10 % (20/50/100 si plus de 7 lignes).
  - **Objectifs** : 11 textes/prédicats sans jauge ni bande (`c.sp` ajouté au contexte). **Textes** : +32 dépêches,
    +6 incidents, +12 accidents.
  - Mesures (copie figée) : régression 18 parties 0 erreur 0 écart ; `cover3` 3 264 plans 0 anomalie ; `goalchk`
    aucun prédicat cassé ; reprise à froid OK. 36 parties `play.js --lev 1|1.6` : 0 erreur, ~0,9 accident par partie
    à 1,6×, 1,5 rouge par partie avant le réglage du seuil médiane ; concurrents médians ×1,08 / ×1,65 / ×0,82 en deux
    ans (Citadelle ramenée ensuite de 40 à 34 %). `play.js` : option `--lev` et sorties `tails`, `red`, `riv`, `idx`.
  - Constat ancien, non corrigé : avec `play.js`, le style flux finit presque toujours à quelques M$ d'encours malgré
    une performance positive (rachats) — déjà vrai sur le fichier publié. À mesurer au bot intelligent.

- **Lot 67** (`99zzc-lot67.py`) — demandes d'Antoine :
  - **Mi-parcours** : latent = trimestre − dépêches/desk/incidents (il était recalculé à part, sans collatéral ni frais,
    et pouvait contredire le total) ; le titre parle du trimestre entier.
  - **Nuage μ / σ** : μ = rendement attendu annualisé (4 × trimestre), σ = risque ; abscisses toujours en bas, traits très
    fins tous les 10 % sur les deux axes, valeurs dans le cadre ; grand format : graduations, nom du fonds au lieu de
    « Vous », μ collé à l'axe (plus de recouvrement avec le nom).
  - **Trésorerie** à trois chiffres significatifs (`treso`). **Lignes de marché** : « rentabilité » au lieu de « profit »,
    ordre et coût en tête de ligne (`ordTxt`) à la place du rendement du trimestre passé.
  - **Sauts du ruban** : `rivRet` = chemin pur complet (bruit propre `rivNz`, accident à un instant `rtt`), `rivalReturns`
    = `rivRet(j,1)` sans tirage de `rng` ; dernier pas du trimestre à la densité des autres (`TAPEM`) ; commission de
    performance provisionnée au fil du trimestre (`liveNet`). Sonde : dernier pas des concurrents nul.
  - **Confiance / cartons** : plus de double peine (la perte > 10 % n'est plus notée par le comité, le carton s'en
    charge ; les « griefs accumulés » ne donnent plus de jaune — la dérogation au modèle du quant les nourrissait).
    Seuils : rouge −20 % / repli 30 % ; jaune −10 % / repli 18 % / 20 pts sous la médiane / book vide.
  - **Hauts faits et cartes** : libellés « jauge / comité » → confiance ; « Dompter le levier » (trimestre positif malgré
    un accident) ; carte blanche = quatre trimestres sans carton ; hauts faits d'encours relibellés en performance.
  - **Équilibrage** : `RIVKS` (quant 0,22, fondamental et flux 0,34), Citadelle 30 % de risque ; flux : `ddMax` 0,22,
    `lpMult` 1,35, intuition juste 85 %. Couper après un accident : le latent de la moitié coupée est acquis (`qEvM`).
  - **Bot** (`tools/bot.js`) : l'intelligent choisit l'échelle du book qui maximise `profitBook − ½σ²/4` (plus de cible),
    répond aux accidents (perte du fonds + 2 × trésorerie) ; sorties `red`, `yel`, `tails`, `sp`, `riv`.
  - Mesures, version publiée (`/tmp/g67.html`), 108 parties (6 graines × 3 styles × 3 difficultés × bots intelligent et
    nul) + 54 parties intelligentes : intelligent 100 % de survie (3 abandons flux sur 54), σ choisi 22 à 30 %, 0,2 à
    0,5 rouge et 0,3 à 1,3 jaune par partie, 0,3 à 1,2 accident ; nul : survie 17 à 83 %, score 2 à 8 M$, 0,5 à 1,2
    rouge. Scores moyens intelligents (36 parties par style) : quant ~36, flux ~24, fondamental ~18 M$ (σ 10 à 34) —
    la campagne précédente, sur d'autres graines, donnait l'ordre inverse : **écart de styles non démontré**.
    Performance médiane décroissante avec la difficulté (quant 1,89 / 1,69 / 1,48). Concurrents médians sur deux ans
    +91 / +95 / +65 %. Régression 18 parties, `cover3` 3 264 plans, reprise à froid : 0 erreur, 0 écart.

- **Lot 68** (`99zzd-lot68.py`) :
  - Trader débauché (`S.star`) : coûts ×0,5 sur **toute sa classe** (`grp`), plus ÷3 sur un seul marché.
  - `kPrev(e,mode)` simule sur une copie du book les effets déterministes d'un choix (« mid » = règles de
    `screenTraderEvent`, « exec » = anecdotes d'exécution) et rend le coût des ordres ; `bkD(k1,cost,hid)` affiche
    marchés modifiés, rentabilité, risque (comme les lignes de marché) et coûts. Branché sur anecdotes, desk,
    exigences, conseil, « suivre le mouvement » des dépêches, suivre/contrer un concurrent (coût désormais ×`tcMultQ`,
    comme appliqué) et « couper » d'un accident. `randAdd`/`trendAdd` signalés, pas chiffrés. Contrôle : 482 choix,
    0 échec, book restauré (`tools/tmp/prevchk.js`).
  - Nuage : μ et σ **trimestriels** (σ annuel / 2), traits tous les 5 %, point jaune pâle = book avant les derniers
    changements (`S.k0` sur la page du book, `S.kVal` pendant le trimestre). Les lignes de marché restent en σ annuel.
  - Or : lingot SVG dans `MFLAG`. Hauts faits durcis (série 4, objectifs 4/7, acier 6 % sur 8 trimestres, confiance 95,
    commissions ×0,75/×2/×5, Sharpe probabiliste 97,5 %, performance +200 %/+400 %) ; Graal : 8 trimestres, premier,
    aucun trimestre négatif, aucun carton, +150 %, repli < 8 %.
  - `tools/shot.py` restait bloqué au premier book (bouton d'envoi grisé) : il ajuste le book (`#fitbook`) avant d'envoyer.
  - Régression 18 parties : 0 erreur, 0 écart ; `goalchk` : aucun prédicat cassé. Fréquence des hauts faits non mesurée.

## Calibration (bot intelligent, `tools/bot.js`)

Méthode : parties appariées (même graine, même style) entre une option et le standard ;
`tools/calib.py`. Le bruit est grand (σ du score ≈ 30 M$ sur 2 ans) : compter 150 parties par
option pour un écart de 2 M$. Les budgets sont payés par la société de gestion, qui ne touche que
20 % de la performance : un budget n'est rentable que si son effet sur le fonds vaut environ cinq
fois son coût. Campagnes : `tools/runner.js` + `tools/loop.sh` sur une **copie figée** du jeu (champ `file`
du plan) : `loop.sh` relit le fichier à chaque tranche, une modification en cours de campagne
fausse les résultats.

### Styles, budgets et lisibilité

- Quant : `modelScale` 0,80, `ddMax` 0,40. Flux : intuition juste 93 fois sur 100,
  `modelScale` 1,20, `lpMult` 1,60, `ddMax` 0,16. `ddMax()` centralise le seuil de liquidation.
- Budgets : salle de marché 2/18/50 pb, contrôle 4/12/24 pb, recherche 4/18/64 pb.
- `POSRX` / `evTouchesBook()` écartent du début de trimestre et du conseil les exigences et
  événements qui coupent des positions : le book y est à plat.

Piège de méthode (captures) : **Chromium sans écran n'échantillonne pas SMIL pendant le
déroulé** — les animations sautent de l'état initial à l'état final, et toute image
intermédiaire est donc fausse. Pour filmer : `svg.pauseAnimations()` puis
`svg.setCurrentTime(t)` avant chaque capture (`tools/shot5.py --film`). Attention, le compteur
JS, lui, suit l'horloge réelle : sur un film ainsi piloté il n'est pas synchrone avec le tracé.

Piège de méthode : `sed 's/a.html/b.html/'` sur un plan JSON d'une seule ligne ne remplace
que la première occurrence. Générer les plans en Python.

### Mesure de référence après les lots 1 à 5

90 parties (30 graines × 3 styles), bot intelligent, copie figée, 0 erreur.
**Les chiffres des campagnes antérieures sont périmés** : ils ont été obtenus sur une
économie qui n'existe plus (bonus d'objectif quadruple, exécution payée par le fonds,
effets d'événement en montants fixes).

| Style | Score moyen | σ | Médiane | Survie | Causes de fin |
|---|---|---|---|---|---|
| Quant | 17,1 M$ | 8,8 | 17,0 | 73 % | investisseurs 7, liquidation 1 |
| Fondamental | 26,9 M$ | 32,7 | 17,4 | 60 % | liquidation 10, investisseurs 2 |
| Flux *(avant lot 6)* | 30,8 M$ | 22,7 | 23,9 | 67 % | liquidation 9, investisseurs 1 |
| **Flux** *(après lot 6)* | **31,9 M$** | **29,8** | **25,1** | **57 %** | liquidation 13 |

L'ordre voulu quant < fondamental < flux est respecté sur le score. Le quant meurt des
investisseurs, les deux autres de la liquidation.

**Lot 6 — le flux paie sa prise de risque.** Il survivait mieux (67 %) que le fondamental
(60 %) tout en gagnant plus : un style censé être le plus risqué ne peut pas être à la fois le
plus rentable et le plus sûr. Vérifié dans `tools/bot.js` : le book est dimensionné sur
`S.tgt*0.95*modelScale` et **pas** sur `ddMax`, donc le seuil de liquidation est un vrai
levier — le baisser ne fait pas réduire les positions en compensation. Le repli maximal des
vingt survivants montrait un trou net : 0,159 · 0,127 · 0,112 · 0,109 puis rien au-dessus de
0,076. Réglages : `modelScale` 1,20 → 1,35, `ddMax` 0,16 → 0,13, `incMult` 1,0 → 1,25.
Résultat sur les mêmes 30 graines : 20 survivants → 17, score 30,8 → 31,9, σ 22,7 → 29,8.
La comparaison appariée avant/après est solide ; l'écart flux-fondamental (57 % contre 60 %,
soit une partie) est en revanche **dans le bruit** — la forme est bonne, la marge n'est pas
démontrée. La confirmer demanderait quelques centaines de parties par style.

Économie par partie : bonus d'objectif ≈ 6 M$ (3,1 objectifs tenus), exécution 4,5 à 6,0 M$,
budget 5,4 à 6,5 M$. L'exécution coûte 0,6 à 0,85 M$ par trimestre, soit environ 2 % de
l'encours par an — haut de la fourchette réaliste, assumé pour que le poste existe dans le jeu.
Le bonus d'objectif pèse désormais ~16 % du revenu brut du gérant, contre ~43 % avant.
Encours final médian 184 M$ (quartiles 118 et 281) ; 67 parties sur 90 vont au bout des huit
trimestres.

### Coût d'exécution réellement constaté

Mesuré sur 104 clôtures (`goalchk.js` l'imprime), en pb de l'encours et par trimestre :

| décile | quartile | médiane | quartile | décile | max |
|---|---|---|---|---|---|
| 19 | 26 | **33** | 60 | 83 | 142 |

Soit environ 1,3 % de l'encours par an, book entièrement reconstruit chaque trimestre et
réactions aux dépêches comprises. C'est la référence à laquelle caler tout seuil exprimé en
`tcBp`.

### Lot 7 — ce que `goalchk.js` a trouvé

- **`tcBp` était mille fois trop petit** : `|tcM| / (navB*1000) * 1e4`, alors que `tcM` et
  `navB` sont tous deux en Md$. Conséquence : « L'exécution frugale » (< 15 pb) et
  « L'exécution chirurgicale » (< 8 pb, prime 0,10 — la deuxième plus grosse du jeu) étaient
  vraies **à tous les coups**. Défaut antérieur aux lots 1 à 6, invisible parce qu'un objectif
  toujours gagné ne se plaint pas. Corrigé.
- Les quatre seuils exprimés en `tcBp` (15, 12, 10, 8 pb) dataient d'un monde où ouvrir un
  book coûtait 4 pb ; corrigés, ils devenaient tous inatteignables. Recalés sur les quantiles
  ci-dessus : 26, 22, 20, 16 pb.
- Effet sur l'équilibre : négligeable (score 17,1 / 26,9 / 31,9 → 16,9 / 26,5 / 31,5 ; survie
  inchangée). Ces deux objectifs ne sortent que dans ~2 % des trimestres.
- **Aucun prédicat cassé** : aucun ne lève, aucun ne rend autre chose qu'un booléen, aucun ne
  lit un champ absent du contexte.
- 16 objectifs ne se déclenchent jamais **pour le bot**, parce qu'il ne fait jamais varier son
  budget ni la forme de son book (« Le budget serré », « À l'aveugle », « Le desk de luxe »,
  « Le book minimal », « La ligne qui paie », « Le spécialiste », « Sans actions »…). Ils sont
  atteignables par un joueur : ne pas les « corriger » sur cette base. Pour les couvrir
  vraiment il faudrait faire varier la politique du bot, ce qui reste à faire.
- « Rien d'appelé » (pas d'appel de marge) est toujours vrai sur 104 trimestres : les appels
  de marge sont, en pratique, inexistants pour un joueur qui tient son book.

### Lot 10 — ce que la couverture forcée a trouvé

- **Deux effets d'événement que personne n'appliquait.** `carry` (« Un book de portage vous
  est proposé ») et `leak` (« Nouvelle obligation de reporting position par position ») étaient
  écrits dans les anecdotes, et le moteur savait parfaitement les traiter — `resolveQuarter`
  contient la règle du portage (+0,6 % par trimestre, −3,5 % en crise), `tcost` applique le
  ×1,45 sur les grosses positions publiées. Mais aucun gestionnaire ne posait `S.carry` ni
  `S.leak` : le joueur acceptait un book de portage qui n'existait pas. Deux lignes.
- **`halfOn:'ZW'`** : une anecdote écrivait une chaîne là où toutes les autres écrivent un
  tableau. Le gestionnaire des anecdotes tolérait les deux, celui du conseil appelait
  `.forEach` et cassait. Normalisé, et le gestionnaire accepte désormais les deux formes.
- **Violation de l'invariant 3** dans le même gestionnaire : `setK(IDX[sy], …)` sans garde
  `IDX[sy]!==undefined`. Sur un univers réduit, le marché cité peut ne pas exister et on
  écrivait dans `S.k[undefined]` — silencieux, et pire qu'une exception. Gardé.
- **Deux textes offraient des milliards à un fonds de cent millions** : un bloc de Brent de
  4 Md$ et une souscription souveraine de 12 Md$ (dont l'effet, lui, valait 12 % de l'encours).
  Les 25 autres mentions de milliards parlent du monde extérieur et sont légitimes.
- Après correction : 662 choix forcés, **aucune erreur, aucun « undefined », aucun « NaN »**,
  aucune clé d'effet morte, aucune jauge au-delà de ±15.

### Difficulté : mesurée, laissée en l'état, et pourquoi

La survie globale est de 67 % contre ~51 % dans les campagnes antérieures. **Ne pas chercher
à revenir à 51 %** : cet écart vient de la correction des effets `cashM`, qui ponctionnaient
1,6 M$ par trimestre au hasard des anecdotes de desk. Sur une partie mesurée avant correction,
le fonds mourait avec des positions à −4 M$ et des anecdotes à −13,9 M$ : il était tué par le
desk, pas par le marché. L'ancien taux de survie était donc gonflé par un défaut, pas par une
mécanique de jeu.

Le seuil de liquidation est un **levier mort** — mesuré : le repli maximal médian des
survivants est de 0,133 (quant), 0,079 (fondamental) et 0,052 (flux), contre des seuils de
0,40 / 0,28 / 0,16. Baisser `ddMax` de 20 % ne coûte que 3 à 10 points de survie. La partie
est binaire : soit on explose, soit on croise loin du seuil. Si la difficulté doit être
retouchée un jour, le levier intéressant est la patience des investisseurs (`lp`), qui est une
pression graduelle et jouable, pas la liquidation, qui est une falaise.

- **Lot 57 — nettoyage, troisième passe** (`99zs-nettoyage3.py`) : écran d'accueil, le mur des
  25 marchés et les concurrents passent dans un repli « Les marchés et la concurrence » (le
  joueur voyait tout défiler avant même le bouton « Fonder le fonds »). Anecdotes du desk
  (exécution et mi-parcours) : le texte de tête répétait mot pour mot la ligne du bouton déjà
  lue, pendant que l'effet chiffré était caché sous « Le détail » ; c'est inversé, plus de
  répétition quand il n'y a rien d'autre à dire. Rapport final : la démonstration du Sharpe
  probabiliste (deux paragraphes + formule) passe dans un repli « Le calcul », seul le chiffre
  reste en tête. Régression 11 parties (9 combinaisons + fondamental + flux), reprise à froid,
  `cover3` 2 832 plans : 0 erreur, 0 écart.

## Reste à faire

### En premier
- **Reconstruire les outils perdus** : `cover.js`/`cover2.js` (couverture forcée des anecdotes
  et dépêches, chaque choix), `goalchk.js` (108 prédicats d'objectif), `featchk.js`,
  `flowchk.js`. Sans eux, toute production de texte est non vérifiée. `resumechk.js` est
  partiellement couvert par `play.js --resume N`.

### À trancher

- **Crans 9 et 10 du budget : piège ou option ?** Mesurés perdants à coup sûr (ci-dessus).
  Trois voies : (a) les laisser en piège assumé, inaccessibles en début de partie faute de
  trésorerie ; (b) faire payer au fonds la part au-delà du cran 8, comme une vraie société de
  gestion refacture certains frais — le bénéfice redevient comparable au coût ; (c) resserrer
  l'échelle (max 1,5× au lieu de 2×). Décision d'Antoine attendue.

### Plus loin
- **Équilibre des styles** : le bot intelligent classe quant > flux > fondamental sur 108 parties, l'inverse sur les 72
  précédentes. Il faut ~100 parties par style et par difficulté (graines communes) avant de toucher aux styles.
- Production de texte : 200 anecdotes d'exécution (145 aujourd'hui) et 300 dépêches (269),
  plus la démultiplication des débriefings.
- Rentabilité des budgets : non remesurée depuis le changement d'économie. Avec un seul cœur,
  une campagne de 90 parties prend ~7 minutes ; compter ~300 parties appariées par niveau.
- **Réduction de variance : fait au lot 11**, et mesuré. Expérience appariée, 25 graines,
  style fondamental, budget recherche au niveau 0 contre le niveau 2, sur le fichier d'avant
  et celui d'après :

  | | écart-type de la différence appariée | erreur type sur 25 parties |
  |---|---|---|
  | Flux séquentiel unique | 13,5 M$ | 2,69 |
  | Flux nommés | **6,7 M$** | **1,34 |

  La variance de la différence est divisée par quatre : **il faut quatre fois moins de parties**
  pour la même précision. Ce n'est pas le facteur dix espéré, parce qu'il reste une divergence
  irréductible — deux budgets différents produisent deux books différents, donc deux P&L
  différents même sur le même marché. Mais une campagne de 300 parties par niveau tombe à 75.
  Prochaine étape naturelle : les variables antithétiques, chaque graine jouée avec `+f` et `−f`.
- **Attribution de P&L** à la clôture : `S.f` et les charges `b` sont là, la décomposition
  croissance / inflation / dollar / appétit + résidu est quasi gratuite. C'est ce qui manque
  pour que le joueur comprenne pourquoi il perd.
- **Sonde étendue** : `play.js` ne vérifie l'égalité affiché/appliqué que sur `resolveEvent`.
  Même contrôle à la clôture et sur les événements du conseil, qui écrivent aussi `S.lastG`.
