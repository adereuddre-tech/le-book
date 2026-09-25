# -*- coding: utf-8 -*-
"""Lot 60 — lignes de marché lisibles et identiques aux trois niveaux, risque avec bruit
d'estimation, collatéral espéré payé d'avance, cases grisées tenues à jour, équilibrage.

Risque : le modèle (COV) supposait des facteurs de variance 1 et ignorait le bruit des
indicateurs. Le rendement réel d'un marché s'écarte de ce que le joueur estime par la variance
résiduelle des facteurs après lecture des sources (EXPVF = 1,15, calibrée) et par le bruit des
signaux T/C/V (SIGW² × (bruit² + 0,1), celui de expRet). covE() porte ces deux termes :
facteurs × EXPVF hors diagonale et sur la diagonale, bruit des signaux sur la diagonale.
pvol, riskContrib et volStress la lisent : risque par marché, risque du book, bande, cartons.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
# ── covariance prédictive ──
e.rep("function pvol(w){let v=0;for(let i=0;i<N;i++)for(let j=0;j<N;j++)v+=w[i]*w[j]*COV[i][j];return Math.sqrt(Math.max(v,0))}",
"""/* lot 60 : covariance vue du gérant = facteurs (variance résiduelle EXPVF) + idiosyncrasique
   + bruit d'estimation des indicateurs. Mise en cache par état du bruit. */
let _CE=null,_CEk='';
function covE(){
 const sn=['t','c','v'].map(z=>typeof sigNoise==='function'&&S&&S.bud?sigNoise(z):1);
 let h=N*7919+sn[0]*13+sn[1]*17+sn[2]*19;for(let i=0;i<N;i++){const b=INSTR[i].b;h+=(i+1)*(b[0]*3.1+b[1]*5.3+b[2]*7.7+b[3]*11.9)}
 const key=h;
 if(_CE&&_CEk===key)return _CE;
 const sv=SIGW.t**2*(sn[0]**2+0.1)+SIGW.c**2*(sn[1]**2+0.1)+SIGW.v**2*(sn[2]**2+0.1);
 _CE=[];for(let i=0;i<N;i++){_CE[i]=[];const xi=INSTR[i];for(let j=0;j<N;j++){const xj=INSTR[j];
  let c=0;for(let k=0;k<K;k++)c+=xi.b[k]*xj.b[k];
  if(i===j){const bb=c;_CE[i][j]=xi.sig**2*(EXPVF*bb+Math.max(0,1-bb)+sv)}
  else _CE[i][j]=xi.sig*xj.sig*EXPVF*c}}
 _CEk=key;return _CE;
}
function pvol(w){const CE=covE();let v=0;for(let i=0;i<N;i++)for(let j=0;j<N;j++)v+=w[i]*w[j]*CE[i][j];return Math.sqrt(Math.max(v,0))}""")
e.rep(" return w.map((wi,i)=>{let s=0;for(let j=0;j<N;j++)s+=COV[i][j]*w[j];return wi*s/sp})}",
      " const CE=covE();return w.map((wi,i)=>{let s=0;for(let j=0;j<N;j++)s+=CE[i][j]*w[j];return wi*s/sp})}")
e.rep("""  const si=INSTR[i].sig,sj=INSTR[j].sig;
  let rho=i===j?1:COV[i][j]/(si*sj);""","""  const CE=covE(),si=Math.sqrt(CE[i][i]),sj=Math.sqrt(CE[j][j]);
  let rho=i===j?1:CE[i][j]/(si*sj);""")
# ── coût : fourchette et impact séparés ──
e.rep(""" bp*=m;
 const cost=bn*bp*1e-4;
 return {cost,bp,bn};""",""" bp*=m;
 const cost=bn*bp*1e-4,spr=Math.min(cost,bn*x.s*TCK*m*1e-4);
 return {cost,bp,bn,spr,imp:cost-spr};""")
# ── affichage identique aux trois niveaux ──
e.rep(" const lv=S.size||'mid',r=o.s>0?o.m/o.s:0;"," const lv='small',r=o.s>0?o.m/o.s:0;   /* lot 60 : même affichage aux trois niveaux */")
e.rep(""" if((S.size||'mid')==='mega'){const n=Math.min(3,Math.floor(Math.abs(r)/0.35));return `<span class="${o.m>=0?'pos-g':'neg-g'}">${n?(o.m>=0?'▲':'▼').repeat(n):'·'}</span>`}
""","")
e.rep("/* Affichage dosé : facile = chiffres et intervalle, moyen = barre et attendu, difficile = sens et conviction. */","/* lot 60 : chiffres et intervalle à tous les niveaux. */")
# ── ligne de marché : ordre, attendu, risque +1 / −1, coût, impact ──
old_a=" let gl='';\n if(mktOpen(i)&&S.tcvEst){"
i0=e.s.index(old_a); i1=e.s.index(" el.innerHTML=`<span class=\"fxe\">${ex}</span>",i0)
seg=e.s[i0:i1]
exs=seg[seg.index(" /* expositions aux quatre facteurs"):seg.index(" const k0=S.k0")]
e.rep(seg,exs+""" let gl='';
 if(mktOpen(i)){
  const R=kk=>riskShown(weights(kk)).total,r0=R(S.k),kp=[...S.k],km=[...S.k];kp[i]+=1;km[i]-=1;
  const rP=(R(kp)-r0)*100,rM=(R(km)-r0)*100,rc=v=>`<b class="${v>0.05?'neg-g':v<-0.05?'pos-g':'dim-g'}">${v>=0?'+':'−'}${dec(Math.abs(v),1)} pt</b>`;
  let ex1='<b class="dim-g">—</b>';
  if(S.tcvEst){const o=expRet(i),w1=U/x.sig,g={m:w1*o.m,s:w1*o.s};ex1=`<b class="${cls(g.m)}">${g.m>=0?'+':'−'}${dec(Math.abs(g.m*100),1)} %</b><i>±${dec(2*g.s*100,1)}</i>`}
  const k0=S.k0?S.k0[i]:S.k[i],d=S.k[i]-k0,t=tcost(d,i);
  const od=d>0?`<b class="pos-g">achat ${d}</b>`:d<0?`<b class="neg-g">vente ${-d}</b>`:'<b class="dim-g">aucun</b>';
  gl=`<div class="rgrid"><span>Ordre</span><span>Attendu /u</span><span>Risque +1</span><span>Risque −1</span><span>Coût</span><span>Impact</span>
   <div>${od}</div><div>${ex1}</div><div>${rc(rP)}</div><div>${rc(rM)}</div><div><b>${mm(t.spr||0)}</b></div><div><b>${mm(t.imp||0)}</b></div></div>`}
""")
e.rep(" el.innerHTML=`<span class=\"fxe\">${ex}</span><span class=\"fx\">${gl}</span>${right?`<span class=\"ord\">${right}</span>`:''}`;",
      " el.innerHTML=`<span class=\"fxe\">${ex}</span>${gl}`;")
e.rep(".rowinfo .xk{color:var(--dimmer);font-size:10.5px;margin-right:3px}",""".rowinfo .xk{color:var(--dimmer);font-size:10.5px;margin-right:3px}
.rgrid{display:grid;grid-template-columns:1.05fr 1.25fr 1fr 1fr .95fr .95fr;gap:0 6px;margin-top:5px;width:100%;font-family:var(--mono);align-items:baseline}
.rgrid span{font-size:9.5px;color:var(--dimmer);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-family:var(--sans,inherit)}
.rgrid div{font-size:11px;white-space:nowrap}.rgrid div b{font-weight:600}.rgrid div i{font-style:normal;color:var(--dimmer);font-size:9.5px;margin-left:2px}""")
# ── cases grisées : toutes les lignes recalculées à chaque changement ──
e.rep("""function updateRow(i){
 const seg=app.querySelector(`.seg[data-row="${i}"]`);if(!seg)return;
 seg.querySelectorAll('button').forEach(b=>{const v=+b.dataset.v;b.classList.remove('on','lit');""","""function updateRow(i){
 /* lot 60 : la facture des autres lignes change ce qui reste payable : toutes les cases sont revues */
 app.querySelectorAll('.seg button').forEach(b=>{const j=+b.dataset.i,v=+b.dataset.v;if(isNaN(j))return;
  const dis=S.k[j]!==v&&(Math.abs(v)>kCap(j)||!segAfford(j,v));b.disabled=dis;if(j!==i)b.setAttribute('style',segStyle(j,v,dis))});
 const seg=app.querySelector(`.seg[data-row="${i}"]`);if(!seg)return;
 seg.querySelectorAll('button').forEach(b=>{const v=+b.dataset.v;b.classList.remove('on','lit');""")
# ── collatéral : l'espérance est versée à l'ouverture, l'écart à la clôture ──
e.rep("""   S.budBp=bp;planSignalsAfterBudget();phaseDesk();""","""   S.budBp=bp;
   if(S.colPaidQ!==S.q){const o=colOpt(),ex=colYield()-(redOn('collat')?0:o.p*o.l);   /* lot 60 */
    S.colPaidQ=S.q;S.colBaseNav=S.nav;S.qColM=ex*S.nav;S.nav+=S.qColM;
    toast(`Collatéral : espérance du trimestre versée, <b>${mm(S.qColM)}</b>${o.p&&!redOn('collat')?` · l'écart éventuel à la clôture`:''}`)}
   planSignalsAfterBudget();phaseDesk();""")
e.rep(" S.rumors=[];S.evVerified=false;S.tcvEst=null;"," S.qColM=0;S.colBaseNav=0;S.rumors=[];S.evVerified=false;S.tcvEst=null;")
e.rep(" const collateral=colYield()-(cHit?cO.l:0);\n",""" const collTot=(colYield()-(cHit?cO.l:0))*(S.colBaseNav||S.nav);   /* montant du trimestre */
 const collateral=(collTot-(S.qColM||0))/S.nav;   /* reste à verser (négatif si défaut) */
""")
e.rep("x:collateral-S.rate/4,hit:cHit,l:cO.l,m:(collateral-S.rate/4)*S.nav,","x:collTot/(S.colBaseNav||S.nav)-S.rate/4,hit:cHit,l:cO.l,m:collTot-S.rate/4*(S.colBaseNav||S.nav),")
e.rep(" const grQ=((gross+collateral)*nb+(S.qEvM||0)+(S.qIncM||0)-mgmtM)/q0;"," const grQ=((gross+collateral)*nb+(S.qColM||0)+(S.qEvM||0)+(S.qIncM||0)-mgmtM)/q0;")
e.rep("collM=collateral*navBefore,","collM=collateral*navBefore+(S.qColM||0),")
e.rep(""" g+=colYield();   /* le collatéral court aussi : sans lui le ruban ratait la clôture de ~108 pb */
 return (t*g*S.nav+(S.qEvM||0)""",""" if(!S.qColM)g+=colYield();   /* lot 60 : versé d'avance, sinon couru */
 return (t*g*S.nav+(S.qColM||0)+(S.qEvM||0)""")
e.rep(" const t=qElapsed(),w=weights(S.k);let g=0;for(let i=0;i<N;i++)g+=w[i]*S.rBase[i];g+=colYield();return S.nav*(1+t*g)}",
      " const t=qElapsed(),w=weights(S.k);let g=0;for(let i=0;i<N;i++)g+=w[i]*S.rBase[i];if(!S.qColM)g+=colYield();return S.nav*(1+t*g)}")
e.done("lot 60 — lignes de marché, risque bruité, collatéral d'avance, cases à jour")
# ── équilibrage : facile plus indulgent pour un mauvais gérant, difficile plus généreux pour un bon ──
e=Ed()
e.rep("rivSkill:0.020,rivVol:0.95,lpNeg:0.75,rcNeg:0.75,lp0:8,flowMult:0.75,","rivSkill:0.020,rivVol:0.95,lpNeg:0.60,rcNeg:0.75,lp0:8,flowMult:0.75,")
e.rep("flowMult:2.10,flowIn:2.10","flowMult:1.60,flowIn:2.60")
e.done("lot 60 — équilibrage")
# ── deuxième passe : le facile récompense moins le talent (souscriptions ×0,6), le fondamental
#    redescend d'un cran (+5 sources), le flux retrouve son seuil de liquidation de 16 %
#    (le risque affiché, bruit compris, le faisait sauter trop souvent) ──
e=Ed()
e.rep("lpNeg:0.60,rcNeg:0.75,lp0:8,flowMult:0.75,","lpNeg:0.60,rcNeg:0.75,lp0:8,flowMult:0.75,flowIn:0.60,")
e.rep("sigBonus:6,capture:0.60,","sigBonus:5,capture:0.60,")
e.rep("+6 sources par trimestre : on vous rappelle, on vous parle","+5 sources par trimestre : on vous rappelle, on vous parle")
e.rep("lpMult:1.60,ddMax:0.13,","lpMult:1.60,ddMax:0.16,")
e.rep("rachats pour repli dès 13 % de perte au lieu de 28 %","rachats pour repli dès 16 % de perte au lieu de 28 %")
e.done("lot 60 — équilibrage 2")
