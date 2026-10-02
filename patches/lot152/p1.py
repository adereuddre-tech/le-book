# Lot 152 : « L'essentiel » — dépêches et tuyaux, incidents, frais du fonds sous le gain brut des positions, pour reconstituer
# le résultat du trimestre.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("<div class=\"attr\"><span class=\"an\">Gain brut des positions</span><span class=\"av\">${inU(o.P.grossM,UQ)}</span></div>",
    "<div class=\"attr\"><span class=\"an\">Gain brut des positions</span><span class=\"av\">${inU(o.P.grossM,UQ)}</span></div>\n"
    "  ${Math.abs(o.P.evM||0)>1e-7?`<div class=\"attr\"><span class=\"an\">Dépêches et tuyaux</span><span class=\"av\">${inU(o.P.evM,UQ)}</span></div>`:''}\n"
    "  ${Math.abs(o.P.incM||0)>1e-7?`<div class=\"attr\"><span class=\"an\">Incidents</span><span class=\"av\">${inU(o.P.incM,UQ)}</span></div>`:''}\n"
    "  ${Math.abs(o.P.feeM||0)>1e-7?`<div class=\"attr\"><span class=\"an\">Frais du fonds</span><span class=\"av\">${inU(o.P.feeM,UQ)}</span></div>`:''}")
open('index.html','w',encoding='utf-8').write(s);print('lot152 ok')
