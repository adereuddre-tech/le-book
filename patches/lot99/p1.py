# Lot 99 : objectifs de place conditionnés ; confiance des dépêches sur le résultat net de la dépêche ;
# débauchage et chasseur de têtes ciblent un trader ; back office : protection croissante jusqu'à ×0,5, sixième cran.
import json
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
# 1. objectifs de place : pas au premier trimestre, seulement si l'on peut gagner la place
rep('{nm:"Gagner une place",d:"Progresser d\'au moins une place au classement cumulé.",t:c=>c.rankUp>=1,b:0.07},','{nm:"Gagner une place",d:"Progresser d\'au moins une place au classement cumulé.",t:c=>c.rankUp>=1,b:0.07,pre:\'rank2\'},')
rep('{nm:"Deux places d\'un coup",d:"Progresser d\'au moins deux places au classement cumulé.",t:c=>c.rankUp>=2,b:0.13},','{nm:"Deux places d\'un coup",d:"Progresser d\'au moins deux places au classement cumulé.",t:c=>c.rankUp>=2,b:0.13,pre:\'rank3\'},')
rep("(!g.pre||(g.pre==='never'?false:g.pre==='loss'?lastQ<0:lastQ>0))","(!g.pre||(g.pre==='never'?false:g.pre==='rank2'?S.q>=1&&rivalRank()>=2:g.pre==='rank3'?S.q>=1&&rivalRank()>=3:g.pre==='loss'?lastQ<0:lastQ>0))")
# 2. dépêches : la confiance suit le résultat net de la dépêche (immédiat + suite), pas chaque morceau séparément
rep("function reactGz(p){","function pnlD(p){const i=S.evImm||0,a=pnlGz(i+p),b=pnlGz(i);return {lp:cf(a.lp,a.rc)-cf(b.lp,b.rc),rc:0}}   /* lot 99 */\nfunction reactGz(p){")
rep(" const gzF=payF.map(p=>{const a=pnlGz(p);let lp=a.lp,rc=a.rc;"," const gzF=payF.map(p=>{const a=pnlD(p);let lp=a.lp,rc=a.rc;")
rep("gz:payN.map(p=>{const a=pnlGz(p);return {lp:cf(a.lp,a.rc),rc:a.rc,pnl:a}})","gz:payN.map(p=>{const a=pnlD(p);return {lp:cf(a.lp,a.rc),rc:a.rc,pnl:a}})")
rep(" const plan=evPlans(ev,touched);\n"," S.evImm=imm;   /* lot 99 */\n const plan=evPlans(ev,touched);\n")
# 3. débauchage et chasseur de têtes : un trader présent
rep("for(let p=1;p<=S.bud.fo;p++)if(here(p))cands.push(p);   /* lot 96 : débauchage de base */","for(let p=1;p<=S.bud.fo;p++)if(here(p)&&FOP[p].cls)cands.push(p);   /* lot 96 : débauchage de base ; lot 99 : traders seulement */")
rep("{const p=cands[Math.floor(rng()*cands.length)];S.gone={p,n:1,boss};","{const p=(S.huntP!=null&&cands.includes(S.huntP))?S.huntP:cands[Math.floor(rng()*cands.length)];S.huntP=null;S.gone={p,n:1,boss};")
rep('''{who:"Un chasseur de têtes",t:"Citadelle Nord veut vous recruter, vous",
  p:"Ken Griffon propose le double. La rumeur fait le tour du desk avant même que vous ayez raccroché.",
  ch:[{b:"Refuser et le faire savoir",s:"Le desk est rassuré, les investisseurs aussi (+3).",e:{lp:3}},
      {b:"« Je réfléchis »",s:"Le desk s'inquiète, deux gérants prennent des appels. Débauchage +30 % ce trimestre, investisseurs −2.",e:{poach:0.3,lp:-2}}]}''',
'''{who:"Un chasseur de têtes",hunt:1,t:"Citadelle Nord veut recruter {X}",
  p:"Ken Griffon propose le double à {X}. La rumeur fait le tour du desk avant même que vous l'ayez apprise.",
  ch:[{b:"Surenchérir tout de suite",s:"−3 pb, {X} reste et le fait savoir : débauchage −30 % ce trimestre, investisseurs +1.",e:{cash:-0.0003,poach:-0.3,lp:1}},
      {b:"Laisser {X} réfléchir",s:"Débauchage +30 % ce trimestre, et c'est {X} que Griffon vise. Investisseurs −2.",e:{poach:0.3,lp:-2}}]}''')
rep("function persoOk(e){const w=e.who||'';","function persoOk(e){const w=e.who||'';if(e.hunt&&!huntCands().length)return false;")
rep("function cast(ev){if(!ev||!S||!S.bud)return ev;",r'''function huntCands(){const c=[];for(let p=1;p<FOP.length;p++)if(FOP[p].cls&&here(p))c.push(p);return c}
function huntX(x,n){if(typeof x==='string')return x.split('{X}').join(n);if(Array.isArray(x))return x.map(y=>huntX(y,n));if(x&&typeof x==='object'){const q={};for(const k in x)q[k]=huntX(x[k],n);return q}return x}
function cast(ev){if(ev&&ev.hunt&&S&&S.bud){const c=huntCands();if(c.length){const p=c[Math.floor(rng()*c.length)];S.huntP=p;ev=Object.assign(huntX(ev,FOP[p].who),{t0:ev.t0||ev.t})}}
 if(!ev||!S||!S.bud)return ev;''')
# 4. back office : six crans, protection croissante (×0,5 au dernier)
rep(''' {who:"L'inspecteur Tatillon",hi:"Faites comme si je n'étais pas là. Je note tout.",full:"L'inspecteur Firmin Tatillon",role:"conformité et audit interne",ic:"🔎",bp:45}];''',
''' {who:"L'inspecteur Tatillon",hi:"Faites comme si je n'étais pas là. Je note tout.",full:"L'inspecteur Firmin Tatillon",role:"conformité et audit interne",ic:"🔎",bp:45},
 {who:"La commandante Pare-Feu",hi:"Personne n'entre. Surtout pas vos erreurs.",full:"La commandante Solange Pare-Feu",role:"sécurité, continuité d'activité, cyber",ic:"🛡️",bp:60}];''')
rep("const BOMAP=[0,2,3,5,6],","const BOMAP=[0,1,3,4,5,6],")
rep("RISKM=[5.0,2.00,2.0,1.00,0.636,0.8,0.7],","RISKM=[5.0,2.0,2.0,1.00,0.8,0.65,0.5],")
rep("RISKS=[3.00,1.93,1.95,1.5,1.22,1.3,1.2],","RISKS=[3.00,1.95,1.95,1.5,1.2,0.975,0.75],")
rep("TAILM=[2.5,1.41,1.4,1.00,0.783,0.88,0.8];","TAILM=[2.5,1.4,1.4,1.00,0.8,0.65,0.5];")
rep("BANDB=[0.12,0.18,0.19,0.25,0.292,0.33,0.40];","BANDB=[0.12,0.19,0.19,0.25,0.30,0.36,0.42];")
rep("const RISKRC=[-3.0,-0.9,-1.5,0.00,0.7,2.5,4.0],","const RISKRC=[-3.0,-1.5,-1.5,0.00,2.5,4.0,5.0],")
rep("Au-dessus, le back office rassure surtout le comité.","Au-dessus, chaque poste réduit nettement la fréquence et la gravité des incidents et les accidents de levier, jusqu'à les diviser par deux au dernier cran, et rassure le comité.")
rep("||(/Tatillon/.test(w)&&S.bud.bo<4))","||(/Tatillon/.test(w)&&S.bud.bo<4)||(/Pare-Feu/.test(w)&&S.bud.bo<5))")
P="La commandante Pare-Feu · sécurité"
def ev(t,p,ch): return {"who":P,"t":t,"p":p,"ch":[dict(b=b,s=x,e=e) for b,x,e in ch]}
NEW=[ev("« Quelqu'un a branché une clé USB trouvée sur le parking »","« Elle s'appelait BONUS_2026.xlsx. Évidemment qu'il l'a branchée. »",
  [("Tout isoler et tout réinstaller","−3 pb, comité +3.",{"cash":-0.0003,"rc":3}),("Nettoyer le seul poste concerné","20 % de risque d'intrusion : −0,3 %.",{"risk":[0.2,-0.003],"riskMsg":"La clé était pleine de surprises"})]),
 ev("« Exercice d'évacuation. Tout le monde dehors, desk compris »","« Le plan de continuité prévoit une salle de secours à Créteil. Elle n'a jamais servi. Aujourd'hui, elle sert. »",
  [("Jouer le jeu jusqu'au bout","Coûts +5 % ce trimestre, comité +3.",{"tcMult":1.05,"rc":3}),("Dispenser le desk","Comité −2.",{"rc":-2})]),
 ev("« Un faux Ken Griffon a appelé Josiane pour un virement urgent »","« La voix était bonne. Le compte était à Chypre. Elle a raccroché. »",
  [("Former toute l'équipe à la fraude au président","−2 pb, comité +2.",{"cash":-0.0002,"rc":2}),("Féliciter Josiane","Débauchage −5 %, comité +1.",{"poach":-0.05,"rc":1})]),
 ev("« Vos mots de passe sont collés sur l'écran de Boris »","« Sur un Post-it. Jean-Kevin l'a plastifié pour qu'il tienne mieux. »",
  [("Des clés physiques pour tout le monde","−2 pb, coûts +2 % (tout le monde râle), comité +3.",{"cash":-0.0002,"tcMult":1.02,"rc":3}),("Un rappel par courriel","Comité +1.",{"rc":1})])]
rep("const TRADER_MID=[\n","const TRADER_MID=[\n"+''.join(' '+json.dumps(o,ensure_ascii=False)+',\n' for o in NEW))
rep("S.tailEv=null;S.tailDone=false;S.tailQ=null;S._kLast=null;S._kGhost=null;","S.tailEv=null;S.tailDone=false;S.tailQ=null;S._kLast=null;S._kGhost=null;S.huntP=null;")
open('index.html','w',encoding='utf-8').write(s);print('ok')
