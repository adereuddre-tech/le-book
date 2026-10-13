p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# protection : valeur pour le marché, valeur pour votre desk, jauge, et le tableau des faux positifs / faux négatifs (présentation C)
rep("""function hedgeBlock(){const e=xImmEst(),pX=xProbTot(),ev=hedgeEV(),cr=hedgeCost(),c=cr*S.nav,on=S.hedgeQ===S.q||S.hedgePick===S.q,HP=hedgeParts(),h=hH();""",
"""/* lot 338 : ce que vaut la protection pour votre desk — mêmes dépêches violentes et même put, extrêmes à la probabilité a posteriori */
function hedgeDeskEV(){const HP=hedgeParts(),T=xProbTot(),Pd=xDeskP(),e=xImmEst();const exD=e.sig?Pd*Math.max(0,-e.v):(T>0?HP.ex*Pd/T:0);return hH()*(exD+HP.dp+HP.pt)}
function hedgeGauge(ev,evD,cr){const mx=Math.max(ev,evD,cr,1e-9)*1.1,X=v=>(v/mx*100).toFixed(1);
 const tick=(v,col,w)=>`<em style="position:absolute;left:${X(v)}%;top:0;width:${w}px;height:18px;background:${col};transform:translateX(-50%);border-radius:1px"></em>`;
 return `<div style="position:relative;height:18px;margin:10px 0 4px"><span style="position:absolute;left:0;right:0;top:6px;height:6px;border-radius:3px;background:var(--panel2)"></span>
  <span style="position:absolute;left:0;width:${X(evD)}%;top:6px;height:6px;border-radius:3px;background:var(--gold);opacity:.45"></span>
  ${tick(ev,'var(--dim)',2)}${tick(evD,'var(--gold)',3)}${tick(cr,'var(--short)',3)}</div>
  <p class="note" style="margin:0 0 6px"><b style="color:var(--dim)">▍</b> marché ${mm(ev*S.nav)} · <b style="color:var(--gold)">▍</b> desk ${mm(evD*S.nav)} · <b style="color:var(--short)">▍</b> prime ${mm(cr*S.nav)} — la protection vaut le coup quand le trait doré dépasse le rouge.</p>`}
function hedgeBlock(){const e=xImmEst(),pX=xProbTot(),ev=hedgeEV(),cr=hedgeCost(),c=cr*S.nav,on=S.hedgeQ===S.q||S.hedgePick===S.q,HP=hedgeParts(),h=hH();
 const W=xWatch(),Pd=xDeskP(),evD=hedgeDeskEV(),gap=evD-cr,pc0=v=>`${dec(v*100,1)} %`;""")
rep("""  <p class="note" style="margin:0 0 6px">Un événement extrême frappe ce trimestre avec une probabilité d'environ ${Math.round(pX*100)} %. ${xWatchTxt()}</p>
  <div class="attr"><span class="an">Ce que la protection rend en moyenne, aux probabilités du marché</span><span class="av"><b>${mm(ev*S.nav)} · ${dec(ev*100,2)} %</b></span></div>
  <div class="attr"><span class="an" style="padding-left:10px">dont extrêmes · dépêches violentes · put sur le book</span><span class="av">${mm(h*HP.ex*S.nav)} · ${mm(h*HP.dp*S.nav)} · ${mm(h*HP.pt*S.nav)}</span></div>
  <div class="attr"><span class="an">Prime : ${cr>HEDGE.min+1e-9?(hH()>1?`ce que rendrait une protection à 100 % du choc · le surplus de ${Math.round(hH()*100-100)} % est offert`:`${dec(hL(),0)} × ce montant`):`plancher de ${dec(HEDGE.min*100,1)} %`}</span><span class="av"><b class="neg-g">−${mm(c)} · ${dec(cr*100,2)} %</b></span></div>""",
"""  <div class="attr"><span class="an">Valeur selon le marché · ce qu'elle rend en moyenne, extrême à ${pc0(pX)}</span><span class="av"><b>${mm(ev*S.nav)} · ${dec(ev*100,2)} %</b></span></div>
  <div class="attr"><span class="an" style="padding-left:10px">dont extrêmes · dépêches violentes · put sur le book</span><span class="av">${mm(h*HP.ex*S.nav)} · ${mm(h*HP.dp*S.nav)} · ${mm(h*HP.pt*S.nav)}</span></div>
  <div class="attr"><span class="an">Valeur selon votre desk · extrême à ${pc0(Pd)}, ${S.xHint?'puisque votre veille alerte':'puisque votre veille ne dit rien'}</span><span class="av"><b class="gold-g">${mm(evD*S.nav)} · ${dec(evD*100,2)} %</b></span></div>
  <div class="attr"><span class="an">Prime : ${cr>HEDGE.min+1e-9?(hH()>1?`ce que rendrait une protection à 100 % du choc · le surplus de ${Math.round(hH()*100-100)} % est offert`:`${dec(hL(),0)} × la valeur selon le marché`):`plancher de ${dec(HEDGE.min*100,1)} %`}</span><span class="av"><b class="neg-g">−${mm(c)} · ${dec(cr*100,2)} %</b></span></div>
  <div class="attr"><span class="an"><b>Pour votre desk, la protection est ${gap>=0?'bon marché':'chère'}</b></span><span class="av"><b class="${gap>=0?'pos-g':'neg-g'}">${gap>=0?'+':'−'}${mm(Math.abs(gap)*S.nav)}</b></span></div>
  ${hedgeGauge(ev,evD,cr)}
  <details style="margin:6px 0"><summary>Comment le desk estime : alertes, faux positifs, faux négatifs</summary>
   <table class="qt" style="margin-top:6px"><thead><tr><th style="text-align:left">Ce trimestre</th><th>Alerte</th><th>Pas d'alerte</th></tr></thead><tbody>
    <tr><td style="text-align:left">Extrême (${pc0(pX)})</td><td${S.xHint?' style="color:var(--gold)"':''}>${pc0(pX*W.s)}<br><small>vrai positif</small></td><td${S.xHint?'':' style="color:var(--gold)"'}>${pc0(pX*(1-W.s))}<br><small>faux négatif</small></td></tr>
    <tr><td style="text-align:left">Calme (${pc0(1-pX)})</td><td${S.xHint?' style="color:var(--gold)"':''}>${pc0((1-pX)*W.fa)}<br><small>faux positif</small></td><td${S.xHint?'':' style="color:var(--gold)"'}>${pc0((1-pX)*(1-W.fa))}<br><small>calme confirmé</small></td></tr></tbody></table>
   <p class="note">Le marché ne sait que la probabilité d'un extrême, ${pc0(pX)}. Votre veille en sent venir ${Math.round(W.s*100)} % (les autres arrivent sans prévenir : faux négatifs) et crie au loup ${Math.round(W.fa*100)} % des trimestres calmes (faux positifs). ${S.xHint?`Elle alerte : parmi les trimestres où elle alerte, ${pc0(Pd)} portent vraiment un extrême — colonne de gauche, vrais positifs sur le total.`:`Elle se tait : parmi les trimestres où elle se tait, il reste ${pc0(Pd)} d'extrêmes — les faux négatifs, colonne de droite.`} Quand elle nomme l'événement, elle a raison ${Math.round(W.i*100)} fois sur 100. La valeur pour le desk reprend celle du marché, avec cette probabilité à la place de ${pc0(pX)} ; dépêches violentes et put sur le book ne changent pas.</p></details>""")
open(p,'w',encoding='utf-8').write(s)
