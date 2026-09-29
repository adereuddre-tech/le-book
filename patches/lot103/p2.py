# Lot 103, p2 : un stop respecté (book coupé) ne vaut plus aucun carton, même si la perte continue ;
# concentration jugée au point affiché (70 % affiché = pas de carton).
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("  else if(qTotal<=-2*ls)red=`trimestre à ${sgnp(qTotal,1)}, deux fois le stop`;","  else if(S.stopCut!==S.q-1&&qTotal<=-2*ls)red=`trimestre à ${sgnp(qTotal,1)}, deux fois le stop`;")
rep("  else if(S.stopQn!==S.q-1&&qTotal<=-ls)why","  else if(S.stopQn!==S.q-1&&qTotal<=-ls&&qTotal>-2*ls)why")
rep("  if(cc.v>lc+1e-9)why.push(","  if(Math.round(cc.v*100)>Math.round(lc*100))why.push(")
open('index.html','w',encoding='utf-8').write(s);print('lot103 p2 ok')
