p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)

# Mireille : efface le jaune en cours ET protège la clôture du trimestre ; disponible même sans carton
rep("""{id:'mi',bo:4,ic:'⚖️',nm:'Mireille',t:"Plaider devant le comité",d:"Une fois par mandat, elle fait effacer un carton jaune."}""",
    """{id:'mi',bo:4,ic:'⚖️',nm:'Mireille',t:"Plaider devant le comité",d:"Une fois par mandat : elle fait effacer le carton jaune en cours, et le comité ne donnera pas de jaune à la clôture de ce trimestre."}""")
rep("""if(o.id==='mi')return !S.pwMi&&S.cards&&S.cards.y>0;""","""if(o.id==='mi')return !S.pwMi;""")
rep("""  if(o.id==='mi'){S.pwMi=1;S.cards.y=Math.max(0,S.cards.y-1);(S.cards.log=S.cards.log||[]).push({q:S.q,c:'effacé',why:'Mireille plaide devant le comité'})}});""",
    """  if(o.id==='mi'){S.pwMi=1;S.miShield=S.q;S.cards=S.cards||{y:0,r:0,clean:0,log:[]};const y0=S.cards.y;S.cards.y=0;S.cards.clean=0;
   if(y0)S.cards.log.push({q:S.q,c:'effacé',why:'Mireille plaide devant le comité'});
   toast(`⚖️ <b>Mireille</b> plaide : ${y0?'carton jaune effacé, et ':''}pas de jaune à la clôture de ce trimestre.`)}});""")
rep("""  if(!red&&why.length){C.y++;""","""  if(!red&&why.length&&S.miShield===S.q-1){S.miSaved=why[0];C.log.push({q:S.q,c:'effacé',why:'Mireille : '+why[0]});why.length=0}
  if(!red&&why.length){C.y++;""")
rep("""o.id==='mi'?(S.pwMi?'joué pour le mandat':S.cards&&S.cards.y?'disponible':'aucun carton à effacer')""","""o.id==='mi'?(S.pwMi?'joué pour le mandat':'disponible')""")
rep(""" if(S.qCard)warn.push(S.qCard.c==='rouge'""",""" if(S.miSaved&&S.miShield===S.q-1)warn.push(`⚖️ <b>Mireille a plaidé</b> — le comité voulait un jaune (${S.miSaved}). Il n'en donne pas.`);
 if(S.qCard)warn.push(S.qCard.c==='rouge'""")
open(p,'w',encoding='utf-8').write(s)
