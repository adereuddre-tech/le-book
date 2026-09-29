# Lot 104, E · fin de partie économique. Constat (sonde lot 101, 6 parties) : la trésorerie finit entre 4 et 36 M$,
# jamais négative, parce que budget et coûts suivent l'encours et que les gardes empêchent de dépenser au-delà de la
# caisse. Donc : budget facturé sur max(encours, encours initial) (les salaires ne baissent pas avec l'encours),
# garder son équipe n'est jamais verrouillé (seul monter exige la caisse), et la partie s'arrête après deux clôtures
# de suite en trésorerie négative (faillite de la société de gestion), ou fonds vidé (< 1 % de l'encours initial).
# FUNDMIN (40 M$) et le repli de 50 % disparaissent.
import re
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
def region(a,b,o,n,k):
    global s; i=s.index(a); j=s.index(b,i); seg=s[i:j]; c=seg.count(o); assert c==k,(a[:30],c); s=s[:i]+seg.replace(o,n)+s[j:]

rep("const FUNDMIN=0.04,DDEND=0.50;   /* lot 83 : 40 M$ */","const FUNDMIN=0.04,DDEND=0.50;   /* lot 83 : 40 M$ ; lot 104 : plus lus pour la fin de partie */\nconst FUNDEMPTY=0.01;   /* lot 104 : fonds vidé */\nfunction budNav(){return Math.max(S.nav,S.aum0||S.nav)}   /* lot 104 : salaires et loyer ne suivent pas l'encours à la baisse */")
# budget au prix fixe
region("function setOps(){","function covTxt(){","1e-4*S.nav","1e-4*budNav()",2)
region("function budRest(){","\n","1e-4*S.nav","1e-4*budNav()",1)
region("function screenBudget(){","function drawBuds(){","1e-4*S.nav","1e-4*budNav()",1)
region("function drawBuds(){","app.querySelectorAll('.lvl.tm')","1e-4*S.nav","1e-4*budNav()",9)
# garder son équipe n'est jamais verrouillé ; plus de rétrogradation automatique
rep("const ok=(id,i)=>(i===0||budgetBpIf(id,i)*1e-4*budNav()<=purse)","const ok=(id,i)=>(i===0||(S.budPrev&&i<=S.budPrev[id])||budgetBpIf(id,i)*1e-4*budNav()<=purse)")
rep("  for(let g=0;g<40&&!fits();g++){","  for(let g=0;g<40&&!fits()&&!S.budPrev;g++){")
# fin de partie
rep("if(S.nav<FUNDMIN)S.over='nav';else if(1-S.idx/Math.max(S.idx,S.peakIdx||1)>=DDEND-1e-9)S.over='dd';",
    "S.cashNeg=mgrCash()<-1e-9?(S.cashNeg||0)+1:0;if(S.cashNeg>=2)S.over='cash';else if(extNav()<FUNDEMPTY*S.aum0)S.over='nav';   /* lot 104 */")
rep('''  verdict=S.over==='dd'?"Moitié perdue":"L'encours n'y est plus";vtxt=S.over==='dd'?''',
    '''  verdict=S.over==='cash'?"Dépôt de bilan":S.over==='dd'?"Moitié perdue":"L'encours n'y est plus";vtxt=S.over==='cash'?`Deuxième clôture de suite en trésorerie négative, au trimestre ${S.q} : les commissions ne paient plus l'équipe, le loyer et les ordres. La société de gestion dépose le bilan ; le conseil confie le fonds à une autre maison.`:S.over==='nav'?`Au trimestre ${S.q}, vos investisseurs sont partis : il ne reste presque plus rien à gérer.`:S.over==='dd'?''')
# débriefing : l'alerte
rep(''' {const I=invs().filter(v=>v.ntc>0);''',''' if(!S.over&&mgrCash()<-1e-9)warn.push(`🧾 <b>Trésorerie négative : −${mm(-mgrCash())}.</b> Encore une clôture dans le rouge et la société de gestion dépose le bilan. Les salaires sont facturés sur ${moneyB(budNav())} tant que l'encours reste sous son niveau de départ : alléger l'équipe coûte le versement du bonus aux partants.`);
 {const I=invs().filter(v=>v.ntc>0);''')
# textes
rep("['Seuil de fermeture',moneyB(FUNDMIN)],","['Fin de partie','deux clôtures de suite en trésorerie négative'],")
rep(" Le fonds ferme sous <em>${moneyB(FUNDMIN)}</em> d'encours (rachats compris), ou dès que la perte depuis le plus haut atteint <em>${Math.round(DDEND*100)} %</em>.</p>",
    " Le fonds ne ferme plus sur un seuil d'encours : c'est votre société de gestion qui tient ou non. Deux clôtures de suite en trésorerie négative, et c'est le dépôt de bilan.</p>")
open('index.html','w',encoding='utf-8').write(s);print('lot104 p1 ok')
