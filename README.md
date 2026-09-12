# Le Book — un fonds global macro de 100 milliards

Un jeu de gestion dans un seul fichier HTML, sans serveur, sans dépendance à installer.

## Jouer en local
Ouvrez `index.html` dans un navigateur (Chrome, Safari, Firefox). Fonctionne sur mobile et ordinateur.
Les polices viennent de Google Fonts ; sans connexion, le jeu tourne quand même avec des polices de repli.

## Mettre en ligne (gratuit, deux minutes)
**Netlify Drop** — la solution la plus simple, celle utilisée par « La bataille du budget » :
1. Allez sur https://app.netlify.com/drop
2. Glissez-déposez le dossier `le-book` (celui qui contient `index.html`).
3. Netlify vous donne une adresse du type `https://nom-aleatoire.netlify.app` — modifiable dans *Site settings › Change site name* (par exemple `le-book-macro.netlify.app`).

**GitHub Pages** — si vous avez un compte GitHub :
1. Créez un dépôt public, déposez `index.html` à la racine.
2. *Settings › Pages › Source : main / root*. L'adresse est `https://<votre-compte>.github.io/<dépôt>/`.

**itch.io** — si vous voulez le référencer comme un jeu : créez un projet « HTML », téléversez un zip contenant `index.html`, cochez *This file will be played in the browser*.

## Partager un résultat
En fin de partie, le bouton « Partager ce résultat » copie un résumé (verdict, performance, rang, Sharpe, graine). La graine fixe la trajectoire des marchés : deux joueurs avec la même graine et la même configuration affrontent le même monde — mais pas les mêmes dépêches, car leurs décisions décalent les tirages.

## Reprendre une partie
La partie en cours est sauvegardée dans le navigateur à chaque étape. Si vous fermez l'onglet ou rafraîchissez la page, le bouton « Reprendre la partie en cours » apparaît sur l'écran d'accueil.

## Sous le capot
Quinze marchés, modèle factoriel à quatre facteurs (croissance, inflation, dollar, appétit pour le risque), régimes macro en chaîne de Markov, coûts d'exécution en racine carrée du notionnel, rumeurs vraies avec la probabilité de leur classe de fiabilité, quatre fonds concurrents simulés, Sharpe probabiliste de Bailey et López de Prado au rapport final. Tout est dans le fichier ; le panneau « Comment ça marche sous le capot » sur l'écran de composition en donne le résumé.
