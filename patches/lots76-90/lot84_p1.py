import re
P='/home/claude/le-book/index.html';s=open(P,encoding='utf-8').read()
def rep(old,new,k=1):
    global s;n=s.count(old);assert n==k,(n,old[:100]);s=s.replace(old,new)
# 1. risque propre des marchés ×1,5 ; prime de risque des actions et des taux
rep("function normB(x){let q=x.b.reduce((a,v)=>a+v*v,0);if(q>0.92){const f=Math.sqrt(0.92/q);x.b=x.b.map(v=>v*f);q=0.92}x.idio=Math.sqrt(1-q)}",
"""/* lot 84 : le risque propre de chaque marché (hors facteurs) est relevé de moitié — même avec des indicateurs
   parfaits, une part du mouvement reste imprévisible ; il entre dans le risque ex ante comme dans les rendements */
const IDIOX=1.5;
/* prime de risque par trimestre : actions et taux rapportent en moyenne, comme dans la vraie vie */
const PREM={'Actions':0.012,'Taux':0.004};
function normB(x){let q=x.b.reduce((a,v)=>a+v*v,0);if(q>0.92){const f=Math.sqrt(0.92/q);x.b=x.b.map(v=>v*f);q=0.92}x.idio=Math.sqrt(1-q)*IDIOX}""")
rep("if(R.crowd)r-=R.crowd*S.crowd[i]*x.sigQ;","if(R.crowd)r-=R.crowd*S.crowd[i]*x.sigQ;\n   r+=PREM[x.grp]||0;")
rep("return {m:x.sigQ*z+(x.drift||0),s:x.sigQ*Math.sqrt(v)};","return {m:x.sigQ*z+(x.drift||0)+(PREM[x.grp]||0),s:x.sigQ*Math.sqrt(v)};")
# 2. accidents : probabilité accélérée, protection du contrôle qui s'efface au-delà de 30 %, pertes plus lourdes
rep("function tailP(sp,std){return Math.max(0,Math.min(1,(sp-TAIL.x0)/TAIL.w))*TAIL.p*(std?1:(TAILM[(S&&S.bud)?S.bud.risk:3]||1))}",
"""/* lot 84 : la probabilité accélère avec le risque (e + 0,8 e²), et la protection du contrôle des risques
   s'efface entre 30 et 40 % : au-delà, aucun budget ne vous couvre */
function tailMit(sp){const m=TAILM[(S&&S.bud)?S.bud.risk:3]||1;if(m>=1)return m;const fd=Math.max(0,Math.min(1,(sp-0.30)/0.10));return m+(1-m)*fd}
function tailP(sp,std){const e=Math.max(0,(sp-TAIL.x0)/TAIL.w);return Math.min(0.97,(e+0.8*e*e)*TAIL.p*(std?1:tailMit(sp)))}""")
rep("function tailL(sp){return Math.min(0.62,sp*Math.max(0.3,Math.min(1.2,(sp-0.15)/0.25)))}","function tailL(sp){return Math.min(0.80,1.5*sp*Math.max(0.3,Math.min(1.2,(sp-0.15)/0.25)))}   /* lot 84 : ×1,5 */")
rep("L=Math.min(ev.mg?0.45:0.40,","L=Math.min(ev.mg?0.60:0.55,")
rep("return [{id:'hold',f:te.good?0.3*L:1.5*L,m:0,c:te.good?-1:-8},","return [{id:'hold',f:te.good?0.5*L:1.8*L,m:0,c:te.good?-2:-10},")
rep("{id:'cut',f:0.5*L+Math.min(0.08,te.imp),m:0,c:-3},","{id:'cut',f:0.8*L+Math.min(0.08,te.imp),m:0,c:-4},")
rep("{id:'hedge',f:0.30*L,m:0.20*L,c:-2}]}","{id:'hedge',f:0.50*L,m:0.30*L,c:-3}]}")
rep("if(ev.mg)armTimer(()=>{const b=app.querySelector('.choice[data-t=\"1\"]');if(b&&!b.disabled)b.click()},'sans choix : le prime broker liquide la moitié');",
    "armTimer(()=>{const b=app.querySelector('.choice[data-t=\"1\"]');if(b&&!b.disabled)b.click()},ev.mg?'sans choix : le prime broker liquide la moitié':'sans choix : le desk coupe la moitié du book');")
rep("const TAILMG=0.45;","""TAILEV.push(   /* lot 84 : squeezes, corners, sauts */
 {t:"Short squeeze : vos ventes à découvert s'embrasent",who:"Desk · alerte rouge",sev:[0.65,1.0],
  p:"Un marché sur lequel vous êtes court prend 20 % en deux séances. Tous les vendeurs rachètent en même temps, et vous êtes parmi eux.",
  o:["Tenir la position courte","Racheter la moitié au prix du jour","Couvrir par options, au prix de la panique"]},
 {t:"Corner : un acteur contrôle le livrable",who:"Bourse · surveillance des marchés",sev:[0.6,0.95],
  p:"Un négociant détient l'essentiel du stock livrable. Les positions à l'échéance se dénouent à son prix.",
  o:["Tenir jusqu'à l'échéance","Rouler en perdant la base","Céder la moitié au négociant"]},
 {t:"Gamma squeeze : les teneurs de marché courent après le prix",who:"Desk options",sev:[0.6,0.95],
  p:"Les vendeurs d'options se couvrent dans le sens du mouvement ; chaque point de hausse en appelle un autre, contre vous.",
  o:["Laisser passer la vague","Couper la moitié dans la vague","Acheter la volatilité qui vous tue"]},
 {t:"Saut de prix à l'ouverture",who:"Fil d'actualité · 06h58",sev:[0.55,0.9],
  p:"Une annonce de nuit. Le marché ouvre avec un écart de plusieurs écarts-types : il n'y a eu aucun prix entre hier et maintenant.",
  o:["Tenir et attendre le retour","Vendre la moitié à l'ouverture","Couvrir la suite, cher"]}
);
const TAILMG=0.40;""")
# 3. rachats et confiance : pénalité accélérée au-delà du confort
rep("const RDM={lp0:0.03,","/* lot 84 : terme quadratique — le risque élevé devient brutal */\nconst RISKQ={lp:1.2,fl:2.5};\nconst RDM={lp0:0.03,")
rep("lpD.push([`Risque ex ante de ${dec(sp*100,0)} % : jugé trop élevé`,-Math.round(RISKLP.k*(sp-RISKLP.x0)/0.05)]);",
    "lpD.push([`Risque ex ante de ${dec(sp*50,1)} % : jugé trop élevé`,-Math.round(RISKLP.k*(sp-RISKLP.x0)/0.05+RISKQ.lp*((sp-RISKLP.x0)/0.05)**2)]);")
rep("const riskOut=RISKLP.fk*Math.max(0,sp-RISKLP.fl)*SIZE().flowMult;","const riskOut=(RISKLP.fk*Math.max(0,sp-RISKLP.fl)+RISKQ.fl*Math.max(0,sp-RISKLP.fl)**2)*SIZE().flowMult;")
rep("{const o=1-RISKLP.fk*Math.max(0,rivV(rv)-RISKLP.fl)*((SIZE()&&SIZE().flowMult)||1);",
    "{const ex=Math.max(0,rivV(rv)-RISKLP.fl),o=1-Math.min(0.5,(RISKLP.fk*ex+RISKQ.fl*ex*ex)*((SIZE()&&SIZE().flowMult)||1));")
# 4. co-investissement : 25 % au moins, et il entre dans l'encours du fonds
rep("const COINV=0.10;","const COINV=0.25;")
rep("const COINVS=[0.10,0.25,0.50,0.75,1.00];","const COINVS=[0.25,0.50,0.75,1.00];")
rep("S.coinvBase=coinvPct()*Math.max(0,mgrCash());S.lpQ0=S.lp;",
    "{const tg=coinvPct()*Math.max(0,mgrCash()),d=tg-(S.coinvIn||0);S.nav+=d;S.navQ0+=d;S.coinvBase=tg;S.coinvIn=tg}S.lpQ0=S.lp;   /* lot 84 : la part placée entre dans l'encours */")
rep("S.mgrCoinv=(S.mgrCoinv||0)+coinv;","S.mgrCoinv=(S.mgrCoinv||0)+coinv;S.coinvIn=(S.coinvBase||0)*(1+qTotal);")
rep("10 % au moins.</p>","25 % au moins ; la somme placée entre dans l'encours du fonds.</p>")
# 5. conviction forte : trois fois l'objectif
rep("Vous annoncez deux fois l'objectif de votre mandat, soit ${pctc(2*g)}.","Vous annoncez trois fois l'objectif de votre mandat, soit ${pctc(3*g)}.")
rep("ret:2*g,win:{lp:12,rc:12},lose:{lp:-12,rc:-12}}","ret:3*g,win:{lp:15,rc:15},lose:{lp:-15,rc:-15}}")
# 6. accès aux blocs : dire ce que veut dire la profondeur
rep("g:'plafond de position ±4 · profondeur ×1,5 · coûts d\\'","g:'plafond de position ±4 · marchés 1,5 fois plus profonds pour vous (vos gros ordres bougent moins les prix) · coûts d\\'")
# 7. lecture du flux : dire à quoi elle sert
rep("<b>Votre lecture du flux</b> — la tendance du trimestre, déjà dessinée :",
    "<b>Votre lecture du flux</b> — ces marchés ont fait la moitié de leur trimestre, et la seconde moitié suit en général la première : suivez ou non les dépêches qui les touchent en conséquence. En cours :")
# 8. concurrents : ils choisissent un risque qui sert leur rentabilité, pas un risque qui la détruit
rep(" return Math.max(0.06,Math.min(0.95*rivCapVol(rv),v*((SIZE()&&SIZE().rivVol)||1)))}",
""" const cap=0.95*rivCapVol(rv);v=Math.max(0.06,Math.min(cap,v*((SIZE()&&SIZE().rivVol)||1)));
 /* lot 84 : la moitié du chemin vers le risque qui maximise leur rentabilité attendue */
 let bv=v,by=-1e9;for(let t=0.06;t<=cap+1e-9;t+=0.02){const y=rivPt(rv,t).y;if(y>by){by=y;bv=t}}
 return Math.max(0.06,Math.min(cap,0.5*v+0.5*bv))}""")
# 9. incident opérationnel : choisir entre deux maux
rep(" const loss=uni(inc.loss[0],inc.loss[1])*sev;\n const navB=S.nav;S.nav*=(1-loss);S.qIncM-=loss*navB;\n const g=gauge(inc.lp*sev,inc.rc*sev,inc.t);\n S.incidents.push({t:inc.t,loss});S.evLog.push({t:inc.t,pnl:-loss,m:-loss*navB,lp:g.lp,rc:g.rc});",
""" const loss=uni(inc.loss[0],inc.loss[1])*sev,navB=S.nav;
 /* lot 84 : deux maux — réparer tout et payer de sa poche, ou contenir et le payer en confiance */
 const O=[{b:"Tout réparer, tout de suite",s:"Le fonds paie la facture entière, vous indemnisez les clients sur votre trésorerie ; la transparence rassure.",f:loss,m:0.6*loss,lp:inc.lp*sev*0.3,rc:inc.rc*sev*0.3},
  {b:"Contenir et communiquer plus tard",s:"Le fonds n'absorbe que la moitié. Quand l'affaire sort, la confiance le paie cher.",f:0.5*loss,m:0,lp:inc.lp*sev*2.2-4,rc:inc.rc*sev*2}];
 O.forEach(o=>o.cf=cf(o.lp,o.rc));
 app.innerHTML=statusBar()+`<div class="evwrap fade">
  <div class="evcard bad">${evHead(inc.who,'risk')}<h3>${inc.t}</h3><p>${inc.p}</p>${evTimerHTML}</div>
  ${O.map((o,i)=>{const ko=o.m*navB>mgrCash();return `<button class="choice" data-i="${i}"${ko?' disabled':''}><b>${o.b}</b><span>${o.s}<span class="stks"><span class="stk">fonds <em class="neg-g">−${mm(o.f*navB)}</em></span>${o.m?`<span class="stk">vous <em class="neg-g">−${mm(o.m*navB)}</em></span>`:''}<span class="stk">confiance <em class="${o.cf<0?'neg-g':'dim-g'}">${sd1(o.cf)}</em></span></span>${ko?' <b class="neg-g">hors trésorerie</b>':''}</span></button>`}).join('')}</div>`;
 const pickI=k=>{clearTimer();const o=O[k];S.nav*=(1-o.f);S.qIncM-=o.f*navB;if(o.m){S.mgrCosts+=o.m*navB;refreshGain()}
  const g=gauge(o.lp,o.rc,inc.t);const loss=o.f;
  S.incidents.push({t:inc.t,loss});S.evLog.push({t:inc.t,pnl:-loss,m:-loss*navB,lp:g.lp,rc:g.rc});""")
rep("""${sd1(g.lp)}</b></div>\n   <p class="note">Gravité appliquée""","""${sd1(g.lp)}</b></div>${o.m?`<div class="kv"><span>Payé par vous</span><b class="neg-g">−${mm(o.m*navB)}</b></div>`:''}\n   <p class="note">Gravité appliquée""")
rep(" document.getElementById('ok').onclick=()=>stepEvents();\n}\nfunction resolveQuarter(){",
    " document.getElementById('ok').onclick=()=>stepEvents();};\n app.querySelectorAll('.choice[data-i]').forEach(b=>b.onclick=()=>pickI(+b.dataset.i));\n armTimer(()=>pickI(1),'sans choix : vous contenez l\\'affaire');\n}\nfunction resolveQuarter(){")
open(P,'w',encoding='utf-8').write(s);print('ok')
