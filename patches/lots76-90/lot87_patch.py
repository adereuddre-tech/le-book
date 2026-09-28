P='/home/claude/le-book/index.html';s=open(P,encoding='utf-8').read()
def rep(old,new,k=1):
    global s;n=s.count(old);assert n==k,(n,old[:100]);s=s.replace(old,new)
import re
# annonce : trois crans fixes
m=re.search(r"  \{id:'none',ico:'🤐'.*?ret:3\*g,win:\{lp:15,rc:15\},lose:\{lp:-15,rc:-15\}\}\n",s,re.S);assert m
s=s[:m.start()]+"""  {id:'prud',ico:'📄',nm:"Communication standard",who:"« Nous visons un trimestre solide »",p:`Vous annoncez ${pctc(0.03)} sur le trimestre. C'est ce que les investisseurs attendent d'un fonds macro : le tenir rassure, le manquer se remarque.`,
   ret:0.03,win:{lp:4,rc:4},lose:{lp:-4,rc:-4}},
  {id:'fort',ico:'📣',nm:"Conviction forte",who:"« C'est le trimestre de l'année »",p:`Vous annoncez ${pctc(0.09)}. Si vous y arrivez, on vous croira sur parole pendant longtemps. Sinon, on s'en souviendra aussi longtemps.`,
   ret:0.09,win:{lp:12,rc:12},lose:{lp:-12,rc:-12}},
  {id:'gourou',ico:'🔮',nm:"Prophétie de gourou",who:"« Nous allons écraser le marché »",p:`Vous annoncez ${pctc(0.15)} en un trimestre, devant les caméras. Tenu, vous entrez dans la légende des dîners en ville ; manqué, dans les mèmes des salles de marché.`,
   ret:0.15,win:{lp:22,rc:22},lose:{lp:-25,rc:-25}}
"""+s[m.end():]
rep('t:c=>c.comm===\'none\'&&c.q>0,b:0.07}',"t:c=>c.comm==='none'&&c.q>0,b:0.07,pre:'never'}")
rep("preOk=g=>!g.pre||(g.pre==='loss'?lastQ<0:lastQ>0);","preOk=g=>!g.pre||(g.pre==='never'?false:g.pre==='loss'?lastQ<0:lastQ>0);")
# marchés : risque à deux décimales
rep("pct1=v=>`<b class=\"${v>0.05?'neg-g':v<-0.05?'pos-g':'dim-g'}\">${v>=0?'+':'−'}${dec(Math.abs(v),1)} %</b>`","pct1=v=>`<b class=\"${v>0.005?'neg-g':v<-0.005?'pos-g':'dim-g'}\">${v>=0?'+':'−'}${dec(Math.abs(v),2)} %</b>`")
# systématique : le book du modèle à découvert
num="""   ${PROF().numeric?`<div class="wire" style="margin-bottom:8px"><div class="kv" style="padding-bottom:6px"><span><b>Le book que le modèle construirait</b></span></div><div id="factest"></div></div>`:''}\n"""
rep(num,"")
rep("""   <div class="wire" id="news"></div>\n   <details style="margin-top:8px"><summary>Sous le capot""","""   <div class="wire" id="news"></div>\n"""+num.replace('margin-bottom:8px','margin:10px 0 8px')+"""   <details style="margin-top:8px"><summary>Sous le capot""")
# trésorerie : point de départ du trimestre ; flux cumulés
rep("S.qMgmtM=VOL().mgmt*S.nav;S.nav-=S.qMgmtM;S.mgrFees+=S.qMgmtM;refreshGain();","S.tresQ0=mgrCash();   /* lot 87 */\n S.qMgmtM=VOL().mgmt*S.nav;S.nav-=S.qMgmtM;S.mgrFees+=S.qMgmtM;refreshGain();")
rep("S.qColM=0;S.colBaseNav=0;S.rumors=[];","S.flowInC=(S.flowInC||0)+Math.max(0,S.qFlow||0);S.flowOutC=(S.flowOutC||0)+Math.max(0,-(S.qFlow||0));   /* lot 87 : flux cumulés */\n S.qColM=0;S.colBaseNav=0;S.rumors=[];")
# pop-up d'encours : le détail
rep("['Flux nets d\\'encours (collecte − rachats)',bn(S.flows||0)],",
    "['Souscriptions cumulées',S.flowInC?'+'+mm(S.flowInC):'aucune'],['Rachats cumulés',S.flowOutC?'−'+mm(S.flowOutC):'aucun'],['Flux nets d\\'encours (collecte − rachats)',bn(S.flows||0)],['Dont votre co-investissement',`${mm(S.coinvIn||0)} · ${Math.round(coinvPct()*100)} % de la trésorerie`],['Part de l\\'encours à vous',dec(100*(S.coinvIn||0)/Math.max(1e-9,navNow()),1)+' %'],['Encours sous gestion, hors vous',moneyB(navNow()-(S.coinvIn||0))],['Seuil de fermeture',moneyB(FUNDMIN)],")
# débriefing : tableau de la trésorerie
rep("""  </tbody></table>
 </div>`;
 const coSel=""","""  </tbody></table>
  ${(()=>{const T0=S.tresQ0!==undefined?S.tresQ0:0,T1=mgrCash(),it=[['Commission de gestion',Gq.mgmt||0],['Commission de performance',Gq.perf||0],["Bonus d'objectif",bon],['Co-investissement',Gq.coinv||0],['Restitution',-(Gq.claw||0)],["Budget d'exploitation",-(Gq.ops||0)],["Coûts d'exécution",-(Gq.tc||0)]];
   const oth=T1-T0-it.reduce((a,x)=>a+x[1],0);if(Math.abs(oth)>1e-7)it.push(['Autres (accidents, incidents, desk payés par vous)',oth]);
   return `<table class="qt" style="margin-top:12px"><thead><tr><th style="text-align:left">Trésorerie</th><th>M$</th></tr></thead><tbody>
    <tr><td style="text-align:left">Début du trimestre</td><td>${mm(T0)}</td></tr>
    ${it.filter(x=>Math.abs(x[1])>1e-9).map(x=>`<tr><td style="text-align:left">${x[0]}</td><td class="${cls(x[1])}">${x[1]>=0?'+':'−'}${mm(Math.abs(x[1]))}</td></tr>`).join('')}
    <tr class="me"><td style="text-align:left"><b>Fin du trimestre</b></td><td><b class="gold-g">${mm(T1)}</b></td></tr></tbody></table>`})()}
 </div>`;
 const coSel=""")
open(P,'w',encoding='utf-8').write(s);print('ok')
