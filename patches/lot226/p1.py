# Lot 226 : résultat du trimestre — le commentaire ne contredit plus le résultat. Le régime (titre + phrase) décrit le
# marché sans juger le book ; une seconde phrase dit ce que le book en a fait, selon le signe et l'ampleur du résultat
# (avec un mot propre quand le book gagne contre un vent de face ou perd par vent arrière).
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
rep('{nm:"Vent de face généralisé",d:"Rien de catastrophique, mais tout a tiré dans le mauvais sens.",',
    '{nm:"Vent de face généralisé",d:"Croissance en recul, inflation en hausse, appétit en berne : tout a soufflé contre les acheteurs.",wind:-1,')
rep('{nm:"Vent arrière généralisé",d:"Tout est allé dans le bon sens en même temps. Profitez-en, ça ne se reproduira pas de sitôt.",',
    '{nm:"Vent arrière généralisé",d:"Croissance, désinflation et appétit pour le risque en même temps : tout a porté les acheteurs.",wind:1,')
rep("les marchés ont fait leur travail et le book a fait le sien.","les marchés ont fait leur travail, sans excès.")
rep("function qRegime(){",
"""/* lot 226 : ce que le book a fait du trimestre, cohérent avec son résultat */
function qVerb(R,q){if(R&&R.wind<0&&q>0)return 'Votre book était du bon côté : il gagne contre le vent.';
 if(R&&R.wind>0&&q<0)return "Votre book n'en a pas profité.";
 return q>=0.02?'Votre book en a tiré le meilleur.':q>=0?'Votre book termine dans le vert, sans éclat.':q>-0.02?'Votre book y laisse un peu.':'Votre book en a fait les frais.'}
function qRegime(){""")
rep('<div class="regime">${R.nm}</div><div class="sub">${R.d}</div></div>','<div class="regime">${R.nm}</div><div class="sub">${R.d} ${qVerb(R,o.qTotal)}</div></div>')
open('index.html','w',encoding='utf-8').write(s);print('lot226 ok')
s=open("index.html",encoding="utf-8").read()
rep("Tout le monde gagne de l'argent et personne ne dort tranquille.","Les acheteurs gagnent de l'argent et personne ne dort tranquille.")
rep("Le collatéral rapporte plus que le book.","Le collatéral rapporte plus que la plupart des books.")
rep("et c'est celui que la moitié du book ne regardait pas.","et c'est celui que la moitié des books ne regardait pas.")
open('index.html','w',encoding='utf-8').write(s);print('lot226b ok')
