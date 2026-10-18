p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# P1 : une vraie assurance contre les extrêmes — put au-delà de −10 % (et non −3 %), prime 1,3 × ce qu'elle rend en moyenne (et non 2 ×)
rep("const HEDGE={h:0.70,load:2,min:0.005};","const HEDGE={h:0.70,load:1.3,min:0.005};   /* lot 381 : 2 → 1,3 */")
rep("const PUTK=0.03;   /* lot 322 : le put sur le book paie au-delà de −3 % sur le trimestre */","const PUTK=0.10;   /* lot 381 : au-delà de −10 % (lot 322 : −3 %) */")
# P3 : la protection compte dans le risque du fonds — extrêmes amortis de h × le choc immédiat quand elle est détenue (ou simulée)
rep("""function xLossE(k,sc){const w=weights(k),h=stressHit(sc,k);let v=0;INSTR.forEach((x,i)=>{if(h[x.sym])v+=w[i]*h[x.sym]*x.sigQ});
 const bo=0.5+0.5*((S.bud&&TAILM[S.bud.risk])||1),cr=v<0?crowd(riskShown(w).total)*(S.bud?motS():1):1;return bo*(0.5*v*cr-stressGap(k,sc))+XCONT*v}""",
"""function xLossE(k,sc){const w=weights(k),h=stressHit(sc,k);let v=0;INSTR.forEach((x,i)=>{if(h[x.sym])v+=w[i]*h[x.sym]*x.sigQ});
 const bo=0.5+0.5*((S.bud&&TAILM[S.bud.risk])||1),cr=v<0?crowd(riskShown(w).total)*(S.bud?motS():1):1,im=bo*(0.5*v*cr-stressGap(k,sc));return im+XCONT*v+(hedgeHeld()?hH()*Math.max(0,-im):0)}
/* lot 381 : protection détenue ce trimestre (ou simulée pour la page de la protection) */
let HSIM=null;function hedgeHeld(){return HSIM!=null?HSIM:!!(S&&(S.hedgeQ===S.q))}""")
rep("""function xLossT(k,t){const v=xEvLoss(k,t);return 0.5*v+XCONT*v}""","""function xLossT(k,t){const v=xEvLoss(k,t);return 0.5*v+XCONT*v+(hedgeHeld()?hH()*Math.max(0,-0.5*v):0)}""")
# valeur risque compris
rep("""function hedgeBlock(){const e=xImmEst(),pX=xProbTot(),ev=hedgeEV(),cr=hedgeCost(),c=cr*S.nav,on=S.hedgeQ===S.q||S.hedgePick===S.q,HP=hedgeParts(),h=hH();
 const W=xWatch(),Pd=xDeskP(),evD=hedgeDeskEV(),gap=evD-cr,pc0=v=>`${dec(v*100,1)} %`;""",
"""/* lot 381 : ce que la protection retire au risque du fonds, et ce que vaut ce risque en moins (½ σ² trimestriel, comme dans la rentabilité estimée) */
function hedgeRisk(){const sv=HSIM;HSIM=false;const r0=fundParts(S.k).total/2;HSIM=true;const r1=fundParts(S.k).total/2;HSIM=sv;return {r0,r1,g:Math.max(0,0.5*(r0*r0-r1*r1))}}
function hedgeBlock(){const e=xImmEst(),pX=xProbTot(),ev=hedgeEV(),cr=hedgeCost(),c=cr*S.nav,on=S.hedgeQ===S.q||S.hedgePick===S.q,HP=hedgeParts(),h=hH();
 const W=xWatch(),Pd=xDeskP(),evD=hedgeDeskEV(),HR=hedgeRisk(),gap=evD+HR.g-cr,pc0=v=>`${dec(v*100,1)} %`;""")
rep("""  <div class="attr"><span class="an"><b>Pour votre desk, la protection est ${gap>=0?'bon marché':'chère'}</b></span>""",
    """  <div class="attr"><span class="an">Risque du fonds ce trimestre · sans → avec la protection</span><span class="av"><b>${dec(HR.r0*100,1)} % → ${dec(HR.r1*100,1)} %</b></span></div>
  <div class="attr"><span class="an">Valeur de ce risque en moins · coût du risque évité (½ σ²)</span><span class="av"><b class="gold-g">+${mm(HR.g*S.nav)} · ${dec(HR.g*100,2)} %</b></span></div>
  <div class="attr"><span class="an"><b>Pour votre desk, risque compris, la protection est ${gap>=0?'bon marché':'chère'}</b></span>""")
rep("""  ${hedgeGauge(ev,evD,cr)}""","""  ${hedgeGauge(ev,evD+HR.g,cr)}""")
rep("""<b style="color:var(--gold)">▍</b> desk ${mm(evD*S.nav)} ·""","""<b style="color:var(--gold)">▍</b> desk, risque compris ${mm(evD*S.nav)} ·""")
# textes
rep("""Le marché vend cette protection au double de ce qu'elle rend en moyenne : se couvrir chaque trimestre coûte cher ; elle ne paie que si votre veille vous en dit plus que le marché.""",
    """Le marché vend cette protection 1,3 fois ce qu'elle rend en moyenne : c'est le prix d'une assurance. Elle se justifie quand votre veille vous en dit plus que le marché, ou quand le risque qu'elle retire au fonds vaut plus que ce surcoût.""")
open(p,"w",encoding="utf-8").write(s)
