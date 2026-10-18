p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# Taux de bonus : les crans composent au lieu de multiplier — taux = 1 − (1 − minimum)^cran. Petit minimum : ≈ cran × minimum, comme avant ;
# gros minimum (équipe pleine) : progression régulière jusqu'à près de 100 %, sans plafond qui écrase les crans.
rep("const BONK={fo:2.5,bo:10,max:0.9,floor:0.01};","const BONK={fo:2.5,bo:10,max:0.95,floor:0.01};   /* lot 380 : max = plafond du minimum seul */")
rep("function bonRate(i){return Math.min(BONK.max,bonBase()*BONOFF[i])}","function bonRate(i){return 1-Math.pow(1-bonBase(),BONOFF[i])}   /* lot 380 : 1 − (1 − minimum)^cran, jusqu'à 100 % */")
rep("Crans : ×1, 1,25, 1,5, 2, 2,5 et 4, sans jamais dépasser 90 % de la commission.","Crans : ×1, 1,25, 1,5, 2, 2,5 et 4, composés — taux = 1 − (1 − minimum)<sup>cran</sup> : un petit minimum est multiplié presque tel quel, un gros se rapproche régulièrement de 100 %.")
rep("Chaque cran le multiplie, jusqu'au 🔥, hors de prix.","Chaque cran le relève, jusqu'au 🔥, hors de prix, qui approche 100 % avec une équipe pleine.")
open(p,"w",encoding="utf-8").write(s)
