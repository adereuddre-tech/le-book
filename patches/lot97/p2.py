# Lot 97b : les anecdotes de Dwight (souvent personnelles : voix cassée, beau-frère, cuisine) sortent du tirage en son absence.
s=open('index.html',encoding='utf-8').read()
o="function persoOk(e){const w=e.who||'';if(/Marie-Alpha/.test(w)&&!here(6))return false;"
assert s.count(o)==1; s=s.replace(o,o+"if(/^Dwight/.test(w)&&!here(1))return false;")
open('index.html','w',encoding='utf-8').write(s);print('ok')
