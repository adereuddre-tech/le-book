# Lot 101j : +17,3 ± 4,1 M$ encore face au lot 99 : des chocs symétriques ne freinent pas le levier.
# Coût de liquidité d'un scénario, toujours perdant : les fourchettes s'écartent au moment où tout le monde marque
# au pire. Perte supplémentaire = STRGAP × Σ|w|·σQ × (×2 si extrême) × crowd(risque).
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("const STRESSK=0.4;","const STRESSK=0.4,STRGAP=0.28;\nfunction stressGap(k,sc){const w=weights(k);let g=0;for(let i=0;i<N;i++)g+=Math.abs(w[i])*INSTR[i].sigQ;return STRGAP*g*(sc&&sc.ext?2:1)*crowd(riskShown(w).total)}")
rep("return v<0?v*crowd(riskShown(w).total):v}","return (v<0?v*crowd(riskShown(w).total):v)-2*stressGap(k,sc)}")
rep("if(imm<0)imm*=crowd(riskShown(w).total);","if(imm<0)imm*=crowd(riskShown(w).total);imm-=stressGap(S.k,STRESS.find(x=>x.id===ev.stress))*(0.5+0.5*(TAILM[S.bud.risk]||1));")
open('index.html','w',encoding='utf-8').write(s);print('ok')
