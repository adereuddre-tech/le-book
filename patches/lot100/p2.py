# Lot 100b : l'apport vise juste sous le seuil (sinon il dépasse presque toujours la trésorerie de la société).
s=open('index.html',encoding='utf-8').read()
o=" const inj=Math.max(0,req/tg-nav);"
assert s.count(o)==1; s=s.replace(o," const inj=Math.max(0,req/(MGC.thr*0.98)-nav);")
open('index.html','w',encoding='utf-8').write(s);print('ok')
