# Lot 93 : l'équipe conditionne les anecdotes. Mêmes mécaniques ; si l'auteur ou la personne citée n'est pas
# (ou plus) dans l'équipe, le libellé passe au remplaçant (courtier de la classe, back office présent, Jean-Kevin).
# Les cinq anecdotes qui parlent d'une personne précise (offre de débauchage, concours de chili…) sont retirées
# du tirage tant qu'elle est absente. Répliques d'arrivée dans le toast de recrutement.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep('function covered(g){',r'''/* lot 93 : distribution des rôles */
const CAST=[
 {re:'Dwight Tannenbaum|Dwight',on:()=>here(1),sub:()=>'le courtier actions'},
 {re:'Ingrid Bergström|Ingrid',on:()=>here(2),sub:()=>'le courtier de taux'},
 {re:'Boris Rasoumovsky|Boris',on:()=>here(3),sub:()=>'le courtier devises'},
 {re:'Bartolomeo « Tuco » Ossobuco|Tuco',on:()=>here(4),sub:()=>'le courtier matières premières'},
 {re:'Wing-Fat « Winnie » Leung|Winnie',on:()=>here(5),sub:()=>'le courtier de Hong Kong'},
 {re:'Sœur Marie-Alpha',on:()=>here(6),sub:()=>'Jean-Kevin'},
 {re:'Mireille Cauchemar|Mireille',on:()=>S.bud.bo>=3,sub:()=>S.bud.bo>=2?'Josiane Suspens':'Maître Lettrage'}];
CAST.forEach(c=>{c.rx=new RegExp('(?:'+c.re+')')});
const PERSO={"Tuco a gagné le concours de chili du prime broker":4,"Citadelle Nord fait une offre à Ingrid":2,"Pont-Levis Associés cherche un gérant énergie":4,"Votre gérante taux part chez un concurrent":2,"Un concurrent tourne autour de Boris":3};
function persoOk(e){const p=PERSO[e.t];return p===undefined||here(p)}
function recast(x,c){if(typeof x!=='string'||!c.rx.test(x))return x;const n=c.sub(),A=c.re,le=n.startsWith('le ');
 x=x.replace(new RegExp('(^|[^\\wÀ-ÿ])de (?:'+A+')','g'),(m,p)=>p+(le?'du '+n.slice(3):'de '+n));
 x=x.replace(new RegExp('(^|[^\\wÀ-ÿ])à (?:'+A+')','g'),(m,p)=>p+(le?'au '+n.slice(3):'à '+n));
 x=x.replace(new RegExp('(^|[.!?:]\\s+|«\\s*)(?:'+A+')','g'),(m,p)=>p+n[0].toUpperCase()+n.slice(1));
 return x.replace(new RegExp('(?:'+A+')','g'),n)}
function cast(ev){if(!ev||!S||!S.bud)return ev;const off=CAST.filter(c=>!c.on()&&JSON.stringify(ev).match(c.rx));if(!off.length)return ev;
 const o=Object.assign({},ev,{t0:ev.t0||ev.t});
 off.forEach(c=>{if(typeof o.who==='string'&&c.rx.test(o.who)){const pa=o.who.split(' · ');o.who=c.rx.test(pa[0])?(n=>n[0].toUpperCase()+n.slice(1))(c.sub())+(pa[1]?' · '+pa[1]:''):pa[0]}
  ['t','p','after','riskMsg','safeTxt','safe','msg'].forEach(k=>{o[k]=recast(o[k],c)});
  if(Array.isArray(o.ch))o.ch=o.ch.map(ch=>{const q=Object.assign({},ch);for(const k in q)q[k]=recast(q[k],c);return q})});
 return o}
function covered(g){''')
# tirages
rep("const tav=TRADER_MID.filter(e=>!S.usedTrader.includes(e.t)&&","const tav=TRADER_MID.filter(e=>!S.usedTrader.includes(e.t)&&persoOk(e)&&")
rep("const av=TRADER_EXEC.filter(e=>!S.usedExec.includes(e.t)&&","const av=TRADER_EXEC.filter(e=>!S.usedExec.includes(e.t)&&persoOk(e)&&")
rep("const ev=av.length?pick(av):null;if(ev)S.usedExec.push(ev.t);","const ev=av.length?cast(pick(av)):null;if(ev)S.usedExec.push(ev.t0||ev.t);")
rep("BOARDEV.filter(e=>!S.usedEv.includes(e.t)&&!evTouchesBook(e))","BOARDEV.filter(e=>!S.usedEv.includes(e.t)&&persoOk(e)&&!evTouchesBook(e))",2)
rep("const ev=pick(av);S.usedEv.push(ev.t);","const ev=cast(pick(av));S.usedEv.push(ev.t0||ev.t);")
rep("function screenTraderEvent(ev,next){\n next=next||stepEvents;","function screenTraderEvent(ev,next){\n next=next||stepEvents;ev=cast(ev);")
# répliques d'arrivée
for who,hi in [('Jean-Kevin',"J'ai fait un tableur. Il a des couleurs."),('Dwight',"Mon algorithme a déjà réservé votre bureau."),('Ingrid',"La courbe ne ment pas. Les gens, si."),('Boris',"Un téléphone, vingt minutes, et je vous trouve le prix."),('Tuco',"J'apporte mes cigares et mes contacts à Rotterdam."),('Winnie',"Hong Kong ouvre dans six heures. J'y suis déjà."),('Sœur Marie-Alpha',"Le modèle est juste. Ce sont les hommes qui pèchent."),('Maître Lettrage',"Tout se lettre, même vos erreurs."),('Josiane Suspens',"Aucun ordre ne sort d'ici sans être rapproché."),('Mireille',"Je ne dis pas non. Je dis : justifiez."),("L'inspecteur Tatillon","Faites comme si je n'étais pas là. Je note tout.")]:
    rep('{who:"%s",full:'%who,'{who:"%s",hi:"%s",full:'%(who,hi.replace('"','\\"')))
rep("toast(`${i1>i0?'Recrutement':'Départ'} : <b>${who.map(l=>l.who).join(', ')}</b>","toast(`${i1>i0?'Recrutement':'Départ'} : <b>${who.map(l=>l.who).join(', ')}</b>${i1>i0&&who.length===1&&who[0].hi?` — « ${who[0].hi} »`:''}")
open('index.html','w',encoding='utf-8').write(s);print('ok')
