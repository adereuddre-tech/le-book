# Lot 110, p2 : sonde sur 12 parties — P&L des concurrents de −52 % à +26 % sur un seul événement : leur vol implicite
# (rivV) passait par l'amplification de foule du joueur (×4 à 35 % de vol). Les concurrents sont diversifiés au-delà de
# leurs paris factoriels : book implicite ramené à 60 % de leur vol, plafonnée à 20 %, sans amplification de foule.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("const a=v>1e-9?rivV(rv)/v:0;return w.map(z=>z*a)}","const a=v>1e-9?XRIVV*Math.min(0.20,rivV(rv))/v:0;return w.map(z=>z*a)}\nconst XRIVV=0.60;")
rep("\n  if(v<0)v*=crowd(rivV(rv));return ((S.xRiv||[])[j]||0)+XRIVR*v});","\n  return ((S.xRiv||[])[j]||0)+XRIVR*v});")
open('index.html','w',encoding='utf-8').write(s);print('lot110 p2 ok')
