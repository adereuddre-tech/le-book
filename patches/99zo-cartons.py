# -*- coding: utf-8 -*-
"""Lot 53 — la confiance, ce sont les investisseurs ; le comité donne des cartons.

Décision d'Antoine (option b). Deux jauges cachées (investisseurs, comité), fondues dans une
confiance composite avec des seuils différents pour chacune : c'était ce qui embrouillait.

  - La confiance affichée = la jauge des investisseurs, seule. Les rachats de confiance partent
    sous 20, comme avant ; le rachat « comité » et la réduction de mandat sous 13 disparaissent.
  - Le comité sanctionne des règles, à la clôture, par des cartons :
      rouge  — risque ex-ante au double de la cible ; perte au-delà de 2,2 σ ex-ante ; appel de marge ;
      jaune  — volatilité hors de la bande ; plus de 75 % du risque sur un seul facteur ; book vide ;
               griefs accumulés dans le trimestre (le comité a perdu 25 points de patience ou plus).
    Deux jaunes font un rouge. Un rouge : mandat réduit à ±3 pendant le trimestre suivant,
    5 % de l'encours retiré par les clients qui lisent le rapport, investisseurs −6 ; l'ardoise
    est effacée. Quatre trimestres propres d'affilée retirent un jaune.
    La patience du comité (`S.rc`) continue de réagir à tout ce qui la touchait — dépêches,
    anecdotes, budget de contrôle — mais elle ne se lit plus qu'à travers les cartons.
  - Les effets de jauge affichés disent « confiance ±x » (investisseurs) et, le cas échéant,
    « ⚖️ ±y » (ce que le comité note). La barre d'état montre les cartons en cours.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
def between(a,b):
    assert e.s.count(a)==1,'debut ambigu %r'%a[:60]
    i=e.s.index(a); j=e.s.index(b,i); return e.s[i:j]
# ── une seule confiance ────────────────────────────────────────────────────────
e.rep("function conf(){return 0.6*Math.min(S.lp,S.rc)+0.4*(S.lp+S.rc)/2}","function conf(){return S.lp}   /* lot 53 : la confiance, ce sont les investisseurs */")
e.rep("gArrow(0.6*Math.min(S.lastG.lp0,S.lastG.rc0)+0.4*(S.lastG.lp0+S.lastG.rc0)/2,conf())","gArrow(S.lastG.lp0,conf())")
e.rep("nc=0.6*Math.min(nl,nr)+0.4*(nl+nr)/2,d=nc-conf();","nc=nl,d=nc-conf();")
e.rep(" const c0=0.6*Math.min(l0,r0)+0.4*(l0+r0)/2;"," const c0=l0;")
e.rep(" const d=0.6*Math.min(l1,r1)+0.4*(l1+r1)/2-c0;\n if(Math.abs(d)<0.05&&opt!=='always')return '';",
      " const d=l1-c0,dr=r1-r0;\n if(Math.abs(d)<0.05&&Math.abs(dr)<0.5&&opt!=='always')return '';")
e.rep("""return `<span class="${cls(d)}"${who.length?` title="${who.join(', ')}"`:''}>confiance ${sd1(d)}</span>`;""",
      """return `<span class="${cls(d)}"${who.length?` title="${who.join(', ')}"`:''}>${Math.abs(d)>=0.05||opt==='always'?`confiance ${sd1(d)}`:''}${Math.abs(dr)>=0.5?`${Math.abs(d)>=0.05?' · ':''}<span class="${cls(dr)}">⚖️ ${sd1(dr)}</span>`:''}</span>`;""")
# ── fin des sanctions de jauge du comité, place aux cartons ───────────────────
e.rep(" if(S.rc<=20)redeem('comité',0.05+0.006*(20-S.rc));\n","")
e.rep(" if(S.rc<=13&&S.maxk>3){S.maxk=3;S.k=S.k.map(v=>Math.max(-3,Math.min(3,v)));S.qLog.push('mandat')}",
""" /* ── le comité des risques : cartons ── */
 {const C=S.cards=S.cards||{y:0,r:0,clean:0,log:[]},why=[];let red=null;
  const dev=Math.abs(sp-S.tgt)/Math.max(1e-9,S.tgt),bnd=bandNow();
  if(rsx>2)red=`risque ex-ante à ${dec(rsx,1)} fois la cible`;
  else if(sp>1e-6&&gross<-2.2*sp/2)red='perte au-delà de 2,2 σ ex-ante';
  else if(S.marginCall)red='appel de marge';
  if(sp<0.02)why.push('book vide');
  else{const spV=S.kVal?pvol(weights(S.kVal)):sp;   /* la bande juge le book validé ; les réactions aux dépêches relèvent du rouge au double de la cible */
   if(spV>S.tgt*(1+bnd))why.push(`book validé à ${pct(spV)} de volatilité, au-dessus de la bande (${pct(S.tgt,0)} +${(bnd*100).toFixed(0)} %)`)}
  if(sp>=0.02&&fmax>0.75)why.push(`${(fmax*100).toFixed(0)} % du risque sur un seul facteur`);
  if(S.gSnap&&S.rc-S.gSnap.rc<=-25)why.push('griefs accumulés dans le trimestre');
  S.qCard=null;
  if(!red&&why.length){C.y++;C.clean=0;S.qCard={c:'jaune',why:why[0]};C.log.push({q:S.q,c:'jaune',why:why[0]});
   if(C.y>=2)red='deuxième carton jaune'}
  else if(!red){C.clean++;if(C.clean>=4&&C.y>0){C.y--;C.clean=0}}
  if(red){C.r++;C.y=0;C.clean=0;S.qCard={c:'rouge',why:red};C.log.push({q:S.q,c:'rouge',why:red});
   S.redNext=true;const out=0.05*S.nav;S.nav-=out;S.flows-=out;S.qFlow=(S.qFlow||0)-out;S.lp=Math.max(0,S.lp-6);S.rc=Math.max(S.rc,60)}
  else if(S.qCard)S.lp=Math.max(0,S.lp-2);
 }""")
# mandat réduit pendant le trimestre qui suit un rouge
e.rep(" S.gSnap={lp:S.lp,rc:S.rc,k:[...S.k],"," if(S.redNext){S.maxk=3;S.redNext=false;S.redOn=true}else if(S.redOn){S.maxk=5;S.redOn=false}\n S.gSnap={lp:S.lp,rc:S.rc,k:[...S.k],")
# débriefing : le carton du trimestre
OLD=' if(S.rc<24&&!S.over)warn.push("Le comité des risques a inscrit votre book à l'+"'ordre du jour du conseil.\");"
e.rep(OLD," if(S.qCard)warn.push(S.qCard.c==='rouge'?`🟥 <b>Carton rouge du comité</b> — ${S.qCard.why}. Mandat réduit à ±3 unités au prochain trimestre, 5 % de l'encours retiré, confiance −6.`:`🟨 <b>Carton jaune du comité</b> — ${S.qCard.why}. Confiance −2 ; au deuxième, c'est le rouge.`);")
# barre d'état : cartons en cours
e.rep("<span><i>Confiance des investisseurs</i>","<span><i>Confiance des investisseurs${S.cards&&(S.cards.y||S.redOn)?` <span class=\"cardb\">${S.redOn?'🟥 ±3':'🟨'.repeat(S.cards.y)}</span>`:''}</i>")
e.rep(".lvls{display:grid;",".rules2{margin:8px 0 0 18px;font-size:13.5px;line-height:1.5;color:var(--dim)}.rules2 li{margin-bottom:5px}\n.cardb{font-style:normal;margin-left:4px;font-size:11px}\n.lvls{display:grid;")
# pop-up de la confiance
old=between("} else if(id==='lp'){","} else if(id[0]==='f'){")
e.rep(old,"""} else if(id==='lp'){
  const dl=S.lpD,row=x=>[x[0],`<span class="${cls(x[1])}">${x[1]>=0?'+':'−'}${Math.abs(x[1]).toFixed(1)}</span>`];
  const C=S.cards||{y:0,r:0,log:[]};
  openModal('Confiance des investisseurs',`<p>La confiance, ce sont vos investisseurs : ils suivent la performance nette, les plus hauts historiques, la comparaison avec les trois concurrents, et se détournent avec les pertes, les replis, les incidents. Sous <em>20</em>, des rachats partent à chaque clôture.</p>
   ${tbl([['Confiance',`<b>${Math.round(conf())}</b>`],['Cartons jaunes en cours',C.y?'🟨'.repeat(C.y):'aucun'],['Mandat',S.redOn?'réduit à ±3 ce trimestre (carton rouge)':'±5 unités']])}
   <p style="margin-top:10px"><b>Le comité des risques</b> ne tient pas de jauge : il applique des règles et sort des cartons à la clôture.</p>
   <ul class="rules2"><li>🟥 <b>Rouge</b> : risque au double de la cible, perte au-delà de 2,2 σ, appel de marge, ou deuxième jaune.</li><li>🟨 <b>Jaune</b> : book validé au-dessus de la bande de volatilité, plus de 75 % du risque sur un facteur, book vide, griefs accumulés.</li><li>Un rouge coûte le mandat réduit à ±3 au trimestre suivant, 5 % de l\'encours et 6 points de confiance.</li><li>Quatre trimestres propres d\'affilée retirent un jaune.</li></ul>
   <p class="note" style="margin-top:8px">Dans les dépêches et les anecdotes, « ⚖️ −3 » signale ce que le comité note : trop de griefs dans un trimestre valent un jaune.</p>
   ${dl?tbl(dl.map(row),['Investisseurs · dernier trimestre','Δ']):''}
   ${C.log.length?tbl(C.log.slice(-4).map(l=>[`T${l.q}`,`${l.c==='rouge'?'🟥':'🟨'} ${l.why}`]),['Derniers cartons','']):''}`);
 """)
# le desk du flux visait 135 % de la cible : au-delà de la bande du comité (±25 %), donc un jaune
# à chaque trimestre. Il vise désormais 120 %, dans la bande, comme au lot S.
e.rep("modelScale:1.35","modelScale:1.20")
e.rep("votre desk vise 135 % de la vol cible : plus de rendement, plus de secousses","votre desk vise 120 % de la vol cible : plus de rendement, plus de secousses")
e.rep("function commitOrders(){\n let tot=0;","function commitOrders(){\n S.kVal=[...S.k];   /* le book que le comité juge contre sa bande */\n let tot=0;")
e.done("lot 53 — confiance = investisseurs, comite en cartons")
