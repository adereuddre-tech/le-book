# Lot 231 : flux un peu moins puni — équipe ×1,50 → ×1,35. Diagnostic : le gérant flux touche ~0,5 M$ de frais de gestion
# par trimestre pour ~1 M$ d'équipe ; il vit des commissions de performance et fait faillite après un ou deux trimestres
# sans. Le capital de départ n'y change rien (calibration : 0,5 / 1,5 / 2,5 M$ → survie 50 / 47 / 48 %).
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
rep("STYCOST={syst:0.85,fonda:1,flux:1.50}","STYCOST={syst:0.85,fonda:1,flux:1.35}")
s=s.replace("équipe 50 % plus chère","équipe 35 % plus chère")
open('index.html','w',encoding='utf-8').write(s);print('lot231 ok')
