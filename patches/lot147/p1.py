# Lot 147 : prime broker, « doubler vos lignes de levier » : les effets sont écrits dans les boutons.
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("{b:\"Accepter la ligne\",s:\"Le comité voit une tentation, les investisseurs une marque de confiance.\",e:{lp:3,rc:-6}},","{b:\"Accepter la ligne\",s:\"Confiance +3, comité −6 : les investisseurs y voient une marque de confiance, le comité une tentation. Aucun effet sur vos marges.\",e:{lp:3,rc:-6}},")
rep("{b:\"Décliner\",s:\"Rien ne change.\",e:{rc:2}}]},","{b:\"Décliner\",s:\"Comité +2. Rien d'autre ne change.\",e:{rc:2}}]},")
open('index.html','w',encoding='utf-8').write(s);print('lot147 ok')
