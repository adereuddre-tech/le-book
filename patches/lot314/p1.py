p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# 1. tutoriel
rep("""Le <b>carton</b> à droite rappelle où vous en êtes avec le comité des risques.</p>""","""Juste dessous, le <b>moral</b> de votre desk, nourri par le bonus et les égards : il règle vos coûts, votre lecture des dépêches et le débauchage. Le <b>carton</b>, au bout de la jauge de confiance, rappelle où vous en êtes avec le comité des risques.</p>""")
rep("""leur nombre et leur fiabilité dépendent du budget de recherche macro que vous avez fixé et de votre style.""","""leur nombre et leur fiabilité dépendent de la masse salariale de votre front office et de votre style.""")
rep("""Leur nombre et leur fiabilité dépendent du budget de recherche macro et de votre style.""","""Leur nombre et leur fiabilité dépendent de la masse salariale du front office et de votre style.""")
# 2. budgets : l'équipe se compose personne par personne
rep("""d:"Les traders et la recherche. Chaque recrue améliore l'avis du desk sur toutes les classes et sur la macro : coûts d'exécution, bruit des indicateurs, nombre et fiabilité des sources, lecture des dépêches. Un trader couvre en plus sa classe : sans lui, vos ordres y passent par un courtier, commission et impact de marché multipliés.",""",
    """d:"Les traders et la recherche, recrutés un par un. La masse salariale fixe le niveau du desk sur toutes les classes et sur la macro : coûts d'exécution, bruit des indicateurs, nombre et fiabilité des sources, lecture des dépêches. Chaque personne apporte en plus ce qui lui est propre : un trader couvre sa classe (sans lui, vos ordres y passent par un courtier, commission et impact de marché multipliés), d'autres ont un pouvoir ou un talent particulier.",""")
rep("""d:"Le loyer, la comptabilité, les opérations, le contrôle des risques et la conformité. Josiane Suspens est le point neutre. Le loyer seul, c'est la catastrophe : incidents en série, chocs extrêmes encaissés de plein fouet. Au-dessus, chaque poste réduit nettement la fréquence et la gravité des incidents et amortit le choc immédiat des événements extrêmes, et rassure le comité.",""",
    """d:"La comptabilité, les opérations, le contrôle des risques et la conformité, recrutés un par un. Le niveau de Josiane Suspens est le point neutre. Personne, c'est le loyer seul, et la catastrophe : incidents en série, chocs extrêmes encaissés de plein fouet. Plus la masse salariale monte, plus les incidents sont rares et légers, plus le choc immédiat des extrêmes est amorti, et plus le comité est rassuré ; chaque poste apporte en plus son talent propre.",""")
rep("""<summary>À quoi sert ce budget · les ${b.lv.length} crans</summary>""","""<summary>À quoi sert ce budget · les ${b.lv.length} postes et niveaux</summary>""")
# 3. règles de l'accueil
rep("""Elle est multipliée par votre front office, votre style, le bonus d'équipe, la liquidité du régime""","""Elle est multipliée par votre front office, votre style, le moral du desk, la liquidité du régime""")
rep("""selon votre style, vos équipes et leur bonus, et une protection""","""selon votre style, vos équipes et leur moral, et une protection""")
rep("""Le quantitatif est le plus sûr, le fondamental le plus informé, le flux le plus rapide et le plus exposé.\"""",
    """Le quantitatif est le plus sûr ; le chasseur de queue gagne quand tout s'effondre ; le fondamental est le plus informé ; la valeur relative joue des paires ; le flux est le plus rapide et le plus exposé ; l'activiste force des marchés hors du book.\"""")
# 4. trésorerie : le capital de départ existe
rep("""<p>Votre société de gestion n'a pas de capital : sa trésorerie, ce sont vos gains nets — votre score — moins la part que vous avez placée dans le fonds, qui est bloquée jusqu'à la clôture.</p>""",
    """<p>Votre société de gestion part avec un petit capital, selon la difficulté et votre style ; ensuite, sa trésorerie, ce sont vos gains nets — votre score — moins la part que vous avez placée dans le fonds, bloquée jusqu'à la clôture.</p>""")
rep("""  const it=[[`Commissions de gestion`,S.cMgmt||0],""","""  const it=[...((S.mgrSeed||0)>0?[[`Capital de départ`,S.mgrSeed]]:[]),[`Commissions de gestion`,S.cMgmt||0],""")
# 5. presse et mémoire : la manœuvre
rep("""t=cur.atk.ok?`Nous avions qualifié d'imprudente l'attaque de ${F} sur ${cur.atk.nm}. Nous retirons « imprudente »`:`L'attaque de ${F} sur ${cur.atk.nm} a échoué.""",
    """t=cur.atk.ok?`Nous avions qualifié d'imprudente la manœuvre de ${F} sur ${cur.atk.nm}. Nous retirons « imprudente »`:`La manœuvre de ${F} sur ${cur.atk.nm} a échoué.""")
# 6. bonus : plus de « cran minimal » immédiat, c'est le moral qui glisse
rep(""":' — aucune ce trimestre : rien ne sera versé, et le desk se comporte comme au cran minimal'}""",""":' — aucune ce trimestre : rien ne sera versé, et le moral glisse vers la cible du taux minimum'}""")
rep("""Le minimum vaut 5 fois le coût de votre front office sur 100 M$""","""Le minimum vaut 5 fois la masse salariale de votre front office sur 100 M$""")
# 7. multiplicateur d'exécution : ce n'est plus le débauchage
rep("""${S.execPenalty!==1?`, débauchage ×${dec(S.execPenalty,2)}`:''}""","""${S.execPenalty!==1?`, recrues et moral ×${dec(S.execPenalty,2)}`:''}""")
# 8. objectifs : niveau équivalent
rep("""Porter le front office jusqu'à Winnie au moins, et battre la médiane""","""Porter la masse salariale du front office au niveau de Winnie au moins, et battre la médiane""")
rep("""Porter le front office jusqu'à Winnie au moins, et garder""","""Porter la masse salariale du front office au niveau de Winnie au moins, et garder""")
# 9. glossaire
rep(""" 'drain de volatilité':""",""" 'moral':"L'humeur de vos traders, de 0 à 100. Il ne dépend que de l'argent (le bonus) et des égards (locaux, petits gestes) ; il règle les coûts d'exécution, la lecture des dépêches, les anecdotes et le débauchage.",
 'masse salariale':"La somme des salaires de l'équipe choisie. Elle fixe le niveau du desk ou du back office : le cran le plus haut que cette somme paierait sur l'ancienne échelle.",
 'drain de volatilité':""")
open(p,'w',encoding='utf-8').write(s)
