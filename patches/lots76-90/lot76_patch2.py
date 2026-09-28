P='/home/claude/le-book/index.html';s=open(P,encoding='utf-8').read()
def rep(old,new,k=1):
    global s;n=s.count(old);assert n==k,(n,old[:80]);s=s.replace(old,new)
rep("il juge vos résultats à chaque clôture et sort des cartons. Ce qu'il note entre-temps pèse sur la confiance, pas sur les cartons.",
    "il juge vos résultats à chaque clôture et sort des cartons. Ce qu'il note entre-temps pèse sur la confiance ; une seule exception : si la confiance tombe à zéro, le jaune tombe sur-le-champ.")
rep("20 points sous la médiane des concurrents, book vide.</li>","20 points sous la médiane des concurrents, book vide, confiance à zéro (même en cours de trimestre).</li>")
rep("['Accidents de levier',`au-delà de ${dec(TAIL.x0*100,0)} % de risque ex ante`]","['Accidents de levier et appels de marge',`au-delà de ${dec(TAIL.x0*100,0)} % de risque ex ante`]")
open(P,'w',encoding='utf-8').write(s);print('ok')
