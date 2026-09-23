# Écran du budget : onze crans, nom du cran au-dessus de la rangée, coût en pb et en monnaie.
from playwright.sync_api import sync_playwright
import sys,os
F=os.path.abspath(sys.argv[1]);P=sys.argv[2]
BOT=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'shot.py')).read().split('BOT="""')[1].split('"""')[0]
CLEAN="()=>{document.querySelectorAll('.mbox').forEach(e=>e.parentElement.remove());const t=document.getElementById('toast');if(t)t.remove()}"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    pg=b.new_page(viewport={'width':380,'height':900},device_scale_factor=2)
    pg.goto('file://'+F);pg.wait_for_timeout(400)
    for i in range(300):
        if pg.evaluate("()=>!!document.querySelector('#buds .lvl')"): break
        pg.evaluate(BOT,"false");pg.wait_for_timeout(25)
    pg.evaluate(CLEAN);pg.wait_for_timeout(300)
    pg.screenshot(path=P+'_budget.png',full_page=True)
    # cran maximal sur la salle de marché, pour voir les effets et le coût en monnaie
    pg.evaluate("()=>document.querySelector('#buds .lvl[data-b=\"exec\"][data-i=\"6\"]').click()")
    pg.wait_for_timeout(500);pg.evaluate(CLEAN)
    pg.screenshot(path=P+'_max.png',full_page=True)
    print(pg.evaluate("()=>[...document.querySelectorAll('#buds .lvl')].slice(0,7).map(b=>b.innerText.replace(/\\n/g,' '))"))
    b.close()
