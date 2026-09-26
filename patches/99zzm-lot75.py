# -*- coding: utf-8 -*-
"""Lot 75 — retours de jeu, affichage et un peu d'équilibre.
1. Ordres du book : montant notionnel (3 chiffres significatifs, k$ ou M$) au lieu du nombre d'unités.
2. Marchés : vrais noms des sous-jacents en anglais ; l'ancien libellé français passe en tête du sous-titre.
3. Nuage rentabilité / risque : jauges à couleur uniforme (celle de la valeur), bouts arrondis, pastille au bout,
   trace discrète ; vignette en HTML (le SVG étiré déformait les arrondis). Triangles retirés.
4. Dépêche « Scandale comptable chez un géant de la tech » : le Nasdaq bouge, pas le S&P 500.
5. Minuteur : pleine largeur, en bas, et la page réserve la place dessous. La pastille « confiance » des
   anecdotes d'exécution (que le minuteur masquait) passe dans la description du choix.
6. Cartes de croissance étalées : ×1,15 · (ouverture ×1,4) · ×1,7 · (ouverture ×2,0) · ×2,5 · ×3,2.
7. Conseil de début de trimestre : gains et risques chiffrés sous chaque choix.
8. Carte « Débauché » : trader de la classe (« exotic markets » pour les exotiques).
9. OAT : charge appétit pour le risque −0,08 → +0,25 (prime de spread).
10. Ruban de mi-trimestre : « DEPUIS LE LANCEMENT » seul.
11. Classement du portage du modèle (quant) retiré : doublon du signal C des lignes.
12. Classements : nom du gérant à la ligne sous le nom du fonds."""
import sys,re; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
# ---- 1. montant des ordres
e.rep("""function ordTxt(i){""","""/* lot 75 : montant en k$ / M$ à 3 chiffres significatifs (x en Md$) */
function amt3(x){let a=Math.abs(x)*1000,u='M$';if(a<1){a*=1000;u='k$'}
 const p=Math.pow(10,Math.floor(Math.log10(a))-2),r=Math.round(a/p)*p,d=Math.max(0,2-Math.floor(Math.log10(r)));
 return r.toFixed(d).replace('.',',').replace(/\\B(?=(\\d{3})+(?!\\d))/g,'\\u202f')+' '+u}
function ordTxt(i){""")
e.rep("""${d>0?'achat':'vente'} ${Math.abs(d)}</b>""","""${d>0?'achat':'vente'} ${amt3(notionalBn(Math.abs(d),i))}</b>""")
# ---- 2. noms anglais
EN={'NQ':'Nasdaq 100','ES':'S&P 500','ESTX':'Euro Stoxx 50','TOPX':'TOPIX','MXEF':'MSCI Emerging Markets',
 'TN':'10-Year T-Note','GBL':'Euro-Bund','R':'Long Gilt','OAT':'Euro-OAT','JGB':'10-Year JGB',
 'EUR':'Euro FX','JPY':'Japanese Yen','GBP':'British Pound','AUD':'Australian Dollar','MXP':'Mexican Peso',
 'CL':'WTI Crude Oil','HG':'Copper','GC':'Gold','KC':'Coffee','ZW':'Chicago Wheat',
 'BTC':'Bitcoin','VX':'VIX','EUA':'EU Carbon Allowances','BDI':'Baltic Dry Index','NRAM':'Rainfall Index'}
a=e.s.index("const INSTR_ALL=[\n");b=e.s.index("\n];",a)
blk=e.s[a:b];n=0
def fix(m):
    global n;n+=1;sy,nm,sub=m.group(1),m.group(2),m.group(3)
    rest=sub.split(' · ',1)[1] if sub.startswith('dérivé')==False else sub
    if sy=='NRAM':rest=sub
    return "{sym:'%s'%s,nm:'%s',sub:'%s · %s'"%(sy,m.group(4),EN[sy],nm.replace("'","\\'"),rest)
blk2=re.sub(r"\{sym:'(\w+)'(,\s*rk:\d),nm:'([^']*)',\s*sub:'((?:[^'\\]|\\.)*)'",lambda m:fix(type('M',(),{'group':lambda s,k:{1:m.group(1),2:m.group(3),3:m.group(4),4:m.group(2)}[k]})()),blk)
assert n==25,n
e.s=e.s[:a]+blk2+e.s[b:]
for o in ["Il traite ${INSTR[i].nm.toLowerCase()} mieux","sur ${x.nm.toLowerCase()}.`"]:
    e.rep(o,o.replace('.nm.toLowerCase()','.nm'))
e.rep("g:nx.map(x=>`${x.sym} · ${x.nm.toLowerCase()}`)","g:nx.map(x=>`${x.sym} · ${x.nm}`)")
e.rep("g:nw.map(x=>`${x.sym} · ${x.nm.toLowerCase()}`)","g:nw.map(x=>`${x.sym} · ${x.nm}`)")
# ---- 8. débauché
e.rep("d:`Un trader ${INSTR[S.star].nm.toLowerCase()} quitte","d:`Un trader ${({Actions:'actions',Taux:'taux',Devises:'devises','Matières premières':'matières premières',Exotiques:'exotic markets'})[INSTR[S.star].grp]||'macro'} quitte")
# ---- 3. jauges
e.rep("""  let g=`<defs>${gzGrad('gzxB',stX,0,xm,0,x0,x1)}${gzGrad('gzyB',stY,y0,y1,1,Y(y0),Y(y1))}</defs>`
   +gzBar('gzxB',0,yb+1,3,x0,X(sq),x0,x1,1.5)+gzBar('gzyB',1,x0-4,3,Y(0),Y(pr),Y(y0),Y(y1),1.5);""",
"""  /* lot 75 : jauges pleines, couleur de la valeur, bouts ronds, pastille au bout, trace discrète */
  const ya=Math.min(Y(0),Y(pr)),yh=Math.abs(Y(pr)-Y(0));
  let g=`<rect x="${x0}" y="${yb+2}" width="${x1-x0}" height="4" rx="2" fill="#F3EEE4" opacity=".07"/>`
   +`<rect x="${x0-6}" y="${yt}" width="4" height="${yb-yt}" rx="2" fill="#F3EEE4" opacity=".07"/>`
   +`<rect x="${x0}" y="${yb+2}" width="${f(Math.max(4,X(sq)-x0))}" height="4" rx="2" fill="${cX}"/>`
   +`<rect x="${x0-6}" y="${f(ya)}" width="4" height="${f(Math.max(4,yh))}" rx="2" fill="${cY}"/>`
   +`<line x1="${x0-8}" x2="${x0}" y1="${f(Y(0))}" y2="${f(Y(0))}" stroke="#F3EEE4" stroke-width=".8" opacity=".5"/>`;""")
e.rep("""  g+=`<path d="M${f(px-3.5)} ${yb+7.5} L${f(px+3.5)} ${yb+7.5} L${f(px)} ${yb+1.5}Z" fill="#F3EEE4" stroke="var(--bg,#0b1020)" stroke-width=".6"/>`
   +`<path d="M${x0-7.5} ${f(py-3.5)} L${x0-7.5} ${f(py+3.5)} L${x0-1.5} ${f(py)}Z" fill="#F3EEE4" stroke="var(--bg,#0b1020)" stroke-width=".6"/>`""",
"""  g+=`<circle cx="${f(Math.max(x0+2,px))}" cy="${yb+4}" r="3.4" fill="${cX}" stroke="var(--bg,#0b1020)" stroke-width="1.4"/>`
   +`<circle cx="${x0-4}" cy="${f(py)}" r="3.4" fill="${cY}" stroke="var(--bg,#0b1020)" stroke-width="1.4"/>`""")
e.rep("""<text x="${f(X(v))}" y="${yb+13}" font-size="8\"""","""<text x="${f(X(v))}" y="${yb+15}" font-size="8\"""")
e.rep("""<text x="${x0-7}" y="${f(Y(v)+3)}" font-size="8\"""","""<text x="${x0-10}" y="${f(Y(v)+3)}" font-size="8\"""")
e.rep("""<text x="${x0+2}" y="${yb+13}" font-size="8.5\"""","""<text x="${x0+2}" y="${yb+15}" font-size="8.5\"""")
e.rep("""  +`<defs>${gzGrad(gid+'x',stX,0,xm,0,L,100-Rr)}${gzGrad(gid+'y',stY,y0,y1,1,Y(y0),Y(y1))}</defs>`
  +gzBar(gid+'x',0,100-B+.6,B-.6,L,X(sq),L,100-Rr)+gzBar(gid+'y',1,0,L-.6,Y(0),Y(pr),Y(y0),Y(y1))
""","")
e.rep("""  +`<i class="gzc" style="left:${f(px)}%;bottom:0"></i><i class="gzc v" style="left:0;top:${f(py)}%"></i>`""",
"""  +`<i class="gzt x" style="left:${L}%;right:${Rr}%"></i><i class="gzt y" style="top:${T}%;bottom:${B}%"></i>`
  +`<i class="gzb x" style="left:${L}%;width:${f(Math.max(0,px-L))}%;background:${cX}"></i>`
  +`<i class="gzb y" style="top:${f(Math.min(Y(0),py))}%;height:${f(Math.abs(py-Y(0)))}%;background:${cY}"></i>`
  +`<i class="gzk x" style="left:${f(px)}%;background:${cX}"></i><i class="gzk y" style="top:${f(py)}%;background:${cY}"></i>`""")
e.rep(""".rmap .gzc{position:absolute;width:0;height:0;margin-left:-3.5px;border:3.5px solid transparent;border-bottom:5px solid #F3EEE4;border-top:0}
.rmap .gzc.v{margin:-3.5px 0 0;border:3.5px solid transparent;border-right:0;border-left:5px solid #F3EEE4}""",
""".rmap .gzt,.rmap .gzb{position:absolute;border-radius:2px}
.rmap .gzt{background:rgba(243,238,228,.07)}
.rmap .gzt.x,.rmap .gzb.x{bottom:1px;height:3px}.rmap .gzt.y,.rmap .gzb.y{left:1px;width:3px}
.rmap .gzb.x{min-width:3px}.rmap .gzb.y{min-height:3px}
.rmap .gzk{position:absolute;width:7px;height:7px;border-radius:50%;border:1.5px solid var(--bg,#0b1020);box-sizing:border-box}
.rmap .gzk.x{bottom:-1px;margin-left:-3.5px}.rmap .gzk.y{left:-1px;margin-top:-3.5px}""")
# ---- 4. scandale
e.rep("""hit:{ES:-1.4,ESTX:-0.4,GC:0.5,TN:0.5}""","""hit:{NQ:-1.6,ESTX:-0.3,GC:0.5,TN:0.5}""")
# ---- 5. minuteur
e.rep(" el.classList.add('on');\n"," el.classList.add('on');document.body.classList.add('tmron');\n")
e.rep("function clearTimer(){if(TID){clearInterval(TID);TID=null}","function clearTimer(){document.body.classList.remove('tmron');if(TID){clearInterval(TID);TID=null}")
e.rep("</style>","""/* lot 75 : minuteur pleine largeur (celle de l'app), en bas, place réservée dessous */
.evtimer{left:max(12px,calc(50% - 328px));right:max(12px,calc(50% - 328px));max-width:none!important;bottom:max(12px,env(safe-area-inset-bottom))}
.evtimer .tlb{max-width:none!important}
body.tmron #app{padding-bottom:150px}
.bossn{display:block;font-size:.82em;color:var(--dim);font-weight:400}
</style>""")
e.rep("""  if(gx.lp||gx.rc)out.push(`<span class="stk">${gz(gx.lp,gx.rc)}</span>`);\n""","")
e.rep("""<b>${c.b}</b><span>${fxTxt(c.s,c.e)}${stake(c)}""","""<b>${c.b}</b><span>${fxTxt(c.s,c.e)}${(()=>{const x=c.e||{},q=execGz(x.tcMult,x.leakQ),v=cf(q.lp,q.rc);return v?` Manière d'exécuter : confiance ${v>0?'+':'−'}${Math.abs(v)}.`:''})()}${stake(c)}""")
# ---- 6. seuils des cartes
for o,n2 in [("g>=1.2,","g>=1.15,"),("ENCOURS ×1,2'","ENCOURS ×1,15'"),("g>=1.5,","g>=1.7,"),("ENCOURS ×1,5'","ENCOURS ×1,7'"),("g>=1.6,","g>=2.5,"),("g>=2.2,","g>=3.2,"),("ENCOURS ×2,2'","ENCOURS ×3,2'")]:
    e.rep(o,n2)
e.s=e.s.replace("ENCOURS ×1,6'","ENCOURS ×2,5'") if e.s.count("ENCOURS ×1,6'")==2 else (_ for _ in ()).throw(AssertionError('x1,6'))
# ---- 7. conseil : effets chiffrés
e.rep("function screenBoard(){","""/* lot 75 : ce que coûte et rapporte chaque choix du conseil, en clair */
function boardFx(x){x=x||{};const o=[],c=v=>v>0?'pos-g':v<0?'neg-g':'dim-g',sg=v=>(v>0?'+':'−');
 const v=cf(x.lp,x.rc);if(v)o.push(`confiance <em class="${c(v)}">${sg(v)}${Math.abs(v)}</em>`);
 if(x.aum)o.push(`encours <em class="${c(x.aum)}">${sg(x.aum)}${dec(Math.abs(x.aum)*100,0)} % · ${sg(x.aum)}${mm(Math.abs(x.aum)*S.nav)}</em>`);
 if(x.cash)o.push(`fonds <em class="${c(x.cash)}">${sg(x.cash)}${Math.round(Math.abs(x.cash)*1e4)} pb · ${sg(x.cash)}${mm(Math.abs(x.cash)*S.nav)}</em>`);
 if(x.noise)o.push(`<em class="neg-g">indicateurs plus bruités</em>`);
 if(x.flighty)o.push(`<em class="neg-g">investisseurs plus prompts à racheter</em>`);
 if(x.leak)o.push(`<em class="neg-g">positions connues du marché</em>`);
 if(x.carry)o.push(`<em class="dim-g">book orienté portage</em>`);
 if(x.tgt)o.push(`cible de risque <em>${pct(x.tgt)}</em>`);
 if(x.cut)o.push(`<em class="neg-g">${x.cut.filter(s=>IDX[s]!==undefined).join(', ')} coupés de moitié</em>`);
 return o.length?`<span class="stks">${o.map(s=>`<span class="stk">${s}</span>`).join('')}</span>`:''}
function screenBoard(){""")
e.rep("""<b>${c.b}</b><span>${fxTxt(c.s,c.e)}${ko?' <b class="neg-g">hors trésorerie</b>':''}</span></button>`}).join('')}</div>`;
 const pickB=""","""<b>${c.b}</b><span>${c.s}${boardFx(c.e)}${ko?' <b class="neg-g">hors trésorerie</b>':''}</span></button>`}).join('')}</div>`;
 const pickB=""")
# ---- 9. OAT
e.rep("b:[-0.20,-0.58, 0.26,-0.08], mg:0.025}","b:[-0.20,-0.58, 0.26, 0.25], mg:0.025}")
# ---- 10. ruban
e.rep("<span>T${S.q+1} JUSQU'ICI · DEPUIS LE LANCEMENT</span>","<span>DEPUIS LE LANCEMENT</span>")
# ---- 11. classement du portage
i=e.s.index("   ${S.prof==='syst'&&S.tcvEst?(()=>{const o=INSTR.map((x,i)=>({x,i,c:S.tcvEst.c[i]}))")
j=e.s.index("</details>`})():''}\n",i)+len("</details>`})():''}\n")
assert e.s[i:j].count('carryrk')==1
e.s=e.s[:i]+e.s[j:]
# ---- 12. gérant à la ligne
e.rep("nm:r.nm+' · '+r.boss,","nm:r.nm+'<span class=\"bossn\">'+r.boss+'</span>',")
e.rep("nm:x.nm+' · '+x.boss,","nm:x.nm+'<span class=\"bossn\">'+x.boss+'</span>',")
e.done("lot 75")
