# Lot 101g : 24 scénarios de stress (demande d'Antoine : plus nombreux, plus extrêmes, idées reprises des accidents
# de levier). Trois familles : chocs de facteurs (marché entier), chocs ciblés sur des marchés (corner, guerre,
# sécheresse…), chocs ciblés sur VOTRE book (short squeeze, trader non autorisé, défaut de contrepartie sur le gré
# à gré, crowding). Extras : liquidité, marges du prime broker, fermeture de marchés au trimestre suivant.
# Les scénarios extrêmes sont 3 fois moins probables. Les chocs ciblés se calculent à l'affichage, sur le book réel.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
i=s.find("const STRESS=[");j=s.find("const STRESSK=",i);assert i>0 and j>i
NEW=r'''const STRESS=[
 {id:'krach',nm:'Krach actions',sh:[-1.5,0,0.5,-3.0],p:"Une vente algorithmique déclenche une cascade. Les actifs risqués décrochent ensemble, les refuges montent."},
 {id:'taux',nm:'Choc de taux',sh:[-0.5,2.5,1.0,-1.0],p:"L'inflation surprend, les banques centrales reprennent la main. Obligations et actions baissent ensemble."},
 {id:'dollar',nm:'Flambée du dollar',sh:[-0.5,0,3.0,-1.0],p:"Tout le monde veut des dollars en même temps. Les émergents et les matières premières plient."},
 {id:'petrole',nm:'Choc pétrolier',sh:[-1.5,2.0,0.5,-0.5],x:{CL:2.5},p:"Un détroit est fermé. Le baril bondit, la croissance recule, l'inflation repart."},
 {id:'liquidite',nm:'Assèchement de liquidité',sh:[-1.0,0,1.5,-2.0],liq:1.5,mg:1.2,p:"Les teneurs de marché se retirent. Les fourchettes s'écartent, tout ce qui est gros devient invendable."},
 {id:'squeeze',nm:'Rallye de soulagement',sh:[2.0,-0.5,-1.0,2.5],p:"La crise annoncée n'arrive pas. Les vendeurs à découvert se rachètent tous en même temps."},
 {id:'gilts',nm:'Krach obligataire',sh:[0,2.0,0.5,-1.5],x:{R:-2.0,OAT:-1.2,GBP:-1.5},p:"Un budget non financé, des fonds de pension à effet de levier : la dette souveraine s'effondre en trois séances."},
 {id:'yuan',nm:'Dévaluation surprise du yuan',sh:[-1.0,0,2.0,-1.5],x:{AUD:-1.5,HG:-1.5,MXEF:-1.2},p:"Pékin laisse filer sa monnaie. Les exportateurs concurrents et les matières premières encaissent le choc."},
 {id:'carry',nm:'Fin du carry trade sur le yen',sh:[0,0,-1.5,-2.0],x:{JPY:2.5,TOPX:-1.8},p:"La Banque du Japon remonte ses taux. Des années d'emprunts en yens se débouclent en une semaine."},
 {id:'deflation',nm:'Choc déflationniste',sh:[-2.0,-2.5,1.0,-1.0],x:{CL:-1.5,HG:-1.2},p:"La demande s'effondre plus vite que prévu. Les prix reculent, les taux longs plongent."},
 {id:'bankrun',nm:'Panique bancaire',ext:1,sh:[-2.0,-1.0,1.0,-3.0],liq:1.8,mg:1.3,x:{GC:1.5},p:"Des files d'attente devant les agences, des dépôts qui s'envolent en ligne en quelques heures. Tout le monde vend ce qui se vend."},
 {id:'lehman',nm:'Faillite d\'un grand prime broker',ext:1,sh:[-2.0,-0.5,1.5,-3.0],liq:2.0,mg:1.6,p:"Un courtier de premier rang fait défaut. Les autres relèvent toutes leurs marges dans la nuit, y compris le vôtre."},
 {id:'shortsq',nm:'Short squeeze',ext:1,tgt:'short',H:3.0,sh:[0,0,0,0.5],p:"Des acheteurs coordonnés s'attaquent à votre plus grosse vente à découvert. Chaque hausse en déclenche une autre."},
 {id:'corner',nm:'Corner sur le cuivre',ext:1,x:{HG:3.5},sh:[0,0.5,0,0],p:"Un négociant a acheté tout le métal livrable. Les vendeurs n'ont plus rien à livrer."},
 {id:'frontieres',nm:'Fermeture des frontières',ext:1,sh:[-3.0,-1.0,1.0,-2.5],x:{BDI:-2.5,KC:1.5},shut:['MXEF','MXP'],p:"Une épidémie ferme les frontières. Le fret s'arrête, deux marchés émergents suspendent leurs cotations jusqu'au trimestre prochain."},
 {id:'guerre',nm:'Guerre en Europe',ext:1,sh:[-1.5,2.0,1.0,-2.0],x:{EUA:2.0,ZW:2.5,CL:1.5,GC:1.5,ESTX:-1.5},p:"Des chars franchissent une frontière. Énergie, blé, or et carbone s'envolent ; l'Europe décroche."},
 {id:'taiwan',nm:'Blocus de Taïwan',ext:1,sh:[-2.0,0.5,1.5,-3.0],x:{NQ:-2.0,TOPX:-2.0,MXEF:-2.0},p:"La marine bloque le détroit. Les semi-conducteurs cessent de circuler, les indices technologiques s'effondrent."},
 {id:'souverain',nm:'Défaut souverain émergent',ext:1,sh:[-1.0,0,1.5,-2.0],x:{MXP:-3.0,MXEF:-2.0},p:"Un grand émetteur émergent suspend ses paiements. Les capitaux fuient toute la classe d'actifs."},
 {id:'contrepartie',nm:'Défaut d\'une contrepartie',ext:1,tgt:'otc',H:2.0,sh:[0,0,0,-0.5],p:"La banque en face de vos forwards et de vos swaps fait défaut. Vos positions de gré à gré sont remplacées au pire prix."},
 {id:'rogue',nm:'Trader non autorisé',ext:1,tgt:'rogue',H:3.0,sh:[0,0,0,0],p:"Des opérations cachées doublaient votre plus grosse ligne. Le marché sent la position et va contre elle."},
 {id:'crowding',nm:'Tout le monde a le même book',ext:1,tgt:'crowd',H:0.8,sh:[0,0,0,-0.5],p:"Les grands fonds macro portaient les mêmes positions que vous. L'un d'eux réduit ; toutes vos lignes partent contre vous."},
 {id:'cyber',nm:'Cyberattaque sur les bourses',ext:1,sh:[-0.5,0,0.5,-1.5],liq:2.0,mg:1.2,p:"Les systèmes d'une grande place de cotation tombent pendant deux séances. Personne ne sait plus où est le prix."},
 {id:'crypto',nm:'Effondrement d\'une plateforme crypto',ext:1,x:{BTC:-3.5},sh:[0,0,0,-1.0],p:"La plus grande plateforme d'échange gèle les retraits. Le bitcoin perd un tiers en un week-end."},
 {id:'secheresse',nm:'Sécheresse historique',ext:1,x:{NRAM:-3.0,ZW:2.5,KC:2.5},sh:[0,0.5,0,0],p:"Trois mois sans pluie sur les grandes plaines et au Brésil. Les récoltes fondent, les prix agricoles flambent."}];
'''
s=s[:i]+NEW+s[j:]
rep("function stressHit(sc){const h={};INSTR.forEach(x=>{let v=0;for(let k=0;k<4;k++)v+=x.b[k]*sc.sh[k];v*=STRESSK;if(Math.abs(v)>=0.03)h[x.sym]=+v.toFixed(3)});return h}",
r'''function stressHit(sc,k){k=k||S.k;const h={};INSTR.forEach((x,i)=>{let v=0;for(let f=0;f<4;f++)v+=x.b[f]*(sc.sh?sc.sh[f]:0);v*=STRESSK;if(sc.x&&sc.x[x.sym])v+=sc.x[x.sym]*STRESSK*1.5;
  if(sc.tgt==='otc'&&x.pt==='otc'&&k[i])v-=Math.sign(k[i])*sc.H;
  if(sc.tgt==='crowd'&&k[i])v-=Math.sign(k[i])*sc.H;
  if(Math.abs(v)>=0.03)h[x.sym]=+v.toFixed(3)});
 if(sc.tgt==='short'||sc.tgt==='rogue'){let bi=-1,bv=0;for(let i=0;i<N;i++){const a=sc.tgt==='short'?-k[i]:Math.abs(k[i]);if(a>bv){bv=a;bi=i}}
  if(bi>=0){const sy=INSTR[bi].sym;h[sy]=+((h[sy]||0)-Math.sign(k[bi])*sc.H).toFixed(3)}}
 return h}''')
rep("function stressEv(id){const sc=STRESS.find(x=>x.id===id);if(!sc)return null;return {stress:id,t:`Scénario de stress : ${sc.nm.toLowerCase()}`,who:'Test de résistance · grandeur nature',p:sc.p,hit:stressHit(sc),...(sc.liq?{liq:sc.liq}:{})}}",
    "function stressEv(id){const sc=STRESS.find(x=>x.id===id);if(!sc)return null;return {stress:id,t:`Scénario de stress : ${sc.nm.charAt(0).toLowerCase()+sc.nm.slice(1)}`,who:sc.ext?'Scénario extrême · grandeur nature':'Test de résistance · grandeur nature',p:sc.p,hit:stressHit(sc),...(sc.liq?{liq:sc.liq}:{}),...(sc.shut?{shut:sc.shut}:{}),...(sc.mg?{mg:sc.mg}:{})}}")
rep("function stressLoss(k,sc){const w=weights(k),h=stressHit(sc);","function stressLoss(k,sc){const w=weights(k),h=stressHit(sc,k);")
rep("function stressP(){return Math.min(0.30,0.08+","function stressP(){return Math.min(0.32,0.10+")
# tirage pondéré (extrêmes ×1/3) ; les chocs ciblés se recalculent à l'affichage
rep("const sc=STRESS[Math.floor(u()*STRESS.length)],ev=stressEv(sc.id);if(ev&&Object.keys(ev.hit).length){",
    "const wt=STRESS.map(x=>x.ext?1/3:1),tw=wt.reduce((a,b)=>a+b,0);let r=u()*tw,si=0;while(si<STRESS.length-1&&r>=wt[si]){r-=wt[si];si++}\n   const sc=STRESS[si],ev=stressEv(sc.id);if(ev){")
rep("function screenMacroEvent(ev){\n hint('event');","function screenMacroEvent(ev){\n if(ev&&ev.stress){const e2=stressEv(ev.stress);if(e2)ev=e2}   /* lot 101 : choc calculé sur le book du moment */\n hint('event');")
rep(" if(shutL.length){S.shut=S.shut||{};shutL.forEach(sy=>S.shut[sy]=S.q+1)}"," if(shutL.length){S.shut=S.shut||{};shutL.forEach(sy=>S.shut[sy]=S.q+1)}\n if(ev.stress&&ev.mg){const m0=S.mgMult||1;S.mgMult=Math.min(2,m0*ev.mg);toast(`Le prime broker relève ses marges : ×${dec(m0,2)} → ×${dec(S.mgMult,2)}`)}")
# panneau : les six pires pour votre book, le reste replié
rep("${tbl(STRESS.map(sc=>{const v=stressLoss(S.k,sc);return [sc.nm,`<b class=\"${v>=0?'pos-g':'neg-g'}\">${sgn(v,1)} · ${moneyB(Math.abs(v)*S.nav)}</b>`]}),['Scénario','Mouvement complet sur le book'])}",
    "${(()=>{const L=STRESS.map(sc=>({sc,v:stressLoss(S.k,sc)})).sort((a,b)=>a.v-b.v),row=o=>[o.sc.nm+(o.sc.ext?' <span class=\"dim-g\">· extrême</span>':''),`<b class=\"${o.v>=0?'pos-g':'neg-g'}\">${sgn(o.v,1)} · ${moneyB(Math.abs(o.v)*S.nav)}</b>`];return tbl(L.slice(0,6).map(row),['Les six pires pour votre book','Mouvement complet'])+`<details><summary>Les ${L.length-6} autres scénarios</summary>${tbl(L.slice(6).map(row))}</details>`})()}")
open('index.html','w',encoding='utf-8').write(s);print('ok',NEW.count("{id:"))
