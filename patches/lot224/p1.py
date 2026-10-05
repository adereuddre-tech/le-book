# Lot 224 : dépêches, rivalité, accident — le panneau de détail garde la même hauteur quel que soit le cran : tous les
# panneaux sont posés dans la même cellule (grille), seul celui du cran choisi est visible ; la hauteur est celle du
# plus grand. Ligne « rentabilité · risque » insécable. Résultat d'une dépêche : la liste chiffrée des ordres
# (« ES 0 → −1 (46,9 M$, 15 k$) ; … ») est retirée, elle figure déjà dans le détail.
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
rep(".evstep:disabled{opacity:.35}",".evstep:disabled{opacity:.35}\n.evpan{display:grid}.evpan>.pcell{grid-area:1/1;visibility:hidden}.evpan>.pcell.on{visibility:visible}\n.bkd .nw{white-space:nowrap}")
rep("""const pan=i=>{const o=plan[i];document.getElementById('evpan').innerHTML=`<div class="choice evopt" data-i="${i}" style="cursor:default"><b>${o.b}</b><span class="evs">${o.s}${o.n!==0&&o.trades.length&&o.t?bkD(o.t,0,false):''}${o.ban?' <b class="neg-g">interdit par le comité (carton rouge)</b>':''}</span>${ptab(o)}</div>`;
  app.querySelectorAll('.evstep').forEach(b=>b.classList.toggle('on',+b.dataset.i===i));sel=i};""",
"""document.getElementById('evpan').innerHTML=plan.map((o,i)=>`<div class="pcell" data-p="${i}"><div class="choice evopt" data-i="${i}" style="cursor:default"><b>${o.b}</b><span class="evs">${o.s}${o.n!==0&&o.trades.length&&o.t?bkD(o.t,0,false):''}${o.ban?' <b class="neg-g">interdit par le comité (carton rouge)</b>':''}</span>${ptab(o)}</div></div>`).join('');   /* lot 224 */
 const pan=i=>{app.querySelectorAll('#evpan>.pcell').forEach(c=>c.classList.toggle('on',+c.dataset.p===i));
  app.querySelectorAll('.evstep').forEach(b=>b.classList.toggle('on',+b.dataset.i===i));sel=i};""")
rep("""let sel='none';const pan=a=>{document.getElementById('rvpan').innerHTML=`<div class="choice" style="cursor:default">${RP[a]}</div>`;""",
"""let sel='none';document.getElementById('rvpan').innerHTML=Object.keys(RP).map(a=>`<div class="pcell" data-p="${a}"><div class="choice" style="cursor:default">${RP[a]}</div></div>`).join('');   /* lot 224 */
 const pan=a=>{app.querySelectorAll('#rvpan>.pcell').forEach(c=>c.classList.toggle('on',c.dataset.p===a));""")
rep("""let sel=CUT;const pan=k=>{const o=O[k];document.getElementById('tlpan').innerHTML=`<div class="choice" style="cursor:default"><b>${LAB[o.id]}</b><span>${body(o)}</span></div>`;""",
"""let sel=CUT;document.getElementById('tlpan').innerHTML=O.map((o,k)=>`<div class="pcell" data-p="${k}"><div class="choice" style="cursor:default"><b>${LAB[o.id]}</b><span>${body(o)}</span></div></div>`).join('');   /* lot 224 */
 const pan=k=>{app.querySelectorAll('#tlpan>.pcell').forEach(c=>c.classList.toggle('on',+c.dataset.p===k));""")
rep("""${ch.length?`<span>rentabilité ${pc2(dp)} · risque""","""${ch.length?`<span class="nw">rentabilité ${pc2(dp)} · risque""")
rep("[o.n]||'suivez le mouvement'} : ${tr}.","[o.n]||'suivez le mouvement'}.")
open('index.html','w',encoding='utf-8').write(s);print('lot224 ok')
