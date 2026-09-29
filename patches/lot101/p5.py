# Lot 101e : sans accidents de levier, le bot passait de 20 à 33 % de vol ex ante et le score triplait (+24 ± 8,5 M$).
# Le frein convexe revient par la liquidité : quand tout le monde réduit en même temps, un gros book se vend mal.
# Une perte de scénario est multipliée par crowd(sp) = 1 + 1,5·max(0, sp − 0,20)/0,10 (×1 à 20 %, ×2,5 à 30 %,
# ×4 à 40 % de vol annuelle). Les gains ne sont pas amplifiés. tailExp (coût attendu) suit, pour le bot et l'affichage.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("function stressLoss(k,sc){const w=weights(k),h=stressHit(sc);let v=0;INSTR.forEach((x,i)=>{if(h[x.sym])v+=w[i]*h[x.sym]*x.sigQ});return v}",
    "function crowd(sp){return 1+1.5*Math.max(0,sp-0.20)/0.10}\nfunction stressLoss(k,sc){const w=weights(k),h=stressHit(sc);let v=0;INSTR.forEach((x,i)=>{if(h[x.sym])v+=w[i]*h[x.sym]*x.sigQ});return v<0?v*crowd(riskShown(w).total):v}")
rep(" if(ev.stress){imm*=0.5+0.5*(TAILM[S.bud.risk]||1);"," if(ev.stress){imm*=0.5+0.5*(TAILM[S.bud.risk]||1);if(imm<0)imm*=crowd(riskShown(w).total);")
rep("function tailExp(sp,std){return tailP(sp,std)*TAILSEV*tailL(sp)*0.55}","function tailExp(sp,std){if(!std)return stressP()*0.2*sp*crowd(sp)*(0.5+0.5*(TAILM[S.bud.risk]||1));return tailP(sp,std)*TAILSEV*tailL(sp)*0.55}")
rep("<p class=\"note\" style=\"margin-top:4px\">La moitié du choc tombe tout de suite ;","<p class=\"note\" style=\"margin-top:4px\">Au-delà de 20 % de risque annuel, les pertes sont amplifiées : un gros book se vend mal quand tout le monde réduit (×${dec(crowd(RS.total),1)} pour le vôtre). La moitié du choc tombe tout de suite ;")
open('index.html','w',encoding='utf-8').write(s);print('ok')
