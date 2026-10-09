p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
# styles
rep("['g',\"il lit tendance, portage et valeur plus nettement que les autres styles\"]",
    "['g',\"il lit les trois signaux de marché, tendance, portage et valeur, avec un bruit ×0,6 ; chaque autre style lit le sien ×0,3 mais les deux autres ×1,3\"]")
rep("['g',\"+5 sources par trimestre : on vous rappelle, on vous parle\"]",
    "['g',\"+5 sources par trimestre : on vous rappelle, on vous parle\"],['g',\"vous lisez la valeur trois fois plus nettement (bruit ×0,3) ; tendance et portage moins bien (×1,3)\"]")
rep("['g',\"vous lisez les dépêches mieux que personne : probabilités 40 % plus précises\"]",
    "['g',\"vous lisez les dépêches mieux que personne : probabilités 40 % plus précises\"],['g',\"vous lisez la tendance trois fois plus nettement (bruit ×0,3) ; portage et valeur moins bien (×1,3)\"]")
rep(",['b',\"incidents opérationnels +25 % : on va vite, on vérifie peu\"]","")
# difficultés
rep('["g","investisseurs patients : confiance de départ +8, rachats 25 % plus petits"]',
    '["g","investisseurs patients : confiance de départ +8, pertes 40 % moins mal vécues, rachats 25 % plus petits"],["g","comité indulgent : une perte lui coûte 25 % de moins"]')
rep('["b","investisseurs exigeants"]','["b","investisseurs et comité de référence : ni indulgents, ni voraces"]')
rep('["b","investisseurs voraces : confiance de départ −8, pertes 40 % plus mal vécues, rachats 15 % plus gros"]',
    '["b","investisseurs voraces : confiance de départ −8, pertes 40 % plus mal vécues, rachats 15 % plus gros"],["b","comité sévère : une perte lui coûte 35 % de plus"]')
# durées
rep('ef:[["g","format court : une erreur ne condamne pas la partie"],["g","les jauges ont moins le temps de se dégrader"],',
    'ef:[["g","format court : idéal pour découvrir les écrans et les mécaniques"],["g","les jauges ont moins le temps de se dégrader"],["b","pas le temps de se refaire après un mauvais trimestre"],')
rep('ef:[["g","assez long pour que la discipline paie"],["g","commissions cumulées substantielles"],',
    'ef:[["g","assez long pour que la discipline paie"],["g","commissions cumulées substantielles"],')
# coûts, sous le capot
rep("Chaque changement de position paie une demi-fourchette plus un impact qui croît en racine carrée du notionnel, puis de plus en plus vite quand l'encours dépasse celui du départ (puissance 0,8), multiplié par le budget desk, l'organisation, la liquidité du régime et le taux au jour le jour.",
    "Chaque changement de position paie une demi-fourchette plus un impact qui croît en racine carrée du notionnel (plus vite dans les carnets étroits). La facture entière est ensuite freinée par la taille : au-delà de 100 M$ d'encours, × (encours / 100 M$)<sup>0,35</sup> — deux fois plus cher à 700 M$. Elle est multipliée par votre front office, votre style, le bonus d'équipe, la liquidité du régime et le taux au jour le jour ; sans trader sur la classe, l'ordre passe par un courtier, ×2. En cours de trimestre s'ajoute un surcoût d'urgence : suivre un mouvement coûte plus cher, le contrer moins, et un gros contre-pied dans un extrême peut rapporter.")
rep("/* commission de performance : fixée par la difficulté (15 / 20 / 25 %) */","/* commission de performance : fixée par la difficulté (15 / 20 / 30 %), plus le style */")
open(p,'w',encoding='utf-8').write(s)
