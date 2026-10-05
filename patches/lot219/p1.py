# Lot 219 : la marge s'affiche sur le panneau. Elle suivait « risque … » sur l'étiquette du bas de la carte
# rentabilité/risque, qui débordait sur téléphone (« · marge » coupé). Elle a désormais sa propre étiquette, en haut à
# droite de la carte, sans rien déplacer.
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
rep("color:${cX}\">risque ${sv}${S.k&&S.k.some(v=>v)?` · marge ${Math.round(marginPct(S.k)*100)} %`:''}</span>`",
    "color:${cX}\">risque ${sv}</span>`\n  +(S.k&&S.k.some(v=>v)?`<span class=\"rv mgl\" style=\"right:3%;top:4%;left:auto;color:var(--dim)\">marge ${Math.round(marginPct(S.k)*100)} %</span>`:'')")
open('index.html','w',encoding='utf-8').write(s);print('lot219 ok')
