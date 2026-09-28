# Lot 92c : campagne 180 parties (lot 92 vs lot 91) : standard (Boris, Maître Lettrage) +3,3 ± 3,4 M$, neutre ;
# cran Tuco + Mireille −7,0 ± 1,6 M$ = exactement son surcoût (85 pb/trim.) : effets nuls au prix. Crans hauts moins chers.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
for a,b in [('ic:"🛢️",bp:100','ic:"🛢️",bp:75'),('ic:"🐉",bp:200','ic:"🐉",bp:120'),('ic:"📿",bp:400','ic:"📿",bp:200'),('ic:"⚖️",bp:50','ic:"⚖️",bp:40'),('ic:"🔎",bp:75','ic:"🔎",bp:60')]: rep(a,b)
open('index.html','w',encoding='utf-8').write(s);print('ok')
