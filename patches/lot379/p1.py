p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# Rapport final et trésorerie : qui paie quoi
rep("""<div class="cl">Exécution payée de votre poche</div><div class="cv">${moneyB(S.totalTC)}</div>""","""<div class="cl">Fourchette et impact, payés par le fonds</div><div class="cv">${moneyB(S.totalTC)}</div>""")
rep("""<div class="cl">Budget d'exploitation payé</div>""","""<div class="cl">Budget de l'équipe, payé par vous</div>""")
rep("""Il vous reste <em>${mm(mgrCash())}</em> pour payer budget et ordres.""","""Il vous reste <em>${mm(mgrCash())}</em> pour payer l'équipe, le courtage et les bonus.""")
open(p,"w",encoding="utf-8").write(s)
