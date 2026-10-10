p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
# valeur relative : les paires du trimestre passent au-dessus des marchés du book
rep("""  <div class="block"><div class="blockhead"><h2>Le book</h2><span class="hint">unités de risque, de −${S.maxk} à +${S.maxk}</span></div>""",
    """  ${PROF().pairs?'<div class="block" id="stypw"></div>':''}
  <div class="block"><div class="blockhead"><h2>Le book</h2><span class="hint">unités de risque, de −${S.maxk} à +${S.maxk}</span></div>""")
rep("""  <div class="block" id="stypw"${PROF().pairs||PROF().atk||PROF().tailH?'':' hidden'}></div>""",
    """  ${PROF().pairs?'':`<div class="block" id="stypw"${PROF().atk||PROF().tailH?'':' hidden'}></div>`}   <!-- lot 295 : les paires au-dessus du book -->""")
open(p,'w',encoding='utf-8').write(s)
