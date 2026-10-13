p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# pouvoirs de garde (Solange, Josiane, Mireille ; Gontran déjà) : armés, ils ne comptent que s'ils servent
rep("""function pwCommit(){if(!S.pw)return;S.pwLast=S.pwLast||{};S.pwMaK=null;
 PW.forEach(o=>{if(o.info||!pwOn(o.id)||S.pwLast[o.id]===S.q)return;S.pwLast[o.id]=S.q;""",
"""const PWG=['so','jo','mi'];   /* lot 334 : les gardiens ne comptent que s'ils servent */
function pwGuard(id){if(!pwOn(id))return false;(S.pwLast=S.pwLast||{})[id]=S.q;return true}
function pwCommit(){if(!S.pw)return;S.pwLast=S.pwLast||{};S.pwMaK=null;
 PW.forEach(o=>{if(o.info||!pwOn(o.id)||S.pwLast[o.id]===S.q)return;if(!PWG.includes(o.id))S.pwLast[o.id]=S.q;""")
rep("""  if(o.id==='on'){gauge(8,0,'Onésime sur un plateau télé');if(!pwOn('jo'))S.leakQ=true}
  if(o.id==='jo')S.leakQ=false;""","""  if(o.id==='on'){gauge(8,0,'Onésime sur un plateau télé');if(!pwGuard('jo'))S.leakQ=true}
  if(o.id==='jo'&&S.leakQ){S.leakQ=false;S.pwLast.jo=S.q}""")
rep("""  if(e.leakQ&&!pwOn('jo'))S.leakQ=true;""","""  if(e.leakQ&&!pwGuard('jo'))S.leakQ=true;""",2)
rep("""if(e.leakQ&&!pwOn('jo'))S.leakQ=true;msg.push""","""if(e.leakQ&&!pwGuard('jo'))S.leakQ=true;msg.push""")
rep(""" if(ev.stress&&pwOn('so')&&imm<0)imm*=ev.stress==='cyber'?0:0.65;""",""" if(ev.stress&&imm<0&&pwGuard('so'))imm*=ev.stress==='cyber'?0:0.65;""")
rep("""  if(o.id==='mi'){S.pwMi=1;S.miShield=S.q;""","""  if(o.id==='mi'){S.miShield=S.q;""")
rep("""   if(y0)S.cards.log.push({q:S.q,c:'effacé',why:'Mireille plaide devant le comité'});""","""   if(y0){S.pwMi=1;S.cards.log.push({q:S.q,c:'effacé',why:'Mireille plaide devant le comité'})}""")
rep("""if(!red&&why.length&&S.miShield===S.q-1){S.miSaved=why[0];""","""if(!red&&why.length&&S.miShield===S.q-1){S.miSaved=why[0];S.pwMi=1;""")
# textes
rep("""d:"Une fois par mandat : elle fait effacer le carton jaune en cours, et le comité ne donnera pas de jaune à la clôture de ce trimestre."}""",
    """d:"Une fois par mandat : elle fait effacer le carton jaune en cours, et le comité ne donnera pas de jaune à la clôture de ce trimestre. Ne compte pour le mandat que si elle a effacé ou évité un carton."}""")
rep("""d:"Aucune fuite de vos positions ce trimestre, quoi qu'il arrive — même si Onésime passe à la télé."}""",
    """d:"Aucune fuite de vos positions ce trimestre, quoi qu'il arrive — même si Onésime passe à la télé. Ne compte pour l'année que si elle a empêché une fuite."}""")
rep("""et une cyberattaque ne vous touche pas. S'ajoute à la protection, qui rend sur le choc du marché."}""",
    """et une cyberattaque ne vous touche pas. S'ajoute à la protection, qui rend sur le choc du marché. Ne compte pour l'année que si un extrême ou une cyberattaque tombe."}""")
rep("""Se joue sur l'écran de l'incident."}""","""Se joue sur l'écran de l'incident ; ne compte pour l'année que si vous l'utilisez."}""")
rep("""<span class="hint">un coup de pouce chacun par an · Jean-Kevin chaque trimestre</span>""","""<span class="hint">un coup de pouce chacun par an · Jean-Kevin chaque trimestre · les gardiens ne comptent que s'ils servent</span>""")
rep("""const st=on?(o.info?'joué ce trimestre':'armé · touchez pour désarmer')""","""const st=on?(o.info?'joué ce trimestre':S.pwLast&&S.pwLast[o.id]===S.q&&PWG.includes(o.id)?'a servi · compté':PWG.includes(o.id)?(S.phase==='book'?'armé · touchez pour désarmer · ne compte que s’il sert':'en garde · ne compte que s’il sert'):'armé · touchez pour désarmer')""")
open(p,'w',encoding='utf-8').write(s)
