p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
rep('nm:"Chasseur de queues"','nm:"Chasseur de cygnes noirs"')
rep("le chasseur de queue gagne quand tout s'effondre","le chasseur de cygnes noirs gagne quand tout s'effondre")
open(p,'w',encoding='utf-8').write(s)
