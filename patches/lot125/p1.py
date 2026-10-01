# Lot 125 : commission de performance du flux +5 pts (variantes testées sur 60 parties de flux appariées : +2 pts +1,2 ± 1,4 M$,
# +5 pts +6,3 ± 2,2, +10 pts +16,5 ± 4,7, ×1,1 +1,7 ± 1,3, ×1,2 +2,2 ± 2,1) ; tableau récapitulatif des styles sous leurs cartes.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("function perfFee(){return (S&&SIZE().perf)||0.20}",
    "const STYPERF={syst:0,fonda:0,flux:0.05};   /* lot 125 : le style expert touche 5 pts de commission de plus */\n"
    "const STYSEED={syst:0.0004,fonda:0.00015,flux:0};\n"
    "function perfFee(){return ((S&&SIZE().perf)||0.20)+((S&&STYPERF[S.prof])||0)}")
rep("S.mgrSeed=(SIZE().seed||0)+({syst:0.0004,fonda:0.00015,flux:0}[S.prof]||0);","S.mgrSeed=(SIZE().seed||0)+(STYSEED[S.prof]||0);")
rep("['b',\"aucun capital de départ supplémentaire ; équipe 30 % plus chère\"]","['g',\"commission de performance +5 pts\"],['b',\"aucun capital de départ supplémentaire ; équipe 30 % plus chère\"]")
rep("function screenSetup(){",r'''function styTable(){const P=PROFILES,f=(x,d=2)=>'×'+dec(x,d),pw={syst:"book du modèle, en un bouton ; signaux lus plus nettement",fonda:"sources vérifiées : une probabilité sûre par trimestre",flux:"intuition : le sens d'un facteur, juste 4 fois sur 5"};
 const R=[["Pouvoir",p=>pw[p.id]],["Capital de départ",p=>STYSEED[p.id]?'+'+dec(STYSEED[p.id]*1000,2)+' M$':'—'],["Commission de performance",p=>STYPERF[p.id]?'+'+Math.round(STYPERF[p.id]*100)+' pts':'—'],
  ["Coût de l'équipe",p=>f(STYCOST[p.id])],["Coûts d'exécution",p=>f(p.tcMult)],["Book visé",p=>f(p.modelScale)+' la vol cible'],["Nervosité des investisseurs",p=>f(p.lpMult)],["Incidents",p=>f(p.incMult)],["Mouvement capté sur les dépêches",p=>Math.round(p.capture*100)+' %']];
 return `<details class="wire" style="margin-top:10px"><summary>Les trois styles en un tableau</summary><div style="overflow-x:auto"><table class="qt" style="margin-top:8px;font-size:12px"><thead><tr><th style="text-align:left"></th>${P.map(p=>`<th>${p.nm.split(' ')[0]==='Gérant'?p.nm.replace('Gérant de ','').replace(' et de momentum',''):p.nm.split(' ').slice(0,2).join(' ')}</th>`).join('')}</tr></thead><tbody>${R.map(([l,fn])=>`<tr><td style="text-align:left">${l}</td>${P.map(p=>`<td>${fn(p)}</td>`).join('')}</tr>`).join('')}</tbody></table></div></details>`}
function screenSetup(){''')
rep("   grp(\"Votre style de gestion\",\"1 sur 3\",PROFILES,'prof')+","   grp(\"Votre style de gestion\",\"1 sur 3\",PROFILES,'prof')+styTable()+")
open('index.html','w',encoding='utf-8').write(s);print('lot125 p1 ok')
