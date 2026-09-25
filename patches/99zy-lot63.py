# -*- coding: utf-8 -*-
"""Lot 63 — pas de capital de départ, collatéral dans le profit en direct, lignes de marché
(+1 / −1 en clair, expositions en toutes lettres, indicateurs au-dessus), nuage risque/profit
relu, ruban de performance resserré et trait du joueur à sa couleur, pop-up du carton rouge,
confiance avant / après dans les dépêches."""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
# ── pas de capital : trésorerie = gains nets, à tout instant ──
e.rep("mgrCap0:0.005*Z.nav,","mgrCap0:0,")
e.rep("function mgrCash(){return (S.mgrCap0||0)+mgrNet()}","function mgrCash(){return mgrNet()}   /* lot 63 : pas de capital de départ, trésorerie = gains nets */")
e.rep("""     ['Capital de départ de la société',`<span class="dim-g">+${mm(S.mgrCap0||0)}</span>`],\n""","")
e.rep("""Votre société a démarré avec <em>${mm(S.mgrCap0||0)}</em> en caisse, soit un trimestre de commission de gestion. Tout ce que vous engagez""",
      """Votre société n'a pas de capital : sa trésorerie, ce sont vos gains nets. Tout ce que vous engagez""")
e.rep("quand la caisse se limite au capital de départ et à la première commission,","quand la caisse se limite à la première commission de gestion,")
# ── collatéral : le profit du panneau suit le choix sans attendre ──
e.rep("el.querySelectorAll('.coll').forEach(b=>b.onclick=()=>{S.col=+b.dataset.c;drawColl();","el.querySelectorAll('.coll').forEach(b=>b.onclick=()=>{S.col=+b.dataset.c;drawColl();refreshStatus();")
# ── ligne de marché ──
e.rep(""" const ex=x.b.map((b,k)=>{const a=Math.abs(b),hot='';
   if(a<0.15)return `<b style="color:var(--dimmer)${hot}">${FACT[k].id}0</b>`;
   const n=a>=0.55?3:a>=0.32?2:1;return `<b style="color:${b>0?'var(--long)':'var(--short)'}${hot}">${FACT[k].id}${(b>0?'+':'−').repeat(n)}</b>`}).join(' ');""",
""" const FN=['Croissance','Inflation','Dollar','Appétit'];   /* lot 63 : en toutes lettres */
 const ex=x.b.map((b,k)=>{const a=Math.abs(b);
   if(a<0.15)return `<span style="color:var(--dimmer)">${FN[k]} 0</span>`;
   const n=a>=0.55?3:a>=0.32?2:1;return `<span>${FN[k]} <b style="color:${b>0?'var(--long)':'var(--short)'}">${(b>0?'+':'−').repeat(n)}</b></span>`}).join(' · ');""")
old=e.s[e.s.index("  gl=`<div class=\"rgrid\"><span>Ordre</span>"):]
old=old[:old.index("</div></div>`}")+len("</div></div>`}")]
e.rep(old,"""  const pM=pc2(profitBook(km)-profitBook(S.k)),pct1=v=>`<b class="${v>0.05?'neg-g':v<-0.05?'pos-g':'dim-g'}">${v>=0?'+':'−'}${dec(Math.abs(v),1)} %</b>`;
  gl=`<div class="rgrid2"><div><span class="k">Ordre</span> ${od}<span class="k" style="margin-left:10px">coût</span> <b>${mm(t.cost||0)}</b></div>
   <div><span class="k">+1</span> profit ${ex1} · risque ${pct1(rP)}</div><div><span class="k">−1</span> profit ${pM} · risque ${pct1(rM)}</div></div>`}""")
e.rep(" el.innerHTML=`<span class=\"fxe\">${ex}</span>${gl}`;"," el.innerHTML=`<div class=\"fxe2\">${ex}</div>${gl}`;")
e.rep(".rgrid{display:grid;",""".fxe2{font-size:10.5px;color:var(--dim);width:100%;white-space:normal;line-height:1.35}
.rgrid2{width:100%;font-family:var(--mono);font-size:11px;color:var(--dim);margin-top:4px;display:flex;flex-direction:column;gap:1px}
.rgrid2 .k{color:var(--dimmer);font-size:10px;display:inline-block;min-width:20px}
.rgrid{display:grid;""")
# indicateurs techniques au-dessus de l'ordre et du profit
e.rep("""     <div class="rowinfo" id="ri${i}"></div>

     <div class="tcv"><button data-mkt="${i}" class="tcvb">${(()=>{const m=STYLESIG[S.prof]||'t';
       return ['t','c','v'].map(z=>`<span class="${z===m?'mine':'oth'}">${tcvChip(SIGNM[z],S.tcvEst[z][i])}</span>`).join('')})()}${(S.prof==='fonda'&&S.cat&&S.cat.includes(i))?'<i class="cat" title="Catalyseur : l&#39;écart de valeur se referme ce trimestre">⚡</i>':''}<span class="more">détails ›</span></button></div></div>`;""",
"""     <div class="tcv"><button data-mkt="${i}" class="tcvb">${(()=>{const m=STYLESIG[S.prof]||'t';
       return ['t','c','v'].map(z=>`<span class="${z===m?'mine':'oth'}">${tcvChip(SIGNM[z],S.tcvEst[z][i])}</span>`).join('')})()}${(S.prof==='fonda'&&S.cat&&S.cat.includes(i))?'<i class="cat" title="Catalyseur : l&#39;écart de valeur se referme ce trimestre">⚡</i>':''}<span class="more">détails ›</span></button></div>
     <div class="rowinfo" id="ri${i}"></div></div>`;""")
# ── nuage : chiffres sur les axes, en blanc ; pas de point initial ; plus grand ──
old=e.s[e.s.index("function riskMap(sp){"):]
old=old[:old.index("\nfunction colExp(){")]
e.rep(old,"""function riskMap(sp){
 const W=150,H=66,x0=3,x1=W-3,yb=H-2,yt=3;   /* axe des abscisses tout en bas du cadre */
 const pr=profitBook(S.k),R=(S.rivals||[]).map(rivPt),bd=bandNow();
 const xs=[sp,S.tgt*(1+bd),S.tgt*(1-bd),...R.map(r=>r.x)],ys=[pr,0,...R.map(r=>r.y)];
 const xa=Math.min(...xs)*0.85,xm=Math.max(...xs)*1.08;
 const ya=Math.min(...ys),yz=Math.max(...ys),yp=(yz-ya)*0.18+0.002;
 const X=v=>x0+(x1-x0)*(v-xa)/(xm-xa),Y=v=>yb-(yb-yt)*(v-(ya-yp))/((yz+yp)-(ya-yp));
 const hi=sp>S.tgt*(1+bd)+1e-9,col=hi?'#D2463C':'var(--gold)',f=v=>v.toFixed(1);
 let g=`<rect x="${f(X(S.tgt*(1-bd)))}" y="${yt}" width="${f(X(S.tgt*(1+bd))-X(S.tgt*(1-bd)))}" height="${yb-yt}" fill="var(--long)" opacity=".13"/>`
  +`<line x1="${f(X(S.tgt))}" x2="${f(X(S.tgt))}" y1="${yt}" y2="${yb}" stroke="var(--long)" stroke-width=".8" stroke-dasharray="2 2" opacity=".7"/>`
  +`<line x1="${x0}" x2="${x1}" y1="${f(Y(0))}" y2="${f(Y(0))}" stroke="var(--dimmer)" stroke-width=".6" stroke-dasharray="2 2"/>`
  +`<line x1="${x0}" x2="${x1}" y1="${yb}" y2="${yb}" stroke="var(--dimmer)" stroke-width=".8"/><line x1="${x0}" x2="${x0}" y1="${yt}" y2="${yb}" stroke="var(--dimmer)" stroke-width=".8"/>`
  +`<text x="${x1}" y="${yb-2}" font-size="6.5" text-anchor="end" fill="var(--dimmer)" font-family="var(--mono)">risque</text>`
  +`<text x="${x0+2}" y="${yt+6}" font-size="6.5" fill="var(--dimmer)" font-family="var(--mono)">profit</text>`;
 R.forEach(r=>{g+=`<circle cx="${f(X(r.x))}" cy="${f(Y(r.y))}" r="2.1" fill="var(--dim)"/><text x="${f(X(r.x)+3)}" y="${f(Y(r.y)+2.5)}" font-size="7" fill="var(--dim)" font-family="var(--mono)">${r.l}</text>`});
 const px=X(sp),py=Y(pr);
 /* repères du joueur : tirets vers les axes, valeurs en blanc au bord de chaque axe */
 g+=`<line x1="${f(px)}" x2="${f(px)}" y1="${f(py)}" y2="${yb}" stroke="#F3EEE4" stroke-width=".5" stroke-dasharray="1.5 1.5" opacity=".6"/>`
  +`<line x1="${x0}" x2="${f(px)}" y1="${f(py)}" y2="${f(py)}" stroke="#F3EEE4" stroke-width=".5" stroke-dasharray="1.5 1.5" opacity=".6"/>`
  +`<text x="${f(Math.min(x1-16,Math.max(x0+14,px)))}" y="${yb-2}" font-size="7.5" text-anchor="middle" fill="#F3EEE4" font-family="var(--mono)" font-weight="600">${dec(sp*100,1)} %</text>`
  +`<text x="${x0+2}" y="${f(Math.min(yb-9,Math.max(yt+14,py-2)))}" font-size="7.5" fill="#F3EEE4" font-family="var(--mono)" font-weight="600">${pr>=0?'+':'−'}${dec(Math.abs(pr)*100,2)} %</text>`
  +`<circle cx="${f(px)}" cy="${f(py)}" r="3.6" fill="${col}" stroke="var(--bg,#0b1020)" stroke-width=".8"/>`;
 return `<svg class="rmap" viewBox="0 0 ${W} ${H}" preserveAspectRatio="none">${g}</svg>`;
}""")
e.rep(".rmap{display:block;width:100%;height:46px;margin-top:1px}",".rmap{display:block;width:100%;height:64px}")
# ── ruban : échelle resserrée sur les quatre fonds, trait du joueur à sa couleur ──
e.rep(""" let m=1e-6;p.forEach(v=>m=Math.max(m,Math.abs(v-100)));
 rv.forEach(r=>r.pts.forEach(v=>m=Math.max(m,Math.abs(v-100))));
 m*=1.18;
 const lo=100-m,hi=100+m;""","""  /* lot 63 : juste l'étendue des quatre fonds (base 100 comprise), une marge de 8 % */
 let a=100,b=100;p.forEach(v=>{a=Math.min(a,v);b=Math.max(b,v)});rv.forEach(r=>r.pts.forEach(v=>{a=Math.min(a,v);b=Math.max(b,v)}));
 const mg=Math.max(0.3,(b-a)*0.08),lo=a-mg,hi=b+mg;""")
e.rep("""  const c=s.up?TAPE_UP:TAPE_DN,pts=s.pts.map(q=>f(q[0])+','+f(q[1])).join(' ');""","""  const c=myCol(rv),pts=s.pts.map(q=>f(q[0])+','+f(q[1])).join(' ');""")
e.rep("function tapeSvg(p,from,opt){","""/* couleur du joueur : celle de son blason, sinon l'or, sinon l'ivoire — jamais celle d'un concurrent */
function myCol(rv){const used=(rv||[]).map((r,j)=>CRESTS[(r.crest!==undefined?r.crest:RIVCREST[j%4])%CRESTS.length].a.toLowerCase());
 const c0=CRESTS[((S&&S.crest)||0)%CRESTS.length].a;return [c0,'#E8C547','#F3EEE4'].find(c=>!used.includes(c.toLowerCase()))}
function tapeSvg(p,from,opt){""")
# ── carton rouge : pop-up rouge à la clôture ──
e.rep(" if(S.qCard)warn.push(",""" if(S.qCard&&S.qCard.c==='rouge'&&S.qCardPop!==S.q){S.qCardPop=S.q;const qc=S.qCard;setTimeout(()=>{
   openModal('Carton rouge',`<div class="redpop"><svg viewBox="0 0 18 24" width="54" height="72"><rect x="1.5" y="1.5" width="15" height="21" rx="2.5" fill="#D2463C"/></svg>
    <p><b>Le comité des risques vous sort le rouge.</b><br>${qc.why}.</p>
    <ul class="rules2"><li>Au prochain trimestre : <b>${qc.cn?qc.cn.nm:'contrainte'}</b> — ${qc.cn?qc.cn.t:''}.</li><li>5 % de l'encours retiré par les investisseurs.</li><li>Confiance −6.</li></ul></div>`);
   const mb=document.querySelector('#modal .mbox');if(mb)mb.classList.add('redbox')},30)}
 if(S.qCard)warn.push(""")
e.rep(".tile.cardt{",""".mbox.redbox{border:2px solid #D2463C;box-shadow:0 0 0 3px rgba(210,70,60,.25)}
.mbox.redbox .mhead h3{color:#E5675C}
.redpop{text-align:center}.redpop svg{display:block;margin:4px auto 10px}.redpop ul{text-align:left}
.tile.cardt{""")
# ── dépêches : confiance avant, confiance finale par issue ──
e.rep(""" const gcell=v=>{const r=Math.round(v);return `<span class="pn" style="color:${r>0?'var(--long)':r<0?'var(--short)':'var(--dim)'}">${r>0?'+':r<0?'−':''}${Math.abs(r)}</span>`};""",
""" const gcell=v=>{const r=Math.round(v),fin=Math.round(Math.max(0,Math.min(100,S.lp+v)));return `<span class="pn" style="color:${r>0?'var(--long)':r<0?'var(--short)':'var(--dim)'}">${fin}</span>`};""")
e.rep("""<span class="ph pn">Confiance</span>""","""<span class="ph pn">Confiance</span>""")
e.rep("""   ${plan.map((o,i)=>{const ban=""","""   <p class="note" style="margin:0 0 6px">Confiance avant votre décision : <b>${Math.round(S.lp)}</b>. Chaque issue donne la confiance à la fin de la dépêche.</p>
   ${plan.map((o,i)=>{const ban=""")
e.rep("""  ['Effets',gz(tg.lp,0,'always')]];""","""  ['Confiance',`${Math.round(S.lp-tg.lp)} → <b>${Math.round(S.lp)}</b> (${gz(tg.lp,0,'always')})`]];""")
e.done("lot 63")
