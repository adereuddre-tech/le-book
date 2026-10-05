# Le Book — note de reprise (état au lot 212, bot 211)

Jeu de gérant de hedge fund global macro, en français. Fichier unique `index.html` (~830 ko), publié sur GitHub Pages :
https://adereuddre-tech.github.io/le-book/ — dépôt `adereuddre-tech/le-book`, branche `main`. **Dernier lot publié : 217.**

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
Lots 102–174 : voir `docs/HANDOFF_archive_lot192.md` (section « Lots 105–110 (détail) » et suivantes).
