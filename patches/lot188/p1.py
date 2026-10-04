# Lot 188 : ordres passés dans l'urgence — suivre une dépêche coûte ×2 le tarif normal (fourchette et impact ; ×1,6 avant),
# ×5 pendant un événement extrême (×2,5 avant). Les concurrents qui suivent une dépêche paient leurs ordres au même barème.
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("const c=tc.cost*1.6*S.tcMultQ*(S.leakQ?1.45:1)*(ev.stress?2.5:1);","const c=tc.cost*(ev.stress?5:2)*S.tcMultQ*(S.leakQ?1.45:1);")
rep("  let v=0;touched.forEach(i=>{const h=(ev.hit[INSTR[i].sym]||0)*INSTR[i].sigQ;v+=w[i]*h*(0.5+ph*mult)});return v});addXRiv(a)}",
    "  let v=0;touched.forEach(i=>{const h=(ev.hit[INSTR[i].sym]||0)*INSTR[i].sigQ;v+=w[i]*h*(0.5+ph*mult)});\n  if(ph>1){const w1=[...w];touched.forEach(i=>{w1[i]=w[i]*ph});v-=rivTurn(w1,w)*(ev.stress?5:2)}return v});addXRiv(a)}")
open('index.html','w',encoding='utf-8').write(s);print('lot188 ok')
