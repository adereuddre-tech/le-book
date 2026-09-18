# -*- coding: utf-8 -*-
"""Lot 2 — économie du gérant.

1. La société de gestion a une trésorerie. Elle démarre avec 2 % de l'encours initial
   (« capital de départ »), encaisse les commissions et paie ce qu'elle décide de dépenser.
2. La commission de gestion est versée à l'OUVERTURE de chaque trimestre ; la commission
   de performance et le bonus d'objectif à la CLÔTURE.
3. Les coûts d'exécution sont à la charge du gérant et non plus du fonds.
4. On ne peut engager que ce qu'on a en caisse : niveaux de budget verrouillés, ordres bloqués.
5. Le bonus d'objectif est ramené au quart : il pesait autant que la commission de
   performance, il redevient un accessoire.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()

# ══ 1. trésorerie ══
e.rep("""function budgetBp(){return BUDGET.reduce((a,b)=>a+b.lv[S.bud[b.id]].bp,0)+DESK().fixed*1e4}""",
"""function budgetBp(){return BUDGET.reduce((a,b)=>a+b.lv[S.bud[b.id]].bp,0)+DESK().fixed*1e4}
/* budget si l'on basculait un seul poste sur un autre niveau */
function budgetBpIf(id,lv){return BUDGET.reduce((a,b)=>a+b.lv[b.id===id?lv:S.bud[b.id]].bp,0)+DESK().fixed*1e4}
/* Le score : commissions encaissées moins tout ce que le gérant a payé, coûts d'exécution
   du trimestre en cours compris — ils bougent pendant qu'on construit le book. */
function mgrNet(){return S.mgrFees-S.mgrCosts-(S.phase==='book'?liveTC():(S.pendingTC||0)*S.nav)}
/* Ce qu'il peut encore engager : son score plus le capital de départ de la société. */
function mgrCash(){return (S.mgrCap0||0)+mgrNet()}""")
e.rep("""   idx:1,hwmIdx:1,peakIdx:1,fl:{},rumBought:0,outBand:0,""",
      """   idx:1,hwmIdx:1,peakIdx:1,fl:{},rumBought:0,outBand:0,mgrCap0:0.02*Z.nav,qMgmtM:0,""")
e.rep("""   k:new Array(N).fill(0),rets:[],navs:[100],regimes:[],""",
      """   k:new Array(N).fill(0),rets:[],navs:[Z.nav],regimes:[],""")

# ══ 2. commission de gestion versée à l'ouverture ══
e.rep(""" S.pendingTC=0;S.freeAdjUsed=false;
}""",
""" S.pendingTC=0;S.freeAdjUsed=false;
 /* la commission de gestion est prélevée sur le fonds et vous est versée dès l'ouverture ;
    la performance et le bonus d'objectif attendent la clôture */
 S.qMgmtM=VOL().mgmt*S.nav;S.nav-=S.qMgmtM;S.mgrFees+=S.qMgmtM;refreshGain();
}""")

# ══ 3. clôture : plus de transaction dans le fonds, plus de gestion à la clôture ══
e.rep(""" const collateral=S.rate/4;
 const ops=S.budBp*1e-4;
 const tc=S.pendingTC;
 const navBefore=S.nav;
 const nb=S.nav,q0=Math.max(1e-9,S.navQ0);
 const grQ=((gross+collateral-tc)*nb+(S.qEvM||0)+(S.qIncM||0))/q0;
 const mgmtQ0=VOL().mgmt;
 const idxPre=S.idx*(1+grQ-mgmtQ0);
 const perfQ0=idxPre>S.hwmIdx?VOL().perf*(idxPre-S.hwmIdx)/Math.max(1e-9,S.idx):0;
 let mgmt=mgmtQ0*q0/nb;const perf=perfQ0*q0/nb;
 const net=gross+collateral-tc-mgmt-perf;
 S.nav*=(1+net);
 const grossM=gross*navBefore,collM=collateral*navBefore,tcM=-tc*navBefore,feeM=-(mgmt+perf)*navBefore;
 const evM=S.qEvM||0,incM=S.qIncM||0;
 const perfM=grossM+collM+tcM+feeM+evM+incM;""",
""" const collateral=S.rate/4;
 const ops=S.budBp*1e-4;
 const tc=S.pendingTC;S.pendingTC=0;      /* à la charge du gérant, plus à celle du fonds */
 const navBefore=S.nav;
 const nb=S.nav,q0=Math.max(1e-9,S.navQ0);
 const mgmtM=S.qMgmtM||0;                 /* déjà prélevée à l'ouverture du trimestre */
 const grQ=((gross+collateral)*nb+(S.qEvM||0)+(S.qIncM||0)-mgmtM)/q0;
 const idxPre=S.idx*(1+grQ);
 const perfQ0=idxPre>S.hwmIdx?VOL().perf*(idxPre-S.hwmIdx)/Math.max(1e-9,S.idx):0;
 const perf=perfQ0*q0/nb;
 const net=gross+collateral-perf;
 S.nav*=(1+net);
 const grossM=gross*navBefore,collM=collateral*navBefore,tcM=-tc*navBefore,feeM=-(mgmtM+perf*navBefore);
 const evM=S.qEvM||0,incM=S.qIncM||0;
 const perfM=grossM+collM+feeM+evM+incM;  /* tcM n'y est pas : c'est vous qui payez */""")
e.rep(""" S.mgrFees=(S.mgrFees||0)+(mgmt+perf)*navBefore;refreshGain();
 S.mgrQ={fees:(mgmt+perf)*navBefore,ops:S.qOps||0,rum:0,mgmt:mgmt*navBefore,perf:perf*navBefore};""",
""" S.mgrFees=(S.mgrFees||0)+perf*navBefore;S.mgrCosts+=tc*navBefore;refreshGain();
 S.mgrQ={fees:mgmtM+perf*navBefore,ops:S.qOps||0,rum:0,mgmt:mgmtM,perf:perf*navBefore,tc:tc*navBefore};""")
e.rep(""" screenDebrief({r,gross,net,attr,w:wFin,collateral,ops,tc,mgmt,perf,dd,sp,nav0:navBefore,qTotal,q0:S.navQ0,P:S.qPnl});""",
      """ screenDebrief({r,gross,net,attr,w:wFin,collateral,ops,tc,mgmt:mgmtM/Math.max(1e-9,navBefore),perf,dd,sp,nav0:navBefore,qTotal,q0:S.navQ0,P:S.qPnl});""")

# ══ 4. bonus d'objectif ramené au quart ══
e.rep("""const QGOALS=[""",
"""/* Mesuré avant réglage : sur dix parties, les bonus d'objectif pesaient autant que la
   commission de performance et davantage que la commission de gestion — le bonus ÉTAIT le
   score. Ramené au quart, il redevient un accessoire de la performance. */
const GOALB=0.25;
function goalBon(g){return g?g.b*GOALB*S.aum0:0}
const QGOALS=[""")
e.rep("""  const bon=ok?S.goal.b*S.aum0:0;""","""  const bon=ok?goalBon(S.goal):0;""")
e.rep("""Bonus de ${moneyB(S.goal.b*S.aum0)} sur votre score.""","""Bonus de ${moneyB(goalBon(S.goal))} sur votre score.""")

# ══ 5. le score affiché tient compte des coûts en cours ══
e.rep("""<b id="gaintile" class="${(S.mgrFees-S.mgrCosts)>=0?'':'neg-g'}">${score(S.mgrFees-S.mgrCosts)}</b>""",
      """<b id="gaintile" class="${mgrNet()>=0?'':'neg-g'}">${score(mgrNet())}</b>""")
e.rep("""function refreshGain(){const e=document.getElementById('gaintile');if(!e||!S)return;
 const v=S.mgrFees-S.mgrCosts;e.textContent=score(v);e.className=v>=0?'':'neg-g'}""",
"""function refreshGain(){const e=document.getElementById('gaintile');if(!e||!S)return;
 const v=mgrNet();e.textContent=score(v);e.className=v>=0?'':'neg-g'}""")
e.rep("""<span class="av"><b class="gold-g">${score(S.mgrFees-S.mgrCosts)}</b></span></div>""",
      """<span class="av"><b class="gold-g">${score(mgrNet())}</b></span></div>""")

e.done("lot 2 — économie du gérant (comptabilité)")
