# Lot 108 : traders et bonus d'équipe. Le budget salle de marché ne donne plus que la moitié de sa baisse des coûts
# d'exécution (coûts et impact) ; la motivation du desk donne le reste. Taux de bonus permanent à 5 crans (0 à 20 % de la
# commission de performance, versé à l'ouverture). La motivation (0 à 1) tend vers taux/20 % (moitié du chemin par
# trimestre), prend +0,10 par cran de hausse et −0,18 par cran de baisse. Débauchage : 50 % × (1 − 0,8 × motivation),
# ×1,6 le trimestre d'une baisse de taux.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("const BONUS=[0,0.05,0.10],BONM=[1,0.5,0.2],GROGNE=1.5,POACHP=0.5;",
    "const BONUS=[0,0.05,0.10,0.15,0.20],POACHP=0.5,MOT={m0:0.30,k:0.5,up:0.10,dn:0.18,poach:0.8,cut:1.6,i0:2};\n"
    "function motNow(){return S&&S.mot!=null?S.mot:MOT.m0}\n"
    "function execMot(i){const e=EXECM[i==null?S.bud.exec:i];return e<1?1-(1-e)*(0.5+0.5*motNow()):e}   /* lot 108 : la motivation donne la moitié du gain */\n"
    "function poachNow(){return Math.min(0.95,POACHP*(1-MOT.poach*motNow())*(S.bonCutQ===S.q?MOT.cut:1))}")
i=s.index("function bonTxt(){");j=s.index("function payBonus(){",i)
s=s[:i]+'''function bonTxt(){return `<br>Motivation du desk : <b>${Math.round(motNow()*100)} %</b> · coûts ×${dec(execMot(),2)} au lieu de ×${dec(EXECM[S.bud.exec],2)} · risque de débauchage ${Math.round(poachNow()*100)} % ce trimestre${S.qBonT>0?` · bonus versé ${mm(S.qBonT)}`:''}${S.bonCutQ===S.q?' · <span class="neg-g">baisse du taux mal vécue</span>':''}.`}
'''+s[j:]
i=s.index("function payBonus(){");j=s.index("function covered(g){",i)
s=s[:i]+'''function payBonus(){S.qBonT=0;S.bonWhoQ=null;if(S.q<1)return;const perf=(S.mgrQ&&S.mgrQ.perf)||0;
 if(S.bonI==null)S.bonI=MOT.i0;const i=S.bonI,p=S.bonPrev==null?MOT.i0:S.bonPrev,d=i-p;
 const amt=Math.min(BONUS[i]*Math.max(0,perf),Math.max(0,mgrCash()));
 if(amt>0){S.mgrCosts+=amt;S.cBonT=(S.cBonT||0)+amt;S.qBonT=amt}
 const tg=perf>0?BONUS[i]/0.20:0;let m=motNow();m+=MOT.k*(tg-m)+(d>0?MOT.up*d:MOT.dn*d);S.mot=Math.max(0,Math.min(1,m));
 if(d<0)S.bonCutQ=S.q;S.bonPrev=i}
'''+s[j:]
rep("const pP=Math.min(0.95,Math.max(0,(POACHP+0.5*(S.poachBoost||0))*(S.bonMultQ||1)))","const pP=Math.min(0.95,Math.max(0,poachNow()+0.5*(S.poachBoost||0)))")
rep("return pf>0?Math.min(BONUS[S.bonI||0]*pf,Math.max(0,mgrCash())):0}","return pf>0?Math.min(BONUS[S.bonI==null?MOT.i0:S.bonI]*pf,Math.max(0,mgrCash())):0}")
# coûts : EXECM du cran × motivation
rep("let m=EXECM[S.bud.exec]*desk.mult(x)","let m=execMot()*desk.mult(x)")
rep("×${dec((EXECM[S.bud.exec]*DESK().mult(INSTR[0])","×${dec((execMot()*DESK().mult(INSTR[0])")
rep("const mult=EXECM[S.bud.exec]*S.liq*","const mult=execMot()*S.liq*")
rep("budget desk ×${dec(EXECM[S.bud.exec],2)}","budget desk ×${dec(execMot(),2)} (motivation ${Math.round(motNow()*100)} %)")
# débriefing : le taux est un réglage permanent
i=s.index(" const bnSel=");j=s.index(" const gtSel=",i)
s=s[:i]+''' const bnSel=(S.over||S.q>=QT())?'':(()=>{const pf=Math.max(0,(S.mgrQ&&S.mgrQ.perf)||0),cur=S.bonI==null?MOT.i0:S.bonI,prev=S.bonPrev==null?MOT.i0:S.bonPrev;
  const proj=i=>{const d=i-prev,tg=pf>0?BONUS[i]/0.20:0;let m=motNow();m+=MOT.k*(tg-m)+(d>0?MOT.up*d:MOT.dn*d);m=Math.max(0,Math.min(1,m));return {m,p:Math.min(0.95,POACHP*(1-MOT.poach*m)*(d<0?MOT.cut:1))}};
  return `<div class="block"><div class="blockhead"><h2>Taux de bonus d'équipe</h2><span class="hint">versé à l'ouverture</span></div>
  <p class="note" style="margin-top:0">Une part de votre commission de performance${pf>0?` (${mm(pf)} ce trimestre)`:' — aucune ce trimestre : rien ne sera versé, et la motivation retombe'}. La motivation du desk (${Math.round(motNow()*100)} % aujourd'hui) règle la moitié de la baisse des coûts d'exécution que paie votre budget salle de marché, et le risque de débauchage. Elle suit le taux, gagne à chaque hausse et perd davantage à chaque baisse.</p>
  <div class="cisel">${BONUS.map((p,i)=>{const o=proj(i);return `<button class="bnp${i===cur?' on':''}" data-i="${i}">${Math.round(p*100)} %<br><small>${mm(p*pf)} · motiv. ${Math.round(o.m*100)} % · débauche ${Math.round(o.p*100)} %</small></button>`}).join('')}</div></div>`})();
'''+s[j:]
open('index.html','w',encoding='utf-8').write(s);print('lot108 p1 ok')
