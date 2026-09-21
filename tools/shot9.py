# Lot 47 : minuteur en pause sous une fenêtre ; « Abandonner » au débriefing et son verdict.
from playwright.sync_api import sync_playwright
import os,sys
F=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else 'index.html')
BOT=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'shot.py')).read().split('BOT="""')[1].split('"""')[0]
BOT=BOT.replace("if($('#commok'))","{const cg=document.querySelector('.card.commgo');if(cg){c(cg);return 1}}\nif($('#commok'))")
CLEAN="()=>{const m=document.getElementById('modal');if(m)m.style.display='none';document.querySelectorAll('#gold').forEach(e=>e.remove())}"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    pg=b.new_page(viewport={'width':380,'height':850},device_scale_factor=2)
    pg.goto('file://'+F);pg.wait_for_timeout(400)
    for i in range(600):
        if pg.evaluate("()=>!!document.querySelector('.evopt')&&document.getElementById('evtimer')&&document.getElementById('evtimer').classList.contains('on')"): break
        pg.evaluate(CLEAN);pg.evaluate(BOT,"false");pg.wait_for_timeout(25)
    pg.evaluate(CLEAN);pg.wait_for_timeout(1200)
    t0=pg.evaluate("()=>document.querySelector('#evtimer').innerText")
    pg.evaluate("()=>showGauge('lp')");pg.wait_for_timeout(3200)
    t1=pg.evaluate("()=>document.querySelector('#evtimer').innerText")
    pg.screenshot(path='shots/l47_pause.png')
    pg.evaluate(CLEAN);pg.wait_for_timeout(2200)
    t2=pg.evaluate("()=>document.querySelector('#evtimer').innerText")
    print('minuteur avant',t0.split()[0],'| après 3,2 s sous la fenêtre',t1.split()[0],'| 2,2 s après fermeture',t2.split()[0])
    for i in range(3000):
        if pg.evaluate("()=>!!document.getElementById('quit')"): break
        pg.evaluate(CLEAN);pg.evaluate(BOT,"false");pg.wait_for_timeout(20)
    pg.evaluate(CLEAN);pg.wait_for_timeout(300)
    q=pg.query_selector('#quit');q.scroll_into_view_if_needed();pg.evaluate("()=>{const n=document.getElementById('nx');n.scrollIntoView({block:'center'})}")
    pg.screenshot(path='shots/l47_quitbtn.png')
    pg.evaluate("()=>document.getElementById('quit').click()");pg.wait_for_timeout(400)
    pg.screenshot(path='shots/l47_confirm.png')
    pg.evaluate("()=>document.getElementById('quitok').click()");pg.wait_for_timeout(1500);pg.evaluate(CLEAN)
    print(pg.evaluate("()=>[S.over,(document.querySelector('h1.verdict')||{}).innerText]"))
    b.close()
