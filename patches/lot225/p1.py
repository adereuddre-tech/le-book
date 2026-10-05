# Lot 225 : taux de capture des dépêches tiré au sort. Chaque dépêche tire le taux du desk dans [0,7 × taux du style ;
# 1,3 × taux du style] (loi uniforme, au plus 100 %) : quant 35–65 %, fondamental 42–78 %, flux 60–100 %. Le tirage
# est fait à l'arrivée de la dépêche (S.sc.cap) et sert à l'affichage comme au résultat ; le panneau le dit.
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
rep("S.sc.ph=ver?S.sc.p:Math.max(0.10,Math.min(0.80,S.sc.p+sh+sd*gauss()));   /* lot 217 : 80 % au plus */S.sc.ver=ver}",
    "S.sc.ph=ver?S.sc.p:Math.max(0.10,Math.min(0.80,S.sc.p+sh+sd*gauss()));   /* lot 217 : 80 % au plus */S.sc.ver=ver;\n  S.sc.cap=Math.min(1,pr.capture*(0.7+0.6*rng()))}   /* lot 225 : capture tirée, ±30 % autour du taux du style */")
rep("function evPlans(","function capNow(){return S.sc&&S.sc.cap!=null?S.sc.cap:PROF().capture}   /* lot 225 */\nfunction evPlans(")
rep("kE[i]=S.k[i]+prof.capture*d;","kE[i]=S.k[i]+capNow()*d;")
rep("votre desk n'est en place qu'à ${(prof.capture*100).toFixed(0)} % quand le marché repart, c'est aussi déduit.",
    "votre desk n'est en place qu'à ${(capNow()*100).toFixed(0)} % quand le marché repart sur cette dépêche (de ${Math.round(prof.capture*70)} à ${Math.min(100,Math.round(prof.capture*130))} % selon les dépêches pour votre style), c'est aussi déduit.")
rep("${prof.capture<1?` Réaction ${prof.capture<0.5?'lente':'rapide'} : ${(prof.capture*100).toFixed(0)} % de la no",
    "${capNow()<1?` Réaction ${capNow()<0.5?'lente':'rapide'} : ${(capNow()*100).toFixed(0)} % de la no")
open('index.html','w',encoding='utf-8').write(s);print('lot225 ok')
