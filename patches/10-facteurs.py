# -*- coding: utf-8 -*-
"""Lot 1 — charges factorielles demandées, et « silence radio » sans pénalité.

Échelle d'affichage (rowInfo) : |b| < 0,15 → 0 ; < 0,32 → 1 ; < 0,55 → 2 ; >= 0,55 → 3.
Contrainte dure : Σb² <= 0,92 par marché, sinon normB rescale tout le vecteur et fait
retomber une charge d'un cran sans prévenir. On vise Σb² <= 0,87 pour laisser passer la
dérive trimestrielle (0,035 de bruit par facteur et par trimestre).
Quand une demande ne tenait pas dans le budget, c'est une charge NON demandée du même
marché qui a été rognée — jamais la charge demandée.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()

CH=[
 # sym   ancien                        nouveau                       ce qui change
 ('ES',  "[ 0.45,-0.22, 0.18, 0.62]", "[ 0.45,-0.22, 0.18, 0.46]"),  # appétit 3 → 2
 ('MXEF',"[ 0.58, 0.24,-0.42, 0.34]", "[ 0.58, 0.24,-0.34, 0.58]"),  # appétit 2 → 3 ; dollar −2 conservé, un peu rogné
 ('NQ',  "[ 0.30,-0.48, 0.26, 0.72]", "[ 0.62,-0.34, 0.16, 0.58]"),  # croissance 1 → 3 ; inflation et appétit rognés
 ('TN',  "[-0.50,-0.40, 0.22,-0.42]", "[-0.50,-0.40,-0.42,-0.42]"),  # dollar +1 → −2
 ('GBL', "[-0.16,-0.66, 0.34,-0.18]", "[-0.16,-0.58, 0.34,-0.58]"),  # appétit −1 → −3 ; inflation reste −3
 ('R',   "[-0.34,-0.52,-0.30,-0.44]", "[-0.34,-0.52, 0.24,-0.44]"),  # dollar −1 → +1
 ('OAT', "[-0.20,-0.58, 0.26,-0.52]", "[-0.20,-0.58, 0.26,-0.08]"),  # appétit −2 → 0
 ('GC',  "[-0.18, 0.56,-0.58,-0.30]", "[-0.18, 0.62,-0.58,-0.30]"),  # inflation 3, éloignée du seuil
 ('BTC', "[ 0.24, 0.20,-0.36, 0.74]", "[ 0.24, 0.40,-0.34, 0.70]"),  # inflation 1 → 2 ; appétit reste 3
]
for sym,old,new in CH:
    e.rep("b:"+old,"b:"+new)

# « Silence radio » : ne rien promettre ne coûte plus rien.
e.rep("""   ret:null,win:{lp:-2,rc:-2},lose:{lp:-2,rc:-2}},""",
      """   ret:null,win:{lp:0,rc:0},lose:{lp:0,rc:0}},""")
e.rep("""Pas de lettre, pas de réunion, aucun chiffre avancé. Vous ne risquez pas de manquer une promesse, mais personne ne saura vous créditer d'un bon trimestre annoncé d'avance.""",
      """Pas de lettre, pas de réunion, aucun chiffre avancé. Vous ne risquez rien et vous ne gagnez rien : personne ne pourra vous reprocher une promesse manquée, personne ne vous créditera d'un bon trimestre annoncé d'avance.""")
e.rep("""   ret:null,win:{lp:0,rc:0},lose:{lp:0,rc:0}},""",
      """   ret:null,win:{lp:0,rc:0},lose:{lp:0,rc:0},neutre:true},""")
# une ligne de débriefing à zéro n'apprend rien : on ne l'écrit plus
e.rep("""else if(S.comm&&S.comm.id==='none')lpD.push(['Aucune communication ce trimestre',S.comm.lose.lp]);""",
      """else if(S.comm&&S.comm.id==='none'&&S.comm.lose.lp)lpD.push(['Aucune communication ce trimestre',S.comm.lose.lp]);""")
e.rep("""else if(S.comm&&S.comm.id==='none')rcD.push(['Aucune communication ce trimestre',S.comm.lose.rc]);""",
      """else if(S.comm&&S.comm.id==='none'&&S.comm.lose.rc)rcD.push(['Aucune communication ce trimestre',S.comm.lose.rc]);""")

e.done("lot 1 — facteurs et silence radio")
