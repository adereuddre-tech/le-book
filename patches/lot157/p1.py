# Lot 157 : concurrents à book réel (3/4) — pool de fonds et de gérants (parodies validées par Antoine), tirés au hasard en
# début de partie ; trésorerie de départ des concurrents (RIVSEED) ; faillite d'un concurrent (trésorerie négative à la
# clôture) → remplacé par un fonds du même style tiré dans le pool, nouveau gérant, montée en charge depuis son lancement.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("/* ════════════════════ 3. ÉVÉNEMENTS ════════════════════ */",r'''const RIVPOOL={fonda:["Pont-Levis Associés","Fonds Sorosse","Tudoré Investissements","Place Perchée Capital","Beau-Poste Group","Feu Vert Capital"],
 syst:["Médaillon d'Or","Deux Sigmas","D. E. Chaud & Cie","ACR Capital","Homme AHL","Wintonne"],
 flux:["Citadelle Nord","Millénaire Gestion","Point 73","Brevent Ouard","Rue Jeanne","Plus Capital"]};
const RIVBOSS=["Rayon Daglio","Jim Simonet","Ken Griffon","Georges Sorosse","Paul Tudoré-Jaunes","Bill Hackman","Seth Clairman","David Licorne","Paul Chanteur",
 "David Chaud","Cliff Asnière","David Hardi","Jean Surdeck","Izzy Anglais","Steve Cohène","Alain Ouard","Dmitri Balyasnov","Louis Jambon"];
const RIVSEED=0.0005;   /* trésorerie de départ d'un concurrent : 0,5 M$ (à tester, lot 158) */
function rivPick(arr,used,u){const L=arr.filter(x=>!used.includes(x));const P=L.length?L:arr;return P[Math.floor(u()*P.length)]}
function rivDraw(){const u=prng32(hash32('rivnames',S.seed));S.rivUsedF=[];S.rivUsedB=[];
 S.rivals.forEach(rv=>{rv.nm=rivPick(RIVPOOL[rv.style]||RIVPOOL.fonda,S.rivUsedF,u);rv.boss=rivPick(RIVBOSS,S.rivUsedB,u);S.rivUsedF.push(rv.nm);S.rivUsedB.push(rv.boss);rv.mgr0=RIVSEED;rv.q0=0})}
function rivReplace(j){const old=S.rivals[j],Z=SIZE(),base=RIVALS.find(r=>r.style===old.style)||RIVALS[0],u=prng32(hash32('rivnew'+j+'_'+S.q,S.seed));
 const nm=rivPick(RIVPOOL[old.style]||RIVPOOL.fonda,S.rivUsedF||[],u),boss=rivPick(RIVBOSS,S.rivUsedB||[],u);(S.rivUsedF=S.rivUsedF||[]).push(nm);(S.rivUsedB=S.rivUsedB||[]).push(boss);
 const n=(old.hist||[]).length,nv={...base,nm,boss,style:old.style,crest:old.crest,skill:Math.max(0.5,Math.min(0.88,base.skill+Z.rivSkill+(u()-0.5)*0.06)),vol:base.vol*Z.rivVol*(0.9+0.2*u()),
  cum:1,peak:1,last:0,hist:new Array(n).fill(0),vqh:new Array(n).fill(base.vol*Z.rivVol),mgr:RIVSEED,mgr0:RIVSEED,mAum:S.aum0,mHwm:S.aum0,perfH:[],q0:S.q+1,fresh:S.q+1,prevNm:old.nm,prevBoss:old.boss};
 S.rivals[j]=nv;(S.rivNews=S.rivNews||[]).push({q:S.q,old:old.nm,oldBoss:old.boss,nm,boss});return nv}
/* ════════════════════ 3. ÉVÉNEMENTS ════════════════════ */''')
rep("function rivRamp(q){return RIVB.ramp[Math.min(RIVB.ramp.length-1,Math.max(0,q))]}","function rivRamp(q){return RIVB.ramp[Math.min(RIVB.ramp.length-1,Math.max(0,q))]}   /* q : trimestres depuis le lancement du concurrent */")
rep("function rivBookQ(rv,j,q){const x=rivFx(rv,j),w=INSTR.map(m=>m.b.reduce((a,b,k)=>a+b*x[k],0)/m.sig),v=pvol(w);const a=v>1e-9?rivV(rv)*rivRamp(q)/v:0;",
    "function rivBookQ(rv,j,q){const x=rivFx(rv,j),w=INSTR.map(m=>m.b.reduce((a,b,k)=>a+b*x[k],0)/m.sig),v=pvol(w);const a=v>1e-9?rivV(rv)*rivRamp(q-(rv.q0||0))/v:0;")
rep("  rv.mAum=S.aum0;rv.mHwm=S.aum0;rv.mgr=0;\n","  rv.mAum=S.aum0;rv.mHwm=S.aum0;rv.mgr=rv.mgr0||0;\n")
# tirage en début de partie
rep("evLog:[]};\n S.mgrSeed=","evLog:[]};\n rivDraw();   /* lot 157 */\n S.mgrSeed=")
# faillite à la clôture
rep("(rv.vqh=rv.vqh||[]).push(rivV(rv));rv.vqLast=rivV(rv);rivalMgrQuarter(rv,rr[j])});",
    "(rv.vqh=rv.vqh||[]).push(rivV(rv));rv.vqLast=rivV(rv);rivalMgrQuarter(rv,rr[j])});\n S.qRivNew=[];S.rivals.forEach((rv,j)=>{if((rv.mgr||0)<-1e-9){const o={nm:rv.nm,boss:rv.boss},nv=rivReplace(j);S.qRivNew.push({o,nv})}});   /* lot 157 */")
# débriefing : l'annonce
rep(" {const I=invs().filter(v=>v.ntc>0);",
    " (S.qRivNew||[]).forEach(x=>warn.push(`🏚️ <b>${x.o.nm} ferme ses portes</b> : la société de gestion de ${x.o.boss} n'a plus de trésorerie. <b>${x.nv.nm}</b> prend sa place, lancé par ${x.nv.boss}, ancien bras droit de ${x.o.boss} ; il part de zéro et monte en charge.`));\n {const I=invs().filter(v=>v.ntc>0);")
open('index.html','w',encoding='utf-8').write(s);print('lot157 ok')
s=open('index.html',encoding='utf-8').read()
rep("const h=(rv.hist||[]).slice(0,-1);rv.mgr=0;h.forEach(g=>rivalMgrQuarter(rv,g));","const h=(rv.hist||[]).slice(0,-1);rv.mgr=rv.mgr0||0;h.forEach(g=>rivalMgrQuarter(rv,g));")
open('index.html','w',encoding='utf-8').write(s);print('lot157 p1b ok')
