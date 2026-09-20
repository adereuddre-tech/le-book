# -*- coding: utf-8 -*-
"""Lot 33 — virgule décimale dans tout ce que le joueur lit.

Constat (capture 380 px du lot 32) : « Nervosité de votre profil : ×1.60 », « Votre mandat
facture 2.0 % de gestion ». Invariant 8 et lot S (« virgule décimale partout ») : recensement
dans le fichier publié, 74 gabarits `${x.toFixed(n)}` dont 57 finissent dans du texte (les 17
autres sont des attributs SVG — cx, cy, x1, translate, rgba, dasharray — où la virgule
casserait le dessin) et 8 concaténations `(x).toFixed(n)+…`. Un seul cas tordu : la ligne
« Commission de gestion » construisait une chaîne ordinaire contenant `${…}` puis la remplaçait
par la valeur à point — réécrite en gabarit.
"""
import sys,re; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
e.rep("""'Commission de gestion (${(VOL().mgmt*400).toFixed(1)} % par an)'.replace('${(VOL().mgmt*400).toFixed(1)}',(VOL().mgmt*400).toFixed(1))""",
      """`Commission de gestion (${dec(VOL().mgmt*400,1)} % par an)`""")
R=re.compile(r"\$\{([^{}`]+?)\.toFixed\(([123])\)\}")
def isattr(s,i):
    p=s[max(0,i-14):i]
    return p.endswith(('="','translate(','scale(','},','${rgb},'))
hits=[m for m in R.finditer(e.s) if not isattr(e.s,m.start())]
assert len(hits)==57,'gabarits textuels : %d'%len(hits)
out=[];last=0
for m in hits:
    ex=m.group(1)
    # une expression à opérateur de tête sans parenthèses changerait de sens dans dec(...)
    top=re.sub(r"\([^()]*\)","",re.sub(r"\([^()]*\)","",re.sub(r"\([^()]*\)","",ex)))
    assert not re.search(r"[+\-*/?:]",top),'expression ambigue : %r'%ex
    out.append(e.s[last:m.start()]); out.append("${dec(%s,%s)}"%(ex,m.group(2))); last=m.end()
out.append(e.s[last:]); e.s=''.join(out)
# concaténations affichées
e.rep("""'−'+(dd*100).toFixed(1)+' %'""","""'−'+dec(dd*100,1)+' %'""")
e.rep("""'−'+(S.maxdd*100).toFixed(1)+' %'""","""'−'+dec(S.maxdd*100,1)+' %'""")
e.rep("""+Math.abs(S.fLast[k]).toFixed(2):'—'""","""+dec(Math.abs(S.fLast[k]),2):'—'""")
for c,f in (('t','0.12'),('c','0.10'),('v','0.08')):
    e.rep("${(%s*e.%s[i]*x.sigQ*100).toFixed(1).replace('-','−')} %%"%(f,c),"${dec(%s*e.%s[i]*x.sigQ*100,1).replace('-','−')} %%"%(f,c))
e.rep("""${sr.toFixed(2).replace('-','−')}""","""${dec(sr,2).replace('-','−')}""")
e.done("lot 33 — virgules decimales")
