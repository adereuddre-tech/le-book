# Lot 175 : flux un peu plus risqué — équipe ×1,50 (×1,30). Les incidents (fréquence ×2,1 ou coût ×3,5) et la commission +4 pts
# ne font plus bouger sa survie ; l'équipe, oui. 90 parties de flux, graines 10001–10030 : actuel 71 % · 50,4 M$ (méd 21,1) ;
# équipe ×1,50 : 67 % · 48,4 (méd 16,2) ; commission +4 : 72 % · 53,6 ; incidents ×3,5 : 72 % · 49,3 ; fréquence ×2,1 : 71 % · 53,8.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("const STYCOST={syst:0.85,fonda:1,flux:1.30};","const STYCOST={syst:0.85,fonda:1,flux:1.50};")
rep("équipe 30 % plus chère","équipe 50 % plus chère")
open('index.html','w',encoding='utf-8').write(s);print('lot175 ok')
