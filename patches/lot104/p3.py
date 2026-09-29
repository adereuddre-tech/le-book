# Lot 104, p3 : recalibration. Campagne 225 parties (bot, normal 90 appariées contre le lot 101, difficile 45) :
# score inchangé (−0,6 ± 1,9 M$), mais survie 79 % en normal (64 % au lot 101) et 71 % en difficile, pour des cibles de
# 70 % et 60 % ; rachats cumulés 21 M$ contre 70 M$ au lot 101. Avis de rachat plus lourds : 30 % + 70 % de l'écart.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("const INVP={n0:0.20,nk:0.60,","const INVP={n0:0.30,nk:0.70,")
open('index.html','w',encoding='utf-8').write(s);print('lot104 p3 ok')
