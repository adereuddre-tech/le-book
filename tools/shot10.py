# Lot 49 : écran de création (trois choix), trois paliers de cartes, emblèmes des concurrents.
from playwright.sync_api import sync_playwright
import os,sys
F=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else 'index.html')
CLEAN="()=>{const m=document.getElementById('modal');if(m)m.style.display='none';document.querySelectorAll('#gold').forEach(e=>e.remove())}"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    pg=b.new_page(viewport={'width':380,'height':800},device_scale_factor=2)
    pg.goto('file://'+F);pg.wait_for_timeout(400);pg.evaluate(CLEAN)
    pg.evaluate("()=>{const f=document.getElementById('found');if(f)f.click()}");pg.wait_for_timeout(500);pg.evaluate(CLEAN)
    print('groupes :',pg.evaluate("()=>[...document.querySelectorAll('.pickhead h2')].map(h=>h.innerText.split('\\n')[0])"))
    el=pg.query_selector_all('.pickhead')[1];el.scroll_into_view_if_needed();pg.screenshot(path='shots/l49_diff.png')
    pg.evaluate("()=>{const g=document.getElementById('go');if(g)g.click()}");pg.wait_for_timeout(500);pg.evaluate(CLEAN)
    for t in ['bronze','argent','or']:
        pg.evaluate("t=>{GOLDQ.length=0;goldOn=false;goldPop({v:'trophy',tier:t,k:'OBJECTIF DU TRIMESTRE',t:'La main ferme',d:'Tenir le book sans ajustement jusqu\\'à la clôture.',g:'+0,4 M$ de bonus sur vos gains'})}",t)
        pg.wait_for_timeout(2200);c=pg.query_selector('.gcard');c.screenshot(path=f'shots/l49_{t}.png')
    pg.evaluate(CLEAN)
    print('emblèmes des concurrents :',pg.evaluate("()=>S.rivals.map((r,j)=>r.nm+' → '+CRESTS[RIVCREST[j]].nm)"),'| choix joueur :',pg.evaluate("()=>document.querySelectorAll('#crests .crestb').length"))
    b.close()
