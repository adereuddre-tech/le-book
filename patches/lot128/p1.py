# Lot 128 : collatéral « tokens liquides de NFT » en bas de liste, le plus rémunérateur et le plus risqué.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep(" {id:'cdo2',nm:'CDO au carré',ico:'🎲',y:0.090,p:0.35,l:0.22,d:\"Des tranches de CDO elles-mêmes adossées à des tranches de CDO. Personne ne sait exactement ce qu'il y a dedans — c'est même l'idée.\"},\n",
    " {id:'cdo2',nm:'CDO au carré',ico:'🎲',y:0.090,p:0.35,l:0.22,d:\"Des tranches de CDO elles-mêmes adossées à des tranches de CDO. Personne ne sait exactement ce qu'il y a dedans — c'est même l'idée.\"},\n"
    " {id:'nft',nm:'Tokens liquides de NFT',ico:'🐒',y:0.120,p:0.40,l:0.35,d:\"Des parts d'un coffre de singes pixelisés, échangeables à toute heure. Liquides, tant que quelqu'un veut encore des singes.\"},\n")
open('index.html','w',encoding='utf-8').write(s);print('lot128 p1 ok')
