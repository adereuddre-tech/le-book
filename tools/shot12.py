# Nettoyage : captures pleine page du desk/book et du débriefing (avant/après).
from playwright.sync_api import sync_playwright
import os,sys
F=os.path.abspath(sys.argv[1]);P=sys.argv[2]
BOT=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'shot.py')).read().split('BOT="""')[1].split('"""')[0]
BOT=BOT.replace("if($('#commok'))","{const cg=document.querySelector('.card.commgo');if(cg){c(cg);return 1}}\nif($('#commok'))")
CLEAN="()=>{const m=document.getElementById('modal');if(m)m.style.display='none';document.querySelectorAll('#gold').forEach(e=>e.remove());const t=document.getElementById('toast');if(t)t.remove()}"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    pg=b.new_page(viewport={'width':380,'height':800},device_scale_factor=1)
    pg.goto('file://'+F);pg.wait_for_timeout(300);pg.evaluate(CLEAN)
    pg.evaluate("()=>{try{localStorage.setItem('lebook_tuto','off')}catch(e){};newGame(4242,'fonda','std','inhouse','std','mid','ext','normal');S.fundName='Essai';S.tuto=99;phaseOpen()}");pg.wait_for_timeout(300)
    for i in range(300):
        if pg.evaluate("()=>S.phase==='book'&&!!document.getElementById('send')"): break
        pg.evaluate(CLEAN);pg.evaluate(BOT,"false");pg.wait_for_timeout(20)
    pg.evaluate(CLEAN);pg.evaluate("()=>{const b=document.getElementById('applymodel');if(b)b.click()}");pg.wait_for_timeout(400);pg.evaluate(CLEAN)
    pg.screenshot(path=P+'_book.png',full_page=True)
    print('hauteur book',pg.evaluate("()=>document.body.scrollHeight"))
    for i in range(3000):
        if pg.evaluate("()=>S.phase==='debrief'&&!!document.getElementById('nx')"): break
        pg.evaluate(CLEAN);pg.evaluate(BOT,"false");pg.wait_for_timeout(15)
    pg.wait_for_timeout(3600);pg.evaluate(CLEAN)
    pg.screenshot(path=P+'_debrief.png',full_page=True)
    print('hauteur débrief',pg.evaluate("()=>document.body.scrollHeight"))
    b.close()
