# Lot 91b : courtage cumulé = ce que mgrNet compte (facturé à la clôture au NAV de début + en cours),
# S.totalTC dérivait de quelques k$ avec le NAV et laissait un résidu « Autres » de signe faux.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:80]); s=s.replace(o,n)
rep('led:1,cMgmt:0,','led:1,cTC:0,cMgmt:0,')
rep('S.mgrCosts+=tc*navBefore;','S.mgrCosts+=tc*navBefore;S.cTC=(S.cTC||0)+tc*navBefore;')
rep("const tcNow=S.phase==='book'?liveTC():0;","const tcNow=S.phase==='book'?liveTC():(S.pendingTC||0)*S.nav,tcAll=S.led?(S.cTC||0)+tcNow:(S.totalTC||0)+(S.phase==='book'?liveTC():0);")
rep("[`Courtage de vos ordres${tcNow?' (dont en préparation)':''}`,-((S.totalTC||0)+tcNow)]","[`Courtage de vos ordres${tcNow?' (dont trimestre en cours −'+mm(tcNow)+')':''}`,-tcAll]")
open('index.html','w',encoding='utf-8').write(s);print('ok')
