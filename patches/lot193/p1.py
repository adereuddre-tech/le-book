# Lot 193 : concurrents à coûts d'équipe fixes, comme le joueur (lot 176). Leur budget (RIVBP, pb) se payait sur l'encours
# du moment (rivalCostQ × mAum) : un concurrent qui grossissait payait son équipe plus cher, un concurrent qui fondait la
# payait moins. Désormais la masse salariale est figée sur l'encours de départ (S.aum0) ; seule la facture d'ordres type
# (16 pb) reste proportionnelle à l'encours. Même règle dans le choix du cran de budget (rivBudget).
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("function rivalCostQ(rv){const L=(rv&&rv.bl)||3;return (RIVBP[L]+16)*1e-4}",
    "function rivalCostQ(rv){const L=(rv&&rv.bl)||3;return (RIVBP[L]+16)*1e-4}\n/* lot 193 : équipe figée sur l'encours de départ, facture d'ordres (16 pb) sur l'encours du moment */\nfunction rivalCostAmt(rv,A){const L=(rv&&rv.bl)||3;return RIVBP[L]*1e-4*(S.aum0||A)+16e-4*A}")
rep("for(let L=4;L<=6;L++){const dc=rivalCostQ({bl:L})-c3;\n  if(cash<2*dc*A)break;",
    "for(let L=4;L<=6;L++){const dc=(rivalCostQ({bl:L})-c3)*(S.aum0||A)/A;   /* lot 193 : surcoût d'équipe fixe */\n  if(cash<2*dc*A)break;")
rep("cost=rivalCostQ(rv)*rv.mAum,ci=","cost=rivalCostAmt(rv,rv.mAum),ci=")
open('index.html','w',encoding='utf-8').write(s);print('lot193 ok')
