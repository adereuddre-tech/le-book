# Lot 129 : incidents du flux plus fréquents (×1,75 au lieu de ×1,25) et plus coûteux (gravité ×2,2, `incSev`).
# Mesure, 90 parties de flux sur les graines de la campagne du lot 127 : en ligne survie 70,1 %, score 14,5 M$ ;
# gravité ×1,6 : 68,9 % / 14,3 ; gravité ×2,2 : 67,8 % / 14,4 ; fréquence ×1,75 + gravité ×2,2 : 65,6 % / 14,6 (médiane 4,6).
# Classement obtenu : quant 73 %, fondamental 68 %, flux 66 % en survie ; flux toujours en tête au score.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep(" const sev=ARCH().sev*RISKS[S.bud.risk];"," const sev=ARCH().sev*RISKS[S.bud.risk]*(PROF().incSev||1);")
rep("incMult:1.25,numeric:false,freeAdj:true,hunch:true}","incMult:1.75,incSev:2.2,numeric:false,freeAdj:true,hunch:true}")
rep("[\"Incidents\",p=>f(p.incMult)]","[\"Incidents : fréquence · coût\",p=>f(p.incMult)+' · '+f(p.incSev||1,1)]")
rep("['g',\"commission de performance +5 pts : l'aura du prophète","['b',\"incidents plus fréquents (×1,75) et deux fois plus chers : un desk qui va vite casse plus de vaisselle\"],['g',\"commission de performance +5 pts : l'aura du prophète")
open('index.html','w',encoding='utf-8').write(s);print('lot129 p1 ok')
