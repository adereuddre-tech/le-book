# Lot 135 : fondamental placé entre le quant et le flux — plus volatil (incidents ×1,35 en fréquence, ×1,4 en coût)
# et plus rentable (commission +3 pts au lieu de +2).
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("rumBonus:0.18,lpMult:1.0,incMult:1.0,modelScale:1.10,","rumBonus:0.18,lpMult:1.0,incMult:1.35,incSev:1.4,modelScale:1.10,")
rep("const STYPERF={syst:0,fonda:0.02,flux:0.05};","const STYPERF={syst:0,fonda:0.03,flux:0.05};")
rep("commission de performance +2 pts : vos investisseurs paient le temps passé à vérifier","commission de performance +3 pts : vos investisseurs paient le temps passé à vérifier ; incidents plus fréquents (×1,35) et plus chers (×1,4) : les grandes convictions font de grosses erreurs")
open('index.html','w',encoding='utf-8').write(s);print('lot135 p1 ok')
