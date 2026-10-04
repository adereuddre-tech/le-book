# Lot 213 : coûts du back office, progression régulière (ratio ≈ 1,7 à 2 entre deux crans) :
# Loyer 5, Gontran 10, Josiane 15 → 20, Firmin 40 → 32, Mireille 60 → 55, Solange 100 (inchangés aux extrémités).
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
rep('role:"responsable du back office",ic:"🗂️",bp:15}','role:"responsable du back office",ic:"🗂️",bp:20}')
rep('role:"conformité et audit interne",ic:"🔎",bp:40}   /* lot 202 : 30 → 40 pb */','role:"conformité et audit interne",ic:"🔎",bp:32}   /* lot 202 : 30 → 40 ; lot 213 : 32 */')
rep('role:"directrice des risques",ic:"⚖️",bp:60}','role:"directrice des risques",ic:"⚖️",bp:55}')
open('index.html','w',encoding='utf-8').write(s);print('lot213 ok')
