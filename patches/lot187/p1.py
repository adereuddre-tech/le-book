# Lot 187 : bonus d'équipe — effet doublé, de ×1,20 (minimum) à ×0,80 (+15 pts). Il s'applique à tout le coût d'un ordre :
# fourchette et impact de marché (tcost multiplie la somme des deux).
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("const BONFX=[{c:1.10,p:0.50},{c:1.05,p:0.40},{c:1.00,p:0.30},{c:0.94,p:0.20},{c:0.90,p:0.12}],BONCUT=1.5;","const BONFX=[{c:1.20,p:0.50},{c:1.10,p:0.40},{c:1.00,p:0.30},{c:0.88,p:0.20},{c:0.80,p:0.12}],BONCUT=1.5;")
rep("un multiplicateur sur tous vos coûts d'exécution (×1,10 à 5 %, ×0,90 à 20 %)","un multiplicateur sur tous vos coûts d'exécution, fourchette et impact de marché compris (×1,20 au minimum, ×0,80 au cran le plus haut)")
open('index.html','w',encoding='utf-8').write(s);print('lot187 ok')
