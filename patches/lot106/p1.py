# Lot 106 : les « scénarios de stress » deviennent des événements extrêmes. Cadre rouge clignotant ; les concurrents
# encaissent aussi le choc ; l'événement peut s'annoncer par une rumeur (plus souvent avec une recherche renforcée, avec
# de fausses alertes) et par le pouvoir de chaque style : source vérifiée du fondamental (nomme l'événement), modèle de
# risque du quant (nomme l'événement et chiffre la perte du book), intuition du flux (sent qu'un choc arrive, sans le nommer).
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
# 1. vocabulaire
rep("Scénario de stress : ${sc.nm.charAt(0).toLowerCase()+sc.nm.slice(1)}","Événement extrême : ${sc.nm.charAt(0).toLowerCase()+sc.nm.slice(1)}")
rep("who:sc.ext?'Scénario extrême · grandeur nature':'Test de résistance · grandeur nature',p:sc.p,","who:sc.ext?'Événement extrême · le plus rare':'Événement extrême',x:true,p:sc.p,")
for a,b,k in [("scénarios de stress","événements extrêmes",5),("scénario de stress","événement extrême",3),("choc de stress","choc des extrêmes",1),("chocs de stress","chocs extrêmes",1)]:rep(a,b,k)
rep("<b>Tests de résistance</b> · un scénario frappe ce trimestre avec une probabilité de","<b>Événements extrêmes</b> · l'un d'eux frappe ce trimestre avec une probabilité de")
rep("Les ${L.length-6} autres scénarios","Les ${L.length-6} autres événements")
rep("Le comité, lui, sort ses cartons sur les pertes et les replis.","Une rumeur, et le pouvoir de votre style, peuvent les annoncer. Le comité, lui, juge ses limites.")
# 2. cadre rouge clignotant
rep(".evcard.xtr{border-color:#D2463C}",".evcard.xtr{border:2px solid #E5483C;animation:xblink 0.9s steps(1,end) infinite}\n@keyframes xblink{0%{border-color:#E5483C;box-shadow:0 0 0 3px rgba(229,72,60,.35),0 0 26px rgba(229,72,60,.5)}50%{border-color:rgba(229,72,60,.15);box-shadow:none}}\n.flag.xh{border-left:3px solid #E5483C;background:rgba(229,72,60,.10)}")
# 3. annonces : rumeur et pouvoirs des styles
rep("const sc=STRESS[si],ev=stressEv(sc.id);if(ev){S.stressQ=sc.id;S.evQueue.splice(1+Math.floor(u()*S.evQueue.length),0,ev)}}}   /* lot 101 */",
    "const sc=STRESS[si],ev=stressEv(sc.id);if(ev){S.stressQ=sc.id;S.evQueue.splice(1+Math.floor(u()*S.evQueue.length),0,ev)}}}   /* lot 101 */\n  xHintDraw();   /* lot 106 */")
rep("function stressP(){",r'''/* lot 106 : l'événement extrême s'annonce parfois. Rumeur : 5 % (loyer) à 65 % (recherche maximale) s'il arrive,
   fausse alerte 6 % sinon. Fondamental : source vérifiée qui le nomme, une fois sur deux. Quant : le modèle de risque le
   nomme et chiffre la perte, six fois sur dix. Flux : sent toujours qu'un choc arrive (sans le nommer), jamais à tort. */
const XH={rum:[0.05,0.10,0.20,0.35,0.45,0.55,0.65],fals:0.06,fonda:0.5,syst:0.6};
function xHintDraw(){const u=prng32(hash32('xhint'+S.q,S.seed)),P=PROF(),sc=S.stressQ?STRESS.find(x=>x.id===S.stressQ):null;S.xHint=null;
 const a=u(),b=u(),c=u(),d=u();
 if(sc){if(P.verified&&a<XH.fonda)S.xHint={src:'fonda',id:sc.id};else if(P.id==='syst'&&a<XH.syst)S.xHint={src:'syst',id:sc.id};
  else if(P.hunch)S.xHint={src:'flux'};else if(b<(XH.rum[S.bud.res]||0.35))S.xHint={src:'rum',id:sc.id}}
 else if(!P.hunch&&c<XH.fals)S.xHint={src:'rum',id:STRESS[Math.floor(d*STRESS.length)].id,fake:1}}
function xHintTxt(k){const h=S&&S.xHint;if(!h)return '';const sc=h.id?STRESS.find(x=>x.id===h.id):null,nm=sc?sc.nm.charAt(0).toLowerCase()+sc.nm.slice(1):'';
 if(h.src==='fonda')return `🔴 <b>Source vérifiée</b> : ${nm}, ce trimestre. C'est certain.`;
 if(h.src==='syst')return `🔴 <b>Le modèle de risque</b> signale un événement extrême probable : ${nm}. Perte du book sur le mouvement complet : ${k?sgnp(stressLoss(k,sc),1)+' · '+moneyB(Math.abs(stressLoss(k,sc))*S.nav):'à lire sur le book'}.`;
 if(h.src==='flux')return `🔴 <b>Votre intuition</b> : un choc extrême se prépare ce trimestre. Vous ne sauriez pas dire lequel.`;
 return `🔴 <b>Rumeur</b> : on parle d'un événement extrême — ${nm}. Rien de vérifié.`}
function stressP(){''')
# rumeurs, écran du desk, page du book
rep(" if(rs&&S.hunch)rs.innerHTML+="," if(rs&&S.xHint)rs.innerHTML+=`<p class=\"note\" style=\"margin:8px 0 0\">${xHintTxt()}</p>`;   /* lot 106 */\n if(rs&&S.hunch)rs.innerHTML+=")
rep(",...(S.hunch?[`<b>Votre intuition</b> : quelque chose vous dit",",...(S.xHint?[xHintTxt()]:[]),...(S.hunch?[`<b>Votre intuition</b> : quelque chose vous dit")
rep("  <div style=\"margin-top:8px\"><div class=\"kv\"><span><b>Événements extrêmes</b>","  ${S.xHint?`<div class=\"flag xh\"><span>${xHintTxt(S.k)}</span></div>`:''}\n  <div style=\"margin-top:8px\"><div class=\"kv\"><span><b>Événements extrêmes</b>")
# 4. les concurrents encaissent aussi
rep("(S.tails=S.tails||[]).push({q:S.q,t:ev.t,f:-imm,id:'stress'})}",
    "(S.tails=S.tails||[]).push({q:S.q,t:ev.t,f:-imm,id:'stress'});xRivHit(ev.stress)}")
rep("function rivalReturns(){",r'''/* lot 106 : un événement extrême frappe aussi les concurrents, selon leur style */
const XRIV={k:0.035,st:{syst:0.8,fonda:1.0,flux:1.3}};
function xRivHit(id){const sc=STRESS.find(x=>x.id===id);if(!sc)return;const u=prng32(hash32('xriv'+S.q+id,S.seed));
 S.xRiv=S.rivals.map((rv,j)=>((S.xRiv||[])[j]||0)-XRIV.k*(sc.ext?2:1)*(XRIV.st[rv.style]||1)*(0.4+1.2*u()));
 toast('Les concurrents encaissent aussi : '+S.rivals.map((rv,j)=>`${rv.nm} ${sgnp(S.xRiv[j],1)}`).join(' · '))}
function rivalReturns(){''')
rep("return S.rivals.map((rv,j)=>{const tl=rivTail(rv,j,rivV(rv),S.q);rv.tailHit=tl>0?tl:0;return rivRet(j,1,S.q)});",
    "return S.rivals.map((rv,j)=>{const tl=rivTail(rv,j,rivV(rv),S.q);rv.tailHit=tl>0?tl:0;return rivRet(j,1,S.q)+((S.xRiv||[])[j]||0)});")
rep("S.rumors=[];S.evVerified=false;","S.rumors=[];S.xRiv=null;S.evVerified=false;")
open('index.html','w',encoding='utf-8').write(s);print('lot106 p1 ok')
