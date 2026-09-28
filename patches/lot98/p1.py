# Lot 98 : trésorerie projetée au débriefing (bonus d'équipe, puis co-investissement calculé après le bonus) ;
# point fantôme du graphique rentabilité / risque avec le collatéral ; restitution supprimée ; bonus de départ
# rendu visible dans le budget.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
# 1. ordre : bonus, puis co-investissement sur la trésorerie restante, puis commission de gestion (hors co-investissement)
rep("S.tresQ0=mgrCash();   /* lot 87 */\n payBonus();   /* lot 95 */","S.tresQ0=mgrCash();   /* lot 87 */\n payBonus();   /* lot 95 */\n const cashCo=Math.max(0,mgrCash());   /* lot 98 : co-investissement en % de la trésorerie après bonus */")
rep("const tg=S.q>=1?coinvPct()*Math.max(0,mgrCash()):0;","const tg=S.q>=1?coinvPct()*cashCo:0;")
rep("function mgrCash(){return mgrNet()-coinvLocked()}",r'''function mgrCash(){return mgrNet()-coinvLocked()}
/* lot 98 : au débriefing, la trésorerie affichée déduit déjà le bonus d'équipe choisi puis la part co-investie */
function bonPend(){if(!S||S.phase!=='debrief'||S.over||S.q>=QT())return 0;const pf=(S.mgrQ&&S.mgrQ.perf)||0;return pf>0?Math.min(BONUS[S.bonI||0]*pf,Math.max(0,mgrCash())):0}
function coPend(){if(!S||S.phase!=='debrief'||S.over||S.q>=QT())return 0;return coinvPct()*Math.max(0,mgrCash()-bonPend())}
function cashView(){return mgrCash()-bonPend()-coPend()}''')
rep("function refreshGain(){const e=document.getElementById('gaintile');if(!e||!S)return;\n const v=mgrCash();","function refreshGain(){const e=document.getElementById('gaintile');if(!e||!S)return;\n const v=cashView();")
rep('<b id="gaintile" class="${mgrCash()>=0?\'\':\'neg-g\'}">${treso(mgrCash())}</b>','<b id="gaintile" class="${cashView()>=0?\'\':\'neg-g\'}">${treso(cashView())}</b>')
rep("<p class=\"note\" id=\"cinote\">${mm(coinvPct()*Math.max(0,mgrCash()))} placés au prochain trimestre.</p>","<p class=\"note\" id=\"cinote\">${mm(coPend())} placés au prochain trimestre, calculés après le bonus d'équipe.</p>")
rep("const n=document.getElementById('cinote');if(n)n.textContent=`${mm(coinvPct()*Math.max(0,mgrCash()))} placés au prochain trimestre.`});","const n=document.getElementById('cinote');if(n)n.textContent=`${mm(coPend())} placés au prochain trimestre, calculés après le bonus d'équipe.`;refreshGain()});")
rep("app.querySelectorAll('.bnp').forEach(b=>b.onclick=()=>{S.bonI=+b.dataset.i;app.querySelectorAll('.bnp').forEach(x=>x.classList.toggle('on',x===b))});","app.querySelectorAll('.bnp').forEach(b=>b.onclick=()=>{S.bonI=+b.dataset.i;app.querySelectorAll('.bnp').forEach(x=>x.classList.toggle('on',x===b));\n  const n=document.getElementById('cinote');if(n)n.textContent=`${mm(coPend())} placés au prochain trimestre, calculés après le bonus d'équipe.`;refreshGain()});")
# 2. point fantôme : même mesure du risque que le point courant (collatéral compris)
rep("{x:riskShown(weights(kB)).total/2,y:profitBook(kB)}","{x:Math.sqrt((riskShown(weights(kB)).total/2)**2+cs*cs),y:profitBook(kB)}")
# 3. restitution supprimée (joueur et concurrents)
rep("const CLAW=3;","const CLAW=0;   /* lot 98 : restitution supprimée, le co-investissement fait déjà partager les pertes */")
rep(" <em>Restitution</em> : si le fonds finit sous son plus haut, vous rendez une part des commissions de performance des quatre derniers trimestres (trois fois le repli, 100 % au plus).","")
rep("['Restitution',-(Gq.claw||0)],","")
rep("[`Restitution de commissions`,-(S.mgrClaw||0)],","...((S.mgrClaw||0)>0?[[`Restitution (avant le lot 98)`,-(S.mgrClaw||0)]]:[]),")
# 4. bonus de départ visible
rep("<p class=\"note\" style=\"margin:2px 0 6px\">${b.id==='fo'?`Touchez une personne : l'équipe va jusqu'à elle. Le prix est celui de toute l'équipe.`:`Touchez un poste : le back office va jusqu'à lui.`}</p>",
 "<p class=\"note\" style=\"margin:2px 0 6px\">${b.id==='fo'?`Touchez une personne : l'équipe va jusqu'à elle. Le prix est celui de toute l'équipe.`:`Touchez un poste : le back office va jusqu'à lui.`} <b class=\"neg-g\">Descendre, c'est licencier : chaque partant touche son bonus de départ, un trimestre de salaire.</b></p>")
rep("<span class=\"tbp\">${l.bp} pb<br>${o?mm(l.bp*1e-4*S.nav):'hors caisse'}</span>","<span class=\"tbp\">${l.bp} pb<br>${o?mm(l.bp*1e-4*S.nav):'hors caisse'}${S.budPrev&&i<S.budPrev[b.id]?`<br><span class=\"neg-g\">départs −${mm((b.lv[S.budPrev[b.id]].bp-l.bp)*1e-4*S.nav)}</span>`:''}</span>")
open('index.html','w',encoding='utf-8').write(s);print('ok')
