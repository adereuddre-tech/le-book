p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
rep("""  sigBonus:0,capture:0.55,tcMult:0.80,rumBonus:0.05,lpMult:0.85,modelScale:0.80,incMult:1.0,incSev:1.0,numeric:false,pairs:true}
];""","""  sigBonus:0,capture:0.55,tcMult:0.80,rumBonus:0.05,lpMult:0.85,modelScale:0.80,incMult:1.0,incSev:1.0,numeric:false,pairs:true},
 {id:'tail',sum:{pw:"la protection au juste prix, et qui rend 120 % du choc : vous gagnez quand tout s'effondre",f:["veille des extrêmes forte","aucun signal mal lu : bruit ×1 partout","incidents −10 %"],w:["investisseurs 25 % plus nerveux","chaque trimestre calme où vous êtes couvert : confiance −2"]},lvl:'Normal',who:"« Je ne sais pas quand, je sais que »",nm:"Chasseur de queues",
  p:"Vous ne prévoyez pas la crise : vous savez qu'elle viendra, et vous êtes le seul à être payé ce jour-là. Le reste du temps, vous payez l'assurance, trimestre après trimestre, sous le regard de plus en plus las de vos investisseurs. Un jour de krach, vous faites en une séance ce que les autres font en dix ans.",
  ef:[['g',"<b>Pouvoir propre — la convexité</b> : votre protection contre les extrêmes coûte son juste prix (1 × ce qu'elle rend en moyenne, au lieu de 2 ×) et rend 120 % du choc immédiat au lieu de 70 % : un extrême vous enrichit"],['g',"veille des extrêmes forte : 25 à 95 % sentis, 40 à 90 % identifiés"],['g',"aucune spécialité de lecture, mais aucune faiblesse : tendance, portage et valeur au bruit ×1"],['g',"incidents −10 % : un desk prudent"],['b',"investisseurs 25 % plus nerveux : ils ne comprennent pas pourquoi vous payez l'assurance"],['b',"chaque trimestre calme où vous êtes couvert : « encore un trimestre à payer l'assurance », confiance −2"],['b',"votre desk vise 18 % de vol"],['b',"commission de performance +3 pts, le prix de la convexité ; capture 60 %"]],
  sigBonus:0,capture:0.60,tcMult:1.0,rumBonus:0.10,lpMult:1.25,modelScale:0.90,incMult:0.9,incSev:1.0,numeric:false,tailH:true}
];""")
rep("const STYPERF={syst:0,fonda:0.03,flux:0.05,rv:0.02};","const STYPERF={syst:0,fonda:0.03,flux:0.05,rv:0.02,tail:0.03};")
rep("const STYSEED={syst:0.0005,fonda:0,flux:0.0005,rv:0.0005};","const STYSEED={syst:0.0005,fonda:0,flux:0.0005,rv:0.0005,tail:0};")
rep("const STYCOST={syst:0.85,fonda:1,flux:1.35,rv:1.10};","const STYCOST={syst:0.85,fonda:1,flux:1.35,rv:1.10,tail:1.0};")
rep("rv:{s:0.20,i:0.30}};","rv:{s:0.20,i:0.30},tail:{s:0.32,i:0.45}};")
rep(""" rv:{F:0.55,T:0.30,C:1.10,V:0.90,X:0.30,macro:0.8,mkt:1.0,""",""" tail:{F:0.80,T:0.70,C:0.30,V:0.60,X:0.20,macro:1.0,mkt:1.0,
  txt:"Votre desk pèse les sources et les signaux sans parti pris ; il préfère la tendance, qui ne coûte rien quand le marché casse, au portage, qui coûte cher ce jour-là."},
 rv:{F:0.55,T:0.30,C:1.10,V:0.90,X:0.30,macro:0.8,mkt:1.0,""")
# bruit ×1 partout pour le chasseur de queues
rep("ne=kk=>e*(S.prof==='syst'?0.6:(kk===mine?0.3:1.3));","ne=kk=>e*(S.prof==='syst'?0.6:S.prof==='tail'?1:(kk===mine?0.3:1.3));")
rep("return e*(S.prof==='syst'?0.6:(typeof STYLESIG","return e*(S.prof==='syst'?0.6:S.prof==='tail'?1:(typeof STYLESIG")
# protection par style
rep("""function hedgeCost(){return Math.max(HEDGE.min,HEDGE.load*hedgeEV())}""","""function hH(){return S&&S.prof==='tail'?1.2:HEDGE.h}function hL(){return S&&S.prof==='tail'?1:HEDGE.load}   /* lot 271 */
function hedgeCost(){return Math.max(HEDGE.min,hL()*hedgeEV())}""")
rep("""return HEDGE.h*e}   /* lot 264 */""","""return hH()*e}   /* lot 264 */""")
rep("""${dec(HEDGE.load,0)} × ce montant""","""${dec(hL(),0)} × ce montant""")
rep("""Rendu par la protection (${Math.round(HEDGE.h*100)} % du choc immédiat)</span><span class="av"><b class="pos-g">${e.v<0?'+'+mm(-e.v*HEDGE""","""Rendu par la protection (${Math.round(hH()*100)} % du choc immédiat)</span><span class="av"><b class="pos-g">${e.v<0?'+'+mm(-e.v*hH""")
s=s.replace("+mm(-e.v*hH.h*S.nav)","+mm(-e.v*hH()*S.nav)")
rep("""<p class="note">La protection rend ${Math.round(HEDGE.h*100)} % du choc immédiat""","""<p class="note">La protection rend ${Math.round(hH()*100)} % du choc immédiat""")
rep("""Le marché vend cette protection au double de ce qu'elle rend en moyenne : se couvrir chaque trimestre coûte cher ; elle ne paie que si votre veille vous en dit plus que le marché.""",
    """${S.prof==='tail'?"Vous l'achetez à son juste prix : elle ne coûte que ce qu'elle rend en moyenne, et rend plus que le choc.":"Le marché vend cette protection au double de ce qu'elle rend en moyenne : se couvrir chaque trimestre coûte cher ; elle ne paie que si votre veille vous en dit plus que le marché."}""")
rep("""let hgB=0;if(ev.x&&S.hedgeQ===S.q&&imm<0){hgB=-imm*HEDGE.h;imm+=hgB}""","""let hgB=0;if(ev.x&&S.hedgeQ===S.q&&imm<0){hgB=-imm*hH();imm+=hgB}""")
rep(""" if(S.budBp>70)lpD.push(['Facture d\\'exploitation jugée lourde',-1.5]);""",""" if(S.budBp>70)lpD.push(['Facture d\\'exploitation jugée lourde',-1.5]);
 if(S.prof==='tail'&&S.hedgeQ===S.q&&!S.stressQ)lpD.push(["Encore un trimestre à payer l'assurance",-2]);   /* lot 271 */""")
rep("""function styDraw(){const el=document.getElementById('stypw');if(!el)return;const P=PROF();let h='';""","""function styDraw(){const el=document.getElementById('stypw');if(!el)return;const P=PROF();let h='';
 if(P.tailH)h=`<div class="blockhead"><h2>La convexité</h2><span class="hint">votre pouvoir</span></div><p class="note" style="margin:0">Après les ordres, la protection contre les extrêmes vous est vendue à son juste prix (aujourd'hui ${dec(hedgeCost()*100,2)} % de l'encours pour ce book) et rend 120 % du choc immédiat. ${xWatchTxt()}</p>`;""")
open(p,'w',encoding='utf-8').write(s)
s=open(p,encoding='utf-8').read()
rep("veille des extrêmes forte : 25 à 95 % sentis, 40 à 90 % identifiés","veille des extrêmes forte : 25 à 90 % sentis, 40 à 80 % identifiés")
rep("veille des extrêmes modeste : 20 à 80 % sentis, 30 à 70 % identifiés","veille des extrêmes modeste : 12 à 78 % sentis, 25 à 65 % identifiés")
rep('rv:"20–80 % · 30–70 %",tail:"30–95 % · 45–90 %"','rv:"12–78 % · 25–65 %",tail:"25–90 % · 40–80 %"')
open(p,'w',encoding='utf-8').write(s)
