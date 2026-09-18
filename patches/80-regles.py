# -*- coding: utf-8 -*-
"""Lot 8 — règles et économie.

1. Trésorerie de départ du gérant : 50 pb, un trimestre de commission de gestion, au lieu de
   200 pb. Conséquence voulue : au premier trimestre, 100 pb en caisse (capital + gestion)
   contre 143 pb pour tous les budgets au maximum — on ne peut donc plus tout prendre.
2. « Vos gains » affiche toujours la trésorerie disponible, capital de départ compris.
3. Flèches des facteurs macro sur cinq crans au lieu de trois.
4. Poursuite d'une dépêche : probabilité dans [0,40 ; 0,90] au lieu de [0,25 ; 0,75].
5. Annonce : investisseurs et comité fusionnés, mêmes montants 0 / 4 / 12 dans les deux sens.
   Les écarts entre les deux jauges et entre gain et perte étaient trop faibles pour se lire.
6. Textes de l'écran de création restés à quinze marchés et douze marchés.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()

# ── 1. trésorerie de départ ──
e.rep("""mgrCap0:0.02*Z.nav,""","""mgrCap0:0.005*Z.nav,""")

# ── 2. « Vos gains » : la trésorerie disponible, toujours ──
e.rep("""     ['<b>Gains nets</b>',`<b class="${mgrNet()>=0?'pos-g':'neg-g'}">${score(mgrNet())}</b>`],
     ['Capital de départ de la société',`<span class="dim-g">+${mm(S.mgrCap0||0)}</span>`],
     ['<b>Trésorerie disponible</b>',`<b class="${mgrCash()>=0?'':'neg-g'}">${mm(mgrCash())}</b>`]])}""",
"""     ['<b>Gains nets</b>',`<b class="${mgrNet()>=0?'pos-g':'neg-g'}">${score(mgrNet())}</b>`],
     ['Capital de départ de la société',`<span class="dim-g">+${mm(S.mgrCap0||0)}</span>`],
     ['<b>Trésorerie disponible</b>',`<b class="${mgrCash()>=0?'gold-g':'neg-g'}">${mm(mgrCash())}</b>`]])}
   <p class="note" style="margin-top:10px">Votre société a démarré avec <em>${mm(S.mgrCap0||0)}</em> en caisse, soit un trimestre de commission de gestion. Tout ce que vous engagez — budget d'exploitation et coûts d'exécution — sort de cette trésorerie : ${mgrCash()>=0?`il vous reste <em>${mm(mgrCash())}</em> à dépenser`:`vous êtes à découvert de <em>${mm(-mgrCash())}</em>, vos dépenses sont bloquées jusqu'à la prochaine commission`}.</p>""")

# ── 3. flèches des facteurs sur cinq crans ──
e.rep(""" const n=Math.min(3,Math.max(1,Math.round(Math.abs(z)/0.7)));
 if(Math.abs(z)<0.3)return '<span class="tri none">···</span>';""",
""" const n=Math.min(5,Math.max(1,Math.round(Math.abs(z)/0.45)));   /* cinq crans, pas trois */
 if(Math.abs(z)<0.25)return '<span class="tri none">···</span>';""")

# ── 4. la poursuite est plus souvent le cas ──
e.rep("""  S.sc={p:0.25+0.50*rng(),m:[0.45+0.40*rng(),-(0.30+0.40*rng())]};""",
"""  S.sc={p:0.40+0.50*rng(),m:[0.45+0.40*rng(),-(0.30+0.40*rng())]};   /* poursuite dans [0,40 ; 0,90] */""")

# ── 5. annonce : une seule échelle, 0 / 4 / 12 ──
e.rep("""   ret:g,win:{lp:4,rc:3},lose:{lp:-4,rc:-3}},""",
      """   ret:g,win:{lp:4,rc:4},lose:{lp:-4,rc:-4}},""")
e.rep("""   ret:2*g,win:{lp:10,rc:7},lose:{lp:-12,rc:-8}}""",
      """   ret:2*g,win:{lp:12,rc:12},lose:{lp:-12,rc:-12}}""")
e.rep("""   ${o.ret===null?`<div class="commrow"><span>En fin de trimestre, quoi qu'il arrive</span>${gzRows(o.lose.lp,o.lose.rc)}</div>`
    :`<div class="commrow"><span>Vous promettez pour ce trimestre</span><b>au moins ${sgnp(o.ret,1)} · ${mm(o.ret*S.nav)}</b></div>
      <div class="commrow"><span>En fin de trimestre, si c'est tenu</span>${gzRows(o.win.lp,o.win.rc)}</div>
      <div class="commrow"><span>En fin de trimestre, si c'est manqué</span>${gzRows(o.lose.lp,o.lose.rc)}</div>`}""",
"""   ${o.ret===null?`<div class="commrow"><span>En fin de trimestre, quoi qu'il arrive</span><b class="dim-g">investisseurs et comité inchangés</b></div>`
    :`<div class="commrow"><span>Vous promettez pour ce trimestre</span><b>au moins ${sgnp(o.ret,1)} · ${mm(o.ret*S.nav)}</b></div>
      <div class="commrow"><span>Si c'est tenu</span><b class="pos-g">investisseurs et comité +${o.win.lp}</b></div>
      <div class="commrow"><span>Si c'est manqué</span><b class="neg-g">investisseurs et comité −${-o.lose.lp}</b></div>`}""")
e.rep("""<h2>Ce que vous annoncez</h2><span class="hint">investisseurs · comité</span>""",
      """<h2>Ce que vous annoncez</h2><span class="hint">investisseurs et comité</span>""")

# ── 6. textes restés à l'ancienne carte du jeu ──
e.rep("""<div class="rule"><b>Le piège</b><span>Quinze marchés, mais seulement quatre grandes forces derrière eux""",
      """<div class="rule"><b>Le piège</b><span>Vingt-cinq marchés, mais seulement quatre grandes forces derrière eux""")
e.rep("""<p class="note">Les rendements des douze marchés sont engendrés par quatre facteurs orthonormés""",
      """<p class="note">Les rendements des marchés sont engendrés par quatre facteurs orthonormés""")
e.rep("""<p class="note">Les rumeurs sont vraies avec la probabilité de leur classe de fiabilité ;""",
      """<p class="note">Les sources disent vrai avec la probabilité de leur classe de fiabilité ;""")
e.rep(""" une rumeur vraie est tirée parmi celles dont l'impact prétendu s'aligne sur les facteurs réalisés.""",
      """ une source vraie est tirée parmi celles dont l'impact prétendu s'aligne sur les facteurs réalisés.""")


# ── 7. le bouton « Passer les ordres » doit se mettre à jour même si le book a changé
#       par un autre chemin que les boutons de position (modèle du desk, sonde, reprise) ──
e.rep("""   const c=liveTC();
   if(c>0&&c>Math.max(0,mgrCash()+c)){toast("Votre société de gestion ne peut pas payer ces ordres.");return}""",
"""   const c=liveTC();
   if(c>0&&c>Math.max(0,mgrCash()+c)){refreshSend();toast("Votre société de gestion ne peut pas payer ces ordres.");return}""")
e.done("lot 8 — regles et economie")
