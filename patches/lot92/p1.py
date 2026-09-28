# Lot 92 : budget en deux postes (front office 7 crans, back office 5 crans) et équipe nommée.
# Front office cran n = anciens tableaux salle/recherche au cran n ; back office → BOMAP vers l'ancien contrôle.
# Classe sans trader : commission et impact ×1,5. Licenciement avec indemnités (dans la limite de la caisse),
# débauchage nominatif (siège vide un trimestre, contre-offre possible).
import re
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)

# --- définition des postes
i=s.find('const BUDGET=[');j=s.find('];',i)+2
NEWB=r'''/* lot 92 : deux postes. Front office cran n = anciens tableaux salle + recherche au cran n ;
   back office cran n = ancien contrôle des risques au cran BOMAP[n]. Les crans sont cumulatifs. */
const FOP=[
 {who:"Jean-Kevin",full:"Jean-Kevin Lévêque-Charbonnier",role:"analyste macro junior, à tout faire",ic:"🐣",bp:0},
 {who:"Dwight",full:"Dwight Tannenbaum",role:"trader actions, exécution et algorithmes",ic:"🤖",bp:10,cls:'Actions'},
 {who:"Ingrid",full:"Ingrid Bergström",role:"cheffe du desk taux, la plus senior",ic:"🏦",bp:25,cls:'Taux'},
 {who:"Boris",full:"Boris Rasoumovsky",role:"trader devises, exécution à la voix",ic:"📞",bp:50,cls:'Devises'},
 {who:"Tuco",full:"Bartolomeo « Tuco » Ossobuco",role:"trader matières premières",ic:"🛢️",bp:100,cls:'Matières premières'},
 {who:"Winnie",full:"Wing-Fat « Winnie » Leung",role:"trader exotiques",ic:"🐉",bp:200,cls:'Exotiques'},
 {who:"Sœur Marie-Alpha",full:"Sœur Marie-Alpha",role:"stratégiste quantitative, recherche",ic:"📿",bp:400}];
const BOP=[
 {who:"Le loyer",full:"Le loyer",role:"bureaux, écrans, électricité",ic:"🏢",bp:5},
 {who:"Maître Lettrage",full:"Maître Ghislain Lettrage",role:"expert-comptable",ic:"🧮",bp:15},
 {who:"Josiane Suspens",full:"Josiane Suspens",role:"responsable du back office",ic:"🗂️",bp:30},
 {who:"Mireille",full:"Mireille Cauchemar",role:"directrice des risques",ic:"⚖️",bp:50},
 {who:"L'inspecteur Tatillon",full:"L'inspecteur Firmin Tatillon",role:"conformité et audit interne",ic:"🔎",bp:75}];
const BOMAP=[0,3,4,5,6],NOTRD=1.5,TRD={'Actions':1,'Taux':2,'Devises':3,'Matières premières':4,'Exotiques':5};
const BUDGET=[
 {id:'fo',ico:'📈',nm:"Front office",
  d:"Les traders et la recherche. Chaque recrue améliore l'avis du desk sur toutes les classes et sur la macro : coûts d'exécution, bruit des indicateurs, nombre et fiabilité des sources, lecture des dépêches, résistance au débauchage. Un trader couvre en plus sa classe : sans lui, vos ordres y passent par un courtier, commission et impact de marché ×1,5.",
  lv:FOP.map(p=>Object.assign({nm:p.who},p))},
 {id:'bo',ico:'⚖️',nm:"Back office",
  d:"Le loyer, la comptabilité, les opérations, le contrôle des risques et la conformité. Un back office sérieux évite les incidents, rend les accidents de levier plus rares et apaise le comité.",
  lv:BOP.map(p=>Object.assign({nm:p.who},p))}
];
function syncBud(){if(!S||!S.bud)return;S.bud.exec=S.bud.res=S.bud.ret=S.bud.fo;S.bud.risk=BOMAP[S.bud.bo]}
function here(p){return !!(S&&S.bud)&&S.bud.fo>=p&&!(S.gone&&S.gone.p===p&&S.gone.n===0)}
function covered(g){const p=TRD[g];return p===undefined||here(p)}
function cntOn(){return S&&S.cntQ===S.q?(S.cntBp||0):0}
function sevRaw(){const P=S.budPrev;if(!P)return 0;return BUDGET.reduce((a,b)=>a+Math.max(0,b.lv[P[b.id]].bp-b.lv[S.bud[b.id]].bp),0)}
/* budget du trimestre + indemnités, plafonnées à ce qui reste en caisse : baisser un cran ne bloque jamais */
function setOps(){S.mgrCosts-=S.qOps||0;S.cOps=(S.cOps||0)-(S.qOps||0);const purse=mgrCash(),b=budgetBp()*1e-4*S.nav;
 S.qSevM=Math.min(sevRaw()*1e-4*S.nav,Math.max(0,purse-b));S.qOps=b+S.qSevM;S.mgrCosts+=S.qOps;S.cOps+=S.qOps}
function covTxt(){const op=GRP.filter(g=>g!=='Exotiques'||S.exoOpen),c=op.filter(covered),u=op.filter(g=>!covered(g));
 return `<br>Classes couvertes : ${c.map(g=>g.toLowerCase()).join(', ')||'aucune'}${u.length?` · <span class="neg-g">sans trader, courtier ×${dec(NOTRD,1)}</span> : ${u.map(g=>g.toLowerCase()).join(', ')}`:''}`}'''
s=s[:i]+NEWB+s[j:]
rep("const DESKS=[{id:'inhouse',nm:\"Desk d'exécution intégré\",mult:()=>1.00,fixed:0.0005,poachPain:1.4}];",
    "const DESKS=[{id:'inhouse',nm:\"Desk d'exécution intégré\",mult:()=>1.00,fixed:0,poachPain:1.4}];   /* lot 92 : les 5 pb de base sont le loyer du back office */")
# effets affichés
rep('function budEf(id,i){','function budEf0(id,i){')
rep('function budExpl(id){const i=S.bud[id];','''function budEf(id,i){if(id==='fo')return budEf0('exec',i)+' · '+budEf0('res',i);if(id==='bo')return budEf0('risk',BOMAP[i]);return budEf0(id,i)}
function budExpl(id){if(id==='fo')return budExpl0('exec',S.bud.fo)+budExpl0('res',S.bud.fo);if(id==='bo')return budExpl0('risk',BOMAP[S.bud.bo]);return budExpl0(id,S.bud[id])}
function budExpl0(id,i){''')
rep("function budgetBp(){return BUDGET.reduce((a,b)=>a+b.lv[S.bud[b.id]].bp,0)+DESK().fixed*1e4}","function budgetBp(){return BUDGET.reduce((a,b)=>a+b.lv[S.bud[b.id]].bp,0)+DESK().fixed*1e4+cntOn()}")
rep("function budgetBpIf(id,lv){return BUDGET.reduce((a,b)=>a+b.lv[b.id===id?lv:S.bud[b.id]].bp,0)+DESK().fixed*1e4}","function budgetBpIf(id,lv){return BUDGET.reduce((a,b)=>a+b.lv[b.id===id?lv:S.bud[b.id]].bp,0)+DESK().fixed*1e4+cntOn()}")
# concurrents : ancien barème figé (3 postes + 5 pb)
rep("function rivalCostQ(rv){const L=(rv&&rv.bl)||3;return (BUDGET.reduce((a,b)=>a+b.lv[L].bp,0)+DESK().fixed*1e4+16)*1e-4}",
    "const RIVBP=[15,18,31,53,119,233,419];   /* lot 92 : ancien barème des concurrents, figé */\nfunction rivalCostQ(rv){const L=(rv&&rv.bl)||3;return (RIVBP[L]+16)*1e-4}")
# état initial et reprise
rep("bud:{exec:3,risk:3,res:3,ret:3},budN:7","bud:{fo:3,bo:1,exec:3,risk:3,res:3,ret:3},budN:7")
rep("S.bud[k]=M11[S.bud[k]]!==undefined?M11[S.bud[k]]:3;S.budN=7}","""S.bud[k]=M11[S.bud[k]]!==undefined?M11[S.bud[k]]:3;S.budN=7}
  if(S.bud&&S.bud.fo===undefined){const r=S.bud.risk!==undefined?S.bud.risk:3;S.bud.fo=Math.round(((S.bud.exec||0)+(S.bud.res||0))/2);let bj=0;BOMAP.forEach((v,j)=>{if(Math.abs(v-r)<Math.abs(BOMAP[bj]-r))bj=j});S.bud.bo=bj;syncBud()}   /* lot 92 */""")
# ouverture de trimestre : siège vide, contre-offre
rep("S.pendingTC=0;S.freeAdjUsed=false;S.live=false;S.execSlipQ=0;","S.pendingTC=0;S.freeAdjUsed=false;S.live=false;S.execSlipQ=0;if(S.gone){if(S.gone.n>0)S.gone.n=0;else S.gone=null}S.cntBp=0;S.qSevM=0;")
# coûts : classe sans trader
rep("if((S.stars||[]).includes(INSTR[i].grp))m*=0.5;","if((S.stars||[]).includes(INSTR[i].grp))m*=0.5;\n if(!covered(x.grp))m*=NOTRD;   /* lot 92 : sans trader, le courtier */")
# en-tête de classe dans le book
rep('<span>${g.toUpperCase()}</span></div>`;','<span>${g.toUpperCase()}</span>${(g!==\'Exotiques\'||S.exoOpen)&&!covered(g)?`<span class="nocov">sans trader · courtier ×${dec(NOTRD,1)}</span>`:\'\'}</div>`;')
# écran du budget : réduction forcée
o=s[s.find("{const purse=mgrCash(),fits=()=>budgetBp()*1e-4*S.nav<=purse+1e-12;"):]
o=o[:o.find("drawBuds();drawColl();")]
n="""{const purse=mgrCash(),fits=()=>budgetBp()*1e-4*S.nav<=purse+1e-12;
  if(redOn('budget')&&S.bud.bo<3){for(let l=3;l>S.bud.bo;l--){const o=S.bud.bo;S.bud.bo=l;if(fits())break;S.bud.bo=o}}
  for(let g=0;g<40&&!fits();g++){let bi=null,bv=0;BUDGET.forEach(b=>{const l=S.bud[b.id];if(l>(redOn('budget')&&b.id==='bo'?3:0)&&b.lv[l].bp>bv){bv=b.lv[l].bp;bi=b.id}});
   if(!bi)break;S.bud[bi]--}syncBud()}
 setOps();
"""+o[o.find(" app.innerHTML=statusBar()"):]
rep(o,n)
rep("S.budBp=bp;","S.budBp=bp;S.budPrev={fo:S.bud.fo,bo:S.bud.bo};")
# drawBuds
i=s.find('function drawBuds(){');j=s.find('/* ---------- positionnement',i)
NEWD=r'''function drawBuds(){
 /* caisse avant le budget de ce trimestre : un niveau qui la dépasse est verrouillé */
 const purse=mgrCash()+(S.qOps||0);
 setTimeout(budRest,0);
 const ok=(id,i)=>(i===0||budgetBpIf(id,i)*1e-4*S.nav<=purse)&&!(id==='bo'&&redOn('budget')&&i<3&&i<S.bud.bo);
 const G=S.gone&&S.gone.n===0&&S.bud.fo>=S.gone.p?S.gone:null,cb=G?FOP[G.p].bp-FOP[G.p-1].bp:0,cok=G&&(budgetBp()+cb)*1e-4*S.nav<=purse;
 document.getElementById('buds').innerHTML=BUDGET.map(b=>{const cur=S.bud[b.id];return `<div class="brow">
   <div class="bh"><b><span class="bico">${b.ico}</span>${b.nm}</b><span>${b.lv[cur].bp} pb · ${mm(b.lv[cur].bp*1e-4*S.nav)}</span></div>
   <p class="note" style="margin:2px 0 6px">${b.id==='fo'?`Touchez une personne : l'équipe va jusqu'à elle. Le prix est celui de toute l'équipe.`:`Touchez un poste : le back office va jusqu'à lui.`}</p>
   <div class="team">${b.lv.map((l,i)=>{const gone=b.id==='fo'&&G&&G.p===i,o=ok(b.id,i);
    return `<button class="lvl tm ${i<=cur?'in':''} ${cur===i?'on':''}${gone?' gone':''}" data-b="${b.id}" data-i="${i}"${o?'':' disabled'}><span class="tic">${l.ic}</span><span class="tnm"><b>${l.full}</b><i>${gone?`parti chez ${G.boss}`:l.role}</i></span><span class="tbp">${l.bp} pb<br>${o?mm(l.bp*1e-4*S.nav):'hors caisse'}</span></button>`}).join('')}</div>
   ${b.id==='fo'&&G?`<div class="flag" style="margin:8px 0 0"><span><b>${FOP[G.p].who} est parti chez ${G.boss}.</b> Son siège reste vide ce trimestre${FOP[G.p].cls?` : la classe ${FOP[G.p].cls.toLowerCase()} passe par un courtier`:''}. Contre-offre : un trimestre de son salaire, ${cb} pb (${mm(cb*1e-4*S.nav)}), et il revient tout de suite.</span></div><button class="lvl cntb" id="cnt"${cok?'':' disabled'}>Faire la contre-offre · ${mm(cb*1e-4*S.nav)}</button>`:''}
   <div class="lvef">${budEf(b.id,cur)}${b.id==='fo'?covTxt():''}</div>
   <details style="margin-top:8px"><summary>À quoi sert ce budget · les ${b.lv.length} crans</summary><p class="note">${b.d}</p>${budExpl(b.id)}<ul class="efl">${b.lv.map((l,i)=>`<li><b>${l.who}</b> · ${l.bp} pb · ${budEf(b.id,i)}</li>`).join('')}</ul></details></div>`}).join('');
 const bp=budgetBp();
 document.getElementById('btot').textContent=`${bp.toFixed(0)} pb · ${mm(bp*1e-4*S.nav)} · ${dec((bp*4/100),1)} % par an${S.qSevM>0?` · indemnités ${mm(S.qSevM)}`:''}`;
 {const t=document.getElementById('btre');if(t){const v=mgrCash();t.textContent=mm(v);t.className=v>=0?'':'neg-g'}}
 const cn=document.getElementById('cnt');if(cn)cn.onclick=()=>{S.cntBp=cb;S.cntQ=S.q;const w=FOP[G.p].who;S.gone=null;setOps();drawBuds();refreshStatus();toast(`Contre-offre acceptée : <b>${w}</b> reste chez vous (${mm(cb*1e-4*S.nav)}).`)};
 app.querySelectorAll('.lvl.tm').forEach(x=>x.onclick=()=>{
  const id=x.dataset.b,i1=+x.dataset.i,i0=S.bud[id],bb=BUDGET.find(q=>q.id===id);if(i1===i0)return;
  const b0=budgetBp();S.bud[id]=i1;syncBud();setOps();drawBuds();refreshStatus();
  const b1=budgetBp(),who=i1>i0?bb.lv.slice(i0+1,i1+1):bb.lv.slice(i1+1,i0+1);
  toast(`${i1>i0?'Recrutement':'Départ'} : <b>${who.map(l=>l.who).join(', ')}</b>${i1<i0&&S.qSevM>0?` · indemnités ${mm(S.qSevM)}`:''} · ${bb.nm} ${b0.toFixed(0)} → <b>${b1.toFixed(0)} pb</b> (${(b1-b0)>=0?'+':'−'}${mm(Math.abs((b1-b0)*1e-4*S.nav))})`);
 });
}

'''
s=s[:i]+NEWD+s[j:]
rep(".lvls{display:grid;grid-template-columns:repeat(7,1fr);gap:3px}",".lvls{display:grid;grid-template-columns:repeat(7,1fr);gap:3px}\n.team{display:flex;flex-direction:column;gap:3px}.lvl.tm{display:flex;align-items:center;gap:9px;text-align:left;padding:6px 9px;width:100%}.lvl.tm:not(.in){opacity:.5}.lvl.tm.gone{opacity:.6}.lvl.tm.gone b{text-decoration:line-through}\n.tm .tic{font-size:19px;width:24px;text-align:center}.tm .tnm{flex:1;display:flex;flex-direction:column;min-width:0}.tm .tnm i{font-style:normal;font-size:11px;color:var(--dim)}.tm .tbp{font-family:var(--mono);font-size:10.5px;text-align:right;color:var(--dim);white-space:nowrap}\n.lvl.cntb{width:100%;margin-top:6px;padding:8px}.sect .nocov{margin-left:auto;color:var(--short);font-size:10px}")
# débauchage nominatif
rep("{S.execPenalty*=1.14;S.poachMsg+=` ${(pick(S.rivals.filter(x=>x.poacher))||S.rivals[S.rivals.length-1]).boss} a débauché deux de vos gérants : coûts d'exécution +14 % durablement.`;",
    "{S.execPenalty*=1.14;const boss=(pick(S.rivals.filter(x=>x.poacher))||S.rivals[S.rivals.length-1]).boss,cands=[];for(let p=1;p<=S.bud.fo;p++)if(here(p))cands.push(p);\n  if(cands.length){const p=pk(cands,92);S.gone={p,n:1,boss};S.poachMsg+=` ${boss} a débauché ${FOP[p].full} : coûts d'exécution +14 % durablement, et son siège reste vide au trimestre prochain${FOP[p].cls?` (${FOP[p].cls.toLowerCase()} par un courtier, ×${dec(NOTRD,1)})`:''}, sauf contre-offre.`}\n  else S.poachMsg+=` ${boss} a débauché deux de vos gérants : coûts d'exécution +14 % durablement.`;")
# textes
rep("budget contrôle « ${BUDGET[1].lv[S.bud.risk].nm.toLowerCase()} »","back office « ${BUDGET[1].lv[S.bud.bo].who} »")
rep("{id:'budget',nm:'Contrôle imposé',t:'budget de contrôle des risques au cran 5 au moins, à vos frais'}","{id:'budget',nm:'Contrôle imposé',t:'Mireille au back office au moins, à vos frais'}")
rep("la recherche macro au cran « Renforcé » ou au-delà","le front office jusqu'à Winnie au moins",2)
rep("la salle de marché au cran « Renforcé » ou au-delà","le front office jusqu'à Winnie au moins")
rep("la recherche macro au minimum","Jean-Kevin seul au front office",2)
rep("les trois budgets au minimum","les deux budgets au minimum")
open('index.html','w',encoding='utf-8').write(s);print('ok')
