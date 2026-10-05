# Lot 215 : les investisseurs souscrivent en % de leur allocation initiale (et non de leur ligne actuelle) ; ils continuent
# de racheter en % de leur ligne actuelle. Allocation initiale : part de départ × encours de départ ; pour la Couronne,
# qui n'est pas là au départ, sa première ligne (mémorisée dans v.a0).
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
rep("function invD(id){return INVR.find(d=>d.id===id)}",
    "function invD(id){return INVR.find(d=>d.id===id)}\n/* lot 215 : base des souscriptions = allocation initiale */\nfunction invBase(v){const D=invD(v.id);if(D&&D.w0>0)return D.w0*S.aum0;if(!v.a0&&v.w>1e-9)v.a0=v.w*extNav();return v.a0||0}")
rep("  const f=invInF(D);if(f>0.002)r.sub=invFlow(v,f*v.w*extNav());else if(capStress()>0.5)r.full=1});",
    "  const f=invInF(D);if(f>0.002)r.sub=invFlow(v,f*invBase(v));else if(capStress()>0.5)r.full=1});   /* lot 215 */")
rep("if(f>0.002){r.sub+=invFlow(v,f*v.w*extNav());r.auto=1}else r.full=1}}   /* lot 122 */",
    "if(f>0.002){r.sub+=invFlow(v,f*invBase(v));r.auto=1}else r.full=1}}   /* lot 122 ; lot 215 : sur sa mise initiale */")
rep("souscrit d'office chaque trimestre, de 5 à 12,5 % de sa ligne selon la confiance","souscrit d'office chaque trimestre, de 5 à 12,5 % de sa mise initiale selon la confiance")
open('index.html','w',encoding='utf-8').write(s);print('lot215 ok')
s=open("index.html",encoding="utf-8").read()
rep("% de la ligne à confiance 50, proportionnellement à la confi","% de l'allocation initiale à confiance 50, proportionnellement à la confi")
open('index.html','w',encoding='utf-8').write(s);print('lot215b ok')
