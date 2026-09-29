# Lot 101i : les extrêmes doivent faire mal : chocs de facteurs et de marchés ×2, chocs ciblés relevés.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("function stressHit(sc,k){k=k||S.k;const h={};INSTR.forEach((x,i)=>{let v=0;for(let f=0;f<4;f++)v+=x.b[f]*(sc.sh?sc.sh[f]:0);v*=STRESSK;if(sc.x&&sc.x[x.sym])v+=sc.x[x.sym]*STRESSK*1.5;",
    "function stressHit(sc,k){k=k||S.k;const h={},K=STRESSK*(sc.ext?2:1);INSTR.forEach((x,i)=>{let v=0;for(let f=0;f<4;f++)v+=x.b[f]*(sc.sh?sc.sh[f]:0);v*=K;if(sc.x&&sc.x[x.sym])v+=sc.x[x.sym]*K*1.5;")
for a,b in [("tgt:'short',H:3.0","tgt:'short',H:5.0"),("tgt:'otc',H:2.0","tgt:'otc',H:3.0"),("tgt:'rogue',H:3.0","tgt:'rogue',H:5.0"),("tgt:'crowd',H:0.8","tgt:'crowd',H:1.5")]: rep(a,b)
open('index.html','w',encoding='utf-8').write(s);print('ok')
