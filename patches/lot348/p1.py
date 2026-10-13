p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# P1 : la fourchette et l'impact (la facture au tarif) sont payés par le fonds ; la société ne paie que le courtage, 0,5 pb du notionnel.
# Calibrage : au tarif standard, le fonds paie la facture + 1,4 × la facture de glissement, soit 2,4 × comme avant (IMPK 2,4 → 1,4).
rep("""const IMPK=2.4,IMPMAX=0.015;""","""const IMPK=1.4,IMPMAX=0.015,COMB=0.5e-4;   /* lot 348 : glissement 1,4 × la facture (la facture elle-même est payée par le fonds) ; courtage 0,5 pb */
function bnTraded(k0,k1){let b=0;for(let i=0;i<N;i++){const d=(k1[i]||0)-(k0[i]||0);if(d)b+=Math.abs(notionalBn(d,i))}return b}
function comAdd(bn){S.qBn=(S.qBn||0)+(bn||0)}
function liveCom(){return COMB*bnTraded(S.k0||S.k,S.k)}
function comNow(){return S.phase==='book'?liveCom():COMB*(S.qBn||0)}
function billFund(amt,why){if(!amt)return;S.pendingTC+=amt/S.nav;execSlip(-amt,why||'Fourchette et impact')}""")
rep(""" S.pendingTC=0;S.freeAdjUsed=false;""",""" S.pendingTC=0;S.qBn=0;S.freeAdjUsed=false;""")
rep(""" S.pendingTC=tot/S.nav;S.totalTC+=tot;S.phase='events';""",""" S.pendingTC=tot/S.nav;S.qBn=bnTraded(S.k0,S.k);S.totalTC+=tot;S.phase='events';""")
# exécution sans anecdote : le fonds paie la facture et le glissement
rep("""  if(!ev){const im=execImpactAmt(S.pendingTC*S.nav,1,S.leakQ);if(im)execSlip(im,'Impact')}""",
    """  if(!ev){const b0=S.pendingTC*S.nav;execSlip(-b0,'Fourchette et impact');const im=execImpactAmt(b0,1,S.leakQ);if(im)execSlip(im,'Impact')}""")
# exécution avec anecdote
rep("""  {const bill=S.pendingTC*S.nav,im=execImpactAmt(bill,e._m||e.tcMult,e.leakQ);
   R.billI=bill;R.im=im;R.im0=execImpactAmt(bill,1,false);""","""  {const bill=S.pendingTC*S.nav,im=execImpactAmt(bill,e._m||e.tcMult,e.leakQ);
   execSlip(-bill,'Fourchette et impact');R.billP=bill;
   R.billI=bill;R.im=im;R.im0=execImpactAmt(bill,1,false);""")
rep("""S.k[i]+=d;S.pendingTC-=t.cost*0.8/S.nav;msg.push(`${INSTR[i].sym} ramené""","""S.k[i]+=d;billFund(-t.cost*0.8);msg.push(`${INSTR[i].sym} ramené""")
rep("""const t=tcost(nk-S.k[i],i);S.pendingTC-=t.cost*0.7/S.nav;S.k[i]=nk;""","""const t=tcost(nk-S.k[i],i);billFund(-t.cost*0.7);S.k[i]=nk;""")
rep("""S.k[o.i]+=d;S.pendingTC-=t.cost*0.8/S.nav;""","""S.k[o.i]+=d;billFund(-t.cost*0.8);""")
rep("""const t=tcost(nk-S.k[i],i);S.pendingTC+=t.cost/S.nav;S.k[i]=nk;msg.push(`${e.kAddAbsE[0]}""","""const t=tcost(nk-S.k[i],i);comAdd(t.bn);billFund(t.cost);S.k[i]=nk;msg.push(`${e.kAddAbsE[0]}""")
# bilan de l'exécution : la société ne paie que le courtage ; le fonds, la facture au tarif et le glissement
rep("""  const billF=S.pendingTC*S.nav,adj=billF-R.bill0-R.dt,mg=R.g+R.op,netM=-billF+mg;""","""  const billF=S.pendingTC*S.nav,adj=billF-R.bill0-R.dt,mg=R.g+R.op,com=COMB*(S.qBn||0),netM=-com+mg;""")
rep("""  const T1=[row('Exécution standard · facture des ordres',-(shA?R.bill0:billF-R.dt),'neg-g')];
  if(Math.abs(R.dt)>1e-9)T1.push(row(`Effet de votre choix · coûts ×${dec(R.m,2)}${R.on?' sur '+R.on.join(', '):''}${R.gm?' (pari perdu)':''}`,-R.dt));
  if(shA)T1.push(row(adj<0?'Positions réduites : ordres en moins':'Positions ajoutées : ordres en plus',-adj));""",
    """  const T1=[row(`Courtage · ${dec(COMB*1e4,1)} pb du notionnel`,-com,'neg-g')];""")
rep("""  const T2=[];
  if(im0)T2.push(row('Exécution standard · impact de marché',im0));""","""  const T2=[row('Exécution standard · fourchette et impact au tarif',-(shA?R.bill0:billF-R.dt),'neg-g')];
  if(Math.abs(R.dt)>1e-9)T2.push(row(`Effet de votre choix · tarif ×${dec(R.m,2)}${R.on?' sur '+R.on.join(', '):''}${R.gm?' (pari perdu)':''}`,-R.dt));
  if(shA)T2.push(row(adj<0?'Positions réduites : ordres en moins':'Positions ajoutées : ordres en plus',-adj));
  if(im0)T2.push(row('Exécution standard · glissement du prix moyen',im0));""")
# l'enjeu affiché de chaque option : le tarif touche désormais le fonds
rep("""const d=sub*(x.tcMult-1);bill=tot+d;soc-=d}""","""const d=sub*(x.tcMult-1);bill=tot+d;fund-=d}""")
# en-tête de l'exécution
rep("""<p class="note" style="margin:0 0 4px">Exécution standard — deux factures distinctes :</p><div class="kv"><span><b style="color:#fff">Ordres · payés par votre société</b></span><b style="color:#fff;font-size:17px">${cS(tot)}</b></div>
   <div class="kv"><span>Impact de marché · supporté par le fonds</span>${mn(execImpactAmt(tot,1,S.leakQ))}</div>""",
    """<p class="note" style="margin:0 0 4px">Exécution standard — qui paie quoi :</p><div class="kv"><span><b style="color:#fff">Fourchette et impact au tarif · payés par le fonds</b></span><b style="color:#fff;font-size:17px">${cS(tot)}</b></div>
   <div class="kv"><span>Glissement du prix moyen · supporté par le fonds</span>${mn(execImpactAmt(tot,1,S.leakQ))}</div>
   <div class="kv"><span>Courtage · payé par votre société (${dec(COMB*1e4,1)} pb du notionnel)</span>${cS(COMB*bnTraded(S.k0,S.k))}</div>""")
# ajustements en cours de trimestre : payés par le fonds, courtage à la société
rep(""" if(acted){S.k=[...o.t];if(o.free)S.freeAdjUsed=true}
 const cost=o.cost;
 S.pendingTC+=cost/S.nav;S.totalTC+=cost;""",""" if(acted){S.k=[...o.t];if(o.free)S.freeAdjUsed=true}
 const cost=o.cost;comAdd(bnTraded(k0,S.k));
 billFund(cost);S.totalTC+=cost;""")
rep("""cost=tt.cost*urgM(1.5,i)*S.tcMultQ;S.k[i]=target;S.pendingTC+=cost/S.nav;""","""cost=tt.cost*urgM(1.5,i)*S.tcMultQ;comAdd(tt.bn);S.k[i]=target;billFund(cost);""")
rep("""const t=tcost(nk-S.k[i],i);const c=t.cost*S.tcMultQ;S.pendingTC+=c/S.nav;S.totalTC+=c;cost+=c;S.k[i]=nk;""","""const t=tcost(nk-S.k[i],i);const c=t.cost*S.tcMultQ;comAdd(t.bn);billFund(c);S.totalTC+=c;cost+=c;S.k[i]=nk;""")
rep("""tcD=b*(e.tcMult-1);S.pendingTC+=tcD/S.nav;S.totalTC+=tcD;S.tcMultQ*=e.tcMult;""","""tcD=b*(e.tcMult-1);billFund(tcD);S.totalTC+=tcD;S.tcMultQ*=e.tcMult;""")
rep("""sur la facture d'ordres (${mm(b)}), payés par votre société de gestion ; les ajustements à venir""","""sur la facture d'ordres (${mm(b)}), payés par le fonds ; les ajustements à venir""")
rep("""[["Coûts d'exécution · société",`<span class="${cls(-tcD)}">${mn(-tcD)}</span>`]]""","""[["Coûts d'exécution · fonds",`<span class="${cls(-tcD)}">${mn(-tcD)}</span>`]]""")
rep("""  if(o.id==='cut'){const r0=liveRet();S.k=k1;const r1=liveRet();S.qEvM=(S.qEvM||0)+(r0-r1)*S.navQ0;S.pendingTC+=c/S.nav;S.totalTC+=c;S.stopCut=S.q}""",
    """  if(o.id==='cut'){const r0=liveRet();comAdd(bnTraded(S.k,k1));S.k=k1;const r1=liveRet();S.qEvM=(S.qEvM||0)+(r0-r1)*S.navQ0;billFund(c);S.totalTC+=c;S.stopCut=S.q}""")
rep("""  else{const r0=liveRet();S.k=o.k;const r1=liveRet();S.qEvM=(S.qEvM||0)+(r0-r1)*S.navQ0;S.pendingTC+=o.tc/S.nav;S.totalTC+=o.tc}""",
    """  else{const r0=liveRet();comAdd(bnTraded(S.k,o.k));S.k=o.k;const r1=liveRet();S.qEvM=(S.qEvM||0)+(r0-r1)*S.navQ0;billFund(o.tc);S.totalTC+=o.tc}""")
rep("""    for(let i=0;i<N;i++){const d=-S.k[i]*f;if(Math.abs(d)>1e-9){const t=tcost(d,i);liq+=t.cost*MGC.crisis}}
    S.pendingTC+=liq/S.nav;""","""    for(let i=0;i<N;i++){const d=-S.k[i]*f;if(Math.abs(d)>1e-9){const t=tcost(d,i);liq+=t.cost*MGC.crisis;comAdd(t.bn)}}
    billFund(liq,'Liquidation');""")
# textes « à votre charge » des ajustements
rep("""`Coût ${nb(mm(cost))} offert par le desk`:cost<0?`Rabais de ${nb(mm(-cost))} pour votre société de gestion : vous fournissez la liquidité que les autres cherchent`:`Coût ${nb(mm(cost))} à votre charge`}""",
    """`Coût ${nb(mm(cost))} offert par le desk`:cost<0?`Rabais de ${nb(mm(-cost))} pour le fonds : vous fournissez la liquidité que les autres cherchent`:`Coût ${nb(mm(cost))} pour le fonds`}""")
rep("""Coût ${mm(tcost(nk-S.k[i],i).cost*urgM(1.5,i)*S.tcMultQ)}, à votre charge, dans un marché""","""Coût ${mm(tcost(nk-S.k[i],i).cost*urgM(1.5,i)*S.tcMultQ)} pour le fonds, dans un marché""")
rep("""Coût ${mm(tcost(hF-S.k[i],i).cost*urgM(1.5,i)*S.tcMultQ)}, à votre charge.""","""Coût ${mm(tcost(hF-S.k[i],i).cost*urgM(1.5,i)*S.tcMultQ)} pour le fonds.""")
rep("""au tarif d'urgence : ${mm(P.c1)} à votre charge.`""","""au tarif d'urgence : ${mm(P.c1)} pour le fonds.`""")
rep("""au pire prix : ${mm(P.c2)} à votre charge.`""","""au pire prix : ${mm(P.c2)} pour le fonds.`""")
rep("""Ordres au tarif d'urgence : ${mm(c)} à votre charge. Pas de carton.""","""Ordres au tarif d'urgence : ${mm(c)} pour le fonds. Pas de carton.""")
# clôture : la société paie le courtage
rep(""" const tc=S.pendingTC;S.pendingTC=0;      /* à la charge du gérant, plus à celle du fonds */""",""" S.pendingTC=0;      /* lot 348 : la facture a été payée par le fonds au fil du trimestre ; le gérant paie le courtage */""")
rep(""" const navBefore=S.nav;""",""" const navBefore=S.nav,tc=(S.qBn||0)*COMB/Math.max(1e-12,navBefore);""")
# trésorerie vivante, coûts, détail du gain
rep("""function mgrNet(){return S.mgrFees-S.mgrCosts-(S.phase==='book'?liveTC():(S.pendingTC||0)*S.nav)""","""function mgrNet(){return S.mgrFees-S.mgrCosts-comNow()""")
rep(""" const tc=S.phase==='book'?liveTC()/S.nav:(S.pendingTC||0);""",""" const tc=comNow()/S.nav;""")
rep("""  const tcNow=S.phase==='book'?liveTC():(S.pendingTC||0)*S.nav,tcAll=S.led?(S.cTC||0)+tcNow:(S.totalTC||0)+(S.phase==='book'?liveTC():0);""",
    """  const tcNow=comNow(),tcAll=(S.cTC||0)+tcNow;""")
rep("""La facture de courtage du trimestre (${mm(-o.P.tcM)}) n'apparaît pas ici : elle est à votre charge, pas à celle du fonds. L'impact de marché de vos ordres, lui, est compté plus haut, avec les dépêches et le desk.""",
    """Le courtage du trimestre (${mm(-o.P.tcM)}) n'apparaît pas ici : il est à votre charge, pas à celle du fonds. La fourchette, l'impact et le glissement de vos ordres, eux, sont payés par le fonds et comptés plus haut, avec les dépêches et le desk.""")
# trésorerie de départ −20 %
rep("""S.mgrSeed=(SIZE().seed||0)+(STYSEED[S.prof]||0);""","""S.mgrSeed=0.8*((SIZE().seed||0)+(STYSEED[S.prof]||0));   /* lot 348 : −20 %, la société ne paie plus que le courtage */""")
open(p,'w',encoding='utf-8').write(s)
s=open(p,encoding='utf-8').read()
rep(""" const c=liveTC(),rest=mgrCash(),avail=Math.max(0,rest+c),ko=false,rb=redBlock();
 if(p)p.innerHTML=`<span>Ordres ${mm(c)} · trésorerie après paiement</span>""",""" const c=liveCom(),rest=mgrCash(),avail=Math.max(0,rest+c),ko=false,rb=redBlock();
 if(p)p.innerHTML=`<span>Courtage ${mm(c)} · trésorerie après paiement</span>""")
rep("""  const c=liveTC(),avail=Math.max(0,mgrCash()+c);
  if(c<=avail)break;""","""  const c=liveCom(),avail=Math.max(0,mgrCash()+c);
  if(c<=avail)break;""")
rep("""<span>Coût total des ordres</span><b class="${cC(tot)}">${cS(tot)} · ${tot>0?'−':'+'}${Math.abs(tot/S.nav*1e4).toFixed(0)} pb de l'encours</b></div>""",
    """<span>Fourchette et impact · payés par le fonds</span><b class="${cC(tot)}">${cS(tot)} · ${tot>0?'−':'+'}${Math.abs(tot/S.nav*1e4).toFixed(0)} pb de l'encours</b></div><div class="kv"><span>Courtage · payé par votre société</span><b>${mm(liveCom())}</b></div>""")
open(p,'w',encoding='utf-8').write(s)
s=open(p,encoding='utf-8').read()
rep("""['exécution',-(Gq.tc||0)]""","""['courtage',-(Gq.tc||0)]""")
rep("""["Coûts d'exécution",-(Gq.tc||0)]""","""["Courtage de vos ordres",-(Gq.tc||0)]""")
open(p,'w',encoding='utf-8').write(s)
s=open(p,encoding='utf-8').read()
rep("""const BUDK=0.90;   /* lot 123 : toutes les équipes 20 % moins chères */""","""const BUDK=1.60;   /* lot 123 : toutes les équipes 20 % moins chères ; lot 348 : ×1,78 — la société ne paie plus la facture des ordres (campagne : survie 81 %, 79 % avant) */""")
open(p,'w',encoding='utf-8').write(s)
