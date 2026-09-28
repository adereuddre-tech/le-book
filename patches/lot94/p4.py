# Lot 94d : campagne 180 parties appariées (standard Boris + Lettrage) : ×3 −0,3 ± 0,8 M$ face à ×1,5 (sans effet),
# ×5 −2,6 ± 1,5 ; équipe complète (Winnie) − standard : −1,2 ± 1,3 à ×3, +1,1 ± 1,6 à ×5. ×5 retenu : le recrutement compte.
s=open('index.html',encoding='utf-8').read()
assert s.count('NOTRD=1.5,')==1; s=s.replace('NOTRD=1.5,','NOTRD=5,')
open('index.html','w',encoding='utf-8').write(s);print('ok')
