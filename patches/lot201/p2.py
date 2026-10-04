# Lot 201b : en facile, les concurrents ne choisissent pas leur cran de budget (rivBud retiré) : avec leurs commissions,
# ils finissaient par s'offrir une meilleure équipe et devenaient plus forts qu'avant (7,3 → 8,7 % par trimestre).
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
rep("rivSkill:0.050,rivVol:0.95,rivBud:1,rivSeed:0.00025,","rivSkill:0.050,rivVol:0.95,rivSeed:0.00025,")
rep('[\"g\",\"concurrents moins adroits et peu capitalisés (0,25 M$ de trésorerie)\"]','[\"g\",\"concurrents moins adroits et peu capitalisés (0,25 M$ de trésorerie, équipe standard)\"]')
open('index.html','w',encoding='utf-8').write(s);print('lot201b ok')
