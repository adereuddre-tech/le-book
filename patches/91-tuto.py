# -*- coding: utf-8 -*-
"""Lot 9 (suite) — écran de création et tutoriel.

- « Composez votre équipe » devient « Créez votre fonds », et il y a cinq choix, pas quatre.
- Le paragraphe d'introduction et les cinq explications dorées passent en pop-up : un bouton
  ouvre l'introduction, un « ? » à côté de chaque titre ouvre l'explication du choix.
  L'écran de création redevient une liste de choix et non un mur de texte.
- Le tutoriel et les info-bulles ne reviennent plus après la première partie : l'état est
  retenu dans le navigateur (`lebook_tuto_v1`), là où ce n'était qu'une variable de page
  remise à vrai à chaque rechargement.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()

# ── mémoire du tutoriel ──
e.rep("""let TUTO=true;
let SHOWHINTS=true;""",
"""/* Le tutoriel ne doit revenir ni au rechargement de la page ni à la partie suivante. */
function tutoSeen(){try{return localStorage.getItem('lebook_tuto_v1')==='1'}catch(e){return false}}
function markTutoSeen(){try{localStorage.setItem('lebook_tuto_v1','1')}catch(e){}}
let TUTO=!tutoSeen();
let SHOWHINTS=!tutoSeen();""")
e.rep("""if(b)b.onclick=()=>{S.tuto=99;TUTO=false;const m=document.getElementById('modal');if(m)m.remove();toast('Tutoriel désactivé.')};""",
      """if(b)b.onclick=()=>{S.tuto=99;TUTO=false;SHOWHINTS=false;markTutoSeen();const m=document.getElementById('modal');if(m)m.remove();toast('Tutoriel désactivé.')};""")
e.rep("""if(b)b.onclick=()=>{S.tuto=99;TUTO=false;const m=document.getElementById('modal');if(m)m.remove();toast('Info-bulles désactivées.')};""",
      """if(b)b.onclick=()=>{S.tuto=99;TUTO=false;SHOWHINTS=false;markTutoSeen();const m=document.getElementById('modal');if(m)m.remove();toast('Info-bulles désactivées.')};""")
e.rep(""" FEATS.forEach(f=>{if(f.tf){try{if(f.tf(S.finalCtx))award(f.id)}catch(e){}}});""",
""" FEATS.forEach(f=>{if(f.tf){try{if(f.tf(S.finalCtx))award(f.id)}catch(e){}}});
 markTutoSeen();TUTO=false;SHOWHINTS=false;   /* une partie jouée : le tutoriel a fait son office */""")

# ── titre, sous-titre, introduction repliée dans une pop-up ──
e.rep("""  <h1 style="font-size:clamp(36px,11vw,58px)">Composez votre équipe</h1>
  <div class="sub">quatre choix, puis le premier trimestre</div>
 </div>
 <div class="prose">""",
"""  <h1 style="font-size:clamp(36px,11vw,58px)">Créez votre fonds</h1>
  <div class="sub">cinq choix, puis le premier trimestre</div>
 </div>
 <button class="cta ghost" id="howto" style="margin-top:12px">Comment on joue, comment on gagne</button>
 <div class="prose" id="introprose" style="display:none">""")

# ── les explications dorées derrière un « ? » ──
e.rep("""   <div class="pickhead"><h2>${title}</h2><span>${hint}</span></div>
   ${SHOWHINTS&&SETUPHINTS[key]?`<div class="flag" data-hint="${key}"><span>${SETUPHINTS[key]}</span><button class="hintx" data-hintx="${key}" aria-label="Masquer">×</button></div>`:''}""",
"""   <div class="pickhead"><h2>${title}${SETUPHINTS[key]?`<button class="hintq" data-hintq="${key}" aria-label="À quoi ça sert ?">?</button>`:''}</h2><span>${hint}</span></div>""")
e.rep(""" app.querySelectorAll('[data-hintx]').forEach(b=>b.onclick=e=>{e.stopPropagation();delete SETUPHINTS[b.dataset.hintx];renderPicks()});""",
""" app.querySelectorAll('[data-hintq]').forEach(b=>b.onclick=ev=>{ev.stopPropagation();
   openModal(b.closest('.pickhead').querySelector('h2').childNodes[0].textContent.trim(),`<p>${SETUPHINTS[b.dataset.hintq]}</p>`)});
 {const hb=document.getElementById('howto'),ip=document.getElementById('introprose');
  const open=()=>{
    openModal('Comment on joue',ip.innerHTML+`<p style="margin-top:12px"><button class="buy" id="tutooff">Ne plus afficher le tutoriel</button></p>`);
    const b=document.getElementById('tutooff');
    if(b)b.onclick=()=>{TUTO=false;SHOWHINTS=false;markTutoSeen();const m=document.getElementById('modal');if(m)m.remove();toast('Tutoriel désactivé.')};
  };
  if(hb&&ip){hb.onclick=open;
   if(SHOWHINTS&&!window.__introShown){window.__introShown=1;setTimeout(open,400)}}}""")
e.rep(""".pickhead h2{font-size:16px;""",
""".hintq{display:inline-flex;align-items:center;justify-content:center;width:17px;height:17px;margin-left:6px;
 border-radius:50%;border:1px solid var(--gold);background:transparent;color:var(--gold);
 font-size:11px;font-weight:600;line-height:1;vertical-align:middle;flex-shrink:0}
.pickhead h2{font-size:16px;""")

e.done("lot 9 — creation et tutoriel")
