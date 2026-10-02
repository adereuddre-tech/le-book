# Lot 162 : moyen — capital de départ retiré (0,15 M$ → 0, le bonus de style reste), équipe ramenée à ×1,10 (×1,20 sans effet).
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("goalMult:1,costM:1.20,seed:0.00015}","goalMult:1,costM:1.10,seed:0}")
rep("[\"g\",\"capital de départ : 0,15 M$, plus celui de votre style\"]","[\"b\",\"pas de capital de départ au-delà de celui de votre style ; équipe 10 % plus chère\"]")
open('index.html','w',encoding='utf-8').write(s);print('lot162 ok')
