# Captures d'écran pleine page aux moments clés du ruban : dépêche, mi-parcours, débriefing.
# Usage : shot5.py fichier préfixe [attente_ms]   — l'attente laisse finir le tracé (5 s).
from playwright.sync_api import sync_playwright
import sys,os
F=os.path.abspath(sys.argv[1]);P=sys.argv[2];WAIT=int(sys.argv[3]) if len(sys.argv)>3 else 5600
FRAMES='--film' in sys.argv
BOT=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'shot.py')).read().split('BOT="""')[1].split('"""')[0]
# l'annonce aux investisseurs se valide au clic sur une carte (lot 4) : shot.py l'ignorait
BOT=BOT.replace("if($('#commok'))","{const cg=document.querySelector('.card.commgo');if(cg){c(cg);return 1}}\nif($('#commok'))")
CLEAN="()=>{document.querySelectorAll('.mbox').forEach(e=>e.parentElement.remove());const t=document.getElementById('toast');if(t)t.remove()}"
STOPS=[('depeche',"!!document.querySelector('.evopt')"),
       ('mi',"document.body.innerText.includes('MI-PARCOURS')"),
       ('debrief',"S&&S.phase==='debrief'&&!!document.getElementById('nx')")]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    pg=b.new_page(viewport={'width':380,'height':800},device_scale_factor=2)
    pg.goto('file://'+F);pg.wait_for_timeout(500)
    for nm,stop in STOPS:
        for i in range(2500):
            r=pg.evaluate(BOT,stop)
            if r=='STOP':break
            pg.wait_for_timeout(25)
        print(nm,'arrêt après',i,'pas', pg.evaluate("()=>[S.phase,S.q,S.evIdx,(S.tape&&S.tape.pts.length)]"))
        pg.evaluate(CLEAN)
        if FRAMES:
            # Chromium sans écran n'échantillonne pas SMIL pendant le déroulé : on fige
            # l'animation et on la place à l'instant voulu, ce qui force l'échantillonnage.
            sel='.tape.big' if nm!='depeche' else '.tape'
            pg.evaluate("s=>document.querySelectorAll(s+' svg').forEach(v=>v.pauseAnimations())",sel)
            for k in range(6):
                pg.evaluate("a=>document.querySelectorAll(a[0]+' svg').forEach(v=>v.setCurrentTime(a[1]))",[sel,k])
                el=pg.query_selector(sel)
                if el: el.screenshot(path=f'{P}_{nm}_f{k}.png')
            continue
        for t,ms in (('a',1200),('b',WAIT)):
            pg.wait_for_timeout(ms if t=='a' else ms-1200);pg.evaluate(CLEAN)
            pg.screenshot(path=f'{P}_{nm}_{t}.png',full_page=False)
    b.close()
