# -*- coding: utf-8 -*-
"""Lot 37 — l'exécution pèse enfin : le prix moyen se dégrade, et ça se voit.

Constat mesuré (`tools/execprobe.js`, 18 parties, 112 trimestres) :
  - la facture d'ordres médiane vaut **15,6 pb de l'encours** (p90 30 pb), soit 0,19 M$ sur un
    fonds de 124 M$ ; elle absorbe déjà 27 % du revenu trimestriel du gérant (p90 99 %) ;
  - mais elle est **entièrement à la charge du gérant** : l'exécution ne touche jamais le fonds,
    donc jamais la performance, donc jamais les jauges. Une anecdote « coûts ×1,5 » coûtait au
    gérant 7,5 pb d'encours, soit ~0,09 M$, et rien d'autre ;
  - côté jauges, sur 435 choix d'exécution, **7 touchent les investisseurs** et 203 le comité,
    pour −1,2 en moyenne.

Multiplier par dix le multiplicateur de coûts aurait menti au joueur : les textes des boutons
sont écrits à la main (« Coûts −25 % ») et l'invariant 9 exige que l'affiché soit l'appliqué.
On ajoute donc un canal, vrai en salle de marché : **la facture reste à votre charge, mais la
dégradation du prix moyen reste dans le fonds.**

  - `execSlipAmt(excess)` : au-delà du tarif standard, le fonds perd `EXECSLIP` (= 12) fois le
    surcoût, plafonné à 1,2 % de l'encours par choix ; en dessous, il gagne 0,35 fois autant.
    L'asymétrie est le garde-fou : sans elle, « exécuter au rabais » serait de l'argent gratuit,
    et le comité, lui, sanctionne l'écart au tarif standard dans les deux sens.
  - `execGz(m,leak)` : le comité lit les rapports de best execution — 3,5 points par unité
    d'écart au tarif standard, dans les deux sens, borné à −4 ; une fuite coûte 2 aux
    investisseurs et 1 au comité, et
    une ligne de clôture le rappelle si les positions ont circulé tout le trimestre.
  - Les ajustements du trimestre passés au multiplicateur hérité (`S.tcMultQ`, fuite ×1,45)
    glissent de la même façon : c'est là que les options « coûts −35 % avec fuite » se paient.
  - Tout est affiché avant le clic : `stake()` annonce l'effet sur les ordres, l'effet sur le
    fonds et les jauges, avec les mêmes fonctions que l'application (invariant 9).

Hors périmètre volontaire : les ajustements pris dans une dépêche (`resolveEvent`), dont les
montants sont chiffrés par `evPlans` — y toucher demanderait de refaire le chiffrage des deux
options, et l'invariant 9 ne pardonne pas l'à-peu-près.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()

# ── 1. le canal de glissement ───────────────────────────────────────────────────
e.rep("function pnlGauge(pnl,why){const z=pnlGz(pnl);return gauge(z.lp,z.rc,why)}",
"""function pnlGauge(pnl,why){const z=pnlGz(pnl);return gauge(z.lp,z.rc,why)}
/* ── Exécution ──────────────────────────────────────────────────────────────────
   La facture des ordres est à la charge du gérant ; la dégradation du prix moyen, elle,
   reste dans le fonds. Au-delà du tarif standard, le fonds perd EXECSLIP fois le surcoût,
   plafonné par choix. En dessous, rien : une commission négociée n'achète pas un meilleur
   prix. `execSlipAmt` sert à l'affichage comme à l'application (invariant 9). */
const EXECSLIP=12,EXECSLIPMAX=0.012,EXECGAIN=0.35;
function execSlipAmt(excess){if(!excess)return 0;
 if(excess>0)return -Math.min(EXECSLIP*excess,EXECSLIPMAX*S.nav);          /* payé plus cher que le standard : le prix moyen se dégrade */
 return Math.min(-EXECGAIN*EXECSLIP*excess,EXECGAIN*EXECSLIPMAX*S.nav);          /* exécuté moins cher : un peu de prix gagné, jamais autant */
}
function execSlip(excess,why){
 const amt=execSlipAmt(excess);if(!amt)return 0;
 const r=amt/S.nav,navB=S.nav;S.nav*=(1+r);S.qEvM+=r*navB;S.execSlipQ=(S.execSlipQ||0)+amt;   /* signé : négatif = le fonds a perdu au prix moyen */
 return r;
}
/* Ce que le comité et les investisseurs retiennent de la manière d'exécuter. */
function execGz(m,leak){let lp=0,rc=0;
 /* le comité veut le tarif standard : s'en écarter dans un sens ou dans l'autre se remarque
    (payer le bloc, ou acheter du rabais avec de l'information), et rien ne se gagne à
    négocier fort — sinon « exécuter au rabais » deviendrait un cadeau sans contrepartie */
 if(m&&Math.abs(m-1)>0.04)rc=-Math.min(4,3.5*Math.abs(m-1));
 if(leak){lp-=2;rc-=1}
 /* en dessous d'un demi-point, le comité ne dit rien : mieux vaut rien afficher qu'un « −0 » */
 lp=Math.abs(lp)<0.5?0:Math.round(lp);rc=Math.abs(rc)<0.5?0:Math.round(rc);
 return {lp,rc};
}""")

# ── 2. l'enjeu affiché sur chaque bouton d'exécution ───────────────────────────
e.rep(""" const stake=c=>{const x=c.e||{};if(!x.tcMult)return '';
  let sub=0;if(x.tcMultOn){orders.forEach(o=>{if(x.tcMultOn.includes(INSTR[o.i].sym))sub+=o.t.cost})}else sub=tot;
  const d=sub*(x.tcMult-1);if(Math.abs(d)<1e-9)return '';
  return ` <b class="${d<0?'pos-g':'neg-g'}">${d<0?'−':'+'}${mm(Math.abs(d))}</b> sur les ordres${x.tcMultOn?'':', et le même tarif sur vos ajustements du trimestre'}`};""",
""" const stake=c=>{const x=c.e||{};const out=[];
  if(x.tcMult){
   let sub=0;if(x.tcMultOn){orders.forEach(o=>{if(x.tcMultOn.includes(INSTR[o.i].sym))sub+=o.t.cost})}else sub=tot;
   const d=sub*(x.tcMult-1);
   if(Math.abs(d)>=1e-9)out.push(`<b class="${d<0?'pos-g':'neg-g'}">${d<0?'−':'+'}${mm(Math.abs(d))}</b> sur les ordres${x.tcMultOn?'':', même tarif sur vos ajustements'}`);
   const sl=execSlipAmt(d);
   if(sl)out.push(`${mn(sl)} de prix moyen pour le fonds`);
  }
  const gx=execGz(x.tcMult,x.leakQ);
  if(gx.lp||gx.rc)out.push(gz(gx.lp,gx.rc));
  return out.length?' '+out.join(' · '):''};""")

# ── 3. application : glissement et jauges d'exécution ──────────────────────────
e.rep("""   const delta=sub*(m-1);S.pendingTC+=delta/S.nav;
   msg.push(`Coûts d'exécution ${delta<=0?'':'+'}${mm(delta)}.`)}""",
"""   const delta=sub*(m-1);S.pendingTC+=delta/S.nav;
   msg.push(`Coûts d'exécution ${delta<=0?'':'+'}${mm(delta)}.`);
   const sl=execSlipAmt(delta);
   if(sl){execSlip(delta,'Exécution');msg.push(`Le prix moyen s'en ressent : ${mn(sl)} pour le fonds.`)}
   e._m=m}""")
e.rep("""  if(e.risk&&!e._hit)msg.push(e.safeTxt||"Le marché n'a pas bougé pendant l'exécution.");
  const pnl=(S.nav-navB0)/navB0;
  const g=pnl?pnlGauge(pnl,`${ev.who.split(' ·')[0]} — ${ch.b}`):{lp:0,rc:0};
  const g2=(e.rc||e.lp)?gauge(e.lp||0,e.rc||0,`${ev.who.split(' ·')[0]} — ${ch.b}`):{lp:0,rc:0};""",
"""  if(e.risk&&!e._hit)msg.push(e.safeTxt||"Le marché n'a pas bougé pendant l'exécution.");
  const pnl=(S.nav-navB0)/navB0;
  const g=pnl?pnlGauge(pnl,`${ev.who.split(' ·')[0]} — ${ch.b}`):{lp:0,rc:0};
  const gx=execGz(e._m||e.tcMult,e.leakQ);
  const g3=(gx.lp||gx.rc)?gauge(gx.lp,gx.rc,"Manière d'exécuter"):{lp:0,rc:0};
  const g2=(e.rc||e.lp)?gauge(e.lp||0,e.rc||0,`${ev.who.split(' ·')[0]} — ${ch.b}`):{lp:0,rc:0};""")
e.rep("""  S.evLog.push({t:ev.t,pnl,m:pnl*navB0,lp:g.lp+g2.lp,rc:g.rc+g2.rc});
  S.totalTC+=(S.pendingTC*S.nav)-tot;
  resultCard('EXÉCUTION · '+ev.who.split(' ·')[0].toUpperCase(),ch.b,[ch.s,...msg],
   [['Coûts d\\'exécution du trimestre',`<span class="neg-g">−${mm(S.pendingTC*S.nav)}</span>`],['Marché pendant l\\'exécution',`<span class="${cls(pnl)}">${sgn(pnl,1)} · ${mn(pnl*navB0)}</span>`],['Jauges',`<span class="${cls(g.lp+g2.lp)}">${sd1(g.lp+g2.lp)}</span> · <span class="${cls(g.rc+g2.rc)}">${sd1(g.rc+g2.rc)}</span>`]],""",
"""  S.evLog.push({t:ev.t,pnl,m:pnl*navB0,lp:g.lp+g2.lp+g3.lp,rc:g.rc+g2.rc+g3.rc});
  S.totalTC+=(S.pendingTC*S.nav)-tot;
  /* le bilan d'exécution était replié dans « Le détail » : c'est précisément ce que le joueur
     doit voir pour sentir le poids de son choix */
  const KEY=[['Coûts d\\'exécution du trimestre',`<span class="neg-g">−${mm(S.pendingTC*S.nav)}</span>`],['Marché et prix moyen pendant l\\'exécution',`<span class="${cls(pnl)}">${sgn(pnl,1)} · ${mn(pnl*navB0)}</span>`],['Investisseurs · comité',`<span class="${cls(g.lp+g2.lp+g3.lp)}">${sd1(g.lp+g2.lp+g3.lp)}</span> · <span class="${cls(g.rc+g2.rc+g3.rc)}">${sd1(g.rc+g2.rc+g3.rc)}</span>`]];
  resultCard('EXÉCUTION · '+ev.who.split(' ·')[0].toUpperCase(),ch.b,[ch.s,...msg],[],""")

# ── 4. ajustements du trimestre : le multiplicateur hérité glisse aussi ─────────
e.rep("""  const setK=(i,nk)=>{nk=Math.max(-S.maxk,Math.min(S.maxk,nk));if(nk!==S.k[i]){const t=tcost(nk-S.k[i],i);const c=t.cost*S.tcMultQ;S.pendingTC+=c/S.nav;S.totalTC+=c;cost+=c;S.k[i]=nk;msg.push(`${INSTR[i].sym} passe à ${nk>0?'+':''}${nk} (${mm(c)} de coûts).`)}};""",
"""  const setK=(i,nk)=>{nk=Math.max(-S.maxk,Math.min(S.maxk,nk));if(nk!==S.k[i]){const t=tcost(nk-S.k[i],i);const c=t.cost*S.tcMultQ;S.pendingTC+=c/S.nav;S.totalTC+=c;cost+=c;S.k[i]=nk;
   /* exécuter au tarif hérité du trimestre (fuite, bloc, urgence) dégrade aussi le prix */
   const xs=c*(1-1/Math.max(0.01,S.tcMultQ)),sl=execSlipAmt(xs);
   if(sl){execSlip(xs,'Exécution');msg.push(`${INSTR[i].sym} passe à ${nk>0?'+':''}${nk} (${mm(c)} de coûts, ${mn(sl)} de prix moyen).`)}
   else msg.push(`${INSTR[i].sym} passe à ${nk>0?'+':''}${nk} (${mm(c)} de coûts).`)}};""")

# ── 5. clôture : les positions connues se paient aussi en confiance ─────────────
OLD=" if(S.budBp>70)lpD.push(['Facture d"+chr(92)+"'exploitation jugée lourde',-1.5]);"
e.rep(OLD,OLD+"\n if(S.leakQ)lpD.push(['Vos positions ont circulé sur le marché',-2.5]);")
e.rep(" if(sp>1e-6&&gross<-2.2*sp/2)rcD.push(['Perte au-delà de 2,2 σ ex-",
      " if(S.leakQ)rcD.push(['Positions connues de contreparties',-2]);\n"
      " if(S.execSlipQ<-0.0015*S.navQ0)rcD.push(['Exécution nettement au-dessus du tarif standard',-2]);\n"
      " if(sp>1e-6&&gross<-2.2*sp/2)rcD.push(['Perte au-delà de 2,2 σ ex-")
# remise à zéro du compteur de glissement à chaque trimestre
e.rep(" S.pendingTC=0;S.freeAdjUsed=false;S.live=false;"," S.pendingTC=0;S.freeAdjUsed=false;S.live=false;S.execSlipQ=0;")

# le bilan passe en tableau visible plutôt que replié dans « Le détail »
e.rep("""   "Lancer le trimestre",phaseLive);""","""   "Lancer le trimestre",phaseLive,{key:KEY});""")

# « −0 » partout où une jauge bouge de moins d'un demi-point : on affiche 0, sans signe
e.rep("""const sd1=x=>`<b class="${cls(x)}">${x>=0?'+':'−'}${Math.round(Math.abs(x))}</b>`;""",
      """const sd1=x=>Math.abs(x)<0.5?'<b class="dim-g">0</b>':`<b class="${cls(x)}">${x>=0?'+':'−'}${Math.round(Math.abs(x))}</b>`;""")
e.done("lot 37 — impact de l'execution")
