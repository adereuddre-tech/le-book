p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# un book vide n'a pas d'accident : la base de 6 % monte avec le risque jusqu'à 10 % (vol annualisée), puis reste fixe
rep("const x=sp/LIM.vol;return Math.min(0.6,(ACC.p0+ACC.p1*x*x)*","const x=sp/LIM.vol;return Math.min(0.6,(ACC.p0*Math.min(1,sp/0.10)+ACC.p1*x*x)*")
open(p,"w",encoding="utf-8").write(s)
