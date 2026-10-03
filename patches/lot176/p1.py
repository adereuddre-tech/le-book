# Lot 176 : coûts des traders et du back office figés à leur coût pour un fonds de 100 M$ (l'encours de départ) : ils ne
# suivent plus l'encours, ni à la hausse ni à la baisse. Avant : facturés sur max(encours, encours de départ).
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("function budNav(){return Math.max(S.nav,S.aum0||S.nav)*((SIZE()&&SIZE().costM)||1)*(STYCOST[S.prof]||1)*BUDK}",
    "function budNav(){return (S.aum0||0.1)*((SIZE()&&SIZE().costM)||1)*(STYCOST[S.prof]||1)*BUDK}   /* lot 176 : base fixe, l'encours de départ */")
rep("Les salaires sont facturés sur ${moneyB(budNav())} tant que l'encours reste sous son niveau de départ : alléger l'équipe coûte le versement du bonus aux partants.",
    "Les salaires sont fixes, quel que soit l'encours : alléger l'équipe coûte le versement du bonus aux partants.")
open('index.html','w',encoding='utf-8').write(s);print('lot176 ok')
s=open('index.html',encoding='utf-8').read()
rep("document.getElementById('btot').textContent=`${bp.toFixed(0)} pb · ${mm(bp*1e-4*budNav())} · ${dec((bp*4/100),1)} % par an",
    "document.getElementById('btot').textContent=`${bp.toFixed(0)} pb de 100 M$ · ${mm(bp*1e-4*budNav())} · ${dec(bp*1e-4*budNav()*4/Math.max(1e-9,S.nav)*100,1)} % de l'encours par an")
open('index.html','w',encoding='utf-8').write(s);print('lot176 p1b ok')
