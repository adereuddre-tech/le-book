p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
# la classe .gl existait déjà (étiquettes des jauges) : le glossaire passe en .glo
rep(".gl{border-bottom:1px dotted var(--gold);cursor:help}",".glo{border-bottom:1px dotted var(--gold);cursor:help}")
rep("if(n.parentElement.closest('.gl,b,a,button'))continue;","if(n.parentElement.closest('.glo,b,a,button'))continue;")
rep("sp.className='gl';","sp.className='glo';")
rep("const g=e.target.closest&&e.target.closest('.gl');","const g=e.target.closest&&e.target.closest('.glo');")
open(p,'w',encoding='utf-8').write(s)
