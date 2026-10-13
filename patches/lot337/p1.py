p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# la veille des extrêmes entre dans l'attendu du book : une alerte y met la perte attendue de l'extrême, à la probabilité du desk
rep("""function xWatchTxt(){""","""/* lot 337 : probabilité d'un extrême ce trimestre pour le desk, sachant l'alerte (ou son absence) — Bayes sur la veille */
function xDeskP(){const T=xProbTot();if(!(T>0))return 0;const W=xWatch();
 return S.xHint?W.s*T/Math.max(1e-9,W.s*T+W.fa*(1-T)):(1-W.s)*T/Math.max(1e-9,(1-W.s)*T+(1-W.fa)*(1-T))}
/* perte attendue sur le book d'un extrême signalé (mouvement complet, choc immédiat amorti par le contrôle des risques) */
function xBookTerm(k){if(!S||!S.xHint||!S.bud)return 0;k=k||S.k;const h=S.xHint,P=xDeskP(),bo=0.5+0.5*(TAILM[S.bud.risk]||1);let L=0;
 if(h.id){const sc=STRESS.find(x=>x.id===h.id);L=sc?stressLoss(k,sc):0}
 else if(h.t)L=xEvLoss(k,h.t);
 else{let sw=0,sl=0;STRESS.forEach(x=>{const p=xScP(x);sw+=p;sl+=p*stressLoss(k,x)});L=sw>0?sl/sw:0}
 return P*(0.5*bo+0.5)*L}
function xWatchTxt(){""")
rep("""const sg=riskShown(w).total;return m-FINK*(sg/0.2)*(sg/0.2);   /* lot 85 : lecture des marchés, moins le financement facturé ; ni accidents ni drain */""",
    """const sg=riskShown(w).total;return m-FINK*(sg/0.2)*(sg/0.2)+xBookTerm(k);   /* lot 85 : lecture des marchés, moins le financement facturé ; ni accidents ni drain ; lot 337 : l'extrême signalé */""")
rep(""" return `🔴 ${who} ${what}${ch}`}""",""" const bt=k?xBookTerm(k):0;
 return `🔴 ${who} ${what}${ch}${Math.abs(bt)>1e-6?` Déjà dans la rentabilité estimée du book, à ${Math.round(xDeskP()*100)} % de probabilité pour votre desk : ${sgnp(bt,2)}.`:''}`}""")
open(p,'w',encoding='utf-8').write(s)
