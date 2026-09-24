# Nettoyage, deuxième passe : captures pleine page du budget, de l'annonce, de l'exécution,
# d'une dépêche et de son résultat. Usage : shot13.py fichier préfixe
from playwright.sync_api import sync_playwright
import os,sys
F=os.path.abspath(sys.argv[1]);P=sys.argv[2]
BOT=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'shot.py')).read().split('BOT="""')[1].split('"""')[0]
BOT=BOT.replace("if($('#commok'))","{const cg=document.querySelector('.card.commgo');if(cg){c(cg);return 1}}\nif($('#commok'))")
CLEAN="()=>{const m=document.getElementById('modal');if(m)m.style.display='none';document.querySelectorAll('#gold').forEach(e=>e.remove());const t=document.getElementById('toast');if(t)t.remove()}"
def until(pg,cond,n=600):
    for i in range(n):
        if pg.evaluate(cond): return True
        pg.evaluate(CLEAN);pg.evaluate(BOT,"false");pg.wait_for_timeout(15)
    return False
def shot(pg,nm):
    pg.wait_for_timeout(3400);pg.evaluate(CLEAN);pg.evaluate("()=>window.scrollTo(0,0)")
    pg.screenshot(path=f'{P}_{nm}.png',full_page=True);print(nm,pg.evaluate("()=>document.body.scrollHeight"))
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    pg=b.new_page(viewport={'width':380,'height':800},device_scale_factor=1)
    pg.goto('file://'+F);pg.wait_for_timeout(300)
    pg.evaluate("()=>{newGame(4242,'fonda','std','inhouse','std','mid','ext','normal');S.fundName='Essai';S.tuto=99;phaseOpen()}")
    until(pg,"()=>S.phase==='budget'&&!!document.querySelector('#buds')");pg.evaluate(CLEAN);shot(pg,'budget')
    until(pg,"()=>!!document.querySelector('.card.commgo')");shot(pg,'annonce')
    until(pg,"()=>document.body.innerText.includes('passent vos ordres')");shot(pg,'exec')
    until(pg,"()=>!!document.querySelector('.evopt')");shot(pg,'depeche')
    pg.evaluate("()=>{const o=[...document.querySelectorAll('.evopt')];o[0].click()}");pg.wait_for_timeout(600);shot(pg,'depeche_res')
    b.close()
