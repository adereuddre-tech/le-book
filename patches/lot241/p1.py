# Lot 241 : bilan d'une anecdote d'exécution lisible et relié au choix. Trois blocs chiffrés :
#  1. votre société de gestion : facture standard des ordres → effet du choix (coûts ×m) → ajustements de positions →
#     facture finale ; gain ou dépense direct du choix ; net ;
#  2. le fonds : impact de marché d'une exécution standard (2,4 × la facture, expliqué) → effet de la manière d'exécuter
#     (×m^−1,2, fuite ×1,6) → aléa du choix, avec sa probabilité et son issue (« le risque ne s'est pas produit » au lieu
#     de « le marché n'a pas bougé ») → effet direct ; total ;
#  3. confiance : manière d'exécuter, effet propre du choix, résultat pour le fonds, en une seule unité (confiance).
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
rep("  const ch=ev.ch[+b.dataset.i],e=ch.e;let msg=[];const navB0=S.nav;",
    "  const ch=ev.ch[+b.dataset.i],e=ch.e;let msg=[];const navB0=S.nav;const R={g:0,op:0,dt:0,m:1,rk:null,cash:0,gm:false,bill0:tot};   /* lot 241 */")
rep("msg.push(\"Le tuyau a mal tourné.\")}S.mgrCosts-=g;","msg.push(\"Le tuyau a mal tourné.\");R.gm=true}S.mgrCosts-=g;R.g=g;")
rep("if(e.gamble&&rng()<pAdj(e.gamble[0],false)){m=e.gamble[1];msg.push(\"Le gros acheteur s'est aperçu de la manœuvre et a tout retiré.\")}",
    "if(e.gamble&&rng()<pAdj(e.gamble[0],false)){m=e.gamble[1];msg.push(\"Le gros acheteur s'est aperçu de la manœuvre et a tout retiré.\");R.gm=true}")
rep("   const delta=sub*(m-1);S.pendingTC+=delta/S.nav;","   const delta=sub*(m-1);S.pendingTC+=delta/S.nav;R.dt=delta;R.m=m;R.sub=sub;R.on=e.tcMultOn;")
rep("   if(im){execSlip(im,'Impact');msg.push(`Impact de marché sur le prix moyen : ${mn(im)} pour le fonds.`)}}",
    "   R.billI=bill;R.im=im;R.im0=execImpactAmt(bill,1,false);\n   if(im){execSlip(im,'Impact');msg.push(`Impact de marché sur le prix moyen : ${mn(im)} pour le fonds.`)}}")
rep("  if(e.risk){if(rng()<pAdj(e.risk[0],riskGood(e))){S.nav*=(1+e.risk[1]);S.qEvM+=e.risk[1]*navB0;",
    "  if(e.risk){R.rk={p:pAdj(e.risk[0],riskGood(e)),v:e.risk[1],hit:false};if(rng()<R.rk.p){R.rk.hit=true;S.nav*=(1+e.risk[1]);S.qEvM+=e.risk[1]*navB0;")
rep("   else if(e.safePnl){S.nav*=(1+e.safePnl);S.qEvM+=e.safePnl*navB0;e._hit=true;msg.push(e.safeTxt)}}",
    "   else if(e.safePnl){R.rk.safe=e.safePnl;S.nav*=(1+e.safePnl);S.qEvM+=e.safePnl*navB0;e._hit=true;msg.push(e.safeTxt)}}")
rep("  if(e.cash){S.nav*=(1+e.cash);S.qEvM+=e.cash*navB0;","  if(e.cash){R.cash=e.cash*S.nav;S.nav*=(1+e.cash);S.qEvM+=e.cash*navB0;")
_i=s.index("function screenExec(){");_j=s.index("  if(e.opex){const a=e.opex*S.aum0;S.mgrCosts-=a;",_i)
s=s[:_j]+"  if(e.opex){const a=e.opex*S.aum0;R.op=a;S.mgrCosts-=a;"+s[_j+len("  if(e.opex){const a=e.opex*S.aum0;S.mgrCosts-=a;"):]
rep("""  if(e.risk&&!e._hit)msg.push(e.safeTxt||"Le marché n'a pas bougé pendant l'exécution.");""",
    """  if(e.risk&&!e._hit)msg.push(e.safeTxt||"Le risque annoncé ne s'est pas produit.");""")
# carte de résultat
a=s.index("  const KEY=[['Coûts d\\'exécution du trimestre'")
b=s.index("\"Lancer le trimestre\",phaseLive,{key:KEY});",a)+len("\"Lancer le trimestre\",phaseLive,{key:KEY});")
s=s[:a]+r"""  /* lot 241 : bilan en trois blocs, dans l'ordre du choix */
  const billF=S.pendingTC*S.nav,adj=billF-R.bill0-R.dt,mg=R.g+R.op,netM=-billF+mg;
  const row=(l,v,c)=>[l,`<span class="${c||cls(v)}">${v>=0?'+':'−'}${mm(Math.abs(v))}</span>`];
  const shA=Math.abs(adj)>Math.max(2e-6,0.02*R.bill0);   /* en dessous : arrondi, rattaché à la facture standard */
  const T1=[row('Facture standard de vos ordres',-(shA?R.bill0:billF-R.dt),'neg-g')];
  if(Math.abs(R.dt)>1e-9)T1.push(row(`Votre choix : coûts ×${dec(R.m,2)}${R.on?' sur '+R.on.join(', '):''}${R.gm?' (pari perdu)':''}`,-R.dt));
  if(shA)T1.push(row(adj<0?'Positions réduites : ordres en moins':'Positions ajoutées : ordres en plus',-adj));
  T1.push(['<b>Facture des ordres</b>',`<b class="neg-g">−${mm(billF)}</b>`]);
  if(Math.abs(mg)>1e-9)T1.push(row(R.g?`${R.g>=0?'Rabais ou commission obtenus':'Rabais repris'}${R.gm?' (pari perdu)':''}`:(R.op<0?'Dépense du choix':'Recette du choix'),mg));
  T1.push(['<b>Net pour votre société de gestion</b>',`<b class="${cls(netM)}">${netM>=0?'+':'−'}${mm(Math.abs(netM))}</b>`]);
  const im0=R.im0||0,imd=(R.im||0)-im0,rkA=R.rk?(R.rk.hit?R.rk.v*navB0:(R.rk.safe||0)*navB0):0,fT=(S.nav-navB0);
  const T2=[];
  if(im0)T2.push(row('Impact de marché, exécution standard',im0));
  if(Math.abs(imd)>1e-9)T2.push(row(imd<0?'Votre manière d\'exécuter : prix moyen dégradé':'Votre manière d\'exécuter : prix moyen protégé',imd));
  if(R.rk)T2.push([`Aléa du choix : ${Math.round(R.rk.p*100)} % de chances de ${sgn(R.rk.v,1)}`,R.rk.hit?`<span class="${cls(R.rk.v)}">arrivé · ${R.rk.v>=0?'+':'−'}${mm(Math.abs(rkA))}</span>`:(R.rk.safe?`<span class="${cls(R.rk.safe)}">évité · ${R.rk.safe>=0?'+':'−'}${mm(Math.abs(rkA))}</span>`:'<span class="dim-g">pas arrivé · 0</span>')]);
  if(R.cash)T2.push(row('Effet direct sur l\'encours',R.cash));
  T2.push(['<b>Total pour le fonds</b>',`<b class="${cls(fT)}">${fT>=0?'+':'−'}${mm(Math.abs(fT))} · ${sgn(fT/navB0,1)}</b>`]);
  const C3=[];const ccx=(l,z)=>{const v=Math.round(z.lp||0);if(v)C3.push([l,`<span class="${cls(v)}">${v>0?'+':'−'}${Math.abs(v)}</span>`])};
  ccx("Manière d'exécuter (le comité veut le tarif standard)",g3);ccx('Effet propre du choix',g2);ccx('Résultat pour le fonds',g);
  const cT=Math.round(g.lp+g2.lp+g3.lp);C3.push(['<b>Total</b>',`<b class="${cls(cT)}">${cT>0?'+':cT<0?'−':''}${Math.abs(cT)}</b>`]);
  const book=msg.filter(t=>/ramené|→|inversée/.test(t));
  const H=`<p class="note" style="margin:6px 0 0">Votre choix : ${fxTxt(ch.s,e)}</p><div class="kicker" style="margin:12px 0 2px">Votre société de gestion</div>${tbl(T1)}
   <div class="kicker" style="margin:14px 0 2px">Le fonds</div>${tbl(T2)}
   <details style="margin-top:4px"><summary>Qu'est-ce que l'impact de marché ?</summary><p class="note">En achetant ou en vendant, vos ordres poussent le prix contre vous : l'écart entre le prix au moment de la décision et le prix moyen obtenu est perdu par le fonds, pas par vous. En exécution standard, il vaut ${dec(IMPK,1)} fois la facture des ordres. Payer plus cher pour être servi vite (bloc, coûts ×1,2…) le réduit ; négocier un rabais (coûts ×0,8…) laisse le marché vous voir venir et l'augmente (facteur coûts<sup>−1,2</sup>) ; si vos ordres fuitent, il est multiplié par 1,6.</p></details>
   ${book.length?`<div class="kicker" style="margin:14px 0 2px">Votre book</div><p class="note" style="margin:0">${book.join(' ')}</p>`:''}
   <div class="kicker" style="margin:14px 0 2px">Confiance</div>${tbl(C3)}`;
  resultCard('EXÉCUTION · '+ev.who.split(' ·')[0].toUpperCase(),ch.b,[],[],
   "Lancer le trimestre",phaseLive,{top:H});"""+s[b:]
open('index.html','w',encoding='utf-8').write(s);print('lot241 ok')
