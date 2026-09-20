# -*- coding: utf-8 -*-
"""Lot 31 — les détails d'un marché : définition du portage, et loi du rendement.

Le portage n'était défini nulle part. Et les trois signaux étaient donnés en mots
(« positif », « très négatif ») sans qu'on sache ce qu'ils valent en rendement.

On ajoute donc la loi du rendement trimestriel du marché, telle que le moteur la tire :
log-normale, de dérive `drift` (l'effet des trois signaux, déjà calculé pour la
recommandation du desk) et d'écart-type `sigQ`. La densité est dessinée en SVG, avec
l'espérance et l'écart-type trimestriels annotés — de quoi juger si un signal « positif »
mérite qu'on y mette du risque.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
e.rep(""" const t1=tcost(1,i);""",
""" const t1=tcost(1,i);
 /* Loi du rendement trimestriel : log-normale de paramètres (mu, sigma) en log.
    Le moteur tire r = exp(mu + sigma·z) − 1 ; on trace la densité de r. */
 const sg=x.sigQ,mu=Math.log(1+drift)-sg*sg/2;
 const esp=Math.exp(mu+sg*sg/2)-1, ect=Math.sqrt((Math.exp(sg*sg)-1))*Math.exp(mu+sg*sg/2);
 const dens=(()=>{const W=320,H=96,pad=6,lo=Math.max(-0.95,esp-3.2*ect),hi=esp+3.2*ect;
  const n=90,ys=[];let mx=1e-9;
  for(let j=0;j<=n;j++){const r=lo+(hi-lo)*j/n,u=1+r;
   const f=u<=0?0:Math.exp(-Math.pow(Math.log(u)-mu,2)/(2*sg*sg))/(u*sg*Math.sqrt(2*Math.PI));
   ys.push(f);mx=Math.max(mx,f)}
  const px=j=>pad+j*(W-2*pad)/n, py=v=>H-pad-v/mx*(H-2*pad);
  const pts=ys.map((v,j)=>px(j).toFixed(1)+','+py(v).toFixed(1));
  const x0=pad+(0-lo)/(hi-lo)*(W-2*pad), xe=pad+(esp-lo)/(hi-lo)*(W-2*pad);
  const col=drift>=0?'#3FCF8E':'#F2545B';
  return `<svg viewBox="0 0 ${W} ${H}" style="width:100%;height:auto;display:block;margin:6px 0">
   <path d="M${pad},${H-pad} L${pts.join(' L')} L${W-pad},${H-pad}Z" fill="${col}" opacity=".18"/>
   <polyline points="${pts.join(' ')}" fill="none" stroke="${col}" stroke-width="1.8"/>
   <line x1="${x0.toFixed(1)}" y1="2" x2="${x0.toFixed(1)}" y2="${H-pad}" stroke="#5B6E8C" stroke-width="1" stroke-dasharray="2 3"/>
   <line x1="${xe.toFixed(1)}" y1="6" x2="${xe.toFixed(1)}" y2="${H-pad}" stroke="#D9B06A" stroke-width="1.4"/>
   <text x="${pad}" y="${H-1}" font-size="8" fill="#6F8199" font-family="ui-monospace,monospace">${(lo*100).toFixed(0)} %</text>
   <text x="${W-pad}" y="${H-1}" text-anchor="end" font-size="8" fill="#6F8199" font-family="ui-monospace,monospace">+${(hi*100).toFixed(0)} %</text></svg>`})();""")
e.rep("""openModal(`${x.sym} — ${x.nm}`,`<p>${x.sub}.""",
"""openModal(`${x.sym} — ${x.nm}`,`${dens}
  <p class="note" style="margin-top:0">Densité du rendement du trimestre, log-normale. Trait doré : l'espérance, <em class="${esp>=0?'pos-g':'neg-g'}">${(esp*100).toFixed(1)} %</em>. Écart-type trimestriel <em>${(ect*100).toFixed(1)} %</em>. Pointillé : le zéro. L'asymétrie vient de la loi elle-même — on ne peut pas perdre plus que tout, on peut gagner davantage.</p>
  <p class="note"><b>Le portage</b> est ce que la position rapporte si rien ne bouge : écart entre le prix du contrat et le comptant, coupon net du coût de financement, prime de roulement d'une échéance à l'autre. Un portage positif paie l'attente, un portage négatif la facture.</p>
  <p>${x.sub}.""")
e.done("lot 31 — portage et densite du rendement")
