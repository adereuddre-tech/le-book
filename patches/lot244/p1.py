# Lot 244 : réaction aux dépêches lisible au moment d'appuyer. Le panneau empilait le texte du cran, la liste des ordres et
# le tableau des scénarios, à la hauteur du plus grand des cinq crans : les boutons sortaient de l'écran. Désormais un dock
# collé en bas de l'écran (.evdock, sticky) : résumé compact du cran choisi en trois lignes (ordres et coût ; poursuite et
# retournement avec probabilité, P&L et confiance ; rentabilité et risque du book), les cinq crans et « Valider ».
# Le texte complet du cran et la liste des ordres s'affichent au-dessus, hors du dock (#evdet).
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
rep("""     return `<div class="evpan" id="evpan"></div>
     <div class="evsel">""","""     return `<div id="evdet" class="evdet"></div><div class="evdock"><div class="evpan" id="evpan"></div>
     <div class="evsel">""")
rep("""     <button class="cta" id="evok" style="margin-top:10px">Valider</button>`})()}""","""     <button class="cta" id="evok" style="margin-top:8px">Valider</button></div>`})()}""")
rep(""" document.getElementById('evpan').innerHTML=plan.map((o,i)=>`<div class="pcell" data-p="${i}"><div class="choice evopt" data-i="${i}" style="cursor:default"><b>${o.b}</b><span class="evs">${o.s}${o.n!==0&&o.trades.length&&o.t?bkD(o.t,0,false):''}${o.ban?' <b class="neg-g">interdit par le comité (carton rouge)</b>':''}</span>${ptab(o)}</div></div>`).join('');   /* lot 224 */
 const pan=i=>{app.querySelectorAll('#evpan>.pcell').forEach(c=>c.classList.toggle('on',+c.dataset.p===i));""",
""" /* lot 244 : résumé compact dans le dock, détail au-dessus */
 const R0=riskShown(weights(S.k)).total,P0=profitBook(S.k);
 const sline=(o,s)=>`<div class="dkr"><span>${['Poursuite','Retournement'][s]} <b>${Math.round(PR[s]*100)} %</b></span><span class="${o.pay[s]>0?'pos-g':o.pay[s]<0?'neg-g':'dim-g'}">${uNum(o.pay[s]*S.nav,UM)} ${unitLab}</span><span>conf. ${gcell(o.gz[s].lp)}</span></div>`;
 document.getElementById('evpan').innerHTML=plan.map((o,i)=>{const dp=o.n!==0&&o.trades.length?profitBook(o.t)-P0:0,dr=o.n!==0&&o.trades.length?(riskShown(weights(o.t)).total-R0)*100:0;
   return `<div class="pcell" data-p="${i}"><div class="evopt evdk" data-i="${i}"><div class="dkh"><b>${o.b}</b><span class="${o.cost>0?'neg-g':'dim-g'}">${o.n===0?'aucun ordre':o.trades.length?'ordres −'+mm(o.cost):'aucun ordre possible'}</span></div>
    ${sline(o,0)}${sline(o,1)}<div class="dkr dkm"><span>rentabilité ${pc2(dp)}</span><span>risque <b class="${dr>0.05?'neg-g':dr<-0.05?'pos-g':'dim-g'}">${dr>=0?'+':'−'}${dec(Math.abs(dr),1)} pt</b></span>${o.ban?'<span class="neg-g">carton rouge : interdit</span>':''}</div></div></div>`}).join('');
 const pan=i=>{app.querySelectorAll('#evpan>.pcell').forEach(c=>c.classList.toggle('on',+c.dataset.p===i));
  {const o=plan[i];document.getElementById('evdet').innerHTML=`<p class="note" style="margin:0"><b>${o.b}</b> · ${o.s}</p>${o.n!==0&&o.trades.length&&o.t?bkD(o.t,0,false):''}`}""")
rep(".evs{display:block;color:var(--dim);font-size:12.5px}",""".evs{display:block;color:var(--dim);font-size:12.5px}
.evdock{position:sticky;bottom:0;z-index:5;background:var(--ink);padding:8px 0 10px;margin-top:8px;border-top:1px solid var(--line);box-shadow:0 -10px 18px rgba(0,0,0,.35)}
.evdet{min-height:3.2em;margin-top:4px}
.evdk{background:var(--panel2);border:1px solid var(--line);border-radius:7px;padding:8px 10px;font-size:12.5px}
.dkh{display:flex;justify-content:space-between;gap:8px;margin-bottom:4px}.dkh b{color:var(--txt)}.dkh span{font-family:var(--mono);white-space:nowrap}
.dkr{display:grid;grid-template-columns:1.3fr 1fr .8fr;gap:6px;font-family:var(--mono);font-size:12px;color:var(--dim);white-space:nowrap}
.dkr span:nth-child(2),.dkr span:nth-child(3){text-align:right}
.dkm{grid-template-columns:1fr 1fr;margin-top:3px;padding-top:3px;border-top:1px solid var(--line)}""")
open('index.html','w',encoding='utf-8').write(s);print('lot244 ok')
