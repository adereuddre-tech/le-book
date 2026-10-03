# Lot 169 : Bund — aucune charge nulle : liquidité −1 (il profite des resserrements de liquidité, valeur refuge).
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("sig:0.060, s:0.35, c:0.30, b:[-0.20,-0.60, 0.00,-0.40],","sig:0.060, s:0.35, c:0.30, b:[-0.20,-0.60, 0.20,-0.40],")
open('index.html','w',encoding='utf-8').write(s);print('lot169 ok')
