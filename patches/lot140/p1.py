# Lot 140 : six anecdotes du back office (Josiane ×2, Gontran, Mireille, Tatillon ×2), au format des anecdotes d'exécution.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
NEW=r'''
 {who:"Josiane Suspens · back office",t:"« Le courtier nous a facturé deux fois le même trimestre. Je l'ai vu parce que je relis tout »",p:"Elle a surligné les deux lignes en jaune fluo. Puis la facture entière, par principe.",
  ch:[{b:"Faire rembourser, avec intérêts",s:"+2 pb récupérés, comité +1.",e:{cash:0.0002,rc:1}},{b:"Laisser passer, garder la relation",s:"Coûts −10 % ce trimestre : le courtier se sent redevable.",e:{tcMult:0.9}}]},
 {who:"Josiane Suspens · back office",t:"« Il manque 4 000 € au rapprochement. Je ne rentre pas tant que je ne les ai pas trouvés »",p:"Il est 22 h. Elle a commandé des sushis pour elle et pour le logiciel de rapprochement.",
  ch:[{b:"Rester avec elle",s:"−2 pb (heures sup et sushis), comité +2.",e:{cash:-0.0002,rc:2}},{b:"Lui dire de rentrer",s:"20 % de risque que l'écart cache une vraie erreur : −0,2 %.",e:{risk:[0.2,-0.002],riskMsg:"Les 4 000 € étaient une erreur de règlement à six zéros",safeTxt:"C'était un arrondi. Josiane l'a trouvé à 8 h, avant son café."}}]},
 {who:"Gontran Report-à-Nouveau · expert-comptable",t:"« Je peux décaler la comptabilisation des frais d'un trimestre. C'est parfaitement légal, ou presque »",p:"Il ajuste ses lunettes. « Presque, c'est un mot comptable. »",
  ch:[{b:"Décaler",s:"+3 pb de trésorerie ce trimestre, comité −3.",e:{cash:0.0003,rc:-3}},{b:"Tout passer dans le trimestre",s:"Comité +1. Gontran soupire.",e:{rc:1}}]},
 {who:"Mireille Cauchemar · contrôle des risques",t:"« Votre plus grosse position représente 31 % du risque. Justifiez-moi ça avant midi »",p:"Elle a imprimé le rapport. Elle l'a annoté à l'encre verte, ce qui est pire que le rouge.",
  ch:[{b:"Justifier, longuement",s:"Comité +2, coûts +5 % : le desk a passé la matinée sur le rapport.",e:{rc:2,tcMult:1.05}},{b:"Promettre de réduire « au prochain signal »",s:"Comité −2.",e:{rc:-2}}]},
 {who:"L'inspecteur Tatillon · conformité",t:"« J'ai relu les messageries du desk. Quelqu'un a écrit “on va les tondre” »",p:"« Je ne dis pas que c'est un délit. Je dis que je l'ai noté. »",
  ch:[{b:"Formation déontologie pour tout le desk",s:"−2 pb, comité +2, débauchage +5 % : le desk déteste les formations.",e:{cash:-0.0002,rc:2,poach:0.05}},{b:"Expliquer que c'était une métaphore agricole",s:"Comité −2.",e:{rc:-2}}]},
 {who:"L'inspecteur Tatillon · conformité",t:"« Votre stagiaire a reçu une cravate d'un courtier. Une cravate à clip, mais une cravate »",p:"Il tient la cravate dans un sachet de pièce à conviction.",
  ch:[{b:"Rendre la cravate, avec une lettre",s:"Comité +1.",e:{rc:1}},{b:"Garder la cravate",s:"Comité −1, Jean-Kevin est ravi.",e:{rc:-1}}]},'''
rep("const TRADER_EXEC=[","const TRADER_EXEC=["+NEW)
open('index.html','w',encoding='utf-8').write(s);print('lot140 p1 ok')
