# Lot 202 : Firmin Tatillon (conformité, back office) un peu plus cher, entre Josiane (15 pb) et Mireille (60 pb) : 30 → 40 pb.
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
rep('role:"conformité et audit interne",ic:"🔎",bp:30}','role:"conformité et audit interne",ic:"🔎",bp:40}   /* lot 202 : 30 → 40 pb */')
open('index.html','w',encoding='utf-8').write(s);print('lot202 ok')
