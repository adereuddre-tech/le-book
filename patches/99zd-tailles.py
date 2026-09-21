# -*- coding: utf-8 -*-
"""Lot 41 — trois tailles réelles (100 M$ · 1 Md$ · 10 Md$), impact en racine carrée de la
profondeur, marchés qui s'ouvrent quand l'encours grossit.

Décisions d'Antoine :
  - pas de plafonds de capacité : le frein est le coût, en racine carrée. Un mastodonte qui
    s'aventure sur le café paie, et tant pis pour qui ne le voit pas venir ;
  - garder le lien taille → marchés accessibles au départ (3 / 4 / 5 par classe), et ouvrir les
    suivants quand l'encours dépasse des seuils.

Mécanique :
  - Encours de départ 0,1 / 1 / 10 Md$, `capX` à 1 : l'impact suivait déjà une loi en racine
    carrée du notionnel, c'est désormais la vraie taille qui la nourrit. Le full-floor retombe
    exactement sur le coût de l'ancien fonds moyen (100 M$ × capX 10 = 1 Md$ × 1).
  - `DEPTH` : la profondeur de chaque carnet, en Md$ (80 sur le T-Note, 0,06 sur les
    précipitations). L'impact est multiplié par √(1 + notionnel / profondeur) : invisible tant
    que l'ordre est petit devant le marché, ×3,7 pour un mastodonte qui prend cinq unités de
    café, ×6,5 sur les précipitations. `S.capBoost` (bonus de croissance) élargit la profondeur.
  - Tous les marchés de l'univers sont dans `INSTR` dès le départ, mais ceux dont le rang
    dépasse `OPENRK` sont fermés : `kCap` = 0, aucune position possible, et aucune dépêche,
    anecdote ou exigence ne les cite (`applyPools`). Rien n'est ré-indexé en cours de partie.
  - Ouverture : un rang de plus quand l'encours atteint 1,4 fois le départ, un autre à 2 fois
    (`unlockNav`), vérifié à chaque clôture, avec sa carte dorée. Le mastodonte a tout d'emblée.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
def between(a,b):
    assert e.s.count(a)==1,'debut ambigu %r'%a[:60]
    i=e.s.index(a); j=e.s.index(b,i); return e.s[i:j]

# ── 1. les trois tailles ───────────────────────────────────────────────────────
old=between("const SIZES=[","\n];")
new='''const SIZES=[
 {id:'small',lvl:'Débutant',nav:0.1,capX:1,nm:"La boutique de Mayfair — 100 M$",who:"« Trois personnes, deux écrans, un mandat »",
  p:"Un fonds de niche. Vous ne bougez aucun marché, personne ne vous surveille vraiment, et vos concurrents non plus ne sont pas les meilleurs de la place. Trois marchés par classe au départ : les autres s'ouvriront quand votre encours aura grossi.",
  ef:[["g","impact de marché négligeable : environ trois fois moins cher qu'au full-floor"],["g","investisseurs et comité indulgents"],["g","concurrents moins aguerris que la moyenne de la place"],["b","trois marchés par classe au départ ; un quatrième à 1,4 fois l'encours initial, un cinquième au double"],["b","des commissions modestes en valeur absolue"]],
  rivSkill:-0.050,rivVol:0.85,lpNeg:0.75,rcNeg:0.75,lp0:8,flowMult:0.7,goalMult:1},
 {id:'mid',lvl:'Normal',nav:1.0,capX:1,nm:"Le full-floor de Hudson Yards — 1 Md$",who:"« Un étage entier, et un loyer qui va avec »",
  p:"Assez gros pour intéresser les allocataires institutionnels et les chasseurs de têtes, assez petit pour encore bouger vite. Quatre marchés par classe ; le cinquième, le plus étroit, s'ouvre quand l'encours a grossi de 40 %.",
  ef:[["g","quatre marchés par classe : la diversification devient exploitable"],["g","commissions substantielles"],["b","impact de marché sensible sur les carnets étroits"],["b","investisseurs exigeants, comité vigilant"],["b","des concurrents sérieux, qui battent le marché plus souvent qu'à leur tour"]],
  rivSkill:0.020,rivVol:1,lpNeg:1,rcNeg:1,lp0:0,flowMult:1,goalMult:1},
 {id:'mega',lvl:'Expert',nav:10.0,capX:1,nm:"Le mastodonte de Greenwich — 10 Md$",who:"« À cette taille, vous êtes le marché »",
  p:"Tous les marchés vous sont ouverts, y compris les plus étroits — mais chaque ordre y déplace les prix, et un gros ordre sur un petit carnet coûte une fortune. Chaque trimestre est commenté, et les meilleurs gérants du monde vous attendent au tournant.",
  ef:[["g","cinq marchés par classe : l'univers complet, d'emblée"],["g","des commissions considérables"],["b","impact de marché lourd : environ trois fois plus cher qu'au full-floor, bien davantage sur les carnets étroits"],["b","investisseurs impitoyables, comité sur votre dos"],["b","concurrents au sommet de leur art : à cette taille, vous jouez contre les meilleurs du monde"]],
  rivSkill:0.085,rivVol:1.15,lpNeg:1.45,rcNeg:1.35,lp0:-8,flowMult:1.35,goalMult:1}'''
e.rep(old,new)

# ── 2. univers : tous les rangs dans INSTR, les fermés verrouillés ─────────────
old=between("function setUniverse(sizeId,univId){","\n}\n")
e.rep(old,"""/* Rang d'ouverture courant : les marchés de rang supérieur sont dans INSTR mais fermés. */
let OPENRK=4;
function rankOf(sy){const x=INSTR_ALL.find(z=>z.sym===sy);return x?x.rk:9}
function setUniverse(sizeId,univId){
 snapPools();markStakePos();
 const ncl=NCLASS[univId]||4;
 const cls=CLASSES.slice(0,ncl);
 OPENRK=MKPERCL[sizeId]||4;
 /* tous les rangs : un marché qui s'ouvre en cours de partie n'oblige à rien ré-indexer */
 const sel=INSTR_ALL.filter(x=>cls.includes(x.grp));
 INSTR.length=0;sel.forEach(x=>INSTR.push(x));reindex();
 applyPools();
}
/* Les pools ne citent que des marchés ouverts. Rappelé à chaque ouverture. */
function applyPools(){
 const ok=sy=>IDX[sy]!==undefined&&rankOf(sy)<=OPENRK;
 /* hit : on élague les marchés fermés, on garde l'événement s'il en reste un */
 POOLS.MACROEV.live.length=0;
 POOLS.MACROEV.all.forEach(e=>{
  const h={};for(const sy in e.hit)if(ok(sy))h[sy]=e.hit[sy];
  if(!Object.keys(h).length)return;
  POOLS.MACROEV.live.push(Object.keys(h).length===Object.keys(e.hit).length?e:Object.assign({},e,{hit:h}));
 });
 /* need / effets : un seul symbole fermé suffit à écarter l'entrée */
 ['TRADER_EXEC','TRADER_MID','STAKE','INCIDENTS','BOARDEV','FEATS'].forEach(nm=>{
  const P=POOLS[nm];if(!P)return;
  P.live.length=0;
  P.all.forEach(e=>{if(symsOf(e).every(ok))P.live.push(e)});
 });""")

# ── 3. impact en racine carrée de la profondeur ────────────────────────────────
e.rep(" bp=(x.s+x.c*Math.pow(bnE,pw)*(pw===0.5?1:1.9))*TCK;",
      " bp=(x.s+x.c*Math.pow(bnE,pw)*(pw===0.5?1:1.9)*depthMult(x,bn))*TCK;")
e.rep("function ddMax(){return (S&&PROF().ddMax)||0.28}",
"""function ddMax(){return (S&&PROF().ddMax)||0.28}
/* Profondeur de chaque carnet, en Md$ de notionnel : ce qu'un ordre peut peser avant que le
   marché ne le fasse payer. Au-delà, l'impact croît en racine carrée du rapport. */
const DEPTH={ES:60,NQ:30,ESTX:20,TOPX:15,MXEF:8,TN:80,GBL:40,JGB:25,R:20,OAT:15,EUR:60,JPY:40,GBP:25,AUD:12,MXP:3,
 GC:20,CL:15,ZW:2,HG:4,KC:0.25,BTC:3,VX:2,EUA:1.2,BDI:0.12,NRAM:0.06};
function depthMult(x,bn){const d=DEPTH[x.sym];return d?Math.sqrt(1+bn/(d*((S&&S.capBoost)||1))):1}
/* Un marché fermé ne prend aucune position ; un marché ouvert, le mandat. */
function mktOpen(i){const x=INSTR[i];return !!x&&x.rk<=OPENRK}
function kCap(i){return mktOpen(i)?((S&&S.maxk)||5):0}
function clampK(i,v){const c=kCap(i);return Math.max(-c,Math.min(c,v))}
/* Encours auquel s'ouvre le rang rk, pour la taille de départ : ×1,4 puis ×2. */
function unlockNav(rk){const per=MKPERCL[S.size]||4,j=rk-per;return j<=0?0:S.aum0*([1.4,2.0][j-1]||99)}""")

# book du modèle
e.rep("let k=raw.map(z=>Math.max(-S.maxk,Math.min(S.maxk,Math.round(z*a))));",
      "let k=raw.map((z,i)=>clampK(i,Math.round(z*a)));")
e.rep("  if(v<1e-9){a=a>0?a*2:1;k=raw.map(z=>Math.max(-S.maxk,Math.min(S.maxk,Math.round(z*a))));continue}",
      "  if(v<1e-9){a=a>0?a*2:1;k=raw.map((z,i)=>clampK(i,Math.round(z*a)));continue}")
e.rep("  a*=r;k=raw.map(z=>Math.max(-S.maxk,Math.min(S.maxk,Math.round(z*a))));}",
      "  a*=r;k=raw.map((z,i)=>clampK(i,Math.round(z*a)));}")
# boutons du book : un marché fermé dit quand il s'ouvre
e.rep("    const dis=Math.abs(v)>S.maxk||!segAfford(i,v),c=v<0?'neg':v>0?'pos':'zero';",
      "    const dis=Math.abs(v)>kCap(i)||!segAfford(i,v),c=v<0?'neg':v>0?'pos':'zero';")
e.rep("""      <span class="nm">${x.nm}<span class="crowd" style="background:${cc}"></span></span>""",
      """      <span class="nm">${x.nm}<span class="crowd" style="background:${cc}"></span>${mktOpen(i)?'':`<span class="capb">fermé · s'ouvre à ${mm(unlockNav(x.rk))}</span>`}</span>""")
e.rep(".lvls{display:grid;",".capb{font-family:var(--mono);font-size:9.5px;color:var(--gold);border:1px solid rgba(214,178,94,.45);border-radius:3px;padding:0 4px;margin-left:6px;white-space:nowrap}\n.lvls{display:grid;")
# anecdotes, dépêches, rivaux : jamais sur un marché fermé
e.rep("const i=Math.floor(rng()*N);const d=rng()<0.5?-1:1;const nk=Math.max(-S.maxk,Math.min(S.maxk,S.k[i]+d));",
      "const i=Math.floor(rng()*N);const d=rng()<0.5?-1:1;const nk=clampK(i,S.k[i]+d);")
e.rep("const i=IDX[e.kAddAbsE[0]];const nk=Math.max(-S.maxk,Math.min(S.maxk,S.k[i]+e.kAddAbsE[1]));",
      "const i=IDX[e.kAddAbsE[0]];const nk=clampK(i,S.k[i]+e.kAddAbsE[1]);")
e.rep("  const tg=Math.max(-S.maxk,Math.min(S.maxk,S.k[i]+sh*2)),d=tg-S.k[i];if(!d)return;",
      "  const tg=clampK(i,S.k[i]+sh*2),d=tg-S.k[i];if(!d)return;")
e.rep(" const nk=Math.max(-S.maxk,Math.min(S.maxk,dir*Math.max(2,Math.abs(S.k[i])))),t=tcost(nk-S.k[i],i);",
      " const nk=clampK(i,dir*Math.max(2,Math.abs(S.k[i]))),t=tcost(nk-S.k[i],i);")
e.rep("  const setK=(i,nk)=>{nk=Math.max(-S.maxk,Math.min(S.maxk,nk));",
      "  const setK=(i,nk)=>{nk=clampK(i,nk);")
e.rep("const cand=INSTR.map((x,i)=>i).filter(i=>Math.abs(S.k[i])<S.maxk);",
      "const cand=INSTR.map((x,i)=>i).filter(i=>Math.abs(S.k[i])<kCap(i));")
e.rep("const cand=INSTR.map((x,i)=>({i,r:S.rBase[i]})).filter(o=>Math.abs(o.r)>0.6*INSTR[o.i].sigQ&&Math.sign(S.k[o.i])!==Math.sign(o.r));",
      "const cand=INSTR.map((x,i)=>({i,r:S.rBase[i]})).filter(o=>mktOpen(o.i)&&Math.abs(o.r)>0.6*INSTR[o.i].sigQ&&Math.sign(S.k[o.i])!==Math.sign(o.r));")
# reprise : le rang d'ouverture est dans la sauvegarde
e.rep("  if(S.goal&&S.goal.nm)S.goal=QGOALS.find(g=>g.nm===S.goal.nm)||null;",
      "  if(S.openRk){OPENRK=S.openRk;applyPools()}\n  if(S.goal&&S.goal.nm)S.goal=QGOALS.find(g=>g.nm===S.goal.nm)||null;")

# ── 4. le seul coût en dollars fixes suit la taille : 150 pb d'encours initial ──
e.rep('s:"−1,5 M$ de votre poche ; le bruit de vos indicateurs',
      's:"Trois trimestres de commission de gestion, de votre poche ; le bruit de vos indicateurs')
e.rep("{const mg=(c.e&&c.e.mgrM)||0,ko=mg<0&&(-mg/1000)>mgrCash();","{const mg=((c.e&&c.e.mgrM)||0)*S.aum0/0.1,ko=mg<0&&(-mg/1000)>mgrCash();",k=3)
e.rep("if(e.mgrM){S.mgrCosts-=e.mgrM/1000;refreshGain();msg.push(`${e.mgrM<0?'−':'+'}${mm(Math.abs(e.mgrM)/1000)} sur vos gains de gérant.`)}",
      "if(e.mgrM){const a=e.mgrM/1000*S.aum0/0.1;S.mgrCosts-=a;refreshGain();msg.push(`${a<0?'−':'+'}${mm(Math.abs(a))} sur vos gains de gérant.`)}   /* 150 pb d'encours initial, à toute taille */")
# ── 5. textes et palmarès ──────────────────────────────────────────────────────
e.rep(" Les marchés les plus étroits de cette classe ne s'ouvrent qu'aux plus gros fonds.\",",
      " Les marchés les plus étroits de cette classe ne s'ouvrent qu'aux gros fonds, ou à ceux qui grossissent.\",")
e.rep("[\"b\",\"le fret ne s'ouvre qu'à partir du full-floor, les dérivés climatiques qu'au mastodonte\"]",
      "[\"b\",\"le fret s'ouvre au full-floor, les dérivés climatiques au mastodonte — ou quand l'encours a grossi\"]")
e.rep("const SZ={small:'75 M$',mid:'100 M$',mega:'150 M$'}","const SZ={small:'100 M$',mid:'1 Md$',mega:'10 Md$'}")

# ── 6. le desk connaît la profondeur de ses carnets : son book évite les marchés où deux
#       unités coûteraient plus que le signal n'en vaut (le joueur, lui, reste libre) ──
e.rep(" const raw=sc.map(o=>o.v/mx*3);"," const raw=sc.map(o=>{const x=INSTR[o.i],dm=depthMult(x,Math.abs(2*U/x.sig*S.nav));return o.v/mx*3/(dm*dm)});")
e.done("lot 41 — tailles reelles, impact de profondeur, marches a ouvrir")
