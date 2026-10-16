p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# Gontran et Octave (pouvoirs d'incident) : la carte n'est plus grisée quand ils sont disponibles ; la toucher explique où ils se jouent
rep("""data-pw="${o.id}"${ok?'':' disabled'}>""","""data-pw="${o.id}"${ok||(o.inc&&pwAvail(o))?'':' disabled'}>""")
rep("""function pwUse(id){const o=PW.find(x=>x.id===id);if(!o||!pwOk(o))return;""",
    """function pwUse(id){const o=PW.find(x=>x.id===id);if(o&&o.inc&&pwAvail(o)&&!pwOn(o.id)){toast(`${o.ic} <b>${o.nm}</b> est prêt${o.id==='oc'?" : il se jouera sur l'écran de l'appel de marge, si l'appel tombe.":" : il se jouera sur l'écran de l'incident, si un incident tombe."} Rien à armer.`);return}
 if(!o||!pwOk(o))return;""")
open(p,"w",encoding="utf-8").write(s)
