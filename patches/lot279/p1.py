import re
p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
# 1. grilles : coût total de l'équipe au cran, en pb d'une base fixe de 100 M$ (avant facteurs de style, de taille et de locaux)
FO=[0,10,25,45,70,100,140,190];BO=[0,5,12,22,35,50]
a=s.index("const FOP=[");b=s.index("];",a);blk=s[a:b];i=[0]
def f(m):
    v=FO[i[0]];i[0]+=1;return 'bp:%d'%v
blk2=re.sub(r'bp:\d+',f,blk);assert i[0]==8
blk2+=""",
 {who:"Priya",hi:"Les satellites voient les parkings pleins avant les résultats.",full:"Priya « Pixel » Raman",role:"données alternatives, images satellites et cartes bancaires",ic:"🛰️",bp:250,g:'f',pw:"bruit des signaux tendance, portage et valeur ×0,75"},
 {who:"Sir Mervyn",hi:"J'ai écrit ce communiqué il y a dix ans. Ils n'ont changé que la date.",full:"Sir Mervyn « Forward Guidance » Hale",role:"ancien banquier central",ic:"🏛️",bp:320,pw:"sur les dépêches de banques centrales et de taux, la probabilité de suite est donnée exacte"},
 {who:"Kenji",hi:"Je connais leur book par cœur. Je l'ai construit.",full:"Kenji « Le Transfuge » Ota",role:"gérant star débauché chez un concurrent",ic:"🥷",bp:400,pw:"le meilleur concurrent perd 20 % d'adresse ; un deuxième signal lu aussi bien que le vôtre"},
 {who:"Pr Ada",hi:"Le marché est efficient. Sauf quand je le regarde.",full:"Pr Ada « Nobel » Lindqvist",role:"prix Nobel d'économie, une conférence par mois",ic:"🏅",bp:490,g:'f',pw:"lecture des dépêches 30 % plus précise, confiance +2 par trimestre ; mais 10 % de risque de fuite par trimestre"},
 {who:"Victoria",hi:"Le ministre m'appelle encore. Pour avoir mon avis.",full:"Victoria « Black Book » Ashworth",role:"ancienne directrice de cabinet d'un ministre des Finances",ic:"📒",bp:590,g:'f',pw:"chaque trimestre, le sens du facteur macro le plus fort, juste neuf fois sur dix"}"""
s=s[:a]+blk2+s[b:]
a=s.index("const BOP=[");b=s.index("];",a);blk=s[a:b];i=[0]
def g(m):
    v=BO[i[0]];i[0]+=1;return 'bp:%d'%v
blk2=re.sub(r'bp:\d+',g,blk);assert i[0]==6
blk2+=""",
 {who:"Margaux",hi:"Un investisseur qui comprend est un investisseur qui reste.",full:"Margaux « Sourire » Delacroix",role:"relations investisseurs",ic:"🤝",bp:70,pw:"rachats −30 % ; une gate ne coûte plus que la moitié de la confiance"},
 {who:"Maître Fourche",hi:"Tout est négociable, surtout ce qui est écrit.",full:"Maître Aurélien Fourche",role:"juriste, contentieux et contrats",ic:"📜",bp:95,pw:"incidents 40 % moins chers"},
 {who:"Lord Basil",hi:"Bruxelles est un village. Washington aussi.",full:"Lord Basil Lobbington",role:"affaires publiques, Bruxelles et Washington",ic:"🎖️",bp:125,pw:"contrôle des risques +2 par trimestre ; les extrêmes sentis sont identifiés 15 pts plus souvent"},
 {who:"Cassandra",hi:"Je ne prédis pas les crises. Je les tarife.",full:"Cassandra « Black Swan » Mehta",role:"cheffe des risques extrêmes",ic:"🦢",bp:160,pw:"protection contre les extrêmes 30 % moins chère ; veille +15 pts"},
 {who:"Octave",hi:"Votre marge était trop chère. Je l'ai renégociée pendant votre réunion.",full:"Octave « Repo » Mercier",role:"trésorier, financement et collatéral",ic:"💱",bp:200,pw:"marge exigée −15 % sur tout le book"},
 {who:"Hugo",hi:"Deux prime brokers valent mieux qu'un seul qui vous lâche.",full:"Hugo « Two Banks » Ravel",role:"responsable des contreparties",ic:"🏦",bp:245,pw:"accidents de levier par la marge ÷2 ; lignes visibles 30 % moins exposées"},
 {who:"Dr Anouk",hi:"Un trader qui dort bien ne fait pas de fat finger.",full:"Dr Anouk Ferreira",role:"psychologue de la salle des marchés",ic:"🧘",bp:295,pw:"débauchage ÷2 ; incidents −20 %"}"""
s=s[:a]+blk2+s[b:]
rep("const BOMAP=[0,1,3,4,5,6],","const BOMAP=[0,1,3,4,5,6,6,6,6,6,6,6,6],")
rep("function bonBase(){if(!S||!S.bud)return 0;const p=Math.min(S.bud.fo,FOP.length-1);","function bonBase(){if(!S||!S.bud)return 0;const p=Math.min(S.bud.fo,7);   /* lot 279 : base plafonnée au cran d'Onésime */")
# 2. effets
rep("""function cntOn(){""","""function boH(n){return !!(S&&S.bud&&S.bud.bo>=n)}   /* lot 279 : back office au cran n ou plus */
function cntOn(){""")
rep("""function budEf(id,i){if(id==='fo')return budEf0('exec',Math.min(i,7))+' · '+budEf0('res',Math.min(i,7));if(id==='bo')return budEf0('risk',BOMAP[i]);return budEf0(id,i)}""",
    """function budEf(id,i){const X=L=>L.slice(0,i+1).filter(l=>l.pw).map(l=>`<br>${l.ic} <b>${l.who}</b> : ${l.pw}`).join('');   /* lot 279 */
 if(id==='fo')return budEf0('exec',Math.min(i,7))+' · '+budEf0('res',Math.min(i,7))+X(FOP);if(id==='bo')return budEf0('risk',BOMAP[i])+X(BOP);return budEf0(id,i)}""")
# Priya et Kenji : lecture des signaux
rep("ne=kk=>e*(S.prof==='syst'?0.6:S.prof==='tail'?1:(kk===mine?0.3:1.3));","ne=kk=>e*(here(8)?0.75:1)*(here(10)&&kk===SIG2[S.prof]?0.3:S.prof==='syst'?0.6:S.prof==='tail'?1:(kk===mine?0.3:1.3));")
rep("function sigNoise(key){const e=TCVQ[S.bud.exec]*(S.tcvPerm?0.33:1);return e*(S.prof==='syst'?0.6:","const SIG2={syst:'t',fonda:'c',flux:'c',rv:'v',tail:'t',act:'c'};   /* lot 279 : le deuxième signal de Kenji */\nfunction sigNoise(key){const e=TCVQ[S.bud.exec]*(S.tcvPerm?0.33:1)*(here(8)?0.75:1);if(here(10)&&key===SIG2[S.prof])return e*0.3;return e*(S.prof==='syst'?0.6:")
# Sir Mervyn et Ada : dépêches
rep("""  const ver=(pr.id==='fonda'||(S.ecoB==='ver'&&S.ecoQ===S.q))&&!S.evVerified;if(ver)S.evVerified=true;""",
    """  const cb=here(9)&&/banque centrale|Fed\\b|BCE|BoE|BoJ|taux directeur|gouverneur|Réserve fédérale/i.test((ev.t||'')+' '+(ev.who||''));   /* lot 279 : Sir Mervyn */
  const ver=cb||((pr.id==='fonda'||(S.ecoB==='ver'&&S.ecoQ===S.q))&&!S.evVerified);if(ver&&!cb)S.evVerified=true;""")
rep("""  const pr=PROF(),sd=RESPH[S.bud.res]*(pr.id==='flux'?0.6:1)*(BONREAD[bonEff()]||1);""","""  const pr=PROF(),sd=RESPH[S.bud.res]*(pr.id==='flux'?0.6:1)*(BONREAD[bonEff()]||1)*(here(11)?0.7:1);""")
# Ada : confiance et fuite ; Lord Basil : contrôle ; Victoria : le facteur
rep(""" if(offFx('lp',0))lpD.push([`Les locaux : ${OFF().nm}`,offFx('lp',0)]);   /* lot 276 */""",""" if(offFx('lp',0))lpD.push([`Les locaux : ${OFF().nm}`,offFx('lp',0)]);   /* lot 276 */
 if(here(11))lpD.push(["La conférence du Pr Ada",2]);   /* lot 279 */""")
rep(""" const rcD=[];if(offFx('rc',0))""",""" const rcD=[];if(boH(8))rcD.push(["Lord Basil a déjeuné avec le régulateur",2]);if(offFx('rc',0))""")
rep(""" ecoBoost();   /* lot 96 */""",""" ecoBoost();   /* lot 96 */
 if(here(11)&&!pwOn('jo')&&prng32(hash32('ada'+S.q,S.seed))()<0.10){S.leakQ=true;toast("🏅 Le Pr Ada a cité vos positions en conférence : elles circulent ce trimestre.")}   /* lot 279 */
 if(here(12)&&S.f){let k=0;for(let j=1;j<K;j++)if(Math.abs(S.f[j])>Math.abs(S.f[k]))k=j;const ok=prng32(hash32('vic'+S.q,S.seed))()<0.9,up=(S.f[k]>0)===ok;
  (S.pwTips=S.pwTips||[]).push({who:'Victoria',nm:`Le facteur « ${FACT[k].nm.toLowerCase()} »`,up:up===(FSG[k]>0),q:S.q})}
 if(here(10)&&!S.kenjiDone){const R=(S.rivals||[]).filter(r=>!r.closed).sort((a,b)=>(b.cum||0)-(a.cum||0))[0];if(R){R.skill=(R.skill||0.7)*0.8;S.kenjiDone=1;toast(`🥷 Kenji arrive de chez ${R.nm} : ils perdent 20 % d'adresse.`)}}""")
# Margaux, Fourche, Lord Basil (veille), Cassandra, Octave, Hugo, Anouk
rep("""function invOutF(D){return Math.min(1,D.out*2*(1-S.lp/100)*(SIZE().flowMult||1)*offFx('out'))}""","""function invOutF(D){return Math.min(1,D.out*2*(1-S.lp/100)*(SIZE().flowMult||1)*offFx('out')*(boH(6)?0.7:1))}""")
s=s.replace("S.lp=Math.max(0,S.lp+INVP.gateLp);S.lpD.push(['Gate activée : rachats limités à '+Math.round(INVP.gate*100)+' % de l\\'encours',INVP.gateLp])",
            "S.lp=Math.max(0,S.lp+INVP.gateLp*(boH(6)?0.5:1));S.lpD.push(['Gate activée : rachats limités à '+Math.round(INVP.gate*100)+' % de l\\'encours',INVP.gateLp*(boH(6)?0.5:1)])")
rep(""" const loss=uni(inc.loss[0],inc.loss[1])*sev,navB=S.nav""",""" const loss=uni(inc.loss[0],inc.loss[1])*sev*(boH(7)?0.6:1),navB=S.nav""")
rep(""" const sv=Math.max(0.10,Math.min(0.95,B.s+0.30*f+0.20*r+0.15*(b-0.5)+offFx('watch',0))),iv=Math.max(0.05,Math.min(0.95,B.i+0.30*f+0.10*(b-0.5)));""",
    """ const sv=Math.max(0.10,Math.min(0.95,B.s+0.30*f+0.20*r+0.15*(b-0.5)+offFx('watch',0)+(boH(9)?0.15:0))),iv=Math.max(0.05,Math.min(0.95,B.i+0.30*f+0.10*(b-0.5)+(boH(8)?0.15:0)));""")
rep("""function hedgeCost(){return Math.max(HEDGE.min,hL()*hedgeEV())}""","""function hedgeCost(){return Math.max(HEDGE.min,hL()*hedgeEV())*(boH(9)?0.7:1)}""")
rep("""function mgRate(i){const x=INSTR[i];return x.mg*((PTYPE[x.pt]||PTYPE.fut).m)*((S&&S.mgMult)||1)}""","""function mgRate(i){const x=INSTR[i];return x.mg*((PTYPE[x.pt]||PTYPE.fut).m)*((S&&S.mgMult)||1)*(boH(10)?0.85:1)}   /* lot 279 : Octave */""")
rep("""function levAccP(mgu){return mgu<=MGZ.watch?0:Math.min(0.6,MGZ.pmax*Math.pow((mgu-MGZ.watch)/(MGC.thr-MGZ.watch),MGZ.pow))}""","""function levAccP(mgu){return (mgu<=MGZ.watch?0:Math.min(0.6,MGZ.pmax*Math.pow((mgu-MGZ.watch)/(MGC.thr-MGZ.watch),MGZ.pow)))*(boH(11)?0.5:1)}""")
rep("""  if(k[i]<0)L.push({i,f,kind:'short',p:Math.min(VIS.pmax,VIS.p0+VIS.pk*f)});""","""  if(k[i]<0)L.push({i,f,kind:'short',p:Math.min(VIS.pmax,VIS.p0+VIS.pk*f)*(boH(11)?0.7:1)});""")
rep("""  else if(m>MGZ.watch)L.push({i,f,kind:'long',p:Math.min(VIS.pmax,(VIS.p0+VIS.pk*f)*Math.min(2.5,m/MGZ.watch))})}return L}""","""  else if(m>MGZ.watch)L.push({i,f,kind:'long',p:Math.min(VIS.pmax,(VIS.p0+VIS.pk*f)*Math.min(2.5,m/MGZ.watch))*(boH(11)?0.7:1)})}return L}""")
rep("""BONFX[bonEff()].p*(S.bonCutQ===S.q?BONCUT:1)*offFx('poach'))}""","""BONFX[bonEff()].p*(S.bonCutQ===S.q?BONCUT:1)*offFx('poach')*(boH(12)?0.5:1))}""")
s=s.replace("*PROF().incMult*offFx('inc')+","*PROF().incMult*offFx('inc')*(boH(12)?0.8:1)+")
open(p,'w',encoding='utf-8').write(s)
