# Lot 214 : écrans d'événements — le descriptif d'abord, le sélecteur de positions en dessous, puis « Valider ».
# Sélecteurs de dépêche et de rivalité : les contres à gauche, « rien » au centre, les renforcements à droite.
# Descriptif (bkD) : rentabilité et risque sur la même ligne. Accident : descriptif d'abord aussi (ordre des crans inchangé).
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
# dépêche
rep("""     return `<div class="evsel">${plan.map((o,i)=>{const ban=o.trades.length&&(redOn('risk')||redOn('noadd'))&&o.v1>o.v0+1e-9;o.ban=ban;
       return `<button""","""     return `<div class="evpan" id="evpan"></div>
     <div class="evsel">${plan.map((o,i)=>[o,i]).reverse().map(([o,i])=>{const ban=o.trades.length&&(redOn('risk')||redOn('noadd'))&&o.v1>o.v0+1e-9;o.ban=ban;
       return `<button""")
rep("""</small></button>`}).join('')}</div>
     <div class="evpan" id="evpan"></div>
     <button class="cta" id="evok" style="margin-top:10px">Valider</button>`})()}""","""</small></button>`}).join('')}</div>
     <button class="cta" id="evok" style="margin-top:10px">Valider</button>`})()}""")
# rivalité
rep("""  <div class="evsel">${[['follow','+','suivre'],['fhalf','+½','suivre'],['none','0','rien'],['dhalf','−½','contrer'],['fade','−','contrer']].map(""","""  <div class="evpan" id="rvpan"></div>
  <div class="evsel">${[['fade','−','contrer'],['dhalf','−½','contrer'],['none','0','rien'],['fhalf','+½','suivre'],['follow','+','suivre']].map(""")
rep("""</small></button>`}).join('')}</div>
  <div class="evpan" id="rvpan"></div><button class="cta" id="rvok" style="margin-top:10px">Valider</button></div>`;""","""</small></button>`}).join('')}</div>
  <button class="cta" id="rvok" style="margin-top:10px">Valider</button></div>`;""")
# accident
rep("""  <div class="evsel" style="grid-template-columns:repeat(6,1fr)">${O.map(""","""  <div class="evpan" id="tlpan"></div>
  <div class="evsel" style="grid-template-columns:repeat(6,1fr)">${O.map(""")
rep("""</small></button>`).join('')}</div>
  <div class="evpan" id="tlpan"></div><button class="cta" id="tlok" style="margin-top:10px">Valider</button></div>`;""","""</small></button>`).join('')}</div>
  <button class="cta" id="tlok" style="margin-top:10px">Valider</button></div>`;""")
# descriptif : rentabilité et risque sur une seule ligne
rep("""${ch.length?`<span>rentabilité ${pc2(dp)}</span><span>risque <b class=\"${dr>0.05?'neg-g':dr<-0.05?'pos-g':'dim-g'}\">${dr>=0?'+':'−'}${dec(Math.abs(dr),1)} pt</b></span>`:''}""",
    """${ch.length?`<span>rentabilité ${pc2(dp)} · risque <b class=\"${dr>0.05?'neg-g':dr<-0.05?'pos-g':'dim-g'}\">${dr>=0?'+':'−'}${dec(Math.abs(dr),1)} pt</b></span>`:''}""")
open('index.html','w',encoding='utf-8').write(s);print('lot214 ok')
