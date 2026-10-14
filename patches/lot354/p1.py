p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# dépenses croissantes : hurdle au taux des T-bills, loyer indexé sur la taille du fonds, salaires +2 %/trim.
rep("""function perfFee(){""","""function hurdleIdx(){return (S.hwmIdx||1)*(1+(S.rate||0)/4)}   /* lot 354 : la commission ne court qu'au-delà du plus haut relevé du taux des T-bills */
function perfFee(){""")
rep(""" const perfQ0=idxPre>S.hwmIdx?perfFee()*(idxPre-S.hwmIdx)/Math.max(1e-9,S.idx):0;""",""" const perfQ0=idxPre>hurdleIdx()?perfFee()*(idxPre-hurdleIdx())/Math.max(1e-9,S.idx):0;""")
rep(""" return ip>S.hwmIdx?lr-perfFee()*(ip-S.hwmIdx)/Math.max(1e-9,S.idx):lr}""",""" return ip>hurdleIdx()?lr-perfFee()*(ip-hurdleIdx())/Math.max(1e-9,S.idx):lr}""")
rep("""commission de performance (${(perfFee()*100).toFixed(0)} % au-dessus du plus haut historique)""","""commission de performance (${(perfFee()*100).toFixed(0)} % au-delà du plus haut historique relevé du taux des T-bills)""")
rep("""function offBp(){return OFF().bp}""","""function offIdx(){return Math.sqrt(Math.max(1,((S&&S.nav)||1)/((S&&S.aum0)||1)))}   /* lot 354 : un fonds qui grossit a besoin de place */
function salInf(){return Math.pow(1.02,(S&&S.q)||0)}   /* lot 354 : salaires +2 % par trimestre */
function offBp(){return OFF().bp*offIdx()}""")
rep("""function teamBp(f){return f*offFx('team')}""","""function teamBp(f){return f*offFx('team')*salInf()}""")
rep("""<span>${mm(OFF().bp*1e-4*budNav())} par trimestre</span>""","""<span>${mm(offBp()*1e-4*budNav())} par trimestre</span>""")
rep("""<span>${mm(o.bp*1e-4*budNav())} par trimestre""","""<span>${mm(o.bp*offIdx()*1e-4*budNav())} par trimestre""")
rep("""Déménager ne coûte rien de plus que le nouveau loyer ;""","""Déménager ne coûte rien de plus que le nouveau loyer ; les loyers suivent la taille du fonds (×${dec(offIdx(),2)} aujourd'hui, la racine de l'encours rapporté à celui de départ) ;""")
rep("""Recruter ne coûte que le salaire ; licencier coûte un demi-trimestre de salaire d'indemnité.""","""Recruter ne coûte que le salaire ; licencier coûte un demi-trimestre de salaire d'indemnité. Les salaires montent de 2 % par trimestre (×${dec(salInf(),2)} depuis le début du mandat).""")
rep("""capital de départ : 1 M$, plus celui de votre style\"""","""capital de départ : 0,8 M$, plus celui de votre style\"""")
rep("""capital de départ : 0,5 M$, plus celui de votre style\"""","""capital de départ : 0,4 M$, plus celui de votre style\"""")
rep("""après trois réussites, le coup du siècle""","""après trois manœuvres à mises croissantes, le coup du siècle""")
open(p,'w',encoding='utf-8').write(s)
