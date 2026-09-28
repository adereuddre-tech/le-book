P='/home/claude/le-book/index.html';s=open(P,encoding='utf-8').read()
def rep(old,new,k=1):
    global s;n=s.count(old);assert n==k,(n,old[:100]);s=s.replace(old,new)
rep("const COINVS=[0.25,0.50,0.75,1.00];","const COINVS=[0.25,0.50,0.75,0.90,0.95,1.00];")
rep("function mgrCash(){return mgrNet()}",
"""/* lot 90 : la part co-investie est bloquée dans le fonds pendant le trimestre — hors de la trésorerie disponible,
   dans l'encours ; elle revient à la clôture avec son résultat (rachat automatique du gérant) */
function coinvLocked(){return S&&S.coinvLock?S.coinvLock*(1+((S.phase==='events'&&S.live)?liveNet():0)):0}
function mgrCash(){return mgrNet()-coinvLocked()}""")
rep("{const tg=coinvPct()*Math.max(0,mgrCash()),d=tg-(S.coinvIn||0);S.nav+=d;S.navQ0+=d;S.coinvBase=tg;S.coinvIn=tg}",
    "{if(S.coinvIn&&!S.coinvLock){S.nav-=S.coinvIn;S.navQ0-=S.coinvIn;S.coinvIn=0}   /* reprise d'une sauvegarde d'avant le lot 90 */\n  const tg=coinvPct()*Math.max(0,mgrCash());S.nav+=tg;S.navQ0+=tg;S.coinvBase=tg;S.coinvIn=tg;S.coinvLock=tg}")
rep("S.mgrCoinv=(S.mgrCoinv||0)+coinv;S.coinvIn=(S.coinvBase||0)*(1+qTotal);",
    "S.mgrCoinv=(S.mgrCoinv||0)+coinv;{const back=(S.coinvBase||0)*(1+qTotal);S.nav-=back;S.coinvIn=0;S.coinvLock=0}   /* rachat automatique du gérant */")
rep("25 % au moins ; la somme placée entre dans l'encours du fonds.</p>",
    "25 % au moins.</p>")
rep("""<p class="note" id="cinote">${mm(coinvPct()*Math.max(0,mgrCash()))} exposés au prochain trimestre.</p></div>`;""",
    """<p class="note" id="cinote">${mm(coinvPct()*Math.max(0,mgrCash()))} placés au prochain trimestre.</p>
  <p class="note" style="margin-top:2px">Bloquée dans le fonds tout le trimestre, cette somme sort de votre trésorerie : elle ne paie ni budget, ni ordres, ni imprévus. Elle vous revient à la clôture, avec son résultat.</p></div>`;""")
rep("n.textContent=`${mm(coinvPct()*Math.max(0,mgrCash()))} exposés au prochain trimestre.`","n.textContent=`${mm(coinvPct()*Math.max(0,mgrCash()))} placés au prochain trimestre.`")
rep("['Dont votre co-investissement',`${mm(S.coinvIn||0)} · ${Math.round(coinvPct()*100)} % de la trésorerie`],['Part de l\\'encours à vous',dec(100*(S.coinvIn||0)/Math.max(1e-9,navNow()),1)+' %'],['Encours sous gestion, hors vous',moneyB(navNow()-(S.coinvIn||0))],",
    "['Dont votre co-investissement, bloqué ce trimestre',S.coinvLock?`${mm(coinvLocked())} · ${Math.round(coinvPct()*100)} % de la trésorerie`:'aucun (rendu à la clôture)'],['Part de l\\'encours à vous',dec(100*coinvLocked()/Math.max(1e-9,navNow()),1)+' %'],['Encours sous gestion, hors vous',moneyB(navNow()-coinvLocked())],")
open(P,'w',encoding='utf-8').write(s);print('ok')
