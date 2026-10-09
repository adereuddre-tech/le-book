p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
# 1. le style
rep("""];
/* figés depuis le retrait de ces deux choix de l'écran d'accueil */""",""",
 {id:'rv',sum:{pw:"les paires : chaque trimestre, deux couples de marchés mal pricés que vous seul voyez",f:["coûts d'exécution −20 %","investisseurs 15 % moins nerveux","le portage lu trois fois plus nettement"],w:["un extrême fait diverger les paires : décote de liquidité ×2","vol cible 16 % : de petits gains, beaucoup de levier"]},lvl:'Expert',who:"« Je ne parie pas sur le marché, je parie sur l'écart »",nm:"Gérant de valeur relative",
  p:"Deux marchés qui devraient se tenir la main se sont lâchés : vous achetez l'un, vendez l'autre, et attendez qu'ils se retrouvent. Des gains réguliers, peu de risque apparent, beaucoup de levier. Jusqu'au jour où tout le monde sort en même temps et où les écarts, au lieu de se refermer, explosent.",
  ef:[['g',"<b>Pouvoir propre — les paires</b> : chaque trimestre, deux couples de marchés proches dont l'écart s'est ouvert ; jouer les deux jambes (long l'un, court l'autre) rapporte la convergence, que votre attendu intègre"],['g',"veille des extrêmes modeste : 20 à 80 % sentis, 30 à 70 % identifiés"],['g',"vous lisez le portage trois fois plus nettement (bruit ×0,3) ; tendance et valeur moins bien (×1,3)"],['g',"coûts de transaction −20 % : vous traitez des écarts, pas des directions"],['g',"investisseurs 15 % moins nerveux : la courbe est lisse"],['b',"votre desk vise 16 % de vol : de petits écarts, qu'il faut beaucoup de levier pour rendre rentables"],['b',"dans un événement extrême, vos paires divergent : décote de liquidité doublée (LTCM, 1998)"],['b',"capture 55 % d'un mouvement en cours de trimestre"],['g',"commission de performance +2 pts ; capital de départ +0,5 M$"],['b',"équipe 10 % plus chère : il faut des docteurs en mathématiques"]],
  sigBonus:0,capture:0.55,tcMult:0.80,rumBonus:0.05,lpMult:0.85,modelScale:0.80,incMult:1.0,incSev:1.0,numeric:false,pairs:true}
];
/* figés depuis le retrait de ces deux choix de l'écran d'accueil */""")
rep("const STYPERF={syst:0,fonda:0.03,flux:0.05};","const STYPERF={syst:0,fonda:0.03,flux:0.05,rv:0.02};")
rep("const STYSEED={syst:0.0005,fonda:0,flux:0.0005};","const STYSEED={syst:0.0005,fonda:0,flux:0.0005,rv:0.0005};")
rep("const STYCOST={syst:0.85,fonda:1,flux:1.35};","const STYCOST={syst:0.85,fonda:1,flux:1.35,rv:1.10};")
rep("const STYLESIG={syst:'c',flux:'t',fonda:'v'},","const STYLESIG={syst:'c',flux:'t',fonda:'v',rv:'c'},")
rep("const XSB={syst:{s:0.27,i:0.50},fonda:{s:0.175,i:0.65},flux:{s:0.40,i:0.10}};","const XSB={syst:{s:0.27,i:0.50},fonda:{s:0.175,i:0.65},flux:{s:0.40,i:0.10},rv:{s:0.20,i:0.30}};")
rep(""" syst:{F:0.85,T:0.45,C:0.45,V:0.45,X:0,macro:1.0,mkt:1.0,""",""" rv:{F:0.55,T:0.30,C:1.10,V:0.90,X:0.30,macro:0.8,mkt:1.0,
  txt:"Votre desk pèse d'abord le portage et la valeur relative entre marchés voisins ; les sources macro servent à éviter les mauvaises surprises, pas à parier."},
 syst:{F:0.85,T:0.45,C:0.45,V:0.45,X:0,macro:1.0,mkt:1.0,""")
rep(""" grp("Votre style de gestion","1 sur 3",PROFILES,'prof')""",""" grp("Votre style de gestion",`1 sur ${PROFILES.length}`,PROFILES,'prof')""")
rep("""const ICO={prof:{fonda:'📚',flux:'⚡',syst:'🤖'},""","""const ICO={prof:{fonda:'📚',flux:'⚡',syst:'🤖',rv:'🔗',tail:'🦢',act:'🦅'},""")
rep("""pw={syst:"le modèle : book entier en facile, six convictions en moyen et difficile",""","""pw={rv:"les paires : deux écarts à refermer par trimestre",tail:"la protection au juste prix, et qui rend plus que le choc",act:"une attaque de monnaie par an",syst:"le modèle : book entier en facile, six convictions en moyen et difficile",""")
rep("""const XR={syst:"20–85 % · 45–85 %",""","""const XR={rv:"20–80 % · 30–70 %",tail:"30–95 % · 45–90 %",act:"25–90 % · 50–95 %",syst:"20–85 % · 45–85 %",""")
# 2. les paires : un fait de marché (tous les fonds le subissent), que seul ce style voit
rep(""" S.rBase=drawReturns();""",""" S.rBase=drawReturns();
 pairDraw();   /* lot 270 */""")
rep("""function stressGap(k,sc){const w=weights(k);let g=0;for(let i=0;i<N;i++)g+=Math.abs(w[i])*INSTR[i].sigQ;return STRGAP*g*(sc&&sc.ext?2:1)*crowd(riskShown(w).total)}""",
    """function stressGap(k,sc){const w=weights(k);let g=0;for(let i=0;i<N;i++)g+=Math.abs(w[i])*INSTR[i].sigQ;return STRGAP*g*(sc&&sc.ext?2:1)*crowd(riskShown(w).total)*(S&&S.prof==='rv'?2:1)}   /* lot 270 : les paires divergent */
/* lot 270 : deux paires par trimestre — même classe, facteurs les plus proches ; l'écart se referme de PAIRA σ par jambe */
const PAIRA=0.30;
function pairDraw(){const u=prng32(hash32('pair'+S.q,S.seed));S.pairs=[];const used=new Set();const C=[];
 for(let i=0;i<N;i++)for(let j=i+1;j<N;j++){if(!mktOpen(i)||!mktOpen(j)||INSTR[i].grp!==INSTR[j].grp)continue;const a=INSTR[i].b,b=INSTR[j].b;let d=0,na=0,nb=0;for(let k=0;k<K;k++){d+=a[k]*b[k];na+=a[k]*a[k];nb+=b[k]*b[k]}
  const c=d/Math.sqrt(Math.max(1e-9,na*nb));if(c>0.6)C.push({i,j,c,r:u()})}
 C.sort((x,y)=>(y.c+0.6*y.r)-(x.c+0.6*x.r));
 for(const o of C){if(S.pairs.length>=2)break;if(used.has(o.i)||used.has(o.j))continue;used.add(o.i);used.add(o.j);
  const sg=u()<0.5?1:-1,L=sg>0?o.i:o.j,Sh=sg>0?o.j:o.i;S.pairs.push({l:L,s:Sh});
  S.rBase[L]+=PAIRA*INSTR[L].sigQ;S.rBase[Sh]-=PAIRA*INSTR[Sh].sigQ}}
function pairAlpha(i){if(!S||S.prof!=='rv'||!S.pairs)return 0;let z=0;S.pairs.forEach(p=>{if(p.l===i)z+=PAIRA;if(p.s===i)z-=PAIRA});return z}""")
rep("""  z+=(SIGW.t*e.t[i]+SIGW.c*e.c[i]+SIGW.v*cv*e.v[i])*(UNIV().edge||1);""","""  z+=(SIGW.t*e.t[i]+SIGW.c*e.c[i]+SIGW.v*cv*e.v[i])*(UNIV().edge||1);
  z+=pairAlpha(i);   /* lot 270 */""")
# 3. affichage : bloc « votre pouvoir »
rep("""  <div class="block" id="pwblk"></div>""","""  <div class="block" id="stypw"${PROF().pairs||PROF().atk||PROF().tailH?'':' hidden'}></div>
  <div class="block" id="pwblk"></div>""")
rep(""" pwDraw();   /* lot 268 */""",""" pwDraw();styDraw();   /* lot 268 ; lot 270 */""")
rep("""function pwHere(o){""","""function styDraw(){const el=document.getElementById('stypw');if(!el)return;const P=PROF();let h='';
 if(P.pairs&&S.pairs&&S.pairs.length)h=`<div class="blockhead"><h2>Les paires du trimestre</h2><span class="hint">vous seul les voyez</span></div>
  ${S.pairs.map(p=>`<div class="kv"><span>🔗 long <b>${INSTR[p.l].sym}</b> · court <b>${INSTR[p.s].sym}</b> <span class="dim-g">(${INSTR[p.l].nm} / ${INSTR[p.s].nm})</span></span><b class="pos-g">+${dec(PAIRA*100/100*2,2)} σ</b></div>`).join('')}
  <p class="note" style="margin:4px 0 0">L'écart s'est ouvert ; il se referme d'environ ${dec(PAIRA,2)} σ par jambe ce trimestre. Jouez les deux jambes à risque égal : le pari porte sur l'écart, pas sur la direction. Votre attendu par marché l'intègre déjà.</p>`;
 if(typeof styDrawX==='function')h+=styDrawX();
 el.innerHTML=h;el.hidden=!h;if(typeof styWire==='function')styWire(el)}
function pwHere(o){""")
open(p,'w',encoding='utf-8').write(s)
