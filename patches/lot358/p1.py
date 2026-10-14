p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
rep("""const STRESSK=0.32,STRGAP=0.28;""","""const STRESSK=0.32,STRGAP=0.15;   /* lot 358 : gap de crise 28 % → 15 % de la vol trimestrielle de chaque ligne */""")
open(p,'w',encoding='utf-8').write(s)
