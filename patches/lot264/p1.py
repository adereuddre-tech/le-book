p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
# 1. un seul tirage d'extrême par trimestre, deux familles dans un même catalogue
rep(""" {const u=prng32(hash32('stress'+S.q,S.seed));S.stressQ=null;if(u()<stressP()){const wt=STRESS.map(x=>x.ext?1/3:1),tw=wt.reduce((a,b)=>a+b,0);let r=u()*tw,si=0;while(si<STRESS.length-1&&r>=wt[si]){r-=wt[si];si++}
   const sc=STRESS[si],ev=stressEv(sc.id);if(ev){S.stressQ=sc.id;S.evQueue.splice(1+Math.floor(u()*S.evQueue.length),0,ev)}}}   /* lot 101 */""",
""" {const u=prng32(hash32('stress'+S.q,S.seed));S.stressQ=null;if(u()<xProbTot()){   /* lot 264 : un seul tirage, un seul catalogue */
   const pS=stressP(),pX=S.q>=1?XPROB:0,mac=u()<pX/(pS+pX);let sc=null;
   if(mac){S.usedX=S.usedX||[];let av=STRESS.filter(x=>x.mac&&!S.usedX.includes(x.id));if(!av.length){S.usedX=[];av=STRESS.filter(x=>x.mac)}sc=av[Math.floor(u()*av.length)];S.usedX.push(sc.id)}
   else{const C=STRESS.filter(x=>!x.mac),wt=C.map(x=>x.ext?1/3:1),tw=wt.reduce((a,b)=>a+b,0);let r=u()*tw,si=0;while(si<C.length-1&&r>=wt[si]){r-=wt[si];si++}sc=C[si]}
   const ev=stressEv(sc.id);if(ev){S.stressQ=sc.id;S.evQueue.splice(1+Math.floor(u()*S.evQueue.length),0,ev)}}}   /* lot 101 */""")
rep(""" /* lot 58 : un événement extrême, une fois tous les six ou sept trimestres (tirage pur, aucun flux déplacé) */
 if(S.q>=1){const u=prng32(hash32('xev'+S.q,S.seed));
  if(u()<XPROB){S.usedX=S.usedX||[];let av=MACROEV.filter(e=>e.x&&!S.usedX.includes(e.t));if(!av.length){S.usedX=[];av=MACROEV.filter(e=>e.x)}
   if(av.length){const e=av[Math.floor(u()*av.length)];S.usedX.push(e.t);S.evQueue.splice(Math.floor(u()*(S.evQueue.length+1)),0,e)}}}
""","")
# 2. conversion des dépêches extrêmes (x:1) en scénarios du catalogue, chocs à l'identique (x = h / (STRESSK × 1,5))
rep("""const STRESSK=0.32,STRGAP=0.28;""","""const STRESSK=0.32,STRGAP=0.28;
/* lot 264 : les dépêches extrêmes rejoignent le catalogue ; même calcul sur le book, même veille, même protection */
MACROEV.filter(e=>e.x).forEach((e,j)=>{const x={};for(const sy in e.hit)x[sy]=e.hit[sy]/(STRESSK*1.5);
 STRESS.push({id:'mx'+j,mac:1,nm:e.t,t0:e.t,who:e.who,x,sh:[0,0,0,0],p:e.p,...(e.liq?{liq:e.liq}:{}),...(e.shut?{shut:e.shut}:{})})});
/* probabilité qu'un extrême frappe ce trimestre, et celle de chaque scénario */
function xProbTot(){return 1-(1-stressP())*(1-((S&&S.q>=1)?XPROB:0))}
function xScP(sc){const pS=stressP(),pX=(S&&S.q>=1)?XPROB:0,T=xProbTot();if(!sc||T<=0)return 0;
 if(sc.mac)return T*pX/(pS+pX)/Math.max(1,STRESS.filter(x=>x.mac).length);
 const C=STRESS.filter(x=>!x.mac),tw=C.reduce((a,x)=>a+(x.ext?1/3:1),0);return T*pS/(pS+pX)*(sc.ext?1/3:1)/tw}""")
rep("""function stressEv(id){const sc=STRESS.find(x=>x.id===id);if(!sc)return null;return {stress:id,t:`Événement extrême : ${sc.nm.charAt(0).toLowerCase()+sc.nm.slice(1)}`,who:sc.ext?'Événement extrême · le plus rare':'Événement extrême',""",
    """function stressEv(id){const sc=STRESS.find(x=>x.id===id);if(!sc)return null;return {stress:id,t:sc.mac?sc.t0:`Événement extrême : ${sc.nm.charAt(0).toLowerCase()+sc.nm.slice(1)}`,who:sc.mac?sc.who:sc.ext?'Événement extrême · le plus rare':'Événement extrême',""")
# 3. protection et probabilités affichées
rep("""function hedgeEV(){const k=S.k,bo=0.5+0.5*(TAILM[S.bud.risk]||1),wt=STRESS.map(x=>x.ext?1/3:1),tw=wt.reduce((a,b)=>a+b,0),pS=stressP(),pX=S.q>=1?XPROB:0;
 let e=0;STRESS.forEach((x,j)=>{e+=pS*wt[j]/tw*Math.max(0,-0.5*bo*stressLoss(k,x))});
 const xs=MACROEV.filter(m=>m.x);xs.forEach(m=>{e+=pX/xs.length*Math.max(0,-0.5*xEvLoss(k,m.t))});return HEDGE.h*e}""",
    """function hedgeEV(){const k=S.k,bo=0.5+0.5*(TAILM[S.bud.risk]||1);let e=0;STRESS.forEach(x=>{e+=xScP(x)*Math.max(0,-0.5*bo*stressLoss(k,x))});return HEDGE.h*e}   /* lot 264 */""")
rep("""function xMktP(e){if(e.t){const n=MACROEV.filter(m=>m.x).length;return (S.q>=1?XPROB:0)/Math.max(1,n)}
 const wt=STRESS.map(x=>x.ext?1/3:1),tw=wt.reduce((a,b)=>a+b,0),j=STRESS.findIndex(x=>x.id===e.id);return j<0?0:stressP()*wt[j]/tw}""",
    """function xMktP(e){return xScP(STRESS.find(x=>x.id===e.id))}   /* lot 264 */""")
rep("""function hedgeBlock(){const e=xImmEst(),pX=1-(1-stressP())*(1-(S.q>=1?XPROB:0)),""","""function hedgeBlock(){const e=xImmEst(),pX=xProbTot(),""")
rep("""l'un d'eux frappe ce trimestre avec une probabilité de ${Math.round(stressP()*100)} %""","""l'un d'eux frappe ce trimestre avec une probabilité de ${Math.round(xProbTot()*100)} %""")
open(p,'w',encoding='utf-8').write(s)
