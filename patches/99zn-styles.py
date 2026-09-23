# -*- coding: utf-8 -*-
"""Lot 52 — chaque style lit mieux son signal, en voit plus, et le voit d'abord.

Décision d'Antoine : (a) + (b) + (c).
  (a) Précision. Le quant lit le portage, le gérant de flux la tendance, le discrétionnaire
      (fondamental) la valeur, avec un bruit ×0,3 ; les deux autres signaux ×1,3. Le nombre de
      tirages est inchangé (trois par marché) : aucun flux de hasard ne bouge. Le rendement
      attendu (lot 51) utilise ces mêmes précisions.
  (b) Profondeur.
      - Quant : le classement du portage, les trois marchés à porter et les trois à vendre.
      - Flux : au mi-parcours, la tendance du trimestre déjà dessinée sur les marchés qui
        bougent le plus (moitié du mouvement réel, légèrement bruitée).
      - Discrétionnaire : les catalyseurs. Chaque trimestre, deux marchés dont la valeur est
        nettement décalée (|V| ≥ 1) voient l'écart commencer à se refermer : le terme de valeur
        y compte double, pour tout le monde. Seul le discrétionnaire sait lesquels (badge ⚡ dans
        le book, et son rendement attendu en tient compte). Choix par tirage pur (hash32).
  (c) Mise en avant. Le signal du style s'affiche en premier, en gras ; les deux autres en retrait.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
e.rep("const SIGW={t:0.12,c:0.10,v:0.08};","const SIGW={t:0.12,c:0.10,v:0.08};\n/* le signal que chaque style lit le mieux */\nconst STYLESIG={syst:'c',flux:'t',fonda:'v'},SIGNM={t:'Tendance',c:'Portage',v:'Valeur'};")
# (a) précision
e.rep("S.tcvEst={t:S.tcv.t.map(z=>quant(z+e*gauss())),c:S.tcv.c.map(z=>quant(z+e*gauss())),v:S.tcv.v.map(z=>quant(z+e*gauss()))};",
      "/* lot 52 : chaque style lit son signal avec un bruit ×0,3, les deux autres ×1,3 */\n"
      " const mine=STYLESIG[S.prof],ne=kk=>e*(kk===mine?0.3:1.3);\n"
      " S.tcvEst={t:S.tcv.t.map(z=>quant(z+ne('t')*gauss())),c:S.tcv.c.map(z=>quant(z+ne('c')*gauss())),v:S.tcv.v.map(z=>quant(z+ne('v')*gauss()))};")
# (b) catalyseurs : choisis avant le tirage des rendements, comptés dans le marché
e.rep("S.rBase=drawReturns();",
      "/* catalyseurs : deux marchés où l'écart de valeur se referme ce trimestre (tirage pur) */\n"
      " {const c=INSTR.map((x,i)=>i).filter(i=>mktOpen(i)&&Math.abs(S.tcv.v[i])>=1);\n"
      "  S.cat=c.map(i=>({i,u:prng32(hash32('cat'+i+'_'+S.q,S.seed))()})).sort((a,b)=>a.u-b.u).slice(0,2).map(o=>o.i)}\n"
      " S.rBase=drawReturns();")
e.rep("   r+=x.sigQ*(0.12*S.tcv.t[i]+0.10*S.tcv.c[i]+0.08*S.tcv.v[i])*(UNIV().edge||1);",
      "   r+=x.sigQ*(0.12*S.tcv.t[i]+0.10*S.tcv.c[i]+0.08*S.tcv.v[i]*((S.cat&&S.cat.includes(i))?2:1))*(UNIV().edge||1);")
e.rep(" if(e){z+=(SIGW.t*e.t[i]+SIGW.c*e.c[i]+SIGW.v*e.v[i])*(UNIV().edge||1);",
      " if(e){const cv=(S.prof==='fonda'&&S.cat&&S.cat.includes(i))?2:1;   /* seul le discrétionnaire connaît ses catalyseurs */\n"
      "  z+=(SIGW.t*e.t[i]+SIGW.c*e.c[i]+SIGW.v*cv*e.v[i])*(UNIV().edge||1);")
# (c) mise en avant + badge catalyseur
e.rep("""<div class="tcv"><button data-mkt="${i}" class="tcvb">${tcvChip('Tendance',S.tcvEst.t[i])}${tcvChip('Portage',S.tcvEst.c[i])}${tcvChip('Valeur',S.tcvEst.v[i])}<span class="more">détails ›</span></button></div></div>`;""",
      """<div class="tcv"><button data-mkt="${i}" class="tcvb">${(()=>{const m=STYLESIG[S.prof]||'t',o=['t','c','v'].filter(z=>z!==m);
       return `<span class="mine">${tcvChip(SIGNM[m],S.tcvEst[m][i])}</span>`+o.map(z=>`<span class="oth">${tcvChip(SIGNM[z],S.tcvEst[z][i])}</span>`).join('')})()}${(S.prof==='fonda'&&S.cat&&S.cat.includes(i))?'<i class="cat">⚡ catalyseur</i>':''}<span class="more">détails ›</span></button></div></div>`;""")
e.rep(".lvls{display:grid;",".tcvb .mine i{font-weight:700;font-size:12.5px;border:1px solid currentColor}\n.tcvb .oth i{opacity:.55}\n.tcvb i.cat{color:var(--gold);border:1px solid rgba(214,178,94,.5)}\n.carryrk{font-family:var(--mono);font-size:12px;line-height:1.7}\n.lvls{display:grid;")
# (b) quant : classement du portage, au-dessus du book
e.rep("""   <div class="xbook" id="xbook"></div>""","""   <div class="xbook" id="xbook"></div>
   ${S.prof==='syst'&&S.tcvEst?(()=>{const o=INSTR.map((x,i)=>({x,i,c:S.tcvEst.c[i]})).filter(o=>mktOpen(o.i));o.sort((a,b)=>b.c-a.c);
     const L=o.slice(0,3).filter(z=>z.c>0),Sh=o.slice(-3).reverse().filter(z=>z.c<0);
     return `<details class="xbook" open><summary>Votre modèle · classement du portage</summary><div class="carryrk"><span class="pos-g">À porter</span> ${L.map(z=>`${MFLAG[z.x.sym]||''} ${z.x.sym} ${chip(z.c)}`).join(' · ')||'—'}<br><span class="neg-g">À vendre</span> ${Sh.map(z=>`${MFLAG[z.x.sym]||''} ${z.x.sym} ${chip(z.c)}`).join(' · ')||'—'}</div></details>`})():''}""")
# (b) flux : tendance du trimestre à mi-parcours
e.rep("  \"Poursuivre le trimestre\",stepEvents,midTape());",
      "  \"Poursuivre le trimestre\",stepEvents,Object.assign(midTape(),S.prof==='flux'?{top:fluxMid()}:{}));")
e.rep("function midTape(){","""/* Gérant de flux : la tendance déjà dessinée à mi-parcours, sur les marchés qui bougent le plus. */
function fluxMid(){
 const o=INSTR.map((x,i)=>({x,i,r:0.5*S.rBase[i]*(1+0.25*(prng32(hash32('fm'+i+'_'+S.q,S.seed))()-0.5))})).filter(o=>mktOpen(o.i));
 o.sort((a,b)=>Math.abs(b.r/b.x.sigQ)-Math.abs(a.r/a.x.sigQ));
 return `<p><b>Votre lecture du flux</b> — la tendance du trimestre, déjà dessinée : ${o.slice(0,4).map(z=>`${MFLAG[z.x.sym]||''} ${z.x.sym} <span class="${cls(z.r)}">${sgn(z.r,1)}</span>`).join(' · ')}.</p>`;
}
function midTape(){""")
e.rep("depuis le début de l'année. Sur ce total,","depuis le lancement. Sur ce total,")
e.done("lot 52 — signaux par style : precision, profondeur, mise en avant")
