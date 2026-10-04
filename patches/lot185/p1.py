# Lot 185 : rappel de l'objectif sur la page du book — il affichait toujours 3 % (objectif du mandat) au lieu de l'objectif
# ajusté au marché du trimestre (goalK).
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("function objRows(){const g=VOL().goal/4,","function objRows(){const g=0.03*goalK(),")
rep("(annonce standard)`}","(annonce standard${goalK()>1.005?', relevé : marché agité':goalK()<0.995?', abaissé : marché calme':''})`}") if s.count("(annonce standard)`}")==1 else None
open('index.html','w',encoding='utf-8').write(s);print('lot185 ok')
