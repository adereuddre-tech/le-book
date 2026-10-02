# Lot 150 : écran des annonces — l'objectif affiché et les promesses suivent l'objectif du trimestre ajusté au marché
# (lot 145), au lieu du mandat fixe de 3 %.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("p:`Vous annoncez ${pctc(0.15)} en un trimestre","p:`Vous annoncez ${pctc(0.15*gk)} en un trimestre")
rep(" const w=weights(S.k),sp=pvol(w),g=VOL().goal/4;\n const spD=Math.max(sp,0.04);"," const w=weights(S.k),sp=pvol(w),gk=goalK(),g=0.03*gk;\n const spD=Math.max(sp,0.04);")
rep("p:`Vous annoncez ${pctc(0.03)} sur le trimestre.","p:`Vous annoncez ${pctc(0.03*gk)} sur le trimestre.")
rep("p:`Vous annoncez ${pctc(0.09)}.","p:`Vous annoncez ${pctc(0.09*gk)}.")
rep("<div class=\"kv\"><span>Objectif trimestriel du mandat</span>","<div class=\"kv\"><span>Objectif du trimestre${gk>1.005||gk<0.995?` (mandat 3 %, ${gk>1?'relevé':'abaissé'} selon le marché)`:''}</span>")
rep("S.comm={id:o.id,nm:o.nm,ret:o.ret*goalK(),win:o.win,lose:o.lose};","S.comm={id:o.id,nm:o.nm,ret:o.ret,win:o.win,lose:o.lose};")
i=s.index("function screenComm(){");j=s.index("\n ];\n",i)
s=s[:j]+"\n ];\n opts.forEach(o=>{if(o.ret!=null)o.ret*=gk});   /* lot 150 */"+s[j+len("\n ];"):]
open('index.html','w',encoding='utf-8').write(s);print('lot150 ok')
