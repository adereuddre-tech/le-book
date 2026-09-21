# -*- coding: utf-8 -*-
"""Lot 45 — budget à sept crans, plafond à 1,5 fois l'ancien maximum, sur une seule ligne.

Décision d'Antoine : onze crans, c'était trop ; le maximum à deux fois l'ancien était un piège
que la mesure du lot 39 a confirmé (tout au maximum : 6,1 M$ contre 21,7 au standard).

  Salle de marché    2 · 10 · 14 · 18 · 32 · 50 · 75 pb
  Contrôle           4 ·  8 · 10 · 12 · 18 · 24 · 36 pb
  Recherche          4 · 12 · 15 · 18 · 36 · 64 · 96 pb

Les crans 0 / 3 / 5 sont exactement les trois anciens niveaux (prix et effets inchangés) ; les
autres reprennent les crans 2, 6 et 9 de l'échelle à onze, et leurs effets. Le dernier vaut
1,5 fois l'ancien maximum. `BUDMAX` = 5 (« Renforcé » = l'ancien maximum).
Sauvegardes : onze crans → sept par [0,1,1,2,3,3,4,4,5,6,6] ; trois niveaux → 0 / 3 / 5.
"""
import sys,re; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
P=[0,2,3,4,6,8,9]
def pick(line):
    m=re.search(r"\[([^\]]+)\]",line);vals=[v.strip() for v in m.group(1).split(',')]
    assert len(vals)==11,line
    return line[:m.start()]+'['+','.join(vals[i] for i in P)+']'+line[m.end():]
# niveaux : noms et prix
for bid,bps,mx in (('exec',None,75),('risk',None,36),('res',None,96)):
    pass
def lvrep(old_bps,new_last):
    pat=re.compile(r"lv:\[(\{nm:\"[^\"]+\",bp:\d+\}(?:,\{nm:\"[^\"]+\",bp:\d+\}){10})\]")
    return pat
pat=re.compile(r"lv:\[((?:\{nm:\"[^\"]+\",bp:\d+\},?){11})\]")
ms=list(pat.finditer(e.s));assert len(ms)==3,len(ms)
MX=[75,36,96]
out=[];last=0
for k,m in enumerate(ms):
    items=re.findall(r"\{nm:\"([^\"]+)\",bp:(\d+)\}",m.group(1))
    sel=[items[i] for i in P]
    sel[-1]=("Sans limite",str(MX[k]))
    out.append(e.s[last:m.start()]);out.append('lv:['+','.join('{nm:"%s",bp:%s}'%x for x in sel)+']');last=m.end()
out.append(e.s[last:]);e.s=''.join(out)
# tableaux d'effets
for name in ['const EXECM=','RISKM=','RISKS=','RETM =','const RESN=','RESREL=','RESR  =','RESPH =','const TCVQ=','BANDB=','const RISKRC=','STARP=']:
    i=e.s.index(name);j=e.s.index(']',i)+1
    e.s=e.s[:i]+pick(e.s[i:j])+e.s[j:]
e.rep("const BUDMAX=8;","const BUDMAX=5;")
e.rep("gravité ×${dec(RISKS[i]/RISKS[4],2)}","gravité ×${dec(RISKS[i]/RISKS[3],2)}")
e.rep("bud:{exec:4,risk:4,res:4,ret:4},budN:11,","bud:{exec:3,risk:3,res:3,ret:3},budN:7,")
e.rep("  if(!S.budN&&S.bud){const M3=[0,4,8];for(const k in S.bud)S.bud[k]=M3[S.bud[k]]!==undefined?M3[S.bud[k]]:4;S.budN=11}",
      "  if(!S.budN&&S.bud){const M3=[0,3,5];for(const k in S.bud)S.bud[k]=M3[S.bud[k]]!==undefined?M3[S.bud[k]]:3;S.budN=7}\n"
      "  /* sauvegarde des lots 39 à 44 : onze crans ramenés à sept */\n"
      "  if(S.budN===11&&S.bud){const M11=[0,1,1,2,3,3,4,4,5,6,6];for(const k in S.bud)S.bud[k]=M11[S.bud[k]]!==undefined?M11[S.bud[k]]:3;S.budN=7}")
e.rep("function rivalCostQ(){return (BUDGET.reduce((a,b)=>a+b.lv[4].bp,0)","function rivalCostQ(){return (BUDGET.reduce((a,b)=>a+b.lv[3].bp,0)")
e.rep("Budget standard (cran 5 sur 11 des trois postes","Budget standard (cran 4 sur 7 des trois postes")
# objectifs et bonus qui visaient l'ancien cran « Renforcé »
e.rep("t:c=>c.budRes>=8&&c.rel>0","t:c=>c.budRes>=BUDMAX&&c.rel>0")
e.rep("t:c=>c.budExec>=8&&c.tcBp<22","t:c=>c.budExec>=BUDMAX&&c.tcBp<22")
e.rep("tq:c=>c.budRes>=8&&c.q>0","tq:c=>c.budRes>=BUDMAX&&c.q>0")
e.rep("S.q>=1&&S.bud.res>=6&&bonusDraw('fed')","S.q>=1&&S.bud.res>=4&&bonusDraw('fed')")
e.rep("S.q>=1&&S.bud.exec>=8&&bonusDraw('star')","S.q>=1&&S.bud.exec>=BUDMAX&&bonusDraw('star')")
# une seule ligne de sept boutons
e.rep(".lvls{display:grid;grid-template-columns:repeat(6,1fr);gap:4px}",".lvls{display:grid;grid-template-columns:repeat(7,1fr);gap:3px}\n.lvls .lvl b{font-size:15px}.lvls .lvl span{font-size:8.5px;letter-spacing:-.02em}")
e.rep("<summary>Les onze crans</summary>","<summary>Les sept crans</summary>")
e.done("lot 45 — budget a sept crans")
