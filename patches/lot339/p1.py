p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)

# déménager joue sur le moral tout de suite, de l'écart entier (iii)
rep("""   S.budBp=bp;S.budPrev={fo:S.bud.fo,bo:S.bud.bo};S.teamPrev=teamCopy();   /* lot 304 */S.officePrev=S.office==null?0:S.office;""",
    """   {const o1=S.office==null?0:S.office,o0=S.officePrev==null?0:S.officePrev;if(o1!==o0){const m1=motOff();S.office=o0;const m0=motOff();S.office=o1;   /* lot 339 */
     if(m1!==m0){motAdd(m1-m0,'déménagement');toast(`${OFFICES[o1].ic} Déménagement : moral ${m1>m0?'+':'−'}${Math.abs(m1-m0)}, dès ce trimestre.`)}}}
   S.budBp=bp;S.budPrev={fo:S.bud.fo,bo:S.bud.bo};S.teamPrev=teamCopy();   /* lot 304 */S.officePrev=S.office==null?0:S.office;""")
rep("""relevée par vos locaux (garage 0, yacht +13).""","""relevée par vos locaux (garage 0, yacht +13) ; un déménagement joue tout de suite, de l'écart entier, avant les signaux et les ordres du trimestre.""")
open(p,'w',encoding='utf-8').write(s)
