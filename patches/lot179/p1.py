# Lot 179 : bonus d'équipe minimal = 10 × le coût, en % de 100 M$, des traders embauchés (Winnie, 100 pb = 1 % → 10 %).
# Le cran de gauche vaut ce minimum ; les autres ajoutent 2,5 / 5 / 10 / 15 points. Effets par cran (coûts, débauchage) inchangés.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("const BONUS=[0.05,0.075,0.10,0.15,0.20],POACHP=0.5,MOT={i0:2};",
    "const BONOFF=[0,0.025,0.05,0.10,0.15],POACHP=0.5,MOT={i0:2};\n"
    "function bonBase(){if(!S||!S.bud)return 0;let t=-1;for(let p=Math.min(S.bud.fo,FOP.length-1);p>=0;p--)if(FOP[p].cls){t=p;break}return t>=0?10*FOP[t].bp*1e-4:0}   /* lot 179 */\n"
    "function bonRate(i){return bonBase()+BONOFF[i]}")
rep("Bonus au cran ${dec(BONUS[bonEff()]*100,1)} %","Bonus au taux de ${dec(bonRate(bonEff())*100,1)} %")
rep("const amt=Math.min(BONUS[i]*Math.max(0,perf),Math.max(0,mgrCash()));","const amt=Math.min(bonRate(i)*Math.max(0,perf),Math.max(0,mgrCash()));")
rep("return pf>0?Math.min(BONUS[S.bonI==null?MOT.i0:S.bonI]*pf,Math.max(0,mgrCash())):0}","return pf>0?Math.min(bonRate(S.bonI==null?MOT.i0:S.bonI)*pf,Math.max(0,mgrCash())):0}")
rep("(bonus ${dec(BONUS[bonEff()]*100,1)} %)","(bonus ${dec(bonRate(bonEff())*100,1)} %)")
rep("${BONUS.map((p,i)=>{const F=BONFX[pf>0?i:0],c=F.c;return `<button class=\"bnp${i===cur?' on':''}\" data-i=\"${i}\">${dec(p*100,Number.isInteger(Math.round(p*1000)/10)?0:1)} %<br><small>${mm(p*pf)}",
    "${BONOFF.map((o,i)=>{const p=bonRate(i),F=BONFX[pf>0?i:0],c=F.c;return `<button class=\"bnp${i===cur?' on':''}\" data-i=\"${i}\">${dec(p*100,Number.isInteger(Math.round(p*1000)/10)?0:1)} %<br><small>${mm(p*pf)}")
rep("Une part de votre commission de performance${pf>0?` (${mm(pf)} ce trimestre)`:' — aucune ce trimestre : rien ne sera versé, et le desk se comporte comme au cran minimal'}",
    "Une part de votre commission de performance${pf>0?` (${mm(pf)} ce trimestre)`:' — aucune ce trimestre : rien ne sera versé, et le desk se comporte comme au cran minimal'}. Le minimum vaut 10 fois le coût de vos traders sur 100 M$ (${dec(bonBase()*100,1)} % aujourd'hui) ; chaque cran ajoute 2,5, 5, 10 ou 15 points")
assert 'BONUS[' not in s and 'BONUS.map' not in s
open('index.html','w',encoding='utf-8').write(s);print('lot179 ok')
