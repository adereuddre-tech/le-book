# Lot 134 : fondamental, coûts d'exécution ×1,00 (au lieu de ×1,12) et commission de performance +2 pts (choix d'Antoine). Campagne finale, partie normale (540 parties) : le
# fondamental était dominé — survie 70 % (flux 69 %) pour 20,3 M$ (quant 25,6, flux 30,1).
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("sigBonus:5,capture:0.60,tcMult:1.12,","sigBonus:5,capture:0.60,tcMult:1.00,")
rep("capital de départ +0,15 M$ ; coûts de transaction +12 % : vous arbitrez tard, et cher","capital de départ +0,15 M$")
open('index.html','w',encoding='utf-8').write(s);print('lot134 p1 ok')
s=open('index.html',encoding='utf-8').read()
rep("const STYPERF={syst:0,fonda:0,flux:0.05};","const STYPERF={syst:0,fonda:0.02,flux:0.05};")
rep("capital de départ +0,15 M$","capital de départ +0,15 M$ ; commission de performance +2 pts : vos investisseurs paient le temps passé à vérifier")
open('index.html','w',encoding='utf-8').write(s);print('lot134 p1b ok')
