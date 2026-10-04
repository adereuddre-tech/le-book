# Lot 191 : écran d'ouverture — la trésorerie affichée retirait une seconde fois le bonus d'équipe et le co-investissement
# (déjà prélevés à l'ouverture) parce que le jeu se croyait encore au débriefing ; 2,80 M$ affichés pour 9,56 M$ réels.
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("function phaseDesk(){\n save('phaseDesk');","function phaseDesk(){\n S.phase='open';   /* lot 191 */\n save('phaseDesk');")
open('index.html','w',encoding='utf-8').write(s);print('lot191 ok')
