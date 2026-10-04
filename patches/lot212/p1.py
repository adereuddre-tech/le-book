# Lot 212 (lot E) : concurrents face aux dépêches — règle de netteté. Avant : quant jamais, flux toujours, fondamental
# une fois sur deux, et « réagir » grossissait de 50 % toutes les positions touchées, dans un sens comme dans l'autre.
# Désormais : z = espérance de la suite du mouvement / son écart-type (scénarios de la dépêche) ; chaque concurrent
# perçoit ẑ = z + η·bruit (η selon la difficulté : facile 1,0, moyen 0,6, difficile 0,3 ; tirage déterministe) ;
# il renforce (ẑ > θ : à moitié ; ẑ > 2θ : en plein) ou contre (symétrique) selon son style (θ quant 1,2, fondamental
# 0,7, flux 0,3 : calibrés pour réagir à ~21 %, ~46 %, ~75 % des dépêches ; valeurs de départ 0,8 / 0,4 / 0) ; ampleur k (quant ×1,25, fondamental ×1,5, flux ×1,75) appliquée dans le sens du choc sur chaque marché
# touché : w + r·(k−1)·max(|w|, u)·signe(choc), u = taille moyenne d'une ligne. Rotation payée comme avant.
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
i=s.index('function rivEvHit(ev,touched,mult){');j=s.index('\nfunction xRivHit',i)
s=s[:i]+r'''const RIVTH={syst:1.2,fonda:0.7,flux:0.3},RIVAMP={syst:1.25,fonda:1.5,flux:1.75};   /* lot 212 */
function rivEta(){const z=SIZE()||{};return z.id==='small'?1.0:z.id==='mega'?0.3:0.6}
function rivEvHit(ev,touched,mult,SC){if(!S.rivals)return;
 let z0=0;if(SC&&SC.m&&SC.m.length===2){const p=SC.p,e=p*SC.m[0]+(1-p)*SC.m[1],sd=Math.abs(SC.m[0]-SC.m[1])*Math.sqrt(p*(1-p));z0=sd>1e-9?e/sd:0}
 const a=S.rivals.map((rv,j)=>{const w=(rv._bk&&rv._bkq===S.q)?rv._bk:rivBookQ(rv,j,S.q);
  const st=rv.style||'fonda',th=RIVTH[st]!=null?RIVTH[st]:0.4,k=RIVAMP[st]||1.5;
  const g=prng32(hash32('rev'+j+'_'+S.q+'_'+(ev.t||''),S.seed)),u1=g(),u2=g();
  const zh=z0+rivEta()*Math.sqrt(-2*Math.log(u1+1e-12))*Math.cos(2*Math.PI*u2);
  const r=zh>2*th?1:zh>th?0.5:zh<-2*th?-1:zh<-th?-0.5:0;
  const nzw=w.filter(x=>x!==0),u=nzw.length?nzw.reduce((a,x)=>a+Math.abs(x),0)/nzw.length:0;
  const w1=[...w];if(r)touched.forEach(i=>{const h=ev.hit[INSTR[i].sym]||0;if(h)w1[i]=w[i]+r*(k-1)*Math.max(Math.abs(w[i]),u)*Math.sign(h)});
  let v=0,v0=0;touched.forEach(i=>{const h=(ev.hit[INSTR[i].sym]||0)*INSTR[i].sigQ;v+=w[i]*h*0.5+w1[i]*h*mult;v0+=w[i]*h*(0.5+mult)});
  if(r)v-=rivTurn(w1,w)*(ev.stress?5:2);
  if(window.__rvlog)window.__rvlog.push({st,sz:(SIZE()||{}).id,r,dv:v-v0});
  return v});addXRiv(a)}'''+s[j:]
rep("if(!ev.stress)try{rivEvHit(ev,touched,mult)}catch(e){}","if(!ev.stress)try{rivEvHit(ev,touched,mult,SC)}catch(e){}")
open('index.html','w',encoding='utf-8').write(s);print('lot212 ok')
