p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# M1 : le moral visé ne dépend que du cran de bonus versé (30, 40, 50, 62, 75, 95) et des locaux ; le taux reste celui du lot 363
rep("""function motTrho(r){return 30+65*(1-Math.exp(-Math.max(0,r)/BONK.r0))+motOff()}
""","")
rep("""function motT(i){return motTrho(bonRho(i,(S&&S.mgrQ&&S.mgrQ.perf)||0))}   /* lot 363 : cible lue sur le bonus rapporté aux salaires */""",
"""function motT(i){return MORAL.tg[Math.max(0,Math.min(MORAL.tg.length-1,i))]+motOff()}   /* lot 365 : retour à la cible par cran, quel que soit le montant */""")
rep("""const BONK={fo:2.5,bo:10,max:0.9,floor:0.01,r0:0.8};""","""const BONK={fo:2.5,bo:10,max:0.9,floor:0.01};""")
rep("""function bonRho(i,perf){const sq=salQ();return sq>0&&perf>0?Math.min(bonRate(i)*perf,Math.max(0,mgrCash()))/sq:0}   /* bonus versé / salaires du trimestre */
""","")
rep(""" S.bonEff=perf>0?i:0;
 motV();motAdd(MORAL.k*(motTrho(perf>0&&salQ()>0?amt/salQ():0)-S.mot),""",""" S.bonEff=perf>0&&amt>0?i:0;
 motV();motAdd(MORAL.k*(motT(S.bonEff)-S.mot),""")
rep("""fixée par ce que le bonus représente pour l'équipe — 30 sans bonus, ≈ 52 à un tiers des salaires du trimestre, ≈ 76 à un trimestre de salaire, ≈ 90 à deux, ≈ 95 à quatre — relevée""",
"""fixée par votre cran de bonus — 30 au minimum ou sans bonus versé, puis 40, 50, 62, 75 et 95 au cran 🔥 — relevée""")
rep("""vers une cible qui dépend de ce que le bonus représente pour l'équipe : 30 sans bonus, ≈ 52 à un tiers des salaires du trimestre, ≈ 76 à un trimestre de salaire, ≈ 90 à deux, ≈ 95 à quatre, plus selon vos locaux.""",
"""vers la cible de votre cran (${MORAL.tg.join(', ')}, plus selon vos locaux), pourvu qu'un bonus soit versé ; sinon, vers ${MORAL.tg[0]}.""")
rep("""un multiplicateur sur tous vos coûts d'exécution, fourchette et impact de marché compris,""","""un multiplicateur sur vos coûts d'impact de marché (ni la demi-fourchette ni le courtage),""")
rep(""" · ${Math.round(bonRho(i,pf)*100)} % des salaires · moral →"""," · moral →")
s=s.replace("""function motTrho""","""function motTrho""")
open(p,"w",encoding="utf-8").write(s)
