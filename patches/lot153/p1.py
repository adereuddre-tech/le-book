# Lot 153 : coûts d'exécution des taux et de l'AUD ramenés à des niveaux réalistes, rapportés au risque (demi-fourchette / vol) :
# Bund 11,7 → 5,8 (au niveau du T-Note), Gilt 15,7 → 7,9, OAT 18,5 → 9,2, JGB 32,5 → 15, AUD 11,8 → 6,8.
# L'ordre des coûts suit désormais l'ordre d'ouverture (rk) dans chaque classe.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("grp:'Taux', sig:0.060, s:0.70, c:0.55,","grp:'Taux', sig:0.060, s:0.35, c:0.30,")
rep("grp:'Taux', sig:0.070, s:1.10, c:1.00,","grp:'Taux', sig:0.070, s:0.55, c:0.50,")
rep("grp:'Taux', sig:0.065, s:1.20, c:1.10,","grp:'Taux', sig:0.065, s:0.60, c:0.55,")
rep("grp:'Taux', sig:0.040, s:1.30, c:1.30,","grp:'Taux', sig:0.040, s:0.60, c:0.60,")
rep("grp:'Devises', sig:0.110, s:1.30, c:1.10,","grp:'Devises', sig:0.110, s:0.75, c:0.65,")
open('index.html','w',encoding='utf-8').write(s);print('lot153 ok')
