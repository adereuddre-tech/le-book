# Lot 154 : concurrents à book réel (voie intermédiaire, 1/4). Chaque trimestre, un concurrent tient un book (ses paris
# factoriels projetés sur les marchés ouverts, à sa vol) et gagne Σ poids × vrais rendements des marchés du trimestre
# (S.rBase, ceux du joueur) ; il paie ses ordres à la rotation du book (même barème que le joueur, salle de marché pleine
# ×0,75) ; il monte en charge : 60 % de sa vol au premier trimestre, 80 % au deuxième. Son bruit propre est réduit (la part
# idiosyncratique vient désormais des marchés). Accidents de levier, événements extrêmes et tuyaux inchangés.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("function rivRet(j,t,q){",r'''const RIVB={ramp:[0.6,0.8,1],exec:0.75,noise:0.35,k:{syst:0.65,fonda:1,flux:1}};   /* k : calé sur les rendements de l'ancien modèle (moyenne, écart type) */
function rivRamp(q){return RIVB.ramp[Math.min(RIVB.ramp.length-1,Math.max(0,q))]}
/* book du concurrent j au trimestre q (pleine vol × montée en charge) ; même graine que rivalE */
function rivBookQ(rv,j,q){const x=rivFx(rv,j),w=INSTR.map(m=>m.b.reduce((a,b,k)=>a+b*x[k],0)/m.sig),v=pvol(w);const a=v>1e-9?rivV(rv)*rivRamp(q)/v:0;return w.map(z=>z*a)}
/* coût de rotation du book, en fraction d'encours : barème du joueur, salle de marché pleine */
function rivTurn(w,w0){let c=0;INSTR.forEach((x,i)=>{const d=Math.abs(w[i]-((w0&&w0[i])||0));if(d>1e-9){const bn=d*S.nav;c+=d*(x.s+x.c*Math.sqrt(bn))*TCK*RIVB.exec*1e-4}});return c}
function rivBookRet(j,q){const rv=S.rivals[j];if(!S.rBase)return 0;
 if(!rv._bk||rv._bkq!==q){rv._bk=rivBookQ(rv,j,q);rv._bkq=q;rv._bkc=rivTurn(rv._bk,rv.wPrev)}
 let g=0;rv._bk.forEach((w,i)=>g+=w*(S.rBase[i]||0));return {g,c:rv._bkc}}
function rivRet(j,t,q){
 if(S.rivals&&S.rivals[j]&&S.rBase&&q===S.q){const r=S.rivals[j],v=rivV(r),tl=rivTail(r,j,v,q),tt=0.2+0.7*prng32(hash32('rtt'+j+'_'+q,S.seed))(),B=rivBookRet(j,q);
  return t*((RIVB.k[r.style]||1)*B.g+(v/2)*RIVB.noise*(RIVNOISE[r.style]||0.78)*rivNz(j,q)-0.008-rivDrag(v)+(r.bRet||0))-B.c-(t>=tt?tl:0)}
 return rivRetOld(j,t,q)}
function rivRetOld(j,t,q){''')
rep("S.rivals.forEach((rv,j)=>{rv.last=rr[j];rv.cum*=(1+rr[j]);","S.rivals.forEach((rv,j)=>{if(rv._bk&&rv._bkq===S.q){rv.wPrev=rv._bk}rv.last=rr[j];rv.cum*=(1+rr[j]);")
open('index.html','w',encoding='utf-8').write(s);print('lot154 ok')
