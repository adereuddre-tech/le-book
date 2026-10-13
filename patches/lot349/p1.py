p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# B : rentabilité du fonds, tout compris — même périmètre que le risque du fonds ; lue pour la rentabilité marginale.
# Le bot et le panneau du book gardent la « lecture des marchés » (profitBook).
rep("""function fundParts(k){k=k||S.k;const w=weights(k),st=volStress(w,undefined,covInfo()),ev=evVarExp(w).v,Vb=st*st+ev;
 const Pd=typeof xDeskP==='function'?xDeskP():0,bo=0.5+0.5*((S.bud&&TAILM[S.bud.risk])||1),h=S.xHint;let Q=[];
 if(h&&h.id){const sc=STRESS.find(x=>x.id===h.id);if(sc)Q=[[sc,1]]}
 if(!Q.length){let sw=0;STRESS.forEach(x=>{const p=xScP(x);if(p>0){Q.push([x,p]);sw+=p}});Q=sw>0?Q.map(([x,p])=>[x,p/sw]):[]}
 let E1=0,E2=0;Q.forEach(([x,q])=>{const L=(0.5*bo+0.5)*stressLoss(k,x);E1+=q*L;E2+=q*L*L});
 if(h&&h.t&&!h.id){const L=(0.5*bo+0.5)*xEvLoss(k,h.t);E1=L;E2=L*L}
""","""/* moments de la perte du book sur un extrême du trimestre, à la probabilité du desk (alerte nommée : ce scénario) */
function xMoments(k){const Pd=typeof xDeskP==='function'&&S.bud?xDeskP():0,bo=0.5+0.5*((S.bud&&TAILM[S.bud.risk])||1),h=S.xHint;let Q=[];
 if(h&&h.id){const sc=STRESS.find(x=>x.id===h.id);if(sc)Q=[[sc,1]]}
 if(!Q.length){let sw=0;STRESS.forEach(x=>{const p=xScP(x);if(p>0){Q.push([x,p]);sw+=p}});Q=sw>0?Q.map(([x,p])=>[x,p/sw]):[]}
 let E1=0,E2=0;Q.forEach(([x,q])=>{const L=(0.5*bo+0.5)*stressLoss(k,x);E1+=q*L;E2+=q*L*L});
 if(h&&h.t&&!h.id){const L=(0.5*bo+0.5)*xEvLoss(k,h.t);E1=L;E2=L*L}
 return {Pd,E1,E2}}
/* lot 349 : rentabilité du fonds, tout compris (trimestrielle) */
function fundRetParts(k){k=k||S.k;const k0=S.k0||S.k,w=weights(k);
 const lect=profitBook(k)-xBookTerm(k);
 let cx=0;for(let i=0;i<N;i++){const d=k[i]-k0[i];if(d){const t=tcost(d,i);cx+=(t.imp-(1+IMPK)*t.cost)/S.nav}}   /* le fonds paie la facture et le glissement, pas seulement l'impact */
 const XM=xMoments(k),ext=XM.Pd*XM.E1;
 const A=accP(k),sp=A.sp,spE=Math.max(sp,0.20+0.5*(A.mgu-MGZ.watch)),Lm=Math.min(0.6,TAILSEV*tailL(spE));
 let im=0;if(A.m>0)for(let m=0;m<N;m++){const d=Math.trunc(k[m]/2)-k[m];if(d)im+=tcost(d,m).cost*urgM(URG.tail,m)}
 const acc=-A.m*(0.8*Lm+Math.min(0.08,im/S.nav));
 const V=visList(k),pv=visP(k);let vl=0,vp=0;V.forEach(v=>{const H=v.kind==='short'?VIS.Hs:VIS.Hl,L=Math.min(0.6,Math.abs(w[v.i])*INSTR[v.i].sigQ*H*crowd(sp));vl+=v.p*0.8*L;vp+=v.p});
 const vis=vp>0?-pv*vl/vp:0;
 return {total:lect+cx+ext+acc+vis,lect,cx,ext,acc,vis,pd:XM.Pd}}
function fundRet(k){return fundRetParts(k).total}
function fundParts(k){k=k||S.k;const w=weights(k),st=volStress(w,undefined,covInfo()),ev=evVarExp(w).v,Vb=st*st+ev;
 const XM=xMoments(k),Pd=XM.Pd,E1=XM.E1,E2=XM.E2;
""")
# rentabilité marginale : fonds tout compris
rep("""  const ex1=pc2(profitBook(kp)-profitBook(S.k));""","""  const fr0=fundRet(S.k),ex1=pc2(fundRet(kp)-fr0);   /* lot 349 */""")
rep("""  const pM=pc2(profitBook(km)-profitBook(S.k)),""","""  const pM=pc2(fundRet(km)-fr0),""")
rep(""" const R=kk=>fundRisk(kk),dr=(R(k1)-R(S.k))*100,dp=profitBook(k1)-profitBook(S.k);""",""" const R=kk=>fundRisk(kk),dr=(R(k1)-R(S.k))*100,dp=fundRet(k1)-fundRet(S.k);""")
rep(""" const R0=fundRisk(S.k),P0=profitBook(S.k);""",""" const R0=fundRisk(S.k),P0=fundRet(S.k);""")
rep("""const dp=o.n!==0&&o.trades.length?profitBook(o.t)-P0:0,""","""const dp=o.n!==0&&o.trades.length?fundRet(o.t)-P0:0,""")
# panneau : la rentabilité du fonds à côté de son risque
rep(""" const FP=fundParts(k);
 return `<div class="kv"><span>Risque du fonds · book, extrêmes, collatéral</span><b>${dec(FP.total*50,1)} %</b></div>""",""" const FP=fundParts(k),FR=fundRetParts(k),p2=v=>`${v>=0?'+':'−'}${dec(Math.abs(v)*100,2)} %`;
 return `<div class="kv"><span>Rentabilité du fonds · tout compris, ce trimestre</span><b class="${cls(FR.total)}">${p2(FR.total)}</b></div>
  <p class="note" style="margin:0 0 4px">Lecture des marchés ${p2(FR.lect)} · fourchette, impact et glissement ${p2(FR.cx)} · extrêmes (${Math.round(FR.pd*100)} %) ${p2(FR.ext)} · accidents de levier et appels de marge ${p2(FR.acc)}${FR.vis?` · squeezes ${p2(FR.vis)}`:''}. C'est sur elle que se lit la rentabilité marginale des marchés.</p>
  <div class="kv"><span>Risque du fonds · book, extrêmes, collatéral</span><b>${dec(FP.total*50,1)} %</b></div>""")
rep("""   <p>Risque marginal : ce qu'une unité de plus (ou de moins) ajoute au risque du <em>fonds</em>""","""   <p>Rentabilité et risque marginaux se lisent sur le <em>fonds</em>, tout compris : lecture des marchés, fourchette, impact et glissement, extrêmes à la probabilité du desk, accidents de levier, appels de marge et squeezes, collatéral selon la marge. Le panneau du book montre la lecture des marchés seule.</p>
   <p>Risque marginal : ce qu'une unité de plus (ou de moins) ajoute au risque du <em>fonds</em>""")
open(p,'w',encoding='utf-8').write(s)
