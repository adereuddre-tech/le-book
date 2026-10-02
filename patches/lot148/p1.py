# Lot 148 : marge utilisée visible en permanence, sous le libellé « risque » de la carte du bandeau.
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("+`<span class=\"rv\" style=\"left:${f(Math.min(44,Math.max(L+2,px-14)))}%;bottom:7%;color:${cX}\">risque ${sv}</span>`",
    "+`<span class=\"rv\" style=\"left:${f(Math.min(44,Math.max(L+2,px-14)))}%;bottom:7%;color:${cX}\">risque ${sv}${S.k&&S.k.some(v=>v)?` · marge ${Math.round(marginPct(S.k)*100)} %`:''}</span>`")
open('index.html','w',encoding='utf-8').write(s);print('lot148 ok')
