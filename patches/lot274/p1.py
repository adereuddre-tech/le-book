p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
# 1. accidents de levier aussi par la marge : sous 30 % rien, puis jusqu'à 40 % de chances au seuil d'appel
rep("""const TAIL={x0:0.20,w:0.30,p:0.60},""","""/* lot 274 : la marge fait aussi les accidents — au-delà de 20 % de l'encours, le prime broker regarde ;
   la probabilité monte jusqu'à 40 % au seuil d'appel (50 %) */
const MGZ={watch:0.20,pmax:0.40,pow:1.3};
function levAccP(mgu){return mgu<=MGZ.watch?0:Math.min(0.6,MGZ.pmax*Math.pow((mgu-MGZ.watch)/(MGC.thr-MGZ.watch),MGZ.pow))}
function accP(k){const sp=riskShown(weights(k)).total,a=tailP(sp),b=levAccP(marginPct(k));return {p:1-(1-a)*(1-b),r:a,m:b,sp,mgu:marginPct(k)}}
function mgCol(m){return m>=MGC.thr?'var(--short)':m>=MGC.warn?'#E08A3C':m>=MGZ.watch?'var(--warn)':'var(--long)'}
const TAIL={x0:0.20,w:0.30,p:0.60},""")
rep(""" const sp=riskShown(weights(S.k)).total,u=prng32(hash32('tail'+S.q,S.seed));
 if(u()>=tailP(sp))return null;
 const wantMg=u()<TAILMG,pool=TAILEV.map((e,j)=>j).filter(j=>!!TAILEV[j].mg===wantMg),i=pool[Math.floor(u()*pool.length)],ev=TAILEV[i],
  L=Math.min(ev.mg?0.60:0.55,(ev.sev[0]+(ev.sev[1]-ev.sev[0])*u())*tailL(sp)),good=u()<0.5;""",""" const A=accP(S.k),sp=A.sp,u=prng32(hash32('tail'+S.q,S.seed));
 if(u()>=A.p)return null;
 const byMg=u()<A.m/Math.max(1e-9,A.r+A.m);   /* lot 274 : l'accident vient de la marge ou du risque, au prorata */
 const wantMg=byMg,pool=TAILEV.map((e,j)=>j).filter(j=>!!TAILEV[j].mg===wantMg),i=pool[Math.floor(u()*pool.length)],ev=TAILEV[i],
  spE=byMg?Math.max(sp,0.20+0.5*(A.mgu-MGZ.watch)):sp,
  L=Math.min(ev.mg?0.60:0.55,(ev.sev[0]+(ev.sev[1]-ev.sev[0])*u())*tailL(spE)),good=u()<0.5;""")
rep(""" return {i,sp,L,good,imp:imp/S.nav};""",""" return {i,sp,L,good,imp:imp/S.nav,byMg,mgu:A.mgu};""")
rep("""   <p class="note">${ev.mg?'Appel de marge':'Accident de levier'} : votre book tourne à ${pct(RQ(te.sp))} de risque. En dessous de ${dec(TAIL.x0*50,0)} %, il ne serait pas arrivé.</p></div>""",
    """   <p class="note">${te.byMg?`Appel de marge : votre marge utilisée atteint ${Math.round(te.mgu*100)} % de l'encours. En dessous de ${Math.round(MGZ.watch*100)} %, il ne serait pas arrivé.`:`Accident de levier : votre book tourne à ${pct(RQ(te.sp))} de risque. En dessous de ${dec(TAIL.x0*50,0)} %, il ne serait pas arrivé.`}</p></div>""")
# 2. la marge dans la barre d'état : une jauge, pas une mention
rep("""${S.k&&S.k.some(v=>v)?`<span class="mgt">marge ${Math.round(marginPct(S.k)*100)} %</span>`:''}</span><b id="gaintile" class="${cashView()>=0?'':'neg-g'}">${treso(cashView())}</b></button>""",
    """</span><b id="gaintile" class="${cashView()>=0?'':'neg-g'}">${treso(cashView())}</b>${(()=>{const m=S.k&&S.k.some(v=>v)?marginPct(S.k):0;return `<span class="mgbar${m>=MGC.warn?' hot':''}" title="Marge utilisée"><i style="width:${Math.min(100,m/0.6*100).toFixed(0)}%;background:${mgCol(m)}"></i><em style="left:${(MGZ.watch/0.6*100).toFixed(0)}%"></em><em style="left:${(MGC.thr/0.6*100).toFixed(0)}%" class="thr"></em></span><span class="mgl" style="color:${mgCol(m)}">marge ${Math.round(m*100)} %</span>`})()}</button>""")
rep(""".epi{""",""".mgbar{display:block;position:relative;height:5px;border-radius:3px;background:var(--line2);margin-top:4px;overflow:visible}.mgbar i{display:block;height:100%;border-radius:3px}.mgbar em{position:absolute;top:-2px;width:1px;height:9px;background:var(--dim)}.mgbar em.thr{background:var(--short)}.mgbar.hot{animation:mgp 1.1s ease-in-out infinite}@keyframes mgp{50%{opacity:.45}}.mgl{display:block;font-size:10px;font-family:var(--mono);margin-top:2px}
.epi{""")
# 3. page du book : une ligne de levier toujours visible, au-dessus du bouton
rep("""  <div class="kv" id="purse"></div>""","""  <div class="mgline" id="mgline"></div>
  <div class="kv" id="purse"></div>""")
rep("""function renderRisk(){
 const w=weights(S.k),sp=pvol(w),vd=varDecomp(w),rc=riskContrib(w);""","""function mgLineDraw(){const el=document.getElementById('mgline');if(!el)return;const A=accP(S.k),m=A.mgu;
 const msg=m>=MGC.thr?"au-dessus du seuil : l'appel de marge tombera à la première dépêche":m>=MGC.warn?"le prime broker appelle deux fois par jour":m>=MGZ.watch?"le prime broker vous surveille":"tranquille";
 el.innerHTML=`<div class="kv"><span><b>Levier</b> · marge utilisée <b style="color:${mgCol(m)}">${Math.round(m*100)} %</b> de l'encours <span class="dim-g">(surveillance ${Math.round(MGZ.watch*100)} % · appel ${Math.round(MGC.thr*100)} %)</span></span><b style="color:${A.p>0.15?'var(--short)':A.p>0.03?'var(--warn)':'var(--dim)'}">accident ${Math.round(A.p*100)} %</b></div>
  <span class="mgbar${m>=MGC.warn?' hot':''}" style="height:7px"><i style="width:${Math.min(100,m/0.6*100).toFixed(0)}%;background:${mgCol(m)}"></i><em style="left:${(MGZ.watch/0.6*100).toFixed(0)}%"></em><em style="left:${(MGC.thr/0.6*100).toFixed(0)}%" class="thr"></em></span>
  <p class="note" style="margin:4px 0 0">${msg[0].toUpperCase()+msg.slice(1)}. Probabilité d'un accident de levier ce trimestre : ${Math.round(A.p*100)} %, nulle sous ${Math.round(MGZ.watch*100)} % de marge, ${Math.round(MGZ.pmax*100)} % au seuil d'appel. Pour la faire baisser : moins de notionnel, surtout sur les marchés à forte marge (actions, matières premières, crypto).</p>`}
function renderRisk(){
 mgLineDraw();   /* lot 274 */
 const w=weights(S.k),sp=pvol(w),vd=varDecomp(w),rc=riskContrib(w);""")
rep(""".epi{""",""".mgline{margin:10px 0 8px;padding:8px 10px;border:1px solid var(--line2);border-radius:6px;background:var(--panel2)}
.epi{""")
open(p,'w',encoding='utf-8').write(s)
