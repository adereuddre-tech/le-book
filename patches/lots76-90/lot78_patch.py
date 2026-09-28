P='/home/claude/le-book/index.html';s=open(P,encoding='utf-8').read()
def rep(old,new,k=1):
    global s;n=s.count(old);assert n==k,(n,old[:90]);s=s.replace(old,new)
# 1. encours à quatre chiffres significatifs
rep("const moneyB=x=>{","/* lot 78 : encours de la tuile à quatre chiffres significatifs */\nconst money4=x=>{const a=Math.abs(x);if(a>=1)return x.toFixed(a>=100?1:a>=10?2:3).replace('.',',')+' Md$';\n const m=x*1000,b=Math.abs(m);return m.toFixed(b>=100?1:b>=10?2:3).replace('.',',')+' M$'};\nconst moneyB=x=>{")
rep('<b id="navtile">${moneyB(navNow())}</b>','<b id="navtile">${money4(navNow())}</b>')
# 2. concurrence : cumul porté par chaque ligne (la recherche par nom ratait quand le nom ne contenait pas « · »)
rep("const all=[{nm:S.fundName,v:o.qTotal,me:1,rk:o.sp},...S.rivals.map(r=>({nm:r.nm+'<span class=\"bossn\">'+r.boss+'</span>',v:r.last,",
    "const all=[{nm:S.fundName,v:o.qTotal,me:1,rk:o.sp,cv:S.idx-1},...S.rivals.map(r=>({nm:r.nm+'<span class=\"bossn\">'+r.boss+'</span>',v:r.last,cv:r.cum-1,")
rep("${all.map(a=>{const c=cums.find(z=>z.nm===(a.me?S.fundName:a.nm.split(' · ')[0]));return {a,cv:c?c.v:0}}).sort(",
    "${all.map(a=>({a,cv:a.cv})).sort(")
# 3. le ruban ne recompte plus le trimestre clos : le latent n'existe qu'en séance
rep("return {y0,base:v,now:cur*(1+liveNet())/v*100,","return {y0,base:v,now:cur*(1+((S.phase==='events'&&S.live)?liveNet():0))/v*100,")
# 4. volatilité homogène : un segment compte des points au prorata du temps qu'il couvre
rep("const TAPEM=48;","const TAPEM=48;\n/* lot 78 : points au prorata du temps couvert — un trimestre fait toujours ~48 points, quel que soit\n   le nombre de mises à jour ; l'amplitude par point est alors la même partout */\nfunction tapeM(dt){return Math.max(3,Math.round(TAPEM*Math.max(0,dt)))}")
rep("bridgePts(last,tgt,TAPEM,hash32('tapeq'+S.q+'_'+(S.tape.seg++),S.seed),tapeVol(TAPEM,t1-t0))",
    "const mq=tapeM(t1-t0);bridgePts(last,tgt,mq,hash32('tapeq'+S.q+'_'+(S.tape.seg++),S.seed),tapeVol(mq,t1-t0))")
rep("bridgePts(last,tgt,TAPEM,hash32('settle'+S.q,S.seed),tapeVol(TAPEM,dtl)).forEach(",
    "bridgePts(last,tgt,tapeM(dtl),hash32('settle'+S.q,S.seed),tapeVol(tapeM(dtl),dtl)).forEach(")
D1="t-(k?ts[k-1]:0)"
rep("bridgePts(last,nv,TAPEM,hash32('rivq'+j+'_'+tq+'_'+k,S.seed),tapeVol(TAPEM,t-(k?ts[k-1]:0),rivV(r)))",
    "bridgePts(last,nv,tapeM("+D1+"),hash32('rivq'+j+'_'+tq+'_'+k,S.seed),tapeVol(tapeM("+D1+"),"+D1+",rivV(r)))")
D2="Math.max(0.04,1-(ts.length?ts[ts.length-1]:0))"
rep("bridgePts(last,nv,TAPEM,hash32('rivs'+j+'_'+tq,S.seed),tapeVol(TAPEM,"+D2+",rivV(r)))",
    "bridgePts(last,nv,tapeM("+D2+"),hash32('rivs'+j+'_'+tq,S.seed),tapeVol(tapeM("+D2+"),"+D2+",rivV(r)))")
# 5. minuteur sur les appels de marge : faute de réponse, le prime broker liquide la moitié
rep("function armTimer(fn){","function armTimer(fn,lbl){")
rep("""<span class="tlb">sans choix : l'option du bas</span>`;""","""<span class="tlb">${lbl||"sans choix : l'option du bas"}</span>`;""")
rep("document.querySelectorAll('.choice[data-t]').forEach(b=>b.onclick=()=>{",
    "if(ev.mg)armTimer(()=>{const b=app.querySelector('.choice[data-t=\"1\"]');if(b&&!b.disabled)b.click()},'sans choix : le prime broker liquide la moitié');\n document.querySelectorAll('.choice[data-t]').forEach(b=>b.onclick=()=>{clearTimer();")
rep("const g=gauge(o.c,0,`Accident de levier : ${ev.t}`);","const g=gauge(o.c,0,`${ev.mg?'Appel de marge':'Accident de levier'} : ${ev.t}`);")
open(P,'w',encoding='utf-8').write(s);print('ok')
