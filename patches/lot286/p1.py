p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
rep("const RECO={prof:'flux',","const RECO={prof:'syst',")
# risque de croisière : deux tiers de la limite du comité, l'unique repère avec la limite elle-même
rep("""function limVol(raw){""","""function cruise(){return limVol()*2/3}   /* lot 286 : risque de croisière, remplace la vol cible pour le joueur */
function limVol(raw){""")
rep(""" const tgM=S.tgt*(PROF().modelScale||1);""",""" const tgM=cruise()*(PROF().modelScale||1);   /* lot 286 */""")
rep("""pour une référence de ${pct(RQ(S.tgt),0)}.""","""pour un risque de croisière de ${pct(RQ(cruise()),1)} (deux tiers de la limite du comité).""")
rep("""if(id==='risk'&&sp>0.7*S.tgt+1e-9)return `Carton rouge : risque ${pct(RQ(sp))}, plafond ${pct(RQ(0.7*S.tgt))}`;""","""if(id==='risk'&&sp>0.7*cruise()+1e-9)return `Carton rouge : risque ${pct(RQ(sp))}, plafond ${pct(RQ(0.7*cruise()))}`;""")
rep("""if(id==='noadd'&&sp>S.tgt+1e-9)return `Carton rouge : risque ${pct(RQ(sp))}, plafond ${pct(RQ(S.tgt))}`;""","""if(id==='noadd'&&sp>cruise()+1e-9)return `Carton rouge : risque ${pct(RQ(sp))}, plafond ${pct(RQ(cruise()))}`;""")
rep(""" const band=bandNow(),rk=S.tgt>0?sp/S.tgt:0;
 /* couleur continue : vert dans la bande, puis jaune, orange, rouge à mesure que l'écart
    au mandat grandit. Un dégradé se lit mieux que trois paliers. */
 const rdev=Math.max(0,(Math.abs(rk-1)-band)/0.95);""",""" /* lot 286 : couleur lue sur la limite du comité — vert sous les deux tiers, ocre jusqu'à la limite, brique au-delà */
 const rdev=Math.max(0,(sp/Math.max(1e-9,limVol())-2/3)/0.6);""")
rep("""const a=S.tgt/sp;S.k=S.k.map((v,i)=>clampK(i,Math.round(v*a)));""","""const a=cruise()/sp;S.k=S.k.map((v,i)=>clampK(i,Math.round(v*a)));""")
rep("""Elle recale votre book sur le risque cible, ligne par ligne""","""Elle recale votre book sur le risque de croisière (deux tiers de la limite du comité), ligne par ligne""")
s=s.replace("xa=Math.min((S.tgt||0.2)/2,xr*0.85)","xa=Math.min(cruise()/2,xr*0.85)")
rep("""["Book visé",p=>f(p.modelScale)+' la vol cible']""","""["Book du modèle",p=>f(p.modelScale)+' le risque de croisière']""")
rep("""<summary>Les trois styles en un tableau</summary>""","""<summary>Les six styles en un tableau</summary>""")
rep("""w:["vol cible 18 % : il laisse du rendement",""","""w:["le modèle vise 90 % du risque de croisière : il laisse du rendement",""")
rep(""""vol cible 16 % : de petits gains, beaucoup de levier"]""",""""il vise 80 % du risque de croisière : de petits gains, beaucoup de levier"]""")
open(p,'w',encoding='utf-8').write(s)
s=open(p,encoding='utf-8').read()
for a,b in [("le modèle vise 18 % de vol : régulier, mais il laisse du rendement","le modèle vise 90 % du risque de croisière : régulier, mais il laisse du rendement"),
 ("votre desk vise 18 % de vol\"","votre desk vise 90 % du risque de croisière\""),
 ("votre desk vise 22 % de vol : des convictions","votre desk vise 110 % du risque de croisière : des convictions"),
 ("votre desk vise 16 % de vol : de petits écarts","votre desk vise 80 % du risque de croisière : de petits écarts"),
 ("votre desk vise 24 % de vol : plus de rendement","votre desk vise 120 % du risque de croisière : plus de rendement"),
 ("votre desk vise 23 % de vol : des convictions massives","votre desk vise 115 % du risque de croisière : des convictions massives")]:
    rep(a,b)
open(p,'w',encoding='utf-8').write(s)
