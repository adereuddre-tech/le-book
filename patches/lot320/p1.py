p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# 1. en-tête : l'exécution standard, et qui paie quoi
rep("""<div class="kv"><span><b style="color:#fff">Ordres, à votre charge</b></span>""","""<p class="note" style="margin:0 0 4px">Exécution standard — deux factures distinctes :</p><div class="kv"><span><b style="color:#fff">Ordres · payés par votre société</b></span>""")
rep("""<div class="kv"><span>Impact de marché, pour le fonds</span>${mn(execImpactAmt(tot,1,S.leakQ))}</div>""","""<div class="kv"><span>Impact de marché · supporté par le fonds</span>${mn(execImpactAmt(tot,1,S.leakQ))}</div>""")
# 2. chaque option : l'écart avec l'exécution standard, pour votre société et pour le fonds
a=s.index(" const stake=c=>{const x=c.e||{};const out=[];let bill=tot;");b=s.index(" const lqNm=",a)
s=s[:a]+""" /* lot 320 : chaque option dit ce qu'elle change par rapport à l'exécution standard, pour votre société et pour le fonds */
 const stake=c=>{const x=c.e||{};let bill=tot,soc=0,fund=0;const extra=[];
  if(x.tcMult){let sub=0;if(x.tcMultOn){orders.forEach(o=>{if(x.tcMultOn.includes(INSTR[o.i].sym))sub+=o.t.cost})}else sub=tot;const d=sub*(x.tcMult-1);bill=tot+d;soc-=d}
  if(x.gainBp)soc+=x.gainBp*1e-4*S.aum0;
  if(x.opex)soc+=x.opex*S.aum0;
  fund+=execImpactAmt(bill,x.tcMult,x.leakQ)-execImpactAmt(tot,1,S.leakQ);
  if(x.cash)fund+=x.cash*S.nav;
  if(x.risk)extra.push(`aléa fonds <em class="${x.risk[1]>=0?'pos-g':'neg-g'}">${Math.round(x.risk[0]*100)} % de ${x.risk[1]>=0?'+':'−'}${mm(Math.abs(x.risk[1])*S.nav)}</em>${x.safePnl?` (sinon ${x.safePnl>=0?'+':'−'}${mm(Math.abs(x.safePnl)*S.nav)})`:''}`);
  if(x.gamble)extra.push(`pari <em class="neg-g">${Math.round(x.gamble[0]*100)} % de risque${x.tcMult?` : coûts ×${dec(x.gamble[1],1)}`:' : gain divisé par −2'}</em>`);
  const f=v=>`<em class="${cls(v)}">${Math.abs(v)<1e-9?'0':(v>0?'+':'−')+mm(Math.abs(v))}</em>`;
  return `<span class="stks"><span class="stk">vs standard · votre société ${f(soc)}</span><span class="stk">le fonds ${f(fund)}</span>${extra.map(t=>`<span class="stk">${t}</span>`).join('')}</span>`};
"""+s[b:]
rep("""${stake(c)}${opxChip(c.e)}${winChip(c.e)}""","""${stake(c)}${winChip(c.e)}""")
# 3. bilan : standard, effet du choix, total — pour la société puis pour le fonds
rep("""  const T1=[row('Facture standard de vos ordres',-(shA?R.bill0:billF-R.dt),'neg-g')];""","""  const T1=[row('Exécution standard · facture des ordres',-(shA?R.bill0:billF-R.dt),'neg-g')];""")
rep("""  if(Math.abs(R.dt)>1e-9)T1.push(row(`Votre choix : coûts ×${dec(R.m,2)}""","""  if(Math.abs(R.dt)>1e-9)T1.push(row(`Effet de votre choix · coûts ×${dec(R.m,2)}""")
rep("""  T1.push(['<b>Facture des ordres</b>',`<b class="neg-g">−${mm(billF)}</b>`]);
  if(Math.abs(mg)>1e-9)T1.push(row(R.g?`${R.g>=0?'Rabais ou commission obtenus':'Rabais repris'}${R.gm?' (pari perdu)':''}`:(R.op<0?'Dépense du choix':'Recette du choix'),mg));
  T1.push(['<b>Net pour votre société de gestion</b>',`<b class="${cls(netM)}">${netM>=0?'+':'−'}${mm(Math.abs(netM))}</b>`]);""",
"""  if(Math.abs(mg)>1e-9)T1.push(row(R.g?`Effet de votre choix · ${R.g>=0?'rabais ou commission obtenus':'rabais repris'}${R.gm?' (pari perdu)':''}`:(R.op<0?'Effet de votre choix · dépense':'Effet de votre choix · recette'),mg));
  T1.push(['<b>Total pour votre société</b>',`<b class="${cls(netM)}">${netM>=0?'+':'−'}${mm(Math.abs(netM))}</b>`]);""")
rep("""  if(im0)T2.push(row('Impact de marché, exécution standard',im0));
  if(Math.abs(imd)>1e-9)T2.push(row(imd<0?'Votre manière d\\'exécuter : prix moyen dégradé':'Votre manière d\\'exécuter : prix moyen protégé',imd));""",
"""  if(im0)T2.push(row('Exécution standard · impact de marché',im0));
  if(Math.abs(imd)>1e-9)T2.push(row(imd<0?'Effet de votre choix · prix moyen dégradé':'Effet de votre choix · prix moyen protégé',imd));""")
rep("""  if(R.cash)T2.push(row('Effet direct sur l\\'encours',R.cash));""","""  if(R.cash)T2.push(row('Effet de votre choix · sur l\\'encours',R.cash));""")
rep("""const H=`<p class="note" style="margin:6px 0 0">Votre choix : ${fxTxt(ch.s,e)}</p><div class="kicker" style="margin:12px 0 2px">Votre société de gestion</div>${tbl(T1)}""",
    """const socD=netM+(shA?R.bill0:billF-R.dt),fundD=fT-im0;
  const H=`<p class="note" style="margin:6px 0 0">Votre choix : ${fxTxt(ch.s,e)}</p>
   <p class="note" style="margin:6px 0 0">Par rapport à l'exécution standard : votre société <b class="${cls(socD)}">${socD>=0?'+':'−'}${mm(Math.abs(socD))}</b> · le fonds <b class="${cls(fundD)}">${fundD>=0?'+':'−'}${mm(Math.abs(fundD))}</b>. Votre société paie les ordres ; le fonds supporte l'impact de marché et les aléas.</p>
   <div class="kicker" style="margin:12px 0 2px">Votre société de gestion · votre trésorerie</div>${tbl(T1)}""")
rep("""   <div class="kicker" style="margin:14px 0 2px">Le fonds</div>${tbl(T2)}""","""   <div class="kicker" style="margin:14px 0 2px">Le fonds · l'encours des investisseurs</div>${tbl(T2)}""")
open(p,'w',encoding='utf-8').write(s)
s=open(p,encoding='utf-8').read()
rep(""" if(e.gamble)sub(e.gamble[0],false);if(e.risk)sub(e.risk[0],riskGood(e));return s}""",
    """ if(e.gamble)sub(e.gamble[0],false);if(e.risk)sub(e.risk[0],riskGood(e));
 if(e.cash&&!/encours|fonds/.test(s))s=s.replace(/([−+-]\\s?\\d+(?:,\\d+)?\\s?pb)/,'$1 de l\\'encours (le fonds)');   /* lot 320 : qui paie */
 return s}""")
rep("""  const f=v=>`<em class="${cls(v)}">${Math.abs(v)<1e-9?'0':(v>0?'+':'−')+mm(Math.abs(v))}</em>`;""","""  const f=v=>`<em class="${Math.abs(v)<1e-6?'dim-g':cls(v)}">${Math.abs(v)<1e-6?'0':(v>0?'+':'−')+mm(Math.abs(v))}</em>`;""")
rep("""Par rapport à l'exécution standard : votre société <b class="${cls(socD)}">${socD>=0?'+':'−'}${mm(Math.abs(socD))}</b> · le fonds <b class="${cls(fundD)}">${fundD>=0?'+':'−'}${mm(Math.abs(fundD))}</b>.""",
    """Par rapport à l'exécution standard : votre société ${Math.abs(socD)<1e-6?'<b class="dim-g">inchangée</b>':`<b class="${cls(socD)}">${socD>=0?'+':'−'}${mm(Math.abs(socD))}</b>`} · le fonds ${Math.abs(fundD)<1e-6?'<b class="dim-g">inchangé</b>':`<b class="${cls(fundD)}">${fundD>=0?'+':'−'}${mm(Math.abs(fundD))}</b>`}.""")
open(p,'w',encoding='utf-8').write(s)
