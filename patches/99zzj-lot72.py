# -*- coding: utf-8 -*-
"""Lot 72 — marchés classés par liquidité dans chaque classe.
Mesure (coût d'une unité à l'ouverture, en pb de l'encours, identique aux trois tailles) :
actions NQ 0,17 < ES 0,19 < ESTX 0,41 < TOPX 0,45 < MXEF 0,89 ;
taux TN 0,42 < GBL 0,90 < R 1,22 < OAT 1,45 < JGB 2,70 ;
matières premières CL 0,56 < HG 0,66 < GC 0,89 < KC 1,49 < ZW 1,87 ;
devises et exotiques déjà dans l'ordre. Le rang `rk` (ordre d'ouverture) et l'ordre du tableau
suivent désormais ce classement : au départ, TOPIX, JGB et blé cèdent la place au Nasdaq, au gilt
et au cuivre. L'ordre des marchés change les indices : une sauvegarde d'avant ce lot est refusée
(signature `d.ord`), sans effacement (invariant 2)."""
import sys,re; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
ORD=['NQ','ES','ESTX','TOPX','MXEF','TN','GBL','R','OAT','JGB','EUR','JPY','GBP','AUD','MXP',
     'CL','HG','GC','KC','ZW','BTC','VX','EUA','BDI','NRAM']
a=e.s.index("const INSTR_ALL=[\n")+len("const INSTR_ALL=[\n");b=e.s.index("\n];",a)
lines=e.s[a:b].split('\n');assert len(lines)==25
by={}
for l in lines:
    m=re.match(r" \{sym:'(\w+)',\s*rk:\d",l);assert m,l[:40];by[m.group(1)]=l.rstrip(',')
assert sorted(by)==sorted(ORD)
out=[]
for j,sy in enumerate(ORD):
    l=re.sub(r"(\{sym:'\w+',\s*rk:)\d",lambda m:m.group(1)+str(j%5+1),by[sy],count=1)
    out.append(l)
e.s=e.s[:a]+',\n'.join(out)+e.s[b:]
# signature d'ordre dans la sauvegarde
e.rep("d.b=INSTR.map(x=>x.b);d.rngState=rngState;","d.b=INSTR.map(x=>x.b);d.ord=INSTR.map(x=>x.sym).join(',');d.rngState=rngState;")
e.rep("  setUniverse(d.size,d.univ);\n  rng=mulberry32(0);",
 "  setUniverse(d.size,d.univ);\n  if((d.ord||'')!==INSTR.map(x=>x.sym).join(','))return false;   /* lot 72 : ordre des marchés changé, les indices ne correspondent plus */\n  rng=mulberry32(0);")
# une reprise ratée par #resume ne laisse plus une page vide
e.rep("if(!(hasSave()&&location.hash==='#resume'))screenIntro();else loadGame();",
 "if(!(hasSave()&&location.hash==='#resume'))screenIntro();else if(!loadGame())screenIntro();")
e.done("lot 72")
