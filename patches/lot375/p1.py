p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# Page du budget : textes justes (impact, accidents), courts, le détail replié
rep("""  return `coûts ×${dec(EXECM[i],2)} · bruit des indicateurs""","""  return `impact ×${dec(EXECM[i],2)} · bruit des indicateurs""")
rep(""" if(id==='risk')return `incidents ×${dec(RISKM[i],2)} · gravité ×${dec(RISKS[i]/RISKS[3],2)} · choc des extrêmes ×${dec(0.5+0.5*TAILM[i],2)}`""",
    """ if(id==='risk')return `incidents ×${dec(RISKM[i],2)} · gravité ×${dec(RISKS[i]/RISKS[3],2)} · choc des extrêmes ×${dec(0.5+0.5*TAILM[i],2)} · accidents de levier ×${dec(Math.sqrt(TAILM[i]),2)}`""")
rep("""<b>Coûts</b> : chaque ordre coûte ${dec(EXECM[i],2)} fois le tarif de référence.""","""<b>Impact</b> : chaque ordre pousse le prix ${dec(EXECM[i],2)} fois comme au tarif de référence (la demi-fourchette ne change pas).""")
rep("""<b>Choc immédiat des événements extrêmes</b> ×${dec(0.5+0.5*TAILM[i],2)}.""","""<b>Choc immédiat des événements extrêmes</b> ×${dec(0.5+0.5*TAILM[i],2)}. <b>Accidents de levier</b> : fréquence ×${dec(Math.sqrt(TAILM[i]),2)}.""")
rep("""Moral du desk ${Math.round(motV())} : coûts d'exécution ×${dec(motC(),2)}""","""Moral du desk ${Math.round(motV())} : impact ×${dec(motC(),2)}""")
rep("""g:`coûts d'exécution ÷2 sur toute la classe""","""g:`coûts d'impact ÷2 sur toute la classe""")
rep("""   <p class="note" style="margin:2px 0 6px">Touchez une personne pour la recruter ou vous en séparer${b.id==='bo'?' ; sans personne, il reste le loyer':''}. Ce qu'elle apporte en propre n'existe que si elle est là ; les effets d'ensemble suivent la masse salariale. Recruter ne coûte que le salaire ; licencier coûte un demi-trimestre de salaire d'indemnité. Les salaires montent de 2 % par trimestre (×${dec(salInf(),2)} depuis le début du mandat).${b.id==='bo'&&redOn('budget')""",
    """   <p class="note" style="margin:2px 0 6px">Touchez une personne pour la recruter (son salaire) ou vous en séparer (un demi-trimestre d'indemnité).${b.id==='bo'&&redOn('budget')""")
rep("""<details style="margin-top:8px"><summary>À quoi sert ce budget · les ${b.lv.length} postes et niveaux</summary><p class="note">${b.d}</p>""",
    """<details style="margin-top:8px"><summary>À quoi sert ce budget · les ${b.lv.length} postes et niveaux</summary><p class="note">${b.d}</p><p class="note">Ce qu'une personne apporte en propre (son pouvoir, sa classe d'actifs) n'existe que si elle est là ; les effets d'ensemble suivent la masse salariale.${b.id==='bo'?' Sans personne, il reste le loyer.':''} Les salaires montent de 2 % par trimestre (×${dec(salInf(),2)} depuis le début du mandat).</p>""")
rep("""<p class="note" style="margin:2px 0 6px">Un seul lieu à la fois, du garage au yacht ; chaque adresse fait un peu mieux que son loyer, et reprend les avantages des précédentes. Déménager ne coûte rien de plus que le nouveau loyer ; les loyers suivent la taille du fonds (×${dec(offIdx(),2)} aujourd'hui, la racine de l'encours rapporté à celui de départ) ; le chiffre « budget » compte aussi l'effet des locaux sur le coût de l'équipe (le garage la fait 5 % moins chère).</p>""",
    """<p class="note" style="margin:2px 0 6px">Un seul lieu à la fois, du garage au yacht : chaque adresse reprend les avantages des précédentes et relève le moral. Déménager ne coûte que le nouveau loyer.</p>
  <details><summary>Loyers et budget</summary><p class="note">Les loyers suivent la taille du fonds : ×${dec(offIdx(),2)} aujourd'hui, la racine de l'encours rapporté à celui de départ. Le chiffre « budget » de chaque adresse compte aussi son effet sur le coût de l'équipe (le garage la fait 5 % moins chère).</p></details>""")
open(p,"w",encoding="utf-8").write(s)
s=open(p,encoding="utf-8").read()
rep("""La masse salariale fixe le niveau du desk sur toutes les classes et sur la macro : coûts d'exécution, bruit des indicateurs,""","""La masse salariale fixe le niveau du desk sur toutes les classes et sur la macro : impact de vos ordres, bruit des indicateurs,""")
rep("""(sans lui, vos ordres y passent par un courtier, commission et impact de marché multipliés)""","""(sans lui, vos ordres y passent par un courtier : impact ×${'$'}{dec(NOTRD,0)})""".replace("${'$'}","$") if False else """(sans lui, vos ordres y passent par un courtier : impact ×3)""")
rep("""Plus la masse salariale monte, plus les incidents sont rares et légers, plus le choc immédiat des extrêmes est amorti, et plus le comité est rassuré""","""Plus la masse salariale monte, plus les incidents et les accidents de levier sont rares, plus le choc immédiat des extrêmes est amorti, et plus le comité est rassuré""")
rep("""Tous les courtiers à deux rues : coûts d'exécution −7 %""","""Tous les courtiers à deux rues : impact −7 %""")
rep("""coûts −25 % sur l'Asie et les exotiques""","""impact −25 % sur l'Asie et les exotiques""")
open(p,"w",encoding="utf-8").write(s)
