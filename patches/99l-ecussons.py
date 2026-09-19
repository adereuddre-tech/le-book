# -*- coding: utf-8 -*-
"""Lot 24 — écussons : douze blasons, un par fonds, plus une marque lisible à 9 px.

Chaque écusson existe en deux versions, parce qu'un blason dessiné pour 130 px devient une
tache à 11 px sur le graphique :
  - `crestSvg(i,px)` : l'écu complet, trait de 2,5, deux couleurs — pour l'écran de création
    et le rapport final ;
  - `crestMark(i,cx,cy,r)` : un disque de la couleur dominante portant une forme PLEINE,
    dessinée pour rester reconnaissable réduite — pour identifier les concurrents sur le ruban.
Les formes pleines évitent les traits fins, seuls capables de survivre à la réduction.

Les quatre concurrents ont un écusson fixe, cohérent avec leur nom. Le joueur choisit le sien
à la création du fonds ; il est conservé dans la sauvegarde.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()

CRESTS = r"""
/* ─── Écussons ─────────────────────────────────────────────────────────────── */
const CREST_SHIELD='M4 6 H68 V50 C68 68 52 78 36 82 C20 78 4 68 4 50 Z';
const CRESTS=[
 {nm:"Le phare",a:'#D9B06A',b:'#3FCF8E',
  d:'<path d="M4 26H68" stroke="$a" stroke-width="1.2" opacity=".45"/><path d="M36 16V62" stroke="$a" stroke-width="2"/><path d="M24 30 36 16 48 30" fill="none" stroke="$a" stroke-width="2.4" stroke-linejoin="round"/><circle cx="36" cy="46" r="7.5" fill="none" stroke="$b" stroke-width="2.4"/><path d="M18 62C26 56 46 56 54 62" fill="none" stroke="$b" stroke-width="2.2" stroke-linecap="round"/>',
  m:'M12 3 20 12H16V21H8V12H4Z'},
 {nm:"Le sommet",a:'#7C8FF0',b:'#D9B06A',
  d:'<path d="M16 54 28 38 36 46 46 26 56 40" fill="none" stroke="$a" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/><circle cx="46" cy="26" r="4" fill="$b"/><path d="M16 64H56" stroke="$a" stroke-width="1.6" opacity=".5"/>',
  m:'M2 20 9 9l4 5 7-11 2 17Z'},
 {nm:"La rose des vents",a:'#3FCF8E',b:'#D9B06A',
  d:'<circle cx="36" cy="42" r="19" fill="none" stroke="$a" stroke-width="1.6" opacity=".55"/><path d="M36 23 41 37 55 42 41 47 36 61 31 47 17 42 31 37Z" fill="$b"/><circle cx="36" cy="42" r="4" fill="#131F2E"/>',
  m:'M12 1 15 9l8 3-8 3-3 8-3-8-8-3 8-3Z'},
 {nm:"La clé de voûte",a:'#C9A227',b:'#9FB2CC',
  d:'<path d="M22 26H50L56 60H16Z" fill="none" stroke="$a" stroke-width="2.6" stroke-linejoin="round"/><path d="M28 26V60M44 26V60" stroke="$b" stroke-width="1.4" opacity=".5"/><path d="M16 66H56" stroke="$a" stroke-width="2"/>',
  m:'M6 4h12l4 17H2Z'},
 {nm:"Le chêne",a:'#3FCF8E',b:'#C9A227',
  d:'<path d="M36 62V38" stroke="$b" stroke-width="2.6"/><path d="M36 40C26 40 20 33 22 24c8-2 14 4 14 12 0-8 6-14 14-12 2 9-4 16-14 16Z" fill="$a"/><path d="M26 66h20" stroke="$b" stroke-width="2"/>',
  m:'M11 22V12C5 12 2 8 3 3c5-1 8 3 8 8 0-5 3-9 8-8 1 5-2 9-8 9v10Z'},
 {nm:"L'ancre",a:'#7C8FF0',b:'#D9B06A',
  d:'<circle cx="36" cy="24" r="5" fill="none" stroke="$a" stroke-width="2.6"/><path d="M36 29V64" stroke="$a" stroke-width="2.8"/><path d="M24 38H48" stroke="$a" stroke-width="2.4"/><path d="M18 50c0 10 8 15 18 15s18-5 18-15" fill="none" stroke="$b" stroke-width="2.6" stroke-linecap="round"/>',
  m:'M12 2a3 3 0 1 1 0 6 3 3 0 0 1 0-6Zm-1 7h2v13h-2ZM6 11h12v2H6Zm-3 6c0 5 4 7 9 7s9-2 9-7h-2c0 3-3 5-7 5s-7-2-7-5Z'},
 {nm:"Le pont",a:'#5FBFC4',b:'#D9B06A',
  d:'<path d="M12 58C12 36 60 36 60 58" fill="none" stroke="$a" stroke-width="2.8"/><path d="M12 58V66M60 58V66M36 44V66" stroke="$b" stroke-width="2"/><path d="M10 66H62" stroke="$a" stroke-width="2.4"/>',
  m:'M1 20C1 6 23 6 23 20h-2c0-10-18-10-18 0Zm10-8h2v9h-2ZM0 21h24v2H0Z'},
 {nm:"La tour",a:'#9FB2CC',b:'#C9A227',
  d:'<path d="M24 24h6v-6h4v6h4v-6h4v6h6v40H24Z" fill="none" stroke="$a" stroke-width="2.4" stroke-linejoin="round"/><path d="M33 44h6v20h-6Z" fill="$b"/><path d="M18 66h36" stroke="$a" stroke-width="2"/>',
  m:'M5 6h3V2h2v4h4V2h2v4h3v16H5Z'},
 {nm:"Le faucon",a:'#F2545B',b:'#D9B06A',
  d:'<path d="M10 34C22 30 30 36 36 46c6-10 14-16 26-12-6 14-14 22-26 26-12-4-20-12-26-26Z" fill="$a" opacity=".9"/><circle cx="36" cy="30" r="3.4" fill="$b"/>',
  m:'M1 7c7-3 10 1 11 6 1-5 4-9 11-6-3 8-7 12-11 14C8 19 4 15 1 7Z'},
 {nm:"Le sablier",a:'#D9B06A',b:'#5FBFC4',
  d:'<path d="M20 20h32L36 42 52 64H20L36 42Z" fill="none" stroke="$a" stroke-width="2.6" stroke-linejoin="round"/><path d="M27 58h18L36 46Z" fill="$b"/><path d="M16 18h40M16 66h40" stroke="$a" stroke-width="2.2"/>',
  m:'M3 1h18L12 12l9 11H3l9-11Z'},
 {nm:"L'étoile polaire",a:'#7C8FF0',b:'#D9B06A',
  d:'<path d="M36 18 40 36 58 40 40 44 36 62 32 44 14 40 32 36Z" fill="$b"/><circle cx="20" cy="24" r="2.2" fill="$a"/><circle cx="54" cy="56" r="2.2" fill="$a"/><circle cx="54" cy="24" r="1.6" fill="$a" opacity=".7"/>',
  m:'M12 0 14 10l10 2-10 2-2 10-2-10-10-2 10-2Z'},
 {nm:"Le rouage",a:'#C9A227',b:'#9FB2CC',
  d:'<circle cx="36" cy="42" r="14" fill="none" stroke="$a" stroke-width="3"/><circle cx="36" cy="42" r="5" fill="$b"/><path d="M36 22v8M36 54v8M16 42h8M48 42h8M22 28l6 6M50 56l-6-6M50 28l-6 6M22 56l6-6" stroke="$a" stroke-width="2.4" stroke-linecap="round"/>',
  m:'M12 0l2 3h3l1 3 3 2-1 3 1 3-3 2-1 3h-3l-2 3-2-3H7l-1-3-3-2 1-3-1-3 3-2 1-3h3Zm0 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8Z'}
];
function crestSvg(i,px){const c=CRESTS[((i|0)%CRESTS.length+CRESTS.length)%CRESTS.length];
 return `<svg viewBox="0 0 72 88" width="${px}" height="${Math.round(px*88/72)}" aria-hidden="true">
  <path d="${CREST_SHIELD}" fill="#131F2E" stroke="${c.a}" stroke-width="2.5"/>
  ${c.d.replace(/\$a/g,c.a).replace(/\$b/g,c.b)}</svg>`;}
/* marque pleine, lisible à 9 px : disque de la couleur dominante + forme simple */
function crestMark(i,cx,cy,r){const c=CRESTS[((i|0)%CRESTS.length+CRESTS.length)%CRESTS.length];
 const s=(r*1.5)/24;
 return `<circle cx="${cx.toFixed(1)}" cy="${cy.toFixed(1)}" r="${r}" fill="${c.a}" opacity=".95"/>`
  +`<g transform="translate(${(cx-r*0.75).toFixed(1)},${(cy-r*0.75).toFixed(1)}) scale(${s.toFixed(3)})">`
  +`<path d="${c.m}" fill="#0E1621"/></g>`;}
const RIVCREST=[1,3,8,10];
"""
e.rep("""const TAPE_UP='#3FCF8E',TAPE_DN='#F2545B';""",
      """const TAPE_UP='#3FCF8E',TAPE_DN='#F2545B';"""+CRESTS)

# concurrents identifiés par leur écusson sur le ruban
e.rep("""  riv+=`<circle cx="${f(ex)}" cy="${f(ey)}" r="5.4" fill="${c}" opacity=".92"/>`
     +`<text x="${f(ex)}" y="${f(ey+2)}" text-anchor="middle" font-size="5.6" font-weight="700" fill="#0E1621" font-family="ui-monospace,monospace">${rivTag(r.nm)}</text>`;""",
"""  riv+=crestMark(r.crest!==undefined?r.crest:RIVCREST[j%4],ex,ey,5.6);""")
e.rep("""  riv+=`<polyline points="${pts}" fill="none" stroke="${c}" stroke-width=".9" opacity=".28" stroke-linejoin="round"/>`;""",
"""  riv+=`<polyline points="${pts}" fill="none" stroke="${CRESTS[(r.crest!==undefined?r.crest:RIVCREST[j%4])%CRESTS.length].a}" stroke-width="1.1" opacity=".42" stroke-linejoin="round"/>`;""")
e.rep("""  return {nm:r.nm,pts};""","""  return {nm:r.nm,crest:RIVCREST[j%4],pts};""")
e.rep(""" const rivals=RIVALS.map((x,j)=>({nm:x.nm,pts:mk(11+j,0.011).pts}));""",
      """ const rivals=RIVALS.map((x,j)=>({nm:x.nm,crest:RIVCREST[j%4],pts:mk(11+j,0.011).pts}));""")

# choix de l'écusson à la création du fonds
e.rep("""let fundName='';""","""let fundName='';let fundCrest=Math.floor(Math.random()*12);""")
e.rep("""   <div class="namerow"><button class="cta ghost" id="shuffle" style="margin:0">Proposez-m'en un</button></div>""",
"""   <div class="namerow"><button class="cta ghost" id="shuffle" style="margin:0">Proposez-m'en un</button></div>
   <div class="kicker" style="margin-top:14px">ET UN ÉCUSSON</div>
   <div class="crestrow" id="crests">${CRESTS.map((c,i)=>`<button class="crestb${i===fundCrest?' on':''}" data-c="${i}" title="${c.nm}">${crestSvg(i,40)}</button>`).join('')}</div>""")
e.rep(""" document.getElementById('shuffle').onclick=()=>{fundName=randName();inp.value=fundName};""",
""" document.getElementById('shuffle').onclick=()=>{fundName=randName();inp.value=fundName};
 app.querySelectorAll('[data-c]').forEach(b=>b.onclick=()=>{fundCrest=+b.dataset.c;
   app.querySelectorAll('[data-c]').forEach(z=>z.classList.toggle('on',+z.dataset.c===fundCrest))});""")
e.rep(""".rivs{display:grid;""",
""".crestrow{display:grid;grid-template-columns:repeat(6,1fr);gap:6px;margin-top:8px}
.crestb{padding:4px 0;border:1px solid var(--line);border-radius:8px;background:var(--panel);line-height:0}
.crestb.on{border-color:var(--gold);background:rgba(217,176,106,.12)}
.rivs{display:grid;""")
# l'écusson suit la partie
e.rep("""   idx:1,hwmIdx:1,peakIdx:1,""","""   crest:fundCrest,idx:1,hwmIdx:1,peakIdx:1,""")
e.rep("""  <div class="kicker">${S.fundName.toUpperCase()} · RAPPORT AUX INVESTISSEURS""",
"""  <div style="text-align:center;margin-bottom:6px">${crestSvg(S.crest||0,64)}</div>
  <div class="kicker">${S.fundName.toUpperCase()} · RAPPORT AUX INVESTISSEURS""")

e.done("lot 24 — ecussons")
