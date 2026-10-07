p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
rep('<div class="regime">${PGS[k][0]}</div></div><div class="thold">${PGS[k][1]}</div>','<div class="regime">${PGS[k][0]}</div></div><div>${PGS[k][1]}</div>')
open(p,'w',encoding='utf-8').write(s)
