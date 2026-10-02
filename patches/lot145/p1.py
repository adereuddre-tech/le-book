# Lot 145 : l'objectif du trimestre suit l'intensité des facteurs macro, autour de 3 % : ×0,80 (marché calme) à ×1,25
# (marché agité), selon la norme du vecteur factoriel du trimestre. Annonces forte et gourou au même prorata.
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("S.pendingTC=0;S.freeAdjUsed=false;S.live=false;S.qClosed=false;","S.pendingTC=0;S.freeAdjUsed=false;S.live=false;S.qClosed=false;S.goalK=null;")
rep("function objRows(){","function goalK(){if(S.goalK==null){const f=S.f||[0,0,0,0],I=Math.sqrt(f.reduce((a,x)=>a+x*x,0)/4);S.goalK=Math.max(0.80,Math.min(1.25,0.70+0.45*I))}return S.goalK}   /* lot 145 */\nfunction objRows(){")
rep("S.comm={id:o.id,nm:o.nm,ret:o.ret,win:o.win,lose:o.lose};","S.comm={id:o.id,nm:o.nm,ret:o.ret*goalK(),win:o.win,lose:o.lose};")
rep("🎯 <b>Objectif du trimestre : ${sgnp(0.03,1)} net</b> (annonce standard ; vous pourrez promettre plus après le book).","🎯 <b>Objectif du trimestre : ${sgnp(0.03*goalK(),1)} net</b> (annonce standard, ${goalK()>1.05?'relevé : le marché s\\'annonce agité':goalK()<0.95?'abaissé : le marché s\\'annonce calme':'normal'} ; vous pourrez promettre plus après le book).")
rep("const tg=S.comm&&S.comm.ret!=null?S.comm.ret:VOL().goal/4;","const tg=S.comm&&S.comm.ret!=null?S.comm.ret:0.03*goalK();")
open('index.html','w',encoding='utf-8').write(s);print('lot145 ok')
