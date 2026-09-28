# Lot 98b : la pop-up de trésorerie montre aussi, au débriefing, les deux déductions choisies.
s=open('index.html',encoding='utf-8').read()
o="[`<b>Trésorerie disponible</b>`,`<b class=\"${mgrCash()>=0?'gold-g':'neg-g'}\">${mm(mgrCash())}</b>`]]"
assert s.count(o)==1
s=s.replace(o,o[:-1]+",...(bonPend()+coPend()>0?[[`Bonus d'équipe choisi`,`<b class=\"neg-g\">−${mm(bonPend())}</b>`],[`Co-investissement du prochain trimestre`,`<b class=\"neg-g\">−${mm(coPend())}</b>`],[`<b>Après vos choix</b>`,`<b class=\"${cashView()>=0?'gold-g':'neg-g'}\">${mm(cashView())}</b>`]]:[])]")
open('index.html','w',encoding='utf-8').write(s);print('ok')
