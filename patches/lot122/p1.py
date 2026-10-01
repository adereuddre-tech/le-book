# Lot 122 : retours d'Antoine + coût de l'équipe selon le style.
import re
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
# 1. coût de l'équipe selon le style (quant ×0,85, fondamental ×1, flux ×1,15)
rep("function budNav(){return Math.max(S.nav,S.aum0||S.nav)*((SIZE()&&SIZE().costM)||1)}",
    "const STYCOST={syst:0.85,fonda:1,flux:1.15};   /* lot 122 */\nfunction budNav(){return Math.max(S.nav,S.aum0||S.nav)*((SIZE()&&SIZE().costM)||1)*(STYCOST[S.prof]||1)}")
rep("['g',\"capital de départ +0,40 M$\"]","['g',\"capital de départ +0,40 M$ ; équipe 15 % moins chère\"]")
rep("['b',\"aucun capital de départ supplémentaire\"]","['b',\"aucun capital de départ supplémentaire ; équipe 15 % plus chère\"]")
# 2. pré-annonces : sens économique des décisions de banque centrale (le vecteur projeté sur les charges lisait un rally obligataire
#    comme « croissance, inflation et liquidité en baisse ») ; indice 2 interne = dollar, liquidité = −dollar
rep("function eventFactorVec(ev){\n const v=[0,0,0,0];",
    "const EVFV=[[/programme d'achats|assouplissement|achats illimités|anti-fragmentation|injecte|baisse (surprise )?(de )?ses taux|baisse ses taux|baisse des taux|coupe ses taux|relance budgétaire/i,[1,1,-2,2]],\n [/relève (ses|les) taux|hausse (surprise )?(de )?ses taux|resserrement monétaire|plus faucon|resserre/i,[-1,-1,2,-2]]];\n"
    "function eventFactorVec(ev){\n if(ev.fv)return ev.fv;{const tx=(ev.t||'')+' '+(ev.p||'');for(const [rx,v] of EVFV)if(rx.test(tx))return v}\n const v=[0,0,0,0];")
# 3. ligne des facteurs d'un marché : noms abrégés
rep("const FN=['Croissance','Inflation','Liquidité','Appétit'];","const FN=['Crois.','Infl.','Liquid.','Appét.'];")
# 4. investisseurs : la Couronne en dernier, souscription automatique ; plus de clause de repli
rep("function invs(){if(!S.inv)S.inv=INVR.map(d=>({id:d.id,w:d.w0,ntc:0}));if(!S.inv.some(v=>v.id==='roy'))S.inv.splice(3,0,{id:'roy',w:0,ntc:0});return S.inv}",
    "function invs(){if(!S.inv)S.inv=INVR.map(d=>({id:d.id,w:d.w0,ntc:0}));if(!S.inv.some(v=>v.id==='roy'))S.inv.push({id:'roy',w:0,ntc:0});\n const o=INVR.map(d=>d.id);S.inv.sort((a,b)=>o.indexOf(a.id)-o.indexOf(b.id));return S.inv}")
m=re.search(r"\n \{id:'roy',[^\n]*\n  rule:\"[^\n]*\"\},",s);assert m;roy=m.group(0);s=s[:m.start()]+s[m.end():]
roy=roy.replace("rule:\"la holding de la famille royale se règle sur le plus sévère des quatre autres : elle rachète dès que l'un d'eux rachète, et ne souscrit que si tous souscrivent — au taux de rachat le plus fort et au taux de souscription le plus faible.\"",
 "rule:\"la holding de la famille royale souscrit d'office chaque trimestre, de 10 à 25 % de sa ligne selon la confiance ; en plus, elle se règle sur le plus sévère des quatre autres : elle rachète dès que l'un d'eux rachète (au taux le plus fort, 55 %), et souscrit encore si tous souscrivent.\"")
i=s.index("const INVR=[");j=s.index("];",i);s=s[:j]+","+roy.lstrip('\n').rstrip(',')+"\n"+s[j:] if not s[i:j].rstrip().endswith(',') else s[:j]+roy.lstrip('\n')+"\n"+s[j:]
rep("rule:\"souscrit après 2 trimestres positifs d'affilée, rachète après 2 trimestres négatifs d'affilée. Clause de repli : au-delà du repli maximal de votre style, la moitié de sa part.\"",
    "rule:\"souscrit après 2 trimestres positifs d'affilée, rachète après 2 trimestres négatifs d'affilée.\"")
rep("  if(v.id==='cr'&&o.ddp>=ddMax()){f=Math.max(f,0.5);r.clause=true}\n","")
rep("const INVP={","const INVP={royAuto:[0.10,0.25],",1)
rep(" S.invQ=R;const net="," {const v=I.find(x=>x.id==='roy'),r=R.find(x=>x.id==='roy');if(v&&v.w>1e-6&&!(v.ntc>0)&&r){const f=INVP.royAuto[0]+(INVP.royAuto[1]-INVP.royAuto[0])*S.lp/100;r.sub+=invFlow(v,f*v.w*extNav());r.auto=1}}   /* lot 122 */\n S.invQ=R;const net=")
rep("['g',\"clause de repli de la caisse de retraite à 40 % de perte au lieu de 28 %\"],","")
rep("['b',\"clause de repli de la caisse de retraite dès 22 % de perte au lieu de 28 %\"],","")
rep(", la caisse de retraite demande la moitié de sa part.",", le fonds continue : les investisseurs jugent sur leurs propres critères.") if s.count(", la caisse de retraite demande la moitié de sa part.")==1 else None
# 5. annonces
rep("ret:0.03,win:{lp:5,rc:0},lose:{lp:-10,rc:0}},","ret:0.03,win:{lp:5,rc:0},lose:{lp:-5,rc:0}},")
rep("ret:0.09,win:{lp:15,rc:0},lose:{lp:-12,rc:0}},","ret:0.09,win:{lp:15,rc:0},lose:{lp:-8,rc:0}},")
rep("ret:0.15,win:{lp:30,rc:0},lose:{lp:-15,rc:0}}","ret:0.15,win:{lp:30,rc:0},lose:{lp:-10,rc:0}}")
# 6. flux : ce que veut dire « réagir juste »
rep("p:\"Vous ne prédisez rien : vous écoutez le marché. Vous regardez un carnet d'ordres comme d'autres regardent la mer, et il vous arrive d'avoir raison avant d'avoir compris pourquoi.\",",
    "p:\"Vous ne prédisez rien : vous écoutez le marché. Votre avantage se joue sur les dépêches : vous lisez mieux que les autres la probabilité qu'un mouvement continue ou se retourne, vous en captez 85 % quand vous le suivez, et un ajustement par trimestre est gratuit. Le revers : un book plus chargé, des investisseurs qui suivent votre courbe au jour le jour, une équipe plus chère. Si vous suivez quand il fallait laisser passer, vous payez deux fois — les ordres et le retournement.\",")
# 7. tuyau du prime broker : écran de résultat
rep("  screenExec();window.scrollTo(0,0)};\n app.querySelectorAll('.choice[data-tip]')",
    "  {const lpT=k?(win?2:-1):0,g=lpT?gauge(lpT,0,`${t.nm} : ${win?'le pari a payé':'le pari a échoué'}`):{lp:0,rc:0};\n"
    "   resultCard('PRIME BROKER · PROPOSITION HORS BOOK',k?(win?`${t.ic} ${t.nm} : l'affaire passe`:`${t.ic} ${t.nm} : l'affaire échoue`):`${t.ic} ${t.nm} : ${rv.nm} l'a prise`,\n"
    "    [k?`Coût certain −${dec(t.c*100,1)} %${win?`, gain +${dec(t.g*100,1)} %`:''} : <em class=\"${cls(imm)}\">${sgn(imm,1)}</em> pour le fonds, soit ${mn(imm*S.nav)}. Le résultat compte dans le trimestre.`\n"
    "      :`Vous avez passé. ${rv.nm} a pris l'affaire : ${win?'elle est passée':'elle a échoué'}, <em class=\"${cls(imm)}\">${sgn(imm,1)}</em> pour son trimestre.`],\n"
    "    [['<b>Résultat pour le fonds</b>',k?`<span class=\"${cls(imm)}\">${sgn(imm,1)} · ${mn(imm*S.nav)}</span>`:'—'],['Confiance',`<span class=\"${cls(g.lp)}\">${sd1(g.lp)}</span>`]],\n"
    "    \"Passer à l'exécution\",()=>{screenExec();window.scrollTo(0,0)})}};\n app.querySelectorAll('.choice[data-tip]')")
rep("  screenExec();window.scrollTo(0,0)};\n app.querySelectorAll('.choice[data-tip]')","",0) if False else None
# 8. concurrents : montants des accidents, et ceux du joueur
rep("const all=[{nm:S.fundName,v:o.qTotal,me:1,rk:o.sp,cv:S.idx-1},",
    "const myT=(S.tails||[]).filter(x=>x.q===S.q-1);\n const all=[{nm:S.fundName,v:o.qTotal,me:1,rk:o.sp,cv:S.idx-1,mt:myT},")
rep("${a.th?`<br><span class=\"neg-g\" style=\"font-size:11px\">accident de levier</span>`:''}",
    "${a.th?`<br><span class=\"neg-g\" style=\"font-size:11px\">accident de levier −${dec(a.th*100,1)} %</span>`:''}${(a.mt||[]).map(x=>`<br><span class=\"${cls(-x.f)}\" style=\"font-size:11px\">${x.id==='stress'?'événement extrême':'accident de levier'} ${sgnp(-x.f,1)}</span>`).join('')}")
# 9. événement du conseil : la Couronne entre au capital
rep("{who:\"Relations investisseurs\",t:\"Un fonds souverain veut entrer\",",
    "{who:\"Relations investisseurs\",t:\"La Couronne du Liquidistan veut entrer\",")
rep("ch:[{b:\"Prendre l'argent\",s:\"L'encours grimpe, le passif devient plus fragile.\",e:{aum:0.12,lp:4,rc:-7,flighty:true}},",
    "ch:[{b:\"Prendre l'argent\",s:\"La holding royale entre avec 12 % de l'encours : il grimpe, le passif devient plus fragile.\",e:{royIn:0.12,lp:4,rc:-7,flighty:true}},")
rep("  if(e.aum){S.flows=(S.flows||0)+e.aum*S.nav;S.nav*=(1+e.aum)}\n",
    "  if(e.aum){S.flows=(S.flows||0)+e.aum*S.nav;S.nav*=(1+e.aum)}\n  if(e.royIn){const v=invs().find(x=>x.id==='roy');invFlow(v,e.royIn*extNav())}   /* lot 122 */\n")
# 10. le desk : objectif du trimestre en haut
rep("\"Le desk vous attend\",\n  [`Liquidité des marchés","\"Le desk vous attend\",\n  [`🎯 <b>Objectif du trimestre : ${sgnp(0.03,1)} net</b> (annonce standard ; vous pourrez promettre plus après le book).`,`Liquidité des marchés")
open('index.html','w',encoding='utf-8').write(s);print('lot122 p1 ok')
