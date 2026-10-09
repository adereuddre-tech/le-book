p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
rep("""function budgetBp(){return BUDGET.reduce((a,b)=>a+b.lv[S.bud[b.id]].bp,0)+DESK().fixed*1e4+cntOn()}""",
"""/* lot 276 : les locaux — un seul lieu à la fois ; loyer en plus du budget (pb de la base d'équipe), progression linéaire ;
   déménager coûte un trimestre du nouveau loyer. La Défense est le défaut, compris dans le loyer du back office. */
const OFFICES=[
 {id:'garage',ic:'🔧',nm:"Un garage à Montreuil",bp:0,fx:{team:0.9,poach:1.3,lp:-1},d:"Équipe 10 % moins chère (on vient en jean) ; débauchage ×1,3 ; confiance −1 par trimestre : les investisseurs n'aiment pas l'odeur d'huile."},
 {id:'defense',ic:'🏢',nm:"La Défense, tour B, 27e étage",bp:0,fx:{},d:"Neutre. La moquette est grise, le café correct, la vue imprenable sur la tour d'en face."},
 {id:'montaigne',ic:'🥂',nm:"Avenue Montaigne",bp:10,fx:{lp:1,inc:1.05},d:"Confiance +1 par trimestre : les investisseurs aiment l'adresse ; incidents +5 % (les déjeuners s'allongent)."},
 {id:'mayfair',ic:'🎩',nm:"Mayfair, Londres",bp:20,fx:{poach:0.8,subs:1.10},d:"Débauchage ×0,8 : vos traders aiment le quartier ; souscriptions +10 %."},
 {id:'geneve',ic:'⛲',nm:"Genève, quai du Mont-Blanc",bp:30,fx:{out:0.8,rc:-0.5},d:"Rachats −20 % : les grandes familles sont patientes ; contrôle −0,5 par trimestre (le comité n'aime pas la discrétion)."},
 {id:'greenwich',ic:'🌳',nm:"Greenwich, Connecticut",bp:40,fx:{tc:0.92,subs:1.15},d:"Coûts d'exécution −8 % : tous les courtiers sont à deux rues ; souscriptions +15 %."},
 {id:'singapour',ic:'🌇',nm:"Singapour, Marina Bay",bp:50,fx:{asia:0.75,watch:0.05,cap:0.9},d:"Coûts −25 % sur l'Asie et les exotiques ; veille des extrêmes +5 pts ; décalage horaire : 10 % de mouvement capté en moins sur les dépêches."},
 {id:'monaco',ic:'🛥️',nm:"Monaco, sur un yacht",bp:60,fx:{lp:2,inc:1.25,rc:-1},d:"Confiance +2 par trimestre, presse flatteuse ; incidents ×1,25 et contrôle −1 par trimestre : on ne sait jamais où est le gérant."}];
function OFF(){return OFFICES[(S&&S.office!=null)?S.office:1]||OFFICES[1]}
function offFx(k,d){const v=OFF().fx[k];return v==null?(d==null?1:d):v}
function offBp(){const o=OFF();return o.bp+((S.officePrev!=null&&S.office!==S.officePrev)?o.bp:0)}
function teamBp(f){return f*offFx('team')}
function budgetBp(){return teamBp(BUDGET.reduce((a,b)=>a+b.lv[S.bud[b.id]].bp,0))+DESK().fixed*1e4+cntOn()+offBp()}""")
rep("""function budgetBpIf(id,lv){return BUDGET.reduce((a,b)=>a+b.lv[b.id===id?lv:S.bud[b.id]].bp,0)+DESK().fixed*1e4+cntOn()}""",
    """function budgetBpIf(id,lv){return teamBp(BUDGET.reduce((a,b)=>a+b.lv[b.id===id?lv:S.bud[b.id]].bp,0))+DESK().fixed*1e4+cntOn()+offBp()}""")
rep("""   const bp=BUDGET.reduce((a,b)=>a+b.lv[S.bud[b.id]].bp,0)+DESK().fixed*1e4;
   S.budBp=bp;S.budPrev={fo:S.bud.fo,bo:S.bud.bo};""","""   const bp=budgetBp()-cntOn();
   S.budBp=bp;S.budPrev={fo:S.bud.fo,bo:S.bud.bo};S.officePrev=S.office==null?1:S.office;   /* lot 276 */""")
rep("""   <div class="budtot"><span>Total du trimestre</span><b id="btot"></b></div>""","""   <div id="offs"></div>
   <div class="budtot"><span>Total du trimestre</span><b id="btot"></b></div>""")
rep("""function drawBuds(){""","""function drawOffs(){const el=document.getElementById('offs');if(!el)return;const cur=S.office==null?1:S.office,base=S.officePrev==null?1:S.officePrev;
 el.innerHTML=`<div class="brow"><div class="bh"><b><span class="bico">🏙️</span>Les locaux</b><span>${mm(OFF().bp*1e-4*budNav())} par trimestre${cur!==base&&OFF().bp?` · déménagement ${mm(OFF().bp*1e-4*budNav())}`:''}</span></div>
  <p class="note" style="margin:2px 0 6px">Un seul lieu à la fois. Déménager coûte un trimestre du nouveau loyer.</p>
  <div class="offl">${OFFICES.map((o,i)=>`<button class="offb${i===cur?' on':''}" data-off="${i}"><b>${o.ic} ${o.nm}</b><span>${o.bp?o.bp+' pb':'sans loyer en plus'}</span><small>${o.d}</small></button>`).join('')}</div></div>`;
 el.querySelectorAll('.offb').forEach(b=>b.onclick=()=>{S.office=+b.dataset.off;setOps();drawBuds();refreshStatus()})}
function drawBuds(){
 drawOffs();   /* lot 276 */""")
rep(""".epi{""",""".offl{display:grid;gap:5px}.offb{text-align:left;padding:7px 9px;border-radius:6px;background:var(--panel2);border:1px solid var(--line2);color:var(--txt);font-size:12.5px;display:grid;grid-template-columns:1fr auto;gap:2px 8px}.offb span{color:var(--gold);font-family:var(--mono);font-size:11px}.offb small{grid-column:1/-1;color:var(--dim);font-size:11px}.offb.on{border-color:var(--gold);background:rgba(214,178,94,.10)}
.epi{""")
# effets
rep("""function poachNow(){return Math.min(0.95,BONFX[bonEff()].p*(S.bonCutQ===S.q?BONCUT:1))}""","""function poachNow(){return Math.min(0.95,BONFX[bonEff()].p*(S.bonCutQ===S.q?BONCUT:1)*offFx('poach'))}""")
rep("""function invOutF(D){return Math.min(1,D.out*2*(1-S.lp/100)*(SIZE().flowMult||1))}""","""function invOutF(D){return Math.min(1,D.out*2*(1-S.lp/100)*(SIZE().flowMult||1)*offFx('out'))}""")
rep("""*(S.commFx&&S.commFx.q===S.q?S.commFx.m:1)}   /* lot 256 */""","""*(S.commFx&&S.commFx.q===S.q?S.commFx.m:1)*offFx('subs')}   /* lot 256 ; lot 276 */""")
s=s.replace("let pInc=0.09*ARCH().incMult*RISKM[S.bud.risk]*PROF().incMult+","let pInc=0.09*ARCH().incMult*RISKM[S.bud.risk]*PROF().incMult*offFx('inc')+")
rep(""" if(pwOn('jk'))m*=S.pwJK||1;""",""" m*=offFx('tc');if(OFF().fx.asia&&(x.grp==='Exotiques'||['TOPX','JGB','JPY','MXEF'].includes(x.sym)))m*=OFF().fx.asia;   /* lot 276 */
 if(pwOn('jk'))m*=S.pwJK||1;""")
rep("""function capNow(){return S.sc&&S.sc.cap!=null?S.sc.cap:PROF().capture}""","""function capNow(){return (S.sc&&S.sc.cap!=null?S.sc.cap:PROF().capture)*offFx('cap')}""")
rep(""" const sv=Math.max(0.10,Math.min(0.95,B.s+0.30*f+0.20*r+0.15*(b-0.5))),""",""" const sv=Math.max(0.10,Math.min(0.95,B.s+0.30*f+0.20*r+0.15*(b-0.5)+offFx('watch',0))),""")
rep(""" if(S.budBp>70)lpD.push(['Facture d\\'exploitation jugée lourde',-1.5]);""",""" if(S.budBp>70)lpD.push(['Facture d\\'exploitation jugée lourde',-1.5]);
 if(offFx('lp',0))lpD.push([`Les locaux : ${OFF().nm}`,offFx('lp',0)]);   /* lot 276 */""")
rep(""" const rcD=[];""",""" const rcD=[];if(offFx('rc',0))rcD.push([`Les locaux : ${OFF().nm}`,offFx('rc',0)]);   /* lot 276 */""")
open(p,'w',encoding='utf-8').write(s)
