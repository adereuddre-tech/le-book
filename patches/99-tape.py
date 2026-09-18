# -*- coding: utf-8 -*-
"""Lot 13 — le ruban de P&L du fonds, en direct pendant le trimestre.

Dès que les ordres sont passés (`S.phase==='events'`), le bandeau d'informations continues
cède la place à un graphique vivant du P&L du fonds depuis le début de l'année.

Trois exigences, et la façon dont chacune est tenue :

1. « Aspect d'un mouvement brownien géométrique. » Chaque segment est un **pont brownien
   géométrique** : bruit cumulé en logarithme, moins sa dérive terminale, puis exponentielle.
   On obtient la texture d'un cours de bourse avec les deux extrémités clouées.
2. « La valeur finale correspond précisément au P&L du fonds à cet instant. » Par construction
   du pont, le dernier point EST la cible. Et la cible est `liveRet()`, qui est exactement la
   formule de clôture `grQ` avec la fraction de trimestre écoulée `t` à la place de 1 : à la
   fin du trimestre le ruban tombe donc pile sur le chiffre du débriefing.
3. « Apparaît progressivement et se fige au moment où l'événement survient. » Le tracé est
   animé par `stroke-dashoffset` en 1,4 s, `forwards` : il se fige de lui-même. Les points
   déjà tracés sont **stockés** dans `S.tape` et ne sont jamais recalculés — le passé du ruban
   ne bouge pas quand le présent avance.

Piège évité : `mulberry32` écrit dans le `rngState` global. L'utiliser pour le décor aurait
silencieusement décalé les flux aléatoires nommés du lot 11. Le ruban a son propre générateur
pur, `prng32`, qui ne touche à rien.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()

# ── générateur pur, et fabrique de ponts ──
e.rep("""function reseed(ch,q){""",
"""/* Générateur PUR pour le décor : il ne touche pas à rngState, contrairement à mulberry32.
   Y toucher décalerait les flux nommés et casserait l'appariement des campagnes. */
function prng32(a){let s=a|0;return function(){s=s+0x6D2B79F5|0;let t=Math.imul(s^s>>>15,1|s);
 t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
/* Pont brownien géométrique : m points de v0 à v1, texture de cours, extrémités clouées. */
function bridgePts(v0,v1,m,seed,vol){
 const r=prng32(seed),a=Math.log(Math.max(1e-9,v0)),b=Math.log(Math.max(1e-9,v1));
 const raw=[];let w=0;
 for(let i=0;i<m;i++){w+=(r()*2-1)*vol;raw.push(w)}
 const last=raw[m-1]||0,out=[];
 for(let i=1;i<=m;i++)out.push(Math.exp(a+(b-a)*(i/m)+(raw[i-1]-last*(i/m))));
 return out;
}
function reseed(ch,q){""")

# ── la valeur à afficher : le P&L du fonds à cet instant ──
e.rep("""function statusBar(done){""",
"""/* Fraction du trimestre écoulée, lue sur l'avancement de la file de dépêches. */
function qElapsed(){const n=(S.evQueue||[]).length||1;return Math.max(0,Math.min(1,(S.evIdx||0)/n))}
/* Rendement du trimestre à cet instant. C'est `grQ` de resolveQuarter avec t au lieu de 1 :
   au bout du trimestre, le ruban tombe exactement sur le chiffre du débriefing. */
function liveRet(){
 if(!S.rBase)return 0;
 const t=qElapsed(),w=weights(S.k);
 let g=0;for(let i=0;i<N;i++)g+=w[i]*S.rBase[i];
 g+=S.rate/4;   /* le collatéral court aussi : sans lui le ruban ratait la clôture de ~108 pb */
 return (t*g*S.nav+(S.qEvM||0)+(S.qIncM||0)-(S.qMgmtM||0))/Math.max(1e-9,S.navQ0);
}
/* Indice de performance nette, base 100 au premier jour de l'année en cours. */
function ytdIdx(){
 const y0=Math.floor(S.q/4)*4;let v=1;
 for(let i=0;i<y0;i++)v*=(1+S.rets[i]);
 let cur=1;for(let i=0;i<S.q;i++)cur*=(1+S.rets[i]);
 return {y0,base:v,now:cur*(1+liveRet())/v*100,closes:S.rets.slice(y0,S.q)};
}
/* Le ruban. Le passé est stocké, jamais recalculé ; seul le présent s'allonge. */
function tapeTick(){
 const y=ytdIdx(),yk=y.y0;
 if(!S.tape||S.tape.y!==yk||S.tape.q!==S.q){
  const pts=[100];let v=1;
  y.closes.forEach((r,i)=>{const nv=v*(1+r);
    bridgePts(v*100,nv*100,16,hash32('tape'+(yk+i),S.seed),0.010).forEach(x=>pts.push(x));v=nv});
  S.tape={y:yk,q:S.q,pts,seg:0};
 }
 const tgt=y.now,last=S.tape.pts[S.tape.pts.length-1];
 if(Math.abs(tgt/last-1)>1e-9){
  const vol=Math.max(0.004,(S.tgt||0.05)/6);
  bridgePts(last,tgt,9,hash32('tapeq'+S.q+'_'+(S.tape.seg++),S.seed),vol).forEach(x=>S.tape.pts.push(x));
  if(S.tape.pts.length>420)S.tape.pts.splice(0,S.tape.pts.length-420);
 }
}
function tapeBand(){
 try{tapeTick()}catch(err){return ticker()}
 const p=S.tape&&S.tape.pts||[];
 if(p.length<3)return ticker();
 const v=p[p.length-1],up=v>=100;
 return `<div class="tape"><div class="tapehead"><span>P&amp;L DU FONDS · ANNÉE ${1+Math.floor(S.q/4)}</span>
   <b class="${up?'pos-g':'neg-g'}">${up?'+':'−'}${dec(Math.abs(v-100),1)} %</b></div>
  ${navChart(p,{h:78,base:100,anim:1,pulse:1})}</div>`;
}
function statusBar(done){""")

# ── le point de tête bat, comme un cours en direct ──
e.rep(""" mk+=`<circle cx="${px(v.length-1).toFixed(1)}" cy="${py(v[v.length-1]).toFixed(1)}" r="3.2" fill="${col}"/>`;""",
""" mk+=`<circle cx="${px(v.length-1).toFixed(1)}" cy="${py(v[v.length-1]).toFixed(1)}" r="3.2" fill="${col}">`
  +(o.pulse?`<animate attributeName="r" values="3.2;6;3.2" dur="1.8s" repeatCount="indefinite"/>`:'')+`</circle>`;""")

# ── le bandeau cède la place dès que les ordres sont passés ──
e.rep("""  </div>${ticker()}</div>`;""",
"""  </div>${S.phase==='events'?tapeBand():ticker()}</div>`;""")

# ── habillage ──
e.rep(""".navbox{margin:14px 0 0;""",
""".tape{margin:10px -2px 0;padding:6px 8px 2px;border:1px solid var(--line);border-radius:8px;
 background:linear-gradient(180deg,rgba(21,32,47,.55),rgba(21,32,47,0))}
.tapehead{display:flex;justify-content:space-between;align-items:baseline;
 font-family:var(--mono);font-size:10px;letter-spacing:.05em;color:var(--dimmer);margin-bottom:2px}
.tapehead b{font-size:12px}
.tape .navdraw{animation-duration:1.4s}
.navbox{margin:14px 0 0;""")

e.done("lot 13 — ruban de P&L en direct")
