# Lot 133 : incidents du flux ×1,70 en fréquence (×1,65 au lot 132), coût ×2,2 inchangé.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("incMult:1.65,incSev:2.2,","incMult:1.70,incSev:2.2,")
rep("incidents plus fréquents (×1,65) et deux fois plus chers","incidents plus fréquents (×1,70) et deux fois plus chers")
open('index.html','w',encoding='utf-8').write(s);print('lot133 p1 ok')
