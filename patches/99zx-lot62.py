# -*- coding: utf-8 -*-
"""Lot 62 — panneau du haut : nuage risque / profit avec les concurrents (choix B d'Antoine).

La tuile Risque devient un mini-graphique : risque (abscisse, % annualisé) contre profit
(ordonnée, % du trimestre). Bande du mandat en fond, cible en pointillé, zéro de profit en
pointillé, les trois concurrents (initiale) à leur couple estimé, le book de début de trimestre
en fantôme relié au book courant (point doré, rouge au-dessus de la bande).

Profit estimé d'un concurrent, même convention que profitBook : collatéral au taux sans risque
+ espérance de rivalE (formule fermée, |f| moyen 0,8, max de quatre |f| ≈ 1,6) × vol/2 × 0,35
− 0,8 % de frais − ½ vol²/4. Risque : sa vol annuelle.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
e.rep("function colExp(){","""function rivPt(rv){
 const s=rv.skill,K4=4;let E;
 if(rv.style==='syst')E=0.9*(2*s-1)*K4*0.8+0.8;
 else if(rv.style==='flux'){const p=Math.min(1,0.5+0.5*Math.max(0,(s-0.5)*1.8));E=1.1*(2*p-1)*K4*0.8}
 else E=(2*s-1)*1.6*1.8;
 return {x:rv.vol,y:S.rate/4+(rv.vol/2)*0.35*E-0.008-0.5*rv.vol*rv.vol/4,l:(rv.nm||'?').replace(/^(Le |La |L')/,'')[0]};
}
function riskMap(sp){
 const W=140,H=52,x0=5,x1=W-4,y0=H-4,y1=5;
 const k0=S.k0||S.k,sp0=riskShown(weights(k0)).total,pr=profitBook(S.k),pr0=profitBook(k0);
 const R=(S.rivals||[]).map(rivPt),bd=bandNow();
 const xs=[sp,sp0,S.tgt*(1+bd),...R.map(r=>r.x)],ys=[pr,pr0,0,...R.map(r=>r.y)];
 const xm=Math.max(0.3,...xs)*1.08,ya=Math.min(-0.005,...ys),yb=Math.max(0.01,...ys),yp=(yb-ya)*0.12;
 const X=v=>x0+(x1-x0)*Math.max(0,v)/xm,Y=v=>y0-(y0-y1)*(v-(ya-yp))/((yb+yp)-(ya-yp));
 const hi=sp>S.tgt*(1+bd)+1e-9,col=hi?'#D2463C':'var(--gold)';
 let g=`<rect x="${X(S.tgt*(1-bd)).toFixed(1)}" y="${y1-3}" width="${(X(S.tgt*(1+bd))-X(S.tgt*(1-bd))).toFixed(1)}" height="${y0-y1+6}" fill="var(--long)" opacity=".13"/>`
  +`<line x1="${X(S.tgt).toFixed(1)}" x2="${X(S.tgt).toFixed(1)}" y1="${y1-3}" y2="${y0+3}" stroke="var(--long)" stroke-width=".8" stroke-dasharray="2 2" opacity=".7"/>`
  +`<line x1="${x0}" x2="${x1}" y1="${Y(0).toFixed(1)}" y2="${Y(0).toFixed(1)}" stroke="var(--dimmer)" stroke-width=".6" stroke-dasharray="2 2"/>`;
 R.forEach(r=>{g+=`<circle cx="${X(r.x).toFixed(1)}" cy="${Y(r.y).toFixed(1)}" r="2.1" fill="var(--dim)"/><text x="${(X(r.x)+3).toFixed(1)}" y="${(Y(r.y)+2.5).toFixed(1)}" font-size="7" fill="var(--dim)" font-family="var(--mono)">${r.l}</text>`});
 if(Math.abs(sp-sp0)>1e-4||Math.abs(pr-pr0)>1e-6)g+=`<circle cx="${X(sp0).toFixed(1)}" cy="${Y(pr0).toFixed(1)}" r="2.6" fill="none" stroke="var(--dimmer)" stroke-width=".9"/><line x1="${X(sp0).toFixed(1)}" y1="${Y(pr0).toFixed(1)}" x2="${X(sp).toFixed(1)}" y2="${Y(pr).toFixed(1)}" stroke="var(--dimmer)" stroke-width=".7"/>`;
 g+=`<circle cx="${X(sp).toFixed(1)}" cy="${Y(pr).toFixed(1)}" r="3.4" fill="${col}" stroke="var(--bg,#0b1020)" stroke-width=".8"/>`;
 g+=`<text x="${x1}" y="${y0+3.5}" font-size="6.5" text-anchor="end" fill="var(--dimmer)" font-family="var(--mono)">risque →</text><text x="${x0}" y="${y1+2}" font-size="6.5" fill="var(--dimmer)" font-family="var(--mono)">↑ profit</text>`;
 return `<span class="rmh"><b class="${hi?'neg-g':''}">${dec(sp*100,1)} %</b>${pc2(pr)}</span><svg class="rmap" viewBox="0 0 ${W} ${H}" preserveAspectRatio="none">${g}</svg>`;
}
function colExp(){""")
e.rep(""".rgrid{display:grid;""",""".fg.rmt{padding:3px 5px 2px;align-items:stretch}
.rmh{display:flex;justify-content:space-between;gap:4px;font-family:var(--mono);font-size:9.5px;color:var(--dimmer);white-space:nowrap}
.rmh i{font-style:normal}.rmh b{font-size:11px}.rmh b[class=""]{color:var(--txt)}
.rmap{display:block;width:100%;height:46px;margin-top:1px}
.rgrid{display:grid;""")
old=e.s[e.s.index('   <button class="fg" data-gauge="risk" style="flex:2.2">'):]
old=old[:old.index('</button>')+len('</button>')]
e.rep(old,'''   <button class="fg rmt" data-gauge="risk" style="flex:2.8">${riskMap(sp)}</button>''')
e.done("lot 62 — nuage risque / profit avec les concurrents")
