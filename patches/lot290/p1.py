p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
# 1. nouvelle liste : une fois par an et par personne, impact renforcé
a=s.index("const PW=[");b=s.index("function pwDraw(){",a)
mid=s[s.index("}];",a)+3:s.index("function pwHere",a)]   # pouvoirs de style (styDraw, attaque) : conservés
e=s.index("\n/* Les ordres sortent de la poche du gérant",b)
s=s[:a]+r"""/* lot 290 : un coup de pouce par personne et par an (Mireille : une fois par mandat), impact renforcé.
   Pouvoirs d'action : armés, désarmables jusqu'à « Passer les ordres », qui les confirme (pwCommit).
   Pouvoirs d'information (Ingrid, Tuco) : joués à la lecture, après confirmation. Gontran se joue sur l'écran de l'incident. */
const PW=[
 {id:'jk',fo:0,ic:'🐣',nm:'Jean-Kevin',t:"Le tableur à couleurs",d:"Il « optimise » vos ordres du trimestre : une chance sur deux de −20 % sur tous les coûts, une sur deux de +20 % (bug). Le verdict tombe à l'exécution."},
 {id:'dw',fo:1,ic:'📞',nm:'Dwight',t:"Un bloc à la voix",d:"Vos ordres sur les actions passent sans impact de marché tout le trimestre : seule la fourchette est due."},
 {id:'ig',fo:2,ic:'🏦',nm:'Ingrid',info:1,t:"Lire l'adjudication",d:"Elle vous dit dans quel sens finira le marché de taux le plus parlant ce trimestre. Juste quatre fois sur cinq."},
 {id:'bo',fo:3,ic:'🤖',nm:'Boris',t:"L'algorithme en urgence",d:"Surcoût d'urgence divisé par trois sur les devises ce trimestre (dépêches, extrêmes, rivalités)."},
 {id:'tu',fo:4,ic:'🛢️',nm:'Tuco',info:1,t:"Les cuves de Rotterdam",d:"Il vous dit dans quel sens finira la matière première la plus parlante ce trimestre. Juste 85 fois sur 100 : les cuves ne mentent pas."},
 {id:'wi',fo:5,ic:'🐉',nm:'Winnie',t:"Hong Kong d'abord",d:"Sur les dépêches qui touchent l'Asie ou les exotiques, vous captez 100 % du mouvement ce trimestre : elle a exécuté avant l'ouverture européenne."},
 {id:'ma',fo:6,ic:'📿',nm:'Sœur Marie-Alpha',t:"Le rééquilibrage béni",d:"Elle recale votre book sur le risque de croisière (deux tiers de la limite du comité), ligne par ligne, et les ordres du début de trimestre coûtent 40 % de moins."},
 {id:'on',fo:7,ic:'🎓',nm:'Onésime',t:"Un plateau télé",d:"Confiance des investisseurs +8. Mais il parle trop : vos grosses lignes fuitent ce trimestre (coûts ×1,45), sauf si Josiane veille."},
 {id:'go',bo:1,ic:'🧮',nm:'Gontran',inc:1,t:"Passer l'écriture",d:"Si un incident tombe, il le rattrape : le fonds n'en paie qu'un quart, sans perte de confiance. Se joue sur l'écran de l'incident."},
 {id:'jo',bo:2,ic:'🗂️',nm:'Josiane',t:"Tout rapprocher",d:"Aucune fuite de vos positions ce trimestre, quoi qu'il arrive — même si Onésime passe à la télé."},
 {id:'fi',bo:3,ic:'🔎',nm:'Firmin',t:"Un audit propre",d:"Le rapport d'audit annuel tombe à point : contrôle des risques +5."},
 {id:'mi',bo:4,ic:'⚖️',nm:'Mireille',t:"Plaider devant le comité",d:"Une fois par mandat, elle fait effacer un carton jaune."},
 {id:'so',bo:5,ic:'🛡️',nm:'Solange',t:"Exercice de crise",d:"Ce trimestre, le choc immédiat d'un événement extrême est réduit de 35 %, et une cyberattaque ne vous touche pas."}];"""+mid+r"""function pwHere(o){return o.fo!=null?(o.fo===0||here(o.fo)):(S.bud&&S.bud.bo>=o.bo)}
function pwOn(id){return !!(S&&S.pw&&S.pw[id]===S.q)}
function pwBack(id){const l=S.pwLast&&S.pwLast[id];return l==null?0:l+4}   /* trimestre où le pouvoir revient */
function pwAvail(o){if(!pwHere(o))return false;if(o.id==='mi')return !S.pwMi&&S.cards&&S.cards.y>0;return S.q>=pwBack(o.id)}
function pwOk(o){return pwOn(o.id)?!o.info&&S.phase==='book':pwAvail(o)&&!o.inc}
function pwTip(cls,rel,who){const c=[];for(let i=0;i<N;i++)if(mktOpen(i)&&INSTR[i].grp===cls)c.push(i);if(!c.length)return null;
 const i=c.sort((a,b)=>Math.abs(expRet(b).m)-Math.abs(expRet(a).m))[0],u=prng32(hash32('pw'+who+S.q,S.seed))(),up=(S.rBase[i]>0)===(u<rel);return {who,sym:INSTR[i].sym,nm:INSTR[i].nm,up}}
function pwUse(id){const o=PW.find(x=>x.id===id);if(!o||!pwOk(o))return;S.pw=S.pw||{};S.pwLast=S.pwLast||{};
 if(o.info){if(S.pwConf!==id){S.pwConf=id;pwDraw();return}S.pwConf=null;S.pw[id]=S.q;S.pwLast[id]=S.q;
  const t=pwTip(id==='ig'?'Taux':'Matières premières',id==='ig'?0.80:0.85,o.nm);if(t)(S.pwTips=S.pwTips||[]).push(Object.assign(t,{q:S.q}));
  toast(`${o.ic} <b>${o.nm}</b> · ${t?`${t.nm} finira le trimestre en ${t.up?'hausse':'baisse'}`:'rien à dire ce trimestre'}. Compté pour l'année.`);pwDraw();return}
 if(pwOn(id)){delete S.pw[id];if(id==='ma'&&S.pwMaK){S.k=S.pwMaK;S.pwMaK=null;drawRows();renderRisk();refreshSend();refreshGain()}toast(`${o.ic} <b>${o.nm}</b> · désarmé.`)}
 else{S.pw[id]=S.q;if(id==='jk')S.pwJK=null;if(id==='ma'){S.pwMaK=[...S.k];const sp=pvol(weights(S.k));if(sp>1e-6){const a=cruise()/sp;S.k=S.k.map((v,i)=>clampK(i,Math.round(v*a)));drawRows();renderRisk();refreshSend();refreshGain()}}
  toast(`${o.ic} <b>${o.nm}</b> · armé : confirmé quand vous passerez les ordres.`)}
 refreshStatus();renderTC&&renderTC();pwDraw()}
/* à « Passer les ordres » : les pouvoirs armés sont joués et comptés pour l'année */
function pwCommit(){if(!S.pw)return;S.pwLast=S.pwLast||{};S.pwMaK=null;
 PW.forEach(o=>{if(o.info||!pwOn(o.id)||S.pwLast[o.id]===S.q)return;S.pwLast[o.id]=S.q;
  if(o.id==='jk')S.pwJK=prng32(hash32('jk'+S.q,S.seed))()<0.5?0.8:1.2;
  if(o.id==='on'){gauge(8,0,'Onésime sur un plateau télé');if(!pwOn('jo'))S.leakQ=true}
  if(o.id==='jo')S.leakQ=false;
  if(o.id==='fi')gauge(0,5,"Audit propre de Firmin");
  if(o.id==='mi'){S.pwMi=1;S.cards.y=Math.max(0,S.cards.y-1);(S.cards.log=S.cards.log||[]).push({q:S.q,c:'effacé',why:'Mireille plaide devant le comité'})}});
 if(pwOn('jk'))toast(S.pwJK<1?'🐣 Le tableur de Jean-Kevin marche : coûts −20 % ce trimestre.':'🐣 Le tableur de Jean-Kevin plante : coûts +20 % ce trimestre.')}
function pwDraw(){const el=document.getElementById('pwblk');if(!el)return;const L=PW.filter(pwHere);
 const tips=(S.pwTips||[]).filter(t=>t.q===S.q);
 el.innerHTML=`<div class="blockhead"><h2>Votre équipe</h2><span class="hint">un coup de pouce chacun par an</span></div>
  ${tips.map(t=>`<div class="flag" style="margin:0 0 8px"><span>📌 <b>${t.who}</b> : ${t.nm} finira le trimestre en <b>${t.up?'hausse':'baisse'}</b>.</span></div>`).join('')}
  <div class="pwl">${L.map(o=>{const on=pwOn(o.id),ok=pwOk(o),back=pwBack(o.id);
   const st=on?(o.info?'joué ce trimestre':'armé · touchez pour désarmer'):o.inc?(pwAvail(o)?'disponible · se joue sur l’incident':`revient au trimestre ${back+1}`):o.id==='mi'?(S.pwMi?'joué pour le mandat':S.cards&&S.cards.y?'disponible':'aucun carton à effacer'):pwAvail(o)?(S.pwConf===o.id?'touchez encore pour confirmer : compté pour l’année':'disponible'):`revient au trimestre ${back+1}`;
   return `<button class="pwb${on?' on':''}${S.pwConf===o.id?' conf':''}" data-pw="${o.id}"${ok?'':' disabled'}><b>${o.ic} ${o.nm} · ${o.t}</b><small>${o.d} <i>· ${st}</i></small></button>`}).join('')}</div>`;
 el.querySelectorAll('.pwb[data-pw]').forEach(b=>b.onclick=()=>pwUse(b.dataset.pw))}"""+s[e:]
rep("""   commitOrders();screenCoinv();window.scrollTo(0,0);""","""   pwCommit();commitOrders();screenCoinv();window.scrollTo(0,0);   /* lot 290 */""")
# 2. effets renforcés
rep("if(pwOn('jk'))m*=S.pwJK||1;if(pwOn('ma')&&S.phase==='book')m*=0.75;","if(pwOn('jk')&&S.pwJK)m*=S.pwJK;if(pwOn('ma')&&S.phase==='book')m*=0.6;")
rep("function urgM(m,i){if(pwOn('bo')&&INSTR[i].grp==='Devises'&&m>1)m=1+(m-1)/2;","function urgM(m,i){if(pwOn('bo')&&INSTR[i].grp==='Devises'&&m>1)m=1+(m-1)/3;")
rep("if(ev.stress&&pwOn('so')&&imm<0)imm*=ev.stress==='cyber'?0:0.8;","if(ev.stress&&pwOn('so')&&imm<0)imm*=ev.stress==='cyber'?0:0.65;")
rep("""if(pwOn('go')&&S.pwGo!==S.q)O.push({b:"Gontran passe l'écriture",s:"Il rattrape l'erreur dans les comptes : le fonds n'en paie que la moitié, et personne n'en entend parler.",f:0.5*loss,m:0,lp:0,rc:0,go:1});""",
    """{const g=PW.find(x=>x.id==='go');if(g&&pwAvail(g))O.push({b:"Gontran passe l'écriture",s:"Il rattrape l'erreur dans les comptes : le fonds n'en paie qu'un quart, et personne n'en entend parler. Compté pour l'année.",f:0.25*loss,m:0,lp:0,rc:0,go:1})}""")
rep("""const pickI=k=>{clearTimer();const o=O[k];if(o.go)S.pwGo=S.q;""","""const pickI=k=>{clearTimer();const o=O[k];if(o.go){S.pwLast=S.pwLast||{};S.pwLast.go=S.q}""")
rep(""".pwb.on{border-color:var(--gold)}""",""".pwb.on{border-color:var(--gold);background:rgba(214,178,94,.10)}.pwb.conf{border-color:var(--warn)}""")
open(p,'w',encoding='utf-8').write(s)
