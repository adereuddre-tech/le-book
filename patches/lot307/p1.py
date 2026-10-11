p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# 1. plus de frais d'embauche (le licenciement garde son indemnité d'un demi-trimestre)
rep("""function hireRaw(T){T=T||teamInit();""","""function hireRaw(T){return 0;   /* lot 307 : recruter ne coûte que le salaire */
 T=T||teamInit();""")
rep("""Recruter ou licencier coûte un demi-trimestre de son salaire.""","""Recruter ne coûte que le salaire ; licencier coûte un demi-trimestre de salaire d'indemnité.""")
rep(""":`<span class="neg-g">embauche −${m3(0.5*sal)}</span>`)""",""":'<span class="pos-g">recrue</span>')""")
rep("""${on&&!was?` · frais d'embauche ${mm(fee)}`:!on&&was""","""${!on&&was""")
# 2. capital de départ ramené à celui d'avant le lot 305
rep("costM:0.85,seed:0.0015}","costM:0.85,seed:0.001}")
rep("costM:1.10,seed:0.001}","costM:1.10,seed:0.0005}")
rep("costM:1.75,seed:0.0005}","costM:1.75,seed:0}")
rep('["g","capital de départ : 0,5 M$, plus celui de votre style"]','["b","aucun capital de départ, sauf celui de votre style"]')
rep("capital de départ : 1 M$, plus celui de votre style","capital de départ : 0,5 M$, plus celui de votre style")
rep("capital de départ : 1,5 M$, plus celui de votre style","capital de départ : 1 M$, plus celui de votre style")
open(p,'w',encoding='utf-8').write(s)
