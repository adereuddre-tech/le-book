# -*- coding: utf-8 -*-
"""Lot 57 — nettoyage, troisième passe.

Constat :
- Écran d'accueil : le mur des 25 marchés et les 3 concurrents s'affichent en
  entier avant même le bouton « Fonder le fonds », alors qu'ils ne servent
  qu'à feuilleter. Repliés : le joueur voit direct le nom/écusson/bouton.
- Anecdotes du desk (exécution et mi-parcours) : le texte affiché en tête du
  résultat est presque toujours une répétition mot pour mot de la ligne du
  bouton que le joueur vient de lire et de cliquer, pendant que l'effet
  concret (montant, position) est caché sous « Le détail ». On inverse :
  le concret en tête, plus de répétition quand il n'y a rien d'autre à dire.
- Rapport final : le calcul du Sharpe probabiliste (deux paragraphes +
  formule) reste affiché en entier alors que le chiffre qui compte (le %)
  est déjà répété deux fois dans la phrase. Le détail passe dans un repli.
"""
from _lib import Ed
e = Ed()

# ── Accueil : marchés + concurrents repliés ──────────────────────────────
e.rep(
'''  <div class="isec">LES VINGT-CINQ MARCHÉS</div>
  <p class="splash-p" style="margin-top:8px">Actions, taux, devises, matières premières, et quelques objets moins recommandables. La taille de votre fonds décide de ceux qui vous sont ouverts.</p>
  ${mktWall()}
  <div class="isec">CEUX D'EN FACE</div>
  <p class="splash-p" style="margin-top:8px">Quatre fonds jouent le même trimestre que vous. Vos investisseurs comparent — et c'est l'écart à la médiane qui décide des rachats, pas votre performance absolue.</p>
  ${introRivals()}
  <p class="splash-p" style="margin:18px 0 0">Le monde ne vous attendra pas''',
'''  <details class="wire" style="margin-top:18px"><summary>Les marchés et la concurrence</summary>
  <div class="isec" style="margin-top:14px">LES VINGT-CINQ MARCHÉS</div>
  <p class="splash-p" style="margin-top:8px">Actions, taux, devises, matières premières, et quelques objets moins recommandables. La taille de votre fonds décide de ceux qui vous sont ouverts.</p>
  ${mktWall()}
  <div class="isec">CEUX D'EN FACE</div>
  <p class="splash-p" style="margin-top:8px">Quatre fonds jouent le même trimestre que vous. Vos investisseurs comparent — et c'est l'écart à la médiane qui décide des rachats, pas votre performance absolue.</p>
  ${introRivals()}
  </details>
  <p class="splash-p" style="margin:18px 0 0">Le monde ne vous attendra pas''',
)

# ── Anecdote d'exécution : plus de répétition de ch.s en tête ────────────
e.rep(
"resultCard('EXÉCUTION · '+ev.who.split(' ·')[0].toUpperCase(),ch.b,[ch.s,...msg],[],",
"resultCard('EXÉCUTION · '+ev.who.split(' ·')[0].toUpperCase(),ch.b,msg.length?msg:[''],[],",
)

# ── Anecdote du desk (mi-parcours) : idem, garde ev.after si un jour posé ─
e.rep(
"resultCard(`LE DESK · ${ev.who.split(' ·')[0].toUpperCase()}`,ch.b,[ev.after||ch.s,...msg],",
"resultCard(`LE DESK · ${ev.who.split(' ·')[0].toUpperCase()}`,ch.b,ev.after?[ev.after,...msg]:(msg.length?msg:['']),",
)

# ── Rapport final : la démonstration PSR passe dans un repli ─────────────
e.rep(
'''  <div class="psr"><h2 style="font-size:15px">Ce que ces chiffres prouvent</h2>
   <p>Sur ${n} observations trimestrielles, l'écart-type d'estimation de votre Sharpe annualisé est d'environ <b class="num">±${dec(seSR,2)}</b>. Votre Sharpe probabiliste — la probabilité que le vrai Sharpe soit strictement positif, corrigée de l'asymétrie et de l'épaisseur des queues — ressort à <b class="num">${(psr*100).toFixed(0)} %</b>.</p>
   <p>${psr>0.95?"Au-delà de 95 %, c'est le seuil habituellement retenu pour dire qu'un historique contient autre chose que du bruit. Vous y êtes — sur huit points, ce qui reste très peu.":"En dessous de 95 %, un allocataire sérieux ne peut pas distinguer votre compétence de la chance. C'est vrai de la quasi-totalité des historiques de deux ans, y compris les bons."}</p>
   <div class="f">PSR = Φ[ ŜR·√(n−1) / √(1 − γ₃·ŜR + (γ₄−1)/4·ŜR²) ]<br>n = ${n} · ŜR<sub>trim</sub> = ${dec(srQ,3)} · γ₃ = ${dec(m3,2)} · γ₄ = ${dec(m4,2)}</div></div>''',
'''  <div class="psr"><h2 style="font-size:15px">Ce que ces chiffres prouvent</h2>
   <p>Votre Sharpe probabiliste — la probabilité que le vrai Sharpe soit strictement positif, corrigée de l'asymétrie et de l'épaisseur des queues — ressort à <b class="num">${(psr*100).toFixed(0)} %</b>.</p>
   <details><summary>Le calcul</summary>
   <p style="margin-top:8px">Sur ${n} observations trimestrielles, l'écart-type d'estimation de votre Sharpe annualisé est d'environ <b class="num">±${dec(seSR,2)}</b>. ${psr>0.95?"Au-delà de 95 %, c'est le seuil habituellement retenu pour dire qu'un historique contient autre chose que du bruit. Vous y êtes — sur huit points, ce qui reste très peu.":"En dessous de 95 %, un allocataire sérieux ne peut pas distinguer votre compétence de la chance. C'est vrai de la quasi-totalité des historiques de deux ans, y compris les bons."}</p>
   <div class="f">PSR = Φ[ ŜR·√(n−1) / √(1 − γ₃·ŜR + (γ₄−1)/4·ŜR²) ]<br>n = ${n} · ŜR<sub>trim</sub> = ${dec(srQ,3)} · γ₃ = ${dec(m3,2)} · γ₄ = ${dec(m4,2)}</div></details></div>''',
)

e.done('lot 57 : accueil replié, anecdotes du desk sans répétition, PSR replié')
