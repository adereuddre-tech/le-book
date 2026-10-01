# Lot 124 : les Cheminots ne pouvaient pas retirer un avis (il faut deux trimestres positifs pour passer au vert, l'avis est
# payé dès la clôture suivante). Leur avis tombe désormais dès un trimestre positif.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("if(v.ntc>0){if(r.vd>0){r.cancel=true;v.ntc=0}","if(v.ntc>0){if(r.vd>0||(v.id==='cr'&&o.r>0)){r.cancel=true;v.ntc=0}")
rep("rule:\"souscrit après 2 trimestres positifs d'affilée, rachète après 2 trimestres négatifs d'affilée.\"",
    "rule:\"souscrit après 2 trimestres positifs d'affilée, dépose un avis de rachat après 2 trimestres négatifs d'affilée ; un seul trimestre positif suffit à le lui faire retirer.\"")
rep("l'avis tombe si le critère repasse au vert","l'avis tombe si le critère repasse au vert (pour les Cheminots : dès un trimestre positif)")
open('index.html','w',encoding='utf-8').write(s);print('lot124 p1 ok')
