p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)

# gain du trimestre = fin − début de trésorerie (le bonus d'objectif était compté deux fois, le bonus d'équipe oublié)
rep("""netQ=Gq.fees-Gq.ops-(Gq.tc||0)+(Gq.coinv||0)-(Gq.claw||0)+bon;""","""netQ=mgrCash()-(S.tresQ0!==undefined?S.tresQ0:0);""")
rep("""const gpart=[['commissions',Gq.fees],""","""const gpart=[['commissions',Gq.fees-bon],""")
rep("""['budget',-Gq.ops],['exécution',-(Gq.tc||0)]].filter""","""['budget',-Gq.ops],["bonus d'équipe",-(S.qBonT||0)],['exécution',-(Gq.tc||0)]].filter""")
open(p,'w',encoding='utf-8').write(s)
