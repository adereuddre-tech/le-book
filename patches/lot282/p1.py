p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
rep("function bonBase(){if(!S||!S.bud)return 0;const p=Math.min(S.bud.fo,7);   /* lot 279 : base plafonnée au cran d'Onésime */return p>=0?10*FOP[p].bp*1e-4:0}   /* lot 179 */",
    "function bonBase(){if(!S||!S.bud)return 0;const p=Math.min(S.bud.fo,FOP.length-1);return p>=0?5*FOP[p].bp*1e-4:0}   /* lot 282 : 5 fois le coût du front office en pb, sans plafond */")
rep("Le minimum vaut 10 fois le coût de votre salle de marché sur 100 M$","Le minimum vaut 5 fois le coût de votre front office sur 100 M$")
open(p,'w',encoding='utf-8').write(s)
