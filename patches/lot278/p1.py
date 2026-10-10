p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
a=s.index("const OFFICES=[");b=s.index("];",a)+2
s=s[:a]+"""const OFFICES=[   /* lot 278 : départ au garage ; chaque cran vaut un peu plus que son loyer — aucun optimum où rester bloqué */
 {id:'garage',ic:'🔧',nm:"Un garage à Levallois",bp:1,fx:{team:0.95,poach:1.2},d:"Le point de départ. Équipe 5 % moins chère (on vient en jean) ; débauchage ×1,2 : on part vite d'un garage."},
 {id:'defense',ic:'🏢',nm:"La Défense, tour B, 27e étage",bp:10,fx:{lp:0.5,subs:1.05},d:"Une vraie adresse : confiance +0,5 par trimestre, souscriptions +5 %. La moquette est grise, la vue imprenable sur la tour d'en face."},
 {id:'montaigne',ic:'🥂',nm:"Avenue Montaigne",bp:20,fx:{lp:1,subs:1.08,poach:0.95},d:"Confiance +1 par trimestre : les investisseurs aiment l'adresse ; souscriptions +8 % ; débauchage ×0,95. Les déjeuners s'allongent."},
 {id:'mayfair',ic:'🎩',nm:"Mayfair, Londres",bp:30,fx:{lp:1,subs:1.12,poach:0.8},d:"Confiance +1 ; souscriptions +12 % ; débauchage ×0,8 : vos traders aiment le quartier, et le pub d'en bas."},
 {id:'geneve',ic:'⛲',nm:"Genève, quai du Mont-Blanc",bp:40,fx:{lp:1,subs:1.12,poach:0.8,out:0.8},d:"Les grandes familles sont patientes : rachats −20 %, en plus des avantages de Mayfair. Le secret bancaire a ses charmes."},
 {id:'greenwich',ic:'🌳',nm:"Greenwich, Connecticut",bp:50,fx:{lp:1,subs:1.18,poach:0.75,out:0.8,tc:0.93},d:"Tous les courtiers à deux rues : coûts d'exécution −7 % ; souscriptions +18 % ; débauchage ×0,75 ; rachats −20 %."},
 {id:'singapour',ic:'🌇',nm:"Singapour, Marina Bay",bp:60,fx:{lp:1,subs:1.2,poach:0.75,out:0.8,tc:0.93,asia:0.75,watch:0.05},d:"Tout Greenwich, plus l'Asie : coûts −25 % sur l'Asie et les exotiques, veille des extrêmes +5 pts. Le décalage horaire se gère au café."},
 {id:'monaco',ic:'🛥️',nm:"Monaco, sur un yacht",bp:70,fx:{lp:2,subs:1.25,poach:0.7,out:0.75,tc:0.93,asia:0.75,watch:0.05,inc:1.1},d:"Le sommet : confiance +2 par trimestre, souscriptions +25 %, rachats −25 %, débauchage ×0,7. Seul défaut : incidents ×1,1 — on ne sait jamais où est le gérant."}];"""+s[b:]
rep("""function OFF(){return OFFICES[(S&&S.office!=null)?S.office:1]||OFFICES[1]}""","""function OFF(){return OFFICES[(S&&S.office!=null)?S.office:0]||OFFICES[0]}""")
rep("""S.officePrev=S.office==null?1:S.office;   /* lot 276 */""","""S.officePrev=S.office==null?0:S.office;   /* lot 276 */""")
rep("""const cur=S.office==null?1:S.office,base=S.officePrev==null?1:S.officePrev;""","""const cur=S.office==null?0:S.office,base=S.officePrev==null?0:S.officePrev;""")
rep("""<span>${o.bp?o.bp+' pb':'sans loyer en plus'}</span>""","""<span>${o.bp} pb</span>""")
rep("""  <p class="note" style="margin:2px 0 6px">Un seul lieu à la fois. Déménager coûte un trimestre du nouveau loyer.</p>""","""  <p class="note" style="margin:2px 0 6px">Un seul lieu à la fois, du garage au yacht ; chaque adresse fait un peu mieux que son loyer. Déménager coûte un trimestre du nouveau loyer.</p>""")
open(p,'w',encoding='utf-8').write(s)
s=open(p,encoding='utf-8').read()
rep("""function offBp(){const o=OFF();return o.bp+((S.officePrev!=null&&S.office!==S.officePrev)?o.bp:0)}""","""function offBp(){const o=OFF();return o.bp+((S.officePrev!=null&&(S.office??0)!==S.officePrev)?o.bp:0)}""")
open(p,'w',encoding='utf-8').write(s)
