# -*- coding: utf-8 -*-
"""Lot 42 — le score devient un indice : 100 = le gérant médian de la place.

Décision d'Antoine (option B). Avec des fonds de 100 M$ à 10 Md$, un score en dollars de
commissions n'a plus de sens ; un score en % de l'encours initial serait neutre en taille et
rendrait le mastodonte plus dur sans rien rapporter. On compare donc le gérant à ses pairs.

  - Chaque concurrent tient son propre compte de gérant (`rivalMgrQuarter`) : commission de
    gestion à l'ouverture sur son encours, commission de performance au-dessus de son plus haut,
    moins un budget standard et une facture d'ordres type. Mêmes frais que votre mandat.
  - `mgrIndex()` = 100 + 100 × (vos gains − gains du gérant médian) / max(|médian|, R), où R vaut
    1 % de l'encours initial par année écoulée : un plancher qui empêche l'indice d'exploser
    quand la place gagne presque rien. 150 : moitié mieux que le gérant médian ; 50 : moitié
    moins ; sous 0 : vous avez perdu de l'argent quand la place en gagnait.
  - Les montants restent affichés (M$ ou Md$) à côté, et en % de l'encours initial.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
e.rep(" S.rivals.forEach((rv,j)=>{rv.last=rr[j];rv.cum*=(1+rr[j]);(rv.hist=rv.hist||[]).push(rr[j])});",
      " S.rivals.forEach((rv,j)=>{rv.last=rr[j];rv.cum*=(1+rr[j]);(rv.hist=rv.hist||[]).push(rr[j]);rivalMgrQuarter(rv,rr[j])});")
e.rep("function budgetBp(){","""/* ── le compte de gérant des concurrents : de quoi situer le vôtre ──────────────────
   Budget standard (cran 5 sur 11 des trois postes, masse salariale comprise) et facture
   d'ordres type, par trimestre, en fraction de leur encours. */
function rivalCostQ(){return (BUDGET.reduce((a,b)=>a+b.lv[4].bp,0)+DESK().fixed*1e4+16)*1e-4}
function rivalMgrQuarter(rv,r){
 /* champs propres (mAum, mHwm) : `aum` existe déjà chez les concurrents, en unités d'affichage */
 const v=VOL();
 if(rv.mAum===undefined||rv.mgr===undefined){
  rv.mAum=S.aum0;rv.mHwm=S.aum0;rv.mgr=0;
  /* sauvegarde d'avant le lot 42 : on rejoue les trimestres déjà joués (le dernier de hist est r) */
  const h=(rv.hist||[]).slice(0,-1);rv.mgr=0;h.forEach(g=>rivalMgrQuarter(rv,g));
 }
 const mg=v.mgmt*rv.mAum,cost=rivalCostQ()*rv.mAum;
 rv.mAum*=(1+r);
 const perf=v.perf*Math.max(0,rv.mAum-rv.mHwm);rv.mHwm=Math.max(rv.mHwm,rv.mAum);
 rv.mgr+=mg+perf-cost;
}
function rivalMgrMedian(){const v=S.rivals.map(r=>r.mgr||0).sort((a,b)=>a-b),n=v.length;return n?(n%2?v[n>>1]:(v[n/2-1]+v[n/2])/2):0}
/* L'indice du gérant : 100 = le gérant médian de la place. */
function mgrIndex(){
 const P=S.mgrFees-S.mgrCosts,M=rivalMgrMedian(),R=0.01*S.aum0*Math.max(1,S.q)/4;
 return 100+100*(P-M)/Math.max(Math.abs(M),R);
}
function budgetBp(){""")

# ── affichage de l'indice ───────────────────────────────────────────────────────
e.rep("""   <div class="cell" style="background:linear-gradient(180deg,rgba(217,176,106,.14),rgba(217,176,106,.03))"><div class="cl" style="color:var(--gold)">Vos gains de gérant</div><div class="cv" style="color:var(--gold)">${score(S.mgrFees-S.mgrCosts)}</div></div>""",
"""   <div class="cell" style="grid-column:1/-1;background:linear-gradient(180deg,rgba(217,176,106,.20),rgba(217,176,106,.04))"><div class="cl" style="color:var(--gold)">Indice du gérant · 100 = le gérant médian de la place</div><div class="cv" style="color:var(--gold);font-size:34px">${Math.round(mgrIndex())}</div><div class="cl" style="margin-top:4px">${score(S.mgrFees-S.mgrCosts)} de gains, soit ${sgnp((S.mgrFees-S.mgrCosts)/S.aum0,1)} de l'encours initial · gérant médian ${sgnp(rivalMgrMedian()/S.aum0,1)}</div></div>""")
e.rep("const txt=`${S.fundName} — ${verdict}. ${score(S.mgrFees-S.mgrCosts)} de gains de gérant,",
      "const txt=`${S.fundName} — ${verdict}. Indice du gérant ${Math.round(mgrIndex())} (100 = gérant médian), ${score(S.mgrFees-S.mgrCosts)} de gains,")
# palmarès : classé sur l'indice ; les parties d'avant le lot 42 n'en ont pas et passent après
e.rep(" h.push({f:S.fundName,g:S.mgrFees-S.mgrCosts,v:o.verdict,c:o.cagr,r:o.rank,s:S.size,p:S.prof,q:S.q,d:Date.now()});\n h.sort((a,b)=>b.g-a.g);",
      " h.push({f:S.fundName,g:S.mgrFees-S.mgrCosts,ix:mgrIndex(),v:o.verdict,c:o.cagr,r:o.rank,s:S.size,p:S.prof,q:S.q,d:Date.now()});\n h.sort((a,b)=>(b.ix===undefined?-1e9:b.ix)-(a.ix===undefined?-1e9:a.ix)||b.g-a.g);")
e.rep("Le classement se fait sur les commissions encaissées : c'est le score du jeu.",
      "Le classement se fait sur l'indice du gérant — 100, c'est le gérant médian de la place : il compare des fonds de 100 M$ et de 10 Md$ à armes égales.")
e.rep("""    <span class="hval"><b class="gold-g">${score(r.g)}</b><span class="hsub ${cls(r.c)}">${sgnp(r.c,0)} par an</span></span>""",
      """    <span class="hval"><b class="gold-g">${r.ix===undefined?score(r.g):'indice '+Math.round(r.ix)}</b><span class="hsub ${cls(r.c)}">${r.ix===undefined?'':score(r.g)+' · '}${sgnp(r.c,0)} par an</span></span>""")
# hauts faits de gains : en part de l'encours initial (50 M$ sur l'ancien fonds de 100 M$ = 50 %)
e.rep('nm:"La belle année",d:"Dépasser 50 M$ de gains de gérant sur une partie.",tf:f=>f.gains>0.050}',
      'nm:"La belle année",d:"Gagner, en commissions nettes, la moitié de l\'encours de départ.",tf:f=>f.gains>0.5*f.aum0}')
e.rep('nm:"Le gros chèque",d:"Dépasser 150 M$ de gains de gérant sur une partie.",tf:f=>f.gains>0.150}',
      'nm:"Le gros chèque",d:"Gagner, en commissions nettes, une fois et demie l\'encours de départ.",tf:f=>f.gains>1.5*f.aum0}')
e.rep('nm:"La fortune",d:"Dépasser 400 M$ de gains de gérant sur une partie.",tf:f=>f.gains>0.400}',
      'nm:"La fortune",d:"Gagner, en commissions nettes, quatre fois l\'encours de départ.",tf:f=>f.gains>4*f.aum0}')
e.rep(" S.finalCtx={over:S.over,rank,cagr,tot,gains:S.mgrFees-S.mgrCosts,"," S.finalCtx={over:S.over,rank,cagr,tot,gains:S.mgrFees-S.mgrCosts,aum0:S.aum0,ix:mgrIndex(),")
e.done("lot 42 — indice du gerant")
