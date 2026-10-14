p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# 1) calibrage des extrêmes sur le moteur : choc immédiat (moitié du mouvement, amorti, écart de cotation), suite −12,5 % du mouvement en moyenne
rep("""function xBookTerm(k){if(!S||!S.xHint||!S.bud)return 0;k=k||S.k;const h=S.xHint,P=xDeskP(),bo=0.5+0.5*(TAILM[S.bud.risk]||1);let L=0;
 if(h.id){const sc=STRESS.find(x=>x.id===h.id);L=sc?stressLoss(k,sc):0}
 else if(h.t)L=xEvLoss(k,h.t);
 else{let sw=0,sl=0;STRESS.forEach(x=>{const p=xScP(x);sw+=p;sl+=p*stressLoss(k,x)});L=sw>0?sl/sw:0}
 return P*(0.5*bo+0.5)*L}""","""/* lot 351 : perte attendue d'un extrême telle que le moteur l'applique — choc immédiat bo·(½·mouvement·foule − écart),
   puis la suite du mouvement, qui se retourne un peu en moyenne (−12,5 % du mouvement) */
const XCONT=-0.125;
function xLossE(k,sc){const w=weights(k),h=stressHit(sc,k);let v=0;INSTR.forEach((x,i)=>{if(h[x.sym])v+=w[i]*h[x.sym]*x.sigQ});
 const bo=0.5+0.5*((S.bud&&TAILM[S.bud.risk])||1),cr=v<0?crowd(riskShown(w).total):1;return bo*(0.5*v*cr-stressGap(k,sc))+XCONT*v}
function xLossT(k,t){const v=xEvLoss(k,t);return 0.5*v+XCONT*v}
function xBookTerm(k){if(!S||!S.xHint||!S.bud)return 0;k=k||S.k;const h=S.xHint,P=xDeskP();let L=0;
 if(h.id){const sc=STRESS.find(x=>x.id===h.id);L=sc?xLossE(k,sc):0}
 else if(h.t)L=xLossT(k,h.t);
 else{let sw=0,sl=0;STRESS.forEach(x=>{const p=xScP(x);sw+=p;sl+=p*xLossE(k,x)});L=sw>0?sl/sw:0}
 return P*L}""")
rep(""" let E1=0,E2=0;Q.forEach(([x,q])=>{const L=(0.5*bo+0.5)*stressLoss(k,x);E1+=q*L;E2+=q*L*L});
 if(h&&h.t&&!h.id){const L=(0.5*bo+0.5)*xEvLoss(k,h.t);E1=L;E2=L*L}""",""" let E1=0,E2=0;Q.forEach(([x,q])=>{const L=xLossE(k,x);E1+=q*L;E2+=q*L*L});
 if(h&&h.t&&!h.id){const L=xLossT(k,h.t);E1=L;E2=L*L}""")
# 2) une seule mesure affichée : lecture des marchés − ½·σ² trimestriel − perte moyenne des extrêmes (probabilité du desk)
rep("""function fundRet(k){return fundRetParts(k).total}""","""function fundRet(k){return fundRetParts(k).total}
/* lot 351 : rentabilité ajustée du risque — ce que montrent le panneau, les lignes et le nuage */
function riskCost(k){const sg=riskShown(weights(k)).total;return 0.5*(sg/2)*(sg/2)}
function adjParts(k){k=k||S.k;const lect=profitBook(k)-xBookTerm(k),XM=xMoments(k),ext=XM.Pd*XM.E1,rc=-riskCost(k);return {total:lect+ext+rc,lect,ext,rc,pd:XM.Pd}}
function adjRet(k){return adjParts(k).total}""")
rep("""  const fr0=fundRet(S.k),ex1=pc2(fundRet(kp)-fr0);   /* lot 349 */""","""  const fr0=adjRet(S.k),ex1=pc2(adjRet(kp)-fr0);   /* lot 351 : rentabilité ajustée du risque */""")
rep("""  const pM=pc2(fundRet(km)-fr0),""","""  const pM=pc2(adjRet(km)-fr0),""")
rep(""" const R=kk=>fundRisk(kk),dr=(R(k1)-R(S.k))*100,dp=fundRet(k1)-fundRet(S.k);""",""" const R=kk=>riskShown(weights(kk)).total,dr=(R(k1)-R(S.k))*100,dp=adjRet(k1)-adjRet(S.k);""")
rep(""" const R0=fundRisk(S.k),P0=fundRet(S.k);""",""" const R0=riskShown(weights(S.k)).total,P0=adjRet(S.k);""")
rep("""const dp=o.n!==0&&o.trades.length?fundRet(o.t)-P0:0,""","""const dp=o.n!==0&&o.trades.length?adjRet(o.t)-P0:0,""")
rep("""dr=o.n!==0&&o.trades.length?(fundRisk(o.t)-R0)*100:0;""","""dr=o.n!==0&&o.trades.length?(riskShown(weights(o.t)).total-R0)*100:0;""")
rep("""  const R=kk=>fundRisk(kk),r0=R(S.k),kp=[...S.k],km=[...S.k];kp[i]+=1;km[i]-=1;   /* lot 344 : risque du fonds */""","""  const R=kk=>riskShown(weights(kk)).total,r0=R(S.k),kp=[...S.k],km=[...S.k];kp[i]+=1;km[i]-=1;   /* lot 351 : le risque du panneau */""")
rep("""function riskMarg(i,k){const R=kk=>fundRisk(kk),""","""function riskMarg(i,k){const R=kk=>riskShown(weights(kk)).total,""")
rep("""function riskAdd(i,k){const k1=[...k];k1[i]=(k1[i]||0)+1;return (fundRisk(k1)-fundRisk(k))*100}""","""function riskAdd(i,k){const k1=[...k];k1[i]=(k1[i]||0)+1;return (riskShown(weights(k1)).total-riskShown(weights(k)).total)*100}""")
rep("""    ['Risque marginal du fonds (±1 unité)',`<b class="${rp>0?'neg-g':'pos-g'}">${rp>=0?'+':'−'}${dec(Math.abs(rp),1)} pt</b> sur ${Math.round(fundRisk(S.k)*100)}`],
    ['dont le book seul, vu du comité',(v=>`${v>=0?'+':'−'}${dec(Math.abs(v),1)} pt sur ${Math.round(riskShown(weights(S.k)).total*100)}`)(riskMargB(i,S.k))],""",
    """    ['Risque marginal (±1 unité)',`<b class="${rp>0?'neg-g':'pos-g'}">${rp>=0?'+':'−'}${dec(Math.abs(rp),1)} pt</b> sur ${Math.round(riskShown(weights(S.k)).total*100)}`],
    ['Sur le risque du fonds (extrêmes, collatéral)',(()=>{const R=kk=>fundRisk(kk),kp=[...S.k],km=[...S.k];kp[i]+=1;km[i]-=1;const v=(S.k.some(x=>x)?(R(kp)-R(km))/2:R(kp)-R(S.k))*100;return `${v>=0?'+':'−'}${dec(Math.abs(v),1)} pt sur ${Math.round(fundRisk(S.k)*100)}`})()],
    ['Rentabilité marginale tout compris (+1)',(v=>pc2(v))(fundRet((()=>{const a=[...S.k];a[i]+=1;return a})())-fundRet(S.k))],""")
rep("""   <p>Rentabilité et risque marginaux se lisent sur le <em>fonds</em>, tout compris : lecture des marchés, fourchette, impact et glissement, extrêmes à la probabilité du desk, accidents de levier, appels de marge et squeezes, collatéral selon la marge. Le panneau du book montre la lecture des marchés seule.</p>
   <p>Risque marginal : ce qu'une unité de plus (ou de moins) ajoute au risque du <em>fonds</em> — le book lu avec tout ce que sait le desk (tuyaux de facteurs et de marchés), les extrêmes à la probabilité du desk, le collatéral et la corrélation de ses défauts avec les extrêmes. Le comité, lui, ne juge que le book.</p>""",
    """   <p>Rentabilité affichée partout (panneau, lignes, nuage) : la lecture des marchés, moins le coût du risque (½ σ² du trimestre) et la perte moyenne des extrêmes à la probabilité du desk. Chaque unité rapporte un peu moins que la précédente. Risque marginal : celui du panneau, le book vu du comité.</p>
   <p>Les deux lignes « fonds » vont plus loin : le risque du book lu avec tout ce que sait le desk, les extrêmes, le collatéral et la corrélation de ses défauts avec les extrêmes ; la rentabilité avec la fourchette, l'impact et le glissement, les accidents de levier, les appels de marge et les squeezes.</p>""")
# nuage : la même rentabilité ajustée, pour vous comme pour les concurrents (avant le trimestre)
rep(""" const pr=profitBook(S.k),R=(S.rivals||[]).map((rv,j)=>{const p=rivPtLive(rv,j);p.x/=2;return Object.assign(p,{c:rivCol(j),nm:rv.nm})});""",
    """ const lvQ=S.phase==='events'&&S.live,pr=lvQ?profitBook(S.k):adjRet(S.k),R=(S.rivals||[]).map((rv,j)=>{const p=rivPtLive(rv,j);p.x/=2;if(!lvQ){const A=adjParts(S.k),sp0=riskShown(weights(S.k)).total,xr=sp0>0.02?A.ext/sp0:-tailExp(0.2)/0.2;p.y+=-0.5*p.x*p.x+xr*2*p.x}return Object.assign(p,{c:rivCol(j),nm:rv.nm})});   /* lot 351 */""")
rep("""{x:Math.sqrt((riskShown(weights(kB)).total/2)**2+cs*cs),y:profitBook(kB)}:null;""","""{x:Math.sqrt((riskShown(weights(kB)).total/2)**2+cs*cs),y:lvQ?profitBook(kB):adjRet(kB)}:null;""")
rep("""Rentabilité : rendement attendu du trimestre — collatéral (et ce que la marge lui retire), impact compris ;""","""Rentabilité : rendement attendu du trimestre — collatéral (et ce que la marge lui retire), impact compris, moins le coût du risque (½ σ²) et la perte moyenne des extrêmes à la probabilité du desk ;""")
rep(""" const cash=Math.max(0,mgrCash()),pb=profitBook(S.k),""",""" const cash=Math.max(0,mgrCash()),pb=adjRet(S.k),""")
open(p,'w',encoding='utf-8').write(s)
s=open(p,encoding='utf-8').read()
rep("""ni le drain de volatilité ni les événements extrêmes, qui dépendent du risque et se lisent sur l'axe horizontal ;""","""ni les accidents de levier ni les squeezes, détaillés dans la fenêtre de chaque marché ;""")
open(p,'w',encoding='utf-8').write(s)
