# -*- coding: utf-8 -*-
"""Lot 70 — aperçu des choix sur lignes distinctes (rentabilité, risque), plus de stratégie des concurrents au
débriefing, recrues débauchées gardées jusqu'à la fin sauf si un concurrent les reprend."""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
# 1. bkD : une ligne marchés/coûts, une ligne rentabilité, une ligne risque
e.rep(""" return `<span class="bkd">${ch.length?`${ch.slice(0,4).join(', ')}${ch.length>4?'…':''} · rentabilité ${pc2(dp)} · risque <b class="${dr>0.05?'neg-g':dr<-0.05?'pos-g':'dim-g'}">${dr>=0?'+':'−'}${dec(Math.abs(dr),1)} pt</b>`:''}${cost>0?` · coûts <b>${mm(cost)}</b>`:cost<0?` · coûts <b class="pos-g">−${mm(-cost)}</b>`:''}${hid?`${ch.length?' · ':''}<i>positions supplémentaires tirées au moment de l'exécution</i>`:''}</span>`;""",
""" const cs=cost>0?`coûts <b>${mm(cost)}</b>`:cost<0?`coûts <b class="pos-g">−${mm(-cost)}</b>`:'';
 const l1=[ch.length?`${ch.slice(0,4).join(', ')}${ch.length>4?'…':''}`:'',cs].filter(Boolean).join(' · ');
 return `<span class="bkd">${l1?`<span>${l1}</span>`:''}${ch.length?`<span>rentabilité ${pc2(dp)}</span><span>risque <b class="${dr>0.05?'neg-g':dr<-0.05?'pos-g':'dim-g'}">${dr>=0?'+':'−'}${dec(Math.abs(dr),1)} pt</b></span>`:''}${hid?`<span><i>positions supplémentaires tirées au moment de l'exécution</i></span>`:''}</span>`;""")
e.rep(".bkd b{font-weight:600}",".bkd b{font-weight:600}.bkd>span{display:block}")
# 2. débriefing : plus de stratégie des concurrents, l'accident reste signalé
e.rep("""${a.st?`<br><span class="dim-g" style="font-size:11px">${a.st}${a.th?' · <span class="neg-g">accident</span>':''}</span>`:''}""",
 """${a.th?`<br><span class="neg-g" style="font-size:11px">accident de levier</span>`:''}""")
# 3. recrues : S.stars (classes d'actifs), gardées jusqu'à la fin ; un débauchage subi reprend la dernière
e.rep(" if(S.star>=0&&INSTR[S.star]&&INSTR[i].grp===INSTR[S.star].grp)m*=0.5;   /* lot 68 : toute la classe */",
 " if((S.stars||[]).includes(INSTR[i].grp))m*=0.5;   /* lot 70 : recrues gardées jusqu'à la fin, ÷2 sur leur classe (sans cumul) */")
e.rep("  S.star=i;rv.skill=Math.max(0.5,rv.skill-0.02);","  S.stars=S.stars||[];if(!S.stars.includes(INSTR[i].grp))S.stars.push(INSTR[i].grp);rv.skill=Math.max(0.5,rv.skill-0.02);")
e.rep("g:`coûts ÷2 sur toute la classe ${INSTR[i].grp.toLowerCase()} ce trimestre · ${rv.nm} affaibli`}","g:`coûts ÷2 sur toute la classe ${INSTR[i].grp.toLowerCase()} tant qu'il reste chez vous · ${rv.nm} affaibli`}")
e.rep(""" S.star=-1;
 if(STARP[S.bud.exec]>0&&rng()<STARP[S.bud.exec])S.star=Math.floor(rng()*N);
 if(S.star>=0){""",""" S.star=-1;S.stars=S.stars||[];
 if(STARP[S.bud.exec]>0&&rng()<STARP[S.bud.exec])S.star=Math.floor(rng()*N);
 if(S.star>=0&&!S.stars.includes(INSTR[S.star].grp))S.stars.push(INSTR[S.star].grp);
 if(S.star>=0){""")
e.rep("g:`coûts d'exécution ÷2 sur toute la classe ${INSTR[S.star].grp.toLowerCase()} ce trimestre`}","g:`coûts d'exécution ÷2 sur toute la classe ${INSTR[S.star].grp.toLowerCase()}, tant qu'il reste chez vous`}")
e.rep("S.execPenalty*=1.14;S.poachMsg+=` ${(pick(S.rivals.filter(x=>x.poacher))||S.rivals[S.rivals.length-1]).boss} a débauché deux de vos gérants : coûts d'exécution +14 % durablement.`}",
 "S.execPenalty*=1.14;S.poachMsg+=` ${(pick(S.rivals.filter(x=>x.poacher))||S.rivals[S.rivals.length-1]).boss} a débauché deux de vos gérants : coûts d'exécution +14 % durablement.`;\n  if((S.stars||[]).length){const g=S.stars.pop();S.poachMsg+=` Votre recrue ${g.toLowerCase()} part avec eux : la remise sur cette classe disparaît.`}}")
e.done("lot 70")
