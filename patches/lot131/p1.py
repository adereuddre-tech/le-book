# Lot 131 : audit automatique du sens des 292 dépêches (pré-annonces). Les chocs pétroliers et gaziers étaient cohérents ;
# les défauts et faillites se lisaient « liquidité en hausse » (le dollar recule dans leurs mouvements). Sens imposé :
# un défaut ou une faillite = liquidité, appétit et croissance en baisse (sauf l'accord arraché in extremis).
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep(" [/relève (ses|les) taux|hausse (surprise )?(de )?ses taux|resserrement monétaire|plus faucon|resserre/i,[-1,-1,2,-2]]];",
    " [/relève (ses|les) taux|hausse (surprise )?(de )?ses taux|resserrement monétaire|plus faucon|resserre/i,[-1,-1,2,-2]],\n [/^(?!.*arraché).*(défaut|faillite|panique bancaire)/i,[-1,-0.5,1.5,-2]]];   /* lot 131 */")
open('index.html','w',encoding='utf-8').write(s);print('lot131 p1 ok')
