# Lot 218 : le Liquidistan devient le Farghestan ; derniers « comité ±n » / « investisseurs ±n » affichés passés en confiance
# (choix des événements du conseil désormais lus par fxTxt, trophée « Main chaude », rivalité « ne pas répondre »,
# effet du cran de risque au budget).
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
rep("La holding de la famille royale du Liquidistan, émirat pétrolier et fiscal, prend un gros ticket.","La holding de la famille régnante du Farghestan, puissance lointaine et fortunée de l'autre rive, prend un gros ticket.")
s=s.replace("Liquidistan","Farghestan")
rep("<span>${c.s}${boardFx(c.e)}","<span>${fxTxt(c.s,c.e)}${boardFx(c.e)}")
rep("encours) · investisseurs +4`","encours) · confiance +4`")
rep("Vous ne changez rien. Investisseurs −1,5 de plus : ils voulaient une réaction.","Vous ne changez rien. Confiance −1,5 de plus : vos investisseurs voulaient une réaction.")
rep("` · comité ${RISKRC[i]>0?'+':'−'}${dec(Math.abs(RISKRC[i]),1)} par trimestre`","` · confiance ${RISKRC[i]>0?'+':'−'}${dec(Math.abs(RISKRC[i]*CFW),1)} par trimestre`")
open('index.html','w',encoding='utf-8').write(s);print('lot218 ok')
