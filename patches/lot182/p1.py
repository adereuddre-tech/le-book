# Lot 182 : anecdotes d'exécution rééquilibrées. L'option qui allège vos ordres coûtait souvent bien plus au fonds qu'elle ne
# vous faisait gagner (−35 % sur un marché, contre 30 % de risque de −0,25 % sur tout le fonds). Désormais : baisse des coûts
# ×1,5 (plafonnée à −60 %), risque pour le fonds ÷5. Textes recalculés à partir des valeurs.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("/* ══════════ lot 103 : limites du comité ══════════ */",r'''/* lot 182 : anecdotes d'exécution — plus de gain pour vous, moins de risque pour le fonds */
TRADER_EXEC.forEach(ev=>(ev.ch||[]).forEach(c=>{const e=c.e||{};
 if(e.tcMult<1){const nt=Math.max(0.4,1-(1-e.tcMult)*1.5);e.tcMult=+nt.toFixed(2);if(c.s)c.s=c.s.replace(/Coûts −\d+ %/,'Coûts −'+Math.round((1-e.tcMult)*100)+' %')}
 if(Array.isArray(e.risk)&&e.risk[1]<0){e.risk=[e.risk[0],e.risk[1]/5];if(c.s)c.s=c.s.replace(/−\d+,\d+ %/,'−'+(Math.abs(e.risk[1])*100).toFixed(2).replace('.',',')+' %')}}));
/* ══════════ lot 103 : limites du comité ══════════ */''')
open('index.html','w',encoding='utf-8').write(s);print('lot182 ok')
