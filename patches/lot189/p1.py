# Lot 189 : tableau des concurrents — la ligne des concurrents s'appelait « événement extrême » mais additionnait dépêches,
# tuyaux et chocs extrêmes. Elle dit « dépêches et chocs » ; votre fonds a la même ligne (dépêches et tuyaux du trimestre),
# en plus de ses événements extrêmes et accidents de levier.
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("${Math.abs(a.xr||0)>=0.0005?`<br><span class=\"${cls(a.xr)}\" style=\"font-size:11px\">événement extrême ${sgnp(a.xr,1)}</span>`:''}",
    "${Math.abs(a.xr||0)>=0.0005?`<br><span class=\"${cls(a.xr)}\" style=\"font-size:11px\">dépêches et chocs ${sgnp(a.xr,1)}</span>`:''}")
rep("const myT=(S.tails||[]).filter(x=>x.q===S.q-1);","const myT=(S.tails||[]).filter(x=>x.q===S.q-1),myEv=(o.P&&o.P.evM||0)/Math.max(1e-9,S.navQ0);")
rep("const all=[{nm:S.fundName,v:o.qTotal,me:1,rk:o.sp,cv:S.idx-1,mt:myT},","const all=[{nm:S.fundName,v:o.qTotal,me:1,rk:o.sp,cv:S.idx-1,mt:myT,xr:myEv},")
open('index.html','w',encoding='utf-8').write(s);print('lot189 ok')
