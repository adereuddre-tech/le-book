# -*- coding: utf-8 -*-
"""Lot 61 — collatéral entièrement à la clôture, « profit » dynamique (impact et drain de
volatilité compris), lignes de marché réordonnées, facteurs sans surlignage, tuile Trésorerie.

Profit d'un book (fraction de l'encours, sur le trimestre) :
  rendement du collatéral espéré (taux / 4 + surcroît − probabilité × perte)
  + Σ w_i · attendu_i
  − impact de marché des ordres en cours (partie impact de tcost, rapportée à l'encours)
  − ½ σ²_trim, avec σ le risque affiché (bruit d'estimation compris) : le drain de volatilité.
Profit d'un marché = profit(book + 1 unité) − profit(book), comme le risque +1.

Cases hors caisse : le contrôle était juste (0 case fautive en trésorerie tendue, chk58 --tight),
mais la tuile dorée montrait « Vos gains », négatifs au premier trimestre alors que la société
dispose de son capital de départ. La tuile montre désormais la trésorerie, ce qui borne les
dépenses ; les gains (le score) restent dans sa pop-up.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
# ── collatéral : plus rien d'avance ──
e.rep("""   if(S.colPaidQ!==S.q){const o=colOpt(),ex=colYield()-(redOn('collat')?0:o.p*o.l);   /* lot 60 */
    S.colPaidQ=S.q;S.colBaseNav=S.nav;S.qColM=ex*S.nav;S.nav+=S.qColM;
    toast(`Collatéral : espérance du trimestre versée, <b>${mm(S.qColM)}</b>${o.p&&!redOn('collat')?` · l'écart éventuel à la clôture`:''}`)}
""","""   /* lot 61 : le rendement du collatéral est acquis au fonds et versé en entier à la clôture */
""")
# ── profit ──
e.rep("function expBook(k){","""function colExp(){const o=colOpt();return redOn('collat')?S.rate/4*0.6:S.rate/4+colY(o)-o.p*o.l}
function profitBook(k){
 k=k||S.k;const w=weights(k),k0=S.k0||S.k;let m=colExp();
 for(let i=0;i<N;i++){if(w[i])m+=w[i]*expRet(i).m;const d=k[i]-k0[i];if(d)m-=tcost(d,i).imp/S.nav}
 const sg=riskShown(w).total;return m-0.5*sg*sg/4;
}
const pc2=x=>`<b class="${Math.abs(x)<5e-5?'dim-g':cls(x)}">${x>=0?'+':'−'}${dec(Math.abs(x*100),2)} %</b>`;
function expBook(k){""")
e.rep("""<b>${ex?`<span class="fxa">attendu</span> ${expShort(expBook(S.k))}`:rv}</b>""","""<b><span class="fxa">profit</span> ${pc2(profitBook(S.k))}</b>""")
# ── ligne de marché : ordre | risque −1 | profit | risque +1 | coût | impact ──
e.rep("""  let ex1='<b class="dim-g">—</b>';
  if(S.tcvEst){const o=expRet(i),w1=U/x.sig,g={m:w1*o.m,s:w1*o.s};ex1=`<b class="${cls(g.m)}">${g.m>=0?'+':'−'}${dec(Math.abs(g.m*100),1)} %</b><i>±${dec(2*g.s*100,1)}</i>`}""",
"""  const ex1=pc2(profitBook(kp)-profitBook(S.k));""")
e.rep("""  gl=`<div class="rgrid"><span>Ordre</span><span>Attendu /u</span><span>Risque +1</span><span>Risque −1</span><span>Coût</span><span>Impact</span>
   <div>${od}</div><div>${ex1}</div><div>${rc(rP)}</div><div>${rc(rM)}</div><div><b>${mm(t.spr||0)}</b></div><div><b>${mm(t.imp||0)}</b></div></div>`}""",
"""  gl=`<div class="rgrid"><span>Ordre</span><span>Risque −1</span><span>Profit +1</span><span>Risque +1</span><span>Coût</span><span>Impact</span>
   <div>${od}</div><div>${rc(rM)}</div><div>${ex1}</div><div>${rc(rP)}</div><div><b>${mm(t.spr||0)}</b></div><div><b>${mm(t.imp||0)}</b></div></div>`}""")
e.rep(".rgrid{display:grid;grid-template-columns:1.05fr 1.25fr 1fr 1fr .95fr .95fr;",".rgrid{display:grid;grid-template-columns:1.05fr 1fr 1.15fr 1fr .95fr .95fr;")
# ── facteurs : ni cadre ni soulignement ──
e.rep(".fg.hot{border-color:var(--gold)}",".fg.hot{border-color:var(--line)}")
e.rep("hot=S.hotFactor===k?';text-decoration:underline':'';","hot='';")
# ── tuile Trésorerie ──
e.rep("""<span>Vos gains</span><b id="gaintile" class="${mgrNet()>=0?'':'neg-g'}">${score(mgrNet())}</b>""","""<span>Trésorerie</span><b id="gaintile" class="${mgrCash()>=0?'':'neg-g'}">${score(mgrCash())}</b>""")
e.rep(" const v=mgrNet();e.textContent=score(v);e.className=v>=0?'':'neg-g'}"," const v=mgrCash();e.textContent=score(v);e.className=v>=0?'':'neg-g'}")
# ── budget : la trésorerie sert aussi aux ordres ──
e.rep("""   <div class="kv"><span>Trésorerie disponible ce trimestre</span><b id="btre">${mm(mgrCash()+(S.qOps||0))}</b></div>""",
"""   <div class="kv"><span>Trésorerie disponible ce trimestre</span><b id="btre">${mm(mgrCash()+(S.qOps||0))}</b></div>
   <div class="kv"><span>Reste pour les ordres du trimestre</span><b id="brest"></b></div>
   <p class="note" style="margin:4px 0 8px">⚠ La même trésorerie paie vos ordres de marché : ce que le budget consomme, le book ne peut plus le dépenser. En début de partie, quand la caisse se limite au capital de départ et à la première commission, gardez des budgets serrés ; vous les relèverez quand les commissions de performance rentreront.</p>""")
e.rep("function budgetBpIf(id,lv){","""function budRest(){const e=document.getElementById('brest');if(!e)return;const r=mgrCash()+(S.qOps||0)-budgetBp()*1e-4*S.nav;e.textContent=mm(r);e.className=r>=0?'gold-g':'neg-g'}
function budgetBpIf(id,lv){""")
e.rep(" const ok=(id,i)=>(i===0||budgetBpIf(id,i)*1e-4*S.nav<=purse)"," setTimeout(budRest,0);\n const ok=(id,i)=>(i===0||budgetBpIf(id,i)*1e-4*S.nav<=purse)")
e.done("lot 61 — profit dynamique, collatéral à la clôture, tuile Trésorerie")
