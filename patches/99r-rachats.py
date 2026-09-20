# -*- coding: utf-8 -*-
"""Lot 29 — calibration des rachats : la nervosité du style doit s'y retrouver.

Campagne de 90 parties sur le mécanisme du lot 25 : survie globale 69 %, 2,5 rachats par
partie, ponction cumulée médiane de 30 % de l'encours, et des causes bien réparties
(repli 85, comité 83, investisseurs 55). Les intensités posées à l'estime tiennent.

Un défaut en revanche : le flux redevenait le style le PLUS sûr — 77 % de survie contre 60 %
au fondamental — alors que le lot 6 l'avait réglé à l'inverse. En supprimant la mort par
repli, on a supprimé ce qui le sanctionnait : son seuil de liquidation serré (0,13) était
justement sa contrepartie. Les rachats sont désormais proportionnels à `lpMult`, la nervosité
des investisseurs propre au style — 1,60 pour le flux, 0,90 pour le quant. C'est le paramètre
qui décrit déjà cette contrepartie, et il retrouve là son rôle.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
e.rep(""" const c=conf(),nerf=Math.max(0,(55-c)/55);
 const out=Math.max(0,Math.min(0.45,amp*(0.45+1.35*nerf)));""",
""" const c=conf(),nerf=Math.max(0,(55-c)/55);
 const style=(typeof PROF==='function'&&PROF().lpMult)||1;   /* nervosité propre au style */
 const out=Math.max(0,Math.min(0.5,amp*style*(0.45+1.35*nerf)));""")
e.done("lot 29 — rachats indexes sur la nervosite du style")
