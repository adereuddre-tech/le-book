# Lots 51-53 : indicateur de rendement attendu (trois dosages), signaux par style, cartons.
from playwright.sync_api import sync_playwright
import os,sys
F=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else 'index.html')
BOT=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'shot.py')).read().split('BOT="""')[1].split('"""')[0]
BOT=BOT.replace("if($('#commok'))","{const cg=document.querySelector('.card.commgo');if(cg){c(cg);return 1}}\nif($('#commok'))")
CLEAN="()=>{const m=document.getElementById('modal');if(m)m.style.display='none';document.querySelectorAll('#gold').forEach(e=>e.remove())}"
def book(pg,prof,size,tag):
    pg.goto('file://'+F);pg.wait_for_timeout(300);pg.evaluate(CLEAN)
    pg.evaluate("a=>{newGame(4242,a[0],'std','inhouse','std',a[1],'ext','normal');S.fundName='Essai';phaseOpen()}",[prof,size]);pg.wait_for_timeout(300);pg.evaluate(CLEAN)
    for i in range(300):
        if pg.evaluate("()=>typeof S!=='undefined'&&S&&S.phase==='book'&&!!document.getElementById('send')"): break
        pg.evaluate(CLEAN);pg.evaluate(BOT,"false");pg.wait_for_timeout(20)
    pg.evaluate(CLEAN);pg.evaluate("()=>{const b=document.getElementById('applymodel')||[...document.querySelectorAll('button')].find(x=>/modèle|desk/i.test(x.innerText)&&x.id!=='send');if(b)b.click()}");pg.wait_for_timeout(400);pg.evaluate(CLEAN)
    el=pg.query_selector('#xbook');el.scroll_into_view_if_needed();pg.evaluate(CLEAN);pg.screenshot(path=f'shots/l51_{tag}.png')
    print(tag,pg.evaluate("()=>[S.prof,S.size,document.getElementById('xbook').innerText.replace(/\\n/g,' | ').slice(0,160)]"))
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    pg=b.new_page(viewport={'width':380,'height':800},device_scale_factor=2)
    book(pg,'syst','small','facile_quant')
    book(pg,'fonda','mid','moyen_fonda')
    book(pg,'flux','mega','difficile_flux')
    pg.evaluate("()=>showGauge('lp')");pg.wait_for_timeout(400);pg.query_selector('.mbox').screenshot(path='shots/l53_conf.png')
    b.close()
