# Lot 198 : facteurs affichés incohérents entre eux (captures d'Antoine, même instant, NQ).
# (a) Fenêtre d'un marché : « Exposition × lecture » était en convention brute (Liquidité = dollar : exposition +0,35,
#     lecture −0,35) alors que la ligne du book et les tuiles affichent la liquidité mondiale = −dollar (FSG) : « Liquid. −− ».
#     Le tableau applique désormais FSG aux deux colonnes (le produit, donc l'effet, ne change pas).
# (b) Flèches « lecture » des tuiles et du tableau « Lecture du desk » : calculées à part (somme des rumeurs achetées, sans
#     moyenne, sans l'intuition), donc sans rapport avec la lecture de la fenêtre du marché (moyenne ×2,2 + intuition).
#     Une seule fonction, factRead(), alimente S.factEst, les flèches, le libellé et le détail ; cran = |lecture| / 0,45.
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
rep("""function rumorEst(){
 const b=S.rumors.filter(r=>r.bought);
 const est=[0,0,0,0];b.forEach(r=>{const p=r.p||RELP[r.rel];r.v.forEach((z,k)=>est[k]+=(2*p-1)*z)});
 S.factEst=est.map(z=>z/Math.max(1,b.length)*2.2);
 if(S.hunch&&HUNCHW)S.factEst[S.hunch.k]+=(S.hunch.up?1:-1)*HUNCHW;   /* lot 77 */
}""","""/* lot 198 : la lecture du desk, convention brute (liquidité = dollar) ; une seule source pour tout l'affichage */
function factRead(){
 const b=(S.rumors||[]).filter(r=>r.bought);
 const est=[0,0,0,0];b.forEach(r=>{const p=r.p||RELP[r.rel];r.v.forEach((z,k)=>est[k]+=(2*p-1)*z)});
 const f=est.map(z=>z/Math.max(1,b.length)*2.2);
 if(S.hunch&&HUNCHW)f[S.hunch.k]+=(S.hunch.up?1:-1)*HUNCHW;   /* lot 77 */
 return f;
}
function rumorEst(){S.factEst=factRead()}""")
rep("""function readScore(k){
 const b=(S.rumors||[]).filter(r=>r.bought);if(!b.length)return null;
 let z=0;b.forEach(r=>{const p=r.p||RELP[r.rel];z+=(2*p-1)*r.v[k]/2});return z*FSG[k];
}""","""function readScore(k){
 if(!(S.rumors||[]).some(r=>r.bought)&&!S.hunch)return null;
 return factRead()[k]*FSG[k];   /* lot 198 : convention d'affichage, comme la fenêtre du marché */
}""")
rep("let wsum=0;b.forEach(r=>{const z=r.v[k],p=r.p||RELP[r.rel];wsum+=(2*p-1)*z/2});","const wsum=factRead()[k]*FSG[k];   /* lot 198 */")
rep("et ses impacts prétendus sont additionnés. Score net par facteur : ${FACT.map((f,k)=>{let z=0;b.forEach(r=>{const p=r.p||RELP[r.rel];z+=(2*p-1)*r.v[k]/2});return `${f.id} ${z>=0?'+':'−'}${dec(Math.abs(z),1)}`}).join(' · ')}.",
    "et leurs impacts prétendus sont moyennés. Lecture par facteur, la même que dans le détail d'un marché : ${FACT.map((f,k)=>{const z=factRead()[k]*FSG[k];return `${f.id} ${z>=0?'+':'−'}${dec(Math.abs(z),2)}`}).join(' · ')}. Une flèche = 0,45.")
rep("XP.fac.map((o,k)=>[FACT[k].nm,`${o.b>=0?'+':'−'}${dec(Math.abs(o.b),2)} × ${o.f>=0?'+':'−'}${dec(Math.abs(o.f),2)}`,pc(o.v)])",
    "XP.fac.map((o,k)=>{const g=FSG[k],eb=o.b*g,ef=o.f*g;return [FACT[k].nm,`${eb>=0?'+':'−'}${dec(Math.abs(eb),2)} × ${ef>=0?'+':'−'}${dec(Math.abs(ef),2)}`,pc(o.v)]})")
open('index.html','w',encoding='utf-8').write(s);print('lot198 ok')
