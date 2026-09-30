# Lot 110 : fonds de fonds jugé sur la moyenne des concurrents ; objectif du trimestre sur la page du book ; les
# concurrents subissent le vrai P&L des événements extrêmes sur leur portefeuille implicite ; facteur « dollar »
# présenté comme facteur « liquidité », de sens inverse (affichage seul : charges et tirages inchangés, liquidité = −dollar) ;
# motivation du desk recalibrée (le bonus ne se payait pas : 20 % coûtait 1,95 M$ pour 0,8 M$ de coûts évités).
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
def region(a,b,o,n,k):
    global s; i=s.index(a); j=s.index(b,i+len(a)); seg=s[i:j]; c=seg.count(o); assert c==k,(a[:30],o[:30],c); s=s[:i]+seg.replace(o,n)+s[j:]

# 1. fonds de fonds : moyenne
rep("const tot=invClose({r:qTotal,med,ddp:","const avgR=S.rivals.reduce((a,x)=>a+(x.last||0),0)/Math.max(1,S.rivals.length);\n const tot=invClose({r:qTotal,med:avgR,ddp:")
rep("rule:\"rachète si vous finissez 3 points sous la médiane des concurrents ; souscrit 3 points au-dessus.\"}","rule:\"rachète si vous finissez 3 points sous la moyenne des concurrents ; souscrit 3 points au-dessus.\"}")

# 2. objectif du trimestre sur la page du book
rep("function renderRisk(){\n const w=weights(S.k),sp=pvol(w),vd=varDecomp(w),rc=riskContrib(w);",
    "function objRows(){const g=VOL().goal/4,c=S.comm&&S.comm.ret!=null?S.comm:null;\n return `<div class=\"flag\" style=\"border-left:3px solid var(--gold)\"><span>🎯 <b>Objectif du trimestre</b> : ${sgnp(c?c.ret:g,1)} net${c?` (annonce « ${c.nm.toLowerCase()} »)`:` (mandat : ${sgnp(VOL().goal,1)} par an)`}. Le fonds souverain juge sur cet objectif, la caisse de retraite sur la régularité, le family office sur le signe, le fonds de fonds sur la moyenne des concurrents.${S.goal?`<br>Objectif de place : <b>${S.goal.nm}</b> — ${S.goal.d}`:''}</span></div>`}\nfunction renderRisk(){\n const w=weights(S.k),sp=pvol(w),vd=varDecomp(w),rc=riskContrib(w);")
rep("  ${S.xHint?`<div class=\"flag xh\">","  ${objRows()}\n  ${S.xHint?`<div class=\"flag xh\">")

# 3. concurrents : portefeuille implicite, vrai P&L de l'événement
i=s.index("function xRivHit(id){");j=s.index("function rivalReturns(){",i)
s=s[:i]+r'''/* expositions factorielles implicites d'un concurrent ce trimestre : mêmes tirages que rivalE (même graine) */
function rivFx(rv,j){const u=prng32(hash32('rivk'+j+'_'+S.q,S.seed)),f=S.f||[0,0,0,0],sg=k=>Math.sign(f[k]||1),st=rv.style||'fonda',x=[0,0,0,0];
 if(st==='syst'){for(let k=0;k<K;k++)x[k]=(u()<rv.skill?1:-1)*sg(k)*0.9;return x}
 if(st==='flux'){const p=S.fLast;for(let k=0;k<K;k++){const s0=p&&p[k]?Math.sign(p[k]):(u()<0.5?1:-1);const ok=Math.sign(f[k]||1)===s0||u()<(rv.skill-0.5)*1.8;x[k]=(ok?1:-1)*sg(k)*1.1}return x}
 let km=0;for(let k=1;k<K;k++)if(Math.abs(f[k])>Math.abs(f[km]))km=k;x[km]=(u()<rv.skill?1:-1)*sg(km)*1.8;
 for(let k=0;k<K;k++)if(k!==km)x[k]=(u()<0.55?1:-1)*sg(k)*0.4;return x}
/* book implicite : projection des expositions sur les marchés ouverts, à la vol du concurrent */
function rivBookW(rv,j){const x=rivFx(rv,j),w=INSTR.map(m=>m.b.reduce((a,b,k)=>a+b*x[k],0)/m.sig),v=pvol(w);const a=v>1e-9?rivV(rv)/v:0;return w.map(z=>z*a)}
const XRIVR=0.75;   /* part du mouvement complet que les concurrents encaissent, en moyenne après réaction */
function xRivHit(id){const sc=STRESS.find(x=>x.id===id);if(!sc)return;
 S.xRiv=S.rivals.map((rv,j)=>{const w=rivBookW(rv,j),h=stressHit(sc,w.map(z=>z*100));let v=0;INSTR.forEach((m,i)=>{if(h[m.sym])v+=w[i]*h[m.sym]*m.sigQ});
  if(v<0)v*=crowd(rivV(rv));return ((S.xRiv||[])[j]||0)+XRIVR*v});
 toast('Les concurrents encaissent aussi, selon leur portefeuille : '+S.rivals.map((rv,j)=>`${rv.nm} ${sgnp(S.xRiv[j],1)}`).join(' · '))}
'''+s[j:]

# 4. facteur liquidité (affichage : liquidité = −dollar)
rep("{id:'D',nm:'Dollar'}","{id:'L',nm:'Liquidité'}")
rep("const FACT=[","const FSG=[1,1,-1,1];   /* lot 110 : le facteur 2 s'affiche comme la liquidité mondiale, de sens inverse au dollar */\nconst FACT=[")
rep("${r.v.map((z,k)=>`<i class=\"${z>0?'up':z<0?'dn':''}\">${FACT[k].id} ${chip(z)}</i>`)","${r.v.map((z0,k)=>{const z=z0*FSG[k];return `<i class=\"${z>0?'up':z<0?'dn':''}\">${FACT[k].id} ${chip(z)}</i>`})")
rep("b.forEach(r=>{const p=r.p||RELP[r.rel];z+=(2*p-1)*r.v[k]/2});return z;","b.forEach(r=>{const p=r.p||RELP[r.rel];z+=(2*p-1)*r.v[k]/2});return z*FSG[k];")
rep("const fg=k=>{const v=ex[k],","const fg=k=>{const v=ex[k]*FSG[k],")
rep("['Crois.','Infl.','Dollar','Appét.'][k]","['Crois.','Infl.','Liquid.','Appét.'][k]")
rep("const FN=['Croissance','Inflation','Dollar','Appétit'];","const FN=['Croissance','Inflation','Liquidité','Appétit'];")
rep(" const ex=x.b.map((b,k)=>{const a=Math.abs(b);"," const ex=x.b.map((b0,k)=>{const b=b0*FSG[k],a=Math.abs(b);")
rep("const bw=x.b.map((b,k)=>`${FACT[k].nm}","const bw=x.b.map((b0,k)=>{const b=b0*FSG[k];return `${FACT[k].nm}")
rep("${b>=0?'+':'−'}${dec(Math.abs(b),2)}</span>`).join(' · ');\n const t1=tcost(1,i);","${b>=0?'+':'−'}${dec(Math.abs(b),2)}</span>`}).join(' · ');\n const t1=tcost(1,i);")
A="else if(id[0]==='f'){";B="\n } "
region(A,B,"v:w[i]*x.sig*x.b[k]","v:sg*w[i]*x.sig*x.b[k]",1)
region(A,B,"b=${o.x.b[k]>=0?'+':'−'}${dec(Math.abs(o.x.b[k]),2)}","b=${sg*o.x.b[k]>=0?'+':'−'}${dec(Math.abs(o.x.b[k]),2)}",1)
region(A,B,"ex[k]","exk",5)
region(A,B,"const k=+id[1],f=FACT[k];","const k=+id[1],f=FACT[k],sg=FSG[k],exk=ex[k]*sg;",1)
region(A,B,"(S.fLast[k]>=0?'+':'−')","(sg*S.fLast[k]>=0?'+':'−')",1)
rep("va surprendre ${S.hunch.up?'à la hausse':'à la baisse'} ce trimestre.</p>","va surprendre ${(S.hunch.up===(FSG[S.hunch.k]>0))?'à la hausse':'à la baisse'} ce trimestre.</p>")
rep("va ${S.hunch.up?'surprendre à la hausse':'surprendre à la baisse'} ce tr","va ${(S.hunch.up===(FSG[S.hunch.k]>0))?'surprendre à la hausse':'surprendre à la baisse'} ce tr")
rep("passe de ${S.rupture.old>=0?'+':'−'}${dec(Math.abs(S.rupture.old),2)} à ${S.rupture.nw>=0?'+':'−'}","passe de ${S.rupture.old*FSG[S.rupture.k]>=0?'+':'−'}${dec(Math.abs(S.rupture.old),2)} à ${S.rupture.nw*FSG[S.rupture.k]>=0?'+':'−'}")
rep("msg.push(`Exposition « ${FACT[k].nm.toLowerCase()} » ramenée de ${dec((e0*100),1)} à ${dec((factorExpo(weights(S.k))[k]*100),1)} pts de vol.`)","msg.push(`Exposition « ${FACT[k].nm.toLowerCase()} » ramenée de ${dec((FSG[k]*e0*100),1)} à ${dec((FSG[k]*factorExpo(weights(S.k))[k]*100),1)} pts de vol.`)")
rep("{nm:\"Dollar neutre\",d:\"Terminer avec une exposition au facteur dollar inférieure à 2 % en valeur absolue.\"","{nm:\"Liquidité neutre\",d:\"Terminer avec une exposition au facteur liquidité inférieure à 2 % en valeur absolue.\"")

# 5. motivation : cible concave, plus rapide, effet propre sur les coûts (×1,15 démotivé → ×0,85 motivé)
rep("MOT={m0:0.30,k:0.5,up:0.10,dn:0.18,poach:0.8,cut:1.6,i0:2};","MOT={m0:0.30,k:0.7,up:0.10,dn:0.18,poach:0.8,cut:1.6,i0:2,lo:1.15,hi:0.85};\nfunction motTg(i){return Math.sqrt(BONUS[i]/0.20)}")
rep("function execMot(i){const e=EXECM[i==null?S.bud.exec:i];return e<1?1-(1-e)*(0.5+0.5*motNow()):e}",
    "function execMot(i){const e=EXECM[i==null?S.bud.exec:i],m=motNow();return (e<1?1-(1-e)*(0.5+0.5*m):e)*(MOT.lo+(MOT.hi-MOT.lo)*m)}")
rep("const tg=perf>0?BONUS[i]/0.20:0;let m=motNow();","const tg=perf>0?motTg(i):0;let m=motNow();")
rep("const proj=i=>{const d=i-prev,tg=pf>0?BONUS[i]/0.20:0;","const proj=i=>{const d=i-prev,tg=pf>0?motTg(i):0;")
open('index.html','w',encoding='utf-8').write(s);print('lot110 p1 ok')
