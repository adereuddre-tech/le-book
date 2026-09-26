# -*- coding: utf-8 -*-
"""Lot 67 — demandes d'Antoine : mi-parcours juste, nuage μ/σ quadrillé, trésorerie à 3 chiffres,
lignes de marché plus courtes, confiance/cartons sans double peine, hauts faits et cartes relus,
concurrents sans saut à la clôture, bot qui choisit son risque, équilibrage."""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()

# ───────── A1. concurrents : chemin pur, la clôture tombe exactement sur le dernier point du ruban ─────────
# Constat : rivRet (ruban) omettait le bruit propre (σ ≈ v/2·0,75, soit ~15 % par trimestre à 40 % de risque)
# et l'accident, et tirait son adresse sur un autre flux que rivalReturns : la clôture sautait de tout cela.
e.rep("""function rivalReturns(){
 return S.rivals.map(rv=>{
   const e=rivalE(rv,rng);
   const v=rivV(rv),j=S.rivals.indexOf(rv),tl=rivTail(rv,j,v,S.q);rv.tailHit=tl>0?tl:0;
   return (v/2)*(RIVK*e+(RIVNOISE[rv.style]||0.78)*gauss())-0.008-rivDrag(v)-tl;
 });
}""","""function rivalReturns(){   /* lot 67 : exactement rivRet(j,1) — plus aucun tirage de rng */
 return S.rivals.map((rv,j)=>{const tl=rivTail(rv,j,rivV(rv),S.q);rv.tailHit=tl>0?tl:0;return rivRet(j,1,S.q)});
}""")
e.rep("""function rivRet(j,t,q){
 const r=S.rivals&&S.rivals[j];if(!r||!S.f||!S.f.length)return 0;
 const e=rivalE(r,prng32(hash32('rivk'+j+'_'+q,S.seed)));
 const v=rivV(r);return t*((v/2)*(RIVK*e)-0.008-rivDrag(v));
}""","""function rivNz(j,q){const u=prng32(hash32('rivn'+j+'_'+q,S.seed)),a=Math.max(1e-9,u()),b=u();return Math.sqrt(-2*Math.log(a))*Math.cos(2*Math.PI*b)}
function rivRet(j,t,q){
 const r=S.rivals&&S.rivals[j];if(!r||!S.f||!S.f.length)return 0;
 const e=rivalE(r,prng32(hash32('rivk'+j+'_'+q,S.seed)));
 const v=rivV(r),tl=rivTail(r,j,v,q),tt=0.2+0.7*prng32(hash32('rtt'+j+'_'+q,S.seed))();
 return t*((v/2)*(RIVK*e+(RIVNOISE[r.style]||0.78)*rivNz(j,q))-0.008-rivDrag(v))-(t>=tt?tl:0);
}""")

# ───────── A2. confiance et cartons : une faute, une sanction ─────────
# Un trimestre à −12 % payait : performance (−24), trimestre négatif (−3), repli, écart à la médiane, comité
# « perte > 10 % » (−5 en confiance), puis le carton rouge (−6) — et les notes de clôture du comité pouvaient
# encore déclencher un jaune « griefs ». La perte > 10 % n'est plus notée par le comité (le carton s'en charge),
# et les griefs ne comptent que ce qui s'est passé pendant le trimestre, pas la clôture.
e.rep(" if(qTotal<-0.10)rcD.push(['Perte trimestrielle au-delà de 10 %',-10]);\n","")
e.rep("  if(S.gSnap&&S.rc-S.gSnap.rc<=-25)why.push('griefs accumulés dans le trimestre');","  if(S.gSnap&&clo0.rc0-S.gSnap.rc<=-25)why.push('griefs accumulés dans le trimestre');")
e.rep("else if(S.rcD.some(x=>/au-delà de 10/.test(x[0])))","else if(q<-0.10)")
# pop-up confiance : dire ce que valent les cartons
e.rep("Ce que le comité des risques reproche à votre book s'y ajoute pour moitié. Sous <em>20</em>, des rachats partent à chaque clôture.",
 "Ce que le comité des risques reproche à votre book s'y ajoute pour moitié, et chaque carton coûte à la clôture (jaune −2, rouge −6). Sous <em>20</em>, des rachats partent à chaque clôture.")

# ───────── A3. hauts faits et cartes ─────────
e.rep('d:"Atteindre 90 de confiance investisseurs."','d:"Atteindre 90 de confiance."')
e.rep('d:"Terminer un mandat avec un encours au moins doublé.",tf:f=>f.idx>=2','d:"Terminer un mandat avec une performance nette au moins de +100 %.",tf:f=>f.idx>=2')
e.rep('d:"Terminer un mandat avec un encours au moins triplé.",tf:f=>f.idx>=3','d:"Terminer un mandat avec une performance nette au moins de +200 %.",tf:f=>f.idx>=3')
e.rep(""" {id:'nomargin',""",""" {id:'tail',  tier:2,ic:'🌪️',nm:"Dompter le levier",d:"Finir un trimestre positif malgré un accident de levier.",tq:c=>c.q>0&&c.tail},
 {id:'nomargin',""")
e.rep("  vol:S.realVol,tgt:S.tgt,sp:pvol(w),","  vol:S.realVol,tgt:S.tgt,sp:pvol(w),tail:(S.tails||[]).some(x=>x.q===S.q),")
e.rep("k:'INSTITUTIONNEL · QUATRE TRIMESTRES DANS LA BANDE'","k:'INSTITUTIONNEL · QUATRE TRIMESTRES SANS CARTON'")
e.rep("g:'comité +3 · un ajustement gratuit au prochain trimestre'","g:'confiance +2 · un ajustement gratuit au prochain trimestre'")
e.rep("g:'investisseurs +6 · comité +2'","g:'confiance +7'")
e.rep("· investisseurs +8 · comité +4`","· confiance +10`")
e.rep("g:'investisseurs +3 · on en parlera au dîner'","g:'confiance +3 · on en parlera au dîner'")
e.rep("(+3 %) · investisseurs +5`","(+3 %) · confiance +5`")

# ───────── A4. mi-parcours : le titre dit le trimestre, pas les seules positions ─────────
e.rep("""resultCard(`TRIMESTRE ${S.q+1} · MI-PARCOURS`,p>=0?"Le book est en gains latents":"Le book est en pertes latentes",
  [`Le fonds est à <em class="${cls(tot)}">${sgn(tot/100,1)}</em> depuis le lancement. Sur ce total, <em class="${cls(dir)}">${dir>=0?'+':'−'}${dec(Math.abs(dir),1)} point${Math.abs(dir)>=2?'s':''}</em> viennent des positions directionnelles que vous portez depuis le début du trimestre, soit <em class="${cls(p)}">${sgn(p,1)} sur le trimestre · ${mn(p*navB)}</em>.""",
"""const qtd=navNow()/Math.max(1e-9,S.navQ0)-1,oth=((S.qEvM||0)+(S.qIncM||0))/Math.max(1e-9,S.navQ0);
 const ttl=qtd>=0?(p>=0?"Le trimestre est en gains":"Le fonds gagne grâce aux dépêches, le book est en pertes latentes")
  :(p<0?"Le trimestre est en pertes":"Le book est en gains latents, mais les dépêches ont coûté plus");
 resultCard(`TRIMESTRE ${S.q+1} · MI-PARCOURS`,ttl,
  [`Sur le trimestre, le fonds est à <em class="${cls(qtd)}">${sgn(qtd,1)}</em> : <em class="${cls(p)}">${sgn(p,1)}</em> de positions portées (latent, ${mn(p*navB)}) et <em class="${cls(oth)}">${sgn(oth,1)}</em> de dépêches, desk et incidents. Depuis le lancement : <em class="${cls(tot)}">${sgn(tot/100,1)}</em>.""")
# ───────── A5. ruban : le dernier pas du trimestre a la même densité que les autres ─────────
# Le reste du trimestre après la dernière dépêche (souvent 20 à 40 % du chemin) et la commission de
# performance tenaient en 18 points contre 48 par segment : un pas 2,7 fois plus raide, lu comme un saut.
e.rep("  bridgePts(last,tgt,18,hash32('settle'+S.q,S.seed),tapeVol(18,0.04)).forEach(z=>S.tape.pts.push(z));",
      "  const dtl=Math.max(0.04,1-((S.tape.ts&&S.tape.ts.length)?S.tape.ts[S.tape.ts.length-1]:0));\n  bridgePts(last,tgt,TAPEM,hash32('settle'+S.q,S.seed),tapeVol(TAPEM,dtl)).forEach(z=>S.tape.pts.push(z));")
e.rep("   bridgePts(last,nv,18,hash32('rivs'+j+'_'+tq,S.seed),tapeVol(18,0.04,rivV(r))).forEach(z=>pts.push(z))}",
      "   bridgePts(last,nv,TAPEM,hash32('rivs'+j+'_'+tq,S.seed),tapeVol(TAPEM,Math.max(0.04,1-(ts.length?ts[ts.length-1]:0)),rivV(r))).forEach(z=>pts.push(z))}")
e.done("lot 67 — mécanique")

# ───────── B1. nuage μ / σ : annualisé, quadrillé tous les 10 %, abscisses en bas, libellés dans le cadre ─────────
i=e.s.index("function riskMap(sp,big){");assert e.s.count("function riskMap(sp,big){")==1;j=e.s.index("function colExp(){",i)
e.s=e.s[:i]+r"""/* lot 67 : μ (rendement attendu annualisé = 4 × celui du trimestre) contre σ (risque annualisé). Axe des
   abscisses toujours en bas du cadre ; traits très fins tous les 10 % sur les deux axes ; valeurs du fonds
   dans le cadre ; zone d'accidents de levier teintée. */
function riskMap(sp,big){
 const pr=profitBook(S.k)*4,R=(S.rivals||[]).map((rv,j)=>{const p=rivPt(rv);p.y*=4;return Object.assign(p,{c:rivCol(j),nm:rv.nm})});
 const xm=Math.max(0.10,sp,...R.map(r=>r.x))*1.10;
 const ys=[pr,...R.map(r=>r.y)],ya=Math.min(0,...ys),yz=Math.max(0,...ys),ypad=Math.max(0.01,(yz-ya)*0.14);
 const y0=ya<0?ya-ypad:0,y1=yz+ypad;
 const hot=tailP(sp)>0,me=myCol(S.rivals||[]),f=v=>v.toFixed(1);
 const sv=`${dec(sp*100,1)} %`,mv=`${pr>=0?'+':'−'}${dec(Math.abs(pr)*100,1)} %`;
 const lv=(a,b)=>{const o=[];for(let v=Math.ceil(a/0.1-1e-9)*0.1;v<=b+1e-9;v+=0.1)o.push(+v.toFixed(2));return o};
 const nm=(S.fundName||'Vous').split(' ')[0];
 if(big){
  const W=320,H=210,x0=40,x1=W-8,yb=H-16,yt=8;
  const X=v=>x0+(x1-x0)*v/xm,Y=v=>yb-(yb-yt)*(v-y0)/(y1-y0);
  let g='';
  if(TAIL.x0<xm)g+=`<rect x="${f(X(TAIL.x0))}" y="${yt}" width="${f(x1-X(TAIL.x0))}" height="${f(yb-yt)}" fill="#D2463C" opacity=".10"/>`
   +`<text x="${f(X(TAIL.x0)+3)}" y="${yt+10}" font-size="9" fill="#E5675C" font-family="var(--mono)" opacity=".85">accidents de levier</text>`;
  lv(0.1,xm).forEach(v=>{g+=`<line x1="${f(X(v))}" x2="${f(X(v))}" y1="${yt}" y2="${yb}" stroke="var(--dimmer)" stroke-width=".3" opacity=".6"/><text x="${f(X(v))}" y="${yb+11}" font-size="8" text-anchor="middle" fill="var(--dimmer)" font-family="var(--mono)">${Math.round(v*100)}</text>`});
  lv(y0,y1).forEach(v=>{g+=`<line x1="${x0}" x2="${x1}" y1="${f(Y(v))}" y2="${f(Y(v))}" stroke="var(--dimmer)" stroke-width="${Math.abs(v)<1e-9?.7:.3}" opacity="${Math.abs(v)<1e-9?.9:.6}"/><text x="${x0-3}" y="${f(Y(v)+3)}" font-size="8" text-anchor="end" fill="var(--dimmer)" font-family="var(--mono)">${Math.round(v*100)}</text>`});
  g+=`<line x1="${x0}" x2="${x1}" y1="${yb}" y2="${yb}" stroke="var(--dimmer)" stroke-width=".8"/><line x1="${x0}" x2="${x0}" y1="${yt}" y2="${yb}" stroke="var(--dimmer)" stroke-width=".8"/>`
   +`<text x="${x1-2}" y="${yb-4}" font-size="11" text-anchor="end" fill="var(--dim)" font-family="var(--mono)">σ</text>`
   +`<text x="${x0+4}" y="${yt+10}" font-size="11" fill="var(--dim)" font-family="var(--mono)">μ</text>`;
  R.forEach(r=>{g+=`<circle cx="${f(X(r.x))}" cy="${f(Y(r.y))}" r="4" fill="${r.c}"/><text x="${f(X(r.x)+6)}" y="${f(Y(r.y)+3.5)}" font-size="9.5" fill="${r.c}" font-family="var(--mono)">${r.nm.split(' ')[0]} · σ ${dec(r.x*100,0)} · μ ${r.y>=0?'+':'−'}${dec(Math.abs(r.y)*100,0)}</text>`});
  const px=X(sp),py=Y(pr);
  /* σ et μ du fonds sur les axes, en blanc ; le nom à droite du point, jamais sur la valeur de μ */
  g+=`<line x1="${f(px)}" x2="${f(px)}" y1="${yb-4}" y2="${yb}" stroke="#F3EEE4" stroke-width="1"/><line x1="${x0}" x2="${x0+4}" y1="${f(py)}" y2="${f(py)}" stroke="#F3EEE4" stroke-width="1"/>`
   +`<text x="${f(Math.min(x1-40,Math.max(x0+22,px)))}" y="${yb-7}" font-size="10" text-anchor="middle" fill="${hot?'#E5675C':'#F3EEE4'}" font-family="var(--mono)" font-weight="700">σ ${sv}</text>`
   +`<text x="${x0+6}" y="${f(Math.min(yb-18,Math.max(yt+22,py+3.5)))}" font-size="10" fill="#F3EEE4" font-family="var(--mono)" font-weight="700">μ ${mv}</text>`
   +`<circle cx="${f(px)}" cy="${f(py)}" r="5.5" fill="${me}" stroke="${hot?'#D2463C':'var(--bg,#0b1020)'}" stroke-width="${hot?1.6:.8}"/>`
   +`<text x="${f(px+8)}" y="${f(py-7)}" font-size="10" fill="${me}" font-family="var(--mono)" font-weight="700" ${px>x1-70?'text-anchor="end"':''}>${nm}</text>`;
  const tp=tailP(sp);
  return `<p class="note" style="margin:0 0 4px">σ : risque annualisé du book, bruit d'estimation compris. μ : rendement attendu annualisé (quatre fois celui du trimestre) — collatéral, impact, drain de volatilité et coût moyen des accidents de levier compris. Traits tous les 10 %. Les concurrents sont placés à leur couple estimé.</p><svg viewBox="0 0 ${W} ${H}" style="width:100%;height:auto;display:block;margin-bottom:6px">${g}</svg>`
   +`<p class="note" style="margin:0 0 10px">${tp>0?`À σ ${sv} : <b class="neg-g">${dec(tp*100,0)} % de probabilité</b> d'un accident de levier ce trimestre, perte de l'ordre de ${dec(0.62*tailL(sp)*100,0)} % de l'encours si vous le laissez courir.`:`Sous σ ${dec(TAIL.x0*100,0)} %, pas d'accident de levier possible.`}</p>`;
 }
 const L=3,Rr=4,T=5,B=3;
 const X=v=>L+(100-L-Rr)*v/xm,Y=v=>100-B-(100-B-T)*(v-y0)/(y1-y0);
 let s=`<svg viewBox="0 0 100 100" preserveAspectRatio="none" style="position:absolute;inset:0;width:100%;height:100%">`
  +(TAIL.x0<xm?`<rect x="${f(X(TAIL.x0))}" y="${T}" width="${f(100-Rr-X(TAIL.x0))}" height="${f(100-B-T)}" fill="#D2463C" opacity=".10"/>`:'')
  +lv(0.1,xm).map(v=>`<line x1="${f(X(v))}" x2="${f(X(v))}" y1="${T}" y2="${100-B}" stroke="var(--dimmer)" stroke-width=".5" opacity=".45" vector-effect="non-scaling-stroke"/>`).join('')
  +lv(y0,y1).filter(v=>v>y0+1e-9).map(v=>`<line x1="${L}" x2="${100-Rr}" y1="${f(Y(v))}" y2="${f(Y(v))}" stroke="var(--dimmer)" stroke-width="${Math.abs(v)<1e-9?.9:.5}" opacity="${Math.abs(v)<1e-9?.8:.45}" vector-effect="non-scaling-stroke"/>`).join('')
  +`<line x1="${L}" x2="${100-Rr}" y1="${100-B}" y2="${100-B}" stroke="var(--dimmer)" stroke-width="1" vector-effect="non-scaling-stroke"/>`
  +`<line x1="${L}" x2="${L}" y1="${T}" y2="${100-B}" stroke="var(--dimmer)" stroke-width="1" vector-effect="non-scaling-stroke"/></svg>`;
 R.forEach(r=>{s+=`<i class="rd" style="left:${f(X(r.x))}%;top:${f(Y(r.y))}%;background:${r.c}"></i>`});
 const px=X(sp),py=Y(pr);
 s+=`<i class="rd me${hot?' hot':''}" style="left:${f(px)}%;top:${f(py)}%;background:${me}"></i>`
  +`<span class="rv${hot?' hot':''}" style="left:${f(Math.min(58,Math.max(L+2,px-12)))}%;bottom:6%">σ ${sv}</span>`
  +`<span class="rv" style="left:${L+2}%;top:${f(Math.min(62,Math.max(T+1,py-12)))}%">μ ${mv}</span>`;
 return `<div class="rmap">${s}</div>`;
}
"""+e.s[j:]
e.rep(".rmap .rv{position:absolute;font-family:var(--mono);font-size:9.5px;",".rmap .rv{position:absolute;font-family:var(--mono);font-size:10px;")

# ───────── B2. trésorerie à trois chiffres significatifs ─────────
e.rep("const treso=x=>{const a=Math.abs(x),sg=x<0?'−':'';if(a>=1)return sig3(x,'Md$');if(a>=0.001)return sg+(a*1000).toFixed(1).replace('.',',')+' M$';return sg+Math.round(a*1e6)+' k$'};",
      "const treso=x=>{const a=Math.abs(x),sg=x<0?'−':'',t3=(v,u)=>sg+v.toFixed(v>=99.95?0:v>=9.995?1:2).replace('.',',')+' '+u;   /* lot 67 : trois chiffres */\n if(a>=1)return sig3(x,'Md$');if(a>=0.001)return t3(a*1000,'M$');return t3(a*1e6,'k$')};")

# ───────── B3. lignes de marché : ordre et coût à la place du rendement passé, « rentabilité » ─────────
e.rep("""      <span class="rr ${lr===null?'dim-g':cls(lr)}">${lr===null?'—':sgn(lr,1)}</span></div>""",
      """      <span class="rr">${ordTxt(i)}</span></div>""")
e.rep("""  gl=`<div class="rgrid2"><div><span class="k">Ordre</span> ${od}<span class="k" style="margin-left:10px">coût</span> <b>${mm(t.cost||0)}</b></div>
   <div><span class="k">+1</span> profit ${ex1} · risque ${pct1(rP)}</div><div><span class="k">−1</span> profit ${pM} · risque ${pct1(rM)}</div></div>`}""",
      """  gl=`<div class="rgrid2"><div><span class="k">+1</span> rentabilité ${ex1} · risque ${pct1(rP)}</div><div><span class="k">−1</span> rentabilité ${pM} · risque ${pct1(rM)}</div></div>`}""")
e.rep("function rowInfo(i){","""/* lot 67 : ordre et coût, en tête de ligne */
function ordTxt(i){if(!mktOpen(i))return '';const k0=S.k0?S.k0[i]:S.k[i],d=S.k[i]-k0;if(!d)return '<span class="dim-g">—</span>';
 return `<b class="${d>0?'pos-g':'neg-g'}">${d>0?'achat':'vente'} ${Math.abs(d)}</b> <span class="dim-g">${mm(tcost(d,i).cost||0)}</span>`}
function rowInfo(i){""")

# ───────── C. équilibrage (campagne 108 parties : 3 styles × 3 difficultés × bots intelligent et nul, 6 graines) ─────────
# Mesuré : le bot intelligent, qui choisit désormais son risque (σ moyen 22 à 29 %), recevait 0,5 à 1,5 rouge et
# 1 à 3 jaunes par partie : à σ 29 %, un trimestre à −5 % arrive une fois sur trois — ce n'est pas une faute.
# Seuils doublés. Concurrents : médiane +12 à +50 % en deux ans contre +54 à +113 % pour le bot intelligent :
# RIVK 0,20 → 0,27.
e.rep("  if(qTotal<=-0.12*tt)red=`trimestre à ${sgnp(qTotal,1)}`;","  if(qTotal<=-0.20*tt)red=`trimestre à ${sgnp(qTotal,1)}`;")
e.rep("  else if(ddp>=0.25*tt&&ddp>(C.ddR||0)+0.05)","  else if(ddp>=0.30*tt&&ddp>(C.ddR||0)+0.05)")
e.rep("  if(qTotal<=-0.05*tt)why.push(","  if(qTotal<=-0.10*tt)why.push(")
e.rep("  if(ddp>=0.12*tt&&ddp>(C.ddY||0)+0.04)","  if(ddp>=0.18*tt&&ddp>(C.ddY||0)+0.04)")
e.rep("if(qTotal-med<=-0.10)why.push(","if(qTotal-med<=-0.15)why.push(")
e.rep("  if(ddp<0.08){C.ddR=0;C.ddY=0}","  if(ddp<0.10){C.ddR=0;C.ddY=0}")
e.rep("""<li>🟥 <b>Rouge</b> : trimestre à −12 % ou pire, repli de 25 % depuis le plus haut (puis chaque 5 points de plus), appel de marge, ou deuxième jaune.</li><li>🟨 <b>Jaune</b> : trimestre à −5 % ou pire, repli de 12 % (puis chaque 4 points de plus), 10 points sous la médiane des concurrents, book vide, griefs accumulés.</li>""",
"""<li>🟥 <b>Rouge</b> : trimestre à −20 % ou pire, repli de 30 % depuis le plus haut (puis chaque 5 points de plus), appel de marge, ou deuxième jaune.</li><li>🟨 <b>Jaune</b> : trimestre à −10 % ou pire, repli de 18 % (puis chaque 4 points de plus), 15 points sous la médiane des concurrents, book vide, griefs accumulés.</li>""")
e.rep("RIVK=0.20;","RIVK=0.27;")
# couper la moitié du book après un accident : le latent déjà couru par la moitié coupée est acquis (qEvM),
# sinon le ruban retombait de la moitié du gain du trimestre au point suivant, et la clôture le comptait faux.
e.rep("  if(o.id==='cut')S.k=S.k.map(v=>Math.trunc(v/2));",
      "  if(o.id==='cut'){const r0=typeof liveRet==='function'?liveRet():0;S.k=S.k.map(v=>Math.trunc(v/2));const r1=typeof liveRet==='function'?liveRet():0;S.qEvM=(S.qEvM||0)+(r0-r1)*S.navQ0}")
# contre-campagne (36 parties) : RIVK 0,27 portait les concurrents à +67 à +145 % en deux ans (le coût fixe rend
# la réponse très convexe) → 0,24. Le quant restait à 1,5 rouge par partie : ses jaunes venaient presque tous des
# « griefs accumulés », que la dérogation au modèle (−3 à chaque dépêche suivie) nourrit mécaniquement. Ces notes
# pèsent déjà sur la confiance : plus de carton pour elles. Écart à la médiane : 15 → 20 pts (concurrents plus risqués).
e.rep("RIVK=0.27;","RIVK=0.24;")
e.rep("  if(S.gSnap&&clo0.rc0-S.gSnap.rc<=-25)why.push('griefs accumulés dans le trimestre');\n","")
e.rep("if(qTotal-med<=-0.15)why.push(","if(qTotal-med<=-0.20)why.push(")
e.rep("15 points sous la médiane des concurrents, book vide, griefs accumulés.</li>","20 points sous la médiane des concurrents, book vide.</li>")
e.rep("Le comité ne tient pas de jauge : il juge le book à chaque clôture et sort des cartons. Ce qu'il note entre-temps pèse sur la confiance ; trop de griefs dans un trimestre valent un jaune.",
      "Le comité ne tient pas de jauge : il juge vos résultats à chaque clôture et sort des cartons. Ce qu'il note entre-temps pèse sur la confiance, pas sur les cartons.")
# flux : dernier des trois styles dans les deux campagnes (bot intelligent 6,7 à 36 M$ contre 22 à 80 pour les
# autres, survie jusqu'à 33 %). Son seuil de rachats pour repli (16 %) date du mandat à 20 % de vol : sans mandat,
# à σ 22 %, il saute presque chaque année. 16 → 22 %, nervosité des investisseurs ×1,60 → ×1,35.
e.rep("lpMult:1.60,ddMax:0.16,modelScale:1.20","lpMult:1.35,ddMax:0.22,modelScale:1.20")
e.rep("les investisseurs suivent votre courbe au jour le jour : jauge 60 % plus nerveuse","les investisseurs suivent votre courbe au jour le jour : confiance 35 % plus nerveuse")
e.rep("rachats pour repli dès 16 % de perte au lieu de 28 %","rachats pour repli dès 22 % de perte au lieu de 28 %")
# ───────── A6. ruban : la commission de performance court pendant le trimestre ─────────
# Sonde (4 parties, 90 clôtures) : après le point A1, le dernier pas des concurrents vaut 0 (médiane, p90). Côté
# joueur, le saut restant est la commission de performance, prélevée d'un coup à la clôture (−2 % sur un trimestre
# à +10 %). Elle est désormais provisionnée au fil du trimestre, comme dans un vrai fonds : le ruban et la tuile
# de performance lisent le net (liveNet), et la clôture ne fait plus que confirmer.
e.rep("function liveRet(){","""function liveNet(){const lr=liveRet(),ip=S.idx*(1+lr);
 return ip>S.hwmIdx?lr-perfFee()*(ip-S.hwmIdx)/Math.max(1e-9,S.idx):lr}
function liveRet(){""")
e.rep("return {y0,base:v,now:cur*(1+liveRet())/v*100,","return {y0,base:v,now:cur*(1+liveNet())/v*100,")
e.rep("const lat=(S.phase==='events'&&S.live&&typeof liveRet==='function')?liveRet():0;","const lat=(S.phase==='events'&&S.live&&typeof liveRet==='function')?liveNet():0;")

# ───────── A7. mi-parcours : le latent affiché est exactement le trimestre moins les dépêches ─────────
# Le latent était recalculé à part (½ du rendement de base, sans collatéral ni frais) : il pouvait être négatif
# quand le trimestre, dépêches ôtées, était positif. Désormais latent = trimestre − dépêches/desk/incidents, et les
# contributeurs par marché sont remis à l'échelle de ce latent quand leur somme est de même signe.
e.rep(""" const g=pnlGauge(p*0.8,"Point de mi-trimestre : performance latente des positions");
 const navB=S.nav;""",""" const qtd0=navNow()/Math.max(1e-9,S.navQ0)-1,oth0=((S.qEvM||0)+(S.qIncM||0))/Math.max(1e-9,S.navQ0),lat=qtd0-oth0;
 if(p*lat>0)rows.forEach(o=>o.v*=lat/p);p=lat;
 const g=pnlGauge(p*0.8,"Point de mi-trimestre : performance latente des positions");
 const navB=S.nav;""")
e.rep(""" const qtd=navNow()/Math.max(1e-9,S.navQ0)-1,oth=((S.qEvM||0)+(S.qIncM||0))/Math.max(1e-9,S.navQ0);
 const ttl=qtd>=0?""",""" const qtd=qtd0,oth=oth0;
 const ttl=qtd>=0?""")

# ───────── C2. campagne finale (72 parties, bots intelligent et nul, 3 styles × 3 difficultés) ─────────
# Concurrents médians sur deux ans : Pont-Levis −4 %, Médaillon +86 %, Citadelle −4 % : deux fonds sur trois qui
# ne gagnent rien en deux ans, pendant que le bot intelligent fait +95 à +150 %. Adresse par style : le quant
# garde la sienne, le discrétionnaire et le flux reçoivent 0,34 ; Citadelle redescend à 30 % de risque.
# Flux : dernier des styles pour le bot intelligent (11 M$ contre 24 et 44) : intuition juste 78 → 85 %.
e.rep("RIVK=0.24;","RIVK=0.24,RIVKS={syst:0.22,fonda:0.34,flux:0.34};")
e.rep("return t*((v/2)*(RIVK*e+","return t*((v/2)*((RIVKS[r.style]||RIVK)*e+")
e.rep("y:S.rate/4+(v/2)*RIVK*E-0.008","y:S.rate/4+(v/2)*(RIVKS[rv.style]||RIVK)*E-0.008")
e.rep("base:0.34,conv:0,cut:0.6","base:0.30,conv:0,cut:0.6")
e.rep("S.hunch={k,up:(rng()<0.78)===(S.f[k]>0)};","S.hunch={k,up:(rng()<0.85)===(S.f[k]>0)};")
e.done("lot 67")
