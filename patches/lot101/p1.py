# Lot 101 (refonte B) : tests de résistance. Plus de tirage d'accident de levier pour le joueur : six scénarios
# nommés, définis par des chocs sur les quatre facteurs ; probabilité selon la liquidité observée (pas le régime caché) ;
# quand l'un frappe, il arrive comme une dépêche majeure (mêmes mécaniques : P&L immédiat, suite binaire, confiance,
# relèvement des marges, puis contrôle de marge). Le book affiche la perte de chaque scénario.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("const TAILMG=0;",r'''const STRESS=[
 {id:'krach',nm:'Krach actions',sh:[-1.5,0,0.5,-3.0],p:"Une vente algorithmique déclenche une cascade. Les actifs risqués décrochent ensemble, les refuges montent."},
 {id:'taux',nm:'Choc de taux',sh:[-0.5,2.5,1.0,-1.0],p:"L'inflation surprend, les banques centrales reprennent la main. Obligations et actions baissent ensemble."},
 {id:'dollar',nm:'Flambée du dollar',sh:[-0.5,0,3.0,-1.0],p:"Tout le monde veut des dollars en même temps. Les émergents et les matières premières plient."},
 {id:'petrole',nm:'Choc pétrolier',sh:[-1.5,2.0,0.5,-0.5],p:"Un détroit est fermé. Le baril bondit, la croissance recule, l'inflation repart."},
 {id:'liquidite',nm:'Assèchement de liquidité',sh:[-1.0,0,1.5,-2.0],liq:1.5,p:"Les teneurs de marché se retirent. Les fourchettes s'écartent, tout ce qui est gros devient invendable."},
 {id:'squeeze',nm:'Rallye de soulagement',sh:[2.0,-0.5,-1.0,2.5],p:"La crise annoncée n'arrive pas. Les vendeurs à découvert se rachètent tous en même temps."}];
const STRESSK=1.6;
function stressHit(sc){const h={};INSTR.forEach(x=>{let v=0;for(let k=0;k<4;k++)v+=x.b[k]*sc.sh[k];v*=STRESSK;if(Math.abs(v)>=0.15)h[x.sym]=+v.toFixed(2)});return h}
function stressEv(id){const sc=STRESS.find(x=>x.id===id);if(!sc)return null;return {stress:id,t:`Scénario de stress : ${sc.nm.toLowerCase()}`,who:'Test de résistance · grandeur nature',p:sc.p,hit:stressHit(sc),...(sc.liq?{liq:sc.liq}:{})}}
function stressP(){return Math.min(0.30,0.08+0.20*Math.max(0,((S&&S.liq)||1)-0.9)/0.6)}   /* lue sur la liquidité affichée au desk */
function stressLoss(k,sc){const w=weights(k),h=stressHit(sc);let v=0;INSTR.forEach((x,i)=>{if(h[x.sym])v+=w[i]*h[x.sym]*x.sigQ});return v}   /* mouvement complet */
const TAILMG=0;''')
# le joueur n'a plus d'accident tiré au hasard (les concurrents gardent le leur)
rep("function tailP(sp,std){const e=","function tailP(sp,std){if(!std)return 0;   /* lot 101 : le joueur passe aux scénarios de stress */\n const e=")
# tirage du scénario du trimestre, inséré dans la file
rep(" if(tav.length){const te=pick(tav);S.usedTrader.push(te.t);S.evQueue.splice(Math.floor(rng()*(S.evQueue.length+1)),0,{trader:true,...te})}",
    " if(tav.length){const te=pick(tav);S.usedTrader.push(te.t);S.evQueue.splice(Math.floor(rng()*(S.evQueue.length+1)),0,{trader:true,...te})}\n {const u=prng32(hash32('stress'+S.q,S.seed));S.stressQ=null;if(u()<stressP()){const sc=STRESS[Math.floor(u()*STRESS.length)],ev=stressEv(sc.id);if(ev&&Object.keys(ev.hit).length){S.stressQ=sc.id;S.evQueue.splice(1+Math.floor(u()*S.evQueue.length),0,ev)}}}   /* lot 101 */")
rep(" if(e.stake)return {k:'stake',t:e.t};"," if(e.stress)return {k:'stress',id:e.stress};\n if(e.stake)return {k:'stake',t:e.t};")
rep(" if(g.k==='stake'){"," if(g.k==='stress')return stressEv(g.id);\n if(g.k==='stake'){")
# panneau du book
rep('  <div class="kv"><span>Risque du book · accident de levier</span><b class="${tailP(RS.total)>0?\'neg-g\':\'\'}">${pct(RS.total)} · ${tailP(RS.total)>0?dec(tailP(RS.total)*100,0)+\' %\':\'aucun\'}</b></div>',
    '  <div class="kv"><span>Risque du book</span><b>${pct(RS.total)}</b></div>')
rep("  <div class=\"kv\"><span>Perte à −2 σ trimestriels</span><b class=\"neg-g\">${sgn(-sp)} · ${moneyB(sp*S.nav)}</b></div>",
    "  <div class=\"kv\"><span>Perte à −2 σ trimestriels</span><b class=\"neg-g\">${sgn(-sp)} · ${moneyB(sp*S.nav)}</b></div>\n  <div style=\"margin-top:8px\"><div class=\"kv\"><span><b>Tests de résistance</b> · un scénario frappe ce trimestre avec une probabilité de ${Math.round(stressP()*100)} %</span><b></b></div>${tbl(STRESS.map(sc=>{const v=stressLoss(S.k,sc);return [sc.nm,`<b class=\"${v>=0?'pos-g':'neg-g'}\">${sgn(v,1)} · ${moneyB(Math.abs(v)*S.nav)}</b>`]}),['Scénario','Mouvement complet sur le book'])}<p class=\"note\" style=\"margin-top:4px\">La moitié du choc tombe tout de suite ; la suite dépend de votre réaction, comme pour une dépêche. Le prime broker relève ensuite ses marges.</p></div>")
open('index.html','w',encoding='utf-8').write(s);print('ok')
