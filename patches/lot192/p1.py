# Lot 192 : résultat du trimestre — la performance du trimestre défilait jusqu'à −0,0 % : son point de départ était lu au
# début du trimestre suivant. Point de départ fourni explicitement (valeur de fin ÷ (1 + résultat)).
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("data-q0=\"${(p[Math.min(n-1,opt.qs||0)]||100).toFixed(3)}\"","data-q0=\"${(opt.q0v||p[Math.min(n-1,opt.qs||0)]||100).toFixed(3)}\"")
rep("${tapeSvg(S.tape.pts,S.tape.q0||0,{h:150,anim:1,draw:3,zero:1,rivals:rivalTapes(),qs:S.tape.q0||0,ql:S.q})}","${tapeSvg(S.tape.pts,S.tape.q0||0,{h:150,anim:1,draw:3,zero:1,rivals:rivalTapes(),qs:S.tape.q0||0,ql:S.q,q0v:S.tape.pts[S.tape.pts.length-1]/(1+o.qTotal)})}")
open('index.html','w',encoding='utf-8').write(s);print('lot192 ok')
