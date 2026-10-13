p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# collatéral (D simple) : défauts corrélés aux extrêmes, probabilité moyenne inchangée ; rendement relevé du drain (σ²/2) et de la covariance avec le book
rep("""function colOpt(){return COLL[(S&&S.col)||0]||COLL[0]}""","""const COLK=2.5,COLT0=0.2,COLD=0.05;   /* lot 342 : défaut ×2,5 le trimestre d'un extrême ; T de référence 20 % ; perte typique du fonds dans un extrême 5 % */
COLL.forEach(o=>{if(!o.p)return;const ph=Math.min(0.95,COLK*o.p);o.y0=o.y;o.y+=o.l*o.l*o.p*(1-o.p)/2+COLT0*(ph-o.p)*o.l*COLD});   /* Sharpe géométrique 0,35 + prime de covariance */
function colPx(o,ext){if(!o.p)return 0;const T=Math.min(0.39,xProbTot()),ph=Math.min(0.95,COLK*o.p);return ext?ph:Math.max(0,(o.p-T*ph)/Math.max(1e-9,1-T))}
function colOpt(){return COLL[(S&&S.col)||0]||COLL[0]}""")
rep(""" const cO=colOpt(),cHit=!redOn('collat')&&cO.p>0&&prng32(hash32('coll'+S.q,S.seed))()<cO.p;""",
    """ const cO=colOpt(),cPe=colPx(cO,!!S.stressQ),cHit=!redOn('collat')&&cO.p>0&&prng32(hash32('coll'+S.q,S.seed))()<cPe;   /* lot 342 */""")
rep("""hit:cHit,l:cO.l,p:cO.p,m:""","""hit:cHit,l:cO.l,p:cPe,ext:!!S.stressQ,m:""")
rep("""`Collatéral — ${c.nm} : pas de défaut (${Math.round(c.p*100)} % de risque)""","""`Collatéral — ${c.nm} : pas de défaut (${Math.round(c.p*100)} % de risque${c.ext?', trimestre d’extrême':''})""")
rep("""Le surcroît de chaque placement change d'un trimestre à l'autre ; en moyenne, plus le risque est grand, plus l'attendu l'est.""",
    """Le surcroît de chaque placement change d'un trimestre à l'autre ; en moyenne, plus le risque est grand, plus l'attendu l'est. Les défauts tombent ${dec(COLK,1)} fois plus souvent le trimestre d'un événement extrême (et d'autant moins sinon) : le rendement paie le drain de volatilité et cette corrélation avec votre book.""")
open(p,'w',encoding='utf-8').write(s)
