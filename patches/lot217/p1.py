# Lot 217 : aucune dépêche au-delà de 80 % de chances de se poursuivre. Probabilité réelle tirée dans [0,40 ; 0,80]
# (au lieu de [0,40 ; 0,90]) ; lecture du desk bornée à 80 % (au lieu de 90 %). Les extrêmes restent dans [0,35 ; 0,65].
# Seuils des concurrents recalibrés sur cette loi (mêmes fréquences visées : ~21 / ~45 / ~75 %) : 1,0 / 0,6 / 0,25.
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
rep(":{p:0.40+0.50*rng(),m:[0.45+0.40*rng(),-(0.30+0.40*rng())]};   /* poursuite dans [0,40 ; 0,90] */",
    ":{p:0.40+0.40*rng(),m:[0.45+0.40*rng(),-(0.30+0.40*rng())]};   /* poursuite dans [0,40 ; 0,80] (lot 217) */")
rep("S.sc.ph=ver?S.sc.p:Math.max(0.10,Math.min(0.90,S.sc.p+sh+sd*gauss()));","S.sc.ph=ver?S.sc.p:Math.max(0.10,Math.min(0.80,S.sc.p+sh+sd*gauss()));   /* lot 217 : 80 % au plus */")
rep("const RIVTH={syst:1.2,fonda:0.7,flux:0.3},","const RIVTH={syst:1.0,fonda:0.6,flux:0.25},   /* lot 217 : recalibrés (poursuite ≤ 80 %) */\n ")
open('index.html','w',encoding='utf-8').write(s);print('lot217 ok')
