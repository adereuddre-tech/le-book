# Lot 117, p2 : textes de fin de trimestre sur les investisseurs, alignés sur leurs critères (lot 105/115).
import re
s=open('index.html',encoding='utf-8').read()
i=s.index(" /* relatif ou contexte */\n I.push(rel>0.01?");j=s.index(",3));\n",i)+len(",3));\n")
s=s[:i]+''' /* lot 117 : chaque investisseur, sur son propre critère */
 I.push(invSay());
'''+s[j:]
s=s.replace("function invTable(){",r'''function invSay(){const R=S.invQ||[],H=S.invH||[],L=H[H.length-1]||{r:0,rel:0,ok:false},out=[];
 R.forEach(r=>{const v=r.vd;
  if(r.id==='cr')out.push(v<0?"La caisse de retraite des Cheminots voit deux trimestres négatifs d'affilée : elle demande à sortir.":v>0?"Deux trimestres positifs d'affilée : la caisse de retraite des Cheminots renforce.":"La caisse de retraite attend deux trimestres du même signe pour bouger.");
  if(r.id==='fs')out.push(L.ok?"Objectif annoncé tenu : Nordhavn souscrit, comme promis.":"Objectif annoncé manqué : Nordhavn réduit sa ligne.");
  if(r.id==='fam')out.push(v<0?`Le family office Vandermeer n'aime pas ${sgnp(L.r,1)} : il retire une partie de sa mise.`:v>0?`${sgnp(L.r,1)} : le family office Vandermeer en redemande.`:"Le family office Vandermeer ne bouge pas : trimestre ni assez bon, ni assez mauvais.");
  if(r.id==='ff')out.push(v<0?`${sgnp(L.rel,1)} contre la moyenne des concurrents : le fonds de fonds Albatros vous déclasse.`:v>0?`${sgnp(L.rel,1)} contre la moyenne des concurrents : le fonds de fonds Albatros vous surpondère.`:"Dans la moyenne des concurrents : le fonds de fonds Albatros ne change rien.")});
 return out.join(' ')}
function invTable(){''',1)
assert s.count("function invSay()")==1
open('index.html','w',encoding='utf-8').write(s);print('lot117 p2 ok')
