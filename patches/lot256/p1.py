p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
# options : rien, 2 %, 5 %, 10 % (seuils fixes)
a=s.index(" const opts=[\n  {id:'prud'");b=s.index(" opts.forEach(o=>{if(o.ret!=null)o.ret*=gk});   /* lot 150 */\n")+len(" opts.forEach(o=>{if(o.ret!=null)o.ret*=gk});   /* lot 150 */\n")
s=s[:a]+""" /* lot 256 : seuils fixes (rien, 2, 5, 10 %) ; mémoire de crédibilité et conséquences au-delà de la confiance (commClose) */
 const opts=[
  {id:'none',ico:'🤐',nm:"Pas de chiffre",who:"« Nous ne commentons pas nos objectifs »",p:`Vous ne promettez rien. Rien à gagner, presque rien à perdre : les investisseurs ne relèvent votre silence que si le trimestre finit dans le rouge.`,
   ret:null,win:{lp:0,rc:0},lose:{lp:-2,rc:0}},
  {id:'prud',ico:'📄',nm:"Communication standard",who:"« Nous visons un trimestre solide »",p:`Vous annoncez ${pctc(0.02)} sur le trimestre. C'est ce que les investisseurs attendent d'un fonds macro : le tenir rassure, le manquer se remarque.`,
   ret:0.02,win:{lp:5,rc:0},lose:{lp:-4,rc:0}},
  {id:'fort',ico:'📣',nm:"Conviction forte",who:"« C'est le trimestre de l'année »",p:`Vous annoncez ${pctc(0.05)}. Tenu, un consultant en sélection de fonds vous inscrit sur sa liste : souscriptions ×1,2 le trimestre suivant.`,
   ret:0.05,win:{lp:14,rc:0},lose:{lp:-7,rc:0},fx:{ok:1.2}},
  {id:'gourou',ico:'🔮',nm:"Prophétie de gourou",who:"« Nous allons écraser le marché »",p:`Vous annoncez ${pctc(0.10)} en un trimestre, devant les caméras. Tenu : plateau télé, souscriptions ×1,5 le trimestre suivant. Manqué : un mème, souscriptions ×0,7, et le comité demande qui a validé ce chiffre.`,
   ret:0.10,win:{lp:30,rc:0},lose:{lp:-8,rc:-3},fx:{ok:1.5,ko:0.7}}
 ];
"""+s[b:]
rep("""    :`<div class="commrow"><span>Vous promettez</span><b>au moins ${sgnp(o.ret,1)} · ${mm(o.ret*S.nav)}</b></div>
      <div class="commrow"><span>Tenu · manqué</span><b>confiance <i class="pos-g">+${o.win.lp}</i> · <i class="neg-g">−${-o.lose.lp}</i></b></div>
      ${(()=>{const b=expBook(S.k),z=b.s>0?(b.m-o.ret)/b.s:0,p=1/(1+Math.exp(-1.702*z));
        return `<div class="commrow"><span>Chance de tenir, d'après votre attendu</span><b>${Math.round(p*100)} %</b></div>`})()}`}""",
"""    :`<div class="commrow"><span>Vous promettez</span><b>au moins ${sgnp(o.ret,1)} · ${mm(o.ret*S.nav)}</b></div>
      <div class="commrow"><span>Tenu · manqué</span><b>confiance <i class="pos-g">+${o.win.lp}${(S.commStr||0)>0?'+'+Math.min(5,S.commStr):''}</i> · <i class="neg-g">−${-o.lose.lp*((S.commStr||0)>=2?2:1)}</i></b></div>
      ${(()=>{const p=commP(o.ret);
        return `<div class="commrow"><span>Chance de tenir, attendu net de frais, dépêches et extrêmes</span><b>${Math.round(p*100)} %</b></div>`})()}`}""")
rep("""`<div class="commrow"><span>En fin de trimestre, quoi qu'il arrive</span><b class="dim-g">rien ne bouge</b></div>`""",
    """`<div class="commrow"><span>En fin de trimestre</span><b class="dim-g">confiance −2 si le trimestre est négatif</b></div>`""")
rep("""function screenComm(){""","""/* lot 256 : chance de tenir, calée sur 195 trimestres joués : le résultat tout compris vaut en moyenne 0,65 × l'attendu
   du book − 3 points (frais, dépêches, extrêmes, accidents), avec une dispersion 1,25 fois plus large */
function commP(ret){const b=expBook(S.k);if(!(b.s>0))return 0.5;return 1/(1+Math.exp(-1.702*(0.65*b.m-0.03-ret)/(1.25*b.s)))}
/* lot 256 : solde de la promesse — série de promesses tenues (+1 par promesse, plafond +5), promesse manquée après
   deux tenues : perte doublée ; tenue de moins d'un point : gain moitié ; conséquences sur les souscriptions */
function commClose(qT){const c=S.comm;S.commRes=null;if(!c)return;
 if(c.ret===null){if(qT<0)S.commRes={none:1,e:c.lose.lp,rc:0,lab:'Pas de chiffre, trimestre négatif'};return}
 const ok=qT>=c.ret,st=S.commStr||0,just=ok&&qT-c.ret<0.01;
 const e=ok?Math.round(c.win.lp*(just?0.5:1))+Math.min(5,st):c.lose.lp*(st>=2?2:1);
 S.commRes={ok,okR:ok,okV:true,just,st,e,rc:ok?c.win.rc:c.lose.rc,lab:`Engagement « ${c.nm.toLowerCase()} » ${ok?(just?'tenu de justesse':'tenu'):'manqué'}${ok&&st?` · série de ${st+1}`:''}${!ok&&st>=2?' · après une série : perte doublée':''}`};
 S.commStr=ok?st+1:0;
 const m=c.fx?(ok?c.fx.ok:c.fx.ko):null;S.commFx=m?{q:S.q+1,m,id:c.id,ok}:null}
function screenComm(){""")
rep(""" if(S.comm&&S.comm.ret!==null)S.commRes={ok:qTotal>=S.comm.ret,okR:qTotal>=S.comm.ret,okV:true};""",""" commClose(qTotal);   /* lot 256 */""")
rep("""if(S.commRes){const e=S.commRes.ok?S.comm.win.lp:S.comm.lose.lp;lpD.push([`Engagement « ${S.comm.nm.toLowerCase()} » ${S.commRes.ok?'tenu':'manqué'} (hors plafonnement)`,e]);dlpC+=e}""",
    """if(S.commRes){const e=S.commRes.e;lpD.push([`${S.commRes.lab} (hors plafonnement)`,e]);dlpC+=e}""")
rep("""if(S.commRes)rcD.push([`Engagement « ${S.comm.nm.toLowerCase()} » ${S.commRes.ok?'tenu':'manqué'}`,S.commRes.ok?S.comm.win.rc:S.comm.lose.rc]);""",
    """if(S.commRes&&S.commRes.rc)rcD.push([S.commRes.lab+(S.comm.id==='gourou'&&!S.commRes.ok?' : « qui a validé ce chiffre ? »':''),S.commRes.rc]);""")
# souscriptions du trimestre suivant
rep("""function invInF(D){return D.inn*S.lp/50*(SIZE().flowIn||1)*Math.max(0,1-capStress())}""",
    """function invInF(D){return D.inn*S.lp/50*(SIZE().flowIn||1)*Math.max(0,1-capStress())*(S.commFx&&S.commFx.q===S.q?S.commFx.m:1)}   /* lot 256 */""")
# presse
rep("""if(S.commRes&&!S.commRes.ok)add(""","""if(S.commRes&&S.commRes.just)add(pk(["Les Échos","Bloomberg","Podcast · Salle des marchés"],47),pk([`${F} tient sa promesse de ${sgn(S.comm.ret,1)}… à quelques points de base près. Le service communication respire`,`Promesse tenue au fil du rasoir chez ${F}. On parle d'une dernière séance « très surveillée »`],48));
 else if(S.commRes&&S.commRes.ok&&S.comm.id==='gourou')add(pk(["BFM Business","Bloomberg TV","CNBC"],49),pk([`${F} avait promis d'écraser le marché. C'est fait : le gérant passe ce soir sur le plateau, cravate desserrée`,`Prophétie tenue : ${F} livre plus de ${sgn(S.comm.ret,1)} et s'invite au journal du soir. Les allocataires appellent`],50));
 else if(S.commRes&&!S.commRes.ok&&S.comm.id==='gourou')add(pk(["X · @macro_leaks","Reddit · r/hedgefunds","Podcast · Salle des marchés"],51),pk([`La prophétie de ${F} tourne en mème : « nous allons écraser le marché », avec le graphique du trimestre en dessous`,`${F} promettait ${sgn(S.comm.ret,1)}. Les salles de marché ont trouvé leur fond d'écran de la semaine`],52));
 else if(S.commRes&&S.commRes.ok&&S.commRes.st>=2)add(pk(["Absolute Return","Les Échos"],53),pk([`${S.commRes.st+1} promesses tenues d'affilée chez ${F}. Dans le métier, on commence à le croire sur parole`],54));
 else if(S.commRes&&!S.commRes.ok)add(""")
open(p,'w',encoding='utf-8').write(s)
s=open(p,encoding='utf-8').read()
rep("""
 else if(S.comm&&S.comm.id==='none'&&S.comm.lose.lp)lpD.push(['Aucune communication ce trimestre',S.comm.lose.lp]);""","")
rep("""
 else if(S.comm&&S.comm.id==='none'&&S.comm.lose.rc)rcD.push(['Aucune communication ce trimestre',S.comm.lose.rc]);""","")
open(p,'w',encoding='utf-8').write(s)
s=open(p,encoding='utf-8').read()
rep("""ret:0.05,win:{lp:14,rc:0},lose:{lp:-7,rc:0},fx:{ok:1.2}},""","""ret:0.05,win:{lp:14,rc:0},lose:{lp:-7,rc:0},fx:{ok:1.2},fxT:"tenu : souscriptions ×1,2 au trimestre suivant"},""")
rep("""ret:0.10,win:{lp:30,rc:0},lose:{lp:-8,rc:-3},fx:{ok:1.5,ko:0.7}}""","""ret:0.10,win:{lp:30,rc:0},lose:{lp:-8,rc:-3},fx:{ok:1.5,ko:0.7},fxT:"tenu : plateau télé, souscriptions ×1,5 · manqué : mème, souscriptions ×0,7, comité −3"}""")
rep("""        return `<div class="commrow"><span>Chance de tenir, attendu net de frais, dépêches et extrêmes</span><b>${Math.round(p*100)} %</b></div>`})()}`}""",
    """        return `<div class="commrow"><span>Chance de tenir, attendu net de frais, dépêches et extrêmes</span><b>${Math.round(p*100)} %</b></div>`})()}${o.fxT?`<div class="commrow"><span>Ensuite</span><b>${o.fxT}</b></div>`:''}${(S.commStr||0)>0?`<div class="commrow"><span>Série en cours</span><b>${S.commStr} promesse${S.commStr>1?'s':''} tenue${S.commStr>1?'s':''}${S.commStr>=2?' : manquer coûte double':''}</b></div>`:''}`}""")
open(p,'w',encoding='utf-8').write(s)
