p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)

# Couronne : suit la majorité (au moins deux des quatre) et ne rachète jamais après un trimestre positif
rep("""vdMin=Math.min(...vds);""","""vdMin=Math.min(...vds),vdRoy=o.r>0?(vds.every(x=>x>0)?1:0):(vds.filter(x=>x<0).length>=2?-1:vds.every(x=>x>0)?1:0);   /* lot 340 */""")
rep("""vd:v.id==='roy'?vdMin:invVerdict(v.id,S.invH)""","""vd:v.id==='roy'?vdRoy:invVerdict(v.id,S.invH)""")
rep("""if(r.vd>0||(v.id==='cr'&&o.r>0)){r.cancel=true;v.ntc=0}""","""if(r.vd>0||((v.id==='cr'||v.id==='roy')&&o.r>0)){r.cancel=true;v.ntc=0}""")
rep("""crit:'Le plus sévère',royal:1,""","""crit:'La majorité',royal:1,""")
rep("""en plus, elle se règle sur le plus sévère des quatre autres : elle rachète dès que l'un d'eux rachète (au taux le plus fort, 27,5 %), et souscrit encore si tous souscrivent.""",
    """en plus, elle suit les quatre autres : elle rachète si au moins deux d'entre eux rachètent (au taux le plus fort, 27,5 %), jamais après un trimestre positif, et souscrit encore si tous souscrivent.""")
rep(""""La Couronne du Farghestan suit le plus inquiet de vos investisseurs : elle réduit sa ligne.\"""",""""Au moins deux de vos investisseurs rachètent : la Couronne du Farghestan les suit et réduit sa ligne.\"""")
rep("""et elle se réglera sur le plus sévère de vos investisseurs.""","""et elle suivra vos investisseurs dès que deux d'entre eux s'inquiètent.""")
open(p,'w',encoding='utf-8').write(s)
