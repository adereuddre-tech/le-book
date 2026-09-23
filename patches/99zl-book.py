# -*- coding: utf-8 -*-
"""Lot 50 — difficile à 30 %, drapeaux et symboles dans le book, ruban cohérent et plus
rapide, sanction lourde d'un risque ex-ante au double de la cible.

  - Difficile : commission de performance 30 % (au lieu de 25).
  - Book : un drapeau (pays) ou un pictogramme (matière, actif exotique) devant chaque marché,
    un symbole par classe d'actifs dans l'en-tête de section (📜 actions, % taux, 💱 devises,
    ⛏️ matières premières, 🧪 exotiques).
  - Ruban contre tuile « Perf. » (sonde `tools/tapeprobe.js`, 9 parties, 1 253 rendus :
    174 écarts, jusqu'à 2 points). Cause : entre la clôture et le lancement du trimestre
    suivant (écrans d'exécution et d'annonce), la phase vaut déjà 'events' mais le trimestre
    n'a pas commencé ; `evIdx` garde la valeur du trimestre précédent, `qElapsed()` renvoie
    ≈ 1, et la tuile affichait le P&L latent d'un trimestre entier AVANT qu'il ait lieu —
    le ruban, lui, n'avançait pas. `qElapsed()` vaut désormais 0 tant que le trimestre n'est
    pas lancé, et la tuile n'ajoute le latent qu'une fois lancé.
  - Tracé du grand ruban (mi-parcours, clôture) en 3 s au lieu de 5 ; révélation et cartes
    alignées sur 3 s.
  - Comité : un book dont le risque affiché dépasse le double de la cible (40 pour 20) était
    sanctionné à la validation, mais la sanction était bornée à −15 par `gauge()`. À la clôture,
    le comité sanctionne désormais lourdement : −10 − 40 × (risque/cible − 2), borné à −40, et
    les investisseurs −4 (le rapport de risque circule). Un avertissement l'annonce dans le book.
  - Correctif : la « médiane » des concurrents prenait l'indice 2 d'une liste de trois (le
    meilleur, depuis le lot 46) ; c'est l'indice 1.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
e.rep("{id:'mega',lvl:'Expert',nav:0.1,capX:1,perf:0.25,nm:\"Difficile — 25 % de performance\"",
      "{id:'mega',lvl:'Expert',nav:0.1,capX:1,perf:0.30,nm:\"Difficile — 30 % de performance\"")
e.rep("En échange, vous touchez 25 % de la performance.","En échange, vous touchez 30 % de la performance.")
e.rep('ef:[["g","commission de performance : 25 %"],','ef:[["g","commission de performance : 30 %"],')
e.rep("et la commission de performance que vous touchez : 15, 20 ou 25 %.","et la commission de performance que vous touchez : 15, 20 ou 30 %.")
# ── drapeaux et symboles ────────────────────────────────────────────────────────
e.rep("function drawRows(){","""/* Drapeau du pays ou pictogramme de la matière, symbole de la classe d'actifs. */
const MFLAG={ES:'🇺🇸',NQ:'🇺🇸',ESTX:'🇪🇺',TOPX:'🇯🇵',MXEF:'🌏',TN:'🇺🇸',GBL:'🇩🇪',JGB:'🇯🇵',R:'🇬🇧',OAT:'🇫🇷',
 EUR:'🇪🇺',JPY:'🇯🇵',GBP:'🇬🇧',AUD:'🇦🇺',MXP:'🇲🇽',GC:'🥇',CL:'🛢️',ZW:'🌾',HG:'🔶',KC:'☕',BTC:'🪙',VX:'🌪️',EUA:'🏭',BDI:'🚢',NRAM:'🌧️'};
const CSYM={'Actions':'📜','Taux':'%','Devises':'💱','Matières premières':'⛏️','Exotiques':'🧪'};
function drawRows(){""")
e.rep("""  h+=`<div class="sect"><i style="background:${GRPC[g]}"></i><span>${g.toUpperCase()}</span></div>`;""",
      """  h+=`<div class="sect"><i style="background:${GRPC[g]}"></i><b class="csym">${CSYM[g]||''}</b><span>${g.toUpperCase()}</span></div>`;""")
e.rep("""      <span class="nm">${x.nm}<span class="crowd" style="background:${cc}"></span>""",
      """      <span class="nm"><span class="mflag">${MFLAG[x.sym]||''}</span>${x.nm}<span class="crowd" style="background:${cc}"></span>""")
e.rep(".lvls{display:grid;",".mflag{margin-right:5px;font-size:13px}\n.csym{font-family:var(--mono);font-size:12px;color:var(--txt);margin:0 6px 0 2px;font-weight:700}\n.lvls{display:grid;")
# ── ruban : rien de latent avant le lancement du trimestre ─────────────────────
e.rep("function qElapsed(){const n=(S.evQueue||[]).length||1;",
      "function qElapsed(){if(!S.live)return 0;   /* lot 50 : avant le lancement, le trimestre n'a pas commencé */\n const n=(S.evQueue||[]).length||1;")
e.rep(" const lat=(S.phase==='events'&&typeof liveRet==='function')?liveRet():0;",
      " const lat=(S.phase==='events'&&S.live&&typeof liveRet==='function')?liveRet():0;")
# ── tracé en 3 s ───────────────────────────────────────────────────────────────
e.rep("anim:1,draw:5,zero:1,","anim:1,draw:3,zero:1,",k=2)
e.rep(".thold{opacity:0;pointer-events:none;animation:evshow .6s ease-out 5s forwards}",".thold{opacity:0;pointer-events:none;animation:evshow .5s ease-out 3s forwards}")
e.rep(" goldFlush(5600);"," goldFlush(3500);")
# ── comité : risque au double de la cible ──────────────────────────────────────
e.rep(" const med=[...S.rivals.map(x=>x.last)].sort((a,b)=>a-b)[2];",
      " const med=(()=>{const v=S.rivals.map(x=>x.last).sort((a,b)=>a-b),n=v.length;return n%2?v[n>>1]:(v[n/2-1]+v[n/2])/2})();   /* vraie médiane, quel que soit le nombre de concurrents */")
e.rep(" if(sp>1e-6&&gross<-2.2*sp/2)rcD.push(['Perte au-delà de 2,2 σ ex-ante',-10]);",
      " const rsx=riskShown(wFin).total/Math.max(1e-9,S.tgt);\n"
      " if(rsx>2)rcD.push([`Risque ex-ante à ${dec(rsx,1)} fois la cible`,-Math.min(40,10+40*(rsx-2))]);\n"
      " if(sp>1e-6&&gross<-2.2*sp/2)rcD.push(['Perte au-delà de 2,2 σ ex-ante',-10]);")
e.rep(" if(S.budBp>70)lpD.push(","  if(riskShown(wFin).total>2*S.tgt)lpD.push(['Le rapport de risque circule : book au double de la cible',-4]);\n if(S.budBp>70)lpD.push(")
e.rep(" if(sp>S.tgt*(1+band))flags+=`<div class=\"flag\"><span>Vol ex-ante ${pct(sp)}",
      " if(sp>2*S.tgt)flags+=`<div class=\"flag\" style=\"border-color:var(--short)\"><span><b>Risque au double de la cible.</b> À la clôture, le comité sanctionnera lourdement (jusqu'à −40) et les investisseurs l'apprendront.</span></div>`;\n"
      " else if(sp>S.tgt*(1+band))flags+=`<div class=\"flag\"><span>Vol ex-ante ${pct(sp)}")

# ── le ruban couvre tout le mandat : il dit la même chose que la tuile « Perf. », qui compte
#    depuis le lancement (en deuxième année, « +2 % depuis janvier » contre « +28 % » en haut) ──
e.rep("function ytdIdx(){\n const y0=Math.floor(S.q/4)*4;let v=1;","function ytdIdx(){\n const y0=0;let v=1;   /* lot 50 : base 100 au lancement du fonds */")
e.rep("  const y0=Math.floor((S.q)/4)*4;let base=1;for(let i=0;i<y0;i++)base*=(1+S.rets[i]);\n  const tgt=S.idx/Math.max(1e-9,base)*100",
      "  const base=1;\n  const tgt=S.idx/Math.max(1e-9,base)*100")
e.rep("ICI · DEPUIS JANVIER</span>","ICI · DEPUIS LE LANCEMENT</span>")
e.rep("<span>LE TRIMESTRE · DEPUIS JANVIER</span>","<span>LE TRIMESTRE · DEPUIS LE LANCEMENT</span>")
e.rep("<span>P&amp;L DU FONDS · ANNÉE ${1+Math.floor(S.q/4)}</span>","<span>P&amp;L DU FONDS · DEPUIS LE LANCEMENT</span>")

# badge de marché fermé : court, pour tenir sur la ligne à 380 px ; la phrase complète en info-bulle
e.rep("""${mktOpen(i)?'':`<span class="capb">${x.grp==='Exotiques'&&x.rk<=OPENRK?'fermé · finissez un trimestre premier':`fermé · s'ouvre à ${mm(unlockNav(x.rk))}`}</span>`}""",
      """${mktOpen(i)?'':(x.grp==='Exotiques'&&x.rk<=OPENRK?`<span class="capb" title="S'ouvre la première fois que vous finissez premier d'un trimestre">🔒 1er d'un trimestre</span>`:`<span class="capb" title="S'ouvre quand l'encours atteint ${mm(unlockNav(x.rk))}">🔒 ${mm(unlockNav(x.rk))}</span>`)}""")
e.done("lot 50 — difficile a 30 %, drapeaux, ruban coherent en 3 s, sanction du risque")
