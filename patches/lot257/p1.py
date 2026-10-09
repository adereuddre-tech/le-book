p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
rep("""const HEDGE={c:0.010,h:0.70};""","""const HEDGE={h:0.70,load:2,min:0.005};   /* lot 257 : prime actuarielle = 2 × ce que la protection rend en moyenne, 0,5 % au moins */
/* ce que la protection rendrait en moyenne ce trimestre, aux probabilités du marché (la veille du desk n'entre pas dans le prix) */
function hedgeEV(){const k=S.k,bo=0.5+0.5*(TAILM[S.bud.risk]||1),wt=STRESS.map(x=>x.ext?1/3:1),tw=wt.reduce((a,b)=>a+b,0),pS=stressP(),pX=S.q>=1?XPROB:0;
 let e=0;STRESS.forEach((x,j)=>{e+=pS*wt[j]/tw*Math.max(0,-0.5*bo*stressLoss(k,x))});
 const xs=MACROEV.filter(m=>m.x);xs.forEach(m=>{e+=pX/xs.length*Math.max(0,-0.5*xEvLoss(k,m.t))});return HEDGE.h*e}
function hedgeCost(){return Math.max(HEDGE.min,HEDGE.load*hedgeEV())}
/* probabilité du marché pour un extrême donné (STRESS : par son poids ; dépêche x:1 : uniforme) */
function xMktP(e){if(e.t){const n=MACROEV.filter(m=>m.x).length;return (S.q>=1?XPROB:0)/Math.max(1,n)}
 const wt=STRESS.map(x=>x.ext?1/3:1),tw=wt.reduce((a,b)=>a+b,0),j=STRESS.findIndex(x=>x.id===e.id);return j<0?0:stressP()*wt[j]/tw}""")
rep(""" if(h&&h.t)return {nm:xHintName(),v:0.5*xEvLoss(k,h.t),sig:1};""",""" if(h&&h.t)return {nm:xHintName(),v:0.5*xEvLoss(k,h.t),sig:1,p:xMktP({t:h.t})};""")
rep(""" return {nm:sc.nm.charAt(0).toLowerCase()+sc.nm.slice(1),v:0.5*bo*stressLoss(k,sc),sig}}""",""" return {nm:sc.nm.charAt(0).toLowerCase()+sc.nm.slice(1),v:0.5*bo*stressLoss(k,sc),sig,p:xMktP({id:sc.id})}}""")
rep("""function hedgeBlock(){const e=xImmEst(),pX=1-(1-stressP())*(1-(S.q>=1?XPROB:0)),c=HEDGE.c*S.nav,on=S.hedgeQ===S.q||S.hedgePick===S.q;""",
    """function hedgeBlock(){const e=xImmEst(),pX=1-(1-stressP())*(1-(S.q>=1?XPROB:0)),ev=hedgeEV(),cr=hedgeCost(),c=cr*S.nav,on=S.hedgeQ===S.q||S.hedgePick===S.q;""")
rep("""  <div class="attr"><span class="an">Prime, ${dec(HEDGE.c*100,0)} % de l'encours</span><span class="av"><b class="neg-g">−${mm(c)}</b></span></div>
  <div class="attr"><span class="an">${e.sig?'Extrême signalé':'Pire extrême pour votre book'} : ${e.nm} · choc immédiat</span>""",
    """  <div class="attr"><span class="an">Ce que la protection rend en moyenne, aux probabilités du marché</span><span class="av"><b>${mm(ev*S.nav)} · ${dec(ev*100,2)} %</b></span></div>
  <div class="attr"><span class="an">Prime : ${cr>HEDGE.min+1e-9?`${dec(HEDGE.load,0)} × ce montant`:`plancher de ${dec(HEDGE.min*100,1)} %`}</span><span class="av"><b class="neg-g">−${mm(c)} · ${dec(cr*100,2)} %</b></span></div>
  <div class="attr"><span class="an">${e.sig?'Extrême signalé':'Pire extrême pour votre book'} : ${e.nm} (probabilité du marché ${dec(e.p*100,1)} %) · choc immédiat</span>""")
rep("""Sans extrême, la prime est perdue.</p>""","""Sans extrême, la prime est perdue. Le marché vend cette protection au double de ce qu'elle rend en moyenne : se couvrir chaque trimestre coûte cher ; elle ne paie que si votre veille vous en dit plus que le marché.</p>""")
rep(""" const c=HEDGE.c*S.nav;S.nav-=c;S.qEvM=(S.qEvM||0)-c;S.hedgeQ=S.q;S.evLog.push({t:'Protection contre les extrêmes',pnl:-HEDGE.c,m:-c,lp:0,rc:0});""",
    """ const cr=hedgeCost(),c=cr*S.nav;S.nav-=c;S.qEvM=(S.qEvM||0)-c;S.hedgeQ=S.q;S.evLog.push({t:'Protection contre les extrêmes',pnl:-cr,m:-c,lp:0,rc:0});""")
open(p,'w',encoding='utf-8').write(s)
