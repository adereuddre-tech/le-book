# Lot 127 : difficile, équipe ×1,60 (×1,50). Tests croisés en flux difficile (25 graines appariées par équipe) :
# aucune équipe 17,6 M$ (médiane 12,8, survie 68 %) ; légère +11,8 ± 7,6 (médiane +3,2, survie 76 %) ;
# standard +14,9 ± 5,7 (médiane +6,7, survie 72 %) ; maximale +19,0 ± 11,7 (médiane +1,0, survie 56 %).
# Embaucher reste rentable ; l'équipe maximale paie en moyenne mais pas pour le joueur médian.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("goalMult:1,costM:1.50,seed:0}","goalMult:1,costM:1.60,seed:0}")
rep("équipe 50 % plus chère","équipe 60 % plus chère")
open('index.html','w',encoding='utf-8').write(s);print('lot127 p1 ok')
