# -*- coding: utf-8 -*-
"""Lot 46 — trois concurrents, un par style, et vraiment très bons.

Décision d'Antoine (option a pour l'indice) : les concurrents gagnaient trop peu pour servir
d'étalon (gérant médian ≈ 1 % de l'encours sur deux ans, bot ≈ 20 %, indice ≈ 880). On les
renforce, on leur donne chacun un style, et on retire Millénaire.

  - Médaillon d'Or joue en quant : il lit juste la plupart des facteurs, un peu sur chacun, et
    récolte les signaux de marché — régulier, peu de bruit.
  - Pont-Levis Associés joue en fondamental : une conviction forte sur le thème dominant du
    trimestre, le reste à peine au-dessus du hasard — de grosses années et des trous d'air.
  - Citadelle Nord joue le flux : il prolonge les facteurs du trimestre précédent et sait parfois
    sentir le retournement — excellent quand le régime dure, puni quand il casse.
  `rivalE` porte la logique des trois styles ; `rivalReturns` (clôture, rng) et `rivRet` (ruban,
  tirage pur) la partagent. Plafond d'adresse relevé de 0,82 à 0,88.
Textes : « quatre concurrents » → trois, « cinq fonds » → quatre ; les deux anecdotes où
Millénaire débauchait passent à Citadelle Nord, qui hérite de son appétit de chasseur.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
e.rep(''' {nm:"Pont-Levis Associés",boss:"Rayon Daglio",skill:0.615,vol:0.095,aum:150},
 {nm:"Médaillon d'Or",boss:"Jim Simonet",skill:0.730,vol:0.075,aum:60},
 {nm:"Millénaire Partners",boss:"Isidore Anglaidre",skill:0.665,vol:0.085,aum:170,poacher:1.6},
 {nm:"Citadelle Nord",boss:"Ken Griffon",skill:0.675,vol:0.115,aum:140,poacher:1.3}''',
''' {nm:"Pont-Levis Associés",boss:"Rayon Daglio",style:'fonda',skill:0.74,vol:0.16,aum:150},
 {nm:"Médaillon d'Or",boss:"Jim Simonet",style:'syst',skill:0.78,vol:0.14,aum:60},
 {nm:"Citadelle Nord",boss:"Ken Griffon",style:'flux',skill:0.72,vol:0.20,aum:140,poacher:1.6}''')
e.rep("rivals:RIVALS.map(r=>({...r,skill:Math.max(0.5,Math.min(0.82,r.skill+Z.rivSkill)),",
      "rivals:RIVALS.map(r=>({...r,skill:Math.max(0.5,Math.min(0.88,r.skill+Z.rivSkill)),")
old=e.s[e.s.index("function rivalReturns(){"):]
old=old[:old.index("\n}\n")+3]
e.rep(old,"""/* Ce qu'un concurrent capte des facteurs du trimestre, selon son style. u() : tirage uniforme
   (rng à la clôture, hash pur pour le ruban). */
function rivalE(rv,u){
 const f=S.f||[0,0,0,0],st=rv.style||'fonda';let e=0;
 if(st==='syst'){for(let k=0;k<K;k++)e+=(u()<rv.skill?1:-1)*Math.abs(f[k]);return 0.9*e+0.8}
 if(st==='flux'){const p=S.fLast;
  for(let k=0;k<K;k++){const s0=p&&p[k]?Math.sign(p[k]):(u()<0.5?1:-1);
   const ok=Math.sign(f[k]||1)===s0||u()<(rv.skill-0.5)*1.8;e+=(ok?1:-1)*Math.abs(f[k])}
  return 1.1*e}
 let km=0;for(let k=1;k<K;k++)if(Math.abs(f[k])>Math.abs(f[km]))km=k;
 e=(u()<rv.skill?1:-1)*Math.abs(f[km])*1.8;
 for(let k=0;k<K;k++)if(k!==km)e+=(u()<0.55?1:-1)*Math.abs(f[k])*0.4;
 return e;
}
const RIVNOISE={syst:0.45,fonda:0.75,flux:0.70};
function rivalReturns(){
 return S.rivals.map(rv=>{
   const e=rivalE(rv,rng);
   return (rv.vol/2)*(0.70*e/2+(RIVNOISE[rv.style]||0.78)*gauss())-0.008;
 });
}
""")
e.rep("""function rivRet(j,t,q){
 const r=S.rivals&&S.rivals[j];if(!r||!S.f||!S.f.length)return 0;
 let e=0;for(let k=0;k<K;k++){const u=prng32(hash32('rivk'+j+'_'+q+'_'+k,S.seed))();
  e+=(u<r.skill?1:-1)*Math.sign(S.f[k]||1)*S.f[k]}
 return t*((r.vol/2)*(0.70*e/2)-0.008);""","""function rivRet(j,t,q){
 const r=S.rivals&&S.rivals[j];if(!r||!S.f||!S.f.length)return 0;
 const e=rivalE(r,prng32(hash32('rivk'+j+'_'+q,S.seed)));
 return t*((r.vol/2)*(0.70*e/2)-0.008);""")
# objectifs nominatifs
e.rep(''' {nm:"Millénaire à sa place",d:"Faire mieux que Millénaire Partners ce trimestre.",t:c=>c.beat('Millénaire Partners'),b:0.06},\n''','')
e.rep('d:"Terminer dans les trois premiers au classement cumulé.",t:c=>c.rank<=3,','d:"Terminer dans les deux premiers au classement cumulé.",t:c=>c.rank<=2,')
# anecdotes où Millénaire débauchait
e.rep('t:"Millénaire Partners fait une offre à Ingrid"','t:"Citadelle Nord fait une offre à Ingrid"')
e.rep('Millénaire Partners lui propose son propre pod.','Citadelle Nord lui propose son propre pod.')
# nombre de fonds dans les textes
for a,b,k in [("quatre concurrents","trois concurrents",None),("cinq fonds","quatre fonds",None),
              ("battu les quatre","battu les trois",1),("devant les quatre maisons","devant les trois maisons",1),
              ("<sup>${rank===1?'er':'e'}</sup>/5</b>","<sup>${rank===1?'er':'e'}</sup>/4</b>",1),
              ("sur cinq : ${ahead.nm}","sur quatre : ${ahead.nm}",1),
              ("${rk===5?'cinquième':'quatrième'} sur cinq.","${rk===4?'quatrième':'troisième'} sur quatre.",1),
              ("+'e'} sur cinq : le tableau","+'e'} sur quatre : le tableau",1),
              ("${rank}e sur cinq : ${best.nm}","${rank}e sur quatre : ${best.nm}",1),
              ("</sup> sur cinq</span></div>","</sup> sur quatre</span></div>",1),
              ("${rank===1?'er':'e'} sur 5, perte max","${rank===1?'er':'e'} sur 4, perte max",1)]:
    n=e.s.count(a);assert n>=1,a
    if k:assert n==k,(a,n)
    e.s=e.s.replace(a,b)

# ── des concurrents très bons partout : le surcroît d'adresse du mastodonte est ramené de
#    +0,085 à +0,03, et les investisseurs pèsent l'écart à la médiane un peu moins lourdement
#    (115 → 85 par point) — sinon la place devenait une machine à rachats (survie mesurée du
#    bot au mastodonte : 2 parties sur 15) ──
e.rep("rivSkill:0.085,rivVol:1.15,","rivSkill:0.030,rivVol:1.10,")
# la boutique affrontait des concurrents trop faibles pour servir d'étalon (indice médian du bot ≈ 500)
e.rep("rivSkill:-0.050,rivVol:0.85,","rivSkill:-0.010,rivVol:0.95,")
e.rep("lpD.push(['Écart à la médiane des concurrents',(net-med)*115","lpD.push(['Écart à la médiane des concurrents',(net-med)*85")
e.done("lot 46 — trois concurrents, un par style")
