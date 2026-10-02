# Lot 159 : rééquilibrage après les concurrents à book réel (campagne lot 158 : survie 80 %, facile 88 / moyen 82 / difficile 70 %).
# Équipes ×0,90 (×0,80) ; commission du fondamental +3 pts (+4).
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("const BUDK=0.80;","const BUDK=0.90;")
rep("const STYPERF={syst:0,fonda:0.04,flux:0.05};","const STYPERF={syst:0,fonda:0.03,flux:0.05};")
n=s.count("commission de performance +4 pts");s=s.replace("commission de performance +4 pts","commission de performance +3 pts");print('textes +4→+3 :',n)
open('index.html','w',encoding='utf-8').write(s);print('lot159 ok')
