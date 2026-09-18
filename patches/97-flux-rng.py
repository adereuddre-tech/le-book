# -*- coding: utf-8 -*-
"""Lot 11 — flux aléatoires nommés, pour rendre la calibration abordable.

Problème : un seul générateur séquentiel (`mulberry32`, `rngState` global). Dès qu'une
option consomme un tirage de plus — un incident évité, une source supplémentaire, une
intuition tirée pour un style et pas pour un autre — les deux bras d'une partie appariée
divergent et ne partagent plus aucun chemin de marché. L'appariement ne réduit donc presque
rien, d'où un écart-type de l'ordre de 30 M$ et la nécessité de centaines de parties par
niveau de budget.

Correction : à chaque frontière de phase, le générateur est resemé depuis
`hash(graine, canal, trimestre)`. Le chemin de marché d'un trimestre donné ne dépend donc plus
de ce que les autres phases ont consommé. Les canaux :
  mkt  régime, vecteur factoriel, liquidité
  ev   composition de la file d'événements du trimestre
  mat  dérive de la matrice factorielle, ruptures, états T/C/V, rendements réalisés
  riv  dépêche de rivalité
  rum  sources du trimestre
  sc   suite du mouvement d'une dépêche (un canal par rang de dépêche)
  res  clôture : concurrents, flux, incidents de clôture

La sauvegarde continue de fonctionner sans changement : `rngState` enregistre la position
courante, et les points de resemis sont rejoués à l'identique après une reprise.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()

e.rep("""let rng,spare=null,rngState=0;""",
"""let rng,spare=null,rngState=0;
/* Flux nommés : un canal par usage et par trimestre, dérivé de la graine. Voir la note de
   reprise — c'est ce qui rend les parties appariées réellement appariées. */
function hash32(str,seed){let h=(seed>>>0)^0x9E3779B9;
 for(let i=0;i<str.length;i++)h=Math.imul(h^str.charCodeAt(i),2654435761)>>>0;
 h^=h>>>15;h=Math.imul(h,2246822507)>>>0;h^=h>>>13;return h>>>0}
function reseed(ch,q){rng=mulberry32(hash32(ch+'#'+(q===undefined?(S?S.q:0):q),S?S.seed:0));spare=null}""")

# ── planQuarter : trois blocs de marché, séparés par les tirages d'événements ──
e.rep("""function planQuarter(){
 S.truth=drawK(TRANS[S.regime]);""",
"""function planQuarter(){
 reseed('mkt');
 S.truth=drawK(TRANS[S.regime]);""")
e.rep(""" /* événements macro du trimestre : 2 à 5, plus une interaction avec le desk */
 const nb=2+Math.floor(rng()*4);""",
""" /* événements macro du trimestre : 2 à 5, plus une interaction avec le desk */
 reseed('ev');
 const nb=2+Math.floor(rng()*4);""")
e.rep(""" /* évolution de la matrice factorielle */
 S.bPrev=INSTR.map(x=>[...x.b]);S.rupture=null;""",
""" /* évolution de la matrice factorielle — le chemin de marché proprement dit */
 reseed('mat');
 S.bPrev=INSTR.map(x=>[...x.b]);S.rupture=null;""")
e.rep(""" /* le concurrent qui a eu raison : une fois sur deux, une dépêche de rivalité */
 if(rng()<0.55){""",
""" /* le concurrent qui a eu raison : une fois sur deux, une dépêche de rivalité */
 reseed('riv');
 if(rng()<0.55){""")

# ── sources, dépêches, clôture ──
e.rep("""function genRumors(){
 const n=RESN[S.bud.res]+PROF().sigBonus;""",
"""function genRumors(){
 reseed('rum');
 const n=RESN[S.bud.res]+PROF().sigBonus;""")
e.rep("""  S.sc={p:0.40+0.50*rng(),m:[0.45+0.40*rng(),-(0.30+0.40*rng())]};   /* poursuite dans [0,40 ; 0,90] */""",
"""  reseed('sc'+S.evIdx);   /* un canal par dépêche : son issue ne dépend pas du reste */
  S.sc={p:0.40+0.50*rng(),m:[0.45+0.40*rng(),-(0.30+0.40*rng())]};   /* poursuite dans [0,40 ; 0,90] */""")
e.rep("""function resolveQuarter(){
 const R=REG[S.truth];""",
"""function resolveQuarter(){
 reseed('res');
 const R=REG[S.truth];""")

e.done("lot 11 — flux aleatoires nommes")
