# Lot 183 : anecdotes d'exécution, nouvelle règle (remplace le lot 182). Le risque pour le fonds revient à son niveau
# d'origine. Le gain pour vous n'est plus une baisse de coûts sur un marché (qui dépendait de la configuration) : c'est un
# gain fixe en pb de 100 M$, versé à votre société de gestion — 40 × la baisse d'origine (−35 % → +14 pb, soit 140 k$).
# Un pari raté (« gamble ») coûte la moitié du gain. Textes recalculés au chargement.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
i=s.index("/* lot 182 : anecdotes d'exécution — plus de gain pour vous, moins de risque pour le fonds */");j=s.index("/* ══════════ lot 103 : limites du comité ══════════ */",i)
s=s[:i]+r'''/* lot 183 : anecdotes d'exécution — gain fixe pour la société de gestion, risque du fonds inchangé */
const EXGAIN=40;   /* pb de 100 M$ par unité de baisse de coût d'origine */
TRADER_EXEC.forEach(ev=>(ev.ch||[]).forEach(c=>{const e=c.e||{};
 if(e.tcMult<1){const bp=Math.round(EXGAIN*(1-e.tcMult));e.gainBp=bp;delete e.tcMult;delete e.tcMultOn;
  const k=(bp*10).toFixed(0);if(c.s){c.s=c.s.replace(/Coûts −\d+ %( sur [^.:]*)?( ce trimestre)?/,`+${bp} pb pour votre société de gestion (${k} k$ sur 100 M$)`);
   if(e.gamble)c.s=c.s.replace(/coûts ×\d+(,\d+)? à la place/,`−${Math.round(bp/2)} pb à la place`)}}}));
'''+s[j:]
rep("  if(e.tcMult){let sub=0;\n","  if(e.gainBp){let g=e.gainBp*1e-4*S.aum0;if(e.gamble&&rng()<e.gamble[0]){g=-g/2;msg.push(\"Le tuyau a mal tourné.\")}S.mgrCosts-=g;S.qExGain=(S.qExGain||0)+g;refreshGain();msg.push(`${g>=0?'+':'−'}${mm(Math.abs(g))} pour votre société de gestion.`)}   /* lot 183 */\n  if(e.tcMult){let sub=0;\n")
open('index.html','w',encoding='utf-8').write(s);print('lot183 ok')
