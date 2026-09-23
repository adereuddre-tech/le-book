# -*- coding: utf-8 -*-
"""Lot 49 — un seul départ (100 M$, vol 20 %), trois niveaux de difficulté, des marchés qui se
gagnent, un score en dollars, des flux clients par concurrent, des emblèmes propres aux
concurrents, et trois paliers de cartes : bronze, argent, or.

Décisions d'Antoine :
  - plus de choix de taille, d'univers ni de risque : tout le monde part avec 100 M$, une vol
    cible de 20 %, 2 % de gestion ;
  - trois marchés par classe au départ ; le 4e rang s'ouvre à 1,4 fois l'encours initial, le 5e au
    double (mécanique du lot 41) ; les exotiques s'ouvrent la première fois que vous finissez
    premier d'un trimestre ;
  - un niveau de difficulté qui règle l'adresse des concurrents, la vigilance du comité, la
    voracité et la volatilité des investisseurs — et la commission de performance : 15 / 20 / 25 %
    (`perfFee`). `SIZES` porte désormais les niveaux (ids small / mid / mega conservés : les
    sauvegardes et le palmarès restent lisibles) ;
  - le score redevient le gain net cumulé du gérant ;
  - les souscriptions et rachats se décident concurrent par concurrent : chacun a sa clientèle,
    plus ou moins nerveuse (quant 0,6, fondamental 1,0, flux 1,6). Battre un concurrent attire
    une part de ses clients, perdre contre lui en envoie chez lui ;
  - les trois concurrents portent des emblèmes à eux (médaillon, pont-levis, trident), absents
    de la liste proposée au joueur ;
  - cartes dorées en trois paliers, bronze, argent, or, du plus courant au plus rare.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
def between(a,b):
    assert e.s.count(a)==1,'debut ambigu %r'%a[:60]
    i=e.s.index(a); j=e.s.index(b,i); return e.s[i:j]

# ── 1. les niveaux de difficulté remplacent les tailles ────────────────────────
old=between("const SIZES=[","\n];")
e.rep(old,'''const SIZES=[
 {id:'small',lvl:'Débutant',nav:0.1,capX:1,perf:0.15,nm:"Facile — 15 % de performance",who:"« Des concurrents à votre portée »",
  p:"Des concurrents solides mais battables, un comité qui vous laisse respirer, des investisseurs qui pardonnent un mauvais trimestre. Vous touchez 15 % de la performance au-dessus du plus haut historique.",
  ef:[["g","concurrents moins adroits"],["g","investisseurs patients, flux plus calmes"],["g","comité indulgent"],["b","commission de performance : 15 %"]],
  rivSkill:0.020,rivVol:0.95,lpNeg:0.75,rcNeg:0.75,lp0:8,flowMult:0.75,goalMult:1},
 {id:'mid',lvl:'Normal',nav:0.1,capX:1,perf:0.20,nm:"Moyen — 20 % de performance",who:"« La place telle qu'elle est »",
  p:"Trois très bons concurrents, un comité vigilant, des investisseurs qui comparent. La commission de performance habituelle du métier : 20 %.",
  ef:[["g","commission de performance : 20 %"],["b","concurrents très bons, chacun dans son style"],["b","investisseurs exigeants, comité vigilant"]],
  rivSkill:0.050,rivVol:1,lpNeg:1,rcNeg:1,lp0:0,flowMult:1,goalMult:1},
 {id:'mega',lvl:'Expert',nav:0.1,capX:1,perf:0.25,nm:"Difficile — 25 % de performance",who:"« Les meilleurs du monde, et des clients impitoyables »",
  p:"Des concurrents au sommet de leur art, un comité sur votre dos, des investisseurs voraces dont l'argent part aussi vite qu'il arrive. En échange, vous touchez 25 % de la performance.",
  ef:[["g","commission de performance : 25 %"],["b","concurrents au sommet de leur art"],["b","investisseurs voraces, flux violents"],["b","comité impitoyable"]],
  rivSkill:0.090,rivVol:1.10,lpNeg:1.45,rcNeg:1.35,lp0:-8,flowMult:1.35,goalMult:1}''')
e.rep("const MKPERCL={small:3,mid:4,mega:5};","const MKPERCL={small:3,mid:3,mega:3};   /* lot 49 : un seul départ, les marchés se gagnent */")
e.rep("{id:'ext',edge:1.5,lpMult:1.05,","{id:'ext',edge:1,lpMult:1,")
e.rep("function SIZE(){return SIZES.find(x=>x.id===S.size)||SIZES[1]}",
      "function SIZE(){return SIZES.find(x=>x.id===S.size)||SIZES[1]}\n/* commission de performance : fixée par la difficulté (15 / 20 / 25 %) */\nfunction perfFee(){return (S&&SIZE().perf)||0.20}")
# un seul univers (tout, exotiques verrouillés), une seule vol cible
e.rep("function newGame(seed,prof,arch,desk,vol,size,univ,dur){\n rng=mulberry32(seed);",
      "function newGame(seed,prof,arch,desk,vol,size,univ,dur){\n vol='std';univ='ext';   /* lot 49 : 20 % de vol et l'univers complet pour tous ; les exotiques se gagnent */\n rng=mulberry32(seed);")
e.rep("newGame(S.seed,S.prof,S.arch,S.desk,S.vol,S.size);phaseOpen()","newGame(S.seed,S.prof,S.arch,S.desk,'std',S.size,'ext',S.dur);phaseOpen()")
e.rep("let setup={prof:'fonda',arch:'std',desk:'inhouse',vol:'std',size:'mid',univ:'com',dur:'normal'};","let setup={prof:'fonda',arch:'std',desk:'inhouse',vol:'std',size:'mid',univ:'ext',dur:'normal'};")
e.rep("""   grp("Le niveau de risque du mandat","1 sur 3 · la volatilité que vous facturez",VOLP,'vol')+
   grp("La taille du fonds","1 sur 3 · la difficulté et le nombre de marchés par classe",SIZES,'size')+
   grp("L'univers d'investissement","1 sur 3 · les classes d'actifs autorisées",UNIVS,'univ')+""",
"""   grp("La difficulté","1 sur 3 · la place, le comité, les investisseurs",SIZES,'size')+""")
e.rep(' size:"La taille commande trois choses à la fois : le nombre de marchés ouverts dans chaque classe, l\'impact de vos ordres sur les prix, et la patience des investisseurs. C\'est le curseur de difficulté principal.",',
      ' size:"Tout le monde part avec 100 M$ et une volatilité cible de 20 %. La difficulté règle l\'adresse des trois concurrents, la vigilance du comité, la voracité des investisseurs et la nervosité de leurs flux — et la commission de performance que vous touchez : 15, 20 ou 25 %.",')
old=between("function feeLine(){","\n}\n")
e.rep(old,"""function feeLine(){
 const z=SIZES.find(x=>x.id===setup.size)||SIZES[1];
 return `Votre mandat facture <strong>2 % de gestion</strong> et <strong>${(z.perf*100).toFixed(0)} % de la performance</strong> au-dessus du plus haut historique, plus le budget d'exploitation que vous fixez chaque trimestre. Objectif : <strong>12 % net par an</strong>.`;""")
e.rep("const perfQ0=idxPre>S.hwmIdx?VOL().perf*(idxPre-S.hwmIdx)","const perfQ0=idxPre>S.hwmIdx?perfFee()*(idxPre-S.hwmIdx)")
e.rep("const perf=v.perf*Math.max(0,rv.mAum-rv.mHwm);","const perf=perfFee()*Math.max(0,rv.mAum-rv.mHwm);")
e.rep("commission de performance (${(VOL().perf*100).toFixed(0)} % au-dessus","commission de performance (${(perfFee()*100).toFixed(0)} % au-dessus")
e.rep("const SZ={small:'100 M$',mid:'1 Md$',mega:'10 Md$'}","const SZ={small:'facile',mid:'moyen',mega:'difficile'}")

# ── 2. exotiques verrouillés jusqu'à une première place ─────────────────────────
e.rep("function mktOpen(i){const x=INSTR[i];return !!x&&x.rk<=OPENRK}",
      "function mktOpen(i){const x=INSTR[i];return !!x&&x.rk<=OPENRK&&(x.grp!=='Exotiques'||!!(S&&S.exoOpen))}")
e.rep(" const ok=sy=>IDX[sy]!==undefined&&rankOf(sy)<=OPENRK;",
      " const ok=sy=>{if(IDX[sy]===undefined||rankOf(sy)>OPENRK)return false;const x=INSTR[IDX[sy]];return x.grp!=='Exotiques'||!!(S&&S.exoOpen)};")
e.rep("  if(S.openRk){OPENRK=S.openRk;applyPools()}","  if(S.openRk)OPENRK=S.openRk;\n  applyPools();")
e.rep("""${mktOpen(i)?'':`<span class="capb">fermé · s'ouvre à ${mm(unlockNav(x.rk))}</span>`}""",
      """${mktOpen(i)?'':`<span class="capb">${x.grp==='Exotiques'&&x.rk<=OPENRK?'fermé · finissez un trimestre premier':`fermé · s'ouvre à ${mm(unlockNav(x.rk))}`}</span>`}""")

# ── 3. le score redevient le gain net ───────────────────────────────────────────
e.rep("""<div class="cl" style="color:var(--gold)">Indice du gérant · 100 = le gérant médian de la place</div><div class="cv" style="color:var(--gold);font-size:34px">${Math.round(mgrIndex())}</div><div class="cl" style="margin-top:4px">${score(S.mgrFees-S.mgrCosts)} de gains, soit ${sgnp((S.mgrFees-S.mgrCosts)/S.aum0,1)} de l'encours initial · gérant médian ${sgnp(rivalMgrMedian()/S.aum0,1)}</div></div>""",
      """<div class="cl" style="color:var(--gold)">Vos gains de gérant · le score</div><div class="cv" style="color:var(--gold);font-size:34px">${score(S.mgrFees-S.mgrCosts)}</div><div class="cl" style="margin-top:4px">le gérant médian de la place a gagné ${score(rivalMgrMedian())}</div></div>""")
e.rep("const txt=`${S.fundName} — ${verdict}. Indice du gérant ${Math.round(mgrIndex())} (100 = gérant médian), ${score(S.mgrFees-S.mgrCosts)} de gains,",
      "const txt=`${S.fundName} — ${verdict}. ${score(S.mgrFees-S.mgrCosts)} de gains de gérant,")
e.rep(" h.sort((a,b)=>(b.ix===undefined?-1e9:b.ix)-(a.ix===undefined?-1e9:a.ix)||b.g-a.g);"," h.sort((a,b)=>b.g-a.g);")
e.rep("Le classement se fait sur l'indice du gérant — 100, c'est le gérant médian de la place : il compare des fonds de 100 M$ et de 10 Md$ à armes égales.",
      "Le classement se fait sur les commissions nettes encaissées : c'est le score du jeu.")
e.rep("""<b class="gold-g">${r.ix===undefined?score(r.g):'indice '+Math.round(r.ix)}</b><span class="hsub ${cls(r.c)}">${r.ix===undefined?'':score(r.g)+' · '}${sgnp(r.c,0)} par an</span>""",
      """<b class="gold-g">${score(r.g)}</b><span class="hsub ${cls(r.c)}">${sgnp(r.c,0)} par an</span>""")
e.rep("restent les vôtres et la partie entre au palmarès avec un indice de ${Math.round(mgrIndex())}.</p>","restent les vôtres et la partie entre au palmarès.</p>")

# ── 4. flux clients, concurrent par concurrent ──────────────────────────────────
old=between(" /* les allocataires comparent : c'est l'écart à la médiane des concurrents qui commande, pas la performance absolue */"," /* objectif du trimestre */")
e.rep(old,""" /* Lot 49 : chaque concurrent a sa clientèle, plus ou moins nerveuse. Battre un concurrent
    attire une part de ses clients ; perdre contre lui en envoie chez lui. La somme des trois
    fait le flux net ; la voracité (difficulté) grossit les sorties, une confiance basse aussi. */
 const CLI={syst:0.6,fonda:1.0,flux:1.6};
 const fl=S.rivals.map(rv=>{const d=qTotal-(rv.last||0),s=CLI[rv.style]||1;
   let f=Math.max(-0.06,Math.min(0.06,0.5*s*d));if(f<0)f*=SIZE().flowMult;return {rv,d,f}});
 let tot=fl.reduce((a,x)=>a+x.f,0);
 if(S.lp<40)tot-=0.04*(40-S.lp)/40*SIZE().flowMult;
 tot=Math.max(-0.25,Math.min(0.20,tot+(rng()-0.5)*0.01));
 S.qFlowBy=fl.map(x=>({nm:x.rv.nm,d:x.d,f:x.f}));
 const amt=tot*S.nav;S.nav+=amt;S.flows+=amt;S.qFlow=(S.qFlow||0)+amt;
 const lines=fl.filter(x=>Math.abs(x.f)>=0.002).map(x=>`${x.rv.nm} ${x.f>0?'+':'−'}${dec(Math.abs(x.f)*100,1)} % (${x.d>0?'battu':'devant vous'} de ${dec(Math.abs(x.d)*100,1)} pt${Math.abs(x.d)>=0.015?'s':''})`);
 S.poachMsg=`${tot>=0?'Collecte':'Rachats'} : ${tot>=0?'+':'−'}${dec(Math.abs(tot)*100,1)} % d'encours (${mm(Math.abs(amt))}).${lines.length?' Clients par concurrent — '+lines.join(' · ')+'.':''}`;
 if(tot<-0.01&&rng()<(0.5+S.poachBoost)*RETM[S.bud.ret]*(rel<-0.005?1:0.4)){S.execPenalty*=1.14;S.poachMsg+=` ${(pick(S.rivals.filter(x=>x.poacher))||S.rivals[S.rivals.length-1]).boss} a débauché deux de vos gérants : coûts d'exécution +14 % durablement.`}
 if(tot>0.01&&S.bud.ret>=BUDMAX&&rng()<0.4){S.execPenalty=Math.max(0.7,S.execPenalty*0.92);S.poachMsg+=" Vous avez recruté un trader chez un concurrent : coûts d'exécution −8 %."}
""")

# ── 5. emblèmes propres aux concurrents ─────────────────────────────────────────
e.rep("const RIVCREST=[1,3,8,10];","""/* Emblèmes des concurrents : ajoutés après les douze du joueur, jamais proposés au choix. */
CRESTS.push(
 {nm:"Le pont-levis",a:'#E07A5F',b:'#F2CC8F',
  d:'<path d="M18 62V32H54V62" fill="none" stroke="$a" stroke-width="2.6" stroke-linejoin="round"/><path d="M26 62V46A10 10 0 0 1 46 46V62Z" fill="$b" opacity=".85"/><path d="M18 32 27 45M54 32 45 45" stroke="$a" stroke-width="1.6"/><path d="M14 32H58" stroke="$a" stroke-width="2"/>',
  m:'M3 21V7h18v14h-5v-6a4 4 0 0 0-8 0v6Z'},
 {nm:"Le médaillon",a:'#4FC3D9',b:'#E8D7A0',
  d:'<circle cx="36" cy="42" r="17" fill="none" stroke="$a" stroke-width="2.6"/><circle cx="36" cy="42" r="8" fill="$b"/><path d="M36 19V25M36 59V65M13 42H19M53 42H59" stroke="$a" stroke-width="2"/>',
  m:'M12 3a9 9 0 1 0 .01 0Zm0 5a4 4 0 1 1-.01 0Z'},
 {nm:"Le trident",a:'#B18CF0',b:'#F0E6FF',
  d:'<path d="M36 22V64M24 26V38C24 46 48 46 48 38V26" fill="none" stroke="$a" stroke-width="2.6" stroke-linecap="round"/><path d="M20 27 24 19 28 27ZM32 26 36 18 40 26ZM44 27 48 19 52 27Z" fill="$b"/>',
  m:'M11 22V12H8C6 12 5 10 5 8V3h2v5h2V3h2v6h2V3h2v5h2V3h2v5c0 2-1 4-3 4h-3v10Z'});
const NPC=12;   /* écussons proposés au joueur */
const RIVCREST=[12,13,14,13];   /* Pont-Levis, Médaillon, Citadelle (et un 4e pour les vieilles sauvegardes) */""")
e.rep("""<div class="crestrow" id="crests">${CRESTS.map((c,i)=>""","""<div class="crestrow" id="crests">${CRESTS.slice(0,NPC).map((c,i)=>""")

# ── 6. cartes en trois paliers ──────────────────────────────────────────────────
e.rep("function goldNext(){\n const b=GOLDQ.shift();if(!b){goldOn=false;return}",
      "function goldNext(){\n const b=GOLDQ.shift();if(!b){goldOn=false;return}\n const T=b.tier||'or',TN={bronze:'BRONZE',argent:'ARGENT',or:'OR'}[T]||'OR';")
e.rep("""el.innerHTML=`<div class="gcard" role="dialog" aria-label="${b.t}"><div class="gvis"><svg viewBox="0 0 96 96" aria-hidden="true">${GV[b.v]||GV.star}</svg></div>
  <div class="gkick">${b.k||'BONUS'}</div>""","""el.innerHTML=`<div class="gcard t-${T}" role="dialog" aria-label="${b.t}"><div class="gvis"><svg viewBox="0 0 96 96" aria-hidden="true">${(GV[b.v]||GV.star).replace(/#D9B06A/g,'var(--tc)').replace(/#F3D48C/g,'var(--tl)').replace(/rgba\\(217,176,106,/g,'rgba(var(--trgb),')}</svg></div>
  <div class="gtier">${TN}</div><div class="gkick">${b.k||'BONUS'}</div>""")
e.rep("@keyframes gpop{","""/* trois paliers : bronze, argent, or */
.gcard{--tc:#D9B06A;--tl:#F3D48C;--trgb:217,176,106}
.gcard.t-bronze{--tc:#C98B55;--tl:#E8B585;--trgb:201,139,85;border-color:#C98B55;box-shadow:0 0 0 1px rgba(201,139,85,.25),0 18px 60px rgba(0,0,0,.6),0 0 32px rgba(201,139,85,.22);
 background:radial-gradient(circle at 50% -10%,rgba(201,139,85,.30),rgba(19,25,37,0) 62%),#131925}
.gcard.t-argent{--tc:#C9D3DE;--tl:#F2F6FA;--trgb:201,211,222;border-color:#C9D3DE;box-shadow:0 0 0 1px rgba(201,211,222,.25),0 18px 60px rgba(0,0,0,.6),0 0 38px rgba(201,211,222,.24);
 background:radial-gradient(circle at 50% -10%,rgba(201,211,222,.28),rgba(19,25,37,0) 62%),#131925}
.gcard.t-or{border-width:2px;box-shadow:0 0 0 1px rgba(217,176,106,.35),0 18px 60px rgba(0,0,0,.6),0 0 60px rgba(217,176,106,.40)}
.gcard .gkick,.gcard .ggain{color:var(--tc)}
.gtier{display:inline-block;font-family:var(--mono);font-size:10px;letter-spacing:.2em;color:#0E1621;background:var(--tc);border-radius:3px;padding:2px 8px;margin-bottom:6px}
@keyframes gpop{""")
# paliers des cartes existantes
TIERS=[("k:'CROISSANCE · ENCOURS ×1,3',","bronze"),("k:'CROISSANCE · ENCOURS ×1,6',","argent"),("k:'CROISSANCE · ENCOURS ×2,2',","or"),
       ("k:'SÉRIE · CINQ TRIMESTRES POSITIFS',","argent"),("k:'TROPHÉE · EN TÊTE DE LA PLACE',","argent"),("k:`TROPHÉE · ANNÉE ${y}`,","or"),
       ("k:'INSTITUTIONNEL',","or"),("k:'INSTITUTIONNEL · QUATRE TRIMESTRES DANS LA BANDE',","argent"),
       ("k:'TALENT · RECHERCHE',","argent"),("k:'TALENT · DÉBAUCHAGE',","or"),("k:'INFORMATION',","argent"),
       ("k:'RECRUE DU TRIMESTRE',","bronze"),("k:'COMMISSION DE PERFORMANCE',","bronze"),("k:`CROISSANCE · ENCOURS ${mm(unlockNav(OPENRK))}`,","argent")]
for k,t in TIERS:
    n=e.s.count(k);assert n>=1,k
    e.s=e.s.replace(k,k+"tier:'%s',"%t)
# les deux cartes « RARE » : or
e.s=e.s.replace("k:'RARE',","k:'RARE',tier:'or',")
# objectif tenu : palier selon le bonus ; hauts faits : selon leur rang
e.rep("if(ok)goldLater({v:'trophy',k:'OBJECTIF DU TRIMESTRE',","if(ok)goldLater({v:'trophy',tier:(S.goal.b||0)>=0.09?'or':(S.goal.b||0)>=0.06?'argent':'bronze',k:'OBJECTIF DU TRIMESTRE',")
e.rep("const b={v:f.tier>=3?'crown':'trophy',","const b={v:f.tier>=3?'crown':'trophy',tier:f.tier>=4?'or':f.tier>=2?'argent':'bronze',")
# ouverture des exotiques : or, la première fois que vous finissez premier d'un trimestre
e.rep(" /* croissance : les marchés du rang suivant s'ouvrent quand l'encours franchit son seuil */",
""" if(!S.exoOpen&&S.rivals.every(r=>(r.last||0)<o.qTotal)){S.exoOpen=true;applyPools();
  const nx=INSTR.filter((x,i)=>x.grp==='Exotiques'&&mktOpen(i));
  goldLater({v:'rocket',tier:'or',k:'PREMIER DU TRIMESTRE',t:'Les marchés exotiques vous sont ouverts',d:"Vous avez battu toute la place : le comité vous confie les marchés que personne ne sait gérer.",g:nx.map(x=>`${x.sym} · ${x.nm.toLowerCase()}`).join('<br>')})}
 /* croissance : les marchés du rang suivant s'ouvrent quand l'encours franchit son seuil */""")

# ── sauvegardes d'avant le lot 49 ──────────────────────────────────────────────
e.rep("  if(S.openRk)OPENRK=S.openRk;\n  applyPools();",
      "  if(S.openRk)OPENRK=S.openRk;\n"
      "  else if(S.aum0>=0.5)OPENRK=S.aum0>=5?5:4;   /* full-floor et mastodonte d'avant le lot 49 */\n"
      "  if(S.exoOpen===undefined)S.exoOpen=(S.univ==='ext');   /* l'univers « monde entier » les avait d'emblée */\n"
      "  applyPools();")
e.rep(" vol='std';univ='ext';   /* lot 49"," vol='std';univ='ext';S=null;   /* lot 49")
e.rep("qtot:D.q,tuto:TUTO?0:99,q:0,","qtot:D.q,tuto:TUTO?0:99,exoOpen:false,q:0,")
e.rep("size:{small:'🏠',mid:'🏢',mega:'🏙️'}","size:{small:'🎯',mid:'⚔️',mega:'🔥'}")
e.done("lot 49 — difficulte, marches a gagner, score en dollars, flux par concurrent, emblemes, paliers")
