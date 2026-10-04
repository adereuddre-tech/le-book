# Lot 208 (lot B) : rivalité — réponse graduée à 5 crans : suivre le concurrent (position cible pleine, comme avant),
# suivre à moitié (à mi-chemin), ne pas répondre, contrer à moitié, contrer pleinement. Mêmes coûts (×1,5), même bruit ;
# l'écho de presse est divisé par deux pour les demi-crans. Sélecteur .rvstep, panneau #rvpan, bouton #rvok.
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1,seg=None):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
i0=s.index('function screenRivalEvent');i1=s.index("armTimer(()=>pickR('none'));",i0)+len("armTimer(()=>pickR('none'));")
F=s[i0:i1]
def fr(o,n,k=1):
    global F; c=F.count(o); assert c==k,(c,o[:100]); F=F.replace(o,n)
fr(" const src=pick(PRESS_SRC);",""" const hF=Math.round((S.k[i]+nk)/2),hD=Math.round((S.k[i]-nk)/2);   /* lot 208 : demi-crans, à mi-chemin */
 const RT={follow:nk,fhalf:hF,none:S.k[i],dhalf:hD,fade:-nk};
 const src=pick(PRESS_SRC);""")
# boutons → panneaux
b0=F.index('  <button class="choice" data-a="follow">');b1=F.index('</button></div>`;',b0)+len('</button></div>`;')
old=F[b0:b1]
fol=old[old.index('<span>Coût ${mm(tcost(nk-S.k[i],i).cost'):old.index('</span></button>\n  <button class="choice" data-a="fade">')]
F=F[:b0]+"""  <div class="evsel">${[['follow','+','suivre'],['fhalf','+½','suivre'],['none','0','rien'],['dhalf','−½','contrer'],['fade','−','contrer']].map(([a,l,c])=>{const off=a!=='none'&&RT[a]===S.k[i];
    return `<button class="evstep rvstep ${a==='follow'||a==='fhalf'?'up':a==='none'?'zr':'dn'}${a==='none'?' on':''}" data-a="${a}"${off?' disabled':''}><b>${l}</b><small>${c}</small></button>`}).join('')}</div>
  <div class="evpan" id="rvpan"></div><button class="cta" id="rvok" style="margin-top:10px">Valider</button></div>`;
 const RP={follow:`<b>Suivre ${rv.boss} : passer ${x.sym} à ${nk>0?'+':''}${nk}</b>"""+fol+"""</span>`,
  fhalf:`<b>Suivre à moitié : ${x.sym} à ${hF>0?'+':''}${hF}</b><span>Coût ${mm(tcost(hF-S.k[i],i).cost*1.5*S.tcMultQ)}, à votre charge. La moitié du pari, la moitié de l'écho dans la presse.${bkD(S.k.map((v,m)=>m===i?hF:v),0,false)}</span>`,
  none:`<b>Ne pas répondre à la presse</b><span>Vous ne changez rien. Investisseurs −1,5 de plus : ils voulaient une réaction.</span>`,
  dhalf:`<b>Contrer à moitié : ${x.sym} à ${hD>0?'+':''}${hD}</b><span>Vous pariez, sans tout miser, que ${rv.boss} a tort de rester. Coût ${mm(tcost(hD-S.k[i],i).cost*1.5*S.tcMultQ)}. La moitié de l'écho dans la presse.${bkD(S.k.map((v,m)=>m===i?hD:v),0,false)}</span>`,
  fade:`<b>Prendre le contre-pied : ${x.sym} à ${(-nk)>0?'+':''}${-nk}</b><span>Vous pariez que ${rv.boss} a tort de rester. Coût ${mm(tcost(-nk-S.k[i],i).cost*1.5*S.tcMultQ)}, même bruit, gloire ou ridicule.${bkD(S.k.map((v,m)=>m===i?-nk:v),0,false)}</span>`};"""+F[b1:]
# pickR généralisé
fr("const target=a==='follow'?nk:-nk;","const dA=(a==='follow'||a==='fhalf')?'follow':'fade',hs=(a==='fhalf'||a==='dhalf')?0.5:1,target=RT[a];   /* lot 208 */")
p0=F.index('const pickR=a=>{');P=F[p0:]
P=P.replace("a==='follow'","dA==='follow'").replace("a==='fade'","dA==='fade'").replace("const dA=(dA==='follow'","const dA=(a==='follow'")
for o,n in [("gauge(2,0,","gauge(2*hs,0,"),("gauge(3,1,","gauge(3*hs,1*hs,"),("gauge(-2,-1,","gauge(-2*hs,-1*hs,"),("gauge(-1,0,\"La presse parle d'un gérant qui court","gauge(-1*hs,0,\"La presse parle d'un gérant qui court")]:
    assert P.count(o)==1,(o,P.count(o));P=P.replace(o,n)
P=P.replace(" app.querySelectorAll('.choice').forEach(b=>b.onclick=()=>pickR(b.dataset.a));",
""" let sel='none';const pan=a=>{document.getElementById('rvpan').innerHTML=`<div class="choice" style="cursor:default">${RP[a]}</div>`;
  app.querySelectorAll('.rvstep').forEach(b=>b.classList.toggle('on',b.dataset.a===a));sel=a};pan('none');
 app.querySelectorAll('.rvstep').forEach(b=>b.onclick=()=>{if(!b.disabled)pan(b.dataset.a)});
 document.getElementById('rvok').onclick=()=>pickR(sel);""")
F=F[:p0]+P
s=s[:i0]+F+s[i1:]
open('index.html','w',encoding='utf-8').write(s);print('lot208 ok')
