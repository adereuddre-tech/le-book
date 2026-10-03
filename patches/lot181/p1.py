# Lot 181 : événements extrêmes moins exploitables. Ils étaient trop faciles à jouer en modifiant le book : la suite d'une
# dépêche est biaisée vers la poursuite (p entre 0,40 et 0,90), suivre coûte le tarif normal, et l'ajustement gratuit du flux
# rendait le suivi gratuit. Pour un événement extrême : amplitude ×0,8 (STRESSK 0,32) ; issue imprévisible (p entre 0,35 et
# 0,65), poursuite plus courte et retournement plus violent ; ordres de suivi au tarif de crise ×2,5 ; pas d'ajustement gratuit.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("const STRESSK=0.4,","const STRESSK=0.32,")
rep("S.sc={p:0.40+0.50*rng(),m:[0.45+0.40*rng(),-(0.30+0.40*rng())]};","S.sc=ev.stress?{p:0.35+0.30*rng(),m:[0.25+0.30*rng(),-(0.45+0.40*rng())]}:{p:0.40+0.50*rng(),m:[0.45+0.40*rng(),-(0.30+0.40*rng())]};")
rep("const tc=tcost(d,i);const c=tc.cost*1.6*S.tcMultQ*(S.leakQ?1.45:1);","const tc=tcost(d,i);const c=tc.cost*1.6*S.tcMultQ*(S.leakQ?1.45:1)*(ev.stress?2.5:1);")
rep("const free=cost>0&&(prof.freeAdj||S.freeAdjB>0)&&!S.freeAdjUsed;","const free=cost>0&&!ev.stress&&(prof.freeAdj||S.freeAdjB>0)&&!S.freeAdjUsed;")
open('index.html','w',encoding='utf-8').write(s);print('lot181 ok')
