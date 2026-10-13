p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# Dwight et Boris : un marché annoncé à 90 %, comme Ingrid et Tuco (eux aussi à 90 %)
rep("""{id:'dw',fo:1,ic:'📞',nm:'Dwight',t:"Un bloc à la voix",d:"Vos ordres sur les actions passent sans impact de marché tout le trimestre : seule la fourchette est due."}""",
    """{id:'dw',fo:1,ic:'📞',nm:'Dwight',info:1,t:"Le carnet de Wall Street",d:"Il vous dit dans quel sens finira le marché d'actions le plus parlant ce trimestre. Juste neuf fois sur dix : il connaît tous les vendeurs de la place."}""")
rep("""{id:'ig',fo:2,ic:'🏦',nm:'Ingrid',info:1,t:"Lire l'adjudication",d:"Elle vous dit dans quel sens finira le marché de taux le plus parlant ce trimestre. Juste quatre fois sur cinq."}""",
    """{id:'ig',fo:2,ic:'🏦',nm:'Ingrid',info:1,t:"Lire l'adjudication",d:"Elle vous dit dans quel sens finira le marché de taux le plus parlant ce trimestre. Juste neuf fois sur dix."}""")
rep("""{id:'bo',fo:3,ic:'🤖',nm:'Boris',t:"L'algorithme en urgence",d:"Surcoût d'urgence divisé par trois sur les devises ce trimestre (dépêches, extrêmes, rivalités)."}""",
    """{id:'bo',fo:3,ic:'🤖',nm:'Boris',info:1,t:"Le modèle de change",d:"Il vous dit dans quel sens finira la devise la plus parlante ce trimestre. Juste neuf fois sur dix : son modèle a vu passer les flux."}""")
rep("""Il vous dit dans quel sens finira la matière première la plus parlante ce trimestre. Juste 85 fois sur 100 : les cuves ne mentent pas.""",
    """Il vous dit dans quel sens finira la matière première la plus parlante ce trimestre. Juste neuf fois sur dix : les cuves ne mentent pas.""")
rep("""function urgM(m,i){if(pwOn('bo')&&INSTR[i].grp==='Devises'&&m>1)m=1+(m-1)/3;return""","""function urgM(m,i){return""")
rep(""" if(pwOn('dw')&&x.grp==='Actions')return {cost:spr,bp:spr/bn*1e4,bn,spr,imp:0};   /* lot 268 : Dwight, sans impact */
""","")
rep("""const PWTIP=""","""const PWTIP=""",0)
rep("""  const t=pwTip(id==='ig'?'Taux':'Matières premières',id==='ig'?0.80:0.85,o.nm);""","""  const t=pwTip(PWTIP[id],0.90,o.nm);""")
rep("""function pwTip(cls,rel,who){""","""const PWTIP={ig:'Taux',tu:'Matières premières',dw:'Actions',bo:'Devises'};   /* lot 330 : quatre tuyaux à 90 % */
function pwTip(cls,rel,who){""")
open(p,'w',encoding='utf-8').write(s)
