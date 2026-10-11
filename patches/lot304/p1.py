p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# 1. modèle : une case par personne ; les crans deviennent le niveau équivalent de la masse salariale
rep("""function syncBud(){if(!S||!S.bud)return;S.bud.exec""","""/* lot 304 : l'équipe se compose personne par personne. Salaire propre = écart avec le cran d'avant de la grille.
   Effets individuels (classe couverte, pouvoirs, avantages) : présence. Effets d'ensemble (coûts, sources, incidents) :
   niveau équivalent = le cran le plus haut que la masse salariale paierait sur l'ancienne échelle. Le loyer et Jean-Kevin restent d'office. */
function salP(L,p){return p>0?L[p].bp-L[p-1].bp:0}
function teamL(id){return id==='fo'?FOP:BOP}
function teamInit(){if(!S.team){const f=(S.bud&&S.bud.fo)||0,b=(S.bud&&S.bud.bo)||0;S.team={fo:FOP.map((x,p)=>p===0||p<=f),bo:BOP.map((x,p)=>p===0||p<=b)};
  if(!S.teamPrev&&S.budPrev)S.teamPrev={fo:FOP.map((x,p)=>p===0||p<=S.budPrev.fo),bo:BOP.map((x,p)=>p===0||p<=S.budPrev.bo)}}return S.team}   /* sauvegardes d'avant le lot 304 */
function hired(id,p){return !!teamInit()[id][p]}
function massBp(id,T){T=T||teamInit();const L=teamL(id);let m=0;L.forEach((x,p)=>{if(T[id][p])m+=salP(L,p)});return m}
function eqLvl(id,m){const L=teamL(id);let n=0;for(let p=0;p<L.length;p++)if(L[p].bp<=m+1e-9)n=p;return n}
function teamCopy(T){T=T||teamInit();return {fo:[...T.fo],bo:[...T.bo]}}
function ladderT(id,j,T){const C=teamCopy(T);C[id]=teamL(id).map((x,p)=>p===0||(p<=j&&!(id==='fo'&&goneP(p))));return C}   /* les partis ne reviennent que sur contre-offre */
function teamLadder(id,j){S.team=ladderT(id,j);syncBud();setOps()}
function teamIsLadder(id,j){const T=teamInit(),L=ladderT(id,j);return teamL(id).every((x,p)=>!!T[id][p]===!!L[id][p])}
function goneP(p){return gonesL().some(g=>g.p===p)}
/* recrutement et licenciement : un demi-trimestre du salaire de la personne */
function hireRaw(T){T=T||teamInit();const P=S.teamPrev;let m=0;['fo','bo'].forEach(id=>teamL(id).forEach((x,p)=>{if(p>0&&T[id][p]&&!(P&&P[id][p]))m+=0.5*salP(teamL(id),p)}));return m}
function sevRawT(T){T=T||teamInit();const P=S.teamPrev;if(!P)return 0;let m=0;['fo','bo'].forEach(id=>teamL(id).forEach((x,p)=>{if(p>0&&P[id][p]&&!T[id][p]&&!(id==='fo'&&goneP(p)))m+=0.5*salP(teamL(id),p)}));return m}
function budgetBpT(T){return teamBp(massBp('fo',T)+massBp('bo',T))+DESK().fixed*1e4+cntOn()+offBp()}
function opsT(T){return (budgetBpT(T)+hireRaw(T)+sevRawT(T))*1e-4*budNav()}
function opsLadder(id,j){return opsT(ladderT(id,j))}
function teamLadderSub(id,j){const P=S.teamPrev;if(!P)return false;return teamL(id).every((x,p)=>!(p===0||p<=j)||p===0||P[id][p])}
function syncBud(){if(!S||!S.bud)return;teamInit();S.bud.fo=eqLvl('fo',massBp('fo'));S.bud.bo=eqLvl('bo',massBp('bo'));S.bud.exec""")
rep("""function here(p){return !!(S&&S.bud)&&S.bud.fo>=p&&!gonesL().some(g=>g.p===p&&g.n===0)}""",
    """function here(p){return !!(S&&S.bud)&&hired('fo',p)&&!gonesL().some(g=>g.p===p&&g.n===0)}   /* lot 304 : présence */""")
rep("""on:()=>S.bud.bo>=4,sub:()=>S.bud.bo>=2?'Josiane Suspens':'Gontran Report-à-Nouveau'}];""","""on:()=>boH(4),sub:()=>boH(2)?'Josiane Suspens':'Gontran Report-à-Nouveau'}];""")
rep("""function bonBase(){if(!S||!S.bud)return 0;const p=Math.min(S.bud.fo,FOP.length-1);return p>=0?5*FOP[p].bp*1e-4:0}""",
    """function bonBase(){if(!S||!S.bud)return 0;return 5*massBp('fo')*1e-4}   /* lot 304 : masse salariale du front office */""")
rep("""function boH(n){return !!(S&&S.bud&&S.bud.bo>=n)}""","""function boH(n){return !!(S&&S.bud)&&hired('bo',n)}   /* lot 304 : la personne est là */""")
rep("""function sevRaw(){const P=S.budPrev;if(!P)return 0;return 0.5*BUDGET.reduce((a,b)=>a+Math.max(0,b.lv[P[b.id]].bp-b.lv[S.bud[b.id]].bp),0)}""",
    """function sevRaw(){return sevRawT()}   /* lot 304 : par personne */""")
rep("""function setOps(){S.mgrCosts-=S.qOps||0;S.cOps=(S.cOps||0)-(S.qOps||0);const purse=mgrCash(),b=budgetBp()*1e-4*budNav();
 S.qSevM=Math.min(sevRaw()*1e-4*budNav(),Math.max(0,purse-b));S.qOps=b+S.qSevM;S.mgrCosts+=S.qOps;S.cOps+=S.qOps}""",
"""function setOps(){S.mgrCosts-=S.qOps||0;S.cOps=(S.cOps||0)-(S.qOps||0);const purse=mgrCash(),b=budgetBp()*1e-4*budNav();
 S.qSevM=Math.min(sevRaw()*1e-4*budNav(),Math.max(0,purse-b));S.qHireM=Math.min(hireRaw()*1e-4*budNav(),Math.max(0,purse-b-S.qSevM));S.qOps=b+S.qSevM+S.qHireM;S.mgrCosts+=S.qOps;S.cOps+=S.qOps}   /* lot 304 : recrutements */""")
rep("""function budEf(id,i){const X=L=>L.slice(0,i+1).filter(l=>l.pw).map(l=>`<br>${l.ic} <b>${l.who}</b> : ${l.pw}`).join('');""",
    """function budEf(id,i,one){const X=L=>L.filter((l,p)=>one!=null?p===one:hired(id,p)).filter(l=>l.pw).map(l=>`<br>${l.ic} <b>${l.who}</b> : ${l.pw}`).join('');   /* lot 304 : pouvoirs des présents */""")
rep("""function budgetBp(){return teamBp(BUDGET.reduce((a,b)=>a+b.lv[S.bud[b.id]].bp,0))+DESK().fixed*1e4+cntOn()+offBp()}""",
    """function budgetBp(){return budgetBpT()}   /* lot 304 : masse salariale de l'équipe choisie */""")
rep("""function budgetBpIf(id,lv){return teamBp(BUDGET.reduce((a,b)=>a+b.lv[b.id===id?lv:S.bud[b.id]].bp,0))+DESK().fixed*1e4+cntOn()+offBp()}""",
    """function budgetBpIf(id,lv){return budgetBpT(ladderT(id,lv))}   /* l'échelle jusqu'au cran lv */""")
rep("""const b=BUDGET.map(bb=>[bb.nm+' · '+bb.lv[S.bud[bb.id]].nm,bb.lv[S.bud[bb.id]].bp+' pb','',bb.lv[S.bud[bb.id]].bp*1e-4*S.nav]);""",
    """const b=BUDGET.map(bb=>[bb.nm+' · '+teamInit()[bb.id].filter((x,p)=>x&&p>0).length+' personnes',massBp(bb.id)+' pb','',massBp(bb.id)*1e-4*S.nav]);""")
# 2. ouverture de l'écran : carton rouge et caisse insuffisante, personne par personne
rep("""  if(redOn('budget')&&S.bud.bo<3){for(let l=3;l>S.bud.bo;l--){const o=S.bud.bo;S.bud.bo=l;if(fits())break;S.bud.bo=o}}
  for(let g=0;g<40&&!fits()&&!S.budPrev;g++){let bi=null,bv=0;BUDGET.forEach(b=>{const l=S.bud[b.id];if(l>(redOn('budget')&&b.id==='bo'?3:0)&&b.lv[l].bp>bv){bv=b.lv[l].bp;bi=b.id}});
   if(!bi)break;S.bud[bi]--}syncBud()}""",
"""  teamInit();if(redOn('budget'))for(let p=1;p<=3;p++)S.team.bo[p]=true;   /* lot 304 : le comité impose les trois premiers postes */
  gonesL().forEach(g=>{if(g.n===0)S.team.fo[g.p]=false});   /* un trader débauché quitte l'équipe : plus de salaire, pas d'indemnité */
  for(let g=0;g<40&&!fits()&&!S.teamPrev;g++){let bi=null,bp=-1,bv=0;['fo','bo'].forEach(id=>teamL(id).forEach((x,p)=>{if(p>0&&S.team[id][p]&&!(id==='bo'&&redOn('budget')&&p<=3)&&salP(teamL(id),p)>bv){bv=salP(teamL(id),p);bi=id;bp=p}}));
   if(!bi)break;S.team[bi][bp]=false}syncBud()}""")
rep("""S.budBp=bp;S.budPrev={fo:S.bud.fo,bo:S.bud.bo};""","""S.budBp=bp;S.budPrev={fo:S.bud.fo,bo:S.bud.bo};S.teamPrev=teamCopy();   /* lot 304 */""")
# 3. l'écran : une case par personne
rep(""" const ok=(id,i)=>(i===0||(S.budPrev&&i<=S.budPrev[id])||budgetBpIf(id,i)*1e-4*budNav()<=purse)&&!(id==='bo'&&redOn('budget')&&i<3&&i<S.bud.bo);
 const GL=gonesL().filter(g=>g.n===0&&S.bud.fo>=g.p),cok=g=>(budgetBp()+cntCost(g.p))*1e-4*budNav()<=purse;""",
""" const tog=(id,p)=>{const T=teamCopy();T[id][p]=!T[id][p];return T},lock=(id,p)=>p===0||(id==='bo'&&redOn('budget')&&p<=3)||(id==='fo'&&goneP(p));
 const ok=(id,p)=>!lock(id,p)&&(hired(id,p)||opsT(tog(id,p))<=purse+1e-12);   /* lot 304 : on peut toujours se séparer de quelqu'un */
 const GL=gonesL().filter(g=>g.n===0),cok=g=>(budgetBp()+cntCost(g.p))*1e-4*budNav()<=purse;""")
rep(""" document.getElementById('buds').innerHTML=BUDGET.map(b=>{const cur=S.bud[b.id];return `<div class="brow">
   <div class="bh"><b><span class="bico">${b.ico}</span>${b.nm}</b><span>${mm(b.lv[cur].bp*1e-4*budNav())} · ${(b.lv[cur].bp*1e-4*budNav()/Math.max(1e-9,S.nav)*1e4).toFixed(0)} pb</span></div>""",
""" const P=S.teamPrev;
 document.getElementById('buds').innerHTML=BUDGET.map(b=>{const cur=S.bud[b.id],ms=massBp(b.id),nx=b.lv[cur+1];return `<div class="brow">
   <div class="bh"><b><span class="bico">${b.ico}</span>${b.nm}</b><span>${mm(ms*1e-4*budNav())} · ${(ms*1e-4*budNav()/Math.max(1e-9,S.nav)*1e4).toFixed(0)} pb</span></div>
   <p class="note" style="margin:2px 0 4px">Niveau équivalent : <b>${b.lv[cur].who}</b>${nx?` · encore ${m3((nx.bp-ms)*1e-4*budNav())} de masse salariale pour le niveau ${nx.who}`:''}.</p>""")
rep("""${b.id==='fo'?`Touchez une personne : l'équipe va jusqu'à elle. Le prix est celui de toute l'équipe.`:`Touchez un poste : le back office va jusqu'à lui.`} ${S.budPrev&&S.budPrev[b.id]>0?`<b class="neg-g">Ne pas sélectionner, c'est licencier : chaque partant touche son bonus de départ, un demi-trimestre de salaire.</b>`:''}${b.id==='bo'&&redOn('budget')?` <b class="neg-g">Carton rouge : le comité vous interdit de descendre le back office sous ${BOP[3].who}.</b>`:''}</p>""",
    """Touchez une personne pour la recruter ou vous en séparer${b.id==='bo'?' ; sans personne, il reste le loyer':''}. Ce qu'elle apporte en propre n'existe que si elle est là ; les effets d'ensemble suivent la masse salariale. Recruter ou licencier coûte un demi-trimestre de son salaire.${b.id==='bo'&&redOn('budget')?` <b class="neg-g">Carton rouge : le comité impose ${BOP[1].who}, ${BOP[2].who} et ${BOP[3].who}.</b>`:''}</p>""")
rep("""   <div class="team">${b.lv.map((l,i)=>{const gone=b.id==='fo'&&GL.some(g=>g.p===i),o=ok(b.id,i);
    return `<button class="lvl tm ${i<=cur?'in':''} ${cur===i?'on':''}${gone?' gone':''}" data-b="${b.id}" data-i="${i}"${o?'':' disabled'}><span class="tic">${l.ic}</span><span class="tnm"><b>${l.full}</b><i>${gone?`parti${eF(i)} chez ${GL.find(g=>g.p===i).boss}`:l.role}</i></span><span class="tbp">${i>0?'+'+m3((l.bp-b.lv[i-1].bp)*1e-4*budNav()):'—'}<br>${o?'équipe '+m3(l.bp*1e-4*budNav()):(b.id==='bo'&&redOn('budget')&&i<3?'<span class="hx">interdit : carton rouge</span>':'<span class="hx">hors trésorerie</span>')}${S.budPrev&&i<S.budPrev[b.id]?`<br><span class="neg-g">départs −${m3(0.5*(b.lv[S.budPrev[b.id]].bp-l.bp)*1e-4*budNav())}</span>`:''}</span></button>`}).join('')}</div>""",
"""   <div class="team">${b.lv.map((l,i)=>{const gone=b.id==='fo'&&GL.some(g=>g.p===i),o=ok(b.id,i),h=hired(b.id,i),sal=salP(b.lv,i)*1e-4*budNav(),was=!!(P&&P[b.id][i]);
    return `<button class="lvl tm ${h?'in on':''}${gone?' gone':''}" data-b="${b.id}" data-i="${i}"${o?'':' disabled'}><span class="tic">${l.ic}</span><span class="tnm"><b>${l.full}</b><i>${gone?`parti${eF(i)} chez ${GL.find(g=>g.p===i).boss}`:l.role}</i></span><span class="tbp">${i>0?m3(sal):'—'}<br>${i===0?'<span class="hx">d\\'office</span>':lock(b.id,i)?'<span class="hx">imposé : carton rouge</span>':h?(was?'<span class="hx">en poste</span>':`<span class="neg-g">embauche −${m3(0.5*sal)}</span>`):(was&&!gone?`<span class="neg-g">départ −${m3(0.5*sal)}</span>`:o?'recruter':'<span class="hx">hors trésorerie</span>')}</span></button>`}).join('')}</div>""")
rep("""<ul class="efl">${b.lv.map((l,i)=>`<li><b>${l.who}</b> · ${mm(l.bp*1e-4*budNav())} · ${budEf(b.id,i)}</li>`).join('')}</ul></details></div>`}).join('');""",
    """<ul class="efl">${b.lv.map((l,i)=>`<li><b>${l.who}</b> · salaire ${mm(salP(b.lv,i)*1e-4*budNav())} · niveau ${l.who} à partir de ${mm(l.bp*1e-4*budNav())} de masse salariale : ${budEf(b.id,i,i)}</li>`).join('')}</ul></details></div>`}).join('');""")
rep("""document.getElementById('btot').textContent=`${mm(c)} · ${(c/nv*1e4).toFixed(0)} pb de l'encours ce trimestre · ${dec(c*4/nv*100,1)} % par an${S.qSevM>0?` · dont bonus versés aux partants ${mm(S.qSevM)}`:''}`}""",
    """document.getElementById('btot').textContent=`${mm(c+(S.qHireM||0))} · ${((c+(S.qHireM||0))/nv*1e4).toFixed(0)} pb de l'encours ce trimestre · ${dec(c*4/nv*100,1)} % par an${S.qSevM>0?` · dont indemnités de départ ${mm(S.qSevM)}`:''}${S.qHireM>0?` · dont frais d'embauche ${mm(S.qHireM)}`:''}`}""")
rep(""" app.querySelectorAll('.lvl.tm').forEach(x=>x.onclick=()=>{
  const id=x.dataset.b,i1=+x.dataset.i,i0=S.bud[id],bb=BUDGET.find(q=>q.id===id);if(i1===i0)return;
  const b0=budgetBp();S.bud[id]=i1;syncBud();setOps();drawBuds();refreshStatus();
  const b1=budgetBp(),who=i1>i0?bb.lv.slice(i0+1,i1+1):bb.lv.slice(i1+1,i0+1);
  const fired=i1<i0&&S.budPrev&&i1<S.budPrev[id];
  toast(`${i1>i0?'Recrutement':fired?'Départ':'Sélection retirée'} : <b>${who.map(l=>l.who).join(', ')}</b>${i1>i0&&who.length===1&&who[0].hi?` — « ${who[0].hi} »`:''}${fired&&S.qSevM>0?` · versement du bonus de départ ${mm(S.qSevM)}`:''} · ${bb.nm} ${b0.toFixed(0)} → <b>${b1.toFixed(0)} pb</b> (${(b1-b0)>=0?'+':'−'}${mm(Math.abs((b1-b0)*1e-4*budNav()))})`);
 });""",
""" app.querySelectorAll('.lvl.tm').forEach(x=>x.onclick=()=>{
  const id=x.dataset.b,p=+x.dataset.i,bb=BUDGET.find(q=>q.id===id),l=bb.lv[p];if(x.disabled||p===0)return;
  const b0=budgetBp(),on=!hired(id,p);S.team[id][p]=on;syncBud();setOps();drawBuds();refreshStatus();
  const b1=budgetBp(),was=!!(S.teamPrev&&S.teamPrev[id][p]),fee=0.5*salP(bb.lv,p)*1e-4*budNav();
  toast(`${on?(was?'Retour':'Recrutement'):(was?(id==='fo'&&goneP(p)?'Place libérée':'Licenciement'):'Sélection retirée')} : <b>${l.who}</b>${on&&!was&&l.hi?` — « ${l.hi} »`:''}${on&&!was?` · frais d'embauche ${mm(fee)}`:!on&&was&&!(id==='fo'&&goneP(p))?` · indemnité ${mm(fee)}`:''} · ${bb.nm} ${b0.toFixed(0)} → <b>${b1.toFixed(0)} pb</b>`);
 });""")
# 4. présences ailleurs
rep("""function pwHere(o){return o.fo!=null?(o.fo===0||here(o.fo)):(S.bud&&S.bud.bo>=o.bo)}""","""function pwHere(o){return o.fo!=null?(o.fo===0||here(o.fo)):boH(o.bo)}   /* lot 304 */""")
rep("""cands=[];for(let p=1;p<=S.bud.fo;p++)if(here(p)&&FOP[p].cls)cands.push(p);""","""cands=[];for(let p=1;p<FOP.length;p++)if(here(p)&&FOP[p].cls)cands.push(p);""")
rep(""" const bo=S.bud&&S.bud.bo||0;L.push([BOP[bo].ic""",""" const bo=(()=>{let n=0;if(S.bud)BOP.forEach((x,p)=>{if(hired('bo',p))n=p});return n})();L.push([BOP[bo].ic""")
open(p,'w',encoding='utf-8').write(s)
s=open(p,encoding='utf-8').read()
rep("""S.gones=gonesL().filter(g=>g.p!==p);setOps();drawBuds();""","""S.gones=gonesL().filter(g=>g.p!==p);teamInit().fo[p]=true;syncBud();setOps();drawBuds();""")
rep(""":lock(b.id,i)?'<span class="hx">imposé : carton rouge</span>'""",""":gone?'<span class="hx">contre-offre ci-dessous</span>':lock(b.id,i)?'<span class="hx">imposé : carton rouge</span>'""")
open(p,'w',encoding='utf-8').write(s)
