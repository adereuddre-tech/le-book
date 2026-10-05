# Lot 229 : la marge quitte la carte rentabilité/risque (elle était masquée par l'étiquette de rentabilité) et s'affiche
# discrètement sur la ligne d'intitulé de la tuile Trésorerie, à droite : « Trésorerie · · · marge 23 % ».
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
rep("\n  +(S.k&&S.k.some(v=>v)?`<span class=\"rv mgl\" style=\"right:3%;top:4%;left:auto;color:var(--dim)\">marge ${Math.round(marginPct(S.k)*100)} %</span>`:'')","")
rep("""<button class="tile gold" data-gauge="gain"><span>Trésorerie</span>""",
    """<button class="tile gold" data-gauge="gain"><span style="display:flex;justify-content:space-between;gap:6px"><span>Trésorerie</span>${S.k&&S.k.some(v=>v)?`<span class="mgt">marge ${Math.round(marginPct(S.k)*100)} %</span>`:''}</span>""")
rep(".evstep:disabled{opacity:.35}",".evstep:disabled{opacity:.35}\n.mgt{font-family:var(--mono);font-size:10px;color:var(--dim);letter-spacing:0;white-space:nowrap}")
open('index.html','w',encoding='utf-8').write(s);print('lot229 ok')
