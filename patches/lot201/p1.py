# Lot 201 : capital de départ des concurrents selon la difficulté. Leur trésorerie de départ (RIVSEED 0,5 M$ partout)
# devient rivSeed par difficulté : 0,25 M$ (facile), 1,5 M$ (moyen), 4 M$ (difficile), remplaçants compris. Le choix du
# cran de budget (rivBudget, réservé au difficile) vaut désormais partout : un concurrent riche s'offre d'emblée une
# équipe plus chère (+0,8 à +1,8 % de rendement par trimestre), un concurrent pauvre reste au cran standard.
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
rep("rivSkill:0.050,rivVol:0.95,lpNeg:0.60","rivSkill:0.050,rivVol:0.95,rivBud:1,rivSeed:0.00025,lpNeg:0.60")
rep("rivSkill:0.090,rivVol:1,lpNeg:1","rivSkill:0.090,rivVol:1,rivBud:1,rivSeed:0.0015,lpNeg:1")
rep("rivSkill:0.180,rivVol:1.10,rivBud:1,","rivSkill:0.180,rivVol:1.10,rivBud:1,rivSeed:0.004,")
rep("const RIVSEED=0.0005;   /* trésorerie de départ d'un concurrent : 0,5 M$ (à tester, lot 158) */",
    "const RIVSEED=0.0005;   /* trésorerie de départ d'un concurrent : 0,5 M$ (à tester, lot 158) */\nfunction rivSeed(){const z=SIZE();return z&&z.rivSeed!=null?z.rivSeed:RIVSEED}   /* lot 201 : par difficulté */")
rep("rv.mgr0=RIVSEED;rv.q0=0","rv.mgr0=rivSeed();rv.q0=0")
rep("mgr:RIVSEED,mgr0:RIVSEED,","mgr:rivSeed(),mgr0:rivSeed(),")
rep('[\"g\",\"concurrents moins adroits\"]','[\"g\",\"concurrents moins adroits et peu capitalisés (0,25 M$ de trésorerie)\"]')
rep('[\"b\",\"concurrents très bons, chacun dans son style\"]','[\"b\",\"concurrents très bons, chacun dans son style, 1,5 M$ de trésorerie pour s\'offrir une meilleure équipe\"]')
rep('[\"b\",\"concurrents au sommet de leur art\"]','[\"b\",\"concurrents au sommet de leur art, 4 M$ de trésorerie : la meilleure équipe dès le départ\"]')
open('index.html','w',encoding='utf-8').write(s);print('lot201 ok')
