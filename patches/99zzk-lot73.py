# -*- coding: utf-8 -*-
"""Lot 73 — nuage rentabilité / risque : libellés en clair (« risque », « rentabilité » au lieu de σ et μ)
et deux jauges de couleur le long des axes, calées sur les seuils du jeu :
 - risque (abscisses) : vert jusqu'à la moitié de la cible du mandat, ambre à la cible, rouge au seuil
   des accidents de levier (TAIL.x0) — le rouge commence exactement où la zone teintée commence ;
 - rentabilité (ordonnées) : rouge sous zéro, ambre à zéro, vert au niveau du meilleur concurrent
   (« vert = devant tout le monde ») ; à défaut de concurrent positif, au haut du cadre.
Un curseur blanc marque le fonds sur chaque jauge, et ses deux valeurs prennent la couleur de la jauge
à leur position : on lit la couleur avant le chiffre."""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
# 1. helpers : arrêts de dégradé et couleur interpolée
e.rep("function riskMap(sp,big){\n",
"""const GZC={g:[69,185,124],a:[232,184,74],r:[210,70,60]};
function gzCol(st,v){   /* st : [[valeur,'g'|'a'|'r'],…] croissant */
 const c=k=>GZC[k];if(v<=st[0][0])return c(st[0][1]);
 for(let j=1;j<st.length;j++)if(v<=st[j][0]){const[a,ka]=st[j-1],[b,kb]=st[j],t=b>a?(v-a)/(b-a):1;
  return c(ka).map((z,i)=>Math.round(z+(c(kb)[i]-z)*t))}
 return c(st[st.length-1][1]);
}
const rgb=a=>`rgb(${a.join(',')})`;
function gzGrad(id,st,lo,hi,vert){   /* dégradé SVG, offsets en fraction de l'axe */
 const o=v=>Math.max(0,Math.min(1,(v-lo)/(hi-lo)));
 const s=st.map(([v,k])=>`<stop offset="${(vert?1-o(v):o(v)).toFixed(3)}" stop-color="${rgb(GZC[k])}"/>`);
 if(vert)s.reverse();
 return `<linearGradient id="${id}" x1="0" y1="0" x2="${vert?0:1}" y2="${vert?1:0}">${s.join('')}</linearGradient>`;
}
function riskMap(sp,big){
""")
# 2. arrêts calculés une fois, après xm / y0 / y1
e.rep(""" const hot=tailP(sp)>0,me=myCol(S.rivals||[]),f=v=>v.toFixed(1);
 const sv=`${dec(sq*100,1)} %`,mv=`${pr>=0?'+':'−'}${dec(Math.abs(pr)*100,1)} %`;""",
""" const hot=tailP(sp)>0,me=myCol(S.rivals||[]),f=v=>v.toFixed(1);
 const sv=`${dec(sq*100,1)} %`,mv=`${pr>=0?'+':'−'}${dec(Math.abs(pr)*100,1)} %`;
 /* lot 73 : jauges. Risque : cible du mandat et seuil d'accident, en trimestriel. Rentabilité : zéro et meilleur concurrent. */
 const xr=TAIL.x0/2,xa=Math.min((S.tgt||0.2)/2,xr*0.85),stX=[[0,'g'],[xa*0.5,'g'],[xa,'a'],[xr,'r']];
 const best=Math.max(0,...R.map(r=>r.y)),yg=best>0.002?best:y1,stY=[[Math.min(y0,-0.001),'r'],[0,'a'],[yg,'g']];
 const cX=rgb(gzCol(stX,sq)),cY=rgb(gzCol(stY,pr));""")
# 3. grand format : jauges sous l'axe des abscisses et à gauche de l'axe des ordonnées, curseurs, libellés
e.rep("""  let g='';
  if(TAIL.x0/2<xm)g+=""","""  let g=`<defs>${gzGrad('gzxB',stX,0,xm,0)}${gzGrad('gzyB',stY,y0,y1,1)}</defs>`
   +`<rect x="${x0}" y="${yb+1}" width="${x1-x0}" height="3" rx="1.5" fill="url(#gzxB)"/>`
   +`<rect x="${x0-4}" y="${yt}" width="3" height="${yb-yt}" rx="1.5" fill="url(#gzyB)"/>`;
  if(TAIL.x0/2<xm)g+=""")
e.rep("""<text x="${f(X(v))}" y="${yb+11}" font-size="8" text-anchor="middle\"""","""<text x="${f(X(v))}" y="${yb+13}" font-size="8" text-anchor="middle\"""")
e.rep("""<text x="${x0-3}" y="${f(Y(v)+3)}" font-size="8" text-anchor="end\"""","""<text x="${x0-7}" y="${f(Y(v)+3)}" font-size="8" text-anchor="end\"""")
e.rep("""   +`<text x="${x1-2}" y="${yb-4}" font-size="11" text-anchor="end" fill="var(--dim)" font-family="var(--mono)">σ</text>`
   +`<text x="${x0+4}" y="${yt+10}" font-size="11" fill="var(--dim)" font-family="var(--mono)">μ</text>`;""",
"""   +`<text x="${x0+2}" y="${yb+13}" font-size="8.5" fill="var(--dim)" font-family="var(--mono)">risque →</text>`
   +`<text x="${x0+4}" y="${yt+10}" font-size="9" fill="var(--dim)" font-family="var(--mono)">↑ rentabilité</text>`;""")
e.rep('<text x="${f(X(r.x)+6)}" y="${f(Y(r.y)+3.5)}" font-size="9.5" fill="${r.c}"','<text x="${f(X(r.x)+(X(r.x)>x1-95?-6:6))}" y="${f(Y(r.y)+3.5)}" font-size="9.5" fill="${r.c}"${X(r.x)>x1-95?\' text-anchor="end"\':\'\'}')
e.rep("""${r.nm.split(' ')[0]} · σ ${dec(r.x*100,0)} · μ ${r.y>=0?'+':'−'}${dec(Math.abs(r.y)*100,0)}</text>`});""",
"""${r.nm.split(' ')[0]} · ${dec(r.x*100,0)} % · ${r.y>=0?'+':'−'}${dec(Math.abs(r.y)*100,0)} %</text>`});""")
e.rep("""  g+=`<line x1="${f(px)}" x2="${f(px)}" y1="${yb-4}" y2="${yb}" stroke="#F3EEE4" stroke-width="1"/><line x1="${x0}" x2="${x0+4}" y1="${f(py)}" y2="${f(py)}" stroke="#F3EEE4" stroke-width="1"/>`
   +`<text x="${f(Math.min(x1-40,Math.max(x0+22,px)))}" y="${yb-7}" font-size="10" text-anchor="middle" fill="${hot?'#E5675C':'#F3EEE4'}" font-family="var(--mono)" font-weight="700">σ ${sv}</text>`
   +`<text x="${x0+6}" y="${f(Math.min(yb-18,Math.max(yt+22,py+3.5)))}" font-size="10" fill="#F3EEE4" font-family="var(--mono)" font-weight="700">μ ${mv}</text>`""",
"""  /* curseurs : petits triangles blancs posés sur les jauges, pointés vers le cadre */
  g+=`<path d="M${f(px-3.5)} ${yb+7.5} L${f(px+3.5)} ${yb+7.5} L${f(px)} ${yb+1.5}Z" fill="#F3EEE4" stroke="var(--bg,#0b1020)" stroke-width=".6"/>`
   +`<path d="M${x0-7.5} ${f(py-3.5)} L${x0-7.5} ${f(py+3.5)} L${x0-1.5} ${f(py)}Z" fill="#F3EEE4" stroke="var(--bg,#0b1020)" stroke-width=".6"/>`
   +`<text x="${f(Math.min(x1-52,Math.max(x0+40,px)))}" y="${yb-7}" font-size="10" text-anchor="middle" fill="${cX}" font-family="var(--mono)" font-weight="700">risque ${sv}</text>`
   +`<text x="${x0+6}" y="${f(Math.min(yb-18,Math.max(yt+22,py+3.5)))}" font-size="10" fill="${cY}" font-family="var(--mono)" font-weight="700">rentabilité ${mv}</text>`""")
e.rep("""Valeurs <b>trimestrielles</b>. σ : risque du book sur un trimestre (la moitié du σ annuel des lignes de marché), bruit d'estimation compris. μ : rendement attendu du trimestre""",
"""Valeurs <b>trimestrielles</b>. Risque : volatilité du book sur un trimestre (la moitié de la volatilité annuelle des lignes de marché), bruit d'estimation compris ; sa jauge passe à l'ambre à la cible de votre mandat et au rouge là où commencent les accidents de levier. Rentabilité : rendement attendu du trimestre""")
e.rep("""coût moyen des accidents de levier compris. Traits tous les 5 %.""","""coût moyen des accidents de levier compris ; sa jauge est rouge sous zéro et verte au niveau du meilleur concurrent. Traits tous les 5 %.""")
e.rep("""Les concurrents sont placés à leur couple estimé.</p>""","""Les concurrents sont placés à leur couple estimé (risque · rentabilité).</p>""")
e.rep("""${tp>0?`À σ ${sv} :""","""${tp>0?`À ${sv} de risque :""")
e.rep("""`Sous σ ${dec(TAIL.x0*50,1)} % par trimestre,""","""`Sous ${dec(TAIL.x0*50,1)} % de risque par trimestre,""")
# 4. vignette : jauges dans les marges, curseurs, libellés colorés
e.rep(""" const L=3,Rr=4,T=5,B=3;""",""" const L=3,Rr=4,T=5,B=3,gid='gz'+(++riskMap.n);""")
e.rep("""  +(TAIL.x0/2<xm?`<rect x="${f(X(TAIL.x0/2))}" y="${T}" """,
"""  +`<defs>${gzGrad(gid+'x',stX,0,xm,0)}${gzGrad(gid+'y',stY,y0,y1,1)}</defs>`
  +`<rect x="${L}" y="${100-B+.6}" width="${100-L-Rr}" height="${B-.6}" fill="url(#${gid}x)"/>`
  +`<rect x="0" y="${T}" width="${L-.6}" height="${100-B-T}" fill="url(#${gid}y)"/>`
  +(TAIL.x0/2<xm?`<rect x="${f(X(TAIL.x0/2))}" y="${T}" """)
e.rep("""  +`<span class="rv${hot?' hot':''}" style="left:${f(Math.min(58,Math.max(L+2,px-12)))}%;bottom:6%">σ ${sv}</span>`
  +`<span class="rv" style="left:${L+2}%;top:${f(Math.min(62,Math.max(T+1,py-12)))}%">μ ${mv}</span>`;""",
"""  +`<i class="gzc" style="left:${f(px)}%;bottom:0"></i><i class="gzc v" style="left:0;top:${f(py)}%"></i>`
  +`<span class="rv" style="left:${f(Math.min(44,Math.max(L+2,px-14)))}%;bottom:7%;color:${cX}">risque ${sv}</span>`
  +`<span class="rv" style="left:${L+2}%;top:${f(Math.min(62,Math.max(T+1,py-12)))}%;color:${cY}">rentabilité ${mv}</span>`;""")
e.rep("function colExp(){","riskMap.n=0;\nfunction colExp(){")
e.rep(".rmap .rv.hot{color:#E5675C}",
 ".rmap .rv.hot{color:#E5675C}\n.rmap .gzc{position:absolute;width:0;height:0;margin-left:-3.5px;border:3.5px solid transparent;border-bottom:5px solid #F3EEE4;border-top:0}\n.rmap .gzc.v{margin:-3.5px 0 0;border:3.5px solid transparent;border-right:0;border-left:5px solid #F3EEE4}")
e.done("lot 73")
