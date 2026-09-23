# -*- coding: utf-8 -*-
"""Lot 48 — budgets lissés, page « Le trimestre se déroule » supprimée, bonus un peu plus rares,
difficulté croissante avec la taille.

Budgets. Les sept crans reprenaient des crans de l'échelle à onze : progression irrégulière
(salle de marché 2 · 10 · 14 · 18 · 32 · 50 · 75, sauts de 8, 4, 4, 14, 18, 25). Désormais
bp(i) = min + (max − min) · (i/6)^p, une courbe qui accélère régulièrement, avec p choisi pour
que le cran 3 reste exactement le standard (18 / 12 / 18 pb) :
  salle de marché  p = 2,19 : 2 · 3 · 9 · 18 · 32 · 51 · 75
  contrôle         p = 2    : 4 · 5 · 8 · 12 · 18 · 26 · 36
  recherche        p = 2,72 : 4 · 5 · 9 · 18 · 35 · 60 · 96
Les effets suivent le prix : chaque tableau est interpolé, au nouveau prix, sur la courbe
prix → effet de l'échelle à onze crans (lot 39), qui reste la référence calibrée. Un cran qui
coûte moins rapporte donc moins, et inversement.

« Le trimestre se déroule » : une page de transition sans décision. « Lancer le trimestre »
mène désormais directement à la première dépêche.
"""
import sys,re,math; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
# ── budgets ───────────────────────────────────────────────────────────────────
BP11={'exec':[2,6,10,14,18,24,32,40,50,72,100],'risk':[4,6,8,10,12,15,18,21,24,34,48],'res':[4,8,12,15,18,26,36,48,64,92,128]}
E11={'EXECM':('exec',[1.35,1.15,1.00,0.87,0.75,0.69,0.63,0.57,0.50,0.40,0.30],2),
     'RETM':('exec',[2.00,1.70,1.45,1.20,1.00,0.80,0.63,0.46,0.30,0.15,0.08],2),
     'TCVQ':('exec',[0.90,0.82,0.74,0.67,0.60,0.53,0.47,0.41,0.35,0.26,0.18],2),
     'STARP':('exec',[0,0,0,0,0,0.08,0.15,0.22,0.30,0.45,0.60],2),
     'RISKM':('risk',[2.20,1.80,1.50,1.22,1.00,0.70,0.48,0.32,0.20,0.10,0.04],2),
     'RISKS':('risk',[2.00,1.85,1.72,1.60,1.50,1.28,1.10,0.92,0.75,0.60,0.45],2),
     'BANDB':('risk',[0.18,0.19,0.21,0.23,0.25,0.28,0.31,0.35,0.40,0.50,0.60],2),
     'RISKRC':('risk',[-1,-0.8,-0.6,-0.3,0,0.5,1,1.5,2,3,4],1),
     'RESN':('res',[6,7,8,8,9,10,10,11,12,14,16],0),
     'RESREL':('res',[-0.08,-0.06,-0.04,-0.02,0,0.02,0.04,0.06,0.08,0.12,0.16],2),
     'RESR':('res',[0.30,0.37,0.45,0.52,0.60,0.70,0.79,0.87,0.95,0.98,1.00],2),
     'RESPH':('res',[0.16,0.145,0.13,0.115,0.10,0.088,0.076,0.064,0.05,0.030,0.020],3)}
LIM={'exec':(2,75,18),'risk':(4,36,12),'res':(4,96,18)}
NEW={}
for k,(lo,hi,std) in LIM.items():
    p=math.log((std-lo)/(hi-lo))/math.log(0.5)
    NEW[k]=[round(lo+(hi-lo)*(i/6)**p) for i in range(7)]
    assert NEW[k][3]==std and NEW[k][0]==lo and NEW[k][6]==hi,(k,NEW[k])
def interp(xs,ys,x):
    for a in range(len(xs)-1):
        if xs[a]<=x<=xs[a+1]:
            t=(x-xs[a])/(xs[a+1]-xs[a]);return ys[a]+t*(ys[a+1]-ys[a])
    raise ValueError(x)
pat=re.compile(r"lv:\[((?:\{nm:\"[^\"]+\",bp:\d+\},?){7})\]")
ms=list(pat.finditer(e.s));assert len(ms)==3
out=[];last=0
for k,m in zip(['exec','risk','res'],ms):
    names=re.findall(r'nm:"([^"]+)"',m.group(1))
    out.append(e.s[last:m.start()]);out.append('lv:['+','.join('{nm:"%s",bp:%d}'%(n,b) for n,b in zip(names,NEW[k]))+']');last=m.end()
out.append(e.s[last:]);e.s=''.join(out)
for name,(bud,ys,dp) in E11.items():
    vals=[interp(BP11[bud],ys,x) for x in NEW[bud]]
    txt=','.join(str(int(round(v))) if dp==0 else ('%.*f'%(dp,v)) for v in vals)
    m=re.search(r"(?<![A-Z])"+name+r"\s*=\s*\[[^\]]+\]",e.s);assert m,name
    e.s=e.s[:m.start()]+m.group(0).split('[')[0]+'['+txt+']'+e.s[m.end():]
# ── la page de transition disparaît ───────────────────────────────────────────
old=e.s[e.s.index("function phaseLive(){"):]
old=old[:old.index("\n}\n")+3]
e.rep(old,"""function phaseLive(){
 S.live=true;   /* le ruban ne s'affiche qu'à partir d'ici : avant, la performance ne bouge pas */
 /* lot 48 : plus de page « Le trimestre se déroule » — on entre directement dans les dépêches */
 S.evIdx=0;S.incidentShown=false;S.midShown=false;stepEvents();
}
""")
# ── cartes dorées : un peu plus rares ──────────────────────────────────────────
for a,b in [("B('century',bestEv>=0.12,","B('century',bestEv>=0.15,"),
            ("B('ft',o.qTotal>Math.max(...S.rivals.map(r=>r.last))+0.05&&","B('ft',o.qTotal>Math.max(...S.rivals.map(r=>r.last))+0.10&&"),
            ("B(yid,best&&base>0,","B(yid,best&&base>0.10,"),
            ("B('souv',g>=1.5&&conf0>=75,","B('souv',g>=1.6&&conf0>=78,"),
            ("B('carte',(S.inBand||0)>=3,","B('carte',(S.inBand||0)>=4,"),
            ("k:'INSTITUTIONNEL · TROIS TRIMESTRES DANS LA BANDE'","k:'INSTITUTIONNEL · QUATRE TRIMESTRES DANS LA BANDE'"),
            ("B('blocs',g>=1.25,","B('blocs',g>=1.3,"),("k:'CROISSANCE · ENCOURS ×1,25'","k:'CROISSANCE · ENCOURS ×1,3'"),
            ("B('prime',g>=1.5,","B('prime',g>=1.6,"),
            ("B('dark',g>=2,","B('dark',g>=2.2,"),("k:'CROISSANCE · ENCOURS ×2',t:'Les dark pools","k:'CROISSANCE · ENCOURS ×2,2',t:'Les dark pools"),
            ("bonusDraw('fed')<0.35","bonusDraw('fed')<0.30"),
            ("B('hot',(S.streak||0)>=4,","B('hot',(S.streak||0)>=5,"),("k:'SÉRIE · QUATRE TRIMESTRES POSITIFS'","k:'SÉRIE · CINQ TRIMESTRES POSITIFS'"),("bonusDraw('jh')<0.30","bonusDraw('jh')<0.25")]:
    e.rep(a,b)
e.s=e.s.replace("k:'CROISSANCE · ENCOURS ×1,5',t:'Prime brokerage","k:'CROISSANCE · ENCOURS ×1,6',t:'Prime brokerage")
# ── difficulté croissante avec la taille : des concurrents plus forts à mesure que le fonds grossit ──
e.rep("rivSkill:-0.010,rivVol:0.95,","rivSkill:0.050,rivVol:0.95,")
e.rep("rivSkill:0.020,rivVol:1,","rivSkill:0.050,rivVol:1,")
e.rep("rivSkill:0.030,rivVol:1.10,","rivSkill:0.090,rivVol:1.10,")
e.done("lot 48 — budgets lisses, page de transition supprimee, bonus plus rares, difficulte par taille")
