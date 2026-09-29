# Lot 104, p2 : sans seuil d'encours, un fonds presque vidé rend la marge ingérable (marge / encours explose) ;
# la coupe (60 unités au plus) et la liquidation (90 % au plus) pouvaient laisser la marge au-dessus du seuil :
# appel de marge en boucle (campagne bloquée, graine 1009 flux). Si le choix ne suffit pas, le book est soldé.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("  else{const r0=liveRet();S.k=o.k;const r1=liveRet();S.qEvM=(S.qEvM||0)+(r0-r1)*S.navQ0;S.pendingTC+=o.tc/S.nav;S.totalTC+=o.tc}\n",
    "  else{const r0=liveRet();S.k=o.k;const r1=liveRet();S.qEvM=(S.qEvM||0)+(r0-r1)*S.navQ0;S.pendingTC+=o.tc/S.nav;S.totalTC+=o.tc}\n  if(marginPct(S.k)>MGC.thr){const r0=liveRet();S.k=S.k.map(()=>0);const r1=liveRet();S.qEvM=(S.qEvM||0)+(r0-r1)*S.navQ0;toast('Marge toujours au-delà du seuil : le prime broker solde le book.')}   /* lot 104 */\n")
open('index.html','w',encoding='utf-8').write(s);print('lot104 p2 ok')
