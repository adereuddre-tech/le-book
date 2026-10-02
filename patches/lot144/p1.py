# Lot 144 : bonus d'équipe — l'effet était bloqué à ×1,00 dès que le cran de salle de marché ne baissait pas les coûts
# (Ingrid ×1,00 depuis le lot 126). Effet direct et multiplicatif à tous les crans : 5 % ×1,10 · 7,5 % ×1,05 · 10 % ×1,00 ·
# 15 % ×0,94 · 20 % ×0,90.
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("const BONFX=[{g:0.50,p:0.50},{g:0.65,p:0.40},{g:0.80,p:0.30},{g:0.95,p:0.20},{g:1.10,p:0.12}],BONCUT=1.5;","const BONFX=[{c:1.10,p:0.50},{c:1.05,p:0.40},{c:1.00,p:0.30},{c:0.94,p:0.20},{c:0.90,p:0.12}],BONCUT=1.5;")
rep("function execMot(i){const e=EXECM[i==null?S.bud.exec:i];return e<1?1-(1-e)*BONFX[bonEff()].g:e}","function execMot(i){return EXECM[i==null?S.bud.exec:i]*BONFX[bonEff()].c}")
rep("Bonus au cran ${dec(BONUS[bonEff()]*100,1)} % : le desk livre ${Math.round(BONFX[bonEff()].g*100)} % de la baisse des coûts de votre budget · coûts ×${dec(execMot(),2)} au lieu de ×${dec(EXECM[S.bud.exec],2)}","Bonus au cran ${dec(BONUS[bonEff()]*100,1)} % : coûts d'exécution ×${dec(BONFX[bonEff()].c,2)} · avec votre salle de marché ×${dec(execMot(),2)}")
rep("{const F=BONFX[pf>0?i:0],c=e<1?1-(1-e)*F.g:e;","{const F=BONFX[pf>0?i:0],c=e*F.c;")
rep("Le taux fixe deux choses, directement : la part de la baisse des coûts d'exécution de votre budget salle de marché que le desk livre, et le risque de débauchage.","Le taux fixe deux choses, directement : un multiplicateur sur tous vos coûts d'exécution (×1,10 à 5 %, ×0,90 à 20 %) et le risque de débauchage.")
open('index.html','w',encoding='utf-8').write(s);print('lot144 ok')
