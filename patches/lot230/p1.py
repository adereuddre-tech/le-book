# Lot 230 : les idées de trade des traders (Tuco, Ingrid, Boris, Winnie, Marie-Alpha…) ont raison plus d'une fois sur deux.
# Quand un trader propose une position à pile ou face (gamble2, chance ≤ 55 %, gain positif, position prise dans le sens
# de son idée), sa chance est tirée à chaque apparition dans [55 % ; 70 %] (loi uniforme) ; texte et pastille suivent.
# Exceptions : le stagiaire Jean-Kevin, et l'option « contrarien » qui prend le contre-pied de l'idée.
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
rep("function screenTraderEvent(ev,next){\n next=next||stepEvents;ev=cast(ev);",
"""function screenTraderEvent(ev,next){
 next=next||stepEvents;ev=cast(ev);
 /* lot 230 : idée de trade d'un trader, chance tirée dans [55 % ; 70 %] */
 ev=Object.assign({},ev,{ch:(ev.ch||[]).map(c=>{const e=c.e||{};
  if(!(e.gamble2&&e.gamble2[0]<=0.55&&e.gamble2[1]>0&&(e.kAdd||e.kAddAbs||e.kContra||(e.trendAdd||0)>0)&&!/Jean-Kevin/.test(ev.who||'')))return c;
  const p0=e.gamble2[0],p=Math.round((0.55+0.15*rng())*100)/100,P=Math.round(p*100);
  const s2=c.s.replace(/(\\d+) % de ±([\\d,]+) %/,(m,a,b)=>`${P} % de chances de +${b} %, sinon −${b} %`).replace(new RegExp('\\\\b'+Math.round(p0*100)+' %'),P+' %');
  return Object.assign({},c,{s:s2,e:Object.assign({},e,{gamble2:[p,e.gamble2[1],e.gamble2[2]]})})})});""")
open('index.html','w',encoding='utf-8').write(s);print('lot230 ok')
# … et le texte dit la chance effective (bonus d'équipe compris, lot 223), comme la pastille : chaque probabilité
# tirée au sort citée en % dans le texte est remplacée par sa valeur ajustée.
s=open("index.html",encoding="utf-8").read()
rep("function fxTxt(s,x){",
"""function effTxt(s,e){if(typeof s!=='string'||!e)return s;   /* lot 230 */
 const sub=(p0,good)=>{const a=Math.round(p0*100),b=Math.round(pAdj(p0,good)*100);if(a!==b)s=s.replace(new RegExp('(^|[^\\\\d,])'+a+' %'),(m,c)=>c+b+' %')};
 if(e.gamble2)sub(e.gamble2[0],e.gamble2[1]>=0);if(e.gambleLp)sub(e.gambleLp[0],e.gambleLp[1]>=0);
 if(e.gamble)sub(e.gamble[0],false);if(e.risk)sub(e.risk[0],riskGood(e));return s}
function fxTxt(s,x){s=effTxt(s,x);""")
open('index.html','w',encoding='utf-8').write(s);print('lot230b ok')
# … et la conversion des baisses de coûts des anecdotes d'exécution (lot 183) n'avale plus la suite de la phrase :
# « Coûts −25 % sur tout le trimestre, 25 % de risque de bogue » perdait « 25 % de risque de bogue ».
s=open("index.html",encoding="utf-8").read()
rep("c.s=c.s.replace(/Coûts −\\d+ %( sur [^.:]*)?( ce trimestre)?/,","c.s=c.s.replace(/Coûts −\\d+ %( sur [^.:,]*)?( ce trimestre)?/,")
open('index.html','w',encoding='utf-8').write(s);print('lot230c ok')
