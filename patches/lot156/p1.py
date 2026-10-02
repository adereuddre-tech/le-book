# Lot 156 : concurrents à book réel (2/4) — les dépêches. À chaque dépêche résolue, chaque concurrent encaisse le choc sur
# son propre book, avec la même issue que le joueur (poursuite ou retournement) : moitié immédiate + suite × réaction de
# style (flux suit toujours ×1,5 ; fondamental une fois sur deux ×1,5 ; quant ne réagit pas ×1). Chocs datés dans
# S.xRivL : les rubans les montrent à l'instant où ils arrivent ; S.xRiv reste leur somme pour la clôture.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("function xRivHit(id){",r'''function addXRiv(a){const t=typeof qElapsed==='function'&&S.live?qElapsed():0;(S.xRivL=S.xRivL||[]).push({t,a});S.xRivQ=S.q;S.xRivT=S.xRivT==null?t:S.xRivT;S.xRiv=S.rivals.map((r,j)=>((S.xRiv||[])[j]||0)+(a[j]||0))}
function rivXAt(j,t,tq){if(S.xRivQ!==tq)return 0;if(!S.xRivL)return (S.xRiv&&t>=(S.xRivT||0))?(S.xRiv[j]||0):0;return S.xRivL.reduce((x,e)=>x+(t>=e.t?(e.a[j]||0):0),0)}
const RIVEV={flux:1.5,fonda:1.5,syst:1};
function rivEvHit(ev,touched,mult){if(!S.rivals)return;const a=S.rivals.map((rv,j)=>{const w=(rv._bk&&rv._bkq===S.q)?rv._bk:rivBookQ(rv,j,S.q);
  const st=rv.style||'fonda',ph=st==='fonda'?(prng32(hash32('rev'+j+'_'+S.q+'_'+(ev.t||''),S.seed))()<0.5?RIVEV.fonda:1):(RIVEV[st]||1);
  let v=0;touched.forEach(i=>{const h=(ev.hit[INSTR[i].sym]||0)*INSTR[i].sigQ;v+=w[i]*h*(0.5+ph*mult)});return v});addXRiv(a)}
function xRivHit(id){''')
rep("let v=0;INSTR.forEach((m,i)=>{if(h[m.sym])v+=w[i]*h[m.sym]*m.sigQ});\n  return ((S.xRiv||[])[j]||0)+XRIVR*v});","let v=0;INSTR.forEach((m,i)=>{if(h[m.sym])v+=w[i]*h[m.sym]*m.sigQ});\n  return XRIVR*v});const xa=S.xRiv;S.xRiv=S.rivals.map((r,j)=>((S.xRivB||[])[j]||0));addXRiv(xa);")
rep("function xRivHit(id){const sc=STRESS.find(x=>x.id===id);if(!sc)return;","function xRivHit(id){const sc=STRESS.find(x=>x.id===id);if(!sc)return;S.xRivB=S.xRiv;")
rep("else{S.xRiv=S.rivals.map((r,j)=>((S.xRiv||[])[j]||0)+(j===rj?imm:0));","else{addXRiv(S.rivals.map((r,j)=>j===rj?imm:0));")
rep("const xr=(S.xRiv&&S.xRivQ===tq&&t>=(S.xRivT||0))?(S.xRiv[j]||0):0,","const xr=rivXAt(j,t,tq),")
rep("S.rumors=[];S.xRiv=null;S.xRivT=null;S.xRivQ=null;","S.rumors=[];S.xRiv=null;S.xRivT=null;S.xRivQ=null;S.xRivL=null;S.xRivB=null;")
rep(" const navR=S.nav;S.nav*=(1+resid);S.qEvM+=resid*navR;\n"," const navR=S.nav;S.nav*=(1+resid);S.qEvM+=resid*navR;\n if(!ev.stress)try{rivEvHit(ev,touched,mult)}catch(e){}   /* lot 156 */\n")
open('index.html','w',encoding='utf-8').write(s);print('lot156 ok')
s=open('index.html',encoding='utf-8').read()
rep("S.xRivB=S.xRiv;if(S.xRivT==null||S.xRivQ!==S.q){S.xRivT=typeof qElapsed==='function'?qElapsed():0;S.xRivQ=S.q}\n","S.xRivB=S.xRivQ===S.q?S.xRiv:null;\n")
rep("toast('Les concurrents encaissent aussi, selon leur portefeuille : '+S.rivals.map((rv,j)=>`${rv.nm} ${sgnp(S.xRiv[j],1)}`).join(' · '))}","toast('Les concurrents encaissent aussi, selon leur portefeuille : '+S.rivals.map((rv,j)=>`${rv.nm} ${sgnp(xa[j],1)}`).join(' · '))}")
open('index.html','w',encoding='utf-8').write(s);print('lot156 p1b ok')
