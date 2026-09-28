P='/home/claude/le-book/index.html';s=open(P,encoding='utf-8').read()
def rep(old,new,k=1):
    global s;n=s.count(old);assert n==k,(n,old[:100]);s=s.replace(old,new)

# ---- co-investissement choisi, restitution, trésorerie unique ----
rep("const COINV=0.10;","""const COINV=0.10;
/* lot 82 : le gérant choisit à chaque clôture la part de sa trésorerie placée dans le fonds (10 % au moins) ;
   la part placée est comptée dans la trésorerie à sa valeur du moment — un seul chiffre, le score */
const COINVS=[0.10,0.25,0.50,0.75,1.00];
function coinvPct(){return S.coinvPct||COINV}
/* restitution : sous le plus-haut, le gérant rend CLAW × repli des commissions de performance des quatre
   derniers trimestres (plafonné à 100 %) ; ce qui a été rendu ne l'est pas deux fois */
const CLAW=3;""")
rep("function mgrNet(){return S.mgrFees-S.mgrCosts-(S.phase==='book'?liveTC():(S.pendingTC||0)*S.nav)}",
    "function mgrNet(){return S.mgrFees-S.mgrCosts-(S.phase==='book'?liveTC():(S.pendingTC||0)*S.nav)+((S.phase==='events'&&S.live&&S.coinvBase)?S.coinvBase*liveNet():0)}")
rep(" S.coinvBase=Math.max(0,mgrCash());   /* lot 81 : la part co-investie est fixée à l'ouverture */",
    " S.coinvBase=coinvPct()*Math.max(0,mgrCash());S.lpQ0=S.lp;   /* lot 81-82 : part co-investie fixée à l'ouverture */")
rep(" const coinv=COINV*(S.coinvBase||0)*qTotal;if(coinv>=0)S.mgrFees+=coinv;else S.mgrCosts-=coinv;S.mgrCoinv=(S.mgrCoinv||0)+coinv;refreshGain();",
""" const coinv=(S.coinvBase||0)*qTotal;if(coinv>=0)S.mgrFees+=coinv;else S.mgrCosts-=coinv;S.mgrCoinv=(S.mgrCoinv||0)+coinv;
 (S.perfH=S.perfH||[]).push(perf*navBefore);let claw=0,clawSh=0;
 if(S.idx<S.hwmIdx-1e-12){clawSh=Math.min(1,CLAW*(1-S.idx/S.hwmIdx));
  for(let q=Math.max(0,S.perfH.length-4);q<S.perfH.length;q++){claw+=clawSh*S.perfH[q];S.perfH[q]*=1-clawSh}
  S.mgrCosts+=claw;S.mgrClaw=(S.mgrClaw||0)+claw}
 refreshGain();""")
rep("tc:tc*navBefore,coinv,cb:COINV*(S.coinvBase||0)};","tc:tc*navBefore,coinv,cb:S.coinvBase||0,cp:coinvPct(),claw,clawSh};")
rep(" const mg=v.mgmt*rv.mAum,cost=rivalCostQ(rv)*rv.mAum,ci=COINV*Math.max(0,rv.mgr||0)*r;   /* lot 81 : leur co-investissement */",
    " const mg=v.mgmt*rv.mAum,cost=rivalCostQ(rv)*rv.mAum,ci=COINV*Math.max(0,rv.mgr||0)*r;   /* lot 81 : leur co-investissement (10 %) */")
rep(" rv.mgr+=mg+perf-cost+ci;\n}"," (rv.perfH=rv.perfH||[]).push(perf);let cl=0;\n if(rv.cum<(rv.peak||1)-1e-12){const sh=Math.min(1,CLAW*(1-rv.cum/rv.peak));for(let q=Math.max(0,rv.perfH.length-4);q<rv.perfH.length;q++){cl+=sh*rv.perfH[q];rv.perfH[q]*=1-sh}}\n rv.mgr+=mg+perf-cost+ci-cl;\n}")

# ---- clôture du fonds ----
rep("const NAVEND=0.05;","const NAVEND=0.05;\n/* lot 82 : le fonds ferme sous 50 M$ d'encours (rachats compris) ou à 50 % de perte depuis le plus haut (hors rachats) */\nconst FUNDMIN=0.05,DDEND=0.50;")
rep(" if(S.nav<NAVEND*S.aum0)S.over='nav';"," if(S.nav<FUNDMIN)S.over='nav';else if(1-S.idx/Math.max(S.idx,S.peakIdx||1)>=DDEND-1e-9)S.over='dd';")
rep("Le fonds ne s'arrête que sous <em>${moneyB(NAVEND*S.aum0)}</em>, 5 % de l'encours de départ.",
    "Le fonds ferme sous <em>${moneyB(FUNDMIN)}</em> d'encours (rachats compris), ou dès que la perte depuis le plus haut atteint <em>${Math.round(DDEND*100)} %</em>.")
rep("""verdict="L'encours n'y est plus";vtxt=`Le fonds est tombé sous 5 % de son encours de départ au trimestre ${S.q} :""",
    """verdict=S.over==='dd'?"Moitié perdue":"L'encours n'y est plus";vtxt=S.over==='dd'?`Au trimestre ${S.q}, le fonds a perdu la moitié de sa valeur depuis son plus haut : les investisseurs et le conseil ferment le mandat.`:`Le fonds est tombé sous ${moneyB(FUNDMIN)} d'encours au trimestre ${S.q} :""")

# ---- carton rouge : deux contraintes ----
rep("function redOn(id){return !!(S&&S.redOn&&S.redC&&S.redC.id===id)}",
    "function redOn(id){return !!(S&&S.redOn&&S.redC&&(S.redC.list?S.redC.list.some(c=>c.id===id):S.redC.id===id))}\n/* lot 82 : le rouge impose deux contraintes distinctes */\nfunction redDraw2(w){const a=redDraw(w),b=redDraw(w,[a.id,a.id==='shut'?'class':a.id==='class'?'shut':'',a.id==='risk'?'noadd':a.id==='noadd'?'risk':'']);\n return {id:a.id,nm:a.nm+' et '+b.nm.toLowerCase(),t:a.t+' ; '+b.t,list:[a,b]}}")
rep("function redDraw(w){\n const u=prng32(hash32('redc'+S.q+'_'+((S.cards&&S.cards.r)||0),S.seed));\n const av=REDC.filter(c=>c.id!==S.redLast),",
    "function redDraw(w,excl){\n const u=prng32(hash32('redc'+S.q+'_'+((S.cards&&S.cards.r)||0)+(excl?'b':''),S.seed));\n const av=REDC.filter(c=>c.id!==S.redLast&&!(excl||[]).includes(c.id)),")
rep(" S.redLast=c.id;return c;"," if(!excl)S.redLast=c.id;return c;")
rep(" const id=S.redC.id,sp=riskShown(weights(S.k)).total;\n if(id==='risk'"," const sp=riskShown(weights(S.k)).total;\n for(const id of (S.redC.list?S.redC.list.map(c=>c.id):[S.redC.id])){\n if(id==='risk'")
rep(" if(id==='lines'){const n=S.k.filter(v=>v).length;if(n>4)return `Carton rouge : ${n} lignes, quatre au plus`}\n return '';"," if(id==='lines'){const n=S.k.filter(v=>v).length;if(n>4)return `Carton rouge : ${n} lignes, quatre au plus`}}\n return '';")
rep("const rn=redDraw(wFin);S.qCard=","const rn=redDraw2(wFin);S.qCard=")
rep("<li>Au prochain trimestre : <b>${qc.cn?qc.cn.nm:'contrainte'}</b> — ${qc.cn?qc.cn.t:''}.</li>",
    "${qc.cn&&qc.cn.list?qc.cn.list.map(c=>`<li>Au prochain trimestre : <b>${c.nm}</b> — ${c.t}.</li>`).join(''):`<li>Au prochain trimestre : <b>${qc.cn?qc.cn.nm:'contrainte'}</b> — ${qc.cn?qc.cn.t:''}.</li>`}")

# ---- engagement : hors plafonnement ----
rep(" if(S.commRes)lpD.push([`Engagement « ${S.comm.nm.toLowerCase()} » ${S.commRes.ok?'tenu':'manqué'}`,S.commRes.ok?S.comm.win.lp:S.comm.lose.lp]);","")
rep(" const dlpC=Math.max(-30,Math.min(22,dlp*(dlp<0?SIZE().lpNeg:1)));if(dlpC!==dlp)lpD.push(['Plafonnement',dlpC-dlp]);",
    """ let dlpC=Math.max(-30,Math.min(22,dlp*(dlp<0?SIZE().lpNeg:1)));if(dlpC!==dlp)lpD.push(['Plafonnement',dlpC-dlp]);
 /* lot 82 : l'engagement se solde hors plafonnement — sinon un bon trimestre l'absorbait */
 if(S.commRes){const e=S.commRes.ok?S.comm.win.lp:S.comm.lose.lp;lpD.push([`Engagement « ${S.comm.nm.toLowerCase()} » ${S.commRes.ok?'tenu':'manqué'} (hors plafonnement)`,e]);dlpC+=e}""")

# ---- flèche de confiance : les appels enchaînés d'une même action se cumulent ----
rep("S.gLog.push({why,lp:d,rc:drc});S.lastG={lp:d,rc:drc,lp0,rc0};",
    "S.gLog.push({why,lp:d,rc:drc});{const now=Date.now(),mg=S.lastG&&S.lastG.at&&now-S.lastG.at<250;   /* lot 82 */\n   S.lastG=mg?{lp:S.lastG.lp+d,rc:S.lastG.rc+drc,lp0:S.lastG.lp0,rc0:S.lastG.rc0,at:now}:{lp:d,rc:drc,lp0,rc0,at:now}}")

# ---- panneau : T5/8 ----
rep("${S.fundName.split(' ')[0]}${done?` · T${S.q}`:` · T${Math.min(S.q+1,QT())}`}","${S.fundName.split(' ')[0]}${done?` · T${S.q}/${QT()}`:` · T${Math.min(S.q+1,QT())}/${QT()}`}")
open(P,'w',encoding='utf-8').write(s);print('ok')
