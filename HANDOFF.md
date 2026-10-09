# Le Book — note de reprise (état au lot 212, bot 211)

Jeu de gérant de hedge fund global macro, en français. Fichier unique `index.html` (~830 ko), publié sur GitHub Pages :
https://adereuddre-tech.github.io/le-book/ — dépôt `adereuddre-tech/le-book`, branche `main`. **Dernier lot publié : 274.**

Historique détaillé : `docs/HANDOFF_archive_lot90.md` (lots 1–90) et `docs/HANDOFF_archive_lot192.md` (lots 76–192, mesures,
architecture détaillée, invariants d'origine). Cette note-ci fait foi ; l'archive sert à retrouver le *pourquoi* d'un réglage.

---

## 1. Règles d'Antoine (à respecter)

- Réponses **en français**, **brèves** : ce qui a changé, les chiffres clés, ce qui reste ouvert. Pas de récapitulatif détaillé.
- **Consignes fermées** (« fais X, Y, Z, publie ») : les exécuter sans proposer d'options. Question de conception ouverte : la
  poser **avant** de coder. Quand Antoine demande une « discussion », donner un avis argumenté et une proposition.
- **Découper en lots** : un lot = un sujet = un patch = un commit. Antoine dit souvent « découpe en lots pour ne pas être
  interrompu » : faire peu de choses par appel d'outil, publier au fil de l'eau.
- **Patchs Python ciblés** (`patches/lotNNN/p1.py`) avec `rep(old,new,k)` qui *assert* le nombre d'occurrences ; jamais de
  réécriture du fichier. Chaque patch commence par un commentaire qui dit le constat mesuré et le changement.
- **Tests avant publication** : quelques parties jsdom (`tools/play.js`), régression de 18 parties (`tools/reg.sh`, 0 erreur,
  0 blocage, 0 écart exigés), reprise à froid (`play.js --resume N`).
- **Campagnes** seulement quand l'équilibre change. Lots d'affichage : régression seule.
- **Captures** : au plus une par lot, seulement si l'affichage change (en pratique : aucune, Antoine vérifie en ligne).
- **Publication** : `git push` avec un jeton fine-grained (Contents R/W) fourni par Antoine en début de session. Il circule en
  clair : rappeler à Antoine de le révoquer. Ne jamais l'écrire dans le dépôt.
- **Anciens points mis de côté sur décision d'Antoine — ne rien appliquer sans nouvelle demande** : Gilt « exposition
  croissance » (+1 appétit), tracé complet du ruban de mi-parcours, couverture forcée des anecdotes, remesure express / saison,
  actions du « pink sheet » (refusées : aucun prime broker ne les prend en gage).

## 2. Méthode et outils

### Cycle d'un lot
```
git fetch && git status                      # vérifier qu'aucune autre session n'a poussé ni modifié index.html
python3 patches/lotNNN/p1.py                 # applique sur index.html
node tools/play.js index.html 3 --dur normal --clicks     # 2-3 parties ; nerr=0 et bad=0 exigés
cp index.html /tmp/LNNN.html && bash tools/reg.sh /tmp/LNNN.html /tmp/reg.txt && python3 tools/summ.py /tmp/reg.txt
node tools/play.js /tmp/LNNN.html 4 --dur normal --resume 3              # reprise à froid
# vérification : reconstruire depuis origin/main + patches du lot et comparer octet par octet avec index.html (cmp)
# HANDOFF : ajouter une ligne dans la section 6 ; commit « Lot NNN : … » ; git push
```
Plusieurs lots dans un même tour : les appliquer tous pour tester, puis `git checkout index.html` et les rejouer un par un en
committant chacun (le dernier doit redonner exactement le fichier testé).

### Outils (`tools/`, jsdom : `cd tools && npm i jsdom`, puis `ln -s tools/node_modules node_modules` à la racine)
- `play.js <fichier> <graine> [--prof syst|fonda|flux] [--size small|mid|mega] [--dur express|normal|saison] [--resume N]
  [--clicks]` : partie complète, compte erreurs (`nerr`) et écarts jauges affichées / appliquées (`bad`). `--clicks` active la
  gate et négocie une limite quand c'est possible.
- `reg.sh <fichier> <sortie>` + `summ.py <sortie>` : régression 18 parties (3 styles × prudent/actif × 3 graines).
- `bot.js` — `playGame({file,seed,prof,size,dur,bud,bon,reserve,lim,av,probe,collect})` : bot « intelligent » des campagnes.
  `bon` = cran de bonus (index), `reserve` (défaut 0,35) = part de trésorerie gardée hors budget, `lim` = respecte la limite de
  risque, `bud` = [cran front, cran back]. Il prend toujours les tuyaux du prime broker. `collect` = expression évaluée en fin.
- `runner.js plan.json sortie.jsonl N` : joue N parties d'un plan (liste d'options), reprend là où il s'est arrêté.

### Campagnes : pièges connus
- **Limite de 300 s par commande** : lancer `runner.js` au premier plan, par tranches de ≤ 55 parties normales
  (≈ 4 s/partie), `timeout 240`. Les processus détachés (`setsid nohup …`) sont tués par l'environnement.
- **Une tranche coupée par la limite peut écrire des lignes en double** : dédoublonner (`dict.fromkeys(lignes)`) avant de dépouiller.
- **Fichiers de résultats** : toujours un nom neuf (`zzXXX_$(date +%s).jsonl`), le conteneur a contenu des fichiers d'une autre
  session ; un fichier existant fausse la reprise du runner.
- **Copie figée** : jouer une copie de `index.html` (`/home/claude/LNNN.html`), jamais le fichier en cours d'édition.
- **Comparaisons** : seulement appariées (mêmes graines). Le niveau absolu varie énormément d'une série de graines à l'autre
  (score moyen 22 M$ sur les graines 10031–10050, 45 M$ sur 10001–10030).
- Plan de référence : graines 10001–10030 × 3 difficultés × 3 styles, durée normale, `bon` au cran par défaut (270 parties ;
  ≈ 20 min en 5 tranches). Confirmation : graines 10031–10050 (180 parties). Écart type ≈ 5 pts de survie par ligne.
- **Autre session** : à plusieurs reprises une autre session Claude a travaillé dans le même conteneur et le même dépôt (lots
  concurrents, `index.html` modifié hors patch). Toujours `git fetch`, regarder `git status` et `git diff`, et ne pousser qu'un
  fichier reconstructible depuis `origin/main` + patches.

### Pièges de patch
- Les ancres sont exactes au caractère (indentation réelle d'un ou deux blancs, `\'` dans le JS = une barre oblique).
- Un `rep` qui échoue au milieu d'un patch n'écrit rien : corriger l'ancre et rejouer depuis `git checkout index.html`.
- Les textes recalculés au chargement (anecdotes) se modifient dans le bloc de normalisation, pas dans les tableaux.

## 3. Le jeu aujourd'hui

### Choix de départ
Style (`syst` quant · `fonda` fondamental · `flux`), difficulté (`small` facile · `mid` moyen · `mega` difficile), durée
(express 4 / normal 8 / saison 12 trimestres). Encours de départ 100 M$ (`S.aum0`). Univers fixe (`ext`, 25 marchés).

### Déroulé d'un trimestre
Ouverture (`phaseDesk`, un seul écran : objectif du trimestre, objectif bonus, liquidité, prime broker, signaux) → budget
(`screenBudget`) → book (`screenPlay`) → annonce (`screenComm`) → tuyau du prime broker (`screenTip`, 35 % des trimestres) →
exécution (`screenExec`, anecdote) → événements (`stepEvents` : dépêches, mi-parcours, incidents, extrêmes, appels de marge,
stop) → clôture (`resolveQuarter`) → résultat et débriefing (`screenDebrief`).

### Économie de la société de gestion (le score)
- Score = trésorerie du gérant `mgrNet()` (commissions − tout ce qu'il paie ± co-investissement). `mgrCash()` = disponible.
- **Fin de partie** : trésorerie négative **à la clôture** → dépôt de bilan (`S.cashNeg>=1`, `S.over='cash'`) ; encours < 1 %
  de l'encours de départ → `S.over='nav'`. Plus de seuil d'encours ni de repli de 50 %.
- **Trésorerie négative permise en cours de trimestre pour les transactions** (ordres, choix d'événements, tuyaux, incidents,
  accidents ; lot 178). **Interdite pour les salaires** : budget, bonus d'équipe, départs (gardes `ok()` du budget).
- Capital de départ `S.mgrSeed` = difficulté (`SIZES.seed` : 0,45 / 0 / 0 M$) + style (`STYSEED` : quant 1 M$, autres 0).
- Commissions : gestion 50 pb/trimestre (`VOL().mgmt`), performance `perfFee()` = difficulté (15 / 20 / 30 %) + style
  (`STYPERF` : fondamental +3 pts, flux +5 pts, « l'aura du prophète »).
- **Coûts d'équipe fixes** (lot 176) : `budNav()` = encours de départ × `SIZE().costM` (0,85 / 1,10 / 1,75) ×
  `STYCOST[style]` (0,85 / 1 / 1,50) × `BUDK` (0,90). Ne bougent plus avec l'encours.
- Front office `FOP` (crans cumulés, pb de 100 M$) : Jean-Kevin 0, Dwight 10, Ingrid 25, Boris 45, Tuco 70, Winnie 100,
  Sœur Marie-Alpha 150, Onésime 250 (8e cran normal depuis le lot 197). Back office `BOP` : loyer 5, Gontran 10, Josiane 15, Tatillon 30, Mireille 60,
  Solange 100. `syncBud()` : `exec=res=ret=min(fo,7)`, `risk=BOMAP[bo]`.
- Départ d'un salarié : un demi-trimestre de son salaire (`sevRaw`). Trader débauché : parti pour de bon (`S.gones`),
  « Faire revenir » = 1,5 trimestre de salaire (`cntCost`).
- **Bonus d'équipe** (lots 179–180, 187) : taux = `bonBase()` (10 × coût sur 100 M$ du cran de front office atteint, ex.
  Winnie 10 %, Onésime 25 %) + `BONOFF` (0 / 2,5 / 5 / 10 / 15 pts) ; défaut = minimum (`MOT.i0=0`). Effet par cran
  `BONFX` : coûts d'exécution ×1,20 → ×0,80 (fourchette et impact), débauchage 50 % → 12 %, ×1,5 le trimestre d'une baisse.
  Versé à l'ouverture sur la commission de performance du trimestre écoulé.
- Co-investissement (`COINVS`, défaut 25 %) : bloqué à l'ouverture, rendu avec son résultat à la clôture.

### Coûts d'exécution
`tcost` : (demi-fourchette `s` + impact `c`·√taille) × `TCK`(3) × `execMot()` (= `EXECM[cran]` × bonus) × liquidité ×
taux × style (`tcMult` : quant 0,72, fondamental 1,15, flux 1,00) ; ×4 sans trader dans la classe (`NOTRD`). Plus de
plafond de capacité (`capStress()=0`). Suivre une dépêche : ×2 ; pendant un événement extrême : ×5 (lot 188).

### Investisseurs (`INVR`, `invClose`)
Cinq lignes : Cheminots (régularité : 2 trimestres de même signe ; avis retiré dès un trimestre positif), Nordhavn
(objectif annoncé tenu / manqué), Vandermeer (absolu : < −3 % / > +4 %), Albatros (relatif à la moyenne des concurrents,
±3 pts), Couronne du Liquidistan (entre par le trophée « souv » ; souscrit d'office 5–12,5 %, suit le plus sévère).
Montants divisés par 2 au lot 177 : rachat = `out` × 2 × (1 − confiance/100) (out 0,225 / 0,175 / 0,275 / 0,25 / 0,275),
souscription = `inn` × confiance/50. Préavis d'un trimestre, gate (> 15 % de l'encours en avis), ligne Total.

### Comité et risque
Limites affichées (`LIM`) : risque ex ante 15 %/trim. (rouge ×1,5), stop −10 %/trim. (`screenStopQ`), concentration 70 % ;
cadre flottant `cardWarn()` dès qu'un carton se prépare. Carton rouge : contraintes (`redDraw2`), dont back office bloqué
sous Tatillon (libellé « interdit : carton rouge »). Appel de marge contrôlé après chaque événement.

### Événements
- Dépêches `MACROEV` (≈ 292) : deux options (suivre / ne pas réagir), suite poursuite (p 0,40–0,90) ou retournement ; tout
  ce qui est affiché est appliqué (sonde `bad`). Plancher : si l'effet net sur le fonds est ≥ 0, la confiance ne baisse pas.
  Pré-annonces : vecteur factoriel projeté, sauf `EVFV` (banques centrales, défauts et faillites au sens économique).
- **Événements extrêmes** (`STRESS`, `STRESSK` 0,32) : issue imprévisible (p 0,35–0,65), suivi ×5, pas d'ajustement gratuit ;
  annoncés parfois (`xHintDraw` : rumeur, source vérifiée du fondamental, modèle du quant, intuition du flux) ; les
  concurrents encaissent le vrai P&L sur leur book.
- Accidents de levier (`TAILEV`), incidents (`INCIDENTS`, gravité `incSev` par style : fondamental ×1,4, flux ×2,8 ;
  fréquence `incMult` 0,60 / 1,35 / 1,70), conseil (`BOARDEV`), parties prenantes (`STAKE`).
- **Anecdotes d'exécution** (`TRADER_EXEC`, 40) : depuis le lot 183, l'option qui allège vos ordres rapporte un **gain fixe**
  à la société de gestion, `gainBp` = 40 × la baisse d'origine (pb de 100 M$, `EXGAIN`) ; le risque pour le fonds reste
  d'origine ; pari raté = −½ gain. Textes recalculés au chargement (bloc « lot 183 » avant les limites du comité).
  Anecdotes de milieu de trimestre `TRADER_MID` (≈ 51).
- Tuyaux du prime broker (`TIPS`, 7 affaires à espérance positive) ; pris par un concurrent si vous passez.

### Concurrents (lots 154–157)
Trois fonds tirés en début de partie dans `RIVPOOL` (6 parodies par style) avec un gérant de `RIVBOSS` (18 parodies) —
liste validée par Antoine. Book réel (`rivBookQ` : paris factoriels projetés sur les marchés, montée en charge 60 / 80 /
100 %), rendement = Σ poids × `S.rBase` (les vrais marchés) × `RIVB.k` (quant 0,65), coûts de rotation (`rivTurn`),
dépêches (`rivEvHit`, réaction `RIVEV`), extrêmes (`xRivHit`), tuyaux. Chocs datés (`S.xRivL`) visibles sur les rubans.
Trésorerie de départ `RIVSEED` 0,5 M$ ; faillite → affiché « clôturé », dernier, hors rangs, puis remplacé au `planQuarter` suivant (`rivReplace`, lot 196).
Équipes à coût fixe sur l'encours de départ, facture d'ordres (16 pb) sur l'encours du moment (`rivalCostAmt`, lot 193).

### Divers
Objectif du trimestre = 3 % × `goalK()` (0,80–1,25 selon l'intensité des facteurs) ; annonces au même prorata (+5/−5,
+15/−8, +30/−10 en confiance). Facteur n° 2 affiché « Liquidité » = −dollar (`FSG`). VIX : portage du vendeur selon l'appétit
estimé (`vixCarry`). Tableau des concurrents : lignes « dépêches et chocs », événements extrêmes et accidents de levier
pour votre fonds.

## 4. Invariants à ne pas casser
0. **Convention des facteurs** : tout ce qui est *affiché* (exposition d'un marché, lecture, tuiles) passe par `FSG` (liquidité = −dollar) ; les calculs internes (`expRet`, `S.factEst`, `x.b`) restent en convention brute. Un affichage qui lit `x.b` ou `S.factEst` sans `FSG` est un bug.
1. `setUniverse` avant toute restauration de `b` dans `loadGame` ; un échec de reprise n'appelle pas `clearSave()`.
2. Effets citant un symbole : `IDX[sym]` gardé. Ne jamais indexer un marché par position (`d.ord` fait partie de la sauvegarde).
3. Dépêches : montants et jauges affichés = appliqués (`evPlans` / `resolveEvent`, sonde `bad`).
4. Le book repart à plat chaque trimestre (`S.k`, `S.k0` remis à zéro).
5. Risque calculé en annuel, affiché en trimestriel (`RQ()` ou `*50`). Pourcentages à une décimale.
6. Charges factorielles : Σb² ≤ 0,92 (sinon `normB` rescale) ; crans affichés : |b| < 0,15 → 0, < 0,32 → 1, < 0,55 → 2.
7. À la clôture, `S.q` est déjà incrémenté quand on traite cartons, investisseurs, faillites.
8. Co-investissement rendu à chaque clôture (`S.coinvLock` = 0).
9. `pk()` : XOR final `>>>0`.
10. Effets d'événements sur le **fonds** : en fraction d'encours, jamais en montant fixe. Les gains du **gérant** (anecdotes
    lot 183) sont en pb de 100 M$ fixes, à dessein.
11. `S.phase` vaut `'open'` sur l'écran d'ouverture (sinon `cashView()` retire deux fois bonus et co-investissement).
12. Les textes de boutons recalculés (anecdotes) doivent rester cohérents avec les effets (`gainBp`, `risk`, `gamble`).

## 5. Équilibre (bot, durée normale)

Dernière mesure complète : **lot 174** (avant les lots 175–192). Cumul 420 parties (graines 10001–10050) :

| | Survie |
|---|---|
| Quant / fondamental / flux | ≈ 81 % / 75 % / 71 % |
| Facile / moyen / difficile | ≈ 86 % / 77 % / 65 % |

Cibles d'Antoine : quant le plus sûr, flux le plus risqué et le plus payant ; facile au-dessus du moyen, au-dessus du
difficile (≈ 80 / 70 / 60 %). Lot 175 : flux un peu plus risqué (≈ 67 %, mesuré sur le flux seul).

**Non mesurés depuis** — à remesurer en priorité (270 parties, plan de référence, comparé au lot 174) : coûts d'équipe fixes
(176), flux d'investisseurs ÷2 (177), trésorerie négative en séance (178), bonus minimal et défaut au minimum (179–180, 187),
extrêmes (181, 188), anecdotes à gain fixe (183), nouvelles charges des taux (184), back office plus cher (186).
Leviers éprouvés : coût d'équipe par style / difficulté (le plus efficace sur la survie), capital de départ (agit sur les
faillites du premier trimestre), commission (agit sur le score, pas sur la survie). Inefficaces sur la survie : nervosité
des investisseurs, incidents au-delà de leur niveau actuel, coût d'équipe du seul niveau moyen.

## 6. Reste à faire

1. **Équilibre** (lot 205, bot 199) : survie 77 % ; gradient de difficulté faible (80 / 79 / 73) ; le capital seul ne le crée pas. Capital et coût d'équipe testés sans effet utile (le bot s'adapte). Leviers restants : coût des incidents et accidents pour la société de gestion selon la difficulté (cause principale des faillites), rachats des investisseurs.
2. **Libellés des tuiles de facteurs** (proposé, pas demandé) : « lecture » (flèches) et « votre exposition » (chiffre) ; sur une tuile, flèches et chiffre sont deux grandeurs différentes (lecture du desk / exposition de votre book), ce qui peut sembler contradictoire (▲▲▲ avec −2).

Ensuite (idées anciennes) : anecdotes et dépêches supplémentaires, textes de débriefing.

## 7. Journal des lots 175–205
- **175** : flux, équipe ×1,50.
- **176** : coûts d'équipe figés à leur coût pour 100 M$.
- **177** : rachats et souscriptions des investisseurs ÷2.
- **178** : trésorerie négative permise pour les transactions, pas pour les salaires.
- **179** : bonus minimal = 10 × coût des traders embauchés ; crans = minimum + 0/2,5/5/10/15 pts.
- **180** : bonus par défaut au minimum ; Marie-Alpha et Onésime relèvent le minimum.
- **181** : événements extrêmes moins exploitables (amplitude ×0,8, issue imprévisible, pas d'ajustement gratuit).
- **182** : (remplacé par 183).
- **183** : anecdotes d'exécution à gain fixe pour la société de gestion, risque du fonds d'origine.
- **184** : charges T-Note, Gilt, Bund, OAT, JGB, Euro-fx (proposition d'Antoine).
- **185** : rappel d'objectif du book au niveau ajusté.
- **186** : Mireille 60 pb, Solange 100 pb.
- **187** : bonus d'équipe ×1,20 → ×0,80.
- **188** : suivre une dépêche ×2, un extrême ×5 ; concurrents au même barème.
- **189** : « dépêches et chocs » dans le tableau des concurrents, votre fonds compris.
- **190** : budget en dollars (coût supplémentaire, coût d'équipe, trois chiffres significatifs, départs justes).
- **191** : trésorerie juste sur l'écran d'ouverture (`S.phase='open'`).
- **192** : compteur du trimestre juste sur l'écran de résultat.
- **193** : concurrents à coûts d'équipe fixes (masse salariale sur l'encours de départ, facture d'ordres 16 pb sur l'encours du moment ; `rivalCostAmt`).
- **194** : écussons des fonds dans le tableau des concurrents (résultat), le vôtre compris.
- **195** : objectifs « concurrent nommé » (Citadelle, Pont-Levis, Médaillon) rattachés au concurrent du même style (`rivSty`, getters `nm`/`d`, `id` stable).
- **196** : concurrent fermé affiché, classé dernier, « clôturé » en rouge, exclu des rangs ; remplacé au début du trimestre suivant (`planQuarter`, `S.qRivIn`, annonce à l'ouverture).
- **197** : Onésime 8e cran normal (barèmes prolongés, `syncBud` jusqu'à 7, `syncBud()` au chargement), coup de pouce retiré (`ecoBoost` inerte), « Atterrissage-en-Douceur » retiré du nom.
- **198** : facteurs cohérents partout. Fenêtre d'un marché en convention d'affichage (`FSG` sur exposition et lecture : la liquidité était en dollar brut, d'où « +0,35 » contre « Liquid. −− » sur la ligne) ; flèches des tuiles, tableau « Lecture du desk » et détail de la fenêtre lisent tous `factRead()` (moyenne ×2,2 + intuition ; une flèche = 0,45).
- **199 (outil, jeu inchangé)** : bot conscient du risque de faillite (`tools/bot.js`). Trésorerie visée après book, équipe comprise : `FLOORS` quant 2 %, fondamental 2 %, flux 4 % de l'encours (budget plafonné en conséquence ; book réduit, ordres les plus chers d'abord, jamais sous la moitié). En cours de trimestre, il écarte les ordres de dépêche et les options d'accident qui mettraient la trésorerie dans le rouge. Campagne de référence (270 parties, graines 10001–10030, lot 198) : survie 47 → 76 % (quant 68 → 89, fondamental 41 → 76, flux 32 → 62 ; facile 76, moyen 77, difficile 74), gain moyen 18,3 → 17,8 M$, écart-type 52,5 → 25,1, médiane −0,1 → 9,4. Faillites restantes : surtout trimestres 1 à 3.
- **200** : anecdotes — pastille « chances de gagner NN % » sur chaque choix tiré au sort (exécution et traders), calculée sur les effets (`winP`, `winChip`) ; textes sans pourcentage chiffrés.
- **201 / 201b** : capital de départ des concurrents par difficulté (`rivSeed` : 0,25 / 1,5 / 4 M$) ; choix du cran de budget (`rivBud`) en moyen et difficile, pas en facile (équipe standard). Effet apparié sur leur rendement trimestriel : moyen +0,9 pt, difficile ≈ 0 (déjà au meilleur cran).
- **202** : Firmin Tatillon 30 → 40 pb.
- **203** : promesses — conviction forte ×2 l'objectif standard (6 %), prophétie ×3 (9 %) ; textes « Joueur de poker » et « Le prophète » réécrits.
- **204** : grand ruban du résultat piloté en JS (`opt.js` de `tapeSvg`, `.tclip`, `.tmk`, avancés par `theatre`) : le tracé du trimestre se déroule en 4 s avec le compteur, sans dépendre de SMIL.
- **205** : capital de départ du joueur : facile 1 M$, moyen 0,5 M$, difficile 0 ; style quant +0,5, flux +0,5, fondamental 0. Calibration (378 parties) : survie 86 % à 0 M$, 94 % à 1 M$, 86 % à 2,5 M$ (au-delà, le capital part en équipe et en book).
  Campagne de référence (bot 199, graines 10001–10030) lot 198 → 205 : survie 76 → 77 % (quant 89 → 86, fondamental 76 → 81, flux 62 → 66 ; facile 76 → 80, moyen 77 → 79, difficile 74 → 73), gain moyen 17,8 → 19,3 M$ (écart-type 25,1 → 29,3) ; flux 13,0 → 19,6 M$ (écart-type 36,8).
- **Calibration du coût d'équipe par difficulté (sans changement retenu)** : 240 parties, graines 20001–20010, `costM` facile ×0,85/0,70/0,55 → survie 90/90/83 % ; moyen ×1,10/1,30 → 93/90 % ; difficile ×1,75/2,10/2,50 → 83/87/90 %. Aucun effet utile : le bot ajuste son cran d'équipe à sa caisse, et en difficile une équipe plus chère le pousse vers une équipe plus petite, donc plus prudente. Le coût d'équipe, comme le capital, ne crée pas le gradient de difficulté.
- **Bot 206 (outil)** : plancher de trésorerie retiré (`FLOORK=0`), garde conservée — bot moins prudent. Calibration (285 parties, graines 20001–20008) : plancher ½ + garde 83 %, sans plancher + garde 73 %, sans garde 44–54 %.
- **207 (lot A)** : dépêches et extrêmes à 5 crans (+2, +1, 0, −1, −2 unités dans le sens du choc ; `evPlans` → `mk(a)`, champs `n`, `v0`, `v1`) ; sélecteur `.evstep`, panneau `#evpan`, bouton `#evok` ; défaut « ne pas réagir » ; le carton rouge bloque les crans qui augmentent la vol ex ante. Bot et `play.js` adaptés (bot : argmax de l'utilité sur les crans ouverts).
- **208 (lot B)** : rivalité à 5 crans (suivre, suivre ½ à mi-chemin, rien, contrer ½, contrer ; `RT`, `RP`, `.rvstep`, `#rvpan`, `#rvok`) ; écho de presse ×0,5 pour les demi-crans. Bot (utilité lue sur le panneau, coût déduit) et `play.js` adaptés.
- **209 (lot C)** : accidents de levier et appels de marge — part du book coupée sur 5 crans (0, 25, 50, 75, 100 %) + couverture (`tailOpts` : `x`, `fA/fB`, `cA/cB`, `fE`) ; 25 % = moitié pari, moitié coupe ; 75/100 % = plus d'impact (+0,1 L / +0,2 L) mais confiance −2 / 0. Défaut et minuterie : 50 %. Affichage corrigé (tenir montrait −0,3 L / −1,5 L et −1 / −8 au lieu de −0,5 L / −1,8 L et −2 / −10 appliqués ; couper −3 au lieu de −4 ; couvrir −2 au lieu de −3). `.tlstep`, `#tlpan`, `#tlok`.
- **210** : objectifs bonus réduits à un coup de pouce de début de partie — un objectif au trimestre 1, un au trimestre 2, plus rien ensuite. 13 objectifs (`qn` 1 ou 2, `pre` gain/loss/rank2) remplacent la centaine d'avant ; nouveaux compteurs `S.qReactW`, `S.qContraW` (réactions gagnantes, contres gagnants). Bonus inchangé (`b` × 0,25 × encours de départ, 2 à 3 M$).
- **211 (lot D, outil)** : bot de test — seuil de netteté par style avant de réagir à une dépêche (`THETA0` : quant 0,8, fondamental 0,4, flux 0 ; z = écart d'utilité au cran « rien » / son écart-type entre scénarios). Réactions mesurées : 22 / 29 / 64 %.
- **212 (lot E)** : concurrents face aux dépêches — règle de netteté (`rivEvHit(ev,touched,mult,SC)`) : z de la dépêche, perçu avec un bruit η selon la difficulté (`rivEta` : 1,0 / 0,6 / 0,3), réaction sur 5 crans (½ au-delà de θ, plein au-delà de 2θ, symétrique pour contrer) ; `RIVTH` quant 1,2, fondamental 0,7, flux 0,3 (recalibrés : 0,8/0,4/0 donnaient 43/68/100 % de réactions) ; ampleur `RIVAMP` ×1,25 / ×1,5 / ×1,75 dans le sens du choc. Mesure : réactions 25 / 43 / 74 % ; gain moyen par réaction 37 / 61 / 69 pb (facile / moyen / difficile), 62 / 68 / 71 % de réactions gagnantes. `RIVEV` n'est plus utilisé.
- **213** : coûts du back office en progression régulière : Loyer 5, Gontran 10, Josiane 15 → 20, Firmin 40 → 32, Mireille 60 → 55, Solange 100 (`BOP`). La campagne de référence du lot 212 a été jouée avec les anciens coûts.
- **214** : écrans d'événements — descriptif d'abord, sélecteur en dessous, puis « Valider » (dépêche, rivalité, accident) ; contres à gauche, renforcements à droite (dépêche : −2 −1 0 +1 +2 ; rivalité : − −½ 0 +½ +) ; `bkD` : rentabilité et risque sur une seule ligne. Attention : l'ordre d'affichage des `.evstep` n'est plus celui de `plan` (utiliser `data-i`).
- **215** : investisseurs — souscriptions en % de l'allocation initiale (`invBase` : part de départ × encours de départ ; Couronne : sa première ligne, `v.a0`), rachats toujours en % de la ligne actuelle.
- **216** : anecdotes et autres choix — effets trop faibles renforcés (81 choix) : effet monétaire < 5 pb doublé, 5 pb au moins ; effet sur les coûts < 10 % doublé, 10 % au moins ; textes réécrits ; `EXGAIN` 40 → 80 (une baisse de coûts de 10 % sur une anecdote d'exécution rapporte 8 pb à la société de gestion, et non 4).
- **217** : dépêches — probabilité de poursuite réelle dans [0,40 ; 0,80], lecture du desk bornée à 80 % ; seuils des concurrents recalibrés `RIVTH` 1,0 / 0,6 / 0,25.
- **218** : le Liquidistan devient le Farghestan (« famille régnante », « puissance lointaine et fortunée de l'autre rive ») ; mécanique de la Couronne vérifiée (entrée par trophée, seuils des cartons −20 %, se règle sur le plus sévère). Derniers « comité / investisseurs ±n » affichés passés en confiance : choix du conseil lus par `fxTxt`, trophée « Main chaude », rivalité « ne pas répondre », cran de risque au budget (`RISKRC × CFW`).
- **219** : marge affichée sur le panneau — étiquette propre en haut à droite de la carte rentabilité/risque (`.mgl`) ; elle débordait après « risque ».
- **220** : budget — total du trimestre = coût réel prélevé (bonus aux partants compris), en M$, en pb de l'encours et en % par an ; il mélangeait prix catalogue en pb « de 100 M$ » et montant réel (multiplicateurs difficulté × style × `BUDK`). Lignes et liste des crans en montants réels.
- **221** : probabilités en % — deals du prime broker (« avec 33 % de chances ») et accident de levier (« 50 % de chances »).
- **222** : petites dépenses de fonctionnement (≤ 30 pb : consultants, avocats, formations, heures sup, remises, petites récupérations) à la charge de la société de gestion (`e.opex`, même montant en dollars sur l'encours de départ : 5 pb = 50 k$), pastille `opxChip` ; 73 choix convertis. Restent au fonds (`e.cash`) : financement et marché (base, prime, marge, collatéral) et grosses licences ou frais de développement (> 30 pb), 48 choix.
- **223** : bonus d'équipe — coûts d'exécution ×1,35 … ×0,70 (`BONFX`), lecture des dépêches bruit ×1,25 … ×0,75 (`BONREAD`), chances des anecdotes du desk −8 … +8 pts (`BONWIN`, `pAdj`, `riskGood`, appliqué au tirage et à la pastille `winP`).
- **Campagne de référence lot 223** (bot 211 : sans plancher, garde, seuil par style ; graines 10001–10030, 264 parties) : survie 60 % (quant 78, fondamental 66, flux 35 ; facile 71, moyen 60, difficile 49), gain moyen 11,5 M$ (écart-type 24,9, médiane 2,9). Contre le lot 205 / bot 199 : survie 77 → 60 %, gain 19,5 → 11,5 M$ — effets mêlés (bot moins prudent, lots 207–223). Faillites réparties sur tous les trimestres. Le gradient de difficulté apparaît ; le flux est trop puni.
- **224** : panneau de détail à hauteur fixe ; rentabilité et risque insécables ; ordres chiffrés retirés du résultat d'une dépêche
- **225** : taux de capture des dépêches tiré au sort (±30 % autour du taux du style)
- **226** : résultat du trimestre, commentaire cohérent avec le résultat
- **227** : règles des investisseurs dans le détail « Montants, préavis et confiance »
- **228** : page desk, objectif du trimestre = objectif bonus ; objectif en % et explications des investisseurs retirés
- **229** : marge sur la ligne d'intitulé de la tuile Trésorerie
- **230** : idées de trade des traders à 55–70 % ; textes à la chance effective ; conversion des baisses de coûts corrigée
- **231** : flux, équipe ×1,50 → ×1,35
- **232** : impact de marché en puissance 0,8 (`IMPEXP`, `impScale()`) : le terme d'impact de `tcost` est multiplié par (encours / encours de départ)^0,3 ; rien ne change au départ. Mesuré sur la facture d'un ±1 unité sur 25 marchés : 104 pb à l'encours de départ ; à 10× l'encours 122 pb avant, 147 pb après ; à 20× 133 → 186 pb. L'impact ne pèse que 7 % de la facture au départ (la fourchette domine) : le frein est modéré. Concurrents au même frein (`rivTurn`, `rivalCostAmt`). Plafond d'impact par exécution (`IMPMAX`, 1,5 % de l'encours) retiré.
- **234** : frein sur la facture entière, (encours / départ)^0,25 — jamais publié seul, remplacé par le 235.
- **235** : frein à la croissance retenu par Antoine. Formule initiale d'impact rétablie (racine carrée ; la puissance 0,8 du lot 232 pénalisait d'abord les marchés liquides, où une unité de risque pèse un gros notionnel) ; impact ×1,5 dès le départ (`IMPC`) ; facture entière × (encours / encours de départ)^0,35 au-dessus du départ (`BRK`, `brake(A)`) : ×1,76 à 500 M$, ×2,85 à 2 Md$, identique pour tous les marchés (ordre des coûts conservé). Concurrents freinés selon leur propre encours (`rivTurn(w,w0,A)`, facture d'ordres type). Plafond d'impact de 1,5 % par exécution toujours retiré (lot 232). Coût d'un ordre +1 unité : ×1,03 à 100 M$, ×1,9 à 500 M$, ×3,3 à 2 Md$.
- **236** : frein à la croissance retenu : facture entière × (encours / 200 M$)^0,35 au-delà de 200 M$ (`BRK0=0.2`, seuil absolu), sans multiplicateur d'impact (`IMPC=1`). ×1,38 à 500 M$, ×1,76 à 1 Md$, ×2,24 à 2 Md$. Le lot 235 (départ à l'encours de départ, ×1,5) freinait dès 150–300 M$ : survie 65 → 52 %, gain −45 % sur 12 trimestres.
- **237** : confiance de clôture jugée sur le trimestre tout compris (`qTotal`, dépêches incluses), moins ce que les dépêches ont déjà fait bouger en séance (`S.qEvLp` : part P&L immédiate `S.evImmP` + suite, sans la nervosité) ; écart à la médiane sur `qTotal`. Avant : performance des positions hors dépêches, d'où 91 → 100 à −60 % (dépêches −89 M$, positions +17 M$).
- **238** : fin de trimestre en pages : performance du fonds → gate (si rachats en attente) → trésorerie du gérant (`tresSel`) → bonus d'équipe. `PGS`, `showPg`, `wire`, `finish` dans `screenDebrief` ; chaque page a son `#nx`.
- **239** : négociation d'une limite au début du trimestre, en bas du bloc risque de la page du book (`limNegBlock`, `limNegOk` : phase book, pas de carton à la dernière clôture, pas deux trimestres de suite) ; confiance −3 au choix, remboursée si annulée avant validation ; clic délégué sur `.lmp`.
- **240** : co-investissement sur une page dédiée après la validation du book (`screenCoinv`, reprise comprise) : rentabilité estimée, risque, trésorerie après ordres ; placement `coinvPct() × trésorerie` à ce moment (plus à l'ouverture) ; rien au premier trimestre ; `coSel` et `coPend` retirés de la fin de trimestre.
- **241** : bilan d'une anecdote d'exécution en trois blocs chiffrés reliés au choix : société de gestion (facture standard → coûts ×m → ajustements → facture ; rabais ou dépense du choix ; net), fonds (impact standard 2,4 × facture → effet de la manière d'exécuter → aléa avec probabilité et issue → effet direct ; total), confiance (manière d'exécuter, effet du choix, résultat ; valeurs de `gauge()` telles qu'appliquées). Impact de marché expliqué (dépliant). « Le marché n'a pas bougé » → « Le risque annoncé ne s'est pas produit ».
- **242** : dépenses et recettes des anecdotes pour la société de gestion : 8 + 9 × √(montant d'origine en pb, avant le lot 216), en pb de l'encours de départ (110 à 570 k$ sur 100 M$ ; avant, 50 k$ presque partout). Valeurs d'origine dans `patches/lot242/orig215.json`.
- **243** : commentaire du résultat trimestriel (`qVerb`) : 6 à 8 formulations par situation, tirées par trimestre (`pk`), jamais deux fois de suite (`S.qVerbPrev`).
- **244** : réaction aux dépêches — dock collé en bas de l'écran (`.evdock`, sticky) : résumé du cran en trois lignes (ordres et coût ; poursuite et retournement : probabilité, P&L, confiance ; rentabilité et risque), crans et « Valider » ; texte complet et ordres au-dessus (`#evdet`). Rivalité et accident gardent l'ancien panneau.
- **245** : `#evdet` en grille : le détail de chaque cran est empilé (`.pcell`, un seul visible), hauteur constante ; « Ne pas réagir » affiche « Aucun ordre : le book reste inchangé. »
- **246** : fin de trimestre — les pages Gate, Trésorerie et Bonus d'équipe ne sont plus retenues par `.thold` (3 s) : affichage immédiat.
- **247** : collatéral — 10 placements renommés (T-bills, monétaire prime, repo tripartite, AAA de CLO, prêt de titres réinvesti, dette émergente locale, HY court, prêts cov-lite, AT1, dollar synthétique crypto) ; profils variés (fréquent/léger, rare/lourd) ; dispersion du surcroît `v` par placement (colY) ; net y−p·l relevé (0,26 → 1,8 %/trim.), plus aucun placement à espérance négative.
- **248** : collatéral — écarts-types trimestriels l·√(p(1−p)) échelonnés 0 / 0,5 / 1 / 1,5 / 2 / 2,5 / 3 / 4 / 5 / 6 %, placements classés par écart-type ; probabilités inchangées, pertes recalculées (max 18,4 % pour AT1) ; Sharpe constant 0,30 par trimestre (net = 0,3 σ) ; `colY` = y ± 10 % du net (le net reste croissant avec le risque dans 99 % des trimestres, toujours positif). Champ `v` supprimé.
- **249** : collatéral — noms en anglais (T-bills, Commercial paper, Tri-party repo, AAA CLO, Sec-lending cash reinvestment, Local-currency EM debt, Short-duration HY, Cov-lite leveraged loans, Bank AT1 CoCos, Synthetic dollar) ; σ de 0 à 4,5 % par pas de 0,5 ; pertes des trois derniers 8 / 9 / 10 %, probabilités déduites (26 / 27 / 28 %) ; Sharpe 0,35 ; `colY` ± 8 % du net (ordre croissant sur toute l'échelle dans 95 % des trimestres).
- **250** : collatéral — cov-lite p 40 %, perte 7,1 % ; AT1 perte 18 %, p 5,2 % (σ, Sharpe 0,35 et variation inchangés).
- **251** : « Le book que le desk/modèle construirait » (`#factest`, recoBook, « Appliquer ce book ») affiché pour tous les styles en niveau facile (S.size==='small'), retiré en moyen et difficile, quant compris. Pouvoir propre du quant renommé « modèle de risque » (fiche, styTable) ; ligne ajoutée à la carte Facile. Le bot quant continue d'appeler recoBook directement : la campagne ne mesure pas cette perte pour un joueur humain.
- **252** : veille des extrêmes (`xWatch`, `xHintDraw`) — couvre STRESS et dépêches x:1 (tirage déplacé après XPROB). s = base style (quant 0,27 · fonda 0,175 · flux 0,40) + 0,30 × recherche (RESREL normalisé) + 0,20 × back office (bo/5) + 0,15 × (bonus BONREAD normalisé − 0,5), borné 10–95 % ; identification i = base (0,50 · 0,65 · 0,10) + 0,30 × recherche + 0,10 × (bonus − 0,5), bornée 5–95 % ; fausse alerte 15 % × (1 − s). Plus de canal « rumeur » séparé. Ligne « Votre veille… » sous les extrêmes du book ; le quant chiffre la perte de l'extrême identifié.
- **253** : protection (`HEDGE` c 1 % de l'encours, payée par le fonds, comptée dans qEvM et evLog ; h 70 % du choc immédiat de tout extrême du trimestre). Bloc sur la page co-investissement (après les ordres), page présente dès le 1er trimestre (« Protection » seule au T1). `S.hedgePick/hedgeAsk/hedgeQ`. Estimation du choc immédiat (`xImmEst`) : extrême signalé ou pire STRESS. Espérance sans signal légèrement négative (≈ −0,25 %/trim.), nettement positive avec un signal fiable.
- **254** : quant en moyen/difficile : « La lecture du modèle » (six convictions, sens et rang, sans tailles ni bouton). Fiches des styles et styTable (ligne « Extrêmes : sentir · identifier ») : quant 20–85 · 45–85, fonda 10–75 · 60–95, flux 33–95 · 5–45.
- **255** : fin de trimestre sans commission de performance (trimestre nul, négatif, ou positif sous le plus haut historique) : la page « Bonus d'équipe » devient « Pas de bonus » (`noBonusPage`) — pas de choix, explication, et tableau des effets au trimestre suivant (cran minimal : coûts, lecture des dépêches, anecdotes, veille des extrêmes, débauchage) comparés au taux choisi ; S.bonI conservé.
- **256** : « Ce que vous annoncez » — 4 options à seuils fixes (plus de goalK) : Pas de chiffre (confiance −2 si trimestre négatif), 2 % (+5/−4), 5 % (+14/−7 ; tenu : souscriptions ×1,2 au trimestre suivant), 10 % (+30/−8, comité −3 si manqué ; souscriptions ×1,5 / ×0,7). `commP` : chance affichée calée sur 195 trimestres (0,65 × attendu − 3 pts, dispersion ×1,25). `commClose` : série S.commStr (+1 par promesse tenue, plafond +5 ; manquée après 2 tenues : perte doublée), « tenu de justesse » (< 1 pt) : gain moitié ; S.commFx appliqué dans invInF. Presse : justesse, plateau télé, mème, série. Bot : 2e carte (standard).
- **257** : protection — prime = max(0,5 %, 2 × hedgeEV) ; hedgeEV = 70 % × choc immédiat attendu aux probabilités du marché (STRESS pondérés, dépêches x:1 uniformes), sans la veille. Affichage : espérance, prime, pire extrême avec sa probabilité de marché (`xMktP`). Couverture permanente : environ 1,3 à 2,6 pts de performance par an pour un book médian.
- **258** : extrême « Tout le monde a le même book » — chaque marché recule de S.crowd[i] × H (H 2,5, au lieu de −1,5 σ contre chaque position détenue) : les positions alignées sur la foule perdent, les positions à contre-courant gagnent. Choc immédiat médian −15,3 → −7,9 % ; pire extrême pour 11 % des books (56 % avant).
- **259** : coûts d'exécution — sans trader, courtier ×2 (NOTRD, ×4 avant) ; frein (exposant 0,35) dès 100 M$ (BRK0 0,1, 200 M$ avant).
- **260** : surcoût d'urgence (`URG`, `urgM`) — dépêche : suivre ×2,5 / contrer ×1,5 ; extrême (STRESS et dépêches x:1) : ×4 / ×2 (×5 et ×2 avant) ; accident de levier ×3 (×5) ; trader sur la classe : surcoût (m−1) réduit d'un tiers, aussi sur la rivalité (×1,5), le stop (×1,3) et l'appel de marge (×1,3, ×1,8). Texte « Comment lire ces chiffres » complété.
- **261** : contrer ×1 (dépêche) et ×1,5 (extrême) ; le trader multiplie tout coût d'urgence par 2/3 (et non plus le seul surcoût) : contrer une dépêche ×0,67, suivre ×1,67, extrême ×2,67 / ×1, accident ×2, rivalité ×1, stop ×0,87, appel de marge ×0,87 / ×1,2.
- **262** : décote à contre-sens (`REB`) — sur un cran « contrer », coût × urgence moins k × √(unités) pb du notionnel, plafonnée : dépêche 2,5 pb (6 au plus), extrême 15 pb (40 au plus). Mesure : contrer à fond un extrême rapporte dans 71 % des cas (médiane −16 pb de l'encours) ; contrer une dépêche reste presque toujours payant. Dock et texte : « rabais +… ». `urgF` : stop et appel de marge jamais sous ×1, même avec trader.
- **263** : revue des textes — styles (lecture des signaux tendance/portage/valeur par style, doublon incidents du flux retiré), difficultés (indulgence/sévérité du comité, pertes moins mal vécues en facile), durées (express), « sous le capot » (frein dès 100 M$ à la puissance 0,35, courtier ×2, surcoût d'urgence et contre-pied).
- **264** : extrêmes fusionnés — les dépêches x:1 deviennent des scénarios du catalogue STRESS (`mac:1`, x = h / (STRESSK × 1,5), même choc) : calcul sur le book, back office, foule, veille, protection identiques. Un seul tirage par trimestre : `xProbTot` = 1 − (1 − stressP)(1 − XPROB) ; famille tirée au prorata, scénarios macro sans répétition (S.usedX) ; `xScP` = probabilité de chaque scénario (prime, affichage).
- **265** : fin de trimestre, ligne `.qline` sous le résultat : Book · Dépêches et extrêmes · Incidents · Collatéral · Frais = total (S.qPnl, en % de l'encours de début de trimestre).
- **266** : fiches de style courtes (`sum` : pouvoir, 3 forces, 2 faiblesses ; `cardSum`) ; texte et détail repliés.
- **267** : glossaire au toucher (`GLOSS`, 16 termes ; `glossMark` via MutationObserver sur #app : première occurrence par note soulignée `.gl`, toucher = définition en modale ; jamais dans un bouton ou une carte).
- **268** : correctif — la classe du glossaire devient `.glo` (`.gl` servait déjà aux étiquettes des jauges).
- **269** : pouvoirs de l'équipe (`PW`, bloc `#pwblk` sur la page du book, `pwUse`, `pwOn(id)` = joué ce trimestre, S.pw). Jean-Kevin ±10 % sur tous les coûts (S.pwJK) ; Dwight : actions sans impact (tcost) ; Ingrid / Tuco : sens du marché de taux / de matière première le plus parlant (S.rBase, juste 75 / 80 %, S.pwTips) ; Boris : surcoût d'urgence ÷2 en devises (urgM) ; Winnie : capture 100 % sur les dépêches Asie/exotiques ; Sœur Marie-Alpha : book recalé sur S.tgt (pvol) et ordres du début de trimestre −25 % ; Onésime : confiance +5, fuite ; Gontran : option « passer l'écriture » sur l'incident (moitié, sans confiance) ; Josiane : aucune fuite ; Firmin : contrôle +3 ; Mireille : un jaune effacé par mandat (S.pwMi) ; Solange : choc d'extrême −20 %, cyber nul.
- **270** : 4e style `rv` (valeur relative) — paires (`pairDraw` après drawReturns : deux couples même classe, facteurs corrélés > 0,6 ; l'écart se referme de PAIRA 0,30 σ par jambe dans S.rBase, fait de marché pour tous ; `pairAlpha` dans expRet pour rv seul) ; décote de liquidité ×2 dans les extrêmes (stressGap) ; paramètres : vol ×0,8, coûts ×0,8, capture 0,55, nervosité ×0,85, équipe ×1,10, perf +2, seed 0,5 M$, lecture portage ×0,3, veille 0,20/0,30. Bloc `#stypw` (`styDraw`, crochets `styDrawX`/`styWire` pour les styles suivants). Écran d'accueil « 1 sur N ».
- **271** : 5e style `tail` (chasseur de queues) — `hH()`/`hL()` : protection rendant 120 % du choc immédiat, au juste prix (1 × l'espérance) ; « Encore un trimestre à payer l'assurance » −2 de confiance si couvert sans extrême ; bruit ×1 sur les trois signaux ; nervosité ×1,25 ; perf +3 ; incidents ×0,9 ; veille 0,32/0,45 (25–90 % · 40–80 %). Fourchettes de veille du style rv corrigées (12–78 % · 25–65 %).
- **272** : 6e style `act` (macro activiste) — l'attaque (`ATK` : mise 5/10/15 % de l'encours sur une devise ouverte, p = 0,25 + 0,10 × mise + 0,10 si expRet < 0 ; gain 1,2 × mise ; une par 4 trimestres, S.atk/S.atkLast) choisie sur la page du book (`styDrawX`, `styWire`), comité −2 au lancement ; `atkClose` en tête de resolveQuarter (P&L dans qEvM, evLog) ; confiance +15 / −10, comité −5 si ratée, presse. Paramètres : vol ×1,15, coûts ×1,2, capture 0,75, nervosité ×1,1, incidents ×1,2 / ×1,3, équipe ×1,2, perf +5, seed 1 M$, valeur ×0,3, veille 0,25/0,60.
- **273** : épilogue « Que sont-ils devenus ? » au rapport final (`epilogue(rank,tot)`) : vous (selon fin de partie, rang, performance), chaque trader présent, deux débauchés, le back office, le meilleur et le dernier concurrent.
- **274** : la marge fait les accidents de levier — NB : depuis le lot 101, `tailP(sp)` sans `std` vaut 0 (les accidents par le risque étaient éteints). `levAccP(mgu)` : 0 sous MGZ.watch 20 % de marge, puis 40 % × ((mgu − 20 %)/30 %)^1,3 au seuil d'appel ; `accP(k)` combine ; `tailDraw` tire l'accident (pool mg si dû à la marge, perte sur un risque équivalent 20 % + ½ (mgu − 20 %)). Jauge de marge dans la tuile Trésorerie (`.mgbar`, repères 20 % et 50 %, clignote dès 40 %) ; ligne « Levier » toujours visible sur la page du book (`#mgline`, `mgLineDraw` appelé par renderRisk). Mesure bots : marge médiane 13 %, q90 25 %.
- **233 (outil)** : bot flux plus sobre : équipe [1,1] et réserve de caisse 60 % (`BUD0`, `RES0` ; calibration 30 parties par variante : [3,2] 57 % de survie / 16,4 M$, [2,1] 50 % / 5,5, [1,1] 60 % / 10,6, [1,0] 47 % / 5,1).
  Lot 231 — diagnostic : le gérant flux touche ~0,5 M$ de frais de gestion par trimestre pour ~1 M$ d'équipe ; il vit des commissions de performance. Capital testé sans effet (0,5 / 1,5 / 2,5 M$ → survie 50 / 47 / 48 %, 30 parties chacune).
Lots 102–174 : voir `docs/HANDOFF_archive_lot192.md` (section « Lots 105–110 (détail) » et suivantes).
