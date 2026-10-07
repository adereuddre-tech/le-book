import sys
p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
rep('.evdet{min-height:3.2em;margin-top:4px}','.evdet{min-height:3.2em;margin-top:4px;display:grid}.evdet>.pcell{grid-area:1/1;visibility:hidden}.evdet>.pcell.on{visibility:visible}')
rep(""" const pan=i=>{app.querySelectorAll('#evpan>.pcell').forEach(c=>c.classList.toggle('on',+c.dataset.p===i));
  {const o=plan[i];document.getElementById('evdet').innerHTML=`<p class="note" style="margin:0"><b>${o.b}</b> · ${o.s}</p>${o.n!==0&&o.trades.length&&o.t?bkD(o.t,0,false):''}`}
""",""" /* lot 245 : tous les détails empilés, hauteur constante quel que soit le cran */
 document.getElementById('evdet').innerHTML=plan.map((o,i)=>{const d=o.n!==0&&o.trades.length&&o.t?bkD(o.t,0,false):'';
   return `<div class="pcell" data-p="${i}"><p class="note" style="margin:0"><b>${o.b}</b> · ${o.s}</p>${d||'<p class="note dim-g" style="margin:4px 0 0">Aucun ordre : le book reste inchangé.</p>'}</div>`}).join('');
 const pan=i=>{app.querySelectorAll('#evpan>.pcell,#evdet>.pcell').forEach(c=>c.classList.toggle('on',+c.dataset.p===i));
""")
open(p,'w',encoding='utf-8').write(s)
