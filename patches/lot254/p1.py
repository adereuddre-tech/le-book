p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
# lecture du modèle : quant en moyen et difficile
rep("${S.size==='small'?`<div class=\"wire\" style=\"margin:10px 0 8px\"><div class=\"kv\" style=\"padding-bottom:6px\"><span><b>Le book que ${PROF().numeric?'le modèle':'le desk'} construirait</b></span>",
    "${S.size==='small'||PROF().numeric?`<div class=\"wire\" style=\"margin:10px 0 8px\"><div class=\"kv\" style=\"padding-bottom:6px\"><span><b>${S.size==='small'?`Le book que ${PROF().numeric?'le modèle':'le desk'} construirait`:'La lecture du modèle'}</b></span>")
rep("""  if(am)am.onclick=()=>{S.k=[...S.modelK];drawRows();renderRisk();refreshStatus();refreshGain();refreshSend();toast('Book du desk appliqué — à vous de l\\'ajuster.')};
 }
""","""  if(am)am.onclick=()=>{S.k=[...S.modelK];drawRows();renderRisk();refreshStatus();refreshGain();refreshSend();toast('Book du desk appliqué — à vous de l\\'ajuster.')};
 }
 else if(fe&&PROF().numeric){   /* lot 254 : en moyen et difficile, le quant garde la lecture du modèle — sens et rang, sans tailles ni bouton */
  const {sc}=recoBook(),top=sc.filter(o=>mktOpen(o.i)&&Math.abs(o.v)>1e-6).sort((a,b)=>Math.abs(b.v)-Math.abs(a.v)).slice(0,6);
  fe.innerHTML=top.length?`<div class="chips">${top.map((o,r)=>`<i class="${o.v>0?'up':'dn'}">${r+1}. ${INSTR[o.i].sym} ${o.v>0?'▲':'▼'}</i>`).join('')}</div>
   <p class="note" style="margin:6px 0 0">Les six convictions les plus nettes du modèle, de la plus forte à la moins forte : le sens, pas la taille. Le dimensionnement et le risque restent les vôtres.</p>`
   :`<p class="note" style="margin:0">Le modèle ne voit rien de tranché ce trimestre.</p>`}
""")
# fiches des styles
rep("<b>Pouvoir propre — le modèle de risque</b> : il annonce parfois l'événement extrême et chiffre sa perte ; en niveau facile, le book du modèle, optimisé sur toutes les sources et tous les signaux, s'applique d'un bouton (comme pour tous les styles)",
    "<b>Pouvoir propre — le modèle</b> : en moyen et difficile, la lecture du modèle, ses six convictions les plus nettes, sens et rang ; en facile, le book du modèle entier, applicable d'un bouton (comme pour tous les styles)\"],['g',\"veille des extrêmes équilibrée : le modèle de risque sent venir de 20 à 85 % des extrêmes, en identifie de 45 à 85 % et chiffre la perte du book")
rep("chaque trimestre, deux rumeurs sont recoupées et données pour certaines ; une fois sur deux, votre réseau vous nomme l'événement extrême qui arrive",
    "chaque trimestre, deux rumeurs sont recoupées et données pour certaines\"],['g',\"veille des extrêmes : votre réseau en sent venir moins (10 à 75 %), mais vous dit presque toujours lequel (60 à 95 %)")
rep("chaque trimestre, le sens d'un facteur macro avant tout le monde, juste quatre fois sur cinq ; et vous sentez toujours venir un événement extrême, sans savoir lequel",
    "chaque trimestre, le sens d'un facteur macro avant tout le monde, juste quatre fois sur cinq\"],['g',\"veille des extrêmes : vous sentez venir l'orage mieux que personne (33 à 95 %), sans trop savoir lequel (5 à 45 %)")
rep('syst:"modèle de risque : l\'événement extrême annoncé et chiffré ; signaux lus plus nettement",fonda:"sources vérifiées : une probabilité sûre par trimestre",flux:"intuition : le sens d\'un facteur, juste 4 fois sur 5"',
    'syst:"le modèle : book entier en facile, six convictions en moyen et difficile",fonda:"sources vérifiées : une probabilité sûre par trimestre",flux:"intuition : le sens d\'un facteur, juste 4 fois sur 5"')
rep("""const R=[["Pouvoir",p=>pw[p.id]],""","""const XR={syst:"20–85 % · 45–85 %",fonda:"10–75 % · 60–95 %",flux:"33–95 % · 5–45 %"};
 const R=[["Pouvoir",p=>pw[p.id]],["Extrêmes : sentir · identifier",p=>XR[p.id]],""")
open(p,'w',encoding='utf-8').write(s)
