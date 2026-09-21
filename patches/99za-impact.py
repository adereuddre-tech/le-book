# -*- coding: utf-8 -*-
"""Lot 38 — l'exécution pèse vraiment : l'impact de marché est payé par le fonds.

Mesure de départ (`tools/execmeas.js`, 18 parties, deux familles séparées) :

  | par choix | fonds (pb d'encours) | investisseurs | comité |
  |---|---|---|---|
  | anecdote d'exécution (5 par partie) | méd **0**, moy −0,7, p10 −33 / p90 +27 | méd 0, 24 choix sur 90 | méd 0 |
  | anecdote de desk (14 par partie) | méd 0, moy **−19,6**, p10 −55 | 116 sur 259 | 97 sur 259 |

Le desk pèse vingt-cinq fois plus que l'exécution. La moitié des choix d'exécution ne touchent
pas du tout le fonds : ils ne jouent que sur la facture d'ordres, qui est à la charge du gérant
et vaut 20 pb d'encours — 0,26 M$ quand le trimestre en fait ±300.

Multiplier par dix la facture ne marcherait pas : les 435 textes de boutons annoncent des
pourcentages écrits à la main (« Coûts sur les taux −35 % »), et l'invariant 9 exige que
l'affiché soit l'appliqué. On ajoute donc le canal qui manque, celui qui existe en salle de
marché et qui est **cinq à dix fois plus gros que les commissions** : l'impact de marché.

  - `execImpactAmt(bill,m,leak)` : le fonds perd `IMPK` (= 2,4) fois la facture standard,
    corrigé de la manière d'exécuter. `m^-1,2` : payer le bloc protège le prix moyen,
    négocier un rabais le dégrade — c'est l'arbitrage réel, et il **inverse le signe du lot 37**,
    qui punissait le fonds dans les deux sens (payer plus cher *et* moins bien exécuter).
    Une fuite majore de 60 %. Plafond 1,5 % de l'encours par application.
  - Il se paie à **chaque** trimestre, anecdote ou pas : ~30 pb d'encours, 0,4 M$ sur un fonds
    de 130 M$, contre 0 aujourd'hui. Un choix « coûts −35 % » fait gagner 0,07 M$ au gérant et
    coûte 0,13 M$ de plus au fonds : le joueur a enfin un vrai arbitrage à faire.
  - Pour que ce ne soit pas un simple malus, la facture de courtage passe aux trois quarts (`EXECM`) :
    ce qui était payé par le gérant en commissions se paie maintenant par le fonds en prix
    moyen. C'est aussi plus juste : les commissions sont le petit poste, l'impact le gros.
  - Les jauges suivent sans rien ajouter d'artificiel : l'impact passe par `S.qEvM`, donc par
    `pnlGauge` de la carte d'exécution. On ajoute seulement, à la clôture, la lecture du
    rapport de best execution : investisseurs −2 si l'impact du trimestre dépasse 35 pb,
    comité −2 si l'exécution s'est écartée du standard de plus de 35 %.
  - Tout est affiché avant le clic (`stake`) et rappelé sur l'écran des ordres, avec les mêmes
    fonctions que l'application.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()

# ── 1. le modèle d'impact remplace le glissement du lot 37 ─────────────────────
e.rep("""const EXECSLIP=12,EXECSLIPMAX=0.012,EXECGAIN=0.35;
function execSlipAmt(excess){if(!excess)return 0;
 if(excess>0)return -Math.min(EXECSLIP*excess,EXECSLIPMAX*S.nav);          /* payé plus cher que le standard : le prix moyen se dégrade */
 return Math.min(-EXECGAIN*EXECSLIP*excess,EXECGAIN*EXECSLIPMAX*S.nav);          /* exécuté moins cher : un peu de prix gagné, jamais autant */
}""",
"""/* Impact de marché. Les commissions sont le petit poste de l'exécution ; ce que coûte
   vraiment un ordre, c'est le prix qu'on obtient. Le fonds perd IMPK fois la facture
   standard, corrigé de la manière d'exécuter : payer le bloc (m>1) protège le prix moyen,
   négocier un rabais (m<1) le dégrade, une fuite le dégrade encore. Sert à l'affichage comme
   à l'application (invariant 9). */
const IMPK=2.4,IMPMAX=0.015;
function execImpactF(m,leak){return Math.pow(Math.max(0.3,Math.min(3,m||1)),-1.2)*(leak?1.6:1)}
function execImpactAmt(bill,m,leak){
 if(!(bill>0))return 0;
 return -Math.min(IMPK*bill*execImpactF(m,leak),IMPMAX*S.nav);
}
/* Écart à une exécution standard : ce que ce choix coûte (ou épargne) au fonds en plus. */
function execImpactDelta(bill,m,leak){return execImpactAmt(bill,m,leak)-execImpactAmt(bill,1,false)}""")
# l'ancien nom reste utilisé par les ajustements intra-trimestre : on le redéfinit proprement
e.rep("""function execSlip(excess,why){
 const amt=execSlipAmt(excess);if(!amt)return 0;""",
"""function execSlip(amt,why){
 if(!amt)return 0;""")

# ── 2. jauges : le comité lit le rapport de best execution ─────────────────────
e.rep(" if(m&&Math.abs(m-1)>0.04)rc=-Math.min(4,3.5*Math.abs(m-1));\n if(leak){lp-=2;rc-=1}",
      " if(m&&Math.abs(m-1)>0.04)rc=-Math.min(6,5*Math.abs(m-1));\n if(leak){lp-=3;rc-=2}")

# ── 3. écran des ordres : l'impact annoncé, puis appliqué ──────────────────────
# la facture affichée après ce choix, calculée comme l'application la calcule (invariant 9)
e.rep(""" const stake=c=>{const x=c.e||{};const out=[];
  if(x.tcMult){
   let sub=0;if(x.tcMultOn){orders.forEach(o=>{if(x.tcMultOn.includes(INSTR[o.i].sym))sub+=o.t.cost})}else sub=tot;
   const d=sub*(x.tcMult-1);""",
""" const stake=c=>{const x=c.e||{};const out=[];let bill=tot;
  if(x.tcMult){
   let sub=0;if(x.tcMultOn){orders.forEach(o=>{if(x.tcMultOn.includes(INSTR[o.i].sym))sub+=o.t.cost})}else sub=tot;
   const d=sub*(x.tcMult-1);bill=tot+d;""")
e.rep("""   const sl=execSlipAmt(d);
   if(sl)out.push(`${mn(sl)} de prix moyen pour le fonds`);
  }
  const gx=execGz(x.tcMult,x.leakQ);""",
"""  }
  const im=execImpactAmt(bill,x.tcMult,x.leakQ);
  if(im)out.push(`<b class="neg-g">${mm(Math.abs(im))}</b> d'impact de marché pour le fonds`);
  const gx=execGz(x.tcMult,x.leakQ);""")
e.rep("""   <div class="kv"><span>Trésorerie de votre société après paiement</span>""",
"""   <div class="kv"><span>Impact de marché estimé, payé par le fonds</span><b class="neg-g">${mm(Math.abs(execImpactAmt(tot,1,S.leakQ)))} · ${(Math.abs(execImpactAmt(tot,1,S.leakQ))/S.nav*1e4).toFixed(0)} pb de l'encours</b></div>
   <div class="kv"><span>Trésorerie de votre société après paiement</span>""")
# application : à chaque choix, et aussi quand il n'y a pas d'anecdote
e.rep("""   const delta=sub*(m-1);S.pendingTC+=delta/S.nav;
   msg.push(`Coûts d'exécution ${delta<=0?'':'+'}${mm(delta)}.`);
   const sl=execSlipAmt(delta);
   if(sl){execSlip(delta,'Exécution');msg.push(`Le prix moyen s'en ressent : ${mn(sl)} pour le fonds.`)}
   e._m=m}""",
"""   const delta=sub*(m-1);S.pendingTC+=delta/S.nav;
   msg.push(`Coûts d'exécution ${delta<=0?'':'+'}${mm(delta)}.`);
   e._m=m}
  /* l'impact de marché du trimestre, sur la facture telle qu'elle est après ce choix */
  {const bill=S.pendingTC*S.nav,im=execImpactAmt(bill,e._m||e.tcMult,e.leakQ);
   if(im){execSlip(im,'Impact');msg.push(`Impact de marché sur le prix moyen : ${mn(im)} pour le fonds.`)}}""")
e.rep(" const done=()=>{S.totalTC+=(S.pendingTC*S.nav)-tot;phaseLive()};",
 """ /* sans anecdote, le fonds paie quand même l'impact d'une exécution standard */
 const done=()=>{S.totalTC+=(S.pendingTC*S.nav)-tot;
  if(!ev){const im=execImpactAmt(S.pendingTC*S.nav,1,S.leakQ);if(im)execSlip(im,'Impact')}
  phaseLive()};""")

# ── 4. ajustements en cours de trimestre : même modèle ─────────────────────────
e.rep("""   const xs=c*(1-1/Math.max(0.01,S.tcMultQ)),sl=execSlipAmt(xs);
   if(sl){execSlip(xs,'Exécution');msg.push(`${INSTR[i].sym} passe à ${nk>0?'+':''}${nk} (${mm(c)} de coûts, ${mn(sl)} de prix moyen).`)}""",
"""   const sl=execImpactAmt(c,S.tcMultQ,S.leakQ);
   if(sl){execSlip(sl,'Impact');msg.push(`${INSTR[i].sym} passe à ${nk>0?'+':''}${nk} (${mm(c)} de coûts, ${mn(sl)} d'impact).`)}""")

# ── 5. clôture : ce que les deux camps retiennent de l'exécution ───────────────
e.rep(" if(S.execSlipQ<-0.0015*S.navQ0)rcD.push(['Exécution nettement au-dessus du tarif standard',-2]);",
      " if(S.tcMultQ&&Math.abs(S.tcMultQ-1)>0.35)rcD.push(['Exécution éloignée du tarif standard',-2]);")
OLD=" if(S.leakQ)lpD.push(['Vos positions ont circulé sur le marché',-2.5]);"
e.rep(OLD,OLD+"\n if(S.execSlipQ<-0.0035*S.navQ0)lpD.push(['Impact de marché lourd sur les ordres',-2]);")

# ── 6. la facture de courtage rend la main : le gros du coût passe côté fonds ──
e.rep("const EXECM=[1.80,1.00,0.66],","const EXECM=[1.35,0.75,0.50],   /* lot 38 : trois quarts de l'ancienne facture, le reste se paie en impact de marché */\n")
e.done("lot 38 — impact de marche paye par le fonds")
