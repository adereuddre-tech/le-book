# -*- coding: utf-8 -*-
"""Lot 55 — nettoyage du desk, du book et du débriefing (première passe).

Principe : chaque écran garde en vue la décision et son enjeu chiffré ; les explications et
les tableaux techniques se replient. Mesures avant / après à 380 px (`tools/outline.py`).

Desk (sources) :
  - les trois sources les plus parlantes restent visibles (vérifiée, pré-annonces, fiabilité
    forte d'abord) ; les autres passent dans « Toutes les sources » ;
  - « Lecture consolidée » se replie : les quatre tuiles de facteurs de la barre d'état disent
    la même chose ;
  - « Comment lire ces sources » parlait encore d'achat de sources (retiré au lot S) : réécrit.
Book :
  - la ligne des codes d'exposition (C++ I0 D+ A++) laisse la place à « par unité · risque »,
    et l'ordre à passer reste à droite : une ligne de moins par marché, les expositions sont
    dans le détail du marché.
Débriefing :
  - « Du brut au net » se replie ;
  - « Ce qu'ils en disent » n'affiche plus deux jauges (dont celle du comité, qui n'existe plus
    à l'écran) : la confiance, la voix des investisseurs, et le carton du trimestre ;
  - les flux clients par concurrent passent en tête, avec l'objectif et les cartons.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
def between(a,b):
    assert e.s.count(a)==1,'debut ambigu %r'%a[:60]
    i=e.s.index(a); j=e.s.index(b,i); return e.s[i:j]
# ── desk ───────────────────────────────────────────────────────────────────────
e.rep("function renderNews(){\n const el=document.getElementById('news');if(!el)return;\n el.innerHTML=S.rumors.map(r=>",
      "function renderNews(){\n const el=document.getElementById('news');if(!el)return;\n /* trois sources en vue, les plus parlantes ; les autres repliées */\n const rk=r=>(r.sure?0:r.ev?1:r.rel==='forte'?2:r.rel==='moyenne'?3:4);\n const ord=[...S.rumors].sort((a,b)=>rk(a)-rk(b));\n const one=r=>")
old=between(" const one=r=>","\n const rs=document.getElementById('rsum');")
body=old[len(" const one=r=>"):]
assert body.rstrip().endswith(".join('');"),body[-60:]
body=body.rstrip()[:-len(".join('');")]
body=body[len("S.rumors.map(r=>"):] if body.startswith("S.rumors.map(r=>") else body
if body.rstrip().endswith(")"):body=body.rstrip()[:-1]   # la parenthèse fermante du .map(
e.rep(old," const one=r=>"+body+";")
e.rep(" const rs=document.getElementById('rsum');",
      " el.innerHTML=ord.slice(0,3).map(one).join('')+(ord.length>3?`<details class=\"srcmore\"><summary>Toutes les sources · ${ord.length-3} de plus</summary>${ord.slice(3).map(one).join('')}</details>`:'');\n const rs=document.getElementById('rsum');",k=1)
e.rep("<summary>Comment lire ces sources</summary><p class=\"note\">Une source non achetée ne livre que son origine, le facteur qu'elle concerne et le début de son propos. L'acheter révèle le contenu, l'effet prétendu sur les quatre facteurs et la <em>fiabilité</em> — la probabilité qu'elle dise vrai. Le nombre de sources et leur fiabilité dépendent de votre budget de recherche macro et de votre style ; elles ne s'achètent pas à l'unité.</p>",
      "<summary>Comment lire ces sources</summary><p class=\"note\">Chaque source prétend un effet sur les quatre facteurs (▼▼ à ▲▲) et porte une <em>fiabilité</em> : la probabilité qu'elle dise vrai. Leur nombre et leur fiabilité dépendent du budget de recherche macro et de votre style. Les quatre tuiles de la barre du haut en donnent la lecture consolidée ; le rendement attendu de chaque marché en tient compte.</p>")
e.rep("""   <div class="blockhead" style="margin-top:14px"><h2>Lecture consolidée</h2><span class="hint">sources achetées</span></div>""",
      """   <details style="margin-top:10px"><summary>Lecture consolidée · déjà dans la barre du haut</summary>""")
e.rep("""   <div class="wire" id="rsum"></div>""","""   <div class="wire" id="rsum"></div></details>""")
e.rep(".lvls{display:grid;",".srcmore{margin-top:8px}.srcmore>summary{font-size:13.5px;color:var(--dim)}\n.lvls{display:grid;")
# ── book : une ligne par marché en moins ───────────────────────────────────────
old=between(" const gl=x.b.map((b,k)=>{","\n const k0=S.k0?S.k0[i]:S.k[i],d=S.k[i]-k0;")
e.rep(old,""" /* lot 55 : les expositions sont dans le détail du marché ; ici, ce qui décide */
 let gl='';
 if(mktOpen(i)&&S.tcvEst){const o=expRet(i),w1=U/x.sig,g={m:w1*o.m,s:w1*o.s},rp=S.k[i]?riskPts(S.k)[i]:riskAdd(i,S.k);
  gl=`<span class="xk">unité</span> ${expShort(g)}${(S.size||'mid')==='small'?`<span class="dim-g"> ±${dec(2*g.s*100,1)}</span>`:''} <span class="xk" style="margin-left:8px">${S.k[i]?'risque':'+1'}</span> <span class="${rp>0.05?'neg-g':rp<-0.05?'pos-g':'dim-g'}">${rp>=0?'+':'−'}${dec(Math.abs(rp),1)} pt</span>`}""")
old=between("     ${mktOpen(i)&&S.tcvEst?(()=>{const o=expRet(i),w1=U/x.sig,g={m:w1*o.m,s:w1*o.s},rp=S.k[i]?RP[i]:riskAdd(i,S.k),lv=S.size||'mid';","\n     <div class=\"tcv\">")
e.rep(old,"")
e.rep(".lvls{display:grid;",".rowinfo .xk{color:var(--dimmer);font-size:10.5px;margin-right:3px}\n.lvls{display:grid;")
# ── débriefing ─────────────────────────────────────────────────────────────────
e.rep("""  <div class="block"><div class="blockhead"><h2>Du brut au net</h2><span class="hint">en ${UQ.s.trim()}</span></div>""",
      """  <div class="block"><details><summary style="font-size:15px;color:var(--txt);font-weight:600">Du brut au net · en ${UQ.s.trim()}</summary>""")
e.rep("""ils changent l'encours sans compter dans la performance.</p></details>
  </div>
  <div class="block"><div class="blockhead"><h2>Vos gains</h2>""","""ils changent l'encours sans compter dans la performance.</p></details></details>
  </div>
  <div class="block"><div class="blockhead"><h2>Vos gains</h2>""")
e.rep("""<h2>Ce qu'ils en disent</h2><span class="hint">${Math.round(S.lp)} · ${Math.round(S.rc)}</span></div>""",
      """<h2>Ce qu'ils en disent</h2><span class="hint">confiance ${Math.round(conf())}</span></div>""")
e.rep("""    <div class="kicker" style="margin:12px 0 4px">LE COMITÉ DES RISQUES</div><p style="margin:0;color:var(--dim);font-size:13.5px">${V.com}</p></div>""",
      """    <div class="kicker" style="margin:12px 0 4px">LE COMITÉ DES RISQUES</div><p style="margin:0;color:var(--dim);font-size:13.5px">${S.qCard?(S.qCard.c==='rouge'?'🟥 ':'🟨 ')+'Carton '+S.qCard.c+' : '+S.qCard.why+'.':'Aucun carton ce trimestre.'}${S.cards&&S.cards.y&&!(S.qCard&&S.qCard.c==='rouge')?` ${S.cards.y} jaune${S.cards.y>1?'s':''} en cours.`:''}</p></div>""")
e.rep(" const warn=[];"," const warn=[];\n if(S.poachMsg)warn.push(S.poachMsg);   /* lot 55 : les flux clients par concurrent, en tête */")
# marchés fermés : une ligne, sans boutons ni signaux
e.rep("""   const nb=notionalBn(S.k[i],i);\n   h+=`<div class="pos">""","""   const nb=notionalBn(S.k[i],i);
   if(!mktOpen(i)){h+=`<div class="pos locked"><div class="top"><span class="sym" style="color:${GRPC[g]}">${x.sym}</span><span class="nm"><span class="mflag">${MFLAG[x.sym]||''}</span>${x.nm}</span>${x.grp==='Exotiques'&&x.rk<=OPENRK?'<span class="capb">🔒 1er d&#39;un trimestre</span>':`<span class="capb">🔒 ${mm(unlockNav(x.rk))}</span>`}</div></div>`;return}
   h+=`<div class="pos">""")
e.rep(".lvls{display:grid;",".pos.locked{opacity:.55;padding:6px 0}.pos.locked .top{margin:0}\n.lvls{display:grid;")
# la ligne d'info coupait l'ordre à passer (« achat 46,6 M$ · co… ») : elle passe à la ligne
e.rep(".rowinfo{display:flex;justify-content:space-between;gap:8px;font-family:var(--mono);font-size:10.5px;color:var(--dimmer);margin-top:5px;white-space:nowrap;overflow:hidden}",
      ".rowinfo{display:flex;justify-content:space-between;flex-wrap:wrap;gap:2px 8px;font-family:var(--mono);font-size:10.5px;color:var(--dimmer);margin-top:5px}")
# « Vos gains » affichait la trésorerie (score + capital de départ de la société) : 500 k$ d'écart
# avec « Cumul depuis le début » du débriefing. La tuile montre désormais le score, comme son nom.
e.rep("""<b id="gaintile" class="${mgrCash()>=0?'':'neg-g'}">${score(mgrCash())}</b>""","""<b id="gaintile" class="${mgrNet()>=0?'':'neg-g'}">${score(mgrNet())}</b>""")
e.rep(" const v=mgrCash();e.textContent=score(v);e.className=v>=0?'':'neg-g'}"," const v=mgrNet();e.textContent=score(v);e.className=v>=0?'':'neg-g'}")
e.done("lot 55 — nettoyage du desk, du book et du debriefing")
