# Lot 113 : progression entre difficultés et styles. Sonde : au premier trimestre, commission 0,5 M$, budget 0,3 M$,
# ordres d'un book complet 0,2 à 0,5 M$ — la faillite du premier trimestre (≈ 12 % des parties) ne dépendait pas de la
# difficulté. Capital de départ de la société de gestion selon la difficulté ; coût de l'équipe selon la difficulté ;
# coûts d'exécution du quant ×0,80 (×0,92 mesuré d'abord, quant encore le moins solide) et du fondamental ×1,12.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("lp0:8,flowMult:0.75,flowIn:0.60,goalMult:1}","lp0:8,flowMult:0.75,flowIn:0.60,goalMult:1,costM:0.85,seed:0.0006}")
rep("lp0:0,flowMult:1,goalMult:1}","lp0:0,flowMult:1,goalMult:1,costM:1,seed:0.0003}")
rep("lp0:-8,flowMult:1.15,flowIn:1.60,goalMult:1}","lp0:-8,flowMult:1.15,flowIn:1.60,goalMult:1,costM:1.20,seed:0}")
rep("ef:[[\"g\",\"concurrents moins adroits\"]","ef:[[\"g\",\"capital de départ de la société de gestion : 0,6 M$ ; équipe 15 % moins chère\"],[\"g\",\"concurrents moins adroits\"]")
rep("ef:[[\"g\",\"commission de performance : 20 %\"]","ef:[[\"g\",\"commission de performance : 20 %\"],[\"g\",\"capital de départ de la société de gestion : 0,3 M$\"]")
rep("ef:[[\"g\",\"commission de performance : 25 %\"],","ef:[[\"g\",\"commission de performance : 25 %\"],[\"b\",\"aucun capital de départ ; équipe 20 % plus chère\"],")
rep("function budNav(){return Math.max(S.nav,S.aum0||S.nav)}","function budNav(){return Math.max(S.nav,S.aum0||S.nav)*((SIZE()&&SIZE().costM)||1)}")
rep("evLog:[]};\n planQuarter();\n}","evLog:[]};\n S.mgrSeed=SIZE().seed||0;S.mgrFees+=S.mgrSeed;   /* lot 113 : capital de départ de la société de gestion */\n planQuarter();\n}")
rep("sigBonus:0,capture:0.50,tcMult:1.0,","sigBonus:0,capture:0.50,tcMult:0.80,")
rep("sigBonus:5,capture:0.60,tcMult:1.08,","sigBonus:5,capture:0.60,tcMult:1.12,")
open('index.html','w',encoding='utf-8').write(s);print('lot113 p1 ok')
s=open('index.html',encoding='utf-8').read()
rep("coûts de transaction +8 %","coûts de transaction +12 %")
rep("['b',\"aucune intuition","['g',\"coûts de transaction −20 % : le modèle exécute sans état d'âme\"],['b',\"aucune intuition")
open('index.html','w',encoding='utf-8').write(s);print('lot113 p1b ok')
