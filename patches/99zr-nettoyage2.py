# -*- coding: utf-8 -*-
"""Lot 56 — nettoyage, deuxième passe (budget, annonce, exécution, dépêches) et retour des
expositions factorielles dans le book.

Book — une ligne par marché, pensée avec le reste :
    SYM  🇺🇸 Nom                              dernier rendement
    [ −5 … +5 ]
    C++ I− D+ A++        unité +1,0 %   risque +6,1 pt        ← qui : expositions / ce que ça rapporte / ce que ça pèse
    achat 46,6 M$ · coût 5,2 k$                               ← seulement s'il y a un ordre
    Tendance ▲▲ · Portage ▲▲▲ · Valeur ▲   ⚡   détails ›
  Les expositions (C, I, D, A : croissance, inflation, dollar, appétit ; + à +++ / − à −−−)
  reprennent leur place à gauche ; le facteur que vous survolez dans la barre reste surligné.

Budget : l'intro tient en une ligne ; la description de chaque poste passe dans le repli, avec
  les sept crans (« À quoi sert ce budget · les sept crans »). Le contrôle des risques n'« achète »
  plus la confiance du comité (il n'a plus de jauge) : il évite les incidents, élargit la bande
  de volatilité et apaise les griefs.
Annonce : une ligne d'intro avec l'attendu du book ; chaque option dit ce qu'elle promet, ce
  qu'elle rapporte ou coûte en confiance, et — en facile et en moyen — la chance de la tenir
  d'après votre attendu (Φ((attendu − promesse)/σ)). Les longues descriptions sont retirées.
Exécution : un seul bandeau (ordres à votre charge · impact pour le fonds) ; trésorerie, liquidité
  et taux passent dans le détail. Les enjeux des options étaient écrits en <b>, que les boutons
  affichent en bloc : chaque montant partait sur sa ligne. Ils passent en ligne.
Dépêches : « Effets » n'apparaît plus quand il ne se passe rien ; colonnes « Confiance » et « ⚖️ » ;
  le minuteur est plus compact ; le résultat ne répète plus son titre en première phrase.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
# ── book : expositions à gauche, rendement et risque à droite, ordre en dessous ─────
e.rep("""  gl=`<span class="xk">unité</span> ${expShort(g)}${(S.size||'mid')==='small'?`<span class="dim-g"> ±${dec(2*g.s*100,1)}</span>`:''} <span class="xk" style="margin-left:8px">${S.k[i]?'risque':'+1'}</span> <span class="${rp>0.05?'neg-g':rp<-0.05?'pos-g':'dim-g'}">${rp>=0?'+':'−'}${dec(Math.abs(rp),1)} pt</span>`}""",
      """  gl=`<span class="xk">unité</span>${expShort(g)}${(S.size||'mid')==='small'?`<span class="dim-g"> ±${dec(2*g.s*100,1)}</span>`:''}<span class="xk" style="margin-left:7px">${S.k[i]?'risque':'+1'}</span><span class="${rp>0.05?'neg-g':rp<-0.05?'pos-g':'dim-g'}">${rp>=0?'+':'−'}${dec(Math.abs(rp),1)} pt</span>`}
 /* expositions aux quatre facteurs : le facteur survolé dans la barre reste surligné */
 const ex=x.b.map((b,k)=>{const a=Math.abs(b),hot=S.hotFactor===k?';text-decoration:underline':'';
   if(a<0.15)return `<b style="color:var(--dimmer)${hot}">${FACT[k].id}0</b>`;
   const n=a>=0.55?3:a>=0.32?2:1;return `<b style="color:${b>0?'var(--long)':'var(--short)'}${hot}">${FACT[k].id}${(b>0?'+':'−').repeat(n)}</b>`}).join(' ');""")
e.rep(""" else right='<span style="color:var(--dimmer)">sans ordre</span>';
 el.innerHTML=`<span class="fx">${gl}</span><span>${right}</span>`;""",
      """ else right='';
 el.innerHTML=`<span class="fxe">${ex}</span><span class="fx">${gl}</span>${right?`<span class="ord">${right}</span>`:''}`;""")
e.rep("  if(gx.lp||gx.rc)out.push(gz(gx.lp,gx.rc));","  if(gx.lp||gx.rc)out.push(`<span class=\"stk\">${gz(gx.lp,gx.rc)}</span>`);")
e.rep(".lvls{display:grid;",".rowinfo .fx{white-space:nowrap}.rowinfo .fxe{white-space:nowrap}\n.rowinfo{font-size:10px!important}\n.stks b{display:inline!important;margin:0!important;font-size:inherit!important}\n.commrow b i{font-style:normal}\n.fxe b{font-weight:600;margin-right:1px}\n.rowinfo .ord{flex-basis:100%;color:var(--dim)}\n.lvls{display:grid;")
# ── budget ─────────────────────────────────────────────────────────────────────
e.rep("""   <p class="note" style="margin-top:0">Ces dépenses sortent de <em>votre poche de gérant</em> : elles viennent en déduction de vos gains, pas de la performance du fonds. Vous ne pouvez engager que ce que votre société a en caisse — les commissions encaissées, moins ce que vous avez déjà payé. Un point de base vaut <em>${(S.nav*100).toFixed(0)} k$</em>.</p>""",
      """   <p class="note" style="margin-top:0">Payé de votre poche, pas par le fonds, dans la limite de votre trésorerie. 1 pb = <em>${(S.nav*100).toFixed(0)} k$</em>.</p>""")
e.rep("""<span>${b.lv[S.bud[b.id]].bp} pb · ${mm(b.lv[S.bud[b.id]].bp*1e-4*S.nav)}</span></div><p>${b.d}</p>""",
      """<span>${b.lv[S.bud[b.id]].bp} pb · ${mm(b.lv[S.bud[b.id]].bp*1e-4*S.nav)}</span></div>""")
e.rep("""<details style="margin-top:8px"><summary>Les sept crans</summary><ul class="efl">""",
      """<details style="margin-top:8px"><summary>À quoi sert ce budget · les sept crans</summary><p class="note">${b.d}</p><ul class="efl">""")
e.rep("Un contrôle sérieux évite les incidents et, surtout, achète la confiance du comité : mieux vous êtes tenu, plus large est la bande de volatilité qu'on vous laisse.",
      "Un contrôle sérieux évite les incidents, élargit la bande de volatilité que le comité vous laisse, et apaise ses griefs — moins de cartons.")
# ── annonce ────────────────────────────────────────────────────────────────────
e.rep("""<h2>Ce que vous annoncez</h2><span class="hint">investisseurs et comité</span></div>
   <p class="note" style="margin-top:0">Avant l'exécution, vous rencontrez les investisseurs et le comité des risques. Que promettez-vous pour ce trimestre ? Touchez votre réponse, elle est validée aussitôt.</p>""",
      """<h2>Ce que vous annoncez</h2><span class="hint">aux investisseurs</span></div>
   <p class="note" style="margin-top:0">Touchez votre promesse : elle se solde à la clôture, sur le résultat tout compris.</p>
   ${S.tcvEst?`<div class="kv"><span>Votre attendu pour ce book</span><b>${expShort(expBook(S.k))}</b></div>`:''}""")
e.rep("""   <div class="who">${o.who}</div><b><span class="commico">${o.ico}</span>${o.nm}</b><p>${o.p}</p>""",
      """   <div class="who">${o.who}</div><b><span class="commico">${o.ico}</span>${o.nm}</b>""")
e.rep("""    :`<div class="commrow"><span>Vous promettez pour ce trimestre</span><b>au moins ${sgnp(o.ret,1)} · ${mm(o.ret*S.nav)}</b></div>
      <div class="commrow"><span>Si c'est tenu</span><b class="pos-g">investisseurs et comité +${o.win.lp}</b></div>
      <div class="commrow"><span>Si c'est manqué</span><b class="neg-g">investisseurs et comité −${-o.lose.lp}</b></div>`}""",
      """    :`<div class="commrow"><span>Vous promettez</span><b>au moins ${sgnp(o.ret,1)} · ${mm(o.ret*S.nav)}</b></div>
      <div class="commrow"><span>Tenu · manqué</span><b>confiance <i class="pos-g">+${o.win.lp}</i> · <i class="neg-g">−${-o.lose.lp}</i></b></div>
      ${S.tcvEst&&(S.size||'mid')!=='mega'?(()=>{const b=expBook(S.k),z=b.s>0?(b.m-o.ret)/b.s:0,p=1/(1+Math.exp(-1.702*z));
        return `<div class="commrow"><span>Chance de tenir, d'après votre attendu</span><b>${Math.round(p*100)} %</b></div>`})():''}`}""")
e.rep("""<b class="dim-g">investisseurs et comité inchangés</b>""","""<b class="dim-g">rien ne bouge</b>""")
e.rep("""  <p class="note">L'annonce ne change rien tout de suite : elle se solde à la fin du trimestre, sur le résultat tout compris, commissions et coûts déduits.</p></div>`;""","""  </div>`;""")
# ── exécution ──────────────────────────────────────────────────────────────────
e.rep("""   ${orders.length?`<div class="kv"><span>Coût total des ordres, à votre charge</span><b class="neg-g">${mm(tot)} · ${(tot/S.nav*1e4).toFixed(0)} pb de l'encours</b></div>
   <div class="kv"><span>Impact de marché estimé, payé par le fonds</span><b class="neg-g">${mm(Math.abs(execImpactAmt(tot,1,S.leakQ)))} · ${(Math.abs(execImpactAmt(tot,1,S.leakQ))/S.nav*1e4).toFixed(0)} pb de l'encours</b></div>
   <div class="kv"><span>Trésorerie de votre société après paiement</span><b class="${(mgrCash())>=0?'':'neg-g'}">${mm(mgrCash())}</b></div>
   <p class="note" style="margin:8px 0 0">${orders.length} marché${orders.length>1?'s':''} à travailler, liquidité ${lqNm} (×${dec(S.liq,2)}), taux au jour le jour ${dec((S.rate*100),1)} %. Le desk a son mot à dire sur la manière de faire.</p>`""",
      """   ${orders.length?`<div class="kv"><span>Ordres, à votre charge</span><b class="neg-g">${mm(tot)}</b></div>
   <div class="kv"><span>Impact de marché, pour le fonds</span><b class="neg-g">${mm(Math.abs(execImpactAmt(tot,1,S.leakQ)))}</b></div>`""")
e.rep("""   ${orders.length?`<details style="margin-top:10px"><summary>Détail des ordres et des coûts, marché par marché</summary>
    <div class="wire" style="margin-top:8px">""",
      """   ${orders.length?`<details style="margin-top:10px"><summary>Détail des ordres et des coûts</summary>
    <p class="note" style="margin:8px 0 0">${orders.length} marché${orders.length>1?'s':''} à travailler · liquidité ${lqNm} (×${dec(S.liq,2)}) · taux au jour le jour ${dec((S.rate*100),1)} % · trésorerie après paiement ${mm(mgrCash())} · ordres ${(tot/S.nav*1e4).toFixed(0)} pb, impact ${(Math.abs(execImpactAmt(tot,1,S.leakQ))/S.nav*1e4).toFixed(0)} pb de l'encours.</p>
    <div class="wire" style="margin-top:8px">""")
e.rep("""   if(Math.abs(d)>=1e-9)out.push(`<b class="${d<0?'pos-g':'neg-g'}">${d<0?'−':'+'}${mm(Math.abs(d))}</b> sur les ordres${x.tcMultOn?'':', même tarif sur vos ajustements'}`);""",
      """   if(Math.abs(d)>=1e-9)out.push(`<span class="stk">ordres <em class="${d<0?'pos-g':'neg-g'}">${d<0?'−':'+'}${mm(Math.abs(d))}</em></span>`);""")
e.rep("""  if(im)out.push(`<b class="neg-g">${mm(Math.abs(im))}</b> d'impact de marché pour le fonds`);""",
      """  if(im)out.push(`<span class="stk">impact fonds <em class="neg-g">−${mm(Math.abs(im))}</em></span>`);""")
e.rep("""  return out.length?' '+out.join(' · '):''};""","""  return out.length?`<span class="stks">${out.join('')}</span>`:''};""")
e.rep(".lvls{display:grid;",".stks{display:flex;flex-wrap:wrap;gap:4px 12px;margin-top:5px;font-family:var(--mono);font-size:11.5px;color:var(--dimmer)}.stks em{font-style:normal;font-weight:600}\n.lvls{display:grid;")
# ── dépêches ───────────────────────────────────────────────────────────────────
e.rep("""   <div class="kv nowrp"><span>Effets</span><b>${gz(S.evImmG.lp,S.evImmG.rc,'always')}</b></div>""",
      """   ${(Math.abs(S.evImmG.lp||0)>=0.05||Math.abs(S.evImmG.rc||0)>=0.5)?`<div class="kv nowrp"><span>Effets</span><b>${gz(S.evImmG.lp,S.evImmG.rc)}</b></div>`:''}""")
e.rep("""<span class="ph pn">Invest.</span><span class="ph pn">Comité</span>""","""<span class="ph pn">Confiance</span><span class="ph pn">⚖️</span>""")
e.rep("[`<b>${scName}</b> ${flav} ${what}`","[`${flav} ${what}`")
e.rep("<span class=\"tlb\">Sans décision de votre part, l'option du bas sera retenue.</span>","<span class=\"tlb\">sans choix : l'option du bas</span>")
e.rep(".lvls{display:grid;",".evtimer{padding:5px 10px 5px 5px!important}.evtimer .tdial{transform:scale(.72);transform-origin:left center;margin-right:-14px}.evtimer .tlb{font-size:10.5px!important;max-width:120px}\n.lvls{display:grid;")
e.done("lot 56 — nettoyage (budget, annonce, execution, depeches), expositions dans le book")
