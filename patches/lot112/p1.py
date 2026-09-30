# Lot 112 : bonus d'équipe minimal à 5 % (crans 5 / 7,5 / 10 / 15 / 20 %, 10 % par défaut) ; faillite dès la première
# clôture en trésorerie négative.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("const BONUS=[0,0.05,0.10,0.15,0.20],","const BONUS=[0.05,0.075,0.10,0.15,0.20],")
rep("if(S.cashNeg>=2)S.over='cash';","if(S.cashNeg>=1)S.over='cash';")
rep("`Deuxième clôture de suite en trésorerie négative, au trimestre ${S.q} :","`Trésorerie négative à la clôture du trimestre ${S.q} :")
rep("['Fin de partie','deux clôtures de suite en trésorerie négative']","['Fin de partie','une clôture en trésorerie négative']")
rep("Deux clôtures de suite en trésorerie négative, et c'est le dépôt de bilan.","Une seule clôture en trésorerie négative, et c'est le dépôt de bilan.")
rep("</b> Encore une clôture dans le rouge et la société de gestion dépose le bilan.","</b> À la clôture, la société de gestion déposera le bilan si elle reste dans le rouge.")
open('index.html','w',encoding='utf-8').write(s);print('lot112 p1 ok')
s=open('index.html',encoding='utf-8').read()
rep("data-i=\"${i}\">${Math.round(p*100)} %<br>","data-i=\"${i}\">${dec(p*100,Number.isInteger(Math.round(p*1000)/10)?0:1)} %<br>")
open('index.html','w',encoding='utf-8').write(s);print('lot112 p1b ok')
