# Lot 158 : taux de bonus d'équipe — chaque cran affiche le multiplicateur du seul bonus, pas cumulé avec la salle de marché.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("{const F=BONFX[pf>0?i:0],c=e*F.c;","{const F=BONFX[pf>0?i:0],c=F.c;")
rep("coûts d'exécution ×${dec(BONFX[bonEff()].c,2)} · avec votre salle de marché ×${dec(execMot(),2)}","coûts d'exécution ×${dec(BONFX[bonEff()].c,2)} (effet du seul bonus)")
open('index.html','w',encoding='utf-8').write(s);print('lot158 ok')
