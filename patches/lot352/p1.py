p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
rep("""const BUDK=1.60;   /* lot 123 : toutes les équipes 20 % moins chères ; lot 348 : ×1,78 — la société ne paie plus la facture des ordres (campagne : survie 81 %, 79 % avant) */""",
    """const BUDK=0.90;   /* lot 123 : toutes les équipes 20 % moins chères ; lot 348 : 1,60 ; lot 352 : retour à 0,90 (trop cher), la compensation viendra d'ailleurs */""")
open(p,'w',encoding='utf-8').write(s)
