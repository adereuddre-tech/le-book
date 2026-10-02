# Lot 143 : graphique de performance — le cumul comptait deux fois le trimestre sur l'écran de résultat (phase encore
# « events », P&L vivant ajouté au trimestre déjà clos : +17,6 % affiché +41,7 %). Drapeau S.qClosed.
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("now:cur*(1+((S.phase==='events'&&S.live)?liveNet():0))/v*100","now:cur*(1+((S.phase==='events'&&S.live&&!S.qClosed)?liveNet():0))/v*100")
rep("S.navs.push(S.nav);S.rets.push(qTotal);","S.navs.push(S.nav);S.rets.push(qTotal);S.qClosed=true;")
rep("S.pendingTC=0;S.freeAdjUsed=false;S.live=false;","S.pendingTC=0;S.freeAdjUsed=false;S.live=false;S.qClosed=false;")
open('index.html','w',encoding='utf-8').write(s);print('lot143 ok')
