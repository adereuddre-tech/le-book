# -*- coding: utf-8 -*-
"""Lot 74 — jauges du nuage rentabilité / risque raccourcies à la valeur du fonds.
Risque : de l'origine jusqu'au risque du fonds. Rentabilité : de zéro jusqu'à la rentabilité du fonds (vers le
bas si elle est négative). Le dégradé reste calé sur l'axe entier (userSpaceOnUse) : la couleur au bout de la
barre est celle de la valeur. Une trace très pâle de l'échelle complète reste visible sous la barre."""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
e.rep("""function gzGrad(id,st,lo,hi,vert){   /* dégradé SVG, offsets en fraction de l'axe */
 const o=v=>Math.max(0,Math.min(1,(v-lo)/(hi-lo)));
 const s=st.map(([v,k])=>`<stop offset="${(vert?1-o(v):o(v)).toFixed(3)}" stop-color="${rgb(GZC[k])}"/>`);
 if(vert)s.reverse();
 return `<linearGradient id="${id}" x1="0" y1="0" x2="${vert?0:1}" y2="${vert?1:0}">${s.join('')}</linearGradient>`;
}""","""function gzGrad(id,st,lo,hi,vert,pa,pb){   /* lot 74 : dégradé en coordonnées de l'axe (pa = pixel de lo, pb = de hi) */
 const o=v=>Math.max(0,Math.min(1,(v-lo)/(hi-lo)));
 const s=st.map(([v,k])=>`<stop offset="${o(v).toFixed(3)}" stop-color="${rgb(GZC[k])}"/>`);
 const c=vert?`x1="0" x2="0" y1="${pa}" y2="${pb}"`:`x1="${pa}" x2="${pb}" y1="0" y2="0"`;
 return `<linearGradient id="${id}" gradientUnits="userSpaceOnUse" ${c}>${s.join('')}</linearGradient>`;
}
/* barre de jauge d'une valeur à une autre, sur une trace pâle de l'axe entier */
function gzBar(id,vert,fix,th,a,b,full0,full1,rx){
 const lo=Math.min(a,b),hi=Math.max(a,b),f0=Math.min(full0,full1),f1=Math.max(full0,full1),r=rx?` rx="${rx}"`:'';
 const R=(p,q,op)=>vert?`<rect x="${fix}" y="${p.toFixed(2)}" width="${th}" height="${Math.max(0,q-p).toFixed(2)}"${r} fill="url(#${id})"${op?` opacity="${op}"`:''}/>`
  :`<rect x="${p.toFixed(2)}" y="${fix}" width="${Math.max(0,q-p).toFixed(2)}" height="${th}"${r} fill="url(#${id})"${op?` opacity="${op}"`:''}/>`;
 return R(f0,f1,.14)+R(lo,hi);
}""")
e.rep("""  let g=`<defs>${gzGrad('gzxB',stX,0,xm,0)}${gzGrad('gzyB',stY,y0,y1,1)}</defs>`
   +`<rect x="${x0}" y="${yb+1}" width="${x1-x0}" height="3" rx="1.5" fill="url(#gzxB)"/>`
   +`<rect x="${x0-4}" y="${yt}" width="3" height="${yb-yt}" rx="1.5" fill="url(#gzyB)"/>`;""",
"""  let g=`<defs>${gzGrad('gzxB',stX,0,xm,0,x0,x1)}${gzGrad('gzyB',stY,y0,y1,1,Y(y0),Y(y1))}</defs>`
   +gzBar('gzxB',0,yb+1,3,x0,X(sq),x0,x1,1.5)+gzBar('gzyB',1,x0-4,3,Y(0),Y(pr),Y(y0),Y(y1),1.5);""")
e.rep("""  +`<defs>${gzGrad(gid+'x',stX,0,xm,0)}${gzGrad(gid+'y',stY,y0,y1,1)}</defs>`
  +`<rect x="${L}" y="${100-B+.6}" width="${100-L-Rr}" height="${B-.6}" fill="url(#${gid}x)"/>`
  +`<rect x="0" y="${T}" width="${L-.6}" height="${100-B-T}" fill="url(#${gid}y)"/>`""",
"""  +`<defs>${gzGrad(gid+'x',stX,0,xm,0,L,100-Rr)}${gzGrad(gid+'y',stY,y0,y1,1,Y(y0),Y(y1))}</defs>`
  +gzBar(gid+'x',0,100-B+.6,B-.6,L,X(sq),L,100-Rr)+gzBar(gid+'y',1,0,L-.6,Y(0),Y(pr),Y(y0),Y(y1))""")
e.done("lot 74")
