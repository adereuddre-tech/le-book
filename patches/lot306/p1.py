p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# 1. plus de frais de déménagement ; loyers +15 % (le trimestre de déménagement amorti, et la valeur des avantages)
rep("function offBp(){const o=OFF();return o.bp+((S.officePrev!=null&&(S.office??0)!==S.officePrev)?o.bp:0)}","function offBp(){return OFF().bp}   /* lot 306 : plus de frais de déménagement */")
for a,b in [("id:'defense',ic:'🏢',nm:\"La Défense, tour B, 27e étage\",bp:10","id:'defense',ic:'🏢',nm:\"La Défense, tour B, 27e étage\",bp:12")]:
    rep(a,b)
import re
for idv,old,new in [('montaigne',20,23),('mayfair',30,35),('geneve',40,46),('greenwich',50,58),('singapour',60,69),('monaco',70,80)]:
    o=re.search(r"\{id:'%s',ic:'[^']*',nm:\"[^\"]*\",bp:%d,"%(idv,old),s);assert o,idv
    s=s[:o.start()]+o.group(0).replace(f"bp:{old},",f"bp:{new},")+s[o.end():]
rep("   déménager coûte un trimestre du nouveau loyer. La Défense est le défaut, compris dans le loyer du back office. */","   lot 306 : déménager est gratuit, les loyers ont pris 15 %. */")
# 2. écran : pas de ligne de déménagement ; une adresse hors trésorerie est verrouillée
rep("""<span>${mm(OFF().bp*1e-4*budNav())} par trimestre${cur!==base&&OFF().bp?` · déménagement ${mm(OFF().bp*1e-4*budNav())}`:''}</span></div>""","""<span>${mm(OFF().bp*1e-4*budNav())} par trimestre</span></div>""")
rep("""chaque adresse fait un peu mieux que son loyer. Déménager coûte un trimestre du nouveau loyer.</p>""","""chaque adresse fait un peu mieux que son loyer, et reprend les avantages des précédentes. Déménager ne coûte rien de plus que le nouveau loyer.</p>""")
rep("""  <div class="offl">${OFFICES.map((o,i)=>`<button class="offb${i===cur?' on':''}" data-off="${i}"><b>${o.ic} ${o.nm}</b><span>${o.bp} pb</span><small>${o.d}</small></button>`).join('')}</div></div>`;
 el.querySelectorAll('.offb').forEach(b=>b.onclick=()=>{S.office=+b.dataset.off;setOps();drawBuds();refreshStatus()})}""",
"""  <div class="offl">${OFFICES.map((o,i)=>{const ok=offOk(i);return `<button class="offb${i===cur?' on':''}" data-off="${i}"${ok?'':' disabled'}><b>${o.ic} ${o.nm}</b><span>${o.bp} pb${ok?'':' · hors trésorerie'}</span><small>${o.d}</small></button>`}).join('')}</div></div>`;
 el.querySelectorAll('.offb').forEach(b=>b.onclick=()=>{if(b.disabled)return;S.office=+b.dataset.off;setOps();drawBuds();refreshStatus()})}
/* lot 306 : une adresse n'est accessible que si la caisse paie le budget du trimestre avec son loyer */
function offOk(i){const cur=S.office==null?0:S.office,base=S.officePrev==null?0:S.officePrev;if(i===cur||i===base||OFFICES[i].bp<=OFFICES[cur].bp)return true;
 const purse=mgrCash()+(S.qOps||0),sv=S.office;S.office=i;const c=opsT();S.office=sv;return c<=purse+1e-12}""")
open(p,'w',encoding='utf-8').write(s)
