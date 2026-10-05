# Lot 228 : page desk (ouverture et book) — « Objectif du trimestre » = l'objectif bonus, s'il existe (trimestres 1 et 2) ;
# l'objectif en % (annonce standard) et l'explication de ce que jugent les investisseurs sont retirés de ces deux écrans
# (l'objectif chiffré reste sur l'écran des promesses, où il sert).
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
i=s.index('function objRows(){');j=s.index('\nfunction ',i+5)
s=s[:i]+"""function objRows(){if(!S.goal)return '';   /* lot 228 : l'objectif bonus seul */
 return `<div class="flag" style="border-left:3px solid var(--gold)"><span>🎯 <b>Objectif du trimestre : ${S.goal.nm}</b> — ${S.goal.d} Bonus de ${moneyB(goalBon(S.goal))} sur votre score.</span></div>`}"""+s[j:]
rep("""`🎯 <b>Objectif du trimestre : ${sgnp(0.03*goalK(),1)} net</b> (annonce standard, ${goalK()>1.05?'relevé : le marché s\\'annonce agité':goalK()<0.95?'abaissé : le marché s\\'annonce calme':'normal'} ; vous pourrez promettre plus après le book).`,""","")
rep("...(S.goal?[`🏅 <b>Objectif bonus : ${S.goal.nm}</b> — ${S.goal.d} Bonus de ${moneyB(goalBon(S.goal))} sur votre score.`]:[])",
    "...(S.goal?[`🎯 <b>Objectif du trimestre : ${S.goal.nm}</b> — ${S.goal.d} Bonus de ${moneyB(goalBon(S.goal))} sur votre score.`]:[])")
open('index.html','w',encoding='utf-8').write(s);print('lot228 ok')
