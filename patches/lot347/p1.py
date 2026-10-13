p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# F1 : plus de « financement du levier » fictif — sur des futures, le seul coût est le collatéral déposé en marge, déjà compté
rep("""/* lot 80 : le prime broker finance le levier à un coût qui croît comme le carré du risque — même barème pour tous */
const FINK=0.006;""","""/* lot 80 : le prime broker finance le levier à un coût qui croît comme le carré du risque — même barème pour tous.
   lot 347 : supprimé (FINK = 0). Sur des futures, le seul coût du levier est le collatéral déposé en marge, déjà compté. */
const FINK=0;""")
rep("""Rentabilité : rendement attendu du trimestre — collatéral, impact, financement du levier compris ;""","""Rentabilité : rendement attendu du trimestre — collatéral (et ce que la marge lui retire), impact compris ;""")
rep("""/* lot 85 : lecture des marchés, moins le financement facturé ; ni accidents ni drain ; lot 337 : l'extrême signalé */""","""/* lot 85 : lecture des marchés ; ni accidents ni drain ; lot 337 : l'extrême signalé ; lot 347 : plus de financement fictif */""")
open(p,'w',encoding='utf-8').write(s)
