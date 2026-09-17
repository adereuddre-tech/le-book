# Outils de test de Le Book

Prérequis : Node 22 et `npm i jsdom` à la racine du dépôt ; Playwright (Python) et un
Chromium pour les captures.

| Outil | Rôle |
|---|---|
| `play.js <fichier> <graine> [--sage] [--size small\|mid\|mega] [--univ fin\|com\|ext] [--dur express\|normal\|saison] [--prof syst\|fonda\|flux] [--resume N] [--log]` | Joue une partie complète jusqu'à `#again`, compte les erreurs, sonde l'écart entre jauges affichées et appliquées dans les dépêches (`bad`, 0 exigé). `--resume N` recharge à froid à la N-ième dépêche. Sortie : une ligne JSON. |
| `reg.sh [fichier] [sortie]` | Régression 9 combinaisons × 2 styles. |
| `summ.py <sortie>…` | Synthèse des lignes `style mode JSON`. |
| `cover3.js [fichier]` | `evPlans` sur toutes les dépêches ouvertes, 3 styles × 2 univers, avec et sans interdiction du comité. |
| `shot.py <fichier> "<condition JS d'arrêt>" "<sélecteur>" <sortie.png>` | Joue dans Chromium (380 px) jusqu'à la condition, capture le sélecteur. |

Exemples :

```
node tools/play.js index.html 11 --prof flux --dur normal
node tools/play.js index.html 3 --prof syst --resume 2
python3 tools/shot.py index.html "!!document.querySelector('.evopt')" ".status" status.png
```

Dans `shot.py`, le chemin du Chromium est `/opt/pw-browsers/chromium-1194/chrome-linux/chrome` :
à adapter hors du bac à sable Claude.
