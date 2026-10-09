p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
# 1. bloc sur la page du book
rep("""  <div class="block"><details><summary style="font-size:15px;color:var(--txt);font-weight:600">Risque ex-ante du book</summary>""",
    """  <div class="block" id="pwblk"></div>
  <div class="block"><details><summary style="font-size:15px;color:var(--txt);font-weight:600">Risque ex-ante du book</summary>""")
rep("""   commitOrders();screenCoinv();window.scrollTo(0,0);
 };
}""","""   commitOrders();screenCoinv();window.scrollTo(0,0);
 };
 pwDraw();   /* lot 268 */
}
/* lot 268 : un coup de pouce par personne et par trimestre (Mireille : une fois par mandat). Effets lus ailleurs par S.pw[id]===S.q. */
const PW=[
 {id:'jk',fo:0,ic:'🐣',nm:'Jean-Kevin',t:"Le tableur à couleurs",d:"Il « optimise » vos ordres : une chance sur deux de −10 % sur tous les coûts du trimestre, une sur deux de +10 % (bug)."},
 {id:'dw',fo:1,ic:'📞',nm:'Dwight',t:"Un bloc à la voix",d:"Vos ordres sur les actions passent sans impact de marché tout le trimestre : seule la fourchette est due."},
 {id:'ig',fo:2,ic:'🏦',nm:'Ingrid',t:"Lire l'adjudication",d:"Elle vous dit dans quel sens finira le marché de taux le plus parlant ce trimestre. Juste trois fois sur quatre."},
 {id:'bo',fo:3,ic:'🤖',nm:'Boris',t:"L'algorithme en urgence",d:"Surcoût d'urgence divisé par deux sur les devises ce trimestre (dépêches, extrêmes, rivalités)."},
 {id:'tu',fo:4,ic:'🛢️',nm:'Tuco',t:"Les cuves de Rotterdam",d:"Il vous dit dans quel sens finira la matière première la plus parlante ce trimestre. Juste quatre fois sur cinq : les cuves ne mentent pas."},
 {id:'wi',fo:5,ic:'🐉',nm:'Winnie',t:"Hong Kong d'abord",d:"Sur les dépêches qui touchent l'Asie ou les exotiques, vous captez 100 % du mouvement ce trimestre : elle a exécuté avant l'ouverture européenne."},
 {id:'ma',fo:6,ic:'📿',nm:'Sœur Marie-Alpha',t:"Le rééquilibrage béni",d:"Elle recale votre book sur le risque cible, ligne par ligne, et les ordres du début de trimestre coûtent 25 % de moins."},
 {id:'on',fo:7,ic:'🎓',nm:'Onésime',t:"Un plateau télé",d:"Confiance des investisseurs +5 tout de suite. Mais il parle trop : vos grosses lignes fuitent ce trimestre (coûts ×1,45)."},
 {id:'go',bo:1,ic:'🧮',nm:'Gontran',t:"Passer l'écriture",d:"Si un incident tombe ce trimestre, il le rattrape : le fonds n'en paie que la moitié, sans perte de confiance. Se joue sur l'écran de l'incident."},
 {id:'jo',bo:2,ic:'🗂️',nm:'Josiane',t:"Tout rapprocher",d:"Aucune fuite de vos positions ce trimestre, quoi qu'il arrive — même si Onésime passe à la télé."},
 {id:'fi',bo:3,ic:'🔎',nm:'Firmin',t:"Un audit propre",d:"Le rapport d'audit tombe à point : contrôle des risques +3."},
 {id:'mi',bo:4,ic:'⚖️',nm:'Mireille',t:"Plaider devant le comité",d:"Une fois par mandat, elle fait effacer un carton jaune."},
 {id:'so',bo:5,ic:'🛡️',nm:'Solange',t:"Exercice de crise",d:"Ce trimestre, le choc immédiat d'un événement extrême est réduit de 20 %, et une cyberattaque ne vous touche pas."}];
function pwHere(o){return o.fo!=null?(o.fo===0||here(o.fo)):(S.bud&&S.bud.bo>=o.bo)}
function pwOn(id){return !!(S&&S.pw&&S.pw[id]===S.q)}
function pwOk(o){if(!pwHere(o))return false;if(o.id==='mi')return !(S.pwMi)&&S.cards&&S.cards.y>0;return !pwOn(o.id)}
function pwTip(cls,rel,who){const c=[];for(let i=0;i<N;i++)if(mktOpen(i)&&INSTR[i].grp===cls)c.push(i);if(!c.length)return null;
 const i=c.sort((a,b)=>Math.abs(expRet(b).m)-Math.abs(expRet(a).m))[0],u=prng32(hash32('pw'+who+S.q,S.seed))(),up=(S.rBase[i]>0)===(u<rel);return {who,sym:INSTR[i].sym,nm:INSTR[i].nm,up}}
function pwUse(id){const o=PW.find(x=>x.id===id);if(!o||!pwOk(o))return;S.pw=S.pw||{};S.pw[id]=S.q;let msg='';
 if(id==='jk'){const g=prng32(hash32('jk'+S.q,S.seed))()<0.5;S.pwJK=g?0.9:1.1;msg=g?'Le tableur marche : coûts −10 % ce trimestre.':'Le tableur plante : coûts +10 % ce trimestre.'}
 if(id==='ig'||id==='tu'){const t=pwTip(id==='ig'?'Taux':'Matières premières',id==='ig'?0.75:0.8,o.nm);if(t){(S.pwTips=S.pwTips||[]).push(Object.assign(t,{q:S.q}));msg=`${o.nm} : ${t.nm} finira le trimestre en ${t.up?'hausse':'baisse'}.`}}
 if(id==='ma'){const sp=pvol(weights(S.k));if(sp>1e-6){const a=S.tgt/sp;S.k=S.k.map((v,i)=>clampK(i,Math.round(v*a)));drawRows();renderRisk();refreshSend();refreshGain()}msg='Book recalé sur la cible ; ordres du début de trimestre −25 %.'}
 if(id==='on'){gauge(5,0,'Onésime sur un plateau télé');if(!pwOn('jo'))S.leakQ=true;msg='Confiance +5. Vos lignes circulent sur le marché.'}
 if(id==='jo'){S.leakQ=false;msg='Aucune fuite possible ce trimestre.'}
 if(id==='fi'){gauge(0,3,"Audit propre de Firmin");msg='Contrôle des risques +3.'}
 if(id==='mi'){S.pwMi=1;S.cards.y=Math.max(0,S.cards.y-1);(S.cards.log=S.cards.log||[]).push({q:S.q,c:'effacé',why:'Mireille plaide devant le comité'});msg='Un carton jaune effacé.'}
 if(['dw','bo','wi','go','so'].includes(id))msg=o.d;
 toast(`${o.ic} <b>${o.nm}</b> · ${msg}`);refreshStatus();renderTC&&renderTC();pwDraw()}
function pwDraw(){const el=document.getElementById('pwblk');if(!el)return;const L=PW.filter(pwHere);
 const tips=(S.pwTips||[]).filter(t=>t.q===S.q);
 el.innerHTML=`<div class="blockhead"><h2>Votre équipe</h2><span class="hint">un coup de pouce chacun par trimestre</span></div>
  ${tips.map(t=>`<div class="flag" style="margin:0 0 8px"><span>📌 <b>${t.who}</b> : ${t.nm} finira le trimestre en <b>${t.up?'hausse':'baisse'}</b>.</span></div>`).join('')}
  <div class="pwl">${L.map(o=>{const on=pwOn(o.id)||(o.id==='mi'&&S.pwMi),ok=pwOk(o);return `<button class="pwb${on?' on':''}" data-pw="${o.id}"${ok?'':' disabled'}><b>${o.ic} ${o.nm} · ${o.t}</b><small>${o.d}${on?' <i>· joué</i>':''}</small></button>`}).join('')}</div>`;
 el.querySelectorAll('.pwb[data-pw]').forEach(b=>b.onclick=()=>pwUse(b.dataset.pw))}""")
rep(""".glo{""",""".pwl{display:grid;gap:6px}.pwb{text-align:left;padding:8px 10px;border-radius:6px;background:var(--panel2);border:1px solid var(--line2);color:var(--txt);font-size:12.5px}.pwb small{display:block;color:var(--dim);font-size:11.5px;margin-top:2px}.pwb.on{border-color:var(--gold)}.pwb[disabled]{opacity:.55}
.glo{""")
# 2. effets
rep(""" if((S.stars||[]).includes(INSTR[i].grp))m*=0.5;""",""" if((S.stars||[]).includes(INSTR[i].grp))m*=0.5;
 if(pwOn('jk'))m*=S.pwJK||1;if(pwOn('ma')&&S.phase==='book')m*=0.75;   /* lot 268 : Jean-Kevin, Sœur Marie-Alpha */""")
rep(""" const cost=bn*bp*1e-4,spr=Math.min(cost,bn*x.s*TCK*m*brake()*1e-4);
 return {cost,bp,bn,spr,imp:cost-spr};""",""" const cost=bn*bp*1e-4,spr=Math.min(cost,bn*x.s*TCK*m*brake()*1e-4);
 if(pwOn('dw')&&x.grp==='Actions')return {cost:spr,bp:spr/bn*1e4,bn,spr,imp:0};   /* lot 268 : Dwight, sans impact */
 return {cost,bp,bn,spr,imp:cost-spr};""")
rep("""function urgM(m,i){return covered(INSTR[i].grp)?m*2/3:m}""","""function urgM(m,i){if(pwOn('bo')&&INSTR[i].grp==='Devises'&&m>1)m=1+(m-1)/2;return covered(INSTR[i].grp)?m*2/3:m}   /* lot 268 : Boris */""")
rep(""" const SC=S.sc;if(SC.ph===undefined)SC.ph=SC.p;""",""" const SC=S.sc;if(SC.ph===undefined)SC.ph=SC.p;
 if(pwOn('wi')&&touched.some(i=>INSTR[i].grp==='Exotiques'||['TOPX','JGB','JPY','MXEF'].includes(INSTR[i].sym)))SC.cap=1;   /* lot 268 : Winnie */""")
rep(""" let hgB=0;if(ev.x&&S.hedgeQ===S.q&&imm<0){hgB=-imm*HEDGE.h;imm+=hgB}   /* lot 253 : protection */""",""" let hgB=0;if(ev.x&&S.hedgeQ===S.q&&imm<0){hgB=-imm*HEDGE.h;imm+=hgB}   /* lot 253 : protection */
 if(ev.stress&&pwOn('so')&&imm<0)imm*=ev.stress==='cyber'?0:0.8;   /* lot 268 : Solange */""")
s=s.replace("if(e.leakQ)S.leakQ=true","if(e.leakQ&&!pwOn('jo'))S.leakQ=true")
rep("""  {b:"Contenir et communiquer plus tard",s:"Le fonds n'absorbe que la moitié. Quand l'affaire sort, la confiance le paie cher.",f:0.5*loss,m:0,lp:inc.lp*sev*2.2-4,rc:inc.rc*sev*2}];""",
    """  {b:"Contenir et communiquer plus tard",s:"Le fonds n'absorbe que la moitié. Quand l'affaire sort, la confiance le paie cher.",f:0.5*loss,m:0,lp:inc.lp*sev*2.2-4,rc:inc.rc*sev*2}];
 if(pwOn('go')&&S.pwGo!==S.q)O.push({b:"Gontran passe l'écriture",s:"Il rattrape l'erreur dans les comptes : le fonds n'en paie que la moitié, et personne n'en entend parler.",f:0.5*loss,m:0,lp:0,rc:0,go:1});   /* lot 268 */""")
rep(""" const pickI=k=>{clearTimer();const o=O[k];S.nav*=(1-o.f);""",""" const pickI=k=>{clearTimer();const o=O[k];if(o.go)S.pwGo=S.q;S.nav*=(1-o.f);""")
open(p,'w',encoding='utf-8').write(s)
