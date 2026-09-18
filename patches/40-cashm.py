# -*- coding: utf-8 -*-
"""Lot 4 — les effets en millions de dollars fixes, remis à l'échelle du fonds.

Constat mesuré sur huit parties : les 49 effets `cashM` (de −20 à +45 M$) ponctionnaient
1,6 M$ par trimestre sur un fonds de 100 M$, soit environ 160 pb par trimestre et 6,4 %
par an — davantage que tout ce que la gestion rapporte au gérant sur deux ans. Sur une
partie, le fonds mourait avec des positions à −4 M$ et des anecdotes de desk à −13,9 M$.
Ces montants datent de la version où le fonds faisait 100 Md$.

Correction : la famille `cashM` disparaît. Chaque effet devient un pourcentage de l'encours
(`cash`), divisé par 20 : −12 M$ → −60 pb, soit −0,6 M$ sur un fonds de 100 M$. Les montants
deviennent proportionnels à la taille du fonds, et le texte affiché est réécrit avec eux
pour que « affiché = appliqué » tienne.
"""
import sys,re; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()

DIV=20.0   # facteur de remise à l'échelle demandé

# ── deux cas dont le texte ne porte pas simplement la valeur de l'effet ──
e.rep("""{b:"Acheter et le revendre à un concurrent",s:"−5 M$, coûts −20 %, +8 M$, comité −7.",e:{cashM:3,tcMult:0.8,rc:-7}}""",
      """{b:"Acheter et le revendre à un concurrent",s:"−25 pb, coûts −20 %, +40 pb, comité −7.",e:{cash:0.0015,tcMult:0.8,rc:-7}}""")
e.rep("""{b:"Acheter le flux et le revendre à un concurrent",s:"Coûts −20 %, comité −7 (la licence l'interdit expressément).",e:{tcMultOn:['ESTX','MXEF'],tcMult:0.8,rc:-7,cashM:10}}""",
      """{b:"Acheter le flux et le revendre à un concurrent",s:"+50 pb, coûts −20 %, comité −7 (la licence l'interdit expressément).",e:{tcMultOn:['ESTX','MXEF'],tcMult:0.8,rc:-7,cash:0.005}}""")

# ── conversion automatique du reste ──
s=e.s
CH=re.compile(r'\{b:"((?:[^"\\]|\\.)*)",s:"((?:[^"\\]|\\.)*)",e:\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}\}')
NUM=re.compile(r'cashM:(-?[\d.]+)')
def bp(v):        # v en M$ sur 100 M$ d'encours → pb après division
    return v/DIV/100.0*1e4
def frac(v):
    return round(v/DIV/100.0,6)
def conv(m):
    b,txt,eff=m.group(1),m.group(2),m.group(3)
    n=NUM.search(eff)
    if not n: return m.group(0)
    v=float(n.group(1))
    # le texte porte la valeur en M$ : on la remplace par sa valeur en pb
    raw=n.group(1).lstrip('-')
    raw=raw[:-2] if raw.endswith('.0') else raw
    txt2,cnt=re.subn(re.escape(raw)+r'\s*M\$', ('%g'%abs(bp(v)))+' pb', txt)
    assert cnt==1,'texte non réécrit : %r (valeur %s)'%(txt,raw)
    eff2=NUM.sub('cash:%g'%frac(v),eff,count=1)
    return '{b:"%s",s:"%s",e:{%s}}'%(b,txt2,eff2)
s,changed=CH.subn(conv,s)
rest=s.count('cashM:')
assert rest==0,'il reste %d effets cashM'%rest
e.s=s

# ── les deux gestionnaires deviennent inutiles ──
e.rep("""  if(e.cashM){S.nav+=e.cashM/1000;S.qEvM+=e.cashM/1000;msg.push(`${e.cashM>=0?'+':'−'}${Math.abs(e.cashM)} M$.`)}\n""","")
e.rep("""  if(e.cashM){pnl+=e.cashM/1000/navB;msg.push(`${e.cashM>=0?'+':'−'}${Math.abs(e.cashM)} M$.`)}\n""","")
# le message d'un effet proportionnel manquait côté desk : on l'ajoute
e.rep("""  if(e.cash){pnl+=e.cash}""",
      """  if(e.cash){pnl+=e.cash;msg.push(`Trésorerie ${sgn(e.cash,1)} (${(e.cash*1e4).toFixed(0)} pb).`)}""")

e.done("lot 4 — effets fixes remis à l'échelle (÷%d)"%DIV)
