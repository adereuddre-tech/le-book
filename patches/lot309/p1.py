p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# loyers affichés en dollars par trimestre (le barème reste en points de base de la base de coûts)
rep("""<b>${o.ic} ${o.nm}</b><span>${o.bp} pb${ok?'':' · hors trésorerie'}</span>""","""<b>${o.ic} ${o.nm}</b><span>${mm(o.bp*1e-4*budNav())} par trimestre${ok?'':' · hors trésorerie'}</span>""")
open(p,'w',encoding='utf-8').write(s)
