# -*- coding: utf-8 -*-
"""Lot 66 — demandes d'Antoine.
Panneau du haut : encours et performance dans une même tuile, trésorerie à gauche de la 2e ligne,
nuage rendement/risque remonté sur toute la hauteur de la colonne de droite, bas aligné sur les facteurs.
Plus de mandat de volatilité : ni cible, ni bande, ni sanction sur le risque ex ante. Le risque est borné
par le plafond de position, la marge et la trésorerie, et payé par les accidents de levier (TAILEV) dont la
probabilité et la gravité croissent avec le risque. Cartons sur pertes et replis. Concurrents à stratégie
de risque propre (vq), sous les mêmes contraintes de marchés et de plafond que le joueur.
Nuage ancré à l'origine, sans pointillés. Rubans en échelle log, zoomés sur les tracés, traits tous les 10 %.
Objectifs : scories de jauges nettoyées."""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()

# ───────────── 1. panneau du haut ─────────────
e.rep("""  <div class="srow">
   <button class="tile" data-gauge="cap"><span><i><span class="crestmini">${crestSvg(S.crest||0,15)}</span>${S.fundName.split(' ')[0]}${done?` · T${S.q}`:` · T${Math.min(S.q+1,QT())}`}</i><b>${rank}<sup>${rank===1?'er':'e'}</sup>/4</b></span><b id="navtile">${moneyB(navNow())}</b></button>
   <button class="tile" data-gauge="perf"><span><i>Perf.</i>${dd>0.005?`<b class="neg-g">repli ${(dd*100).toFixed(0)} %</b>`:'<b class="dim-g">au plus haut</b>'}</span><b class="${cls(cum)}">${sgnp(cum,1)}</b></button>
  </div>
  <div class="sgrid"><div class="sl">
  <div class="srow">
   ${(()=>{if(S.phase!=='book'||!S.k0)return '';const p=previewGauge();S._pv=p;return ''})()}""",
"""  <div class="sgrid"><div class="sl">
  <div class="srow">
   <button class="tile aum" data-gauge="cap"><span><i><span class="crestmini">${crestSvg(S.crest||0,15)}</span>${S.fundName.split(' ')[0]}${done?` · T${S.q}`:` · T${Math.min(S.q+1,QT())}`}</i><b>${rank}<sup>${rank===1?'er':'e'}</sup>/4</b></span><span class="aumv"><b id="navtile">${moneyB(navNow())}</b><b class="${cls(cum)}">${sgnp(cum,1)}${dd>0.005?`<em class="neg-g"> ↓${(dd*100).toFixed(0)} %</em>`:''}</b></span></button>
  </div>
  <div class="srow">
   ${(()=>{if(S.phase!=='book'||!S.k0)return '';const p=previewGauge();S._pv=p;return ''})()}
   <button class="tile gold" data-gauge="gain"><span>Trésorerie</span><b id="gaintile" class="${mgrCash()>=0?'':'neg-g'}">${treso(mgrCash())}</b></button>""")
e.rep("""   ${cardTile()}
   <button class="tile gold" data-gauge="gain" style="flex:.95"><span>Trésorerie</span><b id="gaintile" class="${mgrCash()>=0?'':'neg-g'}">${treso(mgrCash())}</b></button>
  </div>""","""   ${cardTile()}
  </div>""")
e.rep(".sgrid .sl{flex:1.45;",".sgrid .sl{flex:1.7;")
e.rep(".sgrid .fg.rmt{flex:1;min-width:0;padding:3px 4px;display:flex}\n.sgrid .rmap{height:100%;min-height:108px}",
""".sgrid .fg.rmt{flex:1;min-width:0;padding:0;display:block;position:relative;overflow:hidden}
.sgrid .rmap{position:absolute;inset:0;height:auto}
.sgrid .tile.aum>span.aumv{display:flex;justify-content:space-between;align-items:baseline;gap:6px;font-size:inherit;color:inherit}
.sgrid .tile.aum>span.aumv b{font-family:var(--mono);font-size:15px;font-weight:500}.sgrid .tile.aum>span.aumv b:first-child{color:var(--txt)}
.sgrid .tile.aum>span.aumv em{font-style:normal;font-size:10.5px}
.rmap .rd{position:absolute;width:6px;height:6px;margin:-3px 0 0 -3px;border-radius:50%}
.rmap .rd.me{width:9px;height:9px;margin:-4.5px 0 0 -4.5px;border:1px solid var(--bg,#0b1020)}.rmap .rd.me.hot{border:1.5px solid #D2463C}
.rmap .rl{position:absolute;font-family:var(--mono);font-size:7px;line-height:1;white-space:nowrap}
.rmap .rv{position:absolute;font-family:var(--mono);font-size:9.5px;font-weight:700;color:#F3EEE4;line-height:1.05;white-space:nowrap}
.rmap .rv small{display:block;font-size:7.5px;font-weight:400;color:var(--dim)}
.rmap .rv.hot{color:#E5675C}""")
# la pop-up « cap » reprend la performance
e.rep("""   <p style="margin-top:10px">Au-delà de <em>${Math.round(ddMax()*100)} % de repli</em> depuis le pic, des investisseurs demandent leur sortie.""",
"""   <p style="margin:12px 0 4px">Performance nette cumulée</p>
   ${tbl([['Depuis le début',`<span class="${cls(S.idx-1)}">${sgn(S.idx-1,1)}</span>`],...S.rets.map((r,i)=>[`T${i+1} · ${REG[S.regimes[i]].nm}`,`<span class="${cls(r)}">${sgn(r,1)}</span>`])])}
   <p class="note">Ce qu'un investisseur entré au premier jour a gagné ou perdu, après frais de gestion et commission de performance. Coûts de transaction et budget sont payés par votre société de gestion.</p>
   <p style="margin-top:10px">Au-delà de <em>${Math.round(ddMax()*100)} % de repli</em> depuis le pic, des investisseurs demandent leur sortie.""")
e.done("lot 66 — étape 1")

# ───────────── 2. accidents de levier, concurrents, nuage ─────────────
def cut(a,b):
    i=e.s.index(a);assert e.s.count(a)==1,a[:60];j=e.s.index(b,i);return i,j
i,j=cut("function rivPt(rv){","function rivCol(j){")
e.s=e.s[:i]+r"""/* lot 66 : plus de mandat de volatilité. Au-delà de TAIL.x0 de risque ex ante, un accident de levier
   (TAILEV) devient possible ; sa probabilité croît jusqu'à TAIL.p à x0 + w, sa gravité avec le risque.
   Le contrôle des risques en réduit la fréquence (TAILM, racine du multiplicateur d'incidents). */
const TAIL={x0:0.25,w:0.35,p:0.50},TAILM=[1.48,1.41,1.22,1.00,0.69,0.42,0.30];
function tailP(sp,std){return Math.max(0,Math.min(1,(sp-TAIL.x0)/TAIL.w))*TAIL.p*(std?1:(TAILM[(S&&S.bud)?S.bud.risk:3]||1))}
function tailL(sp){return sp*Math.max(0.3,Math.min(1.2,(sp-0.15)/0.25))}   /* perte de référence, × gravité de l'accident */
function tailExp(sp,std){return tailP(sp,std)*0.62*tailL(sp)*0.55}          /* coût moyen, sortie la moins chère */
/* Concurrents : chacun choisit son risque du trimestre (vq) selon sa stratégie, sous les mêmes contraintes
   que le joueur — marchés ouverts et plafond de position selon son propre encours. */
const RIVSTRAT={syst:{nm:'Kelly fractionnaire',d:'vise un quart du levier optimal, coupe de moitié après un repli',base:0.26,conv:0.06,cut:0.5,tail:'cut'},
 fonda:{nm:'Conviction',d:'monte le risque avec la force de son scénario',base:0.15,conv:0.34,cut:0.65,tail:'hedge'},
 flux:{nm:'Plein levier',d:'va au plafond de ce que ses marchés permettent, encaisse les accidents',base:0.47,conv:0,cut:0.6,tail:'hold'}};
function rivCapVol(rv){const a=(rv.mAum||S.aum0)/Math.max(1e-9,S.aum0),n=12+(a>=1.4?4:0)+(a>=2?4:0),ck=a>=1.5?5:a>=1.2?4:3;
 return 0.52*Math.sqrt(n/12)*ck/3}
function rivVolQ(rv){const st=RIVSTRAT[rv.style]||RIVSTRAT.fonda;let cv=0;(S.f||[]).forEach(x=>cv=Math.max(cv,Math.abs(x)));
 let v=st.base+st.conv*Math.min(1,cv/2)*(rv.skill||0.7)/0.7;
 const dd=1-(rv.cum||1)/Math.max(rv.peak||1,rv.cum||1);if(dd>0.12)v*=st.cut;
 return Math.max(0.06,Math.min(0.95*rivCapVol(rv),v*((SIZE()&&SIZE().rivVol)||1)))}
function rivV(rv){return rv.vq||rv.vol}
function rivDrag(v){return 0.004*(v/0.2)*(v/0.2)}   /* impact et financement d'un gros book, par trimestre */
function rivTail(rv,j,v,q){const u=prng32(hash32('rtail'+j+'_'+q,S.seed));if(u()>=tailP(v,1))return 0;
 const L=(0.45+0.35*u())*tailL(v),m=(RIVSTRAT[rv.style]||RIVSTRAT.fonda).tail;
 return m==='cut'?0.5*L:m==='hedge'?0.55*L:(u()<0.5?0.3*L:1.5*L)}
function rivPt(rv){
 const s=rv.skill,K4=4,v=rivV(rv);let E;
 if(rv.style==='syst')E=0.9*(2*s-1)*K4*0.8+0.8;
 else if(rv.style==='flux'){const p=Math.min(1,0.5+0.5*Math.max(0,(s-0.5)*1.8));E=1.1*(2*p-1)*K4*0.8}
 else E=(2*s-1)*1.6*1.8;
 return {x:v,y:S.rate/4+(v/2)*0.35*E-0.008-rivDrag(v)-0.5*v*v/4-tailExp(v,1),l:(rv.nm||'?').replace(/^(Le |La |L')/,'')[0]};
}
"""+e.s[j:]
i,j=cut("function riskMap(sp,big){","function colExp(){")
e.s=e.s[:i]+r"""/* lot 66 : nuage rendement / risque ancré à l'origine (les axes sont les zéros), zoomé sur le fonds le plus
   risqué et sur le rendement le plus haut, sans pointillés. Zone d'accidents de levier teintée. */
function riskMap(sp,big){
 const pr=profitBook(S.k),R=(S.rivals||[]).map((rv,j)=>Object.assign(rivPt(rv),{c:rivCol(j),nm:rv.nm}));
 const xm=Math.max(0.10,sp,...R.map(r=>r.x))*1.10;
 const ys=[pr,...R.map(r=>r.y)],ya=Math.min(0,...ys),yz=Math.max(0,...ys),ypad=Math.max(0.004,(yz-ya)*0.12);
 const y0=ya<0?ya-ypad:0,y1=yz+ypad;
 const hot=tailP(sp)>0,me=myCol(S.rivals||[]),f=v=>v.toFixed(1);
 const rv=`${dec(sp*100,1)} %`,yv=`${pr>=0?'+':'−'}${dec(Math.abs(pr)*100,1)} %`;
 if(big){
  const W=320,H=210,x0=34,x1=W-10,yb=H-22,yt=8;
  const X=v=>x0+(x1-x0)*v/xm,Y=v=>yb-(yb-yt)*(v-y0)/(y1-y0);
  let g='';
  if(TAIL.x0<xm)g+=`<rect x="${f(X(TAIL.x0))}" y="${yt}" width="${f(x1-X(TAIL.x0))}" height="${f(yb-yt)}" fill="#D2463C" opacity=".10"/>`
   +`<text x="${f(X(TAIL.x0)+3)}" y="${yt+10}" font-size="9" fill="#E5675C" font-family="var(--mono)" opacity=".85">accidents de levier</text>`;
  g+=`<line x1="${x0}" x2="${x1}" y1="${f(Y(0))}" y2="${f(Y(0))}" stroke="var(--dimmer)" stroke-width=".8"/><line x1="${x0}" x2="${x0}" y1="${yt}" y2="${yb}" stroke="var(--dimmer)" stroke-width=".8"/>`
   +`<text x="${x1}" y="${f(Y(0)+12)}" font-size="9" text-anchor="end" fill="var(--dim)" font-family="var(--mono)">risque →</text>`
   +`<text x="${x0-4}" y="${yt+8}" font-size="9" text-anchor="end" fill="var(--dim)" font-family="var(--mono)">↑</text>`
   +`<text x="${x0-4}" y="${f(Y(0)+3)}" font-size="9" text-anchor="end" fill="var(--dim)" font-family="var(--mono)">0</text>`;
  R.forEach(r=>{g+=`<circle cx="${f(X(r.x))}" cy="${f(Y(r.y))}" r="4" fill="${r.c}"/><text x="${f(X(r.x)+6)}" y="${f(Y(r.y)+3.5)}" font-size="10" fill="${r.c}" font-family="var(--mono)">${r.nm} · ${dec(r.x*100,0)} % · ${r.y>=0?'+':'−'}${dec(Math.abs(r.y)*100,1)} %</text>`});
  const px=X(sp),py=Y(pr);
  g+=`<text x="${f(Math.min(x1-30,Math.max(x0+24,px)))}" y="${yb+14}" font-size="10" text-anchor="middle" fill="${hot?'#E5675C':'#F3EEE4'}" font-family="var(--mono)" font-weight="700">${rv} <tspan font-weight="400" fill="var(--dim)" font-size="9">risque</tspan></text>`
   +`<text x="${x0+3}" y="${f(Math.min(yb-14,Math.max(yt+10,py-4)))}" font-size="10" fill="#F3EEE4" font-family="var(--mono)" font-weight="700">${yv} <tspan font-weight="400" fill="var(--dim)" font-size="9">rendement</tspan></text>`
   +`<circle cx="${f(px)}" cy="${f(py)}" r="5.5" fill="${me}" stroke="${hot?'#D2463C':'var(--bg,#0b1020)'}" stroke-width="${hot?1.6:.8}"/>`
   +`<text x="${f(px+8)}" y="${f(py-6)}" font-size="10" fill="${me}" font-family="var(--mono)" font-weight="700">Vous</text>`;
  const tp=tailP(sp);
  return `<p class="note" style="margin:0 0 4px">Risque annualisé du book (bruit d'estimation compris) en abscisse, rendement attendu du trimestre en ordonnée — collatéral, impact, drain de volatilité et coût moyen des accidents de levier compris. Les concurrents sont placés à leur couple estimé.</p><svg viewBox="0 0 ${W} ${H}" style="width:100%;height:auto;display:block;margin-bottom:6px">${g}</svg>`
   +`<p class="note" style="margin:0 0 10px">${tp>0?`À ${rv} de risque : <b class="neg-g">${dec(tp*100,0)} % de probabilité</b> d'un accident de levier ce trimestre, perte de l'ordre de ${dec(0.62*tailL(sp)*100,0)} % de l'encours si vous le laissez courir.`:`Sous ${dec(TAIL.x0*100,0)} % de risque, pas d'accident de levier possible.`}</p>`;
 }
 /* petit format : lignes en SVG étiré, points et libellés en HTML positionnés en %, jamais déformés */
 const L=3,Rr=4,T=5,B=15;
 const X=v=>L+(100-L-Rr)*v/xm,Y=v=>100-B-(100-B-T)*(v-y0)/(y1-y0);
 const ax=Y(0);
 let s=`<svg viewBox="0 0 100 100" preserveAspectRatio="none" style="position:absolute;inset:0;width:100%;height:100%">`
  +(TAIL.x0<xm?`<rect x="${f(X(TAIL.x0))}" y="${T}" width="${f(100-Rr-X(TAIL.x0))}" height="${f(100-B-T)}" fill="#D2463C" opacity=".10"/>`:'')
  +`<line x1="${L}" x2="${100-Rr}" y1="${f(ax)}" y2="${f(ax)}" stroke="var(--dimmer)" stroke-width="1" vector-effect="non-scaling-stroke"/>`
  +`<line x1="${L}" x2="${L}" y1="${T}" y2="${100-B}" stroke="var(--dimmer)" stroke-width="1" vector-effect="non-scaling-stroke"/></svg>`;
 R.forEach(r=>{s+=`<i class="rd" style="left:${f(X(r.x))}%;top:${f(Y(r.y))}%;background:${r.c}"></i>`});
 const px=X(sp),py=Y(pr);
 s+=`<i class="rd me${hot?' hot':''}" style="left:${f(px)}%;top:${f(py)}%;background:${me}"></i>`
  +`<span class="rv${hot?' hot':''}" style="left:${f(Math.min(62,Math.max(L,px-14)))}%;bottom:1px">${rv} <small style="display:inline">risque</small></span>`
  +`<span class="rv" style="left:${L+2}%;top:${f(Math.min(100-B-24,Math.max(T,py-16)))}%">${yv}<small>rendement</small></span>`;
 return `<div class="rmap">${s}</div>`;
}
"""+e.s[j:]
# le rendement attendu du book compte le coût moyen des accidents de levier
e.rep(" const sg=riskShown(w).total;return m-0.5*sg*sg/4;"," const sg=riskShown(w).total;return m-0.5*sg*sg/4-tailExp(sg);")

# ───────────── 3. concurrents branchés ─────────────
e.rep(" S.stopQ=false;S.noAddQ=false;\n"," S.stopQ=false;S.noAddQ=false;\n (S.rivals||[]).forEach(rv=>{rv.vq=rivVolQ(rv)});   /* lot 66 : risque du trimestre, sans tirage */\n S.tailEv=null;S.tailDone=false;S.tailQ=null;\n",1)
e.rep("""   return (rv.vol/2)*(0.70*e/2+(RIVNOISE[rv.style]||0.78)*gauss())-0.008;""",
"""   const v=rivV(rv),j=S.rivals.indexOf(rv),tl=rivTail(rv,j,v,S.q);rv.tailHit=tl>0?tl:0;
   return (v/2)*(0.70*e/2+(RIVNOISE[rv.style]||0.78)*gauss())-0.008-rivDrag(v)-tl;""")
e.rep(" return t*((r.vol/2)*(0.70*e/2)-0.008);"," const v=rivV(r);return t*((v/2)*(0.70*e/2)-0.008-rivDrag(v));")
e.rep("tapeVol(TAPEM,1,r.vol)","tapeVol(TAPEM,1,(r.vqh&&r.vqh[i])||r.vol)")
e.rep("tapeVol(TAPEM,t-(k?ts[k-1]:0),r.vol)","tapeVol(TAPEM,t-(k?ts[k-1]:0),rivV(r))")
e.rep("tapeVol(18,0.04,r.vol)","tapeVol(18,0.04,rivV(r))")
e.rep(" S.rivals.forEach((rv,j)=>{rv.last=rr[j];rv.cum*=(1+rr[j]);(rv.hist=rv.hist||[]).push(rr[j]);rivalMgrQuarter(rv,rr[j])});",
 " S.rivals.forEach((rv,j)=>{rv.last=rr[j];rv.cum*=(1+rr[j]);rv.peak=Math.max(rv.peak||1,rv.cum);(rv.hist=rv.hist||[]).push(rr[j]);(rv.vqh=rv.vqh||[]).push(rivV(rv));rv.vqLast=rivV(rv);rivalMgrQuarter(rv,rr[j])});")
# tableau de la concurrence : colonne risque
e.rep(" const all=[{nm:S.fundName,v:o.qTotal,me:1},...S.rivals.map(r=>({nm:r.nm+' · '+r.boss,v:r.last}))]",
 " const all=[{nm:S.fundName,v:o.qTotal,me:1,rk:o.sp},...S.rivals.map(r=>({nm:r.nm+' · '+r.boss,v:r.last,rk:r.vqLast||rivV(r),st:(RIVSTRAT[r.style]||{}).nm,th:r.tailHit}))]")
e.rep("<th>Fonds</th><th>Trim.</th><th>Cumul</th>","<th>Fonds</th><th>Risque</th><th>Trim.</th><th>Cumul</th>")
e.rep("""`<tr class="${a.me?'me':''}"><td>${a.nm}</td><td class="${cls(a.v)}">""",
 """`<tr class="${a.me?'me':''}"><td>${a.nm}${a.st?`<br><span class="dim-g" style="font-size:11px">${a.st}${a.th?' · <span class="neg-g">accident</span>':''}</span>`:''}</td><td>${a.rk!==undefined?dec(a.rk*100,0)+' %':''}</td><td class="${cls(a.v)}">""")
e.rep("""function introRivals(){
 return `<div class="rivs">${RIVALS.map(r=>`<div class="riv">${avatar(r.boss,'rival')}<div><b>${r.boss}</b><span>${r.nm.toUpperCase()}</span></div></div>`).join('')}</div>`;""",
"""function introRivals(){
 return `<div class="rivs">${RIVALS.map(r=>`<div class="riv">${avatar(r.boss,'rival')}<div><b>${r.boss}</b><span>${r.nm.toUpperCase()}</span><span style="text-transform:none">${(RIVSTRAT[r.style]||{}).nm} — ${(RIVSTRAT[r.style]||{}).d}</span></div></div>`).join('')}</div>`;""")

# ───────────── 4. accidents de levier : pool, tirage pur, écran ─────────────
e.rep("const BOARDEV=[",r"""/* lot 66 : accidents de levier. Tirés seulement au-dessus de TAIL.x0 de risque ex ante, à la fin de la file
   du trimestre, par un tirage pur (hash32('tail'+q)) : aucun flux nommé n'est déplacé. o = libellés
   [tenir, couper, couvrir]. sev = gravité, multiplie tailL(risque). */
const TAILEV=[
 {t:"Krach éclair : les carnets se vident en quatre minutes",who:"Desk · alerte rouge",sev:[0.55,0.80],
  p:"Un vendeur algorithmique déclenche une cascade. Vos positions les plus grosses sont celles que tout le monde veut sortir en même temps.",
  o:["Tenir et attendre que les carnets se remplissent","Couper la moitié du book dans le vide","Acheter de la protection à n'importe quel prix"]},
 {t:"Un trader a doublé ses positions en cachette",who:"Contrôle des risques · rapport d'urgence",sev:[0.45,0.75],
  p:"Des transactions inter-books masquaient un pari deux fois plus gros que le vôtre. Le marché commence à sentir la position.",
  o:["Garder la position et espérer un rebond","Déboucler la moitié du book immédiatement","Couvrir par des dérivés, le prime broker fixe le prix"]},
 {t:"Le moteur d'ordres a renvoyé chaque ordre trois fois",who:"Incident technique · critique",sev:[0.40,0.70],
  p:"Une mise à jour a cassé le contrôle des doublons. Votre book réel pèse trois fois ce que vous croyez, sur les marchés les plus serrés.",
  o:["Laisser le surplus se résorber","Vendre en urgence, impact compris","Geler le surplus contre une garantie du prime broker"]},
 {t:"Votre prime broker relève les marges de 40 % dans la nuit",who:"Prime broker · courrier recommandé",sev:[0.45,0.70],
  p:"Il invoque la concentration de votre book. Vous avez jusqu'à l'ouverture pour poster le collatéral ou réduire.",
  o:["Ne rien faire et négocier","Réduire de moitié à l'ouverture","Poster le collatéral sur une ligne de crédit hors de prix"]},
 {t:"Squeeze sur votre plus grosse vente à découvert",who:"Desk · exécution",sev:[0.50,0.85],
  p:"Un concurrent a repéré votre position et rachète tout ce qui se présente. Chaque tick vous coûte, et tout le monde le sait.",
  o:["Tenir la position courte","Racheter la moitié, à n'importe quel prix","Couvrir par des options d'achat hors de prix"]},
 {t:"La chambre de compensation exige un dépôt exceptionnel",who:"Chambre de compensation · appel d'urgence",sev:[0.40,0.65],
  p:"Après une journée de volatilité record, la chambre recalcule ses marges initiales. Les fonds les plus levés passent en premier.",
  o:["Laisser courir et payer ce qu'on vous demandera","Réduire de moitié pour rentrer dans les clous","Emprunter le dépôt au taux que la banque choisit"]},
 {t:"Défaut d'une contrepartie sur vos swaps",who:"Juridique · alerte",sev:[0.40,0.70],
  p:"La banque qui portait vos swaps de taux et de change suspend ses paiements. Vos couvertures n'existent plus, vos positions si.",
  o:["Attendre la procédure de résolution","Fermer la moitié des positions découvertes","Retrouver une contrepartie, avec une prime d'urgence"]},
 {t:"Tout le monde a le même book que vous",who:"Prime broker · note confidentielle",sev:[0.45,0.80],
  p:"Les fonds macro sortent ensemble d'un trade devenu trop encombré. Vos positions, les leurs : le même paquet, dans le même sens.",
  o:["Rester et parier que la foule rentrera","Sortir de la moitié avant les autres","Couvrir le facteur commun par des indices"]},
 {t:"Le risque de modèle se matérialise",who:"Quantitatif · rapport",sev:[0.40,0.70],
  p:"Les corrélations sur lesquelles reposait votre book se sont inversées en une semaine. Vos compensations sont devenues des paris dans le même sens.",
  o:["Faire confiance au modèle","Couper la moitié du book","Superposer une couverture de corrélation"]},
 {t:"Panne du fournisseur de données en pleine séance",who:"Infrastructure · incident majeur",sev:[0.35,0.60],
  p:"Pendant trois heures, vos prix sont faux et vos limites de risque aveugles. Le marché, lui, bouge vraiment.",
  o:["Attendre le retour des prix","Réduire à l'aveugle de moitié","Faire coter par téléphone, à prix de gré à gré"]},
 {t:"Une ligne de crédit vous est coupée sans préavis",who:"Trésorerie · urgent",sev:[0.40,0.70],
  p:"Votre deuxième banque se retire du financement des fonds à fort levier. La moitié de votre financement disparaît à la fin du mois.",
  o:["Espérer un repreneur de ligne","Déleverager de moitié tout de suite","Refinancer auprès d'un prêteur de dernier recours"]},
 {t:"Rumeur de liquidation de votre fonds",who:"Fil d'actualité · 06h40",sev:[0.45,0.75],
  p:"Un message non sourcé annonce vos difficultés. Les contreparties vous vendent ce que vous achetez et vous achètent ce que vous vendez.",
  o:["Démentir et tenir","Réduire de moitié pour prouver votre solvabilité","Faire garantir vos positions par une banque, contre commission"]}
];
const BOARDEV=[""")
e.rep(" if(S.incidentDue&&!S.incidentShown){S.incidentShown=true;screenIncident();window.scrollTo(0,0);return}",
""" if(!S.tailDone){if(S.tailEv===null||S.tailEv===undefined)S.tailEv=tailDraw()||0;
  if(S.tailEv){screenTail(S.tailEv);window.scrollTo(0,0);return}S.tailDone=true}
 if(S.incidentDue&&!S.incidentShown){S.incidentShown=true;screenIncident();window.scrollTo(0,0);return}""")
e.rep("function screenIncident(){",r"""/* lot 66 : accident de levier. Tout est tiré avant l'affichage : les montants des boutons sont appliqués tels quels. */
function tailDraw(){
 const sp=riskShown(weights(S.k)).total,u=prng32(hash32('tail'+S.q,S.seed));
 if(u()>=tailP(sp))return null;
 const i=Math.floor(u()*TAILEV.length),ev=TAILEV[i],L=(ev.sev[0]+(ev.sev[1]-ev.sev[0])*u())*tailL(sp),good=u()<0.5;
 let imp=0;for(let m=0;m<N;m++){const d=Math.trunc(S.k[m]/2)-S.k[m];if(d)imp+=tcost(d,m).cost*5}
 return {i,sp,L,good,imp:imp/S.nav};
}
function tailOpts(te){const L=te.L;
 return [{id:'hold',f:te.good?0.3*L:1.5*L,m:0,c:te.good?-1:-8},
  {id:'cut',f:0.5*L+Math.min(0.08,te.imp),m:0,c:-3},
  {id:'hedge',f:0.30*L,m:0.20*L,c:-2}]}
function screenTail(te){
 const ev=TAILEV[te.i]||TAILEV[0],O=tailOpts(te),nav=S.nav,L=te.L;
 const row=(a,b)=>`<div class="gzr"><span>${a}</span>${b}</div>`;
 const btn=(o,k)=>{const ko=o.m>0&&mgrCash()<o.m*nav;
  const body=o.id==='hold'?row('une chance sur deux',`<b class="neg-g">−${mm(0.3*L*nav)} · confiance −1</b>`)+row('une chance sur deux',`<b class="neg-g">−${mm(1.5*L*nav)} · confiance −8</b>`)
   :row('fonds',`<b class="neg-g">−${mm(o.f*nav)} · ${sgnp(-o.f,1)}</b>`)+(o.m?row('votre trésorerie',`<b class="neg-g">−${mm(o.m*nav)}</b>`):'')
    +row(o.id==='cut'?'book':'confiance',o.id==='cut'?'<b>positions divisées par deux · confiance −3</b>':`<b class="neg-g">−2</b>`);
  return `<button class="choice" data-t="${k}"${ko?' disabled':''}><b>${ev.o[k]}</b><span>${body}${ko?' <b class="neg-g">hors trésorerie</b>':''}</span></button>`};
 app.innerHTML=statusBar()+`<div class="evwrap fade">
  <div class="evcard bad">${evHead(ev.who,'risk')}<h3>${ev.t}</h3><p>${ev.p}</p>
   <p class="note">Accident de levier : votre book tourne à ${pct(te.sp)} de risque. En dessous de ${dec(TAIL.x0*100,0)} %, il ne serait pas arrivé.</p></div>
  <div class="choices" style="margin-top:12px">${O.map((o,k)=>btn(o,k)).join('')}</div></div>`;
 document.querySelectorAll('.choice[data-t]').forEach(b=>b.onclick=()=>{
  const k=+b.dataset.t,o=O[k],loss=o.f*nav;
  S.nav-=loss;S.qIncM-=loss;
  if(o.m){S.mgrCosts+=o.m*nav;S.qTailMgr=(S.qTailMgr||0)+o.m*nav}
  if(o.id==='cut')S.k=S.k.map(v=>Math.trunc(v/2));
  const g=gauge(o.c,0,`Accident de levier : ${ev.t}`);
  S.evLog.push({t:ev.t,pnl:-o.f,m:-loss,lp:g.lp,rc:g.rc});(S.tails=S.tails||[]).push({q:S.q,t:ev.t,f:o.f,id:o.id});
  S.tailDone=true;S.tailEv=0;try{refreshGain()}catch(err){}
  const res=o.id==='hold'?(te.good?'La tempête passe sans emporter le book. Cette fois.':'La tempête emporte tout ce qui dépasse.'):o.id==='cut'?'Le book est coupé de moitié, au pire prix de la séance.':'La couverture tient. Elle a coûté ce qu\'on vous a demandé.';
  app.innerHTML=statusBar()+`<div class="evwrap fade"><div class="evcard rescard ${o.f>0.05?'bad':''}"><h3>${res}</h3>
   <div class="kv"><span>Coût pour le fonds</span><b class="neg-g">−${mm(loss)} · ${sgnp(-o.f,1)}</b></div>
   ${o.m?`<div class="kv"><span>Payé par votre trésorerie</span><b class="neg-g">−${mm(o.m*nav)}</b></div>`:''}
   <div class="kv"><span>Confiance</span><b class="${cls(g.lp)}">${sd1(g.lp)}</b></div></div>
   <button class="cta" id="ok">Poursuivre le trimestre</button></div>`;
  document.getElementById('ok').onclick=()=>stepEvents();window.scrollTo(0,0);
 });
}
function screenIncident(){""")

# ───────────── 5. plus de mandat de volatilité ; cartons sur pertes et replis ─────────────
e.rep("""function riskRc(k){
 const w=weights(k),sp=riskShown(w).total,vd=varDecomp(w),fmax=Math.max(...vd.fv)/vd.tot;
 const band=bandNow(),dev=Math.abs(sp-S.tgt)/S.tgt;
 /* plus aucun plafond : la sanction croît continûment avec l'écart au mandat. La seule
    limite restante est la borne de gauge(). */
 const ex=Math.max(0,dev-band);
 let d=dev<band?3*(1-dev/band):-ex*32*(1+ex)*SIZE().rcNeg;
 if(fmax>0.75)d-=3*SIZE().rcNeg;if(sp<0.02)d-=4;
 return d;
}""","""function riskRc(k){   /* lot 66 : plus de mandat de volatilité ; seul le book vide est noté */
 return riskShown(weights(k)).total<0.02?-4:0;
}""")
e.rep("""const band=bandNow(),dev=Math.abs(sp-S.tgt)/S.tgt;
 let drc=dev<band?3:-Math.min(12,(dev-band)*18)*SIZE().rcNeg;
 if(fmax>0.75)drc-=3*SIZE().rcNeg;if(sp<0.02)drc-=4;""","""let drc=sp<0.02?-4:0;""")
e.rep("""if(sp<0.7*S.tgt)dlp-=Math.min(7,(0.7*S.tgt-sp)/S.tgt*18);
 else if(dev<band*0.5)dlp+=1;
 if(sp>S.tgt*(1+band))dlp-=Math.min(4,(sp/S.tgt-1-band)*10);
""","")
e.rep("""if(sp<0.7*S.tgt)why.push('book sous-investi pour le mandat');
 if(sp>S.tgt*(1+band))why.push('risque au-dessus du budget');
 else if(dev<band)why.push('vol dans la bande');
 if(fmax>0.75)why.push('un seul facteur');if(sp<0.02)""","""if(tailP(sp)>0)why.push(`accident de levier possible (${dec(tailP(sp)*100,0)} %)`);
 if(sp<0.02)""")
# clôture : confiance et comité
e.rep("  if(riskShown(wFin).total>2*S.tgt)lpD.push(['Le rapport de risque circule : book au double de la cible',-4]);\n","")
e.rep(""" const rsx=riskShown(wFin).total/Math.max(1e-9,S.tgt);
 if(rsx>2)rcD.push([`Risque ex-ante à ${dec(rsx,1)} fois la cible`,-Math.min(40,10+40*(rsx-2))]);
 if(sp>1e-6&&gross<-2.2*sp/2)rcD.push(['Perte au-delà de 2,2 σ ex-ante',-10]);""",""" if(qTotal<-0.10)rcD.push(['Perte trimestrielle au-delà de 10 %',-10]);""")
e.rep(" if(Math.abs(pvol(weights(S.k))-S.tgt)/S.tgt>bandNow())S.outBand=(S.outBand||0)+1;\n","")
e.rep("""  const dev=Math.abs(sp-S.tgt)/Math.max(1e-9,S.tgt),bnd=bandNow();
  if(rsx>2)red=`risque ex-ante à ${dec(rsx,1)} fois la cible`;
  else if(sp>1e-6&&gross<-2.2*sp/2)red='perte au-delà de 2,2 σ ex-ante';
  else if(S.marginCall)red='appel de marge';
  if(sp<0.02)why.push('book vide');
  else{const spV=S.kVal?pvol(weights(S.kVal)):sp;   /* la bande juge le book validé ; les réactions aux dépêches relèvent du rouge au double de la cible */
   if(spV>S.tgt*(1+bnd))why.push(`book validé à ${pct(spV)} de volatilité, au-dessus de la bande (${pct(S.tgt,0)} +${(bnd*100).toFixed(0)} %)`)}
  if(sp>=0.02&&fmax>0.75)why.push(`${(fmax*100).toFixed(0)} % du risque sur un seul facteur`);""",
"""  /* lot 66 : le comité juge les pertes et les replis, plus le risque ex ante. Un repli ne vaut un carton
     qu'à chaque nouveau palier (+5 pts pour le rouge, +4 pour le jaune), réarmé sous 8 %. */
  const tt=S.bandTight||1,ddp=Math.max(0,1-S.idx/Math.max(S.hwmIdx||1,S.idx));
  if(ddp<0.08){C.ddR=0;C.ddY=0}
  if(qTotal<=-0.12*tt)red=`trimestre à ${sgnp(qTotal,1)}`;
  else if(ddp>=0.25*tt&&ddp>(C.ddR||0)+0.05){red=`repli de ${dec(ddp*100,0)} % depuis le plus haut`;C.ddR=ddp}
  else if(S.marginCall)red='appel de marge';
  if(sp<0.02&&!(S.tails||[]).some(x=>x.q===S.q))why.push('book vide');
  if(qTotal<=-0.05*tt)why.push(`trimestre à ${sgnp(qTotal,1)}`);
  if(ddp>=0.12*tt&&ddp>(C.ddY||0)+0.04){why.push(`repli de ${dec(ddp*100,0)} % depuis le plus haut`);C.ddY=ddp}
  if(qTotal-med<=-0.08)why.push(`${dec((med-qTotal)*100,0)} pts sous la médiane des concurrents`);""")
e.rep(" if(Math.abs(pvol(weights(S.k))-S.tgt)/S.tgt>bandNow())S.inBand=0;else S.inBand=(S.inBand||0)+1;",
      " if(S.qCard)S.inBand=0;else S.inBand=(S.inBand||0)+1;   /* lot 66 : trimestres sans carton */")
# book : drapeaux et ligne de risque
e.rep(""" if(sp>2*S.tgt)flags+=`<div class="flag" style="border-color:var(--short)"><span><b>Risque au double de la cible.</b> À la clôture, le comité sanctionnera lourdement (jusqu'à −40) et les investisseurs l'apprendront.</span></div>`;
 else if(sp>S.tgt*(1+band))flags+=`<div class="flag"><span>Vol ex-ante ${pct(sp)} contre une cible de ${pct(S.tgt,0)} — hors de la bande de tolérance de votre comité (±${(band*100).toFixed(0)} %).</span></div>`;
 if(sp<S.tgt*0.5&&sp>0.001)""","""  if(tailP(RS.total)>0)flags+=`<div class="flag" style="border-color:var(--short)"><span><b>Zone d'accidents de levier.</b> À ${pct(RS.total)} de risque : ${dec(tailP(RS.total)*100,0)} % de probabilité d'un accident ce trimestre, perte de l'ordre de ${dec(0.62*tailL(RS.total)*100,0)} % de l'encours si vous le laissez courir. Toute sortie coûte cher.</span></div>`;
 if(sp<0.08&&sp>0.001)""".replace("  if(tailP"," if(tailP"))
e.rep("""  <div class="kv"><span>Risque du book · cible ±bande</span><b>${pct(RS.total)} · ${pct(S.tgt,0)} ±${(band*100).toFixed(0)} %</b></div>""",
"""  <div class="kv"><span>Risque du book · accident de levier</span><b class="${tailP(RS.total)>0?'neg-g':''}">${pct(RS.total)} · ${tailP(RS.total)>0?dec(tailP(RS.total)*100,0)+' %':'aucun'}</b></div>""")
# pop-ups
e.rep("""['Bande de volatilité',`${pct(S.tgt,0)} ±${(bandNow()*100).toFixed(0)} %`]""","""['Accidents de levier',`au-delà de ${dec(TAIL.x0*100,0)} % de risque ex ante`]""")
e.rep("""<li>🟥 <b>Rouge</b> : risque au double de la cible, perte au-delà de 2,2 σ, appel de marge, ou deuxième jaune.</li><li>🟨 <b>Jaune</b> : book validé au-dessus de la bande de volatilité, plus de 75 % du risque sur un facteur, book vide, griefs accumulés.</li>""",
"""<li>🟥 <b>Rouge</b> : trimestre à −12 % ou pire, repli de 25 % depuis le plus haut (puis chaque 5 points de plus), appel de marge, ou deuxième jaune.</li><li>🟨 <b>Jaune</b> : trimestre à −5 % ou pire, repli de 12 % (puis chaque 4 points de plus), 8 points sous la médiane des concurrents, book vide, griefs accumulés.</li><li>Le comité ne juge plus le risque ex ante : il n'y a pas de mandat de volatilité. Le risque se paie autrement, par les accidents de levier.</li>""")
e.rep("""   <p class="note">Votre comité, lui, juge sur le σ du modèle (${pct(RS.base)}) face à la cible et à sa bande : il a son propre calcul et il ne majore pas. L'écart entre les deux chiffres est votre information, pas la sienne.</p>""","")
e.rep("""['Cible · bande du comité',`${(S.tgt*100).toFixed(0)} % · ${dec((S.tgt*(1-bandNow())*100),1)}–${dec((S.tgt*(1+bandNow())*100),1)} %`]""",
"""['Accident de levier ce trimestre',tailP(RS.total)>0?`${dec(tailP(RS.total)*100,0)} % · perte ≈ ${dec(0.62*tailL(RS.total)*100,0)} %`:`aucun sous ${dec(TAIL.x0*100,0)} %`]""")
# débriefing, presse, textes
e.rep("""const w=weights(S.k),sp=pvol(w),band=bandNow(),dev=Math.abs(sp-S.tgt)/S.tgt;
 const inc=""","""const w=weights(S.k),sp=pvol(w);
 const inc=""")
i=e.s.index(" C.push(dev<band*0.5?t([`Vol ex-ante ${pct(sp)} : au cœur de la bande");j=e.s.index(" if(inc)C.push(",i)
e.s=e.s[:i]+""" C.push(dd>0.15?t([`${dec(dd*100,0)} % sous le plus haut : le comité veut savoir ce qui est encore en place.`,`Un repli de ${dec(dd*100,0)} % : le comité parle de « plan de redressement ».`],8)
  :tailP(sp)>0?t([`${pct(sp)} de risque : le comité rappelle que les accidents de levier ne préviennent pas.`,`Book à ${pct(sp)} : on vous demande qui paie si le prime broker rappelle ses marges.`],8)
  :sp<0.08?t([`${pct(sp)} de risque : le comité n'a rien à vous reprocher, les investisseurs peut-être.`,`Un book à ${pct(sp)} : prudent, et facturé au tarif plein.`],8)
  :t([`Risque ex ante ${pct(sp)} : le comité prend acte.`,`${pct(sp)} de risque : rien à redire tant que les pertes restent contenues.`],8));
"""+e.s[j:]
e.rep("else if(S.rcD.some(x=>/2,2 σ/.test(x[0])))","else if(S.rcD.some(x=>/au-delà de 10/.test(x[0])))")
e.rep("La perte dépasse ce que votre propre modèle annonçait : la seule chose qu'un comité ne pardonne pas.","Une perte à deux chiffres en un trimestre : la seule chose qu'un comité ne pardonne pas.")
e.rep("Le modèle est faux, ou le book n'était pas celui du rapport. Les deux hypothèses vous desservent.","On vous demande si le risque pris valait ce qu'il a coûté. La réponse est dans le chiffre.")
e.rep(" else if(sp<0.6*S.tgt)add("," else if(sp<0.10)add(")
e.rep("`${F} facture un mandat à ${pct(S.tgt,0)} de vol et en livre ${pct(sp)} :","`${F} facture des frais de fonds macro et livre ${pct(sp)} de vol :")
e.rep("`Risque sous-employé chez ${F} : ${pct(sp)} de vol pour une cible de ${pct(S.tgt,0)}. Les frais, eux, sont au tarif plein`","`Risque sous-employé chez ${F} : ${pct(sp)} de vol. Les frais, eux, sont au tarif plein`")
e.rep("`${F} : vol réalisée ${pct(sp)}, cible ${pct(S.tgt,0)}.","`${F} : vol réalisée ${pct(sp)}, moitié moins que ses concurrents.")
e.rep("""t:"« Le mandat n'est pas rempli. Montez le risque ou expliquez pourquoi vous facturez »",cond:()=>pvol(weights(S.k))<0.7*S.tgt""","""t:"« Le risque dort. Montez-le ou expliquez pourquoi vous facturez »",cond:()=>pvol(weights(S.k))<0.14""")
e.rep("cond:()=>pvol(weights(S.k))<0.85*S.tgt,","cond:()=>pvol(weights(S.k))<0.17,")
e.rep("Un contrôle sérieux évite les incidents, élargit la bande de volatilité que le comité vous laisse, et apaise ses griefs — moins de cartons.","Un contrôle sérieux évite les incidents, rend les accidents de levier plus rares, et apaise les griefs du comité.")
e.rep("· bande du comité ±${Math.round(BANDB[i]*100)} %`","· accidents de levier ×${dec(TAILM[i],2)}`")
e.rep("Un mandat de taille, avec ses conditions : le comité resserre votre bande de volatilité.","Un mandat de taille, avec ses conditions : le comité sortira ses cartons plus tôt.")
e.rep("· bande du comité −20 %`","· seuils des cartons −20 %`")
e.rep("<b>Risque du book</b> affiche votre volatilité ex-ante majorée, à comparer à la cible de votre mandat.","<b>Le nuage</b> place votre book en risque et en rendement attendu, face aux trois concurrents ; au-delà de 25 % de risque, la zone rouge est celle des accidents de levier.")
e.rep("pour une cible de ${pct(S.tgt,0)}. Pondération","pour une référence de ${pct(S.tgt,0)}. Pondération")
for a,b in [("le modèle ne vise que 80 % de la vol cible","le modèle ne vise que 16 % de vol"),("votre desk vise 110 % de la vol cible","votre desk vise 22 % de vol"),("votre desk vise 120 % de la vol cible","votre desk vise 24 % de vol")]:
    e.rep(a,b)
e.rep("Une unité de position vaut un huitième de la vol cible du mandat en volatilité standalone","Une unité de position vaut 2,5 % de volatilité standalone")
e.rep("""  <div class="rule"><b>Le piège</b>""","""  <div class="rule"><b>Le risque</b><span>Pas de mandat de volatilité : un fonds macro est là pour gagner. Le risque est borné par le plafond de position, la marge du prime broker et votre trésorerie. Au-delà de <strong>25 %</strong> de risque ex ante, des <strong>accidents de levier</strong> deviennent possibles — krach éclair, trader non autorisé, erreur système, marges relevées — et d'autant plus graves que le book est gros. S'en sortir coûte très cher. Le comité, lui, sort ses cartons sur les pertes et les replis.</span></div>
  <div class="rule"><b>Le piège</b>""")
e.rep("Tout le monde part avec 100 M$ et une volatilité cible de 20 %.","Tout le monde part avec 100 M$, sans mandat de volatilité.")
# objectifs et haut fait
G=[("""{nm:"La main légère",d:"Garder la volatilité réalisée sous la cible du mandat.",t:c=>c.vol<c.tgt,b:0.06}""","""{nm:"La main légère",d:"Garder la volatilité réalisée sous 15 %.",t:c=>c.vol<0.15,b:0.06}"""),
 ("""{nm:"Dans la bande",d:"Terminer avec une volatilité ex-ante dans la bande du comité.",t:c=>c.inBand,b:0.05}""","""{nm:"Le gros calibre",d:"Terminer avec plus de 30 % de risque ex ante et un trimestre positif.",t:c=>c.sp>0.30&&c.q>0,b:0.10}"""),
 ("""d:"Terminer avec la jauge investisseurs plus haute qu'au début du trimestre.",t:c=>c.dLp>0""","""d:"Terminer avec la confiance plus haute qu'au début du trimestre.",t:c=>c.dLp>0"""),
 ("""{nm:"Rassurer le comité",d:"Terminer avec la jauge comité plus haute qu'au début du trimestre.",t:c=>c.dRc>0,b:0.05}""","""{nm:"Près du sommet",d:"Terminer le trimestre à moins de 2 % de votre plus haut.",t:c=>c.dd<0.02,b:0.05}"""),
 ("""{nm:"Les deux à la fois",d:"Terminer avec les deux jauges en hausse sur le trimestre.",t:c=>c.dLp>0&&c.dRc>0,b:0.09}""","""{nm:"Les deux à la fois",d:"Terminer avec la confiance en hausse et un nouveau plus haut historique.",t:c=>c.dLp>0&&c.newHigh,b:0.09}"""),
 ("""{nm:"Le comité serein",d:"Terminer avec la jauge comité au-dessus de 75.",t:c=>c.rc>75,b:0.07}""","""{nm:"La confiance solide",d:"Terminer avec la confiance au-dessus de 70.",t:c=>c.lp>70,b:0.07}"""),
 ("""d:"Regagner au moins huit points de jauge investisseurs sur le trimestre.\"""","""d:"Regagner au moins huit points de confiance sur le trimestre.\""""),
 ("""rester sous 5 % de repli et finir avec les deux jauges en hausse.",t:c=>c.rel>0&&c.dd<0.05&&c.dLp>0&&c.dRc>0""","""rester sous 5 % de repli et finir avec la confiance en hausse.",t:c=>c.rel>0&&c.dd<0.05&&c.dLp>0"""),
 ("""d:"Livrer l'objectif du mandat avec une volatilité réalisée sous la cible.",t:c=>c.q>=c.goalQ&&c.vol<c.tgt""","""d:"Livrer l'objectif du mandat avec une volatilité réalisée sous 15 %.",t:c=>c.q>=c.goalQ&&c.vol<0.15"""),
 ("""d:"Regagner des points sur les deux jauges après un trimestre négatif.",t:c=>c.prevQ<0&&c.dLp>0&&c.dRc>0,b:0.12""","""d:"Regagner de la confiance après un trimestre négatif.",t:c=>c.prevQ<0&&c.dLp>0,b:0.08"""),
 ("""d:"Trimestre positif, collecte positive et comité en hausse.",t:c=>c.q>0&&c.flow>0&&c.dRc>0""","""d:"Trimestre positif, collecte positive et confiance en hausse.",t:c=>c.q>0&&c.flow>0&&c.dLp>0""")]
for a,b in G: e.rep(a,b)
e.rep("vol:S.realVol,tgt:S.tgt,inBand:Math.abs(pvol(w)-S.tgt)/S.tgt<=bandNow(),","vol:S.realVol,tgt:S.tgt,sp:pvol(w),")
e.rep("""d:"Ne jamais sortir de la bande de volatilité d'un mandat d'au moins huit trimestres.",tf:f=>!f.over&&!f.outBand&&f.q>=8""",
      """d:"Ne recevoir aucun carton du comité sur un mandat d'au moins huit trimestres.",tf:f=>!f.over&&f.nocard&&f.q>=8""")
e.rep("outBand:!!S.outBand,mc:","outBand:!!S.outBand,nocard:!(S.cards&&S.cards.log&&S.cards.log.length),mc:")
e.rep(" La marge utilisée se lit dans la jauge Risque et sous le book."," La marge utilisée se lit sous le book.")

# ───────────── 6. rubans : échelle log, zoom sur les tracés, traits tous les 10 % ─────────────
e.rep(""" let a=100,b=100;p.forEach(v=>{a=Math.min(a,v);b=Math.max(b,v)});rv.forEach(r=>r.pts.forEach(v=>{a=Math.min(a,v);b=Math.max(b,v)}));
 const mg=Math.max(0.3,(b-a)*0.08),lo=a-mg,hi=b+mg;
 const x=i=>pad+i*(W-2*pad)/Math.max(1,n-1),y=v=>H-pad-(v-lo)/(hi-lo)*(H-2*pad);
 const y0=y(100),id='tp'+(NGID++);""",""" /* lot 66 : échelle logarithmique, bornée aux seuls tracés (plus de 100 imposé), marge de 5 % */
 let a=Infinity,b=-Infinity;const see=v=>{if(isFinite(v)&&v>0){a=Math.min(a,v);b=Math.max(b,v)}};p.forEach(see);rv.forEach(r=>r.pts.forEach(see));
 if(!isFinite(a)){a=b=100}
 const la=Math.log(a),lb=Math.log(b),mg=Math.max(0.002,(lb-la)*0.05),lo=la-mg,hi=lb+mg;
 const x=i=>pad+i*(W-2*pad)/Math.max(1,n-1),y=v=>H-pad-(Math.log(Math.max(1e-6,v))-lo)/(hi-lo)*(H-2*pad);
 const y0=Math.max(pad,Math.min(H-pad,y(100))),id='tp'+(NGID++);
 const va=Math.exp(lo),vb=Math.exp(hi);let stp=10;for(const s of [10,20,50,100,200])if(Math.floor(vb/s)-Math.ceil(va/s)+1<=7){stp=s;break}
 let grid='';for(let L=Math.ceil(va/stp)*stp;L<=vb;L+=stp){if(L<=0||L===100)continue;const yy=y(L);
  grid+=`<line x1="0" y1="${yy.toFixed(1)}" x2="${W}" y2="${yy.toFixed(1)}" stroke="#2A3A55" stroke-width=".5"/><text x="2" y="${(yy-1.5).toFixed(1)}" font-size="6.5" fill="#5B6E8C" font-family="var(--mono)">${L>100?'+':'−'}${Math.abs(L-100)} %</text>`}""")
e.rep(""" const base=`<line x1="0" y1="${f(y0)}" x2="${W}" y2="${f(y0)}" stroke="#5B6E8C" stroke-width="1"/>`;""",
""" const base=grid+(va<=100&&vb>=100?`<line x1="0" y1="${f(y0)}" x2="${W}" y2="${f(y0)}" stroke="#5B6E8C" stroke-width="1"/>`:'');""")

# ───────────── 7. calibrage des concurrents : l'adresse se dilue quand le book grossit ─────────────
# mesuré (graine 5, flux) : avec l'ancien coefficient 0,35 et un risque de 27 à 53 %, Médaillon faisait ×3,6 en deux
# ans et les rachats vidaient le fonds du joueur à +57 % de performance. 0,20 ramène ~25-35 % par an.
e.rep("const RIVNOISE={syst:0.45,fonda:0.75,flux:0.70};","const RIVNOISE={syst:0.45,fonda:0.75,flux:0.70},RIVK=0.20;")
e.rep("return (v/2)*(0.70*e/2+(RIVNOISE[rv.style]||0.78)*gauss())-0.008-rivDrag(v)-tl;","return (v/2)*(RIVK*e+(RIVNOISE[rv.style]||0.78)*gauss())-0.008-rivDrag(v)-tl;")
e.rep("const v=rivV(r);return t*((v/2)*(0.70*e/2)-0.008-rivDrag(v));","const v=rivV(r);return t*((v/2)*(RIVK*e)-0.008-rivDrag(v));")
e.rep("return {x:v,y:S.rate/4+(v/2)*0.35*E-0.008","return {x:v,y:S.rate/4+(v/2)*RIVK*E-0.008")
e.rep("base:0.15,conv:0.34,cut:0.65","base:0.16,conv:0.26,cut:0.65")
e.rep("base:0.47,conv:0,cut:0.6","base:0.40,conv:0,cut:0.6")

# ───────────── 8. nouveaux textes : 32 dépêches, 6 incidents ─────────────
NEWEV=r""",
 {t:"La Fed publie un compte rendu bien plus faucon que prévu",who:"FOMC · minutes",p:"Plusieurs membres évoquent une hausse supplémentaire. Le marché retire deux baisses de son scénario.",rum:"Un ancien économiste de la Fed consulté par le desk trouve le ton du dernier discours du président inhabituellement dur.",hit:{TN:-1.1,ES:-0.6,NQ:-0.8,EUR:-0.4,GC:-0.5}},
 {t:"Grève générale dans les ports de la côte Est américaine",who:"Syndicat des dockers · préavis",p:"Trente-six ports à l'arrêt. Les porte-conteneurs s'accumulent au large, les délais de livraison s'envolent.",rum:"Le desk matières premières note un bond des réservations de fret aérien.",hit:{BDI:1.4,ES:-0.4,CL:0.3}},
 {t:"La Chine autorise de nouveau les exportations de terres rares",who:"Pékin · ministère du Commerce",p:"Les licences suspendues depuis six mois sont rétablies d'un coup. Les industriels respirent.",rum:"Un courtier de Shanghai signale des réservations de conteneurs inhabituelles vers l'Europe.",hit:{HG:0.6,MXEF:0.7,NQ:0.4}},
 {t:"Le Japon intervient sur le yen pour la première fois en deux ans",who:"Ministère des Finances · Tokyo",p:"Plusieurs dizaines de milliards de dollars vendus en une matinée. Le yen reprend quatre figures.",rum:"Des sources au ministère évoquent un seuil de tolérance déjà franchi la semaine dernière.",hit:{JPY:1.6,TOPX:-0.6,JGB:-0.3}},
 {t:"Accord de l'OPEP+ sur une coupe surprise",who:"Vienne · communiqué",p:"Un million de barils par jour retirés du marché dès le mois prochain. Personne ne l'avait vu venir.",rum:"Un attaché commercial d'une délégation du Golfe laisse entendre que les quotas vont bouger.",hit:{CL:1.7,MXP:0.5,ES:-0.3,AUD:0.3}},
 {t:"Le Brésil annonce une taxe sur les sorties de capitaux",who:"Brasília · décret",p:"Les investisseurs étrangers paieront 6 % pour rapatrier leurs fonds. Les émergents décrochent en bloc.",rum:"Un fonds local signale des réunions nocturnes au ministère de l'Économie.",hit:{MXEF:-1.2,MXP:-0.7,GC:0.3}},
 {t:"Le bitcoin intégré aux réserves d'un État du G20",who:"Communiqué présidentiel",p:"Un premier achat de vingt mille bitcoins est annoncé. Les plateformes saturent.",rum:"Un contact dans une grande plateforme d'échange évoque un client souverain.",hit:{BTC:2.0,GC:0.3,NQ:0.3}},
 {t:"Faillite du premier promoteur immobilier chinois",who:"Tribunal de Hong Kong",p:"L'ordonnance de liquidation est prononcée. Les créanciers étrangers découvrent qu'ils passent en dernier.",rum:"Le desk crédit note des ventes forcées d'obligations en dollars du secteur depuis trois jours.",hit:{HG:-1.0,MXEF:-1.0,AUD:-0.8,TN:0.4}},
 {t:"La BCE surprend avec une baisse de 50 points",who:"Francfort · conférence de presse",p:"La présidente parle d'un « risque de déflation qu'on ne peut plus ignorer ». L'euro recule immédiatement.",rum:"Un gouverneur a accordé la veille un entretien étrangement pessimiste à un quotidien régional.",hit:{EUR:-1.2,ESTX:0.8,GBL:0.9,OAT:0.8}},
 {t:"Gel tardif sur le café au Brésil",who:"Minas Gerais · météo",p:"Deux nuits sous zéro en pleine floraison. Les coopératives parlent de la pire récolte depuis vingt ans.",rum:"Les modèles saisonniers du desk annonçaient une descente d'air polaire inhabituelle.",hit:{KC:2.2}},
 {t:"Accord sur la dette américaine arraché à deux jours du défaut",who:"Congrès · vote de nuit",p:"Le plafond est relevé pour deux ans. Le Trésor va devoir émettre massivement pour reconstituer sa trésorerie.",rum:"Un lobbyiste du Capitole assure que les chefs de groupe ont un texte depuis une semaine.",hit:{ES:0.6,TN:-0.7,GC:-0.4,VX:-0.8}},
 {t:"Le VIX double en une séance sans nouvelle",who:"Chicago · clôture",p:"Des vendeurs de volatilité débouclent en catastrophe. Personne ne sait qui a commencé.",rum:"Un market maker d'options signale des positions courtes de volatilité énormes chez un seul client.",hit:{VX:2.4,ES:-0.9,NQ:-1.1,JPY:0.5}},
 {t:"Le Royaume-Uni annonce un budget non financé",who:"Chancelier de l'Échiquier · Westminster",p:"Des baisses d'impôts massives sans une ligne de financement. Les gilts et la livre décrochent ensemble.",rum:"Un ancien du Trésor britannique dit que l'Office budgétaire n'a pas été consulté.",hit:{GBP:-1.5,R:-1.3,ESTX:-0.3}},
 {t:"Résultats stratosphériques d'un géant des semi-conducteurs",who:"Publication trimestrielle · après clôture",p:"Chiffre d'affaires doublé, prévisions relevées de 40 %. Tout le secteur technologique s'embrase.",rum:"Des fournisseurs taïwanais parlent de commandes au-delà de toutes leurs capacités.",hit:{NQ:1.5,ES:0.6,TOPX:0.4}},
 {t:"Le marché du carbone européen suspend ses enchères",who:"Commission européenne",p:"Une fraude sur les registres nationaux a été découverte. Les enchères sont gelées pour un mois.",rum:"Un opérateur de registre évoque des transferts de quotas anormaux depuis un pays membre.",hit:{EUA:-1.6}},
 {t:"La Banque du Japon abandonne le contrôle de la courbe",who:"Tokyo · réunion de politique monétaire",p:"Le plafond du rendement à dix ans saute. Les investisseurs japonais rapatrient leurs capitaux.",rum:"Des sources proches du gouverneur évoquent une « normalisation qui ne peut plus attendre ».",hit:{JGB:-1.4,JPY:1.1,TN:-0.5,GBL:-0.4}},
 {t:"L'Inde interdit les exportations de blé",who:"New Delhi · ordonnance",p:"La canicule a amputé la récolte. Le premier producteur mondial ferme ses frontières sans délai.",rum:"Le desk agricole a relevé des achats de l'État indien sur ses propres marchés intérieurs.",hit:{ZW:1.8,MXEF:-0.3}},
 {t:"Découverte d'un gisement géant de cuivre au Chili",who:"Codelco · annonce",p:"Des réserves estimées à dix ans de production mondiale. Les minières rivales perdent un cinquième en séance.",rum:"Un géologue consulté par le desk évoque des carottages exceptionnels dans l'Atacama.",hit:{HG:-1.4,AUD:-0.4}},
 {t:"Élection surprise d'un candidat hostile à l'euro",who:"Soirée électorale · capitale européenne",p:"Le vainqueur promet un référendum sur la monnaie unique. Les écarts de taux s'ouvrent dès l'ouverture.",rum:"Les sondages internes des partis, consultés par le desk, montraient une remontée tardive.",hit:{EUR:-1.1,ESTX:-1.0,OAT:-0.8,GBL:0.8,GC:0.6}},
 {t:"Un grand assureur-vie japonais vend ses obligations étrangères",who:"Tokyo · communiqué",p:"Le rapatriement porte sur des dizaines de milliards de dollars. Les taux longs occidentaux montent.",rum:"Un vendeur obligataire note des lignes inhabituelles vendues via un intermédiaire japonais.",hit:{TN:-0.9,GBL:-0.7,OAT:-0.6,JPY:0.8}},
 {t:"Chiffres de l'emploi américain catastrophiques",who:"Bureau des statistiques · premier vendredi",p:"Deux cent mille emplois détruits, révisions en baisse. Le mot récession est dans toutes les notes.",rum:"Les données de paie d'un grand prestataire, consultées par le desk, se sont effondrées.",hit:{TN:1.4,ES:-0.8,NQ:-0.7,CL:-0.6,GC:0.7,EUR:0.5}},
 {t:"Accord commercial sino-américain signé",who:"Maison-Blanche · cérémonie",p:"Les droits de douane reviennent aux niveaux d'avant la guerre commerciale. Les cycliques explosent.",rum:"Un conseiller commercial évoque des navettes discrètes de négociateurs à Genève.",hit:{MXEF:1.2,HG:0.9,AUD:0.8,ES:0.6,TOPX:0.5}},
 {t:"Pénurie de gaz annoncée pour l'hiver en Europe",who:"Régulateurs de l'énergie · alerte",p:"Les stocks ne seront pas remplis à temps. Les industriels sont prévenus de coupures possibles.",rum:"Les flux physiques suivis par le desk montrent des injections bien sous la normale.",hit:{EUA:0.8,ESTX:-0.7,EUR:-0.6,CL:0.5}},
 {t:"Le Mexique nationalise son secteur du lithium",who:"Mexico · décret présidentiel",p:"Les concessions étrangères sont annulées sans indemnité précise. Le peso vacille.",rum:"Un avocat d'affaires de Mexico évoque un texte prêt depuis des mois.",hit:{MXP:-1.1,MXEF:-0.4}},
 {t:"Tempête solaire : les satellites de navigation perturbés",who:"Agence spatiale · alerte",p:"Le GPS dérive de plusieurs kilomètres pendant six heures. Le transport maritime et aérien ralentit.",rum:"Les observatoires suivis par le desk signalaient une éruption de classe X trois jours plus tôt.",hit:{BDI:-0.6,CL:-0.4,VX:0.6}},
 {t:"La Suisse abandonne son plancher de change",who:"Banque nationale suisse · communiqué",p:"Sans préavis. Le franc bondit de 15 % en quelques minutes, les courtiers de détail sautent.",rum:"Un banquier zurichois s'étonnait du silence de la BNS sur ses réserves.",hit:{EUR:-0.9,GC:0.7,VX:0.9,ESTX:-0.5}},
 {t:"Le Congrès américain adopte un plan d'infrastructures géant",who:"Washington · vote final",p:"Deux mille milliards sur dix ans, cuivre et acier en tête. Les industriels relèvent leurs prévisions.",rum:"Des lobbyistes du secteur du BTP parlent d'un compromis trouvé en commission.",hit:{HG:1.1,ES:0.5,TN:-0.6,AUD:0.4}},
 {t:"Vague de défauts sur les prêts étudiants américains",who:"Département de l'Éducation",p:"La reprise des remboursements tourne mal : un emprunteur sur cinq ne paie plus. La consommation fléchit.",rum:"Le desk crédit note un bond des retards de paiement sur les cartes de crédit des moins de trente ans.",hit:{ES:-0.6,TN:0.7,NQ:-0.4}},
 {t:"L'Arabie saoudite ouvre les vannes",who:"Riyad · ministère de l'Énergie",p:"Le royaume abandonne la défense des prix et vise des parts de marché. Le brut perd un dixième en deux séances.",rum:"Des affréteurs signalent des réservations massives de supertankers au départ du Golfe.",hit:{CL:-2.0,MXP:-0.6,AUD:-0.3,ES:0.3}},
 {t:"Le rapport sur l'inflation européenne dépasse toutes les prévisions",who:"Eurostat · estimation rapide",p:"Sous-jacent à 4,8 %, services en accélération. La BCE ne pourra pas baisser.",rum:"Les prix relevés en ligne par le desk accéléraient depuis six semaines.",hit:{GBL:-1.2,OAT:-1.1,EUR:0.6,ESTX:-0.5}},
 {t:"Ruée sur les stablecoins après la chute de l'un d'eux",who:"Plateformes crypto · 02h00",p:"Le jeton adossé au dollar tombe à 0,86. Les rachats se propagent aux autres, le bitcoin plonge.",rum:"Un analyste on-chain signale des retraits massifs des réserves de l'émetteur depuis la veille.",hit:{BTC:-2.2,NQ:-0.5,TN:0.3}},
 {t:"L'Australie relève ses taux contre toute attente",who:"Reserve Bank of Australia",p:"Le marché attendait une pause. Le dollar australien saute de deux figures.",rum:"Un ancien membre du conseil de la RBA trouve le dernier compte rendu « plus nerveux qu'il n'y paraît ».",hit:{AUD:1.4,HG:0.2}}"""
e.rep("hit:{ES:0.7,CL:0.8,TN:-0.7,ZW:0.4}}\n","hit:{ES:0.7,CL:0.8,TN:-0.7,ZW:0.4}}"+NEWEV+"\n")
e.rep("""  loss:[0.0004,0.0018],lp:-6,rc:-9}
];""","""  loss:[0.0004,0.0018],lp:-6,rc:-9},
 {t:"Fuite du code de la stratégie",who:"Incident de sécurité · grave",
  p:"Un ancien développeur a emporté le dépôt du modèle chez un concurrent. Il faut tout réécrire et prévenir les investisseurs.",
  loss:[0.002,0.009],lp:-8,rc:-10},
 {t:"Ordres passés sur un compte de test… en production",who:"Incident technique",
  p:"Un script de recette pointait sur le vrai marché. Trois cents ordres fictifs sont devenus très réels.",
  loss:[0.0010,0.0045],lp:-3,rc:-7},
 {t:"Rapport de valorisation erroné envoyé aux investisseurs",who:"Incident opérationnel",
  p:"La valeur liquidative publiée était surévaluée de 2 %. Le correctif part avec une lettre d'excuses.",
  loss:[0.0003,0.0012],lp:-7,rc:-6},
 {t:"Hameçonnage réussi sur la trésorerie",who:"Incident de sécurité",
  p:"Un faux ordre de virement signé du directeur financier a été exécuté. La banque tente de rappeler les fonds.",
  loss:[0.0008,0.004],lp:-5,rc:-9},
 {t:"Oubli de roulement sur un contrat à terme",who:"Incident opérationnel",
  p:"Personne n'a roulé la position avant l'échéance. Le fonds se retrouve à devoir livrer, ou à racheter au pire moment.",
  loss:[0.0010,0.005],lp:-3,rc:-8},
 {t:"Dépassement de limite non signalé pendant trois semaines",who:"Contrôle des risques · rapport",
  p:"Une limite de concentration était franchie depuis le début du mois. Le système d'alerte envoyait ses courriels à une adresse fermée.",
  loss:[0.0005,0.002],lp:-4,rc:-10}
];""")

# ───────────── 9. réglages après mesure (36 parties, copie figée) ─────────────
# Citadelle à 40 % finissait médiane ×0,82 en deux ans (accidents + coût du levier) : 34 %, au bord de la zone.
# 1,5 rouge par partie dont beaucoup par deuxième jaune « sous la médiane » : seuil 8 → 10 pts.
e.rep("base:0.40,conv:0,cut:0.6","base:0.34,conv:0,cut:0.6")
e.rep("if(qTotal-med<=-0.08)why.push(`${dec((med-qTotal)*100,0)} pts sous la médiane des concurrents`);","if(qTotal-med<=-0.10)why.push(`${dec((med-qTotal)*100,0)} pts sous la médiane des concurrents`);")
e.rep("8 points sous la médiane des concurrents, book vide","10 points sous la médiane des concurrents, book vide")
# garde : une partie forcée à 1,8× le modèle a tenu un accident à −105 % de l'encours. L plafonné à 40 % :
# tenir coûte au pire 60 %, couper 20 % plus l'impact, couvrir 12 % plus 8 % de trésorerie.
e.rep("const i=Math.floor(u()*TAILEV.length),ev=TAILEV[i],L=(ev.sev[0]+(ev.sev[1]-ev.sev[0])*u())*tailL(sp),good=u()<0.5;",
      "const i=Math.floor(u()*TAILEV.length),ev=TAILEV[i],L=Math.min(0.40,(ev.sev[0]+(ev.sev[1]-ev.sev[0])*u())*tailL(sp)),good=u()<0.5;")
e.rep(" const L=(0.45+0.35*u())*tailL(v),m="," const L=Math.min(0.40,(0.45+0.35*u())*tailL(v)),m=")
e.rep("function tailL(sp){return sp*Math.max(0.3,Math.min(1.2,(sp-0.15)/0.25))}","function tailL(sp){return Math.min(0.62,sp*Math.max(0.3,Math.min(1.2,(sp-0.15)/0.25)))}")
e.done("lot 66")
