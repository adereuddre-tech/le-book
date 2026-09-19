# -*- coding: utf-8 -*-
"""Lot 25 — une seule façon de perdre, une seule jauge à surveiller.

Avant : quatre morts distinctes (repli, jauge investisseurs, jauge comité, appel de marge),
qui mesuraient toutes la même chose sans se parler, plus des rachats qui saignaient à côté.
Un gérant pouvait multiplier son fonds par sept et mourir d'un repli de 13 % pris depuis un
sommet, sans avoir perdu un dollar par rapport au départ.

Après : il n'y a qu'une façon de perdre un mandat, et c'est que les investisseurs partent.
  - **Une seule jauge affichée, la confiance**, qui agrège ce que pensent les investisseurs et
    le comité : `0,6 × le plus bas des deux + 0,4 × leur moyenne`. Le plus bas pèse le plus,
    parce qu'il suffit d'un des deux pour déclencher les rachats. Les deux canaux restent
    séparés en interne — ils réagissent à des choses différentes — mais le joueur n'a plus
    qu'un chiffre à suivre.
  - **Le repli, le comité et les appels de marge ne tuent plus.** Ils provoquent des rachats,
    d'autant plus violents que la confiance est basse et que le repli est profond.
  - **Une seule mort : l'encours.** Sous 40 % de l'encours initial, il n'y a plus de quoi
    payer la structure et le mandat s'arrête.

Effet de bord voulu : la sanction devient automatiquement proportionnelle au risque pris.
Un gérant qui court à six fois son mandat subit des rachats bien plus souvent, donc son
encours fond ; nul besoin d'indexer un seuil de repli sur la volatilité.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()

e.rep("""function gauge(dlp,drc,why){""",
"""/* La confiance : ce que le joueur suit. Le plus bas des deux canaux pèse le plus, parce
   qu'un seul suffit à vider la base d'investisseurs. */
function conf(){return 0.6*Math.min(S.lp,S.rc)+0.4*(S.lp+S.rc)/2}
/* Rachats : tout ce qui allait tuer provoque désormais un départ d'allocataires. */
function redeem(cause,amp){
 const c=conf(),nerf=Math.max(0,(55-c)/55);
 const out=Math.max(0,Math.min(0.45,amp*(0.45+1.35*nerf)));
 if(out<0.002)return 0;
 S.nav*=(1-out);S.flows-=out*S.nav;S.qFlow=(S.qFlow||0)-out*S.nav;
 (S.qRedeem=S.qRedeem||[]).push({cause,out});
 return out;
}
function gauge(dlp,drc,why){""")

# ── la mort : l'encours, et lui seul ──
e.rep(""" if(S.maxdd>=ddMax())S.over='dd';
 else if(S.lp<=8)S.over='lp';
 else if(S.rc<=4)S.over='rc';
 else if(S.rc<=13&&S.maxk>3){""",
""" /* plus de mort par jauge ni par repli : chacun provoque des rachats, et c'est l'encours
    qui décide de la fin du mandat */
 S.qRedeem=[];
 if(S.maxdd>=ddMax())redeem('repli',0.10+0.35*(S.maxdd-ddMax()));
 if(S.lp<=20)redeem('investisseurs',0.05+0.006*(20-S.lp));
 if(S.rc<=20)redeem('comité',0.05+0.006*(20-S.rc));
 if(S.nav<0.40*S.aum0)S.over='nav';
 if(S.rc<=13&&S.maxk>3){""")

# ── verdicts ──
e.rep(""" if(S.over==='dd'){verdict="Le fonds est liquidé";vtxt=`La perte a dépassé ${Math.round(ddMax()*100)} %. Les clauses de rachat se sont déclenchées en cascade au trimestre ${S.q}.`}""",
""" if(S.over==='nav'){verdict="L'encours n'y est plus";vtxt=`Le fonds est tombé sous 40 % de son encours de départ au trimestre ${S.q} : les commissions ne couvrent plus la structure, le mandat s'arrête. Les rachats se sont enchaînés — perte de confiance, replis, appels de marge — jusqu'à ce qu'il ne reste plus assez à gérer.`}
 else if(S.over==='dd'){verdict="Le fonds est liquidé";vtxt=`La perte a dépassé ${Math.round(ddMax()*100)} %. Les clauses de rachat se sont déclenchées en cascade au trimestre ${S.q}.`}""")

# ── la barre d'état : une jauge au lieu de deux ──
e.rep("""<button class="tile gauge${mvL?' moved':''}" data-gauge="lp" style="flex:1.05${mvSty(mvL)}">""",
      """<button class="tile gauge${(mvL||mvR)?' moved':''}" data-gauge="lp" style="flex:2.1${mvSty(mvL||mvR)}">""")
e.rep("""<button class="tile gauge${mvR?' moved':''}" data-gauge="rc" style="flex:1.05${mvSty(mvR)}">""",
      """<button class="tile gauge" data-gauge="rc" style="display:none">""")
e.rep("""<span><i>Invest.</i><b>${S.phase!=='book'&&S.lastG?gArrow(S.lastG.lp0,S.lp):Math.round(S.lp)}${S.phase==='book'&&S._pv&&Math.abs(S._pv.lp)>=0.05?`<span class="${cls(S._pv.lp)}">→${Math.round(Math.max(0,Math.min(100,S.lp+S._pv.lp)))}</span>`:''}</b></span>""",
"""<span><i>Confiance</i><b>${S.phase!=='book'&&S.lastG?gArrow(0.6*Math.min(S.lastG.lp0,S.lastG.rc0)+0.4*(S.lastG.lp0+S.lastG.rc0)/2,conf()):Math.round(conf())}${S.phase==='book'&&S._pv?(()=>{const nl=Math.max(0,Math.min(100,S.lp+(S._pv.lp||0))),nr=Math.max(0,Math.min(100,S.rc+(S._pv.rc||0))),nc=0.6*Math.min(nl,nr)+0.4*(nl+nr)/2,d=nc-conf();return Math.abs(d)>=0.05?`<span class="${cls(d)}">→${Math.round(nc)}</span>`:''})():''}</b></span>""")

e.done("lot 25 — confiance unique, mort unique")
