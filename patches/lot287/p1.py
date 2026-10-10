p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
rep("""function recoBook(){
 const {W,f}=styleEst();
 const sc=INSTR.map((x,i)=>{let v=0;for(let k=0;k<K;k++)v+=x.b[k]*f[k]*W.F;
  if(S.tcvEst)v+=0.24*W.T*S.tcvEst.t[i]+0.20*W.C*S.tcvEst.c[i]+0.18*W.V*S.tcvEst.v[i];
  v+=W.X*0.30*S.crowd[i];
  return {i,v}});""","""function recoBook(){
 const {W,f:f0}=styleEst(),f=[...f0];
 /* lot 287 : le book du desk intègre ce que sait le style — l'intuition du flux, les catalyseurs du fondamental, les paires */
 if(S.hunch)f[S.hunch.k]+=(S.hunch.up?1:-1)*1.03;
 const sc=INSTR.map((x,i)=>{let v=0;for(let k=0;k<K;k++)v+=x.b[k]*f[k]*Math.max(W.F,0.5);
  if(S.tcvEst)v+=0.24*W.T*S.tcvEst.t[i]+0.20*W.C*S.tcvEst.c[i]+0.18*W.V*S.tcvEst.v[i]*((S.prof==='fonda'&&S.cat&&S.cat.includes(i))?CATM:1);
  v+=W.X*0.30*S.crowd[i]+2*pairAlpha(i);
  return {i,v}});""")
open(p,'w',encoding='utf-8').write(s)
