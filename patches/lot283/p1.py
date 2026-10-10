p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
# chasseur de queues : trop dur (survie 50–61 % sur trois campagnes) — vers ~72 %, entre le fondamental et la valeur relative
rep("sigBonus:0,capture:0.60,tcMult:1.0,rumBonus:0.10,lpMult:1.25,modelScale:0.90,incMult:0.9,incSev:1.0,numeric:false,tailH:true}","sigBonus:0,capture:0.60,tcMult:1.0,rumBonus:0.10,lpMult:1.10,modelScale:0.90,incMult:0.9,incSev:1.0,numeric:false,tailH:true}")
rep("rv:0.0005,tail:0,act:0.001};","rv:0.0005,tail:0.0005,act:0.001};")
rep("rv:1.10,tail:1.0,act:1.20};","rv:1.10,tail:0.90,act:1.20};")
rep("""lpD.push(["Encore un trimestre à payer l'assurance",-2]);""","""lpD.push(["Encore un trimestre à payer l'assurance",-1]);""")
rep("""['b',"investisseurs 25 % plus nerveux : ils ne comprennent pas pourquoi vous payez l'assurance"],['b',"chaque trimestre calme où vous êtes couvert : « encore un trimestre à payer l'assurance », confiance −2"]""",
    """['b',"investisseurs 10 % plus nerveux : ils ne comprennent pas pourquoi vous payez l'assurance"],['b',"chaque trimestre calme où vous êtes couvert : « encore un trimestre à payer l'assurance », confiance −1"],['g',"capital de départ +0,5 M$ ; équipe 10 % moins chère : un desk sobre"]""")
rep("""w:["investisseurs 25 % plus nerveux","chaque trimestre calme où vous êtes couvert : confiance −2"]""","""w:["investisseurs 10 % plus nerveux","chaque trimestre calme où vous êtes couvert : confiance −1"]""")
open(p,'w',encoding='utf-8').write(s)
