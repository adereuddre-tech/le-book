# -*- coding: utf-8 -*-
import io
P='index.html'
def load():
    return io.open(P,encoding='utf-8').read()
def save(s):
    io.open(P,'w',encoding='utf-8').write(s)
class Ed:
    def __init__(self): self.s=load()
    def rep(self,o,n,k=1):
        c=self.s.count(o)
        assert c==k,'ancre trouvee %d fois (attendu %d) : %r'%(c,k,o[:90])
        self.s=self.s.replace(o,n)
    def done(self,msg): save(self.s); print(msg)
