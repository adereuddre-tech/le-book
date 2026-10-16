p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# A1 : accident de levier toujours possible pour le joueur — p = (6 % + 14 %·(risque/limite)²) × contrôle des risques (racine) × sang-froid ;
#      perte = 0,65 × gravité × risque × foule × sang-froid (plafond 45 %) ; la marge garde sa probabilité, sa perte suit la même formule.
# A3 : la rentabilité estimée retranche le coût moyen des accidents.
rep("""function tailP(sp,std){if(!std)return 0;   /* lot 101 : le joueur passe aux événements extrêmes */""",
"""/* lot 368 : accidents du joueur, sans seuil — la fréquence monte avec le carré du risque rapporté à la limite, la gravité avec le risque */
const ACC={p0:0.06,p1:0.14,s:0.65,cap:0.45,hot:0.15};
function accRP(sp){if(!S||!S.bud)return 0;const x=sp/LIM.vol;return Math.min(0.6,(ACC.p0+ACC.p1*x*x)*Math.sqrt(tailMit(sp))*motS())}
function accLoss(sp,mgu,byMg,sev){const spE=byMg?Math.max(sp,0.20+0.5*((mgu||0)-MGZ.watch)):sp;return Math.min(ACC.cap,ACC.s*(sev==null?TAILSEV:sev)*spE*crowd(sp)*motS())}
function accExp(k,A){A=A||accP(k);return A.r*0.8*accLoss(A.sp,A.mgu,false)+A.m*0.8*accLoss(A.sp,A.mgu,true)}   /* coût moyen, sortie raisonnable */
function accHot(sp){return accRP(sp)>=ACC.hot}
function tailP(sp,std){if(!std)return accRP(sp);   /* lot 368 : le joueur retrouve ses accidents (lot 101 : supprimés) */""")
rep("""function accP(k){const sp=riskShown(weights(k)).total,a=tailP(sp),""","""function accP(k){const sp=riskShown(weights(k)).total,a=accRP(sp),""")
# tirage
rep("""  L=Math.min(ev.mg?0.60:0.55,(ev.sev[0]+(ev.sev[1]-ev.sev[0])*u())*tailL(spE)),good=u()<0.5;""",
    """  L=accLoss(sp,A.mgu,byMg,ev.sev[0]+(ev.sev[1]-ev.sev[0])*u()),good=u()<0.5;   /* lot 368 */""")
# rentabilité du fonds et rentabilité estimée
rep(""" const A=accP(k),sp=A.sp,spE=Math.max(sp,0.20+0.5*(A.mgu-MGZ.watch)),Lm=Math.min(0.6,TAILSEV*tailL(spE));
 let im=0;if(A.m>0)for(let m=0;m<N;m++){const d=Math.trunc(k[m]/2)-k[m];if(d)im+=tcost(d,m).cost*urgM(URG.tail,m)}
 const acc=-A.m*(0.8*Lm+Math.min(0.08,im/S.nav));""",
""" const A=accP(k),sp=A.sp;
 let im=0;if(A.p>0)for(let m=0;m<N;m++){const d=Math.trunc(k[m]/2)-k[m];if(d)im+=tcost(d,m).cost*urgM(URG.tail,m)}
 const acc=-(accExp(k,A)+A.p*Math.min(0.08,im/S.nav));   /* lot 368 : accidents du risque et de la marge */""")
rep("""function adjParts(k){k=k||S.k;const lect=profitBook(k)-xBookTerm(k),XM=xMoments(k),ext=XM.Pd*XM.E1,rc=-riskCost(k);return {total:lect+ext+rc,lect,ext,rc,pd:XM.Pd}}""",
    """function adjParts(k){k=k||S.k;const lect=profitBook(k)-xBookTerm(k),XM=xMoments(k),ext=XM.Pd*XM.E1,rc=-riskCost(k),acc=S&&S.bud?-accExp(k):0;return {total:lect+ext+rc+acc,lect,ext,rc,acc,pd:XM.Pd}}   /* lot 368 : coût moyen des accidents */""")
# affichages
rep(""" if(tailP(sp)>0)why.push(`accident de levier possible (${dec(tailP(sp)*100,0)} %)`);""",""" if(accHot(sp))why.push(`accident de levier probable (${dec(accRP(sp)*100,0)} %)`);""")
rep("""['Accident de levier ce trimestre',tailP(RS.total)>0?`${dec(tailP(RS.total)*100,0)} % · perte ≈ ${dec(TAILSEV*tailL(RS.total)*100,0)} %`:`aucun sous ${dec(TAIL.x0*50,0)} %`]""",
    """['Accident de levier ce trimestre',`${dec(accRP(RS.total)*100,0)} % · perte ≈ ${dec(accLoss(RS.total)*100,1)} %`]""")
rep(""" const hot=tailP(sp)>0,me=""",""" const hot=accHot(sp),me=""")
rep("""  const tp=tailP(sp);""","""  const tp=accRP(sp);""")
rep("""${tp>0?`À ${sv} de risque : <b class="neg-g">${dec(tp*100,0)} % de probabilité</b> d'un accident de levier ce trimestre, perte de l'ordre de ${dec(TAILSEV*tailL(sp)*100,0)} % de l'encours si vous le laissez courir.`:`Sous ${dec(TAIL.x0*50,1)} % de risque par trimestre, pas d'accident de levier possible.`}""",
    """À ${sv} de risque : <b class="${accHot(sp)?'neg-g':''}">${dec(tp*100,0)} % de probabilité</b> d'un accident de levier ce trimestre, perte de l'ordre de ${dec(accLoss(sp)*100,1)} % de l'encours si vous le laissez courir. Aucun book n'y échappe tout à fait : la fréquence monte avec le carré du risque, la perte avec le risque, et le sang-froid du desk joue sur les deux.""")
rep(""" if(tailP(RS.total)>0)flags+=`<div class="flag" style="border-color:var(--short)"><span><b>Zone d'accidents de levier.</b> À ${pct(RS.total)} de risque : ${dec(tailP(RS.total)*100,0)} % de probabilité d'un accident ce trimestre, perte de l'ordre de ${dec(TAILSEV*tailL(RS.total)*100,0)} % de l'encours""",
    """ if(accHot(RS.total))flags+=`<div class="flag" style="border-color:var(--short)"><span><b>Zone d'accidents de levier.</b> À ${pct(RS.total)} de risque : ${dec(accRP(RS.total)*100,0)} % de probabilité d'un accident ce trimestre, perte de l'ordre de ${dec(accLoss(RS.total)*100,1)} % de l'encours""")
rep("""  :tailP(sp)>0?t([""","""  :accHot(sp)?t([""")
rep("""Probabilité d'un accident de levier ce trimestre : ${Math.round(A.p*100)} %, nulle sous ${Math.round(MGZ.watch*100)} % de marge, ${Math.round(MGZ.pmax*100)} % au seuil d'appel.""",
    """Probabilité d'un accident de levier ce trimestre : ${Math.round(A.p*100)} % — ${Math.round(A.r*100)} % par le risque du book, jamais nul, et ${Math.round(A.m*100)} % par la marge, nul sous ${Math.round(MGZ.watch*100)} %, ${Math.round(MGZ.pmax*100)} % au seuil d'appel.""")
rep("""`Accident de levier : votre book tourne à ${pct(RQ(te.sp))} de risque. En dessous de ${dec(TAIL.x0*50,0)} %, il ne serait pas arrivé.`""",
    """`Accident de levier : votre book tourne à ${pct(RQ(te.sp))} de risque. Moins de risque l'aurait rendu plus rare et moins grave ; le sang-froid du desk (×${dec(motS(),2)}) pèse sur les deux.`""")
open(p,"w",encoding="utf-8").write(s)
