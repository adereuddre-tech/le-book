# Lot 94 : pas de co-investissement au premier trimestre (trésorerie de départ = commission de gestion, 500 k$) ;
# barème du front office 0/10/25/45/70/100/150 pb ; « indemnités » → « versement du bonus ».
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("const tg=coinvPct()*Math.max(0,mgrCash());","const tg=S.q>=1?coinvPct()*Math.max(0,mgrCash()):0;   /* lot 94 : rien au premier trimestre */\n ")
for a,b in [('ic:"📞",bp:50','ic:"📞",bp:45'),('ic:"🛢️",bp:75','ic:"🛢️",bp:70'),('ic:"🐉",bp:120','ic:"🐉",bp:100'),('ic:"📿",bp:200','ic:"📿",bp:150')]: rep(a,b)
rep("/* budget du trimestre + indemnités,","/* budget du trimestre + bonus versés aux partants,")
rep("${S.qSevM>0?` · indemnités ${mm(S.qSevM)}`:''}`;","${S.qSevM>0?` · bonus versés aux partants ${mm(S.qSevM)}`:''}`;")
rep("${i1<i0&&S.qSevM>0?` · indemnités ${mm(S.qSevM)}`:''}","${i1<i0&&S.qSevM>0?` · versement du bonus ${mm(S.qSevM)}`:''}")
rep("les indemnités quand vous licenciez.","le bonus versé à ceux qui partent quand vous baissez d'un cran.")
rep("[`Part placée en ce moment`,`aucune, trimestre clos`]","[`Part placée en ce moment`,S.q===0?`aucune au premier trimestre`:`aucune, trimestre clos`]")
open('index.html','w',encoding='utf-8').write(s);print('ok')
