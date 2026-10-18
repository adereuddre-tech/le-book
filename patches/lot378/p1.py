p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# Glossaire et info-bulles : à jour (impact payé par le fonds, moral, accidents, sang-froid), sans jargon d'ancienne échelle
rep(""" 'impact de marché':"Le prix qui bouge contre vous pendant que vous exécutez : plus l'ordre est gros par rapport au carnet, plus il pèse.",""",
    """ 'impact de marché':"Le prix qui bouge contre vous pendant que vous exécutez : plus l'ordre est gros par rapport au carnet, plus il pèse. Il est payé par le fonds.",""")
rep(""" 'moral':"L'humeur de vos traders, de 0 à 100. Il ne dépend que de l'argent (le bonus) et des égards (locaux, petits gestes) ; il règle les coûts d'exécution, la lecture des dépêches, les anecdotes et le débauchage.",""",
    """ 'moral':"L'humeur de vos traders, de 0 à 100. Il ne dépend que de l'argent (le cran de bonus) et des égards (locaux, petits gestes) ; il règle l'impact de vos ordres, la lecture des dépêches et la veille, les anecdotes, le sang-froid et le débauchage.",
 'sang-froid':"Ce que le moral donne dans les crises : ×1,4 à moral 0, ×0,7 à 100, sur la fréquence des accidents internes et des fuites, et sur la gravité des accidents et des extrêmes.",
 'accident de levier':"Un choc venu de l'intérieur ou du prime broker : positions cachées, ordres en double, marges relevées. Possible à tout niveau de risque, plus fréquent et plus grave quand il monte ; le contrôle des risques et le sang-froid du desk le réduisent.",""")
rep(""" 'masse salariale':"La somme des salaires de l'équipe choisie. Elle fixe le niveau du desk ou du back office : le cran le plus haut que cette somme paierait sur l'ancienne échelle.",""",
    """ 'masse salariale':"La somme des salaires de l'équipe choisie. Elle fixe le niveau d'ensemble du desk ou du back office ; ce qu'apporte chaque personne en propre s'y ajoute.",""")
rep("""<p>Les chiffres annoncés dans les options sont exacts : « coûts −40 % » réduit vraiment de 40 % la facture de courtage, que paie votre société. Mais l'impact de marché, lui, est payé par le fonds, et il suit la manière d'exécuter : payer le bloc protège le prix moyen, négocier un rabais le dégrade. Chaque bouton annonce les deux, avec l'effet sur les jauges.</p>""",
    """<p>Les chiffres annoncés dans les options sont exacts : « coûts −40 % » réduit vraiment de 40 % la facture des ordres, fourchette et impact, que paie le fonds. Le prix moyen suit la manière d'exécuter : payer le bloc le protège, négocier un rabais le dégrade. Votre société ne paie que le courtage, et les rabais ou dépenses de votre choix. Chaque bouton annonce les deux, avec l'effet sur les jauges.</p>""")
rep("""   ${row("Coûts d'exécution",'×'+dec(Fc.c,2),'×'+dec(F0.c,2))}""","""   ${row("Impact de vos ordres",'×'+dec(Fc.c,2),'×'+dec(F0.c,2))}""")
rep("""et redouble d'efforts (coûts d'exécution −8 %).`}""","""et redouble d'efforts (impact −8 %).`}""")
rep("""Vous avez recruté un trader chez un concurrent : coûts d'exécution −8 %.\"""","""Vous avez recruté un trader chez un concurrent : impact −8 %.\"""")
open(p,"w",encoding="utf-8").write(s)
