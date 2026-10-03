# Lot 177 : rachats et souscriptions des investisseurs divisés par 2 (demande d'Antoine : « trop énorme »). Taux de rachat
# et de souscription de chaque investisseur, souscription d'office de la Couronne (5 à 12,5 %), retour d'un investisseur parti
# (2,5 % de l'encours de départ).
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
for a,b in [("w0:0.35,out:0.45,inn:0.05","w0:0.35,out:0.225,inn:0.025"),("w0:0.30,out:0.35,inn:0.08","w0:0.30,out:0.175,inn:0.04"),
            ("w0:0.15,out:0.55,inn:0.12","w0:0.15,out:0.275,inn:0.06"),("w0:0.20,out:0.50,inn:0.10","w0:0.20,out:0.25,inn:0.05"),
            ("w0:0,out:0.55,inn:0.05","w0:0,out:0.275,inn:0.025"),("royAuto:[0.10,0.25]","royAuto:[0.05,0.125]"),("back:0.05,backLp","back:0.025,backLp")]:rep(a,b)
open('index.html','w',encoding='utf-8').write(s);print('lot177 ok')
s=open('index.html',encoding='utf-8').read()
rep("de 10 à 25 % de sa ligne selon la confiance","de 5 à 12,5 % de sa ligne selon la confiance")
rep("(au taux le plus fort, 55 %)","(au taux le plus fort, 27,5 %)")
open('index.html','w',encoding='utf-8').write(s);print('lot177 p1b ok')
