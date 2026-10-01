# Lot 123, p2 : embaucher doit rester rentable dans le pire cas (flux, difficile). Test apparié, 30 parties par variante :
# équipe standard contre aucune équipe — moyenne +11,0 ± 7,3 M$, mais médiane 4,5 contre 6,8 M$ et survie 53 % contre 63 %.
# Avec toutes les équipes 20 % moins chères : +14,5 ± 7,7 M$, médiane 6,7 contre 5,4 M$, survie 63 % des deux côtés.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("function budNav(){return Math.max(S.nav,S.aum0||S.nav)*((SIZE()&&SIZE().costM)||1)*(STYCOST[S.prof]||1)}",
    "const BUDK=0.80;   /* lot 123 : toutes les équipes 20 % moins chères */\nfunction budNav(){return Math.max(S.nav,S.aum0||S.nav)*((SIZE()&&SIZE().costM)||1)*(STYCOST[S.prof]||1)*BUDK}")
open('index.html','w',encoding='utf-8').write(s);print('lot123 p2 ok')
