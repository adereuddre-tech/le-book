# -*- coding: utf-8 -*-
"""Lots 43-44 — les bonus : pop-ups dorés, et treize nouveaux bonus à décrocher.

Lot 43 — la mise en scène. `goldPop()` : une carte au centre de l'écran, bordée d'or, avec un
visuel dessiné (couronne, clé, journal, fusée…), un titre, et le gain chiffré. Un éclat balaie
la carte ; elle se ferme d'un toucher ; les bonus du même instant passent en file, jamais
empilés. Les bonus de clôture attendent la fin du grand ruban (5,6 s) pour ne pas le masquer.
Déjà dans le jeu et désormais mis en scène : hauts faits (au lieu d'une notification), objectif
du trimestre tenu, recrue du trimestre (présentée comme un débauchage chez un concurrent),
nouveau plus haut historique quand il est net (le premier de la partie).

Lot 44 — treize bonus, décision d'Antoine : les quatre familles.
  Croissance (encours rapporté au départ) : ×1,25 accès aux blocs (plafonds ×1,5, coûts −10 %) ;
    ×1,5 prime brokerage (un ajustement gratuit par trimestre) ; ×2 dark pools (plafonds ×2,
    coûts −10 %).
  Séries : main chaude (quatre trimestres positifs : souscription +3 %, investisseurs +4) ; à la
    une du FT (battre les quatre concurrents de 3 points : investisseurs +6, comité +2) ; fonds macro de
    l'année (premier sur l'année civile : souscription +5 %, investisseurs +8, comité +4).
  Talents et information, en début de trimestre : l'économiste de la Fed (recherche au cran 7
    ou plus : +2 sources pendant deux trimestres) ; le trader star d'un concurrent (salle au
    cran 8 ou plus : coûts ÷3 sur un marché, et le concurrent s'affaiblit) ; le dîner de
    Jackson Hole (confiance 75 ou plus : la première dépêche du trimestre est pré-annoncée).
  Institutionnel et rares : le fonds souverain (encours ×1,5 et confiance 75 : +20 %
    d'encours, mais une bande de volatilité resserrée de 20 %) ; carte blanche du comité
    (trois trimestres de suite dans la bande : comité +3, un ajustement gratuit) ; le trade du
    siècle (+12 % ou plus sur une seule dépêche) ; le cygne noir apprivoisé (trimestre de crise
    ou de récession fini positif : souscription +3 %, investisseurs +5).

Garde-fous :
  - aucun tirage de `rng` : les chances passent par hash32/prng32, les flux nommés ne bougent pas ;
  - rien ne s'applique au milieu d'une dépêche (invariant 9) : clôture ou début de trimestre ;
  - l'ajustement gratuit passe par `evPlans`, qui chiffre l'option : l'affiché reste l'appliqué ;
  - chaque bonus une fois par partie, sauf le fonds de l'année (une fois par an).
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()

# ── 1. CSS ─────────────────────────────────────────────────────────────────────
e.rep("@media (prefers-reduced-motion:reduce){.thold{opacity:1;pointer-events:auto;animation:none}}",
"""@media (prefers-reduced-motion:reduce){.thold{opacity:1;pointer-events:auto;animation:none}}
/* bonus : la carte dorée */
#gold{position:fixed;inset:0;z-index:9999;display:flex;align-items:center;justify-content:center;background:rgba(4,7,13,.74);animation:gfade .25s ease-out;cursor:pointer}
.gcard{position:relative;overflow:hidden;width:min(320px,86vw);padding:22px 20px 16px;border-radius:14px;text-align:center;
 background:radial-gradient(circle at 50% -10%,rgba(217,176,106,.32),rgba(19,25,37,0) 62%),#131925;border:1.5px solid var(--gold);
 box-shadow:0 0 0 1px rgba(217,176,106,.22),0 18px 60px rgba(0,0,0,.6),0 0 46px rgba(217,176,106,.28);animation:gpop .55s cubic-bezier(.2,1.4,.4,1)}
.gcard::after{content:'';position:absolute;top:-60%;left:-70%;width:40%;height:220%;transform:rotate(22deg);
 background:linear-gradient(90deg,transparent,rgba(255,238,196,.38),transparent);animation:gshine 1.5s .45s ease-out forwards}
.gvis svg{width:92px;height:92px;display:block;margin:0 auto 6px}
.gkick{font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;color:var(--gold)}
.gcard h3{font-family:var(--serif);font-size:25px;line-height:1.1;margin:6px 0 6px;color:#F3EEE4;font-weight:400}
.gcard p{font-size:13.5px;line-height:1.45;color:var(--dim);margin:0}
.ggain{font-family:var(--mono);font-size:14px;color:var(--gold);margin-top:10px;line-height:1.5}
.gtap{font-family:var(--mono);font-size:10px;color:var(--dimmer);margin-top:12px;letter-spacing:.06em}
@keyframes gpop{from{transform:scale(.55);opacity:0}to{transform:scale(1);opacity:1}}
@keyframes gshine{to{left:140%}}
@keyframes gfade{from{opacity:0}}
@media (prefers-reduced-motion:reduce){#gold,.gcard,.gcard::after{animation:none}}""")

# ── 2. la mécanique d'affichage, les visuels, les bonus ────────────────────────
e.rep("function budgetBp(){","""/* ══════════ bonus : visuels, file d'affichage, déclencheurs ══════════ */
const GV={
 crown:'<path d="M18 66 L22 34 L36 48 L48 26 L60 48 L74 34 L78 66 Z" fill="rgba(217,176,106,.18)" stroke="#D9B06A" stroke-width="3" stroke-linejoin="round"/><rect x="18" y="68" width="60" height="8" rx="2" fill="#D9B06A"/><circle cx="22" cy="32" r="4" fill="#F3D48C"/><circle cx="48" cy="24" r="4" fill="#F3D48C"/><circle cx="74" cy="32" r="4" fill="#F3D48C"/>',
 trophy:'<path d="M32 20 H64 V40 C64 52 56 58 48 58 C40 58 32 52 32 40 Z" fill="rgba(217,176,106,.18)" stroke="#D9B06A" stroke-width="3"/><path d="M32 26 H22 C22 38 28 42 32 42 M64 26 H74 C74 38 68 42 64 42" fill="none" stroke="#D9B06A" stroke-width="3"/><path d="M44 58 V68 H52 V58 M36 76 H60" stroke="#D9B06A" stroke-width="4" fill="none" stroke-linecap="round"/>',
 key:'<circle cx="34" cy="48" r="14" fill="rgba(217,176,106,.18)" stroke="#D9B06A" stroke-width="3"/><circle cx="34" cy="48" r="5" fill="#D9B06A"/><path d="M48 48 H80 M70 48 V58 M78 48 V56" stroke="#D9B06A" stroke-width="4" stroke-linecap="round"/>',
 paper:'<rect x="20" y="20" width="56" height="58" rx="3" fill="rgba(217,176,106,.14)" stroke="#D9B06A" stroke-width="3"/><path d="M28 32 H68" stroke="#F3D48C" stroke-width="5"/><path d="M28 44 H46 M28 52 H46 M28 60 H46 M28 68 H46" stroke="#D9B06A" stroke-width="2.5"/><rect x="52" y="42" width="16" height="28" fill="#D9B06A" opacity=".6"/>',
 rocket:'<path d="M48 16 C60 28 62 46 56 62 H40 C34 46 36 28 48 16 Z" fill="rgba(217,176,106,.18)" stroke="#D9B06A" stroke-width="3"/><circle cx="48" cy="38" r="6" fill="#F3D48C"/><path d="M40 56 L30 66 L40 64 M56 56 L66 66 L56 64" fill="none" stroke="#D9B06A" stroke-width="3"/><path d="M44 66 L48 80 L52 66" fill="#F3D48C"/>',
 chart:'<path d="M18 76 H80 M18 76 V18" stroke="#5B6E8C" stroke-width="2"/><path d="M22 66 L36 54 L46 60 L60 38 L72 28" fill="none" stroke="#D9B06A" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><path d="M64 26 H74 V36" fill="none" stroke="#D9B06A" stroke-width="4" stroke-linecap="round"/><circle cx="72" cy="28" r="4" fill="#F3D48C"/>',
 doors:'<rect x="20" y="18" width="56" height="62" rx="2" fill="rgba(217,176,106,.12)" stroke="#D9B06A" stroke-width="3"/><path d="M48 18 V80" stroke="#D9B06A" stroke-width="2"/><path d="M48 22 L30 28 V74 L48 78 Z" fill="rgba(217,176,106,.3)" stroke="#D9B06A" stroke-width="2"/><circle cx="44" cy="50" r="2.5" fill="#F3D48C"/>',
 bank:'<path d="M16 38 L48 20 L80 38 Z" fill="rgba(217,176,106,.2)" stroke="#D9B06A" stroke-width="3" stroke-linejoin="round"/><path d="M24 42 V70 M36 42 V70 M48 42 V70 M60 42 V70 M72 42 V70" stroke="#D9B06A" stroke-width="4"/><rect x="16" y="72" width="64" height="7" fill="#D9B06A"/>',
 star:'<path d="M48 16 L57 38 L80 40 L62 55 L68 78 L48 66 L28 78 L34 55 L16 40 L39 38 Z" fill="rgba(217,176,106,.25)" stroke="#D9B06A" stroke-width="3" stroke-linejoin="round"/>',
 glass:'<path d="M30 18 H66 L60 42 H36 Z M36 54 H60 L66 78 H30 Z" fill="rgba(217,176,106,.15)" stroke="#D9B06A" stroke-width="3" stroke-linejoin="round"/><path d="M40 70 H56 L60 76 H36 Z" fill="#F3D48C"/><path d="M36 42 L48 50 L60 42 M36 54 L48 50 L60 54" stroke="#D9B06A" stroke-width="3" fill="none"/>',
 bolt:'<path d="M54 14 L28 52 H46 L40 82 L68 42 H50 Z" fill="rgba(217,176,106,.3)" stroke="#D9B06A" stroke-width="3" stroke-linejoin="round"/>',
 swan:'<path d="M24 66 C34 74 62 74 74 62 C66 60 58 54 56 44 C54 32 60 26 66 26 C58 20 46 26 46 40 C46 50 50 56 44 60 C38 62 30 60 24 66 Z" fill="rgba(217,176,106,.2)" stroke="#D9B06A" stroke-width="3" stroke-linejoin="round"/><circle cx="62" cy="28" r="2.5" fill="#F3D48C"/><path d="M18 78 H78" stroke="#5B6E8C" stroke-width="2"/>',
 hand:'<path d="M18 50 L34 38 L48 44 L62 38 L78 50 L64 64 C60 68 54 68 50 64 L44 58" fill="rgba(217,176,106,.18)" stroke="#D9B06A" stroke-width="3" stroke-linejoin="round"/><path d="M36 56 L44 64 M42 50 L52 60 M48 46 L58 56" stroke="#D9B06A" stroke-width="3" stroke-linecap="round"/>'
};
const GOLDQ=[];let goldOn=false;
function goldPop(b){GOLDQ.push(b);if(!goldOn)goldNext()}
function goldNext(){
 const b=GOLDQ.shift();if(!b){goldOn=false;return}
 goldOn=true;let el=document.getElementById('gold');if(el)el.remove();
 el=document.createElement('div');el.id='gold';
 el.innerHTML=`<div class="gcard" role="dialog" aria-label="${b.t}"><div class="gvis"><svg viewBox="0 0 96 96" aria-hidden="true">${GV[b.v]||GV.star}</svg></div>
  <div class="gkick">${b.k||'BONUS'}</div><h3>${b.t}</h3>${b.d?`<p>${b.d}</p>`:''}${b.g?`<div class="ggain">${b.g}</div>`:''}<div class="gtap">toucher pour continuer</div></div>`;
 document.body.appendChild(el);
 el.onclick=()=>{el.remove();goldNext()};
}
/* Les bonus déclenchés pendant un calcul attendent l'écran qui les montre. */
function goldLater(b){if(!S)return;(S.goldPend=S.goldPend||[]).push(b);(S.bonusLog=S.bonusLog||[]).push({t:b.t,q:S.q})}
function goldFlush(delay){
 if(!S||!S.goldPend||!S.goldPend.length)return;
 const L=S.goldPend.splice(0);
 setTimeout(()=>L.forEach(goldPop),delay||0);
}
/* Tirage pur pour les chances de bonus : aucun flux nommé de rng n'est déplacé. */
function bonusDraw(tag){return prng32(hash32('bonus'+tag+'_'+S.q,S.seed))()}
function hasBonus(id){return !!(S.bonus&&S.bonus[id])}
function markBonus(id){(S.bonus=S.bonus||{})[id]=S.q+1}
function flowInB(frac){const inn=frac*S.nav;S.nav+=inn;S.flows+=inn;return inn}
/* Bonus de clôture : appelés une fois le trimestre soldé, avant le débriefing. */
function bonusClose(o){
 /* l'ajustement gratuit de la carte blanche ne vaut qu'un trimestre ; celui du prime broker (99) dure */
 if(S.freeAdjB>0&&S.freeAdjB<99)S.freeAdjB--;
 const g=S.nav/S.aum0,conf0=conf();
 const B=(id,test,f)=>{if(!hasBonus(id)&&test){markBonus(id);goldLater(f())}};
 /* croissance : les marchés du rang suivant s'ouvrent quand l'encours franchit son seuil */
 while(typeof OPENRK!=='undefined'&&OPENRK<5&&S.nav>=unlockNav(OPENRK+1)){
  OPENRK++;S.openRk=OPENRK;applyPools();
  const nw=INSTR.filter(x=>x.rk===OPENRK);
  if(nw.length)goldLater({v:'doors',k:`CROISSANCE · ENCOURS ${mm(unlockNav(OPENRK))}`,t:"De nouveaux carnets s'ouvrent",
   d:"Votre courtier vous donne accès aux marchés que votre taille ne justifiait pas encore.",g:nw.map(x=>`${x.sym} · ${x.nm.toLowerCase()}`).join('<br>')});
 }
 /* croissance */
 B('blocs',g>=1.25,()=>{S.capBoost=Math.max(S.capBoost||1,1.5);S.execPenalty=Math.max(0.7,S.execPenalty*0.9);
  return {v:'key',k:'CROISSANCE · ENCOURS ×1,25',t:'Accès aux blocs',d:"Les grandes maisons vous proposent désormais leurs blocs de gré à gré.",g:'plafonds de capacité ×1,5 · coûts d\\'exécution −10 %'}});
 B('prime',g>=1.5,()=>{if(PROF().freeAdj){S.execPenalty=Math.max(0.7,S.execPenalty*0.9);
   return {v:'bank',k:'CROISSANCE · ENCOURS ×1,5',t:'Prime brokerage de premier rang',d:"Votre courtier principal vous passe au guichet des très gros clients.",g:'coûts d\\'exécution −10 %'}}
  S.freeAdjB=99;return {v:'bank',k:'CROISSANCE · ENCOURS ×1,5',t:'Prime brokerage de premier rang',d:"Votre courtier principal vous passe au guichet des très gros clients.",g:'un ajustement gratuit par trimestre'}});
 B('dark',g>=2,()=>{S.capBoost=Math.max(S.capBoost||1,2);S.execPenalty=Math.max(0.7,S.execPenalty*0.9);
  return {v:'doors',k:'CROISSANCE · ENCOURS ×2',t:'Les dark pools vous ouvrent leurs portes',d:"Vous traitez désormais là où personne ne voit passer vos ordres.",g:'plafonds de capacité ×2 · coûts d\\'exécution −10 %'}});
 /* séries et trophées */
 B('hot',(S.streak||0)>=4,()=>{const m=flowInB(0.03);gauge(4,0,'Main chaude');
  return {v:'bolt',k:'SÉRIE · QUATRE TRIMESTRES POSITIFS',t:'Main chaude',d:"Les allocataires qui hésitaient se décident.",g:`souscription ${mm(m)} (+3 % d'encours) · investisseurs +4`}});
 B('ft',o.qTotal>Math.max(...S.rivals.map(r=>r.last))+0.03&&S.rivals.every(r=>r.cum<S.idx),()=>{gauge(6,2,'À la une du Financial Times');
  return {v:'paper',k:'TROPHÉE · EN TÊTE DE LA PLACE',t:'À la une du Financial Times',d:"« Le fonds qui a battu tout le monde ce trimestre » : votre nom en première page.",g:'investisseurs +6 · comité +2'}});
 if(S.q%4===0){const y=S.q/4,yid='year'+y;
  const base=S.rets.slice(-4).reduce((a,r)=>a*(1+r),1)-1;
  const best=S.rivals.every(r=>(r.hist||[]).slice(-4).reduce((a,x)=>a*(1+x),1)-1<base);
  B(yid,best&&base>0,()=>{const m=flowInB(0.05);gauge(8,4,"Fonds macro de l'année");
   return {v:'crown',k:`TROPHÉE · ANNÉE ${y}`,t:"Fonds macro de l'année",d:"Le jury vous décerne le prix, devant les quatre maisons que vous affrontez.",g:`souscription ${mm(m)} (+5 %) · investisseurs +8 · comité +4`}})}
 /* institutionnel et rares */
 B('souv',g>=1.5&&conf0>=75,()=>{const m=flowInB(0.20);S.bandTight=0.8;
  return {v:'hand',k:'INSTITUTIONNEL',t:'Le fonds souverain frappe à la porte',d:"Un mandat de taille, avec ses conditions : le comité resserre votre bande de volatilité.",g:`souscription ${mm(m)} (+20 % d'encours) · bande du comité −20 %`}});
 B('carte',(S.inBand||0)>=3,()=>{gauge(0,3,'Carte blanche du comité');S.freeAdjB=Math.max(S.freeAdjB||0,1);
  return {v:'key',k:'INSTITUTIONNEL · TROIS TRIMESTRES DANS LA BANDE',t:'Carte blanche du comité',d:"Le comité vous fait confiance : il ne vous demandera pas de comptes sur le prochain ajustement.",g:'comité +3 · un ajustement gratuit au prochain trimestre'}});
 const bestEv=Math.max(0,...(S.evLog||[]).map(x=>x.pnl||0));
 B('century',bestEv>=0.12,()=>{gauge(3,0,'Le trade du siècle');
  return {v:'rocket',k:'RARE',t:'Le trade du siècle',d:`Une seule dépêche vous a rapporté ${sgnp(bestEv,1)} d'encours.`,g:'investisseurs +3 · on en parlera au dîner'}});
 B('swan',(S.regime==='crise'||S.regime==='recession')&&o.qTotal>0,()=>{const m=flowInB(0.03);gauge(5,0,'Le cygne noir apprivoisé');
  return {v:'swan',k:'RARE',t:'Le cygne noir apprivoisé',d:"Un trimestre où presque tout le monde a perdu, et vous finissez devant.",g:`souscription ${mm(m)} (+3 %) · investisseurs +5`}});
}
/* Bonus de début de trimestre : talents et information. */
function bonusOpen(){
 if(S.srcBonusN>0)S.srcBonusN--;
 S.jh=false;
 if(!hasBonus('fed')&&S.q>=1&&S.bud.res>=6&&bonusDraw('fed')<0.35){markBonus('fed');S.srcBonusN=2;
  goldLater({v:'glass',k:'TALENT · RECHERCHE',t:"L'ancien économiste de la Fed signe chez vous",d:"Trente ans de réunions du FOMC, et un carnet d'adresses qu'on ne trouve pas dans les manuels.",g:'+2 sources par trimestre, pendant deux trimestres'})}
 if(!hasBonus('star')&&S.q>=1&&S.bud.exec>=8&&bonusDraw('star')<0.30){markBonus('star');
  const rv=S.rivals.slice().sort((a,b)=>b.cum-a.cum)[0],i=Math.floor(bonusDraw('starmkt')*N);
  S.star=i;rv.skill=Math.max(0.5,rv.skill-0.02);
  goldLater({v:'star',k:'TALENT · DÉBAUCHAGE',t:`Le trader star de ${rv.nm}`,d:`Il traite ${INSTR[i].nm.toLowerCase()} mieux que personne, et il a choisi votre desk.`,g:`coûts ÷3 sur ${INSTR[i].sym} ce trimestre · ${rv.nm} affaibli`})}
 if(!hasBonus('jh')&&S.q>=1&&conf()>=75&&bonusDraw('jh')<0.30){markBonus('jh');S.jh=true;
  goldLater({v:'glass',k:'INFORMATION',t:'Dîner à Jackson Hole',d:"Entre la poire et le fromage, un gouverneur laisse entendre ce qui va tomber.",g:'la première dépêche du trimestre vous est pré-annoncée à coup sûr'})}
}
function budgetBp(){""")

# ── 3. branchements ────────────────────────────────────────────────────────────
# hauts faits : la carte dorée remplace la notification
e.rep(" const f=FEATS.find(x=>x.id===id);if(f)toast(`<span style=\"color:var(--gold)\">${f.ic} Haut fait débloqué</span><br>${f.nm} — ${f.d}`)}",
      " const f=FEATS.find(x=>x.id===id);if(f){const b={v:f.tier>=3?'crown':'trophy',k:'HAUT FAIT · '+TIERS[f.tier].toUpperCase(),t:`${f.ic} ${f.nm}`,d:f.d};if(S&&S.phase!=='final'&&!S.over)goldLater(b);else goldPop(b)}}")
# objectif du trimestre tenu
e.rep("  S.qGoal={nm:S.goal.nm,d:S.goal.d,ok,bonus:bon};",
      "  S.qGoal={nm:S.goal.nm,d:S.goal.d,ok,bonus:bon};\n"
      "  if(ok)goldLater({v:'trophy',k:'OBJECTIF DU TRIMESTRE',t:S.goal.nm,d:S.goal.d,g:`${mm(bon)} de bonus sur vos gains`});")
# recrue du trimestre (débauchage chez un concurrent), puis bonus d'ouverture
e.rep("S.star=-1;\n if(STARP[S.bud.exec]>0&&rng()<STARP[S.bud.exec])S.star=Math.floor(rng()*N);\n}",
      "S.star=-1;\n if(STARP[S.bud.exec]>0&&rng()<STARP[S.bud.exec])S.star=Math.floor(rng()*N);\n"
      " if(S.star>=0){const rv=S.rivals[Math.floor(bonusDraw('recrue')*S.rivals.length)];\n"
      "  goldLater({v:'star',k:'RECRUE DU TRIMESTRE',t:`Débauché chez ${rv.nm}`,d:`Un trader ${INSTR[S.star].nm.toLowerCase()} quitte ${rv.nm} pour votre desk.`,g:`coûts d'exécution ÷3 sur ${INSTR[S.star].sym} ce trimestre`})}\n"
      " bonusOpen();\n}")
# clôture : plus haut historique net, puis les bonus
e.rep(" S.phase='debrief';S.tcMultQ=1;S.leakQ=false;S.poachBoost=0;",
      " if(S.nav>=S.hwm-1e-9&&qTotal>0&&perf>0&&!S.hwmShown){S.hwmShown=S.idx;\n"
      "  goldLater({v:'chart',k:'COMMISSION DE PERFORMANCE',t:'Nouveau plus haut historique',d:\"Le fonds dépasse son sommet : la commission de performance tombe.\",g:`${mm(perf*navBefore)} de commission de performance`})}\n"
      " if(Math.abs(pvol(weights(S.k))-S.tgt)/S.tgt>bandNow())S.inBand=0;else S.inBand=(S.inBand||0)+1;\n"
      " if(!S.over)bonusClose({qTotal});\n"
      " S.phase='debrief';S.tcMultQ=1;S.leakQ=false;S.poachBoost=0;")
# les pop-ups de clôture attendent la fin du grand ruban ; celles d'ouverture, le desk
e.rep(" theatre(app.querySelector('.pnlhead').parentElement);",
      " theatre(app.querySelector('.pnlhead').parentElement);\n goldFlush(5600);")
e.rep("function screenPlay(){\n tuto(1,2);","function screenPlay(){\n tuto(1,2);\n goldFlush(500);")
# effets : sources, pré-annonce garantie, ajustement gratuit, bande resserrée
e.rep("const n=RESN[S.bud.res]+PROF().sigBonus;","const n=RESN[S.bud.res]+PROF().sigBonus+(S.srcBonusN>0?2:0);")
e.rep("S.evQueue.filter(ev=>!ev.trader&&!ev.rivalEv&&!ev.stake&&ev.t&&ev.hit).slice(0,3).forEach(ev=>{if(rng()<pr){",
      "S.evQueue.filter(ev=>!ev.trader&&!ev.rivalEv&&!ev.stake&&ev.t&&ev.hit).slice(0,3).forEach((ev,j)=>{if((S.jh&&j===0)||rng()<pr){")
e.rep("const free=cost>0&&prof.freeAdj&&!S.freeAdjUsed;","const free=cost>0&&(prof.freeAdj||S.freeAdjB>0)&&!S.freeAdjUsed;")
e.rep("function bandNow(){return BANDB[(S&&S.bud)?S.bud.risk:1]}","function bandNow(){return BANDB[(S&&S.bud)?S.bud.risk:1]*((S&&S.bandTight)||1)}")
e.done("lots 43-44 — pop-ups dores et treize bonus")
