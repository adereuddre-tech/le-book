# Le Book — note de reprise (état au lot 90)

Jeu de gérant de hedge fund global macro. Fichier unique `index.html` (~716 ko),
publié sur GitHub Pages : https://adereuddre-tech.github.io/le-book/
Dépôt : `adereuddre-tech/le-book`, branche `main`. Dernier lot publié : **174**.
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
- `play.js … --clicks` : active la gate et négocie une limite à chaque débriefing où c'est possible.
- `bot.js` : option `lim` (défaut vrai) — le bot ne dépasse pas 97 % de `limVol()`.
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
- **Budgets** (lot 92) : deux postes, front office 7 crans (`FOP`) et back office 5 crans (`BOP`), crans cumulatifs
  nommés ; `syncBud()` recopie `fo` vers `exec/res/ret` et `BOMAP[bo]` vers `risk`, les anciens tableaux restent lus.
  Avant le lot 92 : trois postes, sept crans ; crans 4–6 coûtent ×4/3, ×5/3, ×2 et leurs effets sont ramenés
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


- **Lot 91** (`lot91/p1.py`, `p2.py`, affichage, pas de campagne) : pop-up « Trésorerie » réécrite — gains nets cumulés
  ventilés (gestion, performance, bonus, co-investissement dont latent, restitution, budget, courtage, autres) jusqu'à la
  trésorerie disponible (part co-investie bloquée déduite) ; bloc co-investissement (part, valeur du moment, rachat,
  exemple chiffré à ±5 %, cumul). Nouveaux cumuls `S.cMgmt`, `S.cPerf`, `S.cBon`, `S.cOps`, `S.cTC` (courtage au NAV de
  facturation, comme `mgrNet`) ; `S.led` marque les parties qui les tiennent, sinon ligne « non ventilé ». Résidu
  « autres » = accidents et incidents à votre charge, vérifié nul hors accidents sur 5 parties sondées. Débriefing :
  ligne co-investissement avec part et mise. Régression 18 parties : 0 erreur, 0 blocage, 0 écart.

- **Lot 92** (`lot92/p1–p4.py`) : budget en deux postes. Front office : Jean-Kevin 0, Dwight (actions) 10, Ingrid (taux) 25,
  Boris (devises) 50, Tuco (matières) 75, Winnie (exotiques) 120, Sœur Marie-Alpha 200 pb (prix de l'équipe entière).
  Back office : loyer 5 (les 5 pb de base), Maître Lettrage 15, Josiane Suspens 30, Mireille 40, l'inspecteur Tatillon 60.
  Départ : `fo` 3, `bo` 1. Classe sans son trader (`covered`, `TRD`) : commission et impact ×1,5 (`NOTRD`), mention dans
  l'en-tête de classe du book. Licenciement : indemnités = écart de prix (`sevRaw`), plafonnées à la caisse (`setOps`).
  Débauchage nominatif : `S.gone={p,n,boss}`, siège vide un trimestre, contre-offre (`S.cntBp`). Concurrents : ancien
  barème figé `RIVBP`. Reprise des sauvegardes : `fo` = moyenne salle/recherche, `bo` = cran le plus proche via `BOMAP`.
  Bot : `bud:[fo,bo]`. Campagne 180 parties appariées sur le lot 91 : standard +3,3 ± 3,4 M$ (neutre) ; Tuco + Mireille
  −7,0 ± 1,6 au premier barème, −5,6 ± 1,6 après baisse des crans hauts (60 parties) : monter coûte plus qu'il ne rapporte.
- **Lot 93** (`lot93/p1–p2.py`) : l'équipe conditionne les anecdotes. `cast(ev)` réécrit auteur et textes (champs imbriqués
  compris, `deepCast`) quand la personne est absente : courtier de la classe, back office présent (Josiane ou Lettrage à la
  place de Mireille). `PERSO` : 5 anecdotes sur une personne précise, retirées en son absence ; anecdotes de Sœur
  Marie-Alpha retirées sans elle (texte au féminin). `ev.t0` garde le titre d'origine pour `usedExec`/`usedEv`.
  Répliques d'arrivée (`hi`) dans le toast de recrutement. Régression 18 parties 0/0/0, reprises à froid OK.
- **Lot 94** (`lot94/p1–p4.py`) : pas de co-investissement au premier trimestre (trésorerie de départ = commission de
  gestion, 500 k$) ; front office 0/10/25/45/70/100/150 pb ; « indemnités » → « versement du bonus » ; classe sans trader
  ×5 (`NOTRD`) après campagne de 180 parties appariées : ×3 −0,3 ± 0,8 M$ face à ×1,5, ×5 −2,6 ± 1,5 ; équipe complète
  − standard −1,2 ± 1,3 à ×3, +1,1 ± 1,6 à ×5. Neuf anecdotes de milieu de trimestre pour Maître Lettrage (bo ≥ 1),
  Josiane Suspens (bo ≥ 2) et Tatillon (bo ≥ 4), filtrées par `persoOk`. Couverture forcée sans anomalie.
- **Lot 95** (`lot95/p1.py`) : classe sans trader ×4 (`NOTRD`). Bonus d'équipe : au débriefing d'un trimestre à commission de
  performance positive, 0/10/25 % de celle-ci (`BONUS`, `S.bonI`) et un bénéficiaire (`S.bonWho`) ; versé à l'ouverture
  suivante par `payBonus()` (après `S.tresQ0`, avant le co-investissement, plafonné à la caisse). Effets sur ce trimestre :
  débauchage ×1/×0,6/×0,3 (`BONM`, `S.bonMultQ`), bénéficiaire intouchable et coûts de sa classe −10 % (`S.bonWhoQ`).
  Deux trimestres gagnants sans bonus (pas forcément consécutifs, `S.noBon`) : grogne, débauchage ×1,5. Lignes dans la
  pop-up (`S.cBonT`) et le tableau de trésorerie (`S.qBonT`). Campagne 90 parties appariées : 10 % −0,7 ± 0,2 M$, 25 %
  −1,6 ± 0,4 M$, survie 60 → 63 → 67 % : le bonus coûte son montant et ne rapporte presque rien au bot, le débauchage
  (seulement si rachats > 1 %) étant rare. Score moyen 4,5 M$, survie 60 % (normal).
- **Lot 96** (`lot96/p1.py`) : débauchage de base à chaque clôture, 50 % (`POACHP`), ×0,5 avec 10 % de bonus, ×0,2
  avec 25 % (`BONM`), grogne ×1,5 ; plus de bénéficiaire ni de +14 % durable : le coût est le siège vide un trimestre.
  `RETM` n'est plus lu ni affiché. Deuxièmes prénoms (`full`). Dwight à la voix, Boris à l'algorithme (les 15 anecdotes
  « exécution quantitative » passent à Boris). Économiste en chef, Pr Onésime Barnabé Atterrissage-en-Douceur, cran 7
  à 250 pb : `ecoBoost()` à chaque trimestre (un rang de marché si `OPENRK`<5, sinon les exotiques, sinon confiance +3
  à la télévision ou au comité, ou une dépêche lue juste `S.ecoB='ver'`) ; `syncBud` plafonne les anciennes tables au
  cran 6. Back office : Josiane neutre (défaut `bo:2`), barème 5/10/15/30/45 pb, `BOMAP=[0,2,3,5,6]`, tables réécrites à
  ces crans (loyer : incidents ×5, gravité ×2, accidents ×2,5, comité −3 par clôture ; Tatillon : incidents ×0,7,
  comité +4). Maître Lettrage → Maître Gontran Hilaire Report-à-Nouveau. Bot : standard `[3,2]`.
  Campagne 180 parties appariées (standard, sans bonus : 11,2 M$, survie 80 %) : bonus 10 % −2,5 ± 0,8, 25 % −4,5 ± 0,8 ;
  économiste −6,0 ± 2,9 (survie 90 %) ; loyer seul −3,8 ± 2,5 (survie 63 %) ; Tatillon +0,9 ± 2,6 (survie 83 %).
- **Lot 97** (`lot97/p1.diff`, `p2.py`) : bonus 5/10 % (`BONUS`). Surnoms anglais pour le front (Jean-Kevin « Jay Kay »,
  Dwight « The Voice », Ingrid « Iceberg », Boris « Black Box », Tuco, Winnie, Sœur Marie-Alpha « Sister Sharpe »,
  Pr Onésime « The Oracle »), plus de deuxième prénom au back office. Anecdotes nouvelles : Dwight 16 (13 d'exécution à
  la voix, 3 de desk), Jean-Kevin 5, l'économiste 6, Report-à-Nouveau 4, Josiane 4, Tatillon 4 ; une anecdote de devises
  « à la voix » passe de Boris à Dwight. Anecdotes de Dwight retirées en son absence (`persoOk`), de l'économiste sans le
  cran 7. Le p1 est un diff : le script d'origine a été perdu lors d'un redémarrage de la machine.
  Campagne 90 parties appariées : bonus 5 % +0,1 ± 0,5 M$, 10 % −0,1 ± 0,4 (neutres). Contrôle sur les mêmes graines
  contre le lot 96 : −2,0 ± 1,0 M$ (nouvelles anecdotes), graines plus dures (3,8 M$, survie 60 %).
- **Lot 98** (`lot98/p1–p2.py`) : ouverture du trimestre dans l'ordre bonus d'équipe → co-investissement en % de la
  trésorerie restante (`cashCo`, avant la commission de gestion, qui reste hors co-investissement) → gestion. Au
  débriefing, `cashView()` = `mgrCash()` − `bonPend()` − `coPend()` alimente la tuile, la note du co-investissement et
  la pop-up ; vérifié égal aux montants réellement prélevés. Point fantôme du graphique rentabilité / risque : risque avec
  le collatéral, comme le point courant. Restitution supprimée (`CLAW=0`, joueur et concurrents ; l'ancienne ligne ne
  s'affiche que si une sauvegarde en porte). Budget : « descendre, c'est licencier » et coût des départs sous chaque cran
  inférieur à celui du trimestre précédent (`S.budPrev`). Campagne 90 parties appariées contre le lot 97 : +3,8 ± 1,0 M$,
  survie 69 → 78 %.
- **Lot 99** (`lot99/p1.py`) : « Gagner une place » (`pre:'rank2'`) et « Deux places d'un coup » (`rank3`) seulement
  à partir du 2e trimestre et si le rang le permet. Dépêches : la confiance suit le résultat net de la dépêche,
  `pnlD(p)` = `cf(pnlGz(imm+p))` − `cf(pnlGz(imm))` (`S.evImm`), dans les boutons comme à l'application (0 écart) ;
  seule la nervosité reste à part. Débauchage : traders seulement (`FOP[p].cls`). Chasseur de têtes : l'anecdote
  « Citadelle Nord veut recruter {X} » (`hunt:1`) vise un trader présent (`huntCands`, `S.huntP`, qui est aussi la
  cible du débauchage suivant). Back office à six crans : la commandante Solange Pare-Feu (60 pb), `BOMAP=[0,1,3,4,5,6]`,
  incidents ×5/×2/×1/×0,8/×0,65/×0,5, gravité ×2/×1,3/×1/×0,8/×0,65/×0,5, accidents de levier ×2,5/×1,4/×1/×0,8/×0,65/×0,5,
  comité −3/−1,5/0/+2,5/+4/+5 ; quatre anecdotes pour elle (bo ≥ 5). Campagne 120 parties appariées : nouveau
  standard −0,5 ± 0,5 M$ contre le lot 98 (confiance moyenne 42 → 46), Tatillon −1,3 ± 1,3, Pare-Feu −2,0 ± 1,1.

### Refonte « la totale » (A à E), validée par Antoine
- **Lot 100, A · prime broker** (`lot100/p1–p2.py`) : ordre ouverture → desk → budget → book (rumeurs après le budget).
  Type de produit `x.pt` (devises, fret, pluie = gré à gré, marge ×1,3 ; `PTYPE`), `mgRate(i)` = taux × type ×
  `S.mgMult` (1 + 0,3·(liq − 1) à l'ouverture, ×(1 + 0,04·choc) après une grosse dépêche, plafond 1,5 ; ×`mg` d'un
  scénario, plafond 2). Contrôle dans `stepEvents()` après chaque événement : au-delà de `MGC.thr` 50 %,
  `screenMarginCall()` : apport de la société (juste sous le seuil, bloqué avec le co-investissement), coupe choisie
  (×1,3, jusqu'à `MGC.back` 45 %), liquidation par le prime broker (×1,8, confiance −5, choix du minuteur). La marge
  déposée rapporte T-bills −10 pb (`mgShare`, `colYield`, `colExp`, `colStdQ`). `TAILMG` 0 ; plus de pénalité de marge à
  la validation. Liquidation automatique de clôture conservée. Mesuré seul : +0,6 ± 0,7 M$.
- **Lot 101, B · scénarios de stress** (`lot101/p1–p10.py`) : 24 scénarios `STRESS` (10 sévères, 14 extrêmes 3 fois
  moins probables) : chocs de facteurs `sh`, chocs de marchés `x`, cibles sur le book `tgt` (short, rogue, otc, crowd),
  `liq`, `mg`, `shut`. Probabilité `stressP()` 10 à 32 % selon la liquidité affichée. Tirés à `planQuarter`
  (`S.stressQ`), insérés dans la file comme une dépêche (tag `stress`), recalculés à l'affichage sur le book réel
  (`stressEv`, `stressHit`). Immédiat × back office (0,5 + 0,5·`TAILM`), pertes × `crowd(sp)` = 1 + 2,5·max(0, sp − 0,20)/0,10,
  coût de liquidité toujours perdant `stressGap` (`STRGAP` 0,28, ×2 si extrême). Plus d'accident de levier pour le
  joueur (`tailP(sp)` = 0 sans `std` ; `tailExp` du joueur = coût attendu des scénarios). Panneau du book : les six pires
  scénarios pour votre book, les autres repliés. Campagne 45 parties appariées contre le lot 99 : +2,8 ± 2,1 M$,
  survie 59 % (62 % au lot 99 sur ces graines), vol du bot 20,4 % ; 1,3 scénario et 0,8 appel de marge par partie.
  Réglages traversés : sans frein +24 ± 8,5 ; amplification seule +13 ; coût de liquidité 0,12 +9,6.
- **Lot 102, C · investisseurs nommés** (`lot102/p1.py`) : `INVR` (caisse de retraite des Cheminots 35 %, fonds souverain
  de Nordhavn 30 %, family office Vandermeer 15 %, fonds de fonds Albatros 20 %), état `S.inv=[{id,w,off,ntc}]` créé
  paresseusement (`invs()`, les vieilles sauvegardes passent). Satisfaction = `S.lp` + `off` (humeur propre : poids par
  cause de confiance `wt`, via `invCat` sur les libellés de `S.lpD`, ramenée vers `off0` ×0,85, bornée ±25). Sous `thr`
  (25/20/35/30) : avis de rachat `ntc` = 30 % + 70 % × écart relatif × `flowMult`, payé à la clôture suivante, retiré à
  `thr`+8 ; clause de repli de la caisse (½ de sa part au-delà de `ddMax()`). Souscriptions au-dessus de 65 (6/10/15/12 %
  de la part × `flowIn` × capacité) ; retour d'un investisseur parti à 70 (5 % de l'encours initial). Gate (`gateOk`,
  `S.gateNext`) choisie au débriefing si les avis dépassent 15 % de l'encours : paiement à 15 % au prorata, reste reporté,
  confiance −6, pas deux trimestres de suite. `invFlow(v,amt)` tient les parts ; les flux d'anecdotes restent au prorata.
  Supprimés : flux par concurrent, `RDM.low`, retrait pour risque, les deux `redeem()`, 5 % du rouge, `midFlows`.
  Affichage : `invTable()` dans « L'essentiel » et la pop-up d'encours, alerte « avis de rachat ».
- **Lot 103, D · comité à limites** (`lot103/p1–p2.py`) : `LIM` ; `limVol()` 0,30 annuel (15 % trimestriel, rouge ×1,5),
  `limStop()` −10 %, `limConc()` 70 % du risque (`riskContrib`) dans une classe (`clsConc`) ; vol et stop × √(bande du back
  office) × `bandTight`. Affichées par `limRows()` (book, pop-up du comité). Stop vérifié dans `stepEvents` (`screenStopQ`) :
  couper de moitié (×1,3, aucun carton même si la perte continue, `S.stopCut`) ou passer outre (jaune, `S.stopY`) ; puis
  `noAddQ`. Clôture : rouge si risque ≥ 1,5 × limite ou trimestre ≤ 2 × stop sans avoir coupé ; jaune si risque > limite,
  stop franchi sans couper, concentration > limite. Négociation au débriefing (`S.limNeg={id,q}`) : risque ×1,25, stop +3
  pts ou concentration +15 pts un trimestre, confiance −3 à l'ouverture, sans carton et pas deux fois de suite. Retirés :
  cartons repli/médiane/book vide/appel de marge/confiance nulle, `midYellow`, pénalité de risque dans la confiance,
  −7/−12 de clôture sur appel de marge, coût en confiance des cartons (−2/−6).
- **Lot 104, E · fin économique** (`lot104/p1–p3.py`) : budget facturé sur `budNav()` = max(encours, encours initial) ;
  garder son équipe n'est jamais verrouillé (seul monter exige la caisse, plus de rétrogradation automatique). Fin :
  `S.cashNeg` ≥ 2 clôtures de suite en trésorerie négative (`S.over='cash'`, « Dépôt de bilan »), ou fonds vidé
  (`extNav()` < 1 % de l'encours initial). `FUNDMIN`/`DDEND` ne sont plus lus. p2 : appel de marge en boucle sur un fonds
  presque vide → book soldé si la coupe ne suffit pas.
- **Recalibration** (bot avec `lim` : il respecte la limite de risque ; normal 90 parties appariées, difficile 45) :

  | | Score moyen | Médiane | Survie | Fins (faillite / vidé) | Rang |
  |---|---|---|---|---|---|
  | Lot 101, normal | 22,8 | 11,0 | 64 % | — / 32 (encours) | 2,67 |
  | Lot 104, normal | 21,9 | 10,3 | 76 % | 13 / 9 | 2,67 |
  | Lot 104, difficile | 23,3 | 8,1 | 58 % | 10 / 9 | 2,96 |

  Apparié lot 104 − lot 101 (normal) : −0,6 ± 1,9 M$ avant p3, p3 −0,7 ± 0,3. Rachats cumulés 23 M$ (70 au lot 101),
  souscriptions 45. Quant faible : survie 63 % en normal, 33 % en difficile.
- **À faire** (ancienne liste, fait aux lots 102–104) : C (investisseurs nommés : caisse de retraite, fonds souverain, family office, fonds de fonds ; satisfaction,
  rachats sur préavis d'un trimestre, souscriptions, gate ; remplacent les sept sources de rachats), D (comité à limites
  affichées : vol ex ante, stop trimestriel contrôlé dans `stepEvents`, concentration ; limite négociable ; plus de
  pénalités en double ni de jaune à confiance nulle), E (fin sur trésorerie négative à deux clôtures, à la place de
  `FUNDMIN` et du repli de 50 %), puis recalibration complète.

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

### Équipe : suite
- Textes des nouveaux venus : trois anecdotes chacun (lot 94), à étoffer.
- Bonus d'équipe à 5/10 % (lot 97) : neutre pour le bot.
- Scores en baisse depuis le lot 91 (9,7 → 4,5 M$ au bot) et survie ≈ 60 % pour une cible de 70 % : à rééquilibrer.
- Économiste en chef (lot 96) : −6 M$ au bot pour 250 pb, surtout utile à la survie.
- Premier trimestre : 500 k$ en caisse contre 600 k$ pour le standard (45 + 15 pb) : le front descend à Ingrid, accepté par Antoine.
- Crans hauts non rentables pour le bot (voir lot 92) : effets à renforcer ou prix à baisser, à remesurer.

### Lots 105–110 (détail)
- **105 · Investisseurs sur la confiance** (remplace la satisfaction du lot 102). `INVR` : déclencheur propre
  (`invVerdict`) — caisse de retraite : régularité (rachat si 3 des 4 derniers trimestres < 0, souscription après 4 > 0) ;
  fonds souverain : objectif (annonce, sinon mandat) manqué / tenu deux fois de suite ; family office : absolu (< −3 % /
  > +4 %) ; fonds de fonds : écart à la **moyenne** des concurrents (±3 pts, lot 110). Montant : rachat = `out` × 2 ×
  (1 − confiance/100) × `flowMult` (`out` 0,45/0,35/0,55/0,50 depuis lot 110 p4), souscription = `inn` × confiance/50.
  Préavis d'un trimestre, avis retiré si le verdict repasse positif ; gate et clause de repli inchangées. Historique `S.invH`.
- **106 · Événements extrêmes** (ex-scénarios de stress) : vocabulaire, `ev.x` (cadre rouge clignotant `xblink`).
  Annonces `xHintDraw()`/`xHintTxt()` : rumeur `XH.rum[res]` (5 à 65 %), fausse alerte 6 % ; fondamental : source vérifiée
  1 fois sur 2 ; quant : modèle de risque 6 fois sur 10 (nomme + perte du book) ; flux : intuition toujours, sans nom.
  Affichées dans les sources, à l'écran du desk et sur le book.
- **107 · Budget** : cran 0 partout au premier trimestre ; cran choisi surligné (`.lvl.tm.on`) ; « hors trésorerie »
  en rouge (`.hx`) ; boutons d'événements désactivés plus lisibles.
- **108/110 · Bonus et motivation** : `BONUS` 0/5/10/15/20 %, réglage permanent `S.bonI` (10 % par défaut). Motivation
  `S.mot` : vise √(taux/20 %) (`motTg`), 70 % du chemin par trimestre, +0,10 par cran de hausse, −0,18 par cran de baisse.
  `execMot()` = gain du budget salle de marché × (0,5 + 0,5 m) × (1,15 − 0,30 m) ; remplace `EXECM[S.bud.exec]` partout.
  Débauchage `poachNow()` = 50 % × (1 − 0,8 m), ×1,6 le trimestre d'une baisse. Mesure appariée (60 parties par taux) :
  10 % − 0 % = +2,7 ± 1,4 M$, 20 % − 10 % = −0,8 ± 0,6 M$ : optimum intérieur à 10 %.
- **109 · Tuyaux du prime broker** (`TIPS`, 7 affaires, espérance positive, 35 % des trimestres, écran `screenTip` avant
  l'exécution, boutons `data-tip`) : pris, le fonds paie et encaisse tout de suite ; refusé, un concurrent le prend
  (`S.xRiv`). Le bot les prend.
- **110** : objectif du trimestre sur le book (`objRows`) ; concurrents exposés aux événements extrêmes par un book
  implicite (`rivFx` rejoue les tirages de `rivalE`, `rivBookW` à 60 % de leur vol plafonnée à 20 %, `XRIVR` 0,75 du
  mouvement complet) ; facteur 2 affiché « Liquidité » = −dollar (`FSG=[1,1,-1,1]`, affichage seul : charges et tirages
  inchangés) ; code mort retiré (`redeem`, `midFlows`, `midYellow`, `RDM`, `RISKCAP`).
- Calibration (bot, taux de bonus 10 %) : normal 87 % de survie (quant 85, fondamental 95, flux 80), difficile 67 %.
  Faillites : 8 sur 60 en normal, 11 sur 45 en difficile.

- **111** : amplification de foule plafonnée à ×2,5 (`crowd`) — pertes immédiates jusqu'à 44 % du fonds auparavant.
  Apparié : +4,1 ± 1,9 M$ en normal, −0,1 ± 0,7 en difficile ; survie inchangée (87 % / 73 %). Resserrer les
  déclencheurs des investisseurs ne change pas la survie : les fins sont des faillites de la société de gestion.

- **112** : bonus d'équipe minimal 5 % (crans 5 / 7,5 / 10 / 15 / 20 %, défaut 10 %) ; faillite dès la première clôture
  en trésorerie négative (`S.cashNeg>=1`). Apparié (bot, bonus 10 %) : normal 70 % de survie (quant 75, fondamental 75,
  flux 60), score −2,1 ± 0,8 M$ ; difficile 71 %, inchangé. Faillites surtout au premier trimestre (9 sur 18 en normal).

- **113 · Progression styles × difficultés** : capital de départ de la société de gestion `SIZES.seed` (facile 0,6 M$,
  moyen 0,3 M$, difficile 0 ; `S.mgrSeed` ajouté à `mgrFees` à la création), coût de l'équipe `SIZES.costM`
  (0,85 / 1 / 1,20, dans `budNav()`), coûts d'exécution du quant ×0,80 et du fondamental ×1,12. Cause : au premier
  trimestre, commission 0,5 M$ ≈ budget 0,3 M$ + ordres 0,2 à 0,5 M$ : la faillite du premier trimestre ne dépendait
  pas de la difficulté. Bot : `reserve` (défaut 35 %) — il garde une réserve de trésorerie hors budget.
  Mesure (bot prudent, 25 parties par case, écart type ≈ 9 pts par case) : survie facile 75 %, moyen 69 %, difficile 63 %
  (cibles 80 / 70 / 60) ; par style, toutes difficultés : quant ≈ 71 %, fondamental 76 %, flux 63 % (cibles 80 / 70 / 60 :
  quant et fondamental encore inversés, dans le bruit). Score moyen 15,6 / 19,7 / 17,9 M$ : le difficile ne rapporte pas
  plus que le moyen.

- **114** : difficile à 30 % de commission de performance ; coûts d'exécution du quant ×0,72.
- **115** : trader de chaque classe dans l'en-tête du book ; budget : le licenciement (bonus de départ) n'est mentionné
  que sous le cran du trimestre précédent ; caisse de retraite sur 2 trimestres d'affilée ; fonds souverain chaque
  trimestre sur l'objectif annoncé (annonce standard par défaut) ; bonus à effet direct `BONFX` (part de la baisse des
  coûts livrée 50/65/80/95/110 %, débauchage 50/40/30/20/12 %, ×1,5 le trimestre d'une baisse, cran minimal sans
  commission de performance) — motivation supprimée ; négociation de limite stylée et facultative (`.lmp`, `.gtp`) ;
  flux coûts ×1,00, quant investisseurs ×0,75, difficile équipe ×1,35.
  Mesure (60 parties par case) : survie facile 77 %, moyen 68 %, difficile 60 % ; survivants 15,6 / 18,5 / 32,5 M$ ;
  styles : quant 66 %, fondamental 65 %, flux 73 % — coûts et patience ne classent pas les styles.

- **116** : impacts d'une unité au book en colonnes vente | achat (`.rgrid3`) ; book du modèle du quant à 90 % de la vol cible.
- **117** : Jean-Kevin stagiaire ; « Maître » retiré de Gontran ; Tatillon cran 3, Mireille cran 4 (crans inchangés) ;
  « CUMUL » sur le graphique ; annonces +5/−10, +15/−12, +30/−15 ; confiance des lignes de détail = texte (`gcf`) ;
  mi-parcours au chiffre du ruban ; écran du desk réécrit ; licenciement à un demi-trimestre (`sevRaw`×0,5) ; débauchage
  définitif, liste `S.gones`, un bouton « Faire revenir » par trader (`cntCost` = 1,5 trimestre de salaire) ; anecdotes
  de fidélisation à 15 pb minimum ; cadre flottant `cardWarn()` dès qu'un carton se prépare ; textes de fin de trimestre par
  investisseur (`invSay`). Bogue trouvé par la campagne : `G` resté dans la tuile « parti chez » → parties bloquées.
- **118** : intuition du flux juste 80 % du temps (bot : poids 1,03) ; le quant lit les trois signaux à ×0,6.
- **119** : gain brut des positions dans « l'essentiel » ; événement extrême des concurrents dans leur tableau ; tableau des
  investisseurs sans % ni critère, critères en clair, montants repliés ; holding royale « Couronne du Liquidistan » (`roy`,
  entre par le trophée, verdict = le plus sévère des quatre, rachat 55 %, souscription 5 %) ; dépêches : plancher `z.fl`
  si l'effet net sur le fonds est ≥ 0.
- **120** : capital de départ = difficulté (0,45 / 0,15 / 0 M$) + style (quant +0,40, fondamental +0,15, flux 0).
  Mesure lot 119 (270 parties) : survie facile 73 %, moyen 72 %, difficile 56 % ; styles 66 / 67 / 68 % ; scores 10,0 / 12,0 /
  14,3 M$. Lot 120 non remesuré.

- **121** : accueil réécrit (« Prenez les commandes… », objectif : engranger un maximum de bonus avant d'être débarqué) ;
  « Créez votre fonds » : trois choix, tutoriel « Comment on joue » en trois paragraphes, règles en sept lignes à jour
  (trésorerie, investisseurs, comité, chocs, liquidité), points d'interrogation dorés pleins (`.hintq`), aides, styles et
  difficultés réécrits sur les paramètres réels ; tutoriels des jauges, du budget et des facteurs à jour.

- **122** : coût de l'équipe selon le style (`STYCOST` quant 0,85 / fondamental 1 / flux 1,15, dans `budNav`) ; pré-annonces
  de banques centrales au sens économique (`EVFV` : assouplissement = liquidité, inflation, appétit en hausse ; le vecteur
  projeté lisait un rally obligataire comme croissance et liquidité en baisse ; `ev.fv` prioritaire) ; facteurs abrégés sur
  les lignes de marché ; Couronne du Liquidistan en dernier, souscription d'office 10 à 25 % de sa ligne selon la confiance,
  entrée aussi par l'événement du conseil (`royIn`) ; clause de repli de la caisse supprimée ; annonces +5/−5, +15/−8, +30/−10 ;
  description du flux détaillée ; écran de résultat du tuyau du prime broker (confiance +2 gagné, −1 perdu) ; concurrents :
  montant des accidents de levier, et événements extrêmes / accidents du joueur ; objectif du trimestre sur l'écran du desk ;
  portraits : icône de la personne citée et genre (`PGEN`, `personOf`).
  Mesure (357 parties, 40 par case) : survie facile 72 %, moyen 62 %, difficile 61 % ; styles quant 71 % · 12,7 M$,
  fondamental 61 % · 10,9 M$, flux 62 % · 10,5 M$.

- **123** : Winnie est une femme (`PGEN`, `g:'f'` sur Winnie et Ingrid, accords via `eF(p)`) ; coût de l'équipe flux ×1,30,
  difficile ×1,50 ; toutes les équipes ×0,80 (`BUDK`) pour qu'embaucher reste rentable en flux difficile (apparié, 30 parties :
  équipe standard − aucune équipe = +14,5 ± 7,7 M$, médiane 6,7 contre 5,4 M$, survie 63 % des deux côtés ; sans la baisse :
  médiane 4,5 contre 6,8 M$ et survie 53 % contre 63 %). Campagne générale non refaite après ce lot.

- **124** : les Cheminots retirent leur avis dès un trimestre positif (leur verdict ne pouvait passer que de rouge à neutre,
  l'avis était donc toujours payé) ; phrase de fin de trimestre quand un investisseur retire son avis.
  Mesure (335 parties, ≈ 37 par case, lots 123–124) : survie facile 76 %, moyen 69 %, difficile 65 % ; scores 9,8 / 11,6 /
  17,1 M$ ; styles quant 76 % · 14,5 M$ (médiane 8,6), fondamental 70 % · 14,2 M$ (7,1), flux 65 % · 9,9 M$ (3,8).

- **125** : commission de performance du flux +5 pts (`STYPERF`, dans `perfFee()`). Variantes, 60 parties de flux appariées
  (20 graines × 3 difficultés) : +2 pts +1,2 ± 1,4 M$ ; +5 pts +6,3 ± 2,2 ; +10 pts +16,5 ± 4,7 ; ×1,1 +1,7 ± 1,3 ;
  ×1,2 +2,2 ± 2,1. Retenu +5 pts : ramène le flux un peu au-dessus du quant et du fondamental en score moyen (9,9 → ≈ 16 M$
  contre 14,5 et 14,2 au lot 124). Tableau récapitulatif des styles (`styTable`, `STYSEED`) sous leurs cartes.

- **126** : texte « l'aura du prophète » pour la commission +5 pts du flux ; coûts d'exécution Dwight ×1,15 et Ingrid ×1,00
  (`EXECM` crans 1 et 2, avant ×1,30 et ×1,04) ; collatéraux prêts à effet de levier, stablecoins synthétiques, CDO au carré
  (le « pink sheet » écarté : aucun prime broker ne le prend en gage).

- **127** : difficile, équipe ×1,60. Tests croisés en flux difficile (25 graines appariées) : aucune équipe 17,6 M$
  (médiane 12,8, survie 68 %) ; légère +11,8 ± 7,6 M$ ; standard +14,9 ± 5,7 M$ (médiane +6,7, survie 72 %) ; maximale
  +19,0 ± 11,7 M$ mais médiane +1,0 et survie 56 %. Embaucher reste rentable.

- **128** : collatéral « Tokens liquides de NFT » (rendement 12 %, p 0,40, perte 0,35), en bas de liste.
  Testé et non retenu : nervosité des investisseurs du flux ×1,30 (au lieu de ×1,20) — 90 parties de flux sur les graines de la
  campagne du lot 127 : survie 70,0 % contre 70,1 %, score 14,6 contre 14,5 M$, aucun effet (les fins sont des faillites de
  trésorerie, que la confiance touche peu). Campagne générale du lot 127 (262 parties) : survie facile 76 %, moyen 72 %,
  difficile 62 % ; quant 73 % · 12,7 M$, fondamental 68 % · 11,6 M$, flux 70 % · 14,5 M$.

- **129** : incidents du flux ×1,75 en fréquence et ×2,2 en coût (`PROF().incSev` dans `screenIncident`). Mesure, 90 parties
  de flux (graines de la campagne du lot 127) : survie 70,1 → 65,6 %, score 14,5 → 14,6 M$. Classement visé atteint : quant 73 %,
  fondamental 68 %, flux ≈ 66 % en survie ; flux en tête au score.

- **130** : incidents du flux ×1,55 en fréquence (choix d'Antoine), coût ×2,2 inchangé. Mesure (90 parties de flux, graines
  du lot 127) : survie 67,8 %, score 14,8 M$, médiane 4,8 (×1,25 : 70,1 % / 14,5 ; ×1,5 seule : 70,0 % / 15,2 ;
  ×1,75 + coût ×2,2 : 65,6 % / 14,6).

- **131** : audit automatique du sens des 292 dépêches (pré-annonces, `/tmp/audit.js` à reconstruire si besoin : règles
  par mots-clés contre `eventFactorVec`). Chocs pétroliers et gaziers cohérents ; défauts et faillites lus « liquidité en
  hausse » → sens imposé (`EVFV` : croissance −, liquidité −, appétit −), sauf l'accord arraché in extremis. 11 alertes
  restantes, toutes de faux positifs de la règle (baisse du pétrole = inflation en baisse, à raison).

- **132** : incidents du flux ×1,65 en fréquence, coût ×2,2. Mesure (90 parties de flux, graines du lot 127) : survie 66,7 %
  (facile 73, moyen 70, difficile 57), score 15,1 M$, médiane 4,4.

- **133** : incidents du flux ×1,70 en fréquence, coût ×2,2 (choix d'Antoine). Équilibre gelé après la campagne finale.

- **134** : fondamental, coûts d'exécution ×1,00 (×1,12) et commission +2 pts (`STYPERF`). Campagne finale, durée normale,
  60 parties par case (lot 133) : quant 76 % · 25,6 M$ (méd 14,2), fondamental 70 % · 20,3 (8,4), flux 69 % · 30,1 (10,3) ;
  facile 81 %, moyen 70 %, difficile 64 %. Fondamental remesuré (180 parties appariées) : ×1,06 seul 76 % · 20,1 ; ×1,00 seul
  78 % · 21,7 ; ×1,00 + 2 pts 80 % · 24,4 M$ (méd 13,6), +4,2 ± 1,6 M$ vs lot 133. Express et saison restent à mesurer.

- **135** : fondamental, incidents ×1,35 en fréquence et ×1,4 en coût, commission +3 pts. Mesure (180 parties normales) :
  79 % · 26,2 M$ (méd 14,9), +1,8 ± 0,4 M$ vs lot 134 ; score entre quant (25,6) et flux (30,1), survie encore au-dessus du
  quant (76 %). Variante incidents ×1,5 / coût ×2,0 : 79 % · 25,7 — les incidents ne font pas baisser sa survie.
  Express (lot 134, 180 parties) : survie 92 / 82 / 82 %, scores 12,1 / 13,5 / 18,0 M$ ; quant 82 %, fondamental 90 %, flux 83 %.

- **136** : fondamental sans bonus de capital de départ, coûts ×1,08, commission +4 pts. 180 parties normales : capital à 0
  seul 78 % · 26,7 M$ ; avec coûts ×1,08 et +4 pts 76 % · 27,8 M$ (méd 14,2). Score entre quant et flux, survie au niveau
  du quant.

- **137** : rubans des concurrents — `S.xRiv` appliqué à partir de l'instant du choc (`S.xRivT`, `S.xRivQ`) et non plus
  seulement à la clôture ; micro-anecdotes dans les rôles de Tuco, Winnie, Sœur Marie-Alpha, Onésime ; budget total du
  trimestre dans le bouton « Valider le budget » ; coût des ordres en blanc gras sur l'écran du desk.
  Campagne finale (lots 133–136) : normal 81 / 70 / 64 %, express 92 / 82 / 82 %, saison 82 / 70 / 72 % ; équilibre gelé
  (choix d'Antoine), y compris le flux en saison (78 % · 54,2 M$).

- **138** : audit des 88 rumeurs (une incohérence : relèvement surprise de la BCE affiché « liquidité en hausse », corrigé) ;
  six anecdotes d'exécution nouvelles (Tuco ×2, Winnie ×2, Sœur Marie-Alpha, Onésime) reprenant leurs micro-anecdotes.

- **139** : débriefing « ce qu'on en dit » : deux variantes de plus par palier (investisseurs ton et performance, comité) ;
  six anecdotes d'exécution (Dwight, Ingrid, Boris ×2, Jean-Kevin ×2). TRADER_EXEC : 34 anecdotes.

- **140** : six anecdotes du back office (Josiane ×2, Gontran, Mireille, Tatillon ×2), dans TRADER_EXEC (40 au total).
- **141** : six anecdotes de milieu de trimestre (TRADER_MID, 51 au total : Ingrid, Dwight, Tuco, Winnie, Sœur Marie-Alpha, Onésime).
- **142** : fin de partie — trois variantes par verdict (`vp`, tirage déterministe sur la graine et le trimestre).

- **143** : graphique de performance — le cumul comptait deux fois le trimestre sur l'écran de résultat (P&L vivant ajouté
  au trimestre clos) ; drapeau `S.qClosed`.
- **144** : bonus d'équipe — multiplicateur direct sur tous les coûts d'exécution (`BONFX.c` : 1,10 / 1,05 / 1,00 / 0,94 / 0,90) ;
  l'ancien effet était bloqué à ×1,00 dès que le cran de salle de marché valait ×1,00.
- **145** : objectif du trimestre = 3 % × `goalK()` (0,80 à 1,25 selon la norme du vecteur factoriel du trimestre) ;
  annonces au même prorata.
- **146** : en-têtes de tableaux et titres de blocs plus visibles.
- **147** : « doubler vos lignes de levier » : effets écrits dans les boutons.
- **148** : marge utilisée affichée en permanence sous le libellé « risque » de la carte du bandeau.

- **149** : « L'inspecteur » et « La commandante » retirés (Firmin Tatillon, Solange Pare-Feu) ; prêts à effet de levier :
  20 % de risque de perdre 21 %.

- **150** : écran des annonces — objectif et promesses × `goalK()` (l'objectif ajusté au marché du lot 145).
- **151** : mi-parcours et résultat — la performance du trimestre défile avec le tracé (`.cntq`, `data-q0`, `theatre`).

- **152** : « L'essentiel » — lignes dépêches et tuyaux, incidents, frais du fonds sous le gain brut des positions.
- **153** : coûts des taux et de l'AUD réalistes en demi-fourchette / vol : Bund 0,35 / 0,30 (au niveau du T-Note), Gilt
  0,55 / 0,50, OAT 0,60 / 0,55, JGB 0,60 / 0,60, AUD 0,75 / 0,65 ; l'ordre des coûts suit l'ordre d'ouverture (rk) dans chaque
  classe. Prochain chantier : concurrents à book réel (voie intermédiaire), en plusieurs lots.

- **154** : concurrents à book réel (1/4) — `rivBookQ` (paris factoriels projetés sur les marchés, à leur vol × montée en
  charge `RIVB.ramp` 0,6 / 0,8 / 1), rendement = Σ poids × `S.rBase` (les vrais marchés du trimestre) × `RIVB.k` par style
  (quant 0,65), coût de rotation `rivTurn` (barème du joueur, salle ×0,75), bruit propre ×0,35. Rendements trimestriels
  (14 parties, 97 trimestres par style) — ancien : fondamental 6,2 % ± 18,8, quant 6,3 ± 7,9, flux 5,0 ± 15,5 ; nouveau :
  6,9 ± 20,0, 5,5 ± 8,5, 6,3 ± 15,2. Reste : dépêches (2/4), trésorerie de départ (3/4), équilibrage (4/4).

- **155** : objectif bonus (objectif de place) rappelé en tête de l'écran du desk.
- **156** : concurrents à book réel (2/4) — dépêches : `rivEvHit` (moitié immédiate + suite × réaction de style `RIVEV` :
  flux ×1,5, fondamental ×1,5 une fois sur deux, quant ×1), même issue que le joueur ; chocs datés `S.xRivL` / `addXRiv` /
  `rivXAt` (rubans à l'instant du choc), `S.xRiv` = somme pour la clôture. Rendements trimestriels (14 parties) :
  fondamental 6,5 % ± 20,8, quant 5,5 ± 10,2, flux 5,6 ± 17,1.

- **157** : concurrents (3/4) — pool `RIVPOOL` (6 fonds parodiques par style) et `RIVBOSS` (18 gérants), tirés en début de
  partie (`rivDraw`, validés par Antoine) ; trésorerie de départ `RIVSEED` 0,5 M$ ; trésorerie négative à la clôture →
  `rivReplace` : fonds du même style tiré dans le pool, nouveau gérant, part de zéro, montée en charge depuis `rv.q0` ;
  annonce au débriefing. Bogue corrigé : la trésorerie d'un concurrent était remise à zéro à sa première clôture.
  Test trésorerie de départ (12 parties, 36 concurrents) : 0,5 M$ → 6 faillites ; 1 M$ → 1 ; 1,5 et 3 M$ → 0. Retenu 0,5 M$.

- **158** : taux de bonus d'équipe — chaque cran affiche le multiplicateur du seul bonus.

- **159** : équipes ×0,90 (`BUDK`, ×0,80 avant) et commission du fondamental +3 pts (+4). Campagne (270 parties normales,
  graines 10001–10030) : lot 158 80 % · 39,6 M$ (facile 88, moyen 82, difficile 70 ; quant 87, fondamental 82, flux 71) →
  lot 159 75 % · 36,8 M$ (83 / 79 / 62 ; 80 / 78 / 67 ; flux le plus payant 41,5). Δ apparié −2,8 ± 1,9 M$. Moyen encore haut.

- **160** : moyen, équipe ×1,10 ; « fonds plein » affiché quand la capacité bloque une souscription (souscriptions nulles
  à 2 × `capSoftNav()`, 300 M$ en moyen) ; souscription d'office de la Couronne soumise à la capacité. Campagne (270 parties
  normales) : 74 % · 35,0 M$ ; facile 84, moyen 76, difficile 62 % ; quant 78, fondamental 80, flux 64 %.

- **161** : plus de plafond de capacité (`capStress()` = 0 : impact en racine carrée seulement, souscriptions libres) ; moyen
  équipe ×1,20 ; fondamental coûts ×1,15. Campagne (270 normales) : 73 % · 42,5 M$ ; facile 83, moyen 77, difficile 60 % ;
  quant 79 · 43,1, fondamental 77 · 37,8, flux 64 · 46,6. Encours final moyen 398 M$, max 4,7 Md$. Moyen insensible au coût
  d'équipe (79 → 76 → 77 %).

- **162** : moyen sans capital de départ (bonus de style seul), équipe ×1,10. Campagne (270 normales, graines 10001–10030) :
  73 % · 39,7 M$ ; facile 83, moyen 74, difficile 60 % ; quant 79 · 39,8, fondamental 76 · 33,5, flux 63 · 45,7.
  Moyen par style : quant 80, fondamental 83, flux 60 % (± 7 pts par case).

- **163** : objectif du trimestre et objectif bonus en haut de la page du book ; textes « book reconduit » corrigés (il repart
  à plat chaque trimestre) ; « dollar » → « liquidité » dans l'aide des sources.
- **164** : chance de tenir chaque annonce affichée à tous les niveaux ; événement du conseil « Vos investisseurs veulent
  remettre au pot » (+12 % au prorata) à la place de l'entrée de la Couronne.
- **165** : charges des taux européens (proposition d'Antoine, un cran = 0,20, affichage C/I/L/A) — Bund −1 −3 0 −2,
  Gilt −2 −2 +1 −2, OAT −1 −3 −1 +1.

- **166** : un seul écran d'ouverture (« Le trimestre N commence ») ; lignes animées (`phase`, `evshow` décalé).
- **167** : dépêches d'institutions — icône selon le type (`EVICO`, `evIco`) au lieu d'un visage ; les personnes gardent leur portrait.
- **168** : VIX — portage du vendeur dans l'attendu selon l'appétit estimé (`vixCarry` : nul à −1,5 σ) ; le réalisé dépendait
  déjà du régime (crise ×−2,2, récession ×−0,9).
- **169** : Bund liquidité −1 (aucune charge nulle).
- **170** : tableau des investisseurs, ligne Total.
- **171** : tableau des concurrents, votre fonds a toujours ses lignes « événements extrêmes » et « accidents de levier ».

- **172** : retouches après la campagne de contrôle du lot 171 (270 parties + 180 graines neuves : quant 74 / fondamental 74 /
  flux 76 %, difficile 67 %) — flux, coût des incidents ×2,8 (×2,2) ; difficile, équipe ×1,75 (×1,60). Lot 171 → lot 173
  (270 parties, graines 10001–10030) : 75 → 74 % ; facile 86 → 87, moyen 73 → 73, difficile 67 → 62 ; quant 74 → 74,
  fondamental 74 → 77, flux 77 → 71. Δ apparié −1,4 ± 0,9 M$. Le quant n'est plus le plus sûr (74 contre 77 pour le fondamental).
- **173** : budget du back office — avec un carton rouge le comité interdit de descendre sous Tatillon ; les crans du bas
  affichaient « hors trésorerie », ils disent maintenant « interdit : carton rouge » et le paragraphe l'explique.

- **174** : quant, capital de départ 1 M$ (`STYSEED`, 0,4 avant). 90 parties de quant sur les graines 10001–10030 : 0,4 M$ → 74 % ;
  0,7 M$ → 76 % ; 1,0 M$ → 83 % (facile 90, moyen 83, difficile 77). Ensemble reconstitué : 77 % · 45,6 M$ ; quant 83,
  fondamental 77, flux 71 ; facile 88, moyen 77, difficile 67.

- **Confirmation du lot 174** (180 parties, graines neuves 10031–10050) : 74 % · 22,5 M$ ; facile 82, moyen 78, difficile 62 ;
  quant 78, fondamental 72, flux 72. Cumul avec les graines 10001–10030 (240 parties de quant et de chaque style) : quant ≈ 81 %,
  fondamental ≈ 75 %, flux ≈ 71 % ; facile ≈ 86 %, moyen ≈ 77 %, difficile ≈ 65 %. Équilibre gelé (lots 172–174). Hors
  périmètre, laissés tels quels à la demande d'Antoine : Gilt +1 appétit, tracé de mi-parcours, couverture forcée des anecdotes,
  express et saison remesurés.

### Après les lots 102–110
- Survie par difficulté à l'ordre voulu (lot 113) ; quant encore pas le plus solide ; score du difficile ≤ moyen.
- Pertes immédiates jusqu'à 60 % sur certains événements extrêmes pour le bot (sécheresse, short squeeze) : héritage du
  lot 101 (amplification de foule), à vérifier.
- Qualificatifs de trimestre : parlent encore du « dollar » (exact, mais pas du vocabulaire « liquidité »).
- Une autre session a travaillé dans le même conteneur (lot 105 concurrent, fichiers `eq*`, `v*`) : toujours vérifier
  `git fetch` et reconstruire depuis `origin/main` avant de pousser.

### Anciennes notes (lots 102–104)
- Survie du quant (63 % normal, 33 % difficile) contre 80–90 % pour les deux autres styles.
- Normal à 76 % de survie pour une cible de 70 % (±4,5 pts à 90 parties) : à confirmer sur plus de parties.
- Le bot ne négocie jamais de limite ni n'active la gate : leur valeur n'est pas mesurée.
- « Risque du book » (`pct(RS.total)`) et la limite du comité (`pvol`) ne sont pas la même mesure : à harmoniser.

### Ensuite
- Campagne de référence (voir Calibration).
- Hauts faits jamais atteints par le bot faute de jouer ces choix (budgets renforcés, conviction forte,
  prophétie, book mono-classe) : vérifiables seulement à la main ou avec un bot dédié.
- Production de texte : objectif de 200 anecdotes d'exécution et 300 dépêches, textes de débriefing.
