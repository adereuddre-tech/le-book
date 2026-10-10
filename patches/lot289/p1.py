p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
rep("""["Book du modèle",p=>f(p.modelScale)+' le risque de croisière']""","""["Book du desk (facile)",p=>f(p.deskScale||p.modelScale)+' le risque de croisière']""")
rep("votre desk vise 120 % du risque de croisière : plus de rendement, plus de secousses","en facile, votre desk propose un book prudent (60 % du risque de croisière) : à vous d'oser plus")
rep("votre desk vise 115 % du risque de croisière : des convictions massives","en facile, votre desk propose un book prudent (75 % du risque de croisière) : les convictions massives, c'est vous")
open(p,'w',encoding='utf-8').write(s)
