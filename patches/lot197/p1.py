# Lot 197 : Onésime dans la progression normale du front office. Il plafonnait les effets au 7e cran (Marie-Alpha) et
# apportait à la place un « coup de pouce » par trimestre (ecoBoost) ; son nom portait « Atterrissage-en-Douceur », comme
# deux régimes. Désormais : 8e cran à part entière (EXECM, TCVQ, RESN, RESREL, RESR, RESPH, RETM, STARP prolongés d'un
# pas, au rythme du dernier ; syncBud sans plafond), coup de pouce retiré, nom « Pr Onésime « The Oracle » », dit « le
# professeur Onésime » dans les événements.
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep('{who:"Le professeur Atterrissage",hi:',"{who:\"Le professeur Onésime\",hi:")
rep('full:"Pr Onésime « The Oracle » Atterrissage-en-Douceur",role:"économiste en chef, une prévision par plateau télé : un coup de pouce par trimestre"',
    'full:"Pr Onésime « The Oracle »",role:"économiste en chef, une prévision par plateau télé"')
rep('"Le professeur Atterrissage · économiste en chef"','"Le professeur Onésime · économiste en chef"',8)
rep("if(/Atterrissage/.test(w)&&!here(7))return false;","if(/Onésime/.test(w)&&!here(7))return false;")
rep(" L'économiste en chef, au dernier cran, apporte un coup de pouce par trimestre.","")
# barèmes : un 8e cran
rep("const EXECM=[1.35,1.15,1.00,0.75,0.666,0.575,0.498],","const EXECM=[1.35,1.15,1.00,0.75,0.666,0.575,0.498,0.431],   /* lot 197 : 8e cran (Onésime) */")
rep("RETM =[2.00,1.93,1.51,1.00,0.741,0.503,0.398];","RETM =[2.00,1.93,1.51,1.00,0.741,0.503,0.398,0.315];")
rep("const RESN=[6,6,7,9,10,11,12],","const RESN=[6,6,7,9,10,11,12,13],")
rep("RESREL=[-0.08,-0.07,-0.06,0.00,0.028,0.049,0.084],","RESREL=[-0.08,-0.07,-0.06,0.00,0.028,0.049,0.084,0.11],")
rep("RESR  =[0.3,0.32,0.39,0.6,0.726,0.831,0.866],","RESR  =[0.3,0.32,0.39,0.6,0.726,0.831,0.866,0.89],")
rep("RESPH =[0.16,0.156,0.141,0.1,0.084,0.068,0.05];","RESPH =[0.16,0.156,0.141,0.1,0.084,0.068,0.05,0.037];")
rep("const TCVQ=[0.9,0.88,0.76,0.6,0.509,0.425,0.355],","const TCVQ=[0.9,0.88,0.76,0.6,0.509,0.425,0.355,0.296],")
rep("STARP=[0.00,0.00,0.00,0.00,0.105,0.217,0.329];","STARP=[0.00,0.00,0.00,0.00,0.105,0.217,0.329,0.44];")
rep("S.bud.exec=S.bud.res=S.bud.ret=Math.min(S.bud.fo,6);","S.bud.exec=S.bud.res=S.bud.ret=Math.min(S.bud.fo,7);   /* lot 197 : 8 crans */")
# libellés
rep("function budEf(id,i){if(id==='fo')return budEf0('exec',Math.min(i,6))+' · '+budEf0('res',Math.min(i,6))+(i>=7?' · un coup de pouce de l\\'économiste chaque trimestre':'');",
    "function budEf(id,i){if(id==='fo')return budEf0('exec',Math.min(i,7))+' · '+budEf0('res',Math.min(i,7));")
rep("function budExpl(id){if(id==='fo')return budExpl0('exec',Math.min(S.bud.fo,6))+budExpl0('res',Math.min(S.bud.fo,6))+`<p class=\"note\"><b>Économiste en chef</b> (dernier cran) : à chaque trimestre, un marché de plus s'il en reste à ouvrir, sinon un passage à la télévision (confiance +3), une note au comité (confiance +3) ou une dépêche lue juste.</p>`;",
    "function budExpl(id){if(id==='fo')return budExpl0('exec',Math.min(S.bud.fo,7))+budExpl0('res',Math.min(S.bud.fo,7));")
rep("sans limite ${dec(TCVQ[6],2)}","sans limite ${dec(TCVQ[7],2)}")
# coup de pouce retiré
rep("function ecoBoost(){if(!here(7)||S.ecoQ===S.q)return;","function ecoBoost(){return;   /* lot 197 : coup de pouce retiré, Onésime est un cran comme les autres */\n if(!here(7)||S.ecoQ===S.q)return;")
rep("toast(`🎓 <b>Le professeur Atterrissage</b> : ${t}.`)","toast(`🎓 <b>Le professeur Onésime</b> : ${t}.`)")
open('index.html','w',encoding='utf-8').write(s);print('lot197 ok')
s=open("index.html",encoding="utf-8").read()
rep("  if(S.openRk)OPENRK=S.openRk;\n","  syncBud();   /* lot 197 : une sauvegarde avec Onésime passe au 8e cran */\n  if(S.openRk)OPENRK=S.openRk;\n")
open('index.html','w',encoding='utf-8').write(s);print('lot197b ok')
