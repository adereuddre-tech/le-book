# Lot 91 : pop-up « Trésorerie » — décomposition cumulée fine et co-investissement expliqué.
# Constat : la pop-up ne montrait que commissions / coûts en deux lignes et ne disait rien
# de la part co-investie bloquée, alors que mgrCash = mgrNet − coinvLocked().
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:80]); s=s.replace(o,n)
# cumuls
rep('totalTC:0,totalOps:0,','totalTC:0,totalOps:0,led:1,cMgmt:0,cPerf:0,cBon:0,cOps:0,')
rep('S.qMgmtM=VOL().mgmt*S.nav;S.nav-=S.qMgmtM;S.mgrFees+=S.qMgmtM;','S.qMgmtM=VOL().mgmt*S.nav;S.nav-=S.qMgmtM;S.mgrFees+=S.qMgmtM;S.cMgmt=(S.cMgmt||0)+S.qMgmtM;')
rep('S.mgrFees=(S.mgrFees||0)+perf*navBefore;','S.mgrFees=(S.mgrFees||0)+perf*navBefore;S.cPerf=(S.cPerf||0)+perf*navBefore;')
rep('if(ok)S.mgrFees+=bon;','if(ok){S.mgrFees+=bon;S.cBon=(S.cBon||0)+bon}')
rep('S.mgrCosts-=S.qOps||0;','S.mgrCosts-=S.qOps||0;S.cOps=(S.cOps||0)-(S.qOps||0);',2)
rep('S.qOps=budgetBp()*1e-4*S.nav;S.mgrCosts+=S.qOps;','S.qOps=budgetBp()*1e-4*S.nav;S.mgrCosts+=S.qOps;S.cOps=(S.cOps||0)+S.qOps;',2)
# débriefing : part placée
rep("['Co-investissement',Gq.coinv||0]","[Gq.cb?`Co-investissement (${Math.round((Gq.cp||0)*100)} % · ${mm(Gq.cb)} placés)`:'Co-investissement',Gq.coinv||0]")
# pop-up
i=s.find("} else if(id==='gain'){");j=s.find("} else if(id==='cost'){");assert i>0 and j>i
NEW=r"""} else if(id==='gain'){
  const sg=v=>`<b class="${v>=0?'pos-g':'neg-g'}">${v>=0?'+':'−'}${mm(Math.abs(v))}</b>`;
  const live=S.phase==='events'&&S.live,cLive=live&&S.coinvBase?S.coinvBase*liveNet():0,lock=coinvLocked(),net=mgrNet();
  const tcNow=S.phase==='book'?liveTC():0;
  const it=[[`Commissions de gestion`,S.cMgmt||0],[`Commissions de performance`,S.cPerf||0],[`Bonus d'objectif`,S.cBon||0],
   [`Résultat du co-investissement${cLive?' (dont en cours '+(cLive>=0?'+':'−')+mm(Math.abs(cLive))+')':''}`,(S.mgrCoinv||0)+cLive],
   [`Restitution de commissions`,-(S.mgrClaw||0)],[`Budget d'exploitation`,-(S.cOps||0)],[`Courtage de vos ordres${tcNow?' (dont en préparation)':''}`,-((S.totalTC||0)+tcNow)]];
  const oth=net-it.reduce((a,x)=>a+x[1],0);
  if(Math.abs(oth)>1e-7)it.push([S.led?`Autres : accidents de levier, incidents payés par vous`:`Non ventilé (partie commencée avant la mise à jour)`,oth]);
  const pc=Math.round(coinvPct()*100);
  const ex=lock?S.coinvBase:coinvPct()*Math.max(0,mgrCash());
  openModal('Trésorerie de votre société',`<p>Votre société de gestion n'a pas de capital : sa trésorerie, ce sont vos gains nets — votre score — moins la part que vous avez placée dans le fonds, qui est bloquée jusqu'à la clôture.</p>
   <p style="margin:12px 0 4px">D'où viennent vos gains nets, depuis le premier jour</p>
   ${tbl([...it.filter(x=>Math.abs(x[1])>1e-9).map(x=>[x[0],sg(x[1])]),[`<b>Gains nets · le score</b>`,`<b class="${net>=0?'pos-g':'neg-g'}">${score(net)}</b>`],
     ...(lock?[[`Part co-investie, bloquée (valeur du moment)`,`<b class="neg-g">−${mm(lock)}</b>`]]:[]),
     [`<b>Trésorerie disponible</b>`,`<b class="${mgrCash()>=0?'gold-g':'neg-g'}">${mm(mgrCash())}</b>`]])}
   <p class="note" style="margin-top:6px">${mgrCash()>=0?`Il vous reste <em>${mm(mgrCash())}</em> pour payer budget et ordres.`:`Vous êtes à découvert de <em>${mm(-mgrCash())}</em> : dépenses bloquées jusqu'à la prochaine commission.`}</p>
   <p style="margin:12px 0 4px">Le co-investissement</p>
   ${lock?tbl([[`Part placée à l'ouverture`,`${pc} % · ${mm(S.coinvBase)}`],[`Valeur du moment`,`${mm(lock)}${cLive?' · '+sg(cLive):''}`],[`Rendue à la clôture`,`${mm(S.coinvBase)} × (1 + résultat du fonds)`],[`Part au trimestre prochain`,`${Math.round((S.coinvPct||COINV)*100)} %`]])
     :tbl([[`Part placée en ce moment`,`aucune, trimestre clos`],[`Part au trimestre prochain`,`${pc} % de la trésorerie d'ouverture`]])}
   <p class="note" style="margin-top:6px">À l'ouverture de chaque trimestre, après la commission de gestion, ${pc} % de votre trésorerie entre dans le fonds, aux côtés des investisseurs. Cette somme ne paie ni budget ni ordres. À la clôture, la société la rachète automatiquement : elle récupère la mise plus ou moins le résultat du fonds sur le trimestre, qui passe dans vos gains. Avec vos chiffres, ${mm(ex)} placés rapportent ${mm(ex*0.05)} si le fonds fait +5 % et en coûtent autant s'il fait −5 %. Cumul depuis le début : ${sg((S.mgrCoinv||0)+cLive)}.</p>
   <p class="note">Pourquoi : la commission de performance ne vous fait partager que les gains ; le co-investissement vous fait aussi partager les pertes, en proportion de la part placée. La part se choisit au débriefing, 25 % au moins.</p>
   <details><summary>Chaque ligne, en détail</summary><p class="note"><em>Gestion</em> : ${dec(VOL().mgmt*400,1)} % par an de l'encours, versée à l'ouverture, votre seul revenu certain. <em>Performance</em> : versée à la clôture, seulement au-dessus du plus haut historique du fonds. <em>Bonus</em> : objectif du trimestre tenu. <em>Restitution</em> : si le fonds finit sous son plus haut, vous rendez une part des commissions de performance des quatre derniers trimestres (trois fois le repli, 100 % au plus). <em>Budget</em> : les postes choisis en début de trimestre. <em>Courtage</em> : la facture de vos ordres, dépêches comprises ; l'impact de marché, lui, est payé par le fonds. <em>Autres</em> : ce que les accidents de levier et les incidents opérationnels ont mis à votre charge.</p></details>`);
 """
s=s[:i]+NEW+s[j:]
open('index.html','w',encoding='utf-8').write(s)
print('ok')
