# Lot 34 : trois tirages de nom, l'écusson assorti doit suivre ; puis clic sur un écusson, il doit rester.
from playwright.sync_api import sync_playwright
import sys,os
F=os.path.abspath(sys.argv[1]);P=sys.argv[2]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    pg=b.new_page(viewport={'width':380,'height':800},device_scale_factor=2)
    pg.goto('file://'+F);pg.wait_for_timeout(800)
    pg.evaluate("()=>{document.querySelectorAll('.mbox').forEach(e=>e.parentElement.remove())}")
    log=[]
    for k in range(3):
        pg.click('#shuffle');pg.wait_for_timeout(200)
        log.append(pg.evaluate("()=>[fundName,fundCrest,CRESTS[fundCrest].nm,document.querySelector('.crestb.on').dataset.c]"))
        pg.query_selector('.namebox').screenshot(path=f'{P}_tirage{k}.png')
    pg.click('[data-c=\"9\"]');pg.wait_for_timeout(100)
    for k in range(3):
        pg.click('#shuffle');pg.wait_for_timeout(100)
        log.append(pg.evaluate("()=>[fundName,fundCrest,CRESTS[fundCrest].nm,document.querySelector('.crestb.on').dataset.c]"))
    pg.query_selector('.namebox').screenshot(path=f'{P}_fige.png')
    print(*log,sep='\n')
    b.close()
