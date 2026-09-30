# Lot 120 : repli demandé par Antoine — capital de départ selon le style ET la difficulté. Mesure lot 119 (270 parties) :
# survie quant 66 %, fondamental 67 %, flux 68 % : les pouvoirs ne classent pas les styles. Capital = difficulté + style :
# difficulté 0,45 / 0,15 / 0 M$ ; style quant +0,40, fondamental +0,15, flux 0.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("goalMult:1,costM:0.85,seed:0.0006}","goalMult:1,costM:0.85,seed:0.00045}")
rep("goalMult:1,costM:1,seed:0.0003}","goalMult:1,costM:1,seed:0.00015}")
rep(" S.mgrSeed=SIZE().seed||0;"," S.mgrSeed=(SIZE().seed||0)+({syst:0.0004,fonda:0.00015,flux:0}[S.prof]||0);   /* lot 120 : difficulté + style */")
rep("[\"g\",\"capital de départ de la société de gestion : 0,6 M$ ; équipe 15 % moins chère\"]","[\"g\",\"capital de départ de la société de gestion : 0,45 M$ (plus le bonus de votre style) ; équipe 15 % moins chère\"]")
rep("[\"g\",\"capital de départ de la société de gestion : 0,3 M$\"]","[\"g\",\"capital de départ de la société de gestion : 0,15 M$ (plus le bonus de votre style)\"]")
rep("[\"b\",\"aucun capital de départ ; équipe 35 % plus chère\"]","[\"b\",\"pas de capital de départ au-delà du bonus de votre style ; équipe 35 % plus chère\"]")
rep("['g',\"coûts de transaction −28 % : le modèle","['g',\"capital de départ +0,40 M$\"],['g',\"coûts de transaction −28 % : le modèle")
rep("coûts de transaction +12 %","capital de départ +0,15 M$ ; coûts de transaction +12 %")
open('index.html','w',encoding='utf-8').write(s);print('lot120 p1 ok')
