p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
rep(""" const tgM=cruise()*(PROF().modelScale||1);   /* lot 286 */""",""" const tgM=cruise()*(PROF().deskScale||PROF().modelScale||1);   /* lot 286 ; lot 288 : flux et activiste, book du desk plus prudent */""")
rep("incMult:1.70,incSev:2.2,numeric:false,freeAdj:true,hunch:true}","incMult:1.70,incSev:2.2,numeric:false,freeAdj:true,hunch:true,deskScale:0.6}")
rep("incMult:1.2,incSev:1.3,numeric:false,atk:true}","incMult:1.2,incSev:1.3,numeric:false,atk:true,deskScale:0.75}")
open(p,'w',encoding='utf-8').write(s)
