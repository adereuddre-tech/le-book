# Lot 221 : probabilités en pourcentage — deals du prime broker en début de trimestre (« une fois sur 3,0 » → « 33 % de
# chances ») et lignes de l'accident de levier (« une chance sur deux » → « 50 % de chances »).
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
rep("<span>−${dec(t.c*100,1)} % tout de suite, +${dec(t.g*100,1)} % une fois sur ${dec(1/t.p,1)}.</span>",
    "<span>−${dec(t.c*100,1)} % tout de suite, +${dec(t.g*100,1)} % avec ${Math.round(t.p*100)} % de chances.</span>")
rep("row('une chance sur deux',","row('50 % de chances',",2)
open('index.html','w',encoding='utf-8').write(s);print('lot221 ok')
