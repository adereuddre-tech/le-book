# Lot 165 : charges factorielles des taux européens, proposition d'Antoine (échelle −3…+3, un cran = 0,20 ; affichage
# Croissance, Inflation, Liquidité, Appétit ; liquidité = −dollar en interne). Bund, valeur refuge : −1 −3 0 −2 ;
# Gilt : −2 −2 +1 −2 ; OAT, prime de spread (appétit positif) : −1 −3 −1 +1.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("sig:0.060, s:0.35, c:0.30, b:[-0.16,-0.58, 0.34,-0.58],","sig:0.060, s:0.35, c:0.30, b:[-0.20,-0.60, 0.00,-0.40],")
rep("sig:0.070, s:0.55, c:0.50, b:[-0.34,-0.52, 0.24,-0.44],","sig:0.070, s:0.55, c:0.50, b:[-0.40,-0.40,-0.20,-0.40],")
rep("sig:0.065, s:0.60, c:0.55, b:[-0.20,-0.58, 0.26, 0.25],","sig:0.065, s:0.60, c:0.55, b:[-0.20,-0.60, 0.20, 0.20],")
open('index.html','w',encoding='utf-8').write(s);print('lot165 ok')
