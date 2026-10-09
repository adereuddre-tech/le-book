p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
rep("""</div></div><p>${o.p}</p></button>
     <details class="carddet"><summary>Détails</summary>""","""</div></div>${o.sum?cardSum(o.sum):`<p>${o.p}</p>`}</button>
     <details class="carddet"><summary>Détails</summary>${o.sum?`<p class="note" style="margin:6px 0">${o.p}</p>`:''}""")
rep("""function renderPicks(){""","""/* lot 266 : fiche courte — un pouvoir, trois forces, deux faiblesses ; le reste replié */
function cardSum(m){return `<div class="csum"><div class="cpw">✦ ${m.pw}</div>${m.f.map(x=>`<div class="g">+ ${x}</div>`).join('')}${m.w.map(x=>`<div class="b">− ${x}</div>`).join('')}</div>`}
function renderPicks(){""")
rep(""".qline{""",""".csum{font-size:12.5px;line-height:1.45;margin-top:6px;text-align:left}.csum .cpw{color:var(--gold);margin-bottom:2px}.csum .g{color:var(--long)}.csum .b{color:var(--short)}
.qline{""")
SUM={'syst':"sum:{pw:\"le modèle : son book entier en facile, ses six convictions en moyen et difficile\",f:[\"coûts d'exécution −28 %\",\"investisseurs 25 % moins nerveux\",\"incidents −40 %\"],w:[\"vol cible 18 % : il laisse du rendement\",\"ajuster en cours de trimestre exige une dérogation\"]},",
 'fonda':"sum:{pw:\"deux sources vérifiées par trimestre, et une dépêche dont la suite est connue\",f:[\"+5 sources par trimestre\",\"la valeur lue trois fois plus nettement, trois catalyseurs secrets\",\"les extrêmes presque toujours identifiés\"],w:[\"coûts +15 %, incidents plus fréquents et plus chers\",\"60 % seulement d'un mouvement capté\"]},",
 'flux':"sum:{pw:\"l'intuition : le sens d'un facteur macro, juste quatre fois sur cinq\",f:[\"dépêches lues 40 % plus juste, 85 % du mouvement capté\",\"un ajustement gratuit par trimestre\",\"il sent venir les extrêmes mieux que personne\"],w:[\"investisseurs 20 % plus nerveux, équipe 35 % plus chère\",\"incidents ×1,7, presque trois fois plus chers\"]},"}
for k,v in SUM.items():
    rep("{id:'%s',lvl:"%k,"{id:'%s',%slvl:"%(k,v))
open(p,'w',encoding='utf-8').write(s)
