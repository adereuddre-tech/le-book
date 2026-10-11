import re
p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
OLD=open('patches/lot301/oldgoals.txt',encoding='utf-8').read()
# objectifs retirés : nom de concurrent figé, budgets d'avant la refonte
for nm in ["Contre le champion, deux fois","Gagner sans rien dépenser"]:
    L=[l for l in OLD.split('\n') if f'nm:"{nm}"' in l];assert len(L)==1,nm;OLD=OLD.replace(L[0]+'\n','')
OLD=OLD.replace('{nm:"Les investisseurs conquis",d:"Terminer avec la jauge investisseurs au-dessus de 80."','{nm:"Les investisseurs conquis",d:"Terminer avec la confiance au-dessus de 80."')
OLD=OLD.replace("cls:'Actions',cls:'Actions'","cls:'Actions'").replace("cls:'Exotiques',cls:'Exotiques'","cls:'Exotiques'")
# 1. la liste : les objectifs d'aujourd'hui (tous trimestres) + l'ancien catalogue + des objectifs sur les mécaniques récentes
a=s.index("const QGOALS=[");b=s.index("\n];",a)
cur=s[a+len("const QGOALS=["):b]
cur=re.sub(r"\{qn:\d,","{",cur)
cur=cur.replace(" /* — trimestre 1 : faire ses preuves — */"," /* — premiers pas (lot 210) — */").replace(" /* — trimestre 2 : confirmer — */"," /* — confirmer — */")
NEW=''' /* — mécaniques récentes (lot 301) — */
 {nm:"Le desk heureux",d:"Terminer le trimestre avec le moral du desk à 60 ou plus.",t:c=>motV()>=60,b:0.08},
 {nm:"Le desk en feu",d:"Terminer le trimestre avec le moral du desk au-dessus de 80.",t:c=>motV()>80,b:0.14},
 {nm:"Couvert et gagnant",d:"Acheter la protection contre les extrêmes et finir le trimestre positif.",t:c=>S.hedgeQ===S.q&&c.q>0,b:0.07},
 {nm:"Le parapluie ouvert",d:"Être protégé le trimestre où un événement extrême frappe.",t:c=>S.hedgeQ===S.q&&c.tail,b:0.12},
 {nm:"Sous le radar",d:"Terminer avec au moins cinq lignes sans qu'aucune ne soit visible du marché.",t:c=>c.nPos>=5&&visList(S.k).length===0,b:0.07},
 {nm:"Sans appel du comité",d:"Finir le trimestre positif sans carton jaune ni rouge en vue.",t:c=>c.q>0&&!cardWarn(),b:0.06},
 {nm:"La marge sage",d:"Battre la médiane avec une marge utilisée sous 20 % de l'encours.",t:c=>c.rel>0&&c.mgu<0.20,b:0.09},
 {nm:"L'équipe tient",d:"Traverser le trimestre sans perdre un trader au profit d'un concurrent, avec au moins trois traders.",t:c=>!/débauché|part en entraînant/.test(S.poachMsg||'')&&(S.bud.fo||0)>=3,b:0.06}
'''
s=s[:a]+"const QGOALS=["+cur.rstrip()+",\n /* — catalogue d'avant le lot 210 — */\n"+OLD.rstrip().rstrip(',')+",\n"+NEW.rstrip()+s[b:]
# 2. un objectif à chaque trimestre, sans répéter les 30 derniers
rep(""" S.usedGoals=(S.usedGoals||[]).slice(-16);""",""" S.usedGoals=(S.usedGoals||[]).slice(-30);""")
rep(""" const gav=QGOALS.filter(g=>g.qn===S.q+1&&preOk(g));   /* lot 210 : trimestres 1 et 2 seulement */
 S.goal=S.q<2&&gav.length?pick(gav):null;""",""" const gav=QGOALS.filter(g=>preOk(g)&&!S.usedGoals.includes(g.id||g.nm));   /* lot 301 : tous les trimestres, catalogue complet */
 S.goal=gav.length?pick(gav):null;""")
# 3. le montant : autour de 1 M$ (0,7 à 1,35 M$ selon la difficulté), prélevé sur l'encours comme la commission de performance
rep("function goalBon(g){return g?g.b*GOALB*S.aum0:0}","function goalBon(g){return g?(0.0005+0.005*(g.b||0.10))*S.aum0/0.1:0}   /* lot 301 : ≈ 1 M$, payé par le fonds */")
rep(" const qTotal=perfM/S.navQ0;"," let qTotal=perfM/S.navQ0;   /* lot 301 : l'objectif tenu est prélevé ensuite */")
rep("""  if(ok){S.mgrFees+=bon;S.cBon=(S.cBon||0)+bon}""",
"""  if(ok){S.mgrFees+=bon;S.cBon=(S.cBon||0)+bon;   /* lot 301 : prélevé sur l'encours, comme la commission de performance */
   const n0=S.nav,f=Math.min(0.5,bon/Math.max(1e-9,n0)),i0=S.idx;S.nav-=bon;S.idx*=(1-f);
   if(S.hwm===n0)S.hwm=S.nav;if(S.peak===n0)S.peak=S.nav;if(S.hwmIdx===i0)S.hwmIdx=S.idx;if(S.peakIdx===i0)S.peakIdx=S.idx;
   if(S.navs.length)S.navs[S.navs.length-1]=S.nav;qTotal=(1+qTotal)*(1-f)-1;S.rets[S.rets.length-1]=qTotal;
   if(S.qPnl){S.qPnl.feeM-=bon;S.qPnl.perfM-=bon}S.mgrQ.fees+=bon;S.mgrQ.goal=bon}""")
rep("""g:`${mm(bon)} de bonus sur vos gains`});""","""g:`${mm(bon)} pour vous, prélevés sur l'encours`});""")
rep("""${S.goal.d} Bonus de ${moneyB(goalBon(S.goal))} sur votre score.`]:[])""","""${S.goal.d} Bonus de ${mm(goalBon(S.goal))}, prélevé sur l'encours comme la commission de performance.`]:[])""")
rep("""${S.goal.d} Bonus de ${moneyB(goalBon(S.goal))} sur votre score.</span>""","""${S.goal.d} Bonus de ${mm(goalBon(S.goal))}, prélevé sur l'encours.</span>""")
open(p,'w',encoding='utf-8').write(s)
