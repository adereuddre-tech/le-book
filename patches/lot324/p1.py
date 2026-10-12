p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)

# événements du desk à « coûts ±x % » : appliqués à la facture d'ordres du trimestre et aux ajustements à venir
rep("""  if(e.tcMultQ)S.tcMultQ=e.tcMultQ;
  if(e.cash){pnl+=e.cash;""","""  if(e.tcMultQ)S.tcMultQ=e.tcMultQ;
  let tcD=0;if(e.tcMult&&!e.tcMultQ){const b=(S.pendingTC||0)*S.nav;tcD=b*(e.tcMult-1);S.pendingTC+=tcD/S.nav;S.totalTC+=tcD;S.tcMultQ*=e.tcMult;
   msg.push(`Coûts d'exécution du trimestre ${e.tcMult>1?'+':'−'}${Math.round(Math.abs(e.tcMult-1)*100)} % : ${tcD>=0?'+':'−'}${mm(Math.abs(tcD))} sur la facture d'ordres (${mm(b)}), payés par votre société de gestion ; les ajustements à venir suivent le même tarif.`)}
  if(e.cash){pnl+=e.cash;""")
rep("""Aller sur le desk",next,{key:[['<b>Résultat</b>',`<span class="${cls(total)}">${sgn(total,1)} · ${mn(total*navB)}</span>`],['Confiance',""",
    """Aller sur le desk",next,{key:[['<b>Résultat</b>',`<span class="${cls(total)}">${sgn(total,1)} · ${mn(total*navB)}</span>`],...(tcD?[["Coûts d'exécution · société",`<span class="${cls(-tcD)}">${mn(-tcD)}</span>`]]:[]),['Confiance',""")
open(p,'w',encoding='utf-8').write(s)
