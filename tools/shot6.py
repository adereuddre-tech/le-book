# Capture de l'écran d'exécution (anecdote du desk) et de sa carte de résultat.
from playwright.sync_api import sync_playwright
import sys,os
F=os.path.abspath(sys.argv[1]);P=sys.argv[2];SEED=sys.argv[3] if len(sys.argv)>3 else '3'
BOT=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'shot.py')).read().split('BOT="""')[1].split('"""')[0]
BOT=BOT.replace("if($('#commok'))","{const cg=document.querySelector('.card.commgo');if(cg){c(cg);return 1}}\nif($('#commok'))")
CLEAN="()=>{document.querySelectorAll('.mbox').forEach(e=>e.parentElement.remove());const t=document.getElementById('toast');if(t)t.remove()}"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    pg=b.new_page(viewport={'width':380,'height':900},device_scale_factor=2)
    for essai in range(8):
        pg.goto('file://'+F);pg.wait_for_timeout(400)
        for i in range(400):
            if pg.evaluate("()=>typeof S!=='undefined'&&S&&S.phase==='book'&&!!document.getElementById('send')"): break
            pg.evaluate(BOT,"false");pg.wait_for_timeout(20)
        pg.evaluate(CLEAN);pg.evaluate("()=>document.getElementById('send').click()");pg.wait_for_timeout(700);pg.evaluate(CLEAN)
        ok=False
        for i in range(40):
            if pg.evaluate("()=>document.body.innerText.includes('passent vos ordres')&&document.querySelectorAll('.choice').length>0"): ok=True;break
            pg.evaluate(BOT,"false");pg.wait_for_timeout(40)
        pg.evaluate(CLEAN)
        if ok: break
    print('essais',essai)
    pg.screenshot(path=P+'_exec.png',full_page=True)
    txt=pg.evaluate("()=>[...document.querySelectorAll('.choice')].map(b=>b.innerText.replace(/\\n/g,' | '))")
    print(*txt,sep='\n---\n')
    pg.evaluate("()=>{const c=[...document.querySelectorAll('.choice')];c[0].click()}");pg.wait_for_timeout(900);pg.evaluate(CLEAN)
    pg.screenshot(path=P+'_res.png',full_page=True)
    b.close()
