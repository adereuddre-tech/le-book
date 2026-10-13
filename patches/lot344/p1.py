p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# risque incrémental = risque du fonds : book lu avec toute l'information du desk (tuyaux de facteurs et de marchés),
# extrêmes à la probabilité du desk, collatéral et covariance de ses défauts avec les extrêmes. Le comité juge toujours le book seul.
rep("""function volStress(w,kap){
 kap=kap===undefined?MGC.kap():kap;
 let v=0;
 for(let i=0;i<N;i++)for(let j=0;j<N;j++){
  const CE=covE(),si=Math.sqrt(CE[i][i]),sj=Math.sqrt(CE[j][j]);""","""function volStress(w,kap,CEx){
 kap=kap===undefined?MGC.kap():kap;
 let v=0;const CE=CEx||covE();
 for(let i=0;i<N;i++)for(let j=0;j<N;j++){
  const si=Math.sqrt(CE[i][i]),sj=Math.sqrt(CE[j][j]);""")
rep("""function pvol(w){const CE=covE();""","""/* lot 344 : covariance vue avec toute l'information du desk. Un signal de sens juste à r sur une gaussienne centrée
   en réduit la variance de (2r−1)²·2/π : facteurs (Victoria, Sir Mervyn, l'intuition du flux) et marchés (tuyaux). */
function tipVarF(r){return 1-(2*r-1)*(2*r-1)*2/Math.PI}
let _CI=null,_CIk='';
function covInfo(){const base=covE();if(!S)return base;
 const EV=[1,1,1,1];if(S.vic&&S.vic.q===S.q)EV[S.vic.k]*=tipVarF(0.9);if(S.mer&&S.mer.q===S.q)EV[S.mer.k]*=tipVarF(0.85);if(S.hunch)EV[S.hunch.k]*=tipVarF(0.8);
 const rho=new Array(N).fill(1);(S.pwTips||[]).forEach(t=>{if(t.q===S.q&&t.i!=null&&t.rel)rho[t.i]*=tipVarF(t.rel)});
 const key=_CEk+'|'+EV.join(',')+'|'+rho.join(',');if(EV.every(v=>v===1)&&rho.every(v=>v===1))return base;if(_CI&&_CIk===key)return _CI;
 const sn=['t','c','v'].map(z=>typeof sigNoise==='function'&&S.bud?sigNoise(z):1),sv=SIGW.t**2*(sn[0]**2+0.1)+SIGW.c**2*(sn[1]**2+0.1)+SIGW.v**2*(sn[2]**2+0.1);
 _CI=[];for(let i=0;i<N;i++){_CI[i]=[];const xi=INSTR[i];for(let j=0;j<N;j++){const xj=INSTR[j];let c=0,bb=0;for(let k=0;k<K;k++){c+=xi.b[k]*xj.b[k]*EV[k];bb+=xi.b[k]*xj.b[k]}
  const a=Math.sqrt(rho[i]*rho[j]);_CI[i][j]=i===j?rho[i]*xi.sig**2*(EXPVF*c+Math.max(0,1-bb)+sv):a*xi.sig*xj.sig*EXPVF*c}}
 _CIk=key;return _CI}
/* risque du fonds, en vol annualisée comme riskShown : book (information du desk) + extrêmes + collatéral + covariance */
function fundParts(k){k=k||S.k;const w=weights(k),st=volStress(w,undefined,covInfo()),ev=evVarExp(w).v,Vb=st*st+ev;
 const Pd=typeof xDeskP==='function'?xDeskP():0,bo=0.5+0.5*((S.bud&&TAILM[S.bud.risk])||1),h=S.xHint;let Q=[];
 if(h&&h.id){const sc=STRESS.find(x=>x.id===h.id);if(sc)Q=[[sc,1]]}
 if(!Q.length){let sw=0;STRESS.forEach(x=>{const p=xScP(x);if(p>0){Q.push([x,p]);sw+=p}});Q=sw>0?Q.map(([x,p])=>[x,p/sw]):[]}
 let E1=0,E2=0;Q.forEach(([x,q])=>{const L=(0.5*bo+0.5)*stressLoss(k,x);E1+=q*L;E2+=q*L*L});
 if(h&&h.t&&!h.id){const L=(0.5*bo+0.5)*xEvLoss(k,h.t);E1=L;E2=L*L}
 const VX=Math.max(0,Pd*E2-(Pd*E1)**2);
 const o=colOpt();let VC=0,CV=0;
 if(!redOn('collat')&&o.p>0){const a=(1-Math.min(1,marginPct(k)))*o.l,ph=Math.min(0.95,COLK*o.p),pl=colPx(o,false),pD=Pd*ph+(1-Pd)*pl;
  VC=a*a*pD*(1-pD);CV=-a*Pd*E1*(ph-pD)}
 const V=Vb+4*(VX+VC+2*CV);
 const T=Math.sqrt(Math.max(0,V));return {total:T,book:Math.sqrt(Vb),x:Math.sqrt(4*VX),col:Math.sqrt(4*VC),cov:T-Math.sqrt(Math.max(0,V-8*CV)),pd:Pd}}
function fundRisk(k){return fundParts(k).total}
function pvol(w){const CE=covE();""")
rep("""function riskMarg(i,k){const R=kk=>riskShown(weights(kk)).total,""","""function riskMarg(i,k){const R=kk=>fundRisk(kk),""")
rep("""function riskAdd(i,k){const k1=[...k];k1[i]=(k1[i]||0)+1;return (riskShown(weights(k1)).total-riskShown(weights(k)).total)*100}""",
    """function riskAdd(i,k){const k1=[...k];k1[i]=(k1[i]||0)+1;return (fundRisk(k1)-fundRisk(k))*100}""")
rep("""  const R=kk=>riskShown(weights(kk)).total,r0=R(S.k),kp=[...S.k],km=[...S.k];kp[i]+=1;km[i]-=1;""","""  const R=kk=>fundRisk(kk),r0=R(S.k),kp=[...S.k],km=[...S.k];kp[i]+=1;km[i]-=1;   /* lot 344 : risque du fonds */""")
rep(""" const R=kk=>riskShown(weights(kk)).total,dr=(R(k1)-R(S.k))*100,dp=profitBook(k1)-profitBook(S.k);""",""" const R=kk=>fundRisk(kk),dr=(R(k1)-R(S.k))*100,dp=profitBook(k1)-profitBook(S.k);""")
rep(""" const R0=riskShown(weights(S.k)).total,P0=profitBook(S.k);""",""" const R0=fundRisk(S.k),P0=profitBook(S.k);""")
rep("""dr=o.n!==0&&o.trades.length?(riskShown(weights(o.t)).total-R0)*100:0;""","""dr=o.n!==0&&o.trades.length?(fundRisk(o.t)-R0)*100:0;""")
rep("""    ['Risque marginal (±1 unité)',`<b class="${rp>0?'neg-g':'pos-g'}">${rp>=0?'+':'−'}${dec(Math.abs(rp),1)} pt</b> sur ${Math.round(riskShown(weights(S.k)).total*100)}`],""",
    """    ['Risque marginal du fonds (±1 unité)',`<b class="${rp>0?'neg-g':'pos-g'}">${rp>=0?'+':'−'}${dec(Math.abs(rp),1)} pt</b> sur ${Math.round(fundRisk(S.k)*100)}`],
    ['dont le book seul, vu du comité',(v=>`${v>=0?'+':'−'}${dec(Math.abs(v),1)} pt sur ${Math.round(riskShown(weights(S.k)).total*100)}`)(riskMargB(i,S.k))],""")
rep("""function riskAdd(i,k){""","""function riskMargB(i,k){const R=kk=>riskShown(weights(kk)).total,kp=[...k],km=[...k];kp[i]=(kp[i]||0)+1;km[i]=(km[i]||0)-1;return (k.some(v=>v)?(R(kp)-R(km))/2:R(kp)-R(k))*100}
function riskAdd(i,k){""")
rep("""   <p><em>Tendance</em> — ${TCVTXT.t.d}</p>""","""   <p>Risque marginal : ce qu'une unité de plus (ou de moins) ajoute au risque du <em>fonds</em> — le book lu avec tout ce que sait le desk (tuyaux de facteurs et de marchés), les extrêmes à la probabilité du desk, le collatéral et la corrélation de ses défauts avec les extrêmes. Le comité, lui, ne juge que le book.</p>
   <p><em>Tendance</em> — ${TCVTXT.t.d}</p>""")
# panneau des limites : le risque du fonds à côté du risque du comité
rep(""" return `<div class="kv"><span>Limite du comité · risque ex ante${ng==='vol'?' (négociée)':''}</span>""",""" const FP=fundParts(k);
 return `<div class="kv"><span>Risque du fonds · book, extrêmes, collatéral</span><b>${dec(FP.total*50,1)} %</b></div>
  <p class="note" style="margin:0 0 4px">Book lu par le desk ${dec(FP.book*50,1)} % · extrêmes (${Math.round(FP.pd*100)} %) ${dec(FP.x*50,1)} % · collatéral ${dec(FP.col*50,1)} %${Math.abs(FP.cov)>5e-5?` · dont corrélation défauts–extrêmes ${FP.cov>=0?'+':'−'}${dec(Math.abs(FP.cov)*50,2)} %`:''}. C'est sur lui que se lit le risque marginal des marchés.</p>
  <div class="kv"><span>Limite du comité · risque ex ante${ng==='vol'?' (négociée)':''}</span>""")
open(p,'w',encoding='utf-8').write(s)
