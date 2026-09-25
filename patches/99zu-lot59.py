# -*- coding: utf-8 -*-
"""Lot 59 — double facturation supprimée, collatéral variable, équilibrage styles × difficulté.

Constat : suivre une dépêche (et une rivalité) retirait le coût des ordres de l'encours du fonds
(`S.nav-=cost`) ET l'ajoutait à la facture du gérant (`pendingTC`, soldée à la clôture). Les ordres
sont à la charge du gérant depuis le lot 2 : le fonds ne paie plus rien, les montants affichés dans
les boutons des dépêches sont désormais hors coûts (invariant 9 conservé : même calcul des deux côtés).

Collatéral : rendement du trimestre affiché (taux sans risque / 4 + surcroît) ; le surcroît de chaque
placement varie de ±35 % d'un trimestre à l'autre (tirage pur), espérance croissante en moyenne :
Trésor 0 < monétaire +0,2 % < repo +0,4 % < titrisations +0,6 % par trimestre.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
# ── double facturation ──
e.rep("return v-costP/S.nav","return v   /* lot 59 : les ordres sont payés par le gérant, pas par le fonds */")
e.rep("const navR=S.nav;S.nav*=(1+resid);S.nav-=cost;S.qEvM+=resid*navR-cost;","const navR=S.nav;S.nav*=(1+resid);S.qEvM+=resid*navR;")
e.rep(" const react=resid-cost/navR;"," const react=resid;")
e.rep(" const total=imm+resid*navR/navB-cost/navB;"," const total=imm+resid*navR/navB;")
e.rep("  S.nav*=(1+pnl);S.nav-=cost;S.qEvM+=pnl*navB-cost;\n  const total=pnl-cost/navB;","  S.nav*=(1+pnl);S.qEvM+=pnl*navB;\n  const total=pnl;   /* lot 59 : coût payé par le gérant seul */")
e.rep("Coût ${(t.cost*1000*1.5).toFixed(0)} M$ dans un marché","Coût ${mm(t.cost*1.5)}, à votre charge, dans un marché")
e.rep("coûts d'ajustement déduits ;","hors coûts d'ajustement, que paie votre société de gestion ;")
e.rep("${free?`Coût ${nb(mm(cost))} offert par le desk`:`Coût ${nb(mm(cost))}`}","${free?`Coût ${nb(mm(cost))} offert par le desk`:`Coût ${nb(mm(cost))} à votre charge`}")
# ── collatéral : surcroît variable, espérance croissante ──
e.rep(""" {id:'mmf',nm:'Monétaire prime',ico:'💧',y:0.003,p:0.05,l:0.02,""",""" {id:'mmf',nm:'Monétaire prime',ico:'💧',y:0.003,p:0.05,l:0.02,""")
e.rep(""" {id:'repo',nm:'Repo contre crédit',ico:'🔁',y:0.007,p:0.10,l:0.04,""",""" {id:'repo',nm:'Repo contre crédit',ico:'🔁',y:0.008,p:0.10,l:0.04,""")
e.rep(""" {id:'abs',nm:'Titrisations',ico:'🧨',y:0.014,p:0.20,l:0.06,""",""" {id:'abs',nm:'Titrisations',ico:'🧨',y:0.018,p:0.20,l:0.06,""")
e.rep("""function colOpt(){return COLL[(S&&S.col)||0]||COLL[0]}
function colYield(){const b=(S.rate||0)/4;return redOn('collat')?b*0.6:b+colOpt().y}""",
"""function colOpt(){return COLL[(S&&S.col)||0]||COLL[0]}
/* surcroît du trimestre : ±35 % autour de la moyenne, tirage pur par trimestre et par placement */
function colY(o){if(!o.y)return 0;const u=prng32(hash32('coly'+o.id+'_'+S.q,S.seed))();return o.y*(1+0.7*(u-0.5))}
function colYield(){const b=(S.rate||0)/4;return redOn('collat')?b*0.6:b+colY(colOpt())}""")
e.rep("""   <b><span class="ci">${o.ico}</span> ${o.nm}</b><span class="${o.y?'pos-g':'dim-g'}">${o.y?`+${dec(o.y*100,1)} % · ${mm(o.y*S.nav)}`:'taux sans risque'}</span>
   <span class="${o.p?'neg-g':'dim-g'}">${o.p?`${Math.round(o.p*100)} % de −${dec(o.l*100,1)} %`:'aucun risque'}</span></button>`).join('')}</div>
  <p class="note" style="margin-top:6px">${colOpt().d} ${colOpt().p?`Espérance ${sgn(colOpt().y-colOpt().p*colOpt().l,1)} sur le trimestre.`:''}</p>`;""",
"""   <b><span class="ci">${o.ico}</span> ${o.nm}</b><span>${dec((S.rate/4+colY(o))*100,1)} % ce trimestre</span><span class="${o.y?'pos-g':'dim-g'}">${o.y?`dont +${dec(colY(o)*100,1)} % · ${mm(colY(o)*S.nav)}`:'taux sans risque'}</span>
   <span class="${o.p?'neg-g':'dim-g'}">${o.p?`${Math.round(o.p*100)} % de −${dec(o.l*100,1)} %`:'aucun risque'}</span>
   <span class="dim-g">attendu ${sgn(colY(o)-o.p*o.l,1)}</span></button>`).join('')}</div>
  <p class="note" style="margin-top:6px">${colOpt().d} Le surcroît de chaque placement change d'un trimestre à l'autre ; en moyenne, plus le risque est grand, plus l'attendu l'est.</p>`;""")
e.rep("""taux sans risque ${dec(S.rate*100,1)} % l'an, ou un surcroît""","""taux sans risque ${dec(S.rate*100,1)} % l'an, soit <em>${dec(S.rate/4*100,1)} %</em> ce trimestre, ou un surcroît""")
e.rep("""toast(`Collatéral → <b>${o.nm}</b>${o.y?` · +${dec(o.y*100,1)} % par trimestre, ${Math.round(o.p*100)} % de risque de −${dec(o.l*100,1)} %`:''}`)""",
      """toast(`Collatéral → <b>${o.nm}</b> · ${dec((S.rate/4+colY(o))*100,1)} % ce trimestre${o.p?`, ${Math.round(o.p*100)} % de risque de −${dec(o.l*100,1)} %`:''}`)""")
e.done("lot 59 — facturation unique, collatéral variable")
# ═══════════ équilibrage (mesures dans la note de reprise) ═══════════
# Difficulté : commissions 15 / 20 / 25 % (au lieu de 30 %). Le mode difficile doit rapporter autant
# qu'au moyen à un bon gérant, avec plus de variance, et moins à un mauvais : les flux clients y sont
# amplifiés dans les deux sens (l'argent arrive aussi vite qu'il part), et les concurrents sont les plus adroits du jeu (0,12 contre 0,05 au moyen).
e=Ed()
e.rep("perf:0.30,nm:\"Difficile — 30 % de performance\"","perf:0.25,nm:\"Difficile — 25 % de performance\"")
e.rep(" En échange, vous touchez 30 % de la performance."," En échange, vous touchez 25 % de la performance, et les souscriptions arrivent aussi vite que les rachats.")
e.rep("ef:[[\"g\",\"commission de performance : 30 %\"],","ef:[[\"g\",\"commission de performance : 25 %\"],[\"g\",\"flux violents dans les deux sens : un bon trimestre attire gros\"],")
e.rep("rivSkill:0.090,rivVol:1.10,lpNeg:1.45,rcNeg:1.35,lp0:-8,flowMult:1.35,","rivSkill:0.120,rivVol:1.10,lpNeg:1.45,rcNeg:1.35,lp0:-8,flowMult:2.10,flowIn:2.10,")
e.rep("let f=Math.max(-0.06,Math.min(0.06,0.5*s*d));if(f<0)f*=SIZE().flowMult;","let f=Math.max(-0.06,Math.min(0.06,0.5*s*d));if(f<0)f*=SIZE().flowMult;else f*=(SIZE().flowIn||1);")
# Fondamental : il vivait sur le signal le plus faible (valeur, 0,08) et ses catalyseurs ne
# comptaient que double. Valeur 0,10, catalyseur ×3, réactivité aux dépêches 0,60.
e.rep("0.08*S.tcv.v[i]*((S.cat&&S.cat.includes(i))?2:1)","0.10*S.tcv.v[i]*((S.cat&&S.cat.includes(i))?CATM:1)")
e.rep("const SIGW={t:0.12,c:0.10,v:0.08};","const SIGW={t:0.12,c:0.10,v:0.10},CATM=3;")
e.rep("const cv=(S.prof==='fonda'&&S.cat&&S.cat.includes(i))?2:1;","const cv=(S.prof==='fonda'&&S.cat&&S.cat.includes(i))?CATM:1;",2)
e.rep("la valeur compte double sur un catalyseur","la valeur compte triple sur un catalyseur")
e.rep("sigBonus:4,capture:0.45,","sigBonus:4,capture:0.60,")
e.rep("réaction lente : vous ne captez que 45 % d'un mouvement en cours de trimestre","réaction mesurée : vous ne captez que 60 % d'un mouvement en cours de trimestre")
# Fondamental, deuxième passe : son desk vise 110 % de la cible (le quant 80 %, le flux 120 %),
# trois catalyseurs par trimestre au lieu de deux.
e.rep("sigBonus:4,capture:0.60,tcMult:1.08,rumBonus:0.18,lpMult:1.0,incMult:1.0,","sigBonus:4,capture:0.60,tcMult:1.08,rumBonus:0.18,lpMult:1.0,incMult:1.0,modelScale:1.10,")
e.rep(".sort((a,b)=>a.u-b.u).slice(0,2).map(o=>o.i)}",".sort((a,b)=>a.u-b.u).slice(0,3).map(o=>o.i)}")
e.rep("['b',\"coûts de transaction +8 % : vous arbitrez tard, et cher\"]]","['g',\"trois catalyseurs par trimestre, que vous seul connaissez : la valeur y compte triple\"],['b',\"votre desk vise 110 % de la vol cible : des convictions, et le risque qui va avec\"],['b',\"coûts de transaction +8 % : vous arbitrez tard, et cher\"]]")
# deux sources vérifiées par trimestre au lieu d'une, +6 sources au lieu de +4
e.rep("""   if(cand.length){const r=pick(cand);r.truth=true;r.p=0.97;r.rel='forte';r.sure=true}""",
"""   for(let n=0;n<2&&cand.length;n++){const r=cand.splice(Math.floor(rng()*cand.length),1)[0];r.truth=true;r.p=0.97;r.rel='forte';r.sure=true}""")
e.rep("sigBonus:4,capture:0.60,","sigBonus:6,capture:0.60,")
e.rep("chaque trimestre, une rumeur est recoupée par votre réseau et vous est donnée pour certaine","chaque trimestre, deux rumeurs sont recoupées par votre réseau et vous sont données pour certaines")
e.rep("+4 sources par trimestre : on vous rappelle, on vous parle","+6 sources par trimestre : on vous rappelle, on vous parle")
e.done("lot 59 — équilibrage")
