# Lot 161 : plus de contrainte de capacité (choix d'Antoine) — l'impact de marché reste en racine carrée de la taille, sans
# surcoût au-delà d'un encours seuil, et les souscriptions ne sont plus freinées. La rentabilité affichée au book déduit
# déjà cet impact (profitBook). Équilibrage : moyen, équipe ×1,20 (×1,10) ; fondamental, coûts d'exécution ×1,15 (×1,08).
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("function capStress(){return Math.max(0,S.nav/capSoftNav()-1)}","function capStress(){return 0}   /* lot 161 : pas de plafond de capacité */")
rep(" Capacité : au-delà de ${mm(capSoftNav())}, les souscriptions diminuent, et s'arrêtent à ${mm(2*capSoftNav())} (« fonds plein ») : un fonds trop gros ne peut plus placer l'argent sans faire bouger les marchés.","")
rep("goalMult:1,costM:1.10,seed:0.00015}","goalMult:1,costM:1.20,seed:0.00015}")
rep("sigBonus:5,capture:0.60,tcMult:1.08,","sigBonus:5,capture:0.60,tcMult:1.15,")
open('index.html','w',encoding='utf-8').write(s);print('lot161 ok')
s=open('index.html',encoding='utf-8').read()
rep("coûts de transaction +8 % : vous arbitrez tard","coûts de transaction +15 % : vous arbitrez tard")
open('index.html','w',encoding='utf-8').write(s);print('lot161 p1b ok')
