import sys
P='/home/claude/le-book/index.html';s=open(P,encoding='utf-8').read()
def rep(old,new,k=1):
    global s;n=s.count(old);assert n==k,(n,old[:80]);s=s.replace(old,new)

# 1. quadrillage du ruban : paliers « ronds » en gain, espacés d'au moins H/7 pixels, du zéro vers l'extérieur
rep("""const va=Math.exp(lo),vb=Math.exp(hi);let stp=10;for(const s of [10,20,50,100,200])if(Math.floor(vb/s)-Math.ceil(va/s)+1<=7){stp=s;break}
 let grid='';for(let L=Math.ceil(va/stp)*stp;L<=vb;L+=stp){if(L<=0||L===100)continue;const yy=y(L);
  grid+=""","""const va=Math.exp(lo),vb=Math.exp(hi);
 /* lot 76 : paliers ronds, les plus proches du zéro d'abord, jamais à moins de H/7 pixels l'un de l'autre */
 const TG=[5,10,20,30,50,75,100,150,200,300,500,750,1000,1500,2000,3000,5000,10000].flatMap(g=>g<100?[g,-g]:[g]);
 let grid='';const gys=[y0];for(const g of TG){const L=100+g;if(L<va||L>vb)continue;const yy=y(L);
  if(gys.some(v=>Math.abs(v-yy)<Math.max(11,H/7)))continue;gys.push(yy);
  grid+=""")
rep("""fill="#5B6E8C" font-family="var(--mono)">${L>100?'+':'−'}${Math.abs(L-100)} %</text>`}""",
    """fill="#5B6E8C" font-family="var(--mono)">${g>0?'+':'−'}${Math.abs(g).toLocaleString('fr-FR')} %</text>`}""")

# 2. confiance à zéro en cours de trimestre : carton jaune immédiat
rep(""" S.lp=Math.max(0,Math.min(100,S.lp+d));S.rc=Math.max(0,Math.min(100,S.rc+drc));
 if(d||Math.abs(drc)>=0.05){""",""" S.lp=Math.max(0,Math.min(100,S.lp+d));S.rc=Math.max(0,Math.min(100,S.rc+drc));
 if(lp0>0&&S.lp<=0&&['budget','book','events'].includes(S.phase)&&S.midY!==S.q)midYellow();
 if(d||Math.abs(drc)>=0.05){""")
rep("function gauge(dlp,drc,why){","""/* lot 76 : confiance à zéro en cours de trimestre = carton jaune sur-le-champ. Il est compté tout de suite
   (la tuile passe au jaune) et consigné à la clôture ; un deuxième jaune y devient rouge. */
function midYellow(){const C=S.cards=S.cards||{y:0,r:0,clean:0,log:[]};S.midY=S.q;C.y++;C.clean=0;
 setTimeout(()=>toast(`🟨 <b>Carton jaune du comité</b> — la confiance des investisseurs est tombée à zéro.${C.y>=2?' Deuxième jaune : le rouge tombera à la clôture.':''}`),900)}
function gauge(dlp,drc,why){""")
rep("""  S.qCard=null;
  if(!red&&why.length){C.y++;""","""  if(S.midY===S.q){why.unshift('confiance tombée à zéro en cours de trimestre');C.y=Math.max(0,C.y-1)}
  else if(S.lp<=0)why.unshift('confiance des investisseurs à zéro');
  S.qCard=null;
  if(!red&&why.length){C.y++;""")

# 3. objectifs conditionnés au trimestre précédent
rep("""t:c=>c.q>0&&c.prevQ>0,b:0.07}""","""t:c=>c.q>0&&c.prevQ>0,b:0.07,pre:'gain'}""")
rep("""t:c=>c.q>0&&c.prevQ<0,b:0.08}""","""t:c=>c.q>0&&c.prevQ<0,b:0.08,pre:'loss'}""")
rep("""t:c=>c.prevQ<0&&c.dLp>0,b:0.08}""","""t:c=>c.prevQ<0&&c.dLp>0,b:0.08,pre:'loss'}""")
rep(""" const gav=QGOALS.filter(g=>!S.usedGoals.includes(g.nm));
 S.goal=pick(gav.length?gav:QGOALS);""",""" /* lot 76 : « Le rebond » et ses cousins ne sortent qu'après un trimestre du bon signe */
 const lastQ=(S.rets&&S.rets.length)?S.rets[S.rets.length-1]:0,preOk=g=>!g.pre||(g.pre==='loss'?lastQ<0:lastQ>0);
 const gav=QGOALS.filter(g=>!S.usedGoals.includes(g.nm)&&preOk(g));
 S.goal=pick(gav.length?gav:QGOALS.filter(preOk));""")

# 4. accidents : appels de marge, plus fréquents et plus lourds
rep("""{t:"Votre prime broker relève les marges de 40 % dans la nuit",""","""{mg:1,t:"Votre prime broker relève les marges de 40 % dans la nuit",""")
rep("""{t:"La chambre de compensation exige un dépôt exceptionnel",""","""{mg:1,t:"La chambre de compensation exige un dépôt exceptionnel",""")
rep("""const TAIL={x0:0.25,w:0.35,p:0.50},""","""/* lot 76 : appels de marge (mg) — 45 % des accidents, gravité plus forte, perte plafonnée à 45 % au lieu de 40 % */
TAILEV.push(
 {mg:1,t:"Appel de marge à 7 heures : le cash avant midi",who:"Prime broker · appel de marge",sev:[0.65,0.95],
  p:"Une nuit de volatilité a gonflé vos marges initiales. Le prime broker veut l'argent avant la cloche de midi ; sinon, il se sert lui-même, au prix qu'il trouvera.",
  o:["Contester le calcul et tenir le book","Laisser le prime broker liquider la moitié","Payer sur une ligne de crédit à taux punitif"]},
 {mg:1,t:"La chambre relève les marges en séance, deux fois",who:"Chambre de compensation · avis d'urgence",sev:[0.6,0.9],
  p:"Première hausse à 10 heures, deuxième à 15 heures. Chaque fonds levé vend ce qu'il peut pour payer, et c'est justement ce que vous détenez.",
  o:["Tenir et payer ce qui sera demandé","Réduire de moitié au prix du jour","Emprunter le dépôt au prix que la banque fixe"]},
 {mg:1,t:"Spirale d'appels de marge : les autres vendent ce que vous tenez",who:"Desk · alerte rouge",sev:[0.7,1.0],
  p:"Un fonds plus gros que vous est liquidé par son prime broker. Ses positions sont les vôtres ; chacune de ses ventes déclenche un nouvel appel chez vous.",
  o:["Tenir jusqu'à la fin de la liquidation","Vendre avant la prochaine vague","Payer la marge et couvrir le reste, au prix du vendeur"]},
 {mg:1,t:"Le prime broker change sa méthode de calcul de marge",who:"Prime broker · courrier recommandé",sev:[0.55,0.9],
  p:"Nouveau modèle de risque, effet immédiat : votre marge requise double. La lettre est polie, le délai est de vingt-quatre heures.",
  o:["Négocier un délai et tenir","Réduire de moitié pour rentrer dans le modèle","Poster du collatéral emprunté hors de prix"]},
 {mg:1,t:"Décote relevée sur tout votre collatéral",who:"Trésorerie · alerte",sev:[0.6,0.9],
  p:"Le prime broker applique une décote de 25 % sur les titres que vous avez déposés. Du jour au lendemain, il manque de quoi couvrir la marge.",
  o:["Contester la décote et tenir","Vendre la moitié du book pour dégager du cash","Remplacer le collatéral à crédit, au taux de la banque"]}
);
const TAILMG=0.45;
/* gravité moyenne relative à celle d'avant le lot 76 (0,62 calé sur 0,581 de sévérité médiane) */
const TAILSEV=(()=>{const m=a=>a.reduce((s,e)=>s+(e.sev[0]+e.sev[1])/2,0)/Math.max(1,a.length);
 return 0.62/0.5806*(TAILMG*m(TAILEV.filter(e=>e.mg))+(1-TAILMG)*m(TAILEV.filter(e=>!e.mg)))})();
const TAIL={x0:0.25,w:0.35,p:0.60},""")
rep("0.62*tailL(RS.total","TAILSEV*tailL(RS.total",2)
rep("0.62*tailL(sp","TAILSEV*tailL(sp",2)
rep(""" const i=Math.floor(u()*TAILEV.length),ev=TAILEV[i],L=Math.min(0.40,(ev.sev[0]+(ev.sev[1]-ev.sev[0])*u())*tailL(sp)),good=u()<0.5;""",
""" const pool=TAILEV.map((e,j)=>j).filter(j=>!!TAILEV[j].mg===(u()<TAILMG)),i=pool[Math.floor(u()*pool.length)],ev=TAILEV[i],
  L=Math.min(ev.mg?0.45:0.40,(ev.sev[0]+(ev.sev[1]-ev.sev[0])*u())*tailL(sp)),good=u()<0.5;""")
rep("""<p class="note">Accident de levier : votre book tourne à""","""<p class="note">${ev.mg?'Appel de marge':'Accident de levier'} : votre book tourne à""")

# 5. collatéral : deux crans de plus, résultat détaillé à la clôture
rep(""" {id:'abs',nm:'Titrisations',ico:'🧨',y:0.018,p:0.20,l:0.06,d:"Des tranches de prêts titrisés. Le rendement paie un risque que tout le monde connaît."},
];""",""" {id:'abs',nm:'Titrisations',ico:'🧨',y:0.018,p:0.20,l:0.06,d:"Des tranches de prêts titrisés. Le rendement paie un risque que tout le monde connaît."},
 {id:'rehyp',nm:'Titres réhypothéqués',ico:'⛓️',y:0.030,p:0.25,l:0.09,d:"Vos titres en gage sont reprêtés, puis reprêtés encore. Chaque maillon paie ; si l'un casse, vous êtes au bout de la chaîne."},
 {id:'junk',nm:'Junk bonds',ico:'☠️',y:0.045,p:0.30,l:0.12,d:"Des obligations notées sous la catégorie investissement. Le coupon est superbe tant que personne ne fait défaut."},
];""")
rep(""" S.colRes={nm:redOn('collat')?'Collatéral renforcé':cO.nm,x:collTot/(S.colBaseNav||S.nav)-S.rate/4,hit:cHit,l:cO.l,m:collTot-S.rate/4*(S.colBaseNav||S.nav),show:redOn('collat')||cO.id!=='tres'};""",
""" {const bN=S.colBaseNav||S.nav,loss=cHit?cO.l*bN:0;
  S.colRes={nm:redOn('collat')?'Collatéral renforcé':cO.nm,lock:redOn('collat'),x:collTot/bN-S.rate/4,hit:cHit,l:cO.l,p:cO.p,m:collTot-S.rate/4*bN,
   sur:collTot-S.rate/4*bN+loss,loss,show:redOn('collat')||cO.id!=='tres'}}""")
rep("""if(S.colRes&&S.colRes.hit)warn.push(`💥 <b>Le placement du collatéral a fait défaut</b> — ${S.colRes.nm} : −${dec(S.colRes.l*100,1)} % de l'encours, surcroît de rendement compris ${sgn(S.colRes.x,1)} sur le trimestre.`);""",
"""{const c=S.colRes;if(c&&c.show)warn.push(c.lock?`Collatéral renforcé : rémunéré à 60 % du taux, ${mn(c.m)} par rapport aux bons du Trésor.`
  :c.hit?`💥 <b>Le placement du collatéral a fait défaut</b> — ${c.nm} : surcroît de rendement ${mn(c.sur)}, défaut <b class="neg-g">−${mm(c.loss)}</b> (−${dec(c.l*100,1)} % de l'encours), soit ${mn(c.m)} au total par rapport aux bons du Trésor.`
  :`Collatéral — ${c.nm} : pas de défaut (${Math.round(c.p*100)} % de risque), surcroît de rendement ${mn(c.sur)} par rapport aux bons du Trésor.`)}""")
rep("""<span class="an" style="color:var(--dimmer)">dont ${S.colRes.nm.toLowerCase()}${S.colRes.hit?' · défaut':''}</span><span class="av">${inU(S.colRes.m,UQ)}</span></div>`:''}""",
"""<span class="an" style="color:var(--dimmer)">dont ${S.colRes.lock?'collatéral renforcé':'surcroît · '+S.colRes.nm.toLowerCase()}</span><span class="av">${inU(S.colRes.lock?S.colRes.m:S.colRes.sur,UQ)}</span></div>${S.colRes.hit?`
   <div class="attr"><span class="an" style="color:var(--dimmer)">dont défaut du placement</span><span class="av">${inU(-S.colRes.loss,UQ)}</span></div>`:''}`:''}""")

# 6. les lignes d'alerte du débriefing gardent leur texte en un seul bloc (flex coupait aux <b>)
rep("""<div class="flag" style="margin-top:12px">${t}</div>""","""<div class="flag" style="margin-top:12px"><span>${t}</span></div>""")
open(P,'w',encoding='utf-8').write(s);print('ok')
