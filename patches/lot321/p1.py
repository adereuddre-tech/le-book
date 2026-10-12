p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# comptabilité additive dans le trimestre : le P&L du book s'applique à l'encours de début de trimestre ;
# un choc (dépêche, extrême, accident de levier) pris sur l'encours ne rétrécit plus après coup le P&L du book.
# Ce qui est affiché pendant l'événement est exactement ce que le fonds perd ou gagne à la clôture.
rep("""function navNow(){if(!S)return 0;if(S.phase!=='events'||!S.live||!S.rBase)return S.nav;
 const t=qElapsed(),w=weights(S.k);let g=-finDrag(S.k);for(let i=0;i<N;i++)g+=w[i]*S.rBase[i];if(!S.qColM)g+=colYield();return S.nav*(1+t*g)}""",
"""function navNow(){if(!S)return 0;if(S.phase!=='events'||!S.live||!S.rBase)return S.nav;
 const t=qElapsed(),w=weights(S.k);let g=-finDrag(S.k);for(let i=0;i<N;i++)g+=w[i]*S.rBase[i];return S.nav+t*(g*(S.navQ0||S.nav)+(S.qColM?0:colYield()*S.nav))}   /* lot 321 */""")
a=s.index("function liveRet(){");b=s.index("return (t*g*S.nav+(S.qColM||0)",a)
seg=s[a:b]
assert "if(!S.qColM)g+=colYield();" in seg
seg2=seg.replace("if(!S.qColM)g+=colYield();","const cy=S.qColM?0:colYield();")
s=s[:a]+seg2+s[b:]
rep("""return (t*g*S.nav+(S.qColM||0)+(S.qEvM||0)+(S.qIncM||0)-(S.qMgmtM||0))/Math.max(1e-9,S.navQ0);""",
    """return (t*(g*(S.navQ0||S.nav)+cy*S.nav)+(S.qColM||0)+(S.qEvM||0)+(S.qIncM||0)-(S.qMgmtM||0))/Math.max(1e-9,S.navQ0);   /* lot 321 : book sur l'encours de début de trimestre */""")
rep(""" const grQ=((gross+collateral)*nb+(S.qColM||0)+(S.qEvM||0)+(S.qIncM||0)-mgmtM)/q0;""",""" const grQ=(gross*q0+collateral*nb+(S.qColM||0)+(S.qEvM||0)+(S.qIncM||0)-mgmtM)/q0;   /* lot 321 */""")
rep(""" S.nav*=(1+net);""",""" S.nav+=gross*q0+(collateral-perf)*nb;   /* lot 321 : comptabilité additive */""")
rep(""" const grossM=gross*navBefore,""",""" const grossM=gross*q0,""")
open(p,'w',encoding='utf-8').write(s)
