# -*- coding: utf-8 -*-
"""Lot 17 — le ruban : zones vertes et rouges, fenêtre zoomée glissante, dézoom final.

Rendu (voir la référence fournie) : le trait ET le remplissage changent de couleur de part
et d'autre du zéro. Les tronçons sont découpés aux croisements exacts, interpolés
linéairement entre les deux points qui encadrent la ligne de base — sinon la couleur change
un point trop tard et la zone colorée déborde du bon côté.

Animation, en deux temps :
  - 5 s de tracé, vus à travers une fenêtre zoomée qui glisse en gardant la tête du trait
    au centre. Le zoom horizontal est calculé pour que le segment nouveau occupe toujours
    la même fraction de la fenêtre : la vitesse de défilement est donc constante d'un
    trimestre à l'autre, que le ruban compte 300 points ou 900. Le zoom vertical est plus
    faible que l'horizontal, sinon la courbe sort du cadre.
  - 0,9 s de dézoom vers la vue complète, puis plus rien ne bouge sauf le point de tête.

Piège : `animateTransform` n'accepte PAS `type="matrix"` — SVG 1.1 ne définit que translate,
scale, rotate, skewX et skewY. L'animation est silencieusement ignorée, le graphique reste
plat et rien ne signale l'erreur. D'où deux groupes imbriqués, l'un animé en translation,
l'autre en échelle.

Le dévoilement se fait par une fenêtre de découpe qui s'élargit, et non par `stroke-dasharray` :
avec un trait coupé en tronçons de couleurs, il faudrait sinon répartir le retard et la durée
sur chaque morceau au prorata de sa longueur.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()

e.rep("""function tapeSvg(p,from){
 const W=320,H=78,pad=5,n=p.length;
 let lo=Math.min(100,...p),hi=Math.max(100,...p);
 const sp=(hi-lo)||1;lo-=sp*0.12;hi+=sp*0.12;
 const px=i=>pad+i*(W-2*pad)/(n-1),py=v=>H-pad-(v-lo)/(hi-lo)*(H-2*pad);
 const pt=i=>px(i).toFixed(1)+','+py(p[i]).toFixed(1);
 const col=p[n-1]>=100?'#4FA98C':'#C4576F',id='tp'+(NGID++);
 const k=Math.max(0,Math.min(n-1,from|0));
 const seg=(a,b)=>{const o=[];for(let i=a;i<=b;i++)o.push(pt(i));return o};
 const area=(a,b)=>{const o=seg(a,b);
   return 'M'+px(a).toFixed(1)+','+(H-pad)+' L'+o.join(' L')+' L'+px(b).toFixed(1)+','+(H-pad)+'Z'};
 return `<svg class="navc" viewBox="0 0 ${W} ${H}" aria-hidden="true">
  <defs><linearGradient id="${id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${col}" stop-opacity=".30"/><stop offset="1" stop-color="${col}" stop-opacity="0"/></linearGradient></defs>
  ${k>0?`<path d="${area(0,k)}" fill="url(#${id})"/>`:''}
  ${k<n-1?`<path class="tapefill" d="${area(k,n-1)}" fill="url(#${id})"/>`:''}
  <line x1="0" y1="${py(100).toFixed(1)}" x2="${W}" y2="${py(100).toFixed(1)}" stroke="#35496A" stroke-width="1" stroke-dasharray="3 4"/>
  ${k>0?`<polyline points="${seg(0,k).join(' ')}" fill="none" stroke="${col}" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"/>`:''}
  ${k<n-1?`<polyline class="tapedraw" points="${seg(k,n-1).join(' ')}" fill="none" stroke="${col}" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"/>`:''}
  <circle class="tapehead2" cx="${px(n-1).toFixed(1)}" cy="${py(p[n-1]).toFixed(1)}" r="3" fill="${col}">
   <animate attributeName="r" values="3;6;3" dur="1.8s" repeatCount="indefinite"/></circle></svg>`;
}""",
"""const TAPE_UP='#3FCF8E',TAPE_DN='#F2545B';
/* Tronçons de même signe, croisements de la ligne de base interpolés. */
function tapePieces(p,x,y,base){
 const n=p.length,out=[];let cur=[[x(0),y(p[0])]],up=p[0]>=base;
 for(let i=1;i<n;i++){
  const u=p[i]>=base;
  if(u!==up&&p[i]!==p[i-1]){
   const t=(base-p[i-1])/(p[i]-p[i-1]),xi=(i-1)+t,c=[x(xi),y(base)];
   cur.push(c);out.push({up,pts:cur});cur=[c];up=u;
  }
  cur.push([x(i),y(p[i])]);
 }
 out.push({up,pts:cur});return out;
}
/* opt.anim : tracé animé avec fenêtre glissante. Sinon rendu statique complet. */
function tapeSvg(p,from,opt){
 opt=opt||{};
 const W=320,H=opt.h||78,pad=5,n=p.length;
 let lo=Math.min(100,...p),hi=Math.max(100,...p);
 const sp=(hi-lo)||1;lo-=sp*0.14;hi+=sp*0.14;
 const x=i=>pad+i*(W-2*pad)/Math.max(1,n-1),y=v=>H-pad-(v-lo)/(hi-lo)*(H-2*pad);
 const y0=y(100),id='tp'+(NGID++);
 const f=n=>n.toFixed(1);
 let body='';
 tapePieces(p,x,y,100).forEach(s=>{
  const c=s.up?TAPE_UP:TAPE_DN,pts=s.pts.map(q=>f(q[0])+','+f(q[1])).join(' ');
  body+=`<path d="M${f(s.pts[0][0])},${f(y0)} L${pts} L${f(s.pts[s.pts.length-1][0])},${f(y0)}Z" fill="${c}" opacity=".20"/>`
      +`<polyline points="${pts}" fill="none" stroke="${c}" stroke-width="1.7" stroke-linejoin="round" stroke-linecap="round"/>`;
 });
 const headC=p[n-1]>=100?TAPE_UP:TAPE_DN;
 const base=`<line x1="0" y1="${f(y0)}" x2="${W}" y2="${f(y0)}" stroke="#4A5C78" stroke-width="1" stroke-dasharray="2 3"/>`;
 if(!opt.anim||from<=0||from>=n-1){
  return `<svg class="navc" viewBox="0 0 ${W} ${H}" aria-hidden="true">${base}${body}
   <circle cx="${f(x(n-1))}" cy="${f(y(p[n-1]))}" r="3" fill="${headC}">
    <animate attributeName="r" values="3;6;3" dur="1.8s" repeatCount="indefinite"/></circle></svg>`;
 }
 /* fenêtre glissante : la tête reste au centre, le zoom horizontal est réglé pour que le
    segment nouveau occupe toujours la même fraction de la fenêtre */
 const DRAW=5,ZOUT=0.9,TOT=DRAW+ZOUT;
 const x0=x(from),x1=x(n-1);
 const Zx=Math.max(2.5,Math.min(13,(W*0.62)/Math.max(6,x1-x0)));
 const Zy=Math.min(3.0,Math.max(1.6,Zx*0.34));
 const cx=W/2,cy=H/2,K=40,tr=[],sc=[],kt=[];
 for(let j=0;j<=K;j++){
  const u=j/K,idx=from+(n-1-from)*u,px=x(idx),py=y(p[Math.round(idx)]);
  tr.push(`${f(cx-Zx*px)} ${f(cy-Zy*py)}`);sc.push(`${f(Zx)} ${f(Zy)}`);
  kt.push((u*DRAW/TOT).toFixed(4));
 }
 tr.push('0 0');sc.push('1 1');kt.push('1');
 return `<svg class="navc" viewBox="0 0 ${W} ${H}" aria-hidden="true">
  <defs><clipPath id="c${id}" clipPathUnits="userSpaceOnUse">
   <rect x="0" y="-${H*4}" height="${H*9}" width="${f(x0)}">
    <animate attributeName="width" from="${f(x0)}" to="${W}" dur="${DRAW}s" fill="freeze"/></rect>
  </clipPath></defs>
  ${base}
  <g><animateTransform attributeName="transform" type="translate" dur="${TOT}s" fill="freeze"
      calcMode="linear" keyTimes="${kt.join(';')}" values="${tr.join(';')}"/>
   <g><animateTransform attributeName="transform" type="scale" dur="${TOT}s" fill="freeze"
       calcMode="linear" keyTimes="${kt.join(';')}" values="${sc.join(';')}"/>
    <g clip-path="url(#c${id})">${body}</g></g></g>
  <circle cx="${f(cx)}" cy="${f(cy)}" r="3.4" fill="${headC}">
   <animate attributeName="cx" from="${f(cx)}" to="${f(x(n-1))}" begin="${DRAW}s" dur="${ZOUT}s" fill="freeze"/>
   <animate attributeName="cy" from="${f(cy)}" to="${f(y(p[n-1]))}" begin="${DRAW}s" dur="${ZOUT}s" fill="freeze"/>
   <animate attributeName="r" values="3;6;3" dur="1.8s" begin="${TOT}s" repeatCount="indefinite"/></circle></svg>`;
}""")
e.rep("""  ${tapeSvg(p,S.tape.from||0)}</div>`;""",
      """  ${tapeSvg(p,S.tape.from||0,{anim:1})}</div>`;""")

# ── le trimestre bouclé, en grand, à la place de l'ancienne courbe ──
e.rep("""  ${navBox(`PERFORMANCE NETTE CUMULÉE · ${S.q} TRIMESTRE${S.q>1?'S':''}`,idxSeries(),{anim:1,trough:1})}""",
"""  ${(S.tape&&S.tape.pts&&S.tape.pts.length>3)?`<div class="tape" style="margin-top:12px"><div class="tapehead">
    <span>LE TRIMESTRE, HEURE PAR HEURE</span><b class="${S.tape.pts[S.tape.pts.length-1]>=100?'pos-g':'neg-g'}">${sgnp((S.tape.pts[S.tape.pts.length-1]-100)/100,1)} DEPUIS JANVIER</b></div>
    ${tapeSvg(S.tape.pts,0,{h:132})}</div>`
   :navBox(`PERFORMANCE NETTE CUMULÉE · ${S.q} TRIMESTRE${S.q>1?'S':''}`,idxSeries(),{anim:1,trough:1})}""")
e.rep(""".tapedraw{stroke-dasharray:4000;stroke-dashoffset:4000;animation:navdr 3s linear forwards}
.tapefill{opacity:0;animation:tapefade 3s linear forwards}
@keyframes tapefade{to{opacity:1}}
@media (prefers-reduced-motion:reduce){.tapedraw{animation:none;stroke-dashoffset:0}.tapefill{animation:none;opacity:1}}""",
"""@media (prefers-reduced-motion:reduce){.tape animate,.tape animateTransform{display:none}}""")

e.done("lot 17 — ruban colore, fenetre glissante, dezoom")
