# Lot 236 : frein à la croissance — démarrage à 200 M$ (et non à l'encours de départ), sans multiplicateur d'impact
# (IMPC 1,5 → 1), puissance 0,35 conservée : facture × (encours / 200 M$)^0,35 au-delà de 200 M$ ; ×1 en dessous.
# 500 M$ : ×1,38 ; 1 Md$ : ×1,76 ; 2 Md$ : ×2,24. Seuil absolu : un fonds parti de 50 M$ ou de 400 M$ (tailles) est freiné
# au-delà des mêmes 200 M$.
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
rep("const IMPC=1.5;","const IMPC=1;   /* lot 236 : sans multiplicateur */\nconst BRK0=0.2;   /* lot 236 : seuil du frein, 200 M$ */")
rep("function brake(A){const a0=(S&&S.aum0)||0.1;return Math.pow(Math.max(1,(A===undefined?S.nav:A)/a0),BRK)}",
    "function brake(A){return Math.pow(Math.max(1,(A===undefined?S.nav:A)/BRK0),BRK)}")
open('index.html','w',encoding='utf-8').write(s);print('lot236 ok')
