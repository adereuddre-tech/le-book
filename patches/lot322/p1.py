p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# 5. probabilité figée au tirage : celle qu'on affiche est celle qui a joué
rep("""{const u=prng32(hash32('stress'+S.q,S.seed));S.stressQ=null;if(u()<xProbTot()){""","""{const u=prng32(hash32('stress'+S.q,S.seed));S.stressQ=null;S.xPd=null;S.xPd={q:S.q,pS:stressP(),pX:S.q>=1?XPROB:0};if(u()<xProbTot()){   /* lot 322 : probabilités figées au tirage */""")
rep("""   const pS=stressP(),pX=S.q>=1?XPROB:0,mac=u()<pX/(pS+pX);let sc=null;""","""   const pS=S.xPd.pS,pX=S.xPd.pX,mac=u()<pX/(pS+pX);let sc=null;""")
rep("""function xProbTot(){return 1-(1-stressP())*(1-((S&&S.q>=1)?XPROB:0))}
function xScP(sc){const pS=stressP(),pX=(S&&S.q>=1)?XPROB:0,T=xProbTot();""","""function xPs(){return S&&S.xPd&&S.xPd.q===S.q?S.xPd.pS:stressP()}function xPx(){return S&&S.xPd&&S.xPd.q===S.q?S.xPd.pX:((S&&S.q>=1)?XPROB:0)}
function xProbTot(){return 1-(1-xPs())*(1-xPx())}
function xScP(sc){const pS=xPs(),pX=xPx(),T=xProbTot();""")
# 1-2. la protection rend aussi sur les dépêches violentes (moitié) et, à la clôture, un put sur le book
rep("""function hedgeEV(){const k=S.k,bo=0.5+0.5*(TAILM[S.bud.risk]||1);let e=0;STRESS.forEach(x=>{e+=xScP(x)*Math.max(0,-0.5*bo*stressLoss(k,x))});return hH()*e}""",
"""const PUTK=0.03;   /* lot 322 : le put sur le book paie au-delà de −3 % sur le trimestre */
function nCdf(x){const t=1/(1+0.2316419*Math.abs(x)),d=0.3989423*Math.exp(-x*x/2),p=d*t*(0.3193815+t*(-0.3565638+t*(1.781478+t*(-1.821256+t*1.330274))));return x>0?1-p:p}
function hedgeParts(){const k=S.k,w=weights(k),bo=0.5+0.5*(TAILM[S.bud.risk]||1);let ex=0;STRESS.forEach(x=>{ex+=xScP(x)*Math.max(0,-0.5*bo*stressLoss(k,x))});
 let dp=0;(S.evQueue||[]).forEach(ev=>{if(!ev||ev.x||ev.stress||!ev.hit||ev.trader||ev.rivalEv||ev.stake)return;const mh=Math.max(...Object.values(ev.hit).map(Math.abs));if(mh<1)return;
  let im=0;for(const sy in ev.hit){const i=IDX[sy];if(i!==undefined)im+=w[i]*0.5*ev.hit[sy]*INSTR[i].sigQ}dp+=0.5*0.5*Math.abs(im)});   /* sens inconnu : une chance sur deux d'être contre vous */
 const sg=Math.max(1e-6,1.25*pvol(w)/2),d=PUTK/sg,pt=sg*Math.exp(-d*d/2)/Math.sqrt(2*Math.PI)-PUTK*(1-nCdf(d));
 return {ex,dp,pt:Math.max(0,pt)}}
function hedgeEV(){const P=hedgeParts();return hH()*(P.ex+P.dp+P.pt)}   /* lot 322 : extrêmes, dépêches violentes, put sur le book */""")
rep("""let hgB=0;if(ev.x&&S.hedgeQ===S.q&&imm<0)hgB=-imm*hH();""","""let hgB=0;if(S.hedgeQ===S.q&&imm<0){if(ev.x)hgB=-imm*hH();else if(Math.max(...Object.values(ev.hit).map(Math.abs))>=1)hgB=-imm*hH()*0.5}   /* lot 322 : dépêche violente, moitié */
 if(hgB){S.hgGot=(S.hgGot||0)+hgB*S.nav;S.hgPayQ=S.q}""")
rep(""" const navBefore=S.nav;
 const nb=S.nav,q0=Math.max(1e-9,S.navQ0);""",""" /* lot 322 : la protection est aussi un put sur le book, payé à la clôture au-delà de −3 % */
 S.hgPutQ=null;if(S.hedgeQ===S.q){const qp=Math.max(1e-9,S.navQ0),rp=(gross*qp+collateral*S.nav+(S.qColM||0)+(S.qEvM||0)+(S.qIncM||0)-(S.qMgmtM||0))/qp;
  if(rp<-PUTK){const pay=hH()*(-rp-PUTK)*qp;S.nav+=pay;S.qEvM=(S.qEvM||0)+pay;S.hgGot=(S.hgGot||0)+pay;S.hgPayQ=S.q;S.hgPutQ={m:pay,r:rp};S.evLog.push({t:'Protection : put sur le book',pnl:pay/qp,m:pay,lp:0,rc:0})}}
 const navBefore=S.nav;
 const nb=S.nav,q0=Math.max(1e-9,S.navQ0);""")
# 4. compteur
rep("""const cr=hedgeCost(),c=cr*S.nav;S.nav-=c;S.qEvM=(S.qEvM||0)-c;S.hedgeQ=S.q;""","""const cr=hedgeCost(),c=cr*S.nav;S.nav-=c;S.qEvM=(S.qEvM||0)-c;S.hedgeQ=S.q;S.hgPaid=(S.hgPaid||0)+c;""")
# 3. plus de malus du trimestre calme ; bonus quand la protection paie
rep("""if(S.prof==='tail'&&S.hedgeQ===S.q&&!S.stressQ)lpD.push(["Encore un trimestre à payer l'assurance",-1]);   /* lot 271 */""",
    """if(S.hgPayQ===S.q)lpD.push(["La protection a payé : le fonds encaisse quand les autres perdent",S.prof==='tail'?3:1]);   /* lot 322 : plus de malus du trimestre calme */""")
open(p,'w',encoding='utf-8').write(s)
s=open(p,encoding='utf-8').read()
rep("""function hedgeBlock(){const e=xImmEst(),pX=xProbTot(),ev=hedgeEV(),cr=hedgeCost(),c=cr*S.nav,on=S.hedgeQ===S.q||S.hedgePick===S.q;""",
    """function hedgeBlock(){const e=xImmEst(),pX=xProbTot(),ev=hedgeEV(),cr=hedgeCost(),c=cr*S.nav,on=S.hedgeQ===S.q||S.hedgePick===S.q,HP=hedgeParts(),h=hH();""")
rep("""<div class="attr"><span class="an">Ce que la protection rend en moyenne, aux probabilités du marché</span><span class="av"><b>${mm(ev*S.nav)} · ${dec(ev*100,2)} %</b></span></div>""",
    """<div class="attr"><span class="an">Ce que la protection rend en moyenne, aux probabilités du marché</span><span class="av"><b>${mm(ev*S.nav)} · ${dec(ev*100,2)} %</b></span></div>
  <div class="attr"><span class="an" style="padding-left:10px">dont extrêmes · dépêches violentes · put sur le book</span><span class="av">${mm(h*HP.ex*S.nav)} · ${mm(h*HP.dp*S.nav)} · ${mm(h*HP.pt*S.nav)}</span></div>""")
rep("""  <p class="note">La protection rend ${Math.round(hH()*100)} % du choc immédiat de tout événement extrême du trimestre ; la suite du mouvement reste à votre charge, comme pour une dépêche. Sans extrême, la prime est perdue.""",
    """  <p class="note">La protection rend ${Math.round(h*100)} % du choc immédiat de tout événement extrême du trimestre, ${Math.round(h*50)} % de celui d'une dépêche violente (choc d'au moins 1 σ), et, à la clôture, ${Math.round(h*100)} % de la perte du trimestre au-delà de −${Math.round(PUTK*100)} % : un put sur votre propre book. La suite des mouvements reste à votre charge. Si rien de tout cela n'arrive, la prime est perdue.""")
rep("""  <div class="cisel"><button class="hgp${on?'':' on'}" data-h="0">Sans protection</button>""","""  ${(S.hgPaid||0)>0?`<div class="attr"><span class="an">Depuis le début du mandat : primes payées · rendu par la protection</span><span class="av"><b class="neg-g">−${mm(S.hgPaid)}</b> · <b class="pos-g">+${mm(S.hgGot||0)}</b></span></div>`:''}
  <div class="cisel"><button class="hgp${on?'':' on'}" data-h="0">Sans protection</button>""")
rep("""<h2>Protection contre les extrêmes</h2><span class="hint">payée par le fonds</span>""","""<h2>Protection</h2><span class="hint">extrêmes, dépêches violentes, put sur le book · payée par le fonds</span>""")
# textes du style
rep("""w:["investisseurs 10 % plus nerveux","chaque trimestre calme où vous êtes couvert : confiance −1"]""","""w:["investisseurs 10 % plus nerveux","la protection coûte chaque trimestre ; elle ne paie que dans les coups durs"]""")
rep("""['b',"chaque trimestre calme où vous êtes couvert : « encore un trimestre à payer l'assurance », confiance −1"]""","""['g',"quand la protection paie, confiance +3 : « le seul fonds qui a gagné pendant la crise »"]""")
rep("""votre protection contre les extrêmes rend 120 % du choc immédiat au lieu de 70 %""","""votre protection rend 120 % au lieu de 70 % — du choc immédiat d'un extrême, de la moitié de celui d'une dépêche violente, et de la perte du trimestre au-delà de −3 % (put sur le book) —""")
open(p,'w',encoding='utf-8').write(s)
