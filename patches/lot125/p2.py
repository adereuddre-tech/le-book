# Lot 125, p2 : en-têtes courts du tableau des styles.
s=open('index.html',encoding='utf-8').read()
o="${P.map(p=>`<th>${p.nm.split(' ')[0]==='Gérant'?p.nm.replace('Gérant de ','').replace(' et de momentum',''):p.nm.split(' ').slice(0,2).join(' ')}</th>`).join('')}"
assert s.count(o)==1
s=s.replace(o,"${P.map(p=>`<th>${({syst:'Quant',fonda:'Fondamental',flux:'Flux'})[p.id]}</th>`).join('')}")
open('index.html','w',encoding='utf-8').write(s);print('lot125 p2 ok')
