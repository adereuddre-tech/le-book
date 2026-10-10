p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
rep(""" if(H.length<4){const ctx={F:F,boss:best.boss,rk:rk,ahead:ahead?ahead.nm:'personne',rival:pick(S.rivals).nm};""",""" recurPress(add,q,F);   /* lot 280 */
 if(H.length<4){const ctx={F:F,boss:best.boss,rk:rk,ahead:ahead?ahead.nm:'personne',rival:pick(S.rivals).nm};""")
rep("""function pressFeed(o){""","""/* lot 280 : deux personnages récurrents. Clémence Ardoise (« La Lettre du Macro ») se souvient de vos trimestres
   passés ; Hector Vasseur, consultant en sélection de fonds, note le fonds chaque année — la note pèse sur les souscriptions. */
const HECT={A:1.2,B:1.05,C:0.95,D:0.8};
function hectorM(){return S&&S.hector&&S.q<=S.hector.until?HECT[S.hector.g]:1}
function recurPress(add,q,F){
 const M=S.memo=S.memo||[];const cur={q:S.q,r:q,off:OFF().nm,comm:S.comm&&S.comm.ret!=null?{ret:S.comm.ret,ok:!!(S.commRes&&S.commRes.ok)}:null,atk:S.atkRes?{ok:S.atkRes.ok,nm:S.atkRes.nm}:null};
 const ch=(a,k)=>a[(hash32('cl'+k+S.q,S.seed)>>>0)%a.length];let t=null;
 const prev=M.length?M[M.length-1]:null,miss=M.filter(m=>m.comm&&!m.comm.ok),old=miss.length?miss[miss.length-1]:null,ORD=['','','Deuxième','Troisième','Quatrième','Cinquième','Sixième'];let ty=null;
 if(prev&&prev.off!==cur.off)ty='off',t=ch([`${F} quitte « ${prev.off} » pour « ${cur.off} ». Le loyer a changé d'échelle ; on attend de voir si la performance suit`,`Déménagement chez ${F} : de « ${prev.off} » à « ${cur.off} ». Dans le métier, on appelle ça « signaler sa réussite » — ou « l'anticiper »`],'off');
 else if(cur.comm&&!cur.comm.ok&&old)ty='miss',t=`${ORD[Math.min(6,miss.length+1)]||'Énième'} promesse manquée pour ${F} : au trimestre ${old.q}, on nous annonçait déjà ${sgnp(old.comm.ret,0)}. Nous gardons les lettres`;
 else if(cur.comm&&cur.comm.ok&&miss.length&&S.clemT!=='kept')ty='kept',t=`${F} tient enfin sa promesse. Nous n'avions pas oublié les précédentes, et nous notons celle-ci aussi`;
 else if(prev&&prev.r<-0.04&&q>0.04)ty='up',t=`Il y a un trimestre, ${F} perdait ${sgnp(prev.r,1)} et l'on parlait de fermeture. Le voici à ${sgnp(q,1)}. Nous avions écrit que c'était prématuré — nous le relisons avec plaisir`;
 else if(prev&&prev.r>0.04&&q<-0.04)ty='down',t=`Le trimestre dernier, ${F} gagnait ${sgnp(prev.r,1)} ; celui-ci, ${sgnp(q,1)}. Nous avions titré « l'insolent » ; nous gardons le mot, pour d'autres raisons`;
 else if(cur.atk)ty='atk',t=cur.atk.ok?`Nous avions qualifié d'imprudente l'attaque de ${F} sur ${cur.atk.nm}. Nous retirons « imprudente »`:`L'attaque de ${F} sur ${cur.atk.nm} a échoué. Nous l'avions écrit ; nous ne le réécrirons pas, c'est inutile`;
 if(t&&S.memoQ!==S.q){add('Clémence Ardoise · La Lettre du Macro',t);S.clemT=ty}else if(S.memoQ!==S.q)S.clemT=null;
 /* Hector Vasseur : une note par an, au 4e, 8e, 12e trimestre */
 if(S.memoQ!==S.q&&S.q>=4&&S.q%4===0){const R=(S.rets||[]).slice(-4),mu=R.reduce((a,b)=>a+b,0)/Math.max(1,R.length),sd=Math.sqrt(R.reduce((a,b)=>a+(b-mu)**2,0)/Math.max(1,R.length-1))||1e-9,sh=mu/sd*2;
  const g=sh>1.2&&S.maxdd<0.15?'A':sh>0.5?'B':sh>0?'C':'D',g0=S.hector?S.hector.g:null;S.hector={g,until:S.q+4};
  add('Hector Vasseur · Vasseur & Associés, sélection de fonds',g0&&g0!==g?`Nous ${g<g0?'relevons':'abaissons'} la note de ${F} de ${g0} à ${g}. ${g==='A'?"Nous le recommandons désormais sans réserve.":g==='D'?"Nous déconseillons toute nouvelle souscription.":"La note est revue dans un an."}`:`Notre note annuelle sur ${F} : ${g}. ${g==='A'?"Le fonds entre dans nos recommandations.":g==='B'?"Un fonds solide, à suivre.":g==='C'?"Des réserves sur la régularité.":"Nous déconseillons toute nouvelle souscription."} Souscriptions de nos clients ×${dec(HECT[g],2)} pendant un an`)}
 if(S.memoQ!==S.q){M.push(cur);if(M.length>12)M.shift();S.memoQ=S.q}}
function pressFeed(o){""")
rep("""*offFx('subs')}   /* lot 256 ; lot 276 */""","""*offFx('subs')*hectorM()}   /* lot 256 ; lot 276 ; lot 280 */""")
open(p,'w',encoding='utf-8').write(s)
