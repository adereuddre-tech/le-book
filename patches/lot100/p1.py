# Lot 100 (refonte A, le prime broker) :
# - ordre du trimestre : ouverture → desk (contexte) → budget → book ; les rumeurs suivent le budget de recherche ;
# - marge : taux par marché × type de produit (coté / gré à gré) × multiplicateur du prime broker (liquidité à
#   l'ouverture, relevé après les grosses dépêches) ; contrôlée après chaque événement (stepEvents) : appel de marge
#   avec trois sorties (apport de la société de gestion, coupe choisie, liquidation par le prime broker) ;
# - la marge déposée rapporte le taux des T-bills −10 pb, le reste suit le placement choisi ;
# - plus d'accident « appel de marge » tiré au hasard (TAILMG 0), plus de pénalité de confiance à la validation.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
# --- ordre des écrans
rep('"Première décision : le budget d\'exploitation."],\n  "Fixer le budget",screenBudget);','"D\'abord, le contexte du trimestre ; ensuite le budget, juste avant le book."],\n  "Voir le desk",phaseDesk);')
rep("[`Budget validé : <b>${budgetBp().toFixed(0)} pb</b>, soit ${mm(budgetBp()*1e-4*S.nav)}.`,`${nr} rumeurs ont été collectées${S.rupture?', et une rupture factorielle signalée':''}.`,",
    "[`Les rumeurs arriveront après le budget : la recherche décide de leur nombre et de leur qualité.`,`Prime broker : marges à <b>×${dec(S.mgMult||1,2)}</b> du barème ce trimestre${(S.mgMult||1)>1.05?', liquidité oblige':''}.`,")
rep('"Vous positionnez le book pour les trois prochains mois."],\n  "Voir le desk",()=>{if(S.preDesk&&(!S.preDesk.cond||S.preDesk.cond())){const ev=S.preDesk;S.preDesk=null;screenTraderEvent(ev,screenPlay)}else screenPlay()});',
    '"Prochaine étape : le budget, puis le book pour les trois prochains mois."],\n  "Fixer le budget",screenBudget);')
rep("<button class=\"cta\" id=\"ok\">Valider le budget et voir le desk</button>","<button class=\"cta\" id=\"ok\">Valider le budget et passer au book</button>")
rep("   planSignalsAfterBudget();phaseDesk();\n","   planSignalsAfterBudget();\n   if(S.preDesk&&(!S.preDesk.cond||S.preDesk.cond())){const ev=S.preDesk;S.preDesk=null;screenTraderEvent(ev,screenPlay)}else screenPlay();\n")
# --- types de produits et taux de marge
rep("const CLASSES=['Actions','Taux','Devises','Matières premières','Exotiques'];",r'''const CLASSES=['Actions','Taux','Devises','Matières premières','Exotiques'];
/* lot 100 : type de produit. Les devises se traitent en forwards, le fret et la pluie en swaps : gré à gré, marge ×1,3. */
const PTYPE={fut:{nm:'future coté',m:1.0},otc:{nm:'gré à gré (forward, swap)',m:1.3}};
INSTR_ALL.forEach(x=>{x.pt=['EUR','JPY','GBP','AUD','MXP','BDI','NRAM'].includes(x.sym)?'otc':'fut'});
function mgRate(i){const x=INSTR[i];return x.mg*((PTYPE[x.pt]||PTYPE.fut).m)*((S&&S.mgMult)||1)}''')
rep("function marginPct(k){let m=0;for(let i=0;i<N;i++)m+=Math.abs(notionalBn(k[i],i))*INSTR[i].mg;return m/Math.max(1e-9,S.nav)}",
    "function marginPct(k){let m=0;for(let i=0;i<N;i++)m+=Math.abs(notionalBn(k[i],i))*mgRate(i);return m/Math.max(1e-9,S.nav)}")
rep(" S.liq=R.liq*(1+0.15*gauss());S.liq=Math.max(0.7,S.liq);"," S.liq=R.liq*(1+0.15*gauss());S.liq=Math.max(0.7,S.liq);\n S.mgMult=1+0.3*Math.max(0,S.liq-1);S.mgBusy=false;   /* lot 100 : barème du prime broker ce trimestre */")
# relèvement après une grosse dépêche
rep('const gn=mh>0.8?gauge(-(0.4+0.5*mh),-(0.2+0.2*mh),"Nervosité : investisseurs et comité lisent les mêmes dépêches que vous"):{lp:0,rc:0};',
    'const gn=mh>0.8?gauge(-(0.4+0.5*mh),-(0.2+0.2*mh),"Nervosité : investisseurs et comité lisent les mêmes dépêches que vous"):{lp:0,rc:0};\n if(mh>0.8){const m0=S.mgMult||1;S.mgMult=Math.min(1.8,m0*(1+0.06*mh));toast(`Le prime broker relève ses marges : ×${dec(m0,2)} → ×${dec(S.mgMult,2)}`)}   /* lot 100 */')
# --- contrôle après chaque événement
rep("function stepEvents(){\n S.bigTape=false;\n save('stepEvents');","function stepEvents(){\n S.bigTape=false;\n if(S.live&&marginPct(S.k)>MGC.thr+1e-9){screenMarginCall();window.scrollTo(0,0);return}   /* lot 100 */\n save('stepEvents');")
rep("function screenIncident(){",r'''/* lot 100 : appel de marge, vérifié après chaque événement du trimestre. Cible : revenir à MGC.back de l'encours. */
function mgPlan(){const nav=S.nav,mgu=marginPct(S.k),req=mgu*nav,tg=MGC.back;
 const inj=Math.max(0,req/tg-nav);
 /* coupe choisie : on retire d'abord les unités qui consomment le plus de marge, au coût d'urgence ×1,3 */
 const k=[...S.k];let c1=0;for(let g=0;g<60&&marginPct(k)>tg;g++){let bi=-1,bv=0;for(let i=0;i<N;i++){if(!k[i])continue;const v=Math.abs(notionalBn(1,i))*mgRate(i);if(v>bv){bv=v;bi=i}}
  if(bi<0)break;const d=-Math.sign(k[bi]);c1+=tcost(d,bi).cost*1.3;k[bi]+=d}
 const f=Math.max(0.05,Math.min(0.9,1-tg/mgu)),k2=S.k.map(v=>Math.trunc(v*(1-f)));let c2=0;for(let i=0;i<N;i++){const d=k2[i]-S.k[i];if(d)c2+=tcost(d,i).cost*MGC.crisis}
 return {mgu,inj,k1:k,c1,k2,c2,f}}
function screenMarginCall(){const P=mgPlan(),cash=mgrCash(),nav=S.nav;
 const O=[{id:'inj',b:"Apporter des fonds propres",s:`La société de gestion verse ${mm(P.inj)} dans le fonds, bloqués avec votre co-investissement jusqu'à la clôture. Le book ne bouge pas.`,c:-1,ko:P.inj>cash},
  {id:'cut',b:"Couper vous-même",s:`Vous retirez les lignes les plus gourmandes en marge, au tarif d'urgence : ${mm(P.c1)} à votre charge.`,c:-2,k:P.k1,tc:P.c1},
  {id:'pb',b:"Laisser le prime broker liquider",s:`Il coupe ${Math.round(P.f*100)} % de chaque ligne au pire prix : ${mm(P.c2)} à votre charge.`,c:-5,k:P.k2,tc:P.c2}];
 app.innerHTML=statusBar()+`<div class="evwrap fade"><div class="evcard bad">${evHead('Prime broker · appel de marge','risk')}<h3>Marge utilisée ${Math.round(P.mgu*100)} % : au-delà du seuil de ${Math.round(MGC.thr*100)} %</h3>
  <p>Le prime broker recalcule vos exigences après chaque mouvement. Il faut revenir à ${Math.round(MGC.back*100)} % de l'encours avant la prochaine séance.</p>${evTimerHTML}</div>
  <div class="choices" style="margin-top:12px">${O.map((o,i)=>`<button class="choice" data-m="${i}"${o.ko?' disabled':''}><b>${o.b}</b><span>${o.s} Confiance ${o.c}.${o.k?bkD(o.k,0,false):''}${o.ko?' <b class="neg-g">hors trésorerie</b>':''}</span></button>`).join('')}</div></div>`;
 const go=i=>{clearTimer();const o=O[i];
  if(o.id==='inj'){const x=P.inj;S.nav+=x;S.navQ0+=x;S.coinvBase=(S.coinvBase||0)+x;S.coinvIn=(S.coinvIn||0)+x;S.coinvLock=(S.coinvLock||0)+x;S.mgInj=(S.mgInj||0)+x}
  else{const r0=liveRet();S.k=o.k;const r1=liveRet();S.qEvM=(S.qEvM||0)+(r0-r1)*S.navQ0;S.pendingTC+=o.tc/S.nav;S.totalTC+=o.tc}
  S.marginCalls=(S.marginCalls||0)+1;S.everMarginCall=1;
  const g=gauge(o.c,0,`Appel de marge : ${o.b.toLowerCase()}`);S.evLog.push({t:'Appel de marge',pnl:0,m:0,lp:g.lp,rc:g.rc});
  refreshGain();stepEvents()};
 app.querySelectorAll('.choice[data-m]').forEach(b=>b.onclick=()=>go(+b.dataset.m));
 armTimer(()=>go(2),'sans réponse : le prime broker liquide')}
function screenIncident(){''')
rep("const MGC={thr:0.50,warn:0.40,cut:0.60,crisis:1.8,trough:0.55};","const MGC={thr:0.50,warn:0.40,back:0.45,cut:0.60,crisis:1.8,trough:0.55};")
# --- plus de pénalité de confiance à la validation : l'appel de marge est la conséquence
rep(" if(mgu>MGC.thr)drc-=Math.min(9,(mgu-MGC.thr)*45)*SIZE().rcNeg;\n else if(mgu>MGC.warn)drc-=1.5*SIZE().rcNeg;\n let dlp=0;if(mgu>MGC.thr)dlp-=Math.min(5,(mgu-MGC.thr)*25);"," let dlp=0;   /* lot 100 : la marge ne coûte plus en confiance à la validation ; le prime broker appelle */")
rep("Un trimestre négatif déclenchera une liquidation d'office.","Le prime broker fera un appel de marge dès le début du trimestre.")
# --- accidents : plus de faux appels de marge tirés au hasard
rep("const TAILMG=0.40;","const TAILMG=0;   /* lot 100 : les appels de marge viennent de la marge réelle */")
# --- rendement de la marge déposée : T-bills −10 pb
rep("function colYield(){const b=(S.rate||0)/4;return redOn('collat')?b*0.6:b+colY(colOpt())}",
    "function mgShare(){return (S&&S.k&&N)?Math.min(1,marginPct(S.k)):0}   /* lot 100 : part de l'encours déposée en marge */\nfunction colYield(){const b=(S.rate||0)/4,m=mgShare(),bm=Math.max(0,(S.rate||0)-0.001)/4;return redOn('collat')?b*0.6:m*bm+(1-m)*(b+colY(colOpt()))}")
rep("function colExp(){const o=colOpt();return redOn('collat')?S.rate/4*0.6:S.rate/4+colY(o)-o.p*o.l}",
    "function colExp(){const o=colOpt(),m=mgShare();return redOn('collat')?S.rate/4*0.6:m*Math.max(0,S.rate-0.001)/4+(1-m)*(S.rate/4+colY(o)-o.p*o.l)}")
rep("function colStdQ(){if(redOn('collat'))return 0;const o=colOpt();return o.l*Math.sqrt(o.p*(1-o.p))}","function colStdQ(){if(redOn('collat'))return 0;const o=colOpt();return (1-mgShare())*o.l*Math.sqrt(o.p*(1-o.p))}")
rep("const collTot=(colYield()-(cHit?cO.l:0))*(S.colBaseNav||S.nav);","const collTot=(colYield()-(cHit?cO.l*(1-mgShare()):0))*(S.colBaseNav||S.nav);")
rep("L'encours qui ne sert pas de marge est placé : taux sans risque","La marge déposée chez le prime broker rapporte le taux des T-bills moins 10 pb. Le reste de l'encours est placé : taux sans risque")
open('index.html','w',encoding='utf-8').write(s);print('ok')
