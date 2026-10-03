# Lot 164 : annonces — la chance de tenir chaque promesse est affichée à tous les niveaux ; événement du conseil : les
# investisseurs en place veulent remettre au pot (la Couronne n'entre plus que par son trophée).
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("${S.tcvEst&&(S.size||'mid')!=='mega'?(()=>{const b=expBook(S.k),z=b.s>0?(b.m-o.ret)/b.s:0,p=1/(1+Math.exp(-1.702*z));\n        return `<div class=\"commrow\"><span>Chance de tenir, d'après votre attendu</span><b>${Math.round(p*100)} %</b></div>`})():''}",
    "${(()=>{const b=expBook(S.k),z=b.s>0?(b.m-o.ret)/b.s:0,p=1/(1+Math.exp(-1.702*z));\n        return `<div class=\"commrow\"><span>Chance de tenir, d'après votre attendu</span><b>${Math.round(p*100)} %</b></div>`})()}")
rep(" {who:\"Relations investisseurs\",t:\"La Couronne du Liquidistan veut entrer\",\n  p:\"Une souscription de 12 % de votre encours, disponible immédiatement, assortie d'une fenêtre de rachat trimestrielle sans préavis.\",\n  ch:[{b:\"Prendre l'argent\",s:\"La holding royale entre avec 12 % de l'encours : il grimpe, le passif devient plus fragile.\",e:{royIn:0.12,lp:4,rc:-7,flighty:true}},",
    " {who:\"Relations investisseurs\",t:\"Vos investisseurs veulent remettre au pot\",\n  p:\"Ensemble, ils proposent 12 % d'encours en plus, tout de suite — en échange d'une fenêtre de rachat trimestrielle sans préavis.\",\n  ch:[{b:\"Prendre l'argent\",s:\"+12 % d'encours, au prorata de chacun ; le passif devient plus fragile.\",e:{aum:0.12,lp:4,rc:-7,flighty:true}},")
open('index.html','w',encoding='utf-8').write(s);print('lot164 ok')
