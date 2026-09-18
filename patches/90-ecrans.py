# -*- coding: utf-8 -*-
"""Lot 9 — écrans.

1. Jauges investisseurs et comité : barres plus épaisses, et un liseré fin de la couleur du
   mouvement quand elles viennent de bouger.
2. Bilan de dépêche : la flèche de la barre d'état ne montrait que le DERNIER appel à
   `gauge()`. Une dépêche en fait deux à quatre (effet du mouvement, réaction offensive,
   pénalités du comité) : l'écran annonçait « investisseurs −9 » pendant que la tuile affichait
   « 61 →59 ». Corrigé : la flèche couvre maintenant toute la dépêche, effet immédiat compris.
3. Écran de création : « Créez votre fonds », cinq choix et non quatre, le paragraphe
   d'introduction et les explications dorées passent en pop-up de tutoriel.
4. Le tutoriel ne revient plus après la première partie (retenu dans le navigateur).
5. Mi-parcours : le mouvement des jauges est dans le texte visible, les contributeurs restent
   dans le détail replié.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()

# ══ 1. jauges plus épaisses, liseré au mouvement ══
e.rep(""".track{height:3px;background:var(--flat);border-radius:2px;overflow:hidden}
.track i{display:block;height:100%;border-radius:2px;transition:width .4s}""",
""".track{height:3px;background:var(--flat);border-radius:2px;overflow:hidden}
.track i{display:block;height:100%;border-radius:2px;transition:width .4s}
/* investisseurs et comité : la lecture centrale du jeu, elle mérite d'être épaisse */
.tile.gauge .track{height:7px;border-radius:4px}
.tile.gauge .track i{border-radius:4px}
.tile.gauge{padding-bottom:7px}
.tile.gauge.moved{box-shadow:0 0 0 1px var(--mv) inset;border-color:var(--mv)}
.tile.gauge.moved>span i{color:var(--mv)}""")

# ══ 2. la flèche doit couvrir toute la dépêche ══
# on note l'état des jauges AVANT l'effet immédiat de la dépêche
e.rep(""" const w=weights(S.k);
 let imm=0;const touched=[];""",
""" const w=weights(S.k);
 S.evG0={lp:S.lp,rc:S.rc};   /* état des jauges avant la dépêche : la flèche de la barre
                                d'état doit couvrir la dépêche entière, pas le dernier appel */
 let imm=0;const touched=[];""")
e.rep(""" const flowLines=[];midFlows(total,flowLines);
 const ev0=S.evImmG||{lp:0,rc:0};S.evImmG=null;""",
""" const flowLines=[];midFlows(total,flowLines);
 const ev0=S.evImmG||{lp:0,rc:0};S.evImmG=null;
 /* la barre d'état doit raconter la dépêche entière : `gauge()` écrase S.lastG à chaque
    appel et il y en a deux à quatre ici, d'où une flèche qui contredisait la ligne « Effets » */
 {const t={lp:ev0.lp+g.lp+gr.lp,rc:ev0.rc+g.rc+gr.rc};
  if(Math.abs(t.lp)>=0.05||Math.abs(t.rc)>=0.05)
   S.lastG={lp:t.lp,rc:t.rc,lp0:S.evG0?S.evG0.lp:S.lp-t.lp,rc0:S.evG0?S.evG0.rc:S.rc-t.rc};}
 S.evG0=null;""")

# ══ 3. mi-parcours : les jauges dans le texte visible ══
e.rep("""Rien n'est encaissé, mais les investisseurs et le comité reçoivent le rapport hebdomadaire et réagissent.`,""",
      """Rien n'est encaissé, mais les investisseurs et le comité reçoivent le rapport hebdomadaire et réagissent : ${gz(g.lp,g.rc,'always')}.`,""")


# ══ les deux tuiles centrales : épaisses, et cerclées quand elles viennent de bouger ══
e.rep(""" const gc=v=>v>55?'var(--long)':v>25?'var(--warn)':'var(--short)';""",
""" const gc=v=>v>55?'var(--long)':v>25?'var(--warn)':'var(--short)';
 /* liseré de la couleur du mouvement : on ne le montre que hors page de book, où la flèche
    indique un changement déjà appliqué et non une prévisualisation */
 const mvd=S.phase!=='book'&&S.lastG?S.lastG:null;
 const mvL=mvd&&Math.abs(mvd.lp)>=0.05?mvd.lp:0, mvR=mvd&&Math.abs(mvd.rc)>=0.05?mvd.rc:0;
 const mvSty=v=>v?`;--mv:${v>0?'var(--long)':'var(--short)'}`:'';""")
e.rep("""<button class="tile" data-gauge="lp" style="flex:1.05">""",
      """<button class="tile gauge${mvL?' moved':''}" data-gauge="lp" style="flex:1.05${mvSty(mvL)}">""")
e.rep("""<button class="tile" data-gauge="rc" style="flex:1.05">""",
      """<button class="tile gauge${mvR?' moved':''}" data-gauge="rc" style="flex:1.05${mvSty(mvR)}">""")

# ── le total affiché doit être le mouvement réel des jauges, bornes et retraits compris ──
# `midFlows` appelle aussi `gauge()` (un retrait après une mauvaise dépêche coûte 1 point) et
# `gauge()` borne les jauges à [0,100] : additionner les effets un à un ne donne donc pas
# toujours ce que le joueur voit bouger. On mesure l'écart réel entre avant et après.
e.rep(""" {const t={lp:ev0.lp+g.lp+gr.lp,rc:ev0.rc+g.rc+gr.rc};
  if(Math.abs(t.lp)>=0.05||Math.abs(t.rc)>=0.05)
   S.lastG={lp:t.lp,rc:t.rc,lp0:S.evG0?S.evG0.lp:S.lp-t.lp,rc0:S.evG0?S.evG0.rc:S.rc-t.rc};}
 S.evG0=null;""",
""" const g0=S.evG0||{lp:S.lp-(ev0.lp+g.lp+gr.lp),rc:S.rc-(ev0.rc+g.rc+gr.rc)};
 const tg={lp:S.lp-g0.lp,rc:S.rc-g0.rc};
 if(Math.abs(tg.lp)>=0.05||Math.abs(tg.rc)>=0.05)S.lastG={lp:tg.lp,rc:tg.rc,lp0:g0.lp,rc0:g0.rc};
 S.evG0=null;""")
# `S.evLog` reste l'effet propre de la dépêche : c'est lui qui sert à l'attribution du
# trimestre, et c'est sur lui que porte la sonde « affiché = appliqué » du harnais. Le point de
# jauge perdu sur un retrait d'allocataire appartient aux flux, pas à la dépêche.
e.rep("""  ['Effets',gz(ev0.lp+g.lp+gr.lp,ev0.rc+g.rc+gr.rc,'always')]];""",
      """  ['Effets',gz(tg.lp,tg.rc,'always')]];""")
e.done("lot 9 — jauges, bilan de depeche, mi-parcours")
