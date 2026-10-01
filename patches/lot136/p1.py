# Lot 136 : fondamental sans bonus de capital de départ (0 au lieu de +0,15 M$), coûts d'exécution ×1,08 (×1,00) et
# commission +4 pts (+3). Mesure (180 parties normales) : seul, le capital à 0 : 78 % · 26,7 M$ ; avec coûts ×1,08 et
# +4 pts : 76 % · 27,8 M$ (méd 14,2) — score entre quant (25,6) et flux (30,1), survie au niveau du quant (76 %).
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("const STYSEED={syst:0.0004,fonda:0.00015,flux:0};","const STYSEED={syst:0.0004,fonda:0,flux:0};")
rep("capital de départ +0,15 M$ ; commission","commission")
rep("sigBonus:5,capture:0.60,tcMult:1.00,","sigBonus:5,capture:0.60,tcMult:1.08,")
rep("const STYPERF={syst:0,fonda:0.03,flux:0.05};","const STYPERF={syst:0,fonda:0.04,flux:0.05};")
rep("commission de performance +3 pts : vos investisseurs paient le temps passé à vérifier","commission de performance +4 pts : vos investisseurs paient le temps passé à vérifier ; coûts de transaction +8 % : vous arbitrez tard")
open('index.html','w',encoding='utf-8').write(s);print('lot136 p1 ok')
