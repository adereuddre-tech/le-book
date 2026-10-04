# Lot 186 : back office — Mireille Cauchemar coûte un tiers de plus (45 → 60 pb), Solange Pare-Feu deux tiers de plus (60 → 100 pb).
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep('full:"Mireille Cauchemar",role:"directrice des risques",ic:"⚖️",bp:45','full:"Mireille Cauchemar",role:"directrice des risques",ic:"⚖️",bp:60')
rep('ic:"🛡️",bp:60','ic:"🛡️",bp:100')
open('index.html','w',encoding='utf-8').write(s);print('lot186 ok')
