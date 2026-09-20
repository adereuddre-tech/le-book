# Captures du lot 32 : barre d'état, pop-up Confiance, règles, rapport final sur mort d'encours.
from playwright.sync_api import sync_playwright
import sys,os
F=os.path.abspath(sys.argv[1]); P=sys.argv[2]
BOT=open(os.path.join(os.path.dirname(__file__),'shot.py')).read().split('BOT="""')[1].split('"""')[0]
CLEAN="()=>{document.querySelectorAll('.mbox').forEach(e=>e.parentElement.remove());const t=document.getElementById('toast');if(t)t.remove()}"
def run(pg,stop):
    for i in range(4000):
        if pg.evaluate(BOT,stop)=='STOP':return
        pg.wait_for_timeout(30)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    pg=b.new_page(viewport={'width':380,'height':800},device_scale_factor=2)
    pg.goto('file://'+F)
    # règles
    pg.wait_for_timeout(500)
    if pg.query_selector('#tutooff'): pg.click('#tutooff')
    if pg.query_selector('#found'): pg.click('#found')
    pg.wait_for_timeout(600)
    pg.query_selector('.mbox').screenshot(path=P+'_intro.png'); pg.evaluate(CLEAN)
    pg.evaluate("()=>{document.querySelectorAll('details.wire').forEach(d=>d.open=true);const h=document.getElementById('introprose');if(h)h.style.display=''}")
    pg.wait_for_timeout(300)
    pg.query_selector('.rules').screenshot(path=P+'_regles.png')
    # partie jusqu'au premier débriefing
    run(pg,"S&&S.phase==='debrief'&&!!document.getElementById('nx')")
    pg.wait_for_timeout(1500); pg.evaluate(CLEAN)
    pg.query_selector('.status').screenshot(path=P+'_barre.png')
    pg.click('[data-gauge=lp]'); pg.wait_for_timeout(700)
    pg.query_selector('.mbox').screenshot(path=P+'_confiance.png')
    pg.evaluate(CLEAN)
    pg.click('[data-gauge=cap]'); pg.wait_for_timeout(700)
    pg.query_selector('.mbox').screenshot(path=P+'_capital.png')
    pg.evaluate(CLEAN)
    # rapport final sur mort d'encours, avec une vieille cause 'rc'
    pg.evaluate("()=>{S.over='rc';screenFinal()}"); pg.wait_for_timeout(1500); pg.evaluate(CLEAN)
    pg.query_selector('h1.verdict').evaluate("e=>e.scrollIntoView()")
    pg.screenshot(path=P+'_final.png')
    b.close()
