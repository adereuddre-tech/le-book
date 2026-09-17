# Outils de test de Le Book

Prérequis : Node 22 et `npm i jsdom` à la racine du dépôt ; Playwright (Python) et un
Chromium pour les captures.

| Outil | Rôle |
|---|---|
| `play.js <fichier> <graine> [--sage] [--size small\|mid\|mega] [--univ fin\|com\|ext] [--dur express\|normal\|saison] [--prof syst\|fonda\|flux] [--resume N] [--log]` | Joue une partie complète jusqu'à `#again`, compte les erreurs, sonde l'écart entre jauges affichées et appliquées dans les dépêches (`bad`, 0 exigé). `--resume N` recharge à froid à la N-ième dépêche. Sortie : une ligne JSON. |
| `reg.sh [fichier] [sortie]` | Régression 9 combinaisons × 2 styles. |
| `summ.py <sortie>…` | Synthèse des lignes `style mode JSON`. |
| `cover3.js [fichier]` | `evPlans` sur toutes les dépêches ouvertes, 3 styles × 2 univers, avec et sans interdiction du comité. |
| `bot.js --prof … --seed … [--vol --size --univ --dur] [--bud e,r,s] [--policy smart\|naive]` | Bot « intelligent » : book construit sur les sources, lectures, indicateurs et intuition (95 % de la vol cible) ; dépêches à la meilleure espérance sur les probabilités affichées, jauges pondérées davantage quand elles sont basses ; autres choix lus dans le texte des boutons. Rend score, commissions, budget, rendement, survie. Utilisable en module (`playGame`). |
| `runner.js plan.json sortie.jsonl [N]` | Joue un plan de parties (tableau d'options de `playGame`), reprend là où il s'est arrêté, N parties par processus. |
| `loop.sh plan.json sortie.jsonl` | Enchaîne des `runner.js` courts jusqu'à la fin du plan (jsdom fuit de la mémoire : un processus long finit par caler). Crée `sortie.jsonl.fin`. **Un seul `loop.sh` par fichier de sortie**, sinon les lignes se décalent par rapport au plan. |
| `calib.py res.jsonl:plan.json …` | Écarts appariés (même graine, même style) des budgets par rapport au standard, et scores des choix initiaux. |
| `powerchk.js [fichier]` | Pouvoirs propres : source vérifiée toujours vraie, intuition juste, bouton du modèle, captures, coûts, ajustement offert, précision des probabilités de dépêche. |
| `shot.py <fichier> "<condition JS d'arrêt>" "<sélecteur>" <sortie.png>` | Joue dans Chromium (380 px) jusqu'à la condition, capture le sélecteur. |

Exemples :

```
node tools/play.js index.html 11 --prof flux --dur normal
node tools/play.js index.html 3 --prof syst --resume 2
python3 tools/shot.py index.html "!!document.querySelector('.evopt')" ".status" status.png
```

Dans `shot.py`, le chemin du Chromium est `/opt/pw-browsers/chromium-1194/chrome-linux/chrome` :
à adapter hors du bac à sable Claude.
