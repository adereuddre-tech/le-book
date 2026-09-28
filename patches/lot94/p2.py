# Lot 94b : description du front office sans multiplicateur en dur (il est affiché par covTxt).
s=open('index.html',encoding='utf-8').read()
o="commission et impact de marché ×1,5."
assert s.count(o)==1; s=s.replace(o,"commission et impact de marché multipliés.")
open('index.html','w',encoding='utf-8').write(s)
