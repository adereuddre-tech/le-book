import sys
P=sys.argv[1];s=open(P,encoding='utf-8').read()
def rep(old,new,k=1):
    global s;n=s.count(old);assert n==k,(n,old[:100]);s=s.replace(old,new)
# rachats adoucis, seuil de clôture à 40 M$
rep("const FUNDMIN=0.05,DDEND=0.50;","const FUNDMIN=0.04,DDEND=0.50;   /* lot 83 : 40 M$ */")
rep("/* lot 82 : le fonds ferme sous 50 M$ d'encours","/* lot 82-83 : le fonds ferme sous 40 M$ d'encours")
rep("if(S.lp<=20)redeem('investisseurs',0.05+0.006*(20-S.lp));","if(S.lp<=20)redeem('investisseurs',RDM.lp0+RDM.lpk*(20-S.lp));")
rep("S.ddHit=ddp;redeem('repli',0.10+0.35*(ddp-ddMax()))","S.ddHit=ddp;redeem('repli',RDM.dd0+RDM.ddk*(ddp-ddMax()))")
rep("if(S.lp<40)tot-=0.04*(40-S.lp)/40*SIZE().flowMult;","if(S.lp<40)tot-=RDM.low*(40-S.lp)/40*SIZE().flowMult;")
rep("const RISKLP={x0:0.20,k:4,fl:0.20,fk:0.30};","const RISKLP={x0:0.20,k:4,fl:0.20,fk:RDMFK};")
rep("const RISKCAP={y:0.30,r:0.45};","""/* lot 83 : rachats adoucis pour le seuil de clôture (avant : 5 %+0,6 %/pt sous 20 de confiance, repli 10 %+35 %,
   confiance basse 4 %, risque 0,30 %/pt) */
const RDM={lp0:0.03,lpk:0.003,dd0:0.06,ddk:0.25,low:0.02},RDMFK=0.15;
const RISKCAP={y:0.30,r:0.45};""")
# risque : partout en annualisé
rep("const sv=`${dec(sq*100,1)} %`,","const sv=`${dec(sp*100,1)} %`,   /* lot 83 : risque annualisé, comme partout ailleurs */\n  ")
rep('text-anchor="middle" fill="var(--dimmer)" font-family="var(--mono)">${Math.round(v*100)}</text>','text-anchor="middle" fill="var(--dimmer)" font-family="var(--mono)">${Math.round(v*200)}</text>')
# ruban : performance du trimestre à date, en plus du cumul ; trait au début du trimestre
rep("  grid+=`<line x1=\"0\" y1=","  grid+=`<line x1=\"0\" y1=")
rep(" const f=n=>n.toFixed(1);\n let body='';"," const f=n=>n.toFixed(1);\n if(opt.qs>0&&opt.qs<n-1){const xq=x(opt.qs);grid+=`<line x1=\"${xq.toFixed(1)}\" y1=\"${pad}\" x2=\"${xq.toFixed(1)}\" y2=\"${H-pad}\" stroke=\"#8A9BB8\" stroke-width=\".6\" stroke-dasharray=\"2 2\" opacity=\".7\"/>`+(opt.ql?`<text x=\"${(xq+2).toFixed(1)}\" y=\"${pad+6}\" font-size=\"6.5\" fill=\"#8A9BB8\" font-family=\"var(--mono)\">T${opt.ql}</text>`:'')}   /* lot 83 */\n let body='';")
rep(""" const v=p[p.length-1],up=v>=100;
 return `<div class="tape"><div class="tapehead"><span>P&amp;L DU FONDS · DEPUIS LE LANCEMENT</span>
   <b class="${up?'pos-g':'neg-g'}">${up?'+':'−'}${dec(Math.abs(v-100),1)} %</b></div>
  ${tapeSvg(p,S.tape.from||0,{anim:1,draw:3,rivals:rivalTapes()})}</div>`;""",
""" const v=p[p.length-1],up=v>=100,q0=Math.min(p.length-1,S.tape.q0||0),qv=v/p[q0]-1,ql=S.phase==='debrief'?S.q:Math.min(S.q+1,QT());
 /* lot 83 : la performance du trimestre à date, lue sur le même tracé que le cumul */
 return `<div class="tape"><div class="tapehead"><span>T${ql} À DATE <b class="${qv>=0?'pos-g':'neg-g'}">${qv>=0?'+':'−'}${dec(Math.abs(qv)*100,1)} %</b> · DEPUIS LE LANCEMENT</span>
   <b class="${up?'pos-g':'neg-g'}">${up?'+':'−'}${dec(Math.abs(v-100),1)} %</b></div>
  ${tapeSvg(p,S.tape.from||0,{anim:1,draw:3,rivals:rivalTapes(),qs:q0,ql})}</div>`;""")
rep("""    <span>LE TRIMESTRE · DEPUIS LE LANCEMENT</span><b class="cnt">—</b></div>
    ${tapeSvg(S.tape.pts,S.tape.q0||0,{h:150,anim:1,draw:3,zero:1,rivals:rivalTapes()})}</div>`""",
"""    <span>T${S.q} <b class="${cls(o.qTotal)}">${sgn(o.qTotal,1)}</b> · DEPUIS LE LANCEMENT</span><b class="cnt">—</b></div>
    ${tapeSvg(S.tape.pts,S.tape.q0||0,{h:150,anim:1,draw:3,zero:1,rivals:rivalTapes(),qs:S.tape.q0||0,ql:S.q})}</div>`""")
open(P,'w',encoding='utf-8').write(s);print('ok')
