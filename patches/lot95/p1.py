# Lot 95 : bonus d'équipe (validé par Antoine) et classe sans trader ×4.
# Au débriefing d'un trimestre à commission de performance positive : 0 / 10 / 25 % de cette commission, versés à
# l'ouverture suivante (avant le co-investissement). Débauchage à la clôture de ce trimestre ×1 / ×0,6 / ×0,3 ;
# un bénéficiaire, intouchable, coûts de sa classe −10 %. Deux trimestres gagnants d'affilée sans bonus : grogne, ×1,5.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep('NOTRD=5,','NOTRD=4,')
rep("function covered(g){",r'''const BONUS=[0,0.10,0.25],BONM=[1,0.6,0.3],GROGNE=1.5;
function bonCands(){const c=[];for(let p=FOP.length-1;p>=0;p--)if(here(p))c.push(p);return c}
function bonTxt(){if(S.qBonT>0){const w=S.bonWhoQ!=null?FOP[S.bonWhoQ]:null;return `<br>Bonus d'équipe versé : ${mm(S.qBonT)} · débauchage ×${dec(S.bonMultQ,1)}${w?` · ${w.who} intouchable${w.cls?`, ${w.cls.toLowerCase()} −10 %`:''}`:''}`}
 return S.bonMultQ>1?`<br><span class="neg-g">Le desk grogne : deux trimestres gagnants sans bonus. Débauchage ×${dec(GROGNE,1)} ce trimestre.</span>`:''}
function payBonus(){S.qBonT=0;S.bonWhoQ=null;S.bonMultQ=1;if(S.q<1)return;const perf=(S.mgrQ&&S.mgrQ.perf)||0,i=S.bonI||0;
 if(perf>0)S.noBon=i>0?0:(S.noBon||0)+1;
 const amt=Math.min(BONUS[i]*Math.max(0,perf),Math.max(0,mgrCash()));
 if(amt>0){S.mgrCosts+=amt;S.cBonT=(S.cBonT||0)+amt;S.qBonT=amt;S.bonMultQ=BONM[i];const w=S.bonWho;S.bonWhoQ=(w!=null&&here(w))?w:(bonCands()[0]??null)}
 else if((S.noBon||0)>=2){S.bonMultQ=GROGNE;S.noBon=0}
 S.bonI=0}
function covered(g){''')
rep("S.tresQ0=mgrCash();   /* lot 87 */","S.tresQ0=mgrCash();   /* lot 87 */\n payBonus();   /* lot 95 */")
rep("if(!covered(x.grp))m*=NOTRD;","if(!covered(x.grp))m*=NOTRD;\n if(S.bonWhoQ!=null&&FOP[S.bonWhoQ]&&FOP[S.bonWhoQ].cls===x.grp)m*=0.9;   /* lot 95 : bénéficiaire du bonus */")
rep("if(tot<-0.01&&rng()<(0.5+S.poachBoost)*RETM[S.bud.ret]*(rel<-0.005?1:0.4)){","if(tot<-0.01&&rng()<(0.5+S.poachBoost)*RETM[S.bud.ret]*(rel<-0.005?1:0.4)*(S.bonMultQ||1)){")
rep("for(let p=1;p<=S.bud.fo;p++)if(here(p))cands.push(p);","for(let p=1;p<=S.bud.fo;p++)if(here(p)&&p!==S.bonWhoQ)cands.push(p);")
rep("<div class=\"lvef\">${budEf(b.id,cur)}${b.id==='fo'?covTxt():''}</div>","<div class=\"lvef\">${budEf(b.id,cur)}${b.id==='fo'?covTxt()+bonTxt():''}</div>")
# débriefing
rep("const coSel=(S.over||S.q>=QT())?'':`","const bnSel=(S.over||S.q>=QT()||!((S.mgrQ&&S.mgrQ.perf)>0))?'':(()=>{const pf=S.mgrQ.perf,C=bonCands(),w=(S.bonWho!=null&&C.includes(S.bonWho))?S.bonWho:C[0];S.bonWho=w;\n  return `<div class=\"block\"><div class=\"blockhead\"><h2>Bonus d'équipe</h2><span class=\"hint\">versé à l'ouverture</span></div>\n  <p class=\"note\" style=\"margin-top:0\">Une part de votre commission de performance (${mm(pf)}), versée à l'équipe. Elle calme les chasseurs de têtes au trimestre prochain ; un bénéficiaire désigné est intouchable et fait baisser de 10 % les coûts de sa classe.${(S.noBon||0)>=1?` <b class=\"neg-g\">Le trimestre gagnant précédent s'est passé de bonus : un second sans rien et le desk grogne (débauchage ×${dec(GROGNE,1)}).</b>`:''}</p>\n  <div class=\"cisel\">${BONUS.map((p,i)=>`<button class=\"bnp${i===(S.bonI||0)?' on':''}\" data-i=\"${i}\">${Math.round(p*100)} %<br><small>${mm(p*pf)} · ×${dec(BONM[i],1)}</small></button>`).join('')}</div>\n  <div class=\"cisel\" style=\"flex-wrap:wrap\">${C.map(p=>`<button class=\"bnw${p===w?' on':''}\" data-p=\"${p}\">${FOP[p].ic} ${FOP[p].who}</button>`).join('')}</div></div>`})();\n const coSel=(S.over||S.q>=QT())?'':`")
rep("${warn.map(t=>`<div class=\"flag\" style=\"margin-top:12px\"><span>${t}</span></div>`).join('')}${coSel}","${warn.map(t=>`<div class=\"flag\" style=\"margin-top:12px\"><span>${t}</span></div>`).join('')}${bnSel}${coSel}")
rep("app.querySelectorAll('.cip').forEach(b=>b.onclick=()=>{S.coinvPct=+b.dataset.p;","app.querySelectorAll('.bnp').forEach(b=>b.onclick=()=>{S.bonI=+b.dataset.i;app.querySelectorAll('.bnp').forEach(x=>x.classList.toggle('on',x===b))});\n app.querySelectorAll('.bnw').forEach(b=>b.onclick=()=>{S.bonWho=+b.dataset.p;app.querySelectorAll('.bnw').forEach(x=>x.classList.toggle('on',x===b))});\n app.querySelectorAll('.cip').forEach(b=>b.onclick=()=>{S.coinvPct=+b.dataset.p;")
rep(".cisel .cip.on{border-color:var(--gold);color:var(--gold)}",".cisel .cip.on{border-color:var(--gold);color:var(--gold)}\n.cisel .bnp,.cisel .bnw{flex:1;padding:8px 4px;border-radius:6px;background:var(--panel2);border:1px solid var(--line2);color:var(--txt);font-size:12.5px}.cisel .bnp small{color:var(--dim);font-size:10.5px}.cisel .bnw{flex:0 0 auto;padding:6px 9px}.cisel .bnp.on,.cisel .bnw.on{border-color:var(--gold);color:var(--gold)}")
# comptes
rep("[`Budget d'exploitation`,-(S.cOps||0)],","[`Budget d'exploitation`,-(S.cOps||0)],[`Bonus d'équipe`,-(S.cBonT||0)],")
rep("[\"Budget d'exploitation\",-(Gq.ops||0)],","[\"Budget d'exploitation\",-(Gq.ops||0)],[\"Bonus d'équipe versé à l'ouverture\",-(S.qBonT||0)],")
open('index.html','w',encoding='utf-8').write(s);print('ok')
