# -*- coding: utf-8 -*-
"""Lot 58 — NAV instantanée, comité en cartons, événements extrêmes, collatéral, risque
marginal, plafonds de position.

Demandes d'Antoine :
- NAV : plus de flèche ni d'ancienne valeur, la seule valeur instantanée (latent compris).
- Comité : plus de valeur de jauge. Ses effets passent dans la confiance (cf(lp,rc) = lp + rc/2,
  arrondi, borné ±15 : même fonction à l'affichage et à l'application, invariant 9). Une tuile
  carton (vide, jaune, rouge) dans la barre du haut, le clic donne le détail. Un rouge impose une
  contrainte tirée parmi neuf pendant le trimestre suivant.
- Événements extrêmes : dix, ~15 % par trimestre, certains ferment des marchés au trimestre suivant.
- Collatéral : placé à chaque trimestre sur l'écran du budget, surcroît de rendement acquis,
  perte connue d'avance (probabilité × montant) tirée à la clôture.
- Budget : crans hors trésorerie grisés (ils étaient désactivés mais sans style) ; « Suivre » grisé
  quand la trésorerie ne suit pas.
- Marchés : contribution marginale au risque (R(k+1) − R(k−1))/2 au lieu de la contribution d'Euler.
- Plafond de position ±3 au départ, ±4 puis ±5 avec les cartes « Accès aux blocs ».
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
def between(a,b):
    assert e.s.count(a)==1,'debut ambigu %r'%a[:60]
    i=e.s.index(a); j=e.s.index(b,i); return e.s[i:j]

# ═══════════════ 1. confiance : repli du comité ═══════════════
e.rep("function conf(){return S.lp}   /* lot 53 : la confiance, ce sont les investisseurs */",
"""function conf(){return S.lp}   /* lot 53 : la confiance, ce sont les investisseurs */
/* lot 58 : le comité n'a plus de jauge affichée. Ce qu'il note passe dans la confiance pour moitié,
   arrondi à l'entier et borné à ±15 : cf() sert à l'affichage comme à l'application (invariant 9). */
const CFW=0.5;
function cf(lp,rc){const v=(lp||0)+CFW*(rc||0),r=Math.sign(v)*Math.round(Math.abs(v));return Math.max(-15,Math.min(15,r))||0}
/* Les textes écrits à la main disent « comité −4 », « investisseurs +3 » : on les lit en confiance. */
function fxTxt(s,x){
 if(typeof s!=='string'||!/(omité|nvestisseurs)(\\s+des risques)?\\s*[+−-]\\s*\\d/.test(s))return s;
 x=x||{};
 const RX=/([Cc]omité|[Ii]nvestisseurs)(\\s+des risques)?\\s*([+−-])\\s*(\\d+(?:,\\d+)?)/g;
 const T=[];let m;while((m=RX.exec(s)))T.push({i:m.index,n:m[0].length,w:/omité/.test(m[1])?'rc':'lp',v:(m[3]==='+'?1:-1)*parseFloat(m[4].replace(',','.')),cap:/^[CI]/.test(m[1])});
 const cond=x.risk&&(x.riskRc!==undefined||x.riskLp!==undefined);
 T.forEach(t=>{t.g=0;if(!cond)return;const cv=t.w==='rc'?x.riskRc:x.riskLp,uv=t.w==='rc'?x.rc:x.lp;
  if(cv!==undefined&&Math.abs(Math.abs(cv)-Math.abs(t.v))<1e-9&&!(uv!==undefined&&Math.abs(uv-t.v)<1e-9))t.g=1});
 const val=g=>{const tk=T.filter(t=>t.g===g);if(!tk.length)return null;
  if(g===0&&!x.gambleLp&&!x.lpIfPos&&(x.lp||x.rc))return cf(x.lp,x.rc);
  if(g===1&&(x.riskLp||x.riskRc))return cf(x.riskLp,x.riskRc);
  return cf(tk.filter(t=>t.w==='lp').reduce((a,t)=>a+t.v,0),tk.filter(t=>t.w==='rc').reduce((a,t)=>a+t.v,0))};
 const V=[val(0),val(1)],first=[true,true];let out='',p=0;
 T.forEach(t=>{out+=s.slice(p,t.i);p=t.i+t.n;
  if(first[t.g]&&V[t.g]!==null){first[t.g]=false;const v=V[t.g];out+=`${t.cap?'Confiance':'confiance'} ${v?`${v>0?'+':'−'}${Math.abs(v)}`:'inchangée'}`}
  else{first[t.g]=false;out=out.replace(/(,\\s*|\\s+et\\s+|\\s*·\\s*)$/,'');const pm=/^\\s*\\([^)]*\\)/.exec(s.slice(p));if(pm)p+=pm[0].length}});
 out+=s.slice(p);
 out=out.replace('6 points de comité','3 points de confiance');
 return out.replace(/^\\s*[,.]\\s*/,'').replace(/\\s+([,.)])/g,'$1').replace(/,\\s*([.,])/g,'$1').replace(/\\.\\s*\\./g,'.').replace(/\\(\\s*\\)/g,'').replace(/\\s{2,}/g,' ').replace(/^([a-zé])/,c=>c.toUpperCase()).trim();
}""")

old=between("function gauge(dlp,drc,why){","function pnlGz(pnl){")
e.rep(old,"""function gauge(dlp,drc,why){
 refreshGain();
 drc=Math.max(-80,Math.min(15,drc||0));
 const d=cf(dlp,drc);   /* lot 58 : un seul effet, la confiance */
 const lp0=S.lp,rc0=S.rc;
 S.lp=Math.max(0,Math.min(100,S.lp+d));S.rc=Math.max(0,Math.min(100,S.rc+drc));
 if(d||Math.abs(drc)>=0.05){S.gLog.push({why,lp:d,rc:drc});S.lastG={lp:d,rc:drc,lp0,rc0};
  if(d)toast(`${gz(d,0)}<br><span style="color:var(--dim)">${why}</span>`)}
 refreshStatus();return {lp:d,rc:drc};
}
""")
old=between("function gz(lp,rc,opt){","/* La confiance : ce que le joueur suit.")
e.rep(old,"""function gz(lp,rc,opt){
 const l0=S&&S.lp!==undefined?S.lp:60;
 const l1=Math.max(0,Math.min(100,l0+cf(lp,rc))),d=l1-l0;
 if(Math.abs(d)<0.05&&opt!=='always')return '';
 return `<span class="${cls(d)}">confiance ${sd1(d)}</span>`;
}
""")
e.rep("""function gzRows(lp,rc){return `<div class="gzr"><span>investisseurs</span><b class="${cls(lp)}">${sd1(lp)}</b></div><div class="gzr"><span>comité</span><b class="${cls(rc)}">${sd1(rc)}</b></div>`}""",
"""function gzRows(lp,rc){const c=cf(lp,rc);return `<div class="gzr"><span>confiance</span><b class="${cls(c)}">${sd1(c)}</b></div>`}""")
# valeurs déjà repliées (journal, état) : ne pas replier deux fois
e.rep("gz(S.evImmG.lp,S.evImmG.rc)","gz(S.evImmG.lp,0)")
e.rep("Math.abs(S.evImmG.rc||0)>=0.5","false")
e.rep("gz(tg.lp,tg.rc,'always')","gz(tg.lp,0,'always')")
e.rep("gz(gT.lp,gT.rc,'always')","gz(gT.lp,0,'always')")
e.rep("gz(e.lp,e.rc,'always')","gz(e.lp,0,'always')")
# prévisualisation du book dans la tuile
e.rep("const nl=Math.max(0,Math.min(100,S.lp+(S._pv.lp||0))),nr=Math.max(0,Math.min(100,S.rc+(S._pv.rc||0))),nc=nl,d=nc-conf();",
      "const nl=Math.max(0,Math.min(100,S.lp+cf(S._pv.lp,S._pv.rc))),nc=nl,d=nc-conf();")
# conseil : appliqué sans gauge()
e.rep("""  if(e.lp||e.rc)S.lastG={lp:e.lp||0,rc:e.rc||0,lp0:S.lp,rc0:S.rc};
  if(e.lp)S.lp=Math.max(0,Math.min(100,S.lp+e.lp));
  if(e.rc)S.rc=Math.max(0,Math.min(100,S.rc+e.rc));""",
"""  {const d=cf(e.lp,e.rc);if(d||e.rc)S.lastG={lp:d,rc:e.rc||0,lp0:S.lp,rc0:S.rc};
   if(d)S.lp=Math.max(0,Math.min(100,S.lp+d));
   if(e.rc)S.rc=Math.max(0,Math.min(100,S.rc+e.rc));}""")
# textes des choix lus en confiance
e.rep("""<button class="choice" data-i="${i}"${ko?' disabled title="Trésorerie insuffisante"':''}><b>${c.b}</b><span>${c.s}${stake(c)}""",
      """<button class="choice" data-i="${i}"${ko?' disabled title="Trésorerie insuffisante"':''}><b>${c.b}</b><span>${fxTxt(c.s,c.e)}${stake(c)}""")
e.rep("""<button class="choice" data-i="${i}"${ko?' disabled':''}><b>${c.b}</b><span>${c.s}${ko?' <b class="neg-g">hors trésorerie</b>':''}</span>""",
      """<button class="choice" data-i="${i}"${ko?' disabled':''}><b>${c.b}</b><span>${fxTxt(c.s,c.e)}${ko?' <b class="neg-g">hors trésorerie</b>':''}</span>""",2)
# clés de résultat
e.rep("""['Investisseurs · comité',`<span class="${cls(g0.lp+g.lp+g2.lp)}">${sd1(g0.lp+g.lp+g2.lp)}</span> · <span class="${cls(g0.rc+g.rc+g2.rc)}">${sd1(g0.rc+g.rc+g2.rc)}</span>`]""",
      """['Confiance',`<span class="${cls(g0.lp+g.lp+g2.lp)}">${sd1(g0.lp+g.lp+g2.lp)}</span>`]""")
e.rep("""['Investisseurs · comité',`<span class="${cls(g.lp+g2.lp)}">${sd1(g.lp+g2.lp)}</span> · <span class="${cls(g.rc+g2.rc)}">${sd1(g.rc+g2.rc)}</span>`]""",
      """['Confiance',`<span class="${cls(g.lp+g2.lp)}">${sd1(g.lp+g2.lp)}</span>`]""")
e.rep("""[['Jauges',`<span class="${cls(g.lp)}">${sd1(g.lp)}</span> · <span class="${cls(g.rc)}">${sd1(g.rc)}</span>`]]""",
      """[['Confiance',`<span class="${cls(g.lp)}">${sd1(g.lp)}</span>`]]""")
e.rep("""   <div class="kv"><span>Confiance investisseurs</span><b class="neg-g">${(inc.lp*sev).toFixed(0)}</b></div>
   <div class="kv"><span>Comité des risques</span><b class="neg-g">${(inc.rc*sev).toFixed(0)}</b></div>""",
"""   <div class="kv"><span>Confiance</span><b class="${cls(g.lp)}">${sd1(g.lp)}</b></div>""")
e.rep("""tbl([...S.gLog.map(g=>[g.why,sd1(g.lp),sd1(g.rc)]),...S.lpD.map(x=>[x[0],sd1(x[1]),'']),...S.rcD.map(x=>[x[0],'',sd1(x[1])]),['<b>Total</b>',sd1(gT.lp),sd1(gT.rc)]],['Cause','Inv.','Com.'])""",
      """tbl([...S.gLog.filter(g=>g.lp).map(g=>[g.why,sd1(g.lp)]),...S.lpD.map(x=>[x[0],sd1(x[1])]),['<b>Total</b>',sd1(gT.lp)]],['Cause','Confiance'])""")

# ═══════════════ 2. dépêches : une colonne Confiance, suivre grisé si interdit ou hors caisse ═══════════════
e.rep("""  if(trades.length){const r=reactGz(p);lp+=r.lp;rc+=r.rc;fixRc.forEach(x=>rc+=x[0])}
  return {lp,rc,pnl:a}});""",
"""  let c=cf(a.lp,a.rc);   /* lot 58 : la somme exacte de ce que gauge() appliquera, appel par appel */
  if(trades.length){const r=reactGz(p);lp+=r.lp;rc+=r.rc;c+=cf(r.lp,r.rc);fixRc.forEach(x=>{rc+=x[0];c+=cf(0,x[0])})}
  return {lp:c,rc,pnl:a}});""")
e.rep("""gz:payN.map(p=>{const a=pnlGz(p);return {lp:a.lp,rc:a.rc,pnl:a}})""","""gz:payN.map(p=>{const a=pnlGz(p);return {lp:cf(a.lp,a.rc),rc:a.rc,pnl:a}})""")
e.rep("""<span class="ph pn">Confiance</span><span class="ph pn">⚖️</span>""","""<span class="ph pn">Confiance</span>""")
e.rep("""${gcell(o.gz[s].lp)}${gcell(o.gz[s].rc)}""","""${gcell(o.gz[s].lp)}""")
e.rep(".choice .ptab{display:grid;grid-template-columns:minmax(0,1.5fr) repeat(4,minmax(0,1fr));",".choice .ptab{display:grid;grid-template-columns:minmax(0,1.5fr) repeat(3,minmax(0,1fr));")
e.rep("""   ${plan.map((o,i)=>`<button class="choice evopt" data-i="${i}"><b>${o.b}</b><span class="evs">${o.s}</span>${ptab(o)}</button>`).join('')}""",
"""   ${plan.map((o,i)=>{const ban=o.a==='follow'&&o.trades.length&&(redOn('risk')||redOn('noadd')),ko=o.a==='follow'&&o.cost>0&&o.cost>Math.max(0,mgrCash());
     return `<button class="choice evopt" data-i="${i}"${ban||ko?' disabled':''}><b>${o.b}</b><span class="evs">${o.s}${ban?' <b class="neg-g">interdit par le comité (carton rouge)</b>':ko?' <b class="neg-g">hors trésorerie</b>':''}</span>${ptab(o)}</button>`}).join('')}""")
# marchés fermés par l'événement : on ne peut plus y passer d'ordre
e.rep("""touched.forEach(i=>{const sh=Math.sign(ev.hit[INSTR[i].sym]);
  const tg=clampK(i,S.k[i]+sh*2),d=tg-S.k[i];if(!d)return;""","""touched.forEach(i=>{const sh=Math.sign(ev.hit[INSTR[i].sym]);
  if(ev.shut&&ev.shut.includes(INSTR[i].sym))return;   /* lot 58 : cotation suspendue */
  const tg=clampK(i,S.k[i]+sh*2),d=tg-S.k[i];if(!d)return;""")

# ═══════════════ 3. NAV instantanée ═══════════════
e.rep("""<b>${(()=>{const q0=S.navQ0||0,d=q0?S.nav/q0-1:0;
     return (S.phase!=='budget'&&Math.abs(d)>0.002)
      ?`<span class="dim-g" style="font-weight:400">${moneyB(q0)}</span> <span class="${cls(d)}">→${moneyB(S.nav)}</span>`
      :moneyB(S.nav)})()}</b></button>""","""<b id="navtile">${moneyB(navNow())}</b></button>""")
e.rep("""function liveRet(){""","""/* lot 58 : encours instantané, latent des positions et collatéral couru compris — le ruban,
   la tuile « Perf. » et la tuile d'encours disent la même chose au même instant */
function navNow(){if(!S)return 0;if(S.phase!=='events'||!S.live||!S.rBase)return S.nav;
 const t=qElapsed(),w=weights(S.k);let g=0;for(let i=0;i<N;i++)g+=w[i]*S.rBase[i];g+=colYield();return S.nav*(1+t*g)}
function liveRet(){""")
e.rep(" g+=S.rate/4;   /* le collatéral court aussi"," g+=colYield();   /* le collatéral court aussi")
e.rep("['Encours actuel',moneyB(S.nav)]","['Encours actuel',moneyB(navNow())]")

# ═══════════════ 4. cartons : tuile, pop-up, contraintes ═══════════════
e.rep("""<span><i>Confiance des investisseurs${S.cards&&(S.cards.y||S.redOn)?` <span class="cardb">${S.redOn?'🟥 ±3':'🟨'.repeat(S.cards.y)}</span>`:''}</i>""",
      """<span><i>Confiance</i>""")
e.rep("""   <button class="tile gold" data-gauge="gain" style="flex:.95">""","""   ${cardTile()}
   <button class="tile gold" data-gauge="gain" style="flex:.95">""")
e.rep(".cardb{font-style:normal;margin-left:4px;font-size:11px}",""".cardb{font-style:normal;margin-left:4px;font-size:11px}
.tile.cardt{flex:0 0 38px;align-items:center;justify-content:center;padding:4px}
.tile.cardt svg{display:block}
.lvl[disabled],.coll[disabled]{opacity:.25;cursor:not-allowed}
.seg button[disabled]{cursor:not-allowed}
.redflag{border-left:3px solid #D2463C;background:rgba(210,70,60,.08);padding:7px 10px;border-radius:4px;font-size:13px;margin:0 0 10px}
.evcard.xtr{border-color:#D2463C}
.xtag{font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;color:#fff;background:#D2463C;display:inline-block;padding:2px 8px;border-radius:3px;margin-bottom:8px}
.colls{display:grid;grid-template-columns:1fr 1fr;gap:6px}
.coll{text-align:left;padding:8px;border-radius:6px;background:var(--panel2);border:1px solid transparent;display:flex;flex-direction:column;gap:2px}
.coll.on{background:var(--panel);border-color:var(--gold)}
.coll b{font-size:13px}.coll span{font-family:var(--mono);font-size:10.5px}.coll .ci{font-size:15px}""")

old=between("} else if(id==='lp'){","} else if(id[0]==='f'){")
e.rep(old,"""} else if(id==='lp'){
  const dl=S.lpD,row=x=>[x[0],`<span class="${cls(x[1])}">${x[1]>=0?'+':'−'}${Math.abs(x[1]).toFixed(1)}</span>`];
  openModal('Confiance des investisseurs',`<p>La confiance, ce sont vos investisseurs : ils suivent la performance nette, les plus hauts historiques, la comparaison avec les trois concurrents, et se détournent avec les pertes, les replis, les incidents. Ce que le comité des risques reproche à votre book s'y ajoute pour moitié. Sous <em>20</em>, des rachats partent à chaque clôture.</p>
   ${tbl([['Confiance',`<b>${Math.round(conf())}</b>`]])}
   ${dl?tbl(dl.map(row),['Investisseurs · dernier trimestre','Δ']):''}`);
 } else if(id==='card'){
  const C=S.cards||{y:0,r:0,log:[]},rc=S.redOn?S.redC:null,rn=S.redNext&&typeof S.redNext==='object'?S.redNext:null;
  const head=rc?`<p><b>🟥 Carton rouge — contrainte en vigueur ce trimestre.</b><br>${rc.nm} : ${rc.t}.</p>`
   :rn?`<p><b>🟥 Carton rouge.</b> Au prochain trimestre, le comité impose : ${rn.nm} — ${rn.t}.</p>`
   :C.y?`<p><b>🟨 Un carton jaune en cours.</b> Au prochain manquement, c'est le rouge.</p>`
   :`<p><b>Aucun carton.</b> Le comité vous laisse travailler.</p>`;
  openModal('Le comité des risques',`${head}
   ${tbl([['Plafond de position',`±${S.maxk} unité${S.maxk>1?'s':''}${(S.capK||5)<5?` <span class="dim-g">· ±${(S.capK||5)+1} avec l'accès aux blocs</span>`:''}`],['Bande de volatilité',`${pct(S.tgt,0)} ±${(bandNow()*100).toFixed(0)} %`]])}
   <p style="margin-top:10px">Le comité ne tient pas de jauge : il juge le book à chaque clôture et sort des cartons. Ce qu'il note entre-temps pèse sur la confiance ; trop de griefs dans un trimestre valent un jaune.</p>
   <ul class="rules2"><li>🟥 <b>Rouge</b> : risque au double de la cible, perte au-delà de 2,2 σ, appel de marge, ou deuxième jaune.</li><li>🟨 <b>Jaune</b> : book validé au-dessus de la bande de volatilité, plus de 75 % du risque sur un facteur, book vide, griefs accumulés.</li><li>Un rouge coûte 5 % de l\\'encours, 6 points de confiance, et une contrainte forte pendant le trimestre suivant, tirée au sort : plafond de position, risque plafonné, stop ex post, marchés ou classe fermés, collatéral renforcé, book resserré, contrôle imposé, gel des renforcements.</li><li>Quatre trimestres propres d\\'affilée retirent un jaune.</li></ul>
   ${C.log.length?tbl(C.log.slice(-4).map(l=>[`T${l.q}`,`${l.c==='rouge'?'🟥':'🟨'} ${l.why}${l.cn?` → ${l.cn}`:''}`]),['Derniers cartons','']):''}`);
 """)

# contraintes
e.rep("function budgetBp(){return BUDGET.reduce(","""/* ── lot 58 : un carton rouge impose une contrainte au trimestre suivant, tirée parmi neuf ── */
const REDC=[
 {id:'cap',nm:'Plafond de position',t:'±2 unités au plus sur chaque marché'},
 {id:'risk',nm:'Risque plafonné',t:'risque ex ante du book limité à 70 % de la cible, aucun renforcement sur les dépêches'},
 {id:'expost',nm:'Stop ex post',t:'au-delà de −4 % brut sur le trimestre, le comité coupe les trois quarts du book'},
 {id:'shut',nm:'Marchés fermés',t:''},
 {id:'class',nm:'Classe interdite',t:''},
 {id:'collat',nm:'Collatéral renforcé',t:"40 % de l'encours en dépôt de garantie non rémunéré, placement imposé en bons du Trésor"},
 {id:'lines',nm:'Book resserré',t:'quatre lignes ouvertes au plus'},
 {id:'budget',nm:'Contrôle imposé',t:'budget de contrôle des risques au cran 5 au moins, à vos frais'},
 {id:'noadd',nm:'Gel des renforcements',t:'risque ex ante sous la cible, sans bande, et aucun renforcement sur les dépêches'},
];
function redOn(id){return !!(S&&S.redOn&&S.redC&&S.redC.id===id)}
function redDraw(w){
 const u=prng32(hash32('redc'+S.q+'_'+((S.cards&&S.cards.r)||0),S.seed));
 const av=REDC.filter(c=>c.id!==S.redLast),c=Object.assign({},av[Math.floor(u()*av.length)]);
 if(c.id==='shut'){const rc=riskContrib(w);
  let o=INSTR.map((x,i)=>({i,v:Math.abs(rc[i]||0)})).filter(z=>mktOpen(z.i)).sort((a,b)=>b.v-a.v||a.i-b.i);
  if(!(o[0]&&o[0].v>1e-9))o=o.map(z=>({i:z.i,v:u()})).sort((a,b)=>b.v-a.v);
  c.syms=o.slice(0,3).map(z=>INSTR[z.i].sym);c.t=`${c.syms.join(', ')} fermés au fonds`}
 if(c.id==='class'){const cl=[...new Set(INSTR.filter((x,i)=>mktOpen(i)).map(x=>x.grp))];
  const g=cl[Math.floor(u()*cl.length)];c.syms=INSTR.filter((x,i)=>x.grp===g&&mktOpen(i)).map(x=>x.sym);
  c.t=`toute la classe « ${g.toLowerCase()} » interdite (${c.syms.join(', ')})`}
 if(c.syms){S.shut=S.shut||{};c.syms.forEach(sy=>S.shut[sy]=S.q)}   /* fermés pendant le trimestre qui vient */
 S.redLast=c.id;return c;
}
/* Ce qui bloque la validation du book sous contrainte (vide si rien) */
function redBlock(){
 if(S.k.some((v,i)=>Math.abs(v)>kCap(i)))return 'Positions au-delà des plafonds';
 if(!S.redOn||!S.redC)return '';
 const id=S.redC.id,sp=riskShown(weights(S.k)).total;
 if(id==='risk'&&sp>0.7*S.tgt+1e-9)return `Carton rouge : risque ${pct(sp)}, plafond ${pct(0.7*S.tgt)}`;
 if(id==='noadd'&&sp>S.tgt+1e-9)return `Carton rouge : risque ${pct(sp)}, plafond ${pct(S.tgt)}`;
 if(id==='lines'){const n=S.k.filter(v=>v).length;if(n>4)return `Carton rouge : ${n} lignes, quatre au plus`}
 return '';
}
function redNote(){return S.redOn&&S.redC?`<div class="redflag">🟥 <b>Contrainte du comité ce trimestre</b> — ${S.redC.nm} : ${S.redC.t}.</div>`:''}
function cardTile(){const C=S.cards||{y:0};const st=(S.redOn||S.redNext)?'r':C.y?'y':'n';
 const r=st==='n'?'fill="none" stroke="var(--dimmer)" stroke-width="1.4" stroke-dasharray="3 2"':`fill="${st==='r'?'#D2463C':'#E8C547'}"`;
 return `<button class="tile cardt" data-gauge="card" aria-label="Carton du comité"><svg viewBox="0 0 18 24" width="17" height="23"><rect x="1.5" y="1.5" width="15" height="21" rx="2.5" ${r}/></svg></button>`}
function budgetBp(){return BUDGET.reduce(""")
e.rep("function mktOpen(i){const x=INSTR[i];return !!x&&x.rk<=OPENRK&&(x.grp!=='Exotiques'||!!(S&&S.exoOpen))}",
      "function mktOpen(i){const x=INSTR[i];return !!x&&x.rk<=OPENRK&&(x.grp!=='Exotiques'||!!(S&&S.exoOpen))&&!(S&&S.shut&&S.shut[x.sym]===S.q)}")
# clôture : le rouge tire sa contrainte
e.rep("""  if(red){C.r++;C.y=0;C.clean=0;S.qCard={c:'rouge',why:red};C.log.push({q:S.q,c:'rouge',why:red});
   S.redNext=true;""","""  if(red){C.r++;C.y=0;C.clean=0;const rn=redDraw(wFin);S.qCard={c:'rouge',why:red,cn:rn};C.log.push({q:S.q,c:'rouge',why:red,cn:rn.nm});
   S.redNext=rn;""")
e.rep("""Mandat réduit à ±3 unités au prochain trimestre, 5 % de l'encours retiré, confiance −6.`""",
      """Au prochain trimestre : <b>${S.qCard.cn.nm}</b> — ${S.qCard.cn.t}. 5 % de l'encours retiré, confiance −6.`""")
# ouverture du trimestre : plafond de base, contrainte en vigueur
e.rep(" if(S.redNext){S.maxk=3;S.redNext=false;S.redOn=true}else if(S.redOn){S.maxk=5;S.redOn=false}",
""" if(S.redNext){S.redC=typeof S.redNext==='object'?S.redNext:{id:'cap',nm:'Plafond de position',t:'±2 unités au plus sur chaque marché'};S.redNext=false;S.redOn=true}
 else if(S.redOn){S.redOn=false;S.redC=null}
 S.maxk=S.capK||5;if(redOn('cap'))S.maxk=Math.min(S.maxk,2);   /* lot 58 : plafond de base ±3, ±4, ±5 */""")
e.rep("tgt:V.tgt,maxk:5,rate:0.0425","tgt:V.tgt,maxk:3,capK:3,rate:0.0425")
# stop ex post du comité
e.rep(" if((S.stop||S.stopQ)&&gross<-0.08)gross=-0.08+(gross+0.08)*0.5;",
      " if((S.stop||S.stopQ)&&gross<-0.08)gross=-0.08+(gross+0.08)*0.5;\n if(redOn('expost')&&gross<-0.04){gross=-0.04+(gross+0.04)*0.25;S.qLog.push('stop du comité')}")
# book : note de contrainte, validation gardée, ajustement automatique
e.rep("""  <div class="block"><div class="blockhead"><h2>Le book</h2><span class="hint">unités de risque, de −${S.maxk} à +${S.maxk}</span></div>""",
      """  <div class="block"><div class="blockhead"><h2>Le book</h2><span class="hint">unités de risque, de −${S.maxk} à +${S.maxk}</span></div>
   ${redNote()}""")
e.rep("""   <details style="margin:0 0 8px"><summary>Le surlevier, au-delà de ±3</summary>""","""   <details style="margin:0 0 8px"${S.maxk>3?'':' hidden'}><summary>Le surlevier, au-delà de ±3</summary>""")
e.rep(""" const c=liveTC(),rest=mgrCash(),avail=Math.max(0,rest+c),ko=c>0&&c>avail;""",""" const c=liveTC(),rest=mgrCash(),avail=Math.max(0,rest+c),ko=c>0&&c>avail,rb=redBlock();""")
e.rep("""   +(ko?` <button class="buy" id="fitbook" style="margin-left:8px">Ramener le book au payable</button>`:'');""",
      """   +(ko||rb?` <button class="buy" id="fitbook" style="margin-left:8px">${rb?'Ramener le book dans la contrainte':'Ramener le book au payable'}</button>`:'');""")
e.rep(""" b.disabled=ko;
 b.textContent=ko?`Trésorerie insuffisante : ${mm(c-avail)} de trop`:'Passer les ordres';""",""" b.disabled=ko||!!rb;
 b.textContent=rb||(ko?`Trésorerie insuffisante : ${mm(c-avail)} de trop`:'Passer les ordres');""")
e.rep("""   if(c>0&&c>Math.max(0,mgrCash()+c)){refreshSend();toast("Votre société de gestion ne peut pas payer ces ordres.");return}""",
      """   if(c>0&&c>Math.max(0,mgrCash()+c)){refreshSend();toast("Votre société de gestion ne peut pas payer ces ordres.");return}
   if(redBlock()){refreshSend();toast(redBlock());return}""")
e.rep("""function fitBook(){
 for(let g=0;g<400;g++){""","""function fitBook(){
 /* lot 58 : plafonds et contrainte du comité d'abord, trésorerie ensuite */
 S.k=S.k.map((v,i)=>clampK(i,v));
 for(let g=0;g<80&&redBlock();g++){
  const w=weights(S.k),rc=riskContrib(w);let bi=-1,bv=-1;
  if(redOn('lines')){for(let i=0;i<N;i++)if(S.k[i]&&(bi<0||Math.abs(rc[i])<bv)){bv=Math.abs(rc[i]);bi=i}if(bi>=0)S.k[bi]=0}
  else{for(let i=0;i<N;i++)if(S.k[i]&&rc[i]>bv){bv=rc[i];bi=i}if(bi<0)break;S.k[bi]-=Math.sign(S.k[bi])}
 }
 for(let g=0;g<400;g++){""")
# marché fermé : badge
e.rep("""   if(!mktOpen(i)){h+=`<div class="pos locked"><div class="top"><span class="sym" style="color:${GRPC[g]}">${x.sym}</span><span class="nm"><span class="mflag">${MFLAG[x.sym]||''}</span>${x.nm}</span>${x.grp==='Exotiques'&&x.rk<=OPENRK""",
      """   if(!mktOpen(i)){h+=`<div class="pos locked"><div class="top"><span class="sym" style="color:${GRPC[g]}">${x.sym}</span><span class="nm"><span class="mflag">${MFLAG[x.sym]||''}</span>${x.nm}</span>${S.shut&&S.shut[x.sym]===S.q?'<span class="capb">🔒 fermé ce trimestre</span>':x.grp==='Exotiques'&&x.rk<=OPENRK""")

# ═══════════════ 5. plafonds : ±3, puis ±4 et ±5 avec l'accès aux blocs ═══════════════
e.rep("""B('blocs',g>=1.3,()=>{S.capBoost=Math.max(S.capBoost||1,1.5);S.execPenalty=Math.max(0.7,S.execPenalty*0.9);
  return {v:'key',k:'CROISSANCE · ENCOURS ×1,3',tier:'bronze',t:'Accès aux blocs',d:"Les grandes maisons vous proposent désormais leurs blocs de gré à gré.",g:'plafonds de capacité ×1,5 · coûts d\\'exécution −10 %'}});""",
"""B('blocs',g>=1.2,()=>{S.capBoost=Math.max(S.capBoost||1,1.5);S.execPenalty=Math.max(0.7,S.execPenalty*0.9);S.capK=Math.max(S.capK||3,4);
  return {v:'key',k:'CROISSANCE · ENCOURS ×1,2',tier:'bronze',t:'Accès aux blocs',d:"Les grandes maisons vous proposent désormais leurs blocs de gré à gré.",g:'plafond de position ±4 · profondeur ×1,5 · coûts d\\'exécution −10 %'}});
 B('blocs2',g>=1.5,()=>{S.capK=Math.max(S.capK||3,5);
  return {v:'key',k:'CROISSANCE · ENCOURS ×1,5',tier:'argent',t:'Accès aux blocs · premier cercle',d:"Les desks de gré à gré vous servent avant les autres, et en taille.",g:'plafond de position ±5'}});""")

# ═══════════════ 6. collatéral placé chaque trimestre ═══════════════
e.rep("function budgetBpIf(id,lv){","""/* lot 58 : placement du collatéral. Le surcroît de rendement est acquis au fil du trimestre ;
   la perte, de probabilité et de montant annoncés, tombe à la clôture (tirage pur). */
const COLL=[
 {id:'tres',nm:'Bons du Trésor',ico:'🏛️',y:0,p:0,l:0,d:"Le taux sans risque, rien de plus, rien de moins."},
 {id:'mmf',nm:'Monétaire prime',ico:'💧',y:0.003,p:0.05,l:0.02,d:"Du papier commercial bien noté. Rarement un problème, jamais zéro."},
 {id:'repo',nm:'Repo contre crédit',ico:'🔁',y:0.007,p:0.10,l:0.04,d:"Vous prêtez contre des obligations d'entreprises : le gage vaut ce que vaut le marché du crédit."},
 {id:'abs',nm:'Titrisations',ico:'🧨',y:0.014,p:0.20,l:0.06,d:"Des tranches de prêts titrisés. Le rendement paie un risque que tout le monde connaît."},
];
function colOpt(){return COLL[(S&&S.col)||0]||COLL[0]}
function colYield(){const b=(S.rate||0)/4;return redOn('collat')?b*0.6:b+colOpt().y}
function drawColl(){
 const el=document.getElementById('colls');if(!el)return;const lock=redOn('collat');if(lock)S.col=0;
 el.innerHTML=(lock?redNote():'')+`<div class="colls">${COLL.map((o,i)=>`<button class="coll ${(S.col||0)===i?'on':''}" data-c="${i}"${lock&&i?' disabled':''}>
   <b><span class="ci">${o.ico}</span> ${o.nm}</b><span class="${o.y?'pos-g':'dim-g'}">${o.y?`+${dec(o.y*100,1)} % · ${mm(o.y*S.nav)}`:'taux sans risque'}</span>
   <span class="${o.p?'neg-g':'dim-g'}">${o.p?`${Math.round(o.p*100)} % de −${dec(o.l*100,1)} %`:'aucun risque'}</span></button>`).join('')}</div>
  <p class="note" style="margin-top:6px">${colOpt().d} ${colOpt().p?`Espérance ${sgn(colOpt().y-colOpt().p*colOpt().l,1)} sur le trimestre.`:''}</p>`;
 el.querySelectorAll('.coll').forEach(b=>b.onclick=()=>{S.col=+b.dataset.c;drawColl();const o=colOpt();
  toast(`Collatéral → <b>${o.nm}</b>${o.y?` · +${dec(o.y*100,1)} % par trimestre, ${Math.round(o.p*100)} % de risque de −${dec(o.l*100,1)} %`:''}`)});
}
function budgetBpIf(id,lv){""")
e.rep("""   <div class="budtot"><span>Total du trimestre</span><b id="btot"></b></div>
  </div>""","""   <div class="budtot"><span>Total du trimestre</span><b id="btot"></b></div>
  </div>
  <div class="block"><div class="blockhead"><h2>Placement du collatéral</h2><span class="hint">pour le fonds</span></div>
   <p class="note" style="margin-top:0">L'encours qui ne sert pas de marge est placé : taux sans risque ${dec(S.rate*100,1)} % l'an, ou un surcroît de rendement contre un risque de perte connu d'avance, tiré à la clôture.</p>
   <div id="colls"></div></div>""")
e.rep(""" drawBuds();
 document.getElementById('ok').onclick=()=>{""",""" drawBuds();drawColl();
 document.getElementById('ok').onclick=()=>{""")
# budget : contrôle imposé, et un budget reconduit qui dépasse la caisse redescend
e.rep(""" S.mgrCosts-=S.qOps||0;S.qOps=budgetBp()*1e-4*S.nav;S.mgrCosts+=S.qOps;
 app.innerHTML=statusBar()+`<div class="fade">
  <div class="block"><div class="blockhead"><h2>Budget d'exploitation du trimestre</h2>""",""" S.mgrCosts-=S.qOps||0;S.qOps=0;
 {const purse=mgrCash(),fits=()=>budgetBp()*1e-4*S.nav<=purse+1e-12;
  if(redOn('budget')&&S.bud.risk<5){for(let l=5;l>S.bud.risk;l--){const o=S.bud.risk;S.bud.risk=l;if(fits())break;S.bud.risk=o}}
  for(let g=0;g<40&&!fits();g++){let bi=null,bv=0;BUDGET.forEach(b=>{const l=S.bud[b.id];if(l>(redOn('budget')&&b.id==='risk'?5:0)&&b.lv[l].bp>bv){bv=b.lv[l].bp;bi=b.id}});
   if(!bi)break;S.bud[bi]--;if(bi==='exec')S.bud.ret=S.bud.exec}}
 S.qOps=budgetBp()*1e-4*S.nav;S.mgrCosts+=S.qOps;
 app.innerHTML=statusBar()+`<div class="fade">
  <div class="block"><div class="blockhead"><h2>Budget d'exploitation du trimestre</h2>""")
e.rep(""" const ok=(id,i)=>i===0||budgetBpIf(id,i)*1e-4*S.nav<=purse;""",""" const ok=(id,i)=>(i===0||budgetBpIf(id,i)*1e-4*S.nav<=purse)&&!(id==='risk'&&redOn('budget')&&i<5&&i<S.bud.risk);""")
e.rep("""  <div class="block"><div class="blockhead"><h2>Budget d'exploitation du trimestre</h2><span class="hint">à votre charge</span></div>""",
      """  <div class="block"><div class="blockhead"><h2>Budget d'exploitation du trimestre</h2><span class="hint">à votre charge</span></div>
   ${redNote()}""")
# clôture : rendement et perte du collatéral
e.rep(" const collateral=S.rate/4;\n",""" const cO=colOpt(),cHit=!redOn('collat')&&cO.p>0&&prng32(hash32('coll'+S.q,S.seed))()<cO.p;
 const collateral=colYield()-(cHit?cO.l:0);
 S.colRes={nm:redOn('collat')?'Collatéral renforcé':cO.nm,x:collateral-S.rate/4,hit:cHit,l:cO.l,m:(collateral-S.rate/4)*S.nav,show:redOn('collat')||cO.id!=='tres'};
""")
e.rep("""   <div class="attr"><span class="an">Rémunération du collatéral</span><span class="av">${inU(o.P.collM,UQ)}</span></div>""",
      """   <div class="attr"><span class="an">Rémunération du collatéral</span><span class="av">${inU(o.P.collM,UQ)}</span></div>${S.colRes&&S.colRes.show?`
   <div class="attr"><span class="an" style="color:var(--dimmer)">dont ${S.colRes.nm.toLowerCase()}${S.colRes.hit?' · défaut':''}</span><span class="av">${inU(S.colRes.m,UQ)}</span></div>`:''}""")
e.rep(""" if(S.qGoal)warn.push(`Objectif du trimestre""",""" if(S.colRes&&S.colRes.hit)warn.push(`💥 <b>Le placement du collatéral a fait défaut</b> — ${S.colRes.nm} : −${dec(S.colRes.l*100,1)} % de l'encours, surcroît de rendement compris ${sgn(S.colRes.x,1)} sur le trimestre.`);
 if(S.qGoal)warn.push(`Objectif du trimestre""")

# ═══════════════ 7. risque marginal par marché ═══════════════
e.rep("function riskAdd(i,k){","""/* lot 58 : contribution marginale, moyenne des pentes à +1 et à −1 : (R(k+1) − R(k−1)) / 2, en points.
   Book vide : l'effet d'une unité (les deux pentes sont alors égales en valeur absolue). */
function riskMarg(i,k){const R=kk=>riskShown(weights(kk)).total,kp=[...k],km=[...k];kp[i]=(kp[i]||0)+1;km[i]=(km[i]||0)-1;
 return (k.some(v=>v)?(R(kp)-R(km))/2:R(kp)-R(k))*100}
function riskAdd(i,k){""")
e.rep("""rp=S.k[i]?riskPts(S.k)[i]:riskAdd(i,S.k);
  gl=`""","""rp=riskMarg(i,S.k);
  gl=`""")
e.rep("""<span class="xk" style="margin-left:7px">${S.k[i]?'risque':'+1'}</span>""","""<span class="xk" style="margin-left:7px">marg.</span>""")
e.rep("""const pc=v=>`<span class="${cls(v)}">${sgn(v,1)}</span>`,w1=U/x.sig,rp=S.k[i]?riskPts(S.k)[i]:riskAdd(i,S.k);""",
      """const pc=v=>`<span class="${cls(v)}">${sgn(v,1)}</span>`,w1=U/x.sig,rp=riskMarg(i,S.k);""")
e.rep("""[S.k[i]?'Contribution au risque':'Une unité ajouterait',""","""['Risque marginal (±1 unité)',""")

# ═══════════════ 8. événements extrêmes ═══════════════
e.rep("""hit:{MXEF:-1.6,MXP:-1.8,GC:0.7,VX:0.9},liq:1.5}
);""","""hit:{MXEF:-1.6,MXP:-1.8,GC:0.7,VX:0.9},liq:1.5}
);
/* lot 58 : événements extrêmes (x:1), hors du tirage ordinaire ; shut = marchés fermés au fonds le trimestre suivant */
const XPROB=0.15;
MACROEV.push(
 {x:1,t:"Faillite d'une banque systémique un dimanche soir",who:"Alerte · régulateurs réunis en urgence",p:"Aucun repreneur n'a été trouvé. Les lignes interbancaires se ferment une à une, les fonds monétaires suspendent leurs rachats et les marchés ouvrent en limite de baisse.",hit:{ES:-3.4,ESTX:-3.6,TOPX:-2.6,NQ:-3.2,MXEF:-3.2,TN:2.6,GBL:2.4,JPY:2.0,GC:2.2,VX:3.8},liq:2.2},
 {x:1,t:"Krach : Wall Street perd 18 % en une séance",who:"Clôture · New York",p:"Aucune nouvelle ne l'explique. Les ventes programmées s'enchaînent, les coupe-circuits sautent deux fois et les teneurs de marché se retirent.",hit:{ES:-4.2,NQ:-4.6,ESTX:-3.4,TOPX:-3.2,MXEF:-3.0,TN:2.2,JPY:1.8,VX:4.5,BTC:-3.0},liq:2.4},
 {x:1,t:"Les bourses de la zone euro suspendent la cotation",who:"Autorités de marché · communiqué commun",p:"Une panne de la chambre de compensation paralyse les places européennes. Les positions sont gelées : personne ne sait à quel prix elles rouvriront.",hit:{ESTX:-3.0,EUR:-2.4,GBL:1.8,OAT:-1.6,GBP:1.0,ES:-1.2},liq:1.9,shut:['ESTX','OAT']},
 {x:1,t:"La guerre éclate aux portes de l'Europe",who:"Fil d'actualité · 04h30",p:"Des colonnes blindées franchissent la frontière avant l'aube. Les sanctions tombent dans la journée ; le gaz et le blé s'envolent, les places de l'Est ferment.",hit:{CL:3.2,ZW:3.6,GC:2.6,ESTX:-3.4,EUR:-2.6,ES:-1.6,EUA:1.6,GBL:1.4},liq:1.9},
 {x:1,t:"Blocus naval autour de Taïwan",who:"Fil d'actualité · 02h15",p:"La marine encercle l'île et ferme le détroit. Les fonderies de semi-conducteurs sont coupées du monde, les armateurs détournent leurs routes, Pékin impose un contrôle des changes.",hit:{NQ:-4.0,TOPX:-3.4,MXEF:-3.6,ES:-2.4,HG:-2.2,BDI:3.4,GC:2.8,JPY:1.8,AUD:-2.2},liq:2.0,shut:['MXEF']},
 {x:1,t:"Un tsunami ravage la côte pacifique du Japon",who:"Agence météorologique · alerte maximale",p:"La vague a franchi les digues sur trois cents kilomètres. Deux centrales et des dizaines d'usines de composants sont à l'arrêt ; la bourse de Tokyo ne rouvrira pas de sitôt.",hit:{TOPX:-3.8,JPY:2.6,JGB:1.6,NQ:-1.6,HG:-1.4,CL:1.2,ES:-1.0},liq:1.8,shut:['TOPX']},
 {x:1,t:"Défaut d'un grand pays de la zone euro",who:"Ministère des Finances · déclaration",p:"Le coupon n'est pas payé. La banque centrale convoque un conseil extraordinaire ; les obligations des voisins décrochent et les banques du pays ferment leurs guichets.",hit:{OAT:-3.6,ESTX:-3.8,EUR:-3.2,GBL:2.8,GC:2.6,GBP:-1.2,ES:-1.8,VX:3.0},liq:2.1},
 {x:1,t:"Une pandémie foudroyante ferme les frontières",who:"Organisation mondiale de la santé · urgence internationale",p:"Les cas doublent en trois jours. Les flottes aériennes sont clouées au sol, les usines ferment, le pétrole n'a plus d'acheteurs.",hit:{ES:-3.4,ESTX:-3.2,MXEF:-3.4,CL:-4.2,HG:-2.8,BDI:-3.2,TN:3.0,GBL:2.2,GC:1.6,VX:4.0,AUD:-2.4},liq:2.3},
 {x:1,t:"Cyberattaque sur le système de paiement en dollars",who:"Réserve fédérale · déclaration d'urgence",p:"Les virements interbancaires sont bloqués depuis l'ouverture. Les appels de marge ne peuvent pas être réglés ; la chambre de compensation suspend les contrats de taux.",hit:{ES:-2.6,NQ:-3.0,TN:-2.0,EUR:2.2,JPY:2.4,GC:3.2,BTC:2.4,VX:3.4},liq:2.5,shut:['TN']},
 {x:1,t:"Éruption d'un supervolcan : l'hiver volcanique menace",who:"Institut de géophysique · alerte rouge",p:"Le nuage de cendres couvre l'hémisphère Nord. Les vols sont suspendus sur trois continents et les agronomes parlent d'une récolte perdue.",hit:{ZW:3.8,KC:3.0,CL:1.6,ES:-2.2,ESTX:-2.8,BDI:-2.4,GC:1.8,NRAM:-2.6},liq:1.8}
);""")
e.rep(""" if(MACROEV.filter(e=>!S.usedMacro.includes(e.t)).length<6)S.usedMacro=[];
 for(let i=0;i<nb;i++){
   const avail=MACROEV.filter(e=>!S.usedMacro.includes(e.t));if(!avail.length)break;""",""" if(MACROEV.filter(e=>!e.x&&!S.usedMacro.includes(e.t)).length<6)S.usedMacro=[];
 for(let i=0;i<nb;i++){
   const avail=MACROEV.filter(e=>!e.x&&!S.usedMacro.includes(e.t));if(!avail.length)break;""")
e.rep("   const pool=MACROEV.filter(e=>!S.evQueue.includes(e));","   const pool=MACROEV.filter(e=>!e.x&&!S.evQueue.includes(e));")
e.rep(" S.preDesk=null;\n",""" /* lot 58 : un événement extrême, une fois tous les six ou sept trimestres (tirage pur, aucun flux déplacé) */
 if(S.q>=1){const u=prng32(hash32('xev'+S.q,S.seed));
  if(u()<XPROB){S.usedX=S.usedX||[];let av=MACROEV.filter(e=>e.x&&!S.usedX.includes(e.t));if(!av.length){S.usedX=[];av=MACROEV.filter(e=>e.x)}
   if(av.length){const e=av[Math.floor(u()*av.length)];S.usedX.push(e.t);S.evQueue.splice(Math.floor(u()*(S.evQueue.length+1)),0,e)}}}
 S.preDesk=null;
""",1)
# ni pré-annonce ni rumeur sur un extrême
e.rep("S.evQueue.filter(ev=>!ev.trader&&!ev.rivalEv&&!ev.stake&&ev.t&&ev.hit)","S.evQueue.filter(ev=>!ev.trader&&!ev.rivalEv&&!ev.stake&&ev.t&&ev.hit&&!ev.x)")
e.rep("const f=pick(MACROEV.filter(e=>!S.evQueue.includes(e)&&!S.usedMacro.includes(e.t)));","const f=pick(MACROEV.filter(e=>!e.x&&!S.evQueue.includes(e)&&!S.usedMacro.includes(e.t)));")
# carte de la dépêche
e.rep("""  <div class="evcard">${evHead(ev.who,'news')}<h3>${ev.t}</h3><p>${ev.p}</p>
   <div class="shock">${chips}</div>${evTimerHTML}</div>""","""  <div class="evcard${ev.x?' xtr':''}">${ev.x?'<div class="xtag">⚠ ÉVÉNEMENT EXTRÊME</div>':''}${evHead(ev.who,'news')}<h3>${ev.t}</h3><p>${ev.p}</p>
   <div class="shock">${chips}</div>${shutL.length?`<p class="note" style="margin:8px 0 0">🔒 Cotation suspendue : ${shutL.join(', ')} — aucun ordre possible jusqu'à la clôture, et fermés au fonds le trimestre prochain.</p>`:''}${evTimerHTML}</div>""")
e.rep(""" const plan=evPlans(ev,touched);
 const UM=pickU(""",""" const shutL=(ev.shut||[]).filter(sy=>IDX[sy]!==undefined&&mktOpen(IDX[sy]));
 if(shutL.length){S.shut=S.shut||{};shutL.forEach(sy=>S.shut[sy]=S.q+1)}
 const plan=evPlans(ev,touched);
 const UM=pickU(""")
e.done("lot 58 — NAV instantanée, cartons du comité, extrêmes, collatéral, risque marginal, plafonds")
