# -*- coding: utf-8 -*-
"""Lot 64 — minuteur selon la difficulté, sources regroupées, texte du budget dans le tutoriel,
nuage aux couleurs des fonds (et en grand au clic), trésorerie à une décimale, rubans sans
lignes droites, cartons rouges ciblés sur les lignes à risque."""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
def cut(a,b):
    i=e.s.index(a); j=e.s.index(b,i)+len(b); return e.s[i:j]
# ── minuteur : facile 45–60 s, moyen 25–35 s, difficile 15–25 s ──
e.rep(" const sec=15+Math.floor(Math.random()*16);let t=sec;   /* tirage uniforme 15–30 s */",
      " const TR={small:[45,60],mid:[25,35],mega:[15,25]}[(S&&S.size)||'mid']||[25,35],sec=TR[0]+Math.floor(Math.random()*(TR[1]-TR[0]+1));let t=sec;   /* lot 64 : selon la difficulté */")
# ── sources : mode d'emploi, lecture consolidée et matrice dans un seul volet ──
blk=cut('   <details style="margin-top:8px"><summary>Comment lire ces sources</summary>','</p>\n   </details>')
assert "Matrice d'exposition" in blk and blk.count('<details')==blk.count('</details>'), 'bloc sources'
e.rep(blk,'   <details style="margin-top:8px"><summary>Lire les sources · lecture consolidée · matrice</summary>\n'+blk.replace('style="margin-top:8px"><summary>Comment lire','style="margin-top:4px"><summary>Comment lire',1)+'\n   </details>')
# ── budget : le texte part dans le tutoriel de première partie ──
e.rep("""   <p class="note" style="margin-top:0">Payé de votre poche, pas par le fonds, dans la limite de votre trésorerie. 1 pb = <em>${(S.nav*100).toFixed(0)} k$</em>.</p>
   <div class="kv"><span>Trésorerie disponible ce trimestre</span><b id="btre">${mm(mgrCash()+(S.qOps||0))}</b></div>
   <div class="kv"><span>Reste pour les ordres du trimestre</span><b id="brest"></b></div>
""","")
nt=cut('   <p class="note" style="margin:4px 0 8px">⚠ La même trésorerie paie vos ordres de marché','</p>\n')
e.rep(nt,"")
e.rep(""" {id:1,t:"Les sources, et ce qu'elles valent",""",""" {id:1,t:"Le budget, et votre trésorerie",
  h:`<p>Le budget d'exploitation est payé <b>de votre poche</b>, pas par le fonds, dans la limite de votre <b>trésorerie</b> — la tuile dorée du haut. Votre société n'a pas de capital : sa trésorerie, ce sont vos gains nets. Un point de base d'encours vaut 10 k$ pour un fonds de 100 M$.</p>
  <p>⚠ La même trésorerie paie vos <b>ordres de marché</b> : ce que le budget consomme, le book ne peut plus le dépenser, et les cases trop chères se grisent. En début de partie, la caisse se limite à la première commission de gestion : gardez des budgets serrés, vous les relèverez quand les commissions de performance rentreront.</p>`},
 {id:2,t:"Les sources, et ce qu'elles valent",""")
e.rep(""" {id:2,t:"Facteurs et signaux : d'où vient la performance",""",""" {id:3,t:"Facteurs et signaux : d'où vient la performance",""")
e.rep("openModal(`Tutoriel · ${n+1} sur 3 — ${T.t}`","openModal(`Tutoriel · ${n+1} sur 4 — ${T.t}`")
e.rep("function screenBudget(){\n tuto(0);","function screenBudget(){\n tuto(0,1);")
e.rep("tuto(1,2);","tuto(2,3);")
e.rep("<b>Vos gains</b> est votre score : les commissions encaissées, moins ce que vous dépensez.","<b>Trésorerie</b>, c'est votre score : les commissions encaissées, moins ce que vous dépensez.")
# ── trésorerie : M$ à une décimale ──
e.rep("const score=x=>{","const treso=x=>{const a=Math.abs(x),sg=x<0?'−':'';if(a>=1)return sig3(x,'Md$');if(a>=0.001)return sg+(a*1000).toFixed(1).replace('.',',')+' M$';return sg+Math.round(a*1e6)+' k$'};\nconst score=x=>{")
e.rep("""<b id="gaintile" class="${mgrCash()>=0?'':'neg-g'}">${score(mgrCash())}</b>""","""<b id="gaintile" class="${mgrCash()>=0?'':'neg-g'}">${treso(mgrCash())}</b>""")
e.rep(" const v=mgrCash();e.textContent=score(v);"," const v=mgrCash();e.textContent=treso(v);")
# ── rubans : le bruit du pont suit l'ampleur du mouvement, plus de rampe droite ──
e.rep(" const r=prng32(seed),a=Math.log(Math.max(1e-9,v0)),b=Math.log(Math.max(1e-9,v1));",
      " const r=prng32(seed),a=Math.log(Math.max(1e-9,v0)),b=Math.log(Math.max(1e-9,v1));\n vol=Math.max(vol,Math.abs(b-a)*0.55/Math.sqrt(Math.max(1,m)));   /* lot 64 : un grand pas reste brownien */")
# ── nuage : couleurs des fonds, sans libellés d'axes, grand format au clic ──
old=cut("function riskMap(sp){","\n return `<svg class=\"rmap\" viewBox=\"0 0 ${W} ${H}\" preserveAspectRatio=\"none\">${g}</svg>`;\n}")
e.rep(old,"""function rivCol(j){const r=S.rivals[j];return CRESTS[((r&&r.crest!==undefined)?r.crest:RIVCREST[j%4])%CRESTS.length].a}
function riskMap(sp,big){
 const W=big?320:150,H=big?210:66,x0=big?30:3,x1=W-(big?8:3),yb=H-(big?18:2),yt=big?8:3,fs=big?11:9,ls=big?10:7;
 const pr=profitBook(S.k),R=(S.rivals||[]).map((rv,j)=>Object.assign(rivPt(rv),{c:rivCol(j),nm:rv.nm})),bd=bandNow();
 const xs=[sp,S.tgt*(1+bd),S.tgt*(1-bd),...R.map(r=>r.x)],ys=[pr,0,...R.map(r=>r.y)];
 const xa=Math.min(...xs)*0.85,xm=Math.max(...xs)*1.08,ya=Math.min(...ys),yz=Math.max(...ys),yp=(yz-ya)*0.18+0.002;
 const X=v=>x0+(x1-x0)*(v-xa)/(xm-xa),Y=v=>yb-(yb-yt)*(v-(ya-yp))/((yz+yp)-(ya-yp));
 const hi=sp>S.tgt*(1+bd)+1e-9,me=myCol(S.rivals||[]),f=v=>v.toFixed(1);
 let g=`<rect x="${f(X(S.tgt*(1-bd)))}" y="${yt}" width="${f(X(S.tgt*(1+bd))-X(S.tgt*(1-bd)))}" height="${yb-yt}" fill="var(--long)" opacity=".13"/>`
  +`<line x1="${f(X(S.tgt))}" x2="${f(X(S.tgt))}" y1="${yt}" y2="${yb}" stroke="var(--long)" stroke-width=".8" stroke-dasharray="2 2" opacity=".7"/>`
  +`<line x1="${x0}" x2="${x1}" y1="${f(Y(0))}" y2="${f(Y(0))}" stroke="var(--dimmer)" stroke-width=".6" stroke-dasharray="2 2"/>`
  +`<line x1="${x0}" x2="${x1}" y1="${yb}" y2="${yb}" stroke="var(--dimmer)" stroke-width=".8"/><line x1="${x0}" x2="${x0}" y1="${yt}" y2="${yb}" stroke="var(--dimmer)" stroke-width=".8"/>`;
 if(big){
  const t=(v,lab)=>`<text x="${f(X(v))}" y="${yb+12}" font-size="9" text-anchor="middle" fill="var(--dim)" font-family="var(--mono)">${lab}</text>`;
  g+=t(S.tgt*(1-bd),dec(S.tgt*(1-bd)*100,0)+' %')+t(S.tgt,'cible')+t(S.tgt*(1+bd),dec(S.tgt*(1+bd)*100,0)+' %')
   +`<text x="${x0-3}" y="${f(Y(0)+3)}" font-size="9" text-anchor="end" fill="var(--dim)" font-family="var(--mono)">0</text>`
   +`<text x="${f(X(S.tgt*(1-bd))+3)}" y="${yt+10}" font-size="9" fill="var(--long)" font-family="var(--mono)" opacity=".8">bande du mandat</text>`;
 }
 R.forEach(r=>{g+=`<circle cx="${f(X(r.x))}" cy="${f(Y(r.y))}" r="${big?4:2.4}" fill="${r.c}"/><text x="${f(X(r.x)+(big?6:3.2))}" y="${f(Y(r.y)+(big?3.5:2.5))}" font-size="${ls}" fill="${r.c}" font-family="var(--mono)">${big?`${r.nm} · ${dec(r.x*100,0)} % · ${r.y>=0?'+':'−'}${dec(Math.abs(r.y)*100,1)} %`:r.l}</text>`});
 const px=X(sp),py=Y(pr);
 g+=`<line x1="${f(px)}" x2="${f(px)}" y1="${f(py)}" y2="${yb}" stroke="#F3EEE4" stroke-width=".5" stroke-dasharray="1.5 1.5" opacity=".6"/>`
  +`<line x1="${x0}" x2="${f(px)}" y1="${f(py)}" y2="${f(py)}" stroke="#F3EEE4" stroke-width=".5" stroke-dasharray="1.5 1.5" opacity=".6"/>`
  +`<text x="${f(Math.min(x1-20,Math.max(x0+20,px)))}" y="${yb-3}" font-size="${fs}" text-anchor="middle" fill="${hi?'#E5675C':'#F3EEE4'}" font-family="var(--mono)" font-weight="700">${dec(sp*100,1)} %</text>`
  +`<text x="${x0+2}" y="${f(Math.min(yb-fs-3,Math.max(yt+fs,py-3)))}" font-size="${fs}" fill="#F3EEE4" font-family="var(--mono)" font-weight="700">${pr>=0?'+':'−'}${dec(Math.abs(pr)*100,1)} %</text>`
  +`<circle cx="${f(px)}" cy="${f(py)}" r="${big?5.5:3.8}" fill="${me}" stroke="${hi?'#D2463C':'var(--bg,#0b1020)'}" stroke-width="${hi?1.6:.8}"/>`
  +(big?`<text x="${f(px+8)}" y="${f(py-6)}" font-size="10" fill="${me}" font-family="var(--mono)" font-weight="700">Vous</text>`:'');
 return big?`<p class="note" style="margin:0 0 4px">Risque annualisé du book (bruit d'estimation compris) en abscisse, profit attendu du trimestre en ordonnée — collatéral, impact et drain de volatilité compris. Les concurrents sont placés à leur couple estimé.</p><svg viewBox="0 0 ${W} ${H}" style="width:100%;height:auto;display:block;margin-bottom:10px">${g}</svg>`
  :`<svg class="rmap" viewBox="0 0 ${W} ${H}" preserveAspectRatio="none">${g}</svg>`;
}""")
e.rep(" else if(id==='risk'){\n  const vd=varDecomp(w),rc=riskContrib(w);"," else if(id==='risk'){\n  window.__pre=riskMap(riskShown(w).total,1);   /* lot 64 : le nuage en grand, puis la page */\n  const vd=varDecomp(w),rc=riskContrib(w);")
e.rep("""<div class="mbody">${html}</div>""","""<div class="mbody">${window.__pre||''}${html}</div>""")
e.rep(" m.style.display='block';"," m.style.display='block';window.__pre='';",1)
# ── carton rouge : fermer les lignes qui ont porté le risque ──
e.rep(""" if(c.id==='shut'){const rc=riskContrib(w);
  let o=INSTR.map((x,i)=>({i,v:Math.abs(rc[i]||0)})).filter(z=>mktOpen(z.i)).sort((a,b)=>b.v-a.v||a.i-b.i);
  if(!(o[0]&&o[0].v>1e-9))o=o.map(z=>({i:z.i,v:u()})).sort((a,b)=>b.v-a.v);
  c.syms=o.slice(0,3).map(z=>INSTR[z.i].sym);c.t=`${c.syms.join(', ')} fermés au fonds`}
 if(c.id==='class'){const cl=[...new Set(INSTR.filter((x,i)=>mktOpen(i)).map(x=>x.grp))];
  const g=cl[Math.floor(u()*cl.length)];""",""" /* lot 64 : les marchés fermés sont ceux où le risque a été pris — contribution positive au
    risque du book de fin de trimestre, puis taille de position ; le hasard seulement à book vide */
 const rcw=riskContrib(w),kk=S.kVal||S.k;
 if(c.id==='shut'){
  let o=INSTR.map((x,i)=>({i,v:rcw[i]||0,k:Math.abs(kk[i]||0)})).filter(z=>mktOpen(z.i)&&(z.v>1e-9||z.k>0)).sort((a,b)=>b.v-a.v||b.k-a.k||a.i-b.i);
  if(!o.length)o=INSTR.map((x,i)=>({i,v:u()})).filter(z=>mktOpen(z.i)).sort((a,b)=>b.v-a.v);
  c.syms=o.slice(0,3).map(z=>INSTR[z.i].sym);c.t=`${c.syms.join(', ')} fermés au fonds : les lignes qui portaient le plus de risque`}
 if(c.id==='class'){const cl=[...new Set(INSTR.filter((x,i)=>mktOpen(i)).map(x=>x.grp))];
  const cr=g=>INSTR.reduce((a,x,i)=>a+(x.grp===g?Math.max(0,rcw[i]||0):0),0);
  const g=cl.slice().sort((a,b)=>cr(b)-cr(a))[0]&&cr(cl.slice().sort((a,b)=>cr(b)-cr(a))[0])>1e-9?cl.slice().sort((a,b)=>cr(b)-cr(a))[0]:cl[Math.floor(u()*cl.length)];""")
e.done("lot 64")
