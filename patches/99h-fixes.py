# -*- coding: utf-8 -*-
"""Lot 20 — corrections de fond signalées en jeu."""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()

# 1. « Trésorerie −0,9 % » : c'est l'encours du FONDS qui bouge, pas la caisse du gérant.
e.rep("""msg.push(`Trésorerie ${sgn(e.cash,1)}.`)}""",
      """msg.push(`Encours du fonds ${sgn(e.cash,1)}.`)}""")
e.rep("""msg.push(`Trésorerie ${sgn(e.cash,1)} (${(e.cash*1e4).toFixed(0)} pb).`)}""",
      """msg.push(`Encours du fonds ${sgn(e.cash,1)} (${(e.cash*1e4).toFixed(0)} pb).`)}""")

# 2. mi-parcours : dire dans quelle unité on parle
e.rep("""viennent des positions directionnelles que vous portez depuis le début du trimestre — <em class="${cls(p)}">${sgn(p,1)} · ${mn(p*navB)}</em>.""",
      """viennent des positions directionnelles que vous portez depuis le début du trimestre, soit <em class="${cls(p)}">${sgn(p,1)} sur le trimestre · ${mn(p*navB)}</em>.""")

# 3. rapport final : le vrai ruban
e.rep("""  ${navBox(`PERFORMANCE NETTE CUMULÉE · ${n} TRIMESTRE${n>1?'S':''}`,idxSeries(),{anim:1,trough:1,h:130})}""",
"""  ${(S.tape&&S.tape.pts&&S.tape.pts.length>3)?`<div class="tape" style="margin-top:12px"><div class="tapehead">
    <span>L'ANNÉE, HEURE PAR HEURE</span><b class="${S.tape.pts[S.tape.pts.length-1]>=100?'pos-g':'neg-g'}">${sgnp((S.tape.pts[S.tape.pts.length-1]-100)/100,1)}</b></div>
    ${tapeSvg(S.tape.pts,0,{h:140,rivals:rivalTapes()})}</div>`
   :navBox(`PERFORMANCE NETTE CUMULÉE · ${n} TRIMESTRE${n>1?'S':''}`,idxSeries(),{anim:1,trough:1,h:130})}""")

# 4. le book du desk doit remplir le mandat de risque
e.rep(""" for(let it=0;it<6;it++){const v=pvol(weights(k));
  if(v<1e-9)break;
  const r=tgM/v;
  if(r>0.94&&r<1.06)break;
  a*=r;k=raw.map(z=>Math.max(-S.maxk,Math.min(S.maxk,Math.round(z*a))));}""",
""" /* Si le premier arrondi écrase tout à zéro, la boucle sortait aussitôt et le desk
    proposait un book vide, sans rapport avec le mandat. On pousse l'échelle au lieu
    d'abandonner, et on laisse plus d'itérations pour converger malgré l'arrondi. */
 for(let it=0;it<14;it++){const v=pvol(weights(k));
  if(v<1e-9){a=a>0?a*2:1;k=raw.map(z=>Math.max(-S.maxk,Math.min(S.maxk,Math.round(z*a))));continue}
  const r=tgM/v;
  if(r>0.94&&r<1.06)break;
  a*=r;k=raw.map(z=>Math.max(-S.maxk,Math.min(S.maxk,Math.round(z*a))));}""")

# 5. un choix qui coûte plus que la caisse du gérant doit être grisé
e.rep("""   ${ev.ch.map((c,i)=>`<button class="choice" data-i="${i}"><b>${c.b}</b><span>${c.s}${stake(c)}</span></button>`).join('')}</div>`""",
"""   ${ev.ch.map((c,i)=>{const mg=(c.e&&c.e.mgrM)||0,ko=mg<0&&(-mg/1000)>mgrCash();
     return `<button class="choice" data-i="${i}"${ko?' disabled title="Trésorerie insuffisante"':''}><b>${c.b}</b><span>${c.s}${stake(c)}${ko?' <b class="neg-g">hors trésorerie</b>':''}</span></button>`}).join('')}</div>`""")
e.rep("""  ${ev.ch.map((c,i)=>`<button class="choice" data-i="${i}"><b>${c.b}</b><span>${c.s}</span></button>`).join('')}""",
"""  ${ev.ch.map((c,i)=>{const mg=(c.e&&c.e.mgrM)||0,ko=mg<0&&(-mg/1000)>mgrCash();
    return `<button class="choice" data-i="${i}"${ko?' disabled':''}><b>${c.b}</b><span>${c.s}${ko?' <b class="neg-g">hors trésorerie</b>':''}</span></button>`}).join('')}""",2)

e.done("lot 20 — corrections")
