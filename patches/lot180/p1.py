# Lot 180 : bonus d'équipe — cran par défaut au minimum ; Sœur Marie-Alpha et Onésime relèvent aussi le minimum
# (10 × le coût du cran de salle de marché atteint : Marie-Alpha 15 %, Onésime 25 %).
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("const BONOFF=[0,0.025,0.05,0.10,0.15],POACHP=0.5,MOT={i0:2};","const BONOFF=[0,0.025,0.05,0.10,0.15],POACHP=0.5,MOT={i0:0};")
rep("function bonBase(){if(!S||!S.bud)return 0;let t=-1;for(let p=Math.min(S.bud.fo,FOP.length-1);p>=0;p--)if(FOP[p].cls){t=p;break}return t>=0?10*FOP[t].bp*1e-4:0}",
    "function bonBase(){if(!S||!S.bud)return 0;const p=Math.min(S.bud.fo,FOP.length-1);return p>=0?10*FOP[p].bp*1e-4:0}")
rep("Le minimum vaut 10 fois le coût de vos traders sur 100 M$","Le minimum vaut 10 fois le coût de votre salle de marché sur 100 M$")
open('index.html','w',encoding='utf-8').write(s);print('lot180 ok')
