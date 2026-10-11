p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
# Jean-Kevin : tous les trimestres, et il apprend — 50 % de réussite, +5 points à chaque appel, plafond 90 % (au 8e appel)
rep("""d:"Il « optimise » vos ordres du trimestre : une chance sur deux de −20 % sur tous les coûts, une sur deux de +20 % (bug). Le verdict tombe à l'exécution."}""",
    """d:"Il « optimise » vos ordres du trimestre : −20 % sur tous les coûts si le tableur marche, +20 % s'il plante. Le verdict tombe à l'exécution. Disponible chaque trimestre ; il apprend : 50 % de réussite au premier appel, 5 points de plus à chaque fois, jusqu'à 90 %."}""")
rep("""function pwBack(id){const l=S.pwLast&&S.pwLast[id];return l==null?0:l+4}""",
    """function pwBack(id){const l=S.pwLast&&S.pwLast[id];return l==null?0:l+(id==='jk'?1:4)}   /* lot 302 : Jean-Kevin chaque trimestre */
function jkP(){return Math.min(0.90,0.50+0.05*(S.pwJKn||0))}""")
rep("""  if(o.id==='jk')S.pwJK=prng32(hash32('jk'+S.q,S.seed))()<0.5?0.8:1.2;""",
    """  if(o.id==='jk'){S.pwJK=prng32(hash32('jk'+S.q,S.seed))()<jkP()?0.8:1.2;S.pwJKn=(S.pwJKn||0)+1}""")
rep("""<span class="hint">un coup de pouce chacun par an</span>""","""<span class="hint">un coup de pouce chacun par an · Jean-Kevin chaque trimestre</span>""")
rep("""<b>${o.ic} ${o.nm} · ${o.t}</b><small>${o.d} <i>· ${st}</i></small>""","""<b>${o.ic} ${o.nm} · ${o.t}</b><small>${o.d} <i>· ${st}${o.id==='jk'?` · réussite ${Math.round((pwOn('jk')&&S.pwLast&&S.pwLast.jk===S.q?Math.min(0.9,jkP()-0.05):jkP())*100)} %`:''}</i></small>""")
open(p,'w',encoding='utf-8').write(s)
s=open(p,encoding='utf-8').read()
rep("""toast(S.pwJK<1?'🐣 Le tableur de Jean-Kevin marche : coûts −20 % ce trimestre.':'🐣 Le tableur de Jean-Kevin plante : coûts +20 % ce trimestre.')}""",
    """toast((S.pwJK<1?'🐣 Le tableur de Jean-Kevin marche : coûts −20 % ce trimestre.':'🐣 Le tableur de Jean-Kevin plante : coûts +20 % ce trimestre.')+` Il apprend : ${Math.round(jkP()*100)} % de réussite la prochaine fois.`)}""")
open(p,'w',encoding='utf-8').write(s)
