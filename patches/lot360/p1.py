p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# A : un seul risque (celui affiché) et un seul seuil (la limite du comité), aussi pour l'encombrement des extrêmes
rep("""const LIM={vol:0.30,""","""const LIM={vol:0.327,""")   # ×1,09 : le risque affiché dépasse en moyenne de 9 % celui des positions seules
rep(""" const w=weights(S.k),sp=pvol(w),lv=limVol(),cc=clsConc(w),lc=limConc(),out=[];let lvl=0;""",""" const w=weights(S.k),sp=riskShown(w).total,lv=limVol(),cc=clsConc(w),lc=limConc(),out=[];let lvl=0;   /* lot 360 : le risque affiché */""")
rep("""function limRows(k){const w=weights(k),sp=pvol(w),""","""function limRows(k){const w=weights(k),sp=riskShown(w).total,""")
rep(""" const sp=pvol(wFin),vd=varDecomp(wFin),""",""" const sp=riskShown(wFin).total,vd=varDecomp(wFin),""")
rep(""" const v0=pvol(weights(raw));""",""" const v0=riskShown(weights(raw)).total;""")
rep(""" for(let it=0;it<14;it++){const v=pvol(weights(k));""",""" for(let it=0;it<14;it++){const v=riskShown(weights(k)).total;""")
rep(""" return {k,W,sc,mx,vol:pvol(weights(k))};""",""" return {k,W,sc,mx,vol:riskShown(weights(k)).total};""")
rep("""if(id==='ma'){S.pwMaK=[...S.k];const sp=pvol(weights(S.k));""","""if(id==='ma'){S.pwMaK=[...S.k];const sp=riskShown(weights(S.k)).total;""")
# nuage : les zones du comité (vert, ambre à la croisière, rouge à la limite)
rep(""" const xr=TAIL.x0/2,xa=Math.min(cruise()/2,xr*0.85),stX=[[0,'g'],[xa*0.5,'g'],[xa,'a'],[xr,'r']];""",""" const xr=limVol()/2,xa=cruise()/2,stX=[[0,'g'],[xa*0.5,'g'],[xa,'a'],[xr,'r']];   /* lot 360 : les zones du comité */""")
rep("""(TAIL.x0/2<xm?`<rect x="${f(X(TAIL.x0/2))}" y="${T}" width="${f(100-Rr-X(TAIL.x0/2))}" height="${f(100-B-T)}" fill="#D2463C" opacity=".10"/>`:'')""",
    """(cruise()/2<xm?`<rect x="${f(X(cruise()/2))}" y="${T}" width="${f(Math.max(0,Math.min(100-Rr,X(limVol()/2))-X(cruise()/2)))}" height="${f(100-B-T)}" fill="#DFA45B" opacity=".07"/>`:'')
  +(limVol()/2<xm?`<rect x="${f(X(limVol()/2))}" y="${T}" width="${f(100-Rr-X(limVol()/2))}" height="${f(100-B-T)}" fill="#D2463C" opacity=".12"/>`:'')
  +(LIM.red*limVol()/2<xm?`<rect x="${f(X(LIM.red*limVol()/2))}" y="${T}" width="${f(100-Rr-X(LIM.red*limVol()/2))}" height="${f(100-B-T)}" fill="#D2463C" opacity=".12"/>`:'')""")
# l'encombrement des extrêmes démarre à la limite du comité, en douceur (plus de cassure de pente)
rep("""function crowd(sp){return Math.min(2.5,1+2.5*Math.max(0,sp-0.20)/0.10)}""","""function crowd(sp){const L=(S&&S.bud&&typeof limVol==='function')?limVol(1):0.20,x=(sp-L)/0.10,sp4=Math.log1p(Math.exp(4*x-2))/4;return 1+1.5*Math.tanh(2.5*sp4/1.5)}   /* lot 360 : départ à la limite du comité, montée douce, plafond 2,5 */""")
open(p,'w',encoding='utf-8').write(s)
s=open(p,encoding='utf-8').read()
# scénarios « short » et « rogue » : la cible n'est plus la seule plus grosse ligne (bascule brutale), mais les plus grosses au prorata
rep(""" if(sc.tgt==='short'||sc.tgt==='rogue'){let bi=-1,bv=0;for(let i=0;i<N;i++){const a=sc.tgt==='short'?-k[i]:Math.abs(k[i]);if(a>bv){bv=a;bi=i}}
  if(bi>=0){const sy=INSTR[bi].sym;h[sy]=+((h[sy]||0)-Math.sign(k[bi])*sc.H).toFixed(3)}}""",
    """ if(sc.tgt==='short'||sc.tgt==='rogue'){const A=k.map(v=>Math.max(0,sc.tgt==='short'?-v:Math.abs(v))**3),T=A.reduce((a,b)=>a+b,0);   /* lot 360 : au prorata du cube */
  if(T>0)A.forEach((a,i)=>{if(a>0){const sy=INSTR[i].sym;h[sy]=+((h[sy]||0)-Math.sign(k[i])*sc.H*a/T).toFixed(4)}})}""")
open(p,'w',encoding='utf-8').write(s)
