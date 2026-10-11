p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
# un coût s'affiche toujours avec son signe moins ; un coût négatif (on est payé pour offrir de la liquidité) avec un plus
rep("""const mn=x=>`<b class="${cls(x)}">${x>=0?'+':'−'}${mm(Math.abs(x))}</b>`;""",
    """const mn=x=>`<b class="${cls(x)}">${x>=0?'+':'−'}${mm(Math.abs(x))}</b>`;
/* lot 300 : un coût (positif = on paie) affiché en négatif */
const cS=c=>`${c>0?'−':'+'}${mm(Math.abs(c))}`,cB=b=>`${b>0?'−':'+'}${dec(Math.abs(b),1)} pb`,cC=c=>c>0?'neg-g':'pos-g';""")
rep("""`${dec(t.bp,1)} pb`,`−${mm(t.cost)}`])}}""","""cB(t.bp),cS(t.cost)])}}""")
rep("""   <span class="av neg-g">${dec(t.bp,1)} pb · ${mm(t.cost)}</span></div>`;""","""   <span class="av ${cC(t.cost)}">${cB(t.bp)} · ${cS(t.cost)}</span></div>`;""")
rep("""<span>Coût total des ordres</span><b class="neg-g">${mm(tot)} · ${(tot/S.nav*1e4).toFixed(0)} pb de l'encours</b>""",
    """<span>Coût total des ordres</span><b class="${cC(tot)}">${cS(tot)} · ${tot>0?'−':'+'}${Math.abs(tot/S.nav*1e4).toFixed(0)} pb de l'encours</b>""")
rep("""<b style="color:#fff;font-size:17px">−${mm(tot)}</b></div>
   <div class="kv"><span>Impact de marché, pour le fonds</span><b class="neg-g">${mm(Math.abs(execImpactAmt(tot,1,S.leakQ)))}</b></div>`""",
    """<b style="color:#fff;font-size:17px">${cS(tot)}</b></div>
   <div class="kv"><span>Impact de marché, pour le fonds</span>${mn(execImpactAmt(tot,1,S.leakQ))}</div>`""")
rep("""<span class="av neg-g">${dec(o.t.bp,1)} pb · ${mm(o.t.cost)}</span></div>`).join('')}""","""<span class="av ${cC(o.t.cost)}">${cB(o.t.bp)} · ${cS(o.t.cost)}</span></div>`).join('')}""")
open(p,'w',encoding='utf-8').write(s)
s=open(p,encoding='utf-8').read()
rep("""['Impact de marché du trimestre',`${(-S.execSlipQ/S.nav*1e4).toFixed(0)} pb`""","""['Impact de marché du trimestre',`${S.execSlipQ<0?'−':'+'}${Math.abs(S.execSlipQ/S.nav*1e4).toFixed(0)} pb`""")
rep("""out.push(`<span class="stk">impact fonds <em class="neg-g">−${mm(Math.abs(im))}</em></span>`);""","""out.push(`<span class="stk">impact fonds <em class="${cls(im)}">${im<0?'−':'+'}${mm(Math.abs(im))}</em></span>`);""")
open(p,'w',encoding='utf-8').write(s)
s=open(p,encoding='utf-8').read()
rep("""out.push(`<span class="stk">ordres <em class="${d<0?'pos-g':'neg-g'}">${d<0?'−':'+'}${mm(Math.abs(d))}</em></span>`);""",
    """out.push(`<span class="stk">ordres <em class="${d<0?'pos-g':'neg-g'}">${d<0?'+':'−'}${mm(Math.abs(d))}</em></span>`);   /* lot 300 : du point de vue de votre caisse */""")
open(p,'w',encoding='utf-8').write(s)
