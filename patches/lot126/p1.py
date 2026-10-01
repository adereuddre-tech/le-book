# Lot 126 : flux, « l'aura du prophète » (texte de la commission +5 pts) ; Dwight ×1,15 et Ingrid ×1,00 sur les coûts
# d'exécution (EXECM, crans 1 et 2) ; trois collatéraux plus risqués en bas de liste (prêts à effet de levier, stablecoins
# synthétiques, CDO au carré). Les actions du « pink sheet » ne sont pas ajoutées : aucun prime broker ne les prend en gage.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("['g',\"commission de performance +5 pts\"]","['g',\"commission de performance +5 pts : l'aura du prophète — vos investisseurs paient plus cher pour être du bon côté de celui qui « sent » le marché, et aucun ne veut être celui qui est parti juste avant le grand coup\"]")
rep("const EXECM=[1.35,1.3,1.04,","const EXECM=[1.35,1.15,1.00,")
rep(" {id:'junk',nm:'Junk bonds',ico:'☠️',y:0.045,p:0.30,l:0.12,d:\"Des obligations notées sous la catégorie investissement. Le coupon est superbe tant que personne ne fait défaut.\"},\n",
    " {id:'junk',nm:'Junk bonds',ico:'☠️',y:0.045,p:0.30,l:0.12,d:\"Des obligations notées sous la catégorie investissement. Le coupon est superbe tant que personne ne fait défaut.\"},\n"
    " {id:'lev',nm:'Prêts à effet de levier',ico:'🏗️',y:0.055,p:0.30,l:0.14,d:\"Des prêts syndiqués aux rachats d'entreprises, sans clauses de protection. Taux variable, liquidité de week-end.\"},\n"
    " {id:'stab',nm:'Stablecoins synthétiques',ico:'🪙',y:0.070,p:0.25,l:0.22,d:\"Un dollar numérique tenu par une position de base sur les dérivés crypto. Stable, sauf le jour où il ne l'est pas.\"},\n"
    " {id:'cdo2',nm:'CDO au carré',ico:'🎲',y:0.090,p:0.35,l:0.22,d:\"Des tranches de CDO elles-mêmes adossées à des tranches de CDO. Personne ne sait exactement ce qu'il y a dedans — c'est même l'idée.\"},\n")
open('index.html','w',encoding='utf-8').write(s);print('lot126 p1 ok')
