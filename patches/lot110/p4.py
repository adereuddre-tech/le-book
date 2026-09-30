# Lot 110, p4 : recalibration. Campagne 225 parties (bot, taux de bonus 0/10/20 % appariés) :
# bonus : optimum intérieur à 10 % (10 % − 0 % : +2,7 ± 1,4 M$ ; 20 % − 10 % : −0,8 ± 0,6 M$) — paramètres gardés.
# survie trop haute (normal 87 %, difficile 71 %, cibles 70/60) : rachats des investisseurs relevés (×1,4 environ).
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("w0:0.35,out:0.30,inn:0.05,","w0:0.35,out:0.45,inn:0.05,")
rep("w0:0.30,out:0.25,inn:0.08,","w0:0.30,out:0.35,inn:0.08,")
rep("w0:0.15,out:0.40,inn:0.12,","w0:0.15,out:0.55,inn:0.12,")
rep("w0:0.20,out:0.35,inn:0.10,","w0:0.20,out:0.50,inn:0.10,")
open('index.html','w',encoding='utf-8').write(s);print('lot110 p4 ok')
