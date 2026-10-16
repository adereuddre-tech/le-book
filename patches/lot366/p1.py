p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# D1 : débauchage plus raide selon le moral (85, 55, 25, 8, 0 % par trimestre) ; D2 : courtier ×3, contre-offre plus chère quand le moral est bas
rep("const BONFX=[{c:1.60,p:0.70},{c:1.30,p:0.45},{c:1.00,p:0.30},{c:0.75,p:0.15},{c:0.45,p:0.03}]",
    "const BONFX=[{c:1.60,p:0.85},{c:1.30,p:0.55},{c:1.00,p:0.25},{c:0.75,p:0.08},{c:0.45,p:0}]")   # lot 366
rep("function motP(m){return mclp(motI(BONFX.map(f=>f.p),motX(m)),0.03,0.7)}","function motP(m){return mclp(motI(BONFX.map(f=>f.p),motX(m)),0,0.9)}   /* lot 366 */")
rep("NOTRD=2,   /* lot 259 : courtier ×2 (×4 avant) */","NOTRD=3,   /* lot 366 : courtier ×3 (lot 259 : ×2) */")
rep("function cntCost(p){return Math.round(CNTK*(FOP[p].bp-FOP[p-1].bp))}",
    "function cntMot(){return mclp(1+(50-motV())/50,1,2)}   /* lot 366 : sous 50 de moral, la contre-offre coûte plus cher, jusqu'à ×2 à 0 */\nfunction cntCost(p){return Math.round(CNTK*(FOP[p].bp-FOP[p-1].bp)*cntMot())}")
rep("l'ordre passe par un courtier, ×2.","l'ordre passe par un courtier, ×3.")
rep("débauchage 3 %, et il refuse toutes les offres","débauchage 0 %, et il refuse toutes les offres")
rep("Contre-offre : son salaire plus une prime de retour, ${cntCost(G.p)} pb au total",
    "Contre-offre : son salaire plus une prime de retour${cntMot()>1.005?`, ×${dec(cntMot(),2)} avec un moral à ${Math.round(motV())}`:''}, ${cntCost(G.p)} pb au total")
open(p,"w",encoding="utf-8").write(s)
