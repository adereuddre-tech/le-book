# Lot 172 : retouches d'équilibrage proposées après la campagne de contrôle du lot 171 (270 parties + 180 graines neuves) :
# survie des trois styles à égalité (≈ 74 %) au lieu de quant 79 > fondamental 76 > flux 63, difficile à 67 % pour 60 % visé.
# Flux : coût des incidents ×2,8 (×2,2) ; difficile : équipe ×1,75 (×1,60).
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("incMult:1.70,incSev:2.2,","incMult:1.70,incSev:2.8,")
rep("goalMult:1,costM:1.60,seed:0}","goalMult:1,costM:1.75,seed:0}")
rep("équipe 60 % plus chère","équipe 75 % plus chère")
open('index.html','w',encoding='utf-8').write(s);print('lot172 ok')
s=open('index.html',encoding='utf-8').read()
rep("incidents plus fréquents (×1,70) et deux fois plus chers","incidents plus fréquents (×1,70) et presque trois fois plus chers")
open('index.html','w',encoding='utf-8').write(s);print('lot172 p1b ok')
