# Lot 96 : débauchage de base à chaque clôture (50 %, ×0,5 avec 10 % de bonus, ×0,2 avec 25 %), sans bénéficiaire ;
# deuxièmes prénoms ; Dwight à la voix, Boris à l'algorithme ; économiste en chef au cran 7 (250 pb, un bonus par
# trimestre) ; back office recentré sur Josiane (neutre), loyer catastrophique, effets sur incidents et accidents
# réduits, comité renforcé ; Maître Lettrage devient Maître Report-à-Nouveau.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
def cut(a,b,new):
    global s; i=s.find(a); j=s.find(b,i); assert i>=0 and j>i,(a[:40],b[:40]); s=s[:i]+new+s[j:]
# --- équipe
cut('const FOP=[','const BOMAP=',r'''const FOP=[
 {who:"Jean-Kevin",hi:"J'ai fait un tableur. Il a des couleurs.",full:"Jean-Kevin Brayan Lévêque-Charbonnier",role:"analyste macro junior, à tout faire",ic:"🐣",bp:0},
 {who:"Dwight",hi:"Un téléphone, vingt minutes, et je vous trouve le prix.",full:"Dwight Elvis Tannenbaum",role:"trader actions, exécution à la voix",ic:"📞",bp:10,cls:'Actions'},
 {who:"Ingrid",hi:"La courbe ne ment pas. Les gens, si.",full:"Ingrid Solveig Bergström",role:"cheffe du desk taux, la plus senior",ic:"🏦",bp:25,cls:'Taux'},
 {who:"Boris",hi:"Mon algorithme a déjà réservé votre bureau.",full:"Boris Vladlenovitch Rasoumovsky",role:"trader devises, expert exécution et algorithmes",ic:"🤖",bp:45,cls:'Devises'},
 {who:"Tuco",hi:"J'apporte mes cigares et mes contacts à Rotterdam.",full:"Bartolomeo Ernesto « Tuco » Ossobuco",role:"trader matières premières",ic:"🛢️",bp:70,cls:'Matières premières'},
 {who:"Winnie",hi:"Hong Kong ouvre dans six heures. J'y suis déjà.",full:"Wing-Fat Jericho « Winnie » Leung",role:"trader exotiques",ic:"🐉",bp:100,cls:'Exotiques'},
 {who:"Sœur Marie-Alpha",hi:"Le modèle est juste. Ce sont les hommes qui pèchent.",full:"Sœur Marie-Alpha Bêta",role:"stratégiste quantitative, recherche",ic:"📿",bp:150},
 {who:"Le professeur Atterrissage",hi:"Je ne prévois pas la récession. Je la commente avant tout le monde.",full:"Pr Onésime Barnabé Atterrissage-en-Douceur",role:"économiste en chef : un coup de pouce par trimestre",ic:"🎓",bp:250}];
const BOP=[
 {who:"Le loyer",full:"Le loyer",role:"bureaux, écrans, électricité, et rien d'autre",ic:"🏢",bp:5},
 {who:"Maître Report-à-Nouveau",hi:"Tout finit au report à nouveau, même vos erreurs.",full:"Maître Gontran Hilaire Report-à-Nouveau",role:"expert-comptable",ic:"🧮",bp:10},
 {who:"Josiane Suspens",hi:"Aucun ordre ne sort d'ici sans être rapproché.",full:"Josiane Ghislaine Suspens",role:"responsable du back office",ic:"🗂️",bp:15},
 {who:"Mireille",hi:"Je ne dis pas non. Je dis : justifiez.",full:"Mireille Perpétue Cauchemar",role:"directrice des risques",ic:"⚖️",bp:30},
 {who:"L'inspecteur Tatillon",hi:"Faites comme si je n'étais pas là. Je note tout.",full:"L'inspecteur Firmin Anatole Tatillon",role:"conformité et audit interne",ic:"🔎",bp:45}];
''')
rep("const BOMAP=[0,3,4,5,6],","const BOMAP=[0,2,3,5,6],")
rep("Les traders et la recherche. Chaque recrue améliore l'avis du desk sur toutes les classes et sur la macro : coûts d'exécution, bruit des indicateurs, nombre et fiabilité des sources, lecture des dépêches, résistance au débauchage.","Les traders et la recherche. Chaque recrue améliore l'avis du desk sur toutes les classes et sur la macro : coûts d'exécution, bruit des indicateurs, nombre et fiabilité des sources, lecture des dépêches. L'économiste en chef, au dernier cran, apporte un coup de pouce par trimestre.")
rep("Un back office sérieux évite les incidents, rend les accidents de levier plus rares et apaise le comité.","Josiane Suspens est le point neutre. Le loyer seul, c'est la catastrophe : incidents en série, accidents de levier. Au-dessus, le back office rassure surtout le comité.")
rep("bud:{fo:3,bo:1,exec:3,risk:3,res:3,ret:3}","bud:{fo:3,bo:2,exec:3,risk:3,res:3,ret:3}")
rep("function syncBud(){if(!S||!S.bud)return;S.bud.exec=S.bud.res=S.bud.ret=S.bud.fo;","function syncBud(){if(!S||!S.bud)return;S.bud.exec=S.bud.res=S.bud.ret=Math.min(S.bud.fo,6);")
rep("function budEf(id,i){if(id==='fo')return budEf0('exec',i)+' · '+budEf0('res',i);","function budEf(id,i){if(id==='fo')return budEf0('exec',Math.min(i,6))+' · '+budEf0('res',Math.min(i,6))+(i>=7?' · un coup de pouce de l\\'économiste chaque trimestre':'');")
rep("function budExpl(id){if(id==='fo')return budExpl0('exec',S.bud.fo)+budExpl0('res',S.bud.fo);","function budExpl(id){if(id==='fo')return budExpl0('exec',Math.min(S.bud.fo,6))+budExpl0('res',Math.min(S.bud.fo,6))+`<p class=\"note\"><b>Économiste en chef</b> (dernier cran) : à chaque trimestre, un marché de plus s'il en reste à ouvrir, sinon un passage à la télévision (confiance +3), une note au comité (confiance +3) ou une dépêche lue juste.</p>`;")
# back office : crans 0, 2, 3, 5, 6 des anciennes tables (loyer, Report-à-Nouveau, Josiane, Mireille, Tatillon)
rep("RISKM=[2.2,2.00,1.5,1.00,0.636,0.426,0.363],","RISKM=[5.0,2.00,2.0,1.00,0.636,0.8,0.7],   /* lot 96 : aux crans 0,2,3,5,6 seulement (BOMAP) */")
rep("RISKS=[2.00,1.93,1.72,1.5,1.22,0.954,0.856],","RISKS=[3.00,1.93,1.95,1.5,1.22,1.3,1.2],")
rep("TAILM=[1.48,1.41,1.22,1.00,0.783,0.594,0.51];","TAILM=[2.5,1.41,1.4,1.00,0.783,0.88,0.8];")
rep("BANDB=[0.18,0.18,0.21,0.25,0.292,0.369,0.432];","BANDB=[0.12,0.18,0.19,0.25,0.292,0.33,0.40];")
rep("const RISKRC=[-1.00,-0.9,-0.6,0.00,0.7,1.54,2.17],","const RISKRC=[-3.0,-0.9,-1.5,0.00,0.7,2.5,4.0],")
rep(" · débauchage ×${dec(RETM[i],2)}","")
rep(" <b>Débauchage</b> : risque de perdre un gérant ×${dec(RETM[i],2)}.","")
# --- anecdotes : l'algorithme passe à Boris, Lettrage devient Report-à-Nouveau
rep('who:"Dwight Tannenbaum · exécution quantitative"','who:"Boris Rasoumovsky · exécution quantitative"',15)
rep("L'algorithme de Dwight","L'algorithme de Boris")
rep("Dwight admet une limite","Boris admet une limite")
rep("Maître Lettrage","Maître Report-à-Nouveau",6)
rep("/Lettrage/.test(w)","/Report-à-Nouveau/.test(w)")
# --- bonus sans bénéficiaire, débauchage de base
rep("const BONUS=[0,0.10,0.25],BONM=[1,0.6,0.3],GROGNE=1.5;","const BONUS=[0,0.10,0.25],BONM=[1,0.5,0.2],GROGNE=1.5,POACHP=0.5;")
cut("function bonTxt(){","function payBonus(){",r'''function bonTxt(){if(S.qBonT>0)return `<br>Bonus d'équipe versé : ${mm(S.qBonT)} · risque de débauchage ${Math.round(POACHP*S.bonMultQ*100)} % ce trimestre`;
 return S.bonMultQ>1?`<br><span class="neg-g">Le desk grogne : deux trimestres gagnants sans bonus. Risque de débauchage ${Math.round(Math.min(0.95,POACHP*GROGNE)*100)} % ce trimestre.</span>`:`<br>Risque de débauchage : ${Math.round(POACHP*100)} % ce trimestre (sans bonus d'équipe).`}
''')
rep("if(amt>0){S.mgrCosts+=amt;S.cBonT=(S.cBonT||0)+amt;S.qBonT=amt;S.bonMultQ=BONM[i];const w=S.bonWho;S.bonWhoQ=(w!=null&&here(w))?w:(bonCands()[0]??null)}","if(amt>0){S.mgrCosts+=amt;S.cBonT=(S.cBonT||0)+amt;S.qBonT=amt;S.bonMultQ=BONM[i]}")
rep("\n if(S.bonWhoQ!=null&&FOP[S.bonWhoQ]&&FOP[S.bonWhoQ].cls===x.grp)m*=0.9;   /* lot 95 : bénéficiaire du bonus */","")
cut("const bnSel=","\n const coSel=",r'''const bnSel=(S.over||S.q>=QT()||!((S.mgrQ&&S.mgrQ.perf)>0))?'':(()=>{const pf=S.mgrQ.perf;
  return `<div class="block"><div class="blockhead"><h2>Bonus d'équipe</h2><span class="hint">versé à l'ouverture</span></div>
  <p class="note" style="margin-top:0">Une part de votre commission de performance (${mm(pf)}), versée à l'équipe. Sans bonus, un concurrent débauche l'un de vos gérants une fois sur deux à la clôture ; son siège reste vide un trimestre.${(S.noBon||0)>=1?` <b class="neg-g">Le trimestre gagnant précédent s'est passé de bonus : un second sans rien et le desk grogne (risque ${Math.round(Math.min(0.95,POACHP*GROGNE)*100)} %).</b>`:''}</p>
  <div class="cisel">${BONUS.map((p,i)=>`<button class="bnp${i===(S.bonI||0)?' on':''}" data-i="${i}">${Math.round(p*100)} %<br><small>${mm(p*pf)} · risque ${Math.round(POACHP*BONM[i]*100)} %</small></button>`).join('')}</div></div>`})();''')
rep("\n app.querySelectorAll('.bnw').forEach(b=>b.onclick=()=>{S.bonWho=+b.dataset.p;app.querySelectorAll('.bnw').forEach(x=>x.classList.toggle('on',x===b))});","")
rep("if(tot<-0.01&&rng()<(0.5+S.poachBoost)*RETM[S.bud.ret]*(rel<-0.005?1:0.4)*(S.bonMultQ||1)){S.execPenalty*=1.14;const boss=(pick(S.rivals.filter(x=>x.poacher))||S.rivals[S.rivals.length-1]).boss,cands=[];for(let p=1;p<=S.bud.fo;p++)if(here(p)&&p!==S.bonWhoQ)cands.push(p);",
 "{const pP=Math.min(0.95,Math.max(0,(POACHP+0.5*(S.poachBoost||0))*(S.bonMultQ||1))),cands=[];for(let p=1;p<=S.bud.fo;p++)if(here(p))cands.push(p);   /* lot 96 : débauchage de base */\n if(!S.over&&cands.length&&rng()<pP){const boss=(pick(S.rivals.filter(x=>x.poacher))||S.rivals[S.rivals.length-1]).boss;")
rep("if(cands.length){const p=pk(cands,92);S.gone={p,n:1,boss};S.poachMsg+=` ${boss} a débauché ${FOP[p].full} : coûts d'exécution +14 % durablement, et son siège reste vide","{const p=cands[Math.floor(rng()*cands.length)];S.gone={p,n:1,boss};S.poachMsg+=` ${boss} a débauché ${FOP[p].full} : son siège reste vide")
rep("\n  else S.poachMsg+=` ${boss} a débauché deux de vos gérants : coûts d'exécution +14 % durablement.`;","")
rep("la remise sur cette classe disparaît.`}}","la remise sur cette classe disparaît.`}}}")
# --- économiste en chef : un coup de pouce par trimestre, tiré après le budget
rep("function planSignalsAfterBudget(){",r'''function ecoBoost(){if(!here(7)||S.ecoQ===S.q)return;S.ecoQ=S.q;let t;
 if(OPENRK<5){OPENRK++;S.openRk=OPENRK;applyPools();const nw=INSTR.filter(x=>x.rk===OPENRK);S.ecoB='mk';t=`il obtient de votre courtier l'accès à ${nw.map(x=>x.nm).join(', ')||'un nouveau marché'}`}
 else if(!S.exoOpen&&GRP.includes('Exotiques')){S.exoOpen=true;applyPools();S.ecoB='exo';t="il convainc le comité de vous ouvrir les marchés exotiques"}
 else{const o=PROF().id==='fonda'?['tv','note']:['tv','note','ver'];S.ecoB=o[Math.floor(rng()*o.length)];
  if(S.ecoB==='tv'){gauge(3,0,"L'économiste en chef à la télévision");t="il passe au journal de 20 heures : confiance +3"}
  else if(S.ecoB==='note'){gauge(0,3,"Note de l'économiste en chef au comité");t="sa note rassure le comité : confiance +3"}
  else t="il vous lira juste la première dépêche du trimestre"}
 S.ecoTxt=t;toast(`🎓 <b>Le professeur Atterrissage</b> : ${t}.`)}
function planSignalsAfterBudget(){
 ecoBoost();   /* lot 96 */''')
rep("const ver=pr.id==='fonda'&&!S.evVerified;","const ver=(pr.id==='fonda'||(S.ecoB==='ver'&&S.ecoQ===S.q))&&!S.evVerified;")
open('index.html','w',encoding='utf-8').write(s);print('ok')
