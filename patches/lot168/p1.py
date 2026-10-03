# Lot 168 : VIX — le portage du vendeur dépend de l'appétit pour le risque estimé : plein en marché serein, nul quand votre
# lecture annonce une chute nette de l'appétit (courbe du VIX aplatie ou inversée). Calcul identique pour l'attendu affiché
# et pour le rendement réalisé (lecture estimée pour l'attendu, appétit réel du trimestre pour le réalisé).
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("function expRet(i){","function vixCarry(x,a){if(x.sym!=='VX'||!x.drift)return x.drift||0;return x.drift*Math.max(0,Math.min(1,1+a/1.5))}   /* lot 168 : a = appétit (σ) ; −1,5 σ ⇒ portage nul */\nfunction expRet(i){")
rep(" return {m:x.sigQ*z+(x.drift||0)+(PREM[x.grp]||0),s:x.sigQ*Math.sqrt(v)};"," return {m:x.sigQ*z+vixCarry(x,f[3]||0)+(PREM[x.grp]||0),s:x.sigQ*Math.sqrt(v)};")
rep("t:x.sigQ*SIGW.t*(e.t[i]||0)*ed,c:x.sigQ*SIGW.c*(e.c[i]||0)*ed,v:x.sigQ*SIGW.v*cv*(e.v[i]||0)*ed,cv,drift:x.drift||0};","t:x.sigQ*SIGW.t*(e.t[i]||0)*ed,c:x.sigQ*SIGW.c*(e.c[i]||0)*ed,v:x.sigQ*SIGW.v*cv*(e.v[i]||0)*ed,cv,drift:vixCarry(x,f[3]||0)};")
open('index.html','w',encoding='utf-8').write(s);print('lot168 ok')
