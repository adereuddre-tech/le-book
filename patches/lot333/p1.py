p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# positions visibles : seuil 2 % du carnet et jamais sous ±3 unités
rep("""const VIS={thr:0.01,""","""const VIS={thr:0.02,kMin:3,""")
rep("""if(!k[i])continue;const f=footprint(i,k);if(f<VIS.thr)continue;""","""if(Math.abs(k[i])<VIS.kMin)continue;const f=footprint(i,k);if(f<VIS.thr)continue;""")
rep("""Une ligne devient visible au-delà de ${Math.round(VIS.thr*100)} % de la profondeur de son carnet (les marchés étroits d'abord, et tous quand le fonds grossit).""",
    """Une ligne devient visible à partir de ±${VIS.kMin} unités et au-delà de ${Math.round(VIS.thr*100)} % de la profondeur de son carnet (les marchés étroits d'abord, et tous quand le fonds grossit).""")
rep("""au-delà de ${Math.round(VIS.thr*100)} %, elle est déclarée et tout le marché la voit.""","""à partir de ±${VIS.kMin} unités et au-delà de ${Math.round(VIS.thr*100)} %, elle est déclarée et tout le marché la voit.""")
rep("""/* lot 275 : visibilité. L'empreinte d'une ligne est son notionnel rapporté à la profondeur du carnet. Au-delà de 1 % :""",
    """/* lot 275 : visibilité. L'empreinte d'une ligne est son notionnel rapporté à la profondeur du carnet. Au-delà de 2 % et à partir de ±3 (lot 333) :""")
open(p,'w',encoding='utf-8').write(s)
