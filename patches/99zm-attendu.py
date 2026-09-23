# -*- coding: utf-8 -*-
"""Lot 51 — rendement attendu ± 2σ, par marché et pour le book, dosé par la difficulté.

Le rendement d'un marché, dans le moteur (`drawReturns`), vaut
    σ_trimestre × [ Σ_k b_k·f_k + 0,12·tendance + 0,10·portage + 0,08·valeur + propre ] + dérive.
Le joueur en voit chaque morceau séparément (expositions C/I/D/A, lectures des sources, trois
signaux bruités) et devait faire la synthèse de tête. `expRet(i)` la fait avec SES informations
seulement — jamais la vérité :
  - attendu = σ · ( Σ b_k·f̂_k + 0,12·T̂ + 0,10·Ĉ + 0,08·V̂ ) + dérive, où f̂ est la lecture des
    sources (`S.factEst`) et T̂, Ĉ, V̂ les lectures bruitées du desk ;
  - incertitude = σ · √( Σ b_k²·VF + propre² + bruit des lectures ), VF calibré pour que
    l'intervalle ± 2σ contienne le mouvement réel environ 95 fois sur 100 (`tools/expchk.js`).
Pour le book : attendu = Σ w_i·attendu_i ; incertitude par la même structure factorielle.

Dosage par la difficulté :
  - facile : chiffre attendu, intervalle ± 2σ en clair, barre ;
  - moyen : barre avec intervalle et chiffre attendu ;
  - difficile : sens et conviction seulement (▲▲ ★★☆), le rapport attendu / σ.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
e.rep("function drawRows(){","""/* ── rendement attendu : ce que VOS informations disent du trimestre ────────────── */
const EXPVF=1.15;   /* variance résiduelle d'un facteur une fois les sources lues (calibrée) */
const SIGW={t:0.12,c:0.10,v:0.08};
function sigNoise(key){const e=TCVQ[S.bud.exec]*(S.tcvPerm?0.33:1);return e*((typeof STYLESIG!=='undefined'&&STYLESIG[S.prof]===key)?0.3:(typeof STYLESIG!=='undefined'?1.3:1))}
function expRet(i){
 const x=INSTR[i],f=S.factEst||[0,0,0,0],e=S.tcvEst;
 let z=0;for(let k=0;k<K;k++)z+=x.b[k]*f[k];
 let v=0;for(let k=0;k<K;k++)v+=x.b[k]*x.b[k]*EXPVF;
 if(e){z+=(SIGW.t*e.t[i]+SIGW.c*e.c[i]+SIGW.v*e.v[i])*(UNIV().edge||1);
  v+=SIGW.t**2*(sigNoise('t')**2+0.1)+SIGW.c**2*(sigNoise('c')**2+0.1)+SIGW.v**2*(sigNoise('v')**2+0.1)}
 v+=(x.idio||0)**2;
 return {m:x.sigQ*z+(x.drift||0),s:x.sigQ*Math.sqrt(v)};
}
function expBook(k){
 const w=weights(k);let m=S.rate/4,vf=0,vi=0;const fl=[0,0,0,0];
 for(let i=0;i<N;i++){if(!w[i])continue;const x=INSTR[i],o=expRet(i);m+=w[i]*o.m;
  for(let kk=0;kk<K;kk++)fl[kk]+=w[i]*x.sigQ*x.b[kk];
  vi+=(w[i]*o.s)**2-(w[i]*x.sigQ)**2*x.b.reduce((a,b)=>a+b*b*EXPVF,0)}
 for(let kk=0;kk<K;kk++)vf+=fl[kk]*fl[kk]*EXPVF;
 return {m,s:Math.sqrt(Math.max(0,vf+vi))};
}
/* Affichage dosé : facile = chiffres et intervalle, moyen = barre et attendu, difficile = sens et conviction. */
function expView(o,book){
 const lv=S.size||'mid',r=o.s>0?o.m/o.s:0;
 const lo=o.m-2*o.s,hi=o.m+2*o.s,sc=Math.max(0.02,Math.abs(lo),Math.abs(hi));
 const pos=v=>(50+50*v/sc).toFixed(1);
 const bar=`<span class="xbar"><em></em><i style="left:${pos(lo)}%;width:${(pos(hi)-pos(lo)).toFixed(1)}%"></i><b class="${o.m>=0?'up':'dn'}" style="left:${pos(o.m)}%"></b></span>`;
 if(lv==='mega'){const n=Math.min(3,Math.floor(Math.abs(r)/0.35));
  return `<span class="xv"><span class="xk">${book?'Book':'Attendu'}</span><b class="${o.m>=0?'pos-g':'neg-g'}">${n?(o.m>=0?'▲':'▼').repeat(n):'·'}</b><span class="xs">${'★'.repeat(Math.min(3,Math.round(Math.abs(r)/0.35)))}${'☆'.repeat(3-Math.min(3,Math.round(Math.abs(r)/0.35)))}</span></span>`}
 if(lv==='mid')return `<span class="xv"><span class="xk">${book?'Book':'Attendu'}</span><b class="${cls(o.m)}">${sgn(o.m,1)}</b>${bar}</span>`;
 return `<span class="xv"><span class="xk">${book?'Book':'Attendu'}</span><b class="${cls(o.m)}">${sgn(o.m,1)}</b>${bar}<span class="xs">${sgn(lo,1)} à ${sgn(hi,1)}</span></span>`;
}
function drawRows(){""")
e.rep("""     <div class="rowinfo" id="ri${i}"></div>""","""     <div class="rowinfo" id="ri${i}"></div>
     ${mktOpen(i)&&S.tcvEst?`<div class="xrow">${expView(expRet(i))}</div>`:''}""")
e.rep(".lvls{display:grid;",""".xrow{margin:6px 0 2px}
.xv{display:flex;align-items:center;gap:8px;font-family:var(--mono);font-size:11.5px;color:var(--dim)}
.xv .xk{color:var(--dimmer);min-width:52px}.xv b{min-width:48px}
.xv .xs{color:var(--dimmer);white-space:nowrap}
.xbar{position:relative;flex:1;height:10px;min-width:70px}
.xbar em{position:absolute;left:50%;top:0;bottom:0;width:1px;background:#5B6E8C}
.xbar i{position:absolute;top:3px;height:4px;border-radius:2px;background:rgba(159,178,204,.35)}
.xbar b{position:absolute;top:0;width:3px;height:10px;margin-left:-1px;border-radius:1px;min-width:0}
.xbar b.up{background:var(--long)}.xbar b.dn{background:var(--short)}
.xbook{margin:4px 0 10px;padding:8px 10px;border:1px solid var(--line);border-radius:8px}
.lvls{display:grid;""")
# niveau du book : au-dessus du panneau de risque
e.rep("function renderRisk(){\n const w=weights(S.k),sp=pvol(w),vd=varDecomp(w),rc=riskContrib(w);",
      "function renderRisk(){\n const w=weights(S.k),sp=pvol(w),vd=varDecomp(w),rc=riskContrib(w);\n {const xb=document.getElementById('xbook');if(xb&&S.tcvEst){const o=expBook(S.k);xb.innerHTML=expView(o,true)+`<div class=\"note\" style=\"margin-top:4px\">Ce que vos sources et vos signaux disent du trimestre, pour ce book — intervalle à 95 %. Les dépêches le déplaceront.</div>`}}")
e.rep("""<div class="block"><div class="blockhead"><h2>Le book</h2><span class="hint">unités de risque, de −${S.maxk} à +${S.maxk}</span></div>""",
      """<div class="block"><div class="blockhead"><h2>Le book</h2><span class="hint">unités de risque, de −${S.maxk} à +${S.maxk}</span></div>
   <div class="xbook" id="xbook"></div>""")
e.done("lot 51 — rendement attendu par marche et pour le book")
