p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
rep("""  sigBonus:0,capture:0.60,tcMult:1.0,rumBonus:0.10,lpMult:1.25,modelScale:0.90,incMult:0.9,incSev:1.0,numeric:false,tailH:true}
];""","""  sigBonus:0,capture:0.60,tcMult:1.0,rumBonus:0.10,lpMult:1.25,modelScale:0.90,incMult:0.9,incSev:1.0,numeric:false,tailH:true},
 {id:'act',sum:{pw:"l'attaque : une fois par an, un pari géant contre une banque centrale",f:["identifie presque toujours les extrêmes","la valeur lue trois fois plus nettement","commission de performance +5 pts : la légende se paie"],w:["coûts d'exécution +20 %, incidents plus fréquents et plus chers","investisseurs 10 % plus nerveux, comité sur ses gardes"]},lvl:'Expert',who:"« Quand on a raison, on n'en a jamais assez »",nm:"Macro activiste",
  p:"Vous ne suivez pas le marché : vous le faites. Une monnaie tenue à bout de bras par sa banque centrale, des réserves qui fondent, et vous qui pariez assez gros pour précipiter la chute. Ça a fait des fortunes, et des faillites. Le reste du temps, un macro discrétionnaire très convaincu.",
  ef:[['g',"<b>Pouvoir propre — l'attaque</b> : une fois par an, vous misez 5, 10 ou 15 % de l'encours contre une monnaie. Plus la mise est grosse, plus la banque centrale risque de céder (35 à 55 %, +10 pts si votre desk lit déjà la monnaie faible). Réussie : 1,2 fois la mise, et la légende. Ratée : la mise perdue, et le comité furieux"],['g',"veille des extrêmes : 25 à 90 % sentis, presque toujours identifiés (50 à 95 %)"],['g',"vous lisez la valeur trois fois plus nettement (bruit ×0,3) ; tendance et portage moins bien (×1,3)"],['b',"votre desk vise 23 % de vol : des convictions massives"],['b',"coûts de transaction +20 % : vous bougez le marché, il vous le rend"],['b',"incidents ×1,2, gravité ×1,3"],['b',"investisseurs 10 % plus nerveux"],['g',"commission de performance +5 pts ; capital de départ +1 M$"],['b',"équipe 20 % plus chère ; capture 75 %"]],
  sigBonus:2,capture:0.75,tcMult:1.20,rumBonus:0.12,lpMult:1.10,modelScale:1.15,incMult:1.2,incSev:1.3,numeric:false,atk:true}
];""")
rep("rv:0.02,tail:0.03};","rv:0.02,tail:0.03,act:0.05};")
rep("rv:0.0005,tail:0};","rv:0.0005,tail:0,act:0.001};")
rep("rv:1.10,tail:1.0};","rv:1.10,tail:1.0,act:1.20};")
rep("fonda:'v',rv:'c'},","fonda:'v',rv:'c',act:'v'},")
rep("tail:{s:0.32,i:0.45}};","tail:{s:0.32,i:0.45},act:{s:0.25,i:0.60}};")
rep(""" tail:{F:0.80,T:0.70,C:0.30,V:0.60,X:0.20,macro:1.0,mkt:1.0,""",""" act:{F:1.15,T:0.45,C:0.30,V:0.90,X:0,macro:1.45,mkt:0.50,
  txt:"Votre desk pèse d'abord les sources macro et la cherté des monnaies et des taux : il cherche la banque centrale qui ne pourra pas tenir."},
 tail:{F:0.80,T:0.70,C:0.30,V:0.60,X:0.20,macro:1.0,mkt:1.0,""")
rep('act:"25–90 % · 50–95 %"','act:"18–83 % · 55–95 %"')
s=s.replace("veille des extrêmes : 25 à 90 % sentis, presque toujours identifiés (50 à 95 %)","veille des extrêmes : 18 à 83 % sentis, presque toujours identifiés (55 à 95 %)")
# l'attaque : choix sur la page du book, issue à la clôture
rep("""function pwHere(o){""","""/* lot 272 : l'attaque du macro activiste */
const ATK={stake:0.05,win:1.2,p0:0.25,pm:0.10,read:0.10};
function atkReady(){return PROF().atk&&!(S.atk&&S.atk.q===S.q)&&(S.atkLast==null||S.q-S.atkLast>=4)}
function atkP(i,m){return Math.min(0.95,ATK.p0+ATK.pm*m+(expRet(i).m<0?ATK.read:0))}
function styDrawX(){const P=PROF();if(!P.atk)return '';const D=INSTR.map((x,i)=>i).filter(i=>INSTR[i].grp==='Devises'&&mktOpen(i));
 if(S.atk&&S.atk.q===S.q){const a=S.atk;return `<div class="blockhead"><h2>L'attaque</h2><span class="hint">lancée</span></div><p class="note" style="margin:0">🦅 Vous attaquez <b>${INSTR[a.i].nm}</b> avec ${Math.round(a.m*ATK.stake*100)} % de l'encours. La banque centrale cède avec une probabilité de ${Math.round(a.p*100)} % ; verdict à la clôture.</p>`}
 if(!atkReady())return `<div class="blockhead"><h2>L'attaque</h2><span class="hint">une par an</span></div><p class="note" style="margin:0">Prochaine attaque possible au trimestre ${(S.atkLast||0)+5}.</p>`;
 S.atkSel=S.atkSel??D[0];S.atkM=S.atkM||1;const i=S.atkSel,m=S.atkM,st=m*ATK.stake,p=atkP(i,m);
 return `<div class="blockhead"><h2>L'attaque</h2><span class="hint">une par an · votre pouvoir</span></div>
  <p class="note" style="margin:0 0 6px">Choisissez une monnaie et une mise. Plus la mise est grosse, plus la banque centrale risque de céder ; si votre desk lit déjà la monnaie faible, +10 pts.</p>
  <div class="cisel">${D.map(j=>`<button class="hgp${j===i?' on':''}" data-atk="${j}">${INSTR[j].sym}</button>`).join('')}</div>
  <div class="cisel" style="margin-top:6px">${[1,2,3].map(k=>`<button class="hgp${k===m?' on':''}" data-atm="${k}">${Math.round(k*ATK.stake*100)} %</button>`).join('')}</div>
  <div class="attr"><span class="an">Mise : ${mm(st*S.nav)} · la banque centrale cède à ${Math.round(p*100)} %</span><span class="av"><b class="pos-g">+${mm(ATK.win*st*S.nav)}</b> / <b class="neg-g">−${mm(st*S.nav)}</b></span></div>
  <button class="buy" id="atkgo" style="margin-top:6px">Lancer l'attaque sur ${INSTR[i].sym}</button>`}
function styWire(el){el.querySelectorAll('[data-atk]').forEach(b=>b.onclick=()=>{S.atkSel=+b.dataset.atk;styDraw()});el.querySelectorAll('[data-atm]').forEach(b=>b.onclick=()=>{S.atkM=+b.dataset.atm;styDraw()});
 const g=el.querySelector('#atkgo');if(g)g.onclick=()=>{if(!atkReady())return;const i=S.atkSel,m=S.atkM;S.atk={q:S.q,i,m,p:atkP(i,m)};S.atkLast=S.q;gauge(0,-2,"Le comité apprend votre attaque");toast(`🦅 Attaque lancée sur <b>${INSTR[i].nm}</b>`);styDraw()}}
function atkClose(){S.atkRes=null;const a=S.atk;if(!a||a.q!==S.q)return;const ok=prng32(hash32('atk'+S.q,S.seed))()<a.p,st=a.m*ATK.stake,x=ok?ATK.win*st:-st,nb=S.nav;
 S.nav*=(1+x);S.qEvM=(S.qEvM||0)+x*nb;S.atkRes={ok,x,nm:INSTR[a.i].nm,sym:INSTR[a.i].sym};S.evLog.push({t:`Attaque sur ${INSTR[a.i].nm}`,pnl:x,m:x*nb,lp:0,rc:0});if(ok){S.atkWins=(S.atkWins||0)+1}}
function pwHere(o){""")
rep("""function resolveQuarter(){
 reseed('res');""","""function resolveQuarter(){
 atkClose();   /* lot 272 */
 reseed('res');""")
rep(""" if(S.prof==='tail'&&S.hedgeQ===S.q&&!S.stressQ)lpD.push(["Encore un trimestre à payer l'assurance",-2]);   /* lot 271 */""",""" if(S.prof==='tail'&&S.hedgeQ===S.q&&!S.stressQ)lpD.push(["Encore un trimestre à payer l'assurance",-2]);   /* lot 271 */
 if(S.atkRes)lpD.push([S.atkRes.ok?`L'attaque sur ${S.atkRes.nm} a réussi : la banque centrale a cédé`:`L'attaque sur ${S.atkRes.nm} a échoué : la banque centrale a tenu`,S.atkRes.ok?15:-10]);   /* lot 272 */""")
rep(""" if(S.commRes&&S.commRes.rc)rcD.push(""",""" if(S.atkRes&&!S.atkRes.ok)rcD.push(['Attaque ratée : le comité demande des comptes',-5]);   /* lot 272 */
 if(S.commRes&&S.commRes.rc)rcD.push(""")
rep(""" if(S.commRes&&S.commRes.just)add(""",""" if(S.atkRes)add(pk(["Financial Times","Bloomberg","Les Échos"],55),S.atkRes.ok?pk([`${F} a fait plier la banque centrale : ${S.atkRes.nm} décroche, le fonds encaisse ${sgnp(S.atkRes.x,1)}. On parle déjà de « l'homme qui a cassé » la monnaie`,`Coup de maître de ${F} contre ${S.atkRes.nm} : la banque centrale abandonne la défense de sa monnaie`],56):pk([`La banque centrale a tenu : ${F} perd ${sgnp(S.atkRes.x,1)} sur son attaque contre ${S.atkRes.nm}. Le gouverneur savoure`,`${F} se casse les dents sur ${S.atkRes.nm} : les réserves étaient plus profondes que prévu`],57));
 if(S.commRes&&S.commRes.just)add(""")
open(p,'w',encoding='utf-8').write(s)
