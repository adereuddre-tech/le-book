# Le Book — note de reprise (état au lot 90)

Jeu de gérant de hedge fund global macro. Fichier unique `index.html` (~716 ko),
publié sur GitHub Pages : https://adereuddre-tech.github.io/le-book/
Dépôt : `adereuddre-tech/le-book`, branche `main`. Dernier lot publié : **90**.
L'historique détaillé des lots 1 à 75 et les anciennes mesures sont dans `docs/HANDOFF_archive_lot90.md`.

## Règles d'Antoine (à respecter)

- Réponses **en français**, **brèves** : ce qui a changé, les chiffres clés, ce qui reste ouvert. Pas de
  récapitulatif détaillé.
- Consignes fermées (« fais X, Y, Z, publie ») : les exécuter sans proposer d'options. Quand une question
  de conception est ouverte, la poser **avant** de coder (ex. équipe de gestion, plus bas).
- **Patchs Python ciblés** avec `rep(old,new,k)` qui *assert* le nombre d'occurrences ; jamais de réécriture.
- **Test jsdom d'une partie complète avant publication** ; régression de 18 parties (`tools/reg.sh`,
  0 erreur, 0 blocage, 0 écart exigés) ; reprise à froid (`play.js --resume N`).
- **Captures d'écran** : au plus une par lot, seulement si l'affichage change ; Antoine vérifie souvent
  lui-même en ligne.
- **Campagnes** (60 à 270 parties) seulement quand l'équilibre change. Lots d'affichage : régression seule.
- Publication : `git push` avec un jeton fourni en début de session (fine-grained PAT, Contents R/W). Le
  jeton circule en clair dans la conversation : rappeler à Antoine de le révoquer.

## Méthode et outils (détails techniques)

**Écart à la méthode d'origine** : les lots 76 à 90 ont été appliqués **directement sur `index.html`**, pas via
`base.html` + `patches/NN-*.py` + `build.sh`. Leurs scripts sont archivés dans `patches/lots76-90/` pour
traçabilité mais **ne sont pas rejouables** par `build.sh` (ils supposent l'état du lot précédent).
`build.sh` reconstruit donc l'état du lot 75 seulement. Pour la suite : repartir de `index.html` publié.

Pièges de patch rencontrés : l'indentation réelle diffère souvent de l'affichage (préférer des ancres sans
blancs de tête) ; dans le HTML, `\'` est **une** barre oblique (en Python : `"d\\'"` s'écrit `"d\'"`).

Outils ajoutés depuis le lot 75 (dans `tools/`, jsdom local : `npm i jsdom`) :
- `bot.js` — `playGame({file,seed,prof,size,dur,bud,av,probe,collect})`. `av` = aversion au risque :
  défaut 1 (« bot habituel » : retranche lui-même drain et coût moyen des accidents), `av:0` = **glouton**
  (maximise la rentabilité affichée). `probe` : script injecté au chargement ; `collect` : expression
  évaluée en fin de partie. Le bot annonce le **premier** cran (standard) et garde 25 % de co-investissement.
- `runner.js` + `loop.sh` : campagne sur un plan JSON (liste d'options par partie), reprise automatique ;
  lancer détaché : `(setsid nohup bash tools/loop.sh plan.json res.jsonl > /dev/null 2>&1 < /dev/null &)`.
  Une partie ≈ 5–8 s sur un cœur ; 90 parties ≈ 8 min. Les processus meurent si le conteneur est recyclé :
  relancer `loop.sh`, il reprend au bon endroit.
- `reg.sh <fichier> <sortie>` puis `python3 tools/summ.py <sortie>` : régression de 18 parties.
- `patches/lots76-90/lot89_cov.js` : couverture dynamique — évalue **tous** les prédicats d'objectif et de
  haut fait à chaque clôture de 36 parties ; repère les prédicats jamais / toujours vrais.
- Dépouillement type (score moyen, médiane, survie, risque, cartons, accidents par étiquette) : voir
  `patches/lots76-90/` et l'analyse appariée (même graine, même style) utilisée dans les campagnes.

## Méthode de travail (à respecter)

- **Réponses en français.**
- **Patchs Python ciblés**, jamais de réécriture du fichier. Chaque patch utilise une
  fonction `rep(old, new, k=1)` qui *assert* le nombre d'occurrences avant de remplacer :
  une ancre ambiguë doit faire échouer le patch, pas produire un remplacement au hasard.
- **Un lot par fichier, rejouable.** `base.html` est le fichier publié intact, `patches/NN-*.py`
  applique un lot chacun (via `patches/_lib.py`), `build.sh` reconstruit `index.html` en
  rejouant tout dans l'ordre. Une session coupée ne perd rien : il suffit de relancer
  `sh build.sh` (le fichier n'est pas exécutable). Chaque patch porte en tête le constat mesuré qui le justifie.
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


## État actuel du jeu (fait foi sur l'architecture détaillée plus bas)

- **Choix de départ** : style (quant `syst` / fondamental `fonda` / flux `flux`), difficulté (`size` :
  small = facile, mid = normal, mega = difficile), durée (express 4 / normal 8 / saison 12 trimestres).
  L'univers est fixé à `ext` et la vol cible n'est plus un choix (lot 49). Encours de départ 100 M$.
- **Trésorerie du gérant = score** : `mgrNet()` = commissions − tout ce qu'il a payé (budget, exécution,
  accidents, incidents, restitution) ± co-investissement. `mgrCash()` = `mgrNet()` − part co-investie
  **bloquée** (`coinvLocked()`). Le bot et les campagnes comptent `(mgrFees−mgrCosts)`.
- **Co-investissement** (lots 81–90) : choisi au débriefing, 25/50/75/90/95/100 % (`COINVS`, défaut 25 %).
  À l'ouverture, `S.coinvLock` sort de la trésorerie disponible et entre dans l'encours ; à la clôture,
  rachat automatique du gérant avec le résultat du trimestre. Concurrents : 25 % implicite (`ci`).
- **Restitution** (`CLAW`=3) : sous le plus-haut, le gérant rend 3 × repli des commissions de performance des
  quatre derniers trimestres (plafond 100 %, pas de double restitution, `S.perfH`). Concurrents idem.
- **Fin de partie** : encours < 40 M$ rachats compris (`FUNDMIN`), ou repli d'indice ≥ 50 % (`DDEND`,
  `S.over='dd'`). Rachats : `RDM` (confiance ≤ 20, repli, confiance < 40), risque (`RISKLP`, `RISKQ`
  quadratique), cartons rouges (5 % de l'encours).
- **Risque** : moteur en **annuel** (`riskShown`, `pvol`, seuils `TAIL`, `RISKCAP`, `RISKLP`), **affichage
  en trimestriel partout** via `RQ(v)=v/2` (lot 84). Nuage : risque trimestriel, collatéral compris au
  point de départ (`colStdQ`). Risque propre des marchés ×1,5 (`IDIOX` dans `normB`). Prime de risque
  `PREM` : actions +1,2 %, taux +0,4 % par trimestre.
- **Rentabilité affichée** (`profitBook`, lot 85) = lecture des marchés (signaux, sources, prime, collatéral)
  − impact de marché des ordres depuis le book de départ − financement convexe `FINK·(σ/0,2)²`.
  **Ni drain de volatilité ni coût moyen des accidents** : ils dépendent du risque et se lisent sur l'axe du
  risque. C'est ce qui punit le glouton ; ne pas les réintroduire.
- **Accidents de levier** (`TAILEV`, 27 dont 7 appels de marge `mg:1` et 4 squeezes/corner/saut) :
  probabilité `(e+0,8e²)·p` (e = excès de risque au-delà de 20 % annuel), protection du contrôle des
  risques qui s'efface de 30 à 40 % (`tailMit`), perte `tailL`×1,5 ; minuteur sur tous (défaut : couper).
- **Comité** : jaune à 30 % de risque annuel en clôture (15 % trimestriel), rouge à 45 % (`RISKCAP`) ; jaune
  immédiat si la confiance tombe à zéro en séance (`midYellow`) ; un rouge impose **deux** contraintes
  (`redDraw2`, `S.redC.list`).
- **Annonce** : trois crans fixes — standard 3 % (±4), conviction forte 9 % (±12), « Prophétie de gourou »
  15 % (+22/−25). Soldée **hors plafonnement** de la confiance.
- **Incident opérationnel** : deux maux au choix (tout réparer, en partie à vos frais / contenir, confiance
  ×2,2), minuteur.
- **Concurrents** : `rivSkill` 0,05 / 0,09 / 0,18 ; en difficile, budget choisi par `rivBudget` ; risque à
  mi-chemin de celui qui maximise leur rentabilité (`rivVolQ`) ; points du nuage mis à jour en séance
  (`rivPtLive`, affichage seulement).
- **Budgets** : trois postes, sept crans ; crans 4–6 coûtent ×4/3, ×5/3, ×2 et leurs effets sont ramenés
  à 70 % de leur écart au standard (lot 79). `budExpl(id)` chiffre chaque effet.
- **Débriefing** : bloc « L'essentiel » (fonds, rachats, collatéral, confiance début → fin, engagement,
  objectif, comité, gain du trimestre, trésorerie, **tableau des concurrents**, **tableau de la trésorerie**),
  puis alertes, choix du co-investissement, sections repliées.
- **Ruban** : « T n À DATE ±x % · DEPUIS LE LANCEMENT ±y % », trait au début du trimestre ; points au
  prorata du temps (`tapeM`) pour une volatilité homogène.
- **Objectifs** : 108 (`QGOALS`), filtrés au tirage par `pre` (trimestre précédent), `sym` (marché ouvert),
  `cls` (classe ouverte). **Hauts faits** : 37 (`FEATS`), dont « Le prophète ».

## Architecture du fichier

- **Marchés** : `INSTR_ALL` (25 marchés, 5 classes × 5), champ `rk` = rang d'ouverture, **par liquidité croissante dans la classe**
  (coût d'une unité à l'ouverture, lot 72) ; l'ordre du tableau suit `rk`.
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
- **Textes** : `MACROEV` (347 dépêches, 13 extrêmes), `TRADER_EXEC` (170), `TRADER_MID` (51),
  `STAKE` (34), `INCIDENTS` (19), `TAILEV` (18), `BOARDEV` (16), `RUMORS` (88), `PRESS_SRC` (24), `PRESS_EXTRA`.
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


> Les puces ci-dessus datent du lot 75. En cas de contradiction, la section « État actuel » prévaut
> (notamment : annonce, économie du gérant, budgets, risque, fin de partie).

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
14. L'ordre de `INSTR_ALL` fait partie du format de sauvegarde (`d.ord`) : le changer invalide les
    sauvegardes en cours. Ne jamais indexer un marché par position.

15. Le risque se **calcule** en annuel et s'**affiche** en trimestriel : toute nouvelle valeur affichée passe
    par `RQ()` ou `*50` au lieu de `*100`.
16. `profitBook` ne contient ni drain ni accidents (lot 85). Le bot habituel les retranche lui-même.
17. À la clôture, `S.q` est **déjà incrémenté** quand on passe aux cartons (`S.midY===S.q-1`).
18. `S.lastG` cumule les appels de jauge à moins de 250 ms : la flèche du panneau = effet total d'une action.
19. Le co-investissement doit être rendu à chaque clôture (`S.coinvLock` remis à 0) : sinon il reste compté
    deux fois dans l'encours.

## Lots 76 à 90 (détail)

- **Lot 76** (`lot76/patch.py`, `patch2.py`) : quadrillage du ruban en paliers ronds espacés d'au moins H/7
  (l'ancien repli sur un pas de 10 % empilait des dizaines de lignes au-delà de ×20) ; confiance à zéro =
  carton jaune immédiat (`midYellow`, `S.midY`), consigné à la clôture — attention, `S.q` y est déjà incrémenté,
  d'où `S.midY===S.q-1` — et jaune aussi si la confiance est nulle à la clôture ; appels de marge : 5 accidents
  `mg:1` de plus (+2 anciens marqués), 45 % des tirages (`TAILMG`), perte plafonnée à 45 %, `TAIL.p` 0,50 → 0,60,
  gravité moyenne `TAILSEV` calculée (0,68) ; objectifs `pre:'loss'|'gain'` filtrés au tirage (rebond, retour en
  grâce, la série) ; collatéral : `rehyp` (+3,0 %, 25 % de −9 %) et `junk` (+4,5 %, 30 % de −12 %), ligne de
  résultat (surcroît, défaut, net) et lignes « dont » à la clôture ; alertes du débriefing enveloppées dans un
  `<span>` (le flex coupait aux `<b>`). Campagne 90 parties appariées : quant −3,8 ± 1,8, fondamental
  −7,4 ± 3,0, flux 0,0 ; jaunes et rouges ×2 à ×4 (le bot reste souvent à confiance nulle).

- **Lot 77** (`lot77/pA.py` + réglages) : ordre des styles et difficulté. L'intuition du flux entre dans
  `S.factEst` (`HUNCHW` 1,4) : le desk du flux se dimensionnait sur un attendu qui l'ignorait (risque 0,21 → 0,39) ;
  flux `lpMult` 1,35 → 1,20 ; difficile `flowIn` 2,6 → 1,6, `lpNeg` 1,45 → 1,60 ; jaune de clôture pour confiance
  nulle seulement au trimestre où elle y tombe (`S.lpClose`). Campagne 180 parties : quant 26,9 (méd. 15,5,
  survie 100 %), fondamental 35,4 (28,6, 100 %), flux 39,1 (25,5, 83 %, +15,0 ± 3,9 apparié) ; facile −4,4 ± 1,8
  (survie 96 %), difficile 0,0 ± 1,5 (82 % contre 93 %). Ouvert : quant et fondamental à 100 % de survie au
  niveau moyen ; ~2 jaunes et ~1,2 rouge par partie, surtout des chutes à zéro en cours de trimestre ;
  flux − fondamental dans le bruit, ~200 parties par style pour conclure.

- **Lot 78** (`lot78/patch.py`, affichage, pas de campagne) : tuile d'encours à quatre chiffres significatifs
  (`money4`) ; tableau de la concurrence : cumul porté par chaque ligne (la recherche par nom `split(' · ')`
  ratait selon le nom du fonds → cumul à 0) ; ruban : `ytdIdx` ne compte le latent qu'en séance
  (`S.phase==='events'&&S.live`) — au débriefing, `liveNet()` recomptait le trimestre clos, d'où un ruban à
  +408,9 % contre +199,4 % en tête ; dernier point du règlement posé exactement sur l'indice ; volatilité
  homogène : chaque segment compte `tapeM(dt)=round(48·dt)` points (avant : 48 points par mise à jour, d'où des
  trimestres en cours étirés et plats), mêmes découpes pour les concurrents ; minuteur sur les appels de marge
  (`ev.mg`), faute de réponse le prime broker liquide la moitié (option `cut`), `armTimer(fn,lbl)`.

- **Lot 79** (`lot79/patch.py`) : budgets hauts — coûts des crans 4/5/6 ×4/3, ×5/3, ×2 (salle 43/85/150 pb,
  contrôle 24/43/72, recherche 47/100/192) et effets ramenés à 70 % de leur écart au standard (tous les
  tableaux EXECM…TAILM, RESN arrondi). Concurrents en difficile (`rivBud:1`, `rivSkill` 0,12 → 0,15) :
  `rivBudget(rv)` choisit chaque trimestre un cran 3–6 (les trois postes ensemble) qui maximise
  `RIVBRET[L] − λ·Δcoût`, λ = 3 % de l'encours / trésorerie borné à [0,5 ; 1,5], s'ils ont deux trimestres
  de surcoût en caisse ; `rivalCostQ(rv)` facture le cran, `bRet` s'ajoute à `rivRet` et `rivPt`.
  Nuage : `rivPtLive` — en séance, risque ×exp(1,6·r_t) borné à [0,6 ; 1,3], bruit ±5 % par dépêche,
  attendu + 0,35·r_t (affichage seulement). Campagne 270 parties : standard inchangé ; difficile −0,6 ± 1,5,
  rang moyen 2,76 contre 1,93, crans des concurrents en fin de partie ≈ 4,6 ; crans 5 : salle −0,6 ± 2,0,
  contrôle +1,4 ± 2,7, recherche −3,7 ± 2,6 (lot 75 : +2,5 / +4,4 / +3,6).

- **Lot 80** (`lot80/patch.py` + `patch2.py`, réglages C3) : prise de risque pénalisée. Financement convexe du levier
  `FINK·(σ/0,2)²` par trimestre (`FINK` 0,006, `finDrag`) dans `liveRet`, `navNow`, le brut de clôture et
  `profitBook` ; concurrents : `rivDrag` au même barème. Accidents dès 20 % (`TAIL` x0 0,20, w 0,30). Comité :
  jaune à 30 % de risque ex ante de clôture, rouge à 45 % (`RISKCAP`). Investisseurs (`RISKLP`) : confiance −4
  par tranche de 5 pts au-delà de 20 %, retraits 0,30 %/pt au-delà de 20 % × `flowMult`, idem pour l'encours
  et le plus-haut des concurrents. Bot : option `av` (aversion, défaut 1 ; 0 = glouton). Campagne (15 graines ×
  3 styles) : normal glouton 19,5 / habituel 19,5 / prudent 16,4 (avant 25,2 / 24,3 / 21,6), survie 93 %;
  difficile glouton 19,2 (67 %) / habituel 17,4 (62 %) (avant glouton 24,4, 82 %). Apparié glouton − habituel :
  +0,9 ± 1,6 avant, 0,0 ± 1,2 normal, +1,7 ± 1,2 difficile. Cause restante : la commission de performance est
  une option d'achat pour le gérant (il touche les gains, ne paie pas les pertes) ; piste : co-investissement.

- **Lot 81** (`lot81/patch.py`) : co-investissement du gérant, `COINV` 0,10 de la trésorerie d'ouverture
  (`S.coinvBase`, fixée après la commission de gestion) × résultat net du trimestre, passé en `mgrFees` si gain,
  `mgrCosts` si perte (tous les consommateurs du score restent cohérents), cumul `S.mgrCoinv`, ligne dans le
  détail « Vos gains » ; concurrents : `ci` dans `rivalMgrQuarter`. Campagne 225 parties : +0,6 ± 0,1 (normal) et
  +0,4 ± 0,1 (difficile) pour le bot habituel ; glouton − habituel 0,0 ± 1,3 / +1,8 ± 1,3 : inchangé. Attendu :
  un terme linéaire en rendement ne pénalise pas la variance. Piste : restitution (clawback) des commissions
  de performance en cas de repli sous le plus-haut, qui est concave.

- **Lot 82** (`lot82/p1.py`, `p2.py`, `p3.py`) : co-investissement choisi au débriefing (`COINVS` 10/25/50/75/100 %,
  `S.coinvPct`, base `S.coinvBase` fixée à l'ouverture, valorisée en séance dans `mgrNet` : trésorerie = gain net
  cumulé, un seul chiffre) ; restitution `CLAW`=3 × repli sous le plus-haut des commissions de performance des
  4 derniers trimestres (`S.perfH`, plafond 100 %, pas de double restitution), concurrents idem (`rv.perfH`).
  Clôture : `FUNDMIN` 50 M$ (rachats compris) ou repli d'indice ≥ `DDEND` 50 % (`S.over='dd'`, verdict dédié).
  Rouge : `redDraw2` = deux contraintes distinctes (`S.redC.list`, `redOn`/`redBlock` itèrent). Engagement soldé
  hors plafonnement de la confiance (il était absorbé par le plafond +22). `S.lastG` cumule les appels de jauge
  à moins de 250 ms (flèche du panneau = effet total de la dépêche). Panneau `T5/8`. Débriefing : bloc
  « L'essentiel » (fonds, confiance début → fin et 3 causes, engagement, objectif, comité, gain du trimestre
  décomposé, trésorerie), alertes, choix du co-investissement ; concurrence, presse/commentaires, confiance,
  film, attribution repliés. Budgets : `budExpl` chiffre bruit des indicateurs (σ), fiabilité par classe,
  pré-annonces, lecture des dépêches. Desk : un seul bloc replié à plat (sources, avis du desk, matrice).
  Campagne 179 parties : survie normal 47–49 %, difficile 23–27 %, toutes par encours < 50 M$ (T3,9 en
  moyenne) ; glouton ≈ habituel (15,1 / 15,3 ; 13,6 / 12,8). À régler : rachats trop forts pour ce seuil.

- **Lot 83** (`lot83/patch.py`) : clôture sous 40 M$ (`FUNDMIN` 0,04) ; rachats adoucis (`RDM` : confiance ≤ 20
  → 3 % + 0,3 %/pt, repli 6 % + 25 %, confiance < 40 → 2 %, risque `RDMFK` 0,15 %/pt) ; difficile `flowMult`
  1,60 → 1,15. Ruban : « T n À DATE ±x % » (tracé depuis `S.tape.q0`) en plus du cumul, trait pointillé au début
  du trimestre (`opt.qs`, `opt.ql` de `tapeSvg`), idem au débriefing. Risque annualisé partout : étiquette et
  graduations du nuage (positions toujours tracées en trimestriel, libellés ×2), note du nuage réécrite.
  Campagne 180 parties : normal habituel 17,1 (survie 73 %), glouton 17,3 (78 %) ; difficile 16,9 (47 %).

- **Lot 84** (`lot84/p1.py`, `p2.py`) : risque propre des marchés ×1,5 (`IDIOX` dans `normB`) ; prime de risque
  `PREM` (actions +1,2 %, taux +0,4 % par trimestre) dans `drawReturns` et `expRet`. Accidents : probabilité
  `(e+0,8e²)·p` plafonnée à 0,97, protection du contrôle qui s'efface de 30 à 40 % (`tailMit`), `tailL` ×1,5,
  options plus lourdes (tenir 0,5/1,8 L, couper 0,8 L, couvrir 0,5 L + 0,3 L), quatre accidents de plus
  (short squeeze, corner, gamma squeeze, saut de prix), minuteur sur tous (défaut : couper). Confiance et
  rachats quadratiques au-delà du confort (`RISKQ`), concurrents compris. Co-investissement 25/50/75/100 %,
  la part placée entre dans l'encours (`S.coinvIn`, ajusté à l'ouverture). Incident : deux maux (tout réparer,
  en partie à vos frais / contenir, confiance ×2,2), minuteur. Conviction forte ×3 (±15). Concurrents : risque
  à mi-chemin de celui qui maximise leur rentabilité attendue. Risque affiché en trimestriel partout (`RQ`),
  nuage : collatéral compris au point de départ (`colStdQ`). Mi-parcours : trimestre à date sur le ruban.
  Débriefing : concurrence dans l'essentiel, rachats et collatéral en une ligne (détail replié en bas),
  engagement « ≥ x · tenu ». Carton rouge : cadre de 340 px, dégradé et halo. Rapport final : durée juste
  (`ANS`), verdicts plus enlevés. Campagne 135 : normal 13,3 (64 %), glouton 14,1 (67 %), difficile 12,7 (42 %).

- **Lot 85** (`lot85/patch.py`) : la rentabilité affichée (`profitBook`) n'est plus que la lecture des marchés moins
  le financement facturé — ni drain de volatilité ni coût moyen des accidents, qui se lisent sur l'axe du risque ;
  `rivPt(rv,v,full)` : même lecture pour le nuage, version complète pour leur choix de risque ; bot : l'habituel
  retranche lui-même drain et accidents, le glouton (`av` 0) maximise l'affichage. Difficile `lpNeg` 1,60 → 1,40.
  Campagne 135 : habituel 13,3 (64 %), glouton 3,8 (29 %, risque 0,40), apparié −9,5 ± 2,7 ; difficile 13,9 (47 %).

- **Lot 86** : concurrents plus forts (`rivSkill` facile 0,02 → 0,05, normal 0,05 → 0,09, difficile 0,15 → 0,18) ;
  rachats adoucis `RDM={lp0:0.015,lpk:0.002,dd0:0.04,ddk:0.20,low:0.01}`. Campagne (variante J2 sur J1) : normal
  14,5 M$, survie 73 %, rang moyen 2,6 (≈ 1,9 au lot 79) ; difficile 14,3 M$, survie 64 %, rang 3,0.
  La rentabilité affichée compte l'impact de marché des ordres depuis le book de départ (`tcost().imp`),
  pas la commission, payée par le gérant.

- **Lot 87** (`lot87/patch.py`, affichage et annonce, pas de campagne) : annonce à trois crans fixes — standard 3 %
  (±4), conviction forte 9 % (±12), « Prophétie de gourou » 15 % (+22/−25) ; « silence radio » retiré, objectif
  « Le moine » exclu (`pre:'never'`), haut fait « L'invisible » devenu inaccessible. Risque des marchés à deux
  décimales. Systématique : le book du modèle affiché hors du bloc replié. Pop-up d'encours : souscriptions et
  rachats cumulés (`S.flowInC`, `S.flowOutC`, cumulés à l'ouverture), co-investissement et sa part, encours hors
  vous, seuil de fermeture. Débriefing : tableau de la trésorerie (début `S.tresQ0`, commissions, bonus,
  co-investissement, restitution, budget, exécution, autres par différence, fin).

- **Lot 88** : objectif « Joueur de poker » (annoncer ≥ 9 % et les livrer, bonus 0,10) à la place du « Moine » ;
  haut fait « Le prophète » (palier 3, tenir une prophétie de gourou, `tq`) à la place de « L'invisible ».

- **Lot 89** (`lot89/patch.py` + corrections) : audit des 108 objectifs et 37 hauts faits. Couverture dynamique
  (`lot89/cov.js` : tous les prédicats évalués à chaque clôture de 36 parties) ; corrigés : risque et volatilité
  réécrits en trimestriel dans les libellés ; « Le renseignement rentable » comparait à 1 Md$ au lieu de
  l'encours (`navM`) ; « Le trimestre du comptable » avait le signe inversé ; « Surfer la tendance » visait un
  régime inexistant (→ reflation) ; « Le trimestre calme » impossible (→ « Sans faux pas ») ; plafonds ±3/±5
  rendant deux objectifs acquis (`cap`) ; « Rien d'appelé », « La marge tranquille », « Le trimestre propre »,
  « Aucun facteur dominant » acquis à 89–100 % (durcis, 25–67 %) ; objectifs de marché/classe tirés seulement
  si ouverts (`sym`, `cls`) ; hauts faits « Le mastodonte »/« L'homme de fer » sans l'univers, qui n'est plus un
  choix. Bot : l'annonce cliquait le 2ᵉ cran (conviction forte) depuis le lot 87 → 1ᵉʳ. Restent à 0 chez le bot,
  faute de le jouer : budgets renforcés, conviction forte, prophétie, book mono-classe — atteignables à la main.

- **Lot 90** (`lot90/patch.py`) : co-investissement bloqué — à l'ouverture, `S.coinvLock` = part × trésorerie sort de
  la trésorerie disponible (`mgrCash` = `mgrNet` − `coinvLocked()`, valeur en séance comprise) et entre dans
  l'encours ; à la clôture, rachat automatique du gérant (`S.nav` −= base × (1+résultat)), résultat passé en
  trésorerie. Crans 25/50/75/90/95/100 %. Reprise des sauvegardes lot 84–89 (co-investissement resté dans
  l'encours) : retiré à la première ouverture.


## Calibration actuelle (lots 85–86, bot habituel sauf mention)

| | Score moyen (M$) | Survie | Rang moyen |
|---|---|---|---|
| Normal | 14,5 | 73 % | 2,6 |
| Difficile | 14,3 | 64 % | 3,0 |
| Normal, glouton (`av:0`) | 3,8 | 29 % | — |

Glouton − habituel (apparié) : −9,5 ± 2,7 M$ au lot 85. Styles (lot 77, avant les lots 80–86) :
quant < fondamental < flux en moyenne, flux le plus risqué. **Attention** : du lot 87 au lot 89, le bot
annonçait « conviction forte » par erreur ; aucune campagne n'a été rejouée depuis la correction. Une
campagne de référence (≈ 135 parties : habituel et glouton en normal, habituel en difficile) est la
première chose à relancer avant tout nouvel équilibrage.

Antoine a accepté que le difficile rapporte autant que le normal (il est plus dur par le classement et la
survie). Cibles de survie : ≈ 70 % en normal, ≈ 60 % en difficile.

## Reste à faire

### En cours : l'équipe de gestion (conception validée à moitié, rien de codé)

Demande d'Antoine : budgets simplifiés en deux postes — **front office** (fusion salle de marché +
recherche macro) et **back office** (contrôle des risques + les 5 pb de frais de base aujourd'hui cachés) ;
l'équipe s'étoffe avec le cran de budget ; descriptions et visuels par cran, séparés front / back.

Préalables faits (à valider par Antoine) :
1. Employés présents dans les textes (nombre d'anecdotes) : Boris Rasoumovsky, devises (22) ; Ingrid
   Bergström, taux (22) ; Bartolomeo « Tuco » Ossobuco, énergie (22) ; Mireille Cauchemar, contrôle des
   risques (25) ; Wing-Fat « Winnie » Leung, Asie (20) ; Jean-Kevin Lévêque-Charbonnier, junior (18) ;
   Dwight Tannenbaum, exécution quantitative (15) ; Sœur Marie-Alpha, exécution systématique (10). Hors
   équipe : Ken Griffon (patron concurrent), cabinet Marchand & Fils.
2. Affectation proposée — front : Ingrid (cheffe du desk taux), Boris (devises), Tuco (matières premières),
   Winnie (actions et Asie), Dwight (exécution et algorithmes), Sœur Marie-Alpha (stratégiste quantitative,
   recherche), Jean-Kevin (analyste macro junior) ; back : Mireille (directrice des risques). À créer pour les
   crans hauts : économiste en chef (front), responsable du middle office (back), directrice de la
   conformité (back).

**Question posée, sans réponse** : la composition de l'équipe conditionne-t-elle les événements (pas
d'anecdote de Tuco avant son recrutement) ou reste-t-elle décorative ? Attendre la réponse avant de coder.
Impacts connus de la fusion : `BUDGET` (3 postes → 2), `S.bud.exec/res/risk` lus partout (budEf, budExpl,
objectifs `budRes`/`budExec`/`budRisk`, hauts faits `omni`, `ascet`, `monk`, bot `bud:[e,r,s]`, sauvegardes).

### Ensuite
- Campagne de référence (voir Calibration).
- Hauts faits jamais atteints par le bot faute de jouer ces choix (budgets renforcés, conviction forte,
  prophétie, book mono-classe) : vérifiables seulement à la main ou avec un bot dédié.
- Production de texte : objectif de 200 anecdotes d'exécution et 300 dépêches, textes de débriefing.
