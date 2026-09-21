# Cartes dorées des bonus : une capture par visuel, à 380 px.
from playwright.sync_api import sync_playwright
import os,sys
F=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else 'index.html')
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    pg=b.new_page(viewport={'width':380,'height':720},device_scale_factor=2)
    pg.goto('file://'+F);pg.wait_for_timeout(500)
    pg.evaluate("()=>{document.querySelectorAll('.mbox').forEach(e=>e.parentElement.remove());const f=document.getElementById('found');if(f)f.click()}")
    pg.wait_for_timeout(400)
    pg.evaluate("()=>{document.querySelectorAll('.mbox').forEach(e=>e.parentElement.remove());const g=document.getElementById('go');if(g)g.click()}")
    pg.wait_for_timeout(600)
    cards=[{'v':'crown','k':'TROPHÉE · ANNÉE 1','t':"Fonds macro de l'année",'d':"Le jury vous décerne le prix, devant les quatre maisons que vous affrontez.",'g':"souscription 50 M$ (+5 %) · investisseurs +8 · comité +4"},
           {'v':'doors','k':'CROISSANCE · ENCOURS ×2','t':'Les dark pools vous ouvrent leurs portes','d':"Vous traitez désormais là où personne ne voit passer vos ordres.",'g':"plafonds de capacité ×2 · coûts d'exécution −10 %"},
           {'v':'swan','k':'RARE','t':'Le cygne noir apprivoisé','d':"Un trimestre où presque tout le monde a perdu, et vous finissez devant.",'g':"souscription 30 M$ (+3 %) · investisseurs +5"}]
    for i,c in enumerate(cards):
        pg.evaluate("c=>{document.querySelectorAll('#gold').forEach(e=>e.remove());GOLDQ.length=0;goldOn=false;goldPop(c)}",c)
        pg.wait_for_timeout(2300)
        pg.screenshot(path=f'shots/l43_gold{i}.png')
    b.close()
