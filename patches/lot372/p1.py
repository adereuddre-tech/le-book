p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# Gontran et Octave deviennent des gardiens comme Solange, Josiane et Mireille : armés pendant le book, ne comptent que s'ils servent
rep("""{id:'go',bo:1,ic:'🧮',nm:'Gontran',inc:1,t:"Passer l'écriture",d:"Si un incident tombe, il le rattrape : le fonds n'en paie qu'un quart, sans perte de confiance. Se joue sur l'écran de l'incident ; ne compte pour l'année que si vous l'utilisez."}""",
    """{id:'go',bo:1,ic:'🧮',nm:'Gontran',t:"Passer l'écriture",d:"Armé, il veille tout le trimestre : si un incident tombe, il le rattrape, le fonds n'en paie qu'un quart et la confiance ne bouge pas. Ne compte pour l'année que s'il sert."}""")
rep("""{id:'oc',bo:10,ic:'💱',nm:'Octave',inc:1,t:"Un coup de fil au prime broker",d:"Si un appel de marge tombe, il obtient un délai jusqu'à la clôture : rien n'est coupé, aucune perte de confiance. Se joue sur l'écran de l'appel (et tout seul à la clôture) ; ne compte pour l'année que s'il sert."}""",
    """{id:'oc',bo:10,ic:'💱',nm:'Octave',t:"Un coup de fil au prime broker",d:"Armé, il veille tout le trimestre : si un appel de marge tombe, il obtient un délai jusqu'à la clôture, rien n'est coupé et la confiance ne bouge pas. Ne compte pour l'année que s'il sert."}""")
rep("""{id:'jo',bo:2,ic:'🗂️',nm:'Josiane',t:"Tout rapprocher",d:"Aucune fuite de vos positions ce trimestre, quoi qu'il arrive — même si Onésime passe à la télé. Ne compte pour l'année que si elle a empêché une fuite."}""",
    """{id:'jo',bo:2,ic:'🗂️',nm:'Josiane',t:"Tout rapprocher",d:"Armée, elle veille tout le trimestre : aucune fuite de vos positions, même si Onésime passe à la télé. Ne compte pour l'année que si elle sert."}""")
rep("""d:"Ce trimestre, le choc immédiat d'un événement extrême est réduit de 35 %, et une cyberattaque ne vous touche pas. S'ajoute à la protection, qui rend sur le choc du marché. Ne compte pour l'année que si un extrême ou une cyberattaque tombe."}""",
    """d:"Armée, elle veille tout le trimestre : le choc immédiat d'un extrême est réduit de 35 %, et une cyberattaque ne vous touche pas. S'ajoute à la protection. Ne compte pour l'année que si elle sert."}""")
rep("""d:"Une fois par mandat : elle fait effacer le carton jaune en cours, et le comité ne donnera pas de jaune à la clôture de ce trimestre. Ne compte pour le mandat que si elle a effacé ou évité un carton."}""",
    """d:"Une fois par mandat. Armée, elle fait effacer le carton jaune en cours et le comité ne donnera pas de jaune à la clôture du trimestre. Ne compte que si elle sert."}""")
rep("""const PWG=['so','jo','mi'];   /* lot 334 : les gardiens ne comptent que s'ils servent */""","""const PWG=['so','jo','mi','go','oc'];   /* lot 334 : les gardiens ne comptent que s'ils servent ; lot 372 : Gontran et Octave aussi */""")
rep("""function pwUse(id){const o=PW.find(x=>x.id===id);if(o&&o.inc&&pwAvail(o)&&!pwOn(o.id)){toast(`${o.ic} <b>${o.nm}</b> est prêt${o.id==='oc'?" : il se jouera sur l'écran de l'appel de marge, si l'appel tombe.":" : il se jouera sur l'écran de l'incident, si un incident tombe."} Rien à armer.`);return}
 if(!o||!pwOk(o))return;""","""function pwUse(id){const o=PW.find(x=>x.id===id);if(!o||!pwOk(o))return;""")
rep("""data-pw="${o.id}"${ok||(o.inc&&pwAvail(o))?'':' disabled'}>""","""data-pw="${o.id}"${ok?'':' disabled'}>""")
rep("""{const g=PW.find(x=>x.id==='go');if(g&&pwAvail(g))O.push({b:"Gontran passe l'écriture",s:"Il rattrape l'erreur dans les comptes : le fonds n'en paie qu'un quart, et personne n'en entend parler. Compté pour l'année.",""",
    """if(pwOn('go'))O.unshift({b:"🧮 Gontran passe l'écriture",s:"Armé ce trimestre, il rattrape l'erreur dans les comptes : le fonds n'en paie qu'un quart, et personne n'en entend parler. Compté pour l'année.",""")
rep("""f:0.25*loss,m:0,lp:0,rc:0,go:1})}   /* lot 268 */""","""f:0.25*loss,m:0,lp:0,rc:0,go:1});   /* lot 268 ; lot 372 : seulement s'il est armé */""")
rep("""{const oc=PW.find(x=>x.id==='oc');if(oc&&pwAvail(oc))O.unshift(""","""{if(pwOn('oc'))O.unshift(""")
rep("""s:"Il obtient un délai jusqu'à la clôture : rien n'est coupé, et plus d'appel ce trimestre. Compté pour l'année.",c:0})}""","""s:"Armé ce trimestre, il obtient un délai jusqu'à la clôture : rien n'est coupé, et plus d'appel ce trimestre. Compté pour l'année.",c:0})}""")
rep("""   const oc=PW.find(x=>x.id==='oc');
   if(mgTrough>MGC.thr&&(S.ocGrace===S.q||(oc&&pwAvail(oc)))){""","""   if(mgTrough>MGC.thr&&(S.ocGrace===S.q||pwOn('oc'))){""")
open(p,"w",encoding="utf-8").write(s)
